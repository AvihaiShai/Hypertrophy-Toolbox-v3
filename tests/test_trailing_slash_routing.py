"""Regression tests for trailing-slash routing on the real app.

F3 of ``docs/APP_PY_REVIEW_PLAN.md``. ``app.py`` had a ``clear_trailing``
before_request hook that answered any path ending in ``/`` with
``redirect(rp[:-1])``. It did not shadow ``strict_slashes = False`` — it ran
first and actively counteracted it, redirecting requests permissive routing
would otherwise have served directly. Two consequences:

* the redirect target was built from ``request.path`` alone, so the query
  string was dropped: ``/workout_plan/?x=1`` became ``/workout_plan``;
* it defaulted to 302, and clients re-issue a 302'd POST as GET, so
  ``POST /export_to_workout_log/`` silently became a GET.

Owner decision D1 deleted the hook rather than repairing it to a
query-preserving 308. These tests pin the resulting behavior, since a deletion
with no coverage is indistinguishable from the hook never having been exercised.
"""
import pytest


@pytest.fixture(scope='module')
def real_app_client(tmp_path_factory):
    """A client for the real app.py routes, on a scratch database.

    The conftest test app has no ``clear_trailing`` hook and never did, so it
    cannot tell whether the production hook is gone. This has to be the real one.
    """
    import utils.config

    scratch_db = tmp_path_factory.mktemp('trailing_slash') / 'database.db'
    original_db_file = utils.config.DB_FILE
    utils.config.DB_FILE = str(scratch_db)
    try:
        from app import app

        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    finally:
        utils.config.DB_FILE = original_db_file


@pytest.mark.parametrize('path', ['/workout_plan/', '/weekly_summary/', '/progression/'])
def test_trailing_slash_get_is_served_without_a_redirect(real_app_client, path):
    """``strict_slashes = False`` serves these directly; nothing redirects now."""
    response = real_app_client.get(path)
    assert response.status_code == 200
    assert 'Location' not in response.headers


def test_trailing_slash_get_keeps_its_query_string(real_app_client):
    """The hook rebuilt the target from ``request.path``, dropping ``?x=1``.

    Serving the request directly is what preserves it — assert no redirect
    occurred, because a redirect is the only thing that could have stripped it.
    """
    response = real_app_client.get('/workout_plan/?routine=GYM+-+Full+Body')
    assert response.status_code == 200
    assert 'Location' not in response.headers


def test_trailing_slash_post_is_not_downgraded_to_get(real_app_client):
    """A 302 on POST makes clients re-issue as GET, silently losing the body.

    The assertion is on the absence of a redirect rather than on the export's
    own status, which depends on database contents this test does not control.
    """
    response = real_app_client.post('/export_to_workout_log/', json={})
    assert response.status_code not in (301, 302, 303, 307, 308)
    assert 'Location' not in response.headers


def test_root_path_is_unaffected(real_app_client):
    """The hook always skipped ``/`` via ``rp != '/'``; deleting it changes nothing."""
    response = real_app_client.get('/')
    assert response.status_code == 200
