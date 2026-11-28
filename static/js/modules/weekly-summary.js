import { escapeHtml } from './exercise-helpers.js';
import {
    fetchSummaryData, formatPatternName, onSummaryReady, refreshSummary, setSummaryOutcome, volumeRow,
} from './summary-helpers.js';

const corePatterns = ['squat', 'hinge', 'horizontal_push', 'horizontal_pull', 'vertical_push', 'vertical_pull'];
let patternState = 'initial';

function patternGroup(label, patterns, totals) {
    if (!patterns.length) return '';
    return `<h4>${label}</h4><ul class="pattern-chips" aria-label="${label}">${patterns.map(pattern =>
        `<li class="ui-chip">${escapeHtml(formatPatternName(pattern))} <b>${escapeHtml(totals[pattern] ?? 0)}</b></li>`
    ).join('\n')}</ul>`;
}

function patternCoverage(data) {
    const { min, max } = data.ideal_sets_range;
    const additional = Object.keys(data.total).filter(pattern => !corePatterns.includes(pattern));
    const routines = Object.entries(data.sets_per_routine).map(([name, sets]) => {
        const status = sets < min ? 'Below target' : sets > max ? 'Above target' : 'Within target';
        return `<li class="ui-chip">${escapeHtml(name)} <b>${escapeHtml(sets)} sets</b> · ${status}</li>`;
    });
    const warnings = data.warnings.map(warning =>
        `<li><strong>${escapeHtml(warning.message)}</strong> <span class="pattern-priority">${escapeHtml(warning.level)} priority</span>
            <p>${escapeHtml(warning.description)}</p></li>`);
    return `${warnings.length ? `<ul class="pattern-warnings" aria-label="Pattern warnings">${warnings.join('')}</ul>` : ''}
        <div class="pattern-groups"><section><h3>Total Sets by Movement Pattern</h3>
            ${patternGroup('Core patterns', corePatterns, data.total)}
            ${patternGroup('Additional patterns', additional, data.total)}
        </section><section><h3>Sets per Routine</h3><ul class="pattern-chips">${routines.join('')}</ul>
            <p>Target ${escapeHtml(min)}–${escapeHtml(max)} sets</p>
        </section></div>`;
}

async function updatePatternCoverage() {
    patternState = 'pending';
    setSummaryOutcome('pattern', patternState);
    const container = document.getElementById('pattern-coverage-container');
    container.textContent = 'Loading pattern coverage…';
    try {
        const data = await fetchSummaryData('/api/pattern_coverage');
        // A caught database read returns an empty success envelope without a target range.
        if (!Number.isFinite(data?.ideal_sets_range?.min) || !Number.isFinite(data.ideal_sets_range.max)) {
            patternState = 'unavailable';
        } else if (Object.keys(data.total).length || Object.keys(data.sets_per_routine).length) {
            container.innerHTML = patternCoverage(data);
            patternState = 'populated';
        } else {
            container.textContent = 'No exercises in your workout plan yet. Add exercises to see pattern coverage analysis.';
            patternState = 'empty';
        }
    } catch (error) {
        console.error('Error fetching pattern coverage:', error);
        patternState = 'unavailable';
    }
    if (patternState === 'unavailable') container.textContent = 'Unable to load pattern coverage analysis.';
    setSummaryOutcome('pattern', patternState);
}

function updateWeeklySummary() {
    if (patternState === 'initial' || patternState === 'unavailable') updatePatternCoverage();
    const params = new URLSearchParams({ contribution_mode: document.getElementById('contribution-mode').value });
    return refreshSummary('weekly_summary', params, row => volumeRow(row, true));
}

window.updateWeeklySummary = updateWeeklySummary;
onSummaryReady(updateWeeklySummary);
