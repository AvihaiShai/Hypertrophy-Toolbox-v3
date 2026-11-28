// Shared presentation and refresh behavior for the two Plan volume summaries.
import { api } from './fetch-wrapper.js';
import { escapeHtml } from './exercise-helpers.js';

// Volume classification details based on effective sets.
export function getVolumeDetails(effectiveSets) {
    let volumeClass, volumeLabel;

    if (effectiveSets < 10) {
        volumeClass = 'low-volume';
        volumeLabel = 'Low Volume';
    } else if (effectiveSets < 20) {
        volumeClass = 'medium-volume';
        volumeLabel = 'Medium Volume';
    } else if (effectiveSets < 30) {
        volumeClass = 'high-volume';
        volumeLabel = 'High Volume';
    } else {
        volumeClass = 'ultra-volume';
        volumeLabel = 'Excessive Volume';
    }

    const ranges = {
        'Low Volume': 'Below 10 effective sets',
        'Medium Volume': '10 to below 20 effective sets',
        'High Volume': '20 to below 30 effective sets',
        'Excessive Volume': '30+ effective sets'
    };

    return {
        class: volumeClass,
        label: volumeLabel,
        tooltip: `${volumeLabel}: ${ranges[volumeLabel]} (Current: ${effectiveSets.toFixed(1)} effective sets)`
    };
}

// Movement-pattern display name formatting.
export function formatPatternName(pattern) {
    const nameMap = {
        'squat': 'Squat',
        'hinge': 'Hinge',
        'horizontal_push': 'Horizontal Push',
        'horizontal_pull': 'Horizontal Pull',
        'vertical_push': 'Vertical Push',
        'vertical_pull': 'Vertical Pull',
        'core_static': 'Core (Static)',
        'core_dynamic': 'Core (Dynamic)',
        'upper_isolation': 'Upper Isolation',
        'lower_isolation': 'Lower Isolation',
        'other': 'Other'
    };
    return nameMap[pattern] || pattern.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

export function isWrappedApiResponse(payload) {
    return Boolean(
        payload &&
        typeof payload === 'object' &&
        !Array.isArray(payload) &&
        'data' in payload &&
        (payload.ok === true || payload.status === 'success' || payload.success === true)
    );
}

export function isApiFailure(payload) {
    return Boolean(
        payload &&
        typeof payload === 'object' &&
        (payload.ok === false || payload.success === false)
    );
}

export function unwrapApiPayload(payload) {
    return isWrappedApiResponse(payload) ? payload.data : payload;
}

export function getApiErrorMessage(payload, fallbackMessage) {
    if (!payload || typeof payload !== 'object') {
        return fallbackMessage;
    }

    if (payload.error && typeof payload.error === 'object' && typeof payload.error.message === 'string') {
        return payload.error.message;
    }

    if (typeof payload.error === 'string') {
        return payload.error;
    }

    if (typeof payload.message === 'string' && payload.message.trim()) {
        return payload.message;
    }

    return fallbackMessage;
}

export function getCategoryTooltip(category) {
    const tooltips = {
        'Mechanic': 'Classification based on joint involvement in the exercise',
        'Utility': 'Classification based on exercise role in training',
        'Force': 'Classification based on primary force direction'
    };
    return tooltips[category] || '';
}

export function getSubcategoryTooltip(category, subcategory) {
    const tooltips = {
        'Mechanic': {
            'Compound': 'Multi-joint exercises like squats and bench press',
            'Isolated': 'Single-joint exercises focusing on specific muscles'
        },
        'Utility': {
            'Auxiliary': 'Supportive exercises that complement main lifts',
            'Basic': 'Foundational exercises targeting major muscle groups'
        },
        'Force': {
            'Push': 'Exercises involving pushing motions away from body',
            'Pull': 'Exercises involving pulling motions toward body'
        }
    };
    return tooltips[category]?.[subcategory] || '';
}

export function replaceSummaryRows(tableBody, html) {
    const selector = '[data-bs-toggle="tooltip"]';
    tableBody.querySelectorAll(selector).forEach(element => {
        bootstrap.Tooltip.getInstance(element)?.dispose();
    });
    tableBody.innerHTML = html;
    tableBody.querySelectorAll(selector).forEach(element => {
        bootstrap.Tooltip.getOrCreateInstance(element);
    });
}

export async function fetchSummaryData(url) {
    const result = await api.get(url, {
        headers: { Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
        showLoading: false,
        showErrorToast: false,
        useDefaultHeaders: false,
        retries: 0,
    });
    if (isApiFailure(result)) throw new Error(getApiErrorMessage(result, 'Unable to load summary data.'));
    return unwrapApiPayload(result);
}

// A projection belongs to the HTML request. Weekly also has an independent Pattern request.
const outcomes = { tables: 'pending', pattern: 'pending' };

export function setSummaryOutcome(source, state) {
    outcomes[source] = state;
    const empty = document.getElementById('summary-empty');
    empty.hidden = !(outcomes.tables === 'empty' &&
        document.querySelector('[data-projection-state]').dataset.projectionState === 'empty' &&
        (!document.getElementById('pattern-coverage-container') || outcomes.pattern === 'empty'));
}

function messageRow(text, columns) {
    return `<tr role="row"><td role="cell" colspan="${columns}"><span role="status">${text}</span></td></tr>`;
}

function categoryRow(category) {
    return `<tr role="row">
        <td role="cell" data-label="Category"><span data-bs-toggle="tooltip" title="${escapeHtml(getCategoryTooltip(category.category))}">${escapeHtml(category.category)}</span></td>
        <td role="cell" data-label="Subcategory"><span data-bs-toggle="tooltip" title="${escapeHtml(getSubcategoryTooltip(category.category, category.subcategory))}">${escapeHtml(category.subcategory)}</span></td>
        <td role="cell" data-label="Total Exercises" class="is-num">${escapeHtml(category.total_exercises)}</td>
    </tr>`;
}

export function volumeRow(row, weekly, warning = null) {
    const effectiveSets = row.effective_sets ?? row.total_sets ?? 0;
    const rawSets = row.raw_sets ?? row.total_sets ?? 0;
    const displayVolume = row.total_volume ?? row.total_weight ?? 0;
    const muscleDisplay = window.FilterViewMode?.transformMuscleDisplay(row.muscle_group) || row.muscle_group || 'N/A';
    const volume = getVolumeDetails(effectiveSets);
    return `<tr role="row">
        ${weekly ? '' : `<td role="cell" data-label="Routine">${escapeHtml(row.routine || 'N/A')}</td>`}
        <td role="cell" data-label="Muscle Group" data-raw-value="${escapeHtml(row.muscle_group)}">${escapeHtml(muscleDisplay)}</td>
        <td role="cell" data-label="Effective Sets" class="is-num">${effectiveSets.toFixed(1)}</td>
        <td role="cell" data-label="Raw Sets" class="is-num">${rawSets.toFixed(1)}</td>
        ${weekly ? `<td role="cell" data-label="Routines" class="is-num">${escapeHtml(row.frequency ?? 0)}</td>` : ''}
        <td role="cell" data-label="Total Volume" class="is-num">${displayVolume.toFixed(0)}</td>
        <td role="cell" data-label="${weekly ? 'Volume Classification' : 'Volume Status'}">
            <div class="summary-status">
                <span class="volume-classification" data-bs-toggle="tooltip" title="${escapeHtml(volume.tooltip)}">
                    <span class="volume-badge ${volume.class}">${volume.label}</span>
                </span>
                ${warning ? `<span class="session-warning" data-warning="${escapeHtml(row.warning_level)}"
                    data-bs-toggle="tooltip" title="${escapeHtml(warning.tooltip)}">${escapeHtml(warning.label)}</span>` : ''}
            </div>
        </td>
    </tr>`;
}

let latestRequest = 0;

export async function refreshSummary(key, params, renderRow) {
    const request = ++latestRequest;
    setSummaryOutcome('tables', 'pending');
    const table = document.getElementById(key.replace('_', '-') + '-table');
    const categories = document.getElementById('categories-table-body');
    replaceSummaryRows(table, messageRow('Loading volume…', 6));
    try {
        const data = await fetchSummaryData(`/${key}?${params}`);
        if (request !== latestRequest) return;
        if (![data?.[key], data?.categories, data?.isolated_muscles].every(Array.isArray)) {
            throw new Error('Incomplete summary response');
        }
        const rows = data[key];
        replaceSummaryRows(table, rows.length ? rows.map(renderRow).join('') : messageRow('No data available.', 6));
        replaceSummaryRows(categories, data.categories.length ? data.categories.map(categoryRow).join('') :
            messageRow('No categories data available.', 3));
        setSummaryOutcome('tables', rows.length || data.categories.length || data.isolated_muscles.length ? 'populated' : 'empty');
    } catch (error) {
        if (request !== latestRequest) return;
        console.error('Error fetching data:', error);
        replaceSummaryRows(table, messageRow('Failed to load data.', 6));
        setSummaryOutcome('tables', 'unavailable');
    }
}

export function onSummaryReady(update) {
    document.addEventListener('DOMContentLoaded', () => {
        document.addEventListener('filterViewModeChanged', () => {
            // The global isolated rows stay server-rendered across contribution changes.
            document.querySelectorAll('td[data-label="Isolated Muscle"]').forEach(cell => {
                const raw = cell.dataset.rawValue ?? cell.textContent.trim();
                cell.dataset.rawValue = raw;
                cell.textContent = window.FilterViewMode?.transformIsolatedMuscleDisplay(raw) ?? raw;
            });
            update();
        });
        update();
    });
}
