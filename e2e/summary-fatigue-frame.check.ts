import { test, expect } from './strict-fixtures';
import type { Page } from '@playwright/test';
import path from 'node:path';
import fs from 'node:fs';
import postcss from 'postcss';
import * as sass from 'sass';
import { expectFrameRun, installFrameSettings, openFramePass, fontsLoaded, readFrame, sharedChecks,
  writeMetrics, THEMES, readStylesheets, expectNoThemedUiSelectors } from './frame-check';
import type { FramePass, FrameRead } from './frame-check';
import { expectedRecords, inspectRecords, lastColumnsReachable, summaryData, summaryResponse } from './summary-records';
import { compareFatiguePeriods } from './fatigue-period-readings';

const key = process.env.FRAME_ROUTE!;
const fatigue = key === 'fatigue';
const weekly = key === 'weekly_summary';
const url = '/' + key;
const titles: Record<string,string> = {weekly_summary: 'Plan Volume Summary', session_summary: 'Session Summary', fatigue: 'Fatigue meter'};
const panelCount = fatigue ? 3 : weekly ? 5 : 4;

// The CSS surfaces in the common frame and the corresponding panels on the control.
// Identical elements matching more than one selector count once.
const selectors = {
  header: '.ui-page-header, .page-header, .fatigue-page__header',
  panels: fatigue ? '.ui-panel, [data-testid="fatigue-sfr-row"], [data-heatmap-panel], [data-testid="fatigue-bars"]' :
    '.ui-panel, .fatigue-badge, .summary-section',
};

function measureGroup(main: Element) {
  const readouts = [...main.querySelectorAll('.fatigue-badge__score, [data-testid$="-value"][data-testid^="fatigue-sfr"]')];
  const title = main.querySelector('h1')!;
  const icons = [...main.querySelectorAll('i.fa, i.fas, i.far, i.fa-solid')].filter(i => i.getBoundingClientRect().width > 0);
  const info = main.querySelector('.fatigue-badge__info-btn')?.getBoundingClientRect();
  const box = main.getBoundingClientRect();
  return {
    readouts: readouts.map(el => ({size: getComputedStyle(el).fontSize, value: el.textContent!.trim()})),
    titleText: title.textContent!.trim(),
    titleVisible: title.getBoundingClientRect().height > 0,
    infoTarget: info ? [info.width, info.height] : [],
    icons: icons.map(i => {
      const s = getComputedStyle(i, '::before');
      return s.fontFamily.includes('Font Awesome') && !['""',"''",'none','normal',''].includes(s.content) &&
        document.fonts.check(s.fontWeight + ' ' + s.fontSize + ' ' + s.fontFamily, s.content.slice(1,-1));
    }),
    frame: [box.left, box.width, document.documentElement.clientWidth - box.right],
  };
}

async function phoneFocus(page: Page) {
  const controls = page.locator('#main-content').locator('a[href]:visible, button:visible, select:visible, summary:visible')
    .filter({ visible: true });
  const count = await controls.count();
  const results = [];
  for (const control of [controls.first(), controls.last()]) {
    await control.focus();
    await control.scrollIntoViewIfNeeded();
    results.push(await control.evaluate(el => {
      const r = el.getBoundingClientRect();
      return document.activeElement === el && (el as HTMLElement).tabIndex >= 0 && r.width > 0 && r.height > 0 && r.left >= 0 &&
        r.right <= document.documentElement.clientWidth + 1 &&
        r.top >= document.querySelector('#navbar')!.getBoundingClientRect().bottom - 1 && r.bottom <= innerHeight + 1;
    }));
  }
  return count >= 2 && results.every(Boolean);
}

function checkFatigueCss(source: string) {
  // Expand nesting in the authored partial too, so a stale bundle cannot mask
  // a new themed .ui-* selector (and an up-to-date partial cannot mask stale output).
  const partial = sass.compile(path.join(source, 'scss', '_fatigue.scss')).css;
  const compiled = fs.readFileSync(path.join(source, 'static/css/bootstrap.custom.min.css'), 'utf8');
  for (const content of [partial, compiled]) {
    const root = postcss.parse(content);
    const darkFatigue: string[] = [], violations: string[] = [];
    root.walkRules(rule => {
      for (const selector of rule.selectors) {
        if (!selector.includes('[data-theme')) continue;
        if (selector.includes('.fatigue-')) darkFatigue.push(selector);
        if (/\.ui-[\w-]+/.test(selector)) violations.push(selector);
      }
    });
    expect(darkFatigue.length).toBeGreaterThan(0);
    expect(violations).toEqual([]);
  }
}

test('ordinary populated Summary and Fatigue frame, typography and field geometry', async ({page, baseURL}) => {
  const run = await expectFrameRun(page, baseURL);
  await installFrameSettings(page);
  const entries: (FramePass & FrameRead & ReturnType<typeof measureGroup>)[] = [];
  const checks: {name: string; passed: boolean}[] = [];
  const audits: unknown[] = [];
  const modes = ['total','direct'] as const;
  const record = (name: string, passed: boolean) => checks.push({name, passed});
  const widths = [320, 360, 375, 390, 767, 768, 1440, 2160];
  for (const width of widths) {
    const scales = width < 375 ? [8] : [390,768,1440].includes(width) ? [6,8] : [6];
    for (const scale of scales) for (const theme of THEMES) {
      const pass = {width, scale, theme};
      const label = [width,scale,theme].join('/');
      const received = fatigue ? undefined : summaryResponse(page, url, 'total');
      const documentResponse = page.waitForResponse(r => r.request().isNavigationRequest() && new URL(r.url()).pathname === url);
      await openFramePass(page, run.baseURL, url, pass);
      await fontsLoaded(page);
      let openingFrame: (FrameRead & ReturnType<typeof measureGroup>) | undefined;
      if (fatigue) {
        await expect(page.getByTestId('fatigue-page')).toHaveAttribute('data-heatmap-state', 'ready');
        await expect(page.locator('[data-heatmap-figure] svg')).toHaveCount(2);
        await expect(page.getByTestId('fatigue-muscle-bar').first()).toBeVisible();
        await expect(page.getByText(/descriptive only/i)).toBeVisible();
      } else {
        const html = await (await documentResponse).text();
        expect(await page.evaluate(markup => {
          const doc = new DOMParser().parseFromString(markup, 'text/html');
          return [...doc.querySelectorAll('tbody tr')].some(tr => tr.textContent?.includes('lateral-head-triceps') &&
            tr.textContent.includes('1800'));
        }, html), 'isolated records are present in the actual HTML response').toBe(true);
        if (weekly) await expect(page.locator('#pattern-coverage-container')).toContainText(/vertical pull/i);
        const volume = page.locator(weekly ? '#weekly-summary-table' : '#session-summary-table');
        const cats = page.locator('#categories-table-body');
        const selector = page.getByLabel('Muscle Contribution Mode', {exact:true});
        const inspect = scale === 6 && [375,390,767,768,1440].includes(width);
        let response = await received!;
        for (const mode of modes) {
          if (mode === 'direct') {
            if (!inspect) break;
            const previous = await cats.locator('tr').first().elementHandle();
            const refresh = summaryResponse(page, url, mode);
            await selector.selectOption(mode);
            response = await refresh;
            await expect.poll(() => previous!.evaluate(el => el.isConnected)).toBe(false);
          }
          const data = await summaryData(response);
          const samples = expectedRecords(data, weekly);
          await expect(volume.locator('tr').filter({hasText:'Biceps'})).toContainText(
            samples[0].fields.find(f => f.name === 'Total Volume')!.value);
          await expect(cats).toContainText('Compound');
          if (mode === 'total') openingFrame = await readFrame(page, selectors, measureGroup);
          if (inspect) {
            const records = await inspectRecords(page, samples, width);
            audits.push({label, mode, records});
            for (const sample of records) record([label, mode, sample.identity, ...sample.errors].join(' '), !sample.errors.length);
            if (width >= 768 && theme === 'light' && mode === 'direct') {
              const failures = await lastColumnsReachable(page,samples);
              record(label + ' last columns ' + failures.join(', '),!failures.length);
            }
          }
        }
      }
      await page.evaluate(() => window.scrollTo({top:0,left:0,behavior:'instant'}));
      await expect(page.locator('#navbar')).not.toHaveClass(/\bnb-compact\b/);
      const read = openingFrame ?? await readFrame(page, selectors, measureGroup);
      entries.push({...pass, ...read});
      record(label + ' expected header and panels', read.edges.length === panelCount + 1);
      record(label + ' title and icons', read.titleText === titles[key] && read.titleVisible && read.icons.every(Boolean));
      if (scale === 6) record(label + ' title and readouts', read.title === 24 &&
        read.readouts.length === (fatigue ? 2 : 1) && read.readouts.every(r => r.size === '24px' && /^\d+(\.\d+)?$/.test(r.value)));
      if (width === 2160) record(label + ' centered 1800px cap', read.frame[1] === 1800 &&
        read.frame[0] === read.frame[2] && read.edges.every(pair => pair.every(n => n === 212)));
      if (width < 768 && !fatigue) record(label + ' 44px help target', read.infoTarget.length === 2 && read.infoTarget.every(n => n >= 44));
      if (width <= 390 && scale === 8) record(label + ' first and last focus', await phoneFocus(page));
    }
  }
  const common = sharedChecks(entries.filter(e => e.width !== 2160));
  writeMetrics(run.run, [...entries, {common,checks,audits}]);
  expectNoThemedUiSelectors(readStylesheets(run.source));
  if (fatigue) checkFatigueCss(run.source);
  if (run.control) {
    expect(common.C1, 'Navigation control still uses the legacy frame').toBe(false);
    if (!fatigue) for (const mode of modes) {
      expect(checks.some(c => !c.passed && c.name.startsWith('767/6/light ' + mode + ' Compound') &&
        c.name.includes('unpainted card label')), 'missing mobile category labels').toBe(true);
      expect(checks.some(c => !c.passed && c.name.startsWith('768/6/light ' + mode + ' Biceps') &&
        c.name.includes('Raw Sets: heading mismatch')), 'tablet raw sets under incorrect heading').toBe(true);
    }
  } else {
    for (const [name,result] of Object.entries(common)) expect.soft(result, name).toBe(true);
    expect(checks.filter(c => !c.passed).map(c => c.name)).toEqual([]);
  }
});

if (fatigue) test('dated period readings, meter reference and anatomical paints match the Navigation control', async ({page,baseURL}) => {
  const run = await expectFrameRun(page, baseURL);
  await installFrameSettings(page);
  await compareFatiguePeriods(page, run.baseURL);
});
