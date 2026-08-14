"""Source contracts for the standards-based axe scan in `e2e/accessibility.spec.ts`.

Two things bind the scan, and neither can be enforced from inside Playwright.

The first is the dependency graph. `@axe-core/playwright` declares
`peerDependencies: {"playwright-core": ">= 1.0.0"}` -- a range wide enough that
almost any install satisfies it. Today npm resolves it against the single hoisted
`playwright-core` that `@playwright/test` already brought in, so axe and the test
runner share one browser client. If a future install ever nests a second copy,
axe would evaluate the page through a different CDP build than the one driving
it, and nothing would fail: the scan would simply start reporting against a
browser the suite is not testing.

The second is the register itself. `AXE_REGISTER` records the WCAG violations the
app produces today and asserts exact equality against them, which only stays
honest while every registered rule is also written up in
`docs/testing_phase2/A11Y_EXCEPTIONS.md`. Nothing in the TypeScript can check
that, so it is checked here, in the required pytest gate.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

AXE_PACKAGE = "@axe-core/playwright"
AXE_PINNED_VERSION = "4.13.0"
PLAYWRIGHT_CORE_VERSION = "1.61.0"

SPEC = REPO_ROOT / "e2e" / "accessibility.spec.ts"
FIXTURES = REPO_ROOT / "e2e" / "fixtures.ts"
EXCEPTIONS = REPO_ROOT / "docs" / "testing_phase2" / "A11Y_EXCEPTIONS.md"

# The three states the route matrix cannot reach. Named here so deleting one
# from the spec is a failure rather than a quiet loss of coverage.
REGISTERED_STATES = (
    "state:modal-open",
    "state:validation-error",
    "state:populated-table",
)


def _package_json() -> dict:
    return json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))


def _package_lock() -> dict:
    return json.loads((REPO_ROOT / "package-lock.json").read_text(encoding="utf-8"))


def _register_block() -> str:
    """The `AXE_REGISTER` object literal, or a failure -- never an empty string.

    A regex that silently matched nothing would make every assertion below
    vacuously true, which is the failure mode this whole file exists to prevent.
    """
    source = SPEC.read_text(encoding="utf-8")
    match = re.search(
        r"const AXE_REGISTER: Record<string, AxeFinding\[\]> = \{(.*?)^\};",
        source,
        re.S | re.M,
    )
    assert match is not None, (
        "AXE_REGISTER is no longer a top-level object literal in "
        "e2e/accessibility.spec.ts, so these contracts cannot read it"
    )
    block = match.group(1)
    assert block.strip(), "AXE_REGISTER is empty"
    return block


def _registered_keys() -> list[str]:
    keys = re.findall(r"^  '([^']+)':", _register_block(), re.M)
    assert keys, "no surface keys parsed out of AXE_REGISTER"
    return keys


def _route_names() -> list[str]:
    """Route keys from `ROUTES` in fixtures.ts, lowercased as the spec keys them."""
    source = FIXTURES.read_text(encoding="utf-8")
    match = re.search(r"export const ROUTES = \{(.*?)\} as const;", source, re.S)
    assert match is not None, "ROUTES is no longer a literal in e2e/fixtures.ts"

    names = re.findall(r"^  ([A-Z_]+):", match.group(1), re.M)
    assert names, "no route names parsed out of ROUTES"
    return [name.lower() for name in names]


def test_axe_playwright_is_pinned_to_an_exact_version() -> None:
    """A range would let the engine float, and the register is engine-specific.

    Every node count in `AXE_REGISTER` is a function of axe-core's rule set. A
    caret range that picked up a release which split, merged or retired a rule
    would move counts the app never changed.
    """
    declared = _package_json()["devDependencies"][AXE_PACKAGE]

    assert declared == AXE_PINNED_VERSION, (
        f"{AXE_PACKAGE} must be pinned exactly at {AXE_PINNED_VERSION} in "
        f"package.json devDependencies; found {declared!r}"
    )


def test_lockfile_resolves_exactly_one_playwright_core_at_the_runner_version() -> None:
    """axe and the test runner must drive the page through the same browser client.

    `@axe-core/playwright`'s `>= 1.0.0` peer range is wide enough to accept a
    second, nested `playwright-core`. Nothing would error if npm ever installed
    one -- the scan would just be evaluated by a different build than the one
    running the test.
    """
    packages = _package_lock()["packages"]

    resolved = {
        path: entry["version"]
        for path, entry in packages.items()
        if path.split("node_modules/")[-1] == "playwright-core"
    }

    assert list(resolved.values()) == [PLAYWRIGHT_CORE_VERSION], (
        "package-lock.json must resolve exactly one playwright-core, at "
        f"{PLAYWRIGHT_CORE_VERSION}; found {resolved}"
    )
    assert packages["node_modules/@playwright/test"]["version"] == PLAYWRIGHT_CORE_VERSION, (
        "@playwright/test and playwright-core must stay on the same version, or the "
        "single resolution above is no longer the runner's own client"
    )


def test_lockfile_pins_the_axe_engine_the_register_was_measured_on() -> None:
    packages = _package_lock()["packages"]

    assert packages[f"node_modules/{AXE_PACKAGE}"]["version"] == AXE_PINNED_VERSION
    engine = packages["node_modules/axe-core"]["version"]

    declared = re.search(r"const AXE_ENGINE_MAJOR_MINOR = '([^']+)';", SPEC.read_text(encoding="utf-8"))
    assert declared is not None, "the spec no longer declares AXE_ENGINE_MAJOR_MINOR"

    assert engine.startswith(f"{declared.group(1)}."), (
        f"axe-core resolves to {engine}, but the spec asserts the engine at runtime is "
        f"{declared.group(1)}.x. One of the two moved without the other."
    )


def test_axe_scan_asserts_standards_only() -> None:
    """axe's `best-practice` tag is opinion, not WCAG, and must stay out.

    A required gate that fails on house style asserts something the owner never
    agreed to conform to.
    """
    source = SPEC.read_text(encoding="utf-8")
    match = re.search(r"const AXE_TAGS = \[(.*?)\];", source, re.S)
    assert match is not None, "AXE_TAGS is no longer a declared literal list"

    tags = re.findall(r"'([^']+)'", match.group(1))
    assert tags, "no tags parsed out of AXE_TAGS"
    assert all(tag.startswith("wcag") for tag in tags), (
        f"AXE_TAGS must contain only WCAG conformance tags; found {tags}"
    )


def test_axe_register_covers_every_route_in_both_themes_and_all_three_states() -> None:
    """Coverage is pinned here because the spec cannot notice its own omission.

    The scan iterates `ROUTES`, so a route dropped from the register would fail
    on its missing key -- but a route filtered out of the loop, or a state test
    deleted outright, would take its register entry with it and leave a smaller
    matrix that still passes.
    """
    expected = {
        f"{route}:{theme}" for route in _route_names() for theme in ("light", "dark")
    } | set(REGISTERED_STATES)

    assert set(_registered_keys()) == expected, (
        "AXE_REGISTER must hold exactly one entry per route per theme, plus the "
        "three deterministic states"
    )


def test_registered_keys_are_unique() -> None:
    """A duplicated key is silently last-wins in a JS object literal."""
    keys = _registered_keys()
    assert len(keys) == len(set(keys)), f"duplicate AXE_REGISTER keys: {keys}"


def test_every_registered_rule_is_written_up_in_the_exception_register() -> None:
    """A registered violation that nobody documented is a suppression.

    The register only stays honest while each rule it tolerates carries a named
    row explaining why it is not fixed and which owner-gated packet owns it.
    """
    rules = set(re.findall(r"rule: '([^']+)'", _register_block()))
    assert rules, "no rule ids parsed out of AXE_REGISTER"

    # As a code span, not a bare substring: `label` is a common English word in
    # this document, and a substring match would count prose about a `<label>`
    # element as documentation of axe's `label` rule.
    documented = EXCEPTIONS.read_text(encoding="utf-8")
    undocumented = sorted(rule for rule in rules if f"`{rule}`" not in documented)

    assert not undocumented, (
        f"{undocumented} are tolerated by AXE_REGISTER but appear nowhere in "
        f"{EXCEPTIONS.relative_to(REPO_ROOT).as_posix()}. Add the row, or fix the defect."
    )
