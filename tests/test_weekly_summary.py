import pytest

from utils.exercise_manager import save_exercise, add_exercise
from utils.weekly_summary import (
    calculate_exercise_categories,
    calculate_isolated_muscles_stats,
    calculate_weekly_summary,
)
from utils.effective_sets import CountingMode, ContributionMode


@pytest.mark.usefixtures('clean_db')
def test_weighted_weekly_summary(db_handler):
    """Test weekly summary with effective sets calculation.
    
    This test verifies that:
    1. Effective sets are calculated correctly with effort/rep range factors
    2. Raw sets are preserved for backward compatibility
    3. Muscle contribution weighting works correctly
    """
    save_exercise(
        {
            'exercise_name': 'Bench Press',
            'primary_muscle_group': 'Chest',
            'secondary_muscle_group': 'Triceps',
            'tertiary_muscle_group': 'Front Shoulder',
            'advanced_isolated_muscles': 'anterior-deltoid, upper-pectoralis',
            'utility': 'basic',
            'grips': 'overhand',
            'stabilizers': None,
            'synergists': None,
            'force': 'push',
            'equipment': 'barbell',
            'mechanic': 'compound',
            'difficulty': 'intermediate',
        }
    )

    response = add_exercise(
        routine='Push Day',
        exercise='Bench Press',
        sets=4,
        min_rep_range=6,
        max_rep_range=8,
        rir=2,  # RIR 2 = 0.85 effort factor
        weight=80.0,
        rpe=8.0,
    )
    assert 'successfully' in response.lower()

    # Test default effective sets mode
    summary = calculate_weekly_summary()
    assert 'Chest' in summary
    chest = summary['Chest']
    
    # With RIR 2 (0.85 factor) and rep range 6-8 (1.0 factor):
    # Effective sets = 4 * 0.85 * 1.0 = 3.4
    assert chest['weekly_sets'] == pytest.approx(3.4)  # Effective sets (primary metric)
    assert chest['raw_weekly_sets'] == pytest.approx(4.0)  # Raw sets preserved
    assert chest['effective_weekly_sets'] == pytest.approx(3.4)  # Explicit effective
    assert chest['sets_per_session'] == pytest.approx(3.4)
    assert chest['status'] == 'low'
    
    # Reps and volume also use effective sets
    # Avg reps = (6+8)/2 = 7, effective sets = 3.4
    assert chest['total_reps'] == pytest.approx(3.4 * 7)  # 23.8
    assert chest['total_volume'] == pytest.approx(3.4 * 7 * 80)  # 1904.0

    # Triceps gets 0.5 muscle contribution + effort factor
    triceps = summary['Triceps']
    # 4 * 0.85 * 1.0 * 0.5 = 1.7
    assert triceps['weekly_sets'] == pytest.approx(1.7)
    assert triceps['raw_weekly_sets'] == pytest.approx(2.0)  # Raw: 4 * 0.5
    
    # Front-Shoulder gets 0.25 muscle contribution
    front_shoulder = summary['Front-Shoulder']
    # 4 * 0.85 * 1.0 * 0.25 = 0.85
    assert front_shoulder['weekly_sets'] == pytest.approx(0.85)
    assert front_shoulder['raw_weekly_sets'] == pytest.approx(1.0)  # Raw: 4 * 0.25

    # Verify mode indicators
    assert chest['counting_mode'] == 'effective'
    assert chest['contribution_mode'] == 'total'

    categories = calculate_exercise_categories()
    category_map = {(row['category'], row['subcategory']): row['total_exercises'] for row in categories}
    assert category_map[('Mechanic', 'Compound')] == 1
    assert category_map[('Utility', 'Basic')] == 1
    assert category_map[('Force', 'Push')] == 1

    isolated = calculate_isolated_muscles_stats()
    iso_map = {row['isolated_muscle']: row for row in isolated}
    assert iso_map['anterior-deltoid']['exercise_count'] == 1
    assert iso_map['anterior-deltoid']['total_sets'] == pytest.approx(4.0)  # Raw sets for isolated


@pytest.mark.usefixtures('clean_db')
def test_weekly_summary_raw_mode(db_handler):
    """Test weekly summary in RAW counting mode (backward compatibility)."""
    save_exercise(
        {
            'exercise_name': 'Bench Press',
            'primary_muscle_group': 'Chest',
            'secondary_muscle_group': 'Triceps',
            'tertiary_muscle_group': 'Front Shoulder',
            'advanced_isolated_muscles': 'anterior-deltoid, upper-pectoralis',
            'utility': 'basic',
            'grips': 'overhand',
            'stabilizers': None,
            'synergists': None,
            'force': 'push',
            'equipment': 'barbell',
            'mechanic': 'compound',
            'difficulty': 'intermediate',
        }
    )

    add_exercise(
        routine='Push Day',
        exercise='Bench Press',
        sets=4,
        min_rep_range=6,
        max_rep_range=8,
        rir=2,
        weight=80.0,
        rpe=8.0,
    )

    # Test RAW mode - should match legacy behavior
    summary = calculate_weekly_summary(counting_mode=CountingMode.RAW)
    chest = summary['Chest']
    
    # RAW mode skips effort/rep range weighting
    assert chest['weekly_sets'] == pytest.approx(4.0)  # Raw sets
    assert chest['raw_weekly_sets'] == pytest.approx(4.0)
    
    triceps = summary['Triceps']
    assert triceps['weekly_sets'] == pytest.approx(2.0)  # 4 * 0.5 muscle contribution
    
    assert summary['Front-Shoulder']['weekly_sets'] == pytest.approx(1.0)  # 4 * 0.25


@pytest.mark.usefixtures('clean_db')
def test_weekly_summary_effective_sets_invariant_across_modes(db_handler):
    """effective_weekly_sets should not change when display mode switches to RAW."""
    save_exercise(
        {
            'exercise_name': 'Incline Press',
            'primary_muscle_group': 'Chest',
            'secondary_muscle_group': None,
            'tertiary_muscle_group': None,
            'advanced_isolated_muscles': None,
            'utility': 'basic',
            'grips': 'overhand',
            'stabilizers': None,
            'synergists': None,
            'force': 'push',
            'equipment': 'barbell',
            'mechanic': 'compound',
            'difficulty': 'intermediate',
        }
    )

    add_exercise(
        routine='Push Day',
        exercise='Incline Press',
        sets=12,
        min_rep_range=8,
        max_rep_range=10,
        rir=2,
        weight=100.0,
        rpe=8.0,
    )

    effective_mode = calculate_weekly_summary(counting_mode=CountingMode.EFFECTIVE)
    raw_mode = calculate_weekly_summary(counting_mode=CountingMode.RAW)

    expected_effective_sets = 12 * 0.85 * 1.0  # RIR 2 + 8-10 reps
    assert effective_mode['Chest']['effective_weekly_sets'] == pytest.approx(expected_effective_sets)
    assert raw_mode['Chest']['effective_weekly_sets'] == pytest.approx(expected_effective_sets)


@pytest.mark.usefixtures('clean_db')
def test_weekly_summary_direct_only_mode(db_handler):
    """Test weekly summary in DIRECT_ONLY contribution mode."""
    save_exercise(
        {
            'exercise_name': 'Bench Press',
            'primary_muscle_group': 'Chest',
            'secondary_muscle_group': 'Triceps',
            'tertiary_muscle_group': 'Front Shoulder',
            'advanced_isolated_muscles': 'anterior-deltoid, upper-pectoralis',
            'utility': 'basic',
            'grips': 'overhand',
            'stabilizers': None,
            'synergists': None,
            'force': 'push',
            'equipment': 'barbell',
            'mechanic': 'compound',
            'difficulty': 'intermediate',
        }
    )

    add_exercise(
        routine='Push Day',
        exercise='Bench Press',
        sets=4,
        min_rep_range=6,
        max_rep_range=8,
        rir=2,
        weight=80.0,
        rpe=8.0,
    )

    # Test DIRECT_ONLY mode - only primary muscle gets credit
    summary = calculate_weekly_summary(contribution_mode=ContributionMode.DIRECT_ONLY)
    
    # Chest (primary) should get full effective sets
    assert 'Chest' in summary
    chest = summary['Chest']
    assert chest['weekly_sets'] == pytest.approx(3.4)  # 4 * 0.85 * 1.0
    
    # Secondary and tertiary muscles should NOT appear
    assert 'Triceps' not in summary
    assert 'Front-Shoulder' not in summary


@pytest.mark.usefixtures('clean_db')
def test_duplicate_role_muscle_is_credited_the_sum_of_its_role_weights(db_handler):
    """ADR-009 ruling 1, at the weekly aggregator.

    38 of the shipped catalog's 1,897 exercises name the same muscle in two
    P/S/T roles (Dumbbell Wrist Curl is Forearms / Forearms). Such a muscle is
    credited the SUM of its role weights, so Effective equals Raw when both
    factors are 1.0.

    This test is what makes the fix ATOMIC. It fails in BOTH directions of a
    partial change: accumulating in calculate_effective_sets() alone leaves the
    aggregator adding the summed value once per role (9.0 here), and collapsing
    the aggregator's role loop alone leaves the overwritten 1.5 to be read.
    """
    save_exercise(
        {
            'exercise_name': 'Dumbbell Wrist Curl',
            'primary_muscle_group': 'Forearms',
            'secondary_muscle_group': 'Forearms',
            'tertiary_muscle_group': None,
            'advanced_isolated_muscles': None,
            'utility': 'auxiliary',
            'grips': 'underhand',
            'stabilizers': None,
            'synergists': None,
            'force': 'pull',
            'equipment': 'dumbbell',
            'mechanic': 'isolated',
            'difficulty': 'beginner',
        }
    )
    add_exercise(
        routine='Arms Day',
        exercise='Dumbbell Wrist Curl',
        sets=3,
        min_rep_range=8,
        max_rep_range=12,
        rir=0,  # RIR 0 -> effort 1.0; 8-12 reps -> rep-range 1.0
        weight=10.0,
        rpe=10.0,
    )

    summary = calculate_weekly_summary()
    forearms = summary['Forearms']

    # 3 sets * (primary 1.0 + secondary 0.5) = 4.5, on both columns.
    assert forearms['raw_weekly_sets'] == pytest.approx(4.5)
    assert forearms['effective_weekly_sets'] == pytest.approx(4.5)
    assert forearms['weekly_sets'] == pytest.approx(4.5)
    # sessions_by_muscle accumulates inside the SAME deduplicated loop, so it
    # moves too. Pinned here because it is the only assertion that would catch a
    # partial revert of that one line.
    assert forearms['frequency'] == 1


@pytest.mark.usefixtures('clean_db')
def test_duplicate_role_muscle_frequency_can_cross_the_threshold(db_handler):
    """ADR-009's frequency consequence, at the boundary it actually moves.

    Frequency counts sessions reaching >= 1.0 effective sets. One set at RIR 2
    (0.85 effort) and 8-10 reps (1.0 rep-range) gives base 0.85. Before the
    ruling the muscle was credited 0.85 twice at the secondary weight -- 0.425
    each, and the per-session total the threshold reads was 0.85, BELOW 1.0, so
    frequency was 0. Summing the role weights gives 0.85 * 1.5 = 1.275, so
    frequency is 1. Frequency can only ever move UP this way, never down.
    """
    save_exercise(
        {
            'exercise_name': 'Dumbbell Wrist Curl',
            'primary_muscle_group': 'Forearms',
            'secondary_muscle_group': 'Forearms',
            'tertiary_muscle_group': None,
            'advanced_isolated_muscles': None,
            'utility': 'auxiliary',
            'grips': 'underhand',
            'stabilizers': None,
            'synergists': None,
            'force': 'pull',
            'equipment': 'dumbbell',
            'mechanic': 'isolated',
            'difficulty': 'beginner',
        }
    )
    add_exercise(
        routine='Arms Day',
        exercise='Dumbbell Wrist Curl',
        sets=1,
        min_rep_range=8,
        max_rep_range=10,
        rir=2,
        weight=10.0,
        rpe=8.0,
    )

    forearms = calculate_weekly_summary()['Forearms']
    # 0.85 * 1.5 = 1.275, reported rounded to two decimals.
    assert forearms['effective_weekly_sets'] == pytest.approx(1.27)
    # The threshold reads the UNROUNDED per-session total, which is 1.275 -- so
    # this is 1 where the pre-ruling 0.85 gave 0.
    assert forearms['frequency'] == 1


@pytest.mark.usefixtures('clean_db')
def test_duplicate_role_muscle_direct_only_stays_primary_only(db_handler):
    """DIRECT_ONLY is unchanged by ADR-009 -- primary only, at full credit."""
    save_exercise(
        {
            'exercise_name': 'Dumbbell Wrist Curl',
            'primary_muscle_group': 'Forearms',
            'secondary_muscle_group': 'Forearms',
            'tertiary_muscle_group': None,
            'advanced_isolated_muscles': None,
            'utility': 'auxiliary',
            'grips': 'underhand',
            'stabilizers': None,
            'synergists': None,
            'force': 'pull',
            'equipment': 'dumbbell',
            'mechanic': 'isolated',
            'difficulty': 'beginner',
        }
    )
    add_exercise(
        routine='Arms Day',
        exercise='Dumbbell Wrist Curl',
        sets=3,
        min_rep_range=8,
        max_rep_range=12,
        rir=0,
        weight=10.0,
        rpe=10.0,
    )

    summary = calculate_weekly_summary(
        contribution_mode=ContributionMode.DIRECT_ONLY
    )
    forearms = summary['Forearms']
    assert forearms['raw_weekly_sets'] == pytest.approx(3.0)
    assert forearms['effective_weekly_sets'] == pytest.approx(3.0)
