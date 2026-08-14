"""Structural contracts over the release workflows.

pytest has no YAML parser available (PyYAML is not in requirements.txt), so this reads
the files by indentation, the same way `tests/test_compiled_css_drift_gate_contracts.py`
does -- generalized here to take a path, because this packet spans four workflow files.

**Every assertion below is guarded by the vacuity floor in the first test.** A parser
that silently stops matching turns "no job does X" into a statement about the empty
set. The floor asserts the parser still finds the jobs before anything else asks a
question about them.

Several contracts are deliberately *positive*: a negative scan for a forbidden string
scores green exactly when the line that carried the guarantee is deleted.
"""
import re

import pytest

from scripts.release_gate import (
    EXPECTED_CONTEXTS,
    RELEASE_JOB_IDS,
    REQUIRED_CONTEXTS,
    REPO_ROOT,
)

WORKFLOWS = REPO_ROOT / ".github" / "workflows"
CI = WORKFLOWS / "ci.yml"
DEEP_GATE = WORKFLOWS / "deep-gate.yml"
RELEASE = WORKFLOWS / "release.yml"
PACKAGED = WORKFLOWS / "_packaged-windows.yml"

ALL_WORKFLOWS = (CI, DEEP_GATE, RELEASE, PACKAGED)
NEW_WORKFLOWS = (RELEASE, PACKAGED)

REUSABLE_CALL = "uses: ./.github/workflows/_packaged-windows.yml"
PACKAGED_SMOKE_JOB_NAME = "Packaged Smoke (Windows bootloader, non-required)"
PACKAGED_CHILD_JOB_NAME = "Build and smoke"

# ci.yml job names that exist and are deliberately NOT part of the expected set.
UNEXPECTED_CI_JOB_NAMES = (
    "E2E Functional Shard ${{ matrix.shard }}/2",
    "JS Unit (Vitest, non-required)",
    "CSS Stylelint Measurement (non-required)",
    "JS Supply Chain (npm audit, non-required)",
    PACKAGED_SMOKE_JOB_NAME,
)

JOB_ID = re.compile(r"^  ([A-Za-z0-9_-]+):[ \t]*$", re.MULTILINE)
STEP_SPLIT = re.compile(r"^    - name: ", re.MULTILINE)
NAME_KEY = re.compile(r"^    name: (.+)$", re.MULTILINE)


def text(path):
    return path.read_text(encoding="utf-8")


def executable(path):
    """The file with whole-line comments removed.

    Every "this string must not appear" contract below has to read code rather than
    prose, or the comment explaining why a thing is forbidden becomes the reason the
    test reds. ci.yml says "NO --update-snapshots, here or anywhere in CI" in a
    comment; that sentence is the guarantee, not a violation of it.
    """
    return "\n".join(
        line for line in text(path).splitlines() if not line.lstrip().startswith("#")
    )


def jobs(path):
    """job id -> raw block, scoped to the `jobs:` mapping.

    Scoping matters: `on:` and `concurrency:` also carry two-space children, and a
    naive scan would report `push:` as a job.
    """
    source = text(path)
    start = re.search(r"^jobs:[ \t]*$", source, re.MULTILINE)
    assert start is not None, f"{path.name} has no jobs: mapping"
    body = source[start.end() :]

    found = {}
    matches = list(JOB_ID.finditer(body))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        found[match.group(1)] = body[match.start() : end]
    return found


def job_name(block):
    match = NAME_KEY.search(block)
    return match.group(1).strip() if match else None


def steps(block):
    """(step name, raw step text) for each step in a job block."""
    parts = STEP_SPLIT.split(block)
    return [(part.split("\n", 1)[0].strip(), part) for part in parts[1:]]


def _scopes(source, indent):
    match = re.search(
        rf"^{indent}permissions:[ \t]*\n((?:{indent}  [a-z-]+: [a-z]+\n)+)",
        source,
        re.MULTILINE,
    )
    if match is None:
        return None
    return dict(
        line.strip().split(": ", 1)
        for line in match.group(1).splitlines()
        if line.strip()
    )


def permissions(block):
    """The job's declared permissions mapping, or None when it declares none."""
    return _scopes(block, "    ")


# --------------------------------------------------------------- the vacuity floor


def test_the_parser_still_finds_every_job():
    """Nothing below means anything if this fails. Assert shape before content."""
    release_jobs = jobs(RELEASE)
    assert set(release_jobs) == set(RELEASE_JOB_IDS) | {"release-gate"}
    assert len(release_jobs) == 6

    assert set(jobs(PACKAGED)) == {"build-and-smoke"}

    ci_jobs = jobs(CI)
    assert len(ci_jobs) >= 17
    assert "packaged-smoke-windows" in ci_jobs
    assert len(jobs(DEEP_GATE)) == 7

    for path in ALL_WORKFLOWS:
        for job_id, block in jobs(path).items():
            assert job_name(block) or "uses:" in block, f"{path.name}:{job_id}"


# ------------------------------------------------- the expected-context list is real


def test_every_expected_context_is_a_real_ci_job_name():
    """Derived, not hand-copied.

    A rename of any of the twelve in ci.yml reds here instead of burning the release
    gate's 45-minute deadline on a name that will never report.
    """
    names = {job_name(block) for block in jobs(CI).values()}
    missing = sorted(set(EXPECTED_CONTEXTS) - names)
    assert not missing, f"expected contexts with no matching ci.yml job: {missing}"


def test_the_deliberately_excluded_ci_jobs_exist_and_stay_excluded():
    names = {job_name(block) for block in jobs(CI).values()}
    for name in UNEXPECTED_CI_JOB_NAMES:
        assert name in names, name
        assert name not in EXPECTED_CONTEXTS, name


def test_no_required_context_job_was_converted_to_a_reusable_call():
    """Converting a protected job to `uses:` renames its check to `parent / child`."""
    for job_id, block in jobs(CI).items():
        if job_name(block) in REQUIRED_CONTEXTS:
            assert "steps:" in block, job_id
            assert "uses: ./" not in block, job_id


def test_the_packaged_smoke_job_name_is_unchanged_and_its_child_is_pinned():
    block = jobs(CI)["packaged-smoke-windows"]
    assert job_name(block) == PACKAGED_SMOKE_JOB_NAME
    assert REUSABLE_CALL in block
    assert job_name(jobs(PACKAGED)["build-and-smoke"]) == PACKAGED_CHILD_JOB_NAME


# ----------------------------------------------------------- one build, two callers


def test_the_frozen_build_has_exactly_two_definitions_and_both_callers():
    """Counted by command shape. Counting the filename scores green on zero callers."""
    builds = sum(
        executable(path).count("pyinstaller --clean --noconfirm Hypertrophy-Toolbox.spec")
        for path in ALL_WORKFLOWS
    )
    smokes = sum(
        executable(path).count("python scripts/smoke_packaged_app.py")
        for path in ALL_WORKFLOWS
    )
    assert builds == 2, "expected _packaged-windows.yml and deep-gate.yml only"
    assert smokes == 2
    assert REUSABLE_CALL in executable(CI)
    assert REUSABLE_CALL in executable(RELEASE)


def test_the_smoke_keeps_the_upgrade_migration_run():
    """`--skip-upgrade` would delete the only automated proof that a user's existing
    database moves to the runtime root intact, while passing every other contract."""
    command = dict(steps(jobs(PACKAGED)["build-and-smoke"]))["Smoke the real bootloader"]
    assert "--mode bootloader" in command
    assert "--skip-upgrade" not in command
    assert "--skip-runtime" not in command
    assert "--mode payload" not in command


# ------------------------------------------------------------------- deep-gate stays put


@pytest.mark.parametrize(
    "fragment",
    [
        "  frozen-windows:",
        "name: Frozen executable (real bootloader, Windows)",
        "runs-on: windows-latest",
        "pyinstaller --clean --noconfirm Hypertrophy-Toolbox.spec",
        "--mode bootloader",
    ],
)
def test_deep_gate_still_carries_its_own_frozen_build(fragment):
    """Packet R2 converts this file; R1 must not."""
    assert fragment in text(DEEP_GATE)


def test_deep_gate_does_not_call_the_reusable_workflow():
    """The negative that actually catches R2 creep."""
    assert REUSABLE_CALL not in text(DEEP_GATE)


# ------------------------------------------------------------------ triggers and inputs


def test_the_tag_trigger_is_broad_and_not_semver_narrowed():
    source = text(RELEASE)
    assert "tags: ['v*']" in source
    for narrowed in ("v[0-9]", "v*.*.*", r"v\d"):
        assert narrowed not in source, narrowed


def test_dry_run_is_read_only_by_the_version_guard_and_actually_reaches_it():
    """Asserting only the absence elsewhere passes when the input is dropped entirely."""
    release_jobs = jobs(RELEASE)
    guard = release_jobs["version-guard"]
    assert "${{ inputs.dry_run }}" in guard
    assert "--dry-run" in guard
    for job_id, block in release_jobs.items():
        if job_id != "version-guard":
            assert "dry_run" not in block, job_id


def test_the_string_form_of_the_input_is_never_used():
    assert "github.event.inputs" not in executable(RELEASE)


# ------------------------------------------------------------- fan-in cannot be fooled


def test_the_fan_in_waits_on_exactly_the_expected_job_set():
    block = jobs(RELEASE)["release-gate"]
    listed = re.search(r"^    needs: \[(.+)\]$", block, re.MULTILINE)
    assert listed is not None
    assert sorted(part.strip() for part in listed.group(1).split(",")) == sorted(
        RELEASE_JOB_IDS
    )


def test_the_fan_in_runs_even_when_a_dependency_did_not():
    block = jobs(RELEASE)["release-gate"]
    assert re.search(r"^    if: always\(\)$", block, re.MULTILINE)
    assert "python scripts/release_gate.py fan-in" in block
    assert "RELEASE_NEEDS: ${{ toJSON(needs) }}" in block


# ------------------------------------------------------------ timeouts, ports, perms


def test_every_new_job_is_bounded_by_a_timeout():
    """A `uses:` job cannot declare `timeout-minutes`; the called workflow carries it."""
    for job_id, block in jobs(RELEASE).items():
        if REUSABLE_CALL in block:
            continue
        assert re.search(r"^    timeout-minutes: \d+$", block, re.MULTILINE), job_id
    assert re.search(
        r"^    timeout-minutes: \d+$", jobs(PACKAGED)["build-and-smoke"], re.MULTILINE
    )


@pytest.mark.parametrize(
    "job_id,port", [("first-install", "5124"), ("old-db-migration", "5125")]
)
def test_each_smoke_sets_its_own_port_and_probes_that_same_port(job_id, port):
    """Positive on purpose. `"5000" not in block` passes when HT_PORT is deleted --
    and utils/config.runtime_port() then defaults to 5000, which is the forbidden
    thing. The probe URL is checked too, so setting the variable without using it
    cannot score green."""
    block = jobs(RELEASE)[job_id]
    assert f"HT_PORT: '{port}'" in block
    assert f"http://127.0.0.1:{port}/" in block
    assert "127.0.0.1:5000" not in block


def test_the_packaged_smoke_serves_on_a_port_that_is_not_5000():
    source = executable(PACKAGED)
    assert "--port 5123" in source
    for forbidden in ("--port 5000", "HT_PORT: '5000'", "127.0.0.1:5000"):
        assert forbidden not in source, forbidden


@pytest.mark.parametrize("path", NEW_WORKFLOWS, ids=lambda p: p.name)
def test_every_new_job_has_an_explicit_read_only_token(path):
    """Positive on purpose. A job with no `permissions:` anywhere above it inherits
    the repository default, which is wider than an explicit `read`. The file-level
    block counts as the declaration; the absence of both does not."""
    file_level = _scopes(text(path), "")
    assert file_level, f"{path.name} declares no workflow-level permissions"
    assert set(file_level.values()) <= {"read", "none"}, path.name

    for job_id, block in jobs(path).items():
        if REUSABLE_CALL in block:
            continue
        effective = permissions(block) or file_level
        assert set(effective.values()) <= {"read", "none"}, f"{path.name}:{job_id}"


def test_the_provenance_job_asks_for_check_read():
    declared = permissions(jobs(RELEASE)["ci-provenance"])
    assert declared == {"contents": "read", "checks": "read"}


# --------------------------------------------------------- steps cannot skip quietly


@pytest.mark.parametrize("path", NEW_WORKFLOWS, ids=lambda p: p.name)
def test_no_step_carries_a_condition_that_could_skip_it_silently(path):
    """A conditional guard step that evaluates false leaves its job green while the
    assertion never ran. Only failure-path diagnostics may be conditional."""
    for job_id, block in jobs(path).items():
        for name, raw in steps(block):
            found = re.search(r"^      if: (.+)$", raw, re.MULTILINE)
            if found:
                assert found.group(1).strip() == "failure()", f"{job_id} / {name}"


@pytest.mark.parametrize("path", NEW_WORKFLOWS, ids=lambda p: p.name)
def test_no_assertion_hides_inside_an_and_list(path):
    """`[ "$a" = "200" ] && [ "$b" = "200" ]` does NOT fail a `set -e` step when the
    FIRST test fails: bash exempts every command in an && list except the last, so
    execution falls through and the step still reports success. Verified in bash.
    Each assertion has to stand alone.

    `[ ... ] && break` inside the readiness loop is fine and stays allowed: it is
    flow control, and the loop's outcome is asserted separately afterwards. What is
    forbidden is one test guarding another."""
    chained = re.compile(r"^\[ .+ \] &&\s*\[")
    for job_id, block in jobs(path).items():
        for name, raw in steps(block):
            for line in raw.splitlines():
                assert not chained.match(line.strip()), (
                    f"{path.name}:{job_id} / {name}: chained test -- {line.strip()}"
                )


# --------------------------------------------------------------- concurrency, snapshots


def test_the_release_concurrency_group_never_cancels_a_running_release():
    source = text(RELEASE)
    group = re.search(r"^  group: (.+)$", source, re.MULTILINE)
    assert group is not None
    assert "github.ref" in group.group(1)
    assert "${{ github.workflow }}" in group.group(1)
    assert re.search(r"^  cancel-in-progress: false$", source, re.MULTILINE)


@pytest.mark.parametrize("path", (CI, RELEASE, PACKAGED), ids=lambda p: p.name)
def test_the_pr_and_release_paths_can_never_write_a_visual_baseline(path):
    assert "--update-snapshots" not in executable(path)


def test_the_deep_gate_keeps_baseline_generation_behind_its_generate_mode():
    """deep-gate.yml is the one file allowed to hold `--update-snapshots`, and only
    on a `workflow_dispatch` that explicitly selects generate. Asserted rather than
    exempted, so this packet cannot be read as blessing an ungated occurrence."""
    source = executable(DEEP_GATE)
    assert source.count("--update-snapshots") == 1
    assert 'UPDATE=""; [ "$MODE" = "generate" ] && UPDATE="--update-snapshots"' in source
    assert '[ "${{ github.event_name }}" = "schedule" ] && MODE=compare' in source


# ------------------------------------------------- the release smokes assert no less


def _required_sets(block):
    """The required_columns / required_tables literals from an inline python block."""
    found = {}
    for key in ("required_columns", "required_tables"):
        match = re.search(rf"{key} = \{{(.*?)\}}", block, re.DOTALL)
        assert match is not None, key
        found[key] = set(re.findall(r'"([^"]+)"', match.group(1)))
    return found


def test_the_release_migration_smoke_asserts_at_least_what_the_deep_gate_does():
    """The two copies are allowed to exist; they are not allowed to diverge downward.
    This is the only gate anywhere that proves a user's saved program backups survive
    a schema upgrade."""
    release = _required_sets(jobs(RELEASE)["old-db-migration"])
    deep = _required_sets(jobs(DEEP_GATE)["old-db-migration"])

    assert deep["required_tables"] <= release["required_tables"]
    assert deep["required_columns"] <= release["required_columns"]
    assert {"program_backups", "program_backup_items"} <= release["required_tables"]
