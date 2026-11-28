import type { Locator, Page } from '@playwright/test';
import { details } from './workout-plan-fixture';
import { expect } from './strict-fixtures';

export const planTable = (page: Page) => page.getByTestId('exercise-table');
export const planHeader = (page: Page) => page.locator('#main-content header').filter({
  has: page.getByRole('heading', { name: 'Workout Plan', exact: true, level: 1 }),
});
export const planPanel = (page: Page) => page.locator('section[aria-labelledby="workout-plan-table-heading"]');
export const addPanel = (page: Page) => page.locator('.ui-panel').filter({
  has: page.getByRole('heading', { name: 'Add exercise', exact: true }),
});
export const moreButton = (page: Page) => page.getByRole('button', { name: 'More', exact: true });
export const filterToggle = (page: Page) => page.locator('button[aria-expanded]').filter({ hasText: /^Filters\b/i });
export const planViewToggle = (page: Page) => page.locator('.tbl-view-mode-toggle[data-table-key="workout_plan"]');
export async function setSupersetChoice(row: Locator, selected: boolean) {
  const checkbox = row.locator('.superset-checkbox');
  const label = row.locator('label:has(.superset-checkbox)');
  if (await checkbox.isChecked() !== selected) {
    if (await label.isVisible()) await label.click();
    else await checkbox.setChecked(selected);
  }
  if (selected) await expect(checkbox).toBeChecked();
  else await expect(checkbox).not.toBeChecked();
}

export async function setPlanView(page: Page, mode: 'simple' | 'advanced') {
  const toggle = planViewToggle(page);
  await expect(toggle).toHaveAttribute('data-view-mode', /^(simple|advanced)$/);
  if (await toggle.getAttribute('data-view-mode') !== mode) await toggle.click();
  await expect(toggle).toHaveAttribute('data-view-mode', mode);
}

/** Read every linked phone card in one browser task because the post-link GET replaces the entire tbody. */
export function readSupersetCardPaint(page: Page) {
  return page.locator('#workout').evaluate(workout => {
    const probe = document.createElement('span');
    probe.style.cssText = 'display:none;color:var(--ink-2);background:var(--surface-1)';
    workout.append(probe);
    const ink = getComputedStyle(probe).color;
    const surface = getComputedStyle(probe).backgroundColor;
    probe.remove();
    // The neutral tokens resolve to opaque sRGB colors in both supported themes.
    const opaqueTokens = ink.startsWith('rgb(') && surface.startsWith('rgb(') && ink !== surface;
    const visibleBox = (node: Element) => {
      const box = node.getBoundingClientRect();
      return node.isConnected && box.width > 0 && box.height > 0 &&
        node.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true });
    };
    return [...workout.querySelectorAll<HTMLElement>('#workout_plan_table_body tr[data-superset-group]')].map(card => {
      const base = getComputedStyle(card);
      const before = getComputedStyle(card, '::before');
      const width = parseFloat(before.width);
      const paintedRail = visibleBox(card) && before.display !== 'none' && before.visibility === 'visible' &&
        Number(before.opacity) > 0 && before.content !== 'none' && before.content !== 'normal' &&
        before.position === 'absolute' && parseFloat(before.left) === 0 &&
        width > Math.max(1, parseFloat(base.borderLeftWidth)) && parseFloat(before.height) > width &&
        opaqueTokens && before.backgroundColor === ink;
      const badge = card.querySelector('.superset-badge');
      const style = badge && getComputedStyle(badge);
      const paintedBadge = !!badge && visibleBox(badge) && badge.textContent?.trim() === 'Superset' &&
        opaqueTokens && style?.color === ink && style.backgroundColor === surface;
      return {
        id: Number(card.dataset.exerciseId),
        group: card.dataset.supersetGroup,
        paintedRail,
        paintedBadge,
        badge: [style?.color, style?.backgroundColor],
        rail: [base, before].map(layer => [layer.borderLeftWidth, layer.borderLeftColor, layer.backgroundColor]),
      };
    }).sort((a, b) => a.id - b.id);
  });
}

/** Measure colors even when a legacy action has no shared variant class. */
export function filledPlanActions(page: Page) {
  return page.locator('#main-content').evaluate(main => {
    const probe = document.createElement('span');
    probe.style.cssText = 'display:none;background:var(--ui-primary);color:var(--ui-danger-fill)';
    main.append(probe);
    const primary = getComputedStyle(probe).backgroundColor;
    const danger = getComputedStyle(probe).color;
    probe.remove();
    const controls = [...main.querySelectorAll<HTMLElement>('button, a[role="button"], input[type="submit"]')]
      .filter(node => node.getClientRects().length && getComputedStyle(node).visibility === 'visible');
    const name = (node: HTMLElement) => node.id || node.getAttribute('aria-label') || node.innerText.trim();
    return {
      primaryVariants: controls.filter(node => node.classList.contains('ui-btn--primary')).map(name),
      primaryFills: controls.filter(node => getComputedStyle(node).backgroundColor === primary).map(name),
      dangerFills: controls.filter(node => {
        const [r, g, b, a = 1] = (getComputedStyle(node).backgroundColor.match(/[\d.]+/g) || []).map(Number);
        return (a >= 0.85 && r > 110 && r > g * 1.5 && r > b * 1.5) ||
          getComputedStyle(node).backgroundColor === danger;
      }).map(name),
    };
  });
}

export const singleAddAction = {
  primaryVariants: ['add_exercise_btn'], primaryFills: ['add_exercise_btn'], dangerFills: [],
};

export async function setDetails(page: Page, id: number, open: boolean) {
  const disclosure = details(page, id);
  await expect(disclosure).toHaveAttribute('aria-expanded', /^(true|false)$/);
  if (await disclosure.getAttribute('aria-expanded') !== String(open)) await disclosure.click();
  await expect(disclosure).toHaveAttribute('aria-expanded', String(open));
}

/**
 * WP11 checks document width, containment, and the actual laid-out hit boxes.
 * In the narrow-phone passes, open Details also needs two numeric fields per
 * row. Text ranges catch wrapping or overflow even if the field itself fits.
 */
export function phonePlanProblems(page: Page) {
  return page.locator('#main-content').evaluate(main => {
    const width = document.documentElement.clientWidth;
    const problems: string[] = [];
    const tolerance = 0.5;
    const rendered = (node: Element) => node.getClientRects().length > 0 &&
      getComputedStyle(node).visibility === 'visible';
    const inBox = (inner: DOMRect, outer: DOMRect) =>
      inner.left >= outer.left - tolerance && inner.right <= outer.right + tolerance &&
      inner.top >= outer.top - tolerance && inner.bottom <= outer.bottom + tolerance;
    const name = (node: Element) => node.getAttribute('aria-label') ||
      node.getAttribute('data-label') || node.id || node.textContent?.trim().slice(0, 80) || node.tagName;
    const cards = [...main.querySelectorAll('tr.ui-record-card')].filter(rendered);
    if (!cards.length) problems.push('no exercise cards render');
    if (document.documentElement.scrollWidth > width) problems.push('the page scrolls sideways');
    const textBoxes = (element: Element | null) => {
      if (!element) return [];
      const boxes: DOMRect[] = [];
      const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
      const range = document.createRange();
      for (let node = walker.nextNode(); node; node = walker.nextNode()) {
        if (!node.textContent?.trim() || !node.parentElement || !rendered(node.parentElement)) continue;
        range.selectNodeContents(node);
        boxes.push(...[...range.getClientRects()].filter(rect => rect.width > 0 && rect.height > 0));
      }
      return boxes;
    };
    for (const card of cards) {
      const heading = card.querySelector('.exercise-name');
      const groups = [
        { label: 'title', boxes: textBoxes(card.querySelector('.plan-exercise-heading')) },
        { label: 'routine', boxes: textBoxes(card.querySelector('.routine-cell')) },
        { label: 'prescription', boxes: textBoxes(card.querySelector('.plan-prescription')) },
        { label: 'actions', boxes: [...card.querySelectorAll('.plan-card-actions button')]
          .filter(rendered).map(button => button.getBoundingClientRect()) },
      ];
      const exercise = heading?.textContent?.trim() || name(card);
      for (const [index, group] of groups.entries()) {
        if (!group.boxes.length) problems.push(`${exercise}: ${group.label} has no visible content`);
        const next = groups[index + 1];
        if (next && group.boxes.length && next.boxes.length &&
            Math.max(...group.boxes.map(rect => rect.bottom)) > Math.min(...next.boxes.map(rect => rect.top)) + tolerance) {
          problems.push(`${exercise}: ${group.label} overlaps or follows ${next.label}`);
        }
      }
      if (card.querySelector('.plan-details-toggle[aria-expanded="true"]')) {
        const rows: { top: number; fields: { label: string; left: number }[] }[] = [];
        for (const cell of [...card.querySelectorAll(':scope > [data-field]')].filter(rendered)) {
          const { top, left } = cell.getBoundingClientRect();
          const field = { label: name(cell), left };
          const row = rows.find(row => Math.abs(top - row.top) <= tolerance);
          if (row) row.fields.push(field);
          else rows.push({ top, fields: [field] });

          const value = textBoxes(cell);
          if (!value.length || value.some(box => Math.abs(box.top - value[0].top) > tolerance)) {
            problems.push(`${exercise}: ${field.label} value must fit on one line`);
          }
        }
        const layout = rows.sort((a, b) => a.top - b.top).map(row =>
          row.fields.sort((a, b) => a.left - b.left).map(field => field.label).join(', '),
        ).join(' / ');
        if (layout !== 'Sets, Min Rep / Max Rep, RIR / RPE, Weight') {
          problems.push(`${exercise}: Details needs two numeric fields per row (rendered: ${layout || 'none'})`);
        }
      }
    }
    const selectionBar = main.querySelector('#superset-actions');
    const areas = [...cards, ...main.querySelectorAll(
      '.ui-page-actions, #routine-tabs, #superset-actions, .ui-panel:has(#add_exercise_btn), #filter-chips',
    )].filter(rendered);
    const targets = 'button, a[href], input:not([type="hidden"]), select, .drag-handle, label:has(.superset-checkbox)';
    const checked = new Set<Element>();
    for (const area of areas) {
      const box = area.getBoundingClientRect();
      if (box.left < -tolerance || box.right > width + tolerance) problems.push(name(area) + ' leaves viewport');
      const controls = [...area.querySelectorAll(targets)].filter(rendered).filter(node => {
        // The enhanced selects and wrapped native checkbox have their own visible hit areas.
        if (node.matches('select') && node.closest('.wpdd')) return false;
        if (node.matches('.superset-checkbox') && node.closest('label')) return false;
        return true;
      });
      for (const control of controls) {
        const rect = control.getBoundingClientRect();
        if (!inBox(rect, box)) problems.push(name(control) + ' leaves ' + name(area));
        if (selectionBar && area.matches('tr.ui-record-card')) {
          const hit = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
          if (hit && selectionBar.contains(hit)) problems.push('selection bar covers ' + name(control));
        }
        if (checked.has(control)) continue;
        checked.add(control);
        if (rect.width < 43.5 || rect.height < 43.5) problems.push(name(control) + ' has a target under 44 × 44 px');
      }
      for (const [i, control] of controls.entries()) {
        const a = control.getBoundingClientRect();
        for (const other of controls.slice(i + 1)) {
          if (control.contains(other) || other.contains(control)) continue;
          const b = other.getBoundingClientRect();
          if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > tolerance &&
              Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > tolerance) {
            problems.push(name(control) + ' overlaps ' + name(other));
          }
        }
      }
      for (const cell of area.querySelectorAll('[data-label]')) {
        if (rendered(cell) && (cell.scrollWidth > cell.clientWidth + 1 || cell.scrollHeight > cell.clientHeight + 1)) {
          problems.push('clipped cell content or generated label: ' + name(cell));
        }
      }
      const walker = document.createTreeWalker(area, NodeFilter.SHOW_TEXT);
      for (let node = walker.nextNode(); node; node = walker.nextNode()) {
        const parent = node.parentElement;
        if (!node.textContent?.trim() || !parent || !rendered(parent) || parent.closest('option, .wpdd-select')) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        const field = parent.closest('.ui-field, .ui-tab, .ui-chip, td, button');
        const fieldBox = field?.getBoundingClientRect() ?? box;
        // A 999.5 kg value may use the field padding at 320 px. Its glyphs must still fit.
        if ([...range.getClientRects()].some(rect => !inBox(rect, box) || !inBox(rect, fieldBox))) {
          problems.push('clipped or overflowing text: ' + node.textContent.trim());
        }
      }
    }
    return [...new Set(problems)];
  });
}
