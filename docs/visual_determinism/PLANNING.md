# Visual-Capture Determinism Remediation

Status: **implemented, Gate 2 not approved.** Code + tests only — baseline PNGs are
regenerated in a separate, reviewed step (see §5 Migration notes).

Branch `wt/visual-determinism`, based on `origin/main` = `4e9b7d0`.

---

## Section 0 — Requirements

### Problem

The 84-baseline visual suite is nondeterministic. Across three runs of the *identical*
CI job at the *identical* SHA, 11 of 84 baselines varied (73 observed stable). Six were
genuine rendered-state changes, all on `plan-*` / `workout-plan-*`; five were
sub-perceptual noise. One file showed three distinct states.

Three independent causes, all pre-diagnosed and re-confirmed here from measurement:

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

### Out of scope (do not widen without a new gate)

- Regenerating baseline PNGs. `e2e/__screenshots__/**` stays byte-identical here.
- PR #281, its branch, its baselines, and `snapshotManifest` in
  `docs/CSS_PHASE4_WP4_4_A_BASELINE.json`.
- `prepare_e2e_db.py` / the functional suite's catalog state (see §4).

### Calculation surface

**None touched.** No file under `utils/`, `routes/`, `templates/`, `static/` or `app.py`
is modified. Effective Sets, weekly/session summary, progression, fatigue and volume
distribution are untouched; there is no calculation to re-derive and no worked example to
update. The `plan / log / analyze / progress / distribute / backup` workflows are
unchanged at runtime — the only behavioural delta is in the *test fixture*, and it is a
convergence: the fixture now shows the state a real user already sees ~1.6 s after
launch, instead of oscillating between that state and its predecessor.

---

## 1. Diff scope

| Path | Change |
|---|---|
| `e2e/scripts/prepare_visual_db.py` | `apply_migrations(..., upgrade_catalog=False)` gains an opt-in catalog upgrade; `main()` passes `upgrade_catalog=True`. New `_upgrade_catalog()` helper; module docstring updated. Live-data guard and `--output`-only writing untouched. |
| `e2e/visual-helpers.ts` | New: `MAX_CAPTURE_HEIGHT_PX`, `CAPTURE_SEGMENT_HEIGHT_PX`, `IMAGE_SETTLE_TIMEOUT_MS`, `collectUnloadedImages()`, `waitForImagesSettled()`, `expectFullPageScreenshot()`, `assertCaptureFits()`. `prepareForScreenshot()` now ends with `await waitForImagesSettled(page)`. |
| `e2e/visual.spec.ts` | `expect(page).toHaveScreenshot(...)` → `expectFullPageScreenshot(...)`; unused `expect` import dropped. |
| `e2e/visual-baseline-thumbnails.spec.ts` | Capture-time assertion that every `img.exercise-thumbnail` is decoded, in both the plan and log describe blocks. |
| `tests/test_visual_capture_contracts.py` | **New.** 8 contracts (§3). |
| `docs/test_inventory/TEST_INVENTORY.{json,md}` | Regenerated (blocking drift gate): pytest 2100 → 2108 nodes, 101 → 102 files, 102 → 103 test files. Playwright counts unchanged. |
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

### 3.4 Full visual-suite stability (84 tests, three consecutive passes)

Run against a manually started server on port 5199 (port 5000 was occupied by another
process in the shared checkout), through a scratch Playwright config whose
`snapshotPathTemplate` points into gitignored `artifacts/` — so `e2e/__screenshots__/**`
was never a write target at any point.

| Pass | Result |
|---|---|
| 1 (generate into `artifacts/`) | 84 failed = "A snapshot doesn't exist, writing actual" ×86. **86 writes for 84 tests** — the two segmented tests emit two files each. |
| 2 (compare) | **83 passed, 1 failed** — `volume-splitter-mobile-dark`, 18,190 px |
| 3 (compare) | **83 passed, 1 failed** — `volume-splitter-mobile-dark`, 18,190 px (identical) |

---

## 4. Known reds and deliberate non-changes

### 4.1 `volume-splitter-mobile-dark` is bistable — pre-existing, not introduced here

Two discrete rendered states differing by exactly **18,190 px (1.5%)**, a whole-page
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
`devicePixelRatio` — all byte-identical every run. The flip is therefore in
rasterisation, per browser process, not in layout or font selection. This is one of the
five "sub-perceptual noise" files from the original triage and needs its own packet.

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

1. Regenerate `e2e/__screenshots__/win32/visual.spec.ts-snapshots/` and the linux set:
   delete `user-profile-mobile-{dark,light}.png`, add the four `-segment-N.png` files.
   66 → 68 per platform.
2. `tests/test_css_wp4_4_a_baseline_contracts.py::EXPECTED_SNAPSHOT_COUNTS` —
   `win32/visual.spec.ts-snapshots` and `linux/visual.spec.ts-snapshots`: **66 → 68**.
   That test asserts the count, the exact sorted filename list, *and* a
   `nameAndSizeSha256` over names + file sizes, so it reds on the first regenerated PNG.
3. `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` → `snapshotManifest` — regenerate with
   `scripts/css_audit/emit_baseline.py`. **Deliberately not touched here** (off-limits
   for this branch); it is the reason step 2 cannot be done early either.
4. `tests/test_visual_capture_contracts.py::AWAITING_SEGMENTED_REGENERATION` → empty set.
   The contract fails until this is done.

Also expected in that step: the plan-bearing baselines (`plan-*`, `workout-plan-*`,
`workout-log-*`, and any page rendering the video button) move **once**, to the curated
play-icon state, because the fixture is now catalog-upgraded before first paint. That is
the intended convergence, not a regression — it is the state a real user's app reaches
1.6 s after launch.

---

## 6. Evidence — commands and raw results

| Gate | Command | Result |
|---|---|---|
| Full pytest | `.venv/Scripts/python.exe -m pytest tests/ -q` | **2428 passed, 2 skipped** in 441.69s |
| New contracts (red) | `pytest tests/test_visual_capture_contracts.py -q --tb=line`, carve-out emptied, pre-fix | **4 failed, 4 passed** — see §3.1 |
| New contracts (green) | same, post-fix | **8 passed** |
| Test-inventory drift | `python scripts/generate_test_inventory.py --check` | DRIFT (expected: +8 nodes) → regenerated → **"Test inventory is up to date."** |
| pyright net-new | `npx pyright@1.1.410 --outputjson` + `scripts/pyright_baseline_diff.py` | **PASS — 0 net-new (baseline 175, current 175)** |
| tsc | `npx tsc --noEmit` | **exit 0** |
| JS unit | `npm run test:js` | **9 files, 105 tests passed** |
| E2E visual ×3 | scratch config, artifacts-only snapshot path | pass 1 generate (86 writes / 84 tests); passes 2 and 3 **83 passed / 1 failed** (§4.1) |

### `e2e/__screenshots__/**` is untouched

```
$ git status --porcelain e2e/__screenshots__      # (no output)
$ find e2e/__screenshots__ -name "*.png" | wc -l  # 168
$ git rev-parse HEAD:e2e/__screenshots__          # 99777891d27703d2ea7fb3165ca310f7b0cbd8a6
$ git ls-files -s e2e/__screenshots__ | wc -l     # 168
```

`--update-snapshots` was never run. Every E2E run used a scratch Playwright config whose
`snapshotPathTemplate` resolves under gitignored `artifacts/`.

### Production code

No production file was changed. Remediation B was achievable entirely test-side: the
capture forces `loading="eager"` / `decoding="sync"` on the live DOM before waiting, so
`loading="lazy"` — a real benefit for users on the 71-image Profile page — stays in
`static/js/modules/workout-plan-media.js:19`, `templates/workout_log.html:104` and
`templates/user_profile.html:411`.

### Refactor-invariant check (root `CLAUDE.md` §1)

No plan / log / analyze / progress / distribute / backup behaviour changes: zero
production files in the diff, DB schema unchanged, no API response shape touched, no
calculation module imported by anything new. Coverage was still added (8 contracts) and
migration notes are §5.

---

## 7. Unresolved blockers

1. **Gate 2 is not approved.** This branch is a draft PR by instruction.
2. **Baseline regeneration is not done** and cannot be done here — §5 is its checklist.
   Until it lands, `AWAITING_SEGMENTED_REGENERATION` is carrying two real oversized files.
3. **`volume-splitter-mobile-dark` bistability (§4.1)** is unfixed and out of scope.
   Any regeneration run may capture either of its two states.
4. **The functional suite's startup race (§4.2)** is unfixed and out of scope.
5. **`e2e/CLAUDE.md` is a shared, never-claimed path** per
   `docs/ai_workflow/PARALLEL_WORKFLOW.md`. It was edited additively (one section) because
   leaving it asserting a 66-file inventory would be doc drift; the owner should be aware
   rather than surprised by a conflict.
