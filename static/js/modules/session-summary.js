import { onSummaryReady, refreshSummary, volumeRow } from './summary-helpers.js';
import { getSessionWarningBadge } from './session-summary-helpers.js';

function updateSessionSummary() {
    const params = new URLSearchParams({ contribution_mode: document.getElementById('contribution-mode').value });
    const locationParams = new URLSearchParams(window.location.search);
    for (const key of ['routine', 'start_date', 'end_date']) {
        if (locationParams.has(key)) params.set(key, locationParams.get(key));
    }

    return refreshSummary('session_summary', params, row =>
        volumeRow(row, false, getSessionWarningBadge(row.warning_level, row.effective_per_session)));
}

window.updateSessionSummary = updateSessionSummary;
onSummaryReady(updateSessionSummary);
