# The interpreter guard runs before the rest of the imports on purpose, so an
# unsupported Python fails with ADR-003's message instead of a SyntaxError from
# a dependency that assumes newer syntax. That ordering makes every import below
# E402, hence the per-line suppressions. Do NOT collapse them into a file-level
# `# flake8: noqa: E402` - flake8 7.x treats that as a blanket noqa and would
# silently drop this file out of the blocking F401/F811/E711/E712 gate.
from utils.python_version import require_supported_python

require_supported_python()

from flask import Flask, current_app, jsonify, request  # noqa: E402
import utils.config  # noqa: E402
from utils.database import DatabaseHandler  # noqa: E402
from utils.auto_backup import create_startup_backup, describe_snapshot  # noqa: E402
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
from collections.abc import Mapping  # noqa: E402
from datetime import datetime  # noqa: E402
from typing import Any  # noqa: E402
from werkzeug.middleware.proxy_fix import ProxyFix  # noqa: E402
from utils.logger import get_logger  # noqa: E402
from utils.errors import (  # noqa: E402
    error_response,
    register_error_handlers,
    register_fallback_handlers,
    success_response,
)
from utils.request_id import add_request_id_middleware  # noqa: E402
from utils.runtime_init import init_runtime, should_initialize_runtime  # noqa: E402
from utils.version import APP_VERSION  # noqa: E402
import os  # noqa: E402
import sys  # noqa: E402

# The frozen build's long-cache window. Named rather than inlined so the tests
# and scripts/smoke_packaged_app.py assert against this value instead of each
# hardcoding their own copy, which could then silently disagree with it.
STATIC_LONG_MAX_AGE_SECONDS = 31536000  # 1 year

logger = get_logger()


def format_datetime(value, date_format='%d-%m-%Y'):
    if value and value != 'None':
        try:
            if isinstance(value, str):
                # Parse the date string (assuming it's in ISO format)
                date_obj = datetime.strptime(value, '%Y-%m-%d')
            else:
                date_obj = value
            return date_obj.strftime(date_format)
        except (ValueError, TypeError):
            return value
    return ''


def safe_media_path(value):
    """Return `value` if it satisfies the §4.3 media_path shape rules, else None.

    Defense-in-depth: the apply script validates on write, but rows can be
    edited out-of-band and PLANNING §4.4 mandates revalidation on render.
    Templates wrap `log.media_path | safe_media_path` and skip the `<img>`
    when the filter returns None.
    """
    from utils.media_path import is_valid_media_path_shape
    return value if is_valid_media_path_shape(value) else None


def apply_static_cache_policy(response):
    """Long-cache a static file only when it was requested at this version.

    F4: a blanket ``SEND_FILE_MAX_AGE_DEFAULT`` of a year meant an upgraded
    install kept serving the previous build's assets. Versioning the URLs is
    only half the fix — the cache policy has to distinguish them, because two
    classes of asset carry no ``?v=`` and never can:

    * **transitive ES-module imports.** A ``?v=`` on ``app.js`` does not
      propagate to what it imports: ``import './toast.js'`` resolves against the
      module URL and is fetched bare. Rewriting every import is not tractable,
      so those requests must revalidate instead.
    * **assets fetched at runtime by JS** — the bodymap SVGs and the vendor
      exercise catalog build their URLs in code, not in a template.

    Anything without the current version therefore gets ``no-cache``, which
    still allows a 304 on an unchanged file but can never serve a stale one.

    Only successful responses are long-cached. ``request.endpoint`` is set at
    routing time, so a request for a file missing from the bundle still reaches
    here as ``'static'`` after ``send_static_file`` raised ``NotFound`` — and a
    year-long ``immutable`` on that 404 would pin it in the browser, so a
    hot-fix that ships the file without bumping the version could never be
    picked up. That is the same stale-after-upgrade failure this hook exists to
    prevent, arriving by the opposite route.
    """
    if request.endpoint != 'static':
        return response

    long_max_age = current_app.config.get('STATIC_LONG_MAX_AGE', 0)
    if (
        long_max_age
        and response.status_code in (200, 304)
        and request.args.get('v') == APP_VERSION
    ):
        response.headers['Cache-Control'] = (
            f'public, max-age={long_max_age}, immutable'
        )
    else:
        response.headers['Cache-Control'] = 'no-cache, must-revalidate'
    return response


def inject_app_version():
    """Expose the app version so templates can cache-bust first-party assets.

    Frozen builds long-cache only version-matching static requests — see
    apply_static_cache_policy() and STATIC_LONG_MAX_AGE. Without this value in
    the template context every link renders `?v=` empty, nothing matches, and
    the long cache silently stops applying to anything.

    Do NOT "restore" SEND_FILE_MAX_AGE_DEFAULT here: setting it applies the year
    to every static response including unversioned ones, which is the
    stale-after-upgrade bug F4 records.
    """
    return {'app_version': APP_VERSION}


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

        return jsonify(success_response(
            data={"auto_backup": describe_snapshot(snapshot_path)},
            message='All data has been erased and tables reinitialized successfully.'
        ))
    except Exception:
        logger.exception("Error erasing data")
        return error_response("INTERNAL_ERROR", "Failed to erase data", 500)


def create_app(config_overrides: Mapping[str, Any] | None = None) -> Flask:
    """Build the application. Does no logging setup and no database work.

    The runtime database is initialized separately by ``init_runtime()``, which
    only the entry points call: ``main()``, ``app_launcher.main()`` and
    ``create_initialized_app()``.
    """
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
        # Long-cache static files, but only the ones asked for at the current
        # version — apply_static_cache_policy() narrows this per request.
        # SEND_FILE_MAX_AGE_DEFAULT is deliberately left alone: it would apply the
        # year to every static response including unversioned ones, which is the
        # stale-after-upgrade bug F4 records.
        app.config['STATIC_LONG_MAX_AGE'] = STATIC_LONG_MAX_AGE_SECONDS

    if config_overrides:
        app.config.update(config_overrides)

    # Add request ID middleware for tracking and correlation
    add_request_id_middleware(app)

    # Register standardized error handlers, then the fallback layer that owns
    # whatever they do not: 404, unclaimed HTTP errors, and unhandled exceptions.
    # Both live in utils.errors so the priority-7 test fixture registers identical
    # layering instead of hand-copying it. Order matters — see
    # register_fallback_handlers' docstring.
    register_error_handlers(app)
    register_fallback_handlers(app)

    for blueprint in (
        main_bp,
        workout_log_bp,
        weekly_summary_bp,
        session_summary_bp,
        exports_bp,
        filters_bp,
        workout_plan_bp,
        progression_plan_bp,
        user_profile_bp,
        body_composition_bp,
        volume_splitter_bp,
        program_backup_bp,
        fatigue_bp,
    ):
        app.register_blueprint(blueprint)

    app.add_template_filter(format_datetime, 'datetime')
    app.add_template_filter(safe_media_path, 'safe_media_path')
    app.after_request(apply_static_cache_policy)
    app.context_processor(inject_app_version)
    app.context_processor(inject_scale_level)
    app.add_url_rule('/erase-data', endpoint='erase_data', view_func=erase_data, methods=['POST'])
    return app


def create_initialized_app() -> Flask:
    """The ``flask`` CLI target: initialize the runtime, then build the app.

    Every ``flask`` subcommand against this factory (``run``, ``routes``,
    ``shell``, ...) initializes the runtime database.
    """
    init_runtime()
    return create_app()


# Do not point FLASK_APP at this object: it is uninitialized, so it would serve
# a runtime database that was never migrated, seeded or upgraded. Use the
# factory target app:create_initialized_app instead.
app = create_app()


def _register_shutdown_cleanup() -> None:
    """Checkpoint the WAL on exit and on SIGINT/SIGTERM."""
    import atexit
    import signal

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

    # Handle SIGINT (Ctrl+C) and SIGTERM gracefully
    def signal_handler(_sig, _frame):
        del _sig, _frame  # Required by signal.signal(); intentionally unused.
        logger.info("Received shutdown signal, cleaning up...")
        cleanup_on_exit()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def main() -> None:
    # use_reloader defaults to off. With FLASK_USE_RELOADER=1, only the serving
    # child initializes the runtime and registers the WAL cleanup (see
    # should_initialize_runtime). For flask run, use
    # FLASK_APP=app:create_initialized_app with --no-reload; every flask
    # subcommand against that factory initializes the runtime database.
    use_reloader = os.getenv('FLASK_USE_RELOADER', '0') == '1'

    # Security: Debug mode controlled by environment variable, defaults to False
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'

    if should_initialize_runtime(use_reloader):
        init_runtime()
        _register_shutdown_cleanup()

    # Honour HT_PORT so the packaged smoke can serve on a port it has confirmed
    # is free. This is the payload launch path; app_launcher.py is the other.
    app.run(port=utils.config.runtime_port(), debug=debug_mode, use_reloader=use_reloader)


if __name__ == "__main__":
    main()
