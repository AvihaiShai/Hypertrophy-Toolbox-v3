# Plan Review — WS4 Focused service extraction, slice 1 (`POST /remove_exercise`)

| Field | Value |
|---|---|
| Status | **Section 0 drafted 2026-10-19. Awaiting owner Gate 0.** No Plan v1, council, Gate 1, implementation or approval exists. |
| Author | `product-manager` agent (Claude Code), 2026-10-19, under the owner authorization relayed by the manager (quoted below): requirements only, stop at Gate 0. The manager supplied no agent ID. No council write happened, so there is no Agent provenance block yet. |
| Source of truth | This file holds WS4 slice-1 requirements. Direction and approval status stay in `docs/project_direction/AGREED_PLAN.md` §2 A7, §4 WS4, §5 Q8, §6, §10 F2 and §11. Both are untracked local files. |
| Baseline measured | `origin/main` `e486e3b5362a4c5346e946f91a66d45c9c19c73b`. See the evidence note below for how it was read. Nothing was imported, run or written except this file. |
| Planning size | **Medium.** `docs/ai_workflow/QUALITY_GATE.md` plan-stage routing lists "extract a bounded helper while preserving its interface" as a Medium example. Medium requires Gate 1. Gate 0 is the optional Medium gate, added here because the owner must make the decisions listed below. |
| Tracking | Untracked local file, like `docs/app_factory/PLANNING.md` and `AGREED_PLAN.md` (Q9). This session did not commit it. |

**Evidence note: how the baseline was read.** This agent has no shell, so it could not run `git show origin/main:<path>` or `git grep` itself. Every source fact below comes from `artifacts/project_direction_batch_20261019/ws1b/tree/`. Its `NOTES.md` §1 and §6 describe that tree as `git archive e486e3b5` with a scratch repository at `read-tree e486e3b5`. The tree's only overlay is `docs/MASTER_HANDOVER.md` plus one new archive file, and no source or test file is overlaid. Every figure taken from `ws4_design_report.md` was re-read in that tree before it was used here. This agent did **not** hash-check the extraction against `e486e3b5`. **Evidence gap:** before Gate 1, the manager or owner should confirm that `git -C artifacts/project_direction_batch_20261019/ws1b/tree status --short` lists only the two overlay paths. The shared working tree was not used as a baseline because it is 70 commits behind.

---

## Section 0 — Requirements Brief

**Raw request.** This is the verbatim task message. It reached this agent through the manager as a relayed owner authorization dated 2026-10-19 in chat. The owner should confirm that it matches what they said.

> Owner authorization (2026-10-19, in chat): write the Gate 0 Section 0 brief for WS4 "Focused service extraction" of docs/project_direction/AGREED_PLAN.md. Requirements only — no Plan v1, no council, no implementation. Stop at Gate 0.
>
> Use the requirements skill. Write Section 0 ONLY to a NEW untracked file D:\development\Hypertrophy-Toolbox-v3-main\docs\service_extraction\PLANNING.md (create it; confirm it doesn't already exist first). Model structure and rigor on the existing untracked WS3 brief docs/app_factory/PLANNING.md (read it). Do not edit any other file — not AGREED_PLAN, not tracked files.
>
> Inputs: AGREED_PLAN.md §4 WS4, §5/§11 Q8(a), appendix F2 (untracked local file); the WS3 brief; and the read-only design analysis at D:\development\Hypertrophy-Toolbox-v3-main\artifacts\project_direction_batch_20261019\ws4_design_report.md (baseline origin/main e486e3b5). Verify any fact you rely on against origin/main with `git show origin/main:<path>` / `git grep ... origin/main` — the shared working tree is 70 commits behind and must not be used as the code baseline. Do not modify, stage, commit, checkout, stash, reset or pull anything.
>
> Scope of the first slice: extract POST /remove_exercise into utils/workout_plan_service.py per the report, preserving transaction scope (per-statement autocommit, not atomic), ordering, envelopes and logging; characterization tests first. Record as blocking owner questions at minimum: Q8(a) sequencing after WS3 (priority vs prerequisite); explicit authorization to modify routes/workout_plan.py (recorded off-limits at OPEN_WORK_EXECUTION_PLAN.md:853-861); pin-or-not the partial-commit characterization; raw vs normalized return values; the user_profile contradiction (REFACTOR_PLAN.md:859); correction of AGREED_PLAN §3.4 figures; landing after Q-WS3-2 (logging convention). Record calculation-surface obligations (none touched; excluded handlers listed) and the gate routing (Medium -> Gate 1). Final reply: path written, the open questions list, and a one-line status.

**Problem**

The project rule says routes validate input, call `utils/`, and return a response (`CLAUDE.md` §2 module boundaries; AGREED_PLAN §4 WS4 goal). `routes/workout_plan.py` breaks that rule for several handlers, which run SQL inside the route. `POST /remove_exercise` is the only handler there whose single database context is split between the route and `utils/`. Its partner-unlink statement already lives in `utils/supersets.py` (WP1.4) and runs on the route's handler, while the lookup and both deletes are still inline SQL in the route. As a result, the handler's database behaviour has no single owner that can be tested without HTTP. The non-atomic, per-statement commit behaviour is real but not written down. Its contract is also only partly characterized (F5). The missing outcome is a removal operation owned by `utils/`, with byte-identical public behaviour, established without changing calculation logic, schema or API response shapes (`CLAUDE.md` §1 refactor invariant).

### Measured facts (baseline `e486e3b5`)

**F1 — What the handler does today (`routes/workout_plan.py:252-306`), in order.**

| Step | Behaviour | Source |
|---|---|---|
| 1 | `data = request.get_json()` runs inside `try`. | :254-256 |
| 2 | A falsy `data` returns `error_response("VALIDATION_ERROR", "No data provided", 400)`. | :257-258 |
| 3 | `logger.debug(f"Received data for remove_exercise: {data}")` runs **before** id validation. | :260 |
| 4 | `exercise_id = data.get("id")`. If it is falsy, or `str(exercise_id).isdigit()` is false, the handler returns `400 VALIDATION_ERROR "Invalid exercise ID"`. | :262-264 |
| 5 | One `with DatabaseHandler() as db_handler:` runs `SELECT routine, exercise, superset_group FROM user_selection WHERE id = ?` with `int(exercise_id)`. If no row comes back, it returns `404 NOT_FOUND f"Exercise with ID {exercise_id} not found"` from inside the context. The message uses the **raw** id. | :266-275 |
| 6 | A truthy `superset_group` triggers `superset_service.unlink_partner_for_removal(db_handler, exercise_id, group)`. That function receives the raw id, runs `UPDATE user_selection SET superset_group = NULL WHERE superset_group = ? AND id != ?` with `int(id)`, and logs INFO `"Unlinked partner exercise from superset due to removal"` with extras `superset_group` and the raw `removed_exercise_id`. | :279-282; `utils/supersets.py:226-248` |
| 7 | `DELETE FROM workout_log WHERE workout_plan_id = ?` runs before the selection delete. The schema has `ON DELETE CASCADE`, but the report keeps this order for legacy schemas. | :284-286 |
| 8 | `DELETE FROM user_selection WHERE id = ?`. | :288-290 |
| 9 | The context exits: `__exit__` commits (or rolls back on exception), then closes. | `utils/database.py:514-522` |
| 10 | After the context closes, the handler logs INFO `"Exercise removed from workout plan"` with extras `exercise_id` (raw), `routine` and `exercise`. Both have an `'unknown'` fallback that cannot trigger at this point. | :292-299 |
| 11 | `200 success_response(message="Exercise removed successfully")` returns keys `ok`, `status`, `message`, plus `requestId` only when request-id middleware is installed. It has **no `data` key**. | :300; `utils/errors.py:22-44` |
| 12 | Any `Exception` triggers `logger.exception("Error removing exercise", extra={'exercise_id': data.get("id", 'unknown') if data else 'unknown'})`, then `500 INTERNAL_ERROR "Unable to remove exercise"`. | :301-306 |

Every error envelope is `{"ok": false, "status": "error", "message", "error": {"code", "message", "requestId"}}`. `error_response` also logs `API error: <code> - <message>` with `request.endpoint` (`utils/errors.py:67-107`). The endpoint name is `workout_plan.remove_exercise`.

**F2 — Transaction scope is per statement, not atomic.** `execute_query` defaults to `commit=True` and commits after each statement (`utils/database.py:299,324-325`). On `sqlite3.Error` it rolls back only the failing statement and re-raises (:352-365). `_DB_LOCK` is acquired for each write statement and released in `finally` (:316-318,366-370), so the lock is **not** held across the handler's statements. `__exit__`'s final commit has nothing left to commit. Statements that already committed stay committed if a later statement fails. One existing test pins this for the partner-unlink: `tests/test_superset_service.py:88-111` shows a second connection seeing the NULL while still inside the caller's context. Two documents describe the shared handler as sharing "connection + write lock": `docs/REFACTOR_PLAN.md:824-828` and the docstring at `utils/supersets.py:231-235`. Read literally, that wording suggests a lock held for the whole operation, and the code does not do that.

**F3 — Edge behaviour derived by reading the code (⚠️ not executed; Flask 3.1.3 / Werkzeug 3.1.9 per `requirements.txt`).**

- `id` = `0`, `-1`, `"-1"`, `1.5`, `true` or missing returns 400 `"Invalid exercise ID"`.
- `id` = `"0"` returns **404** `"Exercise with ID 0 not found"`, while integer `0` returns 400.
- `id` = `"007"` resolves to row 7. If that row is missing, the 404 message says `"Exercise with ID 007 not found"`.
- Malformed JSON, or a non-JSON content type, makes `get_json()` raise `BadRequest`/`UnsupportedMediaType`. The generic `except` catches it and returns 500 `"Unable to remove exercise"`.
- A Unicode digit such as `"²"` passes `isdigit()`, then `int()` raises `ValueError`, which ends in a 500.
- A **truthy non-object JSON body** (`[1]`, `5`, `"x"`) raises `AttributeError` at `data.get`. The `except` block then calls `data.get` again and raises a second time, so the exception escapes the view. The outcome depends on the application: the `TESTING` twin app propagates it to the test client, while production goes through `register_error_handlers` / `register_fallback_handlers`. So the behaviour differs between the conftest twin and the real app.
- Falsy JSON (`{}`, `[]`, `0`, `""`, `null`) returns 400 `"No data provided"`.

**F4 — Consumers of the public contract.**

- Production JavaScript: `static/js/modules/exercises.js:25-36` calls `api.post("/remove_exercise", {id})` with `showErrorToast: false`. On success it toasts `result.message || "Exercise removed successfully!"`. On failure it toasts `` `Unable to remove exercise: ${error.message}` ``. Both messages are visible to the user.
- E2E: `api-integration.spec.ts` (2 references), `error-handling.spec.ts`, `exercise-interactions.spec.ts`, `superset-edge-cases.spec.ts`, plus `e2e/fixtures.ts`.
- pytest:
  - `tests/test_workout_plan_routes.py:279-356` checks status codes and `ok` only, not messages or keys.
  - `tests/test_superset.py:181-201`.
  - `tests/test_ui_flows.py:84,373,407`.
  - `tests/test_superset_service.py:63-137` covers partner-only nulling, the passed handler with autocommit, and the raw-id log.
- Vitest: `static/js/modules/__tests__/exercises.test.js`.

**F5 — Uncovered contract today.**

- The exact success keys and message, including the absence of `data`.
- The exact 404 and 400 messages and codes, the raw id in the 404 message, and the digit-string id path.
- The 500 path and its message, and the malformed-JSON 500.
- Statement order, the absence of writes on 404, and partial persistence when a later statement fails.
- The route's own log records (steps 3, 10, 12).

**F6 — Import surface that must survive.**

- `workout_plan_bp` is imported by `app.py:25,119`, `tests/conftest.py:10,266` and `tests/test_priority7_error_handling.py:33,53`. The last one is a third hand-built Flask app.
- `initialize_exercise_order` is imported by `tests/test_harness_isolation.py:5`, `tests/test_program_backup.py:25` and test_priority7. `column_exists` is imported by `tests/test_program_backup.py:25`.
- The module-level compatibility aliases at `routes/workout_plan.py:25-45` are checked by identity in `tests/test_superset_service.py:28-48`, `tests/test_replace_exercise.py:32` and onward, and `tests/test_schema_registry.py`.
- `tests/test_filter_values.py:3` imports the route module as an attribute holder.
- `tests/test_replace_exercise.py:14-15` and `tests/test_superset_service.py:13-14` contain import-in-either-order subprocess tests, a precedent for the new module.
- `tests/test_utils_package.py` requires `utils/__init__.py` to stay an empty facade.
- `utils/workout_plan_service.py` does not exist on the baseline.
- The name `remove_exercise` already exists elsewhere as `utils/exercise_manager.py:168,204` `remove_exercise_by_name`, a different operation.

**F7 — Records that constrain this slice.**

- (a) **Off-limits designation.** `docs/OPEN_WORK_EXECUTION_PLAN.md:853-863` says the #447 authorization for `routes/workout_plan.py` "is spent rather than repealed" and that "a future change to that file needs its own authorization". `docs/REFACTOR_PLAN.md:1623-1628` repeats it as "the file stays off-limits". The REFACTOR_PLAN wording scopes it "to this track" (Track P1); the OPEN_WORK sentence is unscoped.
- (b) **Contradiction.** AGREED_PLAN §4 WS4 says "`user_profile` and `progression_plan` follow the same method". `docs/REFACTOR_PLAN.md:859-860` says "`routes/user_profile.py` needs no extraction WP: its handlers are already thin; the file's size is mostly static view-model data."
- (c) **AGREED_PLAN §3.4 figures do not match the code.** §3.4 says "1,138 lines, 23 endpoints, 27 direct DB-handler calls, 10 inline SQL statements", measured on `7ac1af2d`. The file has not changed since #447 (`3532f86`), so these readings at `e486e3b5` also apply to `7ac1af2d`:
  - 1,138 lines ✓
  - **18** `@workout_plan_bp.route` decorators
  - **9** `with DatabaseHandler()` contexts (lines 175, 266, 313, 336, 405, 442, 471, 633, 1039)
  - **16** `db`/`db_handler` `.execute_query`/`.fetch_one`/`.fetch_all` call sites
  - at least 12 SQL-verb literal lines plus dynamically built statements, so the inline-SQL count depends on how literals are counted

  The report's "16 inline SQL literals (+3 PRAGMA)" was not reproduced by an identical method. Re-measure with a stated command before citing it. The `user_profile.py` and `progression_plan.py` figures in §3.4 were not re-measured.

**F8 — Sequencing records.**

- AGREED_PLAN §11 contains the 2026-10-19 delegated direction decision, which is not an owner gate signature: "Q8(a), WS4 — Handler selection and contract analysis may proceed now. Implementation follows WS3 and its own bounded scope and approvals, with the same isolation conditions. Operation A completion is not an additional dependency."
- §6 WS4 says "DRAFT — follows WS3".
- For WS5, §11 explicitly says "without making WS3 a technical prerequisite". WS4's row has no such sentence, so it leaves "follows" undefined.
- WS3 is stopped at Gate 0 (`docs/app_factory/PLANNING.md`), with Q-WS3-1…6 open.
- The design report finds that the service and its tests are semantically independent of WS3, and that the coupling is limited to these points:
  - test fixtures: the conftest twin becomes `create_app()`, after which `requestId` appears and the F3 non-object-body outcome changes;
  - module-level `get_logger()` versus Q-WS3-2;
  - shared doc files (`CLAUDE.md`, `routes/CLAUDE.md`, `utils/CLAUDE.md`).

**F9 — Gates the eventual diff will trip (`QUALITY_GATE.md` at baseline).**

| Gate | What it requires for this slice |
|---|---|
| Route/API row (`routes/workout_plan.py`) | Route pytest target `tests/test_workout_plan_routes.py` plus blueprint-registration coverage in `tests/conftest.py`. Reviewer: `code-reviewer`. `product-risk-reviewer` is required only if a response shape changes, which this slice forbids. |
| Business-logic row (new `utils/workout_plan_service.py`) | `tests/test_workout_plan_service.py`. Reviewer: `code-reviewer`. No calculation module is touched, so no `product-risk-reviewer`. |
| DB row | Not triggered unless `utils/database.py`, `db_initializer.py`, `program_backup.py` or `auto_backup.py` changes. |
| `Test Inventory Drift` | A new test file and new cases mean `docs/test_inventory/` must be regenerated. |
| Pyright baseline diff | Zero headroom: no net-new diagnostic. |
| Targeted-test derivation | Add the `rg "routes\.workout_plan\|workout_plan_bp\|/remove_exercise" tests` union from F4 and F6. |
| Closing gate | `CLAUDE.md` §4B says refactors finish with `/verify-and-polish`. |

**Acceptance criteria**

1. **Characterization first.** Given the unmodified baseline route, when the new characterization tests (criteria 2–7) are added, then they pass against the unmodified route before any route or service edit. They land in a commit, or a verified pre-edit run, that precedes the extraction. After the extraction they pass unchanged.
2. **Success contract.** Given an existing plan row with id N, when `POST /remove_exercise` is sent with `{"id": N}` or `{"id": "N"}`, then:
   - the response is 200;
   - the body keys excluding `requestId` are exactly `{ok, status, message}`, with `ok is True`, `status == "success"`, `message == "Exercise removed successfully"`, and no `data` key;
   - the row and its `workout_log` rows are gone.
3. **Validation contract.** Given the requests in F3, when they are posted:
   - `{}` returns 400 with `error.code == "VALIDATION_ERROR"` and message `"No data provided"`;
   - `{"id": "abc"}`, `0`, `"-1"`, `1.5` and `true` return 400 with `"VALIDATION_ERROR"` and `"Invalid exercise ID"`;
   - none of these performs a database write.
4. **Not-found contract.** Given no row with that id, when `{"id": 99999}` (and the owner-selected string form, for example `"007"`) is posted, then the response is 404 with `error.code == "NOT_FOUND"`, the message is `"Exercise with ID <raw id> not found"` using the id exactly as sent, and no UPDATE or DELETE runs.
5. **Failure contract.** Given an exception forced inside the database work, and separately a malformed-JSON body, when the request is posted, then each returns 500 with `error.code == "INTERNAL_ERROR"` and message `"Unable to remove exercise"`. The non-object-body case (F3) is characterized only as Q-WS4-8 decides.
6. **Statement scope and order.** Given a supersetted row and a recording wrapper around `DatabaseHandler.execute_query`/`fetch_one`, when the removal runs, then:
   - exactly one `DatabaseHandler` is opened;
   - the statements run in the order `SELECT routine, exercise, superset_group` → partner `UPDATE` (only when the group is truthy) → `DELETE FROM workout_log` → `DELETE FROM user_selection`;
   - every write uses the default `commit=True`;
   - no `BEGIN`, `commit=False`, `executemany` or new transaction wrapper appears;
   - the partner is nulled and the removed row's own group is not touched before deletion.
7. **Partial-commit behaviour.** Given a failure injected into the `DELETE FROM user_selection` statement after the `workout_log` delete succeeded, when the removal runs, then the response is 500, and the persisted state (logs deleted, partner unlinked, plan row still present) is either asserted by a characterization test or explicitly left unasserted and documented, as Q-WS4-3 decides. Either way, this slice changes nothing about it.
8. **Logging.** Given caplog on the `hypertrophy_toolbox` logger, when each path in criteria 2–5 runs, then the same records appear in the same order, with the same level, message text and `extra` keys and values:
   - the debug `Received data for remove_exercise: …`;
   - the supersets INFO, with the raw `removed_exercise_id`;
   - the route INFO `Exercise removed from workout plan`, with the raw `exercise_id`, `routine` and `exercise`;
   - `Error removing exercise` through `logger.exception`;
   - the `error_response` `API error: …` records, with endpoint `workout_plan.remove_exercise`.

   The new service emits no new log records. Q-WS4-7 decides whether it holds a module-level logger at all.
9. **Service boundary.** Given the new `utils/workout_plan_service.py`, when it is imported in a fresh interpreter in either order with `routes.workout_plan`, then:
   - the import succeeds;
   - it imports nothing from `routes`;
   - `utils/__init__.py` is unchanged and `tests/test_utils_package.py` passes;
   - the service returns nothing and writes nothing for a missing id;
   - for an existing id it returns the removed row's routine and exercise, in the form Q-WS4-4 selects;
   - `sqlite3` and other exceptions propagate to the caller unchanged.
10. **Route boundary.** Given the post-extraction route, when `routes/workout_plan.py` is inspected, then:
    - `remove_exercise` still owns `get_json`, the "No data provided" and "Invalid exercise ID" checks, envelope selection, the raw-id 404 message, its own `except Exception` and its two route log calls;
    - it contains no SQL;
    - the URL, method and endpoint name are unchanged;
    - every name listed in F6 still resolves to the same object;
    - the diff to that file is confined to the `remove_exercise` body plus one import line.
11. **Existing assertions untouched.** Given the F4 and F6 tests, when the suite runs, then all of them pass with their assertions unedited. Only import or monkeypatch setup may change, per AGREED_PLAN §4 WS4 "Per handler".
12. **Gates and migration notes.** Given the PR, when it is verified, then all of the following hold:
    - the targeted union (F9) and `/verify-and-polish` pass (full pytest + Chromium + `code-reviewer` + `unslop-reviewer`);
    - `docs/test_inventory/` is regenerated and `Test Inventory Drift` is green;
    - pyright reports no net-new diagnostic;
    - the PR description carries migration notes stating "no behaviour, schema, API-shape or calculation change; DB statements moved from route to `utils/workout_plan_service.py`", the preserved non-atomic scope, and the owner's authorization text for `routes/workout_plan.py`.
13. **Isolation.** Given AGREED_PLAN §11's Q8(a) boundaries, when implementation and validation run, then they run in a standalone clone with independent Git storage and private DB/runtime, backup, log, temp, cache and bytecode paths. There are no writes to the shared checkout and no worktree creation or removal, and any live recovery freeze is checked first.

**Calculation surface**

- **`none`.** No function in `utils/effective_sets.py`, `weekly_summary.py`, `session_summary.py`, `progression_plan.py`, `fatigue*` or `volume_progress.py` is touched, and no schema, catalog data or API response shape changes.
- **Excluded handlers.** These stay byte-identical in this slice:
  - `GET /api/volume_progress` (`routes/workout_plan.py:71-78`) is a calculation path through `get_volume_progress`;
  - `POST /generate_starter_plan` (:490-620) is a calculation path through `utils/plan_generator`;
  - `POST /add_exercise` (:80-166) and `POST /update_exercise` (:373-460) are adjacent to rep-range validation semantics (`validate_workout_bounds`, `accepts_in_isolation`, #394) and are deferred;
  - every other handler is out of slice-1 scope.
- **Migration notes and coverage are still committed** under the `CLAUDE.md` §1 refactor invariant, because `remove_exercise` belongs to the core *plan* workflow: see criteria 1–12.

**In scope**

- New `utils/workout_plan_service.py` holding the removal operation: lookup, conditional partner-unlink through the existing `superset_service.unlink_partner_for_removal`, then both deletes, all in one `DatabaseHandler` context with per-statement commits.
- `routes/workout_plan.py` `remove_exercise` delegating to that service. This is subject to Q-WS4-2.
- Characterization tests in `tests/test_workout_plan_routes.py`, written first, and a new `tests/test_workout_plan_service.py` covering service units, statement order, no `commit=False`, return values, the missing-id no-write case and the import-order subprocess test.
- Regenerated `docs/test_inventory/`, and the PR migration notes.

**Out of scope / non-goals**

- Making removal atomic, or any change to commit, rollback, lock or ordering behaviour. That would be a behaviour change needing separate approval.
- Changing messages, codes, status codes or envelope keys; adding validation; fixing any F3 edge case, including the double-raise on a non-object body.
- Any other handler, including the next candidates the report lists (`clear_workout_plan`, `set_execution_style`, `get_workout_plan`, `update_exercise_order` with its partial-commit decision, and the `add_exercise` typed result).
- `routes/user_profile.py`, `routes/progression_plan.py`, `utils/program_backup.py` (AGREED_PLAN §10 F2 candidates, DB-row gated, later).
- Blueprint split (A7), new blueprints and `app.py`.
- `tests/conftest.py`, `utils/database.py`, `utils/supersets.py` and `static/js/**`. The stale JS test line citations are left as they are. `templates/**`, E2E specs and workflows.
- Editing `AGREED_PLAN.md`, `OPEN_WORK_EXECUTION_PLAN.md` (under the docs-cleanup claim, Q8(b)), `REFACTOR_PLAN.md`, the `CLAUDE.md` files or the `.claude/**` files.
- WS3 work. Any recovery, worktree, release or shared-checkout action.

**Assumptions made**

- ⚠️ **A1:** The service shape follows the report: a function such as `remove_plan_exercise(exercise_id)` returning a `NamedTuple` `RemovedPlanExercise(routine, exercise)` or `None`. The route imports the module as an attribute (`from utils import workout_plan_service as plan_service`) so tests can patch `plan_service.<fn>`. Plan v1 may refine the names, but not the contract.
- ⚠️ **A2:** The route keeps all validation, including the `isdigit()` precondition. The service assumes a validated id and performs `int()` itself, so the Unicode-digit `ValueError` path (F3) still ends in a 500.
- ⚠️ **A3:** The service passes the **raw** id to `unlink_partner_for_removal`, as the route does today. This is pinned by `tests/test_superset_service.py:114-137`.
- ⚠️ **A4:** The log-delete-before-selection-delete order stays, even though `ON DELETE CASCADE` exists. Its legacy-schema rationale comes from the report, and this agent did not re-verify it against old-schema fixtures.
- ⚠️ **A5:** The new characterization tests run on today's conftest twin app. They assert keys and values excluding `requestId` rather than whole envelopes, so they survive WS3's `create_app()` change. No test imports `app`.
- ⚠️ **A6:** The F3 edge behaviours are derived from reading the code and were not executed. Criterion 1 is where they become measured facts.
- ⚠️ **A7:** "Per the report" adopts the report's handler choice and invariants (`ws4_design_report.md` §2) without a second independent handler-selection pass.

**Open questions for the owner**

Blocking means the question must be answered before the stage named.

- **Q-WS4-1: Q8(a) sequencing after WS3 (blocking for implementation, not for Plan v1 or Gate 1).** AGREED_PLAN §11 says WS4 implementation "follows WS3" but does not say how. Choose one:
  - (i) **prerequisite:** WS3 must merge before WS4 slice-1 implementation starts;
  - (ii) **priority only:** WS4 may implement once its own Gate 1 passes, with landing order coordinated with WS3, and the report finds no semantic dependency;
  - (iii) **design prerequisite:** WS3 Gate 1 must be approved, but not merged, before WS4 implements.

  Also confirm that the §11 delegated disposition stands as the owner's Q8(a) classification for WS4. This brief infers no hold release.
- **Q-WS4-2: Authorization to modify `routes/workout_plan.py` (blocking before Gate 1).** The file is recorded off-limits (`OPEN_WORK_EXECUTION_PLAN.md:853-863`; `REFACTOR_PLAN.md:1623-1628`), and the #447 authorization is spent. Suggested wording: *"Explicit owner authorization to modify `routes/workout_plan.py` solely to delegate `POST /remove_exercise` to `utils/workout_plan_service.py` under WS4 slice 1; it supersedes the off-limits designation only for that bounded packet."* Also decide whether the off-limits records are left as they are (recommended: they sit under the docs-cleanup claim, and WS4 cites the authorization in its PR) or updated in a separate coordinated docs change.
- **Q-WS4-3: Pin the partial-commit characterization or not (blocking before Plan v1).** Choose one:
  - (a) pin today's non-atomic outcome as a characterization test, labelled as current behaviour and not endorsed, like the FINDING-1 known-defect test pattern;
  - (b) document it in the PR and `utils/workout_plan_service.py` docstring only, with no test;
  - (c) neither, and make it atomic. Option (c) is out of scope here and needs its own approval.

  Pinning makes any later atomicity fix a visible test change. Not pinning leaves the behaviour unguarded.
- **Q-WS4-4: Raw or normalized return values (blocking before Plan v1).** Should the service return the row's `routine`/`exercise` verbatim (possibly `None`) and leave the route's log extras exactly as today? That is the report's recommendation. Or should it normalize them (stripped, `None` → `'unknown'`, canonical names)? Normalizing would change the route's INFO log extras. Also confirm that the raw id stays in the 404 message and in both log records.
- **Q-WS4-5: The `user_profile` contradiction (blocking for WS4's scope statement beyond slice 1; slice 1 does not touch it).** Choose between AGREED_PLAN §4 WS4 ("`user_profile` and `progression_plan` follow the same method") and `REFACTOR_PLAN.md:859-860` (handlers "already thin"). Options: drop `user_profile` from WS4; keep it pending a fresh per-handler measurement; or override REFACTOR_PLAN. Decide also whether `progression_plan` stays.
- **Q-WS4-6: Correcting AGREED_PLAN §3.4 (blocking before Gate 1 so the plan does not cite wrong figures).** Should the owner, or a delegated editor, correct §3.4's `routes/workout_plan.py` row to the F7(c) readings with a stated counting method, and re-measure the `user_profile.py` and `progression_plan.py` rows? This brief does not edit AGREED_PLAN.
- **Q-WS4-7: Landing after Q-WS3-2, the logging convention (blocking before implementation).** Choose one:
  - (a) WS4 slice 1 waits until Q-WS3-2 is answered, and the new module follows the chosen convention;
  - (b) WS4 proceeds with a service that emits no log records and has **no** module-level `get_logger()`, so it adds nothing to the 45-module logging side effect, which removes this coupling. Remaining logging stays in the route and `utils/supersets.py`, exactly as today.
- **Q-WS4-8: Edge cases to pin (needed before Plan v1).** Which F3 edges become characterization tests? The `"0"`→404 versus `0`→400 asymmetry, `"007"` in the 404 message, non-JSON content type → 500, Unicode digit → 500, and the non-object body. The non-object body's outcome differs between the twin and the production app, so pinning it on the twin would be overturned by WS3. The recommendation is to record it and not pin it.
- **Q-WS4-9: Planning route (needed before Plan v1, not blocking Gate 0).** Medium work requires Gate 1 plan approval but not a council. Choose a plain Plan v1 → Gate 1, or `/council-plan` with the three reviewers. The council adds optional agents, which needs your explicit choice (`CLAUDE.md` §3 "Reasoning effort is not agent authorization").

**Decision not needed now:** where this file lives and whether it is committed, which follows Q9 the same way the WS3 brief does.

### Section 0 sign-off — GATE 0

- [ ] Owner confirms that the relayed raw request matches what was said, and that acceptance criteria 1–13 match intent.
- [ ] Owner reviewed assumptions A1–A7 and corrected or accepted each one.
- [ ] Blocking questions answered at their stated stage:
  - Q-WS4-3, -4 and -8 before Plan v1;
  - Q-WS4-2 and -6 before Gate 1;
  - Q-WS4-1 and -7 before implementation;
  - Q-WS4-5 before WS4 grows past `routes/workout_plan.py`;
  - Q-WS4-9 before Plan v1.

---

*Plan v1, Agent provenance, Reviewer findings, Response matrix, Plan v2 and Sign-off are deliberately absent. This document stops at Gate 0, as the owner's "requirements only" instruction requires. They are drafted only after Gate 0 sign-off, following the planning route chosen in Q-WS4-9 and `docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`.*
