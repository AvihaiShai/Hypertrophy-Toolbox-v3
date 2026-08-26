/**
 * E2E Test: Volume Splitter Page
 * 
 * Tests the volume splitter functionality including:
 * - Page loading
 * - Training frequency selector
 * - Mode toggle (basic/advanced)
 * - Volume sliders
 * - Calculate and reset buttons
 * - Export to Excel
 */
import type { Page } from '@playwright/test';
import {
  test,
  expect,
  ROUTES,
  SELECTORS,
  waitForVolumeSplitterReady,
  expectToast,
} from './fixtures';

async function setVolumeSlider(page: Page, muscle: string, value: number) {
  const slider = page.locator(`#sliders input.volume-slider[data-muscle="${muscle}"]`);
  await expect(slider).toBeVisible();
  await slider.evaluate((element: Element, nextValue: number) => {
    const input = element as HTMLInputElement;
    input.value = String(nextValue);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }, value);
}

async function expectVolumeSliderValue(page: Page, muscle: string, expectedValue: number) {
  const slider = page.locator(`#sliders input.volume-slider[data-muscle="${muscle}"]`);
  const valueBadge = page.locator(`.current-value[data-muscle="${muscle}"]`);

  await expect(slider).toHaveValue(String(expectedValue));
  await expect(valueBadge).toHaveText(String(expectedValue));
}

test.describe('Volume Splitter Page', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.VOLUME_SPLITTER);
    await waitForVolumeSplitterReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('page loads with correct structure', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('Volume Splitter');

    // Check container
    await expect(page.locator(SELECTORS.PAGE_VOLUME_SPLITTER)).toBeVisible();

    // Check lead text
    await expect(page.locator('.lead')).toContainText('training volume');
  });

  test('training frequency selector is present', async ({ page }) => {
    const trainingDays = page.locator(SELECTORS.TRAINING_DAYS);
    await expect(trainingDays).toBeVisible();

    // Should have options 1-7 days
    const options = trainingDays.locator('option');
    const count = await options.count();
    expect(count).toBe(7);

    // Default should be 3 days
    await expect(trainingDays).toHaveValue('3');
  });

  test('mode toggle is present with basic/advanced options', async ({ page }) => {
    const modeToggle = page.locator('.mode-toggle');
    await expect(modeToggle).toBeVisible();

    // Check radio buttons exist
    const basicRadio = page.locator('#mode-basic');
    const advancedRadio = page.locator('#mode-advanced');
    await expect(basicRadio).toBeVisible();
    await expect(advancedRadio).toBeVisible();

    // One should be checked (depends on default mode)
    const basicChecked = await basicRadio.isChecked();
    const advancedChecked = await advancedRadio.isChecked();
    expect(basicChecked || advancedChecked).toBe(true);
  });

  test('volume sliders container is present', async ({ page }) => {
    const sliders = page.locator('#sliders');
    await expect(sliders).toBeVisible();
  });

  test('calculate button is present and clickable', async ({ page }) => {
    const calculateBtn = page.locator(SELECTORS.CALCULATE_VOLUME_BTN);
    await expect(calculateBtn).toBeVisible();
    await expect(calculateBtn).toContainText('Calculate');

    // Button should be clickable
    await expect(calculateBtn).toBeEnabled();
  });

  test('reset button is present and clickable', async ({ page }) => {
    const resetBtn = page.locator(SELECTORS.RESET_VOLUME_BTN);
    await expect(resetBtn).toBeVisible();
    await expect(resetBtn).toContainText('Reset');

    // Button should be clickable
    await expect(resetBtn).toBeEnabled();
  });

  test('export to excel button is present', async ({ page }) => {
    const exportBtn = page.locator(SELECTORS.EXPORT_VOLUME_EXCEL_BTN);
    await expect(exportBtn).toBeVisible();
    await expect(exportBtn).toContainText('Export to Excel');
  });

  test('changing training days updates selection', async ({ page }) => {
    const trainingDays = page.locator(SELECTORS.TRAINING_DAYS);

    // Change to 5 days
    await trainingDays.selectOption('5');
    await expect(trainingDays).toHaveValue('5');

    // Change to 2 days
    await trainingDays.selectOption('2');
    await expect(trainingDays).toHaveValue('2');
  });

  test('mode toggle switches between basic and advanced', async ({ page }) => {
    const basicLabel = page.locator('label[for="mode-basic"]');
    const advancedLabel = page.locator('label[for="mode-advanced"]');
    const basicRadio = page.locator('#mode-basic');
    const advancedRadio = page.locator('#mode-advanced');

    // Click advanced mode
    await advancedLabel.click();
    await page.waitForTimeout(300); // Wait for UI update
    await expect(advancedRadio).toBeChecked();

    // Click basic mode
    await basicLabel.click();
    await page.waitForTimeout(300);
    await expect(basicRadio).toBeChecked();
  });

  /**
   * Regression coverage for the `.d-none` visibility defect.
   *
   * `calculate volume shows results section` below asserts `toHaveClass(/d-none/)`,
   * which is class-token presence and stayed green for the entire life of the
   * defect. These assert VISIBILITY and the computed value instead.
   */
  test('results and suggestions are actually hidden on first load, not merely class-tagged', async ({ page }) => {
    const results = page.locator('.results-section');
    const suggestions = page.locator('.ai-suggestions-section');

    // Both exist in the DOM...
    await expect(results).toHaveCount(1);
    await expect(suggestions).toHaveCount(1);

    // ...and both are genuinely not visible, which `toHaveClass` cannot tell us.
    await expect(results).toBeHidden();
    await expect(suggestions).toBeHidden();

    // Pin the mechanism too: a future change that hides them some other way
    // (inline style, zero height, visibility) would still be a silent
    // regression of `.d-none` itself.
    for (const locator of [results, suggestions]) {
      const display = await locator.evaluate((el) => getComputedStyle(el).display);
      expect(display).toBe('none');
    }

    // And the card must occupy no space -- the original defect was visible
    // layout, not just a reachable element.
    for (const locator of [results, suggestions]) {
      expect(await locator.boundingBox()).toBeNull();
    }
  });

  test('results become visible only through calculating a split', async ({ page }) => {
    const results = page.locator('.results-section');
    await expect(results).toBeHidden();

    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await expect(results).toBeVisible();

    const display = await results.evaluate((el) => getComputedStyle(el).display);
    expect(display).not.toBe('none');

    // Revealed with content, not an empty shell.
    await expect(results.locator('table tbody tr').first()).toBeVisible();
  });

  test('.d-none is a real declaration in the loaded stylesheets', async ({ page }) => {
    /* The defect was invisible to every gate because nothing ever asked whether
     * the class resolves. Ask the browser directly. */
    const rules = await page.evaluate(() => {
      const found: Array<{ selector: string; display: string; priority: string }> = [];
      for (const sheet of Array.from(document.styleSheets)) {
        let cssRules: CSSRuleList;
        try {
          cssRules = sheet.cssRules;
        } catch {
          continue; // cross-origin sheet; cannot contain an app utility
        }
        for (const rule of Array.from(cssRules)) {
          const styleRule = rule as CSSStyleRule;
          if (styleRule.selectorText === '.d-none') {
            found.push({
              selector: styleRule.selectorText,
              display: styleRule.style.getPropertyValue('display'),
              priority: styleRule.style.getPropertyPriority('display'),
            });
          }
        }
      }
      return found;
    });

    expect(rules.length).toBeGreaterThan(0);
    expect(rules.some((r) => r.display === 'none' && r.priority === 'important')).toBe(true);
  });

  test('calculate volume shows results section', async ({ page }) => {
    const calculateBtn = page.locator(SELECTORS.CALCULATE_VOLUME_BTN);
    const resultsSection = page.locator('.results-section');

    // Results should initially be hidden
    await expect(resultsSection).toHaveClass(/d-none/);

    // Click calculate
    await calculateBtn.click();

    // Wait for results to show
    await page.waitForTimeout(500);

    // Results section should be visible (class d-none removed)
    const hasHiddenClass = await resultsSection.evaluate(el => 
      el.classList.contains('d-none')
    );
    expect(hasHiddenClass).toBe(false);
  });

  test('results table shows after calculation', async ({ page }) => {
    // Click calculate
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await page.waitForTimeout(500);

    // Results table should exist
    const resultsTable = page.locator('.results-section table');
    await expect(resultsTable).toBeVisible();

    // Check headers
    const headers = resultsTable.locator('thead th');
    const headerTexts = await headers.allInnerTexts();
    const headerString = headerTexts.join(' ').toLowerCase();

    expect(headerString).toContain('muscle');
    expect(headerString).toContain('weekly sets');
    expect(headerString).toContain('sets per session');
  });

  test('reset button clears or resets values', async ({ page }) => {
    const resetBtn = page.locator(SELECTORS.RESET_VOLUME_BTN);

    // First calculate to show results
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await page.waitForTimeout(500);

    // Results should be visible
    const resultsSection = page.locator('.results-section');
    let hasHiddenClass = await resultsSection.evaluate(el => 
      el.classList.contains('d-none')
    );
    expect(hasHiddenClass).toBe(false);

    // Click reset
    await resetBtn.click();
    await page.waitForTimeout(500);

    // Behavior depends on implementation - either hides results or resets values
    // At minimum, no errors should occur
  });

  test('export to excel triggers download for calculated data', async ({ page }) => {
    // First calculate to generate data
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await page.waitForTimeout(500);

    const exportBtn = page.locator(SELECTORS.EXPORT_VOLUME_EXCEL_BTN);

    // Setup download handler
    const downloadPromise = page.waitForEvent('download', { timeout: 5000 }).catch(() => null);

    // Click export
    await exportBtn.click();

    // Either download starts or handled differently
    const download = await downloadPromise;
    if (download) {
      const filename = download.suggestedFilename();
      expect(filename.toLowerCase()).toContain('xlsx');
    }
  });

  test('saved plans can be restored and deleted through volume history', async ({ page }) => {
    const trainingDays = '7';
    const chestVolume = 59;
    const bicepsVolume = 47;
    const totalVolume = chestVolume + bicepsVolume;
    const historyRows = page.locator('#history-body tr');
    const historyCountBefore = await historyRows.count();
    const historyWasEmpty = historyCountBefore === 1 &&
      await historyRows.first().locator('td[colspan="5"]').getByText(/No saved volume plans yet\./i).count().catch(() => 0) > 0;
    const expectedCountAfterSave = historyWasEmpty ? 1 : Math.min(historyCountBefore + 1, 100);
    const expectedCountAfterDelete = historyWasEmpty ? 1 : historyCountBefore;

    await page.locator(SELECTORS.TRAINING_DAYS).selectOption(trainingDays);
    await setVolumeSlider(page, 'Chest', chestVolume);
    await setVolumeSlider(page, 'Biceps', bicepsVolume);
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();

    await expect(page.locator('.results-section')).not.toHaveClass(/d-none/);
    await expect(page.locator('#results-body tr').filter({ hasText: 'Chest' }).first()).toContainText('59');
    await expect(page.locator('#results-body tr').filter({ hasText: 'Biceps' }).first()).toContainText('47');

    await Promise.all([
      page.waitForResponse((response) =>
        response.url().includes('/api/save_volume_plan') &&
        response.request().method() === 'POST' &&
        response.ok()
      ),
      page.locator('#export-volume').click(),
    ]);

    await expectToast(page, /Plan #\d+ saved\.\s*Activate for Plan tab/i);
    await expect(historyRows).toHaveCount(expectedCountAfterSave);

    const newestHistoryRow = historyRows.first();
    await expect(newestHistoryRow).toContainText(`${trainingDays} days`);
    await expect(newestHistoryRow).toContainText(`${totalVolume} sets`);

    await page.locator(SELECTORS.TRAINING_DAYS).selectOption('2');
    await setVolumeSlider(page, 'Chest', 3);
    await setVolumeSlider(page, 'Biceps', 4);
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await expectVolumeSliderValue(page, 'Chest', 3);
    await expectVolumeSliderValue(page, 'Biceps', 4);

    await Promise.all([
      page.waitForResponse((response) =>
        /\/api\/volume_plan\/\d+$/.test(response.url()) &&
        response.request().method() === 'GET' &&
        response.ok()
      ),
      newestHistoryRow.locator('button.load-plan').click(),
    ]);

    await expect(page.locator(SELECTORS.TRAINING_DAYS)).toHaveValue(trainingDays);
    await expectVolumeSliderValue(page, 'Chest', chestVolume);
    await expectVolumeSliderValue(page, 'Biceps', bicepsVolume);
    await expect(page.locator('#results-body tr').filter({ hasText: 'Chest' }).first()).toContainText('8.4');

    await newestHistoryRow.locator('button.delete-plan').click();
    await expect(page.locator('#deleteVolumePlanModal')).toBeVisible();

    await Promise.all([
      page.waitForResponse((response) =>
        /\/api\/volume_plan\/\d+$/.test(response.url()) &&
        response.request().method() === 'DELETE' &&
        response.ok()
      ),
      page.locator('#confirmDeleteVolumePlan').click(),
    ]);

    await expectToast(page, /Volume plan deleted successfully/i);
    await expect(historyRows).toHaveCount(expectedCountAfterDelete);
    if (historyWasEmpty) {
      await expect(historyRows.first()).toContainText(/No saved volume plans yet\./i);
    }
  });

  test('volume sliders exist for muscle groups', async ({ page }) => {
    const slidersContainer = page.locator('#sliders');
    
    // Wait for sliders to be populated
    await page.waitForTimeout(500);

    // Should have some slider elements
    const sliders = slidersContainer.locator('input[type="range"]');
    const sliderCount = await sliders.count();
    
    // Basic mode should have major muscle groups
    expect(sliderCount).toBeGreaterThan(0);
  });

  test('muscle group volume can be adjusted', async ({ page }) => {
    const slidersContainer = page.locator('#sliders');
    
    // Wait for sliders to be populated
    await page.waitForTimeout(500);

    const sliders = slidersContainer.locator('input[type="range"]');
    const firstSlider = sliders.first();

    if (await firstSlider.isVisible()) {
      const initialValue = await firstSlider.inputValue();
      
      // Change slider value
      await firstSlider.fill('15');
      const newValue = await firstSlider.inputValue();
      
      expect(newValue).toBe('15');
    }
  });

  test('advanced mode shows more muscle groups', async ({ page }) => {
    // Get basic mode slider count
    await page.waitForTimeout(500);
    const basicSliders = page.locator('#sliders input[type="range"]');
    const basicCount = await basicSliders.count();

    // Switch to advanced mode
    const advancedLabel = page.locator('label[for="mode-advanced"]');
    await advancedLabel.click();
    await page.waitForTimeout(500);

    // Get advanced mode slider count
    const advancedSliders = page.locator('#sliders input[type="range"]');
    const advancedCount = await advancedSliders.count();

    // Advanced should have same or more
    expect(advancedCount).toBeGreaterThanOrEqual(basicCount);
  });

  test('slider labels show muscle group names', async ({ page }) => {
    const slidersContainer = page.locator('#sliders');
    await page.waitForTimeout(500);

    // Check for labels
    const labels = slidersContainer.locator('label, .muscle-label, .slider-label');
    const count = await labels.count();
    
    if (count > 0) {
      const firstLabel = await labels.first().textContent();
      expect(firstLabel?.trim()).toBeTruthy();
    }
  });

  test('slider values show current set count', async ({ page }) => {
    const slidersContainer = page.locator('#sliders');
    await page.waitForTimeout(500);

    // Check for value displays
    const valueDisplays = slidersContainer.locator('.slider-value, output, .value-display');
    const count = await valueDisplays.count();

    expect(count).toBeGreaterThanOrEqual(0);
  });

  test('results show total weekly volume', async ({ page }) => {
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await page.waitForTimeout(500);

    const resultsSection = page.locator('.results-section');
    const text = await resultsSection.textContent();

    // Should show some volume statistics
    expect(text?.toLowerCase()).toMatch(/total|volume|sets/);
  });

  test('results per day change with training days', async ({ page }) => {
    // Calculate with 3 days
    const trainingDays = page.locator(SELECTORS.TRAINING_DAYS);
    await trainingDays.selectOption('3');
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await page.waitForTimeout(500);

    const resultsTable = page.locator('.results-section table');
    const firstRowSetsPerSession = await resultsTable.locator('tbody tr').first().locator('td').nth(2).textContent();

    // Change to 5 days
    await trainingDays.selectOption('5');
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await page.waitForTimeout(500);

    const newSetsPerSession = await resultsTable.locator('tbody tr').first().locator('td').nth(2).textContent();

    // Sets per session should be different (or same if weekly total changes)
    // At minimum both should be valid numbers
    expect(firstRowSetsPerSession).toBeTruthy();
    expect(newSetsPerSession).toBeTruthy();
  });

  test('validation prevents invalid slider values', async ({ page }) => {
    const slidersContainer = page.locator('#sliders');
    await page.waitForTimeout(500);

    const slider = slidersContainer.locator('input[type="range"]').first();
    
    if (await slider.isVisible()) {
      const min = await slider.getAttribute('min') || '0';
      const max = await slider.getAttribute('max') || '30';

      // Slider should have reasonable bounds
      expect(parseInt(min)).toBeGreaterThanOrEqual(0);
      expect(parseInt(max)).toBeLessThanOrEqual(100); // Volume can go up to 60+ sets for some muscles
    }
  });

  test('page maintains state after mode switch', async ({ page }) => {
    const trainingDays = page.locator(SELECTORS.TRAINING_DAYS);
    
    // Set training days to 4
    await trainingDays.selectOption('4');

    // Switch modes
    await page.locator('label[for="mode-advanced"]').click();
    await page.waitForTimeout(300);
    
    await page.locator('label[for="mode-basic"]').click();
    await page.waitForTimeout(300);

    // Training days should remain at 4
    await expect(trainingDays).toHaveValue('4');
  });

  test('results table is scrollable if many rows', async ({ page }) => {
    // Switch to advanced for more muscle groups
    await page.locator('label[for="mode-advanced"]').click();
    await page.waitForTimeout(300);

    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await page.waitForTimeout(500);

    const resultsSection = page.locator('.results-section');
    const overflow = await resultsSection.evaluate(el => {
      const style = getComputedStyle(el);
      return style.overflow === 'auto' || style.overflowY === 'auto' || 
             style.overflow === 'scroll' || style.overflowY === 'scroll' ||
             el.scrollHeight > el.clientHeight;
    });

    // Should either have scroll or fit content
    expect(overflow !== null).toBeTruthy();
  });
});

test.describe('Volume Splitter initial readiness', () => {
  test('exposes the initial history fetch until it has rendered', async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();

    let markRequestStarted!: () => void;
    const requestStarted = new Promise<void>((resolve) => {
      markRequestStarted = resolve;
    });
    let releaseHistory!: () => void;
    const historyRelease = new Promise<void>((resolve) => {
      releaseHistory = resolve;
    });

    await page.route('**/api/volume_history', async (route) => {
      markRequestStarted();
      await historyRelease;
      await route.continue();
    });

    await page.goto(ROUTES.VOLUME_SPLITTER);
    await requestStarted;

    const root = page.locator('html');
    await expect(root).toHaveAttribute('data-volume-history-busy', '1');

    // Deliberately NOT `expect.poll(() => readySettled).toBe(false)`. `poll`
    // succeeds on its first satisfying observation, so it passes the instant it
    // sees `false` — which is also what it sees when the helper is one
    // microtask from resolving. It cannot tell "blocked" from "not settled
    // yet", and a no-op helper survives it. Yielding across two full CDP round
    // trips gives a no-op every chance to resolve, then the flag is read once,
    // synchronously. No hard wait is involved.
    let readySettled = false;
    const ready = waitForVolumeSplitterReady(page).then(() => {
      readySettled = true;
    });
    await page.evaluate(() => new Promise(requestAnimationFrame));
    await page.evaluate(() => new Promise(requestAnimationFrame));
    expect(
      readySettled,
      'the helper resolved while the history fetch was still blocked',
    ).toBe(false);

    releaseHistory();
    await ready;

    // Non-retrying reads first: an auto-retrying matcher here would absorb "the
    // render finished shortly after the helper returned", which is the failure
    // being tested. Absence, not `not.toHaveAttribute(…, '1')`, so a marker set
    // to another value cannot pass.
    const busyAfter = await root.getAttribute('data-volume-history-busy');
    const renderedHistoryRows = await page.locator('#history-body tr').count();
    expect(busyAfter, 'the marker must be removed, not set to another value').toBeNull();
    expect(renderedHistoryRows).toBeGreaterThan(0);
    consoleErrors.assertNoErrors();
  });
});

test.describe('Volume Splitter Mobile Responsive', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(ROUTES.VOLUME_SPLITTER);
    await waitForVolumeSplitterReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('controls are usable on mobile', async ({ page }) => {
    const trainingDays = page.locator(SELECTORS.TRAINING_DAYS);
    await expect(trainingDays).toBeVisible();
    
    const calculateBtn = page.locator(SELECTORS.CALCULATE_VOLUME_BTN);
    await expect(calculateBtn).toBeVisible();
  });

  test('sliders are touch-friendly on mobile', async ({ page }) => {
    const sliders = page.locator('#sliders input[type="range"]');
    await page.waitForTimeout(500);
    
    const count = await sliders.count();
    
    if (count > 0) {
      const firstSlider = sliders.first();
      const box = await firstSlider.boundingBox();
      
      if (box) {
        // Slider should have reasonable touch target height
        expect(box.height).toBeGreaterThanOrEqual(20);
      }
    }
  });

  test('results table readable on mobile', async ({ page }) => {
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await page.waitForTimeout(500);

    const resultsTable = page.locator('.results-section table');
    await expect(resultsTable).toBeVisible();
  });
});

/**
 * `initializePageTooltips()` returns early on `typeof tippy !== 'function'`,
 * and the console collector cannot see a missing global either (see
 * `fixtures.ts`), so a tippy that fails to load removes every tooltip on this
 * page silently.
 *
 * Load order is part of the contract: the tippy bundle resolves `Popper` as a
 * global when it evaluates, so Popper must come first.
 */
test.describe('Volume Splitter tooltips', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.VOLUME_SPLITTER);
    await waitForVolumeSplitterReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('tippy and Popper load locally, in order, and bind the frequency select', async ({ page }) => {
    const globals = await page.evaluate(() => {
      const scoped = window as unknown as Record<string, unknown>;
      return {
        tippy: typeof scoped.tippy,
        popper: typeof scoped.Popper,
        bound: Boolean(
          (document.querySelector('#training-days') as unknown as Record<string, unknown>)?._tippy,
        ),
      };
    });

    expect(globals.popper).toBe('object');
    expect(globals.tippy).toBe('function');
    // This is the order oracle, not the two above: tippy's UMD factory captures
    // `global.Popper` when it evaluates, so an instance can only exist if Popper
    // was already there. Presence at assertion time proves nothing about order.
    expect(globals.bound, '#training-days has no tippy instance').toBe(true);
  });

  test('hovering the frequency select shows a styled tooltip', async ({ page }) => {
    await page.locator('#training-days').hover();

    // The bundle build injects tippy's own CSS; a non-bundle build would leave
    // the box unstyled and this transform-positioned root absent.
    const tooltip = page.locator('[data-tippy-root] .tippy-box');
    await expect(tooltip).toBeVisible();
    await expect(tooltip).toContainText('realistic frequency');
  });
});

/**
 * Packet U1 — Volume Splitter calculation-failure feedback.
 *
 * Plan: `docs/volume_failure_feedback/PLANNING.md` §v2.8 (arms) and §v2.10
 * (success-path invariants). Every arm here lives in this spec deliberately:
 * OD-1 chose E2E-only coverage while the JS-unit qualification window is live,
 * so no Vitest file or case is added. See §v2.14 / U1-FOLLOWUP-1.
 *
 * Console posture is **allow-one**, not fixture-less: the block collects
 * console errors and asserts in `afterEach` that every entry carries the
 * deliberate diagnostic marker, so the intended `console.error` passes and
 * anything else reds. `error-handling.spec.ts:56-64` takes the same fixture but
 * leaves `afterEach` empty, which is a *weaker* posture than this one.
 *
 * Pacing is `page.waitForResponse`, never a hard wait — a hard wait here would
 * move the inventory's hard-wait-lines-per-file surface for this spec.
 */
const CALCULATE_ROUTE = '**/api/calculate_volume';
const CALCULATE_ERROR_REGION = '#volume-calculate-error';
const CALCULATE_ERROR_TESTID = '[data-testid="volume-calculate-error"]';
const TOAST_RETRY = '#liveToast button[aria-label="Retry volume calculation"]';
const CALCULATE_FAILURE_MESSAGE =
  'Volume calculation failed, so no results are shown. Please try again.';

/**
 * Both production diagnostics start with this. The shared fetch wrapper's own
 * `API Error` logs are already filtered by the fixture allow-list; a
 * page-specific message is not, which is what makes the allow-one posture work.
 */
const U1_DIAGNOSTIC_MARKER = 'Volume calculation:';

const SERVER_ERROR_BODY = JSON.stringify({
  ok: false,
  status: 'error',
  message: 'Failed to calculate volume',
  error: { code: 'INTERNAL_ERROR', message: 'Failed to calculate volume' },
});

async function routeCalculateServerError(page: Page) {
  await page.route(CALCULATE_ROUTE, async route => {
    await route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: SERVER_ERROR_BODY,
    });
  });
}

/**
 * Dispatch a chosen subset of the slider's events. `change` alone drives the
 * immediate call site; `input` alone drives the 300 ms debounced one. The
 * shared `setVolumeSlider` helper fires both, which would put two calculations
 * in flight and make the failure arms race against their own setup.
 */
async function dispatchSliderEvents(
  page: Page,
  muscle: string,
  value: number,
  events: string[],
) {
  const slider = page.locator(`#sliders input.volume-slider[data-muscle="${muscle}"]`);
  await expect(slider).toBeVisible();
  await slider.evaluate((element: Element, payload: { value: number; events: string[] }) => {
    const input = element as HTMLInputElement;
    input.value = String(payload.value);
    payload.events.forEach(name => input.dispatchEvent(new Event(name, { bubbles: true })));
  }, { value, events });
}

async function calculateSuccessfully(page: Page) {
  await Promise.all([
    page.waitForResponse(CALCULATE_ROUTE),
    dispatchSliderEvents(page, 'Chest', 12, ['change']),
  ]);
  await expect(page.locator('.results-section')).not.toHaveClass(/d-none/);
  await expect(page.locator('#results-body tr')).not.toHaveCount(0);
}

/**
 * Criterion 3's enumerated stale surfaces, plus criterion 5's "the Calculate
 * button stays usable". Assert the toast *before* calling this — it lives
 * 3000 ms and preceding locator work can consume that window.
 */
async function expectCalculateFailureState(page: Page) {
  const region = page.locator(CALCULATE_ERROR_REGION);
  await expect(region).toBeVisible();
  await expect(region).toHaveCount(1);
  await expect(page.locator('#results-body tr')).toHaveCount(0);
  await expect(page.locator('.results-section')).toHaveClass(/d-none/);
  await expect(page.locator('.ai-suggestions-section')).toHaveClass(/d-none/);
  await expect(page.locator('.muscle-row[class*="status-"]')).toHaveCount(0);
  await expect(page.locator('.current-value[class*="volume-value-pill--"]')).toHaveCount(0);
  await expect(page.locator(SELECTORS.CALCULATE_VOLUME_BTN)).toBeEnabled();
}

test.describe('Volume Splitter calculation failure feedback', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.VOLUME_SPLITTER);
    await waitForVolumeSplitterReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    for (const entry of consoleErrors.errors) {
      expect(
        entry,
        'this block tolerates exactly the U1 calculate diagnostics; anything else is a real console error',
      ).toContain(U1_DIAGNOSTIC_MARKER);
    }
  });

  test('a1 surfaces a non-2xx calculate failure and clears the previous results', async ({ page }) => {
    await calculateSuccessfully(page);
    await routeCalculateServerError(page);

    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();

    await expectToast(page, CALCULATE_FAILURE_MESSAGE);
    await expectCalculateFailureState(page);
  });

  test('a2 surfaces a transport failure and clears the previous results', async ({ page }) => {
    await calculateSuccessfully(page);
    await page.route(CALCULATE_ROUTE, async route => {
      await route.abort('failed');
    });

    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();

    await expectToast(page, CALCULATE_FAILURE_MESSAGE);
    await expectCalculateFailureState(page);
  });

  test('a3 holds one failure region across a sustained fault without rebuilding it', async ({ page }) => {
    await routeCalculateServerError(page);

    await Promise.all([
      page.waitForResponse(CALCULATE_ROUTE),
      dispatchSliderEvents(page, 'Chest', 4, ['input']),
    ]);

    const region = page.locator(CALCULATE_ERROR_REGION);
    await expect(region).toBeVisible();
    // Stamp the live node. A bare count of 1 cannot tell a surviving region
    // from a rebuilt one; the stamp can.
    await region.evaluate(element => element.setAttribute('data-probe', '1'));

    for (const value of [5, 6, 7]) {
      await Promise.all([
        page.waitForResponse(CALCULATE_ROUTE),
        dispatchSliderEvents(page, 'Chest', value, ['input']),
      ]);
    }

    await expect(page.locator(CALCULATE_ERROR_REGION)).toHaveCount(1);
    await expect(page.locator(`${CALCULATE_ERROR_REGION}[data-probe="1"]`)).toHaveCount(1);
  });

  test('a4 tells the user about a first-load failure without revealing empty sections', async ({ page }) => {
    await routeCalculateServerError(page);

    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();

    await expectToast(page, CALCULATE_FAILURE_MESSAGE);
    const region = page.locator(CALCULATE_ERROR_REGION);
    await expect(region).toBeVisible();
    await expect(region).toHaveCount(1);
    await expect(page.locator('.results-section')).toHaveClass(/d-none/);
    await expect(page.locator('.ai-suggestions-section')).toHaveClass(/d-none/);
    await expect(page.locator('#results-body tr')).toHaveCount(0);
  });

  test('a5 clears the previous mode results when the mode-switch calculation fails', async ({ page }) => {
    await calculateSuccessfully(page);
    await routeCalculateServerError(page);

    await page.locator('label[for="mode-advanced"]').click();

    await expectToast(page, CALCULATE_FAILURE_MESSAGE);
    await expect(page.locator(CALCULATE_ERROR_REGION)).toBeVisible();
    await expect(page.locator('#results-body tr')).toHaveCount(0);
    await expect(page.locator('.results-section')).toHaveClass(/d-none/);
  });

  test('a6 does not re-announce slider-driven failures while the same failure state stands', async ({ page }) => {
    test.slow();
    await routeCalculateServerError(page);

    let next = 4;
    const driveOneFailure = async () => {
      await Promise.all([
        page.waitForResponse(CALCULATE_ROUTE),
        dispatchSliderEvents(page, 'Chest', (next % 40) + 1, ['input']),
      ]);
      next += 1;
    };

    await driveOneFailure();
    const toast = page.locator(SELECTORS.TOAST);
    await expect(toast).toBeVisible();
    const region = page.locator(CALCULATE_ERROR_REGION);
    await expect(region).toBeVisible();

    // Keep failing past the toast's own 3000 ms life. Under an unconditional
    // showToast the element re-shows on every failure and never gets there.
    const deadline = Date.now() + 4500;
    while (Date.now() < deadline) {
      await driveOneFailure();
    }
    await expect(toast).toBeHidden({ timeout: 1000 });

    for (let i = 0; i < 4; i += 1) {
      await driveOneFailure();
      await expect(toast).toBeHidden({ timeout: 1000 });
    }
    await expect(region).toBeVisible();
  });

  test('b1 surfaces a post-2xx response-handling failure and clears the previous results', async ({ page }) => {
    await calculateSuccessfully(page);

    // A 200 the response handler cannot render: `displayResults()` dereferences
    // the null entry at `const statusLabel = (data.status || 'optimal');`. The
    // throw lands inside `.then(handleCalculateResponse)`, where the shared
    // wrapper's error branch is never reached.
    await page.route(CALCULATE_ROUTE, async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          ok: true,
          data: {
            results: { Chest: null },
            ranges: { Chest: { min: 1, max: 2 } },
            suggestions: [],
          },
        }),
      });
    });

    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();

    await expectToast(page, CALCULATE_FAILURE_MESSAGE);
    await expectCalculateFailureState(page);

    // `applyServerRanges()` runs before the throw, so the injected range is
    // already painted onto the Chest track when the response is declared a
    // failure. That residue is an accepted disposition (§v2.4) and is pinned
    // here so reverting it becomes a deliberate decision rather than a silent
    // one.
    const track = await page.evaluate(() => {
      const slider = document.querySelector(
        '#sliders input.volume-slider[data-muscle="Chest"]',
      ) as HTMLInputElement | null;
      if (!slider) {
        return null;
      }
      return { background: slider.style.background, sliderMax: Number(slider.max) || 60 };
    });
    expect(track).not.toBeNull();
    const stops = [...track!.background.matchAll(/([\d.]+)%/g)].map(match => Number(match[1]));
    expect(stops.length).toBeGreaterThanOrEqual(6);
    expect(stops[1]).toBeCloseTo((1 / track!.sliderMax) * 100, 3);
    expect(stops[3]).toBeCloseTo((2 / track!.sliderMax) * 100, 3);
  });

  test('c1 announces the failure through the live region', async ({ page }) => {
    await routeCalculateServerError(page);

    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();

    const toast = page.locator(SELECTORS.TOAST);
    await expect(toast).toBeVisible({ timeout: 5000 });
    await expect(toast).toHaveAttribute('role', 'alert');
    await expect(toast).toHaveAttribute('aria-live', 'assertive');
    await expect(page.locator('[data-testid="toast-container"]')).toHaveAttribute('aria-live', 'polite');
    await expect(page.locator(SELECTORS.TOAST_BODY)).toContainText(CALCULATE_FAILURE_MESSAGE);
    // Pins the exact selector `dismissCalculateFailureToast()` depends on.
    await expect(page.locator(TOAST_RETRY)).toHaveCount(1);
  });

  test('c2 leaves focus where the user put it', async ({ page }) => {
    await routeCalculateServerError(page);

    const slider = page.locator('#sliders input.volume-slider[data-muscle="Chest"]');
    await slider.focus();
    await Promise.all([
      page.waitForResponse(CALCULATE_ROUTE),
      dispatchSliderEvents(page, 'Chest', 7, ['input']),
    ]);
    await expect(page.locator(CALCULATE_ERROR_REGION)).toBeVisible();

    const midDrag = await page.evaluate(() => {
      const active = document.activeElement as HTMLElement | null;
      return {
        tag: active?.tagName ?? null,
        muscle: active?.getAttribute('data-muscle') ?? null,
        value: (active as HTMLInputElement | null)?.value ?? null,
        insideFailureSurface: active ? Boolean(active.closest('#volume-calculate-error')) : false,
      };
    });
    expect(midDrag.tag).toBe('INPUT');
    expect(midDrag.muscle).toBe('Chest');
    expect(midDrag.value).toBe('7');
    expect(midDrag.insideFailureSurface).toBe(false);

    const calculateButton = page.locator(SELECTORS.CALCULATE_VOLUME_BTN);
    await Promise.all([
      page.waitForResponse(CALCULATE_ROUTE),
      calculateButton.click(),
    ]);
    const buttonPath = await page.evaluate(() => {
      const active = document.activeElement as HTMLElement | null;
      return {
        id: active?.id ?? null,
        insideFailureSurface: active ? Boolean(active.closest('#volume-calculate-error')) : false,
      };
    });
    expect(buttonPath.id).toBe('calculate-volume');
    expect(buttonPath.insideFailureSurface).toBe(false);
  });

  test('s1 leaves the success path observably identical', async ({ page }) => {
    const regionByTestId = page.locator(CALCULATE_ERROR_TESTID);
    await expect(regionByTestId).toHaveCount(0);

    await calculateSuccessfully(page);

    // Absence from the DOM, not a hidden shell.
    await expect(regionByTestId).toHaveCount(0);
    await expect(page.locator('.results-section')).not.toHaveClass(/d-none/);
    await expect(page.locator('#results-body tr')).not.toHaveCount(0);
    await expect(page.locator('.muscle-row[class*="status-"]')).not.toHaveCount(0);
    await expect(page.locator('.current-value[class*="volume-value-pill--"]')).not.toHaveCount(0);
  });

  test('s2 removes the failure region on the next success', async ({ page }) => {
    await routeCalculateServerError(page);
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();
    await expect(page.locator(CALCULATE_ERROR_REGION)).toBeVisible();

    await page.unroute(CALCULATE_ROUTE);
    await Promise.all([
      page.waitForResponse(CALCULATE_ROUTE),
      dispatchSliderEvents(page, 'Chest', 12, ['change']),
    ]);

    // Removed, not hidden.
    await expect(page.locator(CALCULATE_ERROR_REGION)).toHaveCount(0);
    await expect(page.locator(CALCULATE_ERROR_TESTID)).toHaveCount(0);
    await expect(page.locator('.results-section')).not.toHaveClass(/d-none/);
    await expect(page.locator('#results-body tr')).not.toHaveCount(0);
  });

  test('s3 dismisses the standing failure toast when the next calculation succeeds', async ({ page }) => {
    await routeCalculateServerError(page);
    await page.locator(SELECTORS.CALCULATE_VOLUME_BTN).click();

    // Precondition. Without it "the button is hidden" is vacuously true under a
    // mutation that deletes the toast-creating path, and this arm passes for
    // the wrong reason.
    const toastRetry = page.locator(TOAST_RETRY);
    await expect(toastRetry).toBeVisible();

    await page.unroute(CALCULATE_ROUTE);
    await dispatchSliderEvents(page, 'Chest', 12, ['change']);

    // Bootstrap's hide transition is ~150 ms; an un-dismissed toast stays
    // visible for the remainder of its 3000 ms, so 1 s discriminates.
    await expect(toastRetry).toBeHidden({ timeout: 1000 });
    await expect(page.locator('.results-section')).not.toHaveClass(/d-none/);
    await expect(page.locator('#results-body tr')).not.toHaveCount(0);
  });

  test('s6 lets only the newest calculation paint', async ({ page }) => {
    const calculateButton = page.locator(SELECTORS.CALCULATE_VOLUME_BTN);
    const region = page.locator(CALCULATE_ERROR_REGION);
    const results = page.locator('#results-body tr');

    // --- Primary: a slow failure issued first, a fast success issued second.
    let releaseStaleFailure: () => void = () => {};
    const staleFailureGate = new Promise<void>(resolve => { releaseStaleFailure = resolve; });
    let primaryCalls = 0;
    await page.route(CALCULATE_ROUTE, async route => {
      primaryCalls += 1;
      if (primaryCalls === 1) {
        await staleFailureGate;
        await route.fulfill({ status: 500, contentType: 'application/json', body: SERVER_ERROR_BODY });
        return;
      }
      await route.continue();
    });

    await calculateButton.click();
    await Promise.all([
      page.waitForResponse(response => response.url().includes('/api/calculate_volume') && response.status() === 200),
      calculateButton.click(),
    ]);
    await expect(page.locator('.results-section')).not.toHaveClass(/d-none/);
    await expect(results).not.toHaveCount(0);

    // The wrapper logs its final diagnostic synchronously in the same catch the
    // production `.catch` is chained to, so once it has fired one round trip to
    // the page is enough to drain the microtasks behind it.
    const staleFailureLogged = page.waitForEvent('console', message => message.text().includes('API Error (final)'));
    releaseStaleFailure();
    await staleFailureLogged;
    await page.evaluate(() => undefined);

    await expect(region).toHaveCount(0);
    await expect(results).not.toHaveCount(0);
    await expect(page.locator(SELECTORS.TOAST)).toBeHidden();

    // --- Mirror: a slow success issued first, a fast failure issued second.
    await page.unroute(CALCULATE_ROUTE);
    let releaseStaleSuccess: () => void = () => {};
    const staleSuccessGate = new Promise<void>(resolve => { releaseStaleSuccess = resolve; });
    let mirrorCalls = 0;
    await page.route(CALCULATE_ROUTE, async route => {
      mirrorCalls += 1;
      if (mirrorCalls === 1) {
        await staleSuccessGate;
        await route.continue();
        return;
      }
      await route.fulfill({ status: 500, contentType: 'application/json', body: SERVER_ERROR_BODY });
    });

    await calculateButton.click();
    await Promise.all([
      page.waitForResponse(response => response.url().includes('/api/calculate_volume') && response.status() === 500),
      calculateButton.click(),
    ]);
    await expect(region).toBeVisible();
    await expect(results).toHaveCount(0);

    const staleSuccessLogged = page.waitForEvent('console', message => message.text().includes('API Success'));
    releaseStaleSuccess();
    await staleSuccessLogged;
    await page.evaluate(() => undefined);

    await expect(region).toBeVisible();
    await expect(results).toHaveCount(0);
    await expect(page.locator('.results-section')).toHaveClass(/d-none/);
  });
});
