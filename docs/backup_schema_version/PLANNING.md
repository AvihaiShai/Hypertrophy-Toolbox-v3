# Plan Review — `BACKUP_SCHEMA_VERSION` as a reserved informational label (Testing Strategy D6)

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> Gate 0 owner decision: B.
>
> Treat BACKUP_SCHEMA_VERSION as a reserved informational label. Restore remains deliberately version-blind, with structural compatibility handled by column probing.
>
> Proceed with the Gate 0 requirements packet described in your analysis. Do not implement anything yet.
>
> The packet must:
> - define the current contract and the mandatory bump-and-branch rule for the next payload-shape change;
> - include the DECISIONS.md ADR so D6 is conclusively closed;
> - specify the exact tests, including replacing the tautological assertion with a persisted-DB assertion and pinning foreign-version restore behavior;
> - cover every documentation location and the missing APP_FLOW.md Schema-tile row you identified;
> - state whether Phase 3 step 11 is unblocked and define its correct fuzz target;
> - keep the two adjacent findings explicitly out of scope.
>
> Verify the cited locations first, stop at Gate 0, and report which file contains the completed packet. Do not modify the database, run restore, or begin implementation.

**Prior context.** Testing Strategy decision **D6** ([`docs/TESTING_STRATEGY_PLANNING.md:259`](../TESTING_STRATEGY_PLANNING.md#L259)) was, alongside D4, D7 and the `js-unit` half of D2, an unsigned owner decision (§8.1, §8.1a). A read-only trace on 2026-08-14 compared three dispositions (enforce / retain-informational / remove); the owner selected **B — retain as a reserved informational label**. The strategy doc's written preference was A; the owner's decision supersedes it, and the ADR below is what records that supersession rather than leaving it as drift.

---

### Problem

`BACKUP_SCHEMA_VERSION` ([`utils/program_backup.py:21`](../../utils/program_backup.py#L21)) is persisted, returned by four API endpoints, and displayed in the UI, but nothing reads it to make a decision. The TODO above it ([`:18-21`](../../utils/program_backup.py#L18-L21)) states that a first consumer "should read it in `restore_backup` to trigger field migration" — an intention the owner has now declined. Three consequences remain open:

1. **The field's status is undocumented.** Six documentation locations describe the column's existence; none state whether it is enforced, and the module's own TODO implies it is pending work. Every reader re-derives the question, which is why it became D6.
2. **There is no rule for the next payload-shape change.** The version already failed to track one: `BACKUP_SCHEMA_VERSION = 1` shipped in `720cb0e` (2026-02-03); `6b99535` (2026-02-05) added `superset_group` to `program_backup_items` **with** an `ALTER` migration ([`:70-75`](../../utils/program_backup.py#L70-L75)) and **without** bumping the constant. Rows labelled "v1" also span at least three column populations, because `create_backup` writes `exercise_order`/`superset_group` as `NULL` when the source columns are absent ([`:226-227`](../../utils/program_backup.py#L226-L227)). Retaining the field without a written obligation preserves the exact condition that made it meaningless.
3. **Its only test is tautological and hides a false green.** [`tests/test_program_backup.py:55`](../../tests/test_program_backup.py#L55) asserts `backup['schema_version'] == BACKUP_SCHEMA_VERSION` against the dict `create_backup` builds at [`:248`](../../utils/program_backup.py#L248) — a literal copy of the constant. The assertion never reads the database and would pass if the `INSERT` at [`:197-200`](../../utils/program_backup.py#L197-L200) omitted the column entirely.

Downstream, [`docs/TESTING_STRATEGY_PLANNING.md:203`](../TESTING_STRATEGY_PLANNING.md#L203) (Phase 3 step 11, backup-row fuzzing) is explicitly gated on D6 being decided first.

---

### Verified ground truth

Confirmed by direct read on 2026-08-14. Re-verify before relying on any line number.

| Stage | Location | Behavior |
|---|---|---|
| Definition | [`utils/program_backup.py:18-21`](../../utils/program_backup.py#L18-L21) | TODO + `BACKUP_SCHEMA_VERSION = 1` |
| DDL | [`:44`](../../utils/program_backup.py#L44) | `schema_version INTEGER NOT NULL DEFAULT 1`, inside `CREATE TABLE IF NOT EXISTS`. Never `ALTER`ed. |
| Write | [`:197-200`](../../utils/program_backup.py#L197-L200) | One `INSERT`. Sole production caller [`routes/program_backup.py:105`](../../routes/program_backup.py#L105), always `backup_type='manual'`. |
| Read | [`:290`](../../utils/program_backup.py#L290), [`:326`](../../utils/program_backup.py#L326), [`:345`](../../utils/program_backup.py#L345), [`:366`](../../utils/program_backup.py#L366), [`:665`](../../utils/program_backup.py#L665) | Five pass-through `SELECT`s. Nothing branches on the value. |
| Restore | [`:411-415`](../../utils/program_backup.py#L411-L415) | Selects `id, name, item_count` only — never reads the column. |
| Compatibility | [`:437-438`](../../utils/program_backup.py#L437-L438) | `_check_column_exists` probes the **destination** (`user_selection`); this is the mechanism that actually protects restores. |
| Destructive step | [`:445-446`](../../utils/program_backup.py#L445-L446) | `DELETE FROM workout_log` / `user_selection` inside `BEGIN IMMEDIATE`. |
| API | 4 endpoints on `/api/backups` (`POST`, `GET`, `GET <id>`, `PATCH <id>`) | Field present in each. Absent from the restore response ([`:567-572`](../../utils/program_backup.py#L567-L572)). |
| Frontend | [`static/js/modules/backup-center.js:550`](../../static/js/modules/backup-center.js#L550) → [`templates/backup.html:163-166`](../../templates/backup.html#L163-L166) | One "Schema" stat tile inside `#backup-detail-panel`, `hidden` at rest ([`backup.html:145`](../../templates/backup.html#L145)). JS falls back to `?? 1`. |
| Tests | [`tests/test_program_backup.py:21`](../../tests/test_program_backup.py#L21), [`:55`](../../tests/test_program_backup.py#L55) | Import + one tautological assertion. No E2E assertion; no `backup-center.js` unit test. `/backup` is a visual route ([`e2e/visual.spec.ts:21`](../../e2e/visual.spec.ts#L21)) but the tile sits behind the hidden panel. |
| Schema registry | [`utils/schema_registry.py:133-134`](../../utils/schema_registry.py#L133-L134), [`:22-24`](../../utils/schema_registry.py#L22-L24) | `initialize_backup_tables` runs every startup and inside `erase_data(force_base=True)`; `program_backups` is #2 in `OWNED_TABLES_DROP_ORDER`. |

**Entry vectors for a foreign version.** Backups are database rows, not importable files. A row with a version other than `1` can reach `restore_backup` only by (a) a future build writing it and the user then reverting to an older build, or (b) the user hand-placing a whole database file, which is governed by `prepare_runtime_database()` rather than by backup versioning. There is no import endpoint.

---

### Acceptance criteria

1. **Contract is stated at the definition site.** Given a developer opens [`utils/program_backup.py`](../../utils/program_backup.py), when they read the lines that define `BACKUP_SCHEMA_VERSION`, then they find a statement that the value is a **reserved informational label**; that `restore_backup` is **deliberately version-blind**; that structural compatibility is owned by `_check_column_exists`; and the TODO text at [`:18-21`](../../utils/program_backup.py#L18-L21) is gone.

2. **The bump-and-branch rule is written where the next author will hit it.** Given a future change adds, removes, or renames a column in `program_backup_items`, when the author reads either the module contract or [`docs/program_backups.md`](../program_backups.md), then they find a mandatory three-part obligation — bump `BACKUP_SCHEMA_VERSION`, add an `ALTER`-based migration in `initialize_backup_tables` in the shape of the `superset_group` precedent at [`:70-75`](../../utils/program_backup.py#L70-L75), and add the corresponding branch in `restore_backup` — together with the citation that `6b99535` (2026-02-05) skipped exactly this after `720cb0e` (2026-02-03) introduced the constant.

3. **The persisted value is asserted from the database.** Given a backup created through `create_backup`, when the test asserts its version, then the value is read by a fresh `SELECT schema_version FROM program_backups WHERE id = ?` through `DatabaseHandler`, not from the dict returned at [`:248`](../../utils/program_backup.py#L248).

4. **That assertion is proven non-vacuous, and the `DEFAULT 1` mask is defeated.** Given the column is declared `NOT NULL DEFAULT 1`, a persisted-value assertion alone still passes when the `INSERT` at [`:197-200`](../../utils/program_backup.py#L197-L200) drops the column, because the default supplies the same `1`. The test must therefore exercise a constant value that the default **cannot** satisfy — patching `utils.program_backup.BACKUP_SCHEMA_VERSION` to a value ≠ 1 and asserting the persisted row carries that value. When the mutation "remove `schema_version` from the INSERT column list" is applied, then the test **fails**; when it is reverted, then it passes. Both arms are run and recorded as evidence.

5. **Version-blind restore is pinned, using representative foreign integers only.** Given a `program_backups` row whose `schema_version` is `0` or `2` — the two representative foreign values, seeded by a direct `DatabaseHandler` write because `create_backup` cannot produce one — when `restore_backup` runs against it, then it completes exactly as for a version-`1` row: same `restored_count`, same `skipped` list, same resulting `user_selection` contents, and no exception. A future accidental version guard reds this test.

   **`NULL` is deliberately excluded and must not be added** (owner correction, Gate 0). The column is declared `NOT NULL` at [`:44`](../../utils/program_backup.py#L44), so SQLite rejects a `NULL` on both `INSERT` and `UPDATE`; a `NULL` row is unreachable through any supported path. Producing one would require manufacturing a malformed schema or bypassing the constraint (for example via `PRAGMA writable_schema`), which would test a state the application cannot enter and would make the fixture, not the product, the thing under test. `0` and `2` cover the two directions that matter — below the known version and above it.

6. **The API field is retained under contract.** Given `GET /api/backups` and `GET /api/backups/<id>`, when the response envelope is inspected, then each backup object contains `schema_version`. The field is informational but is part of the shipped response shape; a later silent removal must red.

7. **No production behavior changes.** Given the full pytest suite and `e2e/program-backup.spec.ts`, when they run before and after the change, then results are identical apart from the tests this packet adds or replaces. No route, no JS module, no template, and no SQL statement changes behavior; the only production-file edit is non-executable text at the definition site.

8. **Every documentation location is reconciled.** Given the six locations that describe the column plus the one gap identified in the trace, when the packet lands, then each states the same contract:
   - [`utils/program_backup.py:18-21`](../../utils/program_backup.py#L18-L21) — contract replaces the TODO (AC 1).
   - [`docs/program_backups.md:24`](../program_backups.md#L24) — storage table row gains the label semantics and the bump-and-branch rule (AC 2).
   - [`docs/product/BACKEND_SCHEMA.md:612`](../product/BACKEND_SCHEMA.md#L612) — `schema_version` column row notes it is informational; [`:74`](../product/BACKEND_SCHEMA.md#L74)'s existing "unrelated to `user_version`" note is kept and cross-referenced.
   - [`docs/LEFTOVERS_BY_PRIORITY.md:608`](../LEFTOVERS_BY_PRIORITY.md#L608) — disposition changes from "OWNER / D6 open" to resolved, citing the ADR.
   - [`docs/TESTING_STRATEGY_PLANNING.md:259`](../TESTING_STRATEGY_PLANNING.md#L259) — D6 row records the decision as **B**, noting it departs from the doc's own recommendation of A and why; [`:172`](../TESTING_STRATEGY_PLANNING.md#L172) (B11) drops the "escape hatch doesn't exist yet" framing for the settled contract; the sign-off state line and a new §8.1b move D6 out of the unsigned set, leaving the §8.1 and §8.1a tables frozen as historical record per their own stated convention.
   - [`docs/product/APP_FLOW.md`](../product/APP_FLOW.md) — **the identified gap**: the Backup Center control table ([`:594`](../product/APP_FLOW.md#L594) onward) has no row for the Schema stat tile. A row is added describing it as presentation-only, sourced from `schema_version` on the detail payload, always reading `1` today.

9. **D6 is closed by ADR.** Given [`docs/DECISIONS.md`](../DECISIONS.md), when the packet lands, then **ADR-008** exists in the log (ADR-001 through ADR-006 are taken; template at [`:95`](../DECISIONS.md#L95)), status `accepted`, dated, following the established Context / Decision / Consequences shape. Context carries the two load-bearing facts — the `6b99535` non-bump and the absence of any import path. Decision states the reserved-label contract, version-blind restore, and the bump-and-branch obligation. Consequences state what is knowingly accepted: a future v2 payload read by a build predating the bump would be restored without a guard, bounded by the fact that the only route to that state is an app downgrade on the same machine.

10. **Phase 3 step 11 is released with the correct target.** Given [`docs/TESTING_STRATEGY_PLANNING.md:203`](../TESTING_STRATEGY_PLANNING.md#L203), when the packet lands, then that step records that its D6 precondition is **discharged** and that its fuzz target is **type-confused / NULL / out-of-range `program_backup_items` rows** — not `schema_version`, which decision B leaves deliberately unread. The step's own instruction "do not fuzz a value that restore still ignores" is satisfied by naming the row-level target explicitly.

**Answer to the packet's Phase 3 question:** step 11 is **unblocked**, and its target is unchanged from the strategy doc's own corrected formulation — malformed persisted **rows**, asserting a clean error plus an intact live program. Decision B removes no scope from it and adds none. Step 11 remains a separate packet; see out of scope.

---

### Calculation surface

**`none`.**

No function in the calculation surface defined by [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) is touched. `create_backup` and `restore_backup` move persisted rows verbatim; they compute nothing. Effective sets, RIR/RPE handling, weekly/session summaries, progression, volume splitting, and fatigue are all untouched, and no value that reaches them changes. Per AC 7 the packet produces **no** behavioral delta at all — a before/after worked example would be identical by construction, which is itself the claim under test.

---

### In scope

- The contract statement replacing the TODO at the definition site (AC 1) and the bump-and-branch rule (AC 2).
- ADR-008 in [`docs/DECISIONS.md`](../DECISIONS.md) and the D6 sign-off reconciliation in [`docs/TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md) (AC 8, AC 9).
- Test changes in [`tests/test_program_backup.py`](../../tests/test_program_backup.py) only: replace the tautological assertion (AC 3–4), add foreign-version restore pinning (AC 5), add the API-field presence assertion (AC 6).
- The two-arm mutation evidence required by AC 4, recorded in the PR description.
- All seven documentation edits enumerated in AC 8, including the new `APP_FLOW.md` Schema-tile row.
- Regeneration of [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) — verified: [`scripts/generate_test_inventory.py`](../../scripts/generate_test_inventory.py) collects pytest and `rglob`s `e2e/**/*.ts`, and the CI drift check fails on any test add or removal.

### Out of scope / non-goals

- **Any enforcement of the version.** No guard, no supported range, no new error code, no UI state. That is option A, which the owner declined.
- **Any removal.** The column, the four API fields, the JS consumer, and the Schema tile all stay exactly as they are. Option C is declined and would need a separate explicit reversal.
- **`prune_auto_backups()` / `get_latest_auto_backup()`** ([`:618`](../../utils/program_backup.py#L618), [`:656`](../../utils/program_backup.py#L656)) — verified to have no production callers. **Adjacent finding, explicitly excluded**; it is its own decision under [`docs/TESTING_STRATEGY_PLANNING.md:203`](../TESTING_STRATEGY_PLANNING.md#L203), and adding tests here would entrench a dead surface.
- **The erase/backup-survival contradiction** — [`docs/program_backups.md:27`](../program_backups.md#L27) says backups survive an erase; `OWNED_TABLES_DROP_ORDER` drops both tables. **Adjacent finding, explicitly excluded**; already ledgered at [`docs/product/APP_FLOW.md:641`](../product/APP_FLOW.md#L641) and owned by whoever fixes that row. This packet must not "helpfully" correct line 27 while editing line 24 of the same file.
- Phase 3 step 11 implementation (backup-row fuzzing). Released by AC 10, executed elsewhere.
- Any template, SCSS, or JS edit — and therefore no visual-baseline exposure. The Schema tile is unchanged and sits behind a panel that is `hidden` at rest.
- Any database mutation, restore execution, or backup creation against a live database during this packet.

---

### Assumptions made

- ⚠️ **The `NOT NULL DEFAULT 1` mask is real but unproven by execution.** AC 4's requirement is derived by reading the DDL at [`:44`](../../utils/program_backup.py#L44) and the `INSERT` at [`:197-200`](../../utils/program_backup.py#L197-L200); no mutation was run during this read-only analysis. If implementation finds the default does **not** satisfy a column-dropped `INSERT`, AC 4 simplifies — but the two-arm evidence is still required, because the point is to prove the test is honest rather than to predict which arm fails.
- ⚠️ **`ADR-008` is the next free number.** Verified against the current [`docs/DECISIONS.md`](../DECISIONS.md) log (001–006 present, `ADR-NNN` template at [`:95`](../DECISIONS.md#L95)). A concurrent packet claiming 007 first would force a renumber.
- ⚠️ **`docs/product/APP_FLOW.md` has uncommitted working-tree changes** at the start of this session, and it is one of this packet's edit targets. Implementation must run in its own worktree and must not `git add -A`; the APP_FLOW row may need rebasing onto whatever lands first.
- ⚠️ **The Schema tile is assumed absent from every visual baseline** because `#backup-detail-panel` is `hidden` at rest ([`backup.html:145`](../../templates/backup.html#L145)). This packet changes no markup, so the assumption is not load-bearing here — but it must not be inherited as established fact by a later packet that does touch the tile.
- ⚠️ **No JS unit test is proposed** for [`backup-center.js:550`](../../static/js/modules/backup-center.js#L550). Under B the branch is a pass-through with a `?? 1` fallback and no behavior to pin; the module has no existing test file, so adding one would open a jsdom-harness question disproportionate to this packet. Recorded as knowingly not covered, not as an oversight.
- ⚠️ **The D6 row edit reverses the strategy doc's stated recommendation.** AC 8 requires the row to record *both* the recommendation (A) and the decision (B) with the reason, rather than silently rewriting the recommendation to match. Confirm that framing is wanted.

### Open questions for the user

- **None blocking.** The single Gate 0 decision — reserved label vs. enforced contract — is answered (B). The items above are ⚠️ assumptions for review, not blockers; work can proceed on this brief once the two sign-off boxes are checked.

---

### Section 0 sign-off — GATE 0

- [x] Owner confirms the acceptance criteria match intent — **approved 2026-08-14 with one required correction**: AC 5 drops `NULL` and pins version-blind restore with the representative foreign integers `0` and `2`. `schema_version` is `NOT NULL`, so a `NULL` row is unreachable without manufacturing a malformed schema, which is prohibited. Correction applied above.
- [x] Owner reviewed the assumptions and corrected or accepted each one — **all six accepted 2026-08-14**, with these standing instructions:
  1. Retain the patched constant ≠ 1 and **both** mutation arms even if runtime verification confirms the default-mask analysis.
  2. Re-check that `ADR-008` is free **immediately before editing** `docs/DECISIONS.md`.
  3. Use an isolated worktree; preserve the existing `docs/product/APP_FLOW.md` changes; never `git add -A`.
  4. The visual-baseline assumption is accepted as explicitly non-load-bearing.
  5. **No JavaScript unit-test harness is introduced in this packet.**
  6. Preserve **both** the strategy's recommendation of A and the owner's decision B, including the reason for the departure.
- [x] Blocking questions are answered — none outstanding; D6 answered as **B** on 2026-08-14.

**GATE 0 APPROVED — 2026-08-14.** Planning authorized. Implementation is **not** authorized.

---

## Plan v1

**Goal**: Close Testing Strategy D6 by making the reserved-label contract explicit at the definition site, in every document that describes the column, and in an ADR — and by replacing the one vacuous test with assertions that actually hold the contract — with **zero** change to shipped behavior.

### Routing

Per [`QUALITY_GATE.md` plan-stage routing](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) this is **Medium**, not Large: the work is bounded, its contracts are known, and it changes **no schema, no API shape, and no calculation surface**. Gate 0 was added because the requirements were ambiguous, which the routing table explicitly allows for Medium work; it has now been signed. The next gate is therefore **Gate 1 — owner plan approval**, not a council run. A council review is available if the owner wants one, but the routing does not require it and nothing in this packet meets the Large criteria.

Note the distinction the packet must not blur: AC 6 **pins** an existing API field so a later cleanup cannot silently drop it. Pinning a shipped shape in a test is not an API change.

### Scope

**In**
- The reserved-label contract replacing the TODO at [`utils/program_backup.py:18-21`](../../utils/program_backup.py#L18-L21), carrying the bump-and-branch rule.
- `ADR-008` in [`docs/DECISIONS.md`](../DECISIONS.md), plus the D6 sign-off reconciliation in [`docs/TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md).
- Three test changes in [`tests/test_program_backup.py`](../../tests/test_program_backup.py) and nowhere else.
- Two-arm mutation evidence for AC 4, recorded in the PR description.
- Seven documentation edits (AC 8), including the new `APP_FLOW.md` Schema-tile row.
- Regeneration of [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json).

**Out** — as Section 0. Restated for the implementer because each is a live temptation while editing adjacent lines:
- No enforcement, no guard, no error code, no supported range.
- No removal of the column, the four API fields, the JS consumer, or the Schema tile.
- **Do not touch [`docs/program_backups.md:27`](../program_backups.md#L27)** while editing line 24 of the same file.
- **Do not add tests for `prune_auto_backups()` / `get_latest_auto_backup()`** while editing the same test file.
- No template, SCSS, or JS edit — therefore no visual, CSS, or E2E exposure.
- No JS unit-test harness (owner instruction 5).

### Artifacts

| Path | Change | Notes |
|---|---|---|
| [`utils/program_backup.py`](../../utils/program_backup.py) | modify | Replace the TODO at `:18-21` with the contract + bump-and-branch rule. **Comment text only — no executable line changes.** |
| [`tests/test_program_backup.py`](../../tests/test_program_backup.py) | modify | Replace the tautological assertion at `:55` (AC 3–4); add foreign-version restore pinning for `0` and `2` (AC 5); add the API-field presence assertion (AC 6). |
| [`docs/DECISIONS.md`](../DECISIONS.md) | modify | `ADR-008`, status `accepted`. Renumber if a concurrent packet claims it first. |
| [`docs/program_backups.md`](../program_backups.md) | modify | Storage-table row `:24` + the bump-and-branch rule. Line 27 untouched. |
| [`docs/product/BACKEND_SCHEMA.md`](../product/BACKEND_SCHEMA.md) | modify | `:612` column row notes the label semantics; cross-reference the existing `:74` note. |
| [`docs/product/APP_FLOW.md`](../product/APP_FLOW.md) | modify | **New** Schema-tile row in the Backup Center control table (`:594`+). Preserve the concurrent working-tree edits. |
| [`docs/LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md) | modify | `:608` disposition → resolved, citing `ADR-008`. |
| [`docs/TESTING_STRATEGY_PLANNING.md`](../TESTING_STRATEGY_PLANNING.md) | modify | D6 row `:259` (both A and B, with the reason); B11 `:172`; sign-off `:262-263` + §8.1; step 11 `:203` precondition discharged. |
| [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) | regenerate | Script output only — never hand-edited. |
| [`docs/backup_schema_version/PLANNING.md`](PLANNING.md) | modify | Evidence section + sign-off history. |

**Effort**: S · **Owner**: `senior-developer` · **Depends on**: nothing. Two concurrent-packet collisions are tracked below.

### Sequence

1. **Create an isolated worktree** and `git merge --ff-only origin/main` inside it — `new-worktree.ps1` branches from main's stale HEAD. Never `git add -A`; stage by explicit path.
2. **Re-check `ADR-008` is still free** (owner instruction 2). `docs/release_pipeline/PLANNING.md:309` plans an ADR of its own; if it landed first, take the next number and update every cross-reference in one pass.
3. **Write the contract** in `utils/program_backup.py`, replacing the TODO. Verify by `git diff` that no executable line moved.
4. **Test AC 3–4 first** — the persisted assertion with the patched constant ≠ 1. Run it green.
5. **Prove it non-vacuous**: apply the mutation (drop `schema_version` from the `INSERT` column list), confirm the test **reds**, revert, confirm it greens. Record both arms verbatim. If the mutation does **not** red, the test is wrong — fix the test, not the mutation, and re-run both arms.
6. **Tests AC 5 and AC 6**: foreign-version restore pinning (`0`, `2`) and the API-field presence assertion.
7. **Documentation** — the seven locations, `ADR-008` last so it can cite the final state. Re-read each neighbouring paragraph before saving: the failure mode on docs packets here is an edit that falsifies untouched adjacent prose.
8. **Regenerate the test inventory** and confirm the drift check passes locally.
9. **Verification** — targeted pytest, then the full suite, then `code-reviewer` and `unslop-reviewer` (both; they catch disjoint failure modes on docs packets).

Ordering rationale: the mutation proof (step 5) runs **before** any documentation is written, so a test that turns out to be vacuous is discovered while the packet is still cheap to re-scope.

### Expected gates

*Draft — `test-strategist` confirms at Gate 1 if a council run is added.*

- **pytest**: `tests/test_program_backup.py` targeted, then the full suite. Full pytest is required regardless of scope — it carries the working-tree-cleanliness and manifest-digest checks that a targeted run does not.
- **Test-inventory drift check**: mandatory — the gate fails on any test add or removal.
- **E2E**: none expected. No route, template, or JS file changes. To be confirmed at Gate 1 rather than assumed.
- **Visual / CSS**: none. No markup or style file is touched.
- **pyright**: measure-only, but it blocks net-new diagnostics; the packet adds no annotations, so no movement is expected.

### Newly discovered — concurrent-packet collisions

Both found while verifying, after Gate 0 was drafted. Neither blocks planning; both must be re-checked at implementation time.

1. ⚠️ **`docs/release_pipeline/PLANNING.md` (untracked, another session) plans its own ADR** in `docs/DECISIONS.md` (`:309`). Whichever lands second renumbers. This is exactly why owner instruction 2 exists; step 2 above enforces it.
2. ⚠️ **That packet defines its own local decision label "D6"** (`:24` — a CI concurrency group, `release-${{ github.ref }}`), unrelated to Testing Strategy D6. A grep for `D6` across `docs/` now returns two different decisions. Every D6 reference this packet writes must be qualified as *Testing Strategy* D6.
3. ⚠️ **Both packets edit `docs/TESTING_STRATEGY_PLANNING.md`** — theirs touches Phase 4 step 13 status only (`:310`), mine touches `:172`, `:203`, `:259`, `:262-263`, and §8.1. The regions do not overlap, so a clean merge is expected, but it is not guaranteed if either grows.
4. ⚠️ **The `APP_FLOW.md` edits cannot literally be preserved inside a worktree.** They are *uncommitted* in the main checkout's working tree, so a worktree branched from `HEAD` will not see them. Measured: the pending diff is 3 insertions / 2 deletions at lines 8 and 268-269 — far from the Backup Center table (`:594`+), so the two edit sets should merge cleanly. Owner instruction 3 is satisfied by never touching the main checkout, not by carrying the diff across. **Do not "restore" the missing lines inside the worktree** — that would duplicate them when the other session commits.

### Section — Gate 1 sign-off

- [x] Owner approved Plan v1 on 2026-08-14 ("proceed now"); no council run requested.

---

## Evidence

Implemented in worktree `D:/development/Hypertrophy-Toolbox-v3-main-d6-backup-schema`, branch
`wt/d6-backup-schema`, based on `origin/main` `9be1a3f`.

### Base moved before implementation

`new-worktree.ps1` branched from the shared checkout's stale HEAD `a224b39`, as expected;
`git merge --ff-only origin/main` advanced it to `9be1a3f` (30 files). **One target line number
drifted**: the `schema_version` row in `LEFTOVERS_BY_PRIORITY.md` moved from `608` to **`638`**.
Every other cited location was re-verified unchanged at `9be1a3f` before editing.

### AC 4 — the mutation proof (both arms)

The ⚠️ assumption that `NOT NULL DEFAULT 1` masks a dropped column is now **measured, not derived**.

| Arm | `create_backup` INSERT | Result |
|---|---|---|
| Mutated | `schema_version` removed from the column list | **1 failed, 39 passed** — only `test_schema_version_persists_the_constant` |
| Reverted | restored byte-identical (verified by `git diff`) | **40 passed** |

The decisive detail is the mutated arm's *passes*: the plain persisted assertion added to
`test_create_backup_saves_active_program_data` **survived** the mutation, because the column
default supplied the same `1` the constant would have. A persisted-DB read alone would have been a
false green. Only the patched-constant test (`7`, a value the default cannot produce) detects it.

### Suite results

- Targeted: `tests/test_program_backup.py` **40 passed** (36 → 40).
- Full: **2855 passed, 2 skipped** in 221.62s.
- Test inventory regenerated by script; delta is exactly `2531 → 2535` collected and
  `test_program_backup.py` `36 → 40`. No other row moved.

### Scope discipline

Both excluded adjacent findings were left untouched and verified so: `program_backups.md:27`'s
erase claim is unedited (only a new subsection was added after it), and no test was added for
`prune_auto_backups()` / `get_latest_auto_backup()`.

One correction made during review of my own edit: the first draft of the `BACKEND_SCHEMA.md` note
attributed the existing `user_version` remark to the "Relationship diagram" section, which is not
where it lives. Rewritten to point at the opening section instead — the falsifies-neighbouring-prose
failure class this packet was explicitly warned about.

### Review round (`code-reviewer` + `unslop-reviewer`)

Both ran against the staged diff and found real defects; both were applied. The two highest-value
findings were ones this packet's own process had missed:

1. **The only production edit stated a fact the packet's own evidence contradicted.** The contract
   comment claimed `6b99535` added `superset_group` "without any of the three" obligations.
   Verified against the commit: it added the `ALTER` migration **and** five `has_superset` restore
   lines, skipping only the bump. Corrected — a wrong fact in the one comment the packet exists to
   write would have been the worst possible defect here.
2. **AC 6 was under-implemented.** The first version pinned `schema_version` only on the two `GET`
   responses, so deleting it from `create_backup()`'s returned dict left the suite green — exactly
   the silent removal AC 6 exists to catch. Extended to all four responses and **mutation-verified**:
   removing `'schema_version'` from the returned dict now reds
   `test_api_responses_carry_schema_version` (1 failed, 39 passed), and the line was restored with
   `git diff origin/main -- utils/program_backup.py` confirming the file is comment-only.

**AC 8 under-enumerated the documentation surface.** Seven further live "D4, D6 and D7 remain
unsigned" claims existed outside the six locations the brief listed —
`TESTING_STRATEGY_PLANNING.md:16` (the masthead), `:569`, `:846`; `LEFTOVERS_BY_PRIORITY.md:423`;
`MASTER_HANDOVER.md:34`, `:2330`; `ai_workflow/INDEX.md:29` — plus a §4 preamble at
`LEFTOVERS_BY_PRIORITY.md:629` still reading "Four `TODO` markers … covering three decisions"
against a measured three markers and two decisions. All corrected. The §8.1 and §8.1a tables were
left frozen, which their own text requires. `MASTER_HANDOVER.md` and `ai_workflow/INDEX.md` were
outside the declared artifact list and were added rather than deferred: leaving the canonical
current-state doc asserting D6 is unsigned while `DECISIONS.md` records ADR-008 as accepted is the
same falsified-neighbouring-prose failure the packet was warned about.

Also applied: trimmed the duplicated history retelling in `program_backups.md` and the disposition
cell in `LEFTOVERS_BY_PRIORITY.md`; named the correct section in the `BACKEND_SCHEMA.md`
back-pointer (the *Constraint enforcement* section — my earlier in-flight correction was still
wrong); qualified the two test-file `D6` references as *Testing Strategy* D6 per this packet's own
collision note; corrected ADR-008's "Two tests" to three; refreshed `program_backups.md`'s date
stamp.

**Declined:** removing the persisted assertion from `test_create_backup_saves_active_program_data`.
`unslop-reviewer` is right that it cannot fail on its own, but AC 3 is owner-approved and the
assertion still pins that the row exists and is readable. Its comment was shortened and states
plainly that the non-vacuous check lives elsewhere.

### Newly discovered during implementation

⚠️ **Phase 3 step 11 is already being implemented** in worktree `wt/packet-e-restore-fuzz`
(untracked `tests/test_program_backup_restore_fuzz.py`, 3 tests, plus `docs/testing_phase3/`),
which began before D6 was signed. Inspected read-only: it does **not** fuzz `schema_version` — it
deliberately builds every header through production `create_backup()` so it stays independent of
the header schema, and its own docstring says so. It is therefore consistent with decision B, and
this packet's §8.1b discharges the precondition it was already relying on. Two consequences: the
two packets both regenerate `TEST_INVENTORY.json`, so whichever lands second must regenerate again;
and one of its tests is named `test_known_defect_weekly_summary_500_after_restoring_non_numeric_rep_range`,
i.e. it appears to have found a real defect — **not this packet's scope**, flagged only so it is
not lost.
