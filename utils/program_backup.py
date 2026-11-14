"""
Program Backup / Program Library functionality.

Provides snapshot and restore capabilities for the active workout program.
Backups are stored in the program_backups and program_backup_items tables of the
application database. They do not survive Erase All Data: both tables are in
OWNED_TABLES_DROP_ORDER (utils/schema_registry.py) and are dropped with the rest of
the user data. What an erase leaves behind is the whole-database file snapshots in
the auto_backup directory beside the database file (utils/auto_backup.py):
erase_data() writes one first unless the database is missing or holds fewer than
100 exercises, and earlier startup snapshots stay. They have no in-application
restore.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from utils.backup_execution_contract import check_execution_fields, render_value
from utils.database import DatabaseHandler
from utils.logger import get_logger
from utils.workout_validation import validate_workout_bounds

logger = get_logger()

# Reserved informational label for a backup's payload shape (Testing Strategy D6,
# ADR-008). It is persisted to program_backups.schema_version and returned by the
# API, but nothing reads it to make a decision: restore_backup() is deliberately
# version-blind. It tells a missing value from a present one by the stored value
# (a column added by migration reads NULL on every older row), and it leaves out
# of its INSERT any optional column the destination user_selection lacks.
#
# Changing the program_backup_items payload shape requires all three of:
#   1. bump this constant;
#   2. add an ALTER-based migration in initialize_backup_tables() -- the loop
#      over _EXECUTION_ITEM_COLUMNS is the reference shape;
#   3. add the matching branch in restore_backup().
#
# Version 2 (#567) is the first bump that tracks a payload change: it added the
# four execution columns with all three parts. Version 1 does not identify one
# shape -- commit 6b99535 added superset_group with (2) and (3) but without the
# bump -- so a version-1 backup may or may not carry superset_group, and never
# carries the execution columns.
BACKUP_SCHEMA_VERSION = 2

# The four execution fields of a plan row, as (column, declared type). In
# program_backup_items all four are nullable and default to NULL -- never to
# 'standard'. NULL means "missing", which is how a row saved before version 2
# reads (ADR-015).
_EXECUTION_ITEM_COLUMNS = (
    ("execution_style", "TEXT"),
    ("time_cap_seconds", "INTEGER"),
    ("emom_interval_seconds", "INTEGER"),
    ("emom_rounds", "INTEGER"),
)
_EXECUTION_COLUMN_NAMES = tuple(name for name, _ in _EXECUTION_ITEM_COLUMNS)

# The plan-row columns a backup item carries. The first eight exist in every
# user_selection; the rest are added to it by migration, so a backup or a
# restore can meet a user_selection without them.
_REQUIRED_PLAN_COLUMNS = (
    "routine", "exercise", "sets", "min_rep_range", "max_rep_range",
    "rir", "rpe", "weight",
)
_OPTIONAL_PLAN_COLUMNS = ("exercise_order", "superset_group") + _EXECUTION_COLUMN_NAMES

# What restore writes for a row whose execution style is missing.
_MISSING_STYLE_RESTORED_AS = "standard"


class BackupRestoreRefused(Exception):
    """A backup holds an execution value restore cannot interpret (ADR-015).

    Raised by restore_backup() before it issues any write, so the active plan,
    the workout log and the backup are exactly as they were.

    Derives from Exception directly, never from ValueError: the restore route
    answers ValueError as NOT_FOUND.

    Attributes:
        backup_name: Name of the refused backup.
        rows: One ``{routine, exercise, field, value, problem}`` entry per
            problem, in backup order, every value already rendered to text.
        row_count: Number of backup rows that have at least one problem. A row
            with two problems has two entries in ``rows`` and counts once.
    """

    def __init__(self, backup_name: str, rows: List[Dict[str, str]], row_count: int) -> None:
        super().__init__(
            f"Backup '{backup_name}' was not restored: {row_count} row(s) hold "
            "execution settings that cannot be restored"
        )
        self.backup_name = backup_name
        self.rows = rows
        self.row_count = row_count


def initialize_backup_tables(db: Optional[DatabaseHandler] = None) -> None:
    """Create the backup tables if they don't exist.
    
    Creates two tables:
    - program_backups: Header/metadata for each backup
    - program_backup_items: Individual items (user_selection rows) for each backup
    """
    should_close = False
    if db is None:
        db = DatabaseHandler()
        should_close = True
    
    try:
        # Create backup header table
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS program_backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                note TEXT,
                backup_type TEXT NOT NULL DEFAULT 'manual',
                schema_version INTEGER NOT NULL DEFAULT 1,
                item_count INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name, created_at)
            )
        """)
        
        # Create backup items table with FK to header
        db.execute_query("""
            CREATE TABLE IF NOT EXISTS program_backup_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backup_id INTEGER NOT NULL,
                routine TEXT NOT NULL,
                exercise TEXT NOT NULL,
                sets INTEGER NOT NULL,
                min_rep_range INTEGER NOT NULL,
                max_rep_range INTEGER NOT NULL,
                rir INTEGER,
                rpe REAL,
                weight REAL NOT NULL,
                exercise_order INTEGER,
                superset_group TEXT DEFAULT NULL,
                execution_style TEXT DEFAULT NULL,
                time_cap_seconds INTEGER DEFAULT NULL,
                emom_interval_seconds INTEGER DEFAULT NULL,
                emom_rounds INTEGER DEFAULT NULL,
                FOREIGN KEY (backup_id) REFERENCES program_backups(id) ON DELETE CASCADE
            )
        """)

        # Add superset_group column if it doesn't exist (migration for existing backup tables)
        cols = db.fetch_all("PRAGMA table_info(program_backup_items)")
        col_names = {row['name'] for row in cols}
        if 'superset_group' not in col_names:
            db.execute_query("ALTER TABLE program_backup_items ADD COLUMN superset_group TEXT DEFAULT NULL")
            logger.debug("Added superset_group column to program_backup_items table")

        # Add the four execution columns to an existing backup table (schema
        # version 2). They default to NULL -- execution_style included, never
        # 'standard' -- so rows saved before the change read as missing and no
        # existing row or header is rewritten.
        for column, declared_type in _EXECUTION_ITEM_COLUMNS:
            if column not in col_names:
                db.execute_query(
                    f"ALTER TABLE program_backup_items ADD COLUMN {column} {declared_type} DEFAULT NULL"
                )
                logger.debug(f"Added {column} column to program_backup_items table")

        # Create indexes for efficient lookups
        db.execute_query("""
            CREATE INDEX IF NOT EXISTS idx_backup_items_backup_id 
            ON program_backup_items(backup_id)
        """)
        
        db.execute_query("""
            CREATE INDEX IF NOT EXISTS idx_backups_type 
            ON program_backups(backup_type)
        """)
        
        db.execute_query("""
            CREATE INDEX IF NOT EXISTS idx_backups_created_at 
            ON program_backups(created_at DESC)
        """)
        
        logger.debug("Backup tables initialized successfully")
    except sqlite3.Error:
        logger.exception("Failed to initialize backup tables")
        raise
    finally:
        if should_close:
            db.close()


def _get_column_names(db: DatabaseHandler, table: str) -> Set[str]:
    """Return the names of a table's columns; empty if they cannot be read."""
    try:
        columns = db.fetch_all(f"PRAGMA table_info({table})")
        return {col['name'] for col in columns}
    except sqlite3.Error:
        return set()


def create_backup(
    name: str,
    note: Optional[str] = None,
    backup_type: str = "manual",
    db: Optional[DatabaseHandler] = None
) -> Dict[str, Any]:
    """
    Create a backup (snapshot) of the current active program.
    
    Args:
        name: Required name for the backup
        note: Optional note/description
        backup_type: 'manual' (user-initiated) or 'auto' (system-initiated)
        db: Optional shared database handler for callers managing a transaction
    
    Returns:
        Dict with backup metadata including id, name, item_count, etc.
    
    Raises:
        ValueError: If name is empty
        sqlite3.Error: On database errors
    """
    if not name or not name.strip():
        raise ValueError("Backup name is required")

    name = name.strip()
    if len(name) > 100:
        raise ValueError("Backup name must be 100 characters or fewer")

    if note is not None:
        note = note.strip()
        if len(note) > 500:
            raise ValueError("Backup note must be 500 characters or fewer")
        note = note or None
    
    should_close = False
    if db is None:
        db = DatabaseHandler()
        db.__enter__()
        should_close = True

    # When we own the connection, wrap the header insert and all item inserts
    # in a single transaction (mirrors restore_backup's BEGIN IMMEDIATE /
    # commit / rollback shape) so a crash mid-insert leaves no partial
    # backup. When a caller supplies its own `db`, that caller owns the
    # transaction (e.g. a caller that already holds a BEGIN IMMEDIATE), so we
    # just write uncommitted and let it commit.
    own_transaction = should_close

    try:
        if own_transaction:
            db.execute_query("BEGIN IMMEDIATE", commit=False)

        # Check if user_selection table exists
        table_check = db.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user_selection'"
        )
        if not table_check:
            logger.warning("user_selection table does not exist, creating empty backup")
            items = []
        else:
            # Select every optional column user_selection has. One it lacks is
            # stored as NULL in the backup item.
            plan_columns = _get_column_names(db, 'user_selection')
            has_order = 'exercise_order' in plan_columns
            select_cols = ", ".join(
                _REQUIRED_PLAN_COLUMNS
                + tuple(col for col in _OPTIONAL_PLAN_COLUMNS if col in plan_columns)
            )
            order_clause = "ORDER BY exercise_order, routine, exercise" if has_order else "ORDER BY routine, exercise"

            # Fetch all items from active program. Values are copied as stored:
            # nothing is validated or normalized at backup time.
            items = db.fetch_all(f"""
                SELECT {select_cols}
                FROM user_selection
                {order_clause}
            """)
        
        item_count = len(items)
        
        # Create backup header
        db.execute_query("""
            INSERT INTO program_backups (name, note, backup_type, schema_version, item_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, note, backup_type, BACKUP_SCHEMA_VERSION, item_count, datetime.now()), commit=False)
        
        # Get the newly created backup ID
        result = db.fetch_one("SELECT last_insert_rowid() as id")
        if not result:
            raise RuntimeError("Failed to retrieve backup ID after insert")
        backup_id = result['id']
        
        # Insert all items
        if items:
            for item in items:
                db.execute_query("""
                    INSERT INTO program_backup_items 
                    (backup_id, routine, exercise, sets, min_rep_range, max_rep_range,
                     rir, rpe, weight, exercise_order, superset_group,
                     execution_style, time_cap_seconds, emom_interval_seconds, emom_rounds)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    backup_id,
                    item.get('routine'),
                    item.get('exercise'),
                    item.get('sets'),
                    item.get('min_rep_range'),
                    item.get('max_rep_range'),
                    item.get('rir'),
                    item.get('rpe'),
                    item.get('weight'),
                    # Each of the six below is None if user_selection lacks the column
                    item.get('exercise_order'),
                    item.get('superset_group'),
                    item.get('execution_style'),
                    item.get('time_cap_seconds'),
                    item.get('emom_interval_seconds'),
                    item.get('emom_rounds'),
                ), commit=False)

        if own_transaction:
            db.connection.commit()

        logger.info(
            "Backup created successfully",
            extra={
                'backup_id': backup_id,
                'backup_name': name,
                'backup_type': backup_type,
                'item_count': item_count
            }
        )
        
        return {
            'id': backup_id,
            'name': name,
            'note': note,
            'backup_type': backup_type,
            'schema_version': BACKUP_SCHEMA_VERSION,
            'item_count': item_count,
            'created_at': datetime.now().isoformat()
        }
    except BaseException as exc:
        if own_transaction:
            db.connection.rollback()
        if should_close:
            db.__exit__(type(exc), exc, exc.__traceback__)
            should_close = False
        raise
    finally:
        if should_close:
            db.__exit__(None, None, None)


def update_backup_metadata(
    backup_id: int,
    name: Optional[str] = None,
    note: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Update the editable metadata for a backup.

    Args:
        backup_id: The ID of the backup to update
        name: Optional new backup name
        note: Optional new backup note

    Returns:
        Updated backup metadata, or None if the backup does not exist

    Raises:
        ValueError: If neither field is provided or validation fails
        sqlite3.Error: On database errors
    """
    if name is None and note is None:
        raise ValueError("At least one of 'name' or 'note' must be provided")

    with DatabaseHandler() as db:
        existing = db.fetch_one(
            """
            SELECT id, name, note, backup_type, schema_version, item_count, created_at
            FROM program_backups
            WHERE id = ?
            """,
            (backup_id,),
        )

        if not existing:
            return None

        updates = []
        params = []

        if name is not None:
            normalized_name = name.strip()
            if not normalized_name:
                raise ValueError("Backup name is required")
            if len(normalized_name) > 100:
                raise ValueError("Backup name must be 100 characters or fewer")
            updates.append("name = ?")
            params.append(normalized_name)

        if note is not None:
            normalized_note = note.strip()
            if len(normalized_note) > 500:
                raise ValueError("Backup note must be 500 characters or fewer")
            updates.append("note = ?")
            params.append(normalized_note or None)

        db.execute_query(
            f"UPDATE program_backups SET {', '.join(updates)} WHERE id = ?",
            tuple(params + [backup_id]),
        )

        row = db.fetch_one(
            """
            SELECT id, name, note, backup_type, schema_version, item_count, created_at
            FROM program_backups
            WHERE id = ?
            """,
            (backup_id,),
        )

        return dict(row) if row else None


def list_backups() -> List[Dict[str, Any]]:
    """
    List all saved program backups.
    
    Returns:
        List of backup metadata dicts, ordered by created_at DESC
    """
    with DatabaseHandler() as db:
        backups = db.fetch_all("""
            SELECT id, name, note, backup_type, schema_version, item_count, created_at
            FROM program_backups
            ORDER BY created_at DESC
        """)
        
        return [dict(b) for b in backups]


def get_backup_details(backup_id: int) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific backup, including its items.
    
    Args:
        backup_id: The ID of the backup to retrieve
    
    Returns:
        Dict with backup metadata and items, or None if not found
    """
    with DatabaseHandler() as db:
        # Get backup header
        backup = db.fetch_one("""
            SELECT id, name, note, backup_type, schema_version, item_count, created_at
            FROM program_backups
            WHERE id = ?
        """, (backup_id,))
        
        if not backup:
            return None
        
        # Get backup items
        items = db.fetch_all("""
            SELECT routine, exercise, sets, min_rep_range, max_rep_range, 
                   rir, rpe, weight, exercise_order, superset_group
            FROM program_backup_items
            WHERE backup_id = ?
            ORDER BY exercise_order, routine, exercise
        """, (backup_id,))
        
        result = dict(backup)
        result['items'] = [dict(item) for item in items]
        
        return result


def _validate_restore_item(item: Dict[str, Any]) -> Optional[str]:
    """Return a user-facing reason a backup item cannot be restored, or ``None``.

    Applies the canonical ``validate_workout_bounds`` contract to the four bounded
    columns. ``rir`` is the only nullable one in program_backup_items, so it is
    omitted -- left UNSET -- when and only when it is exactly ``None``; an empty
    string stays present and is rejected. ``allow_null`` is deliberately not used:
    it maps ``""`` onto null, which would let a blank pass the bounds check and
    then land in a NOT NULL column under SQLite's type affinity.
    """
    fields: Dict[str, Any] = {
        'weight': item.get('weight'),
        'min_reps': item.get('min_rep_range'),
        'max_reps': item.get('max_rep_range'),
    }
    rir = item.get('rir')
    if rir is not None:
        fields['rir'] = rir

    return validate_workout_bounds(**fields, allow_null=False)


def _as_text(value: Any) -> str:
    """A routine or exercise name as text for a refusal row.

    Names are stored as text and returned unchanged. Anything else -- reachable
    only by editing the database outside the application -- is rendered, so the
    row is always JSON-safe.
    """
    return value if isinstance(value, str) else render_value(value)


def _restore_value(item: Dict[str, Any], column: str) -> Any:
    """The value restore writes to ``column`` of user_selection for ``item``.

    Every value is written as stored, with one exception: a missing execution
    style is written as 'standard'. A missing timing value stays NULL -- restore
    never fills in a default.
    """
    value = item.get(column)
    if column == 'execution_style' and value is None:
        return _MISSING_STYLE_RESTORED_AS
    return value


def restore_backup(backup_id: int) -> Dict[str, Any]:
    """
    Restore a backup to the active program (replace mode).

    Every decision is made before anything is written. Each backup item is
    classified, in backup order:

    1. its exercise is not in the catalog: skipped, reported in ``skipped``;
    2. its weight, rep range or RIR fails the plan's bounds: skipped, reported
       in ``invalid``;
    3. otherwise it is restorable, and its four execution fields are checked
       against the restore-acceptance contract
       (utils/backup_execution_contract.py, ADR-015).

    If any restorable item holds an execution value the contract does not
    accept, the whole restore is refused and nothing is written. Otherwise one
    transaction clears workout_log and user_selection and inserts every
    restorable item. A missing execution style is restored as 'standard'; a
    missing timing value is restored empty.

    Args:
        backup_id: The ID of the backup to restore

    Returns:
        Dict with restore results:
        - backup_id: ID of the restored backup
        - backup_name: Name of the restored backup
        - restored_count: Number of items restored
        - skipped: Exercises skipped because they are missing from the catalog
        - invalid: Items skipped because a bounded value is out of range, each
          ``{routine, exercise, reason}``

    Raises:
        ValueError: If backup_id is invalid
        BackupRestoreRefused: If a restorable item holds an execution value the
            contract does not accept. Raised before any write.
    """
    with DatabaseHandler() as db:
        # Verify backup exists
        backup = db.fetch_one("""
            SELECT id, name, item_count
            FROM program_backups
            WHERE id = ?
        """, (backup_id,))

        if not backup:
            raise ValueError(f"Backup with id {backup_id} not found")

        backup_name = backup['name']

        # Get backup items
        items = db.fetch_all("""
            SELECT routine, exercise, sets, min_rep_range, max_rep_range,
                   rir, rpe, weight, exercise_order, superset_group,
                   execution_style, time_cap_seconds, emom_interval_seconds, emom_rounds
            FROM program_backup_items
            WHERE backup_id = ?
        """, (backup_id,))

        # Get list of valid exercises from catalog
        valid_exercises = db.fetch_all("""
            SELECT exercise_name FROM exercises
        """)
        valid_exercise_names = {row['exercise_name'] for row in valid_exercises}

        # An optional column the destination lacks is left out of the INSERT.
        # The column list comes only from the two fixed tuples, never from
        # input, and the placeholders and each row's parameters are built from
        # this same list, so their order cannot drift apart.
        destination_columns = _get_column_names(db, 'user_selection')
        insert_columns = _REQUIRED_PLAN_COLUMNS + tuple(
            column for column in _OPTIONAL_PLAN_COLUMNS if column in destination_columns
        )
        insert_sql = (
            f"INSERT INTO user_selection ({', '.join(insert_columns)}) "
            f"VALUES ({', '.join('?' for _ in insert_columns)})"
        )

        # Pre-flight: classify every item before anything is written.
        restorable: List[Dict[str, Any]] = []
        skipped: List[Any] = []
        invalid: List[Dict[str, Any]] = []
        refused_rows: List[Dict[str, str]] = []
        refused_row_count = 0

        for item in items:
            exercise_name = item.get('exercise')

            # Check if exercise exists in catalog (FK constraint)
            if exercise_name not in valid_exercise_names:
                skipped.append(exercise_name)
                logger.warning(
                    f"Skipping exercise during restore: '{exercise_name}' not in catalog"
                )
                continue

            # A backup predating validate_workout_bounds can carry values the plan
            # routes reject. Skip that row rather than writing it: a non-numeric rep
            # range reaches six downstream sites, where it can cause failures and
            # silent miscalculation (FINDING-1).
            bounds_error = _validate_restore_item(item)
            if bounds_error:
                invalid.append({
                    'routine': item.get('routine'),
                    'exercise': exercise_name,
                    'reason': bounds_error,
                })
                logger.warning(
                    "Skipping exercise during restore: invalid bounds",
                    extra={'exercise': exercise_name, 'reason': bounds_error},
                )
                continue

            # Only a row that would be written can refuse the restore: a row
            # skipped above never has its execution fields examined.
            problems = check_execution_fields(item)
            if problems:
                refused_row_count += 1
                for problem in problems:
                    refused_rows.append({
                        'routine': _as_text(item.get('routine')),
                        'exercise': _as_text(exercise_name),
                        **problem,
                    })
                continue

            restorable.append(item)

        if refused_rows:
            # Raised before BEGIN IMMEDIATE: no write statement has been issued,
            # so the plan and the log keep their rows and their ids.
            logger.warning(
                "Backup restore refused: execution values cannot be restored",
                extra={
                    'backup_id': backup_id,
                    'backup_name': backup_name,
                    'refused_row_count': refused_row_count,
                    'problem_count': len(refused_rows),
                },
            )
            raise BackupRestoreRefused(backup_name, refused_rows, refused_row_count)

        try:
            db.execute_query("BEGIN IMMEDIATE", commit=False)

            # Clear current active program (user_selection)
            # FK CASCADE from user_selection also clears workout_log; explicit DELETE documents intent.
            db.execute_query("DELETE FROM workout_log", commit=False)
            db.execute_query("DELETE FROM user_selection", commit=False)

            # One INSERT per row, never executemany.
            for item in restorable:
                db.execute_query(
                    insert_sql,
                    tuple(_restore_value(item, column) for column in insert_columns),
                    commit=False,
                )
            db.connection.commit()
        except sqlite3.Error:
            db.connection.rollback()
            raise

        restored_count = len(restorable)

        # Normalize skipped entries while preserving order
        skipped_unique = list(dict.fromkeys(skipped))

        logger.info(
            "Backup restored successfully",
            extra={
                'backup_id': backup_id,
                'backup_name': backup_name,
                'restored_count': restored_count,
                'skipped_count': len(skipped_unique),
                'invalid_count': len(invalid)
            }
        )

        return {
            'backup_id': backup_id,
            'backup_name': backup_name,
            'restored_count': restored_count,
            'skipped': skipped_unique,
            'invalid': invalid
        }


def delete_backup(backup_id: int) -> bool:
    """
    Delete a backup and all its items.
    
    Args:
        backup_id: The ID of the backup to delete
    
    Returns:
        True if deletion was successful, False if backup not found
    """
    with DatabaseHandler() as db:
        # Check if backup exists
        backup = db.fetch_one("""
            SELECT id, name FROM program_backups WHERE id = ?
        """, (backup_id,))
        
        if not backup:
            logger.warning(f"Attempted to delete non-existent backup: {backup_id}")
            return False
        
        backup_name = backup['name']
        
        # Delete backup items first (cascading delete should handle this, but be explicit)
        db.execute_query("""
            DELETE FROM program_backup_items WHERE backup_id = ?
        """, (backup_id,))
        
        # Delete backup header
        db.execute_query("""
            DELETE FROM program_backups WHERE id = ?
        """, (backup_id,))
        
        logger.info(
            "Backup deleted successfully",
            extra={
                'backup_id': backup_id,
                'backup_name': backup_name
            }
        )
        
        return True


def prune_auto_backups(keep_count: int = 10, db: Optional[DatabaseHandler] = None) -> int:
    """Delete auto-backups beyond the latest keep_count. Manual backups are never touched.

    Returns the number of rows deleted.
    """
    should_close = False
    if db is None:
        db = DatabaseHandler()
        db.__enter__()
        should_close = True

    try:
        rowcount = db.execute_query(
            """
            DELETE FROM program_backups
             WHERE backup_type = 'auto'
               AND id NOT IN (
                     SELECT id FROM program_backups
                      WHERE backup_type = 'auto'
                      ORDER BY created_at DESC
                      LIMIT ?
                   )
            """,
            (keep_count,),
            commit=should_close,
        )
        logger.info("Pruned auto-backups", extra={'kept': keep_count, 'deleted': rowcount})
        return rowcount
    except BaseException as exc:
        if should_close:
            db.__exit__(type(exc), exc, exc.__traceback__)
            should_close = False
        raise
    finally:
        if should_close:
            db.__exit__(None, None, None)


def get_latest_auto_backup() -> Optional[Dict[str, Any]]:
    """
    Get the most recent auto-backup.
    
    Returns:
        Backup metadata dict or None if no auto-backups exist
    """
    with DatabaseHandler() as db:
        backup = db.fetch_one("""
            SELECT id, name, note, backup_type, schema_version, item_count, created_at
            FROM program_backups
            WHERE backup_type = 'auto'
            ORDER BY created_at DESC
            LIMIT 1
        """)
        
        return dict(backup) if backup else None


def get_active_program_count() -> int:
    """
    Get the number of items in the current active program.
    
    Returns:
        Number of items in user_selection, or 0 if table doesn't exist
    """
    with DatabaseHandler() as db:
        table_check = db.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user_selection'"
        )
        
        if not table_check:
            return 0
        
        result = db.fetch_one("SELECT COUNT(*) as count FROM user_selection")
        return result['count'] if result else 0
