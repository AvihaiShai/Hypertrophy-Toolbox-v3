/**
 * P5 redesign navigation coverage.
 *
 * Uses strict fixtures so null/undefined selector errors fail this redesign gate.
 */
import type { Page } from '@playwright/test';
import { test, expect, ROUTES, SELECTORS, resetWorkoutPlan, waitForPageReady } from './strict-fixtures';

import { expectBodyClearance, expectCurrentMarker, expectGlyph, expectReadableLink, prepareNavigation, scrollCompact, targetGeometry, visibleLabelFits } from './navigation-geometry';

const ANALYZE_TOGGLE = '#navbar .dropdown-toggle:has-text("Analyze")';
const ROUTE_LIST = [
  ROUTES.HOME,
  ROUTES.WORKOUT_PLAN,
  ROUTES.WORKOUT_LOG,
  ROUTES.WEEKLY_SUMMARY,
  ROUTES.SESSION_SUMMARY,
  ROUTES.PROGRESSION,
  ROUTES.BODY_COMPOSITION,
  ROUTES.VOLUME_SPLITTER,
] as const;

async function openAnalyzeDropdown(page: Page, mode: 'hover' | 'click' = 'hover'): Promise<void> {
  const analyzeToggle = page.locator(ANALYZE_TOGGLE);
  await expect(analyzeToggle).toBeVisible();
  if (mode === 'hover') {
    await analyzeToggle.hover();
  } else {
    await analyzeToggle.click();
  }
  await expect(page.locator('#navbar .dropdown-menu.show')).toBeVisible();
}

async function openMobileNavbar(page: Page): Promise<void> {
  const collapse = page.locator('#navbarNav');
  const toggle = page.locator('#navbar .navbar-toggler');

  await expect(toggle).toBeVisible();
  await toggle.click();
  await expect(collapse).toHaveClass(/show/);
}

async function clickDarkModeToggle(page: Page): Promise<void> {
  await page.locator(SELECTORS.DARK_MODE_TOGGLE).click();
}

test.describe('P5 navbar dropdown and backup navigation', () => {
  test('top-level nav order matches the redesigned workflow', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const labels = await page.locator('#navbarNav > ul.navbar-nav').first().evaluate((navList) =>
      Array.from(navList.children).map((item) => {
        const link = item.querySelector(':scope > .nav-link');
        return (link?.textContent || '').trim().replace(/\s+/g, ' ');
      })
    );

    expect(labels).toEqual([
      'Plan',
      'Log',
      'Analyze',
      'Progress',
      'Profile',
      'Body Composition',
      'Distribute',
      'Backup',
    ]);

    const overflowingLabels = await page.locator('#navbarNav > ul.navbar-nav').first().evaluate((navList) =>
      Array.from(navList.querySelectorAll(':scope > .nav-item > .nav-link'))
        .filter((link) => link.scrollWidth > link.clientWidth + 1)
        .map((link) => (link.textContent || '').trim().replace(/\s+/g, ' '))
    );
    expect(overflowingLabels).toEqual([]);

    const theme = page.locator(SELECTORS.DARK_MODE_TOGGLE);
    for (const width of [1360, 1440, 1501, 1601]) {
      await page.setViewportSize({ width, height: 900 });
      await expect.poll(() => theme.evaluate(button => {
        const { left, right, top, height } = button.getBoundingClientRect();
        return right <= innerWidth && [left + 2, right - 2].every(x =>
          button.contains(document.elementFromPoint(x, top + height / 2)),
        );
      })).toBe(true);
    }

    const brandLink = page.locator(SELECTORS.NAV_BRAND);
    const brandTarget = await targetGeometry(brandLink);
    expect(brandTarget.height).toBeGreaterThanOrEqual(44);
    expect(brandTarget.contained && brandTarget.ownsTargets).toBe(true);
    const brandPadding = await brandLink.evaluate((brand) => {
      const style = getComputedStyle(brand);
      const frame = brand.closest('.container-fluid')!;
      return {
        left: Number.parseFloat(style.paddingLeft),
        right: Number.parseFloat(style.paddingRight),
        glyphOffset: brand.querySelector('.nav-icon')!.getBoundingClientRect().left - frame.getBoundingClientRect().left,
        gutter: Number.parseFloat(getComputedStyle(frame).paddingLeft),
      };
    });
    expect(brandPadding.left).toBeGreaterThanOrEqual(12);
    expect(brandPadding.right).toBeGreaterThanOrEqual(12);
    expect(Math.abs(brandPadding.glyphOffset - brandPadding.gutter)).toBeLessThanOrEqual(1);
  });

  test('Analyze dropdown opens on hover and contains Weekly and Session links', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    await openAnalyzeDropdown(page);

    const weekly = page.locator(SELECTORS.NAV_WEEKLY_SUMMARY);
    const session = page.locator(SELECTORS.NAV_SESSION_SUMMARY);
    await expect(weekly).toBeVisible();
    await expect(session).toBeVisible();
    await expect(weekly).toContainText('Weekly');
    await expect(session).toContainText('Session');
  });

  test('destination links and their glyphs inherit colour without hover motion', async ({ page }) => {
    await prepareNavigation(page, 1440, 'light', 6);
    for (const theme of ['light', 'dark']) {
      await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
      for (const link of [SELECTORS.NAV_USER_PROFILE, SELECTORS.NAV_BODY_COMPOSITION, SELECTORS.NAV_BACKUP]) {
        const item = page.locator(link);
        await item.hover();
        const icon = item.locator('[data-visual-icon]');
        await expect(icon).toHaveCSS('color', await item.evaluate(el => getComputedStyle(el).color));
        for (const target of [item, icon]) {
          await expect(target).toHaveCSS('transform', 'none');
          await expect(target).toHaveCSS('animation-name', 'none');
        }
      }
      await clickDarkModeToggle(page);
    }
  });

  test('Backup nav points to the dedicated backup page', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const backup = page.locator(SELECTORS.NAV_BACKUP);
    await expect(backup).toBeVisible();
    await expect(backup).toHaveAttribute('href', '/backup');
  });

  test('Backup nav opens the dedicated backup page from every page', async ({ page }) => {
    for (const route of ROUTE_LIST) {
      await page.goto(route);
      await waitForPageReady(page);

      await page.locator(SELECTORS.NAV_BACKUP).click();
      await waitForPageReady(page);
      await expect(page).toHaveURL(/\/backup/);
      await expect(page.locator(SELECTORS.PAGE_BACKUP)).toBeVisible();
    }
  });

  test('mobile Analyze dropdown expands inline and links navigate', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);

    const brand = page.getByRole('link', { name: 'Hypertrophy Toolbox' });
    await expect(brand.getByText('Hypertrophy Toolbox')).toBeVisible();
    await expect(brand).toHaveAttribute('aria-current', 'page');

    await openMobileNavbar(page);
    await openAnalyzeDropdown(page, 'click');

    const analyzeToggle = page.locator(ANALYZE_TOGGLE);
    const dropdownMenu = page.locator('#navbar .dropdown-menu.show');
    await expect(dropdownMenu).toHaveCSS('position', 'static');

    const toggleBox = await analyzeToggle.boundingBox();
    const menuBox = await dropdownMenu.boundingBox();
    expect(toggleBox).not.toBeNull();
    expect(menuBox).not.toBeNull();
    expect(menuBox!.y).toBeGreaterThan(toggleBox!.y);

    await page.locator(SELECTORS.NAV_WEEKLY_SUMMARY).click();
    await waitForPageReady(page);
    await expect(page).toHaveURL(/\/weekly_summary/);

    await expect(brand).not.toHaveAttribute('aria-current', 'page');

    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);
    await openMobileNavbar(page);
    await openAnalyzeDropdown(page, 'click');
    await page.locator(SELECTORS.NAV_SESSION_SUMMARY).click();
    await waitForPageReady(page);
    await expect(page).toHaveURL(/\/session_summary/);
  });

  test('dark mode toggle still works after navbar restructure', async ({ page }) => {
    await page.goto(ROUTES.HOME);
    await page.evaluate(() => localStorage.setItem('darkMode', 'false'));
    await page.reload();
    await waitForPageReady(page);

    await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
    await expect(page.locator(SELECTORS.DARK_MODE_TOGGLE)).toBeVisible();
    await clickDarkModeToggle(page);
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  });
});

// ---------------------------------------------------------------------------
// Issue #733: mobile menu panel.
// ---------------------------------------------------------------------------

type Theme = 'light' | 'dark';
type Scenario = { width: number; height: number; theme: Theme; compact: boolean };

const MENU_CONTROLS = [
  '#nav-workout-plan',
  '#nav-workout-log',
  '#nav-analyze-toggle',
  '#nav-progression-plan',
  '#nav-user-profile',
  '#nav-body-composition',
  '#nav-volume-splitter',
  '#nav-backup',
  '#scale-decrease',
  '#scale-increase',
  '#muscleModeToggle',
  '#darkModeToggle',
] as const;

const TOGGLER = '#navbar .navbar-toggler';

async function loadAt(
  page: Page,
  { width, height, theme, compact }: Scenario,
): Promise<void> {
  await page.setViewportSize({ width, height });
  await page.goto(ROUTES.HOME);
  await page.evaluate(
    (value) => localStorage.setItem('darkMode', value),
    theme === 'dark' ? 'true' : 'false',
  );
  await page.reload();
  await waitForPageReady(page);
  await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
  if (compact) {
    await page.evaluate(() => document.getElementById('navbar')!.classList.add('nb-compact'));
  }
}

async function measurePanel(page: Page) {
  return page.evaluate(() => {
    const panel = document.getElementById('navbarNav')!;
    const header = document.getElementById('navbar')!;
    const rect = panel.getBoundingClientRect();
    return {
      headerBottom: header.getBoundingClientRect().bottom,
      top: rect.top,
      bottom: rect.bottom,
      clientHeight: panel.clientHeight,
      scrollHeight: panel.scrollHeight,
      innerHeight: window.innerHeight,
      compact: header.classList.contains('nb-compact'),
    };
  });
}

/** Wait until Bootstrap has finished and the 200ms slideInDown has stopped moving the panel. */
async function waitForPanelSettled(page: Page): Promise<void> {
  await expect(page.locator('#navbarNav')).toHaveClass(/show/);
  await expect(page.locator('#navbarNav')).not.toHaveClass(/collapsing/);
  let previous = '';
  let stableRuns = 0;
  await expect
    .poll(
      async () => {
        const current = JSON.stringify(await measurePanel(page));
        stableRuns = current === previous ? stableRuns + 1 : 0;
        previous = current;
        return stableRuns >= 3;
      },
      { timeout: 5_000, intervals: [60] },
    )
    .toBe(true);
}

async function openAndSettle(page: Page): Promise<void> {
  await openMobileNavbar(page);
  await waitForPanelSettled(page);
}

function panelGeometryProblems(label: string, g: Awaited<ReturnType<typeof measurePanel>>): string[] {
  const problems: string[] = [];
  if (Math.abs(g.top - g.headerBottom) > 0.5) {
    problems.push(`${label}: panel top ${g.top} != header bottom ${g.headerBottom}`);
  }
  if (Math.abs(g.bottom - g.innerHeight) > 0.5) {
    problems.push(`${label}: panel bottom ${g.bottom} != innerHeight ${g.innerHeight}`);
  }
  const needed = g.innerHeight - g.headerBottom - 1;
  if (g.clientHeight < needed) {
    problems.push(`${label}: panel clientHeight ${g.clientHeight} < ${needed} (scrollHeight ${g.scrollHeight})`);
  }
  return problems;
}

async function unreachableControls(page: Page): Promise<string[]> {
  return page.evaluate((selectors) => {
    const headerBottom = document.getElementById('navbar')!.getBoundingClientRect().bottom;
    const bad: string[] = [];
    for (const selector of selectors) {
      const element = document.querySelector<HTMLElement>(selector);
      if (!element) {
        bad.push(`${selector}: missing`);
        continue;
      }
      element.scrollIntoView({ block: 'nearest' });
      const rect = element.getBoundingClientRect();
      const x = rect.left + rect.width / 2;
      const y = rect.top + rect.height / 2;
      const inView =
        rect.width > 0 && rect.height > 0 &&
        y >= headerBottom && y <= window.innerHeight &&
        x >= 0 && x <= window.innerWidth;
      const hit = document.elementFromPoint(x, y);
      if (!inView) {
        bad.push(`${selector}: centre (${Math.round(x)},${Math.round(y)}) outside header-bottom..viewport-bottom`);
      } else if (!hit || !element.contains(hit)) {
        bad.push(`${selector}: covered by ${hit ? (hit.id || hit.tagName) : 'nothing'}`);
      }
    }
    return bad;
  }, [...MENU_CONTROLS]);
}

function alphaOf(color: string): number | null {
  const parseAlpha = (raw: string): number => {
    const text = raw.trim();
    return text.endsWith('%') ? Number.parseFloat(text) / 100 : Number.parseFloat(text);
  };
  const rgb = color.match(/^rgba?\(\s*([^)]*)\)/);
  if (rgb) {
    const parts = rgb[1].split(/[\s,/]+/).filter(Boolean);
    return parts.length >= 4 ? parseAlpha(parts[3]) : 1;
  }
  const modern = color.match(/^color\(\s*[a-z0-9-]+\s+([^)]*)\)/);
  if (modern) {
    const [, alpha] = modern[1].split('/');
    return alpha === undefined ? 1 : parseAlpha(alpha);
  }
  return null;
}

function describeScenario(s: Scenario): string {
  return `${s.width}x${s.height} ${s.theme} ${s.compact ? 'compact' : 'normal'} header`;
}

async function sampleFor<T>(durationMs: number, take: () => Promise<T>): Promise<T[]> {
  const samples: T[] = [];
  const start = Date.now();
  await expect
    .poll(
      async () => {
        samples.push(await take());
        return Date.now() - start >= durationMs;
      },
      { timeout: durationMs + 10_000, intervals: [50] },
    )
    .toBe(true);
  return samples;
}

type MenuSample = {
  show: boolean;
  collapsing: boolean;
  aria: string | null;
  overflow: string;
  inert: number;
  mainAriaHidden: string | null;
  togglerFocused: boolean;
  shown: number;
  hidden: number;
};

async function menuSample(page: Page): Promise<MenuSample> {
  return page.evaluate(() => {
    const panel = document.getElementById('navbarNav')!;
    const toggler = document.querySelector('#navbar .navbar-toggler')!;
    const counters = window as unknown as Record<string, number | undefined>;
    return {
      show: panel.classList.contains('show'),
      collapsing: panel.classList.contains('collapsing'),
      aria: toggler.getAttribute('aria-expanded'),
      overflow: document.body.style.overflow,
      inert: document.querySelectorAll('[inert]').length,
      mainAriaHidden: document.getElementById('main-content')?.getAttribute('aria-hidden') ?? null,
      togglerFocused: document.activeElement === toggler,
      shown: counters.__navShown ?? 0,
      hidden: counters.__navHidden ?? 0,
    };
  });
}

/** Count Bootstrap collapse lifecycle events from now on (counters live on window). */
async function countCollapseEvents(page: Page): Promise<void> {
  await page.evaluate(() => {
    const counters = window as unknown as Record<string, number>;
    counters.__navShown = 0;
    counters.__navHidden = 0;
    const panel = document.getElementById('navbarNav')!;
    panel.addEventListener('shown.bs.collapse', () => { counters.__navShown += 1; });
    panel.addEventListener('hidden.bs.collapse', () => { counters.__navHidden += 1; });
  });
}

/** A point inside the open panel where the panel element itself is the hit target. */
async function findEmptyPanelPoint(page: Page): Promise<{ x: number; y: number } | null> {
  return page.evaluate(() => {
    const panel = document.getElementById('navbarNav')!;
    const rect = panel.getBoundingClientRect();
    const yMin = Math.ceil(Math.max(rect.top, 0)) + 1;
    const yMax = Math.floor(Math.min(rect.bottom, window.innerHeight)) - 1;
    for (let y = yMin; y <= yMax; y += 1) {
      for (let x = 2; x < window.innerWidth - 2; x += 2) {
        if (document.elementFromPoint(x, y) === panel) return { x, y };
      }
    }
    return null;
  });
}

async function menuIsReleased(page: Page): Promise<string[]> {
  const s = await menuSample(page);
  const problems: string[] = [];
  if (s.overflow !== '') problems.push(`body overflow is "${s.overflow}", expected ""`);
  if (s.inert !== 0) problems.push(`${s.inert} [inert] element(s), expected 0`);
  if (s.mainAriaHidden !== null) problems.push(`#main-content aria-hidden="${s.mainAriaHidden}", expected none`);
  return problems;
}

/** Guards the release assertions: they prove nothing unless the open menu held the page first. */
async function expectPageHeld(page: Page): Promise<void> {
  await expect
    .poll(async () => {
      const s = await menuSample(page);
      return s.overflow === 'hidden' && s.inert > 0;
    }, { message: 'the open menu locks page scroll and makes page content inert' })
    .toBe(true);
}

async function waitForMenuClosed(page: Page, timeout = 3_000): Promise<void> {
  await expect
    .poll(
      async () => {
        const s = await menuSample(page);
        return !s.show && !s.collapsing;
      },
      { timeout },
    )
    .toBe(true);
}

async function tabFrom(page: Page, selector: string) {
  await page.evaluate(() => {
    const w = window as unknown as { __lastKeydown?: KeyboardEvent };
    if ((w as { __keyCapture?: boolean }).__keyCapture) return;
    (w as { __keyCapture?: boolean }).__keyCapture = true;
    document.addEventListener('keydown', (event) => { w.__lastKeydown = event; }, true);
  });
  await page.locator(selector).focus();
  await page.keyboard.press('Tab');
  return page.evaluate(() => {
    const w = window as unknown as { __lastKeydown?: KeyboardEvent };
    const active = document.activeElement as HTMLElement | null;
    return {
      key: w.__lastKeydown?.key ?? null,
      defaultPrevented: w.__lastKeydown?.defaultPrevented ?? null,
      activeId: active?.id ?? '',
      insideNavbarNav: Boolean(active?.closest('#navbarNav')),
    };
  });
}

test.describe('#733 mobile menu panel', () => {
  test('open mobile menu panel spans header bottom to viewport bottom and every control is hit-testable in both hamburger bands', async ({ page }) => {
    test.setTimeout(120_000);
    const problems: string[] = [];
    const scenarios: Scenario[] = [];
    for (const [width, height] of [[375, 812], [1100, 900]] as const) {
      for (const theme of ['light', 'dark'] as const) {
        for (const compact of [false, true]) scenarios.push({ width, height, theme, compact });
      }
    }

    for (const scenario of scenarios) {
      const label = describeScenario(scenario);
      await loadAt(page, scenario);
      await openAndSettle(page);
      const g = await measurePanel(page);
      if (g.compact !== scenario.compact) problems.push(`${label}: header compact state is ${g.compact}`);
      problems.push(...panelGeometryProblems(label, g));
      for (const bad of await unreachableControls(page)) problems.push(`${label}: ${bad}`);
    }

    expect(problems).toEqual([]);
  });

  test('open mobile menu panel on a short viewport scrolls inside the panel so every control stays reachable', async ({ page }) => {
    test.setTimeout(90_000);
    const problems: string[] = [];
    for (const theme of ['light', 'dark'] as const) {
      const scenario: Scenario = { width: 375, height: 300, theme, compact: false };
      const label = describeScenario(scenario);
      await loadAt(page, scenario);
      await openAndSettle(page);
      const g = await measurePanel(page);
      // Precondition of this test: the content really is taller than the space below the header.
      expect(g.scrollHeight, `${label}: content must overflow the short viewport`).toBeGreaterThan(
        g.innerHeight - g.headerBottom,
      );
      problems.push(...panelGeometryProblems(label, g));
      // A wheel gesture, because scrollIntoView also moves a box the user cannot scroll.
      await page.mouse.move(scenario.width / 2, (g.headerBottom + g.innerHeight) / 2);
      await page.mouse.wheel(0, 120);
      await expect
        .poll(() => page.evaluate(() => document.getElementById('navbarNav')!.scrollTop), {
          message: `${label}: a wheel gesture over the panel scrolls it`,
        })
        .toBeGreaterThan(0);
      for (const bad of await unreachableControls(page)) problems.push(`${label}: ${bad}`);
    }
    expect(problems).toEqual([]);
  });

  test('open mobile menu panel background is fully opaque in light and dark at both hamburger bands', async ({ page }) => {
    test.setTimeout(90_000);
    const problems: string[] = [];
    for (const [width, height] of [[375, 812], [1100, 900]] as const) {
      for (const theme of ['light', 'dark'] as const) {
        const scenario: Scenario = { width, height, theme, compact: false };
        await loadAt(page, scenario);
        await openAndSettle(page);
        const color = await page.locator('#navbarNav').evaluate((el) => getComputedStyle(el).backgroundColor);
        const alpha = alphaOf(color);
        if (alpha === null) {
          problems.push(`${describeScenario(scenario)}: unparseable background "${color}"`);
        } else if (alpha !== 1) {
          problems.push(`${describeScenario(scenario)}: background "${color}" has alpha ${alpha}, expected 1`);
        }
      }
    }
    expect(problems).toEqual([]);
  });

  for (const reducedMotion of [false, true]) {
    test(`empty-space click closes the open mobile menu and it stays closed${reducedMotion ? ' under reduced motion' : ''}`, async ({ page }) => {
      if (reducedMotion) await page.emulateMedia({ reducedMotion: 'reduce' });
      await loadAt(page, { width: 375, height: 812, theme: 'light', compact: false });
      await openAndSettle(page);
      await expectPageHeld(page);
      await countCollapseEvents(page);

      const point = await findEmptyPanelPoint(page);
      expect(point, 'a point where #navbarNav itself is the hit target').not.toBeNull();

      await page.mouse.click(point!.x, point!.y);

      // Hold past the ~600ms window in which a toggled close would reopen the menu.
      const samples = await sampleFor(1_500, () => menuSample(page));
      const reopened = samples.filter((s) => s.show || s.aria !== 'false' || s.shown > 0);
      expect(
        reopened.map((s) => ({ show: s.show, aria: s.aria, shown: s.shown })).slice(0, 3),
        'menu must never reopen after an empty-space click',
      ).toEqual([]);

      await waitForMenuClosed(page);
      const final = await menuSample(page);
      expect(final.overflow, 'body scroll lock released').toBe('');
      expect(final.inert, 'nothing inert').toBe(0);
      expect(final.mainAriaHidden).toBeNull();
      expect(final.togglerFocused, 'focus returned to the toggler').toBe(true);
      expect(final.shown, 'shown.bs.collapse events after the click').toBe(0);
      expect(final.hidden, 'hidden.bs.collapse reached').toBeGreaterThanOrEqual(1);
    });
  }

  test('one toggler click reopens the mobile menu after Escape, empty-space click and resize closes', async ({ page }) => {
    test.setTimeout(120_000);
    const problems: string[] = [];

    for (const method of ['escape', 'empty-click', 'resize'] as const) {
      await loadAt(page, { width: 375, height: 812, theme: 'light', compact: false });
      await openAndSettle(page);

      if (method === 'escape') {
        await page.keyboard.press('Escape');
      } else if (method === 'empty-click') {
        const point = await findEmptyPanelPoint(page);
        if (!point) {
          problems.push(`${method}: no empty panel point found`);
          continue;
        }
        await page.mouse.click(point.x, point.y);
      } else {
        await page.setViewportSize({ width: 1440, height: 900 });
        await expect.poll(() => menuSample(page).then((s) => s.show), { timeout: 3_000 }).toBe(false).catch(() => {
          problems.push(`${method}: menu still open at 1440px`);
        });
        await page.setViewportSize({ width: 375, height: 812 });
      }

      try {
        await waitForMenuClosed(page);
      } catch {
        problems.push(`${method}: menu is not closed after the close action`);
        continue;
      }

      await page.locator(TOGGLER).click();
      try {
        await expect
          .poll(async () => {
            const s = await menuSample(page);
            return s.show && !s.collapsing && s.aria === 'true';
          }, { timeout: 3_000 })
          .toBe(true);
      } catch {
        problems.push(`${method}: one toggler click did not reopen the menu`);
        continue;
      }
      const held = await sampleFor(600, () => menuSample(page));
      if (held.some((s) => !s.show)) problems.push(`${method}: menu closed again after the reopen click`);
    }

    expect(problems).toEqual([]);
  });

  test('widening 375 to 1440 with the menu open leaves no focus trap and reopening still traps focus', async ({ page }) => {
    await loadAt(page, { width: 375, height: 812, theme: 'light', compact: false });
    await openAndSettle(page);
    await expectPageHeld(page);

    await page.setViewportSize({ width: 1440, height: 900 });
    await expect.soft.poll(() => menuSample(page).then((s) => s.show), { timeout: 3_000 }).toBe(false);

    const afterTab = await tabFrom(page, '#darkModeToggle');
    expect.soft(afterTab.key, 'the Tab keydown was captured').toBe('Tab');
    expect.soft(afterTab.defaultPrevented, 'Tab keydown default-prevented by a stale trap').toBe(false);
    expect.soft(afterTab.activeId, 'focus wrapped to Plan').not.toBe('nav-workout-plan');
    expect.soft(afterTab.insideNavbarNav, 'focus stayed inside #navbarNav').toBe(false);
    expect.soft(await menuIsReleased(page), 'scroll lock and inert released').toEqual([]);

    // Reopen at the hamburger width: trap works again, Escape closes.
    await page.setViewportSize({ width: 375, height: 812 });
    await openAndSettle(page);
    const ids = await page.evaluate(() => {
      const items = Array.from(
        document.querySelectorAll<HTMLElement>(
          '#navbarNav a[href], #navbarNav button:not([disabled]), #navbarNav [tabindex]:not([tabindex="-1"])',
        ),
      ).filter((el) => {
        const style = getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden';
      });
      return { first: items[0]?.id ?? '', last: items[items.length - 1]?.id ?? '' };
    });
    expect(ids.first).toBe('nav-workout-plan');
    // The menu moves focus to its first control shortly after opening; wait for that.
    await expect
      .poll(() => page.evaluate(() => document.activeElement?.id ?? ''), { timeout: 3_000 })
      .toBe(ids.first);
    const wrapped = await tabFrom(page, `#${ids.last}`);
    expect.soft(wrapped.activeId, 'Tab from the last control wraps to the first').toBe(ids.first);
    expect.soft(wrapped.defaultPrevented).toBe(true);

    await page.keyboard.press('Escape');
    await expect.soft.poll(async () => {
      const s = await menuSample(page);
      return !s.show && !s.collapsing && s.aria === 'false';
    }, { timeout: 3_000 }).toBe(true);
  });

  test('resize threshold: 1100 to 1101 and 1359 keep the menu open, 1360 and 1100 to 1440 close it and release the page', async ({ page }) => {
    test.setTimeout(90_000);
    const problems: string[] = [];

    const stayOpenAt = async (width: number): Promise<void> => {
      await page.setViewportSize({ width, height: 900 });
      const samples = await sampleFor(700, () => menuSample(page));
      if (samples.some((s) => !s.show || s.aria !== 'true')) {
        problems.push(`menu closed when resized to ${width}px (expected to stay open)`);
      }
    };
    const closeAt = async (label: string, width: number): Promise<void> => {
      await page.setViewportSize({ width, height: 900 });
      try {
        await waitForMenuClosed(page);
      } catch {
        problems.push(`${label}: menu still open at ${width}px (expected closed)`);
        return;
      }
      for (const issue of await menuIsReleased(page)) problems.push(`${label}: ${issue}`);
    };

    await loadAt(page, { width: 1100, height: 900, theme: 'light', compact: false });
    await openAndSettle(page);
    await expectPageHeld(page);
    await stayOpenAt(1101);
    await stayOpenAt(1359);
    await closeAt('1359 to 1360', 1360);

    await loadAt(page, { width: 1100, height: 900, theme: 'light', compact: false });
    await openAndSettle(page);
    await expectPageHeld(page);
    await closeAt('1100 to 1440', 1440);

    expect(problems).toEqual([]);
  });

  test('crossing to 1360px while the menu is still opening leaves scroll lock, inert state and the focus trap cleared after Bootstrap finishes', async ({ page }) => {
    await loadAt(page, { width: 375, height: 812, theme: 'light', compact: false });
    // Stretch Bootstrap's opening transition so the viewport change reliably lands inside it.
    await page.addStyleTag({ content: '#navbarNav.collapsing { transition-duration: 2000ms !important; }' });
    await countCollapseEvents(page);

    await page.locator(TOGGLER).click();
    await page.setViewportSize({ width: 1440, height: 900 });
    const atCrossing = await page.evaluate(() => {
      const panel = document.getElementById('navbarNav')!;
      const counters = window as unknown as Record<string, number>;
      return {
        innerWidth: window.innerWidth,
        collapsing: panel.classList.contains('collapsing'),
        show: panel.classList.contains('show'),
        shown: counters.__navShown,
      };
    });
    expect(atCrossing, 'the crossing must land while Bootstrap is still opening').toEqual({
      innerWidth: 1440,
      collapsing: true,
      show: false,
      shown: 0,
    });

    // Bootstrap finishes opening (shown.bs.collapse) and the panel leaves .collapsing.
    await expect.poll(() => menuSample(page).then((s) => s.shown), { timeout: 8_000 }).toBeGreaterThanOrEqual(1);
    await expect
      .poll(() => menuSample(page).then((s) => !s.collapsing), { timeout: 8_000 })
      .toBe(true);

    const samples = await sampleFor(1_200, () => menuSample(page));
    const dirty = samples.filter((s) => s.overflow !== '' || s.inert !== 0 || s.mainAriaHidden !== null);
    expect(
      dirty.slice(0, 2).map((s) => ({ overflow: s.overflow, inert: s.inert, mainAriaHidden: s.mainAriaHidden })),
      'scroll lock / inert must stay cleared after shown.bs.collapse at desktop width',
    ).toEqual([]);

    const afterTab = await tabFrom(page, '#darkModeToggle');
    expect(afterTab.key).toBe('Tab');
    expect(afterTab.defaultPrevented, 'no focus trap at desktop width').toBe(false);
    expect(afterTab.activeId).not.toBe('nav-workout-plan');
  });

  test('mobile menu lifecycle listeners are registered exactly once per page load', async ({ page }) => {
    await page.addInitScript(() => {
      const log: Record<string, number> = {};
      (window as unknown as { __navListenerLog: Record<string, number> }).__navListenerLog = log;
      const original = EventTarget.prototype.addEventListener;
      EventTarget.prototype.addEventListener = function (
        this: EventTarget,
        type: string,
        listener: EventListenerOrEventListenerObject | null,
        options?: boolean | AddEventListenerOptions,
      ) {
        if (this instanceof Element && this.id === 'navbarNav') {
          const key = `navbarNav:${type}`;
          log[key] = (log[key] ?? 0) + 1;
        } else if (this === window && type === 'resize' && /navbar-enhancements/.test(new Error().stack ?? '')) {
          log['window:resize(navbar-enhancements)'] = (log['window:resize(navbar-enhancements)'] ?? 0) + 1;
        }
        return original.call(this, type, listener, options);
      } as typeof EventTarget.prototype.addEventListener;
    });

    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto(ROUTES.HOME);
    await waitForPageReady(page);
    await openAndSettle(page); // the keydown trap is attached on open

    const log = await page.evaluate(
      () => (window as unknown as { __navListenerLog: Record<string, number> }).__navListenerLog,
    );
    expect({
      shown: log['navbarNav:shown.bs.collapse'] ?? 0,
      hidden: log['navbarNav:hidden.bs.collapse'] ?? 0,
      click: log['navbarNav:click'] ?? 0,
      keydown: log['navbarNav:keydown'] ?? 0,
      resize: log['window:resize(navbar-enhancements)'] ?? 0,
    }).toEqual({ shown: 1, hidden: 1, click: 1, keydown: 1, resize: 1 });
  });
});

// Ordinary rendering, without the deterministic screenshot helper that masks icons.
const NAV_GLYPHS = {
  'nav-brand': 'f44b', 'nav-workout-plan': 'f0ae', 'nav-workout-log': 'f518',
  'nav-analyze-toggle': 'f201', 'nav-weekly-summary': 'f784', 'nav-session-summary': 'f783',
  'nav-fatigue': 'f242', 'nav-progression-plan': 'f3bf', 'nav-user-profile': 'f2bd',
  'nav-body-composition': 'f545', 'nav-volume-splitter': 'f1de', 'nav-backup': 'f07c',
};

test.describe('Navigation on the fixed header', () => {
  for (const theme of ['light', 'dark'] as const) {
    test(`bundled destination glyphs and current markers render in ${theme}`, async ({ page }) => {
      test.setTimeout(90_000);
      for (const width of [390, 768, 1440]) {
        await prepareNavigation(page, width, theme, 6);
        const mobile = width < 1360;
        if (mobile) await openAndSettle(page);
        await openAnalyzeDropdown(page, mobile ? 'click' : 'hover');
        await expect(page.locator('#navbar [aria-current="page"]')).toHaveAttribute('id', 'nav-fatigue');
        for (const [id, codepoint] of Object.entries(NAV_GLYPHS)) {
          await expectGlyph(page.locator('#' + id), codepoint);
        }
        for (const id of ['nav-workout-plan', 'nav-fatigue']) await expectReadableLink(page.locator('#' + id));
        for (const id of ['nav-analyze-toggle', 'nav-fatigue']) {
          await expectCurrentMarker(page.locator('#' + id), mobile);
        }
        await expectGlyph(page.locator('.nav-signature-link'), 'f08c', 'Font Awesome 5 Brands');
        await expectGlyph(page.locator('#muscleModeToggle'), 'f610');
        await expectGlyph(page.locator('#darkModeToggle'), theme === 'dark' ? 'f185' : 'f186');
        if (mobile) {
          const button = page.getByRole('button', { name: 'Toggle navigation menu' });
          const symbol = button.locator('[data-visual-icon]');
          await expect(symbol).toBeVisible();
          const hasStrokes = await symbol.evaluate(el => {
            const path = el.querySelector('path') ?? (el.matches('path') ? el : null);
            const expected = 'M4 7h22M4 15h22M4 23h22';
            const color = getComputedStyle(el.closest('button')!).color;
            if (path) return path.getAttribute('d') === expected && getComputedStyle(path).stroke === color;
            const style = getComputedStyle(el);
            return decodeURIComponent(style.maskImage).includes(expected) && style.backgroundColor === color;
          });
          expect(hasStrokes, 'original three strokes painted in the button colour').toBe(true);
        }
      }
    });

    test.describe(`touch controls in ${theme}`, () => {
      test.use({ hasTouch: true });
      test(`scale eight phone button owns its centre and edges in ${theme}`, async ({ page }) => {
        test.setTimeout(120_000);
        for (const width of [320, 360, 390]) {
          await prepareNavigation(page, width, theme, 8, 480);
          for (const compact of [false, true]) {
            if (compact) await scrollCompact(page);
            const button = page.locator(TOGGLER);
            for (const state of ['closed', 'open', 'analyze'] as const) {
              if (state === 'open') await waitForPanelSettled(page);
              if (state === 'analyze') await openAnalyzeDropdown(page, 'click');
              const g = await targetGeometry(button);
              const label = `${width}/${theme}/compact=${compact}/${state}`;
              expect(g.width, label).toBeGreaterThanOrEqual(44);
              expect(g.height, label).toBeGreaterThanOrEqual(44);
              expect(g.contained && g.ownsTargets, label).toBe(true);
              expect(g.pageWidth, label).toBe(g.viewport);
              if (state !== 'closed') expect(Math.abs(g.panelGap), label).toBeLessThanOrEqual(0.5);
              if (state !== 'open') await page.mouse.click(g.cx, g.cy);
            }
            await waitForMenuClosed(page);
            const g = await targetGeometry(button);
            await page.touchscreen.tap(g.right - 2, g.cy);
            await waitForPanelSettled(page);
            await page.keyboard.press('Escape');
            await waitForMenuClosed(page);
            await expect(button).toBeFocused();
            expect(await menuIsReleased(page)).toEqual([]);
          }
        }
      });
    });

    test(`all desktop operations fit one row at regular and compact sizes in ${theme}`, async ({ page }) => {
      test.setTimeout(150_000);
      const selectors = ['#nav-brand', ...MENU_CONTROLS.slice(0, 8), '.nav-signature-link',
        '#scale-decrease', '#scale-indicator', '#scale-increase', '#muscleModeToggle', '#darkModeToggle'];
      for (const scale of [6, 8]) {
        await prepareNavigation(page, 1360, theme, scale, 540, ROUTES.USER_PROFILE);
        for (const compact of [false, true]) {
          if (compact) await scrollCompact(page);
          for (const width of [1360, 1440, 1501, 1601]) {
            await page.setViewportSize({ width, height: 540 });
            const rects = [];
            for (const selector of selectors) {
              const control = page.locator(selector);
              const label = `${width}/${scale}/compact=${compact}/${selector}`;
              const g = await targetGeometry(control);
              expect(g.width > 0 && g.height > 0 && g.contained && g.ownsTargets, label).toBe(true);
              expect(await visibleLabelFits(control), label + ' full label').toBe(true);
              rects.push(g);
            }
            const sorted = rects.sort((a, b) => a.left - b.left);
            for (let i = 1; i < sorted.length; i++) {
              expect(sorted[i].left).toBeGreaterThanOrEqual(sorted[i - 1].right - 1);
            }
            expect(Math.max(...rects.map(r => r.top))).toBeLessThan(Math.min(...rects.map(r => r.bottom)));
          }
        }
      }
    });
  }
});

// Session populates this initially empty table from its contribution-mode GET.
// Both successful outcomes exclude its Loading spinner and fetch-error message.
async function expectSessionReady(page: Page) {
  await expect(page.locator('#navbar [aria-current="page"]')).toHaveAttribute('id', 'nav-session-summary');
  const table = page.locator('#session-summary-table');
  const routines = table.locator('td[data-label="Routine"]');
  const empty = table.getByText('No data available.', { exact: true });
  await expect(routines.or(empty).first()).toBeAttached();
}

test.describe('Navigation keyboard and utility controls', () => {
  for (const width of [320, 1360]) {
    test(`Analyze keyboard activation and route history at ${width}px`, async ({ page }) => {
      for (const key of ['Enter', 'Space']) {
        await prepareNavigation(page, width, key === 'Enter' ? 'light' : 'dark', 6);
        const mobile = width === 320;
        if (mobile) await openAndSettle(page);
        const analyze = page.locator('#nav-analyze-toggle');
        await analyze.focus();
        await page.keyboard.press(key);
        await expect(analyze).toHaveAttribute('aria-expanded', 'true');
        const weekly = page.locator('#nav-weekly-summary');
        if (!(await weekly.evaluate(el => el === document.activeElement))) await page.keyboard.press('Tab');
        for (const id of ['nav-weekly-summary', 'nav-session-summary', 'nav-fatigue']) {
          const item = page.locator('#' + id);
          await expect(item).toBeFocused();
          await expectReadableLink(item);
          const feedback = await item.evaluate(el => {
            const style = getComputedStyle(el);
            return el.matches(':focus-visible') && (style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0
              || style.boxShadow !== 'none');
          });
          expect(feedback, 'keyboard focus has a visible indicator').toBe(true);
          if (id !== 'nav-fatigue') await page.keyboard.press('Tab');
        }
        await page.keyboard.press('Shift+Tab');
        await page.keyboard.press('Enter');
        await expect(page).toHaveURL(/\/session_summary$/);
        const current = page.locator('#navbar [aria-current="page"]');
        await expectSessionReady(page);
        await page.reload();
        await expectSessionReady(page);
        await page.goBack();
        await expect(current).toHaveAttribute('id', 'nav-fatigue');
        await page.goForward();
        await expectSessionReady(page);
      }
    });

    test(`scale, theme and muscle-name controls remain operable at ${width}px`, async ({ page }) => {
      await prepareNavigation(page, width, 'light', 8);
      if (width === 320) await openAndSettle(page);
      const signature = page.locator('.nav-signature-link');
      await expect(signature).toHaveAccessibleName('by Avihai');
      await expect(signature).toHaveAttribute('target', '_blank');
      await expect(signature).toHaveAttribute('href', 'https://www.linkedin.com/in/avihaishai');
      expect((await signature.getAttribute('rel'))?.split(/\s+/)).toEqual(expect.arrayContaining(['noopener', 'noreferrer']));
      const up = page.getByRole('button', { name: 'Increase text size' });
      const down = page.getByRole('button', { name: 'Decrease text size' });
      await expect(up).toBeVisible();
      await expect(up).toBeDisabled();
      await down.click();
      await expect(page.locator('#scale-indicator')).toHaveText('7');
      await page.reload();
      if (width === 320) await openAndSettle(page);
      await expect(page.locator('#scale-indicator')).toHaveText('7');
      await up.click();
      await expect(up).toBeDisabled();
      await page.reload();
      if (width === 320) await openAndSettle(page);
      await expect(page.locator('#scale-indicator')).toHaveText('8');
      await expect(page.locator('html')).toHaveCSS('zoom', '1.2');
      const muscle = page.locator('#muscleModeToggle');
      const dark = page.locator('#darkModeToggle');
      await expect(muscle).toHaveAccessibleName('Scientific muscle names');
      await expect(dark).toHaveAccessibleName('Dark Mode');
      for (const [mode, theme, nextTheme] of [['Simple', 'dark', 'Light Mode'], ['Scientific', 'light', 'Dark Mode']]) {
        await muscle.click();
        await expect(muscle.locator('.muscle-mode-label')).toHaveText(mode);
        await expect(muscle).toHaveAccessibleName(`${mode} muscle names`);
        await expectGlyph(muscle, mode === 'Simple' ? 'f007' : 'f610');
        await dark.click();
        await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
        await expect(dark.locator('span')).toHaveText(nextTheme);
        await expect(dark).toHaveAccessibleName(nextTheme);
        await expect(page.locator('#navbar [aria-current="page"]')).toHaveAttribute('id', 'nav-fatigue');
      }
    });
  }

  test('short compact panel wraps focus in both directions and releases the first page control', async ({ page }) => {
    await prepareNavigation(page, 320, 'dark', 8, 400);
    await scrollCompact(page);
    await openAndSettle(page);
    await expectPageHeld(page);
    const first = page.locator('#nav-workout-plan');
    const last = page.locator('#darkModeToggle');
    await expect(first).toBeFocused();
    await page.keyboard.press('Shift+Tab');
    await expect(last).toBeFocused();
    await expect(last).toBeInViewport();
    await page.keyboard.press('Tab');
    await expect(first).toBeFocused();
    const empty = await findEmptyPanelPoint(page);
    expect(empty).not.toBeNull();
    await page.mouse.click(empty!.x, empty!.y);
    await waitForMenuClosed(page);
    await expect(page.locator(TOGGLER)).toBeFocused();
    expect(await menuIsReleased(page)).toEqual([]);
    await page.evaluate(() => scrollTo({ top: 0, behavior: 'instant' }));
    await expect(page.locator('#navbar')).not.toHaveClass(/nb-compact/);
    await expectBodyClearance(page);
    await openAndSettle(page);
    await page.setViewportSize({ width: 1360, height: 700 });
    await waitForMenuClosed(page);
    expect(await menuIsReleased(page)).toEqual([]);
    await expectBodyClearance(page);
    await page.goto(ROUTES.WORKOUT_PLAN);
    await page.keyboard.press('Tab');
    const skip = page.getByRole('link', { name: 'Skip to main content' });
    await expect(skip).toBeFocused();
    await page.keyboard.press('Enter');
    await expect(page.locator('#main-content')).toBeFocused();
  });
});

test.describe('Navigation before JavaScript starts', () => {
  test.use({ javaScriptEnabled: false });

  test('the utility buttons announce their visible default labels', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(ROUTES.HOME);
    const muscle = page.locator('#muscleModeToggle');
    await expect(muscle.locator('.muscle-mode-label')).toHaveText('Simple');
    await expect(muscle).toHaveAccessibleName('Simple muscle names');
    const theme = page.locator('#darkModeToggle');
    await expect(theme.locator('span')).toHaveText('Dark Mode');
    await expect(theme).toHaveAccessibleName('Dark Mode');
  });
});

test('page operations work after using the scale-eight phone menu', async ({ page }) => {
  test.setTimeout(90_000);
  await prepareNavigation(page, 320, 'light', 8, 640);
  const period = page.locator('#fatigue-period');
  const chosen = await period.evaluate((el: HTMLSelectElement) =>
    Array.from(el.options).find(option => !option.selected)!.value);
  const changed = page.waitForResponse(response => {
    const url = new URL(response.url());
    return response.request().method() === 'GET' && url.pathname === '/fatigue' && url.searchParams.get('period') === chosen;
  });
  await period.selectOption(chosen);
  expect((await changed).ok()).toBe(true);
  await expect(period).toHaveValue(chosen);

  // As elsewhere in the functional suite, these writes go to the seeded E2E DB.
  await resetWorkoutPlan(page);
  const seed = await page.request.post('/add_exercise', { data: {
    routine: 'GYM - Full Body - Workout A', exercise: 'Bench Press', sets: 3,
    min_rep_range: 6, max_rep_range: 8, weight: 100,
  } });
  expect(seed.ok()).toBe(true);
  await openAndSettle(page);
  await page.locator('#nav-workout-plan').click();
  const planned = page.locator('#workout_plan_table_body').getByRole('row', { name: /Bench Press/ });
  await expect(planned).toBeVisible();
  await page.locator('#more-btn').click();
  await expect(page.getByRole('menuitem', { name: 'Open Backup Center' })).toBeVisible();
  await page.keyboard.press('Escape');
  await page.locator('#vpToggle').click();
  await expect(page.locator('#vpToggle')).toHaveAttribute('aria-expanded', 'true');
  await page.getByRole('button', { name: 'Close volume targets' }).click();
  await expect(page.locator('#vpToggle')).toHaveAttribute('aria-expanded', 'false');
  await page.locator('#export-to-log-btn').click();
  await expect(page).toHaveURL(/\/workout_log$/);
  await page.locator('#clear-log-btn').click();
  const dialog = page.locator('#clearLogModal');
  await expect(dialog).toBeVisible();
  await dialog.getByRole('button', { name: 'Cancel' }).click();
  await expect(dialog).toBeHidden();
  const imported = page.waitForResponse(r => r.url().endsWith('/export_to_workout_log') && r.request().method() === 'POST');
  const reloaded = page.waitForEvent('domcontentloaded');
  await page.locator('#import-from-plan-btn').click();
  expect((await imported).ok()).toBe(true);
  await reloaded;
  await expect(page.locator('tr[data-log-id]').first()).toBeVisible();

  await openAndSettle(page);
  await page.locator('#nav-backup').click();
  const name = `Navigation E2E ${Date.now()}`;
  await page.locator('#backup-center-name').fill(name);
  await page.locator('#backup-center-save-submit').scrollIntoViewIfNeeded();
  await page.locator('#backup-center-save-submit').click();
  await page.locator('#backup-search').fill(name);
  await expect(page.locator('#backup-center-list')).toContainText(name);
});
