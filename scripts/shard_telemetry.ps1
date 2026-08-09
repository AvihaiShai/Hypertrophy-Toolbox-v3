<#
.SYNOPSIS
    Sample system and TCP state during a shard run and write it as JSONL.

.DESCRIPTION
    Diagnostic instrument for the parallel-only failures the shard launcher hits
    at N>1. It exists to decide between competing hypotheses -- network, CPU,
    disk, memory -- rather than to confirm any one of them, so it records all
    four and lets the analysis choose.

    Cost was measured before the sampling rate was chosen, because a probe that
    perturbs the run it measures is worse than no probe:

        cached PerformanceCounter read   1-6ms   (288ms once, to construct)
        GetActiveTcpConnections          ~18ms
        Get-Process (all)                ~50ms
        Win32_Process tree rebuild       ~130ms  (every RediscoverEvery samples)

    That is roughly 70ms per sample at a 3s interval on a 32-processor machine.

    The TCP primitive was cross-checked against `netstat` before being trusted:
    both reported the same TIME_WAIT count, which matters because the whole
    ERR_ADDRESS_IN_USE hypothesis rests on this number being real.

    Process data is scoped to descendants of -RootPid. Nothing here classifies a
    process by its executable name, and nothing here terminates anything.

.PARAMETER RootPid
    The launcher process. Its descendant tree is what gets attributed.

.PARAMETER ShardPorts
    Comma-separated Flask listening ports, so connections can be attributed to
    the shard that owns them.

.PARAMETER StopFile
    Sampling ends when this path appears, or when RootPid exits.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][int] $RootPid,
    [string] $ShardPorts = "",
    [Parameter(Mandatory = $true)][string] $OutFile,
    [double] $IntervalSeconds = 3,
    [string] $StopFile,
    [int] $MaxMinutes = 120,
    [int] $RediscoverEvery = 5
)

$ErrorActionPreference = "Stop"

$Ports = @()
if ($ShardPorts) { $Ports = $ShardPorts -split ',' | ForEach-Object { [int]$_.Trim() } }

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutFile) | Out-Null
$writer = [System.IO.StreamWriter]::new($OutFile, $false)
$writer.AutoFlush = $true

$defs = @(
    @{ key = 'cpuPct';       cat = 'Processor';    ctr = '% Processor Time';          inst = '_Total' },
    @{ key = 'procQueue';    cat = 'System';       ctr = 'Processor Queue Length';    inst = $null },
    @{ key = 'availMB';      cat = 'Memory';       ctr = 'Available MBytes';          inst = $null },
    @{ key = 'committedPct'; cat = 'Memory';       ctr = '% Committed Bytes In Use';  inst = $null },
    @{ key = 'diskPct';      cat = 'PhysicalDisk'; ctr = '% Disk Time';               inst = '_Total' },
    @{ key = 'diskQueue';    cat = 'PhysicalDisk'; ctr = 'Current Disk Queue Length'; inst = '_Total' },
    @{ key = 'diskSecXfer';  cat = 'PhysicalDisk'; ctr = 'Avg. Disk sec/Transfer';    inst = '_Total' }
)

$counters = @{}
foreach ($d in $defs) {
    try {
        $counters[$d.key] = if ($d.inst) {
            New-Object System.Diagnostics.PerformanceCounter($d.cat, $d.ctr, $d.inst)
        }
        else {
            New-Object System.Diagnostics.PerformanceCounter($d.cat, $d.ctr)
        }
        # Rate counters return 0 on their first read; prime them now so the
        # first recorded sample is a real value rather than a structural zero.
        $null = $counters[$d.key].NextValue()
    }
    catch {
        $counters[$d.key] = $null
    }
}

function Get-DescendantIds {
    param([int] $Root)

    $all = Get-CimInstance Win32_Process -Property ProcessId, ParentProcessId
    $childrenOf = @{}
    foreach ($p in $all) {
        if (-not $childrenOf.ContainsKey($p.ParentProcessId)) { $childrenOf[$p.ParentProcessId] = @() }
        $childrenOf[$p.ParentProcessId] += $p.ProcessId
    }
    $result = [System.Collections.Generic.List[int]]::new()
    $queue = [System.Collections.Generic.Queue[int]]::new()
    $queue.Enqueue($Root)
    while ($queue.Count -gt 0) {
        $current = $queue.Dequeue()
        if ($result.Contains($current)) { continue }
        $result.Add($current)
        if ($childrenOf.ContainsKey($current)) {
            foreach ($child in $childrenOf[$current]) { $queue.Enqueue($child) }
        }
    }
    return $result
}

$tracked = Get-DescendantIds -Root $RootPid
$startedAt = Get-Date
$sample = 0
$previousCpu = @{}

while ($true) {
    $sample++
    if ($StopFile -and (Test-Path $StopFile)) { break }
    if (((Get-Date) - $startedAt).TotalMinutes -gt $MaxMinutes) { break }
    if (-not (Get-Process -Id $RootPid -ErrorAction SilentlyContinue)) { break }

    if ($sample % $RediscoverEvery -eq 1) {
        try { $tracked = Get-DescendantIds -Root $RootPid } catch { }
    }

    $now = Get-Date

    # --- network -----------------------------------------------------------
    $conns = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpConnections()
    $states = @{}
    $dynamicLocal = [System.Collections.Generic.HashSet[int]]::new()
    $toShard = @{}
    $fromShard = @{}
    foreach ($port in $Ports) { $toShard["$port"] = 0; $fromShard["$port"] = 0 }

    foreach ($c in $conns) {
        $state = $c.State.ToString()
        if ($states.ContainsKey($state)) { $states[$state]++ } else { $states[$state] = 1 }
        $lp = $c.LocalEndPoint.Port
        if ($lp -ge 49152) { $null = $dynamicLocal.Add($lp) }
        $rp = $c.RemoteEndPoint.Port
        if ($Ports -contains $rp) { $toShard["$rp"]++ }
        if ($Ports -contains $lp) { $fromShard["$lp"]++ }
    }

    # --- system ------------------------------------------------------------
    $sys = @{}
    foreach ($key in $counters.Keys) {
        $sys[$key] = if ($counters[$key]) { [math]::Round($counters[$key].NextValue(), 3) } else { $null }
    }

    # --- tracked processes -------------------------------------------------
    $live = Get-Process -Id $tracked -ErrorAction SilentlyContinue
    $cpuTotal = 0.0
    $handles = 0
    $wsMB = 0.0
    $cpuDelta = 0.0
    foreach ($p in $live) {
        try {
            $cpuSeconds = $p.TotalProcessorTime.TotalSeconds
            $cpuTotal += $cpuSeconds
            $handles += $p.HandleCount
            $wsMB += $p.WorkingSet64 / 1MB
            if ($previousCpu.ContainsKey($p.Id)) { $cpuDelta += ($cpuSeconds - $previousCpu[$p.Id]) }
            $previousCpu[$p.Id] = $cpuSeconds
        }
        catch { }
    }

    $record = [ordered]@{
        ts             = $now.ToUniversalTime().ToString("o")
        elapsedSec     = [math]::Round(($now - $startedAt).TotalSeconds, 1)
        sample         = $sample
        tcpTotal       = $conns.Count
        tcpStates      = $states
        timeWait       = if ($states.ContainsKey('TimeWait')) { $states['TimeWait'] } else { 0 }
        dynamicLocalPorts = $dynamicLocal.Count
        connToShard    = $toShard
        connFromShard  = $fromShard
        sys            = $sys
        trackedProcs   = @($live).Count
        trackedHandles = $handles
        trackedWorkingSetMB = [math]::Round($wsMB, 1)
        trackedCpuSeconds   = [math]::Round($cpuTotal, 2)
        # Share of ONE processor consumed by the tracked tree since the previous
        # sample. Divide by processor count for a whole-machine figure.
        trackedCpuPctOfOne  = [math]::Round(100 * $cpuDelta / $IntervalSeconds, 1)
    }

    $writer.WriteLine(($record | ConvertTo-Json -Depth 5 -Compress))
    Start-Sleep -Seconds $IntervalSeconds
}

$writer.Close()
