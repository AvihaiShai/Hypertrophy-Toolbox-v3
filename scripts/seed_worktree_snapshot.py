"""Operation A worktree seeding only; stdlib SQLite/captured diagnostics exception.

Never imports application configuration, DatabaseHandler or application logging.
The caller verifies source selection. This is not a preservation/cleanup launcher.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import stat
import sys
import tempfile
import time
from typing import Callable


def verified_path(value: str | Path) -> Path:
    """Reject aliases/reparse ancestry, retaining absent destination components."""
    path = Path(value)
    if not path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ValueError(f"An absolute non-aliased path is required: {value}")
    if os.name == "nt":
        if not re.match(r"^[A-Za-z]:[\\/]", str(path)) or ":" in str(path)[2:]:
            raise ValueError(f"Drive-qualified ordinary path required: {path}")
        for part in path.parts[1:]:
            if (part.endswith((".", " ")) or "~" in part or
                    re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", part, re.I)):
                raise ValueError(f"Ambiguous path component: {part}")
    for ancestor in reversed((path, *path.parents)):
        try:
            info = ancestor.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"Reparse/symlink path is not supported: {ancestor}")
    return path


def validate_snapshot(path: Path, deadline: float | None = None) -> dict[str, object]:
    """Read only the completed disposable copy; reject empty/corrupt schemas."""
    with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as db:
        if deadline is not None:
            db.set_progress_handler(lambda: int(time.monotonic() >= deadline), 1000)
        if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise ValueError("Snapshot integrity_check did not return exactly ok")
        version = db.execute("PRAGMA user_version").fetchone()
        schema_version = db.execute("PRAGMA schema_version").fetchone()
        tables = db.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
        if not tables or version is None or schema_version is None:
            raise ValueError("Snapshot has no readable application schema/version")
        for (name,) in tables:
            quoted = str(name).replace('"', '""')
            db.execute(f'SELECT * FROM "{quoted}" LIMIT 1').fetchall()
        if db.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise ValueError("Snapshot foreign key validation failed")
        return {"user_version": version[0], "schema_version": schema_version[0], "tables": len(tables)}


def publish_snapshot(temporary: Path, target: Path) -> None:
    """Same-directory publication; Windows rename refuses an existing target."""
    verified_path(target)
    if temporary.parent != target.parent or temporary.stat().st_dev != target.parent.stat().st_dev:
        raise ValueError("Publication must stay in the verified destination directory/volume")
    if os.name == "nt":
        os.rename(temporary, target)  # MoveFileEx without REPLACE_EXISTING.
    else:
        os.link(temporary, target)  # Atomic no-overwrite on POSIX, including a late collision.
        temporary.unlink()


def snapshot_database(source: str | Path, target: str | Path, timeout_seconds: float = 30,
                      *, boundary: Callable[[str], None] | None = None) -> dict[str, object]:
    source_path, target_path = verified_path(source), verified_path(target)
    if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive and finite")
    if source_path == target_path or target_path.exists():
        raise FileExistsError("Source/target alias or destination collision")
    source_info = source_path.stat()
    if not source_path.is_file() or source_info.st_nlink != 1:
        raise ValueError("Source must be an ordinary file with exactly one link")
    if not target_path.parent.is_dir():
        raise ValueError("Verified target directory must already exist")
    deadline = time.monotonic() + timeout_seconds

    def checkpoint(name: str) -> None:
        if boundary is not None:
            boundary(name)
        if time.monotonic() >= deadline:
            raise TimeoutError("SQLite snapshot exceeded its total deadline")

    def progress(_status: int, _remaining: int, _total: int) -> None:
        checkpoint("backup_progress")

    fd, filename = tempfile.mkstemp(prefix=".worktree-seed-", suffix=".db", dir=target_path.parent)
    temporary = Path(filename)
    os.close(fd)
    try:
        checkpoint("before_backup")
        verified_path(source_path)
        if source_path.stat() != source_info:
            # WAL writers can alter mtime without changing identity: compare identity only.
            current = source_path.stat()
            if (current.st_dev, current.st_ino) != (source_info.st_dev, source_info.st_ino):
                raise ValueError("Source identity changed before opening")
        with closing(sqlite3.connect(source_path.as_uri() + "?mode=ro", uri=True,
                                     timeout=min(timeout_seconds, 0.1))) as origin:
            with closing(sqlite3.connect(temporary)) as destination:
                origin.backup(destination, pages=64, progress=progress, sleep=0.025)
        checkpoint("after_backup")
        checkpoint("before_validation")
        validation = validate_snapshot(temporary, deadline)
        checkpoint("after_validation")
        with temporary.open("r+b") as completed:
            os.fsync(completed.fileno())
        checkpoint("before_publish")
        publish_snapshot(temporary, target_path)
        checkpoint("after_publish")
        return {"ok": True, "source": str(source_path), "target": str(target_path),
                "sourceIdentity": f"{source_info.st_dev}:{source_info.st_ino}",
                "targetIdentity": f"{target_path.stat().st_dev}:{target_path.stat().st_ino}",
                "validation": validation}
    except BaseException as exc:
        # Retain only newly owned scratch. Never touch source family or a collision.
        print(json.dumps({"ok": False, "error": str(exc), "source": str(source_path),
                          "target": str(target_path), "retainedScratch": str(temporary) if temporary.exists() else None}), file=sys.stderr)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=30)
    args = parser.parse_args()
    try:
        print(json.dumps(snapshot_database(args.source, args.target, args.timeout_seconds)))
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
