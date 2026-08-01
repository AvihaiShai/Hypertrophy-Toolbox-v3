# Plan Review — WP4.4-0: shared bundle decomposition and cascade audit

*Phase 4 CSS. Planning artifact only. Follows [`docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md).*

**Planning size:** Large / cross-cutting per [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) → **Gate 0 required**, then Gate 1 via [`/council-plan`](../../.claude/commands/council-plan.md).
**Status:** **Gate 0 APPROVED** (owner, subject to rulings R1–R6 below). **Gate 1 APPROVED** (owner, 2026-07-27, subject to rulings N1–N10). **N4 CONTINUATION APPROVED** (owner, 2026-07-31) under [`N4_CONTINUATION_AUTHORITY.md`](N4_CONTINUATION_AUTHORITY.md). Plan v2 remains the executable technical plan; the dated continuation authority supersedes its spent hard-stop instructions and records the bounded post-N4 exceptions.
**Base:** `main` @ `f4f9ee6` (clean).
**Current authorized order:** completed packets through `h` → N4 approved → PR #211 harness prerequisite merged → `i` → `j` → `k`.

---

### ▶ EXECUTION STATUS (2026-07-31) — N4 is discharged; Packet i is active

All ten pre-checkpoint packets are merged. The owner approved the proof-first,
narrow-or-abandon execution of `i` and continuous sequential execution through `j` and
`k`. The binding authority, routine-decision fallbacks and genuine hard stops are in
[`N4_CONTINUATION_AUTHORITY.md`](N4_CONTINUATION_AUTHORITY.md); the live restart state is
in [`EXECUTION_HANDOFF_I_K.md`](EXECUTION_HANDOFF_I_K.md).

| Packet | PR | Squash |
|---|---|---|
| `a` | #187 | `46e340e` |
| `c` | #188 | `1b13bfc` |
| `b` | #192 | `3bec677` |
| `e` | #195 | `1346a35` |
| `d1` | #197 | `59e5b10` |
| `f1` | #199 | `1127486` |
| `d2` | #201 | `0a912d9` |
| `f2` | #205 | `6a5465c` |
| **`g`** | **#207** | **`4b7ca58`** |
| **`g` terminology correction** | **#209** | **`a895cb0`** |
| **`h`** | **#208** | **`b2b1cb7`** |
| **visual harness prerequisite** | **#211** | **`1019d34`** |

```
a ✔ → c ✔ → b ✔ → e ✔ → d1 ✔ → f1 ✔ → d2 ✔ → f2 ✔ → g ✔ → h ✔ → N4 ✔ → helper ✔ → i ▶ → j → k
```

**`h` shipped:** 101 declarations, 138 lines, 20 `!important` declarations, 87 cuts and 11
whole rules deleted from `components.css`. It withheld 235 behind the Packet-a layer-span
pin, 18 `.btn.btn-video`, 2 removal-oracle withdrawals and 6 `.value-changed`. The
**`:is()` family: zero eligible, zero touched.** Region H unchanged.

**Both N4 pre-change inventories are prepared and merged:**
[Inventory A — the complete `:is()` family](../CSS_PHASE4_WP4_4_N4_INVENTORY_A_IS_FAMILY.md) ·
[Inventory B — G3 Workout Log regions A–C](../CSS_PHASE4_WP4_4_N4_INVENTORY_B_REGIONS_ABC.md).
**N4 approval was given on 2026-07-31.** Do not ask for it again. Packet i may narrow to
safe branches or end in the pre-authorized N3 abandonment; either resolution proceeds to
j and k.

**Binding lesson from g + h:** a zero-winner ownership result is **not** a removal verdict;
an inline-`!important` sentinel proves reachability and probe integrity only; **only a
removal oracle grants deletion authority.** g nominated 342 zero-winners and h's removal
oracle proved 35 of them live on removal (336 entered certification: 35 removal-live / 180
`deadCertified` / 121 unmatched; D384–D389 never entered).

**Separate decision resolved for this arc:** do **not** re-pin the Packet-a `@layer
workout` span (`openLine 3539 / closeLine 4104`) and do not touch h's 235 withheld
declarations. Record a separately certified future packet at closeout.

---

### ⚠️ Measured corrections from Packet a (binding — supersede the projections below)

Packet **a** shipped 2026-07-27 (PR #187, squash `46e340e`) and replaced several figures this document projected. Where they differ, **the measurement wins**; the authority is [`docs/CSS_PHASE4_WP4_4_A_BASELINE.json`](../CSS_PHASE4_WP4_4_A_BASELINE.json) and the narrative is [`docs/CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md`](../CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md). These are factual/method corrections; **they do not reopen Gate 1 and do not expand production scope.**

| # | Was | Is | Consequence |
|---|---|---|---|
| C1 | `:is()` family specificity `(1,3,1)`/`(1,3,2)` (G1) | **(1,2,0) – (1,5,3)** — see C1a | Packet **i** may **not** assume a uniform family specificity. 19 `:is(` tokens = **17 rules** (two rules span two selector lines). |
| C1a | C1 as first written: **(1,3,0) – (1,5,3)** | **(1,2,0) – (1,5,3)** | C1 gave the range of per-*rule* maxima. Measured per **selector line**, the floor is `components.css:3335` `:is(…) :where(.table).table-calm` at **(1,2,0)** — `:where()` contributes zero, so that arm is one class lighter than its `:3336` twin at (1,3,0). It is the family's lowest-weight arm and therefore the one a page-local `(0,2,x)` rule comes closest to reaching. Source: [Inventory A §2.1](../CSS_PHASE4_WP4_4_N4_INVENTORY_A_IS_FAMILY.md). |
| C9 | The reduced-motion `:is()` rule is at `components.css:4433`, inside `@media` opened at `:4417` | **`:4413`, inside `@media` opened at `:4397`; the rule opens at `:4398`** | WP4.4-h deleted 138 lines, **20 of them before pristine 4417**, so every identity in that block shifts by −20. Cites of "`:4433`" now name a line that does not exist. The twelve four-branch rules at `:3335`–`:3411` are before h's legal window (4105–5345) and did **not** move. |
| C2 | Visual matrix = **60** tests (10 pages) | **66** tests (11 pages), per platform | Every downstream "full 60-test matrix" gate now means **66**. `.claude/rules/testing.md:87` corrected 48 → 66. |
| C3 | `error.html` is "painted 100% by shared bundles" as a rendered route (F5/PR#2) | **Not reachable by a 404 at all.** `app.py:194` returns a hard-coded inline document with **no stylesheet link**; `error.html` renders only when a route handler catches an exception | No packet may treat a bad URL as exercising `error.html`. It has no pixel coverage and is not a shared-bundle canary. |
| C4 | seven-surface Stylelint **2,681**; `components.css` **1,787** | **2,883**; `components.css` **1,989** | V5 line-contribution projections leaning on the old figure are optimistic. |
| C5 | V4 thresholds `no-duplicate-selectors` **86**, `declaration-block-no-duplicate-properties` **8** | **26** and **2** on the seven surfaces (86/8 were *global* WP4.1 figures) | V3/V4 gate against the a-baseline. The old thresholds were unreachable. |
| C6 | — | **11 inherited Linux `desktop` reds**, ledgered in [`docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json`](../CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json) — 10 in `visual.spec.ts` and 1 in `visual-baseline-thumbnails.spec.ts` (`plan-desktop-light-advanced`) | **N8** packets (h, i, j, k) reconcile against that ledger. These reds are **pre-existing and must not be rebaselined**. C6 read **10** until schema v2; the eleventh was measured inherited at `1019d34` but had no slot in the single-`snapshotDir` v1 shape, so it read as a rollback trigger. See P1 in [`CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md`](../CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md) §5. |
| C7 | — | **8 Welcome elements are uncertifiable** by the rest-state harness (infinite animations) | **No downstream packet may classify any declaration affecting those 8 elements as dead using this harness.** Paths are in the ledger file and in `artifacts/wp4_4/runtime/summary.json`. |
| C8 | M6 | **M6a added** — suppress transitions before applying, reading and removing a sentinel | Binding on every remaining packet. See §2b. |

### Terminology (binding for this document)

| Term | Meaning | Count |
|---|---|---|
| **Selector branch** | One argument inside the shared `components.css` `:is(…)` selector list | **4** — `#workout[data-page="workout-plan"]`, `.workout-log-page`, `.summary-frame.frame-calm-glass`, `.progression-plan-container` |
| **Affected route** | An application route whose rendered DOM matches at least one branch | **5** — Workout Plan, Workout Log, Weekly Summary, Session Summary, Progression |

Four branches produce five routes because the single branch `.summary-frame.frame-calm-glass` matches on **both** Weekly Summary and Session Summary. **Never write "four contexts" as a synonym for "five routes."** Every gate that says "all affected routes" means all **five**.

**Corrected by the council (architecture-reviewer A10, test-strategist F8) — the binding triple is `six specs / five routes / four selector branches`:**

- The shared family is **twelve four-branch rules** (`components.css:3335`, `:3351`, `:3360`, `:3368`, `:3377`, `:3381`, `:3386`, `:3390`, `:3395`, `:3400`, `:3405`, `:3409` — note the rule opened at `:3335` has a second selector line at `:3336`, which is a **first-class member of the enumeration**, not a footnote: at (1,3,0) versus `:3335`'s (1,2,0) the two arms carry *different* weights) **plus one *three-branch* rule at `:4433` → post-`h` `:4413`** (rule opens `:4398`), which omits `.summary-frame.frame-calm-glass` and sits inside `@media (prefers-reduced-motion: reduce)` opened at `:4417` **→ post-`h` `:4397`** (see C9). Reduced-motion transition suppression is therefore **not** currently applied to Weekly/Session Summary tables. That is a **pre-existing behavioural asymmetry, not a typo to fix in passing**; normalizing it would be a visible/behavioural change on two routes under reduced motion and requires separate owner approval.
- `components.css` contains **19** `:is(` occurrences in total (verified by grep). "The complete `:is()` family" means the thirteen rules above; the remainder — including the second ID-exporting construct `input.input-calm-inset:is(#weight, #sets, …)` at `:3635`, `:3655`, `:3678`, `:3749`, `:3750`, which is already nested under `#workout[data-page="workout-plan"]` and therefore not a cross-route leak — is enumerated and classified by WP4.4-a so R3 condition 1 has a defensible closure argument.
- **Five affected routes are covered by six spec files**, not five: `workout-plan.spec.ts`, `exercise-interactions.spec.ts`, `superset-edge-cases.spec.ts`, `workout-log.spec.ts`, `summary-pages.spec.ts` (Weekly **and** Session), `progression.spec.ts`.

**Rendered-route denominator — corrected (test-strategist F5, product-risk #2).** The app renders **11 routes**, not 10. `templates/fatigue.html` contains **no `.css` link and no `page_css` block at all** (verified), and `templates/error.html:5` has an **empty** `page_css` block. Both are therefore painted *entirely* by the shared bundles this arc rewrites — the highest shared-bundle exposure in the app — and neither appears in `e2e/visual.spec.ts` or in `ROUTE_BUNDLES`. The Plan v1 phrase "all 10 routes" was inherited from the ten *route bundles*, not from the app's route set. Every "all routes" gate in Plan v2 means **11 rendered routes plus the error page**.

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> Act as the repository’s read-only `manager` agent and follow the canonical workflow in:
>
> - CLAUDE.md
> - docs/MASTER_HANDOVER.md
> - docs/REFACTOR_PLAN.md
> - docs/ai_workflow/QUALITY_GATE.md
> - docs/ai_workflow/AUTONOMY.md
> - docs/ai_workflow/PARALLEL_WORKFLOW.md
> - docs/ai_workflow/WORKSTREAM_OWNERSHIP.md
> - .claude/commands/council-plan.md
>
> Workstream: Phase 4 CSS, new planning/audit packet “WP4.4-0 — shared bundle decomposition and cascade audit.”
>
> This session is authorized for planning and read-only investigation only. Do not edit production CSS, templates, JavaScript, tests, snapshots, MASTER_HANDOVER.md, or other implementation files. The product-manager may create and edit only:
>
> docs/css_phase4_wp4_4/PLANNING.md
>
> Goal:
> Produce an evidence-grounded, council-reviewed Plan v2 that decomposes WP4.4 into small packets with safe ownership, dependencies, test gates, and merge order. Do not implement any packet. Stop at owner Gate 0 and Gate 1 as required.
>
> Required scope:
>
> 1. Audit and plan these surfaces separately:
>    - static/css/base.css
>    - static/css/layout.css
>    - static/css/components.css
>    - static/css/a11y.css
>    - static/css/motion.css
>    - static/css/navbar.css
>    - static/css/theme-dark.css
>
> 2. Ground the plan in the current WP4.3j findings:
>    - The shared components.css `:is()` selector exports ID-level specificity.
>    - WP4.3j-c-dead and WP4.3j-d discharged the deletion prerequisite.
>    - Workout Log regions A–C remain and must be re-measured if shared selector ownership changes.
>    - The superset dark-tint gap and dead `body.dark-mode` rule in layout.css belong to WP4.4.
>    - Do not reopen the ten frozen Workout Plan interaction-state declarations.
>    - Do not modify the locked WP4.3i-c Page Header contract.
>    - Do not redispatch WP4.3i-jm or WP4.3i-o.
>
> 3. Partition the work into named packets. For every packet provide:
>    - exact production paths owned;
>    - exact test/evidence paths owned;
>    - selectors or declaration families in scope;
>    - explicit exclusions;
>    - dependency and merge order;
>    - whether it can run concurrently with another packet;
>    - expected CSS/stylelint/line-count movement;
>    - visual, functional and cascade-contract gates;
>    - known-red handling;
>    - rollback criteria;
>    - whether a token value or visible rendering may change.
>
> 4. Explicitly classify:
>    - packets safe for Codex and Opus to implement concurrently in separate worktrees;
>    - packets that only permit parallel read-only audits;
>    - packets that must land sequentially because of cascade/load-order coupling;
>    - shared files that only one workstream may edit;
>    - the final integration gate after rebasing onto all preceding packets.
>
> 5. The plan must preserve:
>    - no unexplained visual differences;
>    - no snapshot rebaseline unless the owner separately approves an intentional visual change;
>    - no increased maximum specificity or unexplained `!important` count;
>    - monotonic reduction in duplicate declarations/selectors;
>    - the Phase 4 target of 30% total hand-maintained CSS reduction, while treating cascade correctness as more important than line count.
>
> Multi-agent instructions:
>
> - Use the repository’s `/council-plan` workflow.
> - Have the product-manager draft the planning artifact.
> - Run architecture-reviewer, test-strategist, and product-risk-reviewer in parallel against the same artifact.
> - Record all agent IDs and resume the same product-manager for the response matrix and Plan v2.
> - Agents may investigate and review in parallel, but do not allow multiple agents to edit the same artifact simultaneously.
> - Do not dispatch senior-developer implementation.
> - Do not allow multiple production writers.
> - Do not create, remove, merge, or move worktrees from inside the manager session.
>
> First complete the requirements section and stop for my Gate 0 approval if required. After approval, run the council, produce Plan v2, and stop for Gate 1 approval. Report the artifact path, agent IDs, proposed packet DAG, safe parallel pairings, and unresolved owner decisions.

---

**Problem**

Phase 4 has cleaned CSS **page by page** (WP4.3a–WP4.3j-d). Every page packet has now hit the same wall: the page bundles are not the owners of what they paint. The WP4.3j-c audit proved it quantitatively — of 322 audited Workout Log declarations, **227 never win anywhere**, because a shared `components.css` selector uses `:is(#workout[data-page="workout-plan"], .workout-log-page, .summary-frame.frame-calm-glass, .progression-plan-container)` (`static/css/components.css:3335-3413`, plus one more at `:4433`), and `:is()` takes the specificity of its *most specific* argument. The ID-bearing branch exports `(1,3,1)`/`(1,3,2)` + `!important` across **four selector branches reaching five affected routes**, even when the branch that actually matches is a bare class. No page-local ID-free rule can reach it regardless of `!important`.

The consequence is that the remaining Phase 4 debt is **concentrated in the seven shared bundles**, and it cannot be cleaned page-locally:

| Surface | Lines | Lines containing `!important` |
|---|---:|---:|
| `static/css/base.css` | 123 | 0 |
| `static/css/layout.css` | 1,841 | 24 |
| `static/css/components.css` | 5,345 | 939 |
| `static/css/a11y.css` | 813 | 51 |
| `static/css/motion.css` | 71 | 8 |
| `static/css/navbar.css` | 1,542 | 93 |
| `static/css/theme-dark.css` | 621 | 149 |
| **Total (7 surfaces)** | **10,356** | **1,264** |

*(Line counts verified by the manager on `main` @ `f4f9ee6`; `!important` figures are `rg --count` **line** counts measured during this brief, not occurrence counts.)*

⚠️ **These `!important` figures are NON-AUTHORITATIVE (test-strategist F15).** They count *lines containing* `!important`; invariant V3 gates on Stylelint's `declaration-no-important`, an *occurrence* count. A single line bearing two `!important` declarations moves one metric and not the other, so a packet could satisfy V3 while the 1,264 headline is unchanged, or vice versa. **WP4.4-a normalizes all `!important` reporting to Stylelint occurrence counts** and records both units; no packet may quote the line counts as a gate threshold.

*(Load-order diagram scope, product-risk #11: the diagram below models the **cascade-relevant** links only. It deliberately omits the Google Fonts stylesheet at `templates/base.html:13` and the jsdelivr Bootstrap `onerror` fallback at `:15` — neither changes cascade order. They matter for measurement, not ownership: font availability changes text metrics and a failed FontAwesome load collapses icon-only affordances, so a differential taken online and re-taken offline will disagree for reasons unrelated to CSS. WP4.4-a pins and records network state, including whether the jsdelivr fallback fired, in every evidence doc.)*

What is missing is not a cleanup — it is **a decomposition that is safe to execute**. Any edit to a shared bundle changes tie-breaks on up to 10 pages at once, and the load order makes that non-obvious:

```
tokens.css → bootstrap.custom.min.css → (FontAwesome CDN) →
base.css → layout.css → components.css → navbar.css → a11y.css →
{% block page_css %}   ← the 10 page bundles land HERE →
motion.css → theme-dark.css
```
*(Verified against `templates/base.html:14-28`.)*

Three consequences follow and must drive the plan: page bundles load **after** every shared bundle but **before** `motion.css` and `theme-dark.css`; `theme-dark.css` is last and therefore wins every same-specificity, same-importance tie in the app; and splitting or reordering any shared bundle silently re-decides those ties across all 10 pages simultaneously.

A fourth consequence is stronger than load order and was verified during this brief: **`@layer` is in play.** `static/css/tokens.css:2` declares `@layer workout, navbar, workout-dropdowns, welcome;`, and layered blocks exist at `navbar.css:6` (`@layer navbar`, closed before the comment at `navbar.css:908` that says override rules "MUST be outside @layer"), `components.css:3539` (`@layer workout`), `pages-workout-plan.css:468` and `:718`, and `pages-welcome.css:6`. **Corrected by architecture-reviewer A6 — the two directions are opposite, and Plan v1's flat sentence was wrong for `!important`:**

- For **normal** declarations, layered rules lose to every unlayered rule at any specificity. So roughly 900 of `navbar.css`'s 1,542 lines sit inside `@layer navbar` and lose to every unlayered normal declaration.
- For **`!important`** declarations the order **inverts, and unlayered important is the weakest.** A layered `!important` beats every unlayered `!important`; among layers the **earlier-declared** layer wins. Because `tokens.css:2` orders `workout, navbar, workout-dropdowns, welcome`, an `!important` inside `@layer navbar` beats every unlayered `!important` in `components.css`, `a11y.css` and `theme-dark.css`, and loses only to `@layer workout`. `navbar.css` carries **93 `!important` lines inside that layer**.

**A packet-f implementer who read Plan v1's flat sentence as licence to nominate the layered generation as dead would have deleted live winners.** The shared `:is()` table rules at `components.css:3335-3413` are **unlayered** (they precede `@layer workout` at `:3539`). Moving a rule into or out of a layer flips precedence in a direction that specificity arithmetic alone will not predict — which is why G11/N2 freeze layer membership for the whole arc.

Two findings are also parked awaiting WP4.4 and have no home until this plan exists: the superset dark-tint gap (`--superset-bg-1..4` have no live dark override) and the dead `body.dark-mode` rule at `static/css/layout.css:1120`.

**Denominator, stated precisely** (verified against [`CSS_PHASE4_WP4_1_EVIDENCE.md`](../CSS_PHASE4_WP4_1_EVIDENCE.md), [`CSS_PHASE4_WP4_1_TOKEN_INVENTORY.md`](../CSS_PHASE4_WP4_1_TOKEN_INVENTORY.md) and [`CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json`](../CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json), not restated from the ruling). The canonical WP4.1 inventory covers **21 source files = 18 hand-maintained runtime CSS bundles + 3 hand-maintained SCSS sources** (`scss/custom-bootstrap.scss`, `scss/_fatigue.scss`, `scss/pages/_workout_plan_volume_panel.scss` — confirmed by glob). `static/css/bootstrap.custom.min.css` and its `.map` are **generated** and are explicit `exclusions` in the baseline JSON, so they are outside the denominator. Total inventoried size: **30,768 lines**. SCSS is hand-maintained and therefore **stays inside the Phase 4 all-source denominator**, but is **outside WP4.4 implementation scope** — WP4.4 edits no `.scss` file. WP4.4's addressable surface is the **10,356 lines** in the seven named bundles, i.e. **33.7% of the denominator**. Even total elimination of WP4.4's surface would only just reach the Phase-4 30% target, which is precisely why ruling R5 makes 30% a **Phase-4** target that WP4.4 reports a contribution and a shortfall against rather than a quota WP4.4 must hit alone.

WP4.4-0 therefore produces **a plan, not a change**: an evidence-grounded, council-reviewed packet decomposition with ownership, dependencies, merge order, concurrency classification, gates, and rollback criteria — such that each downstream packet is small enough to be individually provable and no two packets can race on the same shared file.

---

**Acceptance criteria**

*Deliverable criteria — checkable by reading the finished artifact.*

1. Given the seven named shared surfaces, when Plan v2 is read, then each surface is addressed by **at least one named packet**, and **no two implementation packets own the same production path**. The ownership model distinguishes two claim types: an **implementation packet** claims a production path exclusively (single-writer), whereas a **read-only prerequisite audit** claims only its own distinct evidence path and **never** claims the production file it reads. Two audits may therefore read the same production file concurrently; two implementation packets may never write it concurrently.
2. Given any packet in Plan v2, when its row is read, then it states **all eleven** required attributes from §3 of the raw request: exact production paths owned; exact test/evidence paths owned; selectors or declaration families in scope; explicit exclusions; dependency and merge order; concurrency eligibility; expected line/Stylelint/`!important` movement; visual + functional + cascade-contract gates; known-red handling; rollback criteria; and whether a token value or visible rendering may change (`yes`/`no`, with `yes` requiring a named owner approval).
3. Given the full packet set, when the dependency graph is drawn, then it is a **DAG with no cycles**, every edge carries a one-line reason, and the reason is one of: cascade/load-order coupling, shared-file exclusivity, evidence dependency, or contract dependency.
4. Given the DAG, when concurrency is classified, then every packet is assigned exactly one of four labels — **(a)** safe for concurrent implementation in a separate worktree, **(b)** parallel read-only audit only, **(c)** must land sequentially due to cascade/load-order coupling, **(d)** single-writer shared file — and every pair proposed as concurrent is proven disjoint at the **file** level, not merely at the selector level.
5. Given all preceding packets have merged, when the final integration gate is described, then Plan v2 names a rebase-onto-all-predecessors step plus the exact gate command set to run at that point (full pytest, contracts, required Chromium set, both-theme visual matrix).
6. Given the WP4.3j findings, when Plan v2 is read, then it explicitly records: the `:is()` ID-specificity export, its **four selector branches** and the **five affected routes** they reach; that WP4.3j-c-dead and WP4.3j-d discharged the deletion prerequisite; and that **Workout Log regions A, B and C must be re-measured before and after** any packet that changes shared selector ownership.
7. Given the Phase 4 measurement mechanism, when Plan v2 states expected movement, then each figure is expressed against a named baseline artifact (`docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json` for Stylelint, `docs/CSS_PHASE4_WP4_0_EVIDENCE.md` for the visual ledger) rather than as an unanchored number.
8. Given the 18-bundle cap in `.claude/rules/frontend.md` and `tests/test_css_cascade_contracts.py`, when any packet proposes splitting, merging, or removing a bundle, then Plan v2 states the exact contract-test consequence and names the owner decision required, because `test_runtime_bundle_cap_and_route_ownership_are_unchanged` asserts exactly 8 global links.

*Preservation invariants — every downstream packet must carry these; Plan v2 must encode them as per-packet gates.*

9. Given any WP4.4 packet, when its visual gate runs, then the result is **zero visual differences beyond the WP4.0 ledger's known reds**, and any diff outside that ledger is a **rollback trigger**, not a finding to explain after the fact. The animated-logo red is treated as drift in a band (observed 1,039 px and 1,046 px in the same run), never as an exact-pixel invariant.
10. Given any WP4.4 packet, when a committed screenshot baseline would change, then the packet **stops and requests separate owner approval**; no packet may run Playwright with `--update-snapshots` under its own authority.
11. Given any WP4.4 packet, when Stylelint is re-measured against the pinned baseline, then **maximum selector specificity does not increase**, `!important` count does not increase without a written per-declaration explanation, and no Stylelint category increases.
12. Given the packet sequence, when duplicate-selector and duplicate-declaration counts are compared packet over packet, then they **decrease monotonically** after the measure baseline; a packet that raises either is rejected or must carry an explicit owner-approved exception.
13. Given the Phase 4 target of 30% hand-maintained CSS reduction, when a packet's line-count movement conflicts with cascade correctness, then **cascade correctness wins** and Plan v2 records the shortfall rather than deleting to hit the number; a packet whose only justification is line count is not a valid packet.
14. Given each deadness claim, when it is proven, then the method obeys the accumulated Phase 4 method rules: a sentinel sweep alone over-reports deadness and must be paired with a rest-state differential **and** a same-CSS control; overpaint-suppressed declarations require a pixel-space differential; the full-page pixel oracle is unusable on animated-navbar routes (scope captures to the element under test); and any specificity model must handle `:is()`/`:where()`/`:not()` and must not split selector lists on a naive comma.
15. Given this session, when Gate 0 is reached, then **no file other than `docs/css_phase4_wp4_4/PLANNING.md` has been created or modified**, and no packet has been implemented.

---

**Calculation surface**

**`none`.**

This is a CSS-only planning packet. No Python calculation module is read for behavior, called, or changed. Specifically untouched: `utils/effective_sets.py` (`calculate_effective_sets`, `CountingMode`, `ContributionMode`), `utils/weekly_summary.py`, `utils/session_summary.py`, the progression logic under `utils/`, and the fatigue modules. No route, response shape, DB schema, or `data/database.db` byte is in scope. No worked before/after example is applicable because no numeric output exists in this packet's surface.

The only "values" in scope are CSS token values and computed style values. Those are covered by the visual and cascade-contract gates (AC9–AC11), not by calculation migration notes. Should any downstream WP4.4 packet ever propose touching a Python calculation module, that packet is **out of scope for this plan** and requires its own Gate 0.

*Recorded so `product-risk-reviewer` can confirm the `none` claim at council time rather than infer it.*

---

**In scope**

- A written audit + decomposition covering all seven named surfaces, each treated as a **separate** surface with its own packet(s): `base.css`, `layout.css`, `components.css`, `a11y.css`, `motion.css`, `navbar.css`, `theme-dark.css`.
- Read-only investigation of the current cascade: selector inventories, specificity distributions, `!important` families, duplicate families, load-order tie-breaks, and cross-page reach of shared selectors.
- Named packets with the eleven attributes of AC2, plus a dependency DAG, merge order, and the final integration gate.
- Concurrency classification for two implementers (Codex, Opus) in separate worktrees, including which shared files are strictly single-writer.
- Explicit recording (not repair) of the `components.css` `:is()` ID-specificity export and the five pages it reaches.
- Planning treatment — including which packet owns them and under what approval — of the two parked findings: the superset dark-tint gap and the dead `body.dark-mode` at `static/css/layout.css:1120`.
- Per-packet gate definitions that extend the existing mechanism in `tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py`, naming which contract each packet adds or tightens.
- Naming the evidence-doc path each downstream packet will write (`docs/CSS_PHASE4_WP4_4_*_EVIDENCE.md` pattern), so no two packets collide on an evidence file.

**Out of scope / non-goals**

- **Implementing any packet.** No production CSS, template, JS, test, snapshot, or evidence file is written in this session. The only artifact is this planning document.
- The **ten frozen Workout Plan interaction-state declarations** from WP4.3i-dead. They stay present; the i-dead contract asserts it. Not re-opened, not re-measured, not deleted.
- The **locked WP4.3i-c Page Header contract** (section 829, 15/15 live). Not modified, not re-derived.
- **Re-dispatching WP4.3i-jm or WP4.3i-o.** Both were attempted and deliberately not committed. Their premises collapsed under measurement; they are closed.
- The un-started Workout Plan **raw-literal → token extraction and `!important` weighting review** (~218 hex literals, ~488 `!important` lines). Redesign-sized, multi-packet, separately owner-gated, and not folded into WP4.4.
- `static/css/bootstrap.custom.min.css` (a build artifact) and everything under `scss/**`. Neither is hand-maintained CSS; neither counts toward the 30% target.
- The **10 page bundles** (`pages-*.css`), except in the narrow case where a shared-selector repair *provably* transfers ownership to or from a page bundle — and then only as a named, measured, separately approved packet with before/after re-measurement of the affected page.
- Any change to `data/database.db`, `data/catalog.seed.db`, or any DB sidecar.
- Worktree creation, removal, merging, or moving — from this session or the manager session.
- Any change to `docs/MASTER_HANDOVER.md`, `docs/REFACTOR_PLAN.md`, `CLAUDE.md`, `.claude/**`, or any existing evidence doc during this planning session.
- Dispatching `senior-developer`, or allowing more than one production writer at any time.

---

**Assumptions made**

*Assumptions A1–A6 were escalated at Gate 0 and are now **RESOLVED by owner ruling** — see "Gate 0 owner rulings" below. They are retained here for audit trail with their resolution stamped. Mapping nit corrected per architecture-reviewer A15: the mapping is **6 assumptions → 5 rulings** (A1→R1, A2→R2, A3→R3, A4→R4, A5→R5, **A6→R4**). R6 answers open question 6 (evidence-doc naming), which was never an assumption.*

- ~~⚠️~~ **A1 `tokens.css` scope.** → **RESOLVED, R1: OUT.** Findings that point at token definitions are recorded and deferred; no `tokens.css` implementation packet exists.
- ~~⚠️~~ **A2 superset dark-tint gap.** `--superset-bg-1..4` are defined at `static/css/pages-workout-plan.css:3424-3427` and consumed at `:3553-3568` with no live dark override (verified). → **RESOLVED, R2: DEFER.** Recorded only. `pages-workout-plan.css` is **not** pulled into this arc, no visible change is authorized, and no rebaseline is planned.
- ~~⚠️~~ **A3 `:is()` repair authorization.** → **RESOLVED, R3: REPAIR MAY BE PLANNED.** See the exact scope limits under R3 — this authorizes *planning a measured repair packet*, and explicitly does **not** authorize implementing it, accepting visual drift, or accepting uncontrolled resurrection of suppressed rules.
- ~~⚠️~~ **A4 `theme-dark.css` end-state.** → **RESOLVED, R4.** It may be reduced to justified token remaps but may **not** be unlinked in this arc, because `templates/base.html` is frozen. **The REFACTOR_PLAN §WP4.4 end-state "or is removed after proof" is therefore explicitly out of reach for this arc** and must not be pursued or implied by any packet.
- ~~⚠️~~ **A5 reduction denominator.** → **RESOLVED, R5: ALL hand-maintained source CSS** per the canonical WP4.1 inventory (21 sources / 30,768 lines, SCSS included in the denominator, generated Bootstrap excluded). 30% is a **Phase-4** target; WP4.4 reports contribution and shortfall.
- ~~⚠️~~ **A6 `base.html` link-order editing.** → **RESOLVED, R4: OUT.** Global link order and the 8-global/10-route bundle contract are frozen for all of WP4.4.
- ⚠️ **Assumed measurement environment:** Windows/Chromium locally, with the pinned Stylelint `16.11.0` + `postcss-scss` `4.0.9` dev-dependency pins and the committed WP4.1 baseline JSON as the comparison anchor. Assumed the two catalog pytest known-reds and the WP4.0 visual known-reds remain the only tolerated reds. Not re-verified in this session (read-only, no test runs).
- ⚠️ **Assumed two implementers, sequential merges.** The request names Codex and Opus. Assumed each gets its own worktree created *outside* the manager session, that only one may hold a given shared file at a time, and that merges land one at a time to `main` with a rebase before each. No concurrency claim in Plan v2 will rest on selector-level disjointness alone (AC4).
- ⚠️ **Assumed `navbar.css`'s "three live generations"** (per REFACTOR_PLAN §WP4.4) still exist as described. Not re-verified declaration-by-declaration in this session; Plan v1 will make the audit that establishes it an explicit first packet rather than assume the count.
- ⚠️ **Assumed the dead `body.dark-mode` at `layout.css:1120` is genuinely dead.** The selector exists at that line (verified), but its deadness is inherited from a prior packet's finding and has not been re-proven under the current method rules (AC14). Plan v1 requires re-proof before deletion, not deletion on the strength of the parked note.
- ⚠️ **Assumed the WP4.1 per-surface Stylelint figures still hold for the seven shared bundles.** The baseline JSON records `base.css` 15, `layout.css` 102, `components.css` 1,787, `a11y.css` 135, `motion.css` 16, `navbar.css` 362, `theme-dark.css` 264 — **2,681 of 7,202 total warnings** at commit `9ee7638`. Every WP4.3 packet edited page bundles only, so these *should* be unchanged, but Stylelint was **not** re-run in this read-only session and the current global total has moved to 5,490 (WP4.3j-d). Re-measuring the seven surfaces is the **first step of packet P0**, not an assumption any later packet may inherit.
- ⚠️ **Assumed layer membership boundaries are as the opening/closing markers suggest.** `@layer` declarations were verified by grep (`tokens.css:2`, `navbar.css:6`, `components.css:3539`, `pages-workout-plan.css:468`/`:718`, `pages-welcome.css:6`), but the exact closing brace of each layer block was **not** parsed. The claim "~900 of `navbar.css` is layered" is an inference from the `navbar.css:908` comment. P0 must establish exact layer spans before any packet relies on them.

---

**Open questions for the user — ALL ANSWERED at Gate 0**

| # | Question | Ruling | Consequence for the plan |
|---|---|---|---|
| 1 | Is `static/css/tokens.css` in scope? | **OUT** | Findings recorded and deferred; **no `tokens.css` implementation packet**. `tokens.css` is read-only for every packet, including `@layer` inspection at `tokens.css:2`. |
| 2 | Is closing the superset dark-tint gap authorized as a visible change? | **DEFER** | Recorded only. `pages-workout-plan.css` stays out of this arc. No visible change, no rebaseline planned. |
| 3 | May a packet repair the `components.css` `:is()` arm? | **REPAIR — planning only** | A narrowly scoped, **sequential, single-writer** repair packet may be *planned* under the eight conditions in R3. Not implemented in this session. |
| 4 | Is `templates/base.html` link-order/removal editing in scope? | **OUT** | Global link order and the 8-global/10-route bundle contract are frozen for all of WP4.4. `theme-dark.css` may shrink to justified token remaps but may **not** be unlinked. |
| 5 | Does the 30% target apply to all hand-maintained CSS or the seven surfaces? | **ALL source CSS** | Denominator is the canonical WP4.1 inventory (21 sources / 30,768 lines, SCSS included). 30% is a **Phase-4** target; WP4.4 reports contribution + shortfall and is not required to hit it alone. |
| 6 | Evidence-doc naming convention? | **Flat existing convention** | All downstream evidence docs are `docs/CSS_PHASE4_WP4_4_*_EVIDENCE.md`. |

**No open questions remain blocking at Gate 0.** New owner decisions surfaced *by Plan v1* are listed separately under "New owner decisions surfaced by Plan v1" at the end of Plan v1; they are Gate-1 decisions, not Gate-0 reopenings.

---

### Gate 0 owner rulings (binding)

**R1 — `tokens.css`: OUT.** Record relevant findings and defer them. Do not create a `tokens.css` implementation packet.

**R2 — Superset dark-tint gap: DEFER.** Record it. Do not pull `pages-workout-plan.css` into this arc, do not authorize a visible change, do not plan a snapshot rebaseline.

**R3 — `components.css` `:is()` arm: REPAIR MAY BE PLANNED.** Owner statement, verbatim: *"This authorizes planning the repair, not implementing it and not accepting visual drift or uncontrolled resurrection of suppressed rules."* The repair packet MUST:

1. begin with evidence establishing the **complete** affected selector/declaration family;
2. measure **Workout Log regions A–C before and after**;
3. cover **all five affected routes** — Workout Plan, Workout Log, Weekly Summary, Session Summary, Progression;
4. **inventory any page-local rules that would become winners BEFORE** changing ownership;
5. preserve zero unexplained visual differences, the maximum-specificity and `!important` invariants, and all cascade contracts;
6. use **ROLLBACK — not rebaseline** — if ownership changes cause unexplained rendering differences;
7. remain **sequential and single-writer** for `components.css`;
8. name any required page-bundle edit as **separately owner-gated**, never as silent production-scope expansion.

> **Reading note (required by the owner).** R3 is authorization to *plan a measured repair*, gated by conditions 1–8. It is **not** owner acceptance of resurrected rules, and **not** owner acceptance of visual drift. If the pre-change inventory (condition 4) shows that suppressed page-local rules would become winners, that is a finding to be resolved or escalated **before** the ownership change — not an outcome the owner has pre-approved.

**R4 — `templates/base.html`: OUT.** Global link order and the existing bundle contract are frozen throughout WP4.4. `theme-dark.css` MAY be reduced to justified token remaps; it may **NOT** be unlinked in this arc. The REFACTOR_PLAN §WP4.4 end-state *"or is removed after proof"* is **explicitly out of reach for this arc**.

**R5 — Reduction denominator: ALL hand-maintained source CSS**, per the canonical WP4.1 inventory. 30% is the overall **Phase-4** target. WP4.4 reports its own contribution and any remaining shortfall; WP4.4 is **not** required to force a 30% reduction by itself.

**R6 — Evidence-doc convention:** flat `docs/CSS_PHASE4_WP4_4_*_EVIDENCE.md`.

---

### Section 0 sign-off — GATE 0

- [x] User confirms the acceptance criteria match intent.
- [x] User reviewed the assumptions and corrected or accepted each one — A1–A6 resolved by R1–R6; the remaining ⚠️ items are unverifiable read-only and are each assigned to the first step of the packet that depends on them.
- [x] Blocking questions are answered — see the ruling table above.

**GATE 0 APPROVED.** Plan v1 follows.

---

## Plan v1

**Goal**: Decompose WP4.4 into eleven individually provable packets — one read-only baseline, one read-only `components.css` audit, seven file-exclusive surface packets, one owner-gated shared-selector repair, and one final integration gate — such that the seven shared bundles can be cleaned without a single unexplained visual difference and without two writers ever holding the same production path.

**Nothing in this session implements anything.** No packet is executed, no worktree is created, moved, merged or removed, no `senior-developer` is dispatched, and the only file written is this artifact.

### Scope

- **In**: audit + decomposition of `base.css`, `layout.css`, `components.css`, `a11y.css`, `motion.css`, `navbar.css`, `theme-dark.css`; the packet DAG, merge order, concurrency classification, per-packet gates, rollback criteria, and the final integration gate; the planned (not implemented) `:is()` repair packet under R3.
- **Out**: everything under Section 0 "Out of scope / non-goals", plus — per Gate 0 rulings — `tokens.css` implementation (R1), the superset dark-tint gap (R2), `templates/base.html` and any load-order or bundle-count change (R4), `scss/**` implementation (in the Phase-4 denominator, out of WP4.4 scope), and unlinking `theme-dark.css` (R4).

### §2 Grounding obligations — standing constraints every packet inherits

Every packet's evidence doc must restate and satisfy these. They are not prose; they are entry conditions.

| # | Constraint | Source |
|---|---|---|
| G1 | The shared `components.css` `:is()` selector exports **ID-level specificity** — `(1,3,1)`/`(1,3,2)` + `!important` — from its ID-bearing branch to **all four branches**, reaching **five affected routes**. `static/css/components.css:3335-3413`, plus `:4433`. **Corrected by C1/C1a/C9:** the per-selector-line range is **(1,2,0)–(1,5,3)**, the family spans `:3335`–`:3411` (unmoved by `h`), and the reduced-motion rule is now `:4413` (rule opens `:4398`). The claim itself — every branch inherits `a = 1` — is unchanged. Full enumeration: [Inventory A](../CSS_PHASE4_WP4_4_N4_INVENTORY_A_IS_FAMILY.md). | `CSS_PHASE4_WP4_3J_C_AUDIT_EVIDENCE.md` |
| G2 | The **deletion prerequisite is discharged**: WP4.3j-c-dead deleted the 37 dead rules (regions D–G) and WP4.3j-d removed the four dead hover-paint declarations, so a shared-selector repair can no longer resurrect them. | REFACTOR_PLAN §WP4.4; `..._J_C_DEAD_...`, `..._J_D_HOVER_PAINT_...` |
| G3 | **Workout Log regions A, B and C remain page-local and ID-free.** Any packet that changes shared selector ownership MUST re-measure A–C **before and after**. This is a hard gate on packet **WP4.4-i**, not advice. | REFACTOR_PLAN §WP4.4 bullet 1 |
| G4 | The **superset dark-tint gap** (`--superset-bg-1..4`, defined `pages-workout-plan.css:3424-3427`, consumed `:3553-3568`, no live dark override) belongs to WP4.4 but is **DEFERRED unacted** by R2. Record it; change nothing. | REFACTOR_PLAN next-state 6; R2 |
| G5 | The dead **`body.dark-mode` at `static/css/layout.css:1120`** belongs to WP4.4. It must be **re-proven dead under the current method rules before deletion** (⚠️ its deadness is inherited, not re-verified). Owned by **WP4.4-e**. | REFACTOR_PLAN next-state 6; Section 0 assumption |
| G6 | **Do not reopen the ten frozen Workout Plan interaction-state declarations.** They stay present; the WP4.3i-dead contract asserts it. | REFACTOR_PLAN next-state 1 |
| G7 | **Do not modify the locked WP4.3i-c Page Header contract** (section 829, 15/15 live). | REFACTOR_PLAN next-state 2 |
| G8 | **Do not re-dispatch WP4.3i-jm or WP4.3i-o.** Both were attempted and deliberately not committed. | REFACTOR_PLAN next-state 7 |
| G9 | The Region H metric-lane block is locked byte-for-byte by `REGION_H_SHA256` in `tests/test_css_cascade_contracts.py:43`. No packet may change it. | that test |
| G10 | ⚠️ **`@layer` is live and precedence-inverting.** `tokens.css:2` declares `@layer workout, navbar, workout-dropdowns, welcome;`; layered blocks exist at `navbar.css:6`, `components.css:3539`, `pages-workout-plan.css:468`/`:718`, `pages-welcome.css:6`. Layered normal declarations lose to all unlayered ones; for `!important` the order inverts. **No packet may change a rule's layer membership** (see New owner decision N2). Exact layer spans are established by WP4.4-a. | verified by grep this session |

### §2b Method rules — expressed as gate obligations

Each is a **pass/fail obligation on the packet's evidence**, not a stylistic note.

| # | Obligation | Origin |
|---|---|---|
| M1 | A sentinel sweep alone **over-reports deadness**. Every deadness claim must be backed by a sentinel sweep **AND** a rest-state differential **AND** a same-CSS control. A packet presenting only a sweep fails its gate. | WP4.3i-dead (24 → 14) |
| M2 | Declarations suppressed by **overpaint** rather than by the cascade must be differenced **in pixel space** — a computed-owner audit will certify them live while zero pixels change. | WP4.3j-a |
| M3 | The **full-page pixel oracle is unusable on animated-navbar routes** (same-CSS control drifts at 10/14 widths inside `y ∈ [18,40]`). Scope every capture to the element under test. | WP4.3j-b-dead |
| M4 | A specificity model that mishandles `:is()`/`:where()`/`:not()`/`:has()` or **naively comma-splits** a selector list will report an owner contradicting the computed value. The model must be unit-checked against hand-computed specificities before use. | WP4.3j-b-dead, j-c |
| M5 | **Every deadness sweep carries a known-live control.** A control that fails invalidates the sweep. | WP4.3j-c-dead |
| M6 | **A probe that changes nothing proves nothing.** Four oracle defects each produced a confident false deadness verdict — notably `var()`-bearing shorthands being invisible to longhand CSSOM queries. Sentinel-took-effect must be asserted per record. | WP4.3j-c |
| M7 | The animated-logo known red is a **band**, not an invariant: 1,039 px and 1,046 px were observed in the same run. No gate may assert an exact pixel count. | WP4.3i-filter-btn |
| M8 | **Delete only proven non-winners.** No packet may delete a declaration that wins anywhere in any measured context. (This is also what makes concurrent packets safe — see §4c.) | derived; see §4c |

### §5 Preservation invariants — per-packet pass/fail gates

Applied to **every** packet. A packet that cannot satisfy all six is rejected, not excepted.

| # | Invariant | Pass condition | Failure action |
|---|---|---|---|
| V1 | No unexplained visual differences | Visual matrix reproduces **only** the WP4.0 ledger known reds, treated as bands per M7 | **Rollback** the packet |
| V2 | No snapshot rebaseline | No `--update-snapshots` run under packet authority; any needed rebaseline **stops and requests separate owner approval** | Stop; escalate |
| V3 | No increased maximum specificity; no unexplained `!important` | Pinned Stylelint: `selector-max-specificity` and `selector-max-id` do not rise; `declaration-no-important` does not rise without a written per-declaration explanation | Reject the diff |
| V4 | Monotonic duplicate reduction | `no-duplicate-selectors` (86 at baseline) and `declaration-block-no-duplicate-properties` (8 at baseline) do not increase, and decrease across the arc | Reject the diff |
| V5 | 30% is a **Phase-4** target | Each packet reports its line contribution; WP4.4-k reports cumulative contribution **and remaining shortfall** against the 30,768-line denominator | Report, do not force |
| V6 | Cascade correctness outranks line count | Where V1–V4 conflict with V5, V1–V4 win and the shortfall is recorded | Record shortfall |

### Packets

**Ownership model.** An **implementation packet** claims its production path exclusively — single-writer, no concurrent writer, ever. A **read-only audit packet** claims only its evidence path and never claims the production file it reads; two audits may read the same file concurrently.

⚠️ **All "expected movement" figures below are projections from the WP4.1 per-file baseline and are unverified.** Confirming or correcting each is the first step of the packet that owns it. No later packet may inherit a projection as fact.

---

#### WP4.4-a — Shared-surface measurement baseline and cascade harness
*Read-only audit. Owns no production path.*

| Attribute | Value |
|---|---|
| **Production paths owned** | **none** — read-only. Reads all of `static/css/**` including `tokens.css` (R1: read-only), `templates/base.html` (read-only, frozen by R4) |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md`; harness scripts under gitignored `artifacts/wp4_4/` |
| **Selectors / declaration families in scope** | none modified. Inventories: exact `@layer` spans in all six layered files; unlayered vs layered line counts per surface; the complete `:is()` family (`components.css:3335-3413`, `:4433`); per-surface Stylelint re-measurement against the pinned baseline |
| **Explicit exclusions** | no production edit of any kind; no `tokens.css` packet (R1); no deletion nomination — this packet measures, it does not classify dead |
| **Dependency / merge order** | **first**. Blocks b, c, d, e, f, g |
| **Concurrency** | **(b) parallel read-only audit** — may run alongside any other read-only work; owns no production file |
| **Expected movement** | production lines **0**; Stylelint **0**; establishes the true per-surface counts (projected: base 15, layout 102, components 1,787, a11y 135, motion 16, navbar 362, theme-dark 264 = **2,681 of 7,202**) |
| **Gates** | `pytest tests/test_css_cascade_contracts.py tests/test_visual_selector_contracts.py`; harness self-checks — same-CSS pixel control **0 diff** on all captured contexts, resolution self-check **0 mismatches**, specificity model unit-checked per M4, sentinel-took-effect per M6 |
| **Known-red handling** | records the current WP4.0 ledger reds and confirms the animated-logo **band** per M7; ⚠️ re-confirms whether catalog pytest known-reds are present on the canonical `HEAD:data/database.db` |
| **Rollback criteria** | n/a (no production diff). If any harness self-check fails, the harness is fixed before any downstream packet may cite it — a failing control invalidates every claim built on it (M5) |
| **Token value / visible rendering may change?** | **no** |

---

#### WP4.4-b — `base.css` triage
| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/base.css` (exclusive) |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_B_BASE_EVIDENCE.md`; `tests/test_css_wp4_4_base_contracts.py` (new, per-packet — see N1) |
| **Selectors / declaration families in scope** | element defaults, app background, baseline typography — the whole 123-line file; 0 `!important` lines makes it the cleanest surface |
| **Explicit exclusions** | every other CSS file; `tokens.css` values it consumes (R1) |
| **Dependency / merge order** | after **a** |
| **Concurrency** | **(a) safe concurrent implementation** — file-disjoint from c, d, e, f |
| **Expected movement** | ⚠️ projected **−0 to −10** lines of 123; Stylelint 15 → 5–15; `!important` unchanged at 0 |
| **Gates** | `pytest tests/test_css_cascade_contracts.py tests/test_visual_selector_contracts.py tests/test_css_wp4_4_base_contracts.py`; Chromium `visual.spec.ts` (all 6 variants), `dark-mode.spec.ts`, `smoke-navigation.spec.ts`; Stylelint delta vs pinned baseline. `base.css` is global → visual matrix covers all 10 routes |
| **Known-red handling** | WP4.0 ledger only; animated-logo as a band (M7) |
| **Rollback criteria** | any visual diff outside the ledger; any Stylelint category increase; any contract red |
| **Token value / visible rendering may change?** | **no** |

---

#### WP4.4-c — `motion.css` triage
| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/motion.css` (exclusive) |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_C_MOTION_EVIDENCE.md`; `tests/test_css_wp4_4_motion_contracts.py` |
| **Selectors / declaration families in scope** | transitions, skeleton states, `prefers-reduced-motion` handling; the 8 `!important` lines; the single `@media` block |
| **Explicit exclusions** | all other files. **Special hazard:** `motion.css` is one of only two shared bundles loading **after** the page bundles — its rules beat same-specificity page rules. Deadness proofs must therefore be taken with page bundles present on all 10 routes, not on one |
| **Dependency / merge order** | after **a** |
| **Concurrency** | **(a) safe concurrent implementation** — file-disjoint from b, d, e, f |
| **Expected movement** | ⚠️ projected **−0 to −15** lines of 71; Stylelint 16 → 5–16 |
| **Gates** | as WP4.4-b, plus `accessibility.spec.ts` (reduced-motion paths) and a forced `prefers-reduced-motion: reduce` capture. Per M1, animation states require the same-CSS control **and** rest-state differential — this file is the highest-risk surface for animation-driven false differences |
| **Known-red handling** | WP4.0 ledger; the animated-logo red is *motion-adjacent* — if it moves outside the observed band, that is a **finding**, and the packet stops rather than rebaselines |
| **Rollback criteria** | as WP4.4-b, plus any change to reduced-motion behavior |
| **Token value / visible rendering may change?** | **no** |

---

#### WP4.4-d — `a11y.css` triage
| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/a11y.css` (exclusive) |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_D_A11Y_EVIDENCE.md`; `tests/test_css_wp4_4_a11y_contracts.py` |
| **Selectors / declaration families in scope** | UI scale system (`data-scale`), focus states, Firefox fallbacks; 51 `!important` lines; 4 `@media` blocks |
| **Explicit exclusions** | all other files. **Do not** weaken any focus-visible or skip-link rule to reduce `!important` count — accessibility affordances are behavior, and V3's "unexplained" carve-out does not license removing a live a11y guarantee |
| **Dependency / merge order** | after **a** |
| **Concurrency** | **(a) safe concurrent implementation** — file-disjoint from b, c, e, f |
| **Expected movement** | ⚠️ projected **−50 to −150** lines of 813; Stylelint 135 → 60–135 |
| **Gates** | as WP4.4-b, plus `accessibility.spec.ts` (**required**), plus captures at every `data-scale` level the file targets and a keyboard-focus traversal. `a11y.css` loads last of the pre-page shared bundles, so it beats layout/components/navbar at equal specificity — proofs must reflect that |
| **Known-red handling** | WP4.0 ledger; ⚠️ the historical accessibility flake (CI fast-follow A7) is recorded — if it appears, re-run in isolation and record, do not suppress |
| **Rollback criteria** | as WP4.4-b, plus **any** measurable change in focus visibility or scale behavior |
| **Token value / visible rendering may change?** | **no** |

---

#### WP4.4-e — `layout.css` triage, including the dead `body.dark-mode`
| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/layout.css` (exclusive) |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md`; `tests/test_css_wp4_4_layout_contracts.py` |
| **Selectors / declaration families in scope** | containers, shell spacing, responsive tables, grid utilities; 36 `@media` blocks; 24 `!important` lines; **and the dead `body.dark-mode` rule at `layout.css:1120`** (G5) |
| **Explicit exclusions** | all other files. The `body.dark-mode` deletion is **conditional on re-proof** (G5) — if the re-proof under M1/M5/M6 shows it live, it stays and the finding is corrected in the evidence doc |
| **Dependency / merge order** | after **a** |
| **Concurrency** | **(a) safe concurrent implementation** — file-disjoint from b, c, d, f |
| **Expected movement** | ⚠️ projected **−100 to −300** lines of 1,841; Stylelint 102 → 40–102; `@media` count may fall if whole ladders prove inert (cf. WP4.3j-b-dead) |
| **Gates** | as WP4.4-b, plus a **breakpoint sweep** across the widths the 36 `@media` blocks target (WP4.3j-b-dead used 14 widths), plus `dark-mode.spec.ts` for the `body.dark-mode` claim, plus per-page specs for any route whose shell measurably depends on a touched family |
| **Known-red handling** | WP4.0 ledger; M3 applies — scope captures to the element under test, never full-page on animated-navbar routes |
| **Rollback criteria** | as WP4.4-b, plus any breakpoint-probe divergence |
| **Token value / visible rendering may change?** | **no** |

---

#### WP4.4-f — `navbar.css` three-generation triage
| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/navbar.css` (exclusive) |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_F_NAVBAR_EVIDENCE.md`; `tests/test_css_wp4_4_navbar_contracts.py` |
| **Selectors / declaration families in scope** | ⚠️ the "three live generations" named in REFACTOR_PLAN §WP4.4 — **establishing that there are exactly three, rule by rule, is step 1 of this packet, not an assumption**. Includes the layered block from `navbar.css:6` and the deliberately-unlayered override tail from `navbar.css:908`; 93 `!important` lines; 16 `@media` blocks |
| **Explicit exclusions** | all other files. **No change to layer membership** (G10 / N2): the `navbar.css:908` comment states the override rules "MUST be outside @layer", and moving rules across that boundary inverts precedence for normal vs `!important` declarations in opposite directions |
| **Dependency / merge order** | after **a**. ⚠️ Highest risk of the concurrent set — the navbar is the one component present on all 10 routes *and* the host of the animated-logo known red |
| **Concurrency** | **(a) safe concurrent implementation** — file-disjoint from b, c, d, e |
| **Expected movement** | ⚠️ projected **−150 to −400** lines of 1,542; Stylelint 362 → 150–362 (second-largest single-file debt after `components.css`) |
| **Gates** | as WP4.4-b, plus `nav-dropdown.spec.ts` (**required** — no longer a known red since 2026-06-11, so failures block), `dark-mode.spec.ts`, `smoke-navigation.spec.ts`, `accessibility.spec.ts`; captures at collapsed and expanded navbar states and both themes |
| **Known-red handling** | the animated-logo red lives **in this component**. Per M7 it is a band (1,039 / 1,046 observed). Movement **within** the band is tolerated and recorded; movement outside it stops the packet |
| **Rollback criteria** | as WP4.4-b, plus any dropdown/keyboard-navigation behavior change, plus any logo diff outside the band |
| **Token value / visible rendering may change?** | **no** |

---

#### WP4.4-g — `components.css` cascade audit
*Read-only audit. Owns no production path.*

| Attribute | Value |
|---|---|
| **Production paths owned** | **none** — read-only. Reads `static/css/components.css` and all 10 page bundles |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_G_COMPONENTS_AUDIT_EVIDENCE.md` |
| **Selectors / declaration families in scope** | the full 5,345-line file: 939 `!important` lines, 1,787 Stylelint warnings (**25% of the entire baseline in one file**), 36 `@media` blocks, the `@layer workout` block at `:3539`, and the complete `:is()` family (G1). Classifies every declaration as live / dead / mixed / unverified across all 10 routes × 2 themes × 3 widths, following the WP4.3j-c method |
| **Explicit exclusions** | **no production edit.** Nominates deletions; authorizes none. Does not touch the `:is()` selector — that is WP4.4-i |
| **Dependency / merge order** | after **a**. Blocks **h** |
| **Concurrency** | **(b) parallel read-only audit** — may run concurrently with b, c, d, e, f because it writes no production file; it *reads* files those packets are editing, so its evidence must record the exact commit it audited and **h** must re-prove against merged `main` (cf. WP4.3j-c-dead re-resolving scope structurally rather than by the audit's line numbers) |
| **Expected movement** | production lines **0** |
| **Gates** | harness self-checks per WP4.4-a: same-CSS pixel control 0 diff on every context, resolution self-check 0 mismatches, sentinel-took-effect per record (M6), known-live controls (M5), `:is()`-aware specificity model unit-checked (M4) |
| **Known-red handling** | records only |
| **Rollback criteria** | n/a. A failing control invalidates the audit and blocks **h** until re-run |
| **Token value / visible rendering may change?** | **no** |

---

#### WP4.4-h — `components.css` dead-declaration deletion
| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/components.css` (**exclusive, single-writer**) |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_H_COMPONENTS_DEAD_EVIDENCE.md`; `tests/test_css_wp4_4_components_contracts.py` |
| **Selectors / declaration families in scope** | only the families WP4.4-g nominated **and** this packet re-proved on a branch cut fresh from merged `main`; scope re-resolved **structurally by selector shape, not by the audit's line numbers** |
| **Explicit exclusions** | the `:is()` selector itself (→ **i**); the `@layer workout` block's membership (G10); Region H (G9); anything the audit left "unverified" or "mixed" — **only unambiguously dead declarations are deleted** (M8) |
| **Dependency / merge order** | after **g**, and after b/c/d/e/f have merged (rebase onto all) |
| **Concurrency** | **(c) sequential** — single-writer on `components.css`; no other packet may hold this file |
| **Expected movement** | ⚠️ projected **−300 to −900** lines of 5,345; Stylelint 1,787 → 900–1,500; `!important` lines 939 → materially lower; `no-descending-specificity` should fall sharply, as it did in WP4.3j-c-dead (200 → 38) |
| **Gates** | full `pytest` + `tests/test_css_cascade_contracts.py` + the new per-packet contract; Chromium `visual.spec.ts`, `dark-mode.spec.ts`, `nav-dropdown.spec.ts`, `accessibility.spec.ts`, `summary-pages.spec.ts`, plus the per-page specs for all **five affected routes** (`workout-plan.spec.ts`, `workout-log.spec.ts`, `summary-pages.spec.ts`, `progression.spec.ts`) and the remaining five routes' specs, since `components.css` is global; before/after differential with **0 computed-value and 0 declaration-owner differences**, positive controls showing records *losing* candidates and **0 gaining** any |
| **Known-red handling** | WP4.0 ledger; band per M7 |
| **Rollback criteria** | any non-zero owner/computed difference not explained by an intended deletion; any visual diff outside the ledger; any Stylelint category increase |
| **Token value / visible rendering may change?** | **no** |

---

#### WP4.4-i — `components.css` `:is()` shared-selector repair *(owner-gated separately at implementation time)*
| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/components.css` (**exclusive, single-writer, sequential**) |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_I_IS_REPAIR_EVIDENCE.md`; extends `tests/test_css_wp4_4_components_contracts.py` |
| **Selectors / declaration families in scope** | the complete `:is()` family established by R3 condition 1, **now fully enumerated at current-`main` identity in [Inventory A](../CSS_PHASE4_WP4_4_N4_INVENTORY_A_IS_FAMILY.md)** — the twelve four-branch rules at `components.css:3335` (**two selector lines, `:3335` + `:3336`**), `:3351`, `:3360`, `:3368`, `:3377`, `:3381`, `:3386`, `:3390`, `:3395`, `:3400`, `:3405`, `:3409` — 38 declarations, four selector branches, five affected routes — **plus** the three-branch reduced-motion rule at `:4398`–`:4415` whose `:is()` line is **`:4413`** (was `:4433` pre-`h`; C9), 1 declaration, three branches, three routes. The five remaining `:is(` tokens (`:3635`, `:3655`, `:3678`, `:3749`, `:3750`) are **out of scope** — already ID-scoped under `#workout` and inside `@layer workout`, which N2 freezes |
| **Explicit exclusions** | any page bundle. **Per R3 condition 8, a required page-bundle edit is named and escalated as separately owner-gated — never absorbed.** Region H (G9); the ten frozen interaction-state declarations (G6); the WP4.3i-c Page Header contract (G7); layer membership (G10) |
| **Dependency / merge order** | after **h** (same-file serialization) and after every other implementation packet has merged. **Second-to-last implementation packet** |
| **Concurrency** | **(c) sequential, cascade-coupled** — by construction. No packet may run concurrently with it, because it re-decides ownership on five routes at once |
| **Expected movement** | ⚠️ line count roughly **flat** (a selector rewrite, not a deletion). The real movement is specificity: baseline `selector-max-id` **191** and `selector-max-specificity` **188** should fall measurably — this is the only planned packet that can move them at the shared level |
| **Gates** | **R3 conditions 1–8 are the gate.** Sequence: (1) complete family inventory; (2) **pre-change inventory of every page-local rule that would become a winner** — across all five routes, both themes, three widths; (3) Workout Log **regions A–C measured before**; (4) apply; (5) regions A–C measured **after**; (6) full differential on all five routes with **0 unexplained computed-value or owner differences**; (7) full `pytest`, all cascade contracts, `visual.spec.ts`, `dark-mode.spec.ts`, `nav-dropdown.spec.ts`, `accessibility.spec.ts`, `summary-pages.spec.ts` + all five route specs; (8) Stylelint showing specificity **down**, no category up |
| **Known-red handling** | WP4.0 ledger; band per M7 |
| **Rollback criteria** | **ROLLBACK, NOT REBASELINE** (R3 condition 6). Any unexplained rendering difference, any resurrection not identified and dispositioned in the step-2 pre-change inventory, or any A–C measurement change → revert the packet entirely. A resurrection discovered *after* the change is a rollback trigger, not a finding to accept |
| **Token value / visible rendering may change?** | **no** — the repair's success criterion is that computed values are identical while ownership becomes honest. Any detected change is a rollback trigger, not an approved change |

---

#### WP4.4-j — `theme-dark.css` triage into legacy values vs justified token remaps
| Attribute | Value |
|---|---|
| **Production paths owned** | `static/css/theme-dark.css` (exclusive) |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_J_THEME_DARK_EVIDENCE.md`; `tests/test_css_wp4_4_theme_dark_contracts.py` |
| **Selectors / declaration families in scope** | 621 lines, 81 top-level rules, 149 `!important` lines, 264 Stylelint warnings, 1 `@media`. Each rule classified as **legacy value** (delete if proven dead) or **justified token remap** (retain, documented) |
| **Explicit exclusions** | **Unlinking the file is forbidden (R4).** The REFACTOR_PLAN "removed after proof" end-state is out of reach for this arc. `templates/base.html` is frozen. No bulk delete. The superset dark-tint gap stays unacted (G4) — **do not** add a dark override for `--superset-bg-1..4` here as a back door |
| **Dependency / merge order** | **last implementation packet**, after **i** and after every other packet. `theme-dark.css` loads last and therefore wins every same-specificity tie in the app; classifying a rule as a "justified remap" is only meaningful against the final state of everything it overrides |
| **Concurrency** | **(c) sequential, cascade-coupled** |
| **Expected movement** | ⚠️ projected **−150 to −400** lines of 621; Stylelint 264 → 100–264; file **must not** reach 0 lines (R4 forbids the unlink, and an empty linked bundle is worse than a small justified one) |
| **Gates** | full `pytest` + all cascade contracts; Chromium `dark-mode.spec.ts` (**primary**), `visual.spec.ts` all 6 variants, `nav-dropdown.spec.ts`, `accessibility.spec.ts`, `summary-pages.spec.ts`, plus all 10 route specs — every route has a dark variant; dark-theme differential across all 10 routes with 0 unexplained differences |
| **Known-red handling** | WP4.0 ledger; the `workout-plan desktop dark` band is directly in this packet's blast radius (M7) |
| **Rollback criteria** | any dark-mode rendering difference; any light-mode difference at all (a dark-only file changing light rendering means the classification was wrong) |
| **Token value / visible rendering may change?** | **no** |

---

#### WP4.4-k — Final integration gate
| Attribute | Value |
|---|---|
| **Production paths owned** | **none.** Documentation only: `docs/MASTER_HANDOVER.md`, `docs/REFACTOR_PLAN.md` status, and `docs/CSS_OWNERSHIP_MAP.md` **if** ownership descriptions changed (see N5) — each a never-claimed shared path, edited by **one** writer at integration time only |
| **Test/evidence paths owned** | `docs/CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md` |
| **Selectors / declaration families in scope** | none — verification and reporting only |
| **Explicit exclusions** | no new CSS change may be introduced here. A defect found at this gate is fixed by a **new packet**, not by an unreviewed integration edit |
| **Dependency / merge order** | **last.** Requires rebase onto every preceding merged packet |
| **Concurrency** | **(c) sequential** — nothing runs alongside it |
| **Expected movement** | reports cumulative: total lines removed across the seven surfaces, Stylelint delta vs the pinned WP4.1 baseline, `!important` delta, duplicate-count delta (V4 monotonicity across the whole arc), and **WP4.4's contribution plus remaining shortfall against the 30,768-line Phase-4 denominator** (V5) |
| **Gates** | `/verify-suite` — **full pytest** + full Chromium E2E; the complete visual matrix in **both themes across all 10 routes**; all cascade contracts; Stylelint full re-measure; a final `:is()`-aware ownership differential proving the arc's net computed-value change is **zero** |
| **Known-red handling** | final ledger reconciliation: the reds present at the end must be exactly the reds present at `f4f9ee6`, with the animated-logo red inside its band |
| **Rollback criteria** | any red not in the ledger blocks the arc close; the offending packet is identified by bisecting the merge order and reverted individually |
| **Token value / visible rendering may change?** | **no** |

---

### Packet DAG

Edge types: `PE` = prerequisite-evidence · `SFS` = same-file-serialization · `CC` = cascade-coupling · `CD` = contract-dependency.

```
                          ┌──────────────────────────────┐
                          │ WP4.4-a  baseline + harness  │  (read-only)
                          └──────┬───────────────────────┘
             PE ┌────────┬───────┼───────┬────────┬────────┐ PE
                ▼        ▼       ▼       ▼        ▼        ▼
            ┌──────┐ ┌───────┐ ┌─────┐ ┌──────┐ ┌──────┐ ┌──────────┐
            │  b   │ │   c   │ │  d  │ │  e   │ │  f   │ │    g     │
            │ base │ │motion │ │a11y │ │layout│ │navbar│ │comp.audit│
            └───┬──┘ └───┬───┘ └──┬──┘ └──┬───┘ └──┬───┘ └────┬─────┘
                │        │        │       │        │  PE      │ PE
                └────────┴────────┴───────┴────────┴──────────┤
                                                              ▼
                                                    ┌──────────────────┐
                                                    │ h  comp. dead-   │
                                                    │    deletion      │
                                                    └────────┬─────────┘
                                                             │ SFS
                                                             ▼
                                                    ┌──────────────────┐
                                                    │ i  :is() repair  │ (owner-gated)
                                                    └────────┬─────────┘
                                                             │ CC
                                                             ▼
                                                    ┌──────────────────┐
                                                    │ j  theme-dark    │
                                                    └────────┬─────────┘
                                                             │ CC
                                                             ▼
                                                    ┌──────────────────┐
                                                    │ k  integration   │
                                                    └──────────────────┘
```

| From | To | Type | Reason |
|---|---|---|---|
| a | b, c, d, e, f, g | `PE` | No packet may classify a declaration dead before the harness's controls pass and the true per-surface baseline is measured (M5, M6) |
| a | f | `PE` | Exact `@layer` spans must exist before any navbar rule is touched (G10) |
| g | h | `PE` | Deletion may only act on families an audit nominated and this packet re-proved |
| b, c, d, e, f | h | `CC` | `components.css` deadness proofs must be taken against the *final* state of the other shared bundles; h rebases onto all of them and re-proves |
| h | i | `SFS` | Both write `static/css/components.css`; only one writer, ever |
| g | i | `PE` | R3 condition 1 — the complete affected family comes from the audit |
| h | i | `CC` | The repair must not resurrect rules; h having already deleted the dead ones is the discharged prerequisite pattern (G2) |
| i | j | `CC` | `theme-dark.css` loads last; "justified remap" is only decidable against final shared ownership |
| b…f, h, i | j | `CC` | Same reason, transitively |
| all | k | `CD` | The integration gate verifies every contract and the cumulative invariants |

**Linear merge order satisfying the DAG:**

`a` → { `b`, `c`, `d`, `e`, `f` — developed concurrently, **merged one at a time in any internal order**, each rebasing onto merged `main` and re-proving } → `g` → `h` → `i` → `j` → `k`

`g` may *start* as soon as `a` lands and run concurrently with b–f, but its evidence must record the audited commit, and `h` re-proves structurally against merged `main`.

### §4 Concurrency classification

**(a) Safe for Codex and Opus to implement concurrently in separate worktrees**

| Packet | File owned | Disjoint at file level from |
|---|---|---|
| WP4.4-b | `static/css/base.css` | c, d, e, f |
| WP4.4-c | `static/css/motion.css` | b, d, e, f |
| WP4.4-d | `static/css/a11y.css` | b, c, e, f |
| WP4.4-e | `static/css/layout.css` | b, c, d, f |
| WP4.4-f | `static/css/navbar.css` | b, c, d, e |

Suggested pairings — **one file each, never two writers on one file**:

| Pairing | Codex | Opus | Rationale |
|---|---|---|---|
| 1 | `b` (base) + `c` (motion) — 194 lines combined | `f` (navbar) — 1,542 lines, highest risk | Balances the two tiny surfaces against the riskiest one |
| 2 | `d` (a11y) | `e` (layout) | Comparable size (813 vs 1,841); disjoint gate suites |

**Why file-level disjointness is sufficient here — and the theorem that makes it so.** Two concurrent deletion packets could in principle interact if rule X in file 1 were dead *because* rule Y in file 2 suppresses it, and packet 2 deletes Y. **M8 forecloses this**: a packet may delete only proven **non-winners**, and a non-winner's deletion cannot change any computed value while its winner remains. Since no packet ever deletes a winner, deletions across files **commute**. Belt-and-braces: every packet **rebases onto merged `main` and re-proves its full differential before merging** — the WP4.3j-c-dead pattern of re-resolving scope structurally rather than by recorded line numbers.

**(b) Parallel read-only audits only**

| Packet | Note |
|---|---|
| WP4.4-a | Owns no production path; may run alongside anything |
| WP4.4-g | Owns no production path; reads `components.css` and all page bundles. May run while b–f edit their files, provided its evidence records the audited commit and `h` re-proves against merged `main` |

**(c) Must land sequentially — cascade / load-order coupling**

| Packet | Coupling |
|---|---|
| WP4.4-h | Single-writer on `components.css`; must follow all shared-bundle changes so its proofs reflect final state |
| WP4.4-i | Same file as h (`SFS`); re-decides ownership on five routes simultaneously; owner-gated |
| WP4.4-j | `theme-dark.css` loads **last** and wins all same-specificity ties; only decidable against final state |
| WP4.4-k | Verification of everything |

**(d) Shared files only one workstream may edit**

| Path | Rule |
|---|---|
| `static/css/components.css` | Single-writer across h and i; strictly serialized |
| `tests/test_css_cascade_contracts.py` | ⚠️ **Shared.** Concurrent packets must NOT both edit it — see New owner decision **N1** (per-packet contract files) |
| `docs/MASTER_HANDOVER.md` | **Never-claimed shared path** ([WORKSTREAM_OWNERSHIP.md](../ai_workflow/WORKSTREAM_OWNERSHIP.md) §Never-claimed). Edited only at WP4.4-k, by one writer |
| `docs/REFACTOR_PLAN.md`, `docs/CSS_OWNERSHIP_MAP.md` | Same treatment — integration-time only |
| root `CLAUDE.md`, folder `CLAUDE.md`, `.claude/settings.json`, `.gitignore`, `app.py` | **Never-claimed shared paths.** No WP4.4 packet touches any of them |
| `templates/base.html` | **Frozen by R4.** No packet edits it |
| `data/database.db` + sidecars, `data/auto_backup/`, `MASTER_HANDOVER.local.md`, `.venv/` | **Per-worktree, never shared.** No packet stages or commits the DB |

**Final integration gate** — WP4.4-k, above: rebase onto every preceding packet, then full `/verify-suite`, the complete both-theme × 10-route visual matrix, all cascade contracts, a full Stylelint re-measure against the pinned baseline, and the V5 contribution/shortfall report.

### Effort · Owner · Depends on

| Packet | Effort | Owner | Depends on |
|---|---|---|---|
| WP4.4-a | M | audit agent (read-only) | — |
| WP4.4-b | S | Codex or Opus | a |
| WP4.4-c | S | Codex or Opus | a |
| WP4.4-d | M | Codex or Opus | a |
| WP4.4-e | M | Codex or Opus | a |
| WP4.4-f | L | Codex or Opus | a |
| WP4.4-g | L | audit agent (read-only) | a |
| WP4.4-h | L | single writer | g, b–f |
| WP4.4-i | L | single writer, **separately owner-gated** | h, g |
| WP4.4-j | M | single writer | i |
| WP4.4-k | M | single writer | all |

### Sequence

1. Gate 1 approval of Plan v2.
2. Run **WP4.4-a**; land its evidence. Correct every ⚠️ projection in this plan from its measurements.
3. Start **WP4.4-g** (read-only) and, concurrently, up to two of { b, c, d, e, f } in **separate worktrees created outside the manager session**.
4. Merge b–f **one at a time**, each rebased onto merged `main` with its differential re-proved.
5. Land **WP4.4-g** evidence.
6. Run **WP4.4-h**; rebase onto everything; re-resolve scope structurally; merge.
7. **Stop for separate owner approval of WP4.4-i.** Run its R3 conditions 1–2 (family inventory + would-become-winner inventory) and present them *before* any edit.
8. Run **WP4.4-i** if approved; rollback-not-rebaseline on any surprise.
9. Run **WP4.4-j**.
10. Run **WP4.4-k**; report contribution and shortfall.

### Expected gates *(to be confirmed / corrected by `test-strategist` at council)*

- **pytest**: `tests/test_css_cascade_contracts.py`, `tests/test_visual_selector_contracts.py`, per-packet `tests/test_css_wp4_4_*_contracts.py`; **full pytest** at h, i, j, k.
- **e2e**: `visual.spec.ts` (every packet), `dark-mode.spec.ts` (every packet), `nav-dropdown.spec.ts` (f, h, i, j, k), `accessibility.spec.ts` (d, c, f, h, i, j, k), `summary-pages.spec.ts` (h, i, j, k), the five affected-route specs (h, i), all 10 route specs (j, k).
- **other**: pinned Stylelint (`16.11.0` + `postcss-scss` `4.0.9`, config `.stylelintrc.json`, `npm run lint:css`) measured against `docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json` on every packet; `/verify-suite` at k. **`/build-css` is NOT required** — no packet edits `scss/**`.

### ⚠️ Honest projection against the Phase-4 target (V5)

Summing the projected mid-points: roughly **−800 to −2,100 lines** across the seven surfaces, i.e. **8–20% of WP4.4's own 10,356-line surface** and **2.6–6.8% of the 30,768-line Phase-4 denominator**. **WP4.4 as planned will not deliver the 30% Phase-4 target by itself**, and per R5 and V6 it is not required to. WP4.4-k reports the contribution and the shortfall; closing the remainder is a later-phase decision, not a licence for any packet here to delete beyond what it can prove.

### New owner decisions surfaced by Plan v1

*These are Gate-1 decisions. Gate 0 did not resolve them because they emerged from the decomposition itself.*

- **N1 — Per-packet contract test files.** `tests/test_css_cascade_contracts.py` is a **single shared file**. If every concurrent packet adds its contract there, the (a)-class packets are no longer file-disjoint and the concurrency claim collapses. **Recommendation: each packet adds `tests/test_css_wp4_4_<surface>_contracts.py`**, leaving the shared file untouched until WP4.4-k optionally consolidates. Needs a yes/no.
- **N2 — Freeze `@layer` membership for the whole arc?** Layered vs unlayered precedence inverts between normal and `!important` declarations, and `navbar.css:908` shows the codebase already relies on the boundary deliberately. **Recommendation: freeze — no packet may move a rule across a layer boundary.** Needs confirmation.
- **N3 — WP4.4-i escalation path (R3 condition 4).** If the pre-change inventory shows page-local rules *would* become winners, what happens? Options: **(i)** abandon the repair; **(ii)** narrow the repair to branches with no would-be winners; **(iii)** delete the offending page-local rules first — which pulls page bundles into scope and needs its own approval. **Recommendation: (ii), falling back to (i).** Needs a ruling before WP4.4-i starts.
- **N4 — Does WP4.4-i require its own approval checkpoint at implementation time?** Plan v1 assumes **yes** (step 7 above stops for it). Confirm.
- **N5 — May WP4.4-k update `docs/CSS_OWNERSHIP_MAP.md`?** Its maintenance rule 1 triggers on *loading* changes, and R4 freezes loading — but the **responsibility** descriptions will have changed materially. **Recommendation: yes, responsibilities only, at k, single writer.** Needs a yes/no.

---

## Agent provenance

*The manager records each agent ID and supplies the `product-manager` its own ID back, because an agent cannot know its own ID. IDs below are stamped exactly as supplied — none invented.*

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a04906a2a312cd209` | Author of Section 0 and Plan v1. ID supplied by the manager at Gate 0 approval. |
| `product-manager` — response matrix + Plan v2 | `a04906a2a312cd209` | Author of the response matrix and Plan v2. Same agent as Plan v1. |
| `architecture-reviewer` | `a7f0ed6f3908ca730` | Step 2 reviewer — verdict **blocking** (A1–A4). |
| `test-strategist` | `aec57a5d3d5137cf2` | Step 2 reviewer — verdict **blocking** (F1, F3, F4, F5, F6, F8; F17 self-upgrading). |
| `product-risk-reviewer` | `a398c39b3f311bfd1` | Step 2 reviewer — verdict **blocking** (#2, #3, #4). |

**Same product-manager resumed for the matrix + Plan v2?** **`yes`** — resumed via `SendMessage` to the Plan v1 agent ID `a04906a2a312cd209`. No fresh `product-manager` was spawned, no council work was rerun, and no ID was invented.

**Evidence gap**: `none`

---

## Reviewer findings

*Council step 2 complete. Three reviewers ran in parallel against Plan v1. **All three returned `blocking`.** Each output is pasted verbatim below, headed by its agent ID — not summarized, not condensed, not re-worded.*

### architecture-reviewer (agent `a7f0ed6f3908ca730`)

### architecture-reviewer — findings on `d:\development\Hypertrophy-Toolbox-v3-main\docs\css_phase4_wp4_4\PLANNING.md` (Plan v1)

---

**A1. WP4.4-i is structurally incapable of passing an existing cascade contract that no packet is authorized to amend.**
Severity: **blocking**
Location: packet **WP4.4-i** (Production paths / Test-evidence paths / Gates rows); §2 G-table (G9 is the only contract lock recorded).

`d:\development\Hypertrophy-Toolbox-v3-main\tests\test_css_cascade_contracts.py:1614-1627` (inside `test_workout_log_drops_cascade_dead_header_and_cell_glass`, the WP4.3j-c-dead contract) asserts the **literal four-branch selector string**:

```python
shared_arm = (':is(#workout[data-page="workout-plan"], .workout-log-page, '
              ".summary-frame.frame-calm-glass, .progression-plan-container)")
assert shared_arm in components
dark_cell = re.search(r"\[data-theme='dark'\] :is\(#workout\[data-page=\"workout-plan\"\][^{]*?"
                      r"\.table\.table-calm tbody td \{[^}]*\}", components)
assert "color: var(--ink-1, #eef1f6) !important;" in dark_cell.group(0)
```

Any repair of the `:is()` arm — by definition — changes that string. WP4.4-i's gate row demands "full `pytest`, all cascade contracts"; it will red by construction. WP4.4-i's declared evidence paths are only its evidence doc plus `tests/test_css_wp4_4_components_contracts.py`; it does not own `tests/test_css_cascade_contracts.py`, and §4(d) lists that file as shared-and-not-to-be-edited. N1–N5 contain no decision covering amendment of an existing shipped contract.
Recommended change: add **N6** — "may WP4.4-i amend `tests/test_css_cascade_contracts.py:1614-1627` (the j-c-dead shared-arm anchor), and under what proof?" — and add `tests/test_css_cascade_contracts.py` to WP4.4-i's owned-evidence row as a serialized single-writer claim, with the amendment restricted to re-expressing the same *premise* (the shared rule still out-specifies the page-local Workout Log families) rather than deleting the assertion.

---

**A2. WP4.4-i's blast radius is unbounded because the repair *shape* is never specified, and two of the plausible shapes need production paths the packet does not own.**
Severity: **blocking**
Location: packet **WP4.4-i**, "Selectors / declaration families in scope" and "Explicit exclusions"; R3 condition 8.

The packet enumerates *which rules* are in scope (correctly — I verified all 12 four-branch rules at `d:\development\Hypertrophy-Toolbox-v3-main\static\css\components.css:3335,3351,3360,3368,3377,3381,3386,3390,3395,3400,3405,3409`) but never states *what the repair does*. The four realistic shapes have materially different reach:

- split the `:is()` list into four separate selectors → drops specificity from `(1,3,x)` to `(0,3,x)` on **three** branches, changes ownership on four routes;
- wrap the ID branch in `:where()` → drops it on **all four**, including Workout Plan;
- delete the ID branch and rely on a class hook → requires a **template** edit (`templates/workout_plan.html`) and possibly JS;
- keep `:is()` and drop `!important` → a different invariant entirely.

R3 condition 8 covers only *page-bundle* edits. A template or JS edit is covered by nothing in the plan, and would be silent production-scope expansion of exactly the kind R3.8 was written to prevent.
Recommended change: WP4.4-i must, at plan time, enumerate the admissible repair shapes and, for each, the **complete set of production paths** it would require; declare that any shape needing a `templates/**` or `static/js/**` change is escalated as a separate owner-gated packet, never absorbed. Then let R3 condition 2's pre-change inventory select among the enumerated shapes.

---

**A3. WP4.4-i can resurrect the ten frozen WP4.3i interaction-state declarations without editing them — G6 as written does not prevent this.**
Severity: **blocking**
Location: §2 G6; packet **WP4.4-i** "Explicit exclusions" ("the ten frozen interaction-state declarations (G6)").

G6 and i's exclusion list are both phrased as *do not edit*. The ten declarations survive in `pages-workout-plan.css` precisely because they are currently non-winners; lowering the shared `:is()` specificity on the `#workout[data-page="workout-plan"]` branch can make them win. That is a visible change on Workout Plan produced without touching a single frozen line — the standing constraint is violated in effect while being honored in letter. The same argument applies to the retained Workout Log region-C hover rule that `tests/test_css_cascade_contracts.py:1644-1649` documents as "proposes a hover `filter` and loses to the region-G light winner".
Recommended change: extend R3 condition 2 (pre-change would-be-winner inventory) with a named sub-list: the ten frozen WP4.3i-dead declarations and Workout Log regions A–C must each be individually proven to remain non-winners after the repair; any of them becoming a winner is a **rollback trigger**, not a finding to disposition.

---

**A4. The (a)-concurrency class is not executable as written: two worktrees cannot run the Playwright visual matrix simultaneously, and `PW_REUSE_SERVER=1` will silently certify a packet against another worktree's CSS.**
Severity: **blocking**
Location: §4(a) "Safe for Codex and Opus to implement concurrently in separate worktrees"; the suggested pairings table; every b–f "Gates" row (each demands `visual.spec.ts` + `dark-mode.spec.ts`).

`d:\development\Hypertrophy-Toolbox-v3-main\playwright.config.ts:67` hard-codes `baseURL: 'http://127.0.0.1:5000'` and line 114 honours `reuseExistingServer` from `PW_REUSE_SERVER === '1'` (documented as a convenience in `.claude\rules\testing.md`). Two concurrent packets either collide on port 5000 or — worse, with the documented env var set — worktree B's visual matrix renders worktree A's stylesheets and returns a **false green** on V1, the plan's primary rollback gate. The plan's disjointness proof is at the file level only and never reaches the measurement apparatus.
Recommended change: add to §4 an explicit serialization rule for E2E/visual runs — either "only one worktree may run Playwright at a time; `PW_REUSE_SERVER` must be unset in every packet worktree", or a per-worktree port override plumbed through `playwright.config.ts` (which is itself a shared path and would need a single-writer claim). Also mandate the worktree seed mode (`scripts\new-worktree.ps1 -Seed visual`) for every packet worktree, since the WP4.0 ledger was measured against the visual seed and an unseeded worktree makes V1 incomparable.

---

**A5. The commutativity theorem has a real cross-file counterexample: custom-property declarations and shorthand/longhand granularity fall outside the "winner" oracle.**
Severity: **should-fix**
Location: §4 "Why file-level disjointness is sufficient here — and the theorem that makes it so"; M8.

The theorem — "a non-winner's deletion cannot change a computed value while its winner remains" — is sound *only over the property universe the oracle enumerates*. Two holes, both cross-file:

1. **Custom properties.** A `--x: …` declaration paints nothing and is a non-winner for every standard property, yet may be the sole definition consumed by a `var()` in a different bundle, and it inherits across the DOM. This is not hypothetical: `tests/test_css_cascade_contracts.py:150-152` asserts `--nav-gap: var(--s-3);` in `navbar.css` precisely because token definitions get deleted as "unused". Packet e deleting a `layout.css` token consumed by `components.css` breaks A-then-B ≠ B-then-A.
2. **Shorthand/longhand.** A shorthand that loses on one longhand may win on another. M6 records the converse defect (`var()`-bearing shorthands invisible to longhand CSSOM queries) but M8 is stated at shorthand granularity.

Recommended change: add **M9** — the deadness oracle's property universe must be longhand-complete, and **no packet may delete a custom-property declaration under the non-winner rule**; custom-property removal requires a `var()` dependency graph resolved across all 21 hand-maintained sources (the WP4.3h `--wpdd-*` precedent at `tests/test_css_cascade_contracts.py:929-947` is the template).

---

**A6. The `@layer` characterisation in the Problem section is wrong for `!important`, and M4's model requirements omit layers entirely.**
Severity: **should-fix**
Location: Section 0 "Problem", the sentence "roughly 900 of `navbar.css`'s 1,542 lines sit inside a layer that loses to every unlayered rule"; §2b M4.

For **normal** declarations that is correct. For **`!important`** the order inverts *and* unlayered important is the **weakest** — a layered `!important` beats every unlayered `!important`, and among layers the earlier-declared layer wins. `tokens.css:2` orders `workout, navbar, workout-dropdowns, welcome`, so an `!important` inside `@layer navbar` (`navbar.css:6`) beats every unlayered `!important` in `components.css`, `a11y.css` and `theme-dark.css`, and loses only to `@layer workout`. `navbar.css` carries 93 `!important` lines. A packet-f implementer reading the plan's flat sentence as licence to nominate the layered generation as dead would delete live winners. G10 states the inversion correctly, which makes the Problem-section sentence an internal contradiction rather than an omission.
Recommended change: correct the sentence to scope it to normal declarations, and extend **M4** to require the specificity/ownership model to implement layer ordering *and* the importance inversion, unit-checked against hand-computed cases, alongside the existing `:is()`/`:where()`/`:not()`/`:has()` requirement.

---

**A7. Packet f can make an existing layer contract unsatisfiable, and the only repairs are both out of bounds.**
Severity: **should-fix**
Location: packet **WP4.4-f**; §2 G10.

`tests/test_css_cascade_contracts.py:84-102` asserts `layer_blocks == set(LAYER_ORDER)` — every layer named in `tokens.css:2` must have a live block. I verified the sources: `workout` is dual-sourced (`components.css:3539`, `pages-workout-plan.css:718`), `workout-dropdowns` and `welcome` live in page bundles, but **`navbar` is single-sourced at `navbar.css:6`**. If f's triage concludes the layered generation is dead and deletes the block, the contract fails, and repairing it requires editing either `tokens.css:2` (R1: out) or the shared contract file (§4(d): not editable by a concurrent packet).
Recommended change: add **G11** — "no packet may delete the last `@layer <name> { … }` block for any name in the `tokens.css:2` order list"; note it explicitly in WP4.4-f's exclusions, so the deletion ceiling is known before the packet starts rather than discovered at its gate.

---

**A8. WP4.4-a does not produce the one artifact every implementation packet needs: a contract-anchor inventory.**
Severity: **should-fix**
Location: packet **WP4.4-a** "Selectors / declaration families in scope"; §2 G-table (only G9 is recorded).

The plan records exactly one contract lock (G9, Region H, correctly cited at `tests/test_css_cascade_contracts.py:43`). The shared contract file contains at least six more assertions that bind the seven surfaces owned by b–j:

| Anchor | Binds |
|---|---|
| `:150-152` `--nav-gap` / `--nav-padding-y` / `--nav-padding-x` string asserts | f |
| `:102` layer-block completeness | f (see A7) |
| `:189-215` exact occurrence counts in `components.css` (`== 1`, `== 2`) | h |
| `:902-906` `.wpdd-button…` strings in `components.css`; `"*:focus-visible,"` in `a11y.css` | h, d |
| `:996-1007` WP4.3i-c page-header anchors — 7 strings in `components.css`, `:where([data-theme="dark"] .frame-header) {` and `backdrop-filter: blur(8px) !important;` in `theme-dark.css` | h, j — and **G7 forbids modifying this contract**, so j's "legacy value vs justified remap" triage is pre-constrained on those two rules |
| `:1614-1627` shared-arm + dark-cell regex | h, i (see A1) |

Without this inventory each packet discovers its ceiling at gate time.
Recommended change: make "contract-anchor inventory — every assertion in `tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py` that reads each of the seven surfaces, with line numbers and a frozen/amendable disposition" an explicit WP4.4-a deliverable, and add a `CD` edge from **a** to every implementation packet.

---

**A9. G3 (Workout Log regions A–C re-measurement) binds only WP4.4-i, but WP4.4-h can change shared selector ownership too.**
Severity: **should-fix**
Location: §2 G3 ("This is a hard gate on packet **WP4.4-i**, not advice"); packet **WP4.4-h** "Explicit exclusions" ("the `:is()` selector itself (→ **i**)").

h's exclusion is written at *selector* granularity. Deleting a declaration from inside one of the twelve four-branch rules leaves the selector intact while changing what the shared rule owns for that property across all five routes — the precise trigger G3 exists for. Under the plan as written h could delete, say, `box-shadow: none !important;` from `components.css:3353` and never re-measure A–C.
Recommended change: restate h's exclusion at declaration granularity ("no declaration inside the twelve four-branch `:is()` rules or the `:4433` rule may be deleted by h; the whole family belongs to i"), and extend G3 to bind h as well.

---

**A10. The `:is()` family is mis-described: `components.css:4433` has three branches, not four, and reaches three routes, not five.**
Severity: **should-fix**
Location: Terminology table; §2 G1; packet **WP4.4-i** scope row (which lists `:4433` alongside the twelve four-branch rules under "Four selector branches; five affected routes").

Verified at `d:\development\Hypertrophy-Toolbox-v3-main\static\css\components.css:4433`:

```css
  :is(#workout[data-page="workout-plan"], .workout-log-page, .progression-plan-container) .table.table-calm tbody td {
    transition: none !important;
```

`.summary-frame.frame-calm-glass` is **absent**, and the rule sits inside `@media (prefers-reduced-motion: reduce)` (opened at `components.css:4417`). So reduced-motion transition suppression is currently **not** applied to Weekly/Session Summary tables — a pre-existing behavioural asymmetry, not a typo to fix in passing. "Normalizing" it during the repair would be a visible/behavioural change on two routes under reduced motion, requiring owner approval.
Recommended change: correct the terminology table and G1 to state that the family is *twelve four-branch rules plus one three-branch reduced-motion rule*; record the asymmetry as a **finding for WP4.4-a/g**, and add it to WP4.4-i's exclusions as "preserve the existing branch asymmetry unless separately approved".

Related, same location: `components.css:3635, 3655, 3678, 3749, 3750` contain a **second** ID-exporting `:is()` construct (`input.input-calm-inset:is(#weight, #sets, …)`). It is already nested under `#workout[data-page="workout-plan"]`, so it is not a cross-route leak — but the plan's phrase "the complete `:is()` family" is imprecise against the 19 `:is()` occurrences in the file. Have WP4.4-a enumerate and classify all 19 so R3 condition 1 has a defensible closure argument.

---

**A11. WP4.4-a's harness is placed under a gitignored path and therefore cannot reach the packets that depend on it.**
Severity: **should-fix**
Location: packet **WP4.4-a** "Test/evidence paths owned" ("harness scripts under gitignored `artifacts/wp4_4/`"); the `a → b,c,d,e,f,g` PE edges.

`d:\development\Hypertrophy-Toolbox-v3-main\.gitignore:55` ignores `/artifacts/`. A gitignored harness does not propagate through a merge to a fresh worktree cut from `main`, so every downstream packet's PE dependency on a's harness is unsatisfiable — each would re-implement it, which contradicts M5/M6 reproducibility and makes the k-gate's "final `:is()`-aware ownership differential" non-reproducible against a's controls. The repo already has the right home: `d:\development\Hypertrophy-Toolbox-v3-main\scripts\` is committed and holds `stylelint-report.mjs`, `pyright_baseline_diff.py`, etc. (ADR-002 sends *generated output* to `artifacts/`, not tooling.)
Recommended change: split a's deliverable — reusable harness **committed** under `scripts/css_audit/` (a new shared path, so declare it single-writer and note that b–f may not modify it without serialization), generated captures/reports under gitignored `artifacts/wp4_4/`. Add it to the §4(d) shared-file table.

---

**A12. Three DAG defects: one missing edge, one edge asserted in prose but absent from the table, one packet whose ordering hazard is unrecorded.**
Severity: **should-fix**
Location: §"Packet DAG" edge table and the linear merge order.

The graph is acyclic and the stated linear order `a → {b,c,d,e,f} → g → h → i → j → k` does satisfy every edge *that is listed*. Three problems:

1. **Missing `b…f → g`.** g classifies `components.css` declarations dead partly *because* rules in `a11y.css`/`layout.css`/`navbar.css` win. If d/e/f delete those, g's classification is stale. The plan mitigates via h's re-proof, and the mitigation is directionally safe (a family that becomes *live* is re-proved live and excluded; only missed opportunities are lost) — but h's scope row describes the re-proof as re-resolving scope "structurally by selector shape", which is weaker than re-running classification. Either add the edge or state explicitly that g is advisory-nomination-only and that **h re-runs full classification for every nominated family**.
2. **`b…f → i` is asserted in i's dependency row ("after every other implementation packet has merged") but absent from the edge table**, which lists only `h → i` and `g → i`. Add it.
3. **WP4.4-c is oracle-affecting, not merely file-disjoint.** `motion.css` owns the transitions whose in-flight state produced WP4.3i-dead's 52-differing-record control failure (M1's origin). Merging c mid-arc invalidates differentials that b/d/e/f captured before it. This is contained by the "rebase and re-prove" rule only if re-proof means a full re-capture. Recommend: schedule c **first** among the concurrent set, and state that re-proof after rebase is a full re-run, not a delta against recorded line numbers.

Nit within the same section: `a → f` is redundant with `a → b,c,d,e,f,g`; and `all → k` is typed `CD` though AC5 names a distinct final-integration step — the legend has no `FI` type.

---

**A13. AC1 is self-violated: `components.css` is owned exclusively by two implementation packets.**
Severity: **should-fix**
Location: AC1 ("no two implementation packets own the same production path"); packets **h** and **i**; §4(d) row 1.

h and i both declare `static/css/components.css` as "exclusive, single-writer". §4(d) resolves it correctly in practice ("single-writer across h and i; strictly serialized"), but the plan's own deliverable acceptance criterion reads as an absolute, so the artifact fails its own AC1 on a literal reading — which matters because AC1 is the criterion a later reviewer will check the plan against.
Recommended change: restate AC1 as "no two **concurrently eligible** implementation packets own the same production path; where a path is claimed by more than one packet, the plan must name the serialization edge" and cite `h --SFS--> i` as the discharge.

---

**A14. Deferring every documentation update to WP4.4-k leaves five merged production changes with no handover record.**
Severity: **should-fix** (process/continuity, not cascade)
Location: packet **WP4.4-k** "Production paths owned"; §4(d) rows for `docs/MASTER_HANDOVER.md` / `docs/REFACTOR_PLAN.md`.

`WORKSTREAM_OWNERSHIP.md` rule 4 asks for **per-edit coordination** on never-claimed paths, not a prohibition — and the plan already serializes merges one at a time, which *is* the coordination. Under Plan v1, if the arc is interrupted after e merges (a realistic outcome given the arc's length and the owner-gate at step 7), `MASTER_HANDOVER.md` and `REFACTOR_PLAN.md` will describe WP4.4 as "not started" while five shared bundles have changed on `main`. Every prior Phase-4 packet updated them at merge.
Recommended change: allow each packet to append its own status line to `docs/MASTER_HANDOVER.md` and the REFACTOR_PLAN status header **at merge time** (serialized by the one-at-a-time merge rule, so still single-writer at any instant); keep the *cumulative* reconciliation and `CSS_OWNERSHIP_MAP.md` responsibility rewrite at k as N5 proposes.

---

**A15. Minor internal inconsistencies.**
Severity: **nit**
- Section 0 states "A1–A6 resolved by R1–R6" — but A6 maps to R4 and R6 answers open question 6, not an assumption. The mapping is 6→5.
- WP4.4-k lists `docs/REFACTOR_PLAN.md` and `docs/CSS_OWNERSHIP_MAP.md` under the never-claimed treatment; only `docs/MASTER_HANDOVER.md` is actually on that list in `WORKSTREAM_OWNERSHIP.md:29-34`. The plan is conservative in the safe direction — no change needed, just don't cite it as a rule requirement.
- WP4.4-i's scope enumeration omits `components.css:3336`, the second selector line of the rule opened at `:3335`.

---

### Areas that are sound — stated once, not padded

- **Ownership model does not leak.** WP4.4-a and WP4.4-g both declare `Production paths owned: none` and claim only evidence paths, exactly as the AC1 model requires; g explicitly records the audited commit and hands re-proof to h. Two read-only audits reading `components.css` concurrently with b–f writing other files is correct.
- **AC2 completeness holds.** All eleven attributes are present in all eleven packet tables; I checked each row.
- **AC8 / the 18-bundle cap is satisfied and correctly reasoned.** No packet proposes splitting, merging or removing a bundle; R4 freezes `templates/base.html`; j's "must not reach 0 lines" is the right guard. `test_runtime_bundle_cap_and_route_ownership_are_unchanged` (`tests/test_css_cascade_contracts.py:64-81`) is cited accurately (8 globals, 10 route bundles).
- **R3 conditions 1–8 are transcribed faithfully into WP4.4-i's gate sequence**, including "ROLLBACK — not rebaseline" and the requirement that a post-change resurrection is a rollback trigger rather than a finding. The reading note is preserved intact.
- **Ordering of j last is correctly justified.** `theme-dark.css` loads last (verified against the base.html order and the repeated `motion.css < theme-dark.css` assertions in the contract file), so "justified remap" genuinely is undecidable before the shared state settles.
- **Standing constraints are respected at the level of direct edits**: no packet touches `app.py`, root or folder `CLAUDE.md`, `.claude/settings.json`, `.gitignore`, `templates/base.html`, `tokens.css`, `pages-workout-plan.css`, or `data/**`; WP4.3i-jm and WP4.3i-o are not re-dispatched; R2 keeps the superset gap unacted; G9's Region H hash is cited at the correct line. The only standing-constraint exposure is the *indirect* one in A3.
- **The commutativity theorem is correctly scoped to deletions**, and the plan correctly places the two non-deletion packets (i's rewrite, j's retain-or-delete triage) outside the concurrent class. The theorem's failure modes are the two in A5, not its structure.

---

**Verdict: blocking** — four items (A1–A4) must be resolved before Plan v2 can be approved: the WP4.4-i contract impossibility, its unspecified repair shape and undeclared production paths, its ability to resurrect the frozen WP4.3i declarations without editing them, and the un-serialized Playwright/port collision that can produce a false-green V1 in the (a)-class concurrency. Everything from A5 down is fixable inside Plan v2 without a new Gate 0.

Files cited:
- `d:\development\Hypertrophy-Toolbox-v3-main\docs\css_phase4_wp4_4\PLANNING.md`
- `d:\development\Hypertrophy-Toolbox-v3-main\tests\test_css_cascade_contracts.py`
- `d:\development\Hypertrophy-Toolbox-v3-main\static\css\components.css`
- `d:\development\Hypertrophy-Toolbox-v3-main\static\css\navbar.css`
- `d:\development\Hypertrophy-Toolbox-v3-main\static\css\tokens.css`
- `d:\development\Hypertrophy-Toolbox-v3-main\playwright.config.ts`
- `d:\development\Hypertrophy-Toolbox-v3-main\.gitignore`
- `d:\development\Hypertrophy-Toolbox-v3-main\scripts\` (harness home; precedent `scripts\stylelint-report.mjs`, `scripts\new-worktree.ps1`)
- `d:\development\Hypertrophy-Toolbox-v3-main\docs\ai_workflow\WORKSTREAM_OWNERSHIP.md`
- `d:\development\Hypertrophy-Toolbox-v3-main\docs\ai_workflow\PARALLEL_WORKFLOW.md`
- `d:\development\Hypertrophy-Toolbox-v3-main\docs\REFACTOR_PLAN.md`

---

### test-strategist (agent `aec57a5d3d5137cf2`)

## Findings — test-strategist

Reviewed cold against `d:\development\Hypertrophy-Toolbox-v3-main\docs\css_phase4_wp4_4\PLANNING.md`, `docs\ai_workflow\QUALITY_GATE.md`, and the actual test surfaces. The packet decomposition, ownership model, and DAG are the strongest I have reviewed in this arc. The **gate set is not yet runnable as written**: several named gates are structurally incapable of failing on the surface they are assigned to.

---

### F1 — `visual.spec.ts` cannot falsify WP4.4-c; the determinism layer deletes motion.css's entire output before the screenshot
**Severity: blocking** · **Location: WP4.4-c Gates; §5 V1**

`prepareForScreenshot()` in `d:\development\Hypertrophy-Toolbox-v3-main\e2e\visual-helpers.ts:41-51` injects globally:

```
*, *::before, *::after {
  animation-delay: 0s !important; animation-duration: 0s !important;
  animation-iteration-count: 1 !important;
  transition-duration: 0s !important; transition-delay: 0s !important;
  backdrop-filter: none !important; -webkit-backdrop-filter: none !important;
}
```

WP4.4-c's declared scope is "transitions, skeleton states, `prefers-reduced-motion` handling." Every one of those is zeroed with `!important` before any pixel is captured. A packet that deleted `motion.css` entirely would produce a byte-identical visual matrix. The packet's primary gate is unfalsifiable on its own surface.

**Recommend:** WP4.4-c gets a bespoke, non-pixel oracle owned by WP4.4-a: a computed-style differential over `transition-property`/`transition-duration`/`animation-name`/`animation-duration` at rest for every element on all rendered routes, captured **without** the determinism style tag, plus forced `prefers-reduced-motion: reduce` **and** `no-preference` runs. Add `e2e/ui-hardening.spec.ts` (toast/modal transition contracts). Demote `visual.spec.ts` for this packet to a non-primary backstop and say so explicitly.

---

### F2 — The determinism layer blinds the pixel oracle to the exact declaration families d, h, i, and j are cleaning
**Severity: blocking** · **Location: §5 V1; WP4.4-d/h/i/j Gates**

Beyond F1, `e2e/visual-helpers.ts` neutralizes, before capture:
- `backdrop-filter` / `-webkit-backdrop-filter` → **none** globally (lines 49-50). The glass families in `components.css` and the `theme-dark.css` rule pinned at `tests/test_css_cascade_contracts.py:1007` (`backdrop-filter: blur(8px) !important;`) are invisible to the oracle. That is h/i/j's core surface.
- `[data-visual-scale-control]` → `background/border-color/color: transparent` (lines 115-119). WP4.4-d's declared scope is "the UI scale system (`data-scale`)."
- `[data-visual-icon]` → `visibility: hidden` (lines 112-114).
- Dark theme only: `[data-visual-surface][data-visual-surface]` → forced `background`, `background-image: none`, `border-color: #273145`, `border-radius: 0`, `box-shadow: none`, `text-shadow: none` (lines 68-75). The dark visual baseline is blind to surface paint on exactly the elements `theme-dark.css` (WP4.4-j) exists to paint.
- All form controls → `border-radius: 0; box-shadow: none; text-shadow: none` (lines 93-101, re-applied inline at 129-138).

**Recommend:** make an **oracle blind-spot register** a named WP4.4-a deliverable — the exact `(selector, property)` pairs neutralized by `prepareForScreenshot()`. Add a per-packet gate obligation: *"no declaration this packet deletes or re-weights falls inside the blind-spot register; where one does, a computed-style differential is supplied in its place."* Without this, M2 ("overpaint-suppressed declarations need a pixel-space differential") is applied as decoration — the pixel space it names is pre-neutralized.

---

### F3 — `maxDiffPixels: 800` means the visual matrix cannot enforce V1's "zero visual differences"
**Severity: blocking** · **Location: §5 V1 pass condition; every packet's "Gates" and "Rollback criteria" row**

`visualScreenshotOptions()` (`e2e/visual-helpers.ts:145-166`) sets `maxDiffPixels: 800, threshold: 0, fullPage: true`. Any packet may change up to 800 pixels per route × viewport × theme and the gate stays green. V1 says "zero visual differences… any diff outside that ledger is a rollback trigger" — `visual.spec.ts` cannot deliver that statement.

Two consequences the plan should state:
1. V1's *primary* instrument must be the packet's own element-scoped differential at `maxDiffPixels: 0` (the harness WP4.4-a builds, consistent with M3), with `visual.spec.ts` as a coarse cross-check.
2. The animated-logo band (1,039 / 1,046 px) sits **above** the 800 tolerance — it is an actual snapshot **failure** of `workout-plan-desktop-dark`, not a diff absorbed by the option. The plan's known-red rows should say that plainly, so nobody "fixes" it by raising `maxDiffPixels` (which would silently destroy the oracle for every other route).

**Recommend:** restate V1 as *"0 diff on the packet-scoped element differential; `visual.spec.ts` reproduces only the ledger reds"*, and add an explicit prohibition on editing `maxDiffPixels`, `threshold`, or `mask` in `e2e/visual-helpers.ts` for the whole arc (that file is currently pinned by `tests/test_visual_selector_contracts.py:11-35`, but only for selector *hooks*, not tolerances).

---

### F4 — `dark-mode.spec.ts` is named WP4.4-j's **primary** gate but asserts zero paint
**Severity: blocking** · **Location: WP4.4-j Gates ("`dark-mode.spec.ts` (**primary**)"); also b, c, d, e, f, h, i where it is named as the theme oracle**

`d:\development\Hypertrophy-Toolbox-v3-main\e2e\dark-mode.spec.ts` (6 tests) asserts only: the `data-theme` attribute flips, the `darkMode` localStorage value, persistence across reload, persistence across `HOME → WORKOUT_PLAN → WEEKLY_SUMMARY → VOLUME_SPLITTER`, and the toggle icon class. There is not one computed-style or pixel assertion in the file. Deleting `theme-dark.css` in its entirety would leave all 6 tests green.

For WP4.4-e it is even weaker: the packet names `dark-mode.spec.ts` as the gate "for the `body.dark-mode` claim" at `layout.css:1120` — a selector the spec never evaluates.

**Recommend:** demote `dark-mode.spec.ts` everywhere from oracle to cheap toggle-mechanics regression (keep it, it costs nothing). WP4.4-j's real dark oracle is the dark half of the visual matrix on all rendered routes **plus** a packet-owned computed-style differential across its 81 top-level rules. WP4.4-e's `body.dark-mode` re-proof (G5) must be a computed-owner + rest-state differential per M1/M5/M6, not a spec run.

---

### F5 — `/fatigue` is painted entirely by the seven shared bundles and has **no** visual coverage; "all 10 routes" undercounts the blast radius
**Severity: blocking** · **Location: Terminology table; V1; WP4.4-b/e/f/h/j/k Gates; §Expected gates**

- `e2e/fixtures.ts:80-91` — `ROUTES` has 10 entries; no `/fatigue`.
- `e2e/visual.spec.ts:9-20` — 10 pages; no fatigue. No baseline exists under either `e2e\__screenshots__\win32\` or `e2e\__screenshots__\linux\`.
- `d:\development\Hypertrophy-Toolbox-v3-main\templates\fatigue.html` contains **no** `.css` link and no `page_css` block — grep for `\.css` returns nothing. It is not in `ROUTE_BUNDLES` (`tests/test_css_cascade_contracts.py:27-38`).

So `/fatigue` is the one route rendered *purely* by the eight globals plus `bootstrap.custom.min.css` — the highest shared-bundle exposure in the app — and it is the one route with zero pixel oracle. Every "all 10 routes" gate in the plan systematically excludes it.

**Recommend:** (i) restate the denominator as **11 rendered routes** (10 bundled + `/fatigue`); (ii) add `e2e/fatigue.spec.ts` (8 tests, includes dark and mobile states) to every implementation packet's e2e set, plus `e2e/fatigue-stage4-smokes.spec.ts` for b/e/f (it asserts mobile geometry and dark contrast — a genuine falsifier for layout/navbar/base); (iii) require WP4.4-a's harness differential to include `/fatigue` in both themes at all three widths; (iv) raise a new owner decision — extending `visual.spec.ts` to `/fatigue` requires **creating** win32 *and* linux baselines, which is baseline creation rather than rebaseline, and `tests/test_visual_selector_contracts.py:38-44` pins matrix membership. Do not let a packet do this under V2's radar.

---

### F6 — AC4's "proven disjoint at the file level" is already false for b–f: the shared contract file pins content inside `navbar.css` and `a11y.css`
**Severity: blocking** · **Location: §4(d) "Shared files"; N1; AC4**

`tests/test_css_cascade_contracts.py` does not merely test page bundles. It pins declarations *inside* the surfaces b–f own:
- **`navbar.css`** — line 140 + 150-152: `--nav-gap: var(--s-3);`, `--nav-padding-y: var(--s-3);`, `--nav-padding-x: 1rem;` (WP4.4-f).
- **`a11y.css`** — lines 871, 906: `assert "*:focus-visible," in a11y` (WP4.4-d).
- **`theme-dark.css`** — lines 957, 1006-1007 (WP4.4-j).
- **`components.css`** — seven separate reads (lines 178, 337, 420, 868, 954, 1296, 1484, 1613) (WP4.4-g/h/i).
- **All bundles** — `test_runtime_bundle_cap_and_route_ownership_are_unchanged` (8 globals) and `test_one_explicit_order_covers_every_existing_layer` (layer blocks exactly `{workout, navbar, workout-dropdowns, welcome}`).

If WP4.4-d or WP4.4-f touches a pinned declaration, it **must** edit `tests/test_css_cascade_contracts.py` — and the plan proposes both as class-(a) concurrent. N1 as framed ("should new contracts go in the shared file?") is the wrong question; the collision comes from *existing* assertions that may need updating, which per-packet files do not avoid.

**Recommend:** add a WP4.4-a deliverable — a **contract-pinned declaration register**: every assertion in `tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py` that reads each of the seven surfaces, with the exact string pinned. Then a per-packet entry condition: *"this packet's scope does not intersect the register, or the packet serializes on the shared file."* That converts AC4's disjointness claim from an assertion into a measurement.

---

### F7 — N1 recommendation (answering the open decision)
**Severity: should-fix** · **Location: N1**

**Adopt per-packet contract files — `tests/test_css_wp4_4_<surface>_contracts.py` — and keep them permanently.** Reasoning:
1. Necessary but not sufficient: it removes *additive* collisions, not the *update* collisions in F6. Pair it with the F6 register.
2. Every packet must still **run** `tests/test_css_cascade_contracts.py` and `tests/test_visual_selector_contracts.py` (they are the cross-file cascade invariants). The rule is *run always, edit never-concurrently* — the plan already says this at §4(d); make it explicit that running is not a claim.
3. **Reject the "WP4.4-k optionally consolidates" clause.** A consolidation is a refactor whose only oracle is "the tests still pass," performed at the exact moment the arc is trying to demonstrate stability, and it re-creates the single shared file the decomposition was designed to avoid. WP4.4-k should assert only that all per-packet contract files exist and are collected.

With F6's register plus per-packet files, the claimed concurrency for b/c/e is real. For **d and f it is conditional** on their scope not intersecting the register.

---

### F8 — WP4.4-i's spec set is wrong twice, in the exact way the Terminology section warns against
**Severity: blocking** · **Location: WP4.4-i Gates step (7); also WP4.4-h Gates**

The plan's own binding terminology says never conflate four and five. WP4.4-i's gate then says "**all five route specs**" — there is no such set. The five affected routes are covered by **four** spec files, because `e2e/summary-pages.spec.ts` covers both Weekly and Session (3 `ROUTES.WEEKLY_SUMMARY|SESSION_SUMMARY` references in that file). WP4.4-h gets this right and enumerates four; WP4.4-i does not, and an implementer told to run "all five route specs" will either guess or stop.

Second and more serious: per `QUALITY_GATE.md` §Frontend feature → E2E map, the `workout_plan` / `workout-plan` hint maps to **three** specs — `workout-plan.spec.ts`, `exercise-interactions.spec.ts`, `superset-edge-cases.spec.ts`. Both h and i omit the latter two. The `:is()` branch `#workout[data-page="workout-plan"]` *is* the Workout Plan page scope, and superset row paint (`--superset-bg-1..4`, `user_selection.superset_group`) is one of its highest-risk families. Omitting them under-tests the branch the whole packet exists to repair.

**Recommend:** replace both with the explicit six-spec set for the five affected routes:
`workout-plan.spec.ts`, `exercise-interactions.spec.ts`, `superset-edge-cases.spec.ts`, `workout-log.spec.ts`, `summary-pages.spec.ts` (Weekly + Session), `progression.spec.ts` — and state "six specs / five routes / four selector branches" so the three counts can never be conflated again.

---

### F9 — The `program-backup.spec.ts:79` known red is never mentioned
**Severity: should-fix** · **Location: known-red rows of WP4.4-j and WP4.4-k; §Expected gates**

`QUALITY_GATE.md:88` lists it as the current baseline exception (DB-state-pollution flake, passes in isolation; CI isolates it in the `e2e-backup` job). Packets j and k run all-route specs and `/verify-suite`, which include it. As written, its appearance would trip V1's "any red not in the ledger blocks the arc close" and trigger a spurious bisect.

**Recommend:** add it to the known-red register with the QUALITY_GATE-mandated handling — record whether it passes in isolation; it is a DB-pollution flake, **not** a CSS signal, and must not trigger a V1 rollback.

---

### F10 — Correctly derived: `nav-dropdown` and `/build-css`
**Severity: nit (positive)** · **Location: WP4.4-f known-red row; §Expected gates**

Both are right and should survive into Plan v2 unchanged:
- The plan states `nav-dropdown.spec.ts` is "no longer a known red since 2026-06-11, so failures block." `QUALITY_GATE.md:90` says exactly that. Any council input asserting a live `nav-dropdown.spec.ts:117` red is stale — do not adopt it.
- "`/build-css` is NOT required — no packet edits `scss/**`" is a correct read of the CSS row, whose glob is `scss/**` only.

---

### F11 — `visual.spec.ts` is deep-gate-only and platform-split; the arc's central invariant has no CI enforcement and the plan never says which baseline set applies
**Severity: should-fix** · **Location: §5 V1/V2; every packet's Gates; §Expected gates**

Per `e2e/CLAUDE.md` §Visual spec contract: visual specs **never** run on the PR path and are never a required check; they run only via the `visual-linux` job in `.github/workflows/deep-gate.yml` behind the `run_visual` `workflow_dispatch` input on pinned `ubuntu-24.04`. Baselines are split — both `e2e\__screenshots__\win32\visual.spec.ts-snapshots\` and `e2e\__screenshots__\linux\visual.spec.ts-snapshots\` exist and are maintained independently.

Consequences the plan must state: (a) a packet run locally on Windows proves nothing about the Linux baselines, and vice versa; (b) no packet's V1 gate will be enforced by any required CI check, so "the visual matrix is green" is a claim about one developer's machine unless the deep gate is dispatched.

**Recommend:** name the deep-gate dispatch as an explicit gate on **h, i, j, k** at minimum (the packets that can move five-or-more routes), state that b–f run the win32 matrix locally, and raise it as an owner decision: per-packet Linux deep-gate run, or once at k?

---

### F12 — V2 ("no rebaseline") and R3 condition 6 ("rollback not rebaseline") are honour-system; nothing makes an accidental rebaseline hard
**Severity: should-fix** · **Location: §5 V2; WP4.4-i Rollback criteria**

The question asked was whether a rebaseline is the path of least resistance. For WP4.4-i it currently **is**: the packet's failure mode is a visual diff, `--update-snapshots` makes it disappear in one command, and the only thing stopping it is a prose invariant. Everything else in this plan is mechanized; this is not.

**Recommend:** two mechanical guards, both cheap:
1. A contract in WP4.4-a's new test file asserting a manifest (sorted relative paths + sizes, or a directory hash) over `e2e/__screenshots__/win32/**` and `e2e/__screenshots__/linux/**` — so any `--update-snapshots` run turns a pytest **red** rather than turning a Playwright test green.
2. A per-packet PR gate: `git diff --name-only <base>...HEAD` must show zero paths under `e2e/__screenshots__/` and zero changes to `e2e/visual-helpers.ts`.

With (1), V2 and R3-6 become enforced rather than promised.

---

### F13 — "No later packet may inherit a projection as fact" is prose, not a gate
**Severity: should-fix** · **Location: line 342; V5; WP4.4-a "Expected movement"**

Correctly identified as the risk; not converted into anything checkable. As written, WP4.4-a writes a markdown evidence doc and packets b–k are trusted to read it.

**Recommend:** WP4.4-a additionally emits **`docs/CSS_PHASE4_WP4_4_A_BASELINE.json`** — per-surface line counts, `!important` **occurrence** counts, per-rule Stylelint counts, exact `@layer` open/close spans, the F2 blind-spot register, the F6 contract-pinned register, and a `sourceCommit`. Add a contract `test_wp4_4_baseline_is_pinned_and_matches_disk` asserting the file exists, parses, and its per-surface line counts equal the files on disk at that commit — mirroring the existing `test_stylelint_is_pinned_measure_only_with_committed_baseline` pattern at `tests/test_css_cascade_contracts.py:155-173`. Every packet b–k cites that JSON; a packet quoting a number absent from it fails its evidence gate.

---

### F14 — V3/V4 use pre-WP4.3 numbers as pass thresholds
**Severity: should-fix** · **Location: §5 V3 and V4**

V4 states the thresholds as "`no-duplicate-selectors` (86 at baseline)" and "`declaration-block-no-duplicate-properties` (8 at baseline)". Those come from `docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json`, pinned at commit `9ee7638` with `warningCount` 7202 (asserted at `tests/test_css_cascade_contracts.py:171-172`) — a commit that predates the entire WP4.3 arc. The plan's own §Assumptions notes the current global total has moved to 5,490. So the invariant table itself inherits a stale figure as fact, which is the exact failure mode line 342 warns about.

**Recommend:** V3/V4 compare against the **WP4.4-a measure baseline**; the WP4.1 JSON is retained only as the immutable historical anchor for the arc-level report at k. State this explicitly so no packet trips a threshold that is two arcs old.

---

### F15 — `!important` is counted in two different units inside the same invariant
**Severity: should-fix** · **Location: Problem table (line 116-123) vs §5 V3**

The Problem table is honestly footnoted: "`!important` figures are `rg --count` **line** counts, not occurrence counts." V3 then gates on "`declaration-no-important` does not rise" — a Stylelint **occurrence** count. A single line with two `!important` declarations moves one metric and not the other; a packet could satisfy V3 while the plan's headline 1,264 figure is unchanged, or vice versa.

**Recommend:** WP4.4-a normalizes all `!important` reporting to Stylelint occurrence counts, records both, and the Problem table's line counts are marked non-authoritative.

---

### F16 — No packet requires a red-path proof for the contract it adds; every new contract is self-confirming by construction
**Severity: should-fix** · **Location: WP4.4-b through WP4.4-j "Test/evidence paths owned"**

Each packet authors `tests/test_css_wp4_4_<surface>_contracts.py` *after* making its change, asserting the post-change text. Such a test passes trivially and proves nothing about whether it would catch a regression. This arc already has the corrective habit — WP4.3i-g locked its invariant with a proven-failing contract — but the plan does not carry it forward as an obligation.

**Recommend:** add to every implementation packet's gate: *"the new contract is proven to fail — restore one deleted declaration (or invert one asserted invariant), record the observed failure output in the evidence doc, revert."* One line per packet; it is the only thing that distinguishes a contract from a transcript.

---

### F17 — The "deletions commute" theorem covers deletion only, but b–f's stated scopes exceed deletion
**Severity: should-fix (upgrades to blocking if b–f may do more than delete)** · **Location: §4 "Why file-level disjointness is sufficient"**

The commutation argument rests on M8: only proven **non-winners** are deleted, and a non-winner's removal cannot move a computed value while its winner remains. Sound — for deletion. But WP4.4-d's scope includes reducing 51 `!important` lines and WP4.4-f's includes consolidating "three live generations." Both can **re-weight a winner** without deleting a non-winner, and a re-weight in `a11y.css` (loads last of the pre-page shared bundles) can change which `navbar.css` rule wins. M8 does not foreclose that, so the concurrency proof does not cover d+f running concurrently.

**Recommend:** restrict class-(a) concurrency to **pure deletion of proven non-winners**. Any re-weighting, selector rewrite, or generation-consolidation in b–f reclassifies that packet to class (c) sequential, or splits it into a concurrent deletion half and a sequential re-weight half. State the restriction in §4 so the theorem's precondition is visible.

---

### F18 — Visual matrix size is stated inconsistently; the canonical count in `.claude/rules/testing.md` is stale
**Severity: nit** · **Location: WP4.4-b Gates ("all 6 variants"); WP4.4-j; §Expected gates**

`e2e/visual.spec.ts:9-28` produces 10 pages × 3 viewports × 2 themes = **60** tests (6 variants *per page*). `.claude/rules/testing.md` still records `visual.spec.ts | 48 | Eight-page viewport/theme screenshot matrix` — two pages stale. A packet that "confirms the full matrix ran" against 48 will silently miss two routes.

**Recommend:** write "`visual.spec.ts` — full matrix (10 pages × 3 viewports × 2 themes)" everywhere, and have WP4.4-a re-measure `npx playwright test --list --project=chromium` and flag the `.claude/rules/testing.md` correction (an AI-workflow-doc change; self-review gate, separate from any CSS packet).

---

### F19 — `accessibility.spec.ts` is omitted from WP4.4-b and WP4.4-e, the two packets whose surfaces it actually measures
**Severity: should-fix** · **Location: WP4.4-b and WP4.4-e Gates; §Expected gates line "accessibility.spec.ts (d, c, f, h, i, j, k)"**

`e2e/accessibility.spec.ts:358-395` evaluates computed `color`, `backgroundColor`, and `textDecoration` on body text and links — precisely what `base.css` owns ("element defaults, app background, baseline typography"). Its tap-target and skip-link geometry assertions depend on `layout.css` shell spacing. These are two of the very few genuine computed-style falsifiers in the whole e2e suite, and they are assigned to every packet except the two they best fit.

**Recommend:** run `accessibility.spec.ts` (24 tests, cheap) on **every** implementation packet b–j.

---

### F20 — WP4.4-a's own gate omits the Stylelint run it exists to produce
**Severity: nit** · **Location: WP4.4-a Gates**

The gate row lists pytest and harness self-checks; the "Expected movement" row promises the true per-surface counts. Add the command. Note the script is `"lint:css": "stylelint \"static/css/**/*.css\" \"scss/**/*.scss\""` (`package.json:8`) — it **includes SCSS**, so any packet-level delta must be filtered to the seven surfaces or SCSS noise will move the total and confound V3/V4.

---

### F21 — `QUALITY_GATE.md` has no row for `static/css/**`; the arc's entire routing is inferred, not derived
**Severity: should-fix** · **Location: §Expected gates; New owner decisions**

The change-type table's CSS row globs `scss/**` only. Route/DB/business-logic/template/JS rows do not match `static/css/*.css` either. The only hook is the feature map's last line, "broad layout or CSS visual changes → `visual.spec.ts`." So every gate in this plan is a reasonable inference rather than a derivation from the canonical file — which is also why the review question "is any gate invented?" is hard to answer definitively.

**Recommend:** add **N6** — WP4.4-k adds a `static/css/**` row to `docs/ai_workflow/QUALITY_GATE.md` recording the routing this arc settles on (shared bundle → all-route matrix + fatigue + the blind-spot caveat; page bundle → that route's feature-map specs). It is an AI-workflow-doc change (self-review gate per that same table), needs owner sign-off since `docs/ai_workflow/**` is a never-claimed shared path, and it is the most durable artifact this arc can leave behind.

---

### Falsifiability, per packet

| Packet | Can its gates fail if the packet is wrong? |
|---|---|
| **a** | **Yes.** Harness self-checks (same-CSS control 0 diff, resolution self-check, M4 unit-check, M6 sentinel-took-effect) are genuine red paths. Best-constructed gate in the plan. |
| **b** | **Weakly.** 800px tolerance (F3) + no `accessibility.spec.ts` (F19). Fix both → yes. |
| **c** | **No.** Structurally unfalsifiable on its own surface (F1). Blocking. |
| **d** | **Partly.** `accessibility.spec.ts` is a real oracle; the scale-control surface is pixel-blind (F2). |
| **e** | **Yes.** The 14-width breakpoint sweep is the best-specified gate here; add `volume-progress.spec.ts` (±1px geometry) and `fatigue-stage4-smokes.spec.ts` (overflow booleans) as ready-made layout falsifiers. |
| **f** | **Yes.** `nav-dropdown.spec.ts` is a real, now-blocking oracle; the band handling is correct. |
| **g** | **Yes.** Controls invalidate the audit (M5) and block h. Correct. |
| **h** | **Yes** — "0 computed-value and 0 declaration-owner differences, positive controls showing records losing candidates and 0 gaining" is the strongest single gate in the document. Only the spec list needs F8. |
| **i** | **In principle yes**, but the spec set is wrong (F8) and the rollback discipline is unenforced (F12). |
| **j** | **No**, as written — its named primary asserts no paint (F4) and its surface is pixel-blind in dark (F2). |
| **k** | **Only if the visual matrix actually runs** on a platform whose baselines are current (F11). |

---

## Verdict

**blocking** — six defects (F1, F3, F4, F5, F6, F8) must be resolved before Gate 1. The decomposition, DAG, ownership model, M1–M8 method encoding, and R3 sequencing are sound and unusually rigorous; the failures are concentrated in *which instruments were selected to prove it*. Three named gates (`visual.spec.ts` for motion, `dark-mode.spec.ts` for theme-dark, "all five route specs" for the `:is()` repair) cannot execute or cannot fail on the surface they are assigned to, and one rendered route (`/fatigue`) is invisible to every gate in the plan.

---

## Expected gates — consolidated for Plan v2

**Standing rules (apply to every implementation packet b–j):**
- Run, never concurrently edit: `tests/test_css_cascade_contracts.py`, `tests/test_visual_selector_contracts.py`.
- Red-path proof recorded for every new contract (F16).
- `git diff --name-only <base>...HEAD` shows zero paths under `e2e/__screenshots__/` and zero changes to `e2e/visual-helpers.ts` (F12).
- Stylelint: `npm run lint:css`, delta filtered to the seven surfaces, compared to `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` — **not** the WP4.1 JSON (F13, F14, F20).
- Known reds: WP4.0 ledger; animated logo as a **band** (M7, and note it exceeds `maxDiffPixels: 800`); `program-backup.spec.ts:79` DB-pollution flake — record isolation result, never a V1 rollback trigger (F9).
- `/build-css` **not required** (no `scss/**` edits) — correct as planned.

| Packet | pytest | e2e (Chromium) | other |
|---|---|---|---|
| **a** | `tests/test_css_cascade_contracts.py`, `tests/test_visual_selector_contracts.py` | none (read-only); harness self-checks incl. `/fatigue` | `npm run lint:css`; emit `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` + blind-spot register (F2) + contract-pinned register (F6) + snapshot-manifest contract (F12) |
| **b** base | + `tests/test_css_wp4_4_base_contracts.py` | `visual.spec.ts` (full 60), `smoke-navigation`, `dark-mode`, `accessibility`, `fatigue` | Stylelint delta |
| **c** motion | + `tests/test_css_wp4_4_motion_contracts.py` | `ui-hardening`, `accessibility`, `smoke-navigation`, `fatigue`; `visual.spec.ts` as backstop only | **Bespoke motion oracle** (F1): computed `transition-*`/`animation-*` differential without the determinism tag + forced `reduce` **and** `no-preference` |
| **d** a11y | + `tests/test_css_wp4_4_a11y_contracts.py` | `accessibility` (**required**), `nav-dropdown`, `ui-hardening`, `visual.spec.ts` (full), `smoke-navigation`, `fatigue` | Per-`data-scale` captures; computed-style differential for scale controls (pixel-blind, F2) |
| **e** layout | + `tests/test_css_wp4_4_layout_contracts.py` | `visual.spec.ts` (full), `accessibility`, `volume-progress`, `fatigue-stage4-smokes`, `smoke-navigation`, `summary-pages`, `workout-log`, `workout-plan`, `fatigue` | 14-width breakpoint sweep, element-scoped per M3; `body.dark-mode` re-proof per M1/M5/M6 (**not** `dark-mode.spec.ts`) |
| **f** navbar | + `tests/test_css_wp4_4_navbar_contracts.py` | `nav-dropdown` (**required, blocking**), `smoke-navigation`, `accessibility`, `dark-mode`, `visual.spec.ts` (full), `fatigue` | Collapsed/expanded × both themes, element-scoped (M3); logo band |
| **g** audit | contract files only | none (read-only) | Records audited commit; M4/M5/M6 controls |
| **h** components | **full `pytest`** (`/verify-suite` pytest half) | `workout-plan`, `exercise-interactions`, `superset-edge-cases`, `workout-log`, `summary-pages`, `progression`, `visual.spec.ts` (full), `accessibility`, `nav-dropdown`, `ui-hardening`, `fatigue`, `smoke-navigation` | 0 computed-value / 0 owner differences + positive controls; deep-gate `visual-linux` dispatch (F11) |
| **i** `:is()` repair | **full `pytest`** | same six-spec five-route set as h (F8) + `visual.spec.ts` (full), `accessibility`, `nav-dropdown`, `fatigue` | R3 1–8; regions A–C before/after; pre-change would-become-winner inventory across 5 routes × 2 themes × 3 widths; deep-gate `visual-linux`; **rollback, never rebaseline** — enforced by the F12 manifest contract |
| **j** theme-dark | **full `pytest`** | `visual.spec.ts` (full, dark half is primary), all 11 rendered routes' specs incl. `fatigue`; `dark-mode` demoted to mechanics-only (F4) | Dark computed-style differential over all 81 rules × 11 routes; deep-gate `visual-linux` |
| **k** integration | `/verify-suite` (full pytest) | `/verify-suite` full Chromium set + deep-gate `visual-linux` (`run_visual`) | Full Stylelint re-measure vs WP4.1 anchor **and** the a-baseline; V4 monotonicity across the arc; V5 contribution + shortfall vs 30,768; final `:is()`-aware ownership differential = 0; per-packet contract files all collected (F7); N6 `QUALITY_GATE.md` row (F21) |

**New owner decisions this review adds:** (N6) add a `static/css/**` row to `docs/ai_workflow/QUALITY_GATE.md` at k; (N7) extend `visual.spec.ts` to `/fatigue` — baseline *creation* on both platforms, requires updating `tests/test_visual_selector_contracts.py:38`; (N8) is a Linux deep-gate `visual-linux` run required per packet, or once at k?

---

### product-risk-reviewer (agent `a398c39b3f311bfd1`)

### product-risk-reviewer — findings on Plan v1 (`docs/css_phase4_wp4_4/PLANNING.md`)

---

**1. Calculation surface `none` — VERIFIED, claim is correct.** — *nit (confirmation only)*
Location: Section 0 "Calculation surface"; all packet rows.
Every packet's "Production paths owned" is either `none`, a single `static/css/*.css`, or docs. No packet reaches `utils/effective_sets.py`, `utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py`, `utils/volume_*.py`, `utils/fatigue*.py`, any `routes/*.py`, any response shape, or any DB byte (`data/database.db` + sidecars and `data/auto_backup/` are explicitly per-worktree, never staged, §4d). The new `tests/test_css_wp4_4_*_contracts.py` files are CSS contract tests, not calculation tests. The `none` claim stands as written; no migration notes are owed under CLAUDE.md §1 "Refactor invariant". Backup contract is likewise untouched — no schema change, so existing `program_backup` snapshots stay restorable.

---

**2. The "all 10 routes" visual matrix omits the two routes that shared CSS paints 100% of.** — *blocking*
Location: §5 V1; gate rows for WP4.4-b/c/d/e/f/h/j/k; the repeated phrase "all 10 routes".
`e2e/visual.spec.ts:9-20` covers exactly ten pages: welcome, workout-plan, workout-log, weekly-summary, session-summary, progression, body-composition, volume-splitter, user-profile, backup. Two user-facing routes are missing, and they are the *worst* possible ones to miss here:
- `templates/fatigue.html` (`GET /fatigue`, `fatigue_bp`) has **no `{% block page_css %}` at all** — it is painted entirely by the seven bundles this arc rewrites, plus `tokens.css` and the SCSS-built Bootstrap.
- `templates/error.html:5-6` has an **empty** `page_css` block — same situation.

The plan's "10 routes" figure is inherited from the ten *route bundles* in `.claude/rules/frontend.md`, not from the app's route set. Result: the packets with the largest blast radius have zero visual baseline on the surface where their blast radius is total. A shared-bundle regression on the Fatigue meter page would ship unseen.
**Fix:** replace "all 10 routes" with an explicit route list that includes `/fatigue` and the error page, and add `e2e/fatigue.spec.ts` + `e2e/fatigue-stage4-smokes.spec.ts` to the gate set of every shared-bundle packet (see finding 7). If a visual baseline for `/fatigue` does not exist, WP4.4-a must record that gap rather than let downstream packets inherit an unstated blind spot.

---

**3. The `.value-changed` three-colour family is semantically load-bearing and invisible to every oracle the plan defines.** — *blocking*
Location: method rules M1–M8; WP4.4-h and WP4.4-j scope/gates.
This family encodes *which* field the user just edited, using colour as the sole carrier:

- `static/css/components.css:995-1013` (light) — pink `#ec407a` = rep range, green `#66bb6a` = **RIR/RPE**, yellow `#fdd835` = weight/sets.
- `static/css/theme-dark.css:565-582` (dark) — the same three-colour scheme, all `:where(...)` selectors, i.e. **specificity (0,0,0)** carried entirely by `!important`.
- Reduced-motion arms at `components.css:1016-1035` and `theme-dark.css:585-591`, where the box-shadow is stripped and `border-color` becomes the *only* remaining signal.

`.value-changed` is added by JS on edit. It appears in no screenshot, no rest-state differential, and no same-CSS control. M1 requires "sentinel sweep AND rest-state differential AND same-CSS control" — all three are rest-state oracles, so the method as written returns *dead* for this entire family, in both `components.css` (WP4.4-h) and `theme-dark.css` (WP4.4-j). A near-zero-specificity `:where()` rule is exactly what a specificity-based owner audit will also mis-rank. The user-visible outcome is the loss of edit feedback on Workout Plan inputs — worst in dark mode, worst again under reduced motion, where three distinguishable states flatten into one.
**Fix:** add a method rule M9 — *a declaration reachable only through an interaction state or a JS-applied class is non-deletable unless proven under that state*; and name `.value-changed` (all six rule blocks above) as a must-retain family in WP4.4-h and WP4.4-j exclusions until such a proof exists.

---

**4. Media-query-conditional accessibility rules are structurally mis-classifiable, and only one packet guards against it.** — *blocking*
Location: WP4.4-c / -d / -j gate rows; method rules M1–M8.
`static/css/motion.css:15-22` is the app's entire reduced-motion commitment — a global `*, *::before, *::after { animation: none !important; transition: none !important; }`. It never fires under a default browser profile, so a sweep, a rest-state differential and a same-CSS control all agree it is dead. Same failure mode at:
- `static/css/a11y.css:422` — `@media print` (invisible to any screen capture).
- `static/css/theme-dark.css:585-591` — dark-mode reduced-motion arm.
- `static/css/a11y.css:386` — `@media (max-width: 991.98px)`.

WP4.4-c is the only packet with a forced `prefers-reduced-motion: reduce` capture. WP4.4-d has no print emulation and no breakpoint sweep (only WP4.4-e has one). WP4.4-j has no reduced-motion capture despite owning a reduced-motion block. Reduced motion is an accessibility commitment, not decoration; silently dropping it is a product defect.
**Fix:** make it a global obligation (a new M-rule, not a per-packet note): *no declaration inside an `@media` block may be classified dead without a capture taken under that block's own condition* — and add `emulateMedia({ reducedMotion: 'reduce' })` to WP4.4-j, `emulateMedia({ media: 'print' })` + a breakpoint sweep to WP4.4-d.

---

**5. Custom-property remap blocks are invisible to computed/pixel oracles — WP4.4-j's central triage rests on the one thing the method cannot see.** — *should-fix*
Location: WP4.4-j "legacy value vs justified token remap"; M6.
`static/css/theme-dark.css:597-621` is a pure custom-property block remapping `--bg-primary`, `--bg-secondary`, `--text-primary`, `--text-secondary`, `--border-color`, `--card-bg`, `--input-bg`, `--table-stripe`, `--hover-bg`, the six `--glass-*` tokens, `--bs-body-bg` and `--bs-body-color`. A custom-property declaration "wins" nothing paintable; it is only observable through consumers that may live on a route or a state outside the sweep matrix. M6 correctly records that `var()`-bearing shorthands are invisible to longhand CSSOM queries, but says nothing about custom-property *declarations* themselves. Deleting one of these as a "legacy value" collapses dark mode for every unmatched consumer — a dark-mode-only degradation that the light-mode half of the visual matrix cannot surface at all.
**Fix:** extend M6 — *a custom-property declaration is proven dead only by an exhaustive repo-wide `var(--name)` consumer search plus route coverage for every consumer found*; and mark `theme-dark.css:597-621` as retained-by-default in WP4.4-j, with per-property deletion requiring that proof.

---

**6. R2 deferral is expressible, but WP4.4-i and WP4.4-j can move the superset gap without touching `pages-workout-plan.css`.** — *should-fix*
Location: G4; WP4.4-i step 2 (R3 condition 4); WP4.4-j gates.
The gap is real and the deferral is the right call, but "record it; change nothing" is not automatically true for the *other* packets:
- `pages-workout-plan.css:3551-3569` sets `tr.superset-group-N { background-color: var(--superset-bg-N) !important }` at (0,1,1). The `:is()` family paints the **cell** — `components.css:3368` (`tbody td`, `--surface-2` at 72%) and `:3400` (dark, `--surface-2` at 74%). The superset tint therefore already survives only as the ~26-28% that shows through. Lowering the `:is()` specificity in WP4.4-i changes which rule owns that cell background, i.e. changes how much superset tint shows through on Workout Plan **in both themes** — a visible change to a deferred surface, produced by a packet that never opens `pages-workout-plan.css`.
- WP4.4-j's remaps of `--surface-2` / `--card-bg` / `--table-stripe` change the dark composite over the same tint.

And it is unverifiable by the planned gates: `e2e/scripts/build_visual_seed.py:111-153` never writes `superset_group`, so **`tr.superset-group-*` renders in zero committed screenshots, in either theme.** Superset grouping is a real product concept (two exercises linked for back-to-back performance) and this arc has no way to see it.
**Fix:** (a) restate G4 as "record it; and treat any change in superset row rendering as a rollback trigger", (b) name `tr.superset-group-1..4` explicitly in WP4.4-i's R3 condition-4 would-become-winner inventory, and (c) require WP4.4-i and WP4.4-j to capture Workout Plan with at least one linked superset present, in both themes — a scoped element capture, not a new committed baseline (so R2's "no rebaseline" holds).

---

**7. Required-CI specs that guard exactly this arc's risk surface are absent from every gate list.** — *should-fix*
Location: "Expected gates"; per-packet gate rows.
Missing entirely from the plan:
- `e2e/fatigue-stage4-smokes.spec.ts` — required CI, and its Item 5 captures the fatigue badge's **dark-mode background and text colour across bands** plus 375px overflow. It is the single best automated guard against a dark-token change flattening badge states, and it runs on a route with no page bundle. Adding it is *not* resuming the parked fatigue Stage-4 workstream — it protects it.
- `e2e/fatigue.spec.ts` — page, periods, empty/mobile/dark states.
- `e2e/summary-pages.spec.ts` — currently gated only on h/i/j/k. Its 20 tests are the only automated proof that **Effective Sets and Raw Sets render side-by-side** with the contribution-mode control. `base.css`, `layout.css`, `a11y.css` and `navbar.css` all paint those pages too.
**Fix:** add `summary-pages`, `fatigue` and `fatigue-stage4-smokes` to the gate set for WP4.4-b/c/d/e/f, and keep them through h/i/j/k.

---

**8. V1 leans on a spec that never runs on the PR path and has platform-split baselines.** — *should-fix*
Location: §5 V1; every packet's "Rollback criteria".
`visual.spec.ts` is manual-deep-gate only, `if:`-gated, and explicitly never a required check; Windows baselines live under `e2e/__screenshots__/win32/`, Linux under `linux/`, maintained independently. So "zero visual differences beyond the WP4.0 ledger" is enforced only by a local Windows run that the plan must *mandate*, and Linux-only drift stays invisible until someone dispatches the deep gate. The WP4.0 ledger itself shows the two platforms disagree substantially (1 persistent Windows red vs 11 persistent Linux reds).
**Fix:** state per packet that the Windows visual matrix must be run locally and its result recorded in the evidence doc, and make WP4.4-k's gate include a dispatched `visual-linux` compare run reconciled against the WP4.0 Linux ledger — not just the Windows one.

---

**9. WP4.4-d's a11y protection guards one half of a two-rule focus contract.** — *should-fix*
Location: WP4.4-d "Explicit exclusions".
The guarantee is not carried by any single rule. `a11y.css:439-497` **suppresses** `:focus` outline and box-shadow globally with `!important` across ~55 selectors; `a11y.css:500-514` **restores** a ring for `:focus-visible` only; `a11y.css:520-571` **re-suppresses** at every `html[data-scale="1..5"]`. Deleting the restore half loses keyboard focus visibility app-wide; deleting a suppression half changes rendering everywhere. The plan's guard ("do not weaken any focus-visible or skip-link rule to reduce `!important` count") protects only the restore half, and is prose rather than a gate. `e2e/accessibility.spec.ts:262-266` already asserts outline-or-box-shadow on one focused element — the seed of the right contract, but not parameterised over `data-scale` or theme, which is precisely where `a11y.css` differs.
**Fix:** make `tests/test_css_wp4_4_a11y_contracts.py` assert the *guarantee* — a computed non-`none` outline on a keyboard-focused control at every `data-scale` level, in both themes, plus the skip-link becoming visible on first Tab — so the protection survives any rule-text refactor rather than depending on reviewer vigilance.

---

**10. The "interaction states are uncertifiable" lesson from WP4.3i-dead is not in M1–M8.** — *should-fix*
Location: §2b method rules.
The ten frozen Workout Plan declarations exist *because* a same-CSS control on interaction states produced 52 diffs and the packet shrank 24→14. M1–M8 record the sentinel/control/pixel lessons but not this one. It matters directly here: the `:is()` family carries hover paint at `components.css:3381` and `:3409`, and WP4.3j-d already deleted hover paint on Workout Log. WP4.4-h re-runs that risk at 5,345 lines.
**Fix:** add the rule verbatim to §2b, and have WP4.4-h state up front whether hover/focus/active declarations are in or out of its deletion scope. Standing constraints G6/G7/G8 are otherwise correctly carried; note G7 would be safer as "do not modify **or invalidate**" the WP4.3i-c Page Header contract, since a shared-bundle change can break it without editing `pages-workout-plan.css` — the per-packet `test_css_cascade_contracts.py` gate already catches this, so this is wording only.

---

**11. Non-goals and local-first: clean. One measurement caveat.** — *nit*
Location: Problem statement load-order diagram; WP4.4-a.
No packet introduces auth, cloud sync, a remote DB, or telemetry. `templates/base.html` is frozen by R4, so the three pre-existing externals are untouched by construction: Google Fonts (`base.html:11-13`), FontAwesome cdnjs (`:16`), and the jsdelivr Bootstrap `onerror` fallback (`:15`). No new dependency or network call is proposed. Two small things:
- The load-order diagram cites `templates/base.html:14-28` and so silently omits the Google Fonts stylesheet at `:13` and the jsdelivr fallback at `:15`. Neither changes the cascade, but the diagram is presented as the verified model — say what was excluded and why.
- More materially for the harness: CDN availability changes rendering (Inter vs system-font metrics; a failed FontAwesome load collapses icon-only affordances). A pixel differential or same-CSS control taken online and re-taken offline will disagree for reasons unrelated to CSS. Given this is a local-first app the user may well run offline.
**Fix:** WP4.4-a pins and records the network state (and whether the jsdelivr fallback fired) in every evidence doc, so downstream differentials are comparable.

---

**12. Terminology: clean.** — *nit (confirmation only)*
No packet changes user-visible text; the plan proposes no copy at all. `RIR`/`RPE` appear only as element IDs (`input#rir`, `input#rpe`), never as prose. The plan's own glossary terms ("Selector branch", "Affected route") do not collide with any canonical term, and its insistence that "four contexts" is never a synonym for "five routes" is the right instinct. No CountingMode / ContributionMode / Routine / Movement pattern / Superset string is restated or rebranded.

---

**13. The shortfall framing is honest; one residual incentive to close.** — *should-fix*
Location: "⚠️ Honest projection against the Phase-4 target (V5)"; per-packet "Expected movement".
The 2.6–6.8%-of-30,768 figure is derived, not asserted, the denominator is anchored to the WP4.1 inventory, and V5/V6/AC13 correctly order cascade correctness above line count. No packet's rollback criteria reward line count — every one is visual, Stylelint or contract based. That ordering is genuinely enforced. The residual gap: each packet row's **only quantified target** is its "Expected movement" range (`−150 to −400` for navbar, `−300 to −900` for components), which the plan itself admits is an unverified projection. An implementer landing −20 against a projected −150 will read that as failure and look for more to delete.
**Fix:** state once, next to the ⚠️ banner, that expected-movement figures are *measurements to be corrected, never acceptance criteria*, and that under-delivery against a projection is never grounds to widen a packet's scope or relax M8.

---

**Verdict: blocking** — findings 2, 3 and 4 must be resolved in Plan v2. None is a calculation or non-goal violation; all three are gate-completeness gaps where the plan's own method would classify live, user-visible CSS as dead (semantic edit-feedback colour, reduced-motion and print accessibility rules) on surfaces the planned gates cannot see (`/fatigue`, the error page, interaction states, superset rows). Each is fixable with a method rule and a gate-list addition, not a re-plan; the packet decomposition, ownership model and DAG are sound.

---

## Response matrix

**49 findings, 49 rows. No finding is rejected. Nothing is deferred, so no `MASTER_HANDOVER.local.md` note is owed.** Four dispositions are **accept-with-narrowing** (A14, F5's baseline-creation sub-item, F21, product-risk #6's capture method); the narrowing is stated in the Action column and originates with the manager's synthesis, not with me.

**Triangulated findings — independently reached by two reviewers, and therefore weighted highest:** `/fatigue` blind spot (F5 + PR#2) · contract-anchor gap (A8 + F6) · custom-property hole in the commutativity theorem (A5 + PR#5) · platform-split/deep-gate-only visual enforcement (F11 + PR#8).

| Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|
| A1 — WP4.4-i cannot pass the shipped j-c-dead contract that pins the literal four-branch string (`tests/test_css_cascade_contracts.py:1614-1627`); red by construction | architecture-reviewer | **accept** | New owner decision **N6**. WP4.4-i gains a **serialized single-writer claim** on `tests/test_css_cascade_contracts.py`, with the amendment restricted to re-expressing the same *premise* (the shared rule still out-specifies the page-local Workout Log families) — never deleting the assertion. Recorded in i's owned-evidence row and §4(d). |
| A2 — repair *shape* unspecified; two plausible shapes need `templates/**` or `static/js/**` that i does not own | architecture-reviewer | **accept** | New owner decision **N9**. Plan v2 enumerates the four admissible repair shapes with the complete production-path set each requires; any shape needing a template or JS change is **escalated as a separate owner-gated packet, never absorbed**. R3 condition 2's inventory selects among the enumerated shapes. |
| A3 — i can resurrect the ten frozen WP4.3i declarations without editing them; G6 is *do-not-edit*, not *do-not-resurrect* | architecture-reviewer | **accept** | R3 condition 2 extended with a **named sub-list**: the ten frozen declarations, Workout Log regions A–C, and the region-C hover rule (`tests/test_css_cascade_contracts.py:1644-1649`) each individually proven to remain non-winners. Any becoming a winner is a **rollback trigger**. G6 reworded to "do not reopen **or resurrect**". |
| A4 — two worktrees cannot run Playwright concurrently; `PW_REUSE_SERVER=1` yields a false-green V1 | architecture-reviewer | **accept** | §4 gains an arc-wide **E2E serialization rule**: only one worktree runs Playwright at a time; `PW_REUSE_SERVER` must be **unset** in every packet worktree; every packet worktree is created `-Seed visual`. `playwright.config.ts` is added to §4(d) as never-edited. |
| A5 — commutativity theorem has custom-property and shorthand/longhand holes | architecture-reviewer | **accept** (merged with PR#5 into one rule) | New **M9**: the oracle's property universe must be longhand-complete, and **no packet may delete a custom-property declaration under the non-winner rule**; removal requires a repo-wide `var()` dependency graph across all 21 hand-maintained sources. |
| A6 — `@layer` characterisation wrong for `!important`; M4 omits layers | architecture-reviewer | **accept** | Section 0 Problem sentence corrected and scoped to *normal* declarations, with the importance inversion spelled out. **M4 extended** to require layer ordering *and* the importance inversion, unit-checked against hand-computed cases. |
| A7 — f can delete the single-sourced `@layer navbar` block and make `test_one_explicit_order_covers_every_existing_layer` unsatisfiable | architecture-reviewer | **accept** | New **G11**: no packet may delete the last `@layer <name> { … }` block for any name in the `tokens.css:2` order list. Named in f's exclusions so the ceiling is known before the packet starts. |
| A8 — WP4.4-a produces no contract-anchor inventory; six further anchors bind b–j | architecture-reviewer | **accept** (merged with F6) | WP4.4-a gains a single combined deliverable: the **contract-anchor + pinned-declaration register**. A `CD` edge is added from **a** to every implementation packet. |
| A9 — G3 binds only i, but h can change shared ownership by deleting inside a four-branch rule | architecture-reviewer | **accept** | h's exclusion restated at **declaration granularity**: no declaration inside the twelve four-branch rules or the `:4433` rule may be deleted by h; the whole family belongs to i. **G3 extended to bind h.** |
| A10 — `:4433` has three branches, not four, and sits in `@media (prefers-reduced-motion: reduce)` | architecture-reviewer | **accept** | Factual correction applied to the Terminology table and G1: the family is **twelve four-branch rules plus one three-branch reduced-motion rule**. The Weekly/Session reduced-motion asymmetry is recorded as a **finding**, and i's exclusions require preserving it unless separately approved. WP4.4-a enumerates and classifies all **19** `:is(` occurrences (count verified). |
| A11 — the harness lives under gitignored `/artifacts/`, so the PE edges are unsatisfiable | architecture-reviewer | **accept** | Harness **committed** under `scripts/css_audit/` (precedent: `scripts/stylelint-report.mjs`); generated captures/reports stay in gitignored `artifacts/wp4_4/`. `scripts/css_audit/` added to §4(d) as a single-writer shared path. |
| A12 — three DAG defects: missing `b…f → g`; `b…f → i` in prose only; c is oracle-affecting | architecture-reviewer | **accept** | DAG rebuilt: **g is advisory-nomination-only and h re-runs full classification** for every nominated family (rather than adding the edge); the missing `b…f → i` edge added; **c is scheduled first** in the concurrent set; re-proof after rebase is defined as a **full re-capture**, not a delta against recorded line numbers. Redundant `a → f` dropped; `FI` edge type added. |
| A13 — AC1 self-violated: `components.css` claimed exclusively by both h and i | architecture-reviewer | **accept** | AC1 restated: "no two **concurrently eligible** implementation packets own the same production path; where a path is claimed by more than one packet, the plan must name the serialization edge" — discharged by `h --SFS--> i`. |
| A14 — deferring all doc updates to k leaves merged production changes with no handover record | architecture-reviewer | **accept-with-narrowing** (manager) | Per-packet append to `docs/MASTER_HANDOVER.md` + the REFACTOR_PLAN status header at merge time is permitted **as an owner-coordinated step, not an autonomous one**, since both are never-claimed shared paths. Cumulative reconciliation and the `CSS_OWNERSHIP_MAP.md` rewrite stay at k per N5. |
| A15 — three nits: 6→5 assumption mapping; `REFACTOR_PLAN.md`/`CSS_OWNERSHIP_MAP.md` are not on the never-claimed list; `components.css:3336` omitted | architecture-reviewer | **accept** | All three applied: mapping corrected in Section 0; the never-claimed citation dropped (the conservative treatment is kept, just not cited as a rule requirement); `:3336` added to i's enumeration. |
| F1 — `visual.spec.ts` cannot falsify c; `prepareForScreenshot()` zeroes all animation/transition with `!important` before capture | test-strategist | **accept** | WP4.4-c gets a **bespoke motion oracle owned by WP4.4-a**: computed `transition-*`/`animation-*` differential at rest, captured **without** the determinism tag, plus forced `reduce` **and** `no-preference` runs; `ui-hardening.spec.ts` added. `visual.spec.ts` explicitly **demoted to non-primary backstop** for c. |
| F2 — the determinism layer blinds the oracle to backdrop-filter, scale controls, icons, dark surfaces and form-control paint | test-strategist | **accept** | **Oracle blind-spot register** becomes a named WP4.4-a deliverable — the exact `(selector, property)` pairs neutralized. Per-packet obligation added: no deleted or re-weighted declaration may fall inside the register without a computed-style differential supplied in its place. |
| F3 — `maxDiffPixels: 800` means `visual.spec.ts` cannot enforce V1's "zero differences" | test-strategist | **accept** | **V1 restated**: "0 diff on the packet-scoped element differential; `visual.spec.ts` reproduces only the ledger reds." Arc-wide prohibition on editing `maxDiffPixels`, `threshold` or `mask` in `e2e/visual-helpers.ts`. Recorded that the logo band (1,039/1,046) **exceeds** the 800 tolerance and is a real snapshot failure, not an absorbed diff. |
| F4 — `dark-mode.spec.ts` asserts zero paint yet is named j's primary gate | test-strategist | **accept** | `dark-mode.spec.ts` **demoted everywhere** to cheap toggle-mechanics regression. j's real oracle = the dark half of the visual matrix on all rendered routes + a packet-owned computed-style differential over its 81 top-level rules. e's `body.dark-mode` re-proof is a computed-owner + rest-state differential per M1/M5/M6, **not** a spec run. |
| F5 — `/fatigue` is painted 100% by shared bundles and has zero visual coverage; "all 10 routes" undercounts | test-strategist | **accept** (merged with PR#2); baseline-creation sub-item **narrowed** | Denominator restated as **11 rendered routes + the error page**. `fatigue.spec.ts` added to every implementation packet; `fatigue-stage4-smokes.spec.ts` to b/e/f and kept through h–k. WP4.4-a's harness covers `/fatigue` in both themes at all three widths. **Creating `/fatigue` visual baselines is NOT adopted unilaterally — it becomes owner decision N7**, since it is baseline *creation* and `tests/test_visual_selector_contracts.py:38-44` pins matrix membership. |
| F6 — the shared contract file pins declarations *inside* `navbar.css`, `a11y.css`, `theme-dark.css`, `components.css`; AC4 disjointness already false | test-strategist | **accept** (merged with A8) | The combined **contract-pinned declaration register** is a WP4.4-a deliverable. Per-packet **entry condition**: this packet's scope does not intersect the register, or the packet serializes on the shared file. Converts AC4 from assertion to measurement. |
| F7 — adopt per-packet contract files; reject k-consolidation | test-strategist | **accept in full** | This is the proposed answer to **N1** (owner confirms at Gate 1). Per-packet `tests/test_css_wp4_4_<surface>_contracts.py`, kept **permanently**. Rule stated explicitly: **run always, edit never-concurrently** — running a shared contract file is not a claim on it. The "k optionally consolidates" clause is **removed**; k asserts only that all per-packet files exist and are collected. |
| F8 — i's spec set says "all five route specs" (no such set) and both h and i omit `exercise-interactions` + `superset-edge-cases` | test-strategist | **accept** | Replaced everywhere by the explicit **six-spec set**, and the binding triple **"six specs / five routes / four selector branches"** is written into the Terminology section so the three counts can never be conflated. |
| F9 — the `program-backup.spec.ts:79` DB-pollution flake is never mentioned and would trip V1 | test-strategist | **accept** | Added to the known-red register with QUALITY_GATE-mandated handling: record whether it passes in isolation; it is **not** a CSS signal and must **never** trigger a V1 rollback or a bisect. |
| F10 — `nav-dropdown` blocking-status and "`/build-css` not required" are both correctly derived | test-strategist | **accept** (positive confirmation) | Both carried into Plan v2 unchanged. Explicitly recorded that any claim of a live `nav-dropdown.spec.ts:117` red is **stale** and must not be adopted. |
| F11 — `visual.spec.ts` is deep-gate-only, never a required check, and baselines are platform-split | test-strategist | **accept** (merged with PR#8) + new owner decision | b–f run the **win32** matrix locally with the result recorded in the evidence doc; the **`visual-linux` deep-gate dispatch** is named as an explicit gate on h, i, j, k. Cadence becomes owner decision **N8**. |
| F12 — V2 and R3-6 are honour-system; `--update-snapshots` is the path of least resistance | test-strategist | **accept** | Two mechanical guards: (1) a **snapshot-manifest contract** in WP4.4-a's test file over `e2e/__screenshots__/win32/**` and `linux/**`, so any rebaseline turns a pytest **red**; (2) a per-packet gate — `git diff --name-only <base>...HEAD` shows zero paths under `e2e/__screenshots__/` and zero changes to `e2e/visual-helpers.ts`. |
| F13 — "no packet may inherit a projection as fact" is prose, not a gate | test-strategist | **accept** | WP4.4-a emits **`docs/CSS_PHASE4_WP4_4_A_BASELINE.json`** (per-surface lines, `!important` occurrence counts, per-rule Stylelint counts, exact `@layer` spans, both registers, `sourceCommit`) plus contract `test_wp4_4_baseline_is_pinned_and_matches_disk`. **A packet quoting a number absent from that JSON fails its evidence gate.** |
| F14 — V3/V4 thresholds are WP4.1 figures from a commit predating the whole WP4.3 arc | test-strategist | **accept** | V3/V4 now compare against the **WP4.4-a measure baseline**. The WP4.1 JSON is retained **only** as the immutable historical anchor for the arc-level report at k. |
| F15 — `!important` counted in two different units inside one invariant | test-strategist | **accept** | WP4.4-a normalizes all `!important` reporting to **Stylelint occurrence counts**, recording both units. The Problem table's line counts are marked **non-authoritative** in Section 0. |
| F16 — every new contract is self-confirming; no red-path proof required | test-strategist | **accept** | Added to every implementation packet's gate: the new contract is **proven to fail** — restore one deleted declaration (or invert one asserted invariant), record the observed failure output in the evidence doc, revert. |
| F17 — the commutativity theorem covers deletion only, but d and f's scopes include re-weighting | test-strategist | **accept, treated as blocking** on its own terms | Class-(a) concurrency is **restricted to pure deletion of proven non-winners**. Any re-weight, selector rewrite or generation consolidation in b–f **reclassifies that packet to class (c) or splits it** into a concurrent deletion half and a sequential re-weight half. The restriction is stated in §4 so the theorem's precondition is visible. |
| F18 — matrix size stated as "6 variants"; `.claude/rules/testing.md` records a stale 48 | test-strategist | **accept** | Written everywhere as "`visual.spec.ts` — full matrix (10 pages × 3 viewports × 2 themes) = **60 tests**". WP4.4-a re-measures via `--list` and **flags** the `.claude/rules/testing.md` correction as a separate AI-workflow-doc change, **not** folded into any CSS packet. |
| F19 — `accessibility.spec.ts` omitted from b and e, the two packets whose surfaces it actually measures | test-strategist | **accept** | `accessibility.spec.ts` runs on **every** implementation packet b–j. |
| F20 — a's gate omits the Stylelint run it exists to produce; `lint:css` includes SCSS | test-strategist | **accept** | `npm run lint:css` added to a's gate, with every packet-level delta **filtered to the seven surfaces** so SCSS noise cannot confound V3/V4. |
| F21 — `QUALITY_GATE.md` has no `static/css/**` row; the arc's routing is inferred, not derived | test-strategist | **accept-as-proposal, narrowed** (manager) | Becomes owner decision **N10**. WP4.4-k *proposes* a `static/css/**` row; because `docs/ai_workflow/**` is a never-claimed shared path this is **owner-gated, not autonomous**. |
| PR#1 — Calculation surface `none` verified correct across every packet | product-risk-reviewer | **accept** (confirmation) | Verification recorded in Plan v2. The `none` claim stands; no migration notes are owed; the backup contract is untouched because no schema changes. |
| PR#2 — the matrix omits `/fatigue` and the error page, the two routes shared CSS paints 100% of | product-risk-reviewer | **accept** (merged with F5) | As F5, **plus** `templates/error.html` added explicitly to the uncovered-route list. Where a visual baseline does not exist, WP4.4-a **records the gap** rather than letting downstream packets inherit an unstated blind spot. |
| PR#3 — the `.value-changed` three-colour family is JS-applied and invisible to all three rest-state oracles; M1 would return *dead* for it | product-risk-reviewer | **accept** | New **M10**: a declaration reachable only through an interaction state or a JS-applied class is **non-deletable unless proven under that state**. All six `.value-changed` rule blocks (`components.css:995-1013`, `:1016-1035`; `theme-dark.css:565-582`, `:585-591`) named as **must-retain** in h's and j's exclusions until such a proof exists. |
| PR#4 — `@media`-conditional accessibility rules (reduced-motion, print, breakpoint) are structurally mis-classifiable; only c guards against it | product-risk-reviewer | **accept** | New **M11**, a global obligation: no declaration inside an `@media` block may be classified dead without a capture taken **under that block's own condition**. `emulateMedia({ reducedMotion: 'reduce' })` added to j; `emulateMedia({ media: 'print' })` + a breakpoint sweep added to d. |
| PR#5 — custom-property remap blocks are invisible to computed/pixel oracles; j's central triage rests on what the method cannot see | product-risk-reviewer | **accept** (merged with A5 into M9) | M9 covers the rule. Additionally `theme-dark.css:597-621` is marked **retained-by-default** in j, with per-property deletion requiring the exhaustive repo-wide `var(--name)` consumer search plus route coverage for every consumer found. |
| PR#6 — i and j can move the deferred superset gap without opening `pages-workout-plan.css`; and it renders in zero screenshots | product-risk-reviewer | **accept**, capture method **narrowed** (manager) | **G4 restated**: "record it; and treat any change in superset row rendering as a **rollback trigger**." `tr.superset-group-1..4` named explicitly in i's R3 condition-4 inventory. i and j capture Workout Plan with at least one linked superset present in both themes — as a **scoped element capture, not a new committed baseline**, so R2's no-rebaseline holds. |
| PR#7 — required-CI specs guarding this arc's risk surface are absent from every gate list | product-risk-reviewer | **accept** | `summary-pages`, `fatigue` and `fatigue-stage4-smokes` added to b/c/d/e/f and kept through h–k. Recorded that adding `fatigue-stage4-smokes` **protects** the parked Stage-4 workstream rather than resuming it. |
| PR#8 — V1 leans on a spec that never runs on the PR path, with platform-split baselines | product-risk-reviewer | **accept** (merged with F11) | Per packet, the Windows matrix must be run locally and its result recorded in the evidence doc; k's gate includes a dispatched `visual-linux` compare reconciled against the **WP4.0 Linux ledger**, not only the Windows one. |
| PR#9 — d's a11y guard protects only the restore half of a three-part suppress/restore/re-suppress focus contract | product-risk-reviewer | **accept** | `tests/test_css_wp4_4_a11y_contracts.py` must assert the **guarantee**, not the rule text: computed non-`none` outline on a keyboard-focused control at **every `data-scale` level in both themes**, plus skip-link visibility on first Tab. |
| PR#10 — the "interaction states are uncertifiable" lesson from WP4.3i-dead is missing from M1–M8 | product-risk-reviewer | **accept** | New **M12** added verbatim in substance. **h must state up front** whether hover/focus/active declarations are in or out of its deletion scope. **G7 reworded to "do not modify *or invalidate*"** the WP4.3i-c Page Header contract. |
| PR#11 — the load-order diagram silently omits two `base.html` links; CDN state changes rendering between runs | product-risk-reviewer | **accept** | Section 0 now states what the diagram excluded (`base.html:13` Google Fonts, `:15` jsdelivr fallback) and why. WP4.4-a **pins and records network state** — including whether the jsdelivr fallback fired — in every evidence doc. |
| PR#12 — terminology clean; no user-visible copy changes; no canonical term rebranded | product-risk-reviewer | **accept** (confirmation) | Recorded in Plan v2. No packet proposes copy. |
| PR#13 — expected-movement ranges are the only quantified per-packet targets and will read as quotas | product-risk-reviewer | **accept** | Stated once beside the ⚠️ banner: expected-movement figures are **measurements to be corrected, never acceptance criteria**, and **under-delivery against a projection is never grounds to widen a packet's scope or relax the non-winner rule**. |

---

## Plan v2

**Goal**: unchanged from v1 — decompose WP4.4 into eleven individually provable packets so the seven shared bundles can be cleaned with no unexplained visual difference and no two writers on one production path. **What changed is the instrumentation**: v1's decomposition, DAG, ownership model and R3 sequencing survived review; the gates that were supposed to prove them did not.

**No packet was implemented in this session. No worktree was created, moved, merged or removed. No `senior-developer` was dispatched. The only file written is this artifact.**

### Scope

- **In**: unchanged from v1 — audit + decomposition of the seven surfaces, the DAG, merge order, concurrency classification, per-packet gates, rollback criteria, the final integration gate, and the *planned* (not implemented) `:is()` repair.
- **Out**: unchanged — plus the four narrowings recorded in the matrix: `/fatigue` baseline **creation** (N7), the `QUALITY_GATE.md` row (N10), autonomous handover edits (A14), and any new committed baseline for superset capture (PR#6).

### §0 Factual corrections carried into v2

| Was (v1) | Is (v2) | Source |
|---|---|---|
| "the complete `:is()` family", four branches throughout | **Twelve four-branch rules + one three-branch rule at `:4433`** inside `@media (prefers-reduced-motion: reduce)`; 19 `:is(` occurrences in the file, all enumerated by a | A10 |
| reduced-motion suppression implied uniform | **Weekly/Session Summary tables are NOT reduced-motion-suppressed** — a pre-existing asymmetry to preserve, not fix | A10 |
| "layered rules lose to every unlayered rule" | True for **normal** declarations only; for **`!important`** the order inverts and unlayered important is **weakest** | A6 |
| "all 10 routes" | **11 rendered routes + the error page**; `/fatigue` and `error.html` are painted 100% by shared bundles | F5, PR#2 |
| "`visual.spec.ts` all 6 variants" | **Full matrix = 10 pages × 3 viewports × 2 themes = 60 tests**; `.claude/rules/testing.md`'s 48 is stale | F18 |
| V3/V4 thresholds from the WP4.1 JSON | Thresholds come from the **WP4.4-a measure baseline**; WP4.1 JSON is the historical anchor only | F14 |
| `!important` = line counts | **Stylelint occurrence counts** are authoritative; line counts are non-authoritative | F15 |
| "all five route specs" | **Six specs / five routes / four selector branches** | F8 |
| logo band vs `maxDiffPixels: 800` | The band **exceeds** 800 — it is a genuine snapshot failure, not an absorbed diff | F3 |

### §2b Method rules — M1–M12 (consolidated)

M1–M8 carry forward from v1 unchanged in substance; M4 is extended; M9–M12 are new. **M6a was added after Packet a measured it** — a factual/method correction that tightens the approved plan; it does not reopen Gate 1 or expand production scope.

| # | Obligation | Origin |
|---|---|---|
| M1 | A sentinel sweep alone **over-reports deadness**. Every claim needs sweep **AND** rest-state differential **AND** same-CSS control. | WP4.3i-dead |
| M2 | Overpaint-suppressed declarations must be differenced **in pixel space**. | WP4.3j-a |
| M3 | The full-page pixel oracle is **unusable on animated-navbar routes**; scope every capture to the element under test. | WP4.3j-b-dead |
| M4 | The specificity/ownership model must handle `:is()`/`:where()`/`:not()`/`:has()`, must not naively comma-split, **and must implement `@layer` ordering plus the `!important` inversion** — unit-checked against hand-computed cases before use. | WP4.3j-b-dead, j-c; **extended by A6** |
| M5 | Every deadness sweep carries a **known-live control**; a failing control invalidates the sweep. | WP4.3j-c-dead |
| M6 | **A probe that changes nothing proves nothing.** Sentinel-took-effect asserted per record; `var()`-bearing shorthands are invisible to longhand CSSOM queries. | WP4.3j-c |
| **M6a** | **Suppress transitions before applying, reading AND removing a sentinel.** A sentinel written to a transitioned property reads back its **pre-sentinel** value for the whole transition duration, so `getComputedStyle` reports "no effect" on an element the sentinel reached perfectly — a false deadness verdict. Inline `!important` does **not** help: the lag is in the computed value, not in the cascade. The release is symmetric — drop the sentinel while transitions are still suppressed, or the revert check reads the value mid-flight. Measured live on `header` and `select`, which carry `transition: all 0.3s`. **Binding on every remaining WP4.4 packet.** | **WP4.4-a; adopted by the owner 2026-07-27 as a binding clarification of M6** |
| M7 | The animated-logo red is a **band** (1,039 / 1,046 observed in one run), never an exact-pixel invariant — **and it exceeds `maxDiffPixels: 800`**, so it presents as a real snapshot failure. | WP4.3i-filter-btn; **F3** |
| M8 | **Delete only proven non-winners.** Never delete a winning declaration. (Precondition of the commutativity theorem — see F17 restriction in §4.) | derived |
| **M9** | The oracle's property universe must be **longhand-complete**, and **no packet may delete a custom-property declaration under the non-winner rule**. Removal requires a `var()` dependency graph resolved across all 21 hand-maintained sources, plus route coverage for every consumer found. | **A5 + PR#5** |
| **M10** | A declaration reachable **only through an interaction state or a JS-applied class** is non-deletable unless proven under that state. (`.value-changed` is the named instance.) | **PR#3** |
| **M11** | **No declaration inside an `@media` block may be classified dead without a capture taken under that block's own condition** — reduced-motion, print, and each breakpoint. | **PR#4** |
| **M12** | **Interaction states animate and are uncertifiable without a same-CSS control reaching zero differing records.** WP4.3i-dead's control produced 52 differing records and shrank the packet 24 → 14. Any packet touching hover/focus/active must state that scope up front. | **PR#10** |

*M10 and M12 are distinct and both required: M10 says you must prove under the state; M12 says that proof is itself unreliable until a same-CSS control reaches zero.*

### §2 Standing constraints — G1–G11 (updated)

G1 (corrected per A10), G2, G5, G8, G9, G10 carry forward as written in Plan v1. Changed and new:

| # | Constraint (updated) |
|---|---|
| **G3** | Workout Log regions A–C must be re-measured **before and after** by any packet that changes shared selector ownership — **binding on both h and i** (A9), not i alone. |
| **G4** | The superset dark-tint gap stays **unacted** (R2) — **and any change in superset row rendering is a rollback trigger** (PR#6), including a change produced by a packet that never opens `pages-workout-plan.css`. |
| **G6** | Do not reopen **or resurrect** the ten frozen Workout Plan interaction-state declarations. Resurrection via a shared-specificity change is a violation in effect (A3). |
| **G7** | Do not modify **or invalidate** the locked WP4.3i-c Page Header contract (PR#10). A shared-bundle change can break it without editing any page bundle. |
| **G11** | **No packet may delete the last `@layer <name> { … }` block** for any name in the `tokens.css:2` order list. `navbar` is single-sourced at `navbar.css:6` (A7). |

### §5 Preservation invariants — V1–V6 (restated)

| # | Invariant | Pass condition (v2) |
|---|---|---|
| **V1** | No unexplained visual differences | **0 diff on the packet-scoped element differential** (`maxDiffPixels: 0`, element-scoped per M3); `visual.spec.ts` reproduces **only** the ledger reds. Any other diff → **rollback**. (F3) |
| **V2** | No snapshot rebaseline | Enforced mechanically, not promised: the **snapshot-manifest contract** turns any `--update-snapshots` into a pytest red, and the per-packet `git diff` gate shows zero paths under `e2e/__screenshots__/` and zero changes to `e2e/visual-helpers.ts`. (F12) |
| **V3** | No increased max specificity; no unexplained `!important` | Stylelint **occurrence** counts vs the **WP4.4-a baseline**; `selector-max-specificity` and `selector-max-id` must not rise; delta filtered to the seven surfaces. (F14, F15, F20) |
| **V4** | Monotonic duplicate reduction | `no-duplicate-selectors` and `declaration-block-no-duplicate-properties` measured against the **a-baseline**, never the WP4.1 figures. (F14) |
| **V5** | 30% is a **Phase-4** target | Each packet reports contribution; k reports cumulative + shortfall vs 30,768. **Expected-movement figures are measurements to be corrected, never acceptance criteria; under-delivery is never grounds to widen scope or relax M8.** (PR#13) |
| **V6** | Cascade correctness outranks line count | Unchanged. |

### Packets — deltas from Plan v1

All eleven packets, their eleven attributes, and the ownership model carry forward from Plan v1 **except** as amended below. Every packet additionally inherits the standing gate rules in §"Gates".

| Packet | Amendments applied in v2 |
|---|---|
| **a** baseline + harness | Harness **committed** to `scripts/css_audit/`; generated output stays in `artifacts/wp4_4/` (A11). New deliverables: **`docs/CSS_PHASE4_WP4_4_A_BASELINE.json`** + `test_wp4_4_baseline_is_pinned_and_matches_disk` (F13); **contract-anchor + pinned-declaration register** (A8+F6); **oracle blind-spot register** (F2); **snapshot-manifest contract** (F12); the **bespoke motion oracle** for c (F1); enumeration of all **19** `:is(` occurrences (A10); exact `@layer` spans; `/fatigue` + error page in the harness matrix (F5, PR#2); `npm run lint:css` filtered to the seven surfaces (F20); **network state pinned and recorded** (PR#11); `--list` re-measure flagging the stale `.claude/rules/testing.md` 48 (F18). **N7: create `/fatigue` visual baselines on Windows *and* Linux, and update `tests/test_visual_selector_contracts.py:38` accordingly — creation only; no existing screenshot may be rebaselined.** `CD` edge added from a to every implementation packet. |
| **b** base.css | + `accessibility.spec.ts` (F19), `summary-pages`, `fatigue` (PR#7). Class (a) — **pure deletion only** (F17). |
| **c** motion.css | Primary gate is the **bespoke motion oracle**, not `visual.spec.ts` (F1); + `ui-hardening`, `accessibility`, `fatigue`. **Scheduled first** in the concurrent set (A12.3). M11 binds its `@media` blocks. |
| **d** a11y.css | + `emulateMedia({ media: 'print' })` and a breakpoint sweep (PR#4, M11); contract must assert the **focus guarantee** across every `data-scale` in both themes + skip-link on first Tab (PR#9); scale controls need a computed-style differential (pixel-blind, F2). **Conditional class (a)** — see §4. |
| **e** layout.css | `body.dark-mode` re-proof is a computed-owner + rest-state differential, **not** `dark-mode.spec.ts` (F4); + `accessibility`, `volume-progress`, `fatigue-stage4-smokes`, `summary-pages`, `fatigue` (F19, PR#7). |
| **f** navbar.css | **G11** in exclusions — may not delete the single-sourced `@layer navbar` block (A7); the layered `!important` generation may be a **winner**, not dead (A6); contract-pinned `--nav-gap`/`--nav-padding-*` in scope-intersection check (F6). **Conditional class (a)** — see §4. |
| **g** components audit | **Advisory-nomination-only**; h re-runs **full classification** for every nominated family (A12.1). Records the audited commit. |
| **h** components deletion | Exclusion restated at **declaration granularity** — no declaration inside the twelve four-branch rules or `:4433` (A9); **G3 binds h**; `.value-changed` six blocks **must-retain** (PR#3, M10); must state up front whether hover/focus/active are in scope (PR#10, M12); six-spec set (F8); deep-gate `visual-linux` (F11). |
| **i** `:is()` repair | **Serialized single-writer claim on `tests/test_css_cascade_contracts.py`**, amendment restricted to re-expressing the same premise (A1, N6); **admissible repair shapes enumerated with their production-path sets**, template/JS shapes escalated separately (A2, N9); R3 condition 2 extended with the **named non-winner sub-list** — ten frozen declarations, regions A–C, region-C hover rule, `tr.superset-group-1..4` (A3, PR#6); preserve the `:4433` branch asymmetry (A10); `:3336` added to the enumeration (A15); six-spec set (F8); superset capture in both themes as a **scoped element capture** (PR#6). |
| **j** theme-dark | `dark-mode.spec.ts` **demoted to mechanics** (F4); real oracle = dark visual half over all rendered routes + computed-style differential across the 81 rules; `theme-dark.css:597-621` custom-property block **retained-by-default** (PR#5, M9); `.value-changed` dark blocks **must-retain** (PR#3); `emulateMedia({ reducedMotion: 'reduce' })` (PR#4). |
| **k** integration | Asserts all per-packet contract files exist and are collected — **no consolidation** (F7); reconciles against the **WP4.0 Linux ledger** as well as Windows (PR#8); proposes the `QUALITY_GATE.md` `static/css/**` row **as an owner-gated proposal** (F21, N10). |

### Packet DAG (revised)

Edge types: `PE` prerequisite-evidence · `SFS` same-file-serialization · `CC` cascade-coupling · `CD` contract-dependency · **`FI` final-integration** (new, A12 nit).

| From | To | Type | Reason |
|---|---|---|---|
| a | b, c, d, e, f, g | `PE` | Controls must pass and the true baseline must exist before anything is classified dead |
| a | b, c, d, e, f, g, h, i, j, k | `CD` | **New (A8/F6)** — the contract-anchor + pinned-declaration register binds every implementation packet |
| b, c, d, e, f | h | `CC` | h rebases onto all and re-proves; re-proof is a **full re-capture** (A12.3) |
| g | h | `PE` | h acts only on families g nominated **and h re-classified in full** (A12.1) |
| g | i | `PE` | R3 condition 1 — complete affected family |
| h | i | `SFS` | Both write `components.css`; single-writer |
| h | i | `CC` | Dead rules deleted first so the repair cannot resurrect them (G2 pattern) |
| **b, c, d, e, f** | **i** | `CC` | **Added (A12.2)** — was asserted in i's dependency row but missing from the table |
| i | j | `CC` | `theme-dark.css` loads last; "justified remap" undecidable before shared ownership settles |
| b…f, h, i | j | `CC` | Same reason, transitively |
| all | k | `FI` | Final integration gate after rebasing onto every predecessor |

*Removed: the redundant `a → f` edge (A12 nit). The graph remains acyclic.*

**Linear merge order:** `a` → **`c` first**, then { `b`, `d`, `e`, `f` } → `g` → `h` → `i` → `j` → `k`.

`c` is scheduled first because `motion.css` owns the transitions whose in-flight state produced the 52-differing-record control failure that M1/M12 exist to prevent; merging it mid-arc would invalidate differentials b/d/e/f had already captured. `g` may start once `a` lands and run concurrently with the implementation packets, recording its audited commit.

### §4 Concurrency classification — final, under the F17 restriction

**Class (a) is now restricted to *pure deletion of proven non-winners*.** A packet that re-weights a winner, rewrites a selector, or consolidates a generation is **not** covered by the commutativity theorem and reclassifies.

| Packet | Class | Determination |
|---|---|---|
| **c** motion.css | **(a) concurrent — merges first** | Pure deletion. File-disjoint. |
| **b** base.css | **(a) concurrent** | Pure deletion; 0 `!important`, nothing to re-weight. |
| **e** layout.css | **(a) concurrent** | Pure deletion (including the `body.dark-mode` block, subject to G5 re-proof). |
| **d** a11y.css | **(a) CONDITIONAL → splits** | Its `!important` reduction is **re-weighting**, not deletion (F17), and its `*:focus-visible,` string is contract-pinned (F6). **Split: `d1` = pure deletion, class (a); `d2` = `!important` re-weighting, class (c), sequential.** |
| **f** navbar.css | **(a) CONDITIONAL → splits** | "Consolidating three generations" is re-weighting (F17); `--nav-gap`/`--nav-padding-*` are contract-pinned (F6); the layered `!important` generation may be a live winner (A6); G11 caps deletion. **Split: `f1` = pure deletion, class (a); `f2` = generation consolidation, class (c), sequential.** |
| **a**, **g** | **(b) parallel read-only audit** | Own no production path. |
| **d2**, **f2**, **h**, **i**, **j**, **k** | **(c) sequential** | Re-weighting, same-file serialization, or cascade/load-order coupling. |

**Revised safe pairings** (one file each, pure deletion only): Codex `c` then `b`; Opus `e`; then `d1` and `f1` in either order. `d2` and `f2` land sequentially after the concurrent set, before `g`.

**Arc-wide E2E serialization rule (A4).** File-level disjointness does not reach the measurement apparatus. Therefore: **only one worktree may run Playwright at a time**; `PW_REUSE_SERVER` must be **unset** in every packet worktree (`playwright.config.ts:114` honours it and `:67` hard-codes port 5000, so a concurrent run can certify a packet against another worktree's CSS); every packet worktree is created with `scripts/new-worktree.ps1 -Seed visual`, because the WP4.0 ledger was measured against the visual seed and an unseeded worktree makes V1 incomparable.

**(d) Shared files — single writer or never edited**

| Path | Rule |
|---|---|
| `static/css/components.css` | Single-writer across h and i; strictly serialized (`SFS`) |
| `tests/test_css_cascade_contracts.py` | **Run always, edit never-concurrently.** Running is not a claim. Only **i** may amend it, as a serialized single-writer claim restricted to re-expressing the j-c-dead premise (N6) |
| `scripts/css_audit/` | **New shared path** — written by a; b–k may not modify without serialization (A11) |
| `e2e/visual-helpers.ts`, `playwright.config.ts` | **Never edited by any packet** (F3, F12, A4) |
| `e2e/__screenshots__/**` | **Never written by any packet**; guarded by the manifest contract (F12) |
| `docs/MASTER_HANDOVER.md`, REFACTOR_PLAN status header | Per-packet append at merge time, **owner-coordinated, not autonomous** (A14) |
| `docs/CSS_OWNERSHIP_MAP.md` | k only, subject to N5 |
| `templates/base.html`, `tokens.css`, `pages-workout-plan.css`, `app.py`, `CLAUDE.md` files, `.claude/settings.json`, `.gitignore`, `data/**` | **Not touched by any packet** |

**Final integration gate** — WP4.4-k: rebase onto every predecessor, `/verify-suite`, the full 60-test visual matrix in both themes, `/fatigue` + error page coverage, all cascade contracts, a dispatched `visual-linux` deep gate reconciled against the WP4.0 **Linux** ledger, full Stylelint re-measure against both the a-baseline and the WP4.1 historical anchor, and the V5 contribution/shortfall report.

### Gates

The consolidated gate table from the test-strategist's review is **adopted verbatim as Plan v2's gate specification** — see "Expected gates — consolidated for Plan v2" in the Reviewer findings section above — with these merges applied: `summary-pages`, `fatigue`, `fatigue-stage4-smokes` added to b/c/d/e/f and kept through h–k (PR#7); `accessibility.spec.ts` on every implementation packet b–j (F19); `emulateMedia` print + breakpoint sweep on d and reduced-motion on j (PR#4); the six-spec set on h and i (F8); `d1`/`d2` and `f1`/`f2` inherit their parent packet's gates.

**Standing rules on every implementation packet:** run-never-edit the two shared contract files · red-path proof for every new contract (F16) · `git diff` shows zero `e2e/__screenshots__/` paths and zero `e2e/visual-helpers.ts` changes (F12) · Stylelint filtered to the seven surfaces vs the a-baseline (F14, F20) · known reds = WP4.0 ledger + the logo **band** + the `program-backup.spec.ts:79` DB-pollution flake which is **never** a V1 rollback trigger (F9) · `/build-css` **not required** (F10).

### Effort · Owner · Sequence

Unchanged from Plan v1 except: **c merges first**; **d and f split into d1/d2 and f1/f2**; **i gains an explicit owner checkpoint** before any edit (N4), at which its enumerated repair shape and its two pre-change inventories are presented.

### Owner decisions — N1–N10, ALL RESOLVED at Gate 1 (owner, 2026-07-27)

**Gate 1 rulings — binding on every packet in this arc.** Each ruling is stated verbatim as the owner gave it, followed by what it obliges.

| # | Ruling (binding) | Obligation created |
|---|---|---|
| **N1** | **Permanently use per-packet contract files; no consolidation at k.** | Every implementation packet adds its own `tests/test_css_wp4_4_<packet>_contracts.py`. **k asserts all per-packet contract files exist and are collected; k may not merge, fold or consolidate them.** This is what makes class-(a) concurrency real for the pure-deletion packets (F7). |
| **N2** | **Freeze `@layer` membership for the entire arc.** | No packet may move a rule across a layer boundary, add a layered block, or remove one. Extends G10 from advice to a hard gate for a–k. A diff that changes layer membership is rejected, not discussed. |
| **N3** | **Narrow the `:is()` repair to branches with no would-be winners; abandon the repair if that cannot be proven safely.** | Packet **i** proceeds only on branches where it is *proven* no page-local rule would become a winner. Branches that cannot be proven safe are excluded. If no branch survives the proof, **i is abandoned** and WP4.4 ends as audit + deletion. `delete-offenders-first` is NOT authorized. |
| **N4** | **Require a separate owner checkpoint immediately before Packet i.** | The arc **stops after h**. Before any edit under i, present i's enumerated repair shape and both pre-change inventories (the complete `:is()` family from g/h, and the G3 regions A–C measurement) and wait for owner approval. Gate 1 authority does **not** extend to i. |
| **N5** | **Allow k to update `docs/CSS_OWNERSHIP_MAP.md`, responsibilities only.** | k is the single writer of that map, restricted to responsibility/ownership statements. k may not use it to record decisions, gate routing, or history. |
| **N6** | **Allow Packet i to amend the existing cascade contract only to re-express the same premise; the regression assertion may not be removed or weakened.** | i holds a serialized single-writer claim on `tests/test_css_cascade_contracts.py:1614-1627`. The amendment must re-express the **same** j-c-dead shared-arm premise against the repaired selector shape. Removing, weakening, loosening, or `xfail`-ing the assertion fails the packet. All other packets: **run always, edit never**. |
| **N7** | **Create `/fatigue` visual baselines on both Windows and Linux during Packet a.** | Explicit authorization for baseline **creation** at a, on both platforms, plus the `tests/test_visual_selector_contracts.py:38` update this requires. **This is not authorization to rebaseline any existing screenshot** — V2 stands unchanged for every pre-existing snapshot, and a needed rebaseline still stops and escalates. |
| **N8** | **Run the Linux visual deep gate at h, i, j, and k.** | `visual-linux` is dispatched at those four packets and reconciled against the WP4.0 **Linux** ledger. b, c, d, e, f, g gate on Windows/Chromium only. |
| **N9** | **Only CSS-local repair shapes are admissible: split the selector list, or apply `:where()` to the ID branch. Any template or JavaScript solution requires a separate owner-gated packet.** | i's production scope is `static/css/components.css` and nothing else. A class-hook shape touching `templates/**` or `static/js/**` may be *proposed* at the N4 checkpoint but may never be absorbed into i. |
| **N10** | **Allow k to propose a `static/css/**` row in `docs/ai_workflow/QUALITY_GATE.md`, subject to owner review.** | k drafts the row; it does not land on packet authority. `docs/ai_workflow/**` remains a never-claimed shared path — the proposal is presented for owner review at k's merge. |

**Consequences of the rulings taken together.** N6 `yes-restricted` makes **i** executable rather than red-by-construction (A1). N9 keeps **i** single-file, so R3 condition 8 holds. N3 + N4 together mean i may still end in abandonment, and that outcome is pre-authorized as an acceptable arc result, not a failure. N1 preserves the concurrency claim for b/c/d1/e/f1. N2 removes the precedence-inversion hazard G10 identified. N7 closes the `/fatigue` oracle gap that F5 and product-risk #2 raised.

#### Original decision table (as presented for Gate 1)

| # | Decision | Recommendation | Consequence of each answer |
|---|---|---|---|
| **N1** | Per-packet contract files vs the shared `tests/test_css_cascade_contracts.py`? | **Adopt per-packet files permanently**; reject k-consolidation (F7) | `yes` → class-(a) concurrency is real for the pure-deletion packets. `no` → b–f serialize on one test file and the concurrency claim collapses. |
| **N2** | Freeze `@layer` membership arc-wide? | **Freeze** | `freeze` → no packet moves a rule across a layer boundary. `allow` → precedence flips in opposite directions for normal vs `!important`, and G11 alone will not contain it. |
| **N3** | WP4.4-i escalation path if page-local rules would become winners | **Narrow the repair to branches with no would-be winners; fall back to abandoning** | `narrow` → repair proceeds on safe branches. `abandon` → WP4.4 becomes audit+deletion only. `delete-offenders-first` → pulls page bundles in and needs its own approval. |
| **N4** | Does WP4.4-i need its own approval checkpoint at implementation time? | **Yes** | `yes` → the arc stops after h and presents i's enumerated shape + both inventories. `no` → i proceeds on Gate 1 authority alone, which the council's A1–A3 argue against. |
| **N5** | May k update `docs/CSS_OWNERSHIP_MAP.md`? | **Yes — responsibilities only, at k, single writer** | `yes` → the map reflects post-arc ownership. `no` → the map documents responsibilities that no longer match the code. |
| **N6** | May WP4.4-i amend `tests/test_css_cascade_contracts.py:1614-1627` (the j-c-dead shared-arm anchor), and under what proof? | **Yes — restricted to re-expressing the same premise**, never deleting the assertion | `yes-restricted` → i is executable. `no` → **i is impossible as specified**; it reds by construction (A1). `yes-unrestricted` → the arc loses its strongest Workout Log regression guard. |
| **N7** | Create `/fatigue` visual baselines on **both** platforms? | **Owner call — this is baseline *creation*, not rebaseline**; I recommend `yes` at a, before any implementation packet | `yes` → the highest-shared-exposure route gains a pixel oracle; requires updating `tests/test_visual_selector_contracts.py:38`. `no` → `/fatigue` is covered only by its functional specs and the harness differential, and the gap is recorded explicitly. |
| **N8** | Linux `visual-linux` deep-gate cadence — per packet, or once at k? | **h, i, j and k** (the packets that can move five-or-more routes) | `per-packet` → slowest, safest. `once-at-k` → cheapest, but Linux-only drift is attributed to the whole arc rather than one packet. |
| **N9** | Which `:is()` repair shapes are admissible? | **Split the list, or `:where()` the ID branch** — both stay inside `components.css`. **Any shape needing `templates/**` or `static/js/**` is escalated as a separate owner-gated packet, never absorbed** | Choosing a CSS-only shape keeps i single-file. Choosing the class-hook shape expands production scope to templates and possibly JS — exactly what R3 condition 8 exists to prevent. |
| **N10** | May k propose a `static/css/**` row for `docs/ai_workflow/QUALITY_GATE.md`? | **Yes, as an owner-gated proposal** — `docs/ai_workflow/**` is a never-claimed shared path | `yes` → the arc leaves its most durable artifact: derived rather than inferred CSS gate routing. `no` → every future CSS packet re-infers its gates. |

**N6 and N9 were the two that could stop the arc.** Both were ruled in the arc's favour: N6 `yes-restricted` and N9 CSS-local-only. WP4.4-i is executable as specified and stays single-file — subject to N3's proof obligation and N4's checkpoint.

---

## Sign-off

- [x] Gate 0 complete — approved with rulings R1–R6.
- [x] Every finding has a disposition — **49 of 49** (architecture-reviewer A1–A15, test-strategist F1–F21, product-risk-reviewer #1–#13). None rejected; none deferred; four accept-with-narrowing.
- [x] Agent provenance complete — both `product-manager` IDs (`a04906a2a312cd209`, same agent resumed via `SendMessage`), same-PM-resumed `yes`, the three reviewer IDs, evidence gap `none`.
- [x] User approved Plan v2 — **Gate 1 APPROVED by the owner on 2026-07-27**, subject to rulings N1–N10.
- [x] All ten owner decisions resolved — N1–N10 recorded above as binding rulings.
- [x] Ready to implement.

**GATE 1 APPROVED (historical scope).** Plan v2 authorized `a` through `h` and
correctly stopped at N4. **N4 was subsequently approved by the owner on 2026-07-31.**
[`N4_CONTINUATION_AUTHORITY.md`](N4_CONTINUATION_AUTHORITY.md) now authorizes the
sequential `i` → `j` → `k` continuation, records all bounded exceptions and pre-answers
routine decisions. Where this historical Gate-1 paragraph says i is unauthorized, the
dated continuation authority supersedes it.

Planning-artifact commit precedes implementation: this document is committed by itself, with no production, test, or handover file in the same commit.
