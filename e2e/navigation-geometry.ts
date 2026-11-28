import type { Locator, Page } from '@playwright/test';
import { expect } from './strict-fixtures';

/** Geometry in CSS viewport coordinates, including both axes of each hit target. */
export async function targetGeometry(control: Locator) {
  return control.evaluate(el => {
    const { left, right, top, bottom, width, height } = el.getBoundingClientRect();
    const cx = (left + right) / 2;
    const cy = (top + bottom) / 2;
    const points = [[cx, cy], [left + 2, cy], [right - 2, cy], [cx, top + 2], [cx, bottom - 2]];
    const header = document.querySelector('#navbar')!.getBoundingClientRect();
    const panel = document.querySelector('#navbarNav')!.getBoundingClientRect();
    return {
      width, height, cx, cy, left, right, top, bottom,
      contained: left >= 0 && right <= innerWidth && top >= header.top && bottom <= header.bottom + 0.5,
      ownsTargets: points.every(([x, y]) => el.contains(document.elementFromPoint(x, y))),
      panelGap: panel.top - header.bottom,
      pageWidth: document.documentElement.scrollWidth, viewport: document.documentElement.clientWidth,
    };
  });
}

export async function visibleLabelFits(control: Locator) {
  return control.evaluate(el => {
    const rect = el.getBoundingClientRect();
    // A DOM Range measures the entire string even inside a clipped 1px
    // screen-reader label. Only the naming control has that extra text.
    let spokenSuffix: Element | null = null;
    if (el.id === 'muscleModeToggle') {
      spokenSuffix = el.querySelector(':scope > .visually-hidden');
      if (spokenSuffix?.textContent?.trim() !== 'muscle names') return false;
      const style = getComputedStyle(spokenSuffix);
      if (style.width !== '1px' || style.height !== '1px' || style.overflow !== 'hidden' ||
          style.clip !== 'rect(0px, 0px, 0px, 0px)') return false;
    }
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      if (!walker.currentNode.textContent?.trim()) continue;
      if (spokenSuffix?.contains(walker.currentNode)) continue;
      const parent = walker.currentNode.parentElement!;
      const style = getComputedStyle(parent);
      if (style.visibility !== 'visible' || Number(style.opacity) === 0) return false;
      const range = document.createRange();
      range.selectNodeContents(walker.currentNode);
      const text = range.getBoundingClientRect();
      if (!text.width || text.left < rect.left - 1 || text.right > rect.right + 1
        || text.top < rect.top - 1 || text.bottom > rect.bottom + 1) return false;
    }
    return true;
  });
}

export async function expectGlyph(link: Locator, hex: string, family = 'Font Awesome 5 Free') {
  const weight = family === 'Font Awesome 5 Brands' ? '400' : '900';
  const icon = link.locator('[data-visual-icon]');
  await expect(icon).toBeVisible();
  await icon.scrollIntoViewIfNeeded();
  const sample = await icon.evaluate(async (el, { codepoint, family, weight }) => {
    const link = el.closest('a,button')!;
    const ink = getComputedStyle(el, '::before');
    const linkStyle = getComputedStyle(link);
    const text = String.fromCodePoint(parseInt(codepoint, 16));
    const face = await document.fonts.load(`${weight} 16px "${family}"`, text);
    const rect = el.getBoundingClientRect();
    const cx = (rect.left + rect.right) / 2;
    const cy = (rect.top + rect.bottom) / 2;
    const painted = [[cx, cy], [rect.left + 1, cy], [rect.right - 1, cy],
      [cx, rect.top + 1], [cx, rect.bottom - 1]].every(([x, y]) => link.contains(document.elementFromPoint(x, y)));
    let opaque = true;
    for (let ancestor: Element | null = el; ancestor; ancestor = ancestor.parentElement) {
      if (Number(getComputedStyle(ancestor).opacity) !== 1) opaque = false;
    }
    return {
      glyph: ink.content.replace(/^["']|["']$/g, ''), face: ink.fontFamily.replace(/["']/g, ''),
      weight: ink.fontWeight, visible: ink.display !== 'none' && ink.visibility === 'visible' && Number(ink.opacity) === 1,
      inherited: ink.color === linkStyle.color && ink.fontSize === linkStyle.fontSize,
      fontLoaded: face.some(f => f.status === 'loaded' && f.weight === weight),
      painted, opaque, positive: rect.width > 0 && rect.height > 0,
    };
  }, { codepoint: hex, family, weight });
  expect(sample, await link.getAttribute('id') ?? 'nav glyph').toEqual({
    glyph: String.fromCodePoint(parseInt(hex, 16)), face: family, weight,
    visible: true, inherited: true, fontLoaded: true, painted: true, opaque: true, positive: true,
  });
}

export async function expectCurrentMarker(link: Locator, mobile: boolean) {
  await expect(link).toHaveClass(/\bactive\b/);
  const marked = await link.evaluate((el, phone) => {
    const style = getComputedStyle(el);
    const painted = (ink: string) => ink !== 'transparent' && ink !== 'rgba(0, 0, 0, 0)';
    const border = phone ? style.borderLeft : style.borderBottom;
    if (border.startsWith('2px solid') && painted(phone ? style.borderLeftColor : style.borderBottomColor)) return true;
    return ['::before', '::after'].some(pseudo => {
      const marker = getComputedStyle(el, pseudo);
      const thickness = phone ? marker.width : marker.height;
      const length = parseFloat(phone ? marker.height : marker.width);
      return marker.content !== 'none' && marker.display !== 'none' && marker.visibility === 'visible'
        && Number(marker.opacity) > 0 && thickness === '2px' && length > 3
        && parseFloat(phone ? marker.left : marker.bottom) === 0 && painted(marker.backgroundColor);
    });
  }, mobile);
  expect(marked, 'visible 2px current-location marker at the leading or bottom edge').toBe(true);
}

export async function prepareNavigation(page: Page, width: number, theme: 'light' | 'dark', scale: number, height = 900, route = '/fatigue') {
  await page.setViewportSize({ width, height });
  await page.goto('/fatigue');
  await page.evaluate(({ theme, scale }) => {
    localStorage.setItem('darkMode', String(theme === 'dark'));
    localStorage.setItem('ui-scale-level', String(scale));
    document.cookie = `ui-scale-level=${scale}; path=/; SameSite=Lax`;
    localStorage.setItem('hypertrophy_filter_view_mode', 'advanced');
  }, { theme, scale });
  await page.goto(route);
  await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
  await expect(page.locator('html')).toHaveAttribute('data-scale', String(scale));
  await expect(page.locator('#muscleModeToggle')).toContainText('Scientific');
  const zoom = await page.locator('#navbar').evaluate(el => [
    Number(getComputedStyle(document.documentElement).zoom), Number(getComputedStyle(el).zoom),
  ]);
  expect(zoom[0]).toBe(scale === 8 ? 1.2 : 1);
  expect(zoom[0] * zoom[1]).toBeCloseTo(1, 2);
}

export async function scrollCompact(page: Page) {
  await page.mouse.move(80, 240);
  await page.mouse.wheel(0, 400);
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(80);
  await expect(page.locator('#navbar')).toHaveClass(/nb-compact/);
}

export async function expectReadableLink(link: Locator) {
  const ratio = await link.evaluate(el => {
    const ctx = document.createElement('canvas').getContext('2d')!;
    function rgba(css: string) {
      ctx.clearRect(0, 0, 1, 1);
      ctx.fillStyle = css;
      ctx.fillRect(0, 0, 1, 1);
      return ctx.getImageData(0, 0, 1, 1).data;
    }
    function luminance(rgb: Uint8ClampedArray) {
      return [0.2126, 0.7152, 0.0722].reduce((sum, weight, i) => {
        const c = rgb[i] / 255;
        return sum + weight * (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
      }, 0);
    }
    let background = rgba('white');
    for (let parent: Element | null = el; parent; parent = parent.parentElement) {
      const color = rgba(getComputedStyle(parent).backgroundColor);
      if (color[3] === 255) { background = color; break; }
    }
    const ink = luminance(rgba(getComputedStyle(el).color));
    const surface = luminance(background);
    return (Math.max(ink, surface) + 0.05) / (Math.min(ink, surface) + 0.05);
  });
  expect(ratio, 'navigation label contrast').toBeGreaterThanOrEqual(4.5);
}

export async function expectBodyClearance(page: Page) {
  const heading = page.locator('#main-content h1:visible').first();
  const first = page.locator('#main-content').locator('button:visible:enabled, a[href]:visible, select:visible:enabled, input:visible:enabled').first();
  await expect(heading).toBeVisible();
  const header = page.locator('#navbar');
  const headerBox = (await header.boundingBox())!;
  expect((await heading.boundingBox())!.y).toBeGreaterThanOrEqual(headerBox.y + headerBox.height - 1);
  await first.scrollIntoViewIfNeeded();
  await first.focus();
  await expect(first).toBeFocused();
  const usable = await first.evaluate(el => {
    const box = el.getBoundingClientRect();
    return box.top >= document.querySelector('#navbar')!.getBoundingClientRect().bottom - 1
      && el.contains(document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2));
  });
  expect(usable, 'actual first control receives focus and pointer below the fixed header').toBe(true);
}
