import type { Locator, Page } from '@playwright/test';

export type VisualTheme = 'light' | 'dark';

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
      /* Playwright captures full pages and oversized locators outside the
         viewport. Sticky table layers are recomposited while that happens, so
         the header and first column can land at different offsets between the
         consecutive frames used by toHaveScreenshot(). Static positioning is
         visually equivalent at the capture's scroll origin and prevents those
         capture-only jumps. */
      [data-testid="exercise-table"] thead th,
      [data-testid="exercise-table"] tr > :first-child {
        position: static !important;
      }
      /* Closed fixed overlays live just outside the viewport. Full-page and
         oversized-locator screenshots expand beyond that viewport and would
         otherwise capture those non-visible layers at compositor-dependent
         offsets. */
      .vp-drawer[aria-hidden="true"],
      .vp-backdrop[hidden] {
        display: none !important;
      }
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

    /* Lazy thumbnails can start loading only when Playwright scrolls an
       oversized target into view. Decode every image up front so neither the
       target geometry nor its paint state changes between comparison frames. */
    const images = Array.from(document.images);
    images.forEach((image) => {
      image.loading = 'eager';
    });
    await Promise.all(images.map((image) => image.decode().catch(() => undefined)));
    await document.fonts.ready;
    await new Promise<void>((resolveFrame) => {
      requestAnimationFrame(() => requestAnimationFrame(() => resolveFrame()));
    });
    window.scrollTo(0, 0);
  });
}

/**
 * Prepare an oversized locator capture without letting the sticky page navbar
 * overlay the locator as Playwright scrolls it into view. Absolute positioning
 * keeps the navbar's full-page behaviour unchanged and moves it out of the
 * table-only capture once the document is scrolled to the target.
 */
export async function prepareForElementScreenshot(page: Page): Promise<void> {
  await prepareForScreenshot(page);
  await page.addStyleTag({
    content: '#navbar { visibility: hidden !important; }',
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
