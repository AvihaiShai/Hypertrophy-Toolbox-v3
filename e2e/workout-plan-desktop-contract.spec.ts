import { test, expect, ROUTES, waitForPageReady } from './strict-fixtures';

/**
 * Non-raster contract for the five workout-plan desktop captures that left the
 * byte gate.
 *
 * Those five were removed because Chromium rasters them nondeterministically on
 * the ubuntu-24.04 runner — measured across 8 independent experiment sets / 21
 * generations, they flip between two states at identical layout, and no
 * combination of six documented capture controls closes it. The full evidence
 * is `docs/visual_determinism/PLANNING.md` §8; the exemption table naming each
 * file and its replacement is §8.10.
 *
 * Everything here is computed style, geometry or DOM structure — no pixels — so
 * it is immune to the raster defect while still failing on the things a
 * screenshot of this page would have failed on:
 *
 *   - a section disappearing, moving, or reordering;
 *   - progressive column disclosure regressing at 1440px in either view mode;
 *   - a theme surface losing its token colour or its text contrast;
 *   - a row losing its thumbnail, its swap control or its media button;
 *   - the curated/uncurated media split changing, which is the startup race the
 *     plan-bearing baselines used to be the only guard for;
 *   - a table separator losing contrast.
 *
 * Runs at 1440x900 only. The viewport is deliberately unchanged: narrowing it
 * would sidestep the raster behaviour by testing a different layout, which is
 * the opposite of preserving the coverage.
 */

const VIEWPORT = { width: 1440, height: 900 } as const;
const THEMES = ['light', 'dark'] as const;
const MODES = ['simple', 'advanced'] as const;
const MIN_SEPARATOR_CONTRAST = 3.0; // WCAG 2.2 SC 1.4.11
const MIN_TEXT_CONTRAST = 4.5; // WCAG 2.2 SC 1.4.3

/**
 * Columns the table shows at 1440px, per view mode, in document order.
 *
 * These are the visible-column sets the exempted element captures pinned as
 * pixels. `col--low` / `col--med` disclosure is driven by container queries
 * (`static/css/layout.css`), so a container-width regression that silently
 * collapsed a column would change this list and nothing else.
 *
 * The unnamed second entry is the drag-handle column, which has no header text.
 */
const SIMPLE_COLUMNS = [
  'Select for Superset', '', 'Routine', 'Exercise',
  'Primary Muscle', 'Secondary Muscle', 'Isolated Muscles',
  'Sets', 'Min Rep', 'Max Rep', 'RIR', 'RPE', 'Weight', 'Style', 'Grips',
  'Actions',
] as const;

/** Advanced adds exactly these six, and reorders nothing. */
const ADVANCED_ONLY_COLUMNS = [
  'Tertiary Muscle', 'Utility', 'Movement Pattern', 'Movement Subpattern',
  'Stabilizers', 'Synergists',
] as const;

const ADVANCED_COLUMNS = [
  'Select for Superset', '', 'Routine', 'Exercise',
  'Primary Muscle', 'Secondary Muscle', 'Tertiary Muscle', 'Isolated Muscles',
  'Utility', 'Movement Pattern', 'Movement Subpattern',
  'Sets', 'Min Rep', 'Max Rep', 'RIR', 'RPE', 'Weight', 'Style', 'Grips',
  'Stabilizers', 'Synergists', 'Actions',
] as const;

const SECTIONS = [
  '#workout > header.ui-page-header',
  '#workout > section[aria-labelledby="workout-plan-table-heading"]',
  '#workout > section[aria-labelledby="plan-add-heading"]',
] as const;

/** Body background per theme, from the shipped tokens. */
const BODY_BACKGROUND = {
  light: 'rgb(238, 241, 246)',
  dark: 'rgb(16, 20, 25)',
} as const;

const SEED_ROWS = 6;

function relativeLuminance([r, g, b]: [number, number, number]): number {
  const channel = (value: number) => {
    const v = value / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b);
}

function contrastRatio(a: [number, number, number], b: [number, number, number]): number {
  const la = relativeLuminance(a);
  const lb = relativeLuminance(b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

/**
 * Parse either colour syntax Chromium reports here.
 *
 * The Calm Glass surfaces resolve to `color(srgb r g b / a)` with 0-1 channels,
 * not `rgba()` with 0-255 ones, so a parser that only knows `rgba()` silently
 * treats the busiest surface on the page as unmeasurable.
 */
function parseColour(value: string): { rgb: [number, number, number]; alpha: number } | null {
  const srgb = value.match(/color\(srgb\s+([^)]+)\)/);
  if (srgb) {
    const [channels, alpha] = srgb[1].split('/');
    const parts = channels.trim().split(/\s+/).map((part) => parseFloat(part) * 255);
    return {
      rgb: [parts[0], parts[1], parts[2]] as [number, number, number],
      alpha: alpha === undefined ? 1 : parseFloat(alpha),
    };
  }
  const match = value.match(/rgba?\(([^)]+)\)/);
  if (!match) return null;
  const parts = match[1].split(',').map((part) => parseFloat(part));
  return {
    rgb: [parts[0], parts[1], parts[2]] as [number, number, number],
    alpha: parts.length > 3 ? parts[3] : 1,
  };
}

/** Composite `colour` over `backdrop` so an alpha value is judged as painted. */
function flatten(
  colour: { rgb: [number, number, number]; alpha: number },
  backdrop: [number, number, number],
): [number, number, number] {
  return colour.rgb.map((v, i) =>
    Math.round(v * colour.alpha + backdrop[i] * (1 - colour.alpha)),
  ) as [number, number, number];
}

async function openPlan(page: import('@playwright/test').Page, theme: string, mode: string) {
  await page.setViewportSize(VIEWPORT);
  await page.addInitScript(([t, m]) => {
    localStorage.clear();
    localStorage.setItem('darkMode', t === 'dark' ? 'true' : 'false');
    localStorage.setItem('hypertrophy_filter_view_mode', m);
    document.documentElement?.setAttribute('data-theme', t);
  }, [theme, mode]);
  await page.goto(ROUTES.WORKOUT_PLAN);
  await waitForPageReady(page);
  await page.waitForSelector('#workout_plan_table_body tr', { timeout: 15_000 });
  const all = page.locator('#tab-all');
  await all.click();
  await expect(all).toHaveAttribute('aria-selected', 'true');
}

for (const theme of THEMES) {
  for (const mode of MODES) {
    test.describe(`workout-plan desktop contract: ${theme} ${mode}`, () => {
      test(`page composition and section order: ${theme} ${mode}`, async ({ page }) => {
        await openPlan(page, theme, mode);

        const region = page.getByRole('region', { name: 'Workout plan exercises table' });
        await expect(page.locator('#navbar')).toBeVisible();
        await expect(region).toBeVisible();
        await expect(region).toHaveAttribute('tabindex', '0');
        await expect(region.getByTestId('exercise-table')).toBeVisible();
        for (const section of SECTIONS) await expect(page.locator(section)).toBeVisible();

        const layout = await page.evaluate((selectors) => {
          const doc = document.documentElement;
          return {
            sections: selectors.map((selector) => {
              const rect = document.querySelector(selector)!.getBoundingClientRect();
              return {
                selector,
                top: rect.top,
                leftGutter: rect.left,
                rightGutter: doc.clientWidth - rect.right,
              };
            }),
            routineTabHeights: Array.from(
              document.querySelectorAll<HTMLElement>('#routine-tabs .routine-tab-btn'),
            ).map((tab) => ({
              routine: tab.dataset.routine,
              height: tab.getBoundingClientRect().height,
            })),
            scrollWidth: doc.scrollWidth,
            clientWidth: doc.clientWidth,
          };
        }, SECTIONS);

        for (const [index, section] of layout.sections.entries()) {
          expect(section.leftGutter, `${section.selector} left gutter`).toBeCloseTo(32, 0);
          expect(section.rightGutter, `${section.selector} right gutter`).toBeCloseTo(32, 0);
          if (index > 0) {
            expect(section.top, `${section.selector} must follow the preceding section`)
              .toBeGreaterThan(layout.sections[index - 1].top);
          }
        }
        expect(layout.routineTabHeights.length, 'seeded routine tabs are missing').toBeGreaterThan(1);
        const tabHeights = layout.routineTabHeights.map((tab) => tab.height);
        expect(
          Math.max(...tabHeights) - Math.min(...tabHeights),
          `routine tabs have mismatched heights: ${JSON.stringify(layout.routineTabHeights)}`,
        ).toBeLessThanOrEqual(1);

        expect(layout.clientWidth).toBe(VIEWPORT.width);
        expect(layout.scrollWidth, 'the page has horizontal overflow').toBe(layout.clientWidth);

        const tableLayout = await region.evaluate((element) => {
          const headings = Array.from(element.querySelectorAll('thead th'));
          return {
            maxScroll: element.scrollWidth - element.clientWidth,
            clippedHeadings: headings.filter((heading) => heading.scrollWidth > heading.clientWidth)
              .map((heading) => heading.textContent?.trim()),
            exerciseWidth: element.querySelector('th[data-label="Exercise"]')!.getBoundingClientRect().width,
          };
        });
        expect(tableLayout.clippedHeadings).toEqual([]);
        expect(tableLayout.exerciseWidth).toBeGreaterThanOrEqual(220);
        if (mode === 'advanced') {
          expect(tableLayout.maxScroll, 'advanced table must overflow the region').toBeGreaterThan(0);
        }
        if (tableLayout.maxScroll > 0) {
          await region.focus();
          await expect(region).toBeFocused();
          await region.press('ArrowRight');
          await expect.poll(() => region.evaluate((element) => element.scrollLeft)).toBeGreaterThan(0);
        }

        const reachable = await region.evaluate((element) => {
          element.scrollLeft = element.scrollWidth;
          const left = element.getBoundingClientRect().left + element.clientLeft;
          const right = left + element.clientWidth;
          const insideInlineBounds = (rect: DOMRect) =>
            rect.width > 0 && rect.left >= left - 1 && rect.right <= right + 1;
          const lastColumn = element.querySelector('thead th:last-child')!;
          const controls = Array.from(element.querySelectorAll('tbody [data-action="delete"]'));
          return {
            lastColumn: insideInlineBounds(lastColumn.getBoundingClientRect()),
            reachableRemoves: controls.filter((control) => {
              const rect = control.getBoundingClientRect();
              if (!insideInlineBounds(rect) || rect.height === 0) return false;
              window.scrollBy(0, rect.top + rect.height / 2 - window.innerHeight / 2);
              const box = control.getBoundingClientRect();
              const target = document.elementFromPoint(box.left + box.width / 2, box.top + box.height / 2);
              return control.contains(target);
            }).length,
          };
        });
        expect(reachable.lastColumn, 'last column is inside the visible region at the scroll end').toBe(true);
        expect(reachable.reachableRemoves, 'every Remove control is reachable at the scroll end').toBe(SEED_ROWS);
      });

      test(`progressive column disclosure: ${theme} ${mode}`, async ({ page }) => {
        await openPlan(page, theme, mode);

        const table = await page.evaluate(() => {
          const el = document.querySelector('[data-testid="exercise-table"]') as HTMLElement;
          const visible = (node: Element) => {
            const rect = node.getBoundingClientRect();
            const style = getComputedStyle(node);
            return rect.width > 0 && rect.height > 0
              && style.display !== 'none' && style.visibility !== 'hidden';
          };
          const headers = Array.from(el.querySelectorAll('thead th'));
          const rows = Array.from(el.querySelectorAll('#workout_plan_table_body tr'));
          return {
            className: el.className,
            visibleHeaders: headers.filter(visible)
              .map((h) => (h.textContent ?? '').trim().replace(/\s+/g, ' ')),
            rowCount: rows.length,
            visibleCellsPerRow: rows.map(
              (r) => Array.from(r.querySelectorAll('td')).filter(visible).length,
            ),
            scrollWidth: el.scrollWidth,
          };
        });

        const expected = mode === 'advanced' ? ADVANCED_COLUMNS : SIMPLE_COLUMNS;
        expect(table.className).toContain(`tbl--view-${mode}`);
        expect(
          table.visibleHeaders,
          `visible columns at 1440px changed for ${mode}`,
        ).toEqual([...expected]);

        if (mode === 'advanced') {
          const extra = table.visibleHeaders.filter((h) => !SIMPLE_COLUMNS.includes(h as never));
          expect(
            extra.sort(),
            'advanced no longer adds exactly the six low-priority columns',
          ).toEqual([...ADVANCED_ONLY_COLUMNS].sort());
        }

        expect(table.rowCount, 'seeded plan row count changed').toBe(SEED_ROWS);
        expect(
          table.visibleCellsPerRow,
          'a body row does not expose one visible cell per visible column',
        ).toEqual(Array(SEED_ROWS).fill(expected.length));
      });

      test(`row media and controls: ${theme} ${mode}`, async ({ page }) => {
        await openPlan(page, theme, mode);

        const thumbnails = page.getByTestId('exercise-table').locator('img.exercise-thumbnail');
        await expect.poll(() => thumbnails.evaluateAll((images) => images.filter((image) => {
          const thumbnail = image as HTMLImageElement;
          return thumbnail.complete && thumbnail.naturalWidth > 0;
        }).length), { message: 'all seeded thumbnails decode after selecting All' }).toBe(SEED_ROWS);

        const row = await page.evaluate(() => {
          const el = document.querySelector('[data-testid="exercise-table"]') as HTMLElement;
          const thumbs = Array.from(el.querySelectorAll<HTMLImageElement>('img.exercise-thumbnail'));
          const mediaButtons = Array.from(el.querySelectorAll<HTMLElement>('[data-action="play-video"]'));
          const swaps = Array.from(el.querySelectorAll<HTMLElement>('.btn-swap'));
          return {
            thumbCount: thumbs.length,
            thumbsDecoded: thumbs.filter((i) => i.complete && i.naturalWidth > 0).length,
            thumbSrcOk: thumbs.every((i) =>
              (i.getAttribute('src') ?? '').startsWith('/static/vendor/free-exercise-db/exercises/')),
            mediaCount: mediaButtons.length,
            curated: mediaButtons.filter((b) => b.querySelector('i.fa-play')).length,
            uncurated: mediaButtons.filter((b) => b.querySelector('i.fa-search')).length,
            swapCount: swaps.length,
            swapsRendered: swaps.filter((b) => {
              const r = b.getBoundingClientRect();
              return r.width > 0 && r.height > 0;
            }).length,
            removeCount: el.querySelectorAll('#workout_plan_table_body [data-action="delete"]').length,
          };
        });

        expect(row.thumbCount, 'one thumbnail per seeded row').toBe(SEED_ROWS);
        expect(row.thumbsDecoded, 'a thumbnail did not decode').toBe(SEED_ROWS);
        expect(row.thumbSrcOk, 'a thumbnail src left the vendored exercise directory').toBe(true);

        expect(row.mediaCount, 'one media button per seeded row').toBe(SEED_ROWS);
        // The catalog upgrade must have completed before first paint. If it has
        // not, every row falls back to the magnifier and this split moves —
        // which is the startup race the plan-bearing baselines used to be the
        // only guard for (PLANNING.md §0 cause 1).
        expect(
          row.curated + row.uncurated,
          'a media button rendered neither the play nor the search icon',
        ).toBe(SEED_ROWS);
        expect(
          row.curated,
          'curated/uncurated media split changed; the catalog upgrade may be racing first paint',
        ).toBe(4);

        expect(row.swapCount, 'one swap control per seeded row').toBe(SEED_ROWS);
        expect(row.swapsRendered, 'a swap control has no rendered box').toBe(SEED_ROWS);
        expect(row.removeCount, 'one remove control per seeded row').toBe(SEED_ROWS);
      });

      test(`theme surfaces and separator contrast: ${theme} ${mode}`, async ({ page }) => {
        await openPlan(page, theme, mode);

        const measured = await page.evaluate(() => {
          const table = document.querySelector('[data-testid="exercise-table"]') as HTMLElement;
          const backdropOf = (el: HTMLElement) => {
            let node: HTMLElement | null = el;
            while (node && node !== document.documentElement) {
              const bg = getComputedStyle(node).backgroundColor;
              if (bg && !/rgba\(0, 0, 0, 0\)/.test(bg)) return bg;
              node = node.parentElement;
            }
            return getComputedStyle(document.body).backgroundColor;
          };
          const dataRows = Array.from(
            table.querySelectorAll<HTMLElement>('#workout_plan_table_body tr'),
          );
          const cell = dataRows[0].querySelector('td') as HTMLElement;
          const cellStyle = getComputedStyle(cell);
          const rowStyle = getComputedStyle(dataRows[0]);
          return {
            bodyBackground: getComputedStyle(document.body).backgroundColor,
            bodyColour: getComputedStyle(document.body).color,
            tableBackground: getComputedStyle(table).backgroundColor,
            cellColour: cellStyle.color,
            cellBackdrop: backdropOf(cell),
            separatorColour: cellStyle.borderBottomColor,
            separatorWidth: cellStyle.borderBottomWidth,
            outlineColour: rowStyle.borderTopColor,
            outlineWidth: rowStyle.borderTopWidth,
          };
        });

        expect(
          measured.bodyBackground,
          `body background is not the ${theme} token`,
        ).toBe(BODY_BACKGROUND[theme]);

        const rawBackdrop = parseColour(measured.cellBackdrop);
        expect(rawBackdrop, `unparseable backdrop: ${measured.cellBackdrop}`).not.toBeNull();
        if (!rawBackdrop) return;
        // The Calm Glass cell surface is itself translucent, so composite it
        // over the page background before judging anything against it.
        const page_ = parseColour(measured.bodyBackground);
        const backdrop = {
          rgb: page_ ? flatten(rawBackdrop, page_.rgb) : rawBackdrop.rgb,
          alpha: 1,
        };

        const text = parseColour(measured.cellColour);
        expect(text, `unparseable cell colour: ${measured.cellColour}`).not.toBeNull();
        if (!text) return;
        const textRatio = contrastRatio(flatten(text, backdrop.rgb), backdrop.rgb);
        expect(
          textRatio,
          `${theme}/${mode}: table text contrast ${textRatio.toFixed(2)}:1 `
            + `(${measured.cellColour} on ${measured.cellBackdrop}) is below ${MIN_TEXT_CONTRAST}:1`,
        ).toBeGreaterThanOrEqual(MIN_TEXT_CONTRAST);

        const checkEdge = (label: string, colour: string, width: string) => {
          if (width === '0px') return; // not drawn here; nothing to perceive
          const parsed = parseColour(colour);
          expect(parsed, `${label} unparseable: ${colour}`).not.toBeNull();
          if (!parsed) return;
          expect(
            parsed.alpha,
            `${theme}/${mode}: ${label} is fully transparent`,
          ).toBeGreaterThan(0);
          const ratio = contrastRatio(flatten(parsed, backdrop.rgb), backdrop.rgb);
          expect(
            ratio,
            `${theme}/${mode}: ${label} contrast ${ratio.toFixed(2)}:1 `
              + `(${colour} on ${measured.cellBackdrop}) is below ${MIN_SEPARATOR_CONTRAST}:1`,
          ).toBeGreaterThanOrEqual(MIN_SEPARATOR_CONTRAST);
        };

        expect(parseFloat(measured.separatorWidth), 'table cells draw a bottom separator').toBeGreaterThan(0);
        checkEdge('field separator (td bottom border)', measured.separatorColour, measured.separatorWidth);
        checkEdge('row-card outline (tr border)', measured.outlineColour, measured.outlineWidth);
      });
    });
  }
}
