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
 * The shared guard, with the `consoleAllowlist` option removed from its type.
 *
 * The behaviour these specs had is unchanged: every console error and every
 * page error fails the test, except the same three infrastructure fragments
 * (`favicon`, `Source map`, `[HMR]`). The narrowed type is what keeps it that
 * way — a `test.use({ consoleAllowlist: [...] })` line in any importer of this
 * module is a compile error, so the zero-allowance gate cannot be relaxed
 * locally.
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
