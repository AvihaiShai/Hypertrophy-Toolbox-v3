"""Contracts for ``create_app()`` and the entry points that join it to the runtime.

WS3 (``docs/app_factory/PLANNING.md`` Plan v2 §V5) makes ``create_app()`` the
one construction path: production, the packaged launcher, ``flask run`` and the
test suite all build through it, and only the entry points call
``init_runtime()``. These pin what the factory builds, that building it does no
logging setup or database work, and how ``main()``, the launcher and
``create_initialized_app()`` order initialization, cleanup and serving.

``app`` is imported through the ``app_module`` fixture, never at collection: a
first import used to run the whole runtime startup, so the fixture points the
environment at a scratch tree for the duration of that import.
"""
from __future__ import annotations

import atexit
import importlib
import json
import logging
import os
import re
import shutil
import signal
import subprocess
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from types import ModuleType

import pytest
from flask import Flask, abort
from werkzeug.middleware.proxy_fix import ProxyFix

import utils.config
import utils.logger

ROOT = Path(__file__).resolve().parents[1]

# The one deliberate second registration site (R-4): a test oracle, so a
# blueprint dropped from create_app() fails here rather than only as a 404.
EXPECTED_BLUEPRINTS = frozenset({
    "main",
    "workout_log",
    "weekly_summary",
    "session_summary",
    "exports",
    "filters",
    "workout_plan",
    "progression_plan",
    "user_profile",
    "body_composition",
    "volume_splitter",
    "program_backup",
    "fatigue",
})

FACTORY_TARGET = "app:create_initialized_app"

# Q-WS3-2(a), verbatim from docs/app_factory/PLANNING.md Section 0.
IMPORT_PROMISE = (
    "Importing `app` performs no database, data-directory, migration, seed, "
    "catalog-upgrade or backup work. The first `get_logger()` call in a process "
    "— triggered transitively by importing `app`, any route module or most "
    "`utils` modules — still creates `<runtime root>/logs/` and attaches the "
    "`app.log` file handler and the console handler."
)

ERASE_MESSAGE = "All data has been erased and tables reinitialized successfully."
REQUEST_ID = re.compile(r"^req_[0-9a-f]{16}$")


@pytest.fixture(scope="module")
def app_module(tmp_path_factory) -> ModuleType:
    """``app``, imported with the environment pointed at scratch.

    Harmless once import does no data work; before that it keeps a first
    import's startup off the checkout's own database.
    """
    scratch = tmp_path_factory.mktemp("factory_import")
    saved_env = {name: os.environ.get(name) for name in ("DB_FILE", "HT_RUNTIME_DIR")}
    saved_attribute = utils.config.DB_FILE
    os.environ["DB_FILE"] = str(scratch / "database.db")
    os.environ["HT_RUNTIME_DIR"] = str(scratch)
    try:
        return importlib.import_module("app")
    finally:
        utils.config.DB_FILE = saved_attribute
        for name, value in saved_env.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


@pytest.fixture
def factory_app(app_module, schema_template, tmp_path, monkeypatch) -> Flask:
    """A fresh ``create_app(TESTING)`` on a copy of the empty test schema."""
    database = tmp_path / "factory.db"
    shutil.copyfile(schema_template, database)
    monkeypatch.setattr(utils.config, "DB_FILE", str(database))
    return app_module.create_app(config_overrides={"TESTING": True})


def _rule_set(app: Flask) -> set[tuple[str, str, frozenset[str]]]:
    return {
        (rule.rule, rule.endpoint, frozenset(rule.methods or ()))
        for rule in app.url_map.iter_rules()
    }


def _hook_names(hooks: dict) -> dict[object, list[tuple[str, str]]]:
    return {
        key: [(function.__module__, function.__qualname__) for function in functions]
        for key, functions in hooks.items() if functions
    }


def _hypertrophy_handlers() -> list[logging.Handler]:
    return list(logging.getLogger("hypertrophy_toolbox").handlers)


# --- AC4: factory construction -------------------------------------------------


def test_two_factory_calls_build_distinct_equivalent_apps(app_module):
    first = app_module.create_app()
    second = app_module.create_app()

    assert len(EXPECTED_BLUEPRINTS) == 13
    assert isinstance(first, Flask) and isinstance(second, Flask)
    assert first is not second
    assert first is not app_module.app and second is not app_module.app
    for built in (first, second, app_module.app):
        assert set(built.blueprints) == EXPECTED_BLUEPRINTS
    assert _rule_set(first) == _rule_set(second) == _rule_set(app_module.app)
    assert ("/erase-data", "erase_data", frozenset({"POST", "OPTIONS"})) in _rule_set(first)


def test_blueprint_rules_are_non_strict_static_excepted(app_module):
    """Every rule but ``static`` is non-strict.

    Flask adds its ``static`` rule inside ``Flask.__init__``, binding it with
    the map's default ``strict_slashes=True`` before any setting can apply.
    That was equally true of the module-level app before WS3, so the exemption
    preserves behavior rather than relaxing it [TS-2].
    """
    built = app_module.create_app()
    checked = [rule for rule in built.url_map.iter_rules() if rule.endpoint != "static"]

    assert len(checked) > 13
    assert [rule.rule for rule in checked if rule.strict_slashes is not False] == []


@pytest.mark.parametrize("path", ["/workout_plan/", "/weekly_summary/", "/progression/"])
def test_trailing_slash_get_on_blueprint_rules_is_served(factory_app, path):
    response = factory_app.test_client().get(path)

    assert response.status_code == 200
    assert "Location" not in response.headers


def test_proxyfix_wraps_wsgi_app(app_module):
    assert isinstance(app_module.create_app().wsgi_app, ProxyFix)


def test_responses_carry_request_id(factory_app):
    client = factory_app.test_client()

    generated = client.get("/static/css/base.css")
    assert generated.status_code == 200
    assert REQUEST_ID.match(generated.headers.get("X-Request-ID", ""))

    echoed = client.get("/static/css/base.css", headers={"X-Request-ID": "req_0123456789abcdef"})
    assert echoed.headers.get("X-Request-ID") == "req_0123456789abcdef"


def test_handler_layering_behaves_as_documented(factory_app):
    """Code-keyed handlers first, then the fallback layer (``utils/errors.py``).

    Under ``TESTING`` an uncaught exception still becomes a 500 envelope,
    because the ``Exception`` handler claims it before Flask would propagate.
    """
    def bad_request():
        abort(400)

    def boom():
        raise RuntimeError("deliberate failure")

    factory_app.add_url_rule("/__test_bad_request__", "test_bad_request", bad_request)
    factory_app.add_url_rule("/__test_boom__", "test_boom", boom)
    client = factory_app.test_client()
    xhr = {"Accept": "application/json"}

    bad = client.get("/__test_bad_request__", headers=xhr)
    assert bad.status_code == 400
    assert bad.get_json()["error"]["code"] == "BAD_REQUEST"

    not_allowed = client.get("/export_to_workout_log", headers=xhr)
    assert not_allowed.status_code == 405
    assert not_allowed.get_json()["error"]["code"] == "METHOD_NOT_ALLOWED"
    assert "POST" in not_allowed.headers.get("Allow", "")

    missing = client.get("/__no_such_route__", headers=xhr)
    assert missing.status_code == 404
    assert missing.get_json()["error"]["code"] == "NOT_FOUND"

    crashed = client.get("/__test_boom__", headers=xhr)
    assert crashed.status_code == 500
    assert crashed.get_json()["error"]["code"] == "INTERNAL_ERROR"


def test_filters_hooks_processors_and_erase_route_present(factory_app, app_module):
    filters = factory_app.jinja_env.filters
    assert filters["datetime"] is app_module.format_datetime
    assert filters["safe_media_path"] is app_module.safe_media_path
    assert filters["datetime"]("2026-01-31") == "31-01-2026"

    processors = factory_app.template_context_processors[None]
    assert app_module.inject_app_version in processors
    assert app_module.inject_scale_level in processors

    assert app_module.apply_static_cache_policy in factory_app.after_request_funcs[None]
    assert factory_app.view_functions["erase_data"] is app_module.erase_data


def test_only_request_id_and_cache_policy_hooks(factory_app, app_module):
    """Registration order is asserted, not only membership (GA-7).

    Flask runs after-request functions in reverse, so this order is what puts
    the cache policy before the request-id header, as before WS3.
    """
    assert _hook_names(factory_app.before_request_funcs) == {
        None: [("utils.request_id", "add_request_id_middleware.<locals>.before_request")],
    }
    assert _hook_names(factory_app.after_request_funcs) == {
        None: [
            ("utils.request_id", "add_request_id_middleware.<locals>.after_request"),
            ("app", "apply_static_cache_policy"),
        ],
    }
    assert factory_app.after_request_funcs[None][1] is app_module.apply_static_cache_policy


def test_config_overrides_apply_after_frozen_block(app_module, monkeypatch):
    monkeypatch.setattr(sys, "frozen", True, raising=False)

    built = app_module.create_app(config_overrides={"TESTING": True, "STATIC_LONG_MAX_AGE": 5})

    assert built.config["TESTING"] is True
    assert built.config["STATIC_LONG_MAX_AGE"] == 5
    assert built.config["DEBUG"] is False


def test_no_route_listing_logged(app_module, caplog):
    caplog.set_level(logging.DEBUG, logger="hypertrophy_toolbox")
    logging.getLogger("hypertrophy_toolbox").debug("capture probe")
    assert any(record.getMessage() == "capture probe" for record in caplog.records)
    caplog.clear()

    built = app_module.create_app()

    listed = {f"{rule.endpoint}: {rule.rule}" for rule in built.url_map.iter_rules()}
    messages = [record.getMessage() for record in caplog.records]
    assert not any("Registered routes" in message for message in messages)
    assert not any(message.startswith(entry) for message in messages for entry in listed)


def test_factory_does_no_logging_setup_or_database_work(app_module, monkeypatch, tmp_path):
    utils.logger.get_logger()
    target = tmp_path / "never.db"
    monkeypatch.setattr(utils.config, "DB_FILE", str(target))
    monkeypatch.setenv("DB_FILE", str(target))

    def forbidden(*_args, **_kwargs):
        raise AssertionError("create_app() reached a logging-setup, runtime or database call")

    monkeypatch.setattr(utils.logger, "setup_logging", forbidden)
    monkeypatch.setattr("sqlite3.connect", forbidden)
    for name in (
        "setup_logging", "init_runtime", "prepare_runtime_database",
        "bootstrap_runtime_database", "run_all_initializers",
        "upgrade_catalog_from_seed", "create_startup_backup",
    ):
        if hasattr(app_module, name):
            monkeypatch.setattr(app_module, name, forbidden)

    app_module.create_app()
    app_module.create_app(config_overrides={"TESTING": True})

    assert not target.exists()
    assert not (tmp_path / "auto_backup").exists()


def test_factory_adds_no_logger_handlers(app_module):
    utils.logger.get_logger()
    before = _hypertrophy_handlers()

    built = [app_module.create_app(), app_module.create_app()]

    after = _hypertrophy_handlers()
    assert after == before
    assert sum(type(handler) is RotatingFileHandler for handler in after) == 1
    assert sum(type(handler) is logging.StreamHandler for handler in after) == 1
    for instance in built:
        assert not {id(handler) for handler in instance.logger.handlers} & {id(handler) for handler in after}


# --- AC6: the test fixture is the factory ----------------------------------------


def test_app_fixture_is_the_factory_app(app, app_module):
    """conftest's ``app`` is ``create_app(config_overrides=...)``, not a twin."""
    assert app is not app_module.app
    assert Path(app.root_path).resolve() == ROOT
    assert app.name == "app"
    assert app.config["TESTING"] is True
    assert app.config["WTF_CSRF_ENABLED"] is False
    assert set(app.blueprints) == EXPECTED_BLUEPRINTS
    assert app.view_functions["erase_data"] is app_module.erase_data
    assert app.jinja_env.filters["datetime"] is app_module.format_datetime
    assert app_module.apply_static_cache_policy in app.after_request_funcs[None]


# --- AC7 (+R-5): launch paths -----------------------------------------------------


@pytest.fixture
def main_events(app_module, monkeypatch) -> list[tuple[str, tuple, dict]]:
    """``main()`` with initialization, cleanup registration and serving recorded."""
    events: list[tuple[str, tuple, dict]] = []

    def record(name):
        def recorder(*args, **kwargs):
            events.append((name, args, kwargs))
        return recorder

    monkeypatch.setattr(app_module, "init_runtime", record("init"))
    monkeypatch.setattr(app_module, "_register_shutdown_cleanup", record("cleanup"))
    monkeypatch.setattr(app_module.app, "run", record("run"))
    for name in ("FLASK_USE_RELOADER", "FLASK_DEBUG", "HT_PORT", "WERKZEUG_RUN_MAIN"):
        monkeypatch.delenv(name, raising=False)
    return events


def test_main_initializes_then_registers_cleanup_before_run(app_module, main_events):
    app_module.main()

    assert [event[0] for event in main_events] == ["init", "cleanup", "run"]
    assert main_events[0][1:] == ((), {})
    assert main_events[2][1:] == ((), {"port": 5000, "debug": False, "use_reloader": False})


def test_main_reloader_parent_does_not_initialize(app_module, main_events, monkeypatch):
    monkeypatch.setenv("FLASK_USE_RELOADER", "1")

    app_module.main()

    assert [event[0] for event in main_events] == ["run"]
    assert main_events[0][2]["use_reloader"] is True


def test_main_reloader_parent_registers_no_db_cleanup(app_module, monkeypatch):
    """The parent never initialized, so it must not checkpoint a database on
    exit or claim the signals either [AR-1]."""
    registrations: list[str] = []
    monkeypatch.setattr(app_module, "init_runtime", lambda *a, **k: registrations.append("init"))
    monkeypatch.setattr(atexit, "register", lambda *a, **k: registrations.append("atexit"))
    monkeypatch.setattr(signal, "signal", lambda *a, **k: registrations.append("signal"))
    monkeypatch.setattr(app_module.app, "run", lambda *a, **k: registrations.append("run"))
    monkeypatch.setenv("FLASK_USE_RELOADER", "1")
    monkeypatch.delenv("WERKZEUG_RUN_MAIN", raising=False)

    app_module.main()

    assert registrations == ["run"]


def test_main_reloader_child_initializes_and_registers_cleanup(app_module, main_events, monkeypatch):
    monkeypatch.setenv("FLASK_USE_RELOADER", "1")
    monkeypatch.setenv("WERKZEUG_RUN_MAIN", "true")

    app_module.main()

    assert [event[0] for event in main_events] == ["init", "cleanup", "run"]
    assert main_events[2][2]["use_reloader"] is True


def test_main_honours_port_and_debug(app_module, main_events, monkeypatch):
    monkeypatch.setenv("HT_PORT", "5432")
    monkeypatch.setenv("FLASK_DEBUG", "1")

    app_module.main()

    assert main_events[-1] == ("run", (), {"port": 5432, "debug": True, "use_reloader": False})


def test_register_shutdown_cleanup_registers_atexit_and_signals(app_module, monkeypatch):
    exit_hooks: list[object] = []
    signal_hooks: list[tuple[object, object]] = []
    monkeypatch.setattr(atexit, "register", lambda function, *a, **k: exit_hooks.append(function))
    monkeypatch.setattr(signal, "signal", lambda signum, handler: signal_hooks.append((signum, handler)))

    app_module._register_shutdown_cleanup()

    assert len(exit_hooks) == 1 and callable(exit_hooks[0])
    assert {signum for signum, _ in signal_hooks} == {signal.SIGINT, signal.SIGTERM}
    assert all(callable(handler) for _, handler in signal_hooks)

    # The registered cleanup is today's WAL checkpoint, moved verbatim.
    executed: list[str] = []

    class FakeDatabase:
        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return False

        @property
        def connection(self):
            return self

        def execute(self, statement):
            executed.append(statement)

    monkeypatch.setattr(app_module, "DatabaseHandler", FakeDatabase)
    cleanup = exit_hooks[0]
    assert callable(cleanup)
    cleanup()
    assert executed == ["PRAGMA wal_checkpoint(TRUNCATE);"]


@pytest.fixture
def launcher(app_module, monkeypatch):
    """``app_launcher`` with console output, the error wait and serving recorded."""
    monkeypatch.setattr(sys, "path", list(sys.path))
    module = importlib.import_module("app_launcher")
    events: list[tuple[str, object]] = []
    monkeypatch.setattr(module, "print", lambda *args, **_k: events.append(("print", " ".join(map(str, args)))), raising=False)
    monkeypatch.setattr(module, "input", lambda *_a: events.append(("input", "")) or "", raising=False)
    monkeypatch.setattr(app_module.app, "run", lambda *args, **kwargs: events.append(("run", kwargs)))
    monkeypatch.setenv("HT_NO_BROWSER", "1")
    monkeypatch.setenv("HT_PORT", "5433")
    return module, events


def _patch_launcher_init(monkeypatch, module, fake):
    # Plan v2 D-11 imports init_runtime lazily inside main(); a module-level
    # binding is patched too, so either form is exercised rather than the real call.
    monkeypatch.setattr("utils.runtime_init.init_runtime", fake)
    if hasattr(module, "init_runtime"):
        monkeypatch.setattr(module, "init_runtime", fake)


def _printed(events, text):
    return [index for index, (kind, value) in enumerate(events) if kind == "print" and text in str(value)]


def test_launcher_initializes_after_import_before_run(launcher, monkeypatch):
    module, events = launcher
    _patch_launcher_init(
        monkeypatch, module, lambda *args, **kwargs: events.append(("init", (args, kwargs)))
    )

    module.main()

    kinds = [kind for kind, _ in events]
    assert kinds.count("init") == 1 and kinds.count("run") == 1
    assert "input" not in kinds
    init_at, run_at = kinds.index("init"), kinds.index("run")
    assert events[init_at][1] == ((), {})
    # GA-5: a failed initialization must never have printed success first.
    assert _printed(events, "Loading application...")[0] < init_at < _printed(events, "Application loaded successfully!")[0]
    assert init_at < run_at
    assert events[run_at][1] == {
        "host": "127.0.0.1", "port": 5433, "debug": False, "threaded": True, "use_reloader": False,
    }


def test_launcher_init_failure_uses_error_wait(launcher, monkeypatch):
    module, events = launcher

    def failing_init(*_args, **_kwargs):
        raise RuntimeError("init failed")

    _patch_launcher_init(monkeypatch, module, failing_init)

    with pytest.raises(SystemExit) as exit_info:
        module.main()

    assert exit_info.value.code == 1
    kinds = [kind for kind, _ in events]
    assert kinds.count("run") == 0
    assert kinds.count("input") == 1, "the error-wait prompt was not shown"
    assert _printed(events, "Application loaded successfully!") == []
    assert _printed(events, "ERROR: Application failed to start!")


# --- AC8: /erase-data on the factory app -------------------------------------------


@pytest.fixture
def erase_steps(app_module, monkeypatch, tmp_path):
    """Record the erase route's three steps; the snapshot result is settable."""
    steps: list[tuple[str, dict]] = []
    state: dict[str, object] = {"snapshot": tmp_path / "auto_backup" / "database_20260101_000000.db", "drop_error": None}

    def snapshot():
        steps.append(("snapshot", {}))
        return state["snapshot"]

    def drop(_db):
        steps.append(("drop", {}))
        error = state["drop_error"]
        if isinstance(error, BaseException):
            raise error

    def reinitialize(**kwargs):
        steps.append(("reinitialize", kwargs))

    monkeypatch.setattr(app_module, "create_startup_backup", snapshot)
    monkeypatch.setattr(app_module, "drop_all_owned_tables", drop)
    monkeypatch.setattr(app_module, "run_all_initializers", reinitialize)
    return steps, state


def test_erase_success_snapshots_then_drops_then_reinitializes(factory_app, erase_steps):
    steps, _state = erase_steps

    response = factory_app.test_client().post("/erase-data", json={"confirm": "ERASE_ALL_DATA"})

    assert response.status_code == 200
    body = response.get_json()
    assert body["ok"] is True
    assert body["data"] == {"auto_backup": {"filename": "database_20260101_000000.db"}}
    assert body["message"] == ERASE_MESSAGE
    assert steps == [("snapshot", {}), ("drop", {}), ("reinitialize", {"force_base": True})]


def test_erase_success_without_snapshot_reports_none(factory_app, erase_steps):
    steps, state = erase_steps
    state["snapshot"] = None

    response = factory_app.test_client().post("/erase-data", json={"confirm": "ERASE_ALL_DATA"})

    assert response.status_code == 200
    assert response.get_json()["data"] == {"auto_backup": None}
    assert [name for name, _ in steps] == ["snapshot", "drop", "reinitialize"]


def test_erase_failure_returns_internal_error(factory_app, erase_steps):
    steps, state = erase_steps
    state["drop_error"] = RuntimeError("drop failed")

    response = factory_app.test_client().post("/erase-data", json={"confirm": "ERASE_ALL_DATA"})

    assert response.status_code == 500
    body = response.get_json()
    assert body["ok"] is False
    assert body["error"]["code"] == "INTERNAL_ERROR"
    assert body["error"]["message"] == "Failed to erase data"
    assert [name for name, _ in steps] == ["snapshot", "drop"]


@pytest.mark.parametrize("payload", [None, {}, {"confirm": "erase_all_data"}])
def test_erase_rejection_writes_nothing(factory_app, erase_steps, payload):
    steps, _state = erase_steps
    client = factory_app.test_client()

    response = client.post("/erase-data") if payload is None else client.post("/erase-data", json=payload)

    assert response.status_code == 400
    body = response.get_json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Erase requires confirm=ERASE_ALL_DATA in the request body."
    assert steps == []


# --- AC9: frozen build and import surface ------------------------------------------


def test_frozen_block_values(app_module, monkeypatch):
    unfrozen = app_module.create_app()
    assert unfrozen.config.get("STATIC_LONG_MAX_AGE", 0) == 0

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    frozen = app_module.create_app()

    assert frozen.jinja_env.auto_reload is False
    assert frozen.config["TEMPLATES_AUTO_RELOAD"] is False
    assert frozen.config["DEBUG"] is False
    assert frozen.config["TESTING"] is False
    assert frozen.config["STATIC_LONG_MAX_AGE"] == app_module.STATIC_LONG_MAX_AGE_SECONDS == 31536000


def test_public_import_surface(app_module):
    from app import STATIC_LONG_MAX_AGE_SECONDS, app as module_app

    assert isinstance(module_app, Flask)
    assert STATIC_LONG_MAX_AGE_SECONDS == 31536000
    for name in ("create_app", "create_initialized_app", "main", "_register_shutdown_cleanup"):
        assert callable(getattr(app_module, name, None)), name
    # Import-time startup left these behind; their absence is part of C-9.
    for name in ("migration", "database_seeded", "start_timer"):
        assert not hasattr(app_module, name), name


# --- AC10: the written promise -------------------------------------------------------


def test_claude_md_states_the_import_promise():
    """Compared with whitespace collapsed, so line wrapping is not a difference."""
    text = " ".join((ROOT / "CLAUDE.md").read_text(encoding="utf-8").split())

    assert IMPORT_PROMISE in text


# --- AC11 (+GA-1): flask run callers ---------------------------------------------------


def test_create_initialized_app_initializes_then_builds(app_module, monkeypatch):
    events: list[tuple[str, tuple, dict]] = []
    built = object()
    monkeypatch.setattr(app_module, "init_runtime", lambda *a, **k: events.append(("init", a, k)))

    def fake_create_app(*args, **kwargs):
        events.append(("create", args, kwargs))
        return built

    monkeypatch.setattr(app_module, "create_app", fake_create_app)

    assert app_module.create_initialized_app() is built
    assert events == [("init", (), {}), ("create", (), {})]


_FLASK_APP_ASSIGNMENT = re.compile(
    r"""FLASK_APP['"\]]*\s*(?::|=(?!=))\s*(?P<value>[^\s,;)\]}]+)"""
    r"""|['"]FLASK_APP['"]\s*,\s*(?P<setenv>['"][^'"]*['"])"""
)
_APP_OPTION = re.compile(r"""--app(?![\w-])(?:\s*=\s*|\s+|['"]\s*,\s*)(?P<value>[^\s,;)\]}]+)""")
_EXCLUDED_PREFIXES = ("docs/archive/", "docs/app_factory/")


def _literal_target(raw: str) -> str | None:
    """The literal a caller points Flask at, or None for a variable reference."""
    value = raw.strip("'\"`")
    if not value or value[0] in "$%{<":
        return None
    return value


def test_flask_run_callers_use_the_factory():
    """A stale ``FLASK_APP`` serves an uninitialized runtime (PR-1, GA-1).

    Every tracked file is scanned, not a caller list, so a new caller cannot
    be added without either the factory target or a failing test. Assignments
    of a variable (the ``.ps1``'s save/restore of ``$env:FLASK_APP``) are not
    targets and are skipped.
    """
    listing = subprocess.run(
        ["git", "ls-files", "-z"], cwd=str(ROOT), capture_output=True, timeout=120,
    )
    assert listing.returncode == 0, f"git ls-files failed: {listing.stderr.decode(errors='replace')}"
    tracked = [name for name in listing.stdout.decode("utf-8").split("\0") if name]
    this_file = Path(__file__).resolve().relative_to(ROOT).as_posix()
    assert {"app.py", ".vscode/launch.json", "e2e/run_puppeteer_summary_regression.ps1"} <= set(tracked)

    violations: list[str] = []
    for name in tracked:
        if name == this_file or name.startswith(_EXCLUDED_PREFIXES):
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" in data or (b"FLASK_APP" not in data and b"--app" not in data):
            continue
        for number, line in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1):
            for match in _FLASK_APP_ASSIGNMENT.finditer(line):
                target = _literal_target(match.group("value") or match.group("setenv") or "")
                if target is not None and target != FACTORY_TARGET:
                    violations.append(f"{name}:{number}: FLASK_APP -> {target}")
            for match in _APP_OPTION.finditer(line):
                target = _literal_target(match.group("value"))
                if target is not None and target != FACTORY_TARGET:
                    violations.append(f"{name}:{number}: --app {target}")

    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    if re.search(r"flask\s+run\s+--reload", app_source):
        violations.append("app.py recommends `flask run --reload`")
    assert violations == []

    # The two known callers must name the factory, not merely avoid a stale value.
    launch_text = (ROOT / ".vscode" / "launch.json").read_text(encoding="utf-8")
    launch = json.loads("\n".join(
        line for line in launch_text.splitlines() if not line.lstrip().startswith("//")
    ))
    flask_configs = [config for config in launch["configurations"] if config.get("module") == "flask"]
    assert flask_configs and all(config["env"]["FLASK_APP"] == FACTORY_TARGET for config in flask_configs)
    runner = (ROOT / "e2e" / "run_puppeteer_summary_regression.ps1").read_text(encoding="utf-8")
    assert f'$env:FLASK_APP = "{FACTORY_TARGET}"' in runner
