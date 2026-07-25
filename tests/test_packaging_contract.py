"""Source-level contracts for the canonical PyInstaller definition."""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
APPROVED_DATA_FILES = {
    ("data/catalog.seed.db", "data"),
    ("data/free_exercise_db_mapping.csv", "data"),
}
REQUIRED_ASSETS = {
    "templates/base.html",
    "templates/welcome.html",
    "static/css/bootstrap.custom.min.css",
    "static/css/base.css",
    "static/images/favicon.ico",
    "static/js/modules/fetch-wrapper.js",
    "static/vendor/free-exercise-db/exercises.json",
}


def _assignment_literal(source: str, variable: str):
    module = ast.parse(source)
    for statement in module.body:
        if not isinstance(statement, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == variable
            for target in statement.targets
        ):
            return ast.literal_eval(statement.value)
    raise AssertionError(f"Missing literal assignment: {variable}")


def test_spec_data_allowlist_is_exact_and_non_recursive():
    spec_path = REPO_ROOT / "Hypertrophy-Toolbox.spec"
    source = spec_path.read_text(encoding="utf-8")
    approved = {
        tuple(entry)
        for entry in _assignment_literal(source, "approved_data_files")
    }

    assert approved == APPROVED_DATA_FILES
    assert "('data', 'data')" not in source
    assert "excluded_subtree='bodymaps/GPT/'" in source


def test_batch_file_uses_only_the_committed_spec():
    source = (REPO_ROOT / "build_exe.bat").read_text(encoding="utf-8")
    lowered = source.lower()

    command = "pyinstaller.exe --clean --noconfirm hypertrophy-toolbox.spec"
    assert command in lowered
    assert "--add-data" not in lowered
    assert "del /q \"hypertrophy-toolbox.spec\"" not in lowered
    assert "scripts\\guard_package_assets.py" in lowered


def test_reviewed_runtime_assets_remain_tracked():
    tracked = {
        line.replace("\\", "/")
        for line in subprocess.run(
            ["git", "ls-files", "--", "static", "templates"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    }

    assert REQUIRED_ASSETS <= tracked


def test_visual_seeder_fallback_targets_catalog_seed():
    source = (
        REPO_ROOT / "e2e" / "scripts" / "prepare_visual_db.py"
    ).read_text(encoding="utf-8")

    assert 'REPO_ROOT / "data" / "catalog.seed.db"' in source
    assert 'LIVE_DB = REPO_ROOT / "data" / "database.db"' in source
    assert 'AUTO_BACKUP_DIR = REPO_ROOT / "data" / "auto_backup"' in source
