"""Contracts for Volume Splitter's initialization-only readiness signal.

The page fires ``GET /api/volume_history`` from its DOMContentLoaded
initializer without awaiting it.  ``networkidle`` used to make the E2E setup
wait for both that useful work and a fixed half-second silence window.  Packet C
replaces only the Volume Splitter spec's measured paths with a precise
``data-volume-history-busy`` lifecycle.

The signal deliberately wraps only the initial load.  ``loadVolumeHistory`` is
also called after save, delete, and active-plan actions; those are user-action
lifecycles with their own observables and must not be folded into page readiness.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VOLUME_SPLITTER = REPO / "static" / "js" / "modules" / "volume-splitter.js"
FIXTURES = REPO / "e2e" / "fixtures.ts"
SPEC = REPO / "e2e" / "volume-splitter.spec.ts"

ATTR = "data-volume-history-busy"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def function_body(source: str, signature: str) -> str:
    start = source.index(signature)
    remainder = source[start:]
    match = re.search(r"^}\s*$", remainder, re.MULTILINE)
    assert match is not None, f"could not find the end of {signature}"
    return remainder[: match.end()]


def waiter_body() -> str:
    source = read(FIXTURES)
    return function_body(
        source,
        "export async function waitForVolumeSplitterReady(page: Page): Promise<void>",
    )


def test_attribute_name_is_declared_once_as_a_constant() -> None:
    source = read(VOLUME_SPLITTER)
    assert f"VOLUME_HISTORY_BUSY_ATTR = '{ATTR}'" in source
    assert source.count(ATTR) == 1, "production JS must use the named constant"


def test_initial_marker_is_set_before_the_first_await() -> None:
    source = read(VOLUME_SPLITTER)
    body = function_body(source, "async function loadInitialVolumeHistory()")
    assert body.index("setAttribute(VOLUME_HISTORY_BUSY_ATTR") < body.index("await ")


def test_initial_marker_is_cleared_in_finally() -> None:
    source = read(VOLUME_SPLITTER)
    body = function_body(source, "async function loadInitialVolumeHistory()")
    assert body.index("} finally {") < body.index(
        "removeAttribute(VOLUME_HISTORY_BUSY_ATTR"
    )


def test_initializer_uses_the_initial_wrapper_not_the_action_loader() -> None:
    source = read(VOLUME_SPLITTER)
    body = function_body(source, "export function initializeVolumeSplitter()")
    assert "loadInitialVolumeHistory();" in body
    assert "loadVolumeHistory();" not in body


def test_user_action_history_refreshes_do_not_toggle_readiness() -> None:
    source = read(VOLUME_SPLITTER)
    body = function_body(source, "function loadVolumeHistory()")
    assert "VOLUME_HISTORY_BUSY_ATTR" not in body


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
    assert "initial volume-history" in diagnostic
    assert "volume-splitter.js" in diagnostic
    assert "networkidle" not in diagnostic


def test_generic_waiter_remains_for_unconverted_pages() -> None:
    source = read(FIXTURES)
    body = function_body(
        source,
        "export async function waitForPageReady(page: Page): Promise<void>",
    )
    assert "networkidle" in body


def test_volume_splitter_spec_is_exactly_converted() -> None:
    spec = read(SPEC)
    assert "waitForVolumeSplitterReady" in spec
    assert spec.count("await waitForVolumeSplitterReady(page);") == 3
    assert "waitForPageReady" not in spec
    assert "networkidle" not in spec

