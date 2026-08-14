/**
 * E2E Test: Dark Mode Persistence
 * 
 * Tests that dark mode toggle works correctly and
 * persists across page reloads.
 */
import { test, expect, ROUTES, SELECTORS, waitForPageReady, getDarkModeState, getStoredDarkMode } from './fixtures';
import { Page } from '@playwright/test';

/**
 * Click the dark mode toggle using JavaScript evaluation.
 * Bypasses Playwright's actionability checks which fail due to navbar CSS zoom.
 */
async function clickDarkModeToggle(page: Page): Promise<void> {
  await page.evaluate(() => {
    const toggle = document.querySelector('#darkModeToggle') as HTMLElement;
    if (toggle) toggle.click();
  });
  await page.waitForTimeout(100); // Small delay for theme transition
}

test.describe('Dark Mode Persistence', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    // Clear localStorage before each test to ensure clean state
    await page.goto(ROUTES.HOME);
    await page.evaluate(() => localStorage.clear());
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('dark mode toggle changes theme from light to dark', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Get initial state - should be light by default (or system preference)
    const initialTheme = await getDarkModeState(page);
    
    // Click dark mode toggle via JS (bypasses CSS zoom issues)
    const toggle = page.locator(SELECTORS.DARK_MODE_TOGGLE);
    await expect(toggle).toBeVisible();
    await clickDarkModeToggle(page);

    // Theme should have changed
    const newTheme = await getDarkModeState(page);
    expect(newTheme).not.toBe(initialTheme);
  });

  test('dark mode preference persists in localStorage', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Click dark mode toggle via JS
    await clickDarkModeToggle(page);

    // Check localStorage
    const storedValue = await getStoredDarkMode(page);
    expect(storedValue).toBe('true');

    // Click again to toggle back
    await clickDarkModeToggle(page);

    // Check localStorage updated
    const storedValue2 = await getStoredDarkMode(page);
    expect(storedValue2).toBe('false');
  });

  test('dark mode persists after page reload', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Click dark mode toggle to enable dark mode
    const toggle = page.locator(SELECTORS.DARK_MODE_TOGGLE);
    await clickDarkModeToggle(page);

    // Verify dark mode is active
    const themeBeforeReload = await getDarkModeState(page);
    expect(themeBeforeReload).toBe('dark');

    // Reload the page
    await page.reload();
    await waitForPageReady(page);

    // Dark mode should still be active
    const themeAfterReload = await getDarkModeState(page);
    expect(themeAfterReload).toBe('dark');

    // Toggle button text should show "Light Mode" when dark mode is active
    const toggleText = await toggle.locator('span').textContent();
    expect(toggleText).toContain('Light Mode');
  });

  test('toggle back to light mode works correctly', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Enable dark mode
    await clickDarkModeToggle(page);
    expect(await getDarkModeState(page)).toBe('dark');

    // Disable dark mode (go back to light)
    await clickDarkModeToggle(page);
    expect(await getDarkModeState(page)).toBe('light');

    // Reload and verify light mode persists
    await page.reload();
    await waitForPageReady(page);
    expect(await getDarkModeState(page)).toBe('light');
  });

  test('dark mode persists across different pages', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Enable dark mode
    await clickDarkModeToggle(page);
    expect(await getDarkModeState(page)).toBe('dark');

    // Navigate to different pages and verify dark mode persists
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);
    expect(await getDarkModeState(page)).toBe('dark');

    await page.goto(ROUTES.WEEKLY_SUMMARY);
    await waitForPageReady(page);
    expect(await getDarkModeState(page)).toBe('dark');

    await page.goto(ROUTES.VOLUME_SPLITTER);
    await waitForPageReady(page);
    expect(await getDarkModeState(page)).toBe('dark');
  });

  // Register row X6. darkMode.js suppresses transitions for the two frames
  // around a switch so the swap is instant. The CSS half of that pair was
  // deleted by ee82643 and the class matched nothing for four months, so this
  // asserts the suppression reaches the element — not merely that the class is
  // applied, which stayed true throughout the regression.
  test('theme toggle suppresses transitions while switching', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);
    await expect(page.locator(SELECTORS.DARK_MODE_TOGGLE)).toBeVisible();

    const observed = await page.evaluate(() => new Promise<{
      classDuringSwitch: boolean;
      bodyTransitionDuringSwitch: string;
      classAfterSwitch: boolean;
    }>((resolve) => {
      const root = document.documentElement;
      (document.querySelector('#darkModeToggle') as HTMLElement).click();

      // Still inside the click handler's task: applyTheme() has added the class
      // and has not yet reached its double-rAF removal, so this is the only
      // moment at which the suppression is observable.
      const classDuringSwitch = root.classList.contains('theme-animating');
      const bodyTransitionDuringSwitch = getComputedStyle(document.body).transitionDuration;

      // applyTheme queues its removal for the second frame. Ours is queued
      // behind it, so by the third callback the removal has already run.
      requestAnimationFrame(() => requestAnimationFrame(() => requestAnimationFrame(() => {
        resolve({
          classDuringSwitch,
          bodyTransitionDuringSwitch,
          classAfterSwitch: root.classList.contains('theme-animating'),
        });
      })));
    }));

    expect(
      observed.classDuringSwitch,
      'darkMode.js did not apply .theme-animating, so there is nothing for the rule to match'
    ).toBe(true);

    expect(
      observed.bodyTransitionDuringSwitch,
      `body still transitions (${observed.bodyTransitionDuringSwitch}) while .theme-animating is applied, so the suppression rule is not reaching it`
    ).toBe('0s');

    expect(
      observed.classAfterSwitch,
      '.theme-animating was never removed, which would leave transitions dead for the rest of the session'
    ).toBe(false);
  });

  test('toggle icon changes correctly with theme', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const toggle = page.locator(SELECTORS.DARK_MODE_TOGGLE);
    const icon = toggle.locator('i');

    // Initial state - light mode should show moon icon
    await expect(icon).toHaveClass(/fa-moon/);

    // Toggle to dark mode - should show sun icon
    await clickDarkModeToggle(page);
    await expect(icon).toHaveClass(/fa-sun/);

    // Toggle back to light mode - should show moon icon again
    await clickDarkModeToggle(page);
    await expect(icon).toHaveClass(/fa-moon/);
  });
});
