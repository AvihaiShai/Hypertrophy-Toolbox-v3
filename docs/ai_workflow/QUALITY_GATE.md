# Quality Gate

*Required gates per change type. Used by `/unslop` and `/verify-and-polish` to decide which tests and reviewers to run. This file is the canonical authority for both the change-type gates and the plan-stage routing below.*

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
| CSS (static bundles) | `static/css/**`, excluding the generated `bootstrap.custom.min.css*` (see the `scss/**` row) | **Shared surfaces** (`base`, `layout`, `components`, `navbar`, `a11y`, `motion`, `theme-dark`, `tokens`): full `pytest` — the cascade contracts (`tests/test_css_cascade_contracts.py`, `tests/test_visual_selector_contracts.py`) run inside that total; any edit to them must be explicitly scoped, justified, and must not weaken an existing guarantee — + Chromium `smoke-navigation`, `nav-dropdown`, `accessibility`, `dark-mode`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening` + the full `visual.spec.ts` matrix (66 tests per platform over 11 pages) + seven-surface Stylelint (`node scripts/css_audit/stylelint_surfaces.mjs`), no category may rise without a recorded owner exception + the Linux `visual-linux` deep gate reconciled against `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`. **Page bundles** (`pages-*.css`): that page's specs from the feature map below + its `visual.spec.ts` variants + Stylelint on the edited file | none required; a shared-surface change is **Large** at plan stage |
| E2E spec | `e2e/**` | run the spec; intentionally re-baseline if visual | none required |
| Tooling / scripts | `scripts/**` at the repository root only — `e2e/scripts/**` stays with the **E2E spec** row above; when two rows match a path, the more specific glob wins | The union from the stem + directory-token search under Targeted-test derivation. If it is empty, `/verify-suite`. **`/verify-suite` regardless of what the search returns** when the changed script writes the `exercises` catalog (`fatigue_stage1_cleanup.py`, `fatigue_movement_pattern_cleanup.py`, `apply_free_exercise_db_mapping.py`, `apply_youtube_curated.py`), writes a committed baseline (`css_audit/emit_baseline.py`), sits on the packaged-artifact path (`stage_package_assets.py`, imported by `Hypertrophy-Toolbox.spec`), or implements one of the two blocking gates below (`generate_test_inventory.py`, `pyright_baseline_diff.py`). Adding or removing a `.py` or `.mjs` file other than `__init__.py` or `p3_*` under `scripts/css_audit/` also requires `tests/test_css_theme_dark_p3_audit_contracts.py` | `code-reviewer`; + `product-risk-reviewer` if the script writes the `exercises` catalog |
| CI workflows | `.github/workflows/**` | full `pytest` — seven test files parse `ci.yml` (`test_playwright_shard_launcher_contracts`, `test_playwright_runner_contracts`, `test_python_version_contract`, `test_node_version_contract`, `test_css_cascade_contracts`, `test_compiled_css_drift_gate_contracts`, `test_release_workflow_contracts`) and no path glob routes to them + regenerate `docs/test_inventory/` if the `e2e-functional-shard` spec list changed | `code-reviewer` + `architecture-reviewer` if a job is added, removed, or converted to `uses:` |
| AI workflow / agent config | `.claude/**`, `CLAUDE.md`, `*/CLAUDE.md`, `docs/ai_workflow/**` | manual dry-run/self-review; run tests only if source behavior changed | `code-reviewer` or careful self-review |
| Product docs only | `docs/**`, `*.md` excluding AI workflow files above | none unless examples/scripts changed | none |

> All three plan-review council reviewers — `architecture-reviewer`, `test-strategist`, `product-risk-reviewer` — are live. Run them at the plan stage via [`/council-plan`](../../.claude/commands/council-plan.md). The table above also names `architecture-reviewer` and `product-risk-reviewer` as code-time reviewers when the relevant change types are touched; `test-strategist` runs at the plan stage only.

> **Notes on the `static/css/**` row.** Run the visual matrix with `PW_VISUAL_SEED=1`; without it 36 of the 66 tests fail on a page-*height* mismatch — missing plan rows, a data difference rather than a paint one — on unmodified CSS too. **Do not read a red count out of this file.** The visual state is platform-specific and moves whenever baselines are regenerated; the producers are [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md)'s Windows ledger and [`CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`](../CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json) for Linux — consult those, and never resolve a red with `--update-snapshots`. **Caveat on the Linux ledger (recorded 2026-08-04):** its `sourceCommit` is `46e340e` and `revisedOn` is `2026-08-01`, both of which predate PR **#281** (`864043f`), which regenerated and owner-accepted the Linux baseline set. The ledger therefore describes reds against a baseline set that has since been replaced, and reconciling a deep-gate run against it will mis-attribute. Re-derive the Linux inherited set before relying on it, and re-pin the ledger in a packet that owns that file. Declarations covered by the oracle blind-spot register in [`CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md`](../CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md) §8 may not cite the pixel matrix as evidence at all and need a computed-style differential instead. The routing above is derived from the gates the WP4.4 packets actually ran — that document §12, plus [`_E_LAYOUT_`](../CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md) §6, [`_D2_A11Y_`](../CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md) §5, [`_F2_NAVBAR_`](../CSS_PHASE4_WP4_4_F2_NAVBAR_EVIDENCE.md) §5–6, [`_H_COMPONENTS_DEAD_`](../CSS_PHASE4_WP4_4_H_COMPONENTS_DEAD_EVIDENCE.md) §10, [`_J_THEME_DARK_`](../CSS_PHASE4_WP4_4_J_THEME_DARK_EVIDENCE.md) §7 and the arc summary [`_K_INTEGRATION_`](../CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md) §7 — under ruling **N10** in [`docs/css_phase4_wp4_4/PLANNING.md`](../css_phase4_wp4_4/PLANNING.md), which closes finding F21.

## Blocking CI gates the change-type table does not derive

Two required checks fail on changes the table above does not route to. Neither is
*narrowly* path-scoped — both are triggered by broad, cross-cutting conditions — so
they are named here once rather than duplicated into every row.

| Check name (branch protection, verbatim) | What actually blocks | Fix when it reds |
|---|---|---|
| `Test Inventory Drift` | `scripts/generate_test_inventory.py --check` against the committed `docs/test_inventory/`. The job has been red-on-drift since 2026-08-01; it entered branch protection later, re-derived 2026-08-04. The check is a whole-file text diff, so *any* difference reds. | Run `python scripts/generate_test_inventory.py` and commit the regenerated artifact. Never hand-edit it. Never edit the workflow. **And never regenerate while an untracked or gitignored `.md` sits in a globbed surface directory** — that reds `--check` locally while CI is green, and regenerating bakes the local file into the committed artifact. Commit that file or give it a `.local.md` suffix first. |
| `Type Check (tsc blocking + pyright measure-only)` | **Two** blocking steps, despite the name. `tsc --noEmit` must report zero errors. Separately, `scripts/pyright_baseline_diff.py` fails on net-new pyright diagnostics against `docs/ci_cd_phase3/pyright-baseline.json`. Only the pyright *count* step is measure-only; the baseline diff beside it is not. | Fix the net-new diagnostic. Re-baselining to make it pass is an owner decision, not a repair. |

**What trips `Test Inventory Drift`.** The artifact pins five change surfaces, not one:

| Pinned surface | Changed path that trips it |
|---|---|
| Per-file pytest node counts | `tests/**` — add, remove, rename, or move a test between files |
| Per-spec Playwright counts | `e2e/**/*.spec.ts` — add, remove, or rename any test |
| `waitForTimeout` lines per file | `e2e/**/*.ts` — add or delete a single hard wait |
| Required functional spec set, derived from the workflow | `.github/workflows/ci.yml` — the `e2e-functional-shard` spec list, or a rename of that job |
| Parametrized configuration surface | **adding or deleting any file under `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, or `docs/ai_workflow/`** |

That last row is a genuine gap in the routing above: the `AI workflow / agent config`
row says "run tests only if source behavior changed", but *adding or deleting* a file
in those directories changes a parametrized node count and reds a required check even
though no source behavior moved. Editing an existing file in place does not.

The pyright baseline diff is repo-wide, not per-path: run it when the diff touches any
`.py`. No glob narrows it.

**The pyright job's name understates what it enforces, and the name stays anyway.**
"measure-only" is accurate for the count step and wrong for the job. The label is
frozen under the CI job naming rule below: this job sits in branch protection, so
renaming it orphans the required context and every PR then blocks on a check that
will never report again. Correct the understanding here; do not correct the label.

**Known-stale, deliberately not fixed here:** the comment at `.github/workflows/ci.yml`
above the `test-inventory` job still says that job "is not in branch protection".
That was true when written and is superseded by the CI job naming section below.
Trust this table and that section, not the workflow comment.

## Diff collection (used by `/unslop`)

Collect all changed files before deriving tests:

```powershell
git diff --name-only HEAD
git diff --name-only --cached
git ls-files --others --exclude-standard
```

If a feature branch has an upstream or known base, also include `git diff --name-only <merge-base>...HEAD`. De-duplicate the final list. Do not rely on plain `git diff --name-only`; it misses untracked planning and evidence artifacts.

## Targeted-test derivation

For each changed file:

- `routes/X.py` → try `tests/test_X_routes.py`, then `tests/test_X.py`, plus any tests found by `rg "routes\.X|X_bp|/route_name" tests`
- `utils/X.py` → try `tests/test_X.py`, plus any tests found by `rg "utils\.X|from utils.X import" tests`
- `templates/X.html` or `static/js/**/X*` → normalize underscores to hyphens and use the feature map below
- `static/css/**` → the **CSS (static bundles)** row above, not the `/verify-suite` fallback; for `pages-*.css` also normalize the page name and use the feature map below to pick that page's specs
- `scripts/**` (repository root; `e2e/scripts/**` is an E2E spec change) → search `tests` for the file **stem** and, for a file below `scripts/`, its **parent directory name** — separator-free, never as a path. The dominant idioms here are `from scripts.x import y` and `ROOT / "scripts" / "x"`, and a slash-path search matches neither: `rg -n "pyright_baseline_diff" tests`, `rg -n "css_audit" tests`. **Never search the bare `scripts/` prefix** — it matches most of the suite and suppresses the fallback. Take the union of every module found; if it is empty, `/verify-suite`. A hit proves a *mention*, not coverage — some are assertion messages, sample inputs, or comments — so confirm the test asserts the behavior you changed, and escalate to `/verify-suite` when it does not
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

## CI job naming — the `(non-required)` suffix is not a status claim

**Branch protection matches a check by its exact display name.** Renaming a job that
sits in the required-contexts list orphans that context: the gate silently stops being
enforced and the PR blocks on a check that will never report again.

Two jobs carry a `(non-required)` suffix while being **genuinely required** in branch
protection today:

- `E2E Fatigue Context (Chromium, non-required)`
- `E2E Erase Flow (Chromium, isolated, non-required)`

**Treat their suffix as historical and leave both names byte-for-byte alone.** They were
promoted into branch protection without a matching rename, and correcting the label now
would cost more than the inaccuracy does. The same reasoning already keeps
`Type Check (tsc blocking + pyright measure-only)` frozen.

The rule that follows:

| Situation | Action |
|---|---|
| Job is **in** branch protection | Never rename it alone. A rename is only safe when paired with a branch-protection context update in the same change. **Never convert it to `uses:` either** — see below. |
| Job is **not** in branch protection | Rename freely — and drop a stale `(non-required)` suffix when its meaning changes. |
| Promoting a job to blocking | Removing `continue-on-error` and returning a real exit code makes the **job** fail. It does **not** make the merge block until the context is added to branch protection — those are two separate changes. |

### Converting a job to `uses:` renames its check

A job that calls a reusable workflow reports its status as **`<caller job name> / <called
job name>`**, not as the caller's name alone. Converting a job to `uses:` is therefore a
rename by side effect, and it orphans the context if that job sits in branch protection —
the same failure as an outright rename, with none of the visual warning.

Both halves are load-bearing once a composite context is protected. `packaged-smoke-windows`
was converted in Packet R1 precisely because it is **not** protected; its composite name is
`Packaged Smoke (Windows bootloader, non-required) / Build and smoke`, and that whole string
is what R1-D4 would promote after 10 green runs. Renaming the child job in
`_packaged-windows.yml` after promotion breaks the gate exactly as renaming the parent would.

`tests/test_release_workflow_contracts.py` asserts that no job whose `name:` appears in the
required-context list uses `uses:`.

`Test Inventory Drift` was renamed under the second row when it became blocking on
2026-08-01, while it was still unprotected. **That second, deliberate step has since
been taken.** Re-derived 2026-08-04 from
`gh api repos/:owner/:repo/branches/main/protection`, branch protection requires
**11** contexts and `Test Inventory Drift` is one of them — so it now sits under the
*first* row above and must never be renamed alone.

## Known exceptions to treat as pre-existing

Current full-suite baseline (2026-05-10):
- `e2e/program-backup.spec.ts:79` — historical DB-state-pollution flake; passed in the 2026-05-10 full run and passes in isolation.

Treat any reappearance of the program-backup flake as known but record whether it passes in isolation. `nav-dropdown.spec.ts` is no longer a known red as of 2026-06-11; failures there should block navbar/theme changes.
