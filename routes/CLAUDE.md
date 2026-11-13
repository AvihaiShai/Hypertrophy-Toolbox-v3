# routes/ — Orientation

## Purpose
HTTP layer. Each file is one Flask blueprint that validates input, calls `utils/`, and returns a response. No business logic, no direct DB access — those live in `utils/`.

`POST /erase-data` is a direct route (`erase_data()` in `app.py`, added by `create_app()`), not a blueprint.

## Conventions
- All JSON returns via `success_response()` / `error_response()` from `utils/errors.py`.
- New blueprints: define in `routes/X.py`, register in `create_app()` (`app.py`), and add the name to `EXPECTED_BLUEPRINTS` in `tests/test_app_factory.py`, the one deliberate second site, a test oracle. The test `app` fixture is the same factory, so a missing registration = 404 in production and in every test.
- Logger: `from utils.logger import get_logger` then `logger = get_logger()`. Never `print()`.
- Dynamic column names must pass `validate_column_name()` in `filters.py:147` before SQL interpolation.

## Gotchas
- **Response contract**: All JSON routes now use `success_response()` / `error_response()` (legacy `success`/`error` JSON cleaned up 2026-05-21). The replace-exercise "no result" cases (`NO_CANDIDATES`, `DUPLICATE`, `SELECTION_FAILED`) intentionally keep HTTP 200 via `status_code=200` — the JS swap handler keys off `error.reason` rather than HTTP status.
- No auth — single-user local. Do not expose to untrusted networks.
- **`exercise_order` column**: added at startup by `initialize_exercise_order()` (defined in `utils/schema_registry.py`, re-exported from `routes/workout_plan.py`) via `ALTER TABLE`. `get_workout_plan()` in `routes/workout_plan.py` defensively checks `column_exists()` for pre-migration DBs.

## See also
- `.claude/rules/routes.md` — endpoint template, response contract, filter/SQL detail
- root [CLAUDE.md](../CLAUDE.md) §2 (architecture) and §5 (current risks)
