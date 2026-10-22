# Q4 — standalone JS Unit rename

**Owner authority:** the 2026-10-21 ruling in [DECISION.md](DECISION.md),
published through #547, approves `JS Unit (Vitest)` in its own change before
protection changes. The S1 commission on 2026-10-22 authorizes rebuilding the
reviewed candidate `0aa2cd2b8490dffd23caa5a93cc70360a443319f` on current main.
This branch starts at `155181d67a89fe72e86c75a1ff438caec250a9bd` and contains
none of the source branch's ledger or receipt commits; #550 owns those records.

## Change and gates

The `js-unit` display name becomes `JS Unit (Vitest)`. Its identifier, runner,
timeout, dependencies, permissions, steps, install and coverage commands, test
corpus, collection settings and failure propagation stay the same. Workflow
comments and coverage-summary wording reflect the approved decision. The
release contract continues excluding this unprotected check from release
provenance, under its new exact name; release enforcement sets do not change.
The CI PLANNING §7 Q4 row names the current candidate without rewriting its
historical target-set snapshot or other lanes' rows.

The final diff contains five paths: `.github/workflows/ci.yml`, the existing
release contract, `docs/ai_workflow/QUALITY_GATE.md`, this record and the CI
PLANNING Q4 row. `vitest.config.js` is byte-identical to fetched main; no root
config is changed. QUALITY_GATE's workflow row requires full pytest and an
independent code reviewer; its AI-workflow row adds manual review, and its
product-docs row adds no tests. The root-config `/verify-suite` fallback is
not triggered by this final diff. No job is added, removed or converted to
`uses:`. The S1 commission also requires a fresh, independent test strategist.
The existing exact-name contract is updated; no test case is added, removed
or renamed. Run inventory
`--check`, affected workflow/release contracts, JS coverage, TypeScript,
pyright 1.1.410 plus its baseline diff, and blocking flake8. A seeded Vitest
failure must exit nonzero and remain a job failure despite the always-running
coverage summary. Independent reviews and final-head PR CI remain pending
until recorded below; this document grants no merge authority.

## Live protection before publication

Read via `gh api repos/AvihaiShai/Hypertrophy-Toolbox-v3/branches/main/protection`
for this S1 rebuild, server `Date: Wed, 21 Oct 2026 21:42:02 GMT` (the S1
commission is dated 2026-10-22 in the owner's timezone). The connector exposes no protection API, so this is a
read-only REST fallback. Raw response and server-date headers are retained in
`artifacts/s1-q4/protection-before.json` and `protection-readback.txt`.

The floor has exactly **12** required checks, each bound to GitHub Actions
**`app_id: 15368`**, with **`strict: false`**:

| Required context (exact string) | app_id |
|---|---:|
| `Run Tests` | 15368 |
| `E2E Functional (Chromium)` | 15368 |
| `E2E Backup (Chromium, isolated)` | 15368 |
| `E2E Smoke (Chromium)` | 15368 |
| `Type Check (tsc blocking + pyright measure-only)` | 15368 |
| `Code Linting` | 15368 |
| `Frontend Build (npm ci + SCSS)` | 15368 |
| `Security Audit` | 15368 |
| `E2E Fatigue Context (Chromium, non-required)` | 15368 |
| `E2E Erase Flow (Chromium, isolated, non-required)` | 15368 |
| `Test Inventory Drift` | 15368 |
| `JS Supply Chain (npm audit, non-required)` | 15368 |

Neither `JS Unit (Vitest, non-required)` nor `JS Unit (Vitest)` is in that
floor. Renaming the unprotected job therefore orphans no current requirement.
Re-read protection immediately before publishing; preserve all existing
contexts, bindings and strict mode. This packet writes no repository settings.

## §13.0 ledger mapping

The [canonical ledger](../testing_phase3/STEP12_JS_UNIT_GATE0.md) remains the
only producer of qualification rows. Historical rows and snapshots retain
their original exact names and observed conclusions. The source of the
carrier commit determines the expected exact display name:

| Carrier workflow definition | Exact job name to enumerate |
|---|---|
| Before the Q4 rename is present | `JS Unit (Vitest, non-required)` |
| Q4 merge carrier and every descendant retaining this definition | `JS Unit (Vitest)` |

Resolve `.github/workflows/ci.yml` at each carrier's full head SHA, verify the
stable `js-unit` job identifier, then enumerate the carrier's jobs/attempts
for that exact display name. Record run ID, attempt, full head SHA, job ID,
job conclusion and completion timestamp under §13.0. Do not count both names,
credit rerun copies as new executions, or classify the first renamed result
as missing merely because the old name is absent. A genuinely missing,
failed, skipped or cancelled JS job stays adverse; preserve the carrier's
overall conclusion separately under the owner's job-level ruling. Obtain
actual per-run job totals rather than carrying forward a pre-G6 count.

The rename's future merge owes a new observation that this PR cannot yet
write. No row number, merge SHA or successful post-merge result is predicted.
Q4 changes no JS case or executable collection setting, so it does not itself
restart T0. U1 #551 independently changed the post-cycle corpus; this packet
does not relabel its current tests as the historical qualification corpus.

## Readiness, qualification and enforcement

Q4 readiness means the bounded diff, required tests, fresh independent reviews
and all CI on the final PR head pass. It does not mean the rename has merged.
D2's owner signature is conditional on the declared
`2026-08-27T23:18:21Z` → `2026-09-10T23:18:21Z` cycle being recorded through
§13.0 with zero adverse exact JS Unit jobs. The canonical cycle rows are on
main through #544; #550 separately carries the effective-state receipt and
later ledger rows. Current-suite tests and a renamed PR job are readiness
evidence, not replacements for that historical qualification evidence.

After owner-approved Q4 merge, verify a successful real check under the new
exact name on the merged main head. C4's qualified subset, exact check objects,
before/after readback and rollback packet may then be prepared separately.
Executing C4 and proving enforcement require the owner's separate approval.
The rename alone leaves JS Unit unprotected.

## Publication and verification record

S1 claimed workflow slot 1 in the shared locked claims file before publication.
Immediately before push, fetch/rebase current main and verify that no competing
workflow PR is open. Keep the slot through the owner-approved merge or an
explicit release; O1/G7 then S3/WS5 follow. Preserve all clones and refs under
Operation A.

Local evidence under `artifacts/s1-q4/`:

- `invariants.json`: all **24** YAML job definitions retained; parsed workflow
  differs only in the JS display name and coverage-summary heading.
  `vitest.config.js` and `scripts/release_gate.py` are byte-identical to main; the
  Python contract AST changes only the excluded exact name.
- `vitest-coverage.log`: **14 files / 269 tests passed**, exit 0. This is the
  current post-U1 corpus, not the historical 13-file qualification corpus.
- `vitest-seeded-failure.log`: one deliberately failing scratch test exits
  **1**. Its scratch config imports the production config and overrides only
  collection and report destinations, leaving the committed corpus untouched.
  This is local runner evidence. The unchanged direct coverage step has no
  `continue-on-error`; the later always-running summary cannot erase its failure.
- `tsc.log` / `tsc.exit`: zero errors, exit 0. `flake8.log` / `flake8.exit`:
  blocking selections report zero, exit 0.
- The first full pytest attempt was stopped after diagnosing environment
  failures: Windows resolved `bash` to the unconfigured WSL launcher. Targeted
  diagnostics also found the private runtime's absent `data` directory. The
  private launch script now selects installed Git Bash and creates that private
  directory; it changes no repository source. The aborted attempt and failing
  diagnostics are retained and receive no green-gate credit.
- `inventory-check.log`: inventory up to date, exit 0. `pyright.json` and
  `pyright-baseline-diff.log`: pyright 1.1.410 reports zero diagnostics and
  zero new diagnostics; both commands exit 0. No baseline was changed.
- The corrected full pytest was interrupted at implementation handoff; its
  retained `pytest-full-corrected-interrupted-handoff.log` is incomplete and
  receives no green-gate credit. The parent session owns the replacement full
  run and will record its completed result before marking a PR ready.
- The independent code review passed implementation `8485b5b4`. The independent
  test strategist found that the optional root-config comment edit broadened
  the required gate. That edit has been removed entirely, and this five-path
  gate derivation records the fix. The finding remains pending re-review;
  code delta review, publication readbacks and final-head CI are also pending.

### Completion receipt — 2026-10-22

This receipt updates the implementation-handoff states above. Final
documentation-head CI is reported in the public [#554 PR body](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/554).

- Corrected full Windows pytest: **5,811 passed / 2 skipped / 0 failures or
  errors**, exit 0, in 1,390.47 s; XML has **5,813 unique identities** and
  no duplicates. It ran `2026-10-21T21:48:40Z`–`22:11:50Z`, starting at
  `8485b5b4`. The config-comment restoration and Q4 prose update landed as
  `9a2f375f` during the run. All Python, tests, workflows and other tracked
  inputs match between those commits; both Vitest modules evaluate to deeply
  equal configurations. The receipt retains the actual start commit and this
  code-equivalence proof. This later receipt changes prose only.
- Inventory, **269 cases / 14 files** with JS coverage, TypeScript and blocking
  flake8 pass. Pyright **1.1.410** reports zero current and zero net-new
  diagnostics; its baseline is unchanged.
- Fresh reviewers with **no inherited implementation context** completed:
  `/root/q4_cold_code` passed `9a2f375f`; `/root/q4_cold_tests` derived the
  gate union independently, then closed its native failure-proof P2 after
  re-reading the source and raw receipts below. The earlier root-config
  finding is resolved by the config's exact restoration. Context-inheriting
  reviews remain diagnostic history; the two cold reviews satisfy S1's gate.
- Native proof:
  [run `39683330072`, attempt 1, job `119511059749`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39683330072/job/119511059749),
  rehearsal `dac825e79f2078ba2580895ff2755c6b43b61e28`, based on `9a2f375f`.
  Removing one runtime assertion-injection step makes its parsed JS job
  identical to the candidate. **269 original tests passed; the injected test
  alone failed.** The real coverage step failed with exit 1; the unchanged
  `always()` summary then succeeded, reporting absent coverage; the Actions
  job still concluded **failure**. The other 23 jobs were disabled/skipped
  and receive no execution credit. The retained rehearsal branch is outside
  the merge candidate and earns no qualification row.
- [Candidate CI `39682711569`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39682711569)
  passed **30/30 jobs** at `9a2f375f`, including the renamed JS check. The
  final prose-receipt head needs its own green CI before readiness.

Raw XML, interrupted/failed attempts, equivalence proofs, native logs and
cold review reports remain under `artifacts/s1-q4/`. Owner merge, successful
renamed merged-main evidence, workflow-slot release and later C4 preparation
and activation retain their separate boundaries.
