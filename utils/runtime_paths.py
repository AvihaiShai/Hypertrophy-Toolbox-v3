"""Single owner of every mutable runtime path.

Before this module, "where does state live" was answered independently by
``utils/config.py`` (from its own ``__file__``), ``utils/database.py`` (from
``DB_FILE``), and ``utils/auto_backup.py`` (from the database's parent). Three
answers that happened to agree is not one policy, and a frozen build made them
disagree: the installation directory is not writable in general, yet that is
where all three pointed.

Precedence, highest first:

1. ``DB_FILE`` — absolute authority over the database path alone. Resolved in
   ``utils/config.py``; this module never overrides or infers from it.
2. ``HT_RUNTIME_DIR`` — relocates the whole runtime tree in one move. The
   supported answer for portable installs and for a launcher that wants a
   per-worktree root.
3. Frozen build — a per-user OS application-data directory. Local rather than
   roaming on Windows: a SQLite database should not be synchronized between
   machines by a roaming profile.
4. Source checkout or worktree — the repository, exactly as before.

**Packet B1 deliberately does not move the database.** ``runtime_database_path``
is computed and tested, and nothing reads it yet; ``legacy_database_path`` is
what ``DB_FILE`` still defaults to. Switching a frozen install to the new path
while migration does not yet exist would hand an upgrading user a freshly seeded
empty database while their real data sat untouched at the old one. Packet B2
activates the switch atomically with that migration, and
``tests/test_runtime_paths.py`` fails if the switch happens early.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

RUNTIME_ROOT_ENV = "HT_RUNTIME_DIR"

# Windows and macOS convention is a display-cased directory; XDG is lowercase.
APP_DIRECTORY_NAME = "HypertrophyToolbox"
APP_DIRECTORY_NAME_XDG = "hypertrophy-toolbox"

DATABASE_FILENAME = "database.db"
DATA_DIRNAME = "data"
LOGS_DIRNAME = "logs"


def is_frozen() -> bool:
    """Whether this process is a PyInstaller build rather than a checkout."""
    return bool(getattr(sys, "frozen", False))


def installation_root() -> Path:
    """The directory holding immutable application assets.

    Frozen builds resolve to the bundle (``_internal/``) because that is where
    packaged data lands; checkouts resolve to the repository.
    """
    return Path(__file__).resolve().parents[1]


def user_data_root() -> Path:
    """The per-user writable application-data directory for this platform."""
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        root = Path(base) if base else Path.home() / "AppData" / "Local"
        return root / APP_DIRECTORY_NAME
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_DIRECTORY_NAME
    xdg = os.environ.get("XDG_DATA_HOME")
    root = Path(xdg) if xdg else Path.home() / ".local" / "share"
    return root / APP_DIRECTORY_NAME_XDG


def runtime_root() -> Path:
    """The directory under which all mutable state lives."""
    override = os.environ.get(RUNTIME_ROOT_ENV)
    if override:
        return Path(override).expanduser().resolve()
    if is_frozen():
        return user_data_root()
    return installation_root()


def runtime_data_dir() -> Path:
    """Where databases and backups belong. Not yet the database's home."""
    return runtime_root() / DATA_DIRNAME


def runtime_database_path() -> Path:
    """Where the database belongs. Wired to ``DB_FILE`` by Packet B2, not B1."""
    return runtime_data_dir() / DATABASE_FILENAME


def legacy_data_dir() -> Path:
    """The installation-relative data directory the database still uses."""
    return installation_root() / DATA_DIRNAME


def legacy_database_path() -> Path:
    """The database path in use today, and B2's migration source."""
    return legacy_data_dir() / DATABASE_FILENAME


def logs_dir() -> Path:
    """Where log files belong — never the installation directory.

    Unlike the database this moves in B1: logs carry no user data worth
    migrating, so relocating them cannot lose anything.
    """
    return runtime_root() / LOGS_DIRNAME


def ensure_directory(path: Path) -> Path:
    """Create *path* if absent and return it.

    Directories are created where a path is first used, never as an import side
    effect: importing ``utils.config`` used to create ``data/`` and ``logs/`` in
    whatever directory a script happened to resolve, including during test
    collection.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
