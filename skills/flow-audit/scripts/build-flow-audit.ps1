param(
    [Parameter(Mandatory = $true)][string]$LedgerPath,
    [string]$Repository = "."
)

$ErrorActionPreference = "Stop"

function Resolve-TimeZone {
    param([string]$Name)
    try { return [TimeZoneInfo]::FindSystemTimeZoneById($Name) }
    catch {
        if ($Name -eq "Europe/Madrid") { return [TimeZoneInfo]::FindSystemTimeZoneById("Romance Standard Time") }
        throw
    }
}

function Get-StepFromMessage {
    param([string]$Message)
    if ($Message -match '(?i)(?:PASO|STEP)\s*(9[AB]|1[0-9][A-D]?|[1-9])') { return $Matches[1].ToUpperInvariant() }
    if ($Message -match '(?i)\b(14[ABCD])\b') { return $Matches[1].ToUpperInvariant() }
    if ($Message -match '(?i)\b(9[AB])\b') { return $Matches[1].ToUpperInvariant() }
    if ($Message -match '(?i)conformance|\b14D\b') { return "14D" }
    if ($Message -match '(?i)acceptance plan|\b14A\b') { return "14A" }
    if ($Message -match '(?i)\btdd\b|\b14B\b') { return "14B" }
    if ($Message -match '(?i)acceptance test|\b14C\b') { return "14C" }
    if ($Message -match '(?i)iteration plan') { return "1" }
    if ($Message -match '(?i)domain model') { return "2" }
    if ($Message -match '(?i)\bssd\b') { return "3" }
    if ($Message -match '(?i)operation contract|\boc\b') { return "4" }
    if ($Message -match '(?i)\buid\b|ui design|visual spec|interaction spec|vaadin') { return "5" }
    if ($Message -match '(?i)reviewer pass') { return "11" }
    if ($Message -match '(?i)data model|jpa mapping') { return "12" }
    if ($Message -match '(?i)\bswa\b|sw architecture') { return "13" }
    if ($Message -match '(?i)requirements ranking') { return "15" }
    if ($Message -match '(?i)fully dressed') { return "16" }
    if ($Message -match '(?i)\bucr\b|use case realization') { return "10" }
    return $null
}

function Get-StepConfidence {
    param([bool]$ByMessage, [int]$RuleMatches)
    if ($ByMessage) { return "high" }
    if ($RuleMatches -eq 1) { return "medium" }
    return "low"
}

$ledger = Get-Content -LiteralPath $LedgerPath -Raw -Encoding UTF8 | ConvertFrom-Json
$timezone = Resolve-TimeZone -Name $ledger.project_timezone
$stepNames = @{
    "1" = "Iteration Plan"; "2" = "Domain Model"; "3" = "SSDs"; "4" = "Operation Contracts";
    "5" = "UI Design"; "7" = "Architectural Analysis"; "8" = "Logical View packages";
    "9A" = "Domain-to-Design"; "9B" = "Scenario design"; "10" = "Use Case Realization";
    "11" = "Reviewer pass"; "12" = "Data Model"; "13" = "SW Architecture";
    "14A" = "Acceptance plan"; "14B" = "TDD"; "14C" = "Acceptance execution";
    "14D" = "Conformance"; "15" = "Requirements Ranking"; "16" = "Fully dressed UC";
    "17" = "Cycle close"; "18" = "Elaboration history"
}
$rules = @(
    [pscustomobject]@{ Step = "1"; Pattern = '08 Project Management/[^/]*Plan\.md$'; Priority = 90 },
    [pscustomobject]@{ Step = "2"; Pattern = '01 Business Modeling/Domain Model\.md$'; Priority = 80 },
    [pscustomobject]@{ Step = "3"; Pattern = '02 Requirements/SSDs/'; Priority = 80 },
    [pscustomobject]@{ Step = "4"; Pattern = '02 Requirements/Operation Contracts/'; Priority = 80 },
    [pscustomobject]@{ Step = "5"; Pattern = '03 Design/UI/'; Priority = 70 },
    [pscustomobject]@{ Step = "7"; Pattern = '02 Requirements/(Architectural Analysis\.md|Technical memos/|supplementary-specification\.md)'; Priority = 70 },
    [pscustomobject]@{ Step = "8"; Pattern = '03 Design/Logical View/.*\.packageDiagram\.plantuml$'; Priority = 60 },
    [pscustomobject]@{ Step = "9A"; Pattern = 'domain-to-design-transition'; Priority = 75 },
    [pscustomobject]@{ Step = "9B"; Pattern = '03 Design/Logical View/.*(sequenceDiagram|classDiagram)\.plantuml$'; Priority = 65 },
    [pscustomobject]@{ Step = "10"; Pattern = '03 Design/Use Case Realization/'; Priority = 70 },
    [pscustomobject]@{ Step = "12"; Pattern = '03 Design/Data Model/'; Priority = 70 },
    [pscustomobject]@{ Step = "13"; Pattern = '03 Design/SW Architecture Document\.md$'; Priority = 70 },
    [pscustomobject]@{ Step = "14A"; Pattern = '05 Test/.*Acceptance plan\.md$'; Priority = 60 },
    [pscustomobject]@{ Step = "14B"; Pattern = '05 Test/.*Test plan\.md$|src/test/|src/main/'; Priority = 50 },
    [pscustomobject]@{ Step = "15"; Pattern = '08 Project Management/Requirements Ranking\.md$'; Priority = 70 },
    [pscustomobject]@{ Step = "16"; Pattern = '02 Requirements/use-cases/UC.*\.md$'; Priority = 60 },
    [pscustomobject]@{ Step = "18"; Pattern = '08 Project Management/Elaboration Iterations'; Priority = 80 }
)
$toolingPattern = '(^|/)(todo|out)/|src/main/frontend/generated/|^\.agents$|openspec/schemas/|compose\.yaml|Flow Audit|/todo/'

$stepMap = @{}
$unclassified = New-Object System.Collections.Generic.List[object]
$tooling = New-Object System.Collections.Generic.List[object]
$iterationSummaries = New-Object System.Collections.Generic.List[object]

Push-Location $Repository
try {
    foreach ($source in @($ledger.sources)) {
        $range = "$($source.start_ref)..$($source.end_ref)"
        $raw = @(& git log --format="COMMIT%x09%H%x09%aI%x09%s" --name-only $range)
        $commits = New-Object System.Collections.Generic.List[object]
        $current = $null
        foreach ($line in $raw) {
            if ($line -like "COMMIT`t*") {
                if ($null -ne $current) { $commits.Add($current) }
                $parts = $line -split "`t", 4
                $current = [ordered]@{
                    hash = $parts[1]
                    author_iso = $parts[2]
                    subject = $parts[3]
                    paths = New-Object System.Collections.Generic.List[string]
                }
            } elseif (-not [string]::IsNullOrWhiteSpace($line) -and $null -ne $current) {
                $current.paths.Add($line.Trim().Trim('"'))
            }
        }
        if ($null -ne $current) { $commits.Add($current) }

        $iterationAllDates = New-Object System.Collections.Generic.HashSet[string]
        $iterationDevDates = New-Object System.Collections.Generic.HashSet[string]
        foreach ($commit in $commits) {
            $author = [DateTimeOffset]::Parse($commit.author_iso, [Globalization.CultureInfo]::InvariantCulture)
            $local = [TimeZoneInfo]::ConvertTime($author, $timezone)
            $date = $local.ToString("yyyy-MM-dd")
            [void]$iterationAllDates.Add($date)

            $devPaths = New-Object System.Collections.Generic.List[string]
            $toolingPaths = New-Object System.Collections.Generic.List[string]
            foreach ($path in $commit.paths) {
                if ($path -match $toolingPattern) { $toolingPaths.Add($path) } else { $devPaths.Add($path) }
            }

            if ($devPaths.Count -eq 0) {
                $tooling.Add([ordered]@{
                    iteration = $source.iteration; date = $date; hash = $commit.hash; subject = $commit.subject; paths = @($toolingPaths)
                })
                continue
            }

            [void]$iterationDevDates.Add($date)
            $messageStep = Get-StepFromMessage -Message $commit.subject
            $ruleMatches = @()
            foreach ($rule in $rules) {
                foreach ($path in $devPaths) {
                    if ($path -match $rule.Pattern) {
                        if (-not ($ruleMatches | Where-Object { $_.Step -eq $rule.Step })) { $ruleMatches += $rule }
                    }
                }
            }
            $ruleMatches = @($ruleMatches | Sort-Object Priority -Descending)
            $primary = if ($messageStep) { $messageStep } else { if ($ruleMatches.Count -gt 0) { $ruleMatches[0].Step } else { $null } }
            if (-not $primary) {
                $unclassified.Add([ordered]@{
                    iteration = $source.iteration; date = $date; hash = $commit.hash; subject = $commit.subject; paths = @($devPaths)
                })
                continue
            }

            $key = "$($source.iteration)|$primary"
            if (-not $stepMap.ContainsKey($key)) {
                $stepMap[$key] = [ordered]@{
                    iteration = $source.iteration
                    step = $primary
                    step_name = if ($stepNames.ContainsKey($primary)) { $stepNames[$primary] } else { $primary }
                    commit_days = New-Object System.Collections.Generic.HashSet[string]
                    commit_count = 0
                    first_commit_date = $null
                    last_commit_date = $null
                    primary_paths = New-Object System.Collections.Generic.HashSet[string]
                    evidence = New-Object System.Collections.Generic.List[string]
                    secondary_steps = New-Object System.Collections.Generic.HashSet[string]
                    confidence = "low"
                }
            }
            $record = $stepMap[$key]
            [void]$record.commit_days.Add($date)
            $record.commit_count++
            if ($null -eq $record.first_commit_date -or $date -lt $record.first_commit_date) { $record.first_commit_date = $date }
            if ($null -eq $record.last_commit_date -or $date -gt $record.last_commit_date) { $record.last_commit_date = $date }
            foreach ($path in $devPaths) { [void]$record.primary_paths.Add($path) }
            foreach ($m in $ruleMatches) { if ($m.Step -ne $primary) { [void]$record.secondary_steps.Add($m.Step) } }
            if ($record.evidence.Count -lt 3) { $record.evidence.Add($commit.subject) }
            $confidence = Get-StepConfidence -ByMessage ([bool]$messageStep) -RuleMatches $ruleMatches.Count
            if ($confidence -eq "high" -or ($confidence -eq "medium" -and $record.confidence -eq "low")) { $record.confidence = $confidence }
        }

        $stepsForIteration = @($stepMap.Values | Where-Object { $_.iteration -eq $source.iteration })
        $datesWithMultipleSteps = @()
        foreach ($date in $iterationDevDates) {
            $count = 0
            foreach ($step in $stepsForIteration) { if ($step.commit_days.Contains($date)) { $count++ } }
            if ($count -ge 2) { $datesWithMultipleSteps += $date }
        }
        $iterationSummaries.Add([ordered]@{
            iteration = $source.iteration
            status = $source.status
            partial = $source.partial
            start_ref = $source.start_ref
            end_ref = $source.end_ref
            all_commit_days = @($iterationAllDates | Sort-Object)
            dev_commit_days = @($iterationDevDates | Sort-Object)
            all_commit_day_count = $iterationAllDates.Count
            dev_commit_day_count = $iterationDevDates.Count
            step_count = $stepsForIteration.Count
            overlap_days = @($datesWithMultipleSteps | Sort-Object)
        })
    }

    $steps = New-Object System.Collections.Generic.List[object]
    foreach ($record in $stepMap.Values) {
        $span = 0
        if ($record.first_commit_date -and $record.last_commit_date) {
            $first = [DateTime]::ParseExact($record.first_commit_date, "yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture)
            $last = [DateTime]::ParseExact($record.last_commit_date, "yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture)
            $span = ($last - $first).Days + 1
        }
        $steps.Add([ordered]@{
            iteration = $record.iteration
            step = $record.step
            step_name = $record.step_name
            commit_days = @($record.commit_days | Sort-Object)
            commit_day_count = $record.commit_days.Count
            commit_count = $record.commit_count
            first_commit_date = $record.first_commit_date
            last_commit_date = $record.last_commit_date
            span_days = $span
            primary_paths = @($record.primary_paths | Sort-Object)
            secondary_steps = @($record.secondary_steps | Sort-Object)
            confidence = $record.confidence
            evidence = @($record.evidence)
        })
    }

    $iterationArray = @()
    foreach ($item in $iterationSummaries) { $iterationArray += $item }
    $stepArray = @()
    foreach ($item in $steps) { $stepArray += $item }
    $unclassifiedArray = @()
    foreach ($item in $unclassified) { $unclassifiedArray += $item }
    $toolingArray = @()
    foreach ($item in $tooling) { $toolingArray += $item }

    $ledger | Add-Member -NotePropertyName iterations -NotePropertyValue $iterationArray -Force
    $ledger | Add-Member -NotePropertyName steps -NotePropertyValue $stepArray -Force
    $ledger | Add-Member -NotePropertyName unclassified -NotePropertyValue $unclassifiedArray -Force
    $ledger | Add-Member -NotePropertyName tooling -NotePropertyValue $toolingArray -Force
    $ledger | Add-Member -NotePropertyName generated_at -NotePropertyValue ((Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")) -Force
    $ledger | Add-Member -NotePropertyName method -NotePropertyValue "retrospective_commit_path_v1" -Force

    $json = $ledger | ConvertTo-Json -Depth 12
    [IO.File]::WriteAllText((Resolve-Path $LedgerPath), $json.Replace("`r`n", "`n") + "`n", (New-Object Text.UTF8Encoding($false)))
} finally {
    Pop-Location
}
