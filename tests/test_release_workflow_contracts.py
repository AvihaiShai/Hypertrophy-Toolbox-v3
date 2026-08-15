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
WORKFLOW_PATHS = {path.name: path for path in ALL_WORKFLOWS}

REUSABLE_CALL = "uses: ./.github/workflows/_packaged-windows.yml"
PACKAGED_SMOKE_JOB_NAME = "Packaged Smoke (Windows bootloader, non-required)"
PACKAGED_CHILD_JOB_NAME = "Build and smoke"

# Every job in the repository that calls the reusable Windows build, and the `name:`
# each one reports under. Packet R2-b folded `deep-gate.yml`'s `frozen-windows` in, so
# `_packaged-windows.yml` is now the only definition of that build anywhere and this
# mapping is the entire coupling between the PR pipeline, the release gate and the
# weekly deep gate.
#
# It is measured against the workflow files in BOTH directions below: a caller that
# stops calling reds, and a caller that appears without being declared here reds too.
# The second direction is the one that matters for a name -- a `uses:` job reports as
# `<caller name> / Build and smoke`, so adding a caller mints a new composite check
# name, and docs/ai_workflow/QUALITY_GATE.md requires that to be a deliberate act.
PACKAGED_CALLERS = {
    "ci.yml": ("packaged-smoke-windows", PACKAGED_SMOKE_JOB_NAME),
    "release.yml": ("packaged-windows", "Frozen Windows executable"),
    "deep-gate.yml": ("frozen-windows", "Frozen executable (real bootloader, Windows)"),
}

# The build's shape, stated once because it is now stored once. Order is load-bearing:
# staging writes the manifest.sha256 that the smoke verifies the built tree against, so
# it has to run before the build, and the build before the smoke.
PACKAGED_STEP_SEQUENCE = (
    "Checkout code",
    "Set up Python",
    "Install runtime and pinned build dependencies",
    "Stage tracked package assets",
    "Build via the canonical spec",
    "Smoke the real bootloader",
)
PACKAGED_FAILURE_STEP = "Upload distribution inventory on failure"

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


def strip_comments(source):
    """`source` with whole-line comments removed.

    Every "this string must not appear" contract below has to read code rather than
    prose, or the comment explaining why a thing is forbidden becomes the reason the
    test reds. ci.yml says "NO --update-snapshots, here or anywhere in CI" in a
    comment; that sentence is the guarantee, not a violation of it. The same applies
    per job block: `frozen-windows` is a two-line `uses:` job whose comment explains
    the smoke it no longer runs.
    """
    return "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("#")
    )


def executable(path):
    return strip_comments(text(path))


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


def triggers(path):
    """The trigger names under `on:`, read from that block rather than the whole file.

    Scanning the raw file for a forbidden trigger name is fail-closed but also forbids
    a workflow from *naming*, in a comment, the trigger it must never have -- which is
    exactly what deep-gate.yml's conversion rationale needs to do.
    """
    source = strip_comments(text(path))
    match = re.search(r"^on:[ \t]*\n(.*?)(?=^\S)", source, re.MULTILINE | re.DOTALL)
    assert match is not None, f"{path.name} has no on: block"
    return set(re.findall(r"^  ([a-z_]+):", match.group(1), re.MULTILINE))


# --------------------------------------------------------------- the vacuity floor


def test_the_workflow_directory_holds_exactly_the_files_this_file_reads():
    """`ALL_WORKFLOWS` is a literal, and every contract below iterates only it.

    A workflow file outside that list is invisible to all of them -- including "the
    frozen build has exactly one definition" and "no undeclared caller exists". Without
    this, a new `.github/workflows/nightly-package.yml` could inline its own PyInstaller
    build, or mint a fourth `<name> / Build and smoke` composite check, with all 39
    tests still green. The prose in `_packaged-windows.yml` and QUALITY_GATE.md claims
    those guarantees over the repository, so the repository is what has to be measured.

    Globbing inside a test body is not the collection-time globbing the R1 council
    forbade (`T-collect`): this file's node set stays fixed regardless of what is on
    disk, so a new workflow reds an assertion rather than silently adding a test.
    """
    on_disk = {
        path.name for path in WORKFLOWS.iterdir() if path.suffix in {".yml", ".yaml"}
    }
    assert on_disk == set(WORKFLOW_PATHS), (
        "a workflow file appeared or vanished; add it to ALL_WORKFLOWS (and to "
        "PACKAGED_CALLERS if it calls the reusable build) or these contracts do not "
        "cover it"
    )


def test_the_parser_still_finds_every_job():
    """Nothing below means anything if this fails. Assert shape before content."""
    release_jobs = jobs(RELEASE)
    assert set(release_jobs) == set(RELEASE_JOB_IDS) | {"release-gate"}
    assert len(release_jobs) == 6

    assert set(jobs(PACKAGED)) == {"build-and-smoke"}

    ci_jobs = jobs(CI)
    assert len(ci_jobs) >= 17

    deep_gate_jobs = jobs(DEEP_GATE)
    assert len(deep_gate_jobs) == 7

    # Every declared caller must at least be a job the parser can see. Without this,
    # "no caller kept its own build steps" would be a statement about missing blocks.
    for file_name, (job_id, _) in PACKAGED_CALLERS.items():
        assert job_id in jobs(WORKFLOW_PATHS[file_name]), f"{file_name}:{job_id}"

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


# --------------------------------------------------------- one build, three callers


def caller_jobs():
    """{(workflow file name, job id)} for every job that calls the reusable build.

    Measured from the files. Both directions of the caller contract compare against
    this, so neither can be satisfied by a literal that agrees only with itself.
    """
    return {
        (path.name, job_id)
        for path in ALL_WORKFLOWS
        for job_id, block in jobs(path).items()
        if REUSABLE_CALL in strip_comments(block)
    }


def test_the_frozen_build_has_exactly_one_definition():
    """Counted by command shape. Counting the filename scores green on zero callers.

    R1 left this at two -- here and deep-gate.yml's inline copy -- because a scheduled
    workflow runs the default branch's HEAD copy of its own file, so editing it ahead
    of the first authoritative scheduled run would have meant that run validated a
    different file than the one that shipped. R2-b closed it: one build, three
    triggers, nothing left to keep in step by hand.
    """
    builds = sum(
        executable(path).count("pyinstaller --clean --noconfirm Hypertrophy-Toolbox.spec")
        for path in ALL_WORKFLOWS
    )
    smokes = sum(
        executable(path).count("python scripts/smoke_packaged_app.py")
        for path in ALL_WORKFLOWS
    )
    assert builds == 1, "the frozen Windows build lives in _packaged-windows.yml only"
    assert smokes == 1
    assert (
        executable(PACKAGED).count(
            "pyinstaller --clean --noconfirm Hypertrophy-Toolbox.spec"
        )
        == 1
    ), "the one definition is not the reusable workflow"


def test_exactly_the_declared_jobs_call_the_reusable_build():
    """The reverse half of the caller contract, and the one that catches drift.

    An undeclared caller is not a harmless addition: it mints a new composite check
    name (`<its name> / Build and smoke`), and if that job ever sits in branch
    protection both halves become frozen. Whoever adds one has to say so here.
    """
    declared = {(name, job_id) for name, (job_id, _) in PACKAGED_CALLERS.items()}
    assert caller_jobs() == declared


@pytest.mark.parametrize("file_name", sorted(PACKAGED_CALLERS))
def test_each_declared_caller_delegates_the_entire_build(file_name):
    """The forward half, per caller.

    A caller that quietly grows its own build steps back -- the exact regression R2-b
    exists to make impossible -- still contains `uses:` and would satisfy a bare
    "does it call the workflow" check. So this asserts what the caller must NOT have
    kept, against the block with comments stripped: `frozen-windows` is a two-line
    delegation whose comment necessarily discusses the build it no longer runs.
    """
    job_id, expected_name = PACKAGED_CALLERS[file_name]
    block = jobs(WORKFLOW_PATHS[file_name])[job_id]
    body = strip_comments(block)

    assert job_name(block) == expected_name, "composite check names are exact-match"
    assert REUSABLE_CALL in body
    for kept in ("steps:", "runs-on:", "pyinstaller", "smoke_packaged_app.py"):
        assert kept not in body, f"{file_name}:{job_id} kept `{kept}` after the lift"
    # No caller varies the build. The reusable workflow declares no `inputs:`, so a
    # `with:` block here could only be a knob someone added -- which is how one
    # definition starts producing three behaviors without becoming three copies.
    assert "with:" not in body, job_id


def test_the_reusable_build_accepts_nothing_from_its_callers():
    """The other half of the no-`with:` assertion above. Asserting only that callers
    pass nothing passes just as well once an input exists and one caller sets it."""
    assert triggers(PACKAGED) == {"workflow_call"}
    assert "inputs:" not in executable(PACKAGED)


def test_the_packaged_smoke_job_name_and_its_child_are_pinned():
    """R1-D4 would promote `<parent> / Build and smoke` into branch protection after
    10 consecutive green runs. Both halves are load-bearing from that point on, and
    the child half is now shared by all three callers."""
    block = jobs(CI)["packaged-smoke-windows"]
    assert job_name(block) == PACKAGED_SMOKE_JOB_NAME
    assert job_name(jobs(PACKAGED)["build-and-smoke"]) == PACKAGED_CHILD_JOB_NAME


# ------------------------------------------- what the single definition must carry


def test_the_single_definition_keeps_the_shape_both_lifted_jobs_had():
    """After R2-b this file is the only place any of these is stated.

    `runs-on` and `timeout-minutes` are asserted here rather than in the callers
    because a `uses:` job may declare neither. deep-gate.yml's `frozen-windows`
    declared both inline until R2-b, at exactly these values.
    """
    block = jobs(PACKAGED)["build-and-smoke"]
    assert re.search(r"^    runs-on: windows-latest$", block, re.MULTILINE)
    assert re.search(r"^    timeout-minutes: 45$", block, re.MULTILINE)

    names = [name for name, _ in steps(block)]
    assert tuple(names[: len(PACKAGED_STEP_SEQUENCE)]) == PACKAGED_STEP_SEQUENCE
    assert PACKAGED_FAILURE_STEP in names

    # Staging is the one pinned step whose body can be gutted silently. The spec stages
    # again during the build, so `run: echo skip` here still produces a green smoke --
    # and quietly deletes the fast-fail-on-broken-manifest property that is the entire
    # reason this step runs first, and the entire reason the order above is pinned.
    bodies = dict(steps(block))
    assert (
        "python scripts/stage_package_assets.py"
        in bodies["Stage tracked package assets"]
    )

    # A `uses:` job may not declare `continue-on-error`, so a step here is the only
    # place the build can be made non-blocking for all three callers at once -- turning
    # a red bootloader smoke green on the PR path, in the release gate and in the weekly
    # gate simultaneously. ci.yml uses the key legitimately in seven places and records
    # this exact trap in its own comments; it has no business in the shared definition.
    assert "continue-on-error" not in executable(PACKAGED)


def test_the_smoke_keeps_the_upgrade_migration_run():
    """`--skip-upgrade` would delete the only automated proof that a user's existing
    database moves to the runtime root intact, while passing every other contract."""
    command = dict(steps(jobs(PACKAGED)["build-and-smoke"]))["Smoke the real bootloader"]
    assert "--mode bootloader" in command
    assert "--skip-upgrade" not in command
    assert "--skip-runtime" not in command
    assert "--mode payload" not in command


def test_the_failure_diagnostic_survived_the_lift():
    """Both lifted jobs dumped the packaged data tree when the smoke failed. Losing it
    costs nothing visible until the day a run goes red and says only "it failed"."""
    raw = dict(steps(jobs(PACKAGED)["build-and-smoke"]))[PACKAGED_FAILURE_STEP]
    assert re.search(r"^      if: failure\(\)$", raw, re.MULTILINE)
    assert "dist/Hypertrophy-Toolbox/_internal/data" in raw
    assert "shell: pwsh" in raw


# --------------------------------------------- the deep gate after the conversion


def test_the_weekly_gate_still_smokes_a_real_bootloader_on_windows():
    """The lift must not have cost the weekly gate its one packaged-artifact check.

    Asserted through the call rather than inside deep-gate.yml, because that is where
    the guarantee now lives: the caller, the callee, and the argv in between.
    """
    assert REUSABLE_CALL in strip_comments(jobs(DEEP_GATE)["frozen-windows"])
    called = jobs(PACKAGED)["build-and-smoke"]
    assert "runs-on: windows-latest" in called
    assert "--mode bootloader" in dict(steps(called))["Smoke the real bootloader"]


def test_the_deep_gate_produces_no_branch_protection_context():
    """Converting `frozen-windows` renamed its check to `<name> / Build and smoke`.
    That rename is safe only because nothing in this workflow is a required context --
    it runs on the weekly schedule and on workflow_dispatch, never on a pull request.
    Add a `pull_request:` trigger here and the safety argument stops holding, so this
    asserts the trigger set positively -- exactly these two, nothing else -- rather than
    trusting the job names alone or scanning the file for a forbidden word.
    """
    names = {job_name(block) for block in jobs(DEEP_GATE).values()}
    assert not names & set(REQUIRED_CONTEXTS)
    assert triggers(DEEP_GATE) == {"schedule", "workflow_dispatch"}


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


@pytest.mark.parametrize(
    "path", (*NEW_WORKFLOWS, DEEP_GATE), ids=lambda p: p.name
)
def test_no_assertion_hides_inside_an_and_list(path):
    """`[ "$a" = "200" ] && [ "$b" = "200" ]` does NOT fail a `set -e` step when the
    FIRST test fails: bash exempts every command in an && list except the last, so
    execution falls through and the step still reports success. Verified in bash.
    Each assertion has to stand alone.

    `[ ... ] && break` inside the readiness loop is fine and stays allowed: it is
    flow control, and the loop's outcome is asserted separately afterwards. What is
    forbidden is one test guarding another.

    `deep-gate.yml` is not one of the two new workflows this file was written for,
    but it is covered here: it carried this exact defect at its `old-db-migration`
    HTTP assertion until R2-a split it, and it is the only workflow in the repository
    with a `schedule:` trigger, so its jobs run unattended with nothing else gating
    them."""
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
