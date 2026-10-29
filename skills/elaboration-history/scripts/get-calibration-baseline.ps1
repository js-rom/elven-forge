param(
    [Parameter(Mandatory = $true)][string]$LedgerPath
)

$ErrorActionPreference = "Stop"

$ledger = Get-Content -LiteralPath $LedgerPath -Raw -Encoding UTF8 | ConvertFrom-Json
$samples = New-Object System.Collections.Generic.List[object]
$excluded = New-Object System.Collections.Generic.List[object]
$totalDays = 0
$totalUcs = 0

foreach ($iteration in @($ledger.iterations)) {
    $ucCount = 0
    foreach ($item in @($iteration.scope)) {
        if ($item.counts_for_average -eq $true -and ($item.delivery_type -eq "full" -or $item.delivery_type -eq "slice")) {
            $ucCount++
        }
    }

    if ($iteration.include_in_average -ne $true -or $iteration.reliability -ne "high") {
        $reason = if ($iteration.excluded_reason) { $iteration.excluded_reason } else { "Not eligible for average" }
        $excluded.Add([ordered]@{ iteration = $iteration.iteration; reliability = $iteration.reliability; reason = $reason })
        continue
    }

    if ($ucCount -eq 0) {
        $excluded.Add([ordered]@{ iteration = $iteration.iteration; reliability = $iteration.reliability; reason = "No computable use case" })
        continue
    }

    $days = [double]$iteration.effective_days
    if ($days -le 0) {
        $excluded.Add([ordered]@{ iteration = $iteration.iteration; reliability = $iteration.reliability; reason = "No effective days" })
        continue
    }

    $daysPerUc = $days / $ucCount
    $totalDays += $days
    $totalUcs += $ucCount
    $samples.Add([ordered]@{
        iteration = $iteration.iteration
        effective_days = $days
        uc_count = $ucCount
        days_per_uc = $daysPerUc
    })
}

$values = @($samples | ForEach-Object { [double]$_.days_per_uc } | Sort-Object)
$sampleCount = $values.Count
$mean = $null
$median = $null
$min = $null
$max = $null
$range = @()
$weighted = $null

if ($sampleCount -gt 0) {
    $sum = 0
    foreach ($value in $values) { $sum += $value }
    $mean = $sum / $sampleCount
    $min = $values[0]
    $max = $values[$sampleCount - 1]
    $range = @($min, $max)
    if ($sampleCount % 2 -eq 0) {
        $mid = [int]($sampleCount / 2)
        $median = ($values[$mid - 1] + $values[$mid]) / 2
    } else {
        $median = $values[[math]::Floor($sampleCount / 2)]
    }
}

if ($totalUcs -gt 0) {
    $weighted = $totalDays / $totalUcs
}

$confidence = "low"
if ($samples.Count -ge 5 -and $totalUcs -ge 8) {
    $confidence = "high"
} elseif ($samples.Count -ge 3 -and $totalUcs -ge 5) {
    $confidence = "medium"
}

$sampleIterations = @()
foreach ($sample in $samples) { $sampleIterations += [string]$sample.iteration }
$perIteration = @()
foreach ($sample in $samples) { $perIteration += $sample }
$excludedIterations = @()
foreach ($item in $excluded) { $excludedIterations += $item }

$result = [ordered]@{
    source_cutoff = $ledger.last_updated
    sample_iterations = $sampleIterations
    sample_ucs = $totalUcs
    total_effective_days = $totalDays
    per_iteration = $perIteration
    mean_days_per_uc = $mean
    weighted_average_days_per_uc = $weighted
    median_days_per_uc = $median
    min_days_per_uc = $min
    max_days_per_uc = $max
    range = $range
    confidence = $confidence
    excluded_iterations = $excludedIterations
}

$result | ConvertTo-Json -Depth 8
