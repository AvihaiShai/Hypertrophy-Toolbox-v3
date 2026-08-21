// @vitest-environment jsdom
//
// Packet B of Testing Strategy Phase 3 step 12
// (docs/testing_phase3/STEP12_JS_UNIT_GATE0.md §10).
//
// Covers showToast()'s legacy dispatch, the request-ID gate, default copy,
// String coercion, the inline action button, and call ordering. Case IDs
// (B1..B45, 47 cases) map to §10.3; the mutation matrix is §10.5.
//
// This module imports nothing, so there is deliberately no vi.mock here. Its
// only external dependency is the GLOBAL `bootstrap`, faked below (§10.4) --
// the first test in this repository to do so. Real Bootstrap is never
// imported: a Bootstrap upgrade is the visual and E2E tiers' problem, not
// this file's.
//
// toast.js has NO module-level mutable state (every binding in it is
// function-local, including `validTypes`), so there is deliberately no
// vi.resetModules() and no per-test re-import. §4.1 is discharged for this
// module by that fact, not by omission.
//
// TWO AUTHORING RULES APPLY TO EVERY CASE BELOW (§10.3):
//   1. No negative assertion stands alone. A bare not.toContain / not.toHaveBeen
//      passes just as happily when showToast() threw on line one and rendered
//      nothing. Every negative is paired with a positive proving the call ran.
//   2. Every legacy-signature case asserts the rendered BODY TEXT, not only the
//      class. `typeToClass[type] || 'bg-success'` means a BROKEN legacy branch
//      emits the same class a correct one does, so a class-only assertion
//      cannot tell "legacy dispatch ran" from "the fallback happened to agree".

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { showToast } from '../toast.js';

// Reduced from templates/base.html lines 236-263 (re-verified 2026-08-22).
// Kept because the module reads them: #liveToast's id (toast.js:41) and its
// EXACT at-rest class value (:88, :99), #toast-body's id (:35) and its position
// inside #liveToast (the nesting B40 depends on).
//
// Deliberately omitted, and safe to omit because toast.js never reads them:
//   data-testid="toast-container" (base.html:239)  - Playwright locators only
//   aria-live/aria-atomic on the CONTAINER (237-238) - owned by
//       e2e/ui-hardening.spec.ts:358-364 and the axe register
//   the container's inline style (241) and #liveToast's (248) - presentational;
//       jsdom does no layout, so neither could be asserted meaningfully
//
// The ABSENCE of any bg-* class here is load-bearing and is pinned by B42.
const TOAST_FIXTURE = `
<div class="position-fixed toast-container">
  <div id="liveToast" class="toast align-items-center text-white border-0"
       role="alert" aria-live="assertive" aria-atomic="true">
    <div class="d-flex">
      <div class="toast-body" id="toast-body"></div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto"
              data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  </div>
</div>`;

let calls;              // the single ordered log, shared by every fake object
let currentInstance;    // what Toast.getInstance() returns; null by default.
                        // Read at CALL time, so a test may change it between
                        // showToast() returning and the action button click.
let errorSpy;           // the handle B38/B39/B40/B41 assert on

// Every fake method pushes onto ONE shared `calls` array rather than onto
// per-object counters. Because the OLD instance's dispose() and the NEW
// instance's constructor/show() append to the same array, the relative order of
// events across two different objects is directly readable. This is the only
// technique here that could not be expressed as independent per-method spies,
// and it is why a hand-written class is used rather than vi.fn() objects alone.
class FakeToast {
    constructor(element, options) {
        calls.push('construct');
        this.element = element;
        this.options = options;
        FakeToast.constructed.push(this);
    }
    show() { calls.push('show'); }
    hide() { calls.push('hide'); }
    dispose() { calls.push('dispose'); }
}
FakeToast.getInstance = () => {
    calls.push('getInstance');
    return currentInstance;
};

// An "already present" instance is a PLAIN OBJECT, never new FakeToast(...):
// constructing one would push 'construct' onto the log during arrange, before
// the module has done anything, and corrupt B27's and B36's expected arrays.
const makeInstance = () => ({
    show() { calls.push('show'); },
    hide() { calls.push('hide'); },
    dispose() { calls.push('dispose'); },
});

const liveToast = () => document.getElementById('liveToast');
const toastBody = () => document.getElementById('toast-body');

// The message span. toast.js:61-63 creates it and appends it to #toast-body.
const messageSpan = () => toastBody().querySelector('span');
const bodyText = () => messageSpan()?.textContent;

// The action button, located through #liveToast and NEUTRAL about its direct
// parent (owner amendment, Gate 1, 2026-08-22). toast.js appends it to
// #toast-body today, but that placement is the implementation detail
// implicated in the measured wipe defect (§10.7-R10): :60 clears
// toastBody.innerHTML, so the NEXT showToast() from anywhere silently removes
// the button. These cases pin the button's TYPE, LABEL, ARIA-LABEL, GUARD and
// COERCION behavior; they must not pre-commit to the parent a fix would change.
//
// The fixture's own close button is excluded by its data-bs-dismiss attribute
// rather than by the action button's className -- :68's seven-class Bootstrap
// string is deliberately pinned by no case at any tier (§10.5), and matching on
// it here would smuggle that coupling in through the locator.
const actionButtons = () =>
    Array.from(liveToast().querySelectorAll('button:not([data-bs-dismiss="toast"])'));
const actionButton = () => actionButtons()[0] ?? null;

const bgClasses = () =>
    Array.from(liveToast().classList).filter((c) => c.startsWith('bg-')).sort();

const makeAction = (overrides = {}) => ({
    label: 'Undo',
    onClick: () => calls.push('onClick'),
    ...overrides,
});

beforeEach(() => {
    calls = [];
    currentInstance = null;
    // Static, so it MUST be reset per case or it accumulates across the file.
    FakeToast.constructed = [];
    errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    document.body.innerHTML = TOAST_FIXTURE;
    globalThis.bootstrap = { Toast: FakeToast };
});

afterEach(() => {
    delete globalThis.bootstrap;  // never leak the global into another file
    vi.restoreAllMocks();         // undoes the console.error spy
    document.body.innerHTML = '';
});

describe('showToast - modern signatures', () => {
    it('B1: success adds bg-success and renders the message', () => {
        showToast('success', 'Saved');
        expect(bgClasses()).toEqual(['bg-success']);
        expect(bodyText()).toBe('Saved');
    });

    it('B2: error adds bg-danger', () => {
        showToast('error', 'Nope');
        expect(bgClasses()).toEqual(['bg-danger']);
    });

    it('B3: warning adds bg-warning', () => {
        showToast('warning', 'Careful');
        expect(bgClasses()).toEqual(['bg-warning']);
    });

    it('B4: info adds bg-info', () => {
        showToast('info', 'FYI');
        expect(bgClasses()).toEqual(['bg-info']);
    });
});

// Rule 2: every row here asserts the rendered BODY TEXT, not only the class.
describe('showToast - legacy signature', () => {
    it('B5: a bare message dispatches to success and renders that message', () => {
        showToast('Bare message');
        expect(bodyText()).toBe('Bare message');   // NOT the word "success"
        expect(bgClasses()).toEqual(['bg-success']);
    });

    it('B6: (message, true) dispatches to error', () => {
        showToast('Broke', true);
        expect(bodyText()).toBe('Broke');
        expect(bgClasses()).toEqual(['bg-danger']);
    });

    it('B7: (message, false) dispatches to success', () => {
        // The class alone survives N1 -- typeToClass[type] || 'bg-success'
        // yields bg-success either way. Only the body text distinguishes them.
        showToast('Fine', false);
        expect(bodyText()).toBe('Fine');
        expect(bgClasses()).toEqual(['bg-success']);
    });

    it('B8: a non-boolean second argument is not an error flag', () => {
        // Also survives N1 on class alone; the body text is the kill.
        showToast('Msg', 'not-a-boolean');
        expect(bodyText()).toBe('Msg');
        expect(bgClasses()).toEqual(['bg-success']);
    });

    it('B9: an object third argument survives legacy normalisation', () => {
        showToast('Broke', true, { requestId: 'R1' });
        expect(bodyText()).toBe('Broke (Request ID: R1)');
        expect(bgClasses()).toEqual(['bg-danger']);
    });
});

describe('showToast - numeric options, both signatures', () => {
    it('B10: modern numeric third argument becomes the delay', () => {
        showToast('success', 'm', 5000);
        expect(FakeToast.constructed).toHaveLength(1);
        expect(FakeToast.constructed[0].options).toEqual({ delay: 5000 });
    });

    it('B11: legacy numeric third argument becomes the delay', () => {
        // Survives N1 on class AND on delay; only the body text is decisive.
        showToast('m', false, 5000);
        expect(FakeToast.constructed).toHaveLength(1);
        expect(FakeToast.constructed[0].options).toEqual({ delay: 5000 });
        expect(bodyText()).toBe('m');
        expect(bgClasses()).toEqual(['bg-success']);
    });
});

// This file is the SOLE exact-string guard for the two default-copy strings
// (owner ruling 3, Gate 1, 2026-08-22). A deliberate copy change MUST update
// these cases in the same PR; the red is the intended review signal, not an
// obstacle.
//
// Disclosed rather than dressed up: B15a/B15b pin a default that NO production
// call site can currently reach -- no caller passes a null message with type
// 'warning' or 'info'. That is the same "defensive but unreachable" idiom as
// the N13 equivalence, and it is recorded here so a reader does not mistake the
// coverage for reachability.
describe('showToast - default copy, one case per type', () => {
    it('B12: error + null message uses the error copy', () => {
        showToast('error', null);
        expect(bodyText()).toBe('An unexpected error occurred.');
    });

    it('B13: error + undefined message uses the error copy', () => {
        showToast('error', undefined);
        expect(bodyText()).toBe('An unexpected error occurred.');
    });

    it('B14: success + null message uses the non-error copy', () => {
        showToast('success', null);
        expect(bodyText()).toBe('Action completed successfully.');
    });

    it('B15a: warning + null message uses the non-error copy', () => {
        showToast('warning', null);
        expect(bodyText()).toBe('Action completed successfully.');
    });

    it('B15b: info + null message uses the non-error copy', () => {
        // One case per type, so a regression in one type cannot hide behind a
        // sibling's assertion inside a shared row.
        showToast('info', null);
        expect(bodyText()).toBe('Action completed successfully.');
    });
});

// B16/B17 pin a COERCION CONTRACT, not desired output.
describe('showToast - message coercion', () => {
    it('B16: a numeric message is stringified', () => {
        showToast('success', 42);
        expect(bodyText()).toBe('42');
    });

    it('B17: an object message renders as [object Object]', () => {
        // This pins what String() does TODAY, not what the product should show.
        // A future improvement that renders objects sensibly is EXPECTED to red
        // this case, and that red means "update the case", not "revert the
        // improvement".
        showToast('success', { a: 1 });
        expect(bodyText()).toBe('[object Object]');
    });

    it('B18: markup in a message is rendered as text, never as HTML', () => {
        showToast('success', '<b>x</b>');
        expect(bodyText()).toBe('<b>x</b>');
        expect(toastBody().querySelector('b')).toBeNull();
    });
});

// Every row asserts the EXACT full body text with toBe (rule 1), never
// not.toContain('Request ID') -- which would pass just as happily on a
// showToast() that died before rendering anything.
describe('showToast - request-ID gate', () => {
    it('B19: error + a request ID appends the suffix', () => {
        showToast('error', 'Nope', { requestId: 'R1' });
        expect(bodyText()).toBe('Nope (Request ID: R1)');
    });

    it('B20: success + a request ID does not', () => {
        showToast('success', 'Nope', { requestId: 'R1' });
        expect(bodyText()).toBe('Nope');
    });

    it('B21: warning + a request ID does not', () => {
        showToast('warning', 'Nope', { requestId: 'R1' });
        expect(bodyText()).toBe('Nope');
    });

    it('B22: info + a request ID does not', () => {
        showToast('info', 'Nope', { requestId: 'R1' });
        expect(bodyText()).toBe('Nope');
    });

    it('B23: error + an empty request ID does not', () => {
        // N10's predicted kill, but N10 reds four other cases too, so nothing
        // isolates this one.
        showToast('error', 'Nope', { requestId: '' });
        expect(bodyText()).toBe('Nope');
    });
});

describe('showToast - background class handling', () => {
    it('B24: a stale background class is removed', () => {
        liveToast().classList.add('bg-danger');
        showToast('success', 'm');
        expect(bgClasses()).toEqual(['bg-success']);
    });

    it('B25: all four stale classes are removed before info is added', () => {
        liveToast().classList.add('bg-success', 'bg-danger', 'bg-warning', 'bg-info');
        showToast('info', 'm');
        expect(bgClasses()).toEqual(['bg-info']);
    });

    it('B25b: all four stale classes are removed before success is added', () => {
        // This is the ONLY case in the matrix that distinguishes N31, a partial
        // classList.remove. MEASURED: B24 and B25 are both blind to it -- under
        // B25 (all four pre-set, then info) pristine and mutant both read
        // ["bg-info"]. The E2E tier cannot catch it either: ui-hardening.spec.ts
        // goes success -> error, and its not.toContain('bg-info') is vacuous
        // because bg-info was never set.
        liveToast().classList.add('bg-success', 'bg-danger', 'bg-warning', 'bg-info');
        showToast('success', 'm');
        expect(bgClasses()).toEqual(['bg-success']);
    });

    it('B26: a second toast clears the first message', () => {
        showToast('success', 'first');
        showToast('success', 'second');
        expect(toastBody().querySelectorAll('span')).toHaveLength(1);
        expect(bodyText()).toBe('second');
    });
});

// `calls` is a CUMULATIVE log for the whole test, not a per-phase one.
describe('showToast - dispose, construct, show ordering', () => {
    it('B27: an existing instance is disposed BEFORE the new one is constructed', () => {
        // The single deep-equality check pins both "dispose happened" and "it
        // happened before construction". That order IS the KI-004 mitigation,
        // so pinning it is the point: a refactor that preserves semantics but
        // reorders getInstance would red this case, and that red means "confirm
        // intent", not "flaky test".
        currentInstance = makeInstance();
        showToast('success', 'm');
        expect(calls).toEqual(['getInstance', 'dispose', 'construct', 'show']);
    });

    it('B28: with no existing instance there is no dispose', () => {
        showToast('success', 'm');
        expect(calls).toEqual(['getInstance', 'construct', 'show']);
    });

    it('B29: the constructor receives the element and the default delay', () => {
        showToast('success', 'm');
        expect(FakeToast.constructed).toHaveLength(1);
        expect(FakeToast.constructed[0].element).toBe(liveToast());
        expect(FakeToast.constructed[0].options).toEqual({ delay: 3000 });
        expect(calls.filter((c) => c === 'show')).toHaveLength(1);
    });
});

// PLACEMENT-NEUTRAL BY OWNER AMENDMENT (Gate 1, 2026-08-22).
//
// These cases require the action button to exist WITHIN #liveToast and enforce
// its type, label, aria-label, guard and coercion behavior. They deliberately
// do NOT pin its direct parent. toast.js:84 appends it to #toast-body today,
// and that is exactly the implementation detail implicated in the measured wipe
// defect (§10.7-R10): :60 clears toastBody.innerHTML, so any subsequent toast
// from anywhere destroys the button. Reachable inside its own only caller --
// volume-splitter.js raises the action toast with duration 6000, then
// immediately calls loadVolumeHistory(), whose .catch emits showToast('error',
// ...); on a slow or failing history fetch the user's "Activate for Plan tab"
// button vanishes mid-toast.
//
// That defect is PINNED, NOT FIXED, and is NOT mitigated by this file --
// Packet B characterizes current behavior and adds no production change. A fix
// that relocates the button so it survives a body clear must leave every case
// below GREEN, which is the whole reason the parent is not asserted.
describe('showToast - action button construction', () => {
    it('B30: a valid action appends a button inside #liveToast', () => {
        showToast('success', 'm', { action: makeAction({ label: 'Activate' }) });
        expect(actionButtons()).toHaveLength(1);
        expect(actionButton().type).toBe('button');
        expect(actionButton().textContent).toBe('Activate');
    });

    it('B31: action.ariaLabel becomes the accessible name', () => {
        // An a11y assertion, deliberately in scope. What is OUT of scope is
        // live-region and role semantics -- role="alert", aria-live,
        // aria-atomic -- which toast.js never touches and which
        // ui-hardening.spec.ts, accessibility.spec.ts and the axe register own.
        showToast('success', 'm', {
            action: makeAction({ label: 'Activate', ariaLabel: 'Activate this plan' }),
        });
        expect(actionButton().getAttribute('aria-label')).toBe('Activate this plan');
    });

    it('B32: with no ariaLabel the attribute is absent, not "undefined"', () => {
        showToast('success', 'm', { action: makeAction({ label: 'Activate' }) });
        // Non-null FIRST, so the negative below cannot pass on a missing button.
        expect(actionButton()).not.toBeNull();
        expect(actionButton().hasAttribute('aria-label')).toBe(false);
    });

    it('B33: a non-function onClick appends no button', () => {
        showToast('success', 'm', { action: { label: 'Activate', onClick: 'nope' } });
        expect(actionButtons()).toHaveLength(0);
        // Paired positives: the call ran to completion and nothing errored.
        expect(bodyText()).toBe('m');
        expect(errorSpy).not.toHaveBeenCalled();
    });

    it('B34: a falsy label appends no button', () => {
        showToast('success', 'm', { action: makeAction({ label: '' }) });
        expect(actionButtons()).toHaveLength(0);
        expect(bodyText()).toBe('m');
        expect(errorSpy).not.toHaveBeenCalled();
    });

    it('B35: a numeric label is stringified', () => {
        // Like B16/B17, this pins String coercion, not desired output.
        showToast('success', 'm', { action: makeAction({ label: 5 }) });
        expect(actionButton().textContent).toBe('5');
    });
});

describe('showToast - action button click behavior', () => {
    it('B36: the click hides the live instance BEFORE running onClick', () => {
        showToast('success', 'm', { action: makeAction() });
        // Arranged AFTER showToast() returns, for fidelity rather than
        // bookkeeping: setting it before means the module DISPOSES that
        // instance at :105, and a disposed instance is not what production's
        // getInstance returns when the user clicks moments later. This models
        // the real sequence -- showToast() constructs a live instance, and the
        // click finds that one. The fake honours it because getInstance reads
        // the variable at call time.
        currentInstance = makeInstance();
        calls.length = 0;   // isolate the click from showToast()'s own entries
        actionButton().click();
        // 'getInstance' is the click's OWN first entry: the handler at
        // toast.js:74 calls bootstrap.Toast.getInstance(toastElement) itself, so
        // ['hide','onClick'] is not achievable. `hide` BEFORE `onClick` is the
        // assertion this case exists for.
        expect(calls).toEqual(['getInstance', 'hide', 'onClick']);
    });

    it('B37: with no live instance the click still runs onClick and hides nothing', () => {
        showToast('success', 'm', { action: makeAction() });
        // currentInstance left null for the whole case. Together with B36 this
        // proves the click branch is driven by what getInstance returns AT
        // CLICK TIME, not by what showToast() saw.
        calls.length = 0;
        actionButton().click();
        expect(calls).toEqual(['getInstance', 'onClick']);
    });

    it('B38: a throwing onClick is caught and logged', () => {
        const boom = new Error('boom');
        showToast('success', 'm', {
            action: makeAction({ onClick: () => { throw boom; } }),
        });
        errorSpy.mockClear();
        // NOT wrapped in expect(...).not.toThrow(): an exception thrown inside a
        // DOM event listener does not propagate out of .click() in jsdom, so
        // such a wrapper passes with OR without the try/catch at toast.js:78-82
        // and would be a false green. The errorSpy assertion below is the only
        // thing that kills N23 -- MEASURED against the N23 shape, the spy's call
        // count is 0.
        actionButton().click();
        expect(errorSpy).toHaveBeenCalledWith('Toast action handler failed:', expect.any(Error));
    });
});

// Produced by removing an `id` ATTRIBUTE, never a node. #toast-body is nested
// inside #liveToast (base.html 243/251/262), so deleting the #liveToast element
// would take the body with it and drive B40 down B39's path, passing for the
// wrong reason.
describe('showToast - missing-DOM early returns', () => {
    it('B39: an unresolvable #toast-body logs and returns', () => {
        toastBody().removeAttribute('id');
        // The leading guard IS load-bearing here, unlike in B38: N25 kills this
        // case by TypeError, not by the console assertion. With the return at
        // :38 deleted, :60 dereferences a null toastBody and throws, which
        // would make the assertions below unreachable rather than failing
        // informatively.
        expect(() => showToast('success', 'm')).not.toThrow();
        expect(errorSpy).toHaveBeenCalledWith('Error: toast-body not found in the DOM!');
        expect(calls).toEqual([]);                   // Bootstrap never touched
        expect(FakeToast.constructed).toHaveLength(0);
    });

    it('B40: an unresolvable #liveToast logs and returns', () => {
        liveToast().removeAttribute('id');
        // Same leading guard: N26 throws at :88 on a null toastElement.
        expect(() => showToast('success', 'm')).not.toThrow();
        expect(errorSpy).toHaveBeenCalledWith('Error: liveToast not found in the DOM!');
        expect(calls).toEqual([]);
        expect(FakeToast.constructed).toHaveLength(0);
    });

    it('B41: with both unresolvable only the toast-body error fires', () => {
        const body = toastBody();
        const live = liveToast();
        live.removeAttribute('id');
        body.removeAttribute('id');
        showToast('success', 'm');
        // Deep-equalled as a single-entry array, not asserted as "the toast-body
        // message appears somewhere" -- this proves lookup order (:35 before
        // :41), which a toHaveBeenCalledWith would not.
        expect(errorSpy.mock.calls).toEqual([['Error: toast-body not found in the DOM!']]);
    });
});

describe('showToast - anti-vacuity and API sharp edges', () => {
    it('B42: the fixture carries no bg-* class at rest', () => {
        // Without this, a future fixture edit that added one would make B1-B4
        // pass with the module never adding a class.
        expect(liveToast()).not.toBeNull();
        expect(toastBody()).not.toBeNull();
        expect(bgClasses()).toEqual([]);
    });

    it('B43: a single-argument call renders the default copy, not the type word', () => {
        // `message` has no default parameter, so an omitted second argument IS
        // undefined; this is behaviourally identical to showToast('success',
        // undefined). B14 does not cover it -- B14 passes an explicit null.
        // Pinned because it is the edge a reader gets wrong, not because it
        // reaches a distinct branch.
        showToast('success');
        expect(bodyText()).toBe('Action completed successfully.');
    });

    it('B44: a falsy-but-defined message is rendered, not replaced', () => {
        // MEASURED: the `message !== undefined && message !== null` guard at
        // :49 is perturbed by no other case. Mutating it to `if (message)`
        // leaves B1, B12, B14, B16 and B17 all indistinguishable; only an empty
        // (or zero) message tells the two apart. Without this case the module
        // could silently regress to replacing a deliberate empty message with
        // boilerplate copy.
        showToast('success', '');
        expect(bodyText()).toBe('');
    });

    it('B45: a legacy call whose message IS a type word swallows the message', () => {
        // PINNED SHARP EDGE, NOT DESIRED BEHAVIOR -- and NOT mitigated here.
        // 'error' passes validTypes.has() at :15, so the legacy branch never
        // runs, `message` becomes the boolean true, and the caller's actual
        // message is swallowed. Eight live call sites have the collision-capable
        // showToast(error.message || '<fallback>', true) shape, so this is one
        // server-copy change away from firing; it is not reachable today only
        // because utils/errors.py never sets a message to one of the four type
        // words. Fixing it is production code and out of scope for a test-only
        // packet.
        showToast('error', true);
        expect(bodyText()).toBe('true');
        expect(bgClasses()).toEqual(['bg-danger']);
    });
});
