// @vitest-environment jsdom
//
// Packet C of Testing Strategy Phase 3 step 12
// (docs/testing_phase3/STEP12_JS_UNIT_GATE0.md §11).
//
// Covers exercises.js: the missing-ID early return, the module-level
// double-delete guard and its finally release, both api.post argument triples,
// both showToast legacy arities, both notifyVolumeAffectingPlanChange reason
// strings, both error paths, and the three clearWorkoutPlan() modal branches.
// Case IDs (C1..C29, 29 cases) map to §11.3; the mutation matrix is §11.8.
//
// FOUR COLLABORATORS ARE MOCKED and one global is faked (§11.6). None of the
// four factories may use importActual: a partial mock would execute real
// collaborator code, break §11.9's coverage arithmetic, and move toast.js's
// post-Packet-B numbers for reasons unrelated to this file (§11.11-R10).
//
// TWO AUTHORING RULES APPLY TO EVERY CASE BELOW (§11.3):
//   1. No negative assertion stands alone. A bare not.toHaveBeenCalled passes
//      just as happily when the function died on line one. Every negative is
//      paired with a positive proving the call ran to completion; four of them
//      (C9, C17, C18, C25) are expressed as a deep equality on the ordered log,
//      which is the positive and the negative in one assertion.
//   2. api.post rejects with a PLAIN OBJECT, never an Error. fetch-wrapper.js's
//      normalizeError() (:51-91) returns { code, message, requestId } and that
//      object is what is thrown (:216, :249). A `new Error('Boom')` fixture
//      would test a shape production never produces.
//
// COPY OWNERSHIP (§11.11-R15, owner ruling at Gate 1). The literals at
// exercises.js:11, 12, 31, 36, 59, 68 occur nowhere else in the repository as
// EXACT literals -- the server's copy at routes/workout_plan.py:299, :305, :320
// and :323 is the same user-visible phrasing, differing by a trailing "!" or by
// the interpolation -- and, decisively, NO E2E SPEC ASSERTS ANY OF THEM. So
// C1/C2/C5/C8/C22/C24 are their only guard at any tier. A deliberate copy change updates these cases in the SAME PR --
// the resulting red is the intended review signal, not a reason to loosen the
// assertions.
//
// ORDERED-LOG STRICTNESS (§11.11-R8). One relation here is a contract:
// api.post -> resetControls, i.e. the reset runs only after the server clear
// resolves and never on the error path (KI-005 criterion 4,
// ki005_controls_persistence/PLANNING.md:448), pinned by C19's ordering and
// decisively by C25. EVERY OTHER RELATION IS CHARACTERIZATION of current call
// order: fetchWorkoutPlan() touches no workout control (workout-plan.js:90-117)
// and the sole workout-plan:volume-affecting-change listener is 150 ms-debounced
// (plan_volume_panel.js:244-247), so no ordering among fetchWorkoutPlan,
// notifyVolume and resetControls is observable in production. A red on one of
// those means "confirm intent", never "a user-visible defect".

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

// The five mock handles are created ONCE, above every vi.mock factory, and the
// factories RETURN them. vi.hoisted() is REQUIRED (measured, §11.15-M-b):
// vi.mock factories are hoisted above every plain top-level binding, so a
// factory referencing a plain `const` throws
//   ReferenceError: Cannot access '<name>' before initialization
// at COLLECTION and the file reports "(0 test)". It is NOT required to preserve
// identity across vi.resetModules() -- measurement (§11.15-M-a) shows the mock
// registry survives resetModules() and the factory is not re-run.
const h = vi.hoisted(() => ({
    showToast: vi.fn(),
    fetchWorkoutPlan: vi.fn(),
    resetWorkoutControlsToDefaults: vi.fn(),
    notifyVolumeAffectingPlanChange: vi.fn(),
    post: vi.fn(),
}));

vi.mock('../toast.js', () => ({ showToast: h.showToast }));
vi.mock('../workout-plan.js', () => ({
    fetchWorkoutPlan: h.fetchWorkoutPlan,
    resetWorkoutControlsToDefaults: h.resetWorkoutControlsToDefaults,
}));
vi.mock('../workout-plan-events.js', () => ({
    notifyVolumeAffectingPlanChange: h.notifyVolumeAffectingPlanChange,
}));
vi.mock('../fetch-wrapper.js', () => ({ api: { post: h.post } }));

// Reduced from templates/workout_plan.html:564 (#clearPlanModal opens there;
// #clearPlanModalLabel :568, #confirmClearPlanBtn :579). Re-read on b52df68,
// 2026-08-22. The opening tag is transcribed verbatim; only the id is
// load-bearing, because exercises.js:45 does getElementById('clearPlanModal')
// and reads nothing else off the node.
//
// Deliberately omitted, and safe to omit because exercises.js never reads them:
//   #clear-plan-btn (workout_plan.html:277) - the data-bs-toggle trigger; the
//       button -> modal -> confirm journey is e2e/ui-hardening.spec.ts:996-1034's
//   #confirmClearPlanBtn (:579) - the onclick entry point; these cases call the
//       exported function directly, so the wiring is E2E's to own
//   #clearPlanModalLabel (:568) and the body/footer chrome - presentational,
//       and jsdom does no layout
//   the delete button that calls removeExercise - generated by
//       workout-plan-table.js:419, in no template at all, and C16 pins that
//       removeExercise reads no DOM whatsoever
// aria-labelledby is kept verbatim and points at the omitted label element;
// neither this file nor exercises.js reads it, and no a11y check runs here.
const MODAL_FIXTURE = `
<div class="modal fade" id="clearPlanModal" tabindex="-1" aria-labelledby="clearPlanModalLabel" aria-hidden="true"></div>`;

// The exact shape api.post rejects with (§11.3 rule 2). Frozen so a case cannot
// mutate the object the identity assertions in C8 and C24 compare against.
const REMOVE_REJECTION = Object.freeze({ code: 'REMOVE_FAILED', message: 'Boom', requestId: 'R1' });
const CLEAR_REJECTION = Object.freeze({ code: 'CLEAR_FAILED', message: 'Boom', requestId: 'R1' });

const POST_OPTIONS = {
    headers: { 'Content-Type': 'application/json' },
    showLoading: false,
    showErrorToast: false,
    useDefaultHeaders: false,
};

let removeExercise, clearWorkoutPlan;

let calls;                 // the single ordered log, appended to by all five
                           // mocks and by the Modal fake
let currentModalInstance;  // what Modal.getInstance() returns; null by default.
                           // Read at CALL time, so a case controls what :47 sees
let getInstanceArgs;       // every element handed to Modal.getInstance
let errorSpy;              // console.error - C1/C2/C8/C24 assert on it
let logSpy;                // console.log  - C10's duplicate-guard oracle

// An "already present" instance is a PLAIN OBJECT. There is no constructor in
// this fake at all, because exercises.js never constructs a Modal -- so the
// arrange-time log corruption Packet B's makeInstance() existed to avoid cannot
// arise here. Recorded because the reason it cannot arise is a measurement
// about this module, not a general truth.
const modalInstance = () => ({ hide() { calls.push('Modal.hide'); } });

// api.post is the only mock whose return value the module reads, so it is
// re-pointed per case rather than given one default implementation. Both
// helpers log 'api.post' at CALL time, before resolving or throwing, so the
// ordered log records the request rather than its outcome.
const resolvePost = (value) =>
    h.post.mockImplementation(async () => { calls.push('api.post'); return value; });
const rejectPost = (rejection) =>
    h.post.mockImplementation(async () => { calls.push('api.post'); throw rejection; });
const rejectPostOnce = (rejection) =>
    h.post.mockImplementationOnce(async () => { calls.push('api.post'); throw rejection; });

beforeEach(async () => {
    calls = [];
    currentModalInstance = null;
    getInstanceArgs = [];

    h.showToast.mockReset().mockImplementation(() => { calls.push('showToast'); });
    h.fetchWorkoutPlan.mockReset().mockImplementation(() => { calls.push('fetchWorkoutPlan'); });
    h.notifyVolumeAffectingPlanChange.mockReset().mockImplementation(() => { calls.push('notifyVolume'); });
    h.resetWorkoutControlsToDefaults.mockReset().mockImplementation(() => { calls.push('resetControls'); });
    h.post.mockReset();
    resolvePost({ message: 'OK' });

    globalThis.bootstrap = {
        Modal: {
            getInstance: (el) => {
                calls.push('Modal.getInstance');
                getInstanceArgs.push(el);
                return currentModalInstance;
            },
        },
    };

    errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

    // jsdom shares web storage across the cases in a file. Neither export uses
    // it, but workout-plan.js -- mocked here -- is a storage user in production,
    // so the clear stays as a standing §4.2 rule rather than an assumption.
    sessionStorage.clear();
    localStorage.clear();

    document.body.innerHTML = MODAL_FIXTURE;

    // exercises.js's only module-level state, `const deletingExercises = new
    // Set()` at :7, has NO exported reset (§11.5's recorded finding), so a clean
    // instance is only reachable by re-import. Measured sound at §11.15-M-c.
    vi.resetModules();
    ({ removeExercise, clearWorkoutPlan } = await import('../exercises.js'));
});

afterEach(() => {
    delete globalThis.bootstrap;  // never leak the global into another file
    vi.restoreAllMocks();         // undoes the console spies and C16's getElementById spy
    document.body.innerHTML = '';
});

describe('removeExercise - missing-ID early return', () => {
    it('C1: undefined is refused before any work', async () => {
        await removeExercise(undefined);

        expect(errorSpy).toHaveBeenCalledWith('Error: exercise ID is required to remove an exercise.');
        // toHaveBeenCalledWith is arity-exact, so this pins the two-argument
        // legacy shape as well as the copy.
        expect(h.showToast).toHaveBeenCalledWith('Exercise ID is missing. Unable to remove exercise.', true);
        expect(h.post).not.toHaveBeenCalled();
        expect(calls).toEqual(['showToast']);
    });

    it('C2: 0 - the plausible-but-invalid falsy value - is refused too', async () => {
        // 0 is the falsy value that actually reaches this guard: ids arrive as
        // numbers (workout-plan-table.js:419 interpolates a bare ${exercise.id}).
        // Isolated by P42 (!exerciseId -> exerciseId == null), the exact "fix" a
        // developer writes when told the guard is too broad, under which 0 passes
        // while undefined still does not.
        await removeExercise(0);

        expect(errorSpy).toHaveBeenCalledWith('Error: exercise ID is required to remove an exercise.');
        expect(h.showToast).toHaveBeenCalledWith('Exercise ID is missing. Unable to remove exercise.', true);
        expect(h.post).not.toHaveBeenCalled();
        expect(calls).toEqual(['showToast']);
    });
});

describe('removeExercise - success path', () => {
    it('C3: posts the exact argument triple', async () => {
        resolvePost({ message: 'Removed' });

        await removeExercise(7);

        expect(h.post).toHaveBeenCalledTimes(1);
        // The deep equality on POST_OPTIONS is what pins showErrorToast: false --
        // which is why the module toasts for itself at :31/:36. Flipping it would
        // double-toast in production, and P10 reds this row through this line.
        expect(h.post).toHaveBeenCalledWith('/remove_exercise', { id: 7 }, POST_OPTIONS);
    });

    it('C4: result.message is passed through verbatim, one argument', async () => {
        resolvePost({ message: 'Removed' });

        await removeExercise(7);

        expect(h.showToast).toHaveBeenCalledTimes(1);
        expect(h.showToast).toHaveBeenCalledWith('Removed');
    });

    it('C5: a result with no message falls back to the default copy', async () => {
        // DISCLOSED (§11.11-R17): this fallback is UNREACHABLE through the real
        // route. routes/workout_plan.py:299 always returns
        // message="Exercise removed successfully" and utils/errors.py:36-37
        // forwards it whenever truthy, so result.message is always present --
        // and the fallback differs from the server's copy by a trailing "!".
        // Pinned because the branch exists, not because a user can see it.
        resolvePost({});

        await removeExercise(7);

        expect(h.showToast).toHaveBeenCalledTimes(1);
        expect(h.showToast).toHaveBeenCalledWith('Exercise removed successfully!');
    });

    it('C6: notifies with exactly the reason "remove-exercise"', async () => {
        resolvePost({ message: 'Removed' });

        await removeExercise(7);

        expect(h.notifyVolumeAffectingPlanChange).toHaveBeenCalledTimes(1);
        expect(h.notifyVolumeAffectingPlanChange).toHaveBeenCalledWith('remove-exercise');
    });

    it('C7: success call order', async () => {
        // CHARACTERIZATION of current call order (see the file header): nothing
        // requires fetchWorkoutPlan before notifyVolume.
        resolvePost({ message: 'Removed' });

        await removeExercise(7);

        expect(calls).toEqual(['api.post', 'showToast', 'fetchWorkoutPlan', 'notifyVolume']);
    });
});

describe('removeExercise - error path', () => {
    it('C8: records the rejection and interpolates its message into the toast', async () => {
        rejectPost(REMOVE_REJECTION);

        await removeExercise(7);

        expect(errorSpy).toHaveBeenCalledWith('Error removing exercise:', REMOVE_REJECTION);
        expect(errorSpy.mock.calls[0][1]).toBe(REMOVE_REJECTION);   // by identity, not shape
        expect(h.showToast).toHaveBeenCalledWith('Unable to remove exercise: Boom', true);
    });

    it('C9: nothing downstream runs on failure', async () => {
        rejectPost(REMOVE_REJECTION);

        await removeExercise(7);

        // One deep equality carrying the positive (the toast ran) and both
        // negatives (no refresh, no notify) - rule 1 without a bare not.
        expect(calls).toEqual(['api.post', 'showToast']);
    });
});

describe('removeExercise - the concurrent-delete guard', () => {
    it('C10: a concurrent second call for the same id is refused', async () => {
        resolvePost({ message: 'Removed' });

        // Deterministic without timers: the synchronous prologue :10-22 runs to
        // the first await at :25, so the second call's guard check at :17 happens
        // before any microtask can resume p1.
        const p1 = removeExercise(1);
        await removeExercise(1);
        await p1;

        expect(h.post).toHaveBeenCalledTimes(1);
        expect(logSpy).toHaveBeenCalledWith('Delete already in progress for exercise:', 1);
        expect(calls).toEqual(['api.post', 'showToast', 'fetchWorkoutPlan', 'notifyVolume']);
    });

    it('C11: a concurrent call for a different id is not blocked', async () => {
        resolvePost({ message: 'Removed' });

        const p1 = removeExercise(1);
        await removeExercise(2);
        await p1;

        // Co-killed by P41 (.has(exerciseId) -> .size > 0, the realistic
        // broken-guard shape, under which this reads 1) and by P11 (the body
        // shape, which the next two lines pin). NO mutation reds C11 alone --
        // §11.8's disclosure table, corrected against measurement at §11.17.
        expect(h.post).toHaveBeenCalledTimes(2);
        expect(h.post.mock.calls[0][1]).toEqual({ id: 1 });
        expect(h.post.mock.calls[1][1]).toEqual({ id: 2 });
        expect(logSpy).not.toHaveBeenCalled();
    });

    it('C12: the guard is released on success', async () => {
        resolvePost({ message: 'Removed' });

        await removeExercise(1);
        await removeExercise(1);

        // The honest oracle is a second successful call, not inspection of the
        // unexported Set. No mutation isolates C12 from C13 (§11.8's disclosure
        // table): P7 reds both and P8 reds only C13.
        expect(h.post).toHaveBeenCalledTimes(2);
    });

    it('C13: the guard is released on failure', async () => {
        rejectPostOnce(REMOVE_REJECTION);
        resolvePost({ message: 'Removed' });

        await removeExercise(1);
        await removeExercise(1);

        expect(h.post).toHaveBeenCalledTimes(2);
        // The first call took :36 (error shape), the second reached :31 (success
        // shape) - which it could only do if the finally at :38 released the id.
        expect(h.showToast.mock.calls[0]).toEqual(['Unable to remove exercise: Boom', true]);
        expect(h.showToast.mock.calls[1]).toEqual(['Removed']);
    });

    it('C14: CHARACTERIZATION - Set keys are type-sensitive, so 1 and "1" both proceed', async () => {
        // A recorded property of the guard, NOT a bug report and NOT desired
        // behavior. No in-app call site passes a string -- workout-plan-table.js:419
        // interpolates a bare ${exercise.id} -- but removeExercise is also a window
        // global (app.js:36), so "unreachable" would overstate it. Co-killed with
        // C11 by P41; no mutation reds C14 alone (§11.8's disclosure table, which
        // said "killed by no mutation of exercises.js" until §11.17 measured P41).
        // A mutation making the key type-insensitive would isolate it, and is not
        // written, because it would pin the coercion FIX as a defect.
        resolvePost({ message: 'Removed' });

        const p1 = removeExercise(1);
        await removeExercise('1');
        await p1;

        expect(h.post).toHaveBeenCalledTimes(2);
    });
});

describe('removeExercise - isolation and DOM independence', () => {
    it('C15: ANTI-VACUITY - a fresh module instance gets a fresh guard', async () => {
        // Self-contained, with no cross-case ordering dependency (§4.4). If
        // resetModules() did not produce a fresh Set, C10-C14 would pass by
        // accident; this case is what makes that falsifiable. P6 (delete the
        // .add at :22) kills it by making the trapped-id arrangement impossible.
        let releaseFirst;
        const deferred = new Promise((resolve) => { releaseFirst = resolve; });
        h.post.mockReset();
        h.post.mockImplementationOnce(async () => { calls.push('api.post'); return deferred; });
        resolvePost({ message: 'Removed' });

        const p1 = removeExercise(1);   // leaves 1 trapped in this instance's guard
        await removeExercise(1);        // blocked
        expect(h.post).toHaveBeenCalledTimes(1);

        vi.resetModules();
        const fresh = await import('../exercises.js');
        await fresh.removeExercise(1);  // accepted: a different Set

        expect(h.post).toHaveBeenCalledTimes(2);

        releaseFirst({ message: 'Removed' });
        await p1;                       // leave no promise dangling
    });

    it('C16: removeExercise reads no DOM at all', async () => {
        const getElementById = vi.spyOn(document, 'getElementById');
        document.body.innerHTML = '';
        resolvePost({ message: 'Removed' });

        await removeExercise(7);

        expect(calls).toEqual(['api.post', 'showToast', 'fetchWorkoutPlan', 'notifyVolume']);
        expect(getElementById).not.toHaveBeenCalled();
    });
});

describe('clearWorkoutPlan - the three modal branches', () => {
    it('C17: the modal element is absent', async () => {
        document.getElementById('clearPlanModal').remove();
        resolvePost({ message: 'Cleared' });

        await clearWorkoutPlan();

        // Positive first: the whole flow completed. Only then the negative.
        expect(calls).toEqual(['api.post', 'showToast', 'fetchWorkoutPlan', 'notifyVolume', 'resetControls']);
        expect(getInstanceArgs).toEqual([]);
    });

    it('C18: the modal is present but has no Bootstrap instance', async () => {
        currentModalInstance = null;
        resolvePost({ message: 'Cleared' });

        await clearWorkoutPlan();

        // By identity, not merely "was called": this pins that :47 is handed the
        // #clearPlanModal node itself. (P21, if (modal) -> if (true), is C17's
        // killer, not this case's -- C18's fixture HAS the modal, so the two
        // conditions are indistinguishable here. §11.8-P21, measured at §11.17.)
        expect(getInstanceArgs).toHaveLength(1);
        expect(getInstanceArgs[0]).toBe(document.getElementById('clearPlanModal'));
        expect(calls).toEqual([
            'Modal.getInstance',
            'api.post', 'showToast', 'fetchWorkoutPlan', 'notifyVolume', 'resetControls',
        ]);
    });

    it('C19: the modal is present with an instance, and the full call order holds', async () => {
        // TWO CLAIMS OF DIFFERENT STRENGTH.
        // (a) CONTRACT: resetControls runs AFTER api.post resolves -- what KI-005
        //     criterion 4 actually states
        //     (ki005_controls_persistence/PLANNING.md:448).
        // (b) CHARACTERIZATION: everything else in this sequence, including
        //     hide() before api.post and fetchWorkoutPlan before notifyVolume
        //     before resetControls. None of (b) is observable in production.
        currentModalInstance = modalInstance();
        resolvePost({ message: 'Cleared' });

        await clearWorkoutPlan();

        expect(calls).toEqual([
            'Modal.getInstance', 'Modal.hide',
            'api.post', 'showToast', 'fetchWorkoutPlan', 'notifyVolume', 'resetControls',
        ]);
        expect(calls.indexOf('api.post')).toBeLessThan(calls.indexOf('resetControls'));
    });
});

describe('clearWorkoutPlan - success path', () => {
    it('C20: posts the exact argument triple, with a null body', async () => {
        resolvePost({ message: 'Cleared' });

        await clearWorkoutPlan();

        expect(h.post).toHaveBeenCalledTimes(1);
        // The second argument is null - not undefined, not {}. toHaveBeenCalledWith
        // distinguishes all three, which is what P27 (null -> {}) proves.
        expect(h.post).toHaveBeenCalledWith('/clear_workout_plan', null, POST_OPTIONS);
    });

    it('C21: result.message is passed through verbatim, one argument', async () => {
        resolvePost({ message: 'Cleared' });

        await clearWorkoutPlan();

        expect(h.showToast).toHaveBeenCalledTimes(1);
        expect(h.showToast).toHaveBeenCalledWith('Cleared');
    });

    it('C22: a result with no message falls back to the default copy', async () => {
        // DISCLOSED (§11.11-R17), same class as C5: routes/workout_plan.py:320
        // always returns message="Workout plan cleared successfully", so this
        // fallback is unreachable through the real route and differs from the
        // server's copy by a trailing "!".
        resolvePost({});

        await clearWorkoutPlan();

        expect(h.showToast).toHaveBeenCalledTimes(1);
        expect(h.showToast).toHaveBeenCalledWith('Workout plan cleared successfully!');
    });

    it('C23: notifies with exactly the reason "clear-workout-plan"', async () => {
        resolvePost({ message: 'Cleared' });

        await clearWorkoutPlan();

        expect(h.notifyVolumeAffectingPlanChange).toHaveBeenCalledTimes(1);
        expect(h.notifyVolumeAffectingPlanChange).toHaveBeenCalledWith('clear-workout-plan');
    });
});

describe('clearWorkoutPlan - error path', () => {
    it('C24: records the rejection and interpolates its message into the toast', async () => {
        rejectPost(CLEAR_REJECTION);

        await clearWorkoutPlan();

        expect(errorSpy).toHaveBeenCalledWith('Error clearing workout plan:', CLEAR_REJECTION);
        expect(errorSpy.mock.calls[0][1]).toBe(CLEAR_REJECTION);
        expect(h.showToast).toHaveBeenCalledWith('Unable to clear workout plan: Boom', true);
    });

    it('C25: the controls reset never runs on the error path', async () => {
        // THE CONTRACT CASE. KI-005 criterion 4 says the reset runs after the
        // SUCCESSFUL server clear; this pins that it does not run when the clear
        // fails. One deep equality carries the positive (the modal closed, the
        // error toast fired) and all three negatives.
        currentModalInstance = modalInstance();
        rejectPost(CLEAR_REJECTION);

        await clearWorkoutPlan();

        expect(calls).toEqual(['Modal.getInstance', 'Modal.hide', 'api.post', 'showToast']);
    });
});

describe('characterization tie-ins', () => {
    it('C26: a server message equal to a toast type word is passed through unmodified', async () => {
        // KI-010 PASS-THROUGH ONLY. exercises.js:31 and :59 are 2 of the 5
        // one-argument collision sites named at
        // docs/UI_SCENARIOS_GAP_ANALYSIS.md:105. THIS PINS PASS-THROUGH AND
        // NOTHING ELSE: toast.js is mocked here, so this file cannot observe the
        // collision's rendering, and this case neither pins nor mitigates KI-010
        // -- which stays Open in a document Packet C may not edit.
        resolvePost({ message: 'error' });

        await clearWorkoutPlan();

        expect(h.showToast).toHaveBeenCalledTimes(1);
        expect(h.showToast).toHaveBeenCalledWith('error');
    });

    it('C27: fetchWorkoutPlan() is not awaited', async () => {
        // A real regression guard: adding an await at :60 would strand notify and
        // reset behind a slow refresh. P37 reds this BY TIMEOUT, not by
        // assertion. The 1000 ms bound is pinned rather than "short": the
        // pristine path resolves in ~1 ms so it cannot flake, while bounding
        // P37's cost to one second instead of Vitest's default five (§11.11-R11).
        h.fetchWorkoutPlan.mockImplementation(() => {
            calls.push('fetchWorkoutPlan');
            return new Promise(() => {});   // never settles
        });
        resolvePost({ message: 'Cleared' });

        await clearWorkoutPlan();

        expect(calls).toContain('notifyVolume');
        expect(calls).toContain('resetControls');
    }, 1000);
});

describe('anti-vacuity', () => {
    it('C28: the handles this file asserts on are the handles the module receives', async () => {
        // A test whose spies are not the module's spies asserts nothing, however
        // that came about. Killed by P39.
        const toast = await import('../toast.js');
        const workoutPlan = await import('../workout-plan.js');
        const workoutPlanEvents = await import('../workout-plan-events.js');
        const fetchWrapper = await import('../fetch-wrapper.js');

        expect(toast.showToast).toBe(h.showToast);
        expect(workoutPlan.fetchWorkoutPlan).toBe(h.fetchWorkoutPlan);
        expect(workoutPlan.resetWorkoutControlsToDefaults).toBe(h.resetWorkoutControlsToDefaults);
        expect(workoutPlanEvents.notifyVolumeAffectingPlanChange).toBe(h.notifyVolumeAffectingPlanChange);
        expect(fetchWrapper.api.post).toBe(h.post);

        for (const handle of Object.values(h)) {
            expect(vi.isMockFunction(handle)).toBe(true);
            expect(handle).toHaveBeenCalledTimes(0);
        }
    });

    it('C29: the fixture and the bootstrap global are actually installed', async () => {
        // Without this, C17's "modal absent" arrangement would be
        // indistinguishable from a fixture that never had the node, and C18/C19
        // would pass against a bootstrap global that was never installed.
        // Killed by P38.
        expect(document.getElementById('clearPlanModal')).not.toBeNull();
        expect(typeof globalThis.bootstrap.Modal.getInstance).toBe('function');
    });
});
