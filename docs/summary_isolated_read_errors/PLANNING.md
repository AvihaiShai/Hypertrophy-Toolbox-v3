# Plan Review — Summary isolated-muscle read errors (#631)

## Section 0 — Requirements Brief

**Raw request (verbatim excerpt)**

> handle those item where we left off using multiple agents to close those issues\items until it get done end to end.
>
> in case  you are waiting for decisions - span the ai consulting team for each item that pending for decision.

**Problem**

When the isolated-muscle statistics read fails, both summaries report a
successful empty result and the full Excel export omits the sheet. A user
cannot distinguish an unavailable result from a successful query that found
no mappings. The failure was reproduced on a scratch database at `ad6f739b`.
[Issue #631 reproduction](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/631#issuecomment-6963296519)

**Acceptance criteria**

1. Given a failed isolated-muscle statistics read, a normal `GET /weekly_summary`
   or `GET /session_summary` renders its existing error page with HTTP 500.
   The same failure returns HTTP 500 with the existing `INTERNAL_ERROR` JSON
   envelope for JSON or XHR callers. Responses omit SQL and traceback details.
2. Given the same read failure, `GET /export_to_excel` returns HTTP 500 with the
   existing `EXPORT_FAILED` JSON envelope and sends no workbook or attachment.
3. Given a successful read with no mapped exercises, the two summaries still
   return HTTP 200, JSON still reports an empty isolated-muscle array, the HTML
   panel remains hidden, and a valid full Excel workbook may omit that sheet.
   Other available data remains present.
4. Given a successful read with mapped exercises, existing JSON keys, HTML
   panels, workbook sheets and statistics continue to match their contracts.
   Weekly and session calculations, modes, and thresholds keep their current
   behavior.

**Calculation surface**

- `none`. The failure path changes. The isolated-muscle SQL, rollups, and
  interpretation remain the same. Include migration notes for the corrected
  failure responses and regression coverage in the implementation PR.

**In scope**

- AUD-1088, limited to the isolated-muscle read shared by both summaries and the
  full Excel export.
- Regression coverage, product flow documentation, and a recorded disposition
  for each entry in #631 before closure.

**Out of scope / non-goals**

- The other roadmap entries remain deferred, including attendance, parser and
  response alias cleanup, default-factor indicators, isolated-muscle mode parity,
  highlighting, movement patterns, subtitles, and session thresholds.
- Schema and stored data changes, export UI wiring, and adding isolated-muscle
  worksheets to either `POST /export_summary` or `POST /export_large_dataset`.

**Assumptions made**

- None. The successful empty behavior and in-scope export are observable in the
  current callers.

**Open questions for the user**

- None at Gate 0.

### Section 0 sign-off — GATE 0

- [x] Owner approved the requirements and scope in the 2026-11-18 conversation with “Approve all below.”
- [x] No assumptions require separate approval.
- [x] No blocking questions remain at this gate.

---

## Plan v1

**Goal**

Make a failed isolated-muscle read visible in both summary views and the full
Excel export while preserving their healthy results.

**Scope**

- **In** — Propagate failures from the shared statistics helper to existing
  error handlers, cover the three route consumers, and update the corresponding
  product flow documentation.
- **Out** — Calculation logic and successful response shapes, the fatigue badge's
  independent fallback, other export endpoints, summary-page export button
  wiring, and the deferred audit entries.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/weekly_summary.py` | Modify | Return the query's rows directly and allow the original exception to propagate. Keep SQL and the database context manager. |
| `tests/test_weekly_summary_routes.py`, `tests/test_session_summary_routes.py` | Modify | Cover the HTML and JSON/XHR response to a real isolated-muscle table failure. Use existing tests for healthy behavior where they establish the contract. |
| `tests/test_exports.py` | Modify | Cover full Excel export failure before workbook generation, plus healthy omission and inclusion of the isolated-muscle sheet where existing coverage needs it. |
| `docs/product/APP_FLOW.md` | Modify | Document both summary failure outcomes and the full Excel export's failure response. |
| `docs/test_inventory/TEST_INVENTORY.md`, `docs/test_inventory/TEST_INVENTORY.json` | Regenerate | Update the inventory after any test-node changes and verify it with the producer's `--check`. |
| `docs/summary_isolated_read_errors/PLANNING.md` | Complete | Record council findings, approvals, and verification evidence. |

**Effort** — L, due to the cross-cutting HTTP contract. **Owner** — manager for
#631, with delegated test and code owners. **Depends on** — council review,
direct owner Gate 1 approval, and a coordinated editing and testing slot.

**Sequence**

1. Confirm the three consumers of `calculate_isolated_muscles_stats()`.
   The Weekly and Session handlers already log and return the existing safe
   HTML or JSON 500. `GET /export_to_excel` reads all sheet data before creating
   a workbook and already handles failures with `EXPORT_FAILED`. Its callers
   can choose simple or advanced formatting. `POST /export_summary` builds
   Weekly Summary and Categories only. `POST /export_large_dataset` does not
   query the isolated-muscle table. Their current workbook contracts are outside
   this repair.
2. Cover the fault through Flask clients using function-scoped scratch SQLite
   fixtures. Remove the mapping table only in each disposable database after
   seeding otherwise valid plan and session inputs. Confirm other summary reads
   still work so a failure in an earlier dependency cannot satisfy the test.
   Include a normal navigation and JSON/XHR requests for both pages. Assert the
   existing error code and safe copy, absence of the normal summary content on
   HTML errors, and absence of workbook content and attachment headers for the
   full export in both view modes. Exercise a healthy database with working
   mapping schema and zero matches as a separate control and retain populated
   controls for the panels, array, and workbook sheet.
3. Remove the catch that converts errors to `[]` in the helper. Keep the
   original SQLite exception type so the current route handlers can suppress
   secondary rep-range diagnostics on database failures. Existing handlers log
   the error. The healthy empty result still comes directly from the query.
4. Verify that the existing browser summary refresh path handles a JSON error
   with its inline failure feedback. Keep this a verification step unless
   council review finds an in-scope blocker. Update the product flow, regenerate
   inventory if test nodes change, and describe the HTTP/XLSX behavior change
   in the PR migration notes.
5. Follow the implementation review and owner approval gates. Record AUD-1088's
   disposition and note the maintained destinations for all deferred entries
   before closing #631. The summary UX and calculation proposals are recorded in
   [UI Scenarios Gap Analysis](../UI_SCENARIOS_GAP_ANALYSIS.md). The movement
   pattern fork is in the [Duplication Registry](../DUPLICATION_REGISTRY.md).
   Retain AUD-1086 with the issue's historic source citation and the current
   compatibility wrappers and aliases.

**Expected gates (proposed for test-strategist review)**

- pytest includes `tests/test_weekly_summary.py`, `tests/test_weekly_summary_golden.py`,
  `tests/test_weekly_summary_routes.py`, `tests/test_session_summary_routes.py`,
  `tests/test_exports.py`, and `tests/test_app_factory.py`. Check additional
  callers found by targeted search.
- Chromium includes `summary-pages`, `empty-states`, `error-handling`, and
  `api-integration` for the affected outcomes. Verify the browser refresh
  failure through controlled response interception or the supported isolated
  fault harness. The Flask regressions exercise the real SQLite fault.
- Check test inventory and pyright baseline drift. Apply diff-time `code-reviewer`,
  `unslop-reviewer`, and `product-risk-reviewer` requirements. Use the applicable
  owner and named-PR approval gates.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `/root/summary_consult` | Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `/root/summary_consult` | The manager resumed the Plan v1 author. |
| `architecture-reviewer` | `/root/bounds_consult` | Sound. |
| `test-strategist` | `/root/firefox_consult` | Targeted verification sufficient with clarifications. |
| `product-risk-reviewer` | `/root/log_consult` | Preserves product invariants. |

**Same product-manager resumed for the matrix + Plan v2?** Yes.

**Evidence gap** — none.

## Reviewer findings

### architecture-reviewer (`/root/bounds_consult`)

> point any refresh check at the live `static/js/modules/weekly-summary.js:264–269` and `session-summary.js:149–154` handlers, not the legacy `summary.js` fetch stubs. Each existing handler presents `Failed to load data.` in the primary table and leaves already-rendered category/isolated content alone. Pin the explicit failed-refresh signal and retain existing secondary content behavior; no JS change required by approved server-side scope.

### test-strategist (`/root/firefox_consult`)

> (1) name `tests/test_error_page_contract.py` (already validates both shared route error views) and `tests/test_rep_range_integrity.py` (full export/summary diagnostic controls) in the union alongside the listed weekly/golden/weekly+session route/export/app-factory modules; (2) make the healthy real-DB zero-mapping and populated controls explicit in all three test modules. Existing export assertions `tests/test_exports.py:59,66` validate a plan-column header, not the separate `Isolated Muscles` sheet. Assert openpyxl sheet omission/inclusion plus a seeded row value and verify both refresh paths in `summary-pages` or manual/browser interception with only the known seeded HTTP-500 console pattern allowed. Add an HTML-500 browser entry check on both routes if using the fault harness; refresh alone checks different client path.

### product-risk-reviewer (`/root/log_consult`)

> In Plan v2, explicitly verify the failed summary refresh shows failure rather than the healthy no-data text and that the Workout Plan Excel action produces its failure toast and no download. Treat these as verification of existing presentation; the standalone endpoints and existing out-of-scope export wiring stay separate.

## Response matrix

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| Verify the live refresh handlers and preserve existing secondary content. | architecture-reviewer | Accept | Check the Weekly and Session modules' current inline failure row and retain the categories and isolated-muscle panels already rendered. |
| Include the shared error-page and rep-range diagnostic suites. | test-strategist | Accept | Name both suites in the targeted pytest union. |
| Use real healthy controls, check the isolated worksheet, and distinguish refresh from navigation. | test-strategist | Accept | Test healthy populated and zero-mapping cases in both route test files and the export test file. Exercise both browser refreshes and both initial HTML 500 pages when the fault harness is used. |
| Verify the failed refresh and the live Workout Plan download action. | product-risk-reviewer | Accept | Assert the primary table's failure signal, absence of healthy no-data text, the existing export failure toast, and absence of a download. |

## Plan v2

**Goal**

Report an unavailable isolated-muscle read through the two summaries and full
Excel export while retaining healthy results.

**Scope**

- **In** — The shared statistics read, current HTTP error handlers, the existing
  browser error paths used by each summary and the Workout Plan download, and
  documentation of the corrected outcomes.
- **Out** — SQL, calculation rules, successful response shapes and workbook
  structure, independent fatigue fallback, summary-page export wiring, other
  endpoints, and the deferred roadmap entries.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/weekly_summary.py` | Modify | Keep the query and `DatabaseHandler` context manager. Return its rows directly and let the original exception reach the existing handlers. |
| `tests/test_weekly_summary_routes.py`, `tests/test_session_summary_routes.py` | Modify | Exercise the real SQLite fault, healthy empty mappings, and healthy populated mappings through both summary routes. |
| `tests/test_exports.py` | Modify | Check the full export's 500 response and use openpyxl to verify healthy omission, presence, and seeded content of the isolated worksheet. |
| `e2e/summary-pages.spec.ts`, `e2e/error-handling.spec.ts` | Extend if using automated browser coverage | Use existing browser interception or record equivalent manual checks. |
| `docs/product/APP_FLOW.md` | Modify | Describe both summaries and the full Excel export failure outcomes. |
| `docs/test_inventory/TEST_INVENTORY.md`, `docs/test_inventory/TEST_INVENTORY.json` | Regenerate if test nodes change | Use the producer and confirm `--check` passes. |
| `docs/summary_isolated_read_errors/PLANNING.md` | Complete | Record Gate 1 and verification evidence. |

**Sequence**

1. Confirm `GET /weekly_summary`, `GET /session_summary`, and `GET /export_to_excel`
   are the three consumers. Both summaries already log and return safe HTML or
   JSON 500 responses. The full export collects all sheets before producing an
   attachment and already catches failures. `POST /export_summary` builds Weekly
   Summary and Categories. `POST /export_large_dataset` uses its separate sheet
   set. Neither POST reads the isolated-muscle statistics.
2. In function-scoped scratch SQLite fixtures, seed otherwise-valid plan and
   session input and remove only the isolated-muscle mapping table. Confirm the
   other reads remain healthy. In both summary route modules, assert normal HTML
   navigation returns the existing 500 error page and JSON/XHR gets the standard
   `INTERNAL_ERROR` envelope and safe copy. In the export module, assert simple
   and advanced full exports return `EXPORT_FAILED` with HTTP 500, JSON content,
   and no attachment. The regressions must fail against a return-`[]` fallback.
3. In all three test modules, use real healthy databases with the mapping table
   intact. Cover zero matching mappings with other data available, then seed an
   actual mapping. Both summary routes must distinguish the empty array and
   hidden panel from populated JSON and HTML. Open both healthy workbooks with
   openpyxl. Assert the `Isolated Muscles` sheet is omitted in the zero-match
   case, present in the populated case, and contains the seeded muscle and a
   known statistic such as its set count. Check that other workbook data remains
   available.
4. Remove the helper's empty-list fallback and preserve the original SQLite
   exception type. The summary and export handlers already log that failure,
   and their existing check for database errors prevents the secondary
   rep-range diagnostic from opening another connection.
5. Verify both live refresh paths in `weekly-summary.js` and `session-summary.js`.
   Each failed request shows `Failed to load data.` in its primary table, omits
   the healthy no-data message, and leaves already-rendered category and
   isolated-muscle content in place. Use `summary-pages` with intercepted
   requests or perform equivalent manual verification. If the browser fault
   harness is used, also open both summary URLs directly and assert their HTML
   500 error view.
   Verify that the Workout Plan Excel action shows its existing failure toast
   and triggers no download on an export 500. For intercepted automated tests,
   allow only the exact expected console patterns from each seeded failure and
   check for unexpected browser errors. This step verifies existing JavaScript
   behavior.
6. Update product flow and inventory where applicable. Add the failure-response
   change and coverage to the implementation PR migration notes. After an
   authorized merge, record the AUD-1088 result and maintain the other eight
   dispositions before closing #631. Keep the UX and calculation proposals in
   [UI Scenarios Gap Analysis](../UI_SCENARIOS_GAP_ANALYSIS.md), the movement
   pattern fork in the [Duplication Registry](../DUPLICATION_REGISTRY.md), and
   AUD-1086 with the issue's historic citation and current compatibility shims.

**Expected gates**

- Targeted pytest union includes `tests/test_weekly_summary.py`,
  `tests/test_weekly_summary_golden.py`, `tests/test_weekly_summary_routes.py`,
  `tests/test_session_summary_routes.py`, `tests/test_exports.py`,
  `tests/test_app_factory.py`, `tests/test_error_page_contract.py`, and
  `tests/test_rep_range_integrity.py`. Apply the changed-path routing to any
  additions to the final diff.
- Chromium `summary-pages`, `empty-states`, `error-handling`, and
  `api-integration`, plus the browser checks in step 5. The Flask regressions
  provide real SQLite failure evidence.
- Verify inventory and pyright baseline drift and complete `code-reviewer`,
  `unslop-reviewer`, and `product-risk-reviewer` review. Record owner approvals
  independently of reviewer verdicts.

## Verification evidence

- The eight new read-failure cases reproduced HTTP 200 before the helper fix.
  The targeted pytest union passed after the fix, with 255 tests passing on
  18 November 2026. The healthy controls cover both summary responses and the
  exported workbook with zero or populated isolated-muscle mappings.
- The four targeted Chromium specs passed all 107 cases. In a separate isolated
  Chromium 149.0.7827.55 smoke, both summary pages loaded with mapped data. After
  removing the mapping table from the scratch database, both contribution-mode
  requests returned HTTP 500 and showed “Failed to load data.” while keeping
  the existing secondary content visible. Fresh navigation to either summary
  returned its HTML 500 view. The populated Workout Plan's Excel button showed
  its failure toast and generated no attachment or download. The smoke found
  no unexpected console or page errors.
- Test inventory regeneration and `--check` passed. Pyright reported zero
  diagnostics and its baseline comparison passed. `tsc --noEmit` passed.

## Sign-off

- [x] Gate 0 complete.
- [x] Every finding has a disposition.
- [x] Agent provenance complete.
- [x] Direct owner approval of Plan v2 (Gate 1) on 2026-11-18.
- [x] Ready to implement.

> I approve Gate 1 for Plan v2 of #637 (docs/workout_log_read_errors/PLANNING.md) and Plan v2 of #631 (docs/summary_isolated_read_errors/PLANNING.md).

## See also

- [Issue #631](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/631)
- [Council plan command](../../.claude/commands/council-plan.md)
- [Quality Gate](../ai_workflow/QUALITY_GATE.md)
- [Route conventions](../../.claude/rules/routes.md)

Docs retention at closeout: keep active — `docs/summary_isolated_read_errors/PLANNING.md`; [PR #727](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/727) records the shipped behavior and verification; retain the approved page and export failure contract and the deferred roadmap items.
