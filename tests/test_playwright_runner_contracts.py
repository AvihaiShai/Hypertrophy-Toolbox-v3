"""Contracts for the local Playwright wrapper's seed routing.

`playwright.config.ts` chooses the throwaway DB's seeder from `PW_VISUAL_SEED`
and seeds it inside the `webServer` command, before Flask opens it. Two seeds
exist and they are not interchangeable:

* `prepare_e2e_db.py` — catalog preserved, all user state wiped. The functional
  default.
* `prepare_visual_db.py` — plan-bearing, `media_path` thumbnails intact,
  catalog already upgraded.

A spec routed to the wrong seed does not error; it renders a different page and
fails on content, or worse, passes for the wrong reason. `scripts/run-playwright.ps1`
had exactly that defect: it recognized only the literal `visual.spec.ts`, left
the other two visual-seed consumers in the functional group, and reached for
`DB_FILE` — which `playwright.config.ts` unconditionally overrides in
`webServer.env`, so the override was inert and the "visual" run used the
functional seed.

These are static contracts. They cost no browser time and they fail in pytest,
where a routing regression is cheap to see, rather than as a puzzling visual
diff hours later.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
RUNNER = REPO / "scripts" / "run-playwright.ps1"
CONFIG = REPO / "playwright.config.ts"
DEEP_GATE = REPO / ".github" / "workflows" / "deep-gate.yml"
E2E = REPO / "e2e"

SPEC_TOKEN = re.compile(r"e2e/[A-Za-z0-9._-]+\.spec\.ts")

# The prefix names what a spec measures, not how. `visual-field-separator`
# reads composited computed styles and asserts a numeric contrast ratio, takes
# no screenshot, injects its own rows, and runs on the required PR path — so it
# needs the functional seed. Routing it by prefix would break the required gate.
PREFIX_TRAP = "e2e/visual-field-separator.spec.ts"

EXACT_VISUAL_SEED_SPECS = {
    "e2e/visual.spec.ts",
    "e2e/visual-baseline-thumbnails.spec.ts",
    "e2e/workout-plan-desktop-contract.spec.ts",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def runner_visual_group() -> list[str]:
    """The `$VisualSeedSpecs` array literal from the wrapper."""
    body = re.search(
        r"\$VisualSeedSpecs\s*=\s*@\((.*?)\)", read(RUNNER), re.DOTALL
    )
    assert body is not None, "run-playwright.ps1 no longer declares $VisualSeedSpecs"
    return SPEC_TOKEN.findall(body.group(1))


def deep_gate_visual_group() -> list[str]:
    """The spec list the `visual-linux` job runs under PW_VISUAL_SEED=1."""
    text = read(DEEP_GATE)
    step = re.search(
        r"- name: Run visual specs(.*?)(?=\n    - name: |\Z)", text, re.DOTALL
    )
    assert step is not None, "deep-gate.yml no longer has a 'Run visual specs' step"
    assert "PW_VISUAL_SEED" in step.group(1), (
        "the visual-linux step stopped setting PW_VISUAL_SEED; local and CI "
        "seeding would diverge silently"
    )
    return SPEC_TOKEN.findall(step.group(1))


def deep_gate_full_e2e_script() -> str:
    """The Bash body used by the deep gate's functional-suite selection step."""
    text = read(DEEP_GATE)
    step = re.search(
        r"- name: Run full suite \(minus visual\)(.*?)(?=\n    - name: |\Z)",
        text,
        re.DOTALL,
    )
    assert step is not None, (
        "deep-gate.yml no longer has a 'Run full suite (minus visual)' step"
    )
    marker = "      run: |\n"
    assert step.group(1).count(marker) == 1
    return textwrap.dedent(step.group(1).split(marker, 1)[1])


def bash_executable() -> str:
    candidates = [shutil.which("bash")]
    git = shutil.which("git")
    if git:
        candidates.append(str(Path(git).resolve().parents[1] / "bin" / "bash.exe"))
    program_files = os.environ.get("ProgramFiles")
    if program_files:
        candidates.append(str(Path(program_files) / "Git" / "bin" / "bash.exe"))
    found = next(
        (
            candidate
            for candidate in candidates
            if candidate and Path(candidate).is_file()
        ),
        None,
    )
    assert found is not None, "Bash is required to verify the Ubuntu deep-gate selector"
    return found


def run_full_e2e_script(
    script: str, root: Path, inventory: set[str]
) -> tuple[subprocess.CompletedProcess[bytes], list[str] | None]:
    root.mkdir(parents=True)
    (root / "e2e").mkdir()
    for relative_path in inventory:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    wrapper = """set -euo pipefail
npx() {
  printf '__PLAYWRIGHT_ARGV__\\0'
  printf '%s\\0' "$@"
}
""" + script
    result = subprocess.run(
        [bash_executable(), "-c", wrapper],
        cwd=root,
        capture_output=True,
        check=False,
    )
    marker = b"__PLAYWRIGHT_ARGV__\0"
    if marker not in result.stdout:
        return result, None
    encoded = result.stdout.split(marker, 1)[1].rstrip(b"\0")
    return result, encoded.decode("utf-8").split("\0")


def assert_full_e2e_selector_contract(script: str, root: Path) -> None:
    current = {f"e2e/{path.name}" for path in E2E.glob("*.spec.ts")}
    assert len(current) == 33
    assert len(EXACT_VISUAL_SEED_SPECS) == 3
    assert EXACT_VISUAL_SEED_SPECS <= current
    expected_current = current - EXACT_VISUAL_SEED_SPECS
    assert len(expected_current) == 30

    result, argv = run_full_e2e_script(script, root / "current", current)
    assert result.returncode == 0, result.stderr.decode()
    assert argv is not None
    assert argv[:3] == ["playwright", "test", "--project=chromium"]
    assert len(argv[3:]) == 30
    assert set(argv[3:]) == expected_current

    near_and_punctuated = {
        "e2e/nonvisual.spec.ts",
        "e2e/not-visual-baseline-thumbnails.spec.ts",
        "e2e/pre-workout-plan-desktop-contract.spec.ts",
        "e2e/functional [one].spec.ts",
        "e2e/functional;two.spec.ts",
    }
    fabricated = EXACT_VISUAL_SEED_SPECS | near_and_punctuated
    result, argv = run_full_e2e_script(script, root / "near-names", fabricated)
    assert result.returncode == 0, result.stderr.decode()
    assert argv is not None
    assert argv[:3] == ["playwright", "test", "--project=chromium"]
    assert len(argv[3:]) == len(near_and_punctuated)
    assert set(argv[3:]) == near_and_punctuated

    for index, excluded in enumerate(sorted(EXACT_VISUAL_SEED_SPECS)):
        inventory = fabricated - {excluded}
        result, argv = run_full_e2e_script(script, root / f"missing-{index}", inventory)
        assert result.returncode != 0
        assert argv is None

    for name, inventory in (
        ("empty", set()),
        ("excluded-only", EXACT_VISUAL_SEED_SPECS),
    ):
        result, argv = run_full_e2e_script(script, root / name, inventory)
        assert result.returncode != 0
        assert argv is None


def test_runner_and_ci_agree_on_the_visual_seed_group(tmp_path: Path) -> None:
    """Local and CI must seed the same specs the same way.

    This is the load-bearing one. Everything else here is a property of one
    file; this is the equivalence that makes a local visual run mean what a
    deep-gate run means.
    """
    assert sorted(set(runner_visual_group())) == sorted(set(deep_gate_visual_group()))

    inventory = {f"e2e/{path.name}" for path in E2E.glob("*.spec.ts")}
    visual_seed_specs = set(deep_gate_visual_group())
    assert visual_seed_specs == EXACT_VISUAL_SEED_SPECS
    assert PREFIX_TRAP in inventory - visual_seed_specs

    script = deep_gate_full_e2e_script()
    assert_full_e2e_selector_contract(script, tmp_path / "live")

    mutation_patterns = {
        "selector": r'\nfor spec in "\$\{DISCOVERED_SPECS\[@\]\}"; do.*?\ndone\n',
        "nonempty-guard": r'\nif \(\( \$\{#SPECS\[@\]\} == 0 \)\); then.*?\nfi\n',
        "playwright-invocation": r'\nnpx playwright test --project=chromium "\$\{SPECS\[@\]\}"\n',
    }
    for name, pattern in mutation_patterns.items():
        mutated, count = re.subn(pattern, "\n", script, count=1, flags=re.DOTALL)
        assert count == 1, f"mutation target disappeared: {name}"
        with pytest.raises(AssertionError):
            assert_full_e2e_selector_contract(mutated, tmp_path / name)


def test_visual_seed_group_is_exactly_the_three_known_consumers() -> None:
    # The desktop contract is not a snapshot spec; it carries the five
    # byte-gate-exempt captures' coverage over visual-seed plan rows.
    assert set(runner_visual_group()) == EXACT_VISUAL_SEED_SPECS


@pytest.mark.parametrize("spec", sorted(set(runner_visual_group())))
def test_every_routed_spec_exists(spec: str) -> None:
    assert (REPO / spec).is_file(), f"{spec} is routed but does not exist"


def test_snapshot_taking_specs_are_all_routed_to_the_visual_seed() -> None:
    """Forward-looking: a new snapshot spec cannot quietly land in the wrong group.

    Derived from the specs themselves rather than from a second hand-kept list,
    so adding a `toHaveScreenshot` call to a functional spec fails here instead
    of producing a baseline captured against wiped user state.
    """
    snapshot_specs = {
        f"e2e/{path.name}"
        for path in sorted(E2E.glob("*.spec.ts"))
        if re.search(r"toHaveScreenshot\(|expectFullPageScreenshot\(", read(path))
    }
    missing = snapshot_specs - set(runner_visual_group())
    assert not missing, (
        "specs take screenshots but run under the functional seed: "
        + ", ".join(sorted(missing))
    )


def test_the_visual_prefix_trap_stays_on_the_functional_seed() -> None:
    assert (REPO / PREFIX_TRAP).is_file()
    assert PREFIX_TRAP not in runner_visual_group(), (
        f"{PREFIX_TRAP} was routed by its name. It asserts a contrast ratio from "
        "computed styles, injects its own rows, and is a required PR check — it "
        "needs the functional seed."
    )


def test_runner_selects_the_seed_through_pw_visual_seed() -> None:
    runner = read(RUNNER)
    assert 'PW_VISUAL_SEED = "1"' in runner
    # Restoring matters: the wrapper may run both groups in one invocation, so a
    # leaked variable would seed a later functional run with plan rows.
    assert "Remove-Item Env:PW_VISUAL_SEED" in runner


def test_runner_does_not_reach_for_the_overridden_db_file() -> None:
    """`webServer.env` sets DB_FILE unconditionally, so setting it here is inert.

    Asserted as absence because the dead code was actively misleading: it looked
    like the visual run was getting its own database.
    """
    runner = read(RUNNER)
    assert "DB_FILE" not in runner
    assert "New-VisualDatabase" not in runner


def test_config_still_keys_seeding_on_pw_visual_seed() -> None:
    """The wrapper's contract is only meaningful while the config honors it."""
    config = read(CONFIG)
    assert "PW_VISUAL_SEED === '1'" in config
    assert "prepare_visual_db.py" in config
    assert "prepare_e2e_db.py" in config


def test_ci_timing_summary_reads_the_path_the_config_writes() -> None:
    """The summary step swallows errors, so a path drift would be silent.

    `|| true` keeps a reporting problem from reddening a passing shard, which
    also means a wrong path produces an empty summary and no signal at all.
    Pin the two ends together here instead.
    """
    ci = read(REPO / ".github" / "workflows" / "ci.yml")
    script = REPO / "scripts" / "playwright_timing_report.py"
    assert script.is_file()
    assert "playwright_timing_report.py" in ci

    # playwright.config.ts writes junit under its artifacts dir; the CI step
    # must read that same file.
    assert "'junit.xml'" in read(CONFIG)
    assert "artifacts/playwright/junit.xml" in ci


def test_functional_group_is_derived_by_exclusion() -> None:
    """A new spec must default into the functional group, not vanish.

    If the wrapper listed functional specs explicitly, adding a spec would
    silently exclude it from the default run — a spec that exists, passes
    locally when named, and is never run by `npm run test:e2e`.
    """
    assert "$VisualSeedSpecs -notcontains" in read(RUNNER)
