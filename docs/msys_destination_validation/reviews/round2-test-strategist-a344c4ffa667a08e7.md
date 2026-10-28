# test-strategist (agent `a344c4ffa667a08e7`) — Plan v2 delta review, round 2, verbatim final message

## Round 2 delta review: test-strategist (Plan v2)

Read-only. I read Plan v2 cold, then checked it against the guard source and the measurements, including M-10 (`MEASUREMENTS_20261028.md:81-88`). M-10 only supports the `PR-N1` note and does not affect any test finding.

## Round-1 disposition

| Round-1 id | Status | Evidence |
|---|---|---|
| TS-B1 (per-control arms, both directions) | Partially resolved | The arm table exists at 1061–1082 with an over-refuse arm (G-boundary) and per-control monitor arms. The expected sets have errors, listed under TS2-B1 to TS2-B3 below. The protected-path and root-parent refusals still have no arm (TS2-S1). |
| TS-B2 (D4/D5 contradiction, rows) | Resolved | The exemption for delegated and interpreter bodies is in D4 (790). D5(i) is restored (791). R20 `python -c "x=/d/y"` discriminates it: D4's prefix allows `x=`, and the body is then refused by the raw regex because `=` is not a boundary exclusion. A14–A15, R15–R17 are added (954–967). |
| TS-B3 (P6 false-green) | Resolved | P6a (4 levels, drive-token reason, in the G-noop fail set) and P6b (5 levels, existing reason at `guard:1108-1111`, a pin) at 989–990. |
| TS-B4 (protected-path hazard) | Resolved | Only `-ProtectedPath` under `tmp_path` and the print-only `protected[]` are tested (1007), and nothing is neutralized against a real path. |
| TS-S1 | Resolved | The D4 prefix regex at 790 matches M-6, including chained `a=b=`. |
| TS-S2 | Resolved | `outcome_with_stderr` and P7 at 807 and 991–993. P5 is declared non-discriminating (987). |
| TS-S3 | Resolved | D13 (799) and H1 empty stdout (1022). |
| TS-S4 | Resolved | `fcntl.flock`, `icacls /deny` and `getattr(os, "geteuid", None)` (738, 1006, 1031). |
| TS-S5 | Resolved | Guard arms run under each host, monitor tests loop hosts in the body (F8, 1052–1057), and the monitor parses `$args` with bad arguments → 11 (M7, D9). |
| TS-S6 | Resolved | The forced-error seam is `-SnapshotDir` pointing at a regular file (1029). |
| TS-S7 | Partially resolved | H1c and H6 exist, and F1 removed the lock file. H1c is non-deterministic as an arm expectation (TS2-B1). |
| TS-S8 | Resolved | `run_monitor`, `ListRoots` and H8b (M8, 1034–1035, 1043). |
| TS-S9 | Resolved | `-k` per arm, plain ids, the measured count, and a missing host failing in the test body (806, 1053–1057). |
| TS-S10 | Partially resolved | H9, H10, M-fault and re-snapshot on resume exist. The once-per-session state for the fault shape, the new-drive notice and the mid-session notice is not specified, so it is unproven (TS2-S2). |
| TS-N1 to TS-N5 | Resolved | R12 variants (968), M8 non-comment tokens (1044), M9 (1045), latency record (1127), accepted gaps (943–946). |
| TS-N6 | Informational | No action needed. |

## New findings

### Blocking

**TS2-B1. M-lock lists H1c as an expected fail, but H1c can pass with the control neutralized.** (1078, 1023)

- With the handle opened `FileShare.ReadWrite`, N concurrent SessionStarts all write the same content in place. The file is usually still valid, so H1c passes under the mutation, and it is non-deterministic.
- The merge rule would then block randomly. Without that rule, no merge-proof of the lock exists.
- Fix: M-lock's expected-fail set is H6 and the H1 "held by another handle" variant, which are deterministic. H1c becomes a pass-column or smoke test only.
- The H1 held variant must be its own id (see TS2-B3).

**TS2-B2. Expected sets are incomplete or contradict the tests, and the merge rule blocks on any mismatch.** (1061–1082)

- **G-noop** (1063). Its fail list omits P2 and P7, which also assert drive-token denials. P8 passes under G-noop provided the injection anchors on the function header, and it must be listed in the pass column.
- **G-region** (1065).
  - P4c `rmdir /s/q tmp` (PowerShell) also fails. In the Bash region, `/s/q` leads its word and counts as converted.
  - P1's PowerShell variants fail too.
  - R3 and R7 will break if their case-table asserts require the non-conservative prefix, because the Bash path emits the conservative prefix. State that R-rows and P7 accept either prefix.
- **G-interp** (1067).
  - R17 and P4f are marked "(conservative)". With D5(i) off they are still refused, but with the plain `Refused: '` prefix.
  - Any row that asserts the conservative sentence therefore breaks. Only P1 may assert that sentence. R17 stays in the pass column only if its assertion is "either prefix".
  - The patch must disable both the D5(i) scan and the D4 exemption. If the exemption stays, R4, R5 and R17 become allowed and fail instead of passing. The plan's wording is "fall back to D4"; the patch spec must say so.
- **G-offset** (1066). P6a depends on which Case-R row is innermost. It must be pinned: a D5(i) row such as R4 passes under G-offset, and an R9-style row fails. Add it to the matching column.
- **M-new** (1070). Its fail list omits H10 (a later new child is reported) and M9 (reported path), which also need a new child.
- **M-fault** (1073). If M2 still asserts `faultShapedPresent` non-empty (v1 M2 did), M2 fails too. State that M2 asserts only the exit code.
- **M-write** (1074). The patch location is unspecified. A write placed before enumeration in Compare makes M2 and M1 see a changed root. Specify: write after enumeration in Compare, so M2 stays in the pass column.
- **M-sessionfile** (1077). A constant file name breaks every test that addresses the snapshot by name: H1, H4 (invalid-snapshot variant), H6 and H10 all plant or read `claude-drive-root-<id>.json`. H5 is not the only failure. Either list them all, or choose a mutation that preserves names for single-session tests (key on the first characters of the id and give H5 ids that differ after them).
- **M-sessionid** (1079). Constrain the H4 invalid ids:
  - Traversal ids may go only one level above `-SnapshotDir`, so the neutralized arm cannot reach a drive root.
  - One invalid id must be a valid filename (129 characters), because ids with `*` or `?` throw and are caught, which falsely passes the arm.

**TS2-B3. Several expectations cannot be observed because the tests are single nodes.** (1015–1041)

Merged nodes mean one arm's expected-fail and another arm's expected-pass fall on the same junit entry:
- P1: split into P1a (clause expected) and P1b (clause withheld: bad `cwd`, `cd`, conservative). Then G-message-always fails P1b only and G-message-never fails P1a only.
- P3: split into allow and refuse ids.
- H1: one id per `source` plus a held-handle id.
- H4: separate ids for malformed payload, invalid `session_id`, invalid snapshot and forced error.
- M4: separate ids per variant, including a "newly discovered root" id. M-unknown's "non-new-drive variants" and M-newdrive's "newly discovered root" are unobservable otherwise.

### Should-fix

**TS2-S1. No arm covers the protected-path or root-parent refusal** (D14 "any mode", 800; M6, 1040). Add M-protected and M-root-parent arms. Both use `-ProtectedPath` or a root-parent path under `tmp_path`, with refusal disabled, so they are safe. They are expected to fail M6, and the real H4 path is never touched.

**TS2-S2. The once-per-session mechanics have no stored state or test.** (D15–D18, 801–804; H9, H10)

- D15 appends children to `reported[]` only. Nothing says where "fault shape once per session", "new drive once per session" and "mid-session notice not repeated" are recorded.
- No arm proves any of them.
- Name the snapshot field (for example `announced[]` keys), add a "notice repeated" assertion per kind, and add arms that disable each dedupe.

**TS2-S3. The icacls test needs cleanup.** An `icacls /deny` on a `tmp_path` directory leaves pytest unable to remove it. The test needs `icacls /remove:d` in a `finally`.

**TS2-S4. Arm `-k` selection must include both columns.** An expected-pass test outside the `-k` filter is never observed.

### Notes

- M-unknown (1071): clarify whether the M6 UNKNOWN refusals are in scope for that mutation. They are not covered by "UNKNOWN detection returns none" as written.
- The `-k`-filtered per-arm junit and the single-node granularity in TS2-B3 should be fixed together.

Verdict: blocking: TS2-B1, TS2-B2, TS2-B3