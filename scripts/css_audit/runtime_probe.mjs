/**
 * WP4.4 runtime cascade harness.
 *
 * Produces the evidence every deletion packet needs and the self-checks that
 * make that evidence trustworthy:
 *
 *   rest-state differential   every element's computed paint + motion values,
 *                             captured WITHOUT the visual-helpers determinism
 *                             tag, so the F1/F2 blind spots do not apply
 *   same-CSS control (M5)     the identical capture run twice; any differing
 *                             record invalidates the sweep before a packet
 *                             deletes anything
 *   sentinel-took-effect (M6) a probe that changes nothing proves nothing, so
 *                             each sentinel asserts its own visible effect
 *   motion oracle (F1)        transition and animation longhands at rest under BOTH
 *                             prefers-reduced-motion states — the oracle
 *                             WP4.4-c is gated on, because visual.spec.ts
 *                             zeroes exactly these properties before capture
 *   matched-rule dump (M4)    CDP cascade data, resolved against the Python
 *                             specificity model by resolution_check.py
 *   network state (PR#11)     whether the jsdelivr fallback fired and whether
 *                             Google Fonts resolved, so two differentials taken
 *                             on different network days are comparable
 *
 * Generated output goes to artifacts/wp4_4/ (gitignored); this script is
 * committed so packets b-k can re-run it (A11).
 *
 * usage: node scripts/css_audit/runtime_probe.mjs [--out artifacts/wp4_4/runtime] [--routes a,b]
 */
import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync, rmSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { connect } from 'node:net';

const BASE_URL = 'http://127.0.0.1:5000';

// 11 rendered routes. `/fatigue` is included deliberately: templates/fatigue.html
// links no page bundle at all, so it is painted 100% by the seven shared
// surfaces this arc rewrites — the highest exposure in the app, and until N7 the
// only route with no pixel oracle (F5, PR#2).
const ROUTES = [
  { name: 'welcome', path: '/' },
  { name: 'workout-plan', path: '/workout_plan' },
  { name: 'workout-log', path: '/workout_log' },
  { name: 'weekly-summary', path: '/weekly_summary' },
  { name: 'session-summary', path: '/session_summary' },
  { name: 'progression', path: '/progression' },
  { name: 'body-composition', path: '/body_composition' },
  { name: 'volume-splitter', path: '/volume_splitter' },
  { name: 'user-profile', path: '/user_profile' },
  { name: 'backup', path: '/backup' },
  { name: 'fatigue', path: '/fatigue' },
];

const THEMES = ['light', 'dark'];
const VIEWPORT = { width: 1440, height: 900 };

const PAINT_PROPS = [
  'color',
  'background-color',
  'background-image',
  'border-top-color',
  'border-right-color',
  'border-bottom-color',
  'border-left-color',
  'border-top-width',
  'border-radius',
  'box-shadow',
  'text-shadow',
  'backdrop-filter',
  'opacity',
  'visibility',
  'display',
  'outline-color',
  'font-size',
  'font-weight',
  'padding-top',
  'margin-top',
];

// The properties visual.spec.ts destroys before every screenshot (F1). The
// motion oracle exists because a packet could delete motion.css entirely and
// leave the pixel matrix byte-identical.
const MOTION_PROPS = [
  'transition-property',
  'transition-duration',
  'transition-delay',
  'transition-timing-function',
  'animation-name',
  'animation-duration',
  'animation-delay',
  'animation-iteration-count',
  'animation-timing-function',
];

const args = process.argv.slice(2);
const getArg = (flag, fallback) => {
  const index = args.indexOf(flag);
  return index === -1 ? fallback : args[index + 1];
};
const outDir = resolve(getArg('--out', 'artifacts/wp4_4/runtime'));
const routeFilter = getArg('--routes', null);
const routes = routeFilter
  ? ROUTES.filter((route) => routeFilter.split(',').includes(route.name))
  : ROUTES;

const sha = (value) => createHash('sha256').update(value).digest('hex');

/**
 * A stable identity for an element across two runs of the same page.
 * Uses structural position, never a class name: class names are exactly what
 * these packets change.
 */
const DOM_PATH_FN = `
  (el) => {
    const parts = [];
    let node = el;
    while (node && node.nodeType === 1 && node !== document.documentElement) {
      const parent = node.parentElement;
      if (!parent) break;
      const index = Array.prototype.indexOf.call(parent.children, node);
      parts.unshift(node.tagName.toLowerCase() + '[' + index + ']');
      node = parent;
    }
    return 'html/' + parts.join('/');
  }
`;

async function capture(page, props) {
  return page.evaluate(
    ({ propList, domPathSource }) => {
      const domPath = eval(domPathSource);
      const records = [];
      const elements = document.querySelectorAll('*');
      for (const element of elements) {
        const tag = element.tagName.toLowerCase();
        if (tag === 'script' || tag === 'style' || tag === 'link' || tag === 'meta') {
          continue;
        }
        const computed = getComputedStyle(element);
        const values = {};
        for (const prop of propList) {
          values[prop] = computed.getPropertyValue(prop);
        }
        records.push({ path: domPath(element), tag, values });
      }
      return records;
    },
    { propList: props, domPathSource: DOM_PATH_FN },
  );
}

/**
 * CDP matched-rule dump for a sample of elements, restricted to the seven
 * shared surfaces. resolution_check.py replays the cascade over this with the
 * Python specificity model and asserts it picks the same winner the browser
 * did (M4).
 */
async function matchedRules(page, client, limit = 120) {
  const { root } = await client.send('DOM.getDocument', { depth: -1, pierce: false });
  const { nodeIds } = await client.send('DOM.querySelectorAll', {
    nodeId: root.nodeId,
    selector: 'body *',
  });

  const step = Math.max(1, Math.floor(nodeIds.length / limit));
  const sampled = nodeIds.filter((_, index) => index % step === 0).slice(0, limit);
  const out = [];

  for (const nodeId of sampled) {
    let matched;
    try {
      matched = await client.send('CSS.getMatchedStylesForNode', { nodeId });
    } catch {
      continue;
    }
    const rules = (matched.matchedCSSRules ?? [])
      .filter((entry) => {
        const url = entry.rule?.styleSheetId ? entry.rule.origin : null;
        return entry.rule?.origin === 'regular' && url !== null;
      })
      .map((entry) => ({
        selector: entry.rule.selectorList?.text ?? '',
        // Which branches of the selector list actually matched. This is the
        // whole `:is()` question: a rule can match through its class branch
        // while exporting the ID weight of a branch that did not.
        matchingSelectors: entry.matchingSelectors ?? [],
        selectors: (entry.rule.selectorList?.selectors ?? []).map((s) => s.text),
        media: (entry.rule.media ?? []).map((m) => m.text),
        // Layer membership decides precedence before specificity is consulted,
        // and inverts for `!important` (N2 freezes this for the whole arc).
        layers: (entry.rule.layers ?? []).map((layer) => layer.text),
        declarations: (entry.rule.style?.cssProperties ?? [])
          .filter((property) => !property.disabled && property.name)
          .map((property) => ({
            name: property.name,
            value: property.value,
            important: Boolean(property.important),
          })),
      }));

    const { object } = await client.send('DOM.resolveNode', { nodeId });
    let path = null;
    try {
      const result = await client.send('Runtime.callFunctionOn', {
        objectId: object.objectId,
        functionDeclaration: `function() { return (${DOM_PATH_FN})(this); }`,
        returnByValue: true,
      });
      path = result.result.value;
    } catch {
      /* node detached between calls; drop the sample rather than guess */
    }
    await client.send('Runtime.releaseObject', { objectId: object.objectId }).catch(() => {});

    if (path) {
      out.push({ path, rules });
    }
  }

  return out;
}

/**
 * M6 — sentinel-took-effect. Injects a sentinel at a specificity nothing in the
 * app can beat and asserts the computed value actually moved. `var()`-bearing
 * shorthands are invisible to longhand CSSOM queries, which is how four earlier
 * oracle defects each produced a confident false deadness verdict.
 */
async function sentinelSelfCheck(page) {
  const SENTINEL = 'rgb(255, 0, 255)';

  // The sentinel is applied INLINE with `!important`, not through an injected
  // stylesheet. An injected `body * { … !important }` rule has specificity
  // (0,0,1), and among `!important` declarations the more specific one wins —
  // so app rules like the /fatigue header and select outline-colors silently
  // beat it, and the sweep would then report "no effect" on exactly the
  // elements whose declarations it was meant to certify. Inline `!important`
  // is the strongest author-origin position, so a non-taker is a real finding.
  const result = await page.evaluate((sentinel) => {
    const elements = Array.from(document.querySelectorAll('body *')).slice(0, 200);
    const before = elements.map((element) => getComputedStyle(element).outlineColor);

    for (const element of elements) {
      // Transitions must be suppressed BEFORE the sentinel is written. A
      // transitioned property reads back its pre-sentinel value for the whole
      // transition duration, so `getComputedStyle` reports "no effect" on an
      // element the sentinel reached perfectly well — a false deadness verdict
      // on every element carrying `transition: all` (the app sets that on
      // `header` and `select`, among others). This is the same family of oracle
      // defect as M6's four, and it survives inline `!important`.
      element.style.setProperty('transition-property', 'none', 'important');
      element.style.setProperty('outline-color', sentinel, 'important');
    }
    const after = elements.map((element) => getComputedStyle(element).outlineColor);

    // Drop the sentinel while transitions are still suppressed, for the same
    // reason: released first, the value transitions BACK over 0.3s and the
    // revert check reads it mid-flight.
    for (const element of elements) {
      element.style.removeProperty('outline-color');
    }
    const restored = elements.map((element) => getComputedStyle(element).outlineColor);
    for (const element of elements) {
      element.style.removeProperty('transition-property');
    }

    return { before, after, restored };
  }, SENTINEL);

  const probed = result.after.length;
  const tookEffect = result.after.filter((value) => value === SENTINEL).length;
  const changed = result.after.filter(
    (value, index) => value !== result.before[index],
  ).length;
  // Removing the sentinel must put every element back, or the probe has
  // permanently altered the page it was measuring.
  const reverted = result.restored.filter(
    (value, index) => value === result.before[index],
  ).length;

  return {
    probed,
    tookEffect,
    changed,
    reverted,
    pass: probed > 0 && tookEffect === probed && reverted === probed,
  };
}

/**
 * Elements running an animation that never ends. A rest-state differential
 * cannot certify these: two captures a frame apart legitimately disagree, which
 * is how WP4.3i-dead's same-CSS control produced 52 differing records and cost
 * that packet ten declarations. They are excluded from the control's pass/fail
 * and registered explicitly, so no packet can claim a declaration on them is
 * dead on this harness's authority.
 */
async function animatingElements(page) {
  return page.evaluate(
    ({ domPathSource }) => {
      const domPath = eval(domPathSource);
      return Array.from(document.querySelectorAll('*'))
        .map((element) => {
          const computed = getComputedStyle(element);
          return {
            path: domPath(element),
            tag: element.tagName.toLowerCase(),
            animationName: computed.animationName,
            iterationCount: computed.animationIterationCount,
          };
        })
        .filter(
          (record) =>
            record.animationName !== 'none' &&
            record.iterationCount === 'infinite',
        );
    },
    { domPathSource: DOM_PATH_FN },
  );
}

/**
 * Pin every animation to its first frame for the pixel control.
 *
 * Deliberately NOT what `visual-helpers.ts` does. Setting
 * `animation-duration: 0s` jumps each animation to its *end* state and zeroes
 * `transition-duration`, which is the F1 blindness this harness exists to avoid.
 * Pausing at delay 0 keeps every declaration in force and merely stops the
 * clock, so the capture is deterministic without deleting the surface under test.
 */
async function stillAnimations(page) {
  await page.evaluate(() => {
    // `animation-play-state: paused` alone is not deterministic: it freezes an
    // already-running animation at whatever frame it happens to be on, so two
    // captures of an infinite animation still disagree.
    //
    // The two kinds need opposite treatment. A finite entry animation
    // (`page-enter`, `fadeIn`, `slideInRight`) must be FINISHED — its fill
    // state IS the page's rest state, and rewinding it to frame 0 puts the
    // page back into its pre-entry appearance, which is not what any packet
    // ships. An infinite animation has no rest state at all, so it is pinned
    // to frame 0. Either way every declaration stays in force; only the clock
    // is controlled.
    for (const animation of document.getAnimations()) {
      const iterations = animation.effect?.getTiming?.().iterations;
      if (iterations === Infinity) {
        animation.pause();
        animation.currentTime = 0;
      } else {
        try {
          animation.finish();
        } catch {
          animation.pause();
        }
      }
    }
  });
  // One frame for the seek to be painted.
  await page.evaluate(
    () => new Promise((done) => requestAnimationFrame(() => done(null))),
  );
}

/**
 * Pixel diff between two PNG buffers, done in Chromium via canvas.
 *
 * A sha256 comparison answers "identical?" but not "how far off?", and the
 * difference between a two-pixel antialiasing drift and a structural change is
 * the difference between a usable oracle and an unusable one. Returns the
 * differing-pixel count and the bounding box, so a control failure can be read
 * rather than guessed at.
 */
async function diffPng(browser, first, second) {
  const context = await browser.newContext();
  const page = await context.newPage();
  const result = await page.evaluate(
    async ({ a, b }) => {
      const load = (dataUrl) =>
        new Promise((resolve, reject) => {
          const image = new Image();
          image.onload = () => resolve(image);
          image.onerror = reject;
          image.src = dataUrl;
        });

      const [imageA, imageB] = await Promise.all([load(a), load(b)]);
      if (imageA.width !== imageB.width || imageA.height !== imageB.height) {
        return {
          differingPixels: -1,
          note: `size mismatch ${imageA.width}x${imageA.height} vs ${imageB.width}x${imageB.height}`,
        };
      }

      const draw = (image) => {
        const canvas = document.createElement('canvas');
        canvas.width = image.width;
        canvas.height = image.height;
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        ctx.drawImage(image, 0, 0);
        return ctx.getImageData(0, 0, image.width, image.height).data;
      };

      const dataA = draw(imageA);
      const dataB = draw(imageB);
      let differing = 0;
      let maxChannelDelta = 0;
      let minX = Infinity;
      let minY = Infinity;
      let maxX = -1;
      let maxY = -1;

      for (let index = 0; index < dataA.length; index += 4) {
        let delta = 0;
        for (let channel = 0; channel < 4; channel += 1) {
          delta = Math.max(delta, Math.abs(dataA[index + channel] - dataB[index + channel]));
        }
        if (delta > 0) {
          differing += 1;
          maxChannelDelta = Math.max(maxChannelDelta, delta);
          const pixel = index / 4;
          const x = pixel % imageA.width;
          const y = Math.floor(pixel / imageA.width);
          minX = Math.min(minX, x);
          maxX = Math.max(maxX, x);
          minY = Math.min(minY, y);
          maxY = Math.max(maxY, y);
        }
      }

      return {
        width: imageA.width,
        height: imageA.height,
        differingPixels: differing,
        maxChannelDelta,
        boundingBox:
          maxX === -1 ? null : { minX, minY, maxX, maxY, height: maxY - minY + 1 },
      };
    },
    {
      a: `data:image/png;base64,${first.toString('base64')}`,
      b: `data:image/png;base64,${second.toString('base64')}`,
    },
  );
  await context.close();
  return result;
}

/**
 * PR#11 — pin the network, then record the pin.
 *
 * `templates/base.html` pulls Google Fonts (:11-13), FontAwesome CSS (:16, no
 * fallback of any kind) and, if the local Bootstrap fails, jsdelivr (:15). Left
 * live, those five requests resolve at different moments on every run, and the
 * icon glyphs land in the navbar band — which is why two captures of byte-
 * identical CSS disagreed by 33 to 474 pixels, run to run, with the diff moving
 * around the page.
 *
 * Blocking external hosts outright would be deterministic but would drop Inter
 * and every icon, changing text metrics on all eleven routes. Caching the
 * responses to disk on first use and replaying them thereafter keeps the page
 * exactly as a user sees it AND makes every subsequent run — including a run in
 * CI with no network — byte-reproducible. The manifest is recorded so a
 * differential taken by packet b is comparable with one taken by packet j.
 */
const netCacheDir = resolve('artifacts/wp4_4/net-cache');
const netCacheManifest = new Map();

function cachePathFor(url) {
  return join(netCacheDir, `${sha(url).slice(0, 32)}.bin`);
}

async function installNetworkPin(context, network) {
  mkdirSync(netCacheDir, { recursive: true });

  await context.route(
    (url) => !url.hostname.startsWith('127.0.0.1'),
    async (route, request) => {
      const url = request.url();
      const file = cachePathFor(url);
      const metaFile = `${file}.json`;

      if (existsSync(file) && existsSync(metaFile)) {
        const meta = JSON.parse(readFileSync(metaFile, 'utf8'));
        const body = readFileSync(file);
        netCacheManifest.set(url, { ...meta, sha256: sha(body), source: 'cache' });
        network.push({ url, status: meta.status, pinned: 'cache' });
        await route.fulfill({ status: meta.status, headers: meta.headers, body });
        return;
      }

      try {
        const response = await route.fetch();
        const body = await response.body();
        const meta = { status: response.status(), headers: response.headers() };
        writeFileSync(file, body);
        writeFileSync(metaFile, JSON.stringify(meta), 'utf8');
        netCacheManifest.set(url, { ...meta, sha256: sha(body), source: 'network' });
        network.push({ url, status: meta.status, pinned: 'fetched' });
        await route.fulfill({ status: meta.status, headers: meta.headers, body });
      } catch (error) {
        // Offline and not yet cached: record the miss rather than hiding it,
        // because a differential taken with a missing asset is not comparable
        // with one taken with it present.
        netCacheManifest.set(url, { status: 0, source: 'unavailable' });
        network.push({ url, status: 0, pinned: 'unavailable' });
        await route.abort();
      }
    },
  );
}

async function probeContext(browser, route, theme, reducedMotion) {
  const context = await browser.newContext({
    viewport: VIEWPORT,
    colorScheme: theme,
    locale: 'en-US',
    timezoneId: 'UTC',
    deviceScaleFactor: 1,
    reducedMotion,
  });

  const network = [];
  await installNetworkPin(context, network);
  context.on('response', (response) => {
    if (response.url().includes('127.0.0.1')) {
      network.push({ url: response.url(), status: response.status(), pinned: 'local' });
    }
  });

  const page = await context.newPage();
  await page.addInitScript((value) => {
    localStorage.clear();
    localStorage.setItem('darkMode', value === 'dark' ? 'true' : 'false');
    document.documentElement?.setAttribute('data-theme', value);
  }, theme);

  await page.goto(`${BASE_URL}${route.path}`, { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle').catch(() => {});

  // Webfonts must be resolved before anything is measured. The icon glyphs are
  // FontAwesome, and a capture taken while the font is still in flight renders
  // them in the fallback face — which drifts between two runs of identical CSS
  // and lands squarely in the navbar band, producing exactly the "unstable
  // page" verdict that would have cost this arc its pixel oracle. This is
  // PR#11's network-state hazard in concrete form.
  const fontsReady = await page
    .evaluate(() => document.fonts.ready.then(() => document.fonts.status))
    .catch(() => 'unavailable');

  // Let one-shot entry animations finish, then measure at rest. M3: the rest
  // state is the only state a differential can compare; animating elements
  // drift between runs for reasons unrelated to CSS.
  await page.waitForTimeout(1200);

  return { context, page, network, fontsReady };
}

async function main() {
  rmSync(outDir, { recursive: true, force: true });
  mkdirSync(outDir, { recursive: true });

  const dbPath = resolve('artifacts/wp4_4/probe.db');
  mkdirSync(resolve('artifacts/wp4_4'), { recursive: true });
  rmSync(dbPath, { force: true });
  for (const suffix of ['-wal', '-shm']) {
    rmSync(`${dbPath}${suffix}`, { force: true });
  }

  const python = process.platform === 'win32' ? '.venv/Scripts/python.exe' : '.venv/bin/python';
  const server = spawn(python, ['app.py'], {
    env: { ...process.env, DB_FILE: dbPath, FLASK_DEBUG: '0', FLASK_USE_RELOADER: '0' },
    stdio: 'ignore',
  });

  // A raw TCP probe, not fetch(): undici asserts internally when it meets the
  // half-open socket Flask leaves behind while it is still binding.
  const portOpen = () =>
    new Promise((done) => {
      const socket = connect({ host: '127.0.0.1', port: 5000 });
      const settle = (value) => {
        socket.destroy();
        done(value);
      };
      socket.once('connect', () => settle(true));
      socket.once('error', () => settle(false));
      socket.setTimeout(1000, () => settle(false));
    });

  const waitForServer = async () => {
    for (let attempt = 0; attempt < 120; attempt += 1) {
      if (await portOpen()) return true;
      await new Promise((done) => setTimeout(done, 500));
    }
    return false;
  };

  if (!(await waitForServer())) {
    server.kill();
    throw new Error(`server did not come up at ${BASE_URL}`);
  }

  // The same launch flags `playwright.config.ts:36-40` uses for the visual
  // suite. Without them the Welcome page's dark gradient dithers differently
  // between two runs of identical CSS — 36,925 pixels differing at a channel
  // delta of 2, invisible to a human and fatal to a 0-tolerance control. This
  // harness must be at least as deterministic as the oracle it supplements.
  const browser = await chromium.launch({
    args: [
      '--disable-font-subpixel-positioning',
      '--disable-gpu',
      '--force-color-profile=srgb',
    ],
  });
  // Warm-up load, discarded. The FIRST page render in a fresh browser process
  // differs from every later one — font rasterization and raster caches are
  // still cold — so whichever context happens to go first carries a systematic
  // difference against its own control. Measured directly: capture 1 differed
  // from capture 2, and captures 2..6 were byte-identical to each other.
  {
    const warmup = await probeContext(browser, routes[0], 'light', 'no-preference');
    await stillAnimations(warmup.page);
    await warmup.page.screenshot();
    await warmup.context.close();
  }

  const summary = {
    schemaVersion: 1,
    baseUrl: BASE_URL,
    viewport: VIEWPORT,
    routes: routes.map((route) => route.name),
    themes: THEMES,
    capturedAt: new Date().toISOString(),
    selfChecks: { sameCssControl: [], sentinel: [], screenshotControl: [] },
    network: {},
    motionOracle: {},
  };

  for (const route of routes) {
    for (const theme of THEMES) {
      const label = `${route.name}--${theme}`;

      // ---- pass 1 -------------------------------------------------------
      // Order matters: every measurement that must be free of probe artefacts
      // is taken BEFORE the sentinel, which mutates inline styles.
      // M3, made concrete for this app. `header.navbar` is `position: fixed`
      // with `z-index: 1000` and occupies page y 0-64, while `main` starts at
      // y 8 — so the navbar paints OVER main's top 56px and a locator
      // screenshot of `main` still contains the animated band. Every same-CSS
      // control failure measured here (33-515 px, delta up to 237) fell inside
      // that overlay. The capture is therefore clipped to start below every
      // fixed top-anchored element, and capped to one viewport height so a
      // 4,000px page cannot make the control hostage to lazily-rendered
      // content far below the fold.
      const scopedClip = async (page) => {
        const box = await page.evaluate(() => {
          const main = document.querySelector('main') ?? document.body;
          const rect = main.getBoundingClientRect();

          // Only a top BAR counts as an overlay to clip past. Three conditions,
          // each earned: it must be anchored at or above main's top edge, it
          // must actually overlap main horizontally (Workout Plan carries a
          // fixed `aside.vp-drawer` parked off-screen at full viewport height —
          // counting it pushed the clip origin to y=900 and produced an empty
          // capture), and it must occupy no more than the top third of the
          // viewport, so a full-height panel can never swallow the whole page.
          let overlayBottom = 0;
          const overlays = [];
          for (const element of document.querySelectorAll('body *')) {
            const style = getComputedStyle(element);
            if (style.position !== 'fixed' && style.position !== 'sticky') continue;
            const elementRect = element.getBoundingClientRect();
            const overlapsHorizontally =
              elementRect.right > rect.left &&
              elementRect.left < rect.right &&
              elementRect.width > 0;
            const isTopBar =
              elementRect.top <= rect.top &&
              elementRect.height > 0 &&
              elementRect.bottom <= window.innerHeight / 3;
            if (overlapsHorizontally && isTopBar) {
              overlayBottom = Math.max(overlayBottom, elementRect.bottom);
              overlays.push({
                tag: element.tagName.toLowerCase(),
                bottom: Math.round(elementRect.bottom),
              });
            }
          }

          const pageWidth = Math.max(
            document.documentElement.scrollWidth,
            window.innerWidth,
          );
          const pageHeight = Math.max(
            document.documentElement.scrollHeight,
            window.innerHeight,
          );

          const top = Math.max(rect.top + window.scrollY, overlayBottom, 0);
          let bottom = Math.min(
            rect.bottom + window.scrollY,
            top + window.innerHeight,
            pageHeight,
          );
          // A `main` shorter than the fixed overlay (some routes render an
          // almost-empty main and let page content sit elsewhere) would produce
          // a zero or negative clip, which Playwright rejects outright. Fall
          // back to one viewport below the overlay.
          if (bottom - top < 50) {
            bottom = Math.min(top + window.innerHeight, pageHeight);
          }

          const left = Math.max(0, Math.round(rect.left));
          return {
            x: left,
            y: Math.round(top),
            width: Math.max(1, Math.min(Math.round(rect.width), pageWidth - left)),
            height: Math.max(1, Math.round(bottom - top)),
            overlayBottom: Math.round(overlayBottom),
            overlays,
            mainHeight: Math.round(rect.height),
          };
        });
        return box;
      };

      // Both passes must perform the SAME work in the SAME order up to the
      // screenshot. When pass 1 did its extra reads first, the two captures
      // disagreed on every route — a control failure manufactured entirely by
      // the harness, which would have been read as page instability and cost
      // the arc its pixel oracle.
      // Element-scoped, not full-page: M3 — the full-page oracle drifts at
      // 10 of 14 widths inside the animated navbar band.
      const upToScreenshot = async (page) => {
        const paint = await capture(page, PAINT_PROPS);
        await stillAnimations(page);
        const clip = await scopedClip(page);
        // `fullPage` is required: the clip is expressed in DOCUMENT
        // coordinates, and a viewport-relative clip is rejected outright once
        // the region starts below the fold.
        const shotArgs = {
          fullPage: true,
          clip: { x: clip.x, y: clip.y, width: clip.width, height: clip.height },
        };
        // The first raster of a page is not the same as its second. The Welcome
        // hero carries a 57px-blur glow under an infinite animation, and its
        // first rasterization differs from every later one by up to 16,783
        // pixels — enough to fail a 0-tolerance control on whichever context
        // happens to be measured first. Discarding one raster per page makes
        // the measured capture reproducible; doing it in BOTH passes keeps them
        // symmetric.
        await page.screenshot(shotArgs);
        const shot = await page.screenshot(shotArgs);
        return { paint, shot, clip };
      };

      const first = await probeContext(browser, route, theme, 'no-preference');
      const { paint: paintA, shot: shotA, clip: clipA } = await upToScreenshot(first.page);

      const motionA = await capture(first.page, MOTION_PROPS);
      const animating = await animatingElements(first.page);

      const client = await first.context.newCDPSession(first.page);
      await client.send('DOM.enable');
      await client.send('CSS.enable');
      const rules = await matchedRules(first.page, client);

      // Last, because it writes inline styles onto the sampled elements.
      const sentinel = await sentinelSelfCheck(first.page);
      await first.context.close();

      // ---- pass 2: identical CSS, fresh context (M5 control) ------------
      const second = await probeContext(browser, route, theme, 'no-preference');
      const { paint: paintB, shot: shotB } = await upToScreenshot(second.page);
      await second.context.close();

      // ---- motion oracle: reduced-motion half (F1) ----------------------
      const reduced = await probeContext(browser, route, theme, 'reduce');
      const motionReduced = await capture(reduced.page, MOTION_PROPS);
      await reduced.context.close();

      // ---- diffs --------------------------------------------------------
      const uncertifiable = new Set(animating.map((record) => record.path));
      const indexB = new Map(paintB.map((record) => [record.path, record]));
      const differing = [];
      const differingUncertifiable = [];

      for (const record of paintA) {
        const other = indexB.get(record.path);
        const bucket = uncertifiable.has(record.path)
          ? differingUncertifiable
          : differing;
        if (!other) {
          bucket.push({ path: record.path, reason: 'absent in control run' });
          continue;
        }
        for (const prop of PAINT_PROPS) {
          if (record.values[prop] !== other.values[prop]) {
            bucket.push({
              path: record.path,
              property: prop,
              first: record.values[prop],
              second: other.values[prop],
            });
          }
        }
      }

      summary.selfChecks.sameCssControl.push({
        context: label,
        elementsFirst: paintA.length,
        elementsSecond: paintB.length,
        differingRecords: differing.length,
        // Registered, not silently dropped: these elements are outside what any
        // rest-state differential in this arc can certify.
        uncertifiableElements: animating.length,
        uncertifiableDifferingRecords: differingUncertifiable.length,
        uncertifiablePaths: animating.map((record) => record.path),
        pass: differing.length === 0 && paintA.length === paintB.length,
      });
      summary.selfChecks.sentinel.push({ context: label, ...sentinel });
      const pixelDiff =
        sha(shotA) === sha(shotB)
          ? { differingPixels: 0, maxChannelDelta: 0, boundingBox: null }
          : await diffPng(browser, shotA, shotB);

      summary.selfChecks.screenshotControl.push({
        context: label,
        bytesFirst: shotA.length,
        bytesSecond: shotB.length,
        sha256First: sha(shotA),
        sha256Second: sha(shotB),
        clip: clipA,
        ...pixelDiff,
        pass: pixelDiff.differingPixels === 0,
      });

      // Which elements actually carry motion, and how reduced-motion changes
      // that. This is the c-packet oracle: a deletion that changes any of
      // these records is a behaviour change, invisible to the pixel matrix.
      const motionActive = motionA.filter(
        (record) =>
          record.values['transition-duration'] !== '0s' ||
          record.values['animation-name'] !== 'none',
      );
      const reducedIndex = new Map(motionReduced.map((r) => [r.path, r]));
      const suppressedByReducedMotion = motionActive.filter((record) => {
        const other = reducedIndex.get(record.path);
        if (!other) return false;
        return MOTION_PROPS.some(
          (prop) => record.values[prop] !== other.values[prop],
        );
      });

      summary.motionOracle[label] = {
        elements: motionA.length,
        withMotion: motionActive.length,
        changedUnderReducedMotion: suppressedByReducedMotion.length,
      };

      summary.network[label] = {
        requests: first.network.length,
        jsdelivrRequested: first.network.some((entry) => entry.url.includes('jsdelivr')),
        jsdelivrFallbackFired: first.network.some(
          (entry) => entry.url.includes('jsdelivr') && entry.status < 400,
        ),
        googleFontsOk: first.network.some(
          (entry) => entry.url.includes('fonts.g') && entry.status < 400,
        ),
        failedRequests: first.network.filter((entry) => entry.status >= 400).length,
        fontsStatus: first.fontsReady,
      };

      writeFileSync(
        join(outDir, `${label}.json`),
        `${JSON.stringify(
          {
            route: route.name,
            theme,
            paint: paintA,
            motion: motionA,
            motionReduced,
            matchedRules: rules,
            network: first.network,
          },
          null,
          1,
        )}\n`,
        'utf8',
      );
      writeFileSync(join(outDir, `${label}.png`), shotA);

      const control = summary.selfChecks.sameCssControl.at(-1);
      console.log(
        `${label.padEnd(28)} elements=${String(paintA.length).padStart(4)} ` +
          `control=${control.pass ? 'PASS' : `FAIL(${differing.length})`} ` +
          `uncert=${String(animating.length).padStart(2)} ` +
          `sentinel=${sentinel.pass ? 'PASS' : `FAIL(${sentinel.tookEffect}/${sentinel.probed})`} ` +
          `shot=${pixelDiff.differingPixels === 0 ? 'PASS' : `FAIL(${pixelDiff.differingPixels}px d=${pixelDiff.maxChannelDelta} y=${pixelDiff.boundingBox ? pixelDiff.boundingBox.minY + '-' + pixelDiff.boundingBox.maxY : '?'})`}`,
      );
      if (differing.length) {
        writeFileSync(
          join(outDir, `${label}.control-failures.json`),
          `${JSON.stringify(differing.slice(0, 500), null, 1)}\n`,
        );
      }
    }
  }

  await browser.close();
  server.kill();

  const failed = [
    ...summary.selfChecks.sameCssControl.filter((entry) => !entry.pass),
    ...summary.selfChecks.sentinel.filter((entry) => !entry.pass),
    ...summary.selfChecks.screenshotControl.filter((entry) => !entry.pass),
  ];
  summary.allSelfChecksPass = failed.length === 0;

  summary.networkPin = {
    cacheDir: 'artifacts/wp4_4/net-cache',
    externalAssets: Object.fromEntries(
      [...netCacheManifest.entries()].map(([url, meta]) => [
        url,
        { status: meta.status, sha256: meta.sha256 ?? null, source: meta.source },
      ]),
    ),
    unavailable: [...netCacheManifest.entries()]
      .filter(([, meta]) => meta.source === 'unavailable')
      .map(([url]) => url),
  };

  writeFileSync(
    join(outDir, 'summary.json'),
    `${JSON.stringify(summary, null, 2)}\n`,
    'utf8',
  );

  console.log(`\nself-checks ${summary.allSelfChecksPass ? 'PASS' : `FAIL (${failed.length})`}`);
  console.log(`wrote ${outDir}`);
  if (!summary.allSelfChecksPass) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
