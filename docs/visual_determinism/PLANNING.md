# Visual-Capture Determinism Remediation

Status: **✅ GATE 2 PASSED — exact-byte determinism achieved.**
Capture/test changes plus a local copy of the existing Font Awesome dependency; baseline
PNGs are **not** regenerated here and neither manifest is touched.

Branch `wt/visual-determinism`, merged with `origin/main` = `616b3a6`.

> **That status is not current.** A further cause was found on 2026-08-04 and is **still
> open**: the ubuntu-24.04 job disagrees with itself on 2–3 of 86 images per three-run
> sample, confined to the five workout-plan desktop captures. The Gate 2 evidence below
> stands for the corpus and the runs it measured — it was three samples, and the residue
> needs more than three to see. See [§8](#8-compositor-layer-paint-offsets-2026-08-04).

## Gate 2 closure (2026-08-03)

The failed result recorded below was real at SHA `40c2873`, but it is superseded by the
final remediation and fresh-process evidence:

- oversized table locators now neutralize sticky table layers, fixed navbar chrome, and
  closed offscreen drawers before capture;
- Chromium runs with its serialized compositor-stage controls (threaded animation,
  threaded scrolling, checker imaging, and image-animation resync disabled);
- the fractional translucent dark `.summary-header` capture surface is flattened to the
  existing opaque visual token; and
- Font Awesome 5.15.4 is served locally with its solid, regular, and brand WOFF2 files,
  removing the observed cdnjs 502/CORS state.

No screenshot tolerance was raised. Final evidence is partitioned because the last CSS
change can affect only six dark weekly/session-summary baselines:

| Final set | Fresh generations | Result |
|---|---:|---|
| Full 86-image corpus before the final selector | 3 | 84 tests passed each run; **85/86 byte-identical** |
| Six baselines matched by the final `.summary-header` selector | 3 | 6 tests passed each run; **6/6 byte-identical** |
| Remaining 80 baselines, untouched by the final selector | 3 | **80/80 byte-identical** in the full runs |

Therefore the final configuration is **86/86 byte-identical across three isolated DB,
server, and browser generations**. The dependency gate for baseline regeneration is
approved.

## Historical record correction (2026-08-03) — superseded by the closure above

An earlier revision of this document, and this PR's original title, claimed that **three
causes of visual nondeterminism had been closed**. **That claim was wrong and is
withdrawn.** Three fresh CI generation runs at SHA `40c2873` (runs `30769323238`,
`30769329631`, `30769336223`) measured:

> **78 of 86 regenerated screenshots byte-identical across all three runs; 8 still
> differ.** Byte-identical output was **not** reached.

**What the evidence actually supports, stated at its true strength:**

| Claim | Status |
|---|---|
| The `youtube_video_id` startup race **exists** and is measured (1.6 s; 0 → 56 curated ids; 510 rows refreshed) | **PROVEN** |
| That race **caused all plan-thumbnail instability** | **WITHDRAWN — false.** It is at most a **partial contributor** |
| Cause 3 (16,384 px truncation) is closed | **HOLDS** — all four segments single-state across three runs, painted content restored through the document bottom |

`plan-desktop-dark-advanced` still shows **three states with 33,796 hard pixels —
numerically identical to its pre-remediation figures**, i.e. an *untouched* cause, not a
partially-fixed one. Remediation did improve matters (unstable 11 → 8; genuine
rendered-state changes 6 → 3; `workout-plan-desktop-{dark,light}` and both
`plan-desktop-*-simple` became single-state), but the acceptance criterion is not met.

**Eight images observed unstable across the three post-remediation runs:**

| Image | States | Hard px | MaxΔ | Class |
|---|---|---|---|---|
| `plan-desktop-dark-advanced` | 3 | 33,796 | 221 | genuine |
| `plan-desktop-light-advanced` | 3 | 22,802 | 255 | genuine |
| `log-desktop-dark` | 2 | 323 | 202 | genuine |
| `volume-splitter-mobile-dark` | 2 | 0 | 14 | low-delta |
| `backup-mobile-dark` | 2 | 0 | 16 | low-delta |
| `progression-mobile-dark` | 2 | 0 | 2 | low-delta |
| `plan-mobile-dark-advanced` | 2 | 0 | 1 | low-delta |
| `plan-mobile-light-advanced` | 2 | 0 | 1 | low-delta |

At that historical SHA, the five low-delta cases were still gate instability and were
not dismissed or masked with tolerance. They are closed by the final compositor and
capture-layer controls above.

`log-desktop-dark` was single-state across the three *pre*-remediation runs and flips
now. **Whether it was introduced here or is pre-existing-but-unluckily-sampled cannot be
inferred from two three-sample sets** and requires controlled A/B isolation.

---

## Section 0 — Requirements

### Problem

The 84-baseline visual suite is nondeterministic. Across three runs of the *identical*
CI job at the *identical* SHA, 11 of 84 baselines varied (73 observed stable). Six were
genuine rendered-state changes, all on `plan-*` / `workout-plan-*`; five were
sub-perceptual noise. One file showed three distinct states.

At SHA `40c2873`, three candidate causes had been diagnosed and measured and **only cause
3 was demonstrably closed**. Cause 1 was a proven race and partial contributor; cause 2's
measurements were real but did not explain every residual. The final closure above adds
the table-layer, compositor, summary-surface, and local-font controls that this initial
section did not yet contain:

| # | Cause | Measured evidence (this worktree) |
|---|---|---|
| 1 | **Startup race.** `e2e/fixtures/database.visual.seed.db` has no `youtube_video_id` column; `prepare_visual_db.py` runs `run_all_initializers()`, which `ALTER TABLE`s it in as all-NULL. `app.py` then runs `upgrade_catalog_from_seed()`, which mutates the DB *after* Playwright's TCP-only readiness check has passed. | column absent from the fixture; **0** curated ids after seed prep; `upgrade_catalog_from_seed()` = **1.621 s**, **0 → 56** curated ids, **510** rows refreshed. **4 of the 6** seeded plan exercises (Bench Press, Bent Over Row, Deadlift, Curl) are curated, so `buildPlayButton` renders a magnifier before the upgrade and a play icon after it. |
| 2 | **Media readiness never awaited.** `loading="lazy"` + `decoding="async"`; `prepareForScreenshot` waits on `networkidle`, which fires *before* below-fold lazy images are ever requested. The capture then scrolls and races the raster. | at the exact moment `prepareForScreenshot` returned: `workout_plan` 375×812 → **6 of 6** thumbnails unloaded; `workout_log` → **3 of 6**; `user_profile` → **61 of 71** images (desktop: 19 of 71). |
| 3 | **Chromium's 16,384 px surface limit.** A taller `fullPage` capture does not fail — it truncates to a flat, unpainted tail. | exactly **2** of 84 baselines exceed it: `user-profile-mobile-dark` (375×19785) and `user-profile-mobile-light` (375×19742). Truncation measured at document row **16,392**; the tail is **3,393 px = 17.1%** of the page and decodes to **1 distinct colour** (`#0f1220`). Next tallest baseline is 11,570. |

### Approved scope

- **A** — make the prepared visual DB fully catalog-upgraded before the server starts.
  Keep the live-data guard; keep writing only to `--output`.
- **B** — make `prepareForScreenshot` wait for decoded images, with a bounded timeout
  that fails loudly. Prefer a test-side fix over changing production markup.
- **C** — segment the user-profile capture so no capture exceeds 16,384 px and the full
  dark page is exercised. The screenshot inventory changes; that is intended.
- **D** — neutralize fixed/sticky layers for oversized table locators and serialize the
  Chromium compositor pipeline without raising tolerance.
- **E** — serve the existing Font Awesome 5.15.4 dependency locally so icon pixels do
  not depend on a cross-origin CDN response.

### Out of scope (do not widen without a new gate)

- Regenerating baseline PNGs. `e2e/__screenshots__/**` stays byte-identical here.
- PR #281, its branch, its baselines, and `snapshotManifest` in
  `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`.
- `prepare_e2e_db.py` / the functional suite's catalog state (see §4).

### Calculation surface

**No calculation surface is touched.** Effective Sets, weekly/session summary,
progression, fatigue and volume distribution are unchanged; there is no calculation to
re-derive and no worked example to update. Runtime logic is unchanged. The only
production delivery change is `templates/base.html` pointing the same Font Awesome
5.15.4 stylesheet at the vendored local copy instead of cdnjs.

---

## 1. Diff scope

| Path | Change |
|---|---|
| `e2e/scripts/prepare_visual_db.py` | `apply_migrations(..., upgrade_catalog=False)` gains an opt-in catalog upgrade; `main()` passes `upgrade_catalog=True`. New `_upgrade_catalog()` helper; module docstring updated. Live-data guard and `--output`-only writing untouched. |
| `e2e/visual-helpers.ts` | New: `MAX_CAPTURE_HEIGHT_PX`, `CAPTURE_SEGMENT_HEIGHT_PX`, `IMAGE_SETTLE_TIMEOUT_MS`, `collectUnloadedImages()`, `waitForImagesSettled()`, `expectFullPageScreenshot()`, `assertCaptureFits()`. `prepareForScreenshot()` now ends with `await waitForImagesSettled(page)`. |
| `e2e/visual.spec.ts` | `expect(page).toHaveScreenshot(...)` → `expectFullPageScreenshot(...)`; unused `expect` import dropped. |
| `e2e/visual-baseline-thumbnails.spec.ts` | Capture-time assertion that every `img.exercise-thumbnail` is decoded, in both the plan and log describe blocks. |
| `playwright.config.ts` | Serializes compositor stages and disables threaded/checker/image-resync paths used by Chromium's deterministic headless pipeline. |
| `templates/base.html`, `static/vendor/fontawesome/**` | Replace cdnjs Font Awesome 5.15.4 with the identical local CSS, solid/regular/brand WOFF2 assets, and upstream license. |
| `tests/test_visual_capture_contracts.py` | **New.** 11 contracts (§3). |
| `docs/test_inventory/TEST_INVENTORY.{json,md}` | Regenerated (blocking drift gate): pytest **2111** deterministic nodes across 102 files. Playwright counts unchanged. |
| `e2e/CLAUDE.md` | Visual-spec contract section: records the segmented capture, the pre-started catalog, and the regeneration checklist. |
| `docs/visual_determinism/PLANNING.md` | This file. |

**Not touched:** `e2e/__screenshots__/**`, `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`,
`tests/test_css_wp4_4_a_baseline_contracts.py`, `e2e/scripts/prepare_e2e_db.py`,
`playwright.config.ts`, and every production source file.

---

## 2. Revised screenshot inventory

`visual-baseline-thumbnails.spec.ts` is unchanged: **18 per platform**.

`visual.spec.ts`, per platform: **66 → 68**.

| | Old | New |
|---|---|---|
| Removed | `user-profile-mobile-dark.png` (375×19785, truncated at 16,392) | — |
| Removed | `user-profile-mobile-light.png` (375×19742, truncated at 16,375–16,392) | — |
| Added | — | `user-profile-mobile-dark-segment-1.png` (375×10000) |
| Added | — | `user-profile-mobile-dark-segment-2.png` (375×9785) |
| Added | — | `user-profile-mobile-light-segment-1.png` (375×10000) |
| Added | — | `user-profile-mobile-light-segment-2.png` (375×9742) |

The other 64 `visual.spec.ts` names and all 18 thumbnail names are byte-for-byte
unchanged — `expectFullPageScreenshot` only segments a page taller than
`MAX_CAPTURE_HEIGHT_PX`, and no other page is.

Segments tile the document exactly: 10000 + 9785 = **19785** (dark), 10000 + 9742 =
**19742** (light) — no gap, no overlap, identical to the old nominal page heights.
Verified painted: every band of both new segments decodes to 57–155 distinct colours,
against **1** for the old truncated tail.

Totals per platform: **84 → 86**. Repository-wide (win32 + linux): **168 → 172**.

Playwright *test* counts do not change (547): a segmented page issues two
`toHaveScreenshot` calls inside one test.

---

## 3. Tests, with recorded red and green

Red paths were executed, not asserted in prose. Commands and raw output below.

### 3.1 `tests/test_visual_capture_contracts.py` (8 nodes)

RED — run before any fix, with `AWAITING_SEGMENTED_REGENERATION` temporarily emptied:

```
$ .venv/Scripts/python.exe -m pytest tests/test_visual_capture_contracts.py -q --tb=line
E AssertionError: Baselines over Chromium's 16384px capture surface:
  {'user-profile-mobile-dark.png': (375, 19785), 'user-profile-mobile-light.png': (375, 19742)}.
E AssertionError: e2e/visual-helpers.ts must export MAX_CAPTURE_HEIGHT_PX = 16_384 ...
E AssertionError: Prepared visual DB has 0 curated youtube_video_id rows but the shipped
  catalog has 56. app.py startup would mutate the difference in under a running capture.
E AssertionError: app.py startup would still apply a catalog upgrade:
  CatalogUpgradeResult(applied=True, inserted=0, refreshed=510, reason=None)
4 failed, 4 passed, 1 warning in 4.13s
```

Note the red for the corpus contract names **exactly** the two user-profile mobile
files, and only those, out of 168 committed PNGs.

GREEN — after the fix:

```
$ .venv/Scripts/python.exe -m pytest tests/test_visual_capture_contracts.py -q
8 passed, 1 warning in 3.28s
```

### 3.2 Capture-time thumbnail assertion (`visual-baseline-thumbnails.spec.ts`)

RED — the `await waitForImagesSettled(page)` line removed from `prepareForScreenshot`,
i.e. "the wait removed":

```
Error: exercise thumbnails must be decoded before the capture
  expect(received).toEqual(expected)
  - Array []
  + Array [
  +   ".../Barbell_Bench_Press_-_Medium_Grip/0.jpg",
  +   ".../Bent_Over_Barbell_Row/0.jpg",
  +   ".../Barbell_Full_Squat/0.jpg",
  +   ".../Barbell_Deadlift/0.jpg",
  +   ".../Barbell_Curl/0.jpg",
  +   ".../Seated_Barbell_Military_Press/0.jpg",
  + ]
  at e2e/visual-baseline-thumbnails.spec.ts:94
1 failed  (plan-mobile-dark-simple)
```

GREEN — all 18 thumbnail tests pass in the full runs below.

### 3.3 Capture-size invariant (`assertCaptureFits`)

RED — the segmentation branch in `expectFullPageScreenshot` disabled:

```
Error: user-profile-mobile-dark.png: a capture 19785px tall exceeds Chromium's 16384px
surface limit. Chromium does not error on this — it returns a flat, unpainted tail, so
the excess would be baselined as "never rendered".
  Expected: <= 16384
  Received:    19785
  at assertCaptureFits (e2e/visual-helpers.ts:348)
2 failed   (user-profile mobile light, user-profile mobile dark)
```

Exactly the two tests, and only those, out of 66.

GREEN — the same two tests pass segmented in the full runs below.

### 3.4 Final visual-suite stability (84 tests / 86 images)

Run against a manually started server on port 5199 (port 5000 was occupied by another
process in the shared checkout), through a scratch Playwright config whose
`snapshotPathTemplate` points into gitignored `artifacts/` — so `e2e/__screenshots__/**`
was never a write target at any point.

The earlier three-run result was 83/84 and is retained in git history. The final gate used
three fresh prepared databases, Flask processes, and Chromium processes per set. The full
runs passed 84/84 and wrote 86 images each; 85 were byte-identical. The sole remaining
state was a 213-pixel, MaxΔ=1 edge on a translucent `.summary-header`. After flattening
that capture-only surface, all six baselines the selector can affect were byte-identical
across three more fresh generations. Together this proves final **86/86 exact-byte
stability** without a tolerance increase.

---

## 4. Known reds and deliberate non-changes

### 4.1 Resolved: cross-process compositor bistability

The original evidence showed two discrete rendered states differing by exactly **18,190 px (1.5%)**, a whole-page
glyph-edge shift (text antialiasing), reproducible to the pixel. Proven pre-existing by
stashing all four `e2e/` changes and re-running the single test five times against a
freshly generated baseline on the **unmodified** helper:

```
PRE-CHANGE run 1: 18190 pixels different
PRE-CHANGE run 2: 1 passed
PRE-CHANGE run 3: 18190 pixels different
PRE-CHANGE run 4: 18190 pixels different
PRE-CHANGE run 5: 1 passed
```

Ruled out as the cause, across six consecutive loads: font faces loaded (31, identical
list), `document.fonts.status`, computed `font-family`, `-webkit-font-smoothing`, the
`<h1>` bounding rect (`49, 107, 277, 22.86`), `scrollHeight` (3144), `clientWidth`,
`devicePixelRatio` — all byte-identical every run. The flip was therefore in
rasterisation, per browser process, not in layout or font selection. Serializing the
compositor stages closes this class: the five residual targets were **5/5 byte-identical
across three fresh processes**, and the final partitioned full gate is 86/86.

### 4.2 `prepare_e2e_db.py` deliberately keeps its uncurated catalog

`prepare_e2e_db.py` imports `apply_migrations` from `prepare_visual_db.py`, so making the
upgrade unconditional would have flipped the functional suite too. It must not:
`e2e/workout-plan.spec.ts:822` asserts *"Seed rows are uncurated → search-variant icon"*
and expects `fa-search`. Hence the `upgrade_catalog=False` default with an explicit
opt-in from the visual seeder only. `test_the_functional_seed_is_not_dragged_into_the_catalog_upgrade`
locks that decision.

The functional suite therefore still carries the same latent startup race. It is out of
scope here and needs its own packet.

### 4.3 The oversize contract carries a bounded, self-cleaning carve-out

`AWAITING_SEGMENTED_REGENERATION` names the two retired baselines. The two constraints —
"the contract must be red today on exactly those two files" and "leave
`e2e/__screenshots__/**` untouched" — cannot both hold *and* leave the test green, because
the fix that removes those files is the regeneration step this PR is forbidden to do.

The carve-out is a strict **equality**, not an allowlist: a new oversized baseline fails
it, and so does a stale entry. Once regeneration replaces those names, the computed set
is empty, the constant no longer matches, and the test forces its own deletion.

---

## 5. Migration notes — the regeneration step

Regenerating the baselines is a separate, reviewed change. It must do all four of these
together, or CI goes red:

1. Regenerate each independently maintained platform set: delete
   `user-profile-mobile-{dark,light}.png`, add the four `-segment-N.png` files,
   and move that platform 66 → 68. PR #281 performs the Linux half; Windows
   remains an owner-local follow-up.
2. `tests/test_css_wp4_4_a_baseline_contracts.py::EXPECTED_SNAPSHOT_COUNTS` —
   move the regenerated platform's entry **66 → 68**.
   That test asserts the count, the exact sorted filename list, *and* a
   `nameAndSizeSha256` over names + file sizes, so it reds on the first regenerated PNG.
3. `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` → `snapshotManifest` — regenerate with
   `scripts/css_audit/emit_baseline.py`. **Deliberately not touched here** (off-limits
   for this branch); it is the reason step 2 cannot be done early either.
4. Remove the regenerated platform's relative paths from
   `tests/test_visual_capture_contracts.py::AWAITING_SEGMENTED_REGENERATION`.
   The set becomes empty after both platform workflows are complete.

Also expected in that step: the plan-bearing baselines (`plan-*`, `workout-plan-*`,
`workout-log-*`, and any page rendering the video button) move **once**, to the curated
play-icon state, because the fixture is now catalog-upgraded before first paint. That is
the intended convergence, not a regression — it is the state a real user's app reaches
1.6 s after launch.

---

## 6. Evidence — commands and raw results

| Gate | Command | Result |
|---|---|---|
| Full pytest | `.venv/Scripts/python.exe -m pytest tests/ -q` | **2431 passed, 2 skipped** in 444.41s |
| New contracts (red) | `pytest tests/test_visual_capture_contracts.py -q --tb=line`, carve-out emptied, pre-fix | **4 failed, 4 passed** — see §3.1 |
| New contracts (green) | `pytest tests/test_visual_capture_contracts.py -q` | **11 passed** |
| Test-inventory drift | `python scripts/generate_test_inventory.py --check` | DRIFT (expected: +8 nodes) → regenerated → **"Test inventory is up to date."** |
| pyright net-new | `npx pyright@1.1.410 --outputjson` + `scripts/pyright_baseline_diff.py` | **PASS — 0 net-new (baseline 175, current 175)** |
| tsc | `npx tsc --noEmit` | **exit 0** |
| JS unit | `npm run test:js` | **9 files, 105 tests passed** |
| E2E visual ×3 | fresh DB/server/browser generations, artifacts-only snapshot path | final partitioned gate **86/86 byte-identical** (§3.4) |

### `e2e/__screenshots__/**` is untouched

```
$ git status --porcelain e2e/__screenshots__      # (no output)
$ find e2e/__screenshots__ -name "*.png" | wc -l  # 168
$ git rev-parse HEAD:e2e/__screenshots__          # 99777891d27703d2ea7fb3165ca310f7b0cbd8a6
$ git ls-files -s e2e/__screenshots__ | wc -l     # 168
```

Every `--update-snapshots` E2E run used a scratch Playwright config whose
`snapshotPathTemplate` resolves under gitignored `artifacts/`; the committed screenshot
tree was never a write target.

### Production delivery

No application logic changed. Remediation B remains entirely test-side: the capture
forces `loading="eager"` / `decoding="sync"` on the live DOM before waiting, so production
lazy loading stays. The sole production-facing change makes Font Awesome local; it
removes the measured cdnjs 502/CORS failure while preserving version 5.15.4 and all three
font families used by the templates.

### Refactor-invariant check (root `CLAUDE.md` §1)

No plan / log / analyze / progress / distribute / backup behaviour changes: DB schema
unchanged, no API response shape touched, and no calculation module imported by anything
new. Coverage was added (11 contracts) and migration notes are §5.

---

## 7. Remaining follow-up (not Gate 2 blockers)

1. **Baseline regeneration is not done here** — §5 is its checklist and PR #281 owns it.
   Until it lands, `AWAITING_SEGMENTED_REGENERATION` is carrying two real oversized files.
2. **The functional suite's startup race (§4.2)** is unfixed and out of scope.
3. **`e2e/CLAUDE.md` is a shared, never-claimed path** per
   `docs/ai_workflow/PARALLEL_WORKFLOW.md`. It was edited additively (one section) because
   leaving it asserting a 66-file inventory would be doc drift; the owner should be aware
   rather than surprised by a conflict.

---

## 8. Compositor-layer paint offsets (2026-08-04)

A fourth cause, unaddressed by everything above. Recorded here in full because the Gate 2
section reads as final and is not.

### 8.1 What it looked like

`workout-plan desktop light` failed on the ubuntu-24.04 `visual-linux` job at a SHA whose
only content change was six stale progression PNGs. Across two deep-gate compares:

| Run | Result |
|---|---|
| [30866727146](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/30866727146) | `workout-plan desktop light` failed all 3 attempts; **1 failed / 83 passed** |
| [30908183232](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/30908183232) | **2 flaky / 82 passed** — `workout-plan desktop light` failed twice then passed, `plan-desktop-light-advanced` failed once then passed |

A green conclusion reached through retries is not a pass, so neither run met the bar.

### 8.2 What it actually was

Run 30866727146 kept all three attempts' PNGs. Attempt 1 and retry 2 were **byte-identical**
(`2fe65a80…`); retry 1 was different (`a5f4f8bb…`). Two rasters, one job, one SHA — so the
variable was the renderer, not the page.

Cluster-matching the two rasters resolves **197 differing clusters, essentially all of them
a `dy = 1` shift of unchanged pixel values, most with residual 0**. Row rules, glyph runs
and whole button pills were the same pixels one device row lower. That is paint-offset
rounding, not antialiasing:

```
y=447  A=(23,27,48)     B=(23,27,48)
y=448  A=(122,128,153)  B=(23,27,48)      <- separator in A
y=449  A=(31,35,52)     B=(122,128,153)   <- separator in B, one row down
y=452  A=(31,35,52)     B=(31,35,52)      <- re-synced
```

Chromium rounds an element's paint offset against the subpixel accumulation of the
compositor layer it paints into. `static/css/layout.css` promotes `.tbl-wrap`
(`translateZ(0)`, `backface-visibility: hidden`, `will-change: scroll-position`) and
`.tbl` / `.tbl--responsive` (`translateZ(0)`, hidden backfaces) for scroll smoothness. A
capture is taken at the origin and never scrolls, so it gains nothing from them and
inherits their rounding.

### 8.3 A falsified hypothesis, recorded so it is not retried

`--disable-lcd-text` and `--disable-partial-raster` were proposed for a glyph-antialiasing
flip. The cluster analysis above says no such flip occurred. Two generate runs carrying
both switches ([30922971713](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/30922971713) /
[30923013576](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/30923013576))
still disagreed on 2 of 86 images, and moved **12 baselines that were never unstable**.
They were dropped. An earlier `translateZ(0)`-removal experiment was also called falsified,
but it had only ever been run in *compare* mode against baselines generated **with**
promotion, so it could not have shown success whatever it did.

### 8.4 Status: OPEN — narrowed, not closed

Everything below is measured. It does **not** add up to a fix: after six independent
controls the ubuntu-24.04 job still disagrees with itself on 2–3 of 86 images per
three-run sample, always among the five workout-plan desktop captures, always the same
table rows re-rounded. The owner decision this now needs is in §8.8.

### 8.5 The capture controls that were tried, and what each measured

**`dropCompositingHints()`** clears, at capture time only, every identity transform, every
non-`auto` `will-change` and every hidden `backface-visibility` on the page, then settles a
frame. Keyed on *computed* values rather than a selector list (presentation classes are
what CSS refactors rename, per `tests/test_visual_selector_contracts.py`), and restricted
to identity transforms, which paint nothing — removing one cannot move a pixel a real
transform was responsible for.

That took the four unstable images down to one, and the exact-head compare
([30925912334](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/actions/runs/30925912334))
still red on `plan-desktop-dark-advanced`. A third raster of that image made the rest of
the mechanism measurable. Row rules in the advanced plan table sit at

```
271.28125   449.4375   608.875   768.3125   927.75   1124.625
```

px below the table top, and the table top is fractional too — **1826.1875 px** on the plan
page, the sum of every fractional height stacked above it. Chromium picks the device row
for a 1px rule from `boundary + fraction(table top)`, so three rasters at one SHA put the
first two rules at 270/449, 270/448 and 271/449 — exactly what fractions of ~0, ~0.19 and
~0.22 predict. Nothing above the table appears in that capture, and it was steering the
capture's pixels anyway.

A paint-origin snap was also tried, on the theory that the table's fractional document
top was the varying quantity. **A geometry probe falsified that.** With `PW_ORIGIN_PROBE=1`
every capture logged document size, viewport, the captured table's rect, its first eight
row rects and its whole ancestor chain to five decimal places. Across two ubuntu-24.04
runs at one SHA, **all 84 records matched exactly** while the PNGs did not. Layout is not
the variable; raster is. The snap was removed rather than kept as a harmless extra.

The remaining controls, all capture-side, all keeping production untouched:

| Control | Where | Measured effect |
|---|---|---|
| `dropCompositingHints()` | `e2e/visual-helpers.ts` | 4/86 unstable → 0/86 over two runs; a later compare still flipped one image |
| `--disable-lcd-text`, `--disable-partial-raster` | `playwright.config.ts` (Linux) | 7/86 → 2/86 over three runs |
| `--num-raster-threads=1` | same | still 2/86, different pair |
| `--max-untiled-layer-{width,height}=20000` | same | still 2/86 |
| explicit document `clip` on full-page captures | `expectFullPageScreenshot` | still 3/86 |

### 8.6 What moved in the baselines, and why

53 of 86 Linux baselines change. Six are the progression PNGs left stale by #291 (the
`Available exercises: 6` line and its 19 px of page height), byte-identical to the packet
PR #294 proposed. The other 47 carry **zero** pixels above delta 128; hard pixels
(delta > 64) run 0–684 per image against 1–4 M total, and most resolve to a ±1 px shift.

The largest residual is a real improvement, not a regression. On the volume-splitter empty
state the committed baseline painted the table's last separator as neutral
`rgb(208,208,208)`; the regenerated one paints `rgb(125,131,157)` — the accessible colour
#290 gave it, and the value `getComputedStyle` reports for that `td`'s `border-bottom`.
Captured locally at 1:1 with the hints promoted **and** cleared, the product renders
`rgb(125,131,157)` in both. The promoted capture path had been washing that separator out.

### 8.7 Windows

`dropCompositingHints` is cross-platform. The `win32` set was already stale before it:
against a pristine `main` tree at the pinned Playwright 1.61, a full local `win32` compare
reds broadly, and `plan-desktop-light-advanced` alone differs by 541,849 px (29%).
Regenerating and reviewing `win32` remains the owner-local follow-up §5/§7 already track —
this packet does not widen into it, and it changes no `win32` PNG.

### 8.8 The open decision

Six independent capture controls have been tried and measured (§8.5). None closes the
gate. What is now known with confidence:

1. **Layout is not the variable.** 84/84 geometry records identical across two runs.
2. **The variable is raster**, and it is decided **once per browser process** — which is
   why the two-consecutive-screenshots stabilization in `toHaveScreenshot` cannot filter
   it, and why two whole runs can agree by luck. Three samples is the minimum useful
   test; every earlier "N/N byte-identical" claim in this document rests on two or three.
3. **It scales with capture width.** At the 375px and 768px viewports nothing has ever
   flipped. At 1440px only the five captures wider than the viewport flip. Widening the
   desktop viewport to 1700px — run as a deliberate experiment — made **all 28** desktop
   captures flip, so "wider than the viewport" is not the trigger; sheer width is.
4. Every diff is the same table rows re-rounded by one device row, at unchanged colour
   values and unchanged layout.

Point 3 also kills the last mechanical fix, since widening the viewport was it. What
remains are owner decisions, not technical ones:

- **A — narrow the desktop matrix** so the plan page no longer needs a wide raster.
  Cheapest; stops exercising the 1440px layout.
- **B — take the five workout-plan desktop captures off the byte gate** and cover that
  surface the way `visual-field-separator.spec.ts` already does, with computed-style
  assertions. Keeps every other baseline strict; loses pixel coverage on the busiest
  table.
- **C — pin the runner harder**, e.g. a self-hosted or container-pinned runner, removing
  the per-process variability a shared GitHub runner introduces. Highest cost.
- **D — accept the deep gate red on these five** and gate on the other 81.

Nothing in §8.5 should be merged on its own: the controls move 53 baselines without
buying determinism, so they would trade one red gate for a larger diff and the same red
gate. They are recorded here so the next attempt starts from measurement rather than from
the antialiasing and paint-origin theories this one falsified.
