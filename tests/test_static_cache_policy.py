"""Only assets requested at the current version may be long-cached.

F4 of ``docs/APP_PY_REVIEW_PLAN.md``. P4 versioned every first-party CSS/JS link
in the templates, but versioning URLs is only half a fix while the cache policy
stays blanket: a frozen build set ``SEND_FILE_MAX_AGE_DEFAULT`` to a year for
*every* static response, so anything that cannot carry a ``?v=`` inherited the
year and went stale after an upgrade.

Two whole classes cannot carry one, by construction:

* **transitive ES-module imports** — ``?v=`` on ``app.js`` does not propagate to
  ``import './toast.js'``, which resolves against the module URL and is fetched
  bare;
* **runtime-built URLs** — the bodymap SVGs and the vendor exercise catalog are
  assembled in JavaScript, where no template can reach them.

``apply_static_cache_policy`` in ``app.py`` resolves both by narrowing the long
cache to version-matching requests and making everything else revalidate.

The long max-age only exists in a frozen build, so these tests set
``STATIC_LONG_MAX_AGE`` explicitly to exercise the packaged policy from a source
checkout. ``tests/../scripts/smoke_packaged_app.py`` asserts the same contract
against a real bootloader, where the config is genuinely set.
"""
import pytest

from utils.version import APP_VERSION

LONG_MAX_AGE = 31536000

# One representative of each class that cannot carry a version.
UNVERSIFIABLE = (
    pytest.param('/static/js/modules/fetch-wrapper.js', id='transitive-es-import'),
    pytest.param(
        '/static/bodymaps/hypertrophy-advanced/body_anterior.svg',
        id='runtime-built-svg',
    ),
    pytest.param(
        '/static/vendor/free-exercise-db/exercises.json', id='vendor-json'
    ),
    pytest.param('/static/images/favicon.ico', id='favicon'),
)


@pytest.fixture
def frozen_cache_client(real_app_client):
    """The real app with the frozen build's long-cache window enabled.

    ``app.py`` sets ``STATIC_LONG_MAX_AGE`` only under
    ``getattr(sys, 'frozen', False)``, so without this the policy's long-cache
    branch is unreachable from a source checkout and these tests would pass
    vacuously.
    """
    from app import app as real_app

    original = real_app.config.get('STATIC_LONG_MAX_AGE', 0)
    real_app.config['STATIC_LONG_MAX_AGE'] = LONG_MAX_AGE
    try:
        yield real_app_client
    finally:
        real_app.config['STATIC_LONG_MAX_AGE'] = original


def _cache_control(client, url):
    response = client.get(url)
    assert response.status_code == 200, f"{url} -> {response.status_code}"
    return response.headers.get('Cache-Control', '')


def test_current_version_is_long_cached(frozen_cache_client):
    cache_control = _cache_control(
        frozen_cache_client, f'/static/css/base.css?v={APP_VERSION}'
    )
    assert f'max-age={LONG_MAX_AGE}' in cache_control
    assert 'immutable' in cache_control


def test_unversioned_request_must_revalidate(frozen_cache_client):
    """The stale-after-upgrade bug in one assertion."""
    cache_control = _cache_control(frozen_cache_client, '/static/css/base.css')
    assert 'no-cache' in cache_control
    assert str(LONG_MAX_AGE) not in cache_control


def test_stale_version_must_revalidate(frozen_cache_client):
    """A previous build's URL must not keep being honoured after an upgrade."""
    cache_control = _cache_control(
        frozen_cache_client, '/static/css/base.css?v=0.0.0-stale'
    )
    assert 'no-cache' in cache_control
    assert str(LONG_MAX_AGE) not in cache_control


@pytest.mark.parametrize('path', UNVERSIFIABLE)
def test_assets_that_cannot_carry_a_version_must_revalidate(
    frozen_cache_client, path
):
    """Closes the coverage gap P4 left: these are reachable only at runtime, so
    no amount of template work can version them."""
    cache_control = _cache_control(frozen_cache_client, path)
    assert 'no-cache' in cache_control
    assert str(LONG_MAX_AGE) not in cache_control


def test_source_checkout_never_long_caches(real_app_client):
    """Without the frozen config, nothing is long-cached — including a correctly
    versioned URL. Editing CSS in a dev server must not serve stale bytes."""
    from app import app as real_app

    assert real_app.config.get('STATIC_LONG_MAX_AGE', 0) == 0
    cache_control = _cache_control(
        real_app_client, f'/static/css/base.css?v={APP_VERSION}'
    )
    assert 'no-cache' in cache_control


def test_policy_leaves_non_static_responses_alone(real_app_client):
    """The hook is scoped to the static endpoint; pages keep Flask's defaults."""
    response = real_app_client.get('/')
    assert response.status_code == 200
    assert 'no-cache, must-revalidate' != response.headers.get('Cache-Control', '')


def test_a_missing_versioned_asset_is_not_long_cached(frozen_cache_client):
    """A 404 must never inherit the year.

    ``request.endpoint`` is set at routing time, so a file missing from the
    bundle still arrives here as ``'static'`` after ``send_static_file`` raised
    ``NotFound``. Long-caching that pins the 404 in the browser, and a hot-fix
    shipping the file without a version bump could never be picked up — the same
    stale-after-upgrade failure F4 exists to prevent, by the opposite route.
    """
    response = frozen_cache_client.get(f'/static/css/not-a-real-file.css?v={APP_VERSION}')
    assert response.status_code == 404
    cache_control = response.headers.get('Cache-Control', '')
    assert str(LONG_MAX_AGE) not in cache_control
    assert 'no-cache' in cache_control


def test_rendered_pages_carry_the_version(real_app_client):
    """The context processor is what connects APP_VERSION to the templates, and
    nothing else asserts it end to end.

    ``test_version.py`` reads template *source*; the tests above build their URLs
    from ``APP_VERSION`` in Python. So renaming the key ``inject_app_version``
    returns would render every link as ``?v=`` — Jinja prints an undefined as
    empty — while both files stayed green and the long cache silently stopped
    matching anything.
    """
    html = real_app_client.get('/').get_data(as_text=True)
    assert f'?v={APP_VERSION}' in html


def test_frozen_window_is_a_real_year(real_app_client):
    """The frozen block's value itself, which the fixture would otherwise mask.

    ``frozen_cache_client`` injects ``STATIC_LONG_MAX_AGE``, so deleting the
    assignment in ``app.py``'s frozen block leaves every test above passing while
    a packaged build long-caches nothing. Asserting the module constant is the
    cheap half of that; the packaged smoke asserts the served header.
    """
    from app import STATIC_LONG_MAX_AGE_SECONDS

    assert STATIC_LONG_MAX_AGE_SECONDS == LONG_MAX_AGE
    assert STATIC_LONG_MAX_AGE_SECONDS > 0
