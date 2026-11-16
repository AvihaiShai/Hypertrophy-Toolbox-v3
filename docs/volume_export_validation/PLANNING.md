# Plan Review — Volume export validation (#625)

**Status:** Gates 0 and 1 approved on 16 November 2026. The owner approved Plan v2,
confirmed the response-matrix dispositions and resolved Q1 by preserving current
parser behavior. Implementation is authorized; no merge authority is granted.

## Section 0 — Requirements Brief

**Raw owner reply, verbatim**

> Approve both proposed packets

The reply answered the question approving #607's native-zoom Gate 1 plan and
#625's malformed-export Gate 0 requirements in the local follow-through packet,
`artifacts/fable-follow-through-20261116/NEXT_CHANGES.md`. The question explicitly
said #625 would then proceed through its required plan review. This document
carries only that #625 scope; it does not approve implementation or a merge.

**Problem**

`POST /api/export_volume_excel` currently passes parsed input straight to the
workbook builder. Six malformed shapes reproduced as HTTP 500: string/null weekly
sets, list/null `volumes`, and a nonempty list/string root. Its browser caller
consumes every response as a blob, so an error document can be downloaded with
an `.xlsx` filename.

**Acceptance criteria**

1. Given a nonempty parsed root that is not a JSON object, exporting returns the
   standard HTTP 400 `VALIDATION_ERROR` envelope. Preserve the existing parsed
   falsy-root fallback and header-only exports for a missing/empty volumes map.
   Keep malformed-JSON and unsupported-content-type parser outcomes distinct;
   the empty-body wording is clarified for Gate 1 below.
2. Given a supplied `volumes`, it must be an object with finite JSON-number
   values, excluding booleans. Strings, nulls, arrays, nested objects, booleans
   and nonfinite values return the same safe 400 validation envelope. Introduce
   no muscle whitelist, positive-only rule or new numeric range.
3. Given finite numeric volumes, including fractions and negative values, retain
   their existing workbook behavior. Keep current training-day integer coercion,
   fallback to 3 and lower clamp to 1. Add no training-day upper bound or new
   sets/reps/RPE policy.
4. Successful exports retain the `Volume Plan` sheet, its three headers, row
   values, per-session calculation, column widths, filename pattern and XLSX MIME
   type. Missing volumes or an empty map produce a header-only workbook.
5. Invalid shape/type messages are useful and safe. Unexpected failures are
   logged and return a generic 500; internal exception text never reaches the UI.
   Malformed JSON retains a standard 400 envelope and unsupported content types
   retain their standard HTTP outcome.
6. Given a 4xx/5xx response, the browser shows one existing generic export-error
   toast and creates no blob URL, link or download. Successful binary downloads
   continue to work. Preserve meaningful error logging.
7. Route tests cover the valid/empty/malformed cases and training-day compatibility;
   browser tests cover a successful download and error-without-download. Update
   the Distribute export description, generated inventory and required type/test
   gates. The eventual PR carries migration notes for the changed HTTP outcomes.

**Calculation surface**

- No calculation function or schema changes. `build_volume_excel()` retains
  `round(weekly_sets / training_days, 1)` exactly.
- Example: `{"training_days": 3, "volumes": {"Chest": 12}}` exports 12 weekly
  sets and 4 per session before and after. `12.5 / 3` remains 4.2 per session.
- Malformed values change from a failed computation/500 to validation/400; they
  do not acquire a calculated substitute. The PR records that migration and its
  boundary tests.

**In scope**

- Route-boundary shape/type validation and safe exception handling.
- Status checking in the existing volume-export caller.
- Focused route/browser coverage, product-flow text and generated inventory.

**Out of scope**

- Plan-export console cleanup, Workbook #568 fidelity, streaming or filename work.
- A Workout Log export button, browser-support expansion, calculation redesign,
  muscle-taxonomy changes, database migration or persistence changes.
- Other entries in #625; this packet cannot close the mixed-scope issue by itself.

**Facts and assumptions**

- Source read against `main` at `9deb04c8`. The route currently uses
  `data = request.get_json() or {}` without local handling. The service catches
  only `TypeError` and `ValueError` around `int(training_days)`.
- The caller's `collectVolumes()` uses `parseInt(slider.value, 10) || 0`; the
  supported UI sends numbers. The server validation still protects direct callers.
- Global error handlers already provide safe 400, 415 and 500 API envelopes.
- The approved packet's “empty-body/null fallback” wording is broader than the
  source behavior: `get_json()` rejects an empty JSON body before `or {}` runs.
  Proposed interpretation for Gate 1: preserve parser outcomes and preserve the
  fallback only for successfully parsed falsy JSON values.

**Open question for Gate 1**

- **Q1 — empty HTTP body:** confirm the proposed interpretation above, preserving
  HTTP 400 for an empty `application/json` body and HTTP 415 for unsupported or
  missing JSON content type. Parsed JSON `null` still produces a header-only
  workbook. If “empty body” instead means a new successful HTTP outcome, revise
  the acceptance contract explicitly before implementation.

### Section 0 sign-off — GATE 0

- [x] Owner approved the proposed #625 requirements on 16 November 2026 through
  the direct reply quoted above.
- [x] The approved proposal's exclusions and compatibility requirements are retained.
- [x] Council-plan preparation may proceed; implementation waits for Gate 1.

Q1 records a source/wording discrepancy discovered during plan drafting; the
proposal below preserves current parser behavior and puts that interpretation to
the owner at Gate 1 rather than silently changing the HTTP contract.

## Plan v1

**Goal:** malformed volume exports produce safe client errors, and the browser
reports export failures without downloading an error document.

### Route behavior

In `routes/volume_splitter.py`, parse JSON before a narrow export exception
handler, preserving the registered HTTP exception handlers. Apply the existing
`or {}` normalization, then validate the normalized root and `volumes` before
calling `build_volume_excel()`.

| Input | Proposed outcome |
|---|---|
| Parsed `null`, `false`, `0`, `0.0`, `""`, `[]`, or `{}` | Existing fallback to `{}`; header-only XLSX |
| Nonempty list/string, `true`, or nonzero numeric root | 400 `VALIDATION_ERROR`: request data must be a JSON object |
| Object with omitted `volumes`, or `volumes: {}` | Header-only XLSX |
| Supplied null/list/string/number/boolean `volumes` | 400 `VALIDATION_ERROR`: volumes must be a JSON object |
| Each volume is a finite int/float, excluding bool | Pass through unchanged |
| A volume is null/string/list/object/bool or nonfinite | 400 `VALIDATION_ERROR`: volume values must be finite numbers |
| Malformed JSON or empty JSON body | Registered 400 `BAD_REQUEST` envelope, subject to Q1 |
| Unsupported/missing JSON content type | Registered 415 `UNSUPPORTED_MEDIA_TYPE` envelope, subject to Q1 |
| Unexpected builder or file-response failure | Log with the module logger; generic 500 export-error envelope |

Use `error_response()` for local failures and retain the module's `get_logger()`.
Keep input validation at the route boundary; no new single-caller validation
module is needed. Do not wrap HTTP parsing in an `except Exception` that turns
400/415 into 500.

For volume values, distinguish `bool` from `int`. Integers are finite without a
float conversion; call `math.isfinite()` only for floats. This avoids introducing
an accidental upper bound by converting a large Python integer to float merely
to validate it. Existing workbook representability or arithmetic failures remain
unexpected errors with a safe 500, rather than a new undocumented numeric cap.

### Training-day compatibility

Leave the service unchanged, including these cases:

| Stored/request value | Existing behavior retained |
|---|---|
| Missing, null or a value causing `TypeError`/`ValueError` during `int()` | Fallback to 3 |
| Zero, negative or `false` | Lower clamp to 1 |
| Positive integer, integer string or finite fractional number | Existing `int()` conversion, then clamp |
| `NaN` admitted by the JSON parser | `int()` raises `ValueError`; fallback to 3 |
| Positive/negative infinity admitted by the JSON parser | Existing `OverflowError`; logged generic 500 |

Nonfinite **volume values** are rejected by the new boundary. A broader rule for
nonfinite `training_days`, or changing its overflow case to fallback/400, is not
selected by the approved preservation requirement. Tests and migration notes make
this distinction visible; the council can flag it for an explicit owner decision.

### Browser behavior

In `static/js/modules/volume-splitter.js`, check `response.ok` before calling
`response.blob()`. On failure, throw an error into the existing catch so it logs
and shows the existing generic toast once. Do not parse or expose arbitrary server
error text. Keep successful object-URL creation, anchor download and cleanup as
they are. No change to slider collection, calculation or stored volume plans.

### Artifacts

| Path | Change | Purpose |
|---|---|---|
| `routes/volume_splitter.py` | Modify | Validate export input; retain HTTP parser outcomes; log unexpected errors |
| `static/js/modules/volume-splitter.js` | Modify | Gate blob/download creation on HTTP success |
| `tests/test_volume_splitter_api.py` | Modify | Route contracts and real workbook compatibility assertions |
| `e2e/volume-splitter.spec.ts` | Modify | Strict successful-download and error-without-download cases |
| `docs/product/APP_FLOW.md` | Modify | Distribute export success/validation/failure outcomes |
| `docs/test_inventory/TEST_INVENTORY.md` and `.json` | Regenerate | Added pytest and Playwright case identities/counts |
| `docs/volume_export_validation/PLANNING.md` | Maintain | Approvals, council findings, response matrix and implementation evidence |

**Effort:** S–M. **Owner:** implementation agent after Gate 1.
**Depends on:** council completion, Q1 disposition and direct owner Gate 1 approval.
Use the existing checkout and a fresh branch from current `main`; no worktree is
commissioned by this plan.

### Test design

- Parameterize invalid nonempty root shapes, invalid `volumes` containers and
  invalid map values. Assert exact HTTP status and standard envelope, with safe
  messages and no accidental successful binary response. Include numeric strings,
  bool, nested arrays/objects, null and float NaN/infinities.
- Assert each parsed falsy-root fallback, missing/empty volumes, malformed JSON,
  empty JSON body and non-JSON content type. Keep `BAD_REQUEST`,
  `UNSUPPORTED_MEDIA_TYPE` and local `VALIDATION_ERROR` distinct.
- Load a real successful workbook and assert the literal sheet name, all three
  headers, row values, empty result, MIME and filename pattern. Cover fractional,
  zero and negative finite values and representative training-day conversions,
  fallback/clamp, NaN fallback and infinity safe-500 behavior.
- Inject a builder failure; assert a generic 500 envelope and no internal exception
  text. This tests the new local catch rather than relying solely on global handling.
- Browser success test waits for and asserts a real download. It must not catch a
  missing download and accept `null`, as the older weak test currently does.
- New browser tests use `e2e/console-guard.ts`, following the existing strict-fixture
  pattern in the volume spec. Mock representative 400 and 500 responses; assert
  one generic error toast, no `createObjectURL` call and no download event. Set up
  download/object-URL observation before the click and wait on the toast's error
  completion path, avoiding a fixed timeout as the negative-download oracle.
  Allow only the specific expected HTTP/console errors with anchored patterns.
- Manual smoke against private data: a valid slider export downloads a workbook;
  an injected HTTP error shows one readable toast and creates no download. Restore
  the mock; export succeeds again. Record the original failed response separately.

### Sequence

1. Obtain the three cold council reviews; preserve their outputs and resolve every
   finding in the response matrix and Plan v2.
2. Obtain direct owner Gate 1 approval, including the Q1 parser interpretation.
3. Recheck current source, claims and issue state; create a focused branch. Add
   meaningful route/browser regression coverage, then implement route and caller.
4. Update the product flow, regenerate inventory and run the applicable gates.
5. Run required independent code, product-risk and unslop reviews; address findings.
6. Publish a reviewed PR with migration notes and exact validation evidence. Keep
   the mixed-scope #625 issue open and leave merge to the owner.

### Expected gates — council test-strategist to confirm

- Pytest: `tests/test_volume_splitter_api.py` plus
  `tests/test_app_factory.py`; derive additional tests from changed behavior if the
  council changes the artifact list. The service/formula remain untouched.
- Chromium, serial with private runtime/database and zero retries:
  `volume-splitter.spec.ts`, `volume-progress.spec.ts`,
  `api-integration.spec.ts`, `validation-boundary.spec.ts`,
  `error-handling.spec.ts`, `empty-states.spec.ts`, `accessibility.spec.ts`.
  This is the frontend feature/error/API union in the quality guide.
- Interactive manual smoke above; generated inventory check; TypeScript and
  pyright baseline comparison with no new diagnostics; diff check.
- `/unslop` after implementation: independent `code-reviewer`,
  `product-risk-reviewer` for the new route outcome and `unslop-reviewer`.
- No workflow, schema, calculation, CSS or visual-baseline change. No baseline
  regeneration or live workflow dispatch is selected.

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `/root/volume_export_pm` | Canonical ID supplied by the manager; author of this Section 0 and Plan v1 |
| `product-manager` — response matrix + Plan v2 | `/root/volume_export_pm` | Same PM resumed for council Step 4; ID re-supplied by the manager |
| `architecture-reviewer` | `/root/volume_export_architecture` | Manager-supplied reviewer ID; verbatim findings below |
| `test-strategist` | `/root/volume_export_tests` | Manager-supplied reviewer ID; verbatim findings below |
| `product-risk-reviewer` | `/root/volume_export_product` | Manager-supplied reviewer ID; verbatim findings below |

**Same product-manager resumed for matrix + Plan v2?** Yes. The manager resumed
`/root/volume_export_pm` and re-supplied its recorded ID for this write.

**Evidence gap:** none.

## Reviewer findings

The outputs below are verbatim. The test and product reviews requested revisions
to Plan v1; the response matrix records those corrections in Plan v2 without
recasting either original verdict as a pass or an owner approval.

### architecture-reviewer (agent `/root/volume_export_architecture`)

**Plan is sound — no architecture findings.**

- Route-boundary validation preserves the module split: HTTP/type checks stay in `routes/volume_splitter.py`; workbook construction and `round(weekly_sets / training_days, 1)` remain in the unchanged service.
- Parsing before the export exception handler preserves registered 400/415 handling. The proposed falsy-root table matches the current `request.get_json() or {}` behavior.
- Training-day coercion, `TypeError`/`ValueError` fallback, lower clamp and uncaught overflow behavior match current source. The plan distinguishes these from the newly rejected nonfinite volume values.
- Standard error envelopes, module logging and the successful binary response remain covered. No blueprint, schema, DB access or infrastructure change is introduced.
- Q1 correctly exposes the empty-body wording discrepancy for owner disposition at Gate 1; this review does not resolve it or authorize implementation.

Reviewed the plan and referenced source directly. No files changed, tests run or runtime/DB actions performed.

### test-strategist (agent `/root/volume_export_tests`)

1. **Add the existing readiness contract to artifacts and gates** — `docs/volume_export_validation/PLANNING.md:178,229`.
   `tests/test_volume_history_busy_signal_contracts.py:117` pins exactly six occurrences of `await waitForVolumeSplitterReady(page);` in the edited spec. New strict test blocks may change that count and fail CI.
   **Fix:** include this module in targeted pytest; if new initialization sites are added, update its literal count and explanation without weakening the assertion or replacing the deterministic waiter.

2. **Make the injected-failure test distinguish local handling from the existing fallback** — `docs/volume_export_validation/PLANNING.md:201`.
   `utils/errors.py:273` already catches an unhandled builder exception and returns a generic 500. Status/envelope/no-leaked-text assertions alone cannot substantiate the plan’s claim that the test exercises the new route-local catch.
   **Fix:** additionally spy on the route module’s `logger.exception` and assert the expected export-failure log, or pin a distinct safe local export message. For rejected payloads, assert the workbook builder is not called.

Required gate union:

- **Pytest:** `tests/test_volume_splitter_api.py`, `tests/test_app_factory.py`, `tests/test_volume_history_busy_signal_contracts.py`.
- **Chromium:** `volume-splitter.spec.ts`, `volume-progress.spec.ts`, `api-integration.spec.ts`, `validation-boundary.spec.ts`, `error-handling.spec.ts`, `empty-states.spec.ts`, `accessibility.spec.ts`.
- **Other:** interactive private-runtime smoke, generated inventory regeneration/check, TypeScript, pyright baseline comparison, diff check; independent code, product-risk and unslop reviews.

Existing route tests cover calculation, persistence and history, but no direct Excel-export route test was found. The existing browser download test at `e2e/volume-splitter.spec.ts:332` accepts a missing download; the proposed strict success and error-without-download cases fill that gap. Parsed-falsy roots, parser 400/415 separation, finite fractional/negative volumes and training-day compatibility are otherwise covered adequately by the planned cases.

No fixture/schema/blueprint changes are needed. No full pytest, full E2E or visual-baseline gate is warranted by the listed paths. Q1 remains an explicit owner decision before implementation.

**Verdict: Needs revision; targeted gates are sufficient after the two corrections.**

### product-risk-reviewer (agent `/root/volume_export_product`)

1. `docs/volume_export_validation/PLANNING.md:62` — The migration description overstates “500 → 400” for all rejected values.
   - Invariant at risk: accurate migration notes under `CLAUDE.md`’s refactor invariant.
   - Current `build_volume_excel()` accepts boolean volumes: Python division treats `true` as 1, and openpyxl supports boolean cells. The approved validation deliberately changes these successful exports to 400.
   - Fix: distinguish the six reproduced 500 cases from newly rejected boolean values; document the boolean compatibility change explicitly.

The plan otherwise preserves calculation semantics, training-day behavior, safe failure copy and scope. Q1 correctly leaves the empty-body interpretation for explicit Gate 1 confirmation.

**Needs revision — one migration-description correction; no calculation or non-goal violation.**

## Response matrix

Manager-proposed dispositions, applied by the same PM in council Step 4 and
confirmed by the owner's Gate 1 approval on 16 November 2026. There are no rejected
or deferred findings.

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| AR — no architecture findings | architecture-reviewer | Accept; no action | Retain route-boundary validation, unchanged service/formula and parser separation |
| TS1 — edited browser spec has a literal readiness-site contract | test-strategist | Accept | Add `tests/test_volume_history_busy_signal_contracts.py` to artifacts and targeted pytest; update only its readiness-count literal/explanation if new initialization sites require it |
| TS2 — generic 500 alone cannot prove the route-local catch ran | test-strategist | Accept | Spy on `routes.volume_splitter.logger.exception` and assert its export-failure call; assert rejected inputs never call the workbook builder |
| PR1 — boolean volumes currently export successfully | product-risk-reviewer | Accept | Distinguish boolean success-to-400 compatibility change from the six measured 500-to-400 cases in migration notes and tests |

## Plan v2

**Goal:** malformed volume exports return safe client errors, and the browser
reports export failures without downloading an error document. Plan v1 remains
above as the reviewed input; this standalone Plan v2 incorporates all findings.

**Calculation surface:** no service, formula or schema change.
`build_volume_excel()` retains `round(weekly_sets / training_days, 1)`. Twelve
weekly sets over three days still exports four per session; 12.5 still exports
4.2. Validation changes accepted request values, not the calculation for valid
numeric inputs.

### Scope and migration contract

Change only the volume Excel route's input handling and its existing browser
download caller, with tests and documentation. Keep binary success responses,
workbook layout, filename, MIME, training-day compatibility and the service
unchanged. Introduce no new range, positive-only rule, muscle whitelist,
sets/reps/RPE policy, persistence, schema or browser-support change. Other export
proposals and other #625 entries remain separate.

The migration description must distinguish these changes:

- The six reproduced malformed shapes—string/null weekly sets, list/null
  `volumes`, and nonempty list/string roots—currently return 500 and will return
  standard 400 `VALIDATION_ERROR` envelopes.
- Boolean **volume values** currently produce successful workbooks because Python
  treats them numerically and openpyxl writes boolean cells. The approved
  finite-number/excluding-bool contract deliberately changes those successes to
  400. Test both `true` and `false` values and state this compatibility change in
  the PR description; do not describe it as a repaired 500.
- Parsed falsy **root values** retain their existing fallback. This is distinct
  from a boolean value inside the `volumes` map.
- Other invalid values are rejected according to the approved boundary contract;
  do not claim their previous status was measured without a corresponding receipt.
- Valid finite numeric exports retain their values and calculation. A 4xx/5xx no
  longer becomes a downloaded error document in the browser.

### Route design and exact outcomes

In `routes/volume_splitter.py`, call `request.get_json()` before the export
exception handler, retaining global HTTP exception handling. Normalize with the
existing `or {}` expression. Validate the normalized root, `volumes` container
and map values before invoking `build_volume_excel()`.

| Input | Outcome after this change |
|---|---|
| Parsed `null`, `false`, `0`, `0.0`, `""`, `[]`, or `{}` | Existing fallback; header-only XLSX |
| Nonempty list/string, `true`, or nonzero numeric root | 400 `VALIDATION_ERROR`; safe JSON-object message |
| Object with omitted `volumes` or `volumes: {}` | Header-only XLSX |
| Supplied null/list/string/number/boolean `volumes` | 400 `VALIDATION_ERROR`; safe volumes-object message |
| All map values are finite ints/floats, excluding bool | Values pass unchanged to the existing builder |
| A map value is null/string/list/object/bool or nonfinite | 400 `VALIDATION_ERROR`; safe finite-numbers message |
| Malformed JSON or empty `application/json` body | Registered 400 `BAD_REQUEST`, proposed under Q1 |
| Unsupported/missing JSON content type | Registered 415 `UNSUPPORTED_MEDIA_TYPE`, proposed under Q1 |
| Unexpected builder or file-response failure | Route logger records the export failure; safe generic 500 |

Use existing `error_response()` and the route module's logger. Keep validation at
the HTTP boundary; add no single-caller validation module. Do not catch JSON
parsing broadly and convert registered 400/415 outcomes into 500.

Explicitly reject `bool` before accepting `int`. Integers are finite without a
float conversion; use `math.isfinite()` only on float values. No new numeric cap
is introduced accidentally through integer-to-float conversion. Existing
representability or arithmetic failures during workbook construction stay safe
generic 500s, with their cause logged.

### Training-day preservation

Leave `utils/volume_splitter_service.py` unchanged:

| Value | Behavior retained |
|---|---|
| Missing, null, or input causing `TypeError`/`ValueError` in `int()` | Fallback to 3 |
| Zero, negative or `false` | Lower clamp to 1 |
| Positive integer, integer string or finite fractional number | Existing `int()` conversion, then clamp |
| Parser-admitted NaN | Existing `ValueError` fallback to 3 |
| Parser-admitted positive/negative infinity | Existing `OverflowError`, now logged by the local catch and returned as a generic 500 |

This preserves the approved training-day contract. Rejecting nonfinite volume
values does not select a new nonfinite training-day rule, upper bound or broader
fallback. Tests distinguish these cases.

### Browser design

In `static/js/modules/volume-splitter.js`, check `response.ok` before consuming a
response as a blob. An HTTP failure throws into the existing catch, which retains
its meaningful console error and shows the existing generic error toast once.
Do not expose arbitrary server error text. Do not create an object URL, link or
download on that error path. Preserve successful download creation, cleanup,
slider collection, calculation and saved-plan behavior.

### Artifacts

| Path | Change | Purpose |
|---|---|---|
| `routes/volume_splitter.py` | Modify | Boundary validation and local safe failure handling, preserving parser outcomes |
| `static/js/modules/volume-splitter.js` | Modify | Check HTTP success before blob/download creation |
| `tests/test_volume_splitter_api.py` | Modify | Route outcomes, real workbook compatibility and local-handler/builder-call spies |
| `tests/test_volume_history_busy_signal_contracts.py` | Run; narrowly modify if needed | Retain the exact deterministic readiness-site contract; update its literal count and explanation only if added initialization sites change it |
| `e2e/volume-splitter.spec.ts` | Modify | Strict successful download and error-without-download cases |
| `docs/product/APP_FLOW.md` | Modify | Distribute export success/validation/failure behavior |
| `docs/test_inventory/TEST_INVENTORY.md` and `.json` | Regenerate | Changed pytest and Playwright inventory |
| `docs/volume_export_validation/PLANNING.md` | Maintain | This approval/review record and later implementation evidence |

**Effort:** S–M. **Owner:** implementation agent after Gate 1.
**Dependencies:** direct owner Gate 1 approval of Plan v2, its response-matrix
dispositions and Q1. Use the existing checkout and a fresh branch from current
`main`; no additional worktree or clone is commissioned.

### Test design

1. Parameterize invalid nonempty roots, invalid `volumes` containers and invalid
   map values. Cover numeric strings, bool, nested arrays/objects, null and float
   NaN/infinities. Assert 400, the standard envelope and safe messages. Spy on the
   workbook builder and assert it is never called for rejected inputs.
2. Assert every parsed falsy-root fallback, missing/empty volumes, malformed JSON,
   empty JSON body and non-JSON content type. Keep `BAD_REQUEST`,
   `UNSUPPORTED_MEDIA_TYPE` and local `VALIDATION_ERROR` distinct. Q1 must be
   resolved before implementing the empty-body expectations.
3. Load successful workbooks and assert the literal `Volume Plan` sheet name,
   three existing headers, row values, header-only result, MIME and filename
   pattern. Cover finite fractional, zero and negative values; training-day
   conversions, fallback/clamp, NaN fallback and infinity safe-500 behavior.
4. Inject a workbook-builder exception. Assert the generic 500 envelope and no
   leaked internal text **and** spy on
   `routes.volume_splitter.logger.exception`, asserting the route's expected
   export-failure log call. This differentiates the new local handler from the
   pre-existing global fallback.
5. Add a strict real-download browser case. A missing download must fail; do not
   accept a caught timeout or `null` result as success.
6. New cases use `e2e/console-guard.ts`, following the strict pattern already in
   the volume spec. Mock representative 400 and 500 replies. Install object-URL
   and download observers before clicking; wait for the error-completion toast,
   then assert exactly one generic toast, no object-URL call and no download.
   Use only anchored allowances for the specific expected HTTP/console errors;
   introduce no fixed timeout as the negative-download oracle.
7. If new initialization sites alter the count pinned by
   `test_volume_history_busy_signal_contracts.py`, update the literal and its
   explanation to match the actual sites. Keep the deterministic waiter and exact
   assertion; do not weaken or replace either.
8. Perform an interactive smoke against private runtime/data: valid sliders
   produce a readable workbook; an injected HTTP error produces one toast and no
   download; restoring the mock restores successful export. Retain the original
   failed response separately.

### Sequence and gates

1. Obtain direct owner Gate 1 approval of Plan v2, including Q1 and the response
   matrix. No code change precedes it.
2. Recheck current source, issue state and path/resource claims. Create the
   focused implementation branch in the existing checkout.
3. Add regression coverage and implement the route/caller changes. Preserve the
   unchanged service/formula and existing test guarantees.
4. Update the product flow and generated inventory. Run the union below:
   - Pytest: `tests/test_volume_splitter_api.py`, `tests/test_app_factory.py`,
     `tests/test_volume_history_busy_signal_contracts.py`.
   - Chromium, serial, private runtime/database, zero retries:
     `volume-splitter.spec.ts`, `volume-progress.spec.ts`,
     `api-integration.spec.ts`, `validation-boundary.spec.ts`,
     `error-handling.spec.ts`, `empty-states.spec.ts`, `accessibility.spec.ts`.
   - Interactive smoke; inventory regeneration/check; TypeScript; pyright
     baseline comparison with no new diagnostics; diff check.
5. Run `/unslop` with independent `code-reviewer`, `product-risk-reviewer` for
   the changed route outcome, and `unslop-reviewer`. Address findings before
   publication. The test-strategist found no need for full pytest, full E2E or
   visual-baseline gates for this artifact list.
6. Publish the reviewed PR with the explicit boolean-success-to-400 migration
   note, the measured 500-to-400 cases and validation evidence. Keep the other
   #625 entries open; merge requires separate owner approval of the named PR/head.

No workflow, schema, CSS or committed visual baseline changes are included. No
baseline regeneration, live workflow dispatch or unrelated export cleanup is
authorized by this plan.

### Gate 1 decision

The recommended Q1 disposition is to preserve current parser behavior: empty
`application/json` body → 400 `BAD_REQUEST`; unsupported/missing JSON content type
→ 415 `UNSUPPORTED_MEDIA_TYPE`; successfully parsed falsy JSON roots retain the
header-only-workbook fallback. The owner confirmed this interpretation with
Plan v2 on 16 November 2026, as recorded below.

### Gate 1 sign-off — 16 November 2026

**Direct owner reply, verbatim:**

> Approve Plan v2 and preserve parser behavior

The reply answered the question approving this #625 Plan v2 while preserving an
empty JSON body's HTTP 400, unsupported/non-JSON content type's HTTP 415 and parsed
JSON `null`'s header-only workbook fallback, and explicitly excluding boolean
volume values. It approves Plan v2 and confirms every response-matrix disposition.
Q1 is resolved in favor of the parser behavior specified above. Boolean values
inside the `volumes` map remain rejected, as the approved plan requires; parsed
falsy roots retain their separate existing fallback.

The implementation agent may proceed with this bounded route/caller packet and
its required validation and reviews. This approval grants no merge authority and
does not select the other entries in #625.

## Sign-off

- [x] Gate 0 approval recorded with its exact direct reply and packet scope.
- [x] Every council finding has a disposition; all are accepted in Plan v2.
- [x] Council provenance and continuity block complete; evidence gap is none.
- [x] Q1 parser wording reconciled with the owner: preserve current parser behavior.
- [x] Owner approved Plan v2 and its response-matrix dispositions — Gate 1, 16 November 2026.
- [x] Ready to implement; required implementation tests and reviews still apply.

## Implementation evidence — 16 November 2026

Implemented on `fix/625-volume-export-validation`. The route validates finite
numeric volume values while excluding booleans, preserves parser 400/415 outcomes
by parsing before its export catch, and logs unexpected failures while returning
a generic 500. The caller checks `response.ok` before creating a blob or download.
`utils/volume_splitter_service.py` and its calculation remain unchanged.

| Check | Result |
|---|---|
| New API cases before production changes | 25 intended failures and 26 compatibility passes |
| Three planned pytest modules | 118 passed |
| Seven planned Chromium specs | 226 passed, zero retries |
| Focused download/error/recovery cases | 3 passed |
| TypeScript | Clean |
| Pyright baseline comparison | Zero diagnostics, zero net-new diagnostics; baseline unchanged |
| Generated inventory and diff checks | Passed |
| Independent code, unslop and product-risk reviews | PASS, no findings |

The readiness contract's exact literal changed from six initialization sites to
seven for the one added `beforeEach`; its deterministic waiter and exact assertion
remain intact. An initial pyright run reported four optional-`book.active`
diagnostics in the new tests. Selecting the named `Volume Plan` sheet corrected
them; the original receipt is retained and the baseline was not changed.

A separate private-runtime UI smoke downloaded a valid workbook, then injected
400 and 500 responses. Each error showed one generic readable toast and created
zero object URLs or downloads. Restoring successful responses produced one
download and one object URL. Both downloaded workbooks reopened successfully
with equal row values; the toast screenshot was inspected for readability.

Required review identities: `code-reviewer` — `/root/export_code_review`;
`unslop-reviewer` — `/root/export_unslop_review`; `product-risk-reviewer` —
`/root/volume_export_product`.

Evidence is retained under `artifacts/607-625-20261116/`, including
`pytest625-typed.xml`, `625-e2e-gate.log`, `625-ui-smoke.json`,
`625-workbook-smoke.json` and `625-pyright.json`.

This entry precedes PR publication. Remote CI and merge remain pending; these
local results do not claim either. Merge requires the owner's separate approval
of the named PR and head.
