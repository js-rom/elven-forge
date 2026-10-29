param(
    [string]$Repository = ".",
    [string]$StatePath
)

$ErrorActionPreference = "Stop"

function Get-StateField {
    param([string[]]$Lines, [string]$Name)
    $line = @($Lines | Where-Object { $_ -match "^$Name\s*:" } | Select-Object -First 1)
    if ($line.Count -eq 0) { return "" }
    return (($line[0] -replace "^$Name\s*:\s*", "") -replace "\s+#.*$", "").Trim().Trim('"')
}

function Get-StepDescription {
    param([string]$Phase, [string]$Step)
    $inception = @{
        "1" = "Vision draft"; "2" = "Goals, stakeholders, and scope"; "3" = "Actor-goal table";
        "4" = "Use case context and list"; "5" = "Brief use cases"; "6" = "Fully dressed 10%";
        "7" = "Deep investigation"; "8" = "Architectural Analysis"; "9" = "Final Vision";
        "10" = "Persist artifacts"; "11" = "Development environment"; "12" = "Close inception persistence"
    }
    $elaboration = @{
        "1" = "Iteration Plan"; "2" = "Domain Model"; "3" = "System Sequence Diagrams";
        "4" = "Operation Contracts"; "5" = "UI Design"; "6" = "Reports Design (TBD)";
        "7" = "Architectural Analysis"; "8" = "Logical View packages"; "9A" = "Domain-to-Design Transition";
        "9B" = "Scenario Design"; "10" = "Use Case Realization"; "11" = "Reviewer pass";
        "12" = "Data Model and JPA Mapping"; "13" = "SW Architecture Document";
        "14A" = "Acceptance Tests (ATDD)"; "14B" = "TDD"; "14C" = "Acceptance execution";
        "14D" = "Conformance"; "15" = "Requirements Ranking"; "16" = "Use case fully dressed";
        "17" = "Cycle close"; "18" = "Elaboration history and flow audit"; "19" = "Phase close"
    }
    if ($Phase -eq "inception" -and $inception.ContainsKey($Step)) { return $inception[$Step] }
    if ($Phase -eq "elaboration" -and $elaboration.ContainsKey($Step)) { return $elaboration[$Step] }
    return "Step $Step"
}

function Get-PhaseTag {
    param([string]$Phase)
    switch ($Phase.ToLowerInvariant()) {
        "inception" { return "Inception" }
        "elaboration" { return "Elaboration" }
        "construction" { return "Construction" }
        "transition" { return "Transition" }
        default { return $Phase }
    }
}

Push-Location $Repository
try {
    if (-not $StatePath) {
        $states = @(Get-ChildItem -Path "openspec/artifacts" -Recurse -Filter "state.yaml" -ErrorAction SilentlyContinue)
        $active = @($states | Where-Object { (Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8) -match "(?m)^status:\s*in_progress" })
        if ($active.Count -eq 1) { $StatePath = $active[0].FullName }
        elseif ($active.Count -gt 1) { Write-Output "ERROR=multiple_active_states"; $active | ForEach-Object { Write-Output "STATE=$($_.FullName)" }; exit 1 }
        elseif ($states.Count -eq 1) { $StatePath = $states[0].FullName }
        else { Write-Output "ERROR=state_not_found"; exit 1 }
    }

    $lines = @(Get-Content -LiteralPath $StatePath -Encoding UTF8)
    $phase = Get-StateField -Lines $lines -Name "phase"
    $iteration = Get-StateField -Lines $lines -Name "iteration"
    $step = Get-StateField -Lines $lines -Name "current_step"
    if ([string]::IsNullOrWhiteSpace($step) -or $step -eq "0") { $step = Get-StateField -Lines $lines -Name "last_approved_step" }
    if ([string]::IsNullOrWhiteSpace($phase) -or [string]::IsNullOrWhiteSpace($iteration) -or [string]::IsNullOrWhiteSpace($step)) {
        Write-Output "ERROR=incomplete_state"
        exit 1
    }

    $phaseTag = Get-PhaseTag -Phase $phase
    $stepTag = "Step $step"
    $stepDescription = Get-StepDescription -Phase $phase -Step $step
    $subjectPrefix = "[$phaseTag][$iteration][$stepTag]"
    $bodyTemplate = "UP phase: $phaseTag\nIteration: $iteration\nFlow step: $stepTag - $stepDescription\nChanges:"

    $mainStatus = @(& git status --porcelain)
    $mainStaged = @(& git diff --cached --name-status)
    $agentsStatus = @(& git -C .agents status --porcelain)
    $agentsStaged = @(& git -C .agents diff --cached --name-status)
    $mainCheck = @(& git diff --cached --check)
    $agentsCheck = @(& git -C .agents diff --cached --check)
    $conflicts = @(& git diff --cached --name-only --diff-filter=U)
    $conflicts += @(& git -C .agents diff --cached --name-only --diff-filter=U)

    $safety = "OK"
    if ($mainCheck.Count -gt 0 -or $agentsCheck.Count -gt 0 -or $conflicts.Count -gt 0) { $safety = "WARN" }
    foreach ($item in ($mainStaged + $agentsStaged)) {
        if ($item -match '(?i)\.env|secret|credential|\.pem$|\.key$|id_rsa') { $safety = "WARN"; break }
    }

    Write-Output "STATE_PATH=$StatePath"
    Write-Output "PHASE=$phaseTag"
    Write-Output "ITERATION=$iteration"
    Write-Output "STEP=$stepTag"
    Write-Output "STEP_DESC=$stepDescription"
    Write-Output "SUBJECT_PREFIX=$subjectPrefix"
    Write-Output "BODY_TEMPLATE=$bodyTemplate"
    Write-Output "SAFETY=$safety"
    Write-Output "MAIN_STATUS_COUNT=$($mainStatus.Count)"
    Write-Output "AGENTS_DIRTY=$($agentsStatus.Count -gt 0)"
    Write-Output "STAGED_COUNT=$($mainStaged.Count)"
    Write-Output "AGENTS_STAGED_COUNT=$($agentsStaged.Count)"

    Write-Output "STAGED:"
    if ($mainStaged.Count -eq 0) { Write-Output "NONE" } else { $mainStaged | ForEach-Object { Write-Output $_ } }
    Write-Output "AGENTS_STAGED:"
    if ($agentsStaged.Count -eq 0) { Write-Output "NONE" } else { $agentsStaged | ForEach-Object { Write-Output $_ } }

    $nl = '`n'
    $commandBody = "UP phase: $phaseTag${nl}Iteration: $iteration${nl}Flow step: $stepTag - $stepDescription${nl}Changes:${nl}- <change 1>"
    if ($mainStaged.Count -gt 0 -or $agentsStaged.Count -gt 0) {
        Write-Output "COMMAND_TEMPLATE=git commit -m `"$subjectPrefix <summary>`" -m `"$commandBody`""
    } else {
        Write-Output "COMMAND_TEMPLATE=NONE"
    }
    if ($agentsStaged.Count -gt 0) {
        Write-Output "AGENTS_COMMAND_TEMPLATE=git -C .agents commit -m `"$subjectPrefix <summary>`" -m `"$commandBody`""
        Write-Output "AFTER_AGENTS=git add .agents"
    } else {
        Write-Output "AGENTS_COMMAND_TEMPLATE=NONE"
    }
} finally {
    Pop-Location
}
