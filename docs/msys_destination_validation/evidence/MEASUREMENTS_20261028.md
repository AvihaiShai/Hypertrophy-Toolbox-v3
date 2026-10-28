# Pending-assumption measurements — 2026-10-28

Main session, before Plan v1. Every probe was non-mutating or confined to disposable fixtures
under `C:\ht\MSYS-PROBE\` (an existing drive-root child's subtree). No entry was created on a real
drive root. Raw payloads: `C:\ht\MSYS-PROBE\out\` (copied to `probe-out/` beside this file).

Base for implementation: `origin/main` `c29ddf0740ecd9dd90e65424c37050c764504431`, standalone clone
`C:\ht\MSYS` (fresh `git clone` from GitHub; independent object storage), branch
`fix/msys-destination-validation-20261028`. Private Python 3.15.1 (PSF Authenticode Valid) copied to
`C:\ht\MSYS-PY\py3151`; fresh clone `.venv`, `pip check` clean; `npm ci` exit 0.

## M-1 Hook payloads (fresh headless sessions, Claude Code CLI 2.1.302)

Probe project `C:\ht\MSYS-PROBE\p1` registered a payload-dump hook for SessionStart, PreToolUse
(`Bash|PowerShell|Write|Edit`), Stop and SessionEnd. MEASURED:

- PreToolUse carries `session_id`, `cwd` (e.g. `C:\ht\MSYS-PROBE\p1`), `tool_name`
  (`Bash`, `PowerShell`, `Write`), `tool_input`, `permission_mode` (`auto` in `-p`), `transcript_path`,
  `scratchpad_dir`, `prompt_id`, `tool_use_id`. PowerShell tool input field is `command`.
- SessionStart carries `session_id`, `cwd`, `source` (`startup`), `transcript_path`.
- Stop carries `session_id`, `cwd`, `stop_hook_active` (`false` on first stop), `last_assistant_message`.
- SessionEnd fires at headless session end (`reason: other`).
- Visibility: a Stop hook that exits 0 printing `{"systemMessage":"…"}` produced a stream event
  `{"subtype":"informational","content":"Stop says: …","level":"notice"}` — shown to the user.
  SessionStart stdout is returned as `hook_response` (context), exit 0.
- Not measured: interactive VS Code panel rendering of the Stop notice (headless stream only);
  exit 2 on Stop (deliberately not exercised — it blocks stopping).

## M-2 Write tool with a POSIX drive path

Fixture drive `Q:` = `subst` onto `C:\ht\MSYS-PROBE\qroot`, session cwd `Q:\work`, Write
`file_path` `/q/probe-write.txt`. MEASURED: the hook payload already carried `Q:\probe-write.txt`;
the file landed at `Q:\probe-write.txt` (fixture root), not `Q:\q\…`. The harness converts the
Write tool's POSIX drive path before hooks and before writing. Mapping removed afterwards (`subst Q: /D`;
drive list back to C,D,E,F). Edit not separately probed (same file-path handling inferred, ⚠).

## M-3 Git for Windows from PowerShell

`git -C /d/development/Hypertrophy-Toolbox-v3-main rev-parse --show-toplevel` from Windows
PowerShell 5.1, cwd `C:\` and `D:\development`: `fatal: cannot change to '/d/development/…'`.
MEASURED: `git.exe` does not convert `/d/…` when not launched by MSYS bash (read-only probe).

## M-4 Bash redirection target

`cygpath -w /q/out.txt` → `Q:\out.txt`; `cygpath -w /d/x` → `D:\x`. MEASURED for the MSYS resolver
that bash redirection uses; the redirection itself was not executed (inference that bash uses the
same resolver, ⚠ low risk).

## M-5 Python 3.15.1

`os.path.abspath('/d/x')` → `d:\d\x` (cwd `D:`). Same fault class as 3.14.

## M-6 Bash `NAME=` plain argument (S0-a)

argv `x=/d/y`, `--a=/d/y`, `NAME=/d/y`, `a=b=/d/y` → `x=D:/y`, `--a=D:/y`, `NAME=D:/y`, `a=b=D:/y`.
MEASURED: any `<word>=` prefix (including a chained `a=b=`) is converted, not only env assignments.

## M-7 `subst` drive type (S0-b)

With a temporary `subst Q: C:\ht\MSYS-PROBE\qroot`: `Win32_LogicalDisk` reports `Q: type=3` and
`[IO.DriveInfo]` reports `Q:\ Fixed`. MEASURED: a subst drive enumerates as a fixed volume, so a
DriveType-3 enumeration DOES include it (the approved Q5 limit "subst drives are not monitored" is
inaccurate). Mapping removed afterwards; drive list back to C,D,E,F.

## M-8 Existing user-level guard registration (S0-c)

`C:\Users\aviha\.claude\settings.json` lines 123–135: `"hooks": {"PreToolUse": [{"matcher":
"Bash|PowerShell", "hooks": [{"type": "command", "command": "powershell -NoProfile -ExecutionPolicy
Bypass -File \"C:/Users/aviha/.claude/hooks/guard-destructive-command.ps1\" -GuardProfile main"}]}]}`.
No SessionStart/Stop/SessionEnd entries exist at user level. `defaultMode` is `auto`.

## M-9 Resume and hook concurrency (open question 5)

Probe `C:\ht\MSYS-PROBE\p2`, two different SessionStart and two Stop command hooks (each sleeps
1.5 s, appends one line to a shared log). MEASURED:
- `claude -p --resume <id>` keeps the same `session_id`; SessionStart `source` = `resume`.
- Both SessionStart hooks on resume ran concurrently (A 01:39:42.516–44.029, B 01:39:42.513–44.029).
- Unlocked concurrent appends LOST lines: of 8 expected lines only 5 were written. Concurrent hook
  instances therefore need exclusive locking / atomic writes for any shared state.

## M-10 VS Code extension bundled binary (PR-N1)

The installed VS Code extension is `anthropic.claude-code-2.1.310-win32-x64` and bundles its own
`resources\native-binary\claude.exe` 2.1.310 (newer than the PATH CLI 2.1.302). Running THAT binary
headless in probe `C:\ht\MSYS-PROBE\p3` (raw: `probe-out310/`): Bash and PowerShell PreToolUse
payloads both carry `tool_name`, `cwd`, `session_id`, `permission_mode`, `tool_input`; a Stop hook
`systemMessage` again produced the "Stop says: ..." notice. MEASURED for the panel's engine binary
in headless mode; panel rendering itself remains unmeasured.

## M-11 Subagent-originated PreToolUse payload (AR round-2 S-4)

Probe `C:\ht\MSYS-PROBE\p4` (raw: `probe-out-sub/`), bundled `claude.exe` 2.1.310 headless; the main
thread launched one `general-purpose` subagent that ran `echo probe-subagent`. MEASURED: the
subagent's Bash PreToolUse payload carries `tool_name` `Bash`, `cwd` `C:\ht\MSYS-PROBE\p4`,
`agent_id` `a4c79c2174169aca9`, `agent_type` `general-purpose`, `tool_input.command`. Strict Q3a
therefore does not misfire on subagent calls. Charter-frontmatter hook payloads (senior-developer,
automation-qa) were not separately probed; they are produced by the same harness event (inference).

## M-12 Colon-bound options and doubled slashes (diff-review CR-1/CR-2)

Bash tool, Python printing argv: `-Path:/d/x` → `-Path:D:/x`; `/d//x` → `D:/x`; `-X:/c/y` → `-X:C:/y`
(all converted). Windows PowerShell 5.1 `[IO.Path]::GetFullPath("/d//x")` → `d:\d\x` (cwd `D:`).
MEASURED 2026-10-28: both forms reach the drive-root fault when unconverted; both are converted by
MSYS at a leading/attached-option position in Bash.
