# Plan Review — Testing Strategy D4: property invariants for `utils/effective_sets.py`

**Decision of record:** [`TESTING_STRATEGY_PLANNING.md` §8.1e](../TESTING_STRATEGY_PLANNING.md) —
D4 signed 2026-08-29 with a bounded scope.
**Product rulings:** [`DECISIONS.md` ADR-009](../DECISIONS.md).
**Base:** `origin/main` at `116d3c5`, re-measured `2026-08-29T19:36:33Z`, zero PRs open at that
instant.

---

## Section 0 — Requirements Brief

### 0.1 What the owner authorized

Two sequential packets, `utils/effective_sets.py` only:

- **Packet A** — duplicate P/S/T role weights are **summed**, and the fix is **atomic** across
  `utils/effective_sets.py`, `utils/weekly_summary.py` and `utils/session_summary.py`, with cheap
  explicit regression tests on both summary paths.
- **Packet B** — `get_rep_range_factor()` becomes **total** on the ruled bands.

Struck from D4 as written: volume splitter, plan generator, progression, `get_effort_factor()`.
Packet C (DB-backed Effective/Raw parity property) stays **deferred**.

### 0.2 Measured substrate

Every figure below was measured at `116d3c5`, not inferred.

| # | Fact | How measured |
|---|---|---|
| S1 | `hypothesis` absent from `requirements.txt`, `requirements-build.txt`, `pyproject.toml`, `pytest.ini` | grep, all four |
| S2 | **38 of 1,897** rows in `data/catalog.seed.db` repeat a muscle across P/S/T | read-only query on a scratch byte-copy |
| S3 | `calculate_effective_sets()` **overwrites** on a repeated muscle: 3 sets / RIR 0 / 8–12 on `Dumbbell Wrist Curl` → `{'Forearms': 1.5}`, not `3.0` | executed probe |
| S4 | Aggregated, that row reports **Effective 3.0 vs Raw 4.5** — the aggregators visit the collided key once per role | simulated aggregation |
| S5 | `get_rep_range_factor()` falls through to 1.0 at averages in `(5,6)`, `(20,21)`, `(30,31)`, `>100`; `(30,31)`→1.0 exceeds **both** neighbours | executed probe |
| S6 | **No test in the repository** passes the same muscle string to two roles | grep across `tests/` |
| S7 | Every exercise in `test_weekly_summary_golden.py`'s fixtures uses **distinct** P/S/T muscles | read, lines 114–124 |
| S8 | Every rep range in `test_fatigue_golden.py`'s fixtures (8–12, 12–15, 1–5, 6–8, 8–10, 10–10) sits **outside** all four gap regions | read |
| S9 | `muscle_contributions` has exactly **two** production consumers: `weekly_summary.py:122`, `session_summary.py:131` | grep |
| S10 | `calculate_effective_sets` has **three** production callers — the two above plus **`utils/fatigue_data.py:239`**, which reads `result.effective_sets` (scalar) and **not** the dict | grep + read |
| S11 | `REP_RANGE_FACTOR_BUCKETS` / `EFFORT_FACTOR_BUCKETS` have **no consumer outside `utils/effective_sets.py`**, tests included | grep |
| S12 | `Test Inventory Drift` is a **required** branch-protection context; `artifacts/` is gitignored (`.gitignore:57`) | `.claude/rules/testing.md`, `.gitignore` |

**S10 is the finding that most changes the plan.** `utils/fatigue_data.py:_stimulus_from_rows()`
feeds the SFR card's stimulus proxy from `result.effective_sets`. Packet A does not touch that
scalar, so **Packet A cannot reach the fatigue surface**. Packet B changes `rep_range_factor`,
which *is* a multiplicand of that scalar, so **Packet B reaches the fatigue surface** and requires
`product-risk-reviewer` on that ground alone.

### 0.3 Open decision carried into the council

**OD-A1 — what should a non-positive rep average return?** The ruling makes the function total for
"valid positive rep averages" and leaves missing data neutral at 1.0. An average of `0` or a
negative average is **neither**: it is present, and it is not valid-positive. A literal `avg < 6`
implementation returns 0.85 for it, where today it returns 1.0. Proposed: treat a non-positive
average as **unusable data and return the neutral 1.0**, matching the missing-data arm. Flagged for
the reviewers rather than assumed.

### Section 0 sign-off — GATE 0 — SIGNED 2026-08-29 (owner)

Signed by the owner ruling that opens this document. OD-A1 is the one item Gate 0 did not settle.

---

## Plan v1

### Scope

| In | Out |
|---|---|
| `utils/effective_sets.py`, `utils/weekly_summary.py`, `utils/session_summary.py` | Any other `utils/**` module |
| `tests/test_effective_sets.py`, `tests/test_weekly_summary.py`, `tests/test_session_summary.py` | `utils/workout_validation.py`, `utils/rep_range_integrity.py` (~~**R2.1**, undecided, owned by another session's branch `fix/r21-scan-export-bounds-min-max`~~ ⚠️ **SPENT 2026-08-30 — R2.1 is DECIDED as ADR-010 and that branch has merged; the file stays out of D4's scope on its own merits, not because it is owned elsewhere**) |
| `requirements.txt`, `tests/conftest.py` (Hypothesis profile), `pytest.ini` if needed | Ingress rep validation, `utils/constants.py` |
| `docs/test_inventory/TEST_INVENTORY.{md,json}` | `routes/**`, templates, JS |

### v1.1 Hypothesis configuration (F5-3, a landing condition — not a follow-up)

1. `requirements.txt` — add `hypothesis` pinned to an exact version.
2. `tests/conftest.py` — register and load a CI profile at import:
   ```python
   from hypothesis import HealthCheck, settings
   settings.register_profile(
       "ci",
       derandomize=True,      # Run Tests is required with NO retry
       deadline=None,         # shared-runner timing variance
       max_examples=200,
       suppress_health_check=[HealthCheck.too_slow],
   )
   settings.register_profile("dev", derandomize=False, deadline=None)
   settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "ci"))
   ```
   **`ci` is the default**, so a local run reproduces CI unless the developer opts out.
3. Example database under `artifacts/` per ADR-002 — `artifacts/hypothesis` via
   `HYPOTHESIS_STORAGE_DIRECTORY`, or `database=None` in the `ci` profile. `artifacts/` is already
   gitignored (S12), so nothing new reaches the repository root.
4. Regenerate `TEST_INVENTORY.{md,json}` **in the same PR** — `Test Inventory Drift` is required
   and Hypothesis tests collect as single pytest nodes, so the count moves by exactly the number of
   test functions added.

### v1.2 Packet A — exact production change

**A1 · `utils/effective_sets.py:262-286`.** Replace the weight-proxy loop with role-keyed
accumulation:

```python
muscle_contributions: Dict[str, float] = {}

for role, muscle in (
    ('primary', primary_muscle),
    ('secondary', secondary_muscle),
    ('tertiary', tertiary_muscle),
):
    if not muscle:
        continue
    if contribution_mode == ContributionMode.DIRECT_ONLY and role != 'primary':
        continue
    weight = MUSCLE_CONTRIBUTION_WEIGHTS[role]
    muscle_contributions[muscle] = (
        muscle_contributions.get(muscle, 0.0) + base_effective * weight
    )
```

Two changes in one edit, both required: accumulation (the ruling), and selecting the primary role
**by name** instead of by `weight == MUSCLE_CONTRIBUTION_WEIGHTS['primary']`. The current
weight-equality proxy is only correct while the three weights stay distinct; under accumulation it
is actively misleading. `DIRECT_ONLY` output is unchanged — only the primary role survives, and its
weight is 1.0, so `base_effective * 1.0 == base_effective`.

**A2 · `utils/weekly_summary.py:104-137`.** The loop must visit each **muscle** once, not each
role, or the accumulated value is added once per duplicate role — 3.0× where 1.5× is ruled. Insert
a dedupe pass that sums role weights per muscle, then iterate that:

```python
role_weights: Dict[str, float] = {}
for muscle, weight_factor in contributions:
    if not muscle:
        continue
    if contribution_mode == ContributionMode.DIRECT_ONLY:
        if weight_factor != MUSCLE_CONTRIBUTION_WEIGHTS['primary']:
            continue
        weight_factor = 1.0
    role_weights[muscle] = role_weights.get(muscle, 0.0) + weight_factor

for muscle, weight_factor in role_weights.items():
    eff_contribution = eff_result.muscle_contributions.get(muscle, 0.0)
    # ... body unchanged ...
```

The loop body is byte-identical below this point. `dict` preserves insertion order, so muscles are
still visited primary → secondary → tertiary.

**A3 · `utils/session_summary.py:115-152`.** The same transformation. `contributed_muscles` and its
`tuple(dict.fromkeys(...))` dedupe collapse to `tuple(role_weights)`, which is the same value for
distinct muscles and the correct value for duplicates.

**Behavior delta, stated exactly.** For a row with **all-distinct** P/S/T muscles — every row in
every existing fixture (S7) — output is **unchanged**, because each muscle appears once with its
own weight. For a duplicate-role row, per-muscle Effective sets **increase** to the summed weight
and now equal Raw at unit factors. `weekly_summary.py`'s
`sessions_by_muscle[muscle][routine] += eff_contribution` is inside the same loop, so it also moves
— and it can only move **up**, never down (1.5×base once, versus 0.5×base twice), so the `>= 1.0`
frequency threshold can newly be met but can never stop being met.

### v1.3 Packet A — tests

- **Property** (`tests/test_effective_sets.py`): for any role→muscle assignment,
  `muscle_contributions[m] == base_effective * Σ{weight(role) : role ↦ m}`; and for every `m`,
  `TOTAL[m] >= DIRECT_ONLY.get(m, 0)`. Muscle names drawn from the **25 distinct
  `primary_muscle_group` values in the seed catalog**, with replacement so collisions are generated,
  plus `None`. `sets ∈ [0,20]`; `rir ∈ [0,10] ∪ {None}`; `min ≤ max` in `[1,50]`.
  `@example` pins the three real seed rows (`Dumbbell Wrist Curl`, `Barbell Pronated Pendlay Row`,
  `Kettlebell Farmers Carry`).
- **Regression, weekly** (`tests/test_weekly_summary.py`): seed one Forearms/Forearms exercise,
  3 sets, RIR 0, 8–12 reps; assert Effective `== 4.5 == ` Raw. **This is the test that fails if A1
  lands without A2.**
- **Regression, session** (`tests/test_session_summary.py`): the same row through
  `calculate_session_summary`, plus one assertion that the muscle appears **once** in the
  per-routine output.
- **Golden**: `weekly_summary_golden.json` is expected **byte-identical** (S7). A diff there means
  the change reached further than intended — a **stop condition**, not a regeneration prompt.

### v1.4 Packet B — exact production change

**B1 · `utils/effective_sets.py:169-206`.** Replace the interval-dict lookup with explicit total
bands matching the ruling:

```python
if avg_reps < 6:
    return 0.85
if avg_reps <= 20:
    return 1.0
if avg_reps <= 30:
    return 0.85
return 0.70
```

A single cumulative `avg <= upper` loop is **wrong** here and must not be used: the first band's
boundary is strict (`< 6`) while the rest are inclusive, so a uniform loop returns 0.85 at exactly
6 reps, where the ruling requires 1.0. `REP_RANGE_FACTOR_BUCKETS` is retired; it has no consumer
outside the module (S11). `EFFORT_FACTOR_BUCKETS` and `get_effort_factor()` are **untouched**.

**Verified delta** — every previously-bucketed average keeps its factor; only the four gap regions
move: `(5,6)` 1.0→0.85, `(20,21)` 1.0→0.85, `(30,31)` 1.0→0.70, `(150,150)` 1.0→0.70.

**Cross-surface consequence (S10):** `rep_range_factor` multiplies into `effective_sets`, which
`utils/fatigue_data.py:250` sums for the SFR stimulus proxy. A plan using a gap-region rep range
therefore moves on the **fatigue page** as well as the summaries. `fatigue_golden.json` is expected
byte-identical because none of its fixtures use a gap-region range (S8) — same stop-condition rule
as the weekly golden.

### v1.5 Packet B — tests

- **Property**: for every integer `1 ≤ min ≤ max ≤ 200`, the result is a member of
  `{0.70, 0.85, 1.0}` and is **monotone non-increasing** in the average for averages above 20.
  `@example` pins `(5,6)`, `(20,21)`, `(30,31)`, `(150,150)`, plus the exact boundaries `(6,6)` and
  `(20,20)` and `(30,30)`.
- **Example tests** for the four moved values and the three boundaries, so the intent is readable
  without running Hypothesis.
- `test_never_returns_zero_factor` is **extended**, not replaced — its `[3, 8, 15, 25, 40]` sample
  is retained and the gap values added, so the packet cannot be read as deleting coverage.

### v1.6 Sequence and gates

**A then B, sequential, two PRs.** They touch adjacent lines in one function and B's delta is only
provable against A's fixed aggregation.

| Gate | Packet A | Packet B |
|---|---|---|
| Targeted pytest | `test_effective_sets.py`, `test_weekly_summary*.py`, `test_session_summary.py` | `test_effective_sets.py`, `test_fatigue_golden.py`, `test_fatigue.py` |
| Full pytest | required (win32 + CI Linux) | required |
| E2E | `e2e/summary-pages.spec.ts` | `e2e/summary-pages.spec.ts`, `e2e/fatigue.spec.ts` |
| Inventory | regenerate in the same PR | regenerate in the same PR |
| Reviewers | `code-reviewer` + **`product-risk-reviewer`** (QUALITY_GATE.md:28 — `effective_sets` / `weekly_summary` / `session_summary`) | `code-reviewer` + **`product-risk-reviewer`** (adds `fatigue`) |
| Migration notes | required — calculation-surface change | required — calculation-surface change |

**Migration notes for the PR body (both packets):** response *shapes* are unchanged; response
*values* change for the affected rows. A names the 38 catalog rows and the frequency-threshold
direction; B names the four moved rep-average regions and the fatigue-page reach.

### v1.7 Rollback

Each packet is one commit touching ≤3 production files. Revert restores prior numbers exactly;
neither packet writes to the database, changes schema, or alters a response shape.

### v1.8 Open decisions carried into the council

- **OD-A1** (§0.3) — non-positive rep average: neutral 1.0, or 0.85?
- **OD-A2** — should A1's role-by-name change ship inside Packet A, or as a separate no-op refactor?

---

## Reviewer findings

Two plan reviewers ran against Plan v1 at `116d3c5`. **Both returned NEEDS REVISION.** Every
finding below was independently re-verified against the code before disposition; none was accepted
on the reviewer's word alone, and the re-verification is recorded in the matrix.

### product-risk-reviewer — verdict: NEEDS REVISION (4 BLOCKING, 4 IMPORTANT, 4 MINOR)

Confirmed clean: the informational-only rule, the local-first non-goals, the backup contract
(ADR-008), and the Effective/Raw side-by-side presentation. Blocking items were the vacuous
fatigue-golden assurance, an incomplete behavior delta, a missed export consumer, and the on-page
explainer copy.

### architecture-reviewer — verdict: NEEDS REVISION (1 BLOCKING, 6 IMPORTANT, 6 MINOR)

Hand-traced the arithmetic and **confirmed it**: A1+A2+A3 yields 4.5 (1.5×) on the collision row;
all-distinct rows are **exactly** bit-identical (adding `0.0` to a finite float is exact in
IEEE-754, and `dict` preserves primary→secondary→tertiary order); `DIRECT_ONLY` is unchanged on both
sides; B1's four-branch shape hits 6/20/30 correctly and the cumulative-loop form is correctly
rejected. It also confirmed both failure modes are really caught — A1 without A2 gives 9.0, A2
without A1 gives 1.5 against Raw 4.5. Blocking item was an internal contradiction on OD-A1.

## Response matrix

| # | Finding | Severity | Disposition |
|---|---|---|---|
| PR-1 | `test_fatigue_golden.py` never calls `effective_sets`; it imports only `utils.fatigue` and exercises `LOAD_MULTIPLIER_BUCKETS`. S8's byte-identity is **vacuous**, and the surface Packet B actually moves — `_stimulus_from_rows` → the `/fatigue` Stimulus/SFR card — has only a key-presence test (`test_fatigue_routes.py:177-185`) | BLOCKING | **ACCEPTED — re-verified** (0 `effective_sets` references in that file). S8's reasoning is **retracted** as S16. v2.6 adds a value-pinning `_stimulus_from_rows` test as a **landing condition for B** |
| PR-2 | Behavior delta omits `status`, `volume_class`, `warning_level`, `is_borderline`, `is_excessive`, `total_reps`, `total_volume`, `avg_sets_per_session`, `max_sets_per_session`, `sets_per_session` | BLOCKING | **ACCEPTED.** v2.3 enumerates all of them. Note these stay *informational badges* — no rule violation, an incomplete migration note |
| PR-3 | `utils/export_service.py:317,382,443` call `calculate_weekly_summary` and splat every stat into the Excel sheet — a missed second-order consumer | BLOCKING | **ACCEPTED — re-verified.** Added as S13; `tests/test_export_weekly_summary_sheet.py` added to both gate rows; export sheet named in the migration notes |
| PR-4 | `templates/weekly_summary.html:68-81` and `session_summary.html:70-83` state the exact rep bands and role weights both packets falsify; nothing pins this copy | BLOCKING | **ACCEPTED — re-verified** by reading the template. Templates brought **into scope** (v2.2 A4, v2.5 B2). Edits confined to the collapsed `<details>` so visual baselines cannot move |
| AR-1 | v1.4 is labelled "exact production change" but its `if avg_reps < 6` first branch returns 0.85 for `avg <= 0`, contradicting §0.3 which proposes 1.0 | BLOCKING | **ACCEPTED.** OD-A1 is **settled** (below) and v2.5's snippet now matches it |
| PR-5 / AR-7 | Packet B's gate row omits the summary surfaces it feeds via `base_effective` | IMPORTANT | **ACCEPTED.** v2.7 adds `test_weekly_summary*.py`, `test_session_summary.py`, `test_export_weekly_summary_sheet.py`, and the fatigue E2E specs, to Packet B |
| PR-6 | Visual-baseline reach never measured | IMPORTANT | **ACCEPTED, and CLOSED BY MEASUREMENT** — see S14. Read-only query on a byte-copy of `e2e/fixtures/database.visual.seed.db`: **0** duplicate-role plan rows and **0** rows whose factor moves. Neither packet reaches the visual corpus |
| PR-7 | ADR-009's Consequences never mentions the `/fatigue` reach; the parked fatigue workstream boundary is unstated | IMPORTANT | **ACCEPTED.** A dated parenthetical is added to ADR-009 in the ADR-007 style (the accepted decision text is not rewritten), and v2.5 states that B touches no constant under `utils/_fatigue/**` |
| PR-8 / AR-1 | OD-A1 is reachable, not hypothetical: `workout_validation.py:77-80` has no lower rep bound, so `0`/negative persist | IMPORTANT | **ACCEPTED.** OD-A1 moved out of "open" and settled as a Gate 1 landing condition |
| AR-2 | v1.3 names 25 catalog muscle values but no data source; the natural implementation queries `catalog.seed.db` at collection time — a raw read outside `DatabaseHandler` | IMPORTANT | **ACCEPTED.** v2.4 requires a **frozen literal tuple** in the test file, with the catalog as recorded provenance only |
| AR-3 | `Hypertrophy-Toolbox.spec:34-37` excludes `pytest`; a new test-only dependency must join that list, and `requirements.txt` also feeds packaging, `pip-audit` and `safety` | IMPORTANT | **ACCEPTED — re-verified.** `Hypertrophy-Toolbox.spec` added to scope; blast radius named in v2.9 |
| AR-4 | An unconditional `from hypothesis import …` in the **root** `tests/conftest.py` fails collection of the whole suite and breaks `scripts/generate_test_inventory.py`, which shells `pytest --collect-only` | IMPORTANT | **ACCEPTED — re-verified.** v2.1 guards the import so a missing `hypothesis` skips profile registration instead of killing collection |
| AR-5 | v1.1's example-database step is an either/or, and `HYPOTHESIS_STORAGE_DIRECTORY` is order-fragile — losing the race writes `.hypothesis/` to the repo root, violating ADR-002 | IMPORTANT | **ACCEPTED.** Decided now: **`database=None`** in the `ci` profile. With `derandomize=True` the example DB carries no value, and this removes the ordering hazard entirely |
| AR-6 | v1.6's two-PR justification is false — A1 and B1 edit *different* functions ~60 lines apart, and B is provable without A | IMPORTANT | **ACCEPTED.** My "adjacent lines" claim was wrong. v2.8 restates the real grounds: two independent rulings, **different blast radii (A cannot reach `fatigue_data.py:250`; B can)**, independent rollback |
| PR-9 | The frequency claim is true but under-argued, and presupposes `sets >= 0`, which nothing validates | MINOR | **ACCEPTED.** v2.3 states the precondition and links it to the strategy's `sets ∈ [0,20]` bound |
| PR-10 / AR-8 (**OD-A2**) | A2/A3 keep the `weight == …['primary']` proxy that A1 is being changed to remove | MINOR | **ACCEPTED — OD-A2 SETTLED:** the role-by-name conversion ships in **all three files inside Packet A**. It is not separable — under accumulation the proxy in `effective_sets.py` becomes wrong, not merely ugly |
| AR-9 | Line citations under-scoped: the weekly loop body runs to **148** (`sessions_by_muscle`), not 137; the session block runs to **154**, and the `if selection_id is not None and contributed_muscles:` guard at 152 changes | MINOR | **ACCEPTED — re-verified by reading.** Ranges corrected in v2.2; the guard becomes `and role_weights` |
| PR-11 / AR-10 | `MUSCLE_CONTRIBUTION_WEIGHTS` exists twice — `effective_sets.py:84` and `_fatigue/per_muscle.py:32`, re-exported at `fatigue.py:67`. Same values today | MINOR | **ACCEPTED.** Import path pinned in v2.4; collision named in the PR body |
| AR-11 | `utils/volume_progress.py:15,326` is a **third** independent P/S/T aggregator that already sums | MINOR | **ACCEPTED — re-verified.** Added as S15. After Packet A, three of three agree; today one of three disagrees |
| PR-12 / AR-12 | The monotonicity property is false at the bottom of the domain once OD-A1 resolves (1.0 at 0, 0.85 at 1, 1.0 at 6) | MINOR | **ACCEPTED.** v2.6 scopes it to `avg > 20` in the test *name*, with a comment that the bottom discontinuity is the deliberate unusable-data arm |
| AR-13 | A `@given` test taking a function-scoped fixture raises `HealthCheck.function_scoped_fixture`, which the profile does not suppress | MINOR | **ACCEPTED.** v2.4 forbids fixtures in `@given` tests outright |

**Nothing was rejected.** Two reviewer claims were checked and found to *understate* the plan's
error — AR-9's line ranges and PR-1's vacuity — and both are corrected as measured, not as argued.

---

## Plan v2

Changes from v1 only; everything not restated below is unchanged.

### v2.0 Section 0 additions

| # | Fact | How measured |
|---|---|---|
| S13 | `utils/export_service.py:317,382,443` call `calculate_weekly_summary`, and `_weekly_summary_to_rows` (`:174`) splats every stat field into the Excel "Weekly Summary" sheet. **Second-order consumer, no code change needed** | grep + read |
| S14 | **Neither packet reaches the visual corpus.** `e2e/fixtures/database.visual.seed.db` holds **6** plan rows: **0** with a duplicate P/S/T role, and **0** whose rep-range factor moves — the only rep ranges present are `(5,8)`, `(6,10)`, `(8,12)`, `(10,15)`, averages 6.5 / 8 / 10 / 12.5, all `1.0` before **and** after | read-only query on a scratch byte-copy |
| S15 | `utils/volume_progress.py:15,326` is a **third** independent P/S/T aggregator, with its own `ROLE_WEIGHTS`, and it already accumulates | read |
| S16 | **S8 is RETRACTED.** `tests/test_fatigue_golden.py` contains **zero** references to `effective_sets`; it imports only from `utils.fatigue` and exercises `LOAD_MULTIPLIER_BUCKETS`, a different constant. Its byte-identity under Packet B is **vacuous and proves nothing** | grep + read |

### v2.0a OD-A1 — SETTLED (Gate 1 landing condition for Packet B)

**A non-positive rep average returns the neutral `DEFAULT_MULTIPLIER` (1.0)**, as an explicit first
branch, because: the ruling makes the function total for *valid positive* averages and keeps missing
data neutral, and zero/negative is neither; 0.85 would assert hypertrophic value for no work, visibly
on the `/fatigue` Stimulus card; neutral-on-unusable is the module's existing house rule
(`get_effort_factor` returns `DEFAULT_MULTIPLIER` for absent data at `effective_sets.py:155`); and
the function still ends up total. Pinned with example tests at `(0,0)` and `(-3,-1)`.

### v2.0b OD-A2 — SETTLED

The role-by-name conversion ships in **all three files, inside Packet A**.

### v2.1 Hypothesis configuration — corrected

1. `requirements.txt` — `hypothesis` pinned to an exact version **verified against Python 3.14.6**
   (ADR-003).
2. **`Hypertrophy-Toolbox.spec:34-37`** — append `'hypothesis'` to `excludes`, matching the
   existing `'pytest'` convention for test-only packages.
3. `tests/conftest.py` — **guarded** registration, so a missing `hypothesis` skips the profile
   instead of failing collection of the whole suite and breaking the inventory generator:
   ```python
   try:
       from hypothesis import HealthCheck, settings
   except ImportError:
       pass
   else:
       settings.register_profile(
           "ci", derandomize=True, deadline=None, max_examples=200,
           database=None, suppress_health_check=[HealthCheck.too_slow],
       )
       settings.register_profile("dev", derandomize=False, deadline=None)
       settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "ci"))
   ```
   `os` is already imported at `tests/conftest.py:5`.
4. **`database=None` is decided**, not an either/or — it removes the
   `HYPOTHESIS_STORAGE_DIRECTORY` ordering hazard and the ADR-002 root-pollution risk entirely, and
   under `derandomize=True` the example database carries no value. **No `artifacts/` path is needed.**
5. Regenerate `TEST_INVENTORY.{md,json}` in the same PR. *(New file `docs/testing_d4_invariants/PLANNING.md`
   sits outside every globbed inventory surface — `.claude/commands/`, agents, `.claude/rules/`,
   `docs/ai_workflow/` — so it does **not** move the agent-workflow node count.)*

### v2.2 Packet A — corrected scope and ranges

- **A1 · `utils/effective_sets.py:262-286`** — unchanged from v1.2.
- **A2 · `utils/weekly_summary.py:104-148`** *(was 104-137 — the loop body runs to 148)*. The dedupe
  pass is as v1.2, and the corrected range makes explicit that
  `sessions_by_muscle[muscle][routine] += eff_contribution` (line 148) moves inside it.
- **A3 · `utils/session_summary.py:115-154`** *(was 115-152)*. Same transformation; additionally the
  guard at line 152 becomes `if selection_id is not None and role_weights:` and line 153's
  `tuple(dict.fromkeys(contributed_muscles))` becomes `tuple(role_weights)`.
- **A4 · `templates/weekly_summary.html:75-81` and `templates/session_summary.html:77-83`** — add one
  line under *Muscle Contribution Weights*: "A muscle listed in more than one role is credited the
  sum of those weights (primary + secondary = 150%)." **Inside the collapsed `<details>` only**; the
  always-visible block at lines 46-56 is not touched, so visual baselines cannot move.
- **Role-by-name** replaces the weight-equality proxy in **all three** production files.

### v2.3 Packet A — complete behavior delta

All-distinct rows: **exactly** unchanged (IEEE-754 exact; insertion order preserved). Duplicate-role
rows: per-muscle Effective rises to the summed weight and equals Raw at unit factors. **Fields that
move, in full** — weekly `sets`, `reps`, `volume`, `sets_per_session`, `avg_sets_per_session`,
`max_sets_per_session`, `total_reps`, `total_volume`, `status`, `volume_class`, and frequency via
`sessions_by_muscle`; session `warning_level`, `is_borderline`, `is_excessive`; and the exported
Excel "Weekly Summary" sheet (S13). All remain **informational badges** — nothing gates, blocks or
auto-adjusts.

**Frequency direction, with its precondition.** Old credit is `|R| · b · w_min`; new is
`b · Σ_{r∈R} w(r)`; since every `w(r) ≥ w_min`, new ≥ old, equality iff `|R| = 1`. **This holds only
for `b ≥ 0`,** i.e. `sets ≥ 0` — which nothing validates (`validate_workout_bounds` has no `sets`
parameter). The strategy's `sets ∈ [0,20]` bound is what keeps the property aligned with the claim.

### v2.4 Packet A — tests, corrected

- **Property**: as v1.3, but muscle names come from a **frozen literal tuple** in
  `tests/test_effective_sets.py` — never a query against `catalog.seed.db` — with the catalog
  recorded as provenance. Import `MUSCLE_CONTRIBUTION_WEIGHTS` **from `utils.effective_sets`**, never
  from `utils.fatigue` (S-collision). **No fixtures in any `@given` test.**
- **Regressions**: weekly and session, as v1.3. The weekly one fails if A1 lands without A2 (9.0) and
  if A2 lands without A1 (1.5 vs 4.5) — verified by the architecture reviewer's hand-trace.
- **Goldens**: `weekly_summary_golden.json` byte-identical (S7) — **stop condition, not a
  regeneration prompt**.

### v2.5 Packet B — corrected

**B1 · `utils/effective_sets.py:169-206`:**
```python
if avg_reps <= 0:
    return DEFAULT_MULTIPLIER   # unusable data — same arm as missing reps (OD-A1)
if avg_reps < 6:
    return 0.85
if avg_reps <= 20:
    return 1.0
if avg_reps <= 30:
    return 0.85
return 0.70
```
**B2 · both templates** — restate the rep bands in ADR-009's wording ("Under 6 reps: 85% / 6–20 reps
(hypertrophy optimal): 100% / Over 20 up to 30 reps: 85% / Over 30 reps: 70% / Rep range not set:
100% (neutral default)"), again inside the collapsed `<details>` only.

**Packet B touches no constant under `utils/_fatigue/**`** — no landmark, band, or pattern weight —
so it does **not** reopen the parked fatigue workstream, even though it moves a displayed `/fatigue`
number.

### v2.6 Packet B — tests, corrected

- **Property** scoped to `avg > 0`; the monotonicity arm is named for `avg > 20` explicitly, with a
  comment that the bottom discontinuity is the deliberate unusable-data arm and must not be
  "repaired" into the `(30,31)` defect ADR-009 removed.
- **Value-pinning test for `utils/fatigue_data.py::_stimulus_from_rows`** covering one in-band and
  one gap-region rep range. **This is a landing condition for Packet B** — it is the only guard on
  the surface B actually moves, and PR-1 showed there is none today.
- Examples for the four moved values, the three boundaries, and OD-A1's `(0,0)` / `(-3,-1)`.
- `test_never_returns_zero_factor` **extended, not replaced**.

### v2.7 Gates — corrected

| Gate | Packet A | Packet B |
|---|---|---|
| Targeted pytest | `test_effective_sets.py`, `test_weekly_summary*.py`, `test_session_summary.py`, **`test_export_weekly_summary_sheet.py`** | all of A's, plus `test_fatigue_routes.py`, `test_fatigue_golden.py`, `test_fatigue.py` |
| Goldens | `weekly_summary_golden.json` byte-identical | `weekly_summary_golden.json` **and** `fatigue_golden.json` byte-identical — the latter **vacuously** (S16), so it is *not* a guard |
| Full pytest | required (win32 + CI Linux) | required |
| E2E | `summary-pages.spec.ts` | + `fatigue.spec.ts`, `fatigue-context.spec.ts`, `fatigue-stage4-smokes.spec.ts` |
| Visual | **not reached** (S14) — a red would be a real surprise, not a regeneration prompt | **not reached** (S14) — same rule |
| Inventory | regenerate in same PR | regenerate in same PR |
| Reviewers | `code-reviewer` + `product-risk-reviewer` | `code-reviewer` + `product-risk-reviewer` |

**E2E is a smoke gate here, not proof.** `e2e/summary-pages.spec.ts:176-180` compares the rendered
table against the **API response** rather than expected values, and is additionally wrapped in
`if (weeklySummary.length > 0)`. It cannot detect a value change. The pytest regressions carry the
weight.

### v2.8 Sequence — justification corrected

Two PRs, **A then B**. v1's "adjacent lines in one function" reasoning was **wrong**: A1 edits
`calculate_effective_sets` (`:262-286`) and B1 edits `get_rep_range_factor` (`:169-206`) — different
functions, ~60 lines apart — and B is fully provable without A. The real grounds are: two
independent ADR-009 rulings; **different blast radii — A cannot reach `utils/fatigue_data.py:250`,
B can**; and independent rollback. **The whole v2.1 Hypothesis landing condition ships in PR A.**

### v2.9 Rollback and blast radius

Each packet is one revertible commit. Neither writes to the database, changes schema, or alters a
response shape. New in v2: `requirements.txt` reaches the packaging job
(`_packaged-windows.yml:77`), `pip-audit` (`ci.yml:75`) and `safety` (`deep-gate.yml:513`), and
`Hypertrophy-Toolbox.spec` is a root build manifest — a shared-state edit to declare under
`docs/ai_workflow/WORKSTREAM_OWNERSHIP.md`.

### v2.10 Still open

**Nothing blocking.** OD-A1 and OD-A2 are settled above. Packet C remains deferred by owner ruling.
~~The one live external constraint is that `utils/rep_range_integrity.py` / **R2.1** is owned by
another session's branch `fix/r21-scan-export-bounds-min-max`; neither packet touches that file.~~
⚠️ **SPENT 2026-08-30.** R2.1 was ruled as **ADR-010** and that branch merged, so the
constraint is gone rather than satisfied. **Nothing replaces it** — neither packet touches
`utils/rep_range_integrity.py`, which remains out of D4's scope by the scope table above.
