(function initializeThemeBeforePaint() {
    const root = document.documentElement;
    let storedPreference = null;

    try {
        storedPreference = localStorage.getItem('darkMode');
    } catch (_error) {
        // Storage can be unavailable in hardened/private browser contexts.
    }

    const followsSystem = storedPreference === null;
    const prefersDark = window.matchMedia
        && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = followsSystem ? prefersDark : storedPreference === 'true';
    const theme = isDark ? 'dark' : 'light';

    root.setAttribute('data-theme', theme);
    root.style.colorScheme = theme;
})();
