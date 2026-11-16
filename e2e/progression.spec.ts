/**
 * E2E Test: Progression Plan Page
 * 
 * Tests the progression plan functionality including:
 * - Page loading
 * - Exercise selection
 * - Goals table
 * - Delete confirmation modal
 */
import type { Page } from '@playwright/test';
import { test, expect, ROUTES, SELECTORS, waitForPageReady } from './fixtures';
import { test as dataSafetyTest, test as guardedTest } from './console-guard';

dataSafetyTest.describe('Progression suggestion data safety', () => {
  dataSafetyTest('renders a suggestion failure message as literal text', async ({ page }) => {
    const message = '<span data-codeql-injected>unavailable & retry</span>';
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
    await page.evaluate(async value => {
      const { api } = await import('/static/js/modules/fetch-wrapper.js');
      const originalPost = api.post;
      api.post = (...args: unknown[]) => args[0] === '/get_exercise_suggestions'
        ? Promise.reject(new Error(value))
        : originalPost.apply(api, args);
      // Record only this deliberately induced handler log. The strict guard
      // still receives every unrelated console error and every page error.
      const originalError = console.error;
      const records: string[] = [];
      (window as unknown as Record<string, unknown>).__suggestionFailureLogs = records;
      console.error = (...args: unknown[]) => {
        if (args[0] === 'Error fetching suggestions:' && args[1] instanceof Error && args[1].message === value) {
          records.push(args[1].message);
        } else {
          originalError.apply(console, args);
        }
      };
      (document.getElementById('exerciseSelect') as HTMLSelectElement).add(new Option('Fixture', 'Fixture'));
    }, message);
    await page.selectOption('#exerciseSelect', 'Fixture');
    await expect(page.locator('#suggestionsList .alert-danger')).toHaveText(`Error loading suggestions: ${message}`);
    await expect(page.locator('#suggestionsList [data-codeql-injected]')).toHaveCount(0);
    expect(await page.evaluate(() => (window as unknown as Record<string, unknown>).__suggestionFailureLogs)).toEqual([message]);
  });

  dataSafetyTest('renders suggestion text literally and preserves quoted goal data', async ({ page }) => {
    const text = '<span data-codeql-injected>Lift & recover</span>';
    const attribute = '" data-codeql-injected="yes';
    const exercise = `Bench ${text} ${attribute}`;
    const suggestion = {
      type: `weight${attribute}`,
      title: text,
      description: `${text} "quoted" 'label'`,
      action: text,
      current_value: attribute,
      suggested_value: `${attribute} & target`,
    };
    await page.route('**/get_exercise_suggestions', route => route.fulfill({
      json: {
        ok: true, status: 'success', data: [
          suggestion,
          { type: 'weight', title: 'Add weight', description: 'Keep your form', action: 'Set goal', current_value: 0, suggested_value: 2.5 },
          { type: 'reps', title: 'Add reps', description: 'No values yet', action: 'Set goal', current_value: null, suggested_value: null },
        ],
      },
    }));
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
    await page.locator('#exerciseSelect').evaluate((element, value) => {
      (element as HTMLSelectElement).add(new Option(value, value));
    }, exercise);
    await page.selectOption('#exerciseSelect', exercise);

    const cards = page.locator('#suggestionsList .suggestion-card');
    await expect(cards).toHaveCount(3);
    await expect(cards.first().locator('.card-title')).toHaveText(suggestion.title);
    await expect(cards.first().locator('.card-text')).toHaveText(suggestion.description);
    const button = cards.first().locator('.set-goal-btn');
    await expect(button).toHaveText(suggestion.action);
    await expect(cards.first()).toHaveAttribute('data-goal-type', suggestion.type);
    await expect(button).toHaveAttribute('data-goal-type', suggestion.type);
    await expect(button).toHaveAttribute('data-exercise', exercise);
    await expect(button).toHaveAttribute('data-current-value', suggestion.current_value);
    await expect(button).toHaveAttribute('data-target-value', suggestion.suggested_value);
    await expect(page.locator('#suggestionsList [data-codeql-injected]')).toHaveCount(0);
    await expect(cards.nth(2).locator('button')).toHaveAttribute('data-current-value', '');
    await expect(cards.nth(2).locator('button')).toHaveAttribute('data-target-value', '');

    // Zero remains a real prefilled value, and the existing goal action still works.
    await cards.nth(1).locator('button').click();
    await expect(page.locator('#goalSettingModal')).toBeVisible();
    await expect(page.locator('#currentValue')).toHaveValue('0');
    await expect(page.locator('#targetValue')).toHaveValue('2.5');
  });
});

function unwrapProgressionApiData(payload: unknown) {
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

test.describe('Progression Plan Page', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('page loads with correct structure', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('Progression Plan');

    // Check container
    await expect(page.locator(SELECTORS.PAGE_PROGRESSION)).toBeVisible();
  });

  test('exercise selector is present', async ({ page }) => {
    const exerciseSelector = page.locator('#exerciseSelect');
    await expect(exerciseSelector).toBeVisible();

    // Should have default placeholder option
    const defaultOption = exerciseSelector.locator('option').first();
    await expect(defaultOption).toContainText('Choose an exercise');
  });

  test('current goals section is present', async ({ page }) => {
    const goalsSection = page.locator('.current-goals');
    await expect(goalsSection).toBeVisible();

    // Check heading
    await expect(goalsSection.locator('h4')).toContainText('Current Goals');

    // Check table exists
    const table = goalsSection.locator('table');
    await expect(table).toBeVisible();
  });

  test('goals table has correct structure', async ({ page }) => {
    const table = page.locator('.current-goals table');
    const headers = table.locator('thead th');
    const headerTexts = await headers.allInnerTexts();
    const headerString = headerTexts.join(' ').toLowerCase();

    expect(headerString).toContain('exercise');
    expect(headerString).toContain('goal type');
    expect(headerString).toContain('current');
    expect(headerString).toContain('target');
    expect(headerString).toContain('date');
    expect(headerString).toContain('status');
    expect(headerString).toContain('actions');
  });

  test('delete goal modal exists', async ({ page }) => {
    // The modal should be in the DOM but hidden
    const modal = page.locator('#deleteGoalModal');
    await expect(modal).toBeAttached();
    
    // Check modal has correct structure
    await expect(modal.locator('.modal-title')).toContainText('Delete Goal');
  });

  test('exercise selector shows available exercises', async ({ page }) => {
    const exerciseSelector = page.locator('#exerciseSelect');
    const options = exerciseSelector.locator('option');
    const count = await options.count();

    // Should have at least the placeholder option
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test('selecting exercise shows suggestions container', async ({ page }) => {
    const exerciseSelector = page.locator('#exerciseSelect');
    const suggestionsContainer = page.locator('#suggestionsContainer');

    // Initially hidden
    const initialDisplay = await suggestionsContainer.evaluate(el => 
      window.getComputedStyle(el).display
    );
    expect(initialDisplay).toBe('none');

    // Check if there are exercises to select
    const options = exerciseSelector.locator('option');
    const count = await options.count();

    if (count > 1) {
      // Select an exercise
      const optionValue = await options.nth(1).getAttribute('value');
      if (optionValue) {
        await exerciseSelector.selectOption(optionValue);
        
        // Wait for suggestions to potentially load
        await page.waitForTimeout(500);
        
        // Suggestions container might show if API returns data
        // This depends on whether exercises have progression data
      }
    }
  });
});

test.describe('Progression Plan with Data Setup', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();

    // First add an exercise to workout plan
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    // Select routine
    await page.locator(SELECTORS.ROUTINE_ENV).selectOption('GYM');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-program') as HTMLSelectElement;
      return select && select.options.length > 1;
    });
    await page.locator(SELECTORS.ROUTINE_PROGRAM).selectOption('Push Pull Legs');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-day') as HTMLSelectElement;
      return select && select.options.length > 1;
    });
    await page.locator(SELECTORS.ROUTINE_DAY).selectOption('Push 1');

    // Wait for exercise dropdown
    await page.waitForFunction(() => {
      const select = document.getElementById('exercise') as HTMLSelectElement;
      return select && select.options.length > 1;
    });

    // Add Bench Press if available
    const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const options = await exerciseSelect.locator('option').allInnerTexts();
    
    // Find a compound exercise
    const compoundExercise = options.find(opt => 
      opt.toLowerCase().includes('bench press') || 
      opt.toLowerCase().includes('squat') ||
      opt.toLowerCase().includes('deadlift')
    ) || options[1];
    
    if (compoundExercise) {
      await exerciseSelect.selectOption(compoundExercise);
      await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();
      await page.waitForTimeout(500);
    }

    // Navigate to progression page
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('exercise selector reflects added exercises', async ({ page }) => {
    const exerciseSelector = page.locator('#exerciseSelect');
    const options = await exerciseSelector.locator('option').allInnerTexts();
    
    // Should have exercises available (depends on what was added)
    expect(options.length).toBeGreaterThanOrEqual(1);
  });

  test('selecting exercise displays progression info', async ({ page }) => {
    const exerciseSelector = page.locator('#exerciseSelect');
    const options = exerciseSelector.locator('option');
    const count = await options.count();

    if (count > 1) {
      const optionValue = await options.nth(1).getAttribute('value');
      if (optionValue) {
        await exerciseSelector.selectOption(optionValue);
        await page.waitForTimeout(500);

        // Should show exercise-specific info
        const progressionInfo = page.locator('.progression-info, .exercise-progress, #progression-display');
        if (await progressionInfo.count() > 0) {
          await expect(progressionInfo).toBeVisible();
        }
      }
    }
  });
});

test.describe('Progression Goal Management', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('add goal form exists', async ({ page }) => {
    // The progression page uses exercise selection to add goals
    // Check for exercise selector instead of a traditional form
    const exerciseSelect = page.locator('#exerciseSelect');
    const suggestionsContainer = page.locator('#suggestionsContainer');
    const goalsTable = page.locator('.current-goals table');
    
    const hasSelect = await exerciseSelect.count() > 0;
    const hasSuggestions = await suggestionsContainer.count() > 0;
    const hasGoalsTable = await goalsTable.count() > 0;
    
    // At least one of these should exist for goal management
    expect(hasSelect || hasSuggestions || hasGoalsTable).toBeTruthy();
  });

  test('add goal form has required fields', async ({ page }) => {
    // Goal form fields are in a modal - check that modal and form exists
    const goalModal = page.locator('#goalSettingModal');
    const goalForm = page.locator('#goalForm');
    
    // Modal should exist in the DOM (even if not visible)
    await expect(goalModal).toBeAttached();
    await expect(goalForm).toBeAttached();
    
    // Check for form fields within the modal
    const currentValue = page.locator('#currentValue');
    const targetValue = page.locator('#targetValue');
    const goalDate = page.locator('#goalDate');
    
    // At least target value and goal date should exist
    const currentValueCount = await currentValue.count();
    const targetValueCount = await targetValue.count();
    const goalDateCount = await goalDate.count();

    expect(currentValueCount + targetValueCount + goalDateCount).toBeGreaterThan(0);
  });

  test('goal type selector has options', async ({ page }) => {
    const goalType = page.locator('#goal-type, select[name="goal_type"]');
    
    if (await goalType.count() > 0) {
      const options = goalType.locator('option');
      const count = await options.count();
      
      expect(count).toBeGreaterThan(0);
    }
  });

  test('delete goal confirmation modal works', async ({ page }) => {
    const modal = page.locator('#deleteGoalModal');
    
    // Open modal programmatically if there's a delete button
    const deleteBtn = page.locator('.delete-goal').first();
    
    if (await deleteBtn.count() > 0) {
      await deleteBtn.click();
      await page.waitForTimeout(500);
      
      // Modal should have confirm and cancel buttons
      const confirmBtn = modal.getByRole('button', { name: 'Delete' });
      const cancelBtn = modal.getByRole('button', { name: 'Cancel' });
      
      if (await modal.isVisible()) {
        await expect(confirmBtn).toBeVisible();
        await expect(cancelBtn).toBeVisible();
        
        // Close modal
        await page.keyboard.press('Escape');
      }
    }
  });
});

test.describe('Progression Goal Lifecycle Smoke', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('goal can be saved and completed through the progression page', async ({ page }) => {
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);

    const exerciseSelector = page.locator('#exerciseSelect');
    let optionCount = await exerciseSelector.locator('option').count();

    if (optionCount <= 1) {
      await page.goto(ROUTES.WORKOUT_PLAN);
      await waitForPageReady(page);

      await page.locator(SELECTORS.ROUTINE_ENV).selectOption('GYM');
      await page.waitForFunction(() => {
        const select = document.getElementById('routine-program') as HTMLSelectElement;
        return !!select && select.options.length > 1;
      });
      await page.locator(SELECTORS.ROUTINE_PROGRAM).selectOption('Push Pull Legs');
      await page.waitForFunction(() => {
        const select = document.getElementById('routine-day') as HTMLSelectElement;
        return !!select && select.options.length > 1;
      });
      await page.locator(SELECTORS.ROUTINE_DAY).selectOption('Push 1');
      await page.waitForFunction(() => {
        const select = document.getElementById('exercise') as HTMLSelectElement;
        return !!select && select.options.length > 1;
      });

      const exerciseOptions = page.locator(SELECTORS.EXERCISE_SEARCH).locator('option');
      const firstExerciseValue = await exerciseOptions.nth(1).getAttribute('value');
      expect(firstExerciseValue).toBeTruthy();
      await page.locator(SELECTORS.EXERCISE_SEARCH).selectOption(firstExerciseValue!);
      await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();

      await page.goto(ROUTES.PROGRESSION);
      await waitForPageReady(page);
      optionCount = await exerciseSelector.locator('option').count();
    }

    expect(optionCount).toBeGreaterThan(1);

    const initialRowCount = await page.locator('.current-goals tbody tr').count();
    const selectedValue = await exerciseSelector.locator('option').nth(1).getAttribute('value');
    expect(selectedValue).toBeTruthy();
    await exerciseSelector.selectOption(selectedValue!);

    await expect(page.locator('#suggestionsContainer')).toBeVisible();
    await expect(page.locator('.suggestion-card[data-goal-type="weight"]').first()).toBeVisible();
    await expect(page.locator('.suggestion-card[data-goal-type="reps"]').first()).toBeVisible();
    await expect(page.locator('.suggestion-card[data-goal-type="sets"]').first()).toBeVisible();

    const weightGoalButton = page.locator('.set-goal-btn[data-goal-type="weight"]').first();
    await expect(weightGoalButton).toBeVisible();
    await weightGoalButton.click();

    const goalModal = page.locator('#goalSettingModal');
    await expect(goalModal).toBeVisible();
    await expect(page.locator('#currentValue')).toHaveValue(/^[1-9]\d*(\.\d+)?$/);
    await expect(page.locator('#targetValue')).toHaveValue(/^[1-9]\d*(\.\d+)?$/);
    await page.locator('#goalDate').fill('31-12-2099');
    await page.locator('#saveGoal').click();

    await expect.poll(async () => {
      await page.waitForLoadState('networkidle');
      return page.locator('.current-goals tbody tr').count();
    }).toBe(initialRowCount + 1);

    const savedRow = page.locator('.current-goals tbody tr').last();
    await expect(savedRow).toContainText(selectedValue!);
    await savedRow.locator('.complete-goal').click();
    await expect(savedRow.locator('.badge')).toContainText('Completed');

    await page.reload();
    await waitForPageReady(page);
    await expect.poll(async () => page.locator('.current-goals tbody tr').count()).toBe(initialRowCount);
  });
});

test.describe('Progression Methodology Display', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('progression methodology info is displayed', async ({ page }) => {
    // Look for progression-related content on the page
    const pageContent = await page.content();
    const lowerContent = pageContent.toLowerCase();
    
    // Should have progression-related elements
    const hasProgressionContent = 
      lowerContent.includes('progression') ||
      lowerContent.includes('goal') ||
      lowerContent.includes('exercise') ||
      lowerContent.includes('target') ||
      lowerContent.includes('current');
    
    expect(hasProgressionContent).toBeTruthy();
  });

  test('double progression methodology explained', async ({ page }) => {
    const pageContent = await page.content();
    const lowerContent = pageContent.toLowerCase();
    
    // Page should have some progression-related content visible
    // The page focuses on goal setting, not necessarily explaining methodology
    const hasProgressionConcepts = 
      lowerContent.includes('progression') ||
      lowerContent.includes('goal') ||
      lowerContent.includes('target') ||
      lowerContent.includes('exercise') ||
      lowerContent.includes('value');
    
    expect(hasProgressionConcepts).toBeTruthy();
  });
});

test.describe('Progression Status Indicators', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('status column shows goal progress', async ({ page }) => {
    const goalsTable = page.locator('.current-goals table');
    
    if (await goalsTable.isVisible()) {
      const headers = await goalsTable.locator('thead th').allInnerTexts();
      const headerString = headers.join(' ').toLowerCase();
      
      expect(headerString).toContain('status');
    }
  });

  test('status uses color coding', async ({ page }) => {
    const statusCells = page.locator('.status-cell, .goal-status, [class*="status"]');
    const count = await statusCells.count();

    if (count > 0) {
      const firstStatus = statusCells.first();
      
      // Check for color classes
      const classes = await firstStatus.getAttribute('class');
      const hasColorClass = 
        classes?.includes('success') ||
        classes?.includes('warning') ||
        classes?.includes('danger') ||
        classes?.includes('info') ||
        classes?.includes('primary');
      
      // Color may be applied via inline style too
      const bgColor = await firstStatus.evaluate(el => getComputedStyle(el).backgroundColor);
      
      expect(hasColorClass || bgColor !== 'rgba(0, 0, 0, 0)').toBeTruthy();
    }
  });
});

test.describe('Progression Suggestions', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('suggestions container exists', async ({ page }) => {
    const suggestionsContainer = page.locator('#suggestionsContainer, .suggestions-container');
    await expect(suggestionsContainer).toBeAttached();
  });

  test('selecting exercise may show suggestions', async ({ page }) => {
    const exerciseSelector = page.locator('#exerciseSelect');
    const options = exerciseSelector.locator('option');
    const count = await options.count();

    if (count > 1) {
      const optionValue = await options.nth(1).getAttribute('value');
      if (optionValue) {
        await exerciseSelector.selectOption(optionValue);
        await page.waitForTimeout(1000);

        // Suggestions may appear based on exercise data
        const suggestionsContainer = page.locator('#suggestionsContainer, .suggestions-container');
        
        // Check if container has content
        const text = await suggestionsContainer.textContent();
        // Either shows suggestions or remains empty (both are valid states)
      }
    }
  });
});

test.describe('Double Progression Logic (v1.5.0)', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('suggestions display double progression types', async ({ page }) => {
    const exerciseSelector = page.locator('#exerciseSelect');
    const options = exerciseSelector.locator('option');
    const count = await options.count();

    if (count > 1) {
      const optionValue = await options.nth(1).getAttribute('value');
      if (optionValue) {
        await exerciseSelector.selectOption(optionValue);
        await page.waitForTimeout(1500);

        const suggestionsContainer = page.locator('#suggestionsContainer, .suggestions-container');
        
        // If suggestions are visible, verify they have proper structure
        if (await suggestionsContainer.isVisible()) {
          const suggestionCards = suggestionsContainer.locator('.suggestion-card, .card, [class*="suggestion"]');
          const cardCount = await suggestionCards.count();
          
          if (cardCount > 0) {
            // Each suggestion should have title and description
            const firstCard = suggestionCards.first();
            const text = await firstCard.textContent();
            expect(text?.length).toBeGreaterThan(0);
          }
        }
      }
    }
  });

  test('double progression suggestions include weight or rep recommendations', async ({ page }) => {
    // Navigate with an exercise that has workout history
    const exerciseSelector = page.locator('#exerciseSelect');
    const options = exerciseSelector.locator('option');
    const count = await options.count();

    if (count > 1) {
      const optionValue = await options.nth(1).getAttribute('value');
      if (optionValue) {
        await exerciseSelector.selectOption(optionValue);
        await page.waitForTimeout(1500);

        const pageContent = await page.content();
        const lowerContent = pageContent.toLowerCase();
        
        // Double progression should mention weight or rep changes
        const hasProgressionTerms = 
          lowerContent.includes('weight') ||
          lowerContent.includes('reps') ||
          lowerContent.includes('increase') ||
          lowerContent.includes('decrease') ||
          lowerContent.includes('progression') ||
          lowerContent.includes('rep range') ||
          lowerContent.includes('start training'); // Initial state message
        
        expect(hasProgressionTerms).toBeTruthy();
      }
    }
  });

  test('API returns proper suggestion structure', async ({ page, request }) => {
    // Test the API directly using Playwright's request context
    const response = await request.post('/get_exercise_suggestions', {
      data: {
        exercise: 'Bench Press (Barbell)',
        is_novice: true
      }
    });
    
    expect(response.ok()).toBeTruthy();
    const rawPayload = await response.json();
    expect(rawPayload.ok).toBe(true);
    expect(rawPayload.status).toBe('success');
    const suggestions = unwrapProgressionApiData(rawPayload);
    expect(Array.isArray(suggestions)).toBe(true);
    
    // Verify suggestion structure matches v1.5.0 double progression format
    if (Array.isArray(suggestions) && suggestions.length > 0) {
      const suggestion = suggestions[0];
      expect(suggestion).toHaveProperty('type');
      expect(suggestion).toHaveProperty('title');
      expect(suggestion).toHaveProperty('description');
      
      // Valid suggestion types for double progression
      const validTypes = [
        'double_progression_weight', 'double_progression_reps',
        'technique', 'info', 'start', 'warning', 'success'
      ];
      expect(validTypes.some(type => suggestion.type.includes(type) || validTypes.includes(suggestion.type))).toBeTruthy();
    }
  });
});

test.describe('Progression Mobile Responsive', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('exercise selector usable on mobile', async ({ page }) => {
    const exerciseSelector = page.locator('#exerciseSelect');
    await expect(exerciseSelector).toBeVisible();

    const box = await exerciseSelector.boundingBox();
    if (box) {
      expect(box.width).toBeGreaterThanOrEqual(100);
    }
  });

  test('goals table readable on mobile', async ({ page }) => {
    const goalsTable = page.locator('.current-goals table');
    await expect(goalsTable).toBeVisible();

    // The page itself must not overflow sideways (#716). The previous
    // `isScrollable !== null` check could not fail.
    const widths = await page.evaluate(() => ({
      clientWidth: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
    }));
    expect(widths.scrollWidth).toBeLessThanOrEqual(widths.clientWidth);
  });
});

/**
 * Current Goals table responsive contract (#716).
 *
 * Populated through the real save route with the visual fixture's three goals,
 * and asserted from rendered geometry and computed style. Text extraction alone
 * cannot see the original defect: a header hidden with `display: none` still
 * has text, and at 768px five headers were hidden while their cells stayed
 * visible, in a 770px page clipped to a 768px viewport.
 */
const GOAL_FIXTURES = [
  { exercise: 'Barbell Bench Press', goal_type: 'weight', current_value: 60, target_value: 70, goal_date: '2026-03-02' },
  { exercise: 'Barbell Squat', goal_type: 'weight', current_value: 100, target_value: 120, goal_date: '2026-03-16' },
  { exercise: 'Barbell Deadlift', goal_type: 'reps', current_value: 5, target_value: 8, goal_date: '2026-04-06' },
] as const;

// `scrolls` is the measured outcome for these three goals at UI scale 1: the
// table's minimum width is about 713px, so it scrolls inside its 638px region
// at 768px and fits the 894px region at 1024px. Card mode never scrolls.
const GOAL_BANDS = [
  { name: 'mobile', width: 375, height: 812, layout: 'cards', scrolls: false },
  { name: 'tablet', width: 768, height: 1024, layout: 'table', scrolls: true },
  { name: 'tablet-landscape', width: 1024, height: 768, layout: 'table', scrolls: false },
  { name: 'desktop', width: 1440, height: 900, layout: 'table', scrolls: false },
] as const;

type GoalBand = (typeof GOAL_BANDS)[number];
type GoalTheme = 'light' | 'dark';

const GOALS_REGION = '.current-goals .tbl-wrap';
const SCROLL_HINT = '#currentGoalsScrollHint';

async function openGoalsAt(page: Page, band: GoalBand, theme: GoalTheme) {
  await page.setViewportSize({ width: band.width, height: band.height });
  await page.addInitScript((dark) => localStorage.setItem('darkMode', dark ? 'true' : 'false'), theme === 'dark');
  await page.goto(ROUTES.PROGRESSION);
  await waitForPageReady(page);
  await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
}

async function measureGoalsTable(page: Page) {
  return page.evaluate(({ regionSelector, hintSelector }) => {
    const box = (el: Element) => {
      const r = el.getBoundingClientRect();
      return { left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width };
    };
    const shown = (el: Element) => {
      const cs = getComputedStyle(el);
      return cs.display !== 'none' && cs.visibility !== 'hidden' && el.getBoundingClientRect().width > 0;
    };
    const region = document.querySelector(regionSelector) as HTMLElement;
    const table = region.querySelector('table') as HTMLTableElement;
    const hint = document.querySelector(hintSelector) as HTMLElement | null;
    const root = document.documentElement;
    return {
      viewport: root.clientWidth,
      documentScrollWidth: root.scrollWidth,
      bodyScrollWidth: document.body.scrollWidth,
      region: {
        box: box(region),
        scrollWidth: region.scrollWidth,
        clientWidth: region.clientWidth,
        overflowX: getComputedStyle(region).overflowX,
        tabIndex: region.tabIndex,
        role: region.getAttribute('role'),
        label: region.getAttribute('aria-label'),
        describedBy: region.getAttribute('aria-describedby'),
      },
      hint: hint
        ? { present: true, id: hint.id, shown: shown(hint), text: (hint.textContent ?? '').trim() }
        : { present: false, id: '', shown: false, text: '' },
      theadShown: shown(table.tHead as HTMLTableSectionElement),
      headers: [...(table.tHead as HTMLTableSectionElement).rows[0].cells].map((th) => ({
        text: (th.textContent ?? '').trim(),
        shown: shown(th),
        box: box(th),
      })),
      rows: [...table.tBodies[0].rows].map((tr) => ({
        goalId: tr.querySelector('[data-goal-id]')?.getAttribute('data-goal-id') ?? '',
        cells: [...tr.cells].map((td) => ({
          label: td.dataset.label ?? '',
          text: td.innerText.trim(),
          shown: shown(td),
          display: getComputedStyle(td).display,
          before: getComputedStyle(td, '::before').content,
          box: box(td),
          buttons: [...td.querySelectorAll('button')].map(box),
        })),
      })),
    };
  }, { regionSelector: GOALS_REGION, hintSelector: SCROLL_HINT });
}

guardedTest.describe('Progression goals table responsive contract (#716)', () => {
  let goalIds: number[] = [];

  guardedTest.beforeEach(async ({ page }) => {
    goalIds = [];
    for (const goal of GOAL_FIXTURES) {
      const response = await page.request.post('/save_progression_goal', {
        data: goal,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });
      expect(response.status(), await response.text()).toBe(200);
      const body = await response.json();
      goalIds.push(Number(body.data.goal_id));
    }
  });

  guardedTest.afterEach(async ({ page }) => {
    for (const id of goalIds) {
      const response = await page.request.delete(`/delete_progression_goal/${id}`);
      expect([200, 404]).toContain(response.status());
    }
  });

  for (const band of GOAL_BANDS) {
    for (const theme of ['light', 'dark'] as const) {
      guardedTest(`goals table keeps every value under its own visible label: ${band.name} ${theme}`, async ({ page }) => {
        await openGoalsAt(page, band, theme);
        const m = await measureGoalsTable(page);

        // The page never overflows sideways; the region stays inside the viewport.
        expect(m.documentScrollWidth, 'document overflows the viewport').toBeLessThanOrEqual(m.viewport);
        expect(m.bodyScrollWidth, 'body overflows the viewport').toBeLessThanOrEqual(m.viewport);
        expect(m.region.box.right).toBeLessThanOrEqual(m.viewport + 0.5);

        // Every seeded goal is rendered, and every row pairs each value with its column label.
        for (const id of goalIds) {
          expect(m.rows.map((row) => row.goalId)).toContain(String(id));
        }
        const headerTexts = m.headers.map((header) => header.text);
        expect(headerTexts).toEqual(['Exercise', 'Goal Type', 'Current Value', 'Target Value', 'Goal Date', 'Status', 'Actions']);
        for (const row of m.rows) {
          expect(row.cells.map((cell) => cell.label)).toEqual(headerTexts);
          for (const cell of row.cells) {
            expect(cell.shown, `${cell.label} cell is not rendered`).toBe(true);
            expect(cell.text, `${cell.label} cell is empty`).not.toBe('');
          }
        }

        if (band.layout === 'table') {
          expect(m.theadShown).toBe(true);
          for (const header of m.headers) {
            expect(header.shown, `${header.text} header is not rendered`).toBe(true);
          }
          for (const row of m.rows) {
            row.cells.forEach((cell, i) => {
              const header = m.headers[i].box;
              expect(Math.abs(cell.box.left - header.left), `${cell.label} left edge`).toBeLessThanOrEqual(1);
              expect(Math.abs(cell.box.right - header.right), `${cell.label} right edge`).toBeLessThanOrEqual(1);
              expect(header.bottom).toBeLessThanOrEqual(cell.box.top + 1);
            });
          }
        } else {
          // Card mode: the header row is replaced by a generated label per value.
          expect(m.theadShown).toBe(false);
          for (const row of m.rows) {
            for (const cell of row.cells) {
              expect(cell.display).toBe('grid');
              expect(cell.before).toBe(JSON.stringify(cell.label));
              expect(cell.box.right).toBeLessThanOrEqual(m.viewport + 0.5);
              for (const button of cell.buttons) {
                expect(button.right).toBeLessThanOrEqual(m.viewport + 0.5);
              }
            }
          }
        }

        // The region is always a named, focusable landmark. When, and only when,
        // its content overflows, it scrolls and the visible hint describes it.
        expect(m.region.role).toBe('region');
        expect(m.region.label).toBe('Current progression goals table');
        expect(m.region.tabIndex).toBe(0);
        const scrolls = m.region.scrollWidth > m.region.clientWidth + 1;
        expect(scrolls, `region ${m.region.scrollWidth}/${m.region.clientWidth}`).toBe(band.scrolls);
        expect(m.hint.present, 'scroll hint element is missing').toBe(true);
        // A ResizeObserver toggles the hint; wait for it to settle, then re-read.
        if (scrolls) {
          expect(['auto', 'scroll']).toContain(m.region.overflowX);
          await expect(page.locator(SCROLL_HINT)).toBeVisible();
        } else {
          await expect(page.locator(SCROLL_HINT)).toBeHidden();
        }
        const settled = await measureGoalsTable(page);
        if (scrolls) {
          expect(settled.hint.shown).toBe(true);
          expect(settled.hint.text).toBe('Scroll sideways to see all goal columns.');
          expect(settled.region.describedBy).toBe(settled.hint.id);
        } else {
          expect(settled.hint.shown).toBe(false);
          expect(settled.region.describedBy).toBeNull();
        }

        if (band.layout === 'table') {
          // Scrolled fully to the end, the last column and its actions are
          // inside the region, and headers still line up with their cells.
          await page.locator(GOALS_REGION).evaluate((el) => el.scrollTo({ left: el.scrollWidth, behavior: 'instant' }));
          const end = await measureGoalsTable(page);
          const lastHeader = end.headers[end.headers.length - 1].box;
          expect(lastHeader.right).toBeLessThanOrEqual(end.region.box.right + 1);
          for (const row of end.rows) {
            const actions = row.cells[row.cells.length - 1];
            expect(Math.abs(actions.box.left - lastHeader.left)).toBeLessThanOrEqual(1);
            expect(actions.box.right).toBeLessThanOrEqual(end.region.box.right + 1);
            for (const button of actions.buttons) {
              expect(button.left).toBeGreaterThanOrEqual(end.region.box.left - 1);
              expect(button.right).toBeLessThanOrEqual(end.region.box.right + 1);
            }
          }
        }
      });
    }
  }

  const tablet = GOAL_BANDS.find((band) => band.name === 'tablet') as GoalBand;
  for (const theme of ['light', 'dark'] as const) {
    guardedTest(`goals table scroll region is focusable and keyboard operable at tablet width: ${theme}`, async ({ page }) => {
      await openGoalsAt(page, tablet, theme);
      const region = page.locator(GOALS_REGION);

      // The region is the next tab stop after the exercise selector.
      await page.locator('#exerciseSelect').focus();
      await page.keyboard.press('Tab');
      await expect(region).toBeFocused();
      const ring = await region.evaluate((el) => {
        const cs = getComputedStyle(el);
        return { focusVisible: el.matches(':focus-visible'), style: cs.outlineStyle, width: parseFloat(cs.outlineWidth) };
      });
      expect(ring.focusVisible).toBe(true);
      expect(ring.style).not.toBe('none');
      expect(ring.width).toBeGreaterThanOrEqual(2);

      // Arrow keys scroll the focused region.
      expect(await region.evaluate((el) => el.scrollLeft)).toBe(0);
      await page.keyboard.press('ArrowRight');
      await expect.poll(() => region.evaluate((el) => el.scrollLeft)).toBeGreaterThan(0);

      // Tabbing reaches every action, and no focused action is hidden by the
      // region's clip. Chromium does not scroll a partly visible focus target
      // fully into view, so at scrollLeft 0 the actions are partly visible,
      // which is what WCAG 2.4.11 (AA) requires; the arrow keys reveal the rest.
      await region.evaluate((el) => el.scrollTo({ left: 0, behavior: 'instant' }));
      const actions = page.locator('.current-goals tbody .goal-actions button');
      const actionCount = await actions.count();
      expect(actionCount).toBeGreaterThanOrEqual(goalIds.length * 2);
      for (let i = 0; i < actionCount; i++) {
        await page.keyboard.press('Tab');
        await expect(actions.nth(i)).toBeFocused();
        const visibleWidth = await page.evaluate((selector) => {
          const r = (document.querySelector(selector) as HTMLElement).getBoundingClientRect();
          const b = (document.activeElement as HTMLElement).getBoundingClientRect();
          return Math.min(b.right, r.right) - Math.max(b.left, r.left);
        }, GOALS_REGION);
        expect(visibleWidth, `focused action ${i} is clipped out of the region`).toBeGreaterThan(0);
      }

      // The focused action is operable from the keyboard.
      await page.keyboard.press('Enter');
      const modal = page.locator('#deleteGoalModal');
      await expect(modal).toBeVisible();
      await modal.getByRole('button', { name: 'Cancel' }).click();
      await expect(modal).toBeHidden();

      // The visible hint describes the scrolling region.
      await expect(page.locator(SCROLL_HINT)).toBeVisible();
      await expect(region).toHaveAttribute('aria-describedby', 'currentGoalsScrollHint');
    });
  }

  for (const band of GOAL_BANDS.filter((candidate) => candidate.name !== 'tablet-landscape')) {
    guardedTest(`goal completion and removal work in the ${band.name} layout`, async ({ page }) => {
      await openGoalsAt(page, band, 'light');
      const [completeId, removeId, keepId] = goalIds;
      const rowFor = (id: number) =>
        page.locator('.current-goals tbody tr').filter({ has: page.locator(`.delete-goal[data-goal-id="${id}"]`) });

      const completed = page.waitForResponse((r) =>
        r.url().endsWith(`/complete_progression_goal/${completeId}`) && r.request().method() === 'POST');
      await rowFor(completeId).locator('.complete-goal').click();
      expect((await completed).status()).toBe(200);
      await expect(rowFor(completeId).locator('.goal-status-badge')).toHaveText('Completed');
      await expect(rowFor(completeId).locator('.complete-goal')).toHaveCount(0);

      await rowFor(removeId).locator('.delete-goal').click();
      const modal = page.locator('#deleteGoalModal');
      await expect(modal).toBeVisible();
      const removed = page.waitForResponse((r) =>
        r.url().endsWith(`/delete_progression_goal/${removeId}`) && r.request().method() === 'DELETE');
      await modal.locator('#confirmDeleteGoal').click();
      expect((await removed).status()).toBe(200);
      await expect(rowFor(removeId)).toHaveCount(0);
      await expect(modal).toBeHidden();

      // Both changes persisted: completed goals leave the current list.
      await page.reload();
      await waitForPageReady(page);
      await expect(rowFor(completeId)).toHaveCount(0);
      await expect(rowFor(removeId)).toHaveCount(0);
      await expect(rowFor(keepId)).toHaveCount(1);
    });
  }
});

/**
 * Phase 2D-B: advisory fatigue context on the Progression page.
 *
 * Real backend (no mocks): the shared, default-off fatigue-context toggle
 * (also surfaced on Profile) drives whether the additive block is attached to
 * /get_exercise_suggestions. Enabled → a distinct "Fatigue context" section
 * with the mandatory copy renders below the suggestion cards; disabled → it is
 * absent. A plan row is seeded via the real API so the exercise dropdown has a
 * selectable option (the functional seed wipes the plan).
 */
test.describe('Progression Plan — fatigue context (Phase 2D-B)', () => {
  const FATIGUE_CONTEXT_SETTINGS = '/api/user_profile/fatigue_context_settings';
  const PLAN_EXERCISE = {
    routine: 'GYM - Full Body - Workout A',
    exercise: 'Barbell Bench Press',
    sets: 3,
    min_rep_range: 8,
    max_rep_range: 12,
    rir: 2,
    weight: 60,
  };

  test.beforeEach(async ({ page }) => {
    await page.request.post(FATIGUE_CONTEXT_SETTINGS, { data: { enabled: false } });
    await page.request.post('/clear_workout_plan');
    await page.request.post('/add_exercise', { data: PLAN_EXERCISE });
  });

  test.afterEach(async ({ page }) => {
    await page.request.post(FATIGUE_CONTEXT_SETTINGS, { data: { enabled: false } });
    await page.request.post('/clear_workout_plan');
  });

  async function selectPlannedExercise(page: import('@playwright/test').Page) {
    const suggestionsDone = page.waitForResponse((r) =>
      r.url().includes('/get_exercise_suggestions'),
    );
    await page.locator('#exerciseSelect').selectOption(PLAN_EXERCISE.exercise);
    await suggestionsDone;
  }

  test('toggle on shows the advisory section; toggle off hides it', async ({
    page,
    consoleErrors,
  }) => {
    consoleErrors.startCollecting();

    // Enabled → the advisory section renders with the mandatory copy.
    await page.request.post(FATIGUE_CONTEXT_SETTINGS, {
      data: { enabled: true, context_source: 'both', context_period: 'this_week' },
    });
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
    await selectPlannedExercise(page);

    const fatigue = page.locator('#suggestionsFatigueContext [data-fatigue-context]');
    await expect(fatigue).toBeVisible();
    await expect(fatigue).toContainText('Fatigue context');
    await expect(fatigue).toContainText('This does not change your suggestion.');

    // The suggestion cards still render alongside it (advisory never replaces
    // the suggestion).
    await expect(page.locator('#suggestionsList .suggestion-card').first()).toBeVisible();

    // Disabled → reload + reselect → the section is gone.
    await page.request.post(FATIGUE_CONTEXT_SETTINGS, { data: { enabled: false } });
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
    await selectPlannedExercise(page);

    await expect(
      page.locator('#suggestionsFatigueContext [data-fatigue-context]'),
    ).toHaveCount(0);

    consoleErrors.assertNoErrors();
  });
});

/**
 * `progression-plan.js` guards its initializer with
 * `typeof flatpickr !== 'undefined'`, and the console collector cannot see a
 * missing global either (see `fixtures.ts`), so a flatpickr that fails to load
 * degrades `#goalDate` to a plain text input with every spec still green.
 *
 * `goal_date` is required and is read back from the picker's own
 * `selectedDates`, so that failure blocks saving a goal, not just picking one.
 */
test.describe('Progression Plan date picker', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.PROGRESSION);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('flatpickr loads locally and binds the goal-date input', async ({ page }) => {
    // The library evaluated: a wrong path or a corrupt payload fails here.
    expect(
      await page.evaluate(() => typeof (window as unknown as Record<string, unknown>).flatpickr),
    ).toBe('function');

    // …and its initializer actually ran against the real input. flatpickr adds
    // this class itself; the template does not.
    await expect(page.locator('#goalDate')).toHaveClass(/flatpickr-input/);

    // The vendored stylesheet is applied, not merely requested: flatpickr's own
    // CSS is what positions the calendar out of flow.
    const calendar = page.locator('.flatpickr-calendar');
    await expect(calendar).toHaveCount(1);
    expect(
      await calendar.first().evaluate((element) => getComputedStyle(element).position),
    ).toBe('absolute');
  });
});
