"""Characterization of ``POST /remove_exercise`` (WS4 slice 1, written before extraction).

Every node here must pass on the unmodified route AND, unedited, after the
statements move from ``routes/workout_plan.py`` into ``utils/workout_plan_service.py``.

Observation seams, chosen so they survive that move:

* HTTP: exact JSON bodies. ``requestId`` is made deterministic by sending
  ``X-Request-ID`` (``utils/request_id.py`` adopts a client-supplied id), so the
  whole envelope is compared, ``requestId`` included.
* DB statements: ``_Recorder`` patches ``DatabaseHandler`` methods on the CLASS
  (``utils.database.DatabaseHandler``), not a module-level name in the route. A
  service doing ``from utils.database import DatabaseHandler`` gets the same class
  object, so its calls are still seen. A sqlite3 trace callback on every handler
  opened during the request records what actually reached SQLite, so a bypass of
  ``execute_query`` is visible too. The ``BEGIN``/``COMMIT`` pairs in that trace
  are sqlite3's implicit per-statement transactions; "no BEGIN" (AC6) means that
  no explicit ``BEGIN`` statement is issued through the handler.
* DB state: read back through ``clean_db``'s own connection.
* Failure injection: a SQLite trigger, so the real ``execute_query`` error path runs
  and no Python name has to be patched.
* Logs: caplog on ``hypertrophy_toolbox``, minus records emitted by
  ``utils/database.py`` (their level flips DEBUG->WARNING above 100 ms, so pinning
  them would be timing-dependent). The full ordered record list is pinned once per
  distinct route record sequence; every other error node checks only its
  ``API error`` record. No node pins traceback text, ``lineno`` or ``funcName``:
  the extraction adds a ``remove_plan_exercise`` frame and shifts line numbers.
"""
from __future__ import annotations

import logging
import sqlite3
import sys
from dataclasses import dataclass, field
from typing import Any

import pytest

from utils.database import DatabaseHandler

URL = "/remove_exercise"
ENDPOINT = "workout_plan.remove_exercise"
REQUEST_ID = "req_ws4_remove_characterization"
LOGGER_NAME = "hypertrophy_toolbox"

SUCCESS_MESSAGE = "Exercise removed successfully"
NO_DATA = "No data provided"
INVALID_ID = "Invalid exercise ID"
UNABLE = "Unable to remove exercise"

SELECT_SQL = "SELECT routine, exercise, superset_group FROM user_selection WHERE id = ?"
UNLINK_SQL = (
    "UPDATE user_selection SET superset_group = NULL WHERE superset_group = ? AND id != ?"
)
DELETE_LOGS_SQL = "DELETE FROM workout_log WHERE workout_plan_id = ?"
DELETE_ROW_SQL = "DELETE FROM user_selection WHERE id = ?"

# Failure message of every trace equality: the trace text is only measured on
# Windows, so a mismatch elsewhere names the SQLite and Python it ran on.
TRACE_PLATFORM = f"sqlite3.sqlite_version={sqlite3.sqlite_version}; sys.version={sys.version}"


# --------------------------------------------------------------------------- seams


def _norm(sql: str) -> str:
    return " ".join(sql.split())


@dataclass
class _Handler:
    calls: list[tuple[Any, ...]] = field(default_factory=list)
    trace: list[str] = field(default_factory=list)
    exit_exc: list[str | None] = field(default_factory=list)


class _Recorder:
    """Records every ``DatabaseHandler`` constructed after ``install``.

    The wrappers copy the signatures of ``DatabaseHandler.__init__``,
    ``execute_query``, ``executemany``, ``fetch_one``, ``fetch_all`` and
    ``__exit__`` (``utils/database.py:286,294-300,372,432,464,514``) and must
    change when those do.
    """

    def __init__(self) -> None:
        self.handlers: list[_Handler] = []
        self._by_id: dict[int, _Handler] = {}

    @classmethod
    def install(cls, monkeypatch: pytest.MonkeyPatch) -> _Recorder:
        rec = cls()
        orig_init = DatabaseHandler.__init__
        orig_execute = DatabaseHandler.execute_query
        orig_many = DatabaseHandler.executemany
        orig_one = DatabaseHandler.fetch_one
        orig_all = DatabaseHandler.fetch_all
        orig_exit = DatabaseHandler.__exit__

        def init(self: DatabaseHandler, database_path: str | None = None) -> None:
            orig_init(self, database_path)
            handler = _Handler()
            rec.handlers.append(handler)
            rec._by_id[id(self)] = handler
            self.connection.set_trace_callback(handler.trace.append)

        def note(self: DatabaseHandler, entry: tuple[Any, ...]) -> None:
            handler = rec._by_id.get(id(self))
            if handler is not None:
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

        def exit_(self: DatabaseHandler, exc_type: Any, exc: Any, tb: Any) -> None:
            handler = rec._by_id.get(id(self))
            if handler is not None:
                handler.exit_exc.append(exc_type.__name__ if exc_type else None)
            orig_exit(self, exc_type, exc, tb)

        monkeypatch.setattr(DatabaseHandler, "__init__", init)
        monkeypatch.setattr(DatabaseHandler, "execute_query", execute_query)
        monkeypatch.setattr(DatabaseHandler, "executemany", executemany)
        monkeypatch.setattr(DatabaseHandler, "fetch_one", fetch_one)
        monkeypatch.setattr(DatabaseHandler, "fetch_all", fetch_all)
        monkeypatch.setattr(DatabaseHandler, "__exit__", exit_)
        return rec

    def only_handler(self) -> _Handler:
        assert len(self.handlers) == 1, f"expected one DatabaseHandler, got {len(self.handlers)}"
        return self.handlers[0]


def _params(params: Any) -> Any:
    return tuple(params) if isinstance(params, (list, tuple)) else params


_TRACED_VERBS = ("SELECT", "INSERT", "UPDATE", "DELETE", "BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT", "RELEASE")


def _sql_trace(handler: _Handler) -> list[str]:
    """What reached SQLite: DML and transaction control, consecutive repeats collapsed.

    PRAGMAs and ``--`` trigger/FK-action comments are dropped. SQLite 3.50 reports a
    DELETE that fires an ``ON DELETE CASCADE`` action twice in a row; collapsing
    keeps the assertion independent of that SQLite-version detail.
    """
    out: list[str] = []
    for statement in handler.trace:
        text = _norm(statement)
        if not text.upper().startswith(_TRACED_VERBS):
            continue
        if out and out[-1] == text:
            continue
        out.append(text)
    return out


def _bound(sql: str, *values: Any) -> str:
    """Expand ``?`` placeholders the way SQLite's trace callback shows them."""
    for value in values:
        literal = f"'{value}'" if isinstance(value, str) else str(value)
        sql = sql.replace("?", literal, 1)
    return sql


# --------------------------------------------------------------------------- helpers


def _post_json(client: Any, body: Any) -> Any:
    return client.post(URL, json=body, headers={"X-Request-ID": REQUEST_ID})


def _post_raw(client: Any, data: str | None, content_type: str | None) -> Any:
    return client.post(
        URL, data=data, content_type=content_type, headers={"X-Request-ID": REQUEST_ID}
    )


SUCCESS_BODY = {
    "ok": True,
    "status": "success",
    "message": SUCCESS_MESSAGE,
    "requestId": REQUEST_ID,
}


def _error_body(code: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "status": "error",
        "message": message,
        "error": {"code": code, "message": message, "requestId": REQUEST_ID},
    }


def _contract_records(caplog: pytest.LogCaptureFixture) -> list[logging.LogRecord]:
    return [
        record
        for record in caplog.records
        if record.name == LOGGER_NAME and record.filename != "database.py"
    ]


def _shape(records: list[logging.LogRecord]) -> list[tuple[str, str]]:
    return [(record.levelname, record.getMessage()) for record in records]


def _extra(record: logging.LogRecord, *keys: str) -> dict[str, Any]:
    return {key: vars(record)[key] for key in keys}


def _assert_api_error(record: logging.LogRecord, code: str, message: str, status: int) -> None:
    assert (record.levelname, record.getMessage()) == ("ERROR", f"API error: {code} - {message}")
    assert _extra(
        record, "error_code", "status_code", "endpoint", "method", "path", "request_id"
    ) == {
        "error_code": code,
        "status_code": status,
        "endpoint": ENDPOINT,
        "method": "POST",
        "path": URL,
        "request_id": REQUEST_ID,
    }


def _snapshot(db: DatabaseHandler) -> dict[str, list[dict[str, Any]]]:
    return {
        "user_selection": db.fetch_all("SELECT * FROM user_selection ORDER BY id"),
        "workout_log": db.fetch_all("SELECT * FROM workout_log ORDER BY id"),
    }


@dataclass
class _Plan:
    target: int
    partner: int
    other_a: int
    other_b: int
    target_logs: list[int]
    partner_log: int
    other_log: int


@pytest.fixture
def plan(clean_db, exercise_factory, workout_plan_factory, workout_log_factory) -> _Plan:
    """Four plan rows, logs on three of them; no superset groups yet."""
    for name in ("Bench Press", "Cable Fly", "Back Squat", "Leg Curl"):
        exercise_factory(name)
    target = workout_plan_factory(exercise_name="Bench Press", routine="Push")
    partner = workout_plan_factory(exercise_name="Cable Fly", routine="Push")
    other_a = workout_plan_factory(exercise_name="Back Squat", routine="Legs")
    other_b = workout_plan_factory(exercise_name="Leg Curl", routine="Legs")
    target_logs = [
        workout_log_factory(plan_id=target, routine="Push", exercise="Bench Press"),
        workout_log_factory(plan_id=target, routine="Push", exercise="Bench Press"),
    ]
    partner_log = workout_log_factory(plan_id=partner, routine="Push", exercise="Cable Fly")
    other_log = workout_log_factory(plan_id=other_a, routine="Legs", exercise="Back Squat")
    return _Plan(target, partner, other_a, other_b, target_logs, partner_log, other_log)


def _group(db: DatabaseHandler, group: str | None, *ids: int) -> None:
    for row_id in ids:
        db.execute_query(
            "UPDATE user_selection SET superset_group = ? WHERE id = ?", (group, row_id)
        )


def _fail_delete_of(db: DatabaseHandler, row_id: int) -> None:
    """Make ``DELETE FROM user_selection`` of ``row_id`` raise inside SQLite."""
    db.execute_query(
        "CREATE TRIGGER ws4_fail_selection_delete BEFORE DELETE ON user_selection "
        f"WHEN OLD.id = {int(row_id)} BEGIN SELECT RAISE(ABORT, 'ws4 injected failure'); END"
    )


def _expected_after_removal(
    before: dict[str, list[dict[str, Any]]], removed: int, unlinked: tuple[int, ...] = ()
) -> dict[str, list[dict[str, Any]]]:
    rows = []
    for row in before["user_selection"]:
        if row["id"] == removed:
            continue
        rows.append({**row, "superset_group": None} if row["id"] in unlinked else row)
    logs = [log for log in before["workout_log"] if log["workout_plan_id"] != removed]
    return {"user_selection": rows, "workout_log": logs}


# --------------------------------------------------------------------------- 200


class TestSuccessContract:
    @pytest.mark.parametrize("as_string", [False, True], ids=["int-id", "string-id"])
    def test_envelope_and_rows(self, client, clean_db, plan, as_string):
        """AC2: exact keys/message, no ``data``; row + its logs gone, nothing else."""
        before = _snapshot(clean_db)
        sent = str(plan.target) if as_string else plan.target

        resp = _post_json(client, {"id": sent})

        assert resp.status_code == 200
        assert resp.mimetype == "application/json"
        assert resp.get_json() == SUCCESS_BODY
        assert _snapshot(clean_db) == _expected_after_removal(before, plan.target)

    def test_leading_zero_string_id_resolves_the_row(self, client, clean_db, plan, caplog):
        """F3: ``"00N"`` passes ``isdigit`` and ``int()`` finds row N; logs keep the raw id."""
        before = _snapshot(clean_db)
        sent = f"00{plan.target}"

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, {"id": sent})

        assert resp.status_code == 200
        assert resp.get_json() == SUCCESS_BODY
        assert _snapshot(clean_db) == _expected_after_removal(before, plan.target)
        info = _contract_records(caplog)[-1]
        assert _extra(info, "exercise_id") == {"exercise_id": sent}

    def test_logs_without_superset(self, client, clean_db, exercise_factory, caplog):
        """AC8 + Q-WS4-4: debug then INFO; extras are the raw id and the raw row values."""
        exercise_factory("Bench Press")
        clean_db.execute_query(
            "INSERT INTO user_selection (routine, exercise, sets, min_rep_range, "
            "max_rep_range, rir, weight) VALUES (?, ?, 3, 8, 12, 2, 80.0)",
            ("  Push Day  ", "Bench Press"),
        )
        row = clean_db.fetch_one("SELECT last_insert_rowid() AS id")
        assert row is not None
        row_id = row["id"]

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, {"id": row_id})

        assert resp.status_code == 200
        records = _contract_records(caplog)
        assert _shape(records) == [
            ("DEBUG", f"Received data for remove_exercise: {{'id': {row_id}}}"),
            ("INFO", "Exercise removed from workout plan"),
        ]
        assert _extra(records[1], "exercise_id", "routine", "exercise") == {
            "exercise_id": row_id,
            "routine": "  Push Day  ",
            "exercise": "Bench Press",
        }


# --------------------------------------------------------------------------- scope/order


class TestStatementScope:
    @pytest.mark.parametrize("group", [None, ""], ids=["null-group", "empty-group"])
    def test_without_superset(self, client, clean_db, plan, monkeypatch, group):
        """AC6: one handler; SELECT -> DELETE log -> DELETE row; each write commits alone."""
        _group(clean_db, group, plan.target)
        rec = _Recorder.install(monkeypatch)

        resp = _post_json(client, {"id": plan.target})

        assert resp.status_code == 200
        handler = rec.only_handler()
        n = plan.target
        assert handler.calls == [
            ("fetch_one", SELECT_SQL, (n,)),
            ("execute_query", DELETE_LOGS_SQL, (n,), True),
            ("execute_query", DELETE_ROW_SQL, (n,), True),
        ]
        assert handler.exit_exc == [None]
        assert _sql_trace(handler) == [
            _bound(SELECT_SQL, n),
            "BEGIN",
            _bound(DELETE_LOGS_SQL, n),
            "COMMIT",
            "BEGIN",
            _bound(DELETE_ROW_SQL, n),
            "COMMIT",
        ], TRACE_PLATFORM

    def test_with_superset(self, client, clean_db, plan, monkeypatch):
        """AC6: partner UPDATE first, raw id handed on; partner nulled, other group intact."""
        _group(clean_db, "SS-A", plan.target, plan.partner)
        _group(clean_db, "SS-B", plan.other_a, plan.other_b)
        before = _snapshot(clean_db)
        rec = _Recorder.install(monkeypatch)

        resp = _post_json(client, {"id": str(plan.target)})

        assert resp.status_code == 200
        handler = rec.only_handler()
        n = plan.target
        assert handler.calls == [
            ("fetch_one", SELECT_SQL, (n,)),
            ("execute_query", UNLINK_SQL, ("SS-A", n), True),
            ("execute_query", DELETE_LOGS_SQL, (n,), True),
            ("execute_query", DELETE_ROW_SQL, (n,), True),
        ]
        assert handler.exit_exc == [None]
        assert _sql_trace(handler) == [
            _bound(SELECT_SQL, n),
            "BEGIN",
            _bound(UNLINK_SQL, "SS-A", n),
            "COMMIT",
            "BEGIN",
            _bound(DELETE_LOGS_SQL, n),
            "COMMIT",
            "BEGIN",
            _bound(DELETE_ROW_SQL, n),
            "COMMIT",
        ], TRACE_PLATFORM
        assert _snapshot(clean_db) == _expected_after_removal(
            before, plan.target, unlinked=(plan.partner,)
        )

    def test_superset_logs_carry_raw_ids(self, client, clean_db, plan, caplog):
        """AC8 + A3: the supersets INFO and the route INFO both log the id as sent."""
        _group(clean_db, "SS-A", plan.target, plan.partner)
        sent = str(plan.target)

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, {"id": sent})

        assert resp.status_code == 200
        records = _contract_records(caplog)
        assert _shape(records) == [
            ("DEBUG", f"Received data for remove_exercise: {{'id': '{sent}'}}"),
            ("INFO", "Unlinked partner exercise from superset due to removal"),
            ("INFO", "Exercise removed from workout plan"),
        ]
        assert _extra(records[1], "superset_group", "removed_exercise_id") == {
            "superset_group": "SS-A",
            "removed_exercise_id": sent,
        }
        assert _extra(records[2], "exercise_id", "routine", "exercise") == {
            "exercise_id": sent,
            "routine": "Push",
            "exercise": "Bench Press",
        }


# --------------------------------------------------------------------------- 400


class TestValidationContract:
    @pytest.mark.parametrize(
        "raw",
        ["{}", "[]", "0", '""', "false", "null"],
        ids=["empty-object", "empty-list", "zero", "empty-string", "false", "null"],
    )
    def test_falsy_body_is_no_data(self, client, clean_db, plan, monkeypatch, caplog, raw):
        """AC3: falsy JSON -> 400 "No data provided", before the debug log, no DB handler."""
        before = _snapshot(clean_db)
        rec = _Recorder.install(monkeypatch)

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_raw(client, raw, "application/json")

        assert resp.status_code == 400
        assert resp.get_json() == _error_body("VALIDATION_ERROR", NO_DATA)
        assert rec.handlers == []
        assert _snapshot(clean_db) == before
        records = _contract_records(caplog)
        assert len(records) == 1
        _assert_api_error(records[0], "VALIDATION_ERROR", NO_DATA, 400)

    @pytest.mark.parametrize(
        "body",
        [
            pytest.param({"id": "abc"}, id="letters"),
            pytest.param({"id": 0}, id="int-zero"),
            pytest.param({"id": -1}, id="int-negative"),
            pytest.param({"id": "-1"}, id="string-negative"),
            pytest.param({"id": 1.5}, id="float"),
            pytest.param({"id": "1.0"}, id="string-float"),
            pytest.param({"id": True}, id="true"),
            pytest.param({"id": False}, id="false"),
            pytest.param({"id": None}, id="null"),
            pytest.param({"id": ""}, id="empty-string"),
            pytest.param({"id": " 1"}, id="leading-space"),
            pytest.param({"id": [1]}, id="list"),
            pytest.param({"other": 1}, id="missing"),
        ],
    )
    def test_invalid_id(self, client, clean_db, plan, monkeypatch, caplog, body):
        """AC3: 400 "Invalid exercise ID"; no DB handler, no write."""
        before = _snapshot(clean_db)
        rec = _Recorder.install(monkeypatch)

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, body)

        assert resp.status_code == 400
        assert resp.get_json() == _error_body("VALIDATION_ERROR", INVALID_ID)
        assert rec.handlers == []
        assert _snapshot(clean_db) == before
        _assert_api_error(_contract_records(caplog)[-1], "VALIDATION_ERROR", INVALID_ID, 400)

    def test_invalid_id_log_sequence(self, client, clean_db, caplog):
        """AC8: the debug record comes before id validation, then ``API error``."""
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, {"id": "abc"})

        assert resp.status_code == 400
        records = _contract_records(caplog)
        assert _shape(records) == [
            ("DEBUG", "Received data for remove_exercise: {'id': 'abc'}"),
            ("ERROR", f"API error: VALIDATION_ERROR - {INVALID_ID}"),
        ]
        _assert_api_error(records[1], "VALIDATION_ERROR", INVALID_ID, 400)


# --------------------------------------------------------------------------- 404


class TestNotFoundContract:
    @pytest.mark.parametrize(
        "sent, looked_up",
        [(99999, 99999), ("0099999", 99999), ("0", 0)],
        ids=["int", "leading-zero-string", "string-zero"],
    )
    def test_not_found(self, client, clean_db, plan, monkeypatch, caplog, sent, looked_up):
        """AC4: 404 names the id exactly as sent; one SELECT, nothing written."""
        before = _snapshot(clean_db)
        rec = _Recorder.install(monkeypatch)

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, {"id": sent})

        message = f"Exercise with ID {sent} not found"
        assert resp.status_code == 404
        assert resp.get_json() == _error_body("NOT_FOUND", message)
        handler = rec.only_handler()
        assert handler.calls == [("fetch_one", SELECT_SQL, (looked_up,))]
        assert _sql_trace(handler) == [_bound(SELECT_SQL, looked_up)], TRACE_PLATFORM
        assert _snapshot(clean_db) == before
        _assert_api_error(_contract_records(caplog)[-1], "NOT_FOUND", message, 404)

    def test_not_found_log_sequence(self, client, clean_db, caplog):
        """AC8: debug record, then ``API error``; nothing in between."""
        message = "Exercise with ID 99999 not found"

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, {"id": 99999})

        assert resp.status_code == 404
        records = _contract_records(caplog)
        assert _shape(records) == [
            ("DEBUG", "Received data for remove_exercise: {'id': 99999}"),
            ("ERROR", f"API error: NOT_FOUND - {message}"),
        ]
        _assert_api_error(records[1], "NOT_FOUND", message, 404)

    def test_int_zero_is_400_but_string_zero_is_404(self, client, clean_db):
        """F3 asymmetry: ``0`` fails the falsy check, ``"0"`` reaches the lookup."""
        assert _post_json(client, {"id": 0}).status_code == 400
        assert _post_json(client, {"id": "0"}).status_code == 404


# --------------------------------------------------------------------------- 500


class TestFailureContract:
    @pytest.mark.parametrize(
        "data, content_type",
        [
            ("{not json", "application/json"),
            ("id=1", "text/plain"),
            ("id=1", "application/x-www-form-urlencoded"),
            (None, None),
        ],
        ids=["malformed-json", "text-plain", "form-encoded", "no-body"],
    )
    def test_unreadable_body_is_500(
        self, client, clean_db, plan, monkeypatch, caplog, data, content_type
    ):
        """AC5: get_json() raises inside the try -> generic 500; no DB handler, no write."""
        before = _snapshot(clean_db)
        rec = _Recorder.install(monkeypatch)

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_raw(client, data, content_type)

        assert resp.status_code == 500
        assert resp.get_json() == _error_body("INTERNAL_ERROR", UNABLE)
        assert rec.handlers == []
        assert _snapshot(clean_db) == before
        _assert_api_error(_contract_records(caplog)[-1], "INTERNAL_ERROR", UNABLE, 500)

    def test_unreadable_body_log_sequence(self, client, clean_db, caplog):
        """AC8: no debug record; ``Error removing exercise`` with ``exercise_id='unknown'``."""
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_raw(client, "{not json", "application/json")

        assert resp.status_code == 500
        records = _contract_records(caplog)
        assert _shape(records) == [
            ("ERROR", "Error removing exercise"),
            ("ERROR", f"API error: INTERNAL_ERROR - {UNABLE}"),
        ]
        assert records[0].exc_info is not None
        assert _extra(records[0], "exercise_id") == {"exercise_id": "unknown"}
        _assert_api_error(records[1], "INTERNAL_ERROR", UNABLE, 500)

    def test_unicode_digit_is_500(self, client, clean_db, plan, caplog):
        """F3: ``"²"`` passes ``isdigit()``, ``int()`` raises -> 500, no write.

        The number of handlers opened is deliberately not pinned, so a later
        change to the id type is not blocked by it.
        """
        before = _snapshot(clean_db)

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, {"id": "²"})

        assert resp.status_code == 500
        assert resp.get_json() == _error_body("INTERNAL_ERROR", UNABLE)
        assert _snapshot(clean_db) == before
        _assert_api_error(_contract_records(caplog)[-1], "INTERNAL_ERROR", UNABLE, 500)

    def test_database_failure_is_500(self, client, clean_db, plan, caplog):
        """AC5: an sqlite3 error inside the DB work -> generic 500, raw id in the log."""
        _fail_delete_of(clean_db, plan.target)
        sent = str(plan.target)

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, {"id": sent})

        assert resp.status_code == 500
        assert resp.get_json() == _error_body("INTERNAL_ERROR", UNABLE)
        records = _contract_records(caplog)
        assert _shape(records) == [
            ("DEBUG", f"Received data for remove_exercise: {{'id': '{sent}'}}"),
            ("ERROR", "Error removing exercise"),
            ("ERROR", f"API error: INTERNAL_ERROR - {UNABLE}"),
        ]
        exc_info = records[1].exc_info
        assert exc_info is not None and exc_info[0] is not None
        assert issubclass(exc_info[0], sqlite3.Error)
        assert _extra(records[1], "exercise_id") == {"exercise_id": sent}
        _assert_api_error(records[2], "INTERNAL_ERROR", UNABLE, 500)


# --------------------------------------------------------------------------- Q-WS4-3 (a)


def test_known_behaviour_partial_commit_survives_late_failure(
    client, clean_db, plan, monkeypatch
):
    """CURRENT BEHAVIOUR, NOT ENDORSED (Q-WS4-3(a)).

    Removal commits statement by statement. When the final ``DELETE FROM
    user_selection`` fails, the partner unlink and the log delete have already
    committed and stay committed; only the failing statement rolls back. The plan
    row survives with its own ``superset_group`` intact (the unlink's ``id != ?``).

    An atomicity fix (follow-up 3 in ``docs/service_extraction/PLANNING.md``) must
    invert this node deliberately. That fix is out of scope for WS4 slice 1, which
    must leave this node passing.
    """
    _group(clean_db, "SS-A", plan.target, plan.partner)
    _fail_delete_of(clean_db, plan.target)
    before = _snapshot(clean_db)
    rec = _Recorder.install(monkeypatch)

    resp = _post_json(client, {"id": plan.target})

    assert resp.status_code == 500
    assert resp.get_json() == _error_body("INTERNAL_ERROR", UNABLE)

    handler = rec.only_handler()
    assert [call[-1] for call in handler.calls if call[0] == "execute_query"] == [True] * 3
    assert len(handler.exit_exc) == 1 and handler.exit_exc[0] is not None, handler.exit_exc
    assert _sql_trace(handler) == [
        _bound(SELECT_SQL, plan.target),
        "BEGIN",
        _bound(UNLINK_SQL, "SS-A", plan.target),
        "COMMIT",
        "BEGIN",
        _bound(DELETE_LOGS_SQL, plan.target),
        "COMMIT",
        "BEGIN",
        _bound(DELETE_ROW_SQL, plan.target),
        "ROLLBACK",  # execute_query rolls back only the failing statement
    ], TRACE_PLATFORM

    after = _snapshot(clean_db)
    rows = {row["id"]: row for row in after["user_selection"]}
    assert rows[plan.target]["superset_group"] == "SS-A"  # row survives, group untouched
    assert rows[plan.partner]["superset_group"] is None  # partner unlink committed
    assert [log["id"] for log in after["workout_log"]] == [
        log["id"] for log in before["workout_log"] if log["workout_plan_id"] != plan.target
    ]  # target's logs deleted and committed; every other log intact


# --------------------------------------------------------------------------- Q-WS4-8


class TestNonObjectBody:
    """Truthy non-object JSON: ``data.get`` raises in the try AND again in the except.

    The second AttributeError escapes the view, so the app-level ``Exception``
    handler answers, not the route: no "Error removing exercise" record, and the
    route's 500 envelope is not used. Only that outcome is pinned; the exact
    ``utils/errors.py`` copy is not.
    """

    @pytest.mark.parametrize("body", [[1], 5, "x", True], ids=["list", "int", "str", "true"])
    def test_browser_request_gets_html_500(self, client, clean_db, caplog, body):
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            resp = _post_json(client, body)

        assert resp.status_code == 500
        assert resp.mimetype == "text/html"
        records = _contract_records(caplog)
        assert "Error removing exercise" not in [record.getMessage() for record in records]
        if body == [1]:
            # One case is enough to show the body is logged before ``data.get`` raises.
            assert _shape(records)[0] == ("DEBUG", "Received data for remove_exercise: [1]")
