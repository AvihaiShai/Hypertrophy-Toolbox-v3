# WP4.3i-h — Workout Plan obsolete theme-selector removal

Packet: WP4.3i-h (Phase 4 CSS, page #9 Workout Plan)
Base: `main` @ `00eb6f9`, branch `wt/css-wp4-3i-h`, isolated worktree
Date: 2026-07-25

## Scope

Deletion only, in `static/css/pages-workout-plan.css`. Every rule gated exclusively on
`[data-bs-theme="dark"]` or `.dark-mode` was removed. These are obsolete theme mechanisms that
cannot match at runtime.

No token extraction, no `!important` removal, no layer movement, no duplicate-selector
consolidation, no selector rewriting, no formatting changes. The diff is **113 deletions,
0 insertions** in the CSS.

## Why these rules are dead

1. **`data-bs-theme` is never written.** `static/js/darkMode.js:64,66` is the only theme writer and
   it sets `data-theme` (`'dark'` / `'light'`). A repo-wide search over `*.js`, `*.ts`, `*.html`,
   `*.py`, `*.css`, `*.json` (excluding `node_modules`) found `data-bs-theme` in
   `pages-workout-plan.css` **and nowhere else** — not in the Bootstrap build, not in any template,
   not in any script.
2. **`.dark-mode` is never applied as a class.** No template, page script, or test calls
   `classList.add/toggle/replace` with it, and no `class="…"` attribute contains it. The only
   occurrences are: an unrelated `data-testid="dark-mode-toggle"` and `id="darkModeToggle"` in
   `templates/base.html:217`; a defensive *read* in `e2e/fatigue-stage4-smokes.spec.ts:39`
   (`classList.contains('dark-mode')`, a fallback that never fires because `data-theme` is present);
   and a `body.dark-mode` rule in `static/css/layout.css:1120` — a shared bundle, out of scope for
   this packet, flagged below.
3. **No mixed rules.** All 18 rules are gated *exclusively* on the dead mechanisms: every
   comma-separated arm of every rule carries one of them. Zero rules had a live arm, and zero of the
   deleted rules reference `[data-theme=`.

## Rules removed (18)

Superset token block (was line 3512):

| # | Selector |
|---|---|
| 1 | `[data-bs-theme="dark"]` (dark override of `--superset-bg-1..4`) |

Muscle Selector dark block (was lines 5473–5577):

| # | Selector |
|---|---|
| 2 | `[data-bs-theme="dark"] .muscle-selector-container, .dark-mode .muscle-selector-container` |
| 3 | `[data-bs-theme="dark"] .muscle-selector-content, .dark-mode .muscle-selector-content` |
| 4 | `[data-bs-theme="dark"] .svg-container, .dark-mode .svg-container` |
| 5 | `[data-bs-theme="dark"] .body-outline, .dark-mode .body-outline` |
| 6 | `[data-bs-theme="dark"] .muscle-region, .dark-mode .muscle-region` |
| 7 | `[data-bs-theme="dark"] .muscle-region:hover, …:hover/.hover ×4 arms` |
| 8 | `[data-bs-theme="dark"] .muscle-region.selected, .dark-mode .muscle-region.selected` |
| 9 | `[data-bs-theme="dark"] .muscle-region.selected:hover, … ×4 arms` |
| 10 | `[data-bs-theme="dark"] .muscle-region.partial, .dark-mode .muscle-region.partial` |
| 11 | `[data-bs-theme="dark"] .legend-item:hover, … ×4 arms` |
| 12 | `[data-bs-theme="dark"] .legend-checkbox, .dark-mode .legend-checkbox` |
| 13 | `[data-bs-theme="dark"] .legend-key, .dark-mode .legend-key` |
| 14 | `[data-bs-theme="dark"] .legend-items::-webkit-scrollbar-thumb, .dark-mode …` |
| 15 | `[data-bs-theme="dark"] .legend-items::-webkit-scrollbar-thumb:hover, .dark-mode …` |
| 16 | `[data-bs-theme="dark"] .selection-summary, .dark-mode .selection-summary` |
| 17 | `[data-bs-theme="dark"] .muscle-body-tabs .nav-link:hover, .dark-mode …` |
| 18 | `[data-bs-theme="dark"] .muscle-body-tabs .nav-link.active, .dark-mode …` |

Also removed: the 7 comments that exclusively described these rules
(`/* Dark mode superset colors */`, `/* Dark mode SVG body outline */`, `/* Dark mode muscle regions */`,
`/* Dark mode legend */`, `/* Dark mode scrollbar */`, `/* Dark mode summary */`, `/* Dark mode tabs */`)
and 17 blank lines that separated them. The `DARK MODE` section banner was **kept** — the region
still contains a live `[data-theme='dark'] .workout-estimate-provenance` rule.

## Deltas

| Metric | Before | After | Delta |
|---|---|---|---|
| File lines | 5,993 | 5,880 | **−113** |
| CSS rules (postcss walk) | 778 | 760 | −18 |
| Declarations removed | — | — | 30 |
| Raw color literals | 840 | 808 | **−32** (12 hex, 20 rgba) |
| `!important` | 520 | 520 | **0** (none were present in the deleted rules) |

Diff is deletion-only: `113 deletions(-)`, `0` added lines.

### Stylelint — focused (`static/css/pages-workout-plan.css`)

| Rule | Before | After | Delta |
|---|---|---|---|
| `declaration-property-value-disallowed-list` (hardcoded color) | 511 | 481 | **−30** |
| `no-descending-specificity` | 73 | 61 | **−12** |
| `declaration-no-important` | 520 | 520 | 0 |
| `selector-max-id` | 75 | 75 | 0 |
| `selector-max-specificity` | 77 | 77 | 0 |
| `no-duplicate-selectors` | 7 | 7 | 0 |
| **TOTAL** | **1,263** | **1,221** | **−42** |

### Stylelint — total (`static/css/*.css` + `scss/**/*.scss`)

| Rule | Before | After | Delta |
|---|---|---|---|
| `declaration-property-value-disallowed-list` | 2,580 | 2,550 | −30 |
| `no-descending-specificity` | 659 | 647 | −12 |
| `declaration-no-important` | 2,252 | 2,252 | 0 |
| `selector-max-id` | 191 | 191 | 0 |
| `selector-max-specificity` | 187 | 187 | 0 |
| `no-duplicate-selectors` | 46 | 46 | 0 |
| `declaration-block-no-duplicate-properties` | 2 | 2 | 0 |
| `property-no-unknown` | 2 | 2 | 0 |
| **TOTAL** | **5,919** | **5,877** | **−42** |

**No category increased**, focused or total.

## Contract lock

`tests/test_css_cascade_contracts.py::test_workout_plan_drops_obsolete_theme_selector_mechanisms`
(new). It asserts the *premises* as well as the outcome, so the lock stays honest if the runtime
changes:

- `darkMode.js` still writes `data-theme` and still never writes `data-bs-theme`;
- no template, `static/js` script, or e2e spec applies `dark-mode` as a class;
- the bundle contains neither `data-bs-theme` nor `.dark-mode`;
- the live `[data-theme='dark']` mechanism is still present in the bundle.

Red-path proven twice: reinserting a `[data-bs-theme="dark"] .svg-container` rule fails the test,
and so does reinserting a `.dark-mode .svg-container` rule. The `class="…dark-mode"` guard was
verified to match a real class attribute while ignoring `data-testid="dark-mode-toggle"` and
`class="dark-mode-toggle"`.

## Gates

| Gate | Result |
|---|---|
| CSS parse (postcss) | PASS — 760 rules / 53 at-rules / 2,537 decls; braces balanced 813/813; pure CRLF; trailing newline intact |
| Cascade/selector contracts | **25/25 pass** (24 baseline + 1 new) |
| Vitest | **105/105 pass**, 9 files (no JS touched) |
| Full pytest (authoritative) | **1,751 passed, 0 failed** in 298s — 1,750 baseline + 1 new contract, exactly as predicted |
| Focused Workout Plan visual (`visual.spec.ts -g workout-plan`, no `--update-snapshots`) | **5 passed, 1 failed** — see below |

The authoritative pytest run used the canonical tracked catalog
(`HEAD:data/database.db`, blob `b8c7bd0b`, sha256 `e7665b3e…`, 798,720 bytes), swapped into this
isolated worktree for the duration of the run only.

*Diagnostic note, superseded.* An earlier run in this worktree reported 1,749 passed / 2 failed.
Both failures were `test_catalog_invariants.py` NULL-column assertions
(`primary_muscle_group`, `movement_pattern`), caused by the worktree being seeded from
`e2e/fixtures/database.visual.seed.db`, whose reduced catalog has 454 rows with a blank
`movement_pattern`. They reproduced identically with this packet stashed, so they were never
attributable to the change — and on the canonical catalog they do not occur at all. No catalog
cleanup script was run and no test was weakened; the seed DB was restored byte-for-byte
(sha256 `6477b2ac…`, 765,952 bytes) after the run, with `data/database.db` remaining
`skip-worktree` throughout and the tracked blob untouched.

### Visual known-red comparison

`workout-plan desktop dark` failed at **exactly 1,039 pixels (ratio 0.01)** — the established
WP4.0 signature, byte-for-byte the same pixel count as the i-e / i-f / i-g runs.

Diff-image inspection: red pixels appear **only** on the animated navbar logo (two instances, top
right and bottom right of the tall capture). Every layout, control, filter, and table region is
ghosted-unchanged. No red in any region this packet touched. This is animated-media drift, not
layout or cascade drift.

The other five — `desktop light`, `tablet light`, `tablet dark`, `mobile light`, `mobile dark` —
are byte-identical. Both dark viewports that *do* pass confirm the deletion is computed-value-inert
in dark mode, which is the mode these rules nominally targeted.

No snapshot was updated. `git status -- e2e/__screenshots__` is empty.

### Artifact protection

`git status --short` at the end of the run shows exactly two modified files
(`static/css/pages-workout-plan.css`, `tests/test_css_cascade_contracts.py`).
`static/css/bootstrap.custom.min.css` and `scss/` are untouched (no `build:css` was run).
`data/database.db` remains `skip-worktree` (`git ls-files -v` → `S`).

## Findings recorded, not acted on

1. **Latent dark-mode gap (pre-existing, unchanged by this packet).** The deleted
   `[data-bs-theme="dark"]` block was the *only* dark override for `--superset-bg-1..4`. Because it
   never matched, superset row tints already render with the light `:root` values (alpha `0.08`) in
   dark mode. Deleting the block is inert — it changes nothing — but the gap is real. Adding a
   working `[data-theme='dark']` override would be a deliberate visual change and needs owner
   sign-off; it is not part of this packet.
2. **`body.dark-mode` at `static/css/layout.css:1120`** is dead by the same argument. It lives in a
   shared bundle, so it belongs to WP4.4, not here.
3. **`DARK MODE` section banner** (was line 5469) now heads a region whose first rule is the
   light-mode `.workout-estimate-provenance`. Pre-existing mislabelling (that trailing content was
   appended under the banner); left alone as out-of-scope formatting.

## Evidence contradicting the dead-selector conclusion

None found. Every check pointed the same way: no writer for `data-bs-theme` anywhere in the repo,
no applier for `.dark-mode`, zero mixed rules, and both dark-mode visual snapshots that pass are
unchanged by the deletion.
