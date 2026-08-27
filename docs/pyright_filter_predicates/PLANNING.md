# Pyright burn-down Packet P1 — `utils/filter_predicates.py` `reportArgumentType`

*Continuous track — pyright baseline burn-down ([`docs/REFACTOR_PLAN.md:1548`](../REFACTOR_PLAN.md)
§"Continuous track — pyright baseline burn-down"). One file, one tightly coupled
diagnostic pair, structure-only.*

**Status: Gate 1 SIGNED 2026-08-27 (Candidate Q), implementation complete.** §0–§11
were written before the signature and keep their pre-signature findings and reasoning.
Where the signature or the implementation falsified a specific sentence in them — §2's
planning-time rows, §5's and §6's framing, §6.4's three then-open decisions, §7's scope
table, §8's future-tense obligations, §9's column header, §11's ownership claim — that
sentence was corrected in place and says so. **No measurement was revised.** §12 carries
the owner's approval and the three resolved decisions; **§14 carries the measured
results, including two mutation survivors and one deviation from the signed code
block.** No test file, no `docs/test_inventory/**` artifact and no schema was
modified.

Branch `wt/pyright-filter-predicates-gate1`, worktree
`D:\development\Hypertrophy-Toolbox-v3-main-pyright-filter-predicates-gate1`, created
with `scripts/new-worktree.ps1 -Task pyright-filter-predicates-gate1 -Seed empty` and
fast-forwarded to `origin/main` **before any measurement** (§2).

Planning size: **Medium** ([`docs/ai_workflow/QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)
§Plan-stage routing) — bounded, single file, known contracts, no schema, API or
calculation surface. Gate 0 is waived: requirements, non-goals and prohibited
techniques were fully specified by the owner brief that opened this packet.

---

## 0. Objective and non-goals

### Objective

Eliminate exactly the **two** existing `reportArgumentType` diagnostics in
`utils/filter_predicates.py` — both on line 124, both `Literal[0]` passed to
`dict.__getitem__` — without changing runtime behavior, SQL, filtering semantics,
exception behavior, logging, database schema, or any public function signature.

### Non-goals

- **No** SQL or query-construction change. `build_filter_query()` is not touched.
- **No** filtering-semantics change: the field whitelist, the LIKE/exact split, the
  `advanced_isolated_muscles` EXISTS subquery and the parameterization all stay
  byte-identical. The SQL-injection tests at
  [`tests/test_filter_predicates.py:102-134`](../../tests/test_filter_predicates.py#L102-L134)
  cover a surface this packet does not enter.
- **No** exception-behavior change: the `try` / `except Exception` /
  `logger.exception("Error filtering exercises: %s", e)` / `return []` shape is
  preserved exactly, including which statements sit inside the `try`.
- **No** logging change — same logger, same message template, same call site.
- **No** database-schema change; no `utils/database.py` edit. In particular
  `DatabaseHandler.fetch_all()`'s declared return type is **not** widened (§3.4).
- **No** public-signature change. `filter_exercises`, `get_exercises`,
  `build_filter_query`, `validate_filter_field`, `sanitize_filters` and the three
  module-level backward-compat wrappers keep their exact signatures.
- **No suppression**: no `Any`-typed *value*, no `cast`, no `# type: ignore`, no
  assertion added merely to silence Pyright, no rule disablement, no baseline-only
  edit. (`Any` as a *type argument* is discussed honestly in §6.4 — it already crosses
  this boundary today from `fetch_all`'s own declared type.)
- **No opportunistic fixes.** The neighbouring diagnostics in
  `utils/exercise_manager.py` (1 × `reportOptionalMemberAccess`) and
  `tests/test_exercise_manager.py` (7 × `reportOptionalSubscript`) are recorded in
  §1.3 and deliberately left allowlisted.
- **No** deletion of the tuple-result compatibility path, and no deletion of the
  dict-result path. Both are live contracts under test (§4).

---

## 1. Live base, tool version, and reproduced diagnostic identity

### 1.1 Base commit

`origin/main` was fetched and read live rather than assumed; the main checkout's HEAD
was **stale** (`5111a7f`) and `scripts/new-worktree.ps1` forked from it, so the
worktree was fast-forwarded before anything was measured.

| Fact | Value |
|---|---|
| `git rev-parse origin/main` | **`b733c14f8e76c7f85b1d9dcc75acd8bca8321524`** |
| Subject | `chore(deps): bump sass from 1.102.0 to 1.103.1 (#416)` |
| Author date | `2026-08-27 02:22:29 +0300` |
| Worktree HEAD after `git merge --ff-only origin/main` | `b733c14…` — **equal to `origin/main`**, verified before measuring |
| Worktree `git status --porcelain` at measurement time | empty |

Dependabot PR **#416** is therefore already **merged** at this base; the triage lane
named in the brief has landed. See §11.

### 1.2 Pyright version — discovered, not assumed

`.github/workflows/ci.yml:903` runs `npx pyright@1.1.410 --outputjson`, and
`ci.yml:855` records that the committed baseline was generated under **1.1.410**.
Every measurement in this packet used `npx pyright@1.1.410` under the committed
[`pyrightconfig.json`](../../pyrightconfig.json) (`pythonVersion 3.14`,
`pythonPlatform Windows`, `venvPath "."`, `venv ".venv"`). The worktree's `.venv` is a
junction to the main checkout's, used read-only; nothing was installed or upgraded.

```
npx pyright@1.1.410 --outputjson
→ version 1.1.410, filesAnalyzed 239, errorCount 132, warningCount 0, informationCount 0
```

### 1.3 Reproduced diagnostic identity

| file | severity | rule | message | 1-based line:col | baseline count |
|---|---|---|---|---|---|
| `utils/filter_predicates.py` | `error` | `reportArgumentType` | `Argument of type "Literal[0]" cannot be assigned to parameter "key" of type "str" in function "__getitem__"` / `  "Literal[0]" is not assignable to "str"` | **124:29–124:35** and **124:58–124:64** | **2** |

Both instances are on the **same source line**,
[`utils/filter_predicates.py:124`](../../utils/filter_predicates.py#L124):

```python
                    return [row[0] for row in results if row[0]]
```

— the value expression `row[0]` at col 29 and the comprehension guard `row[0]` at
col 58. The baseline keys on the 4-tuple `(file, severity, rule, message)`
(`scripts/pyright_baseline_diff.py:86` `_key_to_record`), so the two instances
collapse into **one record with `count: 2`**
([`docs/ci_cd_phase3/pyright-baseline.json:240-246`](../ci_cd_phase3/pyright-baseline.json)).

Gate reproduction against the committed snapshot, **before** any edit:

```
python scripts/pyright_baseline_diff.py \
    --current artifacts/pyright_before.json \
    --baseline docs/ci_cd_phase3/pyright-baseline.json
→ pyright baseline gate: PASS — 0 net-new diagnostics (baseline 132, current 132).   exit 0
```

Committed baseline `_meta`, re-derived rather than assumed: **132 `total_diagnostics`
/ 42 `distinct_keys`**, and the 42 records sum to exactly 132. The tree therefore
starts clean and any later delta is attributable to this packet.

**Rule-family census at this base** (re-derived from the committed baseline):
`reportOptionalSubscript` 72, **`reportArgumentType` 50**, `reportReturnType` 2,
`reportOperatorIssue` 2, `reportAttributeAccessIssue` 2, `reportCallIssue` 2,
`reportOptionalMemberAccess` 1, `reportOptionalOperand` 1.

**This packet does not eliminate the `reportArgumentType` family and does not claim
to.** The family goes **50 → 48** repo-wide. The 19 `reportArgumentType` records sum
to 50; removing this one leaves **18 records across 9 files** — `routes/workout_plan.py`,
`utils/database.py`, `utils/export_utils.py`, `utils/fatigue_context.py`,
`utils/profile_estimator.py`, `utils/strength_calibration.py` and three test files
(`tests/test_user_profile_routes.py`, `tests/test_volume_progress.py`,
`tests/test_weekly_summary_routes.py`) — all allowlisted and untouched.

### 1.4 Neighbouring diagnostics that are explicitly **not** ours

A path search around this packet's surface also surfaces:

| file | rule | count | Why it is out of scope |
|---|---|---|---|
| `utils/exercise_manager.py:79` | `reportOptionalMemberAccess` (`"get" is not a known attribute of "None"`) | 1 | A **caller** of `FilterPredicates.get_exercises`, but a different file, a different rule family, and a different root cause (an `Optional` row, not a row *shape*). |
| `tests/test_exercise_manager.py` (`:324, :332, :409, :481, :489, :519, :530`) | `reportOptionalSubscript` | 7 | Test file, different rule family. |

`routes/filters.py` — the other caller — carries **no** pyright diagnostic today. All
of the above stay allowlisted in any regenerated baseline and none is claimed as
fixed.

---

## 2. Isolation and read-only discipline actually observed

| Requirement from the brief | What was done |
|---|---|
| Fetch origin, record live `origin/main`, don't trust the main checkout | `git fetch origin`; `origin/main` = `b733c14…`; main checkout HEAD was `5111a7f` and **dirty** (` M .claude/settings.json`, ` M docs/README.md`, `?? docs/OPEN_WORK_EXECUTION_PLAN.md` — all pre-existing, none belonging to this packet, none touched). |
| Create the worktree from the main checkout | `scripts/new-worktree.ps1 -Task pyright-filter-predicates-gate1 -Seed empty` |
| Fast-forward the worktree before measuring | `git merge --ff-only origin/main` → `5111a7f..b733c14`, HEAD verified equal to `origin/main` |
| No app start, no runtime DB | Not started. `-Seed empty` leaves `data/database.db` absent; it was never created. |
| No dependency install/update | None. `.venv` and `node_modules` are **junctions** to the main checkout, used read-only; `npx pyright@1.1.410` resolves from the npm cache and writes nothing into the repo. No `npm ci`, no `pip install`. |
| No full pytest / no E2E | **At planning time:** not run; only the two focused pytest files in §4.1. The full suite was run twice at implementation time (§14.4); no E2E is derived (§10). |
| Ownership claim, limited to one file | **At planning time:** a row in the gitignored `docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md` claiming **`docs/pyright_filter_predicates/PLANNING.md`** and nothing else, with an explicit not-claimed list. Widened to the three §7 paths at implementation start (§11). |

Files touched by this packet: **exactly three**, all listed in §7 — one created
(this document) and two modified. Pyright JSON output, mutation backups and pytest logs
were written to the gitignored `artifacts/` per [`CLAUDE.md`](../../CLAUDE.md) §3
"Repository root policy"; candidate probes and mutation harnesses were written to the
session scratchpad, outside the repository entirely.

---

## 3. Root cause

### 3.1 The declared type

[`utils/database.py:464-468`](../../utils/database.py#L464-L468):

```python
    def fetch_all(
        self,
        query: str,
        params: Optional[Union[Sequence[Any], Mapping[str, Any], Any]] = None,
    ) -> list[dict[str, Any]]:
```

### 3.2 The real row-conversion behavior

`get_connection()` sets `connection.row_factory = sqlite3.Row`
([`utils/database.py:81`](../../utils/database.py#L81)), so `cursor.fetchall()` yields
`sqlite3.Row` objects — and `fetch_all` then converts every one of them:

[`utils/database.py:494`](../../utils/database.py#L494)

```python
        return [dict(row) for row in rows]
```

`fetch_one` does the same at `:462`. **The declared type is truthful for the real
handler: `DatabaseHandler.fetch_all()` never returns a tuple row.** That is the fact
the fix has to be built around — the tuple branch is not reachable through the real
`DatabaseHandler`, but it *is* reachable, and deliberately pinned, through a mocked one
(§4).

### 3.3 Why pyright reports line 124 and not line 126

[`utils/filter_predicates.py:119-130`](../../utils/filter_predicates.py#L119-L130):

```python
        try:
            with DatabaseHandler() as db:
                results = db.fetch_all(query, params if params else None)
                # Handle both tuple and dict results
                if results and isinstance(results[0], tuple):
                    return [row[0] for row in results if row[0]]              # ← 124
                elif results and isinstance(results[0], dict):
                    return [row["exercise_name"] for row in results if row.get("exercise_name")]
                return []
        except Exception as e:
            logger.exception("Error filtering exercises: %s", e)
            return []
```

`results` is inferred `list[dict[str, Any]]`. `isinstance(results[0], tuple)` narrows
**the expression `results[0]`** — it says nothing about the *element type* of
`results`, and nothing at all about `row`, which is a **separate binding** introduced
by the comprehension and typed from `results`'s element type. So inside the tuple
branch `row` is still `dict[str, Any]`, `row[0]` resolves to `dict.__getitem__`, and
`Literal[0]` is not a `str`. Line 126 is clean because `row["exercise_name"]` and
`row.get(...)` are exactly what a `dict[str, Any]` supports.

**Pyright's report is a correct model of the code.** The defect is that the
dual-shape contract this function implements is expressed only in `isinstance` checks
on a *different* expression, and is nowhere present in a type. The fix must put that
contract into the type system, not annotate around it.

### 3.4 Why the fix cannot live in `utils/database.py`

Widening `fetch_all()` to `list[dict[str, Any] | tuple[Any, ...]]` would make the
declaration **false** (§3.2 — it always returns dicts) and would push a new union onto
every one of its call sites repo-wide, almost certainly minting net-new diagnostics
elsewhere. It is also an explicit non-goal: a public-signature change. The correction
stays local to `utils/filter_predicates.py`.

---

## 4. Current runtime / result-shape contract

### 4.1 What the tests pin

[`tests/test_filter_predicates.py`](../../tests/test_filter_predicates.py) patches
`utils.filter_predicates.DatabaseHandler` with a `MagicMock`, so `fetch_all` returns
whatever the test says — which is how the tuple path is reachable at all.

| Test | Line | `fetch_all` returns | Asserted result |
|---|---|---|---|
| `test_filter_exercises_with_tuple_results` | `:237` | `[("Exercise1",), ("Exercise2",)]` | `["Exercise1", "Exercise2"]` |
| `test_filter_exercises_with_dict_results` | `:250` | `[{"exercise_name": "Exercise1"}, {"exercise_name": "Exercise2"}]` | `["Exercise1", "Exercise2"]` |
| `test_filter_exercises_empty_results` | `:266` | `[]` | `[]` |
| `test_filter_exercises_handles_exception` | `:279` | raises `Exception("Database error")` | `[]` |
| `test_filter_exercises_filters_null_names` | `:292` | `[("Exercise1",), (None,), ("Exercise2",)]` | `["Exercise1", "Exercise2"]`, `None not in result` |

**Two of the five pin the tuple path explicitly**, one of them (`:292`) pinning the
falsy-value filter *within* the tuple path. The tuple/dict compatibility is a live,
deliberately tested contract, not dead code — and this plan does not propose removing
either half. Nothing in the repository marks either shape obsolete; there is no
deprecation comment, no `__all__`, and no module-surface test.

Focused run at the base commit, unmodified:

```
.venv/Scripts/python.exe -m pytest tests/test_filter_predicates.py tests/test_filter_registry.py -q
→ 49 passed in 0.10s
```

### 4.2 What the callers consume

| Caller | Line | Call | Consumes |
|---|---|---|---|
| `routes/filters.py` | `:206` | `FilterPredicates.get_exercises(filters=sanitized_filters)` | `len(exercise_names)` for logging, then the list into the response payload |
| `routes/filters.py` | `:307` | `FilterPredicates.get_exercises()` | `jsonify(success_response(data=exercise_names))` |
| `utils/exercise_manager.py` | `:19` | `FilterPredicates.get_exercises(filters)` | returned straight through |

Every caller treats the result as an ordinary `List[str]`. **No caller depends on the
row shape, on which branch ran, or on the exception identity** — only on
"`List[str]`, or `[]` on failure". The response contract of both `/filter_exercises`
and `/get_all_exercises` is therefore untouched by any candidate below.

### 4.3 The full observable contract, measured

Current dispatch behavior across every shape reachable today, with each raise shown as
what it becomes at the `except Exception` boundary (`[]` plus one
`logger.exception` call):

| Input | Current result |
|---|---|
| `[("Exercise1",), ("Exercise2",)]` | `["Exercise1", "Exercise2"]` |
| `[{"exercise_name": "Exercise1"}, …]` | `["Exercise1", "Exercise2"]` |
| `[]` | `[]` |
| `[("Exercise1",), (None,), ("Exercise2",)]` | `["Exercise1", "Exercise2"]` |
| `[{"exercise_name": "Bench Press", "equipment": "Barbell"}]` (real `fetch_all` shape) | `["Bench Press"]` |
| `[{"other": 1}]` (key absent) | `[]` — the comprehension guard runs before the subscript, so **no** `KeyError` |
| `[{"exercise_name": ""}]` | `[]` |
| `[("A",), {"exercise_name": "B"}]` (**mixed**, tuple first) | raises `KeyError` → `[]` |
| `[{"exercise_name": "A"}, ("B",)]` (**mixed**, dict first) | raises `AttributeError` → `[]` |
| `[["A"], ["B"]]` (neither shape) | `[]` — both discriminators false |
| `None` | `[]` |

The two **mixed-shape** rows are the load-bearing detail: the current code decides the
whole result set from `results[0]` and then *raises* on any row of the other shape. A
candidate that narrows per row silently changes those two rows from `[]` to a partial
list. Both are unreachable through the real `DatabaseHandler` and neither is pinned by
a test — but "unpinned" is not "free to change", and §6 treats a change there as a
real cost, not a rounding error.

---

## 5. Candidate matrix

Eight structures were written to a standalone probe reproducing `fetch_all`'s exact
declared return type, and run under `pyright@1.1.410` with `pythonVersion 3.14` /
`pythonPlatform Windows`. **Five of them do not fix the diagnostic at all.**

| # | Structure | pyright 1.1.410 | Why |
|---|---|---|---|
| — | **current code** (control) | **2 errors** | reproduces §1.3 exactly |
| B | keep the outer discriminator, add `isinstance(row, tuple)` inside the comprehension | **2 errors** | `row` is `dict[str, Any]`; `isinstance(row, tuple)` narrows it to a *synthesized intersection* of `dict` and `tuple`, whose `__getitem__` still resolves to `dict`'s |
| C | `results: Sequence[object] = db.fetch_all(...)` | **2 errors** | pyright **narrows a declared variable to the assigned type**; `results` reverts to `list[dict[str, Any]]` |
| D | `results: Sequence[Tuple[Any, ...] \| Dict[str, Any]] = db.fetch_all(...)` | **2 errors** | same narrow-on-assignment rule |
| E | D + per-row `isinstance` | **2 errors** | narrow-on-assignment, then the intersection of B |
| F | single-pass `for` loop with `row[0] if isinstance(row, tuple) else row.get(...)` | **1 error** | same intersection as B |
| G | declare-then-assign on separate statements (`results: Sequence[Row]` / `results = …`) | **2 errors** | narrow-on-assignment applies to the assignment, not the declaration |
| M | `TypeIs[Sequence[Tuple[Any, ...]]]` guard applied to `results` (declared `list[dict[str, Any]]`) | **2 errors** | `TypeIs` narrows *soundly*, i.e. to the intersection of the declared and asserted types — which is again dict-flavoured |
| H / I | private helper whose **parameter** declares `Sequence[Row]` (or `Sequence[object]`) + per-row `isinstance` | **0 errors** | a parameter is not subject to narrow-on-assignment; `row` is a real union member, so narrowing yields `Tuple[Any, ...]` with no intersection |
| O | module-level `TypeGuard[Sequence[Tuple[Any, ...]]]` applied to `results` in place | **0 errors** | `TypeGuard` narrowing is unchecked, so the declared `list[dict[str, Any]]` is replaced outright |
| **P** | private helper with parameter `Sequence[Row]`, **both** branches guarded by `TypeIs` predicates over that same parameter type | **0 errors** | sound: `Sequence[Tuple[Any, ...]]` *is* assignable to `Sequence[Row]` |
| **Q** | identical to P but with `TypeGuard` predicates | **0 errors** | as P, with an unchecked negative branch |

Two conclusions worth carrying forward:

1. **Per-row `isinstance` alone never fixes this.** Candidates B, E and F all fail,
   because narrowing a `dict`-typed name with `isinstance(x, tuple)` produces an
   intersection, not the tuple. Any fix must change the *declared* type that `row` is
   drawn from — and the only place a declaration survives is a **function parameter**.
2. **`TypeIs` is not automatically the safer choice.** Applied directly to `results`
   (candidate M) its soundness rule is exactly what keeps the diagnostic alive. It
   only works once the value has crossed a parameter boundary that declares the union
   (candidate P).

### 5.1 End-to-end proof against the real `DatabaseHandler`

The two recommended shapes were re-run against the **actual**
`utils.database.DatabaseHandler` — pyright configured with `extraPaths` into this
worktree, so `db.fetch_all(...)` resolved to the real declaration at
`utils/database.py:468`, not a stand-in — with the surrounding `try` /
`with DatabaseHandler()` / `except Exception` body copied verbatim from
`filter_predicates.py:117-130`:

| Probe | Result |
|---|---|
| module-level helper + two `TypeGuard` predicates | **0 errors, 0 warnings** |
| `@staticmethod` helpers on the class (matching the file's existing shape) | **0 errors, 0 warnings** |

---

## 6. Recommended fix

**Candidate Q, in the `@staticmethod` form.** The two predicates use neither `cls` nor
`self`, so `@staticmethod` is the accurate decorator; `_exercise_names` takes `cls`
because it calls them. They stay on the class rather than at module scope because every
existing member of `FilterPredicates` is a `classmethod`, and the module-level functions
in this file are reserved for the documented backward-compat wrappers.

```python
from typing import Any, Dict, List, Optional, Sequence, Tuple, TypeGuard, Union

# A result row as this module accepts it: positional (tuple) or keyed (dict).
# DatabaseHandler.fetch_all() returns the keyed shape; the positional shape is a
# supported input from any other row source and is pinned by
# tests/test_filter_predicates.py:237 and :292.
ExerciseRow = Union[Tuple[Any, ...], Dict[str, Any]]


class FilterPredicates:
    ...
    @staticmethod
    def _rows_are_tuples(
        rows: Sequence[ExerciseRow],
    ) -> TypeGuard[Sequence[Tuple[Any, ...]]]:
        return bool(rows) and isinstance(rows[0], tuple)

    @staticmethod
    def _rows_are_dicts(
        rows: Sequence[ExerciseRow],
    ) -> TypeGuard[Sequence[Dict[str, Any]]]:
        return bool(rows) and isinstance(rows[0], dict)

    @classmethod
    def _exercise_names(cls, rows: Sequence[ExerciseRow]) -> List[str]:
        if cls._rows_are_tuples(rows):
            return [row[0] for row in rows if row[0]]
        elif cls._rows_are_dicts(rows):
            return [row["exercise_name"] for row in rows if row.get("exercise_name")]
        return []

    @classmethod
    def filter_exercises(cls, filters: Optional[Dict[str, str]] = None) -> List[str]:
        query, params = cls.build_filter_query(filters)

        try:
            with DatabaseHandler() as db:
                results = db.fetch_all(query, params if params else None)
                # Handle both tuple and dict results
                return cls._exercise_names(results)
        except Exception as e:
            logger.exception("Error filtering exercises: %s", e)
            return []
```

`Union[...]` rather than `X | Y`, and `Dict`/`List`/`Tuple` rather than the builtin
generics, because that is this file's existing idiom (`filter_predicates.py:8`).

### 6.1 Why this and not the smaller diff

Candidate **O** is a smaller edit (one guard, called in place, no helper). It was
rejected as the recommendation because its guard narrows `list[dict[str, Any]]`
straight to `Sequence[Tuple[Any, ...]]` — two types with no real overlap. That is a
`cast` wearing a predicate's clothes. Candidate Q routes the value through a parameter
whose declared type, `Sequence[Tuple[Any, ...] | Dict[str, Any]]`, is the dual-shape
contract this module has always implemented; the narrowing is then from a union to one
of its own members. The helper exists because §5 measures a parameter to be the only
declaration site that survives pyright's narrow-on-assignment rule.

### 6.2 Behavior preservation — measured across all eleven shapes

The recommended dispatch and the current dispatch were executed against every input in
§4.3 and compared, including the raised-exception identity:

```
candidate Q mismatches vs current: 0   (11/11 identical, KeyError and AttributeError included)
candidate H mismatches vs current: 2   (both MIXED rows: [] → a partial list)
```

Q is behaviorally identical because the two predicate bodies are the original
conditions verbatim: `bool(rows) and isinstance(rows[0], tuple)` is
`results and isinstance(results[0], tuple)` evaluated in boolean context, and likewise
for the dict arm. `bool()` changes the return *type* of the predicate, never the
branch taken.

That measurement is also why **H and I are rejected despite type-checking cleanly**:
per-row narrowing silently converts the mixed-shape raise into a partial success. It
is a small change on an unreachable path, but it is a change, and the brief asks for
the narrowest *behavior-preserving* correction.

### 6.3 Proof that both compatibility paths survive

| Contract | Preserved by |
|---|---|
| tuple rows → first column | `_rows_are_tuples` is the original `results and isinstance(results[0], tuple)`; the branch body `[row[0] for row in rows if row[0]]` is byte-identical |
| tuple rows with a falsy first column are dropped | the comprehension guard `if row[0]` is unchanged — pins `tests/…:292` |
| dict rows → `exercise_name` | `_rows_are_dicts` is the original `results and isinstance(results[0], dict)`; the branch body is byte-identical |
| dict rows missing the key are dropped without `KeyError` | the `row.get("exercise_name")` guard is unchanged and still evaluated before the subscript |
| empty result → `[]` | both predicates return `False` on empty; falls through to `return []` |
| neither shape → `[]` | both predicates return `False`; falls through |
| mixed shapes → raise → `[]` + one `logger.exception` | the branch bodies still index every row unconditionally, so the same exception is raised from the same expression |
| any DB failure → `[]` + one `logger.exception` | `_exercise_names` is called **inside** the `with` and inside the `try`; the handler is untouched |

Neither compatibility path is deleted, weakened, or marked deprecated by this plan.

### 6.4 Costs

1. **`TypeGuard`'s negative branch is an unchecked claim.** `TypeIs` (candidate P)
   also measured clean and is the sound form. `TypeGuard` is recommended anyway, for
   the reason this repository has already written down: the in-repo precedent
   [`utils/_profile_estimator/coverage.py:33-43`](../../utils/_profile_estimator/coverage.py#L33-L43)
   declares `_is_lift_filled` as a `TypeGuard` and documents that it is *"deliberately
   not a `TypeIs`"* because a value of the asserted type can still make the predicate
   return `False`. Exactly that holds here: `_rows_are_tuples([])` returns `False`,
   yet `[]` **is** a valid `Sequence[Tuple[Any, ...]]`. Under the house rule, the
   negative branch says nothing, so `TypeGuard` is the truthful annotation. Candidate
   P is a drop-in substitution measured at 0 errors. **Resolved by §12 decision 1:
   `TypeGuard`; candidate P is not to be substituted.**
2. **`Tuple[Any, ...]` introduces `Any` as a type argument.** The brief prohibits
   `Any`. The reading applied here is that the prohibition targets `Any` as an escape
   hatch for a *value*, and that a DB row's column type genuinely is unknown at this
   boundary — `fetch_all` already declares `list[dict[str, Any]]`, and the existing
   dict branch already lets that `Any` satisfy the `List[str]` return today. The
   `Tuple[Any, ...]` arm is therefore symmetric with an `Any` that is **pre-existing
   and not introduced**. `Tuple[str, ...]` also measured clean and would remove the
   `Any`, but it would be a *false* claim: `tests/…:292` feeds `(None,)`. **Resolved
   by §12 decision 2: `Tuple[Any, ...]`, on the owner's ruling that the "no `Any`"
   constraint bars `Any` as an escape hatch, not an accurate description of this row
   boundary.**

### 6.5 Rejected alternatives

| Alternative | Why rejected |
|---|---|
| per-row `isinstance` inside the comprehension (B/E/F) | **Measured: does not fix the diagnostic** (intersection narrowing) |
| widened local annotation, with or without a split declaration (C/D/G) | **Measured: does not fix it** (narrow-on-assignment) |
| `TypeIs` applied directly to `results` (M) | **Measured: does not fix it** (sound narrowing keeps the dict flavour) |
| helper + per-row `isinstance` (H/I) | Type-checks, but **measured to change behavior** on both mixed-shape inputs |
| module-level `TypeGuard` applied in place (O) | Type-checks and preserves behavior, but narrows between disjoint types — a `cast` in disguise (§6.1). **Rejected by §12 decision 3; not to be substituted.** |
| delete the tuple branch as dead code | It is not dead: two tests pin it (§4.1). Deleting a backward-compatibility contract silently is barred by the brief. |
| widen `DatabaseHandler.fetch_all()`'s return type | Makes a truthful declaration false, is a public-signature change, and would push a union onto every call site repo-wide (§3.4). |
| `cast` / `# type: ignore` / `assert isinstance(...)` / rule disable / baseline-only edit | Forbidden by the brief; each hides the defect rather than removing it. |

---

## 7. Implementation file scope

Gate 1 was signed on 2026-08-27 (§12). The implementation modified exactly these three
paths and no others (`git status --porcelain`, §14.1):

| Path | Change |
|---|---|
| `utils/filter_predicates.py` | the §6 edit **only**: one `Union` alias, two `@staticmethod` predicates, one `@classmethod` helper, the dispatch moved into it, and the `typing` import line extended. **Measured: +41 / −7** across four hunks (`:8`, `:12-17`, `:112-144`, `:161`). The pre-signature estimate here read "≈ +26 / −5, one region"; it was low because the three new members carry docstrings the §6 sketch omitted. |
| `docs/ci_cd_phase3/pyright-baseline.json` | regenerate via `scripts/pyright_baseline_diff.py --write-baseline` **only** (never hand-edited) |
| `docs/pyright_filter_predicates/PLANNING.md` | append measured results |

**Not in scope, at implementation time either:** `utils/database.py`,
`utils/exercise_manager.py`, `routes/filters.py`, `tests/test_filter_predicates.py`
(no test change is planned — see §8.1), `tests/test_filter_registry.py`,
`utils/filter_registry.py`, `docs/test_inventory/**`,
`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`, `docs/MASTER_HANDOVER.md`,
`docs/ACTIVE_DEVELOPMENT.md`, `docs/OPEN_WORK_EXECUTION_PLAN.md`,
`docs/REFACTOR_PLAN.md`, any `static/**`, `scss/**`, `e2e/**` or `.github/**` path.

---

## 8. Verification plan

### 8.1 Focused tests

`tests/test_filter_predicates.py` already covers **both** dispatch branches, the empty
case, the falsy-value filter and the exception path (§4.1) — the branch being
restructured is *not* an uncovered branch, which is the condition that forced new
characterization tests in the earlier `volume_splitter` packet. **No test is planned to
be added, removed, renamed, skipped or modified.** That is deliberate and has a
consequence worth stating: it keeps `Test Inventory Drift` out of this packet entirely
(§9.2).

| Step | Command | Expected |
|---|---|---|
| focused | `pytest tests/test_filter_predicates.py tests/test_filter_registry.py -q` | **49 passed** (measured at this base, unmodified) |
| derived union — [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) §Targeted-test derivation, `utils/X.py` → `tests/test_X.py` plus a `utils.filter_predicates` / `FilterPredicates` search over `tests/` | **measured: the search returns exactly those same two files**, so the derived union *is* the focused row above | — |
| caller coverage (judgment, above the derived union — there is no `tests/test_filters_routes.py`; the filters blueprint is covered by `tests/test_priority0_filters.py`) | `pytest tests/test_exercise_manager.py tests/test_priority0_filters.py -q` | **53 passed** (measured at this base, unmodified) |
| track gate — [`REFACTOR_PLAN.md:1554`](../REFACTOR_PLAN.md) | full `pytest tests/ -q` | pass, no new failures |

Mutation discrimination is required before the fix is called verified: invert each
predicate's condition in turn and confirm the tuple test and the dict test each fail
for the right reason. A green suite after a structural change proves nothing on its
own. **Run and recorded in §14.3, including two survivors and the rival-branch arm that
attributes them.**

### 8.2 Pyright / baseline-diff plan

| Step | Command | Expected |
|---|---|---|
| 1. focused, before | `npx pyright@1.1.410 utils/filter_predicates.py --outputjson` | 2 × `reportArgumentType` at `124:29` and `124:58` |
| 2. focused, after | same | **0 diagnostics in the file** |
| 3. full, after | `npx pyright@1.1.410 --outputjson > artifacts/pyright_after.json` | `errorCount` **130** |
| 4. net-new gate vs the **committed** baseline, *before* regenerating | `python scripts/pyright_baseline_diff.py --current artifacts/pyright_after.json --baseline docs/ci_cd_phase3/pyright-baseline.json` | **PASS**, 0 net-new, 132 → 130 |
| 5. key-by-key multiset delta | the tool's own `counts_from_diagnostics` on before/after | exactly one key moves `2 → 0`; **no other key moves; no key increases** |
| 6. regenerate | same tool `--write-baseline` | `_meta` → **130 / 41** |
| 7. re-simulate CI on the committed tree | `pyright_baseline_diff.py` vs the regenerated baseline | **PASS**, 130 == 130 |
| 8. `git diff docs/ci_cd_phase3/pyright-baseline.json` | — | the single `filter_predicates` record removed + the two `_meta` counts; **nothing else** |

Step 5 is the load-bearing one. A count that lands on 130 is not proof: it is
satisfiable by removing these two and adding two elsewhere. The multiset comparison is
what rules that out. **All eight steps run and recorded in §14.2.**

### 8.3 Lint

`flake8 utils/filter_predicates.py --select=E9,F63,F7,F82,F811,E711,E712,F401` must
exit 0 (`ci.yml:110`, blocking). The extended `typing` import must have every new name
used, or F401 reds. The measure-only pass uses `--max-line-length=127`; the longest
proposed line is well under it.

---

## 9. Baseline delta, and what must **not** move

### 9.1 The delta

| Measure | Before (measured) | After (**measured** — every row below was re-derived after the change; §14.2) |
|---|---|---|
| `reportArgumentType` in `utils/filter_predicates.py` | **2** | **0** |
| Diagnostics in `utils/filter_predicates.py`, all rules | **2** | **0** |
| `reportArgumentType` repo-wide | **50** | **48** |
| Baseline `_meta.total_diagnostics` | **132** | **130** |
| Baseline `_meta.distinct_keys` | **42** | **41** |
| pyright `errorCount` / `filesAnalyzed` | 132 / 239 | 130 / 239 |
| Every other baseline key and count | — | **unchanged** |
| Runtime behavior, response envelopes, SQL, logging, DB | — | **unchanged** |

`distinct_keys` drops by exactly 1 because the two instances share one
`(file, severity, rule, message)` key.

### 9.2 Gates that must stay untouched

| Gate | Why it does not move |
|---|---|
| `Test Inventory Drift` | No test is added, removed, renamed or skipped; no `e2e/**` or `static/js/**` change; no `ci.yml` change; and `docs/pyright_filter_predicates/` is **not** one of the four parametrized-configuration directories (`.claude/commands`, `.claude/agents`, `.claude/rules`, `docs/ai_workflow`) that `tests/test_agent_workflow_contracts.py:44-83` enumerates. Verified against the generator and that test, not assumed. |
| `tsc --noEmit` | No TypeScript touched. |
| Compiled-CSS drift / Stylelint / visual matrix | No `scss/**` or `static/css/**` touched. |
| `JS Supply Chain (npm audit)` | No `package.json` / `package-lock.json` touched. |
| Response-contract tests | `routes/filters.py` untouched; both endpoints still receive a `List[str]` (§4.2). |

---

## 10. Quality-gate routing

[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) **Business logic** row
(`utils/**.py`, non-DB) → `pytest tests/test_filter_predicates.py`; reviewer
**`code-reviewer`**. `product-risk-reviewer` is **not** required: none of
`effective_sets`, `weekly_summary`, `session_summary`, `progression` or `fatigue` is
touched, and no calculation surface is entered. Unioned with the continuous-track gate
at [`REFACTOR_PLAN.md:1554`](../REFACTOR_PLAN.md) — "zero net-new diagnostics, lower
count, focused tests, then full pytest" — and with the repo-wide pyright baseline diff,
which no path glob narrows.

**No E2E is derived.** No template, JS, CSS or response-shape change; the
`/filter_exercises` and `/get_all_exercises` payloads are byte-identical.

[`CLAUDE.md`](../../CLAUDE.md) §1 "Refactor invariant" applies — filtering feeds the
Plan workflow — so the implementation PR description must state explicitly that §6.2's
measured equivalence is why there are no migration notes, rather than leaving the
absence implicit.

---

## 11. Parallel-work collision analysis

Measured at base `b733c14`, against `gh pr list --state open`, `git worktree list` and
the live `WORKSTREAM_OWNERSHIP.local.md`.

| Lane | Paths it owns | Overlap with P1 |
|---|---|---|
| **U2 / PR #427** (`feat/u2-backup-save-first-continuity`) | `static/js/modules/backup-center.js`, `e2e/program-backup.spec.ts`, `docs/backup_confirmation_continuity/PLANNING.md`, `docs/DUPLICATION_REGISTRY.md`, `docs/UI_SCENARIOS_GAP_ANALYSIS.md`, `docs/test_inventory/**`, `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` | **none** |
| **U3a / PR #428** (`docs/u3a-ki010-gate1-plan`) | `docs/toast_type_word_collision/PLANNING.md`, `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` | **none** |
| **U3b / PR #426** (`wt/u3-ki011-gate0`) | `docs/toast_action_continuity/PLANNING.md` | **none** |
| **Dependabot #416** | `package.json`, `package-lock.json`, `scss/**`, `static/css/bootstrap.custom.min.css` | **none** — and #416 is **already merged**; it *is* base commit `b733c14`. Its claim row in the local registry is now stale; correcting it belongs to that lane, not this one. |

**No open PR touches a single `.py` file.** `utils/filter_predicates.py`,
`tests/test_filter_predicates.py` and `docs/ci_cd_phase3/pyright-baseline.json` are
unclaimed and unmodified in every registered worktree.

Shared status documents **not** edited by this packet, per the brief and
[`PARALLEL_WORKFLOW.md`](../ai_workflow/PARALLEL_WORKFLOW.md)'s never-claimed list:
`docs/MASTER_HANDOVER.md`, `docs/ACTIVE_DEVELOPMENT.md`,
`docs/OPEN_WORK_EXECUTION_PLAN.md`, `docs/REFACTOR_PLAN.md`, root and folder
`CLAUDE.md`, `.claude/settings.json`, `.gitignore`.

**The one contended path the implementation needs** is
`docs/ci_cd_phase3/pyright-baseline.json`. It was deliberately left unclaimed while
this packet was planning-only, and was **claimed at implementation start on
2026-08-27**, together with `utils/filter_predicates.py`, in the gitignored
`docs/ai_workflow/WORKSTREAM_OWNERSHIP.local.md`. Two consequences, both discharged in
§14:

- Claim it at implementation start, and re-check it then — a second concurrent pyright
  packet regenerating the same file is the one collision this track can actually
  produce.
- The baseline is regenerated from a **full-tree** pyright run, so it captures whatever
  else is on the branch. The implementation must rebase onto a live `origin/main` and
  re-measure immediately before regenerating; a baseline generated on a stale base
  silently re-allowlists diagnostics that another lane removed.

---

## 12. Gate 1 approval

> ### ☑ SIGNED — 2026-08-27
>
> Implementation of the §7 scope is **approved**, with the §6.4 decisions resolved by
> the owner as follows:
>
> 1. **Candidate Q (`TypeGuard`)** — approved, following the in-repo precedent at
>    `utils/_profile_estimator/coverage.py:33-43`. Candidate P (`TypeIs`) is **not** to
>    be substituted.
> 2. **`Tuple[Any, ...]`** — approved explicitly. Owner ruling: *the "no `Any`"
>    constraint prohibits using `Any` as an escape hatch, not accurately representing
>    this existing row boundary.* `Tuple[str, ...]` is **not** to be substituted.
> 3. **Candidate O** (the smaller in-place diff) is **not** to be substituted.
>
> | Field | Value |
> |---|---|
> | Signed by | Repository owner (Yaakov Avihai Shai) |
> | Date | 2026-08-27 |
> | Base commit at signature | `b733c14f8e76c7f85b1d9dcc75acd8bca8321524` — re-fetched and confirmed unchanged from §1.1 immediately before signing |
> | Chosen candidate | **Q** — `@staticmethod` `TypeGuard` predicates over a `Sequence[ExerciseRow]` parameter, with `ExerciseRow = Union[Tuple[Any, ...], Dict[str, Any]]` |
>
> **Pre-signature re-check (2026-08-27).** Everything §1.1, §1.3 and §11 measured was
> re-measured and came back unchanged. The only delta against the plan as written is a
> newly opened **PR #429** (`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md` only), which
> like #426–#428 touches no `.py` file. Nothing material changed, so implementation
> proceeded.

---

## 13. Recorded, deliberately not acted on

- **The two neighbouring diagnostic clusters inventoried in §1.4** — a natural next
  packet each; neither touched, both still allowlisted.
- **`ExerciseManager.get_exercises(filters: Optional[Dict[str, Any]])`** passes a
  `Dict[str, Any]` into a `Dict[str, str]` parameter and type-checks only because `Any`
  is compatible. Latent looseness in a caller, produces no diagnostic, not touched.
- **`utils/database.py:494`'s `[dict(row) for row in rows]` makes the tuple branch of
  `filter_exercises` unreachable via the real handler.** Whether the dual-shape
  contract should still exist at all is a genuine product question — but it is an
  owner decision with two tests pinning the current answer, and this packet is
  explicitly barred from taking it (§0 non-goals, §6.5).

---

## 14. Measured implementation results

Implemented 2026-08-27 on branch `wt/pyright-filter-predicates-gate1`, base
`b733c14`, per the §12 signature. Every number below is a measurement taken on the
shipped tree, not a restatement of §9's prediction.

### 14.1 What changed

```
git status --porcelain
 M docs/ci_cd_phase3/pyright-baseline.json
 M utils/filter_predicates.py
?? docs/pyright_filter_predicates/

git diff --numstat
 2  9  docs/ci_cd_phase3/pyright-baseline.json
41  7  utils/filter_predicates.py
```

Exactly the three §7 paths, and nothing else. `git diff --check` exits 0.

`utils/filter_predicates.py` moves in **four hunks**: `:8` (the `typing` import),
`:12-17` (the `ExerciseRow` alias and its comment), `:112-144` (the two predicates and
`_exercise_names`) and `:161` (the dispatch replaced by the helper call). The
`build_filter_query` body, the `try` / `except Exception` / `logger.exception` handler,
every public signature and all three module-level wrappers are byte-identical.

The baseline diff is the single `utils/filter_predicates.py` record removed plus the two
`_meta` counters — nothing else, verified by reading `git diff` on that file in full.

### 14.2 Pyright — §8.2 steps 1-8

| Step | Result |
|---|---|
| 1. focused, before | 2 × `reportArgumentType` at `124:29` and `124:58` |
| 2. focused, after | **0 diagnostics in the file** |
| 3. full, after | `1.1.410`, **239 files, 130 errors**, 0 warnings |
| 4. net-new gate vs the **committed** baseline, before regenerating | **PASS — 0 net-new, baseline 132, current 130**, exit 0 |
| 5. key-by-key multiset delta | **exactly one key moved, `2 → 0`** (`utils/filter_predicates.py` / `error` / `reportArgumentType`). **Keys that increased: 0. New keys absent from the before set: 0.** 42 keys / 132 → 41 keys / 130 |
| 6. regenerate | `--write-baseline` → `Wrote baseline: docs\ci_cd_phase3\pyright-baseline.json (130 diagnostics, 41 distinct keys)`; `_meta` reads **130 / 41**, and the 41 records sum to 130 |
| 7. re-simulate CI on the committed tree | **PASS — 0 net-new, baseline 130, current 130**, exit 0 |
| 8. `git diff` on the baseline | one record removed + two `_meta` counters; nothing else |

Step 5 is the one that matters: a bare count of 130 would also be satisfied by removing
these two and minting two elsewhere, and the multiset comparison rules that out.

**§9's predicted delta is met exactly** — `reportArgumentType` in the file 2 → 0, all
rules in the file 2 → 0, `reportArgumentType` repo-wide 50 → 48, `_meta` 132 → 130 and
42 → 41, `filesAnalyzed` unchanged at 239, no other key or count moved.

### 14.3 Mutation discrimination — and two survivors

Five mutations, each applied alone to the shipped file and reverted afterwards; the file
was SHA-256-verified byte-identical after every revert.

| Mutation | Verdict | Evidence |
|---|---|---|
| **M1** invert `_rows_are_tuples` | **KILLED** | `test_filter_exercises_with_tuple_results` — `assert [] == ['Exercise1', 'Exercise2']` |
| **M2** invert `_rows_are_dicts` | **KILLED** | `test_filter_exercises_with_dict_results` — `assert [] == ['Exercise1', 'Exercise2']` |
| **M4** drop the falsy-value filter in the tuple branch | **KILLED** | `test_filter_exercises_filters_null_names` — `None` survives into the result |
| **M3** drop the `bool(rows)` empty guard | **SURVIVED** | 39 passed |
| **M5** drop the `row.get("exercise_name")` key guard in the dict branch | **SURVIVED** | 39 passed |

M1 and M2 are the discrimination §8.1 required, and both kill. **The two survivors are
reported rather than buried, and were attributed by a rival-branch arm** — the
equivalent mutations were applied to the **pre-change** file recovered from
`git show HEAD:utils/filter_predicates.py`:

| Rival arm, pre-change file | Verdict |
|---|---|
| M3′ drop the empty guard from `if results and isinstance(results[0], tuple)` | **SURVIVED** |
| M5′ drop the key guard from the dict comprehension | **SURVIVED** |
| CONTROL — unmutated pre-change file | passes, 39 |

Both survive identically before the change, so **they are pre-existing coverage gaps,
not regressions introduced by this packet.** Their causes:

- **M3** — dropping the guard makes `rows[0]` raise `IndexError` on an empty result,
  which the module's own `except Exception` converts to `[]`. The empty-result test
  therefore passes through the error path instead of the intended one, and cannot tell
  the two apart.
- **M5** — every dict row in the fixtures carries `exercise_name`, so the falsy-value
  filter on the dict arm is never exercised. The tuple arm's equivalent filter *is*
  covered (M4 kills).

Closing either gap means adding test cases, which §0 and §7 bar this packet from doing.
Recorded in §13 for a future packet instead.

### 14.4 Tests, lint and inventory

| Gate | Command | Result |
|---|---|---|
| focused | `pytest tests/test_filter_predicates.py tests/test_filter_registry.py -q` | **49 passed** (identical to the pre-change baseline) |
| caller coverage | `pytest tests/test_exercise_manager.py tests/test_priority0_filters.py -q` | **53 passed** |
| both together, final tree | `pytest` on all four files | **102 passed** |
| track gate ([`REFACTOR_PLAN.md:1554`](../REFACTOR_PLAN.md)) | `pytest tests/ -q` | **3175 passed, 2 skipped**, exit 0 — 207.50s on the tree as first implemented, **232.42s on the shipped tree** after the §14.5 review fixes |
| flake8 blocking set (`ci.yml:110`) | `--select=E9,F63,F7,F82,F811,E711,E712,F401` | **0**, exit 0 |
| flake8 measure-only | `--select=W291,W293` | **30 before, 30 after** — every one pre-existing; the change adds none. The file's original trailing whitespace inside untouched docstrings was deliberately preserved so the diff carries no whitespace churn |
| `Test Inventory Drift` | `scripts/generate_test_inventory.py --check` | **"Test inventory is up to date."**, exit 0 — no test was added, removed, renamed or skipped |
| E2E | — | none derived (§10); no template, JS, CSS or response-shape change |

The full suite was run twice — once on the tree as first implemented and once after the
§14.5 review fixes — because those fixes touched the shipped module, and a gate run
against a superseded tree is not evidence about the tree that ships. Both were green
with identical counts.

### 14.5 Review, and what it changed

[`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md)'s Business-logic row requires
`code-reviewer`; `unslop-reviewer` was run alongside it because this packet ships a
large evidence document as well as code.

**`code-reviewer` found no defect in the code.** It independently re-derived the
equivalence argument rather than accepting §6.2, and confirmed three things worth
recording because they were not in the plan:

- `bool(rows)` is **required**, not cosmetic — without it a `TypeGuard`-annotated
  function would return a non-`bool`. It also verified that `bool(x)` and `if x:`
  invoke the same `__bool__` / `__len__` protocol with the same failure modes, so the
  rewrite is equivalent for exotic sequence types too, with an identical number of
  truthiness evaluations and `__getitem__` calls.
- `results is None` still returns `[]`: `bool(None)` is False at both predicates and
  control falls through, exactly as the old `if` / `elif` chain short-circuited.
- One **observable but untested** difference it found that §6.2's harness could not see:
  the traceback captured by `logger.exception` now carries one extra frame
  (`_exercise_names`) and reports the branch line inside the helper. No test asserts log
  content, and the message template, logger and level are unchanged.

Its one defect finding was that §14 was promised three times and did not exist. This
section is that fix.

**`unslop-reviewer`** found three source-comment problems, all accepted and fixed:

| Finding | Fix |
|---|---|
| The `ExerciseRow` comment claimed the tuple shape was "a supported input from any other row source" — an overclaim this document's own §3.2 contradicts | rewritten to say `fetch_all` only ever returns the keyed shape and the positional shape arrives through a substituted handler, with the two test pins named |
| `_exercise_names`'s docstring ended "exactly as it always has" — refactor history in a docstring | reworded to state the invariant without the history |
| `# Handle both tuple and dict results` now restated the call beneath it | deleted; `_exercise_names` names the behavior |

**One deviation from the signed §6 code block is recorded here rather than left
implicit:** that block retained the `# Handle both tuple and dict results` comment.
Deleting it is a comment-only refinement inside the approved file, taken on the
reviewer's finding; no code, type or behavior differs from the signed candidate.

It also found a set of statements elsewhere in this document that the signature and the
implementation had falsified — §2's "files created: exactly one" and its two
planning-time rows, §6.4's three still-open decisions, §7's "future" heading and its
superseded `≈ +26 / −5` estimate, §9's "After (expected)" column header, and the
forward references to this section. All were corrected in place; the amended sections
are named in the status line at the top of this document.

### 14.6 Contract preservation, restated against the shipped code

Nothing in §6.3 moved. Both compatibility paths survive with byte-identical branch
bodies; the mixed-shape result set still raises rather than returning a partial list;
`_exercise_names` is called inside both the `with DatabaseHandler()` block and the
`try`, so every database failure still routes to `logger.exception` and `[]`. No
`cast`, no `# type: ignore`, no `assert`, no rule suppression, and no `Any`-typed value
was introduced — `Tuple[Any, ...]` is a type argument, approved under §12 decision 2.

`CLAUDE.md` §1's refactor invariant is satisfied by argument, not by omission: the PR
description states that §6.2's eleven-input equivalence measurement and §14.3's mutation
results are why there are no migration notes.
