/**
 * Navbar Enhancements - Modern 2025 Features
 * - Compact mode on scroll
 * - Mobile menu focus trap
 * - Body scroll lock
 * - Reduced motion support
 */

export function initializeNavbarEnhancements() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;
  if (navbar.dataset.navbarEnhancementsInitialized === 'true') return;
  navbar.dataset.navbarEnhancementsInitialized = 'true';

  const mobileMenuToggle = navbar.querySelector('.navbar-toggler, .nb-menu-btn');
  const mobileMenu = navbar.querySelector('#navbarNav');

  initializeDesktopHoverDropdowns(navbar);
  
  // Compact mode on scroll
  function handleScroll() {
    navbar.classList.toggle('nb-compact', window.scrollY > 80);
  }

  // Throttled scroll handler
  let ticking = false;
  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        handleScroll();
        ticking = false;
      });
      ticking = true;
    }
  }
  
  window.addEventListener('scroll', onScroll, { passive: true });
  
  // Initialize compact state
  handleScroll();
  
  // Mobile menu enhancements
  if (mobileMenuToggle && mobileMenu) {
    // Track menu state
    let isMenuOpen = false;
    let focusTimer = null;
    let focusableElements = [];
    let firstFocusableElement = null;
    let lastFocusableElement = null;
    
    // Get focusable elements within mobile menu
    function updateFocusableElements() {
      if (!mobileMenu.classList.contains('show')) return;
      
      focusableElements = Array.from(
        mobileMenu.querySelectorAll(
          'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'
        )
      ).filter(el => el.getClientRects().length && getComputedStyle(el).visibility === 'visible');
      
      firstFocusableElement = focusableElements[0] || null;
      lastFocusableElement = focusableElements[focusableElements.length - 1] || null;
    }
    
    // Trap focus within mobile menu
    function trapFocus(e) {
      if (!isMenuOpen || e.defaultPrevented) return;
      
      if (e.key === 'Tab') {
        // Submenu visibility and disabled scale buttons can change while open.
        updateFocusableElements();
        if (e.shiftKey) {
          // Shift + Tab (backward)
          if (document.activeElement === firstFocusableElement) {
            e.preventDefault();
            lastFocusableElement?.focus();
          }
        } else {
          // Tab (forward)
          if (document.activeElement === lastFocusableElement) {
            e.preventDefault();
            firstFocusableElement?.focus();
          }
        }
      }
      
      // Close on Escape
      if (e.key === 'Escape' && isMenuOpen) {
        hideMobileMenu();
      }
    }
    
    // Body scroll lock
    function lockBodyScroll() {
      if (isMenuOpen) {
        document.body.style.overflow = 'hidden';
        // Add inert to main content if supported (with fallback)
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
          try {
            if ('inert' in mainContent) {
              mainContent.setAttribute('inert', '');
            }
          } catch (e) {
            // Fallback: use aria-hidden instead
            mainContent.setAttribute('aria-hidden', 'true');
          }
        }
      }
    }
    
    function unlockBodyScroll() {
      document.body.style.overflow = '';
      const mainContent = document.getElementById('main-content');
      if (mainContent) {
        if (mainContent.hasAttribute('inert')) {
          mainContent.removeAttribute('inert');
        }
        if (mainContent.hasAttribute('aria-hidden')) {
          mainContent.removeAttribute('aria-hidden');
        }
      }
    }
    
    // Open mobile menu
    function openMobileMenu() {
      isMenuOpen = true;
      navbar.setAttribute('aria-expanded', 'true');
      mobileMenuToggle.setAttribute('aria-expanded', 'true');
      lockBodyScroll();
      updateFocusableElements();
      
      // Focus first element after a brief delay
      focusTimer = setTimeout(() => {
        if (!mobileMenu.contains(document.activeElement)) firstFocusableElement?.focus();
      }, 100);
      
      // Add event listeners
      mobileMenu.addEventListener('keydown', trapFocus);
      document.addEventListener('keydown', trapFocus);
    }
    
    // Ask Bootstrap to close; cleanup runs once from hidden.bs.collapse
    function hideMobileMenu() {
      bootstrap.Collapse.getOrCreateInstance(mobileMenu, { toggle: false }).hide();
    }

    // Release menu state (safe to call repeatedly)
    function releaseMenuState() {
      isMenuOpen = false;
      clearTimeout(focusTimer);
      navbar.setAttribute('aria-expanded', 'false');
      mobileMenuToggle.setAttribute('aria-expanded', 'false');
      unlockBodyScroll();

      // Remove event listeners
      mobileMenu.removeEventListener('keydown', trapFocus);
      document.removeEventListener('keydown', trapFocus);
    }

    // Leave the hamburger layout: reset by hand without moving focus
    function leaveHamburgerLayout() {
      releaseMenuState();
      mobileMenu.classList.remove('show');
      mobileMenuToggle.classList.add('collapsed');
    }

    function isDesktopLayout() {
      return window.matchMedia('(min-width: 1360px)').matches;
    }

    // Handle Bootstrap collapse events (since we're using Bootstrap's collapse)
    mobileMenu.addEventListener('shown.bs.collapse', () => {
      if (isDesktopLayout()) {
        leaveHamburgerLayout();
      } else {
        openMobileMenu();
      }
    });

    mobileMenu.addEventListener('hidden.bs.collapse', () => {
      releaseMenuState();
      if (!isDesktopLayout()) mobileMenuToggle.focus();
    });

    // Close when the panel's own empty space is clicked, not a control inside it
    mobileMenu.addEventListener('click', (e) => {
      if (e.target === mobileMenu) {
        hideMobileMenu();
      }
    });

    // Close the menu when the viewport leaves the hamburger layout
    window.addEventListener('resize', () => {
      if (isDesktopLayout() && mobileMenu.classList.contains('show')) {
        leaveHamburgerLayout();
      }
    }, { passive: true });

    // Initial state check
    if (mobileMenu.classList.contains('show')) {
      openMobileMenu();
    }
  }
}

function initializeDesktopHoverDropdowns(navbar) {
  if (navbar.dataset.hoverDropdownsInitialized === 'true') return;
  navbar.dataset.hoverDropdownsInitialized = 'true';

  if (typeof bootstrap === 'undefined' || !bootstrap.Dropdown) return;

  const desktopHoverQuery = window.matchMedia('(hover: hover) and (pointer: fine) and (min-width: 1360px)');
  const dropdowns = navbar.querySelectorAll('.dropdown');

  dropdowns.forEach((dropdown) => {
    const toggle = dropdown.querySelector('[data-bs-toggle="dropdown"]');
    const menu = dropdown.querySelector('.dropdown-menu');
    if (!toggle || !menu) return;

    const dropdownInstance = bootstrap.Dropdown.getOrCreateInstance(toggle);
    let hideTimer = null;

    function isDesktopHover() {
      return desktopHoverQuery.matches;
    }

    function clearHideTimer() {
      if (hideTimer) {
        window.clearTimeout(hideTimer);
        hideTimer = null;
      }
    }

    function openDropdown() {
      if (!isDesktopHover()) return;

      clearHideTimer();
      dropdownInstance.show();
      toggle.setAttribute('aria-expanded', 'true');
    }

    function closeDropdown(delay = 160) {
      if (!isDesktopHover()) return;

      clearHideTimer();
      hideTimer = window.setTimeout(() => {
        dropdownInstance.hide();
        toggle.setAttribute('aria-expanded', 'false');
      }, delay);
    }

    dropdown.addEventListener('mouseenter', openDropdown);
    dropdown.addEventListener('mouseleave', () => closeDropdown());
    dropdown.addEventListener('focusin', (event) => {
      if (!dropdown.contains(event.relatedTarget)) openDropdown();
    });
    // Cached 3.0.1 navbar CSS highlights the open trigger while a submenu item has focus.
    dropdown.addEventListener('shown.bs.dropdown', () => {
      if (isDesktopHover()) dropdown.classList.add('is-hover-open');
    });
    dropdown.addEventListener('hidden.bs.dropdown', () => dropdown.classList.remove('is-hover-open'));
    dropdown.addEventListener('focusout', (event) => {
      if (!dropdown.contains(event.relatedTarget)) {
        closeDropdown(80);
      }
    });

    toggle.addEventListener('click', (event) => {
      if (!isDesktopHover()) return;

      event.preventDefault();
      event.stopPropagation();
      openDropdown();
    });

    toggle.addEventListener('keydown', (event) => {
      if (!isDesktopHover()) return;

      if (event.key === 'ArrowDown' || event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openDropdown();
        menu.querySelector('.dropdown-item')?.focus();
      }

      if (event.key === 'Escape') {
        closeDropdown(0);
      }
    });

    menu.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        toggle.focus();
        closeDropdown(0);
      }
    });

    desktopHoverQuery.addEventListener('change', () => {
      dropdownInstance.hide();
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeNavbarEnhancements);
} else {
  initializeNavbarEnhancements();
}
