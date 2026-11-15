// @vitest-environment jsdom
import { afterEach, expect, it, vi } from 'vitest';
import { Tooltip } from 'bootstrap';
import { replaceSummaryRows } from '../summary-helpers.js';

afterEach(() => {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(element => {
        Tooltip.getInstance(element)?.dispose();
    });
    document.body.innerHTML = '';
    vi.unstubAllGlobals();
});

it('replaces rows without leaving an open tip or replacing persistent instances', () => {
    vi.stubGlobal('bootstrap', { Tooltip });
    document.body.innerHTML = `
        <button data-bs-toggle="tooltip" title="Persistent">Header</button>
        <table><tbody><tr><td data-bs-toggle="tooltip" title="Old">Old</td></tr></tbody></table>`;
    const header = document.querySelector('button');
    const persistent = Tooltip.getOrCreateInstance(header, { animation: false });
    const body = document.querySelector('tbody');
    const oldCell = body.querySelector('td');
    const oldTip = Tooltip.getOrCreateInstance(oldCell, { animation: false });
    oldTip.show();
    expect(document.querySelectorAll('.tooltip.show')).toHaveLength(1);

    replaceSummaryRows(body, '<tr><td data-bs-toggle="tooltip" title="New">New</td></tr>');

    expect(Tooltip.getInstance(oldCell)).toBeNull();
    expect(document.querySelectorAll('.tooltip')).toHaveLength(0);
    expect(Tooltip.getInstance(body.querySelector('td'))).not.toBeNull();
    expect(Tooltip.getInstance(header)).toBe(persistent);
});
