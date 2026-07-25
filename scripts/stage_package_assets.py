"""Stage packaged UI assets from the tracked-file manifest.

PyInstaller used to walk ``static/`` and ``templates/`` off the filesystem, so
any ignored or untracked working-copy file could reach the distribution and had
to be subtracted by name. The manifest comes from ``git ls-files`` instead, and
the build reads a staging tree rebuilt from it: untracked content cannot enter
the package by construction rather than by exclusion.
"""
from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
from pathlib import Path


ASSET_ROOTS = ("static", "templates")
STAGING_RELATIVE = Path("build") / "package-assets"


class StagingError(RuntimeError):
    """Raised when the staged tree cannot be proven to match tracked sources."""


def tracked_assets(repo_root: Path) -> list[str]:
    """Return the sorted, POSIX-relative manifest of tracked packaged assets."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", *ASSET_ROOTS],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    manifest = sorted(
        entry.replace("\\", "/")
        for entry in result.stdout.split("\0")
        if entry
    )
    if not manifest:
        raise StagingError(
            f"No tracked assets found under {'/, '.join(ASSET_ROOTS)}/ in "
            f"{repo_root}. Build from a git checkout of the repository."
        )
    _reject_repository_metadata(manifest)
    _reject_case_collisions(manifest)
    return manifest


def _reject_repository_metadata(manifest: list[str]) -> None:
    nested = [path for path in manifest if ".git" in path.split("/")]
    if nested:
        raise StagingError(
            "Repository metadata cannot be packaged:\n"
            + "\n".join(f"  {path}" for path in nested)
        )


def _reject_case_collisions(manifest: list[str]) -> None:
    """Fail on paths that differ only by case; they collide when staged."""
    seen: dict[str, str] = {}
    collisions = []
    for path in manifest:
        previous = seen.setdefault(path.lower(), path)
        if previous != path:
            collisions.append(f"  {previous}\n  {path}")
    if collisions:
        raise StagingError(
            "Tracked assets differ only by case and cannot stage on a "
            "case-insensitive filesystem:\n" + "\n".join(collisions)
        )


def _needs_copy(source: Path, target: Path) -> bool:
    if not target.exists():
        return True
    source_stat = source.stat()
    target_stat = target.stat()
    return (
        source_stat.st_size != target_stat.st_size
        or int(source_stat.st_mtime) != int(target_stat.st_mtime)
    )


def _prune_staging_tree(staging_root: Path, wanted: set[str]) -> None:
    """Delete staged files and directories no longer in the manifest."""
    if not staging_root.exists():
        return
    for path in sorted(staging_root.rglob("*"), reverse=True):
        if path.is_file():
            if path.relative_to(staging_root).as_posix() not in wanted:
                path.unlink()
        elif path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def sync_staging_tree(repo_root: Path, staging_root: Path) -> list[str]:
    """Rebuild the staging tree from tracked sources and return the manifest."""
    manifest = tracked_assets(repo_root)
    for relative in manifest:
        source = repo_root / relative
        if not source.is_file():
            raise StagingError(
                f"Tracked asset is missing from the working copy: {relative}"
            )
        target = staging_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if _needs_copy(source, target):
            # copy2 carries mode bits and mtime, so the executable bit and the
            # incremental comparison above both survive a restage.
            shutil.copy2(source, target)
    _prune_staging_tree(staging_root, set(manifest))
    verify_staging_tree(repo_root, staging_root, manifest)
    return manifest


def verify_staging_tree(
    repo_root: Path,
    staging_root: Path,
    manifest: list[str],
) -> None:
    """Fail unless the staged tree is exactly the tracked source set."""
    staged = {
        path.relative_to(staging_root).as_posix()
        for path in staging_root.rglob("*")
        if path.is_file()
    }
    expected = set(manifest)
    missing = sorted(expected - staged)
    unexpected = sorted(staged - expected)
    if missing or unexpected:
        raise StagingError(
            "Staged asset tree does not match the tracked manifest.\n"
            + "".join(f"  missing: {path}\n" for path in missing)
            + "".join(f"  unexpected: {path}\n" for path in unexpected)
        )

    mismatched = []
    for relative in manifest:
        source = repo_root / relative
        target = staging_root / relative
        if source.stat().st_size != target.stat().st_size:
            mismatched.append(f"  size: {relative}")
        elif os.name != "nt" and (
            stat.S_IMODE(source.stat().st_mode) & stat.S_IXUSR
            != stat.S_IMODE(target.stat().st_mode) & stat.S_IXUSR
        ):
            mismatched.append(f"  executable bit: {relative}")
    if mismatched:
        raise StagingError(
            "Staged assets differ from tracked sources:\n"
            + "\n".join(mismatched)
        )


def staged_datas(
    repo_root: Path,
    staging_root: Path | None = None,
) -> list[tuple[str, str]]:
    """Return PyInstaller ``datas`` entries for the verified staging tree."""
    staging_root = staging_root or (repo_root / STAGING_RELATIVE)
    manifest = sync_staging_tree(repo_root, staging_root)
    return [
        (
            (staging_root / relative).as_posix(),
            str(Path(relative).parent.as_posix()),
        )
        for relative in manifest
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--staging-root", type=Path, default=None)
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print the manifest instead of a per-root summary.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    staging_root = args.staging_root or (repo_root / STAGING_RELATIVE)
    try:
        manifest = sync_staging_tree(repo_root, staging_root)
    except (StagingError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"[ASSET STAGING] ERROR: {exc}") from exc

    if args.list:
        for relative in manifest:
            print(relative)
        return
    for root in ASSET_ROOTS:
        count = sum(1 for path in manifest if path.startswith(f"{root}/"))
        print(f"[ASSET STAGING] {root}/: {count} tracked files")
    print(f"[ASSET STAGING] staged {len(manifest)} files into {staging_root}")


if __name__ == "__main__":
    main()
