# WP4.4-j — `theme-dark.css` legacy-value vs justified-remap triage

**Status:** 25 declarations deleted, all certified dead by intra-file shadowing; 9 rules
removed whole. **Branch:** `wt/wp4-4-j-theme-dark`. **Base:** `666471e` (`main` after the
WP4.4-i corrective, PR #215).

**`static/css/theme-dark.css`:** `1fade8c3…` → `e54818bf…`, **621 → 574 lines**, 81 → 72
top-level rules, 148 → 124 `!important` declarations, **34 custom-property declarations
retained exactly**. The diff is **47 deletions and 0 insertions** — no reformatting.

---

## 1. What the ruling allows

Continuation ruling **C11** makes j **preservation-only**: keep the file linked and
nonempty, retain custom properties by default, retain `.value-changed`, preserve
reduced-motion behaviour, do not add the deferred superset tint, and **delete only
removal-certified declarations**. A no-op j is explicitly valid, and **C10** states that
projections and line counts are not acceptance criteria — so the plan's −150 to −400
projection is not a target this packet is measured against.

It is not a no-op, because one class of deadness certifies cheaply and completely.

---

## 2. The certification, and why it is stronger than a sweep

Most deadness claims need the full **M1** apparatus — a sentinel sweep *and* a rest-state
differential *and* a same-CSS control — because "nothing else declares this" is a claim
about the entire cascade across every route, theme, viewport and interaction state.

One class is decidable without any of that. A declaration **shadowed inside its own file,
under identical selector text**, cannot win anywhere:

- two declarations written with the same selector string necessarily match the same
  elements on every route, in every state, at every viewport — there is no DOM in which one
  applies and the other does not;
- `theme-dark.css` declares no `@layer` (asserted by the certifier and pinned by
  `test_the_file_declares_no_layer`), so within it the cascade reduces to importance, then
  document order;
- therefore a declaration with a later-or-stronger same-longhand declaration under the same
  selector is a non-winner by construction, and deleting it cannot move a computed value.

The certifier is [`j_shadow_certification.mjs`](../scripts/css_audit/j_shadow_certification.mjs).
It is deliberately conservative:

| Guard | Why |
|---|---|
| Custom properties are never candidates | **M9** — a `var()` consumer in any of the other twenty hand-maintained sources keeps them live, and proving otherwise needs a dependency graph, not an ownership sweep |
| A declaration must be shadowed under **every** selector of its rule | shadowed under two of three means deleting it changes rendering under the third |
| Shorthands expand to longhands in both directions | so `background: none` correctly shadows an earlier `background-color`, and a shorthand is certified only when every longhand it sets is shadowed |
| A rule is removed whole only when **all** its declarations are certified | otherwise the rule stays and loses only the certified lines |
| `@media` contents are excluded | a declaration inside a media query applies in a different context and is not comparable with an unconditional one |

## 3. What was removed

**25 declarations in two legacy patterns.**

**Sixteen** sit in the `results-section` / `table-responsive` / `#results-body` cluster,
where later rules restate the same selectors with newer token values and the older
generation was never deleted — e.g. `:where([data-theme="dark"] #results-body)` declares
`background-color` at `:382` and again at `:417`, and `color` at `:383` and again at `:418`.

**Nine** are a `background-color` immediately followed **on the next line** by a `background`
shorthand carrying the same colour, in the Workout Plan input-highlight rules — `:480`/`:481`,
`:490`/`:491`, and so on. The shorthand overwrites the longhand it follows.

**Nine rules were removed whole** because every declaration in them was certified: `138-140`,
`295-298`, `301-304`, `307-309`, `381-384`, `386-389`, `391-393`, `395-398`, `400-402`.

Full record: `artifacts/wp4_4/j/shadow-certification.json`.

## 4. The measurement

A static proof that is wrong about the file is still wrong, so the certification is
confirmed empirically. [`j_theme_differential.mjs`](../scripts/css_audit/j_theme_differential.mjs)
captures every computed value `theme-dark.css` can move, for **every element in the
document** — this file is not confined to one component family, so a subtree scope would be
a guess about where a regression may appear.

**Matrix:** 11 routes × 2 themes × 3 widths = **66 contexts**.

| Result | Value |
|---|---|
| Contexts compared | 66 |
| Elements compared | 59,886 |
| Computed values compared | **2,275,668** |
| Element drift | **0** |
| **Dark-theme differences** | **0** |
| **Light-theme differences** | **0** |

j's rollback criteria are absolute in both directions — any dark difference, and any light
difference *at all*, since a dark-only file that moves light rendering means the
classification was wrong. Both are zero.

Provenance: before half `artifacts/wp4_4/j/before`, root `…-wp4-4-i-is-repair`
(`theme-dark.css` == served == `1fade8c3…`); after half `artifacts/wp4_4/j/after`, root
`…-wp4-4-j` (== served == `e54818bf…`); frozen DB `5bc6d340…` on both halves; verdict in
`artifacts/wp4_4/j/diff/diff.json`. The differ refuses same-root, same-digest, failed-control
and empty comparisons.

### The animation freeze, found by the harness's own control

The first before-capture failed its own M5 same-CSS control on `welcome|dark|1440`. The
WP4.4-a ledger already records why: eight elements in the welcome hero run
`animation-iteration-count: infinite` and **have no rest state**, so two captures a frame
apart legitimately disagree. Pausing them from page script races animations that start after
the call, which is why the failure was intermittent — a re-run of that route alone passed.

The harness now sets the CDP animation playback rate to **0** before anything is read. That
stops the timeline for animations that already exist *and* any that begin later, and it
mutates no CSS, so the cascade under test is unchanged. All 66 contexts then pass their own
control on both halves. The alternative — excluding those elements — would have removed the
welcome hero from the gate entirely, which is a worse trade for a file that styles it.

## 5. Known-live controls — the instrument is not blind

A differential reporting zero is indistinguishable from a broken differential until the same
instrument is shown to report non-zero when the cascade really moves. WP4.4-i learned this
expensively, so j's control is committed
([`j_known_live_mutation.mjs`](../scripts/css_audit/j_known_live_mutation.mjs)) rather than
a hand edit, refuses any input but the expected digest, and pins its own output.

**Control 1 — `--bg-primary` re-pointed to `#ff00ff`.** Moves **12 dark values and 0 light
values**, all on `volume-splitter` tables. The instrument is live, and its light/dark
partition is real rather than a labelling accident — a token under `[data-theme="dark"]`
must move dark values only, and it does.

**Control 2 — the shadowing winner re-pointed.** `background: none !important`, the
declaration whose presence makes several of the deleted ones dead, was re-pointed to the
same sentinel. It moves **0 values in either theme**.

That second result is reported because it is informative, not because it is comfortable: it
says the declaration wins nowhere in the measured matrix either. The mechanism is visible in
the file — `theme-dark.css` wraps nearly every selector in `:where()`, which contributes
**zero** specificity, so its `!important` declarations lose to any more specific `!important`
elsewhere in the app, including the unlayered `:is(#workout…) .table.table-calm` family in
`components.css` at (1,2,0). Much of this bundle is therefore inert for reasons that have
nothing to do with this packet.

**What that does and does not license.** It does not weaken the removals: intra-file
shadowing is sufficient for deadness on its own, independently of whether the shadowing
declaration itself wins. It does mean the *first* control, not the second, is what
establishes live sensitivity. And it is a finding packet **k** should carry forward — a
bundle whose specificity is zeroed by `:where()` is a candidate for far larger reduction
than C11 permits here, on evidence this packet did not gather.

## 6. C11 invariants, each asserted

`tests/test_css_wp4_4_theme_dark_contracts.py` pins all of them:

| Invariant | State |
|---|---|
| File linked from a frozen `base.html` | unchanged; `git diff templates/` is empty |
| File nonempty | 574 lines, 72 rules |
| Custom-property declarations | **34, pinned exactly** — an accidental addition fails too |
| `.value-changed` | retained, 8 occurrences |
| Reduced-motion `@media` | retained, still covering `.value-changed` |
| Deferred superset tint | **not added** — `superset` appears nowhere in the file |
| No `@layer` | asserted, because the shadow argument depends on it |
| Certified removals stay removed | the four shadowing pairs are pinned by their surviving winner |

## 7. Gates

| Gate | Result | Artifact under `artifacts/wp4_4/j/` |
|---|---|---|
| Full `pytest` | **2296 passed, 1 skipped** (2,289 + this packet's 7 contracts) | `pytest-full.txt` |
| `dark-mode.spec.ts` (primary) + `nav-dropdown` + `summary-pages` + `accessibility` | **57 passed** | `e2e-dark.log` |
| Whole-page theme differential | **0 dark / 0 light** over 2,275,668 values | `diff/diff.json` |
| Known-live control (`--bg-primary`) | **12 dark / 0 light** — instrument live, partition real | `knownlive-diff/diff.json` |
| Known-live control (shadow winner) | **0 / 0** — that declaration wins nowhere (§5) | `knownlive-shadow-diff/diff.json` |
| Windows visual matrix | **36 failed / 30 passed, identities exactly `main`'s**; 0 new, 0 cleared, **no snapshot changed** | `visual-after.json` |
| Stylelint (matched 21-source glob) | `theme-dark.css` **264 → 230**; run-wide 5,392 → 5,358 | `stylelint-{before,after}.json` |

**Gate 8 is satisfied outright — no category rose.** Within `theme-dark.css`:
`declaration-no-important` **148 → 124**, `declaration-property-value-disallowed-list`
**91 → 82**, `no-duplicate-selectors` **1 → 0**, `selector-max-id` **24 → 24** (flat, and
untouchable here — the ID-bearing selectors are the Workout Plan input rules, which are live).
Unlike WP4.4-i this packet needs no bounded Stylelint exception. The plan projected
264 → 100–264; the measured 230 is inside that band, at the conservative end, because C11
preservation-only forbids pursuing the larger reduction §5 identifies.

## 8. Reproduction

```bash
# census and certification (dry run prints the set; --apply performs it)
node scripts/css_audit/j_theme_dark_inventory.mjs --out artifacts/wp4_4/j/inventory.json
node scripts/css_audit/j_shadow_certification.mjs --out artifacts/wp4_4/j/shadow-certification.json

# $I is a checkout of the pre-removal tree, $J this one
python scripts/css_audit/i_seed_probe_db.py --out artifacts/wp4_4/j/probe-j.db
node scripts/css_audit/j_theme_differential.mjs --root $I \
  --frozen-db artifacts/wp4_4/j/probe-j.db --out artifacts/wp4_4/j/before
node scripts/css_audit/j_theme_differential.mjs --root $J \
  --frozen-db artifacts/wp4_4/j/probe-j.db --out artifacts/wp4_4/j/after
node scripts/css_audit/j_diff_theme.mjs \
  artifacts/wp4_4/j/before artifacts/wp4_4/j/after --out artifacts/wp4_4/j/diff

# known-live controls (mutate in place, measure, revert)
node scripts/css_audit/j_known_live_mutation.mjs --root $J              # 12 dark / 0 light
node scripts/css_audit/j_known_live_mutation.mjs --root $J --mode shadow-winner   # 0 / 0
git -C $J checkout -- static/css/theme-dark.css
```
