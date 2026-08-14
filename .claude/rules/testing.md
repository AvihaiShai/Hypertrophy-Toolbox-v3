---
paths:
  - "tests/**"
  - "e2e/**"
  - "tests/conftest.py"
  - "playwright.config.ts"
---

# Testing guide

## Baselines — do not hand-count

Every test total lives in the generated inventory, not in prose:

**[`docs/test_inventory/TEST_INVENTORY.md`](../../docs/test_inventory/TEST_INVENTORY.md)** — per-spec and per-file counts, the required-functional-gate size, and the hard-wait tally. Machine-readable twin: `TEST_INVENTORY.json`.

```bash
.venv/Scripts/python.exe scripts/generate_test_inventory.py            # regenerate
.venv/Scripts/python.exe scripts/generate_test_inventory.py --check    # diff vs committed
```

CI regenerates and diffs it on every PR (`Test Inventory Drift (non-required)`). When your change moves a count, regenerate and commit the artifact in the same PR.

Hand-maintained totals previously rotted into five contradictory numbers at once — the counts that used to sit here were among them. See blindspot B3 in [`docs/TESTING_STRATEGY_PLANNING.md`](../../docs/TESTING_STRATEGY_PLANNING.md). Don't reintroduce one.

## Fixture hierarchy (`tests/conftest.py`)
```
schema_template (session)       — canonical empty schema, built once per worker
test_db_path (function)         — unique `tmp_path` SQLite file per test
  app (function)                — Flask app + a copy of schema_template, all 13 blueprints + erase-data route
    client (function)           — test client bound to the same isolated DB
    db_handler (function)       — DatabaseHandler at the same DB; verifies FK=ON
      clean_db (function)       — DELETEs all rows, preserves tables
        exercise_factory        — INSERTs into exercises
        workout_plan_factory    — INSERTs into user_selection (needs exercise)
        workout_log_factory     — INSERTs into workout_log (needs plan)
```

**Schema comes from a copy, not a rebuild.** `run_all_initializers()` commits
each DDL statement separately, and the pragma profile tests run under fsyncs
every one — `utils/database.py` defaults `FLASK_DEBUG` to `'1'`, selecting
`journal_mode = DELETE` + `synchronous = FULL`. Rebuilding the schema for every
`app` fixture therefore paid a per-statement fsync hundreds of times per run, so
`schema_template` builds it once per worker and `app` copies the file. The copy
is only sound because DELETE mode leaves no `-wal` sidecar; the fixture asserts
that, since a switch to WAL would otherwise yield a silently partial schema. The
erase-data route still calls the real initializers — that path is asserting they
work.

## DB patching pattern — critical
Tests swap DB by **assigning** `utils.config.DB_FILE` (never importing the value):
```python
import utils.config
utils.config.DB_FILE = test_db_path   # ← correct: modifies module attribute
```
`DatabaseHandler.__init__` reads `utils.config.DB_FILE` at call time (`database.py:209`). If you import `DB_FILE` as a bare name at module scope, the patch won't apply.

## Common pitfalls
| Problem | Cause | Fix |
|---|---|---|
| `no such table` in test | Test bypassed conftest init path | Use the shared `app` / `client` / `db_handler` fixtures or run the same init helpers |
| Route returns 404 in test | Blueprint not registered in the test app fixture | Register the needed blueprint in the local test app or use the shared conftest app fixture |
| FK constraint failed | Child row without parent | Use `exercise_factory` before `workout_plan_factory` |
| Test hits live DB | `utils.config.DB_FILE` not patched | Ensure fixture patches it; use `clean_db` fixture |
| `pytest` command not found | System Python, not venv | Use `.venv/Scripts/python.exe -m pytest` |

## E2E setup
```bash
npm install                  # one-time
npx playwright install       # one-time (downloads browsers)
```
Config: `playwright.config.ts` — auto-starts Flask via `.venv/Scripts/python.exe app.py` on port 5000. Chromium only. Serial execution (`fullyParallel: false`). `PW_REUSE_SERVER=1` reuses a running server.

Fixtures: `e2e/fixtures.ts` exports `ROUTES`, `API_ENDPOINTS`, `SELECTORS`, `waitForPageReady()`, `waitForWorkoutPlanReady()`, `expectToast()` — plus a **legacy** `test` whose console collector substring-suppresses real null-dereference crashes and is opt-in per describe.

**New and migrated specs take `test` from `e2e/console-guard.ts` instead**, which fails on every console and page error and takes a per-block allowlist of anchored, wildcard-free patterns. `e2e/strict-fixtures.ts` re-exports the same guard with the allowlist removed from its type for the zero-allowance visual/redesign specs. The split is described in `e2e/CLAUDE.md` and bound by `tests/test_console_guard_contracts.py`.

## E2E test map

Per-spec counts are in [`docs/test_inventory/TEST_INVENTORY.md`](../../docs/test_inventory/TEST_INVENTORY.md), which also marks which specs feed the required functional gate. This table covers what the generator cannot derive: what each spec is *for*.

| Spec | User flow | Fixtures needed |
|---|---|---|
| `smoke-navigation.spec.ts` | Page loads, navbar links, full navigation cycle | None |
| `dark-mode.spec.ts` | Toggle dark mode, localStorage persistence | None |
| `nav-dropdown.spec.ts` | Desktop/mobile navbar behavior and actionability | None |
| `workout-plan.spec.ts` | Routine cascade, plan CRUD, filters, generator, controls, media | Exercises in DB |
| `workout-log.spec.ts` | Import/edit/delete/date/mobile/media flows | Plan + log entries |
| `summary-pages.spec.ts` | Weekly + session structure, Effective/Raw columns, contribution mode, pattern coverage | Exercises |
| `progression.spec.ts` | Page, selector, goals CRUD, methodology, status indicators | Exercises + log |
| `volume-splitter.spec.ts` | Sliders, modes, calculate/reset/export/history | None |
| `volume-progress.spec.ts` | Active-plan volume drawer behavior and geometry | Exercises in DB |
| `program-backup.spec.ts` | Backup Center CRUD, restore, confirmations, API | Plan data |
| `erase-flow.spec.ts` | Erase confirmation and auto-backup banner | None |
| `exercise-interactions.spec.ts` | Delete, replace, superset, inline edit, details | Exercises in plan |
| `accessibility.spec.ts` | Keyboard, ARIA, focus, skip links, contrast, plus a standards-based `@axe-core/playwright` WCAG scan over 11 routes × 2 themes and 3 deterministic states | None; injects its own rows for the populated-table state |
| `api-integration.spec.ts` | API contracts across core workflows | Varies |
| `empty-states.spec.ts` | Empty plan/log/filters/summaries | None |
| `error-handling.spec.ts` | Server 500/503, malformed JSON, double-click | None (mocked) |
| `superset-edge-cases.spec.ts` | Link >2/<2, delete, unlink, replace, persistence | 2+ exercises |
| `validation-boundary.spec.ts` | Negative, rep range, zero, RIR/RPE bounds, decimals | Exercise available |
| `browser-navigation-state.spec.ts` | Back button, refresh, deep-link | None |
| `replace-exercise-errors.spec.ts` | No alternative, all in routine, missing metadata | Specific setup |
| `body-composition.spec.ts` | Snapshot CRUD, BMI fallback, JS/Python parity | None |
| `fatigue.spec.ts` | Fatigue page, periods, empty/mobile/dark states | None |
| `fatigue-context.spec.ts` | Profile setting and advisory Workout Controls | Mocked estimate API |
| `fatigue-stage4-smokes.spec.ts` | Badge mobile geometry and dark contrast | None |
| `learned-calibration.spec.ts` | Calibration settings, actions, golden path | Profile + log data |
| `listener-cleanup.spec.ts` | Detached picker/dropdown listener cleanup | Exercises in plan |
| `ui-hardening.spec.ts` | Toast, form-state, modal keyboard/focus contracts | Varies |
| `user-profile.spec.ts` | Profile, lifts, settings, body map, insights | None |
| `visual.spec.ts` | Eleven-page × 3 viewport × 2 theme screenshot matrix | Visual seed |
| `visual-baseline-thumbnails.spec.ts` | Plan/log thumbnail screenshot matrix | Visual seed |
| `visual-field-separator.spec.ts` | Rendered separator/outline contrast, 7 surfaces × 3 viewports × 2 themes (computed styles, no screenshots — runs in the required functional gate) | None; injects its own rows |

Support files:
- `e2e/fixtures.ts` — route constants, selectors, helpers, and the legacy console collector
- `e2e/console-guard.ts` — strict console/page-error guard with a per-block allowlist
- `e2e/strict-fixtures.ts` — the same guard, narrowed to zero allowance
- `e2e/puppeteer_mcp_summary_regression.py` — Python-based Puppeteer regression (not Playwright)
- `e2e/run_puppeteer_summary_regression.ps1` — PowerShell runner for above
- `e2e/scripts/seed_summary_regression_db.py` — DB seeder for regression testing

## Adding a new blueprint — don't forget the test app
New blueprints must be registered in BOTH `app.py` AND `tests/conftest.py` (in the `app` fixture). Missing step = 404s in tests.
