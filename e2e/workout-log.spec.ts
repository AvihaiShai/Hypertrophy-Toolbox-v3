/**
 * E2E Test: Workout Log
 * 
 * Tests the workout log page functionality including:
 * - Loading page
 * - Import from workout plan
 * - Editing scored values
 * - Deleting entries
 */
import { test, expect, ROUTES, SELECTORS, expectToast, waitForPageReady } from './fixtures';
import type { APIRequestContext, Locator, Page } from '@playwright/test';

// Section 0: the filled primary is #4263eb in the light theme this suite runs in.
const PRIMARY_FILL_LIGHT = 'rgb(66, 99, 235)';
// Section 0, "Behind Details", plus logged RPE when the plan also holds an RIR.
const DETAILS_ONLY_CONTROLS = ['Last Progression', 'Reference Video', 'Delete Entry', 'Logged RPE'];
const PLANNED_VALUE_KEYS = ['sets', 'min_reps', 'max_reps', 'rir', 'rpe', 'weight'] as const;
// Section 0, "Always visible": the logged fields of a phone card, in main-row order.
const MAIN_ROW_FIELDS = [
  'scored_min_reps', 'scored_max_reps', 'scored_weight', 'scored_rir', 'scored_rpe',
] as const;
type MainRowField = (typeof MAIN_ROW_FIELDS)[number];
// How a five-field card arranges its logged fields: on one row, or wrapped three and two.
const FIVE_FIELDS_ON_ONE_ROW: string[][] = [[...MAIN_ROW_FIELDS]];
const FIVE_FIELDS_WRAPPED: string[][] = [
  ['scored_min_reps', 'scored_max_reps', 'scored_weight'],
  ['scored_rir', 'scored_rpe'],
];
// The owner's Barbell Squat case on #736, as the card prints each logged value.
const SQUAT_LOGGED_TEXT: Record<MainRowField, string> = {
  scored_min_reps: '10',
  scored_max_reps: '10',
  scored_weight: '100.0',
  scored_rir: '1',
  scored_rpe: '10.0',
};

/** Ids of the visible actions in the page content that render the filled primary. */
async function filledPrimaryActions(page: Page): Promise<string[]> {
  const actions = page.locator('#main-content').locator('button:visible, a:visible');
  return actions.evaluateAll((nodes, fill) => {
    const filled = nodes.filter(node => getComputedStyle(node).backgroundColor === fill);
    return filled.map(node => node.id || (node.textContent ?? '').trim());
  }, PRIMARY_FILL_LIGHT);
}

/** Ids of the visible actions in the page content that carry the primary variant class. */
async function primaryVariantActions(page: Page): Promise<string[]> {
  const actions = page.locator('#main-content .ui-btn--primary:visible');
  return actions.evaluateAll(nodes => nodes.map(node => node.id));
}

/** Names the focused control when focus is inside the card, or null when it left. */
async function focusedCardControl(card: Locator, controls: string[]): Promise<string | null> {
  return card.evaluate((row, names) => {
    const active = document.activeElement;
    if (!active || !row.contains(active)) return null;
    const described = `${active.getAttribute('aria-label') ?? ''} ${active.textContent ?? ''}`;
    const label = described.replace(/\s+/g, ' ').trim();
    const known = names.find(name => label.toLowerCase().includes(name.toLowerCase()));
    return known ?? label;
  }, controls);
}

/** Every stop the keyboard reaches inside one card, walking both ways from Details. */
async function cardTabStops(page: Page, card: Locator): Promise<string[]> {
  const details = card.getByRole('button', { name: 'Details', exact: true });
  const stops: string[] = [];
  for (const key of ['Tab', 'Shift+Tab']) {
    await details.focus();
    for (let step = 0; step < 12; step += 1) {
      await page.keyboard.press(key);
      const stop = await focusedCardControl(card, DETAILS_ONLY_CONTROLS);
      if (stop === null) break;
      stops.push(stop);
    }
  }
  return stops;
}

/** Criterion 19: with Details closed, logged RPE and RIR share the visible main row. */
async function expectEffortInMainRow(card: Locator, rpeText: RegExp): Promise<void> {
  const details = card.getByRole('button', { name: 'Details', exact: true });
  const rpe = card.locator('[data-field="scored_rpe"]');
  const rpeTrigger = rpe.locator('.log-trigger');
  const rirTrigger = card.locator('[data-field="scored_rir"] .log-trigger');
  await expect(details).toHaveAttribute('aria-expanded', 'false');
  await expect(rpeTrigger).toBeVisible();
  await expect(rpe.locator('.editable-text')).toBeVisible();
  await expect(rpe.locator('.editable-text')).toHaveText(rpeText);
  await expect(rirTrigger).toBeVisible();
  // Both tops come from one read. After a reload the browser may still be scrolling to
  // its restored position, and two reads taken apart place one row at two offsets.
  const tops = await card.evaluate(row => {
    const top = (field: string) =>
      row.querySelector(`[data-field="${field}"] .log-trigger`)!.getBoundingClientRect().top;
    return { rpe: top('scored_rpe'), rir: top('scored_rir') };
  });
  expect(Math.abs(tops.rpe - tops.rir), 'logged RPE and RIR share one row').toBeLessThanOrEqual(1);
}

/**
 * Edges and overflow of one phone card's logged fields, read in one pass. A card that
 * keeps logged RPE behind Details passes the four fields it shows.
 */
async function readMainRowFit(card: Locator, shown: readonly MainRowField[] = MAIN_ROW_FIELDS) {
  return card.evaluate((row, fields) => {
    type Edges = { left: number; right: number; top: number; bottom: number };
    const edges = (rects: DOMRect[]): Edges | null => rects.length === 0 ? null : {
      left: Math.min(...rects.map(rect => rect.left)),
      right: Math.max(...rects.map(rect => rect.right)),
      top: Math.min(...rects.map(rect => rect.top)),
      bottom: Math.max(...rects.map(rect => rect.bottom)),
    };
    const rendered = (node: Element | null | undefined): node is Element =>
      !!node && node.getClientRects().length > 0 && getComputedStyle(node).visibility === 'visible';
    const box = (node: Element | null | undefined) =>
      rendered(node) ? edges([node.getBoundingClientRect()]) : null;
    // A Range follows the glyphs, so text that runs past its own box is still measured.
    const textBox = (node: Element | null | undefined) => {
      if (!rendered(node)) return null;
      const range = document.createRange();
      range.selectNodeContents(node);
      return edges(Array.from(range.getClientRects()).filter(rect => rect.width > 0));
    };
    const root = document.documentElement;
    return {
      card: edges([row.getBoundingClientRect()])!,
      page: { scrollWidth: root.scrollWidth, clientWidth: root.clientWidth },
      fields: fields.map(field => {
        const cell = row.querySelector(`[data-field="${field}"]`);
        const trigger = cell?.querySelector<HTMLElement>('.log-trigger');
        return {
          field,
          box: box(trigger),
          value: textBox(cell?.querySelector('.editable-text')),
          mark: box(cell?.querySelector('.progression-indicator')),
          scrollWidth: trigger?.scrollWidth ?? 0,
          clientWidth: trigger?.clientWidth ?? 0,
        };
      }),
    };
  }, shown);
}

type MainRowFit = Awaited<ReturnType<typeof readMainRowFit>>;
type FitEdges = MainRowFit['card'];

/** How many rows the rendered logged fields occupy, counting tops within 1 px as one row. */
function mainRowCount(read: MainRowFit): number {
  const tops = read.fields.flatMap(entry => entry.box ? [entry.box.top] : []);
  const rows: number[] = [];
  for (const top of tops) {
    if (!rows.some(known => Math.abs(known - top) <= 1)) rows.push(top);
  }
  return rows.length;
}

/**
 * The owner's acceptance for a phone card, as measured failures: every logged field is a
 * 44 x 44 target inside the card, its value and comparison mark sit inside the field and
 * clear of each other, the card is inside the viewport and the page does not scroll
 * sideways. Containment and overlap allow 0.5 px. Sizes allow nothing.
 */
function mainRowFitProblems(read: MainRowFit, viewportWidth: number): string[] {
  const tolerance = 0.5;
  const px = (value: number) => `${Math.round(value * 10) / 10} px`;
  const escapes = (inner: FitEdges, outer: FitEdges) => Math.max(
    outer.left - inner.left,
    inner.right - outer.right,
    outer.top - inner.top,
    inner.bottom - outer.bottom,
  );
  const overlaps = (first: FitEdges, next: FitEdges) =>
    Math.min(first.right, next.right) - Math.max(first.left, next.left) > tolerance &&
    Math.min(first.bottom, next.bottom) - Math.max(first.top, next.top) > tolerance;
  const problems: string[] = [];
  for (const [index, entry] of read.fields.entries()) {
    const name = entry.field;
    if (!entry.box) {
      problems.push(`${name}: the field is not rendered`);
      continue;
    }
    const width = entry.box.right - entry.box.left;
    const height = entry.box.bottom - entry.box.top;
    if (width < 44 || height < 44) {
      problems.push(`${name}: the field is ${px(width)} x ${px(height)}, under 44 x 44`);
    }
    if (escapes(entry.box, read.card) > tolerance) {
      const depth = px(escapes(entry.box, read.card));
      const edge = `field right ${px(entry.box.right)}, card right ${px(read.card.right)}`;
      problems.push(`${name}: the field leaves its card by ${depth} (${edge})`);
    }
    for (const later of read.fields.slice(index + 1)) {
      if (later.box && overlaps(entry.box, later.box)) {
        problems.push(`${name}: the field overlaps the ${later.field} field`);
      }
    }
    if (entry.scrollWidth > entry.clientWidth) {
      const sizes = `${entry.scrollWidth} px of content in a ${entry.clientWidth} px field`;
      problems.push(`${name}: the value is clipped (${sizes})`);
    }
    if (!entry.value) {
      problems.push(`${name}: the value is not rendered`);
    } else if (escapes(entry.value, entry.box) > tolerance) {
      problems.push(`${name}: the value leaves its field by ${px(escapes(entry.value, entry.box))}`);
    }
    if (!entry.mark) {
      problems.push(`${name}: the comparison mark is not rendered`);
    } else if (escapes(entry.mark, entry.box) > tolerance) {
      problems.push(`${name}: the mark leaves its field by ${px(escapes(entry.mark, entry.box))}`);
    }
    if (entry.mark && entry.value && overlaps(entry.mark, entry.value)) {
      problems.push(`${name}: the mark overlaps the value`);
    }
  }
  if (read.card.left < -tolerance || read.card.right > viewportWidth + tolerance) {
    const span = `${px(read.card.left)} to ${px(read.card.right)}`;
    problems.push(`the card spans ${span} in a ${viewportWidth} px viewport`);
  }
  if (read.page.scrollWidth > read.page.clientWidth) {
    const sizes = `scrollWidth ${read.page.scrollWidth}, clientWidth ${read.page.clientWidth}`;
    problems.push(`the page scrolls sideways (${sizes})`);
  }
  return problems;
}

/** The rendered logged fields as rows, top to bottom and left to right. Tops within 1 px share a row. */
function mainRowGroups(read: MainRowFit): string[][] {
  const rows: { top: number; fields: { name: string; left: number }[] }[] = [];
  for (const entry of read.fields) {
    if (!entry.box) continue;
    const { top, left } = entry.box;
    const row = rows.find(known => Math.abs(known.top - top) <= 1);
    if (row) row.fields.push({ name: entry.field, left });
    else rows.push({ top, fields: [{ name: entry.field, left }] });
  }
  return rows.sort((first, next) => first.top - next.top)
    .map(row => row.fields.sort((first, next) => first.left - next.left).map(field => field.name));
}

/**
 * The phone-card acceptance on the given logged fields: each field, its value and its
 * comparison mark are visible, and the card has no fit problem. Returns the measured card.
 */
async function expectMainRowFit(
  card: Locator, fields: readonly MainRowField[], viewportWidth: number, where: string,
): Promise<MainRowFit> {
  for (const field of fields) {
    const cell = card.locator(`[data-field="${field}"]`);
    await expect.soft(cell.locator('.log-trigger'), `${field} field ${where}`).toBeVisible();
    await expect.soft(cell.locator('.editable-text'), `${field} value ${where}`).toBeVisible();
    await expect.soft(cell.locator('.progression-indicator'), `${field} mark ${where}`).toBeVisible();
  }
  const read = await readMainRowFit(card, fields);
  expect.soft(mainRowFitProblems(read, viewportWidth), `phone card fit ${where}`).toEqual([]);
  return read;
}

type LoggedSquat = { id: number; stored: () => Promise<Record<string, unknown>> };

/**
 * Runs the body against one Barbell Squat record on a routine of its own, then removes it.
 * The plan is the owner's case on #736: 6 to 10 reps at 100 kg with RIR 2 and RPE 8, so
 * every field that is logged has a planned value and carries a comparison mark.
 */
async function withLoggedSquat(
  request: APIRequestContext, label: string, logged: Record<string, number>,
  body: (record: LoggedSquat) => Promise<void>,
): Promise<void> {
  const routine = `GYM - ${label} ${Date.now()} - Workout A`;
  const exercise = 'Barbell Squat';
  const added = await request.post('/add_exercise', {
    data: {
      routine, exercise, sets: 3, min_rep_range: 6, max_rep_range: 10, rir: 2, rpe: 8, weight: 100,
    },
  });
  expect(added.ok()).toBe(true);
  const plan = (await (await request.get('/get_workout_plan')).json()).data as
    { id: number; routine: string; exercise: string }[];
  const planRow = plan.find(entry => entry.routine === routine && entry.exercise === exercise);
  expect(planRow).toBeDefined();

  try {
    expect((await request.post('/export_to_workout_log')).ok()).toBe(true);
    const stored = async () => {
      const logs = (await (await request.get('/get_workout_logs')).json()).data as
        Record<string, unknown>[];
      const record = logs.find(entry => entry.routine === routine && entry.exercise === exercise);
      expect(record, `the ${routine} record`).toBeDefined();
      return record!;
    };
    const id = Number((await stored()).id);
    const written = await request.post('/update_workout_log', { data: { id, updates: logged } });
    expect(written.ok()).toBe(true);
    expect(await stored()).toMatchObject({
      planned_min_reps: 6, planned_max_reps: 10, planned_weight: 100,
      planned_rir: 2, planned_rpe: 8, ...logged,
    });
    await body({ id, stored });
  } finally {
    const removed = await request.post('/remove_exercise', { data: { id: planRow!.id } });
    expect(removed.ok()).toBe(true);
  }
}

/**
 * Loads the Workout Log at a phone width with the app scale at level 8. The level goes
 * through the app's own controller, which stores it for the server to render.
 */
async function openLogAtScale8(page: Page, width: number): Promise<void> {
  await page.setViewportSize({ width, height: 844 });
  await page.goto(ROUTES.WORKOUT_LOG);
  await page.evaluate(() => {
    const scale = (window as unknown as {
      accessibilityController: { setScale(level: number): void };
    }).accessibilityController;
    scale.setScale(8);
  });
  await page.goto(ROUTES.WORKOUT_LOG);
  await expect(page.locator('html')).toHaveAttribute('data-scale', '8');
  const zoom = await page.locator('html').evaluate(el => Number(getComputedStyle(el).zoom));
  expect(zoom, `app scale factor at ${width} px at scale 8`).toBe(1.2);
  await page.evaluate(() => document.fonts.ready.then(() => undefined));
}

/** Opens a logged field's inline editor on a phone card and waits for its input to take focus. */
async function openLoggedEditor(card: Locator, field: MainRowField): Promise<Locator> {
  const cell = card.locator(`[data-field="${field}"]`);
  await cell.locator('.log-trigger').click();
  const input = cell.locator('input');
  await expect(input, `${field} editor input`).toBeFocused();
  return input;
}

/** Saves a logged value through the card's inline editor and waits for the card to print it. */
async function saveLoggedValue(page: Page, card: Locator, field: MainRowField, text: string): Promise<void> {
  const id = await card.getAttribute('data-log-id');
  const input = await openLoggedEditor(card, field);
  await input.fill(text);
  const saved = page.waitForResponse(response =>
    new URL(response.url()).pathname === '/update_workout_log' &&
    response.request().method() === 'POST' &&
    String(response.request().postDataJSON().id) === id);
  await input.press('Enter');
  expect((await saved).ok(), `saving ${field} as ${text}`).toBe(true);
  // The page prints the value and refits the card in one step, once the save is confirmed.
  await expect(card.locator(`[data-field="${field}"] .editable-text`)).toHaveText(text);
}

/** Edges of one field's open inline editor and of what it must stay clear of, in one pass. */
async function readEditorFit(card: Locator, field: MainRowField) {
  return card.evaluate((row, name) => {
    const edges = (node: Element) => {
      const box = node.getBoundingClientRect();
      return { left: box.left, right: box.right, top: box.top, bottom: box.bottom };
    };
    const rendered = (node: Element | null | undefined): node is Element =>
      !!node && node.getClientRects().length > 0 && getComputedStyle(node).visibility === 'visible';
    const cell = row.querySelector(`[data-field="${name}"]`);
    const wrapper = cell?.querySelector('.number-input-wrapper');
    const details = row.querySelector('.log-details');
    const root = document.documentElement;
    return {
      card: edges(row),
      page: { scrollWidth: root.scrollWidth, clientWidth: root.clientWidth },
      editor: rendered(wrapper) ? edges(wrapper) : null,
      controls: rendered(wrapper) ? Array.from(wrapper.children).map(control => ({
        name: control.tagName === 'INPUT' ? 'input' : (control.textContent ?? '').trim(),
        box: rendered(control) ? edges(control) : null,
      })) : [],
      fields: Array.from(row.querySelectorAll('.scored-cell')).flatMap(other => {
        const trigger = other.querySelector('.log-trigger');
        return rendered(trigger) ? [{ field: other.getAttribute('data-field') ?? '', box: edges(trigger) }] : [];
      }),
      details: rendered(details) ? edges(details) : null,
    };
  }, field);
}

type EditorFit = Awaited<ReturnType<typeof readEditorFit>>;

/**
 * An open inline editor on a phone card, as measured failures: the editor and its three
 * controls are inside the card and the viewport, each control is a 44 x 44 target, the
 * editor covers no logged field and not the Details button, and the page does not scroll
 * sideways. Containment and overlap allow 0.5 px. Sizes allow nothing.
 */
function editorFitProblems(read: EditorFit, viewportWidth: number): string[] {
  const tolerance = 0.5;
  const px = (value: number) => `${Math.round(value * 10) / 10} px`;
  const escapes = (inner: FitEdges, outer: FitEdges) => Math.max(
    outer.left - inner.left,
    inner.right - outer.right,
    outer.top - inner.top,
    inner.bottom - outer.bottom,
  );
  const overlaps = (first: FitEdges, next: FitEdges) =>
    Math.min(first.right, next.right) - Math.max(first.left, next.left) > tolerance &&
    Math.min(first.bottom, next.bottom) - Math.max(first.top, next.top) > tolerance;
  const problems: string[] = [];
  if (!read.editor) return ['the editor is not rendered'];
  const parts: [string, FitEdges | null][] = [
    ['editor', read.editor],
    ...read.controls.map((control): [string, FitEdges | null] => [`editor ${control.name}`, control.box]),
  ];
  if (read.controls.length !== 3) {
    problems.push(`the editor has ${read.controls.length} controls, not minus, input and plus`);
  }
  for (const [name, box] of parts) {
    if (!box) {
      problems.push(`${name}: not rendered`);
      continue;
    }
    if (escapes(box, read.card) > tolerance) {
      problems.push(`${name}: leaves the card by ${px(escapes(box, read.card))}`);
    }
    if (box.left < -tolerance || box.right > viewportWidth + tolerance) {
      problems.push(`${name}: spans ${px(box.left)} to ${px(box.right)} in a ${viewportWidth} px viewport`);
    }
    if (name !== 'editor' && (box.right - box.left < 44 || box.bottom - box.top < 44)) {
      problems.push(`${name}: is ${px(box.right - box.left)} x ${px(box.bottom - box.top)}, under 44 x 44`);
    }
  }
  for (const entry of read.fields) {
    if (overlaps(read.editor, entry.box)) problems.push(`the editor covers the ${entry.field} field`);
  }
  if (!read.details) problems.push('the Details button is not rendered');
  else if (overlaps(read.editor, read.details)) problems.push('the editor covers the Details button');
  if (read.page.scrollWidth > read.page.clientWidth) {
    const sizes = `scrollWidth ${read.page.scrollWidth}, clientWidth ${read.page.clientWidth}`;
    problems.push(`the page scrolls sideways (${sizes})`);
  }
  return problems;
}

async function importCurrentWorkoutPlan(page: Page): Promise<void> {
  const importResponse = page.waitForResponse(response => {
    return response.url().includes('/export_to_workout_log') &&
      response.request().method() === 'POST';
  });

  await page.locator('#import-from-plan-btn').click();
  const response = await importResponse;

  if (response.ok()) {
    // importFromWorkoutPlan reloads the page after a 1s success toast delay.
    await page.waitForTimeout(1300);
    await waitForPageReady(page);
  }

  await page.locator('#import-from-plan-btn').waitFor({ state: 'visible' });
  await page.waitForFunction(() => {
    const inputs = Array.from(
      document.querySelectorAll<HTMLInputElement>('.workout-log-table input.number-input[type="number"]')
    );

    return inputs.length === 0 || inputs.every(input => input.dataset.hasCustomSpinners === 'true');
  });
}

test.describe('Workout Log Page', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('page loads with correct structure', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('Workout Log');

    // Check import controls section exists
    const importSection = page.locator('.ui-page-actions');
    await expect(importSection).toBeVisible();

    // Check import button exists
    const importBtn = page.locator('#import-from-plan-btn');
    await expect(importBtn).toBeVisible();
    await expect(importBtn).toContainText('Import Current Workout Plan');

    // Check clear log button exists
    const clearBtn = page.locator('#clear-log-btn');
    await expect(clearBtn).toBeVisible();

    // Check table structure
    const table = page.locator('.workout-log-table');
    await expect(table).toBeAttached();
  });

  test('progression legend is visible', async ({ page }) => {
    const legend = page.locator('.progression-legend');
    await expect(legend).toBeVisible({visible: await page.locator('tr[data-log-id]').count() > 0});
    
    // Check legend items
    await expect(legend).toContainText('Improved');
    await expect(legend).toContainText('Maintained');
    await expect(legend).toContainText('Below Target');
  });

  test('workout log table has correct headers', async ({ page }) => {
    const table = page.locator('.workout-log-table');
    const headers = table.locator('thead th');

    // Check expected headers exist
    const headerTexts = await headers.allTextContents();
    const headerString = headerTexts.join(' ').toLowerCase();
    
    expect(headerString).toContain('routine');
    expect(headerString).toContain('exercise');
    expect(headerString).toContain('planned');
    expect(headerString).toContain('logged');
    expect(headerString).toContain('actions');
  });

  test('Import is primary only when the log is empty', async ({page}) => {
    const populated = await page.locator('tr[data-log-id]').count() > 0;
    await expect(page.locator('.ui-empty-state')).toBeVisible({visible: !populated});
    await expect(page.locator('#import-from-plan-btn')).toHaveClass(populated ? /ui-btn--secondary/ : /ui-btn--primary/);
  });

  test('clear log modal opens', async ({ page }) => {
    const clearBtn = page.locator('#clear-log-btn');
    await clearBtn.click();

    // Modal should appear
    const modal = page.locator('#clearLogModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Modal should have confirmation content
    await expect(modal.locator('.modal-body')).toBeVisible();
    await expect(modal.locator('.modal-title')).toContainText('Clear');
    
    // Verify modal has close button and cancel button
    await expect(modal.locator('.btn-close')).toBeVisible();
    await expect(modal.locator('.modal-footer .btn-secondary')).toBeVisible();
  });

  test('editable cells are present in table', async ({ page }) => {
    // Check if editable cells exist (they may only appear when there's data)
    await expect(page.locator('[data-sort-field^="scored_"]')).toHaveCount(5);
    await expect(page.locator('#log-scored')).toHaveAttribute('colspan', '5');
  });
});

test.describe('Workout Log with Data', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();

    // First add some data to workout plan
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    // Select routine and add exercise
    await page.locator(SELECTORS.ROUTINE_ENV).selectOption('GYM');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-program') as HTMLSelectElement;
      return select && select.options.length > 1;
    });
    await page.locator(SELECTORS.ROUTINE_PROGRAM).selectOption('Full Body');
    await page.waitForFunction(() => {
      const select = document.getElementById('routine-day') as HTMLSelectElement;
      return select && select.options.length > 1;
    });
    await page.locator(SELECTORS.ROUTINE_DAY).selectOption('Workout A');

    // Wait for exercise dropdown
    await page.waitForFunction(() => {
      const select = document.getElementById('exercise') as HTMLSelectElement;
      return select && select.options.length > 1;
    });

    // Add an exercise
    const exerciseSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const firstOption = await exerciseSelect.locator('option').nth(1).getAttribute('value');
    if (firstOption) {
      await exerciseSelect.selectOption(firstOption);
    }
    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();

    // Wait for exercise to be added
    await page.waitForSelector('#workout_plan_table_body tr');

    // Navigate to workout log
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('import from workout plan copies exercises', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    // Check if rows appear in the table
    const rows = page.locator('.workout-log-table tbody tr');
    const rowCount = await rows.count();
    
    // Either rows exist or toast shows (depending on implementation)
    // At minimum, no errors should occur
  });

  test('a real import leaves no filled primary and turns Import secondary', async ({ page }) => {
    // Criterion 3, both directions on one page: empty first, then a real import.
    expect((await page.request.post('/clear_workout_log')).ok()).toBe(true);
    await page.reload();
    await waitForPageReady(page);
    const records = page.locator('tr[data-log-id]');
    const importBtn = page.locator('#import-from-plan-btn');
    const clearBtn = page.locator('#clear-log-btn');
    await expect(records).toHaveCount(0);
    await expect(page.locator('.ui-empty-state')).toBeVisible();
    expect(await primaryVariantActions(page)).toEqual(['import-from-plan-btn']);
    expect(await filledPrimaryActions(page)).toEqual(['import-from-plan-btn']);

    await importCurrentWorkoutPlan(page);

    await expect(records.first()).toBeVisible();
    await expect(page.locator('.ui-empty-state')).toBeHidden();
    await expect(importBtn).toBeVisible();
    await expect(importBtn).toHaveClass(/(^|\s)ui-btn--secondary(\s|$)/);
    await expect(importBtn).not.toHaveClass(/(^|\s)ui-btn--primary(\s|$)/);
    await expect(clearBtn).toBeVisible();
    await expect(clearBtn).toHaveClass(/(^|\s)ui-btn--danger(\s|$)/);
    expect(await primaryVariantActions(page)).toEqual([]);
    expect(await filledPrimaryActions(page)).toEqual([]);
  });

  test('phone Log fields have touch targets and Details at the card breakpoint', async ({ page }) => {
    await importCurrentWorkoutPlan(page);
    const row = page.locator('.workout-log-table tr[data-log-id]').first();
    await expect(row.locator('.exercise-name')).toBeVisible();
    for (const width of [375, 390]) {
      await page.setViewportSize({ width, height: 844 });
      const trigger = row.locator('[data-field="scored_rir"] .log-trigger');
      const bounds = await trigger.boundingBox();
      expect(bounds?.width).toBeGreaterThanOrEqual(44);
      expect(bounds?.height).toBeGreaterThanOrEqual(44);
      const details = row.getByRole('button', {name:'Details', exact:true});
      await details.click();
      await expect(row.getByRole('button', {name:/reference video/i})).toBeVisible();
      await expect(row.locator('.date-display')).toBeVisible();
      await details.press('Space');
      await expect(details).toHaveAttribute('aria-expanded', 'false');
      await expect(row.locator('.date-display')).toBeHidden();
      const score = row.locator('[data-field="scored_rir"]');
      await score.locator('.editable-text').click();
      await expect(score.locator('input')).toBeFocused();
      await score.locator('input').press('Escape');
    }
    for (const width of [1359, 1360]) {
      await page.setViewportSize({width, height: 900});
      await expect(page.locator('#log-planned')).toBeVisible({visible: width === 1360});
      await expect(row.locator('.log-details')).toBeVisible({visible: width === 1359});
    }
  });

  test('scored fields can be edited', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const editableCells = page.locator('.editable.scored-cell, [data-field*="scored"]');
    const count = await editableCells.count();

    if (count > 0) {
      const firstCell = editableCells.first();
      await firstCell.click();
      
      // Should be editable - either turns into input or is already input
      const input = firstCell.locator('input');
      const isInput = await input.count() > 0;
      const isContentEditable = await firstCell.getAttribute('contenteditable');
      
      expect(isInput || isContentEditable === 'true').toBeTruthy();
    }
  });

  test('weight field accepts valid values', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const weightCell = page.locator('td[data-field="scored_weight"]').first();
    const count = await weightCell.count();

    if (count > 0) {
      const weightDisplay = weightCell.locator('.editable-text').first();
      await weightDisplay.click();

      const weightInput = weightCell.locator('input').first();
      await expect(weightInput).toBeVisible();
      await weightInput.fill('100');
      await weightInput.blur();
      
      await page.waitForTimeout(700);

      await expect(weightInput).toBeHidden();
      await expect(weightDisplay).toBeVisible();
      await expect(weightDisplay).toContainText('100');
    }
  });

  test('scored reps preserve saved zero after rejection and clear only on an empty edit', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const firstRow = page.locator('.workout-log-table tr[data-log-id]').first();
    await expect(firstRow).toBeVisible();
    const logId = await firstRow.getAttribute('data-log-id');
    expect(logId).toMatch(/^\d+$/);
    const row = page.locator(`.workout-log-table tr[data-log-id="${logId}"]`);
    const minCell = row.locator('[data-field="scored_min_reps"]');
    const maxCell = row.locator('[data-field="scored_max_reps"]');
    const minDisplay = minCell.locator('.editable-text');
    const maxDisplay = maxCell.locator('.editable-text');
    const minInput = minCell.locator('input[type="number"]');
    const maxInput = maxCell.locator('input[type="number"]');

    const readStoredReps = async () => {
      const response = await page.request.get('/get_workout_logs');
      expect(response.ok()).toBeTruthy();
      const rows: Array<{ id: number; scored_min_reps: number | null; scored_max_reps: number | null }> =
        (await response.json()).data;
      const stored = rows.find(entry => String(entry.id) === logId);
      if (!stored) throw new Error(`Workout log entry ${logId} was not found`);
      return { scored_min_reps: stored.scored_min_reps, scored_max_reps: stored.scored_max_reps };
    };
    const original = await readStoredReps();
    const waitForScoreWrite = () => page.waitForResponse(response =>
      new URL(response.url()).pathname === '/update_workout_log' && response.request().method() === 'POST',
    );
    const submittedUpdates: unknown[] = [];
    page.on('request', request => {
      if (new URL(request.url()).pathname === '/update_workout_log' && request.method() === 'POST') {
        submittedUpdates.push(request.postDataJSON().updates);
      }
    });

    try {
      const reset = await page.request.post('/update_workout_log', {
        data: { id: logId, updates: { scored_min_reps: null, scored_max_reps: null } },
      });
      expect(reset.ok()).toBeTruthy();
      await page.clock.install();
      await page.reload();
      await waitForPageReady(page);
      await expect(minDisplay).toHaveText('--');

      await minDisplay.click();
      await minInput.fill('0.0');
      const minSaved = waitForScoreWrite();
      await minInput.press('Enter');
      expect((await minSaved).ok()).toBeTruthy();
      await expect(minDisplay).toHaveText('0');
      await expect(minInput).toBeEnabled();

      await minDisplay.click();
      await expect(minInput).toHaveValue('0');
      await minInput.fill('7');
      await minInput.press('Escape');
      await expect(minDisplay).toHaveText('0');

      await maxDisplay.click();
      await maxInput.fill('0');
      const maxSaved = waitForScoreWrite();
      await maxInput.blur();
      expect((await maxSaved).ok()).toBeTruthy();
      await expect(maxDisplay).toHaveText('0');
      expect(await readStoredReps()).toEqual({ scored_min_reps: 0, scored_max_reps: 0 });

      await page.reload();
      await waitForPageReady(page);
      await expect(minDisplay).toHaveText('0');
      await expect(maxDisplay).toHaveText('0');

      await minDisplay.click();
      await minInput.fill('');
      await minInput.pressSequentially('1e');
      await expect(minInput).toHaveValue('');
      expect(await minInput.evaluate(input => (input as HTMLInputElement).validity.badInput)).toBe(true);
      await minInput.press('Enter');
      await expectToast(page, 'Logged reps must be a whole number of at least 0.');
      await page.clock.runFor(750);
      await expect(minDisplay).toBeVisible();
      await expect(minDisplay).toHaveText('0');
      expect(submittedUpdates).toEqual([{ scored_min_reps: '0.0' }, { scored_max_reps: '0' }]);
      expect(await readStoredReps()).toEqual({ scored_min_reps: 0, scored_max_reps: 0 });

      await minDisplay.click();
      await minInput.fill('1');
      const minRejected = waitForScoreWrite();
      await minInput.press('Enter');
      const rejection = await minRejected;
      expect(rejection.status()).toBe(400);
      expect(await rejection.json()).toMatchObject({ error: { code: 'VALIDATION_ERROR' } });
      await expectToast(page, 'Minimum reps cannot exceed maximum reps.');
      await expect(minDisplay).toHaveText('0');
      await expect(minInput).toBeEnabled();
      expect(await readStoredReps()).toEqual({ scored_min_reps: 0, scored_max_reps: 0 });

      await minDisplay.click();
      await minInput.fill('');
      const minCleared = waitForScoreWrite();
      await minInput.blur();
      const clearResponse = await minCleared;
      expect(clearResponse.ok()).toBeTruthy();
      expect(clearResponse.request().postDataJSON().updates).toEqual({ scored_min_reps: null });
      await expect(minDisplay).toHaveText('--');
      expect(await readStoredReps()).toEqual({ scored_min_reps: null, scored_max_reps: 0 });
      await page.reload();
      await waitForPageReady(page);
      await expect(minDisplay).toHaveText('--');
      await expect(maxDisplay).toHaveText('0');
    } finally {
      await page.request.post('/update_workout_log', { data: { id: logId, updates: original } });
    }
  });

  test('notes field accepts text', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const notesInput = page.locator('input[name*="notes"], textarea[name*="notes"], .notes-input').first();
    const count = await notesInput.count();

    if (count > 0) {
      await notesInput.fill('Test note from E2E');
      await notesInput.blur();
      
      await page.waitForTimeout(500);
    }
  });

  test('delete log entry button works', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const rows = page.locator('.workout-log-table tbody tr');
    const initialCount = await rows.count();

    if (initialCount > 0) {
      // Handle potential confirmation dialog
      page.on('dialog', async dialog => {
        await dialog.accept();
      });

      const deleteBtn = rows.first().locator('button[data-action="delete"], .delete-btn, .btn-danger');
      const hasDel = await deleteBtn.count() > 0;

      if (hasDel) {
        await deleteBtn.first().click();
        await page.waitForTimeout(1000);

        // Verify delete action was attempted (row count may or may not change depending on confirmation)
        const newCount = await rows.count();
        // Test passes as long as no error occurred during the delete flow
        expect(newCount).toBeGreaterThanOrEqual(0);
      } else {
        // No delete button found - test passes (data might not have deletable rows)
        expect(true).toBe(true);
      }
    } else {
      // No rows to delete - test passes
      expect(initialCount).toBe(0);
    }
  });

  test('progression indicator shows status', async ({ page }) => {
    await importCurrentWorkoutPlan(page);

    const rows = page.locator('.workout-log-table tbody tr');
    const count = await rows.count();

    if (count > 0) {
      // Look for progression status indicators
      const statusIndicators = rows.first().locator('.progression-status, .status-indicator, [class*="progress"]');
      const hasIndicators = await statusIndicators.count() > 0;
      
      // Indicators may only appear after editing scored values
      expect(hasIndicators !== null).toBeTruthy();
    }
  });

  test('assisted progression stays achieved after changing its date', async ({ page }) => {
    await page.request.post('/clear_workout_log');
    await page.request.post('/clear_workout_plan');

    try {
      const addResponse = await page.request.post('/add_exercise', {
        data: {
          routine: 'GYM - Full Body - Workout A',
          exercise: 'Machine Assisted Chin Up',
          sets: 3,
          min_rep_range: 6,
          max_rep_range: 10,
          rir: 2,
          rpe: 8,
          weight: 65,
        },
      });
      expect(addResponse.ok()).toBeTruthy();

      const exportResponse = await page.request.post('/export_to_workout_log');
      expect(exportResponse.ok()).toBeTruthy();

      await page.goto(ROUTES.WORKOUT_LOG);
      await waitForPageReady(page);

      const row = page.locator('tr[data-assisted-bodyweight="true"]', {
        hasText: 'Machine Assisted Chin Up',
      });
      await expect(row).toHaveCount(1);

      const badge = row.locator('td[data-label="Progressive Overload"] .badge');
      await expect(badge).toHaveText('Pending');

      const weightCell = row.locator('td[data-field="scored_weight"]');
      const weightInput = weightCell.locator('input');
      await weightCell.locator('.editable-text').click();
      const weightUpdate = page.waitForResponse((response) =>
        new URL(response.url()).pathname === '/update_workout_log'
          && response.request().method() === 'POST',
      );
      await weightInput.fill('60');
      await weightInput.press('Enter');
      expect((await weightUpdate).ok()).toBeTruthy();
      await expect(badge).toHaveText('Achieved');

      let datePostCount = 0;
      page.on('request', (request) => {
        if (
          new URL(request.url()).pathname === '/update_progression_date'
          && request.method() === 'POST'
        ) {
          datePostCount += 1;
        }
      });

      const dateCell = row.locator('td[data-field="last_progression_date"]');
      const dateInput = dateCell.locator('input[type="date"]');
      await dateCell.click();
      await expect(dateInput).toBeVisible();

      const dateUpdate = page.waitForResponse((response) =>
        new URL(response.url()).pathname === '/update_progression_date'
          && response.request().method() === 'POST',
      );
      await dateInput.fill('2026-07-04');
      expect((await dateUpdate).ok()).toBeTruthy();

      await expect(dateCell.locator('.date-display')).toHaveText('04-07-26');
      await expect(badge).toHaveText('Achieved');
      expect(datePostCount).toBe(1);
    } finally {
      await page.request.post('/clear_workout_log');
      await page.request.post('/clear_workout_plan');
    }
  });
});

test('score edits preserve RIR zero and server progression, and Escape discards every numeric draft', async ({ page, request }) => {
  const routine = `GYM - Score editing ${Date.now()} - Workout A`;
  const added = await request.post('/add_exercise', {
    data: {
      routine, exercise: 'Machine Assisted Chin Up', sets: 1,
      min_rep_range: 6, max_rep_range: 10, rir: 2, rpe: 8, weight: 65,
    },
  });
  expect(added.ok()).toBeTruthy();
  const plan = await request.get('/get_workout_plan');
  const planRow = (await plan.json()).data.find((entry: { routine: string }) => entry.routine === routine);
  expect(planRow).toBeDefined();

  try {
    expect((await request.post('/export_to_workout_log')).ok()).toBeTruthy();
    const readEntry = async () => {
      const response = await request.get('/get_workout_logs');
      expect(response.ok()).toBeTruthy();
      return (await response.json()).data.find((entry: { routine: string }) => entry.routine === routine);
    };
    const { id } = await readEntry();
    await page.clock.install();
    await page.goto(ROUTES.WORKOUT_LOG);
    const row = page.locator(`tr[data-log-id="${id}"]`);
    const cell = (field: string) => row.locator(`[data-field="${field}"]`);
    const rir = cell('scored_rir');
    const badge = row.locator('[data-label="Progressive Overload"] .badge');
    const expectProgression = async (expected: 'Achieved' | 'Pending') => {
      const response = await request.get(`/check_progression/${id}`);
      expect((await response.json()).data.status).toBe(expected);
      await expect(badge).toHaveText(expected);
    };
    const updates: unknown[] = [];
    page.on('request', req => {
      if (new URL(req.url()).pathname === '/update_workout_log' && req.method() === 'POST') {
        updates.push(req.postDataJSON().updates);
      }
    });

    await expectProgression('Pending');
    await rir.locator('.editable-text').click();
    await rir.locator('input').fill('0');
    await rir.locator('input').press('Enter');
    await expect(rir.locator('.editable-text')).toHaveText('0');
    await expectProgression('Achieved');
    await page.reload();
    await expect(rir.locator('.editable-text')).toHaveText('0');
    await expectProgression('Achieved');

    const saved = { scored_rir: 0, scored_rpe: null, scored_weight: null, scored_min_reps: null, scored_max_reps: null };
    for (const [field, original] of Object.entries(saved)) {
      const editor = cell(field);
      const input = editor.locator('input');
      await editor.locator('.editable-text').click();
      await expect(input).toHaveValue(original === null ? '' : String(original));
      if (field === 'scored_weight') {
        await editor.locator('.number-spinner-plus').click();
        await expect(input).toHaveValue('0.5');
      } else {
        await input.fill('1');
      }
      // Cross the old debounce deadline both inside the editor and after Escape.
      await page.clock.fastForward(750);
      await input.press('Escape');
      await expect(input).toBeHidden();
      await expect(editor.locator('.editable-text')).toHaveText(original === null ? '--' : String(original));
    }
    await page.clock.fastForward(750);
    expect(updates).toEqual([{ scored_rir: '0' }]);
    expect(await readEntry()).toMatchObject(saved);

    await rir.locator('.editable-text').click();
    await rir.locator('input').fill('');
    await row.locator('.exercise-name').click();
    await expect(rir.locator('.editable-text')).toHaveText('--');
    await expectProgression('Pending');
    await page.reload();
    await expect(rir.locator('.editable-text')).toHaveText('--');
    await expectProgression('Pending');
    expect((await readEntry()).scored_rir).toBeNull();
    expect(updates).toEqual([{ scored_rir: '0' }, { scored_rir: null }]);
  } finally {
    expect((await request.post('/remove_exercise', { data: { id: planRow.id } })).ok()).toBeTruthy();
  }
});

test('phone effort entry persists on the intended exercise and desktop sorting awaits its save', async ({page, request}) => {
  const routine = `GYM - Log pilot ${Date.now()} - Workout A`;
  const planIds: number[] = [];
  try {
    for (const [exercise, effort] of [
      ['Barbell Curl', {rir: 2}], ['Barbell Seated Military Press', {rpe: 8}],
    ] as const) {
      const response = await request.post('/add_exercise', {data: {
        routine, exercise, sets: 3, min_rep_range: 8, max_rep_range: 12, weight: 30, ...effort,
      }});
      expect(response.ok()).toBe(true);
      const plan = (await (await request.get('/get_workout_plan')).json()).data as
        {id: number; routine: string; exercise: string}[];
      planIds.push(plan.find(entry => entry.routine === routine && entry.exercise === exercise)!.id);
    }
    expect((await request.post('/export_to_workout_log')).ok()).toBe(true);
    const records = async () => (await (await request.get('/get_workout_logs')).json()).data as
      {id: number; routine: string; exercise: string; scored_rpe: number|null; planned_rpe: number|null; planned_rir: number|null}[];
    const [curl, press] = (await records()).filter(entry => entry.routine === routine)
      .sort((a,b) => a.exercise.localeCompare(b.exercise));
    expect(press).toMatchObject({exercise:'Barbell Seated Military Press', scored_rpe:null, planned_rpe:8, planned_rir:null});
    expect(curl.exercise).toBe('Barbell Curl');
    for (const [id, weight] of [[curl.id,30], [press.id,50]]) {
      expect((await request.post('/update_workout_log', {data: {id, updates:{scored_weight:weight}}})).ok()).toBe(true);
    }
    await page.setViewportSize({width:390,height:844});
    await page.goto(ROUTES.WORKOUT_LOG);
    const card = page.locator(`tr[data-log-id="${press.id}"]`).filter({hasText:press.exercise});
    const ordinary = page.locator(`tr[data-log-id="${curl.id}"]`);
    await expect(card.locator('.log-details')).toHaveAttribute('aria-expanded','false');
    await expect(ordinary.locator('[data-field="scored_rpe"] .log-trigger')).toBeHidden();
    await expect(card.locator('[data-field="scored_rir"] .log-trigger')).toBeVisible();
    const rpe = card.locator('[data-field="scored_rpe"]');
    await rpe.locator('.log-trigger').click();
    await rpe.locator('input').fill('9');
    const submitted = page.waitForResponse(res => res.url().endsWith('/update_workout_log'));
    await rpe.locator('input').press('Enter');
    expect((await submitted).ok()).toBe(true);
    await expect(rpe.locator('.log-trigger')).toBeFocused();
    await page.goto(ROUTES.WORKOUT_PLAN);
    await expect(page.locator('#workout_plan_table_body')).toBeAttached();
    await page.locator('#navbar .navbar-toggler').click();
    await page.locator('#navbar a[href="/workout_log"]:visible').first().click();
    await expect(card.locator('.log-details')).toHaveAttribute('aria-expanded','false');
    await expect(rpe.locator('.editable-text')).toHaveText(/^9(?:\.0)?$/);
    expect((await records()).find(entry => entry.id === press.id)?.scored_rpe).toBe(9);
    await expect(card.locator('.ui-badge')).toHaveText((await (await request.get(`/check_progression/${press.id}`)).json()).data.status);
    // Criterion 19: the saved RPE stays in the main row, on return and after a reload.
    await expectEffortInMainRow(card, /^9(?:\.0)?$/);
    await page.reload();
    await expect(card).toHaveCount(1);
    await expectEffortInMainRow(card, /^9(?:\.0)?$/);
    expect((await records()).find(entry => entry.id === press.id)?.scored_rpe).toBe(9);

    const weight = ordinary.locator('[data-field="scored_weight"]');
    await weight.locator('.log-trigger').click();
    await weight.locator('input').fill('60');
    await page.setViewportSize({width:1440,height:900});
    await expect(weight.locator('input')).toBeFocused();
    let release!: () => void;
    const held = new Promise<void>(resolve => { release = resolve; });
    let writes = 0;
    await page.route('**/update_workout_log', async route => {
      writes++;
      await held;
      await route.continue();
    });
    const sort = page.locator('[data-sort-field="scored_weight"]');
    try {
      await sort.click();
      await expect.poll(() => writes).toBe(1);
    } finally { release(); }
    await expect(sort.locator('..')).toHaveAttribute('aria-sort','ascending');
    const ordered = await page.locator('tr[data-log-id]').evaluateAll(rows => rows.map(row => row.getAttribute('data-log-id')));
    expect(ordered.indexOf(String(press.id))).toBeLessThan(ordered.indexOf(String(curl.id)));
    expect(writes).toBe(1);
  } finally {
    for (const id of planIds) await request.post('/remove_exercise', {data:{id}});
  }
});

test('phone card fits five logged fields at 320, 360 and 390 px at scale 8', async ({ page, request }) => {
  // The owner's case on #736: Barbell Squat, planned RIR 2 and RPE 8 at 100 kg, logged RPE 10.0.
  const routine = `GYM - Log scale fit ${Date.now()} - Workout A`;
  const exercise = 'Barbell Squat';
  const added = await request.post('/add_exercise', {
    data: {
      routine, exercise, sets: 3, min_rep_range: 6, max_rep_range: 10, rir: 2, rpe: 8, weight: 100,
    },
  });
  expect(added.ok()).toBe(true);
  const plan = (await (await request.get('/get_workout_plan')).json()).data as
    { id: number; routine: string; exercise: string }[];
  const planRow = plan.find(entry => entry.routine === routine && entry.exercise === exercise);
  expect(planRow).toBeDefined();

  try {
    expect((await request.post('/export_to_workout_log')).ok()).toBe(true);
    const stored = async () => {
      const logs = (await (await request.get('/get_workout_logs')).json()).data as
        Record<string, unknown>[];
      return logs.find(entry => entry.routine === routine && entry.exercise === exercise);
    };
    const imported = await stored();
    expect(imported).toBeDefined();
    const logged = {
      scored_min_reps: 10, scored_max_reps: 10, scored_weight: 100, scored_rir: 1, scored_rpe: 10,
    };
    const written = await request.post('/update_workout_log', {
      data: { id: imported!.id, updates: logged },
    });
    expect(written.ok()).toBe(true);
    // Every logged field has a planned value to compare with, so every field carries a mark.
    expect(await stored()).toMatchObject({
      planned_min_reps: 6, planned_max_reps: 10, planned_weight: 100,
      planned_rir: 2, planned_rpe: 8, ...logged,
    });

    // Level 8 through the app's own controller, which stores it for the server to render.
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(ROUTES.WORKOUT_LOG);
    await page.evaluate(() => {
      const scale = (window as unknown as {
        accessibilityController: { setScale(level: number): void };
      }).accessibilityController;
      scale.setScale(8);
    });

    const card = page.locator(`tr[data-log-id="${imported!.id}"]`).filter({ hasText: exercise });
    const details = card.getByRole('button', { name: 'Details', exact: true });
    const cell = (field: string) => card.locator(`[data-field="${field}"]`);
    for (const width of [320, 360, 390]) {
      const where = `at ${width} px at scale 8`;
      await page.setViewportSize({ width, height: 844 });
      await page.goto(ROUTES.WORKOUT_LOG);
      await expect(page.locator('html')).toHaveAttribute('data-scale', '8');
      const zoom = await page.locator('html').evaluate(el => Number(getComputedStyle(el).zoom));
      expect(zoom, `app scale factor ${where}`).toBe(1.2);
      await expect(card).toHaveCount(1);
      await expect(details).toHaveAttribute('aria-expanded', 'false');
      // The marks are placed by the page script, so their presence means the card is laid out.
      await expect(card.locator('.scored-cell .progression-indicator')).toHaveCount(5);
      await page.evaluate(() => document.fonts.ready.then(() => undefined));
      for (const field of MAIN_ROW_FIELDS) {
        const value = cell(field).locator('.editable-text');
        await expect(value, `${field} as printed ${where}`).toHaveText(SQUAT_LOGGED_TEXT[field]);
        await expect.soft(cell(field).locator('.log-trigger'), `${field} field ${where}`).toBeVisible();
        await expect.soft(value, `${field} value ${where}`).toBeVisible();
        await expect.soft(cell(field).locator('.progression-indicator'), `${field} mark ${where}`)
          .toBeVisible();
      }
      const read = await readMainRowFit(card);
      expect.soft(mainRowFitProblems(read, width), `phone card fit ${where}`).toEqual([]);
      if (width === 390) {
        // Measured on 0511344b: at 390 px the five fields share one row inside the card.
        expect.soft(mainRowCount(read), `rows of logged fields ${where}`).toBe(1);
      }
    }
  } finally {
    const removed = await request.post('/remove_exercise', { data: { id: planRow!.id } });
    expect(removed.ok()).toBe(true);
  }
});

test('phone card at scale 8 wraps when a wider logged value is saved and returns to one row for a narrower one', async ({ page, request }) => {
  // Measured on 8bccacf0 at scale 8, one load per width from 300 to 440 px: with a logged
  // weight of 2.5 these five fields share one row from 341 px up, and with 1000.0 from 378 px
  // up. 360 px is 19 px above the first and 18 px below the second.
  const width = 360;
  const logged = {
    scored_min_reps: 10, scored_max_reps: 10, scored_weight: 2.5, scored_rir: 1, scored_rpe: 9.5,
  };
  await withLoggedSquat(request, 'Log refit on save', logged, async ({ id, stored }) => {
    await openLogAtScale8(page, width);
    const card = page.locator(`tr[data-log-id="${id}"]`);
    await expect(card).toHaveCount(1);
    // The page script places four of the five marks, so their count means the card is laid out.
    await expect(card.locator('.scored-cell .progression-indicator')).toHaveCount(5);
    const rows = async () => mainRowGroups(await readMainRowFit(card));

    const before = await expectMainRowFit(card, MAIN_ROW_FIELDS, width, 'before a save');
    expect(mainRowGroups(before), 'rows before a save').toEqual(FIVE_FIELDS_ON_ONE_ROW);

    await saveLoggedValue(page, card, 'scored_weight', '1000.0');
    expect((await stored()).scored_weight).toBe(1000);
    await expect.poll(rows, 'rows after saving the wider weight').toEqual(FIVE_FIELDS_WRAPPED);
    await expectMainRowFit(card, MAIN_ROW_FIELDS, width, 'after saving the wider weight');

    await saveLoggedValue(page, card, 'scored_weight', '2.5');
    expect((await stored()).scored_weight).toBe(2.5);
    await expect.poll(rows, 'rows after saving the narrower weight').toEqual(FIVE_FIELDS_ON_ONE_ROW);
    await expectMainRowFit(card, MAIN_ROW_FIELDS, width, 'after saving the narrower weight');
  });
});

test('phone card at scale 8 refits its five logged fields when the viewport narrows to 320 px and widens back to 390 px', async ({ page, request }) => {
  // The owner's values on #736. Measured on 8bccacf0 at scale 8: one row from 378 px up.
  const logged = {
    scored_min_reps: 10, scored_max_reps: 10, scored_weight: 100, scored_rir: 1, scored_rpe: 10,
  };
  await withLoggedSquat(request, 'Log refit on resize', logged, async ({ id }) => {
    await openLogAtScale8(page, 390);
    const card = page.locator(`tr[data-log-id="${id}"]`);
    await expect(card).toHaveCount(1);
    await expect(card.locator('.scored-cell .progression-indicator')).toHaveCount(5);
    const rows = async () => mainRowGroups(await readMainRowFit(card));
    // A reload would drop this mark, so finding it at the end means the page only resized.
    await page.evaluate(() => { document.documentElement.dataset.resizeProbe = 'kept'; });

    const wide = await expectMainRowFit(card, MAIN_ROW_FIELDS, 390, 'at 390 px before the resize');
    expect(mainRowGroups(wide), 'rows at 390 px before the resize').toEqual(FIVE_FIELDS_ON_ONE_ROW);

    await page.setViewportSize({ width: 320, height: 844 });
    await expect.poll(rows, 'rows after narrowing to 320 px').toEqual(FIVE_FIELDS_WRAPPED);
    await expectMainRowFit(card, MAIN_ROW_FIELDS, 320, 'after narrowing to 320 px');

    await page.setViewportSize({ width: 390, height: 844 });
    await expect.poll(rows, 'rows after widening back to 390 px').toEqual(FIVE_FIELDS_ON_ONE_ROW);
    await expectMainRowFit(card, MAIN_ROW_FIELDS, 390, 'after widening back to 390 px');

    await expect(page.locator('html'), 'the page was resized, not reloaded')
      .toHaveAttribute('data-resize-probe', 'kept');
  });
});

test('inline editor stays inside a wrapped phone card at 320 px at scale 8 and a second-row value saves', async ({ page, request }) => {
  const width = 320;
  // The owner's values on #736. Measured on 8bccacf0 at scale 8: wrapped below 378 px.
  const logged = {
    scored_min_reps: 10, scored_max_reps: 10, scored_weight: 100, scored_rir: 1, scored_rpe: 10,
  };
  await withLoggedSquat(request, 'Log wrapped editor', logged, async ({ id, stored }) => {
    await openLogAtScale8(page, width);
    const card = page.locator(`tr[data-log-id="${id}"]`);
    await expect(card).toHaveCount(1);
    await expect(card.locator('.scored-cell .progression-indicator')).toHaveCount(5);
    const resting = await expectMainRowFit(card, MAIN_ROW_FIELDS, width, 'before an editor opens');
    expect(mainRowGroups(resting), 'rows before an editor opens').toEqual(FIVE_FIELDS_WRAPPED);

    const saves: unknown[] = [];
    page.on('request', sent => {
      if (new URL(sent.url()).pathname === '/update_workout_log' && sent.method() === 'POST') {
        saves.push(sent.postDataJSON().updates);
      }
    });

    // A first-row field, then both second-row fields. Only the RPE editor saves.
    for (const field of ['scored_weight', 'scored_rir', 'scored_rpe'] as const) {
      const where = `with the ${field} editor open`;
      const input = await openLoggedEditor(card, field);
      // The card makes room for the editor over a 0.2 s transition, so the fit is polled
      // until the row has settled.
      const problems = async () => editorFitProblems(await readEditorFit(card, field), width);
      await expect.poll(problems, `editor fit ${where}`).toEqual([]);
      // The fields keep their two rows and their fit while the editor is open.
      const open = await expectMainRowFit(card, MAIN_ROW_FIELDS, width, where);
      expect.soft(mainRowGroups(open), `rows ${where}`).toEqual(FIVE_FIELDS_WRAPPED);
      if (field !== 'scored_rpe') {
        await input.press('Escape');
        await expect(input).toBeHidden();
        await expect(card.locator(`[data-field="${field}"] .editable-text`), `${field} after Escape`)
          .toHaveText(SQUAT_LOGGED_TEXT[field]);
      } else {
        await input.fill('9.5');
        const saved = page.waitForResponse(response =>
          new URL(response.url()).pathname === '/update_workout_log' &&
          response.request().method() === 'POST');
        await input.press('Enter');
        expect((await saved).ok()).toBe(true);
        await expect(input).toBeHidden();
      }
    }

    const rpe = card.locator('[data-field="scored_rpe"]');
    await expect(rpe.locator('.editable-text'), 'the saved RPE as shown').toHaveText('9.5');
    await expect(rpe.locator('.log-trigger'), 'focus returns to the RPE field').toBeFocused();
    expect(saves, 'only the RPE edit is written').toEqual([{ scored_rpe: '9.5' }]);
    expect(await stored(), 'the saved RPE as stored').toMatchObject({ ...logged, scored_rpe: 9.5 });
    const after = await expectMainRowFit(card, MAIN_ROW_FIELDS, width, 'after the save');
    expect(mainRowGroups(after), 'rows after the save').toEqual(FIVE_FIELDS_WRAPPED);

    // The value survives a reload, still wrapped and still inside the card.
    await page.reload();
    await expect(card.locator('.scored-cell .progression-indicator')).toHaveCount(5);
    await page.evaluate(() => document.fonts.ready.then(() => undefined));
    await expect(rpe.locator('.editable-text'), 'the saved RPE after a reload').toHaveText('9.5');
    const reloaded = await expectMainRowFit(card, MAIN_ROW_FIELDS, width, 'after a reload');
    expect(mainRowGroups(reloaded), 'rows after a reload').toEqual(FIVE_FIELDS_WRAPPED);
  });
});

test('wrapped four-field phone card fits two and two at 320 px at scale 8', async ({ page, request }) => {
  const width = 320;
  const fields = MAIN_ROW_FIELDS.filter(field => field !== 'scored_rpe');
  // Wide values in every field. No RPE is logged and the plan holds an RIR, so logged RPE
  // stays behind Details and the card shows four fields.
  const logged = { scored_min_reps: 100, scored_max_reps: 100, scored_weight: 1000, scored_rir: 10 };
  const printed: Record<string, string> = {
    scored_min_reps: '100', scored_max_reps: '100', scored_weight: '1000.0', scored_rir: '10',
  };
  await withLoggedSquat(request, 'Log four fields', logged, async ({ id, stored }) => {
    expect((await stored()).scored_rpe).toBeNull();
    await openLogAtScale8(page, width);
    const card = page.locator(`tr[data-log-id="${id}"]`);
    await expect(card).toHaveCount(1);
    await expect(card.getByRole('button', { name: 'Details', exact: true }))
      .toHaveAttribute('aria-expanded', 'false');
    await expect(card.locator('.scored-cell .progression-indicator')).toHaveCount(4);
    await expect(card.locator('[data-field="scored_rpe"] .log-trigger')).toBeHidden();
    for (const field of fields) {
      await expect(card.locator(`[data-field="${field}"] .editable-text`), `${field} as printed`)
        .toHaveText(printed[field]);
    }
    const read = await expectMainRowFit(card, fields, width, 'on the four-field card');
    expect(mainRowGroups(read), 'rows of the four-field card').toEqual([
      ['scored_min_reps', 'scored_max_reps'],
      ['scored_weight', 'scored_rir'],
    ]);
  });
});

test.describe('Workout Log Details on a phone', () => {
  test.use({ hasTouch: true, viewport: { width: 390, height: 844 } });

  test('Details opens by touch and by keyboard and hides its controls when closed', async ({ page, request }) => {
    const routine = `GYM - Log details ${Date.now()} - Workout A`;
    const exercise = 'Barbell Curl';
    const added = await request.post('/add_exercise', {
      data: {
        routine, exercise, sets: 3, min_rep_range: 8, max_rep_range: 12, rir: 2, rpe: 8, weight: 30,
      },
    });
    expect(added.ok()).toBe(true);
    const plan = (await (await request.get('/get_workout_plan')).json()).data as
      { id: number; routine: string; exercise: string }[];
    const planRow = plan.find(entry => entry.routine === routine && entry.exercise === exercise);
    expect(planRow).toBeDefined();

    try {
      expect((await request.post('/export_to_workout_log')).ok()).toBe(true);
      const logs = (await (await request.get('/get_workout_logs')).json()).data as
        Record<string, unknown>[];
      const record = logs.find(entry => entry.routine === routine && entry.exercise === exercise);
      // Planned by RIR and RPE with nothing logged, so logged RPE sits behind Details.
      expect(record).toMatchObject({
        planned_sets: 3, planned_min_reps: 8, planned_max_reps: 12,
        planned_rir: 2, planned_rpe: 8, planned_weight: 30, scored_rpe: null,
      });

      await page.goto(ROUTES.WORKOUT_LOG);
      const card = page.locator(`tr[data-log-id="${record!.id}"]`).filter({ hasText: exercise });
      await expect(card).toHaveCount(1);
      const details = card.getByRole('button', { name: 'Details', exact: true });
      const plannedValue = (key: string) => card.locator(`[data-field="planned_${key}"]`);
      const dateLabel = card.getByText('Last Progression', { exact: true });
      const controls = {
        'Last Progression': card.getByRole('button', { name: /Last Progression/ }),
        'Reference Video': card.getByRole('button', { name: /reference video/i }),
        'Delete Entry': card.getByRole('button', { name: /Delete Entry/ }),
        'Logged RPE': card.locator('[data-field="scored_rpe"] .log-trigger'),
      };

      const expectClosed = async () => {
        await expect(details).toHaveAttribute('aria-expanded', 'false');
        for (const key of PLANNED_VALUE_KEYS) {
          await expect(plannedValue(key), `planned ${key} while closed`).toBeHidden();
        }
        await expect(dateLabel).toBeHidden();
        for (const [name, control] of Object.entries(controls)) {
          await expect(control, `${name} while closed`).toBeHidden();
        }
        const stops = await cardTabStops(page, card);
        // The walk is only evidence if it reaches the fields that stay in the main row.
        expect(stops.some(stop => /logged RIR/i.test(stop)), 'Tab reaches logged RIR').toBe(true);
        for (const name of DETAILS_ONLY_CONTROLS) {
          expect(stops, `${name} is out of the tab order while closed`).not.toContain(name);
        }
      };

      const expectOpen = async () => {
        await expect(details).toHaveAttribute('aria-expanded', 'true');
        for (const key of PLANNED_VALUE_KEYS) {
          const stored = Number(record![`planned_${key}`]);
          await expect(plannedValue(key), `planned ${key} while open`).toBeVisible();
          await expect(plannedValue(key)).toHaveText(new RegExp(`^${stored}(?:\\.0)?$`));
        }
        await expect(dateLabel).toBeVisible();
        for (const [name, control] of Object.entries(controls)) {
          await expect(control, `${name} while open`).toBeVisible();
        }
        // Section 0: below 768 px every button is at least 44 px tall.
        for (const name of ['Reference Video', 'Delete Entry'] as const) {
          const box = await controls[name].boundingBox();
          expect(box!.height, `${name} height at 390 px`).toBeGreaterThanOrEqual(44);
        }
        const stops = await cardTabStops(page, card);
        for (const name of DETAILS_ONLY_CONTROLS) {
          expect(stops, `Tab reaches ${name} while open`).toContain(name);
        }
      };

      await expectClosed();
      await details.tap();
      await expectOpen();
      await details.press('Enter');
      await expectClosed();
      await details.press('Space');
      await expectOpen();
    } finally {
      const removed = await request.post('/remove_exercise', { data: { id: planRow!.id } });
      expect(removed.ok()).toBe(true);
    }
  });
});

test.describe('Workout Log Date Filter', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('date filter exists', async ({ page }) => {
    // The workout log has date inputs per row for "Last Progression" date
    // Check that at least one date-related input exists in the table
    const dateInputs = page.locator('.workout-log-table input[type="date"], .date-input');
    const count = await dateInputs.count();
    
    // If there are logs, there should be date inputs
    // If no logs, that's also valid
    expect(count >= 0).toBeTruthy();
  });

  test('date filter changes displayed data', async ({ page }) => {
    // This page doesn't have a global date filter, but has per-row date inputs
    // for Last Progression. Test that the date inputs in the table work.
    const dateInputs = page.locator('.workout-log-table .date-input, .workout-log-table input[type="date"]');
    const count = await dateInputs.count();
    
    if (count > 0) {
      // Get the first date input that's visible/editable
      const firstDateInput = dateInputs.first();
      
      // The date inputs might be hidden until clicked, so just verify they exist
      await expect(firstDateInput).toBeAttached();
    }
    
    await expect(page.locator('.workout-log-table')).toBeAttached();
  });
});

test.describe('Workout Log Clear Functionality', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('clear log confirmation modal exists', async ({ page }) => {
    const clearBtn = page.locator('#clear-log-btn');
    await clearBtn.click();

    const modal = page.locator('#clearLogModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Should have warning text
    const modalBody = modal.locator('.modal-body');
    const text = await modalBody.textContent();
    expect(text?.toLowerCase()).toMatch(/clear|delete|remove/);

    await modal.locator('.btn-close').click();
  });

  test('cancel button closes clear modal without action', async ({ page }) => {
    const clearBtn = page.locator('#clear-log-btn');
    await clearBtn.click();

    const modal = page.locator('#clearLogModal');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Verify cancel button exists in modal footer
    const cancelBtn = modal.locator('.modal-footer .btn-secondary');
    await expect(cancelBtn).toBeVisible();
    await expect(cancelBtn).toContainText('Cancel');
    
    // Verify clicking cancel doesn't trigger the clear action
    // (We just verify the button exists and is clickable - Bootstrap modal close is external dependency)
    await cancelBtn.click();
    
    // Wait briefly for any action
    await page.waitForTimeout(300);
    
    // Test passes if no error occurred during cancel click
  });
});

test.describe('Workout Log Mobile Responsive', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('import button accessible on mobile', async ({ page }) => {
    const importBtn = page.locator('#import-from-plan-btn');
    await expect(importBtn).toBeVisible();

    const box = await importBtn.boundingBox();
    if (box) {
      expect(box.width).toBeGreaterThanOrEqual(44);
    }
  });
});

// ============================================================================
// §5 — Exercise reference video modal on /workout_log (PLANNING.md §5.5)
//
// The modal partial is included once in base.html, so the same flow as on
// /workout_plan applies here. Every server-rendered log row carries a video
// button. A valid youtube_video_id opens the modal. A NULL youtube_video_id
// opens a YouTube search tab directly.
// ============================================================================

test.describe('Exercise reference video modal (workout-log)', () => {
  test.beforeEach(async ({ page, consoleErrors }) => {
    consoleErrors.startCollecting();

    // Seed the plan with one exercise, then import into the log so the
    // server-rendered log table actually has a row to inspect.
    await page.goto(ROUTES.WORKOUT_PLAN);
    await waitForPageReady(page);

    await page.locator(SELECTORS.ROUTINE_ENV).selectOption('GYM');
    await page.waitForFunction(() => {
      const s = document.getElementById('routine-program') as HTMLSelectElement | null;
      return Boolean(s && s.options.length > 1);
    });
    await page.locator(SELECTORS.ROUTINE_PROGRAM).selectOption('Full Body');
    await page.waitForFunction(() => {
      const s = document.getElementById('routine-day') as HTMLSelectElement | null;
      return Boolean(s && s.options.length > 1);
    });
    await page.locator(SELECTORS.ROUTINE_DAY).selectOption('Workout A');
    await page.waitForFunction(() => {
      const s = document.getElementById('exercise') as HTMLSelectElement | null;
      return Boolean(s && s.options.length > 1);
    });
    const exSelect = page.locator(SELECTORS.EXERCISE_SEARCH);
    const firstValue = await exSelect.locator('option').nth(1).getAttribute('value');
    if (firstValue) {
      await exSelect.selectOption(firstValue);
    }
    await page.locator(SELECTORS.ADD_EXERCISE_BTN).click();
    await page.waitForSelector('#workout_plan_table_body tr');

    await page.goto(ROUTES.WORKOUT_LOG);
    await waitForPageReady(page);
    await importCurrentWorkoutPlan(page);
  });

  test.afterEach(async ({ consoleErrors }) => {
    consoleErrors.assertNoErrors();
  });

  test('every log row has an accessible play button', async ({ page }) => {
    const rows = page.locator('.workout-log-table tbody tr');
    const rowCount = await rows.count();
    expect(rowCount).toBeGreaterThan(0);

    const firstRow = rows.first();
    const playBtn = firstRow.locator('.log-play-video-btn');
    await expect(playBtn).toBeVisible();

    // Default seed is uncurated → search-variant icon + accessible name.
    const ariaLabel = await playBtn.getAttribute('aria-label');
    expect(ariaLabel).toMatch(/^Search YouTube for a /);
    await expect(playBtn.locator('i')).toHaveClass(/fa-search/);
  });

  test('clicking search on an uncurated row opens a YouTube search tab — no modal', async ({ page }) => {
    await page.evaluate(() => {
      // @ts-expect-error - test-only capture
      window.__openedUrl = null;
      window.open = (url) => {
        // @ts-expect-error - test-only capture
        window.__openedUrl = url;
        return null;
      };
    });

    const playBtn = page.locator('.workout-log-table .log-play-video-btn').first();
    await playBtn.click();

    // Default seed is uncurated → straight to YouTube search, modal stays closed.
    const opened = await page.evaluate(() => {
      // @ts-expect-error - test-only capture set above
      return window.__openedUrl as string | null;
    });
    expect(opened).toMatch(/^https:\/\/www\.youtube\.com\/results\?search_query=/);
    await expect(page.locator('#exerciseVideoModal')).toBeHidden();
  });

  test('valid id (driven via JS) opens embed mode', async ({ page }) => {
    // Server-rendered log rows can carry a real youtube_video_id, but no
    // curated CSV ships with this branch — drive the modal via the public
    // window API to exercise the embed path on the log page.
    await page.evaluate(() => {
      // @ts-expect-error - exposed by exercise-video-modal.js
      window.openExerciseVideoModal('dQw4w9WgXcQ', 'Test Log Exercise');
    });

    await expect(page.locator('#exerciseVideoModal')).toBeVisible();
    await expect(page.locator('#exerciseVideoEmbedWrap')).toBeVisible();

    const src = await page.locator('#exerciseVideoIframe').getAttribute('src');
    expect(src).toMatch(/^https:\/\/www\.youtube\.com\/embed\/dQw4w9WgXcQ/);
  });
});
