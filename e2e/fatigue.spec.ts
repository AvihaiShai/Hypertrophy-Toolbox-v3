/**
 * Fatigue Meter — Phase 2 Stage 2 dedicated page (/fatigue) E2E.
 *
 * Covers the body heatmap panel, page load, period selector, per-muscle bar
 * rendering, SFR cards, empty-state copy, and dark-mode parity.
 *
 * Chromium only. The heatmap block runs first - see the note above it.
 */
import { test, expect } from './fixtures';
import { Page } from '@playwright/test';

const FATIGUE_URL = '/fatigue';

async function gotoFatigue(page: Page, period?: string): Promise<void> {
  const url = period ? `${FATIGUE_URL}?period=${period}` : FATIGUE_URL;
  await page.goto(url);
  await page.waitForSelector('[data-testid="fatigue-page"]', { state: 'visible' });
}

/**
 * Body heatmap.
 *
 * This block runs FIRST on purpose. The functional seed wipes plan and log
 * rows, so `/fatigue` is in its empty state and the panel does not exist at
 * all; every test here seeds its own plan. It also has to sit above the
 * `empty-state copy` test below, which POSTs /erase-data and would otherwise
 * leave the database wiped for everything after it in the file.
 */
const PLAN_ROW = {
  routine: 'GYM - Full Body - Workout A',
  sets: 3,
  min_rep_range: 8,
  max_rep_range: 12,
  rir: 2,
  weight: 100,
};

async function resetPlan(page: Page): Promise<void> {
  // Earlier specs in the shard may have left rows behind, so start from a known
  // state rather than inheriting one.
  await page.request.post('/erase-data', {
    data: { confirm: 'ERASE_ALL_DATA' },
    headers: { 'Content-Type': 'application/json' },
  });
}

async function seedExercise(page: Page, exercise: string): Promise<void> {
  const response = await page.request.post('/add_exercise', {
    data: { ...PLAN_ROW, exercise },
  });
  expect(response.ok()).toBeTruthy();
}

/**
 * Give the logged channel a reading in the current window.
 *
 * Exporting the plan alone is not enough: the accumulator only counts a logged
 * row once it carries scored values, so an unscored export leaves the logged
 * channel empty and the two-channel path untested.
 */
async function seedLoggedSession(page: Page): Promise<void> {
  const exported = await page.request.post('/export_to_workout_log');
  expect(exported.ok()).toBeTruthy();

  const listed = await page.request.get('/get_workout_logs');
  expect(listed.ok()).toBeTruthy();
  const logs = (await listed.json()).data ?? [];
  expect(logs.length).toBeGreaterThan(0);

  for (const log of logs) {
    const scored = await page.request.post('/update_workout_log', {
      data: {
        id: log.id,
        updates: { scored_min_reps: 8, scored_max_reps: 10, scored_rir: 1, scored_weight: 60 },
      },
    });
    expect(scored.ok()).toBeTruthy();
  }
}

async function gotoHeatmap(page: Page, period?: string): Promise<void> {
  await gotoFatigue(page, period);
  await page.waitForSelector('[data-heatmap-state="ready"]');
}

test.describe('/fatigue body heatmap', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await resetPlan(page);
    await seedExercise(page, 'Bench Press');
    await seedExercise(page, 'Dumbbell Lateral Raise');
  });

  test('panel renders above the bar list, open by default', async ({ page, consoleErrors }) => {
    await gotoHeatmap(page);
    const panel = page.locator('[data-testid="fatigue-heatmap"]');
    await expect(panel).toBeVisible();
    await expect(panel.locator('summary')).toHaveText('Body map');
    expect(await panel.evaluate((el: HTMLDetailsElement) => el.open)).toBe(true);

    // "Above the detailed bar list" is the locked placement, so assert order
    // rather than mere presence.
    const panelPrecedesBars = await page.evaluate(() => {
      const heatmap = document.querySelector('[data-testid="fatigue-heatmap"]');
      const bars = document.querySelector('[data-testid="fatigue-bar-list"]');
      if (!heatmap || !bars) return false;
      return Boolean(
        heatmap.compareDocumentPosition(bars) & Node.DOCUMENT_POSITION_FOLLOWING,
      );
    });
    expect(panelPrecedesBars).toBe(true);
    consoleErrors.assertNoErrors();
  });

  test('the panel collapses from the keyboard', async ({ page }) => {
    await gotoHeatmap(page);
    const panel = page.locator('[data-testid="fatigue-heatmap"]');
    await panel.locator('summary').focus();
    await page.keyboard.press('Enter');
    expect(await panel.evaluate((el: HTMLDetailsElement) => el.open)).toBe(false);
    await expect(page.locator('[data-testid="fatigue-heatmap-figure-front"]')).toBeHidden();
  });

  test('both figures mount and carry an accessible name', async ({ page }) => {
    await gotoHeatmap(page);
    for (const side of ['front', 'back']) {
      const svg = page.locator(`[data-testid="fatigue-heatmap-figure-${side}"] svg`);
      await expect(svg).toBeVisible();
      const label = await svg.getAttribute('aria-label');
      expect(label).toContain(side);
      expect(label).toContain('Planned');
    }
  });

  test('Middle-Shoulder paints both deltoid regions identically', async ({ page }) => {
    await gotoHeatmap(page);
    const delts = await page.evaluate(() =>
      ['front-deltoid', 'rear-deltoid'].map((key) => {
        const el = document.querySelector(`.muscle-region[data-canonical-muscles="${key}"]`);
        return {
          muscle: (el as HTMLElement | null)?.dataset.heatmapMuscle ?? null,
          band: (el as HTMLElement | null)?.dataset.heatmapBand ?? null,
          title: el?.querySelector('title')?.textContent ?? null,
        };
      }),
    );
    expect(delts[0].muscle).toBe('Middle-Shoulder');
    expect(delts[0]).toEqual(delts[1]);
    expect(delts[0].title).toContain('Middle-Shoulder');
  });

  test('regions with no reference range stay visible and neutral', async ({ page }) => {
    await gotoHeatmap(page);
    for (const key of ['neck', 'adductors', 'lower-back']) {
      const region = page.locator(`.muscle-region[data-canonical-muscles="${key}"]`).first();
      await expect(region).toBeVisible();
      await expect(region).toHaveClass(/fatigue-unranked/);
      await expect(region.locator('title')).toHaveText(/no typical range yet/);
    }
  });

  test('planned-only data hides the channel control and captions the channel', async ({ page }) => {
    await gotoHeatmap(page);
    // Nothing has been logged, so there is nothing to switch between.
    await expect(page.locator('[data-heatmap-control]')).toBeHidden();
    await expect(page.locator('[data-testid="fatigue-heatmap-caption"]'))
      .toHaveText('Showing: Planned');
  });

  // The control ships hidden, so the test above passes just as happily against
  // a build that can never show it. This is the one that proves it un-hides.
  test('both channels populated shows the control and switches the painting', async ({ page }) => {
    await seedLoggedSession(page);
    await gotoHeatmap(page);

    await expect(page.locator('[data-heatmap-control]')).toBeVisible();
    const logged = page.locator('[data-testid="fatigue-heatmap-channel-logged"]');
    await expect(logged).toBeVisible();
    await expect(page.locator('[data-testid="fatigue-heatmap-caption"]'))
      .toHaveText('Showing: Planned');

    await logged.click();
    await expect(page.locator('[data-testid="fatigue-heatmap-caption"]'))
      .toHaveText('Showing: Logged');
    await expect(logged).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('[data-testid="fatigue-heatmap-channel-planned"]'))
      .toHaveAttribute('aria-pressed', 'false');

    // Switching channel must actually repaint, and must leave exactly one band
    // class behind rather than accumulating them.
    const after = await page.locator('.muscle-region[data-canonical-muscles="chest"]')
      .first().getAttribute('class');
    const bandCount = (after ?? '').split(/\s+/)
      .filter((c) => c.startsWith('fatigue-')).length;
    expect(bandCount).toBe(1);
  });

  test('painted bands still agree with the embedded data after a period change', async ({ page }) => {
    await gotoHeatmap(page);
    const select = page.locator('[data-testid="fatigue-period-select"]');
    await select.selectOption('last_4_weeks');
    await page.waitForURL(/period=last_4_weeks/);
    await page.waitForSelector('[data-heatmap-state="ready"]');

    // Assert the invariant - painted class agrees with the row the server just
    // sent - rather than a hard-coded expected colour, so this survives any
    // data change.
    const disagreements = await page.evaluate(() => {
      const node = document.getElementById('fatigue-heatmap-data');
      const rows = JSON.parse(node?.textContent ?? '[]');
      const byMuscle = Object.fromEntries(rows.map((r: any) => [r.muscle, r]));
      const channel = (document.querySelector('[data-heatmap-panel]') as HTMLElement)
        .dataset.heatmapChannel;
      const bad: string[] = [];
      document.querySelectorAll('.muscle-region[data-canonical-muscles]').forEach((el) => {
        const region = el as HTMLElement;
        const muscle = region.dataset.heatmapMuscle;
        const expected = muscle && byMuscle[muscle]?.[channel as string]
          ? `fatigue-${byMuscle[muscle][channel as string].band.replace(/_/g, '-')}`
          : 'fatigue-unranked';
        if (!region.classList.contains(expected)) {
          bad.push(`${region.dataset.canonicalMuscles}: expected ${expected}`);
        }
      });
      return bad;
    });
    expect(disagreements).toEqual([]);
  });

  test('degrades quietly when the body map asset cannot load', async ({ page, consoleErrors }) => {
    await page.route('**/bodymaps/**/*.svg', (route) => route.abort());
    await gotoHeatmap(page);
    // The panel stays, the fallback copy stands in, and - the point of the test
    // - no unhandled rejection reaches the console, which would otherwise fail
    // every other test in this file through the shared fixture.
    await expect(page.locator('[data-testid="fatigue-heatmap"]')).toBeVisible();
    await expect(page.locator('[data-testid="fatigue-heatmap-figure-front"] svg')).toHaveCount(0);
    consoleErrors.assertNoErrors();
  });

  test('375px viewport keeps the open panel free of horizontal overflow', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await gotoHeatmap(page);
    await expect(page.locator('[data-testid="fatigue-heatmap-figure-back"] svg')).toBeVisible();
    const overflow = await page.evaluate(
      () => document.body.scrollWidth > document.body.clientWidth + 1,
    );
    expect(overflow).toBe(false);
  });
});

test.describe('/fatigue page', () => {
  test.beforeEach(async ({ consoleErrors }) => {
    consoleErrors.startCollecting();
  });

  test('loads with no console errors', async ({ page, consoleErrors }) => {
    await gotoFatigue(page);
    await expect(page.locator('[data-testid="fatigue-page"]')).toBeVisible();
    consoleErrors.assertNoErrors();
  });

  test('renders both SFR cards (planned + logged)', async ({ page }) => {
    await gotoFatigue(page);
    await expect(page.locator('[data-testid="fatigue-sfr-planned"]')).toBeVisible();
    await expect(page.locator('[data-testid="fatigue-sfr-logged"]')).toBeVisible();
    // Sentinel for fatigue==0 → em dash, never "inf".
    const plannedValue = await page
      .locator('[data-testid="fatigue-sfr-planned-value"]')
      .innerText();
    const loggedValue = await page
      .locator('[data-testid="fatigue-sfr-logged-value"]')
      .innerText();
    expect(plannedValue.toLowerCase()).not.toContain('inf');
    expect(loggedValue.toLowerCase()).not.toContain('inf');
  });

  test('period selector toggles the URL query param', async ({ page }) => {
    await gotoFatigue(page);
    const select = page.locator('[data-testid="fatigue-period-select"]');
    await select.selectOption('last_4_weeks');
    // The onchange submits the form, which round-trips through GET /fatigue.
    await page.waitForURL(/period=last_4_weeks/);
    await expect(select).toHaveValue('last_4_weeks');

    await select.selectOption('this_session');
    await page.waitForURL(/period=this_session/);
    await expect(select).toHaveValue('this_session');
  });

  test('invalid period query param silently falls back to this_week', async ({ page }) => {
    await page.goto(`${FATIGUE_URL}?period=garbage`);
    await page.waitForSelector('[data-testid="fatigue-page"]', { state: 'visible' });
    const select = page.locator('[data-testid="fatigue-period-select"]');
    await expect(select).toHaveValue('this_week');
  });

  test('empty-state copy renders when no plan and no logs', async ({ page }) => {
    // Reset to brand-new DB via /erase-data so the page is genuinely empty.
    await page.request.post('/erase-data', {
      data: { confirm: 'ERASE_ALL_DATA' },
      headers: { 'Content-Type': 'application/json' },
    });
    await gotoFatigue(page);
    await expect(page.locator('[data-testid="fatigue-empty-state"]')).toBeVisible();
  });

  test('dark mode parity — page survives toggle without console errors', async ({ page, consoleErrors }) => {
    await page.goto('/');
    await page.evaluate(() => {
      const toggle = document.querySelector('#darkModeToggle') as HTMLElement | null;
      if (toggle) toggle.click();
    });
    await gotoFatigue(page);
    const theme = await page.evaluate(() =>
      document.documentElement.getAttribute('data-theme')
    );
    expect(theme).toBe('dark');
    await expect(page.locator('[data-testid="fatigue-page"]')).toBeVisible();
    await expect(page.locator('[data-testid="fatigue-sfr-planned"]')).toBeVisible();
    consoleErrors.assertNoErrors();
  });

  test('375px viewport — page renders without horizontal overflow', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await gotoFatigue(page);
    const overflow = await page.evaluate(
      () => document.body.scrollWidth > document.body.clientWidth + 1
    );
    expect(overflow).toBe(false);
  });

  test('badge → /fatigue link from /session_summary navigates here', async ({ page }) => {
    // The "View per-muscle breakdown →" link lands in chapter 2.8, so this
    // spec validates round-trip navigation rather than the link itself.
    await page.goto('/session_summary');
    await page.goto(FATIGUE_URL);
    await expect(page.locator('[data-testid="fatigue-page"]')).toBeVisible();
  });
});
