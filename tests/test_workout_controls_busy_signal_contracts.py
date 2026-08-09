"""Contracts for the `data-workout-controls-busy` readiness signal.

Selecting an exercise starts a profile-estimate fetch whose response overwrites
the six Workout Controls. `networkidle` used to hide that race by waiting half a
second after all traffic stopped. Five workout-plan specs now use this signal
on their verified paths instead, which is precise and avoids the fixed
`networkidle` silence interval.

The signal is only sound if three things hold, and each fails silently:

* set **before the first `await`**, so a caller that has just dispatched the
  change event already observes it. Set it after the await and the wait becomes
  a no-op that passes instantly and races exactly as before;
* cleared in **`finally`**, so a rejected estimate cannot strand it and hang
  every later wait until timeout;
* the waiter must not quietly fall back to `networkidle`, which would restore
  the cost this replaced while still reporting success.

A fourth property is pinned here for diagnosability rather than correctness: the
waiter must name what it was waiting on when it times out. A bare
`waitForFunction` timeout reads as a generic page hang and sends the reader to
navigation instead of to the estimate.

Scope, deliberately: the marker is a **boolean observable**, not a refcount and
not a request generation. It is exact only while estimates are serialized, which
is what the converted E2E paths do. Overlapping estimates would clear it on the
first response to settle — a known limitation, not fixed here.

Evidence and mechanism: `docs/E2E_PERFORMANCE_PROFILE.md` finding 1.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ESTIMATES = REPO / "static" / "js" / "modules" / "workout-plan-estimates.js"
FIXTURES = REPO / "e2e" / "fixtures.ts"
SPEC = REPO / "e2e" / "validation-boundary.spec.ts"

ATTR = "data-workout-controls-busy"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def estimate_function() -> str:
    """The body of applyUserProfileEstimateForSelectedExercise()."""
    source = read(ESTIMATES)
    start = source.index("export async function applyUserProfileEstimateForSelectedExercise()")
    return source[start:]


def waiter_body() -> str:
    """The body of waitForWorkoutPlanReady(), up to its column-0 closing brace."""
    match = re.search(
        r"export async function waitForWorkoutPlanReady\(page: Page\): Promise<void> \{(.*?)\n\}",
        read(FIXTURES),
        re.DOTALL,
    )
    assert match is not None, "e2e/fixtures.ts no longer exports waitForWorkoutPlanReady"
    return match.group(1)


def test_attribute_name_is_declared_once_as_a_constant() -> None:
    source = read(ESTIMATES)
    assert f'CONTROLS_BUSY_ATTR = \'{ATTR}\'' in source, (
        "the attribute name must be a named constant, not repeated string literals"
    )


def test_marker_is_set_before_the_first_await() -> None:
    """Set it after the await and the waiter passes instantly and races anyway."""
    body = estimate_function()
    set_at = body.index("setAttribute(CONTROLS_BUSY_ATTR")
    first_await = body.index("await ")
    assert set_at < first_await, (
        "the busy marker must be set synchronously, before the first await, or a "
        "caller that just dispatched the change event will not observe it"
    )


def test_marker_is_cleared_in_a_finally_block() -> None:
    """A rejected estimate must not strand the marker and hang every later wait."""
    body = estimate_function()
    finally_at = body.index("} finally {")
    remove_at = body.index("removeAttribute(CONTROLS_BUSY_ATTR")
    assert finally_at < remove_at, "the busy marker must be cleared in `finally`"


def test_waiter_uses_the_signal_and_not_networkidle() -> None:
    body = waiter_body()
    assert ATTR in body, "the waiter must wait on the readiness signal"
    assert "networkidle" not in body, (
        "waitForWorkoutPlanReady must not fall back to networkidle -- that is the "
        "~500ms/navigation cost it exists to remove"
    )


def test_waiter_timeout_names_the_signal_and_the_estimate_wait() -> None:
    """A bare waitForFunction timeout names nothing and reads as a page hang.

    Without this, the failure that matters most -- an estimate that never settles
    or a stranded marker -- is indistinguishable from a slow navigation, and the
    next reader debugs the wrong half of the helper.
    """
    body = waiter_body()
    assert "catch" in body and "throw new Error(" in body, (
        "the estimate wait must convert its timeout into a named error"
    )

    diagnostic = body[body.index("catch"):]
    assert ATTR in diagnostic, (
        f"the timeout message must name {ATTR}, or the failure reads as a generic hang"
    )
    assert "estimate-readiness" in diagnostic, (
        "the timeout message must say which wait timed out, not just that one did"
    )
    assert "networkidle" not in diagnostic, (
        "the failure path must stay a rethrow -- no networkidle fallback smuggled in"
    )


def test_waiter_preserves_the_readiness_condition_and_its_tolerated_wait() -> None:
    """The diagnostic is message-only: same condition, same timeout budget."""
    body = waiter_body()
    assert "waitForLoadState('load')" in body, "the load half of the readiness wait must remain"
    assert f"hasAttribute('{ATTR}')" in body, "the marker predicate must be unchanged"
    assert "timeout" not in body.split("catch")[0], (
        "no explicit timeout may be introduced -- the tolerated wait stays whatever "
        "the Playwright default was before the diagnostic was added"
    )


def test_waitforpageready_remains_available_for_unconverted_paths() -> None:
    """Retained workout-plan paths and other pages still need the shared helper."""
    fixtures = read(FIXTURES)
    original = re.search(
        r"export async function waitForPageReady\(page: Page\): Promise<void> \{(.*?)\n\}",
        fixtures,
        re.DOTALL,
    )
    assert original is not None
    assert "networkidle" in original.group(1), (
        "waitForPageReady still backs retained and unconverted paths; changing it "
        "would roll the mechanism out without the per-path verification that gates it"
    )


def test_converted_spec_has_no_networkidle_path_left() -> None:
    spec = read(SPEC)
    assert "waitForWorkoutPlanReady" in spec
    assert "waitForPageReady" not in spec, "the converted spec must not keep both waits"
    assert "networkidle" not in spec


def test_converted_spec_waits_after_selecting_an_exercise() -> None:
    """The load-time wait is not enough: the race starts at exercise selection."""
    spec = read(SPEC)
    selector = spec.index("async function selectExercise(")
    body = spec[selector: spec.index("\n}", selector)]
    assert "selectOption" in body
    select_at = body.index("selectOption")
    assert "waitForWorkoutPlanReady" in body[select_at:], (
        "selectExercise() must wait for the estimate to land after selecting, or the "
        "tests type into fields the estimate response then overwrites"
    )
