# WP4.4-k — final integration gate

**Status:** arc closeout. **No production change** — k owns documentation only.
**Arc base:** `46e340e` (WP4.4-a, read-only baseline; it touches no production CSS).
**Arc end:** `47c7687` (WP4.4-j, PR #216).

---

## 1. What the arc did

Ten packets changed production CSS across the seven shared bundles. Per-packet deltas, and
their sum reconciled against a single `git diff` of the whole arc:

| Packet | Commit | Surface | +ins | −del |
|---|---|---|---:|---:|
| b | `3bec677` | `base.css` | 0 | 44 |
| c | `1b13bfc` | `motion.css` | 5 | 3 |
| e | `1346a35` | `layout.css` | 0 | 218 |
| d1 | `59e5b10` | `a11y.css` | 0 | 99 |
| f1 | `1127486` | `navbar.css` | 0 | 6 |
| d2 | `0a912d9` | `a11y.css` | 15 | 1 |
| f2 | `6a5465c` | `navbar.css` | 14 | 17 |
| h | `b2b1cb7` | `components.css` | 0 | 138 |
| i | `5f7b5ac` | `components.css` | 14 | 14 |
| i corrective | `666471e` | *(none — oracles only)* | 0 | 0 |
| j | `47c7687` | `theme-dark.css` | 0 | 47 |
| **Sum** | | | **48** | **587** |

`git diff --numstat 46e340e 47c7687 -- static/css/*.css` reports **+48 / −587**, net
**−539 lines**. The per-packet sum and the whole-arc diff agree exactly, so no packet's
contribution is double-counted or missing.

Packet **g** and the **i corrective** changed no production CSS: g was the components audit,
and the corrective repaired oracles, contracts and evidence only.

## 2. Stylelint — measured from the arc base, not the WP4.1 baseline

| Surface | arc base `46e340e` | now `47c7687` | Δ |
|---|---:|---:|---:|
| `base.css` | 15 | 13 | **−2** |
| `layout.css` | 102 | 84 | **−18** |
| `components.css` | 1,989 | 1,930 | **−59** |
| `a11y.css` | 135 | 128 | **−7** |
| `motion.css` | 16 | 10 | **−6** |
| `navbar.css` | 362 | 356 | **−6** |
| `theme-dark.css` | 264 | 230 | **−34** |
| **Total** | **2,883** | **2,751** | **−132** |

**Every surface fell.** No category rose on any surface except
`no-descending-specificity` on `components.css`, which WP4.4-i raised by 10 under its
bounded, owner-approved exception and attributed line-by-line to the approved split lines.

**This is deliberately not measured against the pinned WP4.1 per-surface baseline, and the
difference matters.** Against WP4.1 the same measurement reads `components.css`
1,787 → 1,930 = **+143**, and an arc total of **+70** — i.e. it would report WP4.4 as a
regression. It is not one. The WP4.1 figures were taken at commit `9ee7638`, before the
WP4.3 packets, and `components.css` had grown to **1,989** by the time WP4.4 began. PLANNING
§"assumptions" states this explicitly: *"Re-measuring the seven surfaces is the first step of
packet P0, not an assumption any later packet may inherit."* Quoting the WP4.1 delta as
WP4.4's contribution would attribute WP4.3-era growth to this arc.

`!important` across the seven surfaces: **−48** (`components.css` 939→919, `theme-dark.css`
148→124, `motion.css` 8→5, `a11y.css` 51→50; `base`, `layout`, `navbar` unchanged).
`theme-dark.css` reads 149→125 by raw `grep`; the declaration counts are 148→124 because one
occurrence is inside a comment.

## 3. The arc changed nothing observable

The arc's central claim is that every deletion was of a declaration that could not win. It is
measured directly: a whole-page computed-value differential between the **arc base** and the
**arc end**, against the same frozen database.

| Result | Value |
|---|---|
| Contexts (11 routes × 2 themes × 3 widths) | 66 |
| Elements compared | 59,886 |
| Computed values compared | **2,275,668** |
| Element drift | **0** |
| Dark-theme differences | **0** |
| Light-theme differences | **0** |

Artifacts: `artifacts/wp4_4/k-arcbase/` (root at `46e340e`) versus `artifacts/wp4_4/j/after/`
(arc end), verdict in `artifacts/wp4_4/k-arcdiff/diff.json`. Both halves' own same-CSS
controls are clean.

**Scope, stated plainly.** The harness measures a 38-longhand paint universe — backgrounds,
borders, box-shadow, colour, opacity, visibility, display, font-weight, text-shadow, outline,
transition, animation, backdrop-filter, fill and stroke. It does **not** measure layout
geometry (padding, margin, width, height, font-size). "Zero" therefore means zero across the
properties CSS deletions of this kind move, not across every property the CSSOM exposes. The
committed pixel matrices in §4 are what cover geometry, and they are unchanged.

## 4. Ledger reconciliation

**Linux (N8 deep gate, `visual_mode=compare`).** Three runs were taken across the closeout:

| Ref | Run | Visual result |
|---|---|---|
| `1019d34` (pre-i) | `30665129779` | 11 failed / 57 passed |
| i + corrective | `30663355864` | 11 failed / 56 passed + 1 flaky |
| j | `30671022691` | 11 failed / 57 passed |

**All three carry the same eleven identities.** Ten are exactly the ten files in
`CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`. The eleventh,
`visual-baseline-thumbnails.spec.ts › plan-desktop-light-advanced`, is **not** in that
ledger — see §5. It reproduces on `1019d34`, which contains no packet from the i–k tail, so
it is inherited. The single accounting difference across the three runs is
`user-profile desktop light`, independently recorded as nondeterministic. Full E2E including
accessibility passed on Linux on every run.

**Windows (`visual.spec.ts`).** 36 failed / 30 passed, with **identical failure identities**
before and after both i and j — 0 introduced, 0 cleared — and
`git status e2e/__screenshots__/` empty on every run. Per **C9**, no snapshot was regenerated
and `--update-snapshots` was never used anywhere in this arc.

## 5. Three proposals — recorded, not applied

Each of these needs owner approval, so k records them and edits nothing.

**P1 — the Linux inherited-reds ledger is incomplete.** It lists 10 reds, all from
`visual.spec.ts`, and its stated scope is `visual.spec.ts-snapshots`. The N8 gate reds an
11th from `visual-baseline-thumbnails.spec.ts`, which the ledger does not cover — while the
ledger's own rules make an unlisted red a rollback trigger. Measurement (§4) shows it is
inherited, so it blocked nothing, but the ledger under-describes reality and every future
packet will hit the same false trigger. Correcting it requires owner approval (V2, R3
condition 6).

**P2 — the N10 `QUALITY_GATE.md` row.** Per **C12**, recorded here as a proposal only;
`QUALITY_GATE.md` is not edited by this arc.

**P3 — `theme-dark.css` is largely inert, and not for the reason its size suggests.** WP4.4-j
measured this directly: re-pointing `background: none !important` — a declaration that
shadows several of j's certified removals — moved **zero** computed values in either theme.
The file wraps nearly every selector in `:where()`, which contributes **zero** specificity, so
its unlayered `!important` declarations lose to any more specific `!important` elsewhere,
including the `:is(#workout…) .table.table-calm` family in `components.css` at (1,2,0). A far
larger reduction than C11 permitted is therefore likely available — on evidence no packet in
this arc gathered. R4 still forbids unlinking the file.

## 6. Status documents reconciled

All three canonical documents were stale at closeout, in different ways:

| Document | Stale claim | Corrected to |
|---|---|---|
| `MASTER_HANDOVER.md` | "N4 IS APPROVED; WP4.4-i IS ACTIVE" | i merged (`5f7b5ac`) + corrective (`666471e`); j merged (`47c7687`); arc closed at k |
| `ACTIVE_DEVELOPMENT.md` | "N4 is approved and WP4.4-i is ACTIVE" | same |
| `REFACTOR_PLAN.md` | "complete through WP4.4-f2 …; WP4.4-g is next" | g, h, i, i-corrective and j all merged |

`REFACTOR_PLAN.md` was furthest behind — it predated g, h, i and j. They are reconciled
**together** in one change, per k's charter, so no reader can consult two of them and get two
different answers.

## 7. Gates

| Gate | Result |
|---|---|
| Full `pytest` | **2296 passed, 1 skipped** |
| Full Chromium suite | **475 passed / 49 failed / 17 skipped** over 541 specs — **every failure is a visual capture; zero functional failures** |
| Arc-wide computed differential | **0 / 2,275,668 values**, both themes |
| Stylelint full re-measure | **2,883 → 2,751 (−132)**, every surface down |
| Windows visual matrix | identities unchanged, no snapshot regenerated |
| Linux N8 deep gate | 11 reds, all reproduced pre-arc-tail |
| Cascade contracts | included in the pytest total |

**The 49 decompose completely**, which is what makes them safe to accept:

| Component | Count | Nature |
|---|---:|---|
| `visual.spec.ts`, also failing in a visual-only run | 36 | the Windows inherited set; identities identical before and after both i and j |
| `visual.spec.ts`, failing **only** in the full suite | 12 | `body-composition` and `user-profile`, all 3 viewports × both themes |
| `visual-baseline-thumbnails.spec.ts` | 1 | `plan-desktop-light-advanced`; inherited, see §5 P1 |

The 12 are pre-existing full-suite state pollution: earlier functional specs mutate the
database before the visual captures run. They are **visual** specs, not functional ones —
`0` specs outside `visual*.spec.ts` fail anywhere in the suite — and **0** specs fail in the
visual-only run but pass in the full run, so the relationship is strictly additive. Artifacts:
`artifacts/wp4_4/k-e2e-full.json` and `artifacts/wp4_4/j/visual-after.json`.

An earlier revision of the WP4.4-i evidence quoted this 49/475/17 split with no committed
artifact. The figures reproduce exactly; they now have one.

## 8. Definition of done

The 235 declarations WP4.4-h withheld remain deferred and untouched (**C8**).
`templates/base.html` is unchanged and `theme-dark.css` remains linked (**R4**). The owner's
local `CLAUDE.md` modification was never staged, stashed, discarded or copied at any point in
the i–k tail.
