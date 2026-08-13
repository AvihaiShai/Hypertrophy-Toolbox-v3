/**
 * E2E Test: Superset Edge Cases
 * 
 * Tests superset functionality edge cases:
 * - Delete exercise that's part of superset
 * - Unlink from superset chain
 * - Replace exercise in superset
 * - Linking more than 2 exercises
 * - Superset state persistence
 */
import {
  test,
  expect,
  ROUTES,
  SELECTORS,
  waitForWorkoutPlanReady,
  API_ENDPOINTS,
  expectToast,
  resetWorkoutPlan,
} from './fixtures';

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

/**
 * Helper to add an exercise to the plan
 */
async function addExercise(page: import('@playwright/test').Page, exerciseName?: string) {
  await page.waitForFunction(() => {
    const select = document.getElementById('exercise') as HTMLSelectElement;
    return select && select.options.length > 1;
  });
  
  const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
  const options = await exerciseSelect.locator('option').allInnerTexts();
  const usedExercises = new Set(
    (await page.locator('#workout_plan_table_body .exercise-name').allInnerTexts())
      .map(text => text.trim().toLowerCase())
      .filter(Boolean)
  );
  
  let targetExercise: string | undefined;
  if (exerciseName) {
    targetExercise = options.find(opt => opt.toLowerCase().includes(exerciseName.toLowerCase()));
  }
  if (!targetExercise) {
    targetExercise = options.find(opt => {
      const normalized = opt.trim().toLowerCase();
      return normalized !== '' && !opt.includes('Select') && !usedExercises.has(normalized);
    });
  }
  if (!targetExercise) {
    targetExercise = options.find(opt => opt && opt.trim() !== '' && !opt.includes('Select'));
  }
  
  expect(targetExercise, 'an unused exercise option should be available').toBeTruthy();
  await exerciseSelect.selectOption({ label: targetExercise! });
  
  await page.fill('#sets', '3');
  await page.fill('#min_rep', '8');
  await page.fill('#max_rep_range', '12');
  await page.fill('#weight', '100');
  
  const rowCountBefore = await page.locator('#workout_plan_table_body tr').count();
  const responsePromise = page.waitForResponse(response =>
    response.url().includes(API_ENDPOINTS.ADD_EXERCISE) &&
    response.request().method() === 'POST'
  );
  await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();
  const response = await responsePromise;
  expect(response.status()).toBe(200);
  await expect(page.locator('#workout_plan_table_body tr')).toHaveCount(rowCountBefore + 1);
}

/**
 * Helper to wait for exercises in table
 */
async function waitForExercisesInTable(page: import('@playwright/test').Page, minCount: number = 1) {
  await page.waitForFunction(
    (min) => document.querySelectorAll('#workout_plan_table_body tr').length >= min,
    minCount,
    { timeout: 5000 }
  );
}

/** Rows the app has marked as belonging to a superset. */
const SUPERSET_ROWS =
  '#workout_plan_table_body tr[data-superset-group]:not([data-superset-group=""])';

function supersetRows(page: import('@playwright/test').Page) {
  return page.locator(SUPERSET_ROWS);
}

/**
 * Select the first `count` superset checkboxes, asserting that many rows exist.
 *
 * The precondition is asserted rather than guarded. These tests used to wrap
 * their whole body in `if (await checkboxes.count() >= 2)`, so a plan that
 * failed to load reported a pass having exercised nothing. A missing row is now
 * a failure that names what was missing.
 */
async function selectExerciseCheckboxes(page: import('@playwright/test').Page, count: number) {
  const checkboxes = page.locator('#workout_plan_table_body .superset-checkbox');
  await expect(checkboxes, `${count} exercise row(s) should be selectable`).toHaveCount(count);
  for (let index = 0; index < count; index++) {
    await checkboxes.nth(index).click();
  }
  return checkboxes;
}

/**
 * Click "Link Superset" for the two selected exercises and wait for the linked
 * rows to be on screen.
 *
 * Waiting for the POST alone is not enough. `handleLinkSuperset()` awaits
 * /api/superset/link and only then calls `refreshPlan()`, so the rows re-render
 * on a *second* round trip; a test that continued at the POST would race that
 * re-render. The fixed 1000ms sleep this replaces was covering both hops, so
 * both are waited for here.
 *
 * The button being enabled is asserted here, not tested for by the callers. It
 * used to be an `if`, which meant "the app would not let us build a superset"
 * and "the superset behaved correctly" were the same green result.
 */
async function linkSelectedExercises(page: import('@playwright/test').Page) {
  const linkBtn = page.locator('#link-superset-btn');
  await expect(linkBtn, 'two same-routine exercises should be linkable').toBeEnabled();
  const linked = page.waitForResponse(response =>
    response.url().endsWith(API_ENDPOINTS.SUPERSET_LINK) && response.request().method() === 'POST'
  );
  await linkBtn.click();
  await linked;
  await expect(supersetRows(page)).toHaveCount(2);
}

test.beforeEach(async ({ page }) => {
  await resetWorkoutPlan(page);
});

test.describe('Superset Linking Edge Cases', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('rejects linking more than 2 exercises', async ({ page }) => {
    // Add 3 exercises
    await addExercise(page, 'bench');
    await addExercise(page, 'squat');
    await addExercise(page, 'deadlift');
    
    await waitForExercisesInTable(page, 3);

    await selectExerciseCheckboxes(page, 3);
    await page.waitForTimeout(300);

    // Three selected must be refused, and the copy must say why.
    await expect(page.locator('#superset-selection-info')).toContainText(
      'supersets can only have 2 exercises'
    );
    await expect(page.locator('#link-superset-btn')).toBeDisabled();
  });

  test('rejects linking only 1 exercise', async ({ page }) => {
    await addExercise(page);
    await waitForExercisesInTable(page, 1);

    await selectExerciseCheckboxes(page, 1);
    await page.waitForTimeout(300);

    await expect(page.locator('#superset-selection-info')).toContainText(
      'select 1 more to create superset'
    );
    await expect(page.locator('#link-superset-btn')).toBeDisabled();
  });

  test('successfully links exactly 2 exercises', async ({ page }) => {
    await addExercise(page, 'bench');
    await addExercise(page, 'row');
    await waitForExercisesInTable(page, 2);
    
    const checkboxes = page.locator('#workout_plan_table_body .superset-checkbox');
    await expect(checkboxes).toHaveCount(2);
    await checkboxes.nth(0).click();
    await checkboxes.nth(1).click();

    const linkBtn = page.locator('#link-superset-btn');
    await expect(linkBtn).toBeEnabled();
    const responsePromise = page.waitForResponse(response =>
      response.url().endsWith('/api/superset/link') && response.request().method() === 'POST'
    );
    await linkBtn.click();
    expect((await responsePromise).status()).toBe(200);

    const linkedRows = page.locator(
      '#workout_plan_table_body tr[data-superset-group]:not([data-superset-group=""])'
    );
    await expect(linkedRows).toHaveCount(2);
  });
});

test.describe('Delete Exercise in Superset', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('deleting one exercise from superset breaks the link', async ({ page }) => {
    // Add and link 2 exercises
    await addExercise(page, 'bench');
    await addExercise(page, 'row');
    await waitForExercisesInTable(page, 2);

    await selectExerciseCheckboxes(page, 2);
    await page.waitForTimeout(300);
    await linkSelectedExercises(page);

    // Now delete one exercise
    const rows = page.locator('#workout_plan_table_body tr');
    const deleteBtn = rows.first().locator('button[data-action="delete"], .delete-btn, .btn-danger');
    await expect(deleteBtn).toBeVisible();
    await deleteBtn.click();
    await page.waitForTimeout(1000);

    // The named behavior: the link is gone, not merely the row.
    await expect(rows).toHaveCount(1);
    await expect(supersetRows(page)).toHaveCount(0);
  });

  test('deleting a linked exercise clears the partner superset group', async ({ page }) => {
    await addExercise(page);
    await addExercise(page);
    await waitForExercisesInTable(page, 2);
    
    // Link exercises first
    await selectExerciseCheckboxes(page, 2);
    await linkSelectedExercises(page);

    // Deleting one member unlinks the remaining partner server-side.
    const deleteBtn = page.locator('#workout_plan_table_body tr').first().locator('button[data-action="delete"], .delete-btn, .btn-danger');
    await expect(deleteBtn).toBeVisible();
    const responsePromise = page.waitForResponse(response =>
      response.url().endsWith('/remove_exercise') && response.request().method() === 'POST'
    );
    await deleteBtn.click();
    expect((await responsePromise).status()).toBe(200);
    await expect(page.locator('#workout_plan_table_body tr')).toHaveCount(1);
    await expect(page.locator('#workout_plan_table_body tr').first()).not.toHaveAttribute(
      'data-superset-group'
    );
  });
});

test.describe('Unlink Superset Edge Cases', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('unlink button only shows for superset exercises', async ({ page }) => {
    await addExercise(page);
    await waitForExercisesInTable(page, 1);

    // Select a non-superset exercise.
    await selectExerciseCheckboxes(page, 1);
    await page.waitForTimeout(300);

    const unlinkBtn = page.locator('#unlink-superset-btn');

    // Rendered state, not the app's intent. Asserting `el.style.display` only
    // proved `updateSupersetActionButtons()` had made the right decision; three
    // `!important` display rules in components.css then outranked that inline
    // style and the user saw the button anyway. `toBeHidden()` is the assertion
    // that fails if the cascade wins again.
    await expect(
      unlinkBtn,
      'unlink must not be rendered for a non-superset selection'
    ).toBeHidden();
    await expect(page.locator('#superset-selection-info')).toContainText(
      'select 1 more to create superset'
    );

    // Defence in depth: `handleUnlinkSuperset()` refuses a selection that is in
    // no superset. Dispatched straight at the hidden button (a real click would
    // fail actionability), it must post nothing and change nothing.
    let unlinkRequests = 0;
    page.on('request', request => {
      if (request.url().endsWith(API_ENDPOINTS.SUPERSET_UNLINK)) unlinkRequests++;
    });
    await unlinkBtn.dispatchEvent('click');
    await expectToast(page, 'Please select an exercise that is part of a superset');
    expect(unlinkRequests, 'the guard must not reach the unlink endpoint').toBe(0);
    await expect(page.locator('#workout_plan_table_body tr')).toHaveCount(1);
    await expect(supersetRows(page)).toHaveCount(0);
  });

  test('unlink shows for selected superset exercise', async ({ page }) => {
    await addExercise(page);
    await addExercise(page);
    await waitForExercisesInTable(page, 2);
    
    // Create superset
    const checkboxes = await selectExerciseCheckboxes(page, 2);
    await linkSelectedExercises(page);

    // Now select one of the superset exercises
    await checkboxes.nth(0).click();
    await page.waitForTimeout(300);

    // Unlink should now be visible, and Link — which this selection cannot use —
    // hidden. Both directions of the same toggle, so a fix that hid everything
    // would fail here.
    const unlinkBtn = page.locator('#unlink-superset-btn');
    await expect(unlinkBtn).toBeVisible();
    await expect(unlinkBtn).toBeEnabled();
    await expect(page.locator('#link-superset-btn')).toBeHidden();
  });

  test('unlink clears both exercises from superset', async ({ page }) => {
    await addExercise(page);
    await addExercise(page);
    await waitForExercisesInTable(page, 2);
    
    // Create superset
    await selectExerciseCheckboxes(page, 2);
    await linkSelectedExercises(page);

    // Select one superset exercise
    const refreshedCheckboxes = page.locator('#workout_plan_table_body .superset-checkbox');
    await refreshedCheckboxes.nth(0).click();
    await page.waitForTimeout(300);

    // Click unlink
    const unlinkBtn = page.locator('#unlink-superset-btn');
    await expect(unlinkBtn).toBeVisible();
    await expect(unlinkBtn).toBeEnabled();
    const responsePromise = page.waitForResponse(response =>
      response.url().endsWith(API_ENDPOINTS.SUPERSET_UNLINK) && response.request().method() === 'POST'
    );
    await unlinkBtn.click();
    expect((await responsePromise).status()).toBe(200);
    // Both partners clear, not just the one that was selected.
    await expect(supersetRows(page)).toHaveCount(0);
  });
});

test.describe('Replace Exercise in Superset', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('replace exercise in superset preserves or clears superset', async ({ page }) => {
    // Named exercises on purpose: the catalog's first unused options are stretch
    // variations with no muscle-group or equipment metadata, and /replace_exercise
    // rejects those with 400 `missing_metadata`. That path is owned by
    // replace-exercise-errors.spec.ts; this test is about the superset invariant,
    // so it needs a member that can actually be swapped.
    await addExercise(page, 'bench');
    await addExercise(page, 'row');
    await waitForExercisesInTable(page, 2);
    
    // Create superset
    await selectExerciseCheckboxes(page, 2);
    await linkSelectedExercises(page);

    // Replace the first exercise. `handleSwapExercise()` posts straight to
    // /replace_exercise -- there is no picker to drive.
    const replaceBtn = page.locator('#workout_plan_table_body tr').first()
      .locator('button[data-action="replace"], .replace-btn, .btn-swap, [title*="Replace"]');
    await expect(replaceBtn.first()).toBeVisible();

    const replaced = page.waitForResponse(response =>
      response.url().endsWith('/replace_exercise') && response.request().method() === 'POST'
    );
    await replaceBtn.first().click();
    // A "no candidates" outcome is a deliberate 200 + ok:false, so either result
    // is a completed request (see CLAUDE.md, response-contract exceptions).
    expect((await replaced).status()).toBe(200);
    await page.waitForTimeout(1500);

    // Measured: the swap succeeds and the group survives it (2 rows still linked).

    // The named behavior: whichever way the swap resolves, the pair must not be
    // left half-linked. Two rows still in the group, or none -- never one.
    await expect(page.locator('#workout_plan_table_body tr')).toHaveCount(2);
    expect(
      [0, 2],
      'a replaced superset member must leave the group intact or fully cleared'
    ).toContain(await supersetRows(page).count());
  });
});

test.describe('Superset State Persistence', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('superset persists after page refresh', async ({ page }) => {
    await addExercise(page);
    await addExercise(page);
    await waitForExercisesInTable(page, 2);
    
    // Create superset
    await selectExerciseCheckboxes(page, 2);
    await linkSelectedExercises(page);

    // Refresh page
    await page.reload();
    await waitForWorkoutPlanReady(page);

    // Re-select routine to load table
    await selectRoutine(page);
    await waitForExercisesInTable(page, 2);

    // Check that superset styling/attributes are preserved
    await expect(supersetRows(page)).toHaveCount(2);
  });

  /**
   * Renamed back: the selection clears by owner decision (2026-08-13). The
   * routine dropdown still targets only the Add form, so the rows stay put and
   * only the transient selection drops.
   *
   * Asserts `#superset-actions` rather than the link button's `disabled`: the
   * template ships that button disabled, so asserting it passes on an untouched
   * page, and it is *enabled* whenever the last selection was a linkable pair.
   */
  test('changing the routine day clears a transient superset selection', async ({ page }) => {
    // Order matters: selectExerciseCheckboxes() asserts against *all* rows, so
    // the pair has to be linked before the third row exists.
    await addExercise(page);
    await addExercise(page);
    await waitForExercisesInTable(page, 2);
    await selectExerciseCheckboxes(page, 2);
    await linkSelectedExercises(page);

    await addExercise(page);
    await waitForExercisesInTable(page, 3);

    const rowsBefore = await page.locator('#workout_plan_table_body tr').count();
    const namesBefore = await page
      .locator('#workout_plan_table_body .exercise-name')
      .allInnerTexts();

    // The transient selection lands on a row that IS part of the linked pair,
    // deliberately. That is the case where the sweep could do damage: those rows
    // also carry `superset-group-N` and the first/last edge classes, so a
    // `className` clobber would strip a persisted superset's styling while
    // leaving `data-superset-group` intact — invisible to an attribute-based
    // assertion. It also drives the `hasExistingSuperset` branch, which is what
    // leaves `unlinkBtn.hidden = false` behind for the reset to restore.
    const linkedCheckbox = supersetRows(page).first().locator('.superset-checkbox');
    await linkedCheckbox.click();

    const actions = page.locator('#superset-actions');
    const info = page.locator('#superset-selection-info');
    const checked = page.locator('#workout_plan_table_body .superset-checkbox:checked');

    // Pin the pre-state, or every post-assertion below is a tautology.
    await expect(checked).toHaveCount(1);
    await expect(actions).toBeVisible();
    await expect(page.locator('#workout_plan_table_body tr.superset-selected')).toHaveCount(1);

    // Nothing may reach the superset endpoints across the routine change.
    let supersetRequests = 0;
    page.on('request', request => {
      const url = request.url();
      if (
        url.endsWith(API_ENDPOINTS.SUPERSET_LINK) ||
        url.endsWith(API_ENDPOINTS.SUPERSET_UNLINK)
      ) {
        supersetRequests++;
      }
    });

    // A real second day, not the placeholder option.
    const daySelect = page.locator(SELECTORS.ROUTINE_DAY);
    const options = await daySelect.locator('option').allInnerTexts();
    const differentDay = options.find(
      opt => opt.trim() !== '' && opt !== 'Workout A' && !opt.includes('Select')
    );
    expect(differentDay, 'the routine needs a second real day to switch to').toBeTruthy();
    await daySelect.selectOption(differentDay!);

    await expect(checked).toHaveCount(0);
    // ...and not because the table emptied.
    await expect(page.locator('#workout_plan_table_body .superset-checkbox')).toHaveCount(3);
    await expect(page.locator('#workout_plan_table_body tr.superset-selected')).toHaveCount(0);
    await expect(actions).toBeHidden();
    await expect(info).toHaveText('');
    expect(
      await info.evaluate(element => (element as HTMLElement).style.color),
      'the inline info colour must not survive the reset',
    ).toBe('');

    // The action bar is back at the template's rest state, not merely hidden:
    // a not-hidden Unlink parked inside a display:none container is the shape
    // of the defect #317 closed.
    await expect(page.locator('#unlink-superset-btn')).toHaveAttribute('hidden', '');
    await expect(page.locator('#link-superset-btn')).toBeDisabled();

    // The id Set really was cleared: a fresh click reads as the first, not the
    // second, selection.
    await linkedCheckbox.click();
    await expect(info).toContainText('1 exercise selected');
    await expect(actions).toBeVisible();

    expect(supersetRequests, 'a UI reset must not call the superset API').toBe(0);
    await expect(supersetRows(page)).toHaveCount(2);
    // The colour/edge classes survive too: a `className` clobber would strip
    // them and leave the data attribute intact.
    await expect(supersetRows(page).first()).toHaveClass(/superset-group/);

    // Which rows are displayed is unchanged — the other half of the owner lock.
    await expect(page.locator('#workout_plan_table_body tr')).toHaveCount(rowsBefore);
    expect(
      await page.locator('#workout_plan_table_body .exercise-name').allInnerTexts(),
    ).toEqual(namesBefore);

    // Server state, not just the un-rerendered DOM: the routine change does not
    // refetch the plan, so the attributes above would survive a covert unlink.
    const plan = await page.request.get('/get_workout_plan');
    expect(plan.ok()).toBeTruthy();
    const payload = await plan.json();
    const groups = (payload.data ?? payload)
      .map((row: Record<string, unknown>) => row.superset_group)
      .filter(Boolean);
    expect(groups, 'the linked pair must still be linked on the server').toHaveLength(2);
    expect(new Set(groups).size, 'both rows share one superset group').toBe(1);
  });

  test('an incomplete cascade keeps the selection; completing it clears', async ({ page }) => {
    // The environment and program legs write an EMPTY composite routine
    // (routine-cascade.js updateCompositeRoutineValue), and the reset is guarded
    // on a non-empty value. So the selection survives a half-finished cascade
    // and drops only once the Add form targets a real routine again. This pins
    // the guard from both sides.
    await addExercise(page);
    await waitForExercisesInTable(page, 1);
    await selectExerciseCheckboxes(page, 1);

    const checked = page.locator('#workout_plan_table_body .superset-checkbox:checked');
    await expect(checked).toHaveCount(1);

    await page.locator(SELECTORS.ROUTINE_ENV).selectOption('Home Workout');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-program') as HTMLSelectElement;
      return select && select.options.length > 1;
    });
    await expect(checked, 'an empty composite routine is not a routine change').toHaveCount(1);

    await page.locator(SELECTORS.ROUTINE_PROGRAM).selectOption('Full Body');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-day') as HTMLSelectElement;
      return select && select.options.length > 1;
    });
    await expect(checked).toHaveCount(1);

    // Completing the cascade gives the Add form a real target, and now it clears.
    await page.locator(SELECTORS.ROUTINE_DAY).selectOption('Workout A');

    await expect(checked).toHaveCount(0);
    await expect(page.locator('#superset-actions')).toBeHidden();
    await expect(page.locator('#workout_plan_table_body .superset-checkbox')).toHaveCount(1);
  });

  test('the selection clears before the routine fetch settles', async ({ page }) => {
    // "Immediately" is a design commitment, not a nicety: the reset runs
    // synchronously above the listener's `try`, so it cannot wait on
    // /get_routine_exercises. Every other assertion in this file auto-retries
    // and would pass just as well if the reset had been moved below that await,
    // so the request is stalled here to tell the two apart.
    await addExercise(page);
    await waitForExercisesInTable(page, 1);
    await selectExerciseCheckboxes(page, 1);

    const checked = page.locator('#workout_plan_table_body .superset-checkbox:checked');
    await expect(checked).toHaveCount(1);

    let release: () => void = () => {};
    const stalled = new Promise<void>(resolve => {
      release = resolve;
    });
    // `times: 1` so only the change under test is held, and the continue is
    // guarded because releasing races test teardown — by then the route may
    // already have been discarded, which is not a failure of anything.
    await page.route(
      '**/get_routine_exercises/**',
      async route => {
        await stalled;
        await route.continue().catch(() => {});
      },
      { times: 1 },
    );

    const daySelect = page.locator(SELECTORS.ROUTINE_DAY);
    const options = await daySelect.locator('option').allInnerTexts();
    const differentDay = options.find(
      opt => opt.trim() !== '' && opt !== 'Workout A' && !opt.includes('Select')
    );
    expect(differentDay, 'the routine needs a second real day to switch to').toBeTruthy();
    await daySelect.selectOption(differentDay!);

    // Still in flight, and the selection is already gone.
    await expect(checked).toHaveCount(0);
    await expect(page.locator('#superset-actions')).toBeHidden();

    // Await the released request rather than letting it race teardown: failing
    // against a closing page logs "Error fetching routine exercises:", which is
    // not on the collector's ignore list and would red the afterEach.
    const settled = page.waitForResponse(response =>
      response.url().includes('/get_routine_exercises/')
    );
    release();
    await settled;
  });

  test('linking clears the action bar before the plan refresh lands', async ({ page }) => {
    // Criterion 2: link and unlink use the same reset. Without this the change
    // is untestable — `refreshPlan()` reaches `updateWorkoutPlanTable()`, which
    // clears the id set and calls `updateSupersetActionButtons()` anyway, so
    // deleting the reset from `handleLinkSuperset` is invisible once the
    // refresh lands. Stalling that refresh is what separates the two.
    await addExercise(page);
    await addExercise(page);
    await waitForExercisesInTable(page, 2);
    await selectExerciseCheckboxes(page, 2);

    const actions = page.locator('#superset-actions');
    const info = page.locator('#superset-selection-info');
    await expect(actions).toBeVisible();
    await expect(info).toContainText('ready to link');

    let release: () => void = () => {};
    const stalled = new Promise<void>(resolve => {
      release = resolve;
    });
    await page.route(
      `**${API_ENDPOINTS.GET_WORKOUT_PLAN}*`,
      async route => {
        await stalled;
        await route.continue().catch(() => {});
      },
      { times: 1 },
    );

    const linked = page.waitForResponse(response =>
      response.url().endsWith(API_ENDPOINTS.SUPERSET_LINK) && response.request().method() === 'POST'
    );
    await page.locator('#link-superset-btn').click();
    await linked;

    // The refresh is still in flight and the bar is already at rest.
    await expect(actions).toBeHidden();
    await expect(info).toHaveText('');
    await expect(
      page.locator('#workout_plan_table_body .superset-checkbox:checked'),
    ).toHaveCount(0);

    const refreshed = page.waitForResponse(response =>
      response.url().includes(API_ENDPOINTS.GET_WORKOUT_PLAN)
    );
    release();
    await refreshed;
    await expect(supersetRows(page)).toHaveCount(2);
  });

  test('Clear Filters does not clear a transient superset selection', async ({ page }) => {
    // KI-005 / OWNER-4: clearing a dropdown is not a deliberate choice. Clear
    // Filters writes an empty routine (filters.js clearFilters()), and the
    // reset is guarded on a non-empty value precisely so this path is inert.
    await addExercise(page);
    await waitForExercisesInTable(page, 1);
    await selectExerciseCheckboxes(page, 1);
    await expect(page.locator('#superset-actions')).toBeVisible();

    await page.locator(SELECTORS.CLEAR_FILTERS_BTN).click();
    // Both assertions below are non-change, so they would pass against the
    // pre-click state. The toast is the last thing clearFilters() does, after
    // its own await, so waiting for it proves the handler actually ran.
    await expectToast(page, 'Filters cleared successfully');

    await expect(
      page.locator('#workout_plan_table_body .superset-checkbox:checked'),
    ).toHaveCount(1);
    await expect(page.locator('#superset-actions')).toBeVisible();
  });
});

test.describe('Superset Visual Indicators', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('linked exercises show visual superset indicator', async ({ page }) => {
    await addExercise(page);
    await addExercise(page);
    await waitForExercisesInTable(page, 2);
    
    await selectExerciseCheckboxes(page, 2);
    await linkSelectedExercises(page);

    // Both partners carry the indicator, and they share one group id.
    const rows = page.locator('#workout_plan_table_body tr');
    await expect(rows.nth(0)).toHaveAttribute('data-superset-group', /^SS-/);
    await expect(rows.nth(1)).toHaveAttribute('data-superset-group', /^SS-/);
    expect(await rows.nth(0).getAttribute('data-superset-group')).toBe(
      await rows.nth(1).getAttribute('data-superset-group')
    );
  });
});
