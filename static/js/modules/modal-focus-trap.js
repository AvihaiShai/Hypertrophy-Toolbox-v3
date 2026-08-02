/**
 * Modal focus-trap wraparound (KI-006).
 *
 * Bootstrap ships its own FocusTrap, but it is a *bounce-back* trap: it listens for
 * `focusin` on the document and, when focus lands outside the modal, sends it back to
 * the first (or last, when tabbing backwards) focusable child.
 *
 * That has one hole. When the modal's last focusable control is also the last focusable
 * element in the document, pressing Tab moves focus to `document.body` — and `body` does
 * not emit `focusin`. Bootstrap's handler never runs and focus escapes the dialog.
 *
 * This is not new in Bootstrap 5.3; the same hole exists in 5.1.3. It shows up on
 * /workout_log (`#clearLogModal` is the last focusable thing on the page) and not on
 * /workout_plan, where two focusable elements happen to follow the dialog. Depending on
 * unrelated DOM ordering for keyboard containment is exactly the fragility KI-006
 * recorded.
 *
 * The fix wraps focus at the boundary instead of catching it after it leaves: on Tab from
 * the last control, and Shift+Tab from the first, move focus explicitly. Bootstrap's own
 * trap still handles focus arriving from elsewhere (a stray programmatic focus, a click
 * outside); the two are complementary, and the handler is a no-op for every other key.
 */
(function () {
    'use strict';

    // Same selector list Bootstrap's SelectorEngine.focusableChildren uses, so "first"
    // and "last" mean the same elements Bootstrap would pick.
    var FOCUSABLE_SELECTOR = [
        'a', 'button', 'input', 'textarea', 'select', 'details',
        '[tabindex]', '[contenteditable="true"]'
    ].map(function (selector) {
        return selector + ':not([tabindex^="-"])';
    }).join(',');

    function focusableChildren(modal) {
        return Array.prototype.filter.call(
            modal.querySelectorAll(FOCUSABLE_SELECTOR),
            function (element) {
                if (element.disabled) {
                    return false;
                }
                var rect = element.getBoundingClientRect();
                return rect.width > 0 && rect.height > 0;
            }
        );
    }

    function handleKeydown(event) {
        if (event.key !== 'Tab') {
            return;
        }

        var modal = event.currentTarget;
        var items = focusableChildren(modal);
        if (items.length === 0) {
            return;
        }

        var first = items[0];
        var last = items[items.length - 1];
        var active = document.activeElement;

        if (event.shiftKey && active === first) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && active === last) {
            event.preventDefault();
            first.focus();
        }
    }

    document.addEventListener('shown.bs.modal', function (event) {
        event.target.addEventListener('keydown', handleKeydown);
    });

    document.addEventListener('hidden.bs.modal', function (event) {
        event.target.removeEventListener('keydown', handleKeydown);
    });
})();
