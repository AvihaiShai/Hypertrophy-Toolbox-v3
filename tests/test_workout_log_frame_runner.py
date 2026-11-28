"""The frame-check launcher refuses an unsafe or unregistered run before it seeds anything.

`e2e/scripts/run_frame_check.py` builds a scratch database and starts a server for one
registered route (#736, R21). The check itself is opt-in and runs in no CI job, so
these tests hold what can be held without a browser: the scratch-path guard, the
route registry, and the Workout Log's own command, which is now a shim.
"""
from __future__ import annotations

import dataclasses
import os
from pathlib import Path
import re
from types import SimpleNamespace
import zipfile

import pytest

from e2e.scripts import run_frame_check as frame
from e2e.scripts import run_workout_log_frame as log_command

E2E = Path(__file__).resolve().parents[1] / "e2e"
ROUTE_KEYS = sorted(frame.ROUTES)
# Every registered control, plus the two the plan names and a ref that is never one.
CONTROL_REFS = sorted({row.control for row in frame.ROUTES.values()} | {"5dc83cef", "8b023d1a", "HEAD"})
# Playwright's default test pattern. The root config sets no testMatch, so it applies.
DEFAULT_TEST_PATTERN = re.compile(r".*(test|spec)\.(js|ts|mjs)$")


def _refuse_launch(*args: object, **kwargs: object) -> None:
    pytest.fail("Unexpected child launch")


def _refuse_seed(*args: object, **kwargs: object) -> None:
    pytest.fail("Unexpected seed")


def _unseeded(route: str) -> frame.Route:
    """The registered row, with a seed step that fails the test if it is reached."""
    return dataclasses.replace(frame.ROUTES[route], seed=_refuse_seed)


@pytest.fixture
def checkout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An empty stand-in checkout in which any seed or child process fails the test."""
    repo = tmp_path / "checkout"
    monkeypatch.setattr(frame, "REPO", repo)
    monkeypatch.setattr(frame.subprocess, "run", _refuse_launch)
    return repo


@pytest.mark.parametrize("route", ROUTE_KEYS)
@pytest.mark.parametrize("destination", ["live", "external", "runtime-outside"])
def test_frame_refuses_unsafe_path_before_seed_or_launch(
    tmp_path: Path, checkout: Path, destination: str, route: str,
) -> None:
    run = checkout / "artifacts" / "frame"
    database = run / "scratch.db"
    runtime = run / "runtime"
    if destination == "live":
        database = checkout / "data/database.db"
    elif destination == "external":
        database = tmp_path / "other/database.db"
    else:
        runtime = tmp_path / "runtime"
    with pytest.raises(ValueError, match="Expected a scratch path"):
        frame.prepare(_unseeded(route), run, database, runtime, checkout)
    assert not database.exists()


@pytest.mark.parametrize("route", ROUTE_KEYS)
def test_frame_accepts_scratch_paths_inside_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, route: str,
) -> None:
    """Positive control: a validator that refuses every path fails here."""
    repo = tmp_path / "checkout"
    monkeypatch.setattr(frame, "REPO", repo)
    run = frame.runs_dir(route) / "candidate"
    assert run == repo / "artifacts" / "frame-check" / route / "candidate"

    # The two paths the launcher itself derives from a run directory. Refusal raises.
    frame.validate_paths(run, run / "database.db", run / "runtime")


@pytest.mark.parametrize("route", ROUTE_KEYS)
def test_frame_refuses_the_live_database_even_inside_the_run(checkout: Path, route: str) -> None:
    """Containment passes here, so only the live-path clause can refuse."""
    live = checkout / "data" / "database.db"

    # With the checkout as the run, the scratch runtime is valid and the database is live.
    frame.validate_paths(checkout, checkout / "scratch.db", checkout / "runtime")
    with pytest.raises(ValueError, match="Expected a scratch path"):
        frame.prepare(_unseeded(route), checkout, live, checkout / "runtime", checkout)
    assert not live.exists()


@pytest.mark.parametrize("fixture_edits", [True, False])
def test_prepare_sets_both_scratch_overrides_before_copying_or_editing_the_seed(
    checkout: Path, monkeypatch: pytest.MonkeyPatch, fixture_edits: bool,
) -> None:
    run = frame.runs_dir("workout_log") / "candidate"
    database, runtime = run / "database.db", run / "runtime"
    calls: list[str] = []
    monkeypatch.setenv("DB_FILE", str(checkout / "other.db"))
    monkeypatch.setenv("HT_RUNTIME_DIR", str(checkout / "other-runtime"))

    def copy(command: list[str], **options: object) -> None:
        assert command[2:] == [
            "--source", str(checkout / "e2e/fixtures/database.visual.seed.db"), "--output", str(database),
        ]
        assert options == {"cwd": checkout, "check": True}
        assert os.environ["DB_FILE"] == str(database)
        assert os.environ["HT_RUNTIME_DIR"] == str(runtime)
        assert os.environ["PW_DB_PATH"] == str(database)
        calls.append("copy")

    def seed(run_path: Path, db_path: Path, source: Path) -> None:
        assert (run_path, db_path, source) == (run, database, checkout)
        assert os.environ["DB_FILE"] == str(database)
        assert os.environ["HT_RUNTIME_DIR"] == str(runtime)
        calls.append("edit")

    monkeypatch.setattr(frame.subprocess, "run", copy)
    route = dataclasses.replace(frame.ROUTES["workout_log"], seed=seed if fixture_edits else None)
    frame.prepare(route, run, database, runtime, checkout)

    assert calls == (["copy", "edit"] if fixture_edits else ["copy"])


def test_launcher_refuses_an_unknown_route_before_seeding(
    checkout: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as refusal:
        frame.main(["--route", "no_such_route"])

    assert refusal.value.code == 2
    assert "invalid choice: 'no_such_route'" in capsys.readouterr().err
    assert not (checkout / "artifacts").exists()


@pytest.mark.parametrize("route", ROUTE_KEYS)
def test_launcher_refuses_a_control_ref_that_is_not_the_routes_own(
    checkout: Path, capsys: pytest.CaptureFixture[str], route: str,
) -> None:
    own = frame.ROUTES[route].control
    others = [ref for ref in CONTROL_REFS if ref != own]
    assert others

    for ref in others:
        with pytest.raises(SystemExit) as refusal:
            frame.main(["--route", route, "--control-ref", ref])
        assert refusal.value.code == 2
        assert f"--control-ref for {route} accepts only {own}" in capsys.readouterr().err
    assert not (checkout / "artifacts").exists()


def test_launcher_refuses_a_route_without_a_control_before_seeding(
    checkout: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    """A check is evidence only if it can be shown to fail, so a row needs its control."""
    monkeypatch.setitem(frame.ROUTES, "bare", dataclasses.replace(frame.ROUTES["workout_log"], control=""))

    with pytest.raises(SystemExit) as refusal:
        frame.main(["--route", "bare"])

    assert refusal.value.code == 2
    assert "route bare has no control ref" in capsys.readouterr().err
    assert not (checkout / "artifacts").exists()


@pytest.mark.parametrize("route", ROUTE_KEYS)
@pytest.mark.parametrize("mode", ["candidate", "control"])
def test_launcher_starts_the_routes_check_on_a_new_run_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
    mode: str, route: str,
) -> None:
    """Positive control for the refusals: a registered route and its own ref do launch."""
    repo = tmp_path / "checkout"
    row = frame.ROUTES[route]
    prepared: list[tuple[object, ...]] = []
    children: list[tuple[list[str], dict[str, object]]] = []

    def child(command: list[str], **options: object) -> None:
        children.append((command, options))
        if command[0] == "git":
            with zipfile.ZipFile(command[command.index("-o") + 1], "w") as archive:
                archive.writestr("app.py", "")

    monkeypatch.setattr(frame, "REPO", repo)
    monkeypatch.setattr(frame, "prepare", lambda *paths: prepared.append(paths))
    monkeypatch.setattr(frame.subprocess, "run", child)
    monkeypatch.setattr(frame.shutil, "which", lambda name: "node")

    frame.main(["--route", route, *(["--control-ref", row.control] if mode == "control" else [])])

    launch, options = children[-1]
    env = options["env"]
    assert isinstance(env, dict)
    run = Path(env["FRAME_RUN"])
    assert run.parent == repo / "artifacts" / "frame-check" / route
    assert run.name.startswith(f"{mode}-")
    assert run.is_dir()
    source = run / "source" if mode == "control" else repo
    assert prepared == [(row, run, run / "database.db", run / "runtime", source)]
    assert env["FRAME_ROUTE"] == route
    assert env["FRAME_CHECK"] == row.check
    assert env["FRAME_SOURCE"] == str(source)
    assert env["FRAME_CONTROL"] == (row.control if mode == "control" else "")
    assert env["FRAME_SERVER"] == str(Path(frame.__file__).resolve())
    assert launch[-3:] == ["test", "--config", str(repo / "e2e/playwright.frame.config.ts")]
    assert options["cwd"] == repo
    exports = [command for command, _ in children if command[0] == "git"]
    if mode == "control":
        # The export is the pinned ref, unpacked inside the run, and the server reads it.
        assert exports == [["git", "archive", "--format=zip", "-o", str(run / "source.zip"), row.control]]
        assert (source / "app.py").is_file()
    else:
        assert exports == []
    assert f"{row.label} evidence: {run}" in capsys.readouterr().out


@pytest.mark.parametrize("route", ROUTE_KEYS)
def test_server_refuses_a_run_outside_its_routes_directory(
    checkout: Path, monkeypatch: pytest.MonkeyPatch, route: str,
) -> None:
    monkeypatch.delenv("FRAME_SOURCE", raising=False)
    monkeypatch.setenv("FRAME_ROUTE", route)
    monkeypatch.setenv("FRAME_RUN", str(checkout / "artifacts" / "frame-check" / "another_route" / "candidate"))

    with pytest.raises(ValueError, match="Unexpected frame run directory"):
        frame.serve()


@pytest.mark.parametrize("route", ROUTE_KEYS)
@pytest.mark.parametrize("control", [False, True])
def test_server_accepts_the_routes_prepared_paths_and_source_before_import(
    checkout: Path, monkeypatch: pytest.MonkeyPatch, route: str, control: bool,
) -> None:
    run = frame.runs_dir(route) / ("control" if control else "candidate")
    source = run / "source" if control else checkout
    settings = {
        "FRAME_ROUTE": route, "FRAME_RUN": str(run), "FRAME_SOURCE": str(source),
        "FRAME_CONTROL": frame.ROUTES[route].control if control else "",
        "DB_FILE": str(run / "database.db"), "HT_RUNTIME_DIR": str(run / "runtime"),
    }
    for key, value in settings.items():
        monkeypatch.setenv(key, value)

    def before_import(index: int, directory: str) -> None:
        assert (index, directory) == (0, str(source))
        raise RuntimeError("ready to import")

    monkeypatch.setattr(frame, "sys", SimpleNamespace(path=SimpleNamespace(insert=before_import)))
    with pytest.raises(RuntimeError, match="ready to import"):
        frame.serve()


@pytest.mark.parametrize("route", ROUTE_KEYS)
@pytest.mark.parametrize(("setting", "value", "message"), [
    ("DB_FILE", "other.db", "Frame server paths differ from the prepared fixture"),
    ("HT_RUNTIME_DIR", "other-runtime", "Frame server paths differ from the prepared fixture"),
    ("FRAME_SOURCE", "source", "Unexpected frame source"),
])
def test_server_refuses_wrong_scratch_paths_before_import(
    checkout: Path, monkeypatch: pytest.MonkeyPatch, route: str, setting: str, value: str, message: str,
) -> None:
    run = frame.runs_dir(route) / "candidate"
    settings = {
        "FRAME_ROUTE": route, "FRAME_RUN": str(run), "FRAME_SOURCE": str(checkout), "FRAME_CONTROL": "",
        "DB_FILE": str(run / "database.db"), "HT_RUNTIME_DIR": str(run / "runtime"),
    }
    settings[setting] = str(run / value)
    for key, path in settings.items():
        monkeypatch.setenv(key, path)

    # No application's module search path should be set up for a refused launch.
    def refuse_import(*args: object) -> None:
        pytest.fail("Unexpected application import")

    monkeypatch.setattr(frame, "sys", SimpleNamespace(path=SimpleNamespace(insert=refuse_import)))
    with pytest.raises(ValueError, match=message):
        frame.serve()


def test_server_refuses_an_unregistered_route(checkout: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FRAME_SOURCE", raising=False)
    monkeypatch.setenv("FRAME_ROUTE", "no_such_route")
    monkeypatch.setenv("FRAME_RUN", str(checkout / "artifacts" / "frame-check" / "no_such_route" / "candidate"))

    with pytest.raises(ValueError, match="Unknown frame route"):
        frame.serve()


def test_log_command_runs_the_log_route_with_its_arguments(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[object, dict[str, object]]] = []
    monkeypatch.setattr(frame, "main", lambda argv=None, **options: calls.append((argv, options)))

    log_command.main(["--control-ref", "5dc83cef"])

    assert calls == [(["--control-ref", "5dc83cef"], {"fixed_route": "workout_log"})]


def test_log_command_cannot_be_pointed_at_another_route(
    checkout: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as refusal:
        log_command.main(["--route", "workout_log"])

    assert refusal.value.code == 2
    assert "unrecognized arguments: --route" in capsys.readouterr().err
    assert not (checkout / "artifacts").exists()


def test_log_command_still_takes_only_the_logs_control_ref(
    checkout: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as refusal:
        log_command.main(["--control-ref", "8b023d1a"])

    assert refusal.value.code == 2
    assert "--control-ref for workout_log accepts only 5dc83cef" in capsys.readouterr().err
    assert not (checkout / "artifacts").exists()


def test_the_log_route_keeps_its_check_its_control_and_its_fixture() -> None:
    log = frame.ROUTES["workout_log"]

    assert (log.label, log.check, log.control) == ("Workout Log", "workout-log-frame.check.ts", "5dc83cef")
    assert log.seed is frame.seed_workout_log


@pytest.mark.parametrize("route", ["weekly_summary", "session_summary", "fatigue"])
def test_summary_and_fatigue_share_the_verified_navigation_control(route):
    row = frame.ROUTES[route]
    assert row.control == "5668cfa3c2d7b6ba1a7c180dd2245e56613b1600"
    assert row.check == "summary-fatigue-frame.check.ts"
    assert row.seed is (frame.seed_fatigue_periods if route == "fatigue" else None)


@pytest.mark.parametrize("route", ROUTE_KEYS)
def test_registered_check_exists_and_stays_out_of_the_default_run(route: str) -> None:
    check = frame.ROUTES[route].check

    assert (E2E / check).is_file(), f"{check} is missing from e2e/"
    assert re.fullmatch(r"[\w-]+\.check\.ts", check), f"{check} is not a .check.ts file in e2e/"
    assert not DEFAULT_TEST_PATTERN.match(check), f"{check} would join the default Playwright run"


@pytest.mark.parametrize("route", ROUTE_KEYS)
def test_registered_check_takes_test_from_the_zero_allowance_fixture(route: str) -> None:
    source = (E2E / frame.ROUTES[route].check).read_text(encoding="utf-8")
    sources = {
        module for names, module in re.findall(r"import\s*\{([^}]*)\}\s*from\s*'([^']+)'", source)
        if re.search(r"(^|[\s,])test([\s,]|$)", names)
    }

    assert sources == {"./strict-fixtures"}


def test_frame_config_selects_one_check_on_its_own_serial_server() -> None:
    config = (E2E / "playwright.frame.config.ts").read_text(encoding="utf-8")

    for pinned in (
        "testMatch: check ?? NO_CHECK",
        "workers: 1",
        "retries: 0",
        "reuseExistingServer: false",
        "export default frameConfig(process.env.FRAME_CHECK);",
    ):
        assert pinned in config, f"playwright.frame.config.ts lost `{pinned}`"

    log_config = (E2E / "playwright.workout-log-frame.config.ts").read_text(encoding="utf-8")
    assert "export default frameConfig('workout-log-frame.check.ts');" in log_config
