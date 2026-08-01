"""Regression tests for the ``/erase-data`` confirmation guard.

F5 of ``docs/APP_PY_REVIEW_PLAN.md``. The guard exists only in ``app.py``'s real
route: it requires ``confirm == "ERASE_ALL_DATA"`` and snapshots before wiping.
``tests/conftest.py`` registers a guard-less twin, so six existing tests POST
``/erase-data`` with no body at all and still expect success. The E2E flow in
``e2e/erase-flow.spec.ts`` only drives the happy path, because the UI always
sends the correct token. Nothing anywhere submitted a missing or wrong token,
so deleting the server-side guard would not have failed a single test.

These drive the real route instead of the twin. Only the rejection paths are
covered, deliberately: the guard returns before ``create_startup_backup()`` and
before ``drop_all_owned_tables()``, so nothing here can erase anything.
"""
import pytest

# ``real_app_client`` comes from tests/conftest.py. It has to be the real route:
# the conftest twin has no confirm guard at all, which is the gap F5 records.


def test_app_py_registers_the_fallback_handlers(real_app_client):
    """`app.py`'s own layering, which nothing else asserts.

    `test_priority7_error_handling.py` builds its own Flask app and calls the
    shared registration itself, so it proves the *functions* work — not that
    `app.py` calls them. Deleting `register_fallback_handlers(app)` from `app.py`
    left all 28 of those tests green. These three run against the real object.
    """
    # F1: the negotiator gives unclaimed HTTP errors their real status.
    method_not_allowed = real_app_client.get(
        '/export_to_workout_log', headers={'Accept': 'application/json'}
    )
    assert method_not_allowed.status_code == 405
    assert 'POST' in method_not_allowed.headers.get('Allow', '')

    # F7: the 404 handler, in its XHR shape.
    not_found = real_app_client.get(
        '/__no_such_route__', headers={'Accept': 'application/json'}
    )
    assert not_found.status_code == 404
    assert not_found.get_json()['error']['code'] == 'NOT_FOUND'

    # The favicon short-circuit, which is asserted nowhere else.
    assert real_app_client.get('/favicon.ico').status_code == 204


def _assert_rejected(response):
    assert response.status_code == 400
    body = response.get_json()
    assert body['ok'] is False
    assert body['error']['code'] == 'VALIDATION_ERROR'


def test_erase_data_rejects_request_with_no_body(real_app_client):
    """The exact shape six existing tests send against the conftest twin."""
    _assert_rejected(real_app_client.post('/erase-data'))


@pytest.mark.parametrize('payload', [
    {},
    {'confirm': ''},
    {'confirm': None},
    {'confirm': 'erase_all_data'},
    {'confirm': 'ERASE_ALL_DATA '},
    {'confirmed': 'ERASE_ALL_DATA'},
])
def test_erase_data_rejects_wrong_confirm_token(real_app_client, payload):
    """Comparison is exact: case, whitespace and key name all matter."""
    _assert_rejected(real_app_client.post('/erase-data', json=payload))


def test_erase_data_rejects_non_json_body(real_app_client):
    """``get_json(silent=True) or {}`` must degrade to a rejection, not a 500."""
    _assert_rejected(real_app_client.post(
        '/erase-data', data='confirm=ERASE_ALL_DATA',
        content_type='application/x-www-form-urlencoded',
    ))


def test_rejected_erase_leaves_the_catalog_intact(real_app_client):
    """The point of the guard: a rejected call must not drop anything.

    Asserted against the database rather than the response, because a guard
    that returned 400 *after* wiping would satisfy every test above.
    """
    from utils.database import DatabaseHandler

    def exercise_count() -> int:
        with DatabaseHandler() as db:
            row = db.fetch_one("SELECT COUNT(*) AS n FROM exercises")
        assert row is not None, "COUNT(*) always returns a row"
        return row["n"]

    before = exercise_count()
    assert before > 0, "scratch database seeded no exercises; test proves nothing"

    _assert_rejected(real_app_client.post('/erase-data', json={'confirm': 'nope'}))

    assert exercise_count() == before
