"""Deterministic Deep Gate watchdog (CI/CD expansion D3).

Each watched workflow is tracked on its own: a non-success completion upserts that
workflow's `deep-gate` failure issue, and a missing scheduled run for the current
Monday 03:17 UTC slot upserts its missing-schedule issue. Evidence the API cannot
deliver is reported as unavailable and never read as healthy.
``tests/test_ci_expansion_contracts.py`` pins the behaviour.

    python scripts/deep_gate_watch.py reconcile --repo OWNER/REPO \
        [--event-path PATH] [--now ISO8601] [--dry-run]
"""
from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

UTC = timezone.utc
DEFAULT_BRANCH = "main"
SLOT_WEEKDAY = 0  # Monday
SLOT_TIME = (3, 17)  # 03:17 UTC, the cron both watched workflows share
MISSING_THRESHOLD = timedelta(hours=20)  # alarm point after the slot
FRESHNESS_DEADLINE = timedelta(hours=36)  # approved bound; detection must precede it
HISTORY_WINDOW = timedelta(days=21)
MAX_PAGES = 50
DEFAULT_API_URL = "https://api.github.com"

VISUAL_JOB_NAME = "Visual regression (Linux baselines)"
COMPARE_STEP_NAME = "Run visual specs (compare)"
NO_WRITE_STEP_NAME = "Assert compare mode wrote no baseline"
ISSUE_LABEL = "deep-gate"
MARKER_PREFIX = "<!-- deep-gate-watch v1 "
MARKER = re.compile(r"<!-- deep-gate-watch v1 workflow=(\S+) kind=(\S+) ([^>]*?) ?-->")
FAILURE, MISSING = "failure", "missing-schedule"

Run = dict[str, Any]


@dataclass(frozen=True)
class Watched:
    file: str
    name: str
    kind: str  # "suite" or "visual"

    @property
    def path(self) -> str:
        return f".github/workflows/{self.file}"


WATCHED = (
    Watched(file="deep-gate.yml", name="Deep Gate (manual + weekly)", kind="suite"),
    Watched(file="deep-gate-visual.yml", name="Deep Gate Visual (Linux)", kind="visual"),
)


class EvidenceUnavailable(Exception):
    """The API did not deliver complete, well-formed evidence."""


@dataclass(frozen=True)
class Evidence:
    kind: str  # failure | recovery | non_evaluative | ignored
    reason: str
    run: Run
    jobs: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class State:
    status: str  # failing | healthy | unknown
    evidence: Evidence | None = None


@dataclass(frozen=True)
class Freshness:
    status: str  # fresh | pending | late | missing
    slot: datetime
    run: Run | None = None


@dataclass(frozen=True)
class Action:
    verb: str  # create | update | close
    kind: str  # failure | missing-schedule
    number: int | None
    reason: str
    title: str = ""
    body: str = ""
    comment: str = ""
    state_reason: str = "completed"


@dataclass
class Outcome:
    watched: Watched
    failure: State | None = None
    freshness: Freshness | None = None
    actions: list[Action] = field(default_factory=list)
    error: str = ""


@dataclass
class Report:
    outcomes: list[Outcome]
    dry_run: bool

    @property
    def unavailable(self) -> list[str]:
        return [o.watched.file for o in self.outcomes if o.error]


# ------------------------------------------------------------------ pure decisions


def parse_time(value: str) -> datetime:
    moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return (moment if moment.tzinfo else moment.replace(tzinfo=UTC)).astimezone(UTC)


def iso(moment: datetime) -> str:
    return moment.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def expected_slot(now: datetime) -> datetime:
    now = now.astimezone(UTC)
    slot = now.replace(hour=SLOT_TIME[0], minute=SLOT_TIME[1], second=0, microsecond=0)
    slot -= timedelta(days=(now.weekday() - SLOT_WEEKDAY) % 7)
    return slot - timedelta(days=7) if slot > now else slot


def evidence_key(run: Run) -> tuple[datetime, int, int]:
    return parse_time(run["created_at"]), int(run["id"]), int(run.get("run_attempt") or 1)


def _step(job: dict[str, Any], name: str) -> dict[str, Any]:
    return next((s for s in job.get("steps") or [] if s.get("name") == name), {})


def _executed_compare(jobs: list[dict[str, Any]]) -> bool:
    return any(
        job.get("name") == VISUAL_JOB_NAME
        and job.get("conclusion") == "success"
        and _step(job, COMPARE_STEP_NAME).get("conclusion") == "success"
        and _step(job, NO_WRITE_STEP_NAME).get("conclusion") == "success"
        for job in jobs
    )


def classify_run(watched: Watched, run: Run, jobs: list[dict[str, Any]] | None) -> Evidence:
    if run.get("path") != watched.path:
        return Evidence("ignored", "other workflow", run)
    if run.get("head_branch") != DEFAULT_BRANCH:
        return Evidence("ignored", "other branch", run)
    if run.get("status") != "completed":
        return Evidence("non_evaluative", "incomplete", run)
    conclusion = run.get("conclusion")
    if conclusion != "success":
        return Evidence("failure", f"concluded {conclusion}", run, list(jobs or []))
    if jobs is None:
        raise EvidenceUnavailable(f"run {run.get('id')}: jobs were not read")
    if watched.kind == "suite":
        if jobs and all(job.get("conclusion") == "success" for job in jobs):
            return Evidence("recovery", "every job succeeded", run, jobs)
        return Evidence("non_evaluative", "not every job succeeded", run, jobs)
    if _executed_compare(jobs):
        return Evidence("recovery", "compare step executed and succeeded", run, jobs)
    return Evidence("non_evaluative", "no executed compare step", run, jobs)


def failure_state(watched: Watched, evidences: list[Evidence]) -> State:
    evaluative = [
        e for e in evidences if e.kind in ("failure", "recovery") and e.run.get("path") == watched.path
    ]
    if not evaluative:
        return State("unknown")
    newest = max(evaluative, key=lambda e: evidence_key(e.run))
    return State("failing" if newest.kind == "failure" else "healthy", newest)


def freshness_state(watched: Watched, runs: list[Run], now: datetime) -> Freshness:
    slot = expected_slot(now)
    qualifying = [
        r
        for r in runs
        if r.get("path") == watched.path
        and r.get("event") == "schedule"
        and r.get("head_branch") == DEFAULT_BRANCH
        and slot <= parse_time(r["created_at"]) < slot + timedelta(days=7)
    ]
    completed = [r for r in qualifying if r.get("status") == "completed"]
    if completed:
        return Freshness("fresh", slot, max(completed, key=evidence_key))
    running = max(qualifying, key=evidence_key, default=None)
    if now < slot + MISSING_THRESHOLD:
        return Freshness("pending", slot, running)
    return Freshness("late" if running else "missing", slot, running)


# ------------------------------------------------------------------ issue planning


def _marker(watched: Watched, kind: str, ident: str) -> str:
    return f"{MARKER_PREFIX}workflow={watched.file} kind={kind} {ident} -->"


def _fields(issue: dict[str, Any], watched: Watched, kind: str) -> dict[str, str] | None:
    found = MARKER.search(issue.get("body") or "")
    if found is None or (found[1], found[2]) != (watched.file, kind):
        return None
    return dict(part.split("=", 1) for part in found[3].split() if "=" in part)


def _held_failure_key(fields: dict[str, str]) -> tuple[datetime, int, int] | None:
    try:
        run_id, attempt = fields["evidence"].split(".")
        return parse_time(fields["created"]), int(run_id), int(attempt)
    except (KeyError, ValueError):
        return None


def _held_slot(fields: dict[str, str]) -> datetime | None:
    try:
        return parse_time(fields["slot"])
    except (KeyError, ValueError):
        return None


def _run_line(run: Run) -> str:
    return f"[{run.get('id')} attempt {run.get('run_attempt') or 1}]({run.get('html_url')})"


def _failed_jobs(jobs: list[dict[str, Any]]) -> list[str]:
    lines = []
    for job in jobs:
        if job.get("conclusion") in ("success", "skipped"):
            continue
        step = next(
            (
                s.get("name")
                for s in job.get("steps") or []
                if s.get("conclusion") in ("failure", "timed_out", "cancelled")
            ),
            None,
        )
        where = f"first failing step `{step}`" if step else "no failing step reported"
        lines.append(f"  - `{job.get('name')}` ({job.get('conclusion')}): {where}")
    return lines or ["  - none reported by the API (the run may not have started a job)"]


def _recovery_rule(watched: Watched) -> str:
    if watched.kind == "visual":
        return (
            f"a newer run of this workflow on `{DEFAULT_BRANCH}` whose `{COMPARE_STEP_NAME}` "
            "step executed and succeeded (generation-mode or skipped comparisons do not count)"
        )
    return f"a newer run of this workflow on `{DEFAULT_BRANCH}` in which every job succeeded"


def failure_issue(watched: Watched, evidence: Evidence) -> tuple[str, str]:
    run = evidence.run
    key = evidence_key(run)
    ident = f"evidence={key[1]}.{key[2]} created={iso(key[0])}"
    body = "\n".join(
        [
            _marker(watched, FAILURE, ident),
            f"**{watched.name}** did not succeed.",
            "",
            f"- Workflow: {watched.name} (`{watched.path}`)",
            f"- Run: {_run_line(run)}",
            f"- Head SHA: `{run.get('head_sha')}`",
            f"- Event: `{run.get('event')}`",
            f"- Conclusion: `{run.get('conclusion')}`",
            f"- Observed: created {run.get('created_at')}, last updated {run.get('updated_at')}",
            "- Failed jobs:",
            *_failed_jobs(evidence.jobs),
            "",
            "Status: UNRESOLVED",
            "",
            f"Closes automatically on {_recovery_rule(watched)}.",
        ]
    )
    return f"Deep Gate watch: {watched.name} — failing", body


def missing_issue(watched: Watched, fresh: Freshness) -> tuple[str, str]:
    if fresh.run is not None:
        observed = (
            f"late: scheduled run {_run_line(fresh.run)} was created {fresh.run.get('created_at')} "
            f"and is still `{fresh.run.get('status')}`"
        )
    else:
        observed = f"missing: no `schedule` run of this workflow on `{DEFAULT_BRANCH}` since the slot"
    hours = int(MISSING_THRESHOLD.total_seconds() // 3600)
    deadline = int(FRESHNESS_DEADLINE.total_seconds() // 3600)
    body = "\n".join(
        [
            _marker(watched, MISSING, f"slot={iso(fresh.slot)}"),
            f"**{watched.name}** has no completed scheduled run for the {fresh.slot:%Y-%m-%d} slot.",
            "",
            f"- Workflow: {watched.name} (`{watched.path}`)",
            f"- Expected slot: {iso(fresh.slot)} (Monday 03:17 UTC)",
            f"- Observed: {observed}",
            f"- Alarm after slot + {hours} h; approved freshness bound slot + {deadline} h",
            "- Manual runs, earlier weeks' runs and other workflows' runs never satisfy this check.",
            "",
            "Status: UNRESOLVED",
            "",
            "Closes automatically when a scheduled run for this slot or a later one completes.",
        ]
    )
    return f"Deep Gate watch: {watched.name} — missing scheduled run", body


def recovery_comment(watched: Watched, evidence: Evidence) -> str:
    run = evidence.run
    detail = (
        f"its `{COMPARE_STEP_NAME}` step (job `{VISUAL_JOB_NAME}`) executed and succeeded"
        if watched.kind == "visual"
        else "every job succeeded"
    )
    return (
        f"Recovered: {watched.name} run {_run_line(run)} on head `{run.get('head_sha')}` "
        f"(event `{run.get('event')}`, created {run.get('created_at')}): {detail}. Closing."
    )


def _plan_failure(watched: Watched, state: State, issue: dict[str, Any] | None) -> list[Action]:
    if state.evidence is None:
        return []
    key = evidence_key(state.evidence.run)
    held = _held_failure_key(_fields(issue, watched, FAILURE) or {}) if issue else None
    newer_or_same = held is not None and held >= key
    if state.status == "failing":
        title, body = failure_issue(watched, state.evidence)
        reason = f"run {key[1]} attempt {key[2]} {state.evidence.reason}"
        if issue is None:
            return [Action("create", FAILURE, None, reason, title, body)]
        return [] if newer_or_same else [Action("update", FAILURE, issue["number"], reason, title, body)]
    if issue is None or newer_or_same:
        return []
    comment = recovery_comment(watched, state.evidence)
    return [Action("close", FAILURE, issue["number"], f"recovered by run {key[1]}", comment=comment)]


def _plan_freshness(watched: Watched, fresh: Freshness, issue: dict[str, Any] | None) -> list[Action]:
    held = _held_slot(_fields(issue, watched, MISSING) or {}) if issue else None
    if fresh.status in ("missing", "late"):
        title, body = missing_issue(watched, fresh)
        reason = f"{fresh.status} for slot {iso(fresh.slot)}"
        if issue is None:
            return [Action("create", MISSING, None, reason, title, body)]
        if held is not None and held >= fresh.slot:
            return []
        return [Action("update", MISSING, issue["number"], reason, title, body)]
    if fresh.status == "fresh" and fresh.run is not None and issue is not None:
        if held is None or held <= fresh.slot:
            comment = (
                f"Scheduled run {_run_line(fresh.run)} for the {iso(fresh.slot)} slot completed "
                f"(conclusion `{fresh.run.get('conclusion')}`). Freshness restored; a failing "
                "conclusion is tracked by the separate failure issue. Closing."
            )
            return [Action("close", MISSING, issue["number"], f"fresh run {fresh.run.get('id')}", comment=comment)]
    return []


def plan_actions(
    watched: Watched, failure: State, fresh: Freshness, open_issues: list[dict[str, Any]]
) -> list[Action]:
    actions: list[Action] = []
    for kind in (FAILURE, MISSING):
        mine = sorted(
            (i for i in open_issues if _fields(i, watched, kind) is not None), key=lambda i: i["number"]
        )
        primary = mine[0] if mine else None
        for duplicate in mine[1:]:
            note = f"Duplicate of #{mine[0]['number']}; the watch keeps one open issue per workflow and kind."
            actions.append(
                Action("close", kind, duplicate["number"], "duplicate", comment=note, state_reason="not_planned")
            )
        if kind == FAILURE:
            actions += _plan_failure(watched, failure, primary)
        else:
            actions += _plan_freshness(watched, fresh, primary)
    return actions


# ------------------------------------------------------------------ GitHub REST client


def _next_link(header: str) -> str | None:
    for url, rels in re.findall(r'<([^>]+)>\s*;\s*rel="([^"]+)"', header):
        if "next" in rels.split():
            return url
    return None


class GitHubClient:
    def __init__(self, repo: str, token: str, api_url: str = DEFAULT_API_URL, timeout: float = 30.0):
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo):
            raise ValueError(f"not an OWNER/REPO name: {repo!r}")
        self.origin = api_url.rstrip("/")
        self.base = f"{self.origin}/repos/{repo}"
        self.token = token
        self.timeout = timeout
        self._label_ready = False

    def _call(self, method: str, url: str, body: Any = None, missing_ok: bool = False) -> tuple[Any, str]:
        request = urllib.request.Request(
            url,
            data=None if body is None else json.dumps(body).encode(),
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "deep-gate-watch",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw, link = response.read(), response.headers.get("Link") or ""
        except urllib.error.HTTPError as exc:
            exc.close()
            if missing_ok and exc.code == 404:
                return None, ""
            raise EvidenceUnavailable(f"{method} {url}: HTTP {exc.code}") from exc
        except (OSError, http.client.HTTPException) as exc:
            raise EvidenceUnavailable(f"{method} {url}: {exc!r}") from exc
        try:
            return (json.loads(raw) if raw else None), link
        except ValueError as exc:
            raise EvidenceUnavailable(f"{method} {url}: malformed JSON") from exc

    def _pages(self, path: str, query: dict[str, Any], envelope: str | None) -> list[dict[str, Any]]:
        url = f"{self.base}{path}?{urllib.parse.urlencode(query)}"
        items: list[dict[str, Any]] = []
        for _ in range(MAX_PAGES):
            payload, link = self._call("GET", url)
            chunk = payload.get(envelope) if envelope and isinstance(payload, dict) else payload
            if not isinstance(chunk, list) or not all(isinstance(item, dict) for item in chunk):
                raise EvidenceUnavailable(f"GET {url}: unexpected payload shape")
            items += chunk
            following = _next_link(link)
            if following is None:
                return items
            if not following.startswith(self.origin + "/"):
                raise EvidenceUnavailable(f"GET {url}: pagination left {self.origin}")
            url = following
        raise EvidenceUnavailable(f"GET {path}: more than {MAX_PAGES} pages")

    def list_runs(self, file: str, since: datetime) -> list[Run]:
        query = {"branch": DEFAULT_BRANCH, "per_page": 100, "created": f">={since.date().isoformat()}"}
        return self._pages(f"/actions/workflows/{urllib.parse.quote(file)}/runs", query, "workflow_runs")

    def list_jobs(self, run: Run) -> list[dict[str, Any]]:
        attempt = run.get("run_attempt") or 1
        jobs = self._pages(f"/actions/runs/{int(run['id'])}/attempts/{int(attempt)}/jobs", {"per_page": 100}, "jobs")
        for job in jobs:
            if (job.get("run_id"), job.get("run_attempt"), job.get("head_sha")) != (
                run["id"],
                attempt,
                run.get("head_sha"),
            ):
                raise EvidenceUnavailable(f"run {run['id']} attempt {attempt}: a job belongs to another run")
        return jobs

    def list_open_issues(self) -> list[dict[str, Any]]:
        query = {"state": "open", "labels": ISSUE_LABEL, "per_page": 100}
        return [i for i in self._pages("/issues", query, None) if "pull_request" not in i]

    def ensure_label(self) -> None:
        if not self._label_ready and self._call("GET", f"{self.base}/labels/{ISSUE_LABEL}", missing_ok=True)[0] is None:
            label = {"name": ISSUE_LABEL, "color": "b60205", "description": "Deep Gate watch tracking issue"}
            self._call("POST", f"{self.base}/labels", label)
        self._label_ready = True

    def apply(self, action: Action) -> None:
        if action.verb == "create":
            self.ensure_label()
            issue = {"title": action.title, "body": action.body, "labels": [ISSUE_LABEL]}
            self._call("POST", f"{self.base}/issues", issue)
        elif action.verb == "update":
            self._call("PATCH", f"{self.base}/issues/{action.number}", {"title": action.title, "body": action.body})
        else:
            self._call("POST", f"{self.base}/issues/{action.number}/comments", {"body": action.comment})
            closed = {"state": "closed", "state_reason": action.state_reason}
            self._call("PATCH", f"{self.base}/issues/{action.number}", closed)


# ------------------------------------------------------------------ reconcile


def _merge_event(runs: list[Run], delivered: Any, watched: Watched) -> list[Run]:
    """Let the delivered run supersede a stale listing of the same run id."""
    if not isinstance(delivered, dict) or delivered.get("path") != watched.path:
        return runs
    for index, listed in enumerate(runs):
        if listed.get("id") != delivered.get("id"):
            continue
        listed_attempt, attempt = listed.get("run_attempt") or 1, delivered.get("run_attempt") or 1
        stale = listed_attempt < attempt or (
            listed_attempt == attempt and listed.get("status") != "completed" and delivered.get("status") == "completed"
        )
        return [*runs[:index], delivered, *runs[index + 1:]] if stale else runs
    return [*runs, delivered]


def _evaluate(client: GitHubClient, watched: Watched, runs: list[Run]) -> list[Evidence]:
    """Newest first, reading jobs until the first evaluative run decides the state."""
    evidences = []
    for run in sorted(runs, key=evidence_key, reverse=True):
        decisive = (
            run.get("path") == watched.path
            and run.get("head_branch") == DEFAULT_BRANCH
            and run.get("status") == "completed"
        )
        evidence = classify_run(watched, run, client.list_jobs(run) if decisive else None)
        evidences.append(evidence)
        if evidence.kind in ("failure", "recovery"):
            break
    return evidences


def reconcile(client: GitHubClient, now: datetime, event: Any = None, dry_run: bool = False) -> Report:
    report = Report([Outcome(w) for w in WATCHED], dry_run)
    try:
        issues = client.list_open_issues()
    except EvidenceUnavailable as exc:
        for outcome in report.outcomes:
            outcome.error = f"open issues unreadable: {exc}"
        return report
    delivered = event.get("workflow_run") if isinstance(event, dict) else None
    for outcome in report.outcomes:
        watched = outcome.watched
        try:
            runs = _merge_event(client.list_runs(watched.file, now - HISTORY_WINDOW), delivered, watched)
            outcome.failure = failure_state(watched, _evaluate(client, watched, runs))
            outcome.freshness = freshness_state(watched, runs, now)
            outcome.actions = plan_actions(watched, outcome.failure, outcome.freshness, issues)
        except (EvidenceUnavailable, KeyError, TypeError, ValueError) as exc:
            outcome.error = f"{type(exc).__name__}: {exc}"
            continue
        if not dry_run:
            _apply(client, outcome)
    return report


def _apply(client: GitHubClient, outcome: Outcome) -> None:
    for action in outcome.actions:
        try:
            client.apply(action)
        except EvidenceUnavailable as exc:
            outcome.error = f"write failed: {exc}"
            return


# ------------------------------------------------------------------ CLI


def dispatch_latency(event: Any, now: datetime) -> int | None:
    run = event.get("workflow_run") if isinstance(event, dict) else None
    if not isinstance(run, dict) or not any(run.get("path") == w.path for w in WATCHED):
        return None
    return int((now - parse_time(run["updated_at"])).total_seconds())


def _describe(action: Action) -> str:
    target = f" #{action.number}" if action.number is not None else ""
    return f"{action.verb} {action.kind} issue{target} ({action.reason})"


def render_summary(report: Report, now: datetime, event: Any) -> str:
    latency = dispatch_latency(event, now)
    if latency is None:
        timing = "- Dispatch latency: not measured; no watched workflow run triggered this check."
    else:
        timing = (
            f"- Dispatch latency (watched run `updated_at` to watchdog start): {latency} s "
            f"(`{event['workflow_run'].get('updated_at')}` to `{iso(now)}`)"
        )
    lines = [
        "## Deep Gate watch",
        "",
        f"- Mode: {'dry run (planned actions were not applied)' if report.dry_run else 'applied'}",
        f"- Watchdog start: `{iso(now)}`",
        timing,
    ]
    for outcome in report.outcomes:
        lines += ["", f"### {outcome.watched.name} (`{outcome.watched.file}`)"]
        if outcome.error:
            lines.append(f"- Evidence unavailable: {outcome.error}. No further issue write for this workflow.")
        if outcome.failure is not None:
            run = outcome.failure.evidence.run if outcome.failure.evidence else None
            cited = f" (run {run.get('id')} attempt {run.get('run_attempt')})" if run else ""
            lines.append(f"- Failure state: {outcome.failure.status}{cited}")
        if outcome.freshness is not None:
            fresh = outcome.freshness
            lines.append(f"- Scheduled freshness for slot `{iso(fresh.slot)}`: {fresh.status}")
        if outcome.failure is not None:
            verb = "Planned" if report.dry_run else "Actions"
            described = [_describe(a) for a in outcome.actions] or ["none"]
            lines.append(f"- {verb}: " + "; ".join(described))
    return "\n".join(lines) + "\n"


def _read_event(path: str | None) -> Any:
    if not path:
        return None
    with open(path, encoding="utf-8") as handle:
        event = json.load(handle)
    if not isinstance(event, dict):
        raise ValueError("event payload is not a JSON object")
    return event


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("reconcile")
    command.add_argument("--repo", required=True)
    command.add_argument("--event-path")
    command.add_argument("--now", help="ISO 8601; also recorded as the watchdog start time")
    command.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        now = parse_time(args.now) if args.now else datetime.now(UTC)
        event = _read_event(args.event_path)
        token = os.environ.get("GH_TOKEN")
        if not token:
            raise ValueError("GH_TOKEN is not set")
        client = GitHubClient(args.repo, token, api_url=os.environ.get("GITHUB_API_URL") or DEFAULT_API_URL)
        report = reconcile(client, now, event=event, dry_run=args.dry_run)
        summary = render_summary(report, now, event)
    except Exception as exc:  # anything but unavailable evidence is a watchdog defect
        print(f"::error title=Deep Gate watch::{type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(summary)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(summary)
    for outcome in report.outcomes:
        if outcome.error:
            print(f"::error title=Deep Gate watch::{outcome.watched.file}: {outcome.error}", file=sys.stderr)
    return 2 if report.unavailable else 0


if __name__ == "__main__":
    raise SystemExit(main())
