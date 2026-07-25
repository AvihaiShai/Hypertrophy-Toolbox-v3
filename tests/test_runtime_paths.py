"""Contracts for the centralized runtime-path resolver (Packet B1)."""
from __future__ import annotations

import ast
import importlib
import sys
from pathlib import Path

import pytest

from utils import runtime_paths

NEW_PATH_HELPER = "runtime_database_path"


@pytest.fixture
def clean_environment(monkeypatch):
    """A process that inherits neither an override nor a frozen marker."""
    monkeypatch.delenv(runtime_paths.RUNTIME_ROOT_ENV, raising=False)
    monkeypatch.delattr(sys, "frozen", raising=False)
    return monkeypatch


def _freeze(monkeypatch):
    monkeypatch.setattr(sys, "frozen", True, raising=False)


class TestPrecedence:
    def test_source_checkout_resolves_to_the_repository(self, clean_environment):
        repository = Path(__file__).resolve().parents[1]

        assert not runtime_paths.is_frozen()
        assert runtime_paths.runtime_root() == repository
        assert runtime_paths.runtime_data_dir() == repository / "data"
        assert runtime_paths.logs_dir() == repository / "logs"

    def test_override_relocates_the_whole_runtime_tree(
        self, clean_environment, tmp_path
    ):
        root = tmp_path / "portable"
        clean_environment.setenv(runtime_paths.RUNTIME_ROOT_ENV, str(root))

        assert runtime_paths.runtime_root() == root.resolve()
        assert runtime_paths.runtime_data_dir() == root.resolve() / "data"
        assert runtime_paths.logs_dir() == root.resolve() / "logs"

    def test_override_wins_over_the_frozen_user_data_directory(
        self, clean_environment, tmp_path
    ):
        _freeze(clean_environment)
        root = tmp_path / "usb"
        clean_environment.setenv(runtime_paths.RUNTIME_ROOT_ENV, str(root))

        assert runtime_paths.runtime_root() == root.resolve()

    def test_frozen_build_resolves_to_a_per_user_directory(
        self, clean_environment
    ):
        _freeze(clean_environment)

        root = runtime_paths.runtime_root()

        assert root == runtime_paths.user_data_root()
        assert root != runtime_paths.installation_root()
        assert runtime_paths.logs_dir() == root / "logs"

    def test_override_expands_a_home_relative_path(
        self, clean_environment
    ):
        clean_environment.setenv(runtime_paths.RUNTIME_ROOT_ENV, "~/ht-runtime")

        assert runtime_paths.runtime_root() == (
            Path.home() / "ht-runtime"
        ).resolve()

    @pytest.mark.parametrize(
        "name", ["with spaces", "ünïcodé", "with spaces and ünïcodé"]
    )
    def test_awkward_path_characters_survive(
        self, clean_environment, tmp_path, name
    ):
        root = tmp_path / name
        clean_environment.setenv(runtime_paths.RUNTIME_ROOT_ENV, str(root))

        resolved = runtime_paths.runtime_data_dir()
        runtime_paths.ensure_directory(resolved)

        assert resolved == root.resolve() / "data"
        assert resolved.is_dir()


class TestUserDataRoot:
    def test_windows_prefers_local_over_roaming(self, clean_environment):
        """A SQLite database must not be synchronized by a roaming profile."""
        clean_environment.setattr(sys, "platform", "win32")
        clean_environment.setenv("LOCALAPPDATA", r"C:\Users\test\AppData\Local")
        clean_environment.setenv("APPDATA", r"C:\Users\test\AppData\Roaming")

        root = runtime_paths.user_data_root()

        assert root == Path(r"C:\Users\test\AppData\Local") / "HypertrophyToolbox"

    def test_windows_falls_back_to_roaming_then_home(self, clean_environment):
        clean_environment.setattr(sys, "platform", "win32")
        clean_environment.delenv("LOCALAPPDATA", raising=False)
        clean_environment.setenv("APPDATA", r"C:\Users\test\AppData\Roaming")

        assert runtime_paths.user_data_root() == (
            Path(r"C:\Users\test\AppData\Roaming") / "HypertrophyToolbox"
        )

        clean_environment.delenv("APPDATA", raising=False)

        assert runtime_paths.user_data_root() == (
            Path.home() / "AppData" / "Local" / "HypertrophyToolbox"
        )

    def test_macos_uses_application_support(self, clean_environment):
        clean_environment.setattr(sys, "platform", "darwin")

        assert runtime_paths.user_data_root() == (
            Path.home()
            / "Library"
            / "Application Support"
            / "HypertrophyToolbox"
        )

    def test_linux_honors_xdg_then_falls_back(self, clean_environment):
        clean_environment.setattr(sys, "platform", "linux")
        clean_environment.setenv("XDG_DATA_HOME", "/tmp/xdg")

        assert runtime_paths.user_data_root() == Path(
            "/tmp/xdg"
        ) / "hypertrophy-toolbox"

        clean_environment.delenv("XDG_DATA_HOME", raising=False)

        assert runtime_paths.user_data_root() == (
            Path.home() / ".local" / "share" / "hypertrophy-toolbox"
        )


class TestPacketB1DoesNotMoveTheDatabase:
    """The sequencing constraint, as an executable contract.

    Packet B2 activates the frozen database switch atomically with legacy
    migration. If that switch lands first, an upgrading user boots onto a
    freshly seeded empty database while their real one sits at the old path.
    These tests fail the moment the switch happens early — deleting them is
    part of B2's job, not a way to make B1 pass.
    """

    def test_legacy_database_path_is_installation_relative(
        self, clean_environment
    ):
        _freeze(clean_environment)

        assert runtime_paths.legacy_database_path() == (
            runtime_paths.installation_root() / "data" / "database.db"
        )

    def test_configured_db_file_is_still_the_legacy_path_when_frozen(
        self, clean_environment
    ):
        _freeze(clean_environment)
        clean_environment.delenv("DB_FILE", raising=False)
        import utils.config

        try:
            importlib.reload(utils.config)

            assert (
                Path(utils.config.DB_FILE)
                == runtime_paths.legacy_database_path()
            )
            assert (
                Path(utils.config.DB_FILE)
                != runtime_paths.runtime_database_path()
            )
        finally:
            clean_environment.undo()
            importlib.reload(utils.config)

    def test_nothing_in_the_application_reads_the_new_database_path(self):
        """B1 computes runtime_database_path(); B2 is what wires it up.

        Parsed rather than grepped: prose about the eventual switch is exactly
        what this packet is supposed to contain.
        """
        repository = Path(__file__).resolve().parents[1]
        readers = []
        for directory in ("utils", "routes"):
            for path in (repository / directory).rglob("*.py"):
                if path.name == "runtime_paths.py":
                    continue
                tree = ast.parse(path.read_text(encoding="utf-8"))
                referenced = any(
                    (isinstance(node, ast.Name) and node.id == NEW_PATH_HELPER)
                    or (
                        isinstance(node, ast.Attribute)
                        and node.attr == NEW_PATH_HELPER
                    )
                    for node in ast.walk(tree)
                )
                if referenced:
                    readers.append(path.relative_to(repository).as_posix())

        assert readers == []


class TestEnvironmentOverride:
    def test_db_file_wins_over_every_resolved_path(
        self, clean_environment, tmp_path
    ):
        _freeze(clean_environment)
        explicit = tmp_path / "explicit" / "chosen.db"
        clean_environment.setenv("DB_FILE", str(explicit))
        clean_environment.setenv(
            runtime_paths.RUNTIME_ROOT_ENV, str(tmp_path / "ignored")
        )
        import utils.config

        try:
            importlib.reload(utils.config)

            assert utils.config.DB_FILE == str(explicit)
        finally:
            clean_environment.undo()
            importlib.reload(utils.config)


class TestEnsureDirectory:
    def test_creates_missing_parents_and_is_idempotent(self, tmp_path):
        target = tmp_path / "a" / "b" / "c"

        assert runtime_paths.ensure_directory(target) == target
        assert target.is_dir()
        assert runtime_paths.ensure_directory(target) == target

    def test_logging_creates_its_own_directory(
        self, clean_environment, tmp_path
    ):
        """A frozen install must not need write access to its own directory."""
        root = tmp_path / "runtime"
        clean_environment.setenv(runtime_paths.RUNTIME_ROOT_ENV, str(root))

        assert not root.exists()
        runtime_paths.ensure_directory(runtime_paths.logs_dir())

        assert (root.resolve() / "logs").is_dir()


class TestDatabaseDirectoryCreation:
    def test_connecting_creates_a_missing_parent_directory(self, tmp_path):
        """Import-time creation used to guarantee this; connection time does now."""
        import utils.config
        from utils.database import get_db_connection

        target = tmp_path / "absent" / "nested" / "database.db"
        original = utils.config.DB_FILE
        utils.config.DB_FILE = str(target)
        try:
            connection = get_db_connection()
            connection.close()
        finally:
            utils.config.DB_FILE = original

        assert target.is_file()


def test_config_paths_delegate_to_the_resolver():
    """One policy, not three modules that happen to agree."""
    import utils.config

    assert Path(utils.config.DATA_DIR) == runtime_paths.legacy_data_dir()
    assert Path(utils.config.LOGS_DIR) == runtime_paths.logs_dir()
    assert Path(utils.config.BASE_DIR) == runtime_paths.installation_root()


def test_dead_data_dir_constant_is_gone():
    """utils/database.py recomputed a second, staler notion of the data dir."""
    import utils.database

    assert not hasattr(utils.database, "DATA_DIR")
