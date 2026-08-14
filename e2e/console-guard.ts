/**
 * Strict console/page-error guard with a per-block allowlist.
 *
 * `fixtures.ts` suppresses broad substrings in both channels - including
 * `Cannot read properties of null`, `Cannot read properties of undefined`,
 * `classList` and `is not defined` - so a genuine null-dereference crash passes
 * silently in any spec that uses it. This module is the replacement: nothing is
 * suppressed globally, and a block that legitimately provokes an error declares
 * that exact error itself. The worked example is `workout-plan.spec.ts`, whose
 * one allowlist is scoped to the single describe that mocks a 400.
 *
 * Three things here are non-obvious:
 *
 * 1. Declare the allowlist on the narrowest `test.describe` that provokes the
 *    error, not the file. Playwright *replaces* option values rather than
 *    merging them, so a nested `test.use({ consoleAllowlist })` silently
 *    discards the outer block entries.
 * 2. It is a Playwright **option fixture**, deliberately not module state:
 *    `playwright.config.ts` runs `workers: 1` with `fullyParallel: false`, so
 *    every spec in a shard shares one worker process and a module-level array
 *    would leak one spec allowance into every other spec in the shard.
 * 3. The entries are wrapped in an object rather than passed as a bare array
 *    because Playwright normalises an array-valued option as a `[value, options]`
 *    fixture tuple and hands the fixture **only its first element** - measured,
 *    at both two and four entries. A bare array would have silently honoured one
 *    entry and dropped the rest.
 *
 * Entries are matched against `console` message text and against a page error
 * `message` - not its stack, which is reported but not matched.
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
  /** The exact message text, or a regex anchored with `^` and `$`. */
  match: string | RegExp;
  /** Which module emits it and why the block provokes it. */
  reason: string;
}

/**
 * Browser/tooling noise that is not the application talking. Matched as
 * substrings - the one place that is allowed here, because the list is closed
 * and cannot be extended by a spec. Allowlist entries get no such latitude.
 */
const INFRASTRUCTURE_NOISE = ['favicon', 'Source map', '[HMR]'];

/**
 * Reject the three shapes that turn an allowlist entry back into a catch-all:
 * an unanchored pattern, the `m` flag (which re-anchors per line, so a pattern
 * can still match a substring of multi-line console text), and an unbounded
 * wildcard. Rejected at setup so it fails on the first run rather than widening
 * quietly.
 */
function assertNarrow(entry: ExpectedConsoleError): void {
  if (typeof entry.match === 'string') return;
  const { source, flags } = entry.match;
  const reject = (why: string) => {
    throw new Error(
      `consoleAllowlist: /${source}/${flags} ${why}. Entry reason: "${entry.reason}"`
    );
  };

  if (!source.startsWith('^') || !source.endsWith('$')) {
    reject('must be anchored with ^ and $ so it cannot match a substring');
  }
  if (flags.includes('m')) {
    reject('must not use the m flag, which re-anchors per line');
  }
  // Strip escaped pairs first, so a literal escaped dot is not read as the
  // wildcard it is escaping.
  if (/\.[*+]/.test(source.replace(/\\./g, ''))) {
    reject('must not contain an unbounded wildcard, which matches anything');
  }
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
    allowed.forEach(assertNarrow);

    const unexpected: string[] = [];
    // `matched` is what the allowlist is tested against; `reported` is what a
    // failure prints. They differ for page errors, where the stack is the useful
    // diagnostic but the message is the stable thing to match on.
    const record = (kind: 'Console' | 'Page', matched: string, reported = matched) => {
      const allowlisted = allowed.some((entry) =>
        typeof entry.match === 'string' ? matched === entry.match : entry.match.test(matched)
      );
      if (allowlisted) return;
      unexpected.push(`${kind} error: ${reported}`);
    };

    page.on('console', (message) => {
      if (message.type() !== 'error') return;
      const text = message.text();
      if (INFRASTRUCTURE_NOISE.some((fragment) => text.includes(fragment))) return;
      record('Console', text);
    });
    page.on('pageerror', (error) => record('Page', error.message, error.stack || error.message));

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
 * The same guard with the allowlist option removed from its type, re-exported by
 * `strict-fixtures.ts` for the visual and redesign specs whose whole value is a
 * zero-allowance gate.
 *
 * The narrowing stops the obvious slip: passing a fresh object literal to
 * `test.use` is a compile error under the blocking `tsc` gate. It does **not**
 * stop a spec from importing this module directly, so the binding contract is
 * `tests/test_console_guard_contracts.py`, which runs in the required pytest
 * gate.
 */
export const strictTest = test as TestType<
  PlaywrightTestArgs & PlaywrightTestOptions,
  PlaywrightWorkerArgs & PlaywrightWorkerOptions
>;
