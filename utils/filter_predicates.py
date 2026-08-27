"""
Consolidated filtering module for exercises.
Single source of truth for all exercise filtering logic.
"""

from utils.database import DatabaseHandler
from utils.logger import get_logger
from typing import Any, Dict, List, Optional, Sequence, Tuple, TypeGuard, Union

logger = get_logger()

# A result row as this module accepts it: positional (tuple) or keyed (dict).
# DatabaseHandler.fetch_all() only ever returns the keyed shape - it converts every
# sqlite3.Row with dict(). The positional shape reaches filter_exercises through a
# substituted handler, and is pinned by tests/test_filter_predicates.py:237 and :292.
ExerciseRow = Union[Tuple[Any, ...], Dict[str, Any]]


class FilterPredicates:
    """
    Centralized filtering predicates for exercises.
    Consolidates logic from utils/filters.py and utils/exercise_manager.py.
    """
    
    # Valid filterable fields
    VALID_FILTER_FIELDS = {
        "primary_muscle_group",
        "secondary_muscle_group", 
        "tertiary_muscle_group",
        "advanced_isolated_muscles",
        "force",
        "equipment",
        "mechanic",
        "difficulty",
        "target_muscles",
        "utility",
        "grips",
        "stabilizers",
        "synergists"
    }
    
    # Fields that should use LIKE operator (for partial matching)
    PARTIAL_MATCH_FIELDS = {
        "primary_muscle_group",
        "secondary_muscle_group",
        "tertiary_muscle_group",
        "advanced_isolated_muscles",
        "grips",
        "stabilizers",
        "synergists"
    }
    
    @classmethod
    def build_filter_query(
        cls, 
        filters: Optional[Dict[str, str]] = None,
        base_query: str = "SELECT exercise_name FROM exercises WHERE 1=1"
    ) -> Tuple[str, List[str]]:
        """
        Build a SQL query with filter conditions.
        
        Args:
            filters: Dictionary of filter criteria {field: value}
            base_query: Base SQL query to append conditions to
            
        Returns:
            Tuple of (query_string, params_list)
        """
        query = base_query
        params = []
        
        if not filters:
            query += " ORDER BY exercise_name ASC"
            return query, params
        
        conditions = []
        
        for field, value in filters.items():
            # Validate field
            if field not in cls.VALID_FILTER_FIELDS:
                continue
                
            if not value:  # Skip empty values
                continue
            
            # Special handling for advanced_isolated_muscles - use mapping table
            if field == "advanced_isolated_muscles":
                conditions.append("""
                    EXISTS (
                        SELECT 1
                        FROM exercise_isolated_muscles m
                        WHERE m.exercise_name = exercises.exercise_name
                          AND m.muscle LIKE ?
                    )
                """)
                params.append(f"%{value}%")
            # Use LIKE for partial matching fields, exact match for others
            elif field in cls.PARTIAL_MATCH_FIELDS:
                conditions.append(f"{field} LIKE ?")
                params.append(f"%{value}%")
            else:
                conditions.append(f"LOWER({field}) = LOWER(?)")
                params.append(value)
        
        if conditions:
            query += " AND " + " AND ".join(conditions)
        
        query += " ORDER BY exercise_name ASC"
        
        return query, params
    
    @staticmethod
    def _rows_are_tuples(
        rows: Sequence[ExerciseRow],
    ) -> TypeGuard[Sequence[Tuple[Any, ...]]]:
        """Whether the result set uses positional (tuple) rows.

        Declared as a ``TypeGuard`` rather than a ``TypeIs``: an empty sequence
        is a valid ``Sequence[Tuple[Any, ...]]`` yet returns False here, so the
        negative branch says nothing about the argument's type.
        """
        return bool(rows) and isinstance(rows[0], tuple)

    @staticmethod
    def _rows_are_dicts(
        rows: Sequence[ExerciseRow],
    ) -> TypeGuard[Sequence[Dict[str, Any]]]:
        """Whether the result set uses keyed (dict) rows. See _rows_are_tuples."""
        return bool(rows) and isinstance(rows[0], dict)

    @classmethod
    def _exercise_names(cls, rows: Sequence[ExerciseRow]) -> List[str]:
        """Pull exercise names out of either supported row shape.

        The shape is decided once, from the first row, and every row is then
        read that way, so a mixed result set raises rather than returning a
        partial list.
        """
        if cls._rows_are_tuples(rows):
            return [row[0] for row in rows if row[0]]
        elif cls._rows_are_dicts(rows):
            return [row["exercise_name"] for row in rows if row.get("exercise_name")]
        return []

    @classmethod
    def filter_exercises(cls, filters: Optional[Dict[str, str]] = None) -> List[str]:
        """
        Filter exercises based on provided criteria.
        
        Args:
            filters: Dictionary containing filter criteria
            
        Returns:
            List of exercise names matching the criteria
        """
        query, params = cls.build_filter_query(filters)
        
        try:
            with DatabaseHandler() as db:
                results = db.fetch_all(query, params if params else None)
                return cls._exercise_names(results)
        except Exception as e:
            logger.exception("Error filtering exercises: %s", e)
            return []
    
    @classmethod
    def get_exercises(cls, filters: Optional[Dict[str, str]] = None) -> List[str]:
        """
        Fetch exercises from the database, optionally filtered.
        Alias for filter_exercises for backward compatibility.
        
        Args:
            filters: Dictionary containing filter criteria
            
        Returns:
            List of exercise names
        """
        return cls.filter_exercises(filters)
    
    @classmethod
    def validate_filter_field(cls, field: str) -> bool:
        """
        Check if a field is valid for filtering.
        
        Args:
            field: Field name to validate
            
        Returns:
            True if field is valid for filtering
        """
        return field in cls.VALID_FILTER_FIELDS
    
    @classmethod
    def sanitize_filters(cls, filters: Dict[str, str]) -> Dict[str, str]:
        """
        Remove invalid fields from filter dictionary.
        
        Args:
            filters: Raw filter dictionary
            
        Returns:
            Sanitized filter dictionary with only valid fields
        """
        return {
            field: value 
            for field, value in filters.items() 
            if field in cls.VALID_FILTER_FIELDS and value
        }


# Convenience functions for backward compatibility
def filter_exercises(filters: Optional[Dict[str, str]] = None) -> List[str]:
    """Filter exercises based on provided criteria."""
    return FilterPredicates.filter_exercises(filters)


def get_exercises(filters: Optional[Dict[str, str]] = None) -> List[str]:
    """Fetch exercises from the database, optionally filtered."""
    return FilterPredicates.get_exercises(filters)


def build_filter_query(
    filters: Optional[Dict[str, str]] = None,
    base_query: str = "SELECT exercise_name FROM exercises WHERE 1=1"
) -> Tuple[str, List[str]]:
    """Build a SQL query with filter conditions."""
    return FilterPredicates.build_filter_query(filters, base_query)
