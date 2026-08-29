"""Effective Sets Calculation Module.

This module provides the core logic for calculating effective (hypertrophy-relevant)
sets based on effort, rep range, and muscle contribution factors.

All outputs are descriptive, not prescriptive - calculations are informational
and never auto-adjust or block user intent.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple


# =============================================================================
# Enums & Constants
# =============================================================================

class CountingMode(Enum):
    """Toggle for raw vs effective set counting."""
    RAW = "raw"
    EFFECTIVE = "effective"


class ContributionMode(Enum):
    """Toggle for direct-only vs total (weighted) volume."""
    DIRECT_ONLY = "direct"
    TOTAL = "total"


class VolumeWarningLevel(Enum):
    """Session volume warning classification."""
    OK = "ok"
    BORDERLINE = "borderline"
    EXCESSIVE = "excessive"


def parse_counting_mode(value: Optional[str]) -> CountingMode:
    """Parse counting mode from a request/query value.

    Defaults to EFFECTIVE for missing or unrecognized values.
    """
    if value and value.lower() == "raw":
        return CountingMode.RAW
    return CountingMode.EFFECTIVE


def parse_contribution_mode(value: Optional[str]) -> ContributionMode:
    """Parse contribution mode from a request/query value.

    Defaults to TOTAL for missing or unrecognized values.
    """
    if value and value.lower() == "direct":
        return ContributionMode.DIRECT_ONLY
    return ContributionMode.TOTAL


# Effort factor buckets (RIR-based, discrete buckets)
# RIR 0-1: High effort (near failure) - full credit
# RIR 2-3: Moderate-high effort - slight reduction
# RIR 4-5: Moderate effort - moderate reduction  
# RIR 6+: Low effort - significant reduction (but not eliminated)
EFFORT_FACTOR_BUCKETS: Dict[Tuple[int, int], float] = {
    (0, 1): 1.0,     # Near failure - full stimulus
    (2, 3): 0.85,    # Moderate-high effort
    (4, 5): 0.70,    # Moderate effort
    (6, 10): 0.55,   # Low effort (not "junk" unless explicitly indicated)
}

# Rep range factor bands (coarse categories), keyed by the average of min/max.
# TOTAL over every positive average, per ADR-009 ruling 2 -- the bands leave no
# gap, so nothing in-domain falls through to the neutral default:
#   avg < 6        -> 0.85   Strength-focused (still hypertrophic, less optimal)
#   6 <= avg <= 20 -> 1.0    Optimal hypertrophy range
#   20 < avg <= 30 -> 0.85   Higher rep endurance work
#   avg > 30       -> 0.70   Very high rep (diminishing returns)
# Missing rep data, and a non-positive average, stay neutral at 1.0.
#
# These replaced disjoint integer buckets -- (1,5), (6,12), (13,20), (21,30),
# (31,100) -- which a fractional or out-of-range average could miss entirely: an
# average of 30.5 scored 1.0, ABOVE both its neighbours (0.85 at 30, 0.70 at 31).
# The bands are documented here rather than expressed as a table because the
# first boundary is strict and the rest are inclusive; see get_rep_range_factor.
REP_RANGE_FACTOR_VALUES: Tuple[float, ...] = (0.70, 0.85, 1.0)

# Muscle contribution weights (primary/secondary/tertiary)
MUSCLE_CONTRIBUTION_WEIGHTS = {
    'primary': 1.0,
    'secondary': 0.5,
    'tertiary': 0.25,
}

# Weekly volume classification thresholds (based on effective sets)
WEEKLY_VOLUME_THRESHOLDS = {
    'low': (0, 10),
    'medium': (10, 20),
    'high': (20, 30),
    'excessive': (30, float('inf')),
}

# Session volume warning thresholds
SESSION_VOLUME_THRESHOLDS = {
    VolumeWarningLevel.OK: (0, 10),
    VolumeWarningLevel.BORDERLINE: (10, 11),
    VolumeWarningLevel.EXCESSIVE: (11, float('inf')),
}

# Default neutral multiplier for missing data
DEFAULT_MULTIPLIER = 1.0


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class EffectiveSetResult:
    """Result container for effective set calculation on a single exercise row."""
    raw_sets: float
    effective_sets: float
    effort_factor: float
    rep_range_factor: float
    # Per-muscle effective sets (after contribution weighting)
    muscle_contributions: Dict[str, float]


# =============================================================================
# Core Calculation Functions
# =============================================================================

def get_effort_factor(rir: Optional[int] = None, rpe: Optional[float] = None) -> float:
    """Calculate effort factor from RIR or RPE.
    
    Args:
        rir: Reps In Reserve (0 = failure, higher = easier). Preferred if available.
        rpe: Rate of Perceived Exertion (10 = failure, lower = easier).
    
    Returns:
        Effort multiplier (0.55 to 1.0). Defaults to 1.0 if both missing.
    
    Notes:
        - Prefers RIR when available
        - Converts RPE to RIR if only RPE is provided: RIR = 10 - RPE
        - Uses discrete buckets to avoid over-precision
        - Clamps RIR to valid range [0, 10]
    """
    effective_rir: Optional[int] = None
    
    # Prefer RIR if available
    if rir is not None:
        effective_rir = rir
    elif rpe is not None:
        # Convert RPE to RIR: RPE 10 = RIR 0, RPE 7 = RIR 3, etc.
        effective_rir = int(round(10 - rpe))
    
    # If neither available, return neutral
    if effective_rir is None:
        return DEFAULT_MULTIPLIER
    
    # Clamp to valid range
    effective_rir = max(0, min(10, effective_rir))
    
    # Find matching bucket
    for (low, high), factor in EFFORT_FACTOR_BUCKETS.items():
        if low <= effective_rir <= high:
            return factor
    
    # Fallback (shouldn't reach here due to clamping)
    return DEFAULT_MULTIPLIER


def get_rep_range_factor(
    min_reps: Optional[int] = None, 
    max_reps: Optional[int] = None
) -> float:
    """Calculate rep range factor from min/max rep range.
    
    Args:
        min_reps: Minimum reps in the target range.
        max_reps: Maximum reps in the target range.
    
    Returns:
        Rep range multiplier (0.70 to 1.0). Defaults to 1.0 if unknown.

    Notes:
        - Uses coarse categories, not per-rep granularity
        - Based on average of min/max if both provided
        - Hypertrophy-optimal range (6-20) gets full credit
        - TOTAL over every positive average (ADR-009 ruling 2): the bands below
          leave no gap, so no in-domain input falls through to the neutral
          default. The previous disjoint integer buckets did: an average of 30.5
          scored 1.0, ABOVE both its neighbours (0.85 at 30, 0.70 at 31).
        - A non-positive average is unusable rather than unknown, and takes the
          same neutral arm as missing data. It is reachable: nothing validates a
          lower rep bound, so 0 and negative values persist.
    """
    # Calculate representative rep count. The chain is exhaustive over the four
    # min/max None combinations, and the last branch returns rather than
    # assigning - that is what proves avg_reps is bound and non-None under the
    # declared Optional[int] types at the band comparisons below. Collapsing the
    # both-None case into an early guard instead reads more directly but defeats
    # pyright's narrowing, which cannot follow an `A is None and B is None`
    # guard back into the later branches.
    if min_reps is not None and max_reps is not None:
        avg_reps = (min_reps + max_reps) / 2.0
    elif max_reps is not None:
        avg_reps = max_reps
    elif min_reps is not None:
        avg_reps = min_reps
    else:
        return DEFAULT_MULTIPLIER

    # Explicit bands, not a cumulative loop: the first boundary is STRICT (< 6)
    # while the rest are inclusive, so a uniform `avg <= upper` walk would
    # return 0.85 at exactly 6 reps, where the ruling requires 1.0.
    if avg_reps <= 0:
        return DEFAULT_MULTIPLIER
    if avg_reps < 6:
        return 0.85
    if avg_reps <= 20:
        return 1.0
    if avg_reps <= 30:
        return 0.85
    return 0.70


def calculate_effective_sets(
    sets: int,
    rir: Optional[int] = None,
    rpe: Optional[float] = None,
    min_rep_range: Optional[int] = None,
    max_rep_range: Optional[int] = None,
    primary_muscle: Optional[str] = None,
    secondary_muscle: Optional[str] = None,
    tertiary_muscle: Optional[str] = None,
    counting_mode: CountingMode = CountingMode.EFFECTIVE,
    contribution_mode: ContributionMode = ContributionMode.TOTAL,
) -> EffectiveSetResult:
    """Calculate effective sets for a single exercise row.
    
    This is the core calculation that applies:
    1. Effort factor (based on RIR/RPE)
    2. Rep range factor (based on rep targets)
    3. Muscle contribution weighting (primary/secondary/tertiary)
    
    All factors are applied multiplicatively at the per-set level.
    
    Args:
        sets: Raw number of sets performed.
        rir: Reps In Reserve (optional).
        rpe: Rate of Perceived Exertion (optional).
        min_rep_range: Minimum target reps (optional).
        max_rep_range: Maximum target reps (optional).
        primary_muscle: Primary muscle group worked.
        secondary_muscle: Secondary muscle group worked (optional).
        tertiary_muscle: Tertiary muscle group worked (optional).
        counting_mode: RAW or EFFECTIVE set counting.
        contribution_mode: DIRECT_ONLY or TOTAL contribution.
    
    Returns:
        EffectiveSetResult containing raw sets, effective sets, factors,
        and per-muscle contributions.
    """
    raw_sets = float(sets) if sets else 0.0
    
    # In RAW mode, skip all weighting
    if counting_mode == CountingMode.RAW:
        effort_factor = DEFAULT_MULTIPLIER
        rep_range_factor = DEFAULT_MULTIPLIER
        base_effective = raw_sets
    else:
        # Calculate factors
        effort_factor = get_effort_factor(rir, rpe)
        rep_range_factor = get_rep_range_factor(min_rep_range, max_rep_range)
        
        # Apply factors multiplicatively
        base_effective = raw_sets * effort_factor * rep_range_factor
    
    # Calculate per-muscle contributions
    muscle_contributions: Dict[str, float] = {}
    
    muscles = [
        ('primary', primary_muscle),
        ('secondary', secondary_muscle),
        ('tertiary', tertiary_muscle),
    ]

    # A muscle may occupy more than one role - 38 of the shipped catalog's 1,897
    # exercises do. Its credit is the SUM of the applicable role weights, so
    # primary + secondary is 1.5x (ADR-009). Assigning instead of accumulating
    # let the lower role overwrite the higher one, which is what made Effective
    # read 3.0 against Raw 4.5 for the same row.
    for role, muscle in muscles:
        if not muscle:
            continue
        if contribution_mode == ContributionMode.DIRECT_ONLY and role != 'primary':
            continue
        weight = MUSCLE_CONTRIBUTION_WEIGHTS[role]
        muscle_contributions[muscle] = (
            muscle_contributions.get(muscle, 0.0) + base_effective * weight
        )

    return EffectiveSetResult(
        raw_sets=raw_sets,
        effective_sets=base_effective,
        effort_factor=effort_factor,
        rep_range_factor=rep_range_factor,
        muscle_contributions=muscle_contributions,
    )


def get_session_volume_warning(effective_sets: float) -> VolumeWarningLevel:
    """Get session volume warning level for a muscle.
    
    Args:
        effective_sets: Effective sets for a muscle in a single session.
    
    Returns:
        VolumeWarningLevel indicating if volume is OK, borderline, or excessive.
    
    Notes:
        - Thresholds: ≤10 OK, 10-11 Borderline, >11 Excessive
        - These are soft signals, not errors
        - Does not block execution or override user intent
    """
    for level, (low, high) in SESSION_VOLUME_THRESHOLDS.items():
        if low <= effective_sets < high:
            return level
    
    return VolumeWarningLevel.OK


def get_weekly_volume_class(effective_sets: float) -> str:
    """Classify weekly volume level for a muscle.
    
    Args:
        effective_sets: Total effective sets for a muscle per week.
    
    Returns:
        Classification string: 'low', 'medium', 'high', or 'excessive'.
    
    Notes:
        - Thresholds are static and explicit
        - Classification is informational only, not a target
        - Based on primary effective sets
    """
    for label, (low, high) in WEEKLY_VOLUME_THRESHOLDS.items():
        if low <= effective_sets < high:
            return label

    return 'low'


# =============================================================================
# Utility Functions
# =============================================================================

def rpe_to_rir(rpe: float) -> int:
    """Convert RPE to RIR.
    
    Args:
        rpe: Rate of Perceived Exertion (1-10 scale, 10 = failure).
    
    Returns:
        Estimated RIR (Reps In Reserve).
    """
    return int(round(10 - rpe))


def rir_to_rpe(rir: int) -> float:
    """Convert RIR to RPE.
    
    Args:
        rir: Reps In Reserve (0 = failure).
    
    Returns:
        Estimated RPE.
    """
    return 10.0 - rir
