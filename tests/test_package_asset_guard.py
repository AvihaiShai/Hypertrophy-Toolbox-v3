"""Fail-closed behavior for recursive static/template package inputs."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "guard_package_assets.py"
)


def _init_repo(path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    (path / "static" / "bodymaps" / "GPT").mkdir(parents=True)
    (path / "templates").mkdir()
    (path / ".gitignore").write_text(
        "static/bodymaps/GPT/\n*.tmp\n",
        encoding="utf-8",
    )
    (path / "static" / "tracked.txt").write_text("tracked", encoding="utf-8")
    (path / "static" / "bodymaps" / "tracked.svg").write_text(
        "tracked",
        encoding="utf-8",
    )
    (path / "templates" / "tracked.html").write_text(
        "tracked",
        encoding="utf-8",
    )
    subprocess.run(
        [
            "git",
            "add",
            ".gitignore",
            "static/tracked.txt",
            "static/bodymaps/tracked.svg",
            "templates/tracked.html",
        ],
        cwd=path,
        check=True,
    )


def _run_guard(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(path)],
        capture_output=True,
        text=True,
    )


def test_guard_allows_only_the_explicitly_excluded_gpt_root(tmp_path):
    _init_repo(tmp_path)
    scratch = tmp_path / "static" / "bodymaps" / "GPT" / "scratch.png"
    scratch.write_bytes(b"scratch")

    result = _run_guard(tmp_path)

    assert result.returncode == 0, result.stderr
    assert "static/bodymaps/GPT/" in result.stdout


def test_guard_fails_closed_on_synthetic_ignored_asset(tmp_path):
    _init_repo(tmp_path)
    unexpected = tmp_path / "static" / "unexpected.tmp"
    unexpected.write_text("private", encoding="utf-8")

    result = _run_guard(tmp_path)

    assert result.returncode != 0
    assert "static/unexpected.tmp" in result.stderr
