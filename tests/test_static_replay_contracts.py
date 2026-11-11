"""Source contracts for the E2E static-asset replay (#565, ADR-014).

Replay only lowers connection pressure if every browser-driving spec gets its
`test` from a module built on `e2e/static-replay.ts`. A spec that imports
`test` straight from `@playwright/test`, or builds its own contexts, silently
falls back to one connection per asset. These tests bind the wiring and name
the two deliberate exceptions.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
E2E = REPO_ROOT / "e2e"

REPLAY_FIXTURE_MODULES = ("./fixtures", "./console-guard", "./strict-fixtures")

# Spec -> why it stays on the native network.
NATIVE_EXCEPTIONS = {
    "api-integration.spec.ts": "uses only the `request` fixture and opens no browser page",
    "visual-baseline-thumbnails.spec.ts": "builds its own 18 contexts in the visual partition",
}

TEST_IMPORT = re.compile(r"import\s*\{([^}]*)\}\s*from\s*'([^']+)'")


def _read(name: str) -> str:
    path = E2E / name
    assert path.is_file(), f"{name} is missing from e2e/"
    return path.read_text(encoding="utf-8")


def _test_sources(source: str) -> set[str]:
    return {
        module
        for names, module in TEST_IMPORT.findall(source)
        if re.search(r"(^|[\s,])test([\s,]|$)", names)
    }


SPECS = sorted(path.name for path in E2E.glob("*.spec.ts"))


@pytest.mark.parametrize("spec", SPECS)
def test_every_spec_takes_test_from_a_replay_module_or_is_a_named_exception(spec: str) -> None:
    sources = _test_sources(_read(spec))
    assert sources, f"{spec} imports no `test`"
    if spec in NATIVE_EXCEPTIONS:
        return
    assert sources <= set(REPLAY_FIXTURE_MODULES), (
        f"{spec} takes `test` from {sorted(sources)}; use one of {REPLAY_FIXTURE_MODULES} "
        "or add it to NATIVE_EXCEPTIONS with the reason it must stay native"
    )


@pytest.mark.parametrize("spec", sorted(NATIVE_EXCEPTIONS))
def test_native_exceptions_still_exist_and_still_need_it(spec: str) -> None:
    sources = _test_sources(_read(spec))
    assert not sources <= set(REPLAY_FIXTURE_MODULES), (
        f"{spec} now uses a replay fixture module; remove it from NATIVE_EXCEPTIONS"
    )


@pytest.mark.parametrize("module", ["fixtures.ts", "console-guard.ts"])
def test_fixture_modules_extend_the_replay_base(module: str) -> None:
    source = _read(module)
    assert re.search(r"import \{ test as base \} from '\./static-replay';", source), (
        f"{module} must build its `test` on static-replay's base"
    )
    assert not re.search(r"\btest as base\b[^;]*from '@playwright/test'", source), (
        f"{module} takes its base from @playwright/test, bypassing replay"
    )


def test_replay_base_keeps_an_explicit_disable_switch() -> None:
    source = _read("static-replay.ts")
    assert "process.env.PW_STATIC_REPLAY !== '0'" in source
    assert re.search(r"staticReplay: \[[^\]]+\{ option: true \}\]", source)


def test_native_network_selection_runs_with_replay_disabled() -> None:
    source = _read("smoke-navigation.spec.ts")
    block = source.split("test.describe('Native static delivery (replay disabled)'", 1)
    assert len(block) == 2, "the native-network describe block is missing"
    assert "staticReplay: false" in block[1].split("test(", 1)[0]


# The one spec allowed to opt out per block, and to build its own contexts
# beyond the named exceptions: it owns the replay and native-network checks.
REPLAY_CHECKS_SPEC = "smoke-navigation.spec.ts"


@pytest.mark.parametrize("spec", SPECS)
def test_only_the_replay_checks_disable_replay_per_block(spec: str) -> None:
    if spec == REPLAY_CHECKS_SPEC:
        return
    source = _read(spec)
    assert "staticReplay" not in source and "PW_STATIC_REPLAY" not in source, (
        f"{spec} switches static replay itself; native-network coverage belongs in "
        f"{REPLAY_CHECKS_SPEC}, and a whole run uses PW_STATIC_REPLAY=0"
    )


@pytest.mark.parametrize("spec", SPECS)
def test_only_named_exceptions_build_their_own_contexts(spec: str) -> None:
    if spec in NATIVE_EXCEPTIONS or spec == REPLAY_CHECKS_SPEC:
        return
    assert "newContext(" not in _read(spec), (
        f"{spec} builds its own browser context, which bypasses the replay fixture; "
        "use the `context`/`page` fixtures, call installStaticReplay, or add a named exception"
    )
