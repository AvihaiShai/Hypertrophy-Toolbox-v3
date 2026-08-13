// Workout plan superset actions module (Refactor Plan v3 WP3.4g).
//
// Mechanical feature-split extracted from workout-plan.js: checkbox selection,
// action-bar state, link/unlink handlers, and action-button initialization. The
// plan refresh remains orchestration owned by workout-plan.js and is injected
// once at module load to avoid a circular import.
import { showToast } from './toast.js';
import { api } from './fetch-wrapper.js';
import { workoutPlanState } from './workout-plan-state.js';
import {
    buildSupersetLinkPayload,
    buildSupersetUnlinkPayload,
} from './workout-plan-helpers.js';

const supersetDeps = {
    refreshPlan: () => {},
};

/**
 * Inject the plan-refresh callback the successful link/unlink paths depend on.
 * Called once by workout-plan.js at module load.
 * @param {Partial<typeof supersetDeps>} deps
 */
export function configureSupersets(deps) {
    Object.assign(supersetDeps, deps);
}

/**
 * Handle superset checkbox change
 * @param {HTMLInputElement} checkbox - The checkbox element
 */
export function handleSupersetCheckboxChange(checkbox) {
    const exerciseId = parseInt(checkbox.dataset.exerciseId);
    const routine = checkbox.dataset.routine;
    const supersetGroup = checkbox.dataset.supersetGroup;
    const row = checkbox.closest('tr');

    if (checkbox.checked) {
        workoutPlanState.selectedExerciseIds.add(exerciseId);
        row.classList.add('superset-selected');
    } else {
        workoutPlanState.selectedExerciseIds.delete(exerciseId);
        row.classList.remove('superset-selected');
    }

    updateSupersetActionButtons();
}

/**
 * Update the superset action buttons based on current selection
 */
export function updateSupersetActionButtons() {
    const actionsContainer = document.getElementById('superset-actions');
    const linkBtn = document.getElementById('link-superset-btn');
    const unlinkBtn = document.getElementById('unlink-superset-btn');
    const infoSpan = document.getElementById('superset-selection-info');

    if (!actionsContainer || !linkBtn || !unlinkBtn || !infoSpan) return;

    const selectedCount = workoutPlanState.selectedExerciseIds.size;

    if (selectedCount === 0) {
        // Return the bar to the rest state the template ships
        // (templates/workout_plan.html: link disabled, unlink hidden, info
        // empty) rather than only hiding it. Hiding alone leaves whatever the
        // last non-zero branch wrote: an `unlinkBtn.hidden = false` parked
        // inside a `display:none` container is the same shape as the defect
        // #317 closed.
        infoSpan.textContent = '';
        infoSpan.style.color = '';
        linkBtn.hidden = false;
        linkBtn.disabled = true;
        unlinkBtn.hidden = true;
        actionsContainer.style.display = 'none';
        return;
    }

    actionsContainer.style.display = 'flex';
    // Every branch below writes textContent but only some write a colour, so
    // without this a `--wp-warn` from a previous 2-row selection bleeds onto
    // the next neutral message.
    infoSpan.style.color = '';

    // Get selected exercises info
    const selectedCheckboxes = document.querySelectorAll('.superset-checkbox:checked');
    const routines = new Set();
    let hasExistingSuperset = false;

    selectedCheckboxes.forEach(cb => {
        routines.add(cb.dataset.routine);
        if (cb.dataset.supersetGroup) {
            hasExistingSuperset = true;
        }
    });

    const sameRoutine = routines.size === 1;

    // Update info text
    if (selectedCount === 1) {
        if (hasExistingSuperset) {
            infoSpan.textContent = '1 exercise selected (in superset)';
            unlinkBtn.hidden = false;
            linkBtn.hidden = true;
        } else {
            infoSpan.textContent = '1 exercise selected - select 1 more to create superset';
            unlinkBtn.hidden = true;
            linkBtn.hidden = false;
            linkBtn.disabled = true;
        }
    } else if (selectedCount === 2) {
        if (!sameRoutine) {
            infoSpan.textContent = '⚠️ Exercises must be in the same routine';
            infoSpan.style.color = 'var(--wp-bad)';
            linkBtn.disabled = true;
            unlinkBtn.hidden = true;
            linkBtn.hidden = false;
        } else if (hasExistingSuperset) {
            infoSpan.textContent = '⚠️ One or both exercises already in a superset';
            infoSpan.style.color = 'var(--wp-warn)';
            linkBtn.disabled = true;
            unlinkBtn.hidden = false;
            linkBtn.hidden = true;
        } else {
            infoSpan.textContent = '2 exercises selected - ready to link';
            infoSpan.style.color = 'var(--wp-good)';
            linkBtn.disabled = false;
            unlinkBtn.hidden = true;
            linkBtn.hidden = false;
        }
    } else {
        infoSpan.textContent = `${selectedCount} exercises selected - supersets can only have 2 exercises`;
        infoSpan.style.color = 'var(--wp-warn)';
        linkBtn.disabled = true;
        unlinkBtn.hidden = true;
        linkBtn.hidden = false;
    }
}

/**
 * Drop every trace of an in-progress superset selection. Transient UI state
 * only — nothing here reaches the API or `refreshPlan()`.
 *
 * The row sweep must stay `classList.remove` and never a `className` write:
 * `supersetRowClasses()` also puts `superset-group-N` and the first/last edge
 * classes on those rows, so clobbering the attribute would make a persisted
 * superset visually dissolve until the next render.
 */
export function clearSupersetSelection() {
    workoutPlanState.selectedExerciseIds.clear();

    document.querySelectorAll('#workout_plan_table_body .superset-checkbox:checked')
        .forEach(checkbox => { checkbox.checked = false; });
    document.querySelectorAll('#workout_plan_table_body tr.superset-selected')
        .forEach(row => row.classList.remove('superset-selected'));

    updateSupersetActionButtons();
}

/**
 * Initialize superset action button click handlers
 */
export function initializeSupersetActions() {
    const linkBtn = document.getElementById('link-superset-btn');
    const unlinkBtn = document.getElementById('unlink-superset-btn');

    if (linkBtn && !linkBtn.dataset.initialized) {
        linkBtn.addEventListener('click', handleLinkSuperset);
        linkBtn.dataset.initialized = 'true';
    }

    if (unlinkBtn && !unlinkBtn.dataset.initialized) {
        unlinkBtn.addEventListener('click', handleUnlinkSuperset);
        unlinkBtn.dataset.initialized = 'true';
    }
}

/**
 * Handle linking selected exercises as a superset
 */
async function handleLinkSuperset() {
    if (workoutPlanState.selectedExerciseIds.size !== 2) {
        showToast('Please select exactly 2 exercises to create a superset', true);
        return;
    }

    const exerciseIds = Array.from(workoutPlanState.selectedExerciseIds);

    try {
        const data = await api.post('/api/superset/link', buildSupersetLinkPayload(exerciseIds), { showErrorToast: false });

        showToast(data.message || 'Superset created successfully');
        // Routed through the shared reset so the action bar drops immediately
        // instead of holding a stale "ready to link" message until the async
        // refresh lands.
        clearSupersetSelection();
        // Refresh the workout plan to show updated superset styling
        supersetDeps.refreshPlan();
    } catch (error) {
        console.error('Error creating superset:', error);
        showToast(error.message || 'Failed to create superset', true);
    }
}

/**
 * Handle unlinking a superset
 */
async function handleUnlinkSuperset() {
    // Get the first selected exercise that's in a superset
    const selectedCheckbox = document.querySelector('.superset-checkbox:checked[data-superset-group]:not([data-superset-group=""])');

    if (!selectedCheckbox) {
        showToast('Please select an exercise that is part of a superset', true);
        return;
    }

    const exerciseId = parseInt(selectedCheckbox.dataset.exerciseId);

    try {
        const data = await api.post('/api/superset/unlink', buildSupersetUnlinkPayload(exerciseId), { showErrorToast: false });

        showToast(data.message || 'Superset unlinked successfully');
        clearSupersetSelection();
        // Refresh the workout plan to show updated styling
        supersetDeps.refreshPlan();
    } catch (error) {
        console.error('Error unlinking superset:', error);
        showToast(error.message || 'Failed to unlink superset', true);
    }
}
