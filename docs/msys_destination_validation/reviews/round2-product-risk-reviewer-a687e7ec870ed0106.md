# product-risk-reviewer (agent `a687e7ec870ed0106`) — Plan v2 delta review, round 2, verbatim final message

# Round 2 delta review of Plan v2 (`PLANNING.md`)

Plan v2 resolves most round-1 findings, with some partial resolutions and no blocking issues. M-10 (`MEASUREMENTS_20261028.md:81-88`) narrows PR-N1. The wording check below found two copy problems: the conservative-refusal remainder (NEW-1) and the "since this session started" notice text (NEW-2). Both are should-fix.

## Round-1 findings

| ID | Status | Evidence |
|---|---|---|
| PR-B1 | **Partially resolved** | D7 (`:793`) hedges, withholds the resolved path when `cwd` is invalid or the command contains a directory change, and uses a distinct "Refused conservatively" first sentence. P1 (`:971-977`) asserts the hedge and the absence of "create". The remainder is still wrong for the conservative case (NEW-1). |
| PR-S1 | **Partially resolved** | D3 (`:789`) adds the exclusions `~ * % } ) ] $`, with cases A16-A21 (`:956-961`) and a corpus pass (`:912-915`). The rejected JS-regex exclusion is pinned as P4f (`:985`), which is reasonable. Two gaps remain (NEW-3, NEW-4). |
| PR-S2 | Resolved | The remedy text is in the D7 template and pinned by P1 and P4. |
| PR-S3 | Resolved | H10, the `CreateNew` mid-session baseline and the D18 mid-session text (`:804`, `:1038`). The invalid-snapshot notice has no exact text (NEW-2). |
| PR-S4 | **Partially resolved** | D18 (`:804`) says "Cause unknown; not necessarily created by this session" and the single-letter text says "origin is not known". The "since this session started" phrase is wrong after `resume`, `clear` or a mid-session baseline (NEW-2). |
| PR-S5 | **Partially resolved** | Installation steps 1-8 (`:1089-1113`) cover backup, ROLLBACK.ps1, a staged probe, `.new` plus hash plus `Move-Item`, and settings last. Step 7 has a lost-update race and a serialization hazard (NEW-5). |
| PR-S6 | Resolved | Proven-unused letter, `subst` set immediately before the session and removed immediately after, and the record that other sessions may show one UNKNOWN notice (`:1120-1128`). |
| PR-S7 | **Partially resolved** | The operational label states its limits (`:1129-1132`). It is now stale after M-10, and the session runs the wrong binary (NEW-6). |
| PR-N1 | Resolved by M-10 | The matrix row (`:759`) and the coverage limit (`:1138-1139`) still say "not measured" (NEW-6). |
| PR-N2 | Resolved | D1 states the try/catch (`:787`); P8 forces an exception inside the scan (`:994-995`). |
| PR-N3 | Resolved | The TEMP accumulation note goes in the monitor header (`:865`); snapshots are never deleted (D14, `:800`). |
| PR-N4 | Resolved | The Stop latency is recorded in the operational evidence (`:1127`). |
| PR-N5 | Resolved | D16 and the coverage limits (`:1137`). |

**Wording check.** Every message text in D7 (`:793`) and D18 (`:804`) is pure ASCII. The only non-ASCII glyph near them is `…` at `:971`, which is test prose and not message text.

## New findings

**NEW-1 (should-fix). `:793`: the conservative-refusal remainder contradicts its own first sentence.**
- The first sentence says "MSYS may or may not convert it". The unchanged remainder then asserts "A native Windows program resolves it under the current drive root".
- P1 would pin that pairing.
- Fix: for the conservative variant, replace the second sentence with "If MSYS does not convert it, a native Windows program resolves it under the current drive root." Keep the textual-check sentence and the remedy. Assert the exact text in P1.

**NEW-2 (should-fix). `:804`, `:813`, `:800`: notice texts are incomplete or inaccurate.**
- "since this session started" is false after a `resume` or `clear` re-snapshot, and after a mid-session baseline.
  - Fix: use "since monitoring began at <UTC time from the snapshot>".
- No exact text exists for these cases:
  - an invalid snapshot
  - an internal-failure UNKNOWN
  - an invalid `session_id`
  - a snapshot root that is now missing or unreadable
  - the third D18 text, "has no snapshot (new drive?)", which is wrong for the missing-root case
- Fix: add a fixed ASCII text for each, with no cause claimed. Example: `Drive-root monitoring: snapshot invalid or unreadable; UNKNOWN. No claim is made about drive roots.` Pin each text in H2, H4 and M9.

**NEW-3 (should-fix). `:985`, `:794`, `:912-915`: the P4f remedy is wrong and the corpus pass has no action threshold.**
- The remedy "write it drive-qualified" does nothing for a JS regex such as `/a/g`. D8 gives a special remedy only for cmd switches.
- Fix: add a remedy for the `node -e` regex case: use `new RegExp(...)` or a script file.
- The corpus pass (step 6) records hit counts but gates nothing.
- Fix: state an action rule. Any false-positive class that appears more than once in routine commands blocks the merge, or needs recorded manager acceptance with the class named.

**NEW-4 (note). `:793`: the `cd` detection must be word-bounded.**
- The text does not say so. Substring matching only errs toward withholding, which is safe, but it would also remove the clause from the operational probe if the command text happened to match.
- Fix: add a P1 pair, one with an identifier containing `cd` (clause emitted) and one with a real `cd` (clause withheld).

**NEW-5 (should-fix). `:1107-1111`: step 7 settings.json edit.**
- Another running session can rewrite user `settings.json` between the read and `Move-Item -Force`, for example when it saves a permission rule. That would be a lost update.
- Fix: re-hash the original immediately before the move and abort if it changed.
- The plan does not forbid reserialization. PowerShell 5.1 `ConvertTo-Json` defaults to `-Depth 2` and would truncate nested hooks.
- Fix: require a textual insertion that preserves bytes, BOM and line endings. Verify that the diff is a pure insertion and that existing `SessionStart` and `Stop` entries, if any, are byte-identical.

**NEW-6 (should-fix). `:759`, `:1115`, `:1129-1132`, `:1138-1139`: M-10 makes several statements stale.**
- The operational session uses CLI 2.1.302, but the VS Code extension runs its bundled 2.1.310.
- Fix: run the operational probe on the bundled 2.1.310 binary, or add it as a second run. Update the label to "payload fields and Stop notice measured on the extension's binary, headless; panel rendering open". Update the PR-N1 row and the coverage limit.

**NEW-7 (note). `:791`, `:795`: smaller points.**
- D5(i) scans `-c` "anywhere in its arguments". `python tool.py -c /d/x` has a leading, MSYS-converted token and would be refused conservatively. This is a small false positive; record it as P4h.
- "Conservative" is defined per body (F3), not per token position. So `python -c "makedirs('/d/x')"`, where nothing converts the token and the resolution is certain, gets no resolved-path clause. This is safe but less informative; consider per-position classification later.
- The token is echoed as written. A non-ASCII token would make the emitted message non-ASCII. Fix: add a P1 variant with a non-ASCII token, and either sanitize it to `?` or accept and pin the behavior.
- The template hard-codes "D:/... or D:\..." in the remedy. Use the token's letter.

## Confirmed good

- The `PREVENTION_COMPLETE` ban stands.
- Installation is recorded as performed by the manager under delegation (`:1088`).
- The calculation surface stays `none`, and no app or DB file is touched (`:874-880`).
- The monitor is read-only with a single snapshot file (D14, F1).
- Hooks never block (D13).
- The operational label states its limits.

**Verdict: no blocking findings.** There are six should-fix findings (NEW-1, NEW-2, NEW-3, NEW-5 and NEW-6, plus PR-S5's step 7 under NEW-5) and two notes (NEW-4 and NEW-7). Fold them into Plan v2 or the implementation before Gate 1 acceptance.