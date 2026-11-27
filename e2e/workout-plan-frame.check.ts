import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { errors, type Page } from '@playwright/test';
import postcss from 'postcss';
import {
  expectFrameRun, expectNoThemedUiSelectors, fontsLoaded, freezeMotion,
  installFrameSettings, openFramePass, readFrame, readStylesheets, sharedChecks, THEMES, writeMetrics,
  type FramePass, type FrameRead,
} from './frame-check';
import { expect, ROUTES, test } from './strict-fixtures';
import {
  DEADLIFT, LONG_EXERCISE, ROUTINE_A, SQUAT, details, editVisualPlanFixture, planPost,
  planRow, planRows, routineTab,
} from './workout-plan-fixture';
import {
  filledPlanActions, filterToggle, moreButton, phonePlanProblems, planTable, planViewToggle,
  setDetails, setPlanView, setSupersetChoice, singleAddAction,
} from './workout-plan-redesign';

const WIDTHS = [320, 360, 390, 768, 1359, 1360, 1440];
const MODES = ['simple', 'advanced'] as const;
type Mode = typeof MODES[number];
const SELECTORS = {
  header: '#workout header:has(h1)',
  panels: '#workout section[aria-labelledby="workout-plan-table-heading"], ' +
    '#workout .ui-panel:has(#add_exercise_btn), #exercise-selection-frame',
};

const SIMPLE = [
  'Select for Superset', '', 'Routine', 'Exercise', 'Primary Muscle', 'Secondary Muscle',
  'Isolated Muscles', 'Sets', 'Min Rep', 'Max Rep', 'RIR', 'RPE', 'Weight', 'Style', 'Grips', 'Actions',
];
const ADVANCED = [
  'Select for Superset', '', 'Routine', 'Exercise', 'Primary Muscle', 'Secondary Muscle',
  'Tertiary Muscle', 'Isolated Muscles', 'Utility', 'Movement Pattern', 'Movement Subpattern',
  'Sets', 'Min Rep', 'Max Rep', 'RIR', 'RPE', 'Weight', 'Style', 'Grips', 'Stabilizers', 'Synergists', 'Actions',
];

/** Uses retained markup on the old page so the control measures real positions and CSS. */
function measurePlan(main: Element) {
  const table = main.querySelector('[data-testid="exercise-table"]') as HTMLTableElement;
  const body = table.tBodies[0];
  const shown = (node: Element) => node.getClientRects().length > 0;
  const headings = [...table.querySelectorAll('thead th')].filter(shown);
  const bodyStyle = getComputedStyle(body);
  const cards = bodyStyle.display === 'grid' ? [...body.querySelectorAll('tr.ui-record-card')].filter(shown) : [];
  const first = cards[0]?.getBoundingClientRect();
  const top = (node: Element | null) => node ? Math.round(node.getBoundingClientRect().top + scrollY) : null;
  const selected = main.querySelector('#routine-tabs [aria-selected="true"]');
  return {
    state: main.querySelector('[data-plan-state]')?.getAttribute('data-plan-state') ?? null,
    selected: selected?.getAttribute('data-routine') ?? null,
    rowCount: body.querySelectorAll('tr[data-exercise-id]').length,
    cardCount: cards.length,
    gridColumns: bodyStyle.gridTemplateColumns.match(/[\d.]+px/g)?.length ?? 0,
    headings: headings.map(node => node.textContent?.trim() ?? ''),
    firstCardTop: first ? Math.round(first.top + scrollY) : null,
    order: [
      top(main.querySelector('header:has(h1)')),
      top(main.querySelector('section[aria-labelledby="workout-plan-table-heading"]')),
      top(main.querySelector('.ui-panel:has(#add_exercise_btn), #exercise-selection-frame')),
    ],
  };
}

/** Capture the complete opening paint without racing the asynchronous plan response. */
async function observeOpeningPaint(page: Page) {
  await page.addInitScript(() => {
    const observations = new Set<string>();
    const changes = { rowBatches: 0, rowAttributes: 0, tabChanges: 0, states: [] as string[] };
    Object.defineProperty(window, 'planOpeningPaint', { value: changes });
    const observer = new MutationObserver(records => {
      const state = document.querySelector('[data-plan-state]')?.getAttribute('data-plan-state');
      if (state && !observations.has(state)) {
        observations.add(state);
        changes.states.push(state);
      }
      if (records.some(record => record.type === 'childList' && record.target instanceof Element &&
          record.target.id === 'workout_plan_table_body' &&
          [...record.addedNodes].some(node => node instanceof Element && node.matches('tr[data-exercise-id]')))) {
        changes.rowBatches++;
      }
      changes.rowAttributes += records.filter(record => record.type === 'attributes' &&
        record.target instanceof Element && record.target.matches('tr[data-exercise-id]')).length;
      changes.tabChanges += records.filter(record => record.attributeName === 'aria-selected' &&
        record.target instanceof Element && !!record.target.closest('#routine-tabs')).length;
    });
    observer.observe(document, {
      subtree: true, childList: true, attributes: true,
      attributeFilter: ['class', 'style', 'aria-selected', 'data-plan-state'],
    });
  });
}

async function readOpeningPaint(page: Page) {
  return page.evaluate(() => {
    const state = (window as unknown as { planOpeningPaint: {
      rowBatches: number; rowAttributes: number; tabChanges: number; states: string[];
    } }).planOpeningPaint;
    return { ...state, states: [...state.states] };
  });
}

/** WP6 reads all closed records in one pass, including their rendered name and actions. */
async function closedCards(page: Page, railIds: (string | null)[]) {
  return planTable(page).evaluate((table, railIds) => {
    const shown = (node: Element | null) => !!node && !!node.getClientRects().length;
    const textLines = (node: Element) => {
      const range = document.createRange();
      range.selectNodeContents(node);
      return new Set([...range.getClientRects()].map(rect => Math.round(rect.top))).size;
    };
    return [...table.querySelectorAll('tr.ui-record-card')].map(card => {
      const name = card.querySelector('.exercise-name')!;
      const nameStyle = getComputedStyle(name);
      const prescription = card.querySelector('[data-label="Exercise"]')?.textContent ?? '';
      return {
        name: name.textContent?.trim() ?? '', lines: textLines(name),
        fullName: nameStyle.textOverflow !== 'ellipsis' && name.scrollWidth <= name.clientWidth + 1,
        height: Math.round(card.getBoundingClientRect().height),
        drag: shown(card.querySelector('.drag-handle')),
        routine: /Workout [AB]/.test(card.textContent ?? ''),
        prescription: /\d+ sets?\s*[×x]\s*\d+.*kg.*RIR/.test(prescription),
        swap: shown(card.querySelector('[data-action="replace"]')),
        video: shown(card.querySelector('[data-action="play-video"]')),
        details: shown(card.querySelector('button[aria-expanded="false"]')),
        hidden: [...card.querySelectorAll(
          '[data-field], .execution-style-cell, .superset-checkbox, button[data-action="delete"], [data-label="Primary Muscle"]',
        )].every(node => !shown(node)),
        pair: !!card.getAttribute('data-superset-group'),
        badge: [...card.querySelectorAll('.superset-badge')].some(node => shown(node) && /Superset/.test(node.textContent ?? '')),
        rail: railIds.includes(card.getAttribute('data-exercise-id')),
      };
    });
  }, railIds);
}

/** WP7 scrolls the focused named region and verifies each row's last action at the end. */
async function tableRegion(page: Page) {
  const region = page.locator('[role="region"]').filter({ has: planTable(page) });
  const before = await region.evaluate(element => {
    element.scrollLeft = 0;
    const headings = [...element.querySelectorAll('th')].filter(node => node.getClientRects().length);
    return {
      ready: element.getAttribute('tabindex') === '0' &&
        !!(element.getAttribute('aria-label') || element.getAttribute('aria-labelledby')),
      overflow: element.scrollWidth - element.clientWidth,
      clippedHeadings: headings.filter(node => node.scrollWidth > node.clientWidth)
        .map(node => node.textContent?.trim()),
      exerciseWidth: headings.find(node => node.textContent?.trim() === 'Exercise')?.getBoundingClientRect().width ?? 0,
    };
  });
  let keyboard = before.overflow <= 0;
  if (before.ready && before.overflow > 0) {
    await region.focus();
    await page.keyboard.press('ArrowRight');
    try {
      await page.waitForFunction(node => !!node && node.scrollLeft > 0, await region.elementHandle(), { timeout: 1500 });
      keyboard = true;
    } catch (error) {
      if (!(error instanceof errors.TimeoutError)) throw error;
    }
  }
  const remove = await region.evaluate(element => {
    const controls = [...element.querySelectorAll('tbody [data-label="Actions"] button')];
    return controls.map(button => {
      button.scrollIntoView({ block: 'center', inline: 'nearest', behavior: 'instant' });
      element.scrollLeft = element.scrollWidth;
      const outer = element.getBoundingClientRect(), box = button.getBoundingClientRect();
      const hit = document.elementFromPoint(box.left + box.width / 2, box.top + box.height / 2);
      return box.width > 0 && box.left >= outer.left - 0.5 && box.right <= outer.right + 0.5 &&
        !!hit && button.contains(hit);
    });
  });
  return { ...before, keyboard, remove };
}

async function measureMenu(page: Page) {
  const button = moreButton(page);
  if (!(await button.isVisible())) return { visible: false, problems: ['More menu is absent'] };
  await button.click();
  const menu = page.getByRole('menu').filter({ has: page.getByRole('menuitem', { name: /Clear Plan/ }) });
  await expect(menu).toBeVisible();
  const problems = await menu.evaluate(element => {
    const style = getComputedStyle(element);
    const { left, right, width } = element.getBoundingClientRect();
    const probe = document.createElement('span');
    probe.style.cssText = 'display:none;background-color:var(--surface-2);box-shadow:var(--shadow-elev-2)';
    element.append(probe);
    const tokens = getComputedStyle(probe);
    const matchesSurface = style.backgroundColor === tokens.backgroundColor && style.boxShadow === tokens.boxShadow;
    probe.remove();
    return [
      left < -0.5 || right > innerWidth + 0.5 ? 'popover leaves the viewport' : '',
      width < 199.5 ? 'popover is narrower than 200 px' : '',
      !matchesSurface || style.borderTopLeftRadius !== '12px' ? 'popover surface, shadow or radius' : '',
      innerWidth < 768 && [...element.querySelectorAll('[role="menuitem"]')].some(
        item => item.getBoundingClientRect().height < 43.5,
      ) ? 'a mobile menu item is under 44 px' : '',
    ].filter(Boolean);
  });
  await page.keyboard.press('Escape');
  await expect(menu).toBeHidden();
  return { visible: true, problems };
}

function supersetAppearance(page: Page) {
  return page.locator('#workout').evaluate(workout => {
    const styleNames = ['background-color', 'border-left-color', 'color'];
    const probe = document.createElement('span');
    probe.style.display = 'none';
    workout.append(probe);
    const legacy = new Set<string>();
    for (const index of [1, 2, 3, 4]) {
      const token = '--superset-color-' + index;
      if (getComputedStyle(workout).getPropertyValue(token).trim()) {
        probe.style.color = 'var(' + token + ')';
        legacy.add(getComputedStyle(probe).color);
      }
    }
    probe.style.color = 'var(--ink-2)';
    const railColor = getComputedStyle(probe).color;
    probe.remove();
    const withOldColor: string[] = [];
    for (const node of workout.querySelectorAll('tr[data-superset-group], tr[data-superset-group] *')) {
      for (const pseudo of [null, '::before', '::after']) {
        const style = getComputedStyle(node, pseudo);
        if (styleNames.some(property => legacy.has(style.getPropertyValue(property)))) {
          withOldColor.push(node.tagName + (pseudo ?? ''));
          break;
        }
      }
    }
    const isVisible = (style: CSSStyleDeclaration) =>
      style.display !== 'none' && style.visibility === 'visible' && Number(style.opacity) > 0;
    const hasRail = (host: Element) => {
      const box = host.getBoundingClientRect();
      const base = getComputedStyle(host);
      if (box.width === 0 || box.height === 0 || !isVisible(base)) return false;
      const borderWidth = parseFloat(base.borderLeftWidth);
      if (borderWidth > 1 && base.borderLeftStyle !== 'none' && base.borderLeftColor === railColor) return true;
      return ['::before', '::after'].some(pseudo => {
        const style = getComputedStyle(host, pseudo);
        const width = parseFloat(style.width);
        return isVisible(style) && style.content !== 'none' && style.content !== 'normal' &&
          style.position === 'absolute' && parseFloat(style.left) === 0 &&
          width > Math.max(1, borderWidth) && parseFloat(style.height) > width && style.backgroundColor === railColor;
      });
    };
    const appearances = [...workout.querySelectorAll('#workout_plan_table_body tr')].map(row => {
      const badge = row.querySelector('.superset-badge');
      const firstCell = row.querySelector('td:first-child');
      return {
        id: row.getAttribute('data-exercise-id'),
        paired: row.hasAttribute('data-superset-group'),
        rail: hasRail(row) || (!!firstCell && hasRail(firstCell)),
        badge: badge?.textContent?.trim(),
        shown: !!badge?.getClientRects().length,
      };
    });
    return {
      pairs: appearances.filter(row => row.paired),
      unpaired: appearances.filter(row => !row.paired),
      withOldColor,
    };
  });
}

const CONTROL = '8b023d1a';
function controlCSS(filename: string) {
  const root = path.join(__dirname, '..');
  const name = 'static/css/' + filename;
  const entry = execFileSync('git', ['ls-tree', CONTROL, '--', name], { cwd: root, encoding: 'utf8' }).trim();
  const [metadata, pathname, extra] = entry.split('\t');
  const oid = /^100644 blob ([0-9a-f]{40})$/.exec(metadata)?.[1];
  if (!oid || pathname !== name || extra) throw new Error('Expected one control CSS blob for ' + name);
  return execFileSync('git', ['cat-file', 'blob', oid], { cwd: root, encoding: 'utf8' });
}

function sourceChecks(source: string) {
  const css = path.join(source, 'static', 'css');
  const plan = fs.readFileSync(path.join(css, 'pages-workout-plan.css'), 'utf8');
  const log = fs.readFileSync(path.join(css, 'pages-workout-log.css'), 'utf8');
  const deletedSelectors: string[] = [];
  postcss.parse(plan).walkRules(rule => {
    if (/\.frame-calm-glass\b|\.collapsible-frame\b|\.collapse-toggle\b|\.btn-calm-[\w-]+|\.input-calm-inset\b|\.table-calm\b|\.tbl-wrap--full\b|\.routine-tab(?:-btn)?\b|#clear-filters-btn\b/.test(rule.selector)) {
      deletedSelectors.push(rule.selector.trim());
    }
  });
  const important = plan.split('\n').filter(line => /!important\b/.test(line)).length;
  const sharedGroups = (text: string) => {
    const rules: string[] = [];
    postcss.parse(text.replace(/\r\n/g, '\n')).walkRules(rule => {
      if (/:is\([^)]*workout-plan[^)]*(?:workout-log-page|summary-frame)|:is\([^)]*(?:workout-log-page|summary-frame)[^)]*workout-plan/.test(rule.selector)) {
        rules.push(rule.toString());
      }
    });
    return rules;
  };
  const sharedGroupsMatch = ['components.css', 'layout.css'].every(filename => {
    const groups = sharedGroups(fs.readFileSync(path.join(css, filename), 'utf8'));
    const baseline = sharedGroups(controlCSS(filename));
    return baseline.length > 0 && JSON.stringify(groups) === JSON.stringify(baseline);
  });
  return { deletedSelectors, important, clearLogRules: log.includes('#clearLogModal'),
    logImportant: /!important\b/.test(log), sharedGroupsMatch };
}

test('measure the Workout Plan on its own seeded server', async ({ page, baseURL }) => {
  test.setTimeout(360_000);
  const frame = await expectFrameRun(page, baseURL);
  const rows = await editVisualPlanFixture(page.request);
  const openingIds = rows.filter(row => row.routine === ROUTINE_A).map(row => row.id);
  const squat = rows.find(row => row.exercise === SQUAT)!;
  const deadlift = rows.find(row => row.exercise === DEADLIFT)!;
  await installFrameSettings(page);
  await observeOpeningPaint(page);

  const entries: (FramePass & FrameRead & ReturnType<typeof measurePlan> & {
    populated: boolean; tab: string; mode: Mode;
  })[] = [];
  const audits: unknown[] = [];
  const checks: { name: string; pass: boolean }[] = [];
  const record = (name: string, pass: boolean) => checks.push({ name, pass });

  for (const populated of [true, false]) {
    if (!populated) await planPost(page.request, '/clear_workout_plan');
    for (const width of populated ? WIDTHS : [390, 768, 1440]) {
      for (const scale of populated ? [6, 8] : [6]) {
        for (const theme of THEMES) {
          if ([1359, 1360].includes(width) && theme === 'dark' && scale === 6) continue;
          const pass = { width, scale, theme };
          const label = [populated ? 'populated' : 'empty', width, scale, theme].join('/');
          const response = page.waitForResponse(result => new URL(result.url()).pathname === '/get_workout_plan');
          await openFramePass(page, frame.baseURL, ROUTES.WORKOUT_PLAN, pass);
          expect((await response).status()).toBe(200);
          await expect(page.locator('#tab-all .tab-count')).toHaveText(String(populated ? rows.length : 0));
          await fontsLoaded(page);
          await freezeMotion(page);
          if (populated) await expect(planRows(page).first()).toBeVisible();
          const initial = await page.locator('#routine-tabs [aria-selected="true"]').getAttribute('data-routine');
          record(label + ' opening tab', initial === (populated ? ROUTINE_A : 'all'));
          if (populated && ((width === 320 && scale === 8) || (width === 1440 && scale === 6))) {
            const paint = await readOpeningPaint(page);
            audits.push({ label, paint });
            record(label + ' opening paint', paint.states.join('/') === 'loading/populated' &&
              paint.rowBatches === 1 && paint.rowAttributes === 0 && paint.tabChanges === 0);
          }
          const actions = await filledPlanActions(page);
          audits.push({ label, actions });
          record(label + ' one filled primary', JSON.stringify(actions) === JSON.stringify(singleAddAction));
          const supersets = populated ? await supersetAppearance(page) : null;
          if (supersets) {
            audits.push({ label, supersets });
            record(label + ' neutral rails and badges', supersets.pairs.length === 2 &&
              supersets.pairs.every(row => row.rail && row.shown && row.badge === 'Superset') &&
              supersets.unpaired.length > 0 && supersets.unpaired.every(row => !row.rail && !row.shown) &&
              supersets.withOldColor.length === 0);
          }

          for (const tab of populated && initial !== 'all' ? ['opening', 'all'] : ['opening']) {
            if (tab === 'all') await routineTab(page, 'all').click();
            if (populated) {
              await expect(planRows(page)).toHaveCount(tab === 'opening' && initial === ROUTINE_A ? openingIds.length : rows.length);
            } else {
              await expect(planRows(page)).toHaveCount(0);
            }
            for (const mode of populated ? MODES : ['simple'] as const) {
              if (frame.control) {
                const toggle = planViewToggle(page);
                await expect(toggle).toHaveAttribute('data-view-mode', /^(simple|advanced)$/);
                if (await toggle.getAttribute('data-view-mode') !== mode) {
                  await toggle.evaluate(node => (node as HTMLButtonElement).click());
                }
              } else {
                await setPlanView(page, mode);
              }
              await page.evaluate(() => window.scrollTo({ top: 0, left: 0, behavior: 'instant' }));
              await expect(page.locator('#navbar')).not.toHaveClass(/\bnb-compact\b/);
              const read = await readFrame(page, SELECTORS, measurePlan);
              entries.push({ ...pass, populated, tab, mode, ...read });
              record(label + '/' + tab + '/' + mode + ' panel order',
                read.order.every(top => top !== null) && Number(read.order[0]) < Number(read.order[1]) &&
                Number(read.order[1]) < Number(read.order[2]));
              if (supersets && width === 390 && scale === 6 && mode === 'simple' && tab === 'opening') {
                const rails = [...supersets.pairs, ...supersets.unpaired].filter(row => row.rail).map(row => row.id);
                const cardRead = await closedCards(page, rails);
                audits.push({ label, cardRead });
                const openingCards = cardRead.filter(card => rows.some(row => row.exercise === card.name && row.routine === ROUTINE_A));
                record(label + ' WP6 cards, content, rails and targets',
                  openingCards.length === 7 && read.firstCardTop !== null && read.firstCardTop < 600 &&
                  openingCards.every(card => card.fullName && card.drag && card.routine && card.prescription &&
                    card.swap && card.video && card.details && card.hidden &&
                    (card.pair ? card.rail && card.badge : !card.rail && !card.badge) &&
                    (card.name === LONG_EXERCISE || card.lines <= 2) &&
                    (card.lines !== 1 || card.height <= 200)));
                record(label + ' WP6 fit and targets', (await phonePlanProblems(page)).length === 0);
              }
              if (populated && [1360, 1440].includes(width) && scale === 6) {
                const measured = await tableRegion(page);
                audits.push({ label, tab, mode, table: measured });
                record(label + '/' + tab + '/' + mode + ' WP7 table',
                  measured.ready && measured.keyboard && (mode !== 'advanced' || measured.overflow > 0) &&
                  measured.clippedHeadings.length === 0 && measured.exerciseWidth >= 219.5 &&
                  measured.remove.length === read.rowCount && measured.remove.every(Boolean) &&
                  JSON.stringify(read.headings) === JSON.stringify(mode === 'simple' ? SIMPLE : ADVANCED));
              }
              if (populated && width < 1360 && [768, 1359].includes(width)) {
                record(label + '/' + tab + '/' + mode + ' two-column cards',
                  read.gridColumns === 2 && read.cardCount === read.rowCount && !read.headings.length);
              }
            }
          }
          if (populated && width <= 390 && (scale === 8 || width === 320)) {
            await setPlanView(page, 'simple');
            const states: Record<string, string[]> = { closed: await phonePlanProblems(page) };
            if (await details(page, squat.id).isVisible()) {
              await setDetails(page, squat.id, true);
              states.squat = await phonePlanProblems(page);
              await setSupersetChoice(planRow(page, squat.id), true);
              await expect(page.locator('#superset-actions')).toBeVisible();
              states.selected = await phonePlanProblems(page);
              await setSupersetChoice(planRow(page, squat.id), false);
              await setDetails(page, squat.id, false);
              await setDetails(page, deadlift.id, true);
              states.deadlift = await phonePlanProblems(page);
              await setDetails(page, deadlift.id, false);
            }
            const filters = filterToggle(page);
            if (await filters.isVisible()) {
              await filters.click();
              for (const [key, label] of [['Primary Muscle Group', 'Chest'], ['Equipment', 'Barbell']]) {
                const filtered = page.waitForResponse(result => new URL(result.url()).pathname === '/filter_exercises');
                await page.locator('#filters-form select[data-filter-key="' + key + '"]')
                  .selectOption({ label }, { force: true });
                expect((await filtered).ok()).toBe(true);
              }
              await filters.click();
              await expect(page.locator('.ui-chip').filter({ hasText: /Chest|Barbell/ })).toHaveCount(2);
              states.chips = await phonePlanProblems(page);
            }
            audits.push({ label, states });
            record(label + ' WP11 closed, open, selected and chips', Object.keys(states).length === 5 &&
              Object.values(states).every(problems => problems.length === 0));
          }
          if (populated && ([390, 1440].includes(width) && scale === 6 || width === 320 && scale === 8)) {
            const menu = await measureMenu(page);
            audits.push({ label, menu });
            record(label + ' WP12 menu', menu.visible && menu.problems.length === 0);
          }
        }
      }
    }
  }

  const common = sharedChecks(entries);
  const boundary = entries.filter(entry => entry.populated && entry.theme === 'light' && entry.scale === 6);
  const WP10 = [1359, 1360].every(width => {
    const passes = boundary.filter(entry => entry.width === width);
    return passes.length > 0 && passes.every(entry => entry.overflow <= 0 && (width === 1359 ?
      entry.cardCount === entry.rowCount && entry.gridColumns === 2 && !entry.headings.length :
      entry.cardCount === 0 && entry.headings.length > 0));
  });
  const source = sourceChecks(frame.source);
  writeMetrics(frame.run, [...entries, { common, WP10, source, checks, audits }]);
  expectNoThemedUiSelectors(readStylesheets(frame.source));
  if (frame.control) {
    for (const [criterion, pass] of Object.entries({ ...common, WP10 })) {
      expect.soft(pass, criterion + ' must fail on ' + CONTROL).toBe(false);
    }
  } else {
    for (const [criterion, pass] of Object.entries({ ...common, WP10 })) {
      expect.soft(pass, criterion).toBe(true);
    }
    expect.soft(source.deletedSelectors, 'WP9 legacy selectors').toEqual([]);
    expect.soft(source.important, 'WP9 important declarations').toBeLessThanOrEqual(65);
    expect.soft(source.clearLogRules, 'Clear Log style lives in the shared overlay').toBe(false);
    expect.soft(source.logImportant, 'Workout Log page bundle uses no !important').toBe(false);
    expect.soft(source.sharedGroupsMatch, 'shared :is() rules stay as in ' + CONTROL).toBe(true);
    expect.soft(checks.filter(check => !check.pass).map(check => check.name)).toEqual([]);
  }
});
