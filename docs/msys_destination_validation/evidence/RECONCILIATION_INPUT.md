# MSYS destination validation — Gate 0 reconciliation input (2026-10-28)

Evidence gathered by the main session; consumed by product-manager to revise Section 0 of
`docs/msys_destination_validation/PLANNING.md`. Nothing here was created on any drive root.
Extracted blobs from origin/main sit beside this file (guard.ps1, settings.json, test_guard.py,
policy docs).

## 1. Refreshed ground truth

- Fetched 2026-10-27T22:38:45Z (UTC; local date 2026-10-28). `origin/main` =
  `c29ddf0740ecd9dd90e65424c37050c764504431`.
- #483 MERGED 2026-09-03T19:49:49Z as `0f1ac2ed66c2` (head `7d7ab47e4b4f`).
- #508 MERGED 2026-10-17T19:27:47Z as `654e929d83d1` (head `da756149782b`).
- #510 MERGED 2026-10-17T19:58:01Z as `b114d5500439`, base `main`, head `ef670f4427ac`
  (Section 0 recorded head `d6eacd080d77` on base `fix/guard-registration-contract-20261017`;
  it was rebased/retargeted before merge).
- #507 MERGED 2026-10-17T22:41:09Z as `a81b3685`; `docs/worktree_cleanup/CLOSEOUT.md` is now on
  main (blob `baf01397`); §18.5 is lines 1026–1033, §19.5 lines 1123+.
- All four merge commits are ancestors of `origin/main`. 81 commits since `b114d550`.
- Since 2026-10-17 no commit touched the guard, `.claude/settings.json`,
  `scripts/audit-worktrees.ps1` or `scripts/preflight-worktree-environment.ps1` except #508/#510
  themselves. **Nothing on main implements destination validation or a drive-root delta check.**
- #530 (`f3adacf1`) split guard-hook tests behind a fail-closed "Run Tests" fan-in in CI.
- Blobs on origin/main: guard `2d8a5a55` (1342 lines, SHA-256 `c157c57c…41ee9`);
  `.claude/settings.json` `851ea132` (PreToolUse matcher `Bash|PowerShell`, lines 48–54, project
  registration `${CLAUDE_PROJECT_DIR}/.claude/hooks/...` `-GuardProfile main`);
  `tests/test_guard_destructive_command.py` `b635a83f` (1541 lines); audit `f56fc8af`;
  preflight `cd8521e9` (unchanged).
- Installation state, measured: user-level copy `C:\Users\aviha\.claude\hooks\guard-destructive-command.ps1`
  is hash-identical to main (`c157c57c…`), registered in user settings line 130 (`-GuardProfile main`).
  The shared main checkout's working-tree guard is an older locally modified copy (SHA-256
  `0afb81b8…`); registrations merge and deny wins, so it does not weaken main's guard, but
  "installed" must be measured per copy.
- Fixed volumes: C, D, E, F (NTFS, DriveType 3). No single-letter child exists on `C:\` or `D:\`
  today. `C:\ht` exists (created 2026-10-17T22:00:44; two letters, not fault-shaped; origin not
  verified). `MSYSTEM=UCRT64` now (was `MINGW64` on 2026-10-17); no MSYS override set.
- No live claim on `docs/msys_destination_validation/**` in `WORKSTREAM_OWNERSHIP.local.md`.
- No retained Gate 0 approval exists; the three sign-off boxes are unchecked.

## 2. Guard facts that shape the control

- The guard does **not** read `tool_name`. It reads `permission_mode`, `agent_id` and every string
  field of `tool_input` except `description` (`$commandFields = command, script, code, cmd, input`
  plus all other string fields). It therefore cannot currently tell a Bash command (MSYS converts
  argv) from a PowerShell-tool command (nothing converts).
- Delegation recovery covers `bash/sh -c`, `powershell/pwsh -Command|-c`, `cmd /c|/k`, `eval`,
  `$(...)`, xargs. It does **not** recover `python -c` / `node -e` bodies.
- Existing contracts to preserve: pure ASCII + UTF-8 BOM; exit 2 is the only block; any internal
  failure exits 2; deny-wins aggregation over every segment; ask in auto/bypass → deny; #483 override
  denials and its harmless-inspection allowances (e.g. test line 667 `cmd /c "set MSYS_NO_PATHCONV"`
  → allow); #510 unknown-field scanning, `-GuardProfile` fail-closed, `agent_id` → agent profile;
  the worktree-retention hold.
- **AC3 conflict 1:** existing test payloads carry no `tool_name` (one occurrence in the file, a
  no-tool_input case). Line 201 `git -C /d/development/wt worktree prune --dry-run` (main) expects
  **allow**. A strict "missing tool_name = unconverted" rule would flip it to deny.
- **AC3 conflict 2:** cmd switches `/c /s /q /M /a` appear throughout (lines 219–899). A pattern
  matching a bare `/<letter>` would deny them. The refused token must be `/<letter>/<non-empty segment>`.
- Live side observation: in this session `git rev-parse "origin/main:.claude/settings.json"` failed
  because MSYS rewrote the argument to `origin\main;.claude\settings.json` (path-list conversion).
  That is a different defect (mangling, no drive-root write); this control must not treat it as in scope.

## 3. Measurements (pure computation / argv printing; nothing created)

cwd `D:\development\Hypertrophy-Toolbox-v3-main` unless stated.

| Resolver | Input | Result |
|---|---|---|
| Windows PowerShell 5.1.26100.9711 `[IO.Path]::GetFullPath` | `/d/development/x` | `D:\d\development\x` |
| same, process cwd `C:\` | `/d/development/x` | `C:\d\development\x` |
| same, cwd `C:\` | `\d\x` | `C:\d\x` |
| same | `//d/x` | `\\d\x` (UNC, network — different fault) |
| pwsh 7.6.9 `GetFullPath` | `/d/development/x` | `D:\d\development\x` |
| pwsh 7.6.9 provider path | `/c/Users/x` | `D:\c\Users\x` |
| Node v24.22.1 `path.resolve` | `/c/Users/x` | `D:\c\Users\x`; cwd `C:` `/d/x` → `C:\d\x` |
| `.venv` Python `os.path.abspath` | `/d/x` | `D:\d\x`; cwd `C:` → `C:\d\x` |

Conclusions: pwsh 7 behaves like 5.1 (assumption confirmed). The fault lands on the **current
drive**, not only `D:` (the "D:\ only" assumption is refuted). Backslash-rooted drive-less paths
(`\d\x`) produce the same fault.

MSYS argument conversion in the Bash tool (Python printing `sys.argv`):

| Word passed | Program received | Converted? |
|---|---|---|
| `/d/development/x` | `D:/development/x` | yes |
| `'/c/Users/x'` (quoted) | `C:/Users/x` | yes — quoting does not prevent it |
| `--json=/c/Users/x` | `--json=C:/Users/x` | yes |
| `-D/d/x` | `-DD:/x` | yes |
| `"-D /d/x"` | `-D /d/x` | **no** |
| `"a /d/x"` | `a /d/x` | **no** |
| `'/d/x y'` | `D:/x y` | yes (leading) |
| `"/d/x,/c/y"` | `D:/x,/c/y` | first only — **second unconverted** |
| `x:/d/y` | `x:/d/y` | no (drive-qualified) |
| `//d/x` | `//d/x` | no (UNC) |
| `/d` | `D:/` | yes |
| `/z/x` | `Z:/x` | yes |
| `/tmp/x` | `C:/Users/aviha/AppData/Local/Temp/x` | yes |
| `"open('/d/x')"` | unchanged | **no** (script body) |
| `origin/main:.claude/x` | `origin\main;.claude\x` | mangled (path list) |
| `HEAD:docs/x` | unchanged | no |
| env `OUT=/d/x` | `D:/x` | yes |
| env `OUT2=--o=/c/y` | `--o=C:/y` | yes |
| stdin `/d/x` | unchanged | **no** |

Unmeasured, for Plan v1: Bash redirection `> /d/x` (MSYS runtime opens it; expected `D:\x`);
whether Git for Windows `git.exe` converts `/d/…` when called from the PowerShell tool; Write/Edit
tool behaviour for a `/d/…` `file_path`; SessionStart/Stop/SessionEnd hook output visibility and
exit-code semantics on the installed CLI.
