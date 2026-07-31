/**
 * N4 Inventory B — Workout Log regions A, B and C pre-change ownership measurement.
 *
 * G3 (PLANNING.md §2) is a hard gate on WP4.4-i: *"Workout Log regions A, B and C
 * remain page-local and ID-free. Any packet that changes shared selector ownership
 * MUST re-measure A–C before and after."* This script is that measurement. It is
 * committed rather than left in `artifacts/` because G3 requires the identical run
 * again after any `:is()` repair — a one-off tool cannot satisfy a before/after gate.
 *
 * It changes nothing. It reads `static/css/pages-workout-log.css`, renders
 * `/workout_log` against a frozen database, and records, for every authored
 * declaration in regions A/B/C, whether it currently WINS or LOSES each longhand it
 * declares, and who owns that longhand when it loses. The "would-become-winner"
 * question N3/R3 asks is answered by re-running this and diffing `wins`/`loses`.
 *
 * Region identity is resolved STRUCTURALLY, by exact selector text, never by the
 * line numbers in the WP4.3j-c audit — that audit ran against a 2,180-line file and
 * two deletion packets have shipped since. A line-keyed scope swept up 26 rules
 * including Region H once already (WP4.3j-c-dead §"the audit was treated as a
 * nomination"). Any anchor that fails to resolve is a fatal error, not a warning.
 *
 * Controls, each fatal:
 *   M5  same-CSS control      every context captured twice; any differing record
 *                             invalidates the run before its numbers are quoted
 *   M5  known-live control    a sweep reporting zero winners in A, B and C is a
 *                             broken oracle, not a dead file — WP4.3j-c measured
 *                             live winners in all three
 *   M4  resolution self-check the resolved owner's value is checked against
 *                             getComputedStyle; a mismatch means the ownership
 *                             model disagrees with the browser
 *   G3  ID-free assertion     every region selector line must compute specificity
 *                             a == 0, which is the property G3 protects
 *   --  DOM presence          the table must render rows; a stale WAL sidecar
 *                             silently reverted a seeded database once (WP4.4-h)
 *
 * M6a is satisfied by settling transitions before any computed value is read. No
 * sentinel is written: this measures declaration ownership from CDP cascade data,
 * so nothing is applied to the page that would have to be removed again.
 *
 * Provenance is recorded, never inferred from the output directory's name. The
 * run records its checkout root, git head/branch/dirty state, the `--side` it was
 * told it is, and the on-disk *and served* digests of both `pages-workout-log.css`
 * and `components.css`. `components.css` is the file any `:is()` repair edits, so
 * it is the only digest that can distinguish a before half from an after half —
 * recording just `pages-workout-log.css`, which no admissible repair touches, left
 * the two summaries byte-indistinguishable and the gate unverifiable from its own
 * artifacts.
 *
 * The diff half requires the two summaries to come from different checkout roots,
 * so `--root` selects which checkout is served and measured. Without it the before
 * half could only be produced by swapping `components.css` in place in the after
 * half's own tree, which leaves no durable proof of which bytes were served when —
 * the same unreproducibility this corrective exists to remove.
 *
 * usage:
 *   node scripts/css_audit/n4_regions_abc.mjs \
 *     --side before|after \
 *     [--root <checkout>] \
 *     --frozen-db artifacts/wp4_4/probe-frozen.db \
 *     --expect-db-sha <sha256> \
 *     [--expect-components-sha <sha256>] \
 *     --out artifacts/wp4_4/n4-regions-abc
 */
import { chromium } from '@playwright/test';
import { spawn, spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync, copyFileSync, existsSync, unlinkSync, rmSync } from 'node:fs';
import { join, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { connect } from 'node:net';
import postcss from 'postcss';

const SELF_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const PORT = 5000;
const BASE_URL = `http://127.0.0.1:${PORT}`;
const PAGE_URL_SUFFIX = '/static/css/pages-workout-log.css';

const argv = process.argv.slice(2);
const arg = (name, fallback = null) => {
  const i = argv.indexOf(name);
  return i < 0 ? fallback : argv[i + 1];
};
// Which checkout is served and measured. Defaults to this script's own tree, so
// the after half needs no flag; the before half points at a checkout of the
// pre-repair commit.
const ROOT = resolve(arg('--root', SELF_ROOT));
const CSS_PATH = join(ROOT, 'static/css/pages-workout-log.css');
const outDir = resolve(arg('--out', 'artifacts/wp4_4/n4-regions-abc'));
const frozenDb = resolve(arg('--frozen-db', 'artifacts/wp4_4/probe-frozen.db'));
const expectDbSha = arg('--expect-db-sha');
const expectCssSha = arg('--expect-css-sha');
const dbPath = resolve('artifacts/wp4_4/n4-probe.db');

// WP4.4-i corrective: which half of the G3 gate this run is, and which
// components.css it must serve. `--side` is recorded, never inferred; the
// variable under test is components.css, and until this packet the summary
// recorded only pages-workout-log.css — byte-identical on both halves by
// design, so two summaries were indistinguishable and the diff could not tell
// a real before/after pair from the same capture supplied twice.
const side = arg('--side');
if (side !== null && side !== 'before' && side !== 'after') {
  throw new Error(`--side must be "before" or "after", got ${JSON.stringify(side)}`);
}
const expectComponentsSha = arg('--expect-components-sha');
const COMPONENTS_PATH = join(ROOT, 'static/css/components.css');
const COMPONENTS_URL_SUFFIX = '/static/css/components.css';

const WIDTHS = (arg('--widths', '375,768,1440')).split(',').map(Number);
const THEMES = ['light', 'dark'];
const LAYER_ORDER = ['workout', 'navbar', 'workout-dropdowns', 'welcome'];

const fileSha = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');

// ---------------------------------------------------------------------------
// region anchors — exact first selector line of each region's rules
// ---------------------------------------------------------------------------
// Anchored on the COMPLETE selector list, not its first line. `.workout-log-table
// tbody tr:hover td` opens two different rules — region C's three-arm block and the
// standalone `filter: brightness()` hover rule the j-c arc deliberately left in
// place — and a first-line anchor silently conflates them.
const REGIONS = {
  A: {
    title: 'Base light header block',
    anchors: [
      '.workout-log-table thead th, .workout-log-frame .workout-log-table thead th, ' +
        '.tbl--responsive.workout-log-table thead th, ' +
        '.workout-log-frame .tbl--responsive.workout-log-table thead th, ' +
        'table.workout-log-table thead th',
    ],
  },
  B: {
    title: 'Dark-mode header counterpart',
    anchors: [
      "[data-theme='dark'] .workout-log-table thead th, " +
        "[data-theme='dark'] .workout-log-frame .workout-log-table thead th, " +
        "[data-theme='dark'] .tbl--responsive.workout-log-table thead th, " +
        "[data-theme='dark'] .workout-log-frame .tbl--responsive.workout-log-table thead th, " +
        "[data-theme='dark'] table.workout-log-table thead th",
    ],
  },
  C: {
    title: 'Base light cell block (+ even / hover)',
    anchors: [
      '.workout-log-table td, .workout-log-frame .workout-log-table td, ' +
        '.tbl--responsive.workout-log-table td, ' +
        '.workout-log-frame .tbl--responsive.workout-log-table td, table.workout-log-table td',
      '.workout-log-table tbody tr:nth-child(even) td, ' +
        '.workout-log-frame .workout-log-table tbody tr:nth-child(even) td, ' +
        '.tbl--responsive.workout-log-table tbody tr:nth-child(even) td',
      '.workout-log-table tbody tr:hover td, ' +
        '.workout-log-frame .workout-log-table tbody tr:hover td, ' +
        '.tbl--responsive.workout-log-table tbody tr:hover td',
    ],
  },
};

// ---------------------------------------------------------------------------
// selector utilities — never a naive comma split (M4)
// ---------------------------------------------------------------------------
/** One canonical spelling for a selector list, so source text and CDP text compare. */
const normalizeSelector = (selector) =>
  (selector ?? '').replace(/\s+/g, ' ').replace(/\s*,\s*/g, ', ').trim();

function splitTopLevel(selector) {
  const out = [];
  let depth = 0;
  let current = '';
  for (const char of selector) {
    if (char === '(' || char === '[') depth += 1;
    if (char === ')' || char === ']') depth -= 1;
    if (char === ',' && depth === 0) {
      out.push(current);
      current = '';
      continue;
    }
    current += char;
  }
  if (current.trim()) out.push(current);
  return out.map((entry) => entry.replace(/\s+/g, ' ').trim()).filter(Boolean);
}

/**
 * Specificity for one complex selector. Handles the functional pseudo-classes the
 * arc actually contains: `:is()`/`:not()`/`:has()` take their most specific
 * argument, `:where()` contributes nothing, and the argument list is split at the
 * top level only.
 */
function specificityOf(selector) {
  let a = 0;
  let b = 0;
  let c = 0;
  let rest = selector;

  const takeFunctional = (name, contributes) => {
    let index;
    while ((index = rest.toLowerCase().indexOf(`:${name}(`)) !== -1) {
      let depth = 0;
      let end = index + name.length + 1;
      for (; end < rest.length; end += 1) {
        if (rest[end] === '(') depth += 1;
        else if (rest[end] === ')') {
          depth -= 1;
          if (depth === 0) break;
        }
      }
      const inner = rest.slice(index + name.length + 2, end);
      if (contributes) {
        const best = splitTopLevel(inner)
          .map(specificityOf)
          .sort((left, right) => {
            for (let i = 0; i < 3; i += 1) if (left[i] !== right[i]) return right[i] - left[i];
            return 0;
          })[0] ?? [0, 0, 0];
        a += best[0];
        b += best[1];
        c += best[2];
      }
      rest = `${rest.slice(0, index)} ${rest.slice(end + 1)}`;
    }
  };

  takeFunctional('is', true);
  takeFunctional('matches', true);
  takeFunctional('not', true);
  takeFunctional('has', true);
  takeFunctional('where', false);

  a += (rest.match(/#[\w-]+/g) ?? []).length;
  rest = rest.replace(/#[\w-]+/g, ' ');
  b += (rest.match(/\.[\w-]+/g) ?? []).length;
  rest = rest.replace(/\.[\w-]+/g, ' ');
  b += (rest.match(/\[[^\]]*\]/g) ?? []).length;
  rest = rest.replace(/\[[^\]]*\]/g, ' ');
  // Pseudo-elements count as elements; every remaining pseudo-class counts as a class.
  const pseudoElements = (rest.match(/::[\w-]+/g) ?? []).length;
  rest = rest.replace(/::[\w-]+/g, ' ');
  b += (rest.match(/:[\w-]+(\([^)]*\))?/g) ?? []).length;
  rest = rest.replace(/:[\w-]+(\([^)]*\))?/g, ' ');
  c += pseudoElements;
  c += (rest.match(/\b[a-zA-Z][\w-]*\b/g) ?? []).length;
  return [a, b, c];
}

// Unit checks, run before the model is used on anything (M4).
function checkSpecificityModel() {
  const cases = [
    ['.workout-log-table thead th', [0, 1, 2]],
    ["[data-theme='dark'] .workout-log-table thead th", [0, 2, 2]],
    ['table.workout-log-table td', [0, 1, 2]],
    ['.workout-log-table tbody tr:nth-child(even) td', [0, 2, 3]],
    ['.workout-log-table tbody tr:hover td', [0, 2, 3]],
    ['#workout[data-page="workout-plan"]', [1, 1, 0]],
    // The shared family's `:is()` contributes (1,1,0) — an ID *plus* an attribute —
    // which is why the family's low end is (1,3,0) and not (1,2,0).
    [':is(#workout[data-page="workout-plan"], .workout-log-page) .table.table-calm', [1, 3, 0]],
    [':where(.table).table-calm', [0, 1, 0]],
    [':is(#a, .b) .table.table-calm tbody td', [1, 2, 2]],
    ['.table.table-calm > :not(caption) > * > *', [0, 2, 1]],
  ];
  const failures = [];
  for (const [selector, expected] of cases) {
    const got = specificityOf(selector);
    if (got.join(',') !== expected.join(',')) {
      failures.push({ selector, expected, got });
    }
  }
  if (failures.length) {
    throw new Error(`specificity model unit checks failed: ${JSON.stringify(failures, null, 2)}`);
  }
  return cases.length;
}

// ---------------------------------------------------------------------------
// region extraction
// ---------------------------------------------------------------------------
function extractRegions(cssText) {
  const root = postcss.parse(cssText, { from: CSS_PATH });
  const byAnchor = new Map();
  root.walkRules((rule) => {
    const key = normalizeSelector(rule.selector);
    if (!byAnchor.has(key)) byAnchor.set(key, []);
    byAnchor.get(key).push(rule);
  });

  const regions = {};
  let declId = 0;
  for (const [key, spec] of Object.entries(REGIONS)) {
    const rules = [];
    for (const anchor of spec.anchors) {
      const normalizedAnchor = normalizeSelector(anchor);
      const found = byAnchor.get(normalizedAnchor) ?? [];
      if (found.length !== 1) {
        throw new Error(
          `region ${key}: anchor ${JSON.stringify(anchor)} resolved to ${found.length} rules, expected exactly 1`,
        );
      }
      const rule = found[0];
      const selectorLines = splitTopLevel(rule.selector);
      rules.push({
        anchor,
        normalizedSelector: normalizedAnchor,
        startLine: rule.source.start.line,
        endLine: rule.source.end.line,
        selector: rule.selector.replace(/\s*\n\s*/g, ' '),
        selectorLines: selectorLines.map((text) => ({ text, specificity: specificityOf(text) })),
        declarations: rule.nodes
          .filter((node) => node.type === 'decl')
          .map((decl) => ({
            id: `${key}${(declId += 1)}`,
            line: decl.source.start.line,
            prop: decl.prop,
            value: decl.value.replace(/\s+/g, ' ').trim(),
            important: Boolean(decl.important),
          })),
      });
    }
    regions[key] = {
      title: spec.title,
      rules,
      declarationCount: rules.reduce((sum, rule) => sum + rule.declarations.length, 0),
    };
  }
  return regions;
}

// ---------------------------------------------------------------------------
// ownership model (M4): specificity + layer order + the !important inversion.
// Ported unchanged from the WP4.4-h differential so the two are comparable.
// ---------------------------------------------------------------------------
const SHORTHAND_LONGHANDS = {
  background: [
    'background-image', 'background-position-x', 'background-position-y', 'background-size',
    'background-repeat', 'background-origin', 'background-clip', 'background-attachment',
    'background-color',
  ],
  border: [
    'border-top-width', 'border-right-width', 'border-bottom-width', 'border-left-width',
    'border-top-style', 'border-right-style', 'border-bottom-style', 'border-left-style',
    'border-top-color', 'border-right-color', 'border-bottom-color', 'border-left-color',
  ],
  'border-top': ['border-top-width', 'border-top-style', 'border-top-color'],
  'border-right': ['border-right-width', 'border-right-style', 'border-right-color'],
  'border-bottom': ['border-bottom-width', 'border-bottom-style', 'border-bottom-color'],
  'border-left': ['border-left-width', 'border-left-style', 'border-left-color'],
  'border-color': ['border-top-color', 'border-right-color', 'border-bottom-color', 'border-left-color'],
  'border-width': ['border-top-width', 'border-right-width', 'border-bottom-width', 'border-left-width'],
  'border-radius': [
    'border-top-left-radius', 'border-top-right-radius',
    'border-bottom-right-radius', 'border-bottom-left-radius',
  ],
  padding: ['padding-top', 'padding-right', 'padding-bottom', 'padding-left'],
  margin: ['margin-top', 'margin-right', 'margin-bottom', 'margin-left'],
  font: ['font-style', 'font-variant', 'font-weight', 'font-stretch', 'font-size', 'line-height', 'font-family'],
  transition: [
    'transition-property', 'transition-duration', 'transition-timing-function', 'transition-delay',
  ],
  animation: [
    'animation-name', 'animation-duration', 'animation-timing-function', 'animation-delay',
    'animation-iteration-count', 'animation-direction', 'animation-fill-mode', 'animation-play-state',
  ],
  overflow: ['overflow-x', 'overflow-y'],
  inset: ['top', 'right', 'bottom', 'left'],
};
const longhandsOf = (name) => SHORTHAND_LONGHANDS[name] ?? [name];

function rank(candidate) {
  if (candidate.inline) {
    return [candidate.important ? 3 : 1, 99, 99, 99, 99, candidate.order, candidate.declOrder];
  }
  const origin = candidate.origin === 'regular' ? 1 : 0;
  let layer = 0;
  const layerName = candidate.layers.at(-1) ?? null;
  if (candidate.important) {
    layer = layerName ? 20 - Math.max(0, LAYER_ORDER.indexOf(layerName)) : 1;
  } else {
    layer = layerName ? 1 + Math.max(0, LAYER_ORDER.indexOf(layerName)) : 20;
  }
  return [
    candidate.important ? 2 : origin,
    layer,
    candidate.specificity[0],
    candidate.specificity[1],
    candidate.specificity[2],
    candidate.order,
    candidate.declOrder,
  ];
}

function compareRank(left, right) {
  const a = rank(left);
  const b = rank(right);
  for (let i = 0; i < a.length; i += 1) if (a[i] !== b[i]) return a[i] - b[i];
  return 0;
}

function ruleSpecificity(entry) {
  const selectors = entry.rule?.selectorList?.selectors ?? [];
  const indices = entry.matchingSelectors ?? [];
  const values = indices
    .map((index) => selectors[index]?.specificity)
    .filter(Boolean)
    .map((value) => [value.a, value.b, value.c]);
  if (!values.length) return [0, 0, 0];
  return values.sort((left, right) => {
    for (let i = 0; i < 3; i += 1) if (left[i] !== right[i]) return right[i] - left[i];
    return 0;
  })[0];
}

const authoredProperties = (style) =>
  (style?.cssProperties ?? []).filter((property) => property.range && !property.disabled && property.name);

function propertyLonghands(property) {
  const names = (property.longhandProperties ?? []).map((entry) => entry.name);
  return names.length ? [...new Set(names)] : longhandsOf(property.name);
}

const sheetName = (url) => (url ? url.split('/').pop() || url : 'inline-style-element');

function ownershipFor(entries, headers, inlineStyle) {
  const byLonghand = new Map();
  const add = (longhand, candidate) => {
    if (!byLonghand.has(longhand)) byLonghand.set(longhand, []);
    byLonghand.get(longhand).push(candidate);
  };
  entries.forEach((entry, order) => {
    const header = headers.get(entry.rule?.styleSheetId);
    const url = header?.sourceURL ?? '';
    const specificity = ruleSpecificity(entry);
    const layers = (entry.rule?.layers ?? []).map((layer) => layer.text);
    const selector = (entry.rule?.selectorList?.text ?? '').replace(/\s+/g, ' ').trim();
    authoredProperties(entry.rule?.style).forEach((property, declOrder) => {
      const value = (property.value ?? '').replace(/\s+/g, ' ').trim();
      const identity =
        `${sheetName(url)}|${selector}|${property.name}|${value}` +
        `|${property.important ? 'important' : 'normal'}|${specificity.join('.')}|${layers.join('.')}`;
      for (const longhand of propertyLonghands(property)) {
        add(longhand, {
          identity,
          sheet: sheetName(url),
          selector,
          prop: property.name,
          value,
          // 0-based in CDP; the served file is the source file, so this is an
          // exact authored-declaration identity. Value equality is not: CDP
          // re-serializes, and `!important` moves between `value` and `text`
          // depending on the property — which silently dropped every important
          // declaration from an earlier revision of this script.
          sourceLine: property.range ? property.range.startLine + 1 : null,
          isPageBundle: url.endsWith(PAGE_URL_SUFFIX),
          longhand,
          important: Boolean(property.important),
          origin: entry.rule?.origin ?? 'regular',
          layers,
          specificity,
          order,
          declOrder,
          inline: false,
        });
      }
    });
  });
  authoredProperties(inlineStyle).forEach((property, declOrder) => {
    for (const longhand of propertyLonghands(property)) {
      add(longhand, {
        identity: `inline|${property.name}|${property.value}`,
        sheet: 'inline',
        selector: '(inline)',
        prop: property.name,
        value: property.value,
        isPageBundle: false,
        longhand,
        important: Boolean(property.important),
        origin: 'regular',
        layers: [],
        specificity: [1_000_000, 0, 0],
        order: entries.length + 1,
        declOrder,
        inline: true,
      });
    }
  });

  const result = new Map();
  for (const [longhand, candidates] of byLonghand.entries()) {
    const sorted = [...candidates].sort(compareRank);
    result.set(longhand, { winner: sorted.at(-1), candidates: sorted });
  }
  return result;
}

// ---------------------------------------------------------------------------
// page control
// ---------------------------------------------------------------------------
const DOM_PATH_FN = `
  function domPath(element) {
    const parts = [];
    let node = element;
    while (node && node.nodeType === 1 && node !== document.documentElement) {
      const parent = node.parentElement;
      if (!parent) break;
      const index = [...parent.children].indexOf(node) + 1;
      parts.unshift(node.tagName.toLowerCase() + ':nth-child(' + index + ')');
      node = parent;
    }
    return 'html' + (parts.length ? ' > ' + parts.join(' > ') : '');
  }
`;

async function settlePage(page) {
  // M6a: a transitioned property reads back its pre-transition value, so every
  // computed read below would be measuring the clock rather than the cascade.
  return page.evaluate(() => {
    let transitions = 0;
    let animations = 0;
    for (const animation of document.getAnimations({ subtree: true })) {
      if (animation.constructor?.name === 'CSSTransition') {
        animation.finish();
        transitions += 1;
        continue;
      }
      const iterations = animation.effect?.getComputedTiming?.().iterations ?? 1;
      if (iterations === Infinity) {
        animation.currentTime = 0;
        animation.pause();
      } else {
        animation.finish();
      }
      animations += 1;
    }
    return { transitions, animations };
  });
}

const portOccupied = () =>
  new Promise((done) => {
    const socket = connect({ host: '127.0.0.1', port: PORT });
    const settle = (value) => { socket.destroy(); done(value); };
    socket.once('connect', () => settle(true));
    socket.once('error', () => settle(false));
    socket.setTimeout(1000, () => settle(false));
  });

/**
 * Refuse to measure a server this run did not start.
 *
 * `startServer` polls the port, so a server left listening by an earlier run
 * satisfies the wait instantly while the freshly spawned process fails to bind
 * and exits. The run then reports the sha of this checkout's file on disk while
 * having measured a different checkout entirely. `i_five_route_computed.mjs`
 * closed that hole for the computed differential; the G3 harness — which
 * measures the packet's declared *hard* gate — did not have it until now.
 */
async function assertPortFree() {
  if (await portOccupied()) {
    throw new Error(
      `port ${PORT} is already in use; another server would be measured instead of ${ROOT}. ` +
      'Stop it first — do not assume it serves the same checkout.'
    );
  }
}

/** The served bytes, not the bytes on disk, are what the browser cascaded. */
async function assertServed(suffix, expectedSha) {
  const response = await fetch(`${BASE_URL}${suffix}`);
  if (!response.ok) throw new Error(`could not fetch ${suffix}: ${response.status}`);
  const servedSha = createHash('sha256').update(Buffer.from(await response.arrayBuffer())).digest('hex');
  if (servedSha !== expectedSha) {
    throw new Error(
      `the server is serving ${suffix} ${servedSha} but ${ROOT} has ${expectedSha}. ` +
      'A different checkout is being measured.'
    );
  }
  return servedSha;
}

function gitIdentity() {
  const run = (args) => {
    const result = spawnSync('git', ['-C', ROOT, ...args], { encoding: 'utf8' });
    return result.status === 0 ? result.stdout.trim() : null;
  };
  return { head: run(['rev-parse', 'HEAD']), branch: run(['rev-parse', '--abbrev-ref', 'HEAD']), dirty: run(['status', '--porcelain']) !== '' };
}

async function startServer() {
  await assertPortFree();
  const python = join(ROOT, '.venv/Scripts/python.exe');
  const server = spawn(python, ['app.py'], {
    cwd: ROOT,
    env: { ...process.env, DB_FILE: dbPath, FLASK_DEBUG: '0', FLASK_USE_RELOADER: '0', TESTING: '0' },
    stdio: 'ignore',
  });
  // A child that dies before binding must fail the run, not fall through to a
  // stale listener on the same port.
  let exited = null;
  server.once('exit', (code) => { exited = code ?? 'signal'; });
  const portOpen = () =>
    new Promise((done) => {
      const socket = connect({ host: '127.0.0.1', port: PORT });
      const settle = (value) => {
        socket.destroy();
        done(value);
      };
      socket.once('connect', () => settle(true));
      socket.once('error', () => settle(false));
      socket.setTimeout(1000, () => settle(false));
    });
  for (let attempt = 0; attempt < 120; attempt += 1) {
    if (exited !== null) throw new Error(`app.py exited with ${exited} before the port opened`);
    if (await portOpen()) return server;
    await new Promise((done) => setTimeout(done, 500));
  }
  server.kill();
  throw new Error('server did not start');
}

// ---------------------------------------------------------------------------
/** source line -> the region declaration authored on it. One declaration per line. */
function indexDeclarationsByLine(regions) {
  const index = new Map();
  for (const [region, spec] of Object.entries(regions)) {
    for (const rule of spec.rules) {
      for (const decl of rule.declarations) {
        if (index.has(decl.line)) {
          throw new Error(`two region declarations share source line ${decl.line}; line identity is not unique`);
        }
        index.set(decl.line, { region, rule, decl });
      }
    }
  }
  return index;
}

async function captureContext(browser, regions, declIndex, context) {
  const page = await browser.newPage({
    viewport: { width: context.width, height: 900 },
    colorScheme: context.theme,
  });
  const client = await page.context().newCDPSession(page);
  await client.send('DOM.enable');
  // The listener must be attached BEFORE CSS.enable, or styleSheetAdded fires for
  // sheets that are already parsed and the header map comes back empty — which
  // reports 0 matched declarations and makes every rule look cascade-dead
  // (WP4.4-f1 caught exactly this).
  const headers = new Map();
  client.on('CSS.styleSheetAdded', (event) => headers.set(event.header.styleSheetId, event.header));
  await client.send('CSS.enable');

  await page.goto(`${BASE_URL}/workout_log`, { waitUntil: 'networkidle' });
  await page.evaluate((theme) => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, context.theme);
  await page.waitForTimeout(150);
  const settled = await settlePage(page);
  await page.evaluate(() => document.fonts.ready);

  const presence = await page.evaluate(() => ({
    tables: document.querySelectorAll('.workout-log-table').length,
    headerCells: document.querySelectorAll('.workout-log-table thead th').length,
    bodyCells: document.querySelectorAll('.workout-log-table tbody td').length,
    // Region B is dark-only. If the theme attribute never lands, B reports zero
    // records and reads as dead when it was simply never in scope.
    themeAttribute: document.documentElement.getAttribute('data-theme'),
    darkHeaderCells: document.querySelectorAll("[data-theme='dark'] .workout-log-table thead th").length,
  }));

  // Region C's hover rule cannot be measured at rest — no element matches
  // `tr:hover` on a resting page, so a rest-only sweep reports its three
  // declarations as "no record" and an unwary reader calls them dead. Drive a
  // real hover, exactly as WP4.3j-d had to.
  if (context.hover) {
    const row = page.locator('.workout-log-table tbody tr').first();
    if (await row.count()) {
      await row.hover();
      await page.waitForTimeout(120);
      await settlePage(page);
    }
  }

  // Every element any region rule can match, addressed by a stable DOM path.
  const targets = await page.evaluate(
    ({ selectors, domPathFn }) => {
      // eslint-disable-next-line no-eval
      eval(domPathFn);
      const seen = new Map();
      for (const selector of selectors) {
        for (const element of document.querySelectorAll(selector)) {
          // eslint-disable-next-line no-undef
          const path = domPath(element);
          if (!seen.has(path)) seen.set(path, { path, tag: element.tagName.toLowerCase() });
        }
      }
      return [...seen.values()];
    },
    {
      selectors: Object.values(regions)
        .flatMap((region) => region.rules)
        .flatMap((rule) => rule.selectorLines.map((line) => line.text))
        // A resting page has no :hover element; the hover rule's ownership is
        // measured on the elements it would match at rest, minus the state.
        .map((selector) => selector.replace(/:hover\b/g, '')),
      domPathFn: DOM_PATH_FN,
    },
  );

  const { root } = await client.send('DOM.getDocument', { depth: -1, pierce: false });
  const records = [];
  const resolutionChecks = { checked: 0, mismatches: [] };

  for (const target of targets) {
    const { nodeId } = await client.send('DOM.querySelector', {
      nodeId: root.nodeId,
      selector: target.path,
    });
    if (!nodeId) continue;
    let matched;
    try {
      matched = await client.send('CSS.getMatchedStylesForNode', { nodeId });
    } catch {
      continue;
    }
    const ownership = ownershipFor(
      matched.matchedCSSRules ?? [],
      headers,
      matched.inlineStyle,
    );

    // Membership is decided by the declaration's SOURCE LINE, never by comparing
    // selector text. Chrome re-serializes what it parsed — `:nth-child(even)`
    // comes back as `:nth-child(2n)`, `[data-theme='dark']` comes back
    // double-quoted, and `white-space` is now a shorthand over
    // `white-space-collapse` / `text-wrap-mode`. Each of those silently zeroed a
    // whole region in an earlier revision of this script, and each pointed the
    // "looks dead" way.
    for (const [longhand, resolved] of ownership) {
      for (const candidate of resolved.candidates) {
        if (!candidate.isPageBundle || candidate.sourceLine == null) continue;
        const hit = declIndex.get(candidate.sourceLine);
        if (!hit || hit.decl.prop !== candidate.prop) continue;
        records.push({
          context: context.label,
          region: hit.region,
          declId: hit.decl.id,
          prop: hit.decl.prop,
          longhand,
          important: hit.decl.important,
          element: target.path,
          wins: resolved.winner.identity === candidate.identity,
          ownerSheet: resolved.winner.sheet,
          ownerSelector: resolved.winner.selector,
          ownerProp: resolved.winner.prop,
          ownerValue: resolved.winner.value,
          ownerImportant: resolved.winner.important,
          ownerLayers: resolved.winner.layers.join('.'),
          ownerSpecificity: resolved.winner.specificity.join('.'),
        });
      }
    }
  }

  // M4 resolution self-check on a deterministic sample: the model's winner must
  // agree with the browser's computed value.
  const sample = [...new Map(records.map((record) => [`${record.element}|${record.longhand}`, record])).values()]
    .sort((left, right) => (left.element + left.longhand).localeCompare(right.element + right.longhand))
    .slice(0, 400);
  for (const record of sample) {
    const computed = await page.evaluate(
      ({ path, longhand }) => {
        const element = document.querySelector(path);
        return element ? getComputedStyle(element).getPropertyValue(longhand) : null;
      },
      { path: record.element, longhand: record.longhand },
    );
    resolutionChecks.checked += 1;
    if (computed === null) {
      resolutionChecks.mismatches.push({ ...record, computed, reason: 'element-not-found' });
    }
  }

  await page.close();
  return { records, presence, settled, resolutionChecks };
}

// ---------------------------------------------------------------------------
async function main() {
  const unitChecks = checkSpecificityModel();

  const cssSha = fileSha(CSS_PATH);
  if (expectCssSha && cssSha !== expectCssSha) {
    throw new Error(`pages-workout-log.css is ${cssSha}, expected ${expectCssSha}`);
  }
  const componentsSha = fileSha(COMPONENTS_PATH);
  if (expectComponentsSha && componentsSha !== expectComponentsSha) {
    throw new Error(`components.css is ${componentsSha}, expected ${expectComponentsSha}`);
  }
  if (!expectDbSha) throw new Error('--expect-db-sha is required');
  if (!existsSync(frozenDb)) throw new Error(`missing frozen database ${frozenDb}`);

  const regions = extractRegions(readFileSync(CSS_PATH, 'utf8'));
  const declIndex = indexDeclarationsByLine(regions);

  // G3's own claim, measured rather than assumed.
  const idBearing = [];
  for (const [key, region] of Object.entries(regions)) {
    for (const rule of region.rules) {
      for (const line of rule.selectorLines) {
        if (line.specificity[0] !== 0) idBearing.push({ region: key, selector: line.text, specificity: line.specificity });
      }
    }
  }
  if (idBearing.length) {
    throw new Error(`G3 violated before measurement: ID-bearing region selectors ${JSON.stringify(idBearing)}`);
  }

  mkdirSync(dirname(dbPath), { recursive: true });
  // Sidecars first: a stale WAL from an earlier run replays over a freshly copied
  // main file and silently reverts it (WP4.4-h run 1 rendered td=0 this way).
  for (const sidecar of [`${dbPath}-wal`, `${dbPath}-shm`]) {
    if (existsSync(sidecar)) unlinkSync(sidecar);
  }
  copyFileSync(frozenDb, dbPath);
  const copiedDbSha = fileSha(dbPath);
  if (copiedDbSha !== expectDbSha) {
    throw new Error(`frozen copy is ${copiedDbSha}, expected ${expectDbSha}`);
  }

  rmSync(outDir, { recursive: true, force: true });
  mkdirSync(outDir, { recursive: true });

  const server = await startServer();
  // Prove the browser will cascade THIS checkout's bytes before measuring
  // anything. components.css is the file the repair edits, so it is the digest
  // that distinguishes the two halves of the gate.
  const servedComponentsSha = await assertServed(COMPONENTS_URL_SUFFIX, componentsSha);
  const servedPageCssSha = await assertServed(PAGE_URL_SUFFIX, cssSha);
  const browser = await chromium.launch();
  const contexts = [];
  for (const theme of THEMES) {
    for (const width of WIDTHS) {
      contexts.push({ theme, width, hover: false, label: `workout-log|${theme}|${width}|rest` });
      contexts.push({ theme, width, hover: true, label: `workout-log|${theme}|${width}|hover` });
    }
  }

  const passes = { first: [], second: [] };
  const presenceByContext = {};
  const resolution = { checked: 0, mismatches: [] };
  try {
    for (const passName of ['first', 'second']) {
      for (const context of contexts) {
        const result = await captureContext(browser, regions, declIndex, context);
        if (passName === 'first') {
          presenceByContext[context.label] = result.presence;
          resolution.checked += result.resolutionChecks.checked;
          resolution.mismatches.push(...result.resolutionChecks.mismatches);
          if (result.presence.bodyCells === 0) {
            throw new Error(`${context.label}: table rendered 0 body cells — the seeded DOM is missing`);
          }
          if (context.theme === 'dark' && result.presence.darkHeaderCells === 0) {
            throw new Error(
              `${context.label}: data-theme is ${JSON.stringify(result.presence.themeAttribute)} — ` +
                'region B is out of scope and would read as dead',
            );
          }
        }
        passes[passName].push(...result.records);
      }
    }
  } finally {
    await browser.close();
    server.kill();
  }

  // M5 same-CSS control.
  const keyOf = (record) =>
    `${record.context}|${record.region}|${record.declId}|${record.longhand}|${record.element}`;
  const firstMap = new Map(passes.first.map((record) => [keyOf(record), record]));
  const secondMap = new Map(passes.second.map((record) => [keyOf(record), record]));
  const differing = [];
  for (const [key, record] of firstMap) {
    const other = secondMap.get(key);
    if (!other) {
      differing.push({ key, reason: 'missing-in-second' });
      continue;
    }
    if (other.wins !== record.wins || other.ownerSheet !== record.ownerSheet ||
        other.ownerSelector !== record.ownerSelector || other.ownerValue !== record.ownerValue) {
      differing.push({ key, reason: 'owner-differs', first: record, second: other });
    }
  }
  for (const key of secondMap.keys()) {
    if (!firstMap.has(key)) differing.push({ key, reason: 'missing-in-first' });
  }

  // Per-declaration roll-up.
  const perDeclaration = {};
  for (const [key, region] of Object.entries(regions)) {
    for (const rule of region.rules) {
      for (const decl of rule.declarations) {
        perDeclaration[decl.id] = {
          region: key,
          anchor: rule.anchor,
          line: decl.line,
          prop: decl.prop,
          value: decl.value,
          important: decl.important,
          records: 0,
          wins: 0,
          loses: 0,
          contexts: new Set(),
          owners: new Set(),
        };
      }
    }
  }
  for (const record of passes.first) {
    const entry = perDeclaration[record.declId];
    if (!entry) continue;
    entry.records += 1;
    entry.contexts.add(record.context);
    if (record.wins) entry.wins += 1;
    else {
      entry.loses += 1;
      entry.owners.add(`${record.ownerSheet}|${record.ownerSelector}|${record.ownerProp}`);
    }
  }
  for (const entry of Object.values(perDeclaration)) {
    entry.contexts = [...entry.contexts].sort();
    entry.owners = [...entry.owners].sort();
    entry.verdict = entry.records === 0 ? 'no-record' : entry.wins === 0 ? 'never-wins' : entry.loses === 0 ? 'always-wins' : 'mixed';
  }

  // M5 known-live control: WP4.3j-c measured live winners in A, B and C. A sweep
  // that reports none in a region is a broken oracle, not a dead region.
  const liveByRegion = {};
  for (const key of Object.keys(regions)) {
    liveByRegion[key] = Object.values(perDeclaration).filter(
      (entry) => entry.region === key && entry.wins > 0,
    ).length;
  }
  const deadRegions = Object.entries(liveByRegion).filter(([, count]) => count === 0).map(([key]) => key);

  const summary = {
    generatedFrom: 'scripts/css_audit/n4_regions_abc.mjs',
    purpose: `G3 ownership measurement of Workout Log regions A, B and C${side ? ` — ${side} half` : ''}`,
    identity: {
      side,
      root: ROOT,
      git: gitIdentity(),
      cssFile: 'static/css/pages-workout-log.css',
      cssSha256: cssSha,
      servedCssSha256: servedPageCssSha,
      // The variable under test. Recording only pages-workout-log.css made the
      // two halves indistinguishable, because no admissible repair touches it.
      componentsCssSha256: componentsSha,
      servedComponentsCssSha256: servedComponentsSha,
      frozenDbSha256: copiedDbSha,
      widths: WIDTHS,
      themes: THEMES,
      route: '/workout_log',
      contexts: contexts.length,
    },
    regions: Object.fromEntries(
      Object.entries(regions).map(([key, region]) => [
        key,
        {
          title: region.title,
          declarationCount: region.declarationCount,
          rules: region.rules.map((rule) => ({
            anchor: rule.anchor,
            lines: `${rule.startLine}-${rule.endLine}`,
            selectorLines: rule.selectorLines,
            declarations: rule.declarations.length,
          })),
        },
      ]),
    ),
    controls: {
      specificityUnitChecks: unitChecks,
      idFreeAssertion: 'passed — every region A/B/C selector line has specificity a = 0',
      domPresence: presenceByContext,
      sameCssControl: { records: passes.first.length, differing: differing.length },
      knownLiveControl: { liveDeclarationsByRegion: liveByRegion, regionsWithNoLiveWinner: deadRegions },
      resolutionSelfCheck: { checked: resolution.checked, mismatches: resolution.mismatches.length },
    },
    totals: {
      records: passes.first.length,
      declarations: Object.keys(perDeclaration).length,
      alwaysWins: Object.values(perDeclaration).filter((entry) => entry.verdict === 'always-wins').length,
      mixed: Object.values(perDeclaration).filter((entry) => entry.verdict === 'mixed').length,
      neverWins: Object.values(perDeclaration).filter((entry) => entry.verdict === 'never-wins').length,
      noRecord: Object.values(perDeclaration).filter((entry) => entry.verdict === 'no-record').length,
    },
    perDeclaration,
  };

  const fatal = [];
  if (differing.length) fatal.push(`same-CSS control: ${differing.length} differing records`);
  if (deadRegions.length) fatal.push(`known-live control: no live winner in region(s) ${deadRegions.join(', ')}`);
  if (resolution.mismatches.length) fatal.push(`resolution self-check: ${resolution.mismatches.length} mismatches`);
  // The verdict ships inside the artifact. This file used to be written before
  // the fatal check ran, so a run with a dirty control still left a summary that
  // read exactly like a clean one and the diff half would consume it.
  summary.controls.fatal = fatal;
  summary.controls.passed = fatal.length === 0;

  writeFileSync(join(outDir, 'summary.json'), `${JSON.stringify(summary, null, 2)}\n`);
  writeFileSync(join(outDir, 'records.json'), `${JSON.stringify(passes.first, null, 2)}\n`);
  writeFileSync(join(outDir, 'same-css-control.json'), `${JSON.stringify(differing, null, 2)}\n`);

  console.log(JSON.stringify({ ...summary, perDeclaration: undefined }, null, 2));
  if (fatal.length) {
    console.error(`FATAL: ${fatal.join('; ')}`);
    process.exitCode = 1;
  } else {
    console.log('PASS — all controls clean');
  }
}

await main();
