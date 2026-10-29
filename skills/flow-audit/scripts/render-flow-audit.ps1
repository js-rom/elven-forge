param(
    [Parameter(Mandatory = $true)][string]$LedgerPath,
    [string]$OutputPath
)

$ErrorActionPreference = "Stop"

function Format-Text {
    param($Value, [string]$Fallback = "-")
    if ($null -eq $Value) { return $Fallback }
    $text = [string]$Value
    if ([string]::IsNullOrWhiteSpace($text)) { return $Fallback }
    return $text
}

function Format-Confidence {
    param([string]$Value)
    switch ($Value) {
        "high" { return "Alta" }
        "medium" { return "Media" }
        "low" { return "Baja" }
        default { return Format-Text $Value }
    }
}

$ledger = Get-Content -LiteralPath $LedgerPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sources = @($ledger.sources)
$iterations = @($ledger.iterations)
$steps = @($ledger.steps)
$manualFindings = @($ledger.manual_findings)
$tooling = @($ledger.tooling)
$unclassified = @($ledger.unclassified)

$dateSet = New-Object System.Collections.Generic.HashSet[string]
foreach ($iteration in $iterations) {
    foreach ($date in @($iteration.dev_commit_days)) { [void]$dateSet.Add($date) }
}
$dates = @($dateSet | Sort-Object)
$topSteps = @($steps | Sort-Object @{Expression={$_.commit_day_count};Descending=$true}, @{Expression={$_.commit_count};Descending=$true} | Select-Object -First 8)

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine("# Auditoria de Flujo de Elaboracion")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("<!-- BEGIN GENERATED:flow-audit -->")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Metodologia")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("- **Fuente:** ``Flow Audit Ledger.json`` y commits de git.")
[void]$sb.AppendLine("- **Unidad:** dias con al menos un commit asignado a un paso.")
[void]$sb.AppendLine("- **Clasificacion:** mensaje del commit, rutas cambiadas y evidencia de ``state.yaml``.")
[void]$sb.AppendLine("- **Exclusiones:** frontend generado, ``out/``, ``todo/``, schemas y submodulo ``.agents`` se registran como tooling.")
[void]$sb.AppendLine("- **Limite retrospectivo:** no hay timestamps de aprobacion; no se calculan esperas ni latencia de revision.")
[void]$sb.AppendLine("- **Corte:** $(Format-Text $ledger.generated_at).")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Cobertura")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Iteracion | Estado | Dias con commits | Pasos detectados | Dias con solape |")
[void]$sb.AppendLine("| :--- | :--- | ---: | ---: | ---: |")
foreach ($iteration in $iterations) {
    $status = if ($iteration.partial -eq $true) { "Parcial" } elseif ($iteration.status -eq "closed") { "Cerrada" } else { Format-Text $iteration.status }
    [void]$sb.AppendLine("| $(Format-Text $iteration.iteration) | $status | $(Format-Text $iteration.dev_commit_day_count) | $(Format-Text $iteration.step_count) | $(Format-Text $iteration.overlap_days.Count) |")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Resumen por iteracion")
[void]$sb.AppendLine("")
foreach ($iteration in $iterations) {
    $iterationSteps = @($steps | Where-Object { $_.iteration -eq $iteration.iteration } | Sort-Object @{Expression={$_.commit_day_count};Descending=$true}, @{Expression={$_.commit_count};Descending=$true})
    $top = @($iterationSteps | Select-Object -First 3)
    [void]$sb.AppendLine("### $(Format-Text $iteration.iteration)")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("- Dias con commits: **$(Format-Text $iteration.dev_commit_day_count)**.")
    [void]$sb.AppendLine("- Pasos detectados: **$(Format-Text $iteration.step_count)**.")
    [void]$sb.AppendLine("- Dias con solape entre pasos: **$(Format-Text $iteration.overlap_days.Count)**.")
    [void]$sb.AppendLine("- Pasos con mas actividad: " + (($top | ForEach-Object { "$($_.step) $($_.step_name) ($($_.commit_day_count)d/$($_.commit_count)c)" }) -join "; "))
    [void]$sb.AppendLine("")
}
[void]$sb.AppendLine("## Top pasos por actividad")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Iteracion | Paso | Nombre | Dias con commits | Commits | Span | Confianza |")
[void]$sb.AppendLine("| :--- | :--- | :--- | ---: | ---: | ---: | :--- |")
foreach ($step in $topSteps) {
    [void]$sb.AppendLine("| $(Format-Text $step.iteration) | $(Format-Text $step.step) | $(Format-Text $step.step_name) | $(Format-Text $step.commit_day_count) | $(Format-Text $step.commit_count) | $(Format-Text $step.span_days) | $(Format-Confidence $step.confidence) |")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Mapa de calor por fecha")
[void]$sb.AppendLine("")
$header = "| Iteracion | Paso | " + (($dates | ForEach-Object { $_.Substring(5) }) -join " | ") + " |"
[void]$sb.AppendLine($header)
[void]$sb.AppendLine("| :--- | :--- | " + (($dates | ForEach-Object { "---" }) -join " | ") + " |")
foreach ($step in ($steps | Sort-Object iteration, step)) {
    $cells = @()
    foreach ($date in $dates) {
        if (@($step.commit_days) -contains $date) { $cells += "X" } else { $cells += "" }
    }
    [void]$sb.AppendLine("| $(Format-Text $step.iteration) | $(Format-Text $step.step) | " + ($cells -join " | ") + " |")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Hallazgos manuales")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Iteracion | Paso | Hallazgo | Impacto |")
[void]$sb.AppendLine("| :--- | :--- | :--- | :--- |")
foreach ($finding in $manualFindings) {
    [void]$sb.AppendLine("| $(Format-Text $finding.iteration) | $(Format-Text $finding.step) | $(Format-Text $finding.finding) | $(Format-Text $finding.impact) |")
}
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Tooling y no clasificado")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("- Commits de tooling: **$(Format-Text $tooling.Count)**.")
[void]$sb.AppendLine("- Commits no clasificados: **$(Format-Text $unclassified.Count)**.")
[void]$sb.AppendLine("- Los commits de tooling no se usan para diagnosticar cuellos de botella de desarrollo.")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Hipotesis de mejora")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("1. **Reducir retrabajo tardio:** si 14B-14D y los reajustes de UI/diseno concentran actividad, adelantar validaciones automaticas de conformidad y enlaces.")
[void]$sb.AppendLine("2. **Congelar alcance tras PASO 15:** si 15-16 acumulan cambios, introducir control de cambios para UCs y ranking.")
[void]$sb.AppendLine("3. **Reducir trabajo en paralelo:** si hay muchos dias con solape, limitar WIP y cerrar un paso antes de abrir el siguiente.")
[void]$sb.AppendLine("4. **Automatizar trabajo repetitivo:** state, schemas, espejos y exportacion de diagramas no deberian consumir dias de desarrollo.")
[void]$sb.AppendLine("5. **Instrumentar tiempos por paso:** anadir timestamps de inicio/aprobacion para medir espera y flow efficiency.")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Experimentos recomendados")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("| Experimento | Metrica | Esfuerzo |")
[void]$sb.AppendLine("| :--- | :--- | :--- |")
[void]$sb.AppendLine("| Preflight automatico antes de 14B/14D | Dias de 14D y defectos de conformidad | Medio |")
[void]$sb.AppendLine("| Congelacion de alcance tras PASO 15 | Dias de 16 y reaperturas | Bajo |")
[void]$sb.AppendLine("| Limite WIP: un paso activo | Dias con solape | Medio |")
[void]$sb.AppendLine("| Automatizar diagramas/estado/schemas | Dias de tooling | Bajo |")
[void]$sb.AppendLine("| Registrar timestamps por paso | Lead time y espera | Bajo |")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("## Siguiente medicion")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("Repetir la auditoria tras la siguiente iteracion cerrada y comparar mediana de dias por paso, dias con solape y reaperturas.")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("<!-- END GENERATED:flow-audit -->")
[void]$sb.AppendLine("")
[void]$sb.AppendLine("_Actualizado: $(Format-Text $ledger.generated_at)._")

$markdown = $sb.ToString().Replace("`r`n", "`n")
if ($OutputPath) {
    $parent = Split-Path -Parent $OutputPath
    if ($parent -and -not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    [IO.File]::WriteAllText($OutputPath, $markdown, (New-Object Text.UTF8Encoding($false)))
} else {
    $markdown
}
