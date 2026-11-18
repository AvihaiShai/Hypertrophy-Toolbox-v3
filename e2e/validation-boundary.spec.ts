/**
 * E2E Test: Input Validation Boundaries
 * 
 * Tests form validation for edge cases and boundary values:
 * - Negative numbers for reps/sets/weight
 * - Min rep > Max rep validation
 * - RIR/RPE maximum value enforcement
 * - Zero and empty value handling
 * - Decimal/float handling
 */
import type { Page } from '@playwright/test';
import { test, expect, ROUTES, SELECTORS, expectToast, waitForWorkoutPlanReady, resetWorkoutPlan } from './fixtures';

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
 * Helper to select an exercise from dropdown
 */
async function selectExercise(page: import('@playwright/test').Page) {
  await page.waitForFunction(() => {
    const select = document.getElementById('exercise') as HTMLSelectElement;
    return select && select.options.length > 1;
  });
  
  const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
  const options = await exerciseSelect.locator('option').allInnerTexts();
  const validExercise = options.find(opt => opt && opt.trim() !== '' && !opt.includes('Select'));
  if (validExercise) {
    await exerciseSelect.selectOption(validExercise);
    // Selecting an exercise starts the profile-estimate fetch, and its response
    // overwrites the six Workout Controls. Every test below types into those
    // fields next, so it has to land first or it lands on top of the input.
    await waitForWorkoutPlanReady(page);
  }
}

async function expectExerciseSubmission(
  page: Page,
  expectedStatus: number,
  expectedPayload: Record<string, number | string>,
  expectedError?: string,
) {
  const rows = page.locator('#workout_plan_table_body tr');
  const initialCount = await rows.count();
  const initialPlan = expectedError ? await readPlanEntries(page) : undefined;
  const responsePromise = page.waitForResponse(response =>
    response.url().endsWith('/add_exercise') && response.request().method() === 'POST'
  );

  await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();
  const response = await responsePromise;

  expect(response.status()).toBe(expectedStatus);
  expect(response.request().postDataJSON()).toMatchObject(expectedPayload);
  if (expectedStatus === 200) {
    await expect.poll(() => rows.count()).toBe(initialCount + 1);
  } else {
    if (expectedError) {
      expect(await response.json()).toMatchObject({
        ok: false,
        error: { code: 'VALIDATION_ERROR', message: expectedError },
      });
      await expectToast(page, expectedError);
      expect(await readPlanEntries(page)).toEqual(initialPlan);
    }
    await expect.poll(() => rows.count()).toBe(initialCount);
  }
}

async function readPlanEntries(page: Page): Promise<Array<{ sets: number }>> {
  const response = await page.request.get('/get_workout_plan');
  expect(response.ok()).toBeTruthy();
  return (await response.json()).data;
}

const countInputSelectors = { sets: '#sets', min_rep_range: '#min_rep', max_rep_range: '#max_rep_range' };

async function expectRejectedCount(
  page: Page, field: keyof typeof countInputSelectors, value: string, message: string,
) {
  await page.fill('#sets', '3');
  await page.fill('#min_rep', '8');
  await page.fill('#max_rep_range', '12');
  await page.fill('#weight', '100');

  const input = page.locator(countInputSelectors[field]);
  await input.fill(value);
  await expect(input).toHaveValue(value);
  await input.blur();
  await expect(input).toHaveValue(value);
  await expectExerciseSubmission(page, 400, { [field]: value }, message);
}

test.beforeEach(async ({ page }) => {
  await resetWorkoutPlan(page);
});

test.describe('Negative Value Validation', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
    await selectExercise(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('rejects negative sets without clamping', async ({ page }) => {
    await expectRejectedCount(page, 'sets', '-1', 'Sets must be at least 1.');
  });

  test('rejects negative min reps without clamping', async ({ page }) => {
    await expectRejectedCount(page, 'min_rep_range', '-5', 'Minimum reps must be at least 1.');
  });

  test('rejects negative max rep value', async ({ page }) => {
    await expectRejectedCount(page, 'max_rep_range', '-10', 'Maximum reps must be at least 1.');
  });

  test('clamps negative weight to zero', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '-50');

    await expectExerciseSubmission(page, 200, { weight: 0 });
  });
});

test.describe('Rep Range Validation', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
    await selectExercise(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('rejects min rep greater than max rep', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '15');  // Min > Max
    await page.fill('#max_rep_range', '8');
    await page.fill('#weight', '100');

    await expectExerciseSubmission(page, 400, {
      min_rep_range: '15',
      max_rep_range: '8',
    });
  });

  test('accepts valid rep range (min < max)', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');

    await expectExerciseSubmission(page, 200, {
      min_rep_range: '8',
      max_rep_range: '12',
    });
  });

  test('accepts equal min and max rep (min == max)', async ({ page }) => {
    await page.fill('#sets', '5');
    await page.fill('#min_rep', '5');  // Fixed rep count
    await page.fill('#max_rep_range', '5');
    await page.fill('#weight', '100');

    await expectExerciseSubmission(page, 200, {
      min_rep_range: '5',
      max_rep_range: '5',
    });
  });
});

test.describe('Zero Value Validation', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
    await selectExercise(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('rejects zero sets without clamping', async ({ page }) => {
    await expectRejectedCount(page, 'sets', '0', 'Sets must be at least 1.');
  });

  test('rejects zero min reps without clamping', async ({ page }) => {
    await expectRejectedCount(page, 'min_rep_range', '0', 'Minimum reps must be at least 1.');
  });

  test('rejects zero max reps without clamping', async ({ page }) => {
    await expectRejectedCount(page, 'max_rep_range', '0', 'Maximum reps must be at least 1.');
  });

  test('accepts zero weight for bodyweight or assisted exercise', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '0');

    await expectExerciseSubmission(page, 200, { weight: 0 });
  });
});

test.describe('RIR/RPE Value Validation', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
    await selectExercise(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('rejects RIR greater than 10', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');
    
    const rirField = page.locator('#rir');
    if (await rirField.isVisible()) {
      await rirField.fill('15');  // RIR > 10 doesn't make sense
    }

    await expectExerciseSubmission(page, 200, { rir: 10 });
  });

  test('rejects negative RIR', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');
    
    const rirField = page.locator('#rir');
    if (await rirField.isVisible()) {
      await rirField.fill('-2');
    }

    await expectExerciseSubmission(page, 200, { rir: 0 });
  });

  test('rejects RPE greater than 10', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');
    
    const rpeField = page.locator('#rpe');
    if (await rpeField.isVisible()) {
      await rpeField.fill('12');  // RPE scale is 1-10
    }

    await expectExerciseSubmission(page, 200, { rpe: 10 });
  });

  test('accepts valid RIR value (0-4 typical range)', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');
    
    const rirField = page.locator('#rir');
    if (await rirField.isVisible()) {
      await rirField.fill('2');
    }

    await expectExerciseSubmission(page, 200, { rir: 2 });
  });
});

test.describe('Decimal/Float Value Handling', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
    await selectExercise(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('accepts decimal weight values', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '102.5');  // Decimal weight (common for kg)

    await expectExerciseSubmission(page, 200, { weight: 102.5 });
  });

  test('rejects fractional sets without rounding', async ({ page }) => {
    await expectRejectedCount(page, 'sets', '3.5', 'Sets must be a whole number.');
  });

  test('rejects fractional min reps without rounding', async ({ page }) => {
    await expectRejectedCount(page, 'min_rep_range', '8.5', 'Minimum reps must be a whole number.');
  });

  test('rejects fractional max reps without rounding', async ({ page }) => {
    await expectRejectedCount(page, 'max_rep_range', '12.5', 'Maximum reps must be a whole number.');
  });
});

test.describe('Empty Value Validation', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('rejects submission without exercise selected', async ({ page }) => {
    // Don't select exercise
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');

    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();
    await page.waitForTimeout(500);

    // Should show validation error about required exercise
    const toast = page.locator('.toast, #liveToast');
    const toastVisible = await toast.isVisible().catch(() => false);
    expect(toastVisible).toBeTruthy();
  });

  test('rejects empty sets field', async ({ page }) => {
    await selectExercise(page);
    await page.fill('#sets', '');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');

    let addRequestSent = false;
    page.on('request', request => {
      if (request.url().endsWith('/add_exercise')) addRequestSent = true;
    });
    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();
    await expect(page.locator('#liveToast')).toBeVisible();
    expect(addRequestSent).toBe(false);
  });

  test('rejects empty weight field', async ({ page }) => {
    await selectExercise(page);
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '');

    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();
    await page.waitForTimeout(500);

    const toast = page.locator('.toast, #liveToast');
    const toastVisible = await toast.isVisible().catch(() => false);
    expect(toastVisible).toBeTruthy();
  });
});

test.describe('Extreme Value Handling', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
    await selectRoutine(page);
    await selectExercise(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('handles very large sets value', async ({ page }) => {
    await page.fill('#sets', '9999');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');

    await expectExerciseSubmission(page, 200, { sets: '9999' });
  });

  test('handles very large weight value', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '50000');  // 50000 lbs = unrealistic

    await expectExerciseSubmission(page, 400, { weight: 50000 });
  });

  test('handles very large rep values', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '500');
    await page.fill('#max_rep_range', '1000');
    await page.fill('#weight', '100');

    await expectExerciseSubmission(page, 200, {
      min_rep_range: '500',
      max_rep_range: '1000',
    });
  });

  test('inline sets accept counts above the hint and keep the last saved value on rejection', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');
    await expectExerciseSubmission(page, 200, { sets: '3' });

    const cell = page.locator('#workout_plan_table_body td[data-field="sets"]');
    const input = cell.locator('input');
    const edit = async (value: string) => {
      await cell.click();
      await expect(input).toHaveAttribute('max', '10');
      await input.fill(value);
      const update = page.waitForResponse(response =>
        response.url().endsWith('/update_exercise') && response.request().method() === 'POST',
      );
      await input.press('Enter');
      const response = await update;
      expect(response.request().postDataJSON()).toMatchObject({ updates: { sets: value } });
      return response;
    };

    expect((await edit('11')).ok()).toBeTruthy();
    await expect(cell).toHaveText('11');
    const confirmedPlan = await readPlanEntries(page);
    expect(confirmedPlan).toMatchObject([{ sets: 11 }]);

    const rejected = await edit('1.5');
    expect(rejected.status()).toBe(400);
    expect(await rejected.json()).toMatchObject({ error: { code: 'VALIDATION_ERROR' } });
    await expectToast(page, 'Sets must be a whole number.');
    await expect(cell).toHaveText('11');
    expect(await readPlanEntries(page)).toEqual(confirmedPlan);
  });

  test('inline sets show the stored number and a blank edit reverts without a write', async ({ page }) => {
    await page.fill('#sets', '3');
    await page.fill('#min_rep', '8');
    await page.fill('#max_rep_range', '12');
    await page.fill('#weight', '100');
    await expectExerciseSubmission(page, 200, { sets: '3' });

    const cell = page.locator('#workout_plan_table_body td[data-field="sets"]');
    const input = cell.locator('input');

    await cell.click();
    await input.fill('08');
    const update = page.waitForResponse(response =>
      response.url().endsWith('/update_exercise') && response.request().method() === 'POST',
    );
    await input.press('Enter');
    expect((await update).ok()).toBeTruthy();
    await expect(cell).toHaveText('8');

    const writes: string[] = [];
    page.on('request', (request) => {
      if (request.url().endsWith('/update_exercise')) writes.push(request.method());
    });
    await cell.click();
    await input.fill('');
    await input.press('Enter');
    await expect(input).toHaveCount(0);
    await expect(cell).toHaveText('8');
    expect(await readPlanEntries(page)).toMatchObject([{ sets: 8 }]);
    expect(writes).toEqual([]);
  });
});
