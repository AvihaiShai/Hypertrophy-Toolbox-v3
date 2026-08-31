# Theme-dark and P3 optional-work feasibility audit

**Audit type:** planning-only, static/source/history analysis

**Audited HEAD:** `97a79167d371a4c7e080ff70d99bd19b8685606e` (`main`, 2026-09-01)

**Audit date:** 2026-09-01

**Production changes made:** none

This report assesses four **independent future investments**. It does not reopen WP4.4 or P3,
authorize an implementation packet, certify a deletion, choose a visual design, or authorize a
baseline update. Every estimate and source identity below is valid only for the audited HEAD.
**Revalidate this audit, its counts, candidate identities, contract pins, visual state, and tool
reuse assessment after any active work merges.** In particular, the unmerged Linux visual-gate
diagnostic work described in §7 directly affects the proof environment.

The source/history pass began at `b36ea9e1a3d7e0e37918e9db4198cb4bf7e0ecf8`. During final
validation, `main` advanced to the audited HEAD above through one docs-only commit adding
`docs/refactor_optional/audits/bounded_shared_css_audit.md`. A path-scoped diff confirmed no change
to CSS, templates, JavaScript, E2E/tests, CSS-audit tools, workflows, WP4.4/P3 evidence, or the
visual ledgers used here. This report was therefore revalidated rather than restarted.

## 1. Executive decision

| Independent option | Expected user-visible effect | Cost | Risk | Likely value | Recommendation |
|---|---|---:|---:|---|---|
| 1. Add the missing superset dark tint | **Intentional:** linked superset rows become more visible/differently tinted in dark mode | S–M | Medium | Clear, bounded product improvement if the owner wants stronger grouping | **PROCEED, after the Linux/visual gate is stable and after a visual choice is signed** |
| 2. Re-certify the 235 Packet-a-span declarations | None; any visible difference is a failure | M–L | Medium–high | At most the historical 235 declarations / 416 lines, probably less after remeasurement | **DEFER** |
| 3. Reopen P3 after P3-a0 | None; any visible difference is a failure | XL across five remaining packets | High, including self-certification | Unknown and explicitly expected to be a small certified deletion, not a gutted file | **DECLINE at present** |
| 4. Unlink or eliminate `theme-dark.css` | None if done as a migration; potentially site-wide dark-theme regressions if wrong | XL–XXL | Very high | Structural simplification and one fewer request; many bytes/rules would move rather than disappear | **DECLINE at present** |

These are not a four-step continuation. The tint changes the product. The 235-declaration project
and P3 are two different dead-CSS certification investments on different source surfaces. Unlinking
is a global ownership and loading migration that must cover live rules which neither deletion
project is allowed to remove.

## 2. Audited state and inherited authority

The relevant closed decisions are consistent:

- WP4.4 continuation ruling **C8** kept the Packet-a `@layer workout` span closed and directed the
  235 declarations to a future, separately authorized removal-certification packet.
- WP4.4 ruling **C11** kept `theme-dark.css` linked and nonempty, retained custom properties,
  `.value-changed`, and reduced-motion behavior, and prohibited adding the superset tint through
  packet j.
- WP4.4 **R4** froze `templates/base.html`, the global link order, and unlinking. It did not prove
  that unlinking would be safe.
- P3 was terminated by the owner at **P3-a0**. P3-a1 is unfunded and P3-b through P3-e are
  unauthorized. The old Gate-0/Gate-1 signatures do not confer residual execution authority.
- WP4.4 closed at 539 net source lines removed, 48 declaration-level `!important` removals,
  2,751 seven-surface Stylelint findings, and a 0/2,275,668 computed-value differential in each
  theme. Those results are historical evidence, not certification for a new HEAD.

At audited HEAD, `theme-dark.css` is still 574 lines and 74 brace-opening blocks, with 125 raw
`!important` occurrences (124 declarations plus one comment occurrence) and 34 custom-property
declarations. Since P3-a0, its topology stayed the same but one value changed: the dark
`.frame-content` background moved from `rgba(26, 26, 34, 0.5)` to `transparent` in #464. That is
enough to make P3-a0's source digest and any declaration-level classification provenance stale.

## 3. Option 1 — missing superset dark-mode tint

### Assessment: PROCEED, conditionally

This is the only option with a direct product payoff and a bounded implementation surface. It is
**not dead-CSS cleanup**. The owner must choose the intended appearance before implementation,
and the result must be reviewed as an intentional dark-mode rendering change.

### 3.1 Current token, consumer, and ownership map

| Item | Current source/behavior | Current owner |
|---|---|---|
| `--superset-color-1..4` | `#7C3AED`, `#0891B2`, `#059669`, `#D97706` in the Workout Plan page bundle | `static/css/pages-workout-plan.css` `:root` |
| `--superset-bg-1..4` | Matching RGB values at alpha `0.08`; the same values resolve in light and dark mode | `static/css/pages-workout-plan.css` `:root` |
| Background consumers | `tr.superset-group-1..4` use the four background tokens with `!important` | `static/css/pages-workout-plan.css` |
| Solid-color consumers | Row edge, connector, badge, checkbox/accent and selection styles use `--superset-color-*` or `--superset-row-color` | `static/css/pages-workout-plan.css` |
| Group assignment | JS cycles groups 1–4, adds `superset-group-N`, edge classes and `data-superset-group`, and supplies the badge's row-color variable | `static/js/modules/workout-plan-table.js` and `workout-plan-helpers.js` |
| Theme state | The app writes only `html[data-theme="light|dark"]` | `static/js/theme-init.js` and `static/js/darkMode.js` |
| Current dark override | None | none |

The four background tokens have only the four row consumers found above. Solid colors and selected,
hover, and drag states are adjacent visual concerns but are not part of the missing-token change
unless the owner deliberately expands the design.

History explains the gap but does not settle the design. Commit `bfadf9d` removed an unreachable
`[data-bs-theme="dark"]` block that set the same RGB values at alpha `0.15`. The app never sets
`data-bs-theme`, so deleting that block was correct dead-selector cleanup. The historical `0.15`
values are useful design evidence, **not** an approved target and not proof that `0.15` is readable,
accessible, or visually balanced in the current table.

### 3.2 Owner decisions required

1. **Appearance:** keep `0.08` in both themes, restore the historical `0.15`, or approve four new
   values after side-by-side review. “Close the gap” is not specific enough to choose among them.
2. **Scope:** backgrounds only, or also the selected/hover/drag states. The recommended first packet
   is backgrounds only.
3. **Ownership:** put a live `[data-theme="dark"]` token override in `theme-dark.css`, which loads
   last, or keep all feature tokens page-local in `pages-workout-plan.css`. Page-local ownership is
   cleaner if elimination of `theme-dark.css` remains a future ambition; late shared-theme ownership
   follows the WP4.4-j convention. Either works without a template change.
4. **Approval artifact:** approve element-scoped dark-mode before/after captures for all four colors,
   including normal cells, row edges and badges. Decide explicitly whether a committed targeted
   baseline is wanted; do not silently rebaseline the existing full-page corpus.

### 3.3 Exact missing prerequisites

- A written visual target for all four dark background tokens and a contrast/readability review.
- A superset-populated probe state. P3-a0 established that its probe database had no
  `superset_group`, so ordinary seeded visual coverage cannot certify this surface by construction.
- A rendered, element-scoped comparison. The tint is alpha-composited behind table cells; checking
  only the row's computed `background-color` can miss the final pixels. The existing
  `i_element_pixel_diff.mjs` is the closest reusable instrument, but using/retargeting it belongs to
  the future packet, not this audit.
- Replacement of `test_the_deferred_superset_tint_was_not_added`: its present negative assertion
  (`"superset" not in theme-dark.css`) records C11's deferral, not the future product contract.
- A current green or explicitly reconciled Windows/Linux visual proof environment (§7).

### 3.4 Proposed packet structure

| Packet | Purpose | Production writes | Stop/checkpoint |
|---|---|---|---|
| S0 — visual decision | Produce four-color light/dark specimens and record the chosen values, owner location, and scope | none | Owner selects the appearance and whether a targeted baseline is desired |
| S1 — probe and contract | Create a contained, disposable superset probe state; add semantic/rendered contracts and prove red paths | tests/probe tooling only | Stop if all four groups cannot be exercised without touching the committed visual DB |
| S2 — implementation | Add only the four dark token overrides and replace the deferral pin with a positive contract | one CSS bundle plus scoped tests/evidence | Owner reviews before/after; intentional differences limited to dark superset rows |
| S3 — integration | Run the CSS/page gate and record the decision; no unrelated cleanup | evidence/status paths authorized for this packet only | No unexplained visual or functional change |

### 3.5 Change-shape verdict

| Surface | Needed? | Reason |
|---|---|---|
| `@layer` membership | No | Token override can stay unlayered in either existing bundle |
| Template/load order | No | The page bundle already loads before late `theme-dark.css`; a page-local dark rule also works |
| Page bundle | Maybe | Required only if the owner selects page-local ownership |
| JavaScript | No | JS already emits the four stable class/token indices and the live `data-theme` state |
| Screenshots/baselines | Review required; regeneration not automatic | This is an intentional visual change. Existing full-page baselines may not contain a linked superset; a targeted proof is still required |

**Expected effect:** dark-mode superset row grouping becomes intentionally stronger or differently
balanced; light mode and grouping behavior remain unchanged.

## 4. Option 2 — the 235 declarations behind the Packet-a layer span

### Assessment: DEFER

The historical number is a **withheld candidate ceiling**, not a deletion-certified set.

### 4.1 Why they were withheld

Packet h's dry-run projected 247 cuts / 336 declarations / 554 lines. It shipped 87 cuts / 101
declarations / 138 lines and withheld 160 cuts / 235 declarations / 416 lines because the Packet-a
contract re-derived this absolute span from the working tree:

```text
components.css: @layer workout, openLine 3539, closeLine 4104
```

Deleting any preceding or enclosed line changed one or both line numbers and failed the frozen-span
contract. Packet h had no authority to re-pin it, and editing the test just to accommodate the
deletion would have defeated the layer-membership freeze. C8 therefore closed that region.

The distinction in Packet h's evidence is important:

| Historical population | Count | What was actually proved |
|---|---:|---|
| Dry-run declarations | 336 | Projected only |
| Above the close line and shipped | 101 | Triple-intersection/removal-oracle certified |
| Behind the span and withheld | 235 | Reported dead by the broad measurement, but never entered h's 103-candidate removal-oracle run |

The later 103-candidate run itself found one live declaration and one `neverProbed` declaration.
That false-dead rate is evidence against promoting the 235 from “measured dead” to “safe to delete.”

The old manifest is also stale. `components.css` has changed since Packet h (including the packet-i
selector repair and later theme-alignment work), and h's gitignored census, range, certification,
differential, manifest, and apply artifacts are not committed at audited HEAD. The current span is
still 3539–4104, but matching line numbers do not preserve old candidate identities or verdicts.

### 4.2 Exact missing prerequisites

- New Gate 0 and Gate 1 authority naming `components.css`, the Packet-a span contract/baseline, and
  the narrow right to re-pin **absolute positions after proof**. Retained rule membership must not
  change merely to make deletion easier.
- A fresh, structural current-HEAD candidate inventory. No old line-number manifest may be reused.
- A committed or otherwise reviewable removal oracle with same-CSS controls, known-live controls,
  restoration/idempotence checks, CSSOM-to-source alignment, and executed red paths. No such
  committed removal oracle exists now.
- A current probe database under `artifacts/`, with `DB_FILE` containment, `TESTING` unset where the
  historical method requires production startup behavior, post-startup freezing, complete route
  and element blast coverage, and no writes to the committed visual fixture or user database.
- Triple authority per declaration: current census non-winner **intersection** independent
  zero-winner recount **intersection** removal-oracle `deadCertified`. `neverProbed`, unresolved,
  pseudo/interaction-only, JS-only and uncovered candidates are excluded.
- AST proof that the before/after layer contains exactly the same retained rules/declarations and
  has the same layer ordering. Only absolute line positions may be re-pinned.
- A freshly measured Linux/Windows visual state. This project is preservation-only: baseline
  regeneration is not a repair and any packet-caused raster difference is a rollback trigger.

### 4.3 Proposed packet structure

| Packet | Purpose | Production writes | Checkpoint |
|---|---|---|---|
| L0 — current census and authority | Reconstruct structural candidates, current layer AST, contract coupling and attainable ceiling | none | Owner decides whether the measured current ceiling justifies tooling work |
| L1 — certification apparatus | Build/recover the removal oracle, probe DB, controls and red-path tests | tools/tests only | Instrument must fail every known-live control; otherwise stop |
| L2 — candidate certification | Run the three independent measurements and publish per-declaration exclusions | none | Owner approves only the certified intersection; an empty/small set may end the project |
| L3 — pure deletion | Delete the approved set and narrowly re-pin the absolute span evidence to the proven retained membership | `components.css` plus scoped contracts | Full CSS gates; zero unexplained computed/pixel/functional change |
| L4 — closeout | Reconcile permanent contracts and measured yield | authorized evidence/status paths only | Confirm no layer order/membership, template, JS, bundle or baseline movement |

### 4.4 Change-shape verdict

| Surface | Needed? | Reason |
|---|---|---|
| `@layer` membership | **Must not change** | Only the absolute span pin may move after retained membership is proved identical |
| Template/load order | No | This is a declaration deletion inside an existing bundle |
| Page bundles | No expected change | Any required page-bundle edit means the candidate is cascade-coupled and should be excluded or separately authorized |
| JavaScript | No expected change | JS-applied/interaction-only candidates require coverage or exclusion, not JS edits |
| Screenshots/baselines | Comparisons required; updates forbidden as repair | The target is zero user-visible effect |

**Yield:** no more than the historical 235 declarations / 416 lines, and probably less after current
source reconstruction, coverage exclusions, and oracle contradictions. **Expected effect:** none.

## 5. Option 3 — reopen P3 after P3-a0

### Assessment: DECLINE at present

P3-a0 did what its split was designed to do: it made the next investment expensive enough to stop
before production CSS was touched. Reopening is feasible in the technical sense, but not justified
as a standalone cleanup at the current cost/risk/value ratio.

### 5.1 What P3-a0 actually concluded

P3-a0 assessed all 19 then-committed CSS-audit tools:

- **9 reusable unmodified:** `specificity.py`, `resolution_check.py`, `measure.py`,
  `i_seed_probe_db.py`, `runtime_probe.mjs`, `j_theme_differential.mjs`, `j_diff_theme.mjs`,
  `stylelint_surfaces.mjs`, and `j_known_live_mutation.mjs`.
- **3 conditionally reusable:** `i_element_pixel_diff.mjs`, `j_shadow_certification.mjs`, and
  `j_theme_dark_inventory.mjs`.
- **7 not reusable for P3's job:** `emit_baseline.py`, `i_five_route_computed.mjs`,
  `i_known_live_mutation.mjs`, `i_diff_computed.mjs`, `i_diff_g3.mjs`, `n4_regions_abc.mjs`, and
  `visual_helper_band_proof.mjs`.

It therefore priced **nine new tools**, not the seven originally projected:

`p3_removal_oracle.mjs`, `p3_census.mjs`, `p3_zero_winner_check.mjs`, `p3_ranges.mjs`,
`p3_build_manifest.mjs`, `p3_apply.mjs`, `p3_family_controls.mjs`, `p3_blind_spots.mjs`, and
`p3_seed_probe_db.py`.

No committed tool was a removal oracle. The owner compared that build against Q6's realistic
outcome—“a small certified deletion plus a reusable instrument, not a gutted file”—and terminated
the arc.

One prerequisite has improved since a0: standalone Q10 work (`5dd0b22`) made the shared
`visual-helpers.ts` blind-spot register bidirectional and now pins 22 entries / 52 declarations.
That removes the old **shared-register repair** as an open defect. It does **not** create a removal
oracle, a P3-local classification, a superset probe DB, family controls, or independent deletion
authority. A reopened P3-a1 must re-audit whether `p3_blind_spots.mjs` can be reduced or replaced by
the repaired shared apparatus; it may not simply lower nine to eight. Active visual-helper work
also makes any tool-reuse count provisional.

### 5.2 Remaining packets, gates, and uncertain yield

| Packet | Work and output | Mandatory checkpoint | Cost/risk |
|---|---|---|---|
| **P3-a1** | Repair/build/certify the oracle set; P3-local blind-spot discipline; contained superset-seeded probe DB; `DB_FILE` guard; frozen DB artifact; first committed pytest coverage for the `.mjs` instruments; executed red paths | **AB-1:** stop if known-live controls, restoration, alignment, idempotence, or candidate resolution fail | L by the old plan; likely the largest tooling packet; source/tool inventory must be re-priced |
| **P3-b** | Machine-derived disjoint partition of every declaration: F1 tokens, F2 residual important paint, F3 dark/agnostic normal rules, F4 expected-live Workout Controls, F5 interaction/JS/pseudo states, F6 reduced motion; run the ancestor-composited check | **Owner yield checkpoint / AB-2:** proceed, narrow, or end as audit-only | M–L; zero production CSS; deletion yield first becomes knowable here |
| **P3-c** | Pure deletion of the certified F2/F3 intersection; `.frame-header` remains excluded absent a new owner ruling | **D1 before first cut**, then full CSS/visual/Linux gates; per-family AB-3 narrowing | L; preservation-only and serial with P3-d |
| **P3-d** | Independently certify/remove the 16 declarations in the legacy F1 token block using a per-token consumer graph and route coverage | Separate go/no-go; abandon independently if any consumer is unprobed or resolution changes | M–L for at most 16 declarations; exact custom-property contract needs a justified re-pin |
| **P3-e** | Arc-wide contracts, full integration, 0/0 computed differential, block-budget and evidence reconciliation; canonical status edits only under new authority | Final integration checkpoint | M; no production CSS, but broad verification and single-writer documentation |

The old plan's 74-block floor permits at most 24 removed blocks arc-wide unless separately amended;
P3-d consumes one of those blocks if it proceeds. F4, F5, F6 and `.frame-header` are excluded or
retained; P3-d's ceiling is 16 declarations. These constraints explain why the deletion yield is
both **unknown until P3-b** and structurally unlikely to approach the file's 574 lines.

### 5.3 Self-certification risk and missing prerequisites

Deletion authority remains:

```text
(removal oracle ∩ census ∩ independent recount) × known-live family controls
```

P3-a1 would author and certify almost all of that apparatus. Existing full pytest is largely
contract/string protection for this surface, functional Chromium specs do not inspect every paint,
Stylelint is not behavioral proof, and the full-page visual helper intentionally neutralizes
properties P3 wants to classify. The repository's prior `occurrences <= 1` and one-way blind-spot
checks demonstrate that a self-authored green control can be unable to fail. Red-path fixtures,
known-live mutations and the a0/a1 split reduce this risk but cannot eliminate it.

Before reopening, all of the following are missing:

- A fresh owner decision and new Gate 0/Gate 1 based on current source, current Q10 state, current
  visual helpers and current Linux policy—not a revival of the 2026-08-02 signatures.
- A new 19-plus-tool inventory and a revised a1 price; nine is the last measured starting point,
  not a guaranteed current count.
- A new `theme-dark.css` digest, ceiling and family partition; #464 invalidated a0 provenance.
- Resolution of the current Linux baseline/gate failure and replacement of the spent N8 ledger.
- An independence decision: at minimum an adversarial review and separately authored mutations;
  preferably an independent implementation/review of one of the census/oracle legs.
- An explicit economic threshold at P3-b. “Any nonempty yield” is technically sufficient under the
  old plan but is not a sound reason to buy a five-packet continuation.

### 5.4 Change-shape verdict

P3-c/d should require no template, load-order, bundle-membership, JS, layer-membership or screenshot
baseline change. They do require JS/interaction-aware coverage and rendered superset checks. A need
to change production code outside `theme-dark.css` is an escalation, not an implementation detail.
Any visible difference is a rollback trigger.

**Expected effect:** none. **Recommendation rationale:** decline as a standalone cleanup. Reconsider
only if the removal-oracle platform is funded for multiple concrete consumers (for example, both P3
and the 235-declaration project), and only after P3-b's owner checkpoint is repriced to stop on weak
economic yield, not merely an empty set.

## 6. Option 4 — unlink or eliminate `theme-dark.css`

### Assessment: DECLINE at present

This is a separate, highest-risk project. “The file is largely inert” does not mean “the link is
unnecessary.” The bundle still owns live late token remaps, normal declarations, reduced-motion and
interaction/JS states, and expected-live Workout Controls rules. Unlinking without migrating those
owners would alter dark rendering across the application.

### 6.1 The two possible strategies

| Strategy | Feasibility | Consequence |
|---|---|---|
| Certify every declaration dead, then unlink | Not credible from present evidence | P3 explicitly retains or excludes live/custom-property/interaction/reduced-motion families; a zero-file result is not its expected outcome |
| Classify, delete genuinely dead rules, migrate every live owner, then unlink | Technically feasible but very expensive | Most surviving bytes move into `tokens.css`, shared bundles or page bundles; cascade, specificity, layer and load-order ownership must be re-proved globally |

Therefore “eliminate” is primarily an **ownership migration**, not dead-CSS removal. Its value must
be judged on simplified ownership and loading, not on claiming all 574 lines as deletion yield.

### 6.2 Exact missing prerequisites and owner decisions

- A product/architecture reason strong enough to justify a global dark-theme migration: fewer
  bundles, clearer ownership, different token architecture, or a measurable runtime benefit.
- A whole-file current classification covering the families P3 excludes: custom properties,
  expected-live controls, hover/focus/pseudo/JS states, `.value-changed`, reduced motion and the
  pinned `.frame-header` behavior.
- A destination map for every retained declaration and token, including whether shared owners live
  in unlayered `tokens.css`/components, in page bundles, or in a new explicit layer. “Move it to the
  nearest file” is not sufficient because late unlayered precedence is part of current behavior.
- An owner decision on whether to preserve the current eight-global/route-bundle contract or adopt a
  new one; `templates/base.html` must be explicitly unfrozen for this project.
- An owner decision on the superset tint before migration. Adding a new override to a bundle marked
  for elimination creates avoidable churn; if desired, the tint should land first with its durable
  owner selected.
- A first-paint/theme-initialization contract across stored dark, stored light and system preference,
  including flash-of-wrong-theme behavior. JS need not change, but its `data-theme` timing must be
  proved against the new CSS loading shape.
- A replacement for all ten link-class assertions across three test files, plus current cascade and
  versioning contracts. These must become positive assertions about the new ownership/load order,
  not merely have the old assertions deleted.
- A stable cross-platform visual oracle and a current per-route dark-state inventory. A preservation
  migration gets no baseline update; any intentional redesign must be split into a separate product
  packet and reviewed as such.

### 6.3 Proposed packet structure

| Packet | Purpose | Checkpoint |
|---|---|---|
| U0 — business case and whole-file inventory | Current declaration classification, live-state matrix, destination options, byte/request/runtime value | Owner chooses migration or stops; do not assume unlink is the goal after costs are visible |
| U1 — target architecture | Exact owner/destination/load/layer map for every retained family; positive contract design; first-paint plan | Gate 1 and owner approval of bundle and layer topology |
| U2…Un — serial family migrations | Move one coherent family at a time while the old link remains; prove light/dark ownership and interaction states | Each packet must be behavior-preserving and independently reversible |
| U-final-1 — empty-bundle proof | Show no remaining declaration or consumer depends on the bundle; full app and visual gates with the link still present | Owner checkpoint before changing `base.html` |
| U-final-2 — unlink/delete | Remove the global link and file, update cache/version/load-order contracts and run the complete gate again | Zero unexplained first-paint, computed, functional or raster change |

### 6.4 Required change-shape

| Surface | Needed? | Risk |
|---|---|---|
| `templates/base.html` / load order | **Yes** | Global; every extending route is affected |
| Shared/page CSS bundles | **Yes** | Live declarations need destinations; page splitting can multiply definitions |
| `@layer` membership | Maybe, and dangerous | Moving an unlayered late rule into a layer can reverse normal and `!important` precedence |
| JavaScript source | Probably no | Keep `data-theme`; change only if a separately approved theme architecture requires it |
| JavaScript behavior tests | **Yes** | Theme initialization, toggling, persisted/system states and JS-applied CSS states remain in blast radius |
| Screenshots/baselines | Full comparison yes; update no for migration | The target is pixel-equivalent behavior. A redesign must be separate |
| Tests/contracts | **Yes** | Ten link assertions and multiple order/content ceilings encode R4 and current ownership |

**Expected effect:** none if successful. Any intended visual change should be removed from this
project. **Value caveat:** one network request and one source file disappear, but much of the CSS may
only relocate; without a demonstrated ownership simplification, the project can increase complexity.

## 7. R2.4 and Linux visual-gate overlap

The audited canonical state cannot support a new preservation claim:

- The committed Linux inherited-red ledger says it is **spent as an operational rule** and must be
  remeasured before a new packet uses it.
- The last canonical open-work state still presents R2.4—whether `visual-linux` joins the release
  gate—as an unsigned adopt/decline/defer decision. Reaching a run-count threshold never authorizes
  promotion by itself.
- Unmerged branch `docs/deep-gate-linux-visual-gate0-20260831` records a 2026-08-31 scheduled run at
  a later head with 65 failures, 17 not run and 18 passed; the same broad result was already observed
  manually at this audit's HEAD. It identifies an unsynchronized rendering-input/Linux-baseline
  state and an unresolved runner-image confounder, and proposes a compare-only Gate-1 experiment.
  This branch is **non-authoritative until merged**, but it is active evidence that the proof system
  is moving and currently red.
- That active line of work overlaps `e2e/visual-helpers.ts`, visual contracts, the Linux ledger and
  deep-gate/release policy—the exact evidence surfaces every option above would depend on.

Required sequence:

1. Finish and merge (or explicitly abandon and supersede) the current Linux visual diagnosis and
   any visual-helper robustness work.
2. Establish the current Windows and Linux baseline state, compare-only behavior, exemption set and
   operative ledger. Record the owner outcome for R2.4 separately from baseline correctness.
3. Rebase/revalidate this audit on the resulting main HEAD.
4. Only then run S0/S1 for the tint or a Gate-0 census for another option.

If R2.4 is adopted, future production-CSS packets must treat the promoted context as part of their
blocking release proof. If it is declined or deferred, the repository's static-CSS quality gate
still requires the Linux deep gate for these packets; the policy decision does not make Linux
rendering evidence optional.

The tint differs from the other three options here: its visual delta is intended and requires
owner-reviewed before/after evidence, potentially followed by a separately approved baseline
change. The 235-declaration, P3 and unlink-migration projects are preservation work and must not
regenerate baselines to turn a red result green.

## 8. File and workflow overlap

| Surface | Superset tint | 235 declarations | Reopen P3 | Unlink/eliminate |
|---|---|---|---|---|
| `static/css/pages-workout-plan.css` | Possible durable owner | Read/coverage only | Read/rendered hazard | Possible destination for live page rules |
| `static/css/components.css` | Read due cell compositing | **Primary production file** | Read as competing owner | Possible destination/source owner |
| `static/css/theme-dark.css` | Possible durable owner | Read as late competitor | **Primary production file** | **Source to classify/migrate/delete** |
| `static/css/tokens.css` and other shared bundles | No expected write | Read competitors | Read competitors | Likely destinations |
| `templates/base.html` | No | No | No | **Mandatory write** |
| Workout Plan JS | Read/functional proof | Read if candidate state is JS-created | Read/interaction proof | Regression proof; source change unlikely |
| `tests/test_css_wp4_4_theme_dark_contracts.py` | Replace one deferral assertion if theme-dark owns tint | No | Narrowly re-pin certified state | Replace/remove R4 ceilings with positive migration contracts |
| Packet-a baseline/span contracts | No | **Narrow authorized re-pin required** | Read/shared apparatus | Possible cascade topology update |
| P3/Q10 CSS-audit apparatus | Rendered helper may be reused | Oracle patterns/tools may be shared | **Primary tooling dependency** | Classification/oracle inputs reusable, but insufficient alone |
| Visual helpers, Win/Linux baselines and ledger | Targeted intentional-delta proof | Preservation proof | Preservation proof plus blind-spot exclusions | Global preservation proof |
| Deep gate / R2.4 policy | Sequencing dependency | Sequencing dependency | Sequencing dependency | Sequencing dependency and largest runtime cost |

Do not run the 235-declaration project, P3, or unlink migration concurrently. They share cascade
competitors, visual apparatus, contract assumptions and—in the latter two cases—the same theme
surface. The tint is source-disjoint if page-local, but it still changes the rendered oracle and
should land before any later theme classification so the later project measures the intended
product state.

## 9. Recommended investment order

1. **Linux/R2.4 prerequisite work first.** Stabilize and record the current cross-platform visual
   contract; then revalidate this report against the merged HEAD.
2. **Superset tint, if the owner wants the product change.** It is bounded, visible, and delivers
   direct user value. Land it before future P3/unlink classification, with durable ownership chosen
   deliberately.
3. **Optionally fund one shared oracle business case.** Re-price whether a committed removal oracle
   serving both the 235-declaration project and P3 is worth building. Do not label this “continue
   WP4.4/P3”; it is a new tooling investment with two potential clients.
4. **If funded, audit the 235 region before reopening P3.** It has a historical bounded candidate
   ceiling and avoids `theme-dark.css`'s whole-file self-certification problem. Stop after L0 or L2
   if the current yield is weak.
5. **Keep P3 declined unless shared-tool reuse materially changes its price.** If reconsidered,
   restart at a new a1 price and retain the P3-b owner abandonment checkpoint.
6. **Keep unlinking declined.** Revisit only after a concrete target CSS architecture and measurable
   benefit exist. If pursued, use the migration packet series in §6; do not treat P3 completion as
   automatic unlink authority.

## 10. Owner decision queue

| Option | Decision needed before any future write |
|---|---|
| Superset tint | Choose the four dark values, background-only scope, durable owner, and review/baseline artifact |
| 235 declarations | Decide whether a fresh current census ceiling justifies oracle work and authorize a narrow retained-membership span re-pin |
| P3 | Explicitly reopen under new gates, fund/re-price the nine-tool starting estimate, choose independent review, and set an economic yield threshold |
| Unlink/eliminate | Approve a target ownership/load/layer architecture and a business benefit; unfreeze `base.html`; decide migration versus redesign |
| Cross-cutting | Resolve the current Linux visual state and separately decide R2.4 adopt/decline/defer |

## 11. Final recommendations

- **Superset dark tint — PROCEED, conditionally.** Best value-to-cost ratio, but only as a named
  product change after visual-gate stabilization and an owner appearance decision.
- **235 Packet-a-span declarations — DEFER.** Feasible as a standalone removal-certification
  project; the historical 235 are not certified and the likely current yield is lower.
- **P3-a1 through P3-e — DECLINE at present.** Technically structured and checkpointed, but still
  five packets, a nine-new-tool starting price, high self-certification risk and uncertain small
  yield.
- **Unlink/eliminate `theme-dark.css` — DECLINE at present.** It is a global live-rule migration,
  not the natural closeout of P3, and has the highest cost and blast radius for mainly structural
  value.
