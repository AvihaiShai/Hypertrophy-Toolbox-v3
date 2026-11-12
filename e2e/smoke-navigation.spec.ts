/**
 * E2E Test: Smoke and Navigation
 * 
 * Tests that the app loads correctly and navigation works
 * as expected across all main routes.
 */
import type { Browser, BrowserContext, Page, Response } from '@playwright/test';
import { test, expect } from './console-guard';
import { ROUTES, SELECTORS, waitForPageReady } from './fixtures';
import { installStaticReplay, isStaticAssetRecorded, staticRecordingsSettled } from './static-replay';

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

/** Fetch `path` from inside the page and return the browser-side response. */
async function fetchInPage(
  page: Page,
  path: string,
  method = 'GET',
  headers: Record<string, string> = {},
): Promise<Response> {
  const [response] = await Promise.all([
    page.waitForResponse((r) => r.url().endsWith(path) && r.request().method() === method),
    page.evaluate(
      ({ url, verb, extra }) =>
        fetch(url, { method: verb, headers: extra }).then((r) => r.arrayBuffer()).then(() => undefined),
      { url: path, verb: method, extra: headers },
    ),
  ]);
  return response;
}

/** A URL no earlier test in this worker can have recorded. */
function coldPath(path: string, tag: string): string {
  return `${path}?${tag}=${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

// These build their own contexts with replay installed explicitly, so they
// hold under PW_STATIC_REPLAY=0 as well.
test.describe('Static asset replay', () => {
  async function replayContext(browser: Browser, baseURL: string): Promise<BrowserContext> {
    const context = await browser.newContext({ baseURL });
    await installStaticReplay(context, new URL(baseURL).origin);
    return context;
  }

  test('a second context replays a recorded asset with identical bytes', async ({ browser, baseURL }) => {
    const path = coldPath('/static/js/app.js', 'replay-probe');
    const first = await replayContext(browser, baseURL!);
    const second = await replayContext(browser, baseURL!);
    try {
      const firstPage = await first.newPage();
      await firstPage.goto(ROUTES.HOME);
      const native = await fetchInPage(firstPage, path);
      expect(await native.serverAddr(), 'a cold asset must come from the server').not.toBeNull();
      await expect.poll(() => isStaticAssetRecorded(native.url())).toBe(true);

      const secondPage = await second.newPage();
      await secondPage.goto(ROUTES.HOME);
      const replayed = await fetchInPage(secondPage, path);
      expect(await replayed.serverAddr(), 'a recorded asset must not open a connection').toBeNull();
      expect(replayed.status()).toBe(200);
      expect(replayed.headers()['content-type']).toBe(native.headers()['content-type']);
      expect(replayed.headers()['etag']).toBe(native.headers()['etag']);
      expect(replayed.headers()['x-request-id'], 'another exchange’s request id must not be replayed').toBeUndefined();
      expect((await replayed.body()).equals(await native.body())).toBe(true);
    } finally {
      await first.close();
      await second.close();
    }
  });

  test('pages, APIs, non-GET requests and failures always reach the server', async ({ browser, baseURL }) => {
    const missing = coldPath('/static/js/replay-missing-probe.js', 'p');
    const posted = coldPath('/static/js/app.js', 'post-probe');
    const context = await replayContext(browser, baseURL!);
    try {
      const page = await context.newPage();
      for (let attempt = 0; attempt < 2; attempt++) {
        const navigation = await page.goto(ROUTES.HOME);
        expect(await navigation!.serverAddr(), 'HTML pages are never replayed').not.toBeNull();

        const api = await fetchInPage(page, '/get_all_exercises');
        expect(await api.serverAddr(), 'APIs are never replayed').not.toBeNull();

        const notFound = await fetchInPage(page, missing);
        expect(notFound.status()).toBe(404);
        expect(await notFound.serverAddr(), 'a 404 is never replayed').not.toBeNull();

        const post = await fetchInPage(page, posted, 'POST');
        expect(post.status()).toBe(405);
        expect(await post.serverAddr(), 'non-GET requests are never replayed').not.toBeNull();
      }
      await staticRecordingsSettled();
      expect(isStaticAssetRecorded(new URL(missing, baseURL).href)).toBe(false);
      expect(isStaticAssetRecorded(new URL(posted, baseURL).href)).toBe(false);
    } finally {
      await context.close();
    }
  });

  test('a conditional request is never recorded and never answered from a recording', async ({ browser, baseURL }) => {
    const path = coldPath('/static/js/app.js', 'conditional-probe');
    const context = await replayContext(browser, baseURL!);
    try {
      const page = await context.newPage();
      await page.goto(ROUTES.HOME);
      // Learn the validator without recording anything under `path`.
      const probe = await fetchInPage(page, coldPath('/static/js/app.js', 'etag-source'));
      const etag = probe.headers()['etag'];
      expect(etag).toBeTruthy();

      const notModified = await fetchInPage(page, path, 'GET', { 'If-None-Match': etag });
      expect(notModified.status()).toBe(304);
      await staticRecordingsSettled();
      expect(isStaticAssetRecorded(notModified.url())).toBe(false);

      const full = await fetchInPage(page, path);
      expect(full.status(), 'a later plain GET must get the full body').toBe(200);
      expect(await full.serverAddr()).not.toBeNull();
      await expect.poll(() => isStaticAssetRecorded(full.url())).toBe(true);

      const revalidated = await fetchInPage(page, path, 'GET', { 'If-None-Match': etag });
      expect(revalidated.status(), 'a recorded 200 must not answer a conditional request').toBe(304);
      expect(await revalidated.serverAddr()).not.toBeNull();
    } finally {
      await context.close();
    }
  });

  test('a Range request is never recorded and never answered from a recording', async ({ browser, baseURL }) => {
    const partialFirst = coldPath('/static/js/app.js', 'range-probe');
    const fullFirst = coldPath('/static/js/app.js', 'range-after-full');
    const range = { Range: 'bytes=0-9' };
    const context = await replayContext(browser, baseURL!);
    try {
      const page = await context.newPage();
      await page.goto(ROUTES.HOME);

      // A 206 carries Flask's validators; the Range bypass is what keeps it out.
      const partial = await fetchInPage(page, partialFirst, 'GET', range);
      expect(partial.status()).toBe(206);
      await staticRecordingsSettled();
      expect(isStaticAssetRecorded(partial.url())).toBe(false);

      const full = await fetchInPage(page, fullFirst);
      await expect.poll(() => isStaticAssetRecorded(full.url())).toBe(true);
      const afterRecording = await fetchInPage(page, fullFirst, 'GET', range);
      expect(afterRecording.status(), 'a recorded 200 must not answer a Range request').toBe(206);
      expect(await afterRecording.serverAddr()).not.toBeNull();
    } finally {
      await context.close();
    }
  });

  test("a spec's own route mock wins and is never recorded", async ({ browser, baseURL }) => {
    const path = coldPath('/static/js/app.js', 'mock-probe');
    const mocked = await replayContext(browser, baseURL!);
    const clean = await replayContext(browser, baseURL!);
    try {
      const mockedPage = await mocked.newPage();
      await mockedPage.route((url) => url.href.endsWith(path), (route) =>
        route.fulfill({
          status: 200,
          contentType: 'text/javascript',
          headers: { etag: '"mock"', 'last-modified': 'Thu, 01 Jan 2026 00:00:00 GMT' },
          body: '// mocked by the spec',
        }),
      );
      await mockedPage.goto(ROUTES.HOME);
      const fromMock = await fetchInPage(mockedPage, path);
      expect(await fromMock.text()).toBe('// mocked by the spec');
      await staticRecordingsSettled();
      expect(isStaticAssetRecorded(fromMock.url())).toBe(false);

      const cleanPage = await clean.newPage();
      await cleanPage.goto(ROUTES.HOME);
      const fromServer = await fetchInPage(cleanPage, path);
      expect(await fromServer.serverAddr(), 'the mock must not leak into another context').not.toBeNull();
      expect(await fromServer.text()).not.toBe('// mocked by the spec');
    } finally {
      await mocked.close();
      await clean.close();
    }
  });
});

// The native-network selection the replay mitigation must not hide: real
// delivery, the source-run cache headers, revalidation (routing disables the
// HTTP cache, so this is only observable without replay) and failure handling.
test.describe('Native static delivery (replay disabled)', () => {
  test.use({
    staticReplay: false,
    consoleAllowlist: {
      expected: [
        {
          match: 'Failed to load resource: the server responded with a status of 404 (NOT FOUND)',
          reason: 'Chromium reports the deliberately missing /static/ probe asset',
        },
      ],
    },
  });

  function collectStatic(page: Page, baseURL: string): Response[] {
    const responses: Response[] = [];
    page.on('response', (response) => {
      const url = new URL(response.url());
      if (url.origin === new URL(baseURL).origin && url.pathname.startsWith('/static/')) {
        responses.push(response);
      }
    });
    return responses;
  }

  test('a page load fetches every asset from the server with its type and validators', async ({ page, baseURL }) => {
    const responses = collectStatic(page, baseURL!);
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    // The routine cascade is populated by the page's modules, so it only works
    // when they were all delivered.
    await page.locator(SELECTORS.ROUTINE_ENV).selectOption('GYM');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-program') as HTMLSelectElement | null;
      return !!select && select.options.length > 1;
    });

    // Only the first response per URL: Blink may serve a repeat reference to
    // the same asset from its memory cache, which has no server address.
    const firstPerUrl = [...new Map(responses.reverse().map((r) => [r.url(), r])).values()];
    expect(firstPerUrl.length).toBeGreaterThan(20);
    for (const response of firstPerUrl) {
      const label = new URL(response.url()).pathname;
      expect(await response.serverAddr(), `${label} must come from the server`).not.toBeNull();
      expect(response.status(), label).toBe(200);
      const headers = response.headers();
      expect(headers['cache-control'], label).toBe('no-cache, must-revalidate');
      expect(headers['etag'], label).toBeTruthy();
      expect(headers['last-modified'], label).toBeTruthy();
      if (label.endsWith('.js')) expect(headers['content-type'], label).toMatch(/javascript/);
      if (label.endsWith('.css')) expect(headers['content-type'], label).toMatch(/^text\/css/);
    }
  });

  test('a second navigation revalidates static assets with 304', async ({ page, baseURL }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const responses = collectStatic(page, baseURL!);
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const revalidated = responses.filter((response) => response.status() === 304);
    expect(revalidated.length, 'no-cache assets must be revalidated, not re-sent').toBeGreaterThan(0);
    for (const response of revalidated) {
      expect(await response.request().headerValue('if-none-match')).toBe(response.headers()['etag']);
    }
  });

  test('a missing asset fails on every request', async ({ page }) => {
    const missing = coldPath('/static/js/native-missing-probe.js', 'p');
    await page.goto(ROUTES.HOME);
    for (let attempt = 0; attempt < 2; attempt++) {
      const response = await fetchInPage(page, missing);
      expect(response.status()).toBe(404);
      expect(await response.serverAddr()).not.toBeNull();
    }
  });
});
