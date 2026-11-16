"""
Program Backup / Program Library API routes.

Provides endpoints for creating, listing, restoring, deleting, and browsing
program backups.
"""
from flask import Blueprint, request, jsonify, render_template
from utils.errors import success_response, error_response, validation_error_response
from utils.logger import get_logger
from utils.program_backup import (
    BackupRestoreRefused,
    create_backup,
    list_backups,
    get_backup_details,
    restore_backup,
    delete_backup,
    update_backup_metadata,
    get_active_program_count,
    initialize_backup_tables,
)

program_backup_bp = Blueprint('program_backup', __name__)
logger = get_logger()


@program_backup_bp.route('/backup', methods=['GET'])
def backup_center():
    """Render the dedicated backup center page."""
    try:
        backups = list_backups()
        manual_backups = [backup for backup in backups if backup.get('backup_type') != 'auto']
        auto_backups = [backup for backup in backups if backup.get('backup_type') == 'auto']

        return render_template(
            'backup.html',
            active_program_count=get_active_program_count(),
            initial_backup_count=len(backups),
            initial_manual_count=len(manual_backups),
            initial_auto_count=len(auto_backups),
            latest_manual_backup=manual_backups[0] if manual_backups else None,
            latest_auto_backup=auto_backups[0] if auto_backups else None,
        )
    except Exception:
        logger.exception("Error loading backup center page")
        return render_template(
            "error.html",
            error_title="Server Error",
            error_code=500,
            error_message="Unable to load backup center.",
        ), 500


@program_backup_bp.route('/api/backups', methods=['GET'])
def api_list_backups():
    """
    List all saved program backups.
    
    Returns:
        JSON list of backup metadata objects with:
        - id: Backup ID
        - name: Backup name
        - note: Optional note
        - backup_type: 'manual' or 'auto'
        - item_count: Number of exercises in backup
        - created_at: Timestamp
    """
    try:
        backups = list_backups()
        logger.debug(f"Listed {len(backups)} backups")
        return jsonify(success_response(data=backups))
    except Exception as e:
        logger.exception("Error listing backups")
        return error_response("INTERNAL_ERROR", "Failed to list backups", 500)


@program_backup_bp.route('/api/backups', methods=['POST'])
def api_create_backup():
    """
    Create a new backup of the current active program.
    
    Request body:
        {
            "name": "My Backup Name" (required),
            "note": "Optional description"
        }
    
    Returns:
        JSON with backup metadata including id, name, item_count
    """
    try:
        data = request.get_json()
        if not data:
            return error_response("VALIDATION_ERROR", "No data provided", 400)
        
        name = data.get('name', '').strip()
        if not name:
            return error_response("VALIDATION_ERROR", "Backup name is required", 400)
        
        note = data.get('note')
        
        logger.info(
            "Creating backup",
            extra={'backup_name': name, 'has_note': bool(note)}
        )
        
        backup = create_backup(name=name, note=note, backup_type='manual')
        
        return jsonify(success_response(
            data=backup,
            message=f"Backup '{name}' created successfully with {backup['item_count']} exercises"
        ))
        
    except ValueError as e:
        logger.warning(f"Validation error creating backup: {e}")
        return validation_error_response(e)
    except Exception as e:
        logger.exception("Error creating backup")
        return error_response("INTERNAL_ERROR", "Failed to create backup", 500)


@program_backup_bp.route('/api/backups/<int:backup_id>', methods=['GET'])
def api_get_backup(backup_id: int):
    """
    Get detailed information about a specific backup.
    
    Args:
        backup_id: The ID of the backup to retrieve
    
    Returns:
        JSON with backup metadata and list of items
    """
    try:
        backup = get_backup_details(backup_id)
        
        if not backup:
            return error_response("NOT_FOUND", f"Backup with id {backup_id} not found", 404)
        
        return jsonify(success_response(data=backup))
        
    except Exception as e:
        logger.exception(f"Error getting backup details for id {backup_id}")
        return error_response("INTERNAL_ERROR", "Failed to get backup details", 500)


def _restore_refused_message(refused: BackupRestoreRefused) -> str:
    """Build the refusal message; it names every problem because the Backup Center shows nothing else."""
    named_rows = "; ".join(
        f"{row['routine']} / {row['exercise']}: {row['problem']}" for row in refused.rows
    )
    return (
        f"Backup '{refused.backup_name}' was not restored. Your current plan and workout "
        "log were preserved; nothing was changed. "
        f"{refused.row_count} row(s) hold execution settings that cannot be restored: "
        f"{named_rows}. "
        "The backup itself was left unchanged and cannot be restored until these values "
        "are corrected."
    )


@program_backup_bp.route('/api/backups/<int:backup_id>/restore', methods=['POST'])
def api_restore_backup(backup_id: int):
    """
    Restore a backup to the active program (replace mode).
    
    This will clear the current active program and load the backup.
    Any exercises that no longer exist in the catalog will be skipped.
    A backup holding an execution value restore cannot interpret is refused
    whole, with nothing changed (ADR-015).
    
    Args:
        backup_id: The ID of the backup to restore
    
    Returns:
        JSON with restore results:
        - restored_count: Number of items successfully restored
        - skipped: List of exercises that were skipped
        - invalid: List of rows skipped for an out-of-bounds value
        - backup_name: Name of the restored backup
        - backup_id: ID of the restored backup

        400 VALIDATION_ERROR with error.reason "RESTORE_REFUSED" and error.rows
        when the restore is refused.
    """
    try:
        logger.info(f"Restoring backup {backup_id}")
        
        result = restore_backup(backup_id)
        
        message = f"Restored {result['restored_count']} exercises from '{result['backup_name']}'"
        if result['skipped']:
            message += f" ({len(result['skipped'])} skipped due to missing exercises)"
        
        return jsonify(success_response(data=result, message=message))
        
    except BackupRestoreRefused as refused:
        # Must stay ahead of the ValueError branch, which answers NOT_FOUND.
        return error_response(
            "VALIDATION_ERROR",
            _restore_refused_message(refused),
            400,
            reason="RESTORE_REFUSED",
            rows=refused.rows,
        )
    except ValueError as e:
        logger.warning(f"Validation error restoring backup: {e}")
        return validation_error_response(e, "NOT_FOUND", 404)
    except Exception as e:
        logger.exception(f"Error restoring backup {backup_id}")
        return error_response("INTERNAL_ERROR", "Failed to restore backup", 500)


@program_backup_bp.route('/api/backups/<int:backup_id>', methods=['DELETE'])
def api_delete_backup(backup_id: int):
    """
    Delete a backup and all its items.
    
    Args:
        backup_id: The ID of the backup to delete
    
    Returns:
        JSON success response or 404 if not found
    """
    try:
        logger.info(f"Deleting backup {backup_id}")
        
        success = delete_backup(backup_id)
        
        if not success:
            return error_response("NOT_FOUND", f"Backup with id {backup_id} not found", 404)
        
        return jsonify(success_response(message="Backup deleted successfully"))
        
    except Exception as e:
        logger.exception(f"Error deleting backup {backup_id}")
        return error_response("INTERNAL_ERROR", "Failed to delete backup", 500)


@program_backup_bp.route('/api/backups/<int:backup_id>', methods=['PATCH'])
def api_update_backup(backup_id: int):
    """Update the editable metadata for a backup."""
    try:
        data = request.get_json() or {}
        if 'name' not in data and 'note' not in data:
            return error_response("VALIDATION_ERROR", "At least one of 'name' or 'note' must be provided", 400)

        name = data.get('name')
        note = data.get('note')

        try:
            updated = update_backup_metadata(backup_id, name=name, note=note)
        except ValueError as e:
            return validation_error_response(e)

        if updated is None:
            return error_response("NOT_FOUND", f"Backup with id {backup_id} not found", 404)

        return jsonify(success_response(data=updated, message="Backup updated"))
    except Exception:
        logger.exception(f"Error updating backup {backup_id}")
        return error_response("INTERNAL_ERROR", "Failed to update backup", 500)


# Initialize backup tables when blueprint is registered
def init_backup_tables():
    """Initialize backup tables. Called during app startup."""
    try:
        initialize_backup_tables()
        logger.info("Backup tables initialized")
    except Exception as e:
        logger.exception("Failed to initialize backup tables")
