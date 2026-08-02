"""Create an isolated SQLite snapshot for visual-regression runs.

The app honors the DB_FILE environment variable. Run this script before P0b
capture, then point Playwright's web server at the printed DB path. By default
it snapshots the committed visual seed DB so normal E2E database mutations do
not change visual baselines:

    python e2e/scripts/prepare_visual_db.py
    $env:DB_FILE = "<printed path>"
    npx playwright test e2e/visual.spec.ts --project=chromium --update-snapshots
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SEED = REPO_ROOT / "e2e" / "fixtures" / "database.visual.seed.db"
DEFAULT_SOURCE = (
    DEFAULT_SEED
    if DEFAULT_SEED.exists()
    else REPO_ROOT / "data" / "catalog.seed.db"
)
DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "visual" / "database.visual.db"

# Paths this seeder must never overwrite: the developer's live DB and the
# auto-backup snapshots beside it. The guard is path-identity based (not
# existence based) so it refuses regardless of whether the file is present.
LIVE_DB = REPO_ROOT / "data" / "database.db"
AUTO_BACKUP_DIR = REPO_ROOT / "data" / "auto_backup"


def assert_safe_output(output: Path, force: bool) -> None:
    resolved = output.resolve()
    live = LIVE_DB.resolve()
    auto_backup = AUTO_BACKUP_DIR.resolve()
    if force:
        return
    if resolved == live or auto_backup in resolved.parents:
        raise SystemExit(
            f"Refusing to --output a live-data path: {resolved}\n"
            "This seeder snapshots a throwaway DB; writing the live "
            "data/database.db (or anything under data/auto_backup/) would "
            "clobber real user data. Pass --force only if you truly intend to."
        )


def _remove_sqlite_sidecars(database_path: Path) -> None:
    for candidate in (
        database_path,
        Path(f"{database_path}-wal"),
        Path(f"{database_path}-shm"),
        Path(f"{database_path}-journal"),
    ):
        candidate.unlink(missing_ok=True)


def snapshot_database(source: Path, output: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source database not found: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)
    _remove_sqlite_sidecars(output)

    with sqlite3.connect(str(source)) as src, sqlite3.connect(str(output)) as dst:
        src.backup(dst)


def apply_migrations(database_path: Path) -> None:
    # Without this, a seed file taken before a schema change silently
    # downgrades the live DB during visual-regression runs and breaks any
    # API that selects newly-added columns.
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))

    import utils.config
    utils.config.DB_FILE = str(database_path)

    from utils.schema_registry import run_all_initializers

    # Mirror app.py's startup table-creation sequence exactly so a visual seed is
    # schema-identical to a freshly booted app — including learned-calibration and
    # fatigue-context settings tables the Profile page reads on every render (a
    # missing table 500s the page and would freeze a broken render into a baseline).
    run_all_initializers(force_base=False)


# Deterministic rows for the two surfaces whose tables would otherwise render
# empty. Without them the Progression goals table and the Body Composition
# snapshot history have no `tbody tr` at all, so no baseline can regress-test
# their row or field separators -- a blind spot that hid a real contrast defect
# until it was found by injecting rows by hand.
#
# Every value here is fixed. Nothing derives from the clock, the catalog or
# insertion order: dates are literals, the ORDER BY keys are distinct, and the
# ids are explicit so row order is stable across regenerations. These rows exist
# only in the throwaway visual snapshot -- this seeder never writes the live DB
# (see assert_safe_output) and nothing in the application creates them.
VISUAL_PROGRESSION_GOALS = (
    # id, exercise, goal_type, current, target, goal_date, created_at
    (1, "Barbell Bench Press", "weight", 60.0, 70.0, "2026-03-02", "2026-01-05 09:00:00"),
    (2, "Barbell Squat", "weight", 100.0, 120.0, "2026-03-16", "2026-01-05 09:00:00"),
    (3, "Barbell Deadlift", "reps", 5.0, 8.0, "2026-04-06", "2026-01-05 09:00:00"),
)

VISUAL_BODY_COMPOSITION_SNAPSHOTS = (
    # id, captured_at, bodyweight, height, neck, waist, hip, age, gender,
    # bfp_navy, bfp_bmi, fat_mass, lean_mass, notes
    (1, "2026-01-06", 82.0, 178.0, 39.0, 86.0, 99.0, 34, "male",
     19.4, 20.1, 15.9, 66.1, "start of block"),
    (2, "2026-02-03", 80.5, 178.0, 38.5, 84.0, 98.0, 34, "male",
     18.1, 19.4, 14.6, 65.9, "mid block"),
    (3, "2026-03-03", 79.2, 178.0, 38.0, 82.5, 97.5, 34, "male",
     17.2, 18.8, 13.6, 65.6, "end of block"),
)


def seed_visual_rows(database_path: Path) -> None:
    """Insert the fixed visual-only rows, idempotently.

    Explicit ids plus DELETE-then-INSERT keep a re-run byte-identical, which is
    what lets two independent generation runs be compared for equality.
    """
    with sqlite3.connect(str(database_path)) as con:
        con.execute("DELETE FROM progression_goals")
        con.executemany(
            """
            INSERT INTO progression_goals (
                id, exercise, goal_type, current_value, target_value,
                goal_date, created_at, completed, completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, NULL)
            """,
            VISUAL_PROGRESSION_GOALS,
        )
        con.execute("DELETE FROM body_composition_snapshots")
        con.executemany(
            """
            INSERT INTO body_composition_snapshots (
                id, captured_at, bodyweight_kg, height_cm, neck_cm, waist_cm,
                hip_cm, age_years, gender, bfp_navy, bfp_bmi, fat_mass_kg,
                lean_mass_kg, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            VISUAL_BODY_COMPOSITION_SNAPSHOTS,
        )
        con.commit()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Override the live-data guard (allows --output of data/database.db).",
    )
    args = parser.parse_args()

    output_path = args.output.resolve()
    assert_safe_output(output_path, args.force)
    snapshot_database(args.source.resolve(), output_path)
    apply_migrations(output_path)
    seed_visual_rows(output_path)
    print(output_path)


if __name__ == "__main__":
    main()
