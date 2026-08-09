<#
.SYNOPSIS
    Block until the machine is in a recorded clean state, then snapshot it.

.DESCRIPTION
    The first N=1/2/3/4 matrix ran back-to-back and was invalidated by it: TCP
    TIME_WAIT entries live for two minutes, so each configuration inherited the
    previous one's draining state and shard count could not be separated from
    run order. N=3 came out slower than N=2, which no clean model predicts.

    A fixed sleep does not fix that, because the thing being waited on is
    observable and variable. This waits on the observation and records what it
    saw, so a later run can be compared against a known starting condition
    instead of an assumed one.

    Conditions, all of which must hold simultaneously:

      * no leftover processes from a previous launcher (matched by command line,
        with this script's own ancestry excluded -- never by executable name);
      * every candidate port unbound, proven by binding it;
      * TIME_WAIT entries involving the candidate ports at or below a threshold;
      * a minimum elapsed time, as a floor rather than as the mechanism.

.PARAMETER Match
    Command-line substring identifying a previous run's processes, e.g. the
    worktree path.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string] $Match,
    [string] $Ports = "",
    # A command line under the worktree is not evidence of a running test -- any
    # shell that cd'd there matches, including the one running this script's
    # siblings. A leftover must also look like part of a run. These tokens are
    # command-line arguments, not executable names; nothing is ever classified
    # or terminated by its image name.
    [string] $RunMarker = '--shard=|app\.py|prepare_e2e_db|prepare_visual_db',
    [int] $MinWaitSeconds = 120,
    [int] $MaxWaitSeconds = 900,
    [int] $TimeWaitThreshold = 50,
    [string] $SnapshotOut,
    [int] $PollSeconds = 5
)

$ErrorActionPreference = "Stop"

$PortList = @()
if ($Ports) { $PortList = $Ports -split ',' | ForEach-Object { [int]$_.Trim() } }

function Get-AncestorIds {
    <#
        This script's own chain (bash -> powershell -> ...) legitimately carries
        the worktree path on its command line and must not be mistaken for a
        leftover shard.
    #>
    $all = Get-CimInstance Win32_Process -Property ProcessId, ParentProcessId
    $parentOf = @{}
    foreach ($p in $all) { $parentOf[$p.ProcessId] = $p.ParentProcessId }
    $chain = [System.Collections.Generic.List[int]]::new()
    $current = $PID
    while ($current -and -not $chain.Contains($current)) {
        $chain.Add($current)
        $current = if ($parentOf.ContainsKey($current)) { $parentOf[$current] } else { 0 }
    }
    return $chain
}

function Get-Leftovers {
    param([int[]] $Exclude)

    Get-CimInstance Win32_Process -Property ProcessId, ParentProcessId, Name, CommandLine |
        Where-Object {
            $_.CommandLine -and
            $_.CommandLine -like "*$Match*" -and
            $_.CommandLine -match $RunMarker -and
            $Exclude -notcontains $_.ProcessId
        }
}

function Test-PortFree {
    param([int] $Port)
    $listener = $null
    try {
        $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        return $true
    }
    catch { return $false }
    finally { if ($null -ne $listener) { $listener.Stop() } }
}

function Get-TcpFacts {
    $conns = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpConnections()
    $timeWaitTotal = 0
    $timeWaitOnPorts = 0
    $dynamic = [System.Collections.Generic.HashSet[int]]::new()
    foreach ($c in $conns) {
        $isTimeWait = $c.State -eq [System.Net.NetworkInformation.TcpState]::TimeWait
        if ($isTimeWait) { $timeWaitTotal++ }
        $lp = $c.LocalEndPoint.Port
        $rp = $c.RemoteEndPoint.Port
        if ($lp -ge 49152) { $null = $dynamic.Add($lp) }
        if ($isTimeWait -and ($PortList -contains $lp -or $PortList -contains $rp)) { $timeWaitOnPorts++ }
    }
    return [PSCustomObject]@{
        Total             = $conns.Count
        TimeWaitTotal     = $timeWaitTotal
        TimeWaitOnPorts   = $timeWaitOnPorts
        DynamicLocalPorts = $dynamic.Count
    }
}

$ancestors = Get-AncestorIds
$started = Get-Date
$attempt = 0

while ($true) {
    $attempt++
    $elapsed = ((Get-Date) - $started).TotalSeconds
    $leftovers = @(Get-Leftovers -Exclude $ancestors)
    $busy = @($PortList | Where-Object { -not (Test-PortFree -Port $_) })
    $tcp = Get-TcpFacts

    $clean = ($leftovers.Count -eq 0) -and ($busy.Count -eq 0) -and
             ($tcp.TimeWaitOnPorts -le $TimeWaitThreshold) -and ($elapsed -ge $MinWaitSeconds)

    Write-Host ("[{0,4:N0}s] leftovers={1} busyPorts={2} timeWaitOnPorts={3} timeWaitTotal={4} dynPorts={5}{6}" -f `
        $elapsed, $leftovers.Count, $busy.Count, $tcp.TimeWaitOnPorts, $tcp.TimeWaitTotal, $tcp.DynamicLocalPorts,
        $(if ($clean) { "  -> CLEAN" } else { "" }))

    if ($clean) { break }

    if ($elapsed -gt $MaxWaitSeconds) {
        Write-Host "Did not reach a clean state within $MaxWaitSeconds s." -ForegroundColor Red
        if ($leftovers.Count -gt 0) {
            Write-Host "Leftover processes (NOT terminated -- inspect them yourself):" -ForegroundColor Yellow
            foreach ($p in $leftovers) { Write-Host "  pid=$($p.ProcessId) $($p.Name)" }
        }
        exit 3
    }

    Start-Sleep -Seconds $PollSeconds
}

$snapshot = [ordered]@{
    startedAt         = (Get-Date).ToUniversalTime().ToString("o")
    waitedSeconds     = [math]::Round(((Get-Date) - $started).TotalSeconds, 1)
    ports             = $PortList
    timeWaitTotal     = $tcp.TimeWaitTotal
    timeWaitOnPorts   = $tcp.TimeWaitOnPorts
    dynamicLocalPorts = $tcp.DynamicLocalPorts
    tcpTotal          = $tcp.Total
    leftoverProcesses = 0
}

Write-Host ""
Write-Host "CLEAN START at $($snapshot.startedAt) after $($snapshot.waitedSeconds)s"
Write-Host "  TIME_WAIT total=$($tcp.TimeWaitTotal) onPorts=$($tcp.TimeWaitOnPorts) dynamicLocalPorts=$($tcp.DynamicLocalPorts)"

if ($SnapshotOut) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $SnapshotOut) | Out-Null
    $snapshot | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 $SnapshotOut
    Write-Host "  snapshot -> $SnapshotOut"
}

exit 0
