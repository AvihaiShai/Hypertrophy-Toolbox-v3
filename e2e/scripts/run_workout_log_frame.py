"""Measure the Workout Log against its signed frame requirements on a scratch database."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import zipfile

REPO = Path(__file__).resolve().parents[2]
RUNS = REPO / "artifacts" / "workout-log-frame"
CONTROL = "5dc83cef"
ROUTINE = "GYM - Full Body - Workout A"
CABLE = "Cable Standing Single Arm Internally Rotated Incline Chest Fly"


def validate_paths(run: Path, database: Path, runtime: Path) -> None:
    root = run.resolve()
    for path in (database.resolve(), runtime.resolve()):
        if root not in path.parents or path == (REPO / "data/database.db").resolve():
            raise ValueError(f"Expected a scratch path inside {root}, got {path}")


def prepare(run: Path, database: Path, runtime: Path, source: Path) -> None:
    validate_paths(run, database, runtime)
    # Set both overrides before the seeder or an application import can resolve them.
    os.environ.update(DB_FILE=str(database), HT_RUNTIME_DIR=str(runtime))
    subprocess.run([
        sys.executable, str(REPO / "e2e/scripts/prepare_visual_db.py"),
        "--source", str(REPO / "e2e/fixtures/database.visual.seed.db"),
        "--output", str(database),
    ], cwd=REPO, check=True)
    sys.path.insert(0, str(source))
    from utils.database import DatabaseHandler
    from build_visual_seed import PLAN, SCORED_COUNT

    columns = ("exercise", "planned_sets", "planned_min_reps", "planned_max_reps",
               "planned_rir", "planned_weight", "scored_min_reps", "scored_max_reps",
               "scored_weight", "scored_rir", "scored_rpe", "planned_rpe")
    expected = []
    for i, row in enumerate(PLAN):
        scores = (10, 10, row[5], 1) if i < SCORED_COUNT else (None,) * 4
        expected.append((*row, *scores, None, None))
    with DatabaseHandler(str(database)) as db:
        records = db.fetch_all("SELECT * FROM workout_log")
        assert all(row["routine"] == ROUTINE for row in records)
        assert sorted(tuple(row[key] for key in columns) for row in records) == sorted(expected)
        for exercise, assignment in (
            ("Barbell Deadlift", "scored_min_reps=5, scored_max_reps=5, scored_weight=120, scored_rir=0"),
            ("Barbell Squat", "scored_rpe=9"),
            ("Barbell Curl", "scored_weight=30"),
            ("Barbell Seated Military Press", "planned_rpe=8, planned_rir=NULL"),
        ):
            updated = db.execute_query(
                f"UPDATE workout_log SET {assignment} WHERE routine=? AND exercise=?",
                (ROUTINE, exercise), commit=False,
            )
            if updated != 1:
                raise ValueError(f"Expected exactly one seed record for {exercise}")
        assert db.fetch_one("SELECT 1 FROM exercises WHERE exercise_name=?", (CABLE,))
        db.execute_query(
            """INSERT INTO workout_log
               (routine, exercise, planned_sets, planned_min_reps, planned_max_reps,
                planned_weight, planned_rir, created_at)
               VALUES (?, ?, 3, 12, 15, 12.5, 2, '2026-04-18 09:00:00')""",
            (ROUTINE, CABLE), commit=False,
        )
        fields = ("id", "routine", "workout_plan_id", *columns)
        fixture = [{key: row[key] for key in fields} for row in
                   db.fetch_all("SELECT * FROM workout_log ORDER BY exercise")]
        assert len(fixture) == 7
    (run / "fixture.json").write_text(json.dumps(fixture, indent=2), encoding="utf-8")


def serve() -> None:
    run = Path(os.environ["FRAME_RUN"]).resolve()
    if run.parent != RUNS.resolve():
        raise ValueError(f"Unexpected frame run directory: {run}")
    source = Path(os.environ["FRAME_SOURCE"])
    database, runtime = run / "database.db", run / "runtime"
    validate_paths(run, Path(os.environ["DB_FILE"]), Path(os.environ["HT_RUNTIME_DIR"]))
    sys.path.insert(0, str(source))
    from utils import config, runtime_paths
    if Path(config.DB_FILE).resolve() != database or runtime_paths.runtime_root().resolve() != runtime:
        raise ValueError("Frame server paths differ from the prepared fixture")
    import app
    from utils.runtime_init import init_runtime
    if Path(app.__file__).resolve() != source / "app.py":
        raise ValueError("Frame server imported the wrong application")
    init_runtime()
    application = app.create_app()

    @application.get("/__frame_identity")
    def identity() -> dict[str, str]:
        return {"database": str(Path(config.DB_FILE).resolve()), "runtime": str(runtime_paths.runtime_root()),
                "source": str(Path(app.__file__).resolve().parent)}

    application.run(host="127.0.0.1", port=int(os.environ["FRAME_PORT"]), use_reloader=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-ref", choices=[CONTROL])
    parser.add_argument("--serve", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.serve:
        serve()
        return
    RUNS.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix="control-" if args.control_ref else "candidate-", dir=RUNS))
    database, runtime = run / "database.db", run / "runtime"
    validate_paths(run, database, runtime)
    source = REPO
    if args.control_ref:
        source = run / "source"
        archive = run / "source.zip"
        subprocess.run(["git", "archive", "--format=zip", "-o", str(archive), CONTROL], cwd=REPO, check=True)
        with zipfile.ZipFile(archive) as files:
            files.extractall(source)
        archive.unlink()
    prepare(run, database, runtime, source)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = dict(os.environ, FRAME_RUN=str(run), FRAME_SOURCE=str(source), FRAME_PORT=str(port),
               FRAME_CONTROL=args.control_ref or "", FRAME_URL=f"http://127.0.0.1:{port}",
               FRAME_PYTHON=sys.executable, FRAME_SERVER=str(Path(__file__).resolve()))
    print(f"Workout Log evidence: {run}", flush=True)
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("Node is required to launch Playwright")
    subprocess.run([node, str(REPO / "node_modules/@playwright/test/cli.js"), "test",
                    "--config", str(REPO / "e2e/playwright.workout-log-frame.config.ts")],
                   cwd=REPO, env=env, check=True)


if __name__ == "__main__":
    main()
