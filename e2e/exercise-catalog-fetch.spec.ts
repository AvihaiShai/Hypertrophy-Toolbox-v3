/**
 * E2E Regression: the exercise catalog is fetched once per /workout_plan load.
 *
 * `/workout_plan` initialization ends with the routine cascade's stateless
 * reset, which writes the empty composite value into the hidden `#routine`
 * field and dispatches a `change` on it (routine-cascade.js
 * `updateCompositeRoutineValue()`). The `#routine` change handler installed by
 * `handleRoutineSelection()` treats an empty routine as "reapply filters, or
 * show everything", so with no filters selected it calls `filterExercises()`,
 * which GETs the whole catalog from `/get_all_exercises`.
 *
 * That is one intended request. It was two, because `handleRoutineSelection()`
 * ran twice during init — once directly from `initializeWorkoutPlan()` in
 * app.js and once from `initializeWorkoutPlanHandlers()`, which app.js calls on
 * the very next line. Two distinct closures meant two live `change` listeners,
 * so the single reset dispatch fanned out into two identical catalog fetches on
 * every navigation. (app.js already carried the same de-duplication note for
 * `fetchWorkoutPlan`; the routine handler was missed.)
 *
 * The reset runs on `pageshow`, which fires after `load`, so the readiness
 * marker used by the other workout-plan specs settles too early to bound this
 * count. `networkidle` is the right wait here for the opposite reason it was
 * removed elsewhere: this test needs the guarantee that nothing is still in
 * flight, which is exactly what half a second of network silence buys.
 */
import { test, expect, ROUTES } from './fixtures';

const CATALOG_PATH = '/get_all_exercises';

/** Record every catalog request issued for the lifetime of the page. */
function trackCatalogRequests(page: import('@playwright/test').Page): string[] {
  const seen: string[] = [];
  page.on('request', (request) => {
    if (new URL(request.url()).pathname === CATALOG_PATH) {
      seen.push(request.url());
    }
  });
  return seen;
}

test.describe('Exercise catalog fetch (single-fetch contract)', () => {
  test('workout plan initialization issues exactly one /get_all_exercises request', async ({
    page,
    consoleErrors,
  }) => {
    consoleErrors.startCollecting();
    const catalogRequests = trackCatalogRequests(page);

    await page.goto(ROUTES.WORKOUT_PLAN);
    await page.waitForLoadState('networkidle');

    // The dropdown must actually be populated from the catalog — a count of 1
    // is only meaningful if the surviving request is the one that fills it.
    await expect
      .poll(() => page.locator('#exercise option').count())
      .toBeGreaterThan(1);

    expect(
      catalogRequests,
      `expected a single ${CATALOG_PATH} request during page initialization, got ` +
        `${catalogRequests.length}. More than one means the #routine change listener ` +
        'is registered more than once (handleRoutineSelection called from both ' +
        'initializeWorkoutPlan and initializeWorkoutPlanHandlers).',
    ).toHaveLength(1);

    consoleErrors.assertNoErrors();
  });

  test('the hidden #routine field carries exactly one change listener after init', async ({
    page,
    consoleErrors,
  }) => {
    consoleErrors.startCollecting();

    // Count `change` registrations against #routine specifically. Registration
    // happens during DOMContentLoaded, so the accounting has to be installed
    // before any page script runs.
    await page.addInitScript(() => {
      const registered: unknown[] = [];
      (window as unknown as { __routineChangeListeners: unknown[] }).__routineChangeListeners =
        registered;
      const origAdd = EventTarget.prototype.addEventListener;
      EventTarget.prototype.addEventListener = function (
        type: string,
        listener: EventListenerOrEventListenerObject | null,
        options?: boolean | AddEventListenerOptions,
      ) {
        if (
          type === 'change' &&
          listener &&
          this instanceof Element &&
          (this as Element).id === 'routine' &&
          !registered.includes(listener)
        ) {
          registered.push(listener);
        }
        return origAdd.call(this, type, listener, options);
      };
    });

    await page.goto(ROUTES.WORKOUT_PLAN);
    await page.waitForLoadState('networkidle');

    const listenerCount = await page.evaluate(
      () => (window as unknown as { __routineChangeListeners: unknown[] }).__routineChangeListeners.length,
    );

    expect(
      listenerCount,
      'a duplicate #routine change listener fans the cascade reset out into ' +
        'duplicate catalog fetches on every navigation',
    ).toBe(1);

    consoleErrors.assertNoErrors();
  });
});
