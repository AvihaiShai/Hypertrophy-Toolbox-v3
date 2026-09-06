param([string] $GuardPath = (Join-Path $PSScriptRoot '..\..\.claude\hooks\guard-destructive-command.ps1'))
$ErrorActionPreference = 'Stop'
$failures = 0
$count = 0
$bytes = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $GuardPath))
if ($bytes.Length -lt 3 -or $bytes[0] -ne 239 -or $bytes[1] -ne 187 -or $bytes[2] -ne 191) { throw 'Guard missing UTF-8 BOM' }
foreach ($b in $bytes[3..($bytes.Length-1)]) { if ($b -gt 127) { throw 'Guard is not ASCII after BOM' } }
$cases = @(
    @{command='MSYS_NO_PATHCONV=1 npx inert --output /c/incident';exit=2},
    @{command='export MSYS2_ARG_CONV_EXCL=0';exit=2},
    @{command='env MSYS_NO_PATHCONV=0 echo inert';exit=2},
    @{command='cmd /c "set MSYS_NO_PATHCONV=0 && echo inert"';exit=2},
    @{command='$env:MSYS2_ARG_CONV_EXCL = "0"';exit=2},
    @{command='[Environment]::SetEnvironmentVariable("MSYS_NO_PATHCONV","0","User")';exit=2},
    @{command='setx MSYS2_ARG_CONV_EXCL 0';exit=2},
    @{command='git status; export MSYS_NO_PATHCONV=0';exit=2},
    @{command='bash -c "export MSYS2_ARG_CONV_EXCL=0; echo inert"';exit=2},
    @{command='cmd /c "set /a MSYS_NO_PATHCONV=1"';exit=2},
    @{command='Set-Item -Path Env:\MSYS2_ARG_CONV_EXCL -Value 1';exit=2},
    @{command='export -n MSYS_NO_PATHCONV=1';exit=2},
    @{command='echo "$(export MSYS2_ARG_CONV_EXCL=1)"';exit=2},
    @{command='$env:MSYS_NO_PATHCONV += "1"';exit=2},
    @{command='cmd /c "set /a MSYS2_ARG_CONV_EXCL+=1"';exit=2},
    @{command='cmd /c "set /a MSYS_NO_PATHCONV += 1"';exit=2},
    @{command='cmd /c "set /a harmless=0,MSYS2_ARG_CONV_EXCL=1"';exit=2},
    @{command='git status --short';exit=0},
    @{command='npx playwright test --output D:\scratch\results';exit=0},
    @{command='git ls-tree -z HEAD -- scripts/new-worktree.ps1';exit=0},
    @{command=('git cat-file blob ' + ('a' * 40));exit=0}
)
foreach ($hostName in @('powershell','pwsh')) {
    $hostCommand = Get-Command $hostName -ErrorAction SilentlyContinue
    if (-not $hostCommand) { Write-Output "UNAVAILABLE host=$hostName"; continue }
    $version = & $hostCommand.Source -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'
    foreach ($profile in @('main','agent')) {
        foreach ($mode in @('default','auto','bypassPermissions')) {
            foreach ($case in $cases) {
                # Serialize only: the historical child payload is NEVER executed.
                $payload = @{permission_mode=$mode;tool_input=@{command=$case.command}} | ConvertTo-Json -Compress
                $start = New-Object Diagnostics.ProcessStartInfo
                $start.FileName = $hostCommand.Source
                $start.Arguments = '-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' + $GuardPath + '" -GuardProfile ' + $profile
                $start.UseShellExecute = $false
                $start.CreateNoWindow = $true
                $start.RedirectStandardInput = $true
                $start.RedirectStandardOutput = $true
                $start.RedirectStandardError = $true
                $child = New-Object Diagnostics.Process
                $child.StartInfo = $start
                [void]$child.Start()
                $child.StandardInput.Write($payload)
                $child.StandardInput.Close()
                $stdout = $child.StandardOutput.ReadToEnd()
                $stderr = $child.StandardError.ReadToEnd()
                $child.WaitForExit()
                $count++
                if ($child.ExitCode -ne $case.exit) {
                    $failures++
                    Write-Output "FAIL host=$hostName version=$version profile=$profile mode=$mode exit=$($child.ExitCode) expected=$($case.exit) payload=$($case.command) stderr=$stderr"
                }
                $child.Dispose()
            }
            Write-Output "CHECKED host=$hostName version=$version profile=$profile permission=$mode"
        }
    }
}
Write-Output "Standalone guard cases=$count failures=$failures; no pytest/conftest/application imports; payloads serialized only."
if ($count -eq 0 -or $failures -gt 0) { exit 1 }
exit 0
