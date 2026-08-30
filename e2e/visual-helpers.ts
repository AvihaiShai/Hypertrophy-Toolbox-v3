import { expect } from '@playwright/test';
import type { Locator, Page } from '@playwright/test';

export type VisualTheme = 'light' | 'dark';

/**
 * Chromium cannot allocate a capture surface taller than this. A `fullPage`
 * screenshot past it does not fail — it silently truncates to a flat,
 * unpainted tail, freezing "never rendered" into a committed baseline.
 * `tests/test_visual_capture_contracts.py` pins the same number.
 */
export const MAX_CAPTURE_HEIGHT_PX = 16_384;

/**
 * Height of each band when a page has to be captured in segments. Comfortably
 * under the limit, and *fixed* rather than an even split of the page height:
 * with a fixed band, a page that grows only changes its last segment instead of
 * shifting every boundary and re-diffing the whole page.
 */
export const CAPTURE_SEGMENT_HEIGHT_PX = 10_000;

/** Bound on the media wait. Long enough for a cold cache, short enough to fail. */
export const IMAGE_SETTLE_TIMEOUT_MS = 15_000;

/**
 * Captures that are deliberately not byte-compared, by baseline stem.
 *
 * Chromium rasters these five nondeterministically on the ubuntu-24.04 runner.
 * In the eight independent experiment sets that selected the exemptions (21
 * generations at six capture configurations), each flipped between two states
 * at *byte-identical layout*. A geometry probe compared document size,
 * viewport, the captured table's rect, its first eight row rects and its whole
 * ancestor chain to five decimal places across two runs; all 84 records matched
 * while the PNGs did not. Six documented capture controls were tried; none
 * closed it. In that bounded sample, these five were the only captures observed
 * above the 800px tolerance. `log-desktop-light` and
 * `workout-plan-mobile-light` flipped by 178px and 13px, so they stayed gated.
 *
 * Later evidence disproved the broader "only captures" inference. Scheduled
 * deep-gate run 32688747703 first failed the non-exempt, still-byte-gated
 * `plan-desktop-light-simple` by 11,392px, then passed it on retry #1 and ended
 * `1 flaky` plus `99 passed`. That is a flaky-success, not a clean comparison:
 * clean means no failed attempt, retry or flaky tally; terminal failure means
 * the comparison stays red after the retry policy and the job fails. Because
 * this run finished green, its failure-only report-and-diff upload was skipped.
 * ADR-011 keeps `plan-desktop-light-simple` byte-gated and keeps this exemption
 * set at exactly five; the later observation does not broaden it.
 *
 * Their coverage moved to `e2e/workout-plan-desktop-contract.spec.ts`, which
 * asserts the same properties through computed style, geometry and DOM
 * structure. `docs/visual_determinism/PLANNING.md` §8.10 maps each file to its
 * replacement; `tests/test_visual_capture_contracts.py` pins this set so it
 * cannot grow silently.
 *
 * This is an exemption from *byte comparison only*. The tests still run, still
 * render at 1440x900, and still fail on a console error.
 */
export const BYTE_GATE_EXEMPT = new Set([
  'workout-plan-desktop-light',
  'workout-plan-desktop-dark',
  'plan-desktop-light-advanced',
  'plan-desktop-dark-advanced',
  'plan-desktop-dark-simple',
]);

export function isByteGateExempt(name: string): boolean {
  return BYTE_GATE_EXEMPT.has(name.replace(/\.png$/i, ''));
}

/**
 * Stand-in assertion for a capture that is exempt from byte comparison.
 *
 * Deliberately not a no-op and deliberately not a `skip`: the page is still
 * built, still rendered at its real viewport, and the console-error fixture
 * still applies. What it drops is the pixel diff, and only that.
 */
export async function expectRenderedWithoutByteComparison(
  page: Page,
  name: string,
): Promise<void> {
  const geometry = await page.evaluate(() => ({
    width: document.documentElement.scrollWidth,
    height: document.documentElement.scrollHeight,
    painted: document.querySelectorAll('[data-visual-surface]').length,
  }));
  expect(geometry.width, `${name}: page has no width`).toBeGreaterThan(0);
  expect(geometry.height, `${name}: page has no height`).toBeGreaterThan(0);
  expect(
    geometry.painted,
    `${name}: no visual surface rendered, so the exempt capture covered nothing`,
  ).toBeGreaterThan(0);
}

export interface VisualDeterminismOptions {
  theme: VisualTheme;
}

export async function installDeterminism(
  page: Page,
  options: VisualDeterminismOptions,
): Promise<void> {
  await page.addInitScript((theme) => {
    const FIXED = new Date('2026-04-18T09:00:00Z').valueOf();
    const NativeDate = Date;

    // Keep no-argument Date construction and Date.now() stable for screenshots.
    // @ts-ignore - this class intentionally shadows the browser Date constructor.
    globalThis.Date = class extends NativeDate {
      constructor(...args: any[]) {
        // Cast to a tuple so the spread satisfies tsc (TS2556); the Date copy
        // shim forwards all original args unchanged at runtime.
        super(...((args.length ? args : [FIXED]) as [number]));
      }

      static now() {
        return FIXED;
      }
    };

    localStorage.clear();
    localStorage.setItem('darkMode', theme === 'dark' ? 'true' : 'false');
    document.documentElement?.setAttribute('data-theme', theme);
  }, options.theme);
}

export async function prepareForScreenshot(page: Page): Promise<void> {
  await page.waitForLoadState('domcontentloaded');
  await page.waitForLoadState('networkidle');

  await page.addStyleTag({
    content: `
      *, *::before, *::after {
        animation-delay: 0s !important;
        animation-duration: 0s !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0s !important;
        transition-delay: 0s !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
      }

      html { scroll-behavior: auto !important; }
      html {
        --visual-surface-0: #eef1f6;
        --visual-surface-1: #f7f9fc;
      }
      html[data-theme='dark'] {
        --visual-surface-0: #090c16;
        --visual-surface-1: #0d101d;
      }
      html[data-theme] body,
      body {
        background: var(--visual-surface-0) !important;
        background-attachment: scroll !important;
      }

      /* This flattener computes to (0,3,1) and is entirely !important, so it owns
         a surface only where no product rule out-specifies it. On the Progression
         goals table the shared components.css Calm Glass family does - but only
         because that family's :is() list borrows ID-level weight from its #workout
         branch. A packet that splits a non-ID branch out of that list drops the arm
         to (0,3,0), below this rule, and the flattener would silently take over
         border-color and border-radius there: two committed dark baselines move for
         a product change that alters no rendered value.

         Only those two properties are at issue, so the rule is split by property
         rather than by element. background and box-shadow are re-declared by the
         family's dark rule at (0,4,0), which still wins after a split; text-shadow
         is NOT declared by the family at all, so this layer legitimately owns it -
         and text-shadow inherits, so an element-wholesale exclusion would hand it
         away and change every descendant. The flattening set below is unchanged and
         still matches every surface. */
      html[data-theme='dark'] [data-visual-surface][data-visual-surface] {
        background: var(--visual-surface-1) !important;
        background-image: none !important;
        box-shadow: none !important;
        text-shadow: none !important;
      }
      /* Summary filters use a translucent rounded surface whose fractional top
         edge can round one channel differently across fresh Skia processes.
         Flatten only the visual capture layer; labels and controls stay intact. */
      html[data-theme='dark'] .summary-header {
        background: var(--visual-surface-1) !important;
        border-radius: 0 !important;
        box-shadow: none !important;
      }
      /* Border geometry only, withheld from surfaces whose borders the product
         owns. Keyed on the inert [data-visual-preserve-border] hook rather than a
         class, because presentation classes are exactly what a CSS refactor churns
         (tests/test_visual_selector_contracts.py). :where(:not(...)) contributes
         zero specificity, so this stays (0,3,1) for every surface it still matches
         and the match-set delta is one element per dark Progression viewport. */
      html[data-theme='dark'] [data-visual-surface][data-visual-surface]:where(:not([data-visual-preserve-border])) {
        border-color: #273145 !important;
        border-radius: 0 !important;
      }
      html[data-theme='dark'] [data-page="workout-plan"] [data-visual-header]::before {
        background: transparent !important;
      }
      html[data-theme='dark'] [data-page="workout-plan"] [data-visual-accent] {
        background: #4f8cff !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        transform: none !important;
        transition: none !important;
      }

      input, textarea { caret-color: transparent !important; }
      select {
        appearance: none !important;
        -webkit-appearance: none !important;
        background-image: none !important;
      }
      [data-visual-control],
      input,
      textarea,
      select,
      input[type="number"] {
        border-radius: 0 !important;
        box-shadow: none !important;
        text-shadow: none !important;
      }
      [data-testid="navbar"] a::before,
      [data-testid="navbar"] button::before {
        background-color: transparent !important;
        border-radius: 0 !important;
        transform: none !important;
        transition: none !important;
      }
      [data-visual-dropdown-toggle]::after {
        border-color: transparent !important;
      }
      [data-visual-icon] {
        visibility: hidden !important;
      }
      [data-visual-scale-control] {
        background: transparent !important;
        border-color: transparent !important;
        color: transparent !important;
      }
      /* Sticky table cells are promoted into compositor-managed layers. That is
         useful while a person scrolls, but a baseline capture is always made at
         the origin and gains nothing from the separate raster path. Keep every
         table capture on the same static paint path, including full-page shots. */
      [data-testid="exercise-table"] thead th,
      [data-testid="exercise-table"] tr > :first-child,
      [data-testid="workout-log-table"] thead th,
      [data-testid="workout-log-table"] tr > :first-child {
        position: static !important;
      }
      input[type="number"]::-webkit-outer-spin-button,
      input[type="number"]::-webkit-inner-spin-button {
        -webkit-appearance: none !important;
        margin: 0 !important;
      }
      ::-webkit-scrollbar { display: none; }
    `,
  });

  await page.evaluate(async () => {
    document
      .querySelectorAll<HTMLElement>(
        '[data-visual-control], input, textarea, select',
      )
      .forEach((element) => {
        element.style.setProperty('border-radius', '0', 'important');
        element.style.setProperty('box-shadow', 'none', 'important');
        element.style.setProperty('text-shadow', 'none', 'important');
      });

    await document.fonts.ready;
    window.scrollTo(0, 0);
  });

  await waitForImagesSettled(page);
}

/**
 * Report every image on the page that is not decodable pixels yet.
 *
 * `complete && naturalWidth > 0` is the only combination that means "the bytes
 * arrived and they decoded". `complete` alone is true for a 404 too, and the
 * `src` attribute — which the thumbnail spec used to assert — is true the
 * instant the markup exists, long before anything is fetched.
 */
export async function collectUnloadedImages(
  page: Page,
  selector = 'img',
): Promise<string[]> {
  return page.$$eval(selector, (elements) =>
    (elements as HTMLImageElement[])
      .filter((image) => !(image.complete && image.naturalWidth > 0))
      .map((image) => image.currentSrc || image.src || '(no src)'),
  );
}

/**
 * Block until every image is loaded and decoded, or fail loudly.
 *
 * `networkidle` is not sufficient and cannot be made sufficient: it fires
 * *before* a below-fold `loading="lazy"` image is ever requested, because the
 * request only starts when the viewport approaches it. `toHaveScreenshot`
 * with `fullPage` then scrolls the page and races the raster it just triggered,
 * which is how a thumbnail could be present in one run and blank in the next at
 * the same commit. Measured on the committed fixture at 375x812 immediately
 * after the previous body of `prepareForScreenshot`: 6 of 6 plan thumbnails,
 * 3 of 6 log thumbnails and 61 of 71 profile images were still unloaded.
 *
 * Forcing `loading="eager"` is a capture-time override applied to the live DOM,
 * not a markup change: `loading="lazy"` is a real production benefit and stays.
 * Without the override the wait below would simply deadlock on images the
 * browser has decided not to fetch yet.
 */
export async function waitForImagesSettled(
  page: Page,
  timeoutMs = IMAGE_SETTLE_TIMEOUT_MS,
): Promise<void> {
  await page.evaluate(() => {
    for (const image of Array.from(document.images)) {
      // Assigning 'eager' to an image whose lazy load has not started begins it
      // immediately; on an already-loaded image it is a no-op.
      image.loading = 'eager';
      image.decoding = 'sync';
    }
  });

  try {
    await page.waitForFunction(
      () =>
        Array.from(document.images).every(
          (image) => image.complete && image.naturalWidth > 0,
        ),
      undefined,
      { timeout: timeoutMs },
    );
  } catch {
    const pending = await collectUnloadedImages(page);
    throw new Error(
      `Images were still unloaded ${timeoutMs}ms into the capture wait, so the ` +
        'screenshot would have raced their raster. Fix the page or the fixture; ' +
        'do not shorten the wait. ' +
        `Pending (${pending.length}): ${pending.slice(0, 10).join(', ')}` +
        (pending.length > 10 ? ` ...+${pending.length - 10} more` : ''),
    );
  }

  // `complete` only promises the bytes arrived; `decoding="async"` defers the
  // raster to some later frame. decode() resolves once it is ready to paint.
  await page.evaluate(async () => {
    await Promise.all(
      Array.from(document.images).map((image) =>
        image.decode().catch(() => undefined),
      ),
    );
    await new Promise<void>((resolveFrame) => {
      requestAnimationFrame(() => requestAnimationFrame(() => resolveFrame()));
    });
    window.scrollTo(0, 0);
  });
}

/**
 * Prepare an oversized locator capture without fixed page chrome contaminating
 * the table image when Playwright scrolls the locator into view.
 */
export async function prepareForElementScreenshot(page: Page): Promise<void> {
  await prepareForScreenshot(page);
  await page.addStyleTag({
    content: `
      /* Fixed page chrome and closed offscreen overlays are not table content. */
      #navbar { visibility: hidden !important; }
      .vp-drawer[aria-hidden="true"],
      .vp-backdrop[hidden] { display: none !important; }
    `,
  });

  // The element-only style above invalidates paint after the common readiness
  // wait. Do not let locator auto-scrolling race that new frame.
  await page.evaluate(async () => {
    window.scrollTo(0, 0);
    await new Promise<void>((resolveFrame) => {
      requestAnimationFrame(() => requestAnimationFrame(() => resolveFrame()));
    });
    window.scrollTo(0, 0);
  });
}

export function visualScreenshotOptions(page: Page): {
  animations: 'disabled';
  caret: 'hide';
  fullPage: true;
  mask: Locator[];
  maxDiffPixels: number;
  threshold: 0;
} {
  return {
    fullPage: true,
    animations: 'disabled',
    caret: 'hide',
    mask: [
      page.locator('#auto-backup-banner'),
      page.locator('.timestamp, [data-volatile]'),
      page.locator('.toast-container'),
      page.locator('img[src$=".gif"]'),
    ],
    maxDiffPixels: 800,
    threshold: 0,
  };
}

/**
 * Full-page baseline capture that can never exceed Chromium's capture surface.
 *
 * Pages at or under the limit keep their existing single baseline and their
 * existing name, so this is a no-op for 64 of the 66 `visual.spec.ts` baselines
 * per platform — only `user-profile-mobile-{dark,light}` is taller. A page over
 * the limit is captured as consecutive document-relative bands named
 * `<base>-segment-<n>.png`.
 *
 * The `assertCaptureFits` call is the contract, not an implementation detail:
 * on the unsegmented path it is what turns "silently truncated to a blank tail"
 * into a failing test.
 */
export async function expectFullPageScreenshot(
  page: Page,
  name: string,
  options: ReturnType<typeof visualScreenshotOptions>,
): Promise<void> {
  const { documentHeight, documentWidth } = await page.evaluate(() => ({
    documentHeight: Math.ceil(document.documentElement.scrollHeight),
    documentWidth: Math.ceil(document.documentElement.clientWidth),
  }));

  if (isByteGateExempt(name)) {
    await expectRenderedWithoutByteComparison(page, name);
    return;
  }

  if (documentHeight <= MAX_CAPTURE_HEIGHT_PX) {
    assertCaptureFits(name, documentHeight);
    await expect(page).toHaveScreenshot(name, options);
    return;
  }

  const base = name.replace(/\.png$/i, '');
  const segments = Math.ceil(documentHeight / CAPTURE_SEGMENT_HEIGHT_PX);

  for (let index = 0; index < segments; index += 1) {
    const y = index * CAPTURE_SEGMENT_HEIGHT_PX;
    const height = Math.min(CAPTURE_SEGMENT_HEIGHT_PX, documentHeight - y);
    const segmentName = `${base}-segment-${index + 1}.png`;

    assertCaptureFits(segmentName, height);
    await expect(page).toHaveScreenshot(segmentName, {
      ...options,
      // With `fullPage`, `clip` is document-relative, so this is the band at
      // document y..y+height — including bands past the surface limit, which a
      // single full-page capture returns unpainted.
      clip: { x: 0, y, width: documentWidth, height },
    });
  }
}

function assertCaptureFits(label: string, height: number): void {
  expect(
    height,
    `${label}: a capture ${height}px tall exceeds Chromium's ` +
      `${MAX_CAPTURE_HEIGHT_PX}px surface limit. Chromium does not error on ` +
      'this — it returns a flat, unpainted tail, so the excess would be ' +
      'baselined as "never rendered".',
  ).toBeLessThanOrEqual(MAX_CAPTURE_HEIGHT_PX);
}

/**
 * Screenshot options for element/locator-scoped shots (e.g. a single table),
 * sharing the same animation/caret/tolerance discipline as the full-page
 * baselines but without `fullPage` (invalid for a locator screenshot).
 */
export function elementScreenshotOptions(): {
  animations: 'disabled';
  caret: 'hide';
  maxDiffPixels: number;
  threshold: 0;
} {
  return {
    animations: 'disabled',
    caret: 'hide',
    maxDiffPixels: 800,
    threshold: 0,
  };
}

/**
 * Per-page terminal content marker.
 *
 * `waitForPageReady` only awaits `domcontentloaded` + `networkidle`, and
 * networkidle fires 500ms after the last request — which says nothing about
 * whether layout has settled. A full-page capture of a tall page can therefore
 * stitch while content is still resolving. That is not hypothetical: the
 * 2026-08-02 generation produced a `user-profile-mobile-light` baseline that
 * ended 3,351px early, missing an entire muscle group, and nothing failed.
 *
 * Each entry names the last thing its page renders. If that marker is present
 * and geometry has stopped moving, the page is complete by construction rather
 * than by elapsed time. Pages without an entry still get the geometry and
 * resource guards below.
 */
const TERMINAL_MARKERS: Record<string, string> = {
  'user-profile': '[data-section="fatigue context"]',
  progression: '.current-goals table tbody tr',
  'body-composition': '.bc-table tbody tr',
  // The heatmap mounts its SVGs client-side, so the page can be laid out before
  // any region is coloured. `data-heatmap-state` is rendered unconditionally and
  // this matches only its two TERMINAL values: `empty` (no data, no panel) and
  // `ready` (bands applied, one frame painted). The transient `pending` is
  // deliberately absent - matching it would make the wait a no-op.
  fatigue: '[data-heatmap-state="ready"], [data-heatmap-state="empty"]',
};

export interface VisualReadyOptions {
  /** Page name from the visual spec's page table. */
  name: string;
  /** Frames of unchanged geometry required before the page counts as settled. */
  stableFrames?: number;
  timeoutMs?: number;
}

/**
 * Assert a page is completely rendered before it is captured.
 *
 * Two conditions, neither of them a sleep:
 *  1. the page-specific terminal marker exists, where one is defined;
 *  2. scrollHeight/scrollWidth hold steady across N consecutive animation
 *     frames — the condition the truncated capture actually violated.
 *
 * Font and image settling is deliberately NOT repeated here: every call site
 * runs `prepareForScreenshot` first, and that owns the stronger version of the
 * wait (forces `loading="eager"`, awaits `decode()`, and fails with the pending
 * list rather than racing a deadline). Decoded pixels are still not a settled
 * layout, which is why the geometry gate below runs after it rather than
 * instead of it.
 *
 * Failures carry the measured geometry series, so the diagnostic says what was
 * still moving instead of only reporting a timeout.
 */
export async function waitForVisualReady(
  page: Page,
  { name, stableFrames = 5, timeoutMs = 8000 }: VisualReadyOptions,
): Promise<void> {
  const marker = TERMINAL_MARKERS[name];
  if (marker) {
    try {
      await page.locator(marker).first().waitFor({ state: 'attached', timeout: timeoutMs });
    } catch {
      throw new Error(
        '[visual-ready] ' + name + ': terminal marker ' + marker + ' never appeared within ' +
          timeoutMs + 'ms. The page did not finish rendering, so capturing it would ' +
          'freeze incomplete content into a baseline.',
      );
    }
  }

  const result = await page.evaluate(
    async ({ stableFrames, timeoutMs }) => {
      const nextFrame = () => new Promise<void>((r) => requestAnimationFrame(() => r()));
      const geometry = () => {
        const el = document.documentElement;
        return el.scrollHeight + 'x' + el.scrollWidth;
      };

      const series: string[] = [];
      const deadline = performance.now() + timeoutMs;
      let last = geometry();
      let stable = 0;
      series.push(last);
      while (performance.now() < deadline) {
        await nextFrame();
        const now = geometry();
        if (now === last) {
          stable += 1;
          if (stable >= stableFrames) {
            return { settled: true, series: series.slice(-8) };
          }
        } else {
          stable = 0;
          series.push(now);
          last = now;
        }
      }
      return { settled: false, series: series.slice(-8) };
    },
    { stableFrames, timeoutMs },
  );

  if (!result.settled) {
    throw new Error(
      '[visual-ready] ' + name + ': page geometry never held still for ' + stableFrames +
        ' frames within ' + timeoutMs + 'ms. Observed sequence (most recent last): ' +
        result.series.join(' -> ') + '. Capturing a page whose height is still moving ' +
        'is how a truncated baseline gets committed.',
    );
  }
}
