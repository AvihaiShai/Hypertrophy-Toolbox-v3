/**
 * WP4.4-i — element-scoped pixel differential.
 *
 * The computed-value differential proves the cascade resolves identically. This
 * proves the rasteriser agrees, at the only scope where the packet could change
 * anything: the `.table-calm` subtree the shared `:is()` family styles.
 *
 * It exists because the committed pixel matrix cannot falsify this repair.
 * `visual.spec.ts` runs only under the manual deep gate, screenshots through
 * `visualScreenshotOptions` (`maxDiffPixels: 800`), and the Linux ledger already
 * reds every desktop capture of every affected route in at least one theme — so a
 * real regression there is indistinguishable from the inherited red. A
 * full-viewport capture has the same problem in reverse: unrelated chrome
 * (scrollbars, fonts, focus rings) produces noise that swamps a table-sized
 * signal. Scoping the capture to the element under test removes both.
 *
 * The element-scoped capture that previously backed this claim was a gitignored
 * one-off (`artifacts/wp4_4/i/prog_fullpage.mjs`), which this document's own A11
 * rule forbids as evidence. This script is the committed replacement.
 *
 * Both roots are served in turn on the same port by this one process, so the two
 * halves cannot differ in browser build, viewport, device scale factor, database
 * or capture settings — only in the bytes of `components.css`.
 *
 * Controls, each fatal:
 *   port free        refuse to measure a server this run did not start
 *   served digest    the bytes the browser cascaded, not the bytes on disk
 *   digests differ   the two halves must serve different `components.css`, or
 *                    the comparison is a same-file self-test that always passes
 *   presence         every context must find the element and a nonzero box
 *   settle           transitions are finished before the shutter, or the capture
 *                    measures the clock
 *
 * Byte-identical PNGs mean zero differing pixels. When digests differ the run
 * decodes both images on a canvas and reports the exact differing-pixel count,
 * so a mismatch is quantified rather than merely flagged.
 *
 * usage:
 *   node scripts/css_audit/i_element_pixel_diff.mjs \
 *     --before-root <checkout> --after-root <checkout> \
 *     --frozen-db artifacts/wp4_4/i/probe-r3.db \
 *     --out artifacts/wp4_4/i/r3-pixel
 */
import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, copyFileSync, existsSync, readFileSync } from 'node:fs';
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

// The same-state control: point both halves at one checkout and assert the
// rasteriser is deterministic across two full capture cycles. Without it a
// differing capture cannot be attributed — a flake and a regression look the
// same. This is the pixel analogue of i_diff_computed's --expect-same-css.
const expectSameCss = argv.includes('--expect-same-css');
const beforeRoot = resolve(arg('--before-root'));
const afterRoot = resolve(arg('--after-root'));
const outDir = resolve(arg('--out', 'artifacts/wp4_4/i/r3-pixel'));
const frozenDb = resolve(arg('--frozen-db', 'artifacts/wp4_4/i/probe-r3.db'));
const dbPath = resolve(arg('--work-db', 'artifacts/wp4_4/i/pixel-work.db'));
const WIDTHS = arg('--widths', '375,768,1440').split(',').map(Number);
const THEMES = ['light', 'dark'];

const ROUTES = [
  { key: 'workout-plan', url: '/workout_plan' },
  { key: 'workout-log', url: '/workout_log' },
  { key: 'weekly-summary', url: '/weekly_summary' },
  { key: 'session-summary', url: '/session_summary' },
  { key: 'progression', url: '/progression' },
];

/** The element the shared family styles — the whole scope of any i regression. */
const TARGET = 'table.table-calm';

/**
 * Per-route minimum body rows, mirroring `i_five_route_computed.mjs`.
 * `/progression` is the only route the repair de-weights, and
 * `i_seed_probe_db.py` seeds six open goals so the even-row, last-row and hover
 * rules all have something to match.
 */
const MIN_ROWS = { progression: 6 };

const sha = (buffer) => createHash('sha256').update(buffer).digest('hex');
const fileSha = (path) => sha(readFileSync(path));

async function probePort() {
  return new Promise((done) => {
    const socket = connect({ host: '127.0.0.1', port: PORT });
    const settle = (value) => { socket.destroy(); done(value); };
    socket.once('connect', () => settle(true));
    socket.once('error', () => settle(false));
    socket.setTimeout(1000, () => settle(false));
  });
}

async function startServer(root) {
  if (await probePort()) {
    throw new Error(`port ${PORT} is already in use; another server would be measured instead of ${root}.`);
  }
  const python = [join(root, '.venv/Scripts/python.exe'), join(SELF_ROOT, '.venv/Scripts/python.exe')]
    .find((path) => existsSync(path));
  if (!python) throw new Error(`no python interpreter found for ${root}`);
  const server = spawn(python, ['app.py'], {
    cwd: root,
    env: { ...process.env, DB_FILE: dbPath, FLASK_DEBUG: '0', FLASK_USE_RELOADER: '0', TESTING: '0' },
    stdio: 'ignore',
  });
  let exited = null;
  server.once('exit', (code) => { exited = code ?? 'signal'; });
  for (let attempt = 0; attempt < 120; attempt += 1) {
    if (exited !== null) throw new Error(`server for ${root} exited (${exited}) before binding`);
    if (await probePort()) return server;
    await new Promise((done) => setTimeout(done, 500));
  }
  server.kill();
  throw new Error(`server for ${root} did not start`);
}

async function stopServer(server) {
  server.kill();
  for (let attempt = 0; attempt < 60; attempt += 1) {
    if (!(await probePort())) return;
    await new Promise((done) => setTimeout(done, 250));
  }
  throw new Error('server did not release the port');
}

async function assertServed(expectedSha) {
  const response = await fetch(`${BASE_URL}/static/css/components.css`);
  if (!response.ok) throw new Error(`could not fetch components.css: ${response.status}`);
  const served = sha(Buffer.from(await response.arrayBuffer()));
  if (served !== expectedSha) {
    throw new Error(`server is serving components.css ${served} but the checkout has ${expectedSha}`);
  }
  return served;
}

/** Capture every context for one checkout. Returns { key: {sha, width, height, png} }. */
async function captureRoot(root, label) {
  const onDisk = fileSha(join(root, 'static/css/components.css'));
  const server = await startServer(root);
  const captures = {};
  const presence = {};
  try {
    const served = await assertServed(onDisk);
    const browser = await chromium.launch();
    try {
      for (const route of ROUTES) {
        for (const theme of THEMES) {
          for (const width of WIDTHS) {
            const context = await browser.newContext({
              viewport: { width, height: 900 },
              deviceScaleFactor: 1,
              colorScheme: theme === 'dark' ? 'dark' : 'light',
              reducedMotion: 'reduce',
            });
            const page = await context.newPage();
            await page.goto(`${BASE_URL}${route.url}`, { waitUntil: 'networkidle' });
            await page.evaluate((value) => {
              document.documentElement.setAttribute('data-theme', value);
            }, theme);
            const applied = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
            if (applied !== theme) throw new Error(`data-theme did not land on ${route.key}|${theme}|${width}`);
            // A transitioned property reads back its pre-transition value, so an
            // unsettled shutter photographs the clock rather than the cascade.
            await page.evaluate(() => {
              for (const animation of document.getAnimations({ subtree: true })) {
                if (animation.constructor?.name === 'CSSTransition') { animation.finish(); continue; }
                const iterations = animation.effect?.getComputedTiming?.().iterations ?? 1;
                if (iterations === Infinity) { animation.currentTime = 0; animation.pause(); }
                else { animation.finish(); }
              }
            });
            // Workout Log renders a table of focusable inputs. A focused field
            // paints a focus ring and a blinking caret, and which field holds
            // focus after load is not deterministic — that is a ~379-pixel
            // high-contrast box and a 1x11 caret sliver respectively, both of
            // which appeared in a same-CSS control before this blur existed.
            await page.evaluate(() => {
              document.activeElement instanceof HTMLElement && document.activeElement.blur();
              window.scrollTo(0, 0);
            });
            const count = await page.locator(TARGET).count();
            if (count === 0) throw new Error(`${route.key}|${theme}|${width}: no ${TARGET} rendered`);
            // Weekly and Session Summary each render three `.table-calm` tables
            // side by side, so `.first()` would leave two thirds of the family's
            // surface unrasterised on those routes.
            for (let index = 0; index < count; index += 1) {
              const element = page.locator(TARGET).nth(index);
              const box = await element.boundingBox();
              // A header-only table satisfies a naive presence gate while proving
              // nothing: four of the thirteen family rules are `tbody td`,
              // `tr:nth-child(even) td`, `tr:last-child td` and `tr:hover td`.
              // WP4.4-h lost a round of captures to exactly this — a stale WAL
              // sidecar emptied the tables and every control still passed.
              const rows = await element.locator('tbody tr').count();
              const cells = await element.locator('tbody td').count();
              if (!box || box.width === 0 || box.height === 0) {
                throw new Error(`${route.key}|${theme}|${width}#${index}: ${TARGET} has no box`);
              }
              if (cells === 0 || rows < (MIN_ROWS[route.key] ?? 1)) {
                throw new Error(
                  `${route.key}|${theme}|${width}#${index}: ${rows} body rows / ${cells} body cells — ` +
                  'the row-styling rules would not be rasterised'
                );
              }
              // Require two consecutive identical rasters before accepting one.
              // This settles residual async paint without masking a real change:
              // a cascade difference is stable and still reported.
              // Blur before *every* shot, not once before the loop. Page scripts
              // can focus a field asynchronously after the initial blur; if that
              // happens between two shots and then persists, the next pair
              // matches and the loop accepts a raster containing a focus ring.
              // That is the ~412-pixel high-contrast box this control kept
              // catching on identical CSS.
              const shoot = async () => {
                await page.evaluate(() => {
                  if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
                });
                return element.screenshot({ animations: 'disabled', caret: 'hide' });
              };
              let png = await shoot();
              let attempts = 1;
              for (; attempts < 6; attempts += 1) {
                const again = await shoot();
                if (sha(again) === sha(png)) break;
                png = again;
              }
              if (attempts === 6) throw new Error(`${route.key}|${theme}|${width}#${index}: raster never settled`);
              const key = `${route.key}|${theme}|${width}#${index}`;
              captures[key] = { sha: sha(png), width: Math.round(box.width), height: Math.round(box.height), png };
              presence[key] = { tables: count, rows, cells, attempts };
            }
            await context.close();
          }
        }
      }
    } finally {
      await browser.close();
    }
    console.log(`${label}: captured ${Object.keys(captures).length} contexts from ${root} (components.css ${served})`);
    return { onDisk, served, captures, presence };
  } finally {
    await stopServer(server);
  }
}

/** Count differing pixels between two PNG buffers by decoding both on a canvas. */
async function countDifferingPixels(browser, aPng, bPng) {
  const page = await (await browser.newContext()).newPage();
  try {
    return await page.evaluate(async ([a, b]) => {
      const decode = (base64) => new Promise((done, fail) => {
        const image = new Image();
        image.onload = () => done(image);
        image.onerror = () => fail(new Error('decode failed'));
        image.src = `data:image/png;base64,${base64}`;
      });
      const [imageA, imageB] = await Promise.all([decode(a), decode(b)]);
      if (imageA.width !== imageB.width || imageA.height !== imageB.height) {
        return { differing: -1, note: `size drift ${imageA.width}x${imageA.height} vs ${imageB.width}x${imageB.height}` };
      }
      const draw = (image) => {
        const canvas = document.createElement('canvas');
        canvas.width = image.width; canvas.height = image.height;
        canvas.getContext('2d').drawImage(image, 0, 0);
        return canvas.getContext('2d').getImageData(0, 0, image.width, image.height).data;
      };
      const dataA = draw(imageA), dataB = draw(imageB);
      let differing = 0, maxDelta = 0;
      // Localise the difference. A regression in a table rule paints whole rows
      // or borders; harness noise (a caret, a focus ring, an async glyph) sits in
      // one small box. The bounding box separates the two by inspection.
      let minX = Infinity, minY = Infinity, maxX = -1, maxY = -1;
      for (let i = 0; i < dataA.length; i += 4) {
        let moved = false;
        for (let channel = 0; channel < 4; channel += 1) {
          const delta = Math.abs(dataA[i + channel] - dataB[i + channel]);
          if (delta > 0) { moved = true; if (delta > maxDelta) maxDelta = delta; }
        }
        if (moved) {
          differing += 1;
          const pixel = i / 4;
          const x = pixel % imageA.width, y = Math.floor(pixel / imageA.width);
          if (x < minX) minX = x; if (x > maxX) maxX = x;
          if (y < minY) minY = y; if (y > maxY) maxY = y;
        }
      }
      const box = differing ? { x: minX, y: minY, width: maxX - minX + 1, height: maxY - minY + 1 } : null;
      return { differing, maxDelta, pixels: dataA.length / 4, box, image: { width: imageA.width, height: imageA.height } };
    }, [aPng.toString('base64'), bPng.toString('base64')]);
  } finally {
    await page.context().close();
  }
}

// ---------------------------------------------------------------------------

mkdirSync(outDir, { recursive: true });
if (!existsSync(frozenDb)) throw new Error(`frozen DB not found: ${frozenDb}`);
mkdirSync(dirname(dbPath), { recursive: true });

/**
 * Reset the work database before each half.
 *
 * The sidecars must go first: a stale `-wal` left by the previous server can
 * replay over a freshly copied database and silently revert it. That is not
 * hypothetical — it emptied the tables during WP4.4-h and produced `td = 0`
 * while every control still reported clean. Both halves also have to start from
 * identical bytes, or the comparison measures database drift.
 */
const resetDb = () => {
  for (const sidecar of [`${dbPath}-wal`, `${dbPath}-shm`]) {
    if (existsSync(sidecar)) unlinkSync(sidecar);
  }
  copyFileSync(frozenDb, dbPath);
  return fileSha(dbPath);
};

const beforeDbSha = resetDb();
const before = await captureRoot(beforeRoot, 'before');
const afterDbSha = resetDb();
const after = await captureRoot(afterRoot, 'after');

const fatal = [];
if (expectSameCss) {
  if (before.onDisk !== after.onDisk) {
    fatal.push(`--expect-same-css was given but the halves served ${before.onDisk} vs ${after.onDisk}`);
  }
} else {
  if (before.onDisk === after.onDisk) {
    fatal.push(`both halves served the same components.css ${before.onDisk} — nothing under test changed ` +
      '(pass --expect-same-css if this is the determinism control)');
  }
  if (beforeRoot === afterRoot) fatal.push(`both halves were captured from the same root ${beforeRoot}`);
}

const keys = Object.keys(before.captures);
const missing = keys.filter((key) => !after.captures[key]);
const extra = Object.keys(after.captures).filter((key) => !before.captures[key]);
if (missing.length || extra.length) fatal.push(`context drift: onlyBefore=${missing} onlyAfter=${extra}`);
if (keys.length === 0) fatal.push('zero contexts captured; an empty comparison is not a pass');
if (beforeDbSha !== afterDbSha) fatal.push(`the two halves started from different databases: ${beforeDbSha} vs ${afterDbSha}`);

const mismatches = keys.filter((key) => after.captures[key] && before.captures[key].sha !== after.captures[key].sha);

let quantified = [];
if (mismatches.length) {
  const browser = await chromium.launch();
  try {
    for (const key of mismatches) {
      const result = await countDifferingPixels(browser, before.captures[key].png, after.captures[key].png);
      quantified.push({ context: key, ...result });
    }
  } finally {
    await browser.close();
  }
}

const report = {
  generatedFrom: 'scripts/css_audit/i_element_pixel_diff.mjs',
  target: TARGET,
  before: { root: beforeRoot, components: before.onDisk, served: before.served },
  after: { root: afterRoot, components: after.onDisk, served: after.served },
  db: { before: beforeDbSha, after: afterDbSha },
  contexts: keys.length,
  identicalContexts: keys.length - mismatches.length,
  mismatchedContexts: mismatches.length,
  quantified,
  perContext: Object.fromEntries(keys.map((key) => [key, {
    before: { sha: before.captures[key].sha, ...before.presence[key] },
    after: after.captures[key] ? { sha: after.captures[key].sha, ...after.presence[key] } : null,
  }])),
  fatal,
  passed: fatal.length === 0 && mismatches.length === 0,
};
writeFileSync(join(outDir, 'pixel-diff.json'), `${JSON.stringify(report, null, 2)}\n`);

console.log(`\ntarget: ${TARGET}`);
console.log(`before: ${beforeRoot} components ${before.onDisk}`);
console.log(`after:  ${afterRoot} components ${after.onDisk}`);
console.log(`contexts compared:      ${keys.length}`);
console.log(`byte-identical captures: ${keys.length - mismatches.length}`);
console.log(`mismatched captures:     ${mismatches.length}`);
for (const entry of quantified) console.log(`  ${entry.context}: ${entry.differing} differing pixels${entry.note ? ` (${entry.note})` : ''}`);
for (const message of fatal) console.log(`FATAL: ${message}`);
console.log(report.passed
  ? '\nPASS — every element-scoped capture is byte-identical'
  : '\nFAIL — see pixel-diff.json');

// Every sibling differ sets this. Without it a real regression, or any fatal
// provenance violation, exits 0 and reads as a pass to any caller or CI wrapper.
process.exit(report.passed ? 0 : 1);
