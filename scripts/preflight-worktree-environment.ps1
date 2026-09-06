<# Read-only Operation A scope and path checks. Dot-source to inject read adapters. #>
param([string]$ApprovedRoot, [string]$RuntimeRoot, [string]$DatabasePath)
$ErrorActionPreference = 'Stop'

function Get-VerifiedWorktreePath {
    param([Parameter(Mandatory=$true)][string]$Path)
    if ($Path -notmatch '^[A-Za-z]:[\\/]' -or $Path.Substring(2).Contains(':') -or
        $Path -match '[*?\x00-\x1f]' -or $Path -match '[\\/](\.|\.\.)([\\/]|$)') {
        throw "Drive-qualified, unambiguous path required: $Path"
    }
    $full = [IO.Path]::GetFullPath($Path).TrimEnd('\')
    if ($full.Length -eq 2) { $full += '\' }
    foreach ($component in $full.Substring(3).Split('\')) {
        if ($component -match '[. ]$|~|^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)') {
            throw "Ambiguous path component: $component"
        }
    }
    $cursor = $full
    while ($cursor) {
        try {
            # Query the literal entry even when its reparse target is missing.
            $attributes = [IO.File]::GetAttributes($cursor)
            if ($attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse path: $cursor" }
        } catch {
            $cause=$_.Exception.GetBaseException()
            if($cause -isnot [IO.FileNotFoundException] -and $cause -isnot [IO.DirectoryNotFoundException]){throw}
            # A missing child does not establish that its ancestors are ordinary.
        }
        $parent = [IO.Path]::GetDirectoryName($cursor)
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
    return $full
}

function Test-WorktreeContainment {
    param([string]$Root,[string]$Path)
    return $Path.Equals($Root,[StringComparison]::OrdinalIgnoreCase) -or
        $Path.StartsWith($Root.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)
}

function Get-WorktreePathIdentity {
    param([Parameter(Mandatory=$true)][string]$Path)
    $verified = Get-VerifiedWorktreePath $Path
    if (-not (Test-Path -LiteralPath $verified)) { throw "Identity unavailable: $verified" }
    if (-not ('WorktreeIdentity' -as [type])) {
        Add-Type -TypeDefinition @'
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;
public static class WorktreeIdentity {
 [StructLayout(LayoutKind.Sequential)] public struct Info {
  public uint Attr, CreationLow, CreationHigh, AccessLow, AccessHigh, WriteLow, WriteHigh;
  public uint Volume, SizeHigh, SizeLow, Links, IndexHigh, IndexLow;
 }
 [DllImport("kernel32.dll", CharSet=CharSet.Unicode, SetLastError=true)]
 static extern SafeFileHandle CreateFile(string path,uint access,uint share,IntPtr security,uint mode,uint flags,IntPtr template);
 [DllImport("kernel32.dll", SetLastError=true)]
 static extern bool GetFileInformationByHandle(SafeFileHandle file,out Info info);
 public static string Read(string path) {
  using(var handle=CreateFile(path,0,7,IntPtr.Zero,3,0x02200000,IntPtr.Zero)) {
   if(handle.IsInvalid) throw new Win32Exception(Marshal.GetLastWin32Error());
   Info info; if(!GetFileInformationByHandle(handle,out info)) throw new Win32Exception(Marshal.GetLastWin32Error());
   if((info.Attr & 0x400)!=0) throw new InvalidOperationException("Reparse identity rejected");
   return info.Volume.ToString("X8")+":"+info.IndexHigh.ToString("X8")+info.IndexLow.ToString("X8");
  }
 }
}
'@
    }
    return [WorktreeIdentity]::Read($verified)
}

function Read-WorktreeEnvironmentScope {
    param([string]$Name,[string]$Scope)
    if ($Scope -eq 'Process') {
        $values = [Environment]::GetEnvironmentVariables('Process')
        return @{Present=$values.Contains($Name);Value=$values[$Name]}
    }
    $hive = if ($Scope -eq 'User') {[Microsoft.Win32.Registry]::CurrentUser} else {[Microsoft.Win32.Registry]::LocalMachine}
    $keyPath = if ($Scope -eq 'User') {'Environment'} else {'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'}
    $key = $hive.OpenSubKey($keyPath,$false)
    if ($null -eq $key) { throw "Cannot read $Scope environment registry scope" }
    try { return @{Present=($key.GetValueNames() -contains $Name);Value=$key.GetValue($Name,$null,[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)} }
    finally { $key.Dispose() }
}

function Test-WorktreeEnvironment {
    param([string]$ApprovedRoot,[string]$RuntimeRoot,[string]$DatabasePath,
          [scriptblock]$ScopeReader = ${function:Read-WorktreeEnvironmentScope})
    $issues = [Collections.Generic.List[string]]::new()
    $scopes = [Collections.Generic.List[object]]::new()
    foreach ($name in @('MSYS_NO_PATHCONV','MSYS2_ARG_CONV_EXCL')) {
        foreach ($scope in @('Process','User','Machine')) {
            try {
                $value = & $ScopeReader $name $scope
                if ($null -eq $value -or $value.Present -isnot [bool]) { throw 'Malformed scope result' }
                $scopes.Add(@{name=$name;scope=$scope;present=$value.Present;readable=$true})
                if ($value.Present) { $issues.Add("$name is present at $scope scope") }
            } catch {
                $scopes.Add(@{name=$name;scope=$scope;present=$null;readable=$false})
                $issues.Add("$name $scope scope unreadable: $_")
            }
        }
    }
    $paths = @{}
    try {
        $root = Get-VerifiedWorktreePath $ApprovedRoot
        if (-not [IO.Directory]::Exists($root)) { throw 'Approved root must exist' }
        $runtime = Get-VerifiedWorktreePath $RuntimeRoot
        $db = Get-VerifiedWorktreePath $DatabasePath
        if (-not (Test-WorktreeContainment $root $runtime) -or -not (Test-WorktreeContainment $runtime $db)) {
            throw 'Runtime and database must remain within approved root/runtime'
        }
        $paths = @{approvedRoot=$root;rootIdentity=(Get-WorktreePathIdentity $root);runtime=$runtime;database=$db;logs=(Join-Path $runtime 'logs')}
    } catch { $issues.Add([string]$_) }
    return @{ok=($issues.Count -eq 0);errors=@($issues.ToArray());paths=$paths;scopes=@($scopes.ToArray())}
}

if ($MyInvocation.InvocationName -ne '.') {
    try {
        $result = Test-WorktreeEnvironment -ApprovedRoot $ApprovedRoot -RuntimeRoot $RuntimeRoot -DatabasePath $DatabasePath
        $result | ConvertTo-Json -Depth 12
        if (-not $result.ok) { exit 1 }
    } catch { @{ok=$false;errors=@([string]$_)} | ConvertTo-Json; exit 1 }
}
