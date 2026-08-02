"""Contract keeping the Python and npm Playwright pins in lockstep (blindspot B9).

The E2E suite is driven entirely by npm's `@playwright/test`. The Python
`playwright` package has zero import sites here -- it arrives only as a
transitive of `pytest-playwright` -- so a skew between the two is completely
silent at runtime. That is exactly how it drifted to 1.59.0 against npm's
1.60.0 without anything failing.

`requirements.txt` has asked for the lockstep in a comment since then, but a
comment cannot fail a build, and Dependabot raises the two ecosystems as
separate pull requests. This module is the enforcement the comment lacked: a
one-sided bump now reds its own pull request instead of landing quietly.

`pytest-playwright` is deliberately NOT compared. It versions independently
(0.x) and pins only `playwright>=1.18`, so tying it to the browser version
would be a false constraint.
"""

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

# Deliberately no ranges, wildcards, carets or tildes: only a literal X.Y.Z.
# Playwright ships a browser build per release and the two ecosystems must
# resolve to the same one, which a range cannot guarantee.
EXACT_VERSION = re.compile(r"\d+\.\d+\.\d+")

REQUIREMENT = re.compile(r"^(?P<name>[A-Za-z0-9._-]+)\s*(?P<specifier>.*)$")


def _requirement_specifier(distribution: str) -> str | None:
    """Return the raw specifier for `distribution`, e.g. `==1.61.0`.

    Matches on the parsed distribution name rather than a substring, so
    `pytest-playwright` is never mistaken for `playwright`.
    """
    text = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        match = REQUIREMENT.match(line)
        if match and match.group("name").lower() == distribution:
            return match.group("specifier").strip()
    return None


def test_python_and_npm_playwright_pins_are_exact_and_identical():
    python_specifier = _requirement_specifier("playwright")
    assert python_specifier is not None, "requirements.txt does not pin playwright"
    assert python_specifier.startswith("=="), (
        f"playwright must be pinned exactly, got {python_specifier!r}"
    )

    python_version = python_specifier[len("==") :]
    assert EXACT_VERSION.fullmatch(python_version), (
        f"playwright must pin a literal X.Y.Z, got {python_version!r}"
    )

    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    npm_version = package["devDependencies"].get("@playwright/test")
    assert npm_version is not None, "package.json does not declare @playwright/test"
    assert EXACT_VERSION.fullmatch(npm_version), (
        f"@playwright/test must pin a literal X.Y.Z, got {npm_version!r}"
    )

    assert python_version == npm_version, (
        "Playwright is skewed across ecosystems: "
        f"requirements.txt pins {python_version}, package.json pins {npm_version}. "
        "Bump both together (blindspot B9)."
    )
