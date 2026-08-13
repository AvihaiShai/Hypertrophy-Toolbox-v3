/**
 * E2E Test: Accessibility
 * 
 * Tests accessibility features including:
 * - Keyboard navigation
 * - ARIA attributes
 * - Focus management
 * - Skip links
 * - Screen reader support
 * - Color contrast (manual checks noted)
 */
import { test, expect, expectToast, ROUTES, SELECTORS, waitForPageReady } from './fixtures';
import type { Page } from '@playwright/test';

/** WCAG 2.1 SC 1.4.3 floor for normal-size body text. */
const MIN_TEXT_CONTRAST = 4.5;

/**
 * WCAG 2.2 SC 2.5.8 (AA) requires 24x24. This app declares a stricter 32px in
 * three route bundles, so that is what is enforced. The 44x44 figure often
 * quoted is SC 2.5.5, which is AAA.
 */
const MIN_TARGET_PX = 32;

/**
 * Computed contrast ratio for an element's text against the first ancestor
 * background with non-zero alpha. The foreground is composited over that
 * background; the background itself is used as-is.
 *
 * Deliberately a second implementation of the math in
 * `visual-field-separator.spec.ts`: that copy lives inside a `page.evaluate()`
 * body, so it is unreachable from here without restructuring that spec.
 */
async function textContrast(
  page: Page,
  selector: string
): Promise<{ ratio: number; foreground: string; background: string }> {
  return page.evaluate((sel) => {
    const el = document.querySelector(sel);
    if (!el) throw new Error(`textContrast: no element matched ${sel}`);

    const parse = (value: string) => {
      const match = value.match(/rgba?\(([^)]+)\)/);
      if (!match) return null;
      const parts = match[1].split(',').map((n) => parseFloat(n));
      return { rgb: [parts[0], parts[1], parts[2]], alpha: parts.length > 3 ? parts[3] : 1 };
    };
    const luminance = (rgb: number[]) => {
      const channel = (v: number) => {
        const x = v / 255;
        return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
      };
      return 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2]);
    };

    let node: Element | null = el;
    let background: number[] | null = null;
    while (node) {
      const raw = getComputedStyle(node).backgroundColor;
      const parsed = parse(raw);
      // Unparseable is not the same as transparent. Conflating them would walk
      // past a painted layer and score the text against the wrong backdrop.
      if (!parsed) throw new Error(`textContrast: unparseable background '${raw}' above ${sel}`);
      if (parsed.alpha > 0) {
        if (parsed.alpha < 1) {
          throw new Error(
            `textContrast: backdrop above ${sel} is translucent (${raw}); this helper does not ` +
              'composite stacked translucent layers'
          );
        }
        background = parsed.rgb;
        break;
      }
      node = node.parentElement;
    }
    if (!background) throw new Error(`textContrast: no opaque background above ${sel}`);

    const fg = parse(getComputedStyle(el).color);
    if (!fg) throw new Error(`textContrast: unparseable color on ${sel}`);
    const composited = fg.rgb.map((v, i) => v * fg.alpha + background![i] * (1 - fg.alpha));

    const a = luminance(composited);
    const b = luminance(background);
    const rounded = (rgb: number[]) => `rgb(${rgb.map((n) => Math.round(n)).join(', ')})`;
    return {
      ratio: (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05),
      // The composited value, so the reported colour is the one that was scored.
      foreground: rounded(composited),
      background: rounded(background),
    };
  }, selector);
}

/**
 * Switch theme through the real toggle, assert it took, then wait for `body`'s
 * paint to settle.
 *
 * `data-theme` flips before the colours finish transitioning (`theme-dark.css`
 * puts an unconditional 0.3s transition on `body`), so sampling on the attribute
 * alone reads intermediate values and scores a paint the user never sees.
 *
 * Only `body` is sampled, which is what both callers measure.
 */
async function setThemeAndSettle(page: Page, theme: 'light' | 'dark'): Promise<void> {
  const current = await page.locator('html').getAttribute('data-theme');
  if ((current === 'dark') !== (theme === 'dark')) {
    await page.locator(SELECTORS.DARK_MODE_TOGGLE).first().click();
  }

  // Asserted here rather than in the callers so it covers both, and so a
  // missing attribute cannot be silently read as "light".
  await expect(page.locator('html')).toHaveAttribute('data-theme', theme);

  await page.evaluate(async () => {
    const frame = () => new Promise((resolve) => requestAnimationFrame(() => resolve(null)));
    const sample = () => {
      const style = getComputedStyle(document.body);
      return `${style.color}|${style.backgroundColor}`;
    };
    // Bounded by frames and by wall clock: a throttled renderer stops producing
    // frames altogether, which would otherwise hang until the test timeout and
    // report as a generic 30s failure instead of this message.
    const deadline = performance.now() + 5000;
    let previous = sample();
    let stable = 0;
    while (performance.now() < deadline) {
      await frame();
      const now = sample();
      if (now === previous) {
        if (++stable >= 12) return;
      } else {
        stable = 0;
      }
      previous = now;
    }
    throw new Error(`setThemeAndSettle: body colours never settled (last ${previous})`);
  });
}

async function waitForBootstrapModalEvent(page: Page, selector: string, eventName: 'shown.bs.modal' | 'hidden.bs.modal'): Promise<void> {
  await page.evaluate(
    ({ selector, eventName }) => new Promise<void>((resolve, reject) => {
      const modal = document.querySelector(selector);
      if (!modal) {
        reject(new Error(`Modal not found: ${selector}`));
        return;
      }

      const timeoutId = window.setTimeout(() => {
        reject(new Error(`Timed out waiting for ${eventName} on ${selector}`));
      }, 5000);

      modal.addEventListener(eventName, () => {
        window.clearTimeout(timeoutId);
        resolve();
      }, { once: true });
    }),
    { selector, eventName }
  );
}

test.describe('Keyboard Navigation', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('can tab through navigation links', async ({ page }) => {
    // Start from body
    await page.locator('body').focus();
    
    // Tab through elements
    for (let i = 0; i < 10; i++) {
      await page.keyboard.press('Tab');
    }

    // Should reach a navbar link
    const activeElement = await page.evaluate(() => document.activeElement?.tagName);
    expect(['A', 'BUTTON', 'INPUT', 'SELECT']).toContain(activeElement);
  });

  test('navbar links are keyboard accessible', async ({ page }) => {
    const navLinks = page.locator('.navbar-nav a.nav-link');
    const count = await navLinks.count();

    // At least verify we found some nav links
    expect(count).toBeGreaterThan(0);

    // Every visible link, not the first three: a defect past the sampling cap
    // was structurally invisible to this test.
    for (let i = 0; i < count; i++) {
      const link = navLinks.nth(i);
      if (!(await link.isVisible())) continue;
      await link.focus();
      await expect(link, `nav link ${i} could not take focus`).toBeFocused();
    }
  });

  // This used to call .click(), so keyboard activation could break silently.
  test('enter key activates links', async ({ page }) => {
    const workoutPlanLink = page.locator('#nav-workout-plan');
    await workoutPlanLink.focus();
    await expect(workoutPlanLink).toBeFocused();

    await Promise.all([
      page.waitForURL(/workout_plan/),
      page.keyboard.press('Enter'),
    ]);

    await waitForPageReady(page);
    expect(page.url()).toContain('workout_plan');
  });

  // KI-006: this used to open the modal behind an `isVisible()` guard, press Escape,
  // and then *click the close button* if the modal was still open — so it passed whether
  // or not Escape worked, and skipped silently if the trigger was not visible. Both
  // escapes are removed: the trigger must be usable, and Escape alone must close it.
  test('escape key closes modals', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    const generateBtn = page.locator('#generate-plan-btn');
    await expect(generateBtn).toBeVisible();
    await expect(generateBtn).toBeEnabled();

    const shownPromise = waitForBootstrapModalEvent(page, '#generatePlanModal', 'shown.bs.modal');
    await generateBtn.click();
    await shownPromise;

    const modal = page.locator('#generatePlanModal');
    await expect(modal).toBeVisible();

    // Escape is the only close path exercised here. No fallback click.
    const hiddenPromise = waitForBootstrapModalEvent(page, '#generatePlanModal', 'hidden.bs.modal');
    await page.keyboard.press('Escape');
    await hiddenPromise;

    await expect(modal).not.toBeVisible();
    await expect(page.locator('.modal-backdrop')).toHaveCount(0);
    await expect(page.locator('body.modal-open')).toHaveCount(0);
  });

  test('dropdown menus are keyboard accessible', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    const select = page.locator(SELECTORS.ROUTINE_ENV);
    await select.focus();
    
    // Should be focused
    await expect(select).toBeFocused();

    // Arrow down should work
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');
  });
});

test.describe('ARIA Attributes', () => {
  test('page has proper landmarks', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Check for main landmark
    const main = page.locator('main, [role="main"]');
    await expect(main).toBeVisible();

    // Check for navigation landmark
    const nav = page.locator('nav, [role="navigation"]');
    await expect(nav).toBeVisible();
  });

  test('buttons have accessible names', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    const buttons = page.locator('button');
    const count = await buttons.count();

    // Every visible button, not the first ten.
    let checked = 0;
    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);
      if (!(await button.isVisible())) continue;
      checked++;

      const ariaLabel = await button.getAttribute('aria-label');
      const text = await button.textContent();
      const title = await button.getAttribute('title');

      expect(
        ariaLabel || text?.trim() || title,
        `button ${i} (id=${(await button.getAttribute('id')) ?? '-'}) has no accessible name`
      ).toBeTruthy();
    }

    expect(checked, 'no visible buttons were found to check').toBeGreaterThan(0);
  });

  test('form inputs have labels', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    const inputs = page.locator('input:visible, select:visible');
    const count = await inputs.count();

    // Every visible control, not the first ten.
    let checked = 0;
    for (let i = 0; i < count; i++) {
      const input = inputs.nth(i);
      const id = await input.getAttribute('id');
      if (!id) continue;
      checked++;

      const ariaLabel = await input.getAttribute('aria-label');
      const ariaLabelledBy = await input.getAttribute('aria-labelledby');
      const hasLabel = (await page.locator(`label[for="${id}"]`).count()) > 0;

      expect(
        hasLabel || ariaLabel || ariaLabelledBy,
        `control #${id} has no label, aria-label, or aria-labelledby`
      ).toBeTruthy();
    }

    expect(checked, 'no visible identified controls were found to check').toBeGreaterThan(0);
  });

  test('images have alt text', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const images = page.locator('img');
    const count = await images.count();

    for (let i = 0; i < count; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');
      const role = await img.getAttribute('role');
      
      // Image should have alt or be marked decorative
      expect(alt !== null || role === 'presentation').toBeTruthy();
    }
  });

  test('tables have proper structure', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    const tables = page.locator('table');
    const count = await tables.count();
    let checked = 0;

    for (let i = 0; i < count; i++) {
      const table = tables.nth(i);
      const isVisible = await table.isVisible();
      
      if (isVisible) {
        // Table should have headers
        const headers = table.locator('th');
        const headerCount = await headers.count();
        expect(headerCount).toBeGreaterThan(0);
        checked++;
      }
    }

    expect(checked, 'no visible tables were found to check').toBeGreaterThan(0);
  });

  test('modals have proper ARIA attributes', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    const modals = page.locator('.modal');
    const count = await modals.count();

    for (let i = 0; i < count; i++) {
      const modal = modals.nth(i);
      
      // Check for proper modal attributes
      const role = await modal.getAttribute('role');
      const ariaModal = await modal.getAttribute('aria-modal');
      const ariaLabelledBy = await modal.getAttribute('aria-labelledby');
      const ariaHidden = await modal.getAttribute('aria-hidden');
      
      expect(role === 'dialog' || ariaModal === 'true' || ariaHidden).toBeTruthy();
    }
  });
});

test.describe('Focus Management', () => {
  test('focus visible on interactive elements', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const link = page.locator(SELECTORS.NAV_WORKOUT_PLAN);
    await link.focus();

    // `style.outline` is the shorthand, which Chromium serialises as
    // "<color> <style> <width>" — e.g. "rgb(74, 74, 90) none 3px" when nothing
    // is drawn. It is never the bare string 'none', so the old
    // `style.outline !== 'none'` operand was unconditionally true and
    // short-circuited the rest. Read the longhands instead.
    const indicator = await link.evaluate((el) => {
      const style = getComputedStyle(el);
      return {
        outlineDrawn: style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0,
        shadowDrawn: style.boxShadow !== 'none',
        outlineStyle: style.outlineStyle,
        outlineWidth: style.outlineWidth,
        boxShadow: style.boxShadow,
      };
    });

    expect(
      indicator.outlineDrawn || indicator.shadowDrawn,
      `focused link paints no visible indicator: outline ${indicator.outlineStyle} ` +
        `${indicator.outlineWidth}, box-shadow ${indicator.boxShadow}`
    ).toBe(true);
  });

  // Containment only. The forward/backward wrap contracts are owned by
  // ui-hardening.spec.ts ("UI Hardening — Modal Keyboard & Focus"); this test
  // deliberately does not duplicate them.

  test('modal traps focus', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    const generateBtn = page.locator('#generate-plan-btn');
    await expect(generateBtn).toBeVisible();
    await expect(generateBtn).toBeEnabled();

    const shownPromise = waitForBootstrapModalEvent(page, '#generatePlanModal', 'shown.bs.modal');
    await generateBtn.click();
    await shownPromise;

    const modal = page.locator('#generatePlanModal');
    await expect(modal).toBeVisible();

    for (let i = 0; i < 12; i++) {
      await page.keyboard.press('Tab');
      const containment = await page.evaluate(() => {
        const active = document.activeElement;
        return {
          inside: !!active?.closest('#generatePlanModal'),
          landedOn: active ? `${active.tagName}#${(active as HTMLElement).id || '-'}` : 'null',
        };
      });
      expect(
        containment.inside,
        `tab ${i + 1} moved focus outside #generatePlanModal, onto ${containment.landedOn}`
      ).toBe(true);
    }
  });

  test('focus returns after modal closes', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    const generateBtn = page.locator('#generate-plan-btn');
    await expect(generateBtn).toBeVisible();
    await expect(generateBtn).toBeEnabled();

    const shownPromise = waitForBootstrapModalEvent(page, '#generatePlanModal', 'shown.bs.modal');
    await generateBtn.click();
    await shownPromise;

    const modal = page.locator('#generatePlanModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Close modal via close button for reliability
    const closeBtn = modal.locator('.btn-close').first();
    const hiddenPromise = waitForBootstrapModalEvent(page, '#generatePlanModal', 'hidden.bs.modal');
    await closeBtn.click();
    await hiddenPromise;
    await expect(modal).not.toBeVisible({ timeout: 3000 });

    await expect(generateBtn).toBeFocused();
  });
});

test.describe('Skip Links', () => {
  test('skip link targets and focuses the single main landmark', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const main = page.locator('main#main-content');
    await expect(page.locator('main')).toHaveCount(1);
    await expect(main).toHaveAttribute('tabindex', '-1');

    await page.keyboard.press('Tab');
    const skipLink = page.locator('.nb-skip-link');
    await expect(skipLink).toBeFocused();
    await expect(skipLink).toHaveAttribute('href', '#main-content');
    await skipLink.click();
    await expect(main).toBeFocused();
  });
});

test.describe('Color and Contrast', () => {
  test('text is readable in light mode', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);
    await setThemeAndSettle(page, 'light');

    const { ratio, foreground, background } = await textContrast(page, 'body');
    expect(
      ratio,
      `light-mode body text ${ratio.toFixed(2)}:1 (${foreground} on ${background}) is below ${MIN_TEXT_CONTRAST}:1`
    ).toBeGreaterThanOrEqual(MIN_TEXT_CONTRAST);
  });

  test('text is readable in dark mode', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);
    await setThemeAndSettle(page, 'dark');

    const { ratio, foreground, background } = await textContrast(page, 'body');
    expect(
      ratio,
      `dark-mode body text ${ratio.toFixed(2)}:1 (${foreground} on ${background}) is below ${MIN_TEXT_CONTRAST}:1`
    ).toBeGreaterThanOrEqual(MIN_TEXT_CONTRAST);
  });

  // Scoped to a named in-content link. `locator('a').first()` resolved to the
  // visually-hidden .nb-skip-link, and the old right operand was dead: a
  // computed `color` is always a non-empty string, so the || could never be
  // reached. This is a design contract for this app's content links, not a
  // claim of SC 1.4.1 conformance — that SC scopes to links inside a block of
  // text, which the navbar is not.
  test('links are distinguishable', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const link = page.locator('a.developer-link').first();
    await expect(link).toBeVisible();

    const style = await link.evaluate((el) => ({
      color: getComputedStyle(el).color,
      decoration: getComputedStyle(el).textDecorationLine,
    }));
    const bodyColor = await page.evaluate(() => getComputedStyle(document.body).color);

    const distinctColor = style.color !== bodyColor;
    const underlined = style.decoration.includes('underline');
    expect(
      distinctColor || underlined,
      `content link is neither recoloured (${style.color} vs body ${bodyColor}) nor underlined (${style.decoration})`
    ).toBe(true);
  });

  // This never induced an error. On a fresh /workout_plan the old selector did
  // match one node — the .text-danger paragraph inside the hidden
  // #clearPlanModal — but isVisible() skipped every body, so no assertion ran.
  // A bare "the set is non-empty" guard would therefore also have passed
  // without inducing anything.
  test('error states are not color-only', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    // Submitting with nothing selected returns before any network call
    // (workout-plan-add-exercise.js), so this writes nothing to the shared DB.
    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();

    // Toast first: it auto-dismisses on a timer, while the invalid-field
    // marking persists. Both are set in the same synchronous handler.
    await expectToast(page, /please select/i);

    // The app marks required fields with .is-invalid-required, not Bootstrap's
    // .is-invalid. Register row X2.
    const invalid = page.locator('.is-invalid-required:visible');
    await expect(
      invalid.first(),
      'no visible invalid field appeared, so the error state was never induced'
    ).toBeVisible();

    // The second non-colour signal: focus moves to the first incomplete
    // control. This holds on the cascade branch, which is the one that runs on
    // a fresh page — routine-cascade.js resets #routine to '' on load, so the
    // routine is always the first thing missing.
    const invalidIsFocused = await page.evaluate(() => {
      const active = document.activeElement;
      return !!active && active.classList.contains('is-invalid-required');
    });
    expect(invalidIsFocused, 'focus did not move to the invalid control').toBe(true);
  });
});

test.describe('Responsive Accessibility', () => {
  test('touch targets are adequately sized on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const buttons = page.locator('button:visible, a.btn:visible');
    const count = await buttons.count();

    // Every visible target must pass; the old form sampled five and passed if
    // *one* cleared the bar. Note the 32px declarations live in the workout-plan
    // / workout-log / user-profile bundles, none of which loads on `/`. Here the
    // binding target is #eraseDataBtn, whose height is derived from padding +
    // line-height (measured 37.2px), so the margin is ~5px and moves with font
    // metrics.
    let measured = 0;
    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);
      const box = await button.boundingBox();
      if (!box) continue;
      measured++;

      const label = (await button.textContent())?.trim().slice(0, 40) || (await button.getAttribute('id')) || `#${i}`;
      expect(
        Math.min(box.width, box.height),
        `touch target "${label}" is ${Math.round(box.width)}x${Math.round(box.height)}, below ${MIN_TARGET_PX}px`
      ).toBeGreaterThanOrEqual(MIN_TARGET_PX);
    }

    expect(measured, 'no visible touch targets were found to measure').toBeGreaterThan(0);
  });

  // KNOWN WEAK: `body.style.zoom` is not real browser zoom. Register row X4.
  test('text remains readable when zoomed 200%', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    // Zoom to 200%
    await page.evaluate(() => {
      document.body.style.zoom = '2';
    });

    // Check that content is still visible
    const mainContent = page.locator('main, .container, .content');
    await expect(mainContent.first()).toBeVisible();

    // Reset zoom
    await page.evaluate(() => {
      document.body.style.zoom = '1';
    });
  });
});

test.describe('Screen Reader Support', () => {
  test('live regions exist for updates', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    // Check for toast container with aria-live
    const liveRegions = page.locator('[aria-live], [role="alert"], [role="status"]');
    const count = await liveRegions.count();

    expect(count).toBeGreaterThan(0);
  });

  test('progress indicators have ARIA attributes', async ({ page }) => {
    await page.goto(ROUTES.VOLUME_SPLITTER);
    await waitForPageReady(page);

    const progressBars = page.locator('[role="progressbar"], .progress-bar, progress');
    const count = await progressBars.count();

    for (let i = 0; i < count; i++) {
      const bar = progressBars.nth(i);
      const isVisible = await bar.isVisible();
      
      if (isVisible) {
        const ariaValueNow = await bar.getAttribute('aria-valuenow');
        const ariaValueMin = await bar.getAttribute('aria-valuemin');
        const ariaValueMax = await bar.getAttribute('aria-valuemax');
        const value = await bar.getAttribute('value');
        
        // Progress bars should have value attributes
        expect(ariaValueNow || value).toBeTruthy();
      }
    }
  });

  test('headings are hierarchical', async ({ page }) => {
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    const h1 = page.locator('h1');
    const h2 = page.locator('h2');
    
    // Should have h1
    const h1Count = await h1.count();
    expect(h1Count).toBeGreaterThanOrEqual(1);

    // If there's h2, there should be h1
    const h2Count = await h2.count();
    if (h2Count > 0) {
      expect(h1Count).toBeGreaterThanOrEqual(1);
    }
  });
});
