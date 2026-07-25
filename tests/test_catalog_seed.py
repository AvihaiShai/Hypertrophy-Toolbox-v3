"""Privacy, integrity, and catalog contracts for the shipped seed."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

from utils.schema_registry import OWNED_TABLES_DROP_ORDER


CATALOG_TABLES = {"exercises", "exercise_isolated_muscles"}
EXPECTED_CATALOGS = {
    "exercises": (1897, "a29fa11f38890e8e"),
    "exercise_isolated_muscles": (1598, "85c4d585567f2f71"),
}


def _connect_seed() -> sqlite3.Connection:
    seed = Path(__file__).resolve().parents[1] / "data" / "catalog.seed.db"
    return sqlite3.connect(seed.resolve().as_uri() + "?mode=ro", uri=True)


def _logical_row_hash(connection: sqlite3.Connection, table: str) -> str:
    columns = [
        row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')
    ]
    quoted_columns = ", ".join(f'"{column}"' for column in columns)
    rows = connection.execute(
        f'SELECT {quoted_columns} FROM "{table}" ORDER BY {quoted_columns}'
    )
    payload = "\n".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":"))
        for row in rows
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_seed_contains_current_schema_and_no_user_state():
    with _connect_seed() as connection:
        application_tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            )
        }

        for table in OWNED_TABLES_DROP_ORDER:
            assert table in application_tables, (
                f"Seed is missing owned table {table}"
            )
            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]
            assert count == 0, f"Seed contains {count} rows in {table}"

        assert application_tables - CATALOG_TABLES == set(
            OWNED_TABLES_DROP_ORDER
        )


def test_seed_catalog_counts_and_logical_hashes_are_stable():
    with _connect_seed() as connection:
        for table, contract in EXPECTED_CATALOGS.items():
            expected_count, expected_hash_prefix = contract
            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]
            assert count == expected_count
            assert _logical_row_hash(connection, table).startswith(
                expected_hash_prefix
            )


def test_seed_has_no_recoverable_user_pages_or_sequence_state():
    with _connect_seed() as connection:
        assert connection.execute("PRAGMA freelist_count").fetchone()[0] == 0
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        assert integrity == "ok"
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []

        sequence_rows = connection.execute(
            "SELECT name FROM sqlite_sequence"
        ).fetchall()
        owned_sequences = {
            row[0]
            for row in sequence_rows
            if row[0] in OWNED_TABLES_DROP_ORDER
        }
        assert owned_sequences == set()
