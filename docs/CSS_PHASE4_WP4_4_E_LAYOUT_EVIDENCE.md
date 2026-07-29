# WP4.4-e — `static/css/layout.css` triage

Packet `e` of the WP4.4 shared-bundle arc. Gate 1 approved 2026-07-27 (rulings
N1–N10); the owner directed sequential execution on 2026-07-29 with `e` first.

**Result: 34 rule blocks deleted, −218 lines. Nine rules deferred.** Zero
declaration-owner changes across 64,961 records; zero motion differences; two
paint differences, both on ledgered-uncertifiable Welcome elements and matched
exactly by the run's own control.

Base commit: `4cd036b`. Production ownership: `static/css/layout.css` only.

---

## 1. What the packet inherited, and what it actually found

The plan carried **one** candidate into this packet: the dead `body.dark-mode`
at `layout.css:1120`, deferred here from WP4.3i-h.

The audit found **42** fully-unreachable rules. `body.dark-mode` is one of them,
and it is the least significant by volume.

| Family | Rules | Disposition |
|---|---|---|
| `.tbl-col-chooser*` (trigger, menu, labels, checkbox, `:hover`, `:focus`, `.active`) | 10 | deleted |
| `.form-container` | 9 | deleted |
| `.input-frame .row` | 6 | deleted |
| `.el-clip` / `.col--ellipsis` / `.col--wrap` / `.col--nowrap` | 3 | deleted |
| `.tbl--loading` + `::after` + `@keyframes tbl-spin` | 3 | deleted |
| `.sr-only` | 1 | deleted |
| `.tbl-toolbar` (standalone) | 1 | deleted |
| `body.dark-mode` | 1 | deleted |
| `.tbl-show-*` / `.tbl-hide-*` | 9 | **deferred** |

---

## 2. `body.dark-mode` — re-proved, not inherited

The plan's label was an assumption from another packet. It was re-measured here.

**The rule is functional.** Adding `dark-mode` to `<body>` changes all seven
`--tbl-*` tokens in **11 of 22** route×theme contexts — the light ones. In the
dark contexts the tokens already hold those values from the live
`[data-theme="dark"]` block immediately above, so the class changes nothing
there. That 11/22 split is the positive control: a rule that changed nothing
when its selector *was* satisfied would mean the oracle could not see it, and no
deletion claim would be trustworthy.

**The selector is never satisfied.** `<body>` never carries the class
(`bodyCarriedClassNaturally: false` in all 22 contexts; full-selector census 0).
`static/js/darkMode.js:64` sets `data-theme` on the root element; nothing
anywhere calls `classList.add('dark-mode')` or hardcodes it in a template. That
premise was already contract-locked repo-wide by WP4.3i-h at
`tests/test_css_cascade_contracts.py:1229` — a file this packet **runs but does
not edit**.

**The sentinel reverted.** `revertedCleanly: true` in all 22 contexts, with
transitions suppressed before apply, read *and* remove (M6a).

**Basis for deletion: unreachability, not the ordinary non-winner rule.** The
block declares only custom properties. The owner's constraint — *do not delete
custom properties under the ordinary non-winner rule* — is respected: this rule
is not deleted because something outranks it, but because nothing can ever match
it. The seven tokens keep their live definition in `[data-theme="dark"]`, now
pinned by `test_dark_theme_table_tokens_have_a_live_definition`.

`dark-mode.spec.ts` was **not** used as evidence of deadness (F4). It is run as
a gate only.

---

## 3. Oracles and controls

### 3a. Rest-state differential — the committed harness

`node scripts/css_audit/runtime_probe.mjs`, 11 routes × 2 themes, before and
after.

| Oracle | Records | Differing |
|---|---|---|
| paint | 340,960 | **2** |
| motion | 153,432 | **0** |
| motionReduced | 153,432 | **0** |
| declaration owner (CDP `matchedRules`) | 64,961 | **0** |

### 3b. The 2 paint differences, and why they are not this packet's

Both are the same element in each theme:
`html/body[1]/main[1]/div[0]/div[0]/section[1]/div[1]/div[0]`, property
`box-shadow`, differing in the **blur radius at the 4th decimal place**
(58.7193px vs 58.8779px). That is an animating glow captured at a slightly
different phase.

Three independent reasons this is not attributable to the deletion:

1. The path appears in the harness's own `uncertifiablePaths` — one of the eight
   uncertifiable Welcome elements the WP4.0 ledger records. N8 forbids
   classifying declarations affecting them from this harness, and none were.
2. The **before**-run's same-CSS control independently reported
   `uncertifiableDifferingRecords: 1` for `welcome--light` and 1 for
   `welcome--dark` — 2 total, the same 2, on identical CSS.
3. `layout.css` never styled that element: the owner differential is 0 across
   all 64,961 records, so no declaration changed hands anywhere.

**Outside the ledgered blind spot the differential is zero.**

### 3c. Same-CSS control (M5) and sentinels (M6a)

| Check | Before | After |
|---|---|---|
| same-CSS control | 22/22 pass, **0** differing / 17,048 elements | 22/22 pass, **0** differing / 17,048 elements |
| sentinel took effect | **4,270 / 4,270** | **4,270 / 4,270** |
| screenshot control | 0 differing pixels, sha256 identical | 0 differing pixels, sha256 identical |

### 3d. Bespoke oracle — census + synthetic injection

The rest-state differential **cannot falsify an unreachable rule**: if no
element carries the class, deleting the rule changes nothing on any rendered
page, so a zero-diff result is consistent with deadness but is not proof of it.
The converging evidence is a census plus synthetic injection.

- **Census**, full-selector `querySelectorAll`, taken before any synthetic is
  injected: **0** for all 42 candidates, across 11 routes × 2 themes × 16
  viewport widths.
- **Synthetic**: build an element satisfying the selector plus a control that
  fails it by exactly one compound, read the rule's **own declared properties**,
  and require a difference. **39 of 42** rules were visible before deletion.
- **After deletion**: 37 of the 39 flipped to invisible. The two that did not
  are proven oracle artifacts — §3e.

Interaction states were **exercised, not inferred**: `:hover` driven by a real
pointer via `page.hover()`, `:focus` by a real `.focus()` call, both with
transitions suppressed first.

### 3e. The two rules that did not flip

Neither is a failed deletion; both are control-construction artifacts, and both
were run down rather than assumed.

**`.tbl-col-chooser-menu input[type="checkbox"]` (`cursor`).** After deletion
the synthetic still read `cursor: default` against a control reading
`cursor: text`. The control drops the distinguishing compound — here the
`type="checkbox"` attribute — so it compared a checkbox against a text input.
That difference is the UA stylesheet's, not `layout.css`'s.

**`.sr-only`.** After deletion the synthetic still resolved
`clip: rect(0,0,0,0); height: 1px; margin: -1px; overflow: hidden;
position: absolute; width: 1px`. **FontAwesome 5.15.4** (`templates/base.html:16`,
CDN) also defines `.sr-only`. The initial grep covered only local
`static/css/*.css` and correctly found `layout.css` as the sole *local*
definition; it did not account for the CDN sheet.

Recorded precisely, because it cuts both ways: `layout.css` loads *after*
FontAwesome, so its copy **was** the winner for `.sr-only` while it existed —
but with census 0 it painted nothing. FontAwesome continues to supply the
utility if anything ever adopts the class. One residual: `layout.css` set
`white-space: nowrap` and FontAwesome does not, so a future consumer would get
slightly different behavior. With census 0 and
`test_deleted_classes_are_still_unreachable` gating future use, that is a
documented residual, not a regression.

### 3f. Instrumentation defects found before deleting anything

Four, each of which pointed the **deletion-favourable** way. They are recorded
because the packet's credibility rests on the controls, not on the result.

| Defect | Symptom | Why it mattered |
|---|---|---|
| Hand-written property lists | 6 families read "paints in 0/22" | `.tbl-toolbar` declares `position/top/z-index/background-color/padding/border-bottom/box-shadow`; the guessed list read `display/align-items/gap/margin-bottom/flex-wrap`. Would have read as strong deadness evidence. |
| Single 1440px viewport | media-gated rules invisible | `.tbl-show-lg`/`.tbl-hide-*` simply do not apply at 1440. |
| Census counted the leaf class | `.input-frame .row` → 96 "live"; `.tbl-col-chooser-menu.active` → 128 | Counted Bootstrap's shared `.row` and `.active`. Fixed to full-selector match, taken before injection so the probe stops counting itself. |
| Control identical to test element | `.tbl-col-chooser-menu label` read BLIND | Stripping "the last compound's classes" strips nothing when the leaf is a bare tag. Fixed to disable the deepest compound that carries classes. |

A fifth was a genuine oracle limit, not a bug: a modifier rule such as
`.tbl-col-chooser-menu.active` restores values its base rule suppressed, so
disabling the whole compound removes the base rule too and the modifier looks
invisible. The control now drops only the final class for multi-class compounds,
which recovered that rule to 32/32 (`opacity, pointer-events, visibility`).

---

## 4. What was retained, and why

### 4a. The deferred breakpoint-helper family — 9 rules

`.tbl-show-sm/md/lg` and `.tbl-hide-sm/md/lg`. Census is 0 and six of the nine
are oracle-visible, so the *unreachability* case is as strong as for the deleted
families. They are deferred anyway because three members — the `@media`
overrides at pre-deletion lines 1818, 1828, 1838 — declare `display: block`,
which is a bare `div`'s initial value. **No control element can distinguish
them**: that is an inherent limit, not a fixable probe defect, so the
post-deletion flip cannot be demonstrated for those three.

Deleting only the six observable members would leave `@media` overrides
targeting classes with no base rule. The family goes as a unit under fresh
evidence or not at all. Under-delivery was preferred to a claim that cannot be
fully evidenced.

Pinned by exact occurrence count in `test_retained_rules_are_still_present`, so
the family cannot be eroded rule by rule.

### 4b. Partially reachable rules — retained whole

Two rules mix a dead branch with a **live** one. Trimming the dead branch out
would re-weight a live rule; that is not deletion and is out of scope for `e`
(it is `d2`/`f2`-shaped work).

- `.tbl-controls, .tbl-toolbar { display: none }` in `@media print` —
  `.tbl-controls` is created at runtime by `static/js/table-responsiveness.js:112`.
  Retained in full, including its `.tbl-toolbar` branch. Print emulation
  confirms both branches still resolve to `display: none`.
- `.input-frame, .action-frame` (9 occurrences) — `.action-frame` is applied
  throughout `templates/user_profile.html`. Retained in full. Only the
  `.input-frame .row` **descendant** rules, whose every branch was unreachable,
  were deleted.

### 4c. Cross-surface note — `.form-container`

`components.css` also defines `.form-container`, and loads after `layout.css`,
so it won at equal specificity for most widths (layout.css's copies were visible
at only 4 of 32 width×theme pairs). This packet deleted only `layout.css`'s
copies; `components.css` is packet `h`'s surface and was not touched. The
deletion basis is unreachability — census 0 — which holds for both copies
independently of which would have won.

---

## 5. Method rules and standing constraints

| Rule | How this packet satisfies it |
|---|---|
| **M5** same-CSS control | 22/22 pass, 0 differing records, both runs. Reported alongside the result. |
| **M6/M6a** sentinels | 4,270/4,270 effective both runs; transitions suppressed before apply, read and remove. |
| **M9** custom properties | No custom property deleted under the non-winner rule. `body.dark-mode`'s seven went on unreachability; their live definitions in `[data-theme="dark"]` are retained and contract-pinned. |
| **N2** `@layer` freeze | `layout.css` had **0** `@layer` tokens at the WP4.4-a baseline and has 0 now, asserted by `test_layout_css_declares_no_cascade_layer`. No rule crossed a layer boundary. |
| **N8** ledgered blind spots | The eight uncertifiable Welcome elements were not classified from this harness. The 2 paint diffs are attributed to them, not to this packet. |
| **F4** | `dark-mode.spec.ts` run as a gate, never used as proof of deadness. |
| **F16** red path | 13/13 contracts proven to fail under their own violation. |
| Interaction states | `:hover` and `:focus` exercised with real pointer/focus, not inferred. |
| `@media` coverage | Every rule probed only at widths its condition admits; 16-width sweep; print emulated. |

---

## 6. Gates

| Gate | Result |
|---|---|
| `tests/test_css_wp4_4_layout_contracts.py` | **13 passed** |
| Red-path proof | **13/13 go red** under their own violation; tree restores to 13 passed |
| Full `pytest tests/` | **2,230 passed, 1 skipped** (405.20s) |
| Shared `test_css_cascade_contracts.py` + visual selector contracts | run, **unedited**, green within the full suite |
| `dark-mode`, `smoke-navigation`, `accessibility`, `volume-progress`, `summary-pages`, `fatigue`, `fatigue-stage4-smokes` | **89 passed** (2.2m) |
| `visual.spec.ts`, Chromium, 6 variants × 11 routes | **65 passed, 1 failed** — the ledgered known red, below |
| Stylelint, seven surfaces | **2,875 → 2,857 (−18)**, no rule increased, 0 parse errors |
| `layout.css` Stylelint | 102 → 84 |

### The one visual failure is the ledgered animated-logo red

`visual.spec.ts:40 › visual baseline: workout-plan › workout-plan desktop dark`.

This is the known red the WP4.4-a baseline records: *"The animated-logo band
(1,039 / 1,046 px) sits above 800 — it is a real snapshot failure of
`workout-plan-desktop-dark`, not a diff the option absorbs. Nobody may 'fix' it
by raising `maxDiffPixels`."* No exact pixel count is asserted here: the diff is
a **band, not a constant**, and the same run has produced 1,039 then 1,046 on
retry.

The same 65-passed / 1-failed shape was recorded by WP4.4-b. `layout.css` does
not style the animated logo, and the owner differential is 0 across all 64,961
records, so nothing in this packet can have moved it.

`maxDiffPixels` was not touched, and no snapshot was written — see V2 below.

### Stylelint attribution

| Rule | Before | After | Δ |
|---|---|---|---|
| `declaration-property-value-disallowed-list` | 1,122 | 1,106 | −16 |
| `no-descending-specificity` | 245 | 244 | −1 |
| `no-duplicate-selectors` | 26 | 25 | −1 |
| `declaration-no-important` | 1,260 | 1,260 | 0 |
| `selector-max-id` | 116 | 116 | 0 |
| `selector-max-specificity` | 102 | 102 | 0 |
| `declaration-block-no-duplicate-properties` | 2 | 2 | 0 |
| `property-no-unknown` | 2 | 2 | 0 |

---

## 7. Preservation invariants

| Invariant | Verdict |
|---|---|
| **V1** no visual difference | Rest-state differential 0 outside the ledgered Welcome blur; screenshot controls byte-identical both runs. |
| **V2** no rebaseline | `git status` shows **0** changed paths under `e2e/__screenshots__/` and no `e2e/visual-helpers.ts` change. |
| **V3** no re-weighting | `!important` **24 → 24**; `selector-max-id` +0; `selector-max-specificity` +0. Pure deletion. |
| **V4** no duplication increase | `no-duplicate-selectors` 26 → 25; `declaration-block-no-duplicate-properties` 2 → 2. |
| **V5** contribution | −218 lines, −34 rules, −128 declarations. Nine rules deliberately left on the table; scope was **not** widened to chase a projection. |
| **V6** no conflict | Single writer, single file. |

---

## 8. Surface accounting

| Metric | Before | After | Δ |
|---|---|---|---|
| lines | 1,842 | 1,624 | −218 |
| rules | 268 | 234 | −34 |
| declarations | 729 | 601 | −128 |
| `!important` | 24 | 24 | 0 |
| custom-property declarations | 46 | 39 | −7 |
| `@layer` tokens | 0 | 0 | 0 |
| fully-unreachable rules | 42 | 9 | −33 |

---

## 9. Reproducing this

```bash
# static candidate enumeration -> artifacts/wp4_4/layout_static.json
python artifacts/wp4_4/layout_static.py
# derive probe specs (properties + admissible widths) from the parsed CSS
python artifacts/wp4_4/make_specs.py

# rest-state differential, committed harness
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/layout_before
#   … apply the deletion …
node scripts/css_audit/runtime_probe.mjs --out artifacts/wp4_4/layout_after
python artifacts/wp4_4/diff_runs.py artifacts/wp4_4/layout_before artifacts/wp4_4/layout_after

# bespoke census + synthetic oracle, before and after
node artifacts/wp4_4/layout_probe2.mjs --out artifacts/wp4_4/probe2_before

# red path
python artifacts/wp4_4/redpath.py

# stylelint, seven surfaces
node scripts/css_audit/stylelint_surfaces.mjs artifacts/wp4_4/stylelint_after.json
```

The analysis scripts live under the gitignored `artifacts/` tree;
`scripts/css_audit/` stays packet-`a`-owned and was not modified (A11).

---

## 10. Out of scope

- `.tbl-show-*` / `.tbl-hide-*` — deferred, §4a.
- `components.css`'s `.form-container` / `.input-frame` — packet `h`'s surface.
- Trimming dead branches out of live selector lists — re-weighting, `d2`/`f2`.
- `theme-dark.css` superset dark tint — packet `j`.
- The `:is()` shared-selector repair — packet `i`, behind the N4 checkpoint.
