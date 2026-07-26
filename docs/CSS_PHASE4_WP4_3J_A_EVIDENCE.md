# WP4.3j-a — Workout Log dark-mode overpainted `background-color` removal

**Branch:** `wt/wp4-3j-a-workout-log-dark` · **Base:** `origin/main` @ `1bb5feb`
**File:** `static/css/pages-workout-log.css` · **Diff:** 5 deletions, 0 insertions

---

## Scope

Five `background-color` declarations in the trailing "COMPREHENSIVE DARK MODE
TEXT VISIBILITY FIXES" block, covering table columns 1–4 and 15–17:

| Line | Selector | Value | Column |
|---|---|---|---|
| 1445 | `[data-theme='dark'] .workout-log-table td:nth-child(2), :nth-child(3)` | `#2d2d2d` | Routine, Exercise |
| 1451 | `[data-theme='dark'] .workout-log-table td:nth-child(1)` | `#1a1a1a` | Row number |
| 1457 | `[data-theme='dark'] .workout-log-table td:nth-child(4)` | `#2d2d2d` | Plan Sets |
| 1463 | `[data-theme='dark'] .workout-log-table td:nth-child(15)` | `#2d2d2d` | Last Progression |
| 1470 | `[data-theme='dark'] .workout-log-table td:nth-child(16), :nth-child(17)` | `#2d2d2d` | Overload, Actions |

Nothing else in the block was touched. This is the first packet of the WP4.3j
Workout Log sub-arc, which the plan requires be split into multiple WPs
(`REFACTOR_PLAN.md` §WP4.3 item 10).

---

## Why these five, and not the rest of the block

The block is 754 lines and carries 145 of the file's 292 `!important`
declarations, so the obvious hypothesis was that it duplicates the tokenized
metric-lane system at lines 393–645. **That hypothesis is wrong**, and the
correction defines the packet:

- **Columns 5–14 do not collide.** The trailing block sets only `color` there
  (lines 1474, 1487); the lane system sets `background` and `box-shadow`. The
  two are complementary. Matching column numbers without comparing properties
  produces a false positive.
- **The `color` declarations are live winners, not dead.** They set `#e0e0e0` at
  specificity (0,3,1), beating the earlier dark-glass rule's
  `rgba(255, 255, 255, 0.9)` at (0,2,1). Near-identical to the eye, genuinely
  different in value. They stay.
- **Only the `background-color` declarations are suppressed** — and by
  *overpaint*, not by the cascade.

## The overpaint mechanism

`[data-theme='dark'] .workout-log-table td` at line 362 sets:

```css
background: linear-gradient(180deg,
  rgba(26, 32, 44, 0.98) 0%,
  rgba(22, 27, 38, 0.95) 100%) !important;
background-color: transparent !important;
```

The five declarations win the cascade against that rule — (0,3,1) beats (0,2,1),
both `!important`. Their computed `background-color` really is `#2d2d2d`. But the
`background` shorthand on the same elements paints a gradient at **0.98 alpha**
over the top, so the winning colour contributes roughly 2% of the final blend at
the very top edge and nothing below it.

**Method consequence — computed style is the wrong oracle for overpainted
declarations.** The WP4.3i-dead computed-declaration-owner audit answers "is this
declaration the winner," and here the answer is *yes* for all five. It cannot
answer "does the winner reach the screen." Deleting these changes the computed
value from `#2d2d2d` to `transparent` — a guaranteed computed-style diff and a
guaranteed *zero* pixel diff. Only a pixel oracle can distinguish the two.

This extends, rather than replaces, the i-dead rule: a sweep still over-reports,
and a control run is still mandatory. The addition is that the differential must
be taken in the space the claim lives in.

---

## How liveness was established

**Oracle:** the six committed win32 baselines
(`e2e/__screenshots__/win32/visual.spec.ts-snapshots/workout-log-*.png`) —
desktop, tablet, and mobile × light and dark — compared with
`toHaveScreenshot()`.

| Stage | Run | Result |
|---|---|---|
| Control | `visual.spec.ts --grep workout-log`, CSS unmodified | **6 passed**, update-free |
| Test | same spec, five declarations deleted | **6 passed**, update-free |

Both runs used `PW_VISUAL_SEED=1`.

> **Harness trap, recorded because it cost a run.** Visual specs require
> `PW_VISUAL_SEED=1` (`playwright.config.ts:33`). Without it Playwright seeds via
> `prepare_e2e_db.py`, which wipes user state, and the log page renders with
> fewer rows. The first control run failed 6/6 that way — 1440×**900** received
> against a 1440×**1095** baseline, 49% of pixels different. The height mismatch
> is the tell: no `background-color` change can alter page height. A run without
> the flag does not error, it silently compares against the wrong data.

---

## Deltas

| Metric | Before | After | Δ |
|---|---:|---:|---:|
| Lines (`pages-workout-log.css`) | 2,185 | 2,180 | −5 |
| `!important` | 292 | 287 | −5 |
| Hex literals | 98 | 93 | −5 |
| Stylelint — focused | 727 | 717 | **−10** |
| Stylelint — total (`static/css/*.css` + `scss/**/*.scss`) | 5,794 | 5,784 | **−10** |

The total and focused deltas match, confirming the reduction is entirely in the
target file. Duplicate-selector and specificity counts are unchanged — no
selector was altered, only declarations removed from inside existing rules.

---

## Gates

| Gate | Result |
|---|---|
| Focused Workout Log visual (6 win32 variants) | **6 passed**, update-free |
| CSS cascade + visual selector contracts | **30 passed** |
| Functional E2E (`workout-log`, `smoke-navigation`, Chromium) | **33 passed** |
| Full pytest | **1,856 passed / 1 skipped** |

Baseline at branch point `1bb5feb` was also **1,856 passed / 1 skipped** — a
CSS-only change, so the count is expected to be identical rather than to grow.

No visual baseline was updated. No SCSS, Bootstrap output, template, JavaScript,
route, or database file appears in the diff.

---

## Findings recorded, not acted on

1. **The two parallel `@media` ladders.** Seventeen media queries at lines
   691–846 and again at 2082–2190 hit the same breakpoints (1280 / 1366 / 1536 /
   1600 / 1920 / 2560). Candidate for **WP4.3j-b**.
2. **196 `nth-child` rules** make every column rule positional. Any column
   reorder in `workout_log.html` silently repaints the wrong columns. Structural,
   out of scope for a deletion packet.
3. **`.editable-input` at line 1502** (`background-color: #2c3034`) is *not* a
   `td`, so the cell gradient never covers it. Genuinely live — excluded from
   this packet deliberately.
4. **The sixteen `--metric-rgb` / `--metric-dark-rgb` declarations at 1804+** are
   a separate block from the flat-grey column rules and were not analysed here.
5. **This file has zero `[data-bs-theme]` and zero `.dark-mode` selectors.** The
   app sets `[data-theme='dark']` on `documentElement`
   (`static/js/darkMode.js:64`). The WP4.3i-h-style "delete obsolete theme
   families" win does not exist on this page — that debt was never incurred here.
