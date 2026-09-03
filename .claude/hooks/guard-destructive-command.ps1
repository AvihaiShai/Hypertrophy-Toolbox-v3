<#
PreToolUse guard for Bash/PowerShell tool calls.

Outcomes (Claude Code PreToolUse contract):
  deny  -> exit 2. The ONLY exit code that blocks. Every other code, including
           1, is non-blocking, so any internal failure here must also exit 2.
  ask   -> permissionDecision JSON on stdout, exit 0. Owner confirms. In
           bypassPermissions, where Claude Code skips prompts, ask-tier
           operations are denied instead of silently proceeding.
  allow -> exit 0, silent.

Profiles:
  agent (default) - charter contract: subagents never push or merge.
  main            - the owner pushes and merges, so those are allowed; every
                    filesystem-destructive verb still applies.

THIS FILE MUST STAY PURE ASCII AND KEEP ITS UTF-8 BOM.
Windows PowerShell 5.1 decodes a BOM-less .ps1 as CP1252. A UTF-8 em dash
(E2 80 94) then becomes U+201D, which PowerShell accepts as a string delimiter,
producing a parser error, exit code 1, and a guard that silently fails open.
tests/test_guard_destructive_command.py pins this.

Contract: confidently classified, or denied. Syntax this guard cannot parse
(unbalanced quoting, base64 -EncodedCommand, nesting past depth 4) denies.

Substring regexes were tried first and leaked: rm -fr, rm -r -f, leading
whitespace, sudo rm -rf, git -C <path> clean -fdx, git clean --force -d, and
git checkout -fq, while blocking the harmless git merge-base. This version
tokenizes with quote awareness, strips wrapper prefixes and their options,
resolves the git subcommand past global options, follows delegated execution
into the command string, and evaluates EVERY position of EVERY segment before
deciding.

Two deliberate limitations, documented so they are not mistaken for oversights:

  * Script FILES are not gated. `bash run.sh` and `powershell -File x.ps1` run
    contents this guard cannot read, but so do `python foo.py`, `node x.js` and
    `npm run x`. Gating only the two shells would break this repo's own
    scripts/*.ps1 tooling and buy consistency of appearance, not of protection.
  * Only two shell grammars are modelled, and only partially. This is a speed
    bump in front of honest mistakes, backed by the deny list in
    .claude/settings.json. It is not a sandbox and must not be described as one.
#>
param(
    [ValidateSet('agent', 'main')]
    [string]$GuardProfile = 'agent'
)

$ErrorActionPreference = 'Stop'

# Wrappers that delegate to the real command.
$prefixes = @('sudo', 'doas', 'command', 'time', 'nice', 'nohup', 'env', 'builtin', 'exec', 'setsid')
# Wrapper options that consume a following value token.
$prefixValueFlags = @('-u', '-g', '-p', '-C', '-t', '-r', '-h', '--user', '--group', '--prompt', '--chdir')

# git global options consumed before the subcommand.
$gitOptsWithValue = @('-C', '-c', '--git-dir', '--work-tree', '--namespace', '--exec-path', '--config-env')
$gitOptsBare = @('--no-pager', '--paginate', '--bare', '--literal-pathspecs', '--no-replace-objects', '--no-optional-locks')

$rmFamily = @('rm', 'del', 'erase', 'rd', 'rmdir', 'remove-item', 'ri')

# Programs that execute a command string given to them. Their argument has to be
# scanned too, or `sh -c "rm -rf tmp"` reads as a harmless call to `sh`.
$posixShells = @('sh', 'bash', 'zsh', 'dash', 'ksh', 'ash')
$psShells = @('powershell', 'pwsh')
# `xargs` deliberately absent: it takes a plain command, not a command string,
# so the every-position scan already reaches the verb in `xargs -I {} rm -rf {}`.
$shellDelegators = $posixShells + $psShells + @('cmd', 'eval')
$maxDelegationDepth = 4

# Fields that may carry an executable command, in preference order.
$commandFields = @('command', 'script', 'code', 'cmd', 'input')

# Disabling MSYS argument conversion can turn a Windows path passed to Git into
# an unrelated POSIX path. Deny observable attempts to set or export either
# escape hatch, while leaving reads and documentation/search text alone.
$blockedEnvironmentNames = @('MSYS_NO_PATHCONV', 'MSYS2_ARG_CONV_EXCL')
$textInspectionCommands = @('echo', 'printf', 'write-output', 'out-string', 'rg',
    'grep', 'git-grep', 'select-string', 'findstr')
$commandPositionMarkers = @('then', 'do', 'else', 'if', 'while', 'until', '{', '(')

function Test-BlockedEnvironmentName([string]$name) {
    return $blockedEnvironmentNames -contains $name.Trim().ToUpperInvariant()
}

function Get-EnvironmentAssignmentName([string]$token) {
    if ($token -match '^([A-Za-z_][A-Za-z0-9_]*)=') { return $matches[1] }
    if ($token -match '^\$\{?env:([A-Za-z_][A-Za-z0-9_]*)\}?=') { return $matches[1] }
    return $null
}

function Test-EnvironmentMutation([string[]]$tokens, [string]$printable) {
    if ($tokens.Count -eq 0) { return $null }

    $head = Get-BareName $tokens[0]
    if ($textInspectionCommands -contains $head) { return $null }
    if ($head -eq 'git' -and $tokens.Count -gt 1 -and $tokens[1].ToLowerInvariant() -eq 'grep') {
        return $null
    }

    # POSIX assignment words are executable only at the start of a simple
    # command (possibly behind wrappers), not as arguments to `echo` or `rg`.
    $i = 0
    while ($i -lt $tokens.Count) {
        $assignmentName = Get-EnvironmentAssignmentName $tokens[$i]
        if ($null -ne $assignmentName) {
            if (Test-BlockedEnvironmentName $assignmentName) {
                return @{ Decision = 'deny'; Reason = "MSYS path-conversion override assignment: $printable" }
            }
            $i++
            continue
        }
        $wrapper = Get-BareName $tokens[$i]
        if ($prefixes -notcontains $wrapper) { break }
        $i++
        while ($i -lt $tokens.Count -and $tokens[$i] -match '^-') {
            if ($prefixValueFlags -contains $tokens[$i]) { $i += 2 } else { $i++ }
        }
    }

    for ($i = 0; $i -lt $tokens.Count; $i++) {
        $token = $tokens[$i]
        $verb = Get-BareName $token
        $rest = @()
        if ($i + 1 -lt $tokens.Count) { $rest = @($tokens[($i + 1)..($tokens.Count - 1)]) }

        # A direct assignment may follow shell control syntax that this partial
        # parser deliberately does not otherwise model.
        $assignmentName = Get-EnvironmentAssignmentName $token
        if ($null -ne $assignmentName -and (Test-BlockedEnvironmentName $assignmentName)) {
            if ($i -eq 0 -or $commandPositionMarkers -contains $tokens[$i - 1].ToLowerInvariant()) {
                return @{ Decision = 'deny'; Reason = "MSYS path-conversion override assignment: $printable" }
            }
        }

        # PowerShell permits whitespace around the assignment operator.
        if ($token -match '^\$\{?env:([A-Za-z_][A-Za-z0-9_]*)\}?$' -and
            (Test-BlockedEnvironmentName $matches[1]) -and $rest.Count -gt 0 -and
            $rest[0] -eq '=') {
            return @{ Decision = 'deny'; Reason = "MSYS path-conversion override assignment: $printable" }
        }

        if ($verb -eq 'env') {
            $j = 0
            while ($j -lt $rest.Count) {
                if ($rest[$j] -match '^-' ) {
                    if ($prefixValueFlags -contains $rest[$j]) { $j += 2 } else { $j++ }
                    continue
                }
                $name = Get-EnvironmentAssignmentName $rest[$j]
                if ($null -eq $name) { break }
                if (Test-BlockedEnvironmentName $name) {
                    return @{ Decision = 'deny'; Reason = "env sets an MSYS path-conversion override: $printable" }
                }
                $j++
            }
        }

        if ($verb -eq 'export') {
            if ($rest -contains '-p' -or $rest -contains '--print' -or $rest -contains '-n') { continue }
            foreach ($candidate in $rest) {
                $name = Get-EnvironmentAssignmentName $candidate
                if ($null -eq $name) { $name = $candidate }
                if (Test-BlockedEnvironmentName $name) {
                    return @{ Decision = 'deny'; Reason = "export exposes an MSYS path-conversion override: $printable" }
                }
            }
        }

        if ($verb -eq 'set' -and $rest.Count -gt 0) {
            $name = Get-EnvironmentAssignmentName $rest[0]
            if ($null -ne $name -and (Test-BlockedEnvironmentName $name)) {
                return @{ Decision = 'deny'; Reason = "cmd set changes an MSYS path-conversion override: $printable" }
            }
        }

        if ($verb -eq 'setx') {
            foreach ($candidate in $rest) {
                if (Test-BlockedEnvironmentName $candidate) {
                    return @{ Decision = 'deny'; Reason = "setx persists an MSYS path-conversion override: $printable" }
                }
            }
        }

        if (@('set-item', 'new-item') -contains $verb) {
            foreach ($candidate in $rest) {
                if ($candidate -match '^(?:env:|environment::)([A-Za-z_][A-Za-z0-9_]*)$' -and
                    (Test-BlockedEnvironmentName $matches[1])) {
                    return @{ Decision = 'deny'; Reason = "PowerShell environment provider changes an MSYS path-conversion override: $printable" }
                }
            }
        }

        if ($token -match '^\[(?:System\.)?Environment\]::SetEnvironmentVariable' -and
            (($tokens[$i..($tokens.Count - 1)] -join ' ') -match
                '(MSYS_NO_PATHCONV|MSYS2_ARG_CONV_EXCL)')) {
            return @{ Decision = 'deny'; Reason = ".NET sets an MSYS path-conversion override: $printable" }
        }
    }
    return $null
}

function Split-Segments([string]$text) {
    # Quote-aware split into segments (on unquoted ; && || | & newline) and
    # tokens (on unquoted whitespace). Quote characters are removed, so a
    # quoted executable path containing spaces survives as one token.
    $segments = New-Object System.Collections.ArrayList
    $tokens = New-Object System.Collections.ArrayList
    $buffer = New-Object System.Text.StringBuilder
    $quote = [char]0

    function Complete-Token {
        if ($buffer.Length -gt 0) {
            [void]$tokens.Add($buffer.ToString())
            [void]$buffer.Clear()
        }
    }
    function Complete-Segment {
        Complete-Token
        if ($tokens.Count -gt 0) {
            [void]$segments.Add(@($tokens.ToArray()))
            [void]$tokens.Clear()
        }
    }

    foreach ($ch in $text.ToCharArray()) {
        if ($quote -ne [char]0) {
            if ($ch -eq $quote) { $quote = [char]0 } else { [void]$buffer.Append($ch) }
            continue
        }
        if ($ch -eq '"' -or $ch -eq "'") { $quote = $ch; continue }
        if ($ch -eq ';' -or $ch -eq '&' -or $ch -eq '|' -or $ch -eq "`n" -or $ch -eq "`r") {
            Complete-Segment
            continue
        }
        if ([char]::IsWhiteSpace($ch)) { Complete-Token; continue }
        [void]$buffer.Append($ch)
    }
    Complete-Segment
    return , $segments.ToArray()
}

function Get-BareName([string]$token) {
    $name = $token
    if ($name.Contains('/') -or $name.Contains('\')) {
        $name = $name.Substring([Math]::Max($name.LastIndexOf('/'), $name.LastIndexOf('\')) + 1)
    }
    return ($name -replace '\.(exe|cmd|bat|ps1)$', '').ToLowerInvariant()
}

function Remove-Wrappers([string[]]$tokens) {
    $i = 0
    while ($i -lt $tokens.Count) {
        $t = $tokens[$i]
        if ($t -match '^[A-Za-z_][A-Za-z0-9_]*=') { $i++; continue }
        if ($prefixes -notcontains (Get-BareName $t)) { break }
        $i++
        while ($i -lt $tokens.Count -and $tokens[$i] -match '^-') {
            if ($prefixValueFlags -contains $tokens[$i]) { $i += 2 } else { $i++ }
        }
    }
    if ($i -ge $tokens.Count) { return @() }
    return @($tokens[$i..($tokens.Count - 1)])
}

function Test-DryRun([string[]]$tokens) {
    foreach ($t in $tokens) {
        if ($t -match '^(--dry-run|--whatif|-WhatIf|-n)$') { return $true }
    }
    return $false
}

function Test-ShortFlag([string]$token, [string]$letter) {
    # Bundled unix short flag anywhere in the cluster: -f, -fdx, -qf.
    # Excludes PowerShell-style single-dash words such as -Force or -Recurse.
    if ($token -cmatch '^-[a-zA-Z]+$' -and $token -cnotmatch '^-[A-Z][a-z]{2,}$') {
        return $token.Substring(1).Contains($letter)
    }
    return $false
}

function Get-PsParameter([string]$token) {
    # PowerShell parameters may be abbreviated to any unambiguous prefix and may
    # carry an explicit switch value: -Rec, -Fo, -Recurse:$true, -Force:$false.
    if ($token -notmatch '^-([A-Za-z]+)(?::(.*))?$') { return $null }
    return @{
        Name     = $matches[1].ToLowerInvariant()
        HasValue = $token.Contains(':')
        Value    = $matches[2]
    }
}

function Test-PsSwitchOn($param) {
    # Conservative: a switch is ON unless it is explicitly given a false value.
    # Anything unrecognised (a variable, an expression) is treated as ON.
    if (-not $param.HasValue) { return $true }
    $value = ($param.Value -replace '^\$', '').ToLowerInvariant()
    return -not ($value -eq 'false' -or $value -eq '0')
}

function Get-RmFlags([string[]]$tokens, [string]$verb) {
    $recursive = $false
    $force = $false
    # cmd.exe deletion commands take slash-flags: rmdir /s /q, del /f /s /q.
    # Only parsed for those verbs, because `/s` after POSIX `rm` is a path.
    $slashFlagVerbs = @('del', 'erase', 'rd', 'rmdir')
    foreach ($t in $tokens) {
        if ($slashFlagVerbs -contains $verb -and $t -match '^/[a-zA-Z]+$') {
            $letters = $t.Substring(1).ToLowerInvariant()
            if ($letters.Contains('s')) { $recursive = $true }
            if ($letters.Contains('q') -or $letters.Contains('f')) { $force = $true }
            continue
        }
        $psParam = Get-PsParameter $t
        if ($null -ne $psParam) {
            $handled = $true
            if ('recurse'.StartsWith($psParam.Name)) {
                if (Test-PsSwitchOn $psParam) { $recursive = $true }
            }
            elseif ('force'.StartsWith($psParam.Name)) {
                if (Test-PsSwitchOn $psParam) { $force = $true }
            }
            elseif ($psParam.Name.Length -ge 2 -and 'confirm'.StartsWith($psParam.Name)) {
                # -Confirm:$false suppresses the prompt, which is what -Force does.
                if (-not (Test-PsSwitchOn $psParam)) { $force = $true }
            }
            else { $handled = $false }
            if ($handled) { continue }
        }
        if ($t -match '^--recursive$') { $recursive = $true; continue }
        if ($t -match '^--force$') { $force = $true; continue }
        if ($t -match '^--no-preserve-root$') { $force = $true; continue }
        if ((Test-ShortFlag $t 'r') -or (Test-ShortFlag $t 'R')) { $recursive = $true }
        if (Test-ShortFlag $t 'f') { $force = $true }
    }
    return @{ Recursive = $recursive; Force = $force }
}

function Get-GitSubcommand([string[]]$tokens) {
    $i = 1
    while ($i -lt $tokens.Count) {
        $t = $tokens[$i]
        if ($gitOptsWithValue -contains $t) { $i += 2; continue }
        if ($t -match '^(--git-dir|--work-tree|--namespace|--exec-path|--config-env)=') { $i++; continue }
        if ($gitOptsBare -contains $t) { $i++; continue }
        if ($t -match '^-') { $i++; continue }
        # Two statements: see the note in Get-Delegation about single-element
        # arrays unrolling to scalars through if-statement output.
        $rest = @()
        if ($i + 1 -lt $tokens.Count) { $rest = @($tokens[($i + 1)..($tokens.Count - 1)]) }
        return @{ Name = $t.ToLowerInvariant(); Rest = $rest }
    }
    return $null
}

function Test-AnyForce([string[]]$tokens) {
    foreach ($t in $tokens) {
        if ($t -eq '--force' -or (Test-ShortFlag $t 'f')) { return $true }
    }
    return $false
}

function Get-VerbCandidates([string]$token) {
    # Both readings of the program name, because they disagree on escapes:
    # `r\m` is a path whose basename is `m`, but Bash reads the backslash as an
    # escape and runs `rm`. Anything matching EITHER reading is treated as that
    # program. `/bin/rm` and `"C:\...\rm.exe"` still resolve through the path
    # reading.
    $candidates = New-Object System.Collections.ArrayList
    [void]$candidates.Add((Get-BareName $token))
    # Bash ANSI-C quoting: the tokenizer strips the quotes from `$'rm'`, leaving
    # a leading `$` that the shell never passes to exec.
    $bare = $token -replace '^\$', ''
    $unescaped = $bare -replace '\\', ''
    foreach ($form in @($bare, $unescaped)) {
        if ($form -ne $token) {
            [void]$candidates.Add((Get-BareName $form))
            [void]$candidates.Add($form.ToLowerInvariant())
        }
    }
    return $candidates.ToArray()
}

function Test-QuotesBalanced([string]$text) {
    $quote = [char]0
    foreach ($ch in $text.ToCharArray()) {
        if ($quote -ne [char]0) {
            if ($ch -eq $quote) { $quote = [char]0 }
            continue
        }
        if ($ch -eq '"' -or $ch -eq "'") { $quote = $ch }
    }
    return ($quote -eq [char]0)
}

function Get-Delegation([string[]]$tokens) {
    # Returns how to treat a program that runs another command:
    #   script -> the nested command string, to be scanned recursively
    #   deny   -> the nested command cannot be recovered (base64)
    #   ask    -> an opaque script file is being executed
    #   $null  -> not a delegator
    $verbs = Get-VerbCandidates $tokens[0]
    $shell = $null
    foreach ($v in $verbs) {
        if ($shellDelegators -contains $v) { $shell = $v; break }
    }
    if ($null -eq $shell) { return $null }

    $printable = $tokens -join ' '
    # Assigned in two statements on purpose: `$x = if (...) { @($a[1..1]) }`
    # unrolls a one-element array to a scalar string through the if-statement's
    # output, after which $x[0] indexes a CHARACTER instead of the token.
    $rest = @()
    if ($tokens.Count -gt 1) { $rest = @($tokens[1..($tokens.Count - 1)]) }

    foreach ($t in $rest) {
        if ($t -match '^-{1,2}(e|enc|encoded|encodedcommand)$') {
            return @{ Kind = 'deny'; Reason = "base64-encoded shell command cannot be classified: $printable" }
        }
    }

    $flagIndex = -1
    for ($i = 0; $i -lt $rest.Count; $i++) {
        $t = $rest[$i]
        # `c` need not be last in the cluster: `bash -cl <script>` is valid.
        if ($posixShells -contains $shell -and $t -cmatch '^-[a-z]*c[a-z]*$') { $flagIndex = $i; break }
        if ($psShells -contains $shell -and $t -match '^-c[a-z]*$') { $flagIndex = $i; break }
        if ($shell -eq 'cmd' -and $t -match '^[/-][ck]$') { $flagIndex = $i; break }
    }

    if ($shell -eq 'eval') {
        if ($rest.Count -eq 0) { return $null }
        return @{ Kind = 'script'; Script = ($rest -join ' ') }
    }
    if ($flagIndex -ge 0) {
        if ($flagIndex + 1 -ge $rest.Count) {
            return @{ Kind = 'deny'; Reason = "shell invoked with an empty command argument: $printable" }
        }
        return @{ Kind = 'script'; Script = (@($rest[($flagIndex + 1)..($rest.Count - 1)]) -join ' ') }
    }

    # A shell handed a script FILE (`bash run.sh`, `powershell -File x.ps1`) is
    # deliberately not escalated. The guard cannot read that file either way, and
    # gating it while `python foo.py`, `node x.js` and `npm run x` stay ungated
    # buys nothing while breaking this repo's own scripts/*.ps1 tooling.
    return $null
}

# xargs options split by how they take a value, because getting this wrong
# swallows the executable. Case matters: `-I` requires a replace-string, while
# its deprecated lowercase synonym `-i` takes one only when attached.
$xargsRequiredShort = @('-I', '-L', '-n', '-P', '-s', '-d', '-a', '-E')
$xargsOptionalShort = @('-i', '-l', '-e')
$xargsRequiredLong = @('--max-args', '--max-procs', '--max-chars', '--delimiter',
    '--arg-file', '--process-slot-var')
# Optional-value long options bind ONLY as --opt=value. Written alone, the next
# token is the command, so consuming it would hide `xargs --replace rm -rf`.
$xargsOptionalLong = @('--replace', '--max-lines', '--eof')

function Get-XargsCommand([string[]]$tokens) {
    # Everything before the first non-option token belongs to xargs itself; what
    # follows is the program it will run. This boundary matters: in
    # `xargs -n1 echo rm -rf` the executable is `echo` and `rm` is data being
    # printed, so the every-position rule must not be applied to this segment.
    $i = 1
    while ($i -lt $tokens.Count) {
        $t = $tokens[$i]
        # --opt=value carries its own value.
        if ($t -match '^--[a-zA-Z-]+=') { $i++; continue }
        if ($xargsRequiredLong -ccontains $t) { $i += 2; continue }
        # Optional-value long options bind only with `=`, so written alone they
        # consume nothing and the next token is the command.
        if ($xargsOptionalLong -ccontains $t) { $i++; continue }
        if ($t -match '^--') { $i++; continue }
        if ($t -match '^-.') {
            # `-n1` and `-i{}` carry their value attached, whatever the option.
            if ($t.Length -gt 2) { $i++; continue }
            $short = $t.Substring(0, 2)
            # -ccontains: `-I` requires a value, `-i` does not.
            if ($xargsRequiredShort -ccontains $short) { $i += 2; continue }
            # Optional-value and plain switches alone consume nothing.
            $i++
            continue
        }
        break
    }
    if ($i -ge $tokens.Count) { return @() }
    return @($tokens[$i..($tokens.Count - 1)])
}

function Test-Segment([string[]]$tokens, [string]$printable) {
    $tokens = @(Remove-Wrappers $tokens)
    if ($tokens.Count -eq 0) { return $null }

    $verbs = @(Get-VerbCandidates $tokens[0])
    $verb = $null
    foreach ($v in $verbs) {
        if ($rmFamily -contains $v -or $v -eq 'git') { $verb = $v; break }
    }
    if ($null -eq $verb) { return $null }
    $rest = @()
    if ($tokens.Count -gt 1) { $rest = @($tokens[1..($tokens.Count - 1)]) }

    if ($rmFamily -contains $verb) {
        if (Test-DryRun $rest) { return $null }
        $flags = Get-RmFlags $rest $verb
        $inherentlyRecursive = @('rd', 'rmdir') -contains $verb
        if ($flags.Recursive -or $inherentlyRecursive) {
            if ($flags.Force) {
                return @{ Decision = 'deny'; Reason = "recursive force delete: $printable" }
            }
            return @{ Decision = 'ask'; Reason = "recursive delete, confirm the target: $printable" }
        }
        return $null
    }

    if ($verb -ne 'git') { return $null }
    $sub = Get-GitSubcommand $tokens
    if ($null -eq $sub) { return $null }
    $subRest = $sub.Rest
    if (Test-DryRun $subRest) { return $null }

    switch ($sub.Name) {
        'reset' {
            if ($subRest -contains '--hard') {
                return @{ Decision = 'deny'; Reason = "git reset --hard discards working-tree changes: $printable" }
            }
        }
        'clean' {
            if (Test-AnyForce $subRest) {
                return @{ Decision = 'deny'; Reason = "git clean force deletes untracked files: $printable" }
            }
        }
        'rm' {
            if ($subRest -contains '--cached') {
                # --cached only edits the index; the working tree is left alone.
                # The risk is downstream: once untracked, a later clean removes it.
                return @{ Decision = 'ask'; Reason = "git rm --cached untracks files, exposing them to a later clean: $printable" }
            }
            return @{ Decision = 'ask'; Reason = "git rm deletes working-tree files: $printable" }
        }
        'push' {
            foreach ($t in $subRest) {
                if ($t -eq '--force' -or $t -eq '--delete' -or $t -like '--force-with-lease*' -or (Test-ShortFlag $t 'f') -or (Test-ShortFlag $t 'd')) {
                    return @{ Decision = 'deny'; Reason = "force or delete push rewrites remote history: $printable" }
                }
            }
            if ($GuardProfile -eq 'agent') {
                return @{ Decision = 'deny'; Reason = "subagents do not push; hand the branch to the owner" }
            }
        }
        'merge' {
            if ($GuardProfile -eq 'agent') {
                return @{ Decision = 'deny'; Reason = "subagents do not merge; hand the branch to the owner" }
            }
        }
        'branch' {
            $forceDelete = $false
            foreach ($t in $subRest) {
                if ($t -cmatch '^-[a-zA-Z]*D[a-zA-Z]*$') { $forceDelete = $true }
            }
            if (($subRest -contains '--delete') -and (Test-AnyForce $subRest)) { $forceDelete = $true }
            if ($forceDelete) {
                return @{ Decision = 'ask'; Reason = "git branch force-delete drops an unmerged branch: $printable" }
            }
        }
        'worktree' {
            if ($subRest.Count -ge 1 -and $subRest[0] -eq 'remove') {
                return @{ Decision = 'ask'; Reason = "git worktree remove discards a worktree: $printable" }
            }
        }
        'checkout' {
            if (Test-AnyForce $subRest) {
                return @{ Decision = 'ask'; Reason = "git checkout --force overwrites local modifications: $printable" }
            }
        }
    }
    return $null
}

function Get-CandidateCommands($toolInput) {
    # No comma operator here: `, $empty` returns a one-element array containing
    # an empty array, which reads as Count 1 at the call site and defeats the
    # fail-closed check.
    $found = New-Object System.Collections.ArrayList
    if ($null -eq $toolInput) { return @() }
    foreach ($field in $commandFields) {
        $value = $toolInput.PSObject.Properties[$field]
        if ($null -ne $value -and $value.Value -is [string] -and -not [string]::IsNullOrWhiteSpace($value.Value)) {
            [void]$found.Add([string]$value.Value)
        }
    }
    if ($found.Count -eq 0) {
        # Unknown schema. Scan every string field except free-text metadata so a
        # renamed command field cannot slip past unexamined.
        foreach ($property in $toolInput.PSObject.Properties) {
            if ($property.Name -eq 'description') { continue }
            if ($property.Value -is [string] -and -not [string]::IsNullOrWhiteSpace($property.Value)) {
                [void]$found.Add([string]$property.Value)
            }
        }
    }
    return $found.ToArray()
}

function Invoke-CommandScan([string]$command, [int]$depth) {
    if ($depth -gt $maxDelegationDepth) {
        [void]$script:denials.Add("command nesting exceeds $maxDelegationDepth levels; cannot classify: $command")
        return
    }

    # A backslash before a newline is a line continuation: the shell joins the
    # two lines into one word, so `r\<newline>m -rf tmp` runs `rm`. Join first,
    # or the newline reads as a segment break and hides the verb.
    $command = $command -replace '\\\r?\n', ''

    if (-not (Test-QuotesBalanced $command)) {
        # Quoting the guard cannot close means its tokenization is not
        # trustworthy at all: a quote may be hiding a separator, as in
        # `echo "; rm -rf tmp`. Unclassifiable syntax is denied, not guessed at.
        [void]$script:denials.Add("unbalanced quoting; the command cannot be classified: $command")
        return
    }

    foreach ($tokens in (Split-Segments $command)) {
        if ($tokens.Count -eq 0) { continue }

        $environmentMutation = Test-EnvironmentMutation $tokens ($tokens -join ' ')
        if ($null -ne $environmentMutation) {
            [void]$script:denials.Add($environmentMutation.Reason)
        }

        $stripped = @(Remove-Wrappers $tokens)
        if ($stripped.Count -eq 0) { continue }

        # xargs states its own command boundary, so honour it rather than
        # scanning positions: only the program it runs is executable, and its
        # trailing arguments are data.
        if ((Get-VerbCandidates $stripped[0]) -contains 'xargs') {
            $inner = @(Get-XargsCommand $stripped)
            if ($inner.Count -gt 0) {
                $delegation = Get-Delegation $inner
                if ($null -ne $delegation) {
                    switch ($delegation.Kind) {
                        'deny' { [void]$script:denials.Add($delegation.Reason) }
                        'ask' { [void]$script:asks.Add($delegation.Reason) }
                        'script' { Invoke-CommandScan $delegation.Script ($depth + 1) }
                    }
                }
                else {
                    $result = Test-Segment $inner ($inner -join ' ')
                    if ($null -ne $result) {
                        if ($result.Decision -eq 'deny') { [void]$script:denials.Add($result.Reason) }
                        elseif ($result.Decision -eq 'ask') { [void]$script:asks.Add($result.Reason) }
                    }
                }
            }
            continue
        }

        # Evaluate EVERY position, not just the head of the segment. A verb
        # reaches command position behind control syntax the guard does not
        # model -- `then rm -rf x`, `if exist x rmdir /s /q x`, `& { Remove-Item
        # ... }`, `try { ... } catch {}`, `xargs -I {} rm -rf {}`. Enumerating
        # keywords would be an endless list of two-shell grammar; scanning every
        # position removes the whole class instead.
        for ($i = 0; $i -lt $stripped.Count; $i++) {
            $suffix = @($stripped[$i..($stripped.Count - 1)])

            $delegation = Get-Delegation $suffix
            if ($null -ne $delegation) {
                switch ($delegation.Kind) {
                    'deny' { [void]$script:denials.Add($delegation.Reason) }
                    'ask' { [void]$script:asks.Add($delegation.Reason) }
                    'script' { Invoke-CommandScan $delegation.Script ($depth + 1) }
                }
                # The rest of this segment is the nested command's own argument.
                break
            }

            $result = Test-Segment $suffix ($suffix -join ' ')
            if ($null -eq $result) { continue }
            if ($result.Decision -eq 'deny') { [void]$script:denials.Add($result.Reason) }
            elseif ($result.Decision -eq 'ask') { [void]$script:asks.Add($result.Reason) }
        }
    }
}

# --- entry point -------------------------------------------------------------
try {
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) {
        [Console]::Error.WriteLine("Guard received no hook payload; failing closed.")
        exit 2
    }
    $payload = $raw | ConvertFrom-Json
    $permissionMode = [string]$payload.permission_mode
    $toolInput = $payload.tool_input
    if ($null -eq $toolInput) {
        [Console]::Error.WriteLine("Guard received no tool_input; failing closed.")
        exit 2
    }
    $commands = @(Get-CandidateCommands $toolInput)
    if ($commands.Count -eq 0) {
        [Console]::Error.WriteLine("Guard found no command field in tool_input; failing closed.")
        exit 2
    }

    # Evaluate EVERY segment of EVERY candidate before deciding. An early ask
    # must not mask a later deny: `rm -r a && rm -rf b` is a deny, because
    # approving the prompt would run both.
    $script:denials = New-Object System.Collections.ArrayList
    $script:asks = New-Object System.Collections.ArrayList

    foreach ($command in $commands) {
        Invoke-CommandScan $command 0
    }

    $denials = @($script:denials | Select-Object -Unique)
    $asks = @($script:asks | Select-Object -Unique)

    if ($denials.Count -gt 0) {
        [Console]::Error.WriteLine("Blocked by $GuardProfile guard: " + ($denials -join ' | '))
        exit 2
    }
    if ($asks.Count -gt 0) {
        $askReason = ($asks -join ' | ') + " ($GuardProfile guard)"
        if ([string]::IsNullOrWhiteSpace($permissionMode) -or $permissionMode -eq 'bypassPermissions') {
            [Console]::Error.WriteLine(
                "Blocked by $GuardProfile guard: confirmation is required, but permission mode " +
                "'$permissionMode' cannot enforce an ask prompt. Switch out of bypassPermissions " +
                "and retry, or run the command manually. $askReason"
            )
            exit 2
        }
        $decision = @{
            hookSpecificOutput = @{
                hookEventName            = 'PreToolUse'
                permissionDecision       = 'ask'
                permissionDecisionReason = $askReason
            }
        }
        [Console]::Out.WriteLine(($decision | ConvertTo-Json -Compress -Depth 5))
        exit 0
    }
    exit 0
}
catch {
    [Console]::Error.WriteLine("Guard failed to evaluate the command and is failing closed: $_")
    exit 2
}
