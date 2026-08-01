# Quality Gate

*Required gates per change type. Used by `/unslop` and `/verify-and-polish` to decide which tests and reviewers to run. This file is the canonical implemented version of the Tier 1 quality gate.*

## Plan-stage routing

Planning size determines which approval gates happen before implementation. It does
not change the test or reviewer requirements derived from the changed paths below.

| Planning size | Definition | Required planning gates | Repository examples |
|---|---|---|---|
| **Trivial** | Fully specified, single-file, and **no schema, API, or calculation surface** | No Gate 0 or council; proceed to the applicable implementation gate | Correct a product-doc typo; rename a local test variable; clarify a comment without changing behavior |
| **Medium** | Bounded behavior or workflow change with known scope and contracts | Gate 1 (plan approval); Gate 0 may be added when requirements are ambiguous | Add a validation case to an existing route; adjust one existing UI interaction with known E2E coverage; extract a bounded helper while preserving its interface |
| **Large / ambiguous / new workflow** | Cross-cutting work, unclear requirements, a new workflow, or any schema/API/calculation-surface change | Gate 0 (requirements approval) + Gate 1 (council-reviewed plan approval) | Add a new blueprint or table; change Effective Sets/progression/fatigue calculations; introduce a new agent workflow |

**Run the union, never the weaker set.** Planning size never removes a test or
reviewer required by the change-type table. The empty-union `/verify-suite` fallback
under Targeted-test derivation applies only to implementation-gate derivation; a
docs-only change whose row explicitly requires no tests does not escalate to the full
suite.

## Change-type → gates table

| Change type | Path globs | Required gates | Required reviewers |
|---|---|---|---|
| Route / API | `routes/**`, `app.py` | route pytest target (`tests/test_<route>_routes.py` or `tests/test_<route>.py`) + blueprint-registration coverage in `tests/conftest.py` | `code-reviewer`; + `product-risk-reviewer` if response shape changes |
| DB / schema | `utils/db_initializer.py`, `utils/database.py`, `utils/program_backup.py`, `utils/auto_backup.py` | full `pytest` + manual backup/restore smoke | `code-reviewer` + `architecture-reviewer` |
| Business logic | `utils/**.py` (non-DB) | `pytest tests/test_<module>.py` | `code-reviewer`; + `product-risk-reviewer` if `effective_sets` / `weekly_summary` / `session_summary` / `progression` / `fatigue` touched |
| Frontend (template) | `templates/**` | matching Chromium specs from the feature map below | none required |
| Frontend (JS) | `static/js/**` | matching Chromium specs from the feature map below + manual smoke if interactive | none required |
| CSS | `scss/**` | `/build-css` + `e2e/visual.spec.ts` if visual surface changes | none required |
| CSS (static bundles) | `static/css/**`, excluding the generated `bootstrap.custom.min.css*` (see the `scss/**` row) | **Shared surfaces** (`base`, `layout`, `components`, `navbar`, `a11y`, `motion`, `theme-dark`, `tokens`): full `pytest` — the cascade contracts (`tests/test_css_cascade_contracts.py`, `tests/test_visual_selector_contracts.py`) run inside that total, and are run but never edited — + Chromium `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening` + the full `visual.spec.ts` matrix (66 tests per platform over 11 pages) + seven-surface Stylelint (`node scripts/css_audit/stylelint_surfaces.mjs`), no category may rise without a recorded owner exception + the Linux `visual-linux` deep gate reconciled against `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`. **Page bundles** (`pages-*.css`): that page's specs from the feature map below + its `visual.spec.ts` variants + Stylelint on the edited file | none required; a shared-surface change is **Large** at plan stage |
| E2E spec | `e2e/**` | run the spec; intentionally re-baseline if visual | none required |
| AI workflow / agent config | `.claude/**`, `CLAUDE.md`, `*/CLAUDE.md`, `docs/ai_workflow/**` | manual dry-run/self-review; run tests only if source behavior changed | `code-reviewer` or careful self-review |
| Product docs only | `docs/**`, `*.md` excluding AI workflow files above | none unless examples/scripts changed | none |

> All three Tier 2 reviewers — `architecture-reviewer`, `test-strategist`, `product-risk-reviewer` — are live. Run them at the plan stage via [`/council-plan`](../../.claude/commands/council-plan.md). The table above also names `architecture-reviewer` and `product-risk-reviewer` as code-time reviewers when the relevant change types are touched; `test-strategist` runs at the plan stage only.

> **Notes on the `static/css/**` row.** Run the visual matrix with `PW_VISUAL_SEED=1`; without it 36 of the 66 tests fail on a page-*height* mismatch — missing plan rows, a data difference rather than a paint one — on unmodified CSS too. Run correctly, the Windows matrix still carries one inherited red (`workout-plan-desktop-dark`, the animated-logo band); never resolve it with `--update-snapshots`. Declarations covered by the oracle blind-spot register in [`CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md`](../CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md) §8 may not cite the pixel matrix as evidence at all and need a computed-style differential instead. The routing above is derived from the gates the WP4.4 packets actually ran — that document §12, plus [`_E_LAYOUT_`](../CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md) §6, [`_D2_A11Y_`](../CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md) §5, [`_F2_NAVBAR_`](../CSS_PHASE4_WP4_4_F2_NAVBAR_EVIDENCE.md) §5–6, [`_H_COMPONENTS_DEAD_`](../CSS_PHASE4_WP4_4_H_COMPONENTS_DEAD_EVIDENCE.md) §10, [`_J_THEME_DARK_`](../CSS_PHASE4_WP4_4_J_THEME_DARK_EVIDENCE.md) §7 and the arc summary [`_K_INTEGRATION_`](../CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md) §7 — under ruling **N10** in [`docs/css_phase4_wp4_4/PLANNING.md`](../css_phase4_wp4_4/PLANNING.md), which closes finding F21.

## Diff collection (used by `/unslop`)

Collect all changed files before deriving tests:

```powershell
git diff --name-only HEAD
git diff --name-only --cached
git ls-files --others --exclude-standard
```

If a feature branch has an upstream or known base, also include `git diff --name-only <merge-base>...HEAD`. De-duplicate the final list. Do not rely on plain `git diff --name-only`; it misses untracked Tier 1-style artifacts.

## Targeted-test derivation

For each changed file:

- `routes/X.py` → try `tests/test_X_routes.py`, then `tests/test_X.py`, plus any tests found by `rg "routes\.X|X_bp|/route_name" tests`
- `utils/X.py` → try `tests/test_X.py`, plus any tests found by `rg "utils\.X|from utils.X import" tests`
- `templates/X.html` or `static/js/**/X*` → normalize underscores to hyphens and use the feature map below
- `app.py`, `tests/conftest.py`, root configs → fall back to `/verify-suite` (cross-cutting)
- `.claude/**`, `CLAUDE.md`, `*/CLAUDE.md`, `docs/ai_workflow/**` → manual dry-run / self-review per the AI workflow / agent config row above; run tests only if source behavior changed

Run the union. If the union is empty, run `/verify-suite`.

## Frontend feature → E2E map

| Template / JS hint | Primary E2E specs |
|---|---|
| `welcome`, `base`, `navbar`, `darkMode` | `smoke-navigation.spec.ts`, `nav-dropdown.spec.ts`, `dark-mode.spec.ts` |
| `workout_plan`, `workout-plan`, `filters`, `exercises`, `routine-cascade` | `workout-plan.spec.ts`, `exercise-interactions.spec.ts`, `superset-edge-cases.spec.ts` |
| `workout_log`, `workout-log` | `workout-log.spec.ts` |
| `weekly_summary`, `session_summary`, `summary`, `charts` | `summary-pages.spec.ts` |
| `progression_plan`, `progression-plan` | `progression.spec.ts` |
| `volume_splitter`, `volume-splitter`, `plan_volume_panel` | `volume-splitter.spec.ts`, `volume-progress.spec.ts` |
| `user_profile`, `user-profile`, `bodymap`, `muscle-selector` | `user-profile.spec.ts` |
| `backup`, `program-backup`, `backup-center` | `program-backup.spec.ts` |
| validation, error, empty state, accessibility changes | `validation-boundary.spec.ts`, `error-handling.spec.ts`, `empty-states.spec.ts`, `accessibility.spec.ts` |
| API wrapper / endpoint-shape changes | `api-integration.spec.ts` |
| broad layout or CSS visual changes | `visual.spec.ts` |

## Two gates, two purposes

- **`/unslop`** — routine post-implementation polish. Targeted tests + `code-reviewer` + `unslop-reviewer`.
- **`/verify-and-polish`** — full gate before milestones / refactors / schema changes. `/verify-suite` (full pytest + Chromium E2E) + `code-reviewer` + `unslop-reviewer`.

Both end with `/handover` to record what shipped.

## Known exceptions to treat as pre-existing

Current full-suite baseline (2026-05-10):
- `e2e/program-backup.spec.ts:79` — historical DB-state-pollution flake; passed in the 2026-05-10 full run and passes in isolation.

Treat any reappearance of the program-backup flake as known but record whether it passes in isolation. `nav-dropdown.spec.ts` is no longer a known red as of 2026-06-11; failures there should block navbar/theme changes.
