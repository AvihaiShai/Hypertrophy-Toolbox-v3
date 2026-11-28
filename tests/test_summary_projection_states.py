"""The HTML badge, Summary records and Pattern Coverage have independent outcomes."""
from unittest.mock import patch

import pytest

from utils.database import DatabaseHandler
from utils.weekly_summary import _PATTERN_COVERAGE_QUERY


@pytest.mark.parametrize("page,calculator", [
    ("weekly_summary", "compute_weekly_fatigue"),
    ("session_summary", "compute_heaviest_session_fatigue"),
])
def test_confirmed_empty_scored_and_failed_projection(client, workout_plan_factory, page, calculator):
    endpoint = "/" + page
    empty = client.get(endpoint)
    assert empty.status_code == 200
    assert b"No planned exercises yet" in empty.data
    assert b'fatigue-badge-breakdown-link' in empty.data

    workout_plan_factory()
    scores = client.get(endpoint)
    assert scores.status_code == 200
    assert b"No planned exercises yet" not in scores.data
    assert b"Projected fatigue unavailable" not in scores.data

    with patch(f"routes.{page}.{calculator}", side_effect=RuntimeError("test projection failed")):
        failed = client.get(endpoint)
        data = client.get(endpoint, headers={"X-Requested-With": "XMLHttpRequest"})
    assert failed.status_code == 200
    assert data.status_code == 200 and data.get_json()["data"][page]
    assert "—" in failed.get_data(as_text=True)
    assert b"Projected fatigue unavailable" in failed.data
    assert b"View per-muscle breakdown" in failed.data and b'href="/fatigue"' in failed.data
    assert b"No planned exercises yet" not in failed.data


def test_pattern_read_failure_and_empty_plan_have_distinct_success_envelopes(client, clean_db, monkeypatch):
    valid = client.get("/api/pattern_coverage")
    assert valid.status_code == 200
    expected = valid.get_json()["data"]
    assert expected["ideal_sets_range"] == {"min": 15, "max": 24}
    assert expected["total"] == {} and expected["warnings"]

    original = DatabaseHandler.fetch_all

    def fail_pattern_read(db, query, *args, **kwargs):
        if query == _PATTERN_COVERAGE_QUERY:
            raise RuntimeError("caught pattern SQL read failure")
        return original(db, query, *args, **kwargs)

    monkeypatch.setattr(DatabaseHandler, "fetch_all", fail_pattern_read)
    failed = client.get("/api/pattern_coverage")
    assert failed.status_code == 200
    assert failed.get_json()["ok"] is True
    assert failed.get_json()["data"] == {"per_routine": {}, "total": {}, "warnings": [], "sets_per_routine": {}}
