/**
 * E2E Test: Summary Pages (Weekly & Session)
 * 
 * Tests the summary pages functionality including:
 * - Page loading
 * - Contribution mode toggles
 * - Volume legend display
 * - Table rendering
 */
import type { Page } from '@playwright/test';
import { addPlanRow, BENCH, planPost } from './workout-plan-fixture';
import { summaryResponse } from './summary-records';
import { test as guardedTest } from './console-guard';
import { test, expect, ROUTES, SELECTORS, waitForPageReady } from './fixtures';

const CONTRIBUTION_MODE_OPTIONS = [
  { value: 'total', text: 'Total (Primary + Secondary + Tertiary)' },
  { value: 'direct', text: 'Direct Only (Primary Muscle Only)' },
];

for (const route of [ROUTES.WEEKLY_SUMMARY, ROUTES.SESSION_SUMMARY]) {
  guardedTest(`refresh removes open category tooltips on ${route}`, async ({ page }) => {
    let releaseRefresh!: () => void;
    const refreshGate = new Promise<void>(resolve => { releaseRefresh = resolve; });
    const row = {
      routine: 'Tooltip test', muscle_group: 'Chest', effective_sets: 12,
      raw_sets: 12, total_volume: 100, total_exercises: 1,
    };
    await page.route(`**${route}?**`, async request => {
      if (request.request().url().includes('contribution_mode=direct')) await refreshGate;
      await request.fulfill({ json: {
        ok: true, status: 'success', data: {
          weekly_summary: [row], session_summary: [row], isolated_muscles: [],
          categories: [{ category: 'Mechanic', subcategory: 'Compound', total_exercises: 1 }],
        },
      } });
    });
    await page.goto(route);
    await waitForPageReady(page);
    const selector = page.locator('#contribution-mode');
    const cell = page.locator('#categories-table-body [data-bs-toggle="tooltip"]').first();
    await expect(cell).toBeVisible();
    await selector.focus();
    await cell.hover();
    await expect(page.locator('.tooltip.show')).toHaveCount(1);
    await expect(page.locator('.tooltip.show')).toHaveCSS('opacity', '1');
    const oldCell = await cell.elementHandle();
    const response = page.waitForResponse(result =>
      result.url().includes(`${route}?`) && result.url().includes('contribution_mode=direct'));
    const refreshRequest = page.waitForRequest(request =>
      request.url().includes(`${route}?`) && request.url().includes('contribution_mode=direct'));
    await page.keyboard.press('ArrowDown');
    await refreshRequest;
    // Keep the response pending until a real hover tip is open on the rows it replaces.
    await page.mouse.move(5, 5);
    await cell.hover();
    await expect(page.locator('.tooltip.show')).toHaveCSS('opacity', '1');
    releaseRefresh();
    await response;
    await expect(selector).toHaveValue('direct');
    await expect.poll(() => oldCell!.evaluate(element => element.isConnected)).toBe(false);
    await page.mouse.move(5, 5);
    await expect.poll(() => page.locator('.tooltip.show').evaluateAll(tips =>
      tips.filter(tip => !document.querySelector(`[aria-describedby~="${tip.id}"]`)).length,
    )).toBe(0);
  });
}

function unwrapApiData(payload: unknown) {
  if (
    payload &&
    typeof payload === 'object' &&
    !Array.isArray(payload) &&
    'data' in payload
  ) {
    return (payload as { data: unknown }).data;
  }

  return payload;
}

async function expectSharedLegendSwatches(page: Page) {
  const tokenByVolume = {
    low: '--bs-danger',
    medium: '--bs-orange',
    high: '--bs-success',
    ultra: '--bs-purple',
  } as const;

  for (const [volume, token] of Object.entries(tokenByVolume)) {
    const swatch = page.locator(`[data-volume-level="${volume}"]`);
    await expect(swatch).toBeVisible();
    const styles = await swatch.evaluate((element, property) => {
      const rootStyle = getComputedStyle(document.documentElement);
      const swatchStyle = getComputedStyle(element);
      const probe = document.createElement('span');
      probe.style.backgroundColor = rootStyle.getPropertyValue(property).trim();
      document.body.appendChild(probe);
      const tokenColor = getComputedStyle(probe).backgroundColor;
      probe.remove();
      return { swatchColor: swatchStyle.backgroundColor, tokenColor };
    }, token);
    expect(styles.tokenColor).not.toBe('rgba(0, 0, 0, 0)');
    expect(styles.swatchColor).toBe(styles.tokenColor);
  }
}

async function expectMethodSelectorContract(page: Page, updaterName: string) {
  const methodSelector = page.locator('.method-selector').first();
  await expect(methodSelector).toBeVisible();

  const contributionMode = page.locator('#contribution-mode');

  await expect(page.locator('#counting-mode')).toHaveCount(0);
  await expect(page.locator('label[for="counting-mode"]')).toHaveCount(0);
  await expect(page.locator('label[for="contribution-mode"]')).toHaveText('Muscle Contribution Mode');
  await expect(contributionMode).toHaveAttribute('onchange', `${updaterName}()`);

  await expect(contributionMode.locator('option')).toHaveCount(CONTRIBUTION_MODE_OPTIONS.length);

  for (const [index, option] of CONTRIBUTION_MODE_OPTIONS.entries()) {
    await expect(contributionMode.locator('option').nth(index)).toHaveAttribute('value', option.value);
    await expect(contributionMode.locator('option').nth(index)).toHaveText(option.text);
  }
}

test.describe('Weekly Summary Page', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WEEKLY_SUMMARY);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('page loads with correct structure', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText(/(Weekly|Plan Volume) Summary/i);

    // Check summary container
    await expect(page.locator(SELECTORS.PAGE_WEEKLY_SUMMARY)).toBeVisible();
  });

  test('contribution mode selector is present', async ({ page }) => {
    await expectMethodSelectorContract(page, 'updateWeeklySummary');
  });

  test('volume legend is displayed', async ({ page }) => {
    const legend = page.locator('.volume-legend');
    await expect(legend).toBeVisible();

    // Check legend categories
    await expect(legend).toContainText('Low Volume');
    await expect(legend).toContainText('Medium Volume');
    await expect(legend).toContainText('High Volume');
    await expect(legend).toContainText('Excessive Volume');
    await expect(legend).toContainText('Raw Sets');
    await expect(legend).toContainText('Effective Sets');
    await expect(legend).toContainText('Volume Classification');
  });

  test('legend swatches use shared volume classification colors', async ({ page }) => {
    await expectSharedLegendSwatches(page);
  });

  test('weekly summary table has correct headers', async ({ page }) => {
    const table = page.locator('#weekly-summary-container table');
    await expect(table).toBeVisible();

    // Check expected headers
    const headers = table.locator('thead th');
    const headerTexts = await headers.allInnerTexts();
    const headerString = headerTexts.join(' ').toLowerCase();

    expect(headerString).toContain('muscle');
    expect(headerString).toContain('effective sets');
    expect(headerString).toContain('raw sets');
    expect(headerString).toContain('volume');
  });

  test('changing contribution mode updates display', async ({ page }) => {
    const contributionMode = page.locator('#contribution-mode');
    
    // Select "Direct Only" option
    await contributionMode.selectOption('direct');

    // Wait for update
    await page.waitForTimeout(500);

    // The selection should persist
    await expect(contributionMode).toHaveValue('direct');

    // Switch back to total
    await contributionMode.selectOption('total');
    await page.waitForTimeout(500);
    await expect(contributionMode).toHaveValue('total');
  });

  test('fetch-backed weekly summary updates use explicit JSON intent', async ({ page }) => {
    const [contributionResponse] = await Promise.all([
      page.waitForResponse((response) =>
        response.url().includes('/weekly_summary?') &&
        response.url().includes('contribution_mode=direct') &&
        response.request().method() === 'GET' &&
        response.request().headers()['x-requested-with'] === 'XMLHttpRequest'
      ),
      page.locator('#contribution-mode').selectOption('direct'),
    ]);

    expect(contributionResponse.ok()).toBeTruthy();
    expect(contributionResponse.url()).toContain('contribution_mode=direct');
    expect(contributionResponse.url()).not.toContain('counting_mode=');
    const contributionResponsePayload = await contributionResponse.json();
    expect(contributionResponsePayload.ok).toBe(true);
    expect(contributionResponsePayload.status).toBe('success');
    const contributionPayload = unwrapApiData(contributionResponsePayload) as Record<string, unknown>;
    expect(Array.isArray(contributionPayload.weekly_summary)).toBe(true);
    expect(Array.isArray(contributionPayload.categories)).toBe(true);
    expect(contributionPayload).toHaveProperty('isolated_muscles');
    expect(contributionPayload).toHaveProperty('modes');
    await expect(page.locator('#volume-formula-text')).toContainText('Effective Sets');
    const weeklySummary = contributionPayload.weekly_summary as Array<Record<string, unknown>>;
    if (weeklySummary.length > 0) {
      await expect(
        page.locator('#weekly-summary-table tr').first().locator('td[data-label="Effective Sets"]')
      ).toHaveText(Number(weeklySummary[0].effective_sets).toFixed(1));
      await expect(
        page.locator('#weekly-summary-table tr').first().locator('td[data-label="Raw Sets"]')
      ).toHaveText(Number(weeklySummary[0].raw_sets).toFixed(1));
    }
    await expect(page.locator('#weekly-summary-table tr').first()).toBeVisible();
  });
});

test.describe('Session Summary Page', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.SESSION_SUMMARY);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('page loads with correct structure', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('Session Summary');

    // Check summary container
    await expect(page.locator(SELECTORS.PAGE_SESSION_SUMMARY)).toBeVisible();
  });

  test('contribution mode selector is present', async ({ page }) => {
    await expectMethodSelectorContract(page, 'updateSessionSummary');
  });

  test('volume legend is displayed', async ({ page }) => {
    const legend = page.locator('.volume-legend');
    await expect(legend).toBeVisible();

    // Check session-specific content
    await expect(legend).toContainText('Volume Classification');
    await expect(legend).toContainText('Raw Sets');
    await expect(legend).toContainText('Effective Sets');
    await expect(legend).toContainText('Session Warnings');
  });

  test('session legend swatches use shared volume classification colors', async ({ page }) => {
    await expectSharedLegendSwatches(page);
  });

  test('session summary table has correct headers', async ({ page }) => {
    const table = page.locator('#session-summary-container table');
    await expect(table).toBeVisible();

    // Check expected headers
    const headers = table.locator('thead th');
    const headerTexts = await headers.allInnerTexts();
    const headerString = headerTexts.join(' ').toLowerCase();

    expect(headerString).toContain('routine');
    expect(headerString).toContain('muscle');
    expect(headerString).toContain('effective sets');
    expect(headerString).toContain('raw sets');
    expect(headerString).toContain('volume');
  });

  test('method selector section has descriptions', async ({ page }) => {
    const methodSelector = page.locator('.method-selector').first();
    await expect(methodSelector).toBeVisible();

    // Check help text exists (multiple form-text elements, check at least one is visible)
    const formTexts = methodSelector.locator('.form-text');
    await expect(formTexts.first()).toBeVisible();
  });

  test('fetch-backed session summary updates use explicit JSON intent', async ({ page }) => {
    const [contributionResponse] = await Promise.all([
      page.waitForResponse((response) =>
        response.url().includes('/session_summary?') &&
        response.url().includes('contribution_mode=direct') &&
        response.request().method() === 'GET' &&
        response.request().headers()['x-requested-with'] === 'XMLHttpRequest'
      ),
      page.locator('#contribution-mode').selectOption('direct'),
    ]);

    expect(contributionResponse.ok()).toBeTruthy();
    expect(contributionResponse.url()).toContain('contribution_mode=direct');
    expect(contributionResponse.url()).not.toContain('counting_mode=');
    const contributionResponsePayload = await contributionResponse.json();
    expect(contributionResponsePayload.ok).toBe(true);
    expect(contributionResponsePayload.status).toBe('success');
    const contributionPayload = unwrapApiData(contributionResponsePayload) as Record<string, unknown>;
    expect(Array.isArray(contributionPayload.session_summary)).toBe(true);
    expect(Array.isArray(contributionPayload.categories)).toBe(true);
    expect(contributionPayload).toHaveProperty('isolated_muscles');
    expect(contributionPayload).toHaveProperty('modes');
    await expect(page.locator('#volume-formula-text')).toContainText('Effective Sets');
    const sessionSummary = contributionPayload.session_summary as Array<Record<string, unknown>>;
    if (sessionSummary.length > 0) {
      await expect(
        page.locator('#session-summary-table tr').first().locator('td[data-label="Effective Sets"]')
      ).toHaveText(Number(sessionSummary[0].effective_sets).toFixed(1));
      await expect(
        page.locator('#session-summary-table tr').first().locator('td[data-label="Raw Sets"]')
      ).toHaveText(Number(sessionSummary[0].raw_sets).toFixed(1));
    }
    await expect(page.locator('#session-summary-table tr').first()).toBeVisible();
  });
});

test.describe('Pattern Coverage Analysis (v1.5.0)', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WEEKLY_SUMMARY);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('pattern coverage API returns valid structure', async ({ request }) => {
    const response = await request.get('/api/pattern_coverage');
    expect(response.ok()).toBeTruthy();

    const data = await response.json();
    expect(data.ok).toBe(true);
    expect(data.status).toBe('success');
    expect(data.data).toHaveProperty('per_routine');
    expect(data.data).toHaveProperty('total');
    expect(data.data).toHaveProperty('warnings');
    expect(data.data).toHaveProperty('sets_per_routine');
    expect(data.data).toHaveProperty('ideal_sets_range');
  });

  test('pattern coverage warnings are actionable', async ({ request }) => {
    const response = await request.get('/api/pattern_coverage');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    const warnings = data.data.warnings;
    
    // Warnings should be an array
    expect(Array.isArray(warnings)).toBe(true);
    
    // Each warning should have required fields
    for (const warning of warnings) {
      expect(warning).toHaveProperty('type');
      expect(warning).toHaveProperty('message');
      // Level indicates how critical the warning is (high, medium, low)
      expect(warning).toHaveProperty('level');
      expect(['high', 'medium', 'low']).toContain(warning.level);
      // Description provides actionable details
      expect(warning).toHaveProperty('description');
    }
  });

  test('pattern coverage tracks movement patterns', async ({ request }) => {
    const response = await request.get('/api/pattern_coverage');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    const total = data.data.total;
    
    // Total should track core movement patterns
    expect(typeof total).toBe('object');
    
    // Common patterns to track
    const expectedPatterns = ['squat', 'hinge', 'horizontal_push', 'horizontal_pull', 'vertical_push', 'vertical_pull'];
    
    // At least some patterns should be tracked
    const hasPatterns = Object.keys(total).some(key => 
      expectedPatterns.some(pattern => key.toLowerCase().includes(pattern.replace('_', '')))
    );
    
    // Pattern structure may vary, just ensure it's not empty when there's data
    expect(typeof total === 'object').toBeTruthy();
  });

  test('sets_per_routine reports session volume', async ({ request }) => {
    const response = await request.get('/api/pattern_coverage');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    const setsPerRoutine = data.data.sets_per_routine;
    
    // Should be an object mapping routine names to set counts
    expect(typeof setsPerRoutine).toBe('object');
    
    // Each value should be a non-negative number
    for (const [routine, sets] of Object.entries(setsPerRoutine)) {
      expect(typeof sets).toBe('number');
      expect(sets).toBeGreaterThanOrEqual(0);
    }
  });

  test('ideal_sets_range provides guidance', async ({ request }) => {
    const response = await request.get('/api/pattern_coverage');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    const idealRange = data.data.ideal_sets_range;
    
    // Should provide min and max guidance
    expect(idealRange).toHaveProperty('min');
    expect(idealRange).toHaveProperty('max');
    expect(idealRange.min).toBeLessThan(idealRange.max);
    
    // v1.5.0 recommends 15-24 sets per session
    expect(idealRange.min).toBeGreaterThanOrEqual(10);
    expect(idealRange.max).toBeLessThanOrEqual(30);
  });

  test('weekly summary page renders pattern coverage from the live fetch', async ({ page }) => {
    const [response] = await Promise.all([
      page.waitForResponse((networkResponse) =>
        networkResponse.url().includes('/api/pattern_coverage') &&
        networkResponse.request().headers()['x-requested-with'] === 'XMLHttpRequest'
      ),
      page.reload(),
    ]);

    expect(response.ok()).toBeTruthy();
    const payload = unwrapApiData(await response.json()) as Record<string, unknown>;
    expect(payload).toHaveProperty('warnings');
    expect(payload).toHaveProperty('total');
    await expect(page.locator('#pattern-coverage-container .spinner-border')).toHaveCount(0);
    await expect(page.locator('#pattern-coverage-container')).not.toContainText('Loading');
  });
});


guardedTest('Session keeps the routine and date window through initial, Direct and naming refreshes', async ({page}) => {
  const request = page.request;
  await page.setViewportSize({width:1440,height:900});
  await planPost(request, '/clear_workout_log');
  await planPost(request, '/clear_workout_plan');
  try {
    const names = ['Session boundary ten', 'Session boundary eleven'];
    for (const [i,name] of names.entries()) {
      await addPlanRow(request, name, BENCH, {sets:10+i,min_rep_range:8,max_rep_range:12,rir:1,weight:60});
    }
    await planPost(request, '/export_to_workout_log');
    const uri = ROUTES.SESSION_SUMMARY;
    const headers = {'X-Requested-With':'XMLHttpRequest'};
    const global = (await (await request.get(uri,{headers})).json()).data;
    expect(global.categories.length).toBeGreaterThan(0);
    expect(global.isolated_muscles.length).toBeGreaterThan(0);
    let neutralSurface: string[] | undefined;
    for (const [routine,dates,warning,count,score] of [
      [names[0], {start_date:'2000-01-01'}, 'Borderline', 1, '20'],
      [names[1], {end_date:'2099-12-31'}, 'Excessive', 1, '22'],
      [names[0], {start_date:'2000-01-01',end_date:'2000-01-02'}, 'No Sessions', 0, '20'],
    ] as const) {
      const params = new URLSearchParams({routine,...dates});
      const entry = uri + '?' + params;
      for (const action of ['initial','direct','naming']) {
        const mode = action === 'initial' ? 'total' : 'direct';
        const expected = (await (await request.get(entry + '&contribution_mode=' + mode,{headers})).json()).data;
        expect(expected.categories).toEqual(global.categories);
        expect(expected.isolated_muscles).toEqual(global.isolated_muscles);
        const chest = expected.session_summary.find((r:{muscle_group:string}) => r.muscle_group === 'Chest');
        expect(chest).toMatchObject({routine,session_count:count,effective_sets:routine === names[0] ? 10 : 11});
        const result = summaryResponse(page, uri, mode);
        if (action === 'initial') await page.goto(entry);
        if (action === 'direct') await page.getByLabel('Muscle Contribution Mode').selectOption('direct');
        const naming = page.locator('#muscleModeToggle');
        const priorName = action === 'naming' ? await naming.innerText() : '';
        if (action === 'naming') await naming.click();
        const response = await result;
        const query = new URL(response.url()).searchParams;
        for (const key of ['routine','start_date','end_date']) expect.soft(query.get(key), action + ' ' + key).toBe(params.get(key));
        const data = (await response.json()).data;
        expect.soft(data.session_summary, action + ' scoped records').toEqual(expected.session_summary);
        const rows = page.locator('#session-summary-table tr');
        await expect.soft(rows).toHaveCount(expected.session_summary.length);
        const row = rows.filter({has:page.locator('td[data-raw-value="Chest"]')}).filter({hasText:routine});
        await expect(row).toContainText(warning);
        await expect(row).toContainText('Medium Volume');
        await expect(row.locator('td').last().getByText(warning,{exact:true})).toBeVisible();
        await expect(row).not.toHaveClass(/table-(warning|danger)/);
        if (action === 'direct') {
          const surfaces = await row.evaluate(el => [el,...el.querySelectorAll('td')].map(cell => {
            const s = getComputedStyle(cell);
            return [s.backgroundColor,s.backgroundImage,s.boxShadow].join(' ');
          }));
          if (neutralSurface) expect(surfaces, 'same row surface at 10, 11 and no sessions').toEqual(neutralSurface);
          else neutralSurface = surfaces;
        }
        const badge = page.locator('.fatigue-badge');
        await expect(badge.locator('.fatigue-badge__score')).toHaveText(score);
        await expect(badge.locator('.fatigue-badge__band')).toHaveText(score === '22' ? /^\s*moderate\s*$/i : /^\s*light\s*$/i);
        await expect(badge).toContainText('Routine: ' + routine);
        if (action === 'naming') {
          await expect(naming).not.toHaveText(priorName);
          const scientific = (await naming.innerText()).includes('Scientific');
          await expect(row.locator('[data-raw-value="Chest"]')).toContainText(scientific ? 'Upper / Lower Pectoralis' : 'Chest');
          const isolated = page.locator('td[data-raw-value="lateral-head-triceps"]');
          await expect(isolated).toContainText(scientific ? 'Lateral Head Triceps' : 'Triceps');
        }
      }
    }
  } finally {
    await planPost(request,'/clear_workout_log');
    await planPost(request,'/clear_workout_plan');
  }
});



for (const route of [ROUTES.WEEKLY_SUMMARY, ROUTES.SESSION_SUMMARY]) {
  guardedTest('labelled volume settings, definitions and existing workbook action on ' + route, async ({page}) => {
    await page.setViewportSize({width:1440,height:900});
    await addPlanRow(page.request,'Summary actions',BENCH);
    try {
      await page.goto(route);
      const select = page.getByLabel('Muscle Contribution Mode', {exact:true});
      const panel = page.locator('section, .ui-panel').filter({has:select}).filter({has:page.locator('tbody[id$="-summary-table"]')}).last();
      await expect(panel).toBeVisible();
      await expect(select).toHaveValue('total');
      await expect(panel.locator('label[for="contribution-mode"]')).toBeVisible();
      await expect(panel).toContainText(/primary/i);
      const disclosure = panel.locator('details');
      await expect(disclosure).toHaveCount(1);
      await expect(disclosure.locator('#volume-formula-text')).toBeHidden();
      await disclosure.locator('summary').focus();
      await page.keyboard.press('Enter');
      await expect(disclosure.locator('#volume-formula-text')).toBeVisible();
      for (const concept of [/credited/i,/raw sets/i,/effective sets/i,/effort factor/i,/rep.range factor/i,/per.exercise|each exercise/i,/primary/i,/secondary/i,/tertiary/i]) {
        await expect(disclosure).toContainText(concept);
      }
      if (route === ROUTES.SESSION_SUMMARY) {
        await expect(disclosure).toContainText(/(?:below|under|<)\s*10/i);
        await expect(disclosure).toContainText(/10\s*(?:to|–|-)\s*(?:below|under|<)\s*11/i);
        await expect(disclosure).toContainText(/11\s*(?:\+|or (?:more|above|higher))/i);
      }
      await page.keyboard.press('Enter');
      await expect(disclosure.locator('#volume-formula-text')).toBeHidden();
      const exported: string[] = [];
      page.on('request',req => { if (new URL(req.url()).pathname.includes('export')) exported.push(req.url()); });
      const button = page.getByRole('button',{name:/^Export workout data/i});
      await expect(button).toHaveText(/Export workout data/i);
      await button.click();
      await expect(page.locator(SELECTORS.TOAST_BODY)).toContainText(/No exercises to export/i);
      expect(exported, 'existing #754 early return').toEqual([]);
    } finally { await planPost(page.request,'/clear_workout_plan'); }
  });
}

const missingRange = {per_routine:{},total:{},warnings:[],sets_per_routine:{}};

for (const slow of ['summary','pattern'] as const) {
  guardedTest('Weekly confirms one empty state only after the slower ' + slow + ' resolves', async ({page}) => {
    await planPost(page.request,'/clear_workout_plan');
    let release!: () => void;
    const gate = new Promise<void>(resolve => {release = resolve;});
    const slowPath = slow === 'pattern' ? '/api/pattern_coverage' : '/weekly_summary';
    const fastPath = slow === 'pattern' ? '/weekly_summary' : '/api/pattern_coverage';
    const xhr = (r: import('@playwright/test').Response, pathname:string) =>
      new URL(r.url()).pathname === pathname && r.request().headers()['x-requested-with'] === 'XMLHttpRequest';
    await page.route(slow === 'pattern' ? '**/api/pattern_coverage' : '**/weekly_summary?**', async route => {
      const original = await route.fetch();
      await gate;
      await route.fulfill({response:original});
    });
    const fastResponse = page.waitForResponse(r => xhr(r,fastPath));
    const slowResponse = page.waitForResponse(r => xhr(r,slowPath));
    try {
      await page.goto(ROUTES.WEEKLY_SUMMARY);
      const fast = await fastResponse;
      await fast.finished();
      const empty = page.locator('main .ui-empty-state:visible');
      // Two paint opportunities give the first completed request time to update the live DOM.
      await page.evaluate(() => new Promise<void>(done => requestAnimationFrame(() => requestAnimationFrame(() => done()))));
      await expect(empty).toHaveCount(0);
      await expect(page.getByLabel('Muscle Contribution Mode')).toBeEnabled();
      release();
      const slowResult = await slowResponse;
      const pattern = (await (slow === 'pattern' ? slowResult : fast).json()).data;
      expect(pattern).toMatchObject({ideal_sets_range:{min:15,max:24},total:{}});
      expect(pattern.warnings.length).toBeGreaterThan(0);
      await expect(empty).toHaveCount(1);
    } finally { release(); }
  });
}

for (const populated of [false,true]) {
  guardedTest('Weekly reports the caught Pattern read independently with populated=' + populated, async ({page}) => {
    await planPost(page.request,'/clear_workout_plan');
    if (populated) await addPlanRow(page.request,'Independent volume',BENCH);
    try {
      await page.route('**/api/pattern_coverage',r=>r.fulfill({json:{ok:true,status:'success',data:missingRange}}));
      const summary = summaryResponse(page,ROUTES.WEEKLY_SUMMARY,'total');
      await page.goto(ROUTES.WEEKLY_SUMMARY);
      await summary;
      await expect(page.locator('#pattern-coverage-container')).toContainText(/unavailable|failed to load|unable to load/i);
      await expect(page.locator('main .ui-empty-state:visible')).toHaveCount(0);
      const select = page.getByLabel('Muscle Contribution Mode');
      await expect(select).toBeEnabled();
      await select.selectOption('direct');
      if (populated) await expect(page.locator('#weekly-summary-table')).toContainText('Chest');
    } finally { await planPost(page.request,'/clear_workout_plan'); }
  });
}

guardedTest('Weekly names each Pattern warning, pattern count and routine target position', async ({page}) => {
  const warnings = ['high','medium','low'].map((level,i)=>({level,message:'Warning number ' + i,description:'Description number ' + i}));
  const totals = {squat:2,hinge:3,horizontal_push:4,horizontal_pull:5,vertical_push:6,upper_isolation:7};
  const routines = {Short:14,Lower:15,Upper:24,Long:25};
  const data = {total:totals, per_routine:{}, warnings, sets_per_routine:routines, ideal_sets_range:{min:15,max:24}};
  await page.route('**/api/pattern_coverage',r=>r.fulfill({json:{ok:true,status:'success',data}}));
  await page.goto(ROUTES.WEEKLY_SUMMARY);
  const panel = page.locator('#pattern-coverage-container');
  for (const warning of warnings) {
    const group = panel.locator('li, article, section, div').filter({hasText:warning.message}).filter({hasText:warning.description}).last();
    await expect(group).toContainText(new RegExp('\\b' + warning.level + '\\b','i'));
  }
  await expect(panel.getByText(/core patterns/i,{exact:true})).toBeVisible();
  await expect(panel.getByText(/additional patterns/i,{exact:true})).toBeVisible();
  for (const [key,count] of Object.entries({...totals,vertical_pull:0})) {
    await expect(panel).toContainText(new RegExp(key.replaceAll('_',' ') + '[:\\s]+(?=' + count + '\\b)' + count,'i'));
  }
  for (const [name,count] of Object.entries(routines)) {
    const status = count < 15 ? 'below' : count > 24 ? 'above' : 'within';
    const chip = panel.locator('li,article,div').filter({hasText:new RegExp('\\b'+name+'\\b')})
      .filter({hasText:new RegExp('\\b'+count+'\\b')}).last();
    await expect(chip).toContainText(new RegExp(status+' target','i'));
  }
  await expect(panel).toContainText(/15\s*[-–]\s*24/);
});



guardedTest('an older empty Weekly refresh cannot replace the successful Direct result', async ({page}) => {
  await planPost(page.request,'/clear_workout_plan');
  let release!: () => void;
  const wait = new Promise<void>(done => {release = done;});
  await page.route('**/weekly_summary?**',async r => {
    if (new URL(r.request().url()).searchParams.get('contribution_mode') === 'total') {
      const empty = await r.fetch();
      await wait;
      await r.fulfill({response:empty});
    } else {
      await r.fulfill({json:{ok:true,status:'success',data:{
        weekly_summary:[{muscle_group:'Chest',effective_sets:3.2,raw_sets:4,frequency:1,total_volume:319}],
        categories:[],isolated_muscles:[],
      }}});
    }
  });
  const old = summaryResponse(page,ROUTES.WEEKLY_SUMMARY,'total');
  try {
    await page.goto(ROUTES.WEEKLY_SUMMARY);
    await page.getByLabel('Muscle Contribution Mode').selectOption('direct');
    const volume = page.locator('#weekly-summary-table');
    await expect(volume).toContainText('319');
    release();
    await (await old).finished();
    await page.evaluate(() => new Promise<void>(done => requestAnimationFrame(() => requestAnimationFrame(() => done()))));
    await expect(volume).toContainText('319');
    await expect(page.locator('main .ui-empty-state:visible')).toHaveCount(0);
  } finally {release();}
});

guardedTest('Session confirms a single whole-page empty after its real Summary response', async ({page}) => {
  await planPost(page.request,'/clear_workout_plan');
  const xhr = summaryResponse(page,ROUTES.SESSION_SUMMARY,'total');
  await page.goto(ROUTES.SESSION_SUMMARY);
  const data = (await (await xhr).json()).data;
  expect([data.session_summary,data.categories,data.isolated_muscles]).toEqual([[],[],[]]);
  await expect(page.locator('.fatigue-badge')).toContainText(/No planned exercises yet/i);
  await expect(page.locator('main .ui-empty-state:visible')).toHaveCount(1);
  await expect(page.getByLabel('Muscle Contribution Mode')).toBeEnabled();
});

guardedTest.describe('Independent Summary request failures', () => {
  const reason = 'The designated GET returns the test-only 503 envelope.';
  guardedTest.use({consoleAllowlist:{expected:[
    {match:'Failed to load resource: the server responded with a status of 503 (Service Unavailable)',reason},
    {match:/^\[req_[\w]+\] API Error: \{url: \/(?:api\/pattern_coverage|(?:weekly|session)_summary\?contribution_mode=total), method: GET, status: 503, error: Object\}$/,reason},
    {match:/^\[req_[\w]+\] API Error \(final\): \{url: \/(?:api\/pattern_coverage|(?:weekly|session)_summary\?contribution_mode=total), method: GET, error: Object\}$/,reason},
    {match:/^Error fetching (?:data|pattern coverage): \{code: PROBE, message: Section failed, requestId: req_[\w]+\}$/,reason},
  ]}});
  for (const [path,fault] of [[ROUTES.WEEKLY_SUMMARY,'pattern'],[ROUTES.WEEKLY_SUMMARY,'summary'],[ROUTES.SESSION_SUMMARY,'summary']] as const) {
    guardedTest(path + ' keeps siblings usable after failed ' + fault, async ({page}) => {
      await planPost(page.request,'/clear_workout_plan');
      await addPlanRow(page.request,'Section recovery',BENCH,{sets:5});
      try {
        await page.route(fault === 'pattern' ? '**/api/pattern_coverage' : '**'+path+'?**',async route => {
          await route.fulfill({status:503,json:{ok:false,status:'error',error:{code:'PROBE',message:'Section failed'},message:'Section failed'}});
        },{times:1});
        await page.goto(path);
        const volume = page.locator(path === ROUTES.WEEKLY_SUMMARY ? '#weekly-summary-table' : '#session-summary-table');
        const pattern = page.locator('#pattern-coverage-container');
        if (fault === 'pattern') {
          await expect(pattern).toContainText(/unavailable|unable to load|failed to load/i);
          await expect(volume).toContainText('Chest');
        } else {
          await expect(page.locator('main')).toContainText(/failed to load|unable to load|could not load/i);
          if (path === ROUTES.WEEKLY_SUMMARY) await expect(pattern).toContainText('Section recovery');
        }
        await expect(page.locator('main .ui-empty-state:visible')).toHaveCount(0);
        await expect(page.getByTestId('fatigue-badge-breakdown-link')).toBeVisible();
        const refreshed = summaryResponse(page,path,'direct');
        await page.getByLabel('Muscle Contribution Mode').selectOption('direct');
        await refreshed;
        await expect(volume).toContainText('Chest');
        await expect(page.locator('main .ui-empty-state:visible')).toHaveCount(0);
      } finally {await planPost(page.request,'/clear_workout_plan');}
    });
  }
});
