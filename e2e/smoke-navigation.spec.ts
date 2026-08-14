/**
 * E2E Test: Smoke and Navigation
 * 
 * Tests that the app loads correctly and navigation works
 * as expected across all main routes.
 */
import type { Page } from '@playwright/test';
import { test, expect } from './console-guard';
import { ROUTES, SELECTORS, waitForPageReady } from './fixtures';

const ANALYZE_TOGGLE = '#navbar .dropdown-toggle:has-text("Analyze")';

async function openAnalyzeDropdown(page: Page): Promise<void> {
  const analyzeToggle = page.locator(ANALYZE_TOGGLE);
  await expect(analyzeToggle).toBeVisible();
  await analyzeToggle.click();
  await expect(page.locator('#navbar .dropdown-menu.show')).toBeVisible();
}

test.describe('Global Smoke and Navigation', () => {
  test('home page loads with navbar and key links visible', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Assert navbar exists
    const navbar = page.locator(SELECTORS.NAVBAR);
    await expect(navbar).toBeVisible();

    // Assert brand link
    const brand = page.locator(SELECTORS.NAV_BRAND);
    await expect(brand).toBeVisible();
    await expect(brand).toContainText('Hypertrophy Toolbox');

    // Assert top-level nav links are visible
    await expect(page.locator(SELECTORS.NAV_WORKOUT_PLAN)).toBeVisible();
    await expect(page.locator(SELECTORS.NAV_WORKOUT_LOG)).toBeVisible();
    await expect(page.locator(SELECTORS.NAV_PROGRESSION_PLAN)).toBeVisible();
    await expect(page.locator(SELECTORS.NAV_USER_PROFILE)).toBeVisible();
    await expect(page.locator(SELECTORS.NAV_BODY_COMPOSITION)).toBeVisible();
    await expect(page.locator(SELECTORS.NAV_VOLUME_SPLITTER)).toBeVisible();
    await expect(page.locator(SELECTORS.NAV_BACKUP)).toBeVisible();

    // Summary links live inside the Analyze dropdown in the P5 nav flow.
    await openAnalyzeDropdown(page);
    await expect(page.locator(SELECTORS.NAV_WEEKLY_SUMMARY)).toBeVisible();
    await expect(page.locator(SELECTORS.NAV_SESSION_SUMMARY)).toBeVisible();

    // Assert dark mode toggle is visible
    await expect(page.locator(SELECTORS.DARK_MODE_TOGGLE)).toBeVisible();
  });

  test('home page displays welcome content', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Assert welcome page is loaded
    const welcomePage = page.locator(SELECTORS.PAGE_WELCOME);
    await expect(welcomePage).toBeVisible();

    // Check for hero heading
    await expect(page.locator('h1')).toContainText('Hypertrophy');
  });

  test('navigate to Workout Plan via navbar', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Click workout plan nav link
    await page.locator(SELECTORS.NAV_WORKOUT_PLAN).click();
    await waitForPageReady(page);

    // Verify we're on workout plan page
    await expect(page).toHaveURL(/\/workout_plan/);
    const workoutPage = page.locator(SELECTORS.PAGE_WORKOUT_PLAN);
    await expect(workoutPage).toBeVisible();
    await expect(page.locator('h1')).toContainText('Workout Plan');
  });

  test('navigate to Weekly Summary via navbar', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    await openAnalyzeDropdown(page);
    await page.locator(SELECTORS.NAV_WEEKLY_SUMMARY).click();
    await waitForPageReady(page);

    await expect(page).toHaveURL(/\/weekly_summary/);
    const summaryPage = page.locator(SELECTORS.PAGE_WEEKLY_SUMMARY);
    await expect(summaryPage).toBeVisible();
    await expect(page.locator('h1')).toContainText(/(Weekly|Plan Volume) Summary/i);
  });

  test('navigate to Session Summary via navbar', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    await openAnalyzeDropdown(page);
    await page.locator(SELECTORS.NAV_SESSION_SUMMARY).click();
    await waitForPageReady(page);

    await expect(page).toHaveURL(/\/session_summary/);
    const sessionPage = page.locator(SELECTORS.PAGE_SESSION_SUMMARY);
    await expect(sessionPage).toBeVisible();
    await expect(page.locator('h1')).toContainText('Session Summary');
  });

  test('navigate to Workout Log via navbar', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    await page.locator(SELECTORS.NAV_WORKOUT_LOG).click();
    await waitForPageReady(page);

    await expect(page).toHaveURL(/\/workout_log/);
    const logPage = page.locator(SELECTORS.PAGE_WORKOUT_LOG);
    await expect(logPage).toBeVisible();
    await expect(page.locator('h1')).toContainText('Workout Log');
  });

  test('navigate to Progression Plan via navbar', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    await page.locator(SELECTORS.NAV_PROGRESSION_PLAN).click();
    await waitForPageReady(page);

    await expect(page).toHaveURL(/\/progression/);
    const progressionPage = page.locator(SELECTORS.PAGE_PROGRESSION);
    await expect(progressionPage).toBeVisible();
    await expect(page.locator('h1')).toContainText('Progression Plan');
  });

  test('navigate to Volume Splitter via navbar', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    await page.locator(SELECTORS.NAV_VOLUME_SPLITTER).click();
    await waitForPageReady(page);

    await expect(page).toHaveURL(/\/volume_splitter/);
    const volumePage = page.locator(SELECTORS.PAGE_VOLUME_SPLITTER);
    await expect(volumePage).toBeVisible();
    await expect(page.locator('h1')).toContainText('Volume Splitter');
  });

  test('navigate back to home via brand link', async ({ page }) => {
    // Start from workout plan page
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    // Click brand to go home
    await page.locator(SELECTORS.NAV_BRAND).click();
    await waitForPageReady(page);

    // Verify we're on home page
    await expect(page).toHaveURL(/\/$/);
    const welcomePage = page.locator(SELECTORS.PAGE_WELCOME);
    await expect(welcomePage).toBeVisible();
  });

  test('all pages accessible without errors (full navigation cycle)', async ({ page }) => {
    const routes = [
      { url: ROUTES.HOME, selector: SELECTORS.PAGE_WELCOME },
      { url: ROUTES.WORKOUT_PLAN, selector: SELECTORS.PAGE_WORKOUT_PLAN },
      { url: ROUTES.WEEKLY_SUMMARY, selector: SELECTORS.PAGE_WEEKLY_SUMMARY },
      { url: ROUTES.SESSION_SUMMARY, selector: SELECTORS.PAGE_SESSION_SUMMARY },
      { url: ROUTES.WORKOUT_LOG, selector: SELECTORS.PAGE_WORKOUT_LOG },
      { url: ROUTES.PROGRESSION, selector: SELECTORS.PAGE_PROGRESSION },
      { url: ROUTES.USER_PROFILE, selector: SELECTORS.PAGE_USER_PROFILE },
      { url: ROUTES.BODY_COMPOSITION, selector: SELECTORS.PAGE_BODY_COMPOSITION },
      { url: ROUTES.VOLUME_SPLITTER, selector: SELECTORS.PAGE_VOLUME_SPLITTER },
    ];

    for (const route of routes) {
      await page.goto(route.url);
      await waitForPageReady(page);
      await expect(page.locator(route.selector)).toBeVisible({ timeout: 10000 });
      await expect(page.locator('main#main-content')).toHaveCount(1);
      await expect(page.locator('[role="main"]')).toHaveCount(0);
    }
  });

  /**
   * The acceptance proof for the local-first assets packet: navigating the whole
   * app must not contact another origin.
   *
   * Three assertions, because an origin census alone is weak in two directions.
   * A page whose vendored URLs all 404 requests nothing external and would pass
   * — and nothing else would notice, because the console collector cannot see a
   * failed load either (see `fixtures.ts`). And a listener registered after
   * navigation records nothing and passes forever. So this also requires every
   * same-origin response to be non-error, and requires the specific vendored
   * payloads to have actually been fetched.
   *
   * What this cannot cover: `<link rel="preconnect">` opens a socket without
   * requesting a resource, so no request event exists for it. That deletion is
   * asserted in `tests/test_local_first_assets.py` instead.
   */
  test('no page loads an asset from another origin', async ({ page, baseURL }) => {
    const origin = new URL(baseURL as string).origin;
    const foreign: string[] = [];
    const errored: string[] = [];
    const vendored = new Set<string>();

    page.on('request', (request) => {
      const url = request.url();
      // data:, blob: and about: are inline payloads, not network fetches.
      if (!/^https?:/i.test(url)) return;
      if (!url.startsWith(origin)) {
        foreign.push(`${request.resourceType()} ${url}`);
      }
    });
    page.on('response', (response) => {
      const url = response.url();
      if (!url.startsWith(origin)) return;
      if (response.status() >= 400) {
        errored.push(`${response.status()} ${new URL(url).pathname}`);
      }
      if (url.includes('/static/vendor/')) {
        vendored.add(new URL(url).pathname);
      }
    });

    for (const route of Object.values(ROUTES)) {
      await page.goto(route);
      await waitForPageReady(page);
    }

    expect(
      foreign,
      'The app is local-first and must load every asset from its own origin',
    ).toEqual([]);
    expect(
      errored,
      'A vendored asset that 404s makes the origin census pass vacuously',
    ).toEqual([]);

    // Every one of these is loaded unconditionally by a template, and each has
    // a consumer that fails silently when the library is absent.
    for (const required of [
      '/static/vendor/inter/inter.css',
      '/static/vendor/fontawesome/css/all.min.css',
      '/static/vendor/bootstrap/js/bootstrap.bundle.min.js',
      '/static/vendor/sortable/Sortable.min.js',
      '/static/vendor/flatpickr/flatpickr.min.js',
      '/static/vendor/popperjs/popper.min.js',
      '/static/vendor/tippy/tippy-bundle.umd.min.js',
    ]) {
      expect(
        [...vendored],
        `${required} was never requested while walking every route`,
      ).toContain(required);
    }
  });
});
