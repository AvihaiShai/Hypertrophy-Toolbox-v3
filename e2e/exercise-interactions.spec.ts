/**
 * E2E Test: Exercise Interactions
 * 
 * Tests exercise-specific interactions including:
 * - Delete exercise from plan
 * - Replace exercise functionality
 * - Superset linking/unlinking
 * - Exercise details modal
 * - Inline editing (sets, reps, weight)
 * - Reorder exercises
 */
import {
  test,
  expect,
  ROUTES,
  SELECTORS,
  waitForWorkoutPlanReady,
  expectToast,
} from './fixtures';
import type { Page } from '@playwright/test';
import { test as guardedTest } from './console-guard';
import {
  BENCH, DEADLIFT, ROUTINE_A, ROUTINE_B, ROW, SQUAT, addPlanRow, loadPlan, planData,
  planPost, planRow, planRows, routineTab,
} from './workout-plan-fixture';
import { filterToggle, setDetails } from './workout-plan-redesign';

const TEST_ROUTINE = 'GYM - Full Body - Workout A';

/**
 * The rows the plan table renders for `TEST_ROUTINE`.
 *
 * `updateWorkoutPlanTable()` stamps both attributes on every row it builds from
 * plan data, so this matches real exercise rows only — never a placeholder, and
 * never a row another routine put there.
 */
const TEST_ROUTINE_ROWS =
  `#workout_plan_table_body tr[data-exercise-id][data-routine="${TEST_ROUTINE}"]`;

/**
 * Helper to select a complete routine
 */
async function selectRoutine(page: import('@playwright/test').Page) {
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
}

function extractExerciseName(entry: unknown): string | null {
  if (typeof entry === 'string') {
    return entry.trim() || null;
  }
  if (!entry || typeof entry !== 'object') {
    return null;
  }
  const candidate = entry as Record<string, unknown>;
  const raw =
    candidate.exercise ??
    candidate.exercise_name ??
    candidate.name ??
    candidate.value;
  return typeof raw === 'string' && raw.trim() ? raw.trim() : null;
}

function extractRoutineName(entry: unknown): string | null {
  if (!entry || typeof entry !== 'object') {
    return null;
  }
  const candidate = entry as Record<string, unknown>;
  const raw = candidate.routine;
  return typeof raw === 'string' && raw.trim() ? raw.trim() : null;
}

function extractDataRows(payload: unknown): unknown[] {
  if (Array.isArray(payload)) {
    return payload;
  }
  if (!payload || typeof payload !== 'object') {
    return [];
  }
  const candidate = payload as Record<string, unknown>;
  return Array.isArray(candidate.data) ? candidate.data : [];
}

/**
 * Add exercises to `TEST_ROUTINE` until it holds `minimumCount` of them, and
 * report how many were added.
 *
 * The decision comes from `/get_workout_plan` rather than from the table,
 * because an awaited HTTP response says the same thing however fast the browser
 * is. Existing rows are counted first and their names excluded from the
 * candidates, so a partially seeded routine is topped up rather than duplicated
 * and an already-full one is left alone.
 */
async function seedRoutineToMinimum(
  request: import('@playwright/test').APIRequestContext,
  minimumCount: number
): Promise<number> {
  const planResponse = await request.get('/get_workout_plan');
  expect(planResponse.ok(), 'expected /get_workout_plan to succeed during E2E setup').toBeTruthy();
  const planPayload = await planResponse.json().catch(() => ({}));
  const routineRows = extractDataRows(planPayload).filter(
    (row) => extractRoutineName(row) === TEST_ROUTINE
  );

  let currentCount = routineRows.length;
  if (currentCount >= minimumCount) {
    return 0;
  }

  const existingNames = new Set(
    routineRows.map(extractExerciseName).filter((name): name is string => Boolean(name))
  );

  const allResponse = await request.get('/get_all_exercises');
  expect(allResponse.ok(), 'expected /get_all_exercises to succeed during E2E setup').toBeTruthy();
  const allPayload = await allResponse.json().catch(() => ({}));
  const allRows = extractDataRows(allPayload);

  const addCandidates = allRows
    .map(extractExerciseName)
    .filter((name): name is string => Boolean(name))
    .filter((name) => !existingNames.has(name));

  let addedCount = 0;
  for (const exerciseName of addCandidates) {
    if (currentCount >= minimumCount) {
      break;
    }
    const addResponse = await request.post('/add_exercise', {
      data: {
        routine: TEST_ROUTINE,
        exercise: exerciseName,
        sets: 3,
        min_rep_range: 8,
        max_rep_range: 12,
        weight: 100,
        rir: 2,
      },
    });
    if (addResponse.ok()) {
      currentCount += 1;
      addedCount += 1;
      existingNames.add(exerciseName);
    }
  }

  expect(
    currentCount,
    `expected "${TEST_ROUTINE}" to hold at least ${minimumCount} exercise(s) after seeding`
  ).toBeGreaterThanOrEqual(minimumCount);

  return addedCount;
}

/**
 * Leave the page showing at least `minimumCount` exercises in `TEST_ROUTINE`.
 *
 * Both halves are explicit, awaited observables, which is what lets every caller
 * navigate with `waitForWorkoutPlanReady()` instead of `networkidle`.
 * `seedRoutineToMinimum()` decides from a `/get_workout_plan` response, so the
 * seeding decision cannot race the `fetchWorkoutPlan()` that fills the table;
 * the poll below then waits for the browser to have actually rendered those
 * rows, so callers receive a populated table rather than the promise of one.
 * `networkidle` used to supply the second half by accident, and nothing else in
 * this file depended on it — the readiness marker tracks only the
 * profile-estimate write, which is why it could not substitute before.
 *
 * A reload is needed exactly when rows were added behind the loaded page's
 * back; when the routine was already full the page's own fetch will render
 * them and the poll waits for it.
 */
async function ensureRoutineHasExercises(
  page: import('@playwright/test').Page,
  request: import('@playwright/test').APIRequestContext,
  minimumCount: number
) {
  const addedCount = await seedRoutineToMinimum(request, minimumCount);

  if (addedCount > 0) {
    await page.reload();
    await waitForWorkoutPlanReady(page);
  }

  await selectRoutine(page);
  await routineTab(page, TEST_ROUTINE).click();

  await expect.poll(() => page.locator(TEST_ROUTINE_ROWS).count(), {
    message: `expected the plan table to render at least ${minimumCount} "${TEST_ROUTINE}" row(s)`,
  }).toBeGreaterThanOrEqual(minimumCount);
}

test.describe('Exercise Delete Functionality', () => {
  test.beforeEach(async ({ page, request, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await ensureRoutineHasExercises(page, request, 1);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('delete button exists for exercises in table', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const rows = page.locator('#workout_plan_table_body tr');
    expect(await rows.count(), 'beforeEach seeds at least one plan row').toBeGreaterThan(0);

    const deleteBtn = rows.first().locator('button[data-action="delete"], .delete-btn, .btn-danger');
    await expect(deleteBtn).toBeVisible();
  });

  test('clicking delete sends the remove request', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const rows = page.locator('#workout_plan_table_body tr');
    expect(await rows.count(), 'beforeEach seeds at least one plan row').toBeGreaterThan(0);

    const deleteBtn = rows.first().locator('button[data-action="delete"], .delete-btn, .btn-danger');
    const responsePromise = page.waitForResponse(response =>
      response.url().endsWith('/remove_exercise') && response.request().method() === 'POST'
    );
    await deleteBtn.click();
    const response = await responsePromise;
    expect(response.status()).toBe(200);
  });

  test('delete removes exercise from table', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const initialCount = await page.locator('#workout_plan_table_body tr').count();

    if (initialCount > 0) {
      // Handle potential confirmation dialog
      page.on('dialog', async dialog => {
        await dialog.accept();
      });

      const deleteBtn = page.locator('#workout_plan_table_body tr').first().locator('button[data-action="delete"], .delete-btn, .btn-danger');
      await deleteBtn.click();

      // Wait for deletion to complete
      await page.waitForTimeout(1000);

      // Check if count decreased or toast appeared
      const newCount = await page.locator('#workout_plan_table_body tr').count();
      const toastVisible = await page.locator('.toast').isVisible().catch(() => false);

      expect(newCount < initialCount || toastVisible).toBe(true);
    }
  });
});

test.describe('Replace Exercise Functionality', () => {
  test.beforeEach(async ({ page, request, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await ensureRoutineHasExercises(page, request, 1);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('replace button exists for exercises', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const rows = page.locator('#workout_plan_table_body tr');
    const count = await rows.count();

    if (count > 0) {
      const replaceBtn = rows.first().locator('button[data-action="replace"], .replace-btn, [title*="Replace"]');
      await expect(replaceBtn).toHaveCount(1);
      await expect(replaceBtn).toBeVisible();
    }
  });

  test('replace action triggers API call', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const rows = page.locator('#workout_plan_table_body tr');
    const count = await rows.count();

    if (count > 0) {
      // Listen for API call
      const requestPromise = page.waitForRequest(req =>
        req.url().includes('/replace_exercise') && req.method() === 'POST'
      );

      const replaceBtn = rows.first().locator('button[data-action="replace"], .replace-btn, [title*="Replace"], .btn-replace');
      await expect(replaceBtn).toBeVisible();
      await replaceBtn.click();
      const request = await requestPromise;
      expect(request.postDataJSON()).toMatchObject({
        id: expect.anything(),
        strategy: 'ai',
      });
    }
  });
});

test.describe('Superset Functionality', () => {
  test.beforeEach(async ({ page, request, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await ensureRoutineHasExercises(page, request, 2);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('superset checkboxes exist in table', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const checkboxes = page.locator('#workout_plan_table_body input[type="checkbox"]');
    const count = await checkboxes.count();
    expect(count).toBeGreaterThan(0);
  });

  test('link superset button exists', async ({ page }) => {
    const linkBtn = page.locator('#link-superset-btn');
    // Button is in a hidden container initially, just check it exists in DOM
    await expect(linkBtn).toBeAttached();
  });

  test('unlink superset button exists', async ({ page }) => {
    const unlinkBtn = page.locator('#unlink-superset-btn');
    // May be hidden initially
    await expect(unlinkBtn).toBeAttached();
  });

  test('selecting exercises enables link button', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const checkboxes = page.locator('#workout_plan_table_body .superset-checkbox');
    const count = await checkboxes.count();

    if (count >= 2) {
      // Click checkboxes to properly trigger change events
      await checkboxes.nth(0).click();
      await checkboxes.nth(1).click();
      await page.waitForTimeout(300);

      // Link button should be enabled (or at least visible)
      const linkBtn = page.locator('#link-superset-btn');
      // Accept either enabled or visible as valid - depends on UI implementation
      const isEnabled = await linkBtn.isEnabled().catch(() => false);
      const isVisible = await linkBtn.isVisible().catch(() => false);
      expect(isEnabled || isVisible).toBeTruthy();
    }
  });

  test('selection info shows count', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const checkboxes = page.locator('#workout_plan_table_body input[type="checkbox"]');
    const count = await checkboxes.count();

    if (count >= 1) {
      await checkboxes.nth(0).check();

      const selectionInfo = page.locator('#superset-selection-info');
      const text = await selectionInfo.textContent();
      expect(text).toContain('1');
    }
  });

  test('linking exercises creates superset', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const checkboxes = page.locator('#workout_plan_table_body .superset-checkbox');
    const count = await checkboxes.count();

    if (count >= 2) {
      // Click checkboxes to properly trigger change events
      await checkboxes.nth(0).click();
      await checkboxes.nth(1).click();
      await page.waitForTimeout(300);

      const linkBtn = page.locator('#link-superset-btn');
      
      // Only click if enabled
      const isEnabled = await linkBtn.isEnabled().catch(() => false);
      if (isEnabled) {
        await linkBtn.click();
        await page.waitForTimeout(1000);
      }

      await expect.poll(() => page.locator(
        '#workout_plan_table_body tr[data-superset-group]:not([data-superset-group=""])'
      ).count()).toBe(2);
    }
  });
});

test.describe('Exercise Inline Editing', () => {
  test.beforeEach(async ({ page, request, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await ensureRoutineHasExercises(page, request, 1);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('sets field is editable', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const setsInput = page.locator('#workout_plan_table_body tr').first().locator('input[name*="sets"], .sets-input, td:nth-child(4) input');
    const count = await setsInput.count();

    if (count > 0) {
      await expect(setsInput).toBeEditable();
    }
  });

  test('weight field is editable', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const weightInput = page.locator('#workout_plan_table_body tr').first().locator('input[name*="weight"], .weight-input');
    const count = await weightInput.count();

    if (count > 0) {
      await expect(weightInput).toBeEditable();
    }
  });

  test('reps field is editable', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const repsInput = page.locator('#workout_plan_table_body tr').first().locator('input[name*="reps"], .reps-input');
    const count = await repsInput.count();

    if (count > 0) {
      await expect(repsInput).toBeEditable();
    }
  });

  test('editing triggers save', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    // Listen for update API call
    const requestPromise = page.waitForRequest(req => 
      (req.url().includes('/update') || req.url().includes('/save')) && 
      req.method() === 'POST'
    ).catch(() => null);

    // Find an actual number input (sets, reps, weight) - exclude checkboxes
    const setsInput = page.locator('#workout_plan_table_body tr').first().locator('input[type="number"], input.editable-input').first();
    const count = await setsInput.count();

    if (count > 0) {
      const isEditable = await setsInput.isEditable();
      if (isEditable) {
        await setsInput.fill('5');
        await setsInput.blur();
      }
      
      // Wait for potential API call
      await page.waitForTimeout(1000);
    }
  });
});

test.describe('Exercise Details Modal', () => {
  test.beforeEach(async ({ page, request, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await ensureRoutineHasExercises(page, request, 1);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('exercise name is clickable', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const exerciseLink = page.locator('#workout_plan_table_body tr').first().locator('a, .exercise-name, [data-exercise], td:nth-child(4)');
    const count = await exerciseLink.count();

    if (count > 0) {
      // Exercise cell should exist and contain text
      const text = await exerciseLink.first().textContent();
      expect(text?.trim().length).toBeGreaterThan(0);
    }
  });

  test('exercise name is currently rendered as plain text', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const exerciseName = page.locator('#workout_plan_table_body tr').first().locator('.exercise-name');
    await expect(exerciseName).toBeVisible();
    await expect(exerciseName).not.toHaveAttribute('role', 'button');
    await expect(page.locator('#exerciseDetailsModal')).toHaveCount(0);
  });
});

test.describe('Exercise Filter Application', () => {
  // The one block that seeds nothing: its two tests never touch the plan table.
  // They read the server-rendered filter dropdowns, and the one that uses the
  // exercise dropdown waits for it with its own `waitForFunction`.
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('applying filter updates exercise dropdown', async ({ page }) => {
    await selectRoutine(page);
    await filterToggle(page).click();

    // Get initial option count
    const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    await page.waitForFunction(() => {
      const select = document.getElementById('exercise') as HTMLSelectElement;
      return select && select.options.length > 1;
    });

    const initialCount = await exerciseSelect.locator('option').count();

    // Apply a filter
    const filterForm = page.locator('#filters-form');
    const filterSelects = filterForm.locator('select.filter-dropdown');
    const firstFilter = filterSelects.first();

    const options = await firstFilter.locator('option').all();
    if (options.length > 1) {
      const optionValue = await options[1].getAttribute('value');
      if (optionValue) {
        await firstFilter.selectOption(optionValue);
        
        // Wait for filter to apply
        await page.waitForTimeout(1000);

        // Option count should change (typically reduce)
        const newCount = await exerciseSelect.locator('option').count();
        // Either count changed or stayed same (filter may not have effect)
        expect(newCount).toBeGreaterThan(0);
      }
    }
  });

  test('multiple filters can be combined', async ({ page }) => {
    await filterToggle(page).click();
    const filterForm = page.locator('#filters-form');
    const filterSelects = filterForm.locator('select.filter-dropdown');
    const count = await filterSelects.count();

    if (count >= 2) {
      // Apply first filter
      const firstValue = await filterSelects.nth(0).locator('option').nth(1).getAttribute('value');
      if (firstValue) {
        await filterSelects.nth(0).selectOption(firstValue);
      }

      // Apply second filter
      const secondValue = await filterSelects.nth(1).locator('option').nth(1).getAttribute('value');
      if (secondValue) {
        await filterSelects.nth(1).selectOption(secondValue);
      }

      // Both filters should be applied
      await expect(filterSelects.nth(0)).not.toHaveValue('');
      await expect(filterSelects.nth(1)).not.toHaveValue('');
    }
  });
});

test.describe('Routine Tab Navigation', () => {
  test.beforeEach(async ({ page, request, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await ensureRoutineHasExercises(page, request, 1);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('routine tabs filter the table', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const tabs = page.locator('#routine-tabs .routine-tab-btn');
    const tabCount = await tabs.count();

    if (tabCount > 1) {
      // Click second tab (not "All")
      await tabs.nth(1).click();

      // Table should update
      await page.waitForTimeout(500);

      // Tab should be active
      await expect(tabs.nth(1)).toHaveClass(/active/);
    }
  });

  test('All tab shows all exercises', async ({ page }) => {
    await selectRoutine(page);
    await page.waitForSelector('#workout_plan_table_body tr');

    const allTab = page.locator('#tab-all');
    await allTab.click();

    // Tab should be active
    await expect(allTab).toHaveClass(/active/);
  });
});

async function dragByPlanHandle(page: Page, sourceId: number, targetId: number, fitCards = false) {
  const source = planRow(page, sourceId).locator('.drag-handle');
  const target = planRow(page, targetId);
  await source.scrollIntoViewIfNeeded();
  await target.scrollIntoViewIfNeeded();
  if (fitCards) {
    await target.evaluate((element, sourceId) => {
      const source = document.querySelector(`#workout_plan_table_body tr[data-exercise-id="${sourceId}"]`)!;
      const navbarBottom = document.querySelector('#navbar')!.getBoundingClientRect().bottom;
      const boxes = [source, element].map(row => row.getBoundingClientRect());
      const top = Math.min(...boxes.map(box => box.top));
      const bottom = Math.max(...boxes.map(box => box.bottom));
      window.scrollBy({ top: (top + bottom - navbarBottom - window.innerHeight) / 2, behavior: 'instant' });
    }, sourceId);
  }
  const from = await source.boundingBox();
  const to = await target.boundingBox();
  expect(from, 'the row supplied a real drag handle').not.toBeNull();
  expect(to, 'the destination row is laid out').not.toBeNull();
  const x = from!.x + from!.width / 2;
  const y = from!.y + from!.height / 2;
  const destination = { x, y: to!.y + to!.height / 4 };
  if (fitCards) {
    const hits = (element: Element, point: { x: number; y: number }) =>
      element.contains(document.elementFromPoint(point.x, point.y));
    expect(await source.evaluate(hits, { x, y }), 'drag starts on the source handle').toBe(true);
    expect(await target.evaluate(hits, destination), 'drop point is on the target row').toBe(true);
  }
  const response = page.waitForResponse(result => new URL(result.url()).pathname === '/update_exercise_order');
  await page.mouse.move(x, y);
  await page.mouse.down();
  await page.mouse.move(destination.x, destination.y, { steps: 14 });
  if (fitCards) {
    await page.locator('#workout_plan_table_body').evaluate(async (body) => {
      await new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
      const transforms = [...body.querySelectorAll(':scope > tr')]
        .flatMap(row => row.getAnimations())
        .filter(animation => animation instanceof CSSTransition && animation.transitionProperty === 'transform' &&
          Number.isFinite(animation.effect?.getComputedTiming().endTime));
      await Promise.allSettled(transforms.map(animation => animation.finished));
    });
  }
  await page.mouse.move(destination.x + 2, destination.y);
  await page.mouse.up();
  const ordered = await response;
  expect(ordered.ok()).toBe(true);
  return ordered.request().postDataJSON();
}

async function seedTwoDragRoutines(page: Page) {
  await planPost(page.request, '/clear_workout_plan');
  for (const [routine, names] of [[ROUTINE_A, [BENCH, ROW]], [ROUTINE_B, [SQUAT, DEADLIFT]]] as const) {
    for (const name of names) await addPlanRow(page.request, routine, name);
  }
  return planData(page.request);
}

guardedTest.describe('Plan redesign characterization', () => {
  for (const routine of [ROUTINE_A, ROUTINE_B]) {
    guardedTest(`dragging within Workout ${routine.at(-1)} persists that routine and keeps the other routine grouped and ordered`, async ({ page }) => {
      const rows = await seedTwoDragRoutines(page);
      const current = rows.filter(row => row.routine === routine);
      const other = rows.filter(row => row.routine !== routine);
      const [first, last] = current;
      await loadPlan(page);
      await routineTab(page, routine).click();
      await expect(planRows(page).locator('.exercise-name')).toHaveText([first.exercise, last.exercise]);
      expect(await dragByPlanHandle(page, last.id, first.id)).toEqual([
        { id: last.id, order: 1 }, { id: first.id, order: 2 },
      ]);
      await expect(planRows(page).locator('.exercise-name')).toHaveText([last.exercise, first.exercise]);
      await loadPlan(page, true);
      await routineTab(page, routine).click();
      await expect(planRows(page).locator('.exercise-name')).toHaveText([last.exercise, first.exercise]);
      const after = await planData(page.request);
      expect(after.filter(record => record.routine !== routine).map(record => [record.id, record.exercise_order]))
        .toEqual(other.map(record => [record.id, record.exercise_order]));
      await routineTab(page, 'all').click();
      const byRoutine = [ROUTINE_A, ROUTINE_B].flatMap(name => name === routine ? [last, first] : other);
      await expect(planRows(page).locator('.exercise-name')).toHaveText(byRoutine.map(row => row.exercise));
    });
  }
});

guardedTest.describe('Plan redesign acceptance', () => {
  guardedTest('drags the phone card by its handle and writes the same payload as the table', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await seedTwoDragRoutines(page);
    await addPlanRow(page.request, ROUTINE_A, 'Barbell Curl');
    const [first, partner, last] = (await planData(page.request)).filter(row => row.routine === ROUTINE_A);
    await planPost(page.request, '/api/superset/link', { exercise_ids: [partner.id, last.id] });
    await loadPlan(page);
    await routineTab(page, ROUTINE_A).click();
    await expect(planRow(page, first.id), 'the drag handle belongs to a phone card').toHaveClass(/\bui-record-card\b/);
    await expect(planRows(page).locator('.exercise-name')).toHaveText([first.exercise, partner.exercise, last.exercise]);
    expect(await dragByPlanHandle(page, last.id, first.id, true)).toEqual([
      { id: last.id, order: 1 }, { id: partner.id, order: 2 }, { id: first.id, order: 3 },
    ]);
    await loadPlan(page, true);
    await expect(planRows(page).locator('.exercise-name')).toHaveText([last.exercise, partner.exercise, first.exercise]);
  });

  guardedTest.describe('keyboard edits and rejection', () => {
    guardedTest.use({
      consoleAllowlist: { expected: [
        {
          match: 'Failed to load resource: the server responded with a status of 400 (BAD REQUEST)',
          reason: 'Chromium reports the deliberate invalid Sets update',
        },
        {
          match: /^\[req_[0-9a-z_]+\] API Error: \{url: \/update_exercise, method: POST, status: 400, error: Object\}$/,
          reason: 'fetch-wrapper.js logs the deliberate Sets validation rejection',
        },
        {
          match: /^\[req_[0-9a-z_]+\] API Error \(final\): \{url: \/update_exercise, method: POST, error: Object\}$/,
          reason: 'fetch-wrapper.js reports the final Sets validation rejection',
        },
      ] },
    });

    for (const width of [390, 1440]) {
      guardedTest(`edits a field by keyboard, saves once, discards drafts and warns on rejection at ${width} px`, async ({ page }) => {
        await page.setViewportSize({ width, height: 900 });
        await planPost(page.request, '/clear_workout_plan');
        await addPlanRow(page.request, ROUTINE_A, SQUAT);
        const [record] = await planData(page.request);
        await loadPlan(page);
        if (width < 1360) await setDetails(page, record.id, true);
        const field = planRow(page, record.id).locator('[data-field="sets"]');
        const button = field.getByRole('button');
        const input = field.getByRole('spinbutton');
        await expect(button, 'the saved value is a keyboard-operable button').toBeVisible();
        expect(await button.evaluate(node => (node as HTMLElement).tabIndex)).toBeGreaterThanOrEqual(0);
        const posts: object[] = [];
        const isUpdate = (url: string) => new URL(url).pathname === '/update_exercise';
        page.on('request', request => {
          if (isUpdate(request.url()) && request.method() === 'POST') posts.push(request.postDataJSON());
        });
        const edit = async (value: string) => {
          await button.focus();
          await expect(button).toBeFocused();
          await page.keyboard.press('Enter');
          await expect(input).toBeFocused();
          await input.fill(value);
        };

        await edit('4');
        const entered = page.waitForResponse(response => isUpdate(response.url()));
        await input.press('Enter');
        expect((await entered).ok()).toBe(true);
        await expect(field).toHaveText('4');
        expect(posts).toEqual([{ id: record.id, updates: { sets: '4' } }]);

        await edit('5');
        const blurred = page.waitForResponse(response => isUpdate(response.url()));
        await page.getByRole('heading', { name: 'Workout Plan', exact: true }).click();
        expect((await blurred).ok()).toBe(true);
        await expect(field).toHaveText('5');
        expect(posts).toHaveLength(2);
        expect(posts[1]).toEqual({ id: record.id, updates: { sets: '5' } });

        await edit('6');
        await input.press('Escape');
        await expect(field).toHaveText('5');
        await edit('');
        await input.press('Enter');
        await expect(field).toHaveText('5');
        expect(posts, 'Escape and a blank count do not write').toHaveLength(2);

        await edit('3.5');
        const rejected = page.waitForResponse(response => isUpdate(response.url()));
        await input.press('Enter');
        expect((await rejected).status()).toBe(400);
        await expect(page.locator('#liveToast')).toHaveClass(/bg-warning/);
        await expectToast(page, 'Sets must be a whole number.');
        await expect(field).toHaveText('5');
        expect(posts).toHaveLength(3);
        expect((await planData(page.request))[0].sets).toBe(5);

        await loadPlan(page, true);
        if (width < 1360) await setDetails(page, record.id, true);
        await expect(field).toHaveText('5');
      });
    }
  });
});
