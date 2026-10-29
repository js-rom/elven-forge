param(
    [Parameter(Mandatory = $true)][string]$LedgerPath,
    [string]$OutputPath,
    [string]$Title = "Historico de Iteraciones de Elaboracion"
)

$ErrorActionPreference = "Stop"

function Format-Text {
    param($Value, [string]$Fallback = "-")
    if ($null -eq $Value) { return $Fallback }
    $text = [string]$Value
    if ([string]::IsNullOrWhiteSpace($text)) { return $Fallback }
    return $text
}

function Format-Date {
    param($Value, [string]$Fallback = "-")
    return Format-Text -Value $Value -Fallback $Fallback
}

function Format-Number {
    param($Value, [string]$Fallback = "-")
    if ($null -eq $Value) { return $Fallback }
    return ([double]$Value).ToString("0.#", [Globalization.CultureInfo]::GetCultureInfo("es-ES"))
}

function Format-Confidence {
    param([string]$Value)
    switch ($Value) {
        "high" { return "Alta" }
        "medium" { return "Media" }
        "low" { return "Baja" }
        "open" { return "Abierta" }
        default { return Format-Text -Value $Value }
    }
}

function Get-CalendarDays {
    param($Iteration)
    if ($null -eq $Iteration.actual_start) { return "N/D" }
    if ($null -eq $Iteration.actual_end) {
        if ($Iteration.status -eq "in_progress") { return "En curso" }
        return "N/D"
    }
    $start = [DateTime]::ParseExact([string]$Iteration.actual_start, "yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture)
    $end = [DateTime]::ParseExact([string]$Iteration.actual_end, "yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture)
    return [string](($end - $start).Days + 1)
}

function Get-EndLabel {
    param($Iteration)
    if ($null -eq $Iteration.actual_start) { return "-" }
    if ($null -eq $Iteration.actual_end) {
        if ($Iteration.status -eq "in_progress") { return "En curso" }
        return "N/D"
    }
    return [string]$Iteration.actual_end
}

function Format-Status {
    param([string]$Value)
    switch ($Value) {
        "closed" { return "Cerrada" }
        "in_progress" { return "En curso" }
        default { return Format-Text -Value $Value }
    }
}

function Get-EndDeviation {
    param($Iteration)
    if ($null -eq $Iteration.planned_end -or $null -eq $Iteration.actual_end) {
        if ($Iteration.status -eq "in_progress") { return "Pendiente" }
        return "N/D"
    }
    $planned = [DateTime]::ParseExact([string]$Iteration.planned_end, "yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture)
    $actual = [DateTime]::ParseExact([string]$Iteration.actual_end, "yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture)
    $days = ($actual - $planned).Days
    if ($days -gt 0) { return "+$days dias" }
    if ($days -lt 0) { return "$days dias" }
    return "0 dias"
}

function Get-UcLabel {
    param($Iteration)
    $items = @($Iteration.scope)
    if ($items.Count -eq 0) { return "-" }
    $labels = foreach ($item in $items) {
        $uc = Format-Text -Value $item.uc -Fallback ""
        $name = Format-Text -Value $item.name -Fallback ""
        $type = Format-Text -Value $item.delivery_type -Fallback ""
        if ($name -and $uc) { "$uc $name ($type)" }
        elseif ($uc) { "$uc ($type)" }
        elseif ($name) { "$name ($type)" }
    }
    return ($labels -join "; ")
}

function Get-AveragedUcCount {
    param($Iteration)
    $count = 0
    foreach ($item in @($Iteration.scope)) {
        if ($item.counts_for_average -eq $true -and ($item.delivery_type -eq "full" -or $item.delivery_type -eq "slice")) {
            $count++
        }
    }
    return $count
}

$ledger = Get-Content -LiteralPath $LedgerPath -Raw -Encoding UTF8 | ConvertFrom-Json
$iterations = @($ledger.iterations)
$eligible = @($iterations | Where-Object { $_.include_in_average -eq $true -and $_.reliability -eq "high" })
$totalDays = 0
$totalUcs = 0
foreach ($iteration in $eligible) {
    $totalDays += [int]$iteration.effective_days
    $totalUcs += Get-AveragedUcCount -Iteration $iteration
}
$average = if ($totalUcs -gt 0) { $totalDays / $totalUcs } else { $null }

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine("# $Title")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("<!-- BEGIN GENERATED:iteration-history -->")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Metodologia")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("- **Fuente de verdad:** ``Elaboration Iterations Ledger.json``.")
[void]$sb.AppendLine("- **Dias transcurridos:** dias naturales inclusivos entre inicio y fin reales.")
[void]$sb.AppendLine("- **Dias efectivos:** fechas unicas con al menos un commit dentro de ``start_ref..end_ref``, usando fecha de autor.")
[void]$sb.AppendLine("- **Rango de commits:** solo commits alcanzables desde ``end_ref``; no se usa ``git log --all``.")
[void]$sb.AppendLine("- **Media por UC:** solo iteraciones de confianza alta y UCs ``full`` o ``slice``; se excluyen refactors y soporte.")
[void]$sb.AppendLine("- **Zona horaria:** $(Format-Text -Value $ledger.project_timezone).")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Iteraciones")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Iteracion | Inicio | Fin | Dias | Dias efectivos | Casos de uso | Estado | Confianza | Computa media? |")
[void]$sb.AppendLine("| :--- | :--- | :--- | ---: | ---: | :--- | :--- | :--- | :--- |")
foreach ($iteration in $iterations) {
    $include = if ($iteration.include_in_average -eq $true) { "Si" } else { "No" }
    [void]$sb.AppendLine("| $(Format-Text $iteration.iteration) | $(Format-Date $iteration.actual_start) | $(Get-EndLabel $iteration) | $(Get-CalendarDays $iteration) | $(Format-Text $iteration.effective_days) | $(Get-UcLabel $iteration) | $(Format-Status $iteration.status) | $(Format-Confidence $iteration.reliability) | $include |")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Planificado frente a real")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Iteracion | Fin planificado | Fin real | Desviacion |")
[void]$sb.AppendLine("| :--- | :--- | :--- | :--- |")
foreach ($iteration in $iterations) {
    [void]$sb.AppendLine("| $(Format-Text $iteration.iteration) | $(Format-Date $iteration.planned_end) | $(Get-EndLabel $iteration) | $(Get-EndDeviation $iteration) |")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Evidencia git")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Iteracion | start_ref | end_ref | Commits | Dias efectivos | Fechas con commit |")
[void]$sb.AppendLine("| :--- | :--- | :--- | ---: | ---: | :--- |")
foreach ($iteration in $iterations) {
    $days = @($iteration.commit_days)
    $dayText = if ($days.Count -eq 0) { "-" } else { $days -join ", " }
    [void]$sb.AppendLine("| $(Format-Text $iteration.iteration) | $(Format-Text $iteration.start_ref) | $(Format-Text $iteration.end_ref) | $(Format-Text $iteration.commit_count) | $(Format-Text $iteration.effective_days) | $dayText |")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Media de dias efectivos por caso de uso")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("Solo se incluyen iteraciones cerradas, con alcance de casos de uso identificable, referencias git validas y arbol limpio al cierre.")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Iteracion | Dias efectivos | UCs computados | Dias efectivos / UC |")
[void]$sb.AppendLine("| :--- | ---: | :--- | ---: |")
foreach ($iteration in $eligible) {
    $ucCount = Get-AveragedUcCount -Iteration $iteration
    $ratio = if ($ucCount -gt 0) { [double]$iteration.effective_days / $ucCount } else { $null }
    [void]$sb.AppendLine("| $(Format-Text $iteration.iteration) | $(Format-Text $iteration.effective_days) | $(Get-UcLabel $iteration) | $(Format-Number $ratio) |")
}
[void]$sb.AppendLine("| **Total** | **$(Format-Text $totalDays)** | **$(Format-Text $totalUcs)** | **$(Format-Number $average)** |")
[void]$sb.AppendLine("")
if ($null -ne $average) {
    [void]$sb.AppendLine("**Media: $(Format-Number $average) dias efectivos por caso de uso** (``$totalDays / $totalUcs``).")
} else {
    [void]$sb.AppendLine("**Media: no calculable** (no hay iteraciones fiables computables).")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Datos excluidos de la media")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Iteracion | Confianza | Motivo |")
[void]$sb.AppendLine("| :--- | :--- | :--- |")
foreach ($iteration in $iterations) {
    if ($iteration.include_in_average -ne $true) {
        [void]$sb.AppendLine("| $(Format-Text $iteration.iteration) | $(Format-Confidence $iteration.reliability) | $(Format-Text $iteration.excluded_reason) |")
    }
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Notas")
[void]$sb.AppendLine("")
foreach ($note in @($ledger.document_notes)) {
    [void]$sb.AppendLine("- $note")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("<!-- END GENERATED:iteration-history -->")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("_Actualizado: $(Format-Text $ledger.last_updated)._")

$markdown = $sb.ToString().Replace("`r`n", "`n")
if ($OutputPath) {
    $parent = Split-Path -Parent $OutputPath
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    [IO.File]::WriteAllText($OutputPath, $markdown, (New-Object Text.UTF8Encoding($false)))
} else {
    $markdown
}
