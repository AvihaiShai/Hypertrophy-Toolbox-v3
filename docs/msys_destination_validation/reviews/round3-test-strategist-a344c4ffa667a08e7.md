# test-strategist (agent `a344c4ffa667a08e7`) - Plan v2 rev. round 2 delta review, round 3, verbatim final message

## Round 3 delta review: test-strategist (Plan v2, rev. round 2)

Read-only. I read lines 865–1404 of PLANNING.md and the guard's `Split-Segments` (`guard-destructive-command.ps1:237-292`). G3-1 is reviewed as if it were in the file.

## Round-2 findings

| Finding | Status | Evidence |
|---|---|---|
| TS2-B1 (H1c nondeterministic) | Resolved | H1c is a smoke test in no must-fail set (1160–1161, 1262). M-lock is Windows-hosts-only, with H6 and H1-held as must-fail (1254). |
| TS2-B2 (sets wrong or incomplete) | Resolved | The gating model is now a must-fail set plus "everything passes on `restored`", with no expected-pass column (1225–1226). |
| TS2-B2 (message asserts) | Resolved | R-rows and P7 accept either prefix, and only P1b asserts the conservative sentence (1096, 1113–1114). |
| TS2-B2 (G-interp patch) | Resolved | G-interp disables the scan and the D4 exemption together (1236). |
| TS2-B2 (M-sessionfile, M-sessionid) | Resolved | Single-session ids are at most 8 characters, and H5's ids share their first 8 (1142–1144). H4-badid-129 asserts that no file was created (1149–1151). |
| TS2-B2 (M-write location) | Resolved, with a caveat | The write is placed after enumeration in `Compare` (1246). See TS3-S5. |
| TS2-B3 (test granularity) | Resolved | One node per variant: P1a/P1b, P3-allow/refuse, H1-*, H4-*, M4-*, M6-* (1082–1100, 1154–1205). |
| TS2-S1 (protected-path arms) | Resolved | M-protected and M-root-parent (1258–1259), with M6 split (1202). |
| TS2-S2 (once-per-session state) | Resolved, with a caveat | `announced` kinds and per-kind arms exist (900, 1248–1252). See TS3-S3. |
| TS2-S3 (icacls cleanup) | Resolved | `icacls` removed in `finally` (1197). |
| TS2-S4 (-k selection) | Resolved | Each arm runs its must-fail set plus the full selection (1217–1219). |
| Note: M-unknown vs M6 scope | Resolved | M-unknown is stated as "not root-new, not M6" (1243). |
| Notes: `.venv` python rows, M5 scope | Resolved | A15, R17, A22/A23 added (1062–1071); M5 and M2 scope stated (1194, 1200). |

## Arm audit

For each arm I asked three things. Is each must-fail node deterministic? Is it single-purpose? Can it fail when only that control is neutralized?

- **G-noop.** Every R-row, R12 variant, P1a/P1b, P3-refuse, P4a–h, P6a and R21 are allowed by the existing guard, so they fail deterministically. P2, P5 and P7 are listed as "assertions" and need node ids (TS3-N1).
- **G-boundary.** A10a–d, A11 and A16–A21 each contain a token reachable only through the boundary. D4 shares D3's token rules (890), so Bash and PowerShell variants both fail. Sound.
- **G-region.** R1, R2, R11, R13, R14 and the R12 variants all have a leading-word or attached-option token. That is allowed in the Bash region, so they fail. `Split-Segments` does not split on `>`, so R11 and P3 tokenize as the plan assumes. Sound.
- **G-offset.** R8, R9, R16, P3-refuse and P4a are decided only by D4. P6a is pinned to an R9-style innermost row (1110), which is correct. P6a's construction is untested (TS3-N3).
- **G-interp.** R20 is allowed by D4 alone, so it fails. Sound.
- **G-heredoc.** R18 and P4h have only a leading `/d/x` line when D6 is off, so both fail. Sound.
- **G-message-always.** All P1b nodes fail: absent-cwd text, the hedge sentence and the conservative lead. Sound.
- **G-message-never.** P1a nodes fail. Sound.
- **G-cdsubstring.** P1a-cdword fails deterministically. Sound.
- **G-sanitize.** See TS3-S4: it can pass falsely on Windows.
- **M-new.** M1, H2, H3-second, H7, H10-later-child and M9-path all need a detected new child, so they fail. Sound.
- **M-unknown.** Each M4 node asserts its own reason code (898), so neither an internal failure nor an exit 11 can satisfy it. Sound.
- **M-newdrive and M-fault.** M4-newroot, H9-notice and H9-standalone are single-purpose and deterministic.
- **M-compact.** H1-compact-keep fails deterministically.
- **M-sessionid.** H4-badid-129 and H4-traversal both leave a file under `tmp_path` when the regex is gone, on both platforms. Sound.
- **M-protected and M-root-parent.** These write only under `tmp_path`. Sound.
- **M-midsession.** H10-baseline fails. Sound.
- **M-hookexit.** H4-forced-error fails if the error reaches the top-level catch (TS3-N4).
- **M-dedupe-child, -fault, -newroot, -rootgone.** Each is a natural gate and each fails deterministically.
- **M-dedupe-midsession.** Possibly inert (TS3-S3).
- **M-lock.** See TS3-S1.
- **M-sessionfile.** See TS3-S2.
- **M-write.** See TS3-S5.

## G3-1 (G-optvalue)

- As worded ("treat every token after the interpreter as non-option"), the mutation makes `-c` itself a non-option. R20, R4 and R17 then also change behaviour, so it is not single-purpose.
- R21 does fail under it, so the gate is still met.
- Proposed wording: "the value of `-W`/`-X` (and node value options) counts as the first non-option argument; tokens starting with `-` remain options."
  - With that wording R21 fails and R20 passes, which makes the arm single-purpose.
- Add a node-side row for the value-taking node options (`node --require x -e "..."`). The node half of G2-8 has no test today (TS3-N2).

## New findings

None is blocking. Every must-fail node that could pass falsely would trip the merge gate, which blocks the merge. It would not produce a false green.

### Should-fix

**TS3-S1. H6 and H1-held can pass under M-lock unless an unlocked run would visibly act.** (1158, 1177, 1254)

- An unlocked Stop with no new child prints nothing and may leave the file unchanged. An unlocked SessionStart that rewrites identical content also leaves it unchanged.
- Require both nodes to create a new child before the locked call. The unlocked instance would then print or write something different, and the assertion bites.

**TS3-S2. H5 has no stated scenario.** (1176, 1253)

- Under M-sessionfile both sessions share a file. H5 fails only if the scenario makes one session's snapshot visible to the other.
- Specify it. Start session A, create a child, start session B, run Stop for A. A must report the child, and under the mutation it does not.

**TS3-S3. M-dedupe-midsession is only valid if `announced` is the sole gate.** (1251, 904, 900)

- The mid-session notice is emitted when the file is created. The next Stop finds a file and would not re-emit even without `announced`, so the mutation would be inert.
- Specify that Stop emits the notice when `source = stop-baseline` and the `midsession` key is absent. Otherwise drop the arm and H10-once.

**TS3-S4. G-sanitize may pass falsely on Windows.** (1240, 1087)

- A non-ASCII character not representable in the console code page is substituted with `?` by .NET's output encoder, even without the guard's own replacement.
- Use a Latin-1 character such as U+00E9 and assert on raw stderr bytes (no byte above 127). Under the mutation the byte is present on any Latin-1 or OEM code page that contains it.

**TS3-S5. M-write must be exercised by M5.** (1246, 1200)

- M5 must run `Compare` against a valid snapshot. If it only runs `Snapshot` or the hook modes, the patch is never reached and M5 passes.

**TS3-S6. Over-refuse and allow-side controls have no arm.** (1233–1260)

The round-1 request was both directions. Only G-boundary covers the allow side. Proposed arms, each with deterministic must-fail rows:

| Arm | Mutation | Must-fail |
|---|---|---|
| G-region-unconv | D2 always `Unconverted` | A4–A7 |
| G-prefix | the D4 prefix allowance removed (offset 0 only) | A5, A7, P3-allow rows |
| G-exempt-delegated | the D4 exemption for delegated bodies removed | A14 |
| G-nonoption-anywhere | `-c` recognised anywhere among the arguments | A22, A23 |
| M-diff-all | every child reported as new | M2, M3 |

### Notes

- **TS3-N1.** P2, P5 and P7 are named as "assertions" in G-noop's must-fail set (1232). The gate reads node ids, so give each its own node id.
- **TS3-N2.** No row covers node value options (R21 is python-only). Add `node --require x -e "x=/d/y"` as a refuse row.
- **TS3-N3.** P6a needs a concrete command. Split-Segments does not model backslash-escaped quotes (F6), so four levels of quote nesting cannot be built with two quote characters alone. There is also no existing nesting test to copy from (the file mentions depth 4 only at line 30). Use `eval` or `$()` chains and prove the string on the base guard in the step-2 red run.
- **TS3-N4.** For M-hookexit to bite, H4-forced-error must reach the top-level catch. D14's "cannot open because another instance holds it → silent exit 0" must not swallow other open failures. Distinguish a sharing violation from a missing or non-directory parent.
- **TS3-N5.** Define the scope of "every test passes on `restored`" (1226) as the guard file, the monitor file and the registration probe. The full suite carries a recorded pre-existing red.

Final line: no blocking findings