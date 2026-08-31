# Bounded shared-CSS audit: bare `.scale-btn` and table breakpoint helpers

## Audit boundary and disposition

This is a planning-only, read-only source/history audit. No server, browser, workflow,
test suite, tag, pull request, database, screenshot, baseline, or external system was
run or changed. The only repository change made for this audit is this report.

- **Audited HEAD:** `b36ea9e1a3d7e0e37918e9db4198cb4bf7e0ecf8`
- **Starting worktree:** clean
- **Audit date:** 2026-09-01
- **Required operating sources read:** `AGENTS.md`, `CLAUDE.md`,
  `docs/MASTER_HANDOVER.md`, `docs/REFACTOR_PLAN.md`, and
  `docs/ai_workflow/PARALLEL_WORKFLOW.md`
- **Original packet evidence read:**
  `docs/CSS_PHASE4_WP4_4_D1_A11Y_EVIDENCE.md` and
  `docs/CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md`
- **Direct contracts read:** `tests/test_css_wp4_4_a11y_contracts.py` and
  `tests/test_css_wp4_4_layout_contracts.py`
- **Successor evidence read:** `docs/css_scale_btn_cleanup/{PLANNING.md,EVIDENCE.md}`
  and `docs/css_table_helpers_cleanup/{PLANNING.md,EVIDENCE.md}`

The commissioning premise is stale at audited HEAD. Both families were deferred by the
original WP4.4 packets, but both were subsequently audited and deleted atomically:

| Family | Original deferral | Later completion | Current CSS state |
|---|---|---|---|
| bare `.scale-btn` | WP4.4-d1, `59e5b10e8bd1c990121f5805f89a6fa8458dad3f` | PR #302, `9c8377745d4aee7d45e0ebf169d29106fcf6660d` | 0 exact-token rules |
| `.tbl-show-*` / `.tbl-hide-*` | WP4.4-e, `1346a353c260aefaeb6ad89224beb5b162364ed9` | PR #300, `b6550e6cf9304dda44f35c1ed0886d3c90451626` | 0 family rules |

`docs/MASTER_HANDOVER.md` and `docs/REFACTOR_PLAN.md` still carry the old deferred/gated
status. Current source, current contracts, the successor evidence, and the two merged
commits contradict that status. Those canonical documents are explicitly outside this
audit's write authority and remain unchanged. A future status-document reconciliation
would be a separate, owner-authorized documentation packet, not a CSS packet.

## A. Bare `.scale-btn` family

### Exact inventory

The eleven source identities below are reconstructed from the parent of the deletion,
`ee1a5decf0c41d10a65b6a6518d87a5f477f3351`. Line numbers refer to that revision of
`static/css/a11y.css`; they are not current line numbers.

| # | Selector | Rule/block lines | At-rule | Declared properties |
|---:|---|---:|---|---|
| 1 | `.scale-btn` | 128–143 | none | `display`, alignment, dimensions, padding, border, background, color, typography, radius, cursor, transition |
| 2 | `.scale-btn:hover` | 145–148 | none | `background`, `color` |
| 3 | `.scale-btn:focus` | 150–153 | none | `outline`, `outline-offset` |
| 4 | `.scale-btn.active` | 155–159 | none | `background`, `color`, `box-shadow` |
| 5 | `.scale-btn.active:hover` | 161–163 | none | `background` |
| 6 | `.scale-btn[data-scale="1"]` | 166–168 | none | `font-size: 0.65rem` |
| 7 | `.scale-btn[data-scale="2"]` | 170–172 | none | `font-size: 0.7rem` |
| 8 | `.scale-btn[data-scale="3"]` | 174–176 | none | `font-size: 0.75rem` |
| 9 | `.scale-btn[data-scale="4"]` | 178–180 | none | `font-size: 0.8rem` |
| 10 | `.scale-btn[data-scale="5"]` | 182–184 | none | `font-size: 0.85rem` |
| 11 | `.scale-btn` | 312–315 | `@media (max-width: 991.98px)` | `flex: 1`, `max-width: 36px` |

This is eleven rule identities but ten distinct selector strings: members 1 and 11 have
identical selector text. Source range plus enclosing at-rule is therefore mandatory for
identity; substring presence cannot tell the two rules apart. The family contained no
`!important`, custom-property, or `@layer` change.

At audited HEAD:

- `static/css/a11y.css` has **0** exact-token `.scale-btn` definitions.
- The former `@media (max-width: 991.98px)` shell remains empty, with an explanatory
  comment.
- The live `.scale-btn-compact` family remains separate. It is not a bare `.scale-btn`
  match because CSS class matching uses whole tokens.

### Definitions and consumers

Product/source enumeration, using exact-token discrimination:

| Surface | Bare-family reference | Classification |
|---|---|---|
| `static/css/a11y.css` | 0 at audited HEAD; 11 in the pre-deletion parent | definition site, now absent |
| `static/js/accessibility.js:144` | `document.querySelectorAll('.scale-btn[data-scale]')` | query only; attaches click listeners to returned nodes |
| `static/js/accessibility.js:202` | same query | query only; toggles `.active` and sets `aria-pressed` on returned nodes |
| `templates/**/*.html` | 0 bare-token applications | no static bearer |
| `static/js/**/*.js` other than the two queries | 0 bare-token references | no tracked JS constructor/application site |
| `routes/**`, `utils/**`, `e2e/**` | 0 bare-token product references | no server-side or E2E bearer found |
| `templates/base.html:194,202` | `scale-btn-compact` only | known-live sibling; not a consumer of bare rules |
| `static/css/navbar.css:1054,1467–1468` | `scale-btn-compact` only | known-live sibling styling; not a bare definition |
| `templates/base.html:24` | loads `a11y.css` | bundle load site, not a selector consumer |
| `scripts/css_audit/scale_btn_census.mjs` | multiple synthetic/query references | audit harness, not application runtime |

`accessibility.js` does not construct DOM. Its tracked mutations set `data-scale` on
`documentElement`, toggle `open` on the accessibility dropdown, and toggle `active` /
`aria-pressed` on nodes already returned by the bare-button query. It has no current
`createElement`, `innerHTML`, `insertAdjacent*`, `outerHTML`, `cloneNode`, or `className`
assignment path. The query is therefore a consumer only if some other source first emits
a bearer.

### Verification of the empty-query claim

The claim must be split into two different statements:

1. **A query literal exists.** This proves only that the code is prepared to consume
   matching nodes. It proves neither that a node exists nor that no node can exist.
2. **The current application-produced DOM has no matching node.** This needs a natural
   runtime census with a functioning positive control, plus source evidence about how
   nodes can enter the DOM.

Under this audit's no-browser restriction, there is no fresh runtime execution at
`b36ea9e`. The strongest honest current verification is:

- current tracked-source enumeration finds no bare bearer or constructor;
- the current contract `test_legacy_classes_are_still_unreachable` continues to gate
  template/class-list adoption;
- `test_accessibility_js_still_constructs_no_dom` gates construction primitives in the
  querying module; and
- the dedicated successor evidence recorded a natural full-selector census of zero in
  **1,804/1,804 contexts per selector** before injection.

That historical runtime result was broader than WP4.4-d1's preliminary observation.
WP4.4-d1 measured `.scale-btn[data-scale]` at zero in 160/160 screen contexts and correctly
stopped: its earlier static pass had wrongly treated the JS query as reachability. The
successor packet re-derived the result across 11 routes × 2 themes × 10 widths × 8 scale
levels, plus print and reduced-motion contexts. Thus the empty-set claim is strongly
supported for the tracked application and is consistent with current source, but it is
**not freshly runtime-measured by this audit**.

### Dedicated runtime census and oracle-validity control

The correct packet design, now implemented by `scripts/css_audit/scale_btn_census.mjs`, is:

1. Pin all eleven source identities by LF-normalized source range and enclosing at-rule.
2. Before injecting anything, count bare `.scale-btn` and every complete selector over
   all routes, themes, breakpoint-bracketing widths (including 991/992 around the decimal
   991.98px boundary), scale levels 1–8, print, and reduced motion.
3. Validate the census with known-live controls from the sibling generation:
   `.scale-control-compact`, `.scale-btn-compact`, `.scale-indicator`, and
   `[data-visual-scale-control]`. They must be non-zero before and after mutation.
4. Add a two-sided known-dead control: naturally absent, then positively visible when
   injected. A dead-only result cannot distinguish a working oracle from a blind one.
5. Run a same-CSS repeat and require zero differences.
6. For every family member, create a bearer and a control differing by exactly one
   selector compound. Exercise real hover/focus state, `.active`, each `data-scale`, and
   member 11 inside its actual media condition. Derive sentinels from the rule's own
   declarations, settle animation, and prove apply and revert.
7. Resolve ownership through CDP source URL/range rather than selector substring. This is
   essential for member 8, whose `font-size` equals the base rule, and for the two identical
   `.scale-btn` selector texts.
8. After whole-family removal, require every source identity to disappear while all live
   controls remain visible, then run a rest-state collateral-damage differential.

The recorded run passed the live controls in **1,760/1,760** screen contexts on both sides,
passed the two-sided known-dead and same-CSS controls, flipped **22/22** member×theme source
identities, and found **0 differences across 339,120 rest-state records**.

### Dormant functionality versus removable CSS

The following evidence distinguishes the two:

| Finding | Dormant functionality, retain | Removable CSS |
|---|---|---|
| Natural bearer | Any non-zero full-selector census, or a supported state/route that creates one | Zero with a positive census control across the declared state matrix |
| Construction path | Template, JS, route, generated markup, or planned feature can create the token | No application or construction site; query is consumer-only |
| Rule function | A member cannot be made observable under its real state, so absence after deletion cannot be proved | Each source identity is observable before, or its unobservability is independently proved to be cascade-inert, and disappears after |
| Product intent | UI is intentionally dormant/feature-flagged and expected to return | Live compact generation owns the shipped function; bare generation has no producer |
| Future safety | No contract would catch reactivation | Reachability, sibling-definition, and live-generation contracts turn reactivation into a deliberate decision |

The bare family met the removable side. The JS queries themselves remain dormant code;
their existence was deliberately not generalized into either reachability or deadness.

### Evidence currently available

- Exact pre-deletion inventory and current zero-definition state.
- Current static census: two JS queries, zero tracked product bearers/constructors, and
  only exact-token-distinct compact siblings.
- WP4.4-d1's preliminary empty query census and explicit refusal to infer from it.
- Dedicated 1,804-context natural census with positive controls.
- Per-member synthetic/interaction certification and CDP source-range ownership.
- Post-deletion 22/22 source-identity flip and live controls on both sides.
- Zero rest-state differential across 339,120 records.
- Current contracts preserving absence, live compact rendering, the empty breakpoint
  shell, JS no-construction premise, the 1–8 token ladder, sibling-surface absence,
  custom properties, and layer count.
- Recorded shared-surface gates and six executed adversarial red paths in the successor
  evidence.

### Evidence still missing

- A fresh browser census at audited HEAD is intentionally missing because this audit is
  static/history-only. The committed harness makes such a re-check possible later.
- The durable reachability contract is narrower than this audit's source sweep: it parses
  template class attributes and selected `classList` calls, while the no-construction
  contract is limited to `accessibility.js`. A different JS module could theoretically
  introduce a dynamically assembled bare token through another assignment form without
  being caught by those exact tests. Current source contains no such path.
- External DOM injection (extensions/devtools/third-party scripts) is outside the
  application reachability claim and is neither proved nor required.

These are residual assurance limits, not evidence that the removed rules are needed.

### Proposed future packet and owned paths

No new deletion packet should be opened: the bounded packet already completed. The
historically correct packet owned:

- `static/css/a11y.css` — atomic family deletion only;
- `tests/test_css_wp4_4_a11y_contracts.py` — absence, reachability, preservation, and
  red-path contracts;
- `scripts/css_audit/scale_btn_census.mjs` — committed reproducible census;
- `scripts/css_audit/p3_ceiling.py` — audit-tool assessment row only;
- `docs/css_scale_btn_cleanup/**` — plan/evidence;
- `docs/test_inventory/TEST_INVENTORY.{md,json}` — only because test nodes changed.

If future source adopts a bare scale button, the proper packet is a **whole-family
reactivation/design packet**, not a one-rule CSS repair. It would own the producer, the
complete family (or a newly designed replacement), accessibility behavior, focused
contracts, and fresh runtime evidence together. A verification-only re-census needs no
tracked writes.

### Tests and mutation/red-path proof required

For any future re-adjudication:

- absence must be rule-head/source-shape based, with member 11 restored alone as the
  adversarial duplicate-selector mutation;
- a mutation adding a DOM builder to the querying module must red the reachability premise;
- a mutation adding the bare selector to a sibling bundle must red;
- the compact generation and `data-scale` 1–8 token blocks must red if weakened;
- the empty 991.98px shell contract must red if a rule reappears;
- every new/changed contract must be run in its failing state and the tree restored
  byte-identically; and
- runtime acceptance requires the before/after live controls, source-range flips, and
  collateral-damage differential described above.

The successor evidence records **6/6** adversarial paths and the focused contract file
green after restoration. This audit did not rerun them.

### Stop conditions

Stop and retain/reinstate the **whole family** if any of the following occurs:

- a natural bare bearer is found;
- any supported producer or intentional dormant feature is found;
- a known-live, known-dead, or same-CSS control fails on either side;
- any source identity cannot be distinguished or attributed under its real media/state;
- a post-change source-range flip, sentinel revert, accessibility guarantee, or
  collateral-damage gate fails;
- only a subset of the eleven can be certified; or
- the proposed work expands into the compact generation, JS redesign, focus re-weighting,
  print-rule trimming, snapshots, workflows, or canonical status documents.

At audited HEAD there is an additional stop: **the target no longer exists**.

### Risk, expected value, and recommendation

- **Historical deletion risk:** medium before measurement, because dormant JS, focus
  behavior, duplicate selector text, and a media-only member made a naive grep unsafe.
- **Historical expected value:** modest but real: 11 rules / 29 declarations removed,
  61 net lines reduced, and a misleading superseded UI generation eliminated.
- **Current implementation risk:** any attempt to “continue” would recreate or disturb a
  completed deletion and its contracts.
- **Current expected value of another CSS packet:** negative.
- **Recommendation:** **DECLINE** a new implementation packet. Preserve the zero-rule state
  and contracts. Treat a future bearer as a whole-family product decision, not permission
  to restore an isolated selector.

## B. `.tbl-show-*` / `.tbl-hide-*` breakpoint helpers

### Exact inventory and indivisible cascade map

The nine rules are reconstructed from the parent of the deletion,
`4025295f4de68861a4a56705276f1a2dd50c6c7c`. Line numbers refer to that revision of
`static/css/layout.css`.

| # | Selector | Lines | Condition | Declaration | Family role |
|---:|---|---:|---|---|---|
| 1 | `.tbl-show-sm` | 1594–1596 | base | `display: none` | hidden outside/under base cascade |
| 2 | `.tbl-show-md` | 1598–1600 | base | `display: none` | hidden outside/under base cascade |
| 3 | `.tbl-show-lg` | 1602–1604 | base | `display: none` | hidden outside/under base cascade |
| 4 | `.tbl-hide-sm` | 1607–1609 | `max-width: 820px` | `display: none` | hide in small band |
| 5 | `.tbl-show-sm` | 1611–1613 | `max-width: 820px` | `display: block` | override matching base in small band |
| 6 | `.tbl-hide-md` | 1617–1619 | `821px–1200px` | `display: none` | hide in medium band |
| 7 | `.tbl-show-md` | 1621–1623 | `821px–1200px` | `display: block` | override matching base in medium band |
| 8 | `.tbl-hide-lg` | 1627–1629 | `min-width: 1201px` | `display: none` | hide in large band |
| 9 | `.tbl-show-lg` | 1631–1633 | `min-width: 1201px` | `display: block` | override matching base in large band |

The atomic source range was lines 1589–1634: introducing banner/comment, three base
rules, and all three media blocks. The already empty `LOADING STATE` banner at 1584–1586
was a different family's residue and was deliberately excluded.

The base and override rules are one cascade contract:

| Suffix | `.tbl-show-*` outside band | `.tbl-show-*` inside band | `.tbl-hide-*` inside band | `.tbl-hide-*` outside band |
|---|---|---|---|---|
| `sm` | `none` from base | `block` from later ≤820 override | `none` | host/other CSS default |
| `md` | `none` from base | `block` from later 821–1200 override | `none` | host/other CSS default |
| `lg` | `none` from base | `block` from later ≥1201 override | `none` | host/other CSS default |

Deleting a show base but retaining its override changes it from a bounded show utility to
an unbounded no-op outside the band; deleting an override but retaining its base makes it
always hidden. Retaining a hide override without the rest leaves a partial API with no
coherent counterpart. Therefore the family must be nine rules or zero rules. It must
never be eroded member by member.

At audited HEAD all six class names have zero rule heads in `layout.css` and zero
definition sites in other local/static stylesheets.

### Template, JavaScript, and static references

The pre-deletion parent contained the nine CSS rule heads and the old occurrence-count
contract, but no application site. Current exact/static enumeration finds:

| Surface | Current product references | Result |
|---|---:|---|
| `templates/**/*.html` | 0 | no class application |
| `static/js/**/*.js` | 0 | no literal or dynamically assembled `tbl-show` / `tbl-hide` stem |
| `static/**/*.css` | 0 rule heads | no local or vendored definition |
| `routes/**`, `utils/**`, `e2e/**` | 0 | no server-side/application reference |
| `templates/base.html:21` | loads `layout.css` | bundle load site only |

Current non-product references are the six names in
`tests/test_css_wp4_4_layout_contracts.py`, a precedent note in
`tests/test_css_wp4_4_components_contracts.py`, and documentation/evidence. None is an
application consumer.

The live responsive-table system is a different family: `.col--high/.col--med/.col--low`
disclosure, row-card mode, print rules, `.tbl-controls`, `.tbl-view-mode-toggle`, and the
`ResizeObserver` code in `static/js/table-responsiveness.js`. Those were retained and must
not be conflated with the removed helpers.

### The `display: block` initial-value oracle problem

WP4.4-e injected a bare `<div>` as both probe host and control. A div's UA display is
already `block`. For rules 5, 7, and 9, the candidate and control therefore both computed
to `block`, even while the candidate rule applied. The measurement could not distinguish:

- “the author rule owns `display: block`”; from
- “no author rule applies and the UA gives the host `display: block`.”

WP4.4-e called this an inherent limit and deferred the whole family. The conservative
deferral and no-partial-deletion rule were correct; the characterization of the limit was
not. The limit belonged to the chosen host.

A valid display utility must work on elements whose natural display is not block. The
successor control used valid DOM chains for:

- `<span>` → `inline`;
- `<li>` inside `<ul>` → `list-item`; and
- `<td>` inside `table > tbody > tr` → `table-cell`.

No author CSS was injected to manufacture those baselines. On all three hosts, an
applicable `display: block` rule differs from the control. After deletion, the candidate
returns to the same UA display as its control. This directly proves or falsifies removal.

### Whole-family control and oracle design

The correct control suite is:

1. **Natural full-selector census before injection:** six names across every rendered
   route, both themes, and widths immediately below/at/above 820 and 1200, plus interior
   widths. Pair the zero with live table counts so zero is not a blind crawl.
2. **Three non-block hosts:** candidate and control differ by exactly the helper class;
   both sit in valid ancestor chains.
3. **Control-baseline validation:** for every context, computed display must equal the
   host's UA initial value and CDP must show no author rule declaring `display` on the
   control. A control that already reads an author-owned display voids the record.
4. **Known-live display owners:** `.tbl-controls { display:flex }` and
   `.tbl-view-mode-toggle { display:inline-flex }`, both created at runtime and retained.
   `.tbl-wrap` is an invalid known-live display control because `layout.css` styles it but
   never declares `display`; the first successor run caught exactly that 0/78 defect.
5. **Known-dead two-sided control:** a nonexistent class such as `.tbl-show-zz`, proven
   naturally absent and visible when injected.
6. **Measured applicability:** use `matchMedia` in the page, never nominal width alone.
7. **Structural ownership:** resolve source URL, source range, and enclosing media text
   through CDP.
8. **Post-removal flip:** in every formerly applicable record, require no `layout.css`
   display owner and exact equality with the control's `inline`, `list-item`, or
   `table-cell` value.
9. **Same-CSS and rest-state controls:** require repeat stability and no collateral
   owner/paint/motion change.

The executed matrix was 11 routes × 2 themes × 13 widths = **286 contexts**, three hosts
per context = **858 records per rule**. All nine had non-zero, precommitted denominators;
the three formerly blind overrides were distinguished in 100% of applicable records.
Every rule then flipped in 100% of those records after deletion, while the known-live
controls remained owned in **1,716/1,716** records.

### Evidence currently available

- Exact nine-rule source inventory, three breakpoint bands, and atomic deletion range.
- Current zero product/static references across templates, JS, CSS, routes, utils, and
  E2E source.
- WP4.4-e's original zero census, six observable members, and conservative deferral.
- Measured refutation of the bare-div premise on span/list-item/table-cell hosts.
- Full denominator accounting and non-vacuity checks for all nine rules.
- Structural CDP ownership before and clean flip after for all nine.
- Valid known-live controls, including the recorded `.tbl-wrap` control failure and fix.
- Runtime stylesheet enumeration, including local vendored CSS and the then-loaded
  cross-origin sheets.
- Zero ordinary rest-state differences; known animated Welcome records separately
  classified by the existing blind-spot policy.
- Current C1–C5 contracts: zero rule heads, all-or-nothing shape/band topology, no app
  references, no sibling definitions, and no empty media shells.
- Recorded **12/12** adversarial red paths, including the two-sided proof that a complete
  restoration is green under C2 but red under C1.

### Evidence still missing

- No fresh runtime measurement at audited HEAD was made under this audit's restrictions.
- Unlike the scale-button harness, the bespoke table-helper oracle lived under gitignored
  `artifacts/tblhelpers/`. The evidence contains a reproduction recipe, but the repository
  alone does not retain the exact executable oracle. A future fresh runtime claim must
  reconstruct and revalidate it rather than cite old raw artifacts as current output.
- C3's standing reachability gate intentionally scans templates and production JS. This
  audit additionally found zero in routes/utils/E2E, but those extra trees are not all
  part of C3's durable scope. Any future server-generated inline markup would need a fresh
  census and contract review.
- Remote stylesheets can change independently. They cannot make absent application
  classes reachable by themselves, but any future census must enumerate all sheets the
  browser actually loaded rather than assuming the old fetch result remains current.

### Proposed future packet and owned paths

No new deletion packet is warranted. The completed packet owned:

- `static/css/layout.css` — atomic removal of lines 1589–1634 only;
- `tests/test_css_wp4_4_layout_contracts.py` — replacement C1–C5 contracts;
- `docs/css_table_helpers_cleanup/{PLANNING.md,EVIDENCE.md}`;
- `docs/test_inventory/TEST_INVENTORY.{md,json}` — because test nodes changed;
- gitignored `artifacts/tblhelpers/**` — raw oracle/output, never committed.

If a future consumer needs one helper, the future packet must own **all nine rules as one
API**, the consumer, tests, and a new three-host runtime proof. It may choose to restore the
historical family or design a replacement utility system, but it may not restore only the
apparently needed rule. Current C2 is outcome-independent specifically so that this rule
survives both absence and complete restoration.

### Tests and mutation/red-path proof required

Any future packet must preserve or strengthen:

- **C1:** zero rule heads for all six names while the family is absent;
- **C2:** exactly one of two states—fully absent, or the complete historical topology:
  one base plus one banded override per show class, one banded rule per hide class, and
  three distinct media preludes;
- **C3:** no application reference, including static attributes, `classList`,
  `className`, `setAttribute`, and dynamically assembled stems;
- **C4:** no definition in any sibling/local/vendored CSS tree; and
- **C5:** no empty media shell left by removal.

Required mutations include: re-add one rule; add an override without a base; restore all
nine and prove C2 green/C1 red; remove one from the restored family; collapse all bands
into one query; add template, `classList`, and concatenated `className` consumers; add a
sibling CSS definition; and leave an empty media block. Each must fail the intended
contract, followed by byte-exact restoration and a green focused file.

Runtime proof additionally requires all nine pre-effects, all nine post-flips, valid
control baselines, live controls on both sides, non-zero denominators, and a zero
collateral-damage differential. Pixel equality alone is not candidate evidence because an
unreachable class paints no natural element.

### Stop conditions

Stop and retain/reinstate the whole family if:

- any natural application or supported dynamic producer exists;
- any of the nine rules has a zero or unexplained denominator;
- any host control is author-styled instead of at its UA initial display;
- either known-live display control is not detected before and after;
- any rule lacks structural ownership before or fails to return to its control after;
- any same-CSS, sentinel/revert, rest-state, accessibility, or responsive-table gate fails;
- the result would be a partial family, merged breakpoint bands, or orphaned media shell;
  or
- the work reaches live disclosure/card-mode rules, table-responsiveness JS, templates,
  snapshots, workflows, databases, or canonical status documents without separate
  authority.

At audited HEAD, stop because the target family is already absent and protected.

### Risk, expected value, and recommendation

- **Historical deletion risk:** medium. The family was the only local generic responsive
  show/hide utility, and a bad oracle could mistake UA defaults for author ownership.
- **Historical expected value:** small but positive: 47 dead lines removed atomically and
  a misleading unused capability removed. Stylelint appropriately moved by zero.
- **Future reactivation risk:** medium/high if done member by member; low only under a
  complete API/product packet with the band-topology and runtime controls above.
- **Current expected value of another deletion packet:** negative; there is nothing left
  to delete.
- **Recommendation:** **DECLINE** re-dispatch. Keep all nine absent, preserve C2's
  all-or-nothing invariant, and require a whole-family packet if any consumer appears.

## Combined recommendation

Both bounded families should be closed as **already executed**, not left in a deferred
queue and not re-audited as though the rules still existed. The current technical state is
soundly protected: zero definitions, zero product consumers, and family-specific contracts
that turn reintroduction/adoption into a deliberate decision.

The only actionable discrepancy found by this planning audit is documentation status:
the canonical handover/refactor tables still present the pre-PR #300/#302 state. That is
outside the authorized deliverable and must not be repaired incidentally. If the owner
wants it corrected, commission a documentation-only reconciliation whose evidence base is
the two successor evidence files and merged commits above.
