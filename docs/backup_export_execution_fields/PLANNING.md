# Plan Review — Backup/restore and Excel export preserve execution fields (#567, #568)

**Issues**: [#567](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/567) (program backup/restore drops execution fields) · [#568](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/568) (Excel export omits them)
**Branch**: `docs/567-568-execution-fields-planning` · **Brief written**: 2026-11-12
**Status**: Section 0 drafted, **Gate 0 not signed**. No plan exists yet; nothing is authorized for implementation.
**Planning size** ([`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md#plan-stage-routing)): **Large** — PR 1 changes the `program_backup_items` schema, so Gate 0 (this brief) and a council-reviewed Gate 1 are both required.

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

Two owner messages, both dated 12 November 2026, reproduced as the manager supplied them to the `product-manager`.

Message 1:

> Yes, I confirm that backup and Excel export should preserve execution style, time cap, EMOM interval and EMOM rounds. Reproduce the current behavior in an isolated database, then prepare a coordinated plan covering backward-compatible restores and the export format. Separate PRs are fine.

Message 2:

> Proceed with the coordinated two-PR planning approach and the required requirements/council steps. My approval of the product direction does not waive those reviews. For compatibility, distinguish missing legacy fields from present but unrecognized values. Missing execution style can default to standard. Don't silently replace an unrecognized style with standard; propose explicit handling that preserves the existing plan if restore cannot safely interpret the backup.

These messages approve the product direction. By message 2's own terms they are **not** the Gate 0 sign-off on this brief, and they waive no review.

**Problem**

A plan row in `user_selection` carries four execution settings: `execution_style`, `time_cap_seconds`, `emom_interval_seconds` and `emom_rounds`. Two features that claim to carry the plan do not carry all four.

1. **Program backup and restore lose all four, and report success.** A user who sets an exercise to EMOM or AMRAP, saves a backup and later restores it gets every exercise back as `standard` with no timing values. Nothing tells them anything was lost.
2. **The Excel export carries the style but none of its numbers.** The Workout Plan sheet says a row is `emom` or `amrap` and omits the time cap, interval and rounds that give the style its meaning.

*Measured reproduction (manager, 12 November 2026, isolated scratch database, Flask test client — not re-run by the `product-manager`, who has no shell):* a plan row with `execution_style='emom'`, `time_cap_seconds=600`, `emom_interval_seconds=60`, `emom_rounds=10` was backed up and restored. After restore the row read `standard`, `None`, `None`, `None`, and the restore reported success. The code read below explains that result exactly.

*Verified by reading the code on 2026-11-12 (re-verify line numbers before relying on them):*

| Fact | Evidence |
|---|---|
| `program_backup_items` has none of the four columns | DDL at `utils/program_backup.py:71-86`; also stated as known behavior in `docs/product/BACKEND_SCHEMA.md:645-649` ("those settings do not survive a restore") |
| Backup does not read the four fields | `create_backup()` SELECT at `utils/program_backup.py:195-210`, INSERT at `:229-246` |
| Restore does not write them, so the column defaults apply | The four INSERT variants at `utils/program_backup.py:522-605` name no execution column; `user_selection.execution_style` is `TEXT DEFAULT 'standard'`, the three timing columns `INTEGER DEFAULT NULL` (`utils/db_initializer.py:209-220`) |
| `BACKUP_SCHEMA_VERSION = 1` | `utils/program_backup.py:39`. ADR-008 (`docs/DECISIONS.md:107-116`) makes it a reserved informational label, keeps `restore_backup()` deliberately version-blind, and **requires** a bump, an `ALTER` migration and a matching restore branch whenever the `program_backup_items` payload shape changes |
| **Restore deletes before it inspects any row** | `restore_backup()` reads the header, items and catalog names first, then `BEGIN IMMEDIATE` (`:481`), `DELETE FROM workout_log` (`:485`), `DELETE FROM user_selection` (`:486`), then loops over the rows, then commits (`:607`). It rolls back **only** on `sqlite3.Error` (`:608-610`) |
| **Restore also deletes every logged session** | `:485` and `docs/product/APP_FLOW.md:644-656`. Restored rows get new ids, so a restore never leaves the previous plan's log intact |
| **A bad row today is skipped, never refused** | A row whose exercise is not in the catalog goes to `skipped` (`:496-501`); a row failing weight / rep-range / RIR bounds goes to `invalid` (`:507-518`). Either way the existing plan and log are already deleted and the restore returns success. There is no content-based refusal path today |
| Restore's only error outcomes | `ValueError` (unknown backup id) becomes `NOT_FOUND` 404; anything else becomes `INTERNAL_ERROR` 500 (`routes/program_backup.py:172-177`) |
| Backup Center already surfaces a failed restore | The catch at `static/js/modules/backup-center.js:940-941` shows an error toast containing the server's message (`fetch-wrapper.js:61`) |
| **The valid styles are `standard`, `amrap`, `emom`, and the list lives only in the route layer** | `valid_styles = {'standard', 'amrap', 'emom'}` is a local set at `routes/workout_plan.py:895`, inside `_validate_and_normalize_execution_params()`. The limits — time cap 10–600 s, EMOM interval 15–180 s, EMOM rounds 1–20, all inclusive — are at `:906`, `:918`, `:924` and repeated at `:1089-1093`. **Nothing under `utils/` defines either**, and the database has no `CHECK` constraint on the column |
| Only one supported path writes the four fields | `POST /api/execution_style` (`routes/workout_plan.py:971-987`). It writes exactly three shapes: `standard` with no timing; `amrap` with a time cap and no EMOM values; `emom` with interval and rounds and no time cap. Every other writer of `user_selection` omits the columns and so gets `standard` / empty |
| The plan page treats an empty style as standard | `static/js/modules/workout-plan-helpers.js:110` |
| Export selects and labels `execution_style` only | `utils/export_service.py:106`, `:130` (`Style`), `:154` (`Execution Style`), and the three query variants at `:261`, `:276`, `:288`. The file contains no reference to the three timing fields |
| Export column positions today | `WORKOUT_PLAN_COLUMNS['order']` (`utils/export_service.py:90-112`) has 21 entries; the style is the 16th (column P), followed by Grips, Stabilizers, Synergists, Superset Group, Exercise Order (Q–U) |
| Six `/api/backups` response shapes | Metadata objects carry `id`, `name`, `note`, `backup_type`, `schema_version`, `item_count`, `created_at`; the detail payload adds `items`, each with ten keys (`:393-399`); restore returns `backup_id`, `backup_name`, `restored_count`, `skipped`, `invalid` (`:626-632`) |

**Acceptance criteria**

*PR 1 — backup and restore (criteria 1–11)*

1. **Round trip.** Given an active plan holding rows of every valid execution style as the plan page saves them — `standard` (no timing values), `amrap` (time cap set, EMOM values empty) and `emom` (interval and rounds set, time cap empty), including rows at the limit values (time cap 10 and 600; interval 15 and 180; rounds 1 and 20) — when a backup is created with `POST /api/backups`, the plan is then changed or emptied, and the backup is restored with `POST /api/backups/<id>/restore`, then every restored row has the same `execution_style`, `time_cap_seconds`, `emom_interval_seconds` and `emom_rounds` it had when the backup was taken, values that were empty are still empty, and the restore reports success with the counts it reports today.

2. **The pre-restore safety snapshot is covered too.** Given the restore confirmation's "Save current plan first" action, when the user takes it, then the snapshot it creates preserves the four fields exactly as in criterion 1.

3. **A legacy backup still restores.** Given a backup saved by a build that predates this change — its rows hold no value for any of the four fields — when the new build is running and that backup is restored, then the restore succeeds with the same `restored_count`, `skipped` and `invalid` it would produce today, every restored row reads `execution_style = 'standard'`, and its three timing fields are empty.

4. **Upgrading harms no existing backup.** Given a database that already contains backups, when the new build starts on it for the first time, then every backup is still listed with its name, note, type, item count, creation time and `schema_version` (`1`) unchanged, and each can still be opened, renamed, restored and deleted.

5. **A missing value is never an error.** Given a backup row that holds no stored value for its execution style, when it is restored, then the row is restored as `standard`. Given a backup row that holds no stored value for a timing field, when it is restored, then that field is restored empty — never filled with a default such as 60 or 5 — and the absence alone never causes a refusal.

6. **An unrecognized style refuses the whole restore.** Given a backup in which at least one row that would otherwise be restored holds a stored execution style that is not exactly `standard`, `amrap` or `emom` (for example `tabata`, `EMOM`, or an empty string), when a restore of that backup is requested, then:
   - the request fails with the application's standard error envelope and a non-success HTTP status, under an error code that is neither `NOT_FOUND` nor `INTERNAL_ERROR`;
   - the message states that nothing was restored and the current plan is unchanged, and identifies each offending row by routine, exercise and the unrecognized value;
   - no row anywhere is converted to `standard`.

7. **A refused restore changes nothing.** Given a restore refused under criterion 6 or 8, when the database is inspected afterwards, then `user_selection` and `workout_log` hold exactly the rows they held before the request — same ids, same values, same order, every logged session intact — and the refused backup is itself unchanged and still listed. In the Backup Center the user sees an error carrying the server's message, no success message, and an unchanged active-program count.

8. **A present but invalid timing value refuses the whole restore.** Given a backup in which at least one row that would otherwise be restored has a recognized style and a stored timing value the plan page would not accept for that style — not a whole number; outside the limits (time cap 10–600 for `amrap`; interval 15–180 and rounds 1–20 for `emom`); or stored against a style that does not use it (for example a `standard` row with a time cap) — when a restore is requested, then it is refused exactly as in criteria 6 and 7, with the message naming the row, the field and the stored value. *(Proposed handling — see assumptions A5–A8 and question Q2.)*

9. **Today's skip behavior is unchanged.** Given a backup containing rows whose exercise is no longer in the catalog, or whose weight, rep range or RIR fails the plan's bounds, and no execution-field problem in any row that would be restored, when it is restored, then those rows are skipped and reported in `skipped` and `invalid` exactly as today, and every other row is restored with its four execution fields.

10. **The version label follows ADR-008.** Given the new build, when a backup is created, then its `schema_version` is `2` wherever the label is returned or shown; backups created earlier keep `1`. Given two backups identical except for that label, when each is restored, then the outcomes are identical — restore does not consult the label.

11. **Success response shapes are unchanged.** Given any of the six `/api/backups` endpoints, when it succeeds, then its response carries exactly the keys it carries today (listed in the last row of the table above). The only new outcome is the refusal error of criteria 6 and 8.

*PR 2 — Excel export (criteria 12–13)*

12. **The three timing fields are exported.** Given a plan holding rows of each execution style, when `GET /export_to_excel` is requested in either view mode, then the Workout Plan sheet has three additional columns carrying each row's time cap, EMOM interval and EMOM rounds as the stored whole numbers, with an empty cell wherever the row has no value. Values are written as stored; the export does not validate, default or reject them.

13. **Nothing already exported changes.** Given the same request, then the 21 existing Workout Plan headers keep their text, their order relative to one another and their values in both view modes; every other sheet, the download's content type and filename pattern, and the `EXPORT_FAILED` error shape are unchanged. An older consumer that reads the sheet by header name sees the same data plus three headers it does not know. An older consumer that reads by column position sees Grips, Stabilizers, Synergists, Superset Group and Exercise Order three columns further right (Q–U become T–X) under the proposed placement — see A12 and Q3.

*Both PRs (criterion 14)*

14. **Each PR stands alone and carries its own record.** Given either PR merged without the other, then the application works and the other feature behaves as it does today. Each PR's description carries migration notes, each updates the test coverage for the behavior it changes, and each corrects, in the same change, the documentation that states the old behavior (`docs/product/BACKEND_SCHEMA.md:625-649`; `docs/product/APP_FLOW.md:636` "Always reads `1` today" and `:644-664`; the export rows of `APP_FLOW.md` for PR 2).

**Calculation surface**

- `none`.

Verified, not assumed: the four fields are referenced in production Python only by `utils/db_initializer.py` (DDL), `routes/workout_plan.py` (plan read and write) and `utils/export_service.py` (select and label). No module in effective sets, weekly or session summary, progression, volume or fatigue reads them. `program_backup_items` is read only by `utils/program_backup.py`. The export **calls** `calculate_weekly_summary()`, `calculate_exercise_categories()` and `calculate_isolated_muscles_stats()` to fill other sheets; those functions and sheets are not touched. Restore moves stored rows and computes nothing, and the values that feed calculations (sets, rep range, RIR, RPE, weight) are restored as they are today.

This is nonetheless a schema change and a change to backup behavior, so the refactor invariant in `CLAUDE.md` §1 applies in full: migration notes in each PR description and updated test coverage (criterion 14).

**In scope**

- Program backup captures, and restore reinstates, the four execution fields (PR 1).
- Backward-compatible restore of backups written before the change (PR 1).
- Explicit, all-or-nothing refusal when a backup row holds an execution value restore cannot interpret, leaving the plan and the log untouched (PR 1).
- The `schema_version` bump and migration that ADR-008 makes mandatory for this payload change (PR 1).
- Three timing columns on the Workout Plan sheet of `GET /export_to_excel` (PR 2).
- Tests, migration notes and the documentation corrections named in criterion 14.

**Out of scope / non-goals**

- Whole-database `auto_backup` file snapshots (`utils/auto_backup.py`).
- Importing Excel files. No import path exists and none is added.
- Any change to how execution styles are validated on the plan page (`POST /api/execution_style`) or to its limits.
- Issue #569.
- The other exports — `/export_summary`, `/export_large_dataset`, `/api/export_volume_excel` and `/export_to_workout_log`. None carries the plan's execution style today.
- Changing the existing per-row skip behavior for catalog-missing or out-of-bounds rows (criterion 9 pins it as it is).
- Protecting an older build from a newer backup. ADR-008 already records and accepts that a build predating the bump restores a version-2 backup without a guard.
- Reversing ADR-008. Restore stays version-blind (see A9).

**Assumptions made**

- ⚠️ **A1 — the issue texts were not read.** The `product-manager` has no shell or network access and the repository holds no copy of #567, #568 or #569. Their content is taken from the manager's summary; #569 is recorded as out of scope by number only.
- ⚠️ **A2 — the reproduction was not re-run here.** It is the manager's measurement. It is consistent with the code as read.
- ⚠️ **A3 — "missing" means the backup row holds no stored value for the field**, whichever build wrote it. A plan row whose style is empty can be produced only outside the application, and it would also restore as `standard`, which matches how the plan page already displays it.
- ⚠️ **A4 — "unrecognized" means any stored value that is not exactly one of the three styles.** No case folding and no trimming: `EMOM` and an empty string are unrecognized (Q6).
- ⚠️ **A5 — refusal of the whole restore is a proposal**, built from message 2's "preserves the existing plan". It departs from today's precedent, where a bad row is skipped and the rest of the restore proceeds. Its cost is in Q1.
- ⚠️ **A6 — the timing rules in criterion 8 are a proposal; the owner's messages address the style only.** The rule applied is "restore accepts what the plan page itself can save, plus missing values". One part is deliberately lenient: a style whose own timing value is missing (for example `amrap` with no time cap) is restored as stored and is neither refused nor defaulted, following "missing is never an error".
- **A7 — history checked: the application has never been able to leave a timing value on a row whose style does not use it.** Verified finding (manager, 12 November 2026, with git; the current-`main` lines were also read by the `product-manager`):
  - The three timing columns first appear in `routes/workout_plan.py` at commit `04e26d0d`. In that version, at `12c90ac6`, and on current `main` (`routes/workout_plan.py:904-934`), the single validation function sets the timing values a style does not use to `None` before the write: `amrap` clears interval and rounds, `emom` clears the time cap, `standard` clears all three.
  - `git log -S"time_cap_seconds" -- routes/workout_plan.py` lists only three commits (`04e26d0d`, `12c90ac6`, `3532f860`); none removed that clearing.
  - No other writer exists: outside `routes/workout_plan.py`, the only Python reference to `time_cap_seconds` in `utils/`, `routes/`, `scripts/` and `e2e/scripts/` is the `ALTER TABLE` in `utils/db_initializer.py:212-214`.

  *Limit of the finding:* repository history only. ⚠️ **Still unverified: no real user database was inspected.** A stale timing value could reach a plan row only by editing the database outside the application; whether any real database holds one is unknown. If one does, a new backup would capture it faithfully and rule (ii) of criterion 8 would refuse to restore it (Q2).
- ⚠️ **A8 — refusal considers only rows that would otherwise be restored.** A row already skipped because its exercise left the catalog, or because its weight, reps or RIR fail bounds, does not trigger a refusal whatever its execution values are. This keeps refusals to cases where a value would actually have been written.
- ⚠️ **A9 — ADR-008 stands.** Restore tells "missing" from "present" by the stored value, not by `schema_version`. The label moves to `2` because ADR-008's bump-and-branch rule requires it; the number `2` is assumed as the next integer. One existing test, `test_restore_ignores_foreign_schema_version` (`tests/test_program_backup.py:490-520`), uses `2` as its "foreign" version and will need a different value.
- ⚠️ **A10 — the valid-style list and limits may be given a single home under `utils/`** so that restore and the plan page read one definition (utils may not import from routes). This is assumed not to count as "a change to how execution styles are validated on the plan page", provided the plan page's behavior is identical.
- ⚠️ **A11 — restore applies the plan page's limits as they stand when the restore runs.** If those limits are ever narrowed, a backup written under the wider limits would be refused. No such change is planned.
- ⚠️ **A12 — export column names and placement are invented.** Proposed: the three columns sit immediately after the style column, labelled `Time Cap (sec)`, `EMOM Interval (sec)` and `EMOM Rounds` in both view modes, holding plain whole numbers (Q3).
- ⚠️ **A13 — no positional consumer of the workbook is known.** Inside the repository there is none: tests read the sheet by header name and there is no Excel import. Whether the owner has spreadsheets or formulas outside the repository that depend on column letters is unknown.
- ⚠️ **A14 — no new user interface.** The Backup Center's existing error toast carries the refusal, and the detail pane, the plan page, templates and styles are unchanged in both PRs, so no visual baseline moves. The detail payload gains no keys (Q4).
- ⚠️ **A15 — one Gate 0 and one council-reviewed Gate 1 cover both PRs**, as "coordinated plan" in message 1 is read. PR 2 on its own would be Medium.
- ⚠️ **A16 — the two PRs are independent and may merge in either order.**

**Open questions for the user**

*Blocking — PR 1*

- **Q1 — unrecognized style: is refusing the whole restore the handling you want?** It is what criteria 6 and 7 propose. Its cost: a backup containing even one such row cannot be restored through the application at all. Backup rows cannot be edited and there is no import, so the backup's other rows stay out of reach until the row is repaired outside the application. Alternatives:
  - (b) refuse by default, and offer an explicit, user-confirmed "restore the rest and leave these rows out", with those rows reported in `invalid`. Nothing is silent and the plan is replaced only after the user chooses. This needs new interface work.
  - (c) skip and report the row, as bounds failures are handled today. This is consistent with existing behavior, but it replaces the existing plan and deletes the log without the user choosing, which reads as contrary to message 2.
- **Q2 — timing values: do you accept the three rules of criterion 8 and A6?** (i) a value the plan page would reject — not a whole number, or outside the limits — refuses the restore; (ii) a value stored against a style that does not use it refuses the restore; (iii) a style whose own timing value is missing is restored as stored. Rule (ii) is the one to look at: the alternative is to restore such a row exactly as stored. A7 now records that, within this repository's history, the application could never have written such a row, so rule (ii) can refuse only a row whose value was put there outside the application. No real user database was inspected, so whether any such row exists is not known.

*Blocking — PR 2 only*

- **Q3 — where do the three Excel columns go, and what are they called?** Next to the style column (proposed; five existing columns move three to the right), or appended after Exercise Order (no existing column moves, but the timing values sit far from the style)? Are the labels in A12 acceptable?

*Non-blocking — the stated default applies unless you say otherwise*

- **Q4 — should a backup's detail view show the four fields?** Default: no. `GET /api/backups/<id>` items and the detail pane stay as they are. Saying yes adds four keys to each item (an additive response-shape change) and optionally a column to the pane.
- **Q5 — error code and status for a refused restore.** Default: left to the council-reviewed plan, within criterion 6 (standard envelope, non-success status, neither `NOT_FOUND` nor `INTERNAL_ERROR`). It is a new error outcome on an existing endpoint.
- **Q6 — case and spacing variants of a valid style** (`EMOM`, ` emom`). Default: unrecognized, and so refused. The alternative is to accept them as the style they resemble.

### Section 0 sign-off — GATE 0
- [ ] User confirms the acceptance criteria match intent.
- [ ] User reviewed the assumptions and corrected or accepted each one.
- [ ] Blocking questions are answered.

---

*Plan v1, agent provenance, reviewer findings, the response matrix and Plan v2 are added below by `/council-plan` only after Gate 0 is signed.*
