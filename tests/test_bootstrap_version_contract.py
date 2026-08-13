"""Contracts keeping Bootstrap's installed and shipped versions aligned.

`static/css/bootstrap.custom.min.css` is compiled from the pinned
`devDependencies.bootstrap`, and `static/vendor/bootstrap/` ships that release's
runtime bundle. Nothing else forces the two to stay on the same release.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENDORED_BOOTSTRAP = ROOT / "static" / "vendor" / "bootstrap"
BUNDLE = "js/bootstrap.bundle.min.js"


def _pinned_version() -> str:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    return package["devDependencies"]["bootstrap"]


def _vendored_version() -> str:
    text = (VENDORED_BOOTSTRAP / "VERSION").read_text(encoding="utf-8")
    match = re.search(r"^version:\s*(\S+)$", text, re.MULTILINE)
    assert match, "static/vendor/bootstrap/VERSION declares no `version:` line"
    return match.group(1)


def test_the_vendored_bundle_matches_the_pinned_package_version() -> None:
    assert _vendored_version() == _pinned_version(), (
        "static/vendor/bootstrap/VERSION and package.json disagree. Re-vendor "
        "dist/js/bootstrap.bundle.min.js from node_modules and rebuild the CSS: "
        "static/css/bootstrap.custom.min.css compiles from the same package, and "
        "a runtime bundle from another release would pair mismatched CSS and JS."
    )


def test_the_vendored_bundle_is_the_pinned_release_it_claims_to_be() -> None:
    """The version line is a claim; the banner and digest are the evidence."""
    version = _vendored_version()
    bundle = VENDORED_BOOTSTRAP / BUNDLE
    banner = bundle.read_text(encoding="utf-8", errors="replace")[:400]

    assert f"Bootstrap v{version}" in banner, (
        f"static/vendor/bootstrap/{BUNDLE} does not carry the v{version} banner"
    )

    recorded = re.search(
        rf"^\s+([0-9a-f]{{64}})\s\s{re.escape(BUNDLE)}$",
        (VENDORED_BOOTSTRAP / "VERSION").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    assert recorded, f"VERSION records no sha256 for {BUNDLE}"
    assert hashlib.sha256(bundle.read_bytes()).hexdigest() == recorded.group(1)


def test_base_html_loads_the_vendored_bundle_and_no_cdn_copy() -> None:
    base_template = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")

    assert f"filename='vendor/bootstrap/{BUNDLE}'" in base_template, (
        "base.html must load the vendored Bootstrap bundle through url_for"
    )
    assert "bootstrap@" not in base_template, (
        "base.html references a versioned CDN Bootstrap URL again; the "
        "application must load Bootstrap from static/vendor/bootstrap/"
    )
