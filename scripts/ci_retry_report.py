"""G7: an attempt-preserving retry summary for one Playwright job.

Reads the built-in JSON reporter of @playwright/test 1.61.0: top-level config, suites,
errors and stats; one suite per spec file holding specs and nested describe suites;
one test per project in each spec; one result per attempt, numbered by a 0-based
`retry`. Every attempt is appended to the step summary. A missing, malformed,
unsupported, partial or inconsistent report is stated as unavailable, never as zero
retries, and every report outcome exits 0 so the summary cannot change the verdict.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path
from typing import Any, NamedTuple

SUPPORTED_PLAYWRIGHT_VERSIONS: tuple[str, ...] = ("1.61.0",)
STATUSES = frozenset({"passed", "failed", "timedOut", "skipped", "interrupted"})
OUTCOMES = ("expected", "skipped", "unexpected", "flaky")
CLASSIFICATIONS = (
    "first-attempt", "recovered", "rerun", "exhausted", "failed", "skipped", "did-not-run", "interrupted",
)
UNREAD = frozenset({"missing", "malformed", "reporter-error"})
SEP = " › "
NOT_ZERO = "Retry totals are unavailable; this is not a report of zero retries."
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

Entry = tuple[tuple[object, ...], dict[str, Any], Any]


class Malformed(ValueError):
    pass


class Report(NamedTuple):
    version: str
    shard: str | None
    policy: dict[str, int]
    errors: list[Any]
    stats: dict[str, Any]
    tests: list[dict[str, Any]]
    reported: list[Any]


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _require(condition: bool, problem: str) -> None:
    if not condition:
        raise Malformed(problem)


def classify(expected: str, statuses: list[str], retries: int) -> str:
    if not statuses:
        return "skipped" if expected == "skipped" else "did-not-run"
    if statuses[-1] == "interrupted":
        return "interrupted"
    if expected == "skipped" and all(status == "skipped" for status in statuses):
        return "skipped"
    if all(status == "skipped" for status in statuses):
        return "did-not-run"
    if statuses[-1] == expected:
        if len(statuses) == 1:
            return "first-attempt"
        return "recovered" if set(statuses[:-1]) - {expected, "skipped"} else "rerun"
    return "exhausted" if len(statuses) == retries + 1 else "failed"


def outcome(expected: str, statuses: list[str]) -> str:
    """Playwright's computeTestCaseOutcome."""
    ran = [status for status in statuses if status not in ("interrupted", "skipped")]
    matched = sum(status == expected for status in ran)
    if not ran:
        return "skipped"
    if matched == len(ran):
        return "expected"
    if not matched and not (expected == "skipped" and "skipped" in statuses):
        return "unexpected"
    return "flaky"


def _attempts(results: Any, where: str) -> list[dict[str, Any]]:
    _require(isinstance(results, list), f"{where}: results is not a list")
    attempts = []
    for index, result in enumerate(results):
        _require(isinstance(result, dict), f"{where}: a result is not an object")
        status, retry, duration = result.get("status"), result.get("retry"), result.get("duration")
        _require(isinstance(status, str) and status in STATUSES, f"{where}: unknown result status {status!r}")
        _require(_is_int(retry) and retry == index, f"{where}: attempt {index} is numbered {retry!r}")
        _require(isinstance(duration, (int, float)) and not isinstance(duration, bool), f"{where}: duration is not a number")
        attempts.append({"retry": retry, "status": status, "duration_ms": duration})
    return attempts


def _test(spec: dict[str, Any], title: str, test: Any, policy: dict[str, int]) -> Entry:
    where = f"{spec['file']}:{spec['line']} {title}"
    _require(isinstance(test, dict), f"{where}: a test is not an object")
    expected, project = test.get("expectedStatus"), test.get("projectId")
    _require(isinstance(expected, str) and expected in STATUSES, f"{where}: unknown expectedStatus {expected!r}")
    _require(isinstance(project, str) and project in policy, f"{where}: projectId {project!r} is not a configured project")
    _require(isinstance(test.get("status"), str), f"{where}: status is not text")
    attempts = _attempts(test.get("results"), where)
    classification = classify(expected, [attempt["status"] for attempt in attempts], policy[project])
    entry = {
        "file": spec["file"], "line": spec["line"], "title": title, "project": project,
        "expected_status": expected, "attempts": attempts, "classification": classification,
    }
    return (spec["file"], spec["line"], spec["column"], title, project), entry, test["status"]


def _walk(suite: Any, titles: list[str], policy: dict[str, int], found: list[Entry]) -> None:
    _require(isinstance(suite, dict), "a suite is not an object")
    specs, children = suite.get("specs"), suite.get("suites", [])
    _require(isinstance(specs, list) and isinstance(children, list), "a suite's specs or suites is not a list")
    for spec in specs:
        _require(
            isinstance(spec, dict) and isinstance(spec.get("title"), str) and isinstance(spec.get("file"), str)
            and _is_int(spec.get("line")) and _is_int(spec.get("column")) and isinstance(spec.get("tests"), list),
            "a spec lacks a text title/file, integer line/column or a tests list",
        )
        title = SEP.join([*titles, spec["title"]])
        found.extend(_test(spec, title, test, policy) for test in spec["tests"])
    for child in children:
        _require(isinstance(child, dict) and isinstance(child.get("title"), str), "a nested suite has no text title")
        _walk(child, [*titles, child["title"]], policy, found)


def _parse(data: Any) -> Report:
    _require(isinstance(data, dict), "the top level is not an object")
    config, suites, errors, stats = data.get("config"), data.get("suites"), data.get("errors"), data.get("stats")
    _require(isinstance(config, dict), "config is not an object")
    version, projects, shard = config.get("version"), config.get("projects"), config.get("shard")
    _require(isinstance(version, str), "config.version is not text")
    _require(
        isinstance(projects, list) and all(
            isinstance(item, dict) and isinstance(item.get("id"), str) and _is_int(item.get("retries")) for item in projects
        ),
        "config.projects is not a list of projects with a text id and integer retries",
    )
    policy = {project["id"]: project["retries"] for project in projects}
    _require(len(policy) == len(projects), "config.projects repeats a project id")
    _require(
        shard is None or isinstance(shard, dict) and _is_int(shard.get("current")) and _is_int(shard.get("total")),
        "config.shard is neither null nor {current, total}",
    )
    _require(isinstance(suites, list) and isinstance(errors, list), "suites or errors is not a list")
    _require(isinstance(stats, dict) and all(_is_int(stats.get(name)) for name in OUTCOMES), "stats lacks integer counts")
    found: list[Entry] = []
    for suite in suites:
        _walk(suite, [], policy, found)
    seen: set[tuple[object, ...]] = set()
    for identity, _, _ in found:
        _require(identity not in seen, f"two tests share one file/line/column/title/project identity {identity}")
        seen.add(identity)
    return Report(
        version=version,
        shard=None if shard is None else f"{shard['current']}/{shard['total']}",
        policy=policy,
        errors=errors,
        stats=stats,
        tests=[entry for _, entry, _ in found],
        reported=[status for _, _, status in found],
    )


def _first_line(error: Any) -> str:
    message = error.get("message") if isinstance(error, dict) else error
    lines = ANSI.sub("", str(message)).strip().splitlines()
    return lines[0][:200] if lines else "no message"


def _partial(report: Report) -> list[str]:
    problems = []
    if report.errors:
        problems.append(f"{len(report.errors)} top-level error(s), first: {_first_line(report.errors[0])}")
    if not report.tests:
        problems.append("the report holds no tests")
    interrupted = sum(test["classification"] == "interrupted" for test in report.tests)
    if interrupted:
        problems.append(f"{interrupted} test(s) were interrupted")
    unstarted = sum(not test["attempts"] and test["expected_status"] != "skipped" for test in report.tests)
    if unstarted:
        problems.append(f"{unstarted} test(s) never started")
    return problems


def _inconsistent(report: Report, step_outcome: str, expect_shard: str | None) -> list[str]:
    outcomes = [outcome(test["expected_status"], [a["status"] for a in test["attempts"]]) for test in report.tests]
    recount = {name: outcomes.count(name) for name in OUTCOMES}
    declared = {name: report.stats[name] for name in OUTCOMES}
    problems = []
    if recount != declared:
        problems.append(f"stats {declared} disagree with the tests' attempts {recount}")
    disagreeing = sum(reported != found for reported, found in zip(report.reported, outcomes, strict=True))
    if disagreeing:
        problems.append(f"{disagreeing} test status(es) disagree with their attempts")
    if expect_shard is not None and expect_shard != report.shard:
        problems.append(f"the job ran shard {expect_shard} but the report is {report.shard or 'unsharded'}")
    unexpected = recount["unexpected"]
    if step_outcome == "success" and unexpected:
        problems.append(f"the test step succeeded with {unexpected} unexpected test(s)")
    elif step_outcome == "failure" and not unexpected:
        problems.append("the test step failed with no unexpected test")
    elif step_outcome not in ("success", "failure"):
        problems.append(f"test step outcome {step_outcome!r} is neither success nor failure")
    return problems


def _unavailable(
    reason: str,
    detail: str,
    version: str | None = None,
    shard: str | None = None,
    policy: dict[str, int] | None = None,
    tests: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "status": "unavailable", "reason": reason, "detail": detail, "reporter_version": version,
        "shard": shard, "retry_policy": policy or {}, "tests": tests or [], "counts": None,
    }


def _readable_version(data: Any) -> str | None:
    config = data.get("config") if isinstance(data, dict) else None
    version = config.get("version") if isinstance(config, dict) else None
    return version if isinstance(version, str) else None


def analyze(path: Path, *, step_outcome: str, expect_shard: str | None = None) -> dict[str, Any]:
    try:
        data = json.loads(path.read_bytes().decode("utf-8"))
    except FileNotFoundError:
        return _unavailable("missing", f"{path} was not written")
    except (OSError, ValueError, RecursionError) as exc:
        return _unavailable("malformed", f"{path} is not readable UTF-8 JSON: {exc}")
    try:
        report = _parse(data)
    except (Malformed, RecursionError) as exc:
        return _unavailable("malformed", str(exc), _readable_version(data))
    context = (report.version, report.shard, report.policy)
    if report.version not in SUPPORTED_PLAYWRIGHT_VERSIONS:
        detail = f"Playwright {report.version} is not a pinned version ({', '.join(SUPPORTED_PLAYWRIGHT_VERSIONS)})"
        return _unavailable("unsupported-reporter", detail, *context)
    problems = _partial(report)
    if problems:
        return _unavailable("partial", "; ".join(problems), *context, report.tests)
    problems = _inconsistent(report, step_outcome, expect_shard)
    if problems:
        return _unavailable("inconsistent", "; ".join(problems), *context, report.tests)
    counts = dict.fromkeys(CLASSIFICATIONS, 0)
    for test in report.tests:
        counts[test["classification"]] += 1
    return {
        "status": "retries" if any(len(test["attempts"]) > 1 for test in report.tests) else "no-retries",
        "reason": None, "detail": "", "reporter_version": report.version, "shard": report.shard,
        "retry_policy": report.policy, "tests": report.tests, "counts": counts,
    }


def _flat(text: str) -> str:
    return " ".join(text.splitlines())


def _row(test: dict[str, Any]) -> str:
    identity = _flat(f"{test['file']}:{test['line']}{SEP}{test['title']} [{test['project']}]")
    identity = identity.replace("`", "'").replace("|", "\\|")
    tries = " → ".join(
        f"#{attempt['retry']} {attempt['status']} ({attempt['duration_ms'] / 1000:.1f}s)" for attempt in test["attempts"]
    )
    return f"| `{identity}` | {test['classification']} | {tries or 'never started'} |"


def render(result: dict[str, Any], label: str, step_outcome: str, run_attempt: str | None) -> str:
    status, reason, shard = result["status"], result["reason"], result["shard"]
    state = {"no-retries": "no retries", "retries": "retries observed"}.get(status, f"unavailable ({reason})")
    policy = ", ".join(f"{project} retries={retries}" for project, retries in result["retry_policy"].items())
    if shard:
        scope = f"shard {shard}"
    elif reason in UNREAD:
        scope = "shard unknown"
    else:
        scope = "unsharded"
    if run_attempt:
        scope = f"Workflow run attempt {run_attempt}, {scope}"
    outcome_text = _flat(step_outcome).replace("`", "'")
    lines = [
        f"### Retry report — {_flat(label)}",
        "",
        f"**Status:** {state}",
        "",
        f"Original test step outcome: `{outcome_text}`. This summary reports that outcome and does not change it.",
        "",
        f"- Reporter: Playwright JSON {result['reporter_version'] or '(version unknown)'}",
        f"- Retry policy: {policy or 'unknown'}",
        f"- Scope: {scope}",
        "",
    ]
    if status == "unavailable":
        lines += [f"Reason: {_flat(result['detail'])}", "", NOT_ZERO, ""]
    else:
        lines += ["| Classification | Tests |", "|---|---:|", *(f"| {k} | {n} |" for k, n in result["counts"].items()), ""]
    rows = [
        _row(test) for test in result["tests"]
        if len(test["attempts"]) > 1 or test["classification"] not in ("first-attempt", "skipped")
    ]
    if rows:
        lines += ["| Test | Classification | Attempts |", "|---|---|---|", *rows, ""]
    return "\n".join(lines) + "\n"


def _escape(value: str, *, prop: bool = False) -> str:
    value = value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    return value.replace(":", "%3A").replace(",", "%2C") if prop else value


def annotation(result: dict[str, Any], label: str) -> str | None:
    if result["status"] == "retries":
        retried = sum(len(test["attempts"]) > 1 for test in result["tests"])
        message = f"{retried} test(s) needed more than one attempt; the job summary lists every attempt."
    elif result["status"] == "unavailable":
        message = f"Retry report unavailable ({result['reason']}); this is not a report of zero retries."
    else:
        return None
    return f"::warning title={_escape(f'Retry report: {label}', prop=True)}::{_escape(message)}"


def _append(path: Path, markdown: str) -> bool:
    try:
        with path.open("a", encoding="utf-8", errors="replace") as handle:
            handle.write(markdown)
    except OSError:
        return False
    return True


def _outputs(result: dict[str, Any], args: argparse.Namespace) -> tuple[str, str | None]:
    return render(result, args.label, args.step_outcome, args.run_attempt), annotation(result, args.label)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--step-outcome", required=True, help="the test step's outcome; free text, never a usage error")
    parser.add_argument("--expect-shard", help="I/N the job ran, e.g. 1/4")
    parser.add_argument("--run-attempt")
    parser.add_argument("--summary-file", type=Path, help="append the markdown here as UTF-8; stdout otherwise or on failure")
    args = parser.parse_args(argv)
    try:
        result = analyze(args.report, step_outcome=args.step_outcome, expect_shard=args.expect_shard)
        markdown, warning = _outputs(result, args)
    except Exception as exc:  # the summary must never change the test step's verdict
        markdown, warning = _outputs(_unavailable("reporter-error", f"{type(exc).__name__}: {exc}"), args)
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if warning:
        print(warning)
    if args.summary_file is None or not _append(args.summary_file, markdown):
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
