"""The app version is a single source, and templates cache-bust from it.

F4 of ``docs/APP_PY_REVIEW_PLAN.md``. Frozen builds set
``SEND_FILE_MAX_AGE_DEFAULT`` to a year, so an unversioned asset URL means an
upgraded install keeps serving the previous build's CSS and JS from cache.
Owner decision D2 introduced ``utils/version.py`` as the version source, since
before it the only version in the repository was ``package.json``'s, which
Python cannot import.
"""
import json
import re
from pathlib import Path

import pytest

from utils.version import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"

# Matches a first-party CSS/JS static link and captures whatever follows it, so
# an unbusted link is distinguishable from a busted one.
FIRST_PARTY_LINK = re.compile(
    r"\{\{\s*url_for\('static',\s*filename='((?:css|js)/[^']+)'\)\s*\}\}(\?v=\{\{\s*[^}]*\}\})?"
)


def _templates():
    # rglob, not glob: templates/partials/ carries none of these links today, so
    # a first-party link added there would otherwise be silently uncovered.
    return sorted(TEMPLATES.rglob("*.html"))


def test_app_version_matches_package_json():
    """The two version sources must not drift. D2 accepted a manual edit kept
    honest by this check, rather than a build step or a runtime Node read."""
    package_json = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    assert APP_VERSION == package_json["version"]


def test_app_version_is_a_usable_url_token():
    """It goes straight into a query string, so it must need no escaping."""
    assert re.fullmatch(r"[A-Za-z0-9.\-_]+", APP_VERSION)


def test_the_link_regex_actually_matches_something():
    """A floor under the parametrized test below, which passes vacuously if the
    regex stops matching.

    ``FIRST_PARTY_LINK`` requires single-quoted ``url_for('static', ...)``.
    Reformatting the templates to double quotes, or changing the ``url_for``
    call shape, would drop every match to zero — and "no unversioned links
    found" is exactly what an empty result looks like.
    """
    total = sum(
        len(FIRST_PARTY_LINK.findall(path.read_text(encoding="utf-8")))
        for path in _templates()
    )
    assert total >= 30, f"only {total} first-party links matched; the regex has drifted"


@pytest.mark.parametrize('template', _templates(), ids=lambda p: p.name)
def test_every_first_party_asset_link_is_version_busted(template):
    """Every first-party CSS/JS link carries ``?v={{ app_version }}``."""
    unbusted = [
        match.group(1)
        for match in FIRST_PARTY_LINK.finditer(template.read_text(encoding="utf-8"))
        if match.group(2) is None
    ]
    assert not unbusted, f"{template.name} has unversioned first-party assets: {unbusted}"


def test_no_random_cache_busters_remain():
    """The per-render ``random`` buster defeated caching entirely, re-fetching
    unchanged assets on every page view. All seven are gone; none may return."""
    offenders = [
        path.name for path in _templates()
        if "random" in path.read_text(encoding="utf-8")
    ]
    assert not offenders


def test_theme_dark_link_survives_the_buster():
    """Cross-arc guard. ``tests/test_css_wp4_4_theme_dark_contracts.py`` asserts
    the raw substring ``css/theme-dark.css`` appears in base.html, and R4 of the
    WP4.4 CSS arc forbids unlinking the file. Appending ``?v=`` outside the
    ``url_for()`` call keeps that substring intact; appending inside would not.
    """
    assert "css/theme-dark.css" in (TEMPLATES / "base.html").read_text(encoding="utf-8")
