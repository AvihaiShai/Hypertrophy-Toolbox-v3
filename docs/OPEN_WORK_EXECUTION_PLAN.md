# Open Work Execution Plan

**Status:** Proposed sequencing plan — no implementation packet is authorized by this document alone  
**Prepared:** 2026-08-24  
**Revised:** 2026-08-24, after PR [#417](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/417)
merged as squash commit `5111a7f`. The amendments §11.9 previously *proposed* are now folded into
§4, §8 and §10; §11 is a dated evidence log and no longer carries a competing status layer.  
**Corrected:** 2026-08-24 later the same day, in a second pass on the same PR — the JS-unit
ledger reconciled to **six** rows after #417's own merge minted one (§11.10), §10 criterion 3's
misstatement of U2's gate repaired, and §11's blanket measurement timestamp replaced with
per-reading provenance (§11.11).  
**Reconciled:** 2026-08-27 against `origin/main` @ `f9726a3` — T0, U1, U2 and U3's KI-011
half have shipped, and Track D1's queue has emptied. §4, §8 and §10 record those landings;
§12 is the dated evidence log for this pass. **Nothing here authorizes a packet or a merge.**  
**Scope:** Open, unfinished, ongoing, parked, and misleadingly stale work recorded under `docs/`

## 1. Purpose

This document turns the repository-wide documentation review into an executable order of
work. It separates current defects and required evidence from historical findings, optional
roadmap features, and explicitly closed work.

This is a sequencing aid, not a replacement source of truth:

1. [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) owns the latest time-sensitive project state.
2. A dedicated workstream plan owns its detailed decisions and gates.
3. Current code and tests decide whether an old finding still exists.
4. [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md) remains the broad punch list.
5. `scan/`, superseded handoffs, and archived plans are evidence, not executable backlog.

Before starting any packet, re-read the relevant current-state block and verify the finding
against current code. A historical document mentioning a problem is not sufficient evidence
that the problem remains open.

## 2. Intended outcome

Proceed in this order:

1. Repair the documentation status layer so later work starts from trustworthy state.
2. Fix small, currently reachable user-facing defects.
3. Close or explicitly disposition the remaining testing and release evidence gaps.
4. Make one owner decision about the visual-determinism exemptions.
5. Continue pyright reduction as a bounded standing track.
6. Keep costly CSS and product-feature expansions outside the active queue unless the owner
   deliberately reopens them.

## 3. Status vocabulary

| Status | Meaning |
|---|---|
| **Execute** | Current evidence demonstrates a defect or required incomplete gate. |
| **Decision required** | Work must not begin until the owner selects the behavior or risk tradeoff. |
| **Observe** | Calendar or external-run evidence is required; little or no development is currently possible. |
| **Standing** | Valuable incremental work with no single closeout packet. |
| **Park** | Valid future work, but insufficient current benefit to fund. |
| **Closed** | Shipped or deliberately terminated; historical references do not reopen it. |

Estimates below are focused developer time, not elapsed calendar time. They include focused
tests and documentation updates but exclude waiting for scheduled CI runs or owner review.

## 4. Execution sequence

### Packet T0 — Documentation truth reconciliation

**Priority:** P0  
**Status:** **Closed** — shipped 2026-08-25 as squash commit `77f4adf`
([PR #420](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/420)). The work items and
acceptance criteria below are retained as the record of what the packet covered, not as an open
queue.  
**Sequenced after PR #417:** #417 rewrote [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) — the
document T0 reconciles [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md) *against* — so T0
could not run beside it without reconciling to a block that was about to move. #417 merged
2026-08-24 as `5111a7f`, so the dependency is discharged. Read the post-#414 block on `main`, not
the pre-#417 one.  
**Estimate:** 0.5–1.5 developer-days

**Work**

- Correct the stale WP4.4 `i–k` rows in [`REFACTOR_PLAN.md`](REFACTOR_PLAN.md) so they agree
  with the plan's own final status: WP4.4 closed at `k`.
- Re-derive rows 9, 10, and 13 of [`DUPLICATION_REGISTRY.md`](DUPLICATION_REGISTRY.md)
  against current code. Update pointers and split shipped portions from live residuals.
- Re-check [`CSS_OWNERSHIP_MAP.md`](CSS_OWNERSHIP_MAP.md) against current template link order,
  bundle ownership, and generated CSS. Change facts only where measurement proves drift.
- Mark historical scan recommendations clearly as evidence rather than an active work queue.
- Reconcile [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md) with the latest block in
  [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md); do not copy old findings forward without code
  verification.
- Repair the unmatched `**` recorded in §11.8 — `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`
  line 4371 (re-verified at `5111a7f`), inside a superseded ledger block #417 deliberately left
  standing. **Re-derive the count rather than carrying one forward, and record both the count and
  the strip method that produced it.** Scope the parity check to a paragraph, stripping fenced
  blocks — **including blockquoted ones** — then double-backtick spans, then single-backtick
  spans allowing newlines; a per-line check floods with false positives, and a weaker strip
  invents sites. Under that strict method §11.8 measures **one** genuine odd paragraph, at line
  4369. **Line 3517 is a checker artifact, not a repair target** — its only unbalanced `**` is
  the glob `` `e2e/**` `` sitting inside a single-backtick code span.

**Acceptance criteria**

- No current-status table says WP4.4 `i`, `j`, or `k` is active or not started.
- Duplication-registry rows 9, 10, and 13 cite current symbols and distinguish fixed work
  from remaining work.
- The CSS ownership map either matches current load topology or records measured corrections.
- Searching active planning documents does not present completed Track A/Track B work as open.
- Every unmatched `**` T0 re-derives renders closed — **at minimum** the line-4371 span §11.8
  names — and the superseded ledger blocks they sit in are otherwise unchanged. A count **and the
  strip method that produced it** are recorded, not assumed.
- Documentation-only checks required by [`ai_workflow/QUALITY_GATE.md`](ai_workflow/QUALITY_GATE.md)
  pass.

### Packet U1 — Volume calculation failure feedback

**Priority:** P1  
**Status:** **Closed** — Gate 0 `b4d6b13` ([#421](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/421))
and Gate 1 `1243728` ([#422](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/422)) both
signed; the fix shipped 2026-08-26 as `06a3f41`
([#423](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/423)). Both suppression sites
in the table below were addressed — neither alone would have sufficed.  
**Estimate:** 0.5–1 developer-day

**Problem — two independent suppression sites, both of which must be addressed**

`static/js/modules/volume-splitter.js` silences a failed `/api/calculate_volume` call **twice
over**, and each suppression is sufficient on its own. Re-verified against `5111a7f`:

| Site | Location | What it suppresses |
|---|---|---|
| 1 | `showErrorToast: false` in the request options — `volume-splitter.js:131` | The **shared** API error toast the wrapper would otherwise raise |
| 2 | A `.catch` whose only body is `console.error` — `volume-splitter.js:136–137` | The **rejection itself**, so no local handler runs either |

Removing the silent `.catch` alone leaves the shared toast still suppressed by the option;
flipping the option alone leaves the rejection swallowed by the catch. The highest-frequency
request on the page can therefore fail while stale results remain visible with no user feedback.

Both sites are instances of a pattern that repeats across this file — `showErrorToast: false`
appears at lines 131, 191, 251, 288, 372 and 828. U1's scope is the `/api/calculate_volume` path;
whether the neighbouring calls share the defect is a **measurement U1 must make and record**, not
an assumption it may act on.

**Work**

- Define the intended error state as a **behavioral contract** — visible toast, stale-results
  treatment, and retry behavior — and get it signed at U1's **own Gate 0** before implementing.
  This is a user-facing behavior change, so a plan-level mention is not a substitute.
- Address **both** suppression sites named above, and state in the plan which one each change
  targets.
- Use the existing shared API/toast conventions; do not rebuild transport infrastructure.
- Add a fixed-behavior Vitest or focused E2E regression that fails against **each** current
  suppression, so neither can silently return.
- Record the measured disposition of the five neighbouring `showErrorToast: false` sites: in
  scope, separately defective, or deliberate.

**Acceptance criteria**

- A failed calculation produces visible, accessible feedback.
- The UI does not imply stale results are newly calculated.
- Success behavior and slider interactions remain unchanged.
- The signed contract lives in U1's own planning artifact, and a regression fails if **either**
  suppression site is restored.

### Packet U2 — Backup “save first” confirmation continuity

**Priority:** P1  
**Status:** **Closed** — Gate 1 signed as `52c44c4`
([#424](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/424)); the fix shipped
2026-08-27 as `efa780c` ([#427](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/427)).
U2 took no Gate 0, as planned.  
**Estimate:** 0.5–1 developer-day

The defect, the mechanism, and the affected interaction are already stated concretely enough to
review a plan against, so U2 needs no separate requirements round: it enters its own Gate 1
directly. That readiness is U2's alone and is **not** transferable to U1 or U3.

**Problem**

During restore confirmation, “Save current plan first” refreshes the backup center. Detail
rendering calls `clearPendingAction()`, so the restore confirmation disappears instead of
letting the user continue the operation they initiated.

**Work**

- Preserve and restore the pending restore intent across the refresh, or avoid the destructive
  refresh side effect.
- Add a regression around the full save-first → continue-restore interaction.
- Keep the already-shipped erase-flow `showAutoBackupBanner()` behavior unchanged.

**Acceptance criteria**

- After a successful save-first action, the user can continue the same restore without
  restarting the flow.
- Changing selection or cancelling still clears the pending action.
- Backup create, restore, delete, and erase-flow tests remain green.

### Packet U3 — Toast contract defects KI-010 and KI-011

**Priority:** P1  
**Status:** **Split, as planned — one half closed, one half built and awaiting merge**  

| Defect | Gate 0 | Gate 1 | Implementation |
|---|---|---|---|
| **KI-011** action-button survival | — (carried with the fix) | — | **Closed** — `5b35966` ([#426](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/426)), 2026-08-27 |
| **KI-010** type-word collision | signed `db6c34b` ([#425](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/425)) | signed `a37d7e7` ([#428](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/428)) | **Open** — [PR #431](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/431), **draft**, based on `main`, 18/18 green, `MERGEABLE`/`CLEAN` |

**PR #431 being green is not authorization to merge it.** It is the last open engineering item
in this plan, and landing it needs its own explicit owner instruction naming the PR.  
**Estimate:** 1–2 developer-days total

Both defects change what a shared, repository-wide dispatcher emits, and KI-010 requires
**inverting a characterization test that currently pins the defective output**. Deliberately
reversing a pinned contract is exactly the case that must be signed before code moves, so the
replacement contract — for the type-word signature collision and for action-button survival —
is settled at U3's own Gate 0 and reviewed at U3's own Gate 1.

**KI-010 work**

- Remove the ambiguity between legacy and current `showToast` signatures when message text is
  `error`, `warning`, `success`, or `info`.
- Invert the characterization test that currently pins the defective output.
- Migrate collision-capable callers if changing the central dispatcher alone would create an
  ambiguous compatibility rule.

**KI-011 work**

- Keep a live toast action button from being destroyed when a later toast replaces the message.
- Add a fixed-behavior regression for the reachable volume-splitter history-refresh failure.
- Preserve the existing single-toast/last-message-wins behavior unless an explicit product
  decision changes it.

**Acceptance criteria**

- Type-word messages render as messages, not booleans or default success copy.
- A still-valid action remains operable after a later message update.
- Existing toast accessibility, styling, duration, and action coercion tests remain green.
- The inverted characterization test cites the signed contract that replaced the pinned defect,
  so a later reader can tell a deliberate inversion from a regression.

> **U1, U2 and U3 are gated individually, and they do not owe the same gates.** **U1: its own
> Gate 0 and Gate 1. U2: its own Gate 1 only. U3: its own Gate 0 and Gate 1, per defect.** There
> is no roadmap-level **Gate 0 or Gate 1** covering the three together, and this document does not
> create one. They share a theme, not a contract: U1 changes one page's error surface, U2 changes
> a confirmation flow's state handling, and U3 changes a shared dispatcher every page uses. A
> single approval spanning all three would put the widest blast radius through the narrowest
> review — and **U2's lighter requirement is U2's alone**, not a precedent U1 or U3 may borrow to
> skip Gate 0.

### Packet R0 — Refresh external release and testing evidence

**Priority:** P0  
**Status:** **Closed** — merged/completed 2026-08-24, PR
[#417](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/417), squash commit `5111a7f`
on `main`  
**Next external checkpoint:** the **2026-08-31 03:17 UTC** deep-gate cron. It is a **separate
inspection, not a continuation of R0** — the discipline is per-run, and R0 does not stay open to
absorb it.  
**Estimate:** 0.25–0.5 developer-day; calendar time depends on GitHub Actions *(spent)*

R0's acceptance criteria are satisfied **on `main`**, not merely inside a PR: the 2026-08-24
scheduled deep-gate run was inspected at job level (7/7 `success`, `visual-linux` **executed**,
not skipped), the JS-unit ledger gained row 5 without moving T0, and live branch protection was
re-read at 12 contexts. §11.1 holds the measured detail.

**The ledger has advanced past R0's reading, and that does not reopen R0.** #417's own merge
started a `main` `ci.yml` run that minted **row 6** — a run that had not happened when R0's
evidence was read, and that no R0 measurement could have included (§11.10). R0's criterion was to
refresh the ledger *through its inspection date*, which it did. **The qualification window is a
separate, continuing observation**, carried by R2 decision 3 and running to
`2026-09-05T17:59:26Z`; it will keep minting rows after every packet in this plan is finished, and
R0 does not stay open to absorb them.

**Work** *(completed)*

- Inspect the scheduled deep-gate run expected on 2026-08-24 at job level.
- Refresh the JS-unit qualification ledger without resetting its recorded T0. The current
  qualification window ends on 2026-09-05.
- Re-read live branch-protection contexts before proposing any promotion or release action.
- Update current-state documentation with observed evidence, including failures or skipped
  jobs; do not infer job success from the overall workflow result.

**Acceptance criteria**

- The scheduled run is recorded with run ID, commit, job-level results, and whether the relevant
  jobs actually executed.
- The JS-unit ledger reflects observed runs through the inspection date.
- Any next engineering packet is based on a demonstrated residual, not an anticipated one.

**Residual after R0.** Calendar items only — no engineering. Two of them: the **2026-08-31**
cron run, and the standing obligation to extend the JS-unit ledger after **every** `main` `ci.yml`
run until `2026-09-05T17:59:26Z`. Neither is an R0 deliverable: the first is inspected as its own
run, and the second belongs to the qualification window (R2 decision 3). **Nothing R0 measured
produced a new engineering packet.**

### Packet R1 — Deep-gate mutation probes

**Priority:** P1  
**Status:** Decision required; currently recorded as unmeasured and unauthorized  
**Estimate:** 1–2 developer-days

**Work after authorization**

- Prove independently whether a `needs:` shape can prevent a required deep-gate job from gating.
- Prove independently whether job-level `continue-on-error:` can create a false green.
- Add the narrowest contract protection justified by each mutation result.
- If a probe cannot demonstrate a false green, close that hypothesis rather than adding a
  speculative rule.

**Acceptance criteria**

- Each shape has a reproducible mutation result.
- Repository protection matches the demonstrated failure mode only.
- No existing required context is renamed or removed implicitly.

### Packet R2 — Remaining owner-gated testing decisions

**Priority:** P1  
**Status:** Decision required  
**Estimate:** 0.5–1 developer-day after decisions

**Decisions**

1. Define the intended `scan_export_bounds()` behavior when numeric `min > max`.
2. Decide and sign Testing Strategy D4.
3. After the qualification window, decide Q4/D2 and whether `JS Unit (Vitest,
   non-required)` should become a required context. Q4 and D2 are decided **together**; the
   window's strict mark is `2026-09-05T17:59:26Z`.
4. **R1-D3 follow-on — the clock question is settled; the action it feeds is not.** An owner
   ruling dated **2026-08-24** is recorded in **ADR-007** ([`DECISIONS.md`](DECISIONS.md)) and
   states: the **2026-08-17 scheduled run counts** toward the three, so **the clock stands at
   2 of 3**, and the third qualifying run is due **2026-08-31 03:17 UTC**. That ruling settles
   what was, until #417, an open question raised in three documents and answered in none.
   **Reaching three is not authorization to act.** Putting `visual-linux` into the release gate
   remains a fresh owner decision, and R2 carries that decision — not the counting.
   Measure the run count with `gh run list --workflow=deep-gate.yml --event=schedule`; never
   read a count out of the ADR.

The related `utils/rep_range_integrity.py` docstring correction must follow the behavior
decision; documentation must not choose runtime semantics on its own.

**Acceptance criteria**

- Each owner decision is recorded in the canonical decision location.
- Behavior, tests, and documentation agree for export-bound scanning.
- Any CI-context promotion follows the recorded naming/order decision and current live
  branch-protection state.
- The `visual-linux` release-gate question has a recorded outcome — adopted, declined, or
  explicitly deferred — that is distinct from the run-count observation that triggered it.

### Packet R3 — Release tag-trigger proof

**Priority:** P1 for an actual release; otherwise observe  
**Status:** Owner-controlled external action  
**Estimate:** 0.5 developer-day plus workflow runtime

The `push: tags` path is still recorded as never executed. A workflow dispatch proves the
workflow body but cannot prove the tag trigger itself.

**Guardrails**

- Do not create or push a real tag without explicit owner authorization naming the tag.
- Re-read [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) and live required contexts immediately
  before the action.
- Record the run and update the residual register whether the trigger succeeds or fails.
- Do not conflate this with publishing, signing, uploading release assets, or distributing a
  build; those remain separate decisions.

### Packet V1 — Visual determinism disposition

**Priority:** P1 decision; P2 engineering if reopened  
**Status:** Decision required  
**Estimate:** 2–4 hours to decide and reconcile docs; 2–5 developer-days to investigate and
repair the rendering race

**Current boundary**

- 81 of 86 captures are byte-compared.
- Five captures are deliberately exempt and replaced by contract-pinned semantic assertions.
- The exemptions are bounded, not missing by accident.
- The unresolved engineering question is whether the thumbnail rendering race can be removed
  cheaply enough to restore all five byte comparisons.

**Owner options**

1. **Accept 81/86 as the terminal contract.** Reconcile wording that still implies 86/86 byte
   comparison and keep the exact exemption set pinned.
2. **Fund a bounded investigation.** Time-box the race investigation to two developer-days,
   then either propose a measured repair or return to option 1. Do not regenerate baselines to
   hide nondeterminism.

**Acceptance criteria**

- Documentation states one unambiguous terminal policy.
- The exact exemption set and semantic replacements remain contract-protected.
- If engineering is funded, repeated pre/post runs demonstrate determinism before byte gates
  are restored.

### Track P1 — Continuous pyright reduction

**Priority:** P2  
**Status:** Standing — **in progress**; the first packet landed 2026-08-27 as `3098282`
([#430](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/430), `utils/filter_predicates.py`).  
**Baseline, re-measured from `docs/ci_cd_phase3/pyright-baseline.json` at `f9726a3`:**
**130 diagnostics / 41 distinct keys / 25 files**, all severity `error` — down from
**132 / 42 / 26** before #430. The earlier wording "132 diagnostics across
42 files" conflated the *key* count with the *file* count — each entry in the baseline's
`diagnostics` array carries its own `count`, so the array length is a key total, never a
diagnostic total and never a file total.  
**Estimate:** 8–16 developer-days, **re-derived against the corrected definition rather than
carried over unexamined.** The range was sized on a total of 132; #430 removed 2, so **7–15
developer-days remain** on the same rate assumption — but the work is far more concentrated than
"42 files" implied: four files hold **72 of 130** (`tests/test_volume_progress.py` 35,
`tests/test_strength_calibration.py` 16, `tests/test_program_backup.py` 12,
`routes/workout_plan.py` 9), and the top three are test
files, which may price differently from production modules. Expect the range's **lower** half if
the test-file clusters resolve as bulk annotation work, and treat `routes/workout_plan.py` as
excluded — prior packets record it as off-limits. Re-price after the first two packets measure a
real per-diagnostic rate; do not treat 8–16 days as validated by anything other than the total.  
**Per-packet size:** 0.5–1.5 days

**Rules**

- Select coherent modules, not arbitrary diagnostic counts.
- Keep packets type-only unless separately authorized behavior work is required.
- The diagnostic multiset must decrease; moving errors between files is not progress.
- Run focused tests for the touched module plus the pyright baseline-diff gate.
- Do not make total pyright closure a release blocker.
- Quote the multiset as **diagnostics / keys / files** whenever it is restated. The three numbers
  are not interchangeable, and collapsing them is what produced the wording this entry corrects.
- The 130 figure is the **baseline file's** total. Pyright has not been run live against it in
  this pass, and the gate blocks net-new diagnostics against exactly that file — so a large
  live/baseline gap would itself be a finding.
- **A count is not a delta.** #430 moved the total 132 → 130 and the keys 42 → 41; verify a
  packet's progress by comparing the key-by-key multiset, not the two totals.

### Track D1 — Dependency-PR triage

**Priority:** P2  
**Status:** Standing — ordinary triage, deliberately outside the numbered packet sequence.
**Queue empty at 2026-08-27:** #415 and #416 both merged 2026-08-26 (`7a64d2e`, `b733c14`), and
`gh pr list --state open` returns no dependency PR. The rules below stay live for the next one.  
**Estimate:** minutes per PR; escalates only when a bump lands on a gated path

Dependabot PRs had no home in this plan, and every status document asserted zero open PRs while
two were open. Re-measured **three times on 2026-08-24** — in the `17:03:00Z` evidence pass,
again at `21:36:40Z` after #417 merged, and again at `22:14:51Z` during this document's
correction pass:
**#415** (`pyinstaller` 6.22.0 → 6.22.2) and **#416** (`sass` 1.102.0 → 1.103.1) are **both
still open and unmerged**, both `MERGEABLE`/`CLEAN`, at the **latest** of those. The
`#415`/`#416` wording below is retained because the *last* measurement supports it; re-measure
again before reusing these numbers.

**Rules**

- Triage each dependency PR on its own; do not batch them into a packet.
- **`sass` sits on the CSS build path** and `pyinstaller` on the packaged-artifact path. Neither
  is automatically routine — the `stylelint` / `@playwright/test` ignore-rule precedent in
  [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md) records dependency bumps here that were
  not.
- Their CI runs execute on **PR branches**, so they never enter the JS-unit ledger. **If either
  merges, its post-merge `main` run mints the next sequential ledger row, and whoever lands it
  owes that row.** **Do not write a fixed row number into this rule.** The ledger stood at
  **six** rows at `2026-08-24T21:36:40Z` (§11.10) and at **23** rows at `2026-08-27` after #435;
  it advances on every merge to `main` — including this plan's own PR — so the row a given
  dependency PR receives depends on what merged before it. **#415 and #416 duly minted rows on
  their 2026-08-26 merges; that obligation is discharged, not outstanding.**
- Landing one is a merge decision like any other and needs the same explicit authorization.

## 5. Parked work — do not place in the active queue

| Area | If reopened | Current disposition |
|---|---:|---|
| CSS C8 — 235 declarations crossing the frozen `@layer workout` span | 5–10 days | Park. High cascade risk and no demonstrated user-facing defect. Requires a newly certified packet. |
| G4 — superset dark-tint gap | 1–3 days | Park unless a visible defect or explicit design requirement is supplied. |
| Fatigue Phase 3 | 8–15 days | Product roadmap, not incomplete v1 cleanup. Requires product scope and schema review. |
| User Profile per-exercise ratios | 3–5 days | v2 roadmap. |
| User Profile auto-refresh from logs | 3–5 days | v2 roadmap; needs conflict/source-of-truth rules. |
| Bodyweight-aware weighted lift estimates | 2–4 days | v2 roadmap; calculation semantics require product-risk review. |
| User Profile confidence indicator | 1–2 days | v2 roadmap; define the confidence contract before UI work. |
| Testing Strategy Phase 3 step 11 / Phase 5 proposals | Unknown | Do not execute until separately selected and planned. |

Parking means “not funded now,” not “safe to delete.” If the owner decides these will not be
built, update their source plans to **Not planned** so they stop appearing as ambiguous open
work.

## 6. Closed work — do not reopen from historical references

- Track A bug fixes, including CTE write-lock detection.
- Track B owner decisions, including weight-zero handling, validation bounds, export read-only
  behavior, null-routine aggregation, and the erase-flow backup banner.
- Refactor Phases -1 through 3 and WP4.4 `a–k`.
- The CSS P3 arc beyond `P3-a0`; it was deliberately terminated and retains no authorization.
- Body Composition implementation.
- Plan-volume integration.
- workout.cool integration; further curation is optional content work, not an incomplete
  integration.
- Bootstrap 5.3.8 and Node 24 AI-workflow ownership claims; both are released and no active
  claim remains.

If current code demonstrates a regression in one of these areas, open a new bug packet with new
evidence. Do not reactivate the old implementation plan.

## 7. Documentation retirement actions

- Preserve scan documents as historical evidence, with an explicit notice that they are not
  active backlog.
- Keep the superseded Fatigue Stage-4 handoff until its retention window permits archival;
  based on the recorded May 20 activity, the earliest archive review is 2026-11-20.
- Archive completed execution artifacts only under
  [`ai_workflow/DOC_RETENTION.md`](ai_workflow/DOC_RETENTION.md). Do not delete evidence merely
  to reduce the file count.
- Do not deprecate shipped Body Composition, plan-volume, workout.cool, or AI workflow behavior.
  Retire only stale planning surfaces around them.

## 8. Recommended order and total investment

**Status column measured 2026-08-27 against `origin/main` @ `f9726a3` and the live PR list.**

| Order | Packet | Status | Developer time | External/decision dependency | Gate |
|---:|---|---|---:|---|---|
| — | **R0 external evidence refresh** | **Complete** 2026-08-24 | *spent* | Merged as `5111a7f` ([#417](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/417)). Next external checkpoint: the **2026-08-31** cron, inspected as its own run | — |
| — | **T0 documentation truth reconciliation** | **Complete** 2026-08-25 | *spent* | Merged as `77f4adf` ([#420](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/420)) | Docs-only — passed |
| — | **U1 volume failure feedback** | **Complete** 2026-08-26 | *spent* | Gate 0 `b4d6b13` ([#421](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/421)), Gate 1 `1243728` ([#422](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/422)), fix `06a3f41` ([#423](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/423)) | Own Gate 0 + Gate 1 — both signed |
| — | **U2 backup confirmation continuity** | **Complete** 2026-08-27 | *spent* | Gate 1 `52c44c4` ([#424](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/424)), fix `efa780c` ([#427](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/427)) | Own Gate 1 — signed |
| — | **U3 · KI-011** action-button survival | **Complete** 2026-08-27 | *spent* | Fix `5b35966` ([#426](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/426)) | Signed per defect |
| 4 | **U3 · KI-010** type-word collision | **Ongoing** — built, unmerged | ≈0 days remaining | Both gates signed (`db6c34b` [#425](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/425); `a37d7e7` [#428](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/428)). [PR #431](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/431) is **draft**, based on `main`, 18/18 green, `MERGEABLE`/`CLEAN`. **Merging needs its own explicit authorization naming the PR** | Own Gate 0 + Gate 1 — both signed |
| 5 | R1 deep-gate mutation probes | **Not started** | 1–2 days | Owner authorization; both hypotheses still unmeasured | Own Gate 1 |
| 6 | R2 testing decisions | **Not started** | 0.5–1 day | Owner decisions; JS-unit window to `2026-09-05T17:59:26Z`; R1-D3 clock at **2 of 3** per ADR-007, third qualifying run due **2026-08-31** | Decision only |
| 7 | V1 visual disposition | **Not started** | 0.25 day or 2–5 days | Owner chooses acceptance or investigation | Decision, then own Gate 1 if funded |
| 8 | R3 tag-trigger proof | **Not started** | 0.5 day | Explicit authorization for a named real tag; `release.yml` `push` count still **0** | Owner action |
| standing | Track D1 dependency-PR triage | **Idle** — queue empty | minutes per PR | #415 and #416 both merged 2026-08-26; no dependency PR open at 2026-08-27 | Per-PR merge authorization |
| ongoing | Track P1 pyright packets | **Ongoing** | 7–15 days remaining | First packet landed `3098282` ([#430](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/430)); baseline 132 / 42 / 26 → **130 / 41 keys / 25 files** | Per-packet |

**Completed packets are retired from the numbered sequence rather than renumbered in place**, so
the surviving numbers keep matching §4 and an external reference to "order 5" is not silently
repointed. This is why the open rows start at **4** and no rows 1–3 remain: those numbers were
spent, not vacated. U3's two halves are split onto their own rows because they finished at
different times — the single "order 4" row that once covered both would now be half-true.

The original near-term commitment was **4–8 developer-days** for T0, U1–U3 and the authorized
portions of R1/R2. **T0, U1, U2 and KI-011 have been delivered and KI-010 is built**, so the
residual is **1.5–3 developer-days — R1 and R2 — and every hour of it is behind an owner
decision, not behind engineering capacity.** Visual race repair and the remaining pyright
burn-down are separate investments and should not be silently folded into that figure.

**Nothing in this table is an approval.** The Gate column records *which* gates each packet owes,
not that any has been passed — and the three `U` rows deliberately differ: **U1 and U3 owe Gate 0
and Gate 1; U2 owes Gate 1 only.** There is **no roadmap-level Gate 0 or Gate 1 covering U1–U3
jointly**.

## 9. Start checklist for every packet

- [ ] Confirm the item is still open in the latest `MASTER_HANDOVER.md` block, **read on `main`**
      — the block moved with #417 (`5111a7f`).
- [ ] Reproduce or re-measure it against current code.
- [ ] Check `ai_workflow/WORKSTREAM_OWNERSHIP.local.md` for path claims.
- [ ] Use an isolated worktree when the packet may touch the database, dev server, or tests.
- [ ] Route the change through `ai_workflow/QUALITY_GATE.md`.
- [ ] Keep unrelated dirty-worktree changes untouched.
- [ ] Update the owning plan, current handover, and generated inventories only when required.
- [ ] Pass the gates that packet **itself** owes, as recorded in §4 and §8 — **not every packet
      owes both**; U2 owes Gate 1 only. A gate satisfied by a sibling packet does not carry over.
- [ ] Record a closed, parked, or rejected outcome so the item does not remain ambiguously open.

## 10. Completion criteria for this execution plan

This plan is complete when:

1. ~~R0 refreshes the external release and testing evidence.~~ **Done 2026-08-24** — PR #417,
   squash `5111a7f`. The 2026-08-31 cron is the next checkpoint and is inspected as its own run,
   not as R0 reopening.
2. ~~T0 is merged and the active status layer no longer contradicts current code.~~
   **Done 2026-08-25** — PR #420, squash `77f4adf`.
3. U1, U2 and U3 are each fixed or explicitly rejected with rationale, **through the gates that
   packet actually owes** — which are not the same for all three, and §4 and §8 are the record.
   **Three of the four are met (2026-08-27): U1 `06a3f41` (#423), U2 `efa780c` (#427), U3's
   KI-011 `5b35966` (#426). U3's KI-010 has both gates signed and its implementation built in
   draft PR #431; the criterion is met when that lands.** The table below states what each
   packet *owes* and is unchanged by any of them having paid it:

   | Packet | Gates it owes | Why |
   |---|---|---|
   | **U1** | its **own Gate 0 and Gate 1** | the intended error state is a user-facing behavior change that must be signed as a contract before code moves |
   | **U2** | its **own Gate 1 only** | the defect, mechanism and affected interaction are already stated concretely enough to review a plan against, so it needs no separate requirements round (§4 Packet U2) |
   | **U3** | its **own Gate 0 and Gate 1, per defect** | KI-010 inverts a characterization test that pins the defective output, and both defects change a shared repository-wide dispatcher |

   **No joint approval satisfies any of them.** A gate passed by one packet does not carry to a
   sibling, and **there is no roadmap-level Gate 0 or Gate 1 spanning the three** — this document
   does not create one, and an approval that named "U1–U3" together would put U3's shared-dispatcher
   blast radius through the narrowest of the three reviews. **U2's readiness is U2's alone**; it is
   not evidence that U1 or U3 may skip Gate 0.
4. The deep-gate hypotheses, export-bounds behavior, JS-unit promotion, and release-tag proof each
   have a recorded result or explicit owner deferral.
5. **The R1-D3 clock question stays settled where it was settled, and the action it feeds is
   decided separately.** The 2026-08-24 owner ruling in **ADR-007** — the 2026-08-17 run counts,
   the clock is **2 of 3**, the third qualifying run is due **2026-08-31** — is the durable
   source; this plan cites it and does not restate it as an independent authority. **Reaching
   three does not authorize adding `visual-linux` to the release gate**; that remains a fresh
   owner decision carried by R2 (§4, decision 4), and this criterion is met only when that
   decision has its own recorded outcome.
6. **The JS-unit ledger's tally scope and its `Missing` definition agree.** As of #417 they do:
   `Missing` is scoped to *"a `main` **`ci.yml`** run with no `js-unit` job"*, and `main` runs of
   other workflows are **classified in a separate table rather than tallied**. Any future edit to
   either half must move both, because the two agreed for four rows only by the accident that
   every `main` run until 2026-08-24 was `ci.yml`.
7. Visual determinism has one accepted terminal policy.
8. Pyright has a continuing packet rule and a current baseline quoted as **diagnostics / keys /
   files**, even if diagnostics remain.
9. Every parked feature is clearly labeled as roadmap/not funded rather than unfinished current
   work.
10. Open dependency PRs are triaged or explicitly deferred under Track D1 rather than left
    unmentioned.

---

## 11. Evidence log — 2026-08-24 (Claude session; revised after Codex review, reconciled after #417 merged, corrected twice — `21:36Z`, `22:14Z` — then once editorially, no new reading)

**This section is a dated evidence log, not a status layer.** The amendments it once proposed
have been **applied** to §4, §8 and §10, which now describe R0 as merged and carry the ADR-007
R1-D3 ruling, the corrected pyright figures, the per-packet gating, and Track D1. Where §4/§8/§10
and this section could ever be read as disagreeing, **§4/§8/§10 govern** — and the durable
sources they cite (ADR-007, `STEP12_JS_UNIT_GATE0.md` §13.0, `pyright-baseline.json`) govern over
both.

**Provenance — five events on 2026-08-24, and provenance here is per claim, not per section.**
The first draft stamped the whole section `2026-08-24T17:03:00Z`. A first correction replaced that
with three readings, but still attributed the *range* **"§11.2–§11.7"** — explicitly including
*"ADR-007 **as merged**"* — to the 17:03Z read. **That was still chronologically impossible**: the
ruling was not committed until `19:02:37Z` and did not reach `main` until `20:50:48Z`. **A section
range cannot be a provenance unit**, because a single subsection mixes readings taken hours apart —
§11.3 holds both a 17:03Z run count and a 19:02Z ruling, and §11.4 holds two measurements four
hours apart. The table below is therefore keyed to **events**, and each row names the **claims**
that rest on it.

| # | When (UTC) | Event | The claims in §11 that rest on it |
|---:|---|---|---|
| **1** | **`17:03:00Z`** — API `Date` header | **R0's evidence pass.** The only reading taken before every event below | §11.1's deep-gate table — run `32688747703`, 7/7 `success`, `visual-linux` job `97318476983` executed — and its **five-row** ledger reading · §11.3's run counts (`schedule` = **2**, `workflow_dispatch` = **108**) · §11.7's V1 clean-compare datapoint and R3's `release.yml` event totals · §11.5's pyright figures, which are a **working-tree** read from the same pass and are **not** stamped by that API header |
| **2** | **`19:02:37Z`** — commit `da8b765` | **The ADR-007 R1-D3 ruling is written** — **two hours after** event 1, on a branch | §11.3's *"Resolved"*, the quoted ruling text, and every citation of ADR-007 as **signed** · the homing of the follow-on into §4 R2 decision 4 and §10 criterion 5 |
| **3** | **`20:50:48Z`** — #417 squash-merged as `5111a7f` | **The ruling and the post-#414 ledger reach `main`**, and the merge starts run [`32776201165`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32776201165) (`20:50:51Z → 21:00:32Z`; `js-unit` job `97587721956` green at `20:51:38Z`) | §11.1's merge facts and three-commit table · §11.2's *"the settled text is now on `main`"* · §11.7's and §11.8's *"re-verified at `5111a7f`"* readings, which **could not have been taken against a commit that did not yet exist** · the run that became **ledger row 6** |
| **4** | **`21:36:40Z`** — API `Date` header | **This PR's ledger and PR-state re-measurement** | §11.10's six-row ledger, re-derived from the API · §11.10's **PR-state table** for **#415**, **#416** and **#418**, which is also §11.4's **second** measurement |
| **5** | **`22:14:51Z`** — API `Date` header | **This second correction pass**, which repaired event 1's own over-broad attribution | §11.11's third defect · the re-check that #415, #416 and #418 are all still `OPEN`, `MERGEABLE`/`CLEAN` · `da8b765`'s commit timestamp, read from git rather than assumed |

**The commits this PR is made of sit between those events, and are not themselves measurements:**
`acfd558` at **`21:02:45Z`** (the reconciliation) and `c66b808` at **`21:49:54Z`** (the first
correction). §11.8's bold-parity measurement belongs to the second of those — **event 4's pass**,
not event 1's.

**Nothing measured at 17:03Z knew about the ruling, the merge, or row 6.** No figure attributed to
that read may be quoted as though it included later evidence — the ledger count above all, which
was **5** at that read and is **6** now. Where I repeat a figure another document asserts without
re-measuring it, I say so.

> **Revision note.** A Codex review of the first version of this section found **one factual
> error and two provenance defects**, all three correct. The pyright figures are fixed in
> §11.5, the decision-authority framing in §11.2 and §11.3, and the mutation-restore guidance
> in §11.6. Non-durable review chatter has been removed. **The error is worth keeping in view:
> I read a JSON array's length as a diagnostic total when each element carried its own `count`
> field — the same "two numbers that look interchangeable are not" failure this section warns
> about in §11.2.**

### 11.1 Packet R0 — merged; PR head and merge commit are different objects

[PR #417](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/417)
(`docs/post414-evidence-reconciliation`, base `origin/main` @ `31659a5`) was **18/18 green, zero
pending, `MERGEABLE`/`CLEAN`, zero reviews**, and was **squash-merged 2026-08-24T20:50:48Z** on
explicit owner authorization naming it. R0's acceptance criteria are now satisfied **on `main`**,
not merely inside a PR.

**Three distinct commits, and only one of them is on `main`:**

| SHA | What it is | Where it lives |
|---|---|---|
| `1460b1d` | The branch's **first** commit — the post-#414 reconciliation. **This is what the first draft of §11 was written against, which is why it named this SHA.** | Branch history only; **never** a `main` commit |
| `da8b765` | The branch's **head** at merge — adds the ADR-007 R1-D3 ruling, i.e. §11.3's own recommendation, enacted | Branch history only |
| **`5111a7f`** | **The squash-merge commit on `main`** — the only SHA that carries #417's content on the trunk | `main` |

Cite `5111a7f` for anything that must be true *of the repository*. Cite `da8b765` only when
identifying the head that CI actually verified — the 18 green checks ran against `da8b765`, and a
squash commit is a different object that no check ever saw. **`1460b1d` is stale in both senses
and should not be quoted anywhere.**

*(Squash-merge also makes the branch unreachable from `main`, so "is it merged?" cannot be
answered with `git branch --merged`; use `gh pr list --head` or the PR's `state`.)*

The scheduled deep-gate run R0 was waiting for fired and was green:

| | Measured |
|---|---|
| Run | [`32688747703`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32688747703) |
| Event / head | **`schedule`** / `31659a5` |
| Window | `04:05:58Z → 04:24:03Z`, attempt 1 |
| Delivery | **48 m 58 s** after its 03:17:00Z cron (2026-08-17 was 45 m 52 s) |
| Jobs | **7 / 7 `success`**, each read individually — never off the overall green |
| `visual-linux` | job **`97318476983`** — **executed, not skipped** |
| Step level | *Run visual specs* ✅ · *Assert compare mode wrote no baseline* ✅ · both upload steps `skipped` |

JS-unit ledger refreshed **without moving T0**: row 5 = job `97247194117` of run
`32661056527` (`push` / `31659a5`, PR #414, 18/18), `2026-08-23T19:23:22Z`. **T0 stays
`2026-08-22T17:59:26Z`; the strict mark stays `2026-09-05T17:59:26Z`** — matching this plan's
"window ends on 2026-09-05". Branch protection re-read live: **12** contexts,
`JS Unit (Vitest, non-required)` **absent**.

**That paragraph is R0's reading, and it is left as one.** It was measured at `17:03:00Z`, before
#417 merged, so **five rows is where R0's evidence stops** — correctly, and it is not rewritten
here to look as though it saw further. The current ledger is **six** rows; #417's own merge minted
row 6, and §11.10 records it against a fresh `21:36:40Z` read.

The next external-evidence checkpoint is the **2026-08-31** cron. It is a separate
inspection, not a continuation of R0 — the discipline is per-run.

### 11.2 Ledger semantics — settled, and the settled text is now on `main`

**This is no longer an open question.** PR #417 merged as `5111a7f` at **`20:50:48Z`**
(**event 3** — *after* the 17:03Z evidence pass, not part of it), so its wording is the
canonical ledger semantics: non-`ci.yml` `main` runs are recorded in a **separate non-attempt
classification table**, and the `Missing` row is rescoped to *"a `main` **`ci.yml`** run with no
`js-unit` job"* (still **0**). That change came from an explicit written owner instruction in the
session that commissioned #417 — non-`ci.yml` runs "must not be mislabeled as missing JS-unit
jobs" — and it now lives in
[`testing_phase3/STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md) §13.0, which
is the durable source. §10 criterion 6 pins it.

**The earlier draft of this section flagged a conflicting recollection. That flag is withdrawn.**
It rested on an agent-side session memory of a contrary ruling with **no user-visible decision
artifact** behind it. An undocumented agent recollection is not evidence and is not competing
authority — it cannot be weighed against a merged document, and presenting it as a live conflict
manufactured ambiguity where the repository had none. If the owner ever wants the other reading,
that is a fresh instruction against the now-canonical text, not a revival of this note.

*Why the rescope mattered beyond bookkeeping:* §13.0 had tallied *"`main` runs of **any** workflow"*
while defining `Missing` as *"a `main` run with no `js-unit` job"*. **Those two definitions
were never verified to mean the same thing.** They agreed through row 4
**only because every `main` run to date happened to be `ci.yml`**. 2026-08-24 is the first day
they diverge — three Dependabot `dynamic` update runs (`32676594582`, `32676594619`,
`32676594928`, path `dynamic/dependabot/dependabot-updates`, one `Dependabot` job each) plus
the deep gate. Under the un-rescoped wording they would have produced **four phantom
"missing" rows** in a window whose purpose is to prove there are none.

### 11.3 R1-D3's clock — resolved by a signed ADR-007 ruling, and now homed in R2

**Resolved.** The recommendation this section made — convert the unsourced interpretation into a
signed decision recorded where the question was posed — was **enacted** as commit `da8b765`,
committed **`2026-08-24T19:02:37Z`** (**event 2**), and reached `main` inside #417's squash at
**`20:50:48Z`** (**event 3**). **Neither had happened when this section's evidence was read at
`17:03:00Z`**, so no part of the ruling may be attributed to that pass. ADR-007 in
[`DECISIONS.md`](DECISIONS.md) now carries a **2026-08-24 owner ruling** that explicitly settles
the question it had held open since 2026-08-17:

> the **2026-08-17 run counts** toward the three · the clock **stands at 2 of 3** · the third
> qualifying run is due **2026-08-31 03:17 UTC** · **the R1-D3 decision itself is unchanged, and
> reaching three is still not authorization to act on it**

The ruling's own recorded rationale: the R1-D3 text excludes nothing, and the contamination that
prompted the question concerned the **pre-#388 file**, which has not existed on `main` since
2026-08-16.

**The homing defect is fixed too.** §4 R0 inspected the run but never mentioned the clock it
feeds, and §10 did not list it. Both now do — the follow-on decision is **R2 decision 4** (§4)
and **§10 criterion 5**.

**Measured at `17:03:00Z` (event 1), and never in dispute:** `gh run list --workflow=deep-gate.yml
--event=schedule` returns exactly **two** runs repo-wide, both `success` — `31993105305`
(2026-08-17) and `32688747703` (2026-08-24). REST `total_count`: `event=schedule` = **2**,
`event=workflow_dispatch` = **108**, none of the 108 qualifying. Measure the count with that
command; ADR-007 says the same, and neither that ADR nor this section is a place to read a count
from.

**The distinction the ruling preserves, restated because it is the part most easily lost:**
settling *how many runs have counted* is not settling *whether to act*. Putting `visual-linux`
into the release gate remains a fresh owner decision, carried by R2 as its fourth item. A session
that observes the third run on 2026-08-31 has completed an observation, not earned an
authorization.

### 11.4 Two open Dependabot PRs, and "zero open PRs" was stale everywhere

**Measured three times on 2026-08-24, and the wording rests on the latest:** first in the
`17:03:00Z` evidence pass (event 1), again at `21:36:40Z` after #417 merged — the reading
§11.10 tabulates (event 4) — and again at `22:14:51Z` (event 5). **#415** (`pyinstaller` 6.22.0
→ 6.22.2) and **#416** (`sass` 1.102.0 → 1.103.1) — both opened `2026-08-24T00:25Z` — are
**still `OPEN`, `MERGEABLE`/`CLEAN` and unmerged** at the latest of those. Merging #417 did not
close or affect either. **The PR-specific wording here is retained on the last measurement, not
the first**, which is the whole reason the count of measurements is recorded rather than the
wording simply being left alone.

Every status document had asserted **zero** open PRs; #417 corrected the live wording on `main`.

They were homeless in this plan and now are not: **Track D1** (§4) carries dependency-PR triage,
and §10 criterion 10 keeps it from being silently dropped. Two caveats survive into that track —
**`sass` sits on the CSS build path**, and the `stylelint` / `@playwright/test` ignore-rule
precedent in [`LEFTOVERS_BY_PRIORITY.md`](LEFTOVERS_BY_PRIORITY.md) shows dependency bumps here
are not always routine. Their CI runs execute on **PR branches**, so they never enter the JS-unit
ledger; if either merges, its post-merge `main` run mints **the next sequential ledger row**, and
**whoever lands it owes that row**. *(An earlier draft of this sentence named "row 6" as that
future row. It is no longer available: #417's own merge took it — see §11.10. Naming a fixed
future row is the error, not the particular number.)*

*Any later reader: re-run the measurement. These two numbers are the fastest-rotting facts in this
document.*

### 11.5 Track P1 — corrected pyright figures

**My first version of this section said "42 diagnostics across 26 files". That was wrong**,
and Codex's correction is accurate. Each element of the baseline's `diagnostics` array carries
its own **`count`** field; I read the array length as the total.

Re-measured from `docs/ci_cd_phase3/pyright-baseline.json`:

| Figure | Value |
|---|---:|
| Total diagnostics (Σ `count`) | **132** |
| Distinct diagnostic keys (array entries) | **42** |
| Distinct files | **26** |
| Severity | all `error` |

Heaviest files by diagnostic count: `tests/test_volume_progress.py` (**35**),
`tests/test_strength_calibration.py` (**16**), `tests/test_program_backup.py` (**12**),
`routes/workout_plan.py` (**9**).

**§4 Track P1 said "132 diagnostics across 42 files", which was also wrong** — 42 is the key
count, not the file count. **The correct wording is 132 diagnostics / 42 distinct keys / 26
files, and §4 Track P1 now carries it.** The 8–16 developer-day estimate was **reconsidered
against that definition rather than discarded, and retained**: the diagnostic total it was sized
on (132) is right, and the correction moves the *shape* of the work, not its volume — four files
hold **72 of 132**, and the top three are test files, which may price differently from
`routes/workout_plan.py` (recorded off-limits in prior packets). §4 now records that reasoning,
flags the range's lower half as the likelier outcome, and requires re-pricing after two packets
measure a real rate.

I did **not** run pyright live, so I am not claiming the live count equals the baseline. The
gate blocks net-new diagnostics against exactly this file, so a large live/baseline gap would
itself be a finding.

### 11.6 Remark on Packet R1's probe design

R1's two hypotheses are recorded verbatim in `release_pipeline/PLANNING.md` under #402
("Deliberately left open, and not established as defects"). R1 is faithful to that, including
the instruction to close a hypothesis rather than add a speculative rule. Two design notes:

- **`continue-on-error:` needs care as a probe target.** `dependency-health` already carries
  `continue-on-error: true` on **both** its scan steps by design — it reports rather than
  gates. A probe must distinguish *step-level* `continue-on-error` (existing, deliberate) from
  *job-level* (unmeasured, the actual hypothesis), or it will "discover" an intentional
  configuration.
- **Restore method.** Run each mutation in a **disposable isolated worktree** and revert with
  a **safe inverse patch**, then discard the worktree; do not rely on destructive restore
  commands in a shared checkout. Run every mutation in **both directions**, and **measure the
  "before" state rather than inferring it** — the two failure modes #399/#400/#402 paid for
  are a contract that passes **vacuously** and a new contract that is **strictly weaker than
  the sibling it imitates**.

### 11.7 Claims checked and confirmed

- **U1 is real, and its mechanism is now stated in §4 rather than only here.** It is not only a
  silent catch: [`static/js/modules/volume-splitter.js`](../static/js/modules/volume-splitter.js)
  passes **`showErrorToast: false`** in the request options (line 131) and *then* swallows the
  rejection in a `.catch` that only calls `console.error` (lines 136–137). **Both** must be
  addressed — removing the silent catch alone leaves the shared toast still suppressed by the
  option. §4 Packet U1 now carries both sites, the five neighbouring `showErrorToast: false`
  call sites, and the requirement that a regression exist for each suppression. *(§4 U1 states
  these line numbers as re-verified against `5111a7f` — that check belongs to **event 3 or later**,
  since `5111a7f` did not exist at `17:03:00Z`. The file itself is unchanged by #417, which touched
  no `static/js/**` path, so the reading holds either way; the **provenance**, not the number, is
  what the earlier attribution got wrong.)*
- **V1's "81 of 86" matches the repository's own record** (`visual_determinism/PLANNING.md:3`,
  `MASTER_HANDOVER.md:1289`). I did not independently re-count the captures.
- **A V1 datapoint, with its limit stated:** the 2026-08-24 `visual-linux` compare was clean
  and wrote no baseline, so the Linux corpus is in sync as of `31659a5`. **This is not evidence
  the gate can go red.** The corpus was in sync, so "no baseline written" shows nothing *was*
  written, not that real drift would have been caught — **a gate that has only ever passed is
  not yet a gate known to fail correctly**, and two green scheduled runs make that objection
  older rather than weaker. V1's acceptance criteria should not treat a clean compare as
  determinism evidence.
- **R3's premise is now measured, not merely recorded.** `release.yml` lifetime `total_count`
  by event: `push` = **0**, `workflow_dispatch` = **1**, `schedule` = **0**. The tag trigger
  has never fired, and the single dispatch is exactly the "proves the body, not the trigger"
  case R3 describes. R3's guardrails are correct as written.

### 11.8 One item for Packet T0 — folded into §4 T0

*(Now a **work item and acceptance criterion** under §4 Packet T0. The evidence is kept here.)*

**An unmatched `**` opens a bold span that never closes** —
`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md:4371` (`:4326` before #417 shifted the line;
**line 4371 re-verified on `main` at `5111a7f`**):
`` `2026-08-23T18:03:43Z`).** ``, inside a superseded ledger block. **#417 deliberately did
not touch it** — that block is "left standing as that record", and repairing it is a
separately-scoped edit; neither the post-#414 block nor the post-#417 block this PR adds
replicates the pattern.

**Re-measured on this PR's head during event 4's pass — not at `17:03:00Z` — and then
re-classified here under a stricter strip.** That re-classification is a **correction to the
computation, not a new reading of the repository**: the file's bytes are unchanged, and the same
strict check run against `5111a7f` returns the same answer.
A paragraph-scoped check over the whole file, run identically against `5111a7f` and against this
PR's head, reports the **same four** flagged paragraphs both times — **this PR introduces none**.
Under the strict strip only **one** of the four survives:

| Paragraph at line | Verdict | Why |
|---:|---|---|
| **1830** | **Checker artifact** | Balances once *multi-line* single-backtick spans are stripped; the flag came from a code span wrapping a line |
| **2931** | **Checker artifact** | Same cause |
| **3517** | **Checker artifact** | The 60-line numbered-list block's only unbalanced `**` sits inside a single-backtick code span — the glob `` `e2e/**` `` at line 3546. Stripping single-backtick spans takes the paragraph from **125** occurrences to **124**. **Not a repair target** |
| **4369** | **Real — the item §11.8 names** | Contains line 4371, `` `2026-08-23T18:03:43Z`).** `` |

**The strict paragraph-scoped check therefore leaves exactly one genuine odd paragraph in the
file: 4369, carrying the unmatched span at line 4371** — the site §11.8 has named from the start.
The earlier "two odd paragraphs, not one" reading is superseded; under a better strip the count
went **down**, not up.

Line numbers are stable between `5111a7f` and this PR's head because every line this PR adds to
that file falls **below** line 4430.

*Detection note, corrected by the above: a per-line `**` parity check floods with false positives
because bold spans legitimately wrap lines — but a paragraph-scoped check still false-positives if
it strips only line-scoped code spans — and it false-positives again if it misses **blockquoted**
fenced blocks, whose stray backticks mis-pair every code span after them. Strip fenced blocks
**including blockquoted ones**, then double-backtick spans, then single-backtick spans **allowing
newlines**, and only then count. Three of the four flags above came from getting those steps
wrong. 3517 is the instructive one: a glob written `` `e2e/**` `` is indistinguishable from an
unmatched bold opener to any checker that has not already stripped the code span around it.*

### 11.9 Amendments to §4, §8 and §10 — applied in `acfd558` (`2026-08-24T21:02:45Z`)

The proposal list this section carried has been **applied and removed**; what remains is the
audit trail of where each amendment landed, so a reader can check the normative sections against
what was actually asked for.

| # | Amendment | Where it landed |
|---:|---|---|
| 1 | R0 marked merged/completed; **2026-08-31** cron recorded as the next external checkpoint | §4 Packet R0 · §8 R0 row · §10 criterion 1 |
| 2 | R1-D3's clock homed as an owner decision, with "closing it is not authorization to act" stated explicitly | §4 R2 decision 4 · §10 criterion 5 |
| 3 | Ledger-semantics wording reconciled against the merged #417 documents and pinned as a completion criterion | §10 criterion 6 · §11.2 |
| 4 | Track P1 restated as **132 diagnostics / 42 distinct keys / 26 files**, estimate re-derived on that definition | §4 Track P1 · §10 criterion 8 |
| 5 | A home added for dependency-PR triage, after re-measuring #415/#416 | §4 **Track D1** · §8 standing row · §10 criterion 10 · §11.4 |
| — | Per-packet gating made explicit; joint approval of U1–U3 ruled out | §4 U1/U2/U3 · §8 Gate column · §9 · §10 criterion 3 |
| — | U1's problem restated to cover **both** suppression sites | §4 Packet U1 |
| — | T0's dependency on #417 recorded and discharged; §11.8's bold-span item folded in | §4 Packet T0 |

**Amendment 2 landed differently from how it was proposed, and the difference matters.** The
proposal said to record the clock as *"1 or 2 of 3 pending ruling"*. **That is no longer accurate
and must not be reintroduced**: the ruling exists. It was signed by the owner on 2026-08-24 and
written into **ADR-007**, which records the clock at **2 of 3** with the third qualifying run due
**2026-08-31**. §11.3 has the detail.

**Nothing in this document authorizes any packet.** This roadmap sequences work and records
gates; it does not approve implementation. T0 and U1–U3 each require their own authorization and
their own gates, and no packet below R0 has been started.

**Decision status, re-derived rather than carried forward:** **R1-D3's counting question is
signed** (ADR-007, 2026-08-24) while the `visual-linux` release-gate action it feeds is not.
**Q4, D2 and D4 remain unsigned.** Q6 was discharged by PR #413.

### 11.10 JS-unit ledger — #417's own merge minted row 6

**Re-derived from the GitHub API at `2026-08-24T21:36:40Z`** (response `Date` header), not
extended from any page. Method identical to the ledger's own standing rule: a superset query for
**every** `main` run created at or after `2026-08-22T17:00:00Z` — deliberately earlier than T0 —
followed by full `/jobs` enumeration on each, matched on the exact context string
`JS Unit (Vitest, non-required)`. All six rows, including the five R0 had already recorded, came
back byte-identical to the API.

| | Measured |
|---|---|
| Run | [`32776201165`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32776201165) — `CI/CD Pipeline` (`.github/workflows/ci.yml`) |
| Event / head | **`push`** / **`5111a7f`** — the squash commit of PR #417 |
| Window | `2026-08-24T20:50:51Z → 21:00:32Z` |
| Jobs | **18 / 18 `success`**, each read individually |
| `js-unit` job | **`97587721956`**, conclusion **`success`**, completed **`2026-08-24T20:51:38Z`** |
| Ledger position | **Row 6** |

| Ledger state at `2026-08-24T21:36:40Z` | Value |
|---|---:|
| Qualification attempts (`main` `ci.yml` runs at or after T0) | **6** |
| Green `js-unit` results | **6** |
| Red / missing / skipped / cancelled | **0 / 0 / 0 / 0** |
| `main` runs of any workflow (completeness check, **not** a tally) | **10** — the 6 above plus the same 4 non-attempt runs #417 classified |
| **T0** | **`2026-08-22T17:59:26Z`** — unmoved |
| **Strict 14-day mark** | **`2026-09-05T17:59:26Z`** — unmoved |
| Elapsed | **≈ 2 d 3 h 37 m** of **14 d** |

**PR state read in the same `21:36:40Z` pass**, from `gh pr view` rather than carried forward.
This is the table provenance event 4 names, and it is §11.4's **second** measurement of the two
Dependabot PRs:

| PR | Subject | State at `21:36:40Z` |
|---:|---|---|
| **#415** | `pyinstaller` 6.22.0 → 6.22.2 | `OPEN`, `MERGEABLE`/`CLEAN`, unmerged |
| **#416** | `sass` 1.102.0 → 1.103.1 | `OPEN`, `MERGEABLE`/`CLEAN`, unmerged |
| **#418** | this PR | `OPEN`, `MERGEABLE`/`CLEAN` |

All three were re-checked unchanged at `22:14:51Z` (event 5), and §11.4 rests its wording on that
later reading rather than on this one.

**Row 6 did not restart the window.** #417 touched six files, all under `docs/**`, and **zero**
under `static/js/**` — no workflow, no dependency, no generated inventory, no `vitest.config.js`.
The suite the window qualifies is still **13 files / 231 cases**, byte-identical across
`31659a5 → 5111a7f`, so Q2's restart clause did not engage.

The full job-level record lives in
[`testing_phase3/STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md) §13.0's
**post-#417 LIVE LEDGER** block, added by this PR. That document is the durable source; this
subsection cites it and does not compete with it.

**Why row 6 could not have been recorded before it existed — and what that obliges next.** A
ledger block is carried onto `main` by a merge, and that merge is what starts the run the *next*
row records. **No block can ever record its own merge's run.** #417's post-#414 block therefore
ended by owing row 6 to whoever landed it; that debt is discharged here. **The same debt is now
open against this PR.** Merging **#418** will start another `main` `ci.yml` qualification attempt
that **cannot be recorded before the merge**, and **whoever merges #418 owes its post-merge
`js-unit` result in the next ledger refresh.** #418 changes only `docs/**` files, so it cannot
restart the window — but that is a prediction about the restart clause, **not** about the run's
result, which must be measured after it exists rather than assumed green.

**This does not reopen R0.** R0's evidence packet is complete: it inspected the 2026-08-24 cron at
job level, refreshed the ledger through its own inspection date, and re-read branch protection.
The qualification window is a **different obligation** — a continuing observation carried by R2
decision 3, running to `2026-09-05T17:59:26Z`, which will take rows 7, 8 and beyond regardless of
what R0 did. Treating every new row as an R0 residual would make a closed packet permanently open.

### 11.11 Three defects in this document's own text, corrected here

The first two were in this PR's first version (`acfd558`) and were repaired by the first
correction (`c66b808`); that correction introduced the third, repaired by the second
(`1c8c5a6`). None of the three is still live.

- **§10 criterion 3 contradicted §4 and §8 on U2's gate.** §4 Packet U2 and §8's Gate column both
  say U2 enters its **own Gate 1** and needs no separate requirements round; criterion 3 said
  "U1–U3 … each through its own Gate 0 / Gate 1", which silently imposed a Gate 0 on U2 that no
  other statement in the document requires. Criterion 3 now states the three packet-specific
  requirements exactly — **U1: Gate 0 + Gate 1 · U2: Gate 1 only · U3: Gate 0 + Gate 1 per
  defect** — while still rejecting any joint roadmap-level approval, which was the clause worth
  keeping. §9's checklist carried the same "Gate 0 / Gate 1" shorthand and is corrected too.
  **A summary that tightens a requirement is as wrong as one that loosens it**; here it would have
  sent U2 back for a requirements round the document had already ruled unnecessary.
- **§11 carried a blanket measurement timestamp that its own contents falsified.** The preamble
  claimed every fact in the section was measured at `2026-08-24T17:03:00Z`, while §11.1 recorded a
  `20:50:48Z` merge and the run that followed it. The blanket line is replaced by the
  provenance table at the head of this section. **The 17:03Z read is still cited, and still owns
  exactly what it measured** — it is not backdated to cover later evidence, and §11.1's five-row
  ledger reading is deliberately left as the five-row reading it was.
- **The first repair of that timestamp was itself still wrong, and this is the third defect.** It
  replaced the blanket line with three readings but kept a **section-range** attribution, handing
  the 17:03Z read *"§11.2–§11.7 … ADR-007 **as merged**"*. The ruling was committed at
  `19:02:37Z` and merged at `20:50:48Z`; §11.4 already carried a `21:36:40Z` re-measurement. **A
  range that spans subsections cannot carry one timestamp** when a single subsection mixes
  readings hours apart — §11.3 holds a 17:03Z run count beside a 19:02Z ruling. Provenance is now
  keyed to **five dated events** and to the **specific claims** resting on each, and §§11.2, 11.3,
  11.4, 11.7, 11.8 and 11.9 carry inline stamps naming which event they belong to. **Correcting a
  provenance defect with a narrower but still-wrong attribution is the failure worth remembering:
  the fix has to be checked against the same clock the defect was.**

---

## 12. Evidence log — 2026-08-27 status reconciliation

**This section does not amend §§1–10 beyond the status fields §4, §8 and §10 now carry.** It
records what was measured to justify those fields, so a later reader can re-check them instead
of inheriting them. **§11 is left exactly as it stood** — it is the 2026-08-24 reading and
owns only what it measured on that date. Nothing here authorizes a packet or a merge.

### 12.1 Provenance

| Reading | Source | What rests on it |
|---|---|---|
| `origin/main` @ **`f9726a3`** | `git fetch origin main` then `git log` | Every landed-commit claim in §4 and §8 |
| Merged-PR list, 2026-08-27 | `gh pr list --state merged --limit 20` | The PR↔commit pairings below |
| Open-PR list, 2026-08-27 | `gh pr list --state open` | "#431 is the only open PR"; Track D1's empty queue |
| PR #431 detail, 2026-08-27 | `gh pr view 431 --json ...statusCheckRollup` | Draft / base / 18 × `SUCCESS` / `MERGEABLE` / `CLEAN` |
| `docs/ci_cd_phase3/pyright-baseline.json` @ `f9726a3` | Σ of each entry's `count` | **130 / 41 / 25** |

### 12.2 What shipped since §11's 2026-08-24 reading

| Packet | Squash / merge commit | PR | Merged |
|---|---|---|---|
| T0 documentation truth reconciliation | `77f4adf` | [#420](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/420) | 2026-08-25 |
| U1 Gate 0 | `b4d6b13` | [#421](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/421) | 2026-08-25 |
| U1 Gate 1 | `1243728` | [#422](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/422) | 2026-08-26 |
| U1 implementation | `06a3f41` | [#423](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/423) | 2026-08-26 |
| U2 Gate 1 | `52c44c4` | [#424](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/424) | 2026-08-26 |
| U3 · KI-010 Gate 0 | `db6c34b` | [#425](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/425) | 2026-08-26 |
| U3 · KI-011 implementation | `5b35966` | [#426](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/426) | 2026-08-27 |
| U2 implementation | `efa780c` | [#427](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/427) | 2026-08-27 |
| U3 · KI-010 Gate 1 | `a37d7e7` | [#428](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/428) | 2026-08-27 |
| Track P1 packet 1 (`utils/filter_predicates.py`) | `3098282` | [#430](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/430) | 2026-08-27 |
| Track D1 — `pyinstaller` 6.22.0 → 6.22.2 | `7a64d2e` | [#415](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/415) | 2026-08-26 |
| Track D1 — `sass` 1.102.0 → 1.103.1 | `b733c14` | [#416](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/416) | 2026-08-26 |

JS-unit ledger rows minted by those merges landed in #429 (`ec1a5cb`), #432 (`1211915`),
#433 (`07781a8`) and #435 (`f9726a3`); the ledger stands at **23 rows** and **T0 has not
moved** — it is still `2026-08-22T17:59:26Z`, strict mark `2026-09-05T17:59:26Z`.

### 12.3 The one open engineering item

[PR #431](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/431) (KI-010) is **the only open PR in the repository**. It is a **draft**,
based on `main`, `MERGEABLE`/`CLEAN`, with **18 of 18 checks `SUCCESS`**. Both of its gates are
signed and on `main`.

**Green CI is not the go-ahead, and neither is this document.** §4's U3 block and §8's order-4
row both record the same constraint: merging #431 needs an explicit owner instruction naming
the PR. A status reconciliation that made a built change look pre-approved would be exactly the
drift §1 warns against.

### 12.4 Track P1 — the baseline moved, and a count is not a delta

| Figure | Before #430 | At `f9726a3` |
|---|---:|---:|
| Total diagnostics (Σ `count`) | 132 | **130** |
| Distinct keys (array entries) | 42 | **41** |
| Distinct files | 26 | **25** |

The concentration §4 records is unchanged in absolute terms and slightly higher in relative
terms: the same four files hold **72** diagnostics, now of **130** rather than 132.
`routes/workout_plan.py` (9) remains recorded as off-limits, so **63 of the top-four total is
actually addressable**, all of it in test files.

**Do not read the 132 → 130 move as "#430 fixed two diagnostics" without checking the multiset.**
A packet can remove diagnostics in one file and add them in another for a net figure that
flatters it; §4's rule already requires the multiset to decrease, and the totals alone cannot
demonstrate that.

### 12.5 What did *not* change, and is still owed

- **R1** — both mutation hypotheses remain unmeasured and unauthorized. §11.6's probe-design
  caveats still stand and were not revisited in this pass.
- **R2** — D4 unsigned; Q4/D2 unsigned, and their window closes `2026-09-05T17:59:26Z`;
  `scan_export_bounds()`'s `min > max` behavior undecided. **R1-D3's clock is settled at 2 of 3
  in ADR-007 and is not one of these** — but reaching three still authorizes nothing, which is
  R2's fourth decision.
- **V1** — no terminal policy chosen; 81/86 stands unreconciled. §11.7's caution holds and has
  aged rather than weakened: **a gate that has only ever passed is not yet a gate known to fail
  correctly**, and the 2026-08-24 clean compare added a third green run, not evidence.
- **R3** — `release.yml`'s `push` trigger count was **0** at §11.7's reading and no tag has been
  pushed since. **This pass did not re-measure it**; treat it as carried forward, not confirmed.
- **The 2026-08-31 cron** is the next external checkpoint, inspected as its own run.
