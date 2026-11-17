"""Bounded retention uses sanitized reporter fixtures, not a browser failure."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import zipfile
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import prepare_visual_retry_artifact as diagnostics

FIXTURES = Path(__file__).resolve().parent / "fixtures/ci_retry_report"
REAL_IDENTITY = diagnostics._identity


def report_data(statuses=("passed",), outcome="expected"):
    data = json.loads((FIXTURES / "clean.json").read_text(encoding="utf-8"))
    suite = data["suites"][0]
    spec = suite["specs"][0]
    test = spec["tests"][0]
    sample = test["results"][0]
    test["results"] = [
        {**copy.deepcopy(sample), "status": status, "retry": retry, "duration": 25 + retry}
        for retry, status in enumerate(statuses)
    ]
    test["status"] = outcome
    spec["tests"] = [test]
    suite["specs"] = [spec]
    suite["suites"] = []
    data["suites"] = [suite]
    data["stats"].update({key: int(key == outcome) for key in ("expected", "unexpected", "flaky", "skipped")})
    return data


@pytest.fixture
def packet(tmp_path, monkeypatch):
    root = tmp_path / "playwright"
    root.mkdir()
    (root / "junit.xml").write_text("<testsuites/>", encoding="utf-8")
    summary = tmp_path / "summary"
    summary.write_text("Earlier summary remains.\n", encoding="utf-8")
    paths = {
        "report": root / "results.json", "artifact-root": root,
        "staging": tmp_path / "retained", "github-output": tmp_path / "output",
        "summary-file": summary,
    }
    monkeypatch.setattr(diagnostics, "_identity", lambda args, result: {
        "checkout_sha": "1" * 40, "application_base": None, "mode": args.mode,
        "test_step_outcome": args.step_outcome,
    })
    return paths


def invoke(packet, data=None, *, step_outcome="success", mode="compare"):
    if data is not None:
        packet["report"].write_text(json.dumps(data), encoding="utf-8")
    argv = [part for name, path in packet.items() for part in (f"--{name}", str(path))]
    return diagnostics.main(argv + [
        "--label", "Linux visuals", "--step-outcome", step_outcome, "--mode", mode,
    ])


def outputs(packet):
    return dict(line.split("=", 1) for line in packet["github-output"].read_text(encoding="utf-8").splitlines())


def manifest(packet):
    return json.loads((packet["staging"] / "manifest.json").read_text(encoding="utf-8"))


def test_clean_run_emits_validated_no_retry_without_staging(packet):
    assert invoke(packet, report_data()) == 0
    assert outputs(packet) == {"report_status": "no-retries", "upload_needed": "false"}
    assert not packet["staging"].exists()
    summary = packet["summary-file"].read_text(encoding="utf-8")
    assert summary.startswith("Earlier summary remains.\n")
    assert "Status:** no retries" in summary
    assert "unavailable" not in summary


def test_default_staged_payload_budget_matches_owner_approved_limit():
    assert diagnostics.MAX_BYTES == 50 * 1024 * 1024
    assert 0 < diagnostics.METADATA_BYTES < diagnostics.MAX_BYTES


@pytest.mark.parametrize("statuses,outcome,step_outcome", [
    (("failed", "passed"), "flaky", "success"),
    (("timedOut", "passed"), "flaky", "success"),
    (("failed", "failed", "passed"), "flaky", "success"),
    (("failed", "failed", "failed"), "unexpected", "failure"),
])
def test_retry_history_preserves_original_attempt_and_later_retries(packet, statuses, outcome, step_outcome):
    assert invoke(packet, report_data(statuses, outcome), step_outcome=step_outcome) == 0
    assert outputs(packet) == {"report_status": "retries", "upload_needed": "true"}
    kept = manifest(packet)
    attempts = kept["tests"][0]["attempts"]
    assert [(attempt["retry"], attempt["status"]) for attempt in attempts] == list(enumerate(statuses))
    assert kept["tests"][0]["expected_status"] == "passed"
    assert (packet["staging"] / "results.json").read_bytes() == packet["report"].read_bytes()
    assert kept["retention_complete"] is True
    assert kept["unavailable_capture_types"] == [".md", ".png", ".zip"]
    assert not (packet["staging"] / "test-results").exists()
    assert "does not add an initial-attempt trace recorder" in packet["summary-file"].read_text(encoding="utf-8")


def test_unexpected_first_attempt_alone_is_not_a_retry(packet):
    assert invoke(packet, report_data(("failed",), "unexpected"), step_outcome="failure") == 0
    assert outputs(packet) == {"report_status": "no-retries", "upload_needed": "false"}


@pytest.mark.parametrize("problem", ["missing", "invalid-utf8", "malformed", "unsupported", "partial", "inconsistent"])
def test_unreadable_or_untrusted_report_is_never_zero_retries(packet, problem, capsys):
    data = report_data()
    if problem == "invalid-utf8":
        packet["report"].write_bytes(b"\xff\xfe")
    elif problem == "malformed":
        packet["report"].write_text("{", encoding="utf-8")
    elif problem == "unsupported":
        data["config"]["version"] = "999.0.0"
    elif problem == "partial":
        data["errors"] = [{"message": "worker stopped before reporting all tests"}]
    elif problem == "inconsistent":
        data["stats"]["flaky"] = 1
    data = None if problem in ("missing", "invalid-utf8", "malformed") else data
    assert invoke(packet, data) == 0
    assert outputs(packet) == {"report_status": "unavailable", "upload_needed": "true"}
    kept = manifest(packet)
    assert kept["report_status"] == "unavailable"
    assert kept["retention_complete"] is False
    assert "not a report of zero retries" in packet["summary-file"].read_text(encoding="utf-8")
    assert "unavailable" in capsys.readouterr().out


def test_step_report_disagreement_retains_evidence_as_unavailable(packet):
    assert invoke(packet, report_data(), step_outcome="failure") == 0
    assert outputs(packet)["report_status"] == "unavailable"
    assert manifest(packet)["report_reason"] == "inconsistent"


@pytest.mark.parametrize("mode", ["compare", "generate"])
def test_existing_diagnostics_keep_bytes_paths_hashes_and_all_retry_numbers(packet, mode):
    files = {
        "test-results/original/error-context.md": b"original failed context",
        "test-results/original/test-failed-1.png": b"\x89PNG\r\n\x1a\nfixture",
        "test-results/retry2/trace.zip": None,
        "test-results/retry1/video.webm": b"excluded retry video",
        "test-results/retry2/report.html": b"excluded HTML",
    }
    for relative, content in files.items():
        target = packet["artifact-root"] / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if content is None:
            with zipfile.ZipFile(target, "w") as archive:
                archive.writestr("trace.trace", "fixture trace record\n")
        else:
            target.write_bytes(content)
    # HTML data must not be pulled in just because a report directory exists.
    (packet["artifact-root"] / "report").mkdir()
    (packet["artifact-root"] / "report/index.html").write_text("HTML", encoding="utf-8")
    assert invoke(packet, report_data(("failed", "failed", "passed"), "flaky"), mode=mode) == 0
    kept = manifest(packet)
    by_path = {entry["path"]: entry for entry in kept["files"]}
    for relative in list(files)[:3]:
        original = (packet["artifact-root"] / relative).read_bytes()
        assert (packet["staging"] / relative).read_bytes() == original
        assert by_path[relative]["sha256"] == hashlib.sha256(original).hexdigest()
        assert by_path[relative]["disposition"] == "retained"
    for relative in list(files)[3:]:
        assert not (packet["staging"] / relative).exists()
        assert by_path[relative]["disposition"] == "excluded-type"
    assert not (packet["staging"] / "report").exists()
    assert kept["unavailable_capture_types"] == []
    assert kept["retention_complete"] is True


def test_payload_and_metadata_together_obey_cap_with_explicit_large_file_omission(packet, monkeypatch):
    monkeypatch.setattr(diagnostics, "MAX_BYTES", 64 * 1024)
    monkeypatch.setattr(diagnostics, "METADATA_BYTES", 16 * 1024)
    image = packet["artifact-root"] / "test-results/original/large.png"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"x" * (64 * 1024))
    assert invoke(packet, report_data(("failed", "passed"), "flaky")) == 0
    kept = manifest(packet)
    entry = next(row for row in kept["files"] if row["path"].endswith("large.png"))
    assert entry["disposition"] == "payload-budget"
    assert entry["size_bytes"] == 64 * 1024
    assert not (packet["staging"] / entry["path"]).exists()
    assert kept["retention_complete"] is False
    actual_size = sum(path.stat().st_size for path in packet["staging"].rglob("*") if path.is_file())
    assert actual_size <= 64 * 1024
    assert (packet["staging"] / "results.json").read_bytes() == packet["report"].read_bytes()


def test_oversized_core_json_is_hashed_and_omitted_without_invalid_truncation(packet, monkeypatch):
    monkeypatch.setattr(diagnostics, "MAX_BYTES", 32 * 1024)
    monkeypatch.setattr(diagnostics, "METADATA_BYTES", 8 * 1024)
    data = report_data(("failed", "passed"), "flaky")
    data["extra_capture"] = "x" * (32 * 1024)
    assert invoke(packet, data) == 0
    kept = manifest(packet)
    entry = next(row for row in kept["files"] if row["path"] == "results.json")
    assert entry["disposition"] == "payload-budget"
    assert entry["sha256"] == hashlib.sha256(packet["report"].read_bytes()).hexdigest()
    assert not (packet["staging"] / "results.json").exists()
    assert kept["retention_complete"] is False


def test_manifest_overflow_is_explicit_and_still_bounded(packet, monkeypatch):
    monkeypatch.setattr(diagnostics, "MAX_BYTES", 64 * 1024)
    monkeypatch.setattr(diagnostics, "METADATA_BYTES", 4 * 1024)
    results = packet["artifact-root"] / "test-results"
    results.mkdir()
    for index in range(50):
        (results / f"context-{index:03}.md").write_text("small context", encoding="utf-8")
    assert invoke(packet, report_data(("failed", "passed"), "flaky")) == 0
    kept = manifest(packet)
    assert kept["files_count"] == 52
    assert kept["files_complete"] is False
    assert len(kept["files"]) < kept["files_count"]
    assert len(kept["files_sha256"]) == 64
    assert kept["retention_complete"] is False
    assert sum((packet["staging"] / name).stat().st_size for name in ("identity.json", "manifest.json")) <= 4 * 1024


def test_missing_junit_is_explicit_without_discarding_available_json(packet):
    (packet["artifact-root"] / "junit.xml").unlink()
    assert invoke(packet, report_data(("failed", "passed"), "flaky")) == 0
    entry = next(row for row in manifest(packet)["files"] if row["path"] == "junit.xml")
    assert entry["disposition"] == "missing"
    assert manifest(packet)["retention_complete"] is False


@pytest.mark.parametrize("suffix", [".png", ".md"])
def test_declared_missing_original_diagnostic_cannot_be_masked_by_an_unrelated_file(packet, suffix):
    results = packet["artifact-root"] / "test-results"
    results.mkdir()
    (results / f"b{suffix}").write_bytes(b"unrelated diagnostic")
    missing = results / f"a{suffix}"
    data = report_data(("failed", "passed"), "flaky")
    original = data["suites"][0]["specs"][0]["tests"][0]["results"][0]
    original["errors"] = [{"message": "decode timed out\nstack detail"}]
    original["attachments"] = [{"name": "original failure", "contentType": "image/png" if suffix == ".png" else "text/markdown", "path": str(missing)}]
    assert invoke(packet, data) == 0
    kept = manifest(packet)
    assert outputs(packet)["report_status"] == "retries"
    attempt = kept["tests"][0]["attempts"][0]
    assert attempt["retry"] == 0 and attempt["status"] == "failed"
    assert attempt["errors"] == ["decode timed out"]
    assert attempt["attachments"][0] == {
        "name": "original failure", "content_type": original["attachments"][0]["contentType"],
        "declared_path": str(missing), "path": f"test-results/a{suffix}",
        "artifact_path": None, "disposition": "missing",
    }
    files = {entry["path"]: entry for entry in kept["files"]}
    assert files[f"test-results/a{suffix}"]["disposition"] == "missing"
    assert files[f"test-results/b{suffix}"]["disposition"] == "retained"
    assert suffix not in kept["unavailable_capture_types"]
    assert kept["retention_complete"] is False


@pytest.mark.parametrize("disposition", ["retained", "outside-root-or-link", "payload-budget"])
def test_declared_attempt_attachment_keeps_its_actual_copy_disposition(packet, tmp_path, monkeypatch, disposition):
    results = packet["artifact-root"] / "test-results"
    results.mkdir()
    path = results / "a.png"
    content = b"original failure screenshot"
    if disposition == "outside-root-or-link":
        path = tmp_path / "outside.png"
    elif disposition == "payload-budget":
        monkeypatch.setattr(diagnostics, "MAX_BYTES", 32 * 1024)
        monkeypatch.setattr(diagnostics, "METADATA_BYTES", 8 * 1024)
        content = b"x" * (32 * 1024)
    path.write_bytes(content)
    data = report_data(("failed", "passed"), "flaky")
    data["suites"][0]["specs"][0]["tests"][0]["results"][0]["attachments"] = [
        {"name": "failure", "contentType": "image/png", "path": str(path)},
    ]
    assert invoke(packet, data) == 0
    kept = manifest(packet)
    attachment = kept["tests"][0]["attempts"][0]["attachments"][0]
    assert attachment["declared_path"] == str(path)
    assert attachment["disposition"] == disposition
    assert kept["retention_complete"] is (disposition == "retained")
    if disposition == "retained":
        assert attachment["artifact_path"] == "test-results/a.png"
        assert attachment["sha256"] == hashlib.sha256(content).hexdigest()
        assert (packet["staging"] / attachment["artifact_path"]).read_bytes() == content
    else:
        assert attachment["artifact_path"] is None


def test_report_outside_owned_tree_is_not_read_or_copied(packet, tmp_path, capsys):
    outside = tmp_path / "outside.json"
    outside.write_text(json.dumps(report_data(("failed", "passed"), "flaky")), encoding="utf-8")
    packet["report"] = outside
    assert invoke(packet) == 1
    assert outputs(packet) == {"report_status": "unavailable", "upload_needed": "true"}
    assert not packet["staging"].exists()
    assert "owned file inside the artifact root" in capsys.readouterr().out


def test_symlinked_file_and_directory_cannot_copy_outside_content(packet, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "private.txt").write_text("must not be copied", encoding="utf-8")
    results = packet["artifact-root"] / "test-results"
    results.mkdir()
    try:
        (results / "private.txt").symlink_to(outside / "private.txt")
        (results / "linked-directory").symlink_to(outside, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"host cannot create test symlinks: {exc}")
    assert invoke(packet, report_data(("failed", "passed"), "flaky")) == 0
    for relative in ("test-results/private.txt", "test-results/linked-directory"):
        entry = next(row for row in manifest(packet)["files"] if row["path"] == relative)
        assert entry["disposition"] == "outside-root-or-link"
        assert not (packet["staging"] / relative).exists()


def test_lexical_parent_segments_do_not_escape_the_staging_tree(packet):
    packet["report"] = packet["artifact-root"] / ".." / "playwright/results.json"
    assert invoke(packet, report_data(("failed", "passed"), "flaky")) == 0
    assert (packet["staging"] / "results.json").is_file()
    assert all(".." not in Path(row["path"]).parts for row in manifest(packet)["files"])


def test_failed_summary_write_is_unavailable_not_false_clean(packet, tmp_path, capsys):
    packet["summary-file"] = tmp_path
    assert invoke(packet, report_data()) == 1
    assert outputs(packet)["upload_needed"] == "true"
    assert "diagnostics unavailable" in capsys.readouterr().out


def test_failed_machine_output_write_is_an_operational_failure(packet, tmp_path, capsys):
    packet["github-output"] = tmp_path
    assert invoke(packet, report_data()) == 1
    assert "Could not publish diagnostic machine outputs" in capsys.readouterr().out


def test_existing_staging_is_not_overwritten_or_mistaken_for_fresh_evidence(packet):
    packet["staging"].mkdir()
    sentinel = packet["staging"] / "old.txt"
    sentinel.write_text("old", encoding="utf-8")
    assert invoke(packet, report_data(("failed", "passed"), "flaky")) == 1
    assert outputs(packet)["report_status"] == "unavailable"
    assert sentinel.read_text(encoding="utf-8") == "old"


def test_growing_or_shrinking_source_never_leaves_a_truncated_diagnostic(tmp_path):
    source, target = tmp_path / "source", tmp_path / "staging/trace.zip"
    source.write_bytes(b"source changed")
    for expected in (2, 100):
        with pytest.raises(ValueError, match="source (grew|shrank)"):
            diagnostics._copy(source, target, expected)
        assert not target.exists()
    target.write_bytes(b"existing")
    with pytest.raises(FileExistsError):
        diagnostics._copy(source, target, len(source.read_bytes()))
    assert target.read_bytes() == b"existing"


def test_identity_uses_exact_checkout_run_attempt_and_actual_tool_bytes(tmp_path, monkeypatch):
    monkeypatch.setattr(diagnostics, "REPO_ROOT", tmp_path)
    package = tmp_path / "node_modules/playwright/package.json"
    browser = tmp_path / "node_modules/playwright-core/browsers.json"
    package.parent.mkdir(parents=True)
    browser.parent.mkdir(parents=True)
    package.write_text('{"version":"1.61.0"}', encoding="utf-8")
    browser.write_bytes(b"browser identity")
    (tmp_path / "package-lock.json").write_bytes(b"lock identity")
    monkeypatch.setattr(diagnostics.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout="2" * 40 + "\n"))
    for env, value in {
        "GITHUB_SHA": "3" * 40, "GITHUB_JOB": "visual-linux", "GITHUB_RUN_ID": "123",
        "GITHUB_RUN_ATTEMPT": "2", "GITHUB_EVENT_NAME": "schedule", "PW_VISUAL_SEED": "1",
    }.items():
        monkeypatch.setenv(env, value)
    monkeypatch.delenv("SOURCE_BASE", raising=False)
    identity = REAL_IDENTITY(Namespace(mode="compare", step_outcome="success"), {"tests": [{"file": "visual.spec.ts"}]})
    assert identity["checkout_sha"] == "2" * 40
    assert identity["event_sha"] == "3" * 40
    assert identity["application_base"] is None
    assert identity["workflow_run_attempt"] == "2"
    assert identity["job_key"] == "visual-linux"
    assert identity["playwright_version"] == "1.61.0"
    assert identity["browser_manifest_sha256"] == hashlib.sha256(b"browser identity").hexdigest()
    assert identity["package_lock_sha256"] == hashlib.sha256(b"lock identity").hexdigest()


def test_unavailable_identity_remains_absent_instead_of_inventing_a_base(tmp_path, monkeypatch):
    monkeypatch.setattr(diagnostics, "REPO_ROOT", tmp_path)
    def unavailable(*args, **kwargs):
        raise subprocess.TimeoutExpired("git", 5)
    monkeypatch.setattr(diagnostics.subprocess, "run", unavailable)
    monkeypatch.delenv("SOURCE_BASE", raising=False)
    identity = REAL_IDENTITY(Namespace(mode="generate", step_outcome="failure"), {"tests": []})
    for key in ("checkout_sha", "application_base", "playwright_version", "browser_manifest_sha256", "package_lock_sha256"):
        assert identity[key] is None
