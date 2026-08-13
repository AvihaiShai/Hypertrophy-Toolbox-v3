/**
 * E2E Test: Body Composition (Issue #21)
 *
 * Smoke + save-flow coverage for the standalone /body_composition page.
 */
import type { Page } from '@playwright/test';
import { test, expect, waitForBodyCompositionReady, waitForPageReady } from './fixtures';
import parityCases from './fixtures/body-fat-parity.json';

const ROUTE = '/body_composition';

async function seedProfile(page: Page) {
  const res = await page.request.post('/api/user_profile', {
    data: {
      gender: 'M',
      age: 34,
      height_cm: 180,
      weight_kg: 80,
      experience_years: 5,
    },
  });
  expect(res.ok(), 'profile seed must succeed').toBeTruthy();
}

async function clearSnapshots(page: Page) {
  const listResp = await page.request.get('/api/body_composition/snapshots');
  if (!listResp.ok()) return;
  const payload = await listResp.json();
  const items = payload?.data ?? [];
  for (const snap of items) {
    await page.request.delete(`/api/body_composition/snapshots/${snap.id}`);
  }
}

test.describe('Body Composition page', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await seedProfile(page);
    await clearSnapshots(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('navbar link routes to /body_composition', async ({ page }) => {
    await page.goto('/');
    await waitForPageReady(page);
    const navLink = page.locator('#nav-body-composition');
    await expect(navLink).toBeVisible();
    await navLink.click();
    // Wait for the navigation to commit first. `waitForLoadState('load')` is
    // defined against the *currently committed* document, so on an in-flight
    // navigation it resolves instantly against `/` — and the readiness
    // predicate then evaluates on `/`, where the attribute never exists. That
    // would be a strict weakening at this one site: an uncommitted navigation
    // kept the frame busy, so `networkidle` did wait here.
    await page.waitForURL(/\/body_composition/);
    await waitForBodyCompositionReady(page);
    await expect(page).toHaveURL(/\/body_composition/);
    await expect(page.locator('[data-page="body-composition"]')).toBeVisible();
  });

  test('renders form + empty trend with no snapshots', async ({ page }) => {
    await page.goto(ROUTE);
    await waitForBodyCompositionReady(page);
    await expect(page.locator('#bc-form')).toBeVisible();
    await expect(page.locator('[data-bc-trend-empty]')).toBeVisible();
    await expect(page.locator('[data-bc-empty]')).toBeVisible();
    // ACE band segments are rendered client-side once the JS module boots.
    await expect(page.locator('.bc-band-segment').first()).toBeVisible();
  });

  test('save snapshot adds row to history and updates trend', async ({ page }) => {
    await page.goto(ROUTE);
    await waitForBodyCompositionReady(page);

    await page.locator('#bc-neck').fill('38');
    await page.locator('#bc-waist').fill('85');

    // Live results should update before save.
    await expect(page.locator('[data-bc-bfp]')).not.toHaveText('—', { timeout: 5000 });
    await expect(page.locator('[data-bc-method-label]')).toHaveText('U.S. Navy method');

    await page.locator('#bc-save').click();

    const rows = page.locator('[data-bc-history-body] tr');
    await expect(rows).toHaveCount(1, { timeout: 5000 });
    await expect(page.locator('[data-bc-empty]')).toBeHidden();
    await expect(page.locator('[data-bc-trend-empty]')).toBeHidden();

    const polyline = page.locator('[data-bc-trend-line]');
    await expect(polyline).toHaveAttribute('points', /\d/);

    // Delete the row and confirm the empty state returns.
    await rows.first().locator('[data-bc-delete]').click();
    await expect(page.locator('[data-bc-history-body] tr')).toHaveCount(0, { timeout: 5000 });
    await expect(page.locator('[data-bc-empty]')).toBeVisible();
  });

  test('BMI fallback shows when tape fields are blank', async ({ page }) => {
    await page.goto(ROUTE);
    await waitForBodyCompositionReady(page);
    await expect(page.locator('[data-bc-method-label]')).toHaveText('BMI method (fallback)');
    await expect(page.locator('[data-bc-bfp]')).not.toHaveText('—');
  });

  test('JS preview matches Python persisted Navy BFP within rounding', async ({ page }) => {
    await page.goto(ROUTE);
    await waitForBodyCompositionReady(page);

    await page.locator('#bc-neck').fill('38');
    await page.locator('#bc-waist').fill('85');

    const previewText = await page.locator('[data-bc-bfp]').textContent();
    const previewMatch = previewText?.match(/([\d.]+)\s*%/);
    expect(previewMatch, `expected BFP preview text, got "${previewText}"`).not.toBeNull();
    const previewValue = Number(previewMatch![1]);

    await page.locator('#bc-save').click();
    await expect(page.locator('[data-bc-history-body] tr')).toHaveCount(1, { timeout: 5000 });

    const listResp = await page.request.get('/api/body_composition/snapshots');
    expect(listResp.ok()).toBeTruthy();
    const payload = await listResp.json();
    const snap = payload?.data?.[0];
    expect(snap, 'snapshot list should not be empty').toBeTruthy();
    expect(snap.bfp_navy, 'Navy BFP should be persisted').not.toBeNull();

    // JS displays bfp.toFixed(1); server stores the raw float. They must
    // round-trip to within ±0.05 % BFP — anything larger means the JS and
    // Python formulas have drifted.
    expect(Math.abs(previewValue - Number(snap.bfp_navy.toFixed(1)))).toBeLessThanOrEqual(0.05);
  });

  for (const parityCase of parityCases) {
    test(`shared JS/Python parity: ${parityCase.id}`, async ({ page }) => {
      const profileResp = await page.request.post('/api/user_profile', {
        data: {
          gender: parityCase.profile.gender,
          age: parityCase.profile.age,
          height_cm: parityCase.profile.height_cm,
          weight_kg: parityCase.profile.weight_kg,
          experience_years: 5,
        },
      });
      expect(profileResp.ok(), 'parity profile seed must succeed').toBeTruthy();

      await page.goto(ROUTE);
      await waitForBodyCompositionReady(page);
      if (parityCase.tape) {
        await page.locator('#bc-neck').fill(String(parityCase.tape.neck_cm));
        await page.locator('#bc-waist').fill(String(parityCase.tape.waist_cm));
        if ('hip_cm' in parityCase.tape) {
          await page.locator('#bc-hip').fill(String(parityCase.tape.hip_cm));
        }
      }

      await expect(page.locator('[data-bc-method-label]')).toHaveText(parityCase.expected.method);
      await expect(page.locator('[data-bc-bfp]')).toHaveText(`${parityCase.expected.bfp.toFixed(1)} %`);
      await expect(page.locator('[data-bc-bmi]')).toHaveText(parityCase.expected.bmi.toFixed(1));
      await expect(page.locator('[data-bc-band-label]')).toHaveText(parityCase.expected.ace);
      await expect(page.locator('[data-bc-jp-ideal]')).toHaveText(
        `${parityCase.expected.jackson_pollock_ideal.toFixed(1)} %`,
      );
    });
  }
});

test.describe('Body Composition initial readiness', () => {
  test('exposes the initial snapshot fetch until it has rendered', async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();

    // Seed a profile and one snapshot, so the render this test waits for has
    // something to draw. With an empty history `renderTrend()` leaves the
    // server-rendered empty state as it found it, and the post-release
    // assertion could not tell a completed render from no render at all.
    const profileResp = await page.request.post('/api/user_profile', {
      data: { gender: 'M', age: 30, height_cm: 180, weight_kg: 80, experience_years: 5 },
    });
    expect(profileResp.ok(), 'profile seed must succeed').toBeTruthy();
    const snapResp = await page.request.post('/api/body_composition/snapshot', {
      data: { neck_cm: 38, waist_cm: 85, hip_cm: null, notes: null },
    });
    expect(snapResp.ok(), 'snapshot seed must succeed').toBeTruthy();

    let markRequestStarted!: () => void;
    const requestStarted = new Promise<void>((resolve) => {
      markRequestStarted = resolve;
    });
    let releaseSnapshots!: () => void;
    const snapshotsRelease = new Promise<void>((resolve) => {
      releaseSnapshots = resolve;
    });

    await page.route('**/api/body_composition/snapshots', async (route) => {
      markRequestStarted();
      await snapshotsRelease;
      await route.continue();
    });

    await page.goto(ROUTE);
    await requestStarted;

    // The marker is present while the fetch is genuinely in flight...
    const root = page.locator('html');
    await expect(root).toHaveAttribute('data-body-composition-history-busy', '1');

    // ...and the helper does not settle while it is. This is the assertion that
    // makes the helper a real wait rather than a no-op: without the marker it
    // would resolve here, on a page whose history has not arrived.
    //
    // Deliberately NOT `expect.poll(() => readySettled).toBe(false)`. `poll`
    // succeeds on its first satisfying observation, so it passes the instant it
    // sees `false` — which is also what it sees when the helper is about to
    // resolve a microtask later. It cannot distinguish "blocked" from "not
    // settled yet", and a no-op helper survives it. Yielding across two full
    // CDP round trips gives a no-op every chance to resolve, then the state is
    // read once, synchronously. No hard wait is involved.
    let readySettled = false;
    const ready = waitForBodyCompositionReady(page).then(() => {
      readySettled = true;
    });
    await page.evaluate(() => new Promise(requestAnimationFrame));
    await page.evaluate(() => new Promise(requestAnimationFrame));
    expect(
      readySettled,
      'the helper resolved while the snapshot fetch was still blocked',
    ).toBe(false);

    releaseSnapshots();
    await ready;

    // Non-retrying reads FIRST. An auto-retrying matcher here would absorb up
    // to its timeout of "the render finished shortly after the helper
    // returned", which is precisely the failure being tested — a marker cleared
    // before renderTrend() ran would still go green.
    const busyAfter = await page.locator('html').getAttribute('data-body-composition-history-busy');
    const points = await page.locator('[data-bc-trend-line]').getAttribute('points');
    expect(busyAfter, 'the marker must be removed, not set to another value').toBeNull();
    expect(points ?? '', 'the trend line must be drawn by the initial render').toMatch(/\d/);

    // Retrying assertions afterwards, where absorbing a late update is harmless.
    await expect(page.locator('[data-bc-trend-empty]')).toBeHidden();
    consoleErrors.assertNoErrors();
  });
});
