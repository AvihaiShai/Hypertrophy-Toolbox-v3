/**
 * Toast notification functionality with standardized types.
 *
 * TWO DEFECTS WERE FIXED IN THIS MODULE, and both contracts below are live.
 * KI-011 (PR #426) changed how a toast RENDERS; KI-010 (this change) changed how
 * its ARGUMENTS are read. They touch different halves of the same function.
 *
 * ---- KI-010: which signature you get ----------------------------------------
 *
 * TWO SIGNATURES ARE SUPPORTED, and which one you get is decided by argument 2,
 * not by argument 1. Read this table before adding a call site.
 *
 *   showToast(type, message, options?)      MODERN
 *   showToast(message, isError?, duration?) LEGACY
 *
 * | argument 2         | how argument 1 is read | why                              |
 * |--------------------|------------------------|----------------------------------|
 * | a boolean          | as the MESSAGE         | legacy `isError` flag            |
 * | not supplied       | as the MESSAGE         | legacy bare message              |
 * | `null`             | as the TYPE            | modern, "no message" default copy|
 * | anything else      | as the TYPE            | modern                           |
 *
 * An explicitly supplied `undefined` counts as SUPPLIED, so
 * `showToast('error', undefined)` is a MODERN call. See the `isLegacyCall`
 * predicate's comment before refactoring this function's signature.
 *
 * ---- KI-011: an action outlives the message that raised it -------------------
 *
 * ONE shared #liveToast serves the whole application (templates/base.html), and
 * last-message-wins is its governing copy contract. What KI-011 changed is that
 * an ACTION is no longer part of that contract. showToast() used to clear
 * #toast-body wholesale on every call, which destroyed a still-valid action
 * button raised by an earlier call; it now replaces only the message node and
 * keeps the action in its own slot until the action itself becomes invalid.
 *
 * The action's lifetime, per the owner's rulings
 * (docs/toast_action_continuity/PLANNING.md sections 1 and 6.1):
 *   - it lives for the duration of the toast that RAISED it, on its own timer;
 *   - a later toast with NO action preserves it;
 *   - a later toast WITH an action replaces it -- there are never two;
 *   - a standing action extends the toast to the later of the two deadlines;
 *   - it is invalidated by activation, by dismissal, or by expiry.
 *
 * STALENESS IS THE CALLER'S PROBLEM, and that change makes actions live LONGER,
 * so it increases that exposure rather than reducing it. This module cannot know
 * that the plan an onClick closes over was deleted or already activated. A
 * caller whose action can go stale must handle that in its own handler.
 *
 * ACCESSIBILITY, recorded accurately rather than optimistically (ruling OD-13).
 * #liveToast is aria-atomic="true", so while an action stands, every LATER
 * message is announced together with the standing action's label. The slot's
 * aria-live="off" governs changes WITHIN the slot only; it does not remove the
 * slot from what an atomic ancestor presents. The owner accepted that bounded
 * re-announcement rather than change base.html's live-region contract here.
 *
 * -----------------------------------------------------------------------------
 *
 * @param {string} type - Modern: 'success' | 'error' | 'warning' | 'info'.
 *                        Legacy: the message text.
 * @param {string|boolean} [message] - Modern: message to display.
 *                        Legacy: the boolean isError flag.
 * @param {Object|number} [options] - Optional configuration, or a number for the duration.
 * @param {number} options.duration - Duration in ms (default: 3000)
 * @param {string} options.requestId - Optional request ID for debugging; appended for type 'error' only
 * @param {{label: string, onClick: () => void, ariaLabel?: string}} options.action - Optional inline action button
 */
const SLOT_CLASS = 'toast-action-slot';
const MESSAGE_CLASS = 'toast-message';
const DEADLINE_ATTR = 'data-action-deadline';
const WIRED_ATTR = 'data-action-dismiss-wired';
const TIMER_ATTR = 'data-action-timer';

/** The standing action, read from the DOM. No module state. */
function readStanding(toastElement) {
    const button = toastElement.querySelector(`.${SLOT_CLASS} > button`);
    if (!button) {
        return null;
    }
    const raw = Number(button.getAttribute(DEADLINE_ATTR));
    return { button, deadline: Number.isFinite(raw) ? raw : 0 };
}

function clearStanding(toastElement) {
    const standing = readStanding(toastElement);
    if (!standing) {
        return;
    }
    // The timer handle lives on the node, so cancelling it needs no module
    // state and a discarded DOM tree takes its own timer with it.
    const handle = Number(standing.button.getAttribute(TIMER_ATTR));
    if (Number.isFinite(handle) && handle) {
        clearTimeout(handle);
    }
    standing.button.remove();
}

/** OQ-1 / OQ-7: expiry is a real invalidation, not merely a visual timeout. */
function expireIfDue(toastElement) {
    const standing = readStanding(toastElement);
    if (standing && Date.now() >= standing.deadline) {
        clearStanding(toastElement);
    }
}

/**
 * OQ-6: a dedicated slot that is a SIBLING OF THE MESSAGE and a CHILD OF
 * #toast-body.
 *   - inside #toast-body because e2e/fixtures.ts `expectToast` asserts against
 *     #toast-body, and e2e/volume-splitter.spec.ts:340 requires both
 *     "Plan #N saved." and "Activate for Plan tab" in that node's text (K9);
 *   - a DIV, never a SPAN, because toast.test.js B26 counts `#toast-body span`
 *     and must stay at exactly 1;
 *   - aria-live="off" so the slot's own changes never announce.
 */
function resolveSlot(toastBody) {
    let slot = toastBody.querySelector(`.${SLOT_CLASS}`);
    if (!slot) {
        slot = document.createElement('div');
        slot.className = `${SLOT_CLASS} d-inline`;
        slot.setAttribute('aria-live', 'off');
        toastBody.appendChild(slot);
    }
    return slot;
}

function buildActionButton(action, toastElement, deadline) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn btn-sm btn-link text-white text-decoration-underline ms-2 p-0 align-baseline';
    button.textContent = String(action.label);
    button.setAttribute(DEADLINE_ATTR, String(deadline));
    if (action.ariaLabel) {
        button.setAttribute('aria-label', action.ariaLabel);
    }
    button.addEventListener('click', () => {
        const instance = bootstrap.Toast.getInstance(toastElement);
        if (instance) {
            instance.hide();
        }
        button.remove();                       // OQ-7: activation invalidates
        try {
            action.onClick();
        } catch (err) {
            console.error('Toast action handler failed:', err);
        }
    });
    {
        // OQ-1 as signed: validity ends at the RAISING toast's own duration,
        // not merely at the next showToast(). Without this an action whose
        // deadline has passed stays rendered, focusable and CLICKABLE for as
        // long as a later message keeps the toast alive -- measured at 2273 ms
        // past deadline, with onClick firing.
        const handle = setTimeout(() => button.remove(), Math.max(0, deadline - Date.now()));
        button.setAttribute(TIMER_ATTR, String(handle));
    }
    return button;
}

/**
 * OQ-7: the close button and Bootstrap's own auto-hide both end in
 * hidden.bs.toast. A standing action must not outlive the toast it lives in.
 * The "already wired" flag is an ATTRIBUTE ON THE ELEMENT, not a module
 * variable, so a test that replaces document.body starts clean.
 */
function wireDismissal(toastElement) {
    if (toastElement.hasAttribute(WIRED_ATTR)) {
        return;
    }
    toastElement.setAttribute(WIRED_ATTR, '1');
    toastElement.addEventListener('hidden.bs.toast', () => clearStanding(toastElement));
}

/**
 * The dispose half of the replacement, factored out so the mutation matrix can
 * move it. Its POSITION is the contract: see the comment inside.
 */
function disposeExisting(toastElement) {
    const existingToast = bootstrap.Toast.getInstance(toastElement);
    if (!existingToast) {
        return;
    }
    // OD-12(a) -- F-NEW-1, and the ORDERING half of the same repair.
    //
    // The CALLER runs this BEFORE any content is written. That position is
    // load-bearing and was chosen by measurement, not taste: the flush below can
    // fire `hidden.bs.toast` synchronously, and the dismissal listener clears
    // whatever action is standing. With the dispose late, a close click and a
    // replacement in the SAME synchronous turn made the flush wipe the
    // BRAND-NEW action -- measured, final standing action `null`. Disposing
    // first means the flush can only ever clear the OUTGOING action, which is
    // what OQ-7 asks for.
    //
    // F-NEW-1 itself. Bootstrap's show()/hide() queue a completion callback that
    // dereferences `this._element`; dispose() sets that to null, so a
    // replacement landing inside the ~150 ms transition makes the queued
    // callback throw `Cannot read properties of null (reading 'classList')` --
    // measured deterministically at gap 0 and clean from 100 ms up. The repair
    // FLUSHES the pending callback synchronously, so it runs while the instance
    // is still live, and only then disposes. Bootstrap's
    // executeAfterTransition() listens for a real `transitionend` whose target
    // is the element, so a dispatched Event of that type satisfies it: public
    // DOM API only, no Bootstrap private touched, and the dispose-BEFORE-
    // construct order that B27 pins is preserved exactly.
    const midTransition = toastElement.classList.contains('showing')
        || toastElement.classList.contains('hiding');
    if (midTransition) {
        toastElement.dispatchEvent(new Event('transitionend'));
    }
    existingToast.dispose();
}

export function showToast(type, message, options = {}) {
    const validTypes = new Set(['success', 'error', 'warning', 'info']);

    // Backward compatibility: detect legacy signature showToast(message, isError?, duration?).
    //
    // KI-010. This used to test `!validTypes.has(type)` alone. Argument 1's two
    // domains overlap on exactly the four type words, so a legacy caller whose
    // message was one of them was misread as a modern call; the discriminator has
    // to look at argument 2 as well.
    //
    // Contract: owner ruling OD-6, docs/toast_type_word_collision/PLANNING.md
    // (Gate 1 signed 2026-08-27).
    //
    // `arguments.length` -- not `message === undefined` -- is load-bearing. It
    // keeps an explicitly supplied `undefined` a MODERN call, so a modern caller
    // whose message expression evaluates to undefined at runtime still gets the
    // red default-copy error toast rather than a GREEN toast reading the type
    // word. B13 pins that. If this function is ever rewritten with rest
    // parameters, carry the arity check across as `args.length < 2`; dropping it
    // silently reintroduces KI-010 for the one-argument form.
    const isLegacyCall = !validTypes.has(type)
        || typeof message === 'boolean'
        || arguments.length < 2;

    if (isLegacyCall) {
        const legacyMessage = type;
        const legacyIsError = typeof message === 'boolean' ? message : false;
        const legacyDuration = typeof options === 'number' ? options : undefined;
        const legacyOptions = typeof options === 'object' && options !== null ? { ...options } : {};

        type = legacyIsError ? 'error' : 'success';
        message = legacyMessage;
        options = legacyOptions;

        if (legacyDuration !== undefined) {
            options.duration = legacyDuration;
        }
    } else if (typeof options === 'number') {
        options = { duration: options };
    }

    const { duration = 3000, requestId = null, action = null } = options;

    const toastBody = document.getElementById("toast-body");
    if (!toastBody) {
        console.error("Error: toast-body not found in the DOM!");
        return;
    }

    const toastElement = document.getElementById("liveToast");
    if (!toastElement) {
        console.error("Error: liveToast not found in the DOM!");
        return;
    }

    disposeExisting(toastElement);

    wireDismissal(toastElement);
    expireIfDue(toastElement);

    let displayMessage;
    if (message !== undefined && message !== null) {
        displayMessage = String(message);
    } else {
        displayMessage = type === 'error' ? 'An unexpected error occurred.' : 'Action completed successfully.';
    }

    if (requestId && type === 'error') {
        displayMessage += ` (Request ID: ${requestId})`;
    }

    // ---- message: last-message-wins, unchanged (OQ-5) ------------------------
    let messageSpan = toastBody.querySelector(`span.${MESSAGE_CLASS}`);
    if (!messageSpan) {
        // First render into this body: drop whatever markup the template left
        // (an HTML comment and its indentation), then install the two managed
        // nodes. Everything after this is a targeted replacement, never a clear.
        toastBody.replaceChildren();
        messageSpan = document.createElement('span');
        messageSpan.className = MESSAGE_CLASS;
        toastBody.appendChild(messageSpan);
    }
    messageSpan.textContent = displayMessage;   // textContent, never innerHTML (I4)

    // ---- action resolution ---------------------------------------------------
    const wellFormed = Boolean(action && typeof action.onClick === 'function' && action.label);

    if (wellFormed) {
        clearStanding(toastElement);            // OQ-3: never two
        // The slot is created ONLY when a button is about to go in it, so the
        // 110 of 112 call sites that pass no action add no node at all.
        resolveSlot(toastBody)
            .appendChild(buildActionButton(action, toastElement, Date.now() + duration));
    }
    // OQ-2: a later call with no action leaves the standing action alone.

    // ---- OQ-4: the toast lives to the later applicable deadline ---------------
    const standing = readStanding(toastElement);
    const effectiveDelay = standing
        ? Math.max(duration, standing.deadline - Date.now())
        : duration;

    toastElement.classList.remove("bg-success", "bg-danger", "bg-warning", "bg-info");
    const typeToClass = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    };
    toastElement.classList.add(typeToClass[type] || 'bg-success');

    // ---- OQ-6 (focus) --------------------------------------------------------
    // In the pristine path the button is never detached, so focus cannot be
    // dropped and nothing needs restoring. The capture/restore pair is kept so
    // the E2E focus arm still has a subject when the wholesale clear is
    // reintroduced as a mutation, and so any future variant that DOES
    // re-render the button has the seam it needs.
    const hadFocus = Boolean(standing) && document.activeElement === standing.button;


    const toast = new bootstrap.Toast(toastElement, { delay: effectiveDelay });
    toast.show();

    if (hadFocus && standing.button.isConnected) {
        standing.button.focus();
    }
}

/**
 * Council finding A4. `span.toast-message` is this module's DOM shape; a caller
 * that queries it directly turns an internal detail into an unpinned
 * cross-module contract, which the next editor of this file (KI-010) can break
 * silently. Callers ask the module instead.
 *
 * Returns the rendered message text, or null when no toast has rendered yet.
 * Deliberately excludes the action slot: the whole point is to answer "is the
 * MESSAGE still ours", which #toast-body's own textContent cannot do once a
 * button lives inside it.
 */
export function toastMessageText() {
    return document.querySelector(`#toast-body span.${MESSAGE_CLASS}`)?.textContent ?? null;
}
