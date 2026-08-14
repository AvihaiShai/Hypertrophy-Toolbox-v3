"""Source contracts for the E2E console-error guard.

`e2e/console-guard.ts` exports two shapes of the same guard: `test`, which
carries a `consoleAllowlist` option, and `strictTest`, which is the same object
with that option removed from its *type*. `e2e/strict-fixtures.ts` re-exports the
narrowed one for the visual and redesign specs, whose whole value is a
zero-allowance gate.

That narrowing is enforced by `tsc`, which is blocking in CI -- but only against
the obvious slip of passing an object literal to `test.use`. It cannot stop a
spec from simply importing the wide `test` from `console-guard` instead. These
tests are the binding half, and they run in the required pytest gate.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
E2E = REPO_ROOT / "e2e"

# The specs whose gate must stay at zero allowance. Each is either a deep-gate
# visual spec or a required functional spec that exists to catch broken
# selectors hiding behind a screenshot diff.
ZERO_ALLOWANCE_SPECS = (
    "visual.spec.ts",
    "nav-dropdown.spec.ts",
    "visual-field-separator.spec.ts",
    "workout-plan-desktop-contract.spec.ts",
)


def _read(relative: str) -> str:
    path = E2E / relative
    assert path.is_file(), f"{relative} is missing from e2e/"
    return path.read_text(encoding="utf-8")


@pytest.mark.parametrize("spec", ZERO_ALLOWANCE_SPECS)
def test_zero_allowance_specs_take_test_from_strict_fixtures(spec: str) -> None:
    """They must not reach past the narrowed re-export to the wide `test`.

    Importing from `./console-guard` would compile, and would silently make a
    `consoleAllowlist` available to a spec that is supposed to have none.
    """
    source = _read(spec)

    assert re.search(r"from '\./strict-fixtures'", source), (
        f"{spec} must import from './strict-fixtures', which re-exports the guard "
        "with the allowlist option removed from its type"
    )
    assert "from './console-guard'" not in source, (
        f"{spec} imports './console-guard' directly, which hands it the wide `test` "
        "and defeats the narrowing that keeps its gate at zero allowance"
    )


@pytest.mark.parametrize("spec", ZERO_ALLOWANCE_SPECS)
def test_zero_allowance_specs_declare_no_allowlist(spec: str) -> None:
    assert "consoleAllowlist" not in _read(spec), (
        f"{spec} declares a consoleAllowlist. These four specs are the zero-allowance "
        "gate; an expected error belongs in the spec that provokes it, not here"
    )


def test_strict_fixtures_reexports_the_narrowed_guard() -> None:
    """The re-export is the whole mechanism; a local redefinition would bypass it."""
    source = _read("strict-fixtures.ts")

    assert re.search(r"import \{ strictTest \} from '\./console-guard'", source), (
        "strict-fixtures.ts must take its `test` from console-guard's narrowed "
        "`strictTest` rather than defining a second guard"
    )
    assert re.search(r"export const test = strictTest;", source), (
        "strict-fixtures.ts must export `strictTest` as `test`"
    )


def test_guard_rejects_broad_allowlist_patterns() -> None:
    """The anti-catch-all check must keep rejecting all three shapes.

    Deleting any one of these turns an allowlist entry back into the substring
    suppression this module replaced, and no E2E run would fail as a result --
    the entries would simply start matching more.
    """
    source = _read("console-guard.ts")

    assert "function assertNarrow" in source, "the allowlist validator is gone"
    assert "startsWith('^')" in source and "endsWith('$')" in source, (
        "assertNarrow must require ^ and $ anchors"
    )
    assert "flags.includes('m')" in source, (
        "assertNarrow must reject the m flag, which re-anchors per line and so "
        "lets an anchored pattern match a substring of multi-line console text"
    )
    assert "must not contain an unbounded wildcard" in source, (
        "assertNarrow must reject an unbounded wildcard, which matches anything"
    )
    assert "allowed.forEach(assertNarrow)" in source, (
        "assertNarrow must actually run over the declared entries"
    )


def test_guard_does_not_suppress_application_errors_globally() -> None:
    """Only closed infrastructure noise may be matched as a substring.

    `fixtures.ts` is the counter-example this module exists to replace: it
    substring-matches application errors, including null dereferences.
    """
    source = _read("console-guard.ts")

    # Greedy to the closing bracket of the declaration -- one entry is itself
    # bracketed (`[HMR]`), so a negated-class match stops in the wrong place.
    match = re.search(r"const INFRASTRUCTURE_NOISE = \[(.*)\];", source)
    assert match is not None, "INFRASTRUCTURE_NOISE must stay a declared literal list"

    fragments = re.findall(r"'([^']*)'", match.group(1))
    assert sorted(fragments) == sorted(["favicon", "Source map", "[HMR]"]), (
        "the globally-ignored list must stay closed at the three browser/tooling "
        f"fragments; found {fragments}"
    )
