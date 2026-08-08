"""Contracts for the `data-workout-controls-busy` readiness signal.

Selecting an exercise starts a profile-estimate fetch whose response overwrites
the six Workout Controls. `networkidle` used to hide that race by waiting half a
second after all traffic stopped; `validation-boundary.spec.ts` now waits for
this signal instead, which is precise and ~500ms/navigation cheaper.

The signal is only sound if three things hold, and each fails silently:

* set **before the first `await`**, so a caller that has just dispatched the
  change event already observes it. Set it after the await and the wait becomes
  a no-op that passes instantly and races exactly as before;
* cleared in **`finally`**, so a rejected estimate cannot strand it and hang
  every later wait until timeout;
* the waiter must not quietly fall back to `networkidle`, which would restore
  the cost this replaced while still reporting success.

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
    fixtures = read(FIXTURES)
    waiter = re.search(
        r"export async function waitForWorkoutPlanReady\(page: Page\): Promise<void> \{(.*?)\n\}",
        fixtures,
        re.DOTALL,
    )
    assert waiter is not None, "e2e/fixtures.ts no longer exports waitForWorkoutPlanReady"
    body = waiter.group(1)
    assert ATTR in body, "the waiter must wait on the readiness signal"
    assert "networkidle" not in body, (
        "waitForWorkoutPlanReady must not fall back to networkidle -- that is the "
        "~500ms/navigation cost it exists to remove"
    )


def test_waitforpageready_is_unchanged_for_every_other_spec() -> None:
    """This packet converts one spec. The shared helper stays as it was."""
    fixtures = read(FIXTURES)
    original = re.search(
        r"export async function waitForPageReady\(page: Page\): Promise<void> \{(.*?)\n\}",
        fixtures,
        re.DOTALL,
    )
    assert original is not None
    assert "networkidle" in original.group(1), (
        "waitForPageReady still backs 21 unconverted specs; changing it here would "
        "roll the mechanism out without the per-spec verification that gates it"
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
