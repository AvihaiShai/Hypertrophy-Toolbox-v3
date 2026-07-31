/**
 * WP4.4-j — whole-page computed-value differential across every route, in both
 * themes.
 *
 * j's rollback criteria are asymmetric and both are absolute: *any* dark-mode
 * rendering difference, and *any* light-mode difference at all — a dark-only
 * file that changes light rendering means the classification was wrong. So this
 * measures both themes and treats a light difference as the louder failure.
 *
 * Scope is the whole document, not a subtree. `theme-dark.css` is not confined
 * to one component family the way the `:is()` family in WP4.4-i was; its rules
 * reach tables, forms, cards, the navbar, headings and the welcome hero, so any
 * subtree scope would be a guess about where a regression may appear.
 *
 * Controls, each fatal:
 *   M5  same-CSS control   every context captured twice; any differing record
 *                          invalidates the run before its numbers are quoted
 *   --  port free          refuse to measure a server this run did not start
 *   --  served digest      the bytes the browser cascaded, not the bytes on disk
 *   --  theme applied      `data-theme` must actually land, or the dark half
 *                          measures the light cascade
 *   --  DOM presence       every context must find a nonzero element count
 *   M6a transition settle  a transitioned property reads back its pre-transition
 *                          value, so an unsettled read measures the clock
 *
 * usage:
 *   node scripts/css_audit/j_theme_differential.mjs \
 *     --root <checkout> --frozen-db <db> --out artifacts/wp4_4/j/<label>
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
const outDir = resolve(arg('--out', 'artifacts/wp4_4/j/computed'));
const frozenDb = resolve(arg('--frozen-db', 'artifacts/wp4_4/j/probe.db'));
const dbPath = resolve(arg('--work-db', 'artifacts/wp4_4/j/probe-work.db'));
const WIDTHS = arg('--widths', '375,768,1440').split(',').map(Number);
const THEMES = ['light', 'dark'];

const ONLY = arg('--routes') ? new Set(arg('--routes').split(',')) : null;

const ROUTES = [
  { key: 'welcome', url: '/' },
  { key: 'workout-plan', url: '/workout_plan' },
  { key: 'workout-log', url: '/workout_log' },
  { key: 'weekly-summary', url: '/weekly_summary' },
  { key: 'session-summary', url: '/session_summary' },
  { key: 'progression', url: '/progression' },
  { key: 'body-composition', url: '/body_composition' },
  { key: 'volume-splitter', url: '/volume_splitter' },
  { key: 'user-profile', url: '/user_profile' },
  { key: 'backup', url: '/backup' },
  { key: 'fatigue', url: '/fatigue' },
];

/**
 * The union of properties `theme-dark.css` can move, expanded to longhands. A
 * shorthand read back from the CSSOM is not comparable, so every entry is a
 * longhand.
 */
const PROPERTIES = [
  'background-color', 'background-image', 'background-clip', 'background-origin',
  'border-top-width', 'border-right-width', 'border-bottom-width', 'border-left-width',
  'border-top-style', 'border-right-style', 'border-bottom-style', 'border-left-style',
  'border-top-color', 'border-right-color', 'border-bottom-color', 'border-left-color',
  'border-top-left-radius', 'border-top-right-radius',
  'border-bottom-left-radius', 'border-bottom-right-radius',
  'box-shadow', 'color', 'opacity', 'visibility', 'display',
  'font-weight', 'text-shadow', 'outline-color', 'outline-style', 'outline-width',
  'transition-duration', 'transition-property', 'animation-duration', 'animation-name',
  'backdrop-filter', '-webkit-backdrop-filter', 'fill', 'stroke',
];

const fileSha = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');

async function probePort() {
  return new Promise((done) => {
    const socket = connect({ host: '127.0.0.1', port: PORT });
    const settle = (v) => { socket.destroy(); done(v); };
    socket.once('connect', () => settle(true));
    socket.once('error', () => settle(false));
    socket.setTimeout(1000, () => settle(false));
  });
}

async function startServer() {
  if (await probePort()) {
    throw new Error(`port ${PORT} is already in use; another server would be measured instead of ${root}`);
  }
  const python = [arg('--python'), join(root, '.venv/Scripts/python.exe'), join(SELF_ROOT, '.venv/Scripts/python.exe')]
    .filter(Boolean).find((p) => existsSync(p));
  if (!python) throw new Error('no python interpreter found; pass --python');
  const server = spawn(python, ['app.py'], {
    cwd: root,
    env: { ...process.env, DB_FILE: dbPath, FLASK_DEBUG: '0', FLASK_USE_RELOADER: '0', TESTING: '0' },
    stdio: 'ignore',
  });
  let exited = null;
  server.once('exit', (code) => { exited = code ?? 'signal'; });
  for (let attempt = 0; attempt < 120; attempt += 1) {
    if (exited !== null) throw new Error(`server exited (${exited}) before binding`);
    if (await probePort()) return server;
    await new Promise((d) => setTimeout(d, 500));
  }
  server.kill();
  throw new Error('server did not start');
}

async function assertServed(expected) {
  const response = await fetch(`${BASE_URL}/static/css/theme-dark.css`);
  if (!response.ok) throw new Error(`could not fetch theme-dark.css: ${response.status}`);
  const served = createHash('sha256').update(Buffer.from(await response.arrayBuffer())).digest('hex');
  if (served !== expected) {
    throw new Error(`server serves theme-dark.css ${served} but ${root} has ${expected}`);
  }
  return served;
}

async function captureContext(browser, route, theme, width) {
  const context = await browser.newContext({
    viewport: { width, height: 900 },
    colorScheme: theme === 'dark' ? 'dark' : 'light',
    reducedMotion: 'no-preference',
  });
  const page = await context.newPage();
  try {
    await page.goto(`${BASE_URL}${route.url}`, { waitUntil: 'networkidle' });
    await page.evaluate((v) => document.documentElement.setAttribute('data-theme', v), theme);
    const applied = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    if (applied !== theme) throw new Error(`data-theme did not land on ${route.key}|${theme}|${width}`);
    // Freeze the animation timeline at the browser level before anything is
    // read. The welcome hero runs eight `animation-iteration-count: infinite`
    // elements that the WP4.4-a ledger records as having no rest state, and
    // pausing them from script races animations that start after the call --
    // that intermittently reddened this run's own same-CSS control. Setting the
    // CDP playback rate to 0 stops the timeline for animations that already
    // exist and any that begin later, and it mutates no CSS, so the cascade
    // under test is untouched.
    const cdp = await page.context().newCDPSession(page);
    await cdp.send('Animation.enable');
    await cdp.send('Animation.setPlaybackRate', { playbackRate: 0 });
    await page.evaluate(() => {
      for (const animation of document.getAnimations({ subtree: true })) {
        if (animation.constructor?.name === 'CSSTransition') { animation.finish(); continue; }
        const iterations = animation.effect?.getComputedTiming?.().iterations ?? 1;
        if (iterations === Infinity) { animation.currentTime = 0; animation.pause(); }
        else { animation.finish(); }
      }
    });
    const records = await page.evaluate((props) => {
      const path = (el) => {
        const parts = [];
        for (let n = el; n && n.nodeType === 1 && n !== document.documentElement; n = n.parentElement) {
          const i = Array.prototype.indexOf.call(n.parentElement?.children ?? [], n) + 1;
          parts.unshift(`${n.tagName.toLowerCase()}:nth-child(${i})`);
        }
        return parts.join('>');
      };
      const out = {};
      for (const el of document.querySelectorAll('body, body *')) {
        const cs = getComputedStyle(el);
        const values = {};
        for (const p of props) values[p] = cs.getPropertyValue(p);
        out[path(el)] = values;
      }
      return out;
    }, PROPERTIES);
    return { records, count: Object.keys(records).length };
  } finally {
    await context.close();
  }
}

// ---------------------------------------------------------------------------

mkdirSync(outDir, { recursive: true });
if (!existsSync(frozenDb)) throw new Error(`frozen DB not found: ${frozenDb}`);
mkdirSync(dirname(dbPath), { recursive: true });
for (const sidecar of [`${dbPath}-wal`, `${dbPath}-shm`]) {
  if (existsSync(sidecar)) unlinkSync(sidecar);
}
copyFileSync(frozenDb, dbPath);

const onDisk = fileSha(join(root, 'static/css/theme-dark.css'));
const server = await startServer();
const contexts = {};
const presence = {};
const failures = [];
const controlDetail = {};
let served;
try {
  served = await assertServed(onDisk);
  const browser = await chromium.launch();
  try {
    for (const route of ROUTES.filter((r) => !ONLY || ONLY.has(r.key))) {
      for (const theme of THEMES) {
        for (const width of WIDTHS) {
          const label = `${route.key}|${theme}|${width}`;
          const first = await captureContext(browser, route, theme, width);
          // M5: the same context twice. A run whose own captures disagree
          // cannot be quoted, whatever the before/after diff says.
          const second = await captureContext(browser, route, theme, width);
          const a = JSON.stringify(first.records);
          const b = JSON.stringify(second.records);
          if (a !== b) {
            // Record which elements moved. A count alone cannot distinguish a
            // harness defect from the animated elements the WP4.4-a ledger
            // already records as having no rest state.
            const moved = [];
            for (const key of Object.keys(first.records)) {
              const x = first.records[key]; const y = second.records[key] ?? {};
              for (const prop of Object.keys(x)) {
                if (x[prop] !== y[prop]) moved.push({ element: key, prop, a: x[prop], b: y[prop] });
              }
            }
            failures.push(`${label}: same-CSS control differed in ${moved.length} value(s)`);
            controlDetail[label] = moved.slice(0, 40);
          }
          if (first.count === 0) failures.push(`${label}: zero elements captured`);
          contexts[label] = first.records;
          presence[label] = { elements: first.count };
          console.log(`  ${label}: ${first.count} elements`);
        }
      }
    }
  } finally {
    await browser.close();
  }
} finally {
  server.kill();
}

writeFileSync(join(outDir, 'computed.json'), JSON.stringify({ contexts }));
writeFileSync(join(outDir, 'meta.json'), `${JSON.stringify({
  meta: {
    root,
    themeDarkCssSha256: onDisk,
    servedThemeDarkCssSha256: served,
    // The frozen INPUT, not the work copy: Flask mutates the work database on
    // startup (initializers, auto-backup), so hashing it after the run records
    // a value that differs between two halves fed identical input and makes the
    // diff refuse a legitimate pair.
    frozenDbSha256: fileSha(frozenDb),
    workDbSha256AfterRun: fileSha(dbPath),
    widths: WIDTHS,
    themes: THEMES,
    routes: ROUTES.map((r) => r.key),
    properties: PROPERTIES,
    controlsPassed: failures.length === 0,
  },
  presence,
  failures,
  controlDetail,
}, null, 2)}\n`);

console.log(`\ntheme-dark.css sha256: ${onDisk}`);
console.log(failures.length ? `FAIL — ${failures.length} control failure(s)` : 'PASS — all controls clean');
process.exit(failures.length ? 1 : 0);
