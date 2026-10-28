# MSYS destination validation and `D:\`-child monitoring — Planning

**Status:** Gate 0 APPROVED by owner 2026-10-28 (quotes under the Gate 0 sign-off). Gate 1,
implementation, merge, installation and bounded operational acceptance are **accepted under the
owner's task-specific delegation**, not the owner's personal review. PR #654 merged as
`d8e3e3c61866ca0fa123693335d65775d880225e`; the merged user-level hooks are installed and the
fresh bundled-CLI check passed. The four acceptance levels and remaining coverage limits are
recorded at the end of this document and in [CLOSEOUT.md](CLOSEOUT.md). Panel rendering remains
unmeasured; `PREVENTION_COMPLETE` is not claimed. Plan v1 drafted 2026-10-28; council rounds 1–3
complete; Plan v2 (final, rev. round 3). First drafted 2026-10-17 by session `S8-MSYS-GATE0`.

**Planning size:** Large / new workflow (`docs/ai_workflow/QUALITY_GATE.md`, plan-stage routing).
The work changes the executable destructive-command guard or adds a new agent-workflow control,
and introduces a monitoring workflow. Gate 0 and a council-reviewed Gate 1 are both required.

**Measured against:** `origin/main` @ `c29ddf0740ecd9dd90e65424c37050c764504431`, fetched
2026-10-27T22:38:45Z (local date 2026-10-28). All four related PRs are MERGED and are ancestors
of that commit: #483 as `0f1ac2ed66c2`, #508 as `654e929d83d1`, #510 as `b114d5500439` (base
`main`, head `ef670f4427ac`), #507 as `a81b3685`. Nothing on `origin/main` implements destination
validation or a drive-root delta check. Evidence base:
`artifacts/msys-gate0-20261028/RECONCILIATION_INPUT.md`, cited below as "input §n".

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

The queue item, `artifacts/open-work-queue-20261017/PLAN.md`, "MSYS destination validation and
`D:\`-child monitoring":

> - **Owner:** unassigned.
> - **Blocker:** no packet scoped; the controls are unimplemented.
> - **Next permitted action:** scope a packet. **#508 fixed the guard *registration contract*, a
>   different defect class** — §19's closure does **not** cover the drive-root fault. A local branch
>   `fix/msys-path-conversion-prevention-20260903` exists but is **not** what shipped.
> - **Completion evidence:** control implemented with a test that fails without it.

The session brief that commissioned the 2026-10-17 draft:

> Use the requirements skill to write ONLY Section 0 of docs/msys_destination_validation/PLANNING.md
> (a new file; that is your one named tracked-path write; do not commit it). Stop at Gate 0.
> - #508 fixed a different defect class (the registration contract). §19's closure does not cover the
>   drive-root fault. The local branch fix/msys-path-conversion-prevention-20260903 is NOT what
>   shipped: read it for evidence only.
> - Section 0 must require a control with a test that fails without it, and must state that
>   implementation bases on main after #510 lands (both touch the guard).
> - List the blocking owner questions explicitly.

The 2026-10-28 revision objective, relayed by the main session as the owner's intent (a relay, not
an owner approval):

> advance Section 0 through its next required gate for preventing unconverted POSIX drive paths
> from creating unintended Windows directories and detecting new drive-root children. Override
> denial (#483) and guard-registration fixes (#508/#510) are NOT completion of this item. Retained
> requirements: refuse unsafe destinations before creation; detect new drive-root children
> independently of existing audit failures; monitoring read-only; prove each control with a test
> that fails when the control is neutralized and passes when restored, using isolated disposable
> fixtures; preserve existing guard contracts; distinguish implementation, merge, installation and
> operational acceptance. Never claim PREVENTION_COMPLETE.

The controls the item refers to are stated in `docs/worktree_cleanup/CLOSEOUT.md` §18.5 (on
`origin/main` since #507, blob `baf01397`, lines 1026–1033):

> The `D:\c` and `D:\d` faults were **MSYS path conversion**, not destination choice: a
> `/c/...` or `/d/...` path landed as a literal relative directory beneath the drive root.
> Destination validation alone does not address this. The standing controls are therefore:
> native PowerShell with drive-qualified absolute paths; validation of the resolved
> destination before anything is created; and a check that flags unexpected new `D:\`
> children, run around browser-automation sessions.

**Problem**

An agent command can write to a directory beneath the drive root that nobody intended. A POSIX
drive path (`/c/Users/…`, `/d/development/…`) that reaches a native Windows program without
being converted resolves as a path relative to the root of the **current** drive. With the working
directory on `D:`, `/c/Users/x` becomes `D:\c\Users\x`; on `C:`, `/d/development/x` becomes
`C:\d\development\x`. The output is correct but lands in the wrong place, so nothing fails.

Two such trees happened (`docs/worktree_cleanup/CLOSEOUT.md` §18.1; incident record
`artifacts/operation-a-evidence-20260930-015143/coverage/linked-reference_bash_tool_msys_path_conversion.md`):

| Tree | Created | Producer | Disposition |
|---|---|---|---|
| `D:\c\Users\aviha\…\scratchpad\vitest_list_main.json` | 2026-08-30 | `npx vitest list --json=/c/Users/…` with an MSYS override exported | removed 2026-10-17 |
| `D:\d\development\ht-wt-hlinux-gate1-20260902\…` (52 files, 16,994,332 B) | 2026-09-02 | `gh.exe run download -D /d/development/…` with an MSYS override exported | preserved to `artifacts/drive-root-recovery-20261017/`, then removed. It was the only surviving copy of that Gate-1 evidence. |

Three things on `origin/main` each cover one route to the fault; none covers the whole of it:

- **#483** makes the guard deny observable attempts to set `MSYS_NO_PATHCONV` /
  `MSYS2_ARG_CONV_EXCL` (lines 84–225 of #483's guard blob `083634f7`). Both recorded faults
  predate it and used that override.
- `scripts/preflight-worktree-environment.ps1` (blob `cd8521e9`, line 94) checks whether either
  variable is present at Process, User or Machine scope.
- `scripts/audit-worktrees.ps1` (blob `f56fc8af`, lines 231–247) compares drive-root children
  against an owner-approved baseline. It **did** detect both trees (`driveRootUnexpected` rows in
  `artifacts/opA-storage-20261007T130000Z/evidence/opc-sizing.json`), yet **both persisted until
  2026-10-17**. The audit had exited non-zero on 21 of 21 runs as of 2026-10-17 (`PLAN.md`,
  "Prevention completion"), so a new unexpected child is one more line in an always-red report.

**Residual route, re-measured 2026-10-28** (no MSYS override set, `MSYSTEM=UCRT64`; pure path
computation, nothing created; input §3):

| Resolver | Input | cwd drive | Resolved to |
|---|---|---|---|
| Windows PowerShell 5.1.26100.9711 `[IO.Path]::GetFullPath` | `/d/development/x` | D: / C: | `D:\d\development\x` / `C:\d\development\x` |
| same | `\d\x` | C: | `C:\d\x` |
| pwsh 7.6.9 `GetFullPath` / provider path | `/d/development/x` / `/c/Users/x` | D: | `D:\d\development\x` / `D:\c\Users\x` |
| Node v24.22.1 `path.resolve` | `/c/Users/x` / `/d/x` | D: / C: | `D:\c\Users\x` / `C:\d\x` |
| `.venv` Python `os.path.abspath` | `/d/x` | D: / C: | `D:\d\x` / `C:\d\x` |

In the Bash tool MSYS converts a drive path only where it leads a word, follows `--opt=`, is
attached to a short option (`-D/d/x`), or is an env-assignment value; quoting does not stop it. It
does **not** convert a drive path later in a word (`"-D /d/x"`, `"a /d/x"`, the second item of
`"/d/x,/c/y"`), a script body (`python -c`, `node -e`, `powershell -Command`) or stdin. Nothing
converts a PowerShell-tool command (input §2–§3). #483 cannot see this route: no override is
involved.

**What did not fix this.** #508 (MERGED 2026-10-17 as `654e929d83d1`) changed Python tests and
generated inventories only; it closed the guard **registration contract**, a different defect
class, and its CLOSEOUT §19 closure does not cover the drive-root fault. #510 (MERGED 2026-10-17
as `b114d5500439`) closed three fail-opens and tightened `agent_id`; it adds no destination check.
The local branch `fix/msys-path-conversion-prevention-20260903` (tip `7d7ab47e`) is `git patch-id
--stable`-identical (`8d44c95a…`) to the merged #483: override denial only. This packet reads it
as evidence and does not build on it.

**Acceptance criteria**

*Destination validation*

1. **Given** a command on an in-scope surface (Q2), **when** it contains a *drive token* —
   `/<single letter>/<non-empty segment>` at a path boundary, i.e. not preceded by a word
   character, `.`, `/`, `:` or `\`, or immediately after an attached short-option prefix
   `-<one or more letters>` at the start of a word (`-D/d/x`, `-o/c/y`) (so cmd switches
   `/c /s /q`, URLs and relative paths never match) — inside an **unconverted region**, **then** it is refused before anything runs, and the
   refusal names the token as written and the path it resolves to on the drive of the payload's
   `cwd`. Unconverted regions: (a) any PowerShell-tool command; (b) any script body of
   `python -c`, `node -e` or `powershell|pwsh -Command|-c`, including bodies reached through
   `bash -c` / `cmd /c` delegation; (c) a Bash word in which the token is not at a position AC2
   lists as converted (measured: `"-D /d/x"`, `"a /d/x"`, the second token of `"/d/x,/c/y"`). The
   control must read `tool_name`, which the guard does not do today (input §2); a payload with an
   absent or unknown `tool_name` follows Q3a.
2. **Given** the same surfaces, **when** a command uses a drive-qualified Windows path in either
   slash form (`D:/development/…`, `D:\development\…`, `C:\Users\…`), or a Bash word whose token
   is leading, follows `--opt=`, is attached to a short option (`-X/d/…`), or is an env-assignment
   value (all measured converted, input §3), **then** this control does not refuse it. The Case
   table below is normative; every row is a test.
3. **Given** the guard on `origin/main` (blob `2d8a5a55`), **when** this control is added, **then**
   these contracts still hold (input §2): pure ASCII + UTF-8 BOM; exit 2 is the only block and any
   internal failure exits 2; deny-wins aggregation over every segment; ask under auto/bypass becomes
   deny; #483's override denials and its harmless-inspection allowances (test line 667
   `cmd /c "set MSYS_NO_PATHCONV"` → allow); #510's unknown-field scanning, `-GuardProfile`
   fail-closed handling and `agent_id` → agent profile; the worktree-retention hold. Every existing
   guard test keeps its expected decision. Two conflicts are resolved: (i) existing payloads carry
   no `tool_name`, and line 201 (`git -C /d/development/wt worktree prune --dry-run` → allow) would
   flip to deny under a strict rule — the fixture consequence depends on Q3a; (ii) cmd switches
   (lines 219–899) are excluded by the AC1 token definition. No new fail-open: input the control
   cannot parse is refused, not allowed.

*Drive-root-child monitoring*

4. **Given** a snapshot of the direct children of each monitored root (Q5) taken at the start
   point (Q4), **when** the check runs at the end point and a child exists that was not in the
   snapshot, **then** it exits non-zero and names each new child by exact path. The check is
   independent: its own script, its own exit code, its own report. It never reads
   `audit-worktrees.ps1` output or the owner baseline, so a red audit can neither mask nor produce
   its result.
5. **Given** no new child since the snapshot, **then** it exits 0 whatever the state of the baseline
   audit and the `ORPHANED_ANNOTATION` rows. **Given** an unreadable monitored root, or a missing or
   invalid snapshot, **then** it exits non-zero and reports `UNKNOWN`, never 0.
6. **Given** any run of the check, **then** it is read-only: it never creates, deletes, renames or
   modifies a monitored root's entries or anything beneath them. Its one exception is a single
   snapshot/report file at a caller-named path, which must not be a direct child of a monitored root
   nor inside the H4-protected `D:\dev-cleanup-20260824-digest` or `D:\_digest-discard-bin`. A
   read-only post-run check asserts that the H4 trees' NTFS creation times (recorded 2026-10-17:
   `2026-09-28 18:26:56`, `18:31:21`) are unchanged.

*Proof, sequencing and acceptance*

7. **Given** each control, **then** at least one test **fails with the control neutralized and
   passes with it restored**, using disposable fixtures only. The monitor takes an explicit root
   list, so tests pass `tmp_path` roots and never a real drive root. Guard tests are
   classification-only, plus a sentinel proof that a refused payload never executes (the pattern
   of `test_denied_payload_never_executes_its_child`, test line 932). The neutralized arm runs on a
   disposable copy of the control with its decision function replaced by a no-op, in an isolated
   clone or archive at a short path outside `D:\development` (PLAN.md H3). Both directions are
   retained as evidence on the exact candidate commit. An inventory regeneration, or a test never
   run against the neutralized control, does not satisfy this criterion.
8. **Given** #510's precondition is MET (merged 2026-10-17), **then** implementation bases on a
   freshly fetched `origin/main` at its start, with the full 40-character SHA recorded — not local
   `main`, not any PR branch, not `7d7ab47e`.
9. **Given** any added or removed test case, **then** `docs/test_inventory/` is regenerated by its
   own generator and `generate_test_inventory.py --check` exits 0 on the candidate; pyright reports
   no net-new errors on changed Python files; and the #530 guard-test CI fan-in (`f3adacf1`,
   fail-closed "Run Tests") still accounts for any new test file.
10. **Given** the four acceptance levels, **then** each is recorded with its own evidence, and merge
    alone does not close the item:
    - *Implementation* — the AC7 two-direction evidence on the candidate commit.
    - *Merge* — the named PR merged with required checks green.
    - *Installation* — the owner copies the merged guard/monitor to the user-level copies,
      hash-equal to the merged blobs, and registers any hooks. Measured per copy: today the
      user-level guard equals main's (`c157c57c…`) while the shared checkout's working-tree guard is
      an older local copy (`0afb81b8…`) (input §1).
    - *Operational* — in a fresh session the installed guard refuses a seeded refused-row command,
      and the monitor runs from its trigger and reports.

**Calculation surface**

- `none`. No product calculation, schema, API response shape or route is touched. This packet is
  agent-workflow and tooling only.

**In scope**

- A destination-validation control meeting AC1–AC3 on the surfaces selected in Q2.
- A drive-root-child delta check meeting AC4–AC6 on the roots selected in Q5, with the trigger
  selected in Q4.
- Tests meeting AC7, the regenerated inventory, and documentation of both controls in the
  workflow surface the plan names. One PR or two is a Plan v1 decision.

**Out of scope / non-goals**

- Re-opening #483's override denial, #508's registration contract or #510's fail-opens and
  `agent_id` tightening; they are consumed as the base.
- MSYS path-list mangling (Case A12) and UNC `//d/x` (Case A11): different faults.
- Automatic remediation of any drive-root child: no deletion, quarantine or move.
- Changing the owner-local drive baseline, `WORKSTREAM_OWNERSHIP.local.md`, or the
  `ORPHANED_ANNOTATION` rows (owner-only, gitignored).
- Performing installation or hook registration. Those are owner actions after merge; AC10 records
  them but this packet does not execute them. *(Superseded 2026-10-28 for this task by the owner's
  delegation recorded under the Gate 0 sign-off; installation is planned in Plan v1.)*
- Declaring `PREVENTION_COMPLETE` or any of its conjuncts.
- Any worktree creation, removal or prune; any branch or ref deletion; the backup-disappearance
  investigation; B1 preservation.
- Launching the Flask app or running Playwright. Port 5000 is shared and hard-coded.

**Assumptions made** (2026-10-17 set, with 2026-10-28 dispositions; then new items)

- CONFIRMED — PowerShell 7 resolves `/d/…` like 5.1 (pwsh 7.6.9 measured, input §3).
- REFUTED — "monitoring is limited to `D:\`": the fault lands on the cwd drive (`C:\d\…` measured
  with cwd `C:`, input §3). Replaced by Q5.
- CONFIRMED — #510 lands before implementation (merged 2026-10-17; AC8).
- ⚠️ UNSUPPORTED by evidence — tying the monitor to browser-automation sessions: both recorded
  faults came from `npx vitest` and `gh.exe` (Q4).
- ⚠️ Pending Q1 — the control belongs in the destructive-command guard.
- ⚠️ Pending Q2 — in-scope surfaces are the Bash and PowerShell tools; the `PreToolUse` matcher is
  `Bash|PowerShell` (`.claude/settings.json` blob `851ea132`, lines 48–54), so Write/Edit paths and
  MCP parameters are unseen.
- ⚠️ Pending Q1/Q2 — "destination validation" in CLOSEOUT §18.5 means refusing an unconverted POSIX
  drive token (AC1), not allow-listing every write destination.
- ⚠️ Pending Q4 — the delta check compares against a start-point snapshot, not the owner baseline
  (now encoded in AC4).
- ⚠️ NEW — the guard has no `tool_name` input today (input §2); AC1 adds one.
- ⚠️ NEW — the PreToolUse payload carries a usable `cwd` field on the installed CLI. Not measured;
  AC1's resolved-path message depends on it.
- ⚠️ NEW, unmeasured, must be measured in Plan v1 (input §3): Write/Edit behaviour for a `/d/…`
  `file_path`; whether Git for Windows `git.exe` converts `/d/…` when called from the PowerShell
  tool; Bash redirection `> /d/x`; SessionStart/Stop hook output visibility and exit-code
  semantics on the installed CLI.
- ⚠️ NEW — Q3a "strict" is a mechanical fixture change, not a single edit: `outcome()` (test line
  93) builds most payloads, but about fifteen other sites call `json.dumps` directly (e.g. lines
  707, 741, 1015, 1179, 1304, 1433, 1474), measured by grep on blob `b635a83f`.

**Gate 0 decision sheet** — all blocking; defaults are recommendations, not decisions

| Q | Decision | Recommended default | Alternatives | Why / coverage limit |
|---|---|---|---|---|
| Q1 | Where does destination validation live? | (a) a deny rule inside `guard-destructive-command.ps1`, keyed on `tool_name` | (b) a separate `PreToolUse` hook; (c) no runtime deny (documented resolver + contract test) | (a) is already registered on both matchers at project and user level (input §1). (b) doubles registration and installation surface. (c) fails AC1. |
| Q2 | Which surfaces are refused? | Bash and PowerShell tool commands, including recovered delegation bodies and `python -c` / `node -e` bodies | add Write/Edit `file_path` and MCP parameters | The extra surfaces are off the matcher and would need new registrations. Under the default they are covered only by the monitor backstop. |
| Q3 | Ambiguous input | Fail-closed (refuse) | allow | Consistent with the guard's "confidently classified, or denied" contract. |
| Q3a | Payload with absent or unknown `tool_name` | Treat as unconverted (strict); every existing payload site adds `"tool_name": "Bash"`, every expected decision unchanged | treat absent as Bash: existing tests byte-unchanged | The alternative fails open if the field is ever renamed. Strict touches many fixture sites (Assumptions). |
| Q3b | Drive token embedded in a Bash word | Refuse | allow | False positives on prose such as commit-message text; remedy is writing `D:/…`. |
| Q3c | Backslash-rooted `\<letter>\…` | Not refused | refuse | Collides with regex escapes such as `\d\w`. Monitor backstop only (Case L1). |
| Q3d | Other rooted POSIX paths in unconverted regions (`/tmp/x` → `D:\tmp\x`) | Not refused | refuse | Collides with URL route strings such as `'/api/backups'` in `python -c` probes. Monitor backstop only (Case L2). |
| Q4 | Monitor trigger | A standalone read-only script with snapshot and compare modes and an explicit root list; a SessionStart (snapshot) + Stop (compare) hook pair, plus a documented manual run around browser-automation sessions and artifact-download commands | browser-automation-only manual run; the scheduled `OperationA-WorktreeAudit` | Both faults came from `npx vitest` and `gh.exe`, not browser automation. The scheduled task has no reliable natural firings. Hook semantics are unmeasured (Assumptions). |
| Q5 | Which roots? | Every fixed volume enumerated at run time (DriveType 3; today C, D, E, F) | `D:\` only; the cwd drive only | Removable and network drives are not monitored. A `subst` drive enumerates as a fixed volume and **is** monitored (M-7) *(post-Gate-0 correction 2026-10-28; decision unchanged)*. OS-created children on `C:\` will appear as reports. |
| Q6 | What closes the item? | Operational acceptance (AC10); merge is recorded as "merged, not installed" | close at merge with AC7 evidence | Contributes to, but never declares, `PREVENTION_COMPLETE`. |
| Q7 | Does a monitor hit block? | Report-only: non-zero exit and report, never blocks | block the next agent step | Refusal before creation is the guard's job. Blocking after creation cannot undo it, and a blocking Stop hook would trap the agent in a loop. |

**Case table** — normative under the recommended defaults; every row is a test. "Resolves to"
assumes cwd on `D:`; on another drive only the letter changes (input §3).

| # | Tool | Input | MSYS converts? | Resolves to | Decision |
|---|---|---|---|---|---|
| A1 | PS | `Get-Content -LiteralPath D:\development\x` | n/a | `D:\development\x` | allow |
| A2 | PS | `New-Item -ItemType Directory -Path 'D:/development/x'` | n/a | `D:\development\x` | allow |
| A3 | PS | `C:\Users\aviha\x` | n/a | `C:\Users\aviha\x` | allow |
| A4 | Bash | `gh run download 1 -D /d/development/x` | yes (leading) | `D:/development/x` | allow |
| A5 | Bash | `npx vitest list --json=/c/Users/x/out.json` | yes (`--opt=`) | `C:/Users/x/out.json` | allow |
| A6 | Bash | `git -C /d/development/wt worktree prune --dry-run` (test line 201) | yes (leading) | `D:/development/wt` | allow |
| A7 | Bash | `OUT=/d/x python tool.py` | yes (env value) | `D:/x` | allow |
| A8 | Bash | `python -c "open(r'D:/development/x','w')"` | n/a (drive-qualified) | `D:\development\x` | allow |
| A9 | either | `cmd /c "rmdir /s /q tmp"` | n/a — switches are not drive tokens | — | this control silent; existing guard deny (test line 219) stands |
| A10 | either | `https://host/d/x`, `./d/x`, `docs/d/x`, `gh api repos/o/r/contents/d/x` | n/a — no path boundary | — | allow |
| A11 | Bash | `//d/x` | no (UNC) | `\\d\x` | allow — different fault |
| A12 | Bash | `git rev-parse origin/main:.claude/x` | mangled (path list) | `origin\main;.claude\x` | allow — different defect, not this control |
| A13 | Bash | `cat /tmp/x` | yes | `C:/Users/aviha/AppData/Local/Temp/x` | allow |
| R1 | PS | `New-Item -ItemType Directory /d/development/x` | n/a | `D:\d\development\x` | refuse |
| R2 | PS | `gh run download 1 -D /d/development/x` | n/a | `D:\d\development\x` | refuse |
| R3 | PS | `[IO.Path]::GetFullPath('/c/Users/x')` | n/a | `D:\c\Users\x` | refuse — read-only, but a textual control cannot see intent |
| R4 | Bash | `python -c "import os; os.makedirs('/d/development/x')"` | no (script body) | `D:\d\development\x` | refuse |
| R5 | Bash | `node -e "require('fs').mkdirSync('/c/Users/x',{recursive:true})"` | no (script body) | `D:\c\Users\x` | refuse |
| R6 | Bash | `powershell -NoProfile -Command 'New-Item /d/x -ItemType Directory'` | no (script body) | `D:\d\x` | refuse |
| R7 | PS | `pwsh -c "Set-Content /c/x/y.txt hi"` | n/a | `D:\c\x\y.txt` | refuse |
| R8 | Bash | `tool --paths "/d/x,/c/y"` | first only | `D:/x`, `D:\c\y` | refuse (second token) |
| R9 | Bash | `tool "-D /d/x"` | no (embedded) | `D:\d\x` | refuse (Q3b) |
| R10 | Bash | `bash -c "python -c \"open('/d/x','w')\""` | no (nested body) ⚠️ nested form unmeasured | `D:\d\x` | refuse |
| R11 | PS | `Get-Date > /d/out.txt` | n/a | `D:\d\out.txt` | refuse |
| R12 | none | any payload without `tool_name` containing `/d/x` | unknown | — | refuse (Q3a strict) |
| R13 | PS | `git -C /d/development/wt status` | n/a; `git.exe` does not convert from PowerShell (measured, M-3) | `D:\d\development\wt` | refuse |
| R14 | PS | `gh run download 1 -D/d/x` | n/a | ⚠️ inferred `D:\d\x` | refuse (attached short option) |
| L1 | PS | `New-Item \d\x` | n/a | `D:\d\x` | not refused (Q3c) — monitor backstop |
| L2 | PS | `New-Item /tmp/x` | n/a | `D:\tmp\x` ⚠️ inferred, not measured | not refused (Q3d) — monitor backstop |
| L3 | either | `python script.py` whose file contains `/d/x` | no | `D:\d\x` | not refused — file contents invisible |
| L4 | PS | `$p = '/' + 'd/x'; New-Item $p` | n/a | `D:\d\x` | not refused — built at run time |
| L5 | Write | `file_path` `/d/x` | harness converts before hooks (measured, M-2) | `D:\x` (measured analogue `/q/…` → `Q:\…`) | allow — harness converts, measured; Edit inferred ⚠️ |
| M1 | monitor | new child in a fixture root after snapshot, with a red standing-audit fixture present | — | — | non-zero; names the exact path |
| M2 | monitor | no new child, any audit state or `ORPHANED_ANNOTATION` rows | — | — | exit 0 |
| M3 | monitor | a child removed since the snapshot | — | — | not reported as new |
| M4 | monitor | unreadable root, or missing/invalid snapshot | — | — | non-zero, `UNKNOWN` |
| M5 | monitor | any run | — | — | fixture root entries and timestamps unchanged; only the named snapshot/report file written |

**Material coverage limits**

- Script files, stdin, heredocs and npm scripts are invisible to a textual guard (L3).
- MCP tool parameters are off the matcher; only the monitor sees their result. The Write tool
  converts a POSIX drive `file_path` before hooks and writes to the converted path (M-2,
  measured; Edit inferred ⚠️), so L5 is not a fault route *(post-Gate-0 correction 2026-10-28;
  decision unchanged)*.
- Non-Claude processes (Codex, the owner's terminal, scheduled tasks) are not guarded.
- Paths built at run time cannot be detected textually (L4).
- The Q3c/Q3d forms (`\d\x`, `/tmp/x`) are not refused.
- The monitor sees only direct root children, only between snapshot and compare; a child created
  and removed inside that window is invisible.
- The guard is "a speed bump in front of honest mistakes … not a sandbox" (its own docstring,
  guard blob `2d8a5a55` lines 54–56).

**Post-Gate-0 measurements (2026-10-28)** — from
`artifacts/msys-gate0-20261028/MEASUREMENTS_20261028.md` (M-n below). They resolve ⚠️ items
without changing any approved AC, decision or default.

- M-1, MEASURED: PreToolUse payloads carry `cwd`, `tool_name` (`Bash`, `PowerShell`, `Write`) and
  `session_id`; the PowerShell tool's input field is `command`. SessionStart carries
  `session_id`, `cwd`, `source`; Stop carries `session_id`, `cwd`, `stop_hook_active`; SessionEnd
  fires (Claude Code CLI 2.1.302, headless).
- M-1, MEASURED: a Stop hook exiting 0 with `{"systemMessage": …}` is shown to the user as a
  notice (headless stream). Not measured: VS Code panel rendering of that notice; Stop exit 2.
- M-2, MEASURED: the Write tool converts a POSIX drive `file_path` (`/q/…` → `Q:\…`) before hooks
  and writes there. Case L5 is therefore "allow — harness converts". Edit is inferred, not
  probed ⚠️. The second coverage-limit bullet above is corrected accordingly.
- M-6 to M-9 (added after Plan v1) are cited in Plan v2: any `<word>=` prefix converts (M-6); a
  `subst` drive is a fixed volume (M-7, Q5 wording corrected above); the user-level guard
  registration form (M-8); resume keeps `session_id`, and concurrent hooks overlap and lose
  unlocked writes (M-9).
- M-3, MEASURED: Git for Windows `git.exe` launched from PowerShell does not convert `/d/…` (R13
  confirmed).
- M-4: the MSYS resolver bash redirection uses was measured via `cygpath -w` (`/d/x` → `D:\x`);
  that redirection itself uses it is a low-risk inference ⚠️.

### Section 0 sign-off — GATE 0
- [x] User confirms the acceptance criteria match intent.
- [x] User reviewed the assumptions and corrected or accepted each one.
- [x] Blocking questions are answered.
- [x] Owner answered the decision sheet (or accepted the recommended defaults).

Owner approval, 2026-10-28, written by the owner in the main session and relayed verbatim to this
`product-manager` (agent `a96acae55b870d077`) for recording. This agent did not observe the owner's
message directly.

> I approve Gate 0: accept the acceptance criteria, assumptions and recommended defaults for
> Q1–Q7, including Q3a–d, in docs/msys_destination_validation/PLANNING.md. Have product-manager
> record this approval and check the four Gate 0 boxes.

Owner delegation, 2026-10-28, same session and relay:

> For this task only, I delegate the remaining planning and implementation decisions to you within
> the scope below. This explicitly replaces requirements to return to me for personal Gate 1
> sign-off, reviewer-disposition decisions, commit/push/PR/merge permission, and installation
> permission. Preserve the actual reviews, tests and evidence requirements. Record delegated
> acceptance accurately; do not claim I personally reviewed a future Plan v2.
> The previous Section 0 restrictions against implementation, commits, pushes, merges,
> installation and hook registration are superseded by this authorization within this task's
> scope. Do not edit the repository's general approval policies.

Effect: Gate 0 is APPROVED by the owner. Within this task's scope, implementation, commit, push,
PR, merge, installation and hook registration are authorized under the delegation. Gate 1 and
reviewer dispositions are delegated to the main session acting as manager, and they are recorded
as delegated acceptance, never as the owner's personal review. The council reviews, tests and
evidence requirements stay in force, and so do the out-of-scope items above (other than the
superseded installation bullet).

---

## Plan v1

**Goal**: Before anything runs, refuse Bash and PowerShell tool commands that would hand an
unconverted POSIX drive path to a native Windows resolver. Separately, report any new child that
appears on a fixed-volume root during a session, without blocking. Both controls are proven by
two-direction tests and carried through merge, installation and operational acceptance (AC10).

**Design decisions** (Plan v1; open to council challenge)

| # | Decision | Reason |
|---|---|---|
| D1 | The drive-token rule is a new, self-contained walker `Invoke-DriveTokenScan($text, $region, $depth)` inside `guard-destructive-command.ps1`. It is called once per candidate command at the entry point and writes into the existing `$script:denials`. | Q1(a). The existing destructive-verb walk is left byte-unchanged (AC3), deny-wins aggregation is inherited, and the rule is one function a neutralization arm can no-op (AC7). |
| D2 | Region selection: `tool_name -ceq 'Bash'` → `Bash`. Any other value, including `PowerShell`, absent, empty or unknown → `Unconverted`. | Q3a strict. Only the one measured-converting tool gets the lenient grammar. |
| D3 | `Unconverted` region: a raw-text regex scan of the whole string, so nested bodies are covered without parsing. Token: `/<letter>/<segment>`, where the segment is one or more characters other than slash, backslash, whitespace, quote, backtick, `,` `;` `)` `]` `}` `\|` `&` `<` `>`. Boundary: not preceded by `[\w./:\\]`, **or** preceded by `(?<=(^\|[\s'"(])-[A-Za-z]+)` (attached short option, AC1). | AC1 token definition, implemented as pure string computation (Linux pwsh CI). |
| D4 | `Bash` region: tokens come from the existing quote-aware `Split-Segments` (quotes stripped, so `"-D /d/x"` stays one token). A token's drive-token occurrence is *converted* only at offset 0, or right after a prefix matching `^(?:[A-Za-z_]\w*=)?(?:-{1,2}[A-Za-z][\w-]*=\|-[A-Za-z]+)?$` (env value, `--opt=`, `-o=`, attached `-X`, and the measured `OUT2=--o=` chain). Every other occurrence is refused (AC1(c), Q3b). | Allows exactly the measured MSYS conversions (input §3). Anything unmeasured falls to refuse (Q3). Measurement S0-a below decides whether a plain argument `x=/d/y` keeps the `NAME=` prefix allowance outside env-assignment position. |
| D5 | Bash bodies. (i) For `python\|python3\|py\|pythonw` with `-c`, and `node` with `-e\|--eval\|-p\|--print`, the following token is scanned as `Unconverted`. (ii) `Get-Delegation` results are reused: a POSIX shell or `eval` body is re-scanned as `Bash`; a `powershell\|pwsh` or `cmd /c\|/k` body is re-scanned as `Unconverted`. (iii) Depth beyond `$maxDelegationDepth` denies. | AC1(b), R4–R6, R10. Unquoted `powershell -Command New-Item /d/x` is converted by MSYS but refused anyway: an accepted fail-closed false positive (Q3). |
| D6 | Refusal text names the token as written and, when `cwd` matches `^[A-Za-z]:[\\/]`, the resolved path `<cwd letter>:` + the token with `/` turned into `\`. A missing, empty, UNC or otherwise non-drive `cwd` still refuses, but says "cwd unavailable; no resolved path is claimed". | AC1; owner must-address (5). No filesystem call, so the rule is identical on Linux pwsh. |
| D7 | The monitor is ONE self-contained file, `.claude/hooks/drive-root-monitor.ps1`, with modes `Snapshot`, `Compare`, `HookSessionStart` and `HookStop`. | A single file to install at user level, with no repository path dependency. The existing `HOOK_SCRIPTS` glob pins its ASCII + BOM automatically. No `scripts/**` change, so the Tooling/scripts row does not apply. |
| D8 | Roots: an explicit `-Root <string[]>`. When it is omitted, enumerate `[IO.DriveInfo]::GetDrives()` with `DriveType -eq 'Fixed'` and format each as `X:\`. Hook modes take the same optional `-Root` and `-SnapshotDir`. Tests always pass them; production registrations never do. There is no environment-variable override. | Q5. Tests never touch a real drive root (AC7). An env override would be a silent fail-open seam. |
| D9 | Standalone exit codes: `0` CLEAN, `10` NEW_CHILDREN, `11` UNKNOWN (also bad arguments and internal failure). The report is JSON on stdout: `status`, `new[]`, `unknown[]`, `faultShapedPresent[]`. If any root is UNKNOWN the status is UNKNOWN, and `new[]` is still listed. | AC4/AC5; owner must-address (2). Distinct from 2 so an exit code is never confused with a hook block. |
| D10 | Hook modes always exit 0. `HookStop` prints `{"systemMessage": "..."}` only when something needs reporting (NEW, UNKNOWN or fault-shaped). A top-level catch turns every internal failure into exit 0 plus an UNKNOWN notice. `stop_hook_active` changes nothing, because the hook never blocks. | Q7; must-address (2); M-1 measured `systemMessage` visibility. |
| D11 | Snapshot file: in hook mode, `<SnapshotDir or [IO.Path]::GetTempPath()>\claude-drive-root-<session_id>.json`. `session_id` must match `^[A-Za-z0-9_-]{1,128}$`, otherwise UNKNOWN and nothing is written. Created with `FileMode.CreateNew`: an existing valid snapshot (resume, compact, or a second registration) is a no-op. In any mode, a snapshot path whose parent is a monitored root, or that lies under the H4 trees (plus any additive `-ProtectedPath`), is refused as UNKNOWN. | Must-address (3) isolates sessions. AC6's single-file exception. First writer wins, so a double run is harmless. |
| D12 | Repeated Stop: `HookStop` opens the snapshot with `FileShare.None`. It announces only children not yet in the snapshot's `reported[]`, then appends them. If the file is locked by a concurrent instance, it exits 0 silently. Standalone `Compare` ignores `reported[]` and always lists every new child. A missing or invalid snapshot is announced on every Stop, because there is no state to dedupe against. | Must-address (3). One notice per child per session, while the standalone check stays authoritative. |
| D13 | A root present now but absent from the snapshot (a newly mounted drive) → UNKNOWN for that root. A snapshot root that is now unreadable or missing → UNKNOWN. | Must-address (4); M4. |
| D14 | `faultShapedPresent[]` lists every existing single-letter direct child of a monitored root (the `X:\<letter>` fault shape). It is reported as a standing warning in the JSON and in the Stop notice (once per session). It does not change the exit code. | Must-address (1): writes beneath an *existing* child are invisible to a delta check. This flags the one shape where that blindness matters. AC5's exit 0 is preserved. Today no such child exists (input §1). |
| D15 | Registration placement: the monitor hooks are registered at **user level only** (`C:\Users\aviha\.claude\settings.json`: `SessionStart` → `HookSessionStart`, `Stop` → `HookStop`, `timeout` 30). The project `.claude/settings.json` is unchanged. The guard needs no new registration, since it is already on `Bash\|PowerShell` at both levels. | Hooks merge across levels: project + user would run twice in this repository and still miss sessions elsewhere. D11/D12 make an accidental double registration harmless anyway. For the guard, deny-wins makes the double run harmless, and the user-level copy enforces the rule even in a checkout whose project copy is older. |
| D16 | Test placement. Guard cases go in `tests/test_guard_destructive_command.py` (guard-hook shards, Linux pwsh, no-skip proof). Monitor tests go in a new `tests/test_drive_root_monitor.py`, run by `pytest-core`. It is **not** host-parametrized at collection: each test loops over the available hosts in its body, so its node count is machine-independent. It **fails**, not skips, when no host exists. | Neither `ci.yml` nor `tests/test_ci_expansion_contracts.py` changes (`test_together_the_two_test_jobs_cover_every_test_file` keeps holding). No entry in `ENVIRONMENT_DEPENDENT_PYTEST_FILES`, so `generate_test_inventory.py` stays untouched. A missing pwsh reds instead of false-greening. |
| D17 | Q3a fixture change: `outcome()` (test line 87) gains `tool_name: str = "Bash"`, and every builder that models a real tool call adds `"tool_name": "Bash"`. Sites that deliberately model malformed payloads (line 692, the line 942 list) keep their shape. No expected decision changes. | Only lines 200/201 carry a converted-position drive token today (grep, clone blob). Line 872 already expects deny. |

**Scope**
- **In**: D1–D6 in the guard and its header docstring; the D7–D14 monitor; tests per the mapping
  below; regenerated `docs/test_inventory/`; the user-level installation and registration (D15);
  operational acceptance; evidence and this document.
- **Out**: everything Section 0 lists as out of scope (except the superseded installation bullet);
  any `ci.yml`, `scripts/**`, `.claude/settings.json` (project) or general-policy edit; refusing
  Write/Edit/MCP parameters; `\d\x` and `/tmp/x` forms; any change to the shared checkout
  `D:\development\Hypertrophy-Toolbox-v3-main` (its locally modified `.claude/settings.json` and
  guard stay untouched).

**Artifacts**
| Path | Change | Notes |
|---|---|---|
| `.claude/hooks/guard-destructive-command.ps1` | modify | D1–D6. Pure ASCII + UTF-8 BOM; exit 2 is the only block; header gains a "Drive-token rule" paragraph. |
| `.claude/hooks/drive-root-monitor.ps1` | new | D7–D14. Pure ASCII + UTF-8 BOM; header documents modes, exit codes and the D15 user-level registration snippet. |
| `tests/test_guard_destructive_command.py` | modify | D17 fixture change; case-table and P-row tests. |
| `tests/test_drive_root_monitor.py` | new | M-, H- and S-rows below. |
| `docs/test_inventory/TEST_INVENTORY.md`, `.json` | regenerate | New file's per-file count, by the generator only. |
| `docs/msys_destination_validation/PLANNING.md` | modify | This plan, then Plan v2 and evidence. |
| `artifacts/msys-ac7-<UTC>/` (gitignored) | new | AC7 arms, junit, patches, hashes. |
| `C:\ht\MSYS-INSTALL\backup-<UTC>\` | new, outside repo | Pre-install backups and hash records. |
| `C:\Users\aviha\.claude\hooks\guard-destructive-command.ps1` | replace at install | Byte-equal to the merged blob. |
| `C:\Users\aviha\.claude\hooks\drive-root-monitor.ps1` | new at install | Byte-equal to the merged blob. |
| `C:\Users\aviha\.claude\settings.json` | modify at install | Adds the `SessionStart`/`Stop` entries only. |

**Effort**: L · **Owner**: main session (manager, under the 2026-10-28 delegation) · **Depends on**: none (#510 merged).

**Sequence**
0. **Base and pre-measurements.** Re-fetch `origin/main` in `C:\ht\MSYS`. Record the full SHA and,
   if it moved past `c29ddf07…`, rebase the still-empty branch onto it (AC8). Measure read-only:
   - S0-a: in the Bash tool, is a plain argument `x=/d/y` converted? This sets D4's `NAME=` scope.
   - S0-b: is a `subst` drive reported as `DriveType Fixed`? This affects the Q5 limit wording and
     the operational probe.
   - S0-c: the exact form of the user-level guard registration (settings line ~126–130).
   - S0-d: record the H4 trees' creation times.
1. **Guard tests first.** Apply D17, then add the case-table and P-row tests. On base + tests, every
   refuse row and P1 must fail and every allow row must pass. Retain that run as the pre-control
   evidence.
2. **Guard rule.** Implement D1–D6. Run the new cases, then the full guard file under `powershell`
   and `pwsh` locally. Every pre-existing case keeps its expected decision.
3. **Monitor tests, then monitor.** Write `tests/test_drive_root_monitor.py`, confirm it fails
   against a stub, then implement D7–D14.
4. **Gates.** Regenerate the inventory and `--check`. Run the pyright baseline diff, Lint, the
   targeted pytest set (below) and the S0-d H4 post-run check.
5. **AC7 arms** (below) on the exact candidate commit.
6. **Diff-time review**: `code-reviewer` (required by the AI-workflow row) plus the manager's
   self-review. A review that did not run is recorded as incomplete.
7. **Commit, push, PR** (delegated). Wait for required checks green: Run Tests fan-in, Test
   Inventory Drift, Type Check, Lint and the rest. Then merge without `--delete-branch` (branch
   deletion is out of scope). Record the merge SHA → *merge* level.
8. **Installation** (below) → *installation* level.
9. **Operational acceptance** (below) → *operational* level.
10. Record all four levels with evidence paths in this document and the handover. Never declare
    `PREVENTION_COMPLETE`.

**Expected gates** (to be confirmed by `test-strategist`)
- AI workflow / agent config (`.claude/**`): source behaviour changes, so the tests run.
  `code-reviewer` is required.
- Tooling / scripts: not triggered (no `scripts/**` change, D7).
- pytest: `tests/test_guard_destructive_command.py` (full, both hosts locally; four Linux pwsh
  shards in CI), `tests/test_drive_root_monitor.py`, `tests/test_agent_workflow_contracts.py`
  (registrations execute the guard), `tests/test_ci_expansion_contracts.py` and
  `tests/test_worktree_ci_contracts.py` (CI accounting unchanged).
- Test Inventory Drift: regenerate for the new file; `--check` exits 0. The guard file is
  environment-dependent and uncommitted, so its larger count is not drift.
- Type Check: the pyright baseline diff shows no net-new diagnostics in the two test files.
- Guard-hook CI fan-in: new guard cases land in the existing round-robin shards. `verify` (no skips)
  and `union` (every identity once) cover them with no workflow change. Expect roughly 60 extra
  pwsh processes spread across four legs against the 20-minute leg budget; record the measured leg
  times from the PR run.
- e2e: none.

**Test mapping** (AC → tests; every case-table row → one test id)

| AC / row | Test(s) | Notes |
|---|---|---|
| A1–A13 | `test_drive_token_case_table[A1…A13]` × host | A10 splits into A10a–d. A9 asserts the overall deny comes from the existing rule and that no drive-token reason is in stderr. A6 is also the pre-existing line 201 case. |
| R1–R14 | `test_drive_token_case_table[R1…R14]` × host | R12 has two variants: absent and unknown `tool_name`. Each asserts deny and that stderr names the token. |
| L1–L4 | `test_drive_token_case_table[L1…L4]` × host | Pins the limits as `allow`, so a future change to them is visible. |
| L5 | M-2 measurement only | Harness behaviour; no automated test can exercise it. |
| P1 | `test_drive_token_resolution_message` | `cwd` `D:\…` → `D:\d\…`; `C:\…` → `C:\d\…`; missing, empty, UNC or garbage → deny with "no resolved path is claimed". |
| P2 | `test_drive_token_profiles_and_modes` | Deny in `agent`/`main` × `default`/`auto`/`bypassPermissions`/`plan`; an ask elsewhere in the command cannot mask it. |
| P3 | `test_drive_token_converted_positions` | `OUT2=--o=/c/y` allow; `> /d/x` allow; `>/d/x` deny (fail-closed); `x=/d/y` per S0-a. |
| P4 | `test_drive_token_accepted_false_positives` | Pins: Bash `git commit -m "see /d/x"` deny (Q3b); `rmdir /s/q tmp` deny (combined switches); unquoted `powershell -Command New-Item /d/x` deny. |
| P5 | `test_drive_token_refused_payload_never_executes` | Pattern of test line 932, with an R-row command and a `tmp_path` sentinel. |
| P6 | `test_drive_token_nesting_depth_denies` | Five-level delegation → deny. |
| AC3 | the full pre-existing guard file on the candidate; `test_hook_source_is_ascii_with_bom[*]` (now including the monitor file); internal-error cases exit 2; `test_agent_workflow_contracts` registration probes | Reviewer checks the diff: no pre-existing expected value edited. |
| M1 | `test_new_child_reported_despite_red_audit_fixture` | A failing audit-report fixture sits beside the root; the monitor ignores it. Plus a static check that the script never references `audit-worktrees` or the baseline file. |
| M2 | `test_no_new_child_exits_zero` | Including `faultShapedPresent` non-empty → still 0 (D14). |
| M3 | `test_removed_child_not_reported_as_new` | |
| M4 | `test_unknown_cases` | Missing root; unreadable root (POSIX `chmod 000`, skipped when euid 0 or on Windows ⚠️); missing, invalid-JSON and wrong-schema snapshot; newly discovered root (D13). |
| M5 | `test_monitor_is_read_only` | Root entries, `CreationTime`/`LastWriteTime` unchanged (LastAccess excluded); only the snapshot file written; a snapshot path that is a direct child of a root, or protected → UNKNOWN, nothing written. |
| H1 | `test_hook_session_start_creates_once` | A second SessionStart (resume, compact, double registration) is a no-op. |
| H2 | `test_hook_stop_reports_new_child_exit_zero` | `systemMessage` names the exact path. |
| H3 | `test_hook_stop_dedupes_per_session` | A repeated Stop gives no repeat; a later second child is announced. |
| H4 | `test_hook_stop_never_exits_two` | Malformed payload, invalid `session_id`, missing/invalid snapshot, forced internal error → exit 0 plus UNKNOWN. |
| H5 | `test_sessions_are_isolated` | Two `session_id`s, two files; neither reads the other. |
| H6 | `test_hook_stop_skips_when_locked` | The test holds an exclusive lock → exit 0, no output, file unchanged. |
| H7 | `test_standalone_compare_ignores_reported` | Exit 10 after the hook has already announced. |
| H8 | `test_default_roots_are_fixed_volumes` | Windows only (skipped elsewhere): the shape is `X:\` and the list is non-empty. Not run in CI ⚠️. |
| AC6 H4 | S0-d before/after record | A read-only local check on the real machine, retained in evidence. |
| AC7 | the arms below | |
| AC8 | base SHA record (S0) | |
| AC9 | inventory `--check`, pyright diff, CI run links | |
| AC10 | merge SHA; install hash table; operational transcript | |

**AC7 neutralization** (in an isolated archive at a short path outside `D:\development`)
- `git archive <candidate SHA>`, extracted to `C:\ht\MSYS-AC7\restored\` and
  `C:\ht\MSYS-AC7\neut-guard\`, `…\neut-monitor-new\`, `…\neut-monitor-unknown\`. Run with the
  clone's `.venv` Python, with the archive root as cwd and on `PYTHONPATH`.
- `neut-guard`: a retained `git apply` patch replaces the body of `Invoke-DriveTokenScan` with
  `return`. Expected: every R-row, P1–P6 drive-token deny assertion and P5 fail. A-rows and L-rows
  pass.
- `neut-monitor-new`: the new-children diff function returns empty. Expected: M1, H2, H3 and H7
  fail.
- `neut-monitor-unknown`: UNKNOWN detection returns none. Expected: M4 and the H4 UNKNOWN variants
  fail.
- Read-only arm `neut-monitor-write`: the patch adds a write into the first root. Expected: M5
  fails.
- Hook arm `neut-hook-exit`: the patch makes the catch `exit 2`. Expected: H4 fails.
- `restored`: unpatched. Every test passes.
- Retained under `artifacts/msys-ac7-<UTC>/`: candidate SHA; SHA-256 of each arm's patched file;
  each patch; command lines; junit XML; exit codes; and a summary table of expected-fail versus
  observed-fail per test id. An arm whose expected test does not fail blocks the merge.

**Installation** (AC10; authorized by the delegation)
1. Back up byte-for-byte to `C:\ht\MSYS-INSTALL\backup-<UTC>\` with SHA-256:
   - user-level `settings.json` and `hooks\guard-destructive-command.ps1`;
   - a read-only hash record of the shared checkout's `.claude\settings.json` and guard (not
     modified).
2. Materialize the merged blobs by OID with `git cat-file blob` (bytes, no autocrlf). Copy them to
   `C:\Users\aviha\.claude\hooks\` and verify that each SHA-256 equals the blob-derived hash. Record
   the per-copy table: user-level guard, user-level monitor, clone guard, and the shared-checkout
   guard ("locally modified, not updated; user-level copy enforces").
3. Edit user `settings.json` with a minimal textual insertion of the D15 entries, in the S0-c form.
   Parse it before and after, and assert structural equality apart from the added `SessionStart`
   and `Stop` entries. Existing entries are appended to, never replaced.
4. Rollback: restore the backups byte-for-byte and re-verify the hashes.

**Operational acceptance** (fresh headless session, disposable cwd `C:\ht\MSYS-OPS\cwd`)
- Guard: the session runs R3 `[IO.Path]::GetFullPath('/c/Users/x')` through the PowerShell tool. It
  is a pure computation, harmless even if allowed. Pass = the hook denial names `/c/Users/x` and
  `C:\c\Users\x`.
- Monitor: SessionStart creates `claude-drive-root-<session_id>.json` in TEMP, and the first Stop
  is silent (CLEAN). Then the session overwrites *its own* snapshot with invalid JSON (a
  monitor-owned disposable file), and the next Stop must show an UNKNOWN notice. If S0-b shows
  `subst` drives as Fixed: map `subst Q:` to `C:\ht\MSYS-OPS\qroot` before the session, create
  `Q:\probe-child` mid-session, expect a NEW notice naming it, then remove the child and the
  mapping. This touches no real drive root.
- Retain the stream-json transcripts. VS Code panel rendering stays unmeasured ⚠️.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a96acae55b870d077` | ID supplied by the manager. The same agent revised Section 0 on 2026-10-28 and recorded Gate 0. |
| `product-manager` — response matrix + Plan v2 | `a96acae55b870d077` | Same agent, resumed by the manager. |
| `architecture-reviewer` | `aaf09a27b405eb90f` | Round 1: "Needs revision" (2 B, 10 S, 5 N). Round 2 (same agent, resumed): no blocking (5 S, 6 N). |
| `test-strategist` | `a344c4ffa667a08e7` | Round 1: "not ready for Gate 1 as written" (4 B, 10 S, 6 notes). Round 2 (same agent, resumed): blocking TS2-B1/B2/B3 (+4 S, 2 notes). Round 3 (same agent, resumed): no blocking (6 S, 5 N). |
| `product-risk-reviewer` | `a687e7ec870ed0106` | Round 1: "Needs revision" (1 B, 7 S, 5 N). Round 2 (same agent, resumed): no blocking (NEW-1…NEW-7). |

**Same product-manager resumed for the matrix + Plan v2?** `yes` — the manager resumed the Plan v1
agent `a96acae55b870d077`.

**Evidence gap**: none, for all rounds.
- Round 1: every reviewer returned blocking findings, so all three ran a round-2 delta review
  (the same three agents, resumed).
- Round 2: only test-strategist returned blocking findings, so round 3 was a test-strategist-only
  delta review (`a344c4ffa667a08e7`, resumed).
- Round 3: no blocking findings.

---

## Reviewer findings

Round 1, 2026-10-28. The verbatim reports are in
`docs/msys_destination_validation/reviews/round1-<role>-<id>.md`, copied from
`artifacts/msys-council/round1-<role>-<id>.md` (gitignored). The manager made the copies
byte-for-byte. SHA-256 as reported by the manager:
- architecture-reviewer: `d8dab0f0a3d5b6993c51df8681a621367eb7013fcec1a8dedf705a3c7cc096ac`
- test-strategist: `f776977f26aa6776c574e81c2bad25a6859a075b55742ec112295ee1393820e1`
- product-risk-reviewer: `6dcbd244637ac2fafc84bcd7db53665d5876434e208b0394c09bebebfb5f29de`

The lines below are summaries for navigation only.

### architecture-reviewer (agent `aaf09a27b405eb90f`)
Verbatim: `docs/msys_destination_validation/reviews/round1-architecture-reviewer-aaf09a27b405eb90f.md`
- AR-B1 (blocking): P6 cannot fail under the guard arm, because the existing depth deny fires first.
  The plan's merge rule would therefore block itself.
- AR-B2 (blocking): D1 ("called once at the entry point") cannot deliver D5(ii)'s re-scan of
  delegated bodies. Recursion ownership is unspecified.
- AR-S1: M-6 shows any `<word>=` prefix converts. D4's regex refuses `a=b=/d/y`, and S0-a is now
  decided.
- AR-S2: M-7 (`subst` is a fixed volume) contradicts the Q5 limit text and the conditional
  operational probe.
- AR-S3: M-9 resume keeps `session_id`, so the baseline goes stale. Invalid-file handling at
  SessionStart is undefined.
- AR-S4: SessionStart and Stop stdout are model-visible channels and are not pinned.
- AR-S5: PowerShell-tool prose (here-strings, `-m`, `--body`) is refused with no remedy in the
  message.
- AR-S6: the P4 `rmdir /s/q tmp` row names no tool or region. The cmd combined-switch idioms need
  pinning or exclusion.
- AR-S7: `python -c` / `node -e` detection is too narrow (`.venv/Scripts/python.exe`, `-I -c`,
  `--input-type`).
- AR-S8: installation replaces a live guard, which fails open on a parse error, non-atomically.
- AR-S9: the documentation surface is not named. `docs/MASTER_HANDOVER.md` is shared state and is
  not in Artifacts.
- AR-S10: enumeration semantics are unspecified (hidden/system entries, reparse points, case,
  errors).
- AR-N1: the guard runs up to three times (project, user, charter), not two.
- AR-N2: the list of payload sites without `tool_name` is incomplete
  (`test_agent_workflow_contracts.py:295,561`, `worktree_cleanup/guard-contract.ps1:39`). No edits
  are needed.
- AR-N3: the monitor's Windows PowerShell 5.1 behaviour is verified locally only, and H8 is not in
  CI. State this.
- AR-N4: print the notice first, then record `reported[]`.
- AR-N5: a concurrent session's legitimate root child appears in every open session. Add it to the
  limits.

### test-strategist (agent `a344c4ffa667a08e7`)
Verbatim: `docs/msys_destination_validation/reviews/round1-test-strategist-a344c4ffa667a08e7.md`.
The report leaves its notes unnumbered; TS-N1 to TS-N6 are this PM's labels, in bullet order.
- TS-B1 (blocking): the AC7 arms do not cover each control, and nothing can fail on the allow side.
  It proposes per-control arms in both directions.
- TS-B2 (blocking): D4 and D5 contradict each other. D5(i)/(ii) have no observable effect, and
  `bash -c "… -D /d/x"` is undefined.
- TS-B3 (blocking): P6 cannot fail under the guard arm (same as AR-B1).
- TS-B4 (blocking): the built-in protected-path test would write into the real H4 trees when
  neutralized.
- TS-S1: D4's prefix disagrees with M-6. S0-a and S0-b are stale.
- TS-S2: deny assertions can pass for the wrong reason (exit 2 from the catch). P5's sentinel is
  vacuous.
- TS-S3: SessionStart stdout becomes model context. H1 must assert empty stdout in every path.
- TS-S4: Windows/Linux divergence: H6 lock (`flock`), M4 unreadable root (`icacls`), pyright on
  `os.geteuid` / `fcntl`.
- TS-S5: evidence covers only one host. Bad arguments exit 1 under a typed `param()`, not 11.
- TS-S6: forcing an internal error has no defined seam.
- TS-S7: concurrency was measured (M-9) but the tests are sequential. Add H1c with concurrent
  `Popen`.
- TS-S8: isolation from real roots is a convention. Use a single `run_monitor` helper, a print-only
  H8, and non-Windows with no `-Root`.
- TS-S9: timing and collection hygiene: `-k` per arm, a measured case count, plain ids, a missing
  host failing in the body.
- TS-S10: D14 has no test (H9). The missing-snapshot notice repeats every turn, and resume leaves a
  stale baseline.
- TS-N1: R12 variants `"bash"`, `null`, non-string, `"Bash "`.
- TS-N2: M1's static check must ignore comments.
- TS-N3: compare case per host. Reported path = root as given + child name.
- TS-N4: record measured Stop latency against the 30 s timeout.
- TS-N5: `workflow-contracts-windows` does not exercise the monitor. State this as an accepted gap.
- TS-N6: gates that apply without action: machine-independent monitor count; no `conftest.py`
  change.

### product-risk-reviewer (agent `a687e7ec870ed0106`)
Verbatim: `docs/msys_destination_validation/reviews/round1-product-risk-reviewer-a687e7ec870ed0106.md`
- PR-B1 (blocking): the refusal text claims a resolved path that is false or unknowable
  (conservative refusals, a `cd` in the command, read-only R3, "would create").
- PR-S1: token-boundary false positives (globs, pathspecs, `%VAR%`, `${VAR}`, `(expr)`, JS regex
  literals, `sed`). Corpus pass requested.
- PR-S2: prose triggers refusals with no recovery path. The message should offer `-F` /
  `--body-file`.
- PR-S3: a missing snapshot is announced on every Stop. Baseline mid-session and announce once.
- PR-S4: notices must not imply causation. Exact wording is proposed.
- PR-S5: the live user-level guard swap affects every session and repository. Requested: staged
  probe, atomic replace, rollback commands, ordering, and edits limited to `hooks`.
- PR-S6: `subst` is global to the logon session. Use a proven-unused letter and a short window,
  and record the other-session notices.
- PR-S7: the AC10 operational wording is stronger than the evidence (headless, substitute root,
  one row). Installation is done by the manager.
- PR-N1: if VS Code omits or renames `tool_name`/`cwd`, strict Q3a refuses drive-token commands.
  Measure it or accept the risk.
- PR-N2: state that the scan sits inside the existing try/catch, and add a forced-exception P-test.
- PR-N3: snapshots accumulate in TEMP. Document this and do not delete them.
- PR-N4: record measured Stop-hook latency.
- PR-N5: a newly mounted drive gives a one-time UNKNOWN in every open session. Document it.

### Manager's own findings (MG)
Named in `artifacts/msys-council/round1-dispositions.md`. The dispositions file carries no separate
MG text beyond the resolutions that cite MG.
- MG-1 (in R2): a Bash heredoc or here-string body is stdin and is never converted. Plan v1 did not
  scan it as Unconverted.
- MG-2 (in R4): further boundary exclusions beyond PR-S1 (`~`, `$`, `}`, `)`, `]`, `*`, `%`), plus
  the corpus pass.
- MG-3 (in R7): the manager's contribution to the snapshot lifecycle and concurrency resolution.

### Round 2 — delta review of Plan v2 (2026-10-28; same three agents, resumed)

The manager copied the verbatim reports byte-for-byte to
`docs/msys_destination_validation/reviews/round2-<role>-<id>.md`. SHA-256 as reported by the
manager:
- architecture-reviewer: `0eded07eb3eb2d8f1314cc4a2b91cd23bc8d17d3df1e88b00c67d5ebedd97447`
- test-strategist: `719dbac70c894fb06c843cc73949d53a0a4a31f8cc8911307f28154a75c2cf65`
- product-risk-reviewer: `f2ed9fd314c08dbf15cfad0d53a75714619e1f45bdf8a35a8142a96ff264ff6e`

Verdicts: architecture — no blocking; product-risk — no blocking; test-strategist — blocking
TS2-B1/B2/B3. The reviewers number their own findings `S-n`, `N-n` and `NEW-n`. This list prefixes
them AR2-, PR2- and TS2- (TS2-N1/N2 are this PM's labels for TS's two unnumbered notes).

**architecture-reviewer (`aaf09a27b405eb90f`)** — `reviews/round2-architecture-reviewer-aaf09a27b405eb90f.md`
- AR2-S1 (should-fix): D7 withholds the resolved path beyond must-address (5). Keep a conditional
  clause, and match `cd`/`sl` on word boundaries.
- AR2-S2 (should-fix): R20 refuses a `NAME=` word that AC2 allows. State the AC1(b)-over-AC2
  precedence.
- AR2-S3 (should-fix): D5(i) "`-c` anywhere" misclassifies tool options (`python -m pytest -c …`).
- AR2-S4 (should-fix): no subagent payload was measured. Measure one (now M-11).
- AR2-S5 (should-fix): M-10 makes the "VS Code not measured" statements stale.
- AR2-N1: D4 must say that occurrences are found with D3's token and boundary rules.
- AR2-N2: the snapshot schema is unspecified (version, roots, announce state).
- AR2-N3: M-lock discrimination is host-dependent. Prove it on Windows only.
- AR2-N4: heredoc prose (`git commit -F - <<EOF`) is refused but not pinned; the remedy should
  name the Write tool.
- AR2-N5: the corpus pass has no blocking rule.
- AR2-N6: the hard-coded H4 paths in `protected[]` are acceptable as print-only.

**test-strategist (`a344c4ffa667a08e7`)** — `reviews/round2-test-strategist-a344c4ffa667a08e7.md`
- TS2-B1 (blocking): M-lock lists H1c, which can pass under the mutation (non-deterministic).
- TS2-B2 (blocking): expected sets are incomplete or contradict the tests (G-noop, G-region,
  G-interp, G-offset/P6a, M-new, M-fault/M2, M-write placement, M-sessionfile, M-sessionid ids).
- TS2-B3 (blocking): merged single nodes make expectations unobservable. Split P1, P3, H1, H4, M4.
- TS2-S1 (should-fix): no arm covers the protected-path or root-parent refusals.
- TS2-S2 (should-fix): the once-per-session state for the fault, new-drive and mid-session notices
  has no field, test or arm.
- TS2-S3 (should-fix): the `icacls /deny` test needs cleanup in `finally`.
- TS2-S4 (should-fix): each arm's `-k` selection must include both columns.
- TS2-N1 (note): is M6's UNKNOWN in M-unknown's scope?
- TS2-N2 (note): fix `-k` and node granularity together.

**product-risk-reviewer (`a687e7ec870ed0106`)** — `reviews/round2-product-risk-reviewer-a687e7ec870ed0106.md`
- PR2-NEW-1 (should-fix): the conservative remainder contradicts its first sentence.
- PR2-NEW-2 (should-fix): "since this session started" is wrong after resume/clear/mid-session.
  Several UNKNOWN cases lack exact texts.
- PR2-NEW-3 (should-fix): the P4f remedy is wrong for JS regexes, and the corpus pass has no
  action threshold.
- PR2-NEW-4 (note): `cd` detection must be word-bounded. Add a P1 pair.
- PR2-NEW-5 (should-fix): the `settings.json` edit has a lost-update race and a reserialization
  hazard.
- PR2-NEW-6 (should-fix): M-10 makes the operational binary, label, PR-N1 row and limit stale.
- PR2-NEW-7 (note): `python tool.py -c /d/x` is a false positive; per-position conservativeness
  (consider later); non-ASCII token echo; the remedy should use the token's letter.

### Round 3 — delta review of Plan v2 rev. round 2 (2026-10-28; test-strategist only, resumed)

Verbatim: `docs/msys_destination_validation/reviews/round3-test-strategist-a344c4ffa667a08e7.md`.
SHA-256 as reported by the manager:
`e8d28a7b0895e408bf8fb53cb7bf1c8102a8f9594ec3de404ece074c1ebbbb1b`.

Verdict: **no blocking findings**. All round-2 findings are resolved; TS2-B2 (M-write) and TS2-S2
are resolved with caveats, which TS3-S5 and TS3-S3 address.
- G3-1 (on the PM note): as worded, G-optvalue is not single-purpose, because `-c` itself becomes
  a non-option. Reword it so the value counts as the first non-option argument and `-`-tokens
  remain options. Add a node row.
- TS3-S1 (should-fix): H6 and H1-held can pass under M-lock unless an unlocked run would visibly
  act.
- TS3-S2 (should-fix): H5 has no stated scenario.
- TS3-S3 (should-fix): M-dedupe-midsession is inert unless `announced` is the sole gate.
- TS3-S4 (should-fix): G-sanitize may pass falsely on Windows (console encoder substitution).
- TS3-S5 (should-fix): M-write is only exercised if M5 runs `Compare` against a valid snapshot.
- TS3-S6 (should-fix): the over-refuse and allow-side controls have no arm. Five arms proposed.
- TS3-N1: P2, P5 and P7 need node ids.
- TS3-N2: no row covers the node value options.
- TS3-N3: P6a needs a concrete `eval`/`$()` chain, proven on the base guard.
- TS3-N4: distinguish a sharing violation (silent) from other open failures.
- TS3-N5: define the scope of "every test passes on `restored`".

---

## Response matrix

Dispositions were made by the **main session acting as manager under the owner's 2026-10-28
delegation**, not by the owner. Source: `artifacts/msys-council/round1-dispositions.md`. "R*n*"
means that file's resolution *n*; case-table rows are written "Case R*n*". No finding is deferred.
One sub-item is rejected (PR-S1, marked below). The manager's later rulings on the PM flags F1–F10
(end of Plan v2) amended the rows marked "F*n* ruling".

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| AR-B1 | architecture-reviewer | accept (R14) | P6 split: P6a (4-level nested Case-R row → drive-token reason, in G-noop's expected-fail set); P6b (5-level → existing nesting reason; a pin in no expected-fail set). |
| AR-B2 | architecture-reviewer | accept (R1; F4 ruling) | D1: `Invoke-DriveTokenScan` owns its recursion and uses existing helpers read-only; `Invoke-CommandScan` is never edited. D5(iii): its own `$(...)` extraction mirrors `Invoke-CommandScan`'s loop without calling it. |
| AR-S1 | architecture-reviewer | accept (R3) | D4 prefix `^(?:[A-Za-z0-9_.-]+=)*(?:-[A-Za-z]+)?$`; P3 rows; S0-a deleted (M-6). |
| AR-S2 | architecture-reviewer | accept (R12) | Q5 wording corrected post-Gate-0; operational `subst` probe made unconditional. |
| AR-S3 | architecture-reviewer | accept (R7; F1 ruling) | D14 `source`-keyed lifecycle, written in place under an exclusive handle on the single snapshot file (no temp, no lock file); invalid file never overwritten at Stop; H1 variants. |
| AR-S4 | architecture-reviewer | accept (R8) | D13: SessionStart stdout always empty; Stop stdout empty or exactly one `{systemMessage}`. |
| AR-S5 | architecture-reviewer | accept (R5) | D7 fixed template with remedy text; P4b covers PowerShell prose. |
| AR-S6 | architecture-reviewer | accept (R6) | P4 rows name tool/region; cmd combined switches pinned as accepted FPs, remedy "separate switches with spaces". |
| AR-S7 | architecture-reviewer | accept (R1 had made it moot; reinstated by the F4 ruling) | D5(i) restored: python-family verbs via `Get-VerbCandidates` (incl. `.venv/Scripts/python.exe`, `python3.x`), `-c` anywhere incl. `-Ic`; `node -e\|--eval\|-p\|--print`; Cases A15, R17, R20. |
| AR-S8 | architecture-reviewer | accept (R11) | Installation: staged parse + probe, `.new` + hash + `Move-Item -Force`, immediate re-probe, same sequence for rollback. |
| AR-S9 | architecture-reviewer | accept (R19) | Hook headers + new `docs/msys_destination_validation/CLOSEOUT.md`; `MASTER_HANDOVER.md` not edited; second docs-only PR. |
| AR-S10 | architecture-reviewer | accept (R10) | D11 enumeration semantics. |
| AR-N1 | architecture-reviewer | accept (R20) | D19 wording: up to three guard runs. |
| AR-N2 | architecture-reviewer | accept (R20) | D21 lists the extra sites; no edits. |
| AR-N3 | architecture-reviewer | accept (R20) | Stated as accepted gaps in Expected gates. |
| AR-N4 | architecture-reviewer | accept (R7) | D15: print, then record. |
| AR-N5 | architecture-reviewer | accept (R9) | Plan v2 coverage limits. |
| TS-B1 | test-strategist | accept (R15) | AC7 arm table, per control, both directions, both hosts (see PM flags F5–F8). |
| TS-B2 | test-strategist | accept (R1; F4 ruling) | Delegated-body and interpreter-code-body words exempt from D4. D5(i) is now observable through Case R20 (`python -c "x=/d/y"`, which D4 alone would allow) and the G-interp arm. Cases A14, A15, R15–R17, R20. |
| TS-B3 | test-strategist | accept (R14) | As AR-B1. |
| TS-B4 | test-strategist | accept (R16) | Protected-path tests only via `-ProtectedPath` under `tmp_path`; print-only `protected[]` asserted; never neutralized against a real path. |
| TS-S1 | test-strategist | accept (R3, R12) | As AR-S1 and AR-S2. |
| TS-S2 | test-strategist | accept (R17) | `outcome_with_stderr()`; fixed deny-reason prefix; A/L rows assert neither "failing closed" nor the prefix; P5 documented as non-discriminating. |
| TS-S3 | test-strategist | accept (R8) | As AR-S4; H1 asserts empty stdout in every path. |
| TS-S4 | test-strategist | accept (R18) | `fcntl.flock` via `importlib` on POSIX, plain handle on Windows; `icacls /deny` / `chmod 000`; `getattr(os, "geteuid", None)`. |
| TS-S5 | test-strategist | accept (R15, R18) | Arms under both hosts; monitor parses `$args`; bad args → 11 (M7). See PM flag F8. |
| TS-S6 | test-strategist | accept (R18) | Forced-error seam = `-SnapshotDir` pointing at a regular file. |
| TS-S7 | test-strategist | accept (R7; F1 ruling) | The snapshot file is its own exclusive lock (no separate lock file); H1c concurrent `Popen`; H6. |
| TS-S8 | test-strategist | accept (R18) | `run_monitor` helper + bypass check (M8); `ListRoots` for H8; non-Windows with no `-Root` → 11 (H8b). |
| TS-S9 | test-strategist | accept (R15, R18) | `-k` per arm; full guard file once on `restored`; plain ids; missing host fails in body; measured count replaces "≈60". |
| TS-S10 | test-strategist | accept (R7, R15) | H9 + M-fault arm; mid-session baseline (H10); re-snapshot on `resume`. |
| TS-N1 | test-strategist | accept (R20) | Case R12 variants. |
| TS-N2 | test-strategist | accept (R20) | M8 static check on non-comment tokens. |
| TS-N3 | test-strategist | accept (R20) | M9. |
| TS-N4 | test-strategist | accept (R20) | Stop latency in operational evidence. |
| TS-N5 | test-strategist | accept (R20) | Accepted gap stated. |
| TS-N6 | test-strategist | accept — informational | No action. |
| PR-B1 | product-risk-reviewer | accept (R5; F2/F3 rulings) | D7 ASCII template. "Conservative" is defined (Bash-reached `powershell`/`pwsh`/`cmd` bodies and interpreter code bodies) and has its own first sentence. *(Round-1 "resolved clause only under the stated conditions" interpretation withdrawn in round 2, AR2-S1. With a drive-letter `cwd` the clause is always present, conditional for a conservative refusal and hedged after a directory change; only a missing or invalid `cwd` gives `cwd unavailable; no resolved path is claimed.` See D7.)* P1. |
| PR-S1 | product-risk-reviewer | accept in part (R4) | Boundary exclusions + Cases A16–A21 + corpus pass accepted. **Rejected sub-item: the JS-regex-literal exclusion.** It would open a seam where `/d/i`-shaped paths escape; `node -e "s.replace(/a/g,'')"` is pinned instead as an accepted false positive (P4f). |
| PR-S2 | product-risk-reviewer | accept (R5) | Remedy text in every refusal, pinned by P1/P4. |
| PR-S3 | product-risk-reviewer | accept (R7; F1 ruling) | Hook-mode mid-session baseline + one notice (H10), created with `CreateNew` under the exclusive handle; standalone stays 11. |
| PR-S4 | product-risk-reviewer | accept (R9) | D18 fixed wording; H2/H9/M9 assert exact phrases. |
| PR-S5 | product-risk-reviewer | accept (R11) | Installation (a)–(e). |
| PR-S6 | product-risk-reviewer | accept (R12) | Proven-unused letter; mapping immediately before/after; other-session notice recorded. Test-only `--settings` alternative not chosen. |
| PR-S7 | product-risk-reviewer | accept (R13) | AC10 levels recorded with the stated limits; VS Code panel rendering left explicitly open. |
| PR-N1 | product-risk-reviewer | accept — risk accepted (R13); narrowed in round 2 (AR2-S4/S5, PR2-NEW-6) | Payload fields (`tool_name`, `cwd`, `session_id`) and the Stop notice were measured on the VS Code extension's bundled `claude.exe` 2.1.310 (headless, M-10) and on CLI 2.1.302 (M-1). A subagent payload carries `tool_name`/`cwd`/`agent_id` (M-11). Panel rendering is unmeasured; charter-frontmatter payloads are an inference. |
| PR-N2 | product-risk-reviewer | accept (R20) | D1 states the try/catch; P8 forced-exception test. |
| PR-N3 | product-risk-reviewer | accept (R20) | Documented in the monitor header; no deletion. |
| PR-N4 | product-risk-reviewer | accept (R20) | Stop latency recorded. |
| PR-N5 | product-risk-reviewer | accept (R9) | Plan v2 coverage limits. |
| MG-1 | manager | accept (R2) | D6 heredoc/here-string rule; Cases R18, R19 (see PM flag F7). |
| MG-2 | manager | accept (R4) | As PR-S1. |
| MG-3 | manager | accept (R7; F1 ruling) | D14/D15: single self-locking snapshot file. |

### Round-2 response matrix

Dispositions were made by the **main session acting as manager under the owner's 2026-10-28
delegation**, not by the owner. All are accepted, except where a row says otherwise. Nothing is
deferred.

| Finding | Reviewer | Disposition | Action in Plan v2, rev. round 2 |
|---|---|---|---|
| AR2-S1 | architecture-reviewer | accept | D7: a conditional resolved clause is always present when `cwd` is a drive path. A word-bounded directory-change hedge is appended. AC1 is now met literally, and the round-1 "withhold" interpretation is withdrawn. |
| AR2-S2 | architecture-reviewer | accept | D5(i) records the delegated reconciliation: for interpreter code bodies, AC1(b) takes precedence over AC2's converted-position allowance (fail-closed per Q3; conservative wording). |
| AR2-S3 | architecture-reviewer | accept | D5(i) recognises the code flag only among interpreter options before the first non-option argument or `-m <module>`. New allow Cases A22, A23. |
| AR2-S4 | architecture-reviewer | accept | M-11 cited: the subagent payload carries `tool_name`/`cwd`/`agent_id`. Charter-frontmatter payloads remain an inference. |
| AR2-S5 | architecture-reviewer | accept | PR-N1 row, coverage limits and operational label updated. Operational acceptance runs on the bundled 2.1.310 binary. |
| AR2-N1 | architecture-reviewer | accept | D4: occurrences are found with D3's token and boundary rules. |
| AR2-N2 | architecture-reviewer | accept | D14 snapshot schema. |
| AR2-N3 | architecture-reviewer | accept | M-lock is proven on the Windows hosts only. |
| AR2-N4 | architecture-reviewer | accept | D7 remedy names the Write tool; P4h `git commit -F - <<EOF` prose row. |
| AR2-N5 | architecture-reviewer | accept | Corpus rule in step 6. |
| AR2-N6 | architecture-reviewer | accept as written | `protected[]` stays print-only; protection is tested only through `-ProtectedPath`. |
| TS2-B1 | test-strategist | accept | AC7 must-fail gating model. M-lock must-fail = H6 + H1-held. H1c is a smoke test in no must-fail set. |
| TS2-B2 | test-strategist | accept | Must-fail sets rebuilt from deterministic single-purpose nodes, applying TS2-B2's corrections: G-noop (P2, P7); either prefix; G-interp patch (both halves); P6a pinned to an R9-style row; M-new (H10, M9); M2 exit-only; M-write after enumeration; M-sessionfile (first 8 characters); H4 ids. Gated expected-pass columns dropped. |
| TS2-B3 | test-strategist | accept | Split nodes: P1a/P1b, P3-allow/P3-refuse, H1 per `source` + H1-held, H4 per variant, M4 per variant incl. M4-newroot. |
| TS2-S1 | test-strategist | accept | Arms M-protected and M-root-parent (under `tmp_path` only). |
| TS2-S2 | test-strategist | accept | `announced` field. A "not repeated" node per kind (H3-once, H9-once, H10-once, H11-newroot-once), and M-dedupe-<kind> arms. |
| TS2-S3 | test-strategist | accept | `icacls` deny removed in `finally`. |
| TS2-S4 | test-strategist | accept | Each arm's `-k` covers its must-fail set and also runs the full drive-token/monitor selection, whose other outcomes are recorded. |
| TS2-N1 | test-strategist | accept | M6 UNKNOWN refusals are outside M-unknown's mutation; M-protected and M-root-parent prove them. |
| TS2-N2 | test-strategist | accept | Done together with TS2-B3/TS2-S4. |
| PR2-NEW-1 | product-risk-reviewer | accept | Conservative clause: `If MSYS does not convert it, from cwd <X:> …`. |
| PR2-NEW-2 | product-risk-reviewer | accept | D18: `since monitoring began at <UTC>`, plus exact texts for every UNKNOWN case and the mid-session baseline. None claims a cause. |
| PR2-NEW-3 | product-risk-reviewer | accept | node regex remedy `use new RegExp(...) or a script file`; corpus blocking rule. |
| PR2-NEW-4 | product-risk-reviewer | accept | Word-bounded, case-insensitive directory-change match; P1a-cdword / P1b-cd pair. |
| PR2-NEW-5 | product-risk-reviewer | accept | Installation step 7: byte-preserving textual insertion, pure-insertion diff, original re-hashed just before `Move-Item`. |
| PR2-NEW-6 | product-risk-reviewer | accept | As AR2-S5. |
| PR2-NEW-7 | product-risk-reviewer | accept in part | `python tool.py -c /d/x` becomes allow Case A23 (not a pinned FP). Non-ASCII echo → `?` (P1a-nonascii). Remedy uses the token's letter. Per-position conservativeness is **not adopted**: conservative stays per body, as the reviewer allowed ("consider later"). |

### Round-3 response matrix

All accepted by the **main session acting as manager under the owner's 2026-10-28 delegation**,
not by the owner. Nothing is deferred or rejected.

| Finding | Reviewer | Disposition | Action in Plan v2 (final, rev. round 3) |
|---|---|---|---|
| G3-1 | test-strategist | accept | Arm G-optvalue: the value of a value-taking interpreter option counts as the first non-option argument, and tokens starting with `-` remain options. Must-fail R21, R22. |
| TS3-S1 | test-strategist | accept | H6 and H1-held create a new child before the locked call, so an unlocked run would visibly act. |
| TS3-S2 | test-strategist | accept | H5 scenario: start session A, create a child, start session B, run Stop for A. A must report the child. |
| TS3-S3 | test-strategist | accept | D15: Stop emits the mid-session notice when `source` is `stop-baseline` and the `midsession` key is absent from `announced`. The arm and H10-once are kept. |
| TS3-S4 | test-strategist | accept | P1a-nonascii uses U+00E9 and asserts that no stderr byte is above 127. |
| TS3-S5 | test-strategist | accept | M5 runs `Compare` against a valid snapshot. |
| TS3-S6 | test-strategist | accept | Arms G-region-unconv (A4–A7), G-prefix (A5, A7, P3-allow), G-exempt-delegated (A14), G-nonoption-anywhere (A22, A23), M-diff-all (M2, M3). |
| TS3-N1 | test-strategist | accept | Node ids for P2, P5 and P7. |
| TS3-N2 | test-strategist | accept | Refuse Case R22 `node --require x -e "x=/d/y"` (conservative). |
| TS3-N3 | test-strategist | accept | P6a built from `eval`/`$()` chains, and its string proven on the base guard in the step-2 red run. |
| TS3-N4 | test-strategist | accept | D14: a sharing violation → silent; any other open failure → UNKNOWN through the top-level catch. |
| TS3-N5 | test-strategist | accept | "Every test passes on `restored`" covers `tests/test_guard_destructive_command.py`, `tests/test_drive_root_monitor.py` and `tests/test_agent_workflow_contracts.py::test_all_effective_destructive_registrations_execute_deny_allow`. |

---

## Plan v2

**Plan v2 (final, rev. round 3)** (2026-10-28). Revised in place to apply the round-2 and
round-3 dispositions, recorded as manager decisions under the owner's delegation (response
matrices above). Superseded wording is replaced; earlier flags and rulings are kept at the end as
history. **Gate 1 was accepted (delegated) on 2026-10-28**; see the Sign-off.

A self-contained revision of Plan v1 that applies dispositions R1–R20. Plan v1 above is kept
unchanged as the audit trail. Section 0's ACs are unchanged. Where Plan v2 applies an AC
differently from its literal text, the PM flagged it. The F-items at the end carry the manager's
rulings.

**Goal**: unchanged from Plan v1. Before anything runs, refuse Bash and PowerShell tool commands
that would hand an unconverted POSIX drive path to a native Windows resolver. Separately, report
any new child on a fixed-volume root during a session, without blocking. Prove both controls in
both directions, and carry them through merge, installation and operational acceptance (AC10).

**Design decisions**

| # | Decision | Source |
|---|---|---|
| D1 | `Invoke-DriveTokenScan($text, $region, $depth)` owns its own recursion. It may call `Split-Segments`, `Remove-Wrappers`, `Get-Delegation` and `Get-VerbCandidates` read-only, and it never edits `Invoke-CommandScan`. Depth beyond `$maxDelegationDepth` denies with a drive-token reason. It is called once per candidate command, inside the existing entry-point `try/catch`, so any exception exits 2. Denials go into `$script:denials`, which keeps deny-wins aggregation. | R1, PR-N2 |
| D2 | Region: a string `tool_name` that is `-ceq 'Bash'` → `Bash`. Anything else is `Unconverted`: `PowerShell`, absent, `null`, non-string, `"bash"`, `"Bash "`, unknown. | Q3a, R20 |
| D3 | `Unconverted` = a raw-text regex over the whole string. Token: `/<letter>/<segment>`, where the segment is one or more characters other than slash, backslash, whitespace, quote, backtick, `,` `;` `)` `]` `}` `\|` `&` `<` `>`. **Repeated slashes after the letter are allowed** (`/d//x`; diff-time CR-2). Boundary: not preceded by `[\w./:\\~*%})\]$]`, **or** preceded by an attached short-option prefix with an optional colon, `(?<=(^\|[\s'"(])-[A-Za-z]+:?)` (PowerShell `-Path:/d/x`; diff-time CR-1). There is no JS-regex-literal exclusion. | AC1, R4, CR-1, CR-2 |
| D4 | `Bash` region: tokens come from `Split-Segments`, with quotes stripped. Occurrences inside a word are found with D3's token and boundary rules (AR2-N1). A drive-token occurrence is converted only at offset 0 of its word, or right after a prefix matching `^(?:[A-Za-z0-9_.-]+=)*(?:-[A-Za-z]+:?)?\z` (`NAME=`, `--opt=`, chained `a=b=`, `OUT2=--o=`, attached `-X`, and colon-bound `-X:`, which the manager reports measured converted in Bash; M-6; diff-time CR-1). It is anchored with `\z`, not `$`, because `$` would also match before a trailing newline (diff-time CR-4). Every other occurrence is refused. A word that is a delegated body or an interpreter code body (D5) is exempt from D4. | R3, M-6 |
| D5 | Bodies in the `Bash` region.<br>(i) **Interpreter code bodies → `Unconverted`**, conservative wording (D7). Python family: verb resolved through `Get-VerbCandidates` (`python`, `python3`, `python3.x`, `py`, `pythonw`, and path forms such as `.venv/Scripts/python.exe`), with flag `-c`, including clusters ending in `c` such as `-Ic`. `node`: `-e`, `--eval`, `-p`, `--print`. The flag is recognised **only among interpreter options before the first non-option argument or `-m <module>`** (AR2-S3). Option values are tracked (G2-8 ruling): python `-W` and `-X` take a value, separate or attached; node `-r`, `--require`, `--import`, `--input-type`, `--loader` and `--experimental-loader` take a value, separate or with `=`. The first non-option argument is the first token that neither starts with `-` nor is the value of a listed option (refuse Case R21). Examples: `python -m pytest -c /d/x/pytest.ini` and `python tool.py -c /d/x` are allow Cases A22 and A23. Restored to keep AC1(b) literal; discriminating row Case R20. **Delegated reconciliation (AR2-S2):** for interpreter code bodies, AC1(b) takes precedence over AC2's converted-position allowance (fail-closed per Q3; conservative wording). So R20 `python -c "x=/d/y"` is refused although AC2 lists `NAME=` as converted.<br>(ii) Delegated bodies: `bash\|sh\|…-c` and `eval` bodies, and `$(...)` spans → re-scan as `Bash`. `powershell\|pwsh -Command\|-c` and `cmd /c\|/k` bodies → re-scan as `Unconverted`.<br>(iii) `$(...)` spans are found by the function's own quote-aware extraction, which mirrors `Invoke-CommandScan`'s existing loop without calling or editing it. Each span is removed from the outer word before D4 is applied. | R1, F4 ruling |
| D6 | Heredoc and here-string: in the `Bash` region, the body after an unquoted `<<` / `<<-` operator up to its terminator line, and the word after `<<<`, are stdin. They are scanned as `Unconverted`, on the raw text before `Split-Segments`. | R2 |
| D7 | Refusal message (rev. round 2; pure ASCII; AR2-S1, PR2-NEW-1/2/4/7). Sentences in order:<br>1. **Lead.** Non-conservative: `Refused: '<token>' is a POSIX drive path where nothing converts it.` Conservative: `Refused conservatively: '<token>' is a POSIX drive path inside a nested command body; MSYS may or may not convert it.`<br>2. **Resolved clause.** When `cwd` matches `^[A-Za-z]:[\\/]` it is **always** present (AC1 literal). Non-conservative: `From cwd <X:> a native Windows program resolves it to <X:\...>.` Conservative: `If MSYS does not convert it, from cwd <X:> a native Windows program resolves it to <X:\...>.` If the command contains a word-bounded, case-insensitive directory change (`cd`, `chdir`, `pushd`, `Set-Location`, `sl`, `Push-Location`), the clause is followed by ` A directory change in this command may alter this.` The directory-change flag is computed **once per command at the entry point**, so same-depth heredoc or interpreter scans cannot clobber it (diff-time CR-3 = UN-1). When `cwd` is missing or invalid, the clause is replaced by `cwd unavailable; no resolved path is claimed.` (must-address 5).<br>3. `This is a textual check; it does not know what the command would do.`<br>4. **Remedy.** `Write it drive-qualified (<L>:/... or <L>:\...); for prose, write the text to a file (for example with the Write tool) and pass it with -F / --body-file.` `<L>` is the token's own letter, upper-cased.<br>5. **Context hints (G2-4 ruling).** Every refusal inside a `node` body adds `If this is a JavaScript regex literal, use new RegExp(...) or a script file.` Every refusal inside a `cmd` body adds `If these are cmd switches, separate them with spaces.`<br>Non-ASCII characters in the echoed token are replaced by `?`. `<X:\...>` is the token with `/` replaced by `\`, after the cwd letter. AC1 is now met literally for a drive-letter `cwd`. With a missing or invalid `cwd` there is no drive to name, and must-address (5) governs (G2-9 ruling). The round-1 "withhold" interpretation (F3 ruling) is withdrawn.<br>**Conservative** means a drive token inside a body that MSYS may still convert when it is passed: (a) a `powershell\|pwsh -Command\|-c` or `cmd /c\|/k` body reached from the `Bash` region; (b) a `Bash`-region interpreter code body (D5(i)). Conservativeness is per body, not per token position (PR2-NEW-7, not adopted). The words "creates" and "would create" never appear. | R5, F2/F3 rulings, round-2 matrix |
| D8 | Accepted, pinned false positives (P4), each refused with the remedy:<br>- Bash `git commit -m "see /d/x"`<br>- PowerShell prose in `-m`, `--body` or a here-string<br>- PowerShell `rmdir /s/q tmp`<br>- Bash `cmd /c "dir /b/s"`<br>- Bash `cmd /c "xcopy /e/i/y a b"`<br>- Bash `node -e "s.replace(/a/g,'')"` (conservative)<br>- Bash unquoted `powershell -Command New-Item /d/x` (conservative)<br>- Bash heredoc prose `git commit -F - <<EOF` / `see /d/x` / `EOF` (P4h; AR2-N4)<br>The context hints are in D7, sentence 5. | R4, R6, AR2-N4, PR2-NEW-3 |
| D9 | The monitor is one self-contained file, `.claude/hooks/drive-root-monitor.ps1`, with modes `Snapshot`, `Compare`, `ListRoots` (print-only), `HookSessionStart` and `HookStop`. It parses `$args` (no typed `param()`); bad arguments → 11. | D7 (v1), R18 |
| D10 | Roots: explicit `-Root <list>`. Otherwise, on Windows, `[IO.DriveInfo]` fixed volumes as `X:\`, which includes `subst` drives (M-7). On non-Windows with no `-Root` → 11. There is no environment-variable override. Hook modes accept the same optional `-Root` / `-SnapshotDir`; tests always pass them and production registrations never do. | D8 (v1), R12, R18 |
| D11 | Enumeration: names only, non-recursive, `[IO.Directory]::EnumerateFileSystemEntries`. Hidden and system entries are included and reparse points are never followed. Comparison is ordinal-ignore-case on Windows and ordinal elsewhere. An enumeration error on a root → UNKNOWN for that root. | R10 |
| D12 | Standalone exit codes: `0` CLEAN, `10` NEW_CHILDREN, `11` UNKNOWN (also bad arguments and internal failure). The report is JSON on stdout: `status`, `new[]`, `unknown[]`, `faultShapedPresent[]` and `protected[]` (the built-in H4 paths, print-only). If any root is UNKNOWN, the status is UNKNOWN and `new[]` is still listed.<br>Each `unknown[]` entry is `{root, reason}`, with a fixed reason code: `snapshot-missing`, `snapshot-invalid`, `schema-mismatch`, `root-missing`, `root-unreadable`, `root-new`, `protected-path`, `root-parent-path`, `session-id-invalid`, `bad-arguments`, `internal`. This makes each M4/M6 node deterministic. Every M4/M6 must-fail node asserts its specific reason code, never just exit 11, so an internal failure cannot satisfy a specific-variant assertion (G2-1 ruling). | D9 (v1), R16 |
| D13 | Hook I/O. Recognised hook modes always exit 0. An unrecognised `-Mode` exits 11, which is non-blocking; this is the header wording, with no behaviour change (diff-time CR-6). `HookSessionStart` writes nothing to stdout in any path, including failures. `HookStop` stdout is empty or exactly one JSON object whose only key is `systemMessage`. A top-level catch turns any failure into exit 0: SessionStart stays silent, and Stop gives an UNKNOWN notice. `stop_hook_active` changes nothing. | R8, Q7 |
| D14 | Snapshot lifecycle: **one file per session, and that file is its own lock**. File: `<SnapshotDir or TEMP>\claude-drive-root-<session_id>.json`.<br>**Schema (AR2-N2):** `schemaVersion` (integer, `1`), `sessionId`, `createdUtc` (ISO 8601 `Z`; the "monitoring began at" time), `source` (`startup`\|`clear`\|`resume`\|`compact`\|`stop-baseline`), `roots` (object: root → array of child names), `announced` (object: key `<kind>\|<subject>` → UTC). Kinds are `child`, `fault`, `newroot`, `midsession` and `rootgone` (G2-2 ruling). Anything else, or a different `schemaVersion`, is invalid (`schema-mismatch`).<br> It is opened with an exclusive handle (`FileShare.None`) and written in place under that handle (truncate, write, flush). There is no temp file and no separate lock file, so AC6's single-file exception holds literally. `session_id` must match `^[A-Za-z0-9_-]{1,128}$`, otherwise UNKNOWN and no write.<br>**SessionStart** (`OpenOrCreate`): `startup`, `clear` and `resume` replace the contents in place. `compact` keeps a valid snapshot (no write) and replaces an invalid one. If the file cannot be opened because another instance holds it: silent no-op.<br>**Stop** (`Open`): invalid snapshot → UNKNOWN notice on every Stop; it is never overwritten at Stop. Cannot open because another instance holds it → silent exit 0. A missing file is created with `CreateNew` under the same exclusive handle as the mid-session baseline, announced once (R7; see the note under the manager rulings).<br>A crash mid-write leaves an invalid file, which the invalid-snapshot rules handle: replaced at SessionStart, UNKNOWN at Stop. Exception: a **zero-length** file held at Stop, left by a failed baseline write, takes the mid-session baseline branch and is not treated as invalid (diff-time CR-5; node H13-zero-length).<br>**Any mode**: if the snapshot path's parent is a monitored root, or the path lies under the built-in H4 paths or an additive `-ProtectedPath` → UNKNOWN, nothing written.<br>Old snapshots are never deleted.<br>**Open failures (TS3-N4):** only a sharing violation, meaning another handle holds the file, is the silent no-op / exit 0. Every other open failure (a missing or non-directory parent, access denied, a path error) goes to the top-level catch → UNKNOWN (`internal`), which is the path H4-forced-error and M-hookexit exercise. | R7, R16, PR-N3, F1 ruling, TS3-N4 |
| D15 | Dedupe: `HookStop` prints its notice first, then records each announced `<kind>\|<subject>` in `announced`, while still holding the exclusive handle. Every kind is announced once per snapshot lifetime, and `announced` is the **sole** gate (TS3-S3). For example, Stop emits the mid-session notice whenever the snapshot's `source` is `stop-baseline` and the `midsession` key is absent from `announced`, not only at file creation. Invalid-snapshot, invalid-id and internal-failure notices have no usable state, so they repeat on every Stop. Standalone `Compare` ignores `announced`. | R7, AR-N4, TS2-S2 |
| D16 | Newly discovered root: a root present now but absent from the snapshot → UNKNOWN for that root (`root-new`), announced once (`newroot`). A snapshot root that is now missing or unreadable → UNKNOWN (`root-missing` / `root-unreadable`), announced once (`rootgone`, G2-2 ruling). | D13 (v1), R9 |
| D17 | Fault shape: `faultShapedPresent[]` lists every existing single-letter direct child of a monitored root. It is a standing warning, announced once (`fault`), and it does not change the exit code. | D14 (v1), R9 |
| D18 | Notice texts (exact, ASCII, none claims a cause; PR2-NEW-2). `<UTC>` is the snapshot's `createdUtc`.<br>- New child: `New direct child(ren) of <root> since monitoring began at <UTC>: <paths>. Cause unknown; not necessarily created by this session.`<br>- Fault shape: `Single-letter child exists: <path>. It matches the MSYS fault shape; its origin is not known.`<br>- Newly discovered root: `<root> was not present when monitoring began at <UTC>; UNKNOWN.`<br>- Missing or unreadable root (PM wording): `<root> was present when monitoring began at <UTC> but is missing or unreadable now; UNKNOWN.`<br>- Invalid snapshot: `Drive-root monitoring: this session's snapshot is invalid or unreadable; UNKNOWN. No claim is made about drive roots.`<br>- Invalid session id: `Drive-root monitoring: the session id is not usable, so nothing was recorded; UNKNOWN. No claim is made about drive roots.`<br>- Internal failure: `Drive-root monitoring failed internally; UNKNOWN. No claim is made about drive roots.`<br>- Mid-session baseline: `Drive-root monitoring began mid-session at <UTC>; children created earlier in this session are not covered.`<br>H2, H4 and M9 pin these. | R9, R7, PR2-NEW-2 |
| D19 | Registration: the monitor hooks are registered at user level only, in the M-8 form (`SessionStart` → `HookSessionStart`, `Stop` → `HookStop`, `timeout` 30). The project `.claude/settings.json` is unchanged. The guard needs no new registration. It runs up to three times per call (project, user, charter); deny-wins makes that harmless. | D15 (v1), AR-N1, M-8 |
| D20 | Test placement:<br>- Guard cases go in `tests/test_guard_destructive_command.py` (guard-hook shards, Linux pwsh, no-skip proof).<br>- Monitor tests go in a new `tests/test_drive_root_monitor.py` (`pytest-core`). They are host-looped in the body, so the count is machine-independent. Each test evaluates **every** available host before asserting, and its failure message lists each host's result. That is how the AC7 gate reads "fails on each valid host" from one junit (F8 ruling; PM detail, flag G2-3). A missing host fails inside the test body, never at import.<br>- A single `run_monitor` helper always injects `-Root` and `-SnapshotDir`.<br>- Parametrize ids are plain labels (`A1`, `R3`).<br>No `ci.yml`, generator or CI-contract-test change. | D16 (v1), R18 |
| D21 | Q3a fixtures: `outcome()` gains `tool_name="Bash"`. A new `outcome_with_stderr()` returns the decision and stderr. Malformed-payload sites keep their shape. Further sites without `tool_name` are `tests/test_agent_workflow_contracts.py:295,561` and `tests/worktree_cleanup/guard-contract.ps1:39`; none carries a converted-position token, so none is edited. No expected decision changes. | D17 (v1), R17, AR-N2 |

**Owner must-address items**

*(1) Writes beneath an existing drive-root child are invisible to the delta monitor.* The monitor
compares direct root children only (AC4, D11). A fault path whose first segment already exists,
for example `D:\d` left by an earlier fault, adds nothing at root level, and no snapshot diff can
see it.
- D17 covers exactly one case: every existing single-letter root child, the `X:\<letter>` fault
  shape, is reported once per session as a standing warning ("origin is not known"). A session
  is therefore told when the one shape that makes the blind spot dangerous is present.
- D17 does **not** detect any write beneath such a child, nor beneath any non-fault-shaped
  existing child.
- The primary control for that route is the guard's refusal before execution (AC1). The
  remaining exposure is listed in the coverage limits. Today no single-letter child exists on
  `C:\` or `D:\` (input §1).

*(2) The standalone monitor is non-zero on hits or UNKNOWN; the hooks never block Stop.*
- The standalone `Snapshot`/`Compare`/`ListRoots` modes exit 10 on new children and 11 on UNKNOWN,
  bad arguments or internal failure (D12).
- Recognised hook modes always exit 0; an unrecognised `-Mode` exits 11 (non-blocking) (D13). `HookStop` reports only through a single `systemMessage`
  object (measured user-visible, M-1) and never emits `decision`.
- Every internal failure in hook mode is caught and turned into exit 0 plus an UNKNOWN notice. It
  never becomes exit 2, which would block stopping. H4 and the M-hookexit arm prove this.

*(3) Concurrent-session isolation and repeated Stop events.*
- Each session has its own snapshot file, keyed by a validated `session_id`. The file is its own
  exclusive lock (D14). Two sessions never read or write each other's state (H5).
- Concurrent instances of the same hook (M-9: they overlap, and unlocked writes are lost) are
  serialized by the exclusive handle. An instance that cannot open the file is a silent no-op at
  SessionStart and a silent exit 0 at Stop (H1c, H6). A crash mid-write leaves an invalid file,
  handled by the invalid-snapshot rules.
- Stop fires every turn. Each new child, fault-shaped child, newly discovered root and the
  mid-session baseline is announced once: the notice is printed first, then recorded in
  `announced` (D15). The once-only nodes are H3-once, H9-once, H11-newroot-once and H10-once, each
  proven by its M-dedupe arm.
- An invalid snapshot is announced every Stop on purpose: it is evidence, and it is never
  overwritten at Stop.
- `resume` re-snapshots, because the session id persists (M-9).
- Children created by other sessions, the owner or the OS appear in every open session. The
  wording says the cause is unknown (D18; coverage limits).

*(4) A newly discovered drive without a snapshot is UNKNOWN.* A root present at compare but absent
from the snapshot, for example a drive mounted mid-session (including `subst`, M-7), is reported as
UNKNOWN for that root, once per session in hook mode. In standalone `Compare` it gives exit 11
(D16, reason `root-new`). It is never treated as CLEAN and never reported as "new children".
Tested in M4-newroot (standalone) and H11-newroot-once (hook), and proven by the M-newdrive and
M-dedupe-newroot arms.

*(5) A missing or invalid `cwd` never yields a guessed resolved-path claim.* The resolved-path
clause is a pure string computation with no filesystem call (D7, rev. round 2).
- When `cwd` matches `^[A-Za-z]:[\\/]`, the clause is **always** present (AC1 literal):
  - non-conservative: `From cwd <X:> a native Windows program resolves it to <X:\...>.`
  - conservative: `If MSYS does not convert it, from cwd <X:> a native Windows program resolves it
    to <X:\...>.`
- If the command contains a word-bounded, case-insensitive directory change (`cd`, `chdir`,
  `pushd`, `Set-Location`, `sl`, `Push-Location`), the clause is followed by
  ` A directory change in this command may alter this.`
- A missing, empty, UNC or garbage `cwd` still refuses, and the clause is replaced by
  `cwd unavailable; no resolved path is claimed.` (P1b-nocwd / -emptycwd / -unc / -garbage).

So no case states a guessed path as fact. The round-1 "withhold" interpretation is withdrawn. The
G-message arms prove that P1a and P1b discriminate.

**Scope**
- **In**:
  - D1–D8 in the guard, plus its header "Drive-token rule" paragraph.
  - The D9–D18 monitor and its header (modes, exit codes, registration snippet, TEMP
    accumulation note).
  - Tests per the mapping below; the regenerated inventory.
  - The corpus pass (R4).
  - The AC7 arms.
  - The `reviews/` copies (manager).
  - `CLOSEOUT.md`; this document.
  - User-level installation and registration (D19).
  - Operational acceptance.
  - Two PRs.
- **Out**:
  - Everything Section 0 lists as out of scope (except the superseded installation bullet).
  - `ci.yml`, `scripts/**`, the project `.claude/settings.json`, `docs/MASTER_HANDOVER.md`,
    `WORKSTREAM_OWNERSHIP*`, and any general approval policy.
  - Refusing Write/Edit/MCP parameters; the `\d\x` and `/tmp/x` forms.
  - Any change to the shared checkout `D:\development\Hypertrophy-Toolbox-v3-main`.
  - Deleting snapshots.

**Artifacts**
| Path | Change | PR | Notes |
|---|---|---|---|
| `.claude/hooks/guard-destructive-command.ps1` | modify | PR-1 | D1–D8; pure ASCII + UTF-8 BOM; exit 2 is the only block. |
| `.claude/hooks/drive-root-monitor.ps1` | new | PR-1 | D9–D18; pure ASCII + UTF-8 BOM. |
| `tests/test_guard_destructive_command.py` | modify | PR-1 | D21; case table; P-rows. |
| `tests/test_drive_root_monitor.py` | new | PR-1 | M-, H- rows. |
| `docs/test_inventory/TEST_INVENTORY.md`, `.json` | regenerate | PR-1 | Generator only. |
| `docs/msys_destination_validation/PLANNING.md` | modify | PR-1, PR-2 | Plan, evidence. |
| `docs/msys_destination_validation/reviews/round1-*.md`, `round2-*.md` (three each; + round 3) | new | PR-1 | Byte-for-byte copies by the manager, SHA-256 recorded under Reviewer findings. |
| `docs/msys_destination_validation/CLOSEOUT.md` | new / modify | PR-1 (implementation level), PR-2 (merge, installation, operational) | The four AC10 levels with evidence paths. |
| `artifacts/msys-ac7-<UTC>/`, `artifacts/msys-corpus-<UTC>/` (gitignored) | new | — | Arm evidence; corpus hits. |
| `C:\ht\MSYS-INSTALL\backup-<UTC>\`, `staged-<UTC>\`, `ROLLBACK.ps1` | new, outside repo | — | Backups, staged blobs, rollback. |
| `C:\Users\aviha\.claude\hooks\guard-destructive-command.ps1`, `drive-root-monitor.ps1`, `C:\Users\aviha\.claude\settings.json` | install | — | Per R11. |

**Effort**: L · **Owner**: main session (manager, under the 2026-10-28 delegation) · **Depends on**: round-3 delta review (test-strategist) + delegated Gate 1.

**Sequence**
0. **Gate 1.** Round-3 delta review of Plan v2 rev. round 2 by test-strategist, then delegated
   Gate 1 acceptance recorded as such. The manager copies `reviews/` byte-for-byte.
1. **Base.** Re-fetch `origin/main`, record the full SHA, and rebase the still-empty branch if it
   moved (AC8). Record the H4 creation times (S0-d). S0-a/b/c are resolved by M-6/M-7/M-8.
2. **Guard tests first.** D21 fixtures, case-table rows (Plan v1 + v2 additions) and P1–P8. Run
   them on base + tests: every refuse row and P1a/P1b/P3-refuse/P4/P6a/P8 must fail, and every allow
   row must pass. This run also proves that P6a's exact `eval`/`$()` string is allowed by the base
   guard and not caught by the existing nesting deny (TS3-N3). Retain this run.
3. **Guard rule.** Implement D1–D8. Run the new cases, then the full guard file under `powershell`
   and `pwsh`. Record the measured case count (R18).
4. **Monitor.** Write the tests, show them red against a stub, then implement D9–D18.
5. **Gates.** Inventory regeneration + `--check`, pyright baseline diff, Lint, targeted pytest on
   both hosts, the H4 post-run check.
6. **Corpus pass (R4).** Run the implemented token rule read-only over the Bash/PowerShell
   `tool_use` commands in `C:\Users\aviha\.claude\projects\**\*.jsonl`; nothing is executed.
   Record the hit count, each hit's classification and the FP rate. Hits go under
   `artifacts/msys-corpus-<UTC>/`, and `CLOSEOUT.md` carries counts only (F9). **Blocking rule
   (AR2-N5, PR2-NEW-3):** any false-positive class seen more than once in the corpus and not
   already pinned in D8 blocks PR-1, until the rule is adjusted or the manager records acceptance
   naming the class.
7. **AC7 arms** (table below), on the exact candidate commit.
8. **Diff-time review**: `code-reviewer`. Record its result; a review that did not run is
   incomplete.
9. **PR-1** (code, tests, inventory, PLANNING, `reviews/`, `CLOSEOUT.md` implementation level).
   Required checks green. Merge without `--delete-branch` and record the merge SHA → *merge*
   level.
10. **Installation** (below) → *installation* level.
11. **Operational acceptance** (below) → *operational* level.
12. **PR-2** (docs-only: `CLOSEOUT.md` merge/installation/operational evidence + PLANNING).
    Merge it. Never declare `PREVENTION_COMPLETE`.

**Expected gates**
- AI workflow / agent config (`.claude/**`): source behaviour changes, so tests run.
  `code-reviewer` is required.
- Tooling / scripts: not triggered.
- PR-2 is product docs only: no gates.
- pytest:
  - `tests/test_guard_destructive_command.py`: full, both hosts locally; four Linux pwsh shards
    in CI.
  - `tests/test_drive_root_monitor.py`.
  - `tests/test_agent_workflow_contracts.py::test_all_effective_destructive_registrations_execute_deny_allow`.
  - `tests/test_ci_expansion_contracts.py`, `tests/test_worktree_ci_contracts.py`.
- Test Inventory Drift: regenerate for the new file; `--check` exits 0.
- Type Check: no net-new pyright diagnostics (`pythonPlatform: Windows`; R18 idioms).
- Lint: applies.
- Guard-hook CI fan-in: the new guard cases land in the existing shards. `verify` and `union`
  cover them, and the measured leg times are recorded against the 20-minute budget.
- **Accepted gaps** (R20):
  - The monitor's Windows PowerShell 5.1 behaviour is verified locally only.
  - H8 does not run in CI.
  - `workflow-contracts-windows` does not exercise the monitor.
- e2e: none.

**Case table additions** (normative under Plan v2; every row is a test; Plan v1/Section 0 rows
A1–A13, R1–R14, L1–L5 and M1–M5 stand)

| # | Tool | Input | Decision | Source |
|---|---|---|---|---|
| A14 | Bash | `bash -c "gh run download 1 -D /d/x"` | allow (inner bash converts) | R1 |
| A15 | Bash | `.venv/Scripts/python.exe -c "open(r'D:/x')"` | allow | R1 |
| A16 | Bash | `find . -path "*/d/*"` | allow | R4 |
| A17 | Bash | `rg -g '!**/c/**' pattern` | allow | R4 |
| A18 | PS | `Get-Item %USERPROFILE%/a/b` | allow | R4 |
| A19 | Bash | `cat ${HOME}/c/x` | allow | R4 |
| A20 | PS | `Get-Item (Get-Location)/d/x` | allow | R4 |
| A21 | either | `cat ~/d/x` | allow | R4 |
| A22 | Bash | `python -m pytest -c /d/x/pytest.ini` | allow (`-c` belongs to pytest; the token leads its word and is converted) | AR2-S3 |
| A23 | Bash | `python tool.py -c /d/x` | allow (`-c` follows the first non-option argument; the token is converted) | AR2-S3, PR2-NEW-7 |
| A24 | PS | `Set-Content -Path:D:/x -Value hi` | allow (drive-qualified) | diff-time CR-1 |
| A25 | Bash | `tool -Path:/d/x` | allow (manager reports measured converted to `-Path:D:/x`) | diff-time CR-1 |
| A26 | Bash | `tool /d//x` | allow (manager reports measured converted to `D:/x`) | diff-time CR-2 |
| R15 | Bash | `cmd /c "python x.py /d/x"` | refuse | R1 |
| R16 | Bash | `eval 'tool "-D /d/x"'` | refuse | R1, F6 ruling (replaces the backslash-escaped form) |
| R17 | Bash | `.venv/Scripts/python.exe -I -c "import os; os.makedirs('/d/x')"` | refuse (conservative) | R1, F4 ruling |
| R18 | Bash | `cat <<'EOF' > f.txt` / `/d/x` / `EOF` (three lines) | refuse | R2 |
| R19 | Bash | `python - <<<"import os; os.makedirs('/d/x')"` | refuse (regression row; F7 ruling) | R2 |
| R20 | Bash | `python -c "x=/d/y"` | refuse (conservative). D4 alone would allow it, so this row discriminates D5(i). | F4 ruling |
| R21 | Bash | `python -W ignore -c "x=/d/y"` | refuse (conservative; `ignore` is the value of `-W`, not the first non-option argument) | G2-8 ruling |
| R22 | Bash | `node --require x -e "x=/d/y"` | refuse (conservative; `x` is the value of `--require`) | TS3-N2 |
| R23 | PS | `Set-Content -Path:/d/x -Value hi` | refuse (colon-bound parameter; it was a fail-open) | diff-time CR-1 |
| R24 | PS | `Set-Content /d//x hi` | refuse (doubled slash; the manager reports `GetFullPath` measured → `D:\d\x`; it was a fail-open) | diff-time CR-2 |
| R12 variants | — | `tool_name` absent, `null`, `5`, `"bash"`, `"Bash "`, `"Foo"`, with a leading-word `/d/x` | refuse | R20 |

**P-rows**
- *(rev. round 2; TS2-B3 split; one node per variant.)* Every P1 node asserts the exact D7 text for
  its case, the remedy with the token's own letter, pure ASCII, and the absence of "create".
- **P1a — plain resolved clause expected** (non-conservative, valid `cwd`, no directory change):
  - P1a-cwdD: `cwd` `D:\…` → `From cwd D: … D:\d\…`.
  - P1a-cwdC: `cwd` `C:\…` → `C:\d\…`.
  - P1a-nonascii: a token containing U+00E9 → echoed with `?`, asserted on raw stderr bytes: no
    byte is above 127 (TS3-S4).
  - P1a-cdword: an identifier containing `cd`/`sl` (e.g. `abcd`, `isl`) → no hedge sentence.
- **P1b — clause hedged or absent:**
  - Absent (`cwd unavailable; no resolved path is claimed.`): P1b-nocwd, P1b-emptycwd, P1b-unc,
    P1b-garbage.
  - Hedge sentence appended: P1b-cd (`cd C:\ && …`) and P1b-setlocation (`Set-Location …; …`).
  - P1b-conservative-ps: a Bash-reached `powershell -Command` body → the `Refused conservatively`
    lead + the `If MSYS does not convert it` clause.
  - P1b-conservative-interp: a Bash `python -c` body → the same.
  - Only P1b nodes assert the conservative sentence (TS2-B2).
  - P1b-cd-heredoc and P1b-cd-interp (diff-time CR-3): a directory change in the command plus a
    same-depth heredoc or interpreter body → the hedge sentence is still present. These are
    `restored`-only regression nodes and are not arm-gated.
- P2 profiles × modes: one node per pair, `P2-<profile>-<mode>` (`agent`/`main` ×
  `default`/`auto`/`bypassPermissions`/`plan`), each asserting the drive-token deny. Plus P2-mask:
  an ask elsewhere in the command cannot mask it (TS3-N1).
- P3-allow (one node per form): P3-allow-x `tool x=/d/y`, P3-allow-ab `tool a=b=/d/y`,
  P3-allow-out2 `OUT2=--o=/c/y tool`, P3-allow-redirect `tool > /d/x`. P3-refuse: `tool >/d/x`.
  P3-refuse-newline: Bash `tool "a=<newline>/d/x"` → refuse; the prefix ends in a newline, which
  `$` would accept and `\z` does not (diff-time CR-4).
- P4 accepted false positives (D8), each with tool and region named: P4a Bash commit prose; P4b
  PowerShell `-m` / `--body` / here-string prose; P4c PowerShell `rmdir /s/q tmp` (default mode;
  asserts the drive-token reason, since the existing rule alone would only ask); P4d
  `cmd /c "dir /b/s"`; P4e `cmd /c "xcopy /e/i/y a b"`; P4f `node -e "s.replace(/a/g,'')"`
  (conservative; asserts the regex hint); P4g unquoted `powershell -Command New-Item /d/x`
  (conservative); P4h Bash `git commit -F - <<EOF` / `see /d/x` / `EOF` (heredoc prose; asserts
  the Write-tool remedy).
- P5-sentinel: the line-932 pattern with a Case-R command. It is documented as non-discriminating;
  its deny assertion is the real check (R17).
- P6a: the innermost command is pinned to a D4-position row, R9-style `tool "-D /d/x"`, nested 4
  levels through **`eval` / `$()` chains** (not quote nesting, which `Split-Segments` cannot model;
  TS3-N3). It is denied with the drive-token reason, and it is in G-offset's must-fail set. The
  exact string is proven on the base guard in the step-2 red run: allowed there, and not caught by
  the existing nesting deny. P6b: 5 levels → the existing nesting reason (a pin).
- P7 stderr discipline (R17), as node ids (TS3-N1):
  - P7-deny-prefix: every drive-token deny carries **either** fixed prefix, `Refused: '` or
    `Refused conservatively: '`. Case R-rows likewise accept either prefix (TS2-B2).
  - P7-allow-clean: every A/L row's stderr has neither "failing closed" nor either prefix.
  - P7 is not applied to P6b (F10 ruling).
- P8 forced exception (PR-N2): a `tmp_path` copy of the guard with `throw` injected at the start
  of `Invoke-DriveTokenScan` → exit 2 with "failing closed".

**Test mapping**

| AC / rows | Tests |
|---|---|
| AC1 | Case R1–R24, R12 variants, P1a, P1b, P3-refuse, P4a–h, P6a, P7, P8 — `test_drive_token_case_table[<id>]` × host, `test_drive_token_*` |
| AC2 | Case A1–A26, P3-allow, P7 (interpreter code bodies excepted under the AR2-S2 reconciliation, D5(i)) |
| AC3 | the full pre-existing guard file on the candidate; `test_hook_source_is_ascii_with_bom[*]` and `test_hook_source_parses[*]` (now including the monitor); the internal-error cases; the registration probe; P2, P6b. The reviewer checks that no pre-existing expected value was edited. |
| L1–L4 | pinned as allow; L5 by M-2 measurement only |
| AC4 | M1, H2, H7 |
| AC5 | M2 (exit code only), M4-missing-root, M4-unreadable-root, M4-missing-snapshot, M4-invalid-snapshot, M4-wrong-schema, M4-newroot (each asserts exit 11 and its D12 reason code), H4-*, H10-* |
| AC6 | M5 (entries + `CreationTime`/`LastWriteTime` unchanged; only the snapshot file written, with no temp or lock file (F1 ruling)), M6 (`protected[]` lists the H4 paths; `-ProtectedPath` under `tmp_path` and root-parent snapshot → UNKNOWN, nothing written), S0-d H4 creation-time record |
| AC7 | arm table below |
| AC8 | the base SHA record (step 1) |
| AC9 | inventory `--check`, pyright diff, Lint, CI links, measured shard times |
| AC10 | `CLOSEOUT.md`: merge SHA, installation hash table and probe output, operational transcripts |
| Must-address (1)–(5) | (1) H9-*; (2) H4-*, M7, D12 exit tests; (3) H1-*, H1c (smoke), H3-*, H5, H6, H9-once, H10-once, H11-newroot-once; (4) M4-newroot, H11-newroot-once; (5) P1b-nocwd/-emptycwd/-unc/-garbage |

Monitor nodes *(rev. round 2; one deterministic, single-purpose node each; all through
`run_monitor`; host loop in body, evaluating every host before asserting)*. Every hook-mode node
also asserts the stdout discipline of D13.

Test-id constraints (TS2-B2):
- Single-session nodes use ids of **at most 8 characters**, so the M-sessionfile mutation (key on
  the first 8 characters) leaves their file names unchanged (G2-5 ruling).
- H5's two ids are longer than 8 characters and share their first 8.
- `-SnapshotDir` is always `tmp_path/snap`, so a traversal id that climbs one level stays inside
  `tmp_path`.
- AC7 arms select **exact node ids**, passed as full pytest node ids (for example through an
  argfile), never `-k` substrings: `-k A1` would also match `A10`–`A19`.
- AC7 arm runs and local runs use `--basetemp=C:\ht\T`, so the longest snapshot path (the
  129-character id) stays under 260 characters.
- Under the M-sessionid arm, a MAX_PATH exception would be caught as UNKNOWN. H4-badid-129
  therefore asserts that no file was created in `-SnapshotDir`, not only the exit code, so the arm
  cannot pass falsely (G2-5 ruling).

SessionStart:
- H1-startup, H1-clear, H1-resume: the contents are replaced in place. A child created between two
  calls *is* in the new snapshot, and no other file appears in `-SnapshotDir`.
- H1-compact-keep: a valid snapshot is kept, so a child created between two calls is *not* in it.
- H1-compact-invalid: an invalid snapshot is replaced.
- H1-held: a new child is created first, so an unlocked SessionStart would rewrite the snapshot
  with different content (TS3-S1). The test then holds the snapshot (Windows: a plain handle;
  POSIX: `fcntl.flock`) → silent no-op, file unchanged.
- H1c (smoke; in no must-fail set): N concurrent `Popen` `HookSessionStart` → one valid snapshot,
  all exit 0, empty stdout.

Stop:
- H2: a new child → exit 0, exactly one `{systemMessage}`, the D18 new-child text.
- H3-once: a repeated Stop → no repeat.
- H3-second: a later second child → announced.
- H4 (one node per variant):
  - H4-malformed;
  - H4-badid-chars (`*`) and H4-badid-129 (129 characters, a valid file name);
  - H4-traversal (`x\..\..\y`-style, climbing at most one level above `-SnapshotDir`);
  - H4-invalid-snapshot: UNKNOWN on every Stop;
  - H4-forced-error: `-SnapshotDir` is a regular file.

  Each → exit 0 + its exact D18 text, never 2. The id variants also assert that nothing is
  written anywhere under `tmp_path`.
- H5 (TS3-S2): start session A, create a child, start session B, run Stop for A. A must report
  the child. Under M-sessionfile, B's SessionStart overwrites the shared file and A reports
  nothing. The ids are longer than 8 characters and share their first 8.
- H6: a new child is created first, so an unlocked Stop would print a notice and update
  `announced` (TS3-S1). The test then holds the snapshot → exit 0, no output, file unchanged.
- H7: standalone `Compare` after an announce → 10.
- H9-notice: a pre-existing single-letter child → the D18 fault text, exit 0.
- H9-once: no repeat.
- H9-standalone: standalone JSON `faultShapedPresent` lists it; the exit code is unchanged.
- H10-baseline: Stop with no snapshot → a `stop-baseline` snapshot is created, plus the
  mid-session text.
- H10-once: the mid-session text is not repeated.
- H10-later-child: a later new child is reported.
- H11-newroot-once: in hook mode, a root added after the snapshot → the newly-discovered-root text
  once, not repeated. This is the "not repeated" node for the new-drive kind. M4 is standalone, and
  standalone ignores `announced` (G2-2 ruling).
- H12-rootgone-once: in hook mode, a snapshot root removed after the snapshot → the
  missing-or-unreadable-root text once, not repeated (G2-2 ruling).
- H13-zero-length (diff-time CR-5): a zero-length snapshot held at Stop → the mid-session
  baseline branch, with the mid-session text and a valid `stop-baseline` snapshot written. It is
  not the invalid-snapshot UNKNOWN.

Standalone and static:
- M1: new child with a red standing-audit fixture → 10, names the path.
- M2: no new child → exit 0. It asserts the exit code only.
- M3: a removed child is not new.
- M4 (exit 11 + reason code each): M4-missing-root (`root-missing`), M4-unreadable-root
  (`root-unreadable`; `icacls /deny` on Windows, removed in `finally` (TS2-S3); `chmod 000` on
  POSIX, skipped only when euid is 0), M4-missing-snapshot, M4-invalid-snapshot, M4-wrong-schema,
  M4-newroot (`root-new`).
- M5: runs `Compare` against a valid snapshot (TS3-S5), so the M-write patch is reached. Root
  entries and `CreationTime`/`LastWriteTime` are unchanged; only the snapshot file is
  written.
- M6-protected and M6-root-parent: under `tmp_path` only → `protected-path` / `root-parent-path`,
  nothing written.
- M6-list: `protected[]` lists the built-in H4 paths (print-only).
- M7: bad arguments → 11 (`bad-arguments`).
- M8-helper: no test invokes the script except via `run_monitor`.
- M8-static: the non-comment tokens never reference `audit-worktrees` or the baseline.
- M9-path: reported path = root as given + child name.
- M9-case: case sensitivity per host.
- M9-texts: every D18 text, exact.
- H8: `ListRoots` shape on Windows. H8b: non-Windows with no `-Root` → 11.

**AC7 arm table** *(rev. round 2: must-fail gating model; TS2-B1/B2/B3/S1/S2/S4, AR2-N3)*
- **Where**: `git archive <candidate SHA>`, extracted under `C:\ht\MSYS-AC7\<arm>\`. Run with the
  clone's `.venv` Python, archive root as cwd and on `PYTHONPATH`.
- **Patches**: each arm is a retained `git apply` patch on the disposable copy, hashed.
- **Selection** (TS2-S4): each arm's exact-id selection covers its must-fail set, and the arm also runs the full
  drive-token selection (guard arms) or the full monitor file (monitor arms). The outcomes outside
  the must-fail set are recorded in the evidence but not gated.
- **Hosts**:
  - The plan proposed one guard junit per host. The actual accepted format is **one junit per
    arm**, with host-specific guard node IDs; every designated host identity is checked
    individually against its required failure.
  - Monitor arms produce one junit per arm covering both hosts inside each test body. Each
    failure message lists every host's result (F8 ruling, D20), and the independent message audit
    verifies failure on both hosts for every designated monitor node.
  - The manager accepted this evidence-format reconciliation under the owner's delegation on
    2026-10-28. The per-host failure criterion is unchanged; no new reviewer pass is claimed.
  - `restored` runs everything. The full guard file runs once on `restored` under both hosts.
- **Merge gate**: every must-fail node fails under its arm, on each host where the arm is valid,
  **and** every test in the TS3-N5 scope (below the table) passes on `restored`. There is no gated
  expected-pass column.
- **Must-fail sets**: built only from deterministic, single-purpose nodes. M-lock is valid on the
  Windows hosts only, because of Linux `flock` semantics (AR2-N3).

| Arm | Mutation | Must-fail set |
|---|---|---|
| G-noop | `Invoke-DriveTokenScan` body → `return` | every Case R-row (R1–R24; R23, R24 added at diff time) and each R12 variant; P1a-*; P1b-*; P2-<profile>-<mode>, P2-mask; P3-refuse; P4a–h; P5-sentinel; P6a; P7-deny-prefix |
| G-region-unconv | D2 always returns `Unconverted` | A4, A5, A6, A7 (TS3-S6) |
| G-prefix | D4 prefix allowance removed (offset 0 only) | A5, A7, P3-allow-x, P3-allow-ab, P3-allow-out2 (TS3-S6; P3-allow-redirect is an offset-0 word and cannot fail here) |
| G-exempt-delegated | D4 exemption for delegated bodies removed (the outer word is decided by D4) | A14 (TS3-S6) |
| G-optvalue | the value of a value-taking interpreter option counts as the first non-option argument; tokens starting with `-` remain options | R21, R22 (G3-1, TS3-N2) |
| G-nonoption-anywhere | the code flag is recognised anywhere among the arguments | A22, A23 (TS3-S6) |
| G-boundary | boundary lookbehind removed (token matches anywhere) | A10a–d, A11, A16–A21 |
| G-region | D2 always returns `Bash` | R1, R2, R11, R13, R14, each R12 variant |
| G-offset | D4 treats every Bash occurrence as converted | R8, R9, R16, P3-refuse, P3-refuse-newline (diff-time), P4a, P6a |
| G-interp | **both** the D5(i) scan **and** D4's interpreter-body exemption disabled (bodies are decided by D4) | R20 |
| G-heredoc | D6 off | R18, P4h (G2-6 ruling) |
| G-message-always | the plain non-conservative resolved clause is always emitted, using `D` for invalid/missing `cwd` and suppressing the directory-change hedge | P1b-cd, P1b-conservative-interp, P1b-conservative-ps, P1b-emptycwd, P1b-garbage, P1b-nocwd, P1b-setlocation, P1b-unc, each on powershell and pwsh: all 16 failed at `68d52ba7`. P1b-cd-heredoc and P1b-cd-interp remain `restored`-only requirements. |
| G-message-never | the clause is never emitted | P1a-* |
| G-sanitize | no `?` replacement of non-ASCII characters in the echoed token | P1a-nonascii: U+00E9, raw stderr bytes, no byte above 127 (G2-7 ruling, TS3-S4) |
| G-cdsubstring | directory change matched as a substring instead of a whole word | P1a-cdword (G2-7 ruling) |
| M-new | the new-children diff returns empty | M1, H2, H3-second, H7, H10-later-child, M9-path |
| M-diff-all | every current child is reported as new | M2, M3 (TS3-S6; M3 asserts `new[]` is empty) |
| M-unknown | UNKNOWN classification removed for snapshot and root states (not `root-new`, not M6) | M4-missing-root, M4-unreadable-root, M4-missing-snapshot, M4-invalid-snapshot, M4-wrong-schema |
| M-newdrive | D16 newly-discovered-root detection off | M4-newroot |
| M-fault | D17 off | H9-notice, H9-standalone |
| M-write | a write into the first root, placed **after** enumeration in `Compare` | M5 |
| M-compact | `compact` replaces a valid snapshot | H1-compact-keep |
| M-dedupe-child | `child` entries in `announced` ignored | H3-once |
| M-dedupe-fault | `fault` entries ignored | H9-once |
| M-dedupe-newroot | `newroot` entries ignored | H11-newroot-once |
| M-dedupe-midsession | `midsession` entries ignored | H10-once |
| M-dedupe-rootgone | `rootgone` entries ignored | H12-rootgone-once (G2-2 ruling) |
| M-sessionfile | the file name keyed on the first 8 characters of the id | H5 |
| M-lock (Windows hosts only) | the handle opened `FileShare.ReadWrite` instead of `None` | H6, H1-held |
| M-sessionid | `session_id` regex removed | H4-badid-129, H4-traversal |
| M-hookexit | catch → `exit 2` | H4-forced-error |
| M-midsession | a missing snapshot is not baselined at Stop | H10-baseline, H13-zero-length (diff-time) |
| M-protected | protected-path refusal disabled (`-ProtectedPath` under `tmp_path`) | M6-protected |
| M-root-parent | root-parent refusal disabled (root-parent path under `tmp_path`) | M6-root-parent |
| restored | none | — (every test in scope must pass) |

P1b-cd-heredoc and P1b-cd-interp are `restored`-only regression nodes in no must-fail set
(diff-time ruling).

H1c is a smoke test and appears in no must-fail set (TS2-B1). Under the round-1 ruling, L1–L4 are
pins that no single-control arm fails.

G-sanitize and G-cdsubstring were added to the gate by the G2-7 ruling. G-optvalue (G3-1,
reworded per TS3) isolates the G2-8 option-value tracking.

**Scope of "every test passes on `restored`" (TS3-N5):**
- `tests/test_guard_destructive_command.py`
- `tests/test_drive_root_monitor.py`
- `tests/test_agent_workflow_contracts.py::test_all_effective_destructive_registrations_execute_deny_allow`

The full suite carries a recorded pre-existing red and is outside the AC7 gate. Its required CI
checks are judged separately at merge.

Retained under `artifacts/msys-ac7-<UTC>/`:
- the candidate SHA;
- each patch, and the SHA-256 of each patched file;
- command lines and exit codes;
- junit per host (guard) and per run (monitor);
- per test id, a must-fail-versus-observed table plus the recorded non-gated outcomes.

**Installation** (R11; performed by the manager under the owner's delegation, R13)
1. Back up byte-for-byte with SHA-256 to `C:\ht\MSYS-INSTALL\backup-<UTC>\`: the user-level
   `settings.json` and `hooks\guard-destructive-command.ps1`, plus a read-only hash record of the
   shared checkout's `.claude\settings.json` and guard (not modified).
2. Write `C:\ht\MSYS-INSTALL\ROLLBACK.ps1` before any change. It must contain only drive-qualified
   paths and no drive token, use the same `.new` + hash + `Move-Item -Force` sequence, and be
   runnable from the owner's own terminal.
3. Stage the merged blobs by OID with `git cat-file blob` (bytes) into `staged-<UTC>\`. Verify
   their SHA-256 against the blob, and parse each under `powershell` and `pwsh`.
4. Probe the **staged** guard:
   - the registration probe (`MSYS2_ARG_CONV_EXCL=0 echo inert` → 2, `git status --short` → 0,
     `git push origin HEAD` → 0 under `main`);
   - synthetic payloads: Bash and PowerShell × with/without `cwd` × a benign command → 0, and a
     Case-R row → 2.
5. Monitor first, unregistered: write `hooks\drive-root-monitor.ps1.new`, verify the hash,
   `Move-Item -Force`. Run `ListRoots` and a `Snapshot`/`Compare` against a disposable `-Root` /
   `-SnapshotDir` from the installed path.
6. Guard: write `.new`, verify the hash, `Move-Item -Force`. Re-run the step-4 probe against the
   installed path immediately.
7. `settings.json` last, `hooks` object only *(rev. round 2, PR2-NEW-5)*.
   - Add `SessionStart` and `Stop` in the M-8 form
     (`powershell -NoProfile -ExecutionPolicy Bypass -File "C:/Users/aviha/.claude/hooks/drive-root-monitor.ps1" -Mode HookSessionStart`
     / `-Mode HookStop`, `timeout` 30).
   - Edit as a **textual, byte-preserving insertion** into `.new`: BOM and line endings preserved,
     and no `ConvertTo-Json` reserialization.
   - Verify that the byte diff against the original is a pure insertion, and that every
     pre-existing entry is byte-identical, including any existing `SessionStart`/`Stop` entries.
   - Parse `.new` as JSON as a check only.
   - Immediately before `Move-Item -Force`, re-hash the original and **abort** if it changed since
     the backup, because another session may have rewritten it.
8. Record the per-copy hash table: user guard, user monitor, clone guard, and the shared-checkout
   guard ("locally modified, not updated; user-level copy enforces").

**Operational acceptance** *(rev. round 2; R12, R13, AR2-S5, PR2-NEW-6)*. A fresh headless session
on the VS Code extension's **bundled `claude.exe` 2.1.310** (`resources\native-binary\claude.exe`,
M-10), which is the primary run, with disposable cwd `C:\ht\MSYS-OPS\cwd`. Charter-frontmatter
payloads remain an inference (M-11).
- **Guard**: the session runs Case R3 `[IO.Path]::GetFullPath('/c/Users/x')` through the PowerShell
  tool. Pass = the refusal matches D7 exactly, including `From cwd C: a native Windows program
  resolves it to C:\c\Users\x.`
- **Monitor**:
  1. Prove a drive letter unused (`[IO.DriveInfo]` list). Immediately before the session, map
     `subst <L>: C:\ht\MSYS-OPS\qroot`. Confirm that SessionStart created the session's snapshot
     before the first tool call.
  2. Mid-session, create `<L>:\probe-child` (drive-qualified). The next Stop must show the D18
     NEW notice naming it.
  3. Overwrite the session's own snapshot with invalid JSON. The next Stop must show UNKNOWN.
  4. End the session. Immediately remove the child and `subst <L>: /D`.
- **Record**: the Stop-hook latency; that other open sessions may show one UNKNOWN notice
  (new-drive / missing-root).
- **Label the level exactly**: "fresh headless session on the VS Code extension's bundled
  claude.exe 2.1.310; payload fields and Stop notice measured on the bundled 2.1.310 binary
  (headless) and CLI 2.1.302; panel rendering unmeasured (open); detection exercised on a
  substitute (subst) root; guard shown on one harmless row; charter-frontmatter payloads
  inferred".

**Plan v2 coverage limits** (additions to Section 0's list, R9 / R13 / F6; rev. round 2)
- Children created by concurrent sessions, the owner or the OS appear in every open session as
  "cause unknown".
- A drive mounted mid-session is UNKNOWN once per open session.
- If a client omits or renames `tool_name`, strict Q3a refuses every drive-token command. The
  payload fields and the Stop notice were measured on the VS Code extension's bundled `claude.exe`
  2.1.310 (headless) and CLI 2.1.302, and a subagent payload on 2.1.310 (M-10, M-11).
  Panel rendering is unmeasured, and charter-frontmatter payloads are inferred.
- For interpreter code bodies, AC1(b) takes precedence over AC2 (AR2-S2). A converted
  `NAME=/d/...` inside a `python -c` body is refused conservatively.
- Conservativeness is per body, not per token position (PR2-NEW-7): a token that nothing would
  convert inside a `python -c` body still gets the conditional wording.
- Residual of the G2-8 option-value tracking: an unlisted value-taking interpreter option can
  make its value look like the script name. The code body then falls to D4. Non-leading tokens are
  still refused, but leading and `NAME=` forms would pass.
- Writes beneath an existing child are not detected (must-address 1; D17 flags only the
  single-letter shape).
- The guard's tokenizer does not model backslash-escaped quotes inside double quotes, so some
  nested forms tokenize differently from bash. For example, `eval "tool \"-D /d/x\""` is allowed
  where bash would leave `/d/x` unconverted. This was recorded as a limit by the F6 ruling; Case
  R16 uses the single-quoted form.

**PM flags for the round-3 review (G2-n)** — details the PM added to make the manager's round-2
dispositions implementable, or inconsistencies found while applying them. They are reported, not
resolved.
- **G2-1 — reason codes (D12).** The deterministic M4/M6 nodes need a fixed `reason` per UNKNOWN
  kind. Without one, `M4-missing-snapshot` under M-unknown could still exit 11 through the
  internal-failure path and pass.
- **G2-2 — "not repeated" for the new-drive kind.** The ruling names "M4-newroot" as a
  not-repeated node, but M4 is standalone, and standalone ignores `announced`. The PM added a
  hook-mode node, H11-newroot-once. The missing-root case also needs dedupe, or the other sessions
  open during the operational `subst` window would see an UNKNOWN every turn after the mapping is
  removed. The PM proposed the `rootgone` kind, which is not in the manager's list.
- **G2-3 — per-host failure with one junit.** "Fails on each host where the arm is valid" can only
  be read from one junit if every test evaluates all hosts before asserting and names each host's
  result (D20).
- **G2-4 — context hints.** The guard cannot tell a JS regex or a cmd switch from a path, so the
  node-regex and cmd-switch remedies are emitted for every refusal inside a `node` body or a `cmd`
  body (D7 sentence 5). The ruling did not say when to emit them.
- **G2-5 — the M-sessionfile mutation needs an id-length constraint.** Keying on the first 8
  characters leaves single-session file names unchanged only if those tests use ids of at most 8
  characters. Otherwise H1, H4, H6 and H10 also fail, which is harmless to the gate but noisy.
  H4-badid-129 needs a short `tmp_path` (152-character file name; see the MAX_PATH budget).
- **G2-6 — P4h under G-heredoc.** The heredoc-prose row fails deterministically under G-heredoc,
  but the ruling keeps G-heredoc's must-fail set at R18 only. Should P4h be added?
- **G2-7 — no arm for the `?` sanitizer or the word-boundary directory-change match.** These are
  new controls from the message ruling. The PM proposes G-sanitize and G-cdsubstring.
- **G2-8 — `python -W ignore -c …`.** "Before the first non-option argument" needs option-value
  awareness: python `-W`/`-X` take a value, and node options such as `-r`/`--require`/`--import`
  do too. Otherwise the value reads as the first non-option and the code body falls to D4, which
  still refuses non-leading tokens but allows R20-shaped forms.
- **G2-9 — AC1 literal vs must-address (5).** With a missing `cwd` there is no drive to name. The
  plan reads must-address (5) as governing that case, so "AC1 met literally" holds only for a
  drive-letter `cwd`.

**Manager rulings on G2-1–G2-9** (2026-10-28; made by the main session acting as manager under
the owner's delegation, not by the owner; applied in place above)
- **G2-1** — accepted: the D12 reason codes. Every M4/M6 must-fail node asserts its specific reason
  code, never just exit 11.
- **G2-2** — accepted: H11-newroot-once, and the `rootgone` kind with its own "not repeated" node
  (H12-rootgone-once) and arm M-dedupe-rootgone.
- **G2-3** — accepted as written in D20.
- **G2-4** — accepted: the node-regex hint on every refusal inside a `node` body; the
  space-separated-switch hint on every refusal inside a `cmd` body.
- **G2-5** — single-session ids stay at most 8 characters, and the 129-character id is kept. AC7
  and local runs use `--basetemp=C:\ht\T`. H4-badid-129 asserts that no file was created in
  `-SnapshotDir`, because a MAX_PATH exception would be caught as UNKNOWN.
- **G2-6** — yes: P4h is added to G-heredoc's must-fail set.
- **G2-7** — yes: G-sanitize (must-fail P1a-nonascii) and G-cdsubstring (must-fail P1a-cdword) are
  in the gate.
- **G2-8** — accepted: option-value awareness (D5(i)); refuse Case R21; the residual is recorded in
  the coverage limits.
- **G2-9** — accepted: the wording in D7 and must-address (5).

**PM flags raised in Plan v2, round 1** (history, as raised; the manager's rulings follow; F3's
"withhold" interpretation is withdrawn by the round-2 message ruling)
- **F1 — R7 vs AC6.** R7 adds a temp file (atomic replace) and a per-session lock file. AC6
  allows "a single snapshot/report file" as its one write exception. Either AC6's exception is
  read as "the snapshot file and its transient temp/lock companions in the same non-root
  directory", recorded as a delegated interpretation, or the design changes.
- **F2 — R5 template is not ASCII.** The template uses `…`, and the guard must stay pure ASCII.
  Plan v2 renders it as `...`, and P1 asserts the ASCII form.
- **F3 — R5 "conservative" is undefined, and the first sentence contradicts it.** "Where nothing
  converts it" is false for a conservative refusal. The PM definition in D7 is: a token in a
  `powershell`/`pwsh`/`cmd` body reached from a Bash region. That needs per-word position tracking
  through `Get-Delegation`'s joined body, and a distinct first sentence for the conservative
  variant. Also, AC1 says the refusal names the resolved path; R5 omits it in more cases than the
  invalid-`cwd` case must-address (5) covers (directory changes, conservative refusals). This
  narrows AC1 and should be recorded as a delegated interpretation. *(The R5 omission rule this
  flag describes was withdrawn in round 2, AR2-S1; see D7.)*
- **F4 — R1 `$(...)` handling.** The helpers R1 allows (`Split-Segments` and the others) do not
  recognize `$(...)`. The scan needs its own span extraction and removal before D4, as D5
  specifies. R1 also narrows AC1(b) ("any script body … unconverted region") for Bash-region
  `python -c` / `node -e` bodies at measured-converted positions. That is a deviation from AC1's
  literal text, to be recorded as a delegated interpretation.
- **F5 — R15 expected-fail sets.**
  - G-boundary cannot fail L1–L4, which have no `/<letter>/` sequence.
  - G-region cannot fail R3 or R7, which are still refused through D4 / the `pwsh -c` body.
  - G-offset will also fail R4, R5, R10, R16b, R17, P3 `>/d/x`, P4a and P4f.
  - The table above applies these corrections. As written, R15's sets would trip the merge rule
    on G-boundary and G-region.
- **F6 — Case R16 as written cannot pass.** `Split-Segments` has no backslash-escape handling, so
  `eval "tool \"-D /d/x\""` re-scans as `tool \-D /d/x\` with `/d/x\` at offset 0 → allowed.
  R16b (single-quoted) is the PM's proposed replacement.
- **F7 — G-heredoc cannot discriminate Case R19.** The here-string body is already refused by D4
  (non-leading `'/d/x'`). Only R18 discriminates the heredoc rule.
- **F8 — R15 "one junit per host" vs D20's in-body host loop.** The monitor file yields one junit
  covering both hosts unless a host-selection seam is added, and D10 forbids environment
  overrides.
- **F9 — corpus pass privacy (R4).** The transcripts are the owner's local data. Plan v2 keeps
  hits in gitignored `artifacts/` and commits counts and the FP rate only.
- **F10 — R14 / R1.** A 5-level command gets both the existing nesting reason and the drive-token
  depth reason. P6b asserts that the existing reason is present, and P7's prefix assertion must
  not be applied to P6b.

**Manager rulings on F1–F10** (2026-10-28; made by the main session acting as manager under the
owner's delegation, not by the owner; applied to Plan v2 above)
- **F1 — design changed, AC6 unchanged.** One file per session, and the snapshot file is its own
  lock:
  - an exclusive handle (`FileShare.None`), `OpenOrCreate` at SessionStart and `Open` at Stop;
  - written in place under that handle (truncate, write, flush);
  - no temp file and no separate lock file;
  - a concurrent instance that cannot open it is a silent no-op / exit 0;
  - a crash mid-write leaves an invalid file, handled by the invalid-snapshot rules.

  AC6's single-file exception holds literally. Applied in D14, D15, must-address (3), H1, H6,
  M5 and the M-compact / M-lock arms.
  *PM reconciliation note:* R7's mid-session baseline needs Stop to create a missing file, which
  `Open` alone cannot do. D14 creates it with `CreateNew` under the same exclusive handle. This
  is still one file, but the manager should confirm it in round 2.
- **F2 — accepted.** `...` (pure ASCII). P1 asserts pure ASCII.
- **F3 — conservative defined.** (a) A `powershell\|pwsh -Command\|-c` or `cmd /c\|/k` body
  reached from the Bash region. (b) A Bash-region `python -c` / `node -e` code body. Both use the
  first sentence `Refused conservatively: '<token>' is a POSIX drive path inside a nested command
  body; MSYS may or may not convert it.`. Withholding the resolved path is recorded as a delegated
  interpretation of AC1, grounded in owner must-address (5) *(withdrawn in round 2, AR2-S1: the
  clause is now always present for a drive-letter `cwd`; see D7)*. Applied in D7, P1, P7 and
  must-address (5).
- **F4 — D5(i) restored; AC1(b) is literal, with no narrowing.** Python-family verbs resolve
  through `Get-VerbCandidates`, with `-c` anywhere, including clusters such as `-Ic`. `node` uses
  `-e`, `--eval`, `-p` or `--print`. These bodies are scanned as Unconverted with conservative
  wording. New discriminating row Case R20 `python -c "x=/d/y"`. The function implements its own
  `$(...)` extraction, mirroring `Invoke-CommandScan`'s loop without calling or editing it.
  Applied in D4, D5, D7, D8 (P4f), R17, R20 and a new G-interp arm.
  *Consequence for F5's G-offset set:* R4, R5, R10, R17 and P4f are now decided by D5(i), not
  D4. G-offset's expected-fail set is therefore R8, R9, R16, P3 `>/d/x` and P4a, and those rows
  move to its expected-pass column.
- **F5 — accepted**, with the F4 consequence above.
- **F6 — accepted.** Case R16 is now `eval 'tool "-D /d/x"'`, and the backslash-escaped-quote
  tokenizer limit is in the coverage limits.
- **F7 — accepted.** G-heredoc expected-fail = R18 only; R19 stays as a regression row.
- **F8 — accepted.** One junit per run covers both hosts inside each test body; every assertion
  message names the host; no host-selection seam is added.
- **F9 — accepted.** Hits stay in gitignored `artifacts/`; committed docs carry counts and the FP
  rate only.
- **F10 — accepted.** Applied in P7.

---

## Sign-off

- [x] Gate 0 complete when required by planning size; otherwise marked not applicable.
- [x] Every finding has a disposition (round 1; manager under delegation).
- [x] Every round-2 finding has a disposition (manager under delegation).
- [x] Every round-3 finding has a disposition (manager under delegation).
- [x] Agent provenance complete — both `product-manager` IDs, same-PM-resumed yes/no, the three reviewer IDs (rounds 1–3), and an evidence-gap line (none).
- [x] Plan v2 (final, rev. round 3) accepted for Gate 1 — **delegated acceptance** by the main session acting as manager under the owner's 2026-10-28 delegation; not the owner's personal review.
- [x] Ready to implement — **under the delegated Gate 1 acceptance above**; proceed to code, then `/unslop` or `/verify-and-polish` for the diff-time gate.

**Gate 1 — delegated acceptance**

> Accepted 2026-10-28 by the main session acting as manager under the owner's 2026-10-28
> delegation. Basis: three council rounds; all blocking findings (AR-B1, AR-B2, TS-B1..B4, PR-B1
> in round 1; TS2-B1..B3 in round 2) resolved; round 2 architecture and product-risk and round 3
> test-strategist returned no blocking findings; every non-blocking finding accepted (one sub-item
> rejected with rationale). This is delegated acceptance, not the owner's personal review of Plan
> v2.

This `product-manager` (agent `a96acae55b870d077`) recorded the acceptance text as the manager
supplied it. The PM did not give the acceptance.

---

## Evidence — implementation (senior-developer, 2026-10-28)

*Historical implementation handoff: written by senior-developer. From the diff-time review onward
this section was owned by the `product-manager` (agent `a96acae55b870d077`), at the manager's
direction. Later corrections and final-candidate evidence are labelled below; the original
agent's execution scope and dated results are retained.*

Implementation level only; no commit, push, merge, installation or AC7 arm was run by this
agent. Gate 2 is not marked. Base `c29ddf0740ecd9dd90e65424c37050c764504431` (clone HEAD and
`origin/main`, re-confirmed after the owner's PC shutdown; every result below is a fresh
post-restart run). Retained output: `artifacts/msys-impl/` (gitignored; pre-shutdown runs kept
apart in `pre-shutdown/`).

*The figures in "Changed paths", "Commands and results" and "Measured new nodes" below were
**measured at `3d85fd9f`** (the first candidate). For the fix commit, see "Fix commit `a7aa5163`"
after them.*

**Changed paths** (measured at `3d85fd9f`)
- `.claude/hooks/guard-destructive-command.ps1`: +350 / −0 (1692 lines). D1–D8 as
  self-contained functions before the entry point. The entry point gains two payload reads
  (`tool_name` → `Get-DriveTokenRegion`, `cwd` → drive letter) and one call
  `Invoke-DriveTokenScan $command $driveTokenRegion 0` inside the existing loop and `try`. The
  header gains a "Drive-token rule" paragraph. No pre-existing line edited. Pure ASCII, BOM,
  CRLF.
- `.claude/hooks/drive-root-monitor.ps1`: new, 871 lines. D9–D18. Pure ASCII, BOM, CRLF.
- `docs/test_inventory/TEST_INVENTORY.{md,json}`: regenerated by the generator: +48 for the new
  file, 4127 → 4175 deterministic nodes.
- Tests were not edited by this agent (automation-qa's files).
- SHA-256: `artifacts/msys-impl/13-sha256.txt`.

**Commands and results** (measured at `3d85fd9f`; `.venv` Python 3.15.1; both hosts present: powershell 5.1, pwsh 7.6.9)

| # | Command | Exit | Result |
|---|---|---|---|
| 01 | pytest guard+monitor `-k "drive_token or hook_source or test_drive_root_monitor"` `-n 8` | 0 | 256 passed, 1 skipped (H8b, non-Windows only) |
| 03 | pytest `tests/test_guard_destructive_command.py` full, `-n 8` | 0 | 2229 passed in 436 s |
| 04 | pytest `tests/test_drive_root_monitor.py` (serial) | 0 | 47 passed, 1 skipped (H8b) in 70 s |
| 05 | pytest agent-workflow + ci-expansion + worktree-ci contracts, `-n 8` | 0 | 578 passed |
| 06/07 | `generate_test_inventory.py`, then `--check` | 0 / 0 | "Test inventory is up to date." |
| 08/09 | `npx pyright@1.1.410 --outputjson`; `pyright_baseline_diff.py` | 0 / 0 | 0 errors, 0 warnings; 0 net-new |
| 10 | flake8 CI blocking selection on the two test files | 0 | 0 |
| 11 | flake8 advisory (`--exit-zero`, 127 cols, complexity 10) | 0 | 5 × E501 (all pre-existing on base) + 1 × C901 (new, in the monitor test file) |

Measured new nodes: 194 drive-token nodes in the guard file (97 × 2 hosts) plus 3 monitor
`test_hook_source_*` nodes (the guard file is 2229, environment-dependent and excluded from
the inventory); 48 monitor nodes, host-looped in the body. (Measured at `3d85fd9f`.)

**Fix commit `a7aa516317a27fcc6350da6368a41221d03f386f`** (figures as reported by the manager)
- Guard: +351 / −0 against base `c29ddf07`, 1693 lines. "No pre-existing line edited" holds
  **relative to base `c29ddf07`**. The fix rewrote lines that the first commit had added.
- Monitor: 872 lines.
- Inventory: the monitor file goes from 48 to 49 nodes (4176 deterministic nodes in total);
  `--check` exits 0.
- The retained `artifacts/msys-impl/fix1/03-guard-full.txt` records 2245 passed on the earlier
  pre-P4i working tree. It does not prove the complete committed `a7aa5163` or final-candidate
  collection. P4i and P4i-escaped add four host-specific nodes; the exact `68d52ba7` restored
  guard run below passes all 2249. The `a7aa5163` → `68d52ba7` delta adds no test cases.
- Monitor file: 48 passed, 1 skipped (H8b).
- Contract files: 578 passed.
- pyright baseline diff: 0 net-new.
- Measurements the fix relies on: M-12 in
  `docs/msys_destination_validation/evidence/MEASUREMENTS_20261028.md`.

**Corpus pass** (R4, F9 ruling):
- `docs/msys_destination_validation/evidence/CORPUS_PASS_3d85fd9f.md`: 60 hits in 12,442
  commands, classified by class.
- The sed/regex false-positive class was accepted by the manager and pinned as P4i.
- The final `68d52ba7` re-run is appended to that file: 69 hits in 12,612 commands. All 60 earlier
  hits remain; the nine additions introduce no new false-positive class.

**Design choices where the plan left room**
- The refusal echoes the whole path from the D3 token to the next delimiter (`/d/development/x`,
  not only `/d/development`), so the resolved path matches the case table. Tests accept both
  readings.
- D2 and D4, and the parts D5/D6 decide, are separate functions (`Get-DriveTokenRegion`,
  `Test-DriveTokenConverted`, `Get-DriveTokenInterpreterBody`, `Split-DriveTokenHeredocs`,
  `Get-DriveTokenSubstitutions`). *(Corrected by the PM:)* The AC7 arms actually run are
  per-control literal patches, not one mutation point per function. The initial definitions were
  `C:\ht\MSYS-AC7\harness\arms.3d85fd9f.json`; the validated final definitions are retained as
  `C:\ht\MSYS-AC7\runs\68d52ba7-sol-full\arms.json`, with all arm gates passed. The drive-token depth
  reason reads "Drive-token rule: nesting exceeds 4 levels ...". It deliberately avoids the
  existing "command nesting exceeds" wording, so P6a stays discriminating.
- Hints are explicit for Bash-reached `cmd` and `node` bodies. In a raw Unconverted scan they
  come from a word-bounded `cmd /c|/k` or `node` match in the raw text.
- Delegated bodies: every token after the delegating verb is exempt from D4. This mirrors the
  existing walk's "rest of the segment is the nested command".
- Monitor JSON uses its own strict reader and writer, not `ConvertFrom-Json`/`ConvertTo-Json`:
  PowerShell 7 converts ISO strings to `DateTime`, which would alter `createdUtc`. Output is pure
  ASCII (`\uXXXX` escapes).
- Standalone `Snapshot` records `source` `startup`. A SessionStart `source` outside
  startup/clear/resume/compact is treated as `startup`. The `midsession` key is
  `midsession|<session id>`.
- A hook-mode protected-path or root-parent refusal gives the D18 internal-failure text at Stop
  (no D18 text exists for it) and silence at SessionStart. An unparseable Stop payload gives the
  invalid-session-id text.
- `unknown[].root` is `null` for snapshot-level and argument reasons. `protected[]` lists the
  built-in H4 paths plus any `-ProtectedPath`.
- A root absent from the snapshot is `root-new` if it exists now and `root-missing` if it does
  not. In hook mode both are the `newroot` kind and use the "was not present" text.
- Non-Windows sharing violation: HResult 11 or 35 (EWOULDBLOCK), with the .NET message text
  as a fallback.

**Migration notes** (CLAUDE.md §1 refactor invariant). No product workflow
(plan/log/analyze/progress/distribute/backup), schema, API shape or calculation is touched.
Calculation surface `none` (Section 0) holds, so there is no worked example to cross-check.
Agent-workflow behaviour change: Bash/PowerShell tool calls carrying an unconverted POSIX drive
token now deny (exit 2) in every profile and mode. A payload whose `tool_name` is not exactly
`Bash` is scanned as unconverted. The monitor adds no registration (D19: user level, installed
by the manager).

**Known reds / gaps at the initial implementation handoff** (resolved manager steps are recorded
in the final-candidate evidence below).
- No red in the scope above.
- Linux pwsh was not run locally (no WSL on this host). The monitor's POSIX paths (the `flock`
  sharing violation in H6/H1-held, `chmod 000` in M4-unreadable-root, H8b) are first exercised
  by CI.
- AC7 arms, the S0-d H4 creation-time check, the corpus pass and `code-reviewer` are not done
  (manager steps).

---

## Diff-time review (round 1)

**Candidate:** commit `3d85fd9febb7b5bd1ec5755fdf7294425f380fc0`, PR #654 (draft).

**Reviewers:**
- `code-reviewer`, agent `a2a2781864144fd32`;
- `unslop-reviewer`, agent `a280ec8cb8a9dddbc`.

The finding summaries below were relayed by the manager. The original PM did not read the
reviewers' reports; verbatim copies were not yet in `reviews/` at that recording step and are
now retained there.

**Dispositions:** made by the **main session acting as manager under the owner's 2026-10-28
delegation**, not by the owner. All are accepted. Nothing is deferred or rejected.

| Finding | Reviewer | Summary | Disposition | Fix / plan amendment |
|---|---|---|---|---|
| CR-1 | code-reviewer | A colon-bound PowerShell parameter (`-Path:/d/x`) is not refused: a **fail-open**. | accept | The attached-option boundary accepts an optional colon, `-[A-Za-z]+:?` (D3). The D4 converted prefix also accepts `-[A-Za-z]+:`, which the manager reports measured converted in Bash. New rows R23 (refuse), A24 and A25 (allow). |
| CR-2 | code-reviewer | A doubled slash `/d//x` escapes the token: a **fail-open**. | accept | The token allows repeated slashes after the letter (D3). New rows R24 (refuse; `GetFullPath` measured → `D:\d\x` per the manager) and A26 (allow; measured `D:/x` per the manager). |
| CR-3 | code-reviewer | Same-depth heredoc or interpreter scans clobber the directory-change hedge flag. | accept | The flag is computed once per command at the entry point (D7). Rows P1b-cd-heredoc and P1b-cd-interp. |
| CR-4 | code-reviewer | The converted-prefix regex uses `$`, which also matches before a trailing newline. | accept | Use `\z` (D4). Row P3-refuse-newline. |
| CR-5 | code-reviewer | A zero-length snapshot left by a failed baseline write sticks as invalid. | accept | A zero-length file held at Stop takes the mid-session baseline branch (D14). Node H13-zero-length. |
| CR-6 | code-reviewer | The header says "hook modes ALWAYS exit 0", but an unrecognised `-Mode` exits 11. | accept | The header is softened to "recognised hook modes" (D13). No behaviour change: exit 11 is non-blocking. |
| UN-1 | unslop-reviewer | Same as CR-3. | accept (= CR-3) | As CR-3. |
| UN-2 | unslop-reviewer | Plan and finding-ID prefixes in code comments. | accept | Remove them and keep the invariant text. One header-level pointer to the plan stays. |
| UN-3 | unslop-reviewer | Duplicated default snapshot-directory logic. | accept | Deduplicate it. |
| UN-4 | unslop-reviewer | `Get-ProtectedList` is a needless indirection. | accept | Inline it. |
| UN-5 | unslop-reviewer | Two comments restate the code. | accept | Drop them. |
| UN-6 | unslop-reviewer | The PLANNING D7 prose does not match the code. | accept — resolved by CR-3 | After the CR-3 fix the code matches D7. The Evidence sentence about AC7 arms is corrected (see the Evidence section). |

**AC7 amendments** (applied in place in the Plan v2 arm table):
- G-noop must-fail set gains R23 and R24.
- G-offset must-fail set gains P3-refuse-newline.
- M-midsession must-fail set gains H13-zero-length.
- P1b-cd-heredoc and P1b-cd-interp remain `restored`-only regression requirements, not arm-gated.
  The manager originally wrote that G-message-always "does not affect the hedge"; the actual
  final mutation suppresses it. The measured resolution below corrects that earlier rationale.

**Plan amendments applied in place**
- D3: repeated slashes; optional colon in the attached-option boundary.
- D4: `-X:` prefix; `\z`.
- D7: hedge flag computed once per command.
- D13: "recognised hook modes".
- D14: zero-length held file at Stop.
- Case table: A24–A26, R23, R24.
- P1b-cd-heredoc, P1b-cd-interp, P3-refuse-newline, H13-zero-length.
- AC1/AC2 mapping ranges: R1–R24, A1–A26.

**PM flag (historical text; measured resolution follows).** The Plan v2 arm table describes G-message-always as "the plain
non-conservative clause is always emitted, ignoring `cwd` validity, directory change and
conservativeness". It lists P1b-* as must-fail, which includes P1b-cd and P1b-setlocation. The
manager's note says G-message-always does not affect the hedge. If the patch in
`arms.3d85fd9f.json` matches the note and not the table, then P1b-cd and P1b-setlocation will not
fail under it, and the merge gate trips. Either the table's mutation text and must-fail set are
corrected to the actual patch (P1b-* minus the hedge nodes), or the patch also suppresses the
hedge. The manager decides.

*Resolution, 2026-10-28:* the manager accepted the measured `68d52ba7` result under the owner's
delegation. The retained patch always emits the plain resolved clause, substitutes `D` for
invalid/missing `cwd`, and removes the hedge. The designated must-fail set is P1b-cd,
P1b-conservative-interp, P1b-conservative-ps, P1b-emptycwd, P1b-garbage, P1b-nocwd,
P1b-setlocation and P1b-unc on each host: all 16 failed. The arm recorded 20 failures in total;
the additional four are the two-host P1b-cd-heredoc and P1b-cd-interp rows, which remain
`restored`-only requirements under the existing ruling. They are recorded, not added to this
arm's gate. The pending set is resolved; the earlier hedge rationale is superseded by this patch
and observed outcome. Evidence: `C:\ht\MSYS-AC7\runs\68d52ba7-sol-full\G-message-always\`.

### Diff-time review (round 2) — delta review of fix commit `a7aa516317a27fcc6350da6368a41221d03f386f`

The verbatim files `reviews/diff2-*` are retained. Summaries were relayed by the manager.
Dispositions are by the manager under the owner's delegation; all accepted.

| Reviewer | Result | Disposition / owner of the action |
|---|---|---|
| `code-reviewer` `a2a2781864144fd32` | All six round-1 findings (CR-1 to CR-6) resolved; no new defects. Residual: it relies on the recorded M-12 measurements (`evidence/MEASUREMENTS_20261028.md`). | accept; residual recorded under the fix-commit evidence |
| `unslop-reviewer` `a280ec8cb8a9dddbc` | Items 1, 3, 4 and 5 resolved; items 2 and 6 partial at this review; new cosmetic items. | accept. Test-file ID/attribution cleanup and header rewrap completed in `68d52ba7`, merged by #654. The manager rechecked that final delta. PLANNING evidence labels, wording, G-message-always resolution and corpus reference are recorded in this closeout. |

The cleanup and rewrap landed in #654 and were rechecked by the manager against `68d52ba7`.
The exact candidate's CI and restored tests pass, and the pending planning evidence is reconciled
above. Items 2 and 6 are resolved under the manager's delegation; no additional independent
review is claimed for the final cosmetic delta.

---

## Final candidate and acceptance — 2026-10-28

Recorded by fresh Codex `product-manager` `/root/product_manager`, at Sol's direction, from the
active artifact and verified `artifacts/sol-closeout/facts.json`. The original PM
`a96acae55b870d077` was **not resumed** for this closeout; the continuity gap is limited to that
handoff. The council identities, reviews and Gate 0/Gate 1 provenance above remain unchanged.
The decisions below are **delegated manager acceptance**, not the owner's personal review.

**Exact candidate:** `68d52ba74a53a8ba4807842e512719b12e0a94fb`, based on `c29ddf07`.
The final delta from `a7aa5163` changes comments, documentation, assertion wording and the
`refusal_sentences` helper name; it adds no test cases or production behavior. Against base,
the guard is +352 / −0, 1694 lines; the monitor is 872 lines.

| Level | Acceptance and evidence |
|---|---|
| Implementation | **Accepted (delegated).** Exact-candidate CI: 34/34 successful checks, including all 12 protected context/app pairs. AC7: 15 guard arms and 19 monitor arms passed every designated failure gate; all 244 guard must-fail nodes failed, and all 33 monitor must-fail nodes failed on both Windows PowerShell and pwsh (66 host outcomes). `restored`: **2301 passed, 1 documented H8b skip** — guard 2249; monitor 48 passed / 1 skipped; registration probe 4. Final corpus: 69 refusals among 12,612 commands; no new false-positive class or unexpected exit code. Code-reviewer follow-up and the final cosmetic recheck are distinguished above. |
| Merge | **Accepted (delegated).** [PR #654](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/654) merged through normal protections as `d8e3e3c61866ca0fa123693335d65775d880225e` at `2026-10-28T15:56:55Z`. Merged guard blob `427ae4c5ff28f23a41d765ae1e40928237d064fb` and monitor blob `6993a66d530fe2725d4fadc5c826ee1673d8765f` match the tested candidate; source branch retained. |
| Installation | **Accepted (delegated).** User guard and monitor match those merged blobs. Expanded staged/installed probes and `verify_install.ps1` passed. User settings changed by a verified pure insertion, preserving LF, absence of BOM and existing settings. Monitor registrations are **user-level only**; the shared checkout remains untouched. Transcript `C:\ht\MSYS-INSTALL\transcript-20261028T155730Z.json`; backup `C:\ht\MSYS-INSTALL\backup-20261028T155730Z`; prepared rollback `C:\ht\MSYS-INSTALL\ROLLBACK.ps1`. The fake-profile install and byte-for-byte rollback rehearsal also passed. |
| Operational | **Accepted (delegated), within the measured headless scope.** Fresh VS Code extension bundled `claude.exe` **2.1.310** session `ff872564-63a6-4d82-a4e8-d39a32deb274`: exact guard refusal, SessionStart snapshot before first tool, first Stop silent, NEW child notice and UNKNOWN notice all passed. The controller injected invalid JSON only into this test session's own TEMP snapshot. All four Stop hooks exited 0; CLI exited 0. Stop durations were 0.3549763, 0.3568104, 0.3959337 and 0.3159702 seconds. The fixture child and `Q:` subst mapping were removed. Evidence `C:\ht\MSYS-OPS\run-sol-20261028T155934Z`. |

The first operational attempt, `C:\ht\MSYS-OPS\run-sol-20261028T155803Z`, remains **INCOMPLETE**:
Claude declined to corrupt its test snapshot, so UNKNOWN was not exercised. Its first three
phases passed and its fixture mapping was removed; it is not credited as full acceptance. The
second fresh session above supplies the complete result.

AC7 retained evidence: `C:\ht\MSYS-AC7\runs\68d52ba7-sol-full\SUMMARY.md`, `summary.json` and
`host-audit.json`, with per-arm patches, hashes, commands, junit and logs. The final corpus and
manual reconciliation remain under `C:\ht\MSYS-AC7\corpus\run-68d52ba7-sol`; committed counts
are in [the corpus record](evidence/CORPUS_PASS_3d85fd9f.md). Summary:
[ACCEPTANCE_20261028.md](evidence/ACCEPTANCE_20261028.md). H4 creation times were unchanged
after AC7 and in the final after-operational check. Shared-checkout guard/settings hashes
remained unchanged through installation and operational acceptance.

**Operational label:** fresh headless session on the VS Code extension's bundled `claude.exe`
2.1.310; payload fields and Stop notice measured on bundled 2.1.310 (headless) and CLI 2.1.302;
panel rendering unmeasured (open); detection exercised on a substitute (subst) root; guard shown
on one harmless row; charter-frontmatter payloads inferred. Other open sessions may show one
UNKNOWN notice when the fixture drive appears or disappears; their UI was not inspected.

These four levels close this packet within the approved bounded scope. The textual guard still
cannot see script-file contents, stdin, run-time-built paths, MCP parameters or non-Claude
processes. The monitor sees direct root children between snapshot and compare; writes beneath
an existing child remain invisible. The standing warnings and other coverage limits above
remain. `PREVENTION_COMPLETE` is not claimed.
