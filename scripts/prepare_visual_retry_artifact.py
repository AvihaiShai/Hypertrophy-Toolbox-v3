"""Retain bounded Linux visual diagnostics without changing the test verdict."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts import ci_retry_report

REPO_ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 50 * 1024 * 1024
METADATA_BYTES = 1024 * 1024
SUMMARY_BYTES = 64 * 1024
ALLOWED_SUFFIXES = {".md", ".txt", ".png", ".zip", ".json"}


def _json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _identity(args: argparse.Namespace, result: dict[str, Any]) -> dict[str, Any]:
    try:
        checkout = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
            capture_output=True, text=True, timeout=5, check=False,
        )
        checkout_sha = checkout.stdout.strip() if checkout.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        checkout_sha = None
    try:
        package = json.loads((REPO_ROOT / "node_modules/playwright/package.json").read_text(encoding="utf-8"))
        version = package.get("version") if isinstance(package, dict) else None
    except (OSError, ValueError):
        version = None
    files = {
        "package_lock_sha256": REPO_ROOT / "package-lock.json",
        "browser_manifest_sha256": REPO_ROOT / "node_modules/playwright-core/browsers.json",
    }
    hashes = {}
    for key, path in files.items():
        try:
            hashes[key] = _digest(path)
        except OSError:
            hashes[key] = None
    variables = {
        "event_sha": "GITHUB_SHA", "application_base": "SOURCE_BASE",
        "job_key": "GITHUB_JOB", "run_id": "GITHUB_RUN_ID",
        "workflow_run_attempt": "GITHUB_RUN_ATTEMPT", "event": "GITHUB_EVENT_NAME",
        "visual_seed": "PW_VISUAL_SEED", "runner_image": "ImageOS",
        "runner_image_version": "ImageVersion",
    }
    return {
        **{key: os.environ.get(env, "")[:2048] or None for key, env in variables.items()},
        **hashes, "checkout_sha": checkout_sha, "playwright_version": version,
        "mode": args.mode, "test_step_outcome": args.step_outcome,
        "reported_spec_files": sorted({test["file"] for test in result["tests"]}),
    }


def _append(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8", errors="replace") as handle:
        handle.write(text)


def _metadata(identity: dict[str, Any], manifest: dict[str, Any]) -> tuple[bytes, bytes]:
    identity_bytes = _json(identity)
    for key in ("files", "tests"):
        rows = manifest[key]
        manifest[f"{key}_count"] = len(rows)
        manifest[f"{key}_sha256"] = hashlib.sha256(_json(rows)).hexdigest()
        manifest[f"{key}_complete"] = True
    while len(identity_bytes) + len(_json(manifest)) > METADATA_BYTES:
        key = max(("files", "tests"), key=lambda name: len(_json(manifest[name])))
        rows = manifest[key]
        if not rows:
            raise ValueError("diagnostic identity exceeds the metadata budget")
        manifest[key] = rows[: len(rows) // 2]
        manifest[f"{key}_complete"] = False
        manifest["retention_complete"] = False
    return identity_bytes, _json(manifest)


def _candidates(root: Path, report: Path) -> list[tuple[Path, bool]]:
    files = [(report, True), (root / "junit.xml", True)]
    results = root / "test-results"
    if results.is_symlink() or results.is_junction():
        return files + [(results, False)]
    priority = {".md": 0, ".txt": 0, ".png": 1, ".zip": 2, ".json": 3}
    found = []
    for directory, dirs, names in os.walk(results, followlinks=False):
        parent = Path(directory)
        for name in list(dirs):
            child = parent / name
            if child.is_symlink() or child.is_junction():
                found.append(child)
                dirs.remove(name)
        found.extend(parent / name for name in names)
    found.sort(key=lambda path: (priority.get(path.suffix.lower(), 4), path.relative_to(root).as_posix()))
    return files + [(path, False) for path in found]


def _copy(source: Path, target: Path, expected_size: int) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    written = 0
    created = False
    try:
        with source.open("rb") as reader, target.open("xb") as writer:
            created = True
            for block in iter(lambda: reader.read(1024 * 1024), b""):
                if written + len(block) > expected_size:
                    raise ValueError("source grew during retention")
                writer.write(block)
                digest.update(block)
                written += len(block)
        if written != expected_size:
            raise ValueError("source shrank during retention")
    except (OSError, ValueError):
        if created:
            target.unlink(missing_ok=True)
        raise
    return digest.hexdigest()


def _attempt_metadata(report: Path, root: Path, tests: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[Path]]:
    if not tests:
        return [], []
    data = json.loads(report.read_text(encoding="utf-8"))
    pending = list(reversed(data["suites"]))
    raw_tests = []
    while pending:
        suite = pending.pop()
        raw_tests.extend(test for spec in suite["specs"] for test in spec["tests"])
        pending.extend(reversed(suite.get("suites", [])))
    enriched, declared = [], []
    for test, raw in zip(tests, raw_tests, strict=True):
        attempts = []
        for attempt, raw_attempt in zip(test["attempts"], raw["results"], strict=True):
            errors = raw_attempt.get("errors") or ([raw_attempt["error"]] if raw_attempt.get("error") else [])
            messages = [
                str(error.get("message", error.get("value", "")) if isinstance(error, dict) else error).splitlines()
                for error in errors
            ]
            attachments = []
            for attachment in raw_attempt.get("attachments", []):
                entry = {
                    "name": attachment.get("name"), "content_type": attachment.get("contentType"),
                    "declared_path": attachment.get("path"), "artifact_path": None,
                }
                raw_path = attachment.get("path")
                if isinstance(raw_path, str) and raw_path:
                    path = Path(raw_path)
                    path = Path(os.path.abspath(path if path.is_absolute() else root / path))
                    if (not path.is_relative_to(root) or not path.resolve().is_relative_to(root)
                            or path.is_symlink() or path.is_junction()):
                        entry["disposition"] = "outside-root-or-link"
                    else:
                        entry["path"] = path.relative_to(root).as_posix()
                        entry["disposition"] = "pending"
                        declared.append(path)
                elif "body" in attachment:
                    entry["path"] = report.relative_to(root).as_posix()
                    entry["disposition"] = "inline-in-report"
                else:
                    entry["disposition"] = "invalid-declaration"
                attachments.append(entry)
            attempts.append({**attempt, "errors": [lines[0] if lines else "" for lines in messages], "attachments": attachments})
        enriched.append({**test, "attempts": attempts})
    return enriched, declared


def _stage(args: argparse.Namespace, result: dict[str, Any]) -> dict[str, Any]:
    root = args.artifact_root.resolve()
    report = Path(os.path.abspath(args.report))
    staging = args.staging.resolve()
    if staging == root or staging.is_relative_to(root) or root.is_relative_to(staging):
        raise ValueError("diagnostic staging and source trees must be separate")
    staging.mkdir(parents=True, exist_ok=False)
    identity = _identity(args, result)
    tests, declared = _attempt_metadata(report, root, result["tests"])
    manifest: dict[str, Any] = {
        "report_status": result["status"], "report_reason": result["reason"],
        "report_detail": result["detail"][:4096], "payload_limit_bytes": MAX_BYTES,
        "metadata_reserve_bytes": METADATA_BYTES, "retention_complete": False,
        "staging_status": "incomplete", "tests": tests, "files": [],
    }
    identity_bytes, manifest_bytes = _metadata(identity, dict(manifest))
    (staging / "identity.json").write_bytes(identity_bytes)
    (staging / "manifest.json").write_bytes(manifest_bytes)
    used = 0
    incomplete = result["status"] == "unavailable"
    counts: Counter[str] = Counter()
    seen: set[Path] = set()
    retained_types: set[str] = set()
    for path, core in _candidates(root, report) + [(path, False) for path in declared]:
        if path in seen:
            continue
        seen.add(path)
        entry: dict[str, Any] = {"path": path.relative_to(root).as_posix()}
        reason = None
        try:
            if path.is_symlink() or path.is_junction() or not path.resolve().is_relative_to(root):
                reason = "outside-root-or-link"
            elif not path.is_file():
                reason = "missing"
            else:
                size = path.stat().st_size
                entry["size_bytes"] = size
                if not core and path.suffix.lower() not in ALLOWED_SUFFIXES:
                    reason = "excluded-type"
                elif size > MAX_BYTES - METADATA_BYTES - used:
                    reason = "payload-budget"
                    if core:
                        entry["sha256"] = _digest(path)
                else:
                    entry["sha256"] = _copy(path, staging / entry["path"], size)
                    used += size
                    retained_types.add(path.suffix.lower())
        except (OSError, ValueError) as exc:
            reason = "copy-error"
            entry["detail"] = str(exc)[:500]
        entry["disposition"] = reason or "retained"
        counts[entry["disposition"]] += 1
        incomplete |= reason not in (None, "excluded-type")
        manifest["files"].append(entry)
    by_path = {entry["path"]: entry for entry in manifest["files"]}
    for test in tests:
        for attempt in test["attempts"]:
            for attachment in attempt["attachments"]:
                if attachment["disposition"] in ("pending", "inline-in-report"):
                    copied = by_path[attachment["path"]]
                    if attachment["disposition"] == "pending" or copied["disposition"] != "retained":
                        attachment["disposition"] = copied["disposition"]
                    if copied["disposition"] == "retained":
                        attachment["artifact_path"] = copied["path"]
                        attachment["sha256"] = copied["sha256"]
                incomplete |= attachment["disposition"] not in ("retained", "inline-in-report", "excluded-type")
    manifest.update({
        "retention_complete": not incomplete, "staging_status": "finished",
        "file_dispositions": dict(counts), "retained_file_bytes": used,
        "unavailable_capture_types": sorted({".png", ".md", ".zip"} - retained_types),
        "capture_limit": "Only existing files are retained; this packet does not record an initial-attempt trace.",
    })
    identity_bytes, manifest_bytes = _metadata(identity, manifest)
    (staging / "identity.json").write_bytes(identity_bytes)
    (staging / "manifest.json").write_bytes(manifest_bytes)
    return manifest


def prepare(args: argparse.Namespace) -> str:
    root = args.artifact_root.resolve()
    report = Path(os.path.abspath(args.report))
    if not report.is_relative_to(root) or not report.resolve().is_relative_to(root) or report.is_symlink():
        raise ValueError("retry report must be an owned file inside the artifact root")
    result = ci_retry_report.analyze(report, step_outcome=args.step_outcome)
    summary = ci_retry_report.render(result, args.label, args.step_outcome, os.environ.get("GITHUB_RUN_ATTEMPT"))
    encoded = summary.encode("utf-8")
    if len(encoded) > SUMMARY_BYTES:
        summary = encoded[:SUMMARY_BYTES].decode("utf-8", errors="ignore") + "\nSummary truncated; inspect retained diagnostics.\n"
    warning = ci_retry_report.annotation(result, args.label)
    if warning:
        print(warning)
    _append(args.summary_file, summary)
    if result["status"] != "no-retries":
        manifest = _stage(args, result)
        _append(args.summary_file, (
            f"\nDiagnostic staging: {manifest['staging_status']}; "
            f"retention complete: {str(manifest['retention_complete']).lower()}. "
            "The manifest lists retained files and omissions. "
            "This packet does not add an initial-attempt trace recorder.\n"
        ))
    return result["status"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("report", "artifact-root", "staging", "github-output", "summary-file"):
        parser.add_argument(f"--{flag}", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--step-outcome", choices=("success", "failure"), required=True)
    parser.add_argument("--mode", choices=("compare", "generate"), required=True)
    args = parser.parse_args(argv)
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    status, exit_code = "unavailable", 0
    try:
        status = prepare(args)
    except Exception as exc:  # Workflow diagnostics must not replace the visual verdict.
        exit_code = 1
        message = f"Visual retry diagnostics unavailable: {type(exc).__name__}: {exc}"
        print(ci_retry_report.annotation({"status": "unavailable", "reason": "diagnostic-error"}, args.label))
        print(message)
        try:
            _append(args.summary_file, f"\n{message}\n{ci_retry_report.NOT_ZERO}\n")
        except OSError:
            pass
    try:
        _append(args.github_output, f"report_status={status}\nupload_needed={str(status != 'no-retries').lower()}\n")
    except OSError as exc:
        print(f"Could not publish diagnostic machine outputs: {exc}")
        return 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
