<# Create an isolated worktree after reconciled lifecycle/environment checks.
Incomplete creations retain their worktree and branch for explicit owner review.
Dot-source for injected acceptance; no CLI or environment fault switch.
#>
param(
    [string]$Task,[ValidateSet('visual','empty','copy-current')][string]$Seed='visual',
    [string]$BranchPrefix='wt/',[switch]$OpenTerminal,
    [string]$RepoRoot,[string]$DevelopmentParent,[string]$AnnotationPath,[string]$BaselinePath,
    [string]$Owner,[string]$NextReviewDate,[string]$TeardownCondition,[string]$ExpectedPr,
    [string]$PythonExecutable,[string]$SourceDatabase,[string]$PrMetadataPath
)
$creatorArguments=@{}+$PSBoundParameters
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'audit-worktrees.ps1')

function Write-WorktreeAnnotation {
    param([string]$Path,$Record,[scriptblock]$Boundary)
    $verified=Get-VerifiedWorktreePath $Path
    $parent=Split-Path -Parent $verified
    if(-not [IO.Directory]::Exists($parent)){throw 'Annotation parent must already exist'}
    $lock=$null
    $until=[DateTime]::UtcNow.AddSeconds(5)
    while($null -eq $lock) {
        $lockPath=Get-VerifiedWorktreePath ($verified+'.lock')
        try {$lock=[IO.File]::Open($lockPath,[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)}
        catch {if([DateTime]::UtcNow -ge $until){throw 'Annotation lock unavailable'};Start-Sleep -Milliseconds 50}
    }
    try {
        $current=Read-WorktreeAnnotations $verified
        $records=@($current.records | Where-Object {$_.identity -ne $Record.identity})+@($Record)
        $json=@{schemaVersion=1;records=$records}|ConvertTo-Json -Depth 16
        $block="``````json`n$json`n```````n"
        if($current.text){$updated=[regex]::Replace($current.text,'(?ms)^```json\s*\r?\n.*?^```\s*$', [Text.RegularExpressions.MatchEvaluator]{param($m) $block})}
        else{$updated="# Local worktree lifecycle annotations`n`n$block"}
        $temporary=Join-Path $parent ('.annotation-'+[guid]::NewGuid().ToString('N')+'.tmp')
        $bytes=[Text.UTF8Encoding]::new($false).GetBytes($updated)
        $stream=[IO.File]::Open($temporary,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
        try{$stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)}finally{$stream.Dispose()}
        if($Boundary){& $Boundary 'before_annotation_replace'}
        Get-VerifiedWorktreePath $verified | Out-Null
        if([IO.File]::Exists($verified)){[IO.File]::Replace($temporary,$verified,[NullString]::Value)}else{[IO.File]::Move($temporary,$verified)}
        if($Boundary){& $Boundary 'after_annotation_replace'}
    } finally {$lock.Dispose()}
}

function New-IsolatedWorktree {
    param(
        [Parameter(Mandatory=$true)][string]$Task,
        [ValidateSet('visual','empty','copy-current')][string]$Seed='visual',
        [string]$BranchPrefix='wt/',[switch]$OpenTerminal,
        [string]$RepoRoot=(Split-Path -Parent $PSScriptRoot),[string]$DevelopmentParent,
        [string]$AnnotationPath,[string]$BaselinePath,[string]$Owner,[string]$NextReviewDate,
        [string]$TeardownCondition,[string]$ExpectedPr,[string]$PythonExecutable,
        [string]$SourceDatabase,[string]$PrMetadataPath,[scriptblock]$Boundary
    )
    $repo=Get-VerifiedWorktreePath $RepoRoot
    if(-not $DevelopmentParent){$DevelopmentParent=Split-Path -Parent $repo}
    $parent=Get-VerifiedWorktreePath $DevelopmentParent
    if(-not $AnnotationPath){$AnnotationPath=Join-Path $repo 'docs\ai_workflow\WORKSTREAM_OWNERSHIP.local.md'}
    $annotationFile=Get-VerifiedWorktreePath $AnnotationPath
    if(-not $Owner -or -not $TeardownCondition -or -not $NextReviewDate){throw 'Owner, TeardownCondition and NextReviewDate are required'}
    $reviewDate=ConvertTo-WorktreeTimestamp $NextReviewDate
    if($reviewDate -le [DateTimeOffset]::UtcNow){throw 'NextReviewDate must be in the future'}
    $NextReviewDate=$reviewDate.ToString('o',[Globalization.CultureInfo]::InvariantCulture)
    if($Task -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]*$' -or $Task.Contains('..')){throw 'Use a nonempty simple task slug without traversal'}
    $target=Get-VerifiedWorktreePath (Join-Path $parent ((Split-Path -Leaf $repo)+'-'+$Task))
    $targetDb=Join-Path $target 'data\database.db'
    $branch=$BranchPrefix+$Task
    if(Test-Path -LiteralPath $target){throw "Worktree target already exists: $target"}
    $envReport=Test-WorktreeEnvironment -ApprovedRoot $parent -RuntimeRoot $target -DatabasePath $targetDb
    if(-not $envReport.ok){throw ($envReport.errors -join '; ')}
    $audit=Get-WorktreeAudit -RepoRoot $repo -DevelopmentParent $parent -AnnotationPath $annotationFile -BaselinePath $BaselinePath -PrMetadataPath $PrMetadataPath
    if(-not $audit.ok){throw ('Lifecycle preflight refused: '+($audit.errors -join '; '))}
    $main=@($audit.rows | Where-Object {$_.registered})[0].path
    if($annotationFile -ne (Join-Path $main 'docs\ai_workflow\WORKSTREAM_OWNERSHIP.local.md')){throw 'AnnotationPath must be the main checkout canonical local file'}
    Invoke-WorktreeGit $repo @('check-ref-format','--branch',$branch) | Out-Null
    $refs=Invoke-WorktreeGit $repo @('for-each-ref','--format=%(refname)','refs/heads/')
    if(($refs -split "`n") -contains ('refs/heads/'+$branch)){throw 'Branch already exists; choose a new task without retiring any ref'}
    if(Invoke-WorktreeGit $repo @('ls-tree','HEAD','--','data/database.db')){throw 'Tracked data/database.db collides with isolated seed; bytes/index unchanged'}
    $source=$null
    if($Seed -ne 'empty') {
        if(-not $PythonExecutable){$PythonExecutable=Join-Path $repo '.venv\Scripts\python.exe'}
        $PythonExecutable=Get-VerifiedWorktreePath $PythonExecutable
        if(-not [IO.File]::Exists($PythonExecutable)){throw 'Snapshot interpreter unavailable'}
        $helper=Join-Path $repo 'scripts\seed_worktree_snapshot.py'
        if(-not [IO.File]::Exists($helper)){throw 'Snapshot helper unavailable'}
        if($Seed -eq 'visual'){$source=Join-Path $repo 'e2e\fixtures\database.visual.seed.db'}
        elseif($SourceDatabase){$source=$SourceDatabase}
        elseif($env:DB_FILE){$source=$env:DB_FILE}
        elseif($env:HT_RUNTIME_DIR){$source=Join-Path $env:HT_RUNTIME_DIR 'data\database.db'}
        else{$source=Join-Path $repo 'data\database.db'}
        $source=Get-VerifiedWorktreePath $source
        $sourceIdentity=Get-WorktreePathIdentity $source
        Write-Host "Verified source database: $source ($sourceIdentity)"
    }
    $scratch=Join-Path $target 'artifacts\worktree'
    $launch=Join-Path $scratch 'launch-worktree.ps1'
    $hostExe=(Get-Process -Id $PID).Path
    $terminalArguments=@()
    $terminalExe=$null
    if($OpenTerminal){
        $terminalApplication=Get-Command wt.exe -CommandType Application -ErrorAction SilentlyContinue
        if(-not $terminalApplication){throw 'Windows Terminal unavailable; use manual launch without -OpenTerminal'}
        $terminalExe=$terminalApplication.Source
        try {
            $bootstrapHost=Join-Path ([Environment]::GetFolderPath('System')) 'WindowsPowerShell\v1.0\powershell.exe'
            if($bootstrapHost -notmatch '^[A-Za-z]:\\' -or $bootstrapHost -match '\s' -or -not [IO.File]::Exists($bootstrapHost)){
                throw 'An existing absolute system PowerShell path without whitespace is required'
            }
            $bootstrapHost=Get-VerifiedWorktreePath $bootstrapHost
        } catch {throw "Windows Terminal bootstrap unavailable; use manual launch without -OpenTerminal. $_"}
        # Keep both the caller executable and target path inside encoded payloads.
        # The system host invokes the exact caller host without module cmdlets.
        $terminalCommand=". '"+$launch.Replace("'","''")+"'"
        $terminalEncoded=[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($terminalCommand))
        $escapedHostExe=$hostExe.Replace("'","''")
        $bootstrapCommand=@"
`$ErrorActionPreference='Stop'
try {
    & '$escapedHostExe' -NoProfile -NoExit -EncodedCommand '$terminalEncoded'
    if(`$LASTEXITCODE -ne 0){throw "Caller PowerShell exited with code `$LASTEXITCODE"}
    exit 0
} catch {
    [Console]::Error.WriteLine([string]`$_)
    [Console]::WriteLine('Press Enter to close this bootstrap tab')
    [void][Console]::ReadLine()
    exit 1
}
"@
        $bootstrapEncoded=[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($bootstrapCommand))
        # Never leave the outer host at a prompt with inherited source settings.
        $terminalArguments=@('-w','0','nt',$bootstrapHost,'-NoProfile','-EncodedCommand',$bootstrapEncoded)
        # Native operands contain no whitespace; include executable quoting + NUL.
        if(($terminalExe.Length+3+($terminalArguments -join ' ').Length+1) -ge 32767){
            throw 'Windows Terminal command exceeds the Windows limit; use manual launch without -OpenTerminal'
        }
    }
    if($Boundary){& $Boundary 'before_git'}
    Invoke-WorktreeGit $repo @('worktree','add','-b',$branch,$target,'HEAD') | Out-Null
    try {
        if($Boundary){& $Boundary 'after_git'}
        Get-WorktreePathIdentity $target | Out-Null
        if(Test-Path -LiteralPath $targetDb){throw 'Actual target collision after Git creation; index/bytes unchanged'}
        if($Boundary){& $Boundary 'before_seed'}
        foreach($dir in @((Join-Path $target 'data\auto_backup'),(Join-Path $target 'logs'),(Join-Path $target 'artifacts\worktree\tmp'),(Join-Path $target 'artifacts\worktree\cache'),(Join-Path $target 'artifacts\worktree\bytecode'))) {
            Get-VerifiedWorktreePath $dir | Out-Null
            [IO.Directory]::CreateDirectory($dir) | Out-Null
        }
        if($Seed -ne 'empty') {
            & $PythonExecutable -I -S -B $helper --source $source --target $targetDb --timeout-seconds 30
            if($LASTEXITCODE -ne 0){throw "Snapshot helper failed ($LASTEXITCODE); registered target retained"}
        } elseif(Test-Path -LiteralPath $targetDb){throw 'Empty mode requires absent target database'}
        if($Boundary){& $Boundary 'after_seed'; & $Boundary 'before_runtime'}
        $environment=[ordered]@{
            HT_RUNTIME_DIR=$target;DB_FILE=$targetDb;TEMP=(Join-Path $scratch 'tmp');TMP=(Join-Path $scratch 'tmp');TMPDIR=(Join-Path $scratch 'tmp');
            XDG_CACHE_HOME=(Join-Path $scratch 'cache');PIP_CACHE_DIR=(Join-Path $scratch 'cache\pip');npm_config_cache=(Join-Path $scratch 'cache\npm');
            PLAYWRIGHT_BROWSERS_PATH=(Join-Path $scratch 'cache\browsers');HYPOTHESIS_STORAGE_DIRECTORY=(Join-Path $scratch 'cache\hypothesis');
            PYTHONPYCACHEPREFIX=(Join-Path $scratch 'bytecode');PYTHONDONTWRITEBYTECODE='1';PYTHONNOUSERSITE='1';
            TEST_ARTIFACTS_DIR=$scratch;PW_DB_PATH=(Join-Path $scratch 'e2e.db');PYTEST_ADDOPTS=('-o cache_dir='+((Join-Path $scratch 'cache\pytest') -replace '\\','/'))
        }
        $lines=@('# Process-only isolated session setup; dot-source before running app/tests.','$ErrorActionPreference = ''Stop''',
            '[Environment]::SetEnvironmentVariable(''PYTHONPATH'', $null, ''Process'')',
            '[Environment]::SetEnvironmentVariable(''PYTHONHOME'', $null, ''Process'')')
        foreach($pair in $environment.GetEnumerator()){$lines+=('$env:'+$pair.Key+" = '"+$pair.Value.Replace("'","''")+"'")}
        $lines+=("Set-Location -LiteralPath '"+$target.Replace("'","''")+"'")
        [IO.File]::WriteAllLines($launch,$lines,[Text.UTF8Encoding]::new($true))
        $verifyCommand=". '"+$launch.Replace("'","''")+"'; @{database=`$env:DB_FILE;runtime=`$env:HT_RUNTIME_DIR;logs=(Join-Path `$env:HT_RUNTIME_DIR 'logs')} | ConvertTo-Json -Compress"
        $encoded=[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($verifyCommand))
        $verification=& $hostExe -NoProfile -NonInteractive -OutputFormat Text -InputFormat Text -EncodedCommand $encoded
        if($LASTEXITCODE -ne 0){throw 'Target launch verification failed'}
        $resolved=$verification | ConvertFrom-Json
        if($resolved.database -ne $targetDb -or $resolved.runtime -ne $target -or $resolved.logs -ne (Join-Path $target 'logs')){throw 'Target launch resolves outside target runtime'}
        if(-not [IO.File]::Exists((Join-Path $target 'utils\config.py'))){throw 'Effective target application configuration missing'}
        if(-not $PythonExecutable){$PythonExecutable=Join-Path $repo '.venv\Scripts\python.exe'}
        $PythonExecutable=Get-VerifiedWorktreePath $PythonExecutable
        $interpreterIdentity=Get-WorktreePathIdentity $PythonExecutable
        $probePath=Join-Path $scratch 'verify-runtime.py'
        $probe=@'
import json, sys
from pathlib import Path
target = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(target))
import utils.config as c
print(json.dumps({"database": str(c.DB_FILE), "logs": str(c.LOGS_DIR),
                  "module": str(Path(c.__file__).resolve()), "executable": sys.executable}))
'@
        [IO.File]::WriteAllText($probePath,$probe,[Text.UTF8Encoding]::new($false))
        $command=". '"+$launch.Replace("'","''")+"'; & '"+$PythonExecutable.Replace("'","''")+"' -I -S -B '"+$probePath.Replace("'","''")+"'"
        $encoded=[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($command))
        $configResult=& $hostExe -NoProfile -NonInteractive -OutputFormat Text -InputFormat Text -EncodedCommand $encoded
        if($LASTEXITCODE -ne 0){throw 'Effective target application configuration unavailable'}
        $config=$configResult|ConvertFrom-Json
        if($config.database -ne $targetDb -or $config.logs -ne (Join-Path $target 'logs') -or
            $config.module -ne (Join-Path $target 'utils\config.py') -or $config.executable -ne $PythonExecutable -or
            (Get-WorktreePathIdentity $PythonExecutable) -ne $interpreterIdentity){throw 'Effective target DB/log/module/interpreter identity mismatch'}
        if($Boundary){& $Boundary 'after_runtime'; & $Boundary 'before_annotation'}
        $record=@{identity=(Get-WorktreePathIdentity $target);path=$target;owner=$Owner;task=$Task;branch=$branch;
            createdAt=[DateTimeOffset]::UtcNow.ToString('o');expectedPr=$ExpectedPr;teardownCondition=$TeardownCondition;
            nextReviewDate=$NextReviewDate;disposition='ACTIVE';rationale='Created with verified isolated runtime';
            activity='ACTIVE';activityObservedAt=[DateTimeOffset]::UtcNow.ToString('o')}
        Write-WorktreeAnnotation -Path $annotationFile -Record $record -Boundary $Boundary
        if($Boundary){& $Boundary 'after_annotation'}
        Write-Host "Worktree ready: $target"
        Write-Host "Branch: $branch; seed: $Seed"
        Write-Host "Dot-source the process-only HT_RUNTIME_DIR / DB_FILE launch setup:"
        Write-Host (". '"+$launch.Replace("'","''")+"'")
        Write-Host 'Provision a private .venv and private node_modules. Retain worktree and recovery roots.'
        if($OpenTerminal){
            & $terminalExe @terminalArguments | Out-Null
            if($LASTEXITCODE -ne 0){throw "Windows Terminal dispatch failed ($LASTEXITCODE)"}
        }
    } catch { throw "INCOMPLETE creation at $target; retain worktree, branch and owned scratch for owner review. $_" }
}

if($MyInvocation.InvocationName -ne '.') {
    try{New-IsolatedWorktree @creatorArguments}catch{[Console]::Error.WriteLine([string]$_);exit 1}
}
