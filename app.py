
# The interpreter guard runs before the rest of the imports on purpose, so an
# unsupported Python fails with ADR-003's message instead of a SyntaxError from
# a dependency that assumes newer syntax. That ordering makes every import below
# E402, hence the per-line suppressions. Do NOT collapse them into a file-level
# `# flake8: noqa: E402` - flake8 7.x treats that as a blanket noqa and would
# silently drop this file out of the blocking F401/F811/E711/E712 gate.
from utils.python_version import require_supported_python

require_supported_python()

from flask import Flask, jsonify, request, g  # noqa: E402
import utils.config  # noqa: E402
from utils.database import DatabaseHandler  # noqa: E402
from utils.auto_backup import create_startup_backup, describe_snapshot  # noqa: E402
from utils.catalog_seed import bootstrap_runtime_database  # noqa: E402
from utils.catalog_upgrade import upgrade_catalog_from_seed  # noqa: E402
from utils.runtime_migration import prepare_runtime_database  # noqa: E402
from utils.schema_registry import drop_all_owned_tables, run_all_initializers  # noqa: E402
from routes.workout_log import workout_log_bp  # noqa: E402
from routes.weekly_summary import weekly_summary_bp  # noqa: E402
from routes.session_summary import session_summary_bp  # noqa: E402
from routes.exports import exports_bp  # noqa: E402
from routes.filters import filters_bp  # noqa: E402
from routes.workout_plan import workout_plan_bp  # noqa: E402
from routes.main import main_bp  # noqa: E402
from routes.progression_plan import progression_plan_bp  # noqa: E402
from routes.user_profile import user_profile_bp  # noqa: E402
from routes.body_composition import body_composition_bp  # noqa: E402
from routes.volume_splitter import volume_splitter_bp  # noqa: E402
from routes.program_backup import program_backup_bp  # noqa: E402
from routes.fatigue import fatigue_bp  # noqa: E402
from datetime import datetime  # noqa: E402
from werkzeug.middleware.proxy_fix import ProxyFix  # noqa: E402
from utils.logger import setup_logging  # noqa: E402
from utils.errors import error_response, register_error_handlers, register_fallback_handlers  # noqa: E402
from utils.request_id import add_request_id_middleware  # noqa: E402
import time  # noqa: E402
import sys  # noqa: E402

app = Flask(__name__)
app.url_map.strict_slashes = False  # This makes Flask handle URLs with or without trailing slashes
app.wsgi_app = ProxyFix(app.wsgi_app)

# Production optimizations when running as frozen executable
if getattr(sys, 'frozen', False):
    # Enable Jinja2 template caching (auto_reload=False, cache_size increased)
    app.jinja_env.auto_reload = False
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    # Disable debug mode for production
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    # Enable response compression hints
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year cache for static files

# Setup structured logging
logger = setup_logging(app)

# Add request ID middleware for tracking and correlation
add_request_id_middleware(app)

# Register standardized error handlers, then the fallback layer that owns
# whatever they do not: 404, unclaimed HTTP errors, and unhandled exceptions.
# Both live in utils.errors so the priority-7 test fixture registers identical
# layering instead of hand-copying it. Order matters — see
# register_fallback_handlers' docstring.
register_error_handlers(app)
register_fallback_handlers(app)

# Initialize the database.
# Order matters and is load-bearing: an existing database is moved out of the
# installation directory BEFORE the seed bootstrap runs, so a user upgrading a
# frozen install never boots onto a fresh empty catalog while their real data
# sits at the old path. A migration that could not be proven correct returns the
# legacy path, and the seed bootstrap then sees an existing database and does
# nothing.
migration = prepare_runtime_database()
utils.config.DB_FILE = str(migration.database_path)
database_seeded = bootstrap_runtime_database()
run_all_initializers(force_base=False)

# Bring an existing install's catalog up to the shipped one. Called from real
# startup only, never from run_all_initializers(): the test suite initializes
# empty schemas on purpose, and seeding 1,897 exercises into them would change
# what most of the suite means. Additive and update-only — see
# utils/catalog_upgrade.py for why deletion is not the symmetric case.
if not database_seeded:
    upgrade_catalog_from_seed()

# The immutable seed is already a pristine recovery source. Avoid an immediate,
# redundant first-run snapshot; normal subsequent startups retain the backup.
if not database_seeded:
    create_startup_backup()

# Register blueprints
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

# Log registered routes (debug level only)
logger.debug("Registered routes:")
for rule in app.url_map.iter_rules():
    methods = ', '.join(sorted(rule.methods)) if rule.methods else ''
    logger.debug(f"{rule.endpoint}: {rule.rule} [{methods}]")

@app.template_filter('datetime')
def format_datetime(value, format='%d-%m-%Y'):
    if value and value != 'None':
        try:
            if isinstance(value, str):
                # Parse the date string (assuming it's in ISO format)
                date_obj = datetime.strptime(value, '%Y-%m-%d')
            else:
                date_obj = value
            return date_obj.strftime(format)
        except (ValueError, TypeError):
            return value
    return ''


@app.template_filter('safe_media_path')
def safe_media_path(value):
    """Return `value` if it satisfies the §4.3 media_path shape rules, else None.

    Defense-in-depth: the apply script validates on write, but rows can be
    edited out-of-band and PLANNING §4.4 mandates revalidation on render.
    Templates wrap `log.media_path | safe_media_path` and skip the `<img>`
    when the filter returns None.
    """
    from utils.media_path import is_valid_media_path_shape
    return value if is_valid_media_path_shape(value) else None

@app.before_request
def clear_trailing():
    from flask import redirect, request
    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

@app.before_request
def start_timer():
    """Store request start time for performance logging."""
    g.start_time = time.time()

@app.context_processor
def inject_scale_level():
    """Inject UI scale level into all templates from cookie."""
    scale = request.cookies.get('ui-scale-level', '6')
    # Validate scale is 1-8
    try:
        scale_int = int(scale)
        if scale_int < 1 or scale_int > 8:
            scale = '6'
    except (ValueError, TypeError):
        scale = '6'
    
    zoom_values = {'1': '0.75', '2': '0.8', '3': '0.85', '4': '0.9', '5': '0.95', '6': '1', '7': '1.1', '8': '1.2'}
    return {
        'ui_scale_level': scale,
        'ui_zoom_value': zoom_values.get(scale, '1')
    }

# Test routes removed - no longer needed

@app.route('/erase-data', methods=['POST'])
def erase_data():
    payload = request.get_json(silent=True) or {}
    if payload.get('confirm') != 'ERASE_ALL_DATA':
        return error_response(
            "VALIDATION_ERROR",
            "Erase requires confirm=ERASE_ALL_DATA in the request body.",
            400,
        )
    try:
        # Snapshot before wiping so the nuke is recoverable from data/auto_backup/.
        snapshot_path = create_startup_backup()
        # Drop ALL tables including backup tables (full reset)
        with DatabaseHandler() as db:
            drop_all_owned_tables(db)

        # Reinitialize database - force=True to bypass the initialization guard
        # since we just dropped the tables
        run_all_initializers(force_base=True)
        
        from utils.errors import success_response

        response_message = 'All data has been erased and tables reinitialized successfully.'

        return jsonify(success_response(
            data={"auto_backup": describe_snapshot(snapshot_path)},
            message=response_message
        ))
    except Exception:
        logger.exception("Error erasing data")
        return error_response("INTERNAL_ERROR", "Failed to erase data", 500)


if __name__ == "__main__":
    import atexit
    import signal
    import os
    
    # Register cleanup on graceful shutdown
    def cleanup_on_exit():
        """Cleanup resources on application exit."""
        try:
            # Checkpoint any open WAL files
            with DatabaseHandler() as db:
                db.connection.execute("PRAGMA wal_checkpoint(TRUNCATE);")
            logger.info("Database cleanup completed on exit")
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")
    
    atexit.register(cleanup_on_exit)
    
    # Handle SIGTERM (Ctrl+C) gracefully
    def signal_handler(_sig, _frame):
        del _sig, _frame  # Required by signal.signal(); intentionally unused.
        logger.info("Received shutdown signal, cleaning up...")
        cleanup_on_exit()
        import sys
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Use use_reloader=False to prevent the double-process issue that causes
    # database corruption. The auto-reloader spawns a child process that
    # re-runs all startup code, leading to concurrent database writes.
    # For development with auto-reload, use: flask run --reload
    use_reloader = os.getenv('FLASK_USE_RELOADER', '0') == '1'
    
    # Security: Debug mode controlled by environment variable, defaults to False
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    
    app.run(debug=debug_mode, use_reloader=use_reloader)
