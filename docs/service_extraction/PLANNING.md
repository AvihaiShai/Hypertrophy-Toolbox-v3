# Plan Review — WS4 Focused service extraction, slice 1 (`POST /remove_exercise`)

| Field | Value |
|---|---|
| Status | **Gate 0 signed by the owner 2026-10-22** (record in the Section 0 sign-off block). **Gate 1 disposed 2026-10-22 as a DELEGATED Gate 1, not an owner signature (§P15).** Three independent advisers unanimously approved Plan v1, as bound at `3768e52` (SHA-256 `6e95835d…e328f9`), with no BLOCKING finding. No council (Q-WS4-9). Implementation C2–C4 is authorized within §P1, under Plan v1 as amended by GA-1…GA-14 (§P15). The push and the ready PR follow under the owner's lane-O2 instruction (§P14.4). A merge stays owner-only, approved by PR number and head SHA. |
| Authors | Rev 1 (Section 0): a `product-manager` agent, 2026-10-19; no agent ID was supplied. Revs 2–3 (Gate 0 record, rev 2 Section 0 delta, Plan v1): a fresh `product-manager` spawned on 2026-10-22 by the primary session of lane O2, ID `ae7ed7afd0994c6df` (see Agent provenance). |
| Source of truth | This file, for WS4 slice-1 requirements and plan. Direction: `docs/project_direction/AGREED_PLAN.md` §4 WS4, §6 (`:215`) and §11 (`:343`), tracked on `main` since #531. Advisory evidence: `artifacts/parallel-next-five/ws4/` in the clone (gitignored, never committed). The rev 2 delta restates every correction the owner accepted from it. |
| Governing baseline | `origin/main` `155181d67a89fe72e86c75a1ff438caec250a9bd` (#552). The decision packet measured the contract at `d98f45d3` (#545). On 2026-10-22 the primary session confirmed that #549, #551 and #552 change no path this slice reads or writes except `docs/test_inventory/**`. F1–F9 and the rev 1 evidence note below refer to `e486e3b5`. |
| Planning size | **Medium** (`docs/ai_workflow/QUALITY_GATE.md:13`: "extract a bounded helper while preserving its interface"). Gate 1 is required. The optional Medium Gate 0 was added and is now signed. No council (Q-WS4-9). |
| Tracking | Tracked on branch `ws4/remove-exercise-service` in the standalone clone `D:\development\Hypertrophy-Toolbox-v3-ws4-slice1-20261021`. Commit C0 `c5a1a43` holds the rev 1 brief byte-for-byte (SHA-256 `d5d0950d5596101b269077b823368f1121556cec9a99da16542e5a536bd9796b`, 32,699 B). Revs 2–3 land as C1, and the Gate 1 record later lands in its own commit. The shared checkout's untracked original, `D:\development\Hypertrophy-Toolbox-v3-main\docs\service_extraction\PLANNING.md`, stays untouched. **Once this PR merges, that untracked file will block a `git pull` in the shared checkout, so the owner should rename or remove it at that point.** |

### Revision history

| Rev | Date | Author (agent ID) | Change | Inputs |
|---|---|---|---|---|
| 1 | 2026-10-19 | `product-manager` (no ID supplied) | Section 0 drafted at `e486e3b5`; stopped at Gate 0. Committed byte-for-byte as C0 `c5a1a43`. | Owner request relayed 2026-10-19 (quoted in Section 0); `ws4_design_report.md`. |
| 2 | 2026-10-22 | `product-manager` `ae7ed7afd0994c6df` | Gate 0 recorded: owner text verbatim, sign-off boxes ticked, answers to Q-WS4-1…9 and dispositions for A1–A7. Rev 2 Section 0 delta added, carrying the decision packet's §2–§3 corrections into the committed record. The header table and the closing note were replaced; F1–F9, the acceptance criteria, A1–A7 and the questions are unchanged. | Owner decision of 2026-10-22, relayed verbatim by the primary O2 session; `artifacts/parallel-next-five/ws4/DECISION_PACKET.md` §2–§4 and `analyst/CONTRACT_ANALYSIS.md`; the primary session's re-verification at `155181d6`. Preimage: C0. |
| 3 | 2026-10-22 | Same agent as rev 2 | Plan v1 (§P1–§P14), Agent provenance and Sign-off added below Section 0. | Packet §4 *Plan v1 design*; `reviewer/ARCHITECTURE_REVIEW.md` findings 2–15; `designer/TEST_DESIGN.md` §3–§10; the 43-node draft; `designer/mutation/mutate.py` (the M01 reference shape). |
| 4 | 2026-10-22 | `product-manager` `ae7ed7afd0994c6df`, resumed by the primary session via `SendMessage` (same agent as revs 2–3) | Delegated Gate 1 record added as §P15. Also updated: the header Status row, this row, the Agent provenance adviser row and the Sign-off Gate 1 box. §P1–§P14 are unchanged. | The primary session's adopted disposition, relayed by message on 2026-10-22. The adviser reports and the lane prompt are under `artifacts/o2/gate1/`. This agent confirmed the four §P15 quotes and line numbers against the preserved lane prompt, but did not read the adviser reports. Preimage: commit `3768e52`, which is rev 3 including the primary session's three corrections made before hashing. |

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

- [x] Owner confirms that the relayed raw request matches what was said, and that acceptance criteria 1–13 match intent. **Accepted 2026-10-22, as corrected by the rev 2 delta below (decision packet §2–§3).**
- [x] Owner reviewed assumptions A1–A7 and corrected or accepted each one. **A1–A4 and A7 accepted; A5 and A6 corrected (table below).**
- [x] Blocking questions answered at their stated stage:
  - Q-WS4-3, -4 and -8 before Plan v1; **answered.**
  - Q-WS4-2 and -6 before Gate 1; **Q-WS4-2 answered by the authorization sentence; Q-WS4-6 deferred, not blocking slice 1.**
  - Q-WS4-1 and -7 before implementation; **Q-WS4-1 satisfied (WS3 merged as #545, `d98f45d3`); Q-WS4-7 answered.**
  - Q-WS4-5 before WS4 grows past `routes/workout_plan.py`; **deferred, not blocking slice 1.**
  - Q-WS4-9 before Plan v1. **Answered: plain Plan v1 → Gate 1, no council.**

**Gate 0 record.** The owner's decision, verbatim, 2026-10-22. The owner gave it directly in the session prompt for lane O2 (Opus) of the 2026-10-22 six-lane batch, and the primary O2 session relayed it to this agent verbatim. The Gate 0 signature is the owner's own. Gate 1 is delegated by the second paragraph and is not recorded here.

> Owner decision, WS4 slice 1 (2026-10-22): I accept Section 0 of docs/service_extraction/PLANNING.md as corrected by artifacts/parallel-next-five/ws4/DECISION_PACKET.md §2–§3 (Gate 0). Answers: Q-WS4-1 satisfied (WS3 merged); Q-WS4-3 (a) pin as current behaviour, not endorsed; Q-WS4-4 raw; Q-WS4-7 answered by Q-WS3-2(a), service emits no logs; Q-WS4-8 pin per packet D4; Q-WS4-9 plain Plan v1 → Gate 1, no council; Q-WS4-6 and Q-WS4-5 deferred, not blocking slice 1. This is explicit owner authorization to modify routes/workout_plan.py solely to delegate POST /remove_exercise to the new utils/workout_plan_service.py under WS4 slice 1, confined to the remove_exercise body and one import line. It supersedes the off-limits designation (REFACTOR_PLAN.md:1623-1628) only for that bounded packet; the records stay unedited.
>
> Gate 1 for this slice is delegated to the AI consulting team. Three independent advisers review the written Plan v1, bound by its SHA-256. If they approve unanimously or by reasoned majority, with no unresolved BLOCKING finding, that is recorded as a DELEGATED Gate 1, not my signature. A BLOCKING finding is fixed and re-reviewed; if it still blocks, stop and ask me.

**Answers as they apply to this slice**

| Question | Owner answer | Applied in |
|---|---|---|
| Q-WS4-1 | Satisfied: WS3 is merged (#545, `d98f45d3`). | — |
| Q-WS4-2 | The authorization sentence above. The off-limits records stay unedited. | §P1, §P3, §P9 |
| Q-WS4-3 | (a): pin the partial-commit outcome as current behaviour, not endorsed. | §P5.1 item 6 |
| Q-WS4-4 | Raw. The service returns the values verbatim, and the raw id stays in the 404 message, in both route log records and in the supersets call. ACs 4 and 8 already require the raw id. | §P2, §P3 |
| Q-WS4-5 | Deferred; not blocking slice 1. | §P11 |
| Q-WS4-6 | Deferred; not blocking slice 1. Plan v1 cites no AGREED_PLAN §3.4 figure. | §P11, follow-up 7 |
| Q-WS4-7 | Answered by Q-WS3-2(a) (`docs/app_factory/PLANNING.md:474`). The service emits no logs. | §P2 |
| Q-WS4-8 | Pin per packet D4, restated below. | §P5.1 item 7 |
| Q-WS4-9 | Plain Plan v1 → Gate 1, no council. Gate 1 is delegated to three advisers. | §P14 |

**Packet D4**, the content of the Q-WS4-8 answer, verbatim from the packet's recommendation: "**Pin:** `"0"`→404 vs `0`→400; `"007"`/`"00N"`; malformed JSON, `text/plain`, form-encoded and no-body → 500; `"²"` → 500 (handler count *not* pinned); non-object body → 500 `text/html` with no route "Error removing exercise" record. **Do not pin:** the exact `errors.py` HTML/XHR copy, or `"٣"` → 200."

**Assumptions.** The owner accepted Section 0 as corrected by packet §2–§3. The dispositions below apply that sentence and add nothing to it.

| | Disposition | Note |
|---|---|---|
| A1 | Accepted | §P2 fixes the names A1 proposed: `remove_plan_exercise`, `RemovedPlanExercise`, and the route's module alias `plan_service`. |
| A2 | Accepted | `int()` runs inside the service's `with`, so `"²"` opens and closes one handler before the `ValueError`, as on base. |
| A3 | Accepted | Also pinned at route level (§P5.1 item 1) and at unit level (§P5.2 item 6). |
| A4 | Accepted, refined | `_initialize_workout_log_table` forces `ON DELETE CASCADE` on every initialized database (`utils/db_initializer.py:230-251`), so the explicit `workout_log` DELETE is functionally redundant there. It is still observable: it is a separately committed statement, and it decides the partial-commit state. The order stays. |
| A5 | Corrected: obsolete | Δ2 below. |
| A6 | Corrected: discharged | Δ3–Δ6 below. |
| A7 | Accepted | Unchanged. |

### Rev 2 Section 0 delta (2026-10-22)

The owner accepted Section 0 *as corrected by* decision packet §2–§3. The packet sits under the gitignored `artifacts/` and will not be committed, so this delta carries those corrections into the committed record. Section 0 above stays as written: F1–F9, the acceptance criteria, A1–A7 and the questions are verbatim. Where they disagree with this delta, the delta governs.

**Re-verification at `155181d6` (primary session, 2026-10-22).** `origin/main` is `155181d6` (#552). The three commits after the packet's `d98f45d3` (#549, #551, #552) touch none of the following: `routes/`, `utils/`, `tests/conftest.py`, the remove-related tests, `static/js/modules/exercises.js`, `docs/ai_workflow/QUALITY_GATE.md`, the requirements files and the package manifests. They do change `docs/test_inventory/**`, so the inventory figures in TEST_DESIGN §9 are stale and are not used here. Baselines re-run in the clone with the private environment:
- `tests/test_workout_plan_routes.py` + `tests/test_superset.py` + `tests/test_superset_service.py`: **108 passed**;
- the 43-node draft, run via `-p tests.conftest`: **43 passed**.

| Δ | Superseded statement in Section 0 | Correction | Evidence |
|---|---|---|---|
| Δ1 | The rev 1 header's "Baseline measured" (`e486e3b5`), and the evidence note's gap (the ws1b tree was not hash-checked) | The governing baseline is `155181d6`. The contract was re-measured at `d98f45d3` in this independent clone. `routes/workout_plan.py` was last changed by `3532f86` (#447). `utils/database.py`, `utils/supersets.py`, `utils/errors.py`, `utils/request_id.py` and `exercises.js` did not change between `e486e3b5` and `d98f45d3`, or since. Every F1/F2 line citation is therefore still exact, and no fact rests on the ws1b tree any more. | packet §3; CONTRACT_ANALYSIS §1 |
| Δ2 | A5 (tests run on the conftest twin; no test imports `app`) | Obsolete. The conftest `app` fixture is `create_app(config_overrides={"TESTING": True, "WTF_CSRF_ENABLED": False})` (`tests/conftest.py:199-227`). `requestId` is always present and equals the `X-Request-ID` response header. Tests therefore send `X-Request-ID` and compare whole envelopes, `requestId` included. | packet §2, §3 |
| Δ3 | A6 (F3 edges derived, not executed) | Discharged. Every F3 edge was executed: 49 request cases, each run under `TESTING` and production config, with identical results. Δ4–Δ6 are the corrections. | packet §2 |
| Δ4 | F3 bullet 6 (a truthy non-object body; "the behaviour differs between the conftest twin and the real app") | `data.get` raises `AttributeError`, and the `except` block raises it a second time. That exception escapes the view to the `Exception` handler of `register_fallback_handlers` (`utils/errors.py:272-279`). The handler returns an **HTML 500** ("An unexpected error occurred."), or, for an XHR request (`is_xhr_request()`, `utils/errors.py:47-64`), a **JSON 500 `INTERNAL_ERROR` "An unexpected error occurred"**. The route's `Error removing exercise` record never fires. The outcome is identical under `TESTING` and production config. The production client sends neither `Accept` nor `X-Requested-With` (`exercises.js:25-30`, `useDefaultHeaders: false`), so UI calls are non-XHR. | packet §3; CONTRACT_ANALYSIS §4 |
| Δ5 | F3 bullet 5 ("A Unicode digit such as `"²"` … ends in a 500") | This holds only for non-decimal digits such as `"²"`. A Unicode *decimal* digit passes both `isdigit()` and `int()`: `{"id": "٣"}` returns 200 and deletes row 3. It is recorded as follow-up 1 (§P11), and is neither fixed nor pinned. | packet §3 |
| Δ6 | F3 bullet 7 (falsy JSON, including `null`, returns 400) | This holds for a literal JSON `null` body. A request with no body returns 500 (`UnsupportedMediaType`). So do `text/plain`, a form-encoded body and an over-large integer id (`OverflowError` raised from `fetch_one`). | packet §3; TEST_DESIGN §10 item 4; CONTRACT_ANALYSIS §4 |
| Δ7 | F6 and F9 (registration coverage "in `tests/conftest.py`"; F6 line numbers) | `tests/conftest.py` no longer imports `workout_plan_bp`. Blueprint-registration coverage is `tests/test_app_factory.py` `EXPECTED_BLUEPRINTS` (`:40`, size `== 13` at `:123`), which the Route/API row now names (`QUALITY_GATE.md:46`). The remaining importers moved to `app.py:22,232` and `tests/test_priority7_error_handling.py:34,54`. The other F6 names and tests are unchanged. | packet §2; CONTRACT_ANALYSIS §1 |
| Δ8 | F7(a)'s location (`OPEN_WORK_EXECUTION_PLAN.md:853-863`), also cited by Q-WS4-2 | Stale citation. #541 moved the record but did not repeal it. The live designation is `docs/REFACTOR_PLAN.md:1623-1628`. The verbatim #447 record is at `docs/archive/2026/open-work/OPEN_WORK_EXECUTION_HISTORY.md:868-878`. The owner's authorization supersedes the designation for this packet only, and both records stay unedited. | packet §2 |
| Δ9 | F8 (WS3 stopped at Gate 0; three coupling points) | WS3 merged as #545 (`d98f45d3`). The fixture coupling is gone, because the conftest `app` is `create_app()`. Q-WS3-2(a) settles the logger coupling. Slice 1 edits none of the shared documents. | packet §2; CONTRACT_ANALYSIS §6 |
| Δ10 | Q-WS4-8's premise ("pinning it on the twin would be overturned by WS3") | Removed. The non-object outcome is identical under `TESTING` and production config, so a pin is stable. Which edges to pin remained a choice, and the owner chose D4. | packet §2 |
| Δ11 | Q-WS4-3: "Not pinning leaves the behaviour unguarded" | Refuted by measurement. The AC6 order and `commit` nodes kill every atomicity mutant, and the partial-commit node has no unique kill. It is kept for the user-visible persisted state it records. | packet §4 D2; TEST_DESIGN §6 |
| Δ12 | Q-WS4-7's premise ("the 45-module logging side effect") | Importing `utils.database` already attaches the handlers and creates `logs/` (measured). A module-level `get_logger()` in a new utils module would therefore add no side effect. There were 47 such module-level sites at `d98f45d3`. | packet §2; CONTRACT_ANALYSIS §5 |
| Δ13 | "`AGREED_PLAN.md` … untracked" (the rev 1 header's Source of truth and Tracking rows; the raw request's parenthetical) | Stale. `AGREED_PLAN.md` has been tracked on `main` since #531 (`71c4cc6`). This file is tracked from C0, which also settles Section 0's "Decision not needed now" about where it lives (packet D10). | packet §2, §4 D10 |
| Δ14 | AC8's caplog comparison | At DEBUG level, `utils/database.py` emits `SQL exec` and `SQLite connection closed` records on the same logger, interleaved with the route's. Above 100 ms a `SQL exec` line becomes a `Slow query detected` WARNING. AC8's comparisons therefore exclude records emitted from `utils/database.py`. Otherwise they would pin database internals and timing. | packet §3 *Logging*; TEST_DESIGN §4 |

Found while writing Plan v1 (not in the packet):

| Δ | Superseded statement in Section 0 | Correction | Evidence |
|---|---|---|---|
| Δ15 | Q-WS4-9's citation of a `CLAUDE.md` §3 section, "Reasoning effort is not agent authorization" | `CLAUDE.md` at `155181d6` has no such section. It exists only as an uncommitted edit in the shared checkout; the WS3 record found the same (`docs/app_factory/PLANNING.md:529`). The point is moot, because the owner chose no council. | `CLAUDE.md` at `155181d6` |
| Δ16 | F9's closing gate: "`CLAUDE.md` §4B says refactors finish with `/verify-and-polish`" | At `155181d6`, §4B (`CLAUDE.md:145-155`) requires a full-pytest baseline before the change (step 1). Before done it requires "full pytest + relevant E2E specs", using `/verify-suite` (step 5). It does not name `/verify-and-polish`. AC12, as accepted, does name it. Plan v1 runs both: the baseline (§P7 item 1) and the `/verify-and-polish` components (§P7–§P8). | `CLAUDE.md:145-155` at `155181d6` |

**How the corrections apply to the acceptance criteria** (the AC wording is unchanged):
- **AC2:** tests compare the whole success envelope, `requestId` included (Δ2). That is stricter than "keys excluding `requestId`", so it satisfies AC2.
- **AC3:** the measured behaviour is stronger: 400 paths construct no `DatabaseHandler` at all. Plan v1 pins that.
- **AC4:** the owner-selected string forms are the leading-zero id (`"0099999"` when the row is missing, `"00N"` when it exists) and `"0"` → 404 (D4).
- **AC5:** the non-object body is pinned as D4 states (Δ4).
- **AC7:** Q-WS4-3 (a).
- **AC8:** comparisons exclude `utils/database.py` records (Δ14). §P5.1 item 1 pins each distinct route record sequence once.
- **AC9:** "the form Q-WS4-4 selects" is raw.
- **AC10 and AC12:** read F6 and F9 as corrected by Δ7 and Δ16.

**Live records that still disagree with this slice.** These are recorded here and not resolved. All three stay unedited; status edits belong to lane S1.
- `docs/OPEN_WORK_EXECUTION_PLAN.md:48` (§0.2) says WS3–WS5 each need "its own Gate 0, council and Gate 1". For this slice, the owner's Q-WS4-9 answer (no council) and the Gate 1 delegation supersede it.
- `docs/project_direction/AGREED_PLAN.md:215` (§6) still reads "DRAFT — follows WS3".
- `docs/REFACTOR_PLAN.md:1623-1628` still says the file "stays off-limits". The owner's authorization supersedes that for this packet only.

*Gate 0 was signed on 2026-10-22 (record above). Plan v1, Agent provenance and Sign-off follow. There is no council (Q-WS4-9), so the template's Reviewer findings, Response matrix and Plan v2 sections are not used. The delegated Gate 1 record is appended after Plan v1, in its own commit.*

---

## Plan v1

*Written 2026-10-22 (rev 3), after the owner signed Gate 0. It adopts the decision packet's *Plan v1 design* list (§4) and architecture-review findings 2–15. Finding 1 (no authorization to edit the route) is discharged by the owner's 2026-10-22 text. Every `path:line` is at `155181d6` unless marked otherwise. Artifact paths are under the clone's gitignored `artifacts/`.*

**Goal.** The database work of `POST /remove_exercise` moves from `routes/workout_plan.py` into a new `utils/workout_plan_service.py`. Every HTTP, database and pinned-log observable stays the same, including the non-atomic, per-statement commit scope.

**Scope.** In: §P1. Out: §P11, plus Section 0 *Out of scope*, unchanged.

**Effort**: M · **Owner**: the primary O2 session (orchestration and commits), `automation-qa` (tests), `senior-developer` (service and route) · **Depends on**: a favourable delegated Gate 1 (§P14). The push and the ready PR that the CI steps need are authorized by the owner's direct lane-O2 instruction (§P14.4), not by Gate 1, and happen only after Gate 1 and the local §P7 checks.

### P1. File manifest

| Path | Change | Content | Agent | Commit |
|---|---|---|---|---|
| `utils/workout_plan_service.py` | new | §P2 | `senior-developer` | C3 |
| `routes/workout_plan.py` | modify | The `remove_exercise` body (§P3), plus exactly one import line, `from utils import workout_plan_service as plan_service`, placed directly after `from utils import supersets as superset_service` (`:13`). Nothing else. | `senior-developer` | C3 |
| `tests/test_remove_exercise_characterization.py` | new | §P5.1 | `automation-qa` | C2 |
| `tests/test_workout_plan_service.py` | new | §P5.2 | `automation-qa` | C3 |
| `docs/test_inventory/**` | regenerate | Output of `python scripts/generate_test_inventory.py`; never hand-edited | `senior-developer` | C4 |
| `docs/service_extraction/PLANNING.md` | this file | Revs 2–3, then the Gate 1 record | `product-manager` | C1, then its own commit |

**Not touched** (zero diff, checked in §P7 item 10):
- `tests/test_workout_plan_routes.py` and every other existing test (AC11);
- `utils/__init__.py`, `utils/supersets.py`, `utils/database.py`, `tests/conftest.py`, `app.py`;
- `static/**`, `templates/**`, `e2e/**`, `.github/**`, `.claude/**`, every `CLAUDE.md`;
- `docs/MASTER_HANDOVER.md`, `docs/OPEN_WORK_EXECUTION_PLAN.md`, `docs/project_direction/AGREED_PLAN.md`, `docs/REFACTOR_PLAN.md`, `.claude/rules/database.md`.

**Departure from Section 0's *In scope* wording.** Section 0 places the characterization tests "in `tests/test_workout_plan_routes.py`". Plan v1 puts them in a new file instead (packet D9; TEST_DESIGN §9; architecture finding 12), for three reasons:
- the zero diff to the existing route test file makes AC11 provable;
- the file can land as the characterization-first commit on its own;
- it still enters the route's targeted derivation, because it contains `/remove_exercise`.

### P2. Service API (`utils/workout_plan_service.py`)

- **Types.** `class RemovedPlanExercise(NamedTuple)` with `routine: Any` and `exercise: Any`, holding the raw column values (Q-WS4-4).
- **Function.** `remove_plan_exercise(exercise_id: Any) -> Optional[RemovedPlanExercise]`. `exercise_id` is the route-validated id exactly as sent. `None` means that no row has that id.
- **Transaction scope.** One `with DatabaseHandler() as db_handler:` block runs, in this order:
  1. `fetch_one("SELECT routine, exercise, superset_group FROM user_selection WHERE id = ?", (int(exercise_id),))`;
  2. only when `superset_group` is truthy, `superset_service.unlink_partner_for_removal(db_handler, exercise_id, group)`, with the **raw** id;
  3. `execute_query("DELETE FROM workout_log WHERE workout_plan_id = ?", …)`;
  4. `execute_query("DELETE FROM user_selection WHERE id = ?", …)`.

  Each write uses the default `commit=True`; no `commit` keyword is passed.
- `int(exercise_id)` is evaluated inside the `with` (A2).
- There is no `BEGIN`, no `commit=False`, no `executemany`, no new transaction wrapper and no `try`/`except`. Exceptions propagate unchanged, and `__exit__` rolls back and closes exactly as it does today.
- `return None` sits inside the `with`, so `__exit__` commits (nothing is pending) and closes, as base does on the 404 path. The `RemovedPlanExercise` is built after the `with` exits, the point at which base emits its INFO record.
- **Imports.** The module imports only `typing`, `utils.database` (`DatabaseHandler`) and `utils.supersets` (as `superset_service`). It calls the unlink through the module attribute, so a test that patches `utils.supersets.unlink_partner_for_removal` is seen. It never imports `routes`. `utils/__init__.py` is unchanged.
- **No `logger` and no log records (packet D5).** This is a deliberate exception to `CLAUDE.md` Playbook A ("Add `from utils.logger import get_logger` + `logger = get_logger()` at module top", `CLAUDE.md:136`). The justification is the owner's Q-WS4-7 answer ("service emits no logs") and Section 0's Q-WS4-7(b). Every existing record stays in the route and in `utils/supersets.py`, so the record order is unchanged. A module-level logger would add no side effect (Δ12), but it would be an unused name. §P5.2 item 8 asserts that it is absent.

**Reference shape.** This is M01's `SERVICE_SOURCE` (`artifacts/parallel-next-five/ws4/designer/mutation/mutate.py:35-66`) with docstrings added. The statements, arguments, order and control flow are binding; the docstring wording is not. The docstrings must not repeat the "share its connection and write lock" wording that F2 describes as misleading.

```python
"""Plan-row removal behind ``POST /remove_exercise`` (WS4 slice 1).

Moved from ``routes/workout_plan.py`` without a behaviour change. Removal is not
atomic: each statement commits on its own (``execute_query``'s default
``commit=True``), so a failure in a later statement leaves the earlier ones
committed.
"""
from typing import Any, NamedTuple, Optional

from utils import supersets as superset_service
from utils.database import DatabaseHandler


class RemovedPlanExercise(NamedTuple):
    """The removed row's ``routine`` and ``exercise``, verbatim from the database."""

    routine: Any
    exercise: Any


def remove_plan_exercise(exercise_id: Any) -> Optional[RemovedPlanExercise]:
    """Delete one ``user_selection`` row and its ``workout_log`` rows.

    ``exercise_id`` is the caller-validated id exactly as sent. It is passed on
    unchanged to ``unlink_partner_for_removal``, which logs it. Returns ``None``,
    having written nothing, when no row has that id. Exceptions propagate unchanged.
    """
    with DatabaseHandler() as db_handler:
        exercise_info = db_handler.fetch_one(
            "SELECT routine, exercise, superset_group FROM user_selection WHERE id = ?",
            (int(exercise_id),)
        )
        if not exercise_info:
            return None
        if exercise_info.get('superset_group'):
            superset_service.unlink_partner_for_removal(
                db_handler, exercise_id, exercise_info['superset_group']
            )
        db_handler.execute_query(
            "DELETE FROM workout_log WHERE workout_plan_id = ?", (int(exercise_id),)
        )
        db_handler.execute_query(
            "DELETE FROM user_selection WHERE id = ?", (int(exercise_id),)
        )
    return RemovedPlanExercise(exercise_info.get('routine'), exercise_info.get('exercise'))
```

### P3. Route (`routes/workout_plan.py`)

- **What stays in the route:**
  - `data = None`, and `request.get_json()` inside the `try`;
  - the "No data provided" check;
  - the DEBUG `Received data for remove_exercise: …` record, before id validation;
  - the `isdigit()` id check;
  - the raw-id 404 `error_response`;
  - the INFO `Exercise removed from workout plan` record;
  - `jsonify(success_response(...))`;
  - the whole `except Exception` block, including the non-dict double raise (`data.get` inside `extra=`).
- **What is replaced.** Lines `:266-300`, from the `with DatabaseHandler()` block through the success `return`, become M01's `EXTRACTED_ROUTE_BLOCK` (`mutate.py:68-81`). Lines `:252-265` and `:301-306` stay byte-identical, including the whitespace-only line `:259`.
- **The `'unknown'` fallbacks.** At `:296-297` they become `removed.routine` and `removed.exercise`. This is behaviour-neutral. At that point `exercise_info` is always a non-empty `dict`, because the falsy case already returned 404, so the fallback branch is unreachable and both forms yield the raw column value, whatever it is. The packet's further point, that both columns are `NOT NULL` (`utils/db_initializer.py:186-187`), is true but not needed for the argument.
- **Aliases and imports.** No new alias is added. The existing aliases (`:25-41`) and their identity tests stay untouched. The `superset_service` import stays (the aliases and other handlers use it), and so does `DatabaseHandler` (eight other `with` contexts use it). No import becomes unused, which matters because flake8 F401 is blocking (`.github/workflows/ci.yml:119`).

Post-extraction handler. Only the import line and the block between the id check and the `except` differ from base:

```python
@workout_plan_bp.route("/remove_exercise", methods=["POST"])
def remove_exercise():
    data = None
    try:
        data = request.get_json()
        if not data:
            return error_response("VALIDATION_ERROR", "No data provided", 400)
        
        logger.debug(f"Received data for remove_exercise: {data}")

        exercise_id = data.get("id")
        if not exercise_id or not str(exercise_id).isdigit():
            return error_response("VALIDATION_ERROR", "Invalid exercise ID", 400)

        removed = plan_service.remove_plan_exercise(exercise_id)
        if removed is None:
            return error_response("NOT_FOUND", f"Exercise with ID {exercise_id} not found", 404)

        logger.info(
            "Exercise removed from workout plan",
            extra={
                'exercise_id': exercise_id,
                'routine': removed.routine,
                'exercise': removed.exercise
            }
        )
        return jsonify(success_response(message="Exercise removed successfully"))
    except Exception as e:
        logger.exception(
            "Error removing exercise",
            extra={'exercise_id': data.get("id", 'unknown') if data else 'unknown'}
        )
        return error_response("INTERNAL_ERROR", "Unable to remove exercise", 500)
```

### P4. Behaviour preservation

| Observable | Base (`:252-306`) | After C3 | Pinned by |
|---|---|---|---|
| Handlers opened | One, after validation | One, inside the service | `only_handler()` in the scope, 404 and partial-commit nodes; service item 9 |
| Statement order | SELECT → partner UPDATE (only when the group is truthy) → DELETE `workout_log` → DELETE `user_selection` | Same, in the service | Scope nodes (recorded calls and SQLite trace); service item 9 |
| Commit scope | Each write autocommits (`commit=True` default). No `BEGIN`, and the lock is not held between statements. **Not atomic.** | Same; no keyword passed | The `commit` field of the recorded calls; the trace; the partial-commit node |
| Partial-commit state | If the final DELETE fails, the partner unlink and the log delete stay committed, and the row stays with its own group | Same | `test_known_behaviour_partial_commit_survives_late_failure` |
| No-write paths | A 400 opens no handler. A 404 runs only the SELECT. | Same: on 400 the route returns before calling the service; on 404 the service returns `None` after the SELECT | Validation and not-found nodes; service item 4 |
| Raw values | The raw id appears in the 404 message, the unlink call and both log records; row values are verbatim | Same | The single-node killers of M05, M07/M21 and M14/M20; service items 5–6 |
| Envelopes and status codes | Success: `{ok, status, message, requestId}`, no `data`. Error: `{ok, status, message, error{code, message, requestId}}`. Status 200/400/404/500. | The same `success_response`/`error_response` calls, still in the route | Every node |
| Exceptions | Any exception inside the `with` → rollback and close → the route's `except` → 500 | The service's `with` does the same, and the exception reaches the same `except` unchanged | The DB-failure and partial-commit nodes; service item 7 |
| Non-object body | Double raise → app-level 500 | Unchanged; it is raised before the service is called | `TestNonObjectBody` |
| Route log records and their order | DEBUG `Received data…` (after the no-data check, before id validation); supersets INFO; route INFO after the handler closes; `Error removing exercise`; `API error` | Same; the service emits none | The six sequence nodes (§P5.1 item 1); service item 8 |

**Two differences, both already measured and invisible (TEST_DESIGN §10 items 6–7):**
1. **404 ordering.** On the 404 path, base calls `error_response` (and logs `API error`) while the handler is still open. After C3, the service's `with` closes first and the route calls `error_response` afterwards. The only trace of this is the relative order, in `app.log`, of `utils/database.py`'s DEBUG `SQLite connection closed` record and the `API error` record. Records from `utils/database.py` are outside the AC8 contract (Δ14). The database work is identical: one SELECT, an empty commit, then close.
2. **Unicode-digit handler count.** For `"²"`, base opens a handler before `int()` raises. Because `int()` stays inside the service's `with`, the count stays at one handler. The characterization deliberately does not pin the count, so a later change to the id type (follow-up 5) is not blocked by it.

Neither difference changes any HTTP, database or pinned-log observable. The M01 control has this exact shape, and all 43 draft nodes passed against it unchanged (TEST_DESIGN §4).

### P5. Tests

#### P5.1 `tests/test_remove_exercise_characterization.py` (C2; `automation-qa`)

The source is the draft `artifacts/parallel-next-five/ws4/designer/draft/test_remove_exercise_characterization.py`: 43 nodes, all passing on `155181d6` via `-p tests.conftest`. These parts are kept as drafted:
- the `X-Request-ID` header, and whole-envelope equality with `requestId` included;
- the `plan` fixture;
- trigger-based failure injection;
- the caplog filter, which drops records whose `filename` is `database.py` (Δ14).

The draft is changed as follows.

1. **Log assertions (architecture finding 8; AC8).** The full ordered record list (levels, messages and extras) is asserted once for each distinct route record sequence, in six nodes:

   | Route record sequence | Node |
   |---|---|
   | Success, no group: DEBUG `Received…` → INFO `removed` | Draft node 4, `test_logs_without_superset` (the only killer of M14 and M20) |
   | Success, grouped: DEBUG → supersets INFO → INFO `removed` | Draft node 8, `test_superset_logs_carry_raw_ids` (the only killer of M07 and M21) |
   | 400 invalid id: DEBUG → `API error` | One `Invalid exercise ID` case. It must be an invalid-id case, not a falsy-body one: only that path shows that the DEBUG record comes before validation (M17). |
   | 404: DEBUG → `API error` | One not-found case |
   | 500 inside the database work: DEBUG → `Error removing exercise` (raw id, `exc_info`) → `API error` | Draft node 37, `test_database_failure_is_500` |
   | 500 from `get_json`: `Error removing exercise` (`exercise_id='unknown'`, no DEBUG) → `API error` | One unreadable-body case |

   Every other error node checks only the `API error` record, through `_assert_api_error`. The falsy-body nodes also keep their record count, because that single record is their whole sequence. The remaining success nodes assert no log, except draft node 3, which keeps its single raw-`exercise_id` check. Every node keeps its HTTP, recorder and database-state assertions.

   Finding 8 proposed about five representative nodes. The sixth covers the one route sequence those five leave unpinned, the `get_json` failure, which AC8 lists.

   After this trim, M17 is expected to become a single-node kill (the representative 400). §P7 item 3 measures it.
2. **Non-object body (finding 7; D4).** `TestNonObjectBody` keeps the four browser-request cases (`[1]`, `5`, `"x"`, `true`). Each asserts only three things: status 500, `mimetype == "text/html"`, and no record with the message `Error removing exercise`. The exact `errors.py` HTML copy and the `Unhandled exception` record are not asserted. Draft node 43 (the XHR JSON 500) is dropped. M19 stays killed.
3. **Unicode digits (D4; finding 13).** The `"²"` node asserts 500, the envelope, an unchanged database and the `API error` record. It does not pin the handler count. `"٣"` → 200 is **not** pinned (follow-up 1).
4. **SQL trace (finding 9).** The `_sql_trace` equalities stay in the seven nodes that carry them. They are unproven on Linux, so the confirmation comes from the ubuntu `Python Tests (core)` job (`.github/workflows/ci.yml:921-984`) on the PR head. If they fail there while passing on Windows, the fallback is one test-only commit. It removes the trace equalities, plus the trace callback and the `_bound`/`_sql_trace` helpers if nothing else uses them, and is verified to pass on both the C2 and C3 trees. The fallback loses only the M22 kill, and the PR records that loss.
5. **Seam (finding 11).** `_Recorder` keeps patching `utils.database.DatabaseHandler` on the class. It gains a comment that its wrappers copy the signatures of `__init__`, `execute_query`, `executemany`, `fetch_one`, `fetch_all` and `__exit__` (`utils/database.py:286,294-300,372,432,464,514`), and must change when those do. Neither `mutation/test_seam_demo.py` nor the mutation harness is shipped.
6. **Partial commit (finding 10; Q-WS4-3(a)).** The node is named `test_known_behaviour_partial_commit_survives_late_failure`. Its docstring opens with **"CURRENT BEHAVIOUR, NOT ENDORSED (Q-WS4-3(a))"**, and states that an atomicity fix (follow-up 3) must invert the node deliberately. That fix is out of scope here. The `handler.exit_exc == ["IntegrityError"]` assertion is relaxed to "exactly one entry, and it is not None". The persisted-state assertions stay.
7. **D4, exactly.**
   - **Pinned:**
     - `"0"` → 404 versus `0` → 400 (`test_int_zero_is_400_but_string_zero_is_404`, `test_not_found[string-zero]`, `test_invalid_id[int-zero]`);
     - leading-zero ids (`test_not_found[leading-zero-string]` with `"0099999"`, and `test_leading_zero_string_id_resolves_the_row` with `"00N"`);
     - malformed JSON, `text/plain`, form-encoded and no-body → 500 (`test_unreadable_body_is_500`, four cases);
     - `"²"` → 500, without the handler count;
     - non-object body → 500 `text/html`, with no route `Error removing exercise` record.
   - **Not pinned:** the exact `errors.py` HTML and XHR copy, and `"٣"` → 200.

The node count is the draft's 43, minus node 43, plus any dedicated representative nodes `automation-qa` uses for item 1. It is not fixed here, and the inventory is regenerated from the collected count (§P6, C4).

#### P5.2 `tests/test_workout_plan_service.py` (C3; `automation-qa`, written from this plan before the service exists)

The file follows TEST_DESIGN §8.
1. **Import order.** A subprocess test, parametrized over both import orders with `routes.workout_plan` (two nodes). Precedent: `tests/test_superset_service.py:10-25`.
2. **No `routes` import.** An `ast` parse of the module finds no `Import`/`ImportFrom` whose module starts with `routes`.
3. **`utils/__init__.py` untouched.** Already covered by `tests/test_utils_package.py`, which is in the targeted run. No new node.
4. **Missing id.** The function returns `None`. A file-local, class-level recorder shows one handler with exactly one `fetch_one` and no `execute_query`, and the database snapshot is unchanged.
5. **Existing id.** The result is a `RemovedPlanExercise` equal to the row's `routine` and `exercise` verbatim; the row is seeded with surrounding whitespace to prove it. The row and its logs are gone.
6. **Raw id passed through.** The function is called with `str(N)` on a supersetted row, with a spy on the module attribute `utils.supersets.unlink_partner_for_removal`. The spy receives `str(N)` and the same handler instance that ran the SELECT.
7. **Propagation.** A trigger on the selection DELETE makes `sqlite3.IntegrityError` leave the service unwrapped. `"²"` raises `ValueError`.
8. **No logging.** caplog at DEBUG shows no record whose `pathname` ends in `workout_plan_service.py`, and the module has no `logger` attribute.
9. **Included: order and commit without HTTP.** Parametrized over a grouped row and an empty-group row. It asserts one handler, with calls exactly SELECT → UPDATE (grouped only) → DELETE `workout_log` → DELETE `user_selection`, and `commit=True` on every write. Two reasons for including it:
   - Section 0's *In scope*, accepted at Gate 0, lists "statement order, no `commit=False`" for this file.
   - `QUALITY_GATE.md:128` derives the targeted run for a later change to `utils/workout_plan_service.py` alone as `tests/test_workout_plan_service.py` plus `rg "utils\.workout_plan_service|from utils.workout_plan_service import" tests`. The characterization file reaches the service only through HTTP and the class seam, and matches neither pattern. Without item 9, a service-only atomicity or order change would pass its targeted run and be caught only by full pytest.

   The recorder records calls and `commit` only, with no SQLite trace, so the Linux trace fallback touches one file. It is defined in this file, not imported from the characterization module, so neither test file depends on the other.

#### P5.3 Acceptance criterion → test mapping

| AC | Evidence |
|---|---|
| 1 | The C2 run on the unmodified route (§P7 item 2). `git diff C2 C3 -- tests/test_remove_exercise_characterization.py` is empty, and the same file is green at C3 (§P7 items 4, 10). |
| 2 | `TestSuccessContract::test_envelope_and_rows[int-id, string-id]` and `::test_leading_zero_string_id_resolves_the_row`; service item 5 |
| 3 | `TestValidationContract::test_falsy_body_is_no_data` (six cases) and `::test_invalid_id` (13 cases): zero handlers, database unchanged |
| 4 | `TestNotFoundContract::test_not_found[int, leading-zero-string, string-zero]` and `::test_int_zero_is_400_but_string_zero_is_404`; service item 4 |
| 5 | `TestFailureContract::test_unreadable_body_is_500` (four cases), `::test_unicode_digit_is_500` and `::test_database_failure_is_500`; `TestNonObjectBody` (four cases, per D4) |
| 6 | `TestStatementScope::test_without_superset[null-group, empty-group]` and `::test_with_superset`; service item 9 |
| 7 | `test_known_behaviour_partial_commit_survives_late_failure` |
| 8 | The six sequence nodes of §P5.1 item 1; the `API error` check on every error node, which also pins the endpoint `workout_plan.remove_exercise`; service item 8 |
| 9 | Service items 1, 2 and 4–7; the existing `tests/test_utils_package.py` |
| 10 | The diff-confinement check (§P7 item 10a). The existing identity tests: `tests/test_superset_service.py:28-48`, `tests/test_replace_exercise.py:32-48`, `tests/test_schema_registry.py`, `tests/test_filter_values.py`. `tests/test_app_factory.py` (`EXPECTED_BLUEPRINTS`). The endpoint name in every `API error` check. `code-reviewer`. |
| 11 | §P7 item 10c; the F4/F6 tests green with no diff |
| 12 | §P7, §P8 and §P9 |
| 13 | §P13 |

### P6. Sequencing, commits and agents

**S0, readiness** (primary session; no code changes):
- Fetch in the clone. If `origin/main` is no longer `155181d6`, run `git diff --stat 155181d6 origin/main -- routes/ utils/ tests/ static/js/modules/exercises.js docs/ai_workflow/QUALITY_GATE.md requirements.txt package.json package-lock.json`. Any hit outside `docs/test_inventory/**` stops the work until the `product-manager` revises the affected parts of this plan.
- Re-check that no live recovery freeze covers the clone, and that `WORKSTREAM_OWNERSHIP.local.md` (read-only) has no active claim on a §P1 path.
- Record the pre-change full-pytest baseline that `CLAUDE.md` §4B step 1 requires (`CLAUDE.md:146-150`) in `artifacts/o2/runs/baseline_full_pytest.txt`.

**Commits:**
- **C0** (done): `c5a1a43`, the verbatim brief.
- **C1:** this rev 2/3 record. The Gate 1 record is appended later in its own commit, before C2.
- **C2:** the characterization file only. It must pass on the unmodified route, proven by a run at C2 (AC1; §P7 item 2). Mutation check (a) runs at C2.
- **C3:** `automation-qa` first writes `tests/test_workout_plan_service.py`, which is red (`ModuleNotFoundError`). `senior-developer` then writes the service and the route edit, and edits no test. C3 contains all three files. The characterization file is unchanged and still passes. Mutation check (b) runs after C3.
- **C4:** the regenerated `docs/test_inventory/`.
- Every commit uses `git commit -F <file>`, with the message file under `artifacts/o2/`; the repository guard blocks heredocs. Files are staged by explicit path, never with `git add -A`.
- `Test Inventory Drift` is red at C2 and C3 by construction and green from C4. Only the final head is evaluated.
- After C4, run the §P7 checks and the §P8 reviews. Fixes land as new commits, and the affected checks are re-run. Then, under the owner's direct instruction quoted in §P14.4, push the branch and open a ready (non-draft) PR. Fix forward until all CI is green on the final head, then stop. No merge: the owner approves each merge by PR number and head SHA.

**Agents:**
- `automation-qa` finalizes both test files and writes only under `tests/**`.
- `senior-developer` writes the service and the route edit, edits no test, and regenerates the inventory.
- `product-manager` writes only this file.
- The primary session orchestrates and commits.
- The implementers are independent of the §P8 reviewers.

### P7. Validation

Every run uses §P13's isolation, and its output goes under `artifacts/o2/runs/`.
1. **Pre-change baseline** (S0): full pytest at the base.
2. **AC1 at C2:** `pytest tests/test_remove_exercise_characterization.py` on the unmodified route, all passing.
3. **Mutation check (a), at C2.**
   - Copy `artifacts/parallel-next-five/ws4/designer/mutation/mutate.py` to `artifacts/o2/mutation-pre/`, so that the packet's evidence folder is not overwritten. Point the copy at the final characterization file, with the seam demo excluded, and run it on a `git archive` of C2. Never run it on the tracked tree.
   - The matrix has 23 entries: the controls M00 and M01, and 21 behaviour-changing mutants, M02–M22 (`mutate.py:114-237`). The packet's "22/22" (§7) and TEST_DESIGN's "1 of 22" (§1) do not match that count; the list in the harness governs.
   - Pass rule: M00 and M01 show no failures, and each of M02–M22 fails at least one node. Report every mutant's killers, and every single-node killer by name. Expected single-node killers: M05, M07, M21, M14, M20, and, after the log trim, M17.
   - Any surviving mutant sends the file back to `automation-qa` before C3. If the trace fallback is later taken, M22 becomes the one recorded survivor.
4. **Targeted union**, at C3 and after every fix. It combines the derivations of `QUALITY_GATE.md:127-128` with two named oracles and two module importers:
   - for `routes/workout_plan.py`: `tests/test_workout_plan_routes.py` plus `rg "routes\.workout_plan|workout_plan_bp|/remove_exercise" tests`;
   - for `utils/workout_plan_service.py`: `tests/test_workout_plan_service.py` plus `rg "utils\.workout_plan_service|from utils.workout_plan_service import" tests`;
   - `tests/test_app_factory.py`, the Route/API row's registration oracle;
   - `tests/test_utils_package.py` (AC9);
   - `tests/test_schema_registry.py` and `tests/test_filter_values.py`, which import the module as `from routes import workout_plan` and so escape the pattern (CONTRACT_ANALYSIS §7).

   At `d98f45d3`, the analyst's 13-file version of this union, run before the new files existed, gave 307 passed and 1 skipped.
5. **Mutation check (b), after C3.** `git archive` C3 into `artifacts/o2/mutation-post/`. Apply each of these to its copy of `utils/workout_plan_service.py`:
   1. swap the two DELETEs;
   2. `commit=False` on the writes;
   3. pass `int(exercise_id)` to the unlink;
   4. return normalized values (stripped, `'unknown'` for `None`);
   5. unlink unconditionally;
   6. split the work across two handlers (the lookup in one `with`, the writes in another);
   7. add a log record (a module `logger` plus one `info`).

   Pass rule: each mutant is killed by the final test set, and also by `tests/test_workout_plan_service.py` alone, since that is §P5.2 item 9's reason. If not, `automation-qa` strengthens the unit file.
6. **Full pytest before ready:** `.venv/Scripts/python.exe -m pytest tests/ -q`, compared with item 1. A failure absent from the baseline is a defect of this slice. A failure also present in the baseline is recorded as pre-existing, but only after it is confirmed to reproduce on the base.
7. **Chromium, run locally under §P13's isolation.**
   - **Scope: the whole CI functional spec list.** That is the 25 specs of the `e2e-functional-shard` job (`.github/workflows/ci.yml:466-490`). The list already contains the five targeted specs:
     - `workout-plan.spec.ts`, `exercise-interactions.spec.ts` and `superset-edge-cases.spec.ts` (the feature-map row, `QUALITY_GATE.md:142`);
     - `api-integration.spec.ts` and `error-handling.spec.ts` (the F4 remove consumers).
   - **Command.** One invocation: `npx playwright test <the 25 specs> --project=chromium --reporter=line`, with a private `PW_PORT` (a free port other than 5000), a private `PW_DB_PATH` under the clone's `artifacts/`, and `PW_REUSE_SERVER` unset. Playwright then starts this clone's `app.py` against a throwaway database (`playwright.config.ts:168-187`). The five targeted specs may also be run first, on their own.
   - **Not run locally.** These are evidenced by their own CI jobs on the final head (item 12):
     - the isolated jobs' specs: `program-backup.spec.ts`, `fatigue-context.spec.ts` and `erase-flow.spec.ts`;
     - `visual.spec.ts`.

     Rationale: no template, CSS, JS or E2E file changes, and the visual state is platform-specific (`QUALITY_GATE.md:61`).
   - **Triage of a local red.** First rerun an identical batch before blaming the diff. A red that persists is called pre-existing only after it reproduces on base (`155181d6` code). Otherwise it is a defect of this slice.
   - Vitest is not run, because nothing under `static/js/**` changes.
8. **Pyright.** Run the CI-pinned `pyright@1.1.410`, then `scripts/pyright_baseline_diff.py` against `docs/ci_cd_phase3/pyright-baseline.json`. There must be zero net-new diagnostics. Fix the code, never the baseline (`QUALITY_GATE.md:72`). Test files count, because `pyrightconfig.json` excludes only `artifacts/**`.
9. **flake8**, with the blocking selection of `.github/workflows/ci.yml:119`, on the four changed Python files.
10. **Diff confinement.**
    - (a) `git diff C2 C3 -- routes/workout_plan.py` shows one added line after `:13` and the `:266-300` block replaced by §P3's, and nothing else. The new body contains no SQL string and no `DatabaseHandler` or `db_handler` (AC10).
    - (b) `git diff C2 C3 -- tests/test_remove_exercise_characterization.py` is empty (AC1).
    - (c) `git diff --name-only 155181d6 HEAD -- tests/` lists exactly the two new files (AC11).
    - (d) `git diff --name-only 155181d6 HEAD` stays within §P1.
11. **Test inventory.**
    - Regenerate with `python scripts/generate_test_inventory.py`, then run `--check`, which must be clean. Never hand-edit the output.
    - Before regenerating, confirm that no untracked or gitignored `.md` sits in a globbed surface directory (`QUALITY_GATE.md:71`).
    - If another lane merges first, this branch rebases and regenerates (the second-to-merge rule).
12. **CI on the final head.** Every check must be green, including:
    - `Python Tests (core)` on ubuntu, which confirms the trace assertions (§P5.1 item 4);
    - the E2E functional shards;
    - `E2E Backup (Chromium, isolated)`, `E2E Fatigue Context (Chromium, non-required)` and `E2E Erase Flow (Chromium, isolated, non-required)`, plus `Visual Regression (Windows baselines)`: the evidence for the specs that item 7 does not run locally;
    - `Test Inventory Drift`.

    The push and the ready (non-draft) PR this needs are authorized by the owner's direct instruction quoted in §P14.4. They happen only after the delegated Gate 1 and the local checks in items 1–11.

### P8. Implementation reviewers

| Manifest path | `QUALITY_GATE.md` row | Reviewer |
|---|---|---|
| `routes/workout_plan.py` | Route / API (`:46`) | `code-reviewer`. `product-risk-reviewer` only if a response shape changes, and none does. |
| `utils/workout_plan_service.py` | Business logic (`:48`) | `code-reviewer`. No calculation module is touched, so no `product-risk-reviewer`. |
| `tests/**` | none | — |
| `docs/test_inventory/**`, this file | Product docs (`:57`) | none |
| DB-row files | DB / schema (`:47`) | Not tripped, so no `architecture-reviewer` |

The union is a cold `code-reviewer`. A cold `unslop-reviewer` is added as part of `/verify-and-polish`, which AC12 names (`QUALITY_GATE.md:156`).
- **Briefing.** Each reviewer is briefed cold, with the diff against `155181d6`, this file and the governing rows, and no implementer summary.
- **Independence.** The reviewers are independent of each other and of `automation-qa` and `senior-developer`.
- **Incomplete reviews.** A reviewer that does not finish is *pending*, never "no findings".
- **BLOCKING findings.** A BLOCKING finding is fixed, and the fix is re-reviewed.
- **Handover.** The closing `/handover` step of `/verify-and-polish` updates only the local handover scratch. `docs/MASTER_HANDOVER.md` is not edited (§P1).

### P9. Migration notes (PR description)

The PR description carries this text:

> **Migration notes.** No behaviour, schema, API-shape or calculation change. The DB statements of `POST /remove_exercise` moved from `routes/workout_plan.py` to `utils/workout_plan_service.py` (`remove_plan_exercise`). The non-atomic per-statement autocommit scope is preserved: each statement still commits on its own, and a late failure still leaves the earlier statements committed (pinned as current behaviour, not endorsed). No migration notes are owed beyond this: there is no data, schema or configuration migration, no caller change and no user-visible change.

It also includes:
- the owner's authorization sentence, quoted verbatim from the Gate 0 record, with a statement that the off-limits records stay unedited;
- the evidence:
  - the C2 run;
  - the unchanged characterization file at C3;
  - the summaries of mutation checks (a) and (b);
  - full pytest against the baseline;
  - the targeted union;
  - the Chromium specs;
  - the pyright diff;
  - the inventory check;
  - the CI run;
  - each reviewer's verdict and agent ID;
  - §P4's two invisible differences.

### P10. Rollback

- **Before merge:** `git revert` C3, then regenerate `docs/test_inventory/`, because C4's counts include the service-unit file. The route returns to its C2 form. The characterization file is untouched, and it passes, as it did at C2.
- **After a squash merge:** a forward change restores the pre-PR `routes/workout_plan.py`, deletes `utils/workout_plan_service.py` and `tests/test_workout_plan_service.py`, and regenerates the inventory. The characterization file stays and passes.
- **No data rollback:** nothing in this slice changes a schema, data or configuration.

### P11. Out of scope and recorded follow-ups

These are verbatim from decision packet §6, "each would be a behaviour or API change needing its own approval":
1. `isdigit()` accepts Unicode decimal digits: `"٣"` deletes row 3.
2. The supersets unlink logs "Unlinked partner…" even when no partner exists.
3. Removal is non-atomic: a late failure leaves the partner unlinked and the logs deleted.
4. The non-object body double-raise produces the app-level generic 500 instead of the route's envelope.
5. Change the service id parameter to an int.
6. Stale citations: `.claude/rules/database.md:90` (line numbers) and `REFACTOR_PLAN.md:1627-1628` (pointer to an archived §4).
7. AGREED_PLAN §3.4 figures (D7), for the status/docs lanes.

"Also excluded, as the commission requires: `user_profile`, `progression`, schema, transaction redesign, logging reconfiguration, workflows, and global status or ledger edits."

Also out of scope:
- every other handler in `routes/workout_plan.py`, and every other route;
- Q-WS4-5 and Q-WS4-6, deferred by the owner and not blocking this slice;
- the "connection and write lock" wording that F2 describes (`utils/supersets.py:231-235`, `docs/REFACTOR_PLAN.md:824-828`), which stays; the new docstrings do not repeat it.

Fixing any of follow-ups 1–4 inside this PR would make the slice Large (architecture review, *Gate routing*).

### P12. Calculation surface

None. Section 0's *Calculation surface* stands unchanged: no calculation function, schema, catalog data or API response shape changes, and the excluded handlers stay byte-identical. Migration notes and tests are still committed under the `CLAUDE.md` §1 refactor invariant (§P5, §P9).

### P13. Isolation (AC13)

- **Clone.** All work happens in the standalone clone `D:\development\Hypertrophy-Toolbox-v3-ws4-slice1-20261021`, which has independent Git storage (a fresh clone with no `objects/info/alternates`; packet §1), on branch `ws4/remove-exercise-service`.
- **Environment.** Every command first sources `artifacts/o2/env.sh`. That file loads the packet environment:
  - a private `TEMP`/`TMP` (`artifacts\t`), which must exist and be at most 103 characters long (it is 69);
  - `PYTHONPYCACHEPREFIX`;
  - the pip, npm and Playwright caches;
  - unset `HT_RUNTIME_DIR`, `DB_FILE`, `FLASK_APP`, `TESTING`, `FLASK_DEBUG` and `FLASK_USE_RELOADER`.

  It then sets `HT_RUNTIME_DIR` to `artifacts\o2\runtime`. The clone's own `.venv` and `node_modules` are used.
- **Databases and logs.** pytest uses the per-test scratch database from `tests/conftest.py`, and the logs go to `artifacts\o2\runtime\logs`.
- **No app on port 5000.** Nothing is launched by hand. Playwright runs on a free `PW_PORT` other than 5000, with `PW_REUSE_SERVER` unset (§P7 item 7), so it never attaches to another checkout's server.
- **Shared checkout.** Nothing is written to `D:\development\Hypertrophy-Toolbox-v3-main`, including its untracked original of this file.
- **Operation A restrictions.** No worktree creation or removal, no `prune`, no branch deletion and no ref retirement. S0 re-checks that no live recovery freeze covers the clone.
- **Scratch output.** Mutation copies and evidence go under the clone's `artifacts/`, never into the tracked tree.

### P14. Gate 1 — what the advisers approve

**P14.1 Object.** The advisers approve Plan v1 as written: §P1–§P14 of this file, read together with Section 0, the Gate 0 record and the rev 2 delta. The binding is the SHA-256 the primary session computes over the whole file when it sends it out, after filling in the agent-ID placeholder. Any later edit voids the binding, and the file is then re-hashed and re-reviewed.

**P14.2 What the advisers check.**
1. **§P1.** The manifest is complete and confined. `routes/workout_plan.py` changes only inside `remove_exercise`, plus the one import line, as the owner's authorization requires. Nothing on the not-touched list changes. The new characterization file departs from Section 0's *In scope* wording; check that this is acceptable.
2. **§P2.** The service reproduces base's transaction scope exactly:
   - one handler, running the statements in base's order;
   - default commits;
   - `int()` inside the `with`, and `return None` inside the `with`;
   - no wrapper and no `try`;
   - raw values;
   - the unlink called through the module attribute;
   - no `routes` import.

   Also check that the stated exception to Playbook A (no logger) is acceptable.
3. **§P3.** The post-extraction body equals base outside the replaced block. The `except` block and the double raise are unchanged. Replacing the `'unknown'` fallbacks is behaviour-neutral.
4. **§P4.** No row changes an HTTP, database or pinned-log observable, and the two invisible differences are characterized correctly.
5. **§P5.1.**
   - The trims lose no mutant kill other than M22 under the stated fallback.
   - The six full-sequence nodes are the right set, including the sixth beyond finding 8's five.
   - D4 is pinned, and not pinned, exactly.
   - The partial-commit node carries the right label and the relaxed assertion.
6. **§P5.2.** The decision to include item 9, and its reason.
7. **§P5.3.** AC1–AC13 each have evidence.
8. **§P7.**
   - The pre-change baseline.
   - Mutation checks (a) and (b), and their pass rules.
   - The targeted union.
   - Item 7's Chromium design, as AC12's "`/verify-and-polish` (full pytest + Chromium …)":
     - locally, the whole 25-spec CI functional list in one isolated invocation;
     - the isolated-job specs and `visual.spec.ts` evidenced by their own CI jobs on the final head;
     - the triage rule for local reds.

     Check that the scope is sufficient, and that the specs left to CI are justified by the absence of any template, CSS, JS or E2E change.
9. **§P8.** The reviewer set, and the rule that a review that did not finish is pending.
10. **§P9, §P10, §P13.** The migration-note text, the rollback, and the isolation.

**P14.3 Decision rule.** The owner's second paragraph, verbatim (2026-10-22):

> Gate 1 for this slice is delegated to the AI consulting team. Three independent advisers review the written Plan v1, bound by its SHA-256. If they approve unanimously or by reasoned majority, with no unresolved BLOCKING finding, that is recorded as a DELEGATED Gate 1, not my signature. A BLOCKING finding is fixed and re-reviewed; if it still blocks, stop and ask me.

- **Who selects the advisers.** The primary session selects and briefs them. Each adviser reads this file directly at the bound hash, independently of the others, of this plan's author and of the implementers.
- **Fixing a BLOCKING finding.** The `product-manager` amends Plan v1 as a new revision, and the file is re-hashed and re-reviewed.
- **The Gate 1 record.** It names each adviser's agent ID, verdict and report path. It is labelled a DELEGATED Gate 1, not an owner signature, because Gate 1 is otherwise an owner approval (`QUALITY_GATE.md:24-30`).

**P14.4 Not decided by Gate 1 (owner-only).**

The owner's 2026-10-22 lane-O2 session prompt is the same direct instruction that carries the Gate 0 text. The primary O2 session relayed these two sentences from it verbatim:

> Finish at a ready (non-draft) PR with all CI green on the final head, then **STOP**.

> Merging any PR. I approve each merge by PR number and head SHA.

1. **Push and PR: owner-authorized.** `docs/ai_workflow/AUTONOMY.md:18` keeps "pushes to remote" behind explicit confirmation. The first sentence above is that confirmation.
   - The push and the ready PR are authorized by the owner's direct instruction, not by Gate 1, and the advisers neither grant nor withhold them.
   - They happen only after a favourable delegated Gate 1 and the local §P7 checks (items 1–11).
   - Work stops once the PR is ready and all CI is green on the final head (§P7 item 12).
2. **Merge: owner-only.** The owner approves each merge by PR number and head SHA.
3. **The three live status records** (rev 2 delta): lane S1.
4. **Q-WS4-5 and Q-WS4-6:** deferred by the owner.

**P14.5 What a favourable delegated Gate 1 authorizes.** S0 and C2–C4 in the clone, within §P1, together with the §P7 checks and the §P8 reviews. It authorizes nothing outside §P1.

### P15. Gate 1 — delegated decision record (2026-10-22)

*Appended in rev 4. §P1–§P14 above are the bound object and are not edited. The amendments GA-1…GA-14 bind the implementation on top of them. Each amendment takes precedence over the Plan v1 text it names.*

**Bound object.** This file at commit `3768e52`: SHA-256 `6e95835d84923bfd90d7bc63e27d3191308d8ded60a813dc1c9e90b682e328f9`, 96,894 B. The primary session computed the hash, then recomputed it over the byte-identical copy `artifacts/o2/gate1/PLANNING.plan-v1.md`; the two are equal. Rev 4 changes only this section and the four places listed in its Revision history row, so `git diff 3768e52 -- docs/service_extraction/PLANNING.md` shows §P1–§P14 untouched.

**Authority.**
- **Gate 1 delegation.** The owner's Gate 1 delegation, which is the second Gate 0 paragraph, with its decision rule quoted in §P14.3.
- **Consulting-team authorization.** From the same lane-O2 prompt, verbatim:

  > I delegate in-scope technical, classification and plan-disposition decisions to an AI consulting team. When a decision blocks progress:
  > 1. Spawn three independent read-only advisers: architecture, testing, and security/product risk.
  > 2. Quote this authorization to them verbatim.
  > 3. Adopt a reasoned disposition and keep the adviser reports.
  > 4. Record the disposition as DELEGATED (not my signature), then continue.
  >
  > A consulting verdict cannot create evidence, waive a required check, or widen this lane's scope.

- **Preserved prompt.** The lane prompt is preserved at `artifacts/o2/gate1/LANE_PROMPT_O2.md` (SHA-256 `64d9c66b104b288e6ad2ece8b6d54fffd373238156a2c0beebb1fa760ffa3a05`). In it:
  - the consulting authorization is at lines 65–73;
  - the two §P14.4 sentences are at lines 76 and 91;
  - the Gate 1 paragraph is at line 126.

**Advisers.** All three were read-only and were briefed cold, with the authorization quoted verbatim. Each was independent of the others, of this plan's author and of the implementers. Their reports are in the clone's gitignored `artifacts/o2/gate1/`.

| Lens | Agent type | Agent ID | Verdict | Report |
|---|---|---|---|---|
| Architecture | `architecture-reviewer` | `ae4a85c325e322cd0` | **APPROVE**: 0 BLOCKING, 3 NIT | `ADVISER_ARCHITECTURE.md` |
| Testing | `test-strategist` | `a1898718223e9556a` | **APPROVE WITH CHANGES**: 0 BLOCKING, 5 SHOULD, 6 NIT | `ADVISER_TESTING.md` |
| Security / product risk | `product-risk-reviewer` | `adf27f7abe7af2604` | **APPROVE WITH CHANGES**: 0 BLOCKING, 1 SHOULD, 4 NIT | `ADVISER_SECURITY_PRODUCT_RISK.md` |

**Outcome.** All three approved and none raised a BLOCKING finding, so the decision rule is met. This is recorded as a **DELEGATED Gate 1, not the owner's signature**.

The advisers stated these coverage gaps themselves:
- none of them recomputed the hash;
- architecture did not read the §P5 bodies;
- security did not re-read `utils/errors.py` or `CONTRACT_ANALYSIS`;
- testing could not run anything, or test the Linux trace behaviour.

Under the authorization, these verdicts create no evidence. Every §P7 check still has to be run.

**Binding amendments.** The primary session adopted these. Each names its source finding.

1. **GA-1 (testing #1; amends §P7 item 3): mutation check (a) harness.**
   - Copy the harness to `artifacts/o2/mutation-pre/`, and set its interpreter to the clone's absolute `.venv\Scripts\python.exe`.
   - Build the tree from a `git archive` of C2. Target `tests/test_remove_exercise_characterization.py` inside it, and run without `-p tests.conftest`, so that the `tests` package conftest loads normally.
   - Start with an empty `pristine/`, and keep the occurs-exactly-once assertion on every `old` string.
   - **Validity gate, run first:** M00 and M01 must show zero failures *and* zero errors.
   - A kill counts only when a node's outcome is an assertion failure. A mutant "killed" only by collection or import errors is a harness defect to fix.
   - Compare each mutant's killer set with the packet's `runs/mutation/matrix.json`, and explain every difference by a §P5.1 trim.
2. **GA-2 (testing #2; amends §P7 item 5): mutation check (b).**
   - First run an unmutated control, a C3 archive through the same harness, with zero failures and zero errors.
   - Add service-side mutant 8, "swallow": the service body wrapped in `try/except Exception: return None`.
   - Add three route-side mutants, applied to the C3 route text:
     - M05: the 404 message uses the int id;
     - M14: the routine is stripped in the INFO extras;
     - M17: the DEBUG record moves after validation.
   - The "killed by `tests/test_workout_plan_service.py` alone" rule applies only to service-side mutants 1–8. It does not apply to route-side or trace-only (M22-type) mutants.
3. **GA-3 (testing #3; amends §P7 items 2, 9 and 10(b), and §P5.1 item 4): static checks and the AC1 proof.**
   - Before C2 is committed, run pyright 1.1.410 and flake8 (the selection at `ci.yml:119`) on the characterization file. At C3, run both on all four Python files.
   - The AC1 proof becomes: `git diff C2 <final HEAD> -- tests/test_remove_exercise_characterization.py` is empty.
   - If a later edit to that file is unavoidable (the trace fallback, or a reviewer fix), re-verify it in two places:
     - on a `git archive` of the C2 tree, where it must pass on the unmodified route;
     - at the final head.

     Then re-run mutation check (a).
4. **GA-4 (testing #4; amends §P7 item 7 and §P9): additional Chromium coverage.**
   - **Run locally,** in addition to the 25 specs:
     - `listener-cleanup.spec.ts`;
     - `exercise-catalog-fetch.spec.ts`;
     - `workout-plan-desktop-contract.spec.ts`, with `PW_VISUAL_SEED=1`. This is a computed-style/geometry spec, not a screenshot spec.

     A local red in any of these is triaged against base before it is attributed.
   - **Named but not run locally:**
     - `visual-baseline-thumbnails.spec.ts`. It is a screenshot corpus that CI runs only in the weekly `visual-linux` job. Its win32 captures have no CI path and may be stale, and baseline regeneration is owner-only. This slice changes no template, CSS, JS or E2E file.
     - `visual.spec.ts`, evidenced by `visual-windows` on the PR.
   - **Evidenced by their CI jobs:** `program-backup`, `fatigue-context` and `erase-flow`.
   - **Disclosure.** The PR body states this as a disclosed deviation from the literal `/verify-suite` default run, for the owner to see. It does not claim a waiver.
5. **GA-5 (testing #5; amends §P9 and §P13): AC13 evidence in the PR body.**
   - `git rev-parse --git-common-dir`, which must be the clone's own `.git`;
   - no `objects/info/alternates`;
   - `git worktree list`, with a single entry;
   - `len(TEMP)`: 69, within the 103 limit;
   - `git status --short` of the shared checkout, hashed before and after. Paths outside this lane may change because of other sessions; the evidence is that this lane wrote none.
   - nothing from this lane listening on :5000, and the `PW_PORT` that was used.
6. **GA-6 (testing #6; amends §P5.1 item 2).** Keep one first-record assertion, `("DEBUG", "Received data for remove_exercise: [1]")`, in one non-object case.
7. **GA-7 (testing #7; amends §P5.1 item 4).** The failure messages of the trace assertions include `sqlite3.sqlite_version` and `sys.version`. This adds no node and no print. After any trace fallback, re-run check (a).
8. **GA-8 (testing #8; reading of AC6).** "No `BEGIN`" means that no explicit `BEGIN` statement is issued through the handler. The implicit `BEGIN`/`COMMIT` pairs in the trace are sqlite3's per-statement transactions.
9. **GA-9 (testing #9; amends §P7 items 1 and 6).** Run both the baseline and the final full pytest with `--junitxml`, and diff their node-ID sets. The expected delta is exactly the nodes of the two new files. Any other node that is added, removed or changes outcome must be triaged.
10. **GA-10 (testing #10; amends §P7 item 7).** A red at `program-backup.spec.ts:79` is rerun and triaged, not waived.
11. **GA-11 (testing #11; amends §P7).** `tsc` is covered by the required CI `Type Check` job; no TS or JS file changes.
12. **GA-12 (architecture #1; amends §P4).** A third invisible difference, alongside §P4's two:
    - an exception raised inside the `with` now carries one extra traceback frame (`remove_plan_exercise`) in the `exc_info` of `logger.exception`;
    - the `lineno` and `funcName` of the route's INFO and ERROR records shift.

    No test pins traceback text, `lineno` or `funcName`.
13. **GA-13 (architecture #3; amends §P7 item 10(a)).** Also check that `:252-265` and `:301-306` are byte-identical, including the whitespace-only `:259`.
14. **GA-14 (security F1, F2; amends §P9).** The PR text gains two additions:
    - a sentence naming follow-ups 1–4 as pre-existing base behaviour, unchanged by this slice and out of scope:
      - follow-up 1 is unpinned;
      - follow-up 3 is pinned as current behaviour, not endorsed;
      - follow-ups 2 and 4 are recorded;
    - after "No behaviour … change", the parenthetical "(one log-record ordering difference on the 404 path, database-internal records only; see below)".

**Not adopted.**
- **Architecture #2:** no change is needed, and §P11 already records it.
- **Security F3:** already done by the primary session; the lane prompt is preserved with its hash.
- **Security F4:** none requested.
- **Security F5:** already done; the hash was recomputed over both copies, and they are equal.

**Dissent.** None. No adviser blocked.

**What this authorizes.**
- §P14.5 as amended by GA-1…GA-14: S0 and C2–C4 in the clone, within §P1, with the §P7 checks and the §P8 reviews.
- Then, once the local §P7 checks pass, the push and the ready (non-draft) PR, under §P14.4's owner instruction.

It authorizes no merge. The owner approves each merge by PR number and head SHA.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager`, Section 0 (rev 1, 2026-10-19) | not supplied | The rev 1 header (C0) says "The manager supplied no agent ID." The primary O2 session supplied none either. This is a context row; there was no council. |
| `product-manager`, Gate 0 record, rev 2 delta and Plan v1 (revs 2–3, 2026-10-22) | `ae7ed7afd0994c6df` | A fresh `product-manager`, spawned by the primary session of lane O2 of the 2026-10-22 batch. An agent cannot know its own ID. After the agent's first return, the primary session supplied this ID by message to the same agent, which then stamped it here. The agent had no shell: it read files with Read, Grep and Glob, could not compute any SHA-256, and wrote only this file. |
| Decision-packet advisers: route/transaction analyst, characterization-test designer, independent `architecture-reviewer` | not stated in the packet | Advisory inputs dated 2026-10-21 (packet header). They are not council reviewers and not gate signatures. |
| Delegated Gate 1 advisers (rev 4, §P15) | `architecture-reviewer` `ae4a85c325e322cd0`; `test-strategist` `a1898718223e9556a`; `product-risk-reviewer` `adf27f7abe7af2604` | Read-only. Briefed cold by the primary session, with the consulting authorization quoted verbatim. Independent of each other, of the plan's author and of the implementers. Verdicts: APPROVE; APPROVE WITH CHANGES; APPROVE WITH CHANGES; no BLOCKING finding. Reports are in `artifacts/o2/gate1/`. The IDs were supplied by the primary session. The §P15 record was written by `ae7ed7afd0994c6df`, resumed via `SendMessage`. |

**Same product-manager resumed?** **No.** The Section 0 author's ID was never supplied, so it could not be resumed, and a fresh `product-manager` wrote revs 2–3. There was no council, so no question of response-matrix or Plan v2 continuity arises.

**Evidence gap (continuity only).**
> The rev 1 author's agent ID is not in this file and was not supplied to this agent. Revs 2–3 were written by a fresh `product-manager`. It read the committed C0 text in the clone directly, with no paraphrased handoff, and read the decision packet and its evidence files directly. Section 0's raw request, Problem, F1–F9, acceptance criteria, calculation surface, scope, assumptions, questions and rev 1 evidence note are preserved verbatim. Only the header table, the sign-off block and the closing note were replaced. The Revision history, Gate 0 record, rev 2 delta, Plan v1, this section and Sign-off were added. No ID was invented and no completed work was rerun.

**Inputs read** (clone paths):
- `docs/service_extraction/PLANNING.md` (C0 text);
- `artifacts/parallel-next-five/ws4/`:
  - `DECISION_PACKET.md`;
  - `reviewer/ARCHITECTURE_REVIEW.md`;
  - `designer/TEST_DESIGN.md`;
  - `analyst/CONTRACT_ANALYSIS.md`;
  - `designer/draft/test_remove_exercise_characterization.py`;
  - `designer/mutation/mutate.py`;
  - `designer/runs/mutation/summary.txt`;
  - `env.sh`;
- `artifacts/o2/`:
  - `env.sh`;
  - `runs/baseline_draft43.txt`;
  - `msg-c0.txt`;
- source:
  - `routes/workout_plan.py:1-50,245-314`;
  - `utils/supersets.py:220-254`;
  - `utils/database.py:286-370,430-462,495-522`;
  - `utils/errors.py:1-120`;
- tests:
  - `tests/test_superset_service.py:1-50`;
  - `tests/test_utils_package.py`;
  - `tests/test_app_factory.py` (`EXPECTED_BLUEPRINTS`);
- workflow and status documents:
  - `docs/app_factory/PLANNING.md` (structure and Q-WS3-2);
  - `docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`, `QUALITY_GATE.md` and `AUTONOMY.md:1-95`;
  - `CLAUDE.md:1-175`;
  - `docs/OPEN_WORK_EXECUTION_PLAN.md:1-50`;
  - `docs/project_direction/AGREED_PLAN.md` (WS4 lines);
  - `docs/REFACTOR_PLAN.md:1618-1631`;
- configuration:
  - `playwright.config.ts:1-194`;
  - `.github/workflows/ci.yml` (`lint`, `pytest-core`).

The owner decision and the re-verified facts at `155181d6` were supplied by the primary O2 session.

---

## Sign-off

- [x] Gate 0: signed by the owner on 2026-10-22 (Section 0 sign-off block).
- [x] Agent provenance for revs 2–3: `product-manager` `ae7ed7afd0994c6df`, supplied by the primary session. The Gate 1 adviser IDs are added with the Gate 1 record.
- [x] Gate 1: disposed on 2026-10-22 as a DELEGATED Gate 1, not an owner signature (§P15). Plan v1 is bound at `3768e52` (SHA-256 `6e95835d…e328f9`), and GA-1…GA-14 are binding.
- [ ] Implementation C2–C4: only after the Gate 1 record.
- [ ] Push and ready (non-draft) PR: authorized by the owner's direct lane-O2 instruction (§P14.4); done only after Gate 1 and the local §P7 checks; stop once all CI is green on the final head.
- [ ] Merge: owner-only, approved by PR number and head SHA.
