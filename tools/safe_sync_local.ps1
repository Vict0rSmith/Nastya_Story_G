param(
    [Parameter(Mandatory = $true)]
    [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
    Write-Error $Message
    exit 1
}

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    Fail "RepoRoot is empty. Configure NASTYA_LOCAL_REPO before enabling automatic sync."
}

$gitCommand = Get-Command git.exe -ErrorAction SilentlyContinue
if (-not $gitCommand) {
    Fail "git.exe is not available to the runner account. Install Git for Windows for all users or add Git to the system PATH, then restart the runner service."
}

Write-Host "Git executable: $($gitCommand.Source)"

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    Fail "Local repository path does not exist or is not accessible to the runner account: $RepoRoot"
}

$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
Write-Host "Checking local Nastya Story repository: $RepoRoot"

try {
    $actualRoot = (git -C $RepoRoot rev-parse --show-toplevel 2>&1).Trim()
} catch {
    Fail "The configured path is not a Git repository or cannot be accessed by the runner account: $RepoRoot"
}

if (-not $actualRoot) {
    Fail "Unable to resolve Git repository root for: $RepoRoot"
}

$origin = (git -C $RepoRoot remote get-url origin 2>&1).Trim()
if ($LASTEXITCODE -ne 0) {
    Fail "Unable to read origin remote."
}

if ($origin -notmatch 'Vict0rSmith[/\\]Nastya_Story_G(?:\.git)?$') {
    Fail "Unexpected origin remote: $origin. Refusing to sync a different repository."
}

$branch = (git -C $RepoRoot branch --show-current 2>&1).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') {
    Fail "Local working copy must be on branch 'main'. Current branch: '$branch'."
}

$dirty = git -C $RepoRoot status --porcelain
if ($LASTEXITCODE -ne 0) {
    Fail "Unable to read git status."
}

if ($dirty) {
    Write-Host "Local working tree has uncommitted changes:" -ForegroundColor Yellow
    $dirty | ForEach-Object { Write-Host "  $_" -ForegroundColor Yellow }
    Fail "Automatic sync stopped. Commit, discard manually, or otherwise resolve local changes first."
}

Write-Host "Fetching origin..."
git -C $RepoRoot fetch origin
if ($LASTEXITCODE -ne 0) {
    Fail "git fetch origin failed. If this is a private repository, verify that the Windows account running the GitHub Actions Runner can authenticate to GitHub and can access this working copy."
}

$countsRaw = (git -C $RepoRoot rev-list --left-right --count main...origin/main 2>&1).Trim()
if ($LASTEXITCODE -ne 0) {
    Fail "Unable to compare local main with origin/main."
}

$parts = $countsRaw -split '\s+'
if ($parts.Count -lt 2) {
    Fail "Unexpected rev-list result: $countsRaw"
}

[int]$ahead = $parts[0]
[int]$behind = $parts[1]

Write-Host "Local main ahead: $ahead; behind: $behind"

if ($ahead -gt 0) {
    Fail "Local main contains commit(s) not present in origin/main. Automatic sync stopped to avoid overwriting or hiding local work. Push/reconcile manually first."
}

if ($behind -eq 0) {
    $syncedSha = (git -C $RepoRoot rev-parse HEAD).Trim()
    Write-Host "SYNCED: local main = origin/main = $syncedSha; working tree clean."
    exit 0
}

Write-Host "Applying safe fast-forward from origin/main..."
git -C $RepoRoot pull --ff-only origin main
if ($LASTEXITCODE -ne 0) {
    Fail "Fast-forward pull failed. No reset, rebase, stash, or force operation was attempted. Resolve the repository state manually."
}

& (Join-Path $PSScriptRoot 'check_git_sync.ps1') -RepoRoot $RepoRoot
if ($LASTEXITCODE -ne 0) { Fail 'Final synchronization check failed.' }
