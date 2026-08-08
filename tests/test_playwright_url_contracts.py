"""Contracts pinning the Playwright harness's port, base URL, and database together.

Sharding gives each Playwright process its own port, its own SQLite file, and
its own artifacts root. Four values have to agree for that to work, and they are
written in four different places:

* the port Flask listens on (``HT_PORT``, read by ``utils.config.runtime_port``),
* the URL ``webServer`` polls to decide the app is up,
* the ``baseURL`` specs and the ``request`` fixture resolve relative paths against,
* the ``DB_FILE`` the app opens.

A mismatch between the first three does not fail loudly. The server binds fine,
the browser drives a port nobody is serving, and the run hangs for the full 120s
``webServer`` timeout with no message naming the cause. A mismatch on the fourth
is worse: two shards quietly share one SQLite file.

So the config derives all of them from single bindings, and these tests assert
that it still does. They are static, cost no browser time, and fail in pytest
where the cause is legible -- rather than as a timeout hours into a shard run.

The exception is :func:`test_app_honours_the_port_the_config_passes`, which runs
the real resolver. Static text can prove the config *sends* ``HT_PORT``; only
calling the app's own code proves sending it does anything.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / "playwright.config.ts"
PROBE = REPO / "scripts" / "css_audit" / "runtime_probe.mjs"
E2E = REPO / "e2e"

# Any absolute loopback origin. The point of the sweep is that a spec must not
# name a host at all, so this deliberately matches every port, not just 5000.
HOST_ORIGIN = re.compile(r"https?://(?:127\.0\.0\.1|localhost):\d+")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def web_server_block() -> str:
    """The `webServer: { ... }` object literal from the config.

    Matched to the two-space closing brace so the four-space `env: { ... }`
    nested inside does not terminate it early.
    """
    match = re.search(r"\n  webServer:\s*\{(.*?)\n  \},", read(CONFIG), re.DOTALL)
    assert match is not None, "playwright.config.ts no longer declares a webServer block"
    return match.group(1)


def use_block() -> str:
    match = re.search(r"\n  use:\s*\{(.*?)\n  \},", read(CONFIG), re.DOTALL)
    assert match is not None, "playwright.config.ts no longer declares a top-level use block"
    return match.group(1)


def test_base_url_is_derived_from_the_resolved_port() -> None:
    """One port produces the base URL; it is not spelled out a second time."""
    config = read(CONFIG)
    assert re.search(r"^const port = resolvePort\(\);$", config, re.MULTILINE)
    assert re.search(
        r"^const baseURL = process\.env\.PW_BASE_URL \|\| `http://\$\{DEFAULT_HOST\}:\$\{port\}`;$",
        config,
        re.MULTILINE,
    )


def test_test_base_url_is_the_shared_binding() -> None:
    """`use.baseURL` must be the binding, not a literal that happens to match."""
    assert re.search(r"^\s*baseURL,$", use_block(), re.MULTILINE), (
        "use.baseURL stopped referencing the resolved binding"
    )


def test_web_server_polls_the_same_url_the_tests_drive() -> None:
    assert re.search(r"^\s*url: baseURL,$", web_server_block(), re.MULTILINE), (
        "webServer.url drifted away from baseURL; a shard would poll one port "
        "and drive another"
    )


def test_web_server_serves_flask_on_the_resolved_port() -> None:
    assert re.search(r"^\s*HT_PORT: String\(port\),$", web_server_block(), re.MULTILINE), (
        "webServer no longer passes the resolved port to Flask, so the app "
        "would fall back to 5000 regardless of PW_PORT"
    )


def test_web_server_opens_the_parameterized_database() -> None:
    assert re.search(r"^\s*DB_FILE: e2eDbPath,$", web_server_block(), re.MULTILINE)
    assert re.search(
        r"^const e2eDbPath = path\.resolve\($", read(CONFIG), re.MULTILINE
    ), "the e2e DB path stopped resolving from PW_DB_PATH"
    assert "process.env.PW_DB_PATH" in read(CONFIG)


def test_a_disagreeing_base_url_is_rejected_rather_than_ranked() -> None:
    """PW_BASE_URL and PW_PORT disagreeing must throw, not pick a winner.

    A precedence rule is something a caller has to remember. A throw is not.
    """
    config = read(CONFIG)
    assert "PW_BASE_URL (${baseURL}) and the resolved port (${port}) disagree" in config
    assert re.search(r"if \(process\.env\.PW_BASE_URL\) \{", config)


@pytest.mark.parametrize(
    ("name", "pattern"),
    [
        ("port", r"^const DEFAULT_PORT = 5000;$"),
        ("host", r"^const DEFAULT_HOST = '127\.0\.0\.1';$"),
        ("database", r"path\.join\('artifacts', 'e2e', 'database\.e2e\.db'\)"),
        ("artifacts root", r"^const artifactsRoot = process\.env\.TEST_ARTIFACTS_DIR \?\? 'artifacts';$"),
        ("workers", r"^const configuredWorkers = Number\(process\.env\.PW_WORKERS \?\? '1'\);$"),
    ],
)
def test_unset_environment_keeps_the_previous_defaults(name: str, pattern: str) -> None:
    """Parameterizing must not have moved the default for anyone who sets nothing."""
    assert re.search(pattern, read(CONFIG), re.MULTILINE), f"the default {name} changed"


def test_no_playwright_source_hardcodes_an_origin() -> None:
    """Specs and helpers navigate relative paths; only the config names a host.

    Asserted across every `.ts` under e2e/ rather than a fixed list, so a new
    spec that pastes an absolute URL fails here instead of pinning the whole
    suite back to port 5000.
    """
    offenders = {
        f"e2e/{path.name}": sorted(set(HOST_ORIGIN.findall(read(path))))
        for path in sorted(E2E.rglob("*.ts"))
        if HOST_ORIGIN.search(read(path))
    }
    assert not offenders, (
        "hard-coded origins block sharding -- these resolve to one fixed port "
        f"no matter which port the shard's server owns: {offenders}"
    )


def test_runtime_probe_drives_the_port_it_starts() -> None:
    """The probe spawns its own Flask, so its readiness poll must match it.

    This was a real silent defect, not a hypothetical: with the poll pinned to
    5000, a probe run while another checkout held that port succeeded on the
    first attempt, ignored the server it had just spawned, and captured the
    other worktree's CSS.
    """
    probe = read(PROBE)
    assert "const PROBE_PORT = Number(process.env.PW_PORT || DEFAULT_PORT);" in probe
    assert "HT_PORT: String(PROBE_PORT)," in probe, (
        "the probe stopped telling its spawned app which port to serve"
    )
    assert "connect({ host: DEFAULT_HOST, port: PROBE_PORT })" in probe, (
        "the readiness poll drifted from the port the probe starts"
    )
    assert not re.search(r"port: 5000", probe), "a literal port survived in the probe"


def test_app_honours_the_port_the_config_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    """`HT_PORT` has to reach the server, or the whole chain above is decorative.

    Behavioral on purpose. Every other test here reads text; this one calls the
    resolver app.py calls, so `webServer.env.HT_PORT` is proven to land.
    """
    from utils.config import DEFAULT_PORT, runtime_port

    monkeypatch.delenv("HT_PORT", raising=False)
    assert runtime_port() == DEFAULT_PORT == 5000

    monkeypatch.setenv("HT_PORT", "5231")
    assert runtime_port() == 5231
