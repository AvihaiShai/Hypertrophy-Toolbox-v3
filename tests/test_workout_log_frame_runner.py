from pathlib import Path

import pytest

from e2e.scripts import run_workout_log_frame as frame


@pytest.mark.parametrize("destination", ["live", "external", "runtime-outside"])
def test_frame_refuses_unsafe_path_before_seed_or_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, destination: str,
) -> None:
    repo = tmp_path / "checkout"
    monkeypatch.setattr(frame, "REPO", repo)
    run = repo / "artifacts" / "frame"
    database = run / "scratch.db"
    runtime = run / "runtime"
    if destination == "live":
        database = repo / "data/database.db"
    elif destination == "external":
        database = tmp_path / "other/database.db"
    else:
        runtime = tmp_path / "runtime"
    monkeypatch.setattr(frame.subprocess, "run", lambda *a, **kw: pytest.fail("Unexpected child launch"))
    with pytest.raises(ValueError, match="Expected a scratch path"):
        frame.prepare(run, database, runtime, repo)
    assert not database.exists()


def test_frame_accepts_scratch_paths_inside_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Positive control: a validator that refuses every path fails here."""
    repo = tmp_path / "checkout"
    monkeypatch.setattr(frame, "REPO", repo)
    run = repo / "artifacts" / "workout-log-frame" / "candidate"

    # The two paths the launcher itself derives from a run directory. Refusal raises.
    frame.validate_paths(run, run / "database.db", run / "runtime")


def test_frame_refuses_the_live_database_even_inside_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Containment passes here, so only the live-path clause can refuse."""
    repo = tmp_path / "checkout"
    monkeypatch.setattr(frame, "REPO", repo)
    live = repo / "data" / "database.db"

    def refuse_launch(*args: object, **kwargs: object) -> None:
        pytest.fail("Unexpected child launch")

    monkeypatch.setattr(frame.subprocess, "run", refuse_launch)
    # With the checkout as the run, the scratch runtime is valid and the database is live.
    frame.validate_paths(repo, repo / "scratch.db", repo / "runtime")
    with pytest.raises(ValueError, match="Expected a scratch path"):
        frame.prepare(repo, live, repo / "runtime", repo)
    assert not live.exists()
