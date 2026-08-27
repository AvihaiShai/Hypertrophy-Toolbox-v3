/**
 * Toast notification functionality with standardized types.
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
 * `showToast('error', undefined)` is a MODERN call and renders the default error
 * copy. That distinction rests on `arguments.length` -- see the comment on the
 * `isLegacyCall` predicate below before refactoring this function's signature.
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
export function showToast(type, message, options = {}) {
    const validTypes = new Set(['success', 'error', 'warning', 'info']);

    // Backward compatibility: detect legacy signature showToast(message, isError?, duration?).
    //
    // KI-010. This used to test `!validTypes.has(type)` alone, so a LEGACY caller
    // whose message happened to be one of the four type words was misread as a
    // modern call: showToast('error', true) rendered the body text "true", and
    // showToast('warning') rendered "Action completed successfully." on a yellow
    // toast. Argument 1's domains overlap on exactly those four strings, so the
    // discriminator has to look at argument 2 as well.
    //
    // Contract (owner ruling OD-6, Gate 1 signed 2026-08-27,
    // docs/toast_type_word_collision/PLANNING.md): argument 1 is a TYPE only when
    // it is one of the four words AND argument 2 is not a boolean AND argument 2
    // was actually supplied.
    //
    // `arguments.length` -- not `message === undefined` -- is load-bearing and was
    // chosen deliberately over the alternative spelling. It keeps an explicitly
    // supplied `undefined` a MODERN call, so a modern caller whose message
    // expression evaluates to undefined at runtime still gets the red default-copy
    // error toast rather than a GREEN toast reading the type word. B13 pins that.
    // If this function is ever rewritten with rest parameters, carry the arity
    // check across as `args.length < 2`; dropping it silently reintroduces KI-010
    // for the one-argument form.
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
        // Support showToast('success', 'Message', 5000)
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

    // Ensure message is a readable string
    let displayMessage;
    if (message !== undefined && message !== null) {
        displayMessage = String(message);
    } else {
        displayMessage = type === 'error' ? 'An unexpected error occurred.' : 'Action completed successfully.';
    }

    // Set message with optional request ID for debugging
    if (requestId && type === 'error') {
        displayMessage += ` (Request ID: ${requestId})`;
    }

    toastBody.innerHTML = '';
    const messageSpan = document.createElement('span');
    messageSpan.textContent = displayMessage;
    toastBody.appendChild(messageSpan);

    if (action && typeof action.onClick === 'function' && action.label) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'btn btn-sm btn-link text-white text-decoration-underline ms-2 p-0 align-baseline';
        button.textContent = String(action.label);
        if (action.ariaLabel) {
            button.setAttribute('aria-label', action.ariaLabel);
        }
        button.addEventListener('click', () => {
            const instance = bootstrap.Toast.getInstance(toastElement);
            if (instance) {
                instance.hide();
            }
            try {
                action.onClick();
            } catch (err) {
                console.error('Toast action handler failed:', err);
            }
        });
        toastBody.appendChild(button);
    }

    // Remove all possible background classes
    toastElement.classList.remove("bg-success", "bg-danger", "bg-warning", "bg-info");
    
    // Map type to Bootstrap background class
    const typeToClass = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    };
    
    const bgClass = typeToClass[type] || 'bg-success';
    toastElement.classList.add(bgClass);

    // Dispose any existing toast instance to prevent animation conflicts
    // This ensures clean transitions when showing rapid notifications
    const existingToast = bootstrap.Toast.getInstance(toastElement);
    if (existingToast) {
        existingToast.dispose();
    }

    const toast = new bootstrap.Toast(toastElement, { delay: duration });
    toast.show();
}

