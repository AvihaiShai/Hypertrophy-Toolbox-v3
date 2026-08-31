# Workout Plan optional refactor audit

Planning-only audit, 2026-09-01. No server, browser, Playwright, test suite,
workflow, database, screenshot, baseline, production source, or canonical status
document was changed or run for this audit.

## Audit pin and validity

- **Audited worktree:** `wt/opt-wp-audit`
- **Audited HEAD:** `b36ea9e1a3d7e0e37918e9db4198cb4bf7e0ecf8`
  (`b36ea9e`, `docs(policy): close V1 and frozen caller residual (#466)`)
- The worktree was clean before this report was created.
- **Post-rebase validation, 2026-09-01:** the publication branch was rebased
  onto `origin/main` at `c809d02461c5c7f9a63d9d92b883e54809ae9adb`.
  The blobs for `static/css/pages-workout-plan.css`,
  `static/css/components.css`, and `static/css/tokens.css` are byte-identical
  to the audited HEAD, so the ten-candidate inventory and its source/cascade
  claims are unchanged. The newer visual-helper/policy record does narrow the
  proof interpretation: a byte-gated plan capture has failed above tolerance
  and then passed on retry, while the terminal contract remains 81 byte-gated
  captures plus five semantic exemptions. A green retry/flaky result is
  therefore not clean zero-difference evidence. The newer Linux Gate 0 also
  records broad terminal visual reds from unsynchronized rendering inputs and
  committed baselines; that does not authorize baseline regeneration or weaken
  the zero-difference requirement. The JS-unit ledger now includes rows 49–55
  and confirms the same T0, strict mark, path-based restart definition,
  non-required status, and unsigned Q4/D2 boundary stated below.
- **Every count, line reference, cascade claim, harness assumption, and packet
  boundary in this report must be revalidated after the active parallel work
  merges and before any future packet is authorized.** Selectors and structural
  anchors, not the line numbers below, are the durable identifiers.

## Current boundary

The shipped Workout Plan refactor boundary remains:

1. WP4.3i-i, i-b through i-h, i-dead, and i-filter-btn are closed. The dead defined-
   token fallback arc is complete, the 14 certified rest-state declarations are
   gone, and the dead `#filter-btn` family is gone.
2. The ten declarations below are **deferred, not classified dead**. The old
   sentinel sweep nominated them, but the required corroborating differential
   was unstable. `tests/test_css_cascade_contracts.py:1285` protects the shipped
   rest-state removal and, at `:1343-1353`, deliberately asserts that the main
   interaction-state families remain.
3. The Page Header block beginning at
   `static/css/pages-workout-plan.css:829` is outside this optional work. Its
   WP4.3i-c contract is `tests/test_css_cascade_contracts.py:951`; its 15/15
   liveness result is closed and must not be weakened or repurposed as a token
   packet.
4. WP4.3i-jm and WP4.3i-o are closed investigations, not queued packet names.
   They are explained below and must not be re-dispatched.
5. The remaining literal/token and `!important` surface is redesign-sized and
   owner-gated. No bulk cleanup packet has begun.

The recommendation is therefore **do not begin production cleanup now**.
Proceed only with a separately authorized, audit/tooling-only animation oracle
packet. Actual deletion remains conditional on that oracle producing a zero-
difference same-CSS control and a zero-difference old/new result for each exact
declaration.

## Exact deferred candidate inventory

All references are to the audited HEAD. “Raw” counts `#hex`/`rgb()`/`rgba()`/
`hsl()`/`hsla()` occurrences in the declaration value. The first seven
declarations are inside `@layer workout`; the three table declarations are
unlayered. Layer membership must not move.

| ID | Current source and exact selector | Declaration | Raw | `!important` | What must remain if it is removed | Recommendation |
|---|---|---|---:|---:|---|---|
| IS-01 | `static/css/pages-workout-plan.css:982`, `#workout[data-page="workout-plan"] .collapse-toggle:focus-visible` | `box-shadow: 0 0 0 4px rgba(79, 140, 255, 0.2), 0 4px 12px rgba(2, 132, 199, 0.2)` | 2 | yes | `outline` and `outline-offset` in the same rule | **Defer.** Delete only if the stabilized focus-visible oracle proves this exact longhand a non-winner. |
| IS-02 | `:1010`, `#workout[data-page="workout-plan"] .collapse-toggle:disabled` | `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1)` | 1 | yes | `opacity`, `cursor`, and `transform` | **Defer.** Forced `:disabled` must be settled and compared; do not infer deadness from a normally enabled template. |
| IS-03 | `:1105-1107`, grouped `#workout… .filter-dropdown:focus`, `.form-select:focus`, and `.uniform-input:focus` arms | `box-shadow: 0 0 0 3px rgba(79, 140, 255, 0.1)` | 1 | no | `outline` and `border-color`; all three selector arms | **Defer.** The evidence table abbreviated this group; the current rule has three arms and all must be dispositioned. |
| IS-04 | `:1315`, `#workout[data-page="workout-plan"] .selection-actions:hover` | three-stop `background` gradient at `:1316-1319` | 3 | no | `transform`; plus any sibling hover declarations not certified in the same run | **Defer.** Certify with IS-05/06 in one selection-actions state matrix. |
| IS-05 | same selector, `:1320` | `border-color: rgba(79, 140, 255, 0.25)` | 1 | no | `transform` and unremoved siblings | **Defer.** Same gate as IS-04. |
| IS-06 | same selector, `:1321-1325` | four-layer `box-shadow` | 4 | no | `transform` and unremoved siblings | **Defer.** Same gate as IS-04. |
| IS-07 | `:1336`, `[data-theme='dark'] #workout[data-page="workout-plan"] .selection-actions:hover` | four-layer `box-shadow` at `:1342-1346` | 4 | no | the dark `background`, `border-color`, and `transform`, which were not in the deferred set | **Defer.** Dark-only proof; never delete the whole rule. |
| IS-08 | `:2522`, `#workout[data-page="workout-plan"] .workout-plan-table tbody tr:hover td` | two-stop `background` gradient at `:2523-2525` | 2 | yes | none if IS-09 is also certified | **Defer.** IS-08 and IS-09 are the whole rule and must be deleted together or retained. |
| IS-09 | same selector, `:2526` | `box-shadow: inset 0 0 0 1px rgba(79, 140, 255, 0.15)` | 1 | yes | none if IS-08 is also certified | **Defer.** Unit boundary with IS-08. |
| IS-10 | `:2537`, `[data-theme='dark'] #workout[data-page="workout-plan"] .workout-plan-table tbody tr:hover td` | two-stop `background` gradient at `:2538-2540` | 2 | yes | the dark `box-shadow` at `:2541`, which was not deferred | **Defer.** Delete only the background declaration if independently certified. |

This is exactly **10 declarations, 21 raw colour occurrences, and 5
`!important` annotations**. The inventory still matches
`docs/CSS_PHASE4_WP4_3I_DEAD_EVIDENCE.md`; no candidate has disappeared since
that evidence was recorded.

Relevant current competing systems include the Calm-Glass table hover owners at
`static/css/components.css:3381-3383` and `:3409-3410`, the selection-actions
owner at `:3954-3965`, and shared collapse-toggle state owners around
`:3575-3584` and `:5076-5081`. These references explain why a deadness audit is
plausible; they do **not** prove which declaration wins after animation settles.

## Why the previous removal proof was unreliable

WP4.3i-dead used two different oracles:

- A unique-sentinel sweep nominated 24 declarations because their sentinels were
  not observed in computed styles.
- A full old/new computed-style differential then compared every element and
  pseudo-element over the 37 affected longhands.

The forced interaction-state same-CSS control—unchanged CSS captured twice—
produced **52 differing records**. A control that changes when the input is
identical cannot attribute an old/new difference to a deletion. Only the rest
state was stable: same-CSS **0/31,074** and old/new **0/31,074**, which is why
only 14 rest-state declarations shipped.

The failure mechanism is concrete in the current source:

- collapse toggles transition `all` for 200 ms (`pages-workout-plan.css:959`);
- filter/form inputs transition `all` (`:1096`);
- selection actions transition `all` for 300 ms (`:1312`); and
- Calm-Glass table cells transition background, box-shadow, and colour for 150
  ms (`components.css:3371-3374`).

Forcing `:focus`, `:focus-visible`, `:disabled`, or `:hover`, or replacing a
value with a sentinel, can start a CSS transition. `getComputedStyle()` then
returns an interpolated value tied to the capture instant. It may contain
neither the old endpoint nor the sentinel endpoint. Two identical runs sampled
at different elapsed times therefore differ, and absence of the exact sentinel
is not proof that the declaration loses.

The stale assumption was “sentinel not observed means dead.” The evidence
disproved it: at most it means “the endpoint was not observed.” The ten
declarations must continue to be described as **unproven**.

## Future animation-stabilization and same-CSS method

Do not solve this by injecting a universal CSS rule that sets
`transition: none !important`. The repository's later CSS work established that
such a suppressor is beatable by layered `!important` and by more-specific
unlayered `!important`; it also changes the cascade being measured.
`scripts/css_audit/runtime_probe.mjs` explicitly is not transition-safe for this
purpose.

Use a browser-timeline/WAAPI method derived from the later, proven pattern in
`scripts/css_audit/j_theme_differential.mjs:146-164`:

1. Start from a fresh worktree cut from then-current merged `main`, a frozen
   visual seed copy, and served-source digests for every CSS bundle under test.
2. Before forcing any state, enable the CDP Animation domain and set playback
   rate to `0`. This freezes animations that already exist and ones created
   later without inserting CSS.
3. Apply the target state with CDP pseudo-state forcing (or the real disabled
   property where appropriate). Exercise every live selector arm, not only one
   representative node.
4. Repeatedly enumerate `document.getAnimations({subtree: true})` until stable.
   Call `finish()` on each `CSSTransition` and finite animation. For an infinite
   animation, set `currentTime = 0` and `pause()`. Fail closed on an exception,
   an unsettled transition, a newly appearing animation after the fixed-point
   pass, or an animation whose target cannot be mapped to the captured node.
5. Wait two animation frames with the playback rate still zero, re-enumerate,
   and assert the animation inventory and computed values are unchanged. This
   is a verification step, not the settling mechanism.
6. Run the unique-sentinel sweep again. Assert **sentinel-took-effect per
   declaration** on a known-live control and record winner/source information
   from `CSS.getMatchedStylesForNode`; a probe that failed to mutate is invalid.
7. Capture all 37 shorthand-expanded longhands plus declaration-owner metadata,
   geometry, and the exact affected element/pseudo-element pixels. Use stable DOM
   paths and fail on missing/extra records.
8. Execute an **A/A same-CSS control** with byte-identical CSS in independent
   fresh contexts using the exact same state matrix. Pass condition: **zero
   differing records, zero owner differences, zero geometry differences, and
   zero affected-element pixel differences in every context**. No animated-node
   exclusion bucket is allowed for these candidates.
9. Only after A/A is green, execute A/B (current CSS versus a deletion-only
   candidate stylesheet). The A/B pass condition is the same absolute zero.
10. Execute a known-live mutation that must produce a non-zero result. If it
    does not, the oracle is vacuous and the deletion packet stops.

Required state/context matrix:

- light and dark themes;
- current desktop, tablet, and mobile visual widths, plus every breakpoint at
  which the target selector changes;
- all three collapse toggles under focus-visible and disabled;
- every live `.filter-dropdown:focus`, `.form-select:focus`, and any live or
  dynamically created `.uniform-input:focus` arm;
- selection-actions rest/hover in both themes;
- odd and even plan-table rows under hover, including simple/advanced modes and
  each populated routine state; and
- normal and `prefers-reduced-motion: reduce`, because current reduced-motion
  rules still leave some opacity transitions and change table transitions.

The output must retain the exact per-record A/A and A/B ledgers, served digests,
animation inventories, state census, and known-live mutation result. A summary
count without the records is insufficient.

## Required future runtime and visual proof

The following is a future gate design, not work performed by this audit.

For any interaction deletion packet:

- Re-run the stabilized oracle above on the packet's fresh base. Any A/A
  difference is an immediate stop; do not explain it away as animation drift.
- Prove the target selector matches the expected number of real elements and
  that every grouped arm is either exercised or explicitly proven unreachable.
- Run the focused CSS cascade contracts and prove their red paths. Update the
  existing presence lock only in the packet that carries certified deletion.
- Run focused functional Chromium coverage at minimum from
  `e2e/workout-plan.spec.ts`, `e2e/exercise-interactions.spec.ts`, and
  `e2e/workout-plan-desktop-contract.spec.ts`; add the superset spec only if the
  affected state reaches its controls.
- Run the Workout Plan rows of `e2e/visual.spec.ts` and the plan thumbnail
  matrix in compare mode with `PW_VISUAL_SEED=1`, on both supported platforms,
  without `--update-snapshots`.
- Because five platform captures are intentionally byte-gate-exempt under the
  terminal visual policy, use element-scoped pixel captures and their pinned
  semantic contracts as well as the available byte-gated screenshots. A green
  full-page rest-state capture alone cannot prove hover/focus safety.
- Scope pixel comparisons to the element under test. The animated fixed navbar
  can contaminate a `main` or full-page locator capture even when the page
  content is unchanged.
- Run focused Stylelint before/after and require no category increase, no layer
  change, no selector-specificity increase, and no `!important` increase.
- Run full pytest and the repository-required functional gate after the focused
  checks.
- Require `git status --porcelain e2e/__screenshots__` to remain empty. Any
  baseline write or any non-zero target-element pixel change is a stop requiring
  a separately authorized visible-change packet.

## Current literal and `!important` audit

### Measured source surface

Static PostCSS/Stylelint measurement at the audited HEAD gives:

| Metric | Current value | Interpretation |
|---|---:|---|
| Physical CSS lines | 5,810 | Historical i-filter-btn closeout was 5,799. |
| Declarations | 2,499 | Historical closeout was 2,496. |
| `!important` declarations | **489** | Stylelint's declaration count. The file has 490 lexical occurrences because #317's explanatory comment also says `!important`; the status docs' 488 declaration count is stale because #317 added one justified hidden-state override. |
| Stylelint warnings | 1,139 | Focused bundle only. |
| Stylelint hardcoded-colour declaration warnings | **452** | Same count as i-filter-btn, but not proof the declarations or values are unchanged. |
| Raw-colour declarations, all CSS properties | **495** | Broader than the Stylelint property allowlist. |
| Raw-colour instances | **744** | 195 hex plus 549 `rgb`/`rgba`/`hsl`/`hsla`. |
| Distinct normalized raw-colour spellings | **459** | Most values are not repeats. |
| Raw-colour custom-property definitions / other declarations | 50 / 445 | Moving a literal into a custom-property definition does not eliminate the source value. |
| Hex instances / distinct hex values | **195 / 121** | The July “~218 hex” figure is no longer current. |
| Unit-bearing value instances | **1,600** in 1,136 declarations | 1,028 px, 408 rem, 92 deg, 31 s, 24 ms, 8 em, 7 vw, 2 vh; excludes percentages and unitless values. |

The most repeated raw colours are still small families: white alpha .05 (12),
white alpha .08 (11), `#fff` (10), black alpha .15 (10), black alpha .25
(10), white alpha .7 (10), white alpha .8 (10), `#dee2e6` (9), accent alpha
.15 (9), and `#6c757d` (8). Repetition alone is not semantic equivalence:
these values span backgrounds, borders, shadows, text, SVG paint, fallbacks,
and theme definitions.

The largest raw-colour declaration clusters are Buttons (113), colour-coded
Workout Controls (67), Muscle Selector (65), Workout Plan table (39), Routine
Cascade (38), dark-mode support (36), and collapse toggles (25). These are all
visible component systems, not mechanical search-and-replace surfaces.

The largest `!important` concentrations are resolution breakpoints (71), Workout
Plan table (69), collapse toggles (63), Inline Controls (54), colour-coded
Workout Controls (48), Buttons (45), the pre-layer prelude (39), Advanced Mode
table rules (33), and input fields (27). De-weighting one declaration can change
the winning owner even when the computed value happens to be equal; static
specificity arithmetic is nomination evidence only.

### Token/fallback conclusions

| Candidate family | Audit conclusion | Mechanical or visible? | Recommendation |
|---|---|---|---|
| Ten interaction-state declarations | Plausible dead declarations, but not certified because the old control failed. | Mechanical **only after** a stable zero-diff proof. | **Proceed with proof packet; defer deletion.** |
| Remaining non-Bootstrap `var()` fallbacks | Exactly five sites remain: one live undefined `--wpdd-shadow-lg` fallback (`:701`) and four live dynamic `--superset-row-color` fallbacks (`:3547`, `:3591`, `:3611`, `:3621`). The i-g contract at `tests/test_css_cascade_contracts.py:1186` locks this boundary. | Live behavior. | **Decline removal.** |
| `var(--bs-*, fallback)` in Muscle Selector | Bootstrap-integrated defaults deliberately excluded by i-d through i-g; not proven dead. | Framework contract, potentially visible. | **Decline bulk stripping.** |
| Page Header raw values | WP4.3i-c measured 15/15 live and found repeated values serving different roles. | Visible and contract-locked. | **Decline; do not reopen.** |
| White literal token | Current source has 15 `#fff`/`#ffffff` occurrences: three token definitions and twelve consumers/fallbacks. The closed i-o runtime investigation reduced its 11 eligible premise to only two verified-live semantically equivalent consumers; the rest were dead-selector, non-ink surface, unverified/JS-created, or latent white-on-white cases. Normalizing spelling or adding a two-consumer token does not remove the underlying design issue. | Mostly no-op indirection; some latent/visible risk. | **Decline. Do not reopen WP4.3i-o.** |
| Alpha/value-scale tokens such as `--wp-white-a05` | The closed i-jm attempt found 40/97 non-rendering literals, Inline Controls 0/21, a locked header, and a best legal result with net-zero Stylelint. | Artificial indirection without a proven maintenance win. | **Decline the i-jm scheme. Do not re-dispatch it.** |
| Ambient shadow/accent ramps in controls | Exact repeats exist, but i-d already demonstrated that partial accent extraction can leave every declaration flagged because ambient shadow layers remain raw. Whole-shadow tokens would often be single-use or would couple unrelated roles. | Semantic design-system work. | **Defer pending an owner-selected semantic vocabulary and goal.** |
| Raw spacing, radii, typography, and transition durations | Dense responsive ranges intentionally use nearby but unequal values. A value-scale replacement can change responsive geometry or motion even if token values initially match. | Visible redesign/architecture. | **Defer; never combine with colour or `!important` changes.** |
| Remaining 488 legacy `!important` declarations | No current per-declaration winner matrix exists. Their concentration follows shared/page cascade collisions and breakpoint geometry. | Cascade redesign. | **Defer to per-family certification packets.** |
| `#superset-actions .btn[hidden] { display: none !important; }` | This is the one post-closeout addition, added by #317 to fix a real visibility bug where shared important button display rules beat `[hidden]`. | Required behavior. | **Decline removal or de-weighting.** |
| Superset dark tint gap | `--superset-bg-1..4` still use light alpha values in dark mode because the old dark selector never matched. Adding a live dark override changes pixels. | Deliberate visible redesign. | **Defer for a separately named, owner-approved visual packet.** |

There is no remaining broad, genuinely mechanical token-extraction packet. The
only mechanical-looking work is the ten-declaration deletion, and it becomes
mechanical only after the missing runtime proof exists.

## Stale or disproved assumptions

1. **“24 declarations are dead” is disproved.** Fourteen rest-state declarations
   were certified; ten interaction declarations remain unproven.
2. **A sentinel miss is not a deadness proof** on a transitioning property. It
   can be an endpoint that was never reached before sampling.
3. **A CSS universal animation suppressor is not authoritative.** The current
   cascade contains layered and high-specificity important rules that can beat
   it. Browser-timeline stabilization is required.
4. **The status counts 218 hex / 488 important are historical.** At this HEAD
   the measured counts are 195 hex instances and 489 important declarations.
5. **The old exact animated-logo mismatch count is not a current gate.** The
   canonical history explicitly withdrew exact-count assumptions, later
   regenerated the corpus, and now uses an 81-byte-gated plus five-semantic-
   exemption terminal contract per platform. Future work must re-measure its
   own base and cannot inherit a July red band as permission.
6. **“All white occurrences should share a token” was disproved by i-o.** Only
   two eligible, live, semantically equivalent consumers remained after runtime
   classification.
7. **“Repeated rgba values should become a value scale” was not justified by
   i-jm.** Dead literals, locked live regions, and net-zero lint movement removed
   its maintenance case.
8. **Line-number-only packet scopes are stale by construction.** #317 and #464
   changed this stylesheet after i-filter-btn; future packets must resolve
   selector/property structures again.

## Proposed future packet structure

Packets are serial because every implementation packet would single-write
`static/css/pages-workout-plan.css` and several share the same existing
contract. No packet is authorized by this report.

| Order | Packet | Owned write paths | Reads / gates | Stop conditions |
|---:|---|---|---|---|
| 0 | **WP-OPT-R0 — rebase and source revalidation (audit only)** | One new evidence document only; ignored artifacts | Re-resolve all ten selectors/properties, CSS layers, current style counts, current visual policy, current JS-unit ruling, open PR/worktree overlap | Any candidate/source drift, competing-owner change, contract change, or unmerged writer on an owned path returns the plan to owner review. |
| 1 | **WP-OPT-R1 — animation-stable oracle (audit/tooling only)** | Prefer new unique files: `scripts/css_audit/workout_plan_interaction_probe.mjs`, `tests/test_workout_plan_interaction_probe_contracts.py`, and a new evidence doc | CDP/WAAPI fixed-point method; A/A zero; known-live mutation non-zero; no production diff | Any non-zero A/A record, unsettled animation, missing target, failed sentinel application, or vacuous known-live control. Do not proceed to deletion. |
| 2 | **WP-OPT-I1 — collapse/filter candidates** | `static/css/pages-workout-plan.css`; `tests/test_css_cascade_contracts.py`; one new evidence doc | Re-prove IS-01 through IS-03 only; focused functional/visual, Stylelint, pytest | One unproven declaration means that declaration stays. Any changed value/owner/geometry/pixel outside a known-live mutation rolls back the packet. |
| 3 | **WP-OPT-I2 — selection-actions candidates** | Same CSS/test contract paths; separate evidence doc | Re-prove IS-04 through IS-07. Treat light background/border/shadow as one state family; dark deletes only certified properties | Any non-zero target-element difference, or proof that the current hover declaration wins anywhere. |
| 4 | **WP-OPT-I3 — table-hover candidates** | Same CSS/test contract paths; separate evidence doc | Re-prove IS-08 through IS-10 over odd/even rows, themes, modes, routines, and widths. IS-08/09 are a unit | If only one of IS-08/09 is certified, retain both. Preserve the dark shadow. Stop on any shared Calm-Glass owner drift. |
| 5 | **WP-OPT-W1 — `!important` census by one selector family (audit only)** | New evidence doc and, only if necessary, a new unique probe/contract file | Start with one bounded family after I1-I3; record every matched node, winning owner, importance/layer/specificity, and real-state coverage | Zero runtime match without a known-live census control; equal computed values with different owners; any need to rewrite selectors or layers. |
| 6 | **WP-OPT-W2 — certified de-weighting for that one family** | Workout Plan CSS, a narrow contract, evidence doc | Change only the declarations W1 certified; no token/value/selector/reordering changes in the same packet | Any owner/value/geometry/pixel change, any `!important` increase elsewhere, or any selector rewrite. |
| 7 | **WP-OPT-T0 — semantic token decision (owner gate, no implementation)** | A new optional planning/evidence doc only | Owner chooses one component, semantic roles, local versus global ownership, desired lint/maintenance outcome, and whether any visible change is intended | No owner vocabulary/goal; any proposal based only on literal count; any attempt to use the WP4.3i-jm or i-o packet premise. |
| 8 | **WP-OPT-T1+ — one component/one role token packet** | One CSS owner file plus its narrow contracts/evidence; `tokens.css` only with explicit shared-token authority | Exact var-expansion comparison, both themes, all states; no `!important` work in the same packet | Single-use tokens, cross-role coupling, no warning reduction/maintenance benefit, changed computed value, or any visible delta without separate approval. |

For W1/W2 and T1+, “one family” means a structural selector boundary such as
collapse toggles, one colour-coded input role, one button role, or one table
state—not the whole 5,810-line bundle. The current concentration numbers are a
triage order, not authorization to start with the largest cluster.

## File-overlap risks

| Path | Risk | Coordination rule |
|---|---|---|
| `static/css/pages-workout-plan.css` | Single writer for every implementation packet; later changes #317/#464 already demonstrate line and behavior drift. | Exclusive claim; serial packets; fresh branch from merged `main`; structural re-resolution before every deletion. |
| `static/css/components.css` | Holds the competing selection, table, and collapse owners. A shared CSS packet can invalidate every non-winner conclusion without touching the page bundle. | Read-pin its blob digest in evidence; re-run after any shared-CSS merge. Do not edit it in a page-local packet. |
| `static/css/tokens.css` | #464 changed theme/action tokens after the original audit. A token change can move computed values while page CSS is byte-identical. | Read-pin digest; keep read-only unless the owner explicitly approves a shared-token packet. |
| `templates/workout_plan.html` and `static/js/modules/**` | DOM classes, dynamically created controls, and real interaction wiring determine selector reachability. | Read-only for CSS cleanup. Any required behavior change is a separate feature/bug packet. |
| `tests/test_css_cascade_contracts.py` | Existing presence lock must move only when certified deletion lands; it is also a frequent shared CSS contract surface. | Coordinate single writer; prove red paths; never weaken the Page Header or dead-fallback contracts. |
| `scripts/css_audit/**` | Shared audit infrastructure; `runtime_probe.mjs` has a documented transition limitation. Other optional CSS audits may touch this directory. | Prefer a new Workout Plan-specific probe file; do not silently “fix” a shared harness inside a deletion packet. |
| `e2e/visual-helpers.ts` | Differs from the audited HEAD after the upstream visual-policy correction; it controls visual interpretation/exemptions. | Rebase and re-read before runtime proof; do not edit it in Workout Plan cleanup. |
| `e2e/__screenshots__/**` | Baseline churn would obscure whether cleanup is inert. | Compare only; any write is a stop and needs separate owner-reviewed visual authority. |
| `docs/MASTER_HANDOVER.md`, `docs/REFACTOR_PLAN.md`, `docs/ACTIVE_DEVELOPMENT.md`, `docs/OPEN_WORK_EXECUTION_PLAN.md` | Canonical shared status surfaces explicitly excluded from this audit and high-conflict under parallel work. | No optional packet edits them unless separately authorized after implementation. |

## JS-unit qualification clock

At the audited HEAD, the operative owner ruling in
`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md:5143-5170` defines an expansion as
the last merged change that **added, removed, renamed, or materially changed a
case under `static/js/**/*.test.js`**. It declares:

- T0: `2026-08-27T23:18:21Z`;
- source job: `98703428098` on run `33125767570`;
- strict mark: `2026-09-10T23:18:21Z`; and
- `js-unit` remains non-required, with Q4/D2 unsigned.

None of the proposed CSS cleanup packets inherently needs to add, remove,
rename, or materially change a `static/js/**/*.test.js` case. A new pytest
harness contract, a probe under `scripts/css_audit/`, or an E2E interaction test
does not meet that path-based definition. Therefore the planned packet design
has **no JS-unit-clock interaction**.

This is also a hard containment rule:

- `static/js/**/*.test.js` is an explicitly unowned path for R0 through T1+.
- If runtime proof discovers a production-JS defect that genuinely requires a
  Vitest case change, stop the CSS packet and propose a separate JS packet.
- Landing such a case change before the strict mark would create a new final
  expansion and re-engage the restart rule. It must not be smuggled into a CSS
  proof or contract update.
- The local `origin/main` ref already contains a newer ledger edit than this
  audited HEAD. Re-read the live ruling and ledger after merge/rebase; do not
  copy these dates forward as standing truth.

## Owner decisions required

1. Authorize or decline **R1 only**: investment in a transition-safe Workout
   Plan oracle. Authorization to build the oracle is not deletion authority.
2. After R1 evidence, decide whether zero-diff declarations should be removed
   and whether I1, I2, and I3 may proceed serially. Any declaration that wins or
   remains unverified is retained without further debate in that packet.
3. Decide whether the optional objective is lint reduction, maintainability,
   design-system consistency, or an intentional visual redesign. Those goals
   produce different token boundaries and cannot share an implementation
   packet.
4. If token work is desired, select the first **single semantic component** and
   decide page-local versus shared ownership. No generic rgba scale and no white
   token is recommended.
5. Decide whether the superset dark-tint gap should remain accepted or receive
   its own visible-change proposal. It is not refactor cleanup.
6. Decide whether any baseline change is intended. The default for every packet
   above is **no**; a non-zero visual delta stops the packet.

## Final recommendations

- **Proceed** only with a future, separately authorized, audit/tooling-only
  animation-stable oracle packet after the active parallel work is merged and
  the base is revalidated.
- **Defer** all ten interaction-state deletions until that oracle's A/A control
  and per-candidate A/B comparison both reach absolute zero.
- **Defer** raw colour/value tokenization and `!important` re-weighting to small,
  owner-selected semantic/cascade packets; they are redesign-sized, not
  mechanical cleanup.
- **Decline** a bulk token pass, a generic alpha/value scale, white-literal
  tokenization, live fallback stripping, Bootstrap fallback stripping, Page
  Header edits, broad `!important` reduction, or de-weighting the #317 hidden-
  state fix.
- **Do not reopen or rename-and-repeat WP4.3i-jm or WP4.3i-o.** Their closed
  boundaries are evidence against those approaches, not unfinished work.
- **Keep the superset dark-tint gap separate:** it remains an owner-approved
  visible product decision, not refactor cleanup.
