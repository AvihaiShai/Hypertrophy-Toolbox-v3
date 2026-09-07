<#
PreToolUse guard for Bash/PowerShell tool calls.

Outcomes (Claude Code PreToolUse contract):
  deny  -> exit 2. The ONLY exit code that blocks. Every other code, including
           1, is non-blocking, so any internal failure here must also exit 2.
  ask   -> permissionDecision JSON on stdout, exit 0. Owner confirms. In
           auto and bypassPermissions, without verified owner confirmation, ask-tier
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

Worktree-retention hold: worktree removal and branch, tag, symbolic-ref,
update-ref and remote-ref deletion deny in both profiles and every permission
mode. Destructive push forms and worktree prune are exempt only for a proven
dry run from their own option parsers. Other retention checks precede the generic dry-run exemption;
those subcommands have no dry-run option, and git tag -n means annotation lines.
This is bounded Claude-tool coverage; opaque scripts, non-Claude tools and
non-delete ref retirement remain outside it.

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
    $mutation = '(?:[-+*/%&|^]?=|<<=|>>=|\?\?=|\+\+|--)'
    if ($token -match ('^([A-Za-z_][A-Za-z0-9_]*)' + $mutation)) { return $matches[1] }
    if ($token -match ('^\$\{?env:([A-Za-z_][A-Za-z0-9_]*)\}?' + $mutation)) { return $matches[1] }
    if ($token -match '^(?:\+\+|--)\$\{?env:([A-Za-z_][A-Za-z0-9_]*)\}?$') { return $matches[1] }
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
            $rest[0] -match '^(?:[-+*/%&|^]?=|<<=|>>=|\?\?=|\+\+|--)$') {
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
            foreach ($candidate in $rest) {
                $name = Get-EnvironmentAssignmentName $candidate
                if ($null -eq $name) {
                    if ($rest -contains '-p' -or $rest -contains '--print' -or $rest -contains '-n') { continue }
                    $name = $candidate
                }
                if (Test-BlockedEnvironmentName $name) {
                    return @{ Decision = 'deny'; Reason = "export exposes an MSYS path-conversion override: $printable" }
                }
            }
        }

        if ($verb -eq 'set' -and $rest.Count -gt 0) {
            if ($rest[0] -eq '/a') {
                # cmd arithmetic permits spaces around operators and several
                # assignments in one comma-separated expression.
                $arithmetic = ($rest | Select-Object -Skip 1) -join ' '
                foreach ($assignment in [regex]::Matches($arithmetic,
                    '(?:^|[,(\s])([A-Za-z_][A-Za-z0-9_]*)\s*(?:[-+*/%&|^]?=|<<=|>>=|\+\+|--)')) {
                    if (Test-BlockedEnvironmentName $assignment.Groups[1].Value) {
                        return @{ Decision = 'deny'; Reason = "cmd arithmetic changes an MSYS path-conversion override: $printable" }
                    }
                }
            }
            foreach ($candidate in $rest) {
                if ($candidate -match '^/[ap]$') { continue }
                $name = Get-EnvironmentAssignmentName $candidate
                if ($null -ne $name -and (Test-BlockedEnvironmentName $name)) {
                    return @{ Decision = 'deny'; Reason = "cmd set changes an MSYS path-conversion override: $printable" }
                }
            }
        }

        if ($verb -eq 'setx') {
            foreach ($candidate in $rest) {
                if (Test-BlockedEnvironmentName $candidate) {
                    return @{ Decision = 'deny'; Reason = "setx persists an MSYS path-conversion override: $printable" }
                }
            }
        }

        if (@('set-item', 'new-item', 'set-content', 'add-content', 'si', 'ni', 'sc', 'ac') -contains $verb) {
            foreach ($candidate in $rest) {
                if ($candidate -match '^(?:env:|environment::)[\\/]?([A-Za-z_][A-Za-z0-9_]*)$' -and
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
    # An EMPTY quoted argument is a real argument position. Dropping it makes
    # `git update-ref <ref> "" <old-oid>` -- which deletes the ref -- read as an
    # ordinary two-operand update. A hashtable is used rather than a plain
    # variable because a nested function assigning to a parent-scope variable
    # would only create its own local copy; mutating a hashtable property does
    # reach the caller.
    $quoted = @{ Seen = $false }

    function Complete-Token {
        if ($buffer.Length -gt 0 -or $quoted.Seen) {
            [void]$tokens.Add($buffer.ToString())
            [void]$buffer.Clear()
            $quoted.Seen = $false
        }
    }
    function Complete-Segment {
        Complete-Token
        if ($tokens.Count -gt 0) {
            [void]$segments.Add(@($tokens.ToArray()))
            [void]$tokens.Clear()
        }
    }

    for ($characterIndex = 0; $characterIndex -lt $text.Length; $characterIndex++) {
        $ch = $text[$characterIndex]
        if ($quote -ne [char]0) {
            if ($ch -eq $quote) { $quote = [char]0 } else { [void]$buffer.Append($ch) }
            continue
        }
        if ($ch -eq '"' -or $ch -eq "'") { $quote = $ch; $quoted.Seen = $true; continue }
        # Preserve cmd arithmetic compound operators long enough to classify
        # their assignment target; the shell boundary otherwise splits & and |.
        if (($ch -eq '&' -or $ch -eq '|') -and $characterIndex + 1 -lt $text.Length -and
            $text[$characterIndex + 1] -eq '=' -and $tokens.Count -ge 2 -and
            (Get-BareName $tokens[0]) -eq 'set' -and $tokens[1] -eq '/a') {
            [void]$buffer.Append($ch)
            continue
        }
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

function Test-WorktreePruneDryRun([string[]]$pruneArgs) {
    # `git worktree prune` accepts -n/--dry-run, -v/--verbose and
    # --expire <expiry-date>, each with a --no- negation (git 2.55 usage).
    # Test-DryRun above matches a bare --dry-run token ANYWHERE, which two
    # real invocations defeat:
    #   git worktree prune --dry-run --no-dry-run  (last flag wins: prunes)
    #   git worktree prune --expire --dry-run      (--dry-run is eaten as the
    #                                               expiry value: prunes)
    # So prune parses its own grammar, tracking negation and flag order.
    # $true means PROVEN dry run. A proven real prune and anything this parser
    # does not recognise both return $false, so an unknown option is denied
    # rather than exempted.
    $dry = $false
    $i = 0
    while ($i -lt $pruneArgs.Count) {
        $t = $pruneArgs[$i]
        if ($t -eq '--') {
            # prune takes no operands; a trailing one is a malformed call.
            if ($i -ne $pruneArgs.Count - 1) { return $false }
            return $dry
        }
        elseif ($t -eq '--dry-run') { $dry = $true; $i++ }
        elseif ($t -eq '--no-dry-run') { $dry = $false; $i++ }
        elseif ($t -eq '--verbose' -or $t -eq '--no-verbose' -or $t -eq '--no-expire') { $i++ }
        elseif ($t -like '--expire=*') { $i++ }
        elseif ($t -eq '--expire') {
            # Consumes the next token as its value, whatever it looks like.
            # A missing value is malformed: fail closed.
            if ($i + 1 -ge $pruneArgs.Count) { return $false }
            $i += 2
        }
        elseif ($t -cmatch '^-[nv]+$') {
            # Bundled short flags; only n and v are valid here. Case-sensitive:
            # -N and -V are not options of this subcommand.
            if ($t -cmatch 'n') { $dry = $true }
            $i++
        }
        else { return $false }
    }
    return $dry
}

# git push option grammar, transcribed from `git push -h` (git 2.55).
# EVERY push verdict -- dry run, deletion, force, and the operand list the
# refspec check reads -- comes from this one table and the one parser below.
# Two defects came from having more than one reading of the same argument list:
#   git push --del origin wt-example   an exact-string test for '--delete' misses
#                                      an unambiguous parse-opt abbreviation
#   git push -4d origin wt-example     Test-ShortFlag's ^-[a-zA-Z]+$ rejects a
#                                      cluster containing a digit, hiding -d
# Both are real deletions of a remote ref.
$pushLongNames = @(
    'verbose', 'quiet', 'repo', 'all', 'branches', 'mirror', 'delete', 'tags',
    'dry-run', 'porcelain', 'force', 'force-with-lease', 'force-if-includes',
    'recurse-submodules', 'thin', 'receive-pack', 'exec', 'set-upstream',
    'progress', 'prune', 'verify', 'follow-tags', 'signed', 'atomic',
    'push-option', 'ipv4', 'ipv6',
    'no-verbose', 'no-quiet', 'no-repo', 'no-all', 'no-branches', 'no-mirror',
    'no-delete', 'no-tags', 'no-dry-run', 'no-porcelain', 'no-force',
    'no-force-with-lease', 'no-force-if-includes', 'no-recurse-submodules',
    'no-thin', 'no-receive-pack', 'no-exec', 'no-set-upstream', 'no-progress',
    'no-prune', 'no-verify', 'no-follow-tags', 'no-signed', 'no-atomic',
    'no-push-option')
# Options whose value is the FOLLOWING token when written without '='. The
# optional-argument options (--force-with-lease, --signed) are deliberately
# absent: they bind a value only with '=', so written alone they consume nothing.
$pushValueNames = @('repo', 'receive-pack', 'exec', 'push-option',
    'recurse-submodules')
# Short options carrying no meaning for this guard. -n, -d, -f and -o are
# handled by name. Digits are included because -4 and -6 are real options, and a
# cluster may mix them with letters, as in -4d.
$pushShortBare = 'vqu46'

function Resolve-GitPushOption([string]$given) {
    # git's parse-opt takes an exact match first, then a UNIQUE prefix, so
    # `--del` resolves to --delete and deletes. Returns the canonical name, or
    # $null when the token is unknown OR ambiguous -- `--f` matches force,
    # force-with-lease, force-if-includes and follow-tags, and git rejects it.
    if ($pushLongNames -ccontains $given) { return $given }
    $candidates = @($pushLongNames | Where-Object { $_.StartsWith($given) })
    if ($candidates.Count -eq 1) { return $candidates[0] }
    return $null
}

function Set-GitPushIntent($state, [string]$name) {
    # Dry-run, delete, mirror and prune honor their own last positive/negative
    # option. Force and force-with-lease are separately latched during the
    # retention hold: neither negation clears positive force intent. This is
    # deliberately conservative, including self-cancelling force options.
    # A proven dry run remains exempt before the force verdict is evaluated.
    if ($name -ceq 'dry-run') { $state.Dry = $true }
    elseif ($name -ceq 'no-dry-run') { $state.Dry = $false }
    elseif ($name -ceq 'delete') { $state.Delete = $true }
    elseif ($name -ceq 'no-delete') { $state.Delete = $false }
    elseif ($name -ceq 'force') { $state.Force = $true }
    elseif ($name -ceq 'force-with-lease') { $state.ForceWithLease = $true }
    elseif ($name -ceq 'no-force' -or $name -ceq 'no-force-with-lease') {
        # Recognised, so the option resolves and the parse still succeeds, but
        # deliberately inert: a positive force option is not cancellable here.
    }
    elseif ($name -ceq 'mirror') { $state.Mirror = $true }
    elseif ($name -ceq 'no-mirror') { $state.Mirror = $false }
    elseif ($name -ceq 'prune') { $state.Prune = $true }
    elseif ($name -ceq 'no-prune') { $state.Prune = $false }
}

function Get-GitPushParse([string[]]$pushArgs) {
    # git push [<options>] [<repository> [<refspec>...]]
    # One pass produces every intent the caller needs:
    #   Dry / Delete / Mirror / Prune          option intent, negation-aware
    #   Force / ForceWithLease                 option intent, LATCHED; see
    #                                          Set-GitPushIntent for why
    #   Operands                               repository and refspec positions
    #   Parsed                                 $false if any token was not
    #                                          recognised; Unrecognised names it
    #
    # Test-DryRun cannot be used for any of this. It matches a bare --dry-run or
    # -n token anywhere in the list, and all three of these defeat it:
    #   git push --dry-run --no-dry-run ...  last flag wins, so this PUSHES
    #   git push -o --dry-run ...            --dry-run is -o's value
    #   git push --repo --dry-run ...        likewise
    $state = @{
        Dry = $false; Delete = $false; Force = $false; ForceWithLease = $false;
        Mirror = $false; Prune = $false; Operands = @(); Parsed = $true;
        Unrecognised = ''
    }
    $operands = New-Object System.Collections.ArrayList
    $i = 0
    while ($i -lt $pushArgs.Count) {
        $t = $pushArgs[$i]
        if ($t -eq '--') {
            $i++
            while ($i -lt $pushArgs.Count) { [void]$operands.Add($pushArgs[$i]); $i++ }
            break
        }
        if ($t -ceq '-') { [void]$operands.Add($t); $i++; continue }
        if ($t -cmatch '^--') {
            $given = $t.Substring(2)
            $attached = $false
            if ($given.Contains('=')) {
                $given = ($given -split '=', 2)[0]
                $attached = $true
            }
            $name = Resolve-GitPushOption $given
            if ($null -eq $name) {
                $state.Parsed = $false
                $state.Unrecognised = $t
                return $state
            }
            Set-GitPushIntent $state $name
            if (-not $attached -and ($pushValueNames -ccontains $name)) {
                # The value is the following token, whatever it looks like.
                if ($i + 1 -ge $pushArgs.Count) {
                    $state.Parsed = $false
                    $state.Unrecognised = $t
                    return $state
                }
                $i += 2
                continue
            }
            $i++
            continue
        }
        if ($t -cmatch '^-[A-Za-z0-9]') {
            $cluster = $t.Substring(1)
            $takesNextToken = $false
            for ($c = 0; $c -lt $cluster.Length; $c++) {
                $letter = [string]$cluster[$c]
                if ($letter -ceq 'n') { $state.Dry = $true; continue }
                if ($letter -ceq 'd') { $state.Delete = $true; continue }
                if ($letter -ceq 'f') { $state.Force = $true; continue }
                if ($letter -ceq 'o') {
                    # -o wants a value: the rest of the cluster if there is one,
                    # otherwise the next token. Either way the cluster ends here.
                    if ($c -eq $cluster.Length - 1) { $takesNextToken = $true }
                    break
                }
                if ($pushShortBare.Contains($letter)) { continue }
                $state.Parsed = $false
                $state.Unrecognised = $t
                return $state
            }
            $i++
            if ($takesNextToken) {
                if ($i -ge $pushArgs.Count) {
                    $state.Parsed = $false
                    $state.Unrecognised = $t
                    return $state
                }
                $i++
            }
            continue
        }
        [void]$operands.Add($t)
        $i++
    }
    $state.Operands = @($operands.ToArray())
    return $state
}

function Test-LongOptionPrefix([string]$token, [string]$name) {
    # git's parse-opt accepts any UNAMBIGUOUS abbreviation of a long option, so
    # `git branch --del x` deletes exactly as `--delete` does and must classify
    # the same way. Callers pass only names that are unambiguous WITHIN their
    # own subcommand; `git update-ref` deliberately does not use this helper,
    # because there `--d` is ambiguous between --deref and --no-deref and there
    # is no --delete long option at all.
    # A `--no-` negation never matches: it starts with n, so the safe direction
    # (classify as the deleting form) is what an operator gets.
    if ($token -cnotmatch '^--[a-z-]+$') { return $false }
    $given = $token.Substring(2)
    if ($given.Length -eq 0) { return $false }
    return $name.StartsWith($given)
}

function Test-GitBranchDelete([string[]]$branchArgs) {
    # git branch [<options>] [-r] (-d | -D) <branch-name>...
    # Verified against `git branch -h`: -d/--delete deletes a merged branch, -D
    # deletes regardless, and NO other short option of git branch is spelled d
    # in either case. Short options bundle, so -rd and -dr are the same call.
    # There is no --dry-run and no -n, which is why this runs before the
    # generic Test-DryRun exemption.
    # `--no-delete` is not credited: writing `--delete --no-delete` is not a
    # real invocation, and refusing to reason about it keeps the failure on the
    # deny side.
    foreach ($t in $branchArgs) {
        if (Test-ShortFlag $t 'd') { return $true }
        if (Test-ShortFlag $t 'D') { return $true }
        if (Test-LongOptionPrefix $t 'delete') { return $true }
    }
    return $false
}

function Test-GitTagDelete([string[]]$tagArgs) {
    # git tag -d <tagname>...
    # Verified against `git tag -h`. This subcommand is exactly why the generic
    # dry-run exemption cannot be reused: `-n[<num>]` prints annotation lines,
    # so Test-DryRun reads the bare `-n` of `git tag -n -d v1` as a dry run and
    # would exempt a command that still deletes the tag. git tag has no
    # --dry-run in any form.
    foreach ($t in $tagArgs) {
        if (Test-ShortFlag $t 'd') { return $true }
        if (Test-LongOptionPrefix $t 'delete') { return $true }
    }
    return $false
}

function Test-GitSymbolicRefDelete([string[]]$symArgs) {
    # git symbolic-ref --delete [-q] <name>
    # Verified against `git symbolic-ref -h`: long options are --delete,
    # --quiet, --short, --recurse and --no-recurse, so --d is unambiguous.
    # No dry-run option exists.
    foreach ($t in $symArgs) {
        if (Test-ShortFlag $t 'd') { return $true }
        if (Test-LongOptionPrefix $t 'delete') { return $true }
    }
    return $false
}

function Get-GitUpdateRefDenial([string[]]$refArgs) {
    # git update-ref [<options>] -d <refname> [<old-oid>]
    #   or:          [<options>]    <refname> <new-oid> [<old-oid>]
    #   or:          [<options>] --stdin [-z] [--batch-updates]
    # Verified against `git update-ref -h`. Returns a deny reason, or $null
    # when the call is not a ref deletion.
    #
    # Three option facts drive this parser:
    #   * There is NO --delete long option, and --d/--de are ambiguous with
    #     --deref/--no-deref, so ONLY the short -d spells deletion. Passing
    #     'delete' to Test-LongOptionPrefix here would be wrong.
    #   * -m consumes the next token as the reflog reason, so that token is a
    #     value and never an operand.
    #   * There is no --dry-run and no -n, so the generic exemption must not
    #     reach this subcommand.
    #   * Counting operands is NOT enough. `<refname> <new-oid>` deletes the ref
    #     whenever <new-oid> is the empty string or the all-zero object id, and
    #     both of those are two-operand calls. The new value is inspected.
    $operands = New-Object System.Collections.ArrayList
    $i = 0
    while ($i -lt $refArgs.Count) {
        $t = $refArgs[$i]
        if ($t -eq '--') {
            $i++
            while ($i -lt $refArgs.Count) { [void]$operands.Add($refArgs[$i]); $i++ }
            break
        }
        if ($t -eq '-m') {
            if ($i + 1 -ge $refArgs.Count) {
                return 'git update-ref -m is missing its reason and cannot be classified:'
            }
            $i += 2
            continue
        }
        if (Test-LongOptionPrefix $t 'stdin') {
            return 'git update-ref --stdin carries ref updates this guard cannot read:'
        }
        if ($t -cmatch '^-.') {
            if (Test-ShortFlag $t 'd') {
                return 'git update-ref -d deletes a ref; not authorized during the worktree-retention hold:'
            }
            $i++
            continue
        }
        [void]$operands.Add($t)
        $i++
    }
    if ($operands.Count -lt 2 -or $operands.Count -gt 3) {
        return 'git update-ref operand count matches no documented form; cannot be classified:'
    }
    $newValue = [string]$operands[1]
    if ($newValue.Length -eq 0) {
        # `git update-ref <ref> ""` deletes by writing an empty new value. This
        # position survives only because Split-Segments keeps empty quoted
        # arguments; without that it would look like a two-operand update.
        return 'git update-ref with an empty new value deletes a ref; not authorized during the worktree-retention hold:'
    }
    if ($newValue -cmatch '^0+$') {
        # The all-zero object id is git's deletion sentinel. Only the NEW value
        # position means deletion: an all-zero OLD value is the "must not exist
        # yet" guard on a creation, which is not a deletion.
        return 'git update-ref to the all-zero object id deletes a ref; not authorized during the worktree-retention hold:'
    }
    if ($newValue -match '[$`]') {
        # An unexpanded variable or substitution could be the empty string or
        # the null oid. Unclassifiable, so it denies rather than being guessed.
        return 'git update-ref new value contains an unexpanded expansion and cannot be classified:'
    }
    return $null
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
        if ($t.Length -eq 0) { $i++; continue }
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
        $nested = ''
        if ($flagIndex + 1 -lt $rest.Count) {
            $nested = (@($rest[($flagIndex + 1)..($rest.Count - 1)]) -join ' ')
        }
        # Empty quoted arguments now survive tokenization, so `sh -c ""` arrives
        # as an empty script rather than as a missing one. Both are the same
        # malformed call, and both deny.
        if ([string]::IsNullOrWhiteSpace($nested)) {
            return @{ Kind = 'deny'; Reason = "shell invoked with an empty command argument: $printable" }
        }
        return @{ Kind = 'script'; Script = $nested }
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
        # An empty quoted argument is a real position but never the program, and
        # this segment gets no every-position rescan to recover from it.
        if ($t.Length -eq 0) { $i++; continue }
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
    # Evaluated BEFORE the generic dry-run exemption below, which cannot see
    # negation, flag order, or an option that swallows the next token.
    if ($sub.Name -eq 'worktree' -and $subRest.Count -ge 1 -and $subRest[0] -eq 'prune') {
        $pruneArgs = @()
        if ($subRest.Count -gt 1) { $pruneArgs = @($subRest[1..($subRest.Count - 1)]) }
        if (Test-WorktreePruneDryRun $pruneArgs) { return $null }
        return @{ Decision = 'deny'; Reason = "git worktree prune retires worktree registrations; not authorized during the worktree-cleanup hold: $printable" }
    }
    # --- worktree-retention hold ------------------------------------------
    # These operations are prohibited outright, so they DENY rather than ask:
    # an ask is softened by permission mode and by whoever answers the prompt,
    # and the hold is neither mode-dependent nor profile-dependent.
    #
    # They are classified HERE, above `Test-DryRun`, for the same reason the
    # prune block above is. Test-DryRun matches a bare --dry-run, -n, --whatif
    # or -WhatIf token ANYWHERE in the argument list, and NONE of the
    # subcommands below has a dry-run option at all (checked against
    # `git worktree -h`, `git branch -h`, `git tag -h`, `git update-ref -h`
    # and `git symbolic-ref -h`). Worse, `git tag` gives -n an unrelated
    # meaning, so reusing the generic exemption would wave through
    # `git tag -n -d v1`, which deletes.
    if ($sub.Name -eq 'worktree' -and $subRest.Count -ge 1 -and $subRest[0] -eq 'remove') {
        return @{ Decision = 'deny'; Reason = "git worktree remove retires a worktree registration; not authorized during the worktree-retention hold: $printable" }
    }
    if ($sub.Name -eq 'branch' -and (Test-GitBranchDelete $subRest)) {
        return @{ Decision = 'deny'; Reason = "git branch delete retires a ref; not authorized during the worktree-retention hold: $printable" }
    }
    if ($sub.Name -eq 'tag' -and (Test-GitTagDelete $subRest)) {
        return @{ Decision = 'deny'; Reason = "git tag delete retires a ref; not authorized during the worktree-retention hold: $printable" }
    }
    if ($sub.Name -eq 'symbolic-ref' -and (Test-GitSymbolicRefDelete $subRest)) {
        return @{ Decision = 'deny'; Reason = "git symbolic-ref delete retires a ref; not authorized during the worktree-retention hold: $printable" }
    }
    if ($sub.Name -eq 'update-ref') {
        $updateRefDenial = Get-GitUpdateRefDenial $subRest
        if ($null -ne $updateRefDenial) {
            return @{ Decision = 'deny'; Reason = "$updateRefDenial $printable" }
        }
    }

    if ($sub.Name -eq 'push') {
        # git push HAS a real --dry-run, so unlike the subcommands above it can
        # legitimately be exempted -- but only by its own grammar, and the SAME
        # parse decides deletion and force. Reading intent two different ways is
        # what let `git push --del ...` and `git push -4d ...` through.
        $push = Get-GitPushParse $subRest
        if (-not $push.Parsed) {
            # The guard's contract is "confidently classified, or denied". An
            # option it cannot resolve makes every other verdict here a guess --
            # including whether an operand is a refspec at all -- so it denies
            # rather than falling back to a second, looser reading.
            return @{ Decision = 'deny'; Reason = "git push option '$($push.Unrecognised)' is unknown or ambiguous, so the push cannot be classified: $printable" }
        }
        if ($push.Dry) { return $null }
        if ($push.Delete) {
            return @{ Decision = 'deny'; Reason = "git push delete removes a remote ref; not authorized during the worktree-retention hold: $printable" }
        }
        if ($push.Mirror -or $push.Prune) {
            # Both delete every remote ref with no local counterpart, without
            # naming any of them.
            return @{ Decision = 'deny'; Reason = "git push mirror or prune removes remote refs that have no local counterpart; not authorized during the worktree-retention hold: $printable" }
        }
        if ($push.Force -or $push.ForceWithLease) {
            # Either positive force option blocks, and neither is cancellable.
            return @{ Decision = 'deny'; Reason = "force push rewrites remote history: $printable" }
        }
        # Refspec grammar is [+]<src>:<dst>. Only operand positions are
        # refspecs; an option VALUE that happens to look like one is not.
        foreach ($t in $push.Operands) {
            if ($t -cmatch '^\+?:.+') {
                # The optional force marker sits BEFORE the empty source, so
                # `+:dst` deletes exactly as `:dst` does.
                return @{ Decision = 'deny'; Reason = "empty-source refspec deletes a remote ref: $printable" }
            }
            if ($t -cmatch '^\+[^:]+:') {
                # Same force intent as --force, just spelled in the refspec.
                return @{ Decision = 'deny'; Reason = "leading + in a refspec forces the remote update: $printable" }
            }
        }
        if ($GuardProfile -eq 'agent') {
            return @{ Decision = 'deny'; Reason = "subagents do not push; hand the branch to the owner" }
        }
        return $null
    }

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
        # 'push' is handled above the generic dry-run exemption, because that
        # exemption cannot see negation, ordering, or an option that swallows
        # the next token.
        'merge' {
            if ($GuardProfile -eq 'agent') {
                return @{ Decision = 'deny'; Reason = "subagents do not merge; hand the branch to the owner" }
            }
        }
        # 'branch' and 'worktree remove' are handled above the dry-run
        # exemption, as hard denies. They previously asked; the retention hold
        # is not something a confirmation prompt may waive.
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

    # Literal-output commands still execute $() outside single quotes. Inspect
    # those nested command strings before applying the text-inspection allow rule.
    $outerQuote = [char]0
    for ($position = 0; $position -lt $command.Length; $position++) {
        $character = $command[$position]
        if ($character -eq "'" -and $outerQuote -ne '"') {
            if ($outerQuote -eq "'") { $outerQuote = [char]0 } else { $outerQuote = "'" }
            continue
        }
        if ($character -eq '"' -and $outerQuote -ne "'") {
            if ($outerQuote -eq '"') { $outerQuote = [char]0 } else { $outerQuote = '"' }
            continue
        }
        if ($outerQuote -eq "'" -or $character -ne '$' -or $position + 1 -ge $command.Length -or $command[$position + 1] -ne '(') { continue }
        $level = 1
        $end = $position + 2
        $innerQuote = [char]0
        for (; $end -lt $command.Length; $end++) {
            $inner = $command[$end]
            if ($innerQuote -ne [char]0) { if ($inner -eq $innerQuote) { $innerQuote = [char]0 }; continue }
            if ($inner -eq "'" -or $inner -eq '"') { $innerQuote = $inner; continue }
            if ($inner -eq '(') { $level++ }
            if ($inner -eq ')') { $level--; if ($level -eq 0) { break } }
        }
        if ($level -ne 0) { [void]$script:denials.Add('unbalanced command substitution'); return }
        Invoke-CommandScan $command.Substring($position + 2, $end - $position - 2) ($depth + 1)
        $position = $end
    }

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
    if ($GuardProfile -notin @('agent','main')) { throw 'Unknown guard profile' }
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) {
        [Console]::Error.WriteLine("Guard received no hook payload; failing closed.")
        exit 2
    }
    $payload = $raw | ConvertFrom-Json
    $permissionMode = [string]$payload.permission_mode
    if ($permissionMode -notin @('','default','auto','acceptEdits','plan','dontAsk','bypassPermissions')) { throw 'Unknown permission mode' }
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
        if ([string]::IsNullOrWhiteSpace($permissionMode) -or $permissionMode -in @('auto','bypassPermissions')) {
            [Console]::Error.WriteLine(
                "Blocked by $GuardProfile guard: confirmation is required, but permission mode " +
                "'$permissionMode' has no verified owner confirmation for this guard. Use default mode " +
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
