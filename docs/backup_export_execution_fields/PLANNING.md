# Plan Review — Backup/restore and Excel export preserve execution fields (#567, #568)

**Issues**: [#567](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/567) (program backup/restore drops execution fields) · [#568](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/568) (Excel export omits them)
**Branch**: `docs/567-568-execution-fields-planning` · **Brief written**: 2026-11-12 · **Amended**: 2026-11-13
**Status**: Section 0 amended on 13 November 2026 with the owner's answers and four reconciliation points. **Gate 0 signed 13 November 2026** by the owner's message 3 (a forwarded review adopted with "from astra what to do:") — requirements approved as amended. This is not an approval of a plan, an implementation or a merge. Plan v1 was drafted on 13 November 2026 (council Step 1); the three reviewers returned "sound with changes", none blocking; **Plan v2 is written** (council Step 4) with a response matrix covering every finding. **Gate 1 signed 14 November 2026** on the owner's behalf, on the owner's explicit instruction in that day's session, adopting the proposed option for all three owner decisions — see *Gate 1 sign-off* under Plan v2. PR 1 and PR 2 are authorized for implementation; every merge stays owner-only, by PR number and head SHA.
**Planning size** ([`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md#plan-stage-routing)): **Large** — PR 1 changes the `program_backup_items` schema, so Gate 0 (this brief) and a council-reviewed Gate 1 are both required.

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

Three owner messages, reproduced as the manager supplied them to the `product-manager`. Messages 1 and 2 are dated 12 November 2026; message 3 is dated 13 November 2026.

Message 1:

> Yes, I confirm that backup and Excel export should preserve execution style, time cap, EMOM interval and EMOM rounds. Reproduce the current behavior in an isolated database, then prepare a coordinated plan covering backward-compatible restores and the export format. Separate PRs are fine.

Message 2:

> Proceed with the coordinated two-PR planning approach and the required requirements/council steps. My approval of the product direction does not waive those reviews. For compatibility, distinguish missing legacy fields from present but unrecognized values. Missing execution style can default to standard. Don't silently replace an unrecognized style with standard; propose explicit handling that preserves the existing plan if restore cannot safely interpret the backup.

Message 3. As reported by the manager, who received it: the owner's own words in this message were one line — "from astra what to do:" — followed by a pasted review written by a second model, which the owner forwarded as the instruction. The answers below are therefore the forwarded review's wording, adopted by the owner through that line. The relevant part of the paste is quoted verbatim. In the paste the six answers were a tab-separated table headed "Question / Recommended answer"; the manager flattened each row to "Qn: topic — answer" without changing any word.

> 3. #676 — these would be my answers.
> Q1: unknown execution style — Refuse the entire restore. Preserve both the current plan and workout log. Defer a "restore the rest" interface to separate work.
> Q2: invalid timing values — Accept the three proposed rules: reject present invalid or style-incompatible values; preserve missing values as empty. Never silently repair or discard them.
> Q3: Excel columns — Append them after Exercise Order. This preserves existing column positions. Accept Time Cap (sec), EMOM Interval (sec) and EMOM Rounds.
> Q4: show fields in backup details — Keep the proposed default: no UI or detail-response expansion in this work.
> Q5: refusal error — Let the council-reviewed plan select the precise code/status. Require a recognizable validation error and a clear explanation that the plan and log were preserved.
> Q6: case/spacing variants — Accept the strict rule: refuse EMOM,  emom and empty strings, rather than silently normalizing stored data.
>
> Before recording Gate 0 approval, have Fable reconcile these points in the brief:
> - Fix the contradiction in A3/A4: absent columns or SQL NULL mean missing; "" is a present, unrecognized value.
> - Add a reproduction using application-valid rows. The recorded example combines EMOM with a time cap, which the proposed rules reject. Keep that as an invalid-data case, and separately prove round trips for valid AMRAP and EMOM rows.
> - Qualify A11: future tightening of plan-page limits must trigger an explicit backup-compatibility decision, rather than automatically making previously valid backups unrestorable.
> - Update the export criteria to reflect appended columns.
> Then proceed to the formal plan and council review. Approve the requirements as amended—not an implementation or merge yet.

Messages 1 and 2 approve the product direction. By message 2's own terms they are **not** the Gate 0 sign-off on this brief, and they waive no review. Message 3 is the Gate 0 sign-off recorded at the end of this section; in its own words it approves "the requirements as amended—not an implementation or merge yet".

**Problem**

A plan row in `user_selection` carries four execution settings: `execution_style`, `time_cap_seconds`, `emom_interval_seconds` and `emom_rounds`. Two features that claim to carry the plan do not carry all four.

1. **Program backup and restore lose all four, and report success.** A user who sets an exercise to EMOM or AMRAP, saves a backup and later restores it gets every exercise back as `standard` with no timing values. Nothing tells them anything was lost.
2. **The Excel export carries the style but none of its numbers.** The Workout Plan sheet says a row is `emom` or `amrap` and omits the time cap, interval and rounds that give the style its meaning.

Two reproductions are recorded. Both are the manager's measurements; neither was re-run by the `product-manager`, who has no shell. The code read below explains both results exactly.

*Reproduction A — application-valid rows (manager, 13 November 2026, fresh scratch database, Flask test client).* The styles were set through `POST /api/execution_style`, the application's own writer; all three requests returned 200.

| Exercise | Before backup | After restore |
|---|---|---|
| Probe Press | `amrap`, time cap 120, interval NULL, rounds NULL | `standard`, NULL, NULL, NULL |
| Probe Row | `emom`, time cap NULL, interval 60, rounds 10 | `standard`, NULL, NULL, NULL |
| Probe Curl | `standard`, NULL, NULL, NULL | `standard`, NULL, NULL, NULL |

`POST /api/backups` returned 200; the plan was emptied; `POST /api/backups/1/restore` returned 200 with `restored_count` 3, `skipped` `[]`, `invalid` `[]` and the message "Restored 3 exercises from 'probe-valid'". So a valid AMRAP row and a valid EMOM row both lose their settings today while the restore reports success. This is the "before" for criterion 1: after PR 1 the same steps must return all three rows exactly as they were before the backup.

*Reproduction B — invalid-data case (manager, 12 November 2026, isolated scratch database, Flask test client).* A plan row with `execution_style='emom'`, `time_cap_seconds=600`, `emom_interval_seconds=60`, `emom_rounds=10` was inserted by direct SQL, backed up and restored. After restore the row read `standard`, `None`, `None`, `None`, and the restore reported success. The row is a combination the application cannot write: for `emom` the endpoint clears the time cap (`routes/workout_plan.py:930`). It shows the same loss today, but it is **not** a round-trip case. Once backups capture the fields, a backup carrying this row holds a time cap against a style that does not use it, and criterion 8 refuses it; it is that criterion's worked example.

*Verified by reading the code on 2026-11-12; the export positions and the endpoint defaults were re-read on 2026-11-13 (re-verify line numbers before relying on them):*

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
| That path never writes a style without its own timing value | When the timing value is omitted (or is zero), the endpoint fills a default before validating: time cap 60 for `amrap` (`routes/workout_plan.py:905`); interval 60 and rounds 5 for `emom` (`:915-916`); the endpoint docstring says the same (`:1010-1012`). Read on current `main` only |
| The plan page *displays* a NULL or empty-string style as standard | `static/js/modules/workout-plan-helpers.js:110`. This is a fact about display only; it does not decide what restore accepts (A3, A4) |
| Export selects and labels `execution_style` only | `utils/export_service.py:106`, `:130` (`Style`), `:154` (`Execution Style`), and the three query variants at `:261`, `:276`, `:288`. The file contains no reference to the three timing fields |
| Export column positions today | `WORKOUT_PLAN_COLUMNS['order']` (`utils/export_service.py:90-112`) has 21 entries. Headers are written from the first column in the order of the row's keys (`utils/export_utils.py:142-144`, `:255-259`), so the sheet occupies columns A–U: the style is the 16th (P) and Exercise Order is the 21st and last (U). Columns V onward are empty |
| Six `/api/backups` response shapes | Metadata objects carry `id`, `name`, `note`, `backup_type`, `schema_version`, `item_count`, `created_at`; the detail payload adds `items`, each with ten keys (`:393-399`); restore returns `backup_id`, `backup_name`, `restored_count`, `skipped`, `invalid` (`:626-632`) |

**Acceptance criteria**

*PR 1 — backup and restore (criteria 1–11, and 15)*

1. **Round trip.** Given an active plan holding rows of every valid execution style as the plan page saves them — `standard` (no timing values), `amrap` (time cap set, EMOM values empty) and `emom` (interval and rounds set, time cap empty), including rows at the limit values (time cap 10 and 600; interval 15 and 180; rounds 1 and 20) — when a backup is created with `POST /api/backups`, the plan is then changed or emptied, and the backup is restored with `POST /api/backups/<id>/restore`, then every restored row has the same `execution_style`, `time_cap_seconds`, `emom_interval_seconds` and `emom_rounds` it had when the backup was taken, values that were empty are still empty, and the restore reports success with the counts it reports today. *Measured today (reproduction A): the `amrap` and `emom` rows come back as `standard` with no timing values.*

2. **The pre-restore safety snapshot is covered too.** Given the restore confirmation's "Save current plan first" action, when the user takes it, then the snapshot it creates preserves the four fields exactly as in criterion 1.

3. **A legacy backup still restores.** Given a backup saved by a build that predates this change — its rows carry none of the four fields, so all four are missing as criterion 5 defines it — when the new build is running and that backup is restored, then the restore succeeds with the same `restored_count`, `skipped` and `invalid` it would produce today, every restored row reads `execution_style = 'standard'`, and its three timing fields are empty.

4. **Upgrading harms no existing backup.** Given a database that already contains backups, when the new build starts on it for the first time, then every backup is still listed with its name, note, type, item count, creation time and `schema_version` (`1`) unchanged, and each can still be opened, renamed, restored and deleted.

5. **A missing value is never an error.** A value is *missing* when the backup row has no column for the field (a legacy backup) or holds SQL `NULL` in it. An empty string is **not** missing: it is a present value, handled by criteria 6 and 8. Given a backup row whose execution style is missing, when it is restored, then the row is restored as `standard`. Given a backup row in which a timing field is missing, when it is restored, then that field is restored empty — never filled with a default such as 60 or 5 — and the absence alone never causes a refusal.

6. **An unrecognized style refuses the whole restore.** Given a backup in which at least one row that would otherwise be restored holds a present execution style that is not exactly `standard`, `amrap` or `emom` — for example `tabata`, `EMOM`, ` emom` with a leading space, or the empty string `""` — when a restore of that backup is requested, then:
   - the request fails with the application's standard error envelope and a non-success HTTP status, as a recognizable validation error — never `NOT_FOUND` and never `INTERNAL_ERROR`. The precise code and status are chosen by the council-reviewed plan (Q5);
   - the message clearly explains that nothing was restored and that the current plan and the workout log were preserved, and identifies each offending row by routine, exercise and the unrecognized value;
   - no row anywhere is converted to `standard`, and no stored value is normalized, repaired or discarded.

   *(Decided by the owner — Q1, Q5, Q6.)*

7. **A refused restore changes nothing.** Given a restore refused under criterion 6 or 8, when the database is inspected afterwards, then `user_selection` and `workout_log` hold exactly the rows they held before the request — same ids, same values, same order, every logged session intact — and the refused backup is itself unchanged and still listed. In the Backup Center the user sees an error carrying the server's message, no success message, and an unchanged active-program count.

8. **A present but invalid timing value refuses the whole restore.** Given a backup in which at least one row that would otherwise be restored has a recognized or missing style (a missing style counts as `standard`) and a present timing value that is either
   - (i) one the plan page would reject for that style — not a whole number (an empty string included), or outside the limits: time cap 10–600 for `amrap`; interval 15–180 and rounds 1–20 for `emom`; or
   - (ii) stored against a style that does not use it — for example a `standard` row with a time cap, or the `emom` row with a time cap of 600 in reproduction B —

   when a restore is requested, then it is refused exactly as in criteria 6 and 7, with the message naming the row, the field and the stored value. Nothing is silently repaired or discarded. Rule (iii) — a missing timing value is preserved as empty — is criterion 5. *(Decided by the owner — Q2.)*

9. **Today's skip behavior is unchanged.** Given a backup containing rows whose exercise is no longer in the catalog, or whose weight, rep range or RIR fails the plan's bounds, and no execution-field problem in any row that would be restored, when it is restored, then those rows are skipped and reported in `skipped` and `invalid` exactly as today, and every other row is restored with its four execution fields.

10. **The version label follows ADR-008.** Given the new build, when a backup is created, then its `schema_version` is `2` wherever the label is returned or shown; backups created earlier keep `1`. Given two backups identical except for that label, when each is restored, then the outcomes are identical — restore does not consult the label.

11. **Success response shapes are unchanged.** Given any of the six `/api/backups` endpoints, when it succeeds, then its response carries exactly the keys it carries today (listed in the last row of the table above). The only new outcome is the refusal error of criteria 6 and 8.

*PR 2 — Excel export (criteria 12–13)*

12. **The three timing fields are exported, appended after Exercise Order.** Given a plan holding rows of each execution style, when `GET /export_to_excel` is requested in either view mode, then the Workout Plan sheet has three additional columns placed after Exercise Order, in this order and under these headers in both view modes: `Time Cap (sec)`, `EMOM Interval (sec)`, `EMOM Rounds` (columns V, W and X). They carry each row's time cap, EMOM interval and EMOM rounds as the stored whole numbers, with an empty cell wherever the row has no value. Values are written as stored; the export does not validate, default or reject them. *(Decided by the owner — Q3.)*

13. **Nothing already exported changes or moves.** Given the same request, then the 21 existing Workout Plan headers keep their text, their positions (columns A–U) and their values in both view modes; every other sheet, the download's content type and filename pattern, and the `EXPORT_FAILED` error shape are unchanged. An older consumer that reads the sheet by header name sees the same data plus three headers it does not know. An older consumer that reads by column position sees no existing column move; the three new columns occupy V–X, which were empty before.

*Both PRs (criterion 14)*

14. **Each PR stands alone and carries its own record.** Given either PR merged without the other, then the application works and the other feature behaves as it does today. Each PR's description carries migration notes, each updates the test coverage for the behavior it changes, and each corrects, in the same change, the documentation that states the old behavior (`docs/product/BACKEND_SCHEMA.md:625-649`; `docs/product/APP_FLOW.md:636` "Always reads `1` today" and `:644-664`; the export rows of `APP_FLOW.md` for PR 2).

*PR 1 — added 13 November 2026 (criterion 15)*

15. **A later tightening of the plan-page limits cannot silently strand a backup.** Given the build this work delivers and a backup it restores successfully, when a later change narrows a plan-page limit (for example lowers the maximum time cap below 600) or removes a style from the valid list, and records no backup-compatibility decision, then that change cannot both pass the automated test suite and cause that backup to be refused: either what restore accepts is unaffected by it, or a test fails and its failure states that an explicit backup-compatibility decision is required. What restore accepts changes only through a change that says so and records that decision. *(Owner's rule, message 3. The mechanism is left to the plan; see A10 and A11.)*

**Calculation surface**

- `none`.

Verified, not assumed: the four fields are referenced in production Python only by `utils/db_initializer.py` (DDL), `routes/workout_plan.py` (plan read and write) and `utils/export_service.py` (select and label). No module in effective sets, weekly or session summary, progression, volume or fatigue reads them. `program_backup_items` is read only by `utils/program_backup.py`. The export **calls** `calculate_weekly_summary()`, `calculate_exercise_categories()` and `calculate_isolated_muscles_stats()` to fill other sheets; those functions and sheets are not touched. Restore moves stored rows and computes nothing, and the values that feed calculations (sets, rep range, RIR, RPE, weight) are restored as they are today.

This is nonetheless a schema change and a change to backup behavior, so the refactor invariant in `CLAUDE.md` §1 applies in full: migration notes in each PR description and updated test coverage (criterion 14).

**In scope**

- Program backup captures, and restore reinstates, the four execution fields (PR 1).
- Backward-compatible restore of backups written before the change (PR 1).
- Explicit, all-or-nothing refusal when a backup row holds an execution value restore cannot interpret, leaving the plan and the log untouched (PR 1).
- The `schema_version` bump and migration that ADR-008 makes mandatory for this payload change (PR 1).
- A safeguard so that a later tightening of the plan-page limits forces an explicit backup-compatibility decision (PR 1, criterion 15).
- Three timing columns appended after Exercise Order on the Workout Plan sheet of `GET /export_to_excel` (PR 2).
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
- **A "restore the rest" interface** — an explicit, user-confirmed restore that leaves out the rows restore cannot interpret. Deferred to separate work by the owner (Q1).
- **Showing the four fields in a backup's detail view or detail response.** No user-interface or detail-response expansion in this work (Q4).
- **Normalizing or repairing stored execution values** — case folding, trimming, clearing a value its style does not use. Restore refuses instead (Q2, Q6).

**Assumptions made**

Reviewed by the owner in message 3. Entries marked **Decided** or **Owner's rule** are no longer assumptions; they keep their numbers so earlier references still resolve. A ⚠️ marks what is still assumed or unverified.

- ⚠️ **A1 — the issue texts were not read.** The `product-manager` has no shell or network access and the repository holds no copy of #567, #568 or #569. Their content is taken from the manager's summary; #569 is recorded as out of scope by number only.
- ⚠️ **A2 — neither reproduction was re-run here.** Both are the manager's measurements (12 and 13 November 2026). Both are consistent with the code as read.
- **A3 — Decided (message 3, first reconciliation point): "missing" means the backup row has no column for the field (a legacy backup) or holds SQL `NULL` in it**, whichever build wrote it. An empty string is not missing (A4). One consequence: a plan row whose style is SQL `NULL` — reachable only outside the application — is captured as `NULL` and restores as `standard`. The plan page showing a `NULL` or `""` style as standard is a display fact only and does not extend this rule to `""`.
- **A4 — Decided (Q6, and the same reconciliation point): "unrecognized" means any present value that is not exactly one of the three styles.** No case folding and no trimming: `EMOM`, ` emom` and the empty string `""` are present, unrecognized values, and each refuses the restore.
- **A5 — Decided (Q1): the whole restore is refused, and both the current plan and the workout log are preserved.** This departs from today's precedent, where a bad row is skipped and the rest of the restore proceeds. The cost stated in Q1 is accepted: a backup holding such a row cannot be restored through the application until the row is repaired outside it. A "restore the rest" interface is deferred to separate work.
- **A6 — Decided (Q2): the three timing rules are accepted.** (i) A present value the plan page would reject refuses the restore. (ii) A present value stored against a style that does not use it refuses the restore. (iii) A missing value is preserved as empty, neither refused nor defaulted. Nothing is silently repaired or discarded. Confirmed in the code on 13 November 2026: the application cannot write a style without its own timing value, because the endpoint fills a default when one is omitted (`routes/workout_plan.py:905`, `:915-916`). Rule (iii) therefore covers legacy rows, where all four fields are missing, and — for a row such as `amrap` with no time cap — only rows written outside the application. That confirmation is of current `main`; the history of the defaults was not checked.
- **A7 — history checked: the application has never been able to leave a timing value on a row whose style does not use it.** Verified finding (manager, 12 November 2026, with git; the current-`main` lines were also read by the `product-manager`):
  - The three timing columns first appear in `routes/workout_plan.py` at commit `04e26d0d`. In that version, at `12c90ac6`, and on current `main` (`routes/workout_plan.py:904-934`), the single validation function sets the timing values a style does not use to `None` before the write: `amrap` clears interval and rounds, `emom` clears the time cap, `standard` clears all three.
  - `git log -S"time_cap_seconds" -- routes/workout_plan.py` lists only three commits (`04e26d0d`, `12c90ac6`, `3532f860`); none removed that clearing.
  - No other writer exists: outside `routes/workout_plan.py`, the only Python reference to `time_cap_seconds` in `utils/`, `routes/`, `scripts/` and `e2e/scripts/` is the `ALTER TABLE` in `utils/db_initializer.py:212-214`.

  *Limit of the finding:* repository history only. ⚠️ **Still unverified: no real user database was inspected.** A stale timing value could reach a plan row only by editing the database outside the application; whether any real database holds one is unknown. If one does, a new backup would capture it faithfully and rule (ii) of criterion 8 would refuse to restore it (Q2).
- ⚠️ **A8 — refusal considers only rows that would otherwise be restored.** A row already skipped because its exercise left the catalog, or because its weight, reps or RIR fail bounds, does not trigger a refusal whatever its execution values are. This keeps refusals to cases where a value would actually have been written.
- ⚠️ **A9 — ADR-008 stands.** Restore tells "missing" from "present" by the stored value, not by `schema_version`. The label moves to `2` because ADR-008's bump-and-branch rule requires it; the number `2` is assumed as the next integer. One existing test, `test_restore_ignores_foreign_schema_version` (`tests/test_program_backup.py:490-520`), uses `2` as its "foreign" version and will need a different value.
- ⚠️ **A10 — the valid-style list and limits may be given a single home under `utils/`** so that restore and the plan page read one definition (utils may not import from routes). This is assumed not to count as "a change to how execution styles are validated on the plan page", provided the plan page's behavior is identical. **Constraint from A11 and criterion 15:** a shared definition must not be the mechanism by which a later narrowing of the plan-page limits silently changes what restore accepts. Whether restore reads the shared definition, holds its own pinned values, or is guarded some other way is for the plan.
- **A11 — Owner's rule (message 3), replacing the earlier assumption.** Restore applies the styles and limits in force when this work ships: `standard`, `amrap`, `emom`; time cap 10–600; interval 15–180; rounds 1–20. A future tightening of the plan-page limits must trigger an explicit backup-compatibility decision; it must not automatically make previously valid backups unrestorable. Criterion 15 states this as an observable requirement and leaves the mechanism to the plan. The earlier text of A11 — "restore applies the plan page's limits as they stand when the restore runs" — is withdrawn.
- **A12 — Decided (Q3): the three columns are appended after Exercise Order**, labelled `Time Cap (sec)`, `EMOM Interval (sec)` and `EMOM Rounds` in both view modes, holding plain whole numbers. Positions re-verified against the code on 13 November 2026: 21 existing columns, A–U, with Exercise Order last at U, so the new columns are V, W and X. One edge, noted and not a requirement: on a database whose `user_selection` has no `exercise_order` column, the export query omits it (`utils/export_service.py:282-293`) and the sheet has 20 existing columns; the startup migration adds that column, so a running application does not meet this state.
- ⚠️ **A13 — no positional consumer of the workbook is known.** Inside the repository there is none: tests read the sheet by header name and there is no Excel import. Whether the owner has spreadsheets or formulas outside the repository that depend on column letters is unknown. With the columns appended, such a consumer sees no existing column move, so this unknown no longer bears on any criterion.
- **A14 — Decided (Q4): no user-interface or detail-response expansion.** The Backup Center's existing error toast carries the refusal, and the detail payload gains no keys. ⚠️ Still assumed: the detail pane, the plan page, templates and styles need no change in either PR, so no visual baseline moves.
- ⚠️ **A15 — one Gate 0 and one council-reviewed Gate 1 cover both PRs**, as "coordinated plan" in message 1 is read. PR 2 on its own would be Medium.
- ⚠️ **A16 — the two PRs are independent and may merge in either order.**

**Open questions for the user**

None open. All six were answered by the owner's message 3 on 13 November 2026, in the forwarded review's wording quoted under *Raw request*. Each question is kept as it was asked on 12 November, followed by the decision.

- **Q1 — unrecognized style: is refusing the whole restore the handling you want?** It is what criteria 6 and 7 propose. Its cost: a backup containing even one such row cannot be restored through the application at all. Backup rows cannot be edited and there is no import, so the backup's other rows stay out of reach until the row is repaired outside the application. Alternatives:
  - (b) refuse by default, and offer an explicit, user-confirmed "restore the rest and leave these rows out", with those rows reported in `invalid`. Nothing is silent and the plan is replaced only after the user chooses. This needs new interface work.
  - (c) skip and report the row, as bounds failures are handled today. This is consistent with existing behavior, but it replaces the existing plan and deletes the log without the user choosing, which reads as contrary to message 2.

  **Answered:** refuse the entire restore; preserve both the current plan and the workout log; a "restore the rest" interface is deferred to separate work. Recorded in criteria 6 and 7, A5 and *Out of scope*.
- **Q2 — timing values: do you accept the three rules of criterion 8 and A6?** (i) a value the plan page would reject — not a whole number, or outside the limits — refuses the restore; (ii) a value stored against a style that does not use it refuses the restore; (iii) a style whose own timing value is missing is restored as stored. Rule (ii) is the one to look at: the alternative is to restore such a row exactly as stored. A7 now records that, within this repository's history, the application could never have written such a row, so rule (ii) can refuse only a row whose value was put there outside the application. No real user database was inspected, so whether any such row exists is not known.

  **Answered:** the three rules are accepted — reject present invalid or style-incompatible values; preserve missing values as empty; never silently repair or discard them. Recorded in criteria 5 and 8 and A6.
- **Q3 — where do the three Excel columns go, and what are they called?** Next to the style column (proposed; five existing columns move three to the right), or appended after Exercise Order (no existing column moves, but the timing values sit far from the style)? Are the labels in A12 acceptable?

  **Answered:** append them after Exercise Order, which preserves existing column positions; the labels `Time Cap (sec)`, `EMOM Interval (sec)` and `EMOM Rounds` are accepted. Recorded in criteria 12 and 13 and A12. The earlier proposal to place them next to the style column is withdrawn.
- **Q4 — should a backup's detail view show the four fields?** Default: no. `GET /api/backups/<id>` items and the detail pane stay as they are. Saying yes adds four keys to each item (an additive response-shape change) and optionally a column to the pane.

  **Answered:** keep the default — no user-interface or detail-response expansion in this work. Recorded in criterion 11, A14 and *Out of scope*.
- **Q5 — error code and status for a refused restore.** Default: left to the council-reviewed plan, within criterion 6 (standard envelope, non-success status, neither `NOT_FOUND` nor `INTERNAL_ERROR`). It is a new error outcome on an existing endpoint.

  **Answered:** the council-reviewed plan selects the precise code and status. The error must be a recognizable validation error and must clearly explain that the plan and the log were preserved. Recorded in criterion 6.
- **Q6 — case and spacing variants of a valid style** (`EMOM`, ` emom`). Default: unrecognized, and so refused. The alternative is to accept them as the style they resemble.

  **Answered:** the strict rule — refuse `EMOM`, ` emom` and empty strings rather than silently normalizing stored data. Recorded in criterion 6 and A4.

### Section 0 sign-off — GATE 0
- [x] User confirms the acceptance criteria match intent.
- [x] User reviewed the assumptions and corrected or accepted each one.
- [x] Blocking questions are answered.

**Signed 13 November 2026** by the owner's message 3 — a forwarded review adopted with "from astra what to do:" — requirements approved as amended. This is not an approval of a plan, an implementation or a merge. The six answers and the four reconciliation points that message required are made above. The amended text was written after the message, under its instruction to approve "the requirements as amended"; the owner has not read the amended text back.

---

## Plan v1

*Council Step 1, drafted 13 November 2026. Line numbers were re-read in the working tree that day. The checkout was on another branch for unrelated work, so re-verify each against `origin/main` before editing. Criteria (C1–C15), assumptions (A1–A16) and questions (Q1–Q6) refer to Section 0.*

**Goal**: A program backup restores every plan row with the execution style and timing values it had when the backup was taken, refuses — changing nothing — when it holds an execution value it cannot interpret, and the Excel export shows the three timing values beside everything it already exports.

**Scope**
- **In**:
  - **PR 1 — backup and restore** (C1–C11, C15, and its share of C14): four columns on `program_backup_items`, capture in `create_backup()`, a pre-flight check and write in `restore_backup()`, the refusal error on `POST /api/backups/<id>/restore`, `BACKUP_SCHEMA_VERSION` 1 → 2, a pinned restore-acceptance contract, tests, documentation, one ADR.
  - **PR 2 — Excel export** (C12–C13, and its share of C14): three columns appended to the Workout Plan sheet, tests, documentation.
  - Each PR branches from fetched `origin/main` and is mergeable without the other.
- **Out**: everything in Section 0's *Out of scope* list. In particular: no "restore the rest" interface; no change to the backup detail response or pane; no change to plan-page validation behavior; no change to `get_backup_details()`; no template, SCSS or production JavaScript edit in either PR.

**Decisions this plan settles** (left to it by Section 0)

*D1 — Restore decides to refuse before it writes anything.* `restore_backup()` already reads the header, the items and the catalog names before `BEGIN IMMEDIATE` (`utils/program_backup.py:450-478`; `BEGIN` at `:481`, the two `DELETE`s at `:485-486`). The plan adds a pre-flight pass in that same region:

1. Classify every item in today's order: not in the catalog → `skipped` (today's check at `:496`); fails `_validate_restore_item()` → `invalid` (today's check at `:507`); otherwise *restorable*.
2. Check the four execution fields of each restorable item only (A8) and collect every problem, not just the first.
3. If any problem was found, raise a dedicated exception before `BEGIN IMMEDIATE`. No write statement has been issued, so `user_selection` and `workout_log` keep their rows and ids (C7).
4. Otherwise run the transaction as today — the two `DELETE`s, then one `INSERT` per restorable item — and return the same five-key result built from the pre-flight lists.

The exception must **not** be a `ValueError`: the route maps `ValueError` to `NOT_FOUND` 404 (`routes/program_backup.py:172-174`). A second safeguard already exists and is kept: `DatabaseHandler.__exit__` rolls back on any exception (`utils/database.py:520-528`), so a non-SQLite error raised after the `DELETE`s is rolled back too. C9 holds because classification order and the `skipped` / `invalid` channels do not change; the existing fuzz tests pin that.

*D2 — The refusal is `VALIDATION_ERROR`, HTTP 400, with a machine-readable reason.* The route answers a refused restore with `error_response("VALIDATION_ERROR", message, 400, reason="RESTORE_REFUSED", rows=[...])`.

- `VALIDATION_ERROR` / 400 is the repository's existing convention for invalid values (`utils/errors.py:121-123`; `.claude/rules/routes.md` *Input validation*), which is what makes it "recognizable". It is neither `NOT_FOUND` nor `INTERNAL_ERROR`.
- `reason` and `rows` ride in the error object through `error_response()`'s keyword arguments (`utils/errors.py:67`, `:95-100`), the same channel the replace-exercise outcomes use. Tests and any later interface can tell this outcome apart without parsing prose.
- Each entry of `rows` is `{routine, exercise, field, value, problem}`. `value` is rendered to short text (at most 40 characters) inside `utils/` before it leaves, because a stored value can be text, a real number or a blob, and a blob is not JSON-serializable.
- The message has a fixed opening the tests assert on: `Backup '<name>' was not restored. Your current plan and workout log were preserved; nothing was changed.` It then lists up to five offending rows as `<routine> / <exercise>: <problem>` and, beyond five, `and N more`. The full list is always in `rows`.
- No JavaScript changes. The Backup Center's catch shows `Failed to restore backup: <message>` (`static/js/modules/backup-center.js:940-941`), and the toast writes with `textContent` (`static/js/modules/toast.js:294`), so an echoed stored value cannot inject markup.
- Alternative for the reviewers: HTTP 422. It describes "well-formed request, unprocessable stored data" more exactly, but no route in the repository pairs `VALIDATION_ERROR` with 422 today.

*D3 — Two definitions, deliberately separate, and a tripwire between them (A10, A11, C15).*

| Definition | Home | Read by |
|---|---|---|
| Plan-page definition: the three styles, the three limit ranges, the three defaults | `utils/constants.py` (new names; today these are literals at `routes/workout_plan.py:895`, `:905-906`, `:915-916`, `:918`, `:924`, and again at `:1072-1073`, `:1082-1084`, `:1089-1093`) | `routes/workout_plan.py` — the validator and `GET /api/execution_style_options` |
| Restore-acceptance contract: the styles and ranges restore accepts, as its own literals, plus the pure check function | new `utils/backup_execution_contract.py` — imports nothing from the plan-page definition | `utils/program_backup.py` |

- utils never imports from routes; both homes are under `utils/`.
- Moving the plan-page literals is a behavior-preserving refactor. Responses, messages and defaults stay byte-identical, and characterization tests are written first (Sequence, PR 1 step 1).
- **C15 mechanism.** Because restore reads its own contract, narrowing a plan-page limit does not change what restore accepts — previously valid backups stay restorable by default. A tripwire test asserts the two definitions are equal, in both directions, and a second test pins the contract's literal values. Either fails with a message that says a backup-compatibility decision must be recorded under the new ADR before either side changes. Widening the plan page trips it too, which matters as much: the contract must then be widened, or new valid plans would produce backups that restore refuses.
- Fallback if the reviewers judge the `routes/workout_plan.py` edit out of proportion: leave that file untouched and make the tripwire behavioral (probe `POST /api/execution_style` at each boundary and compare `GET /api/execution_style_options`). It is weaker — the validator's numbers and the options endpoint's numbers are already two copies.

*D4 — Migration and version bump, in ADR-008's three parts.*

1. **Bump**: `BACKUP_SCHEMA_VERSION = 2` (`utils/program_backup.py:39`), and the comment block above it (`:26-38`) is rewritten to say version 2 is the first bump that tracks a payload change.
2. **Migration**: `initialize_backup_tables()` adds `execution_style TEXT`, `time_cap_seconds INTEGER`, `emom_interval_seconds INTEGER` and `emom_rounds INTEGER`, all `DEFAULT NULL`, to the `CREATE TABLE` (`:71-86`) and, for existing databases, by one `ALTER TABLE ... ADD COLUMN` per missing column in the shape of the `superset_group` block (`:88-93`). It is idempotent and runs wherever the initializer already runs (`utils/schema_registry.py:134`: startup, erase, the test schema template).
   - `execution_style` defaults to `NULL`, **not** `'standard'`. Legacy rows therefore read as missing (C5), and the upgrade stamps no invented value on any existing backup.
   - No existing row or header is rewritten; legacy headers keep `schema_version` 1 (C4). The header column's own `DEFAULT 1` (`:62`) is left alone — the `INSERT` always supplies the constant (`:215-218`).
3. **Restore branch**: D1 and D5.

`test_restore_ignores_foreign_schema_version` (`tests/test_program_backup.py:490-520`) is parametrized over `[0, 2]`. `2` stops being foreign, so the list becomes `[0, 1, 3]`: below the range, the legacy label, and above. Its docstring is updated; its assertion — identical outcome whatever the label — is C10's second half and does not change. ADR-008's decision stands: restore stays version-blind.

*D5 — What is captured and what is written.*

- **Capture.** `create_backup()` reads `user_selection`'s column names once and selects each of the four fields that exists, as it does for `exercise_order` and `superset_group` (`:191-202`); the `INSERT` (`:229-246`) gains the four columns. A field whose source column is absent is stored as `NULL`. Values are copied as stored — no validation, no normalization at backup time.
- **Restore read.** The item `SELECT` (`:463-468`) gains the four columns.
- **Restore write.** A missing style is written as the literal `'standard'` (an explicit `NULL` would bypass the column default). A recognized style is written as stored. A timing value is written as stored, or `NULL` when missing — never 60 or 5.
- **Insert shape.** Today's four hand-written `INSERT` variants (`:522-605`) are keyed on two optional destination columns; four more optional columns would make that unmanageable. They are replaced by one statement whose column list is assembled from a fixed tuple of column names (never from input), keeping today's rule that a column absent from the destination is left out. `db_initializer.py:209-220` adds all four to `user_selection` at every startup, so that omission is not reachable in a running application.
- **The check** (in `utils/backup_execution_contract.py`), per restorable item:

| Stored style | Stored timing | Outcome |
|---|---|---|
| missing (`NULL`) | all missing | restore as `standard`, timing empty |
| `standard`, `amrap` or `emom` | a field the style uses: missing | restore as stored (rule iii) |
| `standard`, `amrap` or `emom` | a field the style uses: a Python `int` inside the contract's range | restore as stored |
| `standard`, `amrap` or `emom` | a field the style uses: present and not an `int`, or outside the range | refuse (rule i) |
| any, including missing | a field the style does not use: present | refuse (rule ii) |
| present and not exactly one of the three (`tabata`, `EMOM`, ` emom`, `""`) | — | refuse (C6) |

  "Present" means not `NULL`. SQLite's `INTEGER` affinity stores a lossless real such as `60.0` as the integer 60, so a present non-`int` is text, a fractional real or a blob.

*D6 — Export.* In `utils/export_service.py`: the three keys are appended to `WORKOUT_PLAN_COLUMNS['order']` after `exercise_order` (`:111`); both label maps (`:114-136`, `:138-160`) gain `Time Cap (sec)`, `EMOM Interval (sec)`, `EMOM Rounds`; and all three query variants in `build_export_query()` (`:257-263`, `:272-277`, `:284-289`) select the three columns. Headers are written from the first column in key order (`utils/export_utils.py:255-259`), so the sheet becomes A–X with A–U unchanged. A `NULL` already becomes an empty cell (`utils/export_utils.py:279-282`). `utils/export_utils.py` is not edited. One trap for the implementer: `reorder_and_rename_columns()` appends any selected column missing from `order` at the end under its raw key (`:234-238`), so a forgotten label would still "work" with the header `time_cap_seconds`; the exact-header test catches it.

*D7 — One new ADR.* PR 1 adds **ADR-015** to `docs/DECISIONS.md`: restore validates execution fields against a pinned acceptance contract; a present value it cannot interpret refuses the whole restore; changing the plan-page definition or the contract requires a recorded backup-compatibility decision. ADR-008 gains a dated note that version 2 is the first bump under its rule. ⚠️ ADR-015 is the next free number as read today (ADR-014 is the last); a concurrent PR can take it, as happened to ADR-007 in the earlier backup packet. Renumber before merge if so.

**Artifacts**

*PR 1 — backup and restore*

| Path | Change | Notes |
|---|---|---|
| `utils/constants.py` | modify | Plan-page execution definition: styles, limit ranges, defaults (D3) |
| `routes/workout_plan.py` | modify | Validator (`:895-934`) and options endpoint (`:1060-1094`) read the constants; behavior identical |
| `utils/backup_execution_contract.py` | new | Restore-acceptance contract as its own literals, and the pure check (D3, D5). No database access, no logger needed |
| `utils/program_backup.py` | modify | Bump and comment (`:26-39`); migration (`:71-93`); capture (`:191-246`); refusal exception; pre-flight, read and single-statement write in `restore_backup()` (`:429-632`) |
| `routes/program_backup.py` | modify | Map the refusal exception to the D2 response, ahead of the `ValueError` branch (`:172`); docstring |
| `tests/test_backup_execution_contract.py` | new | Unit tests for the check; the tripwire and the literal pin (C15) |
| `tests/test_program_backup_execution_fields.py` | new | C1–C11 at function and API level; legacy and upgrade cases; refusal leaves plan and log untouched |
| `tests/test_program_backup.py` | modify | `_BACKUP_OWNED_COLUMNS` (`:929`) and `_seed_known_program` gain the four fields; foreign-version list → `[0, 1, 3]` (`:490`) |
| `tests/test_program_backup_restore_fuzz.py` | modify | A8 cases: a row already skipped for catalog or bounds does not trigger a refusal. Reuses `_seed_tampered_backup` (`:73`) and `_seed_backup_with_rows` (`:454`) |
| `tests/test_phase3_features.py` | modify | Boundary characterization tests for `POST /api/execution_style`, added **before** the constants move |
| `e2e/program-backup.spec.ts` | modify | One test: a mocked refusal response shows the error toast, no success message, unchanged program count (C7's Backup Center half) |
| `docs/product/BACKEND_SCHEMA.md` | modify | `program_backup_items` table and the paragraph at `:645-649`; `schema_version` note (`:619-623`) |
| `docs/product/APP_FLOW.md` | modify | Schema stat (`:636`), Restore row (`:638`), *What restore actually does* (`:644-664`) |
| `docs/DECISIONS.md` | modify | ADR-015; dated note on ADR-008 (D7) |
| `docs/test_inventory/**` | regenerate | Required: tests are added to `tests/` and `e2e/` |

*PR 2 — Excel export*

| Path | Change | Notes |
|---|---|---|
| `utils/export_service.py` | modify | D6 |
| `tests/test_exports.py` | modify | Exact 24-header list in both view modes; values per style; empty cells; A–U unchanged |
| `docs/product/APP_FLOW.md` | modify | Excel export row (`:224`) names the three appended columns |
| `docs/test_inventory/**` | regenerate | Required: tests are added |

**Effort**: PR 1 **L**, PR 2 **S** · **Owner**: implementation agent assigned by the manager after Gate 1; the owner merges · **Depends on**: Gate 1 sign-off on Plan v2. The PRs do not depend on each other; both regenerate `docs/test_inventory/` and both edit `APP_FLOW.md` (different sections), so whichever merges second rebases onto `main`, regenerates the inventory and re-runs its gates on the rebased tree.

**Sequence**

*PR 1*
1. Branch from fetched `origin/main`. Add boundary characterization tests for `POST /api/execution_style` (10 and 600, 15 and 180, 1 and 20 accepted; 9, 601, 14, 181, 21 rejected; omitted values defaulted to 60 / 60 / 5; unused fields cleared). They must pass on unmodified code.
2. Move the plan-page literals to `utils/constants.py` and have `routes/workout_plan.py` read them. Step 1's tests, `TestExecutionStyles` (`tests/test_phase3_features.py:24-165`) and `e2e/api-integration.spec.ts:189` stay green with no edits.
3. Add `utils/backup_execution_contract.py`, its unit tests, the tripwire and the literal pin.
4. Migration, capture and bump in `utils/program_backup.py`; legacy and upgrade tests (C3, C4); foreign-version list (C10).
5. Restore: read, pre-flight, refusal exception, single-statement write; route mapping; the remaining pytest tests (C1, C2, C5–C9, C11).
6. The mocked-refusal Playwright test.
7. Documentation, ADR-015, the ADR-008 note, the module comment.
8. Regenerate `docs/test_inventory/`; run the pyright baseline diff.
9. Run the gates below, including the manual smoke and the mutation arms; open the PR with migration notes; mark it ready and stop. No merge without the owner's confirmation naming the PR.

*PR 2*
1. Branch from fetched `origin/main`. Add the export tests; they fail on unmodified code.
2. Change `utils/export_service.py` (D6); tests pass.
3. Update `APP_FLOW.md`; regenerate `docs/test_inventory/`; run the pyright baseline diff.
4. Run the gates below; open the PR with migration notes; mark it ready and stop.

**Test coverage by criterion**

| Criterion | Test (PR) |
|---|---|
| C1 | API round trip with styles set through `POST /api/execution_style` — the three shapes of reproduction A plus every limit value; and the row-for-row integrity tests once `_BACKUP_OWNED_COLUMNS` includes the four fields (PR 1) |
| C2 | Covered by C1's API test: "Save current plan first" calls the same `POST /api/backups` (`backup-center.js:1112`). No separate browser test |
| C3, C4 | Build a pre-change `program_backup_items` (the four columns dropped), seed a version-1 header and rows by direct SQL, run `initialize_backup_tables()` twice; header and old columns unchanged, new columns `NULL`; list, open, rename, restore and delete all work; restored rows read `standard` with empty timing (PR 1) |
| C5 | `NULL` style with `NULL` timing → `standard`; `amrap` with `NULL` time cap → `amrap`, still `NULL`; `emom` with one of its two values `NULL` → as stored (PR 1) |
| C6 | Parametrized over `tabata`, `EMOM`, ` emom`, `""`: 400, `VALIDATION_ERROR`, `reason`, the fixed opening sentence, each offending row named in `rows`; no row converted (PR 1) |
| C7 | For each refusal class: `SELECT *` of `user_selection` and `workout_log` ordered by id, and of both backup tables, equal before and after — ids included. Backup Center half: the mocked Playwright test (PR 1) |
| C8 | Rule (i): `'abc'`, `""`, `12.5`, `0`, `-5`, 9 and 601 (time cap), 14 and 181 (interval), 0 and 21 (rounds). Rule (ii): `standard` + time cap; `amrap` + interval; `amrap` + rounds; reproduction B's row (`emom`, 600, 60, 10); missing style + time cap (PR 1) |
| C9, A8 | Existing fuzz tests unchanged and green; new cases where a catalog-missing or bounds-invalid row also carries a bad style still restore successfully with that row in `skipped` / `invalid` (PR 1) |
| C10 | New backup persists and returns `schema_version` 2 (literal); foreign-version test over `[0, 1, 3]` (PR 1) |
| C11 | Exact key sets for the success responses of all six endpoints, including the ten item keys of the detail payload (PR 1) |
| C12, C13 | Exact header row, 24 entries, for `simple` and for `advanced`; A–U equal to today's 21 in order; V–X values for one row of each style; empty cells for missing values; other sheets and download headers by the existing tests (PR 2) |
| C14 | PR description carries migration notes; the documentation rows above are in the same PR (both) |
| C15 | Tripwire (plan-page definition equals the contract) and literal pin of the contract, each with the decision-required message (PR 1) |

*Mutation arms, recorded in the PR description* — each applied, shown red, and reverted: (PR 1) drop the four columns from the restore `INSERT` → C1 red; move the refusal after the two `DELETE`s → C7 red; write `NULL` instead of `'standard'` for a missing style → C3 red. (PR 2) drop the three columns from the export query → C12 red.

**Migration notes each PR description must carry**

- **PR 1**: four nullable columns added to `program_backup_items` by an idempotent startup `ALTER`; no existing row rewritten. `BACKUP_SCHEMA_VERSION` 1 → 2: new backups report `schema_version` 2, earlier ones keep 1, restore ignores the label. Behavior change: a restored row now carries its execution style and timing values, where before it was reset to `standard`. New outcome: `POST /api/backups/<id>/restore` can answer 400 `VALIDATION_ERROR` with `reason: RESTORE_REFUSED`, having changed nothing. Success response shapes unchanged. Reverting the PR leaves the columns in place harmlessly; a build without it restores a version-2 backup without the four fields, as ADR-008 already accepts.
- **PR 2**: the Workout Plan sheet of `GET /export_to_excel` gains columns V–X (`Time Cap (sec)`, `EMOM Interval (sec)`, `EMOM Rounds`) in both view modes; columns A–U and every other sheet are unchanged.

**Expected gates** (drafted by `product-manager` from [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md); `test-strategist` confirms or corrects)

*PR 1* — change types: DB / schema (`utils/program_backup.py`), Route / API (`routes/program_backup.py`, `routes/workout_plan.py`), Business logic (`utils/constants.py`, `utils/backup_execution_contract.py`), E2E spec.
- pytest: **full suite** (DB / schema row). The files this PR adds or changes are `tests/test_backup_execution_contract.py`, `tests/test_program_backup_execution_fields.py`, `tests/test_program_backup.py`, `tests/test_program_backup_restore_fuzz.py`, `tests/test_phase3_features.py`; `tests/test_app_factory.py` runs inside the full suite.
- e2e: `e2e/program-backup.spec.ts` (changed), then the full Chromium suite through `/verify-suite`. No visual surface changes; a visual red is judged against the existing ledger and never resolved with `--update-snapshots`.
- manual backup/restore smoke (DB / schema row), on a scratch database with `DB_FILE` set explicitly, never the real one: (a) start the new build on a copy that holds pre-change backups — they are listed unchanged, Schema reads 1; (b) set one exercise to AMRAP and one to EMOM, save a backup (Schema reads 2), change both, restore — the settings return; (c) restore a pre-change backup — every row is standard; (d) alter one backup row's style by direct SQL, restore — the error toast appears and the plan and log are intact; (e) "Save current plan first", then restore.
- other: `Test Inventory Drift` (regenerate, commit); pyright baseline diff (no net-new diagnostics); the mutation arms above. Final gate `/verify-and-polish`.
- reviewers at code time: `code-reviewer`, `architecture-reviewer` (DB / schema row), `product-risk-reviewer` (a route gains a new response outcome), `unslop-reviewer`.

*PR 2* — change type: Business logic (`utils/export_service.py`).
- pytest: `tests/test_exports.py`, plus every test module that names `utils.export_service` or `/export_to_excel` (`tests/test_export_weekly_summary_sheet.py`, `tests/test_export_blank_rep_bounds_contract.py`, `tests/test_export_blank_rep_bounds_gate0.py`, `tests/test_rep_range_integrity.py`, `tests/test_ui_flows.py`).
- e2e: none required by the change-type row; `e2e/api-integration.spec.ts` covers the endpoint's status and is run as a cheap check.
- other: `Test Inventory Drift`; pyright baseline diff; the mutation arm; open one downloaded workbook by hand in each view mode. Final gate `/unslop`.
- reviewers at code time: `code-reviewer`, `unslop-reviewer`.

**Open points for the council** (none needs the owner unless a reviewer disagrees with the plan's choice)

- D2: 400 or 422 for the refusal.
- D3: whether the `routes/workout_plan.py` constants move belongs in PR 1, or the behavioral-tripwire fallback is enough.
- D5: replacing the four `INSERT` variants on the restore path with one assembled statement.
- C7: whether one mocked Playwright test is the right weight for the Backup Center half.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `ae560180f77de4a02` | Author of Section 0 and of Plan v1 — the same agent, resumed by the manager for each write. ID supplied by the manager. |
| `product-manager` — response matrix + Plan v2 | `ae560180f77de4a02` | Author of the matrix and Plan v2. ID supplied by the manager. |
| `architecture-reviewer` | `a6c8cf93ae9afde4b` | Step 2 reviewer. Verdict: sound with changes; none blocking. |
| `test-strategist` | `a8902d8615bb78daf` | Step 2 reviewer. Verdict: sound with changes; none blocking. |
| `product-risk-reviewer` | `a850a542dbf97a312` | Step 2 reviewer. Verdict: sound with changes; none blocking. |

**Same product-manager resumed for the matrix + Plan v2?** `yes` (resumed via `SendMessage` to the Plan v1 agent ID).

**Evidence gap** — `none` for agent IDs and continuity.

*Transcription note.* The reviewers are read-only and returned their reports to the manager, who passed them to the `product-manager` in the Step 4 message. The text under *Reviewer findings* is each report as returned, with one rendering fix made before it reached the `product-manager`: `<problem>` had arrived HTML-escaped. The proposed dispositions in the response matrix are the manager's synthesis; the owner confirms them at Gate 1.

---

## Reviewer findings

*Council Step 2, 13 November 2026. Each report is reproduced verbatim inside a fenced block, so its own headings and tables stay out of this document's outline. All three reviewed Plan v1. See the transcription note under Agent provenance.*

### architecture-reviewer (agent `a6c8cf93ae9afde4b`)

````markdown
**Verdict: sound with changes.** I found no blocking issues. Two findings need a fix before Gate 1, and the rest are notes. The module boundaries, registration, DB-access and response-contract rules hold, and the structure of D1 to D7 stands.

## Findings

**1. should-fix. D3 and Artifacts: take the plan's own fallback and leave `routes/workout_plan.py` untouched in PR 1.**
- Evidence:
  - The validator (`routes/workout_plan.py:895-934`) and options endpoint (`:1060-1094`) hold the literals. The file has 70 references to the four fields.
  - The plan itself says the restore contract "imports nothing from the plan-page definition". So after the move there are still two copies of every number, one in `utils/constants.py` and one in the contract.
  - The move also pulls the three plan-page defaults (60 / 60 / 5) into `utils/constants.py`. Restore never uses defaults, so the contract has no need of them.
- Cost if left: PR 1 edits a hot route file, and its characterization step (Sequence 1-2) is needed only to protect that edit. Section 0 puts any change to plan-page validation out of scope, and A10 asks for the move only conditionally. The C15 requirement does not need it.
- Change:
  - Leave `routes/workout_plan.py` alone.
  - Make the tripwire behavioral. A test can import `_validate_and_normalize_execution_params` from routes. For each style, probe both limits of each range and one step outside, and assert the verdict matches the contract.
  - Compare `GET /api/execution_style_options` `limits` against the contract.
  - Drop the constants move, the three defaults, and the new `tests/test_phase3_features.py` characterization tests from PR 1.
  - If the owner wants one plan-page home, make that a separate refactor.
- This is my position on open point D3.

**2. should-fix. D3 tripwire: its coverage must include the style set, and the plan should say which direction each assertion catches.**
- Evidence: `valid_styles` at `:895` is an unordered set, and the error message at `:899` joins it in set order. The plan lists "styles" in the tripwire but does not say how it reads the route's list.
- Cost: with the behavioral probe from finding 1, removing or adding a style is detected only if each contract style is posted and one unlisted style is also posted. If the plan leaves this implicit, an implementer may probe only the numeric limits. Then C15's "removes a style" case passes the suite silently.
- Change: state in D3 that the probe covers (a) each of `standard`, `amrap` and `emom` accepted, (b) one rejected style, and (c) every limit boundary and one step beyond.

**3. should-fix. D2 / D1: the exception's home and the route's reason string need pinning.**
- Evidence: the route's catch order is `ValueError`, then bare `Exception` (`routes/program_backup.py:172-177`). The plan says the new exception maps "ahead of the `ValueError` branch" but does not name the class or its module.
- Cost: if the refusal exception subclasses `ValueError`, the new `except` placed first still works. But any other caller that catches `ValueError` around `restore_backup()` turns a refusal into a 404 `NOT_FOUND`. The tests, including `tests/test_program_backup_restore_fuzz.py`, call `restore_backup()` directly.
- Change: the plan should say the exception is defined in `utils/program_backup.py`, derives from `Exception` directly, and carries `rows` (already rendered as short text) and the backup name. The route builds the message from those.

**4. note. Position on D2: keep 400 `VALIDATION_ERROR`.**
- Evidence:
  - `ERROR_CODES` (`utils/errors.py:121-129`) maps `VALIDATION_ERROR` to 400.
  - It also lists `UNPROCESSABLE_ENTITY` as 422, but the plan found no caller using that code, so adopting it adds an unused outcome.
- `error_response()` accepts keyword extras (`utils/errors.py:67`, `:95-100`), so `reason` and `rows` ride along, as the replace-exercise code does. The Backup Center's catch is unchanged.
- Caveat to add to D2: those extras are nested under `error`, not at the top level. Tests should read `body["error"]["reason"]` and `body["error"]["rows"]`.

**5. note. Position on D5: replacing the four INSERT variants with one assembled statement is acceptable.**
- Evidence: the four variants at `utils/program_backup.py:522-605` are keyed on two booleans. Adding four optional columns would make 64 variants.
- A fixed tuple of column names filtered by `_check_column_exists()` keeps injection out and preserves "absent destination column is omitted".
- Condition: keep the placeholders and parameter tuple built from the same filtered list, so the order cannot drift. The existing fuzz and integrity tests are the guard for that.

**6. note. D4: the migration shape is right.**
- Evidence:
  - `initialize_backup_tables()` already has one `ALTER` block for `superset_group` (`:88-93`), and `utils/schema_registry.py:134` already calls it, so no registry change is needed.
  - `schema_registry.py:23-24` already lists both backup tables in the drop order.
- Defaulting `execution_style` to `NULL` rather than `'standard'` is what keeps legacy rows distinguishable as missing. Without that, C3 and C5 are not separable.
- Add one line: write the new columns in a loop over a tuple of (name, type), not four copied `if` blocks.

**7. note. D1 / A8: the pre-flight reads outside the write lock.**
- Evidence: the header, items and catalog reads (`:451-474`) happen before `BEGIN IMMEDIATE` (`:481`). That is already true today, and the plan's pre-flight sits in the same region.
- Impact: none new for a single-user local app, so no change is needed.
- Check I confirmed: raising before `:481` issues no write. `DatabaseHandler.__exit__` also rolls back on any exception (`utils/database.py:520-528`), so a later non-SQLite error is covered. The existing `except sqlite3.Error` at `:608` does not cover that case, so the plan's "second safeguard" claim is accurate.

**8. note. D6 export: confirmed and low-risk.** I confirmed the three query variants, the 21-entry `order` list, and `exercise_order` last. The plan's trap (a forgotten label falling back to the raw key) is real and the exact-header test covers it. I did not open `utils/export_utils.py` or the label maps at `:114-160`.

**9. note. Open point C7 (one mocked Playwright test).** This is outside my charter. I will say only that C2's coverage by the API test is consistent with the repository's existing patterns.

## Open points

| Point | Position |
|---|---|
| D2: 400 or 422 | 400 `VALIDATION_ERROR`, with the nested-`error` caveat above |
| D3: move constants or use the fallback | Fallback, as in findings 1 and 2 |
| D5: one assembled INSERT | Acceptable, with the parameter-order condition |
| C7: Playwright weight | Not in my charter |

## Checked and found correct
- **Boundaries and registration:**
  - `utils/backup_execution_contract.py` imports nothing from `routes/`.
  - No new blueprint, so `create_app()` and `EXPECTED_BLUEPRINTS` need no edit.
  - No new table, so the schema-registry and `clean_db` registration rules do not apply.
  - All DB access stays inside `with DatabaseHandler() as db:`.
  - The refusal uses `error_response()`.
  - No `utils/__init__.py` re-export is proposed.
- **Normalization:** nothing persisted is a canonical enum, and the plan correctly refuses rather than normalizes.
- **Plan claims against code:**
  - The restore ordering, line numbers and the `ValueError` to 404 mapping are accurate.
  - The `DELETE` statements at `:485-486`, the four-INSERT shape, and the validator literals match.
  - `db_initializer.py:209-220` matches, and `BACKUP_SCHEMA_VERSION = 1` at `:39`.
  - ADR-008 is at `docs/DECISIONS.md:107-116`.
  - `get_backup_details()` selects explicit columns (`:393-396`), so the new columns do not leak into the detail payload.
  - The only `schema_version` reader in the frontend (`backup-center.js:605`) is a display fallback.
- **Other writers of the four fields:** `INSERT INTO user_selection` in `utils/plan_generator.py:1446` and `utils/exercise_manager.py:56,61` do not name the execution columns. Only `routes/workout_plan.py:973` writes them, as the plan says.
- **Test touchpoints:** the `[0, 2]` parametrization at `tests/test_program_backup.py:490` is real. The monkeypatch at `:477` and the persisted-version assertion at `:69` read the constant, so they survive the bump. `e2e/scripts/prepare_e2e_db.py:55` only names the table, with no column list.

## Not checked
- The `docs/DECISIONS.md` ADR-014/015 numbering beyond the grep. The "ADR-014 is the last" claim holds only if no later heading exists.
- The `utils/export_utils.py` line references, and the label maps at `export_service.py:114-160`.
- `tests/test_program_backup_restore_fuzz.py` helper names and lines (`:73`, `:454`), and `_BACKUP_OWNED_COLUMNS` at `:929`.
- The `backup-center.js:940` and `toast.js:294` claims, the `APP_FLOW.md` and `BACKEND_SCHEMA.md` line references, and the test-inventory regeneration.
- CI gate names and effort sizing, which are test-strategist's charter.

I wrote nothing to disk.
````

### test-strategist (agent `a8902d8615bb78daf`)

````markdown
## Verdict: sound with changes

The plan maps every criterion to a test. I found no blocking problem, but five should-fix items are needed before Gate 1. The main ones are one mutation arm that cannot go red as written, a C15 tripwire that does not watch the live plan-page validator, and an e2e test that cannot fail where the plan says it can.

## Required gates

- **pytest, PR 1: full suite.** The DB / schema row (`utils/program_backup.py`) requires it. It must include:
  - `tests/test_program_backup.py`
  - `tests/test_program_backup_restore_fuzz.py`
  - `tests/test_phase3_features.py`
  - the two new files, `tests/test_backup_execution_contract.py` and `tests/test_program_backup_execution_fields.py`
- **pytest, PR 2:** `tests/test_exports.py` plus the five modules the plan names. I confirmed all six mention `export_service` or `/export_to_excel` (grep counts). The PR 2 gate is correct.
- **e2e, PR 1:** `e2e/program-backup.spec.ts`, then the full Chromium suite via `/verify-suite`. There is no visual surface.
- **e2e, PR 2:** none required. `e2e/api-integration.spec.ts` as a cheap check is fine.
- **Other, both PRs:** `Test Inventory Drift` (regenerate and commit), the pyright baseline diff, the manual backup/restore smoke on a scratch `DB_FILE` (PR 1 only), and the mutation arms.
- **Fixture impact:** none. `tests/conftest.py:258-259` already lists both backup tables in `clean_db`. There is no new blueprint or table.
- **Known red:** `e2e/program-backup.spec.ts:79` is the documented flake in QUALITY_GATE "Known exceptions". The plan edits that spec but never names it. The "can create a backup" test is at line 80. See finding 7.

## Findings

**1. should-fix — mutation arm "move the refusal after the two `DELETE`s → C7 red" cannot go red.**
- **Plan section:** "Mutation arms", D1.
- **Evidence:**
  - `utils/database.py:520-524`: `__exit__` calls `connection.rollback()` when any exception is in flight. D1 itself cites this safeguard.
  - `utils/program_backup.py:608-610` rolls back only `sqlite3.Error`, but the new exception also propagates out of the `with` block and hits `__exit__`.
- **Failure if left:** after that mutation the refusal still raises, the `DELETE`s are rolled back, and the "before equals after" snapshot in C7 is still equal. The implementer cannot show the arm red. They either skip it or fake it.
- **Change:**
  - Replace the arm with "pre-flight raises nothing, so the restore proceeds" (C6, C7 and C8 red).
  - Add a call-spy test for "refused means no `DELETE` and no `INSERT` was issued". Use the monkeypatch pattern already at `tests/test_program_backup.py:263-273`. This pins D1's real property, "decides before it writes", which the snapshot test cannot see.

**2. should-fix — the C15 tripwire compares constants, not the live plan page.**
- **Plan section:** D3, C15.
- **Evidence:** the tripwire asserts `utils/constants.py` equals the contract. The route reads those constants only if the implementer moves every literal. The plan lists eight literal sites (`routes/workout_plan.py:895, 905-906, 915-916, 918, 924, 1072-1073, 1082-1084, 1089-1093`). I did not read those lines.
- **Failure if left:** someone reintroduces a local literal in the route. The plan page changes, the constants-equality test stays green, and the widening-direction protection is lost. C15's "restore unaffected" half still holds, because restore reads its own contract.
- **Change:** make the tripwire probe `POST /api/execution_style` at each boundary and compare `GET /api/execution_style_options` against the contract. That is the plan's own fallback, and it is the only version that observes the real plan page. Keep the literal-pin test. The probe's failure message must say "record a backup-compatibility decision (ADR-015)".

**3. should-fix — the Step 1 characterization misses the options endpoint.**
- **Plan section:** Sequence, PR 1 step 1.
- **Evidence:** `tests/test_phase3_features.py:27-50` checks only key presence and the `full_name` strings. It never checks the numeric ranges or defaults. The existing tests also never test a boundary:
  - the only rejection test is `time_cap_seconds: 5` (`:130-143`)
  - the only accepted values are 90, 45 and 8
  - the omitted-value defaults of 60, 60 and 5 are untested
  - the plan's boundary list (10/600, 15/180, 1/20) is entirely new
- **Failure if left:** the constants move at `:1072-1093` is a refactor with no safety net for the options payload.
- **Change:** add to Step 1 a full-JSON characterization of `GET /api/execution_style_options` (ranges, defaults, labels), passing on unmodified code.

**4. should-fix — the existing restore-rollback test depends on the `INSERT` text.**
- **Plan section:** D5, replacing the four `INSERT` variants.
- **Evidence:** `tests/test_program_backup.py:266-273` monkeypatches `DatabaseHandler.execute_query`. It matches the substring `"INSERT INTO user_selection"` and raises on the third call. It requires one `execute_query` call per restored row.
- **Failure if left:** an assembled statement that changes the leading text, or batches through `executemany`, makes this test pass for the wrong reason or fail unexpectedly. It is also the only test of rollback mid-restore.
- **Change:** state in the plan that the assembled statement begins `INSERT INTO user_selection` and runs once per row through `execute_query(..., commit=False)`.

**5. should-fix — D5's destination-column logic is only partly covered.**
- **Plan section:** D5.
- **Evidence:** `test_program_backup.py:1074-1110` covers restore into a schema where `exercise_order` is dropped (`DROP COLUMN` at `:1079`). I found no test with `superset_group` absent, or both absent. The plan's single statement replaces all four branches (`utils/program_backup.py:522-605`).
- **Failure if left:** a bug in the "omit absent column" assembly for the other combinations is invisible.
- **Change:** parametrize the existing drop-column test, or add one that drops `superset_group` and one that drops both. Add the four execution columns to `_BASE_OWNED_COLUMNS` handling. Plan v1 only says `_BACKUP_OWNED_COLUMNS` gains the fields (`:929`).

**6. should-fix — the export tests must pin the 21 old headers as literals.**
- **Plan section:** C12/C13 and the PR 2 test row.
- **Evidence:**
  - No test in `tests/` mentions `Execution Style`, `Exercise Order` or `WORKOUT_PLAN_COLUMNS`. I grepped, with zero hits.
  - The current tests read the sheet by name only for six columns (`test_exports.py:304-311`).
  - So "A–U equal to today's 21" has no baseline in the repo.
  - If the test derives the 21 from `WORKOUT_PLAN_COLUMNS['order'][:21]`, it passes tautologically after any reorder.
  - Simple view labels the style `Style` and advanced view `Execution Style` (`utils/export_service.py:130, :154`).
- **Failure if left:** a column move in A–U could pass the test.
- **Change:**
  - Capture the 21 headers per view mode from `main` as literal lists in the test.
  - Add a mutation arm "insert a new column before `exercise_order` → C13 red".
  - The plan's claim that "other sheets … by the existing tests" is only partly true. Existing tests cover content type, filename pattern and `EXPORT_FAILED` (`test_exports.py:320-345, :823`) and the weekly-summary sheet, but nothing asserts the sheet-name list or other sheets' headers. Add one assertion on the sheet-name list if C13's "every other sheet" is to be defended.

**7. should-fix — the mocked Playwright test is weak where the plan leans on it, and the known red goes unnamed.**
- **Plan section:** C7 Backup Center half, open point 4.
- **Evidence:**
  - Existing restore-result tests mock `**/api/backups/*/restore` with `page.route` (`e2e/program-backup.spec.ts:169, 204, 242, 291`). The pattern is established.
  - `backup-center.js:940-941` is the catch the plan relies on. It shows `Failed to ${pendingAction} backup: ${error.message}` and re-enables the buttons.
  - With a mocked 400, "unchanged active-program count" is vacuous, because nothing server-side can have changed.
- **Failure if left:** the e2e adds an inventory count and the known-red exposure but proves less than C7 claims for the UI.
- **Change:**
  - Keep one mocked test. Assert the error toast contains the server message, `#backup-restore-result` is not shown, and the confirm button is re-enabled.
  - Drop the active-program-count claim from the mocked test. The real count is C7's pytest half.
  - Add "if `program-backup.spec.ts:79` reds, rerun in isolation per QUALITY_GATE" to the PR 1 gate.

**8. note — C1's tests need a different fixture than `workout_plan_factory`.**
- **Evidence:** `tests/conftest.py:344-345` inserts only eight columns with no execution fields.
- **Change:** C1/C2 must go through `POST /api/execution_style` with the shared `client`, as the plan says. The `test_client` alias at `test_phase3_features.py:366` is module-local, so the new file cannot reuse it. Direct SQL is needed for the limit-value and invalid-data rows.

**9. note — C4 legacy construction.**
- **Evidence:** `schema_template` already carries the new columns after the change.
- **Change:** build the legacy table with the old `CREATE TABLE` text, or with `DROP COLUMN` (already used at `test_program_backup.py:1079`). I did not read `tests/fixtures/make_old_schema_db.py`, which mentions `program_backup_items` and may already provide this.

**10. note — C10's "shown" has no UI test.**
- **Evidence:** `backup-center.js:605` renders `schema_version ?? 1`. No e2e or JS test pins it. `test_program_backup.py:69` asserts against the constant, and `:601-626` asserts key presence only.
- **Change:** the literal `== 2` test for new backups in the plan is sufficient. The UI is a pass-through, and the manual smoke step (b) covers it.

**11. note — SQLite affinity and C8.**
- **Evidence:** D5's "present non-`int` is text, fractional real or blob" is right. A numeric-looking text such as `'60'` stored in an `INTEGER` column is coerced to 60 and accepted.
- **Change:** build the C8 rows through `_seed_tampered_backup` (`tests/test_program_backup_restore_fuzz.py:73-126`). It asserts `typeof()`, so the stored type is what the test claims. Reuse it in the new file, not only in the fuzz file.

## Positions on the open points (those in charter)

- **D2, 400 vs 422:** no test-cost difference. Assert the chosen status and `reason` literally. 400 matches the repo convention.
- **D3, constants move vs behavioral tripwire:** keep the move, but make the behavioral probe the tripwire (finding 2). Add the options-endpoint characterization (finding 3). The constants-equality test alone is the weaker design.
- **D5, single `INSERT`:** acceptable if findings 4 and 5 are met. Without them the refactor drops coverage.
- **C7, one mocked Playwright test:** right weight, per finding 7. A real-server e2e adds flake exposure for no extra proof.

## Checked and found correct

- **`TestExecutionStyles`:** the plan's `tests/test_phase3_features.py:24-165` is exact.
- **Foreign-version test:** `test_restore_ignores_foreign_schema_version` at `:490-520` is parametrized `[0, 2]`. The `[0, 1, 3]` change is correct and its assertion is version-blind.
- **Fuzz helpers:** `_seed_tampered_backup` at `:73` and `_seed_backup_with_rows` at `:454` exist. `_BACKUP_OWNED_COLUMNS` is at `test_program_backup.py:929` and `_seed_known_program` at `:956`.
- **Restore ordering in `utils/program_backup.py`:** header, items and catalog are read before `BEGIN IMMEDIATE` at `:481`. The `DELETE`s are at `:485-486`. Rollback is on `sqlite3.Error` only (`:608-610`).
- **Route mapping:** `routes/program_backup.py:172-177` maps `ValueError` to `NOT_FOUND` and everything else to `INTERNAL_ERROR`. The plan's "must not be a `ValueError`" is right.
- **Export view modes:** `routes/exports.py:42-44` takes `view_mode`, defaulting to `simple`.
- **Fixture impact:** `clean_db` already deletes both backup tables. `tests/test_schema_registry.py` needs no edit.
- **Gate selection:** it matches the QUALITY_GATE DB / schema, Route and Business-logic rows.

## Not checked

- Whether the route literals at `routes/workout_plan.py:895-934` and `:1060-1094` match the plan's line references.
- `fetch-wrapper.js:61` and `toast.js:294` (the error-message and `textContent` claims).
- `tests/test_backup*` modules other than `test_program_backup.py` and the fuzz file.
- `tests/fixtures/make_old_schema_db.py`.
- The `docs/product/*` line references and the ADR numbering.
- The pyright baseline impact.
- Every `tests/` reference to `export_service` beyond the grep counts.
````

### product-risk-reviewer (agent `a850a542dbf97a312`)

````markdown
**Verdict: sound with changes.** There is no calculation drift, no local-first or non-goal violation, and the refuse-before-write design protects the plan and log. Two should-fix items concern the user-facing refusal copy, and one concerns scope. Nothing blocks.

## Findings

**1. Should-fix — D2, refusal message vs C6/C8.**
- C6 requires the message to identify each offending row by routine, exercise and the unrecognized value. C8 requires it to name the row, the field and the stored value.
- D2 caps the message at five rows plus "and N more" and puts the full list only in `rows`. The error is shown through `error.message`, and `backup-center.js:941` and `fetch-wrapper.js:58-62` pass only `code`, `message` and `requestId` to the toast. The `rows` array never reaches the user.
- So for a backup with six or more bad rows the signed criterion is not met. The user cannot see which rows to repair.
- The plan also never fixes the format of `<problem>`. C8 needs it to carry field and value, for example `emom, time_cap_seconds = 600 (not used by emom)`.
- Change: either list every offending row in the message, or send the truncation to the owner as a Gate-0 deviation instead of settling it silently. Specify the `<problem>` templates and assert them in tests.

**2. Should-fix — D2, copy and toast legibility.**
- The toast default is 3000 ms (`toast.js:253`). It prepends "Failed to restore backup: " (`backup-center.js:941`) and appends " (Request ID: …)" (`toast.js:279-281`). A multi-row message of about 300 characters will likely vanish before it can be read. Existing error toasts are short.
- The opening sentence is fine on terminology: "plan" and "workout log" match the canonical terms.
- The plan states a cost (A5, Q1) but the message does not tell the user what to do next. The backup is not restorable in-app and is left unchanged.
- Change: add a closing clause saying the backup was left unchanged and cannot be restored until the listed values are corrected. Edit `backup-center.js` only to pass a longer duration for this error. That needs a stated exception to "no production JS edit" (D2, Scope Out), or the message must be kept short with the detail carried elsewhere. Decide this explicitly.

**3. Note — D2, the 422 alternative is misdescribed.**
- The plan says no route pairs `VALIDATION_ERROR` with 422. But `utils/errors.py:128` already defines `"UNPROCESSABLE_ENTITY": 422`, and no route uses it.
- Position: keep `VALIDATION_ERROR` / 400. It is what C6 calls "recognizable". The request is well formed, but the repository's only validation convention is `VALIDATION_ERROR` / 400 (`.claude/rules/routes.md`), and the JS keys off neither. If the council prefers 422, the code should be `UNPROCESSABLE_ENTITY`, not `VALIDATION_ERROR`. Correct the plan text either way.

**4. Note — D2, a new error path with an extra kwarg.**
- `error_response` accepts `**kwargs` into the error object (`errors.py:67`, `:95-100`). So `reason="RESTORE_REFUSED"` and `rows` are valid. `routes.md` shows `reason` is an established channel.
- The existing HTTP 200 "no result" pattern is explicitly for replace-exercise only. A 400 is correct here, because the user did not get what they asked for and the state is unchanged.
- No finding. I note that C11 ("only new outcome is the refusal") is consistent.

**5. Should-fix — D3, scope of the `routes/workout_plan.py` refactor.**
- Section 0 puts "any change to how execution styles are validated on the plan page" out of scope. D3 edits the validator at `:895-934`, plus `:1072-1093`, in the same PR that changes backup behavior. A11 and C15 do not require that edit, because restore reads its own pinned literals.
- The refactor is value-identical on its face. It still touches a core Plan-workflow route and widens PR 1's blast radius. The tripwire's value comes from the two definitions being independent, which can be achieved by tests alone.
- Position on D3: use the fallback. Leave `routes/workout_plan.py` untouched. Pin the restore contract's literals in `utils/backup_execution_contract.py`. Make the tripwire behavioral, as the plan outlines: probe `POST /api/execution_style` at each boundary and compare `GET /api/execution_style_options`. That also removes the "characterization tests first" step.
- If the council keeps the move, the characterization tests must run before it, as the plan already says.

**6. Note — D1, ordering is correct and C7 holds.**
- Today the `BEGIN IMMEDIATE` is at `program_backup.py:481` and the two `DELETE`s at `:485-486`. Both come after the header, item and catalog reads (`:451-474`). Raising before `:481` leaves `user_selection` and `workout_log` untouched.
- `DatabaseHandler.__exit__` rolls back on any exception (`database.py:520-528`), so the plan's safeguard claim is right.
- The route's `except ValueError` at `:172` must stay below the new `except`. The plan says so. The refusal exception must not subclass `ValueError`.

**7. Should-fix — D5, the single assembled INSERT.**
- Replacing four hand-written variants (`:522-605`) with one dynamic statement is the riskiest edit on the path that deletes the user's log. The column list comes from a fixed tuple, so there is no injection risk. But a wrong tuple order or a missed `exercise_order` / `superset_group` fallback silently corrupts every restore, and C9/C1 tests may not catch a transposition of same-typed columns.
- Position: acceptable on the data-loss side if the plan adds a row-for-row integrity test over all columns, including `superset_group` and `exercise_order`. It names `_BACKUP_OWNED_COLUMNS`, but it should say explicitly that the test compares every user_selection column except `id`. Add a mutation arm that swaps two same-typed columns, for example `min_rep_range` and `max_rep_range`.

**8. Note — D5, a missing style on a present-but-NULL style column.**
- Writing the literal `'standard'` for a `NULL` style matches C5/A3. Checked: `db_initializer.py:210` makes the column `DEFAULT 'standard'` on `user_selection`, so an explicit `NULL` would indeed bypass it. Correct.

**9. Note — D4, migration and legacy-backup safety.**
- The `ALTER ... ADD COLUMN` pattern mirrors `program_backup.py:88-93`. It is additive and idempotent, which satisfies C4 and the backup contract. Existing backups remain restorable.
- Defaulting `execution_style` to `NULL` rather than `'standard'` is the right call for C5.
- Reverting the PR leaves the columns harmlessly in place, as the migration notes say.

**10. Note — Section 0 / Gate 0 provenance.**
- The plan states the owner "has not read the amended text back". Gate 0 was signed on a forwarded second-model review, adopted by the line "from astra what to do:". The plan records this honestly. I take no position beyond noting that finding 1's deviation, if kept, should go back to the owner.

## Position on the open points
- **D2, 400 or 422:** 400 with `VALIDATION_ERROR` (see finding 3).
- **D3:** the fallback is enough (finding 5).
- **D5:** acceptable with the stronger integrity test and swap mutation (finding 7).
- **C7, mocked Playwright test:** one test is proportionate. It lands on the exact toast path the user will see. If finding 2's duration change is adopted, add a second assertion that the message is still on screen after 3 s.

## Checked and found correct
- `restore_backup()` reads before it writes, and rolls back only on `sqlite3.Error` (`program_backup.py:449-474`, `:481-486`, `:608-610`).
- `DELETE FROM workout_log` at `:485` confirms restore wipes the log.
- The route maps `ValueError` to `NOT_FOUND` and everything else to 500 (`routes/program_backup.py:172-177`).
- The validator literals, defaults and limits at `routes/workout_plan.py:895-934`, and the options endpoint limits at `:1089-1093`, match the plan.
- The endpoint writes only the three shapes the plan claims (`:971-987`).
- The four execution fields are referenced in production Python only in `utils/db_initializer.py` and `utils/export_service.py` under `utils/`, so calculation surface is "none".
- `create_backup()` (`:191-246`) does not read the four fields.
- The Backup Center catch shows `error.message` through `textContent`, so echoed values cannot inject markup (`toast.js:294`).
- There is no effective-sets gating, no telemetry or cloud path, and no auth.
- Terminology: the plan introduces no new user-facing synonyms. The proposed Excel headers are the owner-approved ones.

## Not checked
- The export-side line numbers in `utils/export_service.py` and `utils/export_utils.py`, beyond the grep hits at `:106`, `:130`, `:154`, `:261`, `:276` and `:288`, and the 21-column count.
- `docs/DECISIONS.md` ADR-008 and ADR-014, `docs/product/*` line references, and the test files.
- Whether any real user database holds stale timing values (A7). I did not open `data/database.db`.
- The `exercise_order` / `superset_group` fallback behavior of the dynamic INSERT. It is not yet written, so only its design can be judged.
````

---

## Response matrix

*Council Steps 3–4, 13 November 2026. Dispositions are the manager's synthesis, proposed for the owner to confirm at Gate 1. Finding numbers are each reviewer's own. No finding is deferred. "v2" names the Plan v2 section that carries the change.*

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| AR1 — leave `routes/workout_plan.py` untouched in PR 1; take the fallback | architecture-reviewer | accept | v2 D3: the constants move, the three defaults and the characterization step are dropped; the tripwire is behavioral. Put to the owner as decision (i) because test-strategist disagrees |
| AR2 — the tripwire must cover the style set and say which direction each assertion catches | architecture-reviewer | accept | v2 D3 tripwire table: each style, one rejected style, every limit and one step beyond, with the direction each row catches |
| AR3 — pin the exception's home, base class and payload | architecture-reviewer | accept | v2 D1: `BackupRestoreRefused` is defined in `utils/program_backup.py`, derives from `Exception` directly, carries the rendered rows and the backup name; the route builds the message |
| AR4 — keep 400 `VALIDATION_ERROR`; extras are nested under `error` | architecture-reviewer | accept | v2 D2: tests read `body["error"]["reason"]` and `body["error"]["rows"]` |
| AR5 — one assembled `INSERT` is acceptable if placeholders and parameters come from one list | architecture-reviewer | accept | v2 D5 states that condition |
| AR6 — migration shape is right; add the columns in a loop | architecture-reviewer | accept | v2 D4: a loop over `(name, type)` |
| AR7 — pre-flight reads outside the write lock; no new impact | architecture-reviewer | accept — no action | None. v2 D1 keeps the pre-flight in the existing read region |
| AR8 — export confirmed, low risk | architecture-reviewer | accept — no action | None |
| AR9 — the Playwright weight is outside the reviewer's charter | architecture-reviewer | accept — no action | None |
| TS1 — the "move the refusal after the `DELETE`s → C7 red" arm cannot go red | test-strategist | accept | v2 mutation arms: replaced by "pre-flight raises nothing" (C6, C7, C8 red); a call-spy test pins "refused means no `BEGIN`, no `DELETE`, no `INSERT`", and the moved-raise arm is kept against that spy test, where it can go red |
| TS2 — the tripwire must observe the live plan page | test-strategist | accept | Same change as AR1 and AR2. The literal pin is kept. Both failure messages say to record a backup-compatibility decision under ADR-015 (number as in v2 D7) |
| TS3 — characterize the options endpoint | test-strategist | accept in modified form | The options-endpoint comparison lives inside the tripwire (v2 D3). **The separate Step 1 characterization is rejected**: the refactor it protected is removed by AR1 |
| TS position on D3 — keep the constants move | test-strategist | **rejected** | Two reviewers (AR1, PR5) take the fallback, and Section 0 places plan-page validation changes out of scope. This is a reviewer disagreement: recorded as owner decision (i), with the fallback as the proposed action |
| TS4 — the rollback test depends on the `INSERT` text and one call per row | test-strategist | accept | v2 D5: the statement begins `INSERT INTO user_selection` and runs once per row through `execute_query(..., commit=False)` |
| TS5 — destination-column assembly is only partly covered | test-strategist | accept | v2 tests: the drop-column restore test is parametrized (`exercise_order` absent; `superset_group` absent; both absent), and the owned-column handling covers the four execution columns |
| TS6 — pin the 21 existing headers as literals | test-strategist | accept | v2 PR 2 tests: literal 21-header lists per view mode, confirmed green on unmodified `main`; mutation arm "insert a column before `exercise_order` → C13 red"; one assertion on the sheet-name list |
| TS7 — the mocked Playwright test proves less than claimed; name the known red | test-strategist | accept | v2: one mocked test asserts the toast text, `#backup-restore-result` not shown, confirm button re-enabled. The program-count half of C7 is mapped to the pytest test only. PR 1's gates name the `program-backup.spec.ts:79` rerun rule |
| TS8 — C1 needs rows written through the endpoint | test-strategist | accept | v2 tests: C1 and C2 rows go through `POST /api/execution_style` with the shared `client`; direct SQL only for limit-value and invalid rows |
| TS9 — how to build the legacy table | test-strategist | accept | v2 tests: old `CREATE TABLE` text or `DROP COLUMN`. Checked: `tests/fixtures/make_old_schema_db.py` builds no backup tables — its docstring (`:3-10`) lists them among the tables that do not exist yet in that database — so it does not provide a legacy `program_backup_items` |
| TS10 — C10's "shown" has no UI test; the literal test is enough | test-strategist | accept — no action | None. The manual smoke covers the tile |
| TS11 — build C8 rows through `_seed_tampered_backup` so `typeof()` pins the stored type | test-strategist | accept, placement adjusted | v2 tests: the tampered-row tests (C5–C8, A8) live beside the helper in `tests/test_program_backup_restore_fuzz.py`, with the helper extended to the four columns, instead of importing a helper across test modules |
| PR1 — truncating at five rows breaks C6 and C8; fix the `<problem>` templates | product-risk-reviewer | accept | v2 D2: no row truncation — the message names every offending row, as Gate 0's wording requires. Per-row templates carry field and stored value and are asserted in tests |
| PR2 — the message does not say what happens next; the toast vanishes in 3 s | product-risk-reviewer | accept, flagged for the owner | v2 D2 adds the closing clause. A one-line `backup-center.js` change gives this error's toast a longer duration: owner decision (ii), a stated exception to "no production JS edit". Verified in the code: the 3000 ms default (`toast.js:253`) and the "Failed to restore backup: " prefix (`backup-center.js:941`). **One part of the finding does not hold here**: the " (Request ID: …)" suffix is added only when the caller passes `requestId` (`toast.js:279-281`), and the call at `:941` passes no options |
| PR3 — the 422 alternative is misdescribed | product-risk-reviewer | accept | v2 D2 text corrected: `utils/errors.py:128` defines `UNPROCESSABLE_ENTITY` → 422; only the generic 422 handler (`:166-175`) uses it and no route returns it. The decision stays 400 `VALIDATION_ERROR` |
| PR4 — the new error path and its extra keywords are valid | product-risk-reviewer | accept — no action | None |
| PR5 — the `routes/workout_plan.py` refactor is out of proportion | product-risk-reviewer | accept | Same change as AR1 |
| PR6 — D1 ordering is correct and C7 holds | product-risk-reviewer | accept — no action | None |
| PR7 — the assembled `INSERT` needs a full-column integrity test and a swap mutation | product-risk-reviewer | accept | v2 tests: the integrity test compares every `user_selection` column except `id`; mutation arm swaps `min_rep_range` and `max_rep_range` |
| PR8 — writing the literal `'standard'` for a missing style is correct | product-risk-reviewer | accept — no action | None |
| PR9 — the migration is additive, idempotent and safe for legacy backups | product-risk-reviewer | accept — no action | None |
| PR10 — Gate 0 provenance is recorded honestly; a kept deviation should go back to the owner | product-risk-reviewer | accept — no action | The deviation it refers to (PR1's row truncation) is removed. One smaller point of the same kind is put to the owner as decision (iii) |

---

## Plan v2

*Council Step 4, written 13 November 2026. **Plan v2 governs.** It is complete on its own; Plan v1 is kept above exactly as the reviewers saw it. Line numbers were re-read in the working tree on 13 November 2026 while the checkout was on another branch — re-verify against `origin/main` before editing. C, A and Q numbers refer to Section 0.*

*What changed from v1:* `routes/workout_plan.py` and `utils/constants.py` are no longer touched and the tripwire is behavioral (D3); the refusal exception is named and placed (D1); the message names every offending row, has fixed per-row templates and a closing clause (D2); one production JavaScript line is proposed, as an owner decision (D2); the assembled `INSERT` and the migration loop are pinned (D4, D5); the test list gains a call-spy test, a full-column integrity test, drop-column parametrization and literal export headers; the mutation arms are corrected.

**Goal**: A program backup restores every plan row with the execution style and timing values it had when the backup was taken, refuses — changing nothing — when it holds an execution value it cannot interpret, and the Excel export shows the three timing values beside everything it already exports. *(Unchanged from v1.)*

**Scope**
- **In**:
  - **PR 1 — backup and restore** (C1–C11, C15, and its share of C14): four columns on `program_backup_items`, capture in `create_backup()`, a pre-flight check and write in `restore_backup()`, the refusal error on `POST /api/backups/<id>/restore`, `BACKUP_SCHEMA_VERSION` 1 → 2, a pinned restore-acceptance contract with a behavioral tripwire, tests, documentation, one ADR.
  - **PR 2 — Excel export** (C12–C13, and its share of C14): three columns appended to the Workout Plan sheet, tests, documentation.
  - Each PR branches from fetched `origin/main` and is mergeable without the other.
- **Out**: everything in Section 0's *Out of scope* list. In particular: no "restore the rest" interface; no change to the backup detail response or pane; **no edit to `routes/workout_plan.py` or to plan-page validation**; no change to `get_backup_details()`; no template or SCSS edit. No production JavaScript edit, with one proposed exception — a single line in `static/js/modules/backup-center.js`, owner decision (ii).

**Owner decisions at Gate 1**

| # | Decision | Proposed | Alternative, and what it changes |
|---|---|---|---|
| (i) | Where the plan-page definition lives. The reviewers disagree: architecture-reviewer and product-risk-reviewer take the fallback; test-strategist would keep the constants move | **Fallback**: leave `routes/workout_plan.py` untouched; restore has its own pinned contract; a behavioral tripwire watches the live plan page (D3) | Keep the move of the plan-page literals to `utils/constants.py`. PR 1 then also edits `routes/workout_plan.py` and `utils/constants.py`, and a characterization of `POST /api/execution_style` and `GET /api/execution_style_options` must pass on unmodified code first. The behavioral tripwire stays either way |
| (ii) | One production JavaScript change: the Backup Center keeps the refusal toast on screen longer. This is an explicit exception to "no production JS edit" and touches A14 | **Yes**: one line in the restore catch (`backup-center.js:940-941`) passes `{ duration: 30000 }` when the error is the restore refusal. The toast has a close button (`templates/base.html:261-262`) | Leave the 3-second default (`toast.js:253`). No JavaScript changes, and a refusal message naming several rows disappears before it can be read. The message is still in the server log and the response |
| (iii) | Long stored values in the message. C6 says the message identifies each row by "the unrecognized value"; a stored value can be arbitrarily long text or a blob | **Shorten**: a value longer than 40 characters is shown as its first 40 characters and `…`; a blob is shown as `<binary, N bytes>`. Every offending row is still named | Show every value in full. A pathological value then produces an arbitrarily long message, toast and log line |

**Gate 1 sign-off — 14 November 2026.** The owner approved Plan v2 and instructed the session agent to sign on the owner's behalf and proceed. The approval followed a written decision brief that recommended the proposed option for each decision; the owner adopted it:

- (i) **Fallback** — `routes/workout_plan.py` and `utils/constants.py` stay untouched; restore keeps its own pinned contract; the behavioral tripwire watches the live plan page.
- (ii) **Yes** — the restore-refusal toast stays on screen for 30 seconds (`{ duration: 30000 }`, one line in `backup-center.js`'s restore catch), as the stated exception to "no production JS edit".
- (iii) **Shorten** — a stored value longer than 40 characters is shown as its first 40 characters and `…`; a blob as `<binary, N bytes>`; every offending row is still named.

The response-matrix dispositions are confirmed as proposed. This approves implementation of PR 1 and PR 2 only; it is not a merge approval.

**Decisions this plan settles**

*D1 — Restore decides to refuse before it writes anything.* `restore_backup()` already reads the header, the items and the catalog names before `BEGIN IMMEDIATE` (`utils/program_backup.py:450-478`; `BEGIN` at `:481`, the two `DELETE`s at `:485-486`). A pre-flight pass is added in that same region:

1. Classify every item in today's order: not in the catalog → `skipped` (today's check at `:496`); fails `_validate_restore_item()` → `invalid` (today's check at `:507`); otherwise *restorable*.
2. Check the four execution fields of each restorable item only (A8) and collect every problem, not just the first.
3. If any problem was found, raise `BackupRestoreRefused` before `BEGIN IMMEDIATE`. No write statement has been issued, so `user_selection` and `workout_log` keep their rows and ids (C7).
4. Otherwise run the transaction as today — the two `DELETE`s, then one `INSERT` per restorable item — and return the same five-key result built from the pre-flight lists.

`BackupRestoreRefused` is defined in `utils/program_backup.py`. It derives from `Exception` directly — **never from `ValueError`**, which the route maps to `NOT_FOUND` 404 (`routes/program_backup.py:172-174`). It carries the backup name and the list of rows, each already rendered to JSON-safe text. The route builds the message from those. `DatabaseHandler.__exit__` rolls back on any exception (`utils/database.py:520-528`); that existing safeguard is kept, and it is also why a snapshot test alone cannot prove "decides before it writes" — the call-spy test does (see *Mutation arms*). C9 holds because classification order and the `skipped` / `invalid` channels do not change.

*D2 — The refusal is `VALIDATION_ERROR`, HTTP 400, with a machine-readable reason.* The route answers with `error_response("VALIDATION_ERROR", message, 400, reason="RESTORE_REFUSED", rows=[...])`, in an `except BackupRestoreRefused` placed ahead of the `ValueError` branch.

- `VALIDATION_ERROR` / 400 is the repository's convention for invalid values (`utils/errors.py:121-123`; `.claude/rules/routes.md` *Input validation*); that is what makes it recognizable. `utils/errors.py:128` also defines `UNPROCESSABLE_ENTITY` → 422, used only by the generic 422 handler (`:166-175`); no route returns it, and all three reviewers prefer 400.
- `reason` and `rows` are **nested under `error`** (`utils/errors.py:95-100`). Tests read `body["error"]["reason"]` and `body["error"]["rows"]`. The browser client keeps only `code`, `message` and `requestId` (`fetch-wrapper.js:58-63`), so the user sees the message and nothing else — which is why the message must be complete.
- Each entry of `rows` is `{routine, exercise, field, value, problem}`. `field` is the column name. `value` is rendered to text in `utils/` as decision (iii) settles.
- **The message names every offending row; nothing is truncated by row count.** Its shape is fixed and the tests assert on it:

  `Backup '<name>' was not restored. Your current plan and workout log were preserved; nothing was changed. <n> row(s) hold execution settings that cannot be restored: <row>; <row>; … The backup itself was left unchanged and cannot be restored until these values are corrected.`

  Each `<row>` is `<routine> / <exercise>: <problem>`, and `<problem>` is one of:

  | Case | `<problem>` |
  |---|---|
  | Unrecognized style (C6) | `execution style "<value>" is not recognized` |
  | Rule (i), not a whole number | `<label> "<value>" is not a whole number` |
  | Rule (i), outside the range | `<label> <value> is outside <min>–<max>` |
  | Rule (ii), style does not use the field | `<label> <value> is not used by the <style> style` |

  `<label>` is `time cap`, `EMOM interval` or `EMOM rounds`. For a missing style, `<style>` is `standard`. The closing clause promises no in-application repair; none exists (A5).
- The Backup Center's catch shows `Failed to restore backup: <message>` (`backup-center.js:940-941`) and the toast writes with `textContent` (`toast.js:294`), so an echoed value cannot inject markup. No Request ID suffix is added on this path, because the call passes no options (`toast.js:279-281`).
- **Decision (ii), if adopted:** in that catch, when `pendingAction` is `restore` and `error.code` is `VALIDATION_ERROR`, the call passes `{ duration: 30000 }`. The restore endpoint has no other `VALIDATION_ERROR` outcome, and the thrown error carries `code` (`fetch-wrapper.js:58-63`, `:216`). `duration` is the only mechanism `showToast()` offers (`toast.js:253`, `:332`); there is no "until dismissed" option, and `toast.js` is not edited.

*D3 — A pinned restore contract, and a behavioral tripwire against the live plan page (A10, A11, C15).*

- The plan-page definition **stays where it is**: literals in `routes/workout_plan.py` (`:895`, `:905-906`, `:915-916`, `:918`, `:924`, and again at `:1089-1093`). PR 1 does not edit that file.
- The **restore-acceptance contract** lives in a new `utils/backup_execution_contract.py`: the three styles, the three ranges, which timing fields each style uses, and the pure check function. It holds its own literals, imports nothing from `routes/`, and carries no defaults — restore never applies one.
- **C15 mechanism.** Restore reads only its own contract, so narrowing a plan-page limit does not change what restore accepts: previously valid backups stay restorable by default. The tripwire below fails when the plan page and the contract stop agreeing, in either direction, and a literal pin fails when the contract itself is edited. Both failure messages say: record a backup-compatibility decision under ADR-015 before changing either side. Widening matters as much as narrowing: if the plan page starts accepting more, the contract must be widened or new valid plans would produce backups that restore refuses.
- **Tripwire assertions.** A probe's verdict is "stored as sent": the request succeeds **and** the row afterwards holds exactly the probed value. The verdict must be read from the stored row, because the endpoint replaces an omitted or zero timing value with a default (`routes/workout_plan.py:905`, `:915-916`) — a request for 0 rounds succeeds and stores 5.

  | Assertion | Reads the plan page through | Catches |
  |---|---|---|
  | Each of `standard`, `amrap`, `emom` is stored as sent | `POST /api/execution_style`, then the row | The plan page dropping or renaming a style the contract accepts (narrowing) |
  | One unlisted style (`tabata`) is rejected by the endpoint and refused by the contract | `POST /api/execution_style` | A probe that accepts everything; keeps the other rows honest |
  | The style keys of the options payload equal the contract's styles | `GET /api/execution_style_options` | A style added to or removed from the plan page's advertised list (both directions) |
  | Each limit value — 10 and 600; 15 and 180; 1 and 20 — is stored as sent | `POST /api/execution_style`, then the row | A narrowed limit |
  | One step beyond each limit — 9 and 601; 14 and 181; 0 and 21 — is **not** stored as sent | `POST /api/execution_style`, then the row | A widened limit |
  | The options payload's `limits` equal the contract's ranges | `GET /api/execution_style_options` | Either direction, for the advertised numbers |
  | The contract's literals equal the values written in the test | import | An edit to the contract itself |

- **Known residual, accepted with decision (i).** The validator and the options endpoint are two copies inside the route today. A style added to the validator but not to the options payload is not seen by any row above. The constants move would close that; the reviewers' majority judged the edit to a core plan-page route the larger risk.

*D4 — Migration and version bump, in ADR-008's three parts.*

1. **Bump**: `BACKUP_SCHEMA_VERSION = 2` (`utils/program_backup.py:39`); the comment block above it (`:26-38`) is rewritten to say version 2 is the first bump that tracks a payload change.
2. **Migration**: `initialize_backup_tables()` adds `execution_style TEXT`, `time_cap_seconds INTEGER`, `emom_interval_seconds INTEGER` and `emom_rounds INTEGER`, all `DEFAULT NULL`, to the `CREATE TABLE` (`:71-86`) and, for existing databases, by `ALTER TABLE ... ADD COLUMN` for each missing column — written as **one loop over `(name, type)` pairs**, in the shape of the `superset_group` block (`:88-93`). It is idempotent and needs no registry change (`utils/schema_registry.py:134` already calls it).
   - `execution_style` defaults to `NULL`, **not** `'standard'`: legacy rows read as missing (C5) and no invented value is stamped on an existing backup.
   - No existing row or header is rewritten; legacy headers keep `schema_version` 1 (C4). The header column's own `DEFAULT 1` (`:62`) is left alone.
3. **Restore branch**: D1 and D5.

`test_restore_ignores_foreign_schema_version` (`tests/test_program_backup.py:490-520`) is parametrized over `[0, 2]`; the list becomes `[0, 1, 3]` and its docstring is updated. Its assertion is C10's second half and does not change. ADR-008 stands: restore stays version-blind.

*D5 — What is captured and what is written.*

- **Capture.** `create_backup()` reads `user_selection`'s column names once and selects each of the four fields that exists, as it does for `exercise_order` and `superset_group` (`:191-202`); the `INSERT` (`:229-246`) gains the four columns. A field whose source column is absent is stored as `NULL`. Values are copied as stored — no validation, no normalization at backup time.
- **Restore read.** The item `SELECT` (`:463-468`) gains the four columns.
- **Restore write.** A missing style is written as the literal `'standard'`. A recognized style is written as stored. A timing value is written as stored, or `NULL` when missing — never 60 or 5.
- **Insert shape.** The four hand-written variants (`:522-605`) are replaced by one assembled statement, under four conditions:
  1. the column list comes from a fixed tuple of column names, filtered by which columns the destination has — never from input;
  2. the placeholders and the parameter tuple are built **from that same filtered list**, so their order cannot drift;
  3. the statement text begins `INSERT INTO user_selection`;
  4. it runs **once per row** through `execute_query(..., commit=False)` — no `executemany`. The existing rollback test (`tests/test_program_backup.py:263-273`) matches that text and counts those calls.

  A column absent from the destination is left out, as today. `db_initializer.py:209-220` adds the four execution columns to `user_selection` at every startup, so that omission is not reachable for them in a running application.
- **The check** (in `utils/backup_execution_contract.py`), per restorable item:

  | Stored style | Stored timing | Outcome |
  |---|---|---|
  | missing (`NULL`) | all missing | restore as `standard`, timing empty |
  | `standard`, `amrap` or `emom` | a field the style uses: missing | restore as stored (rule iii) |
  | `standard`, `amrap` or `emom` | a field the style uses: a Python `int` inside the contract's range | restore as stored |
  | `standard`, `amrap` or `emom` | a field the style uses: present and not an `int`, or outside the range | refuse (rule i) |
  | any, including missing | a field the style does not use: present | refuse (rule ii) |
  | present and not exactly one of the three (`tabata`, `EMOM`, ` emom`, `""`) | — | refuse (C6) |

  "Present" means not `NULL`. SQLite's `INTEGER` affinity stores a lossless real such as `60.0`, and numeric-looking text such as `'60'`, as the integer 60; those are then ordinary valid values. A present non-`int` is non-numeric text, a fractional real or a blob.

*D6 — Export.* In `utils/export_service.py`: the three keys are appended to `WORKOUT_PLAN_COLUMNS['order']` after `exercise_order` (`:111`); both label maps (`:114-136`, `:138-160`) gain `Time Cap (sec)`, `EMOM Interval (sec)`, `EMOM Rounds`; all three query variants in `build_export_query()` (`:257-263`, `:272-277`, `:284-289`) select the three columns. Headers are written from the first column in key order (`utils/export_utils.py:255-259`), so the sheet becomes A–X with A–U unchanged; a `NULL` already becomes an empty cell (`utils/export_utils.py:279-282`). `utils/export_utils.py` is not edited. Trap: `reorder_and_rename_columns()` appends any selected column missing from `order` at the end under its raw key (`:234-238`), so a forgotten label still "works" with the header `time_cap_seconds`; the literal-header test catches it. *(Unchanged from v1.)*

*D7 — One new ADR.* PR 1 adds **ADR-015** to `docs/DECISIONS.md`: restore validates execution fields against a pinned acceptance contract; a present value it cannot interpret refuses the whole restore; changing the plan page's accepted values or the contract requires a recorded backup-compatibility decision. ADR-008 gains a dated note that version 2 is the first bump under its rule. ⚠️ ADR-015 is the next free number as read on 13 November 2026 (ADR-014 is the last heading); a concurrent PR can take it. Renumber before merge if so, including the two tripwire failure messages.

**Artifacts**

*PR 1 — backup and restore*

| Path | Change | Notes |
|---|---|---|
| `utils/backup_execution_contract.py` | new | The restore-acceptance contract as its own literals, and the pure check (D3, D5). No database access |
| `utils/program_backup.py` | modify | Bump and comment (`:26-39`); migration loop (`:71-93`); capture (`:191-246`); `BackupRestoreRefused`; pre-flight, read and assembled write in `restore_backup()` (`:429-632`) |
| `routes/program_backup.py` | modify | `except BackupRestoreRefused` ahead of the `ValueError` branch (`:172`); builds the D2 message; docstring |
| `static/js/modules/backup-center.js` | modify — **only if the owner adopts decision (ii)** | One line in the catch at `:940-941` |
| `tests/test_backup_execution_contract.py` | new | Unit tests for the check; the literal pin; the behavioral tripwire (C15) |
| `tests/test_program_backup_execution_fields.py` | new | C1–C4, C10, C11: round trip through the endpoints, legacy and upgrade cases, version label, exact response key sets |
| `tests/test_program_backup_restore_fuzz.py` | modify | `_seed_tampered_backup` (`:73`) extended to the four columns; C5–C8 and A8 tampered-row tests; the call-spy test; the untouched-plan-and-log snapshots |
| `tests/test_program_backup.py` | modify | Integrity tests compare every `user_selection` column except `id`; `_seed_known_program` (`:956`) gains `amrap` and `emom` rows; `_BACKUP_OWNED_COLUMNS` / `_BASE_OWNED_COLUMNS` (`:929-934`) cover the four fields; drop-column test parametrized; foreign-version list → `[0, 1, 3]` (`:490`) |
| `e2e/program-backup.spec.ts` | modify | One mocked-refusal test (C7's Backup Center half) |
| `docs/product/BACKEND_SCHEMA.md` | modify | `program_backup_items` table and the paragraph at `:645-649`; `schema_version` note (`:619-623`) |
| `docs/product/APP_FLOW.md` | modify | Schema stat (`:636`), Restore row (`:638`), *What restore actually does* (`:644-664`) |
| `docs/DECISIONS.md` | modify | ADR-015; dated note on ADR-008 (D7) |
| `docs/test_inventory/**` | regenerate | Required: tests are added to `tests/` and `e2e/` |

Not touched in PR 1, by decision: `routes/workout_plan.py`, `utils/constants.py`, `tests/test_phase3_features.py`, `static/js/modules/toast.js`, `static/js/modules/fetch-wrapper.js`.

*PR 2 — Excel export*

| Path | Change | Notes |
|---|---|---|
| `utils/export_service.py` | modify | D6 |
| `tests/test_exports.py` | modify | Literal header lists for both view modes; values per style; empty cells; sheet-name list |
| `docs/product/APP_FLOW.md` | modify | Excel export row (`:224`) names the three appended columns |
| `docs/test_inventory/**` | regenerate | Required: tests are added |

**Effort**: PR 1 **L**, PR 2 **S** · **Owner**: implementation agent assigned by the manager after Gate 1; the owner merges · **Depends on**: Gate 1 sign-off on this plan, including decisions (i)–(iii). The PRs do not depend on each other; both regenerate `docs/test_inventory/` and both edit `APP_FLOW.md` (different sections), so whichever merges second rebases onto `main`, regenerates the inventory and re-runs its gates on the rebased tree.

**Sequence**

*PR 1*
1. Branch from fetched `origin/main`.
2. Add `utils/backup_execution_contract.py`, its unit tests, the literal pin and the behavioral tripwire. The tripwire must pass against the unmodified plan-page code.
3. Migration loop, capture and bump in `utils/program_backup.py`; legacy and upgrade tests (C3, C4); foreign-version list (C10).
4. Restore: read, pre-flight, `BackupRestoreRefused`, assembled `INSERT`; route mapping and message; the remaining pytest tests, including the call-spy test, the full-column integrity test and the drop-column parametrization.
5. If decision (ii) is adopted, the one-line `backup-center.js` change. Then the mocked-refusal Playwright test.
6. Documentation, ADR-015, the ADR-008 note, the module comment.
7. Regenerate `docs/test_inventory/`; run the pyright baseline diff.
8. Run the gates below, including the manual smoke and the mutation arms; open the PR with migration notes; mark it ready and stop. No merge without the owner's confirmation naming the PR.

*PR 2*
1. Branch from fetched `origin/main`. Add the export tests. The A–U literal-header assertion and the sheet-name assertion pass on unmodified code; the V–X assertions fail.
2. Change `utils/export_service.py` (D6); all pass.
3. Update `APP_FLOW.md`; regenerate `docs/test_inventory/`; run the pyright baseline diff.
4. Run the gates below; open the PR with migration notes; mark it ready and stop.

**Test coverage by criterion**

| Criterion | Test (PR) |
|---|---|
| C1 | API round trip with the shared `client`: styles set through `POST /api/execution_style` (the three shapes of reproduction A), backup, empty the plan, restore, compare the four fields. Limit-value rows are seeded by direct SQL. Plus the row-for-row integrity tests, which compare **every `user_selection` column except `id`** — `superset_group` and `exercise_order` included — over a program that now holds `amrap` and `emom` rows (PR 1) |
| C2 | Covered by C1's API test: "Save current plan first" calls the same `POST /api/backups` (`backup-center.js:1112`). No separate browser test |
| C3, C4 | Build a pre-change `program_backup_items` from the old `CREATE TABLE` text or by `DROP COLUMN` (pattern at `tests/test_program_backup.py:1079`), seed a version-1 header and rows by direct SQL, run `initialize_backup_tables()` twice; header and old columns unchanged, new columns `NULL`; list, open, rename, restore and delete all work; restored rows read `standard` with empty timing (PR 1) |
| C5 | Through `_seed_tampered_backup`: `NULL` style with `NULL` timing → `standard`; `amrap` with `NULL` time cap → `amrap`, still `NULL`; `emom` with one of its two values `NULL` → as stored (PR 1) |
| C6 | Through `_seed_tampered_backup`, parametrized over `tabata`, `EMOM`, ` emom`, `""`: status 400; `body["error"]["code"] == "VALIDATION_ERROR"`; `body["error"]["reason"] == "RESTORE_REFUSED"`; the fixed opening and closing sentences; the exact `<row>` text for each offending row in the message; the matching entry in `body["error"]["rows"]`; no row converted. One case with more than five offending rows asserts every one appears in the message (PR 1) |
| C7 | Pytest: for each refusal class, `SELECT *` of `user_selection` and `workout_log` ordered by id, and of both backup tables, equal before and after — ids included; the active-program count is unchanged. The **call-spy test** asserts a refused restore issues no `BEGIN IMMEDIATE`, no `DELETE` and no `INSERT` (monkeypatch pattern at `tests/test_program_backup.py:263-273`). Playwright, mocked 400: the error toast contains the server message, `#backup-restore-result` is not shown, the confirm button is re-enabled; and, if decision (ii) is adopted, the message is still visible after 3 s. The mocked test proves nothing about the program count — the pytest test does (PR 1) |
| C8 | Through `_seed_tampered_backup`, so `typeof()` pins the stored type. Rule (i): `'abc'`, `""`, `12.5`, `0`, `-5`, 9 and 601 (time cap), 14 and 181 (interval), 0 and 21 (rounds). Rule (ii): `standard` + time cap; `amrap` + interval; `amrap` + rounds; reproduction B's row (`emom`, 600, 60, 10); missing style + time cap. Each asserts the exact `<problem>` text, with field label and stored value (PR 1) |
| C9, A8 | Existing fuzz tests unchanged and green. New cases: a catalog-missing or bounds-invalid row that also carries a bad style still restores successfully, with that row in `skipped` / `invalid`. The drop-column restore test (`tests/test_program_backup.py:1068`) is parametrized over `exercise_order` absent, `superset_group` absent, and both absent (PR 1) |
| C10 | A new backup persists and returns `schema_version` 2 (literal); the foreign-version test over `[0, 1, 3]`. The Schema tile is a pass-through (`backup-center.js:605`), covered by the manual smoke (PR 1) |
| C11 | Exact key sets for the success responses of all six endpoints, including the ten item keys of the detail payload (PR 1) |
| C12, C13 | Header row equal to a **literal** 24-entry list for `simple` and for `advanced`. The first 21 of each are today's headers, written out in the test — not derived from `WORKOUT_PLAN_COLUMNS` — and confirmed green on unmodified `main` before the change. V–X values for one row of each style; empty cells for missing values. One assertion that the workbook's sheet-name list for the test's fixture equals the list captured on unmodified `main` (PR 2) |
| C14 | PR description carries migration notes; the documentation rows above are in the same PR (both) |
| C15 | The behavioral tripwire and the literal pin (D3), each failing with the decision-required message (PR 1) |

The 21 existing headers, as read from `utils/export_service.py:114-160` on 13 November 2026 — the implementer confirms them by running the test on unmodified `main`:

- `simple`: Routine, Exercise, Primary Muscle, Secondary Muscle, Tertiary Muscle, Isolated Muscles, Utility, Movement Pattern, Movement Subpattern, Sets, Min Rep, Max Rep, RIR, RPE, Weight, Style, Grips, Stabilizers, Synergists, Superset Group, Exercise Order.
- `advanced`: Routine, Exercise, Primary Muscle Group, Secondary Muscle Group, Tertiary Muscle Group, Advanced Isolated Muscles, Utility, Movement Pattern, Movement Subpattern, Sets, Min Rep Range, Max Rep Range, RIR, RPE, Weight, Execution Style, Grips, Stabilizers, Synergists, Superset Group, Exercise Order.

*Mutation arms, recorded in the PR description* — each applied, shown red, and reverted.

| PR | Mutation | Must go red |
|---|---|---|
| 1 | Drop the four columns from the assembled restore `INSERT` | C1 |
| 1 | Pre-flight raises nothing, so the restore proceeds | C6, C7, C8 |
| 1 | Raise the refusal after the two `DELETE`s instead of before `BEGIN` | The call-spy test. The snapshot test stays green here, because the rollback restores the rows — expected, and the reason the spy test exists |
| 1 | Write `NULL` instead of `'standard'` for a missing style | C3 |
| 1 | Swap the values written to `min_rep_range` and `max_rep_range` | The full-column integrity test |
| 2 | Drop the three columns from the export query | C12 |
| 2 | Insert a column before `exercise_order` in `WORKOUT_PLAN_COLUMNS['order']` | C13 |

**Migration notes each PR description must carry**

- **PR 1**: four nullable columns added to `program_backup_items` by an idempotent startup `ALTER`; no existing row rewritten. `BACKUP_SCHEMA_VERSION` 1 → 2: new backups report `schema_version` 2, earlier ones keep 1, restore ignores the label. Behavior change: a restored row now carries its execution style and timing values, where before it was reset to `standard`. New outcome: `POST /api/backups/<id>/restore` can answer 400 `VALIDATION_ERROR` with `error.reason` `RESTORE_REFUSED` and `error.rows`, having changed nothing. Success response shapes unchanged. If decision (ii) is adopted: the refusal toast stays for 30 seconds. Reverting the PR leaves the columns in place harmlessly; a build without it restores a version-2 backup without the four fields, as ADR-008 already accepts.
- **PR 2**: the Workout Plan sheet of `GET /export_to_excel` gains columns V–X (`Time Cap (sec)`, `EMOM Interval (sec)`, `EMOM Rounds`) in both view modes; columns A–U and every other sheet are unchanged.

**Expected gates** (per [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md); confirmed by `test-strategist`'s review, adjusted for the files v2 no longer touches)

*PR 1* — change types: DB / schema (`utils/program_backup.py`), Route / API (`routes/program_backup.py`), Business logic (`utils/backup_execution_contract.py`), E2E spec, and Frontend (JS) if decision (ii) is adopted.
- pytest: **full suite** (DB / schema row). It includes `tests/test_backup_execution_contract.py`, `tests/test_program_backup_execution_fields.py`, `tests/test_program_backup.py`, `tests/test_program_backup_restore_fuzz.py`, and `tests/test_phase3_features.py` unchanged. No fixture change: `clean_db` already clears both backup tables.
- e2e: `e2e/program-backup.spec.ts` (changed), then the full Chromium suite through `/verify-suite`. No visual surface changes; a visual red is judged against the existing ledger and never resolved with `--update-snapshots`. **Known red:** if `e2e/program-backup.spec.ts:79` fails, rerun it in isolation and record whether it passes, per QUALITY_GATE *Known exceptions*. The mocked 400 logs console errors by design (`fetch-wrapper.js:204`); the new test handles them in whatever way the spec's fixture requires.
- manual backup/restore smoke (DB / schema row; it also serves the Frontend (JS) row), on a scratch database with `DB_FILE` set explicitly, never the real one: (a) start the new build on a copy that holds pre-change backups — they are listed unchanged, Schema reads 1; (b) set one exercise to AMRAP and one to EMOM, save a backup (Schema reads 2), change both, restore — the settings return; (c) restore a pre-change backup — every row is standard; (d) alter one backup row's style by direct SQL, restore — the error toast appears, is readable, and the plan and log are intact; (e) "Save current plan first", then restore.
- other: `Test Inventory Drift` (regenerate, commit); pyright baseline diff (no net-new diagnostics); the mutation arms. Final gate `/verify-and-polish`.
- reviewers at code time: `code-reviewer`, `architecture-reviewer` (DB / schema row), `product-risk-reviewer` (a route gains a new response outcome), `unslop-reviewer`.

*PR 2* — change type: Business logic (`utils/export_service.py`).
- pytest: `tests/test_exports.py`, plus `tests/test_export_weekly_summary_sheet.py`, `tests/test_export_blank_rep_bounds_contract.py`, `tests/test_export_blank_rep_bounds_gate0.py`, `tests/test_rep_range_integrity.py`, `tests/test_ui_flows.py`.
- e2e: none required by the change-type row; `e2e/api-integration.spec.ts` is run as a cheap check.
- other: `Test Inventory Drift`; pyright baseline diff; the mutation arms; open one downloaded workbook by hand in each view mode. Final gate `/unslop`.
- reviewers at code time: `code-reviewer`, `unslop-reviewer`.

**Re-review.** None of the three reviewers needs a re-run for the changes above: each is a reviewer's own finding applied, or the plan's own stated fallback. The one item no reviewer saw as written is the 30-second value in decision (ii); the mechanism is product-risk-reviewer's.

---

## Sign-off

- [x] Gate 0 complete when required by planning size; otherwise marked not applicable. *(Signed 13 November 2026 — see Section 0 sign-off.)*
- [x] Every finding has a disposition. *(31 rows in the response matrix: AR1–AR9; TS1–TS11 and test-strategist's position on D3; PR1–PR10. None deferred. The dispositions are the manager's proposals and are confirmed by the owner at Gate 1.)*
- [x] Agent provenance complete — both `product-manager` IDs, same-PM-resumed yes/no, the three reviewer IDs, and an evidence-gap line (or `none`).
- [x] Owner approved Plan v2 (Gate 1). *(Signed 14 November 2026 on the owner's behalf at the owner's instruction; decisions (i)–(iii) take the proposed option — see Gate 1 sign-off under Plan v2.)*
- [x] Ready to implement — proceed to code, then `/unslop` or `/verify-and-polish` for the diff-time gate.
