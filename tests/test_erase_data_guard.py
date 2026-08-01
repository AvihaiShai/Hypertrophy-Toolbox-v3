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


@pytest.fixture(scope='module')
def real_app_client(tmp_path_factory):
    """A client for app.py's real route, on a scratch database.

    ``conftest.py`` sets ``TESTING=1``, which makes ``create_startup_backup()``
    a no-op, so importing the module writes no snapshot into the runtime tree.
    """
    import utils.config

    scratch_db = tmp_path_factory.mktemp('erase_guard') / 'database.db'
    original_db_file = utils.config.DB_FILE
    utils.config.DB_FILE = str(scratch_db)
    try:
        from app import app

        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    finally:
        utils.config.DB_FILE = original_db_file


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
