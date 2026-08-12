"""Contracts for the compiled-SCSS drift gate in `frontend-build`.

`static/css/bootstrap.custom.min.css` and its `.map` are tracked build output.
The pytest job never runs npm, so the CSS contracts in `tests/test_css_*.py`
read the *committed* blob; every E2E job rebuilds it and drives the browser
against whatever the SCSS actually compiles to. Before the gate, a change to
`scss/` without a rebuild kept both halves green while they disagreed.

The gate is a clean-build-diff sequence in a workflow, which is exactly why it
needs pinning: nothing about a half-disarmed version looks wrong. Dropping
`.map` from a pathspec, skipping the pre-build delete so a no-longer-emitted
artifact survives from the checkout, swapping `exit $STATUS` for `exit 0`, or
adding `continue-on-error: true` all leave a step named "Fail on compiled-CSS
drift" sitting in a green pipeline, checking nothing.

Assertions here read parsed workflow fields, never raw substrings: the gate's
own failure branch prints a `git add <bundle> <map>` hint and the job carries
explanatory comments, so "is this string somewhere in the job" is true of a
thoroughly disarmed gate.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CI = REPO / ".github" / "workflows" / "ci.yml"
PACKAGE_JSON = REPO / "package.json"

JOB = "frontend-build"
# Live branch-protection required status check. Renaming it orphans the check
# and blocks every open PR, so the string is pinned, not derived.
JOB_DISPLAY_NAME = "Frontend Build (npm ci + SCSS)"

BUILD_COMMAND = "npm run build:css"
CLEAN_STEP = "Remove the tracked CSS build output before rebuilding"
BUILD_STEP = "Build Bootstrap-customized CSS"
DRIFT_STEP = "Fail on compiled-CSS drift"

STEP_START = re.compile(r"^    - name:\s*(.*)$")
STEP_KEY = re.compile(r"^      ([a-z-]+):\s*(.*)$")
JOB_KEY = re.compile(r"^    ([a-z-]+):\s*(.*)$")
RUN_INDENT = 8


def ci_text() -> str:
    return CI.read_text(encoding="utf-8")


def job_block(name: str) -> str:
    """The YAML body of one top-level job, up to the next job key."""
    match = re.search(
        rf"^  {re.escape(name)}:\n(.*?)(?=^  [A-Za-z0-9_-]+:\n|\Z)",
        ci_text(),
        re.MULTILINE | re.DOTALL,
    )
    assert match is not None, f"ci.yml no longer defines a '{name}' job"
    return match.group(1)


def parse_job(name: str) -> dict:
    """A structural read of one workflow job, by indentation.

    pytest has no YAML parser available (PyYAML is not in requirements.txt), and
    the contracts below must distinguish an executable key from prose in a
    comment. This reads only what they need: job-level keys, each step's name and
    `run:` body, and `continue-on-error:` at both levels. Comment lines never
    match the key patterns, so they drop out on their own.
    """
    job: dict = {"steps": []}
    step: dict | None = None
    run_lines: list[str] | None = None

    for raw in job_block(name).split("\n"):
        if run_lines is not None:
            if not raw.strip():
                run_lines.append("")
                continue
            if raw.startswith(" " * RUN_INDENT):
                run_lines.append(raw[RUN_INDENT:])
                continue
            assert step is not None
            step["run"] = "\n".join(run_lines)
            run_lines = None

        start = STEP_START.match(raw)
        if start:
            step = {"name": start.group(1).strip(), "run": ""}
            job["steps"].append(step)
            continue

        if step is not None:
            key = STEP_KEY.match(raw)
            if key:
                name_, value = key.group(1), key.group(2).strip()
                if name_ == "run" and value == "|":
                    run_lines = []
                else:
                    step[name_] = value
            continue

        key = JOB_KEY.match(raw)
        if key and key.group(1) != "steps":
            # `steps:` is the list being accumulated above, not a scalar to store.
            job[key.group(1)] = key.group(2).strip()

    if run_lines is not None and step is not None:
        step["run"] = "\n".join(run_lines)
    return job


def step_named(job: dict, name: str) -> dict | None:
    return next((s for s in job["steps"] if s["name"] == name), None)


def logical_commands(run: str) -> list[str]:
    """A `run:` body reduced to executable lines: comments dropped, `\\` joined."""
    commands: list[str] = []
    pending = ""
    for line in run.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.endswith("\\"):
            pending += stripped[:-1].strip() + " "
            continue
        commands.append((pending + stripped).strip())
        pending = ""
    if pending:
        commands.append(pending.strip())
    return commands


def command_starting_with(run: str, prefix: str) -> str | None:
    return next((c for c in logical_commands(run) if c.startswith(prefix)), None)


def build_output_paths() -> list[str]:
    """The bundle `npm run build:css` writes, plus its sourcemap sibling.

    Derived from package.json rather than restated, so redirecting sass at a new
    filename fails here instead of quietly orphaning the gate's pathspecs.
    """
    script = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))["scripts"]["build:css"]
    outputs = re.findall(r"static/css/\S+\.css", script)
    assert len(outputs) == 1, f"expected one CSS output in build:css, got {outputs}"
    return [outputs[0], outputs[0] + ".map"]


def cleanup_paths(job: dict) -> list[str]:
    step = step_named(job, CLEAN_STEP)
    assert step is not None, f"the '{CLEAN_STEP}' step is gone from {JOB}"
    command = command_starting_with(step["run"], "rm ")
    assert command is not None, f"the '{CLEAN_STEP}' step no longer removes anything"
    return [token for token in command.split()[1:] if not token.startswith("-")]


def gate_pathspec(job: dict) -> list[str]:
    step = step_named(job, DRIFT_STEP)
    assert step is not None, f"the '{DRIFT_STEP}' step is gone from {JOB}"
    command = command_starting_with(step["run"], "git diff --exit-code")
    assert command is not None, "the drift gate no longer runs `git diff --exit-code`"
    parts = command.split(" -- ", 1)
    assert len(parts) == 2, f"the gate's git diff has no `--` pathspec: {command}"
    return parts[1].split()


def test_the_gate_covers_exactly_the_two_tracked_build_artifacts() -> None:
    """Both artifacts, in both pathspecs, and both still tracked.

    The map is not redundant. It records which SCSS sources and line offsets
    produced the bundle, so relocating a rule between partials can leave the
    minified CSS byte-identical and move only the map. Equality rather than
    containment, so a widened pathspec -- which would red the gate on unrelated
    working-tree changes -- fails here too.
    """
    expected = build_output_paths()
    job = parse_job(JOB)

    assert sorted(cleanup_paths(job)) == sorted(expected), (
        f"the pre-build cleanup removes {sorted(cleanup_paths(job))}, expected {sorted(expected)}"
    )
    assert sorted(gate_pathspec(job)) == sorted(expected), (
        f"the drift gate checks {sorted(gate_pathspec(job))}, expected {sorted(expected)}"
    )

    # `git diff` is silent about untracked paths. Adding either artifact to
    # .gitignore would not fail the workflow -- it would make the diff vacuously
    # clean and the whole sequence decorative.
    listed = subprocess.run(
        ["git", "ls-files", "--", *expected],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    assert sorted(listed) == sorted(expected), (
        f"expected both compiled artifacts to be tracked, git listed {listed}"
    )


def test_the_gate_can_actually_fail_the_required_job() -> None:
    """A gate that cannot turn the job red is decoration.

    Four independent ways to disarm it without touching the diff itself: drop
    `--exit-code`, discard the captured status by ending on `exit 0`, mark the
    step or the job `continue-on-error`, or rename the job away from the context
    branch protection actually requires.
    """
    job = parse_job(JOB)
    assert job.get("name") == JOB_DISPLAY_NAME, (
        f"'{JOB}' display name is {job.get('name')!r}; branch protection requires "
        f"{JOB_DISPLAY_NAME!r} byte-for-byte"
    )
    assert job.get("continue-on-error") is None, (
        "frontend-build must not set continue-on-error; it would swallow the gate"
    )

    step = step_named(job, DRIFT_STEP)
    assert step is not None, f"the '{DRIFT_STEP}' step is gone from {JOB}"
    assert step.get("continue-on-error") is None, (
        f"the '{DRIFT_STEP}' step must not set continue-on-error"
    )

    commands = logical_commands(step["run"])
    assert any(c.startswith("git diff --exit-code") for c in commands), (
        "the gate's verdict must come from `git diff --exit-code`"
    )
    assert "STATUS=$?" in commands, "the gate no longer captures the diff's exit status"
    assert commands[-1] == "exit $STATUS", (
        f"the gate must end on `exit $STATUS`, not {commands[-1]!r}"
    )


def test_the_job_cleans_then_builds_then_checks_with_one_compiler() -> None:
    """Order is the whole mechanism, and each pair matters for its own reason.

    Cleanup before build: from an empty start, an artifact the compiler stops
    emitting (`--no-source-map`) is a deletion the diff reports, instead of a
    stale committed copy surviving from the checkout and diffing clean.

    Build before drift: `git diff` compares the working tree to the index, so a
    gate ahead of the build would diff a pristine checkout against itself and
    pass unconditionally.
    """
    job = parse_job(JOB)
    names = [s["name"] for s in job["steps"]]
    for required in (CLEAN_STEP, BUILD_STEP, DRIFT_STEP):
        assert required in names, f"{JOB} no longer has the '{required}' step"
    assert names.index(CLEAN_STEP) < names.index(BUILD_STEP) < names.index(DRIFT_STEP), (
        f"expected cleanup -> build -> drift, got {names}"
    )

    # One compiler path, invoked through the npm script every other job uses. A
    # direct `sass`/`npx sass` call could pass different flags and make the gate
    # assert against a bundle nothing else in the pipeline builds.
    build = step_named(job, BUILD_STEP)
    assert build is not None and build.get("run") == BUILD_COMMAND, (
        f"the '{BUILD_STEP}' step runs {build and build.get('run')!r}, expected {BUILD_COMMAND!r}"
    )
    assert not re.search(r"(npx |^\s*)sass ", ci_text(), re.MULTILINE)
