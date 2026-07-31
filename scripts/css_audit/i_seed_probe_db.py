"""WP4.4-i — build the probe database for the five-route computed differential.

Derived deterministically from the committed `e2e/fixtures/database.visual.seed.db`
so the differential is reproducible from tracked inputs alone. That is not a
stylistic preference: N4 Inventory B recorded its "before" numbers against
`artifacts/wp4_4/probe-frozen.db` (sha 7cef8e0a...), `artifacts/**` is gitignored,
and by the time WP4.4-i needed the "after" half of the same before/after gate the
file no longer existed. A gitignored fixture cannot satisfy a before/after gate.

The visual seed populates `user_selection` and `workout_log`, which is enough for
Workout Plan, Workout Log and both Summary routes. It is NOT enough for
Progression: `progression_goals` holds a single row with `completed = 1`, and
`routes/progression_plan.py:118-122` selects `WHERE completed = 0`, so the Current
Goals table renders with a header and no body cells.

Progression is the only route WP4.4-i changes. Measuring it with an empty table
would satisfy every control while proving nothing about the repair (M6: a probe
that changes nothing proves nothing), so this seeds six open goals — enough to
exercise `tbody td`, `tr:nth-child(even) td`, `tr:last-child td` and `tr:hover td`,
which is every row-position rule in the family.

usage:
  python scripts/css_audit/i_seed_probe_db.py --out artifacts/wp4_4/i/probe-i.db
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "e2e" / "fixtures" / "database.visual.seed.db"

# Fixed in every field. Anything derived from the clock would make the database
# digest differ run to run, and both halves of a before/after gate must be able
# to assert the same one.
GOALS = [
    ("Barbell Bench Press", "weight", 80.0, 85.0, "2027-01-04"),
    ("Barbell Bent Over Row", "reps", 8.0, 10.0, "2027-02-01"),
    ("Barbell Curl", "weight", 30.0, 32.5, "2027-03-01"),
    ("Barbell Squat", "weight", 100.0, 110.0, "2027-04-05"),
    ("Barbell Deadlift", "weight", 120.0, 130.0, "2027-05-03"),
    ("Barbell Overhead Press", "reps", 6.0, 8.0, "2027-06-07"),
]
CREATED_AT = "2026-01-01 00:00:00"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", default=str(SEED))
    args = parser.parse_args()

    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    # A stale WAL sidecar silently reverted a freshly seeded database during
    # WP4.4-h and produced td = 0. Remove both before copying, every time.
    for suffix in ("", "-wal", "-shm"):
        candidate = Path(str(out) + suffix)
        if candidate.exists():
            candidate.unlink()
    shutil.copyfile(args.seed, out)

    connection = sqlite3.connect(out)
    try:
        # Deterministic ids: the seed's own row is id 2, so start above it and
        # leave it in place rather than mutating data another packet may rely on.
        connection.executemany(
            "INSERT INTO progression_goals "
            "(id, exercise, goal_type, current_value, target_value, goal_date, "
            " created_at, completed, completed_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, 0, NULL)",
            [
                (100 + index, exercise, goal_type, current, target, date, CREATED_AT)
                for index, (exercise, goal_type, current, target, date) in enumerate(GOALS)
            ],
        )
        connection.commit()

        open_goals = connection.execute(
            "SELECT COUNT(*) FROM progression_goals WHERE completed = 0"
        ).fetchone()[0]
        assert open_goals == len(GOALS), f"expected {len(GOALS)} open goals, got {open_goals}"
    finally:
        connection.close()

    # Collapse the WAL back into the main file so the digest below describes the
    # whole database, not just its non-journalled part.
    connection = sqlite3.connect(out)
    connection.execute("VACUUM")
    connection.close()
    for suffix in ("-wal", "-shm"):
        candidate = Path(str(out) + suffix)
        if candidate.exists():
            candidate.unlink()

    digest = sha256(out.read_bytes()).hexdigest()
    print(f"seed:  {Path(args.seed).name} {sha256(Path(args.seed).read_bytes()).hexdigest()}")
    print(f"probe: {out}")
    print(f"sha256 {digest}")
    print(f"open progression goals: {len(GOALS)}")


if __name__ == "__main__":
    main()
