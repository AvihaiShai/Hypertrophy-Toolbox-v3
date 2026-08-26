# UI Scenarios Gap Analysis - Current State and Remaining Risks

> **Date**: January 2025  
> **Updated**: April 24, 2026
> **Purpose**: Track UI risk scenarios, confirm what is already implemented, and highlight only the remaining gaps.
> **Current Scope (Locked)**: Single-user, local runtime, single-tab usage mode.

## ✅ IMPLEMENTATION STATUS (Verified)

### E2E Test Suites Present
| Test File | Scope | Status |
|-----------|-------|--------|
| [e2e/error-handling.spec.ts](../e2e/error-handling.spec.ts) | Server errors, network failures, duplicate-click prevention, retry/recovery paths | ✅ Present |
| [e2e/validation-boundary.spec.ts](../e2e/validation-boundary.spec.ts) | Negative values, rep ranges, zero values, RIR/RPE limits | ✅ Present |
| [e2e/superset-edge-cases.spec.ts](../e2e/superset-edge-cases.spec.ts) | Link/unlink/delete/replace/persistence behavior for supersets | ✅ Present |
| [e2e/empty-states.spec.ts](../e2e/empty-states.spec.ts) | Empty exports, empty log flows, empty filters/states | ✅ Present |
| [e2e/browser-navigation-state.spec.ts](../e2e/browser-navigation-state.spec.ts) | Stateless contract for routine cascade (`back`, `refresh`, deep-link query ignore) | ✅ Present |
| [e2e/replace-exercise-errors.spec.ts](../e2e/replace-exercise-errors.spec.ts) | Replace-exercise error toasts (`no_candidates`, `duplicate`, `missing_metadata`) | ✅ Present |
| [e2e/nav-dropdown.spec.ts](../e2e/nav-dropdown.spec.ts) | Navbar dropdown and Backup Center navigation | ✅ Present |
| [e2e/program-backup.spec.ts](../e2e/program-backup.spec.ts) | Backup Center save, restore, delete, metadata, and safety flows | ✅ Present |
| [e2e/visual.spec.ts](../e2e/visual.spec.ts) | Deterministic visual regression coverage across routes, themes, and viewports | ✅ Present |

### Code Fixes Verified
| File | Fix | Status |
|------|-----|--------|
| [exercises.js](../static/js/modules/exercises.js) | Debounce guard on `addExercise()` | ✅ Implemented |
| [exercises.js](../static/js/modules/exercises.js) | Duplicate-delete protection on `removeExercise()` | ✅ Implemented |
| [exercises.js](../static/js/modules/exercises.js) | Client-side validation (rep range, negative values, RIR/RPE limits) | ✅ Implemented |
| [exports.js](../static/js/modules/exports.js) | Empty-state checks before export actions | ✅ Implemented |
| [weekly_summary.py](../routes/weekly_summary.py), [session_summary.py](../routes/session_summary.py) | Forward `raw_total_reps` + `raw_total_volume` in summary API payloads | ✅ Implemented |
| [weekly_summary.html](../templates/weekly_summary.html), [session_summary.html](../templates/session_summary.html) | Raw mode display uses raw totals (`raw_total_volume` / `raw_total_reps`) | ✅ Implemented |
| [weekly_summary.html](../templates/weekly_summary.html) | Renamed `Frequency` to `Routines` with clarifying tooltip | ✅ Implemented |
| [weekly_summary.html](../templates/weekly_summary.html), [session_summary.html](../templates/session_summary.html) | Hide isolated-muscles section when data is empty (`{% if isolated_muscles %}`) | ✅ Implemented |
| [weekly_summary.html](../templates/weekly_summary.html), [session_summary.html](../templates/session_summary.html) | Added collapsible "How it's calculated" explainer block | ✅ Implemented |
| [volume_classifier.py](../utils/volume_classifier.py) | Standardized `Excessive Volume` label + removed duplicate tooltip-map key | ✅ Implemented |

---

## Current Findings Status

### Fixed

- Raw vs effective totals on the summary pages were corrected and verified.
- Summary-page wording and label mismatches called out in earlier reviews were fixed.
- The previously missing focused E2E regressions for navigation, replace-exercise failure cases, and empty/error paths are present.

### Intentional / documented behavior

- The product scope is still intentionally single-user, local, and single-tab.
- Routine-cascade browser navigation is documented and tested as a stateless contract, not as a state-preserving flow.
- `weight = 0` remains allowed for bodyweight-style entries; negative values are still invalid.

### Accepted / deferred

- Multi-tab conflict handling remains backlog-only under the current operating model.
- Medium-risk UX hardening items such as toast stacking, form-state persistence, and modal keyboard polish remain open quality work, not release blockers.
- The concise "Known Issues / Reported Bugs" map now exists in [§0](#0-known-issues--reported-bugs); keep it current as new real reports appear.

---

## Executive Summary

Most high-risk gaps from the original analysis are now addressed in both code and E2E coverage.

April 24, 2026 docs refresh:
1. Confirmed the Backup Center, navbar dropdown, and visual regression specs are part of the live E2E inventory.
2. Confirmed the Calm Glass redesign execution docs are no longer active; current styling ownership is tracked in `CSS_OWNERSHIP_MAP.md`.
3. Kept the remaining medium-risk UX items below as backlog-quality work rather than release blockers.

Latest completed work (February 28, 2026):
1. Fixed Raw-mode summary display path by forwarding and rendering raw totals in both Plan Summary and Session Summary.
2. Standardized volume labels to `Excessive Volume` across summary surfaces.
3. Renamed plan metric header to `Routines` for semantic accuracy.
4. Hid isolated-muscles section when no isolated mappings are available.
5. Added compact, expandable "How it's calculated" guidance in both summary pages.
6. Re-ran targeted verification: summary unit/route tests and summary-page E2E spec all passing.

The highest-value remaining work is now (non-blocking):
1. ✅ **Done (2026-05-21)** — Added concise "Known Issues / Reported Bugs" map in [§0](#0-known-issues--reported-bugs).
2. ✅ **Done (2026-05-21)** — Hardened medium-risk smoke assertions (toast stacking, form-state persistence, modal keyboard/focus) in `e2e/ui-hardening.spec.ts`.
3. Keep multi-tab conflict handling out of current release scope (backlog only).

Document corrections made in this revision:
1. Removed stale "must do" items that are already implemented.
2. Corrected outdated matrix rows that claimed missing E2E suites now present.
3. Resolved `weight = 0` contradiction: current logic allows `0` (bodyweight use case), while still rejecting negative values.

---

## 0. KNOWN ISSUES / REPORTED BUGS

> **Purpose**: Real, locally reproduced or owner-reported issues — separated from theoretical risk in §1–§4. Each row is something a future change must not silently regress. An empty *Status* cell and an explicit **Open** both mean the issue is open — newer rows state it rather than leaving the cell blank; *Mitigated* means we have an assertion guarding against further drift.

| ID | Surface | Symptom (reproduce) | Severity | Status | Notes |
|---|---|---|---|---|---|
| KI-001 | Filter cache (formerly `utils/filter_cache.py`) | TTL-only invalidation risk: stale filter options *could* persist up to 1 hour after exercise data changes. `invalidate_cache()` was defined but never called. | 🟡 Medium | ✅ Resolved 2026-05-23 (deletion) | Triage on 2026-05-23 found the module was dormant: zero production callers, never warmed at startup, no HTTP catalogue-mutation path. Both `utils/filter_cache.py` and `tests/test_filter_cache.py` were deleted along with the latent SQLi exposure on the un-validated `f"SELECT DISTINCT {column} FROM {table}"`. WPB.6 later removed the unused `routes/filters.py::get_unique_values` endpoint; the live `routes/workout_plan.py::fetch_unique_values` wrapper continues to use `DatabaseHandler` through `utils.filter_values.fetch_filter_values`. |
| KI-002 | `e2e/nav-dropdown.spec.ts:117` (1440×900) | Dark-mode toggle was off-viewport at default desktop width; fixed with compact desktop navbar utility chrome and a real Playwright click assertion. | 🟢 Low | ✅ Resolved 2026-06-11 | `nav-dropdown.spec.ts` is promoted to required functional E2E coverage. |
| KI-003 | `e2e/program-backup.spec.ts:79` | **Was**: sequential-DB-pollution flake during full Playwright runs; passed in isolation. | 🟢 Low | ✅ Resolved by CI isolation | The backup suite runs as **`E2E Backup (Chromium, isolated)`**, a **required** branch-protection context on a fresh server against a throwaway DB, so the sequential pollution that caused the flake cannot occur in the gate. The historical flake is retained for context: investigated against the 2026-05-10 baseline. |
| KI-004 | Toast (`templates/base.html:236`, `static/js/modules/toast.js:88-109`) | Single `#liveToast` element re-used on rapid successive `showToast()` calls — last message wins, prior message can be lost mid-fade. | 🟡 Medium | Mitigated | Module disposes the prior Bootstrap instance to prevent animation conflicts. `e2e/ui-hardening.spec.ts` asserts: only one toast element exists, last message wins, stale `bg-*` classes are cleared. |
| KI-005 | Workout Plan controls (`static/js/modules/workout-controls-persistence.js`, `static/js/modules/workout-plan.js`, `static/js/modules/exercises.js:47`) | **Was**: page refresh mid-entry lost unsaved Workout Controls values (weight/sets/RIR/RPE/min-rep/max-rep) — fields reset to template defaults on reload. | 🟢 Low | ✅ Resolved 2026-07-13 (behavior change) | **Contract flipped.** The six controls now persist to tab-scoped `sessionStorage` as one JSON record under `hypertrophy_workout_controls_v1` and are restored on reload; values are captured on a synchronous `input` event, so a mid-entry value survives without a blur. Saved values win over template defaults; missing/malformed/non-numeric/out-of-range stored values fall back to the pinned defaults (weight 25, sets 3, RIR 3, RPE 7, min-rep 6, max-rep 8). A successful **Add Exercise retains the user's pre-add values** (the post-success estimate reset was removed); **Clear Filters** and the routine cascade retain them; **Clear Plan** resets the six fields to defaults and removes the storage key; closing the tab clears them naturally. Plan + owner rulings: `docs/ki005_controls_persistence/PLANNING.md`. `e2e/ui-hardening.spec.ts` locks the new contract (12 cases; the old reset-on-reload assertion is inverted). |
| KI-006 | Modal focus (Bootstrap modals across `workout_plan.html` + `workout_log.html`) | **Was**: Escape close + full focus trap were left to Bootstrap defaults and only partially worked — Tab could leak out of the dialog, and the old tests could not tell the difference. | 🟡 Medium | ✅ Resolved 2026-08-02 (one product fix + strict tests) | **Root cause found, not just re-tested.** Bootstrap's `FocusTrap` is a *bounce-back* trap: it listens for `focusin` and returns focus to the dialog after it leaves. When the modal's last control is also the last focusable element in the document, Tab moves focus to `document.body`, which emits no `focusin`, so the trap never runs. Measured: on `/workout_plan` the Clear Plan dialog's last control is index 61 of 64 focusable elements (two follow it, so the bounce fires and it *looked* fine); on `/workout_log` the Clear Log dialog's last control is index 17 of 18 and focus escaped to `body`. Keyboard containment was depending on unrelated DOM ordering. **Not a Bootstrap 5.3.8 regression** — an A/B swapping only the CDN bundle to 5.1.3 reproduced the identical failure. Fixed by `static/js/modules/modal-focus-trap.js`, loaded globally from `base.html`, which wraps Tab/Shift+Tab *at* the boundary instead of catching focus after it leaves; Bootstrap's own trap still handles focus arriving from elsewhere. Locked by `e2e/ui-hardening.spec.ts` (Plan **and** Log: forward wraparound last→first, backward wraparound first→last via Shift+Tab, Escape-only close with no fallback click, focus-moves-inside, `aria-modal`/`aria-labelledby`, backdrop + `body.modal-open` cleanup) and by the rewritten `e2e/accessibility.spec.ts` Escape test. The superseded assertions were unfalsifiable: the old Escape test clicked the close button when Escape failed, and the old trap test pressed Tab once and only checked focus was still *somewhere* inside — true even with no trap at all. |
| KI-007 | Isolated muscles table (DB table `exercise_isolated_muscles`) | **Was**: table empty in the then-current local DB; dependent sections conditionally hide (`{% if isolated_muscles %}`). | 🟢 Low | ✅ Resolved — premise obsolete | Re-derived 2026-08-04 against the tracked `data/catalog.seed.db`: **1,598 mappings covering 1,351 distinct exercises** out of **1,897** exercises. The table is populated from the seed, so the "empty table" premise no longer holds and the intentional-vs-seeding-gap question is answered — it was a seeding gap, since closed. The `{% if isolated_muscles %}` guard stays as correct defensive rendering for exercises that genuinely have no isolated-muscle rows. |
| KI-008 | Multi-tab editing of same routine | Out of scope under single-user / single-tab operating model. | — | Deferred (backlog only) | Documented in §1.2 and §5.3. Not a release blocker. |
| KI-009 | Workout log Excel export (`routes/workout_log.py` `/export_workout_log`) | `import pandas as pd` (formerly the first line of the route handler) raised `ImportError: DLL load failed while importing aggregations: An Application Control policy has blocked this file.` on Windows installs with AppLocker / Smart App Control rules against the pandas C-extension `pandas/_libs/window/aggregations.pyd`. The `except Exception` fallback converted the failure into HTTP 500 for both the empty-state and data-present paths. | 🟡 Medium | ✅ Resolved 2026-05-23 (pandas removed) | Fixed in commit `4bbe06b` by rewriting the route on top of the existing pandas-free helpers (`utils/export_utils.py::create_excel_workbook`) already used by `/export_to_excel`, `/export_summary`, and `/export_large_dataset`. Pandas was the only `import pandas` site in production code; `pandas`, `numpy`, and `python-dateutil` dropped from `requirements.txt`. Excel work now goes through `XlsxWriter==3.2.9` and `openpyxl==3.1.5` only. Locked by `tests/test_workout_log_routes.py::TestExportWorkoutLog` (5 cases: 404 empty, 200 + Excel content-type, PK magic bytes, `Workout Log` sheet present, header row matches `get_workout_logs()` keys). |
| KI-010 | Toast legacy signature (`static/js/modules/toast.js:14-31`) | A legacy two-argument call whose *message* is itself one of the four type words is swallowed. `showToast('error', true)` renders body text **`"true"`** on a `bg-danger` toast: `validTypes.has(type)` at `:15` sees a valid type, so the legacy branch at `:15-27` never runs and the boolean `true` becomes the message. Identical for `'warning'`, `'success'` and `'info'`. The **one-argument** form collides the other way: `showToast('warning')` renders the default copy **"Action completed successfully."** on a yellow warning toast. | 🟡 Medium | **Open** | **Not mitigated, not fixed** — no production line changed. **Reachability, measured**: **8** live call sites carry the collision-capable `showToast(error.message \|\| '<fallback>', true)` shape — [filters.js:251](../static/js/modules/filters.js#L251), [workout-plan-execution-style.js:215](../static/js/modules/workout-plan-execution-style.js#L215), [workout-plan-supersets.js:200](../static/js/modules/workout-plan-supersets.js#L200) and `:227`, [workout-plan-table.js:688](../static/js/modules/workout-plan-table.js#L688), [workout-plan.js:114](../static/js/modules/workout-plan.js#L114), `:160` and `:193` — so this is **one server-copy change away** from firing. It is not reachable today only because **no `error_response()` / `success_response()` call site passes one of the four type words as the message** — `utils/errors.py` merely forwards whatever its caller supplies (`:36-37`, `:94-97`), and `fetch-wrapper.js:61` hands that envelope message straight to `error.message`. Measured 2026-08-22: **0** of **234** response call sites across `routes/`, `utils/` and `app.py` pass a bare type word. `static/js/modules/__tests__/toast.test.js` **B45** is a **characterization** test: it pins the current *defective* output (`'true'` + `bg-danger`), so it is **not** a regression test for a fix. A further **5** sites carry the same collision in the **one-argument** form — `showToast(result.message \|\| '…')` / `showToast(data.message \|\| '…')` at `exercises.js:31` and `:59`, `workout-plan-supersets.js:191` and `:221`, and `workout-plan-table.js:680` — where a type-word message yields default copy on a mistyped toast. **B43** pins only the `showToast('success')` case, and only its body text; the sharper `showToast('warning')` variant — a **yellow** toast whose copy says the action succeeded — is recorded at §10.7-R3 but is **not pinned by any test**. A production fix must **invert or update B45** (and re-check B43) in the same PR — a red there is the intended review signal, not a regression. Measured evidence: [`STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md) §10.7-R3. |
| KI-011 | Toast action button (`static/js/modules/toast.js:60` + `:84`; callers `static/js/modules/volume-splitter.js:424-431` and `:184-190`) | Any **later** `showToast()` from anywhere destroys a still-live action button: `:60` clears `toastBody.innerHTML` and `:84` appends the button into that same `#toast-body`. **Reachable inside a caller of its own** — the "Activate for Plan tab" toast is raised with `duration: 6000`, `volume-splitter.js:433` immediately calls `loadVolumeHistory()`, and the `.catch` opening at that function’s `:554` emits `showToast('error', …)` at `:564`. On a slow or failing history refresh the user’s button vanishes mid-toast. ⚠️ **AMENDED 2026-08-26 (Packet U1).** This row said **"sole caller … `:299-306`"**, and the KI-012 row below falsifies the "sole" half: U1's Retry action is the **second** caller, at `:184-190`. The four `volume-splitter.js` anchors above were all exact when written and all moved **+125** lines under U1's diff; they are re-anchored here, measured against the shipped file rather than derived from a single drift figure. `toast.js`'s own two anchors did not move — U1 does not touch that file. | 🟡 Medium | **Open** | **Not mitigated, not fixed** — no production line changed, and nothing in the test suite makes the button survive a body clear. `toast.test.js` **B30–B35 are deliberately placement-neutral**: they locate the button through `#liveToast` and assert its type, label, `aria-label`, guard and coercion while staying **silent about its direct parent**, precisely so the relocation a fix requires does not red them (owner ruling, [`STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md) §10.11 ruling 4). They therefore neither fix nor mitigate this defect. **No fixed-behavior regression test exists yet** — one must be added with the fix, and all six of B30–B35 must stay green through it. Measured evidence: §10.7-R10 of the same document. |
| KI-012 | Volume Splitter calculate (`static/js/modules/volume-splitter.js`, the `POST /api/calculate_volume` call) | **Was**: a failed calculation produced no user-visible signal of any kind. Two independent suppressions sat on one call — `showErrorToast: false` in the request options silenced the shared wrapper's toast for the **request-failure** class (non-2xx and transport), and a `.catch` whose entire body was `console.error` silenced the **post-2xx response-handling** class, which never reaches the wrapper's error branch at all. Reproduce on `main` before this change: calculate successfully, force `POST /api/calculate_volume` to 500, calculate again — the previous run's table, suggestion cards, `.muscle-row` status classes and `.current-value` pill modifiers all stay on screen with nothing to say they are stale. | 🟠 High | Mitigated | **Repaired 2026-08-26 (Packet U1).** A failure now raises an accessible toast carrying a Retry action **and** a persistent inline `#volume-calculate-error` region prepended to `.volume-insights-panel`, and `clearResults()` empties every surface that could be mistaken for the failed calculation's output. The region exists **if and only if** the last completed calculation failed and the user has not since reset — it is created on failure, `.remove()`d on the next success, and never present as a hidden shell, so the success path gains no observable state. Repeat **slider-originated** failures do not re-announce while the same region and U1's own toast content stand; explicit commands always announce. Locking tests, all in `e2e/volume-splitter.spec.ts`: **`a1`** (non-2xx after a prior success) and **`a2`** (transport abort) lock the request-failure class; **`b1`** locks the post-2xx class through a 200 the response handler cannot render. Mutations **M1** and **M2** prove the two classes fail *in isolation* — restoring either suppression alone reds only its own arms. **Not fixed here**: `showErrorToast: false` stays in production so the page-specific toast can carry Retry and one failure does not raise two competing notifications; the owner explicitly accepted at Gate 1 that the flag therefore ships without direct regression pressure (`docs/volume_failure_feedback/PLANNING.md` §v2.13, OD-4). U1 is also KI-011's **second** caller of the toast action button and does not fix that defect — the durable Retry is the inline region. Plan and owner decisions: [`docs/volume_failure_feedback/PLANNING.md`](volume_failure_feedback/PLANNING.md). |
| KI-013 | Backup Center save-first (`static/js/modules/backup-center.js`, the `#backup-restore-save-first` click listener) | **Was**: clicking **Save current plan first** from inside an open restore confirmation destroyed that confirmation. The snapshot's own `refreshBackupCenter()` reaches `renderBackupDetails()`, whose `clearPendingAction()` call is the sole writer of `pendingAction = null` — so the panel was hidden, the title reset to `Confirm action`, the warning text emptied and the confirm button relabelled `Confirm`. Measured live at `06a3f41`: the selected backup, its details and the list selection all survived unchanged, and the snapshot was created — **only the intent died**, so the user had to re-open a restore they had already confirmed. Reproduce on `main` before this change: open `/backup`, select a backup, click **Restore To Current Plan**, click **Save current plan first**, wait for the success toast. | 🟠 High | Mitigated 2026-08-27 (Packet U2) | **Repaired 2026-08-27.** The confirmation is now **re-asserted** after the snapshot refresh settles, and the re-assert is **authorized**, not merely identity-checked. A module-scoped `pendingActionGeneration` counter is incremented beside **both** writers of `pendingAction` — `clearPendingAction()` and `showPendingAction()` — so every transition of intent, from any of the six call sites or the Cancel binding, moves it. The save-first handler captures the counter before its first `await` and re-asserts only when the counter has advanced by **exactly one** (the teardown the refresh itself performs) **and** both `selectedBackupId` and `selectedBackupDetails.id` still equal the captured id — two checks, not one, because `selectedBackupId` moves synchronously at `loadBackupDetails()` while `selectedBackupDetails` lags a fetch. A mid-flight **lock** (`setDetailActionDisabled(true)`) additionally makes seven controls and the library list inert for the duration of the snapshot; `#backup-sort` and `#backup-search` are deliberately outside it and are covered by the counter alone. Three owner-pinned strings ship with it: the button relabels to `Current plan saved` and disables after a successful snapshot; the panel carries `Saves the current workout plan only — logged sessions are not included in this snapshot.`, which **discloses** the pre-existing asymmetry between `create_backup()` (reads `user_selection` only) and `restore_backup()` (deletes `workout_log` too) rather than repairing it; and a vanished restore target now raises `The backup you were restoring is no longer available. Please choose it again.` instead of failing silently. The re-asserted panel is announced (`role="alert"`, set from JS) and focus lands on `#backup-action-cancel` — the safe control, never `Confirm Restore`. **Locking tests, all in `e2e/program-backup.spec.ts`** (`Backup Center save-first confirmation continuity`, arms `u1`–`u11`): `u1` uses a **transition oracle** — a `MutationObserver` on `#backup-action-confirm[hidden]` asserting the recorded sequence `[true, false]` — because a state sample after the success toast reads the panel two round trips too early and passes on a mutant that never re-asserts; `u2` proves the re-asserted panel still executes the restore; `u3` proves Cancel survives the lock; `u4`–`u6` pin the three clearing paths that route only through `renderBackupDetails()`; `u7` and `u8` hold the snapshot `POST` open and prove a mid-flight selection change or Cancel **blocks** the re-assert; `u9` omits the target from the refreshed library and pins the warning toast; `u10` guards the untouched failure `catch`; `u11` pins the announcement and the focus target. Mutation evidence: **M3** (drop the generation check) reds `u8` — the destructive-resurrection guard is load-bearing; **M7** (delete `clearPendingAction()` in `renderBackupDetails()`) reds `u4`, `u5` and `u6`, proving those three arms measure the clearing paths rather than the repair; **M6** (forget the unlock) reds `u3`. **Not fixed here**: `backup-center.js` keeps 0 % unit coverage — owner decision **OD-1 (i)**, with no follow-up packet and no rider booked, because a Vitest file would restart the live JS-unit qualification window. The mid-flight lock is a real interaction change, not a bug fix, and on a slow connection it is a visible freeze. Plan and owner decisions: [`docs/backup_confirmation_continuity/PLANNING.md`](backup_confirmation_continuity/PLANNING.md). |

> **How to use this table**:
> 1. When a new bug is reported, add a row (assign next `KI-NNN`) and link to the regression test that locks the fix.
> 2. When closing a row, change *Status* to `Mitigated` + link the test that guards against re-introduction.
> 3. Do not delete rows — they are historical references for future triage.

---

## 1. CRITICAL SCENARIOS (Potential Crashes/Data Loss)

### 1.1 Network Connection Issues
**File**: `fetch-wrapper.js`
| Scenario | Current Handling | Risk |
|----------|------------------|------|
| Complete network loss mid-operation | Error handling tests exist for API/network failures | 🟠 Retry policy still GET-focused |
| Server returns 500 during exercise save | Toast + recovery path tested | 🟡 Form retention should stay asserted over time |
| Timeout during export to Excel | Timeout path covered in E2E | 🟡 Keep regression coverage |

**E2E Coverage**: ✅ Covered in [error-handling.spec.ts](../e2e/error-handling.spec.ts)

### 1.2 Concurrent Operations Race Conditions
**File**: `workout-plan.js`, `exercises.js`
| Scenario | Current Handling | Risk |
|----------|------------------|------|
| Rapid double-click on "Add Exercise" | Debounce + loading state + E2E coverage | ✅ |
| Click "Delete" while request in progress | Duplicate-delete guard in place | ✅ |
| Multiple tabs editing same routine | Out of scope in current `single-tab` operating mode | 🟢 Backlog only |

**E2E Coverage**: ✅ In-scope behavior covered.
**Scope Note**: Multi-tab conflict detection is deferred (not a release requirement for current mode).

### 1.3 Empty/Null State Handling
**File**: `workout-log.js`, `workout-plan.js`
| Scenario | Current Handling | Risk |
|----------|------------------|------|
| Import from empty workout plan | Empty-state flows covered | 🟡 Message quality should remain consistent |
| Clear log when already empty | No-crash behavior covered | 🟡 Minor UX friction still possible |
| Export empty plan to Excel | Empty-state warning implemented and tested | ✅ |

**E2E Coverage**: ✅ Covered in [empty-states.spec.ts](../e2e/empty-states.spec.ts)

---

## 2. HIGH-RISK SCENARIOS (Wrong Output/Broken Features)

### 2.1 Validation Boundaries
**File**: `exercises.js`, `workout-log.js`, `workout-plan.js`
| Scenario | Current Behavior | Status |
|----------|------------------|--------|
| Weight in 0–1000 kg | Inclusive server-side bound; 0 remains valid for bodyweight/assisted entries | ✅ |
| Negative rep range | Rejected | ✅ |
| Min rep > Max rep | Rejected server-side on plan add/edit and scored-log edit | ✅ |
| Sets = 0 | Rejected | ✅ |
| RIR outside 0–10 | Rejected server-side on plan add/edit and scored-log edit | ✅ |
| RPE > 10 | Rejected | ✅ |

**E2E Coverage**: ✅ Covered in [validation-boundary.spec.ts](../e2e/validation-boundary.spec.ts)

### 2.2 Dropdown Cascade State Issues
**File**: `routine-cascade.js`, `workout-dropdowns.js`
| Scenario | Current Behavior | Risk |
|----------|------------------|------|
| Back button after routine selection | Stateless contract enforced: full reset of `env/program/day/#routine` | ✅ |
| Refresh after selection | Stateless contract enforced: full reset of `env/program/day/#routine` | ✅ |
| Deep-link query `?routine=...` | Explicitly ignored in stateless mode | ✅ |
| Hidden routine value mismatch | Hidden field clears with incomplete cascade; no stale value observed | ✅ |

**E2E Coverage**: ✅ Covered in [browser-navigation-state.spec.ts](../e2e/browser-navigation-state.spec.ts)

### 2.3 Superset Edge Cases
**File**: `workout-plan.js`
| Scenario | Current Behavior | Status |
|----------|------------------|--------|
| Link/unlink behavior | Covered in dedicated suite | ✅ |
| Delete exercise in superset | Covered | ✅ |
| Replace exercise in superset | Covered at flow level | ✅ |
| Persistence after refresh | Covered | ✅ |

**E2E Coverage**: ✅ Covered in [superset-edge-cases.spec.ts](../e2e/superset-edge-cases.spec.ts)

### 2.4 Replace Exercise Failure Modes
**File**: `workout-plan.js`
| Scenario | Current Toast | Status |
|----------|---------------|--------|
| No alternative found | "No alternative found for this muscle/equipment" | ✅ Covered |
| All alternatives in routine | "All alternatives are already in this routine" | ✅ Covered |
| Exercise missing muscle data | "This exercise is missing muscle/equipment data" | ✅ Covered |

**E2E Coverage**: ✅ Covered in [replace-exercise-errors.spec.ts](../e2e/replace-exercise-errors.spec.ts)

---

## 3. MEDIUM-RISK SCENARIOS (Glitches/UX Friction)

### 3.1 Toast Notification Issues
**File**: `toast.js`
| Scenario | Risk | Status |
|----------|------|--------|
| Multiple toasts at once | 🟡 Message loss risk | ✅ Mitigated for **message** loss (KI-004) — `e2e/ui-hardening.spec.ts` asserts single `#liveToast` instance, last message wins, stale `bg-*` classes cleared. The **action button** that same shared element destroys is **not** mitigated — open as **KI-011** |
| Long error message overflow | 🟡 Truncation risk | Open — visual concern only |
| Legacy vs new `showToast` signatures | 🟡 Inconsistent style risk | Open — both signatures still supported (`toast.js:14-31`). A message that equals a type word **bypasses** that branch and is swallowed — open as **KI-010** |

### 3.2 Form State Persistence
**Files**: `workout-controls-persistence.js`, `workout-plan.js`, `exercises.js`
| Scenario | Risk | Status |
|----------|------|--------|
| Page refresh mid-entry | 🟡 User input loss | ✅ Resolved 2026-07-13 (KI-005) — the six Workout Controls are restored from tab-scoped `sessionStorage` on reload; `e2e/ui-hardening.spec.ts` asserts restore-on-reload (contract flipped from reset-to-defaults) |
| Tab away and return | 🟡 Stale values | ✅ Contract locked — `e2e/ui-hardening.spec.ts` asserts values retained after visibility-change cycle |
| Add exercise, then change routine | 🟡 Context mismatch | ✅ Contract locked — `e2e/ui-hardening.spec.ts` asserts Workout Controls retained across routine cascade changes |

### 3.3 Table Sorting/Filtering Issues
**File**: `workout-log.js`, `filters.js`
| Scenario | Risk |
|----------|------|
| Sort by date with NULL dates | 🟡 Unexpected order |
| Filter applied, then add exercise | 🟡 New row appears "missing" |
| Clear filters resets sort | 🟡 State surprise |

### 3.4 Modal Focus/Accessibility
**File**: `workout-log.js`, `workout_plan.html`
| Scenario | Risk | Status |
|----------|------|--------|
| Modal layering/z-index behavior | 🟡 Interaction inconsistency | Open — no observed regression |
| Escape key close behavior | 🟡 Accessibility gap | ✅ Resolved 2026-08-02 (KI-006) — Escape alone closes both the Plan and Log dialogs; `e2e/ui-hardening.spec.ts` and `e2e/accessibility.spec.ts` assert it with **no close-button fallback**, waiting on `hidden.bs.modal` and then checking backdrop + `body.modal-open` cleanup. Escape needed no product change; only the tests were dishonest. |
| Focus trap in modal | 🟡 Keyboard nav gap | ✅ Resolved 2026-08-02 (KI-006) — wraparound is now real in both directions and asserted at the boundary (Tab from the last control → first; Shift+Tab from the first → last) on the Plan **and** Log dialogs. Required a product fix: `static/js/modules/modal-focus-trap.js`, because Bootstrap's `focusin`-driven trap cannot fire when focus falls through to `document.body`. |
| Modal ARIA attributes | 🟡 SR navigation gap | ✅ Hardened — `e2e/ui-hardening.spec.ts` asserts `aria-modal="true"` + `aria-labelledby` resolves to a visible heading. |

---

## 4. LOW-RISK SCENARIOS (Cosmetic/Rare)

### 4.1 Dark Mode Edge Cases
| Scenario | Risk |
|----------|------|
| Theme switch mid-modal | 🟢 Minor flicker |
| Charts not updating with theme | 🟢 Visual mismatch |
| Print styling in dark mode | 🟢 Poor print contrast |

### 4.2 Export Edge Cases
| Scenario | Risk |
|----------|------|
| Special characters in filename | 🟢 Encoding quirks |
| Large dataset export | 🟢 Performance |
| Safari Blob handling | 🟢 Browser compatibility |

### 4.3 Mobile/Responsive Issues
| Scenario | Risk |
|----------|------|
| Table overflow on mobile | 🟢 Usability friction |
| Touch gestures for drag/drop | 🟢 Interaction gaps |
| Dropdown taps on small screens | 🟢 Precision issues |

---

## 5. RECOMMENDED NEW E2E TESTS (Remaining, In Scope)

### 5.1 Priority 1 - High Impact
None currently outstanding in this tier.

### 5.2 Priority 2 - Risk Reduction
```typescript
// e2e/modal-accessibility.spec.ts
test.describe('Modal Accessibility', () => {
  test('escape key closes modal');
  test('focus remains trapped inside open modal');
});
```

### 5.3 Out of Scope (Current Iteration)
1. `e2e/multi-tab-conflict.spec.ts` (deferred under `single-user` + `single-tab` mode).

---

## 6. IMMEDIATE CODE FIX RECOMMENDATIONS (Current)

No release-blocking code fix from the original "must do" list remains outstanding in this analysis snapshot.

If starting one targeted code improvement now:
1. Standardize replace-exercise error toasts with actionable next-step hints.
2. Add shared toast assertion helpers to reduce E2E duplication.

---

## 7. TESTING COVERAGE MATRIX (Updated)

| Area | Unit Tests | E2E Tests | Remaining Gap |
|------|-----------|-----------|----------------|
| Add Exercise Flow | ✅ | ✅ | None critical |
| Delete Exercise | ✅ | ✅ | None in current scope |
| Replace Exercise | ✅ | ✅ (flow + error toasts) | None critical |
| Superset Link/Unlink | ✅ | ✅ | None critical |
| Import to Log | ✅ | ✅ | None critical |
| Export Excel | ✅ | ✅ | None critical |
| Routine Cascade | ⚠️ Limited | ✅ + Stateless regression spec | None in current contract |
| Validation | ✅ | ✅ | Strengthen strict assertions in some smoke-style cases |
| Error Handling | ✅ | ✅ | Ongoing regression only |
| Network Errors | ❌ | ✅ | Add unit-level retry policy tests if desired |

---

## 8. SUMMARY ACTION ITEMS

### Must Do (Before Next Release)
1. Keep browser-navigation behavior locked to **Option 2: Stateless** in docs/tests.
2. ✅ Done (2026-05-23) — Added a short "Known Issues / Reported Bugs" map to separate real issues from theoretical risks.
3. Review Open Questions in Section 10.4 and close any that are no longer relevant.

### Should Do (Next Sprint)
1. Harden weak E2E assertions that currently act as smoke checks.
2. Add accessibility checks for modal focus trap and keyboard escape behavior.
3. Rank medium-risk scenarios internally by impact/frequency.

### Nice to Have (Backlog)
1. Multi-tab conflict strategy and tests (out of scope under current operating mode).
2. Mobile responsiveness tests for plan/log tables and dropdown interactions.
3. Performance tests for large export datasets.
4. Cross-browser checks focused on Safari export behavior.

---

*Document synced with current repository state and test suite inventory on February 28, 2026.*

---

## 9. PEER REVIEW — Claude Opus 4.6 (February 26, 2026)

> **Status note**: This section is preserved as historical review context.
> Current decisions and priorities are defined in **Section 10** (scope-locked plan/status).

> **Reviewer**: Claude Opus 4.6
> **Scope**: Full document review — accuracy, priorities, and actionability.
> **File references verified** against `static/js/modules/`: All referenced JS files (`fetch-wrapper.js`, `routine-cascade.js`, `filters.js`, `toast.js`, `exercises.js`, `exports.js`, `workout-plan.js`, `workout-log.js`) confirmed present in repository.

### 9.1 Priority Reassessments

| Item | Current Rating | Recommended Rating | Rationale |
|------|---------------|-------------------|-----------|
| Multi-tab conflict (1.2) | 🔴 Critical / "Must Do" | 🟡 Nice to Have | This is a single-user local training app. Multi-tab editing of the same routine is an edge case, not a real-world crash vector. Downgrade from "Must Do Before Next Release" to backlog. |
| Browser nav cascade (2.2) | 🟠 High / "Must Do" | 🟠 Investigate first | Before writing E2E tests, confirm whether this is a real observed bug or theoretical. Flask server-rendered pages with standard form posts may already handle back/refresh natively. Add a spike task to reproduce the issue before committing to a test suite. |
| Replace exercise errors (2.4) | 🟠 High / "Must Do" | 🟡 Should Do | The toast messages already exist and work. The gap is only missing E2E assertions on specific message text. This is a test-quality improvement, not a code gap — lower priority than actual missing functionality. |

### 9.2 Structural Gaps in This Document

1. **No connection to real bug reports.** The entire analysis is theoretical risk modeling. Add a "Known Issues / Reported Bugs" section that maps actual user-reported problems (if any) to these scenarios. Theoretical risks without real-world evidence should be weighted lower.

2. **Medium-risk items (Section 3) lack internal ranking.** There are 12 medium-risk scenarios listed with no ordering. Recommended priority within Section 3:
   - **Highest**: 3.1 Toast stacking (message loss affects all error paths) and 3.2 Form state persistence (direct user frustration).
   - **Lower**: 3.3 Table sort/filter edge cases and 3.4 Modal accessibility (less frequent, less impactful).

3. **Section 5 test stubs should not be separate spec files.** The `replace-exercise-errors` assertions (Section 5.1) should be added to the existing `superset-edge-cases.spec.ts` or a general `workout-plan.spec.ts` flow — not a new dedicated file. Creating a new spec file for 3 assertions adds maintenance overhead without benefit.

### 9.3 Actionable Corrections for Codex

**For Codex to address when implementing from this document:**

1. **Do NOT implement multi-tab conflict detection (Section 5.2).** This requires cross-tab messaging (`BroadcastChannel` or `localStorage` events), adds significant complexity, and solves a problem that doesn't exist for a single-user app. Remove from "Must Do" and "Should Do" lists entirely.

2. **Before writing `browser-navigation-state.spec.ts`**, manually test: (a) click back after routine selection — does the page break? (b) refresh after selection — does it reset? If Flask re-renders correctly on its own, skip the E2E suite and close this item.

3. **For replace-exercise error assertions**, add 3 assertion lines to the existing E2E flow that already triggers replace-exercise. Do not create a new spec file. Example:
   ```typescript
   // Add to existing replace-exercise test in superset-edge-cases.spec.ts
   await expect(page.locator('.toast')).toContainText('No alternative found');
   ```

4. **Section 8 "Must Do" list should be revised to:**
   - (a) Spike: reproduce cascade nav bug — if not reproducible, close.
   - (b) Add replace-exercise toast assertions to existing E2E (3 lines, not a new file).
   - (c) Move multi-tab and browser-nav items to backlog unless a real bug is reported.

### 9.4 What This Document Gets Right

- Verified implementation table (Section 0) is accurate and useful.
- Risk-tiered structure (Critical → Low) is correct and well-organized.
- Coverage matrix (Section 7) gives a clear snapshot — keep maintaining it.
- The `weight = 0` contradiction resolution (Executive Summary point 3) was a good catch.
- Honest acknowledgment of partial coverage where it exists.

---

*Peer review appended by Claude Opus 4.6 on February 26, 2026.*

---

## 10. IMPLEMENTATION PLAN AND STATUS (FOR REVIEW)

### 10.1 Plan
1. Lock scope assumptions in this document.
2. Re-prioritize action items based on scope.
3. Execute browser-navigation spike and capture evidence.
4. Decide behavior contract for browser navigation.
5. Implement chosen contract and add regression tests.
6. Re-sync this document with outcomes.

### 10.2 What Codex Is Doing Now
1. Finalizing the document after contract implementation.
2. Marking browser-navigation work as completed under Option 2 (Stateless).
3. Leaving only true remaining items in the action list.

### 10.3 Done
1. Scope locked: `single-user`, `local`, `single-tab`.
2. Multi-tab conflict moved from release blocker to backlog/out-of-scope.
3. Browser-navigation spike executed via Playwright on **February 26, 2026**.
4. Decision made: **Option 2 (Stateless)** for browser navigation behavior.
5. Implemented stateless reset logic in [routine-cascade.js](../static/js/modules/routine-cascade.js).
6. Added [browser-navigation-state.spec.ts](../e2e/browser-navigation-state.spec.ts) to enforce the stateless contract.
7. Verified test run: `3 passed` on Chromium (`back`, `refresh`, deep-link ignore).
8. Added [replace-exercise-errors.spec.ts](../e2e/replace-exercise-errors.spec.ts) with 3 reason-specific toast assertions.
9. Verified test run: `3 passed` on Chromium (`no_candidates`, `duplicate`, `missing_metadata`).

### 10.4 Discuss Further
1. Assertion strategy for replace-exercise toasts: exact text vs keyword matching.
2. If product scope changes later, whether to introduce an alternative "stateful" routine mode.

### 10.5 Spike Evidence Snapshot
1. Command run: `npx playwright test e2e/_spike_browser_navigation.spec.ts --project=chromium --workers=1`
2. Captured snapshot:
   ```json
   {
     "initial": { "env": "", "program": "", "day": "", "hidden": "" },
     "selected": { "env": "GYM", "program": "Full Body", "day": "Workout A", "hidden": "GYM - Full Body - Workout A" },
     "afterBack": { "env": "GYM", "program": "", "day": "", "hidden": "" },
     "afterRefresh": { "env": "", "program": "", "day": "", "hidden": "" },
     "deepLink": { "env": "", "program": "", "day": "", "hidden": "" }
   }
   ```
3. Contract verification command: `npx playwright test e2e/browser-navigation-state.spec.ts --project=chromium --workers=1`
4. Verification result: `3 passed`.

---

## 11. SUMMARY PAGES CALCULATION AUDIT — Claude Opus 4.6 (February 28, 2026)

> **Reviewer**: Claude Opus 4.6
> **Scope**: Full code review of Plan Volume Summary and Session Summary — calculation correctness, mode consistency, isolated muscles, and user comprehension.
> **Files reviewed**: `utils/effective_sets.py`, `utils/weekly_summary.py`, `utils/session_summary.py`, `utils/volume_classifier.py`, `routes/weekly_summary.py`, `routes/session_summary.py`, `templates/weekly_summary.html`, `templates/session_summary.html`

### 11.1 Bugs Found (User-Visible)

#### BUG-1: Total Volume column shows effective-weighted values in Raw mode (HIGH)

**Affected pages**: Plan Summary, Session Summary
**Files**: `utils/session_summary.py:243-244`, `utils/weekly_summary.py:201-204`

When user selects **Raw Sets** counting mode, the "Total Volume" column still displays effective-weighted volume. The raw volume exists in the response (`raw_total_volume` / `raw_total_reps`) but is never used by the JS rendering.

**What the user sees**: Switches to Raw mode, sees "Raw Sets: 12" but "Total Volume: 7,140" — the math doesn't match `12 × avg_reps × weight`. Numbers appear wrong.

**Fix**: JS should read `raw_total_volume` when `counting_mode === 'raw'`, and `total_volume` (effective) otherwise. Backend already returns both values.

#### BUG-2: "Ultra Volume" vs "Excessive Volume" label mismatch (MEDIUM)

**Affected pages**: Both summary pages — isolated muscles table vs main table
**Files**: `utils/volume_classifier.py:33` (`get_volume_label` returns "Ultra Volume"), JS `getVolumeDetails()` returns "Excessive Volume"

The main muscle group table (JS-rendered) shows "Excessive Volume" at 30+ sets.
The isolated muscles table (server-rendered via `get_volume_label`) shows "Ultra Volume" at 30+ sets.
Same page, same threshold, different label.

**Fix**: Change `get_volume_label()` in `volume_classifier.py:33` from "Ultra Volume" to "Excessive Volume". Update `get_volume_tooltip()` ranges map accordingly.

#### BUG-3: Isolated muscles table is always empty (LOW)

**Affected pages**: Both summary pages
**File**: `utils/weekly_summary.py:263-286`, DB table `exercise_isolated_muscles`

The `exercise_isolated_muscles` table has 0 rows in the database. The "Advanced Isolated Muscles Statistics" section renders an empty table with headers only. No empty-state message shown.

**Options**: (a) Populate the mapping table during DB initialization, (b) hide the section when empty, or (c) show an informative empty state message.

### 11.2 Calculation Inconsistencies (Correctness)

#### CALC-1: Isolated muscles table ignores all mode toggles

`calculate_isolated_muscles_stats()` uses raw SQL `SUM(us.sets)` with no effort factor, rep range factor, or contribution weighting. The template notes this: *"This table uses raw (unweighted) sets regardless of counting mode."*

**Assessment**: Acceptable as documented, but the volume classification badge on this table uses `get_volume_class(muscle.total_sets)` which applies raw-set thresholds — while the main table uses effective-set thresholds. This means the same muscle could show "Medium Volume" in the main table and "High Volume" in the isolated table for the same underlying data.

#### CALC-2: Plan Summary "Frequency" counts routines, not weekly sessions

`weekly_summary.py:176` counts routines where `eff_contribution >= 1.0`, not actual training sessions per week. A PPL user with Push A + Push B sees Frequency=2 for Chest, which coincidentally equals 2x/week — but a Full Body user with 3 routines sees Frequency=3, implying 3x/week which is only true if all 3 are performed in one week.

**Assessment**: Acceptable for plan-level analysis. The label "Frequency" is slightly misleading — it represents "routine exposure count" not "weekly training frequency". Consider renaming to "Routines" or adding a tooltip.

#### CALC-3: Session Summary volume badge uses weekly thresholds on per-routine data

The volume classification (Low < 10, Medium 10-19, High 20-29, Excessive 30+) applies to the entire plan's weekly volume. Session Summary shows per-routine values that are naturally smaller. A single Push routine with 10 effective sets for Chest shows "Medium Volume" — but that's just one routine's contribution, not the weekly total.

**Assessment**: The session warning badges (OK/Borderline/Excessive with 10/11 thresholds) partially address this, but they only appear for users with logged sessions. Plan-only users see "No Sessions" badges alongside weekly-scale volume classifications applied to single-routine data.

### 11.3 User Comprehension Gaps

| Gap | Description | Suggested Fix |
|-----|-------------|---------------|
| Factor values hidden | UI says "Effort & Rep Range Weighted" but never shows the actual multipliers (RIR 0-1=100%, 2-3=85%, 4-5=70%, 6+=55%; Reps 1-5=85%, 6-20=100%, 21-30=85%, 31+=70%; Secondary=50%, Tertiary=25%) | Add collapsible "How it's calculated" panel |
| No mode-switch diff | Toggling Effective/Raw recalculates all numbers but user can't tell which muscles were most affected | Consider highlighting changed values or showing delta |
| Page naming confusion | "Session Summary" shows plan data grouped by routine, not actual logged training sessions. "Plan Volume Summary" is clearer but users may not understand the difference. | Add subtitle explaining scope: "Volume per routine in your plan" vs "Total weekly volume across all routines" |
| Missing data = neutral (1.0) | If RIR/RPE is not set, effort factor defaults to 1.0 (full credit). User may not realize that leaving RIR blank gives maximum credit — same as training to failure. | Show indicator when default factor is applied |

### 11.4 Proposed Fix Plan (For Codex Review)

Priority order based on user impact:

| # | Fix | Severity | Files to Change | Effort |
|---|-----|----------|-----------------|--------|
| 1 | **BUG-1**: Display `raw_total_volume` / `raw_total_reps` when counting mode is Raw | HIGH | `templates/session_summary.html` (JS), `templates/weekly_summary.html` (JS) | Small — conditional in JS template rendering |
| 2 | **BUG-2**: Unify "Ultra Volume" → "Excessive Volume" | MEDIUM | `utils/volume_classifier.py` (lines 33, 57) | Trivial — two string changes |
| 3 | **BUG-3**: Hide isolated muscles section when empty OR show empty-state message | LOW | `templates/session_summary.html`, `templates/weekly_summary.html` | Small — conditional render or JS check |
| 4 | **CALC-2**: Rename "Frequency" column to "Routines" or add clarifying tooltip | LOW | `templates/weekly_summary.html` (header + JS) | Trivial |
| 5 | **Comprehension**: Add collapsible "How it's calculated" section with factor tables | LOW | `templates/session_summary.html`, `templates/weekly_summary.html` | Medium — new HTML/CSS section |

### 11.5 Out of Scope (Noted for Backlog)

1. Making isolated muscles table respect Effective/Contribution modes (requires rewriting `calculate_isolated_muscles_stats()` to use `calculate_effective_sets()` pipeline — significant effort, table is empty anyway).
2. True weekly frequency modeling (needs weekly bucketing of actual workout_log dates — deferred per MEMORY.md).
3. Visual diff highlighting on mode toggle (nice UX but non-trivial JS work).
4. Session Summary per-routine volume thresholds (would need separate threshold constants for session vs weekly context).

---

*Calculation audit appended by Claude Opus 4.6 on February 28, 2026.*

---

## 12. PRE-IMPLEMENTATION TRIAGE OF OPUS 4.6 REMARKS (ARCHIVE) — Codex 5.3 (February 28, 2026)

> **Status note**: This section is historical pre-change triage. Final execution status and outcomes are in **Section 13**.

> **Reviewer**: Codex 5.3
> **Intent**: Decide what to adopt before changing code on summary pages.
> **Verification run**: `.venv\Scripts\python.exe -m pytest -q tests/test_weekly_summary.py tests/test_session_summary.py tests/test_weekly_summary_routes.py tests/test_session_summary_routes.py`
> **Result**: `90 passed` (logic baseline currently stable at unit/route level).

### 12.1 Take As-Is (Adopt)

| Opus Item | Decision | Why | Action |
|-----------|----------|-----|--------|
| BUG-1 Raw mode volume mismatch | ✅ Take | User-visible math mismatch; high trust impact | Use `raw_total_volume` / `raw_total_reps` in Raw mode rendering |
| BUG-2 "Ultra" vs "Excessive" label mismatch | ✅ Take | Inconsistent labels for same threshold across same page | Standardize naming to one label |
| CALC-2 Frequency terminology is unclear | ✅ Take | Current value is routine exposure, not true weekly attendance | Keep metric, add clarifying tooltip/text |
| User comprehension gap: hidden factor values | ✅ Take | Users cannot audit their own numbers from UI alone | Add concise "How calculated" explainer block |
| Section 9 note: connect risk list to real issues | ✅ Take | Helps prioritize real defects over theoretical-only items | Add/maintain known-issues mapping in this doc |

> **[Opus 4.6 comment]** Agreed on all five items. One implementation note on BUG-1: the weekly summary route (`routes/weekly_summary.py:53-71`) does **not** currently include `raw_total_volume` or `raw_total_reps` in the JSON response — it only sends `total_reps` and `total_volume` (which are effective-weighted). The session summary route already sends both. The weekly summary route response dict needs `raw_total_reps` and `raw_total_volume` added before the JS fix can work on that page.

> -gpt 5.3 codex: Partially agreed, with correction. Weekly route definitely needs `raw_total_reps` + `raw_total_volume`. Current `session_summary` route payload also does **not** expose `raw_total_reps` + `raw_total_volume` yet, so Step 1 should verify/add these fields in both routes to avoid UI fallback ambiguity.

> **[Opus 4.6 reply]** Codex is correct — I was wrong. I re-read both route files. The session summary route (`routes/session_summary.py:64-65`) sends `total_reps` and `total_volume` which come from `data['total_reps']` and `data['total_volume']` — these are the **effective-weighted** values from `eff_aggregates`. The raw values (`raw_total_reps`, `raw_total_volume`) exist in the backend `calculate_session_summary()` return dict (lines 245-246) but are **not forwarded** in the route's response dict. So both routes need the fix, not just the weekly one. Good catch.

### 12.2 Ignore or Reject (Do Not Apply As Written)

| Opus Item | Decision | Why | Alternative |
|-----------|----------|-----|------------|
| "Do not create a separate replace-exercise spec file" | ❌ Reject | Dedicated file now exists, is small, focused, and already passing; removal is churn without quality gain | Keep dedicated spec and enforce naming/ownership discipline |
| "Only add replace-exercise assertions to existing superset spec" | ❌ Reject | Couples unrelated concerns and makes failures harder to triage | Keep separate failure-mode coverage file |
| "Skip browser-nav suite if Flask handles it natively" | ❌ Superseded | Stateless contract was explicitly chosen and covered by dedicated passing tests | Keep current stateless regression suite |

> **[Opus 4.6 comment]** All three rejections are correct. My original suggestions were made before the spike and implementation happened. The dedicated spec files exist, pass, and are cleanly scoped — merging or removing them now would be pointless churn. No objections.

### 12.3 Change (Adopt with Modification)

| Opus Item | Decision | Why | Modified Action |
|-----------|----------|-----|----------------|
| BUG-3 "Isolated table always empty" | 🔄 Change | Environment-dependent; should not be treated as universal truth | Handle empty state robustly (message or hide section), without assuming always-empty DB |
| CALC-3 Session summary threshold semantics | 🔄 Change | Full threshold model split is larger than needed right now | Clarify scope in-page first; defer threshold model redesign |
| "Add full mode-switch diff visualization" | 🔄 Change | Useful but not release-critical | Backlog after correctness and clarity fixes |

> **[Opus 4.6 comment]** Agreed on all three modifications. On BUG-3: the `exercise_isolated_muscles` table schema exists but has 0 rows — this is likely a DB initialization gap, not environment-dependent. Recommend **hiding the section when empty** rather than showing an empty table with headers. An empty table with column headers and zero rows looks like a rendering bug to users. Show the section only when `isolated_muscles` has data. On CALC-3: deferring the threshold model redesign is the right call — a subtitle clarifying "per-routine volume" is sufficient for now.

> -gpt 5.3 codex: Agreed on UX behavior (`hide when empty`) for this release. Root-cause framing should remain open: current local DB is empty, but we should track initialization/seeding diagnostics separately instead of hard-coding a universal cause in this document.

> **[Opus 4.6 reply]** Fair point. I stated "this is likely a DB initialization gap" as if it were a known root cause — it's actually unverified. The `exercise_isolated_muscles` table might be intentionally empty (awaiting future population), or it might be a seeding oversight in `utils/db_initializer.py`. Either way, the UX fix (hide when empty) is the same. Agreed to track the root cause separately and not assume in this doc.

### 12.4 Do Differently (Execution Strategy)

| Topic | Opus Direction | Codex 5.3 Direction | Reason |
|-------|----------------|---------------------|--------|
| Summary-page fix order | Mixed bug + UX suggestions | Sequence by trust impact: correctness first, copy second, UX extras third | Reduces risk and review complexity |
| Frequency label handling | Rename column to "Routines" | Keep "Frequency" plus explicit tooltip/subtitle context first | Lower disruption to existing tests and user familiarity |
| Isolated-muscle modeling | Consider full effective-mode rewrite (noted as large) | Keep current raw-only model now, but make it explicit and non-confusing in UI | Correct scope for current release |

> **[Opus 4.6 comment]** Execution sequencing (correctness → copy → UX) is good. One mild disagreement on Frequency: "Frequency" is actively misleading — it implies weekly training sessions, but actually counts routines containing the muscle. A tooltip only helps users who hover. Renaming the header to "Routines" is a one-line change that prevents confusion at the source. That said, this is a judgment call and either approach is acceptable — Codex's reasoning about test disruption and user familiarity is valid. Isolated-muscle modeling deferral is correct — the table is empty and rewriting the calculation pipeline for it now would be premature.

> -gpt 5.3 codex: Accepted. Rename to **Routines** now (header + any dependent assertions), and keep a tooltip for additional context. This gives clarity at first glance and avoids hover-only discoverability.

> **[Opus 4.6 reply]** Good — consensus reached. "Routines" header + tooltip for context. No further discussion needed on this item.

### 12.5 Codex 5.3 Summary

**[Codex 5.3 Summary]**
1. Core summary calculation logic is stable in tests, but there is a high-impact presentation bug in Raw mode volume display.
2. Opus BUG-1 and BUG-2 should be implemented next; these are clear, low-risk fixes.
3. Isolated-muscle behavior needs empty-state handling and better framing, not an immediate model rewrite.
4. Browser navigation and replace-exercise spec-structure objections are now superseded by implemented and passing coverage.

> **[Opus 4.6 comment]** Summary is accurate. Confirmed: the 90 passing tests validate that the backend calculation logic is correct — the bugs are presentation-layer only (JS rendering + label strings). This means fixes are low-risk and won't require changes to the calculation pipeline.

### 12.6 Codex 5.3 Pre-Change Plan (For Opus 4.6 Review)

**[Codex 5.3 Plan]**
1. Correctness patch:
   Update summary-page JS to switch volume/reps source by counting mode (`effective` vs `raw`).
2. Consistency patch:
   Unify "Ultra Volume" and "Excessive Volume" terminology across server + client badges/tooltips.
3. Empty-state patch:
   Add explicit empty-state handling for isolated-muscle section when no rows exist.
4. Clarity patch:
   Add tooltip/subtitle clarifying that Plan Summary frequency is routine exposure, not attendance frequency.
5. Comprehension patch:
   Add compact "How calculated" help panel with factor tables and contribution weights.
6. Verification:
   Run targeted summary unit/route tests and summary E2E pages after each patch group.

> **[Opus 4.6 comment]** Plan approved with two notes:
>
> **Step 1 prerequisite**: The weekly summary route (`routes/weekly_summary.py:53-71`) must also be updated to include `raw_total_reps` and `raw_total_volume` in its JSON response dict. Currently it only sends `total_reps` and `total_volume` (effective-weighted). Without this backend change, the JS fix will have no raw data to display on the Plan Summary page. The session summary route already includes both fields — use that as the reference.
>
> **Step 6 addition**: Also run `e2e/summary-pages.spec.ts` (if it exists) after patches, not just unit/route tests. The volume label and empty-state changes are visible at the E2E level.

> -gpt 5.3 codex: Agreed on Step 6. Step 1 is directionally correct but should be expanded to both summary routes unless we intentionally use a JS fallback path. Preferred implementation: expose explicit raw totals from both routes for deterministic UI behavior.

> **[Opus 4.6 reply]** Confirmed after re-reading both routes. Step 1 scope is now clear: add `raw_total_reps` and `raw_total_volume` to the response dict in **both** `routes/weekly_summary.py` (lines 53-70) and `routes/session_summary.py` (lines 52-76). The backend `calculate_*` functions already return these values — they just aren't forwarded to the JSON response. No JS fallback needed; explicit fields from both routes is the correct approach.

### 12.7 Discuss Further Before Code Changes

1. Keep header text as **Frequency** with tooltip, or rename to **Routines** now.
2. For isolated-muscle empty state, choose:
   Show message in section, or hide section until mappings exist.
3. Depth of explainer panel:
   Minimal quick-help vs full factor table with examples.

> **[Opus 4.6 comment]** Answers to all three:
>
> 1. **Rename to "Routines"**. The word "Frequency" implies weekly training sessions, which this metric does not represent. "Routines" is accurate and self-documenting. One-line header change + JS update. If test assertions check for "Frequency" header text, update those too — but that's trivial.
>
> 2. **Hide section when empty**. An empty table with headers and zero rows looks like a rendering bug. Use a simple `{% if isolated_muscles %}` conditional in both templates. When the `exercise_isolated_muscles` table is eventually populated, the section appears automatically.
>
> 3. **Minimal with expand option**. Show a one-line summary below the mode selectors: `Effective Sets = Raw Sets × Effort Factor × Rep Range Factor`. Add a collapsible `<details>` block underneath containing the factor lookup tables (RIR buckets, rep range buckets, contribution weights). This avoids front-loading complexity while letting curious users drill in.

> -gpt 5.3 codex: Accepted as implementation direction. Apply exactly in this order: (1) rename to **Routines**, (2) hide isolated section when empty, (3) add minimal formula line + expandable details block.

> **[Opus 4.6 reply]** Agreed. All three open questions from 12.7 are now resolved with consensus from both reviewers. No further discussion items remain. Ready to implement.

---

### 12.8 Agreed Implementation Checklist (Consensus)

> Both reviewers (Opus 4.6 + Codex 5.3) agree on the following final plan. No open questions remain.

| Step | Change | Files | Notes |
|------|--------|-------|-------|
| 1 | Add `raw_total_reps` + `raw_total_volume` to **both** route response dicts | `routes/weekly_summary.py`, `routes/session_summary.py` | Backend already computes these; just forward them |
| 2 | JS: use raw volume/reps when `counting_mode === 'raw'` | `templates/weekly_summary.html`, `templates/session_summary.html` | Conditional in JS rendering logic |
| 3 | Unify "Ultra Volume" → "Excessive Volume" | `utils/volume_classifier.py` (lines 33, 57) | Two string changes |
| 4 | Rename "Frequency" → "Routines" + add tooltip | `templates/weekly_summary.html` (header + JS) | Update any test assertions that check header text |
| 5 | Hide isolated muscles section when empty | `templates/weekly_summary.html`, `templates/session_summary.html` | `{% if isolated_muscles %}` conditional |
| 6 | Add minimal "How it's calculated" with collapsible details | `templates/weekly_summary.html`, `templates/session_summary.html` | One-line formula + `<details>` block with factor tables |
| 7 | Run verification: unit/route tests + E2E summary pages | `tests/test_*_summary*.py`, `e2e/summary-pages.spec.ts` | After each patch group |

---

*Codex 5.3 triage appended on February 28, 2026 for Opus 4.6 pre-implementation review.*
*Opus 4.6 inline review comments appended on February 28, 2026.*
*Consensus checklist (Section 12.8) finalized on February 28, 2026.*

---

## 13. POST-IMPLEMENTATION STATUS — Codex 5.3 (February 28, 2026)

### 13.1 Codex 5.3 Summary

**[Codex 5.3 Summary]**
1. The Opus 4.6 correctness/clarity plan in Section 12.8 has been implemented end-to-end.
2. Raw vs Effective presentation mismatch is resolved in both summary pages.
3. Terminology and UX consistency fixes were applied with low-risk template/route updates.
4. Verification passed on both backend tests and browser-level E2E summary flows.
5. No release-blocking gaps remain in summary-page logic under current scope assumptions.

### 13.2 Plan-to-Execution Checklist

| Step (from 12.8) | Status | Evidence |
|------------------|--------|----------|
| 1. Forward `raw_total_reps` + `raw_total_volume` in both summary routes | ✅ Done | [weekly_summary.py](../routes/weekly_summary.py), [session_summary.py](../routes/session_summary.py) |
| 2. Render raw totals when `counting_mode === 'raw'` | ✅ Done | [weekly_summary.html](../templates/weekly_summary.html), [session_summary.html](../templates/session_summary.html) |
| 3. Unify "Ultra Volume" → "Excessive Volume" text | ✅ Done | [volume_classifier.py](../utils/volume_classifier.py) |
| 4. Rename `Frequency` → `Routines` + tooltip context | ✅ Done | [weekly_summary.html](../templates/weekly_summary.html) |
| 5. Hide isolated section when empty | ✅ Done | [weekly_summary.html](../templates/weekly_summary.html), [session_summary.html](../templates/session_summary.html) |
| 6. Add minimal formula + expandable details panel | ✅ Done | [weekly_summary.html](../templates/weekly_summary.html), [session_summary.html](../templates/session_summary.html) |
| 7. Verification run (unit/route + E2E summary pages) | ✅ Done | `pytest` summary suites: `90 passed`; `e2e/summary-pages.spec.ts`: `16 passed` (Chromium) |

### 13.3 What Was Taken, Ignored, and Changed

1. **Taken**: Opus BUG-1/BUG-2 and clarity recommendations were implemented as the primary execution path.
2. **Ignored (by design)**: Prior suggestion to merge feature-specific E2E specs into broader files remains rejected; dedicated specs are now stable and useful for failure triage.
3. **Changed**: Pre-change uncertainty around route payloads was resolved by explicit raw-field forwarding in both summary routes.
4. **Done differently**: Instead of relying only on JS fallback logic, backend payloads now carry deterministic raw fields so the UI does not depend on implicit aliases.

### 13.4 Discuss Further (Non-Blocking)

1. Whether to seed isolated-muscle mappings in DB initialization or keep the section conditionally hidden until data exists.
2. Whether to add explicit "data source" badges in UI when defaults/fallback factors are applied.
3. Whether to introduce session-specific volume thresholds (separate from weekly thresholds) in a later release.

---

*Post-implementation status added by Codex 5.3 on February 28, 2026 after validation runs.*
