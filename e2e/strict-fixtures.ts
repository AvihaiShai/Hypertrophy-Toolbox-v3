/**
 * Strict fixtures for redesign gates.
 *
 * The legacy fixture intentionally ignores broad null/undefined JavaScript
 * errors for older E2E coverage. Redesign specs should fail on those errors so
 * broken selectors cannot hide behind screenshot diffs.
 */
import { expect } from '@playwright/test';

import { strictTest } from './console-guard';
import {
  API_ENDPOINTS,
  ROUTES,
  SELECTORS,
  expectToast,
  getDarkModeState,
  getStoredDarkMode,
  resetWorkoutPlan,
  waitForPageReady,
} from './fixtures';

/**
 * The shared guard from `console-guard.ts`, with the `consoleAllowlist` option
 * removed from its type so these specs keep a zero-allowance gate. See that
 * module for the mechanism; `tests/test_console_guard_contracts.py` binds it.
 *
 * Pass/fail is unchanged from the fixture this replaced. Two details did change:
 * a page error now reports `error.stack || error.message` through a shared code
 * path, and the console assertion is skipped when the test has already failed
 * for another reason, so a real failure is not buried under an error report.
 */
export const test = strictTest;

export {
  API_ENDPOINTS,
  ROUTES,
  SELECTORS,
  expect,
  expectToast,
  getDarkModeState,
  getStoredDarkMode,
  resetWorkoutPlan,
  waitForPageReady,
};
