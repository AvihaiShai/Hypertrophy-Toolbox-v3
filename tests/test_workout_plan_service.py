"""Unit coverage for ``utils/workout_plan_service.py`` (WS4 slice 1).

``remove_plan_exercise`` is called directly, without HTTP. The route-level
contract lives in ``tests/test_remove_exercise_characterization.py``; this file
does not import from it, so a change to the service alone is caught here.

``_Recorder`` patches ``utils.database.DatabaseHandler`` on the CLASS and
records the handlers opened, the calls made on each and their ``commit``
argument. It records no SQLite trace.
"""
from __future__ import annotations

import ast
import logging
import sqlite3
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

import utils.supersets
import utils.workout_plan_service
from utils.database import DatabaseHandler
from utils.workout_plan_service import RemovedPlanExercise, remove_plan_exercise

LOGGER_NAME = "hypertrophy_toolbox"

SELECT_SQL = "SELECT routine, exercise, superset_group FROM user_selection WHERE id = ?"
UNLINK_SQL = (
    "UPDATE user_selection SET superset_group = NULL WHERE superset_group = ? AND id != ?"
)
DELETE_LOGS_SQL = "DELETE FROM workout_log WHERE workout_plan_id = ?"
DELETE_ROW_SQL = "DELETE FROM user_selection WHERE id = ?"


def _norm(sql: str) -> str:
    return " ".join(sql.split())


def _params(params: Any) -> Any:
    return tuple(params) if isinstance(params, (list, tuple)) else params


@dataclass
class _Handler:
    db: DatabaseHandler
    calls: list[tuple[Any, ...]] = field(default_factory=list)


class _Recorder:
    """Records every ``DatabaseHandler`` constructed after ``install``.

    The wrappers copy the signatures of ``DatabaseHandler.__init__``,
    ``execute_query``, ``executemany``, ``fetch_one`` and ``fetch_all``
    (``utils/database.py:286,294-300,372,432,464``) and must change when those do.
    """

    def __init__(self) -> None:
        self.handlers: list[_Handler] = []

    @classmethod
    def install(cls, monkeypatch: pytest.MonkeyPatch) -> _Recorder:
        rec = cls()
        orig_init = DatabaseHandler.__init__
        orig_execute = DatabaseHandler.execute_query
        orig_many = DatabaseHandler.executemany
        orig_one = DatabaseHandler.fetch_one
        orig_all = DatabaseHandler.fetch_all

        def init(self: DatabaseHandler, database_path: str | None = None) -> None:
            orig_init(self, database_path)
            rec.handlers.append(_Handler(self))

        def note(self: DatabaseHandler, entry: tuple[Any, ...]) -> None:
            for handler in rec.handlers:
                if handler.db is self:
                    handler.calls.append(entry)

        def execute_query(
            self: DatabaseHandler, query: str, params: Any = None, *, commit: bool = True
        ) -> int:
            note(self, ("execute_query", _norm(query), _params(params), commit))
            return orig_execute(self, query, params, commit=commit)

        def executemany(
            self: DatabaseHandler, query: str, param_sets: Any, *, commit: bool = True
        ) -> int:
            note(self, ("executemany", _norm(query), None, commit))
            return orig_many(self, query, param_sets, commit=commit)

        def fetch_one(self: DatabaseHandler, query: str, params: Any = None) -> Any:
            note(self, ("fetch_one", _norm(query), _params(params)))
            return orig_one(self, query, params)

        def fetch_all(self: DatabaseHandler, query: str, params: Any = None) -> Any:
            note(self, ("fetch_all", _norm(query), _params(params)))
            return orig_all(self, query, params)

        monkeypatch.setattr(DatabaseHandler, "__init__", init)
        monkeypatch.setattr(DatabaseHandler, "execute_query", execute_query)
        monkeypatch.setattr(DatabaseHandler, "executemany", executemany)
        monkeypatch.setattr(DatabaseHandler, "fetch_one", fetch_one)
        monkeypatch.setattr(DatabaseHandler, "fetch_all", fetch_all)
        return rec

    def only_handler(self) -> _Handler:
        assert len(self.handlers) == 1, f"expected one DatabaseHandler, got {len(self.handlers)}"
        return self.handlers[0]


def _snapshot(db: DatabaseHandler) -> dict[str, list[dict[str, Any]]]:
    return {
        "user_selection": db.fetch_all("SELECT * FROM user_selection ORDER BY id"),
        "workout_log": db.fetch_all("SELECT * FROM workout_log ORDER BY id"),
    }


@dataclass
class _Rows:
    target: int
    partner: int


@pytest.fixture
def rows(clean_db, exercise_factory, workout_plan_factory, workout_log_factory) -> _Rows:
    """Two plan rows with one log each; no superset group yet."""
    exercise_factory("Bench Press")
    exercise_factory("Cable Fly")
    target = workout_plan_factory(exercise_name="Bench Press", routine="Push")
    partner = workout_plan_factory(exercise_name="Cable Fly", routine="Push")
    workout_log_factory(plan_id=target, routine="Push", exercise="Bench Press")
    workout_log_factory(plan_id=partner, routine="Push", exercise="Cable Fly")
    return _Rows(target, partner)


def _group(db: DatabaseHandler, group: str, *ids: int) -> None:
    for row_id in ids:
        db.execute_query(
            "UPDATE user_selection SET superset_group = ? WHERE id = ?", (group, row_id)
        )


# --------------------------------------------------------------------------- module


@pytest.mark.parametrize(
    "imports",
    [
        "import routes.workout_plan; import utils.workout_plan_service",
        "import utils.workout_plan_service; import routes.workout_plan",
    ],
    ids=["route-first", "service-first"],
)
def test_service_and_route_import_in_either_order(imports):
    completed = subprocess.run(
        [sys.executable, "-c", imports],
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr


def test_service_does_not_import_routes():
    source = Path(str(utils.workout_plan_service.__file__)).read_text(encoding="utf-8")
    imported: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")

    assert imported, "no import statement found; the check would be vacuous"
    assert [name for name in imported if name.split(".")[0] == "routes"] == []


# --------------------------------------------------------------------------- results


def test_missing_id_returns_none_after_one_lookup(clean_db, rows, monkeypatch):
    before = _snapshot(clean_db)
    rec = _Recorder.install(monkeypatch)

    assert remove_plan_exercise(99999) is None

    assert rec.only_handler().calls == [("fetch_one", SELECT_SQL, (99999,))]
    assert _snapshot(clean_db) == before


def test_existing_id_returns_the_raw_row_values(clean_db, exercise_factory, workout_log_factory):
    """Q-WS4-4: ``routine`` and ``exercise`` come back verbatim, whitespace included."""
    exercise_factory("  Bench Press  ")
    clean_db.execute_query(
        "INSERT INTO user_selection (routine, exercise, sets, min_rep_range, "
        "max_rep_range, rir, weight) VALUES (?, ?, 3, 8, 12, 2, 80.0)",
        ("  Push Day  ", "  Bench Press  "),
    )
    row = clean_db.fetch_one("SELECT last_insert_rowid() AS id")
    assert row is not None
    row_id = row["id"]
    workout_log_factory(plan_id=row_id, routine="  Push Day  ", exercise="  Bench Press  ")

    result = remove_plan_exercise(row_id)

    assert type(result) is RemovedPlanExercise
    assert (result.routine, result.exercise) == ("  Push Day  ", "  Bench Press  ")
    assert _snapshot(clean_db) == {"user_selection": [], "workout_log": []}


def test_raw_id_and_the_same_handler_reach_the_unlink(clean_db, rows, monkeypatch):
    """The id is handed on exactly as received, through the handler that ran the SELECT."""
    _group(clean_db, "SS-A", rows.target, rows.partner)
    rec = _Recorder.install(monkeypatch)
    received: list[tuple[Any, Any, Any]] = []
    original = utils.supersets.unlink_partner_for_removal

    def spy(db: DatabaseHandler, exercise_id: Any, superset_group: Any) -> None:
        received.append((db, exercise_id, superset_group))
        original(db, exercise_id, superset_group)

    monkeypatch.setattr(utils.supersets, "unlink_partner_for_removal", spy)
    sent = str(rows.target)

    remove_plan_exercise(sent)

    handler = rec.only_handler()
    assert handler.calls[0] == ("fetch_one", SELECT_SQL, (rows.target,))
    assert len(received) == 1
    db, exercise_id, superset_group = received[0]
    assert db is handler.db
    assert type(exercise_id) is str and exercise_id == sent
    assert superset_group == "SS-A"


# --------------------------------------------------------------------------- failures


def test_database_error_propagates_unwrapped(clean_db, rows):
    clean_db.execute_query(
        "CREATE TRIGGER ws4_fail_selection_delete BEFORE DELETE ON user_selection "
        f"WHEN OLD.id = {rows.target} BEGIN SELECT RAISE(ABORT, 'ws4 injected failure'); END"
    )

    with pytest.raises(sqlite3.IntegrityError) as excinfo:
        remove_plan_exercise(rows.target)

    assert type(excinfo.value) is sqlite3.IntegrityError
    assert str(excinfo.value) == "ws4 injected failure"


def test_unicode_digit_raises_value_error(clean_db):
    """``"²"`` passes the route's ``isdigit()`` check; ``int()`` rejects it here."""
    with pytest.raises(ValueError) as excinfo:
        remove_plan_exercise("²")

    assert type(excinfo.value) is ValueError


def test_service_emits_no_log_records(clean_db, rows, caplog):
    """Q-WS4-7: every record stays in the route and in ``utils/supersets.py``."""
    _group(clean_db, "SS-A", rows.target, rows.partner)

    with caplog.at_level(logging.DEBUG), caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
        remove_plan_exercise(rows.target)
        remove_plan_exercise(99999)
        with pytest.raises(ValueError):
            remove_plan_exercise("²")

    messages = [record.getMessage() for record in caplog.records]
    assert "Unlinked partner exercise from superset due to removal" in messages
    assert [
        record.getMessage()
        for record in caplog.records
        if record.pathname.endswith("workout_plan_service.py")
    ] == []
    assert not hasattr(utils.workout_plan_service, "logger")


# --------------------------------------------------------------------------- scope/order


@pytest.mark.parametrize("group", ["SS-A", ""], ids=["grouped", "empty-group"])
def test_one_handler_ordered_writes_each_committed(clean_db, rows, monkeypatch, group):
    """SELECT -> UPDATE (grouped only) -> DELETE log -> DELETE row, every write ``commit=True``."""
    _group(clean_db, group, rows.target, rows.partner)
    rec = _Recorder.install(monkeypatch)
    n = rows.target

    remove_plan_exercise(n)

    unlink = [("execute_query", UNLINK_SQL, (group, n), True)] if group else []
    assert rec.only_handler().calls == [
        ("fetch_one", SELECT_SQL, (n,)),
        *unlink,
        ("execute_query", DELETE_LOGS_SQL, (n,), True),
        ("execute_query", DELETE_ROW_SQL, (n,), True),
    ]
