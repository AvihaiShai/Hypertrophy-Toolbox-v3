export function initializeMenu(menu) {
    const toggle = menu.querySelector('[aria-haspopup="menu"]');
    const popover = menu.querySelector('[role="menu"]');
    const items = [...popover.querySelectorAll('[role="menuitem"]')];

    function setOpen(open) {
        popover.hidden = !open;
        toggle.setAttribute('aria-expanded', String(open));
        if (open) items[0]?.focus();
    }

    function closeAndFocusToggle() {
        setOpen(false);
        toggle.focus({ preventScroll: true });
    }

    toggle.addEventListener('click', () => setOpen(popover.hidden));
    toggle.addEventListener('keydown', event => {
        if (event.key !== 'ArrowDown') return;
        event.preventDefault();
        setOpen(true);
    });

    popover.addEventListener('keydown', event => {
        if (event.key === 'Escape' || event.key === 'Tab') {
            if (event.key === 'Escape') {
                event.preventDefault();
                event.stopPropagation();
            }
            closeAndFocusToggle();
            return;
        }

        const step = event.key === 'ArrowDown' ? 1 : event.key === 'ArrowUp' ? -1 : 0;
        if (!step || !items.length) return;
        event.preventDefault();
        const current = items.indexOf(document.activeElement);
        items[(current + step + items.length) % items.length].focus();
    });

    popover.addEventListener('click', event => {
        const item = event.target.closest('[role="menuitem"]');
        if (item && item.dataset.bsToggle !== 'modal') closeAndFocusToggle();
    });

    document.addEventListener('click', event => {
        if (!popover.hidden && !menu.contains(event.target)) setOpen(false);
    });

    // Bootstrap's delegated click handler runs before the menu item's click
    // bubbles. Its show event provides a hook before the dialog is displayed.
    document.addEventListener('show.bs.modal', event => {
        if (!(event.relatedTarget instanceof Element) || !popover.contains(event.relatedTarget)) return;
        setOpen(false);
        event.target.addEventListener('hidden.bs.modal', closeAndFocusToggle, { once: true });
    });
}
