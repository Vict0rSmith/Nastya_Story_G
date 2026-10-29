param([Parameter(Mandatory = $true)][string]$RepoRoot)

$ErrorActionPreference = 'Stop'
function GitValue([string[]]$Arguments) {
    $result = & git -C $RepoRoot @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Git check failed: $($Arguments -join ' ')" }
    return ($result -join "`n").Trim()
}

$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$root = GitValue @('rev-parse', '--show-toplevel')
if ((Resolve-Path -LiteralPath $root).Path -ne $RepoRoot) { throw 'RepoRoot must be the Git root.' }
$origin = GitValue @('remote', 'get-url', 'origin')
if ($origin -notmatch '^(https://github.com/|git@github.com:)Vict0rSmith/Nastya_Story_G(?:\.git)?$') {
    throw "Unexpected origin: $origin"
}
$null = GitValue @('fetch', 'origin')
$branch = GitValue @('branch', '--show-current')
$dirty = GitValue @('status', '--porcelain')
$counts = (GitValue @('rev-list', '--left-right', '--count', 'HEAD...origin/main')) -split '\s+'
$localMain = GitValue @('rev-parse', 'main')
$remoteMain = GitValue @('rev-parse', 'origin/main')
$headSha = GitValue @('rev-parse', 'HEAD')
if ($branch -ne 'main' -or $dirty -or $headSha -ne $remoteMain -or $localMain -ne $remoteMain) {
    Write-Output "SYNC PENDING: branch=$branch; ahead=$($counts[0]); behind=$($counts[1]); dirty=$([bool]$dirty)"
    Write-Output 'Do not start the next implementation. Reconcile, publish and update local main first; preserve unfinished work.'
    exit 1
}
Write-Output "SYNCED: main = origin/main = $headSha; working tree clean."
