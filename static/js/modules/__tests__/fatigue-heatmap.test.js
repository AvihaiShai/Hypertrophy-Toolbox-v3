import { describe, it, expect } from 'vitest';

import {
    NEUTRAL_CLASS,
    UNMAPPED_REGIONS,
    bandClass,
    channelsWithData,
    indexRowsByMuscle,
    regionTitle,
    resolveRegionBand,
} from '../fatigue-heatmap.js';

// Shape mirrors utils.fatigue_data._merge_muscle_rows output.
function row(muscle, planned, logged) {
    return { muscle, planned, logged };
}

function side(band, percent) {
    return { band, percent_of_mrv: percent, score: 1, has_landmarks: true };
}

describe('resolveRegionBand', () => {
    const rows = indexRowsByMuscle([
        row('Chest', side('heavy', 78.2), null),
        row('Middle-Shoulder', side('light', 12), side('very_heavy', 104)),
    ]);

    it('returns the band for a mapped region with data', () => {
        const result = resolveRegionBand('chest', rows, 'planned');
        expect(result.muscle).toBe('Chest');
        expect(result.band).toBe('heavy');
        expect(result.hasData).toBe(true);
    });

    it('returns no band for a region no fatigue muscle covers', () => {
        for (const key of UNMAPPED_REGIONS) {
            const result = resolveRegionBand(key, rows, 'planned');
            expect(result.muscle).toBeNull();
            expect(result.band).toBeNull();
            expect(result.hasData).toBe(false);
        }
    });

    it('returns no band when the muscle has no row at all', () => {
        const result = resolveRegionBand('calves', rows, 'planned');
        expect(result.muscle).toBe('Calves');
        expect(result.band).toBeNull();
    });

    it('is channel-independent: an empty logged side does not blank planned', () => {
        expect(resolveRegionBand('chest', rows, 'logged').band).toBeNull();
        expect(resolveRegionBand('chest', rows, 'planned').band).toBe('heavy');
    });

    it('returns the requested channel when the two differ', () => {
        expect(resolveRegionBand('front-deltoid', rows, 'planned').band).toBe('light');
        expect(resolveRegionBand('front-deltoid', rows, 'logged').band).toBe('very_heavy');
    });

    it('paints both delts identically from the one Middle-Shoulder row', () => {
        const front = resolveRegionBand('front-deltoid', rows, 'logged');
        const rear = resolveRegionBand('rear-deltoid', rows, 'logged');
        expect(front).toEqual(rear);
    });

    // The assertion that makes "no new math" testable: a helper that re-derived
    // the band from score or percent_of_mrv would normalise this away.
    it('passes the server band through verbatim and never re-derives it', () => {
        const odd = indexRowsByMuscle([row('Chest', side('nonsense', 999), null)]);
        expect(resolveRegionBand('chest', odd, 'planned').band).toBe('nonsense');
    });
});

describe('bandClass', () => {
    it('maps each classifier band to its palette class', () => {
        expect(bandClass('light')).toBe('fatigue-light');
        expect(bandClass('moderate')).toBe('fatigue-moderate');
        expect(bandClass('heavy')).toBe('fatigue-heavy');
        expect(bandClass('very_heavy')).toBe('fatigue-very-heavy');
    });

    it('falls back to the neutral class for null and unknown bands', () => {
        expect(bandClass(null)).toBe(NEUTRAL_CLASS);
        expect(bandClass('nonsense')).toBe(NEUTRAL_CLASS);
    });

});

describe('regionTitle', () => {
    it('carries the percentage so colour is not the only signal', () => {
        const result = { muscle: 'Chest', band: 'heavy', percentOfMrv: 78.2, hasData: true };
        expect(regionTitle('chest', result)).toBe(
            'Chest — heavy · 78% of typical recoverable range',
        );
    });

    it('says "very heavy", matching the shipped band vocabulary', () => {
        const result = { muscle: 'Glutes', band: 'very_heavy', percentOfMrv: 104, hasData: true };
        expect(regionTitle('gluteal', result)).toContain('very heavy');
        expect(regionTitle('gluteal', result)).not.toContain('very_heavy');
    });

    it('distinguishes "no volume yet" from "no reference range exists"', () => {
        const noVolume = { muscle: 'Chest', band: null, percentOfMrv: null, hasData: false };
        expect(regionTitle('chest', noVolume)).toBe('Chest — no volume in this window');

        const noRange = { muscle: null, band: null, percentOfMrv: null, hasData: false };
        expect(regionTitle('neck', noRange)).toBe('Neck — no typical range yet');
        expect(regionTitle('lower-back', noRange)).toBe('Lower back — no typical range yet');
    });

});

describe('channelsWithData', () => {
    it('reports only the channels that actually carry a reading', () => {
        const rows = [row('Chest', side('heavy', 78), null)];
        expect(channelsWithData(rows)).toEqual(['planned']);
    });

    it('reports both when both sides are populated', () => {
        const rows = [row('Chest', side('heavy', 78), side('light', 10))];
        expect(channelsWithData(rows)).toEqual(['planned', 'logged']);
    });

    it('reports none when the rows carry no readings', () => {
        expect(channelsWithData([row('Chest', null, null)])).toEqual([]);
        expect(channelsWithData([])).toEqual([]);
    });
});
