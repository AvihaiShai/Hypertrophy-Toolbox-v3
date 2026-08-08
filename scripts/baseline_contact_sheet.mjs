/**
 * Contact-sheet builder for the by-eye baseline review.
 *
 * Regenerating a platform's visual baselines is an owner action whose only real
 * gate is a human looking at the PNGs: pixel counts cannot tell expected
 * CSS-arc drift apart from a real regression hiding among them
 * (`MASTER_HANDOVER.md`, "Known LINUX visual reds"). That review is impractical
 * one file at a time -- the corpus is ~83 images per platform and the tallest is
 * 19,785 px -- so this composes labelled sheets instead.
 *
 * The problem it solves: a full-page capture scaled to fit a screen is
 * unreadable (a 375x19785 mobile page becomes a 30 px sliver). Each capture is
 * therefore **unrolled** into vertical bands laid out left-to-right, so a long
 * page reads as a multi-column strip at legible scale. That makes the defects
 * this review exists to catch -- unpainted tails, truncation, collapsed layout,
 * wrong theme, missing sections -- visible at a glance.
 *
 * No image library is required or available: Chromium is already a dependency
 * and is used as the compositor. Bands are CSS background-position offsets, so
 * nothing decodes or re-encodes the PNGs and the baselines are never rewritten.
 *
 * Output goes to the gitignored artifacts/ tree.
 *
 * usage:
 *   node scripts/baseline_contact_sheet.mjs \
 *     --dir e2e/__screenshots__/win32/visual.spec.ts-snapshots \
 *     --out artifacts/review/win32-visual
 */
import { chromium } from '@playwright/test';
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const args = process.argv.slice(2);
const getArg = (flag, fallback) => {
  const i = args.indexOf(flag);
  return i === -1 ? fallback : args[i + 1];
};

const srcDir = resolve(getArg('--dir', 'e2e/__screenshots__/win32/visual.spec.ts-snapshots'));
const outDir = resolve(getArg('--out', 'artifacts/review/sheets'));
const BAND_H = Number(getArg('--band', 1000)); // display px per unrolled band
const DISP_W = Number(getArg('--width', 340)); // display px per column

if (!resolve(outDir).startsWith(resolve('artifacts'))) {
  throw new Error(`--out must resolve under artifacts/ (got ${resolve(outDir)})`);
}

/** PNG IHDR is fixed-offset; no decoder needed just for dimensions. */
function pngSize(path) {
  const head = readFileSync(path).subarray(0, 24);
  if (head.readUInt32BE(0) !== 0x89504e47) throw new Error(`not a PNG: ${path}`);
  return { width: head.readUInt32BE(16), height: head.readUInt32BE(20) };
}

/** `welcome-mobile-dark.png` -> `welcome|dark`, so one sheet holds one page+theme. */
function groupKey(name) {
  const base = name.replace(/\.png$/, '');
  const theme = base.endsWith('-dark') || base.includes('-dark-') ? 'dark' : 'light';
  const page = base
    .replace(/-(mobile|tablet|desktop)(-.*)?$/, '')
    .replace(/-(light|dark)$/, '');
  return `${page}|${theme}`;
}

function sheetHtml(entries) {
  const blocks = entries
    .map(({ name, path, size }) => {
      const scale = DISP_W / size.width;
      const scaledH = Math.ceil(size.height * scale);
      const bands = Math.max(1, Math.ceil(scaledH / BAND_H));
      // Inlined, NOT a file:/// URL. A page built with setContent has an opaque
      // origin, so Chromium blocks local file reads and every band renders
      // blank white -- which looks exactly like a legitimately empty capture and
      // would have made this whole review a rubber stamp. Caught by looking at
      // the first sheet instead of trusting it.
      const url = `data:image/png;base64,${readFileSync(path).toString('base64')}`;
      const cols = Array.from({ length: bands }, (_, k) => {
        // Band k shows the slice starting at k*BAND_H of the SCALED image.
        // background-size pins the scale; background-position does the slicing.
        // The last band is short, so it is clipped rather than stretched.
        const h = Math.min(BAND_H, scaledH - k * BAND_H);
        return `<div class="band" style="width:${DISP_W}px;height:${h}px;
          background-image:url('${url}');
          background-size:${DISP_W}px auto;
          background-position:0 -${k * BAND_H}px;
          background-repeat:no-repeat;"></div>`;
      }).join('');
      return `<section>
        <h2>${name} <em>${size.width}×${size.height}</em> — ${bands} band(s), scale ${scale.toFixed(3)}</h2>
        <div class="strip">${cols}</div>
      </section>`;
    })
    .join('');

  return `<style>
    body{margin:0;padding:16px;background:#7a7a7a;font:13px/1.4 system-ui,sans-serif;color:#fff}
    section{margin:0 0 22px}
    h2{margin:0 0 6px;font-size:14px;font-weight:600}
    h2 em{opacity:.75;font-style:normal;font-weight:400}
    /* width:max-content + flex-shrink:0 are both load-bearing. Without them a
       strip wider than the viewport is SHRUNK by flexbox instead of overflowing,
       so an 8-band mobile page renders horizontally squashed and its right edge
       is silently cropped -- a review artifact that looks like a layout defect.
       fullPage then captures the real scrollWidth. */
    .strip{display:flex;gap:6px;align-items:flex-start;width:max-content}
    /* The checker background makes an unpainted or transparent tail obvious,
       which is the single most important defect this review must catch. */
    .band{flex:0 0 auto;outline:1px solid #000;background-color:#fff;
      background-image:linear-gradient(45deg,#bbb 25%,transparent 25%,transparent 75%,#bbb 75%),
                       linear-gradient(45deg,#bbb 25%,transparent 25%,transparent 75%,#bbb 75%);}
  </style>${blocks}`;
}

async function main() {
  mkdirSync(outDir, { recursive: true });
  const files = readdirSync(srcDir).filter((f) => f.endsWith('.png')).sort();
  if (!files.length) throw new Error(`no PNGs in ${srcDir}`);

  const groups = new Map();
  for (const name of files) {
    const path = join(srcDir, name);
    const entry = { name, path, size: pngSize(path) };
    const key = groupKey(name);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(entry);
  }

  const browser = await chromium.launch();
  const manifest = [];
  try {
    const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
    for (const [key, entries] of [...groups.entries()].sort()) {
      await page.setContent(sheetHtml(entries), { waitUntil: 'load' });
      await page.evaluate(() => Promise.all(
        Array.from(document.images ?? []).map((i) => i.decode().catch(() => {})),
      ));
      await page.waitForTimeout(150);
      const file = join(outDir, `${key.replace('|', '--')}.png`);
      await page.screenshot({ path: file, fullPage: true });
      // A blank sheet is indistinguishable from a legitimately empty capture, so
      // assert every band actually carries inlined image data before trusting it.
      // The first version of this tool used file:/// URLs, which a setContent
      // page cannot read, and produced 22 entirely white sheets that would have
      // passed a careless review.
      const painted = await page.evaluate(() => {
        const bands = Array.from(document.querySelectorAll('.band'));
        return (
          bands.length > 0 &&
          bands.every((b) => getComputedStyle(b).backgroundImage.includes('data:image/png'))
        );
      });
      if (!painted) throw new Error(`sheet ${key}: bands carry no inlined image data`);
      const size = pngSize(file);
      manifest.push({ sheet: key, file, images: entries.map((e) => e.name), size });
      console.log(`  ${key.padEnd(28)} ${entries.length} image(s) -> ${size.width}x${size.height}`);
      if (size.height > 16384 || size.width > 16384) {
        console.log('    !! sheet exceeds Chromium 16384px surface; it is truncated and NOT reviewable');
      }
    }
  } finally {
    await browser.close();
  }
  writeFileSync(join(outDir, 'sheets.json'), JSON.stringify(manifest, null, 2), 'utf8');
  console.log(`\n${manifest.length} sheets covering ${files.length} baselines -> ${outDir}`);
}

await main();
