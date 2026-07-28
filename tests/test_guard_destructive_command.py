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
    ("git branch -D wt/foo", "main", "ask"),
    ("git branch --delete --force wt/foo", "main", "ask"),
    ("git branch -d wt/foo", "main", "allow"),
    ("git worktree remove ../wt", "main", "ask"),
    # Bare form: exactly one token after the subcommand, which is where a
    # single-element array unrolls to a scalar string and $rest[0] becomes 'r'.
    ("git worktree remove", "main", "ask"),
    ("git worktree list", "main", "allow"),
    ("git checkout -fq main", "main", "ask"),
    ("git checkout main", "main", "allow"),
    # --- aggregation: an early ask must never mask a later deny --------------
    ("rm -r a && rm -rf b", "main", "deny"),
    ("git rm file ; git reset --hard HEAD", "main", "deny"),
    ("git branch -D old && git push --force origin main", "main", "deny"),
    ("git worktree remove ../wt && git status", "main", "ask"),
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
    ("gh pr checks 188", "main", "allow"),
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
    payload = json.dumps({"tool_input": {"command": "git worktree remove ../wt"}})
    assert invoke(host, payload, "main").returncode == 2


HOOK_SCRIPTS = sorted((GUARD.parent).glob("*.ps1"))


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
