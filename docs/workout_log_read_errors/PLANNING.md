# Plan Review — Workout Log read errors (#637)

## Section 0 — Requirements Brief

**Raw request (verbatim excerpt)**

> handle those item where we left off using multiple agents to close those issues\items until it get done end to end.
>
> in case  you are waiting for decisions - span the ai consulting team for each item that pending for decision.

**Problem**

A failed Workout Log read looks like a healthy empty log on the page and like a
404 no-data outcome on the standalone export. The failure was reproduced with
scratch-database faults at `ad6f739b`. The independent log-list endpoint already
reports its own read failures as HTTP 500. [Issue #637 and reproduction](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/637#issuecomment-6963295848)

**Acceptance criteria**

1. Given a Workout Log read fails, a normal browser request to `GET /workout_log`
   receives a safe, specific HTML error page with HTTP 500. A JSON or XHR request
   receives HTTP 500 with the standard `INTERNAL_ERROR` envelope. The response
   omits database details and traceback text.
2. Given a Workout Log read fails, `GET /export_workout_log` returns HTTP 500 and
   the standard `INTERNAL_ERROR` JSON envelope without an XLSX or attachment.
3. Given a healthy database with no log rows, `GET /workout_log` still renders
   the normal page with zero rows and HTTP 200, and `GET /export_workout_log`
   still returns its JSON `NOT_FOUND` with HTTP 404.
4. Given a healthy populated log, the rendered rows and XLSX retain their
   existing data, order, and format. The independent `GET /get_workout_logs`
   keeps its success payload and existing HTTP 500 JSON failure behavior.

**Calculation surface**

- `none`. Include migration notes describing the failure-response change and
  regression coverage in the PR, as required for core Log behavior.

**In scope**

- AUD-0925, the Workout Log page and standalone export failure distinction.
- Regression coverage and documentation of the shipped outcomes.

**Out of scope / non-goals**

- AUD-0740 assistance mapping changes. Retain the manual-sync risk as a tracked
  disposition. Revalidation established no assistance-direction defect.
- AUD-1232 optional helper characterization, deferred.
- Import, score, edit, clear, or progression behavior changes, schema or user
  data migration, new export UI, and unrelated endpoints.

**Assumptions made**

- None. Healthy behavior above describes the current routes and template.

**Open questions for the user**

- None at Gate 0.

### Section 0 sign-off — GATE 0

- [x] Owner approved the requirements and scope in the 2026-11-18 conversation with “Approve all below.”
- [x] No assumptions require separate approval.
- [x] No blocking questions remain at this gate.

---

## Plan v1

**Goal**: Make a failed Workout Log or standalone export read visible while
preserving healthy page, workbook, and standalone log-list behavior.

**Scope**

- **In** — Propagate failed reads through the shared page/export helper. Report
  them with the existing route-level logging, error page, and JSON envelope.
  Add regression coverage for failed reads and corroborate healthy contracts.
- **Out** — The helper query, successful row fields and ordering, the
  independent log-list implementation, exports other than the standalone log
  export, and the deferred audit leads.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/workout_log.py` | Modify | Let `DatabaseHandler.fetch_all()` return real rows or raise. Update the helper docstring and remove its redundant exception logging if unused. |
| `routes/workout_log.py` | Modify | Let page and export handlers receive the failure and log it with traceback. For the page, use `is_xhr_request()` and the existing `error.html` per the summary-route pattern. The standalone export keeps its existing JSON 500 handler. |
| `tests/test_workout_log_routes.py` | Modify | Exercise real query failure on a disposable pytest SQLite fixture and lock the page, export, and independent-list contracts. Check healthy routes against existing fixtures. |
| `docs/product/APP_FLOW.md` | Modify | Record the normal and failure outcomes for the page, standalone export, and log-list API without implying that the standalone endpoints are UI-bound. |
| `docs/test_inventory/TEST_INVENTORY.md`, `docs/test_inventory/TEST_INVENTORY.json` | Regenerate | Run the producer for changed test nodes and verify with `--check`. |
| `docs/workout_log_read_errors/PLANNING.md` | Complete | Record council review, approvals, and evidence. |

**Effort**: L (route contracts and two different read consumers) · **Owner**:
manager for #637, with delegated test and code owners · **Depends on**: council
review, direct owner Gate 1, and a coordinated single editing/testing slot.

**Sequence**

1. Confirm callers. `GET /workout_log` and `GET /export_workout_log` both call
   `utils.workout_log.get_workout_logs()`, which sorts by routine and exercise.
   The separate `GET /get_workout_logs` query has extra plan fields and sorts
   newest first. Preserve both query contracts and leave the list handler alone.
2. Have automation QA cover actual SQLite failure on an isolated, function-scoped
   fixture, for example after removing `workout_log` from that test database.
   Check HTML 500 and the absent normal table, JSON 500 for `Accept:
   application/json` and `X-Requested-With: XMLHttpRequest`, JSON 500 without an
   attachment for export, and unchanged JSON 500 for the independent list. Keep
   the normal empty page, export 404, populated page and valid workbook tests.
   Add assertions to existing healthy cases where needed instead of duplicating
   them. Keep fault setup local to tests and leave the development and user DBs
   untouched.
3. Have the developer remove the helper's conversion of errors to `[]`. At the
   page boundary, reuse `is_xhr_request()` and `error.html` to send a safe message
   such as “Unable to load workout log.” Leave success rendering alone. The
   export route already logs exceptions and returns a safe JSON 500, so the
   propagated read failure should use that path before a workbook is created.
4. Update the Log flow documentation and regenerate inventory. Check the shared
   error template on the log URL because the front-end initializer dispatches by
   pathname. Its DOM lookups are guarded, so the current plan needs no JavaScript
   edit. Add the migration note describing the two corrected failure outcomes
   to the implementation PR.
5. Run the applicable test and review gates. After an approved merge, record all
   three audit dispositions in #637, including the retained sync risk and the
   deferred optional coverage, before closing it.

**Expected gates**

- Proposed pytest targets for test-strategist confirmation: `tests/test_workout_log_routes.py`,
  `tests/test_workout_log_utils.py`, `tests/test_app_factory.py`, and the current
  additional caller/payload tests identified by targeted search.
- Proposed Chromium specs for test-strategist confirmation: `workout-log`,
  `empty-states`, `error-handling`, `accessibility`, and `api-integration`.
  The server-side regression uses an actual SQLite failure. Supplement with a
  browser smoke on an isolated fault fixture if the supported harness permits.
- Inventory regeneration and check, pyright baseline diff, and applicable
  diff-time code, unslop, and product-risk review. Record evidence and observe
  the applicable owner and named-PR approval gates.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `/root/log_consult` | Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `/root/log_consult` | Same product manager resumed. |
| `architecture-reviewer` | `/root/firefox_consult` | Plan is sound. |
| `test-strategist` | `/root/summary_consult` | Plan is sound with nonblocking verification refinements. |
| `product-risk-reviewer` | `/root/bounds_consult` | Plan respects product invariants. |

**Same product-manager resumed for the matrix + Plan v2?** Yes.

**Evidence gap** — none.

## Reviewer findings

### architecture-reviewer (agent `/root/firefox_consult`)

> #637 architecture — Plan is sound. `utils.workout_log.get_workout_logs` has two production callers and keeps DatabaseHandler; page can reuse `is_xhr_request`, `error.html`, and `error_response`, while independent list and export envelopes remain. Confirm actual error template context (`error_title`, `error_code`, `error_message`) and no page errors with `initializeWorkoutLog` still dispatched by pathname.

### test-strategist (agent `/root/summary_consult`)

> #637 test-strategist verdict: SOUND; targeted gate sufficient. Nonblocking T637-1 (explicit controls): extend `tests/test_workout_log_routes.py:20` healthy-empty assertion with normal `.workout-log-table`/empty marker and no error-page content, strengthen its existing 404 at :470 to `NOT_FOUND`, and use the real scratch missing-table response to assert `<title>Server Error - Hypertrophy Toolbox</title>`, `500`/safe message and no normal table for HTML. For each Accept/XHR spelling and standalone export, assert envelope/code and no SQL/traceback; for export also content type, absent attachment and no ZIP signature. Existing populated :25 and workbook :475–505 are suitable format controls; existing `tests/test_workout_log_utils.py:36` protects sort, and a two-row workbook body assertion can directly protect order. Include targeted pytest `tests/test_workout_log_routes.py`, `tests/test_workout_log_utils.py`, `tests/test_app_factory.py`, `tests/test_error_page_contract.py`, `tests/test_youtube_video_id.py`, `tests/test_free_exercise_db_mapping.py`, `tests/test_ui_flows.py` and `tests/test_priority7_error_handling.py` (all live path/payload coverage). Chromium union `workout-log`, `validation-boundary` (mapped error routing), `empty-states`, `error-handling`, `accessibility`, `api-integration`. Because pathname dispatch still invokes Log JS on HTML 500, include a Chromium smoke of that normal navigation with strict console checks, real scratch HTTP fault or served exact 500 page; avoid relying on the existing healthy browser specs for this. No conftest/schema edit, baseline work, or application JS work expected. Inventory + pyright and diff-time reviewer gates stand.

### product-risk-reviewer (agent `/root/bounds_consult`)

> #637 · product-risk-reviewer — **Plan respects product invariants.** No blocking or important findings. The chosen copy “Unable to load workout log.” accurately describes a read failure without implying an empty log, a failed prior import, or data loss. Keep that distinction in Plan v2 and APP_FLOW, including navigation to `/workout_log` after a successful Plan→Log action (`docs/product/APP_FLOW.md:328`) and the standalone export’s unchanged 404 for a genuinely empty log (`routes/workout_log.py:158–166`). The export remains API-only, and assistance mapping, progression, data, and worksheet semantics remain out of scope. Plan v1 already requires migration notes and regression evidence. No further product changes.

## Response matrix

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| Pin shared template context and verify pathname dispatch on the error document. | architecture-reviewer | Accept | Set the three existing template fields in the route and verify a strict Chromium navigation on the failed URL. |
| T637-1. Add healthy controls, validate the exact fault shape and workbook order, and specify gate coverage. | test-strategist | Accept | Assert the HTML and JSON branches, safe content, no workbook on failure, normal empty table, and healthy exports. Run the eight pytest modules, six Chromium specs, and the separate failure navigation smoke. |
| Describe a loading failure and preserve the existing import and empty-export behavior. | product-risk-reviewer | Accept | Use the loading-specific copy and document the post-import navigation and the export's two outcomes in APP_FLOW and PR migration notes. |

## Plan v2

**Goal**

Report a failed Workout Log read explicitly on the page and in the standalone
export while preserving successful behavior.

**Scope**

- **In** — AUD-0925 failure propagation, HTTP and browser regression evidence,
  and documentation of the changed outcomes.
- **Out** — The existing SELECT, order and successful payloads, the independent
  log-list implementation, import and mutation behavior, changes to assistance
  or progression, user data and schema changes, new export UI, and deferred
  AUD-0740 and AUD-1232 work.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/workout_log.py` | Modify | Preserve the current query and `DatabaseHandler` context. Return fetched rows or allow the underlying exception to reach the route. |
| `routes/workout_log.py` | Modify | Negotiate the page's error response. Keep the existing standalone export and log-list handlers. |
| `tests/test_workout_log_routes.py` | Modify | Cover real isolated SQLite failure and strengthen healthy route and workbook controls. |
| `docs/product/APP_FLOW.md` | Modify | Describe the Log load and direct endpoint outcomes, including the existing navigation after successful Plan→Log import. |
| `docs/test_inventory/TEST_INVENTORY.md`, `docs/test_inventory/TEST_INVENTORY.json` | Regenerate | Use the inventory producer for new test nodes and verify its `--check`. |
| `docs/workout_log_read_errors/PLANNING.md` and implementation PR description | Complete | Record evidence and migration notes for the corrected failure outcomes. |

**Effort** — L because the change affects multiple HTTP contracts. **Owner** —
manager for #637 with delegated QA and development. **Dependencies** — direct
owner Gate 1 approval and a coordinated editing/testing slot.

**Sequence**

1. Use the function-scoped pytest database to force an actual read failure,
   such as by dropping `workout_log` on that disposable fixture. Assert that
   normal navigation returns HTML 500 with `<title>Server Error - Hypertrophy Toolbox</title>`,
   status code in the shared error content, and “Unable to load workout log.”
   The normal `.workout-log-table` must be absent. Assert HTTP 500 and
   `INTERNAL_ERROR` for both the `Accept: application/json` and
   `X-Requested-With: XMLHttpRequest` paths, and confirm that the exposed
   response bodies contain neither SQL details nor a traceback. Assert that
   the standalone export returns JSON 500 with the same error code, no
   `Content-Disposition` attachment and no XLSX ZIP signature. Assert the
   independent list route still returns its existing JSON 500.
2. Strengthen healthy controls. The empty page returns HTTP 200 with the usual
   table, zero rows and no error page. The empty export returns its JSON 404
   `NOT_FOUND`. Keep the existing populated page, JSON list and workbook shape
   checks. Protect routine/exercise sort with the utility test and confirm two
   distinct rows are exported in that order. The independent list keeps its
   existing fields and newest-first order.
3. Remove the helper's conversion of an exception to `[]`, and remove its
   redundant exception log if unused. The page route logs the failed read and
   uses `is_xhr_request()` to choose the existing `error_response()` envelope
   or `error.html` with `error_title="Server Error"`, `error_code=500`, and
   `error_message="Unable to load workout log."`. Keep the existing export
   handler so the exception reaches its JSON 500 before filename or workbook
   work. Keep all existing successful rendering and attached workbook behavior.
4. Exercise browser navigation to `/workout_log` with a real fault in an
   isolated runtime or by serving the exact HTTP 500 document captured from the
   Flask fault. Confirm its status and loading-specific message, with strict
   page and console error checks apart from the expected HTTP 500 itself.
   `initializeWorkoutLog` still dispatches by pathname, so the actual failure
   document must remain usable with its guarded DOM lookups. The plan keeps
   application JS, shared templates and visual baselines outside the edit scope.
5. Document the load failure without implying an empty Log, a failed prior
   import or data loss. Keep the existing post-import navigation and document
   the direct export's healthy-empty 404 separately from read-failure 500.
   Run the gates and record the user-visible change and regression coverage in
   the PR migration notes. After approved merge, record AUD-0925's fix,
   AUD-0740's retained manual-sync risk and AUD-1232's deferred disposition in
   #637 before closure.

**Expected gates**

- Pytest — `tests/test_workout_log_routes.py`, `tests/test_workout_log_utils.py`,
  `tests/test_app_factory.py`, `tests/test_error_page_contract.py`,
  `tests/test_youtube_video_id.py`, `tests/test_free_exercise_db_mapping.py`,
  `tests/test_ui_flows.py`, and `tests/test_priority7_error_handling.py`.
- Chromium — `workout-log`, `validation-boundary`, `empty-states`,
  `error-handling`, `accessibility`, and `api-integration`, plus the strict
  failure-navigation smoke described above. Keep all fault setup away from the
  user database.
- Regenerate and check inventory, verify the pyright baseline, and obtain the
  diff-time code, unslop and product-risk reviews. Record evidence and observe
  the applicable owner and named-PR approval gates.

## Sign-off

- [x] Gate 0 complete.
- [x] Every finding has a disposition.
- [x] Agent provenance complete.
- [x] Direct owner approval of Plan v2 (Gate 1) on 2026-11-18.
- [x] Ready to implement.

> I approve Gate 1 for Plan v2 of #637 (docs/workout_log_read_errors/PLANNING.md) and Plan v2 of #631 (docs/summary_isolated_read_errors/PLANNING.md).

## Implementation evidence

Verification on 2026-11-18 used disposable SQLite fixtures and runtimes under
`artifacts/issue-637-verification/`. No user database was used.

- Before the fix, the missing-table regression returned HTTP 200 for the three
  page request variants and HTTP 404 for the standalone export. All four
  assertions failed as expected. The independent list and healthy controls
  passed.
- The eight targeted pytest modules passed with 320 passed and one existing
  skip. They cover the real SQLite failure, all three read consumers, healthy
  emptiness, and workbook shape and ordering.
- All 172 tests in the six targeted Chromium specs passed on the first run
  with retries disabled. Chromium 149.0.7827.55 also loaded the real Flask
  HTML 500 from the missing-table runtime. The path-based Workout Log
  initializer ran without an uncaught page error, a failed request, or an
  additional console error beyond the expected navigation HTTP 500.
- The regenerated inventory check passed. Pyright 1.1.410 reported zero
  diagnostics and the baseline gate passed.

## See also

- [Issue #637](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/637)
- [Council plan command](../../.claude/commands/council-plan.md)
- [Quality Gate](../ai_workflow/QUALITY_GATE.md)
- [Route conventions](../../.claude/rules/routes.md)
