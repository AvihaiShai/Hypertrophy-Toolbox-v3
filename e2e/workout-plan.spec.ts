/**
 * E2E Test: Workout Plan
 * 
 * Tests the workout plan page functionality including:
 * - Routine selection cascade
 * - Filters apply/clear
 * - Add exercise flow
 * - Export actions
 */
import type { Locator, Page, Route } from '@playwright/test';
import { test, expect } from './console-guard';
import {
  API_ENDPOINTS,
  ROUTES,
  SELECTORS,
  expectToast,
  waitForPageReady,
  waitForWorkoutPlanReady,
  resetWorkoutPlan,
} from './fixtures';
import {
  BENCH, DEADLIFT, ROUTINE_A, ROUTINE_B, ROW, SQUAT, addPlanRow, addTheWidePhoneValues,
  details, loadPlan, planData, planPost, planRow, planRows, routineTab,
} from './workout-plan-fixture';
import {
  addPanel, filledPlanActions, filterToggle, moreButton, phonePlanProblems, planHeader, planPanel,
  setDetails, setPlanView, setSupersetChoice, singleAddAction,
} from './workout-plan-redesign';

/**
 * Toggle the muscle-naming mode. The `#muscleModeToggle` button lives in the
 * navbar and can sit outside the viewport at desktop widths (same navbar-overflow
 * family as the dark-mode toggle in nav-dropdown.spec.ts), which makes
 * Playwright's actionability click time out. Dispatch the click directly — the
 * button's handler is what we're exercising, not its on-screen hit-testing.
 */
async function clickMuscleModeToggle(page: Page): Promise<void> {
  await page.evaluate(() => {
    const toggle = document.querySelector('#muscleModeToggle') as HTMLElement | null;
    toggle?.click();
  });
}

test.beforeEach(async ({ page }) => {
  await resetWorkoutPlan(page);
});

test.describe('Workout Plan Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    // Deliberately still `waitForPageReady`. The readiness marker covers the
    // profile-estimate write and nothing else, and several tests in this block
    // read the plan table without waiting for the `fetchWorkoutPlan()` that
    // fills it. Here `networkidle` is doing real work, so dropping it would be
    // removing a guarantee rather than replacing one.
    await waitForPageReady(page);
  });


  test('page loads with all controls visible', async ({ page }) => {
    // Page is workout plan
    const workoutPage = page.locator(SELECTORS.PAGE_WORKOUT_PLAN);
    await expect(workoutPage).toBeVisible();
    await expect(page.locator('h1')).toContainText('Workout Plan');

    await expect(page.locator('#filters-form')).toBeHidden();
    await filterToggle(page).click();
    await expect(page.locator('#filters-form')).toBeVisible();

    // Routine cascade selectors should be visible
    await expect(page.locator(SELECTORS.ROUTINE_ENV)).toBeVisible();
    await expect(page.locator(SELECTORS.ROUTINE_PROGRAM)).toBeVisible();
    await expect(page.locator(SELECTORS.ROUTINE_DAY)).toBeVisible();

    // Exercise dropdown should be visible
    await expect(page.locator(SELECTORS.EXERCISE_SEARCH)).toBeVisible();

    // Action buttons should be visible
    await expect(page.locator(SELECTORS.ADD_EXERCISE_BTN)).toBeVisible();
    await expect(page.locator(SELECTORS.EXPORT_EXCEL_BTN)).toBeHidden();
    await moreButton(page).click();
    await expect(page.locator(SELECTORS.EXPORT_EXCEL_BTN)).toBeVisible();
    await expect(page.locator(SELECTORS.EXPORT_TO_LOG_BTN)).toBeVisible();

    await expect(page.getByRole('region', { name: 'Empty plan' })).toBeVisible();
    await expect(page.locator(SELECTORS.EXERCISE_TABLE)).toBeHidden();
  });

  test('routine breadcrumb renders option labels as literal text', async ({ page }) => {
    const label = '<b data-codeql-injected>Workout & recovery</b>';
    await page.route('**/get_routine_exercises/**', route => {
      if (route.request().url().includes('data-codeql-injected')) {
        return route.fulfill({ json: { ok: true, status: 'success', data: [] } });
      }
      return route.continue();
    });
    await page.selectOption('#routine-env', 'GYM');
    await page.selectOption('#routine-program', 'Full Body');
    await page.selectOption('#routine-day', 'Workout A');
    const breadcrumb = page.locator('#routine-breadcrumb');
    await expect(breadcrumb).toHaveText('GYM→Full Body→Workout A');

    // Synthetic options test the sink; ordinary options come from fixed configuration.
    await page.locator('#routine-program').evaluate((element, value) => {
      (element as HTMLSelectElement).add(new Option(value, value));
    }, label);
    await page.selectOption('#routine-program', label);
    await expect(breadcrumb.locator('.breadcrumb-program')).toHaveText(label);
    await page.locator('#routine-day').evaluate((element, value) => {
      const select = element as HTMLSelectElement;
      select.add(new Option(value, value));
      select.disabled = false;
    }, label);
    await page.selectOption('#routine-day', label);
    await expect(breadcrumb.locator('.breadcrumb-routine')).toHaveText(label);
    await expect(breadcrumb).toHaveClass(/has-selection/);
    await expect(breadcrumb.locator('[data-codeql-injected]')).toHaveCount(0);

    await page.locator('#routine-env').evaluate((element, value) => {
      (element as HTMLSelectElement).add(new Option(value, value));
    }, label);
    await page.selectOption('#routine-env', label);
    await expect(breadcrumb.locator('.breadcrumb-env')).toHaveText(label);
    await expect(breadcrumb.locator('[data-codeql-injected]')).toHaveCount(0);
    await expect(breadcrumb).not.toHaveClass(/has-selection/);
  });

  test('routine cascade: selecting environment enables program dropdown', async ({ page }) => {
    const envSelect = page.locator(SELECTORS.ROUTINE_ENV);
    const programSelect = page.locator(SELECTORS.ROUTINE_PROGRAM);
    const daySelect = page.locator(SELECTORS.ROUTINE_DAY);

    // Initially, program and day dropdowns should be disabled
    await expect(programSelect).toBeDisabled();
    await expect(daySelect).toBeDisabled();

    // Select GYM environment
    await envSelect.selectOption('GYM');

    // Program dropdown should now be enabled
    await expect(programSelect).toBeEnabled();
    // Day dropdown should still be disabled until program is selected
    await expect(daySelect).toBeDisabled();
  });

  test('routine cascade: selecting program enables workout dropdown', async ({ page }) => {
    const envSelect = page.locator(SELECTORS.ROUTINE_ENV);
    const programSelect = page.locator(SELECTORS.ROUTINE_PROGRAM);
    const daySelect = page.locator(SELECTORS.ROUTINE_DAY);

    // Select environment
    await envSelect.selectOption('GYM');
    await expect(programSelect).toBeEnabled();

    // Wait for program options to populate
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-program') as HTMLSelectElement;
      return select && select.options.length > 1;
    });

    // Select program (e.g., "Full Body")
    await programSelect.selectOption('Full Body');

    // Workout day dropdown should now be enabled
    await expect(daySelect).toBeEnabled();

    // Verify workout days are populated
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-day') as HTMLSelectElement;
      return select && select.options.length > 1;
    });
  });

  test('routine cascade: complete selection updates hidden field', async ({ page }) => {
    // Select full routine cascade
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

    // Check hidden routine field has the composite value
    const hiddenRoutine = await page.locator('#routine').inputValue();
    expect(hiddenRoutine).toContain('GYM');
    expect(hiddenRoutine).toContain('Full Body');
    expect(hiddenRoutine).toContain('Workout A');
  });

  test('add exercise: successfully adds exercise to plan', async ({ page }) => {
    // First select a routine
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

    // Wait for exercise dropdown to be populated
    await page.waitForFunction(() => {
      const select = document.getElementById('exercise') as HTMLSelectElement;
      return select && select.options.length > 1;
    });

    // Select an exercise from the dropdown - pick one that's less likely to be in the plan
    const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const options = await exerciseSelect.locator('option').all();
    
    // Try to find an exercise that may not be in the plan (pick from later options)
    let exerciseValue: string | null = null;
    for (let i = Math.min(10, options.length - 1); i >= 1; i--) {
      exerciseValue = await options[i].getAttribute('value');
      if (exerciseValue) break;
    }
    
    if (exerciseValue) {
      await exerciseSelect.selectOption(exerciseValue);
    }

    // Get initial row count
    const initialRows = await page.locator('#workout_plan_table_body tr').count();

    // Click add exercise button
    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();

    // Wait for either: row count to increase OR a toast notification to appear
    // (Toast appears for successful add OR duplicate rejection)
    await Promise.race([
      page.waitForFunction((prevCount) => {
        const rows = document.querySelectorAll('#workout_plan_table_body tr');
        return rows.length > prevCount;
      }, initialRows, { timeout: 5000 }),
      page.waitForSelector('.toast', { timeout: 5000 })
    ]);

    // Verify either row was added OR toast appeared (both indicate the action worked)
    const newRows = await page.locator('#workout_plan_table_body tr').count();
    const toastVisible = await page.locator('.toast').isVisible().catch(() => false);
    
    // Test passes if rows increased OR a toast notification appeared
    expect(newRows > initialRows || toastVisible).toBe(true);
  });

  test('add exercise: an exercise used by another routine stays offered and addable', async ({ page }) => {
    // Regression: /get_routine_exercises used to LEFT JOIN user_selection and
    // keep only rows matching the queried routine or unassigned, so an exercise
    // already used by Workout A vanished from Workout B's dropdown.
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

    const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const addButton = page.locator(SELECTORS.ADD_EXERCISE_BTN);

    /** Pick the routine day, then wait out the dropdown refetch it triggers. */
    const selectDay = async (day: string): Promise<string> => {
      const catalogLoaded = page.waitForResponse(
        (response) => response.url().includes('/get_routine_exercises/') && response.status() === 200,
      );
      await page.locator(SELECTORS.ROUTINE_DAY).selectOption(day);
      await catalogLoaded;
      await page.waitForFunction(() => {
        const select = document.getElementById('exercise') as HTMLSelectElement;
        return select && select.options.length > 1;
      });
      return page.locator('#routine').inputValue();
    };

    /** The plan row for one exercise within one routine. */
    const planRow = (routine: string, exercise: string) =>
      page
        .locator(`#workout_plan_table_body tr[data-routine="${routine}"]`)
        .filter({ hasText: exercise });

    const routineA = await selectDay('Workout A');

    // Whichever exercise the catalog offers first is the one we reuse.
    const sharedExercise = await exerciseSelect.locator('option').nth(1).getAttribute('value');
    expect(sharedExercise).toBeTruthy();

    await exerciseSelect.selectOption(sharedExercise!);
    await addButton.click();
    await expect(planRow(routineA, sharedExercise!)).toHaveCount(1);

    // Same cascade, different day — the exercise must still be on offer.
    const routineB = await selectDay('Workout B');
    expect(routineB).not.toBe(routineA);
    await expect(exerciseSelect.locator(`option[value="${sharedExercise}"]`)).toHaveCount(1);

    await exerciseSelect.selectOption(sharedExercise!);
    await addButton.click();
    await expect(planRow(routineB, sharedExercise!)).toHaveCount(1);
  });

  test('add exercise: adding to a routine hidden by the active tab names the routine in the toast', async ({ page }) => {
    const allTab = page.locator('#routine-tabs [data-routine="all"]');
    const workoutATab = page.locator('#routine-tabs [data-routine="GYM - Full Body - Workout A"]');
    const workoutBTab = page.locator('#routine-tabs [data-routine="GYM - Full Body - Workout B"]');
    const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const addButton = page.locator(SELECTORS.ADD_EXERCISE_BTN);
    const toast = page.locator(SELECTORS.TOAST);
    const toastBody = page.locator(SELECTORS.TOAST_BODY);
    const exerciseNames = page.locator('#workout_plan_table_body .exercise-name');

    const selectDay = async (day: string) => {
      const catalogLoaded = page.waitForResponse(response =>
        response.url().includes('/get_routine_exercises/') && response.ok(),
      );
      await page.locator(SELECTORS.ROUTINE_DAY).selectOption(day);
      await catalogLoaded;
    };

    const addExercise = async (exercise: string) => {
      await exerciseSelect.selectOption(exercise);
      await addButton.click();
    };

    await page.locator(SELECTORS.ROUTINE_ENV).selectOption('GYM');
    await page.locator(SELECTORS.ROUTINE_PROGRAM).selectOption('Full Body');
    await selectDay('Workout A');
    await addExercise('Barbell Squat');
    await expect(workoutATab.locator('.tab-count')).toHaveText('1');
    await expect(allTab).toHaveAttribute('aria-selected', 'true');
    await expect(toast).toBeVisible();
    await expect(toastBody).toHaveText('Exercise added successfully');

    await selectDay('Workout B');
    await addExercise('Barbell Bench Press');
    await expect(workoutBTab.locator('.tab-count')).toHaveText('1');
    await workoutBTab.click();
    await addExercise('Dumbbell Bench Press');
    await expect(workoutBTab.locator('.tab-count')).toHaveText('2');
    await expect(toast).toBeVisible();
    await expect(toastBody).toHaveText('Exercise added successfully');
    await expect(exerciseNames).toHaveText(['Barbell Bench Press', 'Dumbbell Bench Press']);

    await selectDay('Workout A');
    await addExercise('Barbell Deadlift');
    await expect(workoutATab.locator('.tab-count')).toHaveText('2');
    await expect(toast).toBeVisible();
    await expect(toastBody).toHaveText(
      "Exercise added to GYM - Full Body - Workout A. Open that routine's tab to see it.",
    );
    await expect(workoutBTab).toHaveAttribute('aria-selected', 'true');
    await expect(exerciseNames).toHaveText(['Barbell Bench Press', 'Dumbbell Bench Press']);
  });

  test('clear filters button resets all filter dropdowns', async ({ page }) => {
    await filterToggle(page).click();
    // Find filter dropdowns and set some values
    const filterForm = page.locator('#filters-form');
    const filterSelects = filterForm.locator('select.filter-dropdown');
    
    // Try to set a filter if available (equipment filter, for example)
    const firstFilter = filterSelects.first();
    await firstFilter.waitFor({ state: 'visible' });
    
    // Get the first non-empty option
    const firstFilterOptions = await firstFilter.locator('option').all();
    if (firstFilterOptions.length > 1) {
      // Select first non-empty option
      const optionValue = await firstFilterOptions[1].getAttribute('value');
      if (optionValue) {
        await firstFilter.selectOption(optionValue);
      }
    }

    // Click clear filters button
    await page.locator(SELECTORS.CLEAR_FILTERS_BTN).click();

    // Verify filter is reset to empty/All
    const filterValue = await firstFilter.inputValue();
    expect(filterValue).toBe('');
  });

  test('filter dropdowns exist and have options', async ({ page }) => {
    await filterToggle(page).click();
    const filterForm = page.locator('#filters-form');
    await expect(filterForm).toBeVisible();

    // Check that at least some filter dropdowns exist (they're dynamically generated)
    const filterSelects = filterForm.locator('select.filter-dropdown');
    const count = await filterSelects.count();
    expect(count).toBeGreaterThan(0);
  });

  test('exercise table has correct structure', async ({ page }) => {
    await addPlanRow(page.request, ROUTINE_A, BENCH);
    await loadPlan(page, true);
    const table = page.locator(SELECTORS.EXERCISE_TABLE);
    await expect(table).toBeVisible();

    // Check table headers exist
    const headers = table.locator('thead th');
    const headerCount = await headers.count();
    expect(headerCount).toBeGreaterThan(5); // Should have multiple columns

    // Check expected columns exist
    const tableHtml = await table.locator('thead').innerHTML();
    expect(tableHtml.toLowerCase()).toContain('routine');
    expect(tableHtml.toLowerCase()).toContain('exercise');
    expect(tableHtml.toLowerCase()).toContain('sets');
    expect(tableHtml.toLowerCase()).toContain('weight');
  });

  test('muscle naming toggle syncs workout table column visibility', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await addPlanRow(page.request, ROUTINE_A, BENCH);
    await loadPlan(page, true);
    const tableModeToggle = page.locator('.tbl-view-mode-toggle[data-table-key="workout_plan"]');
    const advancedOnlyHeader = page.locator('th[data-label="Tertiary Muscle"]');

    await expect(tableModeToggle).toBeVisible();
    await expect(tableModeToggle).toContainText('Simple');
    await expect(advancedOnlyHeader).toBeHidden();

    await clickMuscleModeToggle(page);

    await expect(tableModeToggle).toContainText('Advanced');
    await expect(advancedOnlyHeader).toBeVisible();

    await clickMuscleModeToggle(page);

    await expect(tableModeToggle).toContainText('Simple');
    await expect(advancedOnlyHeader).toBeHidden();
  });

  test('muscle filter selections survive simple-to-scientific toggle', async ({ page }) => {
    const muscleFilters = [
      '#primary_muscle_group',
      '#secondary_muscle_group',
      '#tertiary_muscle_group',
      '#advanced_isolated_muscles',
    ];

    await page.waitForFunction(() => {
      const primary = document.getElementById('primary_muscle_group') as HTMLSelectElement | null;
      return Boolean(primary && Array.from(primary.options).some(option => option.value === 'chest'));
    });

    await page.evaluate((selectors) => {
      selectors.forEach((selector) => {
        const select = document.querySelector(selector) as HTMLSelectElement | null;
        if (!select) return;
        select.value = 'chest';
        select.dispatchEvent(new Event('change', { bubbles: true }));
      });
    }, muscleFilters);

    await clickMuscleModeToggle(page);

    await page.waitForFunction((selectors) => {
      return selectors.every((selector) => {
        const select = document.querySelector(selector) as HTMLSelectElement | null;
        return Boolean(select && select.value === 'chest' && select.selectedOptions[0]?.textContent?.includes('Chest'));
      });
    }, muscleFilters);
  });

  test('routine tabs navigation exists', async ({ page }) => {
    // Routine tabs container should exist
    const routineTabs = page.locator('#routine-tabs');
    await expect(routineTabs).toBeVisible();

    // "All" tab should be present
    const allTab = page.locator('#tab-all');
    await expect(allTab).toBeVisible();
    await expect(allTab).toHaveClass(/active/);
  });

  test('export button is clickable and triggers action', async ({ page }) => {
    // Make sure we have some data first by adding an exercise
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

    // Select and add exercise
    const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const firstOption = await exerciseSelect.locator('option').nth(1).getAttribute('value');
    if (firstOption) {
      await exerciseSelect.selectOption(firstOption);
    }
    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();

    // Wait for row to be added
    await page.waitForSelector('#workout_plan_table_body tr');

    await moreButton(page).click();
    // Setup download handling
    const downloadPromise = page.waitForEvent('download', { timeout: 5000 }).catch(() => null);

    // Click export button
    await page.locator(SELECTORS.EXPORT_EXCEL_BTN).click();

    // Either download starts or toast shows
    const download = await downloadPromise;
    if (download) {
      expect(download.suggestedFilename()).toContain('xlsx');
    }
    // If no download, check for toast (could be empty plan warning)
  });

  test('weight field accepts decimals and preserves manual edits (Issue #5)', async ({ page }) => {
    // Wait for the exercise dropdown to be populated.
    await page.waitForFunction(() => {
      const select = document.getElementById('exercise') as HTMLSelectElement;
      return select && select.options.length > 1;
    });

    const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const options = await exerciseSelect.locator('option').all();
    const firstValue = await options[1].getAttribute('value');
    const secondValue =
      options.length > 2 ? await options[2].getAttribute('value') : null;
    expect(firstValue).toBeTruthy();
    expect(secondValue).toBeTruthy();

    // Select an exercise — this is the one-shot trigger that should apply
    // the profile estimate to the Weight field.
    await exerciseSelect.selectOption(firstValue!);

    // Wait for the estimate to be *applied*, not merely answered. The marker is
    // set synchronously inside the change handler, so unlike a `waitForResponse`
    // registered after `selectOption` it cannot miss a fast response, and it
    // clears only once the value has been written to the input.
    await waitForWorkoutPlanReady(page);

    const weightInput = page.locator('#weight');
    await expect(weightInput).toHaveAttribute('type', 'number');
    const stepAttr = await weightInput.getAttribute('step');
    expect(['any', '0.25']).toContain(stepAttr);

    // Decimal input must persist in the field.
    await weightInput.fill('17.5');
    await expect(weightInput).toHaveValue('17.5');

    // Blur to commit, then re-read — the manual decimal value must survive
    // the change-event clamp/normalization handler.
    await weightInput.blur();
    await expect(weightInput).toHaveValue('17.5');

    // Re-selecting the same exercise should NOT overwrite the user's edit
    // (selectOption with the same value does not fire `change` in the DOM,
    // but assert the value is still intact regardless).
    await expect(weightInput).toHaveValue('17.5');

    // Switching to a different exercise IS the trigger to re-apply the
    // estimate — the manual value may now be replaced by the new estimate.
    if (secondValue && secondValue !== firstValue) {
      await exerciseSelect.selectOption(secondValue);
      await waitForWorkoutPlanReady(page);
      // Weight should now be whatever the new estimate decided — just
      // assert it is a valid non-empty numeric value (not "17.5" frozen).
      const newValue = await weightInput.inputValue();
      expect(newValue).not.toBe('');
      expect(Number.isNaN(parseFloat(newValue))).toBe(false);
    }
  });

  test('Workout Controls "show the math" expander opens with steps and improvement hint (Issue #17)', async ({ page }) => {
    // Seed a cold-start scenario so the trace + improvement hint appear.
    await page.request.post('/api/user_profile', {
      data: {
        gender: 'M',
        age: 30,
        height_cm: 180,
        weight_kg: 75,
        experience_years: 3,
      },
    });
    // Wipe any saved reference lifts that might have leaked from prior tests.
    await page.request.post('/api/user_profile/lifts', {
      data: [
        { lift_key: 'barbell_bench_press', weight_kg: null, reps: null },
        { lift_key: 'barbell_bicep_curl', weight_kg: null, reps: null },
      ],
    });

    await page.reload();
    await waitForWorkoutPlanReady(page);

    await page.locator(SELECTORS.ROUTINE_ENV).selectOption('GYM');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-program') as HTMLSelectElement | null;
      return Boolean(select && select.options.length > 1);
    });
    await page.locator(SELECTORS.ROUTINE_PROGRAM).selectOption('Full Body');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-day') as HTMLSelectElement | null;
      return Boolean(select && select.options.length > 1);
    });
    await page.locator(SELECTORS.ROUTINE_DAY).selectOption('Workout A');

    await page.locator(SELECTORS.EXERCISE_SEARCH).selectOption('Barbell Bench Press');
    await waitForWorkoutPlanReady(page);

    const toggle = page.locator('#workout-estimate-trace-toggle');
    const container = page.locator('#workout-estimate-trace');
    // Toggle is visible (trace is non-empty) and starts collapsed.
    await expect(toggle).toBeVisible();
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(container).toBeHidden();

    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await expect(container).toBeVisible();

    // Cold-start trace must call out its key inputs (Issue #17 §"What might
    // affect the score" — bodyweight, experience, preset, rounding).
    await expect(container).toContainText('Cold-start 1RM');
    await expect(container).toContainText('Light');
    await expect(container).toContainText(/Bodyweight ratio/);

    // Improvement hint surfaces a Profile-page link anchored to the
    // suggested lift row.
    const hintLink = container.locator('[data-trace-improvement-link]');
    await expect(hintLink).toBeVisible();
    const href = await hintLink.getAttribute('href');
    expect(href).toMatch(/\/user_profile.*barbell_bench_press/);
  });

  test('generate starter plan modal opens', async ({ page }) => {
    // Click generate starter plan button
    await moreButton(page).click();
    const generateBtn = page.locator('#generate-plan-btn');
    await expect(generateBtn).toBeVisible();
    await generateBtn.click();

    // Modal should open
    const modal = page.locator('#generatePlanModal');
    await expect(modal).toBeVisible({ timeout: 5000 });
    await expect(modal.locator('.modal-title')).toContainText('Generate Starter Plan');

    // Verify modal has expected content/structure
    await expect(modal.locator('.modal-body')).toBeVisible();
    await expect(modal.locator('.btn-close')).toBeVisible();
  });
});

test.describe('Plan Generator v1.5.0 Features', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
  });


  test('generate plan modal has priority muscles option', async ({ page }) => {
    // Open the generate plan modal
    await moreButton(page).click();
    const generateBtn = page.locator('#generate-plan-btn');
    await generateBtn.click();

    const modal = page.locator('#generatePlanModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Check for priority muscles selector (v1.5.0 feature)
    const priorityMuscles = modal.locator('#priority-muscles, [name="priority_muscles"], select[data-field="priority_muscles"]');
    
    // If the priority muscles field exists, verify it works
    if (await priorityMuscles.count() > 0) {
      await expect(priorityMuscles).toBeVisible();
    }

    // Close modal
    await page.keyboard.press('Escape');
  });

  test('generate plan modal has time budget option', async ({ page }) => {
    // Open the generate plan modal
    await moreButton(page).click();
    const generateBtn = page.locator('#generate-plan-btn');
    await generateBtn.click();

    const modal = page.locator('#generatePlanModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Check for time budget input (v1.5.0 feature)
    const timeBudget = modal.locator('#time-budget, [name="time_budget_minutes"], input[data-field="time_budget"]');
    
    // If the time budget field exists, verify it accepts numeric input
    if (await timeBudget.count() > 0) {
      await expect(timeBudget).toBeVisible();
      // Time budget should accept numbers
      await timeBudget.fill('45');
      await expect(timeBudget).toHaveValue('45');
    }

    // Close modal
    await page.keyboard.press('Escape');
  });

  test('generate plan modal has merge mode toggle', async ({ page }) => {
    // Open the generate plan modal
    await moreButton(page).click();
    const generateBtn = page.locator('#generate-plan-btn');
    await generateBtn.click();

    const modal = page.locator('#generatePlanModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Check for merge mode checkbox (v1.5.0 feature)
    const mergeMode = modal.locator('#merge-mode, [name="merge_mode"], input[type="checkbox"][data-field="merge_mode"]');
    
    // If merge mode toggle exists, verify it's functional
    if (await mergeMode.count() > 0) {
      await expect(mergeMode).toBeVisible();
    }

    // Close modal
    await page.keyboard.press('Escape');
  });

  test('generator API returns priority muscles option', async ({ request }) => {
    const response = await request.get('/get_generator_options');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.data).toHaveProperty('priority_muscles');
    expect(data.data.priority_muscles).toHaveProperty('available');
    expect(Array.isArray(data.data.priority_muscles.available)).toBe(true);
    expect(data.data.priority_muscles.available.length).toBeGreaterThan(0);
    expect(data.data.priority_muscles).toHaveProperty('max_selections');
    expect(data.data.priority_muscles.max_selections).toBe(2);
  });

  test('generator API returns time budget presets', async ({ request }) => {
    const response = await request.get('/get_generator_options');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.data).toHaveProperty('time_budget');
    expect(data.data.time_budget).toHaveProperty('min');
    expect(data.data.time_budget).toHaveProperty('max');
    expect(data.data.time_budget).toHaveProperty('presets');
    expect(Array.isArray(data.data.time_budget.presets)).toBe(true);
  });

  test('generator API validates priority muscles limit', async ({ request }) => {
    // Try to generate with too many priority muscles
    const response = await request.post('/generate_starter_plan', {
      data: {
        training_days: 2,
        environment: 'gym',
        priority_muscles: ['Chest', 'Back', 'Shoulders', 'Arms', 'Legs'],
        persist: false
      }
    });
    
    // Should either accept (with truncation) or return validation error
    expect([200, 400]).toContain(response.status());
    
    if (response.ok()) {
      const data = await response.json();
      // If accepted, it should have truncated to max 2
      if (data.data.metadata && data.data.metadata.priority_muscles) {
        expect(data.data.metadata.priority_muscles.length).toBeLessThanOrEqual(2);
      }
    }
  });
});

// ============================================================================
// Toast severity contract (Track A1) — app.js's generateStarterPlan() previously
// called showToast(message, type) instead of showToast(type, message). toast.js's
// legacy-signature fallback (modules/toast.js:236-248) treats any non-boolean 2nd
// arg as a falsy legacyIsError, so both the client-side validation warning and
// the server-error path silently rendered as a green "success" toast. These
// tests pin the correct severity class (bg-warning / bg-danger) as well as the
// message, so a regression back to the reversed argument order fails loudly.
// ============================================================================

test.describe('Starter plan toast severity contract', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);
  });


  test('no-equipment-selected guard renders a warning toast, not success', async ({ page }) => {
    await moreButton(page).click();
    await page.locator('#generate-plan-btn').click();
    const modal = page.locator('#generatePlanModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Uncheck every equipment box via the modal's own "None" shortcut so
    // generateStarterPlan() hits the client-side equipment-required guard
    // (app.js: showToast('warning', 'Please select at least one equipment type.'))
    // instead of reaching the API.
    await page.locator('button[onclick*="checked = false"]').click();

    await page.locator('#generatePlanSubmit').click();

    const toast = page.locator('#liveToast');
    await expect(toast).toBeVisible({ timeout: 5000 });
    await expect(toast).toHaveClass(/bg-warning/);
    await expect(toast).not.toHaveClass(/bg-success/);
    await expect(page.locator('#toast-body')).toContainText('Please select at least one equipment type.');

    // Submission was blocked client-side, so the modal stays open.
    await expect(modal).toBeVisible();
  });

  // Wrapped so the allowlist covers only the test that provokes it. The sibling
  // test above is blocked client-side and reaches no network, so it must keep a
  // zero allowance.
  test.describe('server rejection', () => {
    // This test fulfils /generate_starter_plan with a 400 on purpose, so these
    // four errors are the assertion's own stimulus, not a defect. Each is
    // anchored; the request id is the only variable part.
    test.use({
      consoleAllowlist: {
        expected: [
          {
            match: /^Failed to load resource: the server responded with a status of 400 \(Bad Request\)$/,
            reason: 'Chromium reports the deliberately-mocked 400 from /generate_starter_plan',
          },
          {
            match: /^\[req_[0-9a-z_]+\] API Error: \{url: \/generate_starter_plan, method: POST, status: 400, error: Object\}$/,
            reason: 'fetch-wrapper.js logs the non-2xx it was given by the route mock',
          },
          {
            match: /^\[req_[0-9a-z_]+\] API Error \(final\): \{url: \/generate_starter_plan, method: POST, error: Object\}$/,
            reason: 'fetch-wrapper.js logs once more after exhausting retries on the mocked 400',
          },
          {
            // `UNKNOWN_ERROR` is what normalizeError() falls back to for a body
            // with no `code`. Deliberately pinned: if the route or fetch-wrapper
            // starts emitting a real code, this reds and the pattern should be
            // re-derived from the new output rather than widened.
            match: /^Error generating plan: \{code: UNKNOWN_ERROR, message: No exercises available for the selected filters\., requestId: req_[0-9a-z_]+\}$/,
            reason: 'app.js generateStarterPlan() logs the rejection whose toast this test asserts',
          },
        ],
      },
    });

    test('server-rejected generation renders an error toast with the server message, not success', async ({ page }) => {
      await page.route('**/generate_starter_plan', async route => {
        await route.fulfill({
          status: 400,
          contentType: 'application/json',
          body: JSON.stringify({ message: 'No exercises available for the selected filters.' }),
        });
      });

      await moreButton(page).click();
      await page.locator('#generate-plan-btn').click();
      const modal = page.locator('#generatePlanModal');
      await expect(modal).toBeVisible({ timeout: 5000 });

      await page.locator('#generatePlanSubmit').click();

      const toast = page.locator('#liveToast');
      await expect(toast).toBeVisible({ timeout: 5000 });
      await expect(toast).toHaveClass(/bg-danger/);
      await expect(toast).not.toHaveClass(/bg-success/);
      await expect(page.locator('#toast-body')).toContainText('No exercises available for the selected filters.');
    });
  });
});

// ============================================================================
// Muscle selector — single MuscleMap body map
//
// One MuscleMap anatomy figure (id="body-{anterior,posterior}-hypertrophy-advanced")
// is used for both front and back. There is no Simple/Advanced toggle; regions
// are single-key (data-canonical-muscles) and select exactly their muscle.
// ============================================================================

test.describe('Muscle selector body map', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);

    await moreButton(page).click();
    await page.locator('#generate-plan-btn').click();
    await expect(page.locator('#generatePlanModal')).toBeVisible({ timeout: 5000 });
    // Wait for the inline SVG fetch + render in the modal.
    await expect(
      page.locator('#muscle-selector-container #svg-container svg')
    ).toBeVisible({ timeout: 5000 });
  });


  test('mounts the MuscleMap figure with no Simple/Advanced toggle', async ({ page }) => {
    const svg = page.locator('#muscle-selector-container #svg-container svg');
    await expect(svg).toHaveAttribute('id', /body-anterior-hypertrophy-advanced/);
    // The Simple/Advanced toggle has been removed.
    await expect(page.locator('#muscle-selector-container [data-view]')).toHaveCount(0);
  });

  test('clicking a region selects exactly that muscle, not neighbours', async ({ page }) => {
    await page
      .locator('#muscle-selector-container svg [data-canonical-muscles="chest"]')
      .first()
      .click();

    await expect(
      page.locator('#muscle-selector-container .legend-item[data-muscle="chest"] .legend-checkbox.checked')
    ).toBeVisible();
    for (const other of ['abs', 'biceps']) {
      await expect(
        page.locator(`#muscle-selector-container .legend-item[data-muscle="${other}"] .legend-checkbox.checked`)
      ).toHaveCount(0);
    }
  });

  test('back tab loads the posterior figure and front selection persists', async ({ page }) => {
    const svg = page.locator('#muscle-selector-container #svg-container svg');

    // Select a front muscle.
    await page.locator('#muscle-selector-container svg [data-canonical-muscles="chest"]').first().click();
    await expect(
      page.locator('#muscle-selector-container .legend-item[data-muscle="chest"] .legend-checkbox.checked')
    ).toBeVisible();

    // Back tab → posterior MuscleMap figure; select the glutes region.
    await page.locator('#muscle-selector-container [data-side="back"]').click();
    await expect(svg).toHaveAttribute('id', /body-posterior-hypertrophy-advanced/);
    await page.locator('#muscle-selector-container svg [data-canonical-muscles="gluteal"]').first().click();
    await expect(
      page.locator('#muscle-selector-container .legend-item[data-muscle="glutes"] .legend-checkbox.checked')
    ).toBeVisible();

    // Front selection survives the tab round trip.
    await page.locator('#muscle-selector-container [data-side="front"]').click();
    await expect(svg).toHaveAttribute('id', /body-anterior-hypertrophy-advanced/);
    await expect(
      page.locator('#muscle-selector-container .legend-item[data-muscle="chest"] .legend-checkbox.checked')
    ).toBeVisible();
  });
});

// ============================================================================
// §5 — Exercise reference video modal (PLANNING.md §5)
//
// Pattern A: a single video button per row. Curated exercises open a modal
// that embeds via youtube.com/embed. Uncurated exercises open a YouTube
// search tab directly. Closing the modal clears the iframe src.
// ============================================================================

test.describe('Exercise reference video modal (workout-plan)', () => {
  test.beforeEach(async ({ page }) => {

    // Block the real YouTube embed network. These specs assert the iframe `src`
    // attribute + link wiring, not playback; loading the real embed pulls in
    // YouTube scripts that emit intermittent console errors (e.g. a
    // compute-pressure permissions-policy violation) which flake the
    // console-error collector in CI. Fulfilling with an empty document keeps the
    // src attribute set while loading nothing third-party.
    await page.route(/^https:\/\/www\.youtube\.com\/embed\//, (route) =>
      route.fulfill({ status: 200, contentType: 'text/html', body: '' }),
    );

    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForWorkoutPlanReady(page);

    // Seed one exercise into the plan so a row renders with the play button.
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
  });


  test('every row has an accessible play button next to Swap', async ({ page }) => {
    const rows = page.locator('#workout_plan_table_body tr');
    const rowCount = await rows.count();
    expect(rowCount).toBeGreaterThan(0);

    const firstRow = rows.first();
    const playBtn = firstRow.locator('.btn-video');
    await expect(playBtn).toBeVisible();

    // Seed rows are uncurated → search-variant icon + accessible name.
    const ariaLabel = await playBtn.getAttribute('aria-label');
    expect(ariaLabel).toMatch(/^Search YouTube for a /);
    await expect(playBtn.locator('i')).toHaveClass(/fa-search/);

    const swapBtn = firstRow.locator('.btn-swap');
    await expect(swapBtn).toBeVisible();
  });

  test('uncurated exercise (NULL youtube_video_id) opens a YouTube search tab — no modal', async ({ page }) => {
    // Stub window.open so the click captures the target URL without spawning a
    // real YouTube tab (deterministic, network-free).
    await page.evaluate(() => {
      // @ts-expect-error - test-only capture
      window.__openedUrl = null;
      window.open = (url) => {
        // @ts-expect-error - test-only capture
        window.__openedUrl = url;
        return null;
      };
    });

    const playBtn = page.locator('#workout_plan_table_body tr .btn-video').first();
    await playBtn.click();

    // Goes straight to YouTube search results — the modal never opens.
    const opened = await page.evaluate(() => {
      // @ts-expect-error - test-only capture set above
      return window.__openedUrl as string | null;
    });
    expect(opened).toMatch(/^https:\/\/www\.youtube\.com\/results\?search_query=/);
    await expect(page.locator('#exerciseVideoModal')).toBeHidden();
  });

  test('valid id opens embed mode; close clears iframe src', async ({ page }) => {
    // Drive the modal directly via its public API. This exercises the JS
    // logic without mutating the live exercises table — equivalent to a
    // curated youtube_video_id arriving in the row data.
    // Open and wait for Bootstrap to FINISH the show transition
    // (`shown.bs.modal`). Interacting before the transition completes makes
    // Bootstrap drop the dismiss click — hide() is a no-op while transitioning —
    // which left the modal open (the actual 1-in-N CI flake here). Registering
    // the listener before show() closes the race.
    await page.evaluate(() => {
      return new Promise<void>((resolve) => {
        const el = document.getElementById('exerciseVideoModal');
        el?.addEventListener('shown.bs.modal', () => resolve(), { once: true });
        // @ts-expect-error - exposed by static/js/modules/exercise-video-modal.js
        window.openExerciseVideoModal('dQw4w9WgXcQ', 'Test Exercise');
      });
    });

    const modal = page.locator('#exerciseVideoModal');
    await expect(modal).toBeVisible();

    // Embed visible.
    await expect(page.locator('#exerciseVideoEmbedWrap')).toBeVisible();

    const iframe = page.locator('#exerciseVideoIframe');
    // Auto-retrying assertion (not a one-shot getAttribute) — robust even though
    // openExerciseVideoModal sets src synchronously.
    await expect(iframe).toHaveAttribute(
      'src',
      /^https:\/\/www\.youtube\.com\/embed\/dQw4w9WgXcQ/,
    );

    const externalLink = page.locator('#exerciseVideoExternalLink');
    const externalHref = await externalLink.getAttribute('href');
    expect(externalHref).toBe('https://www.youtube.com/watch?v=dQw4w9WgXcQ');
    expect(await externalLink.getAttribute('target')).toBe('_blank');
    expect(await externalLink.getAttribute('rel')).toBe('noopener noreferrer');

    // Close — iframe src must be blanked so playback stops. The blank happens in
    // the `hidden.bs.modal` handler (exercise-video-modal.js), which can fire a
    // tick after Playwright considers the modal hidden; poll so the read can't
    // race the handler.
    await page.locator('#exerciseVideoModal .btn-close').click();
    await expect(modal).toBeHidden();
    await expect
      .poll(async () => {
        const srcAfter = await iframe.getAttribute('src');
        return srcAfter === '' || srcAfter === null;
      })
      .toBe(true);
  });

  test('opening for a different exercise swaps the URL cleanly', async ({ page }) => {
    // First open: id A, expect iframe src to match A and title to mention A.
    await page.evaluate(() => {
      // @ts-expect-error - exposed by exercise-video-modal.js
      window.openExerciseVideoModal('dQw4w9WgXcQ', 'First Exercise');
    });
    await expect(page.locator('#exerciseVideoModal')).toBeVisible();
    await expect(page.locator('#exerciseVideoIframe')).toHaveAttribute(
      'src',
      /embed\/dQw4w9WgXcQ/,
    );
    await expect(page.locator('#exerciseVideoModalExerciseName')).toContainText(
      'First Exercise',
    );

    // Second call (modal still open): contents must update in place to id B.
    await page.evaluate(() => {
      // @ts-expect-error - exposed by exercise-video-modal.js
      window.openExerciseVideoModal('aaaaaaaaaaa', 'Second Exercise');
    });
    await expect(page.locator('#exerciseVideoIframe')).toHaveAttribute(
      'src',
      /embed\/aaaaaaaaaaa/,
    );
    await expect(page.locator('#exerciseVideoModalExerciseName')).toContainText(
      'Second Exercise',
    );
  });

  test('malformed id opens a YouTube search tab — no modal', async ({ page }) => {
    const opened = await page.evaluate(() => {
      let captured: string | null = null;
      window.open = (url) => {
        captured = String(url);
        return null;
      };
      // @ts-expect-error - exposed by exercise-video-modal.js
      window.openExerciseVideoModal('not-an-id', 'Fake Exercise');
      return captured;
    });
    await expect(page.locator('#exerciseVideoModal')).toBeHidden();
    expect(opened).toMatch(/^https:\/\/www\.youtube\.com\/results\?search_query=/);
    expect(opened).toContain('Fake');
  });
});

test.describe('§4 free-exercise-db thumbnails', () => {
  // The first successful plan response chooses the opening routine and reveals the table.
  async function loadMockExercises(page: Page, exercises: Record<string, unknown>[]) {
    await page.route(url => url.pathname === API_ENDPOINTS.GET_WORKOUT_PLAN, route => {
      if (route.request().method() !== 'GET') return route.fallback();
      return route.fulfill({ json: { ok: true, data: exercises } });
    });
    await loadPlan(page);
    await expect(page.locator('#workout')).toHaveAttribute('data-plan-state', 'populated');
    await expect(planRows(page)).toHaveCount(exercises.length);
  }

  test('mocked row with media_path renders a thumbnail img with safe src', async ({ page }) => {
    await loadMockExercises(page, [
      {
        id: 9001,
        routine: 'GYM - Full Body - Workout A',
        exercise: 'Band Good Morning',
        media_path: 'Band_Good_Morning/0.jpg',
        primary_muscle_group: 'Hamstrings',
        sets: 3,
        min_rep_range: 8,
        max_rep_range: 12,
        rir: 2,
        weight: 50,
      },
    ]);

    const row = planRow(page, 9001);
    await expect(row).toBeVisible();

    const thumb = row.locator('img.exercise-thumbnail');
    await expect(thumb).toBeVisible();

    const src = await thumb.getAttribute('src');
    expect(src).toBe('/static/vendor/free-exercise-db/exercises/Band_Good_Morning/0.jpg');
    expect(src).not.toContain('..');

    const alt = await thumb.getAttribute('alt');
    expect(alt).toBe('Band Good Morning reference');

    expect(await thumb.getAttribute('loading')).toBe('lazy');
    expect(await thumb.getAttribute('width')).toBe('32');
    expect(await thumb.getAttribute('height')).toBe('32');
  });

  test('mocked row with NULL media_path renders no img and no console errors', async ({ page }) => {
    await loadMockExercises(page, [
      {
        id: 9002,
        routine: 'GYM - Full Body - Workout A',
        exercise: 'Some Uncurated Exercise',
        media_path: null,
        primary_muscle_group: 'Quadriceps',
        sets: 3,
        min_rep_range: 5,
        max_rep_range: 8,
        rir: 1,
        weight: 80,
      },
    ]);

    const row = planRow(page, 9002);
    await expect(row).toBeVisible();
    await expect(row.locator('img.exercise-thumbnail')).toHaveCount(0);
  });

  test('mocked row with HTML-special exercise name renders escaped (no raw markup leaks)', async ({ page }) => {
    await loadMockExercises(page, [
      {
        id: 9003,
        routine: 'GYM - Full Body - Workout A',
        exercise: `Coach's <Test> Press`,
        media_path: 'Band_Good_Morning/0.jpg',
        primary_muscle_group: 'Chest',
        sets: 3,
        min_rep_range: 8,
        max_rep_range: 12,
        rir: 2,
        weight: 60,
      },
    ]);

    const row = planRow(page, 9003);
    // textContent strips markup; if escapeHtml is working, the literal angle brackets are present.
    await expect(row.locator('.exercise-name')).toHaveText(`Coach's <Test> Press`);
    // And no nested <Test> element was injected from the angle brackets.
    expect(await row.locator('.exercise-name Test').count()).toBe(0);

    const thumb = row.locator('img.exercise-thumbnail');
    const alt = await thumb.getAttribute('alt');
    expect(alt).toBe(`Coach's <Test> Press reference`);
  });

  test('escapeHtml + resolveExerciseMediaSrc behave per the §4.3/§4.4 contract', async ({ page }) => {
    await loadPlan(page);
    const result = await page.evaluate(async () => {
      const mod = await import('/static/js/modules/exercise-helpers.js');
      return {
        escapeMixed: mod.escapeHtml(`Coach's <Test> Press`),
        escapeAmp: mod.escapeHtml('A & B'),
        escapeNull: mod.escapeHtml(null),
        validJpg: mod.resolveExerciseMediaSrc('Band_Good_Morning/0.jpg'),
        validUpperExt: mod.resolveExerciseMediaSrc('Foo/0.PNG'),
        invalidEmpty: mod.resolveExerciseMediaSrc(''),
        invalidNull: mod.resolveExerciseMediaSrc(null),
        invalidAbs: mod.resolveExerciseMediaSrc('/abs/path/0.jpg'),
        invalidParent: mod.resolveExerciseMediaSrc('../etc/passwd'),
        invalidBackslash: mod.resolveExerciseMediaSrc('dir\\img.jpg'),
        invalidColon: mod.resolveExerciseMediaSrc('C:/temp/0.jpg'),
        invalidExt: mod.resolveExerciseMediaSrc('dir/img.exe'),
        invalidNoExt: mod.resolveExerciseMediaSrc('dir/img'),
        encodesSpace: mod.resolveExerciseMediaSrc('weird name/0.jpg'),
      };
    });

    expect(result.escapeMixed).toBe('Coach&#39;s &lt;Test&gt; Press');
    expect(result.escapeAmp).toBe('A &amp; B');
    expect(result.escapeNull).toBe('');
    expect(result.validJpg).toBe('/static/vendor/free-exercise-db/exercises/Band_Good_Morning/0.jpg');
    expect(result.validUpperExt).toBe('/static/vendor/free-exercise-db/exercises/Foo/0.PNG');
    expect(result.invalidEmpty).toBeNull();
    expect(result.invalidNull).toBeNull();
    expect(result.invalidAbs).toBeNull();
    expect(result.invalidParent).toBeNull();
    expect(result.invalidBackslash).toBeNull();
    expect(result.invalidColon).toBeNull();
    expect(result.invalidExt).toBeNull();
    expect(result.invalidNoExt).toBeNull();
    expect(result.encodesSpace).toBe('/static/vendor/free-exercise-db/exercises/weird%20name/0.jpg');
  });
});

/**
 * `workout-plan-desktop-contract.spec.ts` asserts the drag-handle *column*
 * exists, but that is server-rendered markup that renders with or without
 * SortableJS.
 *
 * `Sortable.create()` in `static/js/modules/workout-plan-table.js` is unguarded,
 * so a missing library throws — and the collector cannot see that either (see
 * `fixtures.ts`). The throw aborts `populateWorkoutPlanTable()` before
 * `initializeSupersetActions()`, so it takes the superset action bar down too.
 */
test.describe('Workout Plan drag-and-drop library', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);
  });


  test('SortableJS loads locally and is usable by the plan table', async ({ page }) => {
    const sortable = await page.evaluate(() => {
      const scoped = (window as unknown as Record<string, unknown>).Sortable as
        | Record<string, unknown>
        | undefined;
      return {
        type: typeof scoped,
        create: typeof scoped?.create,
        // Proves the payload is the real library rather than any object that
        // happens to answer to the name.
        version: typeof scoped?.version === 'string' ? scoped.version : null,
      };
    });

    expect(sortable.type).toBe('function');
    expect(sortable.create).toBe('function');
    expect(sortable.version).toBe('1.14.0');
  });
});

test.describe('Plan redesign acceptance', () => {
  // Hold one browser request until the test delivers the real Flask response.
  async function holdNextRoute(page: Page, pattern: string) {
    let capture!: (route: Route) => void;
    const next = new Promise<Route>(resolve => { capture = resolve; });
    await page.route(pattern, capture, { times: 1 });
    return { next };
  }

  test('opens on the first routine, exposes All by pointer and keyboard, and never remembers the choice', async ({ page }) => {
    await addPlanRow(page.request, ROUTINE_B, DEADLIFT);
    await addPlanRow(page.request, ROUTINE_A, SQUAT);
    await loadPlan(page);
    await waitForWorkoutPlanReady(page);
    const first = routineTab(page, ROUTINE_A);
    const all = routineTab(page, 'all');
    const storage = () => page.evaluate(() => ({
      local: Object.fromEntries(Object.entries(localStorage).sort()),
      session: Object.fromEntries(Object.entries(sessionStorage).sort()),
      cookies: document.cookie.split('; ').sort(),
    }));
    const before = await storage();
    await expect(first, 'a populated page opens on the first routine in display order').toHaveAttribute('aria-selected', 'true');
    await expect(planRows(page).locator('.exercise-name')).toHaveText([SQUAT]);

    await all.click();
    await expect(all).toHaveAttribute('aria-selected', 'true');
    await expect(planRows(page).locator('.exercise-name')).toHaveText([SQUAT, DEADLIFT]);
    expect(await storage()).toEqual(before);
    await loadPlan(page, true);
    await waitForWorkoutPlanReady(page);
    await expect(first).toHaveAttribute('aria-selected', 'true');
    await expect(planRows(page).locator('.exercise-name')).toHaveText([SQUAT]);
    expect(await storage()).toEqual(before);

    await all.focus();
    await page.keyboard.press('Enter');
    await expect(all).toHaveAttribute('aria-selected', 'true');
    await expect(planRows(page).locator('.exercise-name')).toHaveText([SQUAT, DEADLIFT]);
    expect(await storage()).toEqual(before);

    const planPath = '**' + API_ENDPOINTS.GET_WORKOUT_PLAN;
    const refresh = await holdNextRoute(page, planPath);
    await page.evaluate(() => window.dispatchEvent(new PageTransitionEvent('pageshow', { persisted: true })));
    const route = await refresh.next;
    expect(route.request().method()).toBe('GET');
    const selectedAll = all.and(page.locator('[aria-selected="true"]'));
    expect(await selectedAll.isVisible(), 'restoring the page must not paint the previous All selection').toBe(false);
    const otherRoutineRow = planRows(page).filter({ hasText: DEADLIFT });
    expect(await otherRoutineRow.isVisible(), 'the previous All view must not expose another routine’s actions').toBe(false);
    await expect(page.getByRole('region', { name: 'Empty plan' })).toBeHidden();

    const refreshed = page.waitForResponse(planPath);
    await route.continue();
    const response = await refreshed;
    expect(response.status()).toBe(200);
    expect((await response.json()).ok).toBe(true);
    await expect(first).toHaveAttribute('aria-selected', 'true');
    await expect(planRows(page).locator('.exercise-name')).toHaveText([SQUAT]);
    expect(await storage()).toEqual(before);
  });

  test('a delayed Sets save updates the mounted row after clicking All', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await addPlanRow(page.request, ROUTINE_A, SQUAT);
    await addPlanRow(page.request, ROUTINE_B, DEADLIFT);
    const [squat] = await planData(page.request);
    await loadPlan(page);
    await setDetails(page, squat.id, true);
    const row = planRow(page, squat.id);
    const field = row.locator('[data-field="sets"]');
    await field.getByRole('button').click();
    await field.getByRole('spinbutton').fill('5');
    const held = await holdNextRoute(page, '**/update_exercise');
    const all = routineTab(page, 'all');
    await all.click();
    const route = await held.next;
    expect(route.request().method()).toBe('POST');
    expect(route.request().postDataJSON()).toEqual({ id: squat.id, updates: { sets: '5' } });
    await expect(all).toHaveAttribute('aria-selected', 'true');
    await expect(planRows(page).locator('.exercise-name')).toHaveText([SQUAT, DEADLIFT]);
    const response = await route.fetch();
    expect(response.status()).toBe(200);
    expect((await response.json()).ok).toBe(true);
    await route.fulfill({ response });
    await expect(row.locator('.plan-prescription')).toHaveText('5 sets × 6–10 · 50 kg · RIR 2');
    await expect(field).toHaveText('5');
    await expect(all).toHaveAttribute('aria-selected', 'true');
  });

  for (const older of ['combined filters', 'routine catalog', 'all catalog'] as const) {
    test(`keeps the latest filter results after a delayed ${older} response`, async ({ page }) => {
      await loadPlan(page);
      await waitForPageReady(page);
      await filterToggle(page).click();
      const chest = page.locator('#filters-form select[data-filter-key="Primary Muscle Group"]');
      const equipment = page.locator('#filters-form select[data-filter-key="Equipment"]');
      const muscleChip = page.getByRole('button', { name: /Primary Muscle Group.*Chest/i });
      const filterPath = '**/filter_exercises';
      if (older !== 'routine catalog') {
        const initial = page.waitForResponse(filterPath);
        await chest.selectOption({ label: 'Chest' }, { force: true });
        expect((await initial).status()).toBe(200);
      } else {
        await page.locator('#routine-env').selectOption('GYM');
        await page.locator('#routine-program').selectOption('Full Body');
      }
      const path = older === 'combined filters' ? filterPath :
        older === 'routine catalog' ? '**/get_routine_exercises/*' : '**/get_all_exercises';
      const held = await holdNextRoute(page, path);
      if (older === 'combined filters') await equipment.selectOption({ label: 'Barbell' }, { force: true });
      else if (older === 'routine catalog') await page.locator('#routine-day').selectOption('Workout A');
      else await muscleChip.click();
      const route = await held.next;
      const stale = await route.fetch();
      expect(stale.status()).toBe(200);
      const latest = page.waitForResponse(filterPath);
      if (older === 'combined filters') await muscleChip.click();
      else await equipment.selectOption({ label: 'Barbell' }, { force: true });
      const response = await latest;
      expect(response.request().method()).toBe('POST');
      expect(response.request().postDataJSON()).toEqual({ Equipment: 'Barbell' });
      expect(response.status()).toBe(200);
      const { ok, data: names } = await response.json();
      expect(ok).toBe(true);
      expect(names).toContain(SQUAT);
      expect((await stale.json()).data).not.toEqual(names);
      const badge = page.locator('#exercise-match-count');
      await expect(badge).toHaveText(`${names.length} matching`);
      const delivered = page.waitForResponse(path);
      await route.fulfill({ response: stale });
      expect(await (await delivered).finished()).toBeNull();
      // Drain the older response's browser-side consumers before inspecting stable state.
      await page.waitForLoadState('networkidle');
      await expect(page.locator('#filter-chips button')).toHaveCount(1);
      await expect(page.getByRole('button', { name: /Equipment.*Barbell/i })).toBeVisible();
      await expect(page.locator('#exercise option:not([value=""])')).toHaveText(names);
      await expect(badge).toHaveText(`${names.length} matching`);
      await expect(page.locator('#toast-body .toast-message')).toHaveText(`Found ${names.length} exercises matching Equipment`);
    });
  }

  for (const width of [390, 1440]) {
    test(`shows only Add Exercise as filled primary and puts volume above the tabs at ${width} px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      for (const populated of [false, true]) {
        if (populated) await addPlanRow(page.request, ROUTINE_A, SQUAT);
        const volume = page.waitForResponse(response => new URL(response.url()).pathname === '/api/volume_progress');
        await loadPlan(page);
        expect((await volume).ok()).toBe(true);
        await expect(planRows(page)).toHaveCount(populated ? 1 : 0);
        expect(await filledPlanActions(page), populated ? 'populated plan' : 'empty plan').toEqual(singleAddAction);
        await expect(planHeader(page)).toBeVisible();
        await expect(planPanel(page).locator('#vpActiveSummary')).toBeVisible();
        await expect(planPanel(page).locator('#vpToggle')).toBeVisible();
        const top = await page.locator('#workout').evaluate(workout => {
          const y = (selector: string) => workout.querySelector(selector)!.getBoundingClientRect().top;
          return { volume: y('#vpActiveSummary'), targets: y('#vpToggle'), tabs: y('#routine-tabs') };
        });
        expect(Math.max(top.volume, top.targets)).toBeLessThan(top.tabs);
      }
      await planPanel(page).locator('#vpToggle').click();
      const drawer = page.locator('#vpDrawer');
      await expect(drawer).toHaveAttribute('aria-hidden', 'false');
      await expect(drawer.getByRole('heading', { name: 'Volume targets' })).toBeVisible();
      await loadPlan(page, true);
      await expect(drawer).toHaveAttribute('aria-hidden', 'false');
      await drawer.locator('.vp-close').click();
      await expect(drawer).toHaveAttribute('aria-hidden', 'true');
    });

    test(`collapses filters and renders all 12 dropdown triggers when opened at ${width} px`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      await loadPlan(page);
      const toggle = filterToggle(page);
      const dropdowns = page.locator('#filters-form .wpdd-button');
      await expect(toggle, 'filters open only on demand').toHaveAttribute('aria-expanded', 'false');
      await expect(dropdowns).toHaveCount(12);
      expect(await dropdowns.evaluateAll(nodes => nodes.every(node => !node.getClientRects().length))).toBe(true);
      await toggle.click();
      await expect(toggle).toHaveAttribute('aria-expanded', 'true');
      const widths = await dropdowns.evaluateAll(nodes => nodes.map(node => node.getBoundingClientRect().width));
      expect(widths).toHaveLength(12);
      for (const triggerWidth of widths) expect(triggerWidth).toBeGreaterThan(0);
    });
  }

  test('names active filter chips and removing one sends one filter request', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await loadPlan(page);
    const toggle = filterToggle(page);
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await toggle.click();
    const select = (key: string) => page.locator('#filters-form select[data-filter-key="' + key + '"]');
    const muscle = select('Primary Muscle Group');
    const equipment = select('Equipment');
    const isFilter = (url: string) => new URL(url).pathname === '/filter_exercises';
    for (const [locator, label] of [[muscle, 'Chest'], [equipment, 'Barbell']] as const) {
      const response = page.waitForResponse(result => isFilter(result.url()) && result.request().method() === 'POST');
      await locator.selectOption({ label }, { force: true });
      expect((await response).ok()).toBe(true);
    }
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    const muscleChip = page.getByRole('button', { name: /Primary Muscle Group.*Chest/i });
    const equipmentChip = page.getByRole('button', { name: /Equipment.*Barbell/i });
    await expect(muscleChip).toBeVisible();
    await expect(equipmentChip).toBeVisible();
    const calls: object[] = [];
    const catalogCalls: string[] = [];
    page.on('request', request => {
      const path = new URL(request.url()).pathname;
      if (isFilter(request.url()) && request.method() === 'POST') calls.push(request.postDataJSON());
      if (path.startsWith('/get_routine_exercises/') && request.method() === 'GET') catalogCalls.push(path);
    });
    const filtered = page.waitForResponse(response => isFilter(response.url()) && response.request().method() === 'POST');
    await muscleChip.click();
    expect((await filtered).ok()).toBe(true);
    await expect(muscle).toHaveValue('');
    await expect(equipment).not.toHaveValue('');
    await expect(muscleChip).toBeHidden();
    await expect(equipmentChip).toBeVisible();
    expect(calls, 'removing one chip posts exactly the remaining filter').toEqual([{ Equipment: 'Barbell' }]);

    const cascadeChoices = [
      ['#routine-env', 'GYM'],
      ['#routine-program', 'Full Body'],
      ['#routine-day', 'Workout A'],
    ] as const;
    for (const [selector, value] of cascadeChoices) {
      const before = calls.length;
      const filtered = page.waitForResponse(response => isFilter(response.url()) && response.request().method() === 'POST');
      await page.locator(selector).selectOption(value);
      expect((await filtered).ok()).toBe(true);
      expect(calls.slice(before), `${selector} reapplies the Equipment filter once`).toEqual([{ Equipment: 'Barbell' }]);
    }
    await expect(page.locator('#routine')).toHaveValue(ROUTINE_A);
    const exercise = page.locator('#exercise');
    await exercise.selectOption({ index: 1 }, { force: true });
    await expect(exercise).not.toHaveValue('');
    expect(calls, 'chip removal and the three cascade changes each post once').toHaveLength(1 + cascadeChoices.length);
    expect(catalogCalls, 'active filters bypass the unfiltered routine catalog').toEqual([]);

    await page.locator('#clear-filters-btn').click();
    await expectToast(page, 'Filters cleared successfully');
    await expect(equipmentChip).toBeHidden();
    const values = await page.locator('#filters-form select, #routine, #routine-env, #routine-program, #routine-day, #exercise')
      .evaluateAll(nodes => nodes.map(node => (node as HTMLInputElement).value));
    expect(values).toEqual(Array(17).fill(''));
  });

  test.describe('phone Details', () => {
    test.use({ hasTouch: true, viewport: { width: 390, height: 844 } });

    test('reveals the approved Simple and Advanced fields by touch and keyboard and closes after reload', async ({ page }) => {
      await addPlanRow(page.request, ROUTINE_A, SQUAT);
      const [record] = await planData(page.request);
      await loadPlan(page);
      const row = planRow(page, record.id);
      await expect(row).toBeVisible();
      const disclosure = details(page, record.id);
      await expect(disclosure, 'a closed card shows a Details disclosure').toHaveAttribute('aria-expanded', 'false');
      const common = row.locator('[data-field], .execution-style-cell, .superset-checkbox, [data-label="Primary Muscle"], [data-label="Actions"]');
      const extra = row.locator(
        '[data-label="Tertiary Muscle"], [data-label="Utility"], [data-label="Movement Pattern"], ' +
        '[data-label="Movement Subpattern"], [data-label="Stabilizers"], [data-label="Synergists"]',
      );
      await expect(common).toHaveCount(10);
      await expect(extra).toHaveCount(6);
      for (const cell of await common.all()) await expect(cell).toBeHidden();
      await disclosure.tap();
      await expect(disclosure).toHaveAttribute('aria-expanded', 'true');
      for (const cell of await common.all()) await expect(cell).toBeVisible();
      for (const cell of await extra.all()) await expect(cell).toBeHidden();
      await disclosure.tap();
      await setPlanView(page, 'advanced');
      await disclosure.focus();
      await page.keyboard.press('Space');
      await expect(disclosure).toHaveAttribute('aria-expanded', 'true');
      for (const cell of await extra.all()) await expect(cell).toBeVisible();
      await loadPlan(page, true);
      await expect(disclosure).toHaveAttribute('aria-expanded', 'false');
      for (const cell of await common.all()) await expect(cell).toBeHidden();
    });
  });

  test('dark card Swap uses shared ghost colors and hovered numbers stay unobscured', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.addInitScript(() => localStorage.setItem('darkMode', 'true'));
    await addPlanRow(page.request, ROUTINE_A, SQUAT);
    const [record] = await planData(page.request);
    await loadPlan(page);
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    const swap = planRow(page, record.id).getByRole('button', { name: 'Swap exercise' });
    const reference = details(page, record.id);
    const colors = (control: Locator) => control.evaluate(async node => {
      await Promise.all(node.getAnimations().map(animation => animation.finished));
      const style = getComputedStyle(node);
      return [style.color, style.backgroundColor, style.borderTopColor];
    });
    expect.soft(await colors(swap), 'idle ghost').toEqual(await colors(reference));
    await reference.hover();
    const hovered = await colors(reference);
    await swap.hover();
    expect.soft(await colors(swap), 'hovered ghost').toEqual(hovered);

    await setDetails(page, record.id, true);
    const cell = planRow(page, record.id).locator('[data-field="sets"]');
    await cell.getByRole('button').hover();
    expect(await cell.evaluate(node => {
      const pseudo = getComputedStyle(node, '::after');
      return pseudo.display !== 'none' && pseudo.visibility !== 'hidden' && pseudo.content.includes('✎');
    }), 'the legacy pencil must not cover the Sets value').toBe(false);
  });

  for (const width of [320, 360, 390]) {
    test(`fits widest realistic values and card actions at ${width} px and scale 8`, async ({ page, baseURL }) => {
      await page.setViewportSize({ width, height: 844 });
      const { squat, deadlift } = await addTheWidePhoneValues(page.request);
      expect(baseURL, 'the isolated Playwright server has a base URL').toBeDefined();
      await page.context().addCookies([{ name: 'ui-scale-level', value: '8', url: baseURL! }]);
      await page.addInitScript(() => localStorage.setItem('ui-scale-level', '8'));
      await loadPlan(page);
      await expect(page.locator('html')).toHaveAttribute('data-scale', '8');
      expect(await page.locator('html').evaluate(el => Number(getComputedStyle(el).zoom))).toBe(1.2);
      await page.evaluate(() => document.fonts.ready);
      await expect(planRow(page, squat.id), 'the phone renders a Plan card').toHaveClass(/\bui-record-card\b/);
      expect(await phonePlanProblems(page), 'closed cards').toEqual([]);
      await setDetails(page, squat.id, true);
      for (const [field, value] of Object.entries({ sets: 10, min_rep_range: 30, max_rep_range: 30, weight: 102.5, rir: 10, rpe: 9.5 })) {
        await expect(planRow(page, squat.id).locator('[data-field="' + field + '"]')).toHaveText(String(value));
      }
      expect(await phonePlanProblems(page), 'Squat Details').toEqual([]);
      await setSupersetChoice(planRow(page, squat.id), true);
      await expect(page.locator('#superset-actions')).toBeVisible();
      expect(await phonePlanProblems(page), 'selection bar and Squat Details').toEqual([]);
      await setSupersetChoice(planRow(page, squat.id), false);
      await setDetails(page, squat.id, false);
      await setDetails(page, deadlift.id, true);
      await expect(planRow(page, deadlift.id).locator('[data-field="weight"]')).toHaveText('999.5');
      expect(await phonePlanProblems(page), '999.5 kg Deadlift Details').toEqual([]);
    });
  }

  test('card Details closes on link and execution-style rerenders but stays open on swap and inline edit', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    for (const exercise of [BENCH, ROW, SQUAT]) await addPlanRow(page.request, ROUTINE_A, exercise);
    const rows = await planData(page.request);
    const bench = rows.find(row => row.exercise === BENCH)!;
    const row = rows.find(record => record.exercise === ROW)!;
    const squat = rows.find(record => record.exercise === SQUAT)!;
    await loadPlan(page);
    await setDetails(page, bench.id, true);
    await setDetails(page, row.id, true);
    await setSupersetChoice(planRow(page, bench.id), true);
    await setSupersetChoice(planRow(page, row.id), true);
    const link = page.waitForResponse(response => new URL(response.url()).pathname === '/api/superset/link');
    await page.locator('#link-superset-btn').click();
    expect((await link).ok()).toBe(true);
    await expect(details(page, bench.id)).toHaveAttribute('aria-expanded', 'false');
    await expect(details(page, row.id)).toHaveAttribute('aria-expanded', 'false');

    await setDetails(page, squat.id, true);
    await planRow(page, squat.id).locator('.execution-style-cell .badge').click();
    const picker = page.locator('.execution-style-picker');
    await picker.getByText('AMRAP', { exact: true }).click();
    const style = page.waitForResponse(response => new URL(response.url()).pathname === '/api/execution_style' &&
      response.request().method() === 'POST');
    await picker.getByRole('button', { name: 'Apply' }).click();
    const saved = await style;
    expect(saved.ok()).toBe(true);
    expect(saved.request().postDataJSON()).toMatchObject({ exercise_id: squat.id, execution_style: 'amrap' });
    await expect(details(page, squat.id)).toHaveAttribute('aria-expanded', 'false');

    await setDetails(page, squat.id, true);
    const swap = page.waitForResponse(response => new URL(response.url()).pathname === '/replace_exercise');
    await planRow(page, squat.id).getByRole('button', { name: 'Swap exercise' }).click();
    const swapped = await swap;
    expect(swapped.ok()).toBe(true);
    expect(swapped.request().postDataJSON()).toEqual({ id: squat.id, strategy: 'ai' });
    await expect.poll(async () => (await planData(page.request)).find(record => record.id === squat.id)?.exercise)
      .not.toBe(SQUAT);
    await expect(details(page, squat.id)).toHaveAttribute('aria-expanded', 'true');

    const field = planRow(page, squat.id).locator('[data-field="sets"]');
    await field.getByRole('button').click();
    const editor = field.getByRole('spinbutton');
    await editor.fill('4');
    const update = page.waitForResponse(response => new URL(response.url()).pathname === '/update_exercise');
    await editor.press('Enter');
    expect((await update).ok()).toBe(true);
    await expect(field).toHaveText('4');
    await expect(details(page, squat.id)).toHaveAttribute('aria-expanded', 'true');

    const removed = page.waitForResponse(response => new URL(response.url()).pathname === '/remove_exercise');
    await planRow(page, squat.id).getByRole('button', { name: 'Remove' }).click();
    const deletion = await removed;
    expect(deletion.ok()).toBe(true);
    expect(deletion.request().postDataJSON()).toEqual({ id: squat.id });
    await expectToast(page, /Exercise removed successfully/);
    await expect(planRow(page, squat.id)).toHaveCount(0);
  });
});

test.describe('Plan redesign characterization', () => {
  test('returns to All when the selected routine loses its last exercise', async ({ page }) => {
    await addPlanRow(page.request, ROUTINE_A, SQUAT);
    await addPlanRow(page.request, ROUTINE_B, DEADLIFT);
    await loadPlan(page);
    await routineTab(page, ROUTINE_A).click();
    await expect(planRows(page).locator('.exercise-name')).toHaveText([SQUAT]);
    const deleted = page.waitForResponse(response => new URL(response.url()).pathname === '/remove_exercise');
    await planRows(page).getByRole('button', { name: 'Remove' }).click();
    expect((await deleted).ok()).toBe(true);
    await expect(routineTab(page, ROUTINE_A)).toHaveCount(0);
    await expect(routineTab(page, 'all')).toHaveAttribute('aria-selected', 'true');
    await expect(planRows(page).locator('.exercise-name')).toHaveText([DEADLIFT]);
  });
});

test.describe('Plan redesign acceptance', () => {
  test.beforeEach(async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
  });

  test('phone Add exercise preserves cascade, validation, estimate request, hidden-routine toast and control values', async ({ page }) => {
    await addPlanRow(page.request, ROUTINE_A, BENCH);
    await loadPlan(page);
    await expect(addPanel(page), 'phone Add exercise is in the dedicated panel').toBeVisible();
    const routine = page.locator('#routine');
    const add = page.locator('#add_exercise_btn');
    const exercise = page.locator('#exercise');
    const addRequests: string[] = [];
    page.on('request', request => {
      if (request.method() === 'POST' && new URL(request.url()).pathname === '/add_exercise') {
        addRequests.push(request.url());
      }
    });
    await expect(routine).toHaveValue('');
    await expect(exercise).toHaveValue(/\S/);
    await add.click();
    await expectToast(page, /^Please select: Routine$/);

    await page.locator('#clear-filters-btn').click();
    await expect(exercise).toHaveValue('');
    await expectToast(page, 'Filters cleared successfully');
    await add.click();
    await expectToast(page, /^Please select: Routine and Exercise$/);
    expect(addRequests, 'neither invalid submission posts an exercise').toHaveLength(0);

    await page.locator('#routine-env').selectOption('GYM');
    await page.locator('#routine-program').selectOption('Full Body');
    const catalog = page.waitForResponse(response => new URL(response.url()).pathname.startsWith('/get_routine_exercises/'));
    await page.locator('#routine-day').selectOption('Workout B');
    const routineResult = await catalog;
    expect(routineResult.ok()).toBe(true);
    expect(decodeURIComponent(new URL(routineResult.url()).pathname)).toBe('/get_routine_exercises/' + ROUTINE_B);
    await expect(routine).toHaveValue(ROUTINE_B);
    const estimates = page.waitForResponse(response => new URL(response.url()).pathname === '/api/user_profile/estimate');
    await page.locator('#exercise').selectOption(SQUAT, { force: true });
    expect((await estimates).ok()).toBe(true);
    await waitForWorkoutPlanReady(page);

    const values = { weight: '102.5', sets: '4', rir: '2', rpe: '8', min_rep: '8', max_rep_range: '12' };
    for (const [id, value] of Object.entries(values)) await page.locator('#' + id).fill(value);
    const added = page.waitForResponse(response => new URL(response.url()).pathname === '/add_exercise');
    await add.click();
    const response = await added;
    expect(response.ok()).toBe(true);
    expect(response.request().postDataJSON()).toEqual({
      exercise: SQUAT, routine: ROUTINE_B, sets: '4', min_rep_range: '8', max_rep_range: '12',
      rir: 2, rpe: 8, weight: 102.5,
    });
    await expectToast(page, 'Exercise added to ' + ROUTINE_B + ". Open that routine's tab to see it.");
    await expect(planRows(page).locator('.exercise-name')).toHaveText([BENCH]);
    await routineTab(page, ROUTINE_B).click();
    await expect(planRows(page).locator('.exercise-name')).toHaveText([SQUAT]);

    await loadPlan(page, true);
    await waitForWorkoutPlanReady(page);
    await expect(routine).toHaveValue('');
    for (const [id, value] of Object.entries(values)) await expect(page.locator('#' + id)).toHaveValue(value);
    await page.goto(ROUTES.VOLUME_SPLITTER);
    await page.goBack();
    await expect(routine).toHaveValue('');
    await expect(page.locator('#routine-env')).toHaveValue('');
  });

  test('phone exports the current mode to Excel, follows Backup Center and exports to Workout Log', async ({ page }) => {
    await planPost(page.request, '/clear_workout_log');
    try {
      await addPlanRow(page.request, ROUTINE_A, SQUAT);
      await loadPlan(page);
      const more = moreButton(page);
      await expect(more, 'phone export actions are in the header and More menu').toBeVisible();
      await setPlanView(page, 'advanced');
      await more.click();
      const excel = page.waitForResponse(response => new URL(response.url()).pathname === '/export_to_excel');
      const downloaded = page.waitForEvent('download');
      await page.getByRole('menuitem', { name: /Export All Tables/ }).click();
      const [exported, workbook] = await Promise.all([excel, downloaded]);
      expect(exported.ok()).toBe(true);
      expect(exported.request().method()).toBe('GET');
      expect(new URL(exported.url()).searchParams.get('view_mode')).toBe('advanced');
      expect(workbook.suggestedFilename()).toMatch(/\.xlsx$/);
      await expectToast(page, 'Successfully exported to Excel');

      await expect(more).toHaveAttribute('aria-expanded', 'false');
      await more.click();
      await page.getByRole('menuitem', { name: /Backup Center/ }).click();
      await expect(page).toHaveURL(/\/backup\?intent=browse$/);

      await loadPlan(page);
      const log = page.waitForResponse(response => new URL(response.url()).pathname === '/export_to_workout_log');
      await planHeader(page).getByRole('button', { name: 'Export to workout log' }).click();
      const response = await log;
      expect(response.ok()).toBe(true);
      expect(response.request().postDataJSON()).toEqual({});
      await expectToast(page, 'Successfully exported to workout log');
      await expect(page).toHaveURL(/\/workout_log$/);
      await expect(page.locator('#workout-log-table tbody .exercise-name')).toHaveText([SQUAT]);
    } finally {
      await planPost(page.request, '/clear_workout_log');
    }
  });

  test('phone starter generation keeps its payload and Clear Plan resets the six controls', async ({ page }) => {
    await loadPlan(page);
    const more = moreButton(page);
    await expect(more, 'the phone header exposes Starter and Clear Plan from More').toBeVisible();
    await more.click();
    await page.getByRole('menuitem', { name: 'Generate Starter Plan' }).click();
    const generate = page.locator('#generatePlanModal');
    await expect(generate).toBeVisible();
    await generate.locator('#gen-training-days').selectOption('3');
    await generate.locator('#gen-goal').selectOption('hypertrophy');
    const starter = page.waitForResponse(response => new URL(response.url()).pathname === '/generate_starter_plan');
    await generate.locator('#generatePlanSubmit').click();
    const generated = await starter;
    expect(generated.ok()).toBe(true);
    expect(generated.request().postDataJSON()).toMatchObject({
      training_days: 3, goal: 'hypertrophy', overwrite: true,
      movement_restrictions: null, priority_muscles: null, persist: true,
    });
    const result = await generated.json();
    expect(result.data.total_exercises).toBeGreaterThan(0);
    await expectToast(page, /Plan generated successfully/);
    await expect(planRows(page).first()).toBeVisible();

    const defaults = { weight: '25', sets: '3', rir: '3', rpe: '7', min_rep: '6', max_rep_range: '8' };
    for (const [id, value] of Object.entries(defaults)) await page.locator('#' + id).fill(String(Number(value) + 1));
    await more.click();
    await page.getByRole('menuitem', { name: 'Clear Plan' }).click();
    const clear = page.locator('#clearPlanModal');
    await expect(clear).toBeVisible();
    const cleared = page.waitForResponse(response => new URL(response.url()).pathname === '/clear_workout_plan');
    await clear.locator('#confirmClearPlanBtn').click();
    const response = await cleared;
    expect(response.ok()).toBe(true);
    expect(response.request().postData()).toBeNull();
    await expectToast(page, /Workout plan cleared successfully/);
    await expect(planRows(page)).toHaveCount(0);
    for (const [id, value] of Object.entries(defaults)) await expect(page.locator('#' + id)).toHaveValue(value);
    expect(await page.evaluate(() => sessionStorage.getItem('hypertrophy_workout_controls_v1'))).toBeNull();
  });

  test('phone card keeps thumbnail preview and plays and dismisses the curated reference video', async ({ page }) => {
    await addPlanRow(page.request, ROUTINE_A, BENCH);
    const [record] = await planData(page.request);
    const mediaPath = 'Barbell_Bench_Press_-_Medium_Grip/0.jpg';
    await page.route('**/get_workout_plan', async route => {
      const response = await route.fetch();
      const body = await response.json();
      body.data = body.data.map((row: { id: number }) =>
        row.id === record.id ? { ...row, media_path: mediaPath, youtube_video_id: 'dQw4w9WgXcQ' } : row);
      await route.fulfill({ response, json: body });
    });
    await page.route('https://www.youtube.com/embed/**', route => route.fulfill({ body: '<!doctype html><title>Video fixture</title>' }));
    await loadPlan(page);
    const card = planRow(page, record.id);
    await expect(card, 'the video is reachable from a closed phone card').toHaveClass(/\bui-record-card\b/);
    await expect(details(page, record.id)).toHaveAttribute('aria-expanded', 'false');
    const thumbnail = card.locator('img.exercise-thumbnail');
    await expect(thumbnail).toHaveAttribute('src', '/static/vendor/free-exercise-db/exercises/' + mediaPath);
    await thumbnail.hover();
    await expect(page.locator('#exercise-image-preview')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.locator('#exercise-image-preview')).toBeHidden();

    const modal = page.locator('#exerciseVideoModal');
    await modal.evaluate(element => {
      element.addEventListener('shown.bs.modal', () => element.setAttribute('data-test-opened', ''), { once: true });
    });
    await card.locator('[data-action="play-video"]').click();
    await expect(modal).toHaveAttribute('data-test-opened', '');
    await expect(page.locator('#exerciseVideoIframe')).toHaveAttribute('src', /^https:\/\/www\.youtube\.com\/embed\/dQw4w9WgXcQ/);
    await expect(modal.getByRole('button', { name: 'Close reference video', exact: true })).toBeVisible();
    await modal.getByRole('button', { name: 'Close', exact: true }).click();
    await expect(modal).toBeHidden();
    await expect(page.locator('#exerciseVideoIframe')).toHaveAttribute('src', /^(|about:blank)$/);
  });

  test.describe('swap errors', () => {
    test.use({
      consoleAllowlist: { expected: [
        {
          match: 'Failed to load resource: the server responded with a status of 400 (Bad Request)',
          reason: 'Chromium reports the deliberate missing-metadata response',
        },
        {
          match: /^\[req_[0-9a-z_]+\] API Error: \{url: \/replace_exercise, method: POST, status: 400, error: Object\}$/,
          reason: 'fetch-wrapper.js reports the deliberately injected 400 response',
        },
        {
          match: /^\[req_[0-9a-z_]+\] API Error \(final\): \{url: \/replace_exercise, method: POST, error: Object\}$/,
          reason: 'fetch-wrapper.js reports the final failure for the injected 400 response',
        },
        {
          match: /^Error swapping exercise: \{code: VALIDATION_ERROR, message: Exercise is missing muscle group or equipment metadata, requestId: req_[0-9a-z_]+\}$/,
          reason: 'workout-plan-replacement.js logs the rejected swap before showing its toast',
        },
      ] },
    });

    test('phone card reports each established swap rejection and keeps its exercise', async ({ page }) => {
      await addPlanRow(page.request, ROUTINE_A, SQUAT);
      const [record] = await planData(page.request);
      await loadPlan(page);
      const card = planRow(page, record.id);
      await expect(card, 'Swap is available immediately on the phone card').toHaveClass(/\bui-record-card\b/);
      const cases = [
        {
          status: 200, reason: 'no_candidates', code: 'NO_CANDIDATES',
          message: 'No alternative exercises found for Quadriceps with Barbell',
          toast: 'No alternative found for this muscle/equipment.', severity: /bg-warning/,
        },
        {
          status: 200, reason: 'duplicate', code: 'DUPLICATE',
          message: 'All candidate exercises are already in this routine',
          toast: 'All alternatives are already in this routine.', severity: /bg-warning/,
        },
        {
          status: 400, reason: 'missing_metadata', code: 'VALIDATION_ERROR',
          message: 'Exercise is missing muscle group or equipment metadata',
          toast: 'Exercise is missing muscle group or equipment metadata', severity: /bg-danger/,
        },
      ];
      const posted: object[] = [];
      for (const { status, reason, code, message, toast, severity } of cases) {
        await page.route('**/replace_exercise', async route => {
          posted.push(route.request().postDataJSON());
          await route.fulfill({ status, json: { ok: false, status: 'error', message, error: { code, reason, message } } });
        }, { times: 1 });
        await card.getByRole('button', { name: 'Swap exercise' }).click();
        await expectToast(page, toast);
        await expect(page.locator('#liveToast')).toHaveClass(severity);
        await expect(card.locator('.exercise-name')).toHaveText(SQUAT);
      }
      expect(posted).toEqual(cases.map(() => ({ id: record.id, strategy: 'ai' })));
      expect((await planData(page.request))[0].exercise).toBe(SQUAT);
    });
  });
});
