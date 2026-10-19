"""Fail a fan-in job unless every expected ``needs`` dependency succeeded.

``needs.<job>.result`` is all a fan-in job can see. Anything other than
``success`` -- failure, cancelled, skipped, an absent dependency, an unexpected
extra one or unreadable JSON -- fails, so a required fan-in check can never be
green on a partial or missing result. ``tests/test_ci_expansion_contracts.py``
pins the decision and the ``ci.yml`` wiring.

    NEEDS='${{ toJSON(needs) }}' python3 scripts/ci_fan_in.py pytest-core guard-hook-tests
"""
from __future__ import annotations

import json
import os
import sys


def problems(needs_json: str, expected: list[str]) -> list[str]:
    """Every reason the fan-in must fail; empty only when all expected jobs succeeded."""
    if not expected or len(set(expected)) != len(expected):
        return [f"expected dependencies must be distinct and nonempty: {expected}"]
    try:
        needs = json.loads(needs_json)
    except (TypeError, ValueError) as exc:
        return [f"needs context is not JSON ({exc})"]
    if not isinstance(needs, dict):
        return ["needs context is not a mapping"]
    found = [f"unexpected dependency {job}" for job in sorted(set(needs) - set(expected))]
    for job in expected:
        entry = needs.get(job)
        result = entry.get("result") if isinstance(entry, dict) else None
        if result != "success":
            found.append(f"{job}: result={'missing' if result is None else result}")
    return found


def main(argv: list[str] | None = None) -> int:
    expected = sys.argv[1:] if argv is None else argv
    found = problems(os.environ.get("NEEDS", ""), expected)
    for problem in found:
        print(f"::error title=Fan-in gate::{problem}")
    if not found:
        print(f"All required dependencies succeeded: {', '.join(expected)}")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
