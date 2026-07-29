"""Repository-wide contracts for the minimum supported Python runtime."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from utils.python_version import MIN_PYTHON, MIN_PYTHON_TEXT, require_supported_python


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_current_interpreter_meets_project_minimum():
    assert sys.version_info[:3] >= MIN_PYTHON


def test_runtime_guard_rejects_older_patch_release():
    with pytest.raises(RuntimeError, match=r"requires Python 3\.14\.6 or newer"):
        require_supported_python((3, 14, 5))


@pytest.mark.parametrize("version", [(3, 14, 6), (3, 14, 7), (3, 15, 0)])
def test_runtime_guard_accepts_minimum_and_newer(version):
    require_supported_python(version)


def test_python_version_file_matches_runtime_contract():
    configured = (REPO_ROOT / ".python-version").read_text(encoding="utf-8").strip()
    assert configured == MIN_PYTHON_TEXT


def test_pyright_targets_the_supported_minor_version():
    config = json.loads(
        (REPO_ROOT / "pyrightconfig.json").read_text(encoding="utf-8")
    )
    assert config["pythonVersion"] == ".".join(MIN_PYTHON_TEXT.split(".")[:2])


def test_pyright_excludes_generated_and_environment_roots():
    config = json.loads(
        (REPO_ROOT / "pyrightconfig.json").read_text(encoding="utf-8")
    )
    assert {"artifacts/**", "build/**", "dist/**", "venv/**"} <= set(
        config["exclude"]
    )


@pytest.mark.parametrize(
    "workflow",
    [".github/workflows/ci.yml", ".github/workflows/deep-gate.yml"],
)
def test_github_workflows_use_the_canonical_version_file(workflow):
    source = (REPO_ROOT / workflow).read_text(encoding="utf-8")
    assert "python-version-file: '.python-version'" in source
    # Forbid the inline key outright, not just the 3.11 literal it used to hold:
    # a reintroduced `python-version: '3.12'` would otherwise sail through. The
    # `python-version-file:` key does not contain this substring.
    assert "python-version:" not in source


def test_flake8_excludes_generated_roots_from_every_scan():
    source = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    exclusions = (
        ".venv,venv,env,.git,__pycache__,node_modules,artifacts,build,dist"
    )
    assert source.count(exclusions) == 3


@pytest.mark.parametrize("batch_file", ["START.bat", "build_exe.bat"])
def test_windows_entrypoints_select_canonical_python_and_check_venv(batch_file):
    source = (REPO_ROOT / batch_file).read_text(encoding="utf-8")
    assert source.count("-m utils.python_version") == 2
    assert "set /p PYTHON_VERSION=<.python-version" in source
    assert 'set "PYTHON_CMD=py -%PYTHON_TAG%"' in source
    assert "%PYTHON_CMD% -m venv venv" in source
