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

    // Only `data-theme` is set here. Setting `color-scheme` before the first
    // paint made Chromium rasterise rounded frame edges nondeterministically
    // -- two loads of an identical layout produced different pixels, which no
    // committed baseline can satisfy. `darkMode.js` applies `color-scheme`
    // once the DOM is ready, which keeps native controls theme-matched
    // without destabilising the first paint.
    root.setAttribute('data-theme', theme);
})();
