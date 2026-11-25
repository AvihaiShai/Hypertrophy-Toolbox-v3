import type { Locator, Page, Request, Response } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import postcss from 'postcss';
import AxeBuilder from '@axe-core/playwright';
import { expect, test } from './strict-fixtures';

type Theme = 'light' | 'dark';
type Box = { left: number; right: number; top: number; bottom: number };
type CardPart = { text: string; box: Box | null };

// Section 0 pins these: the panel surface and the danger text, per theme.
const PANEL_SURFACE: Record<Theme, string> = { light: 'rgb(255, 255, 255)', dark: 'rgb(38, 49, 61)' };
const DANGER_TEXT: Record<Theme, string> = { light: 'rgb(192, 54, 44)', dark: 'rgb(240, 138, 128)' };
// Section 0: the six planned fields and the five logged fields, in heading order.
const PLANNED_HEADINGS = ['Sets', 'Min Reps', 'Max Reps', 'RIR', 'RPE', 'Weight'];
const LOGGED_HEADINGS = ['Min Reps', 'Max Reps', 'RIR', 'RPE', 'Weight'];
const FIELD_KEYS: Record<string, string> = {
  Sets: 'sets', 'Min Reps': 'min_reps', 'Max Reps': 'max_reps', RIR: 'rir', RPE: 'rpe', Weight: 'weight',
};
const GROUPED_FIELDS = [
  ...PLANNED_HEADINGS.map(label => ({ field: `planned_${FIELD_KEYS[label]}`, group: 'Planned', label })),
  ...LOGGED_HEADINGS.map(label => ({ field: `scored_${FIELD_KEYS[label]}`, group: 'Logged', label })),
];
// Section 0: the card's logged fields, in the order the main row shows them.
const CARD_FIELDS = [
  { field: 'scored_min_reps', label: 'Min Reps' },
  { field: 'scored_max_reps', label: 'Max Reps' },
  { field: 'scored_weight', label: 'Weight' },
  { field: 'scored_rir', label: 'RIR' },
  { field: 'scored_rpe', label: 'RPE' },
];

/** A stored number as the page may print it: 60 or 60.0, 12.5 as written. */
function printed(value: unknown): string {
  const text = String(value);
  return Number.isInteger(value) ? `${text}(?:\\.0)?` : text.replace('.', '\\.');
}

/** Criterion 3: on a populated log Import is secondary and Clear Log is the danger variant. */
async function expectPopulatedActionVariants(page: Page, theme: Theme, where: string) {
  const styles = await page.evaluate(() => {
    const token = (name: string) => {
      const probe = document.createElement('span');
      probe.style.color = `var(${name})`;
      document.body.append(probe);
      const colour = getComputedStyle(probe).color;
      probe.remove();
      return colour;
    };
    const read = (id: string) => {
      const button = document.getElementById(id)!;
      const style = getComputedStyle(button);
      const sides = ['Top', 'Right', 'Bottom', 'Left'] as const;
      return {
        classes: Array.from(button.classList),
        text: style.color,
        fill: style.backgroundColor,
        borderWidths: sides.map(side => style[`border${side}Width`]),
        borderStyles: sides.map(side => style[`border${side}Style`]),
        borderColours: sides.map(side => style[`border${side}Color`]),
      };
    };
    return {
      ink1: token('--ink-1'),
      ink3: token('--ink-3'),
      importPlan: read('import-from-plan-btn'),
      clearLog: read('clear-log-btn'),
    };
  });
  const { importPlan, clearLog, ink1, ink3 } = styles;
  const four = (value: string) => [value, value, value, value];
  expect.soft(importPlan.classes, `Import variant class ${where}`).toContain('ui-btn--secondary');
  expect.soft(importPlan.classes, `Import variant class ${where}`).not.toContain('ui-btn--primary');
  expect.soft(importPlan.fill, `Import fill ${where}`).toBe(PANEL_SURFACE[theme]);
  expect.soft(importPlan.text, `Import text ${where}`).toBe(ink1);
  expect.soft(importPlan.borderWidths, `Import border ${where}`).toEqual(four('1px'));
  expect.soft(importPlan.borderStyles, `Import border ${where}`).toEqual(four('solid'));
  expect.soft(importPlan.borderColours, `Import border ${where}`).toEqual(four(ink3));
  expect.soft(clearLog.classes, `Clear Log variant class ${where}`).toContain('ui-btn--danger');
  expect.soft(clearLog.classes, `Clear Log variant class ${where}`).not.toContain('ui-btn--primary');
  expect.soft(clearLog.text, `Clear Log text ${where}`).toBe(DANGER_TEXT[theme]);
  expect.soft(clearLog.fill, `Clear Log fill ${where}`).toBe(PANEL_SURFACE[theme]);
  expect.soft(clearLog.borderWidths, `Clear Log border ${where}`).toEqual(four('1px'));
  expect.soft(clearLog.borderStyles, `Clear Log border ${where}`).toEqual(four('solid'));
}

/** Criterion 8: Planned and Logged sit over their fields, and cells name both headings. */
async function expectDesktopColumnGroups(page: Page, where: string) {
  const table = await page.locator('#workout-log-table').evaluate((node, fields) => {
    const label = (cell: Element) => (cell.textContent ?? '').replace(/\s+/g, ' ').trim();
    const describe = (head: HTMLTableCellElement) => {
      const box = head.getBoundingClientRect();
      return {
        label: label(head),
        group: head.scope === 'colgroup',
        span: head.colSpan,
        left: box.left,
        right: box.right,
      };
    };
    const shown = Array.from(node.querySelectorAll<HTMLTableCellElement>('thead th'))
      .filter(head => head.getClientRects().length > 0);
    const cells = [];
    for (const row of Array.from(node.querySelectorAll('tr[data-log-id]'))) {
      for (const { field } of fields) {
        const cell = row.querySelector(`[data-field="${field}"]`)?.closest('td');
        const box = cell?.getBoundingClientRect();
        const ids = (cell?.getAttribute('headers') ?? '').split(/\s+/).filter(Boolean);
        const named = ids.map(id => {
          const head = document.getElementById(id);
          return head instanceof HTMLTableCellElement && head.tagName === 'TH' ? describe(head) : null;
        });
        cells.push({
          record: row.getAttribute('data-log-id'),
          field,
          left: box ? box.left : null,
          right: box ? box.right : null,
          named,
        });
      }
    }
    return { heads: shown.map(describe), cells };
  }, GROUPED_FIELDS);

  const groups = table.heads.filter(head => head.group);
  const fieldHeads = table.heads.filter(head => !head.group);
  expect.soft(groups.map(head => [head.label, head.span]), `group headings ${where}`)
    .toEqual([['Planned', 6], ['Logged', 5]]);
  expect.soft(fieldHeads.map(head => head.label), `field headings ${where}`).toEqual([
    '#', 'Routine', 'Exercise', ...PLANNED_HEADINGS, ...LOGGED_HEADINGS,
    'Last Progression', 'Progressive Overload', 'Actions',
  ]);
  for (const [name, expected] of [['Planned', PLANNED_HEADINGS], ['Logged', LOGGED_HEADINGS]] as const) {
    const group = groups.find(head => head.label === name);
    const under = group
      ? fieldHeads.filter(head => head.left >= group.left - 1 && head.right <= group.right + 1)
      : [];
    expect.soft(under.map(head => head.label), `fields under ${name} ${where}`).toEqual(expected);
    const covered = under.length > 0 && group !== undefined &&
      Math.abs(under[0].left - group.left) <= 1 &&
      Math.abs(under[under.length - 1].right - group.right) <= 1;
    expect.soft(covered, `${name} spans exactly its fields ${where}`).toBe(true);
  }

  expect.soft(table.cells, `grouped cells ${where}`).toHaveLength(7 * GROUPED_FIELDS.length);
  const unassociated = table.cells.filter(cell => {
    const expected = GROUPED_FIELDS.find(entry => entry.field === cell.field)!;
    const groupNames = cell.named.filter(head => head?.group).map(head => head!.label);
    const own = cell.named.filter(head => head && !head.group);
    const aligned = own.length === 1 && cell.left !== null && cell.right !== null &&
      Math.abs(own[0]!.left - cell.left) <= 1 &&
      Math.abs(own[0]!.right - cell.right) <= 1;
    return cell.named.includes(null) || cell.named.length !== 2 ||
      groupNames.join() !== expected.group || own[0]?.label !== expected.label || !aligned;
  });
  expect.soft(
    unassociated.map(cell => `${cell.field} on record ${cell.record}`),
    `cells whose headers do not name their group and own field heading ${where}`,
  ).toEqual([]);
}

/** Reads one closed phone card without waiting, so a red reports once and at once. */
async function readClosedCard(card: Locator) {
  return card.evaluate((row, fields) => {
    type Edges = { left: number; right: number; top: number; bottom: number };
    const rendered = (node: Element | null | undefined): node is Element =>
      !!node && node.getClientRects().length > 0 && getComputedStyle(node).visibility === 'visible';
    const edges = (rects: DOMRect[]): Edges | null => rects.length === 0 ? null : {
      left: Math.min(...rects.map(rect => rect.left)),
      right: Math.max(...rects.map(rect => rect.right)),
      top: Math.min(...rects.map(rect => rect.top)),
      bottom: Math.max(...rects.map(rect => rect.bottom)),
    };
    const box = (node: Element | null | undefined) =>
      rendered(node) ? edges([node.getBoundingClientRect()]) : null;
    // The extent of the text itself: a block's own box spans the whole card row.
    const textBox = (node: Element | null | undefined) => {
      if (!rendered(node)) return null;
      const range = document.createRange();
      range.selectNodeContents(node);
      return edges(Array.from(range.getClientRects()).filter(rect => rect.width > 0));
    };
    const text = (node: Element | null | undefined) =>
      (node?.textContent ?? '').replace(/\s+/g, ' ').trim();
    const name = row.querySelector('.exercise-name');
    const routine = row.querySelector('[data-key="routine"]');
    const status = row.querySelector('.badge.ui-badge');
    const planned = row.querySelector('.log-prescription');
    return {
      viewport: document.documentElement.clientWidth,
      card: edges([row.getBoundingClientRect()])!,
      name: { text: text(name), box: textBox(name) },
      routine: { text: text(routine), box: textBox(routine) },
      status: { text: text(status), box: box(status) },
      planned: { text: text(planned), box: textBox(planned) },
      fields: fields.map(({ field }) => {
        const cell = row.querySelector(`[data-field="${field}"]`);
        const label = cell?.querySelector('.log-field-label');
        return {
          field,
          label: { text: text(label), box: box(label) },
          value: { text: text(cell?.querySelector('.editable-text')), box: box(cell?.querySelector('.log-trigger')) },
        };
      }),
    };
  }, CARD_FIELDS);
}

/**
 * Criterion 4: a closed card shows its name, routine, status, planned line and logged
 * fields, in reading order and inside the viewport. Returns the pairs out of order.
 */
async function expectClosedCardContent(card: Locator, record: Record<string, unknown>) {
  const exercise = String(record.exercise);
  const read = await readClosedCard(card);
  const mainRpe = record.scored_rpe != null || (record.planned_rpe != null && record.planned_rir == null);
  const fields = read.fields.filter(entry => entry.field !== 'scored_rpe' || mainRpe);
  const parts: [string, CardPart][] = [
    ['name', read.name],
    ['routine', read.routine],
    ['status', read.status],
    ['planned line', read.planned],
    ...fields.map((entry): [string, CardPart] => [`logged ${entry.label.text || entry.field}`, entry.value]),
  ];
  const labels: [string, CardPart][] = fields.map(entry => [`label of ${entry.field}`, entry.label]);

  const hidden = [...parts, ...labels].filter(([, part]) => part.box === null).map(([part]) => part);
  expect.soft(hidden, `parts not visible on the closed ${exercise} card`).toEqual([]);

  expect.soft(read.name.text, `name on the ${exercise} card`).toBe(exercise);
  for (const piece of String(record.routine).split(' - ')) {
    expect.soft(read.routine.text, `routine on the ${exercise} card`).toContain(piece);
  }
  expect.soft(read.status.text, `status on the ${exercise} card`).toMatch(/^(Achieved|Pending)$/);
  const line = `planned line on the ${exercise} card`;
  expect.soft(read.planned.text, line).toMatch(new RegExp(`(^|\\D)${printed(record.planned_sets)} sets\\b`));
  const reps = `${printed(record.planned_min_reps)}\\s*[–-]\\s*${printed(record.planned_max_reps)} reps\\b`;
  expect.soft(read.planned.text, line).toMatch(new RegExp(`(^|\\D)${reps}`));
  expect.soft(read.planned.text, line).toMatch(new RegExp(`(^|[^\\d.])${printed(record.planned_weight)} kg\\b`));
  for (const effort of ['rir', 'rpe']) {
    const stored = record[`planned_${effort}`];
    const shown = new RegExp(`\\b${effort.toUpperCase()} ${stored == null ? '' : printed(stored)}`);
    if (stored == null) expect.soft(read.planned.text, line).not.toMatch(shown);
    else expect.soft(read.planned.text, line).toMatch(new RegExp(`${shown.source}($|\\D)`));
  }
  const expectedFields = CARD_FIELDS.filter(entry => entry.field !== 'scored_rpe' || mainRpe);
  expect.soft(fields.map(entry => entry.label.text), `field labels on the ${exercise} card`)
    .toEqual(expectedFields.map(entry => entry.label));
  for (const entry of fields) {
    const stored = record[entry.field];
    const value = stored == null ? /^--$/ : new RegExp(`^${printed(stored)}$`);
    expect.soft(entry.value.text, `${entry.field} on the ${exercise} card`).toMatch(value);
  }

  const outside = [...parts, ...labels].filter(([, part]) => part.box !== null && (
    part.box.left < 0 || part.box.right > read.viewport ||
    part.box.left < read.card.left - 1 || part.box.right > read.card.right + 1 ||
    part.box.top < read.card.top - 1 || part.box.bottom > read.card.bottom + 1
  )).map(([part]) => part);
  expect.soft(outside, `parts outside the viewport or the ${exercise} card`).toEqual([]);

  // Reading order: the next part is below, or on the same row and to the right.
  const follows = (first: Box, next: Box) => {
    const sameRow = next.top < first.bottom - 1 && first.top < next.bottom - 1;
    return sameRow ? next.left >= first.right - 1 : next.top >= first.bottom - 1;
  };
  const misplaced: string[] = [];
  for (let index = 1; index < parts.length; index += 1) {
    const [before, first] = parts[index - 1];
    const [after, next] = parts[index];
    if (first.box && next.box && !follows(first.box, next.box)) {
      misplaced.push(`${exercise}: ${after} does not follow ${before}`);
    }
  }
  return misplaced;
}

/** Criterion 19: with Details closed, logged RPE and RIR share the visible main row. */
async function expectEffortInMainRow(card: Locator, rpeText: RegExp) {
  const details = card.getByRole('button', { name: 'Details', exact: true });
  const rpe = card.locator('[data-field="scored_rpe"]');
  const rpeTrigger = rpe.locator('.log-trigger');
  const rirTrigger = card.locator('[data-field="scored_rir"] .log-trigger');
  await expect.soft(details).toHaveAttribute('aria-expanded', 'false');
  await expect.soft(rpeTrigger, 'logged RPE trigger in the main row').toBeVisible();
  await expect.soft(rpe.locator('.editable-text'), 'logged RPE value in the main row').toBeVisible();
  await expect.soft(rpe.locator('.editable-text')).toHaveText(rpeText);
  await expect.soft(rirTrigger, 'logged RIR trigger in the main row').toBeVisible();
  const rpeBox = await rpeTrigger.isVisible() ? await rpeTrigger.boundingBox() : null;
  const rirBox = await rirTrigger.isVisible() ? await rirTrigger.boundingBox() : null;
  const sameRow = !!rpeBox && !!rirBox && Math.abs(rpeBox.y - rirBox.y) <= 1;
  expect.soft(sameRow, 'logged RPE and RIR share one row').toBe(true);
}

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
      await expect(sort.locator(direction === 'ascending' ? '.fa-sort-up' : '.fa-sort-down')).toBeVisible();
      await expect(page.locator('th:not([aria-sort]) .log-sort .fa-sort')).toHaveCount(15);
      const sorted = await rows.allTextContents();
      if (field === 'exercise') expect(sorted).toEqual(direction === 'ascending' ? names : [...names].reverse());
      else expect(sorted.filter(name => fixture.find(record => record.exercise === name)?.scored_weight != null))
        .toEqual(['Barbell Curl','Barbell Bench Press','Barbell Bent Over Row','Barbell Squat','Barbell Deadlift']);
    }
  }
  await page.setViewportSize({width: 390, height: 844});
  const misplaced: string[] = [];
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
    // Criterion 4, on the closed card and before any edit.
    misplaced.push(...await expectClosedCardContent(card, record));
    await details.press('Enter');
    await expect.soft(details, `Details expanded on ${record.exercise}`).toHaveAttribute('aria-expanded', 'true');
    await expect(rpe).toBeVisible();
    await expect(card.getByRole('button', {name: /reference video/i})).toBeVisible();
    await expect(card.getByRole('button', {name: /Delete Entry/})).toBeVisible();
    // Section 0: below 768 px every button, field and disclosure is at least 44 px tall.
    const targets = {
      'Details': details,
      'Last Progression': card.getByRole('button', {name: /Last Progression/}),
      'Reference Video': card.getByRole('button', {name: /reference video/i}),
      'Delete Entry': card.getByRole('button', {name: /Delete Entry/}),
    };
    for (const [name, target] of Object.entries(targets)) {
      await expect.soft(target, `${name} shown on ${record.exercise}`).toBeVisible();
      const box = await target.isVisible() ? await target.boundingBox() : null;
      const height = box ? Math.round(box.height * 2) / 2 : 0;
      expect.soft(height, `${name} height at 390 px on ${record.exercise}`).toBeGreaterThanOrEqual(44);
    }
    await details.press('Space');
    await expect(card.getByRole('button', {name: /Delete Entry/})).toBeHidden();
  }
  expect.soft(misplaced, 'criterion 4: card parts out of reading order').toEqual([]);
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
  // Criterion 19: after the reload the saved RPE and the RIR trigger are in the main row.
  await expectEffortInMainRow(row('Barbell Seated Military Press'), /^9(?:\.0)?$/);
  await enter('Barbell Deadlift', 'scored_rir', '2');
  await expect(row('Barbell Deadlift').locator('.ui-badge')).toHaveText('Pending');
  // Criterion 11: count every write that carries a zero RIR for this record.
  const deadliftId = await row('Barbell Deadlift').getAttribute('data-log-id');
  const zeroRequests: unknown[] = [];
  const zeroResponses: boolean[] = [];
  const carriesZeroRir = (request: Request) => {
    if (new URL(request.url()).pathname !== '/update_workout_log' || request.method() !== 'POST') return false;
    const body = request.postDataJSON() as {id?: unknown; updates?: Record<string, unknown>} | null;
    const value = body?.updates?.scored_rir;
    const zero = value != null && String(value).trim() !== '' && Number(value) === 0;
    return String(body?.id) === deadliftId && zero;
  };
  const countRequest = (request: Request) => {
    if (carriesZeroRir(request)) zeroRequests.push(request.postDataJSON());
  };
  const countResponse = (response: Response) => {
    if (carriesZeroRir(response.request())) zeroResponses.push(response.ok());
  };
  page.on('request', countRequest);
  page.on('response', countResponse);
  const deadlift = await enter('Barbell Deadlift', 'scored_rir', '0');
  await page.reload();
  page.off('request', countRequest);
  page.off('response', countResponse);
  expect.soft(zeroRequests, 'criterion 11: zero RIR writes for the Deadlift record').toHaveLength(1);
  expect.soft(zeroResponses, 'criterion 11: the zero RIR write succeeded').toEqual([true]);
  const deadliftRir = row('Barbell Deadlift').locator('[data-field="scored_rir"]');
  await expect.soft(deadliftRir.locator('.editable-text'), 'criterion 11: zero stays visible').toBeVisible();
  await expect.soft(deadliftRir.locator('.editable-text'), 'criterion 11: field shows 0').toHaveText('0');
  await expect(row('Barbell Deadlift').locator('[data-field="scored_rir"] .log-improved')).toBeVisible();
  const progression = await (await page.request.get(`/check_progression/${deadlift}`)).json();
  expect.soft(progression.data.status, 'criterion 11: server progression').toBe('Achieved');
  await expect.soft(row('Barbell Deadlift').locator('.ui-badge'), 'criterion 11: badge').toHaveText('Achieved');
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

async function captureEditor(page: Page, run: string, width: number, theme: string) {
  // Squat has all five main fields and a maintained 100.0 kg weight.
  const row = page.locator('tr[data-log-id]').filter({has: page.getByText('Barbell Squat', {exact: true})});
  const filename = (state: string) => path.join(run, `populated-${width}-${theme}-scale6-${state}`);
  const card = width < 1360;
  const weight = row.locator('[data-field="scored_weight"]');
  await expect(weight.locator('.editable-text')).toHaveText('100.0');
  const weightLayout = await weight.evaluate(cell => {
    const mark = cell.querySelector('.progression-indicator')!.getBoundingClientRect();
    const field = cell.querySelector('.log-trigger')!.getBoundingClientRect();
    const range = document.createRange();
    range.selectNodeContents(cell.querySelector('.editable-text')!);
    const digits = range.getBoundingClientRect();
    return {gap: digits.left - mark.right, fits: mark.left > field.left && digits.right < field.right};
  });
  expect.soft(weightLayout.gap, `weight mark clearance at ${width}`).toBeGreaterThan(0);
  expect.soft(weightLayout.fits, 'mark and digits inside the weight field').toBe(true);
  if (card) {
    const buttons = row.locator('.scored-cell .log-trigger:visible');
    const tops = await buttons.evaluateAll(nodes => nodes.map(node => node.getBoundingClientRect().top));
    expect.soft(tops).toHaveLength(5);
    expect.soft(new Set(tops).size, 'resting field alignment').toBe(1);
    await row.locator('.log-details').click();
    await expect(row.locator('.log-details i')).toBeVisible();
    await row.scrollIntoViewIfNeeded();
    await page.screenshot({path: filename('details.png'), fullPage: width === 390});
    await row.locator('.log-details').click();
  }
  const cell = row.locator('[data-field="scored_min_reps"]');
  await cell.locator('.log-trigger').click();
  const editor = await cell.evaluate(td => {
    const box = (node: Element) => node.getBoundingClientRect();
    const wrapper = td.querySelector('.number-input-wrapper')!;
    const sizes = [...wrapper.children].map(el => [box(el).width, box(el).height]);
    const labels = [...td.closest('tr')!.querySelectorAll('.scored-cell .log-field-label')];
    const labelTops = labels.map(el => box(el).top);
    const lineHeights = labels.map(el => {
      const text = document.createRange();
      text.selectNodeContents(el);
      return text.getClientRects().length;
    });
    const contained = [wrapper, ...wrapper.children].every(el =>
      box(el).left >= box(td).left && box(el).right <= box(td).right);
    const row = td.closest('tr')!;
    const triggers = [...row.querySelectorAll('.log-trigger')].filter(el => el.getClientRects().length);
    const fitsBelow = box(wrapper).left >= box(row).left && box(wrapper).right <= box(row).right &&
      triggers.every(el => box(el).bottom <= box(wrapper).top) &&
      box(wrapper).bottom <= box(row.querySelector('.log-details')!).top;
    return {sizes, contained, fitsBelow, labelTops, lineHeights, cellWidth: box(td).width, editorWidth: box(wrapper).width};
  });
  fs.writeFileSync(filename('geometry.json'), JSON.stringify({...weightLayout, ...editor}, null, 2));
  if (card) {
    expect.soft(editor.fitsBelow, 'editor between the field row and Details').toBe(true);
    expect.soft(editor.sizes.every(pair => pair.every(side => side >= 44)), 'editor touch targets').toBe(true);
    expect.soft(new Set(editor.labelTops).size, 'five fields in one row').toBe(1);
    expect.soft(editor.lineHeights, 'single-line labels').toEqual([1,1,1,1,1]);
  } else {
    expect.soft(editor.contained, 'editor and controls inside table cell').toBe(true);
  }
  await row.scrollIntoViewIfNeeded();
  await page.screenshot({path: filename('editing.png'), fullPage: width === 390});
  await cell.locator('input').press('Escape');
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
          if (width === 390) {
            await page.screenshot({path: path.join(run, `${populated ? 'populated' : 'empty'}-390-${theme}-scale${scale}-full.png`), fullPage: true});
          }
          await page.addStyleTag({content: '*,*::before,*::after { transition: none !important; animation: none !important; }'});
          entries.push({populated, scale, width, theme, ...await measure(page, control)});
          if (!control && scale === 6) {
            if (populated && [390, 768, 1360].includes(width)) {
              await captureEditor(page, run, width, theme);
            }
            const expected = populated ? [] : ['import-from-plan-btn'];
            expect(await page.locator('#main-content .ui-btn--primary:visible').evaluateAll(buttons => buttons.map(b => b.id))).toEqual(expected);
            expect(await page.locator('#main-content button:visible').evaluateAll((buttons, fill) =>
              buttons.filter(b => getComputedStyle(b).backgroundColor === fill).map(b => b.id),
              theme === 'dark' ? 'rgb(82, 100, 173)' : 'rgb(66, 99, 235)')).toEqual(expected);
            const where = `at ${width} px in ${theme}`;
            if (populated) {
              await expectPopulatedActionVariants(page, theme as Theme, where);
            }
            if (populated && width === 1440) {
              await expectDesktopColumnGroups(page, where);
            }
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
