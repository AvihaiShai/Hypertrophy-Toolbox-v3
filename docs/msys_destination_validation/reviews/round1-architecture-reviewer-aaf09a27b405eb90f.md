# architecture-reviewer (agent `aaf09a27b405eb90f`) — Plan v1 review, round 1, verbatim final message

# Architecture review: MSYS destination validation, Plan v1

Reviewed against `origin/main` `c29ddf07` in `C:\ht\MSYS`. No Flask module-boundary, blueprint, schema, `DatabaseHandler`, response-contract or logger items apply, because this is `.claude/hooks` and tests only. The findings below cover guard and monitor design, registration, CI placement, and the M-6..M-9 contradictions.

I found 2 blocking, 9 should-fix and 5 note-level findings.

## Blocking

**B1. PLANNING.md:408-409, 524-526 — AC7 neut-guard expects P6 to fail, but P6 can never fail**
- Evidence: P6 is "Five-level delegation → deny". The existing walker already denies at depth > 4 (`guard-destructive-command.ps1:85`, `:1109-1111`), whatever any drive-token function does.
- Risk: the neut-guard arm lists P6 among the tests that must fail. Plan line 534 says "An arm whose expected test does not fail blocks the merge", so the plan blocks its own merge deterministically.
- Fix: rewrite P6 to assert two things. A 4-level nested R-row command is denied with the drive-token reason in stderr. A 5-level command is denied with the existing nesting reason, as a pin that the new rule adds nothing there. Then drop P6 from the neut-guard expected-fail list, or split it so only the first half is listed.

**B2. PLANNING.md:393 (D1), 397 (D5) — D1 cannot deliver D5(ii) as written**
- Evidence: D1 says `Invoke-DriveTokenScan` is "called once per candidate command at the entry point" and the destructive-verb walk is "byte-unchanged". D5(ii) needs delegation bodies re-scanned as `Bash` or as `Unconverted`, and recursion exists only in `Invoke-CommandScan` (`guard:1108-1228`):
  - the `'script'` dispatch is at `:1178` and `:1216`;
  - the `$(...)` recursion is at `:1132-1145`.
- Risk: the implementer must either edit `Invoke-CommandScan`, which breaks the stated AC3 mitigation, or re-implement the recursion in the new function. Both are unspecified, and the neutralization arm's "one function no-ops it" claim holds only for the second.
- Fix: state that `Invoke-DriveTokenScan` owns its own recursion. It may call `Split-Segments` (`:237`), `Remove-Wrappers` (`:302`) and `Get-Delegation` (`:809`) as read-only helpers. It never touches `Invoke-CommandScan`. Its own depth guard should reuse `$maxDelegationDepth`. Say explicitly that `$(...)` bodies inside Bash words are refused by the embedded-token rule rather than recursed into.

## Should-fix

**S1. PLANNING.md:396 (D4) — M-6 contradicts D4's prefix regex, and S0-a is now decided**
- Evidence: M-6 measured that any `<word>=` prefix converts, including a chained `a=b=/d/y` → `a=b=D:/y`. D4's regex `^(?:[A-Za-z_]\w*=)?(?:-{1,2}[A-Za-z][\w-]*=|-[A-Za-z]+)?$` allows one `NAME=` followed by one `--opt=`. It refuses `a=b=/d/y`, which AC2 says must not be refused.
- Risk: a measured-converted form is refused, and P3's "`x=/d/y` per S0-a" row has no stated outcome.
- Fix: widen the prefix to zero or more `[A-Za-z_][\w.-]*=` or `--opt=` groups, then an optional `-[A-Za-z]+`. Make `x=/d/y` and `a=b=/d/y` explicit allow rows in P3. Delete S0-a from the sequence, since it is measured.

**S2. PLANNING.md:271, 270, 555-558 — M-7 contradicts the Q5 limit text and the operational probe's conditional**
- Evidence: M-7 shows a `subst` drive enumerates as `DriveType Fixed`. Q5's limit ("Removable, network and `subst` drives are not monitored"), the S0-b hedge and the "If S0-b shows…" branch were written before it.
- Risk: the approved limit text is factually wrong, and the operational subst probe is still written as conditional.
- Fix: correct the Q5 limit wording in Plan v2 and record it as a post-Gate-0 correction (the AC and defaults are unchanged). Make the `subst Q:` probe unconditional. State that a drive mounted mid-session is UNKNOWN (D13), not NEW, so the probe must map `Q:` before the session starts, as already written.

**S3. PLANNING.md:403, 405 (D11/D12) — M-9 resume behaviour leaves the baseline stale and the invalid-file case undefined**
- Evidence: M-9 shows `--resume` keeps `session_id`, and SessionStart fires again with `source=resume`. D11 makes an existing valid snapshot a no-op, so the baseline can be days old and every unrelated root child created since reads as NEW. D11 also does not say what SessionStart does with an existing invalid or empty file left by a crash between `CreateNew` and the write.
- Risk: noisy or permanent false notices, and a stuck UNKNOWN session.
- Fix: key on the payload's `source`. `startup` and `clear` atomically replace any existing snapshot, and `resume` and `compact` keep a valid one. Any invalid file is replaced at SessionStart only, never at Stop, which keeps the operational "overwrite with invalid JSON" proof working. Do not prune old snapshots, because that would breach AC6's one-file exception. Add an H-row for each branch.

**S4. PLANNING.md:402 (D10), 503-504 (H1/H2) — SessionStart and Stop stdout are model-visible channels and are not pinned**
- Evidence: M-1 and `MEASUREMENTS:24-25` say SessionStart stdout is returned as `hook_response` context. Stop stdout is parsed as hook JSON.
- Risk: any stray pipeline output injects text into model context, or corrupts the Stop JSON. This is easy to cause in PowerShell 5.1.
- Fix: require `HookSessionStart` to write nothing to stdout, with any notice going through `systemMessage` only. H1 asserts empty stdout. H2 asserts stdout is exactly one JSON object with only a `systemMessage` key (never `decision`), under both hosts.

**S5. PLANNING.md:394-395, 494 (P4), 296-299 — false positives on PowerShell-tool prose are not covered**
- Evidence: in the `Unconverted` region D3 scans raw text of the whole command. This repo's docs, PR bodies and commit messages routinely quote `/c/Users/…` and `/d/development/…`. P4 pins only the Bash commit-message case (Q3b).
- Risk: the manager's own `gh pr create --body` and `Set-Content` calls under the PowerShell tool are refused with no stated remedy.
- Fix: add a P4 row for PowerShell here-string, `-m` and `--body` text. Require the refusal message to include the remedy ("write `D:/…` or `D:\…`") so a refusal is self-resolving.

**S6. PLANNING.md:494 (P4) — the `rmdir /s/q tmp` row does not match D4**
- Evidence: P4 says "`rmdir /s/q tmp` deny (combined switches)". `/s/q` fits the AC1 token shape. In a `Bash` region it sits at offset 0, which D4 calls converted, so it would be allowed. In `Unconverted` it is denied. P4 names no tool.
- Fix: name the tool and region per row, `PowerShell` for this one. Add `cmd /c "xcopy /e/i/y a b"` and `cmd /c "dir /b/s"`, which are legitimate cmd idioms refused through the `cmd /c` body. Pin them as accepted false positives, or exclude cmd bodies (and amend AC1(b), which names only `powershell|pwsh`). Do not leave them implicit.

**S7. PLANNING.md:397 (D5(i)) — `python -c` / `node -e` detection is too narrow for this repo's own invocations**
- Evidence: D5(i) says "`-c` … the following token". This repo's canonical interpreter is `.venv/Scripts/python.exe`. Real forms also include `python -I -c`, `python -W ignore -c`, `-Ic` clusters and `node --input-type=module -e`.
- Risk: R4 and R5 pass in simple form while AC1(b)'s "any script body" is missed.
- Fix: scan the argument after the first token that matches the interpreter's code flag anywhere in its argument list. Resolve the verb through `Get-VerbCandidates` (as `Get-Delegation` does at `guard:815`). Add `python.exe`-path and `-I -c` rows to the case table.

**S8. PLANNING.md:432-433, 541-548 — installation replaces a live, fail-open-on-parse-error guard non-atomically**
- Evidence: a parse error exits 1, which is non-blocking (`test_guard_destructive_command.py:951-955`). A partial copy over `C:\Users\aviha\.claude\hooks\guard-destructive-command.ps1` therefore leaves every Bash and PowerShell call unguarded for that window. Install step 2 verifies hashes only.
- Fix: copy to a temp name in the same directory, verify the hash and parse under both `powershell` and `pwsh`, then `Move-Item -Force` into place. Run the deny/allow probe from `test_all_effective_destructive_registrations_execute_deny_allow` against the installed path immediately, before any other step. Use the same sequence for rollback.

**S9. PLANNING.md:213-214, 412-413, 422-434 — "documentation … in the workflow surface the plan names" is missing**
- Evidence: Section 0's In-scope list requires it. The Artifacts table names only header docstrings. Sequence step 10 says "the handover", i.e. `docs/MASTER_HANDOVER.md`, which is a declared shared-state file (WORKSTREAM_OWNERSHIP), and it is neither in Artifacts nor claimed.
- Fix: name the documentation surface (for example the existing guard references in `docs/agent_workflow_integrity/PLANNING.md` or `docs/ai_workflow/`). Add `docs/MASTER_HANDOVER.md` and any new claim in `WORKSTREAM_OWNERSHIP` to Artifacts, or drop the handover edit.

**S10. PLANNING.md:399-402 (D7-D10) — enumeration semantics are unspecified**
- Evidence: M-7 and Q5 widen the root set to C, D, E, F. `C:\` contains hidden or system children such as `$Recycle.Bin` and `System Volume Information`.
- Risk: without `-Force`, a new hidden child is missed. A full `Get-ChildItem` can throw on protected entries. Case-sensitivity differs between the Windows and Linux CI hosts.
- Fix: specify names-only enumeration (for example `[IO.Directory]::EnumerateFileSystemEntries`), non-recursive, with no reparse-point following. Specify an ordinal ignore-case comparison on Windows. Define that an enumeration error on a root is UNKNOWN for that root.

## Notes

- **N1. D15 / `.claude/agents/*.md`:** the guard is also registered in the senior-developer and automation-qa charters (matcher `Bash|PowerShell`; the charter registrations are probed at `tests/test_agent_workflow_contracts.py:524-531`). The guard therefore runs up to three times per call (project, user and charter), not two as D15 says. Deny-wins still makes this harmless. Correct the wording only.
- **N2. D17 / PLANNING.md:409:** the payload sites lacking `tool_name` also include `tests/test_agent_workflow_contracts.py:295,561` and `tests/worktree_cleanup/guard-contract.ps1:39`. None carries a converted-position token, so no decision flips and none needs a fixture edit. List them so the grep claim is complete.
- **N3. Windows PowerShell 5.1 coverage (D16):** the monitor's tests run only in `pytest-core` on Linux pwsh 7. The Windows CI leg is pinned to the two `test_agent_workflow_contracts` tests (`ci.yml:1305`). That matches the guard's existing precedent, since the 5.1 behaviour tests are local-only, and the guard gets a 5.1 parse check from the registration probe. State in Plan v2 that the monitor's 5.1 behaviour is verified locally only (the `HOSTS` loop) and that H8 does not run in CI.
- **N4. D12:** if the announce-then-record ordering is "append `reported[]` then print", a crash between them loses the notice. Print first, then record. Specify the order.
- **N5. D14 / coverage limits:** a concurrent session legitimately creating a root child will appear as NEW in every other live session. Add this to the coverage limits.

## Checked and sound

- Q1(a) in-guard placement, with no new registration, is consistent with project `settings.json:48-58` and M-8.
- D15 user-level-only monitor registration is correct given that hooks merge across levels.
- D16 placement is consistent with `ci.yml:1084` (core ignores only the guard file) and `ci.yml:1184-1229` (four shards).
- The `HOOK_SCRIPTS` glob (`tests/test_guard_destructive_command.py:868`) pins the monitor's ASCII + BOM and parse automatically on both hosts.
- `ENVIRONMENT_DEPENDENT_PYTEST_FILES` (`scripts/generate_test_inventory.py:65`) needs no change for a body-looped monitor file.
- AC3's two conflicts, lines 201 and 872 plus the cmd switches, are correctly resolved. Only 200/201/872 carry tokens in the guard tests (grep, blob in clone).
- The other eight charter items are not triggered.

**Verdict: Needs revision.** B1 and B2 must be resolved before implementation, and S1-S4 and S8 before Plan v2 is accepted.

Files read:
- `C:\ht\MSYS\docs\msys_destination_validation\PLANNING.md`
- `C:\ht\MSYS\artifacts\msys-gate0-20261028\MEASUREMENTS_20261028.md`
- `C:\ht\MSYS\artifacts\msys-gate0-20261028\RECONCILIATION_INPUT.md`
- `C:\ht\MSYS\.claude\hooks\guard-destructive-command.ps1`
- `C:\ht\MSYS\.claude\settings.json`
- `C:\ht\MSYS\.github\workflows\ci.yml`
- `C:\ht\MSYS\tests\test_guard_destructive_command.py`
- `C:\ht\MSYS\tests\test_agent_workflow_contracts.py`
- `C:\ht\MSYS\scripts\generate_test_inventory.py`