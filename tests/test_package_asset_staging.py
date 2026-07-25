"""Contracts for the tracked-asset staging manifest that feeds PyInstaller."""
from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

import pytest

from scripts.stage_package_assets import (
    ASSET_ROOTS,
    STAGING_RELATIVE,
    StagingError,
    _reject_case_collisions,
    _reject_repository_metadata,
    staged_datas,
    sync_staging_tree,
    tracked_assets,
    verify_staging_tree,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

# One reviewed asset per packaged category. Fonts are absent on purpose: the
# repository tracks no font files, so the manifest cannot ship one.
REQUIRED_ASSETS = {
    "template": "templates/base.html",
    "template partial": "templates/partials/_volume_controls.html",
    "css": "static/css/base.css",
    "vendored css": "static/css/bootstrap.custom.min.css",
    "js entrypoint": "static/js/app.js",
    "js module": "static/js/modules/fetch-wrapper.js",
    "favicon": "static/images/favicon.ico",
    "image": "static/images/icons8-session-50.png",
    "body map": "static/bodymaps/hypertrophy-advanced/body_anterior.svg",
    "vendor catalog": "static/vendor/free-exercise-db/exercises.json",
    "vendor license": "static/vendor/free-exercise-db/LICENSE",
    "vendor notice": "static/vendor/musclemap/NOTICE.md",
    "vendor version": "static/vendor/musclemap/VERSION",
    "exercise media": (
        "static/vendor/free-exercise-db/exercises/Barbell_Squat/0.jpg"
    ),
}


def _run_git(repo_root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


@pytest.fixture
def asset_repo(tmp_path: Path) -> Path:
    """A miniature repository with tracked, ignored, and untracked assets."""
    repo = tmp_path / "repo"
    (repo / "static" / "css").mkdir(parents=True)
    (repo / "static" / "bodymaps" / "GPT" / ".git").mkdir(parents=True)
    (repo / "templates").mkdir()

    (repo / ".gitignore").write_text(
        "static/bodymaps/GPT/\n*.tmp\n", encoding="utf-8"
    )
    (repo / "static" / "css" / "base.css").write_text("a{}", encoding="utf-8")
    (repo / "templates" / "base.html").write_text("<html>", encoding="utf-8")
    (repo / "static" / "bodymaps" / "GPT" / "scratch.png").write_bytes(b"x")
    (repo / "static" / "bodymaps" / "GPT" / ".git" / "config").write_text(
        "[core]", encoding="utf-8"
    )
    (repo / "static" / "css" / "local.tmp").write_text("junk", encoding="utf-8")
    (repo / "templates" / "untracked.html").write_text("<p>", encoding="utf-8")

    _run_git(repo, "init", "-q")
    _run_git(repo, "config", "user.email", "test@example.com")
    _run_git(repo, "config", "user.name", "Test")
    _run_git(repo, "add", "static/css/base.css", "templates/base.html")
    _run_git(repo, "commit", "-qm", "assets")
    return repo


def test_manifest_is_exactly_the_tracked_asset_set():
    manifest = tracked_assets(REPO_ROOT)
    tracked = {
        line.replace("\\", "/")
        for line in _run_git(
            REPO_ROOT, "ls-files", "--", *ASSET_ROOTS
        ).splitlines()
    }

    assert set(manifest) == tracked
    assert manifest == sorted(manifest)
    assert len(manifest) == len(set(manifest))


def test_manifest_covers_every_packaged_asset_category():
    manifest = set(tracked_assets(REPO_ROOT))

    missing = {
        category: path
        for category, path in REQUIRED_ASSETS.items()
        if path not in manifest
    }
    assert not missing

    fonts = [
        path
        for path in manifest
        if path.endswith((".woff", ".woff2", ".ttf", ".otf", ".eot"))
    ]
    assert fonts == []


def test_manifest_carries_no_repository_metadata():
    manifest = tracked_assets(REPO_ROOT)

    assert not [path for path in manifest if ".git" in path.split("/")]


def test_ignored_and_untracked_assets_cannot_be_staged(
    asset_repo: Path, tmp_path: Path
):
    staging_root = tmp_path / "staging"
    manifest = sync_staging_tree(asset_repo, staging_root)

    assert manifest == ["static/css/base.css", "templates/base.html"]

    staged = {
        path.relative_to(staging_root).as_posix()
        for path in staging_root.rglob("*")
        if path.is_file()
    }
    assert staged == set(manifest)
    assert not list(staging_root.rglob("*.tmp"))
    assert not (staging_root / "static" / "bodymaps").exists()
    assert not (staging_root / "templates" / "untracked.html").exists()


def test_staging_fails_when_a_tracked_asset_is_missing(
    asset_repo: Path, tmp_path: Path
):
    (asset_repo / "templates" / "base.html").unlink()

    with pytest.raises(StagingError, match="missing from the working copy"):
        sync_staging_tree(asset_repo, tmp_path / "staging")


def test_staging_fails_outside_a_git_checkout(tmp_path: Path):
    plain = tmp_path / "plain"
    (plain / "static").mkdir(parents=True)
    (plain / "static" / "base.css").write_text("a{}", encoding="utf-8")

    with pytest.raises((StagingError, subprocess.CalledProcessError)):
        sync_staging_tree(plain, tmp_path / "staging")


def test_restaging_prunes_files_that_left_the_manifest(
    asset_repo: Path, tmp_path: Path
):
    staging_root = tmp_path / "staging"
    sync_staging_tree(asset_repo, staging_root)
    stale = staging_root / "static" / "css" / "stale.css"
    stale.write_text("b{}", encoding="utf-8")
    (staging_root / "static" / "leaked").mkdir()
    (staging_root / "static" / "leaked" / "secret.png").write_bytes(b"x")

    sync_staging_tree(asset_repo, staging_root)

    assert not stale.exists()
    assert not (staging_root / "static" / "leaked").exists()


def test_verification_rejects_a_divergent_staging_tree(
    asset_repo: Path, tmp_path: Path
):
    staging_root = tmp_path / "staging"
    manifest = sync_staging_tree(asset_repo, staging_root)

    (staging_root / "static" / "css" / "injected.css").write_text(
        "c{}", encoding="utf-8"
    )
    with pytest.raises(StagingError, match="unexpected: "):
        verify_staging_tree(asset_repo, staging_root, manifest)

    (staging_root / "static" / "css" / "injected.css").unlink()
    (staging_root / "templates" / "base.html").unlink()
    with pytest.raises(StagingError, match="missing: "):
        verify_staging_tree(asset_repo, staging_root, manifest)


def test_verification_rejects_altered_staged_content(
    asset_repo: Path, tmp_path: Path
):
    staging_root = tmp_path / "staging"
    manifest = sync_staging_tree(asset_repo, staging_root)
    (staging_root / "static" / "css" / "base.css").write_text(
        "a{color:red}", encoding="utf-8"
    )

    with pytest.raises(StagingError, match="size: static/css/base.css"):
        verify_staging_tree(asset_repo, staging_root, manifest)


def test_staged_datas_map_tracked_paths_to_package_destinations(
    asset_repo: Path, tmp_path: Path
):
    staging_root = tmp_path / "staging"

    datas = staged_datas(asset_repo, staging_root)

    assert datas == [
        ((staging_root / "static/css/base.css").as_posix(), "static/css"),
        ((staging_root / "templates/base.html").as_posix(), "templates"),
    ]
    for source, _ in datas:
        assert Path(source).is_file()


@pytest.mark.skipif(
    os.name == "nt", reason="Windows filesystems carry no executable bit"
)
def test_executable_bit_survives_staging(asset_repo: Path, tmp_path: Path):
    hook = asset_repo / "static" / "hook.sh"
    hook.write_text("#!/bin/sh\n", encoding="utf-8")
    hook.chmod(0o755)
    _run_git(asset_repo, "add", "static/hook.sh")
    _run_git(asset_repo, "commit", "-qm", "hook")
    staging_root = tmp_path / "staging"

    sync_staging_tree(asset_repo, staging_root)

    assert (staging_root / "static" / "hook.sh").stat().st_mode & stat.S_IXUSR


def test_staging_refuses_to_prune_a_checkout(asset_repo: Path):
    """Pruning a staging root that contains the repository would delete it."""
    with pytest.raises(StagingError, match="Refusing to stage over a checkout"):
        sync_staging_tree(asset_repo, asset_repo)

    with pytest.raises(StagingError, match="Refusing to stage over a checkout"):
        sync_staging_tree(asset_repo, asset_repo.parent)


def test_case_colliding_assets_are_rejected():
    """A case-insensitive filesystem would silently merge these two files."""
    with pytest.raises(StagingError, match="differ only by case"):
        _reject_case_collisions(["static/css/Base.css", "static/css/base.css"])


def test_gitlinked_repository_metadata_is_rejected():
    with pytest.raises(StagingError, match="Repository metadata"):
        _reject_repository_metadata(["static/vendor/thing/.git/config"])


def test_spec_default_staging_root_is_ignored_build_output():
    assert STAGING_RELATIVE.parts[0] == "build"
    assert (
        "build/"
        in (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    )
