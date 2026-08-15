// @vitest-environment jsdom
//
// Packet A of Testing Strategy Phase 3 step 12
// (docs/testing_phase3/STEP12_JS_UNIT_GATE0.md §9).
//
// Covers the KI-005 Workout Controls persistence contract. Case IDs (A1..A35)
// map to §9.2 and the mutation matrix in §9.8.
//
// This module imports nothing, so there is deliberately no vi.mock here.

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import {
    WORKOUT_CONTROL_IDS,
    WORKOUT_CONTROL_DEFAULTS,
    beginHydration,
    endHydration,
    withHydrationSuppressed,
    saveWorkoutControls,
    applyWorkoutControlDefaults,
    restoreWorkoutControls,
    clearWorkoutControls,
} from '../workout-controls-persistence.js';

const STORAGE_KEY = 'hypertrophy_workout_controls_v1';

// Copied from templates/workout_plan.html lines 88-108. The min/max attributes
// are load-bearing: declaredRange() reads them off these elements, so a fixture
// that loses them makes every bounds case pass vacuously. A31 pins them.
// class/name/placeholder/aria-label are omitted - the module never reads them.
const CONTROLS_FIXTURE = `
    <input type="number" id="weight" min="0" step="any" value="25">
    <input type="number" id="sets" min="1" value="3">
    <input type="number" id="rir" min="0" max="10" value="3">
    <input type="number" id="rpe" min="1" max="10" step="0.5" value="7">
    <input type="number" id="min_rep" min="1" value="6">
    <input type="number" id="max_rep_range" min="1" value="8">
`;

const el = (id) => document.getElementById(id);
const seedRaw = (raw) => sessionStorage.setItem(STORAGE_KEY, raw);
const seed = (record) => seedRaw(JSON.stringify(record));
const storedRecord = () => JSON.parse(sessionStorage.getItem(STORAGE_KEY));

/**
 * Drive every control to a value that is NOT its pinned default, so a later
 * "fell back to the default" assertion proves an active write rather than an
 * untouched field.
 */
const setAllToNonDefaults = () => {
    el('weight').value = '999';
    el('sets').value = '9';
    el('rir').value = '9';
    el('rpe').value = '9';
    el('min_rep').value = '9';
    el('max_rep_range').value = '9';
};

const currentValues = () => ({
    weight: el('weight').value,
    sets: el('sets').value,
    rir: el('rir').value,
    rpe: el('rpe').value,
    min_rep: el('min_rep').value,
    max_rep_range: el('max_rep_range').value,
});

beforeEach(() => {
    // Primary reset for the module-level `hydrating` flag, through the module's
    // own exported API rather than by reaching into its internals (§9.4).
    endHydration();
    document.body.innerHTML = CONTROLS_FIXTURE;
    sessionStorage.clear();
    localStorage.clear();
});

afterEach(() => {
    // restoreAllMocks first, so the throwing-storage spies cannot break teardown.
    vi.restoreAllMocks();
    endHydration();
    sessionStorage.clear();
    localStorage.clear();
});

describe('A1-A2 exported constants', () => {
    it('A1: WORKOUT_CONTROL_IDS is exactly the six controls, in order', () => {
        expect(WORKOUT_CONTROL_IDS).toEqual([
            'weight', 'sets', 'rir', 'rpe', 'min_rep', 'max_rep_range',
        ]);
    });

    it('A2: WORKOUT_CONTROL_DEFAULTS is the pinned template defaults, all strings', () => {
        expect(WORKOUT_CONTROL_DEFAULTS).toEqual({
            weight: '25',
            sets: '3',
            rir: '3',
            rpe: '7',
            min_rep: '6',
            max_rep_range: '8',
        });
        for (const value of Object.values(WORKOUT_CONTROL_DEFAULTS)) {
            expect(typeof value).toBe('string');
        }
    });
});

describe('A3-A7 hydration guard (OWNER-1)', () => {
    it('A3: saveWorkoutControls is a no-op while hydrating', () => {
        beginHydration();
        saveWorkoutControls();
        expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
    });

    it('A4: endHydration re-arms saving', () => {
        beginHydration();
        endHydration();
        saveWorkoutControls();
        expect(sessionStorage.getItem(STORAGE_KEY)).not.toBeNull();
    });

    it('A5: withHydrationSuppressed passes through the callback return value', () => {
        expect(withHydrationSuppressed(() => 'sentinel')).toBe('sentinel');
    });

    it('A6: withHydrationSuppressed restores the PREVIOUS flag, not false', () => {
        beginHydration();
        withHydrationSuppressed(() => {});
        // Still hydrating: the nested call must not have disarmed the guard.
        saveWorkoutControls();
        expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
    });

    it('A7: withHydrationSuppressed restores the flag when the callback throws, and rethrows', () => {
        expect(() => withHydrationSuppressed(() => {
            throw new Error('boom');
        })).toThrow('boom');

        // Flag restored to its pre-call value (false), so saving works again.
        saveWorkoutControls();
        expect(sessionStorage.getItem(STORAGE_KEY)).not.toBeNull();
    });
});

describe('A8-A13 saveWorkoutControls (OWNER-3)', () => {
    it('A8: writes exactly one key, named hypertrophy_workout_controls_v1', () => {
        saveWorkoutControls();
        expect(sessionStorage.length).toBe(1);
        expect(sessionStorage.key(0)).toBe('hypertrophy_workout_controls_v1');
    });

    it('A9: the stored record holds exactly the six control ids', () => {
        saveWorkoutControls();
        expect(Object.keys(storedRecord())).toEqual([
            'weight', 'sets', 'rir', 'rpe', 'min_rep', 'max_rep_range',
        ]);
    });

    it('A10: values are read from the live DOM, not from the defaults', () => {
        el('weight').value = '77';
        el('rir').value = '1';
        saveWorkoutControls();
        expect(storedRecord().weight).toBe('77');
        expect(storedRecord().rir).toBe('1');
    });

    it('A11: nothing is written to localStorage (criterion 6)', () => {
        saveWorkoutControls();
        expect(localStorage.length).toBe(0);
    });

    it('A12: with no control inputs present, nothing is written', () => {
        document.body.innerHTML = '';
        saveWorkoutControls();
        expect(sessionStorage.length).toBe(0);
    });

    it('A13: with only some inputs present, only those are recorded', () => {
        document.body.innerHTML = `
            <input type="number" id="weight" min="0" value="25">
            <input type="number" id="sets" min="1" value="3">
        `;
        saveWorkoutControls();
        expect(Object.keys(storedRecord())).toEqual(['weight', 'sets']);
    });
});

describe('A14-A15 applyWorkoutControlDefaults (PR-1)', () => {
    it('A14: writes the pinned defaults to all six inputs', () => {
        setAllToNonDefaults();
        applyWorkoutControlDefaults();
        expect(currentValues()).toEqual({
            weight: '25',
            sets: '3',
            rir: '3',
            rpe: '7',
            min_rep: '6',
            max_rep_range: '8',
        });
    });

    it('A15: does not write to storage', () => {
        applyWorkoutControlDefaults();
        expect(sessionStorage.length).toBe(0);
    });
});

describe('A16-A28 restoreWorkoutControls (criteria 8/9, TS-7, OWNER-5, OWNER-1.1/.2)', () => {
    it('A16: a fully valid record restores all six, saved-wins over the rendered values', () => {
        setAllToNonDefaults();
        seed({
            weight: '100', sets: '5', rir: '2',
            rpe: '8', min_rep: '10', max_rep_range: '12',
        });

        const result = restoreWorkoutControls();

        expect(currentValues()).toEqual({
            weight: '100', sets: '5', rir: '2',
            rpe: '8', min_rep: '10', max_rep_range: '12',
        });
        expect(result.restored).toEqual([
            'weight', 'sets', 'rir', 'rpe', 'min_rep', 'max_rep_range',
        ]);
    });

    it('A17: an ABSENT record leaves the rendered values untouched and restores nothing', () => {
        setAllToNonDefaults();

        const result = restoreWorkoutControls();

        // readRecord() returns null for an absent key, and restoreWorkoutControls
        // early-returns without touching a single field. This is NOT the same as
        // the malformed case in A18 - see the packet's evidence note.
        expect(currentValues()).toEqual({
            weight: '999', sets: '9', rir: '9',
            rpe: '9', min_rep: '9', max_rep_range: '9',
        });
        expect(result.restored).toEqual([]);
    });

    it('A18: a MALFORMED record falls every field back to its pinned default', () => {
        setAllToNonDefaults();
        seedRaw('{not json');

        const result = restoreWorkoutControls();

        expect(currentValues()).toEqual({
            weight: '25', sets: '3', rir: '3',
            rpe: '7', min_rep: '6', max_rep_range: '8',
        });
        expect(result.restored).toEqual([]);
    });

    it('A19: a stored ARRAY is treated as an unusable record, every field defaults', () => {
        setAllToNonDefaults();
        seed([1, 2, 3]);

        const result = restoreWorkoutControls();

        expect(currentValues().weight).toBe('25');
        expect(currentValues().rir).toBe('3');
        expect(result.restored).toEqual([]);
    });

    it('A20: a stored JSON null is treated as an unusable record, every field defaults', () => {
        setAllToNonDefaults();
        seedRaw('null');

        const result = restoreWorkoutControls();

        expect(currentValues().weight).toBe('25');
        expect(currentValues().rir).toBe('3');
        expect(result.restored).toEqual([]);
    });

    it('A21: fallback is PER FIELD - a valid field survives an invalid sibling', () => {
        setAllToNonDefaults();
        seed({ weight: '100', rir: 'abc' });

        const result = restoreWorkoutControls();

        expect(el('weight').value).toBe('100');   // valid: stored value wins
        expect(el('rir').value).toBe('3');        // invalid: pinned default
        expect(el('sets').value).toBe('3');       // absent: pinned default
        expect(result.restored).toEqual(['weight']);
    });

    it('A22: an empty or whitespace-only stored value falls back', () => {
        setAllToNonDefaults();
        seed({ weight: '', sets: '   ' });

        const result = restoreWorkoutControls();

        expect(el('weight').value).toBe('25');
        expect(el('sets').value).toBe('3');
        expect(result.restored).toEqual([]);
    });

    it('A23: a boolean or object stored value falls back', () => {
        setAllToNonDefaults();
        seed({ weight: true, sets: { nested: 1 } });

        const result = restoreWorkoutControls();

        expect(el('weight').value).toBe('25');
        expect(el('sets').value).toBe('3');
        expect(result.restored).toEqual([]);
    });

    it('A24: rir above its declared max=10 falls back (OWNER-5)', () => {
        setAllToNonDefaults();
        seed({ rir: '11' });

        const result = restoreWorkoutControls();

        expect(el('rir').value).toBe('3');
        expect(result.restored).toEqual([]);
    });

    it('A25: rpe above its declared max=10 falls back (OWNER-5)', () => {
        setAllToNonDefaults();
        seed({ rpe: '10.5' });

        const result = restoreWorkoutControls();

        expect(el('rpe').value).toBe('7');
        expect(result.restored).toEqual([]);
    });

    it('A26: values below a declared min fall back', () => {
        setAllToNonDefaults();
        seed({ weight: '-1', sets: '0' });

        const result = restoreWorkoutControls();

        expect(el('weight').value).toBe('25');
        expect(el('sets').value).toBe('3');
        expect(result.restored).toEqual([]);
    });

    it('A27: numeric (non-string) stored values are accepted and applied as strings', () => {
        setAllToNonDefaults();
        seed({ weight: 100, sets: 5 });

        const result = restoreWorkoutControls();

        expect(el('weight').value).toBe('100');
        expect(typeof el('weight').value).toBe('string');
        expect(result.restored).toEqual(['weight', 'sets']);
    });

    it('A28: restore never writes to storage (OWNER-1.1/.2)', () => {
        seed({ weight: '100' });

        restoreWorkoutControls();

        // Byte-identical to what was seeded: a partial record stays partial.
        expect(sessionStorage.getItem(STORAGE_KEY)).toBe('{"weight":"100"}');
        expect(sessionStorage.length).toBe(1);
    });
});

describe('A29-A30 clearWorkoutControls (OWNER-1.4)', () => {
    it('A29: leaves the key ABSENT, not empty', () => {
        saveWorkoutControls();
        expect(sessionStorage.length).toBe(1);

        clearWorkoutControls();

        expect(sessionStorage.getItem(STORAGE_KEY)).toBeNull();
        expect(sessionStorage.length).toBe(0);
    });

    it('A30: is a no-op on already-empty storage and does not throw', () => {
        expect(() => clearWorkoutControls()).not.toThrow();
        expect(sessionStorage.length).toBe(0);
    });
});

describe('A31 fixture self-check', () => {
    it('A31: the fixture carries the exact declared bounds the module reads', () => {
        // Only rir and rpe cap. If a future edit strips these, this reds
        // immediately instead of A24-A26 passing for the wrong reason.
        expect(el('rir').getAttribute('max')).toBe('10');
        expect(el('rpe').getAttribute('max')).toBe('10');

        // The other four are deliberately unbounded above (OWNER-5).
        expect(el('weight').getAttribute('max')).toBeNull();
        expect(el('sets').getAttribute('max')).toBeNull();
        expect(el('min_rep').getAttribute('max')).toBeNull();
        expect(el('max_rep_range').getAttribute('max')).toBeNull();

        // Lower bounds are read by the same code path.
        expect(el('weight').getAttribute('min')).toBe('0');
        expect(el('sets').getAttribute('min')).toBe('1');
        expect(el('rir').getAttribute('min')).toBe('0');
        expect(el('rpe').getAttribute('min')).toBe('1');
        expect(el('min_rep').getAttribute('min')).toBe('1');
        expect(el('max_rep_range').getAttribute('min')).toBe('1');
    });
});

describe('A33-A35 storage failures degrade silently', () => {
    it('A33: a throwing setItem does not propagate out of saveWorkoutControls', () => {
        vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
            throw new DOMException('QuotaExceededError');
        });

        expect(() => saveWorkoutControls()).not.toThrow();
    });

    it('A34: a throwing getItem leaves the rendered values untouched and restores nothing', () => {
        setAllToNonDefaults();
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
            throw new Error('storage denied');
        });

        let result;
        expect(() => { result = restoreWorkoutControls(); }).not.toThrow();

        // readRecord() returns null on a throwing getItem, so restore early-returns
        // exactly as it does for an absent key (A17) - it does NOT apply defaults.
        expect(result.restored).toEqual([]);
        expect(currentValues()).toEqual({
            weight: '999', sets: '9', rir: '9',
            rpe: '9', min_rep: '9', max_rep_range: '9',
        });
    });

    it('A35: a throwing removeItem does not propagate out of clearWorkoutControls', () => {
        vi.spyOn(Storage.prototype, 'removeItem').mockImplementation(() => {
            throw new Error('storage denied');
        });

        expect(() => clearWorkoutControls()).not.toThrow();
    });
});

describe('A32 hydration leak detector', () => {
    // Deliberately last: proves nothing above left `hydrating` armed, which would
    // make every save assertion in this file pass for the wrong reason (§9.4).
    it('A32: hydration is disarmed after the whole suite has run', () => {
        saveWorkoutControls();
        expect(sessionStorage.getItem(STORAGE_KEY)).not.toBeNull();
    });
});
