/**
 * Proof harness for the `e2e/visual-helpers.ts` determinism-layer correction.
 *
 * The correction excludes exactly one element from the dark surface-flattening
 * rule. Because that rule is `!important` and computes to (0,3,1), it can only
 * be a no-op where something in the product stylesheets already out-specifies
 * it — so "no-op" is a claim that has to be measured, not argued.
 *
 * Run against a checkout whose product CSS is UNCHANGED (i.e. `main`). Both
 * variants are applied to the same page in the same session, so any difference
 * is attributable to the selector and nothing else. No committed baseline is
 * read or written; this compares the two renderings directly.
 *
 * Emits four things per context:
 *   matchDelta   elements matched by OLD but not NEW (and vice versa)
 *   computed     computed-value differences over every [data-visual-surface]
 *                element and all of its descendants
 *   fullPage     byte comparison of the full-page screenshot
 *   element      byte comparison of an element-scoped Progression-table shot
 *
 * usage:
 *   node scripts/css_audit/visual_helper_band_proof.mjs \
 *     --root <checkout> --python <exe> --seed <db> --work-db <db> --out <dir>
 */
import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync, copyFileSync, existsSync, unlinkSync, readFileSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { connect } from 'node:net';
import { createHash } from 'node:crypto';

const arg = (n, d = null) => { const i = process.argv.indexOf(n); return i < 0 ? d : process.argv[i + 1]; };
const root = resolve(arg('--root'));
const outDir = resolve(arg('--out'));
const seed = resolve(arg('--seed'));
const dbPath = resolve(arg('--work-db'));
const python = arg('--python');
const PORT = 5000;

const ROUTES = [
  ['welcome', '/'], ['workout-plan', '/workout_plan'], ['workout-log', '/workout_log'],
  ['weekly-summary', '/weekly_summary'], ['session-summary', '/session_summary'],
  ['progression', '/progression'], ['body-composition', '/body_composition'],
  ['volume-splitter', '/volume_splitter'], ['user-profile', '/user_profile'],
  ['backup', '/backups'], ['fatigue', '/fatigue'],
];
const WIDTHS = [[375, 812], [768, 1024], [1440, 900]];
const THEMES = ['light', 'dark'];

const SURFACE = "html[data-theme='dark'] [data-visual-surface][data-visual-surface]";
const EXCLUDED = `${SURFACE}:where(:not(.progression-plan-container .table-calm))`;

/** The rule as shipped before the correction: one block, every property. */
const OLD_RULES = `
  ${SURFACE} {
    background: var(--visual-surface-1) !important; background-image: none !important;
    border-color: #273145 !important; border-radius: 0 !important;
    box-shadow: none !important; text-shadow: none !important;
  }`;

/** The correction: flattening set unchanged, border geometry withheld from one element. */
const NEW_RULES = `
  ${SURFACE} {
    background: var(--visual-surface-1) !important; background-image: none !important;
    box-shadow: none !important; text-shadow: none !important;
  }
  ${EXCLUDED} {
    border-color: #273145 !important; border-radius: 0 !important;
  }`;

/** The selector whose match set is compared for the match-delta proof. */
const MATCH_SELECTOR = { old: SURFACE, new: EXCLUDED };

/** The determinism CSS, verbatim from prepareForScreenshot, with the surface rule parameterised. */
const determinismCss = (surfaceRules) => `
  *, *::before, *::after {
    animation-delay: 0s !important; animation-duration: 0s !important;
    animation-iteration-count: 1 !important; transition-duration: 0s !important;
    transition-delay: 0s !important; backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
  }
  html { scroll-behavior: auto !important; }
  html { --visual-surface-0: #eef1f6; --visual-surface-1: #f7f9fc; }
  html[data-theme='dark'] { --visual-surface-0: #090c16; --visual-surface-1: #0d101d; }
  html[data-theme] body, body {
    background: var(--visual-surface-0) !important; background-attachment: scroll !important;
  }
  ${surfaceRules}
  html[data-theme='dark'] [data-page="workout-plan"] [data-visual-header]::before { background: transparent !important; }
  html[data-theme='dark'] [data-page="workout-plan"] [data-visual-accent] {
    background: #4f8cff !important; border-radius: 0 !important; box-shadow: none !important;
    transform: none !important; transition: none !important;
  }
  input, textarea { caret-color: transparent !important; }
  select { appearance: none !important; -webkit-appearance: none !important; background-image: none !important; }
  [data-visual-control], input, textarea, select, input[type="number"] {
    border-radius: 0 !important; box-shadow: none !important; text-shadow: none !important;
  }
  [data-testid="navbar"] a::before, [data-testid="navbar"] button::before {
    background-color: transparent !important; border-radius: 0 !important;
    transform: none !important; transition: none !important;
  }
  [data-visual-dropdown-toggle]::after { border-color: transparent !important; }
  [data-visual-icon] { visibility: hidden !important; }
  [data-visual-scale-control] { background: transparent !important; border-color: transparent !important; color: transparent !important; }
  input[type="number"]::-webkit-outer-spin-button, input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none !important; margin: 0 !important;
  }
  ::-webkit-scrollbar { display: none; }
`;

const sha = (buf) => createHash('sha256').update(buf).digest('hex');

/**
 * Refuse to measure a server this run did not start. `startServer` polls the
 * port, so a server left listening by an earlier run satisfies the wait
 * instantly while the freshly spawned process fails to bind and exits -- the
 * run then measures a different checkout while reporting this one's --root.
 */
async function assertPortFree() {
  const busy = await new Promise((d) => {
    const s = connect({ host: '127.0.0.1', port: PORT });
    const f = (v) => { s.destroy(); d(v); };
    s.once('connect', () => f(true)); s.once('error', () => f(false)); s.setTimeout(1000, () => f(false));
  });
  if (busy) throw new Error(`port ${PORT} is already in use; stop it before measuring`);
}

async function assertServedCss(expected) {
  const r = await fetch(`http://127.0.0.1:${PORT}/static/css/components.css`);
  if (!r.ok) throw new Error(`could not fetch components.css: ${r.status}`);
  const got = createHash('sha256').update(Buffer.from(await r.arrayBuffer())).digest('hex');
  if (got !== expected) throw new Error(`server serves components.css ${got}, --root has ${expected}`);
  return got;
}

async function startServer() {
  for (const s of ['', '-wal', '-shm']) { const p = dbPath + s; if (existsSync(p)) unlinkSync(p); }
  mkdirSync(dirname(dbPath), { recursive: true });
  copyFileSync(seed, dbPath);
  const server = spawn(python, ['app.py'], {
    cwd: root,
    env: { ...process.env, DB_FILE: dbPath, FLASK_DEBUG: '0', FLASK_USE_RELOADER: '0', TESTING: '0' },
    stdio: 'ignore',
  });
  const open = () => new Promise((d) => {
    const s = connect({ host: '127.0.0.1', port: PORT });
    const f = (v) => { s.destroy(); d(v); };
    s.once('connect', () => f(true)); s.once('error', () => f(false)); s.setTimeout(1000, () => f(false));
  });
  for (let i = 0; i < 120; i += 1) { if (await open()) return server; await new Promise((r) => setTimeout(r, 500)); }
  server.kill(); throw new Error('server did not start');
}

/** Apply one variant to a freshly loaded page and read everything back. */
async function measure(page, url, theme, surfaceRules, matchSelector) {
  await page.goto(`http://127.0.0.1:${PORT}${url}`, { waitUntil: 'networkidle' });
  await page.evaluate((t) => {
    localStorage.setItem('darkMode', t === 'dark' ? 'true' : 'false');
    document.documentElement.setAttribute('data-theme', t);
  }, theme);
  await page.addStyleTag({ content: determinismCss(surfaceRules) });
  await page.evaluate(async () => {
    document.querySelectorAll('[data-visual-control], input, textarea, select').forEach((el) => {
      el.style.setProperty('border-radius', '0', 'important');
      el.style.setProperty('box-shadow', 'none', 'important');
      el.style.setProperty('text-shadow', 'none', 'important');
    });
    await document.fonts.ready;
    window.scrollTo(0, 0);
    for (const a of document.getAnimations({ subtree: true })) {
      if (a.constructor?.name === 'CSSTransition') { a.finish(); continue; }
      const it = a.effect?.getComputedTiming?.().iterations ?? 1;
      if (it === Infinity) { a.currentTime = 0; a.pause(); } else { a.finish(); }
    }
  });

  const data = await page.evaluate((selector) => {
    const path = (el) => {
      const parts = []; let n = el;
      while (n && n.nodeType === 1 && n !== document.documentElement) {
        const p = n.parentElement; if (!p) break;
        parts.unshift(n.tagName.toLowerCase() + ':nth-child(' + ([...p.children].indexOf(n) + 1) + ')');
        n = p;
      }
      return 'html' + (parts.length ? ' > ' + parts.join(' > ') : '');
    };
    const matched = [...document.querySelectorAll(selector)].map(path);
    // Every surface and everything inside it - the flattening rule sets inherited
    // properties (text-shadow, border-color), so descendants must be read too.
    const scope = new Set();
    for (const s of document.querySelectorAll('[data-visual-surface]')) {
      scope.add(s);
      for (const d of s.querySelectorAll('*')) scope.add(d);
    }
    const computed = {};
    for (const el of scope) {
      const cs = getComputedStyle(el);
      const e = {};
      for (let i = 0; i < cs.length; i += 1) { const p = cs[i]; e[p] = cs.getPropertyValue(p); }
      const r = el.getBoundingClientRect();
      e.__rect = [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(',');
      computed[path(el)] = e;
    }
    return { matched, computed };
  }, matchSelector);

  const fullPage = await page.screenshot({ fullPage: true, animations: 'disabled', caret: 'hide' });
  let element = null;
  const table = page.locator('.progression-plan-container table.table-calm').first();
  if (await table.count()) {
    element = await table.screenshot({ animations: 'disabled', caret: 'hide' });
  }
  return { ...data, fullPage, element };
}

async function main() {
  mkdirSync(outDir, { recursive: true });
  await assertPortFree();
  const server = await startServer();
  const expectedCss = createHash('sha256')
    .update(readFileSync(join(root, 'static/css/components.css'))).digest('hex');
  const servedCss = await assertServedCss(expectedCss);
  console.log(`serving components.css ${servedCss} from ${root}
`);
  const browser = await chromium.launch();
  const report = { root, contexts: {}, totals: { matchDelta: 0, computed: 0, fullPagePixels: 0, elementPixels: 0, dirtyControls: 0 } };

  try {
    for (const [name, url] of ROUTES) {
      for (const theme of THEMES) {
        for (const [w, h] of WIDTHS) {
          const label = `${name}|${theme}|${w}`;
          const ctx = await browser.newContext({ viewport: { width: w, height: h }, colorScheme: theme, deviceScaleFactor: 1 });
          const page = await ctx.newPage();

          const before = await measure(page, url, theme, OLD_RULES, MATCH_SELECTOR.old);
          // Same-CSS control (M5). Two loads of the identical variant. Any
          // difference here is page nondeterminism, not the correction, and a
          // context whose control is dirty cannot testify about the correction.
          const control = await measure(page, url, theme, OLD_RULES, MATCH_SELECTOR.old);
          const after = await measure(page, url, theme, NEW_RULES, MATCH_SELECTOR.new);
          await ctx.close();

          const onlyOld = before.matched.filter((p) => !after.matched.includes(p));
          const onlyNew = after.matched.filter((p) => !before.matched.includes(p));

          const compare = (a, b) => {
            const out = [];
            for (const [p, vals] of Object.entries(a.computed)) {
              const other = b.computed[p];
              if (!other) { out.push({ path: p, property: '__missing', before: 'present', after: 'absent' }); continue; }
              for (const [k, v] of Object.entries(vals)) {
                if (other[k] !== v) out.push({ path: p, property: k, before: v, after: other[k] });
              }
            }
            return out;
          };
          const diffs = compare(before, after);
          const controlDiffs = compare(before, control);

          const fullPageSame = sha(before.fullPage) === sha(after.fullPage);
          const controlPageSame = sha(before.fullPage) === sha(control.fullPage);
          const shot = (m) => (m.element ? sha(m.element) : null);
          const elementSame = shot(before) === shot(after);
          const controlElementSame = shot(before) === shot(control);

          report.contexts[label] = {
            matchedOld: before.matched.length,
            matchedNew: after.matched.length,
            onlyOld, onlyNew,
            computedDifferences: diffs.length,
            computedSample: diffs.slice(0, 10),
            fullPageIdentical: fullPageSame,
            elementIdentical: elementSame,
            control: {
              computedDifferences: controlDiffs.length,
              fullPageIdentical: controlPageSame,
              elementIdentical: controlElementSame,
              clean: controlDiffs.length === 0 && controlPageSame && controlElementSame,
            },
          };
          report.totals.matchDelta += onlyOld.length + onlyNew.length;
          report.totals.computed += diffs.length;
          if (!fullPageSame) report.totals.fullPagePixels += 1;
          if (!elementSame) report.totals.elementPixels += 1;

          process.stdout.write(
            `  ${label.padEnd(34)} match ${before.matched.length}->${after.matched.length}` +
            ` delta ${onlyOld.length + onlyNew.length}  computed ${diffs.length}` +
            `  page ${fullPageSame ? 'same' : 'DIFF'}  el ${elementSame ? 'same' : 'DIFF'}\n`
          );
        }
      }
    }
  } finally {
    await browser.close();
    server.kill();
  }

  writeFileSync(join(outDir, 'helper-band-proof.json'), JSON.stringify(report, null, 1));
  console.log('\n--- TOTALS ---');
  console.log(`match-set delta elements : ${report.totals.matchDelta}`);
  console.log(`computed differences     : ${report.totals.computed}`);
  console.log(`full-page shots differing: ${report.totals.fullPagePixels}`);
  console.log(`element shots differing  : ${report.totals.elementPixels}`);
  console.log(`contexts w/ dirty control: ${report.totals.dirtyControls}`);

  const signal = Object.entries(report.contexts).filter(
    ([, c]) => c.control.clean && (c.computedDifferences || !c.fullPageIdentical || !c.elementIdentical)
  );
  console.log(`
control-clean contexts still showing ANY difference: ${signal.length}`);
  for (const [k, c] of signal) {
    console.log(`  ${k}  computed ${c.computedDifferences}  page ${c.fullPageIdentical ? 'same' : 'DIFF'}  el ${c.elementIdentical ? 'same' : 'DIFF'}`);
  }
}

await main();
