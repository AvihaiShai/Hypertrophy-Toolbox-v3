"""Fail closed when package asset trees contain unreviewed local files."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ALLOWED_LOCAL_ASSETS = {("!!", "static/bodymaps/GPT/")}
ASSET_ROOTS = ("static", "templates")


def inventory_local_assets(repo_root: Path) -> list[tuple[str, str]]:
    """Return ignored and untracked entries below the packaged asset roots."""
    result = subprocess.run(
        [
            "git",
            "status",
            "--ignored",
            "--porcelain=v1",
            "--",
            *ASSET_ROOTS,
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    entries = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        status = line[:2]
        if status in {"??", "!!"}:
            entries.append((status, line[3:].replace("\\", "/")))
    return entries


def validate_package_assets(repo_root: Path) -> None:
    """Raise when the package could consume an unreviewed local asset."""
    entries = inventory_local_assets(repo_root)
    unexpected = sorted(set(entries) - ALLOWED_LOCAL_ASSETS)
    if unexpected:
        formatted = "\n".join(
            f"  {status} {path}" for status, path in unexpected
        )
        raise RuntimeError(
            "Unreviewed ignored/untracked package assets found:\n"
            f"{formatted}\n"
            "Track, remove, or explicitly review the files before building."
        )

    for status, path in entries:
        print(f"[ASSET GUARD] allowed excluded path: {status} {path}")
    print("[ASSET GUARD] static/ and templates/ inventory approved")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    try:
        validate_package_assets(args.repo_root.resolve())
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"[ASSET GUARD] ERROR: {exc}") from exc


if __name__ == "__main__":
    main()
