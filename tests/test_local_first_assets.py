"""Every asset a page loads must resolve from this repository.

The application is local-first and ships as a frozen desktop build, so an
offline install must render and behave identically to an online one.

The contract below is deliberately **origin-shaped, not host-shaped**. A denylist
of the five hosts that happened to be in use would pass the moment someone adds
a sixth, which is exactly how ``unpkg.com`` on ``/volume_splitter`` survived a
CDN census that named four.

Three things are *not* in scope and must not be "fixed" by tightening these
tests:

* ``<a href>`` to an off-site page (the LinkedIn signature) — a user-initiated
  navigation, not a page-load fetch.
* The exercise reference video iframe, whose ``src`` is empty in the template
  and assigned by JavaScript only when a user opens the modal. Embedded YouTube
  playback is an online feature by design.
* ``http://www.w3.org/2000/svg`` inside inline data URIs — an XML namespace, not
  a request.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

import pytest

from utils.version import APP_VERSION

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "templates"
VENDOR_ROOT = REPO_ROOT / "static" / "vendor"

# The hosts this packet retired. Kept as an explicit list *in addition to* the
# origin-shaped contract so a regression names itself in the failure message.
RETIRED_CDN_HOSTS = (
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "cdn.jsdelivr.net",
    "cdnjs.cloudflare.com",
    "unpkg.com",
)

# Tags whose src/href the browser fetches while loading the page.
ASSET_REFERENCE = re.compile(
    r"<(?P<tag>link|script|img|iframe|source|audio|video)\b[^>]*?"
    r"\b(?:src|href)\s*=\s*(?P<quote>[\"'])(?P<url>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
ABSOLUTE_URL = re.compile(r"^(?:[a-z][a-z0-9+.-]*:)?//", re.IGNORECASE)

# `  <sha256>  <relative path>` lines under a VERSION file's `sha256:` block.
DIGEST_LINE = re.compile(r"^\s+(?P<digest>[0-9a-f]{64})\s\s(?P<relative>\S.*)$")

# A `url_for('static', filename='vendor/…')` whose filename is a *complete*
# literal. The trailing `)` excludes the concatenated exercise-image prefixes.
VENDOR_LITERAL = re.compile(
    r"url_for\(\s*['\"]static['\"]\s*,\s*filename\s*=\s*"
    r"['\"](?P<filename>vendor/[^'\"]+)['\"]\s*\)"
)
APP_VERSION_TOKEN = re.compile(r"\?v=\{\{\s*app_version\s*\}\}")

VENDOR_PACKAGES = ("bootstrap", "flatpickr", "inter", "popperjs", "sortable", "tippy")


def _templates() -> list[Path]:
    found = sorted(TEMPLATE_ROOT.rglob("*.html"))
    assert found, "no templates found; the glob is wrong, not the repository"
    return found


def _asset_references(source: str) -> list[tuple[str, str]]:
    return [
        (match.group("tag").lower(), match.group("url").strip())
        for match in ASSET_REFERENCE.finditer(source)
    ]


def _recorded_digests(package: str) -> dict[str, str]:
    """Parse the ``sha256:`` block of a vendored package's VERSION file."""
    version_file = VENDOR_ROOT / package / "VERSION"
    recorded: dict[str, str] = {}
    in_block = False
    for line in version_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("sha256:"):
            in_block = True
            continue
        if not in_block:
            continue
        match = DIGEST_LINE.match(line)
        if match:
            recorded[match.group("relative")] = match.group("digest")
        elif line.strip():
            break
    assert recorded, f"{package}/VERSION records no sha256 digests"
    return recorded


# ---------------------------------------------------------------------------
# The acceptance contract: nothing is fetched from another origin
# ---------------------------------------------------------------------------


def test_no_template_loads_a_page_asset_from_another_origin():
    """The packet's headline claim, in its cheapest checkable form.

    Scanned over the whole file rather than line by line: attributes routinely
    wrap, and `workout_log.html`'s exercise thumbnail already puts `src` two
    lines below its `<img`. A per-line scan would silently skip every such tag.
    """
    external = []
    for template in _templates():
        source = template.read_text(encoding="utf-8")
        for match in ASSET_REFERENCE.finditer(source):
            url = match.group("url").strip()
            if not ABSOLUTE_URL.match(url):
                continue
            relative = template.relative_to(REPO_ROOT).as_posix()
            line = source.count("\n", 0, match.start()) + 1
            external.append(f"  {relative}:{line} <{match.group('tag').lower()}> {url}")
    assert not external, (
        "These page assets are fetched from another origin. The application is "
        "local-first and must load every asset from static/:\n"
        + "\n".join(external)
    )


@pytest.mark.parametrize("host", RETIRED_CDN_HOSTS)
def test_no_template_mentions_a_retired_cdn_host(host: str):
    """Catches what an attribute-shaped scan cannot.

    Two things. A CDN can live inside an attribute *value* rather than in
    ``src``/``href`` — the Bootstrap stylesheet used to carry
    ``onerror="…this.href='https://cdn.jsdelivr.net/…'"``. And being a plain
    substring scan, this is the one check that cannot be defeated by however a
    tag happens to be wrapped.
    """
    offenders = [
        f"  {template.relative_to(REPO_ROOT).as_posix()}:{number}"
        for template in _templates()
        for number, line in enumerate(
            template.read_text(encoding="utf-8").splitlines(), start=1
        )
        if host in line
    ]
    assert not offenders, (
        f"{host} was retired by the local-first assets packet but is still "
        "referenced:\n" + "\n".join(offenders)
    )


def test_the_bootstrap_stylesheet_has_no_network_fallback():
    """A CDN is not a capability source for an app that may run offline.

    File-scoped rather than line-scoped: this repository does wrap subresource
    tags across lines, so an ``onerror`` on a continuation line would slip a
    line-by-line check. ``base.html`` has no legitimate ``onerror``, which makes
    the whole-file assertion both simpler and stricter.
    """
    base = (TEMPLATE_ROOT / "base.html").read_text(encoding="utf-8")
    assert "bootstrap.custom.min.css" in base, (
        "base.html no longer links bootstrap.custom.min.css at all"
    )
    assert "onerror" not in base, "base.html carries a network fallback attribute"


# ---------------------------------------------------------------------------
# What the templates now point at has to exist, and be what we said it is
# ---------------------------------------------------------------------------


def _template_vendor_references() -> list[tuple[Path, str]]:
    """Every complete ``vendor/…`` filename a template passes to ``url_for``.

    The trailing ``)`` is load-bearing. ``user_profile.html`` and
    ``workout_log.html`` build exercise-image URLs by concatenating a per-row
    value onto a ``vendor/free-exercise-db/exercises/`` prefix; that prefix is
    not a file and asserting it exists would fail for the wrong reason.
    """
    references = [
        (template, match.group("filename"))
        for template in _templates()
        for match in VENDOR_LITERAL.finditer(template.read_text(encoding="utf-8"))
    ]
    assert references, "no template references a vendored asset"
    return references


def test_every_vendored_asset_a_template_references_exists_and_is_non_empty():
    missing = []
    empty = []
    for template, filename in _template_vendor_references():
        target = REPO_ROOT / "static" / filename
        origin = f"{template.relative_to(REPO_ROOT).as_posix()} -> static/{filename}"
        if not target.is_file():
            missing.append(f"  {origin}")
        elif target.stat().st_size == 0:
            empty.append(f"  {origin}")
    assert not missing, "Templates reference vendored files that do not exist:\n" + "\n".join(missing)
    assert not empty, "Vendored files are empty:\n" + "\n".join(empty)


def test_every_vendored_asset_is_tracked_by_git():
    """Existence on disk is the wrong oracle for a packaged build.

    ``Hypertrophy-Toolbox.spec`` stages ``static/`` from ``git ls-files``, not
    from a filesystem walk, so an untracked payload is absent from the frozen
    build while every disk-reading assertion in this module — and Flask itself,
    which also serves from disk — stays green. A forgotten ``git add`` on one
    ``.woff2`` would surface only as Arial text in the shipped ``.exe``.
    """
    tracked = {
        line.replace("\\", "/")
        for line in subprocess.run(
            ["git", "ls-files", "--", "static/vendor"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        if line
    }
    on_disk = {
        path.relative_to(REPO_ROOT).as_posix()
        for package in VENDOR_PACKAGES
        for path in (VENDOR_ROOT / package).rglob("*")
        if path.is_file()
    }
    untracked = sorted(on_disk - tracked)
    assert not untracked, (
        "These vendored files exist locally but are not tracked, so they will "
        "be missing from the packaged build:\n"
        + "\n".join(f"  {path}" for path in untracked)
    )


def test_every_vendored_asset_a_template_references_is_cache_busted():
    """A frozen build long-caches a static file only at the current version.

    ``apply_static_cache_policy`` in ``app.py`` grants the year-long
    ``immutable`` header only when ``?v`` equals ``APP_VERSION``; everything
    else revalidates. Without the token these payloads would revalidate on every
    request forever, which is the opposite of the packaging goal.
    """
    unbusted = []
    for template in _templates():
        source = template.read_text(encoding="utf-8")
        for tag, url in _asset_references(source):
            # Complete literal filenames only — see _template_vendor_references.
            if not VENDOR_LITERAL.search(url):
                continue
            # The token has to be `app_version`, not merely present: the long
            # cache is granted only on an exact match with APP_VERSION, which is
            # why Font Awesome's hard-coded `?v=5.15.4` never qualified for it.
            if not APP_VERSION_TOKEN.search(url):
                relative = template.relative_to(REPO_ROOT).as_posix()
                unbusted.append(f"  {relative} <{tag}> {url}")
    assert not unbusted, (
        "Vendored assets referenced from a template must carry "
        "?v={{ app_version }}:\n" + "\n".join(unbusted)
    )


@pytest.mark.parametrize("package", VENDOR_PACKAGES)
def test_every_vendored_payload_is_recorded(package: str):
    """The digest check is only as good as the completeness of the record.

    Without this, deleting six of Inter's seven ``sha256:`` lines is a green
    change: the digest test iterates what the file happens to list.
    """
    root = VENDOR_ROOT / package
    payloads = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
        and path.name not in {"VERSION", "NOTICE.md"}
        and path.stem.upper() != "LICENSE"
    }
    assert set(_recorded_digests(package)) == payloads, (
        f"static/vendor/{package}/VERSION does not record every payload it ships"
    )


@pytest.mark.parametrize("package", VENDOR_PACKAGES)
def test_every_vendored_payload_matches_its_recorded_digest(package: str):
    """Each package's ``VERSION`` is the record of what it vendors.

    Checked against that file rather than against ``node_modules`` or a live
    CDN, so the assertion still means something on a machine with neither.
    """
    failures = []
    for relative, expected in _recorded_digests(package).items():
        payload = VENDOR_ROOT / package / relative
        if not payload.is_file():
            failures.append(f"  missing: {relative}")
            continue
        actual = hashlib.sha256(payload.read_bytes()).hexdigest()
        if actual != expected:
            failures.append(f"  content: {relative}\n    recorded {expected}\n    actual   {actual}")
    assert not failures, (
        f"static/vendor/{package} does not match static/vendor/{package}/VERSION.\n"
        "Refresh the digests deliberately (see that package's NOTICE.md); do not "
        "edit a vendored payload by hand:\n" + "\n".join(failures)
    )


def test_every_vendored_package_disables_eol_conversion():
    """A recorded digest is platform-neutral only while `-text` holds.

    Under this repository's ``core.autocrlf=true``, a vendored text file with no
    ``-text`` rule is LF in the index and CRLF in a Windows checkout, so its
    SHA-256 pin would hold on one platform and fail on the other.
    """
    rules = (VENDOR_ROOT / ".gitattributes").read_text(encoding="utf-8")
    missing = [name for name in VENDOR_PACKAGES if f"{name}/** -text" not in rules]
    assert not missing, (
        "these vendored packages have no `-text` rule, so their recorded "
        f"digests hold on one platform only: {missing}"
    )


@pytest.mark.parametrize("package", VENDOR_PACKAGES)
def test_every_vendored_package_carries_an_upstream_license(package: str):
    licenses = [
        candidate
        for candidate in (VENDOR_ROOT / package).iterdir()
        if candidate.is_file() and candidate.stem.upper() == "LICENSE"
    ]
    assert licenses, f"static/vendor/{package} ships no upstream license file"
    for licence in licenses:
        assert licence.stat().st_size > 0, f"{licence} is empty"
    notice = VENDOR_ROOT / package / "NOTICE.md"
    version = VENDOR_ROOT / package / "VERSION"
    assert notice.is_file(), f"static/vendor/{package} has no NOTICE.md"
    assert version.is_file(), f"static/vendor/{package} has no VERSION"


# ---------------------------------------------------------------------------
# Inter — the one vendored payload we rewrote rather than copied
# ---------------------------------------------------------------------------


def _inter_font_faces() -> list[str]:
    css = (VENDOR_ROOT / "inter" / "inter.css").read_text(encoding="utf-8")
    faces = re.findall(r"@font-face\s*\{(.*?)\}", css, re.DOTALL)
    assert faces, "inter.css declares no @font-face rules"
    return faces


def test_inter_resolves_every_font_file_locally():
    """The rewrite is the only place a gstatic URL could survive."""
    css = (VENDOR_ROOT / "inter" / "inter.css").read_text(encoding="utf-8")
    urls = re.findall(r"url\(([^)]+)\)", css)
    assert urls, "inter.css references no font files"
    problems = []
    for raw in urls:
        url = raw.strip().strip("'\"")
        if ABSOLUTE_URL.match(url) or url.startswith("/"):
            problems.append(f"  not repository-relative: {url}")
        elif not (VENDOR_ROOT / "inter" / url).is_file():
            problems.append(f"  missing file: {url}")
    assert not problems, "inter.css does not resolve locally:\n" + "\n".join(problems)


def test_inter_still_declares_the_four_weights_the_design_uses():
    """400/500/600/700 — narrowing the set would restyle the whole UI."""
    weights = {
        int(match.group(1))
        for face in _inter_font_faces()
        for match in [re.search(r"font-weight:\s*(\d+)", face)]
        if match
    }
    assert weights == {400, 500, 600, 700}, f"Inter now declares weights {sorted(weights)}"


def test_inter_preserves_the_upstream_swap_and_subset_behavior():
    """A ``@font-face`` without its ``unicode-range`` downloads every subset."""
    for face in _inter_font_faces():
        assert "font-display: swap" in face, f"@font-face lost font-display: swap:\n{face}"
        assert "unicode-range:" in face, f"@font-face lost its unicode-range:\n{face}"


# ---------------------------------------------------------------------------
# Offline resolution, proven through the application rather than the filesystem
# ---------------------------------------------------------------------------


def test_the_running_app_serves_every_vendored_asset(real_app_client):
    """A tracked file is not proof: Flask still has to route and send it."""
    failures = []
    seen = set()
    for _, filename in _template_vendor_references():
        if filename in seen:
            continue
        seen.add(filename)
        response = real_app_client.get(f"/static/{filename}?v={APP_VERSION}")
        if response.status_code != 200:
            failures.append(f"  {filename} -> HTTP {response.status_code}")
        elif not response.data:
            failures.append(f"  {filename} -> empty body")
    assert not failures, "The app cannot serve its own vendored assets:\n" + "\n".join(failures)


@pytest.mark.parametrize(
    "route",
    ("/", "/workout_plan", "/progression", "/volume_splitter"),
    ids=("home", "plan", "progression", "distribute"),
)
def test_rendered_pages_version_bust_every_vendored_asset(real_app_client, route):
    """The template-source check above proves the token is written; this proves
    it survives rendering.

    ``tests/test_version.py``'s link contract only matches ``filename='css/…'``
    and ``filename='js/…'``, so no existing gate sees a ``vendor/`` link at all —
    dropping ``?v={{ app_version }}`` from one would have failed nothing and
    quietly taken that asset out of the frozen build's long cache.
    """
    response = real_app_client.get(route)
    assert response.status_code == 200, f"{route} rendered HTTP {response.status_code}"
    html = response.get_data(as_text=True)
    references = [
        url for _, url in _asset_references(html) if url.startswith("/static/vendor/")
    ]
    assert references, f"{route} rendered no vendored asset links"
    unbusted = [url for url in references if f"?v={APP_VERSION}" not in url]
    assert not unbusted, (
        f"{route} renders vendored assets without ?v={APP_VERSION}:\n"
        + "\n".join(f"  {url}" for url in unbusted)
    )


def test_the_running_app_serves_every_inter_font_file(real_app_client):
    """The woff2 payloads are reachable only through inter.css, not a template."""
    css = (VENDOR_ROOT / "inter" / "inter.css").read_text(encoding="utf-8")
    urls = {raw.strip().strip("'\"") for raw in re.findall(r"url\(([^)]+)\)", css)}
    failures = []
    for url in sorted(urls):
        response = real_app_client.get(f"/static/vendor/inter/{url}")
        if response.status_code != 200 or not response.data:
            failures.append(f"  {url} -> HTTP {response.status_code}, {len(response.data)} bytes")
    assert not failures, "Vendored Inter fonts are not served:\n" + "\n".join(failures)
