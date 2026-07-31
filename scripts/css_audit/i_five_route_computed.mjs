/**
 * WP4.4-i — five-route computed-value differential.
 *
 * The packet's success criterion is that computed values are IDENTICAL while
 * ownership becomes honest, and its rollback criterion is any unexplained
 * rendering difference. The committed pixel matrix cannot enforce that here:
 * `visual.spec.ts` is deep-gate-only, carries `maxDiffPixels: 800`, and the
 * Linux ledger already reds every desktop capture of every affected route in at
 * least one theme — so a real regression on those files is indistinguishable
 * from the inherited red by any assertion M7 permits. This differential is the
 * packet's PRIMARY oracle; the pixel matrix corroborates it.
 *
 * It renders all five routes the shared `:is()` family reaches, in both themes
 * at three widths, in rest and hover, and records every computed value the
 * family can influence for every element in the table subtree. Run once per
 * checkout (`--root`) and diff: any differing value is a rollback trigger.
 *
 * It writes nothing outside `--out` and mutates no page: no sentinel is applied,
 * so nothing has to be removed again (M6).
 *
 * Controls, each fatal:
 *   M5  same-CSS control   every context captured twice; any differing record
 *                          invalidates the run before its numbers are quoted
 *   --  DOM presence       every route must render a `.table-calm` with body
 *                          cells; a stale WAL sidecar silently reverted a seeded
 *                          database once (WP4.4-h) and produced td = 0
 *   --  theme applied      `data-theme` must actually land, or the dark half
 *                          measures the light cascade (Inventory B defect 2)
 *   M6a transition settle  a transitioned property reads back its pre-transition
 *                          value, so an unsettled read measures the clock
 *
 * usage:
 *   node scripts/css_audit/i_five_route_computed.mjs \
 *     --root <checkout> --frozen-db artifacts/wp4_4/probe.db \
 *     --out artifacts/wp4_4/i/<label>
 */
import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, copyFileSync, existsSync, unlinkSync, readFileSync } from 'node:fs';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { connect } from 'node:net';

const SELF_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const PORT = 5000;
const BASE_URL = `http://127.0.0.1:${PORT}`;

const argv = process.argv.slice(2);
const arg = (name, fallback = null) => {
  const i = argv.indexOf(name);
  return i < 0 ? fallback : argv[i + 1];
};

const root = resolve(arg('--root', SELF_ROOT));
const outDir = resolve(arg('--out', 'artifacts/wp4_4/i/computed'));
const frozenDb = resolve(arg('--frozen-db', 'artifacts/wp4_4/probe.db'));
const dbPath = resolve(arg('--work-db', 'artifacts/wp4_4/i/probe-work.db'));
const WIDTHS = arg('--widths', '375,768,1440').split(',').map(Number);
const THEMES = ['light', 'dark'];

const ROUTES = [
  { key: 'workout-plan', url: '/workout_plan' },
  { key: 'workout-log', url: '/workout_log' },
  { key: 'weekly-summary', url: '/weekly_summary' },
  { key: 'session-summary', url: '/session_summary' },
  { key: 'progression', url: '/progression' },
];

/**
 * The union of longhands the thirteen family rules declare, expanded from their
 * shorthands, plus the inherited properties they can move (`color`, `font-*`,
 * `letter-spacing`) and enough layout to catch a reflow. A shorthand read back
 * from the CSSOM is not comparable across engines, so every entry is a longhand.
 */
const PROPERTIES = [
  'background-color', 'background-image', 'background-position', 'background-size',
  'background-repeat', 'background-origin', 'background-clip', 'background-attachment',
  'backdrop-filter', '-webkit-backdrop-filter',
  'border-top-width', 'border-right-width', 'border-bottom-width', 'border-left-width',
  'border-top-style', 'border-right-style', 'border-bottom-style', 'border-left-style',
  'border-top-color', 'border-right-color', 'border-bottom-color', 'border-left-color',
  'border-top-left-radius', 'border-top-right-radius',
  'border-bottom-left-radius', 'border-bottom-right-radius',
  'border-collapse', 'border-spacing',
  'box-shadow', 'color', 'font-family', 'font-size', 'font-weight', 'letter-spacing',
  'overflow-x', 'overflow-y',
  'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
  'text-shadow',
  'transition-property', 'transition-duration', 'transition-timing-function', 'transition-delay',
  'display', 'visibility', 'opacity', 'width', 'height',
];

const fileSha = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');

// ---------------------------------------------------------------------------

async function startServer() {
  // A git worktree carries no `.venv`, so the interpreter is allowed to come
  // from elsewhere. `cwd` is what decides which checkout's CSS gets served.
  const candidates = [
    arg('--python'),
    join(root, '.venv/Scripts/python.exe'),
    join(SELF_ROOT, '.venv/Scripts/python.exe'),
  ].filter(Boolean);
  const interpreter = candidates.find((path) => existsSync(path));
  if (!interpreter) throw new Error('no python interpreter found; pass --python');
  const server = spawn(interpreter, ['app.py'], {
    cwd: root,
    env: { ...process.env, DB_FILE: dbPath, FLASK_DEBUG: '0', FLASK_USE_RELOADER: '0', TESTING: '0' },
    stdio: 'ignore',
  });
  const portOpen = () =>
    new Promise((done) => {
      const socket = connect({ host: '127.0.0.1', port: PORT });
      const settle = (value) => { socket.destroy(); done(value); };
      socket.once('connect', () => settle(true));
      socket.once('error', () => settle(false));
      socket.setTimeout(1000, () => settle(false));
    });
  for (let attempt = 0; attempt < 120; attempt += 1) {
    if (await portOpen()) return server;
    await new Promise((done) => setTimeout(done, 500));
  }
  server.kill();
  throw new Error('server did not start');
}

/**
 * Refuse to measure a server this run did not start.
 *
 * `startServer` polls the port, so a server left listening by an earlier run
 * satisfies the wait instantly while the freshly spawned process fails to bind
 * and exits. The run then reports the sha of the checkout's file on disk while
 * having measured a different checkout entirely — a false result that looks
 * clean. This cost a full round of before/after captures once.
 */
async function assertPortFree() {
  const busy = await new Promise((done) => {
    const socket = connect({ host: '127.0.0.1', port: PORT });
    const settle = (value) => { socket.destroy(); done(value); };
    socket.once('connect', () => settle(true));
    socket.once('error', () => settle(false));
    socket.setTimeout(1000, () => settle(false));
  });
  if (busy) {
    throw new Error(
      `port ${PORT} is already in use; another server would be measured instead of --root. ` +
      'Stop it first — do not assume it serves the same checkout.'
    );
  }
}

/** The served bytes, not the bytes on disk, are what the browser cascaded. */
async function assertServedCssMatches(expectedSha) {
  const response = await fetch(`${BASE_URL}/static/css/components.css`);
  if (!response.ok) throw new Error(`could not fetch components.css: ${response.status}`);
  const servedSha = createHash('sha256').update(Buffer.from(await response.arrayBuffer())).digest('hex');
  if (servedSha !== expectedSha) {
    throw new Error(
      `the server is serving components.css ${servedSha} but --root has ${expectedSha}. ` +
      'A different checkout is being measured.'
    );
  }
  return servedSha;
}

async function settlePage(page) {
  return page.evaluate(() => {
    for (const animation of document.getAnimations({ subtree: true })) {
      if (animation.constructor?.name === 'CSSTransition') { animation.finish(); continue; }
      const iterations = animation.effect?.getComputedTiming?.().iterations ?? 1;
      if (iterations === Infinity) { animation.currentTime = 0; animation.pause(); }
      else { animation.finish(); }
    }
  });
}

/** Capture one context. Returns { records, presence }. */
async function capture(browser, route, theme, width, hover) {
  const context = await browser.newContext({
    viewport: { width, height: 900 },
    colorScheme: theme,
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();
  await page.goto(BASE_URL + route.url, { waitUntil: 'networkidle' });
  await page.evaluate((t) => {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('theme', t);
  }, theme);
  await page.waitForTimeout(120);

  if (hover) {
    const row = page.locator('table.table-calm tbody tr').first();
    if (await row.count()) await row.hover({ force: true }).catch(() => {});
    await page.waitForTimeout(120);
  }

  await settlePage(page);

  const result = await page.evaluate((props) => {
    const domPath = (element) => {
      const parts = [];
      let node = element;
      while (node && node.nodeType === 1 && node !== document.documentElement) {
        const parent = node.parentElement;
        if (!parent) break;
        parts.unshift(node.tagName.toLowerCase() + ':nth-child(' + ([...parent.children].indexOf(node) + 1) + ')');
        node = parent;
      }
      return 'html' + (parts.length ? ' > ' + parts.join(' > ') : '');
    };
    const nodes = [...document.querySelectorAll('table.table-calm, table.table-calm *')];
    const records = {};
    for (const node of nodes) {
      const style = getComputedStyle(node);
      const entry = {};
      for (const prop of props) entry[prop] = style.getPropertyValue(prop);
      records[domPath(node)] = entry;
    }
    return {
      records,
      presence: {
        theme: document.documentElement.getAttribute('data-theme'),
        tables: document.querySelectorAll('table.table-calm').length,
        headerCells: document.querySelectorAll('table.table-calm thead th').length,
        bodyCells: document.querySelectorAll('table.table-calm tbody td').length,
      },
    };
  }, PROPERTIES);

  await context.close();
  return result;
}

// ---------------------------------------------------------------------------

async function main() {
  mkdirSync(outDir, { recursive: true });
  mkdirSync(dirname(dbPath), { recursive: true });

  // A stale WAL sidecar silently reverted a freshly seeded database during
  // WP4.4-h and produced td = 0. Delete both before copying, every time.
  for (const suffix of ['', '-wal', '-shm']) {
    const path = dbPath + suffix;
    if (existsSync(path)) unlinkSync(path);
  }
  copyFileSync(frozenDb, dbPath);

  const cssPath = join(root, 'static/css/components.css');
  const meta = {
    root,
    componentsCssSha256: fileSha(cssPath),
    frozenDbSha256: fileSha(frozenDb),
    widths: WIDTHS,
    themes: THEMES,
    routes: ROUTES.map((r) => r.key),
    properties: PROPERTIES.length,
  };

  await assertPortFree();
  const server = await startServer();
  meta.servedCssSha256 = await assertServedCssMatches(meta.componentsCssSha256);
  const browser = await chromium.launch();
  const contexts = {};
  const presence = {};
  const failures = [];

  try {
    for (const route of ROUTES) {
      for (const theme of THEMES) {
        for (const width of WIDTHS) {
          for (const hover of [false, true]) {
            const label = `${route.key}|${theme}|${width}|${hover ? 'hover' : 'rest'}`;
            const first = await capture(browser, route, theme, width, hover);

            // M5 same-CSS control: the identical context, captured again.
            const second = await capture(browser, route, theme, width, hover);
            const a = JSON.stringify(first.records);
            const b = JSON.stringify(second.records);
            if (a !== b) failures.push(`${label}: same-CSS control differed`);

            if (first.presence.tables === 0) failures.push(`${label}: no .table-calm rendered`);
            if (first.presence.bodyCells === 0) failures.push(`${label}: zero body cells`);
            if (first.presence.theme !== theme) {
              failures.push(`${label}: data-theme is ${JSON.stringify(first.presence.theme)}`);
            }

            contexts[label] = first.records;
            presence[label] = first.presence;
            process.stdout.write(`  ${label}: ${Object.keys(first.records).length} elements\n`);
          }
        }
      }
    }
  } finally {
    await browser.close();
    server.kill();
  }

  writeFileSync(join(outDir, 'computed.json'), JSON.stringify({ meta, presence, contexts }, null, 1));
  writeFileSync(join(outDir, 'meta.json'), JSON.stringify({ meta, presence, failures }, null, 1));

  if (failures.length) {
    console.error('\nFAIL — controls unclean:');
    for (const failure of failures) console.error('  ' + failure);
    process.exit(1);
  }
  console.log('\nPASS — all controls clean');
  console.log('components.css sha256: ' + meta.componentsCssSha256);
}

await main();
