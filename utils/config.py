import os

from utils.runtime_paths import (
    legacy_data_dir,
    legacy_database_path,
    logs_dir,
)

# Paths
# BASE_DIR is the installation root: the repository in a checkout, the bundle in
# a frozen build. utils/runtime_paths.py owns every path derived from it.
BASE_DIR = str(legacy_data_dir().parent)
DATA_DIR = str(legacy_data_dir())  # Database and backups (Packet B2 moves these)
LOGS_DIR = str(logs_dir())  # Per-user writable when frozen, repository-local otherwise

# Database File
# Still installation-relative on purpose. Packet B2 repoints this to
# runtime_paths.runtime_database_path() atomically with legacy migration; doing
# it earlier would seed an empty database over an upgrading user's real data.
DB_FILE = os.getenv("DB_FILE", str(legacy_database_path()))  # Allow override via environment variable

# Application Constants
APP_TITLE = "Workout Tracker"

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
