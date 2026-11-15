"""Program backup and restore carry the four execution fields (#567).

Acceptance tests driven through the ``/api/backups`` endpoints with the shared ``client``:

* **Round trip** -- a plan row's ``execution_style``, ``time_cap_seconds``,
  ``emom_interval_seconds`` and ``emom_rounds`` survive backup and restore exactly, including
  rows at the limit values and the snapshot taken by "Save current plan first".
* **Older backups** -- a backup saved by a build that predates the four columns is untouched
  by the upgrade, stays listed and usable, and restores as ``standard`` with empty timing.
* **Version label** -- a new backup is labelled ``schema_version`` 2; restore ignores the
  label (ADR-008).
* **Response shapes** -- the six endpoints' success responses carry exactly the keys they
  carried before.

The whole-restore refusal and the guarantee that a refused restore changes nothing are in
``tests/test_program_backup_restore_fuzz.py``; the restore-acceptance contract and its
tripwire (ADR-015) are in ``tests/test_backup_execution_contract.py``.

Harness non-claim
-----------------
Plan rows at the limit values and the pre-change backup tables are written by direct SQL. That
constructs a persisted state; it is not a modelled user action. The three shapes the plan page
itself writes -- ``standard`` with no timing, ``amrap`` with a time cap, ``emom`` with an
interval and rounds -- are set through ``POST /api/execution_style``, the application's own
writer.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

import pytest

from utils.database import DatabaseHandler
from utils.program_backup import initialize_backup_tables


_ROUTINE = "GYM - Full Body - Workout A"

_EXECUTION_COLUMNS = (
    "execution_style",
    "time_cap_seconds",
    "emom_interval_seconds",
    "emom_rounds",
)

# The seven metadata keys of a backup, and the ten keys of each item in the detail payload,
# as they were before this change.
_METADATA_KEYS = {
    "id",
    "name",
    "note",
    "backup_type",
    "schema_version",
    "item_count",
    "created_at",
}
_ITEM_KEYS = {
    "routine",
    "exercise",
    "sets",
    "min_rep_range",
    "max_rep_range",
    "rir",
    "rpe",
    "weight",
    "exercise_order",
    "superset_group",
}
_RESTORE_KEYS = {"backup_id", "backup_name", "restored_count", "skipped", "invalid"}

# program_backup_items exactly as utils/program_backup.py created it before the four columns
# were added (the DDL on main at 189756f4).
_PRE_CHANGE_ITEMS_DDL = """
    CREATE TABLE program_backup_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        backup_id INTEGER NOT NULL,
        routine TEXT NOT NULL,
        exercise TEXT NOT NULL,
        sets INTEGER NOT NULL,
        min_rep_range INTEGER NOT NULL,
        max_rep_range INTEGER NOT NULL,
        rir INTEGER,
        rpe REAL,
        weight REAL NOT NULL,
        exercise_order INTEGER,
        superset_group TEXT DEFAULT NULL,
        FOREIGN KEY (backup_id) REFERENCES program_backups(id) ON DELETE CASCADE
    )
"""
_PRE_CHANGE_ITEM_COLUMNS = (
    "id",
    "backup_id",
    "routine",
    "exercise",
    "sets",
    "min_rep_range",
    "max_rep_range",
    "rir",
    "rpe",
    "weight",
    "exercise_order",
    "superset_group",
)

ExecutionFields = Tuple[Any, Any, Any, Any]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _set_style(client: Any, plan_id: int, style: str, **timing: int) -> None:
    """Set a plan row's style the way the plan page does."""
    payload: Dict[str, Any] = {"exercise_id": plan_id, "execution_style": style}
    payload.update(timing)
    response = client.post("/api/execution_style", json=payload)
    assert response.status_code == 200, response.get_json()


def _seed_style_by_sql(plan_id: int, fields: ExecutionFields) -> None:
    with DatabaseHandler() as db:
        rowcount = db.execute_query(
            "UPDATE user_selection SET execution_style = ?, time_cap_seconds = ?, "
            "emom_interval_seconds = ?, emom_rounds = ? WHERE id = ?",
            fields + (plan_id,),
        )
        assert rowcount == 1


def _execution_fields_by_exercise() -> Dict[str, Dict[str, Any]]:
    """Each plan row's four fields with their storage classes, keyed by exercise.

    The storage class is what shows that an empty value is still SQL NULL and a number is
    still an integer, rather than a look-alike such as ``''`` or ``'120'``.
    """
    selected = ", ".join(
        f"{column}, typeof({column}) AS {column}_type" for column in _EXECUTION_COLUMNS
    )
    with DatabaseHandler() as db:
        rows = db.fetch_all(f"SELECT exercise, {selected} FROM user_selection")
    result: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        fields = dict(row)
        exercise = fields.pop("exercise")
        assert exercise not in result, "one plan row per exercise in these tests"
        result[exercise] = fields
    return result


def _expected_fields(fields: ExecutionFields) -> Dict[str, Any]:
    """The stored shape of a row holding ``fields``: the values and their storage classes."""
    expected: Dict[str, Any] = {}
    for column, value in zip(_EXECUTION_COLUMNS, fields):
        expected[column] = value
        if value is None:
            expected[f"{column}_type"] = "null"
        elif isinstance(value, str):
            expected[f"{column}_type"] = "text"
        else:
            expected[f"{column}_type"] = "integer"
    return expected


def _empty_the_plan() -> None:
    with DatabaseHandler() as db:
        db.execute_query("DELETE FROM workout_log")
        db.execute_query("DELETE FROM user_selection")


def _create_backup(client: Any, name: str, note: Optional[str] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"name": name}
    if note is not None:
        payload["note"] = note
    response = client.post("/api/backups", json=payload)
    assert response.status_code == 200, response.get_json()
    body = response.get_json()
    assert body["ok"] is True
    return body["data"]


def _restore(client: Any, backup_id: int) -> Dict[str, Any]:
    response = client.post(f"/api/backups/{backup_id}/restore")
    assert response.status_code == 200, response.get_json()
    body = response.get_json()
    assert body["ok"] is True
    return body


@pytest.fixture
def reproduction_a_plan(client, clean_db, exercise_factory, workout_plan_factory) -> Dict[str, int]:
    """One row of each shape the plan page writes, set through the plan page's endpoint."""
    plan_ids: Dict[str, int] = {}
    for exercise in ("Probe Press", "Probe Row", "Probe Curl"):
        exercise_factory(exercise)
        plan_ids[exercise] = workout_plan_factory(exercise_name=exercise, routine=_ROUTINE)

    _set_style(client, plan_ids["Probe Press"], "amrap", time_cap_seconds=120)
    _set_style(
        client, plan_ids["Probe Row"], "emom", emom_interval_seconds=60, emom_rounds=10
    )
    _set_style(client, plan_ids["Probe Curl"], "standard")
    return plan_ids


_REPRODUCTION_A_FIELDS: Dict[str, ExecutionFields] = {
    "Probe Press": ("amrap", 120, None, None),
    "Probe Row": ("emom", None, 60, 10),
    "Probe Curl": ("standard", None, None, None),
}


# ---------------------------------------------------------------------------
# Round trip
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("plan_after_backup", ["emptied", "changed"])
def test_round_trip_through_the_endpoints_preserves_execution_fields(
    client, reproduction_a_plan, plan_after_backup
):
    """Every restored row has the four fields it had when the backup was taken.

    Measured before this change: the ``amrap`` and ``emom`` rows came back as ``standard`` with
    no timing values, and the restore reported success.
    """
    expected = {
        exercise: _expected_fields(fields)
        for exercise, fields in _REPRODUCTION_A_FIELDS.items()
    }
    before = _execution_fields_by_exercise()
    assert before == expected, "the plan page did not store the three shapes as set"

    backup = _create_backup(client, "probe-valid")
    assert backup["item_count"] == 3

    if plan_after_backup == "emptied":
        _empty_the_plan()
    else:
        # Every row ends up holding a different valid shape than the one backed up.
        _set_style(client, reproduction_a_plan["Probe Press"], "standard")
        _set_style(client, reproduction_a_plan["Probe Row"], "amrap", time_cap_seconds=30)
        _set_style(
            client,
            reproduction_a_plan["Probe Curl"],
            "emom",
            emom_interval_seconds=45,
            emom_rounds=3,
        )
        assert _execution_fields_by_exercise() != before

    body = _restore(client, backup["id"])

    # The restore reports success with the counts it reported before this change.
    assert body["data"]["restored_count"] == 3
    assert body["data"]["skipped"] == []
    assert body["data"]["invalid"] == []
    assert body["message"] == "Restored 3 exercises from 'probe-valid'"

    assert _execution_fields_by_exercise() == before


# exercise, (style, time cap, interval, rounds) -- written by direct SQL.
_LIMIT_VALUE_ROWS: List[Tuple[str, ExecutionFields]] = [
    ("Limit Time Cap Min", ("amrap", 10, None, None)),
    ("Limit Time Cap Max", ("amrap", 600, None, None)),
    ("Limit Emom Both Min", ("emom", None, 15, 1)),
    ("Limit Emom Both Max", ("emom", None, 180, 20)),
    ("Limit Emom Interval Min Rounds Max", ("emom", None, 15, 20)),
    ("Limit Emom Interval Max Rounds Min", ("emom", None, 180, 1)),
    ("Limit Standard", ("standard", None, None, None)),
]


def test_round_trip_preserves_rows_at_the_limit_values(
    client, clean_db, exercise_factory, workout_plan_factory
):
    """Time cap 10 and 600, interval 15 and 180, rounds 1 and 20 all survive exactly."""
    for exercise, fields in _LIMIT_VALUE_ROWS:
        exercise_factory(exercise)
        plan_id = workout_plan_factory(exercise_name=exercise, routine=_ROUTINE)
        _seed_style_by_sql(plan_id, fields)

    expected = {exercise: _expected_fields(fields) for exercise, fields in _LIMIT_VALUE_ROWS}
    before = _execution_fields_by_exercise()
    assert before == expected

    backup = _create_backup(client, "limit-values")
    _empty_the_plan()
    body = _restore(client, backup["id"])

    assert body["data"]["restored_count"] == len(_LIMIT_VALUE_ROWS)
    assert body["data"]["skipped"] == []
    assert body["data"]["invalid"] == []
    assert _execution_fields_by_exercise() == before


# ---------------------------------------------------------------------------
# The pre-restore safety snapshot
# ---------------------------------------------------------------------------


def test_pre_restore_snapshot_preserves_execution_fields(
    client, clean_db, exercise_factory, workout_plan_factory
):
    """The "Save current plan first" snapshot keeps the four fields like any other backup.

    The Backup Center's button calls the same ``POST /api/backups`` with a generated name and a
    fixed note (``static/js/modules/backup-center.js``), so the flow is reproduced here through
    that endpoint: restore an older backup over the plan after saving it first, then get the
    plan back from the snapshot.
    """
    exercise_factory("Snapshot Press")
    exercise_factory("Snapshot Row")
    press_id = workout_plan_factory(exercise_name="Snapshot Press", routine=_ROUTINE)
    row_id = workout_plan_factory(exercise_name="Snapshot Row", routine=_ROUTINE)

    # The older backup the user is about to restore: both rows standard.
    older = _create_backup(client, "older-plan")

    # The current plan, which the snapshot must keep.
    _set_style(client, press_id, "amrap", time_cap_seconds=90)
    _set_style(client, row_id, "emom", emom_interval_seconds=30, emom_rounds=8)
    current = _execution_fields_by_exercise()
    assert current == {
        "Snapshot Press": _expected_fields(("amrap", 90, None, None)),
        "Snapshot Row": _expected_fields(("emom", None, 30, 8)),
    }

    snapshot = _create_backup(
        client,
        "Pre-restore snapshot (2026-11-14 10:00:00)",
        note="Automatic snapshot taken before restore",
    )

    _restore(client, older["id"])
    assert _execution_fields_by_exercise() == {
        "Snapshot Press": _expected_fields(("standard", None, None, None)),
        "Snapshot Row": _expected_fields(("standard", None, None, None)),
    }

    body = _restore(client, snapshot["id"])
    assert body["data"]["restored_count"] == 2
    assert _execution_fields_by_exercise() == current


# ---------------------------------------------------------------------------
# Backups that predate the change
# ---------------------------------------------------------------------------

# routine, exercise, sets, min, max, rir, rpe, weight, exercise_order, superset_group
_LEGACY_ITEMS: List[Tuple[Any, ...]] = [
    ("Upper A", "Legacy Bench Press", 3, 6, 8, 2, 8.0, 100.0, 1, "ss-1"),
    ("Upper A", "Legacy Barbell Row", 4, 8, 12, 1, 9.0, 80.0, 2, "ss-1"),
    ("Lower B", "Legacy Squat", 5, 5, 5, None, None, 140.0, 3, None),
]
_LEGACY_NAME = "Legacy Program"
_LEGACY_NOTE = "Saved by a build without execution fields"
_LEGACY_CREATED_AT = "2026-01-02 03:04:05"


def _item_columns() -> List[Dict[str, Any]]:
    with DatabaseHandler() as db:
        return [dict(row) for row in db.fetch_all("PRAGMA table_info(program_backup_items)")]


def _item_column_names() -> List[str]:
    return [column["name"] for column in _item_columns()]


def _seed_legacy_backup(
    exercise_factory: Any,
    items: Sequence[Tuple[Any, ...]] = tuple(_LEGACY_ITEMS),
    uncatalogued: Sequence[str] = (),
) -> int:
    """Rebuild ``program_backup_items`` in its pre-change shape and seed a version-1 backup.

    The table is recreated from the old ``CREATE TABLE`` text rather than by dropping columns,
    so the starting point is the pre-change schema whatever the current one looks like. The
    header and the items are written by direct SQL: ``create_backup()`` would stamp the current
    version and capture the new columns.
    """
    for item in items:
        if item[1] not in uncatalogued:
            exercise_factory(item[1])

    with DatabaseHandler() as db:
        db.execute_query("DROP TABLE program_backup_items")
        db.execute_query(_PRE_CHANGE_ITEMS_DDL)
        db.execute_query(
            "INSERT INTO program_backups "
            "(name, note, backup_type, schema_version, item_count, created_at) "
            "VALUES (?, ?, 'manual', 1, ?, ?)",
            (_LEGACY_NAME, _LEGACY_NOTE, len(items), _LEGACY_CREATED_AT),
        )
        header = db.fetch_one(
            "SELECT id FROM program_backups WHERE name = ?", (_LEGACY_NAME,)
        )
        assert header is not None
        backup_id = header["id"]
        for item in items:
            db.execute_query(
                "INSERT INTO program_backup_items "
                "(backup_id, routine, exercise, sets, min_rep_range, max_rep_range, "
                "rir, rpe, weight, exercise_order, superset_group) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (backup_id,) + tuple(item),
            )

    assert tuple(_item_column_names()) == _PRE_CHANGE_ITEM_COLUMNS, (
        "the legacy fixture must start without the four execution columns"
    )
    return backup_id


def _legacy_snapshot() -> Dict[str, List[Dict[str, Any]]]:
    """Every header row, and every item row's pre-change columns."""
    item_columns = ", ".join(_PRE_CHANGE_ITEM_COLUMNS)
    with DatabaseHandler() as db:
        return {
            "program_backups": [
                dict(row) for row in db.fetch_all("SELECT * FROM program_backups ORDER BY id")
            ],
            "program_backup_items": [
                dict(row)
                for row in db.fetch_all(
                    f"SELECT {item_columns} FROM program_backup_items ORDER BY id"
                )
            ],
        }


def test_upgrade_leaves_legacy_headers_and_rows_unchanged(clean_db, exercise_factory):
    """Starting the new build rewrites no existing backup; a second start changes nothing."""
    backup_id = _seed_legacy_backup(exercise_factory)
    before = _legacy_snapshot()
    assert len(before["program_backups"]) == 1
    assert len(before["program_backup_items"]) == 3

    initialize_backup_tables()
    after_first_start = _legacy_snapshot()
    initialize_backup_tables()
    after_second_start = _legacy_snapshot()

    assert after_first_start == before
    assert after_second_start == before
    header = after_second_start["program_backups"][0]
    assert header["id"] == backup_id
    # The legacy label is kept, not restamped to the new build's version.
    assert header["schema_version"] == 1


def test_upgrade_adds_the_four_columns_as_null(clean_db, exercise_factory):
    """The migration is additive and idempotent, and stamps no invented value.

    ``execution_style`` must come out NULL -- not ``'standard'`` -- so a legacy row reads as
    *missing*, which is what lets restore tell it from a present value.
    """
    _seed_legacy_backup(exercise_factory)

    initialize_backup_tables()
    columns_after_first_start = _item_columns()
    initialize_backup_tables()
    columns_after_second_start = _item_columns()

    assert columns_after_second_start == columns_after_first_start, "the migration must be idempotent"

    by_name = {column["name"]: column for column in columns_after_first_start}
    assert set(by_name) == set(_PRE_CHANGE_ITEM_COLUMNS) | set(_EXECUTION_COLUMNS)
    expected_types = {
        "execution_style": "TEXT",
        "time_cap_seconds": "INTEGER",
        "emom_interval_seconds": "INTEGER",
        "emom_rounds": "INTEGER",
    }
    for name, declared_type in expected_types.items():
        assert by_name[name]["type"].upper() == declared_type
        assert by_name[name]["notnull"] == 0
        # PRAGMA reports an explicit ``DEFAULT NULL`` as the text 'NULL' and no default as None.
        assert by_name[name]["dflt_value"] in (None, "NULL")

    selected = ", ".join(f"typeof({column}) AS {column}" for column in _EXECUTION_COLUMNS)
    with DatabaseHandler() as db:
        stored = db.fetch_all(f"SELECT {selected} FROM program_backup_items")
    assert len(stored) == 3
    for row in stored:
        assert dict(row) == {column: "null" for column in _EXECUTION_COLUMNS}


def test_legacy_backup_stays_listed_and_usable_after_upgrade(client, clean_db, exercise_factory):
    """An existing backup is still listed unchanged, and can be opened, renamed, restored
    and deleted."""
    backup_id = _seed_legacy_backup(exercise_factory)
    listed_before = client.get("/api/backups").get_json()["data"]
    assert len(listed_before) == 1

    initialize_backup_tables()

    # Listed, with name, note, type, item count, creation time and schema_version unchanged.
    listed_after = client.get("/api/backups").get_json()["data"]
    assert listed_after == listed_before
    entry = listed_after[0]
    assert entry["id"] == backup_id
    assert entry["name"] == _LEGACY_NAME
    assert entry["note"] == _LEGACY_NOTE
    assert entry["backup_type"] == "manual"
    assert entry["item_count"] == 3
    assert entry["schema_version"] == 1

    # Opened.
    detail_response = client.get(f"/api/backups/{backup_id}")
    assert detail_response.status_code == 200
    detail = detail_response.get_json()["data"]
    assert detail["schema_version"] == 1
    assert sorted(item["exercise"] for item in detail["items"]) == sorted(
        item[1] for item in _LEGACY_ITEMS
    )

    # Renamed.
    patch_response = client.patch(f"/api/backups/{backup_id}", json={"name": "Legacy Renamed"})
    assert patch_response.status_code == 200
    patched = patch_response.get_json()["data"]
    assert patched["name"] == "Legacy Renamed"
    assert patched["schema_version"] == 1
    assert patched["created_at"] == entry["created_at"]

    # Restored.
    body = _restore(client, backup_id)
    assert body["data"]["restored_count"] == 3

    # Deleted.
    delete_response = client.delete(f"/api/backups/{backup_id}")
    assert delete_response.status_code == 200
    assert client.get("/api/backups").get_json()["data"] == []


def test_legacy_backup_restores_as_standard_with_empty_timing(
    client, clean_db, exercise_factory, workout_plan_factory
):
    """Every row of a pre-change backup restores as ``standard`` with empty timing.

    The style must be the stored text ``'standard'``, not NULL: the plan page only *displays*
    a NULL style as standard.
    """
    backup_id = _seed_legacy_backup(exercise_factory)
    initialize_backup_tables()

    # A current plan that is not standard, so "standard afterwards" is the restore's doing.
    exercise_factory("Legacy Current Row")
    current_id = workout_plan_factory(exercise_name="Legacy Current Row", routine=_ROUTINE)
    _set_style(client, current_id, "amrap", time_cap_seconds=120)

    body = _restore(client, backup_id)

    assert body["data"]["restored_count"] == 3
    assert body["data"]["skipped"] == []
    assert body["data"]["invalid"] == []
    assert body["message"] == f"Restored 3 exercises from '{_LEGACY_NAME}'"

    standard = _expected_fields(("standard", None, None, None))
    assert _execution_fields_by_exercise() == {item[1]: standard for item in _LEGACY_ITEMS}

    # The columns the backup always carried are restored as they were.
    with DatabaseHandler() as db:
        restored = db.fetch_all(
            "SELECT routine, exercise, sets, min_rep_range, max_rep_range, rir, rpe, weight, "
            "exercise_order, superset_group FROM user_selection ORDER BY exercise_order"
        )
    assert [tuple(row.values()) for row in restored] == _LEGACY_ITEMS


def test_legacy_backup_reports_skipped_and_invalid_rows_as_before(client, clean_db, exercise_factory):
    """A legacy backup's uncatalogued and out-of-bounds rows are skipped and reported on their
    own channels, exactly as before, and the rest restore as ``standard``."""
    items = list(_LEGACY_ITEMS) + [
        ("Upper A", "Legacy Retired Exercise", 3, 8, 10, 2, 8.0, 40.0, 4, None),
        ("Lower B", "Legacy Overloaded Row", 3, 8, 10, 2, 8.0, 99999.0, 5, None),
    ]
    backup_id = _seed_legacy_backup(
        exercise_factory, items=items, uncatalogued=("Legacy Retired Exercise",)
    )
    initialize_backup_tables()

    body = _restore(client, backup_id)

    assert body["data"]["restored_count"] == 3
    assert body["data"]["skipped"] == ["Legacy Retired Exercise"]
    assert body["data"]["invalid"] == [
        {
            "routine": "Lower B",
            "exercise": "Legacy Overloaded Row",
            "reason": "Weight must be between 0 and 1000 kg.",
        }
    ]
    standard = _expected_fields(("standard", None, None, None))
    assert _execution_fields_by_exercise() == {item[1]: standard for item in _LEGACY_ITEMS}


# ---------------------------------------------------------------------------
# The version label
# ---------------------------------------------------------------------------


def test_new_backup_is_labelled_schema_version_2(client, reproduction_a_plan):
    """A backup created by this build reports ``schema_version`` 2 wherever it is returned.

    The literal is deliberate. Comparing against ``BACKUP_SCHEMA_VERSION`` would pass whatever
    the constant says.
    """
    created = _create_backup(client, "version-two")
    backup_id = created["id"]
    assert created["schema_version"] == 2

    with DatabaseHandler() as db:
        persisted = db.fetch_one(
            "SELECT schema_version FROM program_backups WHERE id = ?", (backup_id,)
        )
    assert persisted is not None
    assert persisted["schema_version"] == 2

    listed = client.get("/api/backups").get_json()["data"]
    assert [entry["schema_version"] for entry in listed] == [2]

    detail = client.get(f"/api/backups/{backup_id}").get_json()["data"]
    assert detail["schema_version"] == 2

    patched = client.patch(f"/api/backups/{backup_id}", json={"note": "still two"}).get_json()
    assert patched["data"]["schema_version"] == 2


def _plan_without_ids() -> List[Dict[str, Any]]:
    with DatabaseHandler() as db:
        rows = [dict(row) for row in db.fetch_all("SELECT * FROM user_selection")]
    for row in rows:
        del row["id"]
    return sorted(rows, key=lambda row: row["exercise"])


def test_restore_outcome_does_not_depend_on_the_version_label(client, reproduction_a_plan):
    """Two backups identical except for ``schema_version`` restore identically.

    Restore tells a missing value from a present one by the stored value, never by the label
    (ADR-008).
    """
    labelled_one = _create_backup(client, "label-one")
    labelled_two = _create_backup(client, "label-two")
    with DatabaseHandler() as db:
        db.execute_query(
            "UPDATE program_backups SET schema_version = 1 WHERE id = ?", (labelled_one["id"],)
        )
        db.execute_query(
            "UPDATE program_backups SET schema_version = 2 WHERE id = ?", (labelled_two["id"],)
        )

    outcomes = []
    for backup in (labelled_one, labelled_two):
        _empty_the_plan()
        data = _restore(client, backup["id"])["data"]
        outcomes.append(
            {
                "restored_count": data["restored_count"],
                "skipped": data["skipped"],
                "invalid": data["invalid"],
                "plan": _plan_without_ids(),
            }
        )

    assert outcomes[0]["restored_count"] == 3
    assert outcomes[0] == outcomes[1]


# ---------------------------------------------------------------------------
# Success response shapes: no endpoint gains or loses a key
# ---------------------------------------------------------------------------


@pytest.fixture
def shape_backup(client, reproduction_a_plan) -> Dict[str, Any]:
    """The create response for a backup of a plan that uses every execution style.

    The plan is not all-``standard`` on purpose: a key added only for non-default rows would
    otherwise go unseen.
    """
    response = client.post("/api/backups", json={"name": "shape-probe", "note": "shape note"})
    assert response.status_code == 200
    return response.get_json()


def test_create_backup_response_keys_are_unchanged(shape_backup):
    """``POST /api/backups``."""
    assert shape_backup["ok"] is True
    assert set(shape_backup["data"]) == _METADATA_KEYS


def test_list_backups_response_keys_are_unchanged(client, shape_backup):
    """``GET /api/backups``."""
    response = client.get("/api/backups")
    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert len(body["data"]) == 1
    assert set(body["data"][0]) == _METADATA_KEYS


def test_backup_detail_response_keys_are_unchanged(client, shape_backup):
    """``GET /api/backups/<id>`` gains no key, on the backup or on any of its items: the detail
    response does not expose the four execution fields."""
    response = client.get(f"/api/backups/{shape_backup['data']['id']}")
    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert set(body["data"]) == _METADATA_KEYS | {"items"}
    assert len(body["data"]["items"]) == 3
    for item in body["data"]["items"]:
        assert set(item) == _ITEM_KEYS


def test_update_backup_response_keys_are_unchanged(client, shape_backup):
    """``PATCH /api/backups/<id>``."""
    response = client.patch(
        f"/api/backups/{shape_backup['data']['id']}", json={"name": "shape-renamed"}
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert set(body["data"]) == _METADATA_KEYS


def test_restore_backup_response_keys_are_unchanged(client, shape_backup):
    """``POST /api/backups/<id>/restore``."""
    response = client.post(f"/api/backups/{shape_backup['data']['id']}/restore")
    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert set(body["data"]) == _RESTORE_KEYS


def test_delete_backup_response_keys_are_unchanged(client, shape_backup):
    """``DELETE /api/backups/<id>`` answers with a message and no data."""
    response = client.delete(f"/api/backups/{shape_backup['data']['id']}")
    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert "data" not in body
    assert body["message"] == "Backup deleted successfully"
