param(
    [Parameter(Mandatory = $true)][string]$StartRef,
    [Parameter(Mandatory = $true)][string]$EndRef,
    [string]$Repository = ".",
    [string]$Timezone = "Europe/Madrid"
)

$ErrorActionPreference = "Stop"

function Resolve-TimeZone {
    param([string]$Name)
    try {
        return [TimeZoneInfo]::FindSystemTimeZoneById($Name)
    } catch {
        if ($Name -eq "Europe/Madrid") {
            return [TimeZoneInfo]::FindSystemTimeZoneById("Romance Standard Time")
        }
        throw
    }
}

Push-Location $Repository
try {
    $startResolved = (& git rev-parse --verify "$StartRef^{commit}").Trim()
    $endResolved = (& git rev-parse --verify "$EndRef^{commit}").Trim()

    & git merge-base --is-ancestor $startResolved $endResolved
    $ancestor = ($LASTEXITCODE -eq 0)

    $range = "$startResolved..$endResolved"
    $rawCommits = @(& git log --format="%H%x09%aI%x09%cI" $range)
    $tz = Resolve-TimeZone -Name $Timezone
    $commits = New-Object System.Collections.Generic.List[object]
    $authorDates = New-Object System.Collections.Generic.List[string]
    $committerDates = New-Object System.Collections.Generic.List[string]

    foreach ($line in $rawCommits) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        $parts = $line.Split("`t")
        if ($parts.Count -lt 3) { continue }
        $authorIso = [DateTimeOffset]::Parse($parts[1], [Globalization.CultureInfo]::InvariantCulture)
        $committerIso = [DateTimeOffset]::Parse($parts[2], [Globalization.CultureInfo]::InvariantCulture)
        $authorLocal = [TimeZoneInfo]::ConvertTime($authorIso, $tz)
        $committerLocal = [TimeZoneInfo]::ConvertTime($committerIso, $tz)
        $authorDate = $authorLocal.ToString("yyyy-MM-dd")
        $committerDate = $committerLocal.ToString("yyyy-MM-dd")
        $authorDates.Add($authorDate)
        $committerDates.Add($committerDate)
        $commits.Add([ordered]@{
            hash = $parts[0]
            author_date = $authorDate
            committer_date = $committerDate
            author_timestamp = $authorIso.ToString("o")
            committer_timestamp = $committerIso.ToString("o")
        })
    }

    $uniqueAuthorDates = @($authorDates | Sort-Object -Unique)
    $uniqueCommitterDates = @($committerDates | Sort-Object -Unique)
    $dirty = @(& git status --porcelain)

    $result = [ordered]@{
        start_ref = $startResolved
        end_ref = $endResolved
        commit_range = $range
        timezone = $Timezone
        ancestor = $ancestor
        commit_count = $commits.Count
        effective_days = $uniqueAuthorDates.Count
        commit_days = $uniqueAuthorDates
        committer_effective_days = $uniqueCommitterDates.Count
        committer_days = $uniqueCommitterDates
        first_author_date = if ($uniqueAuthorDates.Count -gt 0) { $uniqueAuthorDates[0] } else { $null }
        last_author_date = if ($uniqueAuthorDates.Count -gt 0) { $uniqueAuthorDates[$uniqueAuthorDates.Count - 1] } else { $null }
        working_tree_clean = ($dirty.Count -eq 0)
        dirty_paths = $dirty
        commits = $commits
        generated_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")
    }

    $result | ConvertTo-Json -Depth 8
} finally {
    Pop-Location
}
