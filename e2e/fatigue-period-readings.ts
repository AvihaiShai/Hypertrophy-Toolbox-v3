import { readFileSync } from 'node:fs';
import path from 'node:path';
import type { Page } from '@playwright/test';
import { expect } from './strict-fixtures';
import { openFramePass, THEMES } from './frame-check';

type Reading = {
  sfr: string[];
  bars: [string, string, string, string | null, string, string | null][];
  regions: Record<string, Record<string, [string, string]>>;
};
const reference: { palette: Record<string, Record<string, string[]>>; periods: Record<string, Reading> } =
  JSON.parse(readFileSync(path.join(__dirname, 'fixtures/fatigue-period-readings.json'), 'utf8'));

export async function compareFatiguePeriods(page: Page, baseURL: string) {
  for (const theme of THEMES) {
    for (const choice of ['', 'invalid', 'this_session', 'this_week', 'last_4_weeks']) {
      const period = choice in reference.periods ? choice : 'this_week';
      const expected = reference.periods[period];
      await openFramePass(page, baseURL, '/fatigue' + (choice ? '?period=' + choice : ''), {width:768,scale:6,theme});
      await expect(page.getByTestId('fatigue-period-select')).toHaveValue(period);
      await expect(page.getByTestId('fatigue-page')).toHaveAttribute('data-heatmap-state','ready');
      for (const [i,side] of ['planned','logged'].entries()) {
        await expect(page.getByTestId('fatigue-sfr-' + side + '-value')).toHaveText(expected.sfr[i]);
      }
      const bars = page.getByTestId('fatigue-muscle-bar');
      await expect(bars).toHaveCount(expected.bars.length);
      const observed = await bars.evaluateAll(nodes => nodes.map(node => {
        const muscle = node.getAttribute('data-muscle')!;
        const percent = node.querySelector('[data-testid="fatigue-percent"]')!.textContent!.trim();
        return {muscle,percent,meters:[...node.querySelectorAll<HTMLElement>('[role=meter]')].map(meter => {
          const marker = getComputedStyle(meter, '::after');
          const fill = meter.firstElementChild;
          const bar = meter.parentElement!;
          return {
            name: meter.getAttribute('aria-label'), score: meter.getAttribute('aria-valuenow'),
            shown: bar.querySelector('.fatigue-bar__score')!.textContent!.trim(),
            fill: fill ? 100 * fill.getBoundingClientRect().width / meter.clientWidth : null,
            fillPaint: fill ? getComputedStyle(fill).backgroundColor : null,
            band: [...bar.classList].find(k => k.startsWith('fatigue-') && !k.startsWith('fatigue-bar'))?.slice(8),
            marker: marker.display !== 'none' && marker.content !== 'none' && marker.content !== 'normal' &&
              parseFloat(marker.width) > 0 && !['transparent','rgba(0, 0, 0, 0)'].includes(marker.backgroundColor),
            position: parseFloat(marker.left) / meter.clientWidth,
          };
        })};
      }));
      for (const [i, [muscle,percent,planned,plannedFill,logged,loggedFill]] of expected.bars.entries()) {
        const row = observed[i];
        expect([row.muscle,row.percent], 'ranked order and displayed percent').toEqual([muscle,percent]);
        expect(row.meters).toHaveLength(2);
        for (const [j, [channel,score,fill]] of [['Planned',planned,plannedFill],['Logged',logged,loggedFill]].entries()) {
          const meter = row.meters[j];
          expect([meter.name,meter.score,meter.shown]).toEqual([channel + ' fatigue for ' + muscle,score,fill ? score : '—']);
          expect(meter.marker).toBe(percent !== '—');
          if (meter.marker) expect(meter.position).toBeCloseTo(2/3, 2);
          if (fill) {
            expect(meter.fill).toBeCloseTo(parseFloat(fill), 0);
            expect(meter.fillPaint).toBe(reference.palette[theme][meter.band!][0]);
          } else expect(meter.fill).toBeNull();
        }
      }
      for (const channel of ['planned','logged']) {
        const button = page.getByTestId('fatigue-heatmap-channel-' + channel);
        await button.click();
        await expect(button).toHaveAttribute('aria-pressed','true');
        const other = channel === 'planned' ? 'logged' : 'planned';
        await expect(page.getByTestId('fatigue-heatmap-channel-' + other)).toHaveAttribute('aria-pressed','false');
        await expect(page.getByTestId('fatigue-heatmap-caption')).toContainText(new RegExp(channel,'i'));
        for (const [key,[muscle,band]] of Object.entries(expected.regions[channel])) {
          const [side,region] = key.split('/');
          const figure = page.getByTestId('fatigue-heatmap-figure-' + side);
          await expect(figure.locator('svg')).toHaveAttribute('aria-label',new RegExp(channel + ' fatigue by muscle, ' + side,'i'));
          const regions = figure.locator('[data-canonical-muscles="' + region + '"]');
          expect(await regions.count()).toBeGreaterThan(0);
          for (const painted of await regions.all()) {
            await expect(painted).toHaveAttribute('data-heatmap-muscle',muscle);
            if (band === 'unranked') expect(await painted.getAttribute('data-heatmap-band')).toBeFalsy();
            else await expect(painted).toHaveAttribute('data-heatmap-band',band);
            const style = await painted.evaluate(el => {
              const s = getComputedStyle(el); return [s.fill,s.stroke,s.strokeWidth];
            });
            expect(style, [period,theme,channel,key].join('/')).toEqual(reference.palette[theme][band.replaceAll('_','-')]);
          }
        }
      }
      for (const [band,[fill,stroke]] of Object.entries(reference.palette[theme])) {
        const swatch = page.getByTestId('fatigue-heatmap-legend').locator('.fatigue-' + band);
        await expect(swatch).toBeVisible();
        await expect(swatch).toHaveCSS('background-color',fill);
        await expect(swatch).toHaveCSS('border-top-color',stroke);
      }
    }
  }
}
