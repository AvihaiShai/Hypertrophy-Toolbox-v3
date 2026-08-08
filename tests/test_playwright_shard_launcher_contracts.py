"""Contracts for the local isolated-shard launcher's spec selection.

`scripts/run-playwright-shards.ps1` exists to measure how long the required
functional gate takes when it is split across isolated processes. That number is
only usable if the launcher runs the same specs the gate runs.

Nothing about a drifted list looks wrong at a glance. The run passes, the timings
look plausible, and the conclusion drawn from them -- how many shards CI should
use -- is quietly about a different suite. So the equivalence is asserted here,
derived from `ci.yml` rather than from a second hand-kept copy.

The launcher also must not pull in specs whose cost or side effects would
poison a repeated benchmark: the four local-only functional specs, and anything
that captures a screenshot.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
LAUNCHER = REPO / "scripts" / "run-playwright-shards.ps1"
CI = REPO / ".github" / "workflows" / "ci.yml"
E2E = REPO / "e2e"

SPEC_TOKEN = re.compile(r"e2e/[A-Za-z0-9._-]+\.spec\.ts")

# Local-only functional specs, excluded from the benchmark by decision.
EXPECTED_EXCLUSIONS = {
    "e2e/erase-flow.spec.ts",
    "e2e/fatigue-context.spec.ts",
    "e2e/listener-cleanup.spec.ts",
    "e2e/program-backup.spec.ts",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def launcher_array(name: str) -> list[str]:
    body = re.search(rf"\${name}\s*=\s*@\((.*?)\n\)", read(LAUNCHER), re.DOTALL)
    assert body is not None, f"run-playwright-shards.ps1 no longer declares ${name}"
    return SPEC_TOKEN.findall(body.group(1))


def ci_required_specs() -> list[str]:
    """The spec list the `e2e-functional-shard` matrix actually runs."""
    text = read(CI)
    step = re.search(
        r"- name: Run functional specs \(shard(.*?)(?=\n    - name: |\Z)", text, re.DOTALL
    )
    assert step is not None, "ci.yml no longer has a 'Run functional specs' step"
    return SPEC_TOKEN.findall(step.group(1))


def test_launcher_runs_exactly_the_required_gate() -> None:
    """The load-bearing one: benchmark set == gate set."""
    assert sorted(set(launcher_array("RequiredSpecs"))) == sorted(set(ci_required_specs()))


def test_required_set_is_the_expected_size() -> None:
    """A guard against both lists being edited together in the same wrong way."""
    assert len(set(ci_required_specs())) == 25


def test_excluded_specs_are_named_and_absent() -> None:
    assert set(launcher_array("ExcludedSpecs")) == EXPECTED_EXCLUSIONS
    assert not EXPECTED_EXCLUSIONS & set(launcher_array("RequiredSpecs"))


@pytest.mark.parametrize("spec", sorted(set(launcher_array("RequiredSpecs"))))
def test_every_benchmarked_spec_exists(spec: str) -> None:
    assert (REPO / spec).is_file(), f"{spec} is benchmarked but does not exist"


def test_no_screenshot_spec_is_benchmarked() -> None:
    """Screenshot specs need the visual seed and would compare against baselines.

    Derived from the specs themselves, so adding `toHaveScreenshot` to a spec in
    the required set fails here rather than producing baseline diffs inside a
    timing run.
    """
    snapshot_specs = {
        f"e2e/{path.name}"
        for path in sorted(E2E.glob("*.spec.ts"))
        if re.search(r"toHaveScreenshot\(|expectFullPageScreenshot\(", read(path))
    }
    assert not snapshot_specs & set(launcher_array("RequiredSpecs"))


def test_launcher_isolates_every_shared_resource() -> None:
    """Port, database, artifacts root, and report path must all be per-shard.

    Any one of these left shared turns a benchmark into a corruption test.
    """
    launcher = read(LAUNCHER)
    for assignment in (
        'PW_PORT = "$($shard.Port)"',
        "PW_DB_PATH = $shard.Database",
        "TEST_ARTIFACTS_DIR = $shard.Directory",
        "PLAYWRIGHT_JSON_OUTPUT_NAME = $shard.JsonReport",
    ):
        assert f"$env:{assignment}" in launcher, f"shards no longer isolate {assignment}"


def test_launcher_refuses_reuse_and_the_visual_seed() -> None:
    launcher = read(LAUNCHER)
    assert "Remove-Item Env:PW_REUSE_SERVER" in launcher, (
        "a reused server would be the previous shard's, on its database"
    )
    assert "Remove-Item Env:PW_VISUAL_SEED" in launcher, (
        "the visual seed leaves plan rows the required specs do not expect"
    )
    assert "--update-snapshots" not in launcher


def test_telemetry_is_opt_in() -> None:
    """The measured configuration must stay reproducible after instrumenting it.

    Telemetry was added after the N=1 baseline was recorded. If it ran by
    default, the committed 719.0s reference would describe a launcher nobody can
    run again.
    """
    launcher = read(LAUNCHER)
    assert "[switch] $Telemetry" in launcher
    assert "if ($Telemetry) {" in launcher


def test_telemetry_stops_by_sentinel_not_by_kill() -> None:
    """A killed sampler loses its buffered tail, which is the interesting part.

    The samples nearest a failure are the ones the diagnosis needs, so the
    sampler is asked to stop and given time to close its writer.
    """
    launcher = read(LAUNCHER)
    assert "New-Item -ItemType File -Force -Path $TelemetryStop" in launcher
    assert "$TelemetryProcess.WaitForExit(15000)" in launcher


def test_clean_start_gate_requires_a_run_marker_not_just_a_path() -> None:
    """A shell that cd'd into the worktree is not a leftover test process.

    Without this the gate reported three of its own sibling shells as leftovers
    and could never declare a clean start.
    """
    gate = read(REPO / "scripts" / "wait_for_clean_start.ps1")
    assert "$RunMarker" in gate
    assert "--shard=|app\\.py|prepare_e2e_db|prepare_visual_db" in gate
    assert "$_.CommandLine -match $RunMarker" in gate


def test_diagnostic_scripts_never_terminate_anything() -> None:
    """Diagnosis observes. Only the launcher's own cleanup path may kill.

    Scoping is by command line and ancestry, so an unrelated node/chromium/python
    belonging to another worktree must never be reachable by these scripts.
    """
    for name in ("wait_for_clean_start.ps1", "shard_telemetry.ps1"):
        text = read(REPO / "scripts" / name)
        for forbidden in ("Stop-Process", "taskkill", "kill()"):
            assert forbidden not in text, f"{name} can terminate processes"


def test_launcher_never_writes_live_data() -> None:
    launcher = read(LAUNCHER)
    assert "would write the live database" in launcher
    assert "would write under data/auto_backup" in launcher


def test_launcher_caches_the_process_handle() -> None:
    """Without this line every shard scores as failed, whatever the tests did.

    `Start-Process -PassThru` returns a Process whose ExitCode and ExitTime read
    as empty once the child exits, unless Handle has been dereferenced while it
    was alive. The first benchmark run hit exactly this: 477/477 passed and the
    launcher reported a failure with a wall time of -63921817341 seconds.

    It is asserted rather than left to review because the failure is silent in
    the direction that matters -- a null exit code compares unequal to 0, so a
    genuinely passing run is reported as broken and a real regression would be
    indistinguishable from it.
    """
    assert "$null = $shard.Process.Handle" in read(LAUNCHER)


def test_launcher_waits_for_every_shard_and_reports_each_exit_code() -> None:
    """A first-red early exit would hide which other shards also failed."""
    launcher = read(LAUNCHER)
    assert "$shard.Process.WaitForExit()" in launcher
    assert "$shard.ExitCode = $shard.Process.ExitCode" in launcher
    assert "taskkill.exe /PID $ProcessId /T /F" in launcher, (
        "without a tree kill, Ctrl+C orphans Flask and Chromium children"
    )
