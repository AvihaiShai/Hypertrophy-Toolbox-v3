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
 * Three independent conditions, none of them a sleep:
 *  1. the page-specific terminal marker exists, where one is defined;
 *  2. fonts are resolved and every image has finished loading, since both
 *     change layout height after networkidle has already fired;
 *  3. scrollHeight/scrollWidth hold steady across N consecutive animation
 *     frames — the condition the truncated capture actually violated.
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

      // Both waits are bounded. A lazy image below the fold never starts
      // loading, so it is never `complete` and fires neither load nor error --
      // awaiting it unconditionally hangs until the test times out, which
      // destroys the diagnostic this contract exists to give. Lazy images are
      // skipped outright (they are not in the capture until scrolled to, and
      // the geometry check below is what actually protects the capture), and
      // the remaining waits race a deadline.
      const bounded = <T,>(p: Promise<T>, ms: number) =>
        Promise.race([p, new Promise<void>((r) => setTimeout(r, ms))]);

      if (document.fonts && document.fonts.ready) {
        await bounded(document.fonts.ready, 3000);
      }
      await bounded(
        Promise.all(
          Array.from(document.images)
            .filter((img) => !img.complete && img.loading !== 'lazy')
            .map(
              (img) =>
                new Promise<void>((resolve) => {
                  img.addEventListener('load', () => resolve(), { once: true });
                  img.addEventListener('error', () => resolve(), { once: true });
                }),
            ),
        ),
        3000,
      );

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
