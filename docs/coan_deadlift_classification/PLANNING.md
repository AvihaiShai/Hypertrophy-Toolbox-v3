# Barbell Coan Deadlift classification (#715, AUD-0966)

Planning size: **Medium** (`docs/ai_workflow/QUALITY_GATE.md`, plan-stage routing): a
bounded catalog-data change with known scope. No schema, API or calculation-code change.
Required planning gate: **Gate 1** (owner plan approval). No council.

## Section 0 — Requirement

### Owner decision (2026-11-18, verbatim)

> #715 — choose b1. Use Gluteus Maximus / Quadriceps / Lower Back, isolated muscle
> gluteus-maximus; retain hinge/deadlift. Treat this as a moderate-confidence catalog
> convention based on the semi-sumo description and consistency with the existing sumo
> row. Remove MuscleWiki as supporting evidence because its classification was not
> verified.
>
> Approve the comment with that correction. Keep existing installations' muscle fields
> unchanged and explain this limitation. Prepare the Gate 1 plan with the proposed
> regression coverage and required reviews.

The decision and its rationale are recorded on issue #715.

### Current state (measured 2026-11-17 on `main` at `ad6f739b`)

`data/catalog.seed.db`, row `Barbell Coan Deadlift`:

| Column | Current | Target |
|---|---|---|
| `primary_muscle_group` | `Quadriceps` | `Gluteus Maximus` |
| `secondary_muscle_group` | `Gluteus Maximus` | `Quadriceps` |
| `tertiary_muscle_group` | `Lower Back` | `Lower Back` (unchanged) |
| `advanced_isolated_muscles` | `quadriceps` | `gluteus maximus` |
| `exercise_isolated_muscles` rows | `quadriceps` | `gluteus-maximus` |
| `movement_pattern` / `movement_subpattern` | `hinge` / `deadlift` | unchanged |

Every other column is unchanged. The target values copy the existing `Barbell Sumo
Deadlift` row's spelling in both places: `gluteus maximus` in the text column (the
form used by 41 catalog rows) and `gluteus-maximus` in the normalized table (81 rows).

### Acceptance criteria

1. **Given** the shipped seed, **when** the `Barbell Coan Deadlift` row is read,
   **then** its muscle columns and isolated-muscle rows equal the Target column
   above, and its movement pattern is `hinge` / `deadlift`.
2. **Given** the shipped seed, **when** any other exercise row or isolated-muscle row
   is compared with `ad6f739b`, **then** it is identical. Row counts stay 1897
   exercises and 1598 isolated-muscle rows.
3. **Given** the seed after the edit, **when** the existing seed-hygiene test runs,
   **then** integrity is `ok`, the freelist is empty and no user state is present.
4. **Given** an existing install whose Coan row holds the old values, **when** the
   catalog upgrade runs against the new shipped seed, **then** the old muscle columns
   and isolated-muscle rows stay unchanged. This is the owner-accepted limitation.
5. **Given** a new install, **when** the runtime database is bootstrapped from the
   seed, **then** the Coan row has the Target values. Bootstrap copies the seed, so
   criterion 1 implies this.

### Calculation surface

No calculation code changes. The edit changes a catalog **input** to
`utils/weekly_summary.py` and `utils/session_summary.py`, which credit primary,
secondary and tertiary roles at 1.0, 0.5 and 0.25 (`utils/effective_sets.py`).

Worked example, new install, 3 logged sets of Barbell Coan Deadlift, raw counting:

| Mode | Before | After |
|---|---|---|
| `TOTAL` | Quadriceps 3.0, Gluteus Maximus 1.5, Lower Back 0.75 | Gluteus Maximus 3.0, Quadriceps 1.5, Lower Back 0.75 |
| `DIRECT_ONLY` | Quadriceps 3 | Gluteus Maximus 3 |

Effective counting applies the same effort and rep-range factors to both columns. The
isolated-muscle stats move the exercise from `quadriceps` to `gluteus-maximus`. The
PR carries migration notes and updated coverage, per the refactor invariant.

### Out of scope

- The catalog-ownership contract in `utils/catalog_upgrade.py` and any migration that
  rewrites existing installs.
- The `utility`, `grips`, `stabilizers`, `synergists` and other columns of the row.
- `e2e/fixtures/database.visual.seed.db`, the visual fixture. It holds its own copy
  of the row. The prepared visual DB refreshes catalog-owned columns only, so the
  visual matrix is unaffected.
- Other catalog rows. The remaining AUD entries on the issue stay deferred.

## Plan

Branch `fix/715-coan-deadlift-classification` from fetched `origin/main`.

1. **Edit the seed.** Use a one-off script under `artifacts/opus-20261117/715/`,
   which is not committed. It:
   - works on a copy of `data/catalog.seed.db`;
   - in one transaction, updates the three changed columns, deletes the Coan
     `exercise_isolated_muscles` row and inserts `gluteus-maximus`;
   - runs `VACUUM`, which keeps the existing freelist-zero and no-recoverable-pages
     contract;
   - asserts integrity `ok` and a clean `foreign_key_check`;
   - writes a row-level diff of the copy against the original for every table;
     the diff must show only the Coan row and its one isolated-muscle row;
   - replaces the seed only after those checks pass.

   The PR records the exact SQL and the before and after logical hashes so the edit
   can be reproduced.
2. **`tests/test_catalog_seed.py`**
   - Update the two hash prefixes in `EXPECTED_CATALOGS`. The counts stay the same.
   - Add `test_barbell_coan_deadlift_classification`. It asserts the full Target
     column, the isolated-muscle rows and the hinge / deadlift pattern (criteria 1
     and 5). It is a named regression guard, because a reverted row would otherwise
     show up only as an opaque hash mismatch.
3. **`tests/test_catalog_upgrade.py`**: add one test. It builds an existing runtime
   database holding the pre-edit Coan values, runs `upgrade_catalog_from_seed()`
   against the real shipped seed, and asserts that the muscle columns and
   isolated-muscle rows keep their old values (criterion 4). It pins the documented
   limitation to the real seed rather than a synthetic one.
4. **`docs/CHANGELOG.md`**: add an Unreleased "Catalog" entry. It states the new
   classification and that existing installs keep their values unless the user
   edits the exercise.
5. **`docs/test_inventory/`**: regenerate from the resulting tree with
   `scripts/generate_test_inventory.py`. If a Sol PR merges first, rebase onto
   fetched `origin/main` and regenerate again.

No changes to `utils/`, `routes/`, templates, static assets or the schema.
`docs/fatigue_meter/data-audit.md` stays a historical record and is not edited.

## Verification

| Gate | Reason |
|---|---|
| `pytest tests/test_catalog_seed.py tests/test_catalog_upgrade.py tests/test_catalog_seed_bootstrap.py tests/test_effective_sets.py tests/test_weekly_summary.py tests/test_session_summary.py` | Targeted: the seed contracts, upgrade ownership, bootstrap, and the summaries that consume the row |
| `/verify-suite` (full pytest, then Chromium E2E) | The seed is the bootstrap source for every E2E runtime. Applies by analogy with the `QUALITY_GATE.md` rule for scripts that write the exercise catalog |
| `scripts/generate_test_inventory.py --check` | Two new pytest nodes (`Test Inventory Drift`) |
| `scripts/pyright_baseline_diff.py` | The diff touches `.py` files |

Reviewers on the finished diff, in parallel: **`code-reviewer`** (required for a
catalog write) and **`product-risk-reviewer`** (the change alters weekly and session
summary output). Their verdicts are reported to the owner; a reviewer that fails to
run is recorded as incomplete.

## Migration notes (for the PR description)

- **New installs:** the Coan row ships as Gluteus Maximus / Quadriceps / Lower Back,
  isolated `gluteus-maximus`. Summaries credit its sets to Gluteus Maximus.
- **Existing installs:** unchanged. Muscle fields and isolated-muscle mappings are
  user-owned, and the catalog upgrade refreshes only movement and media columns. It
  cannot tell an unedited row from an edited one, so it never rewrites them. Users
  who want the new classification can edit the exercise.
- **No schema, API-shape or calculation-code change.**

## Gate 1 sign-off

- [x] Owner approves this plan (2026-11-18): "Gate 1 approved. Proceed with the plan,
  regression tests, required verification and reviewers. Preserve existing
  installations' muscle values and document that limitation."
