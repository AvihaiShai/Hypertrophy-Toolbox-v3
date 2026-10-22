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
    BASE_PR_REQUIRED_CONTEXTS,
    BASE_RELEASE_EXPECTED_CONTEXTS,
    JS_UNIT_CONTEXT,
    PR_REQUIRED_CONTEXTS,
    RELEASE_EXPECTED_CONTEXTS,
    RELEASE_JOB_IDS,
    RELEASE_TAG_PATTERN,
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
SHA = "0123456789abcdef0123456789abcdef01234567"
OTHER_SHA = "89abcdef0123456789abcdef0123456789abcdef"
BASE_PR_NAMES = (
    "Code Linting",
    "E2E Backup (Chromium, isolated)",
    "E2E Erase Flow (Chromium, isolated, non-required)",
    "E2E Fatigue Context (Chromium, non-required)",
    "E2E Functional (Chromium)",
    "E2E Smoke (Chromium)",
    "Frontend Build (npm ci + SCSS)",
    "JS Supply Chain (npm audit, non-required)",
    "Run Tests",
    "Security Audit",
    "Test Inventory Drift",
    "Type Check (tsc blocking + pyright measure-only)",
)


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
    app_id=15368,
    head_sha=SHA,
):
    """One synthetic check-run. Keyword defaults keep each arm a one-field edit."""
    return {
        "name": name,
        "id": run_id,
        "started_at": started_at,
        "status": status,
        "conclusion": conclusion,
        "head_sha": head_sha,
        "app": {"slug": slug, "id": app_id},
        "html_url": f"https://example.invalid/{run_id}",
    }


def all_green(expected=RELEASE_EXPECTED_CONTEXTS):
    return [
        run(name, 1000 + index, "2026-08-14T10:00:00Z")
        for index, name in enumerate(expected)
    ]


def provenance(pages, *, deadline=0.0, expected=RELEASE_EXPECTED_CONTEXTS):
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
        sha=SHA,
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


@pytest.mark.parametrize(
    "actual,expected,count",
    [
        (BASE_PR_REQUIRED_CONTEXTS, BASE_PR_NAMES, 12),
        (BASE_RELEASE_EXPECTED_CONTEXTS, (*BASE_PR_NAMES, "Visual Regression (Windows baselines)"), 13),
        (PR_REQUIRED_CONTEXTS, (*BASE_PR_NAMES, "JS Unit (Vitest)"), 13),
        (RELEASE_EXPECTED_CONTEXTS, (*BASE_PR_NAMES, "Visual Regression (Windows baselines)", "JS Unit (Vitest)"), 14),
    ],
    ids=["baseline-pr", "baseline-release", "js-pr", "js-release"],
)
def test_context_sets_preserve_exact_membership_and_uniqueness(actual, expected, count):
    assert isinstance(actual, tuple)
    assert len(actual) == len(set(actual)) == count
    assert set(actual) == set(expected)


def test_only_js_is_added_to_both_active_sets():
    assert JS_UNIT_CONTEXT == "JS Unit (Vitest)"
    assert VISUAL_CONTEXT == "Visual Regression (Windows baselines)"
    assert set(PR_REQUIRED_CONTEXTS) - set(BASE_PR_REQUIRED_CONTEXTS) == {JS_UNIT_CONTEXT}
    assert set(RELEASE_EXPECTED_CONTEXTS) - set(BASE_RELEASE_EXPECTED_CONTEXTS) == {JS_UNIT_CONTEXT}
    assert RELEASE_EXPECTED_CONTEXTS.count(VISUAL_CONTEXT) == 1
    assert VISUAL_CONTEXT not in PR_REQUIRED_CONTEXTS
    for contexts in (BASE_PR_REQUIRED_CONTEXTS, BASE_RELEASE_EXPECTED_CONTEXTS,
                     PR_REQUIRED_CONTEXTS, RELEASE_EXPECTED_CONTEXTS):
        assert "Dependency Review" not in contexts


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
        [run("Some Other Job", 1, "2026-08-14T10:00:00Z")], RELEASE_EXPECTED_CONTEXTS, sha=SHA
    )
    assert selected == {}
    assert seen == {}


# ------------------------------------------------------------- pending and verdict


@pytest.mark.parametrize("expected", [BASE_RELEASE_EXPECTED_CONTEXTS, RELEASE_EXPECTED_CONTEXTS],
                         ids=["baseline", "js-stage"])
@pytest.mark.parametrize("missing", [False, True], ids=["success", "missing"])
def test_both_release_stages_require_every_context(expected, missing):
    runs = all_green(expected)
    if missing:
        runs = [r for r in runs if r["name"] != VISUAL_CONTEXT]
    code, output, _ = provenance([runs], expected=expected)
    assert code == int(missing)
    if missing:
        assert f"MISSING   {VISUAL_CONTEXT}" in output


@pytest.mark.parametrize("binding", [
    {"head_sha": None}, {"head_sha": OTHER_SHA},
    {"app_id": None}, {"app_id": 1}, {"app_id": "15368"},
    {"app_id": 15368.0}, {"app_id": True},
    {"slug": None}, {"slug": "some-other-app"},
])
def test_wrong_provenance_binding_cannot_supply_a_required_success(binding):
    runs = [r for r in all_green() if r["name"] != JS_UNIT_CONTEXT]
    runs.append(run(JS_UNIT_CONTEXT, 4100, "2026-08-14T12:00:00Z", **binding))
    code, output, _ = provenance([runs])
    assert code == 1
    assert f"MISSING   {JS_UNIT_CONTEXT}" in output


@pytest.mark.parametrize("missing", ["head_sha", "app", "app.id", "app.slug"])
def test_missing_provenance_binding_cannot_supply_a_required_success(missing):
    unbound = run(JS_UNIT_CONTEXT, 4100, "2026-08-14T12:00:00Z")
    if missing.startswith("app."):
        del unbound["app"][missing.split(".")[1]]
    else:
        del unbound[missing]
    runs = [r for r in all_green() if r["name"] != JS_UNIT_CONTEXT] + [unbound]
    code, output, _ = provenance([runs])
    assert code == 1
    assert f"MISSING   {JS_UNIT_CONTEXT}" in output


@pytest.mark.parametrize("binding", [
    {"head_sha": OTHER_SHA}, {"app_id": 1}, {"slug": "some-other-app"},
])
@pytest.mark.parametrize("trusted_conclusion,expected_code", [("success", 0), ("failure", 1)])
def test_untrusted_newer_result_neither_masks_failure_nor_poisons_success(
    binding, trusted_conclusion, expected_code
):
    other = "failure" if trusted_conclusion == "success" else "success"
    runs = [r for r in all_green() if r["name"] != JS_UNIT_CONTEXT] + [
        run(JS_UNIT_CONTEXT, 4200, "2026-08-14T10:00:00Z", trusted_conclusion),
        run(JS_UNIT_CONTEXT, 4201, None, other, **binding),
    ]
    code, output, _ = provenance([runs])
    assert code == expected_code
    assert "id=4200" in output
    assert "id=4201" not in output


@pytest.mark.parametrize("conclusion", [
    "failure", "cancelled", "skipped", "neutral", "timed_out", "action_required",
])
def test_js_unit_requires_a_successful_conclusion(conclusion):
    runs = [r for r in all_green() if r["name"] != JS_UNIT_CONTEXT]
    runs.append(run(JS_UNIT_CONTEXT, 4300, "2026-08-14T10:00:00Z", conclusion))
    code, output, _ = provenance([runs])
    assert code == 1
    assert "did not conclude success" in output
    assert JS_UNIT_CONTEXT in output


@pytest.mark.parametrize("state", ["missing", "old-name", "queued", "in_progress"])
def test_js_unit_missing_renamed_or_pending_expires_at_the_deadline(state):
    runs = [r for r in all_green() if r["name"] != JS_UNIT_CONTEXT]
    if state == "old-name":
        runs.append(run("JS Unit (Vitest, non-required)", 4400, "2026-08-14T10:00:00Z"))
    elif state != "missing":
        runs.append(run(JS_UNIT_CONTEXT, 4400, "2026-08-14T10:00:00Z", None, status=state))
    code, output, fetches = provenance([runs], deadline=2)
    assert code == 1
    assert "timed out after 2s" in output
    assert JS_UNIT_CONTEXT in output
    assert fetches == 3


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
    selected, _ = select_runs(runs, RELEASE_EXPECTED_CONTEXTS, sha=SHA)
    pending, failed = classify(selected, RELEASE_EXPECTED_CONTEXTS)
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
    for name in RELEASE_EXPECTED_CONTEXTS:
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


@pytest.mark.parametrize("newer_conclusion,expected_code", [("failure", 1), ("success", 0), (None, 1)])
@pytest.mark.parametrize("reverse", [False, True], ids=["forward", "reversed"])
def test_page_two_newest_js_result_decides_real_provenance(monkeypatch, newer_conclusion, expected_code, reverse):
    older = "failure" if newer_conclusion == "success" else "success"
    first = all_green() + [run(JS_UNIT_CONTEXT, 9999, "2026-08-14T11:00:00Z", older)]
    first += [run(f"Filler {i}", 11000 + i, "2026-08-14T10:00:00Z")
              for i in range(100 - len(first))]
    second = [run(JS_UNIT_CONTEXT, 12000, "2026-08-14T12:00:00Z", newer_conclusion,
                  status="in_progress" if newer_conclusion is None else "completed")]
    urls = []

    def fake_get(url, _token):
        urls.append(url)
        page = len(urls)
        assert url == (f"https://api.github.com/repos/o/r/commits/{SHA}/check-runs"
                       f"?filter=all&per_page=100&page={page}")
        values = first if page == 1 else second
        return {"check_runs": list(reversed(values)) if reverse else values}

    monkeypatch.setattr("scripts.release_gate._api_get", fake_get)
    code, output, _ = provenance([fetch_check_runs("o/r", SHA, None)])
    assert code == expected_code
    assert len(urls) == 2
    assert "id=12000" in output


@pytest.mark.parametrize("include_js", [True, False], ids=["js-success", "missing-js"])
def test_provenance_cli_uses_the_promoted_release_set(monkeypatch, include_js):
    from scripts import release_gate

    payload = all_green() if include_js else all_green(BASE_RELEASE_EXPECTED_CONTEXTS)
    monkeypatch.setattr(release_gate, "_api_get", lambda _url, _token: {"check_runs": payload})
    monkeypatch.setattr(release_gate, "DEFAULT_DEADLINE_SECONDS", 0)
    assert release_gate.main(["provenance", "--repo", "o/r", "--sha", SHA]) == int(not include_js)


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
    collected = fetch_check_runs("o/r", SHA, None)
    assert len(collected) == 101
    selected, _ = select_runs(collected, ["Run Tests"], sha=SHA)
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
    collected = fetch_check_runs("o/r", SHA, None)
    assert len(collected) == 101
    selected, _ = select_runs(collected, ["Run Tests"], sha=SHA)
    assert selected["Run Tests"]["conclusion"] == "failure"


def test_a_run_with_no_timestamp_is_selected_rather_than_outranked():
    """An empty-string default would sort it below every real run, so a newer
    untimestamped run would lose to an older success and read as passed."""
    runs = [r for r in all_green() if r["name"] != "Run Tests"] + [
        run("Run Tests", 9001, "2026-08-14T10:00:00Z", "success"),
        run("Run Tests", 9002, None, None, status="in_progress"),
    ]
    selected, _ = select_runs(runs, RELEASE_EXPECTED_CONTEXTS, sha=SHA)
    assert selected["Run Tests"]["id"] == 9002
    pending, _ = classify(selected, RELEASE_EXPECTED_CONTEXTS)
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
