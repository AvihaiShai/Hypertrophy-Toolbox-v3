"""Contracts for Body Composition's initialization-only readiness signal.

The second one-page slice of Packet C, mirroring
``test_volume_history_busy_signal_contracts.py``. The page fires
``GET /api/body_composition/snapshots`` from its initializer without awaiting
it, and ``networkidle`` used to make the E2E setup wait for both that useful
work and a fixed half-second silence window.

The signal deliberately wraps only the initial load. ``loadHistory`` also runs
after a snapshot is saved and after one is deleted; those are user-action
lifecycles with their own observables (a prepended row, a removed row) and must
not be folded into page readiness.

One contract differs from the Volume Splitter set by necessity: this spec keeps
a single ``waitForPageReady`` call, because one of its tests starts on ``/`` to
exercise the navbar link and the home page has no readiness signal of its own.
Asserting the generic waiter is *absent* here — as the Volume Splitter contract
can — would force that navigation onto a marker that does not describe it.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BODY_COMPOSITION = REPO / "static" / "js" / "modules" / "body-composition.js"
FIXTURES = REPO / "e2e" / "fixtures.ts"
SPEC = REPO / "e2e" / "body-composition.spec.ts"

ATTR = "data-body-composition-history-busy"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def function_body(source: str, signature: str) -> str:
    """Slice a function body, ending at a brace at the signature's own indent.

    Unlike Volume Splitter's module-level equivalent, this page's loaders are
    nested inside ``bindForm()``. Deriving the closing indent from the signature
    keeps that working without hard-coding a width -- this module is 4-space and
    ``e2e/fixtures.ts``, read by the same helper, is 2-space.
    """
    start = source.index(signature)
    line_start = source.rfind("\n", 0, start) + 1
    indent = source[line_start:start]
    remainder = source[start:]
    match = re.search(rf"^{indent}}}\s*$", remainder, re.MULTILINE)
    assert match is not None, f"could not find the end of {signature}"
    return remainder[: match.end()]


def code_only(source: str) -> str:
    """Strip comments so a contract cannot be satisfied by prose.

    This module's own oracle comment names the assertion it deliberately avoids,
    which a bare substring check reads as the assertion being present — the same
    way a pinned CSS literal was once satisfied by a longer property that merely
    contained it.
    """
    without_blocks = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    return "\n".join(
        re.sub(r"(^|\s)//.*$", "", line)
        for line in without_blocks.splitlines()
        if not line.lstrip().startswith(("*", "//"))
    )


def waiter_body() -> str:
    return function_body(
        read(FIXTURES),
        "export async function waitForBodyCompositionReady(page: Page): Promise<void>",
    )


def test_attribute_name_is_declared_once_as_a_constant() -> None:
    source = read(BODY_COMPOSITION)
    assert f"HISTORY_BUSY_ATTR = '{ATTR}'" in source
    assert source.count(ATTR) == 1, "production JS must use the named constant"


def test_initial_marker_is_set_before_the_first_await() -> None:
    """A marker set after the request starts has a lost-wakeup race: a waiter
    can observe its absence and return while the fetch is already in flight."""
    body = function_body(read(BODY_COMPOSITION), "async function loadInitialHistory()")
    assert body.index("setAttribute(HISTORY_BUSY_ATTR") < body.index("await ")


def test_initial_marker_is_cleared_in_finally() -> None:
    """A rejected fetch must not strand the marker and hang every later wait."""
    body = function_body(read(BODY_COMPOSITION), "async function loadInitialHistory()")
    assert body.index("} finally {") < body.index("removeAttribute(HISTORY_BUSY_ATTR")


def test_initializer_calls_the_initial_wrapper_not_the_action_loader() -> None:
    source = read(BODY_COMPOSITION)
    assert "void loadInitialHistory();" in source
    assert "\n    loadHistory();\n" not in source, (
        "the initializer must go through the marked wrapper"
    )


def test_user_action_history_refreshes_do_not_toggle_readiness() -> None:
    """Save and delete both re-run loadHistory. Marking them would make page
    readiness describe user activity and go inexact if two ever overlap."""
    body = function_body(read(BODY_COMPOSITION), "async function loadHistory()")
    assert "HISTORY_BUSY_ATTR" not in body


def test_waiter_uses_the_signal_without_networkidle_or_timeout_inflation() -> None:
    body = waiter_body()
    assert "waitForLoadState('load')" in body
    assert f"hasAttribute('{ATTR}')" in body
    assert "networkidle" not in body
    assert "timeout" not in body.split("catch")[0]


def test_waiter_timeout_names_the_signal_and_production_lifecycle() -> None:
    body = waiter_body()
    diagnostic = body[body.index("catch") :]
    assert "throw new Error(" in diagnostic
    assert ATTR in diagnostic
    assert "snapshot-history" in diagnostic
    assert "body-composition.js" in diagnostic
    assert "networkidle" not in diagnostic


def test_generic_waiter_remains_for_unconverted_pages() -> None:
    body = function_body(
        read(FIXTURES),
        "export async function waitForPageReady(page: Page): Promise<void>",
    )
    assert "networkidle" in body


def test_body_composition_spec_is_exactly_converted() -> None:
    spec = code_only(read(SPEC))
    assert spec.count("await waitForBodyCompositionReady(page);") == 6
    # Exactly one generic wait survives, and it is the `/` navigation pinned
    # below. There is deliberately no "networkidle not in spec" assertion: this
    # spec still reaches it through that generic wait, so banning the word would
    # be false comfort and would forbid explaining why the site is unconverted.
    assert spec.count("await waitForPageReady(page);") == 1


def test_the_one_generic_wait_is_the_home_page_navigation() -> None:
    """Counts alone cannot tell which site kept the generic waiter.

    Swap the two calls in the navbar test and the 6/1 split is unchanged, every
    test still passes, and the guarantee is silently inverted -- a Body
    Composition marker on ``/`` simply resolves at ``load``.
    """
    spec = code_only(read(SPEC))
    navbar = spec[spec.index("navbar link routes to /body_composition") :]
    navbar = navbar[: navbar.index("test(", 1)] if "test(" in navbar[1:] else navbar
    assert navbar.index("page.goto('/')") < navbar.index("waitForPageReady(page)")
    assert navbar.index("navLink.click()") < navbar.index("waitForBodyCompositionReady(page)")
    assert navbar.index("waitForPageReady(page)") < navbar.index("navLink.click()")


def test_no_hard_wait_is_used_to_prove_the_helper_blocks() -> None:
    """The tempting way to strengthen the pending check is a sleep, which would
    move the inventory's pinned hard-wait tally and reintroduce what ADR-005
    spent a packet removing."""
    assert "waitForTimeout" not in code_only(read(SPEC))


def test_the_waiter_owns_only_its_own_page_signal() -> None:
    body = waiter_body()
    assert "data-volume-history-busy" not in body
    assert "data-workout-controls-busy" not in body


def test_the_readiness_oracle_asserts_the_wait_actually_blocks() -> None:
    """Without this, the helper could be a no-op and every test still pass."""
    spec = code_only(read(SPEC))
    assert "Body Composition initial readiness" in spec
    assert f"toHaveAttribute('{ATTR}', '1')" in spec
    assert "readySettled," in spec and "toBe(false)" in spec
    assert "expect.poll(() => readySettled)" not in spec, (
        "poll succeeds on its first satisfying observation, so it cannot tell "
        "a blocked wait from one that is about to resolve"
    )
    assert "data-bc-trend-line" in spec, (
        "the oracle must prove the render ran, not just that the marker cleared"
    )
    # Non-retrying reads must precede retrying matchers, or a render that
    # completed *after* the helper returned is absorbed instead of caught.
    oracle = spec[spec.index("Body Composition initial readiness") :]
    assert oracle.index("getAttribute('points')") < oracle.index("toBeHidden()")
