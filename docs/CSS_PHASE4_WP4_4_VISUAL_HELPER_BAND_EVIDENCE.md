# Visual determinism layer — the specificity band it occupies

**Change:** `e2e/visual-helpers.ts`, plus one inert test-only attribute in
`templates/progression_plan.html` and its contract. No production CSS or JavaScript, no
snapshot.
**Branch:** `wt/wp4-4-visual-helper-band` off `89523ed`.

---

## 1. The problem

`prepareForScreenshot` injects a dark surface flattener:

```css
html[data-theme='dark'] [data-visual-surface][data-visual-surface] { … }   /* (0,3,1), all !important */
```

It owns a surface only where no product rule out-specifies it. On the Progression goals
table — `templates/progression_plan.html:50`, which carries `data-visual-surface` — the
shared `components.css` Calm Glass table family currently does out-specify it, at
**(1,3,0)**. But that family only reaches `a = 1` because its `:is()` list borrows ID weight
from `#workout[data-page="workout-plan"]`. Any packet that splits a non-ID branch out of
that list drops the branch's arm to **(0,3,0)** — across this rule — and the flattener
silently takes ownership of `border-color` and `border-radius` on `/progression` in dark.

That is a test-harness artifact presenting as a product regression: two committed baselines
move for a change that alters no rendered value in the application. WP4.4-i hit exactly
this, deterministically, on `progression desktop dark` (3,613 px) and `progression tablet
dark` (2,235 px).

**The transferable finding.** De-weighting a shared selector does not only expose
*page-local* rules. It exposes anything occupying the vacated specificity band — including
CSS that exists only inside the test harness. A pre-change inventory that sweeps
`static/css/**` will not find this. Any future packet lowering a shared selector's
specificity must sweep `e2e/**` injected CSS too.

## 2. The correction

Split by **property**, not by element:

| Rule | Selector | Properties |
|---|---|---|
| A | unchanged `(0,3,1)`, every surface | `background`, `background-image`, `box-shadow`, `text-shadow` |
| B | `…:where(:not([data-visual-preserve-border]))` | `border-color`, `border-radius` |

Only the two properties the product family actually owns are withheld, and only from one
element. `background`/`box-shadow` remain with the family's dark rule at (0,4,0) in both
states; `text-shadow` — which the family never declares, and which **inherits** — remains
with this layer in both states, so an element-wholesale exclusion would have been wrong.
`:where()` contributes zero specificity, so rule B stays (0,3,1) for every surface it still
matches.

**Why an attribute and not a class.** `tests/test_visual_selector_contracts.py` forbids
presentation classes in this file — `.table-calm` and `.frame-calm-glass` are on the banned
list — precisely because those are what a CSS refactor churns, which is the situation here.
The `aria-label` was rejected too: it is user-facing copy, and a reword would silently
disable the exclusion with no failing test to explain the moved baselines. So the hook is
`data-visual-preserve-border`: valueless, inert, referenced by nothing in `static/css` or
`static/js`, and pinned by
`test_border_preserve_hook_is_inert_and_used_only_by_the_visual_helper` — which proves it
exists exactly once, that no production file reads it, that the helper keys on it rather
than on a class or the copy, and that rule A was not narrowed. Its red paths cover hook
removal, duplication, a production reference, a broadened exclusion, and a revert to the
aria-label.

That contract needed a correction of its own: counting raw string occurrences made the
"hook was deleted" red path undetectable, because the Jinja comment above the hook *names*
it, so deleting the attribute left the count unchanged. It now strips Jinja comments and
counts rendered usage.

## 3. Proofs, all on unmodified `main`

Harness: [`scripts/css_audit/visual_helper_band_proof.mjs`](../scripts/css_audit/visual_helper_band_proof.mjs).
Both variants are applied to the same page in the same session, so any difference is
attributable to the selector. 11 routes × 2 themes × 3 widths = 66 contexts, each measured
three times (old, old-again as a same-CSS control, new).

| # | Claim | Result |
|---|---|---|
| 1 | Match-set delta is exactly the Progression goals table | **3 elements** — one per `progression\|dark` context; **0** in all 60 other contexts |
| 2 | Zero computed-value/owner differences on all affected surfaces | **0** across every `[data-visual-surface]` element *and all descendants* |
| 2 | Zero pixels on an element-scoped Progression-table capture | **0** differing |
| 3 | No passing screenshot moved beneath the tolerance | see below |
| 4 | Known reds stay within their bands | **35/36 identical; 1 moved by 1px of 2,026,263** |
| — | Same-CSS controls | **0 dirty** |

**Proof 3 detail.** Two contexts showed a full-page byte difference with zero computed
differences. Neither is attributable:

* `user-profile|light|768` — **nondeterministic**: five captures of the *identical* variant
  produced five distinct hashes. It also sits in light theme, where this rule matches zero
  elements and cannot act.
* `session-summary|dark|375` — **deterministic and variant-identical**: eight captures
  alternating old/new produced a single hash.

**Proof 4 detail.** `workout-plan mobile light` reported 2,026,262 rather than 2,026,263 —
a single pixel in 0.0%. It is light theme, where this rule matches zero elements and cannot
act. Re-run nine times on unmodified `main`, that capture yields **both** values
(2,026,263 ×7, 2,026,262 ×2): a two-value band, exactly what M7 describes. The observed
value is inside it.

**Full-suite check.** `visual.spec.ts` + `visual-baseline-thumbnails.spec.ts` on this branch
produce **37 failures whose identities are exactly `main`'s 37**, with 30 passed and 17 not
run — and 35 of the 36 reds carrying pixel counts are identical to `main`, the 36th inside
its measured band per the detail above. Those 37 are
pre-existing Windows baseline drift at ratios 0.28–0.92 on `workout-plan`, `workout-log`,
`weekly-summary`, `session-summary`, `fatigue`, `backup` and one thumbnail; they fail
identically with and without this change. No snapshot was rebaselined.

## 4. A measurement defect this work exposed

The first two proof runs reported ~106 computed differences and were **wrong**. The
harnesses spawned a Flask server and then polled port 5000; when a server from an earlier
run was still listening, the freshly spawned process failed to bind and exited, and the run
measured the *stale* server while reporting the sha of the file at `--root`. The recorded
digest never proved which checkout was rendered.

Both harnesses now refuse to start if the port is held, and assert that the **served**
`components.css` bytes match the checkout under test — the served bytes being what the
browser actually cascades. Every number in §3 comes from a guarded run
(`serving components.css 883e6aa8… from D:\development\Hypertrophy-Toolbox-v3-main`).

## 5. Reproduction

```bash
node scripts/css_audit/visual_helper_band_proof.mjs \
  --root <checkout with unmodified product CSS> \
  --python <python.exe> --seed e2e/fixtures/database.visual.seed.db \
  --work-db artifacts/wp4_4/i/helper-proof.db --out artifacts/wp4_4/i/helper-proof
```
