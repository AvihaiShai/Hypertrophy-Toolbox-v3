"""The release gate's preflight assertions, as testable code rather than inline shell.

`release.yml` calls three subcommands:

``version``     the R1-D1 invariant -- an exact ``v<APP_VERSION>`` tag, with
                ``utils/version.py`` and ``package.json`` agreeing.
``provenance``  R1-D2 -- every expected CI check-run on the commit being shipped
                concluded ``success``, selecting the newest run per name so a stale
                success cannot mask a newer failure.
``fan-in``      the anti-false-green gate -- the set of jobs that reported must be
                exactly the expected set, and every one of them must have succeeded.

All three live here rather than in the workflow because a `run:` block cannot be unit
tested, and each of these is a place where a mistake produces a *green* release.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Callable, Iterable, Sequence, TextIO

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

GITHUB_API = "https://api.github.com"

# The 11 branch-protection contexts, read live from
# `gh api repos/{owner}/{repo}/branches/main/protection/required_status_checks`
# on 2026-08-14. Byte-for-byte, parentheticals included -- two of these say
# "non-required" and are required anyway (docs/ai_workflow/QUALITY_GATE.md).
REQUIRED_CONTEXTS = (
    "Code Linting",
    "E2E Backup (Chromium, isolated)",
    "E2E Erase Flow (Chromium, isolated, non-required)",
    "E2E Fatigue Context (Chromium, non-required)",
    "E2E Functional (Chromium)",
    "E2E Smoke (Chromium)",
    "Frontend Build (npm ci + SCSS)",
    "Run Tests",
    "Security Audit",
    "Test Inventory Drift",
    "Type Check (tsc blocking + pyright measure-only)",
)

# R1-D2: the release gate credits the Windows visual comparison that already ran on
# this commit instead of running a second one. It is not a protected context, so it
# has to be named here explicitly -- "main is green" means these 12, not the 11.
VISUAL_CONTEXT = "Visual Regression (Windows baselines)"

EXPECTED_CONTEXTS = tuple(sorted(REQUIRED_CONTEXTS + (VISUAL_CONTEXT,)))

# A third-party GitHub App can create a check-run with any name it likes. Only runs
# produced by Actions are evidence about this repository's pipeline.
ELIGIBLE_APP_SLUG = "github-actions"

# The job ids `release-gate` expects to hear from. Deleting a job from the workflow's
# `needs:` list without deleting it here is the failure this constant exists to catch.
RELEASE_JOB_IDS = (
    "ci-provenance",
    "first-install",
    "old-db-migration",
    "packaged-windows",
    "version-guard",
)

# Anchored on purpose. An unanchored variant would accept `v3.0.1-rc0`, which is the
# one thing the R1-D1 invariant exists to reject.
RELEASE_TAG_PATTERN = re.compile(r"^v\d+\.\d+\.\d+$")

TAG_REF_PREFIX = "refs/tags/"

DEFAULT_DEADLINE_SECONDS = 45 * 60
DEFAULT_POLL_SECONDS = 30
PER_PAGE = 100

# `compare/main...<sha>`: "identical" when the tag is on main's tip, "behind" when it
# is an older main commit. "ahead" is an unmerged descendant -- a feature branch --
# and "diverged" is anything else. Both must be rejected for R1-D1's "on main".
ON_MAIN_COMPARE_STATUSES = frozenset({"identical", "behind"})


# --------------------------------------------------------------------------- http


def _api_get(url: str, token: str | None):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def fetch_check_runs(repo: str, sha: str, token: str | None) -> list[dict]:
    """Every check-run on ``sha``, across pages.

    ``filter=all`` rather than the endpoint's ``latest`` default: ``latest`` dedupes
    per check-suite, so a re-run that lands in a new suite leaves two runs with one
    name and ``latest`` returns both anyway. Selecting between them is this module's
    job, not the API's.

    Paging stops on a short page rather than on ``total_count``. Trusting the
    envelope means a response that omits the key defaults the total to zero and
    stops after page 1 -- and that fails *open*: the newer failure sitting on page 2
    is never read, so the name reads as passed.
    """
    collected: list[dict] = []
    page = 1
    while True:
        payload = _api_get(
            f"{GITHUB_API}/repos/{repo}/commits/{sha}/check-runs"
            f"?filter=all&per_page={PER_PAGE}&page={page}",
            token,
        )
        runs = payload.get("check_runs") or []
        collected.extend(runs)
        if len(runs) < PER_PAGE:
            return collected
        page += 1


def tag_exists_on_remote(repo: str, tag: str, token: str | None) -> bool:
    """Whether ``tag`` exists, asked of the API rather than the checkout.

    `actions/checkout` fetches no tags by default, so `git tag -l` in a workflow is
    empty whatever the remote holds -- an existence check built on it always answers
    "no" and is a guaranteed false green.

    ``matching-refs`` is a *prefix* match, so an existing ``v3.0.10`` comes back for a
    ``v3.0.1`` query. Hence the exact comparison rather than a truth test on the list.
    """
    refs = _api_get(
        f"{GITHUB_API}/repos/{repo}/git/matching-refs/tags/"
        f"{urllib.parse.quote(tag)}",
        token,
    )
    return any(ref.get("ref") == f"{TAG_REF_PREFIX}{tag}" for ref in refs)


def commit_is_on_main(repo: str, sha: str, token: str | None) -> bool:
    """Whether ``sha`` is on ``main``, which R1-D1 requires of a release tag.

    Nothing else in the pipeline establishes this. `github.ref` carries the tag name,
    not what it points at, and provenance only asks whether the 12 contexts passed on
    this commit -- which a green feature-branch head satisfies just as well.
    """
    payload = _api_get(f"{GITHUB_API}/repos/{repo}/compare/main...{sha}", token)
    return payload.get("status") in ON_MAIN_COMPARE_STATUSES


# ------------------------------------------------------------------------ version


def read_app_version() -> str:
    from utils.version import APP_VERSION

    return APP_VERSION


def read_package_version() -> str:
    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    return package["version"]


def parse_dry_run(raw: str | None) -> bool:
    """``${{ inputs.dry_run }}`` renders as the empty string on a push event.

    Empty must mean release mode: a tag push carries no inputs, and a dispatch-only
    flag that leaked into the tag path would turn every release into a rehearsal.
    """
    return (raw or "").strip().lower() == "true"


def check_version(
    *,
    ref: str,
    dry_run: bool,
    app_version: str,
    package_version: str,
    tag_exists: Callable[[str], bool],
    is_on_main: Callable[[], bool],
    stream: TextIO,
) -> int:
    problems: list[str] = []

    if app_version != package_version:
        problems.append(
            f"version sources disagree: utils/version.py APP_VERSION is "
            f"{app_version!r} but package.json version is {package_version!r}"
        )

    # Checked on both paths. The tag path is the one that matters, but under owner
    # option (c) the rehearsal is the only path that will ever run before a real
    # release -- so if the rehearsal skipped this, an APP_VERSION of "3.0" would
    # rehearse green and red at tag time, after the version-bump PR had merged.
    if not RELEASE_TAG_PATTERN.match(f"v{app_version}"):
        problems.append(
            f"APP_VERSION {app_version!r} cannot produce a publishable tag: it must "
            f"be MAJOR.MINOR.PATCH so that 'v{app_version}' matches "
            f"{RELEASE_TAG_PATTERN.pattern}"
        )

    if ref.startswith(TAG_REF_PREFIX):
        tag = ref[len(TAG_REF_PREFIX) :]
        # R1-D1 says "on main", and this is the only thing that establishes it.
        # Rehearsals are exempt: a dispatch against a feature branch is a legitimate
        # way to exercise this workflow, and it is not a release.
        if not is_on_main():
            problems.append(
                f"tag {tag!r} does not point at a commit on main. A release tag must "
                f"be on main (R1-D1); this commit is not an ancestor of it."
            )
        # Tag identity is enforced whatever dry_run says. A rehearsal flag that could
        # switch it off on a real tag would be a bypass of the only invariant here.
        if not RELEASE_TAG_PATTERN.match(tag):
            problems.append(
                f"tag {tag!r} is not a publishable release tag: the only supported "
                f"form is an exact vMAJOR.MINOR.PATCH tag. There is no release "
                f"candidate tag class -- rehearse with workflow_dispatch and "
                f"dry_run: true against a branch instead."
            )
        elif tag != f"v{app_version}":
            problems.append(
                f"tag {tag!r} does not match the code: utils/version.py APP_VERSION "
                f"is {app_version!r} and package.json version is "
                f"{package_version!r}, so the only accepted tag is 'v{app_version}'"
            )
        else:
            print(f"[release-gate] tag {tag} matches APP_VERSION {app_version}", file=stream)
    elif not dry_run:
        problems.append(
            f"ref {ref!r} is not a tag, so this is not a release run. Dispatch "
            f"against a branch requires dry_run: true."
        )
    else:
        expected_tag = f"v{app_version}"
        if tag_exists(expected_tag):
            problems.append(
                f"rehearsal against {ref!r} but tag {expected_tag!r} already exists: "
                f"bump APP_VERSION and package.json before rehearsing the next release"
            )
        else:
            print(
                f"[release-gate] rehearsal on {ref}: versions agree at "
                f"{app_version}, tag {expected_tag} not yet published",
                file=stream,
            )

    for problem in problems:
        print(f"::error title=Release version guard::{problem}", file=stream)
    return 1 if problems else 0


# --------------------------------------------------------------------- provenance


def select_runs(
    runs: Iterable[dict], expected: Sequence[str]
) -> tuple[dict[str, dict], Counter]:
    """One eligible run per expected name: the newest by ``(started_at, id)``.

    ``id`` is the tiebreak because it is monotonic and always present, which makes the
    choice deterministic when two runs share a timestamp. Without this, a stale
    success sitting beside a newer failure could be the one that gets read.
    """
    expected_set = set(expected)
    best: dict[str, tuple[tuple[str, int], dict]] = {}
    seen: Counter = Counter()

    for run in runs:
        name = run.get("name")
        if name not in expected_set:
            continue
        if (run.get("app") or {}).get("slug") != ELIGIBLE_APP_SLUG:
            continue
        seen[name] += 1
        # A missing timestamp sorts HIGHEST, not lowest. `started_at` is the primary
        # element, so an empty-string default would put such a run below every real
        # one and the id tiebreak could not rescue it -- a newer run with no
        # timestamp would lose to an older success, which is the exact masking this
        # function exists to prevent. Sorted high, it wins and `classify` then judges
        # it on its status.
        key = (run.get("started_at") or "￿", int(run.get("id") or 0))
        if name not in best or key > best[name][0]:
            best[name] = (key, run)

    return {name: run for name, (_, run) in best.items()}, seen


def classify(
    selected: dict[str, dict], expected: Sequence[str]
) -> tuple[list[str], list[str]]:
    """Split the expected names into (still pending, concluded unsuccessfully).

    A name with no run at all is *pending*, not failed: a `needs:`-gated fan-in job
    such as `E2E Functional (Chromium)` has no check-run until its dependencies
    finish, so a release tagged promptly after a merge legitimately sees it missing.
    """
    pending: list[str] = []
    failed: list[str] = []
    for name in expected:
        run = selected.get(name)
        if run is None or run.get("status") != "completed":
            pending.append(name)
        elif run.get("conclusion") != "success":
            failed.append(name)
    return pending, failed


def report(
    selected: dict[str, dict],
    seen: Counter,
    expected: Sequence[str],
    runs: Iterable[dict],
    stream: TextIO,
) -> None:
    print("[release-gate] expected check-runs on this commit:", file=stream)
    for name in expected:
        run = selected.get(name)
        if run is None:
            print(f"  MISSING   {name}", file=stream)
            continue
        duplicate = f"  ({seen[name]} runs, selected id={run.get('id')})" if seen[name] > 1 else ""
        print(
            f"  {str(run.get('status')):<12}{str(run.get('conclusion')):<10}"
            f"{name}  id={run.get('id')}  started={run.get('started_at')}"
            f"  {run.get('html_url')}{duplicate}",
            file=stream,
        )
    # Read from the raw response, not from `seen`, which only ever counts expected
    # names. When an expected name is MISSING, this list is what shows whether the
    # job was renamed rather than never run.
    extra = sorted({str(run["name"]) for run in runs if run.get("name")} - set(expected))
    if extra:
        print(f"[release-gate] other check-runs present (informational): {extra}", file=stream)


def check_provenance(
    *,
    repo: str,
    sha: str,
    expected: Sequence[str],
    fetch: Callable[[str, str], list[dict]],
    deadline_seconds: float,
    poll_seconds: float,
    monotonic: Callable[[], float],
    sleep: Callable[[float], None],
    stream: TextIO,
) -> int:
    if not expected:
        print(
            "::error title=Release provenance::the expected-context list is empty, "
            "so this check would pass without proving anything",
            file=stream,
        )
        return 1

    deadline = monotonic() + deadline_seconds
    while True:
        runs = fetch(repo, sha)
        selected, seen = select_runs(runs, expected)
        pending, failed = classify(selected, expected)

        if failed:
            report(selected, seen, expected, runs, stream)
            print(
                f"::error title=Release provenance::{sha} did not pass CI: "
                f"{failed} did not conclude success",
                file=stream,
            )
            return 1

        if not pending:
            report(selected, seen, expected, runs, stream)
            print(
                f"[release-gate] all {len(expected)} expected check-runs succeeded on {sha}",
                file=stream,
            )
            return 0

        if monotonic() >= deadline:
            report(selected, seen, expected, runs, stream)
            print(
                f"::error title=Release provenance::timed out after "
                f"{deadline_seconds:.0f}s waiting for {pending} on {sha}",
                file=stream,
            )
            return 1

        print(f"[release-gate] waiting on {len(pending)} check-runs: {pending}", file=stream)
        sleep(poll_seconds)


# -------------------------------------------------------------------------- fan-in


def check_fan_in(
    *, needs_json: str, expected_ids: Sequence[str], stream: TextIO
) -> int:
    needs = json.loads(needs_json)
    actual = sorted(needs)
    expected = sorted(expected_ids)

    if actual != expected:
        print(
            f"::error title=Release gate::the set of jobs that reported is not the "
            f"expected set. reported={actual} expected={expected}",
            file=stream,
        )
        return 1

    unsuccessful = [
        f"{job}={result.get('result')}"
        for job, result in sorted(needs.items())
        if result.get("result") != "success"
    ]
    if unsuccessful:
        print(
            f"::error title=Release gate::not every release job succeeded: "
            f"{unsuccessful}",
            file=stream,
        )
        return 1

    print(f"[release-gate] all {len(expected)} release jobs succeeded: {expected}", file=stream)
    return 0


# ----------------------------------------------------------------------------- cli


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    version = sub.add_parser("version", help="tag identity and version-source parity")
    version.add_argument("--ref", required=True, help="github.ref of the run")
    version.add_argument("--dry-run", default="", help="raw ${{ inputs.dry_run }}")
    version.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))

    provenance = sub.add_parser("provenance", help="the commit passed the CI pipeline")
    provenance.add_argument("--sha", required=True)
    provenance.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))

    sub.add_parser("fan-in", help="every release job reported and succeeded")

    args = parser.parse_args(argv)
    token = os.environ.get("GITHUB_TOKEN")

    if args.command == "version":
        return check_version(
            ref=args.ref,
            dry_run=parse_dry_run(args.dry_run),
            app_version=read_app_version(),
            package_version=read_package_version(),
            tag_exists=lambda tag: tag_exists_on_remote(args.repo, tag, token),
            is_on_main=lambda: commit_is_on_main(args.repo, os.environ["GITHUB_SHA"], token),
            stream=sys.stdout,
        )

    if args.command == "provenance":
        return check_provenance(
            repo=args.repo,
            sha=args.sha,
            expected=EXPECTED_CONTEXTS,
            fetch=lambda repo, sha: fetch_check_runs(repo, sha, token),
            deadline_seconds=DEFAULT_DEADLINE_SECONDS,
            poll_seconds=DEFAULT_POLL_SECONDS,
            monotonic=time.monotonic,
            sleep=time.sleep,
            stream=sys.stdout,
        )

    return check_fan_in(
        needs_json=os.environ["RELEASE_NEEDS"],
        expected_ids=RELEASE_JOB_IDS,
        stream=sys.stdout,
    )


if __name__ == "__main__":
    raise SystemExit(main())
