import type { Page, Response } from '@playwright/test';
import { expect } from './strict-fixtures';

export function summaryResponse(page: Page, path: string, mode: string) {
  return page.waitForResponse(response => {
    const url = new URL(response.url());
    return url.pathname === path && url.searchParams.get('contribution_mode') === mode &&
      response.request().headers()['x-requested-with'] === 'XMLHttpRequest';
  });
}

type SummaryData = {
  weekly_summary?: Volume[];
  session_summary?: Volume[];
  categories: {category: string; subcategory: string; total_exercises: number}[];
  isolated_muscles: {isolated_muscle: string; exercise_count: number; total_sets: number; total_reps: number; total_volume: number}[];
};

type Volume = {
  muscle_group: string; routine?: string; effective_sets: number; raw_sets: number;
  total_volume: number; frequency: number; warning_level?: string;
};

export async function summaryData(response: Response): Promise<SummaryData> {
  expect(response.ok()).toBe(true);
  return (await response.json()).data;
}

type Field = { name: string; value: string; numeric?: boolean; alternative?: string };
type RecordSample = { table: string; identity: string; fields: Field[] };

export function expectedRecords(data: SummaryData, weekly: boolean): RecordSample[] {
  const rows = weekly ? data.weekly_summary : data.session_summary;
  const muscle = rows!.find(r => r.muscle_group === 'Biceps')!;
  expect(muscle).toBeDefined();
  const category = data.categories.find(r => r.category === 'Mechanic' && r.subcategory === 'Compound')!;
  const isolated = data.isolated_muscles.find(r => r.isolated_muscle === 'lateral-head-triceps')!;
  expect(category).toMatchObject({total_exercises: 5});
  expect(isolated).toMatchObject({exercise_count: 1, total_sets: 3, total_reps: 30, total_volume: 1800});
  if (!weekly) expect(muscle).toMatchObject({routine: 'GYM - Full Body - Workout A', warning_level: 'ok'});
  expect(muscle.effective_sets).toBeLessThan(10);
  const fields: Field[] = [
    {name: 'Muscle Group', value: 'Biceps'},
    {name: 'Effective Sets', value: muscle.effective_sets.toFixed(1), numeric: true},
    {name: 'Raw Sets', value: muscle.raw_sets.toFixed(1), numeric: true},
  ];
  if (weekly) fields.push({name: 'Routines', value: String(muscle.frequency), numeric: true});
  else fields.unshift({name: 'Routine', value: muscle.routine!});
  fields.push({name: 'Total Volume', value: muscle.total_volume.toFixed(0), numeric: true},
    {name: weekly ? 'Volume Classification' : 'Volume Status', value: weekly ? 'Low Volume' : 'Low Volume OK'});
  return [
    {table: weekly ? '#weekly-summary-table' : '#session-summary-table', identity: 'Biceps', fields},
    {table: '#categories-table-body', identity: 'Compound', fields: [
      {name: 'Category', value: category.category}, {name: 'Subcategory', value: category.subcategory},
      {name: 'Total Exercises', value: String(category.total_exercises), numeric: true},
    ]},
    {table: 'table:has(th[data-label="Isolated Muscle"]) tbody, table[aria-label*="Isolated" i] tbody', identity: isolated.isolated_muscle,
      fields: [{name: 'Isolated Muscle', value: isolated.isolated_muscle, alternative:'Triceps'},
        {name: 'Exercise Count', value: String(isolated.exercise_count), numeric: true},
        {name: 'Total Sets', value: String(isolated.total_sets), numeric: true},
        {name: 'Total Reps', value: String(isolated.total_reps), numeric: true},
        {name: 'Total Volume', value: String(isolated.total_volume), numeric: true},
        {name: 'Volume Classification', value: 'Low Volume'}]},
  ];
}

/** Compare the value's painted text with the named card field or the actual column.
 * A td that still exists under display:none, or data-label with no painted label, cannot pass. */
export async function inspectRecords(page: Page, samples: RecordSample[], width: number) {
  return page.evaluate(({ samples, width }) => {
    const clean = (s: string | null | undefined) => (s ?? '').replace(/\s+/g, ' ').trim();
    const same = (s: string, value: string) => s === value ||
      (/^\d+(?:\.\d+)?$/.test(s) && /^\d+(?:\.\d+)?$/.test(value) && Number(s) === Number(value));
    const positive = (r: DOMRect) => r.width > 0 && r.height > 0;
    const inside = (a: DOMRect, b: DOMRect) => a.left >= b.left - 1 && a.right <= b.right + 1 &&
      a.top >= b.top - 1 && a.bottom <= b.bottom + 1;
    const paintedText = (element: Element) => {
      const walk = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
      const fragments = [];
      for (let node = walk.nextNode(); node; node = walk.nextNode()) {
        const value = clean(node.textContent);
        if (!value) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        const box = range.getBoundingClientRect();
        const style = getComputedStyle(node.parentElement!);
        if (positive(box) && style.visibility === 'visible' && style.opacity !== '0') {
          fragments.push({value, box, style});
        }
      }
      return fragments;
    };
    return samples.map(sample => {
      const tbody = document.querySelector(sample.table);
      const row = [...(tbody?.querySelectorAll('tr') ?? [])].find(tr =>
        [...tr.cells].some(cell => cell.getAttribute('data-raw-value') === sample.identity ||
          clean(cell.textContent).includes(sample.identity)));
      const headings = [...(tbody?.closest('table')?.querySelectorAll('th[scope="col"]') ?? [])];
      const rowBox = row?.getBoundingClientRect();
      const errors: string[] = [];
      sample.fields.forEach((field, index) => {
        const cell = row?.cells[index];
        if (!cell || !rowBox) { errors.push(field.name + ': missing cell'); return; }
        const box = cell.getBoundingClientRect();
        const fragments = paintedText(cell);
        const values = fragments.filter(f => f.value !== field.name);
        const text = values.map(f => f.value).join(' ');
        if (!positive(box) || !inside(box, rowBox) ||
            !(same(text,field.value) || (field.alternative && same(text,field.alternative))) ||
            !values.every(f => inside(f.box, box))) errors.push(field.name + ': invisible or wrong value');
        if (field.numeric && values.some(f => f.style.fontSize !== '14px' || !f.style.fontVariantNumeric.includes('tabular-nums'))) {
          errors.push(field.name + ': numeric type');
        }
        if (field.numeric && values.length && !['right', 'end'].includes(getComputedStyle(cell).textAlign) &&
            !values.every(f => ['right', 'end'].includes(f.style.textAlign))) errors.push(field.name + ': alignment');
        if (width < 768) {
          const before = getComputedStyle(cell, '::before');
          const pseudoLabel = clean(before.content).replace(/^["']|["']$/g, '');
          const shown = fragments.some(f => f.value === field.name && inside(f.box, box) && f.style.fontSize === '12px') ||
            (pseudoLabel === field.name && before.display !== 'none' && before.visibility === 'visible' &&
            before.fontSize === '12px' && positive(box));
          if (!shown) errors.push(field.name + ': unpainted card label');
          if (headings.some(h => positive(h.getBoundingClientRect()) && getComputedStyle(h).visibility === 'visible' &&
              h.getBoundingClientRect().width > 2)) errors.push(field.name + ': table heading on phone');
        } else {
          const heading = headings.find(h => clean(h.textContent) === field.name);
          const head = heading?.getBoundingClientRect();
          if (!heading || !head || !positive(head) || !positive(box) ||
              Math.abs(head.left - box.left) > 1 || Math.abs(head.right - box.right) > 1 ||
              !paintedText(heading).some(f => f.style.fontSize === '12px' && inside(f.box, head))) {
            errors.push(field.name + ': heading mismatch');
          }
        }
      });
      return {identity: sample.identity, errors};
    });
  }, {samples, width});
}



/** If a table exceeds the viewport, keyboard users must be able to reveal its last column. */
export async function lastColumnsReachable(page: Page, samples: RecordSample[]) {
  const failures: string[] = [];
  for (const sample of samples) {
    const body = page.locator(sample.table).first();
    const id = await body.evaluate(tbody => {
      let element = tbody.parentElement;
      while (element && element.id !== 'main-content') {
        if (element.scrollWidth > element.clientWidth + 1 && /auto|scroll/.test(getComputedStyle(element).overflowX)) {
          element.setAttribute('data-frame-scroll-probe','');
          return true;
        }
        element = element.parentElement;
      }
      return false;
    });
    if (!id) continue;
    const area = page.locator('[data-frame-scroll-probe]');
    try {
      const tab = await area.evaluate(el => el.tabIndex >= 0 || el.matches(':focus-visible') ||
        (el.getAttribute('tabindex') === null && el.getAttribute('role') === 'region'));
      await area.focus();
      if (!tab || !await area.evaluate(el => document.activeElement === el)) {
        failures.push(sample.identity + ': scroll region cannot receive keyboard focus');
        continue;
      }
      await area.press('Control+ArrowRight');
      for (let i = 0; i < 45 && !await area.evaluate(el => el.scrollLeft + el.clientWidth >= el.scrollWidth - 1); i++) {
        await area.press('ArrowRight');
        await page.evaluate(() => new Promise<void>(done => requestAnimationFrame(() => done())));
      }
      const reached = await body.evaluate(tbody => {
        const last = tbody.closest('table')!.querySelector('th:last-child')!.getBoundingClientRect();
        const viewport = tbody.closest('[data-frame-scroll-probe]')!.getBoundingClientRect();
        return last.width > 0 && last.right <= viewport.right + 1 && last.left >= viewport.left - 1;
      });
      if (!reached) failures.push(sample.identity + ': last column cannot be reached');
    } finally {
      await area.evaluate(el => { el.scrollLeft = 0; el.removeAttribute('data-frame-scroll-probe'); });
    }
  }
  return failures;
}
