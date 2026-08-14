/**
 * Strict console/page-error guard with a per-spec allowlist.
 *
 * `fixtures.ts` suppresses eleven console substrings and five page-error
 * substrings globally — including `Cannot read properties of null`,
 * `Cannot read properties of undefined`, `classList` and `is not defined`, so a
 * genuine null-dereference crash passes silently in any spec that uses it.
 * This module is the replacement: nothing is suppressed globally, and a spec
 * that legitimately provokes an error declares that exact error itself.
 *
 * Usage, per spec file:
 *
 *   import { test, expect } from './console-guard';
 *   import { ROUTES, waitForPageReady } from './fixtures';
 *
 *   test.use({
 *     consoleAllowlist: {
 *       expected: [
 *         { match: /^Failed to load resource: the server responded with a status of 500 \(INTERNAL SERVER ERROR\)$/,
 *           reason: 'error-handling.spec.ts mocks a 500 to assert the toast path' },
 *       ],
 *     },
 *   });
 *
 * `test.use()` also works inside a `describe`, which is the preferred scope: an
 * allowance should cover the block that provokes the error, not the whole file.
 *
 * The allowlist is a Playwright **option fixture**, so it is scoped to the block
 * that declares it and resolved per test. It is deliberately not module state:
 * `playwright.config.ts` runs `workers: 1` with `fullyParallel: false`, so every
 * spec in a shard shares one worker process, and a module-level array would leak
 * one spec's allowance into every other spec in the same shard.
 *
 * The entries are wrapped in an object rather than passed as a bare array
 * because Playwright normalises an array-valued option as a `[value, options]`
 * fixture tuple and hands the fixture **only its first element** — measured, at
 * both two and four entries. A bare array would therefore have silently honoured
 * one entry and dropped the rest.
 */
import {
  test as base,
  expect,
  type PlaywrightTestArgs,
  type PlaywrightTestOptions,
  type PlaywrightWorkerArgs,
  type PlaywrightWorkerOptions,
  type TestType,
} from '@playwright/test';

export interface ExpectedConsoleError {
  /**
   * The exact message text, or an anchored regex. Substring matching is not
   * supported by design — a broad pattern is how a global suppression list gets
   * rebuilt one entry at a time.
   */
  match: string | RegExp;
  /** Which module emits it and why the test provokes it. Required. */
  reason: string;
}

/**
 * Browser/tooling noise that is not the application talking. These are the same
 * three `strict-fixtures.ts` has always allowed; the list is closed.
 */
const INFRASTRUCTURE_NOISE = ['favicon', 'Source map', '[HMR]'];

function isInfrastructureNoise(text: string): boolean {
  return INFRASTRUCTURE_NOISE.some((fragment) => text.includes(fragment));
}

/**
 * An unanchored regex would match a substring, which is the catch-all this
 * module exists to prevent. Rejected at setup so it fails loudly on the first
 * run rather than silently widening later.
 */
function assertAnchored(entry: ExpectedConsoleError): void {
  if (typeof entry.match === 'string') return;
  const source = entry.match.source;
  if (!source.startsWith('^') || !source.endsWith('$')) {
    throw new Error(
      `consoleAllowlist: /${source}/ must be anchored with ^ and $ so it cannot match a ` +
        `substring. Entry reason: "${entry.reason}"`
    );
  }
}

function matches(entry: ExpectedConsoleError, text: string): boolean {
  return typeof entry.match === 'string' ? text === entry.match : entry.match.test(text);
}

/** Wrapper object — see the fixture-tuple note in the module docstring. */
export interface ConsoleAllowlist {
  expected: ExpectedConsoleError[];
}

type ConsoleGuardOptions = { consoleAllowlist: ConsoleAllowlist };

export const test = base.extend<ConsoleGuardOptions>({
  consoleAllowlist: [{ expected: [] }, { option: true }],

  page: async ({ page, consoleAllowlist }, use, testInfo) => {
    const allowed = consoleAllowlist.expected;
    allowed.forEach(assertAnchored);

    const unexpected: string[] = [];
    const record = (kind: 'Console' | 'Page', text: string) => {
      if (kind === 'Console' && isInfrastructureNoise(text)) return;
      if (allowed.some((entry) => matches(entry, text))) return;
      unexpected.push(`${kind} error: ${text}`);
    };

    page.on('console', (message) => {
      if (message.type() === 'error') record('Console', message.text());
    });
    page.on('pageerror', (error) => record('Page', error.message));

    await use(page);

    // A test that already failed has its own diagnosis; adding a console report
    // on top buries it.
    if (testInfo.status !== testInfo.expectedStatus) return;

    expect(
      unexpected,
      'unexpected browser errors. If one is genuinely expected, add an anchored ' +
        'consoleAllowlist entry naming the emitting module — do not broaden a pattern'
    ).toEqual([]);
  },
});

export { expect };

/**
 * The same guard with the allowlist option removed from its type.
 *
 * `strict-fixtures.ts` re-exports this so its importers — the visual and
 * redesign specs, whose whole value is a zero-allowance gate — cannot weaken
 * themselves with a `test.use({ consoleAllowlist })` line. The narrowing is
 * structural, not a convention.
 */
export const strictTest = test as TestType<
  PlaywrightTestArgs & PlaywrightTestOptions,
  PlaywrightWorkerArgs & PlaywrightWorkerOptions
>;
