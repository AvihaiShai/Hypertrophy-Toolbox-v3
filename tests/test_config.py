"""
Tests for utils/config.py - Application configuration.
"""

import os
from runpy import run_path

import pytest

import utils.config


@pytest.fixture
def scratch_config_runtime(tmp_path, monkeypatch):
    runtime_root = tmp_path.resolve() / "runtime"
    monkeypatch.setenv("HT_RUNTIME_DIR", str(runtime_root))
    monkeypatch.setenv("DB_FILE", str(runtime_root / "data" / "database.db"))
    return runtime_root


def _read_config():
    """Execute the config source in a fresh namespace."""
    config_file = utils.config.__file__
    assert config_file is not None
    return run_path(config_file)


class TestConfigPaths:
    """Tests for configuration path constants."""

    def test_base_dir_is_absolute(self):
        """BASE_DIR should be an absolute path."""
        from utils.config import BASE_DIR
        assert os.path.isabs(BASE_DIR)

    def test_base_dir_exists(self):
        """BASE_DIR should point to existing directory."""
        from utils.config import BASE_DIR
        assert os.path.exists(BASE_DIR)

    def test_data_dir_under_base(self):
        """DATA_DIR should be under BASE_DIR."""
        from utils.config import BASE_DIR, DATA_DIR
        assert DATA_DIR.startswith(BASE_DIR)
        assert DATA_DIR.endswith("data")

    def test_logs_dir_under_base(self):
        """LOGS_DIR should be under BASE_DIR."""
        from utils.config import BASE_DIR, LOGS_DIR
        assert LOGS_DIR.startswith(BASE_DIR)
        assert LOGS_DIR.endswith("logs")

    def test_importing_config_creates_no_directories(self, scratch_config_runtime):
        """Importing configuration must not touch the filesystem.

        It used to create data/ and logs/ under whatever directory resolved at
        import, including during test collection and in unrelated scripts.
        Consumers create what they need, where they need it.
        """
        runtime_root = scratch_config_runtime
        data_dir = runtime_root / "data"
        database_path = data_dir / "database.db"

        config = _read_config()

        assert config["DATA_DIR"] == str(data_dir)
        assert config["LOGS_DIR"] == str(runtime_root / "logs")
        assert config["DB_FILE"] == str(database_path)
        assert not runtime_root.exists()


class TestDbFile:
    """Tests for DB_FILE configuration."""

    def test_db_file_has_default(self):
        """DB_FILE should have a default value."""
        from utils.config import DB_FILE
        assert DB_FILE is not None
        assert DB_FILE.endswith("database.db")

    def test_db_file_in_data_dir(self):
        """Default DB_FILE should be in DATA_DIR."""
        from utils.config import DB_FILE, DATA_DIR
        assert os.path.dirname(DB_FILE) == DATA_DIR

    def test_db_file_env_override(self, tmp_path, monkeypatch):
        """DB_FILE should be overridable via environment variable."""
        runtime_root = tmp_path / "runtime"
        database_path = tmp_path / "custom" / "test.db"
        monkeypatch.setenv("HT_RUNTIME_DIR", str(runtime_root))
        monkeypatch.setenv("DB_FILE", str(database_path))

        config = _read_config()

        assert config["DB_FILE"] == str(database_path)
        assert not runtime_root.exists()
        assert not database_path.parent.exists()


class TestAppConstants:
    """Tests for application constants."""

    def test_app_title_defined(self):
        """APP_TITLE should be defined."""
        from utils.config import APP_TITLE
        assert APP_TITLE == "Workout Tracker"

    def test_app_title_is_string(self):
        """APP_TITLE should be a string."""
        from utils.config import APP_TITLE
        assert isinstance(APP_TITLE, str)


class TestExportConfiguration:
    """Tests for export configuration constants."""

    def test_max_export_rows_default(self):
        """MAX_EXPORT_ROWS should have reasonable default."""
        from utils.config import MAX_EXPORT_ROWS
        assert MAX_EXPORT_ROWS == 1000000

    def test_max_export_rows_is_int(self):
        """MAX_EXPORT_ROWS should be an integer."""
        from utils.config import MAX_EXPORT_ROWS
        assert isinstance(MAX_EXPORT_ROWS, int)

    def test_export_batch_size_default(self):
        """EXPORT_BATCH_SIZE should have reasonable default."""
        from utils.config import EXPORT_BATCH_SIZE
        assert EXPORT_BATCH_SIZE == 10000

    def test_export_batch_size_is_int(self):
        """EXPORT_BATCH_SIZE should be an integer."""
        from utils.config import EXPORT_BATCH_SIZE
        assert isinstance(EXPORT_BATCH_SIZE, int)

    def test_max_filename_length_defined(self):
        """MAX_FILENAME_LENGTH should be defined."""
        from utils.config import MAX_FILENAME_LENGTH
        assert MAX_FILENAME_LENGTH == 200

    def test_streaming_threshold_defined(self):
        """STREAMING_THRESHOLD should be 5MB."""
        from utils.config import STREAMING_THRESHOLD
        assert STREAMING_THRESHOLD == 5 * 1024 * 1024

    @pytest.mark.usefixtures("scratch_config_runtime")
    def test_max_export_rows_env_override(self, monkeypatch):
        """MAX_EXPORT_ROWS should be overridable via environment."""
        monkeypatch.setenv("MAX_EXPORT_ROWS", "500000")
        assert _read_config()["MAX_EXPORT_ROWS"] == 500000

    @pytest.mark.usefixtures("scratch_config_runtime")
    def test_export_batch_size_env_override(self, monkeypatch):
        """EXPORT_BATCH_SIZE should be overridable via environment."""
        monkeypatch.setenv("EXPORT_BATCH_SIZE", "5000")
        assert _read_config()["EXPORT_BATCH_SIZE"] == 5000


class TestDirectoryCreation:
    """Tests for automatic directory creation."""

    def test_data_dir_is_directory(self):
        """DATA_DIR should be a directory."""
        from utils.config import DATA_DIR
        assert os.path.isdir(DATA_DIR)

    def test_logs_dir_is_directory(self):
        """LOGS_DIR should be a directory."""
        from utils.config import LOGS_DIR
        assert os.path.isdir(LOGS_DIR)
