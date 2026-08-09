param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]] $PlaywrightArgs
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

# Specs that need the plan-bearing visual seed rather than the user-state-wiped
# functional seed. playwright.config.ts picks the seeder from PW_VISUAL_SEED and
# seeds the throwaway DB inside the webServer command, before Flask opens it.
#
# This list is a routing contract, asserted by
# tests/test_playwright_runner_contracts.py. Two traps it exists to prevent:
#
# * `visual-field-separator.spec.ts` is NOT here despite the prefix. It reads
#   composited computed styles and asserts a contrast ratio -- no screenshot, no
#   baseline -- and it injects its own rows, so it needs the functional seed and
#   runs on the required PR path. The prefix describes what it measures, not how.
# * `workout-plan-desktop-contract.spec.ts` IS here despite not being a snapshot
#   spec. It carries the coverage of the five byte-gate-exempt captures as
#   computed style / geometry / DOM structure, over the plan rows only the visual
#   seed provides.
$VisualSeedSpecs = @(
    "e2e/visual.spec.ts",
    "e2e/visual-baseline-thumbnails.spec.ts",
    "e2e/workout-plan-desktop-contract.spec.ts"
)

$ArtifactsRoot = if ($env:TEST_ARTIFACTS_DIR) { $env:TEST_ARTIFACTS_DIR } else { Join-Path $RepoRoot "artifacts" }
if (-not [System.IO.Path]::IsPathRooted($ArtifactsRoot)) {
    $ArtifactsRoot = Join-Path $RepoRoot $ArtifactsRoot
}

$LogsDir = Join-Path $ArtifactsRoot "playwright\logs"
New-Item -ItemType Directory -Force -Path $LogsDir | Out-Null

$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$LogFile = Join-Path $LogsDir "playwright-$Timestamp.txt"

$Npx = if ($env:OS -eq "Windows_NT") { "npx.cmd" } else { "npx" }

Write-Host "Writing Playwright log to $LogFile"

function Invoke-PlaywrightRun {
    param(
        [string[]] $PlaywrightRunArgs,
        [string] $Label
    )

    $SafeLabel = $Label -replace '[^A-Za-z0-9_-]', '-'
    $StdoutFile = Join-Path $LogsDir "playwright-$Timestamp.$SafeLabel.stdout.tmp"
    $StderrFile = Join-Path $LogsDir "playwright-$Timestamp.$SafeLabel.stderr.tmp"

    Write-Host "Running Playwright $Label"
    $ArgumentList = @("playwright", "test") + $PlaywrightRunArgs
    $ArgumentString = ($ArgumentList | ForEach-Object {
        if ($_ -match '\s') {
            '"' + ($_ -replace '"', '\"') + '"'
        }
        else {
            $_
        }
    }) -join ' '
    $Process = Start-Process `
        -FilePath $Npx `
        -ArgumentList $ArgumentString `
        -NoNewWindow `
        -Wait `
        -PassThru `
        -RedirectStandardOutput $StdoutFile `
        -RedirectStandardError $StderrFile
    $ExitCode = $Process.ExitCode

    if (Test-Path $StdoutFile) {
        Get-Content -Encoding UTF8 $StdoutFile |
            Tee-Object -FilePath $LogFile -Append |
            ForEach-Object { Write-Host $_ }
    }
    if (Test-Path $StderrFile) {
        Get-Content -Encoding UTF8 $StderrFile |
            Tee-Object -FilePath $LogFile -Append |
            ForEach-Object { Write-Host $_ }
    }

    Remove-Item -LiteralPath $StdoutFile, $StderrFile -Force -ErrorAction SilentlyContinue
    return $ExitCode
}

function Invoke-VisualSeedRun {
    <#
        Run with PW_VISUAL_SEED=1, restoring whatever the caller had -- including
        the case where they had it unset, which must go back to unset rather than
        to an empty string that PW_VISUAL_SEED -eq '1' would read as absent but
        that would still show up in the child environment.
    #>
    param(
        [string[]] $PlaywrightRunArgs,
        [string] $Label
    )

    $HadVisualSeed = Test-Path Env:PW_VISUAL_SEED
    $PreviousVisualSeed = if ($HadVisualSeed) { $env:PW_VISUAL_SEED } else { $null }
    $env:PW_VISUAL_SEED = "1"
    try {
        return Invoke-PlaywrightRun -PlaywrightRunArgs $PlaywrightRunArgs -Label $Label
    }
    finally {
        if ($HadVisualSeed) {
            $env:PW_VISUAL_SEED = $PreviousVisualSeed
        }
        else {
            Remove-Item Env:PW_VISUAL_SEED -ErrorAction SilentlyContinue
        }
    }
}

function Get-SpecGroup {
    <#
        Partition caller arguments into visual-seed specs, functional specs, and
        everything else (flags such as --grep or --project, which must reach both
        runs unchanged).
    #>
    param([string[]] $Arguments)

    $Visual = @()
    $Functional = @()
    $Other = @()

    foreach ($Argument in $Arguments) {
        $Normalized = $Argument -replace '\\', '/'
        if ($Normalized -match '\.spec\.ts$') {
            $Leaf = "e2e/" + [System.IO.Path]::GetFileName($Normalized)
            if ($VisualSeedSpecs -contains $Leaf) {
                $Visual += $Argument
            }
            else {
                $Functional += $Argument
            }
        }
        else {
            $Other += $Argument
        }
    }

    return [PSCustomObject]@{
        Visual     = $Visual
        Functional = $Functional
        Other      = $Other
    }
}

$ExitCode = 0
$RunDefaultSuite = -not $PlaywrightArgs -or $PlaywrightArgs.Count -eq 0

if ($RunDefaultSuite) {
    $FunctionalSpecs = Get-ChildItem (Join-Path $RepoRoot "e2e") -Filter "*.spec.ts" |
        ForEach-Object { "e2e/$($_.Name)" } |
        Where-Object { $VisualSeedSpecs -notcontains $_ }

    $ExitCode = Invoke-PlaywrightRun `
        -PlaywrightRunArgs (@($FunctionalSpecs) + @("--project=chromium")) `
        -Label "functional-seed suite"

    if ($ExitCode -eq 0) {
        $ExitCode = Invoke-VisualSeedRun `
            -PlaywrightRunArgs (@($VisualSeedSpecs) + @("--project=chromium")) `
            -Label "visual-seed suite"
    }
}
else {
    $Group = Get-SpecGroup -Arguments $PlaywrightArgs

    if ($Group.Visual.Count -gt 0 -and $Group.Functional.Count -gt 0) {
        # One webServer start seeds one way, so a mixed request cannot be served
        # by a single run. Split it rather than silently seeding half of it wrong.
        Write-Host "Mixed request: splitting into functional-seed and visual-seed runs."
        $ExitCode = Invoke-PlaywrightRun `
            -PlaywrightRunArgs (@($Group.Functional) + @($Group.Other)) `
            -Label "requested functional-seed specs"
        if ($ExitCode -eq 0) {
            $ExitCode = Invoke-VisualSeedRun `
                -PlaywrightRunArgs (@($Group.Visual) + @($Group.Other)) `
                -Label "requested visual-seed specs"
        }
    }
    elseif ($Group.Visual.Count -gt 0) {
        $ExitCode = Invoke-VisualSeedRun -PlaywrightRunArgs $PlaywrightArgs -Label "requested visual-seed specs"
    }
    else {
        $ExitCode = Invoke-PlaywrightRun -PlaywrightRunArgs $PlaywrightArgs -Label "requested suite"
    }
}

exit $ExitCode
