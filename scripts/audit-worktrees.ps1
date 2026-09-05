<# Read-only lifecycle projection. No removal, ref retirement or annotation writes. #>
param([string]$RepoRoot,[string]$DevelopmentParent,[string]$AnnotationPath,[string]$BaselinePath,[string]$PrMetadataPath)
$auditArguments=@{}+$PSBoundParameters
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'preflight-worktree-environment.ps1')

function ConvertFrom-WorktreeJson {
    param([string]$Text)
    if((Get-Command ConvertFrom-Json).Parameters.ContainsKey('DateKind')) { return ConvertFrom-Json -InputObject $Text -DateKind String }
    return ConvertFrom-Json -InputObject $Text
}

function ConvertTo-WorktreeTimestamp {
    param($Value)
    if($Value -is [DateTimeOffset]){return $Value}
    if($Value -is [DateTime]){return [DateTimeOffset]$Value}
    if([string]$Value -notmatch '^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$'){throw 'An ISO-8601 timestamp with timezone is required'}
    return [DateTimeOffset]::Parse([string]$Value,[Globalization.CultureInfo]::InvariantCulture)
}

function Invoke-WorktreeGit {
    param([string]$Root,[string[]]$Arguments)
    Assert-WorktreeGitEnvironment
    Assert-WorktreeMetadataPaths $Root
    $git = (Get-Command git.exe -ErrorAction Stop).Source
    $previous=$ErrorActionPreference
    try {
        # Windows PowerShell wraps ordinary native stderr as ErrorRecords. Classify
        # the native exit code, never mistake Git's progress line for a failure.
        $ErrorActionPreference='Continue'
        $output = & $git --no-optional-locks -c gc.auto=0 -c maintenance.auto=false -c core.fsmonitor=false -C $Root @Arguments 2>&1
        $code=$LASTEXITCODE
    } finally {$ErrorActionPreference=$previous}
    if ($code -ne 0) { throw "Git failed ($code): $output" }
    return ($output -join "`n")
}

function Assert-WorktreeMetadataPaths {
    param([string]$Root)
    # Inspect literal entries before Git can follow .git or a linked pointer.
    $rootPath=Get-VerifiedWorktreePath $Root
    $dotGit=Get-VerifiedWorktreePath (Join-Path $rootPath '.git')
    if([IO.Directory]::Exists($dotGit)) {$admin=$dotGit;$common=$dotGit}
    elseif([IO.File]::Exists($dotGit)) {
        $pointer=[IO.File]::ReadAllText($dotGit).TrimEnd("`r","`n")
        if($pointer -notmatch '^gitdir: (.+)$'){throw 'Malformed worktree .git pointer'}
        $admin=$Matches[1]
        if(-not [IO.Path]::IsPathRooted($admin)){$admin=Join-Path $rootPath $admin}
        $admin=Get-VerifiedWorktreePath ([IO.Path]::GetFullPath($admin))
        $commonFile=Get-VerifiedWorktreePath (Join-Path $admin 'commondir')
        $backlink=Get-VerifiedWorktreePath (Join-Path $admin 'gitdir')
        if(-not [IO.File]::Exists($backlink)){throw 'Linked admin gitdir backlink missing'}
        $common=[IO.File]::ReadAllText($commonFile).TrimEnd("`r","`n")
        if(-not [IO.Path]::IsPathRooted($common)){$common=Join-Path $admin $common}
        $common=Get-VerifiedWorktreePath ([IO.Path]::GetFullPath($common))
    } else {throw 'Checkout .git metadata missing'}
    if(-not [IO.Directory]::Exists($admin) -or -not [IO.Directory]::Exists($common)){throw 'Git admin/common directory missing'}
    foreach($entry in @((Join-Path $admin 'HEAD'),(Join-Path $admin 'config.worktree'),(Join-Path $common 'config'))) {
        Get-VerifiedWorktreePath $entry | Out-Null
    }
}

function Assert-WorktreeGitEnvironment {
    $values=[Environment]::GetEnvironmentVariables('Process')
    $allowed=@{}
    if($values.Contains('GIT_OPTIONAL_LOCKS') -and $values['GIT_OPTIONAL_LOCKS'] -eq '0'){$allowed['GIT_OPTIONAL_LOCKS']=$true}
    if($values.Contains('GIT_CONFIG_COUNT')) {
        $allowed['GIT_CONFIG_COUNT']=$true
        $count=0
        if(-not [int]::TryParse([string]$values['GIT_CONFIG_COUNT'],[ref]$count) -or $count -lt 0 -or $count -gt 2){throw 'Unverified GIT_CONFIG_COUNT'}
        for($i=0;$i -lt $count;$i++) {
            $key=[string]$values["GIT_CONFIG_KEY_$i"];$value=[string]$values["GIT_CONFIG_VALUE_$i"]
            if(-not (($key -eq 'gc.auto' -and $value -eq '0') -or ($key -eq 'maintenance.auto' -and $value -eq 'false'))){throw 'Inherited Git config override is not permitted'}
            $allowed["GIT_CONFIG_KEY_$i"]=$true;$allowed["GIT_CONFIG_VALUE_$i"]=$true
        }
    }
    foreach($name in $values.Keys) {
        if([string]$name -like 'GIT_*' -and -not $allowed.ContainsKey([string]$name)){throw "Unverified inherited Git environment setting: $name"}
    }
}

function Assert-WorktreeAdminRelationship {
    param([string]$Path,[string]$Admin,[string]$Common,$Entry)
    $dotGit=Get-VerifiedWorktreePath (Join-Path $Path '.git')
    $dotGitItem=Get-Item -Force -LiteralPath $dotGit
    if($Admin -eq $Common) {
        if(-not $dotGitItem.PSIsContainer -or (Get-WorktreePathIdentity $dotGit) -ne (Get-WorktreePathIdentity $Common)) {
            throw 'Main checkout .git/common directory identity mismatch'
        }
    } else {
        if($dotGitItem.PSIsContainer -or (Split-Path -Parent $Admin) -ne (Join-Path $Common 'worktrees')) {throw 'Linked checkout admin topology mismatch'}
        $pointer=[IO.File]::ReadAllText($dotGit).TrimEnd("`r","`n")
        if($pointer -notmatch '^gitdir: (.+)$'){throw 'Malformed worktree .git pointer'}
        $pointerPath=$Matches[1]
        if(-not [IO.Path]::IsPathRooted($pointerPath)){$pointerPath=[IO.Path]::GetFullPath((Join-Path $Path $pointerPath))}
        if((Get-VerifiedWorktreePath $pointerPath) -ne $Admin){throw 'Worktree .git does not name reported admin directory'}
        $backlink=Get-VerifiedWorktreePath (Join-Path $Admin 'gitdir')
        $backlinkPath=[IO.File]::ReadAllText($backlink).TrimEnd("`r","`n")
        if(-not [IO.Path]::IsPathRooted($backlinkPath)){$backlinkPath=[IO.Path]::GetFullPath((Join-Path $Admin $backlinkPath))}
        if((Get-VerifiedWorktreePath $backlinkPath) -ne $dotGit){throw 'Admin gitdir backlink names a different worktree'}
        $commonFile=Get-VerifiedWorktreePath (Join-Path $Admin 'commondir')
        $commonPointer=[IO.File]::ReadAllText($commonFile).TrimEnd("`r","`n")
        if(-not [IO.Path]::IsPathRooted($commonPointer)){$commonPointer=[IO.Path]::GetFullPath((Join-Path $Admin $commonPointer))}
        if((Get-VerifiedWorktreePath $commonPointer) -ne $Common){throw 'Admin commondir backlink mismatch'}
    }
    $effectiveHead=Invoke-WorktreeGit $Path @('rev-parse','--verify','HEAD')
    $effectiveBranch=Invoke-WorktreeGit $Path @('rev-parse','--symbolic-full-name','HEAD')
    $expectedBranch=if($Entry.ContainsKey('detached')){'HEAD'}else{$Entry.branch}
    if($effectiveHead -ne $Entry.HEAD -or $effectiveBranch -ne $expectedBranch){throw 'Registered/effective checkout HEAD or branch mismatch'}
}

function Read-WorktreeAnnotations {
    param([string]$Path)
    $verified = Get-VerifiedWorktreePath $Path
    if (-not [IO.File]::Exists($verified)) { return @{text='';records=@()} }
    $content = [IO.File]::ReadAllText($verified)
    $blocks = [regex]::Matches($content,'(?ms)^```json\s*\r?\n(.*?)^```\s*$')
    if ($blocks.Count -ne 1) { throw 'Annotations require exactly one fenced JSON block' }
    $data = ConvertFrom-WorktreeJson $blocks[0].Groups[1].Value
    if ($data.schemaVersion -ne 1 -or $null -eq $data.records) { throw 'Invalid annotation schemaVersion/records' }
    $seen = @{}
    foreach ($record in $data.records) {
        foreach ($field in @('identity','path','owner','task','branch','createdAt','expectedPr','teardownCondition','nextReviewDate','disposition','rationale','activityObservedAt','activity')) {
            if ($null -eq $record.PSObject.Properties[$field]) { throw "Annotation missing $field" }
        }
        if (-not $record.identity -or $seen.ContainsKey([string]$record.identity)) { throw 'Duplicate/empty annotation identity' }
        $seen[[string]$record.identity]=$true
    }
    return @{text=$content;records=@($data.records)}
}

function Get-WorktreeAudit {
    param([string]$RepoRoot,[string]$DevelopmentParent,[string]$AnnotationPath,[string]$BaselinePath,[string]$PrMetadataPath)
    $issues=[Collections.Generic.List[string]]::new()
    $rows=[Collections.Generic.List[object]]::new()
    $driveRows=[Collections.Generic.List[object]]::new()
    try {
        $repo=Get-VerifiedWorktreePath $RepoRoot
        $parent=Get-VerifiedWorktreePath $DevelopmentParent
        if (-not [IO.Directory]::Exists($parent)) { throw 'Development parent missing' }
        Assert-WorktreeGitEnvironment
        Assert-WorktreeMetadataPaths $repo
        $common=Get-VerifiedWorktreePath (Invoke-WorktreeGit $repo @('rev-parse','--path-format=absolute','--git-common-dir'))
        $raw=Invoke-WorktreeGit $repo @('worktree','list','--porcelain','-z')
        $registered=[Collections.Generic.List[object]]::new()
        $record=@{}
        foreach($field in $raw.Split([char]0)) {
            if ($field -eq '') { if($record.ContainsKey('worktree')) {$registered.Add($record);$record=@{}}; continue }
            $pair=$field.Split([char[]]@(' '),2,[StringSplitOptions]::None)
            $record[$pair[0]]=if($pair.Count -eq 2){$pair[1]}else{$true}
        }
        if($record.ContainsKey('worktree')){$registered.Add($record)}
        try { $annotations=Read-WorktreeAnnotations $AnnotationPath }
        catch { $issues.Add("Annotation read failed: $_");$annotations=@{records=@()} }
        $pr=$null
        if ($PrMetadataPath) {
            try {
                $pr=ConvertFrom-WorktreeJson ([IO.File]::ReadAllText((Get-VerifiedWorktreePath $PrMetadataPath)))
                $observed=ConvertTo-WorktreeTimestamp $pr.observedAt
                if ($pr.schemaVersion -ne 1 -or $observed -gt [DateTimeOffset]::UtcNow -or
                    ([DateTimeOffset]::UtcNow-$observed).TotalHours -gt 24) { $pr=$null }
            } catch {$pr=$null}
        }
        $used=@{}
        $registeredPaths=@{}
        foreach($entry in $registered) {
            $path=[string]$entry.worktree
            $reasons=[Collections.Generic.List[string]]::new()
            $identity=$null;$annotation=$null;$status='OWNERLESS';$activity='UNKNOWN';$prState='UNKNOWN'
            try {
                $path=Get-VerifiedWorktreePath $path
                if ([IO.Path]::GetDirectoryName($path) -ne $parent) { throw 'Registered path is not an immediate development child' }
                $identity=Get-WorktreePathIdentity $path
                Assert-WorktreeMetadataPaths $path
                $actualCommon=Get-VerifiedWorktreePath (Invoke-WorktreeGit $path @('rev-parse','--path-format=absolute','--git-common-dir'))
                $admin=Get-VerifiedWorktreePath (Invoke-WorktreeGit $path @('rev-parse','--absolute-git-dir'))
                if ($actualCommon -ne $common -or -not (Test-WorktreeContainment $common $admin)) { throw 'Git common/admin relationship mismatch' }
                Assert-WorktreeAdminRelationship -Path $path -Admin $admin -Common $common -Entry $entry
                $matches=@($annotations.records | Where-Object {$_.identity -eq $identity -and $_.path.Replace('/','\').TrimEnd('\') -eq $path})
                if($matches.Count -eq 1) {
                    $annotation=$matches[0];$used[$identity]=$true;$status='ANNOTATED'
                    if(-not $annotation.owner -or -not $annotation.task) {$status='OWNERLESS'}
                    else {
                        try {
                            $review=ConvertTo-WorktreeTimestamp $annotation.nextReviewDate
                            $created=ConvertTo-WorktreeTimestamp $annotation.createdAt
                            $activityTime=ConvertTo-WorktreeTimestamp $annotation.activityObservedAt
                            if($created -gt [DateTimeOffset]::UtcNow -or $activityTime -gt [DateTimeOffset]::UtcNow){throw 'Future annotation observation'}
                            if($annotation.branch -ne ([string]$entry.branch -replace '^refs/heads/','')) {$reasons.Add('BRANCH_DRIFT')}
                            if($review -le [DateTimeOffset]::UtcNow){$reasons.Add('OVERDUE')}
                            if(([DateTimeOffset]::UtcNow-$activityTime).TotalHours -le 24){$activity=[string]$annotation.activity}
                        } catch {$reasons.Add('INVALID_ANNOTATION_DATE')}
                        if($pr -and $annotation.expectedPr) {
                            $prs=@($pr.records | Where-Object {$_.number -eq $annotation.expectedPr -and $_.headRefOid -eq $entry.HEAD})
                            if($prs.Count -eq 1 -and $prs[0].state -in @('OPEN','CLOSED','MERGED')){$prState=$prs[0].state}
                        }
                        if($prState -in @('CLOSED','MERGED')){$reasons.Add($prState)}
                    }
                }
            } catch {$status='UNRESOLVED';$reasons.Add([string]$_)}
            $registeredPaths[$path.Replace('/','\').TrimEnd('\')]=$true
            if($status -eq 'OWNERLESS'){$reasons.Add('OWNERLESS')}
            $acknowledged=$false
            if($annotation -and $annotation.disposition -in @('KEEP','DEFERRED','COMPLETED','ABANDONED') -and $annotation.rationale) {
                try {$acknowledged=(ConvertTo-WorktreeTimestamp $annotation.nextReviewDate) -gt [DateTimeOffset]::UtcNow} catch {}
            }
            $hardReasons=@($reasons | Where-Object {$_ -notin @('MERGED','CLOSED','OVERDUE')})
            $blocked=$status -ne 'ANNOTATED' -or $hardReasons.Count -gt 0 -or ($reasons.Count -gt 0 -and -not $acknowledged)
            # An annotation cannot waive a physical/admin disagreement.
            if($status -eq 'UNRESOLVED'){$blocked=$true}
            if($blocked){$issues.Add("Lifecycle review required: $path ($status)")}
            $rows.Add(@{path=$path;identity=$identity;registered=$true;status=$status;activity=$activity;
                branch=([string]$entry.branch -replace '^refs/heads/','');head=$entry.HEAD;detached=$entry.ContainsKey('detached');
                reviewReasons=@($reasons.ToArray());annotation=$annotation;prState=$prState;blocked=$blocked})
        }
        foreach($child in Get-ChildItem -Force -LiteralPath $parent) {
            if($registeredPaths.ContainsKey($child.FullName)){continue}
            $reparse=($child.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
            if(-not $child.PSIsContainer -and -not $reparse){continue}
            $state=if($reparse){'UNRESOLVED'}else{'UNREGISTERED'}
            $issues.Add("Unregistered or reparse development child: $($child.FullName)")
            $rows.Add(@{path=$child.FullName;identity=$null;registered=$false;status=$state;activity='UNKNOWN';annotation=$null;reviewReasons=@($state);prState='UNKNOWN';blocked=$true})
        }
        foreach($note in $annotations.records) {
            if(-not $used.ContainsKey([string]$note.identity)) {
                $issues.Add("Orphaned annotation: $($note.path)")
                $rows.Add(@{path=$note.path;identity=$note.identity;registered=$false;status='ORPHANED_ANNOTATION';activity='UNKNOWN';annotation=$note;reviewReasons=@('ORPHANED_ANNOTATION');prState='UNKNOWN';blocked=$true})
            }
        }
        try {
            $baseline=ConvertFrom-WorktreeJson ([IO.File]::ReadAllText((Get-VerifiedWorktreePath $BaselinePath)))
            if($baseline.schemaVersion -ne 1 -or -not $baseline.approvedBy -or -not $baseline.approvedAt -or -not $baseline.roots -or
                (Get-VerifiedWorktreePath $baseline.developmentParent) -ne $parent){throw 'Baseline approval/schema/development parent invalid'}
            if((ConvertTo-WorktreeTimestamp $baseline.approvedAt) -gt [DateTimeOffset]::UtcNow){throw 'Future baseline approval'}
            foreach($rootEntry in $baseline.roots) {
                $rootPath=Get-VerifiedWorktreePath $rootEntry.path
                $actual=@{}
                foreach($child in Get-ChildItem -Force -LiteralPath $rootPath) {
                    $actual[$child.FullName]=$true
                    $identity=$null;$state='EXPECTED'
                    try{$identity=Get-WorktreePathIdentity $child.FullName}catch{$state='UNRESOLVED'}
                    $expected=@($rootEntry.children | Where-Object {$_.path.Replace('/','\').TrimEnd('\') -eq $child.FullName})
                    if($expected.Count -ne 1){$state='UNEXPECTED'}elseif($expected[0].identity -ne $identity){$state='IDENTITY_DRIFT'}
                    $driveRows.Add(@{root=$rootPath;path=$child.FullName;identity=$identity;status=$state})
                    if($state -ne 'EXPECTED'){$issues.Add("Drive baseline $state : $($child.FullName)")}
                }
                foreach($expected in $rootEntry.children){if(-not $actual.ContainsKey([string]$expected.path)){$issues.Add("Drive baseline missing child: $($expected.path)")}}
            }
        } catch {$issues.Add("Baseline UNKNOWN: $_")}
    } catch {$issues.Add("Audit UNRESOLVED: $_")}
    return @{schemaVersion=1;observedAt=[DateTimeOffset]::UtcNow.ToString('o');ok=($issues.Count -eq 0);errors=@($issues.ToArray());rows=@($rows.ToArray());driveRoots=@($driveRows.ToArray())}
}

if($MyInvocation.InvocationName -ne '.') {
    $result=Get-WorktreeAudit @auditArguments
    $result | ConvertTo-Json -Depth 20
    if(-not $result.ok){exit 1}
}
