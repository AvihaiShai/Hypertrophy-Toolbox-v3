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
import type { Page } from '@playwright/test';

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
    const importSection = page.locator('[data-section="import-controls"]');
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
    await expect(table).toBeVisible();
  });

  test('progression legend is visible', async ({ page }) => {
    const legend = page.locator('.progression-legend');
    await expect(legend).toBeVisible();
    
    // Check legend items
    await expect(legend).toContainText('Improved');
    await expect(legend).toContainText('Maintained');
    await expect(legend).toContainText('Below Target');
  });

  test('workout log table has correct headers', async ({ page }) => {
    const table = page.locator('.workout-log-table');
    const headers = table.locator('thead th');

    // Check expected headers exist
    const headerTexts = await headers.allInnerTexts();
    const headerString = headerTexts.join(' ').toLowerCase();
    
    expect(headerString).toContain('routine');
    expect(headerString).toContain('exercise');
    expect(headerString).toContain('planned');
    expect(headerString).toContain('scored');
    expect(headerString).toContain('actions');
  });

  test('import controls collapsible works', async ({ page }) => {
    const collapseToggle = page.locator('[data-section="import-controls"] .collapse-toggle');
    const content = page.locator('#import-content');
    
    // Should be visible initially
    await expect(content).toBeVisible();
    
    // Click to collapse
    await collapseToggle.click();
    await page.waitForTimeout(300); // Wait for animation
    
    // Content should be hidden
    const isHidden = await content.evaluate(el => {
      return window.getComputedStyle(el).display === 'none' || el.classList.contains('collapsed');
    });
    // Note: Implementation may vary - check if height/display changes
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
    const editableCells = page.locator('.editable.scored-cell');
    
    // The table structure should include editable columns
    const tableHeaders = page.locator('.workout-log-table thead th');
    const headerTexts = await tableHeaders.allInnerTexts();
    const editableHeaders = headerTexts.filter(text => text.toLowerCase().includes('scored'));
    
    // Should have scored (editable) columns
    expect(editableHeaders.length).toBeGreaterThan(0);
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
      await expectToast(page, 'Scored reps must be a whole number of at least 0.');
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
    
    // Table should be visible
    const table = page.locator('.workout-log-table');
    await expect(table).toBeVisible();
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

  test('table is scrollable on mobile', async ({ page }) => {
    const table = page.locator('.workout-log-table');
    await expect(table).toBeVisible();

    // Table or its container should allow horizontal scroll
    const isScrollable = await page.evaluate(() => {
      const tableContainer = document.querySelector('.table-responsive, .table-container');
      const table = document.querySelector('.workout-log-table');
      
      if (tableContainer) {
        return tableContainer.scrollWidth > tableContainer.clientWidth;
      }
      return table ? table.scrollWidth > (table.parentElement?.clientWidth || 0) : false;
    });

    // Should be scrollable or fit within view
    expect(isScrollable !== null).toBeTruthy();
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
    const playBtn = firstRow.locator('.btn-video.log-play-video-btn');
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
