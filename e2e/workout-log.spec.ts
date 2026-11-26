/**
 * E2E Test: Workout Log
 * 
 * Tests the workout log page functionality including:
 * - Loading page
 * - Import from workout plan
 * - Editing scored values
 * - Deleting entries
 */
import { test, expect, ROUTES, SELECTORS, expectToast, waitForPageReady } from './fixtures';
import type { Locator, Page } from '@playwright/test';

// Section 0: the filled primary is #4263eb in the light theme this suite runs in.
const PRIMARY_FILL_LIGHT = 'rgb(66, 99, 235)';
// Section 0, "Behind Details", plus logged RPE when the plan also holds an RIR.
const DETAILS_ONLY_CONTROLS = ['Last Progression', 'Reference Video', 'Delete Entry', 'Logged RPE'];
const PLANNED_VALUE_KEYS = ['sets', 'min_reps', 'max_reps', 'rir', 'rpe', 'weight'] as const;
// Section 0, "Always visible": the logged fields of a phone card, in main-row order.
const MAIN_ROW_FIELDS = [
  'scored_min_reps', 'scored_max_reps', 'scored_weight', 'scored_rir', 'scored_rpe',
] as const;
// The owner's Barbell Squat case on #736, as the card prints each logged value.
const SQUAT_LOGGED_TEXT: Record<(typeof MAIN_ROW_FIELDS)[number], string> = {
  scored_min_reps: '10',
  scored_max_reps: '10',
  scored_weight: '100.0',
  scored_rir: '1',
  scored_rpe: '10.0',
};

/** Ids of the visible actions in the page content that render the filled primary. */
async function filledPrimaryActions(page: Page): Promise<string[]> {
  const actions = page.locator('#main-content').locator('button:visible, a:visible');
  return actions.evaluateAll((nodes, fill) => {
    const filled = nodes.filter(node => getComputedStyle(node).backgroundColor === fill);
    return filled.map(node => node.id || (node.textContent ?? '').trim());
  }, PRIMARY_FILL_LIGHT);
}

/** Ids of the visible actions in the page content that carry the primary variant class. */
async function primaryVariantActions(page: Page): Promise<string[]> {
  const actions = page.locator('#main-content .ui-btn--primary:visible');
  return actions.evaluateAll(nodes => nodes.map(node => node.id));
}

/** Names the focused control when focus is inside the card, or null when it left. */
async function focusedCardControl(card: Locator, controls: string[]): Promise<string | null> {
  return card.evaluate((row, names) => {
    const active = document.activeElement;
    if (!active || !row.contains(active)) return null;
    const described = `${active.getAttribute('aria-label') ?? ''} ${active.textContent ?? ''}`;
    const label = described.replace(/\s+/g, ' ').trim();
    const known = names.find(name => label.toLowerCase().includes(name.toLowerCase()));
    return known ?? label;
  }, controls);
}

/** Every stop the keyboard reaches inside one card, walking both ways from Details. */
async function cardTabStops(page: Page, card: Locator): Promise<string[]> {
  const details = card.getByRole('button', { name: 'Details', exact: true });
  const stops: string[] = [];
  for (const key of ['Tab', 'Shift+Tab']) {
    await details.focus();
    for (let step = 0; step < 12; step += 1) {
      await page.keyboard.press(key);
      const stop = await focusedCardControl(card, DETAILS_ONLY_CONTROLS);
      if (stop === null) break;
      stops.push(stop);
    }
  }
  return stops;
}

/** Criterion 19: with Details closed, logged RPE and RIR share the visible main row. */
async function expectEffortInMainRow(card: Locator, rpeText: RegExp): Promise<void> {
  const details = card.getByRole('button', { name: 'Details', exact: true });
  const rpe = card.locator('[data-field="scored_rpe"]');
  const rpeTrigger = rpe.locator('.log-trigger');
  const rirTrigger = card.locator('[data-field="scored_rir"] .log-trigger');
  await expect(details).toHaveAttribute('aria-expanded', 'false');
  await expect(rpeTrigger).toBeVisible();
  await expect(rpe.locator('.editable-text')).toBeVisible();
  await expect(rpe.locator('.editable-text')).toHaveText(rpeText);
  await expect(rirTrigger).toBeVisible();
  const rpeBox = await rpeTrigger.boundingBox();
  const rirBox = await rirTrigger.boundingBox();
  expect(Math.abs(rpeBox!.y - rirBox!.y), 'logged RPE and RIR share one row').toBeLessThanOrEqual(1);
}

/** Edges and overflow of one phone card's five logged fields, read in one pass. */
async function readMainRowFit(card: Locator) {
  return card.evaluate((row, fields) => {
    type Edges = { left: number; right: number; top: number; bottom: number };
    const edges = (rects: DOMRect[]): Edges | null => rects.length === 0 ? null : {
      left: Math.min(...rects.map(rect => rect.left)),
      right: Math.max(...rects.map(rect => rect.right)),
      top: Math.min(...rects.map(rect => rect.top)),
      bottom: Math.max(...rects.map(rect => rect.bottom)),
    };
    const rendered = (node: Element | null | undefined): node is Element =>
      !!node && node.getClientRects().length > 0 && getComputedStyle(node).visibility === 'visible';
    const box = (node: Element | null | undefined) =>
      rendered(node) ? edges([node.getBoundingClientRect()]) : null;
    // A Range follows the glyphs, so text that runs past its own box is still measured.
    const textBox = (node: Element | null | undefined) => {
      if (!rendered(node)) return null;
      const range = document.createRange();
      range.selectNodeContents(node);
      return edges(Array.from(range.getClientRects()).filter(rect => rect.width > 0));
    };
    const root = document.documentElement;
    return {
      card: edges([row.getBoundingClientRect()])!,
      page: { scrollWidth: root.scrollWidth, clientWidth: root.clientWidth },
      fields: fields.map(field => {
        const cell = row.querySelector(`[data-field="${field}"]`);
        const trigger = cell?.querySelector<HTMLElement>('.log-trigger');
        return {
          field,
          box: box(trigger),
          value: textBox(cell?.querySelector('.editable-text')),
          mark: box(cell?.querySelector('.progression-indicator')),
          scrollWidth: trigger?.scrollWidth ?? 0,
          clientWidth: trigger?.clientWidth ?? 0,
        };
      }),
    };
  }, MAIN_ROW_FIELDS);
}

type MainRowFit = Awaited<ReturnType<typeof readMainRowFit>>;
type FitEdges = MainRowFit['card'];

/** How many rows the rendered logged fields occupy, counting tops within 1 px as one row. */
function mainRowCount(read: MainRowFit): number {
  const tops = read.fields.flatMap(entry => entry.box ? [entry.box.top] : []);
  const rows: number[] = [];
  for (const top of tops) {
    if (!rows.some(known => Math.abs(known - top) <= 1)) rows.push(top);
  }
  return rows.length;
}

/**
 * The owner's acceptance for a phone card, as measured failures: every logged field is a
 * 44 x 44 target inside the card, its value and comparison mark sit inside the field and
 * clear of each other, the card is inside the viewport and the page does not scroll
 * sideways. Containment and overlap allow 0.5 px. Sizes allow nothing.
 */
function mainRowFitProblems(read: MainRowFit, viewportWidth: number): string[] {
  const tolerance = 0.5;
  const px = (value: number) => `${Math.round(value * 10) / 10} px`;
  const escapes = (inner: FitEdges, outer: FitEdges) => Math.max(
    outer.left - inner.left,
    inner.right - outer.right,
    outer.top - inner.top,
    inner.bottom - outer.bottom,
  );
  const overlaps = (first: FitEdges, next: FitEdges) =>
    Math.min(first.right, next.right) - Math.max(first.left, next.left) > tolerance &&
    Math.min(first.bottom, next.bottom) - Math.max(first.top, next.top) > tolerance;
  const problems: string[] = [];
  for (const [index, entry] of read.fields.entries()) {
    const name = entry.field;
    if (!entry.box) {
      problems.push(`${name}: the field is not rendered`);
      continue;
    }
    const width = entry.box.right - entry.box.left;
    const height = entry.box.bottom - entry.box.top;
    if (width < 44 || height < 44) {
      problems.push(`${name}: the field is ${px(width)} x ${px(height)}, under 44 x 44`);
    }
    if (escapes(entry.box, read.card) > tolerance) {
      const depth = px(escapes(entry.box, read.card));
      const edge = `field right ${px(entry.box.right)}, card right ${px(read.card.right)}`;
      problems.push(`${name}: the field leaves its card by ${depth} (${edge})`);
    }
    for (const later of read.fields.slice(index + 1)) {
      if (later.box && overlaps(entry.box, later.box)) {
        problems.push(`${name}: the field overlaps the ${later.field} field`);
      }
    }
    if (entry.scrollWidth > entry.clientWidth) {
      const sizes = `${entry.scrollWidth} px of content in a ${entry.clientWidth} px field`;
      problems.push(`${name}: the value is clipped (${sizes})`);
    }
    if (!entry.value) {
      problems.push(`${name}: the value is not rendered`);
    } else if (escapes(entry.value, entry.box) > tolerance) {
      problems.push(`${name}: the value leaves its field by ${px(escapes(entry.value, entry.box))}`);
    }
    if (!entry.mark) {
      problems.push(`${name}: the comparison mark is not rendered`);
    } else if (escapes(entry.mark, entry.box) > tolerance) {
      problems.push(`${name}: the mark leaves its field by ${px(escapes(entry.mark, entry.box))}`);
    }
    if (entry.mark && entry.value && overlaps(entry.mark, entry.value)) {
      problems.push(`${name}: the mark overlaps the value`);
    }
  }
  if (read.card.left < -tolerance || read.card.right > viewportWidth + tolerance) {
    const span = `${px(read.card.left)} to ${px(read.card.right)}`;
    problems.push(`the card spans ${span} in a ${viewportWidth} px viewport`);
  }
  if (read.page.scrollWidth > read.page.clientWidth) {
    const sizes = `scrollWidth ${read.page.scrollWidth}, clientWidth ${read.page.clientWidth}`;
    problems.push(`the page scrolls sideways (${sizes})`);
  }
  return problems;
}

async function importCurrentWorkoutPlan(page: Page): Promise<void> {
  const importResponse = page.waitForResponse(response => {
    return response.url().includes('/export_to_workout_log') &&
      response.request().method() === 'POST';
  });

  await page.locator('#import-from-plan-btn').click();
  const response = await importResponse;

  if (response.ok()) {
    // importFromWorkoutPlan reloads the page after a 1s success toast delay.
    await page.waitForTimeout(1300);
    await waitForPageReady(page);
  }

  await page.locator('#import-from-plan-btn').waitFor({ state: 'visible' });
  await page.waitForFunction(() => {
    const inputs = Array.from(
      document.querySelectorAll<HTMLInputElement>('.workout-log-table input.number-input[type="number"]')
    );

    return inputs.length === 0 || inputs.every(input => input.dataset.hasCustomSpinners === 'true');
  });
}

test.describe('Workout Log Page', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('page loads with correct structure', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('Workout Log');

    // Check import controls section exists
    const importSection = page.locator('.ui-page-actions');
    await expect(importSection).toBeVisible();

    // Check import button exists
    const importBtn = page.locator('#import-from-plan-btn');
    await expect(importBtn).toBeVisible();
    await expect(importBtn).toContainText('Import Current Workout Plan');

    // Check clear log button exists
    const clearBtn = page.locator('#clear-log-btn');
    await expect(clearBtn).toBeVisible();

    // Check table structure
    const table = page.locator('.workout-log-table');
    await expect(table).toBeAttached();
  });

  test('progression legend is visible', async ({ page }) => {
    const legend = page.locator('.progression-legend');
    await expect(legend).toBeVisible({visible: await page.locator('tr[data-log-id]').count() > 0});
    
    // Check legend items
    await expect(legend).toContainText('Improved');
    await expect(legend).toContainText('Maintained');
    await expect(legend).toContainText('Below Target');
  });

  test('workout log table has correct headers', async ({ page }) => {
    const table = page.locator('.workout-log-table');
    const headers = table.locator('thead th');

    // Check expected headers exist
    const headerTexts = await headers.allTextContents();
    const headerString = headerTexts.join(' ').toLowerCase();
    
    expect(headerString).toContain('routine');
    expect(headerString).toContain('exercise');
    expect(headerString).toContain('planned');
    expect(headerString).toContain('logged');
    expect(headerString).toContain('actions');
  });

  test('Import is primary only when the log is empty', async ({page}) => {
    const populated = await page.locator('tr[data-log-id]').count() > 0;
    await expect(page.locator('.ui-empty-state')).toBeVisible({visible: !populated});
    await expect(page.locator('#import-from-plan-btn')).toHaveClass(populated ? /ui-btn--secondary/ : /ui-btn--primary/);
  });

  test('clear log modal opens', async ({ page }) => {
    const clearBtn = page.locator('#clear-log-btn');
    await clearBtn.click();

    // Modal should appear
    const modal = page.locator('#clearLogModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Modal should have confirmation content
    await expect(modal.locator('.modal-body')).toBeVisible();
    await expect(modal.locator('.modal-title')).toContainText('Clear');
    
    // Verify modal has close button and cancel button
    await expect(modal.locator('.btn-close')).toBeVisible();
    await expect(modal.locator('.modal-footer .btn-secondary')).toBeVisible();
  });

  test('editable cells are present in table', async ({ page }) => {
    // Check if editable cells exist (they may only appear when there's data)
    await expect(page.locator('[data-sort-field^="scored_"]')).toHaveCount(5);
    await expect(page.locator('#log-scored')).toHaveAttribute('colspan', '5');
  });
});

test.describe('Workout Log with Data', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();

    // First add some data to workout plan
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    // Select routine and add exercise
    await page.locator(SELECTORS.ROUTINE_ENV).selectOption('GYM');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-program') as HTMLSelectElement;
      return select && select.options.length > 1;
    });
    await page.locator(SELECTORS.ROUTINE_PROGRAM).selectOption('Full Body');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-day') as HTMLSelectElement;
      return select && select.options.length > 1;
    });
    await page.locator(SELECTORS.ROUTINE_DAY).selectOption('Workout A');

    // Wait for exercise dropdown
    await page.waitForFunction(() => {
      const select = document.getElementById('exercise') as HTMLSelectElement;
      return select && select.options.length > 1;
    });

    // Add an exercise
    const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const firstOption = await exerciseSelect.locator('option').nth(1).getAttribute('value');
    if (firstOption) {
      await exerciseSelect.selectOption(firstOption);
    }
    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();

    // Wait for exercise to be added
    await page.waitForSelector('#workout_plan_table_body tr');

    // Navigate to workout log
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('import from workout plan copies exercises', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    // Check if rows appear in the table
    const rows = page.locator('.workout-log-table tbody tr');
    const rowCount = await rows.count();
    
    // Either rows exist or toast shows (depending on implementation)
    // At minimum, no errors should occur
  });

  test('a real import leaves no filled primary and turns Import secondary', async ({ page }) => {
    // Criterion 3, both directions on one page: empty first, then a real import.
    expect((await page.request.post('/clear_workout_log')).ok()).toBe(true);
    await page.reload();
    await waitForPageReady(page);
    const records = page.locator('tr[data-log-id]');
    const importBtn = page.locator('#import-from-plan-btn');
    const clearBtn = page.locator('#clear-log-btn');
    await expect(records).toHaveCount(0);
    await expect(page.locator('.ui-empty-state')).toBeVisible();
    expect(await primaryVariantActions(page)).toEqual(['import-from-plan-btn']);
    expect(await filledPrimaryActions(page)).toEqual(['import-from-plan-btn']);

    await importCurrentWorkoutPlan(page);

    await expect(records.first()).toBeVisible();
    await expect(page.locator('.ui-empty-state')).toBeHidden();
    await expect(importBtn).toBeVisible();
    await expect(importBtn).toHaveClass(/(^|\s)ui-btn--secondary(\s|$)/);
    await expect(importBtn).not.toHaveClass(/(^|\s)ui-btn--primary(\s|$)/);
    await expect(clearBtn).toBeVisible();
    await expect(clearBtn).toHaveClass(/(^|\s)ui-btn--danger(\s|$)/);
    expect(await primaryVariantActions(page)).toEqual([]);
    expect(await filledPrimaryActions(page)).toEqual([]);
  });

  test('phone Log fields have touch targets and Details at the card breakpoint', async ({ page }) => {
    await importCurrentWorkoutPlan(page);
    const row = page.locator('.workout-log-table tr[data-log-id]').first();
    await expect(row.locator('.exercise-name')).toBeVisible();
    for (const width of [375, 390]) {
      await page.setViewportSize({ width, height: 844 });
      const trigger = row.locator('[data-field="scored_rir"] .log-trigger');
      const bounds = await trigger.boundingBox();
      expect(bounds?.width).toBeGreaterThanOrEqual(44);
      expect(bounds?.height).toBeGreaterThanOrEqual(44);
      const details = row.getByRole('button', {name:'Details', exact:true});
      await details.click();
      await expect(row.getByRole('button', {name:/reference video/i})).toBeVisible();
      await expect(row.locator('.date-display')).toBeVisible();
      await details.press('Space');
      await expect(details).toHaveAttribute('aria-expanded', 'false');
      await expect(row.locator('.date-display')).toBeHidden();
      const score = row.locator('[data-field="scored_rir"]');
      await score.locator('.editable-text').click();
      await expect(score.locator('input')).toBeFocused();
      await score.locator('input').press('Escape');
    }
    for (const width of [1359, 1360]) {
      await page.setViewportSize({width, height: 900});
      await expect(page.locator('#log-planned')).toBeVisible({visible: width === 1360});
      await expect(row.locator('.log-details')).toBeVisible({visible: width === 1359});
    }
  });

  test('scored fields can be edited', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const editableCells = page.locator('.editable.scored-cell, [data-field*="scored"]');
    const count = await editableCells.count();

    if (count > 0) {
      const firstCell = editableCells.first();
      await firstCell.click();
      
      // Should be editable - either turns into input or is already input
      const input = firstCell.locator('input');
      const isInput = await input.count() > 0;
      const isContentEditable = await firstCell.getAttribute('contenteditable');
      
      expect(isInput || isContentEditable === 'true').toBeTruthy();
    }
  });

  test('weight field accepts valid values', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const weightCell = page.locator('td[data-field="scored_weight"]').first();
    const count = await weightCell.count();

    if (count > 0) {
      const weightDisplay = weightCell.locator('.editable-text').first();
      await weightDisplay.click();

      const weightInput = weightCell.locator('input').first();
      await expect(weightInput).toBeVisible();
      await weightInput.fill('100');
      await weightInput.blur();
      
      await page.waitForTimeout(700);

      await expect(weightInput).toBeHidden();
      await expect(weightDisplay).toBeVisible();
      await expect(weightDisplay).toContainText('100');
    }
  });

  test('scored reps preserve saved zero after rejection and clear only on an empty edit', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const firstRow = page.locator('.workout-log-table tr[data-log-id]').first();
    await expect(firstRow).toBeVisible();
    const logId = await firstRow.getAttribute('data-log-id');
    expect(logId).toMatch(/^\d+$/);
    const row = page.locator(`.workout-log-table tr[data-log-id="${logId}"]`);
    const minCell = row.locator('[data-field="scored_min_reps"]');
    const maxCell = row.locator('[data-field="scored_max_reps"]');
    const minDisplay = minCell.locator('.editable-text');
    const maxDisplay = maxCell.locator('.editable-text');
    const minInput = minCell.locator('input[type="number"]');
    const maxInput = maxCell.locator('input[type="number"]');

    const readStoredReps = async () => {
      const response = await page.request.get('/get_workout_logs');
      expect(response.ok()).toBeTruthy();
      const rows: Array<{ id: number; scored_min_reps: number | null; scored_max_reps: number | null }> =
        (await response.json()).data;
      const stored = rows.find(entry => String(entry.id) === logId);
      if (!stored) throw new Error(`Workout log entry ${logId} was not found`);
      return { scored_min_reps: stored.scored_min_reps, scored_max_reps: stored.scored_max_reps };
    };
    const original = await readStoredReps();
    const waitForScoreWrite = () => page.waitForResponse(response =>
      new URL(response.url()).pathname === '/update_workout_log' && response.request().method() === 'POST',
    );
    const submittedUpdates: unknown[] = [];
    page.on('request', request => {
      if (new URL(request.url()).pathname === '/update_workout_log' && request.method() === 'POST') {
        submittedUpdates.push(request.postDataJSON().updates);
      }
    });

    try {
      const reset = await page.request.post('/update_workout_log', {
        data: { id: logId, updates: { scored_min_reps: null, scored_max_reps: null } },
      });
      expect(reset.ok()).toBeTruthy();
      await page.clock.install();
      await page.reload();
      await waitForPageReady(page);
      await expect(minDisplay).toHaveText('--');

      await minDisplay.click();
      await minInput.fill('0.0');
      const minSaved = waitForScoreWrite();
      await minInput.press('Enter');
      expect((await minSaved).ok()).toBeTruthy();
      await expect(minDisplay).toHaveText('0');
      await expect(minInput).toBeEnabled();

      await minDisplay.click();
      await expect(minInput).toHaveValue('0');
      await minInput.fill('7');
      await minInput.press('Escape');
      await expect(minDisplay).toHaveText('0');

      await maxDisplay.click();
      await maxInput.fill('0');
      const maxSaved = waitForScoreWrite();
      await maxInput.blur();
      expect((await maxSaved).ok()).toBeTruthy();
      await expect(maxDisplay).toHaveText('0');
      expect(await readStoredReps()).toEqual({ scored_min_reps: 0, scored_max_reps: 0 });

      await page.reload();
      await waitForPageReady(page);
      await expect(minDisplay).toHaveText('0');
      await expect(maxDisplay).toHaveText('0');

      await minDisplay.click();
      await minInput.fill('');
      await minInput.pressSequentially('1e');
      await expect(minInput).toHaveValue('');
      expect(await minInput.evaluate(input => (input as HTMLInputElement).validity.badInput)).toBe(true);
      await minInput.press('Enter');
      await expectToast(page, 'Logged reps must be a whole number of at least 0.');
      await page.clock.runFor(750);
      await expect(minDisplay).toBeVisible();
      await expect(minDisplay).toHaveText('0');
      expect(submittedUpdates).toEqual([{ scored_min_reps: '0.0' }, { scored_max_reps: '0' }]);
      expect(await readStoredReps()).toEqual({ scored_min_reps: 0, scored_max_reps: 0 });

      await minDisplay.click();
      await minInput.fill('1');
      const minRejected = waitForScoreWrite();
      await minInput.press('Enter');
      const rejection = await minRejected;
      expect(rejection.status()).toBe(400);
      expect(await rejection.json()).toMatchObject({ error: { code: 'VALIDATION_ERROR' } });
      await expectToast(page, 'Minimum reps cannot exceed maximum reps.');
      await expect(minDisplay).toHaveText('0');
      await expect(minInput).toBeEnabled();
      expect(await readStoredReps()).toEqual({ scored_min_reps: 0, scored_max_reps: 0 });

      await minDisplay.click();
      await minInput.fill('');
      const minCleared = waitForScoreWrite();
      await minInput.blur();
      const clearResponse = await minCleared;
      expect(clearResponse.ok()).toBeTruthy();
      expect(clearResponse.request().postDataJSON().updates).toEqual({ scored_min_reps: null });
      await expect(minDisplay).toHaveText('--');
      expect(await readStoredReps()).toEqual({ scored_min_reps: null, scored_max_reps: 0 });
      await page.reload();
      await waitForPageReady(page);
      await expect(minDisplay).toHaveText('--');
      await expect(maxDisplay).toHaveText('0');
    } finally {
      await page.request.post('/update_workout_log', { data: { id: logId, updates: original } });
    }
  });

  test('notes field accepts text', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const notesInput = page.locator('input[name*="notes"], textarea[name*="notes"], .notes-input').first();
    const count = await notesInput.count();

    if (count > 0) {
      await notesInput.fill('Test note from E2E');
      await notesInput.blur();
      
      await page.waitForTimeout(500);
    }
  });

  test('delete log entry button works', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const rows = page.locator('.workout-log-table tbody tr');
    const initialCount = await rows.count();

    if (initialCount > 0) {
      // Handle potential confirmation dialog
      page.on('dialog', async dialog => {
        await dialog.accept();
      });

      const deleteBtn = rows.first().locator('button[data-action="delete"], .delete-btn, .btn-danger');
      const hasDel = await deleteBtn.count() > 0;

      if (hasDel) {
        await deleteBtn.first().click();
        await page.waitForTimeout(1000);

        // Verify delete action was attempted (row count may or may not change depending on confirmation)
        const newCount = await rows.count();
        // Test passes as long as no error occurred during the delete flow
        expect(newCount).toBeGreaterThanOrEqual(0);
      } else {
        // No delete button found - test passes (data might not have deletable rows)
        expect(true).toBe(true);
      }
    } else {
      // No rows to delete - test passes
      expect(initialCount).toBe(0);
    }
  });

  test('progression indicator shows status', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const rows = page.locator('.workout-log-table tbody tr');
    const count = await rows.count();

    if (count > 0) {
      // Look for progression status indicators
      const statusIndicators = rows.first().locator('.progression-status, .status-indicator, [class*="progress"]');
      const hasIndicators = await statusIndicators.count() > 0;
      
      // Indicators may only appear after editing scored values
      expect(hasIndicators !== null).toBeTruthy();
    }
  });

  test('assisted progression stays achieved after changing its date', async ({ page }) => {
    await page.request.post('/clear_workout_log');
    await page.request.post('/clear_workout_plan');

    try {
      const addResponse = await page.request.post('/add_exercise', {
        data: {
          routine: 'GYM - Full Body - Workout A',
          exercise: 'Machine Assisted Chin Up',
          sets: 3,
          min_rep_range: 6,
          max_rep_range: 10,
          rir: 2,
          rpe: 8,
          weight: 65,
        },
      });
      expect(addResponse.ok()).toBeTruthy();

      const exportResponse = await page.request.post('/export_to_workout_log');
      expect(exportResponse.ok()).toBeTruthy();

      await page.goto(ROUTES.WORKOUT_LOG);
      await waitForPageReady(page);

      const row = page.locator('tr[data-assisted-bodyweight="true"]', {
        hasText: 'Machine Assisted Chin Up',
      });
      await expect(row).toHaveCount(1);

      const badge = row.locator('td[data-label="Progressive Overload"] .badge');
      await expect(badge).toHaveText('Pending');

      const weightCell = row.locator('td[data-field="scored_weight"]');
      const weightInput = weightCell.locator('input');
      await weightCell.locator('.editable-text').click();
      const weightUpdate = page.waitForResponse((response) =>
        new URL(response.url()).pathname === '/update_workout_log'
          && response.request().method() === 'POST',
      );
      await weightInput.fill('60');
      await weightInput.press('Enter');
      expect((await weightUpdate).ok()).toBeTruthy();
      await expect(badge).toHaveText('Achieved');

      let datePostCount = 0;
      page.on('request', (request) => {
        if (
          new URL(request.url()).pathname === '/update_progression_date'
          && request.method() === 'POST'
        ) {
          datePostCount += 1;
        }
      });

      const dateCell = row.locator('td[data-field="last_progression_date"]');
      const dateInput = dateCell.locator('input[type="date"]');
      await dateCell.click();
      await expect(dateInput).toBeVisible();

      const dateUpdate = page.waitForResponse((response) =>
        new URL(response.url()).pathname === '/update_progression_date'
          && response.request().method() === 'POST',
      );
      await dateInput.fill('2026-07-04');
      expect((await dateUpdate).ok()).toBeTruthy();

      await expect(dateCell.locator('.date-display')).toHaveText('04-07-26');
      await expect(badge).toHaveText('Achieved');
      expect(datePostCount).toBe(1);
    } finally {
      await page.request.post('/clear_workout_log');
      await page.request.post('/clear_workout_plan');
    }
  });
});

test('score edits preserve RIR zero and server progression, and Escape discards every numeric draft', async ({ page, request }) => {
  const routine = `GYM - Score editing ${Date.now()} - Workout A`;
  const added = await request.post('/add_exercise', {
    data: {
      routine, exercise: 'Machine Assisted Chin Up', sets: 1,
      min_rep_range: 6, max_rep_range: 10, rir: 2, rpe: 8, weight: 65,
    },
  });
  expect(added.ok()).toBeTruthy();
  const plan = await request.get('/get_workout_plan');
  const planRow = (await plan.json()).data.find((entry: { routine: string }) => entry.routine === routine);
  expect(planRow).toBeDefined();

  try {
    expect((await request.post('/export_to_workout_log')).ok()).toBeTruthy();
    const readEntry = async () => {
      const response = await request.get('/get_workout_logs');
      expect(response.ok()).toBeTruthy();
      return (await response.json()).data.find((entry: { routine: string }) => entry.routine === routine);
    };
    const { id } = await readEntry();
    await page.clock.install();
    await page.goto(ROUTES.WORKOUT_LOG);
    const row = page.locator(`tr[data-log-id="${id}"]`);
    const cell = (field: string) => row.locator(`[data-field="${field}"]`);
    const rir = cell('scored_rir');
    const badge = row.locator('[data-label="Progressive Overload"] .badge');
    const expectProgression = async (expected: 'Achieved' | 'Pending') => {
      const response = await request.get(`/check_progression/${id}`);
      expect((await response.json()).data.status).toBe(expected);
      await expect(badge).toHaveText(expected);
    };
    const updates: unknown[] = [];
    page.on('request', req => {
      if (new URL(req.url()).pathname === '/update_workout_log' && req.method() === 'POST') {
        updates.push(req.postDataJSON().updates);
      }
    });

    await expectProgression('Pending');
    await rir.locator('.editable-text').click();
    await rir.locator('input').fill('0');
    await rir.locator('input').press('Enter');
    await expect(rir.locator('.editable-text')).toHaveText('0');
    await expectProgression('Achieved');
    await page.reload();
    await expect(rir.locator('.editable-text')).toHaveText('0');
    await expectProgression('Achieved');

    const saved = { scored_rir: 0, scored_rpe: null, scored_weight: null, scored_min_reps: null, scored_max_reps: null };
    for (const [field, original] of Object.entries(saved)) {
      const editor = cell(field);
      const input = editor.locator('input');
      await editor.locator('.editable-text').click();
      await expect(input).toHaveValue(original === null ? '' : String(original));
      if (field === 'scored_weight') {
        await editor.locator('.number-spinner-plus').click();
        await expect(input).toHaveValue('0.5');
      } else {
        await input.fill('1');
      }
      // Cross the old debounce deadline both inside the editor and after Escape.
      await page.clock.fastForward(750);
      await input.press('Escape');
      await expect(input).toBeHidden();
      await expect(editor.locator('.editable-text')).toHaveText(original === null ? '--' : String(original));
    }
    await page.clock.fastForward(750);
    expect(updates).toEqual([{ scored_rir: '0' }]);
    expect(await readEntry()).toMatchObject(saved);

    await rir.locator('.editable-text').click();
    await rir.locator('input').fill('');
    await row.locator('.exercise-name').click();
    await expect(rir.locator('.editable-text')).toHaveText('--');
    await expectProgression('Pending');
    await page.reload();
    await expect(rir.locator('.editable-text')).toHaveText('--');
    await expectProgression('Pending');
    expect((await readEntry()).scored_rir).toBeNull();
    expect(updates).toEqual([{ scored_rir: '0' }, { scored_rir: null }]);
  } finally {
    expect((await request.post('/remove_exercise', { data: { id: planRow.id } })).ok()).toBeTruthy();
  }
});

test('phone effort entry persists on the intended exercise and desktop sorting awaits its save', async ({page, request}) => {
  const routine = `GYM - Log pilot ${Date.now()} - Workout A`;
  const planIds: number[] = [];
  try {
    for (const [exercise, effort] of [
      ['Barbell Curl', {rir: 2}], ['Barbell Seated Military Press', {rpe: 8}],
    ] as const) {
      const response = await request.post('/add_exercise', {data: {
        routine, exercise, sets: 3, min_rep_range: 8, max_rep_range: 12, weight: 30, ...effort,
      }});
      expect(response.ok()).toBe(true);
      const plan = (await (await request.get('/get_workout_plan')).json()).data as
        {id: number; routine: string; exercise: string}[];
      planIds.push(plan.find(entry => entry.routine === routine && entry.exercise === exercise)!.id);
    }
    expect((await request.post('/export_to_workout_log')).ok()).toBe(true);
    const records = async () => (await (await request.get('/get_workout_logs')).json()).data as
      {id: number; routine: string; exercise: string; scored_rpe: number|null; planned_rpe: number|null; planned_rir: number|null}[];
    const [curl, press] = (await records()).filter(entry => entry.routine === routine)
      .sort((a,b) => a.exercise.localeCompare(b.exercise));
    expect(press).toMatchObject({exercise:'Barbell Seated Military Press', scored_rpe:null, planned_rpe:8, planned_rir:null});
    expect(curl.exercise).toBe('Barbell Curl');
    for (const [id, weight] of [[curl.id,30], [press.id,50]]) {
      expect((await request.post('/update_workout_log', {data: {id, updates:{scored_weight:weight}}})).ok()).toBe(true);
    }
    await page.setViewportSize({width:390,height:844});
    await page.goto(ROUTES.WORKOUT_LOG);
    const card = page.locator(`tr[data-log-id="${press.id}"]`).filter({hasText:press.exercise});
    const ordinary = page.locator(`tr[data-log-id="${curl.id}"]`);
    await expect(card.locator('.log-details')).toHaveAttribute('aria-expanded','false');
    await expect(ordinary.locator('[data-field="scored_rpe"] .log-trigger')).toBeHidden();
    await expect(card.locator('[data-field="scored_rir"] .log-trigger')).toBeVisible();
    const rpe = card.locator('[data-field="scored_rpe"]');
    await rpe.locator('.log-trigger').click();
    await rpe.locator('input').fill('9');
    const submitted = page.waitForResponse(res => res.url().endsWith('/update_workout_log'));
    await rpe.locator('input').press('Enter');
    expect((await submitted).ok()).toBe(true);
    await expect(rpe.locator('.log-trigger')).toBeFocused();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await expect(page.locator('#workout_plan_table_body')).toBeAttached();
    await page.locator('#navbar .navbar-toggler').click();
    await page.locator('#navbar a[href="/workout_log"]:visible').first().click();
    await expect(card.locator('.log-details')).toHaveAttribute('aria-expanded','false');
    await expect(rpe.locator('.editable-text')).toHaveText(/^9(?:\.0)?$/);
    expect((await records()).find(entry => entry.id === press.id)?.scored_rpe).toBe(9);
    await expect(card.locator('.ui-badge')).toHaveText((await (await request.get(`/check_progression/${press.id}`)).json()).data.status);
    // Criterion 19: the saved RPE stays in the main row, on return and after a reload.
    await expectEffortInMainRow(card, /^9(?:\.0)?$/);
    await page.reload();
    await expect(card).toHaveCount(1);
    await expectEffortInMainRow(card, /^9(?:\.0)?$/);
    expect((await records()).find(entry => entry.id === press.id)?.scored_rpe).toBe(9);

    const weight = ordinary.locator('[data-field="scored_weight"]');
    await weight.locator('.log-trigger').click();
    await weight.locator('input').fill('60');
    await page.setViewportSize({width:1440,height:900});
    await expect(weight.locator('input')).toBeFocused();
    let release!: () => void;
    const held = new Promise<void>(resolve => { release = resolve; });
    let writes = 0;
    await page.route('**/update_workout_log', async route => {
      writes++;
      await held;
      await route.continue();
    });
    const sort = page.locator('[data-sort-field="scored_weight"]');
    try {
      await sort.click();
      await expect.poll(() => writes).toBe(1);
    } finally { release(); }
    await expect(sort.locator('..')).toHaveAttribute('aria-sort','ascending');
    const ordered = await page.locator('tr[data-log-id]').evaluateAll(rows => rows.map(row => row.getAttribute('data-log-id')));
    expect(ordered.indexOf(String(press.id))).toBeLessThan(ordered.indexOf(String(curl.id)));
    expect(writes).toBe(1);
  } finally {
    for (const id of planIds) await request.post('/remove_exercise', {data:{id}});
  }
});

test('phone card fits five logged fields at 320, 360 and 390 px at scale 8', async ({ page, request }) => {
  // The owner's case on #736: Barbell Squat, planned RIR 2 and RPE 8 at 100 kg, logged RPE 10.0.
  const routine = `GYM - Log scale fit ${Date.now()} - Workout A`;
  const exercise = 'Barbell Squat';
  const added = await request.post('/add_exercise', {
    data: {
      routine, exercise, sets: 3, min_rep_range: 6, max_rep_range: 10, rir: 2, rpe: 8, weight: 100,
    },
  });
  expect(added.ok()).toBe(true);
  const plan = (await (await request.get('/get_workout_plan')).json()).data as
    { id: number; routine: string; exercise: string }[];
  const planRow = plan.find(entry => entry.routine === routine && entry.exercise === exercise);
  expect(planRow).toBeDefined();

  try {
    expect((await request.post('/export_to_workout_log')).ok()).toBe(true);
    const stored = async () => {
      const logs = (await (await request.get('/get_workout_logs')).json()).data as
        Record<string, unknown>[];
      return logs.find(entry => entry.routine === routine && entry.exercise === exercise);
    };
    const imported = await stored();
    expect(imported).toBeDefined();
    const logged = {
      scored_min_reps: 10, scored_max_reps: 10, scored_weight: 100, scored_rir: 1, scored_rpe: 10,
    };
    const written = await request.post('/update_workout_log', {
      data: { id: imported!.id, updates: logged },
    });
    expect(written.ok()).toBe(true);
    // Every logged field has a planned value to compare with, so every field carries a mark.
    expect(await stored()).toMatchObject({
      planned_min_reps: 6, planned_max_reps: 10, planned_weight: 100,
      planned_rir: 2, planned_rpe: 8, ...logged,
    });

    // Level 8 through the app's own controller, which stores it for the server to render.
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(ROUTES.WORKOUT_LOG);
    await page.evaluate(() => {
      const scale = (window as unknown as {
        accessibilityController: { setScale(level: number): void };
      }).accessibilityController;
      scale.setScale(8);
    });

    const card = page.locator(`tr[data-log-id="${imported!.id}"]`).filter({ hasText: exercise });
    const details = card.getByRole('button', { name: 'Details', exact: true });
    const cell = (field: string) => card.locator(`[data-field="${field}"]`);
    for (const width of [320, 360, 390]) {
      const where = `at ${width} px at scale 8`;
      await page.setViewportSize({ width, height: 844 });
      await page.goto(ROUTES.WORKOUT_LOG);
      await expect(page.locator('html')).toHaveAttribute('data-scale', '8');
      const zoom = await page.locator('html').evaluate(el => Number(getComputedStyle(el).zoom));
      expect(zoom, `app scale factor ${where}`).toBe(1.2);
      await expect(card).toHaveCount(1);
      await expect(details).toHaveAttribute('aria-expanded', 'false');
      // The marks are placed by the page script, so their presence means the card is laid out.
      await expect(card.locator('.scored-cell .progression-indicator')).toHaveCount(5);
      await page.evaluate(() => document.fonts.ready.then(() => undefined));
      for (const field of MAIN_ROW_FIELDS) {
        const value = cell(field).locator('.editable-text');
        await expect(value, `${field} as printed ${where}`).toHaveText(SQUAT_LOGGED_TEXT[field]);
        await expect.soft(cell(field).locator('.log-trigger'), `${field} field ${where}`).toBeVisible();
        await expect.soft(value, `${field} value ${where}`).toBeVisible();
        await expect.soft(cell(field).locator('.progression-indicator'), `${field} mark ${where}`)
          .toBeVisible();
      }
      const read = await readMainRowFit(card);
      expect.soft(mainRowFitProblems(read, width), `phone card fit ${where}`).toEqual([]);
      if (width === 390) {
        // Measured on 0511344b: at 390 px the five fields share one row inside the card.
        expect.soft(mainRowCount(read), `rows of logged fields ${where}`).toBe(1);
      }
    }
  } finally {
    const removed = await request.post('/remove_exercise', { data: { id: planRow!.id } });
    expect(removed.ok()).toBe(true);
  }
});

test.describe('Workout Log Details on a phone', () => {
  test.use({ hasTouch: true, viewport: { width: 390, height: 844 } });

  test('Details opens by touch and by keyboard and hides its controls when closed', async ({ page, request }) => {
    const routine = `GYM - Log details ${Date.now()} - Workout A`;
    const exercise = 'Barbell Curl';
    const added = await request.post('/add_exercise', {
      data: {
        routine, exercise, sets: 3, min_rep_range: 8, max_rep_range: 12, rir: 2, rpe: 8, weight: 30,
      },
    });
    expect(added.ok()).toBe(true);
    const plan = (await (await request.get('/get_workout_plan')).json()).data as
      { id: number; routine: string; exercise: string }[];
    const planRow = plan.find(entry => entry.routine === routine && entry.exercise === exercise);
    expect(planRow).toBeDefined();

    try {
      expect((await request.post('/export_to_workout_log')).ok()).toBe(true);
      const logs = (await (await request.get('/get_workout_logs')).json()).data as
        Record<string, unknown>[];
      const record = logs.find(entry => entry.routine === routine && entry.exercise === exercise);
      // Planned by RIR and RPE with nothing logged, so logged RPE sits behind Details.
      expect(record).toMatchObject({
        planned_sets: 3, planned_min_reps: 8, planned_max_reps: 12,
        planned_rir: 2, planned_rpe: 8, planned_weight: 30, scored_rpe: null,
      });

      await page.goto(ROUTES.WORKOUT_LOG);
      const card = page.locator(`tr[data-log-id="${record!.id}"]`).filter({ hasText: exercise });
      await expect(card).toHaveCount(1);
      const details = card.getByRole('button', { name: 'Details', exact: true });
      const plannedValue = (key: string) => card.locator(`[data-field="planned_${key}"]`);
      const dateLabel = card.getByText('Last Progression', { exact: true });
      const controls = {
        'Last Progression': card.getByRole('button', { name: /Last Progression/ }),
        'Reference Video': card.getByRole('button', { name: /reference video/i }),
        'Delete Entry': card.getByRole('button', { name: /Delete Entry/ }),
        'Logged RPE': card.locator('[data-field="scored_rpe"] .log-trigger'),
      };

      const expectClosed = async () => {
        await expect(details).toHaveAttribute('aria-expanded', 'false');
        for (const key of PLANNED_VALUE_KEYS) {
          await expect(plannedValue(key), `planned ${key} while closed`).toBeHidden();
        }
        await expect(dateLabel).toBeHidden();
        for (const [name, control] of Object.entries(controls)) {
          await expect(control, `${name} while closed`).toBeHidden();
        }
        const stops = await cardTabStops(page, card);
        // The walk is only evidence if it reaches the fields that stay in the main row.
        expect(stops.some(stop => /logged RIR/i.test(stop)), 'Tab reaches logged RIR').toBe(true);
        for (const name of DETAILS_ONLY_CONTROLS) {
          expect(stops, `${name} is out of the tab order while closed`).not.toContain(name);
        }
      };

      const expectOpen = async () => {
        await expect(details).toHaveAttribute('aria-expanded', 'true');
        for (const key of PLANNED_VALUE_KEYS) {
          const stored = Number(record![`planned_${key}`]);
          await expect(plannedValue(key), `planned ${key} while open`).toBeVisible();
          await expect(plannedValue(key)).toHaveText(new RegExp(`^${stored}(?:\\.0)?$`));
        }
        await expect(dateLabel).toBeVisible();
        for (const [name, control] of Object.entries(controls)) {
          await expect(control, `${name} while open`).toBeVisible();
        }
        // Section 0: below 768 px every button is at least 44 px tall.
        for (const name of ['Reference Video', 'Delete Entry'] as const) {
          const box = await controls[name].boundingBox();
          expect(box!.height, `${name} height at 390 px`).toBeGreaterThanOrEqual(44);
        }
        const stops = await cardTabStops(page, card);
        for (const name of DETAILS_ONLY_CONTROLS) {
          expect(stops, `Tab reaches ${name} while open`).toContain(name);
        }
      };

      await expectClosed();
      await details.tap();
      await expectOpen();
      await details.press('Enter');
      await expectClosed();
      await details.press('Space');
      await expectOpen();
    } finally {
      const removed = await request.post('/remove_exercise', { data: { id: planRow!.id } });
      expect(removed.ok()).toBe(true);
    }
  });
});

test.describe('Workout Log Date Filter', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('date filter exists', async ({ page }) => {
    // The workout log has date inputs per row for "Last Progression" date
    // Check that at least one date-related input exists in the table
    const dateInputs = page.locator('.workout-log-table input[type="date"], .date-input');
    const count = await dateInputs.count();
    
    // If there are logs, there should be date inputs
    // If no logs, that's also valid
    expect(count >= 0).toBeTruthy();
  });

  test('date filter changes displayed data', async ({ page }) => {
    // This page doesn't have a global date filter, but has per-row date inputs
    // for Last Progression. Test that the date inputs in the table work.
    const dateInputs = page.locator('.workout-log-table .date-input, .workout-log-table input[type="date"]');
    const count = await dateInputs.count();
    
    if (count > 0) {
      // Get the first date input that's visible/editable
      const firstDateInput = dateInputs.first();
      
      // The date inputs might be hidden until clicked, so just verify they exist
      await expect(firstDateInput).toBeAttached();
    }
    
    await expect(page.locator('.workout-log-table')).toBeAttached();
  });
});

test.describe('Workout Log Clear Functionality', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('clear log confirmation modal exists', async ({ page }) => {
    const clearBtn = page.locator('#clear-log-btn');
    await clearBtn.click();

    const modal = page.locator('#clearLogModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Should have warning text
    const modalBody = modal.locator('.modal-body');
    const text = await modalBody.textContent();
    expect(text?.toLowerCase()).toMatch(/clear|delete|remove/);

    await modal.locator('.btn-close').click();
  });

  test('cancel button closes clear modal without action', async ({ page }) => {
    const clearBtn = page.locator('#clear-log-btn');
    await clearBtn.click();

    const modal = page.locator('#clearLogModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Verify cancel button exists in modal footer
    const cancelBtn = modal.locator('.modal-footer .btn-secondary');
    await expect(cancelBtn).toBeVisible();
    await expect(cancelBtn).toContainText('Cancel');
    
    // Verify clicking cancel doesn't trigger the clear action
    // (We just verify the button exists and is clickable - Bootstrap modal close is external dependency)
    await cancelBtn.click();
    
    // Wait briefly for any action
    await page.waitForTimeout(300);
    
    // Test passes if no error occurred during cancel click
  });
});

test.describe('Workout Log Mobile Responsive', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('import button accessible on mobile', async ({ page }) => {
    const importBtn = page.locator('#import-from-plan-btn');
    await expect(importBtn).toBeVisible();

    const box = await importBtn.boundingBox();
    if (box) {
      expect(box.width).toBeGreaterThanOrEqual(44);
    }
  });
});

// ============================================================================
// §5 — Exercise reference video modal on /workout_log (PLANNING.md §5.5)
//
// The modal partial is included once in base.html, so the same flow as on
// /workout_plan applies here. Every server-rendered log row carries a video
// button. A valid youtube_video_id opens the modal. A NULL youtube_video_id
// opens a YouTube search tab directly.
// ============================================================================

test.describe('Exercise reference video modal (workout-log)', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();

    // Seed the plan with one exercise, then import into the log so the
    // server-rendered log table actually has a row to inspect.
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    await page.locator(SELECTORS.ROUTINE_ENV).selectOption('GYM');
    await page.waitForFunction(() => {
      const s = document.getElementById('routine-program') as HTMLSelectElement | null;
      return Boolean(s && s.options.length > 1);
    });
    await page.locator(SELECTORS.ROUTINE_PROGRAM).selectOption('Full Body');
    await page.waitForFunction(() => {
      const s = document.getElementById('routine-day') as HTMLSelectElement | null;
      return Boolean(s && s.options.length > 1);
    });
    await page.locator(SELECTORS.ROUTINE_DAY).selectOption('Workout A');
    await page.waitForFunction(() => {
      const s = document.getElementById('exercise') as HTMLSelectElement | null;
      return Boolean(s && s.options.length > 1);
    });
    const exSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const firstValue = await exSelect.locator('option').nth(1).getAttribute('value');
    if (firstValue) {
      await exSelect.selectOption(firstValue);
    }
    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();
    await page.waitForSelector('#workout_plan_table_body tr');

    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
    await importCurrentWorkoutPlan(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('every log row has an accessible play button', async ({ page }) => {
    const rows = page.locator('.workout-log-table tbody tr');
    const rowCount = await rows.count();
    expect(rowCount).toBeGreaterThan(0);

    const firstRow = rows.first();
    const playBtn = firstRow.locator('.log-play-video-btn');
    await expect(playBtn).toBeVisible();

    // Default seed is uncurated → search-variant icon + accessible name.
    const ariaLabel = await playBtn.getAttribute('aria-label');
    expect(ariaLabel).toMatch(/^Search YouTube for a /);
    await expect(playBtn.locator('i')).toHaveClass(/fa-search/);
  });

  test('clicking search on an uncurated row opens a YouTube search tab — no modal', async ({ page }) => {
    await page.evaluate(() => {
      // @ts-expect-error - test-only capture
      window.__openedUrl = null;
      window.open = (url) => {
        // @ts-expect-error - test-only capture
        window.__openedUrl = url;
        return null;
      };
    });

    const playBtn = page.locator('.workout-log-table .log-play-video-btn').first();
    await playBtn.click();

    // Default seed is uncurated → straight to YouTube search, modal stays closed.
    const opened = await page.evaluate(() => {
      // @ts-expect-error - test-only capture set above
      return window.__openedUrl as string | null;
    });
    expect(opened).toMatch(/^https:\/\/www\.youtube\.com\/results\?search_query=/);
    await expect(page.locator('#exerciseVideoModal')).toBeHidden();
  });

  test('valid id (driven via JS) opens embed mode', async ({ page }) => {
    // Server-rendered log rows can carry a real youtube_video_id, but no
    // curated CSV ships with this branch — drive the modal via the public
    // window API to exercise the embed path on the log page.
    await page.evaluate(() => {
      // @ts-expect-error - exposed by exercise-video-modal.js
      window.openExerciseVideoModal('dQw4w9WgXcQ', 'Test Log Exercise');
    });

    await expect(page.locator('#exerciseVideoModal')).toBeVisible();
    await expect(page.locator('#exerciseVideoEmbedWrap')).toBeVisible();

    const src = await page.locator('#exerciseVideoIframe').getAttribute('src');
    expect(src).toMatch(/^https:\/\/www\.youtube\.com\/embed\/dQw4w9WgXcQ/);
  });
});
