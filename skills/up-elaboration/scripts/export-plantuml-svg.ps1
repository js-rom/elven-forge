param(
    [string]$ArtifactsRoot = "openspec\artifacts",
    [string]$OutRoot = "out"
)

$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Exports every .plantuml diagram under the artifacts tree to the SVG layout
# used by the Use Case Realization documents:
#   <workspace>/out/{source dir relative to workspace}/{baseName}/{diagramName}.svg
# where {baseName} is the .plantuml file name without extension and
# {diagramName} is the identifier declared after @startuml (fallback: baseName).
#
# Deterministic alternative to the VS Code command
# "PlantUML: Export Workspace Diagrams" (vscode://command/plantuml.exportWorkspace),
# which silently targets the most recently focused VS Code window and can export
# the wrong workspace. Uses the plantuml.jar bundled by the jebbs.plantuml
# extension (or a local plantuml.jar next to this script).
#
# NOTE: the PlantUML CLI names its output files after the diagram name with the
# last dot-segment removed (com.a.b.classDiagram -> com.a.b.svg). This script
# renames every produced SVG back to the full {diagramName}.svg convention used
# by the VS Code extension.
# ---------------------------------------------------------------------------

$workspaceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path

function Get-RelativePath([string]$base, [string]$path) {
    $base = $base.TrimEnd('\') + '\'
    if ($path.StartsWith($base, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $path.Substring($base.Length)
    }
    return $path
}

# 1. Locate plantuml.jar (jebbs.plantuml extension bundle, newest version first).
$jar = $null
$extRoot = Join-Path $env:USERPROFILE ".vscode\extensions"
if (Test-Path $extRoot) {
    $jar = Get-ChildItem $extRoot -Filter "plantuml.jar" -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Directory.Name -like "jebbs.plantuml-*" } |
        Sort-Object { [version]($_.Directory.Name -replace "jebbs.plantuml-", "") } -Descending |
        Select-Object -First 1 -ExpandProperty FullName
}
if (-not $jar) {
    $localJar = Join-Path $PSScriptRoot "plantuml.jar"
    if (Test-Path $localJar) { $jar = $localJar }
}
if (-not $jar -or -not (Test-Path $jar)) {
    throw "plantuml.jar not found. Install the jebbs.plantuml VS Code extension or place a plantuml.jar next to this script."
}

$java = (Get-Command java -ErrorAction Stop).Source
$artifactsRootFull = (Resolve-Path $ArtifactsRoot).Path
$outRootFull = (Resolve-Path $OutRoot).Path

$files = @(Get-ChildItem $artifactsRootFull -Filter "*.plantuml" -Recurse)
if ($files.Count -eq 0) { throw "No .plantuml files found under $artifactsRootFull" }

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("plantuml-export-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tmp | Out-Null

$script:exported = 0
$script:failed = 0
$script:batchSeq = 0

function Get-DiagramName([string]$src) {
    $head = Get-Content $src -TotalCount 5
    foreach ($line in $head) {
        if ($line -match '^@startuml\s+(\S+)') { return $Matches[1] }
    }
    return $null
}

# CLI output name = diagram name (or file base name) minus the last dot-segment.
function Get-CliName([string]$diagramName, [string]$baseName) {
    $name = if ($diagramName) { $diagramName } else { $baseName }
    $idx = $name.LastIndexOf('.')
    if ($idx -ge 0) { $name = $name.Substring(0, $idx) }
    return $name
}

function Place-Svg([string]$src, [string]$produced) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($src)
    $diagramName = Get-DiagramName $src
    if (-not $diagramName) { $diagramName = $baseName }

    $rel = Get-RelativePath $workspaceRoot $src
    $relDir = Split-Path $rel -Parent
    $destDir = Join-Path (Join-Path $outRootFull $relDir) $baseName
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    Copy-Item $produced (Join-Path $destDir "$diagramName.svg") -Force
    $script:exported++
}

function Export-Single([string]$src) {
    $singleTmp = Join-Path $tmp ("s" + ($script:batchSeq++))
    New-Item -ItemType Directory -Path $singleTmp | Out-Null
    & $java -jar $jar -tsvg -charset UTF-8 -o $singleTmp $src
    if ($LASTEXITCODE -ne 0) {
        $script:failed++
        Write-Warning "PlantUML exited with $LASTEXITCODE for $src"
        return
    }
    $svgs = @(Get-ChildItem $singleTmp -Filter "*.svg")
    if ($svgs.Count -ne 1) {
        $script:failed++
        Write-Warning "Expected 1 SVG for $src, got $($svgs.Count)"
        return
    }
    Place-Svg $src $svgs[0].FullName
}

function Export-Batch([string[]]$batch) {
    $batchTmp = Join-Path $tmp ("b" + ($script:batchSeq++))
    New-Item -ItemType Directory -Path $batchTmp | Out-Null
    & $java -jar $jar -tsvg -charset UTF-8 -o $batchTmp @batch
    if ($LASTEXITCODE -ne 0) {
        $script:failed += $batch.Count
        Write-Warning "PlantUML exited with $LASTEXITCODE for a batch of $($batch.Count) files"
        return
    }
    foreach ($src in $batch) {
        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($src)
        $diagramName = Get-DiagramName $src
        $cliName = Get-CliName $diagramName $baseName
        $produced = Join-Path $batchTmp "$cliName.svg"
        if (Test-Path $produced) {
            Place-Svg $src $produced
        } else {
            # Naming edge cases (odd diagram names, collisions): export alone.
            Export-Single $src
        }
    }
}

# 2. Batch files: one java invocation per batch, avoiding duplicate CLI output
#    names inside the same batch (the CLI flattens outputs into one dir) and
#    keeping the command line below the Windows argument length limit.
$batch = @()
$batchNames = @{}
$batchLen = 0
foreach ($f in $files) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
    $cliName = Get-CliName (Get-DiagramName $f.FullName) $baseName
    $full = $f.FullName
    if (($batchLen + $full.Length + 1 -gt 24000) -or $batchNames.ContainsKey($cliName)) {
        Export-Batch $batch
        $batch = @(); $batchNames = @{}; $batchLen = 0
    }
    $batch += $full
    $batchNames[$cliName] = $true
    $batchLen += $full.Length + 1
}
if ($batch.Count -gt 0) {
    Export-Batch $batch
}

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Write-Output "PLANTUML_EXPORT exported=$($script:exported) failed=$($script:failed)"
if ($script:failed -gt 0) { exit 1 }
