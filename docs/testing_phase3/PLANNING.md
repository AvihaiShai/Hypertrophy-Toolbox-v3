# Testing Strategy Phase 3 — Packet E (restore-path fuzz characterization)

> **Scope**: one new test file that characterizes what `restore_backup()` accepts and the plan routes
> reject, plus the single downstream shape that turns a restored row into an HTTP 500. Test-only.
> **No production file is owned by this packet.**
> **Base**: `origin/main` @ `94f0d8c`, branch `wt/packet-e-restore-fuzz`, isolated worktree.
> (Implemented against `f627161`; fast-forwarded to `94f0d8c` at integration time — §7.1.)
> (Planned against `a64ea76`; `origin/main` moved **twice** mid-session and the branch was
> fast-forwarded before each inventory regeneration — §7.)
> **Gate 0**: **CLOSED** by the owner — decisions in §1 are fixed and not reopenable here.
> **Gate 1**: **CLOSED** 2026-08-14 under the owner's conditional approval — see §6.5. Plan v2 stays
> inside §3's scope and §3.5's owned paths and adds no production file, so implementation proceeds.

**Reading this document**: §1–§5 are Plan v1 amended in place. Every amendment carries a
**[v2 · <finding id>]** marker naming the council finding that forced it. §6 holds the provenance,
the full response matrix, and the Plan v2 design. Where a v1 passage was superseded outright
it is marked **SUPERSEDED** and points at §6.4 rather than being rewritten in two places.

> **§6.4 is a PREDICTION, not a record.** Two of its predicted mutation outcomes were **measured
> wrong** (M3 and M8), and the test that shipped differs from what §6.4 prescribes. **§7 is the
> authority on what was built and what happened.** Where the two disagree, §7 wins — the affected
> §6.4 rows carry an inline `[v2-exec]` correction pointing here.

## 1. Owner decisions (fixed)

*Unamended by the council. No reviewer proposed a change here, and none could — these are Gate 0.*

1. **Out-of-range-but-typed rows are CHARACTERIZATION ONLY.** Packet E must not change restore
   behavior or calculation semantics. The tests pin what the code does today; they do not assert
   what it ought to do.
2. **Threat model**: legacy backups created before workout-bound validation existed, plus malformed
   persisted rows as a robustness model. Direct/manual DB editing is **not** a supported workflow,
   and the packet does not depend on decision D7. The model **includes** non-numeric type confusion
   and correctly typed bound/order violations, and **excludes** numeric-looking strings that SQLite
   coerces.
3. **Scope lock**: `BACKUP_SCHEMA_VERSION` / decision **D6** and `prune_auto_backups()` are excluded
   completely. Not tested, not referenced as a dependency, not touched.
4. **If an honest test exposes a defect, Packet E stops at a documented finding.** Any production fix
   is a separate owner-gated packet carrying migration notes per CLAUDE.md §1. No production files
   are owned here.

## 2. Reconciliation

### 2.1 The thesis — verified by reading, not inferred

> **Line-citation drift, re-measured 2026-08-15 at `94f0d8c`.** Every
> `utils/program_backup.py` line number in this document was measured at `f627161`. #373 (D6 /
> ADR-008) added a 13-line contract comment at the top of that module, shifting everything below
> it by **+10**. The anchors in this paragraph are re-pinned to the current base; **elsewhere in
> this document, add 10** — e.g. §3.4's `:451` is now `:461`, and §7's `:445-446` is now
> `:455-456`. Verified current anchors: `restore_backup()` **`:399`**, item `SELECT`
> **`:433-438`**, deletes **`:455-456`**, catalog skip **`:465`**.

`restore_backup()` (`utils/program_backup.py:399`, item loop `:461-558`) applies **no** bounds
validation. It reads ten columns at `:433-438` and passes them into the `INSERT INTO user_selection`
at `:474-557`; nine of the ten go through `item.get(...)` unexamined, and the only filter on the
tenth is the catalog-membership check at `:465` (`exercise_name not in valid_exercise_names` → skip).

So a persisted backup item can carry values that `POST /add_exercise` and `POST /update_exercise`
reject at the boundary. Restoring such a backup writes those values into `user_selection` and returns
HTTP 200. For **one** shape — non-numeric text in a rep-range column — the resulting row makes
`GET /weekly_summary` return 500.

### 2.2 Reachability audit — this is what reshaped the packet

`validate_workout_bounds` (`utils/workout_validation.py:31`) validates exactly four fields: `weight`,
`rir`, `min_reps`, `max_reps`. It is called at `routes/workout_plan.py:87` (add),
`routes/workout_plan.py:402` (update), and `utils/exercise_manager.py:40`.

| Shape | Plan routes | Restore path | Classification |
|---|---|---|---|
| `weight` > 1000 or < 0 | rejected 400 | accepted | restore-only → characterize |
| `rir` > 10 or < 0 | rejected 400 | accepted | restore-only → characterize |
| `min_rep_range` > `max_rep_range` | rejected 400 | accepted | restore-only → characterize |
| `min`/`max_rep_range` = non-numeric text | rejected 400 via `_number()` | accepted | restore-only → **DEFECT PROBE** |
| `sets` = any truthy value | **ACCEPTED** (never validated) | accepted | route-reachable → **OUT OF SCOPE** |
| `rpe` = any value | **ACCEPTED** (never validated) | accepted | route-reachable → **OUT OF SCOPE** |

`utils/exercise_manager.py:36` gates `sets` on truthiness alone
(`if not all([routine, exercise, sets, min_rep_range, max_rep_range])`), and
`routes/workout_plan.py:386` lists `sets` and `rpe` in `valid_fields` for update while neither
reaches the validator. Bounds constants: `MIN_WORKOUT_WEIGHT_KG = 0.0`,
`MAX_WORKOUT_WEIGHT_KG = 1000.0`, `MIN_RIR = 0.0`, `MAX_RIR = 10.0` (`utils/constants.py:7-10`).

The two `OUT OF SCOPE` rows are the reason this packet is three nodes and not six: a shape the public
plan API already accepts is not a restore-path finding. It is recorded as FINDING-2 (§3.7).

### 2.3 The defect chain

```
program_backup_items.min_rep_range = 'abc'   non-numeric TEXT survives INTEGER affinity
  → POST /api/backups/<id>/restore           routes/program_backup.py:144
  → utils/program_backup.py:451-548          no validation
  → user_selection.min_rep_range = 'abc'     typeof() = text
  → GET /weekly_summary                      routes/weekly_summary.py:39
  → utils/weekly_summary.py:246              rows = db.fetch_all(_WEEKLY_PLAN_QUERY), FROM user_selection
  → utils/weekly_summary.py:86               ('abc' + 12) / 2.0 → TypeError
  → routes/weekly_summary.py:125             except Exception → renders error.html, HTTP 500
```

Line 86 sits inside `_aggregate_weekly_volumes` (`def` at `utils/weekly_summary.py:53`, next `def` at
`:153`), which `calculate_weekly_summary` calls at `:248`.

**[v2 · TS2/PR1] This chain is one site of several, not the whole defect.** Guarding `:86` alone does
not stop the 500 — execution continues into `calculate_effective_sets` and detonates again on the
byte-identical arithmetic at `utils/effective_sets.py:192`. `utils/session_summary.py:99-100` carries
the same arithmetic off the same `user_selection` join. FINDING-1 (§3.7) names every site.

**[v2 · A6] The XHR trap has THREE triggers, not one.** `routes/weekly_summary.py:127` branches on
`is_xhr_request()`, which returns true for an `X-Requested-With` header, **or** `'application/json'`
in `Accept`, **or** a path starting `/api/` (`utils/errors.py:52-63`). Only the first two can reach
`/weekly_summary`; the third is why the restore POST is unaffected. That branch returns a JSON
`error_response("INTERNAL_ERROR", ...)` and never renders `error.html`. N2 asserts the HTML error
branch, so its request must carry **neither** reachable trigger. The Flask test client defaults
satisfy that.

### 2.4 Measured SQLite evidence — the anti-vacuity basis

An in-memory replica of both `CREATE TABLE` statements accepted **9 of 11** malformed shapes in
**both** tables. Only `NOT NULL` bites; neither table declares a single `CHECK` constraint.

| Observation | Consequence for the fixtures |
|---|---|
| Non-numeric text survives INTEGER affinity (`sets='abc'` stores as `text`) | This is the vector. `typeof()` must be asserted, not just equality. |
| **Numeric-looking text is COERCED** (`min_rep='8'` stores as `integer`) | Numeric-looking strings are **not** a vector and must **never** be used as a fixture value. A test built on `'8'` would be vacuous. |
| `float('abc')` at `utils/effective_sets.py:244` → `ValueError` | Downstream blast radius of the out-of-scope `sets` shape (FINDING-2). |
| **[v2 · TS12]** `('abc' + 12) / 2.0` at `utils/weekly_summary.py:86` → `TypeError` | Confirms the arithmetic, not the storage, is where a text rep-range detonates. Stated with `'abc'` because row 2 rules `'8'` out as a fixture value — the v1 wording used `'8'` here and contradicted itself. |
| `get_effort_factor` clamps at `utils/effective_sets.py:158` — `max(0, min(10, effective_rir))` | Why `rir=99` is absorbed rather than fatal. |
| `get_rep_range_factor` averages at `utils/effective_sets.py:192` — `(min_reps + max_reps) / 2.0` | Why an inverted rep range is absorbed rather than fatal. |

Bucket tables, quoted because Plan v2's oracle depends on them: `EFFORT_FACTOR_BUCKETS`
(`utils/effective_sets.py:64-69`) = `(0,1) 1.0`, `(2,3) 0.85`, `(4,5) 0.70`, `(6,10) 0.55`.
`REP_RANGE_FACTOR_BUCKETS` (`:75-81`) = `(1,5) 0.85`, `(6,12) 1.0`, `(13,20) 1.0`, `(21,30) 0.85`,
`(31,100) 0.70`.

Schema facts confirmed in the worktree: `program_backup_items` (`utils/program_backup.py:53-67`) and
`user_selection` (`utils/db_initializer.py:184-197`) declare **identical** `NOT NULL` sets on every
shared column — `routine`, `exercise`, `sets`, `min_rep_range`, `max_rep_range`, `weight` are
`NOT NULL`; `rir`, `rpe`, `superset_group` are nullable. `user_selection` additionally carries
`UNIQUE (routine, exercise, sets, min_rep_range, max_rep_range, rir, rpe, weight)` at
`db_initializer.py:196`; `program_backup_items` carries no such constraint.

### 2.5 Four nodes removed from the earlier draft

Each removal is evidence-backed. None is a scope trim for convenience.

| # | Removed node | Evidence |
|---|---|---|
| **C1** | The original **F4** node | **NOT CONSTRUCTIBLE.** It required a `program_backup_items` row that violates a `user_selection` `NOT NULL`. Both tables declare identical `NOT NULL` sets on every shared column (see §2.4), so no such row exists. Removed. |
| **C2** | A restore-rollback node | **ALREADY COVERED** by `tests/test_program_backup.py::TestProgramBackup::test_restore_rollback_preserves_active_program_on_failure` (`:226`). It seeds a live program, forces a `sqlite3.Error` on the third `INSERT INTO user_selection` via a monkeypatched `DatabaseHandler.execute_query`, and asserts the live program survives. Same invariant, same code path, same oracle. Not duplicated. |
| **C3** | The mutation "delete `db.connection.rollback()` at `utils/program_backup.py:551`" | **VACUOUS.** `DatabaseHandler.__exit__` (`utils/database.py:514-518`) rolls back whenever `exc_type` is truthy, and `restore_backup` re-raises at `:552`, so the exception exits the `with` block and `__exit__` rolls back anyway. The mutation stays **GREEN**. Removed with no replacement, because C2 already removed the test it was meant to validate. |
| **C4** | The duplicate-items `UNIQUE` variant | **CONSIDERED AND EXCLUDED.** It is constructible — `user_selection` carries the composite `UNIQUE`, `program_backup_items` does not — and correctly labelled it is a malformed/corrupted persisted backup rather than a user workflow. But it reaches the identical rollback path with the identical oracle as C2's existing test. No new invariant. Excluded. |

**[v2 · TS2] C3's failure mode recurred on a new axis.** C3 was a mutation that stayed green because
a second mechanism produced the same observable. N2's v1 source mutation had the identical defect for
the identical reason — a second arithmetic site produces the same 500. §6.4 replaces it with two
arms. **[v2 · A2]** C4's constraint asymmetry is not merely excluded trivia: it is a live collision
route that N3 must guard against, which is why N3 now varies a non-bounded column across its items.

### 2.6 [v2 · PR3] Threat model — the evidenced leg

Owner decision 2 (§1) names two legs. Plan v1 leaned on the **unevidenced** one and never joined it
to the live one. Corrected:

A malformed **persisted** row is reachable **today**, with no legacy build in the story.
`routes/workout_plan.py:386` writes `sets` and `rpe` unvalidated — `:402-407` passes only `weight`,
`rir`, `min_reps` and `max_reps` to the validator — and `create_backup()` copies `user_selection`
verbatim (`utils/program_backup.py:188-192`). So the *class* "a backup item holds a value the
validator would reject" is demonstrable on the current tree. Only the *specific column* N2 uses
(`min_rep_range`) is gated on both write paths today.

"Legacy backups written before workout-bound validation existed" is therefore recorded as a **stated
assumption**, not evidence. The packet does not rest on it.

## 3. Packet E

One new file, two module-level helpers, three test functions, seven collected nodes — five
parametrized, two not. (No class; §3's earlier "one class" was never built.)

### 3.1 Nodes

**N1 — `test_restore_accepts_rows_the_plan_route_rejects`** · 5 parametrized nodes ·
`weight_above_max` (`99999.0`), `weight_negative` (`-50.0`), `rir_above_max` (`99`),
`rep_range_inverted` (min `20` / max `5`), `min_rep_non_numeric` (`'abc'`).

Four **ordered** assertions per node:

| Step | Assertion |
|---|---|
| (a) precondition | the seeded value is in `program_backup_items` verbatim, `typeof()` matches intent, and **[v2 · TS5]** `SELECT COUNT(*) FROM program_backup_items` for that backup `== 1`, plus the fixture `UPDATE`'s own `rowcount == 1` |
| (b) boundary | `POST /add_exercise` → 400, `error.code == "VALIDATION_ERROR"`, and **[v2 · TS4]** the payload is otherwise **fully valid with exactly one malformed field**, asserting the **exact** message |
| (c) restore | `POST /api/backups/<id>/restore` → 200, `ok` is `True`, `data.restored_count == 1` |
| (d) persisted | `user_selection` holds the value verbatim — equality **and** `typeof()` |

**[v2 · TS5]** v1 used the header's `item_count` as the precondition. That is the wrong column:
`restore_backup` selects `item_count` at `:411-415` but reads only `backup['name']` from that row at
`:420`; the items come from the independent query at `:423-428`. A correct `item_count` therefore
proves nothing about what restore will iterate.

**[v2 · TS4]** v1's step (b) was vacuous: `VALIDATION_ERROR` has three producers in
`routes/workout_plan.py` — `:85` (no data), `:95` (bounds), `:129-140` (missing fields) — so a
malformed *payload* could satisfy the assertion without the *value* ever reaching the validator.

**N2 — `test_known_defect_weekly_summary_500_after_restoring_non_numeric_rep_range`** · 1 node ·
**THE ONLY DEFECT PROBE.** Restore via the public endpoint, then `GET /weekly_summary` with neither
XHR trigger (§2.3). Oracle: restore 200, summary **500**, the response is the HTML error template —
whose byte markers already exist at `tests/test_error_page_contract.py:79-82` **[v2 · A5]** — and the
logged exception is a `TypeError` whose **innermost frame is `_aggregate_weekly_volumes`**. A 500 from
an unrelated cause must not satisfy this node. The frame half of the oracle is load-bearing, and
§6.4's Arm B is what proves it.

**N3 — `test_weekly_summary_returns_200_without_validating_restored_out_of_range_numerics`**
· 1 node · characterization. **[v2 · PR5]** Renamed from `..._absorbs_...`: 200 is not correctness.
The restored values are not validated, corrected, or flagged — they propagate into the displayed
Effective sets, Raw sets and total volume with **no user-visible signal**.

> **SUPERSEDED — [v2 · A1/TS1/PR9/A2/TS10/TS3].** v1's N3 oracle ("`get_rep_range_factor(20, 5)`
> returns the bucket for `avg_reps == 12.5`") was vacuous, and v1's own remedy — pin `12.5` directly —
> was not implementable: `avg_reps` is a **local** at `effective_sets.py:192`, never returned.
> **Replaced in full by §6.4, as further corrected by §7.1.**
>
> Two points survive here because nothing else carries them. **[v2 · PR9]** The product fact is a
> **property**, not a value: an inverted rep range is treated as its **midpoint, symmetrically**, and
> that is **accidental behavior, not a designed contract** — a bounds-fix packet may legitimately
> change it, and N3's failure afterwards is expected churn. **[v2 · A2]** N3 restores **one item**, so
> the `user_selection` composite `UNIQUE` (`db_initializer.py:196`, absent from
> `program_backup_items`) cannot collide mid-restore; v1's "vary a non-bounded column across items"
> describes a multi-item shape that was **not built**.

### 3.2 Classification table

| Node | Classification |
|---|---|
| N1 `weight_above_max` / `weight_negative` / `rir_above_max` / `rep_range_inverted` | characterization |
| N1 `min_rep_non_numeric` | characterization + precondition for N2 |
| **N2** | **DEFECT PROBE — the only node licensed to claim a defect** |
| N3 | characterization |

**[v2 · A8/TS6] The classification must live in the test file, not only here.** A future reader hits
the test, not the plan. Therefore:

- The **module docstring** carries the N1 warning — these nodes assert the *absence* of validation, so
  a future fix packet is **expected** to red them; that is correct churn, not a regression.
- N2's **node docstring** states that green means the defect is **present**.
- N2's node name contains **`known_defect`**, so `rg known_defect tests` finds it. Without that, the
  likeliest failure mode is a later agent "fixing" the failing assertion.

### 3.3 Fixture strategy

1. Create a valid backup through **production** `create_backup()` from a valid plan.
   **[v2 · A9] Never hand-write the header `INSERT`.** Building the header through production code
   means no `schema_version` literal is hard-coded here, so a future D6 packet cannot silently
   reroute these nodes past a header they no longer recognize. This is a constraint, not a
   convenience.
2. Rewrite **only** the target `program_backup_items` column via a direct `UPDATE` inside
   `DatabaseHandler`. The row stays schema-valid; only the value is one an older build would have
   written.

   > **[v2 · PR4] Explicit non-claim (reviewer's wording, kept verbatim):** the `UPDATE` is a
   > **HARNESS DEVICE** for constructing a persisted state, **not a modelled user action**. Packet E
   > makes no claim that hand-editing the database is supported, expected, or protected. What is
   > modelled is the **STATE**. This paragraph also goes in the test module docstring.

3. **Before any restore** **[v2 · TS5]**: assert the stored value, assert SQLite `typeof()`, assert
   `SELECT COUNT(*) FROM program_backup_items` for the backup `== 1`, and assert the fixture
   `UPDATE`'s own `rowcount == 1`. A restore that reads zero items then cannot pass N1 step (c), and
   a silently-missed `UPDATE` cannot pass step (a).
4. Exercise restore through the **public endpoint**, never `restore_backup()` directly.

Reuse the existing `clean_db` / `exercise_factory` / `workout_plan_factory` fixtures from
`tests/conftest.py`, as `tests/test_program_backup.py` does. **Introduce no new fixture names.**

**[v2 · PR10] Fixture value.** `'8-12'` is the more credible legacy story — a build that persisted a
rep *range* as display text. The fixture value stays **`'abc'`**: both are non-numeric and detonate
identically, and `'abc'` cannot be misread as a coercible numeric by a later reader (§2.4 row 2).

**[v2 · TS8] Optional-subscript discipline, everywhere.** `pyright` checks `tests/**`, and
`fetch_one` returns an `Optional`, so every `fetch_one(...)['col']` is a net-new
`reportOptionalSubscript`. Mandatory shape throughout the file:

```
row = db.fetch_one(...)
assert row is not None
value = row['col']
```

### 3.4 Red-path evidence — no vacuous mutations

> **[v2-exec] These are PREDICTIONS. Two were measured wrong — see §7.1 for what actually happened.**
> The rows below are kept as the planning record, not as results.

| Node | Arm | Mutation | Required result | Rationale |
|---|---|---|---|---|
| **N1** | (1) SOURCE | **[v2 · TS9]** insert a `validate_workout_bounds` call into the item loop at `program_backup.py:451` as a **SKIP variant**, mirroring the catalog skip at `:455-460` — the invalid item is skipped and `restored_count` drops | N1 **reds on all 5 params** | v1 under-specified this: a mutant that computes `bounds_error` and then ignores it stays green, proving nothing. The skip variant changes an observable. |
| **N1** | (2) TEST | step (b) expected 400 → 200 | red; revert → green | Both directions. |
| **N1** | (3) FIXTURE | seed a valid in-bounds value, assertions unchanged | step (a) or (b) **reds** | **[v2-exec] PREDICTION — outcome differed (§7.1, M3).** As first written this arm stayed **GREEN**, because the seeded value and the payload value were separate tuple elements and only one moved. After the fix, `updates` drives both, so the arm reds at step (b). It no longer isolates the fixture from the payload; it proves the value is load-bearing **end-to-end**, which is the stronger property. |
| **N2** | (1) SOURCE | **SUPERSEDED — two arms, see §6.4** | Arm A → 200 (N2 reds); Arm B → still 500 but N2 reds on the frame | v1's single-site guard was vacuous for C3's reason on a new axis (§2.5). |
| **N2** | (2) TEST | flip the expected status | red; revert → green | Both directions. |
| **N2** | (3) **BASELINE ARM** | **[v2 · TS6]** run N2 against the **unmodified tree** | must be **GREEN** | Renamed from "rival-branch arm": Packet E changes **zero** production files, so `origin/main` is byte-identical to the branch and there is no rival to run. The arm is real, the name was not. **Inverted meaning**: green here says the defect is present. |
| **N3** | (1) SOURCE | **SUPERSEDED — two distinct site mutations, see §6.4** | `weekly_summary.py:86` → `raw_total_reps` 37.5 → 15.0. **[v2-exec] `effective_sets.py:192` does NOT move `effective_weekly_sets`** — see §7.1, M8 | v1 had one mutation for two averaging sites. The `weekly_summary.py:86` half holds as predicted. The `effective_sets.py:192` half was **measured wrong**: `expected_effective` recomputes `get_rep_range_factor(20, 5)` at assertion time, so both sides move together and cancel. That site is pinned by the **symmetry** assertion instead (§7.2). |
| **N3** | (2) TEST | flip each expected number in §6.4's oracle | red; revert → green | Both directions. |

N1 and N3 must be **GREEN** on the unmodified tree — they characterize. N2 **GREEN means the defect
is PRESENT**. All source mutations are **working-tree only**, reverted before commit, with the
reverted diff pasted in the PR body (standing rule **R5**).

**[v2 · PR7] The N1 source arm is a RED-PATH DEVICE ONLY.** Packet E takes no position on the
remediation shape. Validating inside the restore loop would make restore either **partial** or
**refusing**, and choosing between those weakens or reshapes the Backup contract — an owner decision,
not an implementation detail. Forward note for whoever writes that packet: the safety net for a
**non-`sqlite3`** error raised inside that loop is `DatabaseHandler.__exit__`
(`utils/database.py:514-518`), **not** the `except sqlite3.Error` at `program_backup.py:550`.

**[v2 · TS13] Expect wide collateral red while the mutations are live.** The two-site guard reds
`tests/test_weekly_summary_golden.py` and much of `tests/test_effective_sets.py`. That is the
mutation working, not a regression — state it beside the reverted diff in the PR body so the evidence
is not misread.

### 3.5 Owned paths

**Owned**

- `tests/test_program_backup_restore_fuzz.py` (new)
- `docs/testing_phase3/PLANNING.md` (new — this file)
- `docs/test_inventory/TEST_INVENTORY.json` and `.md` — **GENERATED ONLY, never hand-edited**
- **[v2 · A4]** the local handover file, pinned to **`MASTER_HANDOVER.local.md` at the repository
  root** — nowhere else. v1 left it unnamed, which is a live hazard: a gitignored `.md` sitting in a
  globbed surface directory reds `Test Inventory Drift` locally while CI stays green, and
  regenerating **bakes the local file into the committed artifact** (`QUALITY_GATE.md:50`). It must
  **never** sit under `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, or
  `docs/ai_workflow/`. The `.local.md` suffix is what keeps it invisible to the generator.

**NOT owned — do not modify**

`utils/program_backup.py`, `utils/weekly_summary.py`, `utils/effective_sets.py`,
`utils/workout_validation.py`, `utils/exercise_manager.py`, `utils/session_summary.py`, `routes/**`,
`tests/test_program_backup.py`, `e2e/**`, `scss/**`, `static/css/**`, `.github/workflows/**`,
`package.json`, `docs/MASTER_HANDOVER.md`.

### 3.6 Verification gates

**[v2 · A3] Derived, not asserted.** Changed paths are `tests/**` plus `docs/**` only. No row in
`QUALITY_GATE.md`'s routing table matches `tests/**`, and no derivation rule at `:98-104` matches it
either, so the union is **EMPTY** — and `QUALITY_GATE.md:106` reads "Run the union. If the union is
empty, run `/verify-suite`." **Full pytest is mandatory, not a courtesy.**

```
.venv\Scripts\python.exe -m pytest tests/test_program_backup_restore_fuzz.py tests/test_program_backup.py -q
.venv\Scripts\python.exe -m pytest tests/ -q
.venv\Scripts\python.exe scripts/generate_test_inventory.py       then  --check
```

Plus the blocking `flake8` subset, and post-implementation `code-reviewer` **and** `unslop-reviewer`.

**[v2 · TS8] `pyright` baseline diff — expect it to red, and do not re-baseline.** A **new file** is
a **new baseline key**, so every `Optional` subscript in it is net-new against
`docs/ci_cd_phase3/pyright-baseline.json`. The repair is §3.3's `assert row is not None` discipline.
Re-baselining is an **owner decision, not a repair** (`QUALITY_GATE.md:51`).

**[v2 · TS7] Three corrections to v1's gate mapping.**

| # | v1 claim | Corrected |
|---|---|---|
| (a) | full pytest listed among equals | **Mandatory** via the empty-union escalation above. |
| (b) | "E2E / port requirement: ZERO" | True **locally**; **FALSE in CI**. `ci.yml` carries no `paths:` filter, so every required E2E context runs on this PR regardless of the diff. Name the known DB-pollution flake — `e2e/program-backup.spec.ts:79` — which matters precisely because this is a backup packet. |
| (c) | "no Playwright is invoked" | `scripts/generate_test_inventory.py:90-98` **does** shell out to `npx playwright test --list --project=chromium --reporter=json`. Restate as: **Playwright is invoked in list-only mode — no browser, no server, no port.** |
| (d) | `vulture min_confidence=100` listed as a gate | **Not a CI gate** — it appears nowhere under `.github/`. Demoted to local hygiene. The no-new-fixture-names instruction stands on its own merits. |

**Local port requirement: ZERO.** Every node runs on the pytest Flask test client against a per-test
temporary SQLite database. Nothing binds a port and nothing renders in a browser, so the
port-exhaustion, concurrent-worktree and two-platform re-baseline hazards do not apply **to the local
run**. CI's own E2E contexts are unaffected by that and run anyway — see (b).

**[v2 · TS11] The inventory moves in SEVEN places, not two.** Expect exactly:
JSON — `collected_deterministic` **+7**, `deterministic_files` **+1**, `total_files` **+1**, and one
new `pytest.files` entry. Markdown — two `Totals` rows plus one pytest-files row. Anything else is
drift from another worktree; re-fetch and regenerate (R6).

### 3.7 Findings to record — documented, not fixed

**FINDING-1 (N2) — a MULTI-SITE defect** **[v2 · TS2/PR1] [v2-exec]**. `restore_backup()` writes a
non-numeric rep range into `user_selection`, and the next `GET /weekly_summary` returns 500. v1
under-scoped the blast radius to a single line. The remediation surface, **as measured by the arm
battery** (§7) rather than predicted:

| # | Site | Behavior with a restored non-numeric `min_rep_range` | How it was established |
|---|---|---|---|
| 1 | `utils/weekly_summary.py:86` — `(min_rep + max_rep) / 2.0` | `TypeError` → `routes/weekly_summary.py:125` → HTTP 500. This is the site N2 pins. | **Arm B, measured** |
| 2 | `utils/effective_sets.py:192` — `(min_reps + max_reps) / 2.0` via `get_rep_range_factor` | Independent `TypeError` → HTTP 500. Surfaces only once site 1 is guarded. | **Arm B, measured**: the innermost frame moved from `weekly_summary.py`/`_aggregate_weekly_volumes` to `effective_sets.py` |
| 3 | `utils/_fatigue/core.py:124` — `min_reps > 0` via `routes/weekly_summary.py:91` | `TypeError: '>' not supported between instances of 'str' and 'int'` — **SWALLOWED** at `routes/weekly_summary.py:95` into the "Projected fatigue unavailable" empty-state badge. No 500, no user-visible error. | **Arm A, measured**: the log line appears while the route returns 200 |
| 4 | `utils/session_summary.py:100` — `(min_rep + max_rep) / 2.0` | Byte-identical arithmetic off the same `user_selection` join; `routes/session_summary.py:142-151` renders 500 the same way. Not exercised by Packet E. | **Read, not executed** |
| **5** | **`utils/progression_plan.py:312`** — `target_reps = current_reps + 2` | **HTTP 500 on `/progression`** when `max_rep_range` is the poisoned column. Restore empties `workout_log`, so `/progression` takes the plan-defaults branch and `current_reps` is `planned_max_reps`. `_get_progression_status` at `:89/:91` has the same exposure via `decide_progression_target`. | **Read, 2026-08-15** |
| **6** | **`utils/export_service.py:490`** — `export_plan_to_workout_log()` | **One bad row blocks the whole plan→log export** with `VALIDATION_ERROR` naming no routine or exercise. Distinct in kind: a pre-existing whole-batch refusal, not a raise. | **Read, 2026-08-15** |

**[UPDATED 2026-08-15] The site count is SIX.** v2 recorded four. Sites 5 and 6 extend the blast
radius past Analyze into **Progress** and **Log**, which the four-site framing missed entirely.

A seventh surface does **not** raise and is therefore absent from the remediation table above:
`utils/weekly_summary.py:323` (`calculate_isolated_muscles_stats`) does the same average **in SQL**,
where SQLite coerces unparseable text to 0. For the modelled fixture — `min_rep_range` poisoned,
`max_rep_range` still 8 — it returns **4.0** against an intended 7.0. A plausible wrong number
rather than a detectable sentinel, reaching `/weekly_summary`, `/session_summary`, and the Excel
export at `utils/export_service.py:362`. This is the strongest argument against the
"guard the calculation sites" option: it would trade a loud 500 for a quiet miscount.

**RESOLVED at the ingress 2026-08-15.** The owner selected **skip at restore, per row**.
`restore_backup()` applies the canonical `validate_workout_bounds` contract per item and skips
failures. **None of the six sites was modified**, `utils/_fatigue/**` included. Rows already
poisoned by a pre-fix restore still reach them; that residual, and the Min Rep → Max Rep repair
order it requires, are recorded in `docs/LEFTOVERS_BY_PRIORITY.md` §4a.

> **[UPDATED 2026-08-20 — that residual is CLOSED, and two statements above are
> corrected.]** **#394** (`c208745`) shipped the diagnostic and the repair fix
> without touching a calculation file. The full corrections are folded into
> [`LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md) §4a; the two that bear
> on the table above are:
>
> - **Site 5's route is wrong.** `GET /progression` renders fine — it runs only a
>   `DISTINCT exercise, routine` select, measured 200/200. The surface at
>   `utils/progression_plan.py:312` is **`POST /get_exercise_suggestions`**, and
>   only when `max_rep_range` is the poisoned column.
> - **The repair order was never "Min Rep → Max Rep".** The measured 2×2 matrix
>   was symmetric — the rule was "edit the *poisoned* column first" — and #394
>   removed the constraint entirely, so either column may now be repaired first.
>
> **None of the six sites is modified and none of this changes §3.7's argument.**
> The sites still raise, the "guard the calculation sites" option is still
> rejected, and site 7's silent 4.0 is still unfixed — with the added measured
> qualifier that it is **unreachable through the shipped UI**, because an
> unfiltered calculation raises first on all three surfaces named above. That
> qualifier matters here: a later owner could otherwise authorize a **Large**
> `utils/weekly_summary.py` council against a path the UI cannot reach.

**A remediation packet that guards only site 1 ships a fix that does not fix the 500** — Arm B
measured exactly that, with the status still 500 and only the frame moved. **Sites 1 and 2 must BOTH
be guarded to reach 200** (Arm A, measured). **Site 3 is the quieter hazard**: it degrades silently
today and will keep degrading silently after sites 1 and 2 are fixed.

**[v2-exec] One framing correction.** Plan v2's table already carried
four rows — PR1 named the fatigue path by reading. Execution did not add a site; it changed the
*evidence class* of two of them. Site 2's independence and site 3's exact exception, swallow point
and 200-while-logging are now **measured**, where v2 had inference. Site 4 remains read-only.

Documented only; remediation is a separate owner-gated packet with migration notes.

**FINDING-2 (out of scope) — severity was wrong in BOTH directions** **[v2 · PR6]**.

- **Less severe than v1 implied**: `sets='abc'` is **not UI-reachable**.
  `templates/workout_plan.html:92` is `input type="number"`;
  `static/js/modules/workout-plan-table.js:526` sets `input.type = 'number'`; `:571` refuses empty.
  Reaching it needs a hand-crafted request against a single-user localhost app.
- **More severe than v1 implied**: out-of-range **numerics** are **fully UI-reachable** —
  `workout-plan-table.js:534-554` treats min/max as advisory and nothing on the inline-edit path
  calls `checkValidity()` — the only caller is the form-submit handler at `ui-handlers.js:344`,
  which the inline editor never reaches.
  And `rpe=99` yields `int(round(10 - 99)) = -89`, clamped to `0`, bucket `(0,1)` → **`1.0`, FULL
  effort credit, silently**, for any row with a `NULL` rir.

Still deferred. No test and no fix here; it needs its own Gate 0.

**FINDING-3 (new) — restore is destructive to `workout_log`** **[v2 · PR8]**. `restore_backup`
deletes `workout_log` **and** `user_selection` (`:445-446`) before inserting, while `create_backup`
snapshots **only** `user_selection` (`:188-192`). Logged sessions are therefore unrecoverable by any
backup. This is **correctly disclosed in the UI** (`static/js/modules/backup-center.js:674`), so it is
not a defect — it is recorded so that a remediation packet does not reason about restore as though it
were non-destructive. Documented, not tested.

## 4. Standing rules

Carried forward from [`docs/testing_phase2/PLANNING.md`](../testing_phase2/PLANNING.md) §4.

- **R5 — no committed tracked-file mutation.** Mutate-then-revert; the reverted diff goes in the PR
  body. Every arm in §3.4 and §6.4 is working-tree only. **[v2 · TS13]** Annotate the collateral red.
- **R6 — serialization.** These packets regenerate `docs/test_inventory/`, which sits behind the
  required `Test Inventory Drift` context. Re-fetch `origin/main` **immediately** before
  regenerating. Never hand-merge the inventory. **[v2 · A4]** And never regenerate while an
  untracked or gitignored `.md` sits in a globbed surface directory — see §3.5.
- **R7 — Packet-E note on R6.** **[v2-exec] Packet D's status changed twice while Packet E was in
  flight, and R6's re-fetch step is what caught both.** D was **blocked** by owner decision (PR #367,
  `a64ea76` — *"Packet D is marked blocked, with the evidence"*), which made the D-vs-E serialization
  concern moot. It then **shipped**: PR **#366** merged as `f627161`, now this packet's base. The
  serialization concern was real after all — just resolved by D landing first rather than by
  sequencing. Other concurrent worktrees may still move the inventory, so R6 stands unchanged.

## 5. Execution log

| Packet | Result |
|---|---|
| **E** | Plan v2 recorded 2026-08-14; council closed, Gate 1 **CLOSED** (§6.5). **Implemented and verified the same day — see §7.** 7 nodes, all green. Red-path arms: **10/12 on the first battery, 12/12 on the second** — both misses were test-side vacuity holes the arms exposed and the test was corrected (§7.1). No production file touched. Awaiting Gate 2. |

## 6. Council review

Ran 2026-08-14 via `/council-plan`, three reviewers in parallel, against the worktree at
`origin/main` @ `a64ea76`. **All three returned "Needs revision."** Every accepted fix lands inside
§3.5's owned paths; both `test-strategist` and `product-risk-reviewer` explicitly stated that no owner
escalation is required.

### 6.1 Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a02329cbb9ae85e61` | Author of §1–§5. |
| `product-manager` — response matrix + Plan v2 | `a02329cbb9ae85e61` | Same agent. Author of §6.3 and §6.4. |
| `architecture-reviewer` | `a3679161790209dfb` | Step 2 reviewer. |
| `test-strategist` | `aa9173d7842cb8cf0` | Step 2 reviewer. |
| `product-risk-reviewer` | `ae5c81e656f6cb6a1` | Step 2 reviewer. |

**Same product-manager resumed for the matrix + Plan v2?** **yes** — `a02329cbb9ae85e61` for all
three writes. Every ID above was supplied by the manager and is stamped verbatim; none was inferred.

**Evidence gap**: `none` for continuity.

### 6.2 Reviewer findings

The manager relayed each reviewer's findings as an itemized list with per-finding IDs and severities
and its own synthesized dispositions. Verbatim reviewer transcripts were not relayed to this agent,
so none are pasted here rather than reconstructed. **§6.3 carries every finding, with its reviewer's
ID and severity as supplied — 32 findings, none dropped, none merged.**

### 6.3 Response matrix

Severity as supplied. Disposition: **A** = accepted, **A-M** = accepted-modified, **D** = declined.
Nothing was declined and nothing was deferred.

| ID | Sev | Reviewer | Finding | Disp. | Change in v2 |
|---|---|---|---|---|---|
| A1 | MAJOR | arch | N3's `12.5` assertion is vacuous — `avg_reps` is a local at `effective_sets.py:192`, never returned; `get_rep_range_factor(20,5)` falls through to `DEFAULT_MULTIPLIER` `1.0`, identical to `get_rep_range_factor(None,None)` | A | N3 oracle replaced end-to-end — §6.4 |
| A2 | MAJOR | arch | N3 had no restore-response assertion, so a rolled-back restore passes it vacuously; also flags a real `UNIQUE`-collision route (`db_initializer.py:196` vs none on `program_backup_items`) | A | N3 gains N1's ordered guard; its items vary a non-bounded column — §3.1, §2.5 |
| A3 | MINOR | arch | §3.6's gate list was asserted, not derived | A | Derivation written out: `tests/**` + `docs/**` match no row and no rule, union EMPTY, `QUALITY_GATE.md:106` escalates — §3.6 |
| A4 | MAJOR | arch | The unnamed gitignored handover file could red `Test Inventory Drift` and bake itself into the committed artifact | A | Pinned to `MASTER_HANDOVER.local.md` at repo root, with the four forbidden directories named — §3.5, R6 |
| A5 | MINOR | arch | N3 should use the proven JSON branch; N2 keeps the HTML error branch, whose byte markers exist at `tests/test_error_page_contract.py:79-82` | A | §3.1 N2 oracle cites the markers; N3 asserts through `calculate_weekly_summary` — §6.4 |
| A6 | MINOR | arch | The XHR trap has THREE triggers — `X-Requested-With` **and** `'application/json'` in `Accept` (`utils/errors.py:52-63`) | A | §2.3 restated as both; N2 must carry neither |
| A7 | MINOR | arch | `pyright` checks `tests/**`; `fetch_one` returns `Optional`, so subscripting is `reportOptionalSubscript` | A | Merged with TS8 — §3.3, §3.6 |
| A8 | MINOR | arch | N1 entrenches behavior a future fix packet must delete, and the warning lived only in the plan | A | Warning moves into the test **module docstring** — §3.2 |
| A9 | NIT | arch | Positive: the fixture builds its header through production `create_backup()`, so no `schema_version` literal is hard-coded and a future D6 packet cannot silently reroute these nodes | A | Recorded as a **constraint**: never hand-write the header `INSERT` — §3.3 step 1 |
| TS1 | BLOCKER | test-strat | Same as A1, plus: §3.1's prescribed fix ("pin 12.5 directly") is **not implementable** | A-M | Replaced with the end-to-end oracle — §6.4 |
| TS2 | BLOCKER | test-strat | N2's source mutation is vacuous — guarding only `weekly_summary.py:86` still yields 500, because execution continues to `calculate_effective_sets` → `effective_sets.py:192`, the same arithmetic. C3's failure mode on a new axis | A | Two arms now required (§6.4); FINDING-1 upgraded to MULTI-SITE — §3.7 |
| TS3 | MAJOR | test-strat | N3's surviving clamp assertion duplicates `tests/test_effective_sets.py:120-125` | A | N3's value now comes from the restored-row arithmetic, not the clamp alone — §6.4 |
| TS4 | MAJOR | test-strat | N1 step (b) is vacuous — `VALIDATION_ERROR` has three producers (`routes/workout_plan.py:85`, `:95`, `:129-140`) | A | Fully valid payload, exactly one malformed field, assert the EXACT message — §3.1 |
| TS5 | MAJOR | test-strat | `item_count` is the wrong precondition column — `restore_backup` selects it at `:411-415` but uses only `backup['name']` at `:420`; items come from `:423-428` | A | Replaced by `SELECT COUNT(*) FROM program_backup_items == 1` plus fixture `UPDATE` `rowcount == 1` — §3.1, §3.3 |
| TS6 | MAJOR | test-strat | The "rival-branch arm" is misnamed — Packet E changes zero production files, so main is byte-identical to the branch | A | Relabelled **baseline arm**; anti-"fix" protection moves into the test file — module docstring, node docstring, and `known_defect` in the node name — §3.2, §3.4 |
| TS7 | MAJOR | test-strat | Gate mapping wrong in four places — empty-union escalation, "E2E ZERO" false in CI, the inventory script does invoke Playwright, `vulture` is not a CI gate | A | All four corrected in the §3.6 table; `e2e/program-backup.spec.ts:79` named as the known DB-pollution flake |
| TS8 | MAJOR | test-strat | `pyright` baseline diff will red — a NEW file is a NEW baseline key and every `fetch_one(...)['x']` is net-new `reportOptionalSubscript` | A | `row = fetch_one(...)` / `assert row is not None` / `row['col']` mandated throughout; **never re-baseline** (`QUALITY_GATE.md:51`) — §3.3, §3.6 |
| TS9 | MINOR | test-strat | N1 mutation arm (1) under-specified — a mutant that computes `bounds_error` and ignores it stays green | A | SKIP variant specified, mirroring the catalog skip at `:455-460` — §3.4 |
| TS10 | MINOR | test-strat | N3's fixture shape ambiguous — `exercise_factory` defaults to Chest/Triceps/Shoulders (`conftest.py:325-327`) and would split totals across three muscles | A | ONE item, ONE primary muscle, `secondary` and `tertiary` explicitly `None` — §3.1 |
| TS11 | MINOR | test-strat | Inventory moves in SEVEN places, not two (four JSON, three Markdown) | A | Exact expected movement recorded — §3.6 |
| TS12 | NIT | test-strat | §2.4 row 4 contradicts row 2 by using `('8' + 12)` as evidence after ruling `'8'` out as a fixture value | A | Row 4 now reads `('abc' + 12)` — §2.4 |
| TS13 | NIT | test-strat | Expect wide collateral red while mutations are live — the two-site guard reds `test_weekly_summary_golden.py` and much of `test_effective_sets.py` | A | Stated in §3.4 and R5 so the reverted-diff evidence is not mistaken for a regression |
| PR1 | MAJOR | prod-risk | FINDING-1 under-scopes the blast radius — `session_summary.py:99-100` carries byte-identical arithmetic off the same join and `routes/session_summary.py:142-151` renders 500 the same way; `_fatigue/core.py:124` raises but `routes/weekly_summary.py:90-96` degrades it to a badge | A | FINDING-1 names every site in a table; a one-site fix "ships a fix that does not fix the 500" — §3.7 |
| PR2 | MAJOR | prod-risk | N3 pinned the literal `0.55`, a product-tunable whose own comments mark it a live judgement call | A | Clamp asserted **relationally**: `get_effort_factor(rir=99) == get_effort_factor(rir=MAX_RIR)` — §6.4 |
| PR3 | MAJOR | prod-risk | The threat model leans on its unevidenced leg (legacy builds) and never joins the live one | A | New §2.6: malformed persisted rows are reachable **today** via `routes/workout_plan.py:386` + `create_backup()` `:188-192`; the legacy leg is downgraded to a stated assumption |
| PR4 | MAJOR | prod-risk | The fixture's direct `UPDATE` needs an explicit non-claim | A | Reviewer's exact wording quoted in §3.3 **and** required in the test module docstring |
| PR5 | MAJOR | prod-risk | "absorbs" overstates safety — 200 is not correctness | A | N3 renamed `test_weekly_summary_returns_200_without_validating_restored_out_of_range_numerics`; the no-user-visible-signal consequence is stated — §3.1 |
| PR6 | MINOR | prod-risk | FINDING-2's severity is wrong in BOTH directions | A | Both halves recorded — `sets='abc'` is not UI-reachable; out-of-range numerics are, and `rpe=99` silently yields FULL effort credit. Deferral stands — §3.7 |
| PR7 | MINOR | prod-risk | §3.4's N1 arm prejudges a remediation that would weaken the Backup contract | A | Labelled RED-PATH DEVICE ONLY, with the partial-or-refusing owner decision and the `__exit__`-not-`except` forward note — §3.4 |
| PR8 | MINOR | prod-risk | Restore's destruction of `workout_log` is unmentioned | A | New FINDING-3, documented not tested — §3.7 |
| PR9 | MINOR | prod-risk | Same as A1/TS1, plus: restate the product fact as a PROPERTY and label it accidental behavior | A | "Inverted range → midpoint, symmetrically", labelled **ACCIDENTAL BEHAVIOR, not designed contract** — §3.1 |
| PR10 | NIT | prod-risk | `'8-12'` is a more credible legacy value than `'abc'` | A-M | Recorded as the more credible legacy story; `'abc'` **kept** as the fixture value — both are non-numeric and detonate identically, and `'abc'` cannot be misread as coercible — §3.3 |

### 6.4 Plan v2 — the binding design

Only the parts that changed. §1–§5 above carry the rest, amended in place.

#### N3's oracle — replacing the impossible "pin 12.5 directly"

Restore **ONE** item: `sets=3`, `min_rep_range=20`, `max_rep_range=5`, `rir=99`, `weight=99999.0`,
one primary muscle only (TS10). Then call `calculate_weekly_summary()` and assert on that muscle:

| Assertion | Value | What it pins |
|---|---|---|
| `raw_total_reps` | `== 37.5` | `avg_reps == 12.5` reached end-to-end (`3.0 × 12.5`). Rules out min-only (`60.0`), max-only (`15.0`), and row-dropped (`0.0`). |
| `raw_total_volume` | `== 3749962.5` | `weight=99999.0` survived restore **and** entered the arithmetic. |
| `effective_weekly_sets` | `== round(3 * get_effort_factor(rir=MAX_RIR) * get_rep_range_factor(20, 5), 2)` | Relational, so a legitimate bucket retune does not red it (PR2). **[v2-exec] But the `get_rep_range_factor` term is SELF-CANCELLING** — it appears on both sides, so it pins nothing about that function. See below. |
| clamp | `get_effort_factor(rir=99) == get_effort_factor(rir=MAX_RIR)` | The clamp at `effective_sets.py:158`, relationally rather than as the literal `0.55`. |
| **[v2-exec] symmetry** | `get_rep_range_factor(20, 5) == get_rep_range_factor(5, 20)` | **Added during execution (§7.1, M8).** The rep-range averaging, pinned as a **property** rather than a value — the only form that is not self-cancelling. Without this row the `effective_sets.py:192` mutation stays green. |

**DO NOT assert `total_reps`.** `1.65 × 12.5` lands on a float-representation boundary
(`20.625000000000004`), and `round()`'s half-to-even makes it a live footgun. Stated explicitly so a
later agent does not "complete" the oracle by adding it.

Verified property of the relational clamp assertion: deleting `effective_sets.py:158` drops the left
side to `1.0` while the right side stays, so the mutation still reds — the assertion survives a
retune without going vacuous.

#### The two averaging sites now have DISTINCT load-bearing mutations

| Mutation | Effect on N3 |
|---|---|
| `weekly_summary.py:86` — `(min_rep + max_rep) / 2.0` → `max_rep` | `raw_total_reps` `37.5` → `15.0`, **reds**. Measured, holds as predicted. |
| `effective_sets.py:192` — `(min_reps + max_reps) / 2.0` → `max_reps` | **[v2-exec] PREDICTION WRONG.** Predicted `effective_weekly_sets` `1.65` → `1.4`. Measured: it does **not** move, because `expected_effective` recomputes `get_rep_range_factor(20, 5)` at assertion time and both sides shift together. The node reds via the **symmetry** assertion added above. |

One mutation per site, each pinned by a different assertion. **[v2-exec] Only the first was pinned by
a moving number; the second needs a property.** That distinction is the packet's main lesson — §7.2.

#### N2's two arms

**Arm A** — guard **BOTH** `weekly_summary.py:86` **AND** `effective_sets.py:192` → the route returns
**200** and N2 reds. This must be **EMPIRICALLY CONFIRMED to produce 200, not asserted**. If a third
site detonates, guard it too and **record the count** — the number of sites is itself evidence for
FINDING-1.

**Arm B** — guard `weekly_summary.py:86` **ALONE** → the status stays **500**, but N2 reds anyway,
because the innermost `TypeError` frame moves from `_aggregate_weekly_volumes` to
`get_rep_range_factor`. **This is the arm that proves N2's frame oracle is load-bearing rather than
decorative.** Arm A alone would leave a status-only oracle indistinguishable from a frame-aware one.

#### Direction of green

| Node | Green on the unmodified tree means |
|---|---|
| N1 | the restore path applies no bounds validation — characterization holds |
| N3 | the out-of-range numerics propagate untouched and the route still returns 200 — characterization holds |
| **N2** | **the defect is PRESENT** — inverted meaning; the day N2 reds is the day FINDING-1 is fixed |

### 6.5 Sign-off — GATE 1

- [x] Every finding has a disposition — 32 of 32 in §6.3. None declined, none deferred.
- [x] Agent provenance complete — both `product-manager` writes are `a02329cbb9ae85e61`,
      same-PM-resumed **yes**, three reviewer IDs stamped verbatim, evidence gap `none`.
- [x] **Gate 1 self-check passed.** Plan v2 stays inside §3's scope and §3.5's owned paths, adds no
      production file, and every accepted fix is a test-file, plan-document or generated-artifact
      change. `test-strategist` and `product-risk-reviewer` each explicitly stated that no owner
      escalation is required.
- [x] **GATE 1 CLOSED** 2026-08-14 under the owner's conditional approval recorded in the scope
      blockquote. Implementation proceeds without returning to the owner.
- [x] Implementation complete — see §7. Diff-time reviewers run there.

**Escalation triggers that re-open the owner's gate** — any one of these stops work and returns to the
owner: a proposed change to a production file; a remediation of FINDING-1, FINDING-2 or FINDING-3
inside this packet; a `pyright` re-baseline; or a third detonation site found by Arm A that cannot be
handled as a working-tree mutation.

**None of the four triggers fired.** The additional site Arm A surfaced (site 3, the fatigue badge) is
swallowed rather than fatal, so guarding sites 1 and 2 was sufficient to reach 200 as a working-tree
mutation. No production file was changed, no finding was remediated, and the `pyright` baseline was
not touched.

## 7. Execution record — 2026-08-14

Base `origin/main` **`f627161`** (#366). `origin/main` moved **twice** while this packet was in
flight — `a64ea76` → `9be1a3f` (#368) → `f627161` (#366, **Packet D**) — and the branch was
fast-forwarded before each inventory regeneration, exactly as R6 requires. The second move mattered:
Packet D regenerates the same artifact, so the first regeneration was discarded and redone rather
than merged.

**A toolchain repair was needed, and it is worth recording.** Packet D added `@axe-core/playwright`
to `package.json`. This worktree's `node_modules` was a **junction to the main checkout's**, and the
main checkout sits at an older commit whose `package.json` does not declare that dependency — so
`npx playwright test --list` failed with `Cannot find module '@axe-core/playwright'`, and
`generate_test_inventory.py` hard-exits when that happens (`:72-79`). `npm ci` **in main** — the
usual repair — would **not** have fixed it, because main's `package.json` predates the dependency,
and it would have mutated shared state other worktrees rely on. The correct repair was to give this
worktree its **own** `node_modules`: unlink the junction **non-recursively**
(`[System.IO.Directory]::Delete(path, $false)` — a recursive delete would have destroyed the main
checkout's tree through the link) and run `npm ci` inside the worktree. Main's 179 packages were
verified intact afterwards.

### 7.1 The arm battery — first pass found two vacuity holes in the test

**The first battery was 10 of 12.** Both failures were the battery working as intended: each mutation
was sound and exposed a real hole in the test as written.

| Arm | Predicted | First pass | What it exposed |
|---|---|---|---|
| **M3** — fixture seeds an in-bounds weight | RED | **GREEN** | The fixture value and the `/add_exercise` payload value were separate elements of the parametrize tuple. Seeding a valid weight left the payload still carrying the invalid one, so the node passed while no longer asserting *the same value on both paths* — the node's entire premise. |
| **M8** — `effective_sets.py:192` averaging → `max_reps` | RED | **GREEN** | `expected_effective` called `get_rep_range_factor(20, 5)` **at assertion time**, so mutating that function moved **both sides of the equality together** and cancelled out. |

**Fixes, both inside the test file.** M3: `updates` became the single source of truth, layered onto
the payload with `payload.update(updates)`; the duplicated payload column was deleted from all five
cases. M8: added `get_rep_range_factor(20, 5) == get_rep_range_factor(5, 20)` — PR9's symmetry
property, which is not self-referential, so replacing the average with either endpoint breaks the
equality while leaving `expected_effective` untouched.

**Second battery: 12 of 12 behave as predicted.**

| Arm | Kind | Mutation | Node | Result |
|---|---|---|---|---|
| BASE | — | unmodified tree | N1 / N2 / N3 | **GREEN / GREEN / GREEN** as predicted |
| M1 | source | restore validates and **skips** out-of-bounds items | N1 | RED (5 failed) |
| M2a | test | expected `400` → `200` | N1 | RED |
| M2b | test | reverted | N1 | GREEN — both directions |
| M3 | fixture | seeds an in-bounds weight | N1[weight_above_max] | RED |
| M4 | source | guard **both** averaging sites | N2 | RED — measured `assert 200 == 500` |
| M5 | source | guard `weekly_summary.py` **alone** | N2 | RED — measured `assert 'effective_sets.py' == 'weekly_summary.py'`, status still 500 |
| M6 | source | delete the RIR clamp (`effective_sets.py:158`) | N3 | RED |
| M7 | source | `weekly_summary.py:86` averaging → `max_rep` | N3 | RED (`raw_total_reps` 37.5 → 15.0) |
| M8 | source | `effective_sets.py:192` averaging → `max_reps` | N3 | RED via the new symmetry assertion |

M4 supplies the **empirical** confirmation Plan v2 demanded rather than assumed: with both sites
guarded the route genuinely reaches 200. M5 is the arm that proves N2's frame oracle is load-bearing
— status alone cannot tell the two sites apart.

Every mutation was working-tree only. `git status --porcelain` after the battery showed only the two
intended untracked additions; the reverted diffs belong in the PR body per **R5**.

### 7.2 The lesson, added to the standing rules

**A relational assertion is self-cancelling whenever the function under mutation appears on both
sides.** Use the relational form to avoid pinning a tunable **value** (PR2's concern — the effort
factor). Use a **property** — symmetry, invariance — to pin **logic**. M8 is the worked example: the
same relational form that correctly protects the effort factor silently disarmed the rep-range factor.

This is the **C3 vacuity class recurring for the third time in one packet**: first the rollback
mutation that `__exit__` made green, then the single-site N2 guard that a second detonation site made
green, now the self-referential factor. Each time it arrived on a new axis and each time only
execution caught it. Reading the mutation is not evidence that the mutation reds.

### 7.3 Gate results

> **RE-RUN AT INTEGRATION, 2026-08-15, on `94f0d8c`.** The table below was measured at `f627161`
> and **its numbers do not certify this base** — six commits landed in between, including #373
> (D6 / ADR-008), #374/#375 (release pipeline R1) and #376 (status reconciliation). Every blocking
> gate was re-run here; these figures supersede the table for the shipped commit:
>
> | Gate | Result at `94f0d8c` |
> |---|---|
> | targeted (`..._restore_fuzz.py` + `test_program_backup.py`) | **47 passed** |
> | full `pytest tests/ -q` | **2967 passed, 2 skipped** (was 2866/2 at `f627161`) |
> | **FINDING-1 still reproduces** | yes — the known-defect node has **not** been overtaken by an intervening fix |
> | `flake8` (exact CI select + exclude list) | **0**, exit 0 |
> | `pyright_baseline_diff.py` | **PASS — 0 net-new** (baseline 132, current 132) |
> | inventory delta | exactly this file at **7** nodes (`2640 → 2647`, `121 → 122` deterministic files); nothing else moved |
>
> Deliberately **not** re-run: the `2538 + 322` cross-check recorded in §7.4, which belongs to the
> `f627161` measurement and is left as the historical record rather than restated.

| Gate | Result |
|---|---|
| targeted pytest (new file + `tests/test_program_backup.py`) | **43 passed** |
| full `pytest tests/ -q` | **2866 passed, 2 skipped** (on `f627161`; it was 2858/2 on `9be1a3f` before Packet D landed) |
| `generate_test_inventory.py --check` **before** regen | exit 1, drift = exactly `tests/test_program_backup_restore_fuzz.py` at **7** |
| collected node count | **7** (`--collect-only`), matching the inventory entry |
| `generate_test_inventory.py` then `--check` | **up to date**, exit 0 |
| inventory delta | exactly the seven predicted places (four JSON, three Markdown); Playwright **647/33** and hard waits 82 **unchanged by this packet** — the Playwright rise is Packet D's, already committed at `f627161` |
| `flake8` (exact CI invocation) | **0**, exit 0 |
| `pyright` baseline diff (blocking) | **PASS — 0 net-new** (baseline 132, current 132) |
| `vulture --min-confidence 100` | 5 findings repo-wide, **none** from the new file |

**A local `flake8 .` without `--exclude` is meaningless here** and must not be reported as a result:
the worktree's `.venv` is a junction, so an unexcluded run reports **1071** findings from
`site-packages` that CI never sees. Use the workflow's own exclude list.

Not run, and correctly so: CSS builds, Playwright execution, a Flask server, visual baselines, any
port-bound workflow. Playwright is invoked by the inventory generator in list-only mode only.

### 7.4 Diff-time review

`code-reviewer` (`ac487ed852ace3afd`) and `unslop-reviewer` (`ab0b875eb5119141f`), run in parallel
against the staged diff.

**`code-reviewer`: no BLOCKER, no MAJOR — "the test file is clean."** It verified independently that
no value ever reaches SQL by interpolation (only column names, all from module-level literals, all six
call sites checked); that both DB accesses are context-managed and cannot strand a Windows handle;
that all four asserted envelope shapes match `utils/errors.py`; and that the N3 arithmetic is exactly
representable so `==` is safe. Its cross-check is worth keeping: inventory `collected_deterministic`
2538 + the 322 Windows-host nodes of the one environment-dependent file = 2860 = 2858 passed + 2
skipped, so §7.3's suite total is self-consistent with the artifact.

**Both reviewers independently raised the same top finding**, and it was the one worth having: §6.4
and §3.4 still prescribed the self-cancelling `effective_weekly_sets` assertion as "the binding
design", so anyone re-implementing from §6.4 would have reproduced the exact hole M8 exposed. Fixed by
the `[v2-exec]` corrections now carried in both sections, plus the reading note at the head of this
document establishing **§7 as the authority over §6.4**.

Accepted and applied, beyond the above: N2's name corrected in §3.1 (it contradicted §3.2's own
`known_defect` grep requirement); "one class" and "seven parametrized nodes" corrected to what was
built; the multi-item N3 description replaced with the single-item shape actually implemented; the
stale `a64ea76` base in the scope blockquote; **SIX → SEVEN** inventory movements (four JSON, three
Markdown — the enumeration was right, the numeral was wrong); **TWO → THREE** XHR triggers
(`/api/` prefix, inside the range the passage already cited); `checkValidity()` narrowed to the
inline-edit path; the §3.1 SUPERSEDED blockquote cut to the pointer the document's own convention
promises; two self-congratulatory clauses cut; and in the test file, a docstring that restated its
own asserts, an unused `backup_name` parameter, a comment restating the next line, and an incomplete
`VALIDATION_ERROR` producer list — the duplicate-row branch at `routes/workout_plan.py:121-128` is
the one this payload would actually hit, which is what makes the exact-message assertion load-bearing.

**One finding DECLINED, on evidence.** `unslop-reviewer` rated R7 MEDIUM, arguing that `a64ea76` is
this packet's base rather than a Packet-D ruling and that four other documents record Packet D as
merely queued. `git log -1 a64ea76` reads
*"docs(a11y): record the X1/X2/X6 owner decisions and **block Packet D** (#367)"*, and the body states
"Packet D is marked blocked, with the evidence … that choice belongs before D starts." The commit is
both this packet's original base **and** the Packet-D ruling; the four documents cited predate it.
R7 stands as written. Recorded because the reviewer's reasoning was sound and only its premise was
stale — the kind of finding that is right to raise and wrong to accept.

Declined by design, not by disagreement: `unslop-reviewer`'s suggestion to inline
`_valid_add_exercise_payload` (single-caller). The name is what documents the "fully in-bounds
baseline, exactly one field malformed" contract that TS4 exists to enforce; inlining it would bury
that contract in a literal.
