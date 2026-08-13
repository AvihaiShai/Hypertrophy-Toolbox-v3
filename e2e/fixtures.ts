/**
 * Common test fixtures and utilities for E2E tests
 */
import { test as base, expect, Page } from '@playwright/test';

/**
 * Console error collector - fails test if uncaught JS errors occur
 */
export interface ConsoleErrorCollector {
  errors: string[];
  startCollecting: () => void;
  assertNoErrors: () => void;
}

/**
 * Extended test fixture with console error tracking
 */
export const test = base.extend<{ consoleErrors: ConsoleErrorCollector }>({
  consoleErrors: async ({ page }, use) => {
    const errors: string[] = [];
    
    const collector: ConsoleErrorCollector = {
      errors,
      startCollecting: () => {
        page.on('console', (msg) => {
          if (msg.type() === 'error') {
            // Ignore common non-critical errors
            const text = msg.text();
            if (
              !text.includes('favicon') &&
              !text.includes('Source map') &&
              !text.includes('[HMR]') &&
              !text.includes('404') &&
              !text.includes('Failed to load resource') &&
              !text.includes('not found') && // Ignore "Exercise with ID X not found" errors
              !text.includes('replace_exercise') && // Ignore replace exercise API errors in tests
              !text.includes('swapping exercise') && // Ignore swap exercise errors
              !text.includes('UNKNOWN_ERROR') && // Ignore unknown error responses from API tests
              !text.includes('NETWORK_ERROR') && // Ignore network errors during tests
              !text.includes('Failed to fetch') && // Ignore fetch failures
              !text.includes('Script error') && // Ignore cross-origin script errors
              !text.includes('Global error caught') && // Ignore global error handler logs
              !text.includes('API Error') // Ignore API error logs during testing
            ) {
              errors.push(text);
            }
          }
        });
        
        page.on('pageerror', (error) => {
          // Ignore common non-critical page errors.
          //
          // NOTE FOR ANYONE RELYING ON THIS AS AN ORACLE: the filters below —
          // `is not defined` in particular, and `404` / `Failed to load
          // resource` above — mean a missing third-party global raises nothing
          // this collector will report. A library that failed to load is
          // therefore invisible here, and any spec that needs to know it
          // loaded has to assert that directly.
          const msg = error.message;
          if (
            !msg.includes('classList') && // Null reference on classList
            !msg.includes('Cannot read properties of null') && // General null reference
            !msg.includes('Cannot read properties of undefined') && // General undefined reference
            !msg.includes('Script error') && // Cross-origin errors
            !msg.includes('is not defined') // Ignore undefined function errors during testing
          ) {
            errors.push(`Page Error: ${msg}`);
          }
        });
      },
      assertNoErrors: () => {
        if (errors.length > 0) {
          throw new Error(`Console errors detected:\n${errors.join('\n')}`);
        }
      },
    };
    
    await use(collector);
  },
});

export { expect };

/**
 * Route definitions for easy reference
 */
export const ROUTES = {
  HOME: '/',
  WORKOUT_PLAN: '/workout_plan',
  WORKOUT_LOG: '/workout_log',
  WEEKLY_SUMMARY: '/weekly_summary',
  SESSION_SUMMARY: '/session_summary',
  PROGRESSION: '/progression',
  BODY_COMPOSITION: '/body_composition',
  VOLUME_SPLITTER: '/volume_splitter',
  BACKUP: '/backup',
  USER_PROFILE: '/user_profile',
  // templates/fatigue.html links no page bundle at all, so this route is
  // painted entirely by the shared global bundles — the highest shared-CSS
  // exposure in the app. Added to the visual matrix by WP4.4-a under owner
  // ruling N7 so that arc has a pixel oracle here.
  FATIGUE: '/fatigue',
} as const;

/**
 * API endpoints for direct testing (v1.5.0+)
 */
export const API_ENDPOINTS = {
  // Plan Generator
  GENERATE_PLAN: '/generate_starter_plan',
  GENERATOR_OPTIONS: '/get_generator_options',
  
  // Pattern Coverage Analysis
  PATTERN_COVERAGE: '/api/pattern_coverage',
  
  // Double Progression
  EXERCISE_SUGGESTIONS: '/get_exercise_suggestions',
  
  // Workout Plan
  GET_WORKOUT_PLAN: '/get_workout_plan',
  ADD_EXERCISE: '/add_exercise',
  REMOVE_EXERCISE: '/remove_exercise',
  UPDATE_EXERCISE: '/update_exercise',
  REPLACE_EXERCISE: '/replace_exercise',
  
  // Exports
  EXPORT_EXCEL: '/export_to_excel',
  EXPORT_TO_LOG: '/export_to_workout_log',
  
  // Superset
  SUPERSET_LINK: '/api/superset/link',
  SUPERSET_UNLINK: '/api/superset/unlink',
  SUPERSET_SUGGEST: '/api/superset/suggest',
} as const;

/**
 * Test selectors (data-testid) for stable element selection
 * Uses ID fallbacks for elements where data-testid might not be present
 */
export const SELECTORS = {
  // Navbar
  NAVBAR: '[data-testid="navbar"], #navbar',
  NAV_BRAND: '[data-testid="nav-brand"], #nav-brand',
  NAV_WORKOUT_PLAN: '[data-testid="nav-workout-plan"], #nav-workout-plan',
  NAV_WEEKLY_SUMMARY: '[data-testid="nav-weekly-summary"], #nav-weekly-summary',
  NAV_SESSION_SUMMARY: '[data-testid="nav-session-summary"], #nav-session-summary',
  NAV_WORKOUT_LOG: '[data-testid="nav-workout-log"], #nav-workout-log',
  NAV_PROGRESSION_PLAN: '[data-testid="nav-progression-plan"], #nav-progression-plan',
  NAV_BODY_COMPOSITION: '[data-testid="nav-body-composition"], #nav-body-composition',
  NAV_VOLUME_SPLITTER: '[data-testid="nav-volume-splitter"], #nav-volume-splitter',
  NAV_BACKUP: '[data-testid="nav-backup"], #nav-backup',
  NAV_USER_PROFILE: '[data-testid="nav-user-profile"], #nav-user-profile',
  DARK_MODE_TOGGLE: '[data-testid="dark-mode-toggle"], #darkModeToggle',
  
  // Toast notification
  TOAST_CONTAINER: '[data-testid="toast-container"], .toast-container',
  TOAST: '#liveToast',
  TOAST_BODY: '#toast-body',
  
  // Page identifiers
  PAGE_WELCOME: '[data-page="welcome"]',
  PAGE_WORKOUT_PLAN: '[data-page="workout-plan"]',
  PAGE_WORKOUT_LOG: '.workout-log-frame',
  PAGE_WEEKLY_SUMMARY: '#weekly-summary-container',
  PAGE_SESSION_SUMMARY: '#session-summary-container',
  PAGE_PROGRESSION: '.progression-plan-container',
  PAGE_BODY_COMPOSITION: '[data-page="body-composition"]',
  PAGE_VOLUME_SPLITTER: '#volume-splitter-app',
  PAGE_BACKUP: '[data-testid="backup-center-page"], [data-page="backup-center"]',
  PAGE_USER_PROFILE: '[data-page="user-profile"]',
  
  // Workout Plan page elements (use ID as fallback)
  ROUTINE_ENV: '[data-testid="routine-env"], #routine-env',
  ROUTINE_PROGRAM: '[data-testid="routine-program"], #routine-program',
  ROUTINE_DAY: '[data-testid="routine-day"], #routine-day',
  FILTER_FORM: '#filters-form',
  ADD_EXERCISE_BTN: '[data-testid="add-exercise-btn"], #add_exercise_btn',
  EXERCISE_SEARCH: '[data-testid="exercise-search"], #exercise',
  EXERCISE_TABLE: '[data-testid="exercise-table"], .workout-plan-table',
  EXPORT_EXCEL_BTN: '[data-testid="export-excel-btn"], .btn-export-excel',
  EXPORT_TO_LOG_BTN: '[data-testid="export-to-log-btn"], #export-to-log-btn',
  CLEAR_FILTERS_BTN: '[data-testid="clear-filters-btn"], #clear-filters-btn',
  
  // Volume Splitter
  TRAINING_DAYS: '#training-days',
  CALCULATE_VOLUME_BTN: '#calculate-volume',
  RESET_VOLUME_BTN: '#reset-volume',
  EXPORT_VOLUME_EXCEL_BTN: '#export-to-excel-btn',
  
  // Progression page
  EXERCISE_SELECT: '#exerciseSelect',
  
  // Workout Log
  IMPORT_FROM_PLAN_BTN: '#import-from-plan-btn',
  CLEAR_LOG_BTN: '#clear-log-btn',
} as const;

/**
 * Wait for page to be fully loaded and interactive
 */
export async function waitForPageReady(page: Page): Promise<void> {
  await page.waitForLoadState('domcontentloaded');
  await page.waitForLoadState('networkidle');
}

/**
 * Volume Splitter readiness without the fixed `networkidle` silence window.
 *
 * The page fires one un-awaited initial `/api/volume_history` request from its
 * DOMContentLoaded initializer. Production marks exactly that hydration on
 * `<html>`; later save/delete/activate refreshes are intentionally outside this
 * page-load lifecycle. The helper waits for document load and for the initial
 * history render (or its handled error state) to settle.
 *
 * The default Playwright timeout is preserved. Only the failure message is
 * enriched so a stranded production marker is not misdiagnosed as navigation.
 */
export async function waitForVolumeSplitterReady(page: Page): Promise<void> {
  await page.waitForLoadState('load');
  try {
    await page.waitForFunction(
      () => !document.documentElement.hasAttribute('data-volume-history-busy')
    );
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    throw new Error(
      'waitForVolumeSplitterReady: the initial volume-history readiness wait timed out. ' +
        '`data-volume-history-busy` was still present on <html>, so the initial fetch ' +
        'never settled or its marker was stranded (it is cleared in a `finally` in ' +
        'static/js/modules/volume-splitter.js). This is NOT a page-load timeout — ' +
        `the 'load' state was already reached. Original: ${detail}`
    );
  }
}

/**
 * Workout-plan readiness without `networkidle`.
 *
 * `networkidle` costs a flat ~500ms per call because it is defined as half a
 * second of silence *after* the last request, and the page's own post-load
 * fetches finish about 12ms after `load`. So almost all of it is dead time —
 * except that it also, by accident, waited out the profile-estimate fetch that
 * rewrites the six Workout Controls. Dropping `networkidle` without replacing
 * that guarantee reintroduces a real race (see docs/E2E_PERFORMANCE_PROFILE.md
 * finding 1).
 *
 * This waits for the same two things explicitly: the document has loaded, and no
 * estimate is in flight that could still overwrite the controls.
 *
 * Adopted by the five workout-plan specs whose converted paths were measured:
 * `validation-boundary`, `workout-plan`, `ui-hardening`,
 * `superset-edge-cases`, and `exercise-interactions`. Rolling a readiness
 * mechanism onto other pages requires a separate, owner-gated design.
 *
 * The marker is a boolean observable and is exact only for serialized estimates
 * — see the SCOPE note on `CONTROLS_BUSY_ATTR` in
 * `static/js/modules/workout-plan-estimates.js`.
 *
 * The wait itself is unchanged on timeout: the same condition and the same
 * tolerated duration. Only the failure message is enriched, because the bare
 * `waitForFunction` timeout names no attribute and reads as a generic page hang,
 * which sends the next reader looking at navigation instead of at the estimate.
 */
export async function waitForWorkoutPlanReady(page: Page): Promise<void> {
  await page.waitForLoadState('load');
  try {
    await page.waitForFunction(
      () => !document.documentElement.hasAttribute('data-workout-controls-busy')
    );
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    throw new Error(
      'waitForWorkoutPlanReady: the estimate-readiness wait timed out. ' +
        '`data-workout-controls-busy` was still present on <html>, so a profile-estimate ' +
        'fetch never settled or the marker was stranded (it is cleared in a `finally` in ' +
        'static/js/modules/workout-plan-estimates.js). This is NOT a page-load timeout — ' +
        `the 'load' state was already reached. Original: ${detail}`
    );
  }
}

/**
 * Reset workout-plan state between tests to avoid cross-test duplication drift.
 */
export async function resetWorkoutPlan(page: Page): Promise<void> {
  const response = await page.request.post('/clear_workout_plan', {
    failOnStatusCode: false,
  });

  expect(response.ok(), 'expected /clear_workout_plan to succeed during E2E setup').toBeTruthy();
}

/**
 * Assert toast notification appears with expected message
 */
export async function expectToast(page: Page, expectedText: string | RegExp): Promise<void> {
  const toast = page.locator(SELECTORS.TOAST);
  await expect(toast).toBeVisible({ timeout: 5000 });
  const toastBody = page.locator(SELECTORS.TOAST_BODY);
  await expect(toastBody).toContainText(expectedText);
}

/**
 * Get dark mode state from html element
 */
export async function getDarkModeState(page: Page): Promise<string | null> {
  return page.locator('html').getAttribute('data-theme');
}

/**
 * Check localStorage for dark mode preference
 */
export async function getStoredDarkMode(page: Page): Promise<string | null> {
  return page.evaluate(() => localStorage.getItem('darkMode'));
}
