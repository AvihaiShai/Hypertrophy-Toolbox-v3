"""First-run bootstrap for the immutable exercise catalog seed."""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

import utils.config
from utils.logger import get_logger
from utils.runtime_paths import publish_without_overwrite


logger = get_logger()

CATALOG_SEED_FILENAME = "catalog.seed.db"


def resolve_catalog_seed_path() -> Path:
    """Return the catalog asset path in source and PyInstaller executions."""
    if getattr(sys, "frozen", False):
        bundle_root = Path(
            getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent)
        )
    else:
        bundle_root = Path(__file__).resolve().parents[1]
    return bundle_root / "data" / CATALOG_SEED_FILENAME


def bootstrap_runtime_database(
    *,
    seed_path: Path | str | None = None,
    database_path: Path | str | None = None,
) -> bool:
    """Copy the immutable catalog into a missing runtime database.

    Returns ``True`` only when this process publishes the new runtime database.
    Existing targets are never opened, validated, or replaced. A temporary
    sibling keeps partial copies invisible, and exclusive publication makes two
    simultaneous first launches safe.
    """
    target = Path(
        database_path if database_path is not None else utils.config.DB_FILE
    ).expanduser().resolve()
    if target.exists():
        return False

    seed = Path(
        seed_path if seed_path is not None else resolve_catalog_seed_path()
    ).expanduser().resolve()
    if not seed.is_file():
        logger.warning(
            "Catalog seed is unavailable at %s; continuing with empty-schema "
            "initialization",
            seed,
        )
        return False
    if seed == target:
        raise ValueError("Catalog seed and runtime database paths must differ")

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{target.name}.",
            suffix=".tmp",
            dir=target.parent,
        )
        os.close(descriptor)
        temporary = Path(temporary_name)
        shutil.copyfile(seed, temporary)
        with temporary.open("r+b") as copied:
            os.fsync(copied.fileno())

        try:
            publish_without_overwrite(temporary, target)
        except FileExistsError:
            logger.info(
                "Runtime database was created concurrently at %s; "
                "preserving it",
                target,
            )
            return False

        logger.info(
            "Initialized runtime database from catalog seed at %s",
            target,
        )
        return True
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
