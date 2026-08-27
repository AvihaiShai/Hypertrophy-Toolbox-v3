import { showToast, toastMessageText } from './toast.js';
import { api } from './fetch-wrapper.js';

let volumeConfig = null;
let currentMode = 'basic';
let calculateDebounceId = null;
const modeVolumeState = {
    basic: {},
    advanced: {}
};
const modeRangeState = {
    basic: {},
    advanced: {}
};

const DEFAULT_SLIDER_MAX = 60;
const VOLUME_HISTORY_BUSY_ATTR = 'data-volume-history-busy';
const JSON_REQUEST_HEADERS = {
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
};

const CALCULATE_ERROR_ID = 'volume-calculate-error';
// States what is on screen now, not what happened to it. Event phrasing such as
// "your previous results were cleared" is false on the first failure of a page
// load, where nothing was ever shown.
const CALCULATE_ERROR_MESSAGE = 'Volume calculation failed, so no results are shown. Please try again.';

// Monotonic request counter. The failure state machine is keyed on request
// order, not response arrival order, so a stale response cannot repaint over a
// newer one.
let calculateRequestSeq = 0;

const deepClone = (value) => JSON.parse(JSON.stringify(value || {}));

const toNumericRange = (range) => {
    const fallback = { min: 12, max: 20 };
    if (!range || typeof range !== 'object') {
        return { ...fallback };
    }
    const min = Number(range.min);
    const max = Number(range.max);
    const safeMin = Number.isFinite(min) && min >= 0 ? min : fallback.min;
    const safeMaxCandidate = Number.isFinite(max) && max >= 0 ? max : fallback.max;
    const safeMax = safeMaxCandidate < safeMin ? safeMin : safeMaxCandidate;
    return { min: safeMin, max: safeMax };
};

const normalizeRangeMap = (ranges) => {
    const result = {};
    Object.entries(deepClone(ranges)).forEach(([muscle, range]) => {
        result[muscle] = toNumericRange(range);
    });
    return result;
};

const sanitizeRangePair = (pair) => toNumericRange(pair);

export function initializeVolumeSplitter() {
    const root = document.getElementById('volume-splitter-app');
    if (!root) {
        return;
    }

    volumeConfig = parseConfig(root);
    modeRangeState.basic = normalizeRangeMap(volumeConfig.basicRanges);
    modeRangeState.advanced = normalizeRangeMap(volumeConfig.advancedRanges);
    currentMode = volumeConfig.defaultMode;

    initializeModeToggle(root);
    initializePageTooltips();

    const calculateBtn = document.getElementById('calculate-volume');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', () => calculateVolume());
    }

    const resetBtn = document.getElementById('reset-volume');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetValues);
    }

    const exportBtn = document.getElementById('export-volume');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => exportVolumePlan(false));
    }

    const saveActivateBtn = document.getElementById('save-activate-volume');
    if (saveActivateBtn) {
        saveActivateBtn.addEventListener('click', () => exportVolumePlan(true));
    }

    const exportExcelBtn = document.getElementById('export-to-excel-btn');
    if (exportExcelBtn) {
        exportExcelBtn.addEventListener('click', exportToExcel);
    }

    const historyBody = document.getElementById('history-body');
    if (historyBody) {
        historyBody.addEventListener('click', handleHistoryClick);
    }

    initDeleteModal();

    renderSliders();
    modeVolumeState[currentMode] = collectVolumes();
    modeRangeState[currentMode] = collectRanges();
    void loadInitialVolumeHistory();
}

function initializePageTooltips() {
    if (typeof tippy !== 'function') {
        return;
    }

    tippy('#training-days', {
        content: 'Choose a realistic frequency that you can maintain consistently. More training days allow for better volume distribution.',
        placement: 'right'
    });
}

// `forceAnnounce` selects whether to raise a toast even when a failure region
// already stands. It does not mean "never announce": the announce condition in
// enterCalculateFailureState() still fires on the first failure of a run and
// whenever our toast content has been replaced.
function calculateVolume({ forceAnnounce = true } = {}) {
    const seq = ++calculateRequestSeq;
    const trainingSelect = document.getElementById('training-days');
    const trainingDays = Math.max(parseInt(trainingSelect?.value, 10) || 3, 1);
    const volumes = collectVolumes();
    const ranges = collectRanges();

    modeVolumeState[currentMode] = volumes;
    modeRangeState[currentMode] = ranges;

    api.post('/api/calculate_volume', {
        mode: currentMode,
        training_days: trainingDays,
        volumes,
        ranges
    }, {
        headers: {
            'Content-Type': 'application/json',
            ...JSON_REQUEST_HEADERS
        },
        showLoading: false,
        showErrorToast: false,
        useDefaultHeaders: false
    })
        .then(response => response.data)
        .then(data => {
            if (seq !== calculateRequestSeq) {
                return;
            }
            try {
                handleCalculateResponse(data);
            } catch (error) {
                // Post-2xx response-handling failures never reach the shared
                // wrapper's error branch, so this is their only handler.
                console.error('Volume calculation: response handling failed', error);
                enterCalculateFailureState({ forceAnnounce });
                return;
            }
            exitCalculateFailureState();
        })
        .catch(error => {
            if (seq !== calculateRequestSeq) {
                return;
            }
            // Request-failure class: non-2xx and transport failures, both of
            // which the shared wrapper reports silently for this call.
            console.error('Volume calculation: request failed', error);
            enterCalculateFailureState({ forceAnnounce });
        });
}

function enterCalculateFailureState({ forceAnnounce }) {
    clearResults();

    const standing = Boolean(document.getElementById(CALCULATE_ERROR_ID));
    renderCalculateFailureRegion();

    if (forceAnnounce || !standing || !ourMessageStands()) {
        showToast('error', CALCULATE_ERROR_MESSAGE, {
            action: {
                label: 'Retry',
                ariaLabel: 'Retry volume calculation',
                onClick: () => calculateVolume()
            }
        });
    }
}

function renderCalculateFailureRegion() {
    // Idempotent by contract: a repeat failure must not rebuild the node or
    // rewrite identical text, both of which are DOM churn under one state.
    if (document.getElementById(CALCULATE_ERROR_ID)) {
        return;
    }

    const panel = document.querySelector('.volume-insights-panel');
    if (!panel) {
        return;
    }

    const region = document.createElement('div');
    region.id = CALCULATE_ERROR_ID;
    region.className = 'volume-calculate-error alert alert-danger';
    region.dataset.testid = CALCULATE_ERROR_ID;

    // Deliberately not a live region: the toast already announces assertively,
    // and a second one would double-announce every failure.
    const message = document.createElement('span');
    message.textContent = CALCULATE_ERROR_MESSAGE;
    region.appendChild(message);

    const retry = document.createElement('button');
    retry.type = 'button';
    // Deliberately NOT a `btn btn-*` button. components.css paints `.alert-danger`
    // as a red gradient, and every Bootstrap button variant resolves to danger-red
    // text inside it -- measured at 1.58:1 there, which no class swap fixes. The
    // plain control inherits the UA button surface and measures 18.4:1. Plan v2
    // (D) specifies no Bootstrap button variant here; the spacing utility stays.
    retry.className = 'ms-2';
    retry.dataset.testid = 'volume-calculate-retry';
    retry.setAttribute('aria-label', 'Retry volume calculation');
    retry.textContent = 'Retry';
    retry.addEventListener('click', () => calculateVolume());
    region.appendChild(retry);

    panel.prepend(region);
}

function exitCalculateFailureState() {
    // `.remove()`, never a hidden retained node: the success path may not carry
    // a permanently present element.
    document.getElementById(CALCULATE_ERROR_ID)?.remove();
    dismissCalculateFailureToast();
}

function dismissCalculateFailureToast() {
    // A success arriving inside the toast's 3000 ms life would otherwise leave
    // an error toast standing over fresh results.
    if (!ourToastContentStands()) {
        return;
    }
    // OQ-8, narrowed. KI-011 preserves the action across a message replacement,
    // so the button probe alone would answer "ours" while an UNRELATED message
    // is on screen -- and hide() would dismiss a stranger's toast. The message
    // must be ours too.
    if (!ourMessageStands()) {
        return;
    }

    const toastElement = document.getElementById('liveToast');
    if (toastElement) {
        bootstrap.Toast.getInstance(toastElement)?.hide();
    }
}

// The ACTION probe: "our action button still stands inside #liveToast".
// Scoped to `#liveToast`, never `#toast-body`: the wider scope survives the
// node relocation a KI-011 fix would require. Deliberately blind to
// visibility: it returns true for a toast that has already dismissed itself.
function ourToastContentStands() {
    return Boolean(document.querySelector('#liveToast button[aria-label="Retry volume calculation"]'));
}

// The MESSAGE probe, added for KI-011 (docs/toast_action_continuity/PLANNING.md
// section 4.3). Deliberately NOT a query on #toast-body: the action slot lives
// inside that node, so #toast-body's own textContent can never equal
// CALCULATE_ERROR_MESSAGE once a button is present. toast.js owns its DOM shape
// and exports the reader, so a later rename there cannot break this silently.
//
// Why both probes exist. Before KI-011 they were co-extensive -- toast.js:60
// destroyed message and button together. Now they diverge in BOTH directions: a
// replacement leaves the button but takes the message, and an auto-hide leaves
// the message but takes the button. The announce condition asks about the
// MESSAGE; the dismissal guard requires both.
function ourMessageStands() {
    return toastMessageText() === CALCULATE_ERROR_MESSAGE;
}

function displayResults(results) {
    const tbody = document.getElementById('results-body');
    if (!tbody) {
        return;
    }

    tbody.innerHTML = '';
    const entries = Object.entries(results || {});

    if (!entries.length) {
        const section = document.querySelector('.results-section');
        section?.classList.add('d-none');
        return;
    }

    entries.forEach(([muscle, data]) => {
        const row = document.createElement('tr');
        const statusLabel = (data.status || 'optimal');
        row.innerHTML = `
            <td>${muscle}</td>
            <td>${data.weekly_sets}</td>
            <td>${data.sets_per_session}</td>
            <td class="status-${statusLabel}">
                ${statusLabel.charAt(0).toUpperCase() + statusLabel.slice(1)}
            </td>
        `;
        tbody.appendChild(row);
    });

    document.querySelector('.results-section')?.classList.remove('d-none');

    const ranges = getCurrentRanges();
    entries.forEach(([muscle, data]) => {
        applyStatusToRow(muscle, data, ranges[muscle]);
    });
}

function resetValues() {
    document.querySelectorAll('.volume-slider').forEach(slider => {
        slider.value = 0;
        updateValueDisplay(slider);
    });
    modeVolumeState[currentMode] = collectVolumes();
    clearResults();
    // Invalidate any in-flight calculation so a failure that resolves after the
    // user has zeroed the sliders cannot repaint over a deliberately blank page.
    calculateRequestSeq += 1;
    exitCalculateFailureState();
}

function loadPlan(planId) {
    api.get(`/api/volume_plan/${planId}`, {
        headers: JSON_REQUEST_HEADERS,
        showLoading: false,
        showErrorToast: false,
        useDefaultHeaders: false,
        retries: 0
    })
        .then(response => response.data)
        .then(plan => {
            const trainingSelect = document.getElementById('training-days');
            if (trainingSelect) {
                trainingSelect.value = plan.training_days;
            }

            const planVolumes = plan.volumes || {};
            const numericVolumes = Object.entries(planVolumes).reduce((acc, [muscle, data]) => {
                acc[muscle] = data?.weekly_sets || 0;
                return acc;
            }, {});

            const advancedLabels = new Set(volumeConfig.advancedMuscles);
            const hasAdvancedLabels = Object.keys(numericVolumes).some(label => advancedLabels.has(label));
            const targetMode = plan.mode || (hasAdvancedLabels ? 'advanced' : 'basic');

            setMode(targetMode, numericVolumes, { skipCalculate: true });
            calculateVolume();
        })
        .catch(error => {
            console.error('Error loading plan:', error);
            showToast('error', 'Failed to load plan. Please try again.');
        });
}

let pendingDeletePlanId = null;
let deleteModal = null;

function initDeleteModal() {
    const modalElement = document.getElementById('deleteVolumePlanModal');
    if (modalElement && typeof bootstrap !== 'undefined') {
        deleteModal = new bootstrap.Modal(modalElement);
        
        document.getElementById('confirmDeleteVolumePlan')?.addEventListener('click', () => {
            if (pendingDeletePlanId) {
                executeDeletePlan(pendingDeletePlanId);
            }
        });
    }
}

function deletePlan(planId) {
    pendingDeletePlanId = planId;
    if (deleteModal) {
        deleteModal.show();
    } else {
        // Fallback if modal not initialized
        executeDeletePlan(planId);
    }
}

function executeDeletePlan(planId) {
    api.delete(`/api/volume_plan/${planId}`, {
        headers: JSON_REQUEST_HEADERS,
        showLoading: false,
        showErrorToast: false,
        useDefaultHeaders: false
    })
    .then(response => response.data)
    .then(result => {
        if (deleteModal) deleteModal.hide();
        showToast('success', result?.message || 'Volume plan deleted successfully!');
        loadVolumeHistory();
    })
    .catch(error => {
        if (deleteModal) deleteModal.hide();
        console.error('Error deleting plan:', error);
        showToast('error', 'Failed to delete plan. Please try again.');
    })
    .finally(() => {
        pendingDeletePlanId = null;
    });
}

function exportVolumePlan(activate = false) {
    const trainingSelect = document.getElementById('training-days');
    const trainingDays = Math.max(parseInt(trainingSelect?.value, 10) || 3, 1);
    const volumes = collectVolumes();

    const data = {
        mode: currentMode,
        training_days: trainingDays,
        volumes,
        activate
    };
    
    api.post('/api/save_volume_plan', data, {
        headers: {
            'Content-Type': 'application/json',
            ...JSON_REQUEST_HEADERS
        },
        showLoading: false,
        showErrorToast: false,
        useDefaultHeaders: false
    })
    .then(response => response.data)
    .then(result => {
        const planId = result?.plan_id;
        if (!planId) {
            showToast('success', 'Volume plan saved successfully!');
        } else if (activate) {
            showToast('success', `Plan #${planId} saved and activated.`);
        } else {
            showToast('success', `Plan #${planId} saved.`, {
                duration: 6000,
                action: {
                    label: 'Activate for Plan tab',
                    ariaLabel: `Activate volume plan ${planId}`,
                    onClick: () => toggleActivePlan(planId, false)
                }
            });
        }
        const refreshed = loadVolumeHistory();
        if (activate && planId) {
            Promise.resolve(refreshed).then(() => {
                const summary = document.getElementById('volume-active-summary');
                summary?.focus();
            });
        }
    })
    .catch(error => {
        console.error('Error saving plan:', error);
        showToast('error', 'Failed to save plan. Please try again.');
    });
}

function displaySuggestions(suggestions) {
    const container = document.querySelector('.suggestions-container');
    const section = document.querySelector('.ai-suggestions-section');
    if (!container || !section) {
        return;
    }

    container.innerHTML = '';
    const list = Array.isArray(suggestions) ? suggestions : [];

    if (!list.length) {
        section.classList.add('d-none');
        return;
    }

    list.forEach(suggestion => {
        const card = document.createElement('div');
        card.className = `suggestion-card suggestion-${suggestion.type}`;
        card.dataset.type = suggestion.type;
        card.innerHTML = `
            <p class="mb-0">${suggestion.message}</p>
        `;
        container.appendChild(card);
    });

    section.classList.remove('d-none');
}

/**
 * Expose only the page's initial history hydration as readiness state.
 *
 * `loadVolumeHistory()` is also called by save/delete/activate actions. Those
 * user-action refreshes have their own observables and may overlap, so the
 * boolean page-readiness marker must not be toggled inside that shared loader.
 * Set synchronously before the first await so a waiter cannot observe a false
 * idle gap between DOMContentLoaded and the request starting.
 */
async function loadInitialVolumeHistory() {
    document.documentElement.setAttribute(VOLUME_HISTORY_BUSY_ATTR, '1');
    try {
        await loadVolumeHistory();
    } finally {
        document.documentElement.removeAttribute(VOLUME_HISTORY_BUSY_ATTR);
    }
}

function loadVolumeHistory() {
    return api.get('/api/volume_history', {
        headers: JSON_REQUEST_HEADERS,
        showLoading: false,
        showErrorToast: false,
        useDefaultHeaders: false,
        retries: 0
    })
        .then(response => response.data)
        .then(history => {
            const tbody = document.getElementById('history-body');
            tbody.innerHTML = '';

            const entries = Object.entries(history || {}).sort(([, a], [, b]) => {
                const left = Date.parse(a?.created_at || '') || 0;
                const right = Date.parse(b?.created_at || '') || 0;
                return right - left;
            });

            entries.forEach(([id, data]) => {
                const row = document.createElement('tr');
                row.className = data.is_active ? 'is-active' : '';
                const totalVolume = Object.values(data.muscles)
                    .reduce((sum, muscle) => sum + muscle.weekly_sets, 0);
                const activeLabel = data.is_active
                    ? `Deactivate active volume plan ${id}`
                    : `Activate volume plan ${id}`;
                
                row.innerHTML = `
                    <td>${new Date(data.created_at).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-sm btn-link activate-plan"
                                type="button"
                                data-plan-id="${id}"
                                data-active="${data.is_active ? 'true' : 'false'}"
                                aria-label="${activeLabel}"
                                title="${activeLabel}">
                            <i class="${data.is_active ? 'fas' : 'far'} fa-star" aria-hidden="true"></i>
                        </button>
                    </td>
                    <td>${data.training_days} days</td>
                    <td>${totalVolume} sets</td>
                    <td>
                        <button class="btn btn-sm btn-primary load-plan" 
                                data-plan-id="${id}">Load</button>
                        <button class="btn btn-sm btn-danger delete-plan ms-1" 
                                data-plan-id="${id}">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
            updateActivePlanSummary(entries);
            if (!entries.length) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center text-muted">No saved volume plans yet.</td>
                    </tr>
                `;
                updateActivePlanSummary([]);
            }
        })
        .catch(error => {
            console.error('Error loading volume history:', error);
            const tbody = document.getElementById('history-body');
            if (tbody) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center text-danger">Failed to load volume history.</td>
                    </tr>
                `;
            }
            showToast('error', 'Failed to load saved volume plans. Please try again.');
        });
}

function exportToExcel() {
    const trainingSelect = document.getElementById('training-days');
    const trainingDays = Math.max(parseInt(trainingSelect?.value, 10) || 3, 1);
    const volumes = collectVolumes();

    const data = {
        mode: currentMode,
        training_days: trainingDays,
        volumes
    };
    
    fetch('/api/export_volume_excel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `volume_plan_${new Date().toISOString().slice(0,10)}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    })
    .catch(error => {
        console.error('Error exporting to Excel:', error);
        showToast('error', 'Failed to export plan. Please try again.');
    });
} 

function parseConfig(root) {
    const safeParse = (value, fallback) => {
        try {
            return value ? JSON.parse(value) : fallback;
        } catch (error) {
            console.error('Failed to parse volume splitter config value:', error);
            return fallback;
        }
    };

    const defaultMode = (root.dataset.defaultMode || 'basic').toLowerCase() === 'advanced' ? 'advanced' : 'basic';

    return {
        basicMuscles: safeParse(root.dataset.basicMuscles, []),
        advancedMuscles: safeParse(root.dataset.advancedMuscles, []),
        basicRanges: safeParse(root.dataset.basicRanges, {}),
        advancedRanges: safeParse(root.dataset.advancedRanges, {}),
        defaultMode
    };
}

function initializeModeToggle(root) {
    const radios = root.querySelectorAll('input[name="volume-mode"]');
    radios.forEach(radio => {
        radio.checked = radio.value === currentMode;
        radio.addEventListener('change', event => {
            if (event.target.checked) {
                setMode(event.target.value);
            }
        });
    });
}

function setMode(newMode, prefillVolumes = null, options = {}) {
    const normalized = (newMode || 'basic').toLowerCase() === 'advanced' ? 'advanced' : 'basic';
    const previousMode = currentMode;

    if (document.querySelector('.volume-slider')) {
        modeVolumeState[previousMode] = collectVolumes();
        modeRangeState[previousMode] = collectRanges();
    }

    currentMode = normalized;

    const radios = document.querySelectorAll('input[name="volume-mode"]');
    radios.forEach(radio => {
        radio.checked = radio.value === normalized;
    });

    const volumesToApply = prefillVolumes || modeVolumeState[currentMode] || {};
    renderSliders(volumesToApply);
    modeVolumeState[currentMode] = collectVolumes();
    modeRangeState[currentMode] = collectRanges();

    if (!options.skipCalculate) {
        calculateVolume();
    }
}

function renderSliders(prefillVolumes = {}) {
    const container = document.getElementById('sliders');
    if (!container) {
        return;
    }

    const muscles = getCurrentMuscles();
    const ranges = getCurrentRanges();
    container.innerHTML = '';

    muscles.forEach((muscle, index) => {
        const value = prefillVolumes[muscle] ?? 0;
        const range = ranges[muscle] || toNumericRange();
        const row = createSliderRow(muscle, range, value, index);
        container.appendChild(row);
    });

    attachSliderListeners();
    attachSliderTooltips();
    updateAllSliderTracks();
}

function getCurrentMuscles() {
    return currentMode === 'advanced' ? volumeConfig.advancedMuscles : volumeConfig.basicMuscles;
}

function getCurrentRanges() {
    const state = currentMode === 'advanced' ? modeRangeState.advanced : modeRangeState.basic;
    const defaults = currentMode === 'advanced' ? volumeConfig.advancedRanges : volumeConfig.basicRanges;
    const muscles = getCurrentMuscles();
    const ranges = {};
    muscles.forEach(muscle => {
        if (state && state[muscle]) {
            ranges[muscle] = toNumericRange(state[muscle]);
        } else if (defaults && defaults[muscle]) {
            ranges[muscle] = toNumericRange(defaults[muscle]);
        } else {
            ranges[muscle] = toNumericRange();
        }
    });
    return ranges;
}

function createSliderRow(muscle, range, value, index) {
    const row = document.createElement('div');
    row.className = 'muscle-row mb-3';
    row.dataset.muscle = muscle;

    const initialValue = Number.isFinite(value) ? Math.max(0, Number(value)) : 0;

    // The slider's accessible name comes from the muscle-name span, not from a
    // `for=` on the wrapping label: that label also contains the live value
    // pill below, so associating it would make the name "Neck 12" and mutate it
    // on every drag. Keyed on the render index rather than a slug of `muscle`
    // because renderSliders() clears the container before each rebuild, so the
    // index is unique by construction and needs no escaping.
    const labelId = `volume-slider-label-${index}`;

    row.innerHTML = `
        <label class="form-label d-flex justify-content-between align-items-center">
            <span class="muscle-name" id="${labelId}">${muscle}</span>
            <span class="current-value volume-value-pill" data-muscle="${muscle}">${initialValue}</span>
        </label>
        <div class="d-flex flex-column flex-md-row gap-3 align-items-stretch align-items-md-center">
            <div class="slider-stack flex-fill d-flex align-items-center gap-3">
                <input type="range"
                       class="form-range volume-slider"
                       min="0"
                       max="${DEFAULT_SLIDER_MAX}"
                       step="1"
                       value="${initialValue}"
                       data-muscle="${muscle}"
                       aria-labelledby="${labelId}" />
            </div>
        </div>
    `;

    return row;
}

function attachSliderListeners() {
    document.querySelectorAll('.volume-slider').forEach(slider => {
        slider.addEventListener('input', event => {
            updateValueDisplay(event.target);
            const muscle = event.target.dataset.muscle;
            if (!modeVolumeState[currentMode]) {
                modeVolumeState[currentMode] = {};
            }
            modeVolumeState[currentMode][muscle] = parseInt(event.target.value, 10) || 0;
            updateSliderTrack(event.target, getRangeForMuscle(muscle));
            scheduleCalculate();
        });

        slider.addEventListener('change', () => {
            modeVolumeState[currentMode] = { ...collectVolumes() };
            updateSliderTrack(slider, getRangeForMuscle(slider.dataset.muscle));
            // Not silent: the `|| !standing` fallthrough still announces the
            // first failure. Arrow keys fire `change` on every keypress.
            calculateVolume({ forceAnnounce: false });
        });
    });
}

function getRangeForMuscle(muscle) {
    const ranges = getCurrentRanges();
    return ranges[muscle] || toNumericRange();
}

function updateSliderTrack(slider, range) {
    if (!slider) {
        return;
    }
    const sliderMax = Number(slider.max) || DEFAULT_SLIDER_MAX;
    const safeRange = toNumericRange(range);
    const minPercent = Math.max(0, Math.min(100, (safeRange.min / sliderMax) * 100));
    const maxPercent = Math.max(minPercent, Math.min(100, (safeRange.max / sliderMax) * 100));

    const baseColor = getComputedStyle(document.documentElement).getPropertyValue('--volume-track-bg').trim() || '#e9ecef';
    const highlightColor = getComputedStyle(document.documentElement).getPropertyValue('--volume-track-optimal').trim() || '#0d6efd';

    slider.style.background = `linear-gradient(90deg, ${baseColor} 0%, ${baseColor} ${minPercent}%, ${highlightColor} ${minPercent}%, ${highlightColor} ${maxPercent}%, ${baseColor} ${maxPercent}%, ${baseColor} 100%)`;
}

function updateAllSliderTracks() {
    document.querySelectorAll('.volume-slider').forEach(slider => {
        updateSliderTrack(slider, getRangeForMuscle(slider.dataset.muscle));
    });
}

function attachSliderTooltips() {
    if (typeof tippy !== 'function') {
        return;
    }

    const ranges = getCurrentRanges();
    document.querySelectorAll('.volume-slider').forEach(slider => {
        const muscle = slider.dataset.muscle;
        const range = ranges[muscle] || { min: 12, max: 20 };

        if (slider._tippy) {
            slider._tippy.destroy();
        }

        tippy(slider, {
            content: `
                <div class="tooltip-content">
                    <h6>${muscle}</h6>
                    <ul class="mb-0 ps-3">
                        <li>Recommended weekly sets: ${range.min}-${range.max}</li>
                        <li>Adjust slider to match your plan</li>
                    </ul>
                </div>
            `,
            allowHTML: true,
            placement: 'top'
        });
    });
}

function updateValueDisplay(slider) {
    const muscle = slider.dataset.muscle;
    const valueDisplay = document.querySelector(`.current-value[data-muscle="${escapeForSelector(muscle)}"]`);
    if (valueDisplay) {
        valueDisplay.textContent = slider.value;
    }
}

function collectVolumes() {
    const volumes = {};
    document.querySelectorAll('.volume-slider').forEach(slider => {
        const muscle = slider.dataset.muscle;
        if (!muscle) {
            return;
        }
        volumes[muscle] = parseInt(slider.value, 10) || 0;
    });
    return volumes;
}

function collectRanges() {
    return getCurrentRanges();
}

function applyServerRanges(rangeMap) {
    if (!rangeMap || typeof rangeMap !== 'object') {
        return;
    }

    const state = { ...(modeRangeState[currentMode] || {}) };
    let updatedAny = false;

    Object.entries(rangeMap).forEach(([muscle, rawRange]) => {
        const range = sanitizeRangePair(rawRange);
        state[muscle] = range;
        updatedAny = true;

        const row = document.querySelector(`.muscle-row[data-muscle="${escapeForSelector(muscle)}"]`);
        if (!row) {
            return;
        }

        const slider = row.querySelector('.volume-slider');
        if (slider) {
            updateSliderTrack(slider, range);
        }
    });

    if (updatedAny) {
        modeRangeState[currentMode] = state;
        updateAllSliderTracks();
    }
}

function handleCalculateResponse(data) {
    const payload = data || {};
    const normalizedRanges = normalizeRangeMap(payload.ranges || {});
    applyServerRanges(normalizedRanges);

    const results = payload.results || {};

    displayResults(results);
    displaySuggestions(payload.suggestions || []);

    if (!Object.keys(results).length) {
        clearResults();
    }
}

function applyStatusToRow(muscle, result, range) {
    const row = document.querySelector(`.muscle-row[data-muscle="${escapeForSelector(muscle)}"]`);
    if (!row) {
        return;
    }

    const status = result?.status || 'optimal';
    const statusClasses = ['status-low', 'status-optimal', 'status-high', 'status-excessive'];
    statusClasses.forEach(cls => row.classList.remove(cls));
    row.classList.add(`status-${status}`);

    const badge = row.querySelector('.current-value');
    if (badge) {
        const modifierMap = {
            low: 'volume-value-pill--low',
            optimal: 'volume-value-pill--optimal',
            high: 'volume-value-pill--high',
            excessive: 'volume-value-pill--excessive'
        };
        badge.classList.remove(
            'volume-value-pill--low',
            'volume-value-pill--optimal',
            'volume-value-pill--high',
            'volume-value-pill--excessive'
        );
        const modifier = modifierMap[status];
        if (modifier) {
            badge.classList.add(modifier);
        }
    }
}

function handleHistoryClick(event) {
    const activateBtn = event.target.closest('.activate-plan');
    if (activateBtn) {
        const planId = activateBtn.dataset.planId;
        if (planId) {
            toggleActivePlan(planId, activateBtn.dataset.active === 'true');
        }
        return;
    }

    const loadBtn = event.target.closest('.load-plan');
    if (loadBtn) {
        const planId = loadBtn.dataset.planId;
        if (planId) {
            loadPlan(planId);
        }
        return;
    }
    
    const deleteBtn = event.target.closest('.delete-plan');
    if (deleteBtn) {
        const planId = deleteBtn.dataset.planId;
        if (planId) {
            deletePlan(planId);
        }
    }
}

function toggleActivePlan(planId, isActive) {
    const endpoint = `/api/volume_plan/${planId}/${isActive ? 'deactivate' : 'activate'}`;
    api.post(endpoint, null, {
        headers: JSON_REQUEST_HEADERS,
        showLoading: false,
        showErrorToast: false,
        useDefaultHeaders: false
    })
        .then(response => response.data)
        .then(() => {
            showToast('success', isActive ? `Plan #${planId} deactivated.` : `Plan #${planId} activated for Plan tab.`);
            loadVolumeHistory();
        })
        .catch(error => {
            console.error('Error toggling active plan:', error);
            showToast('error', isActive ? 'Failed to deactivate plan.' : 'Failed to activate plan.');
        });
}

function updateActivePlanSummary(entries) {
    const summary = document.getElementById('volume-active-summary');
    if (!summary) {
        return;
    }

    const activeEntry = entries.find(([, data]) => data?.is_active);
    if (!activeEntry) {
        summary.textContent = 'No active plan - activate one to drive the Plan tab.';
        summary.classList.remove('is-active');
        return;
    }

    const [id, data] = activeEntry;
    const targetedCount = Object.values(data.muscles || {})
        .filter(muscle => Number(muscle.weekly_sets) > 0)
        .length;
    summary.textContent = `Active plan: #${id}, ${data.training_days}-day ${data.mode || 'basic'} split (${targetedCount} muscles targeted)`;
    summary.classList.add('is-active');
}

function scheduleCalculate() {
    if (calculateDebounceId) {
        clearTimeout(calculateDebounceId);
    }
    // Not silent: the `|| !standing` fallthrough still announces the first failure.
    calculateDebounceId = window.setTimeout(() => calculateVolume({ forceAnnounce: false }), 300);
}

function clearResults() {
    const resultsSection = document.querySelector('.results-section');
    const suggestionsSection = document.querySelector('.ai-suggestions-section');
    const resultsBody = document.getElementById('results-body');
    const suggestionsContainer = document.querySelector('.suggestions-container');

    resultsSection?.classList.add('d-none');
    suggestionsSection?.classList.add('d-none');

    if (resultsBody) {
        resultsBody.innerHTML = '';
    }

    if (suggestionsContainer) {
        suggestionsContainer.innerHTML = '';
    }

    document.querySelectorAll('.muscle-row').forEach(row => {
        row.classList.remove('status-low', 'status-optimal', 'status-high', 'status-excessive');
        const badge = row.querySelector('.current-value');
        if (badge) {
            badge.classList.remove(
                'volume-value-pill--low',
                'volume-value-pill--optimal',
                'volume-value-pill--high',
                'volume-value-pill--excessive'
            );
        }
    });
}

function escapeForSelector(value) {
    if (window.CSS && typeof window.CSS.escape === 'function') {
        return window.CSS.escape(value);
    }
    return value.replace(/"/g, '\\"');
}
