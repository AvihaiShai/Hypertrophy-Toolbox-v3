"""
Pytest configuration and fixtures for Priority 0 security tests.
"""
import pytest
import os
import shutil
from pathlib import Path
from utils.database import DatabaseHandler
from utils.runtime_init import _reset_for_tests, init_runtime
from utils.schema_registry import run_all_initializers
import utils.config


# Override config before importing app
os.environ['TESTING'] = '1'
TEST_DB_FILENAME = "test_hypertrophy_toolbox.db"


# Hypothesis profiles (Testing Strategy D4, signed 2026-08-29; F5-3's operational
# preconditions). `ci` is the DEFAULT so a local run reproduces CI: `Run Tests` is
# a required check with no retry, and randomized generation would be the suite's
# first nondeterministic required-path failure. `database=None` keeps Hypothesis
# from writing a `.hypothesis/` directory to the repository root, which ADR-002
# forbids; with derandomize=True the example database carries no value anyway.
#
# The import is guarded because this is the ROOT conftest: an unguarded
# ImportError here would fail collection of the ENTIRE suite rather than of the
# one file that needs Hypothesis. requirements.txt pins hypothesis as a hard
# dependency, so the absent case is not a supported configuration -- the guard
# just keeps its failure proportionate. Note it does NOT keep
# `pytest --collect-only` green on its own: tests/test_effective_sets.py imports
# hypothesis directly.
try:
    from hypothesis import HealthCheck, settings as _hypothesis_settings
except ImportError:  # pragma: no cover - only when the test extra is absent
    pass
else:
    _hypothesis_settings.register_profile(
        "ci",
        derandomize=True,
        deadline=None,
        max_examples=200,
        database=None,
        suppress_health_check=[HealthCheck.too_slow],
    )
    _hypothesis_settings.register_profile(
        "dev",
        derandomize=False,
        deadline=None,
        database=None,
    )
    # An unrecognized value would raise InvalidArgument at root-conftest import
    # time -- the same whole-suite collection failure the guard above exists to
    # avoid -- so fall back rather than abort.
    _profile = os.getenv("HYPOTHESIS_PROFILE", "ci")
    if _profile not in ("ci", "dev"):
        _profile = "ci"
    _hypothesis_settings.load_profile(_profile)


def _cleanup_database_files(database_path: str) -> None:
    """Best-effort cleanup for SQLite database sidecar files."""
    candidates = [Path(database_path)]
    candidates.extend(Path(f"{database_path}{suffix}") for suffix in ("-wal", "-shm", "-journal"))
    for candidate in candidates:
        try:
            candidate.unlink(missing_ok=True)
        except OSError:
            # Some tests intentionally exercise open connections; leave best-effort cleanup non-fatal.
            pass


@pytest.fixture(scope='session')
def schema_template(tmp_path_factory):
    """Build the canonical empty schema once, to be copied per test.

    ``run_all_initializers()`` commits each DDL statement separately, and the
    pragma profile tests run under fsyncs every one of them: ``utils/database.py``
    defaults ``FLASK_DEBUG`` to ``'1'``, which selects ``journal_mode = DELETE``
    + ``synchronous = FULL``. Paid once per ``app`` fixture, that was the largest
    single cost in the suite. Copying the finished file is far cheaper.

    Two properties make the copy sound rather than merely fast, and both are
    asserted below because a silent regression in either yields a subtly empty
    schema rather than a failure:

    * ``DELETE`` journal mode leaves no ``-wal``/``-shm`` sidecar, so the whole
      database is the one file. Were the profile ever switched to WAL, copying
      the ``.db`` alone would drop everything still in the log.
    * ``get_db_connection()`` pools nothing, so the building connection is
      genuinely closed by the time this returns and no write is still buffered.

    Session-scoped on ``tmp_path_factory``, which xdist gives each worker its
    own basetemp for — so this builds once per worker and is never shared
    across processes.
    """
    template = tmp_path_factory.mktemp('schema_template') / 'template.db'
    original_db_file = utils.config.DB_FILE
    utils.config.DB_FILE = str(template)
    try:
        run_all_initializers(force_base=True)
    finally:
        utils.config.DB_FILE = original_db_file

    assert template.exists(), "schema template was not created"
    for suffix in ("-wal", "-shm", "-journal"):
        sidecar = Path(f"{template}{suffix}")
        assert not sidecar.exists(), (
            f"schema template left a {suffix} sidecar; copying the .db alone "
            "would lose part of the schema. Check the journal-mode pragma in "
            "utils/database.py::_configure_connection."
        )
    return template


@pytest.fixture(scope='module')
def real_app_client(tmp_path_factory):
    """A client for the module-level app, initialized on a seeded scratch DB.

    Each module supplies an explicit database path and resets the process
    guard before and after initialization. Both the outcome and config path
    must match scratch before yielding. Environment, config, TESTING and the
    guard are restored on teardown.

    ``HT_RUNTIME_DIR`` is set to scratch as well, but it relocates neither logs
    nor backups here: ``conftest.py``'s own imports fixed the log directory
    before this runs, and auto-backups go beside the database.
    """
    scratch_db = tmp_path_factory.mktemp('real_app') / 'database.db'
    scratch_resolved = Path(scratch_db).resolve()
    runtime_root = tmp_path_factory.mktemp('real_app_runtime')

    # None means "was not set" for the environment variable, and "never captured"
    # for TESTING — neither is a value either can legitimately hold here.
    original_env_db = os.environ.get('DB_FILE')
    original_env_runtime = os.environ.get('HT_RUNTIME_DIR')
    original_config_db = utils.config.DB_FILE
    original_testing: bool | None = None
    real_app = None

    os.environ['DB_FILE'] = str(scratch_db)
    os.environ['HT_RUNTIME_DIR'] = str(runtime_root)
    utils.config.DB_FILE = str(scratch_db)
    try:
        from app import app as real_app

        _reset_for_tests()
        outcome = init_runtime(db_file=str(scratch_db))
        for source, resolved in (
            ("init_runtime() outcome", Path(outcome.database_path).resolve()),
            ("utils.config.DB_FILE", Path(utils.config.DB_FILE).resolve()),
        ):
            if resolved != scratch_resolved:
                pytest.fail(
                    f"real_app_client refuses to run: {source} is not the fixture "
                    f"scratch database.\n  resolved: {resolved}\n  scratch:  {scratch_resolved}"
                )

        original_testing = bool(real_app.config.get('TESTING', False))
        real_app.config['TESTING'] = True

        with real_app.test_client() as client:
            yield client
    finally:
        if real_app is not None and original_testing is not None:
            real_app.config['TESTING'] = original_testing
        _reset_for_tests()
        utils.config.DB_FILE = original_config_db
        if original_env_db is None:
            os.environ.pop('DB_FILE', None)
        else:
            os.environ['DB_FILE'] = original_env_db
        if original_env_runtime is None:
            os.environ.pop('HT_RUNTIME_DIR', None)
        else:
            os.environ['HT_RUNTIME_DIR'] = original_env_runtime
        _cleanup_database_files(str(scratch_db))


@pytest.fixture
def test_db_path(tmp_path):
    """Create a unique temporary database file path per test."""
    return str(tmp_path / TEST_DB_FILENAME)


@pytest.fixture
def catalog_db_path(tmp_path):
    """Copy the shipped catalog into a test-scoped, read-only snapshot."""
    repo_root = Path(__file__).resolve().parents[1]
    source = repo_root / "data" / "catalog.seed.db"
    destination = tmp_path / "catalog.db"

    assert source.exists(), f"Shipped catalog database is missing: {source}"
    shutil.copyfile(source, destination)
    return str(destination)


@pytest.fixture
def app(test_db_path, schema_template):
    """The production ``create_app()`` application on a copy of the empty schema.

    The same factory ``app.py`` uses, so every blueprint, handler, filter, hook
    and the real ``/erase-data`` route (confirm token included) is the
    production one. ``create_app()`` does no runtime initialization, so the
    database stays the unseeded test schema: no migration, catalog seed,
    upgrade or startup backup.
    """
    # Imported here rather than at module top so collecting the suite never
    # imports app (Plan v2 D-12).
    from app import create_app

    original_db_file = utils.config.DB_FILE
    utils.config.DB_FILE = test_db_path

    app = create_app(config_overrides={"TESTING": True, "WTF_CSRF_ENABLED": False})

    # Copy the prebuilt empty schema rather than re-running every initializer.
    # Equivalent output, ~700x cheaper; see the schema_template fixture. The
    # real /erase-data route still calls the initializers itself, so that path
    # keeps asserting they work.
    shutil.copyfile(schema_template, test_db_path)

    try:
        yield app
    finally:
        utils.config.DB_FILE = original_db_file
        _cleanup_database_files(test_db_path)


@pytest.fixture
def client(app):
    """Flask test client."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def db_handler(app, test_db_path):
    """Database handler with test DB and foreign keys enabled."""
    handler = DatabaseHandler(test_db_path)

    with handler.connection:
        result = handler.fetch_one("PRAGMA foreign_keys;")
        assert result is not None, "PRAGMA foreign_keys returned no row"
        assert result['foreign_keys'] == 1, "Foreign keys must be enabled"

    yield handler

    handler.close()


@pytest.fixture
def clean_db(db_handler):
    """Clean database before each test."""
    # Delete all data but keep tables
    with db_handler.connection:
        tables = [
            'program_backup_items',
            'program_backups',
            'ignored_calibration_transfers',
            'exercise_transfer_ratios',
            'learned_strength_calibrations',
            'user_calibration_settings',
            'fatigue_context_settings',
            'user_profile_preferences',
            'user_profile_lifts',
            'user_profile',
            'body_composition_snapshots',
            'exercise_isolated_muscles',
            'workout_log',
            'user_selection',
            'progression_goals',
            'muscle_volumes',
            'volume_plans',
            'exercises',
        ]
        for table in tables:
            db_handler.execute_query(f"DELETE FROM {table}")
    
    yield db_handler


@pytest.fixture
def exercise_factory(clean_db):
    """Factory for creating test exercises."""
    def _create_exercise(name, **kwargs):
        """Create an exercise with optional attributes."""
        defaults = {
            'primary_muscle_group': 'Chest',
            'secondary_muscle_group': 'Triceps',
            'tertiary_muscle_group': 'Shoulders',
            'force': 'Push',
            'equipment': 'Barbell',
            'mechanic': 'Compound',
            'utility': 'Basic',
            'difficulty': 'Intermediate'
        }
        defaults.update(kwargs)
        
        query = """
        INSERT INTO exercises (exercise_name, primary_muscle_group, secondary_muscle_group,
                              tertiary_muscle_group, force, equipment, mechanic, utility, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            name,
            defaults.get('primary_muscle_group'),
            defaults.get('secondary_muscle_group'),
            defaults.get('tertiary_muscle_group'),
            defaults.get('force'),
            defaults.get('equipment'),
            defaults.get('mechanic'),
            defaults.get('utility'),
            defaults.get('difficulty')
        )
        
        clean_db.execute_query(query, params)
        return name
    
    return _create_exercise


@pytest.fixture
def workout_plan_factory(clean_db, exercise_factory):
    """Factory for creating test workout plan entries."""
    def _create_workout_plan(exercise_name=None, routine="GYM - Full Body - Workout A", **kwargs):
        """Create a workout plan entry."""
        if exercise_name is None:
            exercise_name = exercise_factory("Test Exercise")
        
        defaults = {
            'routine': routine,
            'exercise': exercise_name,
            'sets': 3,
            'min_rep_range': 6,
            'max_rep_range': 8,
            'rir': 3,
            'rpe': 7.0,
            'weight': 50.0
        }
        defaults.update(kwargs)
        
        query = """
        INSERT INTO user_selection (routine, exercise, sets, min_rep_range, max_rep_range, rir, rpe, weight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            defaults['routine'],
            defaults['exercise'],
            defaults['sets'],
            defaults['min_rep_range'],
            defaults['max_rep_range'],
            defaults['rir'],
            defaults.get('rpe'),
            defaults['weight']
        )
        
        clean_db.execute_query(query, params)
        
        # Get the inserted ID
        result = clean_db.fetch_one("SELECT last_insert_rowid() as id")
        return result['id']
    
    return _create_workout_plan


@pytest.fixture
def workout_log_factory(clean_db, workout_plan_factory):
    """Factory for creating test workout log entries."""
    def _create_workout_log(plan_id=None, **kwargs):
        """Create a workout log entry."""
        if plan_id is None:
            plan_id = workout_plan_factory()
        
        defaults = {
            'workout_plan_id': plan_id,
            'routine': "GYM - Full Body - Workout A",
            'exercise': "Test Exercise",
            'planned_sets': 3,
            'planned_min_reps': 6,
            'planned_max_reps': 8,
            'planned_rir': 3,
            'planned_rpe': 7.0,
            'planned_weight': 50.0,
            'scored_min_reps': 6,
            'scored_max_reps': 8,
            'scored_rir': 2,
            'scored_rpe': 8.0,
            'scored_weight': 52.5
        }
        defaults.update(kwargs)
        
        query = """
        INSERT INTO workout_log (workout_plan_id, routine, exercise, planned_sets, planned_min_reps,
                                planned_max_reps, planned_rir, planned_rpe, planned_weight,
                                scored_min_reps, scored_max_reps, scored_rir, scored_rpe, scored_weight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            defaults['workout_plan_id'],
            defaults['routine'],
            defaults['exercise'],
            defaults['planned_sets'],
            defaults['planned_min_reps'],
            defaults['planned_max_reps'],
            defaults['planned_rir'],
            defaults.get('planned_rpe'),
            defaults['planned_weight'],
            defaults['scored_min_reps'],
            defaults['scored_max_reps'],
            defaults['scored_rir'],
            defaults.get('scored_rpe'),
            defaults['scored_weight']
        )
        
        clean_db.execute_query(query, params)
        
        # Get the inserted ID
        result = clean_db.fetch_one("SELECT last_insert_rowid() as id")
        return result['id']
    
    return _create_workout_log

