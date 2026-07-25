"""Stage packaged UI assets from the tracked-file manifest.

PyInstaller used to walk ``static/`` and ``templates/`` off the filesystem, so
any ignored or untracked working-copy file could reach the distribution and had
to be subtracted by name. The manifest comes from ``git ls-files`` instead, and
the build reads a staging tree rebuilt from it: untracked content cannot enter
the package by construction rather than by exclusion.

Staged content is compared by SHA-256. Size and mtime agree on a file that was
rewritten in place at the same length with its timestamp restored, which is what
a timestamp-preserving tool, an unlucky partial write, and deliberate tampering
all look like.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
import subprocess
from pathlib import Path


ASSET_ROOTS = ("static", "templates")
STAGING_RELATIVE = Path("build") / "package-assets"
DIGEST_FILENAME = "manifest.sha256"
_DIGEST_CHUNK = 1024 * 1024


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


def file_digest(path: Path) -> str:
    """Return the SHA-256 of *path* as lowercase hex."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(_DIGEST_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _needs_copy(source: Path, target: Path) -> bool:
    """Decide whether *target* must be recopied from *source*.

    Restaging is self-healing on purpose: a staged file that diverged for any
    reason is replaced rather than reported, so a stale staging tree cannot
    poison every later build. ``verify_staging_tree`` is where divergence is
    fatal.
    """
    if not target.exists():
        return True
    if source.stat().st_size != target.stat().st_size:
        return True
    return file_digest(source) != file_digest(target)


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
    # Staging prunes whatever the manifest does not name, so a --staging-root
    # containing the checkout would delete the checkout.
    if repo_root.resolve().is_relative_to(staging_root.resolve()):
        raise StagingError(
            f"Refusing to stage over a checkout: {staging_root.resolve()}"
        )

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
    write_digest_manifest(staging_root, manifest)
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
        # Recomputed rather than reused from the copy decision: evidence that
        # shares a failure mode with the thing it certifies is not evidence.
        elif file_digest(source) != file_digest(target):
            mismatched.append(f"  content: {relative}")
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


def digest_manifest_path(staging_root: Path) -> Path:
    """Return the digest record's path: beside the staging root, never inside.

    The staged tree must keep matching the manifest exactly, so a record of it
    stored inside would be pruned as an unexpected file.
    """
    return staging_root.parent / DIGEST_FILENAME


def write_digest_manifest(staging_root: Path, manifest: list[str]) -> Path:
    """Record staged digests in ``sha256sum`` format and return the path."""
    lines = [
        f"{file_digest(staging_root / relative)}  {relative}"
        for relative in manifest
    ]
    target = digest_manifest_path(staging_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    # newline="\n" explicitly: Windows text mode would emit CRLF, and
    # `sha256sum -c` then looks for paths with a trailing carriage return.
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    return target


def read_digest_manifest(digest_path: Path) -> dict[str, str]:
    """Parse a ``sha256sum``-format record into ``{relative path: digest}``."""
    recorded = {}
    for number, line in enumerate(
        digest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        digest, separator, relative = line.partition("  ")
        if not separator or len(digest) != 64:
            raise StagingError(
                f"Malformed digest record at {digest_path}:{number}: {line!r}"
            )
        recorded[relative] = digest
    return recorded


def verify_against_digest_manifest(
    tree_root: Path,
    digest_path: Path,
) -> list[str]:
    """Fail unless every recorded asset is present under *tree_root* and intact.

    Runs against a staging tree or a built distribution, so a reviewer — or the
    frozen build gate — can check a distribution without the source it came
    from. Returns the verified paths.
    """
    recorded = read_digest_manifest(digest_path)
    if not recorded:
        raise StagingError(f"Digest record is empty: {digest_path}")

    failures = []
    for relative, expected in recorded.items():
        candidate = tree_root / relative
        if not candidate.is_file():
            failures.append(f"  missing: {relative}")
        elif file_digest(candidate) != expected:
            failures.append(f"  content: {relative}")
    if failures:
        raise StagingError(
            f"Tree at {tree_root} does not match {digest_path}:\n"
            + "\n".join(failures)
        )
    return sorted(recorded)


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
    parser.add_argument(
        "--verify-tree",
        type=Path,
        default=None,
        help=(
            "Verify an already-built tree (e.g. a distribution's _internal/) "
            "against a recorded digest manifest instead of staging."
        ),
    )
    parser.add_argument(
        "--digest-manifest",
        type=Path,
        default=None,
        help="Digest record for --verify-tree. Defaults beside --staging-root.",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    staging_root = args.staging_root or (repo_root / STAGING_RELATIVE)

    if args.verify_tree is not None:
        digest_path = args.digest_manifest or digest_manifest_path(staging_root)
        try:
            verified = verify_against_digest_manifest(
                args.verify_tree, digest_path
            )
        except (StagingError, OSError) as exc:
            raise SystemExit(f"[ASSET STAGING] ERROR: {exc}") from exc
        print(
            f"[ASSET STAGING] verified {len(verified)} files in "
            f"{args.verify_tree} against {digest_path}"
        )
        return

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
    print(
        "[ASSET STAGING] digests recorded in "
        f"{digest_manifest_path(staging_root)}"
    )


if __name__ == "__main__":
    main()
