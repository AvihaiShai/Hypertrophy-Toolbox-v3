import os

from utils.runtime_paths import (
    installation_root,
    logs_dir,
    runtime_data_dir,
    runtime_database_path,
)

# Paths
# BASE_DIR is the installation root: the repository in a checkout, the bundle in
# a frozen build. utils/runtime_paths.py owns every path derived from it.
BASE_DIR = str(installation_root())
DATA_DIR = str(runtime_data_dir())  # Database and backups; per-user when frozen
LOGS_DIR = str(logs_dir())  # Per-user writable when frozen, repository-local otherwise

# Database File
# Resolved, not installation-relative: a frozen install writes to the per-user
# data directory, so an application update cannot overwrite user data and a
# read-only installation directory still works. utils/runtime_migration.py moves
# an existing database here on the first startup that needs it.
DB_FILE = os.getenv("DB_FILE", str(runtime_database_path()))  # Allow override via environment variable

# Application Constants
APP_TITLE = "Workout Tracker"

# Server port. Both packaged launch paths honour this — the bootloader through
# app_launcher.py and the payload through app.py's __main__ — so an automated
# smoke can serve on a port it has confirmed is free instead of colliding with
# whatever already owns 5000. Invalid or out-of-range values fall back to the
# default rather than crashing a user's launcher.
DEFAULT_PORT = 5000


def runtime_port() -> int:
    """Resolve the port to serve on from ``HT_PORT``, defaulting to 5000."""
    raw = os.getenv("HT_PORT")
    if not raw:
        return DEFAULT_PORT
    try:
        port = int(raw)
    except ValueError:
        return DEFAULT_PORT
    return port if 1 <= port <= 65535 else DEFAULT_PORT

# Export Configuration
# Maximum rows per export to prevent memory issues
MAX_EXPORT_ROWS = int(os.getenv("MAX_EXPORT_ROWS", 1000000))

# Batch size for processing large datasets
EXPORT_BATCH_SIZE = int(os.getenv("EXPORT_BATCH_SIZE", 10000))

# Maximum filename length for exports
MAX_FILENAME_LENGTH = 200

# Streaming threshold - exports larger than this will use streaming (bytes)
STREAMING_THRESHOLD = 5 * 1024 * 1024  # 5MB

# Directories are NOT created here. Importing a configuration module should not
# touch the filesystem: it ran during test collection and in any script that
# imported utils, creating stray data/ and logs/ trees. Each consumer creates
# what it needs via runtime_paths.ensure_directory().
