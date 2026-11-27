"""Measure a registered route against the signed frame requirements on a scratch database."""
from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from dataclasses import dataclass
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
ROUTINE = "GYM - Full Body - Workout A"
CABLE = "Cable Standing Single Arm Internally Rotated Incline Chest Fly"


def runs_dir(route: str) -> Path:
    """Where a route's runs go. Each run is a new directory inside it."""
    return REPO / "artifacts" / "frame-check" / route


def validate_paths(run: Path, database: Path, runtime: Path) -> None:
    root = run.resolve()
    for path in (database.resolve(), runtime.resolve()):
        if root not in path.parents or path == (REPO / "data/database.db").resolve():
            raise ValueError(f"Expected a scratch path inside {root}, got {path}")


def seed_workout_log(run: Path, database: Path, source: Path) -> None:
    """The Workout Log's seven records: four edited seed records and one added."""
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


@dataclass(frozen=True)
class Route:
    """One row of the registry. A new route adds a row and its check file, nothing else."""

    label: str
    # The file in e2e/ that playwright.frame.config.ts selects.
    check: str
    # The only commit --control-ref accepts: the one on which the check must fail.
    control: str
    # Edits to the scratch database after the visual seed is copied. A route whose
    # check builds its fixture through the page's own endpoints leaves this empty.
    seed: Callable[[Path, Path, Path], None] | None = None


ROUTES: dict[str, Route] = {
    "workout_log": Route("Workout Log", "workout-log-frame.check.ts", "5dc83cef", seed_workout_log),
    "workout_plan": Route("Workout Plan", "workout-plan-frame.check.ts", "8b023d1a"),
    "overlays": Route("Overlay style", "overlay-style.check.ts", "8b023d1a"),
}


def prepare(route: Route, run: Path, database: Path, runtime: Path, source: Path) -> None:
    validate_paths(run, database, runtime)
    # Set both overrides before the seeder or an application import can resolve them.
    os.environ.update(DB_FILE=str(database), HT_RUNTIME_DIR=str(runtime))
    subprocess.run([
        sys.executable, str(REPO / "e2e/scripts/prepare_visual_db.py"),
        "--source", str(REPO / "e2e/fixtures/database.visual.seed.db"),
        "--output", str(database),
    ], cwd=REPO, check=True)
    if route.seed is not None:
        route.seed(run, database, source)


def serve() -> None:
    key = os.environ["FRAME_ROUTE"]
    route = ROUTES.get(key)
    if route is None:
        raise ValueError(f"Unknown frame route: {key}")
    run = Path(os.environ["FRAME_RUN"]).resolve()
    if run.parent != runs_dir(key).resolve():
        raise ValueError(f"Unexpected frame run directory: {run}")
    control = os.environ.get("FRAME_CONTROL", "")
    if not route.control or (control and control != route.control):
        raise ValueError(f"Unexpected frame control ref for {key}: {control}")
    source = Path(os.environ["FRAME_SOURCE"]).resolve()
    if source != (run / "source" if control else REPO):
        raise ValueError(f"Unexpected frame source: {source}")
    database, runtime = run / "database.db", run / "runtime"
    configured_database = Path(os.environ["DB_FILE"]).resolve()
    configured_runtime = Path(os.environ["HT_RUNTIME_DIR"]).resolve()
    validate_paths(run, configured_database, configured_runtime)
    if configured_database != database or configured_runtime != runtime:
        raise ValueError("Frame server paths differ from the prepared fixture")
    sys.path.insert(0, str(source))
    from utils import config, runtime_paths
    if Path(config.DB_FILE).resolve() != database or runtime_paths.runtime_root().resolve() != runtime:
        raise ValueError("Frame server paths differ from the prepared fixture")
    import app
    if Path(app.__file__).resolve() != source / "app.py":
        raise ValueError("Frame server imported the wrong application")
    from utils.runtime_init import init_runtime
    init_runtime()
    application = app.create_app()

    @application.get("/__frame_identity")
    def identity() -> dict[str, str]:
        return {"database": str(Path(config.DB_FILE).resolve()), "runtime": str(runtime_paths.runtime_root()),
                "source": str(Path(app.__file__).resolve().parent)}

    application.run(host="127.0.0.1", port=int(os.environ["FRAME_PORT"]), use_reloader=False)


def main(argv: Sequence[str] | None = None, *, fixed_route: str | None = None) -> None:
    """Run one route's check. A command that is bound to a route passes `fixed_route`."""
    parser = argparse.ArgumentParser(description=__doc__)
    if fixed_route is None:
        parser.add_argument("--route", choices=sorted(ROUTES), help="the registered route to measure")
    parser.add_argument("--control-ref", help="measure the route's pinned control commit instead of this checkout")
    parser.add_argument("--serve", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.serve:
        serve()
        return
    # Every refusal comes before the run directory, the seed and the server exist.
    key = fixed_route if fixed_route is not None else args.route
    if key is None:
        parser.error("--route is required")
    if key not in ROUTES:
        parser.error(f"unknown route {key}")
    route = ROUTES[key]
    if not route.control:
        parser.error(f"route {key} has no control ref, so its check cannot be shown to fail")
    if args.control_ref is not None and args.control_ref != route.control:
        parser.error(f"--control-ref for {key} accepts only {route.control}")
    runs = runs_dir(key)
    runs.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix="control-" if args.control_ref else "candidate-", dir=runs))
    database, runtime = run / "database.db", run / "runtime"
    validate_paths(run, database, runtime)
    source = REPO
    if args.control_ref:
        source = run / "source"
        archive = run / "source.zip"
        subprocess.run(["git", "archive", "--format=zip", "-o", str(archive), route.control], cwd=REPO, check=True)
        with zipfile.ZipFile(archive) as files:
            files.extractall(source)
        archive.unlink()
    prepare(route, run, database, runtime, source)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = dict(os.environ, FRAME_RUN=str(run), FRAME_SOURCE=str(source), FRAME_PORT=str(port),
               FRAME_ROUTE=key, FRAME_CHECK=route.check,
               FRAME_CONTROL=args.control_ref or "", FRAME_URL=f"http://127.0.0.1:{port}",
               FRAME_PYTHON=sys.executable, FRAME_SERVER=str(Path(__file__).resolve()))
    print(f"{route.label} evidence: {run}", flush=True)
    node = shutil.which("node")
    if node is None:
        raise RuntimeError("Node is required to launch Playwright")
    subprocess.run([node, str(REPO / "node_modules/@playwright/test/cli.js"), "test",
                    "--config", str(REPO / "e2e/playwright.frame.config.ts")],
                   cwd=REPO, env=env, check=True)


if __name__ == "__main__":
    main()
