import { test, expect } from './strict-fixtures';
import { ROUTES } from './fixtures';

/**
 * Rendered contrast contract for table separators.
 *
 * The static half lives in `tests/test_css_field_separator_contracts.py`. This
 * half is the one that would have caught the original defect: the CSS looked
 * correct in isolation, and only the composited computed style revealed that
 * three `!important` rules had left the field separator at `#d0d0d0` (1.54:1)
 * or `transparent`.
 *
 * Two separators are measured per surface, because they are drawn by different
 * rules and regressed independently:
 *   - the row-card outline (`tr` border), from `--tbl-card-border`;
 *   - the field/row separator (`td` bottom border), from the appended
 *     components.css rule.
 *
 * Rows are injected where a page renders none, so the contract holds for a
 * populated account even on surfaces the seed leaves empty. That gap is
 * exactly why this defect survived: with zero rows there is no separator to
 * photograph, so no baseline could ever have failed.
 *
 * Runs in the required functional gate on the wiped functional seed, where the
 * summary pages render only an empty-state message row — see the injection note
 * below for why that has to be topped up to two real data rows.
 */

const MIN_CONTRAST = 3.0; // WCAG 2.2 SC 1.4.11, non-text contrast

const SURFACES = [
  { name: 'progression', route: ROUTES.PROGRESSION, table: '.current-goals table' },
  { name: 'body-composition', route: ROUTES.BODY_COMPOSITION, table: '.bc-table' },
  { name: 'session-summary', route: ROUTES.SESSION_SUMMARY, table: 'table.tbl--responsive' },
  { name: 'weekly-summary', route: ROUTES.WEEKLY_SUMMARY, table: 'table.tbl--responsive' },
  { name: 'workout-log', route: ROUTES.WORKOUT_LOG, table: '#workout-log-table' },
  { name: 'workout-plan', route: ROUTES.WORKOUT_PLAN, table: '[data-testid="exercise-table"]' },
  { name: 'volume-splitter', route: ROUTES.VOLUME_SPLITTER, table: 'table.tbl--responsive' },
] as const;

const VIEWPORTS = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 900 },
] as const;

const THEMES = ['light', 'dark'] as const;

for (const surface of SURFACES) {
  for (const viewport of VIEWPORTS) {
    for (const theme of THEMES) {
      test(`separator contrast: ${surface.name} ${viewport.name} ${theme}`, async ({ page }) => {
        await page.setViewportSize({ width: viewport.width, height: viewport.height });
        // Obtain production field markup on the functional lane's empty Log.
        let planId: number | undefined;
        if (surface.name === 'workout-log') {
          const routine = `GYM - Separator ${viewport.name} ${theme} - Workout A`;
          const result = await page.request.post('/add_exercise', {data: {
            routine, exercise: 'Barbell Curl', sets: 3, min_rep_range: 8, max_rep_range: 12, rir: 2, weight: 30,
          }});
          expect(result.ok()).toBe(true);
          const plan = (await (await page.request.get('/get_workout_plan')).json()).data;
          planId = plan.find((row: {routine: string}) => row.routine === routine).id;
          expect((await page.request.post('/export_to_workout_log')).ok()).toBe(true);
        }
        try {
          await page.goto(surface.route);
          await page.evaluate((t) => document.documentElement.setAttribute('data-theme', t), theme);
          if (surface.name === 'workout-plan') {
            await expect(page.locator('#workout')).toHaveAttribute('data-plan-state', /^(empty|populated)$/);
          }

          const measured = await page.evaluate(({ table, isPlan }) => {
            const tbl = document.querySelector(table);
            if (!tbl) return { missing: true as const };

            // Guarantee TWO measurable data rows, and measure the first of them.
            //
            // Two, not one, because the last row's bottom border is suppressed on
            // purpose (`tbody tr:last-child td { border-bottom-color: transparent }`
            // in components.css) — the card outline draws that edge instead. A
            // separator only exists *between* adjacent rows, so a single-row table
            // has nothing to measure and measuring it asserts against design intent.
            //
            // A one-cell row is an empty-state message ("No data logged yet"), not a
            // data row: it has no label/value pair to divide, and on the wiped
            // functional seed it is the only row the summary pages render. Counting
            // it as a row is what made this spec pass on the plan-bearing visual seed
            // and fail on the functional one.
            const cols = tbl.querySelectorAll('thead th').length || 3;
            const body = tbl.querySelector('tbody') ?? tbl.appendChild(document.createElement('tbody'));
            const dataRows = () =>
              Array.from(body.querySelectorAll('tr')).filter((r) => r.querySelectorAll('td').length > 1);
            while (dataRows().length < 2) {
              const row = document.createElement('tr');
              for (let c = 0; c < cols; c++) {
                const td = document.createElement('td');
                td.setAttribute('data-label', 'label ' + c);
                td.textContent = 'value';
                row.appendChild(td);
              }
              body.appendChild(row);
            }
            if (isPlan) {
              // The synthetic data rows need the same visible region as loaded plan rows.
              const plan = tbl.closest<HTMLElement>('#workout');
              if (!plan) return { missing: true as const };
              plan.dataset.planState = 'populated';
              if (!tbl.getClientRects().length) return { missing: true as const };
            }

            const tr = dataRows()[0] as HTMLElement;
            const td = tr.querySelector('td') as HTMLElement;
            const parse = (s: string) => {
              const m = s.match(/rgba?\(([^)]+)\)/);
              if (!m) return null;
              const p = m[1].split(',').map((x) => parseFloat(x));
              return { rgb: [p[0], p[1], p[2]] as [number, number, number], a: p.length > 3 ? p[3] : 1 };
            };
            // Nearest painted ancestor background, so alpha composites correctly.
            const backdrop = (el: HTMLElement) => {
              let n: HTMLElement | null = el;
              while (n && n !== document.documentElement) {
                const bg = getComputedStyle(n).backgroundColor;
                if (bg && !/rgba\(0, 0, 0, 0\)/.test(bg)) return bg;
                n = n.parentElement;
              }
              return getComputedStyle(document.body).backgroundColor;
            };

            if (table === '#workout-log-table') {
              const field = tbl.querySelector<HTMLElement>('tr[data-log-id] [data-field="scored_rir"] .ui-field');
              if (!field || !field.getClientRects().length) return {missing: true as const};
              const style = getComputedStyle(field);
              return { missing: false as const, tdColor: style.borderTopColor, tdWidth: style.borderTopWidth,
                trColor: style.borderTopColor, trWidth: style.borderTopWidth, backdrop: backdrop(field) };
            }
            const cs = getComputedStyle(td);
            const trs = getComputedStyle(tr);
            return {
              missing: false as const,
              tdColor: cs.borderBottomColor,
              tdWidth: cs.borderBottomWidth,
              trColor: trs.borderTopColor,
              trWidth: trs.borderTopWidth,
              backdrop: backdrop(td),
            };
          }, { table: surface.table, isPlan: surface.name === 'workout-plan' });

          expect(measured.missing, `no ${surface.table} on ${surface.name}`).toBe(false);
          if (measured.missing) return;

          const lum = (c: [number, number, number]) => {
            const f = (v: number) => {
              const x = v / 255;
              return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
            };
            return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
          };
          const ratio = (a: [number, number, number], b: [number, number, number]) => {
            const la = lum(a), lb = lum(b);
            return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
          };
          const parse = (s: string) => {
            const m = s.match(/rgba?\(([^)]+)\)/);
            if (!m) return null;
            const p = m[1].split(',').map((x) => parseFloat(x));
            return { rgb: [p[0], p[1], p[2]] as [number, number, number], a: p.length > 3 ? p[3] : 1 };
          };

          const bg = parse(measured.backdrop) ?? { rgb: [255, 255, 255] as [number, number, number], a: 1 };
          const check = (label: string, colour: string, width: string) => {
            if (width === '0px') return; // not drawn here; nothing to perceive
            const c = parse(colour);
            expect(c, `${label} colour unparseable: ${colour}`).not.toBeNull();
            if (!c) return;
            expect(
              c.a,
              `${surface.name} ${viewport.name} ${theme}: ${label} is fully transparent, ` +
                'so the boundary it is meant to draw does not exist',
            ).toBeGreaterThan(0);
            const eff = c.rgb.map((v, i) => Math.round(v * c.a + bg.rgb[i] * (1 - c.a))) as [number, number, number];
            const r = ratio(eff, bg.rgb);
            expect(
              r,
              `${surface.name} ${viewport.name} ${theme}: ${label} contrast ${r.toFixed(2)}:1 ` +
                `(${colour} on ${measured.backdrop}) is below ${MIN_CONTRAST}:1`,
            ).toBeGreaterThanOrEqual(MIN_CONTRAST);
          };

          if (surface.name === 'workout-log') {
            expect(parseFloat(measured.tdWidth)).toBeGreaterThan(0);
            expect(() => check('negative control', measured.backdrop, measured.tdWidth)).toThrow();
          }
          if (surface.name === 'workout-plan') {
            if (viewport.name === 'desktop') {
              expect(parseFloat(measured.tdWidth), 'table cells draw a bottom separator').toBeGreaterThan(0);
            } else {
              expect(parseFloat(measured.trWidth), 'cards draw a top border').toBeGreaterThan(0);
            }
          }
          check('field separator (td bottom border)', measured.tdColor, measured.tdWidth);
          if (surface.name !== 'workout-log') check('row-card outline (tr border)', measured.trColor, measured.trWidth);
        } finally {
          if (planId !== undefined) {
            expect((await page.request.post('/remove_exercise', {data: { id: planId }})).ok()).toBe(true);
          }
        }
      });
    }
  }
}
