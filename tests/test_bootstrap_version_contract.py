"""Contracts keeping Bootstrap's installed and CDN versions aligned."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_bootstrap_package_and_cdn_assets_stay_version_aligned() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    bootstrap_version = package["devDependencies"]["bootstrap"]
    base_template = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")

    assert base_template.count(f"bootstrap@{bootstrap_version}/") == 2
