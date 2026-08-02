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
