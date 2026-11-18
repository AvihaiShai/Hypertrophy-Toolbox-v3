# Plan Review — Workout sets and reps bounds (#596, AUD-1268)

**Status** — Gate 0 approved on 18 November 2026. All three council reviewers rereviewed Plan v2 and cleared their Plan v1 blockers. The owner approved Gate 1 on 18 November 2026 with two scope reductions recorded below. Implementation is authorized under that approved scope.

**Planning size** — Large because plan, log, import and program restore write contracts change together. [Quality Gate](../ai_workflow/QUALITY_GATE.md#plan-stage-routing)

## Section 0 — Requirements Brief

**Raw request** (verbatim excerpts)

> handle those item where we left off using multiple agents to close those issues\items until it get done end to end.
>
> in case  you are waiting for decisions - span the ai consulting team for each item that pending for decision.

Owner’s approval on 18 November 2026:

> Approve all below. For #596, the restore result must state how many rows were skipped and why.

**Problem**

At `ad6f739b`, accepted negative prescriptions produced negative totals in analysis and the workbook. The current shared validator compares rep bounds but allows negative and fractional values, and plan sets bypass it. The browser can truncate a fraction before submission. The log page also treats a saved score of zero as an empty cell on reload. [Issue #596 and revalidation](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/596)

**Acceptance criteria**

1. Given a new plan row or a plan edit, accept positive whole numbers for sets, minimum reps and maximum reps. Require minimum reps to be at most maximum reps when both are usable. Reject zero, negative, fractional, blank, null, malformed, nonfinite and boolean counts on add or when supplied in an edit. Keep compatible whole-number strings used by existing clients. A rejected write returns HTTP 400 `VALIDATION_ERROR` and preserves all the row’s fields. Browser controls must preserve an invalid typed value long enough to reject it, without truncating it into a different valid value.
2. Given a workout log edit, accept whole-number scored minimum and maximum reps from zero upward. Keep minimum reps at most maximum reps when both are usable. Preserve null and empty-string clears, omitted fields, and the 400 validation envelope. Show a confirmed zero as `0` immediately after saving, when reopening the editor, and after reload. Show a clear as empty and retain the last confirmed display on a rejected change.
3. Given an existing row with an invalid count, a user can correct that field directly, repair both rep bounds together, or edit an unrelated field. A malformed or now out-of-bounds untouched companion cannot block repair. Valid companion values still enforce ordering. Legacy scored blanks remain displayable and repairable. Existing data is changed only by the user’s explicit edits and normal restore replacement.
4. Given one invalid prescription in the active plan, importing the plan into the log returns HTTP 400 `VALIDATION_ERROR` before any log row is written, with the routine, exercise and reason available through the existing annotation. A valid import keeps its copy and duplicate behavior.
5. Given a confirmed program restore with rows that fail bounds validation, the result reports the count skipped and each affected row’s routine, exercise and reason. Missing catalog rows retain their own count and reason. Counts are explicit when every row is skipped as well as in mixed results. Existing replace-mode and ADR-015 execution-field refusal semantics apply, with the existing REST response fields and statuses.
6. Given a healthy existing plan or log, preserve existing calculation rules, valid write results and export shape. Add no product maximum for sets or reps. Values must be representable for storage.

**Calculation surface**

- No calculation-function change. Ingress protects existing calculations. For example, with one primary-muscle prescription of `sets = -2`, reps `8–8`, and 50 kg, today the accepted row can contribute `-2` raw sets, `-16` reps, and `-800` kg-volume in applicable summary/Excel totals. After the fix that submission returns HTTP 400 and contributes no new row to any total. A valid two-set prescription still contributes `2` raw sets, `16` reps, and `800` kg-volume under the same counting conditions.
- The PR will document the stricter input boundary, existing-row repair, restore reporting and unchanged formulas. Regression coverage will connect the rejected write to unchanged summary and workbook totals.

**In scope**

- AUD-1268 across plan Add and inline edits, scored-log reps, plan-to-log import, and program backup restore.
- User-visible feedback for rejected writes, scored zero and clearing, and skipped restore rows.
- Regression coverage and product documentation for the changed workflows.

**Out of scope / non-goals**

- RPE policy, weight and RIR bounds, additional limits from AUD-0818, and changes to assistance or progression formulas. Existing responsive controls and dedicated error paths retain their own scope.
- AUD-0896 legacy toast migration, AUD-0938 D4 Packet C, AUD-0894 toast misuse diagnostics, and AUD-0927 duplicate-toast revalidation. Keep their existing dispositions and evidence levels.
- Schema constraints, a data migration, startup cleanup, changes to the generator’s prescriptions, or file-level disaster recovery.

**Assumptions made**

- No product assumptions pending. Keep the tested lower-level import compatibility for actual `None` rep bounds where those values exist out of band. The active plan schema requires both rep bounds and new plan writers reject null. [Import compatibility tests](../../tests/test_export_blank_rep_bounds_gate0.py)

**Open questions for the user**

- None at Gate 0.

### Section 0 sign-off — GATE 0

- [x] The owner approved the acceptance criteria in the 18 November 2026 conversation with the restore reporting requirement quoted above.
- [x] No product assumptions require separate approval.
- [x] Blocking questions are answered.

## Plan v1

**Goal** — Prevent invalid counts from entering new prescriptions or scores while keeping past entries repairable and making restore exclusions explicit.

**Scope**

- **In** — Shared count validation, targeted write-path adoption, accurate repair and display behavior, and explicit counts and reasons on the existing restore result.
- **Out** — Deferred leads listed in Section 0, stored-data cleanup, analytics changes, and new response fields or migration operations.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/workout_validation.py` | Modify | Share exact whole-number parsing and per-call-site minimums and clear rules. Keep existing weight/RIR validation and the existing invalid-number wording where pinned. |
| `routes/workout_plan.py`, `utils/exercise_manager.py` | Modify | Validate plan add at its service entry point and retain the route contract. Validate plan inline writes and compare rep siblings within the same write transaction. |
| `routes/workout_log.py`, `utils/workout_log_service.py`, `utils/workout_log.py` | Modify as needed | Keep the update response shape. Validate scored rep edits, canonicalize new rep clears to SQL `NULL`, and keep legacy nonnumeric or blank rep values from breaking the log page while leaving those rows editable. |
| `utils/export_service.py`, `utils/rep_range_integrity.py` | Modify | Align the plan-to-log validator and diagnostic on sets and reps. Retain the narrower read-only predicate used to diagnose arithmetic failures in summary pages. |
| `utils/program_backup.py`, `routes/program_backup.py` | Modify | Validate plan sets and rep bounds during restore. Report missing-catalog and invalid-bounds counts in the existing result message and retain row details in `invalid`. Preserve all existing response keys. |
| `templates/workout_log.html`, `static/js/modules/workout-log.js`, `static/js/modules/ui-handlers.js` | Modify | Render scored zero as a number. Validate the actual scored rep fields and present only confirmed values through the edited-cell lifecycle. |
| `static/js/modules/workout-plan-add-exercise.js`, `static/js/modules/workout-plan-helpers.js`, `static/js/modules/workout-plan-table.js` | Modify as needed | Prevent truncation before validation. Retain normal successful payloads and inline behavior. Show actionable field validation when the request is rejected. |
| `static/js/modules/backup-center.js` | Modify | Show actual skip counts and reason groups, including outcomes that restore zero rows. Use the existing escaped per-row renderer and existing result panel. |
| Existing route, util, Vitest and E2E test files listed below; `docs/test_inventory/` | Extend | Exercise the real entry points and regenerate inventory for added or renamed cases. |
| `docs/product/APP_FLOW.md` and PR description | Modify | Document the Plan, Log and Backup outcomes and compatibility notes. |

**Effort** — L. **Owner** — #596 implementation lane after Gate 1. **Depends on** — one coordinated checkout slot. Coordinate overlap with #637 in Workout Log and #631 in export, and rerun affected regression checks after integrating either packet.

**Sequence**

1. Add or extend boundary coverage in existing tests. Pair invalid input with a successful control and verify persisted rows through scratch DB fixtures. Use the Work Log edit tests and direct service test paths so client-side checks cannot mask an ingress gap.
2. Extend the shared validator for count fields. Accept mathematically integral finite numbers and equivalent decimal numeric strings within the signed SQLite integer representation, including current string payloads. Compare and persist counts without a lossy float conversion, rounding or truncation. Reject nonnumeric shapes and values outside storage representation as validation errors. Preserve request syntax, unrelated numeric parsers, and the original value of an omitted field. Reject a malformed two-field patch as a unit. When comparing one supplied rep bound with a stored sibling, evaluate the sibling under the applicable count policy and skip the comparison if that sibling independently cannot be used. Keep separately stored unrelated fields out of validation. Hold the SQLite write transaction across this read, comparison, and write using `DatabaseHandler`. Preserve scored calibration invocation after a successful score write and the existing handling of recomputation failure.
3. Apply the positive lower bound in the plan-to-log preflight, before duplicate lookup or any insert, and use the same validation for the row diagnostic and its `sets` projection. Preserve exact-blank rejections, the service seam’s actual-null rep compatibility, and healthy copy behavior. Keep analysis diagnostic calls on their prior numeric-value policy so a legacy negative or fractional count doesn’t get named as the cause of an unrelated read failure. Generated prescriptions already use `max(1, scaled)` and positive rep tables. Verify that producer through its existing tests, without touching generator semantics.
4. Extend the program restore predicate to include sets. Maintain the current ordering of catalog checks, invalid-bounds classification and ADR-015 refusals. A confirmed restore with valid and invalid rows writes only the valid rows and reports the others. A confirmed restore with no restorable rows retains the existing replace-mode behavior. The API `message` and the Backup Center result state how many rows were skipped by reason group using existing `skipped` and `invalid` lists. The result panel identifies each invalid row and its field-specific reason. Leave the error contract and no-write execution refusal flow intact.
5. Adjust the three UI flows. Replace plan Add’s truncating `parseInt` for the three count inputs with lossless handling compatible with the existing valid payload. For scored reps, wire the actual `scored_min_reps` and `scored_max_reps` field identities through the existing editor and avoid displaying unsaved text on blur or Enter. A rejected request keeps the previous confirmed cell, including a stored zero. Treat an older scored blank as missing in display/comparison without rewriting it. Keep the existing escaped restore list and show numeric skip counts even for all-skipped cases.
6. Record test and review evidence for the final patch, update app-flow docs, then prepare one issue-linked PR with migration notes for publish and merge under the existing repo approval flow.

**Expected gates** (test-strategist to confirm)

- Pytest route and app factory gates in `tests/test_workout_plan_routes.py`, `tests/test_workout_log_routes.py`, `tests/test_exports.py`, `tests/test_program_backup.py`, and `tests/test_app_factory.py`. Include add and inline edits with 0/1, numeric and string values, false/true, fractions, malformed values, nonfinite input, unrepresentably large input, ordered/equal pairs, and unchanged state after rejection. Exercise the smallest legal score and a persisted clear. Include a concurrent partial-edit regression if a transaction seam provides a deterministic oracle.
- Pytest utility and compatibility gates in `tests/test_workout_log_utils.py`, `tests/test_workout_log_calibration_route.py`, `tests/test_rep_range_integrity.py`, `tests/test_export_blank_rep_bounds_contract.py`, `tests/test_export_blank_rep_bounds_gate0.py`, `tests/test_program_backup_restore_fuzz.py`, `tests/test_program_backup_execution_fields.py`, and `tests/test_export_weekly_summary_sheet.py`. Exercise matching import diagnostics, whole-batch rejection, mixed and all-skipped restore reporting, ADR-015 no-write refusal, usable/unusable sibling repair, confirmed count storage, and the unaffected valid summary/XLSX totals. Add a focused production-path generator invariant if existing coverage does not pin the relevant output.
- Chromium `workout-plan`, `exercise-interactions`, `superset-edge-cases`, `workout-log`, `program-backup`, `validation-boundary`, `error-handling`, `empty-states`, `accessibility`, and `api-integration`, plus any affected mapped specs from the final diff. Cover an actual Add fraction, inline no-write failure, scored 0/reload/clear, rejection without a false display, and explicit mixed/all-skipped restore counts and row reasons. Manually smoke the edited inputs and restore result against the disposable runtime. Preserve existing Vitest seams for valid request payloads.
- Run the full verification and polish gate for this cross-workflow change. Regenerate and check test inventory and run the pyright baseline check. Use independent `code-reviewer` and `unslop-reviewer` plus `product-risk-reviewer` for the changed ingress and downstream impact. Use no live user database or visual baseline regeneration.

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `/root/bounds_consult` | Section 0 and Plan v1 author. |
| `product-manager` — response matrix + Plan v2 | `/root/bounds_consult` | Resumed for Step 4. |
| `architecture-reviewer` | `/root/log_consult` | Plan v1 reviewer, Plan v2 rereview passed. |
| `test-strategist` | `/root/summary_consult` | Plan v1 reviewer, Plan v2 rereview passed. |
| `product-risk-reviewer` | `/root/firefox_consult` | Plan v1 reviewer, Plan v2 rereview passed. |

**Same product-manager resumed for the matrix + Plan v2?** Yes, by the manager’s follow-up to `/root/bounds_consult`.

**Evidence gap** — none.

## Reviewer findings

### architecture-reviewer (agent `/root/log_consult`)

- **Blocking, Plan v1 §Sequence 4 — Count actual missing-catalog rows before names are de-duplicated.** `utils/program_backup.py:638` converts the list to unique names, and `static/js/modules/program-backup.js:78` returns only `data`, dropping the envelope message. Two routines with the same retired exercise produce two skipped rows but currently render a count of one. Keep the unique-name `skipped` list and existing response keys. Compute actual counts pre-dedup, place them in the existing response message, and plumb that message through the sole Restore client into the result/panel and toast beside the existing escaped row-details list. Alternatively obtain express approval for an additive numeric count field. Add a repeated-retired-name fixture across routines with invalid-bounds rows and assert mixed/all-skipped actual counts and reasons in HTTP and UI.
- **Blocking, Plan v1 §Sequence 2 — Specify a lock-safe atomic range update for both Plan and Log.** `utils/database.py:318` does not treat BEGIN as a write and `:323` only acquires `_DB_LOCK` for the DML statement; its SQLite busy timeout is 30s (`:84`). A naive BEGIN IMMEDIATE → sibling read → locked UPDATE can deadlock temporarily with another `_DB_LOCK` holder waiting on SQLite. Use an atomic UPDATE that guards against a changed sibling and retries/revalidates on a lost race, or a DatabaseHandler transaction API that takes the process lock before the SQLite write lock and releases it after commit or rollback. Add deterministic concurrency coverage on both routes. Preserve missing-row behavior and run scored calibration after the score commit.
- **Blocking, Plan v1 §Sequence 2 — Enforce the planned exact HTTP number contract at decoding.** `routes/workout_plan.py:86,357` and `routes/workout_log.py:45` currently use Flask `request.get_json()`, which decodes decimal JSON literals to binary floats before shared validation. `9007199254740992.5` becomes an apparently integral 9007199254740992, and the integral `9223372036854775807.0` can round out of range. Preserve unrounded tokens for the affected counts at ingress only or get owner agreement to narrower wire-number semantics. Keep exact integer strings, unaffected numeric fields, and existing error behavior. Add raw-JSON HTTP cases for both examples (including persisted exactness of accepted integer inputs), because fixture `json=` can round the value before it reaches Flask.
- **Verdict: Blocking issues.** Fix the actual-count transport, the concurrent sibling-write mechanism, and the exact HTTP decoding contract in Plan v2. The module boundaries, existing envelopes, schema decision and nonnumeric write fields are otherwise within the architecture.

### test-strategist (agent `/root/summary_consult`)

#596 test-strategist verdict: FULL `/verify-and-polish` required, Plan v1 needs the following corrections. Blocking T596-1 Restore row-count oracle: `utils/program_backup.py:637–656` returns deduplicated missing exercise names, so `len(result.skipped)` is not the count of skipped rows. Plan v2 must carry the count of raw missing rows to both the existing API `message` and Backup Center, preserving response fields/status and per-row invalid reasons. Cover the same missing name in two routines plus one invalid row, in both mixed and zero-restorable cases, in `tests/test_program_backup.py` or `test_program_backup_restore_fuzz.py` and `e2e/program-backup.spec.ts`. Assert both existing user-facing result panel and toast convey the actual counts where they report exclusions. Blocking T596-2 Browser rejection oracle: `e2e/validation-boundary.spec.ts:91,100,191,200,311,320` currently pins clamp/truncating saves. Replace those contradictory cases with no-write rejection, visible feedback and exact pre-/post-blur input/unchanged persisted table assertions; control `:109` negative max, add max-rep fraction and zero as applicable, and preserve decimal weight/positive-large cases. Both the `change` clamp in `workout-plan-add-exercise.js:333–347` and `parseInt` in `workout-plan-helpers.js:162–164` can mask invalid input. Test an inline valid value above existing input.max hints (sets >10, reps >30) to prove no product cap. Preserve or explicitly migrate affected Vitest builder tests in `static/js/modules/__tests__/workout-plan-helpers.test.js` and regenerate inventory. Blocking T596-3 Gate omissions: DB/schema row matches `utils/program_backup.py`, so add independent architecture-reviewer and explicit manual backup + restore smoke. Full pytest + Chromium `/verify-suite`, `code-reviewer`, `unslop-reviewer`, product-risk review, inventory check and pyright remain required. Nonblocking T596-4 (pin boundary/state oracles): use exact values around IEEE integer safety plus signed SQLite edges in backend tests, SQL `typeof`/value and 400/no-write assertions, mixed two-field rejection and repair with an independently unusable stored sibling. Add `tests/test_exercise_manager.py`, `tests/test_workout_plan_service.py`, `tests/test_error_page_contract.py` and `tests/test_weekly_summary.py` to explicit affected targets (full pytest already covers). For import, use a valid candidate before a bad duplicate or otherwise non-inserting row and assert zero added, targeted annotation and no duplicate bypass. Retain null compatibility witnesses. Preserve historical `program-backup.spec.ts:79` flake evidence if encountered and remeasure in isolation; no conftest or baseline changes.

### product-risk-reviewer (agent `/root/firefox_consult`)

#596 product risk — revision required, blocking issue is pre-dedup missing-row count; UI helper currently discards envelope `message` (`program-backup.js:78–85`), so Plan v2 should carry that message to Backup Center through a backward-compatible wrapper option and use it for summary without parsing English or changing REST fields. Also should-fix exactness: Decimal in the validator after default Flask JSON float decode cannot recover a decimal/exponent input’s original value (`9007199254740993.0` already rounds); specify exact handling at affected ingress and decimal-looking browser input without `Number` rounding before submission, or precise handling of representational limits agreed with owner; retain unrelated parsers. Existing `SUM(us.sets)` can overflow across SQLite-width inputs, and #631 will surface it rather than hide the panel. Record this as an inherited storage-vs-analysis limitation, without adding a product max or changing formulas in #596. Migration notes and product scopes otherwise hold.

One more #596 Plan v2 should-fix: scored rep editors are `<input type="number">` at templates/workout_log.html:129–151. Malformed typed text can produce DOM `.value === ''` while `validity.badInput` is true, colliding with valid explicit empty clear. Validate badInput before empty-string clearing, and cover malformed input preserving a persisted zero and an intentional blank clearing it. This is separate from fraction rejection/rounding.

## Response matrix

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| Actual restore row count and existing transport | `architecture-reviewer` | Accept | Capture counts before name deduplication. Keep `data` and send an authoritative existing `message` to the panel and toast. |
| Race-safe partial rep writes | `architecture-reviewer` | Accept | Guard the atomic write with the observed persisted values, re-read on a lost guard, and test both edit endpoints under a deterministic race. Run score calibration after commit. |
| Exact HTTP numerical ingress | `architecture-reviewer` | Accept | Retain original number lexemes only at the five affected fields and preserve ordinary Flask decoding elsewhere. Pin raw JSON and SQLite controls. |
| Owner-visible skipped-row counts and explanations | `product-risk-reviewer` | Accept | Report the actual count and reasons in the existing message and restore UI. Exercise mixed and all-skipped repeated-name cases. |
| Preserve invalid browser input and distinguish invalid input from clear | `product-risk-reviewer` | Accept | Remove count clamp and integer truncation. Check `badInput` before mapping blank to clear; assert a confirmed zero survives a rejected edit. |
| Technical integer limit and inherited extreme-count overflow | `product-risk-reviewer` | Accept | Document exact storage support and existing analytical overflow at extreme values in the migration notes. Leave calculations and product maxima alone. |
| Restore row-count oracle (T596-1) | `test-strategist` | Accept | Cover repeated retired names and invalid rows, both with and without a valid row, through HTTP and both visible restore channels. |
| Browser rejection oracle (T596-2) | `test-strategist` | Accept | Replace the contradictory clamp/truncation assertions and add pre/post blur, unchanged state, max-rep and above-hint witnesses. Update builder Vitest cases. |
| Complete change-type gate union (T596-3) | `test-strategist` | Accept | Add explicit manual backup + restore and architecture review. Run full verification, remaining independent reviews, inventory and pyright. |
| Numeric and state regression witnesses (T596-4) | `test-strategist` | Accept | Add exact raw JSON, SQL-type, repair and invalid duplicate cases to the named targets and retain null compatibility and flake evidence. |

## Plan v2

The text here records the version the council rereviewed. The [Gate 1 scope reductions](#gate-1-owner-approval-and-scope-reductions) supersede the two specified implementation and test requirements.

**Goal** — Prevent invalid plan and score counts from being recorded, let users repair legacy values, and report exactly how many backup rows were skipped and why.

**Scope**

- **In** — The five count fields at the three write endpoints, persisted plan validation for plan-to-log import and program restore, repair and rejected-edit behavior, and the existing Backup Center restore result.
- **Out** — Changes to the wire envelope or schema, new maxima for sets or reps, formula changes, historical data cleanup, changes to the generator, and the other deferred #596 leads in Section 0.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/workout_validation.py`, `routes/workout_plan.py`, `routes/workout_log.py` | Modify | Exact count conversion and narrowly applied HTTP token decoding. Keep omitted and unrelated values and normal response handling. |
| `utils/exercise_manager.py`, `utils/workout_log_service.py`, `utils/workout_log.py` | Modify | Validate direct plan Add, apply race-safe scored edits, preserve post-commit calibration and make older malformed rep values displayable and repairable. |
| `utils/export_service.py`, `utils/rep_range_integrity.py` | Modify | Match import validation and its diagnostic against the same persisted count values, with existing read-diagnostic and null compatibility. |
| `utils/program_backup.py`, `routes/program_backup.py` | Modify | Classify numeric-invalid rows, retain existing typed direct service result, and carry pre-dedup counts privately to the route’s existing success message. |
| `static/js/modules/program-backup.js`, `static/js/modules/backup-center.js` | Modify | Preserve the message from the restore response through a backwards-compatible client option. Display it as text in the existing panel and toast, and reuse escaped reason details. |
| `static/js/modules/workout-plan-add-exercise.js`, `static/js/modules/workout-plan-helpers.js`, `static/js/modules/workout-plan-table.js` | Modify | Preserve typed count text through validation, stop clamping counts at Add, and show the validation result without turning the inline hints into limits. |
| `templates/workout_log.html`, `static/js/modules/workout-log.js`, `static/js/modules/ui-handlers.js` | Modify | Keep scored zero visible and editable, reject invalid number input before mapping a genuine clear to `NULL`, and update the display on confirmed saves. |
| Existing pytest, Vitest and Playwright targets below, `docs/test_inventory/` | Extend | Pin exact numbers, no-write failures, concurrency, restore count correctness and valid behavior. Regenerate inventory from the existing producer. |
| `docs/product/APP_FLOW.md`, implementation PR | Update | Explain tightened ingress, legacy repair, count reporting, storage constraints and the inherited extreme-count limit in analysis. |

**Sequence**

1. Write production-path regressions before implementation. For each validator family, exercise successful boundary witnesses and failures that preserve every previously persisted value. Use scratch `DatabaseHandler` fixtures. This packet needs a coordinated editing and testing slot because #637 shares Log files and #631 shares export surfaces. Re-run any affected suites after integrating those packets.
2. Decode exact count values only on `POST /add_exercise` (top-level `sets`, `min_rep_range`, `max_rep_range`), `POST /update_exercise` (those same keys under `updates`), and `POST /update_workout_log` (`scored_min_reps`, `scored_max_reps` under `updates`). Keep Flask’s existing decode for all ordinary fields and body-level behavior. Use the cached raw request to make a second decode with original JSON number lexemes, then overlay only the targeted fields at the indicated shape. Keep exact decimal numeric strings compatible. Distinguish JSON number tokens from strings and booleans, preserve duplicate-key handling and missing fields, and keep MIME, syntax and unrelated number semantics. Parse the target values losslessly, reject nonfinite, fractional, disallowed null and out-of-storage values with the existing 400 envelope, and persist an exact SQLite integer. Treat mathematically integral forms, including an integral decimal literal, as integers. Canonicalize only new scored rep clears, `null` and exact `""`, to SQL `NULL`. Add raw-body tests for `9007199254740992.5` (reject), `9223372036854775807.0` (persist exactly), `9223372036854775808` (reject), and an exact supported value around the IEEE integer boundary. Assert SQLite value and `typeof()` for positives and 400 plus unchanged state for rejections. Keep weight, RIR and RPE handling intact.
3. Apply per-field bounds and conditional ordering at both edit endpoints. When only one rep bound changes, read both stored rep values, classify the untouched sibling independently, and enforce the pair only when both usable. Use a single conditional `UPDATE` through the ordinary `DatabaseHandler` write path, guarding the observed rep pair with null-safe `IS` predicates. An intervening write makes the guard fail. Re-read and revalidate on a lost guard, with a bounded retry and the existing route failure envelope if contention persists. A missing row after re-read keeps each endpoint’s current missing-row behavior. A pair edit validates both supplied values and writes them atomically. Unrelated edits cannot fail because of a legacy count. Avoid acquiring SQLite’s write lock before the handler’s existing process lock. Use two coordinated requests on each endpoint, with `8–12` initially and competing `min = 11` and `max = 9`, each valid against the original row. Prove one commit, one revalidated 400 and an ordered final pair. Cover invalid untouched sibling repair, both-field repair, and invalid mixed-field edit with no write. On Log, run calibration once after the committed score write, with the existing success response and error isolation. Prove the rejected request does not recompute calibration.
4. Apply the Plan policy to new rows and persisted counts. For plan-to-log import, keep the complete validation before duplicate lookup or any write, including a bad count on an otherwise skipped duplicate. Return the existing error with a validator-matched routine, exercise and reason. Preserve the previous export seam for absent legacy rep bounds, its numeric-string copy and exact-blank failure, and its duplicate behavior for valid rows. Give the diagnostic the same fields, including `sets`, and the same policy. Keep the lighter predicate for analysis arithmetic failures so valid numeric values under the old contract cannot be blamed for unrelated read failures. Characterize the generator’s positive integral count outputs using its existing production-path coverage. A count can fit SQLite storage and still trigger inherited `SUM()` overflow if extreme valid counts are combined in analysis. Document that limitation in the PR and retain the current formulas.
5. Validate program restore counts at its current per-row classification point after catalog lookup and before execution-field refusal checks. Compute `missing_row_count` from raw rows before deduplicating names, and `invalid_row_count` from the one-entry-per-row `invalid` list. Carry the counts internally to the route while preserving the direct service’s existing result and HTTP keys. The route builds the authoritative existing success `message` with total skipped rows and counts by reason. For example, a restore with one valid row, a repeated missing name in two routines and one invalid sets row should report three skipped rows, two missing from the catalog and one invalid, while `skipped` retains its single unique name and `invalid` holds the detailed row reason. The Backup Center asks its restore client for the envelope while the helper keeps its existing default result shape. Render the message verbatim as text in both the persistent panel and toast, using the arrays for detail lists without deriving a row count or parsing the message. The existing escaped detail lists explain each invalid row. Cover the same fixture with and without the valid row, and retain clean, all-invalid and all-catalog-missing controls. Leave replacement behavior, transactional rollback and no-write ADR-015 refusal intact.
6. Make the actual browser behavior reflect the server contract. Exclude the three Plan Add count controls from `initializeDefaultValues()`’s `change` clamp and replace `parseInt` payload conversion with lossless input text for those fields. Preserve independent weight, RIR/RPE and normal controls. Keep plan inline text lossless and show safe server field validation where the write fails. Treat its current maximums of 10 sets and 30 reps as hints; edits above them must still succeed. On the log, check native number validity’s `badInput` before any whitespace or `""` becomes a clear. Cancel any pending invalid scored save and leave the last confirmed display visible. Confirm zero, reopen, reload and genuine clear, and exercise browser-invalid syntax after a persisted zero. Keep Escape and Enter compatible with the confirmed-cell behavior, and avoid having one event path save invalid or in-flight text. Keep signed negative and fractional input rejected.
7. Verify, review and prepare the issue-linked PR with the Change Type gates below. Record the UI and HTTP behavior and calculation impact in migration notes. Document the actual numbered restore result and preserve all other audit dispositions before closure under the existing gate and merge flow.

**Required gates**

- Run full pytest and Chromium `/verify-suite` through `/verify-and-polish`. Explicit backend targets are `tests/test_workout_plan_routes.py`, `tests/test_workout_plan_service.py`, `tests/test_exercise_manager.py`, `tests/test_workout_log_routes.py`, `tests/test_workout_log_utils.py`, `tests/test_workout_log_calibration_route.py`, `tests/test_exports.py`, `tests/test_export_blank_rep_bounds_contract.py`, `tests/test_export_blank_rep_bounds_gate0.py`, `tests/test_rep_range_integrity.py`, `tests/test_program_backup.py`, `tests/test_program_backup_restore_fuzz.py`, `tests/test_program_backup_execution_fields.py`, `tests/test_weekly_summary.py`, `tests/test_export_weekly_summary_sheet.py`, `tests/test_error_page_contract.py`, and `tests/test_app_factory.py`. Run affected additional direct call tests from the final path list. Assert no-write behavior and specific failure messages, the invalid duplicate import case before any insert, preserved valid workbook totals, and intact null and legacy repair behavior.
- Explicit Chromium coverage includes `workout-plan`, `exercise-interactions`, `superset-edge-cases`, `workout-log`, `program-backup`, `validation-boundary`, `error-handling`, `empty-states`, `accessibility`, and `api-integration`. Replace the six contradictory clamp/truncation cases at `e2e/validation-boundary.spec.ts:91,100,191,200,311,320` with rejection and unchanged-state assertions. Check raw pre-/post-blur input and visible feedback. Keep the negative max-rep control at line 109 as a rejection, preserving raw submitted input or proving no request. Add max-rep zero and fraction, above-hint inline success, and retain the valid wide count and decimal-weight controls. Demonstrate a persisted zero survives a browser-invalid edit, while a true clear remains empty. Exercise the actual restore result and toast counts, with duplicate missing names across routines, in mixed and zero-restorable cases. If the historical backup flake recurs, retain its receipt and remeasure in isolation with current repo rules.
- Update the affected builder expectations in `static/js/modules/__tests__/workout-plan-seams.test.js` and `workout-plan-helpers.test.js` as needed. Run Vitest, regenerate inventory and run its check, and run the pyright baseline diff. Perform a manual backup + restore smoke against disposable data alongside interactive plan and log smoke.
- Independent implementation `architecture-reviewer` (including `utils/program_backup.py`), `code-reviewer`, `unslop-reviewer`, and `product-risk-reviewer` are required. Use the existing review and approval flow. Tests use disposable databases and existing baselines.

### Council rereview

The manager recorded the following Plan v2 verdicts on 18 November 2026.

| Reviewer | Verdict | What the reviewer confirmed |
|---|---|---|
| `architecture-reviewer` (`/root/log_consult`) | Pass | All three blockers cleared. The five affected fields keep lossless count decoding and raw-JSON persistence controls. Both partial-write paths have null-safe guards, revalidation, concurrency coverage and post-commit scored calibration. Actual restore counts reach the result panel and toast through the existing response shape. |
| `product-risk-reviewer` (`/root/firefox_consult`) | Pass | Restore counts precede name deduplication and reach both visible result channels. Browser and JSON inputs retain exact values, and `badInput` stays distinct from an intentional clear. Plan v2 records the inherited analytical overflow at extreme counts. |
| `test-strategist` (`/root/summary_consult`) | Pass | All three blockers cleared. Coverage includes repeated missing names, panel and toast counts, replacements for the six clamp/truncation assertions, and the numeric and state witnesses. The gate list includes independent architecture review and manual backup and restore. No new findings. |

## Gate 1 owner approval and scope reductions

Direct owner approval on 18 November 2026 (verbatim):

> I approve Gate 1 for #596 Plan v2 with two scope reductions: drop the exact JSON number-token decoding (use normal decoding, accept whole numbers only, and reject values too large to store exactly), and drop the guarded-update retry and its concurrency tests (keep the atomic two-field write). These are reductions, so no council re-review is needed.

The following directions govern implementation. The Plan v2 review and response matrix above remain the record of what the council rereviewed.

| Reviewed requirement | Owner-approved implementation |
|---|---|
| Exact number-token overlay at five fields in Plan v2 artifact table and sequence step 2 | Use normal Flask JSON decoding on all three write routes. Apply whole-number, finite-value, minimum and exact SQLite storage checks to the decoded count values. Parse integer strings without a lossy float conversion. JSON decimal literals follow the ordinary decoder’s representation and precision. Keep the browser’s count text lossless through submission and preserve unaffected numeric parsing. |
| Exact-token-specific raw JSON and SQL witnesses in Plan v2 sequence step 2 and the gate list | Cover normal decoding with ordinary fractional and nonfinite rejection, regular integral values, exact large integer literals and numeric strings within the signed SQLite range, out-of-storage values, `typeof()` and failed-write state. The reviewed raw fractional and integral-decimal lexeme witnesses `9007199254740992.5` and `9223372036854775807.0` are removed as acceptance requirements. The signed integer edge `9223372036854775807`, as a JSON integer or numeric string, remains a persistence witness. |
| Guarded update, lost-race revalidation and deterministic races in Plan v2 sequence step 3 and test gates | When one rep field is supplied, compare it with a usable persisted sibling and allow repair when the sibling is already unusable. When both are supplied, validate both and write them by one ordinary atomic `UPDATE` through `DatabaseHandler`. Preserve whole-request rejection, each route’s existing missing-row behavior and calibration after a successful scored commit. Remove the extra guard, retry, revalidation and concurrent-edit tests. |

The reviewed restore work still counts each skipped row before deduplicating missing exercise names and reports the total and reasons in the HTTP result, Backup Center panel and toast. The rest of Plan v2 applies, including zero versus clear behavior, legacy repair, whole-plan import rejection, migration notes, regression coverage and the required quality gates. The owner’s quoted approval resolves the two reductions without another council review.

## Implementation record

Implemented on 18 November 2026 on `fix/596-sets-reps-bounds` from the handed-over candidate, under the Gate 1 reductions above: normal JSON decoding, exact SQLite integer storage and an ordinary atomic two-field update. The compatibility wrappers (`restore_backup`, the default `restoreBackup` result shape) are preserved.

The owner approved six follow-ups to the candidate on 18 November 2026:

| Follow-up | Implementation |
|---|---|
| Regenerate the test inventory | `docs/test_inventory/` regenerated; the pinned Vitest totals in `tests/test_vitest_inventory_contracts.py` move from 270 to 271 for the one added case. |
| Restore stores parsed whole numbers | `_restore_value()` in `utils/program_backup.py` binds the integer that validation parsed for sets and both rep bounds. |
| All-skipped restore says what happened | When rows were skipped and none restored, the message ends with "Your current plan and workout log were cleared." The skipped-row total and the counts by reason are unchanged, and repeated missing exercises count as separate rows. |
| Show the stored number after a save | `storedCountText()` in `static/js/modules/workout-plan-helpers.js`, used for inline plan counts and scored reps. A decimal or exponent draft beyond the safe-integer range shows as typed until reload. |
| Blank inline plan count edit | Reverts to the saved value without sending a write. Malformed input is still rejected, and clearing a scored rep still sends `null`. |
| Restore explanatory comments | The FINDING-1 rationale in `utils/program_backup.py`, the clamp rationale in `workout-plan-add-exercise.js` and the multiple-inputs comment in `workout-plan-table.js`. |

Code, architecture, product-risk and unslop reviewers read the candidate and then the follow-up delta. None raised a blocking finding. Verification results are in the pull request.

## Sign-off

- [x] Gate 0 complete.
- [x] Every Plan v1 finding has a proposed disposition in the response matrix.
- [x] Agent provenance complete for Plan v1, its reviewers, the response matrix and Plan v2.
- [x] Blocking reviewers have rereviewed Plan v2 and cleared the blockers.
- [x] Owner approved Plan v2 with the recorded reductions (Gate 1).
- [x] Ready to implement within the owner-approved scope.
