import pytest
import sqlite3
import json
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from io import BytesIO
from typing import cast
from unittest.mock import Mock

from openpyxl import load_workbook

import routes.volume_splitter as volume_splitter_routes
from utils.database import DatabaseHandler
from utils.volume_export import export_volume_plan


class TestVolumeExcelExport:
    @pytest.mark.parametrize('payload,message', [
        *[(value, 'Request data must be a JSON object') for value in ([1], 'bad', True, 1, 1.5)],
        *[({'volumes': value}, 'Volumes must be a JSON object')
          for value in (None, [], [12], '', 'bad', 12, False)],
        *[({'volumes': {'Chest': value}}, 'Volume values must be finite numbers')
          for value in (None, '12', [], {}, True, False, float('nan'), float('inf'), -float('inf'))],
    ])
    def test_rejects_invalid_input_before_building_workbook(self, client, monkeypatch, payload, message):
        builder = Mock()
        monkeypatch.setattr(volume_splitter_routes, 'build_volume_excel', builder)
        response = client.post('/api/export_volume_excel', json=payload)
        assert response.status_code == 400
        assert_error_payload(response.get_json(), 'VALIDATION_ERROR', message)
        builder.assert_not_called()

    @pytest.mark.parametrize('payload', [None, False, 0, 0.0, '', [], {}, {'volumes': {}}])
    def test_retains_header_only_exports(self, client, payload):
        response = client.post('/api/export_volume_excel', data=json.dumps(payload), content_type='application/json')
        assert response.status_code == 200
        book = load_workbook(BytesIO(response.data), read_only=True, data_only=True)
        try:
            assert book.sheetnames == ['Volume Plan']
            assert list(book['Volume Plan'].values) == [('Muscle Group', 'Sets per Week', 'Sets per Session')]
        finally:
            book.close()

    @pytest.mark.parametrize('data,content_type,status,code', [
        ('', 'application/json', 400, 'BAD_REQUEST'),
        ('{bad', 'application/json', 400, 'BAD_REQUEST'),
        ('{}', 'text/plain', 415, 'UNSUPPORTED_MEDIA_TYPE'),
        ('', None, 415, 'UNSUPPORTED_MEDIA_TYPE'),
    ])
    def test_preserves_parser_outcomes(self, client, monkeypatch, data, content_type, status, code):
        builder = Mock()
        monkeypatch.setattr(volume_splitter_routes, 'build_volume_excel', builder)
        response = client.post('/api/export_volume_excel', data=data, content_type=content_type)
        assert response.status_code == status
        assert response.get_json()['error']['code'] == code
        assert response.get_json()['ok'] is False
        builder.assert_not_called()

    @pytest.mark.parametrize('days,per_session', [
        (None, 4), ('bad', 4), ('', 4), ([], 4), ({}, 4),
        (0, 12), (-2, 12), (False, 12), (True, 12),
        (3, 4), ('4', 3), (2.9, 6), (float('nan'), 4),
    ])
    def test_preserves_training_day_coercion(self, client, days, per_session):
        response = client.post('/api/export_volume_excel', json={'training_days': days, 'volumes': {'Chest': 12}})
        assert response.status_code == 200
        book = load_workbook(BytesIO(response.data), read_only=True, data_only=True)
        try:
            assert list(book['Volume Plan'].values)[1] == ('Chest', 12, per_session)
        finally:
            book.close()

    def test_preserves_successful_workbook_contract(self, client):
        response = client.post('/api/export_volume_excel', json={
            'volumes': {'Chest': 12.5, 'Back': -2.5, 'Calves': 0},
        })
        assert response.status_code == 200
        assert response.mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        assert re.search(r'attachment; filename=volume_plan_\d{8}_\d{6}\.xlsx', response.headers['Content-Disposition'])
        book = load_workbook(BytesIO(response.data), data_only=True)
        try:
            assert book.sheetnames == ['Volume Plan']
            header, *rows = list(book['Volume Plan'].values)
            assert header == ('Muscle Group', 'Sets per Week', 'Sets per Session')
            assert {row[0]: row[1:] for row in rows} == {'Chest': (12.5, 4.2), 'Back': (-2.5, -0.8), 'Calves': (0, 0)}
            assert [book['Volume Plan'].column_dimensions[column].width for column in 'ABC'] == [15, 15, 15]
        finally:
            book.close()

    @pytest.mark.parametrize('volume', [12, 10 ** 400], ids=['ordinary', 'large-finite-integer'])
    def test_logs_local_builder_failures_without_leaking_detail(self, client, monkeypatch, volume):
        builder = Mock(side_effect=RuntimeError('private builder detail'))
        log = Mock()
        monkeypatch.setattr(volume_splitter_routes, 'build_volume_excel', builder)
        monkeypatch.setattr(volume_splitter_routes.logger, 'exception', log)
        payload = {'volumes': {'Chest': volume}}
        response = client.post('/api/export_volume_excel', json=payload)
        assert response.status_code == 500
        assert_error_payload(response.get_json(), 'INTERNAL_ERROR', 'Failed to export volume plan')
        assert b'private builder detail' not in response.data
        builder.assert_called_once_with(payload)
        log.assert_called_once_with('Error exporting volume plan')

    @pytest.mark.parametrize('days', [float('inf'), -float('inf')])
    def test_training_day_overflow_retains_safe_500(self, client, monkeypatch, days):
        log = Mock()
        monkeypatch.setattr(volume_splitter_routes.logger, 'exception', log)
        response = client.post('/api/export_volume_excel', json={'training_days': days, 'volumes': {'Chest': 12}})
        assert response.status_code == 500
        assert_error_payload(response.get_json(), 'INTERNAL_ERROR', 'Failed to export volume plan')
        assert b'OverflowError' not in response.data
        log.assert_called_once_with('Error exporting volume plan')


def assert_success_payload(payload, *, message=None, expect_data=True):
    assert payload["ok"] is True
    assert payload["status"] == "success"
    if message is not None:
        assert payload["message"] == message
    if expect_data:
        assert "data" in payload
        return payload["data"]
    assert "data" not in payload
    return payload


def assert_error_payload(payload, code, message):
    assert payload["ok"] is False
    assert payload["status"] == "error"
    assert payload["message"] == message
    assert payload["error"]["code"] == code
    assert payload["error"]["message"] == message


def parse_api_datetime(value):
    if "," in value:
        return parsedate_to_datetime(value)
    return datetime.fromisoformat(value)


@pytest.mark.parametrize(
    "volume,ranges,status",
    [
        (10, {"min": 5, "max": 15}, "optimal"),
        (18, {"min": 5, "max": 15}, "high"),
        (10, {"min": 15, "max": 18}, "low"),
    ],
)
def test_calculate_volume_custom_ranges(client, volume, ranges, status):
    response = client.post(
        "/api/calculate_volume",
        json={
            "mode": "basic",
            "training_days": 3,
            "volumes": {"Chest": volume},
            "ranges": {"Chest": ranges},
        },
    )

    assert response.status_code == 200
    payload = assert_success_payload(response.get_json())
    chest_result = payload["results"].get("Chest")

    assert chest_result is not None
    assert chest_result["status"] == status


def test_calculate_volume_sanitizes_ranges(client):
    response = client.post(
        "/api/calculate_volume",
        json={
            "mode": "basic",
            "training_days": 3,
            "volumes": {"Chest": 10},
            "ranges": {"Chest": {"min": -5, "max": 8}},
        },
    )

    assert response.status_code == 200
    payload = assert_success_payload(response.get_json())
    chest_range = payload["ranges"].get("Chest")
    chest_result = payload["results"].get("Chest")

    assert chest_range is not None
    assert pytest.approx(chest_range["min"]) == 12
    assert pytest.approx(chest_range["max"]) == 12
    assert chest_result["status"] == "low"


def test_calculate_volume_non_numeric_training_days_keeps_the_rest_of_the_payload(client):
    """A bad training_days falls back to 3 without discarding mode or volumes.

    The fallback lives in its own narrow ``except (TypeError, ValueError)``; the
    advanced-only muscle key proves ``mode`` survived it, and 12 / 3 == 4.0
    proves the fallback value is the one that reached the calculation.
    """
    response = client.post(
        "/api/calculate_volume",
        json={
            "mode": "advanced",
            "training_days": "not-a-number",
            "volumes": {"lats": 12},
        },
    )

    assert response.status_code == 200
    payload = assert_success_payload(response.get_json())
    lats_result = payload["results"].get("lats")

    assert lats_result is not None
    assert lats_result["weekly_sets"] == 12.0
    assert lats_result["sets_per_session"] == 4.0
    assert "Chest" not in payload["results"]


def test_calculate_volume_non_object_body_returns_the_internal_error_envelope(client):
    """A JSON body that is not an object still returns the 500 error envelope."""
    response = client.post("/api/calculate_volume", json=[1, 2, 3])

    assert response.status_code == 500
    assert_error_payload(
        response.get_json(), "INTERNAL_ERROR", "Failed to calculate volume"
    )


@pytest.fixture
def saved_volume_plan(clean_db):
    plan_id = export_volume_plan(
        {
            "training_days": 4,
            "volumes": {
                "Chest": 20,
                "Back": 12,
            },
        }
    )
    assert plan_id is not None
    return plan_id


def test_save_volume_plan_success(client, clean_db):
    response = client.post(
        "/api/save_volume_plan",
        json={
            "mode": "basic",
            "training_days": 4,
            "volumes": {
                "Chest": 20,
                "Back": 12,
            },
        },
    )

    assert response.status_code == 200
    payload = assert_success_payload(
        response.get_json(),
        message="Volume plan saved successfully",
    )
    assert isinstance(payload["plan_id"], int)

    with DatabaseHandler() as db:
        plan = db.fetch_one(
            "SELECT id, training_days FROM volume_plans WHERE id = ?",
            (payload["plan_id"],),
        )
        muscles = db.fetch_all(
            """
            SELECT muscle_group, weekly_sets, sets_per_session, status
            FROM muscle_volumes
            WHERE plan_id = ?
            ORDER BY muscle_group
            """,
            (payload["plan_id"],),
        )

    assert plan is not None
    assert plan["training_days"] == 4
    assert muscles == [
        {
            "muscle_group": "Back",
            "weekly_sets": 12,
            "sets_per_session": 3.0,
            "status": "optimal",
        },
        {
            "muscle_group": "Chest",
            "weekly_sets": 20,
            "sets_per_session": 5.0,
            "status": "optimal",
        },
    ]


def test_save_volume_plan_returns_500_when_export_fails(client, monkeypatch):
    monkeypatch.setattr(volume_splitter_routes, "export_volume_plan", lambda _data: None)

    response = client.post(
        "/api/save_volume_plan",
        json={"training_days": 4, "volumes": {"Chest": 20}},
    )

    assert response.status_code == 500
    assert_error_payload(response.get_json(), "INTERNAL_ERROR", "Failed to save plan")


def test_get_volume_history_returns_grouped_plan_history(client, clean_db):
    older_plan_id = export_volume_plan(
        {
            "training_days": 3,
            "volumes": {
                "Chest": 15,
            },
        }
    )
    newer_plan_id = export_volume_plan(
        {
            "training_days": 5,
            "volumes": {
                "Back": 25,
                "Chest": 20,
            },
        }
    )
    assert older_plan_id is not None
    assert newer_plan_id is not None

    with DatabaseHandler() as db:
        db.execute_query(
            "UPDATE volume_plans SET created_at = ? WHERE id = ?",
            ("2026-01-01 08:00:00", older_plan_id),
        )
        db.execute_query(
            "UPDATE volume_plans SET created_at = ? WHERE id = ?",
            ("2026-01-02 09:30:00", newer_plan_id),
        )

    response = client.get("/api/volume_history")

    assert response.status_code == 200
    payload = assert_success_payload(response.get_json())
    assert set(payload.keys()) == {str(newer_plan_id), str(older_plan_id)}
    sorted_ids = [
        plan_id
        for plan_id, _data in sorted(
            payload.items(),
            key=lambda item: parse_api_datetime(item[1]["created_at"]),
            reverse=True,
        )
    ]
    assert sorted_ids == [str(newer_plan_id), str(older_plan_id)]
    newer_plan = payload[str(newer_plan_id)]
    assert newer_plan["training_days"] == 5
    assert parse_api_datetime(newer_plan["created_at"]).replace(tzinfo=None) == datetime(
        2026, 1, 2, 9, 30, 0
    )
    assert newer_plan["muscles"] == {
        "Back": {
            "weekly_sets": 25,
            "sets_per_session": 5.0,
            "status": "optimal",
        },
        "Chest": {
            "weekly_sets": 20,
            "sets_per_session": 4.0,
            "status": "optimal",
        },
    }
    older_plan = payload[str(older_plan_id)]
    assert older_plan["training_days"] == 3
    assert parse_api_datetime(older_plan["created_at"]).replace(tzinfo=None) == datetime(
        2026, 1, 1, 8, 0, 0
    )
    assert older_plan["muscles"]["Chest"]["weekly_sets"] == 15


def test_get_volume_plan_returns_wrapped_contract(client, saved_volume_plan):
    response = client.get(f"/api/volume_plan/{saved_volume_plan}")

    assert response.status_code == 200
    payload = assert_success_payload(response.get_json())
    assert set(payload.keys()) == {
        "training_days",
        "created_at",
        "mode",
        "is_active",
        "volumes",
    }
    assert payload["training_days"] == 4
    assert payload["mode"] == "basic"
    assert payload["is_active"] is False
    assert isinstance(payload["created_at"], str)
    assert payload["volumes"] == {
        "Chest": {
            "weekly_sets": 20,
            "sets_per_session": 5.0,
            "status": "optimal",
        },
        "Back": {
            "weekly_sets": 12,
            "sets_per_session": 3.0,
            "status": "optimal",
        },
    }


def test_get_volume_plan_returns_404_for_missing_plan(client, clean_db):
    response = client.get("/api/volume_plan/99999")

    assert response.status_code == 404
    assert_error_payload(response.get_json(), "NOT_FOUND", "Plan not found")


def test_delete_volume_plan_success(client, saved_volume_plan):
    response = client.delete(f"/api/volume_plan/{saved_volume_plan}")

    assert response.status_code == 200
    assert_success_payload(
        response.get_json(),
        message="Volume plan deleted successfully",
        expect_data=False,
    )

    with DatabaseHandler() as db:
        plan = db.fetch_one(
            "SELECT id FROM volume_plans WHERE id = ?",
            (saved_volume_plan,),
        )
        muscle_count = db.fetch_one(
            "SELECT COUNT(*) AS count FROM muscle_volumes WHERE plan_id = ?",
            (saved_volume_plan,),
        )

    assert plan is None
    assert muscle_count is not None
    assert muscle_count["count"] == 0


def test_delete_volume_plan_returns_404_for_missing_plan(client, clean_db):
    response = client.delete("/api/volume_plan/99999")

    assert response.status_code == 404
    assert_error_payload(response.get_json(), "NOT_FOUND", "Plan not found")


def test_export_volume_plan_rolls_back_on_insert_failure(clean_db, monkeypatch):
    class FaultyCursor:
        def __init__(self, cursor):
            self._cursor = cursor
            self._muscle_insert_attempts = 0

        def execute(self, query, params=()):
            normalized = " ".join(query.split()).upper()
            if "INSERT INTO MUSCLE_VOLUMES" in normalized:
                self._muscle_insert_attempts += 1
                if self._muscle_insert_attempts == 2:
                    raise sqlite3.IntegrityError("forced muscle insert failure")
            return self._cursor.execute(query, params)

        @property
        def lastrowid(self):
            return self._cursor.lastrowid

        def __getattr__(self, name):
            return getattr(self._cursor, name)

    class FaultyDatabaseHandler(DatabaseHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # The double forwards every attribute to the real cursor. Cast at
            # the substitution so DatabaseHandler.cursor keeps the concrete
            # sqlite3.Cursor type it has in production.
            self.cursor = cast(sqlite3.Cursor, FaultyCursor(self.cursor))

    monkeypatch.setattr("utils.volume_export.DatabaseHandler", FaultyDatabaseHandler)

    plan_id = export_volume_plan(
        {
            "training_days": 4,
            "volumes": {
                "Chest": 20,
                "Back": 12,
            },
        }
    )

    assert plan_id is None

    with DatabaseHandler() as db:
        plan_count = db.fetch_one("SELECT COUNT(*) AS count FROM volume_plans")
        muscle_count = db.fetch_one("SELECT COUNT(*) AS count FROM muscle_volumes")

    assert plan_count is not None
    assert muscle_count is not None
    assert plan_count["count"] == 0
    assert muscle_count["count"] == 0
