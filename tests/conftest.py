"""
Pytest configuration and fixtures for Priority 0 security tests.
"""
import pytest
import os
import shutil
from pathlib import Path
from flask import Flask, jsonify
from utils.database import DatabaseHandler
from routes.workout_plan import workout_plan_bp
from routes.filters import filters_bp
from routes.workout_log import workout_log_bp
from routes.weekly_summary import weekly_summary_bp
from routes.session_summary import session_summary_bp
from routes.exports import exports_bp
from routes.main import main_bp
from routes.progression_plan import progression_plan_bp
from routes.user_profile import user_profile_bp
from routes.body_composition import body_composition_bp
from routes.volume_splitter import volume_splitter_bp
from routes.program_backup import program_backup_bp
from routes.fatigue import fatigue_bp
from utils.catalog_seed import bootstrap_runtime_database
from utils.schema_registry import drop_all_owned_tables, run_all_initializers
from utils.errors import success_response, error_response
import utils.config


# Override config before importing app
os.environ['TESTING'] = '1'
TEST_DB_FILENAME = "test_hypertrophy_toolbox.db"


def _initialize_test_database() -> None:
    """Create the full test schema for the active database path."""
    run_all_initializers(force_base=True)


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

    ``run_all_initializers()`` costs ~290ms here. It commits each DDL statement
    separately, and the pragma profile tests run under fsyncs every one of them:
    ``utils/database.py`` defaults ``FLASK_DEBUG`` to ``'1'``, which selects
    ``journal_mode = DELETE`` + ``synchronous = FULL``. Paid once per ``app``
    fixture — 787 times per full run — that single call is the largest cost in
    the suite. Copying the finished file instead costs ~0.4ms.

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
    """A client for ``app.py``'s own routes, on a scratch database.

    Distinct from the ``app`` fixture below, which builds a blueprint-only twin.
    Some behavior lives on the real application object and nowhere else — the
    ``/erase-data`` confirm guard, the error-handler layering, trailing-slash
    routing — so it can only be covered against the real one.

    Isolation here is load-bearing, and patching ``utils.config.DB_FILE`` alone
    is NOT enough:

    * ``utils/config.py`` resolves ``DB_FILE`` from the **environment** at import
      time, and ``prepare_runtime_database()`` takes its ``explicit-override``
      branch only when ``os.environ['DB_FILE']`` is set.
    * ``app.py``'s startup then *reassigns* ``utils.config.DB_FILE`` from that
      call's result. With no environment override, a first import resolves the
      real runtime database — the checkout's own ``data/database.db`` in a source
      tree — and silently discards the scratch path.

    So the environment variable is set too, the scratch path is reasserted after
    the import (whether or not that import was a cached no-op that ran startup
    under some other module's path), and the resolved path is asserted before any
    write happens. Both the environment variable and the module attribute are
    restored on teardown, as is the app's original ``TESTING`` value.
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
    # DB_FILE only relocates the database. HT_RUNTIME_DIR relocates the whole
    # runtime tree, so auto-backups and logs land in the scratch area too rather
    # than in the repository — otherwise the first test to exercise a path that
    # writes a backup would target <repo>/data/auto_backup.
    os.environ['HT_RUNTIME_DIR'] = str(runtime_root)
    utils.config.DB_FILE = str(scratch_db)
    try:
        from app import app as real_app

        # Read what app.py's startup actually resolved, BEFORE overwriting it.
        # The previous version reasserted the scratch path first and then
        # compared, which read back the value it had just written and so could
        # never detect a defeated override. On a cached import nothing reassigns
        # and this is simply the value set above; on a fresh import it is
        # whatever prepare_runtime_database() decided, which is the case worth
        # catching. Failing here happens before bootstrap_runtime_database() and
        # run_all_initializers() below, so a defeated override cannot reach a
        # real database.
        resolved_by_startup = Path(utils.config.DB_FILE).resolve()
        if resolved_by_startup != scratch_resolved:
            pytest.fail(
                "real_app_client refuses to run: app.py's startup resolved a "
                "database that is not the fixture scratch database.\n"
                f"  resolved: {resolved_by_startup}\n  scratch:  {scratch_resolved}"
            )

        original_testing = bool(real_app.config.get('TESTING', False))
        real_app.config['TESTING'] = True

        with real_app.app_context():
            bootstrap_runtime_database()
            run_all_initializers(force_base=True)

        with real_app.test_client() as client:
            yield client
    finally:
        if real_app is not None and original_testing is not None:
            real_app.config['TESTING'] = original_testing
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
    """Create Flask app with test configuration."""
    original_db_file = utils.config.DB_FILE
    utils.config.DB_FILE = test_db_path

    repo_root = Path(__file__).resolve().parents[1]

    app = Flask(
        __name__,
        template_folder=str(repo_root / "templates"),
        static_folder=str(repo_root / "static"),
    )
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.url_map.strict_slashes = False

    app.register_blueprint(main_bp)
    app.register_blueprint(workout_log_bp)
    app.register_blueprint(weekly_summary_bp)
    app.register_blueprint(session_summary_bp)
    app.register_blueprint(exports_bp)
    app.register_blueprint(filters_bp)
    app.register_blueprint(workout_plan_bp)
    app.register_blueprint(progression_plan_bp)
    app.register_blueprint(user_profile_bp)
    app.register_blueprint(body_composition_bp)
    app.register_blueprint(volume_splitter_bp)
    app.register_blueprint(program_backup_bp)
    app.register_blueprint(fatigue_bp)

    from utils.media_path import is_valid_media_path_shape

    @app.template_filter('safe_media_path')
    def _safe_media_path(value):
        return value if is_valid_media_path_shape(value) else None

    @app.route('/erase-data', methods=['POST'])
    def erase_data():
        try:
            # Drop ALL tables including backup tables (full reset)
            with DatabaseHandler() as db:
                drop_all_owned_tables(db)

            _initialize_test_database()

            return jsonify(success_response(
                data=None,
                message='All data has been erased and tables reinitialized successfully.'
            ))
        except Exception:
            return error_response("INTERNAL_ERROR", "Failed to erase data", 500)

    # Copy the prebuilt empty schema rather than re-running every initializer.
    # Equivalent output, ~700x cheaper; see the schema_template fixture. The
    # erase-data route above deliberately still calls the real initializers,
    # since that path is asserting they work.
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

