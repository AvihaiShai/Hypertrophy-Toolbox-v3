"""Contracts for the tracked-asset staging manifest that feeds PyInstaller."""
from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

from scripts.stage_package_assets import (
    ASSET_ROOTS,
    DIGEST_FILENAME,
    STAGING_RELATIVE,
    StagingError,
    _reject_case_collisions,
    _reject_repository_metadata,
    digest_manifest_path,
    file_digest,
    read_digest_manifest,
    staged_datas,
    sync_staging_tree,
    tracked_assets,
    verify_against_digest_manifest,
    verify_staging_tree,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

# One reviewed asset per packaged category. Font Awesome is deliberately local
# so packaged and visual runs do not depend on cross-origin CDN font requests.
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
    "Font Awesome brands": (
        "static/vendor/fontawesome/webfonts/fa-brands-400.woff2"
    ),
    "Font Awesome regular": (
        "static/vendor/fontawesome/webfonts/fa-regular-400.woff2"
    ),
    "Font Awesome solid": (
        "static/vendor/fontawesome/webfonts/fa-solid-900.woff2"
    ),
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

    fonts = sorted(
        path
        for path in manifest
        if path.endswith((".woff", ".woff2", ".ttf", ".otf", ".eot"))
    )
    expected_fonts = sorted(
        path
        for category, path in REQUIRED_ASSETS.items()
        if category.startswith("Font Awesome")
    )
    assert fonts == expected_fonts


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


def _mutate_preserving_size_and_mtime(path: Path, replacement: bytes) -> None:
    """Rewrite *path* at its original length with its original timestamps."""
    original = path.stat()
    assert len(replacement) == original.st_size, "test must preserve size"
    path.write_bytes(replacement)
    os.utime(path, (original.st_atime, original.st_mtime))


def test_equal_size_equal_mtime_mutation_is_detected_and_repaired(
    asset_repo: Path, tmp_path: Path
):
    """The regression this packet exists for.

    Size and integer mtime both agree on a staged file rewritten in place at
    the same length with its timestamp restored, so the previous comparison
    neither recopied nor rejected it.
    """
    staging_root = tmp_path / "staging"
    manifest = sync_staging_tree(asset_repo, staging_root)
    staged = staging_root / "static" / "css" / "base.css"
    source = asset_repo / "static" / "css" / "base.css"
    _mutate_preserving_size_and_mtime(staged, b"b{}")

    assert staged.stat().st_size == source.stat().st_size
    assert int(staged.stat().st_mtime) == int(source.stat().st_mtime)

    with pytest.raises(StagingError, match="content: static/css/base.css"):
        verify_staging_tree(asset_repo, staging_root, manifest)

    # Restaging repairs it: a diverged staging tree must not be able to wedge
    # every later build.
    sync_staging_tree(asset_repo, staging_root)

    assert staged.read_bytes() == source.read_bytes()
    verify_staging_tree(asset_repo, staging_root, manifest)


def test_digest_manifest_records_every_staged_asset(
    asset_repo: Path, tmp_path: Path
):
    staging_root = tmp_path / "staging"
    manifest = sync_staging_tree(asset_repo, staging_root)

    recorded = read_digest_manifest(digest_manifest_path(staging_root))

    assert sorted(recorded) == manifest
    for relative, digest in recorded.items():
        assert digest == file_digest(asset_repo / relative)


def test_digest_manifest_is_stored_beside_the_staging_tree(
    asset_repo: Path, tmp_path: Path
):
    """Inside the tree it would be pruned as an unexpected file."""
    staging_root = tmp_path / "staging"
    manifest = sync_staging_tree(asset_repo, staging_root)

    digest_path = digest_manifest_path(staging_root)
    assert digest_path == tmp_path / DIGEST_FILENAME
    assert not list(staging_root.rglob(DIGEST_FILENAME))
    verify_staging_tree(asset_repo, staging_root, manifest)


def test_digest_manifest_is_sha256sum_verifiable(
    asset_repo: Path, tmp_path: Path
):
    staging_root = tmp_path / "staging"
    sync_staging_tree(asset_repo, staging_root)

    lines = (
        digest_manifest_path(staging_root)
        .read_text(encoding="utf-8")
        .splitlines()
    )

    assert lines == [
        f"{file_digest(asset_repo / 'static/css/base.css')}  "
        "static/css/base.css",
        f"{file_digest(asset_repo / 'templates/base.html')}  "
        "templates/base.html",
    ]


def test_digest_manifest_uses_lf_endings(asset_repo: Path, tmp_path: Path):
    """Windows text mode would emit CRLF and break `sha256sum -c`."""
    staging_root = tmp_path / "staging"
    sync_staging_tree(asset_repo, staging_root)

    raw = digest_manifest_path(staging_root).read_bytes()

    assert b"\r" not in raw
    assert raw.endswith(b"\n")


def test_built_tree_verification_detects_tampering(
    asset_repo: Path, tmp_path: Path
):
    """A distribution can be checked without the source it was built from."""
    staging_root = tmp_path / "staging"
    sync_staging_tree(asset_repo, staging_root)
    digest_path = digest_manifest_path(staging_root)
    built = tmp_path / "dist" / "_internal"
    shutil.copytree(staging_root, built)

    assert verify_against_digest_manifest(built, digest_path) == [
        "static/css/base.css",
        "templates/base.html",
    ]

    _mutate_preserving_size_and_mtime(built / "static" / "css" / "base.css", b"b{}")
    with pytest.raises(StagingError, match="content: static/css/base.css"):
        verify_against_digest_manifest(built, digest_path)

    (built / "static" / "css" / "base.css").unlink()
    with pytest.raises(StagingError, match="missing: static/css/base.css"):
        verify_against_digest_manifest(built, digest_path)


def test_malformed_digest_records_are_rejected(tmp_path: Path):
    digest_path = tmp_path / DIGEST_FILENAME

    digest_path.write_text("not-a-digest  static/css/base.css\n", encoding="utf-8")
    with pytest.raises(StagingError, match="Malformed digest record"):
        verify_against_digest_manifest(tmp_path, digest_path)

    digest_path.write_text("", encoding="utf-8")
    with pytest.raises(StagingError, match="Digest record is empty"):
        verify_against_digest_manifest(tmp_path, digest_path)


def test_spec_default_staging_root_is_ignored_build_output():
    assert STAGING_RELATIVE.parts[0] == "build"
    assert (
        "build/"
        in (REPO_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    )
