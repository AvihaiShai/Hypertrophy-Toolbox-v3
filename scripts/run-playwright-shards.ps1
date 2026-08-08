<#
.SYNOPSIS
    Run the CI-required functional Playwright set in N isolated processes.
    Only -Shards 1 is supported. N>1 is REJECTED, not merely unproven.

.DESCRIPTION
    STATUS: -Shards 1 is measured and reliable at 477/477 in 719.0s. Same-machine
    N>1 is rejected by evidence and closed -- see docs/DECISIONS.md ADR-006. It
    remains runnable so the diagnosis stays reproducible, but a green N>1 run is
    NOT evidence: do not use it as a development lane, to select a shard count,
    or to claim a local speedup.

    Measured on this repository, 25 required specs / 477 tests:

        N=1  719.0s  477 passed
        N=2  390.8s  1 failed      <- not usable, and timings invalid (see below)
        N=3  401.4s  9 failed      <- not usable, and timings invalid
        N=4  341.4s  28 failed     <- not usable, and timings invalid

    Those N>1 timings are invalid as evidence: each configuration inherited the
    previous one's TIME_WAIT backlog. A controlled re-run from a measured clean
    start (gate waited 120.8s; leftovers 0, busy candidate ports 0, TIME_WAIT on
    candidate ports 0, total TIME_WAIT 29) still failed 4/477 at N=2 in 407.2s,
    with both shards exiting 1. Per the stop rule, N=3 and N=4 were not re-run.

    ROOT CAUSE (confirmed, not a hypothesis). Werkzeug's WSGIRequestHandler
    speaks HTTP/1.0 and closes the connection per request, so every request
    holds an ephemeral port for the full 120s recycle interval. ~89.9% of the
    suite's requests are static assets (30,752/34,253), and each fresh browser
    context re-fetches a page's whole asset set per navigation. N=1 averaged
    ~57 connections/s and ~6,840 steady-state ports; N=2 averaged ~85/s and
    peaked at 16,318 of the 16,384-port dynamic range (99.6%). Sharding does not
    reduce total connections, it compresses them into less wall-clock, raising
    the rate against a fixed pool -- which is why failures scale with N. CPU,
    processor queue, memory and disk were measured and were not limiting.

    Every remedy is out of bounds: OS/TCP/registry/port/TIME_WAIT tuning makes
    the suite a property of one machine; HTTP/1.1 keep-alive or asset
    cache-policy changes alter what the suite exercises relative to production;
    a new WSGI server adds a dependency to serve a benchmark; retries, timeout
    inflation, shared browser contexts and reduced coverage buy the number by
    weakening the gate.

    CI's two-shard split is unaffected by any of this: its shards run on
    separate runners, so they share none of the machine state implicated here.
    Nothing in this file informs the CI shard count.

    Playwright's own `workers` setting shares one webServer, one database, and
    one artifacts root across parallel workers. This suite cannot use it: the
    specs mutate shared application state (plan rows, user profile, logged
    sets), which is why the config pins `fullyParallel: false` and `workers: 1`.

    This launcher parallelises a level up instead. Each shard is a separate
    `npx playwright test` process with `--shard=i/N`, its own port, its own
    SQLite file, and its own artifacts root, so nothing is shared and the
    within-shard serial ordering the specs rely on is untouched. That is the
    same isolation CI's 2-way matrix gets from running each leg on its own
    runner -- reproduced locally on one machine.

    Benchmark scope is deliberately the CI-required functional set and nothing
    else. Measuring a different group of specs than the gate actually runs
    produces numbers that cannot be used to argue about the gate.

.PARAMETER Shards
    Number of isolated shard processes. 1 is the only supported value and the
    default. Values above 1 are a rejected configuration retained for
    reproducing the ADR-006 diagnosis; they warn at runtime and their results
    are not evidence.

.PARAMETER BasePort
    First port to allocate. Shard i gets BasePort + (i - 1).

.PARAMETER OutputRoot
    Where per-shard artifacts go. Defaults to a timestamped directory under
    artifacts/shards/ so repeat runs never overwrite each other's evidence.

.PARAMETER KeepDatabases
    Keep each shard's SQLite file after the run. Off by default -- they are
    seeded copies of the catalog and cost disk for nothing once the run is
    scored.

.EXAMPLE
    ./scripts/run-playwright-shards.ps1
#>
[CmdletBinding()]
param(
    [ValidateRange(1, 8)]
    [int] $Shards = 1,

    [ValidateRange(1024, 60000)]
    [int] $BasePort = 5300,

    [string] $OutputRoot,

    # An N=1 report.json. When supplied, the summary proves this run's shards
    # partition exactly the same set of tests the serial reference ran.
    [string] $BaselineReport,

    # Off by default so the default path stays exactly what produced the
    # committed measurements. When set, a separate process samples TCP and
    # system state alongside the run; measured cost is ~70ms every 3s.
    [switch] $Telemetry,

    [switch] $KeepDatabases
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

# Mirrors the required functional gate's spec list in .github/workflows/ci.yml.
# Kept identical by tests/test_playwright_shard_launcher_contracts.py: a
# benchmark of a different set than the gate runs cannot inform a decision about
# the gate, and the drift would be invisible in the timings.
$RequiredSpecs = @(
    "e2e/accessibility.spec.ts",
    "e2e/api-integration.spec.ts",
    "e2e/body-composition.spec.ts",
    "e2e/browser-navigation-state.spec.ts",
    "e2e/dark-mode.spec.ts",
    "e2e/empty-states.spec.ts",
    "e2e/error-handling.spec.ts",
    "e2e/exercise-interactions.spec.ts",
    "e2e/fatigue-stage4-smokes.spec.ts",
    "e2e/fatigue.spec.ts",
    "e2e/learned-calibration.spec.ts",
    "e2e/nav-dropdown.spec.ts",
    "e2e/progression.spec.ts",
    "e2e/replace-exercise-errors.spec.ts",
    "e2e/smoke-navigation.spec.ts",
    "e2e/summary-pages.spec.ts",
    "e2e/superset-edge-cases.spec.ts",
    "e2e/ui-hardening.spec.ts",
    "e2e/user-profile.spec.ts",
    "e2e/validation-boundary.spec.ts",
    "e2e/visual-field-separator.spec.ts",
    "e2e/volume-progress.spec.ts",
    "e2e/volume-splitter.spec.ts",
    "e2e/workout-log.spec.ts",
    "e2e/workout-plan.spec.ts"
)

# Local-only functional specs. They are not part of the required gate, so
# including them would inflate every number against a set CI never runs.
# program-backup and erase-flow additionally perform destructive backup/restore
# and erase mutations that have no place in a repeated benchmark.
$ExcludedSpecs = @(
    "e2e/erase-flow.spec.ts",
    "e2e/fatigue-context.spec.ts",
    "e2e/listener-cleanup.spec.ts",
    "e2e/program-backup.spec.ts"
)

$LiveDatabase = (Join-Path $RepoRoot "data\database.db")
$AutoBackupDir = (Join-Path $RepoRoot "data\auto_backup")

function Test-PortFree {
    param([int] $Port)

    $listener = $null
    try {
        $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        return $true
    }
    catch {
        return $false
    }
    finally {
        if ($null -ne $listener) { $listener.Stop() }
    }
}

function Stop-ProcessTree {
    <#
        Kill the shard and everything under it. `npx` is a launcher: the Node
        test process, the Flask server it starts through webServer, and the
        Chromium children all hang off it. Killing only the top pid orphans a
        Flask holding a port and a Chromium holding memory, which then breaks
        the NEXT run's collision check for reasons that look unrelated.
    #>
    param([int] $ProcessId)

    & taskkill.exe /PID $ProcessId /T /F 2>&1 | Out-Null
}

if (-not $OutputRoot) {
    $OutputRoot = Join-Path $RepoRoot ("artifacts\shards\{0}-n{1}" -f (Get-Date -Format "yyyyMMdd-HHmmss"), $Shards)
}
if (-not [System.IO.Path]::IsPathRooted($OutputRoot)) {
    $OutputRoot = Join-Path $RepoRoot $OutputRoot
}

# ---------------------------------------------------------------- plan + guards

$Plan = @()
for ($i = 1; $i -le $Shards; $i++) {
    $shardDir = Join-Path $OutputRoot "shard-$i"
    $Plan += [PSCustomObject]@{
        Index      = $i
        Port       = $BasePort + ($i - 1)
        Directory  = $shardDir
        Database   = Join-Path $shardDir "database.e2e.db"
        JsonReport = Join-Path $shardDir "report.json"
        Stdout     = Join-Path $shardDir "stdout.txt"
        Stderr     = Join-Path $shardDir "stderr.txt"
        Process    = $null
        ExitCode   = $null
        WallSeconds = $null
    }
}

# Every collision is checked BEFORE anything starts. Discovering a taken port
# after three shards are already seeding databases leaves processes to clean up
# and a partial result that reads like a test failure.
$problems = @()

$duplicatePorts = $Plan.Port | Group-Object | Where-Object { $_.Count -gt 1 }
if ($duplicatePorts) { $problems += "duplicate ports in plan: $($duplicatePorts.Name -join ', ')" }

$duplicatePaths = $Plan.Database | Group-Object | Where-Object { $_.Count -gt 1 }
if ($duplicatePaths) { $problems += "duplicate database paths in plan: $($duplicatePaths.Name -join ', ')" }

foreach ($shard in $Plan) {
    if (-not (Test-PortFree -Port $shard.Port)) {
        $problems += "port $($shard.Port) is already in use (shard $($shard.Index))"
    }

    $resolvedDb = [System.IO.Path]::GetFullPath($shard.Database)
    if ($resolvedDb -eq [System.IO.Path]::GetFullPath($LiveDatabase)) {
        $problems += "shard $($shard.Index) would write the live database"
    }
    if ($resolvedDb.StartsWith([System.IO.Path]::GetFullPath($AutoBackupDir), [System.StringComparison]::OrdinalIgnoreCase)) {
        $problems += "shard $($shard.Index) would write under data/auto_backup"
    }
}

if ($problems.Count -gt 0) {
    Write-Host "Refusing to start:" -ForegroundColor Red
    $problems | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    exit 2
}

foreach ($shard in $Plan) {
    New-Item -ItemType Directory -Force -Path $shard.Directory | Out-Null
}

$Npx = if ($env:OS -eq "Windows_NT") { "npx.cmd" } else { "npx" }

if ($Shards -gt 1) {
    Write-Warning "UNSUPPORTED CONFIGURATION: -Shards $Shards. Same-machine N>1 is rejected by evidence (docs/DECISIONS.md ADR-006): this host's 16,384 ephemeral ports are exhausted by Werkzeug's per-request connection close, and a controlled clean-start N=2 still failed 4/477. This run is a diagnostic reproduction; its pass/fail and its timings are not evidence."
}

Write-Host "Required functional set: $($RequiredSpecs.Count) specs across $Shards shard(s)"
Write-Host "Ports: $(($Plan.Port) -join ', ')"
Write-Host "Output: $OutputRoot"
Write-Host ""

# ------------------------------------------------------------------- execution

$OverallStopwatch = [System.Diagnostics.Stopwatch]::StartNew()

$TelemetryStop = Join-Path $OutputRoot "telemetry.stop"
$TelemetryProcess = $null
if ($Telemetry) {
    Remove-Item -LiteralPath $TelemetryStop -Force -ErrorAction SilentlyContinue
    $TelemetryProcess = Start-Process `
        -FilePath "powershell.exe" `
        -ArgumentList @(
            "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", (Join-Path $RepoRoot "scripts\shard_telemetry.ps1"),
            "-RootPid", $PID,
            "-ShardPorts", (($Plan.Port) -join ','),
            "-OutFile", (Join-Path $OutputRoot "telemetry.jsonl"),
            "-StopFile", $TelemetryStop
        ) `
        -NoNewWindow -PassThru
    $null = $TelemetryProcess.Handle
    Write-Host "Telemetry sampling to $(Join-Path $OutputRoot 'telemetry.jsonl')"
}

try {
    foreach ($shard in $Plan) {
        # Start-Process gives each child a snapshot of the environment as it
        # exists at creation, so setting these immediately before each launch
        # gives every shard its own values even though all shards run at once.
        # Restored in the finally below so the caller's session is unchanged.
        $env:PW_PORT = "$($shard.Port)"
        $env:PW_DB_PATH = $shard.Database
        $env:TEST_ARTIFACTS_DIR = $shard.Directory
        $env:PLAYWRIGHT_JSON_OUTPUT_NAME = $shard.JsonReport
        $env:PW_WORKERS = "1"
        # A reused server would be the previous shard's, on the previous
        # shard's database. The whole point is that each shard starts its own.
        Remove-Item Env:PW_REUSE_SERVER -ErrorAction SilentlyContinue
        # Functional seed, always. The visual seed leaves plan rows in place and
        # every spec in the required set expects wiped user state.
        Remove-Item Env:PW_VISUAL_SEED -ErrorAction SilentlyContinue

        $arguments = @("playwright", "test") + $RequiredSpecs + @(
            "--project=chromium",
            "--workers=1",
            "--shard=$($shard.Index)/$Shards",
            "--reporter=line,json"
        )

        $shard.Process = Start-Process `
            -FilePath $Npx `
            -ArgumentList $arguments `
            -WorkingDirectory $RepoRoot `
            -NoNewWindow `
            -PassThru `
            -RedirectStandardOutput $shard.Stdout `
            -RedirectStandardError $shard.Stderr

        # Dereferencing Handle once caches it on the object, and that is the
        # only thing that keeps ExitCode and ExitTime readable after the child
        # exits. Without it `Start-Process -PassThru` hands back a Process whose
        # ExitCode reads as empty, every shard is scored as failed, and the wall
        # time comes out as a large negative number from an unset ExitTime.
        # Measured directly: a `cmd /c exit 7` child reports '' without this
        # line and 7 with it.
        $null = $shard.Process.Handle

        Write-Host "Started shard $($shard.Index)/$Shards on port $($shard.Port) (pid $($shard.Process.Id))"
    }

    Write-Host ""
    Write-Host "Waiting for all shards. A failing shard does not stop the others -- the"
    Write-Host "point of the wait is a complete failure picture, not the first red."
    Write-Host ""

    foreach ($shard in $Plan) {
        $shard.Process.WaitForExit()
        $shard.ExitCode = $shard.Process.ExitCode
        # Each shard's own wall time, measured from the launcher. Reading it off
        # the report instead would give summed testcase duration, which excludes
        # server start, seeding, and browser launch.
        $shard.WallSeconds = [math]::Round(($shard.Process.ExitTime - $shard.Process.StartTime).TotalSeconds, 1)
        $status = if ($shard.ExitCode -eq 0) { "passed" } else { "FAILED" }
        Write-Host "Shard $($shard.Index)/$Shards $status in $($shard.WallSeconds)s (exit $($shard.ExitCode))"
    }
}
finally {
    if ($TelemetryProcess) {
        # Sentinel rather than a kill, so the sampler closes its writer and the
        # last records are not lost on a Ctrl+C.
        New-Item -ItemType File -Force -Path $TelemetryStop | Out-Null
        if (-not $TelemetryProcess.WaitForExit(15000)) {
            Stop-ProcessTree -ProcessId $TelemetryProcess.Id
        }
    }
    foreach ($shard in $Plan) {
        if ($null -ne $shard.Process -and -not $shard.Process.HasExited) {
            Write-Host "Cleaning up shard $($shard.Index) (pid $($shard.Process.Id))" -ForegroundColor Yellow
            Stop-ProcessTree -ProcessId $shard.Process.Id
        }
    }
    Remove-Item Env:PW_PORT, Env:PW_DB_PATH, Env:TEST_ARTIFACTS_DIR, `
        Env:PLAYWRIGHT_JSON_OUTPUT_NAME, Env:PW_WORKERS -ErrorAction SilentlyContinue
}

$OverallStopwatch.Stop()
$WallSeconds = [math]::Round($OverallStopwatch.Elapsed.TotalSeconds, 1)

# --------------------------------------------------------------------- summary

$manifest = [PSCustomObject]@{
    shards          = $Shards
    basePort        = $BasePort
    specCount       = $RequiredSpecs.Count
    wallSeconds     = $WallSeconds
    excludedSpecs   = $ExcludedSpecs
    results         = @($Plan | ForEach-Object {
        [PSCustomObject]@{
            index       = $_.Index
            port        = $_.Port
            exitCode    = $_.ExitCode
            wallSeconds = $_.WallSeconds
            jsonReport  = $_.JsonReport
        }
    })
}
$ManifestPath = Join-Path $OutputRoot "shards.json"
$manifest | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 $ManifestPath

Write-Host ""
$python = if ($env:OS -eq "Windows_NT") { ".venv\Scripts\python.exe" } else { ".venv/bin/python" }
if (Test-Path $python) {
    $summaryArgs = @((Join-Path $RepoRoot "scripts\playwright_shard_summary.py"), "--manifest", $ManifestPath)
    if ($BaselineReport) { $summaryArgs += @("--baseline", $BaselineReport) }
    & $python @summaryArgs
}
else {
    Write-Host "No .venv python found; raw manifest at $ManifestPath"
}

if (-not $KeepDatabases) {
    foreach ($shard in $Plan) {
        foreach ($suffix in @("", "-wal", "-shm", "-journal")) {
            Remove-Item -LiteralPath "$($shard.Database)$suffix" -Force -ErrorAction SilentlyContinue
        }
    }
}

$failed = @($Plan | Where-Object { $_.ExitCode -ne 0 })
if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "FAILED shards: $(($failed.Index) -join ', ')" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "All $Shards shard(s) passed in $WallSeconds s wall clock." -ForegroundColor Green
exit 0
