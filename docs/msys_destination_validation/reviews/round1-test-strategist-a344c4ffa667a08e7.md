# test-strategist (agent `a344c4ffa667a08e7`) — Plan v1 review, round 1, verbatim final message

## Required gates

I read the plan, the measurements and the clone at `c29ddf07` read-only. I ran no tests.

- **pytest (local, both hosts):**
  - `tests/test_guard_destructive_command.py`, in full.
  - `tests/test_drive_root_monitor.py`.
  - `tests/test_agent_workflow_contracts.py::test_all_effective_destructive_registrations_execute_deny_allow`. Its payloads (lines 552–563) carry no `tool_name` and no drive token, so they are unaffected by the strict rule.
  - `tests/test_ci_expansion_contracts.py` and `tests/test_worktree_ci_contracts.py` (line 72). Both stay green only if `ci.yml` is untouched.
- **CI, derived from `ci.yml`:**
  - `pytest-core` (lines 1023–1090) picks up the new monitor file automatically because it runs `tests/` with only the guard file ignored. It has a 20-minute budget and has measured 2.3–3.6 minutes.
  - `guard-hook-shard` ×4 (lines 1184–1229) and `guard-hook-tests` (lines 1244–1272) cover new guard nodes with no workflow change.
  - `verify` fails any skipped node, and `union` requires identical collections across the four legs.
  - `Run Tests` fan-in (line 1352).
- **Test Inventory Drift:** regenerate for the new test file (QUALITY_GATE.md:71–83). The guard file is exempt as environment-dependent (`generate_test_inventory.py:65–74`).
- **Type Check:** `tsc` has no impact. The pyright baseline diff applies repo-wide (QUALITY_GATE.md:97).
- **Lint:** applies.
- **e2e:** none. `e2e/program-backup.spec.ts:79` is not touched.
- **Conftest:** the plan's "none" is correct. There is no new blueprint or table.

## Existing coverage

- `.claude/hooks/guard-destructive-command.ps1` has the 322/163-node file (322 on a host with both PowerShell versions, 163 on the ubuntu runner).
  - Only line 201 has a converted-position drive token. Line 200 is a deny anyway, and line 872 denies on the env-mutation rule. I checked this with grep.
  - `test_hook_source_is_ascii_with_bom` and `test_hook_source_parses` (lines 947–979) will pin the new monitor script automatically through the `HOOK_SCRIPTS` glob (line 868).
  - `test_denied_payload_never_executes_its_child` is at line 932.
- `drive-root-monitor.ps1` has no existing coverage.

## Findings

### Blocking

**B1. AC7 arms do not cover each control, and nothing can fail on the allow side.** (PLANNING.md:176–184, 517–534)

AC7 says "each control". Five arms exist: guard-whole, monitor-new, monitor-unknown, monitor-write and hook-exit.

- **Missing controls.** These have no arm, so their tests are never shown to fail without them:
  - D11 first-writer-wins, `session_id` validation and the protected-path refusal.
  - D12 dedupe and the lock skip.
  - D13 newly-mounted root.
  - D14 `faultShapedPresent`.
  - H5 session isolation.
  - D2 region selection, D4 Bash grammar and D6 resolved-path message. The guard arm replaces the whole function, so it cannot attribute a failure to any one of these.
- **Allow side.** The A-rows and L-rows pass trivially under a no-op, so no arm can fail them. Memory says to run every mutation in both directions.
- **Proposed arms** (small `git apply` patches, hashed like the others):
  - Over-refuse: drop the boundary lookbehind. A-rows A10a–d and L-rows must fail.
  - Region forced to `Bash`. R1–R3, R7, R11, R13, R14 and R12 must fail.
  - D4 offset rule neutralized. R8 and R9 must fail.
  - D6 message neutralized. P1 must fail.
  - `CreateNew` changed to `Create`. H1 must fail.
  - `reported[]` ignored. H3 must fail.
  - Per-session filename made constant. H5 must fail.
  - Lock skipped. H6 must fail.
  - `session_id` regex removed. The H4 invalid-id variant must fail.
  - D13 and D14 each disabled.
- H1 must also create a new child between the two SessionStart calls and assert the snapshot is unchanged. Otherwise the overwrite arm cannot fail.

**B2. D4 and D5 contradict each other, and D5(i)/(ii) cannot be tested.** (PLANNING.md:396–397, 296–302)

- D4 refuses any drive token not at offset 0 or after the allowed prefixes, and applies this to the quote-stripped Bash word.
  - The body of `python -c "import os; os.makedirs('/d/x')"` is one such word. The token sits at offset ~24, so D4 refuses it with no D5 involvement.
  - R4, R5, R6 and R10 can therefore be satisfied by D4 alone. D5(i) (python/node body recovery) and the powershell/cmd half of D5(ii) have no observable effect, so no test or arm can show they work.
- The same D4 rule would refuse the outer word of `bash -c "gh run download 1 -D /d/development/x"`.
  - The inner bash would convert that token, which sits in a leading position there. D5(ii) says "re-scan as Bash", which implies allow.
  - The case table has no row for this very common form, so the expected decision is undefined.
- **Proposed change:**
  - Decide that delegated-body words are exempt from D4 and are decided only by the re-scan.
  - Add an allow row: `bash -c "gh run download 1 -D /d/x"`.
  - Add `cmd /c "python -c ..."`, `eval` and `$()` rows. AC1(b) names `cmd /c` but no row covers it.
  - Add a row for `.venv/Scripts/python.exe -c`, `python -Ic` and `python3.12 -c`. The verb list `python|python3|py|pythonw` misses these, and the first is this repo's own form.
  - Otherwise delete D5(i) as redundant.

**B3. P6 cannot fail under the guard arm, so the arm's prediction is wrong.** (PLANNING.md:496, 524–525)

- The depth deny is existing code at `guard-destructive-command.ps1:1108–1111`. It fires before any scan, with `$maxDelegationDepth = 4` at line 85. A no-op `Invoke-DriveTokenScan` leaves P6 green.
- The plan blocks the merge when an expected test does not fail, so the plan would block itself.
- **Proposed change:**
  - Remove P6 from the list of tests expected to fail.
  - Either pin it as an existing-behaviour test, or change it to a five-level `Unconverted` body that must be refused by the raw scan with the drive-token reason in stderr.

**B4. The built-in protected-path test would write into the real H4 trees when neutralized.** (PLANNING.md:403, 502, 511)

- D11 hard-codes `D:\dev-cleanup-20260824-digest` and `D:\_digest-discard-bin`. Those paths do not exist on the Linux CI runner, so CI can only test the additive `-ProtectedPath`.
- A Windows test that points the snapshot at the real H4 path is safe when the control works. If the control is neutralized, `CreateNew` succeeds and creates a file in a preserved tree. That breaks AC6, and the plan has no arm for it.
- **Proposed change:**
  - Test only through `-ProtectedPath` with `tmp_path`.
  - Add a pure-computation mode or JSON field (for example `protected[]`) and assert that it lists the built-in H4 paths.
  - Never neutralize this control against a real path.

### Should-fix

**S1. D4's prefix regex disagrees with M-6, and the plan has stale items.** (PLANNING.md:396, 441–443, 271, 493)

- M-6 measured that any `<word>=` prefix converts, including the chained `a=b=/d/y`. D4's pattern `^(?:[A-Za-z_]\w*=)?(?:...=|-[A-Za-z]+)?$` allows one `NAME=` only, so `a=b=/d/y` would be refused despite being converted. Widen the pattern to `(?:[^\s=]+=)+`.
- S0-a is now answered, so P3 `x=/d/y` is allow.
- M-7 (a `subst` drive enumerates as Fixed) contradicts the Q5 limit wording and S0-b. The operational probe that depends on it (lines 556–559) is now justified. Update both places.

**S2. Deny assertions can pass for the wrong reason.**

- `outcome()` (test lines 87–109) returns `deny` for any exit 2. The guard's catch also exits 2 (guard lines 1339–1342). A throw in the new function, or a typo, would satisfy any P-row that only checks the outcome.
- Only R-rows are specified to check stderr. P2, P5 and P6 check only the outcome.
- **Proposed change:**
  - Add a helper returning `(decision, stderr)`.
  - Every drive-token deny asserts a fixed reason prefix.
  - Every A/L assertion asserts that stderr contains no "failing closed" and no drive-token reason.
- P5's sentinel assertion is vacuous in both directions, because the guard never executes the command. Its only discriminating part is the deny assertion.

**S3. SessionStart stdout becomes model context.** (PLANNING.md:402, 503; MEASUREMENTS:23–25)

- M-1 shows SessionStart stdout is returned as context. D10 applies the "UNKNOWN notice" to every hook failure.
- H1 should assert that `HookSessionStart` stdout is empty in every case, including failures. Any notice must go to stderr or stay out of context.

**S4. Windows/Linux divergence in the monitor tests.** (PLANNING.md:501, 508)

- **H6 lock.** .NET `FileShare.None` on Linux is an advisory `flock`.
  - A Python `open()` holds no flock there, so the test cannot block the monitor.
  - On Windows a plain `open()` does block it.
  - The test needs `fcntl.flock` on POSIX and a plain handle on Windows.
- **M4 unreadable root.** `chmod 000` is skipped on Windows, so the unreadable-root path is never exercised on the machine that produces AC7 evidence. Use `icacls /deny` on a `tmp_path` directory on Windows.
- **pyright.** `pyrightconfig.json` sets `pythonPlatform: Windows` and does not exclude `tests/`. `os.geteuid` and `import fcntl` would be flagged as net-new diagnostics. Use `getattr(os, "geteuid", None)` and an `importlib` import.

**S5. Evidence covers only one host and the wrong exit code for bad arguments.**

- CI runs only Linux pwsh for the guard and monitor files. The real hook host is Windows PowerShell 5.1 (M-8 registration). Specify that every AC7 arm and the restored arm run under both hosts, with one junit file per host.
- D9 promises exit 11 for bad arguments. A typed `param()` fails at binding with exit 1, before any catch. The guard documents this at lines 58–64. State that the monitor parses `$args` and add a bad-argument test that asserts 11.

**S6. Forcing an internal error has no defined seam.** (PLANNING.md:506, 530; D8 forbids env overrides)

- H4 "forced internal error" and the `neut-hook-exit` arm need a reachable catch.
- Name the trigger, for example a `-SnapshotDir` that is a regular file. Add a test that the arm's patched `exit 2` is reached.

**S7. Concurrency was measured but the tests are sequential.** (MEASUREMENTS:72–79; PLANNING.md:503, 508)

- M-9 shows concurrent SessionStart hooks overlap and unlocked appends lost lines.
- Add H1c, which launches N concurrent `HookSessionStart` processes with `Popen`. It asserts exactly one valid snapshot, all exit codes 0, and empty stdout.
- Specify behaviour for an existing snapshot that is locked or half-written (silent no-op).

**S8. Isolation from real roots is a convention, not a test property.** (PLANNING.md:400, 510)

- Use a single `run_monitor` helper that always injects `-Root` and `-SnapshotDir`, and assert that no test bypasses it.
- H8 (default roots) should call a print-only mode and not Snapshot. Snapshot would list the real drive roots.
- Add a non-Windows test: with no `-Root`, the monitor exits UNKNOWN and does not crash. D8's `X:\` formatting is wrong on Linux.

**S9. Timing and collection hygiene.**

- Do not run the full guard file per AC7 arm. It took 28 minutes serially in CI and has 322 nodes on a two-host Windows machine.
  - Run `-k drive_token` per arm.
  - Run the full file once on the restored arm.
- The "roughly 60 extra pwsh processes" estimate (PLANNING.md:478) needs a count tied to the real case table and `P2` loops. The Linux legs already have a 12.5-minute straggler against a 20-minute budget (`ci.yml:1172–1177`).
- Use plain labels as parametrize ids (`A1`, `R3`). R3's command contains brackets and R6's contains quotes, and the shard argfile must round-trip the node ids.
- A missing PowerShell host must fail inside the test body and must not raise at import. An import-time failure breaks collection, the inventory generator and all of `pytest-core`.

**S10. D14 has no test, and the Stop hook may be noisy.** (PLANNING.md:406, 404)

- Add H9: a pre-existing single-letter child produces one Stop notice per session, the exit code stays 0, and the standalone JSON lists it. Pair it with the D14-off arm from B1.
- D12 announces a missing snapshot on every Stop. Every session already running at installation time has no snapshot, so it would show the notice every turn.
- A resumed session keeps the same `session_id` (M-9), so the stale snapshot makes legitimate later children report as new.
- Decide the behaviour explicitly: baseline-at-first-Stop plus a single notice, and re-snapshot on `source=resume`. Then test it.

### Notes

- Add R12 variants for `"bash"`, `null`, a non-string `tool_name` and `"Bash "`. D2 uses `-ceq`, so all of them are Unconverted.
- M1's static check that the script never references `audit-worktrees` or the baseline would trip on a header comment documenting the independence. Check non-comment tokens only.
- Compare children with case sensitivity matching the host, and assert that reported paths equal the root string as given joined with the child name.
- Stop fires every turn (M-1) and enumerates every fixed drive. Record its measured latency against the 30-second timeout in the operational evidence.
- `workflow-contracts-windows` runs only six cases, so no Windows CI job exercises the monitor. The plan's decision to leave `ci.yml` untouched makes this an accepted gap. State it in the plan.
- Gates that apply without further action: the inventory per-file count for the monitor file is machine-independent as long as it is not parametrized by host at collection, as D16 says. `tests/conftest.py` needs no change.

## Conftest / fixture work

None for `tests/conftest.py`. Fixture work is limited to D17 in the guard test file, covering the roughly fifteen direct `json.dumps` sites. Only lines 200–201 need a Bash `tool_name` to keep their expected decisions.

## Verdict

**Targeted gate sufficient** on the change surface: no schema, `app.py`, `conftest.py` or `ci.yml` change, and the gates above. **Plan v1 is not ready for Gate 1 as written.** Plan v2 must resolve B1–B4, which change the case table, the arm list and a safety property, and should address S1–S10. Without B1–B3, the AC7 evidence step would fail its own "expected test must fail" check or leave controls unproven.

Files read:
- `C:\ht\MSYS\docs\msys_destination_validation\PLANNING.md`
- `C:\ht\MSYS\artifacts\msys-gate0-20261028\MEASUREMENTS_20261028.md`
- `C:\ht\MSYS\artifacts\msys-gate0-20261028\RECONCILIATION_INPUT.md`
- `C:\ht\MSYS\.claude\hooks\guard-destructive-command.ps1`
- `C:\ht\MSYS\tests\test_guard_destructive_command.py`
- `C:\ht\MSYS\tests\test_agent_workflow_contracts.py`
- `C:\ht\MSYS\tests\test_ci_expansion_contracts.py`
- `C:\ht\MSYS\tests\test_worktree_ci_contracts.py`
- `C:\ht\MSYS\.github\workflows\ci.yml`
- `C:\ht\MSYS\scripts\generate_test_inventory.py`
- `C:\ht\MSYS\scripts\ci_executed_report.py`
- `C:\ht\MSYS\docs\ai_workflow\QUALITY_GATE.md`
- `C:\ht\MSYS\pyrightconfig.json`