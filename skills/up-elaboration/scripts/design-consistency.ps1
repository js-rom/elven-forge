param(
    [string]$DesignRoot,
    [string]$SourceRoot = "",
    [string[]]$NewPackages = @(),
    [string[]]$Include = @(),
    [string[]]$TypeAllowlist = @()
)

# ---------------------------------------------------------------------------
# Deterministic design-consistency validator for UP elaboration artifacts.
#
# L1  DSD <-> DCD operation resolution: every solid call between lifelines
#     must resolve to an operation declared in the target package's class
#     diagrams; command.x field references must exist in the command record
#     declared by the scenario's input message.
# L2  DCD completeness: every type referenced by a class diagram (fields,
#     parameters, return types, associations) must be declared in some class
#     diagram of the checked set, or be a known builtin/framework type.
# L3  Code authority (only when -SourceRoot is given): classifiers and
#     packages that the diagrams declare as already existing must exist in
#     the production source tree; operations declared on them must appear in
#     the corresponding source file. Elements marked "NEW in {iteration}"
#     inline in the diagram and packages listed in -NewPackages are exempt.
#
# Exit code: 0 = no ERROR (WARN allowed), 2 = one or more ERROR.
# ---------------------------------------------------------------------------

$ErrorActionPreference = "Stop"

if (-not $DesignRoot) { throw "-DesignRoot is required" }

$designRootFull = (Resolve-Path $DesignRoot).Path
$files = @(Get-ChildItem $designRootFull -Filter "*.plantuml" -Recurse)
if ($files.Count -eq 0) { throw "no .plantuml files under $designRootFull" }

$builtinTypes = @(
    "String", "List", "Map", "Set", "Optional", "Clock", "UUID", "LocalDate",
    "LocalDateTime", "Instant", "Integer", "Long", "Double", "BigDecimal",
    "int", "boolean", "void", "Duration", "Object", "Component", "Button",
    "Select", "DatePicker", "Paragraph", "Div", "Span", "TextField",
    "NumberField", "Checkbox", "Avatar", "Icon", "Grid", "Dialog",
    "VerticalLayout", "HorizontalLayout", "RouterLink", "Anchor", "Image",
    "OrderedLayout", "ScrollPanel", "SplitLayout", "Tabs", "Tab", "FormLayout",
    "Notification", "I18NProvider", "Locale", "ThemeVariant", "Key",
    "Supplier", "TransactionTemplate", "ZonedDateTime", "ZoneId", "JdbcTemplate"
) + $TypeAllowlist

$errors = New-Object System.Collections.ArrayList
$warns = New-Object System.Collections.ArrayList

function Emit-Error([string]$check, [string]$where, [string]$msg) {
    [void]$errors.Add("[ERROR] $check $where : $msg")
}

function Emit-Warn([string]$check, [string]$where, [string]$msg) {
    [void]$warns.Add("[WARN] $check $where : $msg")
}

# ---------------------------------------------------------------------------
# Parse class diagrams into a symbol index.
# ---------------------------------------------------------------------------

$classifiers = @()   # each: name, fqcn, kind, ops, fields, external, inScope
$declaredNames = New-Object System.Collections.Generic.HashSet[string]

foreach ($file in $files) {
    if ($file.Name -notlike "*.classDiagram.plantuml") { continue }

    $lines = [System.IO.File]::ReadAllLines($file.FullName, [System.Text.Encoding]::UTF8)
    $packageFqcn = ""
    $current = $null
    $braceDepth = 0

    foreach ($line in $lines) {
        if ($line -match '^\s*package\s+(\w+)\s+as\s+"([^"]+)"') {
            $packageFqcn = $Matches[2]
            continue
        }
        if ($line -match '^\s*package\s+"([^"]+)"') {
            $packageFqcn = $Matches[1]
            continue
        }
        if ($line -match '^\s*(abstract\s+)?(class|interface|enum)\s+(?:"([^"]+)"\s+as\s+(\w+)|(\w+))\s*(<<[^>]+>>)?\s*\{?') {
            $kind = $Matches[2]
            if ($Matches[3]) { $name = $Matches[4]; $alias = $Matches[3] } else { $name = $Matches[5]; $alias = $Matches[5] }
            $external = ($packageFqcn -eq "") -and ($line -match 'as\s+"([\w.\\\n]+)"')
            $extFqcn = ""
            if ($line -match 'as\s+"([\w.\\\n]+)"') { $extFqcn = (($Matches[1] -replace '\\n\.', '.') -replace '\\n', '.').TrimEnd('.') }
            $current = @{
                name = $name; alias = $alias; kind = $kind
                fqcn = if ($external) { $extFqcn } else { $packageFqcn }
                ops = New-Object System.Collections.ArrayList
                fields = New-Object System.Collections.ArrayList
                external = $external
                file = $file.Name
                markerNew = $false
                markerNewLines = New-Object System.Collections.ArrayList
            }
            $classifiers += $current
            [void]$declaredNames.Add($name)
            [void]$declaredNames.Add($alias)
            if ($line -match '\{') { $braceDepth = 1 } else { $braceDepth = 0 }
            if ($line -match 'NEW\s+in') { $current.markerNew = $true }
            continue
        }
        if ($current) {
            if ($braceDepth -gt 0) {
                $braceDepth += ([regex]::Matches($line, '\{')).Count
                $braceDepth -= ([regex]::Matches($line, '\}')).Count
                if ($braceDepth -lt 0) { $braceDepth = 0 }
            }
            if ($line -match 'NEW\s+in') { $current.markerNew = $true }
            if ($line -match '^\s*(?:\{static\}\s*)?[+~#-]\s*([A-Za-z]\w*)\s*\(') {
                [void]$current.ops.Add($Matches[1])
                if ($line -match 'NEW\s+in') { [void]$current.markerNewLines.Add($Matches[1]) }
            }
            if ($line -match '^\s*[+-]\s+([A-Za-z]\w*)\s*:') {
                [void]$current.fields.Add($Matches[1])
            }
            if ($braceDepth -eq 0 -and $line -match '^\s*\}?\s*$' -and $line -notmatch '\S' -and $current.ops.Count -gt 0) {
                $current = $null
            }
        }
    }
}

$classifierByAlias = @{}
foreach ($c in $classifiers) { $classifierByAlias[$c.alias] = $c }

# ---------------------------------------------------------------------------
# L1: DSD messages resolve to declared operations; command.x fields exist.
# ---------------------------------------------------------------------------

foreach ($file in $files) {
    if ($file.Name -notlike "*.sequenceDiagram.plantuml") { continue }
    $inScope = $true
    if ($Include.Count -gt 0) {
        $inScope = $false
        foreach ($pattern in $Include) {
            if ($file.Name -like $pattern -or $file.FullName -like "*$pattern*") { $inScope = $true; break }
        }
    }
    if (-not $inScope) { continue }

    $lines = [System.IO.File]::ReadAllLines($file.FullName, [System.Text.Encoding]::UTF8)
    $participants = @{}
    $commandType = ""

    foreach ($line in $lines) {
        if ($line -match '^\s*participant\s+"([^"]*)"\s+as\s+(\w+)') {
            $label = $Matches[1]
            $id = $Matches[2]
            $pkg = ""
            if ($label -match '\(([\w.]+)\)') { $pkg = $Matches[1] }
            $participants[$id] = $pkg
            continue
        }
        if ($line -notmatch '^\s*(\[|\w+)\s*(->|-->|->>|-->>)\s*(\]|\w+)\s*:\s*(.+)$') { continue }
        $from = $Matches[1]
        $arrow = $Matches[2]
        $to = $Matches[3]
        $text = $Matches[4]
        if ($to -eq ']') { continue }
        if ($text -match '\(\s*(\w*Command)\s*\)') { $commandType = $Matches[1] }
        if ($text -match 'command\.(\w+)') {
            $field = $Matches[1]
            if ($commandType) {
                $command = $classifiers | Where-Object { $_.alias -eq $commandType -or $_.name -eq $commandType } | Select-Object -First 1
                if ($command) {
                    if ($command.fields -notcontains $field) {
                        Emit-Error "L1-command-field" "$($file.Name):$($participants[$to])" "command.$field is not declared in $commandType ($($command.fields -join ', '))"
                    }
                }
            }
        }
        if ($arrow -ne '->') { continue }
        if ($to -eq $from) { continue }
        if ($to -notin $participants.Keys) { continue }
        $targetPkg = $participants[$to]
        if (-not $targetPkg) {
            Emit-Warn "L1-op" "$($file.Name)" "participant '$to' has no package hint; skipped"
            continue
        }
        if ($text -notmatch '^([A-Za-z]\w*)\s*\(') {
            if ($text -match '^([A-Za-z]\w*)$') {
                Emit-Warn "L1-op" "$($file.Name)" "solid call without arguments: '$text'"
            }
            continue
        }
        $op = $Matches[1]
        $targets = $classifiers | Where-Object { $_.fqcn -eq $targetPkg }
        if (-not $targets) {
            Emit-Warn "L1-op" "$($file.Name)" "no classifiers declared in package '$targetPkg' (target of '$op')"
            continue
        }
        $found = $false
        foreach ($t in $targets) {
            if ($t.ops -contains $op) { $found = $true; break }
        }
        if (-not $found) {
            Emit-Error "L1-op" "$($file.Name)" "'$op' is not declared on any classifier of '$targetPkg'"
        }
    }
}

# ---------------------------------------------------------------------------
# L2: types referenced by in-scope class diagrams must be declared.
# ---------------------------------------------------------------------------

$typeRefs = @{}
foreach ($file in $files) {
    if ($file.Name -notlike "*.classDiagram.plantuml") { continue }
    $inScope = $true
    if ($Include.Count -gt 0) {
        $inScope = $false
        foreach ($pattern in $Include) {
            if ($file.Name -like $pattern -or $file.FullName -like "*$pattern*") { $inScope = $true; break }
        }
    }
    if (-not $inScope) { continue }

    $lines = [System.IO.File]::ReadAllLines($file.FullName, [System.Text.Encoding]::UTF8)
    $inNote = $false
    foreach ($line in $lines) {
        if ($line -match '^\s*note\b') { $inNote = $true }
        if ($inNote -and $line -match '^\s*end\s+note\b') { $inNote = $false; continue }
        if ($inNote) { continue }
        if ($line.TrimStart().StartsWith("'")) { continue }
        $types = New-Object System.Collections.ArrayList
        if ($line -match '^\s*[+-]\s+([A-Za-z]\w*)\s*:\s*(.+)$') {
            foreach ($token in [regex]::Matches($Matches[2], '[A-Z][A-Za-z]\w*')) { [void]$types.Add($token.Value) }
        }
        if ($line -match '^\s*(?:\{static\}\s*)?[+~#-]\s*([A-Za-z]\w*)\s*\(([^)]*)\)(?:\s*:\s*([\w<>,. ]+))?') {
            foreach ($token in [regex]::Matches($Matches[3], '[A-Z][A-Za-z]\w*')) { [void]$types.Add($token.Value) }
        }
        if ($line -match '(?:\.\.>|-->|o--|\*--|--\|>|-->)\s*([\w.]+)') {
            $target = $Matches[1]
            $last = $target.Substring($target.LastIndexOf('.') + 1)
            if ($last -cmatch '^[A-Z]') { [void]$types.Add($last) }
        }
        foreach ($type in $types) {
            if ($builtinTypes -contains $type) { continue }
            if ($declaredNames.Contains($type)) { continue }
            if ($typeRefs.ContainsKey($type)) { $typeRefs[$type] += @($file.Name) } else { $typeRefs[$type] = @($file.Name) }
        }
    }
}
foreach ($entry in $typeRefs.GetEnumerator() | Sort-Object Name) {
    Emit-Error "L2-type" "$($entry.Value | Select-Object -Unique | Out-String -Stream | Select-Object -First 1)" "type '$($entry.Key)' is referenced but not declared in any class diagram"
}

# ---------------------------------------------------------------------------
# L3: code authority over already-existing packages and classifiers.
# ---------------------------------------------------------------------------

if ($SourceRoot) {
    $sourceRootFull = (Resolve-Path $SourceRoot).Path
    $allSourceFiles = @(Get-ChildItem $sourceRootFull -File -Recurse)
    $allSourceDirs = @(Get-ChildItem $sourceRootFull -Directory -Recurse)

    $contentCache = @{}
    function Get-SourceContent([string]$path) {
        if (-not $contentCache.ContainsKey($path)) {
            $contentCache[$path] = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
        }
        return $contentCache[$path]
    }

    function Test-NewPackagePrefix([string]$fqcn) {
        foreach ($np in $NewPackages) { if ($fqcn -like "$np*") { return $true } }
        return $false
    }

    $frameworkPrefixes = @("java.","javax.","jakarta.","kotlin.","lombok.","org.springframework.","org.hibernate.","org.slf4j.","com.vaadin.")

    function Test-FrameworkFqcn([string]$fqcn) {
        foreach ($prefix in $frameworkPrefixes) { if ($fqcn.StartsWith($prefix, [System.StringComparison]::Ordinal)) { return $true } }
        return $false
    }

    function Check-Classifier([hashtable]$item, [string]$fileName) {
        if (-not $item) { return }
        if (Test-NewPackagePrefix $item.fqcn) { return }
        if (Test-FrameworkFqcn $item.fqcn) { return }
        if ($item.markerNew) { return }
        $shortName = $item.fqcn.Substring($item.fqcn.LastIndexOf('.') + 1)
        $srcFile = $allSourceFiles | Where-Object { $_.BaseName -eq $shortName } | Select-Object -First 1
        if (-not $srcFile) {
            Emit-Error "L3-class" "$fileName" "'$($item.fqcn)' does not exist in the production source tree"
            return
        }
        if ($item.ops.Count -eq 0) { return }
        $content = Get-SourceContent $srcFile.FullName
        foreach ($op in $item.ops) {
            if ($content -notmatch ([regex]::Escape($op) + '\s*\(')) {
                Emit-Error "L3-op" "$fileName" "operation '$op' of '$($item.fqcn)' not found in source file '$($srcFile.Name)'"
            }
        }
    }

foreach ($file in $files) {
    if ($file.Name -notlike "*.classDiagram.plantuml") { continue }
    $inScope = $true
    if ($Include.Count -gt 0) {
        $inScope = $false
        foreach ($pattern in $Include) {
            if ($file.Name -like $pattern -or $file.FullName -like "*$pattern*") { $inScope = $true; break }
        }
    }
    if (-not $inScope) { continue }

        $lines = [System.IO.File]::ReadAllLines($file.FullName, [System.Text.Encoding]::UTF8)
        $packageFqcn = ""
        $current = $null
        $inNote = $false
        $prevLine = ""
        foreach ($line in $lines) {
            if ($line -match '^\s*note\b') { $inNote = $true }
            if ($inNote -and $line -match '^\s*end\s+note\b') { $inNote = $false; continue }
            if ($inNote) { continue }
            if ($line -match '^\s*package\s+\w+\s+as\s+"([^"]+)"' -or $line -match '^\s*package\s+"([^"]+)"') {
                if ($current) { Check-Classifier $current $file.Name; $current = $null }
                $packageFqcn = $Matches[1]
                continue
            }
            if ($line -match '^\s*(abstract\s+)?(class|interface|enum)\s+(?:"([^"]+)"\s+as\s+(\w+)|(\w+))') {
                if ($current) { Check-Classifier $current $file.Name }
                if ($Matches[3]) { $name = $Matches[4] } else { $name = $Matches[5] }
                $fqcn = if ($line -match 'as\s+"([\w.\\\n]+)"') { (($Matches[1] -replace '\\n\.', '.') -replace '\\n', '.').TrimEnd('.') }
                        elseif ($packageFqcn) { "$packageFqcn.$name" }
                        else { $name }
                $current = @{
                    fqcn = $fqcn
                    markerNew = (($line -match 'NEW\s+in') -or ($prevLine -match 'NEW\s+in'))
                    ops = New-Object System.Collections.ArrayList
                }
                continue
            }
            if (-not $current) { continue }
            if ($line -match 'NEW\s+in') { $current.markerNew = $true }
            if ($line -match '^\s*(?:\{static\}\s*)?[+~#-]\s*([A-Za-z]\w*)\s*\(') {
                $opExempt = ($line -match 'NEW\s+in') -or ($prevLine -match 'NEW\s+in')
                if (-not $opExempt) { [void]$current.ops.Add($Matches[1]) }
            }
            if ($line -match '^\s*\}') {
                Check-Classifier $current $file.Name
                $current = $null
            }
            $prevLine = $line
        }
        if ($current) { Check-Classifier $current $file.Name }
    }

    foreach ($file in $files) {
        if ($file.Name -notlike "*.packageDiagram.plantuml") { continue }
        $inScope = $true
        if ($Include.Count -gt 0) {
            $inScope = $false
            foreach ($pattern in $Include) {
                if ($file.Name -like $pattern -or $file.FullName -like "*$pattern*") { $inScope = $true; break }
            }
        }
        if (-not $inScope) { continue }

        $lines = [System.IO.File]::ReadAllLines($file.FullName, [System.Text.Encoding]::UTF8)
        foreach ($line in $lines) {
            if ($line -match '^\s*package\s+"([\w.]+)"\s*$') {
                $pkg = $Matches[1]
                if (Test-NewPackagePrefix $pkg) { continue }
                $relPath = $pkg -replace '\.', '\'
                $dir = $allSourceDirs |
                    Where-Object { $_.FullName.Substring($sourceRootFull.Length).TrimStart('\').EndsWith('\' + $relPath) } |
                    Sort-Object { $_.FullName.Length } |
                    Select-Object -First 1
                if (-not $dir) {
                    Emit-Error "L3-package" "$($file.Name)" "package '$pkg' does not exist in the production source tree"
                }
            }
        }
    }
}

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

foreach ($w in $warns) { Write-Output $w }
foreach ($e in $errors) { Write-Output $e }
$allCalls = 0
foreach ($file in $files) { if ($file.Name -like "*.sequenceDiagram.plantuml") { $allCalls++ } }

Write-Output ("DESIGN_CONSISTENCY errors={0} warnings={1} dcds={2} dsds={3} source={4}" -f $errors.Count, $warns.Count, $classifiers.Count, $allCalls, $(if ($SourceRoot) { "yes" } else { "no" }))
if ($errors.Count -gt 0) { exit 2 } else { exit 0 }
