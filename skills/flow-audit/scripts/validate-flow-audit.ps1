param(
    [Parameter(Mandatory = $true)][string]$LedgerPath
)

$ErrorActionPreference = "Stop"
$errors = New-Object System.Collections.Generic.List[string]

$ledger = Get-Content -LiteralPath $LedgerPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sourceIds = @{}
foreach ($source in @($ledger.sources)) {
    if ($sourceIds.ContainsKey($source.iteration)) { $errors.Add("Duplicate source: $($source.iteration)") }
    $sourceIds[$source.iteration] = $true
    if (-not $source.start_ref -or -not $source.end_ref) { $errors.Add("Source $($source.iteration) missing refs") }
}

$keys = @{}
foreach ($step in @($ledger.steps)) {
    $key = "$($step.iteration)|$($step.step)"
    if ($keys.ContainsKey($key)) { $errors.Add("Duplicate step: $key") }
    $keys[$key] = $true
    if (-not $sourceIds.ContainsKey($step.iteration)) { $errors.Add("Step $key has no source") }
    $days = @($step.commit_days)
    if ([int]$step.commit_day_count -ne $days.Count) { $errors.Add("Step $key commit_day_count mismatch") }
    if ((@($days | Sort-Object -Unique)).Count -ne $days.Count) { $errors.Add("Step $key has duplicate commit days") }
    if ([int]$step.commit_count -lt 1) { $errors.Add("Step $key has no commits") }
    if ([int]$step.span_days -lt 1) { $errors.Add("Step $key has invalid span_days") }
}

foreach ($iteration in @($ledger.iterations)) {
    if (-not $sourceIds.ContainsKey($iteration.iteration)) { $errors.Add("Iteration summary without source: $($iteration.iteration)") }
    if ([int]$iteration.dev_commit_day_count -ne @($iteration.dev_commit_days).Count) { $errors.Add("Iteration $($iteration.iteration) dev_commit_day_count mismatch") }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Output "ERROR: $_" }
    exit 1
}

Write-Output "OK: sources=$($sourceIds.Count) steps=$($keys.Count) unclassified=$(@($ledger.unclassified).Count) tooling=$(@($ledger.tooling).Count)"
