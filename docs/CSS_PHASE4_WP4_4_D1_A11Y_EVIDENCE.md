# WP4.4-d1 — `static/css/a11y.css` pure deletion

Packet `d1` of the WP4.4 shared-bundle arc — the pure-deletion half of the split
`d` packet. Re-weighting and `!important` work belongs to `d2` and is **not**
present here.

**Result: 14 rule blocks deleted, −99 lines.** `!important` 51 → 51, custom
properties 17 → 17, `@layer` 0 → 0. Zero declaration-owner changes across 64,961
records.

Base commit: `c0a6096`. Production ownership: `static/css/a11y.css` only.

---

## 1. Static candidate inventory

`a11y.css` at `c0a6096`: 814 lines, 101 rules, 303 declarations, 51
`!important`, 17 custom-property declarations, **0** `@layer` tokens
(WP4.4-a baseline: 813 lines / 51 important / Stylelint 135).

The static pass nominated **14** fully-unreachable rules. Every one of them was
treated as a **hypothesis only** — "absent from templates" is not proof, and the
runtime census below is what decided them.

| Line | Selector | Decls |
|---|---|---|
| 126 | `.scale-control` | 6 |
| 135 | `.scale-control-label` | 4 |
| 142 | `.scale-btn-group` | 7 |
| 244 | `.accessibility-menu` | 14 |
| 261 | `.accessibility-dropdown.open .accessibility-menu` | 3 |
| 267 | `.accessibility-section` | 1 |
| 271 | `.accessibility-section:not(:last-child)` | 2 |
| 276 | `.accessibility-section-title` | 6 |
| 286 | `.scale-labels` | 4 |
| 293 | `.scale-label` | 2 |
| 387 | `.scale-control` | 3 |
| 393 | `.scale-btn-group` | 3 |
| 404 | `.accessibility-menu` | 7 |
| 414 | `.accessibility-dropdown.open .accessibility-menu` | 1 |

Lines 387–414 sit inside `@media (max-width: 991.98px)`.

---

## 2. The generation split

`a11y.css` carried **two generations** of the scale / accessibility UI. This is
the single most important finding in the packet: the nominated selectors are not
scattered dead rules, they are a coherent superseded generation sitting beside a
live one.

| | Legacy — deleted | Current — retained |
|---|---|---|
| scale container | `.scale-control` | `.scale-control-compact` |
| scale buttons | `.scale-btn-group` | `.scale-btn-compact` |
| scale readout | `.scale-labels`, `.scale-label`, `.scale-control-label` | `.scale-indicator` |
| menu | `.accessibility-menu`, `.accessibility-section*` | *(no current equivalent rendered)* |

The live generation is emitted by `templates/base.html:190-202` and carries the
`data-visual-scale-control` hook. `static/js/accessibility.js:82` applies the
scale by setting `data-scale` on `documentElement`.

---

## 3. Oracle validity gate — run before anything was believed

`[data-visual-scale-control]` is a **registered visual blind spot** for packet
`d` (the visual harness neutralizes its `background`, `border-color` and
`color`), so pixel equality cannot certify these deletions. Computed-style and
declaration-owner evidence are the load-bearing oracles.

Before trusting any candidate result, the probe measured the **known-live**
compact generation. If the oracle could not see rules that demonstrably render,
nothing it reported about the candidates would count.

| Known-live control | Natural census | Verdict |
|---|---|---|
| `.scale-control-compact` | census > 0 in **160/160** contexts | LIVE |
| `.scale-btn-compact` | census > 0 in **160/160** (max 2) | LIVE |
| `.scale-indicator` | census > 0 in **160/160** | LIVE |
| `[data-visual-scale-control]` | census > 0 in **160/160** (max 3) | LIVE |

**Gate: PASS.**

### 3a. A fifth control that was *not* live — recorded, not acted on

`.scale-btn[data-scale]` reports census **0 in 160/160**. That means
`accessibility.js:144` and `:202` query an empty set — a second dormant JS path
alongside the dropdown.

The static pass had treated `scale-btn` as *reachable* purely because the
literal string appears in that JS file. That is precisely the "a JavaScript
query alone does not prove reachability" trap. Consequently the bare `.scale-btn`
rules (11 exact-token occurrences) were **never audited as d1 candidates**, and
they are **retained untouched**. The gap is recorded here rather than
generalized from; deleting them would require its own census and its own packet.

---

## 4. Runtime census and classification

State matrix, per capture: **2 themes × 10 widths × 8 `data-scale` levels**
(1–8, set exactly as `accessibility.js:82` sets it) = 160 contexts, plus **print
emulation** ×2 and **reduced-motion** ×2 = **164 total**.

Widths: 375, 576, 768, 769, 820, 991, 992, 1200, 1440, 1920 — chosen to bracket
`a11y.css`'s three `@media` boundaries (`max-width: 991.98px`, `print`,
`max-width: 768px`).

Census uses `querySelectorAll` on the **full selector**, taken **before** any
synthetic is injected.

| Line | Selector | Census | Observable before | Category |
|---|---|---|---|---|
| 126 | `.scale-control` | 0 | 164/164 | **never matches** |
| 135 | `.scale-control-label` | 0 | 164/164 | **never matches** |
| 142 | `.scale-btn-group` | 0 | 164/164 | **never matches** |
| 244 | `.accessibility-menu` | 0 | 164/164 | **never matches** |
| 261 | `.accessibility-dropdown.open .accessibility-menu` | 0 | 162/164 | **never matches** |
| 267 | `.accessibility-section` | 0 | 164/164 | **never matches** |
| 271 | `.accessibility-section:not(:last-child)` | 0 | 164/164 | **never matches** |
| 276 | `.accessibility-section-title` | 0 | 164/164 | **never matches** |
| 286 | `.scale-labels` | 0 | 164/164 | **never matches** |
| 293 | `.scale-label` | 0 | 164/164 | **never matches** |
| 387 | `.scale-control` | 0 | 100/100 | **never matches** |
| 393 | `.scale-btn-group` | 0 | 96/100 | **never matches** |
| 404 | `.accessibility-menu` | 0 | 100/100 | **never matches** |
| 414 | `.accessibility-dropdown.open .accessibility-menu` | 0 | 98/100 | **never matches** |

**No candidate fell into** *matches-but-never-wins*, *interaction-state-only*,
*oracle-blind*, *coupled-family-unsplittable*, or *live*.

The sub-total observability counts (162/164, 96/100, 98/100) are **print and
reduced-motion at 1440px**, where the `max-width: 991.98px` block does not apply
and no distinction is expected. They are not blind spots.

**Family coupling:** the 14 rules form 10 logical families, each a base rule plus
its `@media` override. **Every member of every family was observable**, so all
families were deleted whole. Nothing was split — contrast WP4.4-e, which deferred
its `.tbl-show-*`/`.tbl-hide-*` family for exactly that reason.

---

## 5. Dormant-dropdown analysis

Recorded precisely, and **not generalized**:

- `static/js/accessibility.js:165-166` queries `.accessibility-toggle` and
  `.accessibility-dropdown`, then `:171` toggles `open` on the latter.
- The current templates provide **neither hook**, so both lookups naturally
  return `null` and the toggle never fires.
- Runtime DOM counts, measured: `toggleInDom 0`, `dropdownInDom 0`,
  `menuInDom 0`, `openMenuInDom 0`.
- **Interaction-state attempt performed:** the probe tries to add `open` to a
  `.accessibility-dropdown` and re-count. There was no dropdown to open
  (`afterOpenMenuInDom: null`), so the state could not be reached.

**The deletion does not rest on the dropdown being dormant.** It rests on the
`.accessibility-menu` compound: nothing in `templates/`, `static/js/`, `routes/`
or `utils/` creates `.accessibility-menu` — `accessibility.js` contains no
`createElement`, `innerHTML` or `insertAdjacentHTML` at all. The complete
selector is therefore unreachable regardless of what the dropdown path does.

**Not generalized:** the other `.accessibility-dropdown` rules in `a11y.css`
were **not** candidates and are **not** touched, including the mixed rule in §6.

---

## 6. What was retained

### 6a. The mixed print rule — retained whole

`a11y.css:328`, inside `@media print`:

```css
.scale-control,
.accessibility-dropdown {
    display: none !important;
}
```

`.accessibility-dropdown` was never audited as a `d1` candidate. Trimming
`.scale-control` out would be **re-weighting a rule this packet did not prove**,
which is out of bounds for a pure-deletion packet. Retained whole, `!important`
untouched, and pinned by
`test_mixed_selector_lists_kept_their_dead_branch`.

This retention is directly visible in the post-deletion measurement — see §7b.

### 6b. Everything else

- All **51** `!important` declarations — `d1` removed none, because all 14
  deleted rules contained **zero**. The d1/d2 boundary holds by construction.
- All **17** custom-property declarations (M9).
- The bare `.scale-btn` rules (§3a).
- The full `data-scale` 1–8 ladder and the `*:focus-visible` guarantees (§8).

---

## 7. Oracles and controls

### 7a. Rest-state differential

| Oracle | Records | Differing |
|---|---|---|
| declaration owner (CDP `matchedRules`) | 64,961 | **0** |
| motion | 153,432 | **0** |
| motionReduced | 153,432 | **0** |
| paint | 340,960 | **2** |

The 2 paint records are the same animating Welcome glow in each theme,
`box-shadow` blur differing at the 4th decimal (58.87 vs 58.71) on
`html/body[1]/main[1]/div[0]/div[0]/section[1]/div[1]/div[0]` — one of the eight
ledgered uncertifiable Welcome elements (N8), and independently reproduced by the
run's own same-CSS control on identical CSS. `a11y.css` never styled that
element, and the owner differential is 0 everywhere.

### 7b. Positive candidate-inventory flip — stated by source identity

A zero differential alone would not prove the deletion reached the browser. The
same oracle was re-run after deletion. The result is deliberately **not**
reported as "the rules went blind", because that phrasing cannot be told apart
from "the oracle stopped working". Four things must be kept separate:

1. **deleted rule identity** — the specific source block at a specific location;
2. **selector text**, which may legitimately occur elsewhere in the file;
3. **retained source rule**, which may use that same text;
4. **computed declaration owner** — which rule actually supplies the value.

| | Before | After |
|---|---|---|
| candidate rules distinguishable from their control | **14 / 14** | **2 / 14** |

**Twelve of the fourteen deleted rules were observable before deletion and their
declarations were absent afterwards.** For each, the synthetic element became
indistinguishable from its control — no source block supplies those declarations
any more.

**Two selector *names* still resolve, and only because a retained rule uses the
same text.** `.scale-control` (deleted at former lines 126 and 387) still
distinguishes in **exactly 2 contexts each — print light and print dark**. That
is the retained `@media print` rule of §6a, not a surviving deleted block.

### 7c. Residual-owner proof (CDP `CSS.getMatchedStylesForNode`)

"The selector text still occurs" and "a deleted rule survived" are different
claims, and no substring check separates them. The residual was therefore
attributed to a specific source rule by resolving the actual declaration owner
against a synthetic `.scale-control` element:

| Media | Author rules naming `.scale-control` | Owner |
|---|---|---|
| `screen` | **0** | — every deleted block is gone |
| `print` | **1** | selectors `.scale-control, .accessibility-dropdown`; `@media print`; declaration block at source lines **329–331**; `display: none !important` |

The print owner is the **retained** mixed rule, at the retained location, with
the retained declaration. No deleted source block appears in either media.

Universal selectors (`*, *::before, *::after` — Bootstrap's `box-sizing` reset
and the probe's own transition-suppression tag) match every element and are
excluded from the population: they say nothing about whether a deleted block
survived.

**This is the packet's strongest single result.** A blanket zero would have been
equally consistent with "deleted the right rules" and with "the probe went
blind". A residual that (a) appears only in the contexts where a retained rule
should fire, and (b) resolves by declaration owner to that retained rule's exact
source range, distinguishes those two cases. Together with the known-live
compact-generation controls of §3, it establishes that the oracle remained
capable of observing live rules **after** the deletion, not merely before it.

### 7c. Same-CSS control (M5) and sentinels (M6a)

| Check | Before | After |
|---|---|---|
| same-CSS control | 22/22 pass, **0** differing / 17,048 elements | 22/22 pass, **0** differing |
| sentinel took effect | **4,270 / 4,270** | **4,270 / 4,270** |
| screenshot control | 0 differing pixels | 0 differing pixels |

Dedicated sentinel apply/read/**revert** on the live compact controls, with
transitions suppressed before all three steps:

| Element | before | during | after | took effect | reverted |
|---|---|---|---|---|---|
| `.scale-control-compact` | `rgb(26,26,46)` | `rgb(1,2,3)` | `rgb(26,26,46)` | ✅ | ✅ |
| `.scale-btn-compact` | `rgb(71,85,105)` | `rgb(1,2,3)` | `rgb(71,85,105)` | ✅ | ✅ |
| `.scale-indicator` | `rgb(37,99,235)` | `rgb(1,2,3)` | `rgb(37,99,235)` | ✅ | ✅ |

---

## 8. Accessibility guarantees — verified by computed evidence

Not by screenshot appearance. `[data-visual-scale-control]` is a registered
visual blind spot, so pixels cannot certify this.

| Guarantee | Evidence |
|---|---|
| skip-link on first Tab | first `Tab` focuses `a.nb-skip-link` "Skip to main content" in **both themes** |
| focus **visible** | that element matches `:focus-visible` and computes `outline-style: solid`, `outline-width: 2px` |
| focus vs focus-visible | recorded separately per element (`matches(':focus')` and `matches(':focus-visible')`) |
| keyboard traversal | **12/12** focused elements across a 12-stop Tab walk have a computed visible-focus indicator (outline width > 0 **or** a box-shadow), in both themes |
| `data-scale` ladder | all levels **1–8** still targeted; asserted by contract |
| per-scale focus ladder | `html[data-scale="N"] *:focus-visible` for **N = 1–5**, unchanged |
| print | `@media print` block intact, exercised by emulation |
| reduced motion | exercised via `emulateMedia({ reducedMotion: 'reduce' })` |

The skip-link is `.nb-skip-link` — **navbar-owned, not styled by `a11y.css` at
all**, so `d1` could not affect it. Verified rather than assumed.

---

## 9. Instrumentation defects found and corrected

Recorded because the packet's credibility rests on the controls, not the result.
Two were found in `d1` itself; both would have produced a wrong answer.

| # | Defect | Symptom | Direction of error | Caught by |
|---|---|---|---|---|
| 1 | `@media (max-width: **991.98**px)` — decimal breakpoint | width matcher used `(\d+)px`, so the four media-gated candidates were probed at all 10 widths including ones their block cannot apply to | would have manufactured **false deadness** | spec review before probing |
| 2 | `.accessibility-section:not(:last-child)` | a lone injected child is **always** `:last-child`, so the selector was unsatisfiable and the rule was undetectable for a DOM-construction reason | would have manufactured **false deadness** | spec review before probing |
| 3 | contract over-assertion | asserted a per-scale `*:focus-visible` ladder for `data-scale` 1–8; it only ever covered **1–5**, identically before and after | would have invented a **phantom regression** | pre-deletion comparison against the backup |
| 4 | contract substring weakness | `"*:focus-visible," in css` is satisfied by `html[data-scale="1"] *:focus-visible,`, so deleting the bare global selector left the test **green** | would have left a real guarantee **ungated** | red-path proof |
| 5 | missing source-shape gate | `.scale-control` was absent from the deleted-class list because its text legitimately survives in the retained print rule — so **no contract asserted its two deleted rules stay deleted** | would have left two deletions **ungated** | reviewing the contract against the retained-rule case |
| 6 | `re` character-class bug | `(?<![\w-,])` parses `\w-,` as an invalid range and raises `re.PatternError` — the test *errored* rather than asserting | noisy, not silent | running the new test |
| 7 | CDP range semantics | `style.range` is the **declaration-block** range, not the whole rule; the selector list spans lines 328–329 so the block opens at 1-based 329 (0-based 328). An assertion of 327 failed spuriously | would have **falsely failed** a correct proof | residual-owner run |
| 8 | verdict predicate too broad | the residual-owner check counted *all* author rules, including universal `*, *::before, *::after` (Bootstrap reset + the probe's own injected tag), so a correct measurement reported FAIL | would have **falsely failed** a correct proof | reading the raw rule dump instead of the verdict |
| 9 | comment stripper not newline-preserving | `_strip_comments` replaced every comment character with a space **including newlines**, so line numbers derived from the blanked text shift — it placed the retained rule at line 304 instead of **328** | latent; no current assertion does line arithmetic, but it is the exact hazard `.claude/rules/verification.md` names | chasing defect 7 |

Defects 1–5 would have produced a *wrong packet*. Defects 6–8 would have blocked
a *correct* one. Defect 9 was latent and is now fixed rather than left as a trap.

Two observations worth carrying forward:

- **Defect 4 is the same class as one found during WP4.4-e** — a substring
  assertion masked by duplicate selector text. It recurred here on a different
  surface, which suggests it is a property of the technique rather than a
  one-off. Structural/occurrence-aware assertions are the fix, and both this
  packet's contract and its `.scale-control` source-shape gate now use them.
  *(WP4.4-e's shipped artifacts were not edited by this packet.)*
- **The errors ran in both directions.** Four pushed toward deleting too much,
  three toward rejecting a sound result. That symmetry is the argument that the
  controls — not the outcome — are doing the work.

---

## 10. Gates

| Gate | Result |
|---|---|
| `tests/test_css_wp4_4_a11y_contracts.py` | **16 passed** |
| Red-path proof | **15/15 go red** under their own violation; tree restores to 16 passed |
| Full `pytest tests/` | **2,245 passed, 1 skipped** (387.84s) |
| Shared `test_css_cascade_contracts.py` + visual selector contracts | run, **unedited**, green within the full suite |
| `accessibility`, `dark-mode`, `smoke-navigation`, `summary-pages`, `volume-progress`, `fatigue`, `fatigue-stage4-smokes`, `ui-hardening`, `nav-dropdown` | **127 passed** (3.4m) |
| `visual.spec.ts`, Chromium, 6 variants × 11 routes | **65 passed, 1 failed** — the ledgered red, below |
| Residual-owner proof (CDP) | **PASS** — screen 0 rules, print 1 retained rule at lines 329–331 |
| Stylelint, seven surfaces | **2,857 → 2,851 (−6)**, no rule increased, 0 parse errors |
| `a11y.css` Stylelint | 135 → 129 |

### The one visual failure is the ledgered animated-logo red

`visual.spec.ts:40 › visual baseline: workout-plan › workout-plan desktop dark`
— the same route, theme, viewport and failure shape recorded by WP4.4-b and
WP4.4-e. The WP4.4-a baseline documents it as a genuine snapshot failure whose
band (1,039 / 1,046 px) sits above `maxDiffPixels: 800`, and which must never be
"fixed" by raising the tolerance. No exact pixel count is asserted — it is a
band, not a constant.

`a11y.css` does not style the animated logo, and the declaration-owner
differential is 0 across all 64,961 records, so nothing in this packet can have
moved it. `maxDiffPixels` was not touched and no snapshot was written.

**No non-ledger visual difference appeared**, in any route, theme or viewport.
d1 does not run the Linux deep gate (N8).

### Stylelint attribution

| Rule | Before | After | Δ |
|---|---|---|---|
| `declaration-property-value-disallowed-list` | 1,106 | 1,100 | −6 |
| `declaration-no-important` | 1,260 | 1,260 | **0** |
| `no-descending-specificity` | 244 | 244 | 0 |
| `no-duplicate-selectors` | 25 | 25 | 0 |
| `selector-max-id` / `selector-max-specificity` | 116 / 102 | 116 / 102 | 0 |

`declaration-no-important` holding at 1,260 is independent confirmation that no
re-weighting occurred.

---

## 11. Preservation invariants

| Invariant | Verdict |
|---|---|
| **V1** no visual difference | Rest-state differential 0 outside the ledgered Welcome blur; screenshot controls byte-identical both runs. |
| **V2** no rebaseline | 0 changed paths under `e2e/__screenshots__/`; no `e2e/visual-helpers.ts` change. |
| **V3** no re-weighting | `!important` **51 → 51**; `selector-max-id` +0; `selector-max-specificity` +0. |
| **V4** no duplication increase | `no-duplicate-selectors` 25 → 25; `declaration-block-no-duplicate-properties` 2 → 2. |
| **V5** contribution | −99 lines, −14 rules, −63 declarations. Scope was not widened to improve Stylelint totals. |
| **V6** no conflict | Single writer, single file. |

---

## 12. Surface accounting

| Metric | Before | After | Δ |
|---|---|---|---|
| lines | 814 | 715 | −99 |
| rules | 101 | 87 | −14 |
| declarations | 303 | 240 | −63 |
| `!important` | 51 | 51 | **0** |
| custom-property declarations | 17 | 17 | **0** |
| `@layer` tokens | 0 | 0 | **0** |
| fully-unreachable rules | 14 | 0 | −14 |

---

## 13. Reproducing this

```bash
python artifacts/wp4_4/layout_static.py      # static candidate enumeration
python artifacts/wp4_4/make_specs.py         # derive props + admissible widths

node artifacts/wp4_4/a11y_probe.mjs --out artifacts/wp4_4/a11y_before
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/a11y_rt_before
#   … apply the deletion …
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/a11y_rt_after
node artifacts/wp4_4/a11y_probe.mjs --out artifacts/wp4_4/a11y_after
python artifacts/wp4_4/diff_runs.py artifacts/wp4_4/a11y_rt_before artifacts/wp4_4/a11y_rt_after

python artifacts/wp4_4/redpath_d1.py
node scripts/css_audit/stylelint_surfaces.mjs artifacts/wp4_4/stylelint_after.json
```

Analysis scripts live under the gitignored `artifacts/` tree.
`scripts/css_audit/` stays packet-`a`-owned and was not modified (A11).

---

## 14. Out of scope

- **All re-weighting** — `!important` reduction, specificity changes, generation
  consolidation, trimming live selector lists. That is `d2`.
- The bare `.scale-btn` rules (§3a) — dormant but unaudited; own packet.
- The other `.accessibility-dropdown` rules — not candidates, not generalized to.
- `navbar.css` (`f1`/`f2`), `components.css` (`g`/`h`), `theme-dark.css` (`j`).
