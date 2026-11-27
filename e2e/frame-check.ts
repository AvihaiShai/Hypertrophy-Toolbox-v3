/**
 * Shared part of the frame check (#736, R21). Not a spec.
 *
 * A route's `*-frame.check.ts` imports this for the launcher handshake, the theme
 * and scale setup, the one-pass read behind C1 to C5 and the C8 source scan, and
 * keeps its own extras beside them. `e2e/scripts/run_frame_check.py` owns the
 * scratch server and names the route's check file for `playwright.frame.config.ts`.
 */
import type { Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import postcss from 'postcss';
import { expect } from './strict-fixtures';

export type Theme = 'light' | 'dark';
export const THEMES: Theme[] = ['light', 'dark'];

/** One page load of a route's matrix. A route adds its own dimensions beside these. */
export type FramePass = { scale: number; width: number; theme: Theme };

/**
 * Where a route keeps its frame, inside `#main-content`: the page header block, and
 * every panel whose left and right edges C1 compares with the gutter.
 */
export type FrameSelectors = { header: string; panels: string };

/** What `readFrame` returns, in the key order `metrics.json` prints. */
export type FrameRead = {
  edges: number[][];
  radii: number[];
  sizes: number[];
  weights: string[];
  effects: string[];
  title: number;
  offset: number;
  overflow: number;
};

export type FrameRun = { run: string; source: string; baseURL: string; control: boolean };

export const gutter = (width: number) => width < 768 ? 16 : width < 1360 ? 24 : 32;

/** The app's zoom factor at each scale level the check uses. */
const SCALE_ZOOM: Record<number, number> = { 6: 1, 8: 1.2 };

const STILL = '*,*::before,*::after { transition: none !important; animation: none !important; }';

/**
 * Reads what the launcher handed over and proves the server is the scratch one: its
 * database, runtime root and source are the run's own. A check that is started any
 * other way stops here.
 */
export async function expectFrameRun(page: Page, baseURL: string | undefined): Promise<FrameRun> {
  const run = process.env.FRAME_RUN;
  const source = process.env.FRAME_SOURCE;
  if (!run || !source || !baseURL) {
    throw new Error('Start the fixture with e2e/scripts/run_frame_check.py --route <route>');
  }
  const identity = await page.request.get('/__frame_identity');
  expect(await identity.json()).toEqual({
    database: path.join(run, 'database.db'), runtime: path.join(run, 'runtime'), source,
  });
  return { run, source, baseURL, control: !!process.env.FRAME_CONTROL };
}

/**
 * Before any navigation: each load copies the theme and scale the pass put in its
 * cookies into the app's own persisted settings, so the page starts in that state.
 */
export async function installFrameSettings(page: Page) {
  await page.addInitScript(() => {
    const dark = document.cookie.split('; ').includes('frame-theme=dark');
    localStorage.setItem('darkMode', String(dark));
    const scale = document.cookie.match(/ui-scale-level=(\d)/);
    localStorage.setItem('ui-scale-level', scale![1]);
  });
}

/** 390 x 844, 768 x 1024 and 900 px high from there. Narrower phones keep 844. */
export function frameViewport(width: number) {
  return { width, height: width < 768 ? 844 : width === 768 ? 1024 : 900 };
}

/** The theme and scale the page reports, and the zoom it computes for that scale. */
export async function expectFrameSettings(page: Page, theme: Theme, scale: number) {
  await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
  await expect(page.locator('html')).toHaveAttribute('data-scale', String(scale));
  expect(await page.locator('html').evaluate(el => Number(getComputedStyle(el).zoom))).toBe(SCALE_ZOOM[scale]);
}

/**
 * Sizes the viewport, sets the pass's theme and scale, loads the route and asserts
 * that both applied. The route then waits for its own content and for the fonts.
 */
export async function openFramePass(page: Page, baseURL: string, route: string, pass: FramePass) {
  await page.setViewportSize(frameViewport(pass.width));
  await page.context().addCookies([
    { name: 'frame-theme', value: pass.theme, url: baseURL },
    { name: 'ui-scale-level', value: String(pass.scale), url: baseURL },
  ]);
  await page.goto(route);
  await expectFrameSettings(page, pass.theme, pass.scale);
}

export async function fontsLoaded(page: Page) {
  await page.evaluate(() => document.fonts.ready.then(() => undefined));
}

/** Transitions and animations off, so a measurement reads the settled value. */
export async function freezeMotion(page: Page) {
  await page.addStyleTag({ content: STILL });
}

/** Read C1 to C5 from rendered elements inside the main content. */
function measureFrame(main: Element, frame: FrameSelectors): FrameRead {
  const round = (value: number) => Math.round(value * 2) / 2;
  const visible = (node: Element) => node.getClientRects().length > 0;
  const population = Array.from(main.querySelectorAll('*')).filter(visible);
  const sizes = new Set<number>(), weights = new Set<string>(), radii = new Set<number>();
  const effects = new Set<string>();
  for (const node of population) {
    const style = getComputedStyle(node);
    const radius = round(parseFloat(style.borderTopLeftRadius));
    if (radius) radii.add(radius);
    if (!style.fontFamily.includes('Font Awesome') &&
        Array.from(node.childNodes).some(child => child.nodeType === Node.TEXT_NODE && child.textContent?.trim())) {
      sizes.add(round(parseFloat(style.fontSize)));
      weights.add(style.fontWeight);
    }
    for (const property of ['box-shadow', 'background-image', 'backdrop-filter']) {
      if (style.getPropertyValue(property) !== 'none') effects.add(property);
    }
  }
  const title = main.querySelector('h1')!;
  const header = main.querySelector(frame.header)!;
  const frames = [header, ...main.querySelectorAll(frame.panels)].filter(visible);
  const edges = frames.map(node => {
    const box = node.getBoundingClientRect();
    return [round(box.left), round(document.documentElement.clientWidth - box.right)];
  });
  return {
    edges, radii: [...radii].sort((a,b) => a-b), sizes: [...sizes].sort((a,b) => a-b),
    weights: [...weights].sort(), effects: [...effects].sort(),
    title: round(parseFloat(getComputedStyle(title).fontSize)),
    offset: round(header.getBoundingClientRect().top - document.querySelector('#navbar')!.getBoundingClientRect().bottom),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
}

/** Read shared and route-specific positions in a single browser evaluation. */
export function readFrame(page: Page, selectors: FrameSelectors): Promise<FrameRead>;
export function readFrame<Extra extends object>(
  page: Page, selectors: FrameSelectors, measureRoute: (main: Element) => Extra,
): Promise<FrameRead & Extra>;
export function readFrame(
  page: Page, selectors: FrameSelectors, measureRoute?: (main: Element) => object,
): Promise<FrameRead> {
  const main = page.locator('#main-content');
  if (!measureRoute) return main.evaluate(measureFrame, selectors);

  // Playwright serializes the evaluator without its closure. Inline both browser-only
  // functions so the route's geometry and the shared frame come from the same layout.
  const evaluate = new Function('main', 'selectors', `return {
    ...(${measureFrame})(main, selectors),
    ...(${measureRoute})(main),
  };`) as (main: Element, selectors: FrameSelectors) => FrameRead;
  return main.evaluate(evaluate, selectors);
}

/**
 * Section 0's shared checks on the measured passes. C1 to C4 are judged at scale 6;
 * C5 at every width and scale. A route decides which of them its control must fail.
 */
export function sharedChecks(entries: (FramePass & FrameRead)[]) {
  const base = entries.filter(e => e.scale === 6);
  return {
    C1: base.every(e => e.edges.every(pair => pair.every(edge => edge === gutter(e.width))) &&
      e.offset === (e.width < 768 ? 16 : 24)),
    C2: base.every(e => e.radii.every(radius => [8,12,999].includes(radius))),
    C3: base.every(e => e.sizes.every(size => [12,14,16,18,20,24].includes(size)) &&
      e.weights.every(weight => ['400','500','600'].includes(weight)) && e.title === Math.max(...e.sizes)),
    C4: base.every(e => e.effects.length === 0),
    C5: entries.every(e => e.overflow <= 0),
  };
}

/** The run's stable report. Two runs of one head must write the same bytes. */
export function writeMetrics(run: string, entries: unknown[]) {
  fs.writeFileSync(path.join(run, 'metrics.json'), JSON.stringify(entries, null, 2) + '\n');
}

/** Every stylesheet the source scans read: `static/css/*.css` without the tokens and minified files. */
export function readStylesheets(source: string) {
  const cssDir = path.join(source, 'static', 'css');
  return fs.readdirSync(cssDir)
    .filter(name => name.endsWith('.css') && name !== 'tokens.css' && !name.endsWith('.min.css'))
    .map(name => ({ name, css: postcss.parse(fs.readFileSync(path.join(cssDir, name), 'utf8')) }));
}

/** C8: outside `tokens.css`, no `[data-theme` selector names a `ui-` class. */
export function expectNoThemedUiSelectors(sheets: ReturnType<typeof readStylesheets>) {
  for (const { css } of sheets) {
    css.walkRules(rule => {
      if (rule.selector.includes('[data-theme')) expect.soft(rule.selector).not.toMatch(/\.ui-[\w-]+/);
    });
  }
}
