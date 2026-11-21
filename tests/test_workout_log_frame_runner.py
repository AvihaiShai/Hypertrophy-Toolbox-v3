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
