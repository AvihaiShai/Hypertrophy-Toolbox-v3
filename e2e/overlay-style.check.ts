import type { Locator, Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import {
  expectFrameRun, fontsLoaded, gutter, installFrameSettings,
  openFramePass, THEMES, writeMetrics,
} from './frame-check';
import { expect, ROUTES, test } from './strict-fixtures';
import { editVisualPlanFixture, planRows } from './workout-plan-fixture';

const MIGRATED = [
  { route: ROUTES.WORKOUT_PLAN, id: 'generatePlanModal', width: 1120, fill: '--ui-primary' },
  { route: ROUTES.WORKOUT_PLAN, id: 'clearPlanModal', width: 480, fill: '--ui-danger-fill' },
  { route: ROUTES.WORKOUT_PLAN, id: 'exerciseVideoModal', width: 800, fill: null },
  { route: ROUTES.WORKOUT_LOG, id: 'clearLogModal', width: 480, fill: '--ui-danger-fill' },
] as const;

const UNMIGRATED = [
  { route: ROUTES.HOME, id: 'eraseDataModal' },
  { route: ROUTES.PROGRESSION, id: 'deleteGoalModal' },
  { route: ROUTES.PROGRESSION, id: 'goalSettingModal' },
  { route: ROUTES.VOLUME_SPLITTER, id: 'deleteVolumePlanModal' },
] as const;

const REFERENCE = 'overlay-style.reference.json';

async function toggleModal(modal: Locator, show: boolean) {
  await modal.evaluate((element, opening) => new Promise<void>(resolve => {
    const { bootstrap } = window as unknown as {
      bootstrap: { Modal: { getOrCreateInstance: (element: Element) => { show(): void; hide(): void } } };
    };
    element.addEventListener(opening ? 'shown.bs.modal' : 'hidden.bs.modal', () => resolve(), { once: true });
    const instance = bootstrap.Modal.getOrCreateInstance(element);
    if (opening) instance.show();
    else instance.hide();
  }), show);
}

function modalStyle(modal: Locator) {
  return modal.evaluate(element => {
    const read = (selector: string, properties: string[]) => {
      const node = element.querySelector(selector);
      if (!node) return null;
      const style = getComputedStyle(node);
      return Object.fromEntries(properties.map(property => [property, style.getPropertyValue(property)]));
    };
    const dialog = element.querySelector('.modal-dialog')!;
    const rect = dialog.getBoundingClientRect();
    const round = (value: number) => Math.round(value * 2) / 2;
    const tokens = document.createElement('span');
    tokens.style.cssText =
      'position:absolute; visibility:hidden; background:var(--surface-2); box-shadow:var(--shadow-elev-2);' +
      'color:var(--ui-primary); border:1px solid var(--ui-danger-fill);';
    element.append(tokens);
    const tokenStyle = getComputedStyle(tokens);
    const expected = {
      surface: tokenStyle.backgroundColor, shadow: tokenStyle.boxShadow,
      primary: tokenStyle.color, danger: tokenStyle.borderTopColor,
    };
    tokens.remove();
    const boxStyles = ['background-color', 'background-image', 'backdrop-filter', 'border-top-width',
      'border-top-style', 'border-top-color', 'border-top-left-radius', 'box-shadow', 'padding-top'];
    return {
      dialog: { left: round(rect.left), right: round(rect.right), width: round(rect.width) },
      content: read('.modal-content', boxStyles)!,
      header: read('.modal-header', boxStyles)!,
      title: read('.modal-title', ['color', 'font-size', 'line-height', 'font-weight'])!,
      body: read('.modal-body', boxStyles)!,
      footer: read('.modal-footer', boxStyles),
      controls: [...element.querySelectorAll('button, .modal-footer a[href]')]
        .filter(node => node.getClientRects().length)
        .map(node => {
          const style = getComputedStyle(node);
          return {
            text: node.getAttribute('aria-label') || node.textContent?.trim(),
            height: round(node.getBoundingClientRect().height),
            fill: style.backgroundColor, image: style.backgroundImage, color: style.color,
            footer: !!node.closest('.modal-footer'),
            close: node.matches('.btn-close'),
          };
        }),
      expected,
    };
  });
}

type ModalStyle = Awaited<ReturnType<typeof modalStyle>>;
const transparent = 'rgba(0, 0, 0, 0)';

function modalProblems(style: ModalStyle, spec: typeof MIGRATED[number], width: number) {
  const problems: string[] = [];
  const must = (condition: boolean, symptom: string) => { if (!condition) problems.push(symptom); };
  must(style.content['background-color'] === style.expected.surface, 'opaque modal surface');
  must(style.content['border-top-left-radius'] === '16px', '16 px radius');
  must(style.content['border-top-width'] === '1px', '1 px border');
  must(style.content['box-shadow'] === style.expected.shadow, 'elevation shadow');
  for (const [part, properties] of [['content', style.content], ['header', style.header], ['footer', style.footer]] as const) {
    if (properties) {
      must(properties['backdrop-filter'] === 'none', part + ' backdrop filter');
      must(properties['background-image'] === 'none', part + ' background image');
    }
  }
  must([transparent, style.expected.surface].includes(style.header['background-color']), 'plain header');
  must(style.title['font-size'] === '18px' && style.title['line-height'] === '24px' &&
    style.title['font-weight'] === '600', 'title typography');
  must(style.body['padding-top'] === '16px', 'body padding');
  if (style.footer) must(style.footer['padding-top'] === '16px', 'footer padding');
  const expectedFill = spec.fill === '--ui-primary' ? style.expected.primary : style.expected.danger;
  const filled = style.controls.filter(button => button.footer &&
    (button.fill === style.expected.primary || button.fill === style.expected.danger || button.image !== 'none'));
  must(filled.length === (spec.fill ? 1 : 0) &&
    (!spec.fill || (filled[0]?.fill === expectedFill && filled[0]?.image === 'none')),
  'footer confirm is the only filled primary or danger action');
  const gutterWidth = gutter(width);
  must(style.dialog.left >= gutterWidth - 0.5 && style.dialog.right <= width - gutterWidth + 0.5 &&
    style.dialog.width <= spec.width + 0.5, 'dialog width and side gutters');
  const close = style.controls.find(control => control.close);
  must(!!close && close.height >= (width < 768 ? 44 : 40) - 0.5, 'close target');
  if (width < 768) {
    must(style.controls.every(control => control.height >= 43.5), 'phone control heights');
  }
  return problems;
}

async function modalTextContrast(modal: Locator, id: string) {
  if (id === 'generatePlanModal') {
    await expect(modal.locator('#svg-container svg')).toBeVisible();
    const back = modal.locator('#muscle-selector-container [data-side="back"]');
    await expect(back).toBeVisible();
    await expect(back).toHaveText('Back');
  }
  const samples = await modal.evaluate(element => {
    type RGB = [number, number, number];
    type Color = { rgb: RGB; alpha: number };
    const parse = (value: string): Color | null => {
      const srgb = value.startsWith('color(srgb ');
      if (!srgb && !/^rgba?\(/.test(value)) return null;
      const channels = value.match(/-?[\d.]+/g)?.map(Number);
      if (!channels || channels.length < 3) return null;
      return { rgb: channels.slice(0, 3).map(channel => channel * (srgb ? 255 : 1)) as RGB, alpha: channels[3] ?? 1 };
    };
    const composite = (color: Color, below: RGB) => color.rgb.map((channel, index) =>
      channel * color.alpha + below[index] * (1 - color.alpha)) as RGB;
    const luminance = (rgb: RGB) => {
      const [r, g, b] = rgb.map(channel => {
        const s = channel / 255;
        return s <= 0.04045 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
      });
      return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };
    const background = (start: Element): RGB | null => {
      const overlays: Color[] = [];
      for (let node: Element | null = start; node; node = node.parentElement) {
        const style = getComputedStyle(node);
        const color = parse(style.backgroundColor);
        if (!color || style.backgroundImage !== 'none') return null;
        if (color.alpha === 1) return overlays.reduceRight((below, above) => composite(above, below), color.rgb);
        if (color.alpha > 0) overlays.push(color);
      }
      return null;
    };
    const caption = '.modal-title, .modal-body p, .modal-body label, .modal-body .form-label, .ui-modal__caption, ' +
      '.preview-label, .preview-badge, #muscle-selector-container [data-side], #muscle-select-all, #muscle-clear-all, ' +
      '.selection-summary, .plan-disclaimer, .modal-footer :is(button, a[href])';
    const readings: {
      text: string; foreground: string; background: RGB | null; ratio: number | null; previewValue?: string;
    }[] = [];
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
    const range = document.createRange();
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const parent = node.parentElement;
      const text = node.textContent?.trim().replace(/\s+/g, ' ');
      if (!text || !parent?.closest(caption) ||
          parent.closest(':disabled, [aria-disabled="true"], [hidden], [aria-hidden="true"], .visually-hidden')) continue;
      if (parent.closest('label')?.control?.matches(':disabled')) continue;
      range.selectNodeContents(node);
      if (!range.getClientRects().length || getComputedStyle(parent).visibility !== 'visible') continue;
      const foreground = getComputedStyle(parent).color;
      const color = parse(foreground);
      const backdrop = background(parent);
      const a = color && backdrop ? luminance(composite(color, backdrop)) : null;
      const b = backdrop ? luminance(backdrop) : null;
      const ratio = a === null || b === null ? null : (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
      const badge = parent.closest('.badge-value')?.closest('.preview-badge');
      const previewValue = badge ? [...badge.classList].find(className => className.startsWith('badge-')) : undefined;
      readings.push({ text, foreground, background: backdrop, ratio, previewValue });
    }
    return readings;
  });
  const problems: string[] = [];
  if (id === 'generatePlanModal') {
    for (const label of ['Training Days', 'Environment', 'Experience', 'Goal', 'Volume:', 'Options', 'Equipment',
      'Preview', 'Priority Muscle Groups', 'Front', 'Back', 'Priority:', 'Select All', 'Clear']) {
      if (!samples.some(sample => sample.text === label)) problems.push(`missing contrast sample for ${label}`);
    }
    for (const badge of ['badge-routines', 'badge-exercises', 'badge-sets', 'badge-reps']) {
      if (!samples.some(sample => sample.previewValue === badge)) problems.push(`missing contrast sample for ${badge}`);
    }
  }
  const captions = id === 'generatePlanModal' ? ['balanced volume across all muscles',
    'select up to 2 muscles to get extra sets on top of the balanced plan', 'Plan covers all muscle groups'] :
    id === 'clearLogModal' ? ['permanently deleted'] : [];
  for (const text of captions) {
    if (!samples.some(sample => sample.text.includes(text))) problems.push(`missing contrast sample for ${text}`);
  }
  for (const sample of samples) {
    if (sample.ratio === null) problems.push(`text contrast for “${sample.text}” has no measurable opaque backdrop`);
    else if (sample.ratio < 4.5) problems.push(`text contrast for “${sample.text}” is ${sample.ratio.toFixed(2)}:1`);
  }
  return { samples, problems };
}

async function routinePreviewGeometry(modal: Locator) {
  const routine = modal.locator('#plan-preview .badge-routines .badge-value');
  await expect(routine).toHaveText('3 Days Split: Workout A, Workout B, Workout C');
  const measured = await routine.evaluate(value => {
    const preview = value.closest<HTMLElement>('#plan-preview')!;
    const body = value.closest<HTMLElement>('.modal-body')!;
    const portTop = body.getBoundingClientRect().top + body.clientTop;
    const before = value.getBoundingClientRect();
    const neededVerticalScroll = before.top < portTop || before.bottom > portTop + body.clientHeight;
    const overflowY = getComputedStyle(body).overflowY;
    // Center the routine vertically without following any horizontal overflow.
    body.scrollTo({
      top: body.scrollTop + (before.top + before.bottom) / 2 - portTop - body.clientHeight / 2,
      left: 0,
      behavior: 'instant',
    });
    const clientBox = (element: HTMLElement) => {
      const bounds = element.getBoundingClientRect();
      const left = bounds.left + element.clientLeft;
      const top = bounds.top + element.clientTop;
      return { left, right: left + element.clientWidth, top, bottom: top + element.clientHeight };
    };
    const range = document.createRange();
    range.selectNodeContents(value);
    const text = Array.from(range.getClientRects(), ({ left, right, top, bottom }) => ({ left, right, top, bottom }));
    return { text, preview: clientBox(preview), scrollport: clientBox(body), neededVerticalScroll, overflowY };
  });
  const { text, preview, scrollport, neededVerticalScroll, overflowY } = measured;
  const problems: string[] = [];
  const tolerance = 0.5;
  if (!text.length) problems.push('routine preview has no rendered text');
  if (text.some(({ left, right }) => left < preview.left - tolerance || right > preview.right + tolerance)) {
    problems.push('routine preview text exceeds the preview box horizontally');
  }
  if (text.some(({ left, right }) => left < scrollport.left - tolerance || right > scrollport.right + tolerance)) {
    problems.push('routine preview text exceeds the modal scrollport horizontally');
  }
  if ((neededVerticalScroll && !['auto', 'scroll'].includes(overflowY)) ||
      text.some(({ top, bottom }) => top < scrollport.top - tolerance || bottom > scrollport.bottom + tolerance)) {
    problems.push('routine preview text cannot be reached by vertical modal scrolling');
  }
  return { measured, problems };
}

/** The shell and each rendered descendant that the legacy light and dark drawer rules style. */
async function drawerStyle(page: Page, width: number) {
  const drawer = page.locator('#vpDrawer');
  await page.locator('#vpToggle').click();
  await expect(drawer).toHaveAttribute('aria-hidden', 'false');
  await expect(drawer.locator('.vp-state')).toContainText('No active volume plan');
  await drawer.evaluate(async element => {
    await new Promise<void>(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve())));
    await Promise.all(element.getAnimations().map(animation => animation.finished));
  });
  const measured = await drawer.evaluate(element => {
    const read = (node: Element, properties: string[]) => {
      const style = getComputedStyle(node);
      return Object.fromEntries(properties.map(property => [property, style.getPropertyValue(property)]));
    };
    const tokens = document.createElement('span');
    tokens.style.cssText = 'position:absolute;visibility:hidden;background:var(--surface-2);box-shadow:var(--shadow-elev-2)';
    element.append(tokens);
    const tokenStyle = getComputedStyle(tokens);
    const expected = { surface: tokenStyle.backgroundColor, shadow: tokenStyle.boxShadow };
    tokens.remove();
    const { left, right, top, bottom, width: renderedWidth } = element.getBoundingClientRect();
    const part = (selector: string, properties: string[]) => read(element.querySelector(selector)!, properties);
    const edges = ['border-left-width', 'border-left-style', 'border-left-color'];
    return {
      expected, bounds: { left, right, top, bottom, width: renderedWidth, height: window.innerHeight },
      shell: read(element, ['position', 'top', 'right', 'z-index', 'display', 'flex-direction', 'width', 'height',
        'background-color', 'background-image', 'backdrop-filter', 'box-shadow', 'transform',
        'border-top-left-radius', 'border-bottom-left-radius', ...edges]),
      transition: read(element, ['transition-property', 'transition-duration', 'transition-timing-function']),
      header: part('.vp-drawer__header', ['display', 'align-items', 'justify-content', 'gap', 'padding',
        'background-color', 'border-bottom-width', 'border-bottom-style', 'border-bottom-color']),
      title: part('.vp-drawer__header h2', ['font-size', 'line-height', 'font-weight', 'margin', 'color']),
      close: part('.vp-close', ['display', 'align-items', 'justify-content', 'width', 'height',
        'border-width', 'border-radius', 'background-color', 'color', 'font-size', 'line-height']),
      body: part('.vp-drawer__body', ['overflow-y', 'padding']),
      state: part('.vp-state', ['border-width', 'border-style', 'border-color', 'border-radius',
        'padding', 'color', 'background-color']),
      paragraph: part('.vp-state p', ['margin']),
    };
  });
  const { shell, expected, bounds, transition, header, title, close, body } = measured;
  const problems: string[] = [];
  if (shell['background-color'] !== expected.surface || shell['box-shadow'] !== expected.shadow ||
      shell['border-top-left-radius'] !== '16px' || shell['border-bottom-left-radius'] !== '16px') {
    problems.push('drawer surface, radius and shadow');
  }
  if (shell.position !== 'fixed' || bounds.left < -0.5 || Math.abs(bounds.right - width) > 0.5 ||
      Math.abs(bounds.top) > 0.5 || Math.abs(bounds.bottom - bounds.height) > 0.5 ||
      Math.abs(bounds.width - Math.min(360, width)) > 0.5) {
    problems.push('drawer containment and size');
  }
  if (![transparent, expected.surface].includes(header['background-color']) ||
      title['font-size'] !== '18px' || title['line-height'] !== '24px' || title['font-weight'] !== '600') {
    problems.push('drawer header');
  }
  if (Number.parseFloat(close.height) < (width < 768 ? 44 : 40) ||
      Number.parseFloat(close.width) < (width < 768 ? 44 : 40)) {
    problems.push('drawer close target');
  }
  if (body.padding !== '16px' || body['overflow-y'] !== 'auto') {
    problems.push('drawer body padding and scrolling');
  }
  if (transition['transition-property'] !== 'transform' || transition['transition-duration'] !== '0.22s' ||
      transition['transition-timing-function'] !== 'ease') {
    problems.push('drawer retains its transform transition');
  }
  return { measured, problems };
}

test('measure migrated overlays and compare the four legacy modals to the control', async ({ page, baseURL }) => {
  const frame = await expectFrameRun(page, baseURL);
  await editVisualPlanFixture(page.request);
  await installFrameSettings(page);
  const reference: unknown[] = [];
  const metrics: unknown[] = [];
  const failures: { id: string; width: number; theme: string; problems: string[] }[] = [];

  for (const width of [390, 1440]) {
    for (const theme of THEMES) {
      let currentRoute = '';
      for (const spec of [...MIGRATED, ...UNMIGRATED]) {
        if (currentRoute !== spec.route) {
          await openFramePass(page, frame.baseURL, spec.route, { width, theme, scale: 6 });
          await fontsLoaded(page);
          currentRoute = spec.route;
        }
        const modal = page.locator('#' + spec.id);
        await toggleModal(modal, true);
        const { expected, ...style } = await modalStyle(modal);
        const entry = { id: spec.id, width, theme, style };
        if ('fill' in spec) {
          const problems = modalProblems({ ...style, expected }, spec, width);
          const contrast = frame.control ? null : await modalTextContrast(modal, spec.id);
          const preview = !frame.control && spec.id === 'generatePlanModal' && width === 390
            ? await routinePreviewGeometry(modal)
            : null;
          if (contrast) problems.push(...contrast.problems);
          if (preview) problems.push(...preview.problems);
          failures.push({ id: spec.id, width, theme, problems });
          metrics.push({
            ...entry,
            ...(contrast && { contrast: contrast.samples }),
            ...(preview && { routinePreview: preview.measured }),
            problems,
          });
        } else {
          reference.push(entry);
        }
        await toggleModal(modal, false);
      }
      await openFramePass(page, frame.baseURL, ROUTES.WORKOUT_PLAN, { width, theme, scale: 6 });
      await expect(planRows(page).first()).toBeVisible();
      await fontsLoaded(page);
      const { measured, problems } = await drawerStyle(page, width);
      failures.push({ id: 'vpDrawer', width, theme, problems });
      metrics.push({ id: 'vpDrawer', width, theme, style: measured, problems });
      await page.locator('#vpDrawer .vp-close').click();
    }
  }

  writeMetrics(frame.run, metrics);
  const referenceJSON = JSON.stringify(reference, null, 2) + '\n';
  fs.writeFileSync(path.join(frame.run, REFERENCE), referenceJSON);
  const fixture = path.join(__dirname, REFERENCE);
  expect(fs.existsSync(fixture), 'capture in ' + frame.run + ' before creating the reference').toBe(true);
  expect(reference).toEqual(JSON.parse(fs.readFileSync(fixture, 'utf8')));
  for (const { id, width, theme, problems } of failures) {
    const label = id + ' at ' + width + ' px, ' + theme;
    if (frame.control) expect.soft(problems.length, label + ' must expose the legacy style').toBeGreaterThan(0);
    else expect.soft(problems, label).toEqual([]);
  }
});
