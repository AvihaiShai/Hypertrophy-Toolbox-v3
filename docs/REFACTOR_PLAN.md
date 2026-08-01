# Deep Refactor Plan — v3 (2026-07-04, full-scan grounded)

**Status update (2026-08-01, supersedes every status line below):** **WP4.4 is
COMPLETE and the arc is closed.** `i` merged as `5f7b5ac` (PR #212) with an
in-scope oracle corrective at `666471e` (PR #215); `j` merged as `47c7687`
(PR #216); `k` is the closeout. The arc removed **539 net lines** from the seven
shared bundles with **0 observable change** — an arc-base-to-arc-end computed
differential over **2,275,668 values** in both themes reports zero. Stylelint
**2,883 → 2,751 (−132)** measured from the arc base; `!important` −48. Report:
[`CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md`](CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md).

The §WP4.4 end-state below says `theme-dark.css` is reduced to justified remaps
*"or is removed after proof"*. **The removal half was explicitly out of reach for
this arc (R4)** and remains so: `templates/base.html` is frozen and the file is
still linked. `j` reduced it 621 → 574 lines. The 235 Packet-a-span declarations
remain deferred (C8), as does the superset dark-tint gap (G4).

See [`N4_CONTINUATION_AUTHORITY.md`](css_phase4_wp4_4/N4_CONTINUATION_AUTHORITY.md)
and [`EXECUTION_HANDOFF_I_K.md`](css_phase4_wp4_4/EXECUTION_HANDOFF_I_K.md) for
the tail's authority and restart ledger.

**Status (2026-07-30, superseded by the update above): Track A, Phases -1 through 3, and Phase-4 packets
WP4.-1, WP4.0a, WP4.0, WP4.1, WP4.2, and WP4.3a–WP4.3h are complete, as is the
WP4.3i Workout Plan dead-CSS arc through WP4.3i-filter-btn. WP4.3j-a is merged,
WP4.3j-b is complete as an audit-only no-op, WP4.3j-b-dead has shipped the
deletion it nominated, WP4.3j-c-dead has shipped the c-audit deletion, and
WP4.3j-d-hover-paint is complete in PR #186. WP4.4 is complete through
WP4.4-f2 (PR #205, squash `6a5465c`); WP4.4-g is next.** WP2.2 is committed
as `c461840`; optional WP3.6 is committed as `0cbedac`. WP4.0 measurement
provenance remains unchanged head `e46b67e`, with its ledger committed as
`ca725c2`. Local integration verification through WP4.3d is complete
(history-preserving merge `40bc09f`); nothing was pushed through WP4.3d.
WP4.3e (Welcome) shipped to `origin/main` via PR #160 (`5e7d290`), WP4.3f
(Session Summary) via PR #161 (`08256f0`), WP4.3g (Weekly Summary) via PR #162
(`bc9da14`), WP4.3h (User Profile) plus WP4.3i-i/i-b…i-g via PR up to
`00eb6f9`, WP4.3i-h via PR #164 (`bfadf9d`), and WP4.3i-dead plus
WP4.3i-filter-btn via **PR #165 (merge commit `95f30c1`, 2026-07-25)**. Track B
is mostly shipped; WPB.4 remains unimplemented and product-risk gated.

**Phase-4 frontier — WP4.3i Workout Plan dead-CSS sweep, fully shipped.** Three
packets sit past `00eb6f9`; **all three are on `origin/main`**:

| Packet | Commit | State | Headline |
|---|---|---|---|
| WP4.3i-h | `bfadf9d` | **on `origin/main`** (PR #164, squash) | 18 dead `[data-bs-theme]`/`.dark-mode` rules deleted, −113 lines, pure deletion; pytest **1,751 / 0** |
| WP4.3i-dead | `db23801` | **on `origin/main`** (PR #165; cherry-pick of `93a3134`) | 14 overridden **rest-state** declarations deleted, −33 lines, `!important` 520 → 513; contracts **26/26**, pytest **1,752 / 0**, focused Stylelint **1,221 → 1,204** |
| WP4.3i-filter-btn | `cb5ff6e` | **on `origin/main`** (PR #165; authored on `wt/css-wp4-3i-filter-btn`) | 5 rules gated on the non-existent `#filter-btn` deleted — 48 lines / 27 decls / 25 `!important` / 37 literals; contracts **27/27**, Workout Plan Chromium **56 passed**, pytest **1,753 / 0**, focused Stylelint **1,204 → 1,138 (−66)**, first packet to move `selector-max-id` and `selector-max-specificity` (−10 each) |

**PR #165 was merged 2026-07-25 as merge commit `95f30c1`**, with the closeout
docs commit `0cd44eb`. A true merge commit was used rather than a squash, so
`db23801` and `cb5ff6e` remain individually reachable from `main` and the ladder
above stays valid. The PR landed green — **14/14 checks**, `mergeStateStatus`
CLEAN, 0 required approving reviews — over a six-file diff whose CSS change was
0 insertions / 81 deletions. **Local `main` == `origin/main` == `95f30c1`.**
Evidence: [`CSS_PHASE4_WP4_3I_DEAD_EVIDENCE.md`](CSS_PHASE4_WP4_3I_DEAD_EVIDENCE.md)
and [`CSS_PHASE4_WP4_3I_FILTER_BTN_EVIDENCE.md`](CSS_PHASE4_WP4_3I_FILTER_BTN_EVIDENCE.md).
No visual baseline was updated in any packet, and no Bootstrap output, SCSS, or
database file appears in any diff.

**Known animated-logo visual red — not a fixed pixel count.** `workout-plan
desktop dark` remains the WP4.0 animated-navbar-logo red. It failed at **1,039 px
first attempt and 1,046 px on retry within the same i-filter-btn run**; i-h and
i-dead happened to land on 1,039 twice. Red pixels appear only on the animated
navbar logo. Treat it as drift in a band, not an invariant, and do not gate on
the exact number. The other five variants are byte-identical.

**Method rule established by WP4.3i-dead:** a browser sentinel sweep alone
**over-reports deadness**. Its 24-declaration verdict reduced to 14 once a stable
oracle was demanded, because a same-CSS control run over forced interaction
states produced 52 differing records — those states animate. Every future
dead-CSS packet on this page must pair the sweep with a rest-state differential
**and** a same-CSS control.

**Next-state constraints. Items 1–4 are owner-gated and not started; item 5
records the WP4.4 authorization granted at Gate 1:**

1. **Do not remove the 10 deferred interaction-state declarations** from
   WP4.3i-dead. They require animation stabilization plus a same-CSS control
   reaching **zero** differing records; the i-dead contract asserts they are
   still present.
2. **Do not modify the WP4.3i-c Page Header contract.** Section 829 is 15/15
   live and locked.
3. **Do not tokenize the remaining white literals** merely to remove literals —
   the i-o investigation found only **two** live, semantically equivalent
   consumers.
4. The remaining Workout Plan **raw-literal → token extraction and `!important`
   weighting review** is redesign-sized, multi-packet, and **has not started**.
5. **WP4.3j (Workout Log) is complete through WP4.3j-d-hover-paint and pauses
   there**; **WP4.4 (shared bundles / navbar / `theme-dark.css`) Plan v2 is
   Gate-1 approved (owner, 2026-07-27) and executes from
   [`docs/css_phase4_wp4_4/PLANNING.md`](css_phase4_wp4_4/PLANNING.md)** —
   authorized order `a` ✔ → `c` ✔ → `b` ✔ → `e` ✔ → `d1` ✔ → `f1` ✔ → `d2` ✔ → `f2` ✔ →
   `g` → `h`, run **sequentially** per owner direction of 2026-07-29, then a
   **hard stop before `i`** for the N4 owner checkpoint. WP4.3j-a merged
   through
   PR #181 at `99dfee1`; it removed the five overpainted dark-mode
   `background-color` declarations on columns 1–4 and 15–17 — evidence:
   [`CSS_PHASE4_WP4_3J_A_EVIDENCE.md`](CSS_PHASE4_WP4_3J_A_EVIDENCE.md).
   **Method addition from that packet: for declarations suppressed by overpaint
   rather than by the cascade, the differential must be taken in pixel space.** A
   computed-declaration-owner audit certifies them live — correctly, by its own
   question — while zero pixels change. WP4.3j-b then audited the apparent
   duplicate `@media` ladders and closed as a **zero-CSS-change no-op**: they
   target different selector/property families, while the measured table
   padding/type declarations lose to the shared important `components.css`
   table-cell owner and the measured frame-padding declarations lose to
   `html body .workout-log-frame { padding: 0 !important; }`. Fourteen
   breakpoint probes were invariant. The `992px` overflow rule, the first
   ladder's page/button/routine families, and the separate legend query were not
   measured and are not classified as dead. Evidence:
   [`CSS_PHASE4_WP4_3J_B_EVIDENCE.md`](CSS_PHASE4_WP4_3J_B_EVIDENCE.md).
   **WP4.3j-b-dead then SHIPPED the deletion packet j-b had only nominated.** It
   removed the eight-query `RESPONSIVE FRAME ADJUSTMENTS` block, the first
   ladder's `thead th` / `td` padding and type blocks, and the base
   `.workout-log-frame` `padding: var(--frame-padding, 1.25rem)` declaration:
   lines **2,180 → 2,025**, `@media` **17 → 9**. Every j-b claim was re-proven on
   a branch cut fresh from merged `main` — **385 declaration-instances across 14
   widths, 0 ever a winning owner**; before vs after **0 differing records / 504**
   and **14/14 zero-diff** frame pixels; invariants measured identical
   (`12px 16px`, `14.08px`, `0px`). Gates: visuals **6/6** update-free, contracts
   **31/31** (red path proven), functional Chromium **33/33**, pytest **1,857 / 1
   skipped**. Stylelint moved by **zero** and is reported as zero. Evidence:
   [`CSS_PHASE4_WP4_3J_B_DEAD_EVIDENCE.md`](CSS_PHASE4_WP4_3J_B_DEAD_EVIDENCE.md).
   **Two oracle rules added by this packet:** the full-page pixel oracle is
   unusable on this route (same-CSS control drifts at 10/14 widths inside the
   animated navbar strip `y ∈ [18,40]` — scope pixel claims to the element under
   test), and a specificity model that mishandles `:is()` or splits selectors on a
   naive comma will report an owner contradicting the computed value.
   **WP4.3j-c is now COMPLETE as an evidence-only audit** of the overlapping
   header and table-cell glass systems — no production file changed. It found
   that **the Workout Log table is painted by the shared `components.css`
   `.table.table-calm` system, not by the page's own glass systems**: of **322**
   declarations audited across regions A–I, **227 never win anywhere**, 31 are
   live, 55 mixed, 9 unverified, and **0 are winning-but-overpainted**. Regions
   **D (dark cell), E (metric-lane `nth-child` glass) and F (dark-mode
   visibility)** are dead in their entirety. The cause is the ID-bearing `:is()`
   arm exporting `(1,3,1)`/`(1,3,2)` specificity; every page-local rule in A–G is
   ID-free and unreachable regardless of `!important`. The only page-local family
   that renders is region H, the only one written with an ID at `(1,5,2)`.
   Per-column ownership collapses to two groups (1–4/15–17 vs the 5–14 metric
   lanes) with **no column deviating from its group**. Audit gates: pixel control
   **0 diff 6/6**, resolution self-check **9,358 / 0 mismatches**, sentinels
   **222/222 effective**, **15,336** records. Evidence:
   [`CSS_PHASE4_WP4_3J_C_AUDIT_EVIDENCE.md`](CSS_PHASE4_WP4_3J_C_AUDIT_EVIDENCE.md).
   It **corrects** the j-a claim that the dark `#e0e0e0` colours are live
   winners — they are cascade-dead, beaten by `components.css` at `(1,4,2)`.
   The documented deletion candidate later shipped as **WP4.3j-c-dead**: 37
   rules / 69 declarations, lines **2,025 → 1,621**, `!important` **285 → 217**.
   **WP4.3j-d-hover-paint** then removed the four cascade-dead light/dark
   `background` and `box-shadow` declarations from the two retained Region G
   hover rules while preserving their full selectors and live filters. Its
   real-hover differential is **0 computed / 0 owner differences across 11,016
   records and 6/6 byte-identical frames**; 408 records lost candidates and 0
   gained any. Gates: contracts **33/33**, focused Chromium **33/33**, pytest
   **1,859 / 1 skipped**. Stylelint total **5,498 → 5,490**, focused **431 →
   423**, no category increased. Evidence:
   [`CSS_PHASE4_WP4_3J_D_HOVER_PAINT_EVIDENCE.md`](CSS_PHASE4_WP4_3J_D_HOVER_PAINT_EVIDENCE.md).
   **Method rule added by the c audit: a probe
   that changes nothing proves nothing** — four oracle defects each produced a
   confident false deadness verdict (`var()`-bearing shorthands invisible to
   longhand CSSOM queries, an injected sentinel losing the cascade, a running
   transition outranking important author declarations, and `page.screenshot`
   not painting clip regions beyond the viewport).
   The shared ID-bearing `:is()` specificity finding still belongs to WP4.4 and
   is recorded, not acted on. The sequencing constraint is discharged for the
   deleted D–G families; regions A–C remain and must be re-measured if WP4.4
   changes the shared selector.
6. Deferred and unacted: the superset dark-tint gap (`--superset-bg-1..4` has no
   live dark override) and the dead `body.dark-mode` in
   `static/css/layout.css:1120` (→ WP4.4).
7. **WP4.3i-jm and WP4.3i-o were attempted and deliberately not committed** —
   do not re-dispatch them. See `docs/MASTER_HANDOVER.md` for why.

This supersedes v2. It incorporates:

- the v1 council review;
- the complete line-by-line scan on `scan/codebase-grounding` at `a6574b9`;
- `docs/SCAN_PROGRESS.md`, `docs/SCAN_FINDINGS.md`,
  `docs/SCAN_RECOMMENDATIONS.md`, and `docs/scan/PHASE_02.md` through
  `PHASE_22.md` from that scan worktree;
- a second review of high-risk scan claims against `main` at `b5e837d`.

The scan artifacts are merged into this checkout (WP-1.0, 2026-07-04):
`docs/SCAN_FINDINGS.md`, `docs/SCAN_RECOMMENDATIONS.md`, `docs/SCAN_PROGRESS.md`,
and `docs/scan/PHASE_02.md`–`PHASE_22.md`.

The scan's headline is right: the architectural direction survived, but the sizing and
sequencing did not. Python work needs broader schema/route scope, the proposed JS seams
miss real feature clusters and shared state, and CSS cleanup needs cascade and test-harness
prerequisites. The scan also found real bugs. Those belong in a separate behavior-changing
track and must never be smuggled into move-only refactor PRs.

---

## 1. Review disposition

### Accepted scan findings

- Startup and erase repeat the full initializer chain, and the chain has six
  `add_*` functions plus the base initializer, exercise-order migration, and backup
  tables—not the smaller inventory in v2.
- Filter-value behavior is spread across four implementations and two hand-maintained
  allowlists.
- Three additional route modules perform direct DB/domain work:
  `routes/workout_log.py`, `routes/body_composition.py`, and
  `routes/volume_splitter.py`; `routes/exports.py` is also a genuine fat route.
- `profile_estimator.py` has six natural clusters, not the three proposed in v2.
- `workout-plan.js` has roughly 660 lines with no destination in v2 and four mutable
  state variables crossing the guessed boundaries.
- `volume-splitter.js` contains a local `apiFetch` reimplementation that should be
  deleted once its JSON calls use the shared wrapper.
- CSS contains an undeclared `@layer` ordering trap, duplicate token vocabularies,
  six local token namespaces, a four-copy summary/frame block, and misfiled page CSS.
- Phase -1 closed the identified safety-net gaps: catalog tests are hermetic, the named
  vacuous E2E assertions now observe real outcomes, startup backup copying has direct
  tests, and fatigue-context E2E is a required branch-protection context.

### Accepted with stricter safeguards

- `utils.errors.not_found` and `handle_unexpected_error` appear shadowed by later
  registrations in `app.py`; delete only after an isolated runtime registration probe
  proves handler selection for HTML, XHR, 404, HTTPException, and generic Exception.
- `weekly_summary.STATUS_MAP`, `MovementCategory`, `HOME_BASIC_EQUIPMENT`, and the other
  definition-only constants remain safe Phase-0 candidates after a fresh repository-wide
  reference check.
- `scripts/seed_visual_baseline.py` may be archived, but the move must also disposition
  its documentation references and pyright-baseline entry. It is not literally
  reference-free across the repository.
- JavaScript dead code requires import/call-graph and runtime-wiring checks. A symbol
  assigned to `window` is not live merely because grep finds the assignment.

### Not accepted as behavior-preserving deletion

- The second `effective_sets.py` pipeline is production-unreferenced but exported,
  documented, and covered by 26 tests. Removing it changes a callable contract.
- The five HTTP endpoints with no product-frontend callers are pytest/E2E-pinned API
  surfaces. “No frontend caller” is not proof that a route is dead.
- `create_auto_backup_before_erase()` is production-unreferenced but has a tested public
  contract and a deliberately different persistence model from file-copy startup backup.
- `advanced_to_basic` remains test-enshrined. Do not remove it without an explicit
  contract decision.

These items go to the owner-decision queue. If removal is approved, use a deprecation or
contract-removal WP with explicit migration notes and authorized test changes.

### Disposition of remaining scan observations

- Consolidate the duplicate `get_request_id()` implementation onto
  `utils/request_id.py` in WP0.1 after identity/behavior tests.
- Keep `success_response()`/`error_response()` asymmetry unchanged. It is awkward but
  changing return types is a cross-repository response-contract migration, not cleanup.
- Keep the tested-but-unused export streaming helpers pending OD10; do not call them dead
  solely because current routes do not select them.
- Normalize the `<main>` landmark in WP-1.5 with accessibility coverage.
- Record hardcoded assisted-exercise names, missing fatigue landmarks, server-data-to-JS
  conventions, taxonomy mirrors, cache-busting strategy, and long calibration helpers in
  the duplication/deferred registry. They are drift risks, not proven refactor defects.
- Investigate the volume-splitter silent-failure path and backup refresh/confirmation race
  before promoting either to Track A; the scan observed risk but did not provide a complete
  failing regression case.
- Leave `get_related_calibration_candidate` and duplicate generator validation untouched;
  they are outside the current payoff/risk boundary unless later profiling or defects
  justify a dedicated protected-logic WP.

---

## 2. Global rules

1. **Refactor WPs preserve behavior.** Do not change calculations, DB shapes, API shapes,
   status codes, user-visible copy, event timing, or persistence semantics in a refactor PR.
2. **Bug fixes are separate.** Track A below contains behavior changes. One bug or one
   tightly coupled bug family per PR, with a regression test that fails before the fix.
3. **Protected zones may move but may not change:**
   - effective-set factors and informational-only behavior;
   - fatigue thresholds, bands, landmarks, and Stage-4 evidence artifacts;
   - estimator priority chain;
   - progression decisions;
   - weekly/session aggregation and null-routine semantics;
   - volume taxonomy/classification mappings;
   - replace-exercise HTTP-200 error outcomes;
   - the locked fatigue advisory copy;
   - all Phase 2D-D-gated work.
4. **Public/tested is not dead.** Removing a tested function or HTTP endpoint requires an
   owner-approved contract-removal WP. Test deletion is allowed only when that WP names
   the deleted contract and migration impact explicitly.
5. **Dead-code proof is language-aware.** Python checks include decorators, registration
   closures, imports, scripts, tests, CI, and docs. JS checks include imports, DOM wiring,
   inline handlers, dynamic lookup, `window` assignments and actual callers. CSS checks
   include templates, JS-created classes, E2E selectors, and visual-helper overrides.
6. **Gate each source-changing WP.** Record the pytest baseline, run focused tests during
   implementation, then full pytest plus the literal E2E specs named by the WP. Counts may
   change only for explicitly added regression tests or approved contract removals.
   Documentation-only WPs use the repository's docs self-review gate. Phase close uses
   `/verify-suite`.
7. **Preserve import contracts.** Original Python import paths remain valid. Before a
   module split, commit an import/export and import-order characterization test.
8. **One WP = one PR.** Aim for reviewable diffs. Mechanical moves over 400 lines are
   allowed only where marked; do not combine a large move with logic cleanup.
9. **Never stage `data/database.db`; never rename CI job `name:` values.**
10. **Parallel work requires isolation.** Before concurrent work involving the DB, dev
    server, pytest, or E2E, follow `docs/ai_workflow/PARALLEL_WORKFLOW.md` and create
    worktrees with `scripts/new-worktree.ps1`.
11. **Rollback quickly.** If a gate fails and one focused correction does not explain it,
    revert/stash the WP and report rather than widening scope.
12. **Use symbols, not line numbers, as execution anchors.** Scan line numbers are evidence
    pointers only and will drift.

---

## 3. Owner-decision queue — RESOLVED 2026-07-04

All ten decisions recorded with the owner on 2026-07-04.

| ID | Decision | Owner decision (2026-07-04) |
|---|---|---|
| OD1 | Is plan weight `0` valid for bodyweight/assisted exercises? | **Allow 0 kg.** Behavior-change WP: fix the falsy-check family (`exercise_manager.py` weight, plus order=0 in remove/reorder), rewrite `test_add_exercise_missing_weight` accordingly. |
| OD2 | What are canonical server bounds for plan/log updates? | **Add sanity bounds.** Behavior-change WP: define and enforce server-side limits (weight ≥0 with sane cap, RIR 0–10, min-reps ≤ max-reps) on add/update paths; new tests; docs then become true. |
| OD3 | Should `GET /export_to_excel` mutate `exercise_order` while assembling a workbook? | **Fix it.** Behavior-change WP: remove the hidden `recalculate_exercise_order` write from Excel export after WP1.8 extracts it. `/export_to_workout_log` was already POST-only and all repository callers already used POST, so no method or frontend migration is needed. |
| OD4 | Null routines: dropped from weekly frequency or bucketed as `Unassigned`? | **Unify as `Unassigned`.** Behavior-change WP on a protected calc zone: weekly summary gains an Unassigned bucket matching session summary. Golden fixtures (WP2.3) must land first; product-risk review required. |
| OD5 | Is the novice branch in `_calculate_weight_increment` a no-op below 20 kg intentionally? | **Make experience matter.** Behavior-change WP on a protected zone: experienced lifters get +5 kg below 20 kg too. Regression tests on both experience levels around the 20 kg boundary. |
| OD6 | Remove/deprecate the five frontend-unreferenced HTTP endpoints? | **Remove them.** Contract-removal WP: delete `/get_routine_options`, `/get_user_selection`, `/get_exercise_details/<id>`, `/get_filtered_exercises`, `/get_unique_values/<table>/<column>` plus their tests, with migration notes. Sequence AFTER WP1.1/WP1.2 (the last one is in scope there). |
| OD7 | Remove the test-only effective-sets pipeline, `advanced_to_basic`, `create_auto_backup_before_erase`? | **Remove all three.** Contract-removal WP(s) with explicit migration notes; authorized test deletions (~26 effective-sets pipeline tests, taxonomy test, backup-contract tests). Note: the pre-erase **file snapshot** in `/erase-data` is live and stays — only the unused DB-table variant goes. |
| OD8 | Wire or delete `showAutoBackupBanner`? | **Wire it up.** Small feature WP: erase flow shows the banner referencing the live file-copy snapshot in `data/auto_backup/` (NOT the OD7-removed DB-table function). E2E on the erase flow. |
| OD9 | Promote `fatigue-context.spec.ts` into required CI? | **Promote to required.** CI WP: add as a NEW job/context (never rename existing required contexts); land after it has run green as non-required for a few PRs. |
| OD10 | Retire the exported/tested streaming-threshold helpers no route uses? | **Keep them.** WP1.8 gives them a clear home during export extraction. |

Owner decisions produce separate WPs — drafted as **Track B** below (2026-07-04).
They are not permission to fold behavior changes into the refactor packets below.
OD1–OD5 supersede the corresponding "Deferred behavior fixes" entries in Track A;
OD6/OD7 removals must be sequenced after the Phase-1 extractions that touch the same
files. OD10 requires no WP (keep as-is; WP1.8 homes the helpers).

---

## Track A — confirmed bug fixes (before structural refactors)

Each item is a separate, small PR unless two entries explicitly share one root cause.

**Completed 2026-07-04.** A1–A8 landed as PRs #91–#98 (A4–A8 used
#92–#96; A2/A3 used #97/#98). The final integrated gate on PR #98 passed
1629 pytest tests and both required functional E2E shards (202 + 202). Track B
prerequisites that say "Track A complete" are now satisfied.

### A1 Toast severity contract

- Correct all five reversed-signature `app.js` calls: two warnings, one success, and
  two errors.
- Add Vitest or E2E coverage proving success/warning/error classes and messages.
- A warning on legacy misuse is optional; do not remove the legacy API in this PR.
- Gate: JS test plus starter-plan paths in `workout-plan.spec.ts`.

### A2 Workout-log duplicate submission

- Keep the debounced handler and remove the competing inline `onchange` path.
- Prove one edit causes exactly one `/update_workout_log` POST and one calibration update.
- Gate: focused pytest plus `workout-log.spec.ts` and `learned-calibration.spec.ts`.

### A3 Progression badge drift

- Extract the assisted-bodyweight decision used by all three client update paths.
- Add a date-change regression case.
- Gate: JS characterization plus `workout-log.spec.ts` and `progression.spec.ts`.

### A4 Error-page and fatigue error-path fixes

- Align `error.html` with the variables passed by all route error renderers.
- Call `is_xhr_request()` with its actual zero-argument contract.
- These are separate commits/PRs if their focused test surfaces are independent.
- Gate: `tests/test_priority7_error_handling.py`, fatigue route tests, and
  `error-handling.spec.ts`.

### A5 Backup atomicity

- Make `create_backup()` header and item inserts one transaction, following the existing
  restore transaction pattern.
- Add a forced-mid-insert rollback test and item-count invariant.
- Gate: full program-backup pytest plus isolated `program-backup.spec.ts`.

### A6 Event-listener cleanup

- Close every execution-style-picker path through one cleanup function.
- Invoke the existing workout-dropdown cleanup when the owner element is replaced/closed.
- Gate: Playwright listener instrumentation (or Vitest if WP3.1 has landed) plus
  workout-plan interaction E2E.

### A7 Export delay

- Remove the unconditional `time.sleep(0.5)` from workbook cleanup.
- Verify generated workbooks and error cleanup, not elapsed time alone.
- Gate: export pytest and a manual download smoke.

### A8 DatabaseHandler CTE write locking

- Make write detection recognize `WITH ... INSERT/UPDATE/DELETE` statements, including
  `maintenance.REBUILD_EIM_SQL`.
- Add concurrency/dispatch unit cases without changing transaction semantics.
- Gate: database/maintenance pytest and full pytest.

### Deferred behavior fixes

- Weight-zero semantics, update validation, export-GET mutation, null-routine
  bucketing, and novice progression semantics are now decided (OD1–OD5) and drafted
  as WPB.1–WPB.5 in Track B below.
- Token load order is handled as visual-gated WP4.-1, not hidden in Track A.

---

## Track B — owner-decided behavior and contract changes (OD1–OD9)

Drafted 2026-07-04 from the §3 decisions. Each WP is a **separate PR** with migration
notes in the PR description and updated test coverage (refactor invariant, `CLAUDE.md`).
None of these may ride inside a move-only refactor WP. Prerequisites vary per WP — Track B
is interleaved with the phases, not a block; the prerequisite column in each entry governs.
Execution requires the owner's Track-A/Plan-v3 sign-off boxes plus this section's approval
per the sign-off checklist.

**Status at `main` @ `cbd5a25` (2026-07-05):** WPB.1 (#103), WPB.2 (#107),
WPB.5 (#101), WPB.7 (#102), WPB.8 (#104), and WPB.9 are shipped. WPB.9's job
landed in #100 and became required after ten consecutive green PRs (#100–#109),
without renaming or removing an existing context. At that baseline, WPB.3, WPB.4,
and WPB.6 remained prerequisite-gated.

**Current update (2026-07-07):** Phase 1 is complete — WP1.1–WP1.8 all landed
(#123, #126, #127, #130, #124, #125, #121, #122). WPB.3 shipped in #128 and WPB.6
shipped in #129. WPB.4 remains prerequisite-gated (needs WP2.3 golden fixtures).
Integrated `main` @ `f9bfb50`: pytest **1708 passed**; required Chromium functional
shards **205 + 202**; smoke **10**, backup **20**, erase **2**, fatigue-context **6**;
Playwright inventory **504 tests / 30 specs**.

### WPB.1 (OD1) Allow plan weight 0 for bodyweight/assisted exercises

- Fix the falsy-check family in `utils/exercise_manager.py`: weight `0` treated as
  missing on add, and `exercise_order`/`order` `0` treated as missing in remove/reorder.
- Rewrite `test_add_exercise_missing_weight` to assert 0 is accepted and `None`/absent
  is still rejected.
- Prerequisite: Track A complete. Land before Phase 1 touches the same routes/utils.
- Gate: workout-plan pytest family plus `workout-plan.spec.ts`.

### WPB.2 (OD2) Server-side bounds for plan/log updates

- Define canonical limits in one place (`utils/constants.py` or the WP1.1 validator
  module if it has landed): weight ≥ 0 with a sane upper cap, RIR 0–10,
  min-reps ≤ max-reps.
- Enforce on add and update paths for plan and log; reject with `error_response()`.
- New boundary tests per field; update any docs that previously overstated validation.
- Prerequisite: WPB.1 (weight-0 semantics define the lower bound). Coordinate with
  WP1.1 if concurrent — the allowlist/validator module is the natural home.
- Gate: plan/log pytest families plus `workout-plan.spec.ts` and `workout-log.spec.ts`.

### WPB.3 (OD3) Excel export stops mutating exercise order

- Remove the `recalculate_exercise_order` write from `GET /export_to_excel`; workbook
  assembly becomes read-only even when stored order values are duplicate or `NULL`.
- `/export_to_workout_log` was already POST-only, and both live frontend callers plus
  active pytest/E2E callers already used POST. Pin that contract in tests; no method or
  frontend migration is required.
- Migration note: startup `initialize_exercise_order()` still initializes `NULL` values.
  It does not repair duplicate non-NULL order values; those remain unchanged until an
  explicit reorder operation.
- Prerequisite: **WP1.8 first** (landed in #122). **SHIPPED in #128** (`73f40ad`),
  2026-07-07. The plan wording above was partly stale: `/export_to_workout_log` was
  already POST and all callers already used POST, so the only defect fixed was the
  hidden `recalculate_exercise_order` write on `GET /export_to_excel`. Test delta was
  intentional: four obsolete mutation tests removed, three stronger read-only
  preservation tests added.
- Gate: export pytest family plus the export/workout-log E2E paths.

### WPB.4 (OD4) Weekly summary `Unassigned` bucket for null routines

- Protected calc zone. Weekly summary buckets null-routine rows as `Unassigned`,
  matching session summary, instead of dropping them from frequency.
- Prerequisite: **WP2.3 golden fixtures must land first**; product-risk review required
  before merge.
- Gate: weekly-summary pytest + goldens diff reviewed as intentional, plus
  weekly-summary visual/E2E specs.

**Risk-mitigation gate (reviewed 2026-07-17):**

- The production schema makes `routine` `TEXT NOT NULL`; the reachable case is an empty
  string, while `None` remains relevant to mocked/legacy rows. State explicitly that all
  falsy routine values coalesce into one synthetic `Unassigned` session.
- Freeze scope to session-derived metrics only: weekly raw/effective totals, reps, volume,
  status, contribution weights, rounding, response fields, and pattern coverage must not
  change. Decide separately whether `global_sessions` includes the synthetic bucket; do
  not let that denominator change happen implicitly.
- Add focused cases for empty/`None`, above- and below-1.0 frequency thresholds, multiple
  anonymous rows accumulating into one bucket, and mixed named/anonymous routines across
  the full counting-mode x contribution-mode matrix.
- Regenerate the WP2.3 golden only after reviewing the exact delta. For the existing Calves
  sentinel, the intended change is frequency `0 -> 1`; effective-mode `sets_per_session`
  `0.85 -> 5.1`; raw-mode `sets_per_session` `1 -> 6`; and effective-derived average/max
  `0/0 -> 5.1/5.1`. Weekly totals and classifications must remain identical.
- Add route/E2E assertions for the displayed frequency and average/max-per-session values,
  run summary-page functional and visual gates, and include migration notes describing the
  intentional semantic change and the conservative one-bucket assumption.

### WPB.5 (OD5) Experience-aware increment below 20 kg

- Protected calc zone. In `_calculate_weight_increment`, experienced lifters get
  +5 kg below 20 kg too (novice behavior unchanged).
- Regression tests on both experience levels around the 20 kg boundary (just below,
  at, just above).
- Prerequisite: Track A complete; product-risk review required (progression semantics).
- Gate: progression pytest family plus `progression.spec.ts`.

### WPB.6 (OD6) Remove the five frontend-unreferenced endpoints

- Delete `/get_routine_options`, `/get_user_selection`, `/get_exercise_details/<id>`,
  `/get_filtered_exercises`, `/get_unique_values/<table>/<column>` plus their tests.
- Migration notes list each removed route and its replacement (or "none — unused").
- Implementation baseline after WP1.2: pytest collection **1714 → 1694** (20 approved
  endpoint-contract cases removed); Playwright inventory **505 → 504** (the permissive
  routine-options API test removed). Migration replacements are recorded in
  `docs/CHANGELOG.md`.
- Prerequisite: **after WP1.1/WP1.2** — `/get_unique_values` is in WP1.2's scope; removing
  it earlier would churn that extraction. **SHIPPED in #129** (`f9bfb50`), 2026-07-07,
  rebased onto post-WP1.4 `main`. Also removed the endpoint-only
  `fetch_registered_unique_values`; `fetch_filter_values` and
  `ExerciseManager.fetch_unique_values` are preserved.
- Gate: full pytest (expected count drop documented) plus API-integration E2E.

### WPB.7 (OD7) Remove the three dead contracts

- Remove the second (test-only) effective-sets pipeline, `advanced_to_basic`, and the
  **DB-table** `create_auto_backup_before_erase` variant.
- The pre-erase **file snapshot** in `/erase-data` (live copy into `data/auto_backup/`)
  **stays** — verify the erase flow still produces it before merging.
- Authorized test deletions: ~26 effective-sets pipeline tests, the taxonomy test, and
  the DB-table backup-contract tests. Migration notes list every deleted public symbol.
- Prerequisite: after the Phase-1 extraction touching the same file, if any; must land
  **before or independent of** WPB.8 — the banner must never reference the removed
  function.
- Gate: full pytest (expected count drop documented) plus erase-flow smoke.

### WPB.8 (OD8) Wire `showAutoBackupBanner` into the erase flow

- Erase flow shows the banner referencing the **live file-copy snapshot in
  `data/auto_backup/`** — not the DB-table function WPB.7 removes.
- E2E asserting the banner appears post-erase with the snapshot reference.
- Prerequisite: coordinate with WPB.7 (either order, but the banner's data source is
  the file snapshot from day one).
- Gate: erase-flow E2E plus any program-backup pytest touching the banner's data.

### WPB.9 (OD9) Promote `fatigue-context.spec.ts` to required CI

- Add as a **new** job/context — never rename an existing required context (renames
  orphan branch-protection checks and hard-block PRs).
- Land only after the spec has run green as non-required on several consecutive PRs;
  record the observed runs in the PR description.
- Prerequisite: none code-side; timing-gated by the green-run streak.
- Gate: the new context green on the promoting PR itself; branch-protection update is a
  separate, reversible settings change.

---

## Phase -1 — evidence, docs, and gate hardening

**Completed 2026-07-05.** WP-1.0 evidence was already integrated; WP-1.1 through
WP-1.5 shipped in PRs #106, #105, and #108–#110. Final CI on PR #110 passed
1684 pytest tests, functional Chromium shards 206 + 202, fatigue-context 6, and
erase-flow 2. The full Playwright inventory is 505 tests across 30 specs.

### WP-1.0 Merge the scan evidence

- Bring `SCAN_PROGRESS.md`, `SCAN_FINDINGS.md`, `SCAN_RECOMMENDATIONS.md`, and
  `docs/scan/PHASE_*.md` from `scan/codebase-grounding@a6574b9` into the target branch.
- Documentation only; preserve provenance and do not edit findings to match this plan.

### WP-1.1 Documentation truth sync

**Completed in PR #106.**

- Correct the startup initializer inventory, blueprint count, current verified counts,
  handover SHA wording, route-validation claims, E2E spec ledger, and fatigue-context CI row.
- Correct stale `STATUS_MAP` import documentation; current `session_summary.py` imports only
  `EFFECTIVE_STATUS_MAP`.
- Gate: docs self-review and command/example dry run.

### WP-1.2 Hermetic pytest baseline

**Completed in PR #105.**

- Move `test_volume_taxonomy.py` and `test_catalog_invariants.py` off live
  `data/database.db` onto isolated fixtures or committed test fixtures.
- Add a guard test that fails if test DB resolution points at the live path.
- Gate: both files repeatedly, then full pytest with live DB hash unchanged.

### WP-1.3 Close prerequisite unit-test gaps

**Completed in PR #108.**

- Add direct tests for `create_startup_backup`, `lift_matching`, and `exercise_media`.
- Add import-order/export-surface tests needed by the estimator split.
- Extend body-fat JS↔Python parity to all four mandated functions, preferably through a
  shared fixture consumed by pytest and Vitest/E2E.
- Keep these characterization-only; no production changes.

### WP-1.4 Repair vacuous E2E assertions

**Completed in PR #109.**

- Replace `expect(true)`, `x || true`, and equivalent non-assertions in
  `validation-boundary`, `empty-states`, `exercise-interactions`, and
  `superset-edge-cases` with observable outcomes.
- Do not introduce WPB.2's approved-but-not-yet-implemented validation behavior here;
  characterize current behavior or mark the case pending on WPB.2.

### WP-1.5 Normalize the main landmark

**Completed in PR #110.**

- Make `base.html` own the single `<main id="main-content">` landmark and replace nested
  page-level `<main>` elements with neutral containers, or choose the inverse pattern and
  apply it consistently. Never produce nested or duplicate main landmarks.
- Preserve page IDs/classes/data hooks and skip-link target behavior.
- Gate: template pytest plus accessibility and smoke-navigation E2E.

---

## Phase 0 — safe dead code and repository hygiene

### WP0.1 Proven Python dead code/constants

- Runtime-probe the shadowed error handlers; remove only the two proven unreachable
  registrations while preserving live 400/422/500/APIError behavior.
- Recheck and remove definition-only constants:
  `HOME_BASIC_EQUIPMENT`, `DEFAULT_SETS_TARGET`, `MovementCategory`, `REP_RANGE_PCT`,
  and `weekly_summary.STATUS_MAP`.
- Replace the duplicate `utils.errors.get_request_id` helper with an import from
  `utils.request_id`; preserve request-header and generated-ID behavior.
- Do not touch OD6/OD7 candidates.
- Gate: focused error/summary/movement/estimator tests, then full pytest.

### WP0.2 Empty `utils/__init__.py`

- Reconfirm zero facade importers, including function-local and dynamic imports.
- Reduce the file to its package docstring; concrete module imports remain canonical.
- Must land before filter/module relocation work.
- Gate: full pytest plus isolated app boot and `GET /`.

### WP0.3 Archive one-off scripts and root baselines

- Recheck scripts against code, tests, CI, scheduled tasks, pyright baseline, and docs.
- Preserve all Stage-4 observer automation and live mapping/build helpers.
- Archive the v2 candidates plus `seed_visual_baseline.py` only after updating its docs
  and static-analysis disposition; do not confuse it with
  `e2e/scripts/build_visual_seed.py` or `prepare_visual_db.py`.
- ~~Remove root `baseline_e2e.txt`/`baseline_pytest.txt` and ignore future copies.~~
  **Done** — the files were removed and `/baseline*.txt` is ignored (`.gitignore`);
  the generating command now writes to `artifacts/` (root-cleanup Packet C1).
- Gate: full pytest, pyright baseline diff, visual seed smoke, CI.

### WP0.4 JavaScript dead-code sweep

Handle one coherent cluster per PR, with import/call/runtime proof:

- `charts.js` and its unreachable initializer path;
- `summary.js` no-op exports (coordinate with WP3.2);
- duplicate Add-Exercise flow in `exercises.js`;
- dead workout-log filter block and nonexistent endpoint call;
- dead progression modal/card functions;
- runtime-unreachable table-responsiveness exports;
- `showAutoBackupBanner` only after OD8.

Do not delete CSS here; CSS reachability needs the Phase-4 selector/visual harness.

---

## Phase 1 — route and service boundaries

Goal: routes parse/validate HTTP input, call utils services, and shape responses. Preserve
all endpoint URLs and response envelopes unless an OD-approved contract WP says otherwise.

**STATUS: COMPLETE (2026-07-07).** All eight work packets landed on `main` @ `f9bfb50`
via PRs #123, #126, #127, #130, #124, #125, #121, #122. Integrated CI: pytest **1708
passed**; required Chromium functional shards **205 + 202**; Playwright inventory **504
tests / 30 specs**. Each WP preserved endpoint URLs and response envelopes.

### WP1.1 Central filter allowlist and validators — **SHIPPED (#123)**

- Move `ALLOWED_TABLES`, `ALLOWED_COLUMNS`, and validation into a utils-owned registry.
- Reconcile it explicitly with `FilterPredicates.VALID_FILTER_FIELDS`; encode aliases and
  purpose-specific subsets instead of silently taking a union.
- Keep route-level re-exports for existing tests/callers.
- Add malicious table/column cases and vocabulary parity tests.

### WP1.2 Extract both route-level unique-value contracts — **SHIPPED (#126)**

- Move the workout-plan specialized normalization contract to
  `utils/filter_values.fetch_filter_values`.
- Move `/get_unique_values/<table>/<column>` query behavior to a separate utils function
  using the central registry.
- Keep `ExerciseManager.fetch_unique_values(table, column)` as a distinct generic/internal
  contract for now; do not merge signatures or normalization semantics.
- Gate: filter/exercise-manager pytest plus workout-plan, exercise-interactions, and API E2E.

### WP1.3 Extract replace-exercise service — **SHIPPED (#127)**

- Move candidate selection, deduplication, and swap persistence to
  `utils/exercise_replacement.py`.
- Keep parsing and structurally identical response envelopes in the route, including the
  three HTTP-200 error outcomes.
- Gate: replacement pytest, `replace-exercise-errors.spec.ts`, `workout-plan.spec.ts`.

### WP1.4 Extract superset service — **SHIPPED (#130)**

- Move validation queries, pairing, persistence, and suggestions to `utils/supersets.py`.
- Preserve ID generation, ordering, messages, and response shapes even where improvement
  is tempting.
- Persistence coverage includes the `remove_exercise` partner-unlink, extracted to
  `unlink_partner_for_removal(db, exercise_id, superset_group)`. Unlike the other service
  entry points it reuses the caller's `DatabaseHandler` so the partner-null, log-delete,
  and exercise-delete continue to share one handler (connection + write lock); behavior
  and the removal log are preserved exactly.
- Gate: superset pytest, `superset-edge-cases.spec.ts`, `workout-plan.spec.ts`.

### WP1.5 Workout-log service boundary — **SHIPPED (#124)**

- Move mutations and calibration-trigger orchestration from `routes/workout_log.py` to
  `utils/workout_log_service.py`.
- Do not add validation until OD2 is resolved.
- Gate: workout-log/calibration pytest and workout-log/learned-calibration E2E.

### WP1.6 Body-composition service boundary — **SHIPPED (#125)**

- Move CRUD/query logic to utils while keeping body-fat formulas unchanged.
- Preserve the JS↔Python parity fixture introduced in WP-1.3.
- Gate: body-composition pytest and `body-composition.spec.ts`.

### WP1.7 Volume-splitter service boundary — **SHIPPED (#121)**

- Move history/get/delete, range defaults/sanitization, and export orchestration to utils.
- Document the second classification vocabulary; do not consolidate it with canonical
  volume classes in this behavior-preserving WP.
- Gate: volume-splitter pytest, volume-splitter and volume-progress E2E.

### WP1.8 Export service boundary — **SHIPPED (#122)**

- Move mapping tables, dataframe transforms, query construction, sheet assembly, and
  export-to-log persistence into utils modules.
- Preserved `GET /export_to_excel`'s exercise-order side effect at extraction time;
  WPB.3 (#128) subsequently removed that side effect per OD3.
- Gate: export pytest plus plan export/download and workout-log import flows.

`routes/user_profile.py` needs no extraction WP: its handlers are already thin; the file's
size is mostly static view-model data.

---

## Phase 2 — Python module structure and schema ownership

### WP2.1a Estimator characterization and dependency map

- Freeze the supported export surface, underscore names used by tests, lift-matching alias
  identity, and both import orders with `strength_calibration`.
- Document the six clusters and their dependency direction before moving code.
- No production move in this WP.

### WP2.1b–f Staged `profile_estimator` extraction

Keep `utils/profile_estimator.py` as the stable public facade/orchestrator. Extract leaf
clusters into an internal package such as `utils/_profile_estimator/` in separate PRs:

1. constants and lookup tables;
2. trace builders;
3. accuracy and coverage-guidance helpers;
4. cohort ranges/bars/donut;
5. bodymap `muscle_coverage_state` helpers.

The estimation priority chain remains in the facade/core until leaf moves are stable.
Lazy `strength_calibration` imports stay function-local. Each move is mechanical; no
renaming or “cleanup while here.” This staged shape replaces v2's risky atomic 2,418-line
file-to-package conversion.

- Gate each PR: estimator and calibration pytest; final close adds user-profile and
  learned-calibration E2E plus import-order tests.

### WP2.2 Decompose plan-generator functions

- Extract helpers from `_score_exercise`, `_apply_priority_muscle_boost`, `persist`, and
  `generate_starter_plan` without reordering scoring.
- Preserve `persist()`'s inner swallow/log/continue and outer re-raise tiers exactly.
- Removing the unused `routine` parameter changes a callable signature; defer it unless a
  separate internal-caller proof authorizes it. The unused loop variable may be cleaned.
- Gate: unmodified plan-generator tests plus starter-plan E2E.

**Completed 2026-07-16.** Extracted scoring, priority-allocation, persistence, and
result-assembly helpers without changing the public callable signature, score ordering,
row-order mutation, or the inner-continue/outer-reraise exception tiers. Added explicit
contract tests for those seams. Local gate: **1,723 pytest passed** and the complete
API-integration + workout-plan Chromium pair **92 passed**.

### WP2.3 Weekly-summary decomposition with durable goldens

- First commit deterministic seeded golden fixtures for both public calculations,
  canonicalized as JSON and checked in tests—not pasted only into a PR description.
- Extract private helpers in the same module, using session-summary structure as a model.
- Preserve Effective/Raw side-by-side shape, warning order, rounding, null-routine
  behavior, and movement fallback pending OD4.
- Gate: all summary/pattern/effective-set tests, golden equality, summary-pages and API E2E,
  product-risk review.

### WP2.4 Staged fatigue-module split

- Freeze exports and golden outputs first.
- Move the four banner-delimited concerns—phase-1 core, per-muscle, period-window, SFR—into
  internal modules while `utils/fatigue.py` remains the public facade.
- Do not consolidate duplicated scored-row or tie-break rules in the move PRs; record them
  in the duplication registry below.
- Gate: all fatigue pytest, fatigue/fatigue-context/summary E2E, product-risk review.

### WP2.5 Duplication registry (document-only decisions)

Record owners, current semantic differences, tests, and a future convergence decision for:

- fatigue scored-row and sort tie-break rules;
- estimator/calibration load-basis arithmetic;
- weekly/session aggregations and the exported effective-set pipeline;
- movement-pattern classification forks;
- weekly/session null-routine behavior;
- JS/Python taxonomy lists;
- assisted-bodyweight catalog names and fatigue landmark coverage;
- the three server-data-to-JS conventions and static-asset cache-busting policy;
- volume-splitter silent failures and backup refresh/confirmation interaction;
- response-helper return-type asymmetry and long protected calibration helpers.

Do not consolidate protected logic merely because arithmetic looks identical.

**Shipped** — see [`docs/DUPLICATION_REGISTRY.md`](DUPLICATION_REGISTRY.md) (14 items,
docs-only, zero code change; no consolidation performed). The one drift-removing
consolidation (schema-init manifests) is deferred to WP2.6.

### WP2.6 Schema registry — last Python WP

- Create `utils/schema_registry.py` with
  `run_all_initializers(*, force_base: bool = False)`.
- Call every initializer in current order: base schema, all six `add_*` functions,
  exercise-order migration, then `utils.program_backup.initialize_backup_tables`.
- Remove the duplicate progression-goals instance/module implementation only after caller
  inventory proves one can become a thin compatibility wrapper.
- Startup passes `force_base=False`; erase and isolated test setup pass `True` where they
  currently force base reinitialization.
- Move `initialize_exercise_order`, `column_exists`, and `table_exists` to utils and keep
  temporary route re-exports.
- Define canonical owned-table/drop ordering in utils and consume it from erase paths.
  Preserve child-before-parent drops and the pre-erase file snapshot.
- Reconcile `maintenance.py`'s drifted isolated-muscle schema with the canonical definition;
  do not create a new table shape.
- Classify callers before editing:
  - full-startup mirrors migrate to the registry;
  - isolated initializer/migration tests remain direct;
  - old-schema fixtures deliberately remain partial.
- Keep `create_startup_backup()` outside the registry and after initialization.
- Explicit large cross-cutting WP; architecture and code review required.
- Gate: `/verify-suite`, isolated backup restore, fresh scratch-DB boot, erase/reinitialize
  smoke, legacy-schema fixtures, and proof the live DB was untouched.

---

## Phase 3 — JavaScript characterization, extraction, and transport

Decision remains plain JavaScript + Vitest; no TypeScript conversion.

### WP3.1 Vitest scaffold

- Add pinned `vitest` and `jsdom`, config, `test:js`, and a non-required CI job without
  renaming existing contexts.
- Seed with genuinely pure `exercise-helpers.js` tests. `toast.js` is DOM/Bootstrap code;
  test it only with explicit DOM and Bootstrap fakes, not as a “trivial pure helper.”

### WP3.2a–d Extract inline scripts one page at a time

Separate PRs:

1. weekly summary;
2. session summary;
3. workout plan;
4. welcome/base only if their blocks remain non-trivial after audit.

Preserve script type, placement, DOM-ready timing, globals, and mode defaults. The summary
inline scripts are the live implementation; do not merge them into no-op `summary.js`.
Delete that file only when all imports/callers are proven gone.

- Gate each page with matching pytest and literal feature-map E2E; base/welcome extraction
  additionally runs smoke-navigation, nav-dropdown, and dark-mode.

### WP3.3 Characterize workout-plan seams and shared state

- Write tests for payload builders, formatting, estimate rendering data, execution-style
  decisions, replacement payloads, Add-Exercise validation/payloads, and superset helpers.
- Introduce a named state module or explicit dependency object for
  `selectedExerciseIds`, `supersetColorMap`, `allExercisesCache`, and
  `currentRoutineTabFilter` before feature splitting.
- No DOM feature move until these tests are green.

### WP3.4a–h Split `workout-plan.js` by real feature boundaries

Use separate mechanical PRs, allowing large move-only diffs:

- `state.js` — **delivered by WP3.3 (#147).** The four shared values
  (`selectedExerciseIds`, `supersetColorMap`, `allExercisesCache`,
  `currentRoutineTabFilter`) already live in `workout-plan-state.js` as a singleton the
  monolith mutates inline; no accessor/mutator functions remain to move, so no separate
  `state.js` move-only PR is needed. Routine-tab/table behavior folds into WP3.4b below,
  importing the existing state singleton.
- `table.js` including adjacency/color integration points, plus the routine-tab filter/render
  functions (state singleton imported, not re-declared);
- `estimates.js` including fatigue context/nudge;
- `execution-style.js`;
- `replacement.js`;
- `add-exercise.js`;
- `supersets.js` with table dependencies injected explicitly;
- `media.js` and a thin `index.js` wiring entry.

Preserve the single entry script and event timing. Run Vitest plus workout-plan,
exercise-interactions, superset-edge-cases, fatigue-context, learned-calibration, and
replace-exercise-errors E2E after every boundary-affecting move.

### WP3.5 JSON API transport consolidation

- Re-run a repository-wide raw-fetch inventory after inline extraction.
- Migrate JSON app-endpoint calls to shared `apiFetch`/`api`.
- Delete `volume-splitter.js`'s local envelope/error wrapper rather than layering the
  shared wrapper beneath it.
- **Keep raw fetch** for static SVG/text assets in `bodymap-svg.js` and
  `muscle-selector.js`, and for blob/download exports, because the wrapper has no binary
  contract. Document every intentional exception.
- Coordinate bodymap files with the queued heatmap workstream.
- Gate: Vitest, full pytest, API integration, volume, plan, profile, navigation, and export
  download flows.

### WP3.6 Optional user-profile split

Only after the core JS track: characterize and split the 1,483-line file by demographics,
reference lifts, coverage/bodymap, calibration review, and settings toggles. Consolidating
the two optimistic-toggle paths is a later behavior-aware cleanup, not part of move-only PRs.

**Completed 2026-07-17 in the current working tree.** The original entry module is now a
small coordinator over focused data, forms/autosave, insights, bodymap, settings, and
calibration-review modules. Initialization order, DOM hooks, API endpoints, payloads,
toasts, rollback behavior, and the two distinct optimistic-toggle implementations are
unchanged. Added pure estimator-seam characterization tests. Gate: Vitest **105 passed**,
focused Python **75 passed**, full pytest **1,723 passed**, and profile +
learned-calibration + fatigue-context Chromium **38 passed** against the isolated E2E
database.

---

## Phase 4 — CSS foundation, visual harness, then cleanup

Stay on structured plain CSS. SCSS continues to own Bootstrap customization plus its
existing fatigue/volume-panel partials; remember those selectors are compiled into
`bootstrap.custom.min.css` and are part of the collision audit.

### Visual contract for every CSS WP

- Use `PW_VISUAL_SEED=1`; never seed or rewrite the live DB.
- Windows compares `e2e/__screenshots__/win32`; the manually dispatched `visual-linux`
  deep-gate job compares Linux baselines.
- Run the affected functional specs as well as snapshots. Pixel equality alone cannot
  catch selector-helper mistakes.
- Rebaseline only for intentional, owner-reviewed visual changes on both platforms.

### WP4.-1 Cascade and load-order foundation

- Load `tokens.css` before every consumer bundle.
- Declare one explicit `@layer` order covering existing layers before removing any
  `!important` declarations.
- Inventory selectors compiled into `bootstrap.custom.min.css`.
- No class rename, token-value change, or bulk de-`!important` work here.
- Gate: full functional frontend set plus byte-identical visual comparison.

**Completed 2026-07-16 in the isolated WP4 worktree.** `tokens.css` now loads
before Bootstrap's compiled app partials and every global/route consumer. One
explicit order preserves the prior implicit precedence as `workout`, `navbar`,
`workout-dropdowns`, `welcome`; the 18-bundle cap and all ten route owners are
unchanged. The compiled artifact inventory found 1,429 unique selector entries,
including 58 fatigue and 57 workout-plan volume-panel entries owned by SCSS.
Four focused contracts, blocking static checks, Vitest (93), and the complete
required Chromium set (407) passed. Seeded visual comparison reproduced the
unchanged animated-GIF known-reds with identical mismatch counts; no snapshot
was rebaselined. Full evidence: [`CSS_PHASE4_WP4_-1_EVIDENCE.md`](CSS_PHASE4_WP4_-1_EVIDENCE.md).
WP4.0a followed and is not included in this packet.

### WP4.0a Harden visual and functional selectors

- Replace visual-helper hardcoded presentation classes with stable `data-testid`/data
  hooks where appropriate.
- Replace exact-RGB assertions in nav/summary functional specs with token-aware semantic
  assertions or snapshots without weakening what they prove.
- Add User Profile and Backup to `visual.spec.ts`; v2's page list omitted both while
  scheduling their bundles for cleanup.
- Generate and review both platform baselines before CSS restructuring.

**Completed 2026-07-17 from committed WP4.-1 (`6e0a408`).** Stable
`data-visual-*` hooks replace visual-helper presentation classes, nav/summary
color contracts resolve their owning CSS variables, and Profile/Backup expand
each platform matrix from 48 to 60 images. All 12 new images per platform were
reviewed and passed update-free comparison. The 48 old Windows images stayed
byte-identical; Linux artifact review rejected 17 regenerated legacy variants
and imported only the 12 missing images. The Linux compare's 11 reds were all
confined to pre-existing animated signature/exercise-thumbnail pixels; no new
route failed. Static/unit/Python gates and the full 407-test functional set are
verified. See
[`CSS_PHASE4_WP4_0A_EVIDENCE.md`](CSS_PHASE4_WP4_0A_EVIDENCE.md). WP4.0 followed
and is not included in this packet.

### WP4.0 Fresh known-red ledger

- Run the complete functional and visual deep gates on unchanged `main` after WP4.0a.
- Record exact current reds in this plan and handover. Do not inherit the May ledger.

**Completed 2026-07-17 on unchanged branch head `e46b67e`.** Fresh gates:
selector/cascade contracts **7**, blocking flake8 **0**, tsc passed, Vitest
**93**, full pytest **1,722 passed + 2 visual-seed catalog reds**, and the exact
required Chromium functional list **407/407**. Update-free Windows visual
comparison produced **59 passed + 1 animated-frame red**; its serial thumbnail
companion produced **1 passed + 1 animated-frame red + 16 not run**. Fresh
pinned-Linux compare run
[29539611526](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/29539611526)
produced **51 passed + 11 animated-frame reds + 16 not run**, plus one
initial-attempt profile GIF flake that passed retry. Every report/diff was
inspected; there was no unexplained cascade or layout regression. All 156
snapshot PNGs, generated Bootstrap CSS, the main live DB, and the unrelated
main-checkout WP2.2 edits stayed byte-identical. No snapshot was updated.
Complete ledger:
[`CSS_PHASE4_WP4_0_EVIDENCE.md`](CSS_PHASE4_WP4_0_EVIDENCE.md). WP4.1 is next
and is not included in this packet.

### WP4.1 Token vocabulary consolidation

- Inventory hardcoded values, duplicate spacing vocabularies (`--space-*` vs `--s-*`),
  and six local namespaces (`--wl-*`, `--nav-*`, `--bc-*`, `--backup-*`, `--volume-*`,
  `--fatigue-*`).
- Define alias/deprecation mapping before consumption; adding aliases must be visually
  neutral.
- Add stylelint as non-required measure-only CI with pinned rules and a baseline report.

**Completed 2026-07-17 in the isolated `wt/wp4-1-token-vocabulary`
worktree.** The frozen inventory distinguishes responsive layout spacing from
fixed component spacing: new `--layout-space-*` definitions retain every
former `--space-*` value, while `--space-*` remains a compatibility alias and
`--s-*` remains fixed. Only exact `--wl-*` status/duration and `--nav-*`
spacing matches were aliased; all other local feature namespaces remain
intact. Pinned Stylelint 16.11.0 measures 7,202 pre-change warnings across 21
sources and reports a non-blocking CI delta; no required context was renamed.
Static, unit, Python, functional Chromium, and update-free visual gates passed
with only the exact WP4.0 known reds. All 156 screenshots, generated Bootstrap
CSS, and live databases stayed byte-identical. Evidence:
[`CSS_PHASE4_WP4_1_EVIDENCE.md`](CSS_PHASE4_WP4_1_EVIDENCE.md). WP4.2 is next
and is not included in this packet.

### WP4.2 Shared-frame dedupe and ownership repair

- Extract the four-copy weekly/session/log/plan frame block once into `components.css`.
- Relocate the roughly 600 lines of log/summary content misfiled in
  `pages-workout-plan.css`.
- Delete only template/JS/E2E-proven dead selectors.
- Treat this as cascade-sensitive structural movement with full visual gates.

**Completed 2026-07-18 in the isolated `wt/wp4-2-shared-frame-dedupe`
worktree.** The shared block is owned once in `components.css` under
`:where(#workout, .workout-log-page, .summary-frame)`; route-specific log and
summary surfaces remain later in their route bundles. A diagnostic rejected the
initial document-wide `html:has(...)` gate: it changed masked Chromium
compositing on Progression despite no changed matched rule or computed value.
Direct container scope restores byte-identical Progression output. The five CSS
files shrink by a net **3,668 lines**. Contracts **12/12**, affected Chromium
**84/84**, required Chromium **407/407**, pytest **1,733 + 2 known catalog reds**,
and update-free visual locks all match. Stylelint falls from the 7,202 baseline
to **6,444** with unchanged selector ceiling warning counts and zero parse/config
errors. All 156 snapshots, generated Bootstrap, and protected DBs are unchanged.
Evidence: [`CSS_PHASE4_WP4_2_EVIDENCE.md`](CSS_PHASE4_WP4_2_EVIDENCE.md). The
packet was integrated into local `main` as merge `d695188`; narrow post-merge
gates passed, nothing was pushed, and WP4.3 had not started.

### WP4.3 Page dark-mode/token cleanup

One page per PR, smallest first. Use `pages-user-profile.css` as the target pattern but do
not churn it merely for consistency. Suggested order:

1. backup;
2. body composition;
3. progression;
4. volume splitter;
5. welcome;
6. session summary;
7. weekly summary;
8. user profile (audit/minimal cleanup);
9. workout plan, split into coherent internal sections;
10. workout log, split into multiple WPs because its per-theme colors and 375
    `!important` declarations make it redesign-sized.

**WP4.3a Backup completed 2026-07-18 in isolated
`wt/wp4-3-backup-dark-token-cleanup`.** Five exact repeated Backup values now use
semantic page-local tokens, unused `--backup-warm` was removed, and the existing
exact border token was reused. No shared near-match or page-local dark rule was
mechanically changed. Browser auditing preserved computed values and declaration
owners for 16 representative dynamic targets in both themes. Pinned Stylelint
falls **6,444 → 6,435** with no increase to duplicate, specificity, or important
counts. Contracts **13/13**, focused Backup Chromium **20/20**, required Chromium
**407/407**, and pytest **1,734 + 2 catalog known-reds** match the expected gates;
all six Backup variants pass and the full suites reproduce only the exact WP4.0
known reds. All integrity locks are unchanged. Evidence:
[`CSS_PHASE4_WP4_3A_EVIDENCE.md`](CSS_PHASE4_WP4_3A_EVIDENCE.md). The packet was
integrated into local `main` as merge `dc607fe`; narrow post-merge gates passed,
all protected identities remained unchanged, nothing was pushed, and WP4.3b had
not started. Begin only the Body Composition page packet next.

**WP4.3b Body Composition completed 2026-07-18 in isolated
`wt/wp4-3-body-composition-dark-token-cleanup`.** Three exact repeated route
values now use semantic `--bc-*` tokens. Browser auditing proved the route's
heading colors were dead because shared important component rules already win in
both themes; those declarations and an unused dark `--bc-accent-soft` remap were
removed with no rendered computed-style delta. Pinned Stylelint falls **6,435 →
6,428** with no increase to duplicate, specificity, or important counts.
Contracts **14/14**, focused Body Composition Chromium **9/9**, required
Chromium **407/407**, and pytest **1,735 + 2 catalog known-reds** match the
expected gates. All six Windows route variants pass; all twelve committed Body
Composition images and all integrity locks are unchanged. The full suites
reproduce only the exact WP4.0 known reds. Evidence:
[`CSS_PHASE4_WP4_3B_EVIDENCE.md`](CSS_PHASE4_WP4_3B_EVIDENCE.md). The packet was
integrated into local `main` as merge `92291ed`; narrow post-merge gates passed,
all protected identities remained unchanged, and nothing was pushed. Progression
and later packets have not started; wait for explicit direction before beginning
another packet.

**WP4.3c Progression completed 2026-07-18 in isolated
`wt/wp4-3-progression-dark-token-cleanup`.** Exact repeated route expressions now
use semantic `--progression-*` tokens; repeated dark Flatpickr literals use four
tokens scoped to the existing calendar owner. Browser auditing proved that the
dark suggestion-card copy declaration was shared-owned and that three fatigue
colors were redundant under the global dark token remaps. Only those dead or
redundant properties were removed; live goal-badge, fatigue-mix, and Flatpickr
dark owners remain. Computed values for 33 targets are identical in both themes.
Pinned Stylelint falls **6,428 → 6,404** with no increase to duplicate,
specificity, or important counts. Contracts **15/15**, focused Progression
Chromium **26/26**, required Chromium **407/407**, and pytest **1,736 + 2 catalog
known-reds** match the expected gates. All six Windows route variants pass; all
twelve committed Progression images and all integrity locks are unchanged. The
full suites reproduce only the exact WP4.0 known reds. Evidence:
[`CSS_PHASE4_WP4_3C_EVIDENCE.md`](CSS_PHASE4_WP4_3C_EVIDENCE.md). The packet was
integrated into local `main` as merge `e7feffa`; narrow post-merge gates passed,
all protected identities remained unchanged, and nothing was pushed. Volume
Splitter and later packets have not started; wait for explicit direction before
another packet begins.

**WP4.3d Volume Splitter completed 2026-07-18 in isolated
`wt/wp4-3-volume-splitter-dark-token-cleanup`.** Exact repeated status, accent,
heading, and dark-surface values now use semantic page-local tokens. Browser
auditing proved that shared component rules own the removed dark result-section,
table-copy, and history properties, while later type-specific rules own every
runtime suggestion-card background. Only those dead/redundant declarations were
removed; live result borders, backgrounds, shadows, focus styles, and suggestion
types remain. Thirty-seven stable dynamic targets are identical in both themes.
Pinned Stylelint falls **6,404 → 6,364**: hardcoded values **-36** and important
declarations **-4**, with duplicate and specificity counts unchanged. Contracts
**16/16**, focused Volume Splitter Chromium **27/27**, required Chromium
**407/407**, and pytest **1,737 + 2 catalog known-reds** match the expected gates.
All six Windows route variants pass; all twelve committed Volume Splitter images
and every integrity lock are unchanged. Full visuals reproduce only the exact
WP4.0 known reds. Evidence:
[`CSS_PHASE4_WP4_3D_EVIDENCE.md`](CSS_PHASE4_WP4_3D_EVIDENCE.md). The packet was
integrated into local `main` as merge `40bc09f`; narrow post-merge gates passed,
all protected identities remained unchanged, and nothing was pushed. Leave its
isolated worktree and branch for review and wait for explicit direction before
another packet.

**WP4.3e Welcome completed 2026-07-19 in isolated
`wt/wp4-3-welcome-dark-token-cleanup`.** The exact repeated white-ink and
translucent-white overlay expressions now use four page-local semantic tokens
(`--wl-on-accent`, `--wl-overlay-soft`, `--wl-overlay-strong`,
`--wl-overlay-border`); no near-match brand accent/gradient literal was
normalized. Seven dead (zero-`var()`-consumer) custom properties were removed
outright — the `--wl-featured-start`/`-end`/`-gradient` trio (the cards paint
their hardcoded `!important` gradients directly), the
`--wl-accent-glow`/`--wl-shadow-glow` chain, `--wl-info`, and
`--wl-duration-slow`. Every substitution is exact-value and every removal is an
unused variable, so no rendered element's cascade winner moved; the live
featured gradients, dark override, and all three breakpoints remain. Pinned
Stylelint falls **6,364 → 6,331** (focused Welcome **144 → 111**, all -33 in
hardcoded values), with important, specificity, and duplicate counts unchanged.
Contracts **17/17**, focused Welcome Chromium visual **6/6** update-free,
required Chromium **426/426** (the list grew from 407 as later specs landed), and
pytest **1,738 + 2 catalog known-reds** match the expected gates. All six Windows
Welcome variants pass; all twelve committed Welcome images and every integrity
lock are unchanged. Full visuals reproduce only the exact WP4.0 known reds
(workout-plan desktop-dark 1,039 px; plan-desktop-light-advanced 6,262 px).
Evidence: [`CSS_PHASE4_WP4_3E_EVIDENCE.md`](CSS_PHASE4_WP4_3E_EVIDENCE.md). The
packet shipped to origin/main via PR #160 (squash `5e7d290`, all 14 CI checks
green).

**WP4.3f Session Summary completed 2026-07-19 in isolated
`wt/wp4-3-session-summary-dark-token-cleanup`.** The repeated solid-color
dark-mode, ink, and border literals in the session-summary-only bundle now use
eleven page-local semantic tokens (a `:root` block for the two light tokens and a
`[data-theme='dark']` block for the nine dark tokens, mirroring the WP4.3d
volume-splitter pattern). Distinct roles keep distinct tokens even when values
coincide (`#495057` backs both `--ss-label-ink` light ink and
`--ss-dark-border-strong` dark border, split by CSS property). Pure value-
preserving extraction — no custom property removed, no rule deleted; the shared
volume-badge colors, light striping, glass overlays, and all nine breakpoints
stay untouched. Two hygiene findings were **deferred** (documented, not acted on):
the dead `#weekly-summary-container`/`-table` selector arms (those ids live only
in `weekly_summary.html`, which loads its own bundle) and the two parallel dark
table systems on the shared `.summary-*` classes — both better handled with
WP4.3g Weekly Summary or a shared-frame dedupe. Pinned Stylelint falls
**6,331 → 6,294** (focused Session Summary **183 → 146**, all -37 in hardcoded
values), with important, specificity, and duplicate counts unchanged. Contracts
**18/18**, focused Session Summary Chromium visual **6/6** update-free, required
Chromium **426/426**, and pytest **1,739 + 2 catalog known-reds** match the
expected gates. All six Windows Session Summary variants pass; all twelve
committed Session Summary images and every integrity lock are unchanged. Full
visuals reproduce only the exact WP4.0 known reds (workout-plan desktop-dark
1,039 px; plan-desktop-light-advanced 6,262 px). Evidence:
[`CSS_PHASE4_WP4_3F_EVIDENCE.md`](CSS_PHASE4_WP4_3F_EVIDENCE.md). Shipped to
origin/main via PR. Next is WP4.3g Weekly Summary; wait for explicit direction
before starting it.

**WP4.3g Weekly Summary completed 2026-07-20 in isolated
`wt/wp4-3-weekly-summary-dark-token-cleanup`.** The repeated solid-color
dark-mode, ink, and border literals in the weekly-summary-only bundle now use
eleven page-local `--wk-*` semantic tokens (a `:root` block for the two light
tokens and a `[data-theme='dark']` block for the nine dark tokens), mirroring
the WP4.3f session-summary set — the two bundles were byte-identical for this
region. Distinct roles keep distinct tokens even when values coincide (`#495057`
backs both `--wk-label-ink` light ink and `--wk-dark-border-strong` dark border,
split by CSS property); the substitution is exact-value and self-verified by
`var()`-expansion. The two WP4.3f-deferred findings were resolved: **(a)** the
twelve dead `#session-summary-*` selector arms — those ids render only on
`session_summary.html` — were dropped, each affected rule keeping its live
`#weekly-summary`/class arms so no declaration was lost; **(b)** a browser
computed-declaration-owner audit in both themes across the page's three tables
proved both parallel dark table systems retain live winners (Table 1 governed by
the ID-bearing System-1 rules, Tables 2/3 by System-2 thead-bg/border + odd-row
bg and System-1 striping even-row bg / non-ID row text color, with a shared
components.css rule owning non-ID thead text color), so no whole dark rule is
safely removable — the systems were left intact and documented. The weekly-only
`#isolated_muscles_filter` block and single-use dark literals
(`#252525`/`#2a2a2a`/`#2c3034`/`#b0b0b0`) stay untouched. Pinned Stylelint falls
**6,294 → 6,254** (focused Weekly Summary **184 → 144**: hardcoded values -37,
descending-specificity -3), with important and duplicate counts unchanged.
Contracts **19/19**, focused Weekly Summary Chromium visual **6/6** update-free,
required Chromium **426/426**, and pytest **1,740 + 2 catalog known-reds** match
the expected gates. All six Windows Weekly Summary variants pass; all twelve
committed Weekly Summary images and every integrity lock are unchanged. Full
visuals reproduce only the exact WP4.0 known reds (workout-plan desktop-dark
1,039 px; plan-desktop-light-advanced 6,262 px). Evidence:
[`CSS_PHASE4_WP4_3G_EVIDENCE.md`](CSS_PHASE4_WP4_3G_EVIDENCE.md). Shipped to
origin/main via PR #162 (`bc9da14`).

**WP4.3j-c-dead completed 2026-07-27 in `wt/wp4-3j-c-dead`, cut fresh from
merged `main` at `69dcf5e`.** It deleted the 37 rules the WP4.3j-c audit
nominated but did not authorize: regions D (dark cell glass, 3), E (positional
metric-lane glass, 20), F (dark-mode visibility, 8) and six of the eight
region-G final-override rules — 69 declarations. **Lines 2,025 → 1,621 (−404);
`!important` 285 → 217 (−68); `@media` unchanged at 9.** The scope was
re-resolved structurally by selector shape rather than by the audit's line
numbers, and every claim was re-proven: all 37 rules match live elements and
none ever wins; before vs after **0 computed-value and 0 declaration-owner
differences across 15,336 records**; **6/6 zero-diff** frame captures; same-CSS
control 0 on both sides; matching-rule count −37 per context and 5,496 records
losing candidates as positive controls. The two region-G hover rules are
retained with their winning `filter` declarations, and region H is locked
byte-for-byte by sha256. Gates: visuals **6/6** update-free, contracts
**32/32** (red path proven five ways), focused functional Chromium **33/33**,
pytest **1,858 passed / 1 skipped**; Stylelint total **5,784 → 5,498**, focused
**717 → 431**, `no-descending-specificity` **200 → 38**, no category increased.
Two measured corrections to the audit are recorded (its `!important` projection
of 71 was 68; one of the nine unverified declarations is in region A, not H), as
is a new method rule — *every deadness sweep must carry a known-live control*.
Evidence:
[`CSS_PHASE4_WP4_3J_C_DEAD_EVIDENCE.md`](CSS_PHASE4_WP4_3J_C_DEAD_EVIDENCE.md).
**This deletion had to precede WP4.4:** repairing the shared `:is()` selector
first would have resurrected these rules. **Wait for explicit direction before
the next packet.**

**WP4.3j-d-hover-paint completed 2026-07-27 in
`wt/wp4-3j-d-hover-paint`, cut fresh from merged `main` at `c29b05f`.** It
removed exactly four cascade-dead declarations from the two retained Region G
hover rules: light/dark `background` and `box-shadow`. Both complete selector
lists and both winning filters are byte-identical. A real mouse-hover audit
compared **11,016 records** across six contexts: **0 computed-value differences,
0 declaration-owner differences, and 6/6 byte-identical frames**. Known-live
filter controls passed 6/6 before and after; **408 records lost candidates and 0
gained any**. The Region H contract's defective first-occurrence anchor was
corrected to its unique 282-line banner span. Gates: visuals **6/6** update-free,
contracts **33/33**, focused functional Chromium **33/33**, pytest **1,859
passed / 1 skipped**; Stylelint total **5,498 → 5,490**, focused **431 → 423**,
no category increased. Evidence:
[`CSS_PHASE4_WP4_3J_D_HOVER_PAINT_EVIDENCE.md`](CSS_PHASE4_WP4_3J_D_HOVER_PAINT_EVIDENCE.md).
**Wait for explicit direction before further Workout Log cleanup.** WP4.4 is
separately authorized at Gate 1 — see the section below.

**WP4.3h User Profile and the WP4.3i Workout Plan dead-CSS arc followed and are
complete through WP4.3i-filter-btn (`cb5ff6e`).** Their per-packet evidence docs
are `CSS_PHASE4_WP4_3H_EVIDENCE.md` and `CSS_PHASE4_WP4_3I_EVIDENCE.md` plus
`_B`/`_C`/`_D`/`_E`/`_F`/`_G`, `_DEAD`, and `_FILTER_BTN`. The current-status
section at the top of this document carries the commit ladder, gates, the
animated-logo known red, and the next-state constraints; `docs/MASTER_HANDOVER.md`
carries the narrative. **Wait for explicit direction before the next packet.**

### WP4.4 Shared bundles, navbar, and `theme-dark.css`

> **Superseded as the executable specification.** WP4.4 Plan v2 in
> [`docs/css_phase4_wp4_4/PLANNING.md`](css_phase4_wp4_4/PLANNING.md) is
> **Gate-1 approved (owner, 2026-07-27, rulings N1–N10)** and is the plan that
> executes. The bullets below remain as the original scope statement and the
> prerequisite record; where they differ from Plan v2, Plan v2 wins.
>
> **Authorized sequence, as directed by the owner on 2026-07-29 — SEQUENTIAL,
> one packet / worktree / writer / PR at a time:**
>
> ```
> a ✔ → c ✔ → b ✔ → e ✔ → d1 ✔ → f1 ✔ → d2 ✔ → f2 ✔ → g → h → HARD STOP
> ```
>
> **The arc stops after `h`** for the N4 owner checkpoint. Gate 1 authority does
> **not** extend to `i`; `j` and `k` wait until `i` is approved, narrowed, or
> abandoned. The serial order narrowed Plan v2 §4 (which classifies `e`, `d1`
> and `f1` as concurrency-eligible class (a)) rather than contradicting it. The
> pure-deletion run is now **finished**: every class (a) packet has shipped, and
> `f1` was deliberately last because navbar layering, global exposure and the
> animated-logo oracle made it the riskiest.
>
> **WP4.4-a is COMPLETE** — PR #187, squash `46e340e`, read-only, no production
> CSS changed.
>
> **WP4.4-c is COMPLETE** — PR #188, squash `1b13bfc`, merged 2026-07-28. It
> deleted the three cascade-dead paint declarations from `.is-success` while
> retaining the `success-pulse` animation, and corrected the Packet-a baseline
> contract to verify the seven surfaces at the baseline's own `sourceCommit`
> (plus an ancestry assertion, so a pin to an unreachable pre-squash commit
> reds instead of dying on a fresh clone).
>
> **WP4.4-b is COMPLETE** — PR #192, squash `3bec677`, merged 2026-07-29. Pure
> deletion of four dead `base.css` rule blocks (−44 lines): `.skeleton`, beaten
> by `motion.css` at equal specificity, and the three unreachable classes
> `.loading-spinner`, `.fade-enter`, `.fade-enter-active`. All 12 `:root` custom
> properties retained and contract-pinned under M9. Stylelint **−2**, no rule
> increased; full pytest **2,204 / 1 skipped**; visual **65 / 1 ledgered red**.
>
> **WP4.4-e is COMPLETE** — PR #195, squash `1346a35`, merged 2026-07-29. Pure
> deletion of **34 unreachable rule blocks from `layout.css` (−218 lines, 0
> insertions)**. The plan carried one candidate (`body.dark-mode`); the audit
> found **42** fully-unreachable rules. `body.dark-mode` was re-proved and
> deleted on **unreachability**, not the ordinary non-winner rule — it declares
> only custom properties, whose live definitions in `[data-theme="dark"]` are
> retained and contract-pinned. 0 declaration-owner differences across 64,961
> records; Stylelint 2,875 → 2,857 (−18); `!important` 24 → 24; `@layer` 0 → 0.
>
> **`e` deferred nine rules** — the `.tbl-show-*` / `.tbl-hide-*` family. Three
> members declare `display: block`, a bare div's initial value, so no control
> element can distinguish them. Pinned by exact occurrence count; delete as a
> unit under fresh evidence or not at all.
>
> **WP4.4-d1 is COMPLETE** — PR #197, squash `59e5b10`, merged 2026-07-29.
> Pure deletion of **14 rule blocks from `a11y.css` (−99 lines, 0 insertions)**:
> a *superseded generation* of the scale / accessibility UI, leaving the live
> compact generation intact. Full-selector census 0 for all 14 across 164
> contexts; oracle validity gate passed first (live generation 160/160).
> `!important` **51 → 51**, custom properties 17 → 17, `@layer` 0 → 0.
>
> **WP4.4-f1 is COMPLETE** — PR #199, squash `1127486`, merged 2026-07-29.
> Pure deletion of **one rule from `navbar.css` (−6 lines, 0 insertions)**:
> `body:not(:has(#navbar)) .navbar`, unreachable **by construction** —
> `navbar.css` is linked only from `base.html:22`, which renders `#navbar`
> unconditionally, so the guard is unsatisfiable in every document that loads
> the file. Census agreed at 0/522 contexts. `!important` **93 → 93**, custom
> properties 72 → 72, `@layer` blocks 1 → 1, layered rules 103 → 103.
>
> The plan projected −150 to −400 lines; `f1` delivered −6, and that is the
> correct outcome — a projected line reduction is not an acceptance criterion.
>
> **WP4.4-d2 is COMPLETE** — PR #201, squash `0a912d9`, merged 2026-07-29.
> Every one of the 51 `!important` annotations left in `a11y.css` was
> adjudicated. Exactly one shipped: `.is-invalid { box-shadow }` remains
> present and remains the same effective owner, but no longer needs priority
> `important`. `!important` **51 → 50**; declarations **240 → 240**, style
> rules **94 → 94**, custom properties **17 → 17**, `@layer` **0 → 0**.
>
> A second census nomination,
> `.selection-field.has-validation-error label { color }`, failed targeted
> certification and was retained. The census synthetic never constructed the
> doubly-matched label; an exact-structure declaration-owner probe found an
> owner transfer to the later `pages-workout-plan.css:4449` rule in 15/15
> light-mode measurements. Census results therefore remain nominations until a
> declaration-owner adjudicator exercises the exact competing structure.
>
> `d2` also proved the CSS-only M6a suppressor beatable by layered
> `!important` and by more-specific unlayered `!important`. Its packet oracle
> settled `CSSTransition` objects through the Web Animations API and proved the
> CTLF red path; `scripts/css_audit/runtime_probe.mjs` remains unfixed and may
> not be treated as transition-safe. Gates: contracts 22/22 with every red path
> proven, pytest 2,268/1 skipped, nine specs 127 passed, visual 65/1 ledgered
> red inside the known band, Stylelint −1, all 14 PR checks green.
>
> **WP4.4-f2 is COMPLETE** — PR #205, squash `6a5465c`, merged 2026-07-30.
> It consolidated three exact duplicate `navbar.css` source rules into existing
> generation owners. Style rules **193 → 190**, declarations **692 → 690**,
> physical lines **1,536 → 1,533**. The sole `@layer navbar` block remains
> source-pinned at lines 6–883; all 93 `!important` occurrences, all 72
> custom-property declarations, layer membership, and `--nav-gap` /
> `--nav-padding-y` / `--nav-padding-x` are unchanged.
>
> Exact owner controls proved the merged scrollbar and light-theme toggle
> background live, mobile container `max-width` and row gap live, and the
> desktop base `max-width` overridden. The post matrix had **486/486**
> candidate, restore and focus checks green. M6a used a genuinely transitioned
> known-live control and settled 7 `CSSTransition` objects outside the cascade;
> `--no-settle` failed as required. Gates: contracts 62 passed, pytest
> 2,271/1 skipped, required functional/navigation/accessibility Chromium 127
> passed plus `fatigue.spec.ts` 8 passed, visual 65/1 at 875/882/875 inside the
> known band, Stylelint −5 across the seven surfaces, all 14 PR checks green.
>
> **The "three live generations" count this section asserted is now
> established rather than assumed**, and is confirmed at exactly three: layered
> scoped (103 rules), legacy `.navbar` fallback (2), unlayered override tail
> (89), plus 5 `@keyframes` steps. **Generation B is not dead legacy** — its
> `.navbar` rule is unlayered while `#navbar { position: sticky }` sits inside
> `@layer navbar`, so the unlayered class selector wins and `position: fixed` is
> what the browser computes. The file's own comments at `:885` and `:893` say
> the opposite and must not be trusted.
>
> **`f2` disposition:** the 155 f1 matched-but-never-winning nominations remain
> uncertified and retained. Only three exact, owner-proven duplicate structures
> were consolidated; the remaining near-duplicate `@media` conditions were not
> chased.
>
> The `c`-before-`b`/`d1`/`e`/`f1` prerequisite is **discharged**. **`g` is
> next.** `a`, `c`, `b`, `e`, `d1`, `f1`, `d2` and `f2` must not be
> re-dispatched.
>
> **Method rule M6a is binding on every remaining packet** (Plan v2 §2b):
> suppress transitions before applying, reading **and** removing a sentinel — a
> transitioned property reads back its pre-sentinel value and reports a live
> declaration as dead. `d2` strengthens the rule: a CSS-only universal
> `transition: none !important` is itself beatable, so the oracle needs a
> transitioned known-live control and a settlement mechanism outside the
> cascade.
>
> **Packet-a corrections that supersede this section's projections** (Plan v2
> C1–C8): the `:is()` family specificity range is **(1,3,0)–(1,5,3)**, not
> (1,3,1)/(1,3,2), across **17 rules** from 19 `:is(` tokens; the visual matrix
> is **66** tests per platform, not 60; `templates/error.html` is **not
> reachable by a 404** (`app.py:194` returns an inline document with no
> stylesheet), so no packet may treat a bad URL as exercising it; seven-surface
> Stylelint is **2,883** with `components.css` at **1,989**; V4's 86/8
> thresholds were global WP4.1 figures and are **26/2** here. The **eleven**
> inherited Linux `desktop` reds — spanning two spec files, corrected from ten
> under proposal P1 — and the eight uncertifiable Welcome elements are
> ledgered in
> [`CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`](CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json)
> — **do not rebaseline the reds**, and **no packet may classify a declaration
> affecting those eight elements as dead using the rest-state harness.**

- **Prerequisite discharged 2026-07-27.** The `components.css` `:is()` arm that
  exports ID-level specificity is why four generations of page-local Workout Log
  table styling were dead. Repairing that selector would have *resurrected* them,
  so WP4.3j-c-dead deleted the dead rules first and WP4.3j-d removed the four
  dead hover-paint declarations from the retained Region G rules. Regions A, B
  and C on that page remain page-local and ID-free, so a selector repair still
  changes what they own — re-measure before assuming otherwise.
- Handle base/layout/components/a11y/motion separately from navbar/theme.
- Triage navbar's three live generations rule by rule.
- Triage `theme-dark.css` into legacy values versus legitimate token remaps; do not bulk
  delete it.
- Final goal: theme file contains only justified token swaps or is removed after proof.
- Gate: full visual deep gate, dark-mode, nav-dropdown, accessibility, summary-pages.

### Phase-4 success metrics

- Zero unjustified visual diffs from the WP4.0 ledger.
- No increased maximum specificity or unexplained `!important` count.
- Duplicate-selector/declaration counts decrease monotonically after the measure baseline.
- Total hand-maintained CSS reduction: 30% required target, 40% stretch target. Line count
  is secondary to ownership, cascade safety, and visual equivalence.

---

## Continuous track — pyright baseline burn-down

- One file or tightly coupled diagnostic family per WP.
- Type-only changes; no behavior refactors disguised as typing fixes.
- Baseline diagnostic multiset may only shrink; regenerate with the existing script when
  removals are intentional.
- Gate: zero net-new diagnostics, lower count, focused tests, then full pytest.

---

## Execution order and phase gates

| Order | Track/phase | Prerequisite | Close gate |
|---|---|---|---|
| 1 | Track A safe bug fixes | owner approval of behavior-changing track | focused regression + full pytest/E2E union |
| — | Track B owner-decided changes (WPB.1–WPB.9) | per-WP prerequisites in Track B; interleaved with phases, not a block | per-WP gate + migration notes in every PR |
| 2 | Phase -1 evidence/docs/tests | scan docs merged | `/verify-suite`; live DB unchanged |
| 3 | Phase 0 dead code/hygiene | hermetic baseline | `/verify-suite` + pyright baseline diff |
| 4 | Phase 1 route boundaries | Phase 0 import cleanup | `/verify-suite` + API integration |
| 5 | Phase 2 Python structure/schema | Phase 1; schema WP last | `/verify-suite` + backup/fresh-DB/erase smokes |
| 6 | Phase 3 JS | Vitest scaffold; may overlap Python only in isolated worktrees | Vitest + `/verify-suite` |
| 7 | Phase 4 CSS | WP3.2 scripts stable; WP4.-1/0a/0 complete | both-platform visual deep gate + functional frontend |

At every phase close, update `docs/MASTER_HANDOVER.md`, the verified-count block in
`CLAUDE.md`, and this plan's status. Do not mark a phase complete while follow-up contract
decisions are silently outstanding; either resolve them or leave them explicitly deferred.

## Sign-off checklist

- [x] v1 council findings retained or superseded explicitly.
- [x] Full scan completed at `scan/codebase-grounding@a6574b9`.
- [x] Scan recommendations reviewed rather than copied verbatim.
- [x] Behavior-changing bugs separated from behavior-preserving refactors.
- [x] Prior review gaps incorporated: visual page coverage, static-fetch carve-outs,
  schema force semantics, durable goldens, import characterization, realistic WP sizing,
  and parallel isolation.
- [x] Scan evidence merged into the implementation branch (2026-07-04; WP-1.0).
- [x] Owner decisions OD1–OD10 recorded (2026-07-04; see §3).
- [x] OD follow-ups drafted as Track B work packets WPB.1–WPB.9 (2026-07-04).
- [x] Owner approves Track A execution (2026-07-04).
- [x] Owner approves Track B execution (behavior + contract changes) (2026-07-04).
- [x] Owner approves Plan v3 for refactor execution (2026-07-05).

---

## Owner review status table — not for agents or LLMs

> **Owner-review aid only.** This table is for the human owner to review progress.
> It is **not** an instruction set, execution queue, authorization to start work,
> or source for autonomous dispatch by agents or LLMs. Agents and LLMs must use
> the detailed work-packet requirements above and wait for explicit owner
> direction wherever the plan requires it.

Snapshot: **2026-08-01 (latest)**. **WP4.4 is complete and the arc is closed at
`k`.** Every packet `a` through `k` is merged — the tail being `i` (#212,
`5f7b5ac`) with its oracle corrective (#215, `666471e`), `j` (#216, `47c7687`)
and `k` (#217, `c521d3a`). **No packet in this arc is next.** Of the three
closeout proposals, **P1 (#223, `d543a4b`) and P2 (#222, `4b0670b`) are
owner-approved and merged**; **P3** (`theme-dark.css` `:where()` inertia) is
**planning only** with Gate 0 and Gate 1 both unsigned — see
[`css_theme_dark_p3/PLANNING.md`](css_theme_dark_p3/PLANNING.md). The older
packet counts/status prose immediately below is retained as historical detail.

> **Superseded 2026-08-01.** This snapshot previously read *"Snapshot:
> 2026-07-31 (latest) … **WP4.4-i is active** and j/k are authorized
> sequentially"*. Correct on 2026-07-31; stale once the tail merged.

> **Superseded snapshot detail (2026-07-30).** **Eight of eleven WP4.4 packets are merged.**
**WP4.4-a** (PR #187, squash `46e340e`) produced evidence and audit tooling, not
a production CSS edit. **WP4.4-c** (PR #188, squash `1b13bfc`) was the arc's
first production CSS deletion. **WP4.4-b** (PR #192, squash `3bec677`) deleted
four dead `base.css` rule blocks. **WP4.4-e** (PR #195, squash `1346a35`)
deleted 34 unreachable `layout.css` rule blocks, −218 lines. **WP4.4-d1**
(PR #197, squash `59e5b10`) deleted a superseded scale/menu generation from
`a11y.css`, −99 lines. **WP4.4-f1** (PR #199, squash `1127486`) deleted the
unreachable legacy fallback rule from `navbar.css`, −6 lines. **WP4.4-d2**
(PR #201, squash `0a912d9`) de-weighted one certified `a11y.css` annotation
and retained 50. **WP4.4-f2** (PR #205, squash `6a5465c`) consolidated three
exact duplicate `navbar.css` source rules with layer membership and importance
unchanged. **`a`, `c`, `b`, `e`, `d1`, `f1`, `d2` and `f2` are DONE and must
not be re-dispatched.**

The current remaining order is sequential — one packet, worktree, writer and PR
at a time: `i` → `j` → `k`. Parallelism is read-only analysis/review within a
packet; stateful gates and writes remain serialized.
The continuous pyright burn-down is a standing track, not an active packet or
branch.

| Area / packet | Owner-review status | What has been done / current boundary | Why it is not started, deferred, or gated |
|---|---|---|---|
| Owner decisions and plan approval | **Done** | OD1–OD10 are resolved; Track A, Track B, and Plan v3 approvals are recorded. | — |
| Track A — A1–A8 bug fixes | **Done** | All eight fixes shipped in PRs #91–#98 with the integrated test and E2E gates passing. | — |
| Track B — WPB.1–WPB.3 and WPB.5–WPB.9 | **Done** | All owner-decided behavior/contract packets except WPB.4 shipped, including the required fatigue-context CI job. | — |
| Track B — WPB.4 `Unassigned` weekly-summary bucket | **Gated / not started** | The owner decision and risk-mitigation gate are documented; WP2.3 supplied the prerequisite goldens, but no WPB.4 implementation has started. | Protected calculation behavior still requires explicit product-risk review, a decision about the `global_sessions` denominator, intentional golden-delta review, and the named summary functional/visual gates. |
| Phase -1 — evidence, docs, and gate hardening | **Done** | WP-1.0–WP-1.5 shipped. | — |
| Phase 0 — dead code and repository hygiene | **Done** | Phase 0 is closed under the plan’s top-level status. | — |
| Phase 1 — route and service boundaries | **Done** | WP1.1–WP1.8 shipped in PRs #121–#130 while preserving endpoint and response contracts except for separately approved Track B changes. | — |
| Phase 2 — Python structure and schema ownership | **Done** | Phase 2 is closed; this includes the schema registry, duplication registry, protected decompositions, and WP2.2 plan-generator work. | — |
| Phase 3 — JavaScript characterization, extraction, and transport | **Done** | The core JS track is closed; optional WP3.6 was also completed and committed. | — |
| Phase 4 foundation — WP4.-1 through WP4.2 | **Done** | Cascade/load-order foundation, selector hardening, known-red ledger, token consolidation, and shared-frame ownership work are complete. | — |
| WP4.3 page packets completed to the current boundary | **Done** | WP4.3a–WP4.3h are complete; the Workout Plan arc is complete through WP4.3i-filter-btn; Workout Log is complete through WP4.3j-d-hover-paint. WP4.3j-b and WP4.3j-c were audit-only packets, and their authorized deletion follow-ups shipped. | — |
| Workout Plan — 10 deferred interaction-state declarations | **Deferred / gated** | The declarations were investigated and intentionally retained; the existing contract asserts their presence. | Animated interaction states made the deadness oracle unstable. Removal requires animation stabilization and a same-CSS control that reaches zero differing records. |
| Workout Plan — remaining raw-literal/token extraction and `!important` weighting | **Not started / owner-gated** | No implementation packet has started. | The remaining work is redesign-sized and multi-packet; literal removal alone is not sufficient justification. It requires explicit owner direction and a protected visual/cascade plan. |
| Workout Plan — WP4.3i-jm and WP4.3i-o | **Closed / do not resume** | Both investigations were attempted and deliberately left uncommitted. | Their premises did not justify a safe change. They must not be re-dispatched; the detailed reasons remain in `docs/MASTER_HANDOVER.md`. |
| Workout Log — cleanup beyond WP4.3j-d-hover-paint | **Not started / owner-gated** | Work is paused at the completed j-d boundary; retained regions and unverified declarations remain protected by the recorded contracts. | Further cleanup needs a newly scoped packet, explicit owner direction, and fresh cascade/visual measurement. A shared-selector change can alter page-local ownership, so prior deadness findings cannot be generalized. |
| WP4.4-a — shared-surface baseline and cascade harness | **Done** | Merged via PR #187 (squash `46e340e`), read-only, no production CSS changed. Delivered the pinned baseline JSON, the committed harness under `scripts/css_audit/`, nine red-path-proven contracts, and `/fatigue` visual baselines on both platforms under N7. Harness self-checks 22/22; M4 resolution check 9,842 pairs / 0 inversions. | — |
| WP4.4-c — `motion.css` dead success paint | **Done** | Merged via PR #188 (squash `1b13bfc`, 2026-07-28). Deleted the three cascade-dead `.is-success` paint declarations, retaining `success-pulse`; ownership resolved over `CSS.getMatchedStylesForNode` across 11 routes × 2 themes under both `prefers-reduced-motion` states, 0 motion-record differences. Also re-pinned the Packet-a baseline contract to its own `sourceCommit` and added the ancestry assertion. | — |
| WP4.4-b — `base.css` four dead rule blocks | **Done** | Merged via PR #192 (squash `3bec677`, 2026-07-29). Pure deletion, −44 lines: the `.skeleton` block beaten by `motion.css` at equal specificity, plus the three unreachable classes `.loading-spinner`, `.fade-enter`, `.fade-enter-active`. All 12 `:root` custom properties retained and contract-pinned under M9. Packet contracts 8 passed; full pytest 2,204 / 1 skipped; five required specs 68 passed; visual 65 passed / 1 ledgered known red; Stylelint −2, no rule increased. | — |
| WP4.4-e — `layout.css` unreachable rule blocks | **Done** | Merged via PR #195 (squash `1346a35`, 2026-07-29). Pure deletion of **34 rule blocks, −218 lines, 0 insertions**: the `.tbl-col-chooser*` widget (10), `.form-container` (9), `.input-frame .row` (6), `.el-clip`/`.col--*` (3), `.tbl--loading` + `::after` + orphaned `@keyframes tbl-spin` (3), `.sr-only`, standalone `.tbl-toolbar`, `body.dark-mode`. Census 0 on the full selector across 11 routes × 2 themes × 16 widths; 0 declaration-owner differences / 64,961 records; contracts 13 passed with 13/13 red-path proven; pytest 2,230 / 1 skipped; seven required specs 89 passed; visual 65 / 1 ledgered red; Stylelint 2,875 → 2,857 (−18); `!important` 24 → 24; `@layer` 0 → 0. | — |
| WP4.4-d1 — `a11y.css` superseded scale/menu generation | **Done** | Merged via PR #197 (squash `59e5b10`, 2026-07-29). Pure deletion of **14 rule blocks, −99 lines, 0 insertions**: `.scale-control`, `.scale-control-label`, `.scale-btn-group`, `.scale-labels`, `.scale-label`, `.accessibility-menu`, `.accessibility-section*` and their `@media` overrides. The live compact generation (`.scale-control-compact`, `.scale-btn-compact`, `.scale-indicator`) is retained and contract-pinned. Full-selector census **0 for all 14 across 164 contexts** (2 themes × 10 widths × 8 `data-scale` levels + print + reduced-motion); **oracle validity gate passed first** (live generation census > 0 in 160/160). Residual `.scale-control` matches attributed by CDP to the **retained** `@media print` rule at source lines 329–331; **0** rules on `screen`. Contracts 16 passed with **15/15 red-path proven**; pytest 2,245/1 skipped; nine specs 127 passed; visual 65/1 ledgered red; Stylelint 2,857 → 2,851 (−6). `!important` **51 → 51**, custom properties 17 → 17, `@layer` 0 → 0. | — |
| WP4.4-d2 — `a11y.css` `!important` re-weighting | **Done** | Merged via PR #201 (squash `0a912d9`, 2026-07-29). Adjudicated all 51 annotations: `.is-invalid { box-shadow }` certified and de-weighted; 50 retained. The C50 census nomination failed targeted exact-structure certification because ownership moves to `pages-workout-plan.css:4449` in 15/15 light measurements despite the same computed value. `!important` 51 → 50; declarations/rules/custom properties/layers unchanged. Contracts 22 passed with 22/22 red paths proven; pytest 2,268/1 skipped; nine specs 127 passed; visual 65/1 ledgered red; all 14 CI checks green. | — |
| WP4.4-f2 — `navbar.css` generation consolidation | **Done** | Merged via PR #205 (squash `6a5465c`, 2026-07-30). Consolidated three exact duplicate source rules: layered scrollbar declarations, layered dark-toggle defaults, and identical-match-set calm container declarations. Style rules 193 → 190; declarations 692 → 690; lines 1,536 → 1,533. The sole layer remains at lines 6–883; all 93 `!important` occurrences, 72 custom-property declarations and pinned nav variables are unchanged. Exact owner matrix 486/486 green; genuine M6a control settled 7 transitions; contracts 62; pytest 2,271/1; required Chromium 127 + fatigue 8; visual 65/1 inside the band; Stylelint −5; all 14 CI checks green. | — |
| WP4.4 — shared bundles through `h` | **Done** | `g` merged in #207 (`4b7ca58`), its terminology correction in #209 (`a895cb0`), and `h` in #208 (`b2b1cb7`). PR #211 (`1019d34`) then corrected the visual harness prerequisite without snapshots or effective-render change. | Do not re-dispatch. The g/h zero-winner-versus-removal lesson remains binding. |
| `a11y.css` bare `.scale-btn` rules | **Recorded by `d1` / not audited / gated** | 11 exact-token occurrences. Runtime census is **0** — `accessibility.js:144` and `:202` query an empty set, a second dormant JS path beside the accessibility dropdown. `d1`'s static pass wrongly treated that JS *query* as proof of reachability, so these rules were **never audited as candidates** and are retained untouched. | Deleting them requires its own census, its own oracle-validity control and its own packet. A JavaScript query is not evidence of reachability. |
| `layout.css` `.tbl-show-*` / `.tbl-hide-*` breakpoint helpers | **Deferred by WP4.4-e / gated** | Nine rules. Census 0 and six of nine are visible to the synthetic oracle, but three declare `display: block` — a bare div's initial value — so no control element can distinguish them and their post-deletion flip cannot be demonstrated. Pinned by exact occurrence count in `tests/test_css_wp4_4_layout_contracts.py`. | Splitting the family would leave `@media` overrides targeting classes with no base rule. It must be deleted as a **unit** under fresh evidence, never eroded rule by rule. |
| WP4.4-i — shared `:is()` selector repair | **Active / N4 approved** | Existing worktree and WIP checkpoint are recorded in the execution handoff. The owner approved the CSS-local split-list, branch-safe narrow-or-abandon shape and bounded contract/Stylelint exceptions. | Finish only from fresh post-#211 evidence. True G3 before comes from current main and after from i; artifact names do not establish provenance. |
| WP4.4-j — `theme-dark.css` triage | **Authorized after i resolves** | Not started; arrange its isolated checkout from merged post-i main through the external worktree workflow. | Preservation-only: retain uncertified/custom-property/JS-state work, accept a no-op, no rebaseline or visible change. |
| WP4.4-k — final integration | **Authorized after j merges** | Not started; docs/verification only. | N10 stays evidence-only; do not edit `QUALITY_GATE.md`. Corrective subpackets are limited by the continuation authority. |
| Superset dark tint and `layout.css` dead `body.dark-mode` | **`body.dark-mode` RESOLVED by WP4.4-e; superset tint still deferred** | `body.dark-mode` was re-proved and **deleted** in PR #195. The rule was *functional* (all seven `--tbl-*` tokens changed in 11/22 contexts when the class was applied) but its selector was *never satisfied*: `<body>` never carries the class and `darkMode.js:64` sets `data-theme` on the root element. Deleted on **unreachability**, explicitly **not** the ordinary non-winner rule, which does not apply to custom properties. The seven tokens keep their live `[data-theme="dark"]` definitions, now contract-pinned. The missing live dark override for `--superset-bg-1..4` remains recorded and unchanged. | The superset tint belongs to `theme-dark.css` ownership (packet `j`), still gated. |
| Continuous pyright baseline burn-down | **Ongoing — standing track only** | The track remains available for one file or one tightly coupled diagnostic family at a time; no active packet is identified by this snapshot. | It has no single phase-close packet. Each change must remain type-only, reduce the diagnostic multiset, and pass focused plus full pytest gates. |
| Overall refactor plan | **Partially complete; WP4.4-i active** | Track A and Phases -1 through 3 are complete; Track B is complete except WPB.4; WP4.4 continues under the dated N4 authority through i → j → k. | WPB.4 and remaining Workout Plan/Log cleanup stay paused. The 235 layer-pin declarations remain deferred. |
