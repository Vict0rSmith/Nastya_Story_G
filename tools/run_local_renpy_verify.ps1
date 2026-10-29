param(
    [Parameter(Mandatory = $true)]
    [string]$RepoRoot,

    [Parameter(Mandatory = $true)]
    [string]$RenpySdkRoot,

    [string]$LintOutput = "",
    [string]$TestOutput = "",
    [string]$ScreenshotOutput = "",
    # Saves/persistent for lint and tests. Default: a fresh temporary directory per run,
    # so verification never touches the player's real persistent data.
    [string]$SaveDir = "",
    # Test window drawable size in pixels; converted to logical units using the Windows DPI scale.
    [ValidatePattern('^\d+x\d+$')]
    [string]$WindowSize = "1920x1080",
    [ValidateRange(1, 900)]
    [int]$RuntimeTestTimeoutSeconds = 120,
    # Ren'Py accepts a suite or a fully qualified testcase name.
    [ValidatePattern('^[A-Za-z_][A-Za-z0-9_]*(?:(?:\.|::)[A-Za-z_][A-Za-z0-9_]*)*$')]
    [string[]]$Tests = @('nastya_runtime'),
    [switch]$LintOnly,
    [switch]$DetailedReport
)

$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
    Write-Error $Message
    exit 1
}

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    Fail "Nastya Story repository path does not exist: $RepoRoot"
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot "game") -PathType Container)) {
    Fail "The configured repository does not contain a game directory: $RepoRoot"
}

if (-not (Test-Path -LiteralPath $RenpySdkRoot -PathType Container)) {
    Fail "Ren'Py SDK root does not exist: $RenpySdkRoot"
}

$renpyPy = Join-Path $RenpySdkRoot "renpy.py"
$renpyPython = Join-Path $RenpySdkRoot "lib\py3-windows-x86_64\python.exe"

if (-not (Test-Path -LiteralPath $renpyPy -PathType Leaf)) {
    Fail "renpy.py was not found under Ren'Py SDK root: $renpyPy"
}

if (-not (Test-Path -LiteralPath $renpyPython -PathType Leaf)) {
    Fail "Ren'Py bundled Python was not found: $renpyPython"
}

$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
# `-File` invocations pass "a,b" as one string; accept comma-separated selections.
$Tests = @($Tests | ForEach-Object { "$_" -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
foreach ($testName in $Tests) {
    if ($testName -notmatch '^[A-Za-z_][A-Za-z0-9_]*(?:(?:\.|::)[A-Za-z_][A-Za-z0-9_]*)*$') { Fail "Invalid test selection: $testName" }
}
$RenpySdkRoot = (Resolve-Path -LiteralPath $RenpySdkRoot).Path

if ([string]::IsNullOrWhiteSpace($LintOutput)) {
    $LintOutput = Join-Path $env:TEMP "nastya-story-renpy-lint.txt"
}
if ([string]::IsNullOrWhiteSpace($TestOutput)) {
    $TestOutput = Join-Path $env:TEMP "nastya-story-renpy-tests.txt"
}
if ([string]::IsNullOrWhiteSpace($ScreenshotOutput)) {
    $ScreenshotOutput = Join-Path $env:TEMP "nastya-story-renpy-screenshots"
}

foreach ($outputPath in @($LintOutput, $TestOutput)) {
    $parent = Split-Path -Parent $outputPath
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
}

if ([string]::IsNullOrWhiteSpace($SaveDir)) {
    $SaveDir = Join-Path (Join-Path $env:TEMP "nastya-story-renpy-savedir") ([guid]::NewGuid().ToString('N'))
}
New-Item -ItemType Directory -Force -Path $SaveDir | Out-Null
$SaveDir = (Resolve-Path -LiteralPath $SaveDir).Path

# Each invocation owns a new directory; preserve previous evidence and baselines.
$ScreenshotOutput = Join-Path $ScreenshotOutput ([guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $ScreenshotOutput | Out-Null
$ScreenshotOutput = (Resolve-Path -LiteralPath $ScreenshotOutput).Path

Write-Host "Nastya Story local repository: $RepoRoot"
Write-Host "Ren'Py SDK: $RenpySdkRoot"
Write-Host "Ren'Py Python: $renpyPython"
Write-Host "Lint report: $LintOutput"
Write-Host "Runtime test report: $TestOutput"
Write-Host "Runtime screenshots: $ScreenshotOutput"
Write-Host "Ren'Py save directory: $SaveDir"
Write-Host "Runtime test timeout: $RuntimeTestTimeoutSeconds seconds"
Write-Host ""

Write-Host "Ren'Py version:"
& $renpyPython $renpyPy --version
if ($LASTEXITCODE -ne 0) {
    Fail "Unable to start the configured Ren'Py SDK."
}

Write-Host ""
Write-Host "Running Ren'Py lint..."
# Never reuse an earlier PASS report when this invocation fails before runtime.
Set-Content -LiteralPath $TestOutput -Value 'Runtime: NOT RUN (verification started)' -Encoding UTF8
Remove-Item -LiteralPath $LintOutput -Force -ErrorAction SilentlyContinue
& $renpyPython $renpyPy --savedir $SaveDir $RepoRoot lint $LintOutput --error-code --all-problems --check-unclosed-tags
$lintExitCode = $LASTEXITCODE

if (-not (Test-Path -LiteralPath $LintOutput -PathType Leaf)) {
    Fail "Ren'Py did not create the requested lint report file."
}
if ($DetailedReport -or $lintExitCode -ne 0) {
    if ($DetailedReport) { Get-Content -LiteralPath $LintOutput | ForEach-Object { Write-Host $_ } }
    else { Get-Content -LiteralPath $LintOutput | Select-Object -First 80 | ForEach-Object { Write-Host $_ } }
}

if ($lintExitCode -ne 0) {
    Fail "Ren'Py lint reported one or more errors (exit code $lintExitCode)."
}

Write-Host "Ren'Py lint completed successfully." -ForegroundColor Green
Write-Host ""
if ($LintOnly) {
    "Runtime: NOT RUN (LintOnly)" | Set-Content -LiteralPath $TestOutput -Encoding UTF8
    Write-Host "Runtime: NOT RUN (LintOnly). Report: $TestOutput"
    exit 0
}
if (-not $Tests -or $Tests.Count -eq 0) { Fail "Select at least one test or use -LintOnly." }
Set-Content -LiteralPath $TestOutput -Value '' -Encoding UTF8

# Ren'Py sizes its window in Windows logical units; divide by the DPI scale so the
# screenshot surface is exactly $WindowSize pixels (crops in tests assume 1920x1080).
$dpiScale = 1.0
try {
    Add-Type -Namespace NastyaVerify -Name Dpi -MemberDefinition @"
[DllImport("user32.dll")] public static extern IntPtr GetDC(IntPtr hWnd);
[DllImport("user32.dll")] public static extern int ReleaseDC(IntPtr hWnd, IntPtr hDC);
[DllImport("gdi32.dll")] public static extern int GetDeviceCaps(IntPtr hdc, int index);
"@ -ErrorAction SilentlyContinue
    $hdc = [NastyaVerify.Dpi]::GetDC([IntPtr]::Zero)
    $logicalWidth = [NastyaVerify.Dpi]::GetDeviceCaps($hdc, 8)    # HORZRES
    $physicalWidth = [NastyaVerify.Dpi]::GetDeviceCaps($hdc, 118) # DESKTOPHORZRES
    [void][NastyaVerify.Dpi]::ReleaseDC([IntPtr]::Zero, $hdc)
    if ($logicalWidth -gt 0 -and $physicalWidth -gt 0) { $dpiScale = $physicalWidth / $logicalWidth }
} catch { $dpiScale = 1.0 }
$windowParts = $WindowSize.Split('x')
$logicalWindowSize = "{0}x{1}" -f [int][math]::Round([int]$windowParts[0] / $dpiScale), [int][math]::Round([int]$windowParts[1] / $dpiScale)
Write-Host ("Test window: {0} px (DPI scale {1}, logical {2})" -f $WindowSize, $dpiScale, $logicalWindowSize)

foreach ($testName in ($Tests | Select-Object -Unique)) {
Write-Host "Running Ren'Py test: $testName"

$env:RENPY_DISABLE_SOUND = "pss"
$env:RENPY_DISABLE_JOYSTICK = "1"
$env:RENPY_DISABLE_FULLSCREEN = "1"
$env:NASTYA_RENPY_TEST_WINDOW_SIZE = $logicalWindowSize
# Works both inside a git checkout and in a plain folder (or without git installed).
$vcRevision = $null
if (Get-Command git -ErrorAction SilentlyContinue) {
    try { $vcRevision = & git -C $RepoRoot rev-parse HEAD 2>$null } catch { $vcRevision = $null }
    if ($LASTEXITCODE -ne 0) { $vcRevision = $null }
}
$env:RENPY_TEST_VC_REVISION = if ($vcRevision) { "$vcRevision".Trim() } else { "no-git" }
$env:NASTYA_RENPY_SCREENSHOT_DIR = Join-Path $ScreenshotOutput $testName.Replace(':', '-')

$stdoutPath = "$TestOutput.stdout"
$stderrPath = "$TestOutput.stderr"
Remove-Item -LiteralPath $stdoutPath, $stderrPath -Force -ErrorAction SilentlyContinue

$testArguments = @(
    ('"{0}"' -f $renpyPy),
    "--savedir",
    ('"{0}"' -f $SaveDir),
    ('"{0}"' -f $RepoRoot),
    "test",
    $testName,
    "--report-detailed",
    "--hide-header",
    "--hide-execution", "all"
)

$testStart = New-Object System.Diagnostics.ProcessStartInfo
$testStart.FileName = $renpyPython
$testStart.Arguments = $testArguments -join ' '
$testStart.WorkingDirectory = $RenpySdkRoot
$testStart.UseShellExecute = $false
$testStart.CreateNoWindow = $true
$testStart.RedirectStandardInput = $true
$testStart.RedirectStandardOutput = $true
$testStart.RedirectStandardError = $true
$testProcess = New-Object System.Diagnostics.Process
$testProcess.StartInfo = $testStart
if (-not $testProcess.Start()) { Fail "Unable to start Ren'Py runtime tests." }
$testProcess.StandardInput.Close()
$stdoutRead = $testProcess.StandardOutput.ReadToEndAsync()
$stderrRead = $testProcess.StandardError.ReadToEndAsync()

$finished = $testProcess.WaitForExit($RuntimeTestTimeoutSeconds * 1000)
if (-not $finished) {
    Write-Warning "Ren'Py runtime tests exceeded $RuntimeTestTimeoutSeconds seconds. Terminating the process tree."
    & taskkill.exe /PID $testProcess.Id /T /F | Out-Host
    $testProcess.WaitForExit()
    [System.IO.File]::WriteAllText($stdoutPath, $stdoutRead.GetAwaiter().GetResult())
    [System.IO.File]::WriteAllText($stderrPath, $stderrRead.GetAwaiter().GetResult())
    @(
        "Ren'Py runtime tests timed out after $RuntimeTestTimeoutSeconds seconds.",
        "This usually means the test runner could not obtain an interactive graphics context or a testcase blocked indefinitely."
    ) | Add-Content -LiteralPath $TestOutput -Encoding UTF8
    foreach ($timeoutLog in @($stdoutPath, $stderrPath)) {
        if (Test-Path -LiteralPath $timeoutLog) { Get-Content -LiteralPath $timeoutLog | Add-Content -LiteralPath $TestOutput -Encoding UTF8 }
    }
    Fail "Ren'Py automated runtime tests timed out."
}

# Ensure redirected streams have been flushed before reading the report.
$testProcess.WaitForExit()
[System.IO.File]::WriteAllText($stdoutPath, $stdoutRead.GetAwaiter().GetResult())
[System.IO.File]::WriteAllText($stderrPath, $stderrRead.GetAwaiter().GetResult())
$testProcess.Refresh()
$testExitCode = $null
try {
    $testExitCode = $testProcess.ExitCode
}
catch {
    Write-Warning "PowerShell could not read the Ren'Py process exit code; validating the official rpytest report instead."
}

$combined = @()
if (Test-Path -LiteralPath $stdoutPath -PathType Leaf) {
    $combined += Get-Content -LiteralPath $stdoutPath
}
if (Test-Path -LiteralPath $stderrPath -PathType Leaf) {
    $stderrLines = @(Get-Content -LiteralPath $stderrPath)
    if ($stderrLines.Count -gt 0) {
        $combined += ""
        $combined += "----- STDERR -----"
        $combined += $stderrLines
    }
}
"Test selection: $testName" | Add-Content -LiteralPath $TestOutput -Encoding UTF8
$combined | Add-Content -LiteralPath $TestOutput -Encoding UTF8
Remove-Item -LiteralPath $stdoutPath, $stderrPath -Force -ErrorAction SilentlyContinue

$passedMarker = $combined | Where-Object { $_ -match '^\[rpytest\]\s+Status:\s+PASSED\s*$' }
$failedMarker = $combined | Where-Object { $_ -match '^\[rpytest\]\s+Status:\s+(FAILED|ERROR)\s*$' }
# An init traceback can coexist with a later PASSED test report.
$runtimeError = $combined | Where-Object { $_ -match '^Full traceback:|^Traceback \(most recent call last\):' }
$executedCases = $combined | Where-Object { $_ -match '^\[rpytest\]\s+Test cases\s*:.*\|\s*[1-9][0-9]* passed' }
if ($DetailedReport) {
    $combined | ForEach-Object { Write-Host $_ }
} elseif ($failedMarker -or $runtimeError -or -not $passedMarker -or -not $executedCases -or ($null -ne $testExitCode -and $testExitCode -ne 0)) {
    $combined | Select-Object -Last 60 | ForEach-Object { Write-Host $_ }
} else {
    $combined | Where-Object { $_ -match '^\[rpytest\]\s+(Status\s*:|Test cases\s*:|Assertions\s*:|Time\s*:)' } | ForEach-Object { Write-Host $_ }
}

if ($failedMarker) {
    Fail "Ren'Py automated runtime tests reported a failing rpytest status."
}
if ($runtimeError) { Fail "Ren'Py reported a traceback; see $TestOutput" }
if (-not $executedCases) { Fail "No passing testcases executed for $testName; see $TestOutput" }

if ($null -ne $testExitCode -and $testExitCode -ne 0) {
    Fail "Ren'Py automated runtime tests failed (exit code $testExitCode)."
}

if (-not $passedMarker) {
    Fail "Ren'Py automated runtime tests did not produce a PASSED rpytest status."
}

Write-Host "Ren'Py automated runtime tests completed successfully." -ForegroundColor Green
}
$screenshots = @(Get-ChildItem -LiteralPath $ScreenshotOutput -Filter *.png -File -Recurse -ErrorAction SilentlyContinue)
Write-Host "Captured screenshots: $($screenshots.Count). Directory: $ScreenshotOutput"
Write-Host "Full runtime report: $TestOutput"
