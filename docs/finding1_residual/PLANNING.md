# Plan Review — FINDING-1 residual diagnostics + Testing Strategy D7 README draft

*Shell copied from [`docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md). The council has run: Plan v1 is superseded by Plan v2, and every section below it is filled.*

Worktree: `D:\development\Hypertrophy-Toolbox-v3-main-finding1-d7` · branch `wt/finding1-d7` · base `origin/main` `d583225`.

---

> ## D7 SIGNED 2026-08-21 — the Item 2 draft has LANDED in `README.md`
>
> **Read this before anything below.** Every "D7 is unsigned", "`README.md` is
> not modified", "drafted-but-not-committable" and
> `DRAFT — pending D7 signature, not landed` statement in this document was
> **correct when written** and is now **historical**. The owner signed D7 on
> **2026-08-21**, exactly as recommended — retain the "no in-app restore" stance
> for startup database snapshots, and publish the reviewed manual recovery
> procedure in `README.md`. That procedure is now a live `README.md` section.
>
> The ruling, the scope it authorized, and what it deliberately did **not**
> authorize are recorded in
> [`../TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md) **§8.1d**.
> Nothing below is rewritten: this document is the reviewable artifact the owner
> signed against, and its F1–F7 correction history is why the landed text is
> trusted. Only annotations were added.
>
> **Three wording deltas** were applied when the text was re-verified against the
> implementation at landing time, and are the only differences from the draft
> below: the Backup Center's restore control is named exactly (**Restore To
> Current Plan**); its own generated entries are named by the label the page
> actually shows (**Auto Recovery**); and `DB_FILE`'s precedence over
> `HT_RUNTIME_DIR` is stated. One verified fact was added — the corruption path
> unlinks the `-wal`/`-shm` sidecars *before* renaming the database to
> `database.db.corrupted_<timestamp>` (`utils/database.py:217-231`).

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> Two independent items. Neither needs a browser or port 5000.
>
> ITEM 1 — FINDING-1 residual (docs/LEFTOVERS_BY_PRIORITY.md §4a)
> #384 closed the restore ingress, but rows already poisoned by a pre-fix restore still reach six sites and still raise. Two user-visible problems remain:
>   (a) A bare HTTP 500 on /weekly_summary, /session_summary, /progression and the Excel export, naming no routine and no exercise.
>   (b) Repair through the Plan editor only works in Min Rep -> Max Rep order: routes/workout_plan.py:390-401 re-reads the untouched sibling rep column and feeds it to the validator, so editing Max Rep first returns a 400 naming "Minimum reps" — a field the user did not touch.
>
> GATE 0 — STOP AND REPORT. Propose a diagnostic that names the routine and exercise instead of a bare 500, and a fix for the edit-order trap. HARD CONSTRAINT: your proposal must not change any calculation semantics. Do not modify utils/effective_sets.py, utils/weekly_summary.py, utils/session_summary.py, utils/progression_plan.py, utils/export_service.py or utils/_fatigue/** — mapping a non-numeric rep range onto a number is the explicitly REJECTED option, because it silently changes volume numbers. If your design cannot avoid those files, say so and stop: that is a Large change needing a full council, not this packet.
>
> ITEM 2 — Testing Strategy D7 (docs/TESTING_STRATEGY_PLANNING.md §6)
> D7 is unsigned. Its recommendation is already written: keep the "no in-app restore" stance, but document the manual auto-backup recovery procedure in the README. Draft the README section (verify the real procedure against utils/program_backup.py and the actual data/auto_backup/ layout — do not invent steps), present it, and STOP for the owner's D7 signature. Do not record D7 as signed yourself.
>
> VERIFY: Full pytest. No E2E, no Flask server, no port.
> If you add or remove a test, regenerate docs/test_inventory/TEST_INVENTORY.json and .md as the LAST step.
> OUT OF SCOPE — do not touch: templates/**, static/**, e2e/**, .github/workflows/**, and MASTER_HANDOVER.md / TESTING_STRATEGY_PLANNING.md / LEFTOVERS_BY_PRIORITY.md beyond reading them.
> STOP CONDITION: create the PR, poll CI to zero-pending, mark ready, then STOP. Do not merge.

**Problem**

Two unrelated problems share this packet.

*Item 1.* PR #384 closed the **ingress** for FINDING-1: `restore_backup()` now skips backup items whose rep ranges fail `validate_workout_bounds`, and reports them as `{"routine", "exercise", "reason"}` rows (`utils/program_backup.py:496-511`). It did nothing for rows **already** written into `user_selection` by a restore that ran before the fix. Those rows still flow into six downstream sites. The user-visible residue is that the app fails **anonymously**: a poisoned row anywhere in the plan takes out three whole pages and the Excel export with an error that names neither the routine nor the exercise, so the user has no way to find the row they must repair. And when they do find it, the Plan editor rejects the repair unless they happen to edit the poisoned column first.

*Item 2.* Decision D7 in `docs/TESTING_STRATEGY_PLANNING.md` §6 ("Auto-backup file snapshots: keep 'no in-app restore' stance?" → "Keep, but document the manual recovery procedure in the README") is **unsigned**. §6 states verbatim: *"**D4 and D7 remain unsigned** and no work may act on them."* The user therefore needs the README section **drafted and presented for review**, not landed.

**Measured evidence** (probed empirically on this base; a throwaway pytest probe seeded a poisoned `user_selection` row and hit every surface, then was deleted — the worktree is clean). This table is the packet's ground truth and is not re-derived or softened below.

| Surface | min poisoned | max poisoned | Current message |
|---|---|---|---|
| `GET /weekly_summary` | 500 | 500 | bare error page |
| `GET /session_summary` | 500 | 500 | bare error page |
| `GET /progression` (page) | 200 | 200 | renders fine |
| `POST /get_exercise_suggestions` | 200 | 500 | `Failed to get exercise suggestions` |
| `POST /export_to_workout_log` | 400 | 400 | `Minimum reps must be a finite number.` |
| `GET /export_to_excel` | 500 | 500 | `Failed to export data to Excel.` |

**Three corrections to `docs/LEFTOVERS_BY_PRIORITY.md` §4a.** §4a is out of scope to edit, so the corrections are recorded here instead. A later packet that owns that file should fold them in.

1. **Site 5 is misattributed.** §4a claims `GET /progression` → 500. It does not; that route only runs a `DISTINCT exercise, routine` select and measured 200/200. The real surface is `POST /get_exercise_suggestions` → `utils/progression_plan.py:312` (`target_reps = current_reps + 2`), and it fires **only when `max_rep_range` is poisoned**, because that is the column it reads (`planned_max_reps`). For the record: an initial probe *did* show `/progression` returning 500, but that is an unrelated **test-fixture artifact** — `app.py:133` registers a `datetime` Jinja filter and `tests/conftest.py` does not, so `templates/progression_plan.html:77` raises `TemplateAssertionError` under the test client only. Not a FINDING-1 symptom, and out of scope to fix here.
2. **The edit-order trap is symmetric.** §4a documents only "Min → Max". The measured matrix is: (poisoned = min, edited = min) → 200; (min, max) → 400 `Minimum reps must be a finite number.`; (max, max) → 200; (max, min) → 400 `Maximum reps must be a finite number.` The true rule is **"you must edit the poisoned column first"**, not "Min before Max".
3. **Site 6 returns 400, not 500.** Its message is the canonical validator string, which names the *field* but never the routine or exercise. Separately, site 7 (`utils/weekly_summary.py:323`) was confirmed to be a **silent wrong number**, not a raise: `SELECT ('abc' + 8) / 2.0` evaluates to **4.0** where 7.0 was intended.
4. **Site 7's reachability is overstated by §4a, and Plan v1 repeated the overstatement** (added at council review, `product-risk-reviewer` P1). On all three surfaces where §4a claims the 4.0 "reaches" the user, an **unfiltered** calculation raises **first** and the request 500s before anything renders: `routes/weekly_summary.py:50` runs before `:81`; `routes/session_summary.py:54` runs before `:91`; `utils/export_service.py:317` runs before `:362`. The wrong number is therefore **never rendered** on any of them. The one path that does render it is `GET /session_summary?routine=<a routine containing no poisoned row>` — `_build_plan_query` filters by routine (`utils/session_summary.py:40-42`) while `calculate_isolated_muscles_stats` stays unfiltered (`utils/weekly_summary.py:318-330`) — and the shipped UI never sends a `routine=` parameter (`static/js/modules/session-summary.js:53-57`). So site 7 is **unreachable through the shipped UI and reachable only via a hand-constructed request**. This correction is recorded because a later owner reading §4a or Plan v1 could otherwise authorize a Large `utils/weekly_summary.py` council against a residual the UI cannot reach. Leaving site 7 unfixed remains correct.

**Acceptance criteria**

1. Given a `user_selection` row with a non-numeric `min_rep_range` or `max_rep_range`, when the user loads `/weekly_summary` or `/session_summary`, then the error page still returns HTTP 500 but its message names the offending routine and exercise.
2. Given the same poisoned row, when the user requests `GET /export_to_excel`, then the JSON error still returns HTTP 500 with code `EXPORT_FAILED` and its message names the offending routine and exercise. **Scope note (A3):** this is a JSON-body and log improvement only. `static/js/modules/exports.js:88` catches the failure and shows a hardcoded `showToast('error', 'Failed to export to Excel')`, discarding the server message, and `static/**` is out of scope — so **no user-visible change reaches the Excel toast in this packet**. Accepted residual; UI surfacing is deferred to a `static/**` packet. Site 3 stays in scope because pytest and any API consumer do see the improvement. Contrast: the plan→log site *is* user-visible — `exports.js:110` and `fetch-wrapper.js:213` render `error.message` verbatim into the toast.
3. Given the same poisoned row, when the user requests `POST /export_to_workout_log`, then the response still returns HTTP 400 with code `VALIDATION_ERROR` and its message names the offending routine and exercise in addition to the canonical field string.
4. Given a poisoned `max_rep_range`, when the user requests `POST /get_exercise_suggestions` for that exercise, then the response still returns HTTP 500 with code `INTERNAL_ERROR` and its message names **that** exercise and its routine — not an arbitrary sample of unrelated poisoned rows.
5. **(restated per A1 + B1.)** Given a database with **no** poisoned rows, when any of the four surfaces above is exercised, then the response is **byte-for-byte identical to today**, and no scan runs on any path that succeeds today **or that fails for a non-validation reason** — specifically including `NO_DATA` (`utils/export_service.py:486-488`), which is an empty but perfectly conformant plan. The oracle is a **call counter** monkeypatched into each of the four route modules asserting zero calls, plus the existing strict-equality `assert_error_payload` helper. The original "count-for-count identical query count" half is **dropped**: no query-counting instrument exists repo-wide (`rg "set_trace_callback|query_count|count_queries"` → zero matches), and this packet does not invent one.
5a. **(new, per P2.)** Given a surface that fails but whose scan returns `[]` — a real case: `utils/progression_plan.py:410,417` sources `current_reps` from a `workout_log` row's `planned_max_reps` rather than `user_selection`, and site 6 also validates `weight` and `rir` (`utils/export_service.py:493-501`), so a row blocked on weight yields a 400 the rep-range scanner reports nothing for — then the message is **byte-identical to today's**, and the formatter emits no "no problems found" or equivalent phrasing. A diagnostic that announces it found nothing is worse than today's bare message.
6. Given a poisoned `max_rep_range`, when the user edits **only** Max Rep through the Plan editor to a valid number, then the update succeeds with HTTP 200 (today: 400 `Minimum reps must be a finite number.`).
7. Given a poisoned `min_rep_range`, when the user edits **only** Min Rep to a valid number, then the update succeeds with HTTP 200 (unchanged from today).
8. Given a row whose stored sibling rep value is a valid number, when the user edits the other rep column to a value that violates `min > max`, then the request is still rejected with HTTP 400 `Minimum reps cannot exceed maximum reps.` — the cross-field guard is preserved exactly.
9. Given the user supplies a non-numeric value themselves in the request body, then it is still rejected with the canonical 400 — the fix loosens nothing about user-supplied input.
10. Given Item 2, when the packet finishes, then the README auto-backup recovery section exists **only as a draft committed inside this planning document** under a heading reading `DRAFT — pending D7 signature, not landed`, mirrored in the PR description; `README.md` is not modified on this branch and `docs/TESTING_STRATEGY_PLANNING.md` is not edited to mark D7 signed.
11. Full pytest is green. **The baseline is host-qualified (B5): 2983 passed, 2 skipped, 196.55 s on `d583225`, on Windows.** The same tree collects **2826** on Linux — `TEST_INVENTORY.json:244` gives `collected_deterministic: 2663`, and `tests/test_guard_destructive_command.py` parametrizes 322 nodes on Windows against 163 on ubuntu (`:248-249`); 2663 + 322 = 2985 = 2983 + 2. **Never read a CI count as a regression against 2983.** No E2E, no Flask server, no port.
12. Given the test inventory, when the new test file lands, then `total_files` moves 123 → 124 and `deterministic_files` 122 → 123. `docs/finding1_residual/PLANNING.md` itself does **not** move the inventory — `tests/test_agent_workflow_contracts.py:81-84` parametrizes only `.claude/commands`, `.claude/agents`, `.claude/rules` and `docs/ai_workflow`.

**Calculation surface**

- **`none`.** No calculation function is added, removed, or altered. None of `utils/effective_sets.py`, `utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py`, `utils/export_service.py`, `utils/_fatigue/**` is touched. Sites 1–6 continue to raise on poisoned rows exactly as measured; this packet only **names the cause**. No volume number moves.
- The one behavior change that could be mistaken for a calculation change is Proposal B, so it gets an explicit worked before/after of the **validator input** — not of any computed number:
  - Stored row: `min_rep_range = 'abc'` (poisoned), `max_rep_range = 12`. Request: `{"updates": {"max_rep_range": 10}}`.
    - **Before**: `validate_workout_bounds(min_reps='abc', max_reps=10)` → `"Minimum reps must be a finite number."` → HTTP 400. The row stays poisoned.
    - **After**: the unparsable stored sibling is passed as `UNSET`, so `validate_workout_bounds(min_reps=UNSET, max_reps=10)` → `None` → the `max_rep_range = 10` write proceeds, HTTP 200. `min_rep_range` is left as `'abc'` — **nothing is coerced, defaulted, or mapped onto a number**.
  - Stored row: `min_rep_range = 8`, `max_rep_range = 12`. Request: `{"updates": {"max_rep_range": 5}}`.
    - **Before**: `validate_workout_bounds(min_reps=8, max_reps=5)` → `"Minimum reps cannot exceed maximum reps."` → HTTP 400.
    - **After**: identical — a numeric stored sibling still parses, so it is still passed and still compared. **Byte-identical.**
- **Migration notes** committed to the PR description: (i) the four enriched error messages are a message-text change on already-failing paths — HTTP status codes and the `error_response` JSON envelope keys are unchanged; (ii) `routes/workout_plan.py` relaxes the *stored-sibling* half of the cross-field rep comparison only, never the user-supplied half; (iii) no DB schema change, no data migration, no backfill — poisoned rows stay poisoned until the user repairs them.

**In scope**

- A new read-only diagnostic module `utils/rep_range_integrity.py`.
- Enriched error messages on **four** route files, on paths that are *already* failing: `routes/weekly_summary.py`, `routes/session_summary.py`, `routes/exports.py` (two sites), `routes/progression_plan.py` (`get_suggestions`).
- The edit-order fix at `routes/workout_plan.py:389-401`.
- New/extended pytest coverage for both proposals.
- A **drafted, uncommitted** README auto-backup recovery section for D7, plus the corrections to the brief's own D7 pointers recorded below.
- Regeneration of `docs/test_inventory/TEST_INVENTORY.json` and `.md` as the **last** step, because tests are added.

**Out of scope / non-goals**

- **Site 7's silent wrong number (4.0 where 7.0 was intended) is knowingly left unfixed.** Correcting it means editing `utils/weekly_summary.py:323`, which is the explicitly rejected option. The scanner can *report* the row, but nothing in this packet changes the number. **Severity restated per P1** (Plan v1 called this "the packet's single largest accepted residual risk" — that was an overstatement): it is **unreachable through the shipped UI, and reachable only via a hand-constructed `GET /session_summary?routine=<clean routine>` request**, because every UI-reachable path raises on an unfiltered calculation first. See correction 4 above. It must still be stated in the PR description, but with this reachability qualifier attached.
- **The Excel toast text.** `static/js/modules/exports.js:88` discards the server message; fixing that needs a `static/**` packet. See AC2's scope note.
- Any preflight/eager validation. The scanner runs only inside an `except` block that has already fired (and on site 6's existing `VALIDATION_ERROR` return).
- Any repair, coercion, backfill, quarantine, or auto-deletion of poisoned rows.
- Any change to HTTP status codes. 500/500/500/400 stay exactly as measured; changing them is response-contract drift.
- Editing `docs/LEFTOVERS_BY_PRIORITY.md` §4a, `docs/MASTER_HANDOVER.md`, or `docs/TESTING_STRATEGY_PLANNING.md`.
- Committing the README section, or recording D7 as signed.
- `templates/**`, `static/**`, `e2e/**`, `.github/workflows/**`.
- Fixing the `/progression` test-fixture artifact (missing `datetime` Jinja filter in `tests/conftest.py`).
- Fixing the stale `_attempt_database_recovery` docstring (see Assumptions).

**Assumptions made**

- ⚠️ **The diagnostic must fit inside the existing `error_message` string**, because `templates/error.html` is out of scope. Sites 1 and 2 render `error.html` with `error_message="Unable to load weekly summary."` (`routes/weekly_summary.py:129-134`) / `"Unable to load session summary."` (`routes/session_summary.py:146-151`). The plan therefore appends the offending rows to that string rather than adding a template variable.
- ✅ **RESOLVED at Gate 0 — JSON envelope keys stay unchanged.** `error_response(code, message, status_code, **kwargs)` (`utils/errors.py:67`) accepts extra detail kwargs, so a structured `invalid_rows` key was *available*. The owner confirmed **message-only**, and two reviewers verified the reasoning independently: the kwarg lands as an additive key inside `error` (`utils/errors.py:99`) on four endpoints, which is response-shape drift on a packet that promises none (`architecture-reviewer`), and it would also push the packet to **Large** at plan stage and pull `api-integration.spec.ts` in, contesting the owner's no-E2E constraint (`test-strategist` N9). No longer an assumption.
- ✅ **RESOLVED at Gate 0 — the cap is a hard UI constraint, not invented scope.** `fetch-wrapper.js:213` and `exports.js:110` render `error.message` verbatim into a Bootstrap toast, and `templates/error.html:18` renders `error_message` inside a single `<p>`. The cap stays at **5 named rows plus "(+N more)"**, with the constraint added by A2: **the cap must always retain the causally-implicated row**. Naming five unrelated rows is worse than a bare 500 because it misdirects the repair.
- ⚠️ **Scanner scope is `user_selection` only.** `workout_log` is not scanned. No measured site implicated it, but this is an assumption rather than a proof. P2 shows the consequence directly — `utils/progression_plan.py:410,417` reads `planned_max_reps` off a `workout_log` row, which is why AC5a exists.
- ⚠️ **The scanner inherits a destructive failure mode** (A4). `get_db_connection` calls `_attempt_database_recovery` on a `DatabaseError` matching malformed / not-a-database / encrypted, which **renames the live DB** to `<name>.corrupted_<timestamp>` (`utils/database.py:226-231`). A scanner that opens a fresh connection from inside an already-failing `except` can be the call that triggers that quarantine; `_RECOVERY_ATTEMPTS` (`:204-205`) caps it at one attempt per path per process, which bounds but does not remove the hazard. Mitigation: the module docstring states it, and the scanner is kept out of any handler that already caught a `sqlite3.DatabaseError`.
- ⚠️ **Item 2's producer pointer in the raw request is wrong**, and the plan corrects it: the auto-backup producer is **`utils/auto_backup.py`**, not `utils/program_backup.py`. `program_backup.py` is the in-DB Backup Center (`program_backups` / `program_backup_items` tables, `/api/backups`) — a different feature. Verified facts for the draft, all measured:
  - `create_startup_backup()` copies the live DB via the SQLite **online-backup API** (`src.backup(dst)`, `utils/auto_backup.py:75`) to `<db parent>/auto_backup/database_<YYYYMMDD_HHMMSS>.db`.
  - Called at startup (`app.py:106-108`) but **skipped on a fresh seed / first launch** (`if not database_seeded:`), and again immediately before `/erase-data` (`app.py:256`).
  - Skipped when `TESTING=1`, when the live DB is missing, or when `SELECT COUNT(*) FROM exercises` < `MIN_EXERCISES_TO_BACKUP` = **100** (`utils/auto_backup.py:45-66`).
  - `AUTO_BACKUP_KEEP` = **7**, rotated by mtime (`_rotate`, `:23-34`). The real `data/auto_backup/` folder holds exactly 7 files.
  - Snapshot folder resolution, probed for four configurations: source checkout → `<repo>\data\auto_backup\`; `HT_RUNTIME_DIR` set → `<HT_RUNTIME_DIR>\data\auto_backup\`; `DB_FILE` set → an `auto_backup\` folder **beside that file** (no `data\` segment, because `_backup_dir()` is `live_db_path.parent / "auto_backup"`); frozen Windows build → `%LOCALAPPDATA%\HypertrophyToolbox\data\auto_backup\`.
  - The draft's "delete leftover `-wal` / `-shm` sidecars" step is **not invented**: `utils/database.py:217-224` deletes exactly those two sidecars for exactly this reason when swapping in a replacement DB.
- ⚠️ **Rotation actively destroys recovery material during troubleshooting** (P7 — the most safety-critical Item 2 fact, and the one Plan v1's draft outline was missing). `AUTO_BACKUP_KEEP = 7` and `_rotate` (`utils/auto_backup.py:15,23-34`) delete the oldest snapshot by mtime on **every** startup that takes a snapshot, and the real `data/auto_backup/` folder already holds exactly 7. So every restart during troubleshooting silently destroys one snapshot, **oldest first — the one most likely to predate the problem**. The drafted procedure must therefore front-load "copy the whole folder out before restarting anything". Compounding it: `create_startup_backup()` is skipped when the live DB looks empty (< 100 exercises), so a user whose data is **already** gone gets no protective snapshot either.
- ⚠️ **Incidental finding recorded, not fixed.** `_attempt_database_recovery`'s docstring (`utils/database.py:209`) says it will "restore a safe copy when available", but the code has no such branch — it deletes the sidecars, quarantines the corrupt file to `<name>.corrupted_<timestamp>`, and lets a **fresh empty database** be created (`:236`). The app therefore does **not** auto-recover data on corruption, which is precisely what makes the manual procedure the only recovery path. Out of scope to fix here; worth its own trivial packet.
- ⚠️ **Planning size.** Under [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) this is a bounded **Medium** change by content (no schema, no API-shape, no calculation surface), but the raw request explicitly invokes Gate 0, so it is run as **Large**: Gate 0 + Gate 1 council. Change-type gates are the union of the *Route / API* row (route pytest targets + `tests/conftest.py` blueprint coverage) and the *Business logic* row, and the request pins the verify step at **full pytest** regardless.

**Open questions for the user** — *all four were answered at Gate 0; answers recorded verbatim below and folded into Plan v2.*

1. ~~**Structured detail or message-only?**~~ → **ANSWERED: message-only.** Confirmed independently by two reviewers. An `invalid_rows` kwarg lands as an additive key inside `error` (`utils/errors.py:99`) on four endpoints — response-shape drift on a packet that promises none — and per `test-strategist` N9 it would also make the packet **Large** at plan stage and pull `api-integration.spec.ts` in, contesting the no-E2E constraint. Consequence: `product-risk-reviewer` is **not** additionally required at code time on response-shape grounds.
2. ~~**Row cap.**~~ → **ANSWERED: keep the cap of 5 + "(+N more)"**, and it is no longer invented scope — `fetch-wrapper.js:213` and `exports.js:110` render `error.message` verbatim into a Bootstrap toast, which is the justification. Hard constraint added from A2: **the cap must always retain the causally-implicated row.**
3. ~~**Item 2 delivery.**~~ → **ANSWERED: commit the README draft inside this planning document**, under a heading labeled `DRAFT — pending D7 signature, not landed`, and mirror it in the PR description. A PR body alone is not durable evidence of what was reviewed, and a labeled draft in the packet's own planning doc is not a D7 action. `README.md` still must not be modified.
4. ~~**Data exposure?**~~ → **ANSWERED: no.** Single-user localhost, no auth, and the same routine/exercise strings already appear in `restore_backup()`'s response (`utils/program_backup.py:502-506`) and in progression copy (`utils/progression_plan.py:293,313`).

### Section 0 sign-off — GATE 0
- [ ] User confirms the acceptance criteria match intent.
- [ ] User reviewed the assumptions and corrected or accepted each one.
- [x] Blocking questions are answered. *(All four open questions answered at Gate 0; see the strikethrough answers above.)*

---

## Plan v1

> **Superseded by [Plan v2](#plan-v2).** Left unedited as the historical record of what the council reviewed. All three reviewers returned **Needs revision**; every finding was accepted. Implement from Plan v2, not from here.

**Goal**: When a pre-#384 poisoned rep range breaks a page, the error names the routine and exercise that must be repaired; and repairing it through the Plan editor works whichever rep column the user edits first — with no calculation semantics touched anywhere.

**Scope**

- **In**
  - **Proposal A — diagnose-on-failure, route layer only.** New `utils/rep_range_integrity.py`: a read-only scanner over `user_selection` that imports **only** `utils.database.DatabaseHandler` and `utils.workout_validation.validate_workout_bounds`. It returns the rows failing the canonical contract in the same shape `restore_backup()` already returns — `[{"routine": …, "exercise": …, "reason": …}]`, per the precedent at `utils/program_backup.py:500-506` — plus a formatter that renders that list into a single sentence for an error message. **Critically: the scan runs only inside an `except` block that is already failing**, and on site 6's existing `VALIDATION_ERROR` return. Never as a preflight. On a conformant database zero extra queries run and zero response bytes change.
  - Wiring into **four route files only**:
    - `routes/weekly_summary.py:125-134` — existing `except`; enrich both the XHR `error_response("INTERNAL_ERROR", …, 500)` message and the `error.html` `error_message`. Stays 500.
    - `routes/session_summary.py:142-151` — same shape, same treatment. Stays 500.
    - `routes/exports.py:81-88` — Excel `EXPORT_FAILED` 500; and `routes/exports.py:98-103` — the plan→log `VALIDATION_ERROR` return, where `result.status_code` is honoured unchanged. Stays 500 / 400.
    - `routes/progression_plan.py:200-205` — the `get_suggestions` catch-all `INTERNAL_ERROR`. Stays 500.
  - **Proposal B — the edit-order trap.** At `routes/workout_plan.py:389-401`, the **only** reason the sibling rep column is re-read from the DB is the cross-field `min > max` comparison inside `validate_workout_bounds` (`utils/workout_validation.py:77-80`) — the validator applies no other rule to reps beyond finiteness. Fix: keep the stored sibling for that comparison **only when it parses as a number**; otherwise pass `UNSET`. Fields the user actually supplied stay strictly validated. A numeric stored sibling behaves byte-identically to today. No value is ever coerced, defaulted, or mapped onto a number.
  - Tests for both proposals, plus the regenerated test inventory.
  - Item 2's README draft, produced and presented but **not committed**.
- **Out**
  - Every non-goal in Section 0. In particular: **site 7's silent 4.0-vs-7.0 wrong number stays unfixed**, HTTP status codes stay as measured, and no poisoned row is ever repaired by the app.

**Constraint compliance — stated explicitly.** None of `utils/effective_sets.py`, `utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py`, `utils/export_service.py`, `utils/_fatigue/**` is touched by this plan. Sites 1–6 still raise on poisoned rows; the packet only names the cause. **No volume number moves.** The design does not require any of the forbidden files, so the "say so and stop" escape hatch in the raw request is not triggered.

**Item 2 is BLOCKED pending signature.** `docs/TESTING_STRATEGY_PLANNING.md` §6 states verbatim: *"**D4 and D7 remain unsigned** and no work may act on them."* Landing the README section **is** the D7 action. Item 2 is therefore planned as **drafted-but-not-committable**: the draft is written and presented for the owner's D7 signature, `README.md` is left unmodified on this branch, and D7 is **not** recorded as signed by this packet. A follow-up packet lands the section once the owner signs.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/rep_range_integrity.py` | **new** | Read-only `user_selection` scanner + message formatter. Imports only `DatabaseHandler` and `validate_workout_bounds`. Returns `[{routine, exercise, reason}]`, mirroring `utils/program_backup.py:500-506`. Swallows its own errors — a failing diagnostic must never mask the original failure. |
| `routes/weekly_summary.py` | modify | `:125-134` existing `except` only. Enrich XHR message + `error.html` `error_message`. Status stays 500. |
| `routes/session_summary.py` | modify | `:142-151` existing `except` only. Status stays 500. |
| `routes/exports.py` | modify | `:81-88` (Excel, 500) and `:98-103` (plan→log `VALIDATION_ERROR`, 400). Both already-failing paths. |
| `routes/progression_plan.py` | modify | `:200-205` `get_suggestions` catch-all only. Status stays 500. The `/progression` page handler at `:131-138` is **not** touched — it does not fail. |
| `routes/workout_plan.py` | modify | `:389-401` only. Stored sibling passed to the validator only when it parses as a number, else `UNSET`. |
| `tests/test_rep_range_integrity.py` | **new** | Unit tests: clean DB → `[]`; poisoned min / poisoned max / both; row shape; cap-and-overflow formatting; scanner failure is swallowed. |
| `tests/test_weekly_summary_routes.py` | modify | Poisoned row → 500 **and** message names routine + exercise. Clean DB → response byte-identical. |
| `tests/test_session_summary_routes.py` | modify | Same pair. |
| `tests/test_exports.py` | modify | Excel 500 + named row; plan→log **400** + named row alongside the canonical field string. |
| `tests/test_progression_plan_routes.py` | modify | Poisoned `max_rep_range` → 500 + named row; poisoned `min_rep_range` → still **200** (site 5 reads `planned_max_reps` only). |
| `tests/test_workout_plan_routes.py` | modify | The full 2×2 edit-order matrix: (min,min) 200, (min,max) **200 — was 400**, (max,max) 200, (max,min) **200 — was 400**; plus numeric-sibling `min > max` still 400; plus user-supplied garbage still 400. |
| `docs/test_inventory/TEST_INVENTORY.json` + `.md` | regenerate | **Last step.** Tests are added, so `Test Inventory Drift` will red otherwise. Never hand-edit. Confirm no untracked/gitignored `.md` sits in a globbed surface directory first. |
| `docs/finding1_residual/PLANNING.md` | this file | Council record; also the only home of the three §4a corrections, since §4a is out of scope. |
| `README.md` | **no change** | Item 2's section is drafted and presented for D7 signature, **not committed**. |
| `docs/TESTING_STRATEGY_PLANNING.md` | **no change** | D7 is not recorded as signed by this packet. |
| `docs/LEFTOVERS_BY_PRIORITY.md` | **no change** | Read-only; the §4a corrections live in Section 0 above. |

**Effort**: **M** · **Owner**: implementation agent (this worktree) · **Depends on**: Gate 0 answers to open questions 1 and 3; Item 2's landing depends on an owner D7 signature that this packet must not manufacture.

**Sequence**

1. **Gate 0.** Stop and report Section 0. Do not write code until the owner answers open questions 1 and 3.
2. Re-confirm the baseline is still green on this worktree if any time has passed (`d583225`: 2983 passed, 2 skipped, 196.55 s).
3. Write `utils/rep_range_integrity.py` and `tests/test_rep_range_integrity.py`. Run that one file.
4. Wire Proposal A into `routes/weekly_summary.py` and `routes/session_summary.py`; extend their two route test files. Run both.
5. Wire Proposal A into `routes/exports.py` (both sites) and `routes/progression_plan.py` (`get_suggestions` only); extend `tests/test_exports.py` and `tests/test_progression_plan_routes.py`. Run both. Assert the plan→log site is **400**, not 500.
6. Apply Proposal B at `routes/workout_plan.py:389-401`; extend `tests/test_workout_plan_routes.py` with the full 2×2 matrix plus the two preservation cases. Run that file.
7. Mutation-check Proposal B in **both directions** before believing the tests: revert the guard and confirm the two new matrix cases red; then re-apply and confirm the `min > max` preservation case still reds if the sibling is dropped unconditionally. A test that passes under both variants proves nothing.
8. Confirm the zero-cost claim empirically: on a clean DB, assert the four surfaces' responses are unchanged and the scanner is never entered (patch it to raise and confirm the happy paths still pass).
9. Draft the Item 2 README section against the verified facts in Section 0's assumptions. Do **not** touch `README.md`; do **not** edit `docs/TESTING_STRATEGY_PLANNING.md`.
10. **Full pytest.** No E2E, no Flask server, no port. Compare against the 2983/2 baseline; the pass count should rise only by the tests added.
11. **Last step:** `python scripts/generate_test_inventory.py`, commit the regenerated `docs/test_inventory/TEST_INVENTORY.json` and `.md`.
12. Create the PR. Its description carries the migration notes, the three §4a corrections, the knowingly-unfixed site 7 residual, the Item 2 draft, and the two incidental findings (the `/progression` fixture artifact and the `_attempt_database_recovery` docstring).
13. Poll CI to **zero pending** (the count grows 17→18 mid-run — poll, do not sample once). Mark ready. **STOP. Do not merge.**

**Expected gates** — superseded; see [Plan v2's filled block](#expected-gates).

---

## Agent provenance

*Required for every council run. The manager records each agent ID returned by its `Agent(...)` call and supplies the `product-manager` its own ID back, because an agent cannot know its own ID. The `product-manager` stamps the IDs the manager supplies — **never invent an ID**, never rerun completed council work to manufacture continuity, and record an unrecoverable ID as an evidence gap.*

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a3157fc0d7cdde344` | Author of Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `a3157fc0d7cdde344` | Author of the matrix and Plan v2 — the same agent, resumed. |
| `architecture-reviewer` | `ab088d21cbe0e4f29` | Step 2 reviewer. Verdict: **Needs revision** (A1–A3 blocking). |
| `test-strategist` | `a14b6cfdb6a819433` | Step 2 reviewer. Verdict: **Needs revision** (B1–B5 blocking). |
| `product-risk-reviewer` | `a938a67e33a7811ee` | Step 2 reviewer. Verdict: **Needs revision** (P1–P3, P7 blocking). |

**Same product-manager resumed for the matrix + Plan v2?** `yes` — resumed via `SendMessage` to the Plan v1 agent ID `a3157fc0d7cdde344`.

**Evidence gap**: `none`.

---

## Reviewer findings

*Run [`.claude/commands/council-plan.md`](../../.claude/commands/council-plan.md) step 2 — three agents in parallel. Paste each agent's output verbatim below. Do not summarize. Head each section with the reviewer's agent ID, matching the Agent provenance table.*

**All three reviewers returned `Needs revision`.**

*Provenance note: the three reviewers ran in the manager's context. The manager pasted each agent's own output below without rewording. Dispositions are **not** mixed into this section — they live in the Response matrix. An earlier revision of this section carried the manager's disposition-annotated relay instead of the reviewers' own text; that has been replaced with the verbatim output.*

### architecture-reviewer (agent `ab088d21cbe0e4f29`)

**Verdict: Needs revision.**

#### Blocking

**Plan v1 → Scope → `routes/exports.py:98-103`; AC5 (line 61) — the "zero extra queries on a conformant database" claim is false at this site.**
`if not result.ok:` is not an exception path. `utils/export_service.py:486-488` returns `PlanExportResult(False, "No exercises to export", "NO_DATA", 400)` for an **empty but perfectly conformant** plan, which is the common case for a fresh DB and for most `clean_db`-fixture tests. Wiring the scanner into that branch unconditionally makes every empty-plan export run an extra full `user_selection` scan.
  Risk: AC5's "count-for-count identical to today" and Plan v1's "On a conformant database zero extra queries run" are both falsifiable on day one. Worse, Sequence step 8 ("patch it to raise and confirm the happy paths still pass") is structurally blind to this — the empty-plan 400 is not a happy path, so the plan's own verification cannot catch its own broken claim.
  Fix: gate the site-6 enrichment on `result.code == "VALIDATION_ERROR"` (leaving `NO_DATA` untouched), and restate AC5 as "no extra query on any path that succeeds today, and none on a non-validation failure."

**AC4 (line 60) + Assumption "row cap = 5" (line 106) vs `routes/progression_plan.py:200-205` — a whole-table scan with a 5-row cap cannot guarantee it names *the* offending row.**
At site 4 the causal row is known exactly: it is the exercise in the request body (`exercise`, bound at `routes/progression_plan.py:156`), and `get_exercise_plan_defaults` reads a single `user_selection` row for it (`utils/progression_plan.py:22-36`). At site 6 the causal row is the first row failing the loop at `utils/export_service.py:492-501`. An unfiltered table scan truncated at 5 can omit both.
  Risk: on a DB with more than five poisoned rows, AC4/AC3 fail — the message names five rows, none of which is the one that broke this request, which is strictly worse than a bare 500 because it misdirects the repair.
  Fix: filter the scan by the request's `exercise` at site 4, and require the cap to always retain the causally-implicated row at sites 3/6.

**AC2 (line 58) vs `static/js/modules/exports.js:88` — the enriched Excel message is discarded before the user ever sees it.**
`exportToExcel` reads the JSON body and re-throws (`:55-57`), then its own `catch` shows a hardcoded toast: `showToast('error', 'Failed to export to Excel')` (`:88`). The server message is dropped. `static/**` is out of scope for this packet, so it cannot be fixed here. (Contrast: the plan→log site is fine — `exports.js:110` and `fetch-wrapper.js:213` both render `error.message` verbatim.)
  Risk: the Problem statement's premise — "the user has no way to find the row they must repair" — remains true for `/export_to_excel` after the packet ships; AC2 passes in pytest while delivering nothing user-visible.
  Fix: state this explicitly in Section 0 as an accepted residual (diagnostic reaches the JSON body and the log only, UI surfacing deferred to a `static/**` packet), or drop site 3 from scope.

#### Non-blocking

**Artifacts → `utils/rep_range_integrity.py` ("Swallows its own errors") vs `utils/database.py:271-276` — swallowing does not undo a destructive side effect.**
`get_db_connection` calls `_attempt_database_recovery` on a `DatabaseError` matching "malformed"/"not a database"/"encrypted", which **renames the live DB to `<name>.corrupted_<ts>`** (`utils/database.py:226-231`) before the exception propagates. A scanner that opens a *new* connection from inside an already-failing `except` can be the call that triggers that quarantine. `_RECOVERY_ATTEMPTS` (`:204-205`) caps it at one attempt per path per process, so the exposure is narrow, but the plan should say so.
  Risk: a read-only diagnostic acquires a destructive failure mode on exactly the DB state it is meant to describe.
  Fix: note in the module docstring that the scanner opens a fresh `DatabaseHandler` and inherits the corruption-recovery path, and keep it out of any handler that already caught a `sqlite3.DatabaseError`.

**Plan v1 line 139 ("rows failing the canonical contract") vs `utils/workout_validation.py:64-80` — calling `validate_workout_bounds` verbatim over-reports.**
The validator also returns "Minimum reps cannot exceed maximum reps." (`:79-80`) and the weight/RIR range messages (`:64-75`). None of those conditions causes the 500s at sites 1/2/4 — arithmetic on numeric-but-inverted reps succeeds.
  Risk: the diagnostic names a numerically valid row as the cause of a failure it did not cause.
  Fix: restrict the scanner to the finiteness check on `min_rep_range` / `max_rep_range`, or carry the validator's own message through as `reason` so the user can tell the two classes apart.

**Plan v1 → `routes/progression_plan.py:200-205` — only the `INTERNAL_ERROR` arm is wired; the `ValueError` arm at `:191-199` is not.**
The measurement holds today (`current_reps + 2` at `utils/progression_plan.py:312` raises `TypeError` on a string), so this is correct as written.
  Risk: if any future poisoned-value shape raises `ValueError`, it lands on `:199` as a 400 with no diagnostic and no test covering the gap.
  Fix: one sentence in the plan recording that the 400 arm is deliberately unenriched because no poisoned shape reaches it.

**Artifacts → `utils/rep_range_integrity.py` — the module's logger is unspecified.**
Root `CLAUDE.md` §3 requires `get_logger()` from `utils/logger.py`, and "swallows its own errors" implies it logs them.
  Risk: an implementation agent reaches for `logging.getLogger(__name__)` or a bare `pass`.
  Fix: add "`logger = get_logger()`; swallowed exceptions go to `logger.exception`" to the artifact row.

**Assumption line 106 (row cap) — the cap is a hard UI constraint, not a style choice.**
`fetch-wrapper.js:213` and `exports.js:110` render `error.message` verbatim into a Bootstrap toast. That is supporting evidence for Open Question 2: cap it. The plan currently presents the cap as invented scope with no justification.

#### Verified clean — no action

- **Module boundaries.** `utils/rep_range_integrity.py` importing only `utils.database.DatabaseHandler` and `utils.workout_validation.validate_workout_bounds` is utils→utils; no `from routes.X import` anywhere in the plan; all four route files already import only from `utils/`. DB access is via the `DatabaseHandler` context manager. No `utils/__init__.py` re-export is proposed. Root `CLAUDE.md` §2 satisfied.
- **Registration triples / schema.** No new blueprint and no new table, so the triple and the creator-helper rule are N/A. All five touched blueprints are already wired at `tests/conftest.py:218-230` (`weekly_summary_bp`, `session_summary_bp`, `exports_bp`, `workout_plan_bp`, `progression_plan_bp`).
- **Status codes and envelope.** Every cited site already returns through `error_response()` (`routes/weekly_summary.py:128`, `routes/session_summary.py:145`, `routes/exports.py:84-88`, `:99-103`, `routes/progression_plan.py:205`), which builds the fixed `{ok, status, message, error:{code, message, requestId}}` envelope at `utils/errors.py:91-101` and returns `(jsonify(...), status_code)`. Message-only enrichment changes no key and no status. The XHR/HTML split at `routes/weekly_summary.py:127-134` and `routes/session_summary.py:144-151` is correctly identified — both arms need the enrichment, and the HTML arm's `error_message` is the only channel available without touching `templates/error.html`. **Open Question 1: message-only is the right call** — an `invalid_rows` kwarg would land as an additive key inside `error` (`utils/errors.py:99`) on four endpoints, which is response-shape drift on a packet that promises none.
- **`routes/workout_plan.py` update path — nothing persisted changes.** `bounded_updates` (`:387`) and the UPDATE-building loop (`:411-414`) apply the identical `valid_fields` filter, and no value read at `:389-401` ever reaches `params`. Proposal B alters validator input only; the claim is accurate. The cross-field guard is protected by the existing `tests/test_workout_plan_routes.py:571-585` parametrization, whose `{"min_rep_range": 13}` case depends on the stored numeric max still being read. And `min_rep_range INTEGER NOT NULL` / `max_rep_range INTEGER NOT NULL` (`utils/db_initializer.py:189-190`) makes the NULL-sibling branch (`utils/workout_validation.py:57-58`) unreachable, so "numeric → pass, else `UNSET`" has no unhandled third case.
- **Shared-state.** No edit to `app.py`, any `CLAUDE.md`, `.claude/settings.json`, `docs/MASTER_HANDOVER.md`, or `.gitignore`; the plan declares those explicitly as no-change.

### test-strategist (agent `a14b6cfdb6a819433`)

**Verdict up front.** The plan is substantially sound — its route/test mapping is real (every file it names exists), its `/progression` fixture-artifact claim is verifiable, and its no-E2E stance does **not** conflict with the change-type table. But five things block: one proposed oracle is provably vacuous, one required CI gate is unmentioned, the last mandatory step has an unverified prerequisite, and the baseline number is host-specific.

#### BLOCKING

**B1 — Sequence step 8's zero-cost oracle is defeated by the plan's own design. Vacuous as written.**

`PLANNING.md:159` specifies the scanner "**Swallows its own errors** — a failing diagnostic must never mask the original failure." `PLANNING.md:188` then proposes to prove the scanner never runs on a clean DB by "patch it to raise and confirm the happy paths still pass."

Those two are contradictory. If the scanner swallows its own exceptions, the happy paths pass whether the scanner was entered or not. The test cannot distinguish "never called" from "called and swallowed" — it is green under both hypotheses, so it proves nothing.

Also, acceptance criterion 5 (`PLANNING.md:61`) claims "**count-for-count identical**" query counts, but there is no query-counting oracle anywhere in the repo: `rg "set_trace_callback|query_count|count_queries"` across the whole worktree returns **zero matches**. The claim currently has no instrument at all.

Required resolution — two separate oracles:
- *Not-called*: monkeypatch the scanner symbol **as imported into each route module** with a counter (`calls.append(1)`) and assert `calls == []` after a clean-DB request to each of the four surfaces. A raise-patch is not a substitute.
- *Zero extra queries*: build one, since none exists — `sqlite3.Connection.set_trace_callback` on the handler's connection, asserting the clean-path statement count is equal before and after the change. Or drop criterion 5's query half and keep only the byte-identity half, which **is** already instrumented (see N1).

**B2 — Four derived pytest targets are missing from the Artifacts table, one of which directly exercises the changed lines.**

Per QUALITY_GATE.md:99 (`routes/X.py` → `tests/test_X_routes.py`, then `tests/test_X.py`, plus rg hits):

- `tests/test_error_page_contract.py:18-83` — parametrized over `/weekly_summary`, `/session_summary`, `/progression`; forces the exact `except` blocks the plan edits and asserts `expected_message.encode() in response.data` (`:82`). It is a substring assertion so appending will not red it, but it is the *only* existing test that renders `error.html` for real on those two routes.
- `tests/test_program_backup_restore_fuzz.py:245,283,360,542` — hits `GET /weekly_summary` expecting 200 four times on non-poisoned data. This is the ready-made **negative control** for criterion 5 and the plan does not cite it.
- `tests/test_downstream_normalization.py`, `tests/test_trailing_slash_routing.py` — rg hits on `/weekly_summary` and `/session_summary`.
- `tests/test_weekly_summary.py`, `tests/test_session_summary.py` — the second-choice derivation targets.

For `routes/exports.py`, rg adds `tests/test_workout_log_routes.py`, `tests/test_ui_flows.py`, `tests/test_erase_data_guard.py`.

**B3 — The pyright baseline gate is unmentioned and is a required check.**

QUALITY_GATE.md:52 and :69-70: `scripts/pyright_baseline_diff.py` "is repo-wide, not per-path: run it when the diff touches any `.py`. No glob narrows it." The check name is `Type Check (tsc blocking + pyright measure-only)` and only the *count* step is measure-only — the baseline diff beside it is blocking.

This plan adds one new `.py` module and edits five more plus six test files. A brand-new module is exactly where net-new diagnostics appear (`DatabaseHandler` row access, `Optional` returns from `fetch_all`). The plan mentions no type-check step at any point in its 13-step sequence. Add it before step 12.

**B4 — Step 11 has an unverified hard prerequisite, and it is sequenced last, where failure is most expensive.**

`scripts/generate_test_inventory.py:72-79` calls `_npx()`, which raises `SystemExit` if `npx` is not on PATH, and `:90-98` shells out to `npx playwright test --list`. Regeneration therefore **cannot run without a working `node_modules` in this worktree**, and `node_modules/@playwright/test/package.json` does not resolve here by glob. Worktrees junction to main's `node_modules` and that junction is a known-fragile surface.

Two consequences the plan must state:
1. Verify `npx playwright test --list --project=chromium` returns non-empty at **step 2**, not step 11. If it fails at step 11 you have a complete implementation and a red required check with no path forward inside the branch.
2. **This does not violate the owner's constraint.** The script's own docstring (`:83`) says "Lists only; starts no browser or server." `--list` binds no port and starts no Flask server. An implementer reading "no E2E, no Flask server, no port" literally will be tempted to skip the mandatory regeneration — say explicitly that `--list` is permitted.

**B5 — The 2983/2 baseline is a Windows-only number and step 10's comparison will not reproduce in CI.**

`docs/test_inventory/TEST_INVENTORY.json:244` records `collected_deterministic: 2663` across `deterministic_files: 122`, plus `tests/test_guard_destructive_command.py` which is explicitly environment-dependent (`:248-249`): **322 on Windows, 163 on ubuntu**.

2663 + 322 = 2985 = 2983 passed + 2 skipped. The plan's baseline reconciles exactly — on Windows. On the Linux runner the same tree collects 2663 + 163 = **2826**. Step 10's "the pass count should rise only by the tests added" is only valid same-host. State the host with the number, and never read a CI count as a regression against 2983.

Other things that move the count, none of which the plan flags:
- `total_files: 123` → 124 and `deterministic_files: 122` → 123 when `tests/test_rep_range_integrity.py` lands. Test Inventory Drift **is** implicated, on the "per-file pytest node counts" surface (QUALITY_GATE.md:58). The plan's step-11-last ordering is correct.
- `docs/finding1_residual/PLANNING.md` does **not** move it. `tests/test_agent_workflow_contracts.py:81-84` parametrizes only over `.claude/commands`, `.claude/agents`, `.claude/rules` and `docs/ai_workflow` — `docs/finding1_residual/` is outside all four. QUALITY_GATE.md:62's "parametrized configuration surface" row is not triggered.
- Regenerating while an untracked `.md` sits in one of those four globbed directories bakes it into the artifact (QUALITY_GATE.md:51). The plan already carries this warning at `PLANNING.md:171` — good, keep it.

#### NON-BLOCKING

**N1 — The byte-identity oracle for criterion 5 already exists on the XHR path; cite it and do not weaken it.**

`tests/test_weekly_summary_routes.py:36-41` and `tests/test_session_summary_routes.py:34-39` define `assert_error_payload` with **strict equality**:

```python
assert payload["message"] == message
assert payload["error"]["message"] == message
```

Used at `test_weekly_summary_routes.py:353-367` and `test_session_summary_routes.py:361-376`, which patch the calculator to raise and then pin `"Unable to fetch weekly summary"` / `"Unable to fetch session summary"` exactly. Any unconditional suffix on the clean path reds both immediately. That is criterion 5's byte-identity half, already instrumented and free.

The failure mode to pre-empt: an implementer hitting a red there will be tempted to relax the equality to `in`. **That silently destroys the guarantee.** Add an explicit instruction not to touch `assert_error_payload`.

**N2 — The HTML path has no message tripwire at all; the new node must not be a status assertion.**

`tests/test_weekly_summary_routes.py:369-378` (`test_html_error_response`) patches `render_template` wholesale and asserts only `status_code == 500`. It is blind to `error_message`. A new node modelled on it would be vacuous — 500 is what the route returns today.

The enriched-HTML assertion must either inspect `mock_render.call_args.kwargs["error_message"]`, or render for real and assert on `response.data` the way `test_error_page_contract.py:82` does. And it needs a **paired negative**: same request, clean DB, assert the routine name is *absent* from the body. Without the negative, a fixture whose routine name happens to collide with boilerplate makes the positive unfalsifiable.

**N3 — There is a documented precedent for exactly this bug class: new code inside an `except` block.**

`tests/test_fatigue_routes.py:13-14`: *"is_xhr_request() takes zero arguments; the route previously called is_xhr_request(request), which raised TypeError inside the except."* This plan inserts new code into **four** except blocks. The `PLANNING.md:159` swallow is the right mitigation, but it needs its own node: force the scanner to raise, assert each of the four surfaces still returns its **original** status and its **original** message. That node is also the only honest way to test the swallow — and it is a different test from B1's not-called node.

**N4 — Two of four edit-order matrix cells are already green; mutation-check per cell, not per file.**

`PLANNING.md:170`: (min,min) 200 and (max,max) 200 pass today. Only (min,max) and (max,min) are new behavior. Step 7's both-directions mutation (`PLANNING.md:187`) is correct in principle but must be asserted **cell by cell** — a file-level "the tests red" observation is satisfied by the two pre-existing cells and proves nothing about the fix.

**N5 — Proposal B silently forks `_number()`'s semantics unless it reuses it.**

`utils/workout_validation.py:18-28` — `_number()` rejects `bool` before `float()` and rejects non-finite values. If `routes/workout_plan.py:389-401` decides "parses as a number" with a bare `float(x)`, then a stored `True` becomes `1.0` and `float('inf')` becomes a valid sibling, both of which the validator would have rejected. `PLANNING.md:145`'s "a numeric stored sibling behaves byte-identically to today" is only true if the same predicate is used. Add a node covering a stored non-finite / bool-typed sibling, or reuse `_number` (it is module-private, so importing it is a deliberate coupling decision worth stating).

**N6 — E2E: no conflict, and the closest coupling is safe.**

No `templates/**`, `static/**`, `scss/**` or `e2e/**` path is touched, so the Frontend, CSS and E2E-spec rows (QUALITY_GATE.md:29-33) never fire and the feature map (`:111-123`) is not consulted. The owner's no-E2E constraint requires **no** waiver.

The nearest coupling is `e2e/program-backup.spec.ts:258,277`, which asserts `'Minimum reps must be a finite number.'` — but that string is produced by `restore_backup()` via `validate_workout_bounds`, and the plan touches neither `utils/program_backup.py` nor `utils/workout_validation.py`. Not implicated. The known-red `e2e/program-backup.spec.ts:79` (QUALITY_GATE.md:183) is likewise not implicated.

Caveat to hold: if open question 1 is answered "add the `invalid_rows` kwarg", the API-shape row of the feature map (`:122` → `api-integration.spec.ts`) starts to matter and the no-E2E constraint becomes contested. Message-only keeps it clean.

**N7 — Conftest: no work required, and the plan should say so explicitly.**

`tests/conftest.py:218-230` already registers all five affected blueprints (`weekly_summary_bp`, `session_summary_bp`, `exports_bp`, `workout_plan_bp`, `progression_plan_bp`). No new blueprint, no new table, so no `app` fixture or `erase_data()` change. QUALITY_GATE.md:26's "blueprint-registration coverage in `tests/conftest.py`" is satisfied as-is. `PLANNING.md:116` invokes that clause without resolving it — resolve it to "none".

**N8 — Correction 1's mechanism checks out exactly.**

`app.py:133` `@app.template_filter('datetime')`; `templates/progression_plan.html:77` `{{ goal.goal_date|datetime('%d-%m-%Y') }}`; `tests/conftest.py:234` registers only `safe_media_path`. The plan's dismissal of the `/progression` 500 as a fixture artifact is verified, not asserted. Note the consequence it does not draw: **no pytest node can ever exercise the `/progression` success page with goal rows present** until conftest gains that filter. If any proposed node depends on that page rendering, it is unrunnable.

**N9 — Open question 1 has a gate consequence, not just a design one.**

QUALITY_GATE.md:26 makes `product-risk-reviewer` a required code-time reviewer "if response shape changes." Adding `invalid_rows` to four endpoints is a response-shape change on four endpoints, which also re-reads as **Large** at plan stage under `:14`. `PLANNING.md:120` calls this "blocking" for the reviewer question — correct; it is also blocking for the planning size. Message-only keeps the packet where `PLANNING.md:116` puts it.

### product-risk-reviewer (agent `a938a67e33a7811ee`)

**Verdict: Needs revision.** The calculation-semantics constraint is genuinely honored — I verified it rather than taking the plan's word. The revisions are the accuracy of the site-7 residual record, the unspecified empty-scan message, the scanner-predicate mismatch at site 6, and the missing "copy the snapshots out before restarting" step in the README draft.

First, the thing the plan gets right, verified rather than assumed: **the hard constraint holds.** `utils/workout_validation.py:77-80` confirms the validator's only rep rules are finiteness and `min > max`, so Proposal B's premise ("the sibling is re-read for the cross-field comparison and nothing else") is exact, not approximate. The proposed scanner's two imports (`DatabaseHandler`, `validate_workout_bounds`) pull in no forbidden module transitively — `utils/workout_validation.py:1-12` imports only `math`, `typing`, and `utils.constants`. No calculation file, and nothing under `utils/_fatigue/**`, is reached directly or indirectly. Acceptance criterion 5 (zero extra queries on a conformant DB) is achievable as designed. That part is sound.

#### Blocking

**Section 0 "Three corrections" / "Out of scope" (:53, :92) — site 7's reachability is misstated, and the plan inherits the error it set out to correct.**
- Invariant at risk: CLAUDE.md §1 "Refactor invariant" — this document is declared "the packet's ground truth" and the only home of the §4a corrections, so a wrong fact here governs a future calculation-file packet.
- I traced all three surfaces `docs/LEFTOVERS_BY_PRIORITY.md:676` claims the 4.0 "reaches". On every one of them an **unfiltered** calculation raises before `calculate_isolated_muscles_stats()` is ever called: `routes/weekly_summary.py:50` before `:81`; `routes/session_summary.py:54` before `:91`; `utils/export_service.py:317` before `:362`. The wrong number is therefore never rendered on any of them. The one path that does render it is `GET /session_summary?routine=<a routine with no poisoned row>` — `_build_plan_query` filters plan rows by routine (`utils/session_summary.py:40-42`) while `calculate_isolated_muscles_stats` is unfiltered (`utils/weekly_summary.py:318-330`), so the 200 page shows a poisoned row's contribution at `templates/session_summary.html:177`. The shipped UI never sends `routine=` (`static/js/modules/session-summary.js:53-57` sends `contribution_mode` only), so this is a hand-typed-URL path.
- Risk: **leaving site 7 unfixed is the correct call** — but the plan justifies it as "the packet's single largest accepted residual risk," which is false in the inflating direction. A later owner reading this record will authorize a Large `utils/weekly_summary.py` council against a residual that the shipped UI cannot reach.
- Fix: add correction #4 to Section 0 stating the measured reachability above, and restate the residual as "unreachable through the shipped UI; reachable only via a hand-constructed `?routine=` request."

On your question "is there anything the packet could legitimately do about it without touching a forbidden file?" — yes, two things, and only the first is worth doing. (a) Record the correction above; free, already in scope. (b) The packet *could* run the scanner and emit a `logger.warning` from `routes/session_summary.py` when `routine` is present, which touches no forbidden file, no template, and no response shape — but it adds a query on a conformant DB and so contradicts acceptance criterion 5. Given (a) shows the path is UI-unreachable, I'd take (a) and decline (b).

**Acceptance criteria 1-4 (:57-60) — no criterion covers "the surface failed but the scan found nothing."**
- Invariant at risk: CLAUDE.md §1 "Refactor invariant" — message-text change on four workflows without a specified degenerate case.
- Two concrete paths produce it. First, `utils/progression_plan.py:410,417` sources `current_reps` from a `workout_log` row's `planned_max_reps`, not from `user_selection`; the plan's own assumption (:107) flags `workout_log` as unscanned "an assumption rather than a proof." Second, site 6 at `utils/export_service.py:493-501` validates `weight` and `rir` as well as the rep range, so a row blocked on weight yields a 400 that a rep-range scanner reports nothing for.
- Risk: the user gets a 500/400 accompanied by a diagnostic that says nothing was found — actively worse than today's bare message, because it tells them the app checked and the data is fine.
- Fix: add an acceptance criterion — when the scan returns `[]`, the message is byte-identical to today's, and the formatter emits no "no problems found" phrasing.

**Artifacts row `utils/rep_range_integrity.py` (:159) / Scope In (:139) — the scanner's predicate is not pinned to each call site's actual validator invocation.**
- Invariant at risk: CLAUDE.md §1 "Refactor invariant" (silent divergence between what the app rejects and what it reports).
- `utils/export_service.py:493-498` calls `validate_workout_bounds(..., allow_null=True)`, which maps `""` onto null and accepts it (`utils/workout_validation.py:54-56`). A scanner using the default `allow_null=False` diverges in both directions: it flags a `min_rep_range=''` row that site 6 accepts, and misses a row site 6 blocks on `weight`/`rir`. `''` is reachable — `min_rep_range INTEGER NOT NULL` (`utils/db_initializer.py:189-190`) rejects NULL but not the empty string.
- Risk: the 400 names a field the row didn't fail on, or names rows unrelated to the failure — reintroducing the "names a field the user did not touch" confusion the packet exists to remove.
- Fix: specify that the scanner reproduces each wiring site's exact `validate_workout_bounds` call (fields and `allow_null`), rather than one canonical scan shared by all four sites.

#### Non-blocking

**Plan v1 Scope In, Proposal B (:145) — "parses as a number" is a weaker predicate than the validator's.**
- Risk: if the parse test is a bare `float()`, a stored `'nan'`/`'inf'` parses but `math.isfinite` (`utils/workout_validation.py:26-27`) still returns "must be a finite number", so the edit-order trap survives for those values while the plan claims it is closed.
- Fix: define the predicate as "pass the stored sibling only when `validate_workout_bounds` accepts it in isolation," which is exact, self-maintaining, and settles `''` and `None` by construction.

**Proposal B's own risk — I assessed it and it does not admit a genuinely bad state.** The relaxation fires only when the sibling is already outside the contract, i.e. the row is already invalid; no numeric `min > max` pair can be created because the surviving half is not a number. AC 8 and 9 pin both preservation directions and Sequence step 7's two-direction mutation check is the right guard. One coupling to record in the migration notes: the `(min poisoned, max edited)` case moves 400 → 200, which removes the user's only current signal (`"Minimum reps must be a finite number."`) and replaces it with "Exercise updated successfully" on a row that still 500s the Analyze pages. That is acceptable *only* because Proposal A ships in the same PR and its `reason` string names the field. Proposal B must not land without Proposal A.

**Assumptions (:104-106) — the literal diagnostic copy is never drafted, so Gate 0 cannot review it.** Two specific hazards to pin before code: rows with a falsy `routine` must render as **Unassigned**, the established vocabulary at `utils/weekly_summary.py:24` and `utils/session_summary.py:90` — a raw read of `user_selection.routine` prints an empty string; and `templates/error.html:18` renders `error_message` in a single `<p>`, so five routine/exercise pairs plus "(+N more)" must read as one sentence. Terminology is otherwise clean: reusing the validator's own "Minimum reps"/"Maximum reps" strings avoids inventing a synonym, and **Routine** / **Exercise** are canonical.

**Item 2 (:108-115) — the drafted recovery procedure is missing the one step that can destroy the user's recovery material.** `AUTO_BACKUP_KEEP = 7` (`utils/auto_backup.py:15`) and `_rotate` (`:23-34`) delete the oldest snapshot by mtime on **every** startup, and the plan's own probe records that the real folder already holds exactly 7 files. Every app restart during troubleshooting therefore silently destroys one snapshot, oldest first — the one most likely to predate the problem. The draft must instruct: stop the app; copy the entire `auto_backup/` folder outside the runtime tree **before** restarting anything; rename rather than overwrite the current `database.db`; then delete `-wal`/`-shm` sidecars *before* copying the snapshot into place. Everything else in the plan's fact list I verified as accurate — `_backup_dir` is `live_db_path.parent / "auto_backup"` (`:19-20`), the `<100 exercises` skip (`:16,:59-66`), `src.backup(dst)` (`:75`), and the sidecar precedent at `utils/database.py:217-224`. Two facts worth adding to the draft: `create_startup_backup()` is skipped when the DB looks empty, so a user whose data is already gone gets no protective snapshot; and `_attempt_database_recovery` (`utils/database.py:208-237`) does not restore data despite its docstring, which the plan already caught (:115) and which is the strongest argument for the section existing.

**Item 2's D7 gating is the correct call.** I verified the quote verbatim at `docs/TESTING_STRATEGY_PLANNING.md:297-298` and `:623`: "**D4 and D7 remain unsigned** and no work may act on them." Drafting and presenting is not acting on D7, since `README.md` is untouched and no sign-off table is edited. On open question 3: commit the draft inside `docs/finding1_residual/PLANNING.md` labeled "DRAFT — pending D7 signature, not landed" **and** mirror it in the PR description. A PR body alone is not durable evidence of what was reviewed, and a labeled draft in the packet's own planning doc is not a D7 action.

**Clean on my remaining lanes.** No accounts, no sync, no telemetry, no schema change, no `program_backup` format change, no navigation or workflow-ownership change. Effective sets stay informational — the diagnostic never gates, blocks, or auto-adjusts, consistent with `utils/effective_sets.py:6-7`. Nothing under `utils/_fatigue/**` is touched and no threshold moves, so the Phase-2 Stage-4 closure is not reopened. Open question 4: naming a routine and exercise in an error message is not data exposure — single-user localhost, no auth, and the same strings already appear in `restore_backup()`'s response (`utils/program_backup.py:502-506`) and in progression copy (`utils/progression_plan.py:293,313`).
---

## Response matrix

Every finding gets a row. "Defer" requires a one-line reason and a note in `MASTER_HANDOVER.local.md`. **Every finding in this council was accepted; there are no defers and therefore no `MASTER_HANDOVER.local.md` note is owed.**

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| **A1** `NO_DATA` is a conformant path; wiring site 6 on `if not result.ok:` scans on every empty-plan export | architecture-reviewer | **accept** | Site-6 enrichment gated on `result.code == "VALIDATION_ERROR"`; AC5 restated as "no extra query on any path that succeeds today, and none on a non-validation failure". Sequence step 5 asserts an empty plan still returns the untouched `NO_DATA` 400. |
| **A2** a capped unfiltered scan cannot guarantee it names *the* offending row | architecture-reviewer | **accept** | Per-site row filter added to the predicate table: site 4 filters by the request's `exercise` mirroring `get_exercise_plan_defaults`' `WHERE exercise = ? ORDER BY id DESC LIMIT 1`; sites 3 and 6 must retain the causally-implicated row inside the cap (site 6's is the *first* failing row, since `export_service` returns on first). |
| **A3** the enriched Excel message never reaches the user — `exports.js:88` hardcodes its toast | architecture-reviewer | **accept** (as a declared residual; site 3 stays in scope) | AC2 carries an explicit scope note; the residual is listed in Out of scope and is a required line in the PR description. AC2 no longer implies a user-visible win. |
| **A4** the scanner inherits `_attempt_database_recovery`'s live-DB quarantine | architecture-reviewer | **accept** | Recorded as a Section 0 assumption; the module docstring must state it; the scanner is kept out of any handler that already caught `sqlite3.DatabaseError`. |
| **A5** calling `validate_workout_bounds` verbatim over-reports | architecture-reviewer | **accept**, merged into P3 | Resolved by the per-site predicate table, not by narrowing to finiteness: sites 1–4 validate each rep field **in isolation**, which structurally excludes the cross-field and weight/RIR messages. |
| **A6** the `ValueError` arm at `routes/progression_plan.py:191-199` is unenriched | architecture-reviewer | **accept** | Plan v2 records one sentence: the 400 arm is deliberately unenriched because `current_reps + 2` raises `TypeError`, so no poisoned shape reaches it. |
| **A7** the new module's logger is unspecified | architecture-reviewer | **accept** | Artifact row now specifies `logger = get_logger()` and that swallowed exceptions go to `logger.exception`. |
| **A8** the cap is a hard UI constraint, not a style choice | architecture-reviewer | **accept** | Folded into Q2's answer; the cap's justification is now `fetch-wrapper.js:213` / `exports.js:110` / `error.html:18`, not taste. |
| **B1** step 8's raise-patch oracle is vacuous, and AC5's query count has no instrument | test-strategist | **accept** | Step 8 replaced with a **call counter** monkeypatched into all four route modules; the query-count half of AC5 is dropped, the byte-identity half kept (N1's `assert_error_payload`). No query-counting harness is invented. |
| **B2** four derived pytest targets missing from the Artifacts table | test-strategist | **accept** | All nine named files added to the Artifacts table, including `tests/test_program_backup_restore_fuzz.py` as an explicit **negative control** for AC5. |
| **B3** the pyright baseline gate is unmentioned and is required | test-strategist | **accept** | New Sequence step 12, before the inventory regen. Re-baselining flagged as an owner decision, not a repair. |
| **B4** step 11's `npx` prerequisite is unverified and sequenced last | test-strategist | **accept** | Moved to Sequence step 2 as a pre-check, with the explicit note that `npx playwright test --list` starts no browser and no server and therefore does not violate the no-E2E/no-port constraint. |
| **B5** the 2983/2 baseline is Windows-only | test-strategist | **accept** | AC11 rewritten to host-qualify the number and forbid reading a CI count as a regression against it; AC12 added for the inventory deltas. |
| **N1** `assert_error_payload` is strict-equality and is AC5's free byte-identity oracle | test-strategist | **accept** | Named as AC5's oracle, with an explicit standing instruction never to relax it to a substring match if it reds. |
| **N2** `test_html_error_response` patches `render_template` wholesale and is blind to `error_message` | test-strategist | **accept** | Test plan requires asserting `mock_render.call_args.kwargs["error_message"]` or rendering for real per `test_error_page_contract.py:82`, and pairing every positive with a clean-DB negative. |
| **N3** the swallow needs its own node | test-strategist | **accept** | Dedicated node added: force the scanner to raise, assert all four surfaces return original status **and** original message. Precedent cited: `tests/test_fatigue_routes.py:13-14`. |
| **N4** mutation-check cell by cell | test-strategist | **accept** | Sequence step 7 rewritten to mutate per matrix cell; a file-level red is explicitly called insufficient. |
| **N5** use the validator as the predicate, not a bare `float()` | test-strategist | **accept**, merged into P4 | Single shared `_accepts_in_isolation()` helper used by both the scanner and Proposal B. |
| **N6** no E2E waiver needed | test-strategist | **accept** (informational) | Recorded in Expected gates: `e2e/program-backup.spec.ts:258,277` asserts the same validator string but is produced by untouched code. |
| **N7** conftest blueprint registration — resolve to "none required" | test-strategist | **accept** | Plan v1's open clause closed; all five blueprints already registered at `tests/conftest.py:218-230`. |
| **N8** no pytest node can exercise the `/progression` success page with goal rows | test-strategist | **accept** (informational) | Recorded as a constraint on test design: no proposed node may depend on that page rendering until conftest gains the `datetime` filter. |
| **N9** a structured `invalid_rows` key would make the packet Large and pull in `api-integration.spec.ts` | test-strategist | **accept** | Folded into Q1's answer (message-only). |
| **P0** the hard constraint holds — `utils/workout_validation.py:1-12` reaches no forbidden module | product-risk-reviewer | **accept** (record it) | Recorded as verified rather than assumed in Plan v2's constraint-compliance paragraph. |
| **P1** site 7's reachability is misstated, and Plan v1 inflated it | product-risk-reviewer | **accept** | Added as **correction #4** in Section 0; the Out-of-scope residual is restated as "unreachable through the shipped UI; reachable only via a hand-constructed `?routine=` request". This is the single largest change from v1. |
| **P2** no criterion covers "the surface failed but the scan found nothing" | product-risk-reviewer | **accept** | New **AC5a**: on an empty scan the message is byte-identical to today's and the formatter emits no "no problems found" phrasing. |
| **P3** the predicate is not pinned to each call site's actual validator invocation | product-risk-reviewer | **accept** | New **per-site predicate table** in Plan v2 fixing fields, `allow_null`, and row filter per site — site 6 mirrors `allow_null=True`, sites 1–4 use `allow_null=False` on reps in isolation. |
| **P4** "parses as a number" is weaker than the validator (`'nan'` / `'inf'`) | product-risk-reviewer | **accept** | Proposal B's predicate is now "pass the stored sibling only when `validate_workout_bounds` accepts it in isolation", via the shared helper. Test case for `'nan'` and `'inf'` added. |
| **P5** Proposal B must not land without Proposal A | product-risk-reviewer | **accept** | Added as a hard sequencing constraint in Plan v2 ("Do not split this PR"), with P5's own reasoning that the relaxation cannot admit a genuinely bad state recorded alongside. |
| **P6** copy hazards — falsy routine, and one-sentence rendering | product-risk-reviewer | **accept** | Falsy routine renders as `Unassigned`; the **literal diagnostic copy is drafted in Plan v2** rather than left to implementation. |
| **P7** the README draft is missing the step that destroys the user's recovery material | product-risk-reviewer | **accept** | The draft is rewritten with P7's ordering — stop, **copy the whole folder out before restarting anything**, rename don't overwrite, delete sidecars before copying in — plus the empty-DB skip and the `_attempt_database_recovery` fact. |
| **P8** D7 gating verified correct | product-risk-reviewer | **accept** | Folded into Q3's answer. |
| **P9** no data-exposure concern | product-risk-reviewer | **accept** | Folded into Q4's answer. |

---

## Plan v2

**Goal**: unchanged from v1 — when a pre-#384 poisoned rep range breaks a page, the error names the routine and exercise that must be repaired, and repairing it through the Plan editor works whichever rep column the user edits first, with no calculation semantics touched anywhere. **What changed is precision, not direction:** the scan is now pinned per call site, the causally-implicated row is guaranteed to survive the cap, the zero-cost claim has a real oracle, and two claims Plan v1 made about user impact (site 7's severity, the Excel toast) are corrected downward.

**Scope**

- **In**
  - **Proposal A — diagnose-on-failure, route layer only.** New `utils/rep_range_integrity.py`: a read-only scanner over `user_selection` importing **only** `utils.database.DatabaseHandler`, `utils.workout_validation.validate_workout_bounds` (+ `UNSET`), and `utils.logger.get_logger`. P0 verified that this reaches no forbidden module transitively — `utils/workout_validation.py:1-12` imports only `math`, `typing` and `utils.constants`. Returns `[{"routine": …, "exercise": …, "reason": …}]`, the shape `restore_backup()` already returns (`utils/program_backup.py:500-506`), plus a formatter. **The scan runs only inside an `except` that has already fired, or on site 6's `VALIDATION_ERROR` return specifically — never as a preflight, and never on `NO_DATA` (A1).**
  - **Proposal B — the edit-order trap**, at `routes/workout_plan.py:389-401`, using the same isolation predicate.
  - Tests per B2/N1–N4, the pyright baseline diff (B3), and the inventory regen (B4/B5).
  - Item 2's README draft, **committed into this document** under a `DRAFT — pending D7 signature, not landed` heading and mirrored in the PR description.
- **Out**
  - Everything in Section 0's Out of scope, as revised: site 7 (now qualified as UI-unreachable), the Excel toast text (`static/**`), status-code changes, poisoned-row repair, `templates/**`, `static/**`, `e2e/**`, `.github/workflows/**`, and the three read-only docs.

**Constraint compliance — verified, not assumed.** `utils/effective_sets.py`, `utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py`, `utils/export_service.py` and `utils/_fatigue/**` are untouched, and P0 confirmed the scanner's import closure never reaches them. Sites 1–6 still raise on poisoned rows. **No volume number moves.** The forbidden-file escape hatch in the raw request is not triggered.

**Sequencing constraint (P5) — do not split this PR.** Proposal B moves the `(min poisoned, max edited)` case from 400 to 200, which removes the user's only current signal and replaces it with "Exercise updated successfully" on a row that still 500s the Analyze pages. That is acceptable **only** because Proposal A ships in the same PR and its `reason` names the field. Recorded alongside: the relaxation cannot admit a genuinely bad state — it fires only when the sibling is already outside the contract, and no numeric `min > max` pair can be formed because the surviving half is not a number.

### The isolation predicate (P4 + N5 + A5)

One helper, used by both proposals:

```
_accepts_in_isolation(field, value) -> bool
    # True iff validate_workout_bounds(**{field: value}) returns None,
    # with every other field left UNSET.
```

Validating **one field at a time** is what makes this correct rather than convenient: it structurally excludes `"Minimum reps cannot exceed maximum reps."` (`utils/workout_validation.py:79-80`) and the weight/RIR range messages (`:64-75`), none of which cause the 500s at sites 1/2/4 — that is A5's resolution. **[AMENDED 2026-08-29 by owner ruling R2.1 / ADR-009: this sentence is true of sites 1/2/4, which it was written about, and is NOT true of site 6. `export_plan_to_workout_log` makes one combined call in which the cross-field verdict fires, and that verdict is exactly what blocks it — so `scan_export_bounds` now makes that same combined call and reports `min > max`. Sites 1/2/4 keep per-field isolation and still report nothing for an inverted row. The per-site table below already says "the full four" for site 6 and needs no change.]** It also settles `'nan'` / `'inf'` / `''` / `None` by construction rather than by a bare `float()` that would let `'nan'` through (P4).

### Per-site predicate table (P3 + A2)

The scanner does **not** expose one canonical scan. Each wiring site gets its own call, reproducing what that site actually does:

| Site | Wiring point | Fields scanned | `allow_null` | Row filter | Cap rule |
|---|---|---|---|---|---|
| 1 · `/weekly_summary` | `routes/weekly_summary.py:125-134` existing `except` | `min_rep_range`, `max_rep_range`, **each in isolation** | `False` | none — the failing calculation is unfiltered | 5 + "(+N more)" |
| 2 · `/session_summary` | `routes/session_summary.py:142-151` existing `except` | same | `False` | the request's `routine` arg when present, else none — mirrors `_build_plan_query` (`utils/session_summary.py:40-42`) | 5 + "(+N more)" |
| 3 · `/export_to_excel` | `routes/exports.py:81-88` existing `except` | same | `False` | none | 5, **must retain the causally-implicated row** |
| 4 · `/get_exercise_suggestions` | `routes/progression_plan.py:200-205` catch-all only | same | `False` | **`WHERE exercise = ? ORDER BY id DESC LIMIT 1`** — mirrors `get_exercise_plan_defaults` (`utils/progression_plan.py:22-33`) exactly, including the `LIMIT 1`, so the named row is *the* row the route read | at most 1 by construction |
| 6 · `/export_to_workout_log` | `routes/exports.py:98-103`, **only when `result.code == "VALIDATION_ERROR"`** (A1) | `weight`, `rir`, `min_rep_range`, `max_rep_range` — the full four, matching `utils/export_service.py:493-498` | **`True`** | none | 5, **must retain the first failing row**, since `export_service` returns on first |

Note that site 4's query at `utils/progression_plan.py:22-33` selects no `routine` column, so the scanner reads `routine` itself from the same row. Site 6 is the only site using `allow_null=True`, which is exactly why P3 was blocking: `''` is reachable (`min_rep_range INTEGER NOT NULL`, `utils/db_initializer.py:189-190`, rejects NULL but not the empty string) and `allow_null=True` accepts it (`utils/workout_validation.py:54-56`), so a shared `allow_null=False` scan would diverge from site 6 in both directions.

**Empty-scan rule (P2), binding on every site**: when the scan returns `[]`, the formatter returns the original message **unchanged, byte for byte**, and emits nothing — no "no problems found", no empty list, no trailing punctuation change. Two real paths reach it: `utils/progression_plan.py:410,417` sources `current_reps` from a `workout_log` row, and site 6 also fails on `weight`/`rir`.

### Literal diagnostic copy (P6)

Drafted here so it is reviewable rather than left to implementation. One sentence, no newlines and no markup — `templates/error.html:18` renders `error_message` inside a single `<p>`, and `fetch-wrapper.js:213` / `exports.js:110` render `error.message` verbatim into a Bootstrap toast.

Appended clause (falsy `routine` renders as `Unassigned`, per `utils/weekly_summary.py:24` and the literal at `utils/session_summary.py:90`):

```
 Invalid rep range on: Push Day / Barbell Bench Press (Minimum reps must be a finite number.);
 Unassigned / Cable Fly (Maximum reps must be a finite number.) (+3 more). Fix these in the Workout Plan editor.
```

Full per-site messages, with the unchanged prefix in **bold**:

| Site | Message when the scan is non-empty | Message when the scan is empty |
|---|---|---|
| 1 | **Unable to load weekly summary.** + clause | **Unable to load weekly summary.** (unchanged) |
| 1 (XHR) | **Unable to fetch weekly summary** + clause | unchanged |
| 2 | **Unable to load session summary.** + clause | unchanged |
| 2 (XHR) | **Unable to fetch session summary** + clause | unchanged |
| 3 | **Failed to export data to Excel. Please try again.** + clause | unchanged |
| 4 | **Failed to get exercise suggestions** + clause | unchanged |
| 6 | **`<the canonical validator string>`** + clause | unchanged |

The scanner uses the literal `'Unassigned'` rather than importing `UNASSIGNED_ROUTINE` from `utils/weekly_summary.py` — that import would widen the module's closure into a forbidden file for no benefit, and `utils/session_summary.py:90` already sets the precedent of using the literal.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `utils/rep_range_integrity.py` | **new** | Read-only `user_selection` scanner + `_accepts_in_isolation` + formatter. Imports only `DatabaseHandler`, `validate_workout_bounds`/`UNSET`, `get_logger`. **`logger = get_logger()`; every swallowed exception goes to `logger.exception` (A7).** Module docstring must state A4: opening a connection from inside a failing `except` can itself trigger `_attempt_database_recovery`'s live-DB rename (`utils/database.py:226-231`), so the scanner is never called from a handler that already caught `sqlite3.DatabaseError`. |
| `routes/weekly_summary.py` | modify | `:125-134` only. Status stays 500. |
| `routes/session_summary.py` | modify | `:142-151` only. Status stays 500. Passes the request's `routine` arg as the filter. |
| `routes/exports.py` | modify | `:81-88` (Excel 500) and `:98-103` **gated on `result.code == "VALIDATION_ERROR"`** so `NO_DATA` is untouched (A1). |
| `routes/progression_plan.py` | modify | `:200-205` only, filtered by the request's `exercise` (A2). The `ValueError` arm at `:191-199` is **deliberately left unenriched** — `current_reps + 2` raises `TypeError`, so no poisoned shape reaches it (A6). The `/progression` page handler at `:131-138` is not touched. |
| `routes/workout_plan.py` | modify | `:389-401`. Stored sibling passed only when `_accepts_in_isolation` accepts it, else `UNSET`. |
| `tests/test_rep_range_integrity.py` | **new** | Unit: clean → `[]`; poisoned min / max / both; `''`, `None`, `'nan'`, `'inf'`; `allow_null` True vs False divergence; row shape; falsy routine → `Unassigned`; cap retains the causal row; empty scan returns the original string unchanged; swallow path. |
| `tests/test_weekly_summary_routes.py` | modify | **As built:** the `app` fixture now pins `DB_FILE` to a per-test temp path. These tests build a bare Flask app with no DB patching, so once the error handler ran the diagnostic they would have read — and created — the checkout's real `data/database.db`. `assert_error_payload`'s strict equality is preserved untouched (N1). **It is a weaker oracle here than it looks**, and the record should not claim otherwise: the tmp path has no schema copied, so in these two files the scan always raises `no such table` and is swallowed to `[]`. The assertion still pins the string, but it is green under both "scan found nothing" and "scan could not read". The real clean-path oracle is `tests/test_error_page_contract.py`'s paired negative on the schema-backed conftest client, plus the identity assertion `annotate(original, []) is original`. |
| `tests/test_session_summary_routes.py` | modify | Same fixture change, same reason. |
| `tests/test_exports.py` | modify | Excel 500 + named row; plan→log **400** + named row; **empty plan still returns the untouched `NO_DATA` 400 with zero scans** (A1). |
| `tests/test_progression_plan_routes.py` | modify | Poisoned `max_rep_range` → 500 naming *that* exercise; poisoned `min_rep_range` → still **200**; a second poisoned exercise must **not** appear in the message (A2). No node may depend on the `/progression` success page rendering (N8). |
| `tests/test_workout_plan_routes.py` | modify | Full 2×2 matrix — (min,min) 200, (min,max) **200 (was 400)**, (max,max) 200, (max,min) **200 (was 400)** — plus numeric-sibling `min > max` still 400, user-supplied garbage still 400, and `'nan'`/`'inf'` siblings treated as unparsable (P4). |
| `tests/test_error_page_contract.py` | modify | **Added per B2, and as built this is where the named-row assertions landed** — not in the two route files above, which build a bare Flask app with no template folder and no database. It drives the real app and renders `error.html` for real, asserting `error_message` as `:82` does rather than modelling on the wholesale-mock at `test_weekly_summary_routes.py:369-378` (N2), with the paired clean-DB negative. |
| `tests/test_program_backup_restore_fuzz.py` | run as **negative control** | **Added per B2** (`:245,283,360,542`). Exercises the #384 ingress on a conformant path — a ready-made AC5 control. Expected unchanged. |
| `tests/test_downstream_normalization.py` | run | Added per B2. |
| `tests/test_trailing_slash_routing.py` | run | Added per B2. |
| `tests/test_weekly_summary.py`, `tests/test_session_summary.py` | run | Added per B2 — util-level regression guard for the untouched calculations. |
| `tests/test_workout_log_routes.py`, `tests/test_ui_flows.py`, `tests/test_erase_data_guard.py` | run | Added per B2 — derived from `routes/exports.py`. |
| `tests/conftest.py` | **no change** | N7: all five blueprints already registered at `:218-230`. |
| `docs/test_inventory/TEST_INVENTORY.json` + `.md` | regenerate | Last step. `total_files` 123→124, `deterministic_files` 122→123. Never hand-edit; check for untracked/gitignored `.md` in globbed surface dirs first. |
| `docs/finding1_residual/PLANNING.md` | this file | Council record, the four §4a corrections, and the Item 2 draft. Does **not** move the inventory (B5). |
| `README.md` | **no change** | Draft lives in this document under `DRAFT — pending D7 signature, not landed`. **[UPDATED 2026-08-21 — the owner signed D7 and the draft LANDED in `README.md` in a separate, later packet. This row was correct for the #394 packet.]** |
| `docs/TESTING_STRATEGY_PLANNING.md` | **no change** | D7 is not recorded as signed by this packet (P8). **[UPDATED 2026-08-21 — a later packet recorded D7 as signed in §8.1d. Still true of the #394 packet.]** |
| `docs/LEFTOVERS_BY_PRIORITY.md` | **no change** | Read-only; the four corrections live in Section 0. |

**Effort**: **M** · **Owner**: implementation agent (this worktree) · **Depends on**: Gate 1 approval of this Plan v2; Item 2's *landing* depends on an owner D7 signature this packet must not manufacture.

**Sequence**

1. **Gate 1.** Owner approves Plan v2. Do not start until then.
2. **Pre-checks, both before any code (B4):** (a) re-confirm the Windows baseline is green — 2983 passed, 2 skipped on `d583225`; (b) run `npx playwright test --list --project=chromium` and confirm non-empty output. `--list` starts **no browser and no server** (`scripts/generate_test_inventory.py:83`), so this does **not** violate the owner's no-E2E / no-port constraint; skipping it means discovering at step 13 that `generate_test_inventory.py:72-79` hard-exits without `npx`, on a worktree that junctions to main's `node_modules`.
3. Write `utils/rep_range_integrity.py` with `_accepts_in_isolation`, the per-site scan functions, the formatter, and the A4 docstring. Write `tests/test_rep_range_integrity.py`. Run that file.
4. Wire sites 1 and 2; extend `tests/test_weekly_summary_routes.py`, `tests/test_session_summary_routes.py` and `tests/test_error_page_contract.py`. Every positive gets a clean-DB negative (N2). Run all three.
5. Wire sites 3 and 6 in `routes/exports.py`, **gating site 6 on `result.code == "VALIDATION_ERROR"`**; extend `tests/test_exports.py`, including the empty-plan `NO_DATA` case (A1). Assert plan→log is **400**, not 500. Run it.
6. Wire site 4 in `routes/progression_plan.py`, filtered by the request's `exercise`; extend `tests/test_progression_plan_routes.py` including the "a second poisoned exercise is not named" case (A2). Run it.
7. Apply Proposal B at `routes/workout_plan.py:389-401`; extend `tests/test_workout_plan_routes.py` with the full matrix plus preservation and `'nan'`/`'inf'` cases. **Mutation-check cell by cell (N4)** — (min,min) and (max,max) pass today, so a file-level "the tests red" observation proves nothing. Run each direction: revert the guard and confirm the two changed cells red; drop the sibling unconditionally and confirm the `min > max` preservation case reds.
8. **Zero-cost proof (B1).** Monkeypatch a **call counter** into each of the four route modules and assert zero calls on a clean DB. Do **not** use a raise-patch: the scanner swallows its own errors, so that oracle is green under both "never called" and "called and swallowed". `assert_error_payload`'s strict equality (`tests/test_weekly_summary_routes.py:36-41`, `tests/test_session_summary_routes.py:34-39`) is the byte-identity half — **never relax it to a substring match if it reds** (N1). Run `tests/test_program_backup_restore_fuzz.py` as the negative control.
9. **Swallow node (N3).** Force the scanner to raise; assert all four surfaces return their **original** status *and* **original** message. Bug-class precedent: `tests/test_fatigue_routes.py:13-14`.
10. Draft nothing new for Item 2 — the draft is already below. Re-verify it against `utils/auto_backup.py` and `utils/database.py:217-224` before the PR. Do not touch `README.md` or `docs/TESTING_STRATEGY_PLANNING.md`.
11. **Full pytest** on Windows. No E2E, no Flask server, no port. Expect 2983 + the added nodes; **never compare a CI count against 2983** (B5).
12. **`python scripts/pyright_baseline_diff.py` (B3)** — repo-wide on any `.py` touched. A net-new diagnostic is a defect to fix; re-baselining is an owner decision, not a repair.
13. **Last step:** `python scripts/generate_test_inventory.py`; commit the regenerated `.json` and `.md`.
14. Create the PR. Its description must carry: the migration notes; the **four** §4a corrections; site 7's residual **with P1's reachability qualifier**; A3's Excel-toast residual stated plainly as "JSON body and log only, no UI change"; the Item 2 draft mirrored; and the two incidental findings (the `/progression` `datetime`-filter fixture artifact, and the `_attempt_database_recovery` docstring).
15. Poll CI to **zero pending** (the count grows 17→18 mid-run — poll, do not sample once). Mark ready. **STOP. Do not merge.**

**Expected gates**

> *Evidence-gap note resolved.* An earlier revision of this section was derived from the relayed findings because the `test-strategist`'s paste-ready block had not reached the authoring agent. The verbatim block was subsequently recovered from the manager's context and is reproduced below unaltered. Where it offers a choice, this packet takes the second option per **B1** — the query-count half of AC5 is dropped in favour of the already-instrumented byte-identity oracle, and no query-counting harness is built.

*Verbatim, `test-strategist` (agent `a14b6cfdb6a819433`):*

- **pytest — full suite is the gate** (owner-pinned at Section 0, and required
  anyway because step 11's inventory regeneration runs a full `--collect-only`).
  The change-type table alone would yield only a Targeted gate: no `app.py`, no
  `tests/conftest.py`, no schema — so full pytest is a superset, not a conflict.
  Inner-loop targets, derived per QUALITY_GATE.md#targeted-test-derivation:
  - `tests/test_rep_range_integrity.py` (new — Business logic row, `utils/rep_range_integrity.py`)
  - `tests/test_weekly_summary_routes.py`, `tests/test_weekly_summary.py`
  - `tests/test_session_summary_routes.py`, `tests/test_session_summary.py`
  - `tests/test_exports.py`
  - `tests/test_progression_plan_routes.py`
  - `tests/test_workout_plan_routes.py`
  - **added by derivation, absent from the Artifacts table above:**
    `tests/test_error_page_contract.py` (forces all three `except` blocks and
    renders `error.html` for real — `:18-83`),
    `tests/test_program_backup_restore_fuzz.py` (`:245,283,360,542` hit
    `/weekly_summary` expecting 200 on clean data — the negative control for
    acceptance criterion 5), `tests/test_downstream_normalization.py`,
    `tests/test_trailing_slash_routing.py`, `tests/test_export_weekly_summary_sheet.py`
  - `tests/conftest.py`: **no change required.** All five blueprints are already
    registered at `:218-230`; no new blueprint, no new table, no `erase_data()` work.

- **e2e — none, and no waiver is needed.** No `templates/**`, `static/**`,
  `scss/**` or `e2e/**` path is touched, so the Frontend / CSS / E2E-spec rows
  never fire and the feature map is not consulted. `e2e/program-backup.spec.ts:258,277`
  asserts `'Minimum reps must be a finite number.'`, but that string comes from
  `restore_backup()` via `validate_workout_bounds` — both untouched. The known-red
  `e2e/program-backup.spec.ts:79` is not implicated. This holds **only** while
  the diagnostic stays message-only; adding an `invalid_rows` JSON key would pull
  in `api-integration.spec.ts` and contest the no-E2E constraint.

- **other:**
  - `Type Check (tsc blocking + pyright measure-only)` — required check, repo-wide,
    triggered by any `.py` in the diff (QUALITY_GATE.md:52,69-70). Run
    `scripts/pyright_baseline_diff.py` before step 12; the new module is the likely
    source of net-new diagnostics. Re-baselining is an owner decision, not a repair.
  - `Test Inventory Drift` — required check, tripped by the per-file pytest node
    count surface. `python scripts/generate_test_inventory.py`, last step, never
    hand-edited. **Prerequisite to verify at step 2, not step 11:**
    `generate_test_inventory.py:72-79` hard-exits without `npx`, and `:90-98`
    shells out to `npx playwright test --list`. Confirm `node_modules` resolves in
    this worktree first. `--list` starts no browser and no server (`:83`), so it
    does not violate the no-port/no-E2E constraint.
  - No `/build-css`, no `/verify-suite` E2E half.

- **Baseline is host-specific.** 2983 passed / 2 skipped is a **Windows** number:
  `TEST_INVENTORY.json:244` gives `collected_deterministic: 2663`, plus
  `tests/test_guard_destructive_command.py` at 322 on Windows / 163 on ubuntu
  (`:248-249`). 2663+322 = 2985 = 2983+2. The same tree collects **2826** on the
  Linux runner. Step 10's delta check is valid same-host only; never read a CI
  count as a regression against 2983.

- **Oracle requirements — three nodes that would otherwise be vacuous:**
  1. *Scanner-not-called (criterion 5).* Step 8's "patch it to raise" is defeated by
     the swallow at Artifacts row 1 — the happy path passes whether or not the
     scanner ran. Replace with a **call counter** monkeypatched into each of the
     four route modules, asserting zero calls on a clean DB.
  2. *Zero extra queries (criterion 5).* No query-counting idiom exists in this repo
     (`rg "set_trace_callback|query_count"` → zero hits). Either build one via
     `sqlite3.Connection.set_trace_callback`, or drop the query half of criterion 5
     and keep only the byte-identity half — which is **already** instrumented by
     `assert_error_payload`'s strict equality at `tests/test_weekly_summary_routes.py:36-41`
     and `tests/test_session_summary_routes.py:34-39`. **Do not relax those to
     substring matches** if they red; the equality is the guarantee.
  3. *Enriched-message assertions must be falsifiable.* `test_html_error_response`
     (`tests/test_weekly_summary_routes.py:369-378`) asserts status only and is
     blind to `error_message` — modelling a new node on it proves nothing. Assert
     `mock_render.call_args.kwargs["error_message"]`, or render for real as
     `test_error_page_contract.py:82` does, and **pair every positive with a
     clean-DB negative** asserting the routine name is absent.
  Plus: a node forcing the scanner to raise and asserting all four surfaces return
  their **original** status and **original** message — the swallow needs its own
  proof (precedent: `tests/test_fatigue_routes.py:13-14`, a real TypeError
  introduced inside an `except`).

- **Mutation discipline.** Step 7 must red **cell by cell**: (min,max) and (max,min)
  are the only new cells; (min,min) and (max,max) pass today, so a file-level "the
  tests red" observation is satisfied by the pre-existing cells and proves nothing.

*Manager's adjustment, per B1:* oracle requirement 2 takes the **second** option — the query half of AC5 is dropped and the existing `assert_error_payload` strict equality is the byte-identity oracle. No `set_trace_callback` harness is built in this packet.

---

## Item 2 — README auto-backup recovery section

### DRAFT — pending D7 signature, not landed

> **[SUPERSEDED 2026-08-21 — this heading is historical. D7 was signed and this text, with the three wording deltas listed in the banner at the top of this document, is now a live section of `README.md`. Read `README.md` for the authoritative wording; this copy is retained as the reviewed artifact, not as a second source of truth.]**

> **Status.** A **draft only**. `docs/TESTING_STRATEGY_PLANNING.md` §6 states verbatim: *"**D4 and D7 remain unsigned** and no work may act on them"* — re-verified against `origin/main` `63b206e` at `:316` and `:642`. (The verbatim reviewer findings above cite `:297-298` and `:623`; those were correct when written and drifted when #392 edited that file. The quote itself is unchanged, and **D7 is still unsigned upstream** — which is the fact this packet depends on.) Landing this text in `README.md` **is** the D7 action, so `README.md` is deliberately unmodified on this branch and D7 is **not** recorded as signed by this packet. Committing the draft here, labeled, is not a D7 action — it is the reviewable artifact the owner signs against.
>
> **Correction to the brief carried into this draft:** the auto-backup producer is **`utils/auto_backup.py`**, not `utils/program_backup.py`. The latter is the in-DB Backup Center (`program_backups` / `program_backup_items`, `/api/backups`) — a different feature that stores its backups *inside* the same database file and therefore cannot protect against that file being lost or corrupted.
>
> **Revised after `product-risk-reviewer` (agent `ab29bb4b8f96c0ac6`) found three data-destroying defects in the first draft.** All three were verified against the code before rewriting — see *Review corrections* at the end of this section. The reviewer's verdict was **sign the stance, amend the text**.

---

## 💾 Recovering Data from an Automatic Snapshot

The app keeps two independent backups. **Only the first can be restored from inside the app.**

| | Backup Center | Startup database snapshots |
|---|---|---|
| What it saves | Your workout plan | The entire database file |
| Where it lives | Inside `database.db` | `auto_backup\database_<timestamp>.db` |
| Survives a lost or corrupted `database.db`? | **No** — it lives inside that file | **Yes** — separate files |
| How to restore | In the app — Backup Center → Restore | **By hand — steps below** |

Startup snapshots are disaster recovery. They are never listed in the Backup Center, and there is deliberately no in-app restore button for them — recovering one means copying a file yourself.

> ### ⚠️ Before you restart the app, read this
>
> The app keeps only the **7 most recent** snapshots and deletes the oldest each time it takes a new one — which is every normal start. It takes one **even when your data is already gone**, because the check that skips it counts the built-in exercise library, not your workouts, and that library is always present.
>
> So from the **very first restart after a problem appears**, each launch destroys one real snapshot, oldest first — the one most likely to predate the problem. Seven restarts and every genuine snapshot is gone.
>
> **Close the app and copy the whole `auto_backup` folder somewhere safe — your Desktop is fine — before you restart anything or try any fix.** Everything below works on that copy.

### When a snapshot is taken

- Every time the app starts, except the very first launch of a brand-new install.
- Immediately before **Erase All Data** wipes everything, so a full erase stays recoverable. The confirmation message names the file it just wrote.

### Where the snapshots are

The folder sits beside whichever database the app is using. **Start the app normally with `START.bat`? Use the first row. Running the standalone `.exe`? Use the last row.** The middle two apply only if you set those variables yourself.

| How you run it | Snapshot folder |
|---|---|
| `START.bat` from a source checkout | `<repo>\data\auto_backup\` |
| With `HT_RUNTIME_DIR` set | `<HT_RUNTIME_DIR>\data\auto_backup\` |
| With `DB_FILE` set | an `auto_backup\` folder beside that file |
| Standalone executable (Windows) | `%LOCALAPPDATA%\HypertrophyToolbox\data\auto_backup\` |

If none of those has what you expect, the app records the exact path every time it writes one. Open `logs\app.log` and search for `Auto-backup written to`.

If you upgraded from an older version, an older set may still sit in the `data\auto_backup\` folder next to the app itself. Copy that folder out too.

Files are named `database_<YYYYMMDD>_<HHMMSS>.db`, stamped in local time.

### Restoring one by hand

> Do this with the app **closed**, on the copy you made above.

1. **Stop the app.** Close the console window, or quit the executable.
2. **Pick a snapshot** — the newest one timestamped *before* the problem appeared.
3. **Rename the current database out of the way — do not delete anything.** In the folder holding `database.db`, rename **every** file whose name starts with `database.db` to start with `database.broken.db` instead, keeping the rest of the name exactly:
   - `database.db` → `database.broken.db`
   - `database.db-wal` → `database.broken.db-wal` *(if present)*
   - `database.db-shm` → `database.broken.db-shm` *(if present)*
   - `database.db-journal` → `database.broken.db-journal` *(if present)*

   Those extra files are not junk — they hold your most recent changes, and they belong to the database they are named after. Renaming them together keeps the broken copy intact and, just as importantly, stops them being applied to the snapshot you are about to put in their place.
4. **Check the folder.** Nothing named `database.db` or `database.db-…` should be left.
5. **Copy the snapshot into place.** Copy — do not move — your chosen `database_<timestamp>.db` into that folder and rename the copy to `database.db`. Copying keeps the snapshot intact if you picked the wrong one.
6. **Start the app and check.** Open Workout Plan and Weekly Summary and confirm the data is the version you expected. If it is not, stop the app and repeat from step 3 with a different snapshot — your `database.broken.db` and your copied folder are both still there.

Once you are satisfied, delete the `database.broken.db*` files yourself; nothing removes them for you.

### Good to know

- **If the database is corrupted, the app does not recover your data for you.** It renames the damaged file to `database.db.corrupted_<timestamp>` and starts with an empty database. That file is worth keeping too.
- **A Backup Center restore replaces your whole current plan and deletes your workout log.** Do not reach for it while you are investigating a lost or corrupted database — finish the file steps above first.
- The Backup Center also has its own **"Auto"** entries. Those are a different thing with a different limit, stored inside the database, and unrelated to the snapshot files described here.

---

### Review corrections applied to this draft

Recorded so the next reader knows the first version was wrong, and why.

| # | Defect in the first draft | Verified by |
|---|---|---|
| **F1** | Step 6 told the user to **delete** `-wal` / `-shm`. That destroys the most recent state of the very copy the previous step told them to keep, and it names the wrong file: `FLASK_DEBUG` defaults to `'1'` inside `utils/database.py:88`, and neither `START.bat` nor `RUN_APP.bat` sets it, so a real user runs `journal_mode = DELETE` and has a **`database.db-journal`** the draft never mentioned. An orphaned journal beside a swapped-in snapshot is exactly the corruption the step existed to prevent, because SQLite pairs a journal to a database **by filename**. Now a lossless rename of all four, with a check instead of a deletion. | `utils/database.py:88-93`; no `FLASK_DEBUG` in either launcher; `utils/runtime_migration.py:42` already treats `-journal` as state-carrying |
| **F2** | The draft said a restart "will not create a protective snapshot of the empty database — but it will still rotate an old one out." **Both halves were false, in the dangerous direction.** `create_startup_backup()` returns at `utils/auto_backup.py:66`, *before* `_rotate()` at `:80`, so a skipped snapshot rotates nothing. And the `< 100` guard counts the **catalog** (`:55`), which `erase-data` never drops (`exercises` is absent from `OWNED_TABLES_DROP_ORDER`) and which `upgrade_catalog_from_seed()` refills before the check runs (`app.py:102-108`). So the app **does** snapshot the emptied database and **does** delete a real one — from the first restart onward. The warning is now front-loaded and states the true mechanism. | `utils/auto_backup.py:55,59-66,80`; `utils/schema_registry.py` `OWNED_TABLES_DROP_ORDER`; `app.py:94,102-108` |
| **F3** | The draft recommended Backup Center as "the right tool for *I want my old routine back*" with no caveat, in a section read during a data-loss panic. `restore_backup()` runs `DELETE FROM workout_log` inside its transaction and backup items carry only `user_selection` columns — **the workout log is deleted and never restored.** | `utils/program_backup.py:474-479`, `:456-461` |
| **F4–F7** | Added the legacy `data\auto_backup\` location left behind by `utils/runtime_migration.py:175-204`; made the folder table usable by a non-technical user and gave them the `app.log` fallback (`utils/auto_backup.py:81-83`); separated "startup database snapshots" from Backup Center's own **"Auto"** entries, which have a different retention (`prune_auto_backups(keep_count=10)`); made the rotation sentence precise. | as cited |

### Out of scope for D7, and worth its own decision

The reviewer identified a real gap that this README cannot close: **nothing in the app tells a user that a quarantine happened, that snapshots exist, or where they are.** After a corruption the app simply looks brand new, and the rotation clock is already running against them. A README only helps someone who thinks to read it *before* restarting. Candidates — a read-only in-app surface pointing at the snapshot folder, and/or not rotating when the snapshot contains no user rows — but the second changes `create_startup_backup()` and is therefore a Backup-contract change needing migration notes and tests. **Do not widen D7 to cover this**; open it separately.

---

## Diff-time gate (post-implementation)

Run after the code landed, per [`council-plan`](../../.claude/commands/council-plan.md) step 6. The council reviews a plan; these two review the diff.

| Reviewer | Agent ID | Verdict |
|---|---|---|
| `code-reviewer` | `a3511da61df62a19d` | One blocking finding, since fixed |
| `unslop-reviewer` | `a36436450be54435d` | No blocking findings; 14 trims, 12 applied |

Both reviewers ran without Bash and reconstructed the diff by reading the worktree against the main checkout. `code-reviewer` flagged that explicitly and asked for a `git diff --cached --stat` confirmation of the protected files; that confirmation is recorded below.

### Blocking — fixed

**The corruption-quarantine mitigation shipped only half.** The module docstring stated the rule ("never call in from a handler that already caught a `sqlite3.DatabaseError`") but no call site enforced it, and all four are bare `except Exception`, which catches exactly that. `utils/database.py:271-276` routes a `DatabaseError` into `_attempt_database_recovery`, which renames the live database to `<name>.corrupted_<timestamp>` — so a read-only diagnostic could have been the call that quarantined a user's database. The module's own `except` swallow cannot cover it, because the rename happens inside the connect.

This was prescribed as a two-part fix by finding **A4** at plan stage; only the docstring half was implemented. Now closed with `suppressed_for()` and a guard at each of the four sites.

**The first fix was itself half-pinned, and a second review round caught that too.** `TestACorruptionErrorIsNeverDescribed` originally parametrized over `/weekly_summary` and `/session_summary` only, so deleting the guard from `routes/exports.py` or `routes/progression_plan.py` left the whole suite green. Stubbing the shared predicate to `False` reds three nodes, but that is a module-level mutation and is equally consistent with the guard existing at two sites or at four — it cannot distinguish them, so it was never evidence for the four-site claim. Both remaining sites are now pinned, and each mutation reds independently.

The exposure was narrow, and saying so is part of the record: `_RECOVERY_ATTEMPTS` (`utils/database.py:204-211`) is a process-lifetime latch, so if the original failure was a connect-time corruption error, recovery had already run and the diagnostic could not have triggered it. The reachable window is an execute-time `DatabaseError` on a connection that opened cleanly.

### Non-blocking — applied

- **Two docstring claims were false and load-bearing.** Per-field isolation excludes only the cross-field verdict; the weight and RIR *range* checks are per-field and do fire, which is correct for `scan_export_bounds` and wrong in the prose that said otherwise. And "the row that blocked the export is the first one reported" is not guaranteed by SQL — neither query orders explicitly, so it holds by shared table order, not by construction. Both restated.
- **Slop trims (12).** Constraint-justification prose that belongs in the PR body, a docstring restating the comment eight lines below it, change-history narration in a route comment, a stray `(self, )`, a duplicate assertion strictly weaker than the one above it, and four route imports sitting 230 lines into a test file.
- **A test whose name overstated it.** `test_cross_field_verdicts_cannot_reach_it` asserted only that two isolated calls pass — equally consistent with there being no cross-field rule at all. It now carries the control proving the rule exists and fires.
- **This document falsified itself in two places.** Its header still said everything below Plan v1 was an unfilled placeholder, and Plan v1's `Expected gates` still held `<files>` / `<specs>`.
- **The Artifacts table did not match what was built.** It assigned the named-row assertions to `test_weekly_summary_routes.py` and `test_session_summary_routes.py`; they landed in `test_error_page_contract.py`, which drives the real app and renders `error.html` for real. Those two files were modified for a different reason, now recorded: they build a bare Flask app with no `DB_FILE` patching, so once the error handler ran a diagnostic they would have read — and created — the checkout's real `data/database.db`.

### Declined, with reason

**One `poisoned_plan_row` fixture in `tests/conftest.py`**, replacing the four-line poison-a-row setup copied across five test files (`unslop-reviewer`). The duplication is real and the reviewer is right that five callers make it consolidation rather than premature abstraction. Declined anyway: finding **N7** resolved `tests/conftest.py` to *no change* for this packet, and widening a fixture shared by 123 test files to save four lines in five is a worse trade than the repetition — every one of those files is currently insulated from the others. Recorded as a follow-up rather than dropped.

### Confirmations the reviewers asked for

- `git diff --cached --stat` covers 16 files. **None of `utils/effective_sets.py`, `utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py`, `utils/export_service.py` or `utils/_fatigue/**` appears in it** — the byte-level confirmation `code-reviewer` could not run itself.
- `/export_to_excel`'s diagnostic reaching only the JSON body and the log is intended, not an oversight; it is finding **A3**, accepted as a declared residual, and the route comment says so at the call site.

---

## Sign-off

- [ ] Gate 0 complete when required by planning size; otherwise marked not applicable. *(Section 0's blocking-questions box is ticked — all four answered — but the two owner-confirmation boxes remain the owner's.)*
- [x] Every finding has a disposition. *(31 rows; all accepted, no defers, so no `MASTER_HANDOVER.local.md` note is owed.)*
- [x] Agent provenance complete — both `product-manager` IDs, same-PM-resumed yes/no, the three reviewer IDs, and an evidence-gap line (`none`).
- [ ] User approved Plan v2.
- [ ] Ready to implement — proceed to code, then `/unslop` or `/verify-and-polish` for the diff-time gate.

---

## See also
- [`.claude/commands/council-plan.md`](../../.claude/commands/council-plan.md) — how to run the council.
- [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md) — change-type → required tests/reviewers.
- [`.claude/agents/architecture-reviewer.md`](../../.claude/agents/architecture-reviewer.md), [`.claude/agents/test-strategist.md`](../../.claude/agents/test-strategist.md), [`.claude/agents/product-risk-reviewer.md`](../../.claude/agents/product-risk-reviewer.md) — reviewer charters.
