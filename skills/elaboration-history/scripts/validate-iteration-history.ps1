param(
    [Parameter(Mandatory = $true)][string]$LedgerPath,
    [string]$Repository = "."
)

$ErrorActionPreference = "Stop"
$errors = New-Object System.Collections.Generic.List[string]

$ledger = Get-Content -LiteralPath $LedgerPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($ledger.schema_version -ne 1) {
    $errors.Add("Unsupported schema_version: $($ledger.schema_version)")
}

$seen = @{}
$totalDays = 0
$totalUcs = 0

foreach ($iteration in @($ledger.iterations)) {
    $id = [string]$iteration.iteration
    if ($seen.ContainsKey($id)) {
        $errors.Add("Duplicate iteration: $id")
    } else {
        $seen[$id] = $true
    }

    $commitDays = @($iteration.commit_days)
    if ($null -ne $iteration.effective_days -and [int]$iteration.effective_days -ne $commitDays.Count) {
        $errors.Add("$id effective_days ($($iteration.effective_days)) does not match commit_days count ($($commitDays.Count))")
    }

    if ($iteration.include_in_average -eq $true -and $iteration.reliability -ne "high") {
        $errors.Add("$id is included in the average but reliability is $($iteration.reliability)")
    }

    $ucCount = 0
    foreach ($item in @($iteration.scope)) {
        if ($item.counts_for_average -eq $true) {
            if ($item.delivery_type -ne "full" -and $item.delivery_type -ne "slice") {
                $errors.Add("$id UC $($item.uc) counts for average but delivery_type is $($item.delivery_type)")
            }
            if ($iteration.include_in_average -eq $true) {
                $ucCount++
            }
        }
    }

    if ($iteration.include_in_average -eq $true) {
        $totalDays += [int]$iteration.effective_days
        $totalUcs += $ucCount
        if ($ucCount -eq 0) {
            $errors.Add("$id is included in the average but has no computable UC")
        }
    }

    if ($iteration.reliability -eq "high") {
        if ($null -eq $iteration.start_ref -or $null -eq $iteration.end_ref) {
            $errors.Add("$id is high but start_ref/end_ref is missing")
        } else {
            Push-Location $Repository
            try {
                & git rev-parse --verify "$($iteration.start_ref)^{commit}" | Out-Null
                if ($LASTEXITCODE -ne 0) { $errors.Add("$id start_ref does not exist: $($iteration.start_ref)") }
                & git rev-parse --verify "$($iteration.end_ref)^{commit}" | Out-Null
                if ($LASTEXITCODE -ne 0) { $errors.Add("$id end_ref does not exist: $($iteration.end_ref)") }
                if ($LASTEXITCODE -eq 0) {
                    & git merge-base --is-ancestor $iteration.start_ref $iteration.end_ref
                    if ($LASTEXITCODE -ne 0) { $errors.Add("$id start_ref is not an ancestor of end_ref") }
                }
            } finally {
                Pop-Location
            }
        }
    }
}

$average = if ($totalUcs -gt 0) { $totalDays / $totalUcs } else { $null }

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Output "ERROR: $_" }
    exit 1
}

Write-Output "OK: iterations=$($seen.Count) average_days=$([math]::Round($average, 2)) total_days=$totalDays total_ucs=$totalUcs"
