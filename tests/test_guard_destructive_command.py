"""Regression table for the PreToolUse destructive-command guard.

Two defect classes drove this file, both of which passed an earlier hand-picked
check:

1. Substring regexes leaked. `rm -fr`, `rm -r -f`, a leading space,
   `sudo rm -rf`, `git -C <path> clean -fdx`, `git clean --force -d` and
   `git checkout -fq` all slipped through, while `git merge-base` was blocked
   as if it were `git merge`.
2. The guard ran green under pwsh 7 and was a parser error under Windows
   PowerShell 5.1, which exits 1 -- a non-blocking code, so the production hook
   failed open. The cause was one non-ASCII character in a BOM-less .ps1:
   5.1 decodes such files as CP1252, and the resulting U+201D is a string
   delimiter to PowerShell.

A third incident came from disabling MSYS argument conversion while reading a
Git blob. The guard now denies observable attempts to set or export either
conversion override, without blocking environment inspection or quoted text.

So every case runs against EVERY PowerShell host on the machine, and the source
encoding is asserted directly. `.claude/settings.json` and the agent charters
invoke `powershell`; if that host is present it must be covered.

Outcome vocabulary matches the PreToolUse contract:
  deny  - exit code 2 (the only blocking exit code)
  ask   - exit 0 plus permissionDecision=ask on stdout
  allow - exit 0, no payload

The guard's contract is "confidently classified, or denied". Syntax it cannot
parse -- unbalanced quoting, base64 `-EncodedCommand`, nesting past depth 4 --
denies rather than being guessed at.

Two limitations are deliberate, and are limitations rather than oversights:

* **Script files are not gated.** `bash run.sh` and `powershell -File x.ps1`
  execute contents this guard cannot read. Gating them would break this repo's
  own `scripts/*.ps1` tooling while `python foo.py`, `node x.js` and
  `npm run x` remain equally opaque and equally ungated, so it would buy
  consistency of appearance rather than of protection.
* **Only two shells are modelled.** An ad-hoc parser cannot cover all of Bash
  and PowerShell grammar. It is a speed bump backed by the `deny` list in
  `.claude/settings.json`, not a sandbox, and it should never be described as
  one.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

GUARD = (
    Path(__file__).resolve().parents[1]
    / ".claude"
    / "hooks"
    / "guard-destructive-command.ps1"
)

HOSTS = [name for name in ("powershell", "pwsh") if shutil.which(name)]

pytestmark = pytest.mark.skipif(
    not HOSTS, reason="no PowerShell host available on this platform"
)


def invoke(host: str, payload: str, profile: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            host,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(GUARD),
            "-GuardProfile",
            profile,
        ],
        input=payload,
        capture_output=True,
        text=True,
    )


def outcome(
    host: str,
    command: str,
    profile: str,
    permission_mode: str = "default",
) -> str:
    payload = json.dumps(
        {
            "permission_mode": permission_mode,
            "tool_input": {"command": command},
        }
    )
    proc = invoke(host, payload, profile)
    if proc.returncode == 2:
        return "deny"
    if proc.returncode != 0:
        raise AssertionError(
            f"{host} exited {proc.returncode}; every code except 2 is "
            f"non-blocking, so the guard failed OPEN.\n{proc.stderr}"
        )
    if "permissionDecision" in proc.stdout:
        return json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"]
    return "allow"


# (command, profile, expected outcome)
CASES = [
    # --- recursive force delete: every spelling that has leaked --------------
    ("rm -rf tmp", "main", "deny"),
    ("rm -fr tmp", "main", "deny"),
    ("rm -r -f tmp", "main", "deny"),
    ("rm -Rf tmp", "main", "deny"),
    ("rm -qrf tmp", "main", "deny"),
    ("  rm -rf tmp", "main", "deny"),
    ("sudo rm -rf tmp", "main", "deny"),
    ("sudo -u root rm -rf tmp", "main", "deny"),
    ("env -i rm -rf tmp", "main", "deny"),
    ("FOO=bar rm -rf tmp", "main", "deny"),
    ("cd artifacts && rm -rf tmp", "main", "deny"),
    ("ls\nrm -rf tmp", "main", "deny"),
    ("/bin/rm -rf tmp", "main", "deny"),
    ('"C:\\Program Files\\Git\\usr\\bin\\rm.exe" -rf tmp', "main", "deny"),
    ("rm --recursive --force tmp", "main", "deny"),
    ("Remove-Item .\\wt -Recurse -Force", "main", "deny"),
    ("rm .\\wt -Recurse -Force", "main", "deny"),
    # PowerShell accepts any unambiguous parameter prefix, and switches may
    # carry an explicit value. Both are valid syntax, case-insensitively.
    ("Remove-Item .\\wt -Rec -Fo", "main", "deny"),
    ("Remove-Item .\\wt -Recurse:$true -Force:$true", "main", "deny"),
    ("remove-item .\\wt -rec -fo", "main", "deny"),
    ("Remove-Item .\\wt -R -F", "main", "deny"),
    ("Remove-Item .\\wt -Recurse -Confirm:$false", "main", "deny"),
    ('powershell -Command "Remove-Item .\\wt -Rec -Fo"', "main", "deny"),
    ('pwsh -Command "Remove-Item .\\wt -Recurse:$true -Force:$true"', "main", "deny"),
    # An explicitly disabled switch is not the recursive form.
    ("Remove-Item .\\wt -Recurse:$false -Force", "main", "allow"),
    # --- recursive without force is confirmable ------------------------------
    ("rm -r tmp", "main", "ask"),
    ("Remove-Item .\\wt -Recurse", "main", "ask"),
    ("rmdir build", "main", "ask"),
    # --- ordinary deletes stay out of the way --------------------------------
    ("rm artifacts/baseline.txt", "main", "allow"),
    ("rm -f artifacts/baseline.txt", "main", "allow"),
    ("npm rm --save-dev foo", "main", "allow"),
    ("rm -rf --dry-run tmp", "main", "allow"),
    ("Remove-Item .\\wt -Recurse -WhatIf", "main", "allow"),
    # --- git global options must not hide the subcommand ---------------------
    ("git reset --hard origin/main", "main", "deny"),
    ("git -C ../wt reset --hard", "main", "deny"),
    ("git --no-pager -C ../wt reset --hard", "main", "deny"),
    ("git clean -fdx", "main", "deny"),
    ("git clean -df", "main", "deny"),
    ("git clean --force -d", "main", "deny"),
    ("git -C ../wt clean -fdx", "main", "deny"),
    ("git clean -n", "main", "allow"),
    ("git clean --dry-run", "main", "allow"),
    # --- exact subcommand matching -------------------------------------------
    ("git merge-base main HEAD", "agent", "allow"),
    ("git merge-base main HEAD", "main", "allow"),
    ("git merge origin/main", "agent", "deny"),
    ("git merge --ff-only origin/main", "main", "allow"),
    # --- push: profile-dependent, force always denied ------------------------
    ("git push origin HEAD", "main", "allow"),
    ("git push origin HEAD", "agent", "deny"),
    ("git push --force origin HEAD", "main", "deny"),
    ("git push -f origin HEAD", "main", "deny"),
    ("git push --force-with-lease origin HEAD", "main", "deny"),
    ("git push --delete origin wt/foo", "main", "deny"),
    # --- index and branch surgery is confirmable -----------------------------
    ("git rm -r --cached .idea", "main", "ask"),
    ("git rm --cached --dry-run x", "main", "allow"),
    ("git rm src/foo.py", "main", "ask"),
    ("git worktree list", "main", "allow"),
    # --- worktree prune: denied, with its own option-grammar dry-run parse ---
    ("git worktree prune", "main", "deny"),
    ("git worktree prune", "agent", "deny"),
    ("git worktree prune -n", "main", "allow"),
    ("git worktree prune --dry-run", "main", "allow"),
    ("git worktree prune -nv", "main", "allow"),
    ("git worktree prune -vn", "agent", "allow"),
    # Negation and order: git takes the last flag, so must the guard.
    ("git worktree prune --dry-run --no-dry-run", "main", "deny"),
    ("git worktree prune --no-dry-run --dry-run", "main", "allow"),
    # --expire eats the next token, so this --dry-run is its VALUE, not a flag.
    ("git worktree prune --expire --dry-run", "main", "deny"),
    ("git worktree prune --expire 3.days.ago", "main", "deny"),
    ("git worktree prune --expire=3.days.ago --dry-run", "main", "allow"),
    ("git worktree prune --expire", "main", "deny"),
    ("git worktree prune --verbose", "main", "deny"),
    # Unrecognised option: denied even alongside a real --dry-run.
    ("git worktree prune --dry-run --bogus", "main", "deny"),
    ("git worktree prune -- extra", "main", "deny"),
    ("git worktree prune --dry-run --", "main", "allow"),
    ("git -C /d/development/wt worktree prune", "main", "deny"),
    ("git -C /d/development/wt worktree prune --dry-run", "main", "allow"),
    ("git status && git worktree prune", "main", "deny"),
    ("git worktree prune --dry-run && git worktree prune", "main", "deny"),
    ('sh -c "git worktree prune"', "main", "deny"),
    ("git checkout -fq main", "main", "ask"),
    ("git checkout main", "main", "allow"),
    # --- aggregation: an early ask must never mask a later deny --------------
    ("rm -r a && rm -rf b", "main", "deny"),
    ("git rm file ; git reset --hard HEAD", "main", "deny"),
    ("git branch -D old && git push --force origin main", "main", "deny"),
    ("git worktree remove ../wt && git status", "main", "deny"),
    ("git status && git log --oneline -5", "main", "allow"),
    # --- delegated execution: the nested command must be scanned too ---------
    ('sh -c "rm -rf tmp"', "main", "deny"),
    ("sh -c 'rm -rf tmp'", "main", "deny"),
    ('bash -c "git reset --hard HEAD"', "main", "deny"),
    ('bash -lc "rm -rf tmp"', "main", "deny"),
    ('zsh -c "rm -rf tmp"', "main", "deny"),
    ('cmd /c "rmdir /s /q tmp"', "main", "deny"),
    ('cmd /c "del /f /s /q tmp"', "main", "deny"),
    ('powershell -Command "Remove-Item .\\wt -Recurse -Force"', "main", "deny"),
    ('pwsh -c "Remove-Item .\\wt -Recurse -Force"', "main", "deny"),
    ('eval "rm -rf tmp"', "main", "deny"),
    ("find . -name x | xargs rm -rf", "main", "deny"),
    ("xargs -n1 rm -rf", "main", "deny"),
    ('bash -c "sh -c \'rm -rf tmp\'"', "main", "deny"),
    ('sudo bash -c "rm -rf tmp"', "main", "deny"),
    # base64 cannot be classified, so it cannot be waved through
    ("pwsh -EncodedCommand cgBtACAALQByAGYA", "main", "deny"),
    ("bash -c", "main", "deny"),
    # --- escaped spellings: Bash reads `r\m` as `rm` -------------------------
    ("r\\m -rf tmp", "main", "deny"),
    ("\\rm -rf tmp", "main", "deny"),
    ('"rm" -rf tmp', "main", "deny"),
    # --- command position: the verb is not always token 0 --------------------
    # Each of these is executable syntax that puts a destructive verb behind
    # control structure the guard does not model. Enumerating shell keywords
    # would be an endless list across two grammars, so every position in a
    # segment is evaluated instead.
    ('bash -cl "rm -rf tmp"', "main", "deny"),
    ("xargs -I {} rm -rf {}", "main", "deny"),
    ('powershell -Command "& { Remove-Item .\\wt -Recurse -Force }"', "main", "deny"),
    ('bash -c "if true; then rm -rf tmp; fi"', "main", "deny"),
    ('cmd /c "if exist tmp rmdir /s /q tmp"', "main", "deny"),
    ('pwsh -Command "try { Remove-Item .\\wt -Recurse -Force } catch {}"', "main", "deny"),
    ("$'rm' -rf tmp", "main", "deny"),
    # Line continuation: the shell joins these into `rm`, so joining must happen
    # before the newline is read as a segment break.
    ("r\\\nm -rf tmp", "main", "deny"),
    # --- unclassifiable syntax is denied, never guessed at -------------------
    # Owner ruling: unbalanced or otherwise unclassifiable quoting denies. An
    # earlier revision rescanned and allowed when the rescan found nothing;
    # that traded a real guarantee for convenience.
    ('echo "; rm -rf tmp', "main", "deny"),
    ("echo '; git reset --hard HEAD", "main", "deny"),
    ("echo don't", "main", "deny"),
    # Balanced quoting is still read normally, so ordinary text is unaffected.
    ("git commit -m \"the owner's flow\"", "main", "allow"),
    # --- delegation false positives: these must stay usable ------------------
    ('sh -c "git status"', "main", "allow"),
    ("bash scripts/run.sh", "main", "allow"),
    ("powershell -File scripts/run-pytest.ps1", "main", "allow"),
    ("powershell -NoProfile -ExecutionPolicy Bypass -File scripts/x.ps1", "main", "allow"),
    ("cmd /c dir", "main", "allow"),
    ("xargs -n1 echo", "main", "allow"),
    ("npx playwright test", "main", "allow"),
    # xargs states its own command boundary: `echo` is the executable here and
    # `rm -rf` is data being printed. Applying the every-position rule to this
    # segment would deny a command that deletes nothing.
    ("xargs -n1 echo rm -rf", "main", "allow"),
    ("xargs -I {} echo rm -rf {}", "main", "allow"),
    # ...while the same shapes with rm in command position still deny
    ("xargs -I {} rm -rf {}", "main", "deny"),
    ("xargs -n1 rm -rf", "main", "deny"),
    ("xargs -L 2 rm -rf", "main", "deny"),
    # Optional-argument options take a value only when attached. Written alone
    # the NEXT token is the executable, so consuming it hides the command.
    # Case matters: -I requires a replace-string, its synonym -i does not.
    ("xargs -i rm -rf", "main", "deny"),
    ("xargs -l rm -rf", "main", "deny"),
    ("xargs -e rm -rf", "main", "deny"),
    ("xargs --replace rm -rf", "main", "deny"),
    ("xargs --max-lines rm -rf", "main", "deny"),
    ("xargs --eof rm -rf", "main", "deny"),
    # The matching executable-boundary controls: same options, echo in command
    # position, rm as data. If these deny, the parser ate the wrong token.
    ("xargs -i echo rm -rf", "main", "allow"),
    ("xargs -l echo rm -rf", "main", "allow"),
    ("xargs -e echo rm -rf", "main", "allow"),
    ("xargs --replace echo rm -rf", "main", "allow"),
    ("xargs --max-lines echo rm -rf", "main", "allow"),
    ("xargs --eof echo rm -rf", "main", "allow"),
    # Attached values still bind, and must not leave the executable behind.
    ("xargs -i{} rm -rf {}", "main", "deny"),
    ("xargs --max-lines=2 rm -rf", "main", "deny"),
    ("xargs -i{} echo rm -rf", "main", "allow"),
    # Quoted literals are data, not commands. Pinned so later hardening cannot
    # quietly start denying documentation, search and commit messages.
    ('rg "rm -rf" .', "main", "allow"),
    ('grep -rn "rm -rf" .', "main", "allow"),
    ('Write-Output "rm -rf tmp"', "main", "allow"),
    ('git commit -m "document why rm -rf is denied"', "main", "allow"),
    ('git commit -m "guard: deny rm -rf and git reset --hard"', "main", "allow"),
    # Script-file execution stays ungated by design -- see the module docstring.
    ("bash scripts/new-worktree.sh", "main", "allow"),
    ("pwsh -File scripts/run-playwright.ps1", "main", "allow"),
    # Every-position scanning must not fire on ordinary arguments.
    ("git log --oneline --all -20", "main", "allow"),
    ("gh pr view 188 --json headRefOid", "main", "allow"),
    ("npm run build:css -- --watch", "main", "allow"),
    # --- read-only and build commands are untouched --------------------------
    ("git status --short", "main", "allow"),
    ("git log --oneline -20", "main", "allow"),
    (".venv/Scripts/python.exe -m pytest -q", "main", "allow"),
    ("npm run build:css", "main", "allow"),
    ("gh pr list --state all --limit 20", "main", "allow"),
    # --- worktree-retention hold: prohibited, so deny rather than ask -------
    # These deny in BOTH profiles and in every permission mode; the matrix in
    # test_retention_hold_verdict_is_mode_and_profile_independent pins that.
    # The rows here also pin the option variants and the neighbours that must
    # stay allowed.
    #
    # git worktree remove. `git worktree -h` gives it `[-f] <worktree>` and no
    # dry-run option at all, so the generic Test-DryRun exemption -- which
    # matches a bare --dry-run/-n/--whatif token anywhere -- must not reach it.
    ("git worktree remove ../wt", "main", "deny"),
    ("git worktree remove ../wt", "agent", "deny"),
    ("git worktree remove -f ../wt", "main", "deny"),
    ("git worktree remove --force ../wt", "main", "deny"),
    # Bare form: exactly one token after the subcommand, which is where a
    # single-element array unrolls to a scalar string and $rest[0] becomes 'r'.
    ("git worktree remove", "main", "deny"),
    ("git -C ../wt worktree remove ../wt", "main", "deny"),
    ("git worktree remove -n ../wt", "main", "deny"),
    ("git worktree remove --dry-run ../wt", "main", "deny"),
    ("git worktree remove ../wt --whatif", "main", "deny"),
    ("git worktree add ../wt -b feat origin/main", "main", "allow"),
    ("git worktree repair", "main", "allow"),
    #
    # Branch deletion. -d and -D both delete, short options bundle, and git's
    # parse-opt accepts any unambiguous abbreviation of --delete.
    ("git branch -d wt/foo", "main", "deny"),
    ("git branch -d wt/foo", "agent", "deny"),
    ("git branch -D wt/foo", "main", "deny"),
    ("git branch --delete wt/foo", "main", "deny"),
    ("git branch --delete --force wt/foo", "main", "deny"),
    ("git branch -rd origin/wt/foo", "main", "deny"),
    ("git branch -dr origin/wt/foo", "main", "deny"),
    ("git branch -rD origin/wt/foo", "main", "deny"),
    ("git branch --del wt/foo", "main", "deny"),
    ("git branch --d wt/foo", "main", "deny"),
    # git branch has no -n and no --dry-run, so neither token exempts anything.
    ("git branch -d -n wt/foo", "main", "deny"),
    ("git branch --delete --dry-run wt/foo", "main", "deny"),
    ("git -C ../wt branch -D wt/foo", "main", "deny"),
    # Listing, renaming, copying and creating are untouched.
    ("git branch", "main", "allow"),
    ("git branch -a", "main", "allow"),
    ("git branch -vv", "main", "allow"),
    ("git branch --show-current", "main", "allow"),
    ("git branch --list wt/*", "main", "allow"),
    ("git branch --merged origin/main", "main", "allow"),
    ("git branch --no-merged origin/main", "main", "allow"),
    ("git branch --sort=-committerdate", "main", "allow"),
    ("git branch --format=%(refname)", "main", "allow"),
    ("git branch --contains HEAD", "main", "allow"),
    ("git branch -m old new", "main", "allow"),
    ("git branch -c old copy", "main", "allow"),
    ("git branch feat origin/main", "main", "allow"),
    #
    # Tag deletion. This subcommand is the reason the generic dry-run exemption
    # cannot be reused: `-n[<num>]` is git tag's annotation-line count, so
    # Test-DryRun reads the bare -n of `git tag -n -d v1` as a dry run and would
    # wave through a command that still deletes the tag.
    ("git tag -d v1", "main", "deny"),
    ("git tag -d v1", "agent", "deny"),
    ("git tag --delete v1", "main", "deny"),
    ("git tag --del v1", "main", "deny"),
    ("git tag -n -d v1", "main", "deny"),
    ("git tag -d -n v1", "main", "deny"),
    ("git tag --dry-run -d v1", "main", "deny"),
    ("git tag", "main", "allow"),
    ("git tag -l v1*", "main", "allow"),
    ("git tag -n5 -l", "main", "allow"),
    ("git tag -a v1 -m release", "main", "allow"),
    ("git tag --points-at HEAD", "main", "allow"),
    ("git tag --column", "main", "allow"),
    ("git tag -v v1", "main", "allow"),
    #
    # update-ref deletion. There is NO --delete long option here, and --d/--de
    # are ambiguous with --deref/--no-deref, so only the short -d spells
    # deletion -- which is why this subcommand does not share the long-option
    # prefix helper. --stdin carries updates the guard cannot read, so it denies
    # as unclassifiable rather than being guessed at.
    ("git update-ref -d refs/heads/wt/foo", "main", "deny"),
    ("git update-ref -d refs/heads/wt/foo", "agent", "deny"),
    ("git update-ref -d refs/heads/wt/foo abc123", "main", "deny"),
    ("git update-ref -dz refs/heads/wt/foo", "main", "deny"),
    ("git update-ref --stdin", "main", "deny"),
    ("git update-ref --stdin -z", "main", "deny"),
    ("git update-ref --s", "main", "deny"),
    ("git update-ref -m reason -d refs/heads/wt/foo", "main", "deny"),
    # `git update-ref <ref> ""` deletes by writing an empty new value. The
    # tokenizer preserves the empty quoted argument so the new-value deletion
    # cannot be mistaken for an ordinary update.
    ('git update-ref refs/heads/wt/foo ""', "main", "deny"),
    ("git update-ref -d -n refs/heads/wt/foo", "main", "deny"),
    ("git update-ref --dry-run -d refs/heads/wt/foo", "main", "deny"),
    # -m consumes the next token as the reflog reason, so it is never an
    # operand; these are ordinary two- and three-operand updates.
    ("git update-ref refs/archive/wt-foo abc123", "main", "allow"),
    ("git update-ref --no-deref refs/archive/x abc123", "main", "allow"),
    ("git update-ref -m archive refs/archive/x abc123 def456", "main", "allow"),
    #
    # symbolic-ref deletion.
    ("git symbolic-ref -d refs/heads/x", "main", "deny"),
    ("git symbolic-ref --delete refs/heads/x", "main", "deny"),
    ("git symbolic-ref --d refs/heads/x", "main", "deny"),
    ("git symbolic-ref HEAD", "main", "allow"),
    ("git symbolic-ref -q --short HEAD", "main", "allow"),
    #
    # A refspec with an empty source deletes the remote ref, which the existing
    # --delete check does not cover. A source-bearing colon refspec is an
    # ordinary push and keeps the pre-existing per-profile verdict.
    ("git push origin :wt/foo", "main", "deny"),
    ("git push origin :refs/heads/wt/foo", "main", "deny"),
    ("git push origin HEAD:refs/heads/feat", "main", "allow"),
    ("git push origin HEAD:refs/heads/feat", "agent", "deny"),
    #
    # Chaining and delegation: an allow or an ask must never mask the deny.
    ("git status && git worktree remove ../wt", "main", "deny"),
    ("git worktree remove ../wt && git status", "agent", "deny"),
    ("git branch -d a; git branch -d b", "main", "deny"),
    ("git log --oneline | head -5 && git tag -d v1", "main", "deny"),
    ("git rm src/foo.py && git branch -D old", "main", "deny"),
    ('sh -c "git worktree remove ../wt"', "main", "deny"),
    ('bash -lc "git branch -D wt/foo"', "main", "deny"),
    ('cmd /c "git update-ref -d refs/heads/x"', "main", "deny"),
    ("xargs -I {} git branch -D {}", "main", "deny"),
    ('bash -c "sh -c \'git tag -d v1\'"', "main", "deny"),
    ("git\\ branch -D wt/foo", "main", "deny"),
    ("git for-each-ref refs/heads", "main", "allow"),
    # --- rev 2: option values, negation and ordering in the push dry-run ---
    # Test-DryRun matches a bare --dry-run/-n token anywhere in the list, so
    # every command in this first group was exempted while still deleting a
    # remote ref. git push is parsed by its own grammar now
    # (Get-GitPushParse), which is also why the genuine dry runs below still
    # allow.
    ("git push --dry-run --no-dry-run origin :refs/heads/wt-example", "main", "deny"),
    ("git push -n --no-dry-run origin :refs/heads/wt-example", "main", "deny"),
    ("git push --dry-run --no-dry-run origin +:refs/heads/wt-example", "main", "deny"),
    ("git push --dry-run --no-dry-run --force origin main", "main", "deny"),
    # -o, --repo and --push-option consume the FOLLOWING token, so the
    # --dry-run in each of these is a value and the push is real.
    ("git push -o --dry-run origin :refs/heads/wt-example", "main", "deny"),
    ("git push --repo --dry-run origin :refs/heads/wt-example", "main", "deny"),
    ("git push -vo --dry-run origin :refs/heads/wt-example", "main", "deny"),
    ("git push --push-option --dry-run origin +:refs/heads/wt-example", "main", "deny"),
    # An unrecognised push option makes classification uncertain, so the whole
    # command denies without a dry-run exemption or a fallback operand scan.
    ("git push --bogus --dry-run origin :refs/heads/wt-example", "main", "deny"),
    # The refspec grammar is [+]<src>:<dst>. The optional force marker sits
    # BEFORE the empty source, so +:dst deletes exactly as :dst does.
    ("git push origin +:refs/heads/wt-example", "main", "deny"),
    ("git push origin +:refs/heads/wt-example", "agent", "deny"),
    # Proven dry runs stay allowed, including across an option value.
    ("git push --dry-run origin :refs/heads/wt-example", "main", "allow"),
    ("git push --dry-run origin :refs/heads/wt-example", "agent", "allow"),
    ("git push -n origin :refs/heads/wt-example", "main", "allow"),
    ("git push --no-dry-run --dry-run origin :refs/heads/wt-example", "main", "allow"),
    ("git push -o ci.skip --dry-run origin :refs/heads/wt-example", "main", "allow"),
    ("git push --repo upstream --dry-run origin :refs/heads/wt-example", "main", "allow"),
    ("git push -vn origin :refs/heads/wt-example", "main", "allow"),
    ("git push --recurse-submodules=no --dry-run origin :refs/x", "main", "allow"),
    # Ordinary pushes are untouched. (A source-bearing + refspec is NOT one:
    # rev 3 treats it as the force intent it is. See the rev-3 block below.)
    ("git push -o ci.skip origin HEAD", "main", "allow"),
    ("git push --repo upstream origin HEAD", "main", "allow"),
    ("git push --set-upstream origin feat", "main", "allow"),
    ("git push --tags origin", "main", "allow"),
    ("git push -4 origin HEAD", "main", "allow"),
    ("git push --signed=if-asked origin HEAD", "main", "allow"),
    #
    # --- rev 2: update-ref deletes by VALUE, not only by operand count ------
    # `<refname> <new-oid>` deletes whenever the new value is the empty string
    # or the all-zero object id, and both of those are two-operand calls.
    ('git update-ref refs/heads/wt-example "" 1111111111111111111111111111111111111111', "main", "deny"),
    ('git update-ref refs/heads/wt-example ""', "main", "deny"),
    ("git update-ref refs/heads/wt-example 0000000000000000000000000000000000000000", "main", "deny"),
    ("git update-ref refs/heads/wt-example 0000000000000000000000000000000000000000", "agent", "deny"),
    ("git update-ref refs/heads/wt-example 0000000000000000000000000000000000000000 1111111111111111111111111111111111111111", "main", "deny"),
    ("git update-ref -m retire refs/heads/wt-example 0000000000000000000000000000000000000000", "main", "deny"),
    ("git update-ref refs/heads/wt-example 0", "main", "deny"),
    ("git update-ref -- refs/heads/wt-example 0000000000000000000000000000000000000000", "main", "deny"),
    # An unexpanded expansion could be the empty string or the null oid, so it
    # cannot be classified and denies.
    ("git update-ref refs/heads/wt-example $SHA", "main", "deny"),
    # No documented form takes four operands.
    ("git update-ref refs/heads/wt-example 1111111111111111111111111111111111111111 1111111111111111111111111111111111111111 extra", "main", "deny"),
    # The empty position has to survive delegation and chaining too.
    ('sh -c \'git update-ref refs/heads/wt-example "" 1111111111111111111111111111111111111111\'', "main", "deny"),
    ("git status && git update-ref refs/heads/wt-example 0000000000000000000000000000000000000000", "main", "deny"),
    # An all-zero OLD value is the "must not exist yet" guard on a creation.
    # Only the NEW value position means deletion.
    ("git update-ref refs/archive/wt-foo 1111111111111111111111111111111111111111 0000000000000000000000000000000000000000", "main", "allow"),
    ("git update-ref refs/archive/wt-foo 1111111111111111111111111111111111111111", "main", "allow"),
    ("git update-ref refs/archive/wt-foo 0abc123", "main", "allow"),
    ("git update-ref -m archive refs/archive/x 1111111111111111111111111111111111111111 1111111111111111111111111111111111111111", "main", "allow"),
    #
    # --- rev 2: empty argument positions survive tokenization ---------------
    # Dropping an empty quoted argument is what made the update-ref deletion
    # above read as an ordinary two-operand update. Preserving it must not
    # disturb anything else, and an empty token is never an executable.
    ('rm -rf ""', "main", "deny"),
    ('xargs "" rm -rf', "main", "deny"),
    ('git "" branch -D wt/foo', "main", "deny"),
    # An absent command argument and an explicitly empty one are the same
    # malformed call.
    ('sh -c ""', "main", "deny"),
    ('git status ""', "main", "allow"),
    ('echo ""', "main", "allow"),
    ('git commit -m ""', "main", "allow"),
    # --- rev 3: ONE reading of the push option list ------------------------
    # rev 2 kept three readings of the same argument list alive: the grammar
    # parser reported only dry-run, while deletion and force were judged by an
    # exact-string / Test-ShortFlag scan, and refspecs came from operands or
    # from every token depending on whether the parse succeeded. Both of the
    # next two commands really delete a remote ref and both used to allow.
    ("git push --del origin wt-example", "main", "deny"),
    ("git push --del origin wt-example", "agent", "deny"),
    ("git push -4d origin wt-example", "main", "deny"),
    ("git push -4d origin wt-example", "agent", "deny"),
    # --del is an unambiguous parse-opt abbreviation, which an exact-string test
    # for '--delete' misses. -4d is a cluster containing a digit, which
    # Test-ShortFlag's ^-[a-zA-Z]+$ rejects outright, hiding the -d.
    ("git push --de origin wt-example", "main", "deny"),
    ("git push -d origin wt-example", "main", "deny"),
    ("git push -6d origin wt-example", "main", "deny"),
    ("git push -fd origin wt-example", "main", "deny"),
    ("git push -df origin wt-example", "main", "deny"),
    # --mirror and --prune delete every remote ref with no local counterpart,
    # without naming any of them.
    ("git push --mirror origin", "main", "deny"),
    ("git push --mir origin", "main", "deny"),
    ("git push --prune origin main", "main", "deny"),
    # Same force intent as --force, spelled in the refspec instead.
    ("git push origin +refs/heads/a:refs/heads/b", "main", "deny"),
    ("git push --for origin main", "main", "deny"),
    # Ambiguous abbreviations: git rejects these too. --d matches delete and
    # dry-run; --f matches force, force-with-lease, force-if-includes and
    # follow-tags. An option the guard cannot resolve makes every other verdict
    # a guess, so the push is denied rather than read a second, looser way.
    ("git push --d origin wt-example", "main", "deny"),
    ("git push --f origin main", "main", "deny"),
    ("git push --bogus origin HEAD", "main", "deny"),
    ("git push -x origin HEAD", "main", "deny"),
    # An option missing its required value is equally unclassifiable.
    ("git push -o", "main", "deny"),
    ("git push --repo", "main", "deny"),
    #
    # --- rev 3 safe neighbours ---------------------------------------------
    # Negation is honoured for DELETE, because git takes the last spelling of
    # an option and a cancelled delete removes nothing. Force is deliberately
    # not negatable -- see the rev-4 block below.
    ("git push --no-del origin wt-example", "main", "allow"),
    ("git push --delete --no-delete origin wt-example", "main", "allow"),
    ("git push -d --no-delete origin wt-example", "main", "allow"),
    # A dry run performs nothing, so it is checked before the deletion intent.
    ("git push -nd origin wt-example", "main", "allow"),
    ("git push --del --dry-run origin wt-example", "main", "allow"),
    ("git push --dry origin :refs/x", "main", "allow"),
    # A refspec without the leading + is an ordinary update.
    ("git push origin refs/heads/a:refs/heads/b", "main", "allow"),
    # Ordinary options must not be swept up by the digit-aware cluster parser
    # or by the prefix resolver.
    ("git push -4 origin HEAD", "main", "allow"),
    ("git push -6 origin HEAD", "main", "allow"),
    ("git push -u origin feat", "main", "allow"),
    ("git push -qv origin HEAD", "main", "allow"),
    ("git push --thin origin HEAD", "main", "allow"),
    ("git push --atomic origin HEAD", "main", "allow"),
    ("git push --follow-tags origin HEAD", "main", "allow"),
    ("git push --no-verify origin HEAD", "main", "allow"),
    ("git push --porcelain origin HEAD", "main", "allow"),
    # --force-if-includes is a safety CONDITION on --force-with-lease, not a
    # force in its own right.
    ("git push --force-if-includes origin HEAD", "main", "allow"),
    ("git push --exec /usr/bin/git-receive-pack origin HEAD", "main", "allow"),
    ("git push --receive-pack=/usr/bin/grp origin HEAD", "main", "allow"),
    ("git push --no-mirror origin HEAD", "main", "allow"),
    ("git push --no-prune origin HEAD", "main", "allow"),
    #
    # --- rev 4: --force and --force-with-lease are separate options ---------
    # rev 3 recorded both in ONE Boolean, so each option's --no- form cancelled
    # the OTHER one. Both of the next two really force-push, and both allowed.
    ("git push --force --no-force-with-lease origin wt-example", "main", "deny"),
    ("git push --force-with-lease --no-force origin wt-example", "main", "deny"),
    ("git push --force --no-force-with-lease origin wt-example", "agent", "deny"),
    ("git push --force-with-lease --no-force origin wt-example", "agent", "deny"),
    # Reversed ordering -- the negation first, the positive option second --
    # denied under rev 3 as well, which is exactly why the defect was not
    # visible from one ordering alone.
    ("git push --no-force-with-lease --force origin wt-example", "main", "deny"),
    ("git push --no-force --force-with-lease origin wt-example", "main", "deny"),
    # A positive force option is LATCHED: no later negation clears it, not even
    # its own. This matches the live guard, which scans for --force,
    # --force-with-lease* and -f with no notion of negation at all. Honouring
    # the negation would loosen the guard during the retention hold.
    ("git push --force --no-force origin main", "main", "deny"),
    ("git push --force-with-lease --no-force-with-lease origin main", "main", "deny"),
    ("git push -f --no-force origin main", "main", "deny"),
    ("git push --force-with-lease=origin/main --no-force origin main", "main", "deny"),
    # Spellings are resolved by the same unified parser, so an unambiguous
    # abbreviation and a short flag latch exactly as the full spelling does.
    ("git push --force-w --no-force origin main", "main", "deny"),
    ("git push --force --no-force-w origin main", "main", "deny"),
    ("git push -qf --no-force-with-lease origin main", "main", "deny"),
    # --for is ambiguous between force, force-with-lease and force-if-includes,
    # so it denies as unclassifiable rather than as a latched force. Either way
    # a negation cannot rescue it.
    ("git push --for --no-force-with-lease origin main", "main", "deny"),
    # A PROVEN dry run performs nothing and stays exempt, force or not, in
    # either order. The push block reads Dry before it reads force.
    ("git push --dry-run --force --no-force-with-lease origin wt-example", "main", "allow"),
    ("git push --force-with-lease --no-force --dry-run origin wt-example", "main", "allow"),
    ("git push --force --dry-run origin main", "main", "allow"),
    ("git push -n -f origin main", "main", "allow"),
    ("git push -nf origin main", "main", "allow"),
    # A CANCELLED dry run is not a dry run, and the force behind it still
    # blocks. Dry-run negation is honoured; force negation is not.
    ("git push --dry-run --no-dry-run --force-with-lease origin main", "main", "deny"),
    # Ordinary pushes are untouched, including a bare negation with no force to
    # cancel and the safety CONDITION that is not a force in its own right.
    ("git push --no-force origin HEAD", "main", "allow"),
    ("git push --no-force-with-lease origin HEAD", "main", "allow"),
    ("git push --no-force --no-force-with-lease origin HEAD", "main", "allow"),
    ("git push --force-if-includes --no-force origin HEAD", "main", "allow"),
    ("git push --set-upstream origin feat", "main", "allow"),
    ("git push origin refs/heads/a:refs/heads/b", "main", "allow"),
    ("gh pr checks 188", "main", "allow"),

    ('MSYS_NO_PATHCONV=1 git status', 'main', 'deny'),
    ('msys_no_pathconv=1 git status', 'main', 'deny'),
    ('MSYS2_ARG_CONV_EXCL=* git status', 'main', 'deny'),
    ('FOO=bar MSYS_NO_PATHCONV=1 git status', 'main', 'deny'),
    ('env MSYS_NO_PATHCONV=1 git status', 'main', 'deny'),
    ('sudo env -i MSYS2_ARG_CONV_EXCL=* git status', 'main', 'deny'),
    ('export MSYS_NO_PATHCONV=1', 'main', 'deny'),
    ('export msys2_arg_conv_excl', 'main', 'deny'),
    ('set MSYS_NO_PATHCONV=1', 'main', 'deny'),
    ('cmd /c "set MSYS2_ARG_CONV_EXCL=*"', 'main', 'deny'),
    ("$env:MSYS_NO_PATHCONV = '1'", 'main', 'deny'),
    ("${env:msys2_arg_conv_excl}='*'", 'main', 'deny'),
    ('Set-Item Env:MSYS_NO_PATHCONV 1', 'main', 'deny'),
    ("New-Item -Path Env:MSYS2_ARG_CONV_EXCL -Value '*'", 'main', 'deny'),
    ("[Environment]::SetEnvironmentVariable('MSYS_NO_PATHCONV','1','Process')", 'main', 'deny'),
    ("[System.Environment]::SetEnvironmentVariable('msys2_arg_conv_excl','*','User')", 'main', 'deny'),
    ('setx MSYS_NO_PATHCONV 1', 'main', 'deny'),
    ('setx /M msys2_arg_conv_excl *', 'main', 'deny'),
    ('git status && MSYS_NO_PATHCONV=1 git show HEAD:file', 'main', 'deny'),
    ('bash -c "export MSYS2_ARG_CONV_EXCL=*; git status"', 'main', 'deny'),
    ('pwsh -Command "$env:MSYS_NO_PATHCONV=1; git status"', 'main', 'deny'),
    ('echo $MSYS_NO_PATHCONV', 'main', 'allow'),
    ('printenv MSYS2_ARG_CONV_EXCL', 'main', 'allow'),
    ('Get-Item Env:MSYS_NO_PATHCONV', 'main', 'allow'),
    ("[Environment]::GetEnvironmentVariable('MSYS2_ARG_CONV_EXCL','Machine')", 'main', 'allow'),
    ('cmd /c "set MSYS_NO_PATHCONV"', 'main', 'allow'),
    ('rg "MSYS_NO_PATHCONV=1" .', 'main', 'allow'),
    ('Write-Output "export MSYS2_ARG_CONV_EXCL=*"', 'main', 'allow'),
    ('git commit -m "never set MSYS_NO_PATHCONV=1"', 'main', 'allow'),
    ('export -p MSYS_NO_PATHCONV', 'main', 'allow'),
    ('env -u MSYS2_ARG_CONV_EXCL git status', 'main', 'allow'),
]


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize(
    "command,profile,expected",
    CASES,
    ids=[f"{p}:{c}" for c, p, _ in CASES],
)
def test_guard_outcome(host: str, command: str, profile: str, expected: str) -> None:
    assert outcome(host, command, profile) == expected


# Malformed or unrecognised payloads must fail CLOSED: any exit code other than
# 2 is non-blocking, so "I could not parse this" has to mean "block".
MALFORMED = [
    ("not json", "{not json"),
    ("empty stdin", ""),
    ("empty object", "{}"),
    ("no tool_input", '{"tool_name":"Bash"}'),
    ("empty tool_input", '{"tool_input":{}}'),
    ("no command field", '{"tool_input":{"description":"rm -rf tmp"}}'),
]


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("label,payload", MALFORMED, ids=[m[0] for m in MALFORMED])
def test_guard_fails_closed(host: str, label: str, payload: str) -> None:
    assert invoke(host, payload, "main").returncode == 2


@pytest.mark.parametrize("host", HOSTS)
def test_unknown_command_field_is_still_inspected(host: str) -> None:
    """A renamed command field must not slip past unexamined."""
    payload = json.dumps(
        {
            "permission_mode": "default",
            "tool_input": {"shellCommand": "rm -rf tmp"},
        }
    )
    assert invoke(host, payload, "main").returncode == 2


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize(
    "command,expected",
    [
        ("MSYS_NO_PATHCONV=1 git status", "deny"),
        ("setx MSYS2_ARG_CONV_EXCL *", "deny"),
        ("git worktree remove ../wt", "deny"),
        ("git rm src/foo.py", "deny"),
        ("rm -r tmp", "deny"),
        ("rm -rf tmp", "deny"),
        ("git status --short", "allow"),
    ],
)
def test_bypass_mode_never_silently_executes_confirmation_tier(
    host: str,
    command: str,
    expected: str,
) -> None:
    """bypassPermissions skips prompts, so ask-tier operations must hard-deny."""
    assert outcome(host, command, "main", "bypassPermissions") == expected


@pytest.mark.parametrize("host", HOSTS)
def test_missing_permission_mode_denies_confirmation_tier(host: str) -> None:
    """Unknown permission semantics are unsafe for a command requiring approval."""
    payload = json.dumps({"tool_input": {"command": "git rm src/foo.py"}})
    assert invoke(host, payload, "main").returncode == 2


RETENTION_HOLD = [
    ("git worktree remove ../wt", "deny"),
    ("git worktree prune", "deny"),
    ("git branch -D wt/foo", "deny"),
    ("git branch --delete wt/foo", "deny"),
    ("git tag -d v1", "deny"),
    ("git update-ref -d refs/heads/wt/foo", "deny"),
    ("git symbolic-ref --delete refs/heads/x", "deny"),
    ("git push origin :wt/foo", "deny"),
    ("git push origin +:refs/heads/wt-example", "deny"),
    ("git push --dry-run --no-dry-run origin :wt/foo", "deny"),
    ("git update-ref refs/heads/wt-example 0000000000000000000000000000000000000000", "deny"),
    ("git push --del origin wt-example", "deny"),
    ("git push -4d origin wt-example", "deny"),
    # xargs re-opens the argument list, so push and prune dry-run proofs are no
    # more trustworthy than git rm's was. Head position and behind control
    # syntax both reach the flag, by two different routes through the scan.
    ("echo --no-dry-run | xargs git push --dry-run origin :wt/foo", "deny"),
    ("echo --no-dry-run | xargs git worktree prune --dry-run", "deny"),
    ("echo --no-dry-run | { xargs git push --dry-run origin :wt/foo; }", "deny"),
    ("if true; then xargs git worktree prune --dry-run; fi", "deny"),
    # The neighbours must stay reachable under every mode too, or the hold
    # would be indistinguishable from a guard that simply blocks git.
    ("git worktree list", "allow"),
    ("git branch --show-current", "allow"),
    ("git tag -l v1*", "allow"),
    ("git update-ref refs/archive/x abc123", "allow"),
    ("git push --dry-run origin :wt/foo", "allow"),
]


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ["main", "agent"])
@pytest.mark.parametrize(
    "mode",
    ["", "default", "auto", "acceptEdits", "plan", "dontAsk", "bypassPermissions"],
)
@pytest.mark.parametrize(
    "command,expected",
    RETENTION_HOLD,
    ids=[c for c, _ in RETENTION_HOLD],
)
def test_retention_hold_verdict_is_mode_and_profile_independent(
    host: str,
    profile: str,
    mode: str,
    command: str,
    expected: str,
) -> None:
    """Retention denial and safe neighbors are invariant across profiles and modes."""
    assert outcome(host, command, profile, mode) == expected, context(command, profile, mode)


# (command, reason fragment). The verdict rows above prove these deny; these
# prove they deny for the RIGHT rule, which a bare verdict cannot show.
XARGS_VOIDS_DRY_RUN_PROOF = [
    ("echo --no-dry-run | xargs git push --dry-run origin :wt/foo",
     "empty-source refspec deletes a remote ref"),
    ("echo --no-dry-run | { xargs git push --dry-run origin :wt/foo; }",
     "empty-source refspec deletes a remote ref"),
    ("echo --no-dry-run | xargs git worktree prune --dry-run",
     "git worktree prune retires worktree registrations"),
    ("if true; then xargs git worktree prune --dry-run; fi",
     "git worktree prune retires worktree registrations"),
]


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize(
    "command,reason",
    XARGS_VOIDS_DRY_RUN_PROOF,
    ids=[c for c, _ in XARGS_VOIDS_DRY_RUN_PROOF],
)
def test_xargs_voids_push_and_prune_dry_run_proof(host, command, reason):
    for profile in ("main", "agent"):
        proc = invoke_mode(host, command, profile, "default")
        where = context(command, profile, "default")
        assert proc.returncode == 2, f"{where}: {proc.stdout}{proc.stderr}"
        assert not proc.stdout, f"{where}: {proc.stdout}"
        assert proc.stderr.startswith(f"Blocked by {profile} guard:"), f"{where}: {proc.stderr}"
        assert reason in proc.stderr, f"{where}: {proc.stderr}"
        assert "failing closed" not in proc.stderr, f"{where}: {proc.stderr}"


# An open argument list does not make every push a retention deny -- HEAD:main
# names no ref to delete. What it must do is stop the dry-run proof from
# skipping the agent push deny, which sits BELOW it in the same branch.
XARGS_PUSH_PROFILE_SPLIT = [
    "echo --no-dry-run | xargs git push --dry-run origin HEAD:main",
    "echo --no-dry-run | { xargs git push --dry-run origin HEAD:main; }",
]


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize(
    "mode",
    ["", "default", "auto", "acceptEdits", "plan", "dontAsk", "bypassPermissions"],
)
@pytest.mark.parametrize("command", XARGS_PUSH_PROFILE_SPLIT)
def test_xargs_open_arguments_keep_profile_push_policy(host, mode, command):
    assert outcome(host, command, "main", mode) == "allow", context(command, "main", mode)
    proc = invoke_mode(host, command, "agent", mode)
    where = context(command, "agent", mode)
    assert proc.returncode == 2, f"{where}: {proc.stdout}{proc.stderr}"
    assert proc.stderr.startswith("Blocked by agent guard:"), f"{where}: {proc.stderr}"
    assert "subagents do not push" in proc.stderr, f"{where}: {proc.stderr}"


# The flag is a property of ONE segment. A future change that made it
# command-wide would silently deny these, and no other row would notice.
XARGS_SEGMENT_SCOPE = [
    "find . | xargs echo hi; git push --dry-run origin :wt/foo",
    "find . | xargs echo hi; git worktree prune --dry-run",
]


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("command", XARGS_SEGMENT_SCOPE)
def test_xargs_open_arguments_are_scoped_to_one_segment(host, command):
    for profile in ("main", "agent"):
        assert outcome(host, command, profile, "default") == "allow", context(command, profile, "default")


HOOK_SCRIPTS = sorted((GUARD.parent).glob("*.ps1"))

# Historical incident-shaped commands are DATA passed to the hook; none is executed.
SUPPRESSION_FORMS = [
    "{name}=1 npx example --output /c/incident",
    "export {name}=0",
    "export {name}",
    "env {name}=* gh example",
    'cmd /c "set {name}=0 && echo inert"',
    "$env:{name} = '0'",
    "Set-Item Env:{name} '0'",
    "Set-Content Env:{name} '0'",
    "[Environment]::SetEnvironmentVariable('{name}','0','Process')",
    "[System.Environment]::SetEnvironmentVariable('{name}','0','User')",
    "setx {name} 0",
    "git status; {name}=0 echo inert",
    "git status\nexport {name}=0",
    "bash -c 'export {name}=0; echo inert'",
    'powershell -Command "$env:{name}=0"',
    'cmd /c "set /a {name}=1"',
    r"Set-Item -Path Env:\{name} -Value 1",
    "export -n {name}=1",
    'echo "$(export {name}=1)"',
    "$env:{name}++",
    "++$env:{name}",
    "$env:{name}--",
    "--$env:{name}",
    'cmd /c "set /a {name} += 1"',
    'cmd /c "set /a harmless=0,{name}=1"',
]
SUPPRESSION_FORMS += [f"$env:{{name}} {operator} '1'" for operator in ("+=", "-=", "*=", "/=", "%=", "??=")]
SUPPRESSION_FORMS += [f'cmd /c "set /a {{name}}{operator}1"' for operator in
                      ("+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=")]


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ("main", "agent"))
@pytest.mark.parametrize("permission", ("default", "auto", "bypassPermissions"))
@pytest.mark.parametrize("name", ("MSYS_NO_PATHCONV", "MSYS2_ARG_CONV_EXCL"))
def test_suppression_forms_are_profile_and_permission_invariant(host, profile, permission, name):
    for template in SUPPRESSION_FORMS:
        command = template.format(name=name)
        assert outcome(host, command, profile, permission) == "deny", command


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ("main", "agent"))
@pytest.mark.parametrize("permission", ("default", "auto", "bypassPermissions"))
def test_safe_native_and_full_blob_controls_allow(host, profile, permission):
    for command in (r"npx playwright test --output D:\scratch\results", "git status --short",
                    "git ls-tree -z HEAD -- scripts/new-worktree.ps1",
                    "git cat-file blob " + "a" * 40,
                    "Write-Output 'MSYS_NO_PATHCONV=1'", "rg 'export MSYS_NO_PATHCONV' .",
                    "git commit -m 'Document MSYS_NO_PATHCONV=1 as historical input'"):
        assert outcome(host, command, profile, permission) == "allow", command


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ("main", "agent"))
def test_unknown_permission_semantics_cannot_approve_confirmation_tier(host, profile):
    assert outcome(host, "git rm retained", profile, "futureUnknownMode") == "deny"


@pytest.mark.parametrize("host", HOSTS)
def test_denied_payload_never_executes_its_child(host, tmp_path):
    sentinel = tmp_path / "child-was-executed"
    command = "$env:MSYS_NO_PATHCONV='0'; Set-Content -LiteralPath '" + str(sentinel) + "' -Value BAD"
    assert outcome(host, command, "main", "bypassPermissions") == "deny"
    assert not sentinel.exists()


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ("main", "agent"))
def test_internal_error_inputs_exit_exactly_two_under_every_profile(host, profile):
    for payload in ("", "{invalid", "{}", '{"permission_mode":"default","tool_input":{}}',
                    '{"permission_mode":"bypassPermissions","tool_input":{"command":"echo unterminated\'"}}'):
        assert invoke(host, payload, profile).returncode == 2


@pytest.mark.parametrize("script", HOOK_SCRIPTS, ids=lambda p: p.name)
def test_hook_source_is_ascii_with_bom(script: Path) -> None:
    """Windows PowerShell 5.1 reads a BOM-less .ps1 as CP1252.

    A single UTF-8 em dash then decodes to U+201D, which PowerShell treats as a
    string delimiter: the guard becomes a parser error and exits 1. Exit 1 is
    non-blocking, so the hook fails OPEN while appearing installed. Every hook
    in this directory is pinned, not just the one that was bitten.
    """
    raw = script.read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf"), f"{script.name} lost its UTF-8 BOM"
    offenders = [(i, hex(b)) for i, b in enumerate(raw[3:]) if b > 127]
    assert not offenders, f"non-ASCII bytes in {script.name}: {offenders[:5]}"


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("script", HOOK_SCRIPTS, ids=lambda p: p.name)
def test_hook_source_parses(host: str, script: Path) -> None:
    """A hook that cannot be parsed exits non-2 and silently permits the call."""
    proc = subprocess.run(
        [
            host,
            "-NoProfile",
            "-Command",
            f"$errors = $null; "
            f"$null = [System.Management.Automation.Language.Parser]::ParseFile("
            f"'{script}', [ref]$null, [ref]$errors); "
            f"if ($errors.Count) {{ $errors[0].Message; exit 1 }}",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"{script.name} fails to parse under {host}: {proc.stdout}{proc.stderr}"


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ("main", "agent"))
@pytest.mark.parametrize("mode", ("default", "acceptEdits", "plan", "dontAsk", "auto", "bypassPermissions"))
def test_confirmation_tier_preserves_owner_boundary(host, profile, mode):
    expected = "deny" if mode in ("auto", "bypassPermissions") else "ask"
    for command in ("git checkout -f retained", "rm -r retained"):
        assert outcome(host, command, profile, mode) == expected


# git rm is split by profile. An agent never removes tracked
# paths, even with approval, so its verdict is a hard deny with no
# confirmation wording in every mode, including a missing or empty one. The
# main profile keeps the confirmation tier: ask where the host can prompt,
# deny where it cannot. Only a proven dry run is allowed, in either profile.
GIT_RM_FORMS = [
    "git rm retained",
    "git rm -r retained",
    "git rm -f retained",
    "git rm --cached retained",
    "git -C ../wt rm retained",
    "git status && git rm retained",
    'sh -c "git rm retained"',
]
PROMPTING_MODES = ("default", "acceptEdits", "plan", "dontAsk")
# None drops the permission_mode key from the payload entirely.
EVERY_MODE = (None, "", *PROMPTING_MODES, "auto", "bypassPermissions")
EVERY_MODE_IDS = ["missing", "empty", *PROMPTING_MODES, "auto", "bypassPermissions"]


def invoke_mode(host: str, command: str, profile: str, mode: str | None) -> subprocess.CompletedProcess:
    body: dict = {"tool_input": {"command": command}}
    if mode is not None:
        body["permission_mode"] = mode
    return invoke(host, json.dumps(body), profile)


def context(command: str | None, profile: str | None = None, mode: str | None = None) -> str:
    """Name the row in an assertion message: which command, profile and mode failed."""
    return f"command={command!r} profile={profile!r} mode={mode!r}"


def assert_agent_hard_deny(
    proc: subprocess.CompletedProcess,
    command: str | None = None,
    mode: str | None = None,
) -> None:
    # A guard crash also exits 2 with empty stdout; the prefix and the absence
    # of the fail-closed wording prove this deny is a verdict, not an error.
    where = context(command, "agent", mode)
    assert proc.returncode == 2, f"{where}: {proc.stdout}{proc.stderr}"
    assert not proc.stdout, f"{where}: {proc.stdout}"
    assert proc.stderr.startswith("Blocked by agent guard:"), f"{where}: {proc.stderr}"
    # Pin the reason too: a deny from an unrelated rule is not this contract.
    assert "subagents do not run git rm" in proc.stderr, f"{where}: {proc.stderr}"
    assert "failing closed" not in proc.stderr, f"{where}: {proc.stderr}"
    assert "confirmation is required" not in proc.stderr, f"{where}: {proc.stderr}"


# The two main-profile git rm reasons are distinct rules, so pinning the tier
# alone would accept either one -- or an ask raised somewhere else entirely.
GIT_RM_MAIN_REASONS = {
    "git rm retained": "git rm deletes working-tree files",
    "git rm --cached retained": "git rm --cached untracks files",
}


def assert_main_confirmation_tier(
    proc: subprocess.CompletedProcess,
    mode: str | None,
    command: str | None = None,
    expected_reason: str = "git rm",
) -> None:
    where = context(command, "main", mode)
    if mode in PROMPTING_MODES:
        assert proc.returncode == 0, f"{where}: {proc.stderr}"
        decision = json.loads(proc.stdout)["hookSpecificOutput"]
        assert decision["permissionDecision"] == "ask", f"{where}: {proc.stdout}"
        # Pin the reason, as the agent side already does: the tier alone cannot
        # tell this rule from any other ask, nor --cached from the working tree.
        reason = decision["permissionDecisionReason"]
        assert expected_reason in reason, f"{where}: {reason}"
    else:
        # The prefix separates the no-prompt fallback from a guard crash.
        assert proc.returncode == 2, f"{where}: {proc.stdout}"
        assert not proc.stdout, f"{where}: {proc.stdout}"
        assert proc.stderr.startswith("Blocked by main guard: confirmation is required"), f"{where}: {proc.stderr}"


def assert_git_rm_verdict(
    proc: subprocess.CompletedProcess,
    profile: str,
    mode: str | None,
    proven_dry_run: bool,
    command: str | None = None,
) -> None:
    if proven_dry_run:
        where = context(command, profile, mode)
        assert proc.returncode == 0 and not proc.stdout, f"{where}: {proc.stdout}{proc.stderr}"
    elif profile == "agent":
        assert_agent_hard_deny(proc, command, mode)
    else:
        assert_main_confirmation_tier(proc, mode, command)


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("mode", EVERY_MODE, ids=EVERY_MODE_IDS)
@pytest.mark.parametrize("command", GIT_RM_FORMS)
def test_agent_git_rm_is_hard_deny_in_every_mode(host, mode, command):
    assert_agent_hard_deny(invoke_mode(host, command, "agent", mode), command, mode)


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("mode", EVERY_MODE, ids=EVERY_MODE_IDS)
@pytest.mark.parametrize("command", ("git rm retained", "git rm --cached retained"))
def test_main_git_rm_keeps_confirmation_tier(host, mode, command):
    # The other forms reach the same branch; the agent rows above prove that.
    # The two commands are parametrized to exercise two DIFFERENT reasons, so
    # each asserts its own -- otherwise the pair proves nothing the first does.
    assert_main_confirmation_tier(
        invoke_mode(host, command, "main", mode), mode, command, GIT_RM_MAIN_REASONS[command]
    )


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ("main", "agent"))
@pytest.mark.parametrize("mode", (None, ""), ids=["missing", "empty"])
def test_confirmation_tier_denies_without_a_mode(host, profile, mode):
    for command in ("git checkout -f retained", "rm -r retained"):
        proc = invoke_mode(host, command, profile, mode)
        assert proc.returncode == 2 and not proc.stdout, proc.stdout
        assert proc.stderr.startswith(f"Blocked by {profile} guard: confirmation is required"), proc.stderr


# (command, proven dry run). git rm parses options after a pathspec, lets the
# last of --dry-run / --no-dry-run win, and stops at -- or --end-of-options.
# Anything the guard cannot read with certainty is not a proven dry run.
GIT_RM_DRY_RUN_EVERY_MODE = [
    ("git rm --cached --dry-run x", True),
    ("git rm x --no-dry-run -n", True),
    ("git rm -n --no-dry-run x", False),
    ("git rm --dry x", False),
]
GIT_RM_DRY_RUN_GRAMMAR = [
    ("git rm -n x", True),
    ("git rm --dry-run x", True),
    ("git rm x -n", True),
    # Not -rn: the every-position scan reads its `rm -rn x` suffix as a
    # recursive POSIX rm and asks, which is stricter, not a bypass.
    ("git rm -qn x", True),
    ("git rm -fn x", True),
    # -nq: the third bundle the owner named in decision D-BUNDLE.
    ("git rm -nq x", True),
    ("git rm -q --dry-run -- x", True),
    ("git rm --dry-run --no-dry-run x", False),
    ("git rm -- -n", False),
    ("git rm --end-of-options -n x", False),
    ("git rm -N x", False),
    ("git rm --whatif x", False),
    ("git rm --pathspec-from-file=list -n", False),
    ('sh -c "git rm -n --no-dry-run x"', False),
    # The shell or xargs can hand git a --no-dry-run the guard never reads.
    ("git rm -n x \\--no-dry-run", False),
    ("git rm -n x $'--no-dry-run'", False),
    ("git rm -n {--no-dry-run,x}", False),
    ("git rm -n x `--no-dry-run", False),
    ("git rm -n x,--no-dry-run", False),
    ("git rm -n *", False),
    ("echo --no-dry-run | xargs git rm -n x", False),
    # xargs behind control syntax is not the segment head, so the head-position
    # branch never fires and the every-position scan carries the flag itself.
    ("echo --no-dry-run | { xargs git rm -n x; }", False),
    ("if true; then xargs git rm -n x; fi", False),
]


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ("main", "agent"))
@pytest.mark.parametrize("mode", EVERY_MODE, ids=EVERY_MODE_IDS)
def test_git_rm_dry_run_is_proven_in_every_mode(host, profile, mode):
    for command, proven in GIT_RM_DRY_RUN_EVERY_MODE:
        assert_git_rm_verdict(invoke_mode(host, command, profile, mode), profile, mode, proven, command)


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("command,proven", GIT_RM_DRY_RUN_GRAMMAR, ids=[c for c, _ in GIT_RM_DRY_RUN_GRAMMAR])
def test_git_rm_dry_run_grammar(host, command, proven):
    for profile in ("main", "agent"):
        assert_git_rm_verdict(invoke_mode(host, command, profile, "default"), profile, "default", proven, command)


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ("main", "agent"))
def test_auto_keeps_profile_policy_and_deny_precedence(host, profile):
    for command in ("git push", "git merge feature", "git merge --abort"):
        assert outcome(host, command, profile, "auto") == ("deny" if profile == "agent" else "allow")
    # Agent git rm is itself a hard deny, so agent precedence needs an ask-tier command.
    confirmation = "git rm retained" if profile == "main" else "rm -r retained"
    denied = invoke(host, json.dumps({"permission_mode": "auto", "tool_input": {
        "command": confirmation + "; export MSYS_NO_PATHCONV=1"}}), profile)
    assert denied.returncode == 2 and not denied.stdout
    assert "confirmation is required" not in denied.stderr  # deny takes precedence over ask
    assert outcome(host, "echo safe", profile, "futureUnknownMode") == "deny"
    for payload in ('{"permission_mode":"auto","tool_input":{}}',
                    json.dumps({"permission_mode": "auto", "tool_input": {"command": "echo unterminated'"}})):
        assert invoke(host, payload, profile).returncode == 2


@pytest.mark.parametrize("host", HOSTS)
@pytest.mark.parametrize("profile", ("main", "agent"))
@pytest.mark.parametrize("mode", ("default", "auto", "bypassPermissions"))
def test_retention_and_confirmation_aggregation_preserves_stricter_verdict(host, profile, mode):
    """A real ask-tier command must not mask retention denial in either order."""
    # Agent git rm is a hard deny, not ask-tier, so the agent side needs a
    # command that still asks or ask-never-masks-deny goes unexercised.
    confirmation = "git rm retained" if profile == "main" else "rm -r retained"
    held = "git push --force --no-force-with-lease origin retained"
    for command in (confirmation + "; " + held, held + "; " + confirmation):
        proc = invoke(host, json.dumps({"permission_mode": mode, "tool_input": {"command": command}}), profile)
        assert proc.returncode == 2
        assert not proc.stdout
        assert "confirmation is required" not in proc.stderr
    safe_dry_run = "git push --dry-run origin :retained"
    assert outcome(host, safe_dry_run, profile, mode) == "allow"
    expected = "ask" if mode == "default" else "deny"
    assert outcome(host, safe_dry_run + "; " + confirmation, profile, mode) == expected
    if profile == "agent":
        # The allowed dry run cannot soften the agent's git rm hard deny.
        chained = json.dumps({"permission_mode": mode, "tool_input": {"command": safe_dry_run + "; git rm retained"}})
        assert_agent_hard_deny(invoke(host, chained, profile), safe_dry_run + "; git rm retained", mode)
