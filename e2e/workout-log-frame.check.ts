import type { Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import postcss from 'postcss';
import AxeBuilder from '@axe-core/playwright';
import { expect, test } from './strict-fixtures';

async function exercisePilot(page: Page, fixture: Record<string, unknown>[]) {
  const row = (name: string) => page.locator('tr[data-log-id]').filter({
    has: page.getByText(name, { exact: true }),
  });
  const names = fixture.map(record => String(record.exercise));
  const rows = page.locator('tr[data-log-id] .exercise-name');
  await page.setViewportSize({width: 1440, height: 900});
  await page.goto('/workout_log');
  for (const key of ['click', 'press'] as const) {
    await page.reload();
    for (const [field, direction] of [['scored_weight','ascending'], ['exercise','ascending'], ['exercise','descending']]) {
      const sort = page.locator(`[data-sort-field="${field}"]`);
      if (key === 'click') await sort.click();
      else await sort.press('Enter');
      await expect(sort.locator('..')).toHaveAttribute('aria-sort', direction);
      const sorted = await rows.allTextContents();
      if (field === 'exercise') expect(sorted).toEqual(direction === 'ascending' ? names : [...names].reverse());
      else expect(sorted.filter(name => fixture.find(record => record.exercise === name)?.scored_weight != null))
        .toEqual(['Barbell Curl','Barbell Bench Press','Barbell Bent Over Row','Barbell Squat','Barbell Deadlift']);
    }
  }
  await page.setViewportSize({width: 390, height: 844});
  for (const record of fixture) {
    const card = row(String(record.exercise));
    await expect(card).toHaveAttribute('data-log-id', String(record.id));
    const status = (await (await page.request.get(`/check_progression/${record.id}`)).json()).data.status;
    await expect(card.locator('.badge.ui-badge')).toHaveText(status);
    const details = card.getByRole('button', {name: 'Details', exact: true});
    await expect(details).toHaveAttribute('aria-expanded','false');
    const rpe = card.locator('[data-field="scored_rpe"] .log-trigger');
    await expect(rpe).toHaveCount(1);
    await expect(rpe).toBeVisible({visible: record.scored_rpe != null || record.planned_rpe != null});
    await expect(card.locator('[data-field="scored_rir"] .log-trigger')).toBeVisible();
    await details.press('Enter');
    await expect(rpe).toBeVisible();
    await expect(card.getByRole('button', {name: /reference video/i})).toBeVisible();
    await expect(card.getByRole('button', {name: /Delete Entry/})).toBeVisible();
    await details.press('Space');
    await expect(card.getByRole('button', {name: /Delete Entry/})).toBeHidden();
  }
  async function enter(name: string, field: string, value: string) {
    const card = row(name), cell = card.locator(`[data-field="${field}"]`);
    const id = await card.getAttribute('data-log-id');
    await cell.locator('.log-trigger').click();
    const input = cell.locator('input');
    await input.fill(value);
    const saved = page.waitForResponse(response => response.url().endsWith('/update_workout_log') &&
      response.request().method() === 'POST' && String(response.request().postDataJSON().id) === id);
    await input.press('Enter');
    expect((await saved).ok()).toBe(true);
    await expect(cell.locator('.editable-text')).toHaveText(value);
    const stored = (await (await page.request.get('/get_workout_logs')).json()).data as Record<string,unknown>[];
    expect(stored.find(record => String(record.id) === id)?.[field]).toBe(Number(value));
    return id;
  }
  await enter('Barbell Seated Military Press', 'scored_rpe', '9');
  await page.reload();
  await expect(row('Barbell Seated Military Press').locator('[data-field="scored_rpe"] .editable-text')).toHaveText(/^9(?:\.0)?$/);
  await enter('Barbell Deadlift', 'scored_rir', '2');
  await expect(row('Barbell Deadlift').locator('.ui-badge')).toHaveText('Pending');
  const deadlift = await enter('Barbell Deadlift', 'scored_rir', '0');
  await page.reload();
  await expect(row('Barbell Deadlift').locator('[data-field="scored_rir"] .log-improved')).toBeVisible();
  await expect(row('Barbell Deadlift').locator('.ui-badge')).toHaveText(
    (await (await page.request.get(`/check_progression/${deadlift}`)).json()).data.status);
  const cable = names.find(name => name.startsWith('Cable '))!;
  const id = await enter(cable, 'scored_rir', '1');
  await page.goto('/workout_plan');
  await expect(page.locator('#workout_plan_table_body')).toBeAttached();
  await page.goto('/workout_log');
  await expect(row(cable)).toHaveAttribute('data-log-id', id!);
  await expect(row(cable).locator('[data-field="scored_rir"] .editable-text')).toHaveText('1');
  await expect(row(cable).locator('.ui-badge')).toHaveText('Achieved');
}

// Run with e2e/scripts/run_workout_log_frame.py. The launcher owns the scratch server.
async function measure(page: Page, control: boolean) {
  return page.locator('#main-content').evaluate((main, legacy) => {
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
    const header = main.querySelector(legacy ? '.page-header' : '.ui-page-header')!;
    const frames = [header, ...main.querySelectorAll(legacy
      ? '.workout-log-controls-frame, .workout-log-frame, #workout-log-table'
      : '.ui-panel, #workout-log-table')].filter(visible);
    const edges = frames.map(node => {
      const box = node.getBoundingClientRect();
      return [round(box.left), round(document.documentElement.clientWidth - box.right)];
    });
    const rows = Array.from(main.querySelectorAll('tr[data-log-id]'));
    const heads = Array.from(main.querySelectorAll<HTMLElement>('th')).filter(visible);
    const exercise = main.querySelector('td[data-label="Exercise"]');
    const cards = rows.map(row => {
      const name = row.querySelector<HTMLElement>('.exercise-name')!;
      const range = document.createRange();
      range.selectNodeContents(name);
      const rects = Array.from(range.getClientRects());
      const box = name.getBoundingClientRect();
      const fields = Array.from(row.querySelectorAll('.log-trigger')).filter(visible);
      return {
        lines: new Set(rects.map(rect => round(rect.top))).size,
        fullName: rects.every(rect => rect.left >= box.left - 1 && rect.right <= box.right + 1 &&
          rect.bottom <= box.bottom + 1) && getComputedStyle(name).textOverflow !== 'ellipsis',
        height: round(row.getBoundingClientRect().height),
        fieldSizes: fields.map(field => [round(field.getBoundingClientRect().width), round(field.getBoundingClientRect().height)]),
      };
    });
    return {
      edges, radii: [...radii].sort((a,b) => a-b), sizes: [...sizes].sort((a,b) => a-b),
      weights: [...weights].sort(), effects: [...effects].sort(),
      title: round(parseFloat(getComputedStyle(title).fontSize)),
      offset: round(header.getBoundingClientRect().top - document.querySelector('#navbar')!.getBoundingClientRect().bottom),
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      headings: heads.length, clipped: heads.filter(h => h.scrollWidth > h.clientWidth).map(h => h.innerText),
      columns: new Set(rows.map(row => round(row.getBoundingClientRect().left))).size,
      exerciseWidth: exercise && round(exercise.getBoundingClientRect().width),
      firstHeight: rows.length ? round(rows[0].getBoundingClientRect().height) : null,
      groups: heads.filter(h => h.getAttribute('scope') === 'colgroup').map(h => h.innerText.trim()), cards,
    };
  }, control);
}

test('measure the Workout Log on its own seeded server', async ({page, baseURL}) => {
  const run = process.env.FRAME_RUN;
  if (!run || !baseURL) throw new Error('Start the fixture with run_workout_log_frame.py');
  const control = !!process.env.FRAME_CONTROL;
  const identity = await page.request.get('/__frame_identity');
  expect(await identity.json()).toEqual({
    database: path.join(run, 'database.db'), runtime: path.join(run, 'runtime'), source: process.env.FRAME_SOURCE,
  });
  const fixture = JSON.parse(fs.readFileSync(path.join(run, 'fixture.json'), 'utf8')) as Record<string, unknown>[];
  const read = async () => (await (await page.request.get('/get_workout_logs')).json()).data;
  expect(await read()).toHaveLength(7);
  expect(await read()).toEqual(expect.arrayContaining(fixture.map(row => expect.objectContaining(row))));
  const entries = [];
  await page.addInitScript(() => {
    const dark = document.cookie.split('; ').includes('frame-theme=dark');
    localStorage.setItem('darkMode', String(dark));
    const scale = document.cookie.match(/ui-scale-level=(\d)/);
    localStorage.setItem('ui-scale-level', scale![1]);
  });
  for (const populated of [true, false]) {
    if (!populated) {
      if (!control) {
        await page.context().addCookies([{name:'ui-scale-level',value:'6',url:baseURL}]);
        await exercisePilot(page, fixture);
      }
      expect((await page.request.post('/clear_workout_log')).ok()).toBe(true);
      expect(await read()).toEqual([]);
    }
    for (const scale of [6, 8]) {
      const widths = scale === 8 ? [390, 1440] : populated ? [390, 768, 1359, 1360, 1440] : [390, 768, 1440];
      for (const width of widths) {
        for (const theme of ['light', 'dark']) {
          if ((width === 1359 || width === 1360) && theme === 'dark') continue;
          await page.setViewportSize({width, height: width === 390 ? 844 : width === 768 ? 1024 : 900});
          await page.context().addCookies([
            {name: 'frame-theme', value: theme, url: baseURL},
            {name: 'ui-scale-level', value: String(scale), url: baseURL},
          ]);
          await page.goto('/workout_log');
          await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
          await expect(page.locator('html')).toHaveAttribute('data-scale', String(scale));
          expect(await page.locator('html').evaluate(el => Number(getComputedStyle(el).zoom))).toBe(scale === 6 ? 1 : 1.2);
          await expect(page.locator('tr[data-log-id]')).toHaveCount(populated ? 7 : 0);
          await page.evaluate(() => document.fonts.ready.then(() => undefined));
          await page.screenshot({path: path.join(run, `${populated ? 'populated' : 'empty'}-${width}-${theme}-scale${scale}.png`)});
          await page.addStyleTag({content: '*,*::before,*::after { transition: none !important; animation: none !important; }'});
          entries.push({populated, scale, width, theme, ...await measure(page, control)});
          if (!control && scale === 6) {
            const expected = populated ? [] : ['import-from-plan-btn'];
            expect(await page.locator('#main-content .ui-btn--primary:visible').evaluateAll(buttons => buttons.map(b => b.id))).toEqual(expected);
            expect(await page.locator('#main-content button:visible').evaluateAll((buttons, fill) =>
              buttons.filter(b => getComputedStyle(b).backgroundColor === fill).map(b => b.id),
              theme === 'dark' ? 'rgb(82, 100, 173)' : 'rgb(66, 99, 235)')).toEqual(expected);
            if (populated && (width === 390 || width === 1440)) {
              const audit = async () => {
                const results = await new AxeBuilder({page}).include('#main-content')
                  .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
                expect.soft(results.violations.map(v => [v.id, v.nodes.map(n => n.target)]),
                  `accessibility at ${width} in ${theme}`).toEqual([]);
              };
              await audit();
              const first = page.locator('tr[data-log-id]').first();
              if (width === 390) {
                await first.locator('.log-details').click();
                await audit();
              }
              await first.locator('[data-field="scored_rir"] .log-trigger').click();
              await audit();
              await first.locator('[data-field="scored_rir"] input').press('Escape');
            }
          }
        }
      }
    }
  }
  fs.writeFileSync(path.join(run, 'metrics.json'), JSON.stringify(entries, null, 2) + '\n');
  const base = entries.filter(e => e.scale === 6);
  const gutter = (width: number) => width < 768 ? 16 : width < 1360 ? 24 : 32;
  const checks = {
    C1: base.every(e => e.edges.every(pair => pair.every(edge => edge === gutter(e.width))) &&
      e.offset === (e.width < 768 ? 16 : 24)),
    C2: base.every(e => e.radii.every(radius => [8,12,999].includes(radius))),
    C3: base.every(e => e.sizes.every(size => [12,14,16,18,20,24].includes(size)) &&
      e.weights.every(weight => ['400','500','600'].includes(weight)) && e.title === Math.max(...e.sizes)),
    C4: base.every(e => e.effects.length === 0),
    C10: base.filter(e => e.width === 1359 || e.width === 1360).every(e =>
      e.overflow <= 0 && (e.width === 1359 ? e.columns === 2 && e.headings === 0 :
        e.groups.join('/') === 'Planned/Logged' && e.clipped.length === 0 && Number(e.exerciseWidth) >= 220)),
  };
  for (const [criterion, passed] of Object.entries(checks)) expect.soft(passed, criterion).toBe(!control);
  if (!control) {
    for (const entry of entries) {
      expect.soft(entry.overflow, 'C5 page overflow').toBeLessThanOrEqual(0);
      expect.soft(entry.cards.every(card => card.fullName), 'full exercise names').toBe(true);
      if (entry.populated && entry.scale === 6 && entry.width === 390) {
        expect.soft(entry.cards.slice(0, 6).every(card => card.lines <= 2), 'seed names').toBe(true);
        for (const card of entry.cards) {
          if (card.lines === 1) expect.soft(card.height, 'C6 card height').toBeLessThanOrEqual(250);
          expect.soft(card.fieldSizes.every(pair => pair.every(side => side >= 44)), 'C6 field targets').toBe(true);
        }
      }
      if (entry.populated && entry.width === 768) expect.soft(entry.columns).toBe(2);
      if (entry.populated && entry.width === 1440 && entry.scale === 6) {
        expect.soft(entry.clipped).toEqual([]);
        expect.soft(entry.exerciseWidth!).toBeGreaterThanOrEqual(220);
      }
    }
    const cssDir = path.join(process.env.FRAME_SOURCE!, 'static', 'css');
    for (const name of fs.readdirSync(cssDir).filter(name => name.endsWith('.css') && name !== 'tokens.css' && !name.endsWith('.min.css'))) {
      const css = postcss.parse(fs.readFileSync(path.join(cssDir, name), 'utf8'));
      let important = 0;
      css.walkRules(rule => {
        if (rule.selector.includes('[data-theme')) expect.soft(rule.selector).not.toMatch(/\.ui-[\w-]+/);
        if (name === 'pages-workout-log.css' && !rule.selector.includes('#clearLogModal')) {
          expect.soft(rule.selector).not.toMatch(/\.tbl\b|\.frame-header|\.collapsible-frame|\.metric-lane|\.form-control|\.badge\b|\.container-fluid|\.page-header\b/);
          rule.walkDecls(decl => { expect.soft(decl.important).toBeFalsy(); });
        }
      });
      if (name === 'pages-workout-log.css') {
        css.walkDecls(decl => { if (decl.important) important++; });
        expect(important).toBeLessThan(242);
      }
    }
  }
});
