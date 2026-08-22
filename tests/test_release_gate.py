"""Unit tests for the release gate's three preflight assertions.

Every one of these guards a place where a mistake produces a *green* release rather
than a red one, so the arms come in pairs: each fixture that must fail has a sibling
that must pass, differing in exactly one field. A rule that only ever fails is
indistinguishable from an unconditional failure.
"""
import io
import json

import pytest

from scripts.release_gate import (
    EXPECTED_CONTEXTS,
    RELEASE_JOB_IDS,
    RELEASE_TAG_PATTERN,
    REQUIRED_CONTEXTS,
    VISUAL_CONTEXT,
    check_fan_in,
    check_provenance,
    check_version,
    classify,
    fetch_check_runs,
    parse_dry_run,
    select_runs,
    tag_exists_on_remote,
)

APP = "3.0.1"


def run(
    name: str,
    run_id: int,
    # None is a shape the selection rule has to survive: `started_at` is its primary
    # sort key, so a run without one must not be silently outranked.
    started_at: str | None,
    # None is the real shape of an in-flight run: GitHub reports `conclusion: null`
    # until `status` reaches "completed".
    conclusion: str | None = "success",
    *,
    status: str = "completed",
    slug: str = "github-actions",
):
    """One synthetic check-run. Keyword defaults keep each arm a one-field edit."""
    return {
        "name": name,
        "id": run_id,
        "started_at": started_at,
        "status": status,
        "conclusion": conclusion,
        "app": {"slug": slug},
        "html_url": f"https://example.invalid/{run_id}",
    }


def all_green():
    return [
        run(name, 1000 + index, "2026-08-14T10:00:00Z")
        for index, name in enumerate(EXPECTED_CONTEXTS)
    ]


def provenance(pages, *, deadline=0.0, expected=EXPECTED_CONTEXTS):
    """Drive the real poll loop with a scripted sequence of per-poll responses."""
    calls = {"n": 0}
    clock = {"t": 0.0}

    def fetch(_repo, _sha):
        index = min(calls["n"], len(pages) - 1)
        calls["n"] += 1
        return pages[index]

    def monotonic():
        return clock["t"]

    def sleep(seconds):
        clock["t"] += max(seconds, 1.0)

    stream = io.StringIO()
    code = check_provenance(
        repo="o/r",
        sha="deadbeef",
        expected=expected,
        fetch=fetch,
        deadline_seconds=deadline,
        poll_seconds=1.0,
        monotonic=monotonic,
        sleep=sleep,
        stream=stream,
    )
    return code, stream.getvalue(), calls["n"]


def version(
    ref,
    *,
    dry_run="",
    app=APP,
    package=APP,
    tag_exists=lambda _tag: False,
    is_on_main=lambda: True,
):
    stream = io.StringIO()
    code = check_version(
        ref=ref,
        dry_run=parse_dry_run(dry_run),
        app_version=app,
        package_version=package,
        tag_exists=tag_exists,
        is_on_main=is_on_main,
        stream=stream,
    )
    return code, stream.getvalue()


# ------------------------------------------------------------------ the constants


def test_expected_contexts_is_the_twelve_required_plus_the_visual_one():
    assert len(REQUIRED_CONTEXTS) == 12
    assert "JS Supply Chain (npm audit, non-required)" in REQUIRED_CONTEXTS
    assert VISUAL_CONTEXT not in REQUIRED_CONTEXTS
    assert set(EXPECTED_CONTEXTS) == set(REQUIRED_CONTEXTS) | {VISUAL_CONTEXT}
    assert len(EXPECTED_CONTEXTS) == 13


def test_the_release_tag_pattern_is_anchored():
    """Unanchored, it would accept v3.0.1-rc0 while every other test still passed."""
    assert RELEASE_TAG_PATTERN.match("v3.0.1")
    assert RELEASE_TAG_PATTERN.match("v10.20.30")
    for rejected in ("v3.0.1-rc0", "v3.0.1rc", "xv3.0.1", "v3.0.1.4", "v3.0", "vNEXT"):
        assert not RELEASE_TAG_PATTERN.match(rejected), rejected


# -------------------------------------------------------------------- version cmd


def test_an_exact_tag_on_matching_sources_passes():
    code, _ = version("refs/tags/v3.0.1")
    assert code == 0


def test_a_mismatched_tag_fails_and_names_all_three_sources():
    code, output = version("refs/tags/v3.0.2")
    assert code == 1
    # Section 0 criterion 2 requires attributability: the exit code alone lets a
    # message regression through.
    assert "v3.0.2" in output
    assert "APP_VERSION" in output and APP in output
    assert "package.json" in output


def test_a_prerelease_tag_fails_and_points_at_the_rehearsal_route():
    code, output = version("refs/tags/v3.0.1-rc0")
    assert code == 1
    assert "workflow_dispatch" in output
    assert "dry_run" in output


def test_source_parity_is_checked_against_two_literals():
    code, output = version("refs/tags/v3.0.1", app="3.0.1", package="3.0.2")
    assert code == 1
    assert "disagree" in output


@pytest.mark.parametrize("raw", ["", "   ", "false", "False", "no", None])
def test_a_push_event_resolves_to_release_mode(raw):
    """`${{ inputs.dry_run }}` renders empty on a tag push; empty must not rehearse."""
    assert parse_dry_run(raw) is False


@pytest.mark.parametrize("raw", ["true", "True", " TRUE "])
def test_only_an_explicit_true_rehearses(raw):
    assert parse_dry_run(raw) is True


def test_dry_run_is_not_a_bypass_on_a_tag_ref():
    code, output = version("refs/tags/v3.0.2", dry_run="true")
    assert code == 1
    assert "does not match the code" in output


def test_a_branch_ref_without_dry_run_is_rejected():
    code, output = version("refs/heads/main", dry_run="")
    assert code == 1
    assert "not a tag" in output


def test_a_branch_rehearsal_passes_when_the_tag_is_unpublished():
    code, _ = version("refs/heads/main", dry_run="true")
    assert code == 0


def test_a_branch_rehearsal_fails_when_the_tag_already_exists():
    code, output = version(
        "refs/heads/main", dry_run="true", tag_exists=lambda tag: tag == "v3.0.1"
    )
    assert code == 1
    assert "already exists" in output


def test_a_tag_off_main_is_rejected():
    """R1-D1 says "on main"; nothing else in the pipeline establishes it. A green
    feature-branch head satisfies provenance just as well as a main commit."""
    code, output = version("refs/tags/v3.0.1", is_on_main=lambda: False)
    assert code == 1
    assert "on main" in output


def test_a_rehearsal_is_not_required_to_be_on_main():
    """A dispatch against a feature branch is a legitimate way to exercise this
    workflow, and it is not a release."""
    code, _ = version("refs/heads/wip", dry_run="true", is_on_main=lambda: False)
    assert code == 0


@pytest.mark.parametrize("bad", ["3.0", "3.0.1rc1", "3.0.1.4", "v3.0.1"])
def test_an_unreleasable_app_version_fails_on_the_rehearsal_path(bad):
    """Under option (c) the rehearsal is the only path that runs before a real
    release, so it has to catch a version that can never produce a valid tag."""
    code, output = version("refs/heads/main", dry_run="true", app=bad, package=bad)
    assert code == 1
    assert "cannot produce a publishable tag" in output


# ------------------------------------------------------- tag existence, over http


def _matching_refs(monkeypatch, payload):
    monkeypatch.setattr("scripts.release_gate._api_get", lambda _url, _token: payload)


def test_tag_existence_is_an_exact_ref_match_not_a_prefix_match(monkeypatch):
    """matching-refs is a PREFIX endpoint: v3.0.10 comes back for a v3.0.1 query.

    Treating a non-empty response as "the tag exists" would block every rehearsal
    once any longer-numbered tag existed.
    """
    _matching_refs(monkeypatch, [{"ref": "refs/tags/v3.0.10"}])
    assert tag_exists_on_remote("o/r", "v3.0.1", None) is False


def test_tag_existence_is_true_for_the_exact_ref(monkeypatch):
    _matching_refs(
        monkeypatch, [{"ref": "refs/tags/v3.0.1"}, {"ref": "refs/tags/v3.0.10"}]
    )
    assert tag_exists_on_remote("o/r", "v3.0.1", None) is True


def test_no_matching_refs_means_the_tag_is_free(monkeypatch):
    _matching_refs(monkeypatch, [])
    assert tag_exists_on_remote("o/r", "v3.0.1", None) is False


# ---------------------------------------------------------------- run selection


def test_a_newer_failure_beats_a_stale_success():
    runs = all_green() + [
        run("Run Tests", 1001, "2026-08-14T10:00:00Z", "success"),
        run("Run Tests", 1002, "2026-08-14T11:00:00Z", "failure"),
    ]
    code, output, _ = provenance([runs])
    assert code == 1
    assert "id=1002" in output
    assert "3 runs" in output


def test_a_newer_success_beats_a_stale_failure():
    """The mirror arm. Without it, the rule is indistinguishable from 'any failure reds'."""
    runs = all_green() + [
        run("Run Tests", 1001, "2026-08-14T10:00:00Z", "failure"),
        run("Run Tests", 1002, "2026-08-14T11:00:00Z", "success"),
    ]
    code, _, _ = provenance([runs])
    assert code == 0


@pytest.mark.parametrize(
    "newer_conclusion,expected_code", [("failure", 1), ("success", 0)]
)
def test_timestamp_wins_when_it_disagrees_with_id(newer_conclusion, expected_code):
    """Kills a `max(id)` implementation, which A/B alone cannot distinguish."""
    other = "success" if newer_conclusion == "failure" else "failure"
    runs = all_green() + [
        run("Run Tests", 2000, "2026-08-14T11:00:00Z", other),
        run("Run Tests", 1999, "2026-08-14T12:00:00Z", newer_conclusion),
    ]
    code, _, _ = provenance([runs])
    assert code == expected_code


@pytest.mark.parametrize(
    "higher_id_conclusion,expected_code", [("failure", 1), ("success", 0)]
)
def test_id_breaks_a_timestamp_tie(higher_id_conclusion, expected_code):
    other = "success" if higher_id_conclusion == "failure" else "failure"
    runs = all_green() + [
        run("Run Tests", 3001, "2026-08-14T10:00:00Z", other),
        run("Run Tests", 3002, "2026-08-14T10:00:00Z", higher_id_conclusion),
    ]
    code, _, _ = provenance([runs])
    assert code == expected_code


def test_array_order_does_not_decide():
    """Kills 'take the last element' and 'take the first element'."""
    runs = [
        run("Run Tests", 1002, "2026-08-14T11:00:00Z", "failure"),
        run("Run Tests", 1001, "2026-08-14T10:00:00Z", "success"),
    ] + all_green()
    code, _, _ = provenance([runs])
    assert code == 1


def test_a_third_party_success_cannot_win():
    runs = all_green() + [
        run("Run Tests", 4001, "2026-08-14T11:00:00Z", "failure"),
        run("Run Tests", 4002, "2026-08-14T12:00:00Z", "success", slug="some-other-app"),
    ]
    code, _, _ = provenance([runs])
    assert code == 1


def test_a_third_party_failure_is_discarded_rather_than_fatal():
    """The mirror arm: the filter must EXCLUDE foreign runs, not red on them."""
    runs = all_green() + [
        run("Run Tests", 4001, "2026-08-14T11:00:00Z", "success"),
        run("Run Tests", 4002, "2026-08-14T12:00:00Z", "failure", slug="some-other-app"),
    ]
    code, _, _ = provenance([runs])
    assert code == 0


def test_select_runs_ignores_names_nobody_expects():
    selected, seen = select_runs(
        [run("Some Other Job", 1, "2026-08-14T10:00:00Z")], EXPECTED_CONTEXTS
    )
    assert selected == {}
    assert seen == {}


# ------------------------------------------------------------- pending and verdict


@pytest.mark.parametrize(
    "conclusion", ["failure", "cancelled", "skipped", "neutral", "timed_out"]
)
def test_success_is_the_only_passing_conclusion(conclusion):
    """`!= "failure"` would let four of these five through."""
    runs = [r for r in all_green() if r["name"] != "Run Tests"]
    runs.append(run("Run Tests", 5000, "2026-08-14T10:00:00Z", conclusion))
    code, _, _ = provenance([runs])
    assert code == 1


def test_a_newer_in_progress_run_keeps_the_name_pending():
    """The live-observed shape: an older success beside a newer in-flight re-run."""
    runs = all_green() + [
        run("Run Tests", 5001, "2026-08-14T10:00:00Z", "success"),
        run("Run Tests", 5002, "2026-08-14T11:00:00Z", None, status="in_progress"),
    ]
    selected, _ = select_runs(runs, EXPECTED_CONTEXTS)
    pending, failed = classify(selected, EXPECTED_CONTEXTS)
    assert pending == ["Run Tests"]
    assert failed == []


def test_a_missing_name_is_pending_then_fails_at_the_deadline():
    """`E2E Functional (Chromium)` has no check-run until its shards finish."""
    runs = [r for r in all_green() if r["name"] != "E2E Functional (Chromium)"]
    code, output, _ = provenance([runs])
    assert code == 1
    assert "MISSING   E2E Functional (Chromium)" in output
    assert "timed out" in output


def test_an_empty_response_fails_naming_every_expected_context():
    code, output, _ = provenance([[]])
    assert code == 1
    for name in EXPECTED_CONTEXTS:
        assert f"MISSING   {name}" in output


def test_the_loop_polls_until_the_pending_run_completes():
    pending_page = [r for r in all_green() if r["name"] != "Run Tests"] + [
        run("Run Tests", 6001, "2026-08-14T10:00:00Z", None, status="queued")
    ]
    code, _, fetches = provenance([pending_page, all_green()], deadline=120.0)
    assert code == 0
    assert fetches == 2


def test_a_failure_stops_the_loop_immediately():
    failing = [r for r in all_green() if r["name"] != "Run Tests"] + [
        run("Run Tests", 6002, "2026-08-14T10:00:00Z", "failure")
    ]
    code, _, fetches = provenance([failing, all_green()], deadline=600.0)
    assert code == 1
    assert fetches == 1


# ------------------------------------------------------------------- pagination


def test_pagination_reads_every_page(monkeypatch):
    """The decisive run sits on page 2, so a single-page read scores green."""
    page_one = [
        run(f"Filler {index}", 7000 + index, "2026-08-14T10:00:00Z")
        for index in range(100)
    ]
    page_two = [run("Run Tests", 8000, "2026-08-14T12:00:00Z", "failure")]

    def fake_get(url, _token):
        assert "filter=all" in url
        assert "per_page=100" in url
        # Match on the delimiter: `per_page=100` contains `page=1` as a substring.
        page = int(url.rsplit("&page=", 1)[1])
        return {"total_count": 101, "check_runs": page_one if page == 1 else page_two}

    monkeypatch.setattr("scripts.release_gate._api_get", fake_get)
    collected = fetch_check_runs("o/r", "sha", None)
    assert len(collected) == 101
    selected, _ = select_runs(collected, ["Run Tests"])
    assert selected["Run Tests"]["conclusion"] == "failure"


def test_pagination_stops_on_an_empty_page(monkeypatch):
    """A total_count larger than what the API actually returns must not spin forever."""
    monkeypatch.setattr(
        "scripts.release_gate._api_get",
        lambda _url, _token: {"total_count": 500, "check_runs": []},
    )
    assert fetch_check_runs("o/r", "sha", None) == []


def test_pagination_does_not_trust_a_missing_total_count(monkeypatch):
    """Paging on `total_count` fails OPEN when the key is absent: the total defaults
    to zero, page 2 is never read, and the newer failure living there is invisible."""
    page_one = [
        run(f"Filler {index}", 9000 + index, "2026-08-14T10:00:00Z")
        for index in range(100)
    ]
    page_two = [run("Run Tests", 9500, "2026-08-14T12:00:00Z", "failure")]

    def fake_get(url, _token):
        page = int(url.rsplit("&page=", 1)[1])
        return {"check_runs": page_one if page == 1 else page_two}

    monkeypatch.setattr("scripts.release_gate._api_get", fake_get)
    collected = fetch_check_runs("o/r", "sha", None)
    assert len(collected) == 101
    selected, _ = select_runs(collected, ["Run Tests"])
    assert selected["Run Tests"]["conclusion"] == "failure"


def test_a_run_with_no_timestamp_is_selected_rather_than_outranked():
    """An empty-string default would sort it below every real run, so a newer
    untimestamped run would lose to an older success and read as passed."""
    runs = [r for r in all_green() if r["name"] != "Run Tests"] + [
        run("Run Tests", 9001, "2026-08-14T10:00:00Z", "success"),
        run("Run Tests", 9002, None, None, status="in_progress"),
    ]
    selected, _ = select_runs(runs, EXPECTED_CONTEXTS)
    assert selected["Run Tests"]["id"] == 9002
    pending, _ = classify(selected, EXPECTED_CONTEXTS)
    assert pending == ["Run Tests"]


def test_an_empty_expected_list_cannot_pass():
    code, output, _ = provenance([all_green()], expected=())
    assert code == 1
    assert "empty" in output


# ----------------------------------------------------------------------- fan-in


def test_fan_in_passes_when_every_expected_job_succeeded():
    payload = json.dumps({job: {"result": "success"} for job in RELEASE_JOB_IDS})
    stream = io.StringIO()
    assert check_fan_in(needs_json=payload, expected_ids=RELEASE_JOB_IDS, stream=stream) == 0


@pytest.mark.parametrize("result", ["failure", "skipped", "cancelled", "unknown"])
def test_fan_in_fails_on_any_non_success_result(result):
    """`skipped` is the one that matters: a skipped job is not a passed job."""
    payload = json.dumps(
        {
            job: {"result": result if job == "packaged-windows" else "success"}
            for job in RELEASE_JOB_IDS
        }
    )
    stream = io.StringIO()
    code = check_fan_in(needs_json=payload, expected_ids=RELEASE_JOB_IDS, stream=stream)
    assert code == 1
    assert "packaged-windows" in stream.getvalue()


def test_fan_in_fails_when_a_job_was_removed_from_needs():
    payload = json.dumps(
        {job: {"result": "success"} for job in RELEASE_JOB_IDS if job != "first-install"}
    )
    stream = io.StringIO()
    code = check_fan_in(needs_json=payload, expected_ids=RELEASE_JOB_IDS, stream=stream)
    assert code == 1
    assert "first-install" in stream.getvalue()


def test_fan_in_fails_when_an_unexpected_job_reports():
    """The mirror arm: the set comparison is two-sided, not a subset check."""
    payload = json.dumps(
        {job: {"result": "success"} for job in (*RELEASE_JOB_IDS, "surprise-job")}
    )
    stream = io.StringIO()
    code = check_fan_in(needs_json=payload, expected_ids=RELEASE_JOB_IDS, stream=stream)
    assert code == 1
    assert "surprise-job" in stream.getvalue()
