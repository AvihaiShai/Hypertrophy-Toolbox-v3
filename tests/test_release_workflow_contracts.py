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

# The two ways `deep-gate.yml`'s `visual-linux` job is allowed to start, as the exact
# disjuncts of its job-level `if:`. The weekly schedule is what makes the Linux visual
# comparison run at all; the input is the manual opt-in. Neither is optional, and
# nothing else may be added -- a third disjunct is a third way to enter a job whose
# every later step branches on which of these fired.
VISUAL_LINUX_DISJUNCTS = frozenset(
    {"github.event_name == 'schedule'", "inputs.run_visual"}
)

# Every `deep-gate.yml` job, split by whether it may carry a job-level `if:` at all.
#
# GitHub counts a SKIPPED job as a success, and the weekly run is unattended and
# reports one conclusion for the whole workflow -- so `if: ${{ false }}` on any job
# below silently removes that job's evidence from the gate while the run still says
# green. Nothing else in this file notices: the steps are all still present, they
# just never execute. Measured on the unprotected set, one `if:` line added after
# each job's `name:` in turn and then all five at once -- every arm left every
# contract this file held before this packet passing.
#
# `visual-linux` is the one job deliberately allowed one, and what its condition may
# contain is pinned by VISUAL_LINUX_DISJUNCTS above. A job may only join it with its
# condition pinned that way: otherwise moving one across is a two-word edit that
# drops an arm from the parametrized contract below and constrains nothing in its
# place, so the census test measures every member against the file for an `if:` it
# actually carries. `frozen-windows` is barred from carrying one by the
# PACKAGED_CALLERS contracts, which is why it is in neither set here and is read back
# out of that mapping rather than repeated.
DEEP_GATE_UNCONDITIONAL_JOBS = frozenset(
    {
        "full-e2e",
        "first-install",
        "empty-schema",
        "old-db-migration",
        "dependency-health",
    }
)
DEEP_GATE_CONDITIONAL_JOBS = frozenset({"visual-linux"})

# ci.yml job names that exist and are deliberately NOT part of the expected set.
#
# `JS Supply Chain (npm audit, non-required)` left this tuple on 2026-08-22 when
# lever L3 promoted it into branch protection (M4,
# docs/NPM_AUDIT_SEVERITY_POLICY_DECISION.md section 5.2). Deleting it from here
# only stops asserting that it is excluded, which is a green-by-silence move, so
# the promotion is contracted positively below instead.
UNEXPECTED_CI_JOB_NAMES = (
    "E2E Functional Shard ${{ matrix.shard }}/2",
    "JS Unit (Vitest, non-required)",
    "CSS Stylelint Measurement (non-required)",
    PACKAGED_SMOKE_JOB_NAME,
)

# Promoted by M4. The suffix is deliberately unchanged: renaming a protected
# context orphans it (docs/ai_workflow/QUALITY_GATE.md, "the `(non-required)`
# suffix is not a status claim").
NPM_AUDIT_JOB_NAME = "JS Supply Chain (npm audit, non-required)"

JOB_ID = re.compile(r"^  ([A-Za-z0-9_-]+):[ \t]*$", re.MULTILINE)
STEP_SPLIT = re.compile(r"^    - name: ", re.MULTILINE)
NAME_KEY = re.compile(r"^    name: (.+)$", re.MULTILINE)
STEPS_KEY = re.compile(r"^    steps:[ \t]*$", re.MULTILINE)
# The same sequence entries as STEP_SPLIT, but blind to how far they are indented.
# YAML lets a block sequence sit at its key's column or any column deeper, so
# `      - name:` is the same document as `    - name:` -- and STEP_SPLIT matches only
# the second. Counting both is what turns a reindent into a failure instead of an
# empty list. A `- name:` line inside a `run: |` block scalar would be counted here
# too; none exists today, and one appearing should red this rather than quietly
# change what "a step" means to a parser that cannot tell the difference.
ANY_STEP_ENTRY = re.compile(r"^ *- name: ", re.MULTILINE)


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
    """(step name, raw step text) for each step in a job block.

    An empty list is never a valid answer for a job that declares `steps:`, but it was
    the answer this gave for any equivalent reindent of the sequence. Moving every step
    from four spaces to six is the same YAML document and matches STEP_SPLIT nowhere,
    so `for name, raw in steps(block)` became a loop over nothing and every contract
    built on one passed while saying nothing about a workflow the parser could no
    longer read. Measured on deep-gate.yml: all seven jobs parsed to zero steps and the
    file's whole contract set stayed green.

    So the parse is cross-checked against ANY_STEP_ENTRY, which counts the same entries
    without pinning their indent. A job declaring `steps:` must yield at least one, and
    the two counts must agree -- which also catches a partial reindent, where some steps
    still match and the loss is smaller but no louder.
    """
    parts = STEP_SPLIT.split(block)
    parsed = [(part.split("\n", 1)[0].strip(), part) for part in parts[1:]]
    entries = len(ANY_STEP_ENTRY.findall(block))

    if STEPS_KEY.search(block) is None:
        # A `uses:` job legitimately has none; anything else here is a block this
        # parser is misreading.
        assert not entries, (
            f"a job with no `steps:` key holds {entries} `- name:` entries; the job "
            "parser is misreading this block"
        )
        return parsed

    assert parsed, (
        f"a job declaring `steps:` parsed to zero steps while {entries} `- name:` "
        "entries are present -- STEP_SPLIT pins a four-space sequence indent and this "
        "job's is not four. Every contract iterating steps() would now be vacuous."
    )
    assert len(parsed) == entries, (
        f"steps() read {len(parsed)} four-space steps but the block holds {entries} "
        "`- name:` entries; the difference is invisible to every contract below"
    )
    return parsed


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
    build, or mint a fourth `<name> / Build and smoke` composite check, with every
    other contract in this file still green. The prose in `_packaged-windows.yml` and QUALITY_GATE.md claims
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


def test_the_step_parser_reads_every_job_that_declares_steps():
    """The second vacuity floor: shape before content, one level down.

    The floor above proves the parser still finds the JOBS. It says nothing about
    whether it can still read their steps, and #399's own commit message records why
    that gap was invisible: `steps()` discards `parts[0]`, so a job whose sequence sits
    at six spaces instead of four returns an empty list rather than an error.

    `steps()` now refuses to answer that way. This calls it over every job in every
    workflow so the refusal does not depend on some other test happening to iterate
    that file -- nothing else in this file iterates ci.yml's steps at all, so a
    reindent there would otherwise still be unmeasured.
    """
    for path in ALL_WORKFLOWS:
        for job_id, block in jobs(path).items():
            declares_steps = STEPS_KEY.search(block) is not None
            assert bool(steps(block)) == declares_steps, (
                f"{path.name}:{job_id}: `steps:` key present={declares_steps} but the "
                "step parse disagrees"
            )


# ------------------------------------------------- the expected-context list is real


def test_every_expected_context_is_a_real_ci_job_name():
    """Derived, not hand-copied.

    A rename of any of the thirteen in ci.yml reds here instead of burning the
    release gate's 45-minute deadline on a name that will never report.
    """
    names = {job_name(block) for block in jobs(CI).values()}
    missing = sorted(set(EXPECTED_CONTEXTS) - names)
    assert not missing, f"expected contexts with no matching ci.yml job: {missing}"


def test_the_deliberately_excluded_ci_jobs_exist_and_stay_excluded():
    names = {job_name(block) for block in jobs(CI).values()}
    for name in UNEXPECTED_CI_JOB_NAMES:
        assert name in names, name
        assert name not in EXPECTED_CONTEXTS, name


def test_the_npm_audit_job_is_required_and_keeps_its_name_byte_for_byte():
    """M4 / lever L3, asserted positively in both directions.

    The excluded-jobs test above scored green on this name until 2026-08-22 by
    asserting it was *not* required. Simply dropping it there would have left the
    promotion asserted by nothing at all -- a name can go missing from a tuple
    without any test noticing. So: the job still exists in `ci.yml` under exactly
    this string, and that string is a required context. Renaming the job in
    `ci.yml` alone reds the first half; dropping it from `REQUIRED_CONTEXTS`
    alone reds the second.
    """
    names = {job_name(block) for block in jobs(CI).values()}
    assert NPM_AUDIT_JOB_NAME in names, NPM_AUDIT_JOB_NAME
    assert NPM_AUDIT_JOB_NAME in REQUIRED_CONTEXTS, NPM_AUDIT_JOB_NAME
    assert NPM_AUDIT_JOB_NAME not in UNEXPECTED_CI_JOB_NAMES


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
    # `secrets:` is the second way a caller can pass something. The no-`inputs:`
    # contract below does not cover it, and `_packaged-windows.yml` claims in prose
    # that NO caller passes anything -- so the prose was ahead of the tests.
    assert "secrets:" not in body, f"{file_name}:{job_id} passes secrets"
    # A matrix mutates the composite check into `<parent> (x) / <child>`. Both halves
    # are pinned above, but GitHub injects that segment BETWEEN them, so the one
    # rename QUALITY_GATE.md says must never happen silently is the one a matrix
    # performs silently.
    assert "strategy:" not in body, f"{file_name}:{job_id} would rename its own check"
    # `needs:` makes the build conditional on another job succeeding; a skipped
    # dependency skips this job and leaves the run green.
    assert "needs:" not in body, f"{file_name}:{job_id} gated the build behind a job"
    # A `uses:` job whose whole body is one line is one line away from being skipped
    # entirely. `frozen-windows` is guarded by name elsewhere; this covers all three.
    assert not re.search(r"^    if:", body, re.MULTILINE), (
        f"{file_name}:{job_id} must stay unconditional -- a `uses:` job with an `if:` "
        "skips silently and the run still reports green"
    )


def test_the_weekly_schedule_still_fires_weekly():
    """`triggers()` reads trigger NAMES, so `schedule:` staying present says nothing
    about whether the cron can ever fire. Changing `'17 3 * * 1'` to a date that
    effectively never comes -- or deleting the `- cron:` line while keeping the
    `schedule:` key -- silently kills the D3 safety net and reds nothing. Nothing
    else in the repository mentions `cron` at all.

    Pinned to the exact expression because the cadence IS the decision: the weekly
    gate is what the 2026-08-17 first run and the R1-D3 three-run clock are measured
    against.
    """
    assert "schedule" in triggers(DEEP_GATE)
    crons = re.findall(r"^    - cron: '([^']+)'", DEEP_GATE.read_text(encoding="utf-8"), re.MULTILINE)
    assert crons == ["17 3 * * 1"], crons


def test_the_reusable_build_accepts_nothing_from_its_callers():
    """The other half of the no-`with:` assertion above. Asserting only that callers
    pass nothing passes just as well once an input exists and one caller sets it."""
    assert triggers(PACKAGED) == {"workflow_call"}
    assert "inputs:" not in executable(PACKAGED)
    assert "secrets:" not in executable(PACKAGED)


def test_the_shared_build_cannot_be_skipped_or_serialised_for_every_caller_at_once():
    """The widest single false green in this surface.

    `build-and-smoke` is the ONE definition behind three checks. A job-level `if:`
    here skips the frozen Windows build on the PR path, in the release gate and in
    the weekly gate simultaneously, and every other contract in this file stays green
    because the build steps are all still present -- they just never run.

    The step-level guard cannot see this: `steps()` splits on `^    - name: ` and
    discards `parts[0]`, which is the job header, and it matches a SIX-space step
    indent where a job-level key sits at four.

    `concurrency:` is barred for a different reason: the three callers deliberately
    hold three different policies (ci.yml cancels in-progress, release.yml must never
    kill a running release, deep-gate declares none). A group declared here would
    override all three from one place, and R1-D6's no-cancel guarantee is asserted
    against release.yml only.
    """
    body = strip_comments(jobs(PACKAGED)["build-and-smoke"])
    assert not re.search(r"^    if:", body, re.MULTILINE), (
        "`build-and-smoke` must stay unconditional; skipping it silently disarms the "
        "frozen Windows build for all three callers at once"
    )
    assert "concurrency:" not in executable(PACKAGED), (
        "a concurrency group here would apply to all three callers, overriding "
        "release.yml's cancel-in-progress: false guarantee"
    )


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
    # gate simultaneously. ci.yml uses the key legitimately in six places (plus one
    # explicit `continue-on-error: false`, seven occurrences in all) and records
    # this exact trap in its own comments; it has no business in the shared definition.
    # The count was seven-plus-one until the npm-audit enforcement flip removed
    # `js-supply-chain`'s -- see docs/NPM_AUDIT_SEVERITY_POLICY_DECISION.md section
    # 5.2, lever L2.
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
    frozen = strip_comments(jobs(DEEP_GATE)["frozen-windows"])
    assert REUSABLE_CALL in frozen

    # The lift shrank this job to a single `uses:` line, so a one-line `if:` above it
    # would skip the weekly gate's ONLY packaged-artifact check and still report the
    # run green. The step-level guard below is no help: it iterates NEW_WORKFLOWS, and
    # a `uses:` job has no steps to iterate. deep-gate.yml already carries the
    # precedent on `visual-linux`, and MASTER_HANDOVER makes "executed, not skipped"
    # the pass condition of this gate -- so the shape has to be barred by name here.
    assert not re.search(r"^    if:", frozen, re.MULTILINE), (
        "`frozen-windows` must stay unconditional; a `uses:` job with an `if:` "
        "skips silently and leaves the weekly gate green with no bootloader smoke"
    )

    called = jobs(PACKAGED)["build-and-smoke"]
    assert "runs-on: windows-latest" in called
    assert "--mode bootloader" in dict(steps(called))["Smoke the real bootloader"]


def test_the_weekly_visual_comparison_cannot_be_reduced_to_a_manual_opt_in():
    """`visual-linux` is the one job in this repository that may carry a job-level
    `if:`, and the contracts that bar the shape elsewhere therefore had nothing to say
    about what its condition contains.

    Both disjuncts are load-bearing, and the schedule one is the fragile half. A
    `schedule` event carries no `inputs` at all, so `inputs.run_visual` alone resolves
    false: dropping `github.event_name == 'schedule' ||` leaves a workflow whose weekly
    run skips its visual comparison entirely and still reports green -- the exact
    "executed, not skipped" failure the comment above the condition says it exists to
    prevent, and the one this workflow's own prose claims is impossible. Measured: that
    one-line deletion left all 42 contracts in this file passing.

    Pinned as a set of disjuncts rather than as a string so the message names what
    changed, and `&&` is barred by name because it reads as a near-identical edit while
    inverting the meaning -- a scheduled run would then also need an input it can never
    have.
    """
    block = strip_comments(jobs(DEEP_GATE)["visual-linux"])
    found = re.search(r"^    if: \$\{\{ (.+) \}\}$", block, re.MULTILINE)
    assert found is not None, (
        "`visual-linux` lost its job-level `if:`; the weekly/manual split is the "
        "whole reason this job is allowed to carry one"
    )

    condition = found.group(1).strip()
    assert "&&" not in condition, (
        f"`visual-linux` gates its run on a conjunction: {condition!r} -- a scheduled "
        "run carries no inputs, so this never runs weekly"
    )
    disjuncts = {part.strip() for part in condition.split("||")}
    assert disjuncts == VISUAL_LINUX_DISJUNCTS, (
        f"`visual-linux` must run on the weekly schedule AND on an opted-in manual "
        f"dispatch, and on nothing else; found {sorted(disjuncts)}"
    )


def test_every_deep_gate_job_is_classified_as_conditional_or_not():
    """The completeness half, and the reason the per-job contract below is not
    vacuous.

    That contract can only speak about the job ids it is handed. The vacuity floor
    above counts deep-gate's jobs, so a job simply ADDED already reds there -- but a
    count says nothing about WHICH jobs, and a rename, or an add paired with a
    removal, keeps it at seven while moving a job out of the protected set entirely.
    This pins the ids, so the failure names the job that stopped being classified
    instead of reporting a number that no longer matches.
    """
    frozen_id, _ = PACKAGED_CALLERS[DEEP_GATE.name]
    classified = DEEP_GATE_UNCONDITIONAL_JOBS | DEEP_GATE_CONDITIONAL_JOBS | {frozen_id}
    assert set(jobs(DEEP_GATE)) == classified, (
        "deep-gate.yml's jobs no longer match the conditional/unconditional split. An "
        "unclassified job can carry `if: ${{ false }}` and skip out of the unattended "
        "weekly gate while the run still reports green"
    )

    # The conditional set is the escape hatch, so it is measured against the file
    # rather than trusted. Moving an unconditional job into it silently deletes that
    # job's arm from the parametrized contract below and the census above stays green,
    # because the union is unchanged -- but a job that was unconditional has no `if:`
    # to find, which is what this catches.
    unpinned = sorted(
        job_id
        for job_id in DEEP_GATE_CONDITIONAL_JOBS
        if not re.search(
            r"^    if:", strip_comments(jobs(DEEP_GATE)[job_id]), re.MULTILINE
        )
    )
    assert not unpinned, (
        f"{unpinned} are listed as deliberately conditional but carry no job-level "
        "`if:`; a job only belongs here with its condition pinned, or it has left the "
        "unconditional contract with nothing taking its place"
    )
    # The check above is satisfied by moving a job across AND skipping it in the same
    # change, which then shows up only as one fewer parametrize arm. `visual-linux` is
    # the only job whose condition anything pins, so widening the exception has to be
    # a deliberate edit here, against a message saying what it costs.
    assert DEEP_GATE_CONDITIONAL_JOBS == {"visual-linux"}, (
        "`visual-linux` is the only deep-gate job with a pinned condition "
        "(VISUAL_LINUX_DISJUNCTS). Adding another removes it from the unconditional "
        "contract without pinning what its condition may contain -- and it mints a "
        "SECOND job that can skip, which is what "
        "`test_no_unconditional_deep_gate_job_gates_itself_behind_another_job` relies on "
        "not existing: `visual-linux` is exempt from that contract only because a "
        "`needs:` on it can chain to nothing skippable. Widening this set reopens the "
        "`needs:` shape, so widen it there in the same change"
    )


@pytest.mark.parametrize("job_id", sorted(DEEP_GATE_UNCONDITIONAL_JOBS))
def test_no_unconditional_deep_gate_job_can_skip_itself_out_of_the_weekly_run(job_id):
    """The five jobs that must run every week.

    `visual-linux` is allowed a job-level `if:` and `frozen-windows` is barred from
    one by name, so the shape was pinned for exactly two of seven jobs and unmeasured
    for the rest. A skipped job is a successful job to GitHub, and this workflow's
    conclusion is the only thing an unattended weekly run reports -- so one `if:` line
    here deletes the full E2E suite, a cold-start smoke, the empty-schema smoke or the
    old-DB migration proof from the gate without reddening anything, in the workflow
    whose whole purpose is to run the checks the PR pipeline deliberately does not.

    `dependency-health` is the one job here that reports rather than gates -- both its
    scan steps are `continue-on-error: true` -- so skipping it costs the weekly output,
    not a signal. It is held to the same shape anyway: it is the repository's only
    scheduled Python vulnerability scan, and a job that silently stops running is how
    that becomes nobody's job.

    Read against the block with comments stripped, like every other contract here that
    BARS an `if:`, so prose about conditions is not mistaken for one. The value is
    captured only for the message: the key alone is the violation, because
    `    if:\n      ${{ false }}` and a tab after the colon are both the same skip, and
    a pattern demanding `if: ` plus a value passes on either.

    Standing on the second vacuity floor, not asserting it: all five jobs declare
    `steps:` at four spaces, so a 4->6 job reindent would leave every arm here green
    with the parser unable to read the block at all. What reds there is
    `test_the_step_parser_reads_every_job_that_declares_steps`.
    """
    body = strip_comments(jobs(DEEP_GATE)[job_id])
    found = re.search(r"^    if:(.*)$", body, re.MULTILINE)
    condition = found.group(1).strip() if found else None
    assert found is None, (
        f"deep-gate.yml:{job_id} carries a job-level `if: {condition}`. A skipped job "
        "counts as success, so this drops the job's evidence from the weekly gate "
        "while the run still reports green; only `visual-linux` may be conditional here"
    )


# The two shapes Packet R1 measured. #402 recorded both as "deliberately left open,
# and not established as defects"; each is now measured, and each was undetected by
# every contract this file held.
#
# `frozen-windows` is in NEITHER set. Its `needs:` is barred by the PACKAGED_CALLERS
# delegation contract, and a job-level `continue-on-error:` on it was measured
# (arm H2-M4, undetected) but is deliberately OUT of this packet's scope: it is a
# `uses:` job. This repository's recorded position -- stated flatly above the
# `continue-on-error` assertion on `_packaged-windows.yml`, and in
# docs/release_pipeline/PLANNING.md's Plan v1 constraints -- is that a `uses:` job may not
# declare the key at all. What R1 measured is that no CONTRACT here detects it; GitHub's
# enforcement of that constraint was not measured, so whether the shape is a live false
# green or a workflow parse error is what remains open. Recorded, not fixed; closing it
# needs its own authorization.
#
# The two sets differ on purpose, and each covers exactly the jobs whose mutation was
# measured undetected:
#
#   * `needs:` -- the five unconditional jobs. The false-green mechanism is a SKIP
#     chain, and a skipped dependency is the only kind that leaves a run green (a
#     FAILED dependency skips its dependent but reds the run -- measured as arm H1-M2
#     and deliberately NOT claimed as a false green). `visual-linux` is the only job
#     in this workflow that can skip, so it is the only usable dependency; a `needs:`
#     ON `visual-linux` chains to nothing that skips and is therefore not a
#     demonstrated failure mode. R1's own criterion is that protection match the
#     demonstrated mode only, so it is not barred here.
#   * `continue-on-error:` -- those five AND `visual-linux`. This one needs no skip:
#     it swallows a real failure wherever it sits, so `visual-linux`'s scheduled
#     compare is as reachable as the rest.
DEEP_GATE_NO_JOB_LEVEL_CONTINUE_ON_ERROR_JOBS = (
    DEEP_GATE_UNCONDITIONAL_JOBS | DEEP_GATE_CONDITIONAL_JOBS
)

# Job-level keys sit at four spaces; step-level keys at six. The distinction IS the
# contract below: `dependency-health` carries `continue-on-error: true` on both of its
# scan steps by design -- it reports rather than gates -- and a whole-file scan would
# red on that intentional configuration instead of on the unmeasured shape.
JOB_LEVEL_CONTINUE_ON_ERROR = re.compile(r"^    continue-on-error:", re.MULTILINE)
JOB_LEVEL_NEEDS = re.compile(r"^    needs:", re.MULTILINE)


@pytest.mark.parametrize("job_id", sorted(DEEP_GATE_UNCONDITIONAL_JOBS))
def test_no_unconditional_deep_gate_job_gates_itself_behind_another_job(job_id):
    """`needs:` is the second way a job leaves the weekly gate without reddening it.

    A job whose dependency is SKIPPED is skipped too, and a skipped job counts as a
    success -- so `needs: visual-linux` here removes this job's evidence from any run
    where `visual-linux` did not start. That is every `workflow_dispatch` taken with
    the `run_visual` default, which is how this workflow is overwhelmingly exercised.

    Measured on the unprotected set (Packet R1): one `needs: visual-linux` line added
    after each job's `name:` in turn, and all five at once -- every arm left all 51
    contracts in this file passing. The runtime effect is not asserted here and was
    not measured in this repository; it rests on GitHub's documented semantics for a
    skipped job, the same authority the `if:` contract above already stands on.

    The key alone is the violation, for the reason #402 recorded: a pattern demanding
    `needs: ` plus a value passes on `needs:` with its value on the following line and
    on `needs:` followed by a tab, both of which are the same dependency edge. The
    value is captured only for the message.

    Parametrized on `DEEP_GATE_UNCONDITIONAL_JOBS` directly rather than through an
    alias: the set IS the five unconditional jobs, and a second name for it could only
    drift from the census that pins them.

    `frozen-windows` is absent by construction -- it is in neither classification set,
    and its `needs:` is barred by `test_each_declared_caller_delegates_the_entire_build`
    for all three callers at once. Reading the sets rather than a fresh literal is what
    keeps the two contracts from drifting apart.
    """
    body = strip_comments(jobs(DEEP_GATE)[job_id])
    found = JOB_LEVEL_NEEDS.search(body)
    edge = body[found.end() :].split("\n", 1)[0].strip() if found else None
    assert found is None, (
        f"deep-gate.yml:{job_id} gates itself behind `needs: {edge}`. A skipped "
        "dependency skips this job, and a skipped job counts as success -- so this "
        "drops the job's evidence from the run while it still reports green"
    )


@pytest.mark.parametrize(
    "job_id", sorted(DEEP_GATE_NO_JOB_LEVEL_CONTINUE_ON_ERROR_JOBS)
)
def test_no_deep_gate_job_makes_its_own_failure_non_blocking(job_id):
    """The third shape, and the only one of the three that needs no skip at all.

    A job-level `continue-on-error: true` lets the job fail and the RUN still report
    success. That is the field the deep gate is judged by: it is unattended, it
    reports one conclusion, and R1-D3's clock is counted with
    `gh run list --workflow=deep-gate.yml --event=schedule`, which reads the run's
    conclusion and not the job's. `ci.yml` states the mechanism in its own comments
    above the `test-inventory` job -- "continue-on-error swallows a real failure" --
    and uses the key deliberately on `css-stylelint-measure`, a non-required
    measurement job. It has no business on a job that carries evidence.

    Measured (Packet R1): one job-level line added after each job's `name:` in turn,
    all six at once, and in the `${{ true }}`, value-on-the-next-line and tab-separated
    forms -- every arm left all 51 contracts passing. As with `needs:` above, the
    runtime effect is documented rather than measured here.

    **The indent is the whole contract.** `dependency-health` carries
    `continue-on-error: true` on BOTH its scan steps by design, at six spaces; it
    reports rather than gates and that configuration is deliberate. A whole-file
    `"continue-on-error" not in executable(DEEP_GATE)` would red on it instead of on
    the shape this measures -- discovering an intentional configuration, which
    docs/OPEN_WORK_EXECUTION_PLAN.md warned this probe against by name. Deleting one
    of those step-level keys was run as a control arm and must keep passing here:
    it makes the gate stricter, not weaker, and is not this contract's business.

    `frozen-windows` is out of scope; see the comment on the sets above.
    """
    body = strip_comments(jobs(DEEP_GATE)[job_id])
    found = JOB_LEVEL_CONTINUE_ON_ERROR.search(body)
    value = body[found.end() :].split("\n", 1)[0].strip() if found else None
    assert found is None, (
        f"deep-gate.yml:{job_id} declares a job-level `continue-on-error: {value}`. "
        "The job may then fail while the run still reports success, which is the only "
        "signal an unattended weekly gate produces; step-level use inside "
        "`dependency-health` is deliberate and unaffected"
    )


# A job block shaped like the ones `jobs()` returns: two-space job id, four-space job
# keys, and a SIX-space occurrence of each key below them. Both patterns must find
# exactly ONE match here -- the job-level key -- and neither may find the deeper one.
#
# It is a BLOCK rather than a bare key on purpose, and that is half the point of the
# test below. Every bare-key sample puts the key at offset 0, where `^` matches with or
# without `re.MULTILINE`; a real job block never does, because it opens with
# `  <job-id>:`. So a sample built from bare keys stays green when the `re.MULTILINE`
# flag is deleted, while every job arm above silently becomes vacuous -- `search()`
# without the flag can never match a key that is not at offset 0.
#
# The block is SYNTHETIC, and deliberately so: a step never legally carries `needs:`,
# and that line is here anyway. Without a deeper `needs:` to reject, an unanchored
# `^ *needs:` still counts exactly one match and the over-match arm survives -- measured.
# What these patterns must be pinned by is the COLUMN, not by whether a key is plausible
# at that depth, so the sample gives each pattern something at six spaces to ignore.
PATTERN_SAMPLE_BLOCK = """  a-job:
    name: A job
    continue-on-error: true
    needs: [b-job]
    steps:
    - name: a step
      run: true
      needs: not-a-real-step-key
      continue-on-error: true
"""


def test_the_job_level_patterns_cannot_see_a_step_level_key():
    """The boundary both contracts above depend on, proven against literals.

    Asserted on sample text rather than on `deep-gate.yml` so that proving the patterns
    are indentation-scoped does not smuggle in a new constraint on the workflow --
    pinning `dependency-health`'s two step-level keys would bar a future packet from
    promoting that job to blocking, which is a decision nothing here has taken.

    Counted with `findall`, not `search`: `search` proves a match exists and says
    nothing about the step-level key sitting four lines below it, so an over-matching
    pattern would pass a positive and a negative arm that are each looking elsewhere.

    `JOB_LEVEL_NEEDS` needs this more than its sibling does. No deep-gate job carries
    `needs:` today, so its five arms above are all negatives: without a positive here,
    a five-space anchor or a typo'd key would leave every one of them passing while
    matching nothing at all. The `if:` contract this pair imitates does not have that
    hole -- `test_every_deep_gate_job_is_classified_as_conditional_or_not` requires the
    same `^    if:` literal to MATCH on `visual-linux` -- and a contract that is
    strictly weaker than the sibling it imitates is the second failure mode #402 paid
    for.
    """
    assert len(JOB_LEVEL_CONTINUE_ON_ERROR.findall(PATTERN_SAMPLE_BLOCK)) == 1
    assert len(JOB_LEVEL_NEEDS.findall(PATTERN_SAMPLE_BLOCK)) == 1

    # The forms a `key: value` pattern would miss -- all of them the same key, and each
    # written inside a block so `^` is never satisfied by offset 0.
    header = "  a-job:\n    name: A job\n"
    for pattern, tails in (
        (
            JOB_LEVEL_CONTINUE_ON_ERROR,
            (
                "    continue-on-error: true\n",
                "    continue-on-error:\n      true\n",
                "    continue-on-error:\ttrue\n",
                "    continue-on-error: ${{ true }}\n",
            ),
        ),
        (
            JOB_LEVEL_NEEDS,
            (
                "    needs: visual-linux\n",
                "    needs: [visual-linux, first-install]\n",
                "    needs:\n      - visual-linux\n",
                "    needs:\tvisual-linux\n",
            ),
        ),
    ):
        for tail in tails:
            assert pattern.search(header + tail), tail


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
