# Plan Review — Internal exception messages in API responses

Status: **Gate 0 and Gate 1 approved. Plan v2 implementation and API fix PR preparation are authorized, sequenced after the filename branch's frozen verification/publication. Merge remains separately gated.**

Source inspected: GitHub `main` `302ef0e9fcbdf21f4ffd6d52dcf09770a8892252`. The planning checkout at `c56caaae9d663313cdfb343a40f8e1a381c53bc8` has the same source tree. Source references below use that snapshot; refresh affected-source equivalence before implementation.

Native findings: [CodeQL #2](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/security/code-scanning/2), [CodeQL #3](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/security/code-scanning/3). Coordination and settings decisions remain in [#588](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/588). The code-scanning pages own alert dispositions.

## Section 0 — Requirements Brief

**Raw request and direct owner answer** (verbatim)

> Approve these Gate 0 requirements for alerts #2 and #3: replace unexpected internal errors with “Failed to add exercise” or “Failed to save generated plan,” retain full details in logs, and preserve existing HTTP statuses, response fields and useful validation messages? Approval starts preparation of the required council-reviewed plan (architecture, test strategy and product risk); implementation awaits your later plan approval.

> Approve requirements and required planning review

Owner reply: `call_2508a55fa8ab40659cc9087335ba7561`, question item 2. The manager recorded it in the ignored receipt `artifacts/codeql_remaining_20261024/OWNER_APPROVALS.json`; its top-level `exception_gate0_approved: true` is the current authority. The earlier proposal nested inside that receipt retains its historical unapproved flags.

**Problem**

Two unexpected persistence failures expose exception details to the client. `ExerciseManager.add_exercise()` returns `Database error: {exc}` (`utils/exercise_manager.py:105–107`), which the add-exercise route forwards through `error_response()`. `_add_persistence_result()` stores `str(e)` in `persist_error` (`utils/plan_generator.py:1514–1528`), and the starter-plan route includes it in a successful JSON envelope (`routes/workout_plan.py:592`). Internal database or filesystem details should remain in the server log while the client receives stable failure text.

**Acceptance criteria**

1. Given an unexpected database exception during add-exercise persistence, the producer returns exactly `Failed to add exercise`; `POST /add_exercise` returns HTTP 500 with `INTERNAL_ERROR` and its existing JSON envelope. The unexpected exception's distinguishing detail is absent from both client message fields and present in the server's exception record.
2. Given an unexpected exception from generated-plan persistence, the result retains `persisted: false` and a string `persist_error`, whose value is exactly `Failed to save generated plan`. `POST /generate_starter_plan` retains HTTP 200 and its existing successful outer envelope; the internal exception detail is absent from client data and present in server logging.
3. Expected validation messages, validation codes/statuses, duplicate detection, success outcomes, JSON field names/types and ordinary generated-plan data remain unchanged. Body-composition and backup validation paths remain unchanged.
4. Fault-injection coverage exercises the actual changed producers and their HTTP outcomes. It proves omission from the client and retention in logs, alongside the existing success and validation regressions.
5. The PR description explains the intentional response-text migration. Generated test inventory is regenerated through its generator if case counts change.
6. After an independently reviewed implementation and separately approved merge, inspect current-main CodeQL origins and alert states. An alert is recorded as fixed only when native readback confirms it. Remaining expected-validation origins are assessed separately, without masking useful validation to force scanner closure.

**Calculation surface**

- `none`: no generation selection, prescriptions, volume, Effective Sets, RIR/RPE, progression, persistence transaction semantics or schema changes.
- Observable error example: before, `RuntimeError("internal-only-sentinel")` may appear in client failure text; after, the client sees the approved generic message while the exception record retains `internal-only-sentinel`.
- Migration notes and updated failure-path tests are required because response text changes, even though status and envelope fields remain stable.

**In scope**

- The two unexpected-error producers, their local exception logging, relevant unit/HTTP regressions, generated test inventory and the Plan workflow's failure description.
- One bounded remediation PR after Gate 1, with native alerts linked and duplication checked before publication.

**Out of scope / non-goals**

- Blanket redaction in `utils/errors.error_response()`, changes to expected `ValueError` feedback, new response fields, status-code redesign, schema or transaction changes, calculation changes, frontend/CSS changes, screenshot baselines, authentication, cloud services or telemetry.
- Alert dismissal, blocking CodeQL activation, bypass changes and merging. Each remains a separate owner-authorized operation.
- The separately approved filename-cleanup PR for alerts #1/#9 and the completed alert #4 disposition.

**Assumptions made**

- No new product assumption is needed: the two generic messages and preserved contracts were specified in the approved requirements.
- Logging uses the modules' existing `get_logger()` instances; both modules already define `logger` (`utils/exercise_manager.py:5–10`, `utils/plan_generator.py:14–25`). Log-capture mechanics must be verified by the test strategist rather than assuming root-logger propagation.
- The plan is bounded to unexpected failures. Alert #2 also reports expected-validation origins, so removal of the unexpected database origin does not guarantee that the entire native alert automatically closes.

**Open questions for the user**

- `none` blocking Plan v1 drafting. Any council finding that changes the approved messages or preserved contracts returns to the owner before Gate 1.

### Section 0 sign-off — GATE 0

- [x] User confirms the acceptance criteria match intent: direct answer “Approve requirements and required planning review”.
- [x] Requirements preserve the exact selected messages, logging and response/validation contracts; no additional product assumption was selected independently.
- [x] Blocking requirements questions are answered for drafting and council review.

## Plan v1

**Goal:** Keep unexpected add-exercise and generated-plan persistence details in server logs while preserving the approved client failure signals.

**Scope**

- **In:** replace only the two unexpected exception strings; retain/add `logger.exception()` at the producer; add focused producer/HTTP fault coverage; document the two text changes; regenerate inventory when needed.
- **Out:** the exclusions in Section 0. Route serialization and the shared error helper remain unchanged unless a council-approved necessity is found and explicitly included in Plan v2.

**Facts supporting the design**

- `ExerciseManager.add_exercise()` already logs the active exception before returning its text (`utils/exercise_manager.py:105–107`). Keep that log and replace only its return string.
- The route classifies returned text into validation or internal errors (`routes/workout_plan.py:122–143`). The approved generic failure text follows the existing HTTP 500 / `INTERNAL_ERROR` branch; preserve the early expected-validation and duplicate messages.
- `_add_persistence_result()` catches persistence failure and attaches outcome fields (`utils/plan_generator.py:1521–1530`). Add an exception log inside that same catch, then replace only `persist_error` text. Preserve the `should_persist=False` branch and successful `inserted_counts` behavior.
- The starter-plan route deliberately returns the generated result through `jsonify(success_response(data=result))` (`routes/workout_plan.py:592`). Keep the partial-persistence-failure envelope and HTTP status unchanged.
- `tests/test_plan_generator_refactor_contracts.py:172–190` explicitly requires `{"persisted": False, "persist_error": "write failed"}`. Its text expectation must change intentionally while retaining the failure shape.
- `PlanGenerator.persist()` has separate row-failure/continuation semantics already covered at `tests/test_plan_generator_refactor_contracts.py:114–169`. Do not change that algorithm, its exception boundary or transaction behavior.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/exercise_manager.py` | Modify | Generic unexpected DB-failure return; retain existing exception logging and expected validation/success strings. |
| `utils/plan_generator.py` | Modify | Log the active unexpected persistence exception; use the approved generic `persist_error` value only in `_add_persistence_result()`. |
| `tests/test_exercise_manager.py` | Modify | Actual producer fault injection: exact generic result, internal sentinel excluded, exception detail logged; preserve existing ordinary/duplicate/validation cases. |
| `tests/test_plan_generator_refactor_contracts.py` | Modify | Update the explicit public-text contract and verify full logged exception detail; preserve persistence success, disabled-persistence and row-failure contracts. |
| `tests/test_workout_plan_routes.py` | Modify | HTTP fault cases through the real changed producers: add-exercise HTTP 500 and both message fields; generator HTTP 200, `persisted: false`, string generic `persist_error`. Do not mock the final HTTP response into the expected answer. |
| `docs/product/APP_FLOW.md` | Modify narrowly | Document the Plan workflow's two generic unexpected-error messages and preserved response outcomes; the generator control is documented near line 298. |
| `docs/test_inventory/TEST_INVENTORY.json`, `docs/test_inventory/TEST_INVENTORY.md` | Regenerate if case counts change | Use the repository generator; never hand-edit counts or baselines. |
| `docs/codeql_exception_responses/PLANNING.md` | Planning record | Sole council artifact, including approved requirements, verbatim reviews, response matrix and Plan v2. |
| PR description | Author | Before/after failure examples, explicit message migration, preserved status/envelope fields, validation and native alert readback. |

**Effort:** M implementation · **Planning classification:** Large/API surface under `QUALITY_GATE.md` · **Owner:** implementation unassigned until Gate 1 · **Depends on:** council response matrix, owner-approved Plan v2 and an isolated implementation/runtime lane.

**Sequence**

1. Complete the three cold council reviews of this Plan v1. The manager supplies all returned reviewer handles and proposes a disposition for every finding; the same PM writes the matrix and Plan v2.
2. Obtain direct owner Gate 1 approval of Plan v2. No API source/test implementation is authorized by Gate 0 alone.
3. Before implementation/publication, refresh affected-source equivalence and duplicate issue/PR state. Preserve all worktree/branch/recovery holds and establish the selected lane's runtime/DB isolation.
4. Add meaningful fault coverage at the real producer boundaries. Use an unmistakable synthetic internal-error marker; check client omission and captured exception detail. A bare assertion that `logger.exception()` was called is insufficient proof of retained detail.
5. Make the two producer changes and corresponding logging change. Keep routes, shared helpers, expected validations and persistence algorithms unchanged. Exercise the positive/negative regression union.
6. Update the narrow Plan workflow documentation and migration notes; regenerate inventory if tests change. Run the applicable verification/diagnostic gates and address all required diff-review findings before commit/publication.
7. Prepare one remediation PR linked to native alerts #2/#3 and #588. Obtain a separate exact-head merge approval; then inspect merged-main CI/CodeQL and record each affected origin's state.
8. If #2 remains only for expected-validation paths, retain that native alert for source review and a separate owner disposition. Do not dismiss it automatically, blanket-mask validations or declare full closure from a clean PR-diff scan.

**Expected gates — provisional selection for the test-strategist to confirm**

- Focused development coverage: `tests/test_exercise_manager.py`, `tests/test_plan_generator_refactor_contracts.py`, `tests/test_workout_plan_routes.py`.
- Existing utility-import regression union found by the canonical derivation search: the three files above plus `tests/test_plan_generator.py`, `tests/test_phase3_features.py`, `tests/test_pattern_coverage.py`, `tests/test_superset.py`, `tests/test_utils_package.py`, `tests/test_weekly_summary.py`. The strategist must distinguish actual affected behavior from incidental imports.
- Proposed final gate: `/verify-and-polish` for the two-module change, including `/verify-suite` (pytest then full Chromium only after pytest passes), followed by staged-diff `code-reviewer` and `unslop-reviewer`. The strategist confirms the applicable union under `QUALITY_GATE.md` and the documented command procedure.
- Required native checks include Type Check / no net-new Pyright diagnostics and Test Inventory Drift. Preserve their baselines and inventory contracts.
- No CSS/build/screenshot change is planned. Any inherited visual result encountered by a required full run must be recorded with first-attempt evidence; a recovered retry is not a clean pass and cannot be accepted for the owner.
- Unit/HTTP tests use the repository's isolated fixtures. This planning stage runs no tests, imports no application/DB modules and accesses no database.

**Risks and controls**

| Risk | Control |
|---|---|
| Useful validation feedback is lost while fixing a shared sink | Change only the two unexpected-error producers; keep shared `error_response()` and expected `ValueError` branches intact. |
| Returned text changes route classification | Pin the real add-exercise HTTP 500 / `INTERNAL_ERROR` outcome and unchanged expected-validation outcomes. |
| Generator persistence failure becomes an HTTP error or loses failure metadata | Keep HTTP 200, successful outer envelope, `persisted: false` and a string `persist_error`; assert the real serialized result. |
| Logging test proves a method call but loses diagnostic details | Capture the actual exception record/formatted output with its active exception and assert the synthetic internal marker is present. |
| Scanner pressure broadens scope into expected errors | Review every remaining CodeQL origin after merge and require a separate owner alert disposition where appropriate. |
| Fixture or testing work changes calculations or persistence semantics | Reuse isolated fixtures, preserve success/row-continuation tests, and make no algorithm, schema, transaction or runtime-startup edit. |

## Agent provenance

The Codex collaboration tool returns canonical task handles rather than a separate opaque ID. The manager recorded and supplied every exact returned handle below, then resumed the same PM handle to write the response matrix and Plan v2. No identifier was inferred or manufactured. Plan v1 above remains unchanged as the input to the cold reviews.

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `/root/api_plan_pm` | Supplied by the manager after spawn; author of Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `/root/api_plan_pm` | The same PM was resumed with all verbatim reviews and manager-proposed dispositions. |
| `architecture-reviewer` | `/root/api_plan_architecture` | Completed cold, read-only review of Plan v1; verbatim output below. |
| `test-strategist` | `/root/api_plan_test_strategy` | Completed cold, read-only review of Plan v1; verbatim output below. |
| `product-risk-reviewer` | `/root/api_plan_product_risk` | Completed cold, read-only review of Plan v1; verbatim output below. |

**Same product-manager resumed for the matrix + Plan v2?** `yes` — the manager resumed `/root/api_plan_pm`, the same returned handle recorded for Plan v1.

**Evidence gap:** `none`. Canonical returned handles and same-PM continuity are recorded; no completed review was rerun to manufacture provenance.

## Reviewer findings

The completed reviews below are reproduced verbatim inside Markdown fences. Their findings concern Plan v1 and each reviewer's stated read-only coverage. They grant neither an implementation pass nor owner approval.

### architecture-reviewer (agent `/root/api_plan_architecture`)

```markdown
No findings.

Coverage: reviewed both unexpected-error producers (`utils/exercise_manager.py:105`, `utils/plan_generator.py:1514`), their callers, add-exercise classification (`routes/workout_plan.py:124`), starter-plan serialization (`routes/workout_plan.py:592`), shared response helpers, logging, existing persistence contracts and proposed artifact boundaries.

The approved generic messages fit the existing response paths. The plan preserves expected validation, HTTP statuses, envelope fields, persistence semantics and module boundaries. It requires no blueprint, schema, normalization or shared-configuration changes.

This was a read-only architecture review. No tests, application imports, DB access or file changes occurred. Gate 0 authority was verified separately; Gate 1 and implementation remain unapproved.

**Plan is sound.**
```

### test-strategist (agent `/root/api_plan_test_strategy`)

```markdown
Completed read-only review of Plan v1. No tests, collection, imports, DB access, servers, writes or Git mutations were performed.

## Findings

**T1 — Medium: specify separate functional and visual-seed verification runs.**

Location: `docs/codeql_exception_responses/PLANNING.md:114–116`.

The selected `/verify-suite` scope is correct, but its literal Chromium command runs the entire corpus against one seed. `playwright.config.ts:83–89` selects different preparation scripts, and `e2e/CLAUDE.md:105–107` explains why the visual seed cannot substitute for the functional seed. `.github/workflows/deep-gate.yml:93–128` explicitly separates the three visual-seed specs.

**Correction:** Preserve full corpus coverage through two sequential partitions after full pytest passes:

- All specs except `visual.spec.ts`, `visual-baseline-thumbnails.spec.ts` and `workout-plan-desktop-contract.spec.ts`, with `PW_VISUAL_SEED` unset/`0`.
- Exactly those three specs with `PW_VISUAL_SEED=1`.

Use fresh, separate throwaway DB and report paths, no reused server, one worker and zero retries. Retain first-attempt results. Compare existing platform baselines; regeneration remains unauthorized. This is complete corpus coverage, not an exemption.

**T2 — Medium: useful validation text needs an explicit HTTP preservation assertion.**

Locations: `docs/codeql_exception_responses/PLANNING.md:27–28`, `:89–91`; existing tests at `tests/test_workout_plan_routes.py:89–134` and `:718–724`.

The plan preserves useful validation messages but currently relies on existing regressions that mainly assert status and error code. The generator’s expected `ValueError` response at `routes/workout_plan.py:594–596` lacks a verified exact-message regression.

**Correction:** In `tests/test_workout_plan_routes.py`, add a real request using otherwise valid generator parameters and `priority_muscles: "chest"`. `GeneratorConfig.__post_init__()` at `utils/plan_generator.py:284–286` raises `ValueError("priority_muscles must be a list")`. Assert HTTP 400, `VALIDATION_ERROR`, and that exact useful text in both client message fields. Strengthen the existing duplicate/missing-field cases to pin their existing messages alongside status/code. Do not mock the final producer result or HTTP envelope.

## Required gates

- Focused development pytest: `tests/test_exercise_manager.py`, `tests/test_plan_generator_refactor_contracts.py`, `tests/test_workout_plan_routes.py`.
- Final: full `/verify-and-polish`, comprising full pytest, complete Chromium corpus using T1’s seed partitions, staged-diff `code-reviewer`, then `unslop-reviewer`.
- Include `tests/test_app_factory.py` registration coverage; no blueprint entry changes are needed.
- For the Python diff, run repo-wide Pyright and `scripts/pyright_baseline_diff.py` against the existing baseline. Native Type Check also requires `tsc --noEmit`.
- Regenerate both inventory artifacts using `scripts/generate_test_inventory.py` after adding cases, then verify `--check`. Never hand-edit them.
- No CSS build, backup/restore manual gate or snapshot regeneration is derived from the proposed paths.

## Existing coverage

- `utils/exercise_manager.py`: `tests/test_exercise_manager.py:79–308` covers real success, duplicate prevention, missing fields, optional effort values and ordering. `tests/test_weekly_summary.py:13–49` exercises its successful public wrapper.
- `utils/plan_generator.py`: `tests/test_plan_generator_refactor_contracts.py:114–169` pins row continuation and outer persistence failure propagation. Its `:172–190` test directly exercises `_add_persistence_result()`, currently requiring the leaked `"write failed"` text.
- `tests/test_plan_generator.py:511–592` covers generated data and successful real persistence. Its `persist=False` cases execute that branch but do not explicitly assert absence of failure metadata.
- `tests/test_phase3_features.py` exercises generator/API options; `tests/test_superset.py:243–313` exercises successful persistence with overwrite behavior. Neither proves unexpected-error redaction or exception-log retention.
- `tests/test_pattern_coverage.py:346–367` exercises non-persisting generation. Its “full workflow” case at `:384–403` constructs configuration only.
- `tests/test_utils_package.py` names the modules inside an isolation script to assert they are **not imported**. That is boundary coverage, not coverage of either producer.
- `e2e/api-integration.spec.ts:132–143` and `:222–246` cover ordinary add/generator outcomes. `e2e/error-handling.spec.ts:66–88` fulfills a mocked 500 response and does not reach the backend producer.
- `tests/test_priority0_api_contract.py:117–137` injects no DB failure and permits either 400 or 500. Its name does not establish internal-failure coverage.

The full gate includes the mapped API/error specs: `api-integration`, `validation-boundary`, `error-handling`, `empty-states` and `accessibility`, plus the remaining corpus.

## Coverage gaps and implementation requirements

- Inject an unexpected DB fault inside the real `ExerciseManager.add_exercise()` boundary. Assert exact generic producer text and real HTTP 500/`INTERNAL_ERROR`, including both message fields and the existing envelope.
- Exercise the real `_add_persistence_result()` catch through a failing persistence dependency, then through the real generator route. Assert HTTP 200, successful outer envelope, preserved generated data, `persisted is False`, exact string `persist_error`, and no sentinel anywhere in serialized client data.
- For generator fault injection, fail the outer persistence boundary. An individual row insert failure is caught and continued at `utils/plan_generator.py:1471–1477`; it will not exercise the changed catch.
- Capture the producer’s actual exception record. Both modules use the shared `hypertrophy_toolbox` logger; its handlers format exception information (`utils/logger.py:36–69`). A temporary capture handler attached directly to the producer logger avoids depending on root propagation. Assert nonempty `exc_info` and the sentinel in the exception/formatted record. `record.getMessage()` alone omits the traceback detail for a constant `logger.exception()` message.
- T2 supplies the missing useful-validation preservation case. Existing success, duplicate, row-continuation and successful-persistence regressions remain required.

The documented `program-backup` sequential DB-pollution flake remains relevant to the full corpus; record any occurrence and its isolated result. Do not infer a fixed visual red count from historical documentation.

## Conftest / fixture work

None. Reuse the isolated `app`/`client`/DB fixtures. No new blueprint, table, initializer or `clean_db` deletion entry is proposed.

## Verdict

**Full `/verify-suite` required.** Plan v1 needs T1–T2 incorporated before Gate 1. This completed review supplies test-strategy evidence; it grants no implementation or owner approval.
```

### product-risk-reviewer (agent `/root/api_plan_product_risk`)

```markdown
No findings; no P-series IDs assigned.

Plan v1 preserves the exact owner-approved messages and useful validation feedback (`PLANNING.md:25–29, 71–81`). Source inspection confirms the changes can remain confined to the two exception producers without changing exercise inputs, generated prescriptions, persistence algorithms or calculations.

The plan preserves generated data and persistence outcomes, including disabled persistence and row-failure continuation (`PLANNING.md:78–81`). It explicitly requires response-text migration notes, updated failure coverage and narrow product documentation (`PLANNING.md:89–95, 104–106`).

Local-first invariants, backup behavior and parked workstreams remain untouched. Gate 1 and implementation remain unapproved.

Review was read-only; no tests, application imports, database access or file changes occurred.

**Plan respects product invariants**
```

## Response matrix

The manager supplied these proposed dispositions for owner confirmation at Gate 1. Both findings are accepted into Plan v2. No finding is rejected or deferred. Architecture and product-risk reviewers reported no findings within their stated Plan-v1/source coverage; no additional findings or broader implementation passes are inferred from those verdicts.

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| T1 — Separate functional and visual-seed verification runs | `/root/api_plan_test_strategy` | accept | Run full pytest first, then both disjoint Chromium partitions with fresh separate DB/report paths, no reused server, one worker, zero retries and retained first-attempt evidence. Keep existing baselines. |
| T2 — Explicit HTTP preservation of useful validation text | `/root/api_plan_test_strategy` | accept | Add a real malformed-`priority_muscles` request asserting exact useful text in both message fields, and strengthen existing duplicate/missing-field message assertions. |

## Plan v2

**Goal:** Keep unexpected add-exercise and generated-plan persistence details in server logs while returning the exact owner-approved generic messages with existing status, field and validation contracts.

**Scope**

- **In:** only the two unexpected-error producers, their producer-local exception logging, meaningful unit/HTTP failure and validation preservation coverage, generated inventory and narrow Plan workflow documentation.
- **Out:** all Section 0 exclusions. No production route/shared-helper edit is planned; no schema, transaction, calculation, blueprint, frontend/CSS, baseline, runtime-startup or configuration change is selected.
- The two generic messages remain exactly `Failed to add exercise` and `Failed to save generated plan`. HTTP 500 / `INTERNAL_ERROR` for the former and HTTP 200 with `persisted: false` plus string `persist_error` for the latter remain unchanged requirements.

**Artifacts**

| Path | Change | Reviewed requirement |
|---|---|---|
| `utils/exercise_manager.py` | Modify only the unexpected DB-failure return | Retain the existing active-exception log; use `Failed to add exercise`. Keep validation, duplicate, success, order and normalization behavior. |
| `utils/plan_generator.py` | Modify only `_add_persistence_result()`'s unexpected-failure catch | Add `logger.exception()` using the existing module logger and set generic `persist_error`. Preserve success, disabled persistence, generated data, row continuation and transaction semantics. |
| `tests/test_exercise_manager.py` | Add meaningful producer fault coverage | Exercise the real catch; assert exact generic result and retained exception record. Keep all positive/validation/order cases. |
| `tests/test_plan_generator_refactor_contracts.py` | Update public-text expectation; strengthen producer outcome/log coverage | Preserve the exact failure shape, assert generic text and no sentinel, and prove exception detail is logged. Keep outer failure propagation and row-continuation contracts. |
| `tests/test_workout_plan_routes.py` | Add real HTTP failure and validation preservation assertions | Real changed producer paths; exact statuses/envelopes/messages. Incorporate T2 and strengthen existing duplicate/missing-field text checks. |
| `tests/test_plan_generator.py` | Strengthen existing disabled-persistence assertion if its fixture is the appropriate existing location | Explicitly retain `persisted: false` with no failure metadata when persistence was not requested; do not change selection or prescriptions. |
| `docs/product/APP_FLOW.md` | Modify narrowly | Describe the two generic failure messages and unchanged user-visible response outcomes. |
| `docs/test_inventory/TEST_INVENTORY.json`, `docs/test_inventory/TEST_INVENTORY.md` | Regenerate | Use `scripts/generate_test_inventory.py` after added cases, then run `--check`; no hand-edited counts. |
| `docs/codeql_exception_responses/PLANNING.md` | Council audit record | Preserve Plan v1, verbatim reviews, both proposed dispositions and Plan v2/provenance. |
| PR description | Author | Include intentional response-text migration, before/after examples, preserved contracts and exact-head/native validation evidence. |

**Coverage requirements**

1. **Add-exercise fault:** inject an unexpected failure at the real `ExerciseManager.add_exercise()` DB boundary, not by returning a prebuilt generic result from the route alias. Check the producer result, real HTTP 500, `INTERNAL_ERROR`, both client message fields and the existing envelope. The internal sentinel must be absent from the serialized response.
2. **Generator fault:** exercise the actual `_add_persistence_result()` catch using a failing outer persistence dependency, then exercise it through the real generator route with otherwise valid input/catalog fixtures. Fail `generator.persist()` or its outer persistence boundary after generation can proceed. An individual insert failure is caught and continued elsewhere (`utils/plan_generator.py:1471–1477`) and cannot stand in for this catch. Check HTTP 200, the successful outer envelope, unchanged generated data, `persisted is False`, the exact string `persist_error` and absence of the sentinel anywhere in serialized client data. Do not replace the final producer result or HTTP envelope with the expected answer.
3. **Actual log evidence:** attach a temporary capture handler directly to the producer's shared `hypertrophy_toolbox` logger and remove it after the test. Assert a captured record with nonempty `exc_info` and the synthetic sentinel in the exception or formatted record. A method-call assertion or `record.getMessage()` alone is insufficient for a constant exception-log message. Production logging configuration remains unchanged.
4. **Useful validation (T2):** submit a real `POST /generate_starter_plan` request using otherwise valid parameters and `priority_muscles: "chest"`. Assert HTTP 400, `VALIDATION_ERROR`, and exactly `priority_muscles must be a list` in both client message fields. `GeneratorConfig.__post_init__()` must produce the expected `ValueError`; do not mock that exception's final response. Strengthen existing add-exercise duplicate/missing-field cases to assert their existing exact useful text alongside status and code, without changing those producers' wording.
5. **Unchanged branches:** retain existing real success, duplicate, numeric-bound, optional-field, exercise-order, successful-persistence and row-continuation tests. Explicitly check disabled persistence has no newly introduced failure metadata. `tests/test_utils_package.py` remains import-boundary coverage; neither its module-name strings nor mocked browser 500s prove producer redaction.

**Required verification**

- Focused development pytest: `tests/test_exercise_manager.py`, `tests/test_plan_generator_refactor_contracts.py`, `tests/test_workout_plan_routes.py`, and existing producer-related regression files identified in Plan v1 as appropriate. Include `tests/test_app_factory.py` registration coverage; no registration entry changes are selected.
- Final `/verify-and-polish`: full pytest, then the complete Chromium corpus through the two sequential seed partitions below, then staged-diff `code-reviewer`, then `unslop-reviewer`. No test run occurred during this planning council.
- Python diagnostics: repo-wide Pyright and `scripts/pyright_baseline_diff.py` against the unchanged existing baseline. Native Type Check also requires `tsc --noEmit`.
- Inventory: regenerate both artifacts with `scripts/generate_test_inventory.py` after adding cases, then verify `--check`.
- No CSS build, manual backup/restore gate or screenshot regeneration is derived from the selected paths. Existing native checks remain required; none is weakened or newly waived.

**Complete Chromium partition (T1)**

After full pytest passes, enumerate and retain the full current Chromium spec manifest. Partition it into the following disjoint sets; retain evidence that their union covers that manifest without introducing exclusions:

| Sequential run | Spec selection | Seed and isolation |
|---|---|---|
| Functional corpus | Every spec except the three named in the next row | `PW_VISUAL_SEED` unset or `0`; fresh functional throwaway DB, runtime and report paths; no reused server; one worker; zero retries. |
| Visual-seed corpus | Exactly `e2e/visual.spec.ts`, `e2e/visual-baseline-thumbnails.spec.ts`, `e2e/workout-plan-desktop-contract.spec.ts` | `PW_VISUAL_SEED=1`; a separate fresh visual throwaway DB, runtime and report paths; stop the preceding server and use no reused server; one worker; zero retries. |

This preserves complete `/verify-suite` Chromium coverage while respecting `playwright.config.ts`'s distinct preparation scripts and `e2e/CLAUDE.md`'s seed contract; it is not a test exemption. The full corpus includes `api-integration`, `validation-boundary`, `error-handling`, `empty-states`, `accessibility` and all remaining specs. Keep first-attempt results, browser/runtime/seed identities and existing platform baseline comparisons. Do not regenerate baselines or accept a recovered retry as a clean pass. Record any `program-backup` sequential DB-pollution occurrence and its isolated result; do not infer a current fixed visual-red count from historical records.

**Sequence**

1. Present this Plan v2, the proposed T1/T2 response matrix and complete provenance for direct owner Gate 1 approval. No API implementation proceeds before that approval.
2. Refresh the affected sources and duplicate issue/PR state. Use the selected implementation lane's isolated runtime and test fixtures; retain all branch/worktree/recovery holds.
3. Add/strengthen the real producer, HTTP, useful-validation and log-record tests above. Make only the two producer changes and local persistence exception log. Preserve the existing surrounding algorithms, routes and shared response helpers.
4. Update the narrow product documentation and PR migration notes. Regenerate inventory, run focused development checks and diagnostics, then run the complete final verification gate with T1's seed partitions and both independent diff reviewers. Address findings without weakening contracts, baselines or checks.
5. Prepare one bounded remediation PR linked to native alerts #2/#3 and #588 after duplicate checking. Keep alert dispositions on the code-scanning pages and record exact source/check evidence for owner review.
6. Obtain separate direct approval of that PR's exact head before merge. After merge, inspect CI and CodeQL at the actual main merge SHA and every remaining #2/#3 origin. Declare an alert fixed only from native state readback.
7. If #2 remains only for useful expected-validation paths, retain it for a separately reviewed and owner-approved disposition. No automatic dismissal or blanket validation redaction is authorized by this plan.

**Effort and risk**

Implementation remains M, with a full final verification gate. Section 0's calculation surface remains `none`; its exact messages, statuses, fields and non-goals are unchanged. T1 controls seed-induced false failures while retaining every spec; T2 directly proves preservation of useful expected validation. Existing risks and controls in Plan v1 remain applicable, with the real producer/log assertions above replacing reliance on incidental import coverage or mocked final responses. No council finding is deferred, so no deferred-finding handover entry is needed.

## Sign-off

- [x] Gate 0 complete for the approved requirements and council preparation.
- [x] Every finding has a manager-proposed disposition for owner confirmation at Gate 1: accept T1 and T2; no findings rejected or deferred.
- [x] Agent provenance complete — both PM IDs, same-PM-resumed status, all three reviewer IDs and evidence-gap line.
- [x] Owner approved Plan v2 (Gate 1).
- [x] Ready to implement — authority granted; follow the sequencing recorded below.

## See also

- [Quality Gate](../ai_workflow/QUALITY_GATE.md) — planning and implementation authority.
- [Council procedure](../../.claude/commands/council-plan.md) and [template](../ai_workflow/PLAN_REVIEW_TEMPLATE.md).
- [Plan workflow](../product/APP_FLOW.md) and [implementation conventions](../../CLAUDE.md).

## Test-strategist confirmation of Plan v2

The manager supplied this confirmation from the same recorded reviewer, `/root/api_plan_test_strategy`, after review of the genuinely revised Plan v2. The same PM, `/root/api_plan_pm`, appended it without changing Plan v1, the original reviews, response matrix or Plan v2. No new agent ID or council pass is asserted. Gate 1 remains unchecked.

```markdown
- **T1 — Addressed.** Plan v2 `:299–308` specifies both complete-corpus seed partitions, fresh separate DB/runtime/report paths, no server reuse, one worker, zero retries, retained first-attempt evidence and unchanged baselines.
- **T2 — Addressed.** Plan v2 `:288` requires the real malformed-`priority_muscles` request, exact useful text in both message fields, HTTP 400/`VALIDATION_ERROR`, and strengthened duplicate/missing-field assertions.
- **Producer/log/HTTP requirements — Addressed.** Plan v2 `:285–289` requires real producer catches and HTTP serialization, correct fault boundaries, sentinel omission, preserved envelopes/data, actual exception-record capture with `exc_info`, handler cleanup and unchanged branch regressions.

**Residual blocking omissions: none within this bounded confirmation.** Gate 1 remains pending. Verification was read-only; no tests or runtime activity occurred.
```

## Direct owner Gate 1 approval — 2026-10-24

The owner directly approved the reviewed Plan v2 and API fix PR preparation in `call_a2383218760b4f12b668506de9e04f88`:

> Approve Plan v2 and prepare the API fix PR

The manager recorded the direct reply at `2026-10-24T20:49:21.416162+00:00` in `artifacts/codeql_remaining_20261024/API_GATE1_APPROVAL.json`. That receipt records `gate1_approved: true`, `implementation_and_PR_preparation_authorized: true` and `merge_authorized: false`.

**Approved pre-signoff document SHA-256:** `a74b7700b72bcd964d55e5a6330b8e217881aded459e1fb8f678e3f5e43db4d7`. The PM read the direct-approval receipt and verified that the canonical planning document matched this exact hash before adding the current status and sign-off record.

The same PM, `/root/api_plan_pm`, recorded this approval. Plan v1, all verbatim reviews, the response matrix, Plan v2, agent-handle provenance and the strategist's confirmation remain unchanged. Their earlier pending-Gate-1 statements are preserved as the historical review state; this direct owner approval is the current authority. No new council or reviewer pass was run.

**Sequencing:** the root agent will complete the filename branch's frozen verification/publication sequence first, then implement this approved API plan and prepare its fix PR. This sequencing changes no requirement, message, response contract, test obligation or implementation scope. The later API PR still requires its own direct exact-head merge approval.

## Post-signoff operational sequencing update

This manager update supersedes only the earlier filename-first ordering, including its current-status shorthand above. It preserves the approved pre-signoff hash, Gate 1 authority, all Plan v1/v2 requirements, verbatim reviews, response matrix, provenance and confirmation. The same PM, `/root/api_plan_pm`, records the update; no new council pass is asserted.

The root reports that frozen filename verification completed with Python **6,157 passed / 2 skipped** and Chromium **689 passed / 2 failed out of 691**. The failures were a functional routine-initialization timeout at `validation-boundary:342` and a visual workout-log desktop-light missing-styling symptom. The exact functional case passed once with a fresh DB, tracing and zero retries; the full run remains failed, with causes and inheritance unproven. Filename source postimages remain unchanged, and no filename commit or publication has occurred. The requested narrow filename-only verification exception remains pending; permission must not be inferred from the isolated result or this document.

To continue independently authorized API work while that filename permission is pending, the root may use this sequence:

1. Retain the exact two-line filename patch, its full source postimages, verification evidence and hashes. Verify the affected preimages/postimages before changing branches.
2. Reverse only the root's own verified two-line filename patch. Do not stash, reset, delete or disturb other retained work.
3. Create a separate API branch in the same retained manager checkout from main `302ef0e9fcbdf21f4ffd6d52dcf09770a8892252`. Run fresh API preflight, then implement and test the directly approved Plan v2 with its required isolated runtime/DB paths and full gates.
4. Later return to the filename branch and reapply the exact retained filename patch, verifying its postimage hashes, for its separately gated reviews and publication.

This is a permitted alternative orchestration, not a claim that a handoff or branch change has already occurred. The root remains the sole source, branch, test and GitHub writer. No filename partial-success commit is authorized without the direct owner exception. No API test/review waiver, new checkout, DB sharing, cleanup, merge or settings authority is granted. Approved API requirements, messages, response contracts, implementation scope and verification obligations remain unchanged; any eventual PR merge still needs separate direct exact-head approval.
