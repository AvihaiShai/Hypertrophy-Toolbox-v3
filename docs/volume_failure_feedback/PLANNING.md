# Plan Review — Packet U1: Volume calculation failure feedback

*Both gates are represented here. Section 0 is Gate 0 work and is **signed**; Plan v1, the three council reviews verbatim, the response matrix and Plan v2 are Gate 1 work and are now **present** — see [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4, whose closing blockquote records that U2's lighter requirement is not a precedent U1 may borrow to skip Gate 0, and §8, which records which gates U1 owed and that no roadmap-level approval covers U1–U3 jointly. **Gate 1 is SIGNED — 2026-08-26.** The owner approved Plan v2 at the sign-off block at the end of this document, deciding **OD-1**, **OD-3** and **OD-4** there and ratifying **OD-2**'s recommended reading. **Implementation becomes authorized only after this signed planning PR merges successfully** — signing alone authorizes nothing.*

Gate 0 was signed by the owner on 2026-08-25; the answers are recorded under **Owner decisions**
below.

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> Execute Packet U1 — Volume calculation failure feedback, from docs/OPEN_WORK_EXECUTION_PLAN.md §4 as merged on main, stopping at Gate 0. Do not write production or test code in this session.
>
> […]
>
> Then perform U1's Gate 0, and only Gate 0.
>
> Use the repository's requirements skill to create U1's own PLANNING.md and write Section 0. Stop for owner approval after Gate 0. U1 owes a separate Gate 1 later.
>
> Do not implement anything, edit tests, or modify static/js/modules/volume-splitter.js.
>
> Re-verify U1's substrate against origin/main:
>
> - The failed `/api/calculate_volume` request is independently silenced at two sites:
>   - `showErrorToast: false` near line 131.
>   - A `.catch` whose only behavior is `console.error` near lines 136–137.
> - Removing either suppression alone would still leave the request failure silent.
> - Measure and classify each neighboring `showErrorToast: false` site near lines 191, 251, 288, 372, and 828 as:
>   - in scope;
>   - separately defective; or
>   - deliberate.
> - Do not assume their classifications.
> - Record for the later Gate 1 plan that the regression must fail against each independently sufficient suppression site.
>
> Section 0 must define the intended behavioral contract, including:
>
> - What visible and accessible error feedback appears.
> - Whether stale calculated results remain visible, become visibly stale, or are cleared.
> - How the UI avoids implying that stale output came from the failed calculation.
> - Retry behavior.
> - Whether repeated failures deduplicate or repeat feedback.
> - Relevant accessibility expectations.
> - Success behavior and slider interactions that must remain unchanged.
> - The measured disposition of all six neighboring suppression sites.
> - Explicit unanswered product questions, if any.

**Problem**

On `/volume_splitter`, a failed `POST /api/calculate_volume` produces no user-visible signal of any kind. The page's most frequent request can fail while the results table and the suggestion list continue to show the output of an earlier, different calculation. The user has no way to distinguish "these are your numbers" from "these are your last numbers, and the ones you are looking at were never computed".

This is a user-facing behavior change to an error surface, which is why [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4 requires the intended state to be signed as a contract before any code moves.

### 0.1 Measured substrate — and one correction to the packet's stated premise

Every claim below was measured in an isolated worktree at `origin/main` = `77f4adf543adc45dc15dc00b37395f180ffe6439`, by reading [`volume-splitter.js`](../../static/js/modules/volume-splitter.js), [`fetch-wrapper.js`](../../static/js/modules/fetch-wrapper.js), [`toast.js`](../../static/js/modules/toast.js), [`routes/volume_splitter.py`](../../routes/volume_splitter.py), [`templates/volume_splitter.html`](../../templates/volume_splitter.html) and [`templates/base.html`](../../templates/base.html). Nothing here is inferred from the packet text.

**The two suppression sites exist exactly where the packet says.** [`volume-splitter.js:131`](../../static/js/modules/volume-splitter.js#L131) passes `showErrorToast: false` in the request options, and [`volume-splitter.js:136-137`](../../static/js/modules/volume-splitter.js#L136-L137) attaches a `.catch` whose entire body is `console.error('Error calculating volume:', error);`.

⚠️ **The packet's claim that each suppression is sufficient on its own is FALSE in one direction, and only one of the two is load-bearing for user-visible silence.** §4 U1 states: *"Removing the silent `.catch` alone leaves the shared toast still suppressed by the option; flipping the option alone leaves the rejection swallowed by the catch."* The first half holds. The second half conflates *swallowing the rejection* with *producing no feedback*, and the control flow in the shared wrapper does not support it:

| Mutation | What the wrapper does | What the user sees |
|---|---|---|
| Both suppressions present (today) | The HTTP-error branch at [`fetch-wrapper.js:212-216`](../../static/js/modules/fetch-wrapper.js#L212-L216) skips `showToast`, then throws; the local `.catch` logs and stops | **Nothing** |
| Remove the `.catch` only | Toast still skipped; the rejection becomes an unhandled promise rejection, which [`global-error-handler.js:32-34`](../../static/js/global-error-handler.js#L32-L34) only logs | **Nothing** |
| Remove `showErrorToast: false` only | `showToast('error', …)` fires **before** the `throw` on line 216; the `.catch` then logs an already-surfaced error | **An error toast** |
| Remove both | Toast fires; rejection is unhandled | **An error toast** |

**User-visible silence therefore holds if and only if `showErrorToast: false` is present.** The `.catch` suppresses the diagnostic surface, not the user surface — but it is not decorative: it is the sole handler for a failure that happens **after** a 2xx response, inside `.then(handleCalculateResponse)`, where the wrapper's toast is never reached. Both sites are real; they guard different failure classes.

**Only one server failure mode reaches this call path.** [`routes/volume_splitter.py:49-111`](../../routes/volume_splitter.py#L49-L111) returns `error_response('INTERNAL_ERROR', 'Failed to calculate volume', 500)` on failure and has **no** HTTP-200-with-`ok:false` path, so `response.ok` is false and the wrapper's HTTP-error branch is the one that runs. A transport failure (offline, dropped connection) takes the outer branch at [`fetch-wrapper.js:245`](../../static/js/modules/fetch-wrapper.js#L245), gated by the same flag. `retries` defaults to `0` for a `POST` ([`fetch-wrapper.js:140`](../../static/js/modules/fetch-wrapper.js#L140)), so there is no silent retry today, and exactly one toast would appear rather than two.

**The toast surface is functional on this page.** `#liveToast` and `#toast-body` live in [`base.html:243-251`](../../templates/base.html#L243-L251), which [`volume_splitter.html`](../../templates/volume_splitter.html) extends, so the "removing the option yields a toast" row above is a real outcome and not a no-op against a missing container.

**What stale output looks like — and it differs by call path.** `.results-section` and `.ai-suggestions-section` both ship `d-none` in the template; the first is revealed by `displayResults()` ([`:170`](../../static/js/modules/volume-splitter.js#L170)) and the second by `displaySuggestions()` ([`:347`](../../static/js/modules/volume-splitter.js#L347)). On failure neither runs, and neither does `clearResults()`. So:

- **First calculation of a page load** — the sections stay hidden. Silent, but not misleading.
- **Button and slider paths** ([`:64`](../../static/js/modules/volume-splitter.js#L64), [`:633`](../../static/js/modules/volume-splitter.js#L633), and the debounced [`:627`](../../static/js/modules/volume-splitter.js#L627) → [`:867`](../../static/js/modules/volume-splitter.js#L867)) — the previous table rows, suggestion cards, `.muscle-row` status classes and `.volume-value-pill--*` modifiers all remain, while the slider's own value badge has already been repainted by `updateValueDisplay()` on the `input` event. Displayed inputs and displayed outputs no longer correspond.
- **Mode-switch and load-plan paths** ([`:533`](../../static/js/modules/volume-splitter.js#L533), [`:213`](../../static/js/modules/volume-splitter.js#L213)) — `setMode()` calls `renderSliders()`, which clears and rebuilds every `.muscle-row`, so the status classes and pill modifiers are gone *before the request is sent*. What survives is a results table and a suggestion list computed for the **previous mode**, sitting under a freshly rendered slider set for the new one.

The second and third cases are different divergences and a contract that only addresses one of them leaves the other live.

**Failure volume is not one request per click.** `calculateVolume()` is reachable from all five call sites listed above. A sustained server fault during a slider drag therefore produces a stream of failures every 300 ms, which is why deduplication is a contract question and not an implementation detail.

### 0.2 Disposition of all six `showErrorToast: false` sites

Measured, not assumed. Five of the six pair the suppressed shared toast with a local `.catch` that raises a page-specific `showToast('error', …)`; exactly one does not.

| # | Line | Call | `.catch` body | Disposition |
|---|---:|---|---|---|
| 1 | [131](../../static/js/modules/volume-splitter.js#L131) | `POST /api/calculate_volume` | `console.error` only | **In scope** — the packet's defect |
| 2 | [191](../../static/js/modules/volume-splitter.js#L191) | `GET /api/volume_plan/{id}` | `console.error` + `showToast('error', 'Failed to load plan. Please try again.')` | **Deliberate** |
| 3 | [251](../../static/js/modules/volume-splitter.js#L251) | `DELETE /api/volume_plan/{id}` | hides the modal, `console.error` + `showToast('error', 'Failed to delete plan. Please try again.')` | **Deliberate** |
| 4 | [288](../../static/js/modules/volume-splitter.js#L288) | `POST /api/save_volume_plan` | `console.error` + `showToast('error', 'Failed to save plan. Please try again.')` | **Deliberate** |
| 5 | [372](../../static/js/modules/volume-splitter.js#L372) | `GET /api/volume_history` | `console.error`, paints a `text-danger` "Failed to load volume history." row into `#history-body`, **and** `showToast('error', 'Failed to load saved volume plans. Please try again.')` | **Deliberate** — the only site that already pairs an inline treatment with a toast |
| 6 | [828](../../static/js/modules/volume-splitter.js#L828) | `POST /api/volume_plan/{id}/(de)activate` | `console.error` + a direction-specific `showToast('error', …)` | **Deliberate** |

**Zero sites are separately defective.** The pattern in this file is intentional: `showErrorToast: false` opts out of the wrapper's generic message so a page-specific one can replace it. Site 1 is the single instance where the replacement was never written. **This makes U1 a one-site repair, not a five-site sweep.**

**Recorded for the Gate 1 plan.** The regression must red if **either** site-1 suppression is restored in isolation. Because the two sites guard different failure classes (§0.1), a single arm cannot cover both: coverage is owed separately for the request-failure class (non-2xx and transport) and for the post-2xx class that fails inside the response handler. The construction of those arms is Gate 1 work and is not decided here.

**Acceptance criteria** — reconciled with the Gate 0 decisions recorded under
**Owner decisions** below.

1. Given the Volume Splitter page has loaded and a previous calculation succeeded, when a subsequent `POST /api/calculate_volume` fails, then the user is told that the volume calculation failed on **both** of the surfaces signed in Q2 — an accessible toast carrying the immediate notification, and a persistent inline failure region adjacent to the calculation results.
2. Given the same failure, when the feedback is presented, then it is announced to assistive technology, focus is not moved disruptively — in particular it is not taken from the control the user is operating — and both of those properties are covered by explicit regression assertions rather than resting on the inherited markup alone.
3. Given the same failure, when the feedback is presented, then every output that could be mistaken for the result of the failed calculation is cleared or reset — the results table, the suggestion list, the per-muscle status classes and the value-pill modifiers — so that nothing from a previous mode or a previous input state is left presented as current.
4. Given a failure on the mode-switch or load-plan path, when the sliders have already been rebuilt for the new mode, then the results and suggestions computed for the previous mode are cleared by criterion 3 rather than left sitting under the new mode's sliders.
5. Given a failure, when the user activates either the Calculate button — which stays usable throughout — or the Retry action carried by the failure feedback, then a fresh `POST /api/calculate_volume` is issued from the input values as they stand at that moment and, on success, the page returns to its normal successful state with all failure feedback removed. **No automatic `POST` retry is introduced.**
6. Given a sustained server fault, when the user drags a slider and the debounced calculation fails repeatedly, then the page holds **one** logical failure state: the inline region is updated or replaced rather than duplicated and persists until the next successful calculation, and each further toast replaces or updates the standing one rather than stacking beneath it.
   ⚠️ **ANNOTATED 2026-08-26 (Gate 1, OD-3) — no signed word above is rewritten.** The owner granted a **scoped amendment** at Gate 1, in these terms: *"The inline failure region persists until the next successful calculation **or until the user resets**."* The amendment is scoped to the **persistence clause**; the rest of criterion 6 stands unchanged, including its toast half — whose non-stacking is structurally guaranteed by [`toast.js`](../../static/js/modules/toast.js) rather than measured (§v2.5), and whose repeat-announcement suppression is carried by arm `a6` and mutation `M8`. See **OD-3** in §v2.13, and §v2.2 (G) for the single line that implements it.
7. Given the first calculation after a page load fails, when no calculation has ever succeeded on that load, then the failure feedback is shown anyway, and the empty results and suggestions sections are still **not** revealed.
8. Given a successful `POST /api/calculate_volume`, when the response is rendered, then the results table, suggestions, per-muscle status classes, value-pill modifiers, server-supplied ranges and slider track paint are what they are today, and the success path gains **no** permanently present element, class, attribute, message or other observable state — every failure-only affordance is created or activated only on failure and is fully removed or reset once a calculation succeeds.
9. Given any slider interaction, when the user drags, releases, switches mode, resets, or loads a saved plan, then the debounce interval, the request payload and the call sequence are unchanged from today.
10. Given the shipped change, when the five neighbouring call sites at lines 191, 251, 288, 372 and 828 are exercised, then their behavior is unchanged.
11. Given the repaired code, when a regression arm restores the request-failure suppression at the calculate call, then that arm fails.
12. Given the repaired code, when a regression arm restores the post-2xx suppression at the calculate call, then that arm fails.

Criteria 11 and 12 rest on the corrected framing measured in §0.1, which Q0 signed as stated.

**Calculation surface**

- `none`.
- No function in [`utils/effective_sets.py`](../../utils/effective_sets.py), [`utils/weekly_summary.py`](../../utils/weekly_summary.py), [`utils/session_summary.py`](../../utils/session_summary.py), the progression modules or the fatigue modules is in scope. `calculate_volume()` in [`routes/volume_splitter.py`](../../routes/volume_splitter.py) and everything it calls in [`utils/volume_splitter_service.py`](../../utils/volume_splitter_service.py) are **read-only** for U1: the volume numbers, the `low`/`optimal`/`high`/`excessive` classification and the recommended-range derivation must be identical before and after.
- Because no calculated value moves, no worked before/after example applies. U1 changes only what the page does when the calculation does not return one.
- Migration notes: the PR description will state that no calculation, DB schema or API response shape changed, and that the added coverage is a frontend failure-path regression only. If Gate 1 planning discovers that the signed contract cannot be met without touching the response shape, that discovery **reopens Gate 0** rather than proceeding.

**In scope**

- The behavioral contract for a failed `POST /api/calculate_volume` on `/volume_splitter`, signed at this gate.
- The measured disposition of all six `showErrorToast: false` sites in the file (§0.2), recorded here so Gate 1 does not re-derive it.

**Out of scope / non-goals**

- Any production or test code in this session. Nothing under `static/js/**`, `tests/**` or `e2e/**` is written, and [`volume-splitter.js`](../../static/js/modules/volume-splitter.js) is not modified.
- The five deliberate neighbouring sites. They are measured and classified, not changed.
- Any change to the shared [`fetch-wrapper.js`](../../static/js/modules/fetch-wrapper.js) or [`toast.js`](../../static/js/modules/toast.js) contracts. U1 uses the existing conventions; it does not rebuild transport or notification infrastructure. KI-010 and KI-011 belong to Packet U3.
- The server contract for `/api/calculate_volume`, including its status code and error payload.
- [`PRODUCT_DOCS_PLAN.md:113`](../PRODUCT_DOCS_PLAN.md#L113), whose *"The active WP4.4 work"* and *"WP4.4-i is active and i → j → k is already authorized"* assertions are stale against [`MASTER_HANDOVER.md:1773`](../MASTER_HANDOVER.md#L1773), which records WP4.4 complete with the `i → j → k` tail merged on 2026-08-01. **Not repaired by U1**, and this session was not authorized to edit [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) to file it. **Owner action owed: add it to §4 or §7 as its own documentation packet, or it stays tracked only here.**
- [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md) and [`ACTIVE_DEVELOPMENT.md`](../ACTIVE_DEVELOPMENT.md) opening status lines, which U1 does not update.
- [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4's own account of U1, which signing this gate leaves stale in two places. Its premise sentence's second half — *"flipping the option alone leaves the rejection swallowed by the catch"* — is falsified by §0.1; and its `**Status:** Execute — needs its own Gate 0 and Gate 1` line at [`:109`](../OPEN_WORK_EXECUTION_PLAN.md#L109) loses its first half the moment this signing lands. §8's Gate column ([`:509-512`](../OPEN_WORK_EXECUTION_PLAN.md#L509-L512)) and §10's table ([`:539-541`](../OPEN_WORK_EXECUTION_PLAN.md#L539-L541)) survive untouched, because both are framed as the gates a packet *owes* rather than gates it has passed. **Q0 signed the corrected framing without routing it back through §4**, so §4 is left unedited and this brief is the authoritative statement of the mechanism for U1's purposes. **Owner action owed: correct the premise sentence and reduce the §4 Status line to "needs its own Gate 1", or accept both as stale on `main`.**
- [`DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md) row 9, which repeats the same *"each sufficient alone"* claim. Its *"Re-measured at `5ca4191`"* note is accurate about the line numbers, but the characterisation itself was carried forward unexamined, so the row is **not an independent second measurement of the premise** — §0.1 measured that claim false at `77f4adf`. **Not repaired by U1**, and recorded here so that a later session does not read the registry row as corroboration.
- Packets U2, U3, R1, R2, R3, V1, Track P1 and Track D1; Dependabot PRs #415 and #416; branch protection and repository settings.

**Assumptions — reviewed and dispositioned at Gate 0**

- **The existing toast is the intended vehicle — and it is not the only one.** The assumption was drawn from the five sites in this file that already use it. Q2 keeps the toast and adds a persistent inline failure region beside the results, so the assumption is accepted **and widened**; the inline-only alternative it flagged was not chosen.
- **"Accessible" is an `aria-live` announcement without a focus move — and the inherited markup is not sufficient evidence of it.** The existing toast container already carries `aria-live="polite"` on the wrapper and `role="alert"` with `aria-live="assertive"` on `#liveToast` ([`base.html:236-248`](../../templates/base.html#L236-L248)), so a toast-based answer inherits an announcement today. The accessibility decision **refuses that inheritance as proof on its own**: U1 owes an explicit regression assertion instead.
- **The failure is user-recoverable rather than fatal.** Accepted as written: the page keeps working and recalculates on the next interaction. Q3 settles the part that was deliberately not assumed — an explicit retry affordance **is** required, alongside a Calculate button that stays usable.
- **No new i18n or copy-review process.** Accepted unchanged; no answer disturbed it. The message is plain English in the register the file already uses. That register is not quite uniform: four of the five existing messages end "Please try again." ([`:217`](../../static/js/modules/volume-splitter.js#L217), [`:263`](../../static/js/modules/volume-splitter.js#L263), [`:318`](../../static/js/modules/volume-splitter.js#L318), [`:439`](../../static/js/modules/volume-splitter.js#L439)); the activate/deactivate pair at [`:838`](../../static/js/modules/volume-splitter.js#L838) omits it. **Choosing the exact wording is Gate 1 work.**

**Owner decisions — signed 2026-08-25**

Each blocking question is reproduced as it was put to the owner, with the answer and the consequence it carries for this brief. Where an answer changed a criterion or an assumption, the change is already made above; **where a criterion or an assumption states the same requirement, this block governs the wording**.

- **Q0 — the packet's premise is wrong in one direction; confirm the corrected framing.** §4 U1 says each suppression is independently sufficient. Measured (§0.1), only `showErrorToast: false` is sufficient for user-visible silence; the `.catch` is sufficient only for the post-2xx failure class. The alternative offered was to resolve the discrepancy in [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4 first.
  **Decision: the corrected measured framing is accepted, and §4 is NOT amended first.** `showErrorToast: false` causes the silence for the request and transport failure classes; the local `.catch` owns the distinct post-2xx response-handling failure class. **Consequence:** §0.1 stands as measured and is the substrate Gate 1 plans against; §4 is left unedited, and the staleness that leaves behind is booked under *Out of scope*.
- **Q1 — stale results: clear, or mark stale?** Three defensible answers: (a) the results and suggestions are cleared on failure, so the page shows nothing rather than something wrong; (b) they stay and are visibly marked as the previous result; (c) they are left untouched and the failure message alone carries the signal.
  **Decision: (a) — clear.** On failure, clear or reset all output that could be mistaken for the current calculation — the surfaces criterion 3 enumerates. **Consequence:** criterion 3 is now a clearing requirement rather than a deferred one, and criterion 4 resolves to the same clearing on the mode-switch and load-plan paths.
- **Q2 — toast, inline region, or both?** A toast alone auto-dismisses after 3 s ([`toast.js:33`](../../static/js/modules/toast.js#L33)) and leaves no trace next to a stale table; an inline region persists but is easier to miss. Site 5 in §0.2 is the in-repository precedent for doing both.
  **Decision: both surfaces.** An accessible toast for immediate notification, and a persistent inline failure region near the calculation results. **Consequence:** criterion 1 requires both.
- **Q3 — retry.** Is the existing Calculate button sufficient as the retry path, or must the failure feedback carry its own retry affordance? [`toast.js`](../../static/js/modules/toast.js) supports an inline action button (`options.action`), already used at [`volume-splitter.js:299-306`](../../static/js/modules/volume-splitter.js#L299-L306).
  **Decision: both.** The existing Calculate button stays usable, and the failure feedback also carries a Retry action. **No automatic `POST` retries are added**, so `retries` stays `0` for this call ([`fetch-wrapper.js:140`](../../static/js/modules/fetch-wrapper.js#L140)) and request behavior on the success path is untouched. **Consequence:** criterion 5 names both paths.
- **Q4 — repeated failures: deduplicate or repeat?** During a slider drag against a down server, the debounced path can fail every 300 ms. Options: (a) one notification that persists until the next success, replacing rather than stacking; (b) a fresh notification per failure; (c) suppress subsequent notifications for a cooldown window.
  **Decision: (a) — replace rather than stack.** One logical failure state is maintained across repeated failures: the inline message persists until the next successful calculation, and repeated toast notifications replace or update rather than stack. **Consequence:** criterion 6 is now a deduplication requirement.
  ⚠️ **ANNOTATED 2026-08-26 (Gate 1, OD-3) — no signed word above is rewritten.** Criterion 6's persistence clause was amended in scope, and by the governing rule above the same amendment reaches this wording: it now reads *"…persists until the next successful calculation **or until the user resets**."* The dedup requirement itself is untouched. See **OD-3** in §v2.13.
- **Q5 — how literally should "unchanged success path" in criterion 8 be read?** The strict reading is that no new element, class or attribute appears on the success path at all; the weaker reading is that nothing user-perceivable changes, which would permit a permanently-present region that is empty on success.
  **Decision: strict.** The successful path must not gain a permanently present element, class, attribute, message or other observable state. Any failure-only UI is created or activated only on failure and is fully removed or reset after a success. **Consequence:** criterion 8 is the strict reading, and it constrains how Gate 1 may build both Q2 surfaces and the Q3 Retry action.
- **Q6 — does U1 own the first-load case?** If the very first calculation of a page load fails, should the user be told, or should U1 stay silent when nothing has ever been calculated?
  **Decision: yes, U1 owns it.** The error feedback is shown even when no calculation has succeeded yet, but the empty results and suggestions sections are not revealed. **Consequence:** criterion 7 is now an affirmative requirement, and the first-load case §0.1 measured as *"silent, but not misleading"* is one U1 must cover.
- **Accessibility — the evidence standard.** **Decision: an explicit regression assertion is required** for the announcement behavior and for the absence of disruptive focus movement; the existing `aria-live` markup in [`base.html:236-248`](../../templates/base.html#L236-L248) may not be relied on as the sole evidence. **Consequence:** criterion 2 carries the assertion requirement, and Gate 1 owes the arm that satisfies it, alongside the suppression arms recorded at the end of §0.2.

### Section 0 sign-off — GATE 0 — SIGNED 2026-08-25

- [x] User confirms the acceptance criteria match intent.
- [x] User reviewed the assumptions and corrected or accepted each one.
- [x] Blocking questions Q0–Q6 are answered, together with the accessibility evidence standard.

**Gate 0 is SIGNED.**

**Gate 1 has NOT begun, and signing Gate 0 does not authorize it.** U1 still owes a separate
Gate 1 — Plan v1, a council response matrix and Plan v2, reviewed and approved in their own right —
before any implementation, any test authoring, or any change to
[`volume-splitter.js`](../../static/js/modules/volume-splitter.js).

⚠️ **ANNOTATION 2026-08-26 — the *"Gate 1 has NOT begun"* clause immediately above is SPENT. The rest
of that paragraph stands verbatim and is not restated.** Gate 1 **planning** has since run: Plan v1,
the three council reviews, the response matrix and Plan v2 are all below. The signed Section 0 above
is unedited and this annotation adds nothing to it. What the spent clause got right and what still
holds: **Gate 1 is NOT signed**, Plan v2 has **not** been approved, and **no implementation, no test
authoring and no change to [`volume-splitter.js`](../../static/js/modules/volume-splitter.js) is
authorized.** The council ran on 2026-08-25; this annotation was added the following day, when the
document was reconciled against itself.

⚠️ **ANNOTATION 2026-08-26 (second, added at signing) — the annotation immediately above is now SPENT in its turn.** Its surviving clauses — that Gate 1 is not signed, that Plan v2 is not approved, and that no implementation, test authoring or change to [`volume-splitter.js`](../../static/js/modules/volume-splitter.js) is authorized — were accurate when written and are superseded by the owner's Gate 1 approval of 2026-08-26 at the sign-off block below. **Authorization still does not begin at signing — it begins when this signed planning PR merges.** Section 0's only additions are the two OD-3 pointers, under criterion 6 and under Q4's decision.

---

## Plan v1

*Gate 1, first draft. Written against `origin/main` = `b4d6b1337bf730aa675e7126b7713237931ba60c`; every line anchor below was read at that commit. This section proposes; it does not authorize. **No code may be written until Plan v2 is approved at the Gate 1 sign-off below.***

**Goal**: When `POST /api/calculate_volume` fails on `/volume_splitter`, the page tells the user so on both signed surfaces, clears every output that could be mistaken for the failed calculation's result, offers a Retry that uses the inputs as they stand, and leaves the success path observably identical to today.

### v1.0 Gate 0 reopening assessment — and the one live conflict

The signed contract was checked against the immutable surfaces before planning. **No Gate 0 reopening trigger was found.** Specifically:

- **No API response shape changes.** [`routes/volume_splitter.py`](../../routes/volume_splitter.py) and [`utils/volume_splitter_service.py`](../../utils/volume_splitter_service.py) are untouched; the plan reads only the existing `500` + `error_response('INTERNAL_ERROR', …)` behavior and the existing `success_response` envelope.
- **No shared-contract changes.** [`toast.js`](../../static/js/modules/toast.js) and [`fetch-wrapper.js`](../../static/js/modules/fetch-wrapper.js) are read-only. Everything Q2 and Q3 require is already exposed: `options.action` ([`toast.js:65-85`](../../static/js/modules/toast.js#L65-L85)) and single-element replacement ([`toast.js:60-63`](../../static/js/modules/toast.js#L60-L63), [`:101-109`](../../static/js/modules/toast.js#L101-L109)).
- **No calculation behavior changes.** Section 0's Calculation surface stays `none`.
- **No CSS changes.** The inline region is styled with Bootstrap classes already present in the compiled bundle (`alert alert-danger`), so no `scss/**` or `static/css/**` gate is triggered and no visual baseline moves.

**The one place the contract and the substrate pull against each other is criterion 11's mutation, and it is an interpretation question, not a blocked contract.** It is raised as **OD-4** in §v1.13 and must be dispositioned by the council or the owner. Reading criterion 11 literally — *the arm must fail when `showErrorToast: false` is re-added* — would force the repair to flip that flag and let the shared wrapper raise the toast. That collides head-on with Q3, because the wrapper's toast at [`fetch-wrapper.js:212-214`](../../static/js/modules/fetch-wrapper.js#L212-L214) cannot carry a Retry action, and with §0.2's measured finding that `showErrorToast: false` plus a page-specific replacement is this file's deliberate idiom at five of six sites. **If the owner insists on the literal reading, that DOES reopen Gate 0**, because Q3 and criterion 11 cannot both be satisfied. This plan adopts the other reading and says so out loud rather than absorbing the conflict silently.

### v1.1 Blocking open decision — U1's coverage arms vs. the live JS-unit qualification window

**This must be answered before implementation starts. Every artifact and gate line below is written for option (i) and changes if the owner picks otherwise.**

[`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §6.5 ([`:844-868`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L844-L868)) is running a live strict 14-day qualification window: **T0 = `2026-08-22T17:59:26Z`**, strict mark **`2026-09-05T17:59:26Z`**, qualifying the suite pinned at **13 files / 231 cases**. Owner ruling Q2 restarts that window when the suite the `JS Unit` job runs changes. §6.5 grants exactly one exemption — Packet F, as a named required predecessor — and **U1 is not a named predecessor**, so no existing exemption covers it. There is today no `volume-splitter.test.js`; the 13 files all sit under `static/js/modules/__tests__/`.

| Option | What U1 ships | Cost, stated honestly |
|---|---|---|
| **(i) E2E-only coverage now** | All three arms live in [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts). Zero Vitest files, zero Vitest cases. | The window is untouched — the suite stays at 13 files / 231 cases and the strict mark stays `2026-09-05T17:59:26Z`. Cost: the new helpers get no unit-level coverage, so a pure-logic regression is caught only through a browser. Playwright per-spec counts move, which is an ordinary inventory regeneration and reds nothing. |
| **(ii) Add Vitest coverage now** | A new `static/js/modules/__tests__/volume-splitter.test.js`. | Moves the suite off 13 files / 231 cases. Under Q2's restart clause the window arguably restarts from U1's merge, discarding the days already accumulated and pushing the strict mark roughly two weeks later — which delays D2. Whether "arguably" becomes "certainly" is itself an owner call, and D2 is not U1's to spend. |
| **(iii) Defer Vitest coverage past the strict mark** | Option (i) now, plus a follow-up packet that adds the Vitest file after `2026-09-05T17:59:26Z`. | The window is untouched and the unit coverage is eventually written. Cost: a second PR, a second review cycle, and a gap during which the helpers have browser-level coverage only. Needs a tracked owner obligation or it will be forgotten. |

**Plan v1 recommends (i), with (iii) as the named follow-up.** The three arms Gate 0 requires are all failure-path, DOM-and-announcement behaviors that a browser measures directly and jsdom would only approximate. **This is a recommendation, not a decision. The owner decides.**

### Scope

- **In**: the `.catch`/response-handling shape of `calculateVolume()` in [`volume-splitter.js`](../../static/js/modules/volume-splitter.js); four new module-private helpers and two new module-private constants in that same file; one added line in `resetValues()`; one new `test.describe` block appended to [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts); the regenerated [`docs/test_inventory/`](../test_inventory/) artifact; this planning document.
- **Out**: the five deliberate `showErrorToast: false` sites at [`:191`](../../static/js/modules/volume-splitter.js#L191), [`:251`](../../static/js/modules/volume-splitter.js#L251), [`:288`](../../static/js/modules/volume-splitter.js#L288), [`:372`](../../static/js/modules/volume-splitter.js#L372) and [`:828`](../../static/js/modules/volume-splitter.js#L828), whose behavior must not move; [`fetch-wrapper.js`](../../static/js/modules/fetch-wrapper.js); [`toast.js`](../../static/js/modules/toast.js); the `/api/calculate_volume` server contract, status code and payload; [`routes/volume_splitter.py`](../../routes/volume_splitter.py); [`utils/volume_splitter_service.py`](../../utils/volume_splitter_service.py); volume calculations, `low`/`optimal`/`high`/`excessive` classification, recommended ranges, DB schema and API response shapes; the 300 ms debounce interval, the request payload and the call sequence; any new `.spec.ts` file and therefore any edit to [`ci.yml`](../../.github/workflows/ci.yml); any `scss/**` or `static/css/**` edit; packets U2, U3, R1, R2, R3, V1, Track P1 and Track D1; PRs #415 and #416; branch protection and repository settings.
- **Out — recorded debt owned elsewhere, explicitly not repaired here**: [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md); [`DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md) row 9; [`PRODUCT_DOCS_PLAN.md`](../PRODUCT_DOCS_PLAN.md) line 113; [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md); [`ACTIVE_DEVELOPMENT.md`](../ACTIVE_DEVELOPMENT.md).

### Artifacts

| Path | Change | Notes |
|---|---|---|
| [`static/js/modules/volume-splitter.js`](../../static/js/modules/volume-splitter.js) | modify | The whole production change. Rewrite the tail of `calculateVolume()` into two independently-mutatable failure sites; add `enterCalculateFailureState()`, `renderCalculateFailureRegion()`, `exitCalculateFailureState()`, `dismissCalculateFailureToast()`; add one call in `resetValues()`; pass one option from `scheduleCalculate()`. |
| [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts) | modify | One new `test.describe` appended. Already on `ci.yml`'s required list at [`:363`](../../.github/workflows/ci.yml#L363), so extending it is structurally free. |
| [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) · [`.md`](../test_inventory/TEST_INVENTORY.md) | regenerate | Playwright per-spec counts move. Regenerate with the generator; never hand-edit. |
| [`docs/volume_failure_feedback/PLANNING.md`](PLANNING.md) | modify | This document — Plan v1, the response matrix and Plan v2. |
| `static/js/modules/__tests__/volume-splitter.test.js` | **not created under option (i)** | Listed only so the omission is deliberate and visible. See **OD-1**. |
| [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | **not modified** | Adding a new spec file would require editing the list at [`:363`](../../.github/workflows/ci.yml#L363) and would red [`test_playwright_shard_launcher_contracts.py:65-67`](../../tests/test_playwright_shard_launcher_contracts.py#L65-L67), which pins the required set at exactly 25. |
| [`e2e/accessibility.spec.ts`](../../e2e/accessibility.spec.ts) | **not modified** | Run, not edited — see §v1.11. |

**Effort**: M · **Owner**: implementation agent, after Gate 1 sign-off · **Depends on**: **OD-1** answered; Plan v2 approved.

### v1.2 Exact production change — files, symbols, current lines, shape

All in [`static/js/modules/volume-splitter.js`](../../static/js/modules/volume-splitter.js). `showToast` is already imported and used in this module (for example at [`:217`](../../static/js/modules/volume-splitter.js#L217)), so no new import is added.

**A naming note, to prevent a collision with §0.2.** §0.2 numbers the six **call sites** 1 to 6, and the calculate call is its site 1. Everywhere below, **suppression site 1** and **suppression site 2** mean the two *suppressions inside that one call* — respectively `showErrorToast: false` at [`:131`](../../static/js/modules/volume-splitter.js#L131), which silences the request-failure class, and the `console.error`-only `.catch` at [`:136-138`](../../static/js/modules/volume-splitter.js#L136-L138), which silences the post-2xx response-handling class. That is the pairing §0.2's closing paragraph and criteria 11 and 12 refer to.

**(A) Two new module-private constants**, placed beside the existing module constants near the top of the file.

- `CALCULATE_ERROR_ID = 'volume-calculate-error'` — the single inline region's element id, which is also the uniqueness mechanism Q4 relies on.
- `CALCULATE_ERROR_MESSAGE` — one plain-English sentence in the register Section 0's copy assumption measured, ending `Please try again.` to match four of the five existing messages in this file ([`:217`](../../static/js/modules/volume-splitter.js#L217), [`:263`](../../static/js/modules/volume-splitter.js#L263), [`:318`](../../static/js/modules/volume-splitter.js#L318), [`:439`](../../static/js/modules/volume-splitter.js#L439)). It must say both things the user needs: the calculation failed, **and** the previous results were cleared. Exact wording is a one-line detail for Plan v2; the two required propositions are the contract.

**(B) `calculateVolume()`** — [`:111-139`](../../static/js/modules/volume-splitter.js#L111-L139). Two edits, and nothing else in the function moves.

1. The signature gains one defaulted option: `function calculateVolume(options = {})` destructuring `{ announceFailure = true }`. Because it is defaulted, the four call sites that are not modified — the Calculate button at [`:64`](../../static/js/modules/volume-splitter.js#L64), `loadPlan()` at [`:213`](../../static/js/modules/volume-splitter.js#L213), `setMode()` at [`:533`](../../static/js/modules/volume-splitter.js#L533) and the slider `change` listener at [`:633`](../../static/js/modules/volume-splitter.js#L633) — keep today's behavior exactly, and the request payload built at [`:112-124`](../../static/js/modules/volume-splitter.js#L112-L124) is untouched. Criterion 9 holds by construction.
2. The promise tail at [`:134-138`](../../static/js/modules/volume-splitter.js#L134-L138) is replaced. `showErrorToast: false` at [`:131`](../../static/js/modules/volume-splitter.js#L131) **stays**, per §v1.0 and OD-4. The new tail is:

   - `.then(response => response.data)` — unchanged.
   - `.then(data => { … })` whose body is a `try` calling `handleCalculateResponse(data)`, followed on success by `exitCalculateFailureState()`; and a `catch (error)` that logs a diagnostic `console.error` and calls `enterCalculateFailureState({ announce: announceFailure })`, then `return`s. **This inner `catch` is suppression site 2's replacement and the sole handler of the post-2xx response-handling failure class.**
   - `.catch(error => { … })` that logs a diagnostic `console.error` and calls `enterCalculateFailureState({ announce: announceFailure })`. **This outer `.catch` is suppression site 1's replacement and the sole handler of the request-failure class — non-2xx via [`fetch-wrapper.js:200-217`](../../static/js/modules/fetch-wrapper.js#L200-L217) and transport failure via [`:244-247`](../../static/js/modules/fetch-wrapper.js#L244-L247).**

   **Why the inner `try`/`catch` rather than one shared `.catch`.** It is load-bearing, not stylistic. A single handler would make the two failure classes converge on one line, and then no mutation could restore one class's suppression *in isolation* — criteria 11 and 12 would be provable only jointly, which §0.2 explicitly forbids. The inner `catch` also stops a rendering throw from reaching the outer `.catch`, so exactly one failure treatment runs per failed calculation.

   **One classification edge, stated rather than hidden.** If `response` were ever nullish, `response.data` throws inside the first `.then` and lands in the outer `.catch`, i.e. it is classified as a request failure. This cannot arise against the measured server contract (the wrapper returns a parsed object or throws) and is recorded only so a reviewer does not mistake it for an unnoticed hole.

   **A second edge**: if `enterCalculateFailureState()` itself threw inside the inner `catch`, the rejection would reach the outer `.catch` and the handler would run twice. The region helper is idempotent (below), so the observable outcome would still be one region; the toast could double-fire. This is noted, not defended, and is a legitimate target for reviewer challenge.

**(C) `enterCalculateFailureState({ announce })`** — new. Order matters:

1. `clearResults()` — [`:870-899`](../../static/js/modules/volume-splitter.js#L870-L899). Carries criteria 3, 4 and 7 in one call; see §v1.4.
2. Record whether a region is already standing: `const standing = Boolean(document.getElementById(CALCULATE_ERROR_ID))`.
3. `renderCalculateFailureRegion()` — creates the region if and only if none stands.
4. Toast, conditionally: `if (announce || !standing) { showToast('error', CALCULATE_ERROR_MESSAGE, { action: { label: 'Retry', ariaLabel: 'Retry volume calculation', onClick: () => calculateVolume() } }) }`. See §v1.5 and **OD-2**.

**(D) `renderCalculateFailureRegion()`** — new, and **idempotent by contract**. It returns immediately if `document.getElementById(CALCULATE_ERROR_ID)` exists. It does not rewrite the message text on a repeat failure, because rewriting identical text still mutates the DOM and is exactly the kind of churn Q4 rules out. Otherwise it builds the node with `createElement` and `textContent` — never `innerHTML`, since the message is static and the file's `innerHTML` uses are all for server data — assigns `id = CALCULATE_ERROR_ID`, `className = 'volume-calculate-error alert alert-danger …'`, `data-testid="volume-calculate-error"`, appends a message `<span>` and a `<button type="button" data-testid="volume-calculate-retry" aria-label="Retry volume calculation">Retry</button>` whose click handler is `() => calculateVolume()`, and inserts it with `panel.prepend(region)` where `panel` is `document.querySelector('.volume-insights-panel')`.

**Placement, and why it is safe.** The aside is at [`volume_splitter.html:83`](../../templates/volume_splitter.html#L83) and the region lands immediately before `.results-section` at [`:85`](../../templates/volume_splitter.html#L85) — adjacent to the results, as Q2 requires. That position is **outside** the `AGENT:START B-5 PRIORITY-CLASSES` marker, which opens at [`:87`](../../templates/volume_splitter.html#L87) and closes at [`:143`](../../templates/volume_splitter.html#L143), so the marked block is not disturbed. `prepend` on a missing panel is guarded by the early return.

**(E) `exitCalculateFailureState()`** — new. `document.getElementById(CALCULATE_ERROR_ID)?.remove()`, then `dismissCalculateFailureToast()`. **`remove()`, never `classList.add('d-none')`** — Q5 strict forbids a permanently present element, and a hidden-but-present node is exactly what it rules out. Both calls are no-ops when nothing stands, so the success path gains no observable state.

**(F) `dismissCalculateFailureToast()`** — new, and deliberately narrow. `showToast`'s default duration is 3000 ms ([`toast.js:33`](../../static/js/modules/toast.js#L33)), so a success arriving within three seconds of a failure would otherwise leave an error toast standing over fresh results — a failure-only affordance surviving a success, which Q5 strict forbids. The helper finds `#liveToast`, checks it still contains `button[aria-label="Retry volume calculation"]` so that a success toast from an unrelated save or activate action is never dismissed, and calls `bootstrap.Toast.getInstance(toastElement)?.hide()`. That is the same public Bootstrap API [`toast.js`](../../static/js/modules/toast.js) itself uses at [`:74`](../../static/js/modules/toast.js#L74) and [`:103`](../../static/js/modules/toast.js#L103), so **no change to `toast.js` is required or made**.

**(G) `resetValues()`** — [`:178-185`](../../static/js/modules/volume-splitter.js#L178-L185). Add `exitCalculateFailureState()` after the existing `clearResults()` at [`:184`](../../static/js/modules/volume-splitter.js#L184). Reset issues no request, so this is not the calculation success path; the justification is that leaving a standing "we could not calculate" banner above freshly zeroed sliders reproduces precisely the input-output mismatch U1 exists to remove. It changes no request behavior and adds no permanent state. Flagged as **OD-3** because it is a judgement call, not something Gate 0 decided.

**(H) `scheduleCalculate()`** — [`:863-868`](../../static/js/modules/volume-splitter.js#L863-L868). The single change is the timer body at [`:867`](../../static/js/modules/volume-splitter.js#L867): `calculateVolume()` becomes `calculateVolume({ announceFailure: false })`. **The 300 ms interval, the `clearTimeout` guard and the call sequence are unchanged** — criterion 9.

**Untouched by name**, so a reviewer can confirm the blast radius: `displayResults()` [`:141`](../../static/js/modules/volume-splitter.js#L141), `displaySuggestions()` [`:322`](../../static/js/modules/volume-splitter.js#L322), `setMode()` [`:511`](../../static/js/modules/volume-splitter.js#L511), `renderSliders()` [`:537`](../../static/js/modules/volume-splitter.js#L537), `updateValueDisplay()` [`:694`](../../static/js/modules/volume-splitter.js#L694), `applyServerRanges()` [`:718`](../../static/js/modules/volume-splitter.js#L718), `handleCalculateResponse()` [`:748`](../../static/js/modules/volume-splitter.js#L748), `applyStatusToRow()` [`:763`](../../static/js/modules/volume-splitter.js#L763), `clearResults()` [`:870`](../../static/js/modules/volume-splitter.js#L870), and `loadPlan()` [`:187`](../../static/js/modules/volume-splitter.js#L187) apart from its existing `calculateVolume()` call at [`:213`](../../static/js/modules/volume-splitter.js#L213), which is left exactly as it is.

### v1.3 State transitions, enumerated

The page does not calculate on load: `init()` ends at [`:94-97`](../../static/js/modules/volume-splitter.js#L94-L97) with `renderSliders()` and the history fetch, and never calls `calculateVolume()`. Every calculation is therefore user-initiated or plan-initiated, which is what makes T1 below a real state rather than a page-load artifact.

| # | Transition | Entry path | What the user sees afterwards |
|---|---|---|---|
| **T1** | **First-load failure** — no calculation has ever succeeded on this load | Calculate button [`:64`](../../static/js/modules/volume-splitter.js#L64), a slider, or a mode switch | Toast plus inline region. `clearResults()` re-adds `d-none` to both sections at [`:876-877`](../../static/js/modules/volume-splitter.js#L876-L877), which are already hidden — so the empty results and suggestions sections stay hidden. **Criterion 7 is carried by the same call that carries criterion 3, with no special case.** |
| **T2** | **Failure after a prior success** | Calculate button or slider `change` [`:633`](../../static/js/modules/volume-splitter.js#L633) | Toast plus inline region; previous table rows, suggestion cards, `.muscle-row` status classes and `.volume-value-pill--*` modifiers all gone. The sections return to `d-none`. |
| **T3** | **Mode-switch failure** | `setMode()` → `calculateVolume()` at [`:533`](../../static/js/modules/volume-splitter.js#L533), after `renderSliders()` at [`:528`](../../static/js/modules/volume-splitter.js#L528) already rebuilt every `.muscle-row` | Toast plus inline region. The previous mode's results and suggestions — the surviving divergence §0.1 measured — are cleared by the same `clearResults()`. The freshly rendered sliders carry no status classes because `renderSliders()` rebuilt them; `clearResults()` iterating `.muscle-row` is a harmless no-op on that path. **Criterion 4.** |
| **T4** | **Load-plan failure** | `loadPlan()` → `setMode(…, { skipCalculate: true })` then `calculateVolume()` at [`:212-213`](../../static/js/modules/volume-splitter.js#L212-L213) | Same as T3. Note this is a failure of the **calculate** call; a failure of the plan `GET` itself is site 2 in §0.2, deliberate, and unchanged. |
| **T5** | **Retry** | The toast's Retry action, the region's Retry button, or the Calculate button, which stays enabled throughout | A fresh `POST` from the inputs as they stand. `announceFailure` defaults to `true` on all three, so a retry that fails again always produces fresh feedback rather than appearing to do nothing. **Criterion 5.** |
| **T6** | **Repeated failure during a sustained fault** | Debounced `scheduleCalculate()` firing every 300 ms during a drag | Exactly **one** region — `renderCalculateFailureRegion()` returns early, so the node is not replaced and its text is not rewritten — and **no** repeat toast, because `announceFailure` is `false` on the debounced path and a region is standing. The `change` event at drag release calls `calculateVolume()` with the default, so the user gets one announcement when they let go. **Criterion 6.** |
| **T7** | **The later success that clears everything** | Any successful `POST` | `exitCalculateFailureState()` removes the region from the DOM and dismisses a still-standing calculate-failure toast; `handleCalculateResponse()` repaints results, suggestions, status classes, pill modifiers and server ranges exactly as today. **Criteria 5 and 8.** |
| **T8** | **Reset while a failure stands** | Reset button → `resetValues()` [`:178`](../../static/js/modules/volume-splitter.js#L178) | Sliders zeroed, results cleared, region removed. No request is issued. See **OD-3**. |

### v1.4 Clearing and reset, surface by surface

Q1 signed "clear". `clearResults()` at [`:870-899`](../../static/js/modules/volume-splitter.js#L870-L899) was read line by line and **already covers exactly the surface set criterion 3 enumerates**. It is reused as-is; it is not modified, wrapped or duplicated.

| Stale surface | Covered by | Line |
|---|---|---|
| Results table body `#results-body` | `clearResults()` — `resultsBody.innerHTML = ''` | [`:879-881`](../../static/js/modules/volume-splitter.js#L879-L881) |
| Suggestion cards in `.suggestions-container` | `clearResults()` — `suggestionsContainer.innerHTML = ''` | [`:883-885`](../../static/js/modules/volume-splitter.js#L883-L885) |
| `.results-section` visibility | `clearResults()` — re-adds `d-none` | [`:876`](../../static/js/modules/volume-splitter.js#L876) |
| `.ai-suggestions-section` visibility | `clearResults()` — re-adds `d-none` | [`:877`](../../static/js/modules/volume-splitter.js#L877) |
| Per-muscle `status-low` / `status-optimal` / `status-high` / `status-excessive` on every `.muscle-row` | `clearResults()` | [`:887-888`](../../static/js/modules/volume-splitter.js#L887-L888) |
| `volume-value-pill--low` / `--optimal` / `--high` / `--excessive` on every `.current-value` badge | `clearResults()` | [`:889-897`](../../static/js/modules/volume-splitter.js#L889-L897) |

**Nothing in criterion 3's enumeration is left uncovered, and no new clearing helper is written.**

Two surfaces are deliberately **outside** the stale set, each with its reason stated so a reviewer can contest it:

- **The slider value badge text, repainted by `updateValueDisplay()` on `input`** ([`:694-700`](../../static/js/modules/volume-splitter.js#L694-L700)). **Out.** It is an echo of the slider's own current value — an *input*, not calculation output. Resetting it would desynchronize the badge from the thumb position and would itself be a user-visible change to input state, which criterion 9 protects. What made it misleading in §0.1's reading was the *pill colour modifier* sitting on the same element, and that modifier **is** cleared, by [`:889-897`](../../static/js/modules/volume-splitter.js#L889-L897). Note that [`volume-splitter.spec.ts:33-39`](../../e2e/volume-splitter.spec.ts#L33-L39) already asserts badge text tracks slider value, so clearing it would red an existing test.
- **The slider track gradient**, painted by `updateSliderTrack()` [`:643`](../../static/js/modules/volume-splitter.js#L643) from `modeRangeState`, which `applyServerRanges()` [`:718`](../../static/js/modules/volume-splitter.js#L718) last updated from a successful response. **Out.** Criterion 3 enumerates four surfaces and the track is not among them; criterion 8 lists "server-supplied ranges and slider track paint" as state to preserve. A recommended range is a property of the muscle and mode, not of the failed calculation's inputs. On T3 and T4, `renderSliders()` → `updateAllSliderTracks()` [`:556`](../../static/js/modules/volume-splitter.js#L556) has already repainted from the new mode's state before the request is sent, so no cross-mode range leak survives the failure.

### v1.5 The two failure surfaces under Q5 strict — create, update, replace, remove

| | Inline region | Toast |
|---|---|---|
| **Create** | On the first failure since the last success. `renderCalculateFailureRegion()` builds the node and `prepend`s it to `.volume-insights-panel`. Before that moment the element does not exist anywhere — not in [`volume_splitter.html`](../../templates/volume_splitter.html), not hidden, not empty. | `showToast('error', …)` on the transition into failure, and on every user-initiated attempt thereafter. |
| **Update** | **Never on a repeat failure.** The early return means no attribute is rewritten and no text node is replaced. There is one message and one state, so there is nothing to update. | `showToast` rewrites `#toast-body` ([`toast.js:60-63`](../../static/js/modules/toast.js#L60-L63)) each time it is called. |
| **Replace** | Not applicable — the node is never replaced while a failure stands. This is what keeps criterion 6's "updated or replaced rather than duplicated" satisfiable by the strongest available reading: **not duplicated and not churned**. | Structurally guaranteed by [`toast.js`](../../static/js/modules/toast.js): a single `#liveToast` element, body cleared at [`:60-63`](../../static/js/modules/toast.js#L60-L63), any live `bootstrap.Toast` instance disposed and a new one constructed at [`:101-109`](../../static/js/modules/toast.js#L101-L109). **Toasts replace; they cannot stack.** This was read and confirmed rather than assumed, because criterion 6 rests on it. |
| **Remove** | `exitCalculateFailureState()` calls `.remove()`. **Not `d-none`.** After any success the DOM contains no `#volume-calculate-error` at all. | Auto-dismisses after 3000 ms ([`toast.js:33`](../../static/js/modules/toast.js#L33)); additionally dismissed on success by `dismissCalculateFailureToast()` when it is still ours, so the window in which an error toast can overlap fresh results is closed. |

**Q5 strict, restated as the property the code must have**: `#volume-calculate-error` exists **if and only if** the last completed calculation failed. Never on load, never after a success, never as a hidden shell. §v1.9's mutation **M5** exists to prove the test suite can actually detect a violation of this.

### v1.6 Retry — mechanism and payload freshness

The Retry affordance appears in two places and both use the **same** mechanism: an `onClick` of `() => calculateVolume()`, identical to the Calculate button's listener at [`:64`](../../static/js/modules/volume-splitter.js#L64).

- **It re-reads the DOM at click time. It does not replay a captured payload.** `calculateVolume()` re-reads `#training-days`, then calls `collectVolumes()` [`:702`](../../static/js/modules/volume-splitter.js#L702) and `collectRanges()` [`:714`](../../static/js/modules/volume-splitter.js#L714), all of which query live elements. **Why**: criterion 5 says the fresh `POST` is issued "from the input values as they stand at that moment". A captured payload would silently resend inputs the user has since changed — the user moves a slider while the failure banner stands, presses Retry, and gets numbers for values that are no longer on screen. That is a new instance of the very mismatch U1 is repairing.
- **No debounce on Retry.** It calls `calculateVolume()` directly, not `scheduleCalculate()`, so it is immediate and matches the button.
- **No automatic retry is introduced.** `retries` stays at the wrapper's `POST` default of `0` ([`fetch-wrapper.js:140`](../../static/js/modules/fetch-wrapper.js#L140)); the plan passes no `retries` option and adds no loop. Q3.
- The toast's action button hides the toast before invoking `onClick` ([`toast.js:73-83`](../../static/js/modules/toast.js#L73-L83)), which is why `announceFailure` defaults to `true` on retry — otherwise a second failure after Retry would produce no visible change at all.
- The in-repository precedent for `options.action` is this same file at [`:299-306`](../../static/js/modules/volume-splitter.js#L299-L306); the plan copies that shape, including `ariaLabel`.

### v1.7 Focus and live-region behavior

**Announcement.** The toast carries it. `#liveToast` has `role="alert"`, `aria-live="assertive"`, `aria-atomic="true"` and its container has `aria-live="polite"` plus `data-testid="toast-container"` ([`base.html:235-251`](../../templates/base.html#L235-L251)). Gate 0 forbids treating that inherited markup as the **sole** evidence, so arm (c) asserts both the live-region attributes **and** that the failure message text actually lands inside `#toast-body` while the toast is visible — the property, not the inheritance.

**The inline region is deliberately not a live region.** It gets **no** `role="alert"`, `role="status"` or `aria-live`. Reason: with the toast already announcing assertively, a second live region would double-announce every failure, and during a sustained fault the pairing would be actively hostile. The region is a persistent visual and programmatic artifact, first in the reading order of the insights panel, discoverable by navigation. Its Retry button carries `aria-label="Retry volume calculation"`. This is a design decision open to reviewer challenge; the alternative — `role="status"` on the region and no toast announcement — was rejected because Q2 signed the toast as the immediate-notification surface.

**Focus.** **No code path added by this plan calls `.focus()`, `scrollIntoView()`, `autofocus`, or `tabindex="-1"` plus focus.** The guarantee to assert is: after a failure, `document.activeElement` is the same element it was before. Specifically —

- **Mid-drag**: the user's focus is on `input.volume-slider`. The debounced failure inserts the region above the results in a different subtree; inserting a sibling does not move focus. The assertion reads back `document.activeElement`'s `data-muscle` and compares.
- **Button path**: focus is on `#calculate-volume` ([`volume_splitter.html:61`](../../templates/volume_splitter.html#L61)) and stays there.
- The one pre-existing focus move in this module is `summary?.focus()` at [`:312`](../../static/js/modules/volume-splitter.js#L312), on the save-and-activate success path. It is untouched and is not on the calculate path.

### v1.8 The three regression arms

All three live in one new `test.describe('Volume Splitter calculation failure feedback')` appended to [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts). **No new spec file** — see §v1.1 and the artifacts table.

**The console-error collector, handled explicitly.** The existing describe blocks call `consoleErrors.assertNoErrors()` ([`:41-50`](../../e2e/volume-splitter.spec.ts#L41-L50)). The collector's allow-list at [`fixtures.ts:29-44`](../../e2e/fixtures.ts#L29-L44) filters the wrapper's own `API Error` logs, but it does **not** filter a page-specific message such as `Error calculating volume:`, and the fixture exposes no per-test allow-list ([`:71-75`](../../e2e/fixtures.ts#L71-L75)). The repaired failure path deliberately keeps a diagnostic `console.error`. Therefore the new describe block **does not use the `consoleErrors` fixture**, with an in-file comment saying why and pointing at [`error-handling.spec.ts:62-64`](../../e2e/error-handling.spec.ts#L62-L64), which takes exactly the same route for exactly the same reason. **The existing blocks are left untouched and keep asserting no console errors — that is the guard that the repair adds no console noise to the success path** (§v1.10).

**Arm (a) — request-failure class.** Two tests, because the class has two entry points in the wrapper.

- `a1` — non-2xx after a prior success. Calculate once cleanly and assert results are visible; then `await page.route('**/api/calculate_volume', route => route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ ok: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to calculate volume' } }) }))`, matching the idiom at [`error-handling.spec.ts:71-77`](../../e2e/error-handling.spec.ts#L71-L77) and the real server payload; click Calculate. **Assertions**: `#volume-calculate-error` is visible and has count 1; `expectToast(page, /calculate/i)` via the helper at [`fixtures.ts:326`](../../e2e/fixtures.ts#L326); `#results-body tr` has count 0; `.results-section` and `.ai-suggestions-section` are hidden; no `.muscle-row` carries a `status-*` class; no `.current-value` carries a `volume-value-pill--*` modifier; `#calculate-volume` is still enabled.
- `a2` — transport failure. `route.abort('failed')`, the idiom at [`error-handling.spec.ts:148`](../../e2e/error-handling.spec.ts#L148). Same assertions. This is the arm that proves the wrapper's outer branch at [`fetch-wrapper.js:244-247`](../../static/js/modules/fetch-wrapper.js#L244-L247) is covered and not just the HTTP-error branch.
- `a3` — dedup under a sustained fault (criterion 6). With the 500 route standing, focus a slider and dispatch several `input` events spaced past the 300 ms debounce; after the first region appears, stamp it via `page.evaluate` with a `data-probe` attribute, drive further failures, then assert `#volume-calculate-error[data-probe="1"]` still has count 1. **Stamping is what makes "not replaced" measurable** — a plain count of 1 cannot distinguish a surviving node from a node destroyed and rebuilt.

**Arm (b) — post-2xx response-handling class.** `b1` fulfills a **200** whose body is well-formed JSON that makes `handleCalculateResponse()` throw: `{ "ok": true, "data": { "results": { "Chest": null }, "ranges": {}, "suggestions": [] } }`. The wrapper returns the parsed body and `.then(response => response.data)` unwraps to the inner object, so `displayResults()` reaches `data.weekly_sets` on a `null` at [`:161`](../../static/js/modules/volume-splitter.js#L161) and raises a `TypeError` **inside** the response handler, where the wrapper's toast is never reached. **Assertions**: the same failure surfaces as `a1`. This is the arm §0.2 says cannot be folded into arm (a), and it is the only arm that exercises the inner `catch`.

**Arm (c) — accessibility.** Two tests, both explicit assertions rather than inherited-markup claims.

- `c1` — announcement. Drive a 500 failure; assert `#liveToast` is visible and carries `role="alert"` and `aria-live="assertive"`; assert `[data-testid="toast-container"]` carries `aria-live="polite"`; and assert `#toast-body` contains the failure message text while visible. The third assertion is the one that makes this a behavior test — attributes alone would only re-assert [`base.html:235-251`](../../templates/base.html#L235-L251).
- `c2` — no disruptive focus movement, measured **mid-drag**, which is the hostile case. With the 500 route standing, `focus()` a `input.volume-slider`, dispatch `input` only (not `change`) to drive the debounced path, wait for `#volume-calculate-error` to appear, then assert via `page.evaluate` that `document.activeElement` is still that slider — compared by its `data-muscle` — that its value is unchanged, and that neither the region nor its Retry button is the active element. Repeat the same check for the Calculate-button path, where `#calculate-volume` must retain focus.

**Success-path and recovery tests** (`s1`–`s3`) are specified in §v1.10 and live in the same block.

### v1.9 Mutation and negative-control proof

Every mutation is a hand edit to [`static/js/modules/volume-splitter.js`](../../static/js/modules/volume-splitter.js), run in **both directions** — mutate, observe the expected red, then revert with `git checkout -- static/js/modules/volume-splitter.js` and observe green again. **Never revert by retyping the line**; a same-shape hand revert is how a live mutation survives a "verified" pass.

Base command, from the worktree root:

`npx playwright test e2e/volume-splitter.spec.ts --project=chromium --reporter=line -g "calculation failure feedback"`

Narrow to a single arm by replacing the `-g` pattern with that test's title.

| ID | Exact mutation | Restores | Expected result |
|---|---|---|---|
| **M1** | In the **outer** `.catch` of `calculateVolume()`, delete the `enterCalculateFailureState(…)` call, leaving the `console.error` line and nothing else. | Suppression site 1 — the `console.error`-only catch for the **request-failure** class, reproducing today's user-visible silence for non-2xx and transport failures. | `a1`, `a2`, `a3`, `c1`, `c2` **RED**. `b1` **GREEN** — this is the isolation proof: the post-2xx class is untouched. **Criterion 11.** |
| **M2** | In the **inner** `catch` of the response `.then`, delete the `enterCalculateFailureState(…)` call, leaving the `console.error` and the `return`. | Suppression site 2 — the `console.error`-only catch for the **post-2xx response-handling** class. | `b1` **RED**. `a1`, `a2`, `a3`, `c1`, `c2` **GREEN** — the isolation proof in the other direction. **Criterion 12.** |
| **M3** | Delete `clearResults()` from `enterCalculateFailureState()`. | Nothing — this measures the reviewer, not the code. | `a1` **RED** on the stale-clearing assertions. Proves criterion 3 is carried by an assertion rather than by the sections happening to be hidden. |
| **M4** | Append `region.querySelector('button')?.focus();` to `renderCalculateFailureRegion()`. | Nothing — measures the reviewer. | `c2` **RED**. Proves the focus guarantee is actually asserted and not merely stated in prose. |
| **M5** | Change `exitCalculateFailureState()` to `classList.add('d-none')` instead of `.remove()`. | Nothing — measures the reviewer. | `s2` **RED**. Proves Q5 strict is enforced by a DOM-absence assertion, not by a visibility assertion that a hidden shell would satisfy. |
| **M6** | Delete the early-return guard in `renderCalculateFailureRegion()` so every failure removes and rebuilds the node. | Nothing — measures the reviewer. | `a3` **RED** on the `data-probe` survival check. Proves the dedup requirement is measured, not assumed. |

**M1 and M2 together discharge §0.2's closing obligation**: the regression reds if either site-1 suppression is restored *in isolation*, and each arm fails for its own class only. **M3–M6 exist because an arm that cannot be made to fail is not evidence.**

**Note on M1's framing** — see **OD-4**. Under this plan `showErrorToast: false` at [`:131`](../../static/js/modules/volume-splitter.js#L131) is retained deliberately, so "restoring the request-failure suppression" means restoring the `console.error`-only handler, which reproduces today's silence exactly. Re-adding the flag is not available as a mutation because the flag was never removed.

### v1.10 Success-path invariants — proving Q5 strict held

| ID | Assertion | Carries |
|---|---|---|
| `s1` | With no route interception, complete a normal calculation. Before and after, `[data-testid="volume-calculate-error"]` has count **0** — asserted as absence from the DOM, not as hidden. Results section visible, `#results-body` rows present, status classes and pill modifiers applied. | Criterion 8; Q5 strict |
| `s2` | Failure-then-success recovery. Drive a 500, assert the region is present, then `page.unroute('**/api/calculate_volume')` and click Calculate. Assert `#volume-calculate-error` has count **0** — removed, not hidden — and results are visible again. | Criteria 5 and 8; killed by **M5** |
| `s3` | After that success, `#liveToast` no longer contains `button[aria-label="Retry volume calculation"]`, or is not visible. Proves a standing error toast does not survive a success. | Q5 strict |
| `s4` | **Inherited, not newly written.** Every existing describe block in [`volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts) keeps `consoleErrors.assertNoErrors()` ([`:41-50`](../../e2e/volume-splitter.spec.ts#L41-L50)), so any new console output on the success path reds them. This is why the new failure block is scoped separately rather than the fixture being loosened. | Criterion 8 |
| `s5` | **Inherited, not newly written.** [`accessibility.spec.ts`](../../e2e/accessibility.spec.ts) pins `'volume_splitter:light'` at [`:834`](../../e2e/accessibility.spec.ts#L834) and `'volume_splitter:dark'` at [`:839`](../../e2e/accessibility.spec.ts#L839), each at `[{ rule: 'color-contrast', nodes: 2 }]`. **Q5 strict is what protects these pins**: because the region is absent from the DOM in every non-failure state, the axe scan sees exactly what it sees today. The spec is **run, not edited**, and the failure state is deliberately **not** added to the axe scan — doing so would move the pinned node counts and turn an a11y regression gate into a maintenance chore. | Criterion 8; the a11y pins |
| `s6` | Criterion 10 — the five deliberate sites. `git diff` must show no change at [`:191`](../../static/js/modules/volume-splitter.js#L191), [`:251`](../../static/js/modules/volume-splitter.js#L251), [`:288`](../../static/js/modules/volume-splitter.js#L288), [`:372`](../../static/js/modules/volume-splitter.js#L372) or [`:828`](../../static/js/modules/volume-splitter.js#L828) or in their `.catch` bodies. Behaviorally, the save-plan and history paths are already exercised by the existing tests at [`:289-386`](../../e2e/volume-splitter.spec.ts#L289-L386). | Criterion 10 |

### v1.11 Test routing and the gate set for the implementation PR

Changed paths under option (i): `static/js/modules/volume-splitter.js`, `e2e/volume-splitter.spec.ts`, `docs/test_inventory/TEST_INVENTORY.json` and `.md`, `docs/volume_failure_feedback/PLANNING.md`.

Routing derived from [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md): the **Frontend (JS)** row ([`:30`](../ai_workflow/QUALITY_GATE.md#L30)) → the feature map ([`:126`](../ai_workflow/QUALITY_GATE.md#L126)) gives `volume-splitter.spec.ts` and `volume-progress.spec.ts`, plus manual smoke because the surface is interactive; the error/accessibility row ([`:129`](../ai_workflow/QUALITY_GATE.md#L129)) adds `error-handling.spec.ts` and `accessibility.spec.ts`; the **E2E spec** row ([`:33`](../ai_workflow/QUALITY_GATE.md#L33)) says run the spec; the **Product docs** row ([`:37`](../ai_workflow/QUALITY_GATE.md#L37)) requires nothing further. The `Test Inventory Drift` gate ([`:51`](../ai_workflow/QUALITY_GATE.md#L51)) is triggered by the Playwright per-spec count change.

Run in this order:

1. **Regenerate the inventory** — `.venv/Scripts/python.exe scripts/generate_test_inventory.py`, then commit [`docs/test_inventory/`](../test_inventory/). Verify with `.venv/Scripts/python.exe scripts/generate_test_inventory.py --check` exiting 0. **Never hand-edit the artifact.** Before regenerating, confirm no untracked or gitignored `.md` sits in a globbed surface directory — that reds `--check` locally while CI is green and bakes the local file into the committed artifact.
2. **`npm run test:js`** — must report **13 files / 231 cases**, unchanged. This is the affirmative proof that U1 did not move the suite under qualification (§v1.1) and that no production edit broke Vitest collection, which [`QUALITY_GATE.md:60`](../ai_workflow/QUALITY_GATE.md#L60) names as an inventory trip.
3. **`npx tsc --noEmit`** — zero errors; the blocking half of the `Type Check` job.
4. **`npx playwright test e2e/volume-splitter.spec.ts --project=chromium --reporter=line`** — the whole spec, not only the new block, so the untouched success-path blocks and their `assertNoErrors()` run too.
5. **`npx playwright test e2e/volume-progress.spec.ts e2e/error-handling.spec.ts e2e/accessibility.spec.ts --project=chromium --reporter=line`** — `accessibility.spec.ts` is the proof for `s5`.
6. **`.venv/Scripts/python.exe -m pytest tests/ -q`** — full suite. No path glob routes to [`tests/test_playwright_shard_launcher_contracts.py`](../../tests/test_playwright_shard_launcher_contracts.py), whose `== 25` pin at [`:65-67`](../../tests/test_playwright_shard_launcher_contracts.py#L65-L67) must be shown intact, and the suite is cheap enough that narrowing buys nothing.
7. **Manual smoke** via the `run-hypertrophy-toolbox` skill: load `/volume_splitter`, calculate successfully, then stop the server or use devtools request blocking to force a failure and eyeball the region, the toast, Retry, and the return to normal on success. Required by the Frontend (JS) row.
8. **The mutation matrix in §v1.9**, both directions, before the PR is marked ready.

**Not run, and why**: `/build-css` and the `visual.spec.ts` matrix — no `scss/**` or `static/css/**` file changes and no rest-state paint moves. `scripts/pyright_baseline_diff.py` — no `.py` changes.

**Diff-time reviewers**: `/unslop` — `code-reviewer` **and** `unslop-reviewer`, both, because they catch disjoint failure modes.

**PR workflow**: create the PR, poll CI to zero pending, mark ready, then **stop**. Merge only on a separate explicit owner confirmation naming the PR.

### v1.12 Scope containment and rollback

**Containment.** One production file, one spec file, one regenerated artifact, one planning document. The production change is additive apart from the rewritten promise tail of one function and two single-line edits ([`:184`](../../static/js/modules/volume-splitter.js#L184) and [`:867`](../../static/js/modules/volume-splitter.js#L867)). No exported symbol is added or renamed — all four helpers and both constants are module-private, so nothing outside this file can come to depend on them. No import is added. No template, stylesheet, route or service file is touched, so the change cannot reach the server, the schema or any calculation.

**Rollback.** The change is a single-file revert: `git checkout -- static/js/modules/volume-splitter.js` restores today's behavior completely, because every new surface is created at runtime by that file and nothing is persisted. If the spec block also needs to come out, revert [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts) **and re-run step 1** — a partial revert that leaves the committed inventory describing tests that no longer exist reds `Test Inventory Drift`. Work happens in an isolated worktree; if the suite reds and the fix is not obvious within one attempt, `git stash push -- <file>` immediately rather than accumulating a second speculative change on top.

**Blast-radius checks before marking ready**: `git diff --stat` shows exactly the four paths above; `git diff` shows no hunk touching the five deliberate sites (`s6`); `npm run test:js` still prints 13 files / 231 cases; [`ci.yml`](../../.github/workflows/ci.yml) is unmodified.

### v1.13 Open decisions carried into the council

| ID | Decision | Recommended default | Blocking? |
|---|---|---|---|
| **OD-1** | Coverage routing versus the live JS-unit qualification window — options (i), (ii), (iii) in §v1.1. | **(i)** now, **(iii)** as a tracked follow-up. | **Yes.** Implementation cannot start until this is answered; the artifacts table and §v1.11 both assume (i). |
| **OD-2** | Q4 interpretation. This plan suppresses the repeat toast while a region stands **and** the attempt was debounce-driven, while always announcing on a user-initiated attempt. The owner chose (a) "replace rather than stack" and explicitly did not choose (c) "cooldown". Is transition-plus-user-initiated announcement within (a)? | **Yes, keep it.** The alternative — re-fire the toast on every one of roughly three failures per second during a drag, relying on `toast.js` to replace — satisfies the letter of (a) but produces continuous assertive re-announcement. | No. A one-line change either way. |
| **OD-3** | Should `resetValues()` clear a standing failure region (§v1.2 G)? | **Yes.** Reset's contract is a blank page, and a stale banner over zeroed sliders is the same mismatch U1 exists to remove. | No. |
| **OD-4** | Criterion 11's mutation reading (§v1.0). Restore the `console.error`-only handler, or literally re-add `showErrorToast: false`? | **The former.** The latter would force flipping the flag, which collides with Q3 — the wrapper's toast cannot carry a Retry action — and with §0.2's finding that the flag plus a page-specific replacement is this file's deliberate idiom. | **Conditionally.** If the owner requires the literal reading, Q3 and criterion 11 cannot both hold and **Gate 0 must be reopened.** |

### Sequence

1. **Answer OD-1.** Do not start until it is answered.
2. Rewrite the promise tail of `calculateVolume()` into the two independent failure sites, with the diagnostic `console.error` retained at each; add the option parameter.
3. Add the two constants and the four helpers; add the `resetValues()` line and the `scheduleCalculate()` option.
4. Add the new `test.describe` block: arms `a1`–`a3`, `b1`, `c1`–`c2`, and `s1`–`s3`.
5. Run steps 1–6 of §v1.11 and get them green.
6. Run the §v1.9 mutation matrix, both directions, and record the observed result for every row against its expectation. A row that does not red as predicted is a defect in the arm, not a pass.
7. Manual smoke (§v1.11 step 7).
8. `/unslop` — `code-reviewer` and `unslop-reviewer`. Then open the PR, poll CI to zero pending, mark ready, and **stop**.

### Expected gates

*Proposed by the `product-manager`; `test-strategist` owns this block at council review and may replace it.*

- **pytest**: full suite — `.venv/Scripts/python.exe -m pytest tests/ -q`. Named specifically: [`tests/test_playwright_shard_launcher_contracts.py`](../../tests/test_playwright_shard_launcher_contracts.py) must stay green with its `== 25` pin at [`:65-67`](../../tests/test_playwright_shard_launcher_contracts.py#L65-L67) intact.
- **e2e**: [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts) (whole spec), [`e2e/volume-progress.spec.ts`](../../e2e/volume-progress.spec.ts), [`e2e/error-handling.spec.ts`](../../e2e/error-handling.spec.ts), [`e2e/accessibility.spec.ts`](../../e2e/accessibility.spec.ts).
- **js-unit**: `npm run test:js` — asserted **unchanged** at 13 files / 231 cases. Not a coverage gate here; an anti-drift gate on the qualification window.
- **other**: `.venv/Scripts/python.exe scripts/generate_test_inventory.py` plus `--check`; `npx tsc --noEmit`; manual runtime smoke; the §v1.9 mutation matrix run in both directions. **Not** `/build-css`, **not** the `visual.spec.ts` matrix, **not** the pyright baseline diff.

---

## Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a3874ad1fdfb9a3a0` | Author of Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `a3874ad1fdfb9a3a0` | Author of the matrix and Plan v2. Same agent as the row above. |
| `architecture-reviewer` | `a33eb785a2e4fb051` | Step 2 reviewer. Verdict: **Needs revision**. |
| `test-strategist` | `abf41a5af4f327fec` | Step 2 reviewer. Verdict: **Needs revision**. |
| `product-risk-reviewer` | `a9a7673ff3529b17d` | Step 2 reviewer. Verdict: **Needs revision**. |

**Same product-manager resumed for the matrix + Plan v2?** `yes` — resumed via `SendMessage` to the Plan v1 agent ID `a3874ad1fdfb9a3a0`.

**Evidence gap**: `none`.

---

## Reviewer findings

*Nothing below is summarized, reordered or edited. The **only** normalization applied is heading level: each reviewer's own `##`/`###` headings are demoted by two levels so they nest under the `###` subsection headings this template requires, instead of splitting the document at top level. No word, anchor, verdict or code fence was changed.*

### architecture-reviewer (agent `a33eb785a2e4fb051`)

#### architecture-reviewer — Plan v1 findings

Reviewed `## Plan v1` (§v1.0–§v1.13) against the substrate in `D:\development\ht-wt-u1-gate1` at `b4d6b13`. Section 0 was read as binding context only.

**Anchor audit first, because the plan asks to be checked on it.** I spot-checked every load-bearing anchor Plan v1 cites and all but one are exact: `volume-splitter.js:111-139`, `:131`, `:136-137`, `:178-185`/`:184`, `:187`/`:213`, `:511`/`:528`/`:533`, `:537`/`:545`, `:619-634`/`:627`/`:633`, `:694-700`, `:718-745`, `:748-761`, `:863-868`/`:867`, `:870-899` (all six rows of §v1.4's table land exactly: `:876`, `:877`, `:879-881`, `:883-885`, `:887-888`, `:889-897`); `toast.js:33`, `:60-63`, `:65-85`, `:74`, `:101-109`; `fetch-wrapper.js:140`, `:200-217`, `:212-214`, `:244-247`; `base.html:235-251`; `volume_splitter.html:61`, `:83`, `:85`, and the `AGENT:START B-5 PRIORITY-CLASSES` marker opening at `:87` and closing at `:143` — so `panel.prepend()` does land outside the marked block, as §v1.2(D) claims; `ci.yml:363`; `tests/test_playwright_shard_launcher_contracts.py:67` (`== 25`); `fixtures.ts:29-44`, `:71-75`, `:326`; `QUALITY_GATE.md` rows 30, 33, 37, 51, 60, 126, 129. The one wrong anchor is F8 below.

**Charter items that are not engaged, recorded so the record is complete.** No Python file is touched, so the `routes → utils` boundary is not crossed and nothing new imports across it; there is no blueprint, so no registration triple; no table, so no creator/fixture wiring; no `DatabaseHandler` use; no normalization surface; no logger surface; no `utils/__init__.py` re-export. I verified the response contract the plan says it reads rather than trusting it: `routes/volume_splitter.py:104-108` returns `jsonify(success_response(data={...}))` and `:61`/`:111` return `error_response('INTERNAL_ERROR', 'Failed to calculate volume', 500)`, with no HTTP-200-with-`ok:false` path — so §v1.0's account of the server contract is accurate and the arm payloads in §v1.8 are shaped correctly. Shared-state (charter item 8) is handled: the plan touches none of `app.py`, `CLAUDE.md`, `.claude/settings.json`, `MASTER_HANDOVER.md` or `.gitignore`, and it declines `ci.yml` with a stated reason.

**Two things the plan gets right that I want on the record before the findings.** First, `clearResults()` is reused, not wrapped and not duplicated: §v1.4's claim that it already covers exactly criterion 3's enumerated surface is true line-for-line, and no fifth clearing helper is introduced. There is no second source of truth for clearing. Second, the failure state is stored **only in the DOM** (`document.getElementById(CALCULATE_ERROR_ID)` as the `standing` probe) rather than in a module-level boolean. That is the right call and it is what lets one logical region hold across all five existing call sites without a flag that can desync from what the user sees. Keep both in v2.

---

**BLOCKING**

`§v1.2 (B)` + `§v1.3` (state table) — the failure state machine is keyed on **response arrival order**, not request order, and the substrate guarantees concurrent in-flight calculations.

  Risk: `attachSliderListeners()` binds `input` → `scheduleCalculate()` (`static/js/modules/volume-splitter.js:627`) **and** `change` → `calculateVolume()` (`:633`), and `scheduleCalculate()` (`:863-868`) clears only its own prior timer — nothing in `calculateVolume()` cancels a pending debounce. Every drag release therefore issues two POSTs: the immediate `change` one and the debounced one 300 ms later. The e2e harness does the same (`e2e/volume-splitter.spec.ts:25-30` dispatches both events). Today that race is benign, because a failure does nothing. Plan v1 makes it destructive in both directions: a slow failure resolving *after* a fast success calls `enterCalculateFailureState()` → `clearResults()`, wiping freshly painted valid results and raising a failure banner although the newest calculation succeeded; symmetrically, a stale success resolving after a newer failure calls `exitCalculateFailureState()` and paints stale numbers with no failure signal at all. Both are precisely the "displayed inputs and displayed outputs no longer correspond" defect §0.1 measured and U1 exists to remove, and the first one contradicts criterion 8 and transition T7. §v1.3 enumerates eight transitions and none of them is "a second calculation is in flight", so the "one logical state across five call sites" claim is not established by the plan as written.

  Fix: add a module-level `let calculateRequestSeq = 0;` (a fifth private symbol — name it in §v1.2(A) and in §v1.12's containment paragraph), capture `const seq = ++calculateRequestSeq;` as the first statement of `calculateVolume()`, and open all three tails — the success `.then`, the inner `catch`, and the outer `.catch` — with `if (seq !== calculateRequestSeq) { return; }`; this changes no payload, no debounce interval and no call sequence, so criterion 9 still holds by construction, and it needs one mutation row (delete the guard) plus an arm that drives a slow 500 and a fast 200 out of order.

---

**NON-BLOCKING**

`§v1.11` step 5 + `Expected gates` — `e2e/empty-states.spec.ts` is routed but not run.

  Risk: `e2e/empty-states.spec.ts:284-331` is a `test.describe('Empty Volume Splitter')` that clicks Calculate and waits on a `POST /api/calculate_volume` (`:296-306`), clicks Reset (`:309-319` — the function OD-3 modifies), and calls `consoleErrors.assertNoErrors()` in `afterEach` (`:291-293`). `QUALITY_GATE.md:129` routes "empty state" changes to it, and criterion 7 is literally an empty-state criterion. It is absent from §v1.11, from Expected gates, and from `s4`'s inherited-guard list, so a regression in the Reset path or new console noise on the success path would be caught only in CI.

  Fix: add `e2e/empty-states.spec.ts` to §v1.11 step 5 and to Expected gates, and name it alongside `volume-splitter.spec.ts` in `s4` as a second inherited console-error guard.

`§v1.4` (two surfaces deliberately outside the stale set) — the post-2xx failure class leaves `applyServerRanges()` residue that the stated justification does not cover.

  Risk: `handleCalculateResponse()` calls `applyServerRanges(normalizedRanges)` at `static/js/modules/volume-splitter.js:751`, **before** `displayResults()` at `:755`. `applyServerRanges()` mutates `modeRangeState[currentMode]` (`:743`) and repaints every slider track (`:744`). On arm b1's path the throw happens after that, so the inner `catch`'s `clearResults()` leaves the module's range state and all slider track paint derived from a response that was never rendered and was declared a failure. §v1.4 rules the track out of the stale set by citing criterion 8's "server-supplied ranges and slider track paint" — but criterion 8 governs the *success* path and says nothing about a partially applied failed response, so the justification does not reach the b1 case.

  Fix: state the disposition explicitly in v2 — accepting the residue is defensible (a recommended range is a property of muscle and mode, and re-deriving it would need a snapshot/restore that is more moving state than the packet wants) — and pin whichever way it goes with an assertion in `b1`, rather than leaving §v1.4's reasoning to be read as if it covered this path. Do not "fix" it by moving the `applyServerRanges()` call after `displayResults()`; that reorders the success path and would need fresh criterion-8 scrutiny.

`§v1.2 (C)` and `(F)` — KI-011 is live, U1 becomes its second caller, and Plan v1 never mentions it.

  Risk: `docs/UI_SCENARIOS_GAP_ANALYSIS.md:106` records KI-011 as **Open, not mitigated**: any later `showToast()` from anywhere destroys a still-live action button, because `toast.js:60` clears `toastBody.innerHTML` and `:84` appends the button into that same node; the row names `volume-splitter.js:299-306` as the *sole* caller today. U1 makes the packet's own Retry the second one. It is reachable on U1's own page in exactly the scenario criterion 6 describes: during a sustained server fault the history refresh fails and raises `showToast('error', 'Failed to load saved volume plans. Please try again.')` (`:439`), which clears the body and takes the Retry button with it. The contract still survives — the inline region carries a durable Retry, which is a real argument *for* Q2's two-surface answer — but two consequences are unstated. (a) After the failure toast has been destroyed by an unrelated one, `enterCalculateFailureState()` keys its toast decision off the *region's* presence (`announce || !standing`), so a subsequent debounced failure re-announces nothing and the only visible toast reads "Failed to load saved volume plans" while what actually failed was the calculation. (b) `dismissCalculateFailureToast()` probing inside `#liveToast` rather than inside `#toast-body` is what keeps it working across the relocation a KI-011 fix would require — the row notes `toast.test.js` B30–B35 are deliberately placement-neutral *within* `#liveToast` for that reason — but §v1.2(F) gives no reason for the scoping, so an implementer or a later reviewer may "tighten" it to `#toast-body` and silently couple U1 to the open defect.

  Fix: add a short paragraph to §v1.2 naming KI-011, recording that the inline region is the durable retry path and that toast-button loss is accepted, recording that the `#liveToast` scoping in `(F)` is deliberate and must not be narrowed to `#toast-body`, and — if OD-2 is decided the strict way — extending the announce condition so a debounced failure also re-announces when our toast is no longer the live one.

`§v1.9` + `§v1.10 s3` — `dismissCalculateFailureToast()` is the one new helper no mutation kills, and its only assertion can pass without it.

  Risk: M1–M6 cover the two catches, `clearResults()`, focus, `remove()`-vs-`d-none`, and the early-return guard; nothing targets the dismiss helper. Its only oracle is `s3`, which is time-dependent: `showToast`'s default duration is 3000 ms (`static/js/modules/toast.js:33`), so if the success in `s2`/`s3` lands more than three seconds after the failure the toast has already auto-dismissed and `s3` is green whether or not the helper ever ran. The helper is also the one piece of U1 that reaches across a module boundary into a shared singleton's Bootstrap instance and into `toast.js`'s private rendering — `aria-label` is only set when `action.ariaLabel` is supplied (`toast.js:70-72`), so a change there disables the guard silently.

  Fix: add M7 — break the helper's probe (change the `aria-label` it looks for) and require `s3` **red**; make `s3` deterministic by asserting inside the three-second window rather than relying on auto-dismiss; and add to `c1` an assertion that `#liveToast button[aria-label="Retry volume calculation"]` exists, so the exact selector the helper depends on is pinned by a test rather than by prose.

`§v1.10 s3` — Q5-strict is asserted strictly for the region and loosely for the toast, and the plan does not say why.

  Risk: `bootstrap.Toast.hide()` does not clear `#toast-body`, so after `dismissCalculateFailureToast()` runs — and after any auto-dismiss — the Retry button and its live click handler remain in the DOM past a successful calculation. That is a failure-only affordance surviving a success, which is the shape Q5-strict rules out and which M5 exists to forbid for the region. `s3`'s "or is not visible" clause is exactly the weaker reading Q5 rejected, and it is currently the only thing that makes the assertion satisfiable.

  Fix: split `s3` into two separately justified assertions rather than an "or": (1) `#volume-calculate-error` is absent from the DOM — the strict property, U1's own artifact; (2) `#liveToast` is not visible — with a one-line note that clearing `#toast-body` would require editing `toast.js`, which Section 0 puts out of scope, and that the residual node is inert because the compiled bundle carries `.toast:not(.show){display:none}` (`static/css/bootstrap.custom.min.css`), which is also why `s5`'s pinned axe node counts cannot move.

`§v1.8` arm `b1` — the throw line is misdescribed by three lines.

  Risk: the plan says the fabricated `{"results": {"Chest": null}}` payload makes `displayResults()` reach `data.weekly_sets` at `static/js/modules/volume-splitter.js:161`. The first null dereference is one statement earlier, at `:158` — `const statusLabel = (data.status || 'optimal');`. The arm still throws inside the response handler and still works, but the cited anchor is wrong and a later reader re-deriving the arm from it will not find what the plan describes.

  Fix: cite `:158` and `data.status` in `b1`.

`Artifacts` table — `docs/UI_SCENARIOS_GAP_ANALYSIS.md` is the registry this repair is supposed to land in and it is not listed.

  Risk: that document's own usage instruction (`:108-111`) is "when a new bug is reported, add a row (assign next `KI-NNN`) and link to the regression test that locks the fix… when closing a row, change *Status* to `Mitigated` + link the test". U1 repairs a measured user-facing defect and lands three arms that lock it, and there is no row — I grepped: the only volume-splitter reference in that file is KI-011 itself. The registry stays silently incomplete.

  Fix: add `KI-012` marked Mitigated with links to `a1`, `a2` and `b1`, and add the file to the Artifacts table and to §v1.12's blast-radius list; `QUALITY_GATE.md:37` requires no extra gate for it, and editing an existing `docs/*.md` moves no inventory node.

`§v1.0` / `OD-4` — the plan's reading is right, and there is a stronger substrate argument for it than the one given.

  Risk: none if OD-4 is decided as recommended; recording this so the owner has the full basis. Beyond "the wrapper's toast cannot carry a Retry action" — which I confirmed, `fetch-wrapper.js:212-214` passes only `{ requestId }` and has no `action` parameter — the literal reading also breaks criterion 6 directly: with `showErrorToast: true`, a request failure fires the wrapper's toast at `:213` **and then** throws into the plan's outer `.catch`, which fires a second toast. Two notifications per failure is not "one logical failure state". And the literal reading cannot serve criterion 12 at all, because the flag is not consulted on the post-2xx path — the wrapper has already returned by then.

  Fix: add those two sentences to OD-4's recommendation so the owner is not choosing between a design argument and a contract argument.

---

**NIT**

`§v1.8` / `Artifacts` — new e2e selectors bypass the `SELECTORS` registry.

  Risk: `e2e/fixtures.ts` already carries this page's controls (`:186-188`) and the toast (`:157-158`), and the arms would use `#volume-calculate-error` and `[data-testid="volume-calculate-retry"]` as raw strings. If the implementer follows the registry convention instead, `e2e/fixtures.ts` becomes a fifth changed path and §v1.12's "`git diff --stat` shows exactly the four paths above" check reds on a correct change.

  Fix: pick one and say so — either register the two selectors and add `e2e/fixtures.ts` to the Artifacts table and the blast-radius list, or state that raw selectors are deliberate for a single-spec block.

`§v1.11` step 1 — the inventory justification names one pinned surface where the change moves two.

  Risk: `QUALITY_GATE.md:61` pins `waitForTimeout` lines per file as well as per-spec Playwright counts, and `e2e/volume-splitter.spec.ts` already carries 23 hard waits; arms `a3` and `c2` both need to space events past the 300 ms debounce and will likely add more. The regeneration step covers it either way, so nothing breaks — but the stated reason ("Playwright per-spec counts move") is incomplete, and a reviewer checking the artifact diff against the reason will find an unexplained delta.

  Fix: name both pinned surfaces in step 1, and prefer web-first assertions over new `waitForTimeout` lines where the arm allows it.

---

**Verdict: Needs revision** — one blocking finding (the missing request-generation guard, which lets a stale failure clear a successful calculation's results), plus one routing gap and six accuracy/completeness corrections that are cheap to absorb into Plan v2.

### test-strategist (agent `abf41a5af4f327fec`)

Reviewed cold against the code at `origin/main` = `b4d6b1337bf730aa675e7126b7713237931ba60c` in the worktree `D:\development\ht-wt-u1-gate1`. Every pin, line anchor and workflow claim below was opened and read; nothing is taken from the plan's account. Paths are repo-relative to that worktree root.

---

#### Required gates

The union I derive from the changed paths, which is **not** the set in §v1.11:

- **pytest**: full suite (`.venv/Scripts/python.exe -m pytest tests/ -q`). Named specifically, because these three read the two files U1 changes and nothing in QUALITY_GATE's derivation table routes `static/js/**` or `e2e/**` to pytest:
  - `tests/test_volume_history_busy_signal_contracts.py` — **will red as written**, see F1
  - `tests/test_css_cascade_contracts.py::test_volume_splitter_tokens_preserve_runtime_ownership_and_dark_winners` — pins four literal substrings of `volume-splitter.js` at `:500-503`
  - `tests/test_playwright_shard_launcher_contracts.py::test_required_set_is_the_expected_size` — `== 25` at `:65-67`, verified intact
- **e2e**: `e2e/volume-splitter.spec.ts` (whole spec), `e2e/volume-progress.spec.ts`, `e2e/error-handling.spec.ts`, `e2e/accessibility.spec.ts`, **plus `e2e/validation-boundary.spec.ts` and `e2e/empty-states.spec.ts`** (F3)
- **js-unit**: `npm run test:js`, asserted unchanged at 13 files / 231 cases — anti-drift, not coverage. Verified: exactly 13 files exist under `static/js/modules/__tests__/`
- **other**: `scripts/generate_test_inventory.py` + `--check`; `npx tsc --noEmit`; **`scripts/pyright_baseline_diff.py`** once F1 forces a `.py` into the diff; manual runtime smoke; the §v1.9 mutation matrix in both directions
- **Not required, correctly excluded**: `/build-css`, the `visual.spec.ts` matrix. `.alert-danger` is present in both `static/css/bootstrap.custom.min.css` and `static/css/components.css`, so no new rule is needed and no rest-state paint moves. The exclusion holds only while no `scss/**` rule is written for `volume-calculate-error` (N2)

**Known-red awareness**: the only documented exception is `e2e/program-backup.spec.ts:79`. It is outside U1's run set and outside the CI required functional list. **No known-red applies to this change** — every red in U1's gate set should be treated as real.

**Conftest / fixture work**: none. No blueprint, no table, no `tests/conftest.py` impact. `e2e/fixtures.ts` needs no change either — see F7, the posture it needs is achievable with the existing `ConsoleErrorCollector.errors` field.

---

#### Findings

##### F1 — BLOCKING. The plan collides with an exact-count pin on the spec file it edits, and does not know it.

`tests/test_volume_history_busy_signal_contracts.py:107-112`:

```python
def test_volume_splitter_spec_is_exactly_converted() -> None:
    spec = read(SPEC)
    assert "waitForVolumeSplitterReady" in spec
    assert spec.count("await waitForVolumeSplitterReady(page);") == 3
    assert "waitForPageReady" not in spec
    assert "networkidle" not in spec
```

The count is live and exact: `await waitForVolumeSplitterReady(page);` occurs at `e2e/volume-splitter.spec.ts:45`, `:616` and `:670` (the occurrence at `:586` is un-`await`ed and does not match). §v1.8 appends a new `test.describe` whose `beforeEach` must navigate and wait for readiness. Using the helper makes it **4** and reds this test; the two other legal waits are explicitly forbidden by the same function.

Consequences the plan must absorb:

- `tests/test_volume_history_busy_signal_contracts.py` joins the artifacts table, with the pin bumped `3 → 4`. That is a contract-test edit and QUALITY_GATE's `static/css/**` row states the standing rule for contract tests — explicitly scoped, justified, and not weakening an existing guarantee. `3 → 4` does not weaken it, but it must be declared in the plan and in the PR body rather than discovered at step 6.
- It puts a `.py` file in the diff. §v1.11's *"Not run, and why: `scripts/pyright_baseline_diff.py` — no `.py` changes"* becomes false. Add it.
- §v1.12's blast-radius check *"`git diff --stat` shows exactly the four paths"* becomes five.

This is also the strongest argument for running full pytest, and it is a better argument than the one §v1.11 gives. Nothing in QUALITY_GATE's Targeted-test derivation routes `e2e/**` or `static/js/**` to any pytest target; full pytest is the **only** thing that catches this. Say that, rather than *"the suite is cheap enough that narrowing buys nothing."*

##### F2 — BLOCKING. `s3` is an oracle that cannot fail, and helper (F) has no mutation.

`toast.js:33` defaults `duration` to 3000 ms and `toast.js:108` constructs `new bootstrap.Toast(el, { delay: duration })`. `playwright.config.ts:191-193` sets the global `expect` timeout to **10000 ms**. `s3` asserts *"`#liveToast` no longer contains `button[aria-label="Retry volume calculation"]`, **or** is not visible."*

Both disjuncts fail to discriminate:

- The first is **false under the plan's own implementation**. `dismissCalculateFailureToast()` calls `bootstrap.Toast.getInstance(el)?.hide()` and nothing else. `hide()` does not touch `#toast-body`; `showToast` only clears it at `toast.js:60` on the *next* call. The Retry button therefore stays in the DOM after a successful dismiss.
- The second is satisfied by the 3 s auto-dismiss with a 10 s retry budget, **whether or not `dismissCalculateFailureToast()` is ever called**.

So `s3` passes if helper (F) is deleted outright. And §v1.9 contains no mutation targeting (F) — M1–M6 leave it untouched. The entire justification for adding (F) (§v1.2 F: closing the window where an error toast overlaps fresh results) rests on an assertion that cannot detect its absence.

Two changes, both needed:

1. Make the assertion time-bounded and positive. After `page.unroute` + Calculate, assert `page.locator('#liveToast button[aria-label="Retry volume calculation"]')` `.toBeHidden({ timeout: 1000 })` measured from the click, and separately assert the *success* path completed (results visible). Bootstrap's `hide()` transition is ~150 ms; the un-dismissed toast is still visible for the remainder of its 3 s. A 1 s bound discriminates.
2. Add **M7** to §v1.9: delete the `dismissCalculateFailureToast()` call from `exitCalculateFailureState()`; `s3` must red.

Consider also making (F) clear `#toast-body` after `hide()`, which turns the first disjunct into a real, timing-independent oracle. That stays inside the "reach into `#liveToast` with public APIs" posture (F) already adopts and still requires no change to `toast.js`.

##### F3 — BLOCKING. The §v1.11 gate set is not the correct union — one QUALITY_GATE row is taken at half strength.

`QUALITY_GATE.md:129` reads:

| validation, error, empty state, accessibility changes | `validation-boundary.spec.ts`, `error-handling.spec.ts`, `empty-states.spec.ts`, `accessibility.spec.ts` |

§v1.11 takes `error-handling.spec.ts` and `accessibility.spec.ts` and silently drops the other two. U1 is squarely an **error-surface** change *and* an **empty-state** change — criterion 7 is literally about what the empty results and suggestions sections do on failure, and Q1's clearing decision returns the page to the empty state on every failure. Both dropped specs sit in CI's required functional list (`ci.yml:360` and `:346`), so CI would catch a regression, but the plan's local gate under-runs the derived union and QUALITY_GATE's standing instruction is *"Run the union, never the weaker set."*

Add `e2e/validation-boundary.spec.ts` and `e2e/empty-states.spec.ts` to §v1.11 step 5 and to the Expected gates block.

Everything else in §v1.11's derivation checks out. Both blocking CI gates the change-type table does not derive **are** covered — `Test Inventory Drift` at step 1 and the `tsc --noEmit` half of `Type Check` at step 3 — and the pyright half was correctly excluded on the (now falsified, see F1) premise that no `.py` moves.

##### F4 — BLOCKING. Criterion 7 has no arm and no mutation.

Owner-signed criterion 7 and §v1.3's **T1** state the first-load failure case: feedback is shown even when no calculation has ever succeeded, and the empty sections stay hidden. §v1.8 and §v1.10 contain no test for it. `a1` and `a2` both establish a prior success by design; `b1` as written does not, but asserts nothing about first-load specifically.

§v1.3 argues T1 is *"carried by the same call that carries criterion 3, with no special case."* That is an argument about the current draft's shape, not an oracle. An implementer who guarded the failure state behind "a previous success exists on this page load" — a plausible reading of "stale results" — ships green against every arm in §v1.8.

Add `a4`: fresh page load, install the 500 route, click Calculate with no prior success. Assert `#volume-calculate-error` visible and count 1, `expectToast`, and — the criterion-7 half — `.results-section` and `.ai-suggestions-section` **still carry `d-none`** and `#results-body tr` count 0. Cheap, and it is the only place the "shown anyway, but the empty sections are still not revealed" pair is measured.

##### F5 — BLOCKING. OD-2's dedup behavior is unmeasured; nothing in §v1.9 can kill the `announce || !standing` guard.

§v1.5 and §v1.3 T6 promise that during a sustained fault the debounced path produces **no repeat toast**. §v1.8's `a3` measures only the *region*'s survival, via the `data-probe` stamp — good design, and **M6** genuinely discriminates it. But the toast half of criterion 6 has no arm.

§v1.5's defence is that stacking is structurally impossible: one `#liveToast`, body cleared at `toast.js:60-63`, instance disposed and reconstructed at `:101-109`. I verified that and it is correct — which is precisely the problem. *That* half of criterion 6 cannot fail and is not evidence of anything U1 does. The half that **can** fail is the plan's own OD-2 choice, and if an implementer wrote an unconditional `showToast(...)` in `enterCalculateFailureState()`, every arm in §v1.8 and §v1.10 would still be green while the page assertively re-announced roughly three times a second during a drag — the exact behavior OD-2 says it is avoiding.

Add an arm and a mutation:

- `a6`: with the 500 route standing, focus a slider and drive debounced failures continuously for longer than the toast's 3000 ms life, waiting on `page.waitForResponse('**/api/calculate_volume')` between dispatches. Assert `#volume-calculate-error` stays present *and* `#liveToast` becomes hidden and stays hidden while failures continue. Under an unconditional toast the element re-shows and the assertion reds.
- **M8**: replace `if (announce || !standing)` with an unconditional `showToast(...)`; `a6` must red.

This also gives OD-2 something to be decided *against*. As drafted, the council is asked to ratify a behavior no test would notice being removed.

##### F6 — NON-BLOCKING. `b1` is run in a state where half its assertions cannot fail.

Verified the injection works: `handleCalculateResponse` (`:748-761`) calls `applyServerRanges({})` — a no-op on an empty map — then `displayResults({ Chest: null })`, which reaches `${data.weekly_sets}` at `:161` and throws a `TypeError` inside the response handler. The inner `catch` is genuinely the only thing that can see it. Arm (b) is well-founded and M1/M2 do isolate correctly (see the verdict below).

But §v1.8 specifies `b1` with no prior successful calculation. `displayResults` clears `tbody` at `:147` before it throws, and the two sections start the page load with `d-none` from the template (`volume_splitter.html:85`, `:114`). So `b1`'s *"same assertions as `a1`"* — `#results-body tr` count 0, both sections hidden, no `status-*` class, no `volume-value-pill--*` modifier — are **all trivially true before the request is even sent**. Only the region and toast assertions carry `b1`.

Fix: give `b1` a clean successful calculation first, then install the 200-poison route and click Calculate again. Same shape as `a1`. The clearing assertions then become real, and `b1` gains an M3-style kill it currently lacks.

##### F7 — NON-BLOCKING. Dropping the `consoleErrors` fixture removes the only oracle for the one edge §v1.2 admits it cannot defend.

The plan's reasoning for scoping the fixture out is sound as far as it goes — I confirmed the allow-list at `e2e/fixtures.ts:29-44` filters the wrapper's `API Error` and `API Error (final)` logs (`fetch-wrapper.js:204`, `:238`) but would not filter a page-specific `Error calculating volume:`. However, `assertNoErrors()` is not the only available posture. `ConsoleErrorCollector` exposes `errors: string[]` publicly (`fixtures.ts:10`, `:22-24`), so the new block can keep the fixture and assert an allow-one set inline:

```ts
test.afterEach(async ({ consoleErrors }) => {
  for (const e of consoleErrors.errors) {
    expect(e, 'unexpected console/page error on the failure path').toContain('Error calculating volume:');
  }
});
```

This matters because of §v1.2's **second edge**, which the plan flags and declines to defend: if `enterCalculateFailureState()` throws inside the inner `catch`, the rejection reaches the outer `.catch` and the treatment runs twice. Under the current posture that path produces console noise nothing observes. With the allow-one assertion it reds.

Related accuracy point: the plan says the new block *"does not use the `consoleErrors` fixture … pointing at `error-handling.spec.ts:62-64`, which takes exactly the same route."* It does not. `error-handling.spec.ts:56-64` **does** take the fixture and **does** call `startCollecting()`; it simply has an empty `afterEach`. That is a weaker posture than the plan's, not the same one, and the in-file comment as drafted would misdescribe its own precedent.

##### F8 — NON-BLOCKING. Criterion 4 (mode-switch / load-plan failure) has no arm.

§0.1 measured T3/T4 as a **distinct** divergence from T2 — the previous mode's results and suggestions sitting under a freshly rendered slider set — and said explicitly that *"a contract that only addresses one of them leaves the other live."* Criterion 4 was written for it. §v1.8 exercises the Calculate-button path (`a1`, `a2`, `b1`) and the debounced slider path (`a3`, `c2`), and never `setMode()` → `calculateVolume()` at `:533` or `loadPlan()` at `:213`.

The paths converge on one `enterCalculateFailureState()`, so `a1` is a defensible proxy and I would not block on this. But `setMode()` is the one entry point where `renderSliders()` has already rebuilt every `.muscle-row` before the request goes out, so a mode-conditional clearing mistake is exactly the defect this arm would catch and no other would. Add `a5`: calculate successfully in basic mode, install the 500 route, switch to advanced, assert the region appears **and** `#results-body tr` count 0 with `.results-section` hidden — i.e. the previous mode's table is gone.

Note that the existing test at `e2e/volume-splitter.spec.ts:354-366` already exercises the `loadPlan()` → `calculateVolume()` **success** path and asserts a recomputed value, and it lives in the block that keeps `assertNoErrors()`. That is a genuine inherited guard for T4's success side and is worth citing in `s4`.

##### F9 — NON-BLOCKING. Toast-assertion ordering is a live flake source in `a1` and `c1`.

The toast's life is 3000 ms (`toast.js:33`). `expectToast` (`fixtures.ts:326-331`) waits up to 5000 ms for visibility and then asserts text with the 10 s global budget — it will pass on a *visible* toast only. §v1.8 lists `expectToast(page, /calculate/i)` as `a1`'s **second** assertion, after `#volume-calculate-error` visibility and count. `c1` likewise front-loads `#liveToast` attribute reads.

On a slow CI runner the preceding locator resolutions can consume the toast's 3 s window, and the failure looks like a product defect. Specify the order: **assert the toast first**, then the region, then the clearing assertions. Same for `c1` — read `role`/`aria-live`/`#toast-body` text in one pass immediately after the failure is driven.

##### F10 — NON-BLOCKING. `s6` is an inspection, not a test, and its behavioral half is overstated.

`s6` sits in a table headed "Success-path invariants" alongside `s1`–`s3`, which are real Playwright tests. `s6` is *"`git diff` must show no change at …"* — a human eyeball. That is a fine blast-radius check but it should be moved out of the arm table so the evidence classes are not conflated.

Its behavioral half — *"the save-plan and history paths are already exercised by the existing tests at `:289-386`"* — is right for site 4 (save, `:337`), site 2 (load plan, `:360`) and site 3 (delete, `:377`). It is **not** true for site 6, activate/deactivate (`volume-splitter.js:828`), or for site 5's error row (`:372`); I found no test exercising either. Criterion 10 rests on the `git diff` check alone for those two. State that rather than implying uniform coverage.

##### F11 — NON-BLOCKING. §v1.1's reading of the restart clause is correct, under-cited, and if anything too generous to option (ii).

I checked this directly. §6.5's ratified text (`STEP12_JS_UNIT_GATE0.md:846-847`) ties the restart to *"the first successful `JS Unit (Vitest, non-required)` run on `main` after the final expansion packet lands"* and names only two clock events — the expansion packets and a `js-unit` failure. Read alone, that text does **not** say "any suite change restarts", and §v1.1's opening sentence — *"Owner ruling Q2 restarts that window when the suite the `JS Unit` job runs changes"* — is not a quotation of it.

But the document's own operating practice is unambiguous and repeated, and it is what the plan should cite:

- `:74-77` — *"Packet F changed no JS test case, so Q2's restart clause never engaged"*
- `:100-101` — *"PR #412 was documentation-only and changed no JS test case"*
- `:129-131` — *"#413 changed no JS test case, so Q2's restart clause did not engage"*

Three consecutive reconciliations state the operative test as **"changed no JS test case."** The §6.5 carve-out at `:858-859` — Packet F *"is a separate required predecessor and may land inside the window; it does not restart it"* — only makes sense if something other than the A/B/C packets could otherwise restart it. So the plan's reading is not merely defensible, it is the record's settled reading, and U1 is confirmed not to be a named predecessor.

The consequence runs the other way from how the plan states it. Option (ii)'s *"the window arguably restarts … whether 'arguably' becomes 'certainly' is itself an owner call"* **understates** the cost. On the document's own three-times-applied rule, adding `static/js/modules/__tests__/volume-splitter.test.js` restarts the window — not arguably. Recommend rewriting §v1.1's lead sentence to quote the operative practice with those three anchors, and hardening option (ii)'s cost line accordingly.

With that correction, **the recommendation of (i) with (iii) as a named follow-up is the right call**, and the reasoning given for it is the right reasoning: all three Gate 0 arms are DOM-and-announcement failure behaviors — a live-region announcement, `document.activeElement` under a real focus model, a Bootstrap toast lifecycle — that jsdom approximates rather than measures. Costs are stated honestly. One thing option (iii) needs and does not have: a named home for the tracked obligation. "Needs a tracked owner obligation or it will be forgotten" is true and unactioned. Name the file it lands in.

Independently: §v1.11 step 2's affirmative check (`npm run test:js` must print 13 files / 231 cases) is the right instrument, and it doubles as the collection-failure guard `QUALITY_GATE.md:60` calls for. Verified 13 test files exist under `static/js/modules/__tests__/`.

##### F12 — NON-BLOCKING. The accessibility arm is real evidence; the failure surface has no automated a11y oracle at all, and the plan should say so.

On the Gate 0 question directly: **arm (c) is not resting on inherited markup.** `c1`'s third assertion — the failure message text lands in `#toast-body` while the toast is visible — is a behavior assertion, and it is the load-bearing one. The attribute assertions do re-read `base.html:236-248` (verified: container `aria-live="polite"` `aria-atomic="true"` `data-testid="toast-container"`; `#liveToast` `role="alert"` `aria-live="assertive"` `aria-atomic="true"`), but they are there as a guard against the markup being changed out from under the announcement, not as the proof. `c2` is stronger still: a `document.activeElement` read-back mid-drag is exactly the property criterion 2 names, it is killed by **M4**, and I confirmed the only pre-existing `.focus()` in the module is `summary?.focus()` at `:312`, off the calculate path. This satisfies the Gate 0 evidence standard.

`s5`'s reasoning is also correct and I verified both pins: `e2e/accessibility.spec.ts:834` `'volume_splitter:light': [{ rule: 'color-contrast', nodes: 2 }]` and `:839` `'volume_splitter:dark': [{ rule: 'color-contrast', nodes: 2 }]`. Because Q5 strict makes the region absent from the DOM in every non-failure state, the axe scan sees exactly today's document and the pins hold untouched. Running the spec rather than editing it is right, and declining to add the failure state to the axe matrix is a defensible trade.

What the plan should state rather than leave implicit: that trade means **no automated accessibility oracle covers the failure surface in either theme**. `static/css/theme-dark.css` contains zero `.alert` rules, so the region renders with stock Bootstrap `alert-danger` on a dark page. Stock `alert-danger` sets its own background and foreground, so I do not expect a contrast violation — but nothing measures it, and the region is a new light-on-dark block in a themed UI. Add one line to §v1.11 step 7: during manual smoke, run a one-off axe scan (or a devtools contrast read) against the failure state in both themes and record the reading in the PR body as one-time evidence. It costs nothing and it closes the only a11y hole the plan creates.

##### N1 — NIT. `data-testid="volume-calculate-error"` duplicates `CALCULATE_ERROR_ID` as a bare literal in §v1.2 (D). Derive it (`region.dataset.testid = CALCULATE_ERROR_ID`) so the id and the test hook cannot drift.

##### N2 — NIT. `volume-calculate-error` is a class with no rule in any stylesheet. As drafted it is a dead class doing the work `data-testid` already does. Either drop it or keep it explicitly as a JS-only hook — and record that giving it an SCSS rule later escalates the gate to `/build-css` plus the `visual.spec.ts` matrix under `QUALITY_GATE.md:31`, which is precisely the escalation §v1.0 congratulates itself on avoiding.

##### N3 — NIT. §v1.11 step 1 names only *"Playwright per-spec counts"* as the inventory trip. The artifact also pins **`waitForTimeout` lines per file** (`QUALITY_GATE.md:61`; the committed artifact records 82 across 14 files at `docs/test_inventory/TEST_INVENTORY.md:21`). `a3`, `a6` and `c2` all have to cross a 300 ms debounce. Specify that they wait on `page.waitForResponse('**/api/calculate_volume')` per iteration rather than `page.waitForTimeout` — deterministic, and it keeps that pinned surface at zero delta for this file. `route.fulfill` still produces a response event, so the idiom works against the interception.

##### N4 — NIT. §v1.2 (D)'s marker analysis is correct but immaterial. I confirmed `AGENT:START B-5 PRIORITY-CLASSES` opens at `volume_splitter.html:87` and closes at `:143`, and that `panel.prepend()` on the `.volume-insights-panel` aside at `:83` lands the node before `.results-section` at `:85`, outside the block. Since U1 does not edit the template at all, no marker contract can be reached. Keep the placement reasoning, drop the marker paragraph or reduce it to a clause.

---

#### The three regression arms — do they discriminate?

Yes, on the specific question asked. I traced both mutations against the real control flow.

**M1** (delete `enterCalculateFailureState(…)` from the outer `.catch`) restores today's silence for the request-failure class. `a1`'s 500 takes `fetch-wrapper.js:200-217` — `showErrorToast` is false so `:212` is skipped, `:216` throws — and `a2`'s `route.abort('failed')` takes `:223-249`, where `:245`'s `showErrorToast && !(error.code)` is likewise false. Both land in the outer `.catch` and only there. `b1`'s `TypeError` is raised inside `displayResults` under `.then(handleCalculateResponse)`, is caught by the inner `catch`, and `return`s — it never reaches the outer handler. So M1 reds `a1`/`a2`/`a3`/`c1`/`c2` and leaves `b1` green, as predicted.

**M2** (delete it from the inner `catch`) reds `b1` only, because no request-failure path enters the inner `catch` at all.

Neither arm passes for the wrong reason under its own mutation, and the isolation is real in both directions. The §v1.2 justification for the inner `try`/`catch` over one shared `.catch` — that a single handler makes criteria 11 and 12 provable only jointly — is correct and load-bearing, exactly as claimed.

Three qualifications, all covered above: `b1`'s **clearing** assertions cannot fail in the state it runs in (F6); criterion 7 has no arm at all (F4); and the criterion-6 toast half has no arm and no mutation (F5). M3–M6 are well chosen — each targets a specific "the arm might be passing for the wrong reason" hypothesis, and M6's pairing with the `data-probe` stamp is the right instrument for "not replaced," since a bare count of 1 cannot distinguish a surviving node from a rebuilt one. The both-directions discipline and the *"never revert by retyping the line"* rule are right and should be kept verbatim.

---

#### Coverage gaps

- `static/js/modules/volume-splitter.js` (first-load failure, criterion 7) — needs `a4` in `e2e/volume-splitter.spec.ts` covering: failure with no prior success shows region + toast, and `.results-section` / `.ai-suggestions-section` remain `d-none`. **[F4]**
- `static/js/modules/volume-splitter.js` (repeat-toast dedup, criterion 6 / OD-2) — needs `a6` plus mutation **M8**. **[F5]**
- `static/js/modules/volume-splitter.js` (`dismissCalculateFailureToast()`) — needs a time-bounded `s3` plus mutation **M7**. **[F2]**
- `static/js/modules/volume-splitter.js` (mode-switch failure, criterion 4 / T3) — needs `a5`. **[F8]**
- `e2e/volume-splitter.spec.ts` (unexpected console/page errors on the new failure path) — needs the allow-one `afterEach` rather than no fixture. **[F7]**
- `tests/test_volume_history_busy_signal_contracts.py:110` — needs the `3 → 4` bump, scoped and justified in the PR body. **[F1]**

---

#### Verdict

**Full `/verify-suite`-equivalent required**, and the plan already reaches that in substance — but the gate set as written is incomplete on three counts: two required specs are missing from the derived union (F3), the pyright baseline diff is wrongly excluded once F1 forces a `.py` into the diff, and step 6's full-pytest justification is the wrong one for the right conclusion.

The strategy underneath is sound and better than most plans I review here. The suppression-site framing is measured rather than inherited, arms (a) and (b) genuinely discriminate in both directions, M3–M6 exist because the author understood that an arm which cannot be made to fail is not evidence, the accessibility arm clears the Gate 0 bar rather than leaning on `base.html`, the a11y node-count pins are correctly read and correctly protected by Q5 strict, the `consoleErrors` collision was noticed unprompted, and OD-4 surfaces a genuine contract conflict instead of absorbing it. The §v1.1 recommendation is the right call on the right grounds.

**Five blocking items before Gate 1 can sign**: F1 (the spec-count pin, unknown to the plan and fatal to step 6 as drafted), F2 (`s3` cannot fail and helper (F) has no mutation), F3 (under-derived spec union), F4 (criterion 7 uncovered), F5 (criterion 6's toast half uncovered and OD-2 unmeasurable). None of them is a design problem; all five are additions to §v1.8, §v1.9, §v1.11 and the artifacts table.

### product-risk-reviewer (agent `a9a7673ff3529b17d`)

#### product-risk-reviewer — Plan v1 review

Reviewed `docs/volume_failure_feedback/PLANNING.md` at `D:\development\ht-wt-u1-gate1`, checked against `origin/main` = `b4d6b13`. Every code claim below was read in the worktree, not taken from the plan's account of it.

##### What holds up

The plan's substrate claims are accurate where I checked them, and several are load-bearing:

- **Calculation surface is genuinely `none`.** No route, service or `utils/**` file is in scope. `routes/volume_splitter.py`, `utils/volume_splitter_service.py`, `utils/effective_sets.py`, `utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py` and the fatigue modules are all untouched. No volume number, no `low`/`optimal`/`high`/`excessive` classification, no recommended range and no slider track paint moves. `clearResults()` is reused verbatim and computes nothing. The parked fatigue and learned-calibration workstreams are not touched or implied.
- **Stale-output completeness covers both §0.1 divergences.** I read `clearResults()` at `static/js/modules/volume-splitter.js:870-899` line by line. It re-adds `d-none` to `.results-section` (`:876`) and `.ai-suggestions-section` (`:877`), empties `#results-body` (`:879-881`) and `.suggestions-container` (`:883-885`), strips all four `status-*` classes and all four `volume-value-pill--*` modifiers from every `.muscle-row` (`:887-898`). §v1.4's table is correct and the surface set matches criterion 3 exactly. On the mode-switch path it is idempotent against `renderSliders()`' rebuild, so criterion 4 is carried by the same call — the plan is right that no second clearing helper is needed, and right that one call covers both the button/slider divergence and the mode-switch divergence.
- **Local-first / non-goals clean.** Nothing introduces auth, cloud sync, a remote DB, or a telemetry endpoint. Retry is user-initiated only; `retries` stays at the wrapper's POST default of `0`, verified at `fetch-wrapper.js:140`. Nothing auto-adjusts a user input or blocks one — the Calculate button is never disabled today and the plan adds no disable path. Effective sets do not appear on this surface at all, so the informational-only rule is not engaged.
- **Terminology.** No drift. `Retry`, `aria-label="Retry volume calculation"` and "volume calculation" match the page's own vocabulary (`Calculate` button at `templates/volume_splitter.html:61`, "Muscle Volume", "Weekly sets per muscle group"). No canonical term (RIR, RPE, Effective/Raw sets, CountingMode, ContributionMode, Routine, Movement pattern, Superset) is used or rebranded.
- **No workflow disruption, no backup-contract exposure.** The region lives inside the existing Distribute page's `<aside class="volume-insights-panel">`; no navigation, page ownership or DB schema changes.
- **Two claims I expected to fail and did not.** The `AGENT:START B-5 PRIORITY-CLASSES` marker really does open at `templates/volume_splitter.html:87` (inside `.results-section`) and close at `:143`, so `panel.prepend()` against the aside at `:83` lands outside it. And `alert-danger` really is in the shipped bundle (`static/css/bootstrap.custom.min.css`), with `alert alert-danger` already an established in-repo idiom at `progression-plan.js:305`, `muscle-selector.js:293` and `base.html:270` — so "no `scss/**` gate, no visual baseline moves" holds.

Criteria 1, 2, 3, 4, 9, 10 and 12 are satisfied as drafted. Criteria 5, 6, 7, 8 and 11 have gaps, below.

---

##### Findings

**§v1.2 (B)/(C) and §v1.3 T6–T7 — a late-arriving failure destroys a fresh success, and the plan adds no request sequencing**
  Invariant at risk: acceptance criteria 5 and 8; CLAUDE.md §1 "Refactor invariant" (do not silently alter core workflow behavior).
  Risk: `calculateVolume()` has no sequence guard, and the page routinely has two calculate POSTs in flight. At drag release the `input` listener has already armed the 300 ms timer (`:627` → `:867`) and the `change` listener fires `calculateVolume()` immediately (`:633`) — the `change` handler does not clear the pending timer, so a single release issues two POSTs ~300 ms apart. The plan's own T6 depends on this. Today a failed request does nothing, so out-of-order resolution is harmless. Under Plan v1 the failure handler calls `clearResults()`. Sequence: request A (Calculate click or drag-release `change`) hangs and rejects at t=800; request B (the debounced one) succeeds at t=400 and paints correct results while `exitCalculateFailureState()` removes the region; at t=800 A's rejection runs `enterCalculateFailureState()`, wipes B's *successful, current* results and re-raises the failure region. The user is left staring at a failure state produced by a request older than the successful one — a new instance of precisely the "displayed inputs and displayed outputs no longer correspond" defect §0.1 defines U1 to remove, and it surfaces exactly during recovery from the sustained fault criterion 6 targets. The same shape applies to `resetValues()`: reset while a failing request is in flight, and the region reappears over zeroed sliders.
  Fix: add a module-private monotonic request token — capture it at the top of `calculateVolume()`, bump it there and in `resetValues()`, and have both the success tail and both failure handlers return early when their captured token is stale.
  **Blocking.**

**§v1.2 (A) — the mandated message content is false on the first-load path Q6 put in scope**
  Invariant at risk: acceptance criterion 7 / Owner decision Q6; §v1.5's "Update: never" design.
  Risk: `CALCULATE_ERROR_MESSAGE` is specified as one static string that "must say both things the user needs: the calculation failed, **and** the previous results were cleared", and §v1.5 forbids ever rewriting it. On T1 — first calculation of a page load, which Q6 affirmatively assigned to U1 — there are no previous results; `init()` at `:94-97` never calls `calculateVolume()`, and both sections ship `d-none`. The user is told their results were cleared when nothing was on screen. Two messages would resolve it but collide with the single-message design the plan uses to satisfy criterion 6.
  Fix: restate the second required proposition as a description of the *current state* rather than of an event — the message must convey that the calculation failed and that no results are being shown — so one static string is true on both the first-load and post-success paths.
  **Blocking** (must be settled in Plan v1's contract before Plan v2 writes the string).

**§v1.2 (H) / §v1.3 T6 / OD-2 — repeat-toast suppression misses the keyboard slider path**
  Invariant at risk: acceptance criterion 6 / Owner decision Q4.
  Risk: `announceFailure: false` is passed only from `scheduleCalculate()`. Keyboard operation of `input[type=range]` fires `input` **and** `change` on every arrow keypress, so a keyboard user adjusting a slider against a down server routes through the `change` listener at `:633` — `announce` is `true`, and `enterCalculateFailureState()`'s `announce || !standing` condition re-fires an `aria-live="assertive"` toast on every keypress. That is the continuous assertive re-announcement OD-2 says it is avoiding, and it lands on precisely the user for whom it is most hostile. The plan's mid-drag mouse analysis does not cover it.
  Fix: pass `announceFailure: false` from the slider `change` listener at `:633` as well — the `announce || !standing` condition still lets the first failure of an interaction announce, while repeats fall through to the standing region — and record the refinement under OD-2.
  **Non-blocking.**

**§v1.2 (G) / OD-3 — clearing the region on Reset edits a signed criterion and is dispositioned one level too low**
  Invariant at risk: acceptance criterion 6, "the inline region … persists until the next successful calculation".
  Risk: OD-3 removes the region without a successful calculation. I agree with the plan's reasoning on the merits, but criterion 6 is signed text and OD-3 is marked "Blocking? No", which routes it to council disposition. A council cannot narrow a criterion the owner signed.
  Fix: mark OD-3 as owner-decided and record it as a scoped amendment to criterion 6 ("…or until the user resets"), not as a plan-level judgement call.
  **Non-blocking, but re-route to the owner.**

**§v1.0 / §v1.9 M1 / OD-4 — under the recommended reading, `showErrorToast: false` ships with no coverage at all, and no black-box arm can give it any**
  Invariant at risk: acceptance criterion 11; §0.2's closing obligation.
  Risk: OD-4's recommendation rests on "re-adding the flag is not available as a mutation because the flag was never removed." That is true but it understates the consequence. I traced the counterfactual: if a later edit removed `showErrorToast: false` from `:131`, the wrapper fires `showToast('error', errorInfo.message, {requestId})` at `fetch-wrapper.js:213` and then throws; the page's outer `.catch` fires its own `showToast` a microtask later, and `toast.js` clears `#toast-body` (`:60-63`) and disposes/recreates the instance (`:101-109`). The page's toast wins. **There is no user-visible difference, so `a1`, `a2`, `c1` and every other proposed arm stay green.** §0.2's measured finding is that this flag is the single load-bearing cause of user-visible silence, and Plan v1 leaves it as the one shipped surface with zero regression pressure.
  Fix: state that gap explicitly in OD-4 as part of what the owner is accepting, and either (a) accept it on the record, or (b) have `test-strategist` price an arm that observes `#toast-body` transitions (e.g. a `MutationObserver` installed via `addInitScript`) so the flag is pinned. Do not present the recommended reading as coverage-neutral.
  **Non-blocking.**

**§v1.5 "Remove" row / `s3` — the after-success DOM is not as clean as the prose says**
  Invariant at risk: Owner decision Q5 (strict).
  Risk: §v1.5 asserts that after any success "the DOM contains no `#volume-calculate-error` at all" and frames the pair of surfaces as symmetrically removed. But `dismissCalculateFailureToast()` only calls `bootstrap.Toast…hide()`; `toast.js` never clears `#toast-body`, so the failure message span and the `button[aria-label="Retry volume calculation"]` remain in the DOM inside a `display:none` toast after every success. `s3` is written to tolerate this ("…or is not visible"), which means the assertion and the prose disagree. This is pre-existing `toast.js` behavior shared by every toast on every page, so it is not new state U1 introduces — but Q5 was signed *strict* and the plan itself uses "not a hidden shell" as its reason for choosing `.remove()` over `d-none`.
  Fix: say so plainly in §v1.5 — that the toast residue is inherited `toast.js` behavior, out of scope per the shared-contract exclusion, and that Q5 strict is enforced against U1's own element — rather than claiming a clean DOM.
  **Non-blocking.**

**§v1.4 — criterion 8 is cited to justify a failure-path decision, but criterion 8 is success-path-scoped**
  Invariant at risk: acceptance criterion 3's enumeration.
  Risk: the slider-track exclusion is justified partly by "criterion 8 lists 'server-supplied ranges and slider track paint' as state to preserve." Criterion 8 opens "Given a *successful* `POST /api/calculate_volume`" and says nothing about the failure path. The substantive argument — that the track is a property of muscle and mode rather than of the failed calculation's inputs, and that `renderSliders()` → `updateAllSliderTracks()` (`:556`) has already repainted before the request on T3/T4 — is correct on its own and I verified `applyServerRanges()` (`:718-746`) and `updateSliderTrack()` (`:643-656`) behave as described. Leaning on criterion 8 weakens a conclusion that stands without it.
  Fix: re-cite the exclusion to criterion 3's four-surface enumeration plus the muscle/mode-property argument; drop the criterion 8 reference.
  **Nit.**

**§v1.8 arm `b1` — the cited throw site is wrong**
  Risk: the plan says the `{"results": {"Chest": null}}` payload makes `displayResults()` "reach `data.weekly_sets` on a `null` at `:161`". It throws earlier, at `:158`, on `const statusLabel = (data.status || 'optimal')`. The arm still works and still exercises the inner `catch` — only the citation is wrong — but §0.1's whole method is "measured, not inferred", and a wrong anchor invites a later reader to re-derive it.
  Fix: correct the anchor to `:158`.
  **Nit.**

**§v1.5 "Create" row — an inert hidden `.alert alert-danger` already exists and should be named**
  Risk: the plan claims the failure element "does not exist anywhere — not in `templates/volume_splitter.html`, not hidden, not empty". True for `#volume-calculate-error`, but `base.html:268-273` carries `#error-message-container` — a `d-none` + inline-`display:none` `.alert alert-danger` with `role="alert"` and the text "An unexpected error occurred. Please try again later." I checked every consumer: `static/js/global-error-handler.js:11-18` only ever *hides* it, and nothing else in the repo shows it. It is dead. An implementer who greps for an existing inline error surface will find it and may reuse it.
  Fix: one line in §v1.5 recording that `#error-message-container` exists, is inert, and is deliberately not reused — it is page-global rather than adjacent to the results, and activating a permanently present element is what Q5 strict rules out.
  **Nit.**

**§v1.2 (C) — the option name misdescribes the behavior it controls**
  Risk: `announceFailure: false` does not mean "do not announce"; the condition is `announce || !standing`, so a `false` value still announces when no region stands. A later reader will assume the debounced path is silent.
  Fix: name it for what it selects (e.g. `announceOnRepeat`), or document the `|| !standing` fallthrough at the call site in `scheduleCalculate()`.
  **Nit.**

---

**Verdict: Needs revision.** No calculation-semantics drift, no non-goal violation and no terminology drift — the calculation surface really is `none` and the clearing design really does cover both of §0.1's divergences. The two blocking items are a self-inflicted stale-output regression (an out-of-order failure wiping a fresh success, criteria 5 and 8) and a message contract that is false on the first-load case Q6 explicitly put in scope (criterion 7); both are fixable inside the plan's existing file scope.

---

## Response matrix

Every finding gets a row.

**This matrix is the council-response record as written on 2026-08-25, before the owner decided OD-1 to OD-4.** Where a row speaks of a decision as still open — **R21** most visibly — **§v2.13 governs**.

**30 rows. Nothing is deferred.** Every finding is accepted; **one** carries a rejected sub-point (**R4**, restated inline at §v2.2 (F)) and **one** is accepted but re-routed out of the council's authority to the owner (**R21**, now OD-3).

**Where two reviewers reached the same finding from different charters, the row records both.** **Five** rows are convergences: **R1** (architecture + product-risk), **R5** and **R27** (each test-strategist + architecture), **R14** (test-strategist + product-risk), and **R22** — the `:158` anchor — which is **three-way**, both reviewers plus the manager's own independent check.

**Re-verification note.** Every pin cited in a blocking row was re-read at `b4d6b13` before the row was written: the `== 3` count at [`test_volume_history_busy_signal_contracts.py:110`](../../tests/test_volume_history_busy_signal_contracts.py#L110) with its three matching occurrences at [`:45`](../../e2e/volume-splitter.spec.ts#L45), [`:616`](../../e2e/volume-splitter.spec.ts#L616) and [`:670`](../../e2e/volume-splitter.spec.ts#L670) and the un-`await`ed one at [`:586`](../../e2e/volume-splitter.spec.ts#L586); the `clearTimeout`-only-in-`scheduleCalculate` shape at [`:864-865`](../../static/js/modules/volume-splitter.js#L864-L865) against the un-cancelling `change` listener at [`:633`](../../static/js/modules/volume-splitter.js#L633); the throw site at [`:158`](../../static/js/modules/volume-splitter.js#L158); the 10 s `expect` budget at [`playwright.config.ts:191-193`](../../playwright.config.ts#L191-L193); `empty-states.spec.ts` [`:284-331`](../../e2e/empty-states.spec.ts#L284-L331) and [`ci.yml:346`](../../.github/workflows/ci.yml#L346) / [`:360`](../../.github/workflows/ci.yml#L360); the `error-handling.spec.ts` precedent at [`:56-64`](../../e2e/error-handling.spec.ts#L56-L64); KI-011 at [`UI_SCENARIOS_GAP_ANALYSIS.md:106`](../UI_SCENARIOS_GAP_ANALYSIS.md#L106) and its usage rule at [`:108-111`](../UI_SCENARIOS_GAP_ANALYSIS.md#L108-L111); the inert `#error-message-container` at [`base.html:268-273`](../../templates/base.html#L268-L273); zero `.alert` rules in `theme-dark.css`; and the four literal `volume-splitter.js` substring pins at [`test_css_cascade_contracts.py:500-503`](../../tests/test_css_cascade_contracts.py#L500-L503).

| # | Finding | Reviewer | Disposition | Action in v2 |
|---|---|---|---|---|
| R1 | **BLOCKING.** The failure state machine keys on response arrival order; two calculate POSTs are routinely in flight, so a stale failure can wipe a fresh success (and a stale success can erase a live failure). | architecture-reviewer **and** product-risk-reviewer — **independent convergence** | **accept** | Re-verified before accepting: `clearTimeout` exists only inside `scheduleCalculate()` at [`:864-865`](../../static/js/modules/volume-splitter.js#L864-L865), and the `change` listener at [`:633`](../../static/js/modules/volume-splitter.js#L633) calls `calculateVolume()` without cancelling the armed timer, so a drag release genuinely issues two POSTs. §v2.2(A) adds R1's new private counter `calculateRequestSeq`; §v2.2(B) captures it and guards **all three** tails; §v2.2(G) bumps it in `resetValues()`. New arm **`s6`** drives a slow 500 against a fast 200 out of order; new mutation **`M9`** deletes the guard and must red `s6`. The symbol is named in §v2.2(A) and in §v2.12's containment paragraph. |
| R2 | **BLOCKING.** `CALCULATE_ERROR_MESSAGE` is false on the first-load path Q6 put in scope — it promises "previous results were cleared" when nothing was ever shown, and §v1.5 forbids rewriting it. | product-risk-reviewer | **accept** | §v2.2(A) restates the second required proposition as a description of **current state** — that no results are being shown — not of an event. One static string is now true on the first-load path **and** the post-success path, so the single-message design that carries criterion 6 survives intact. |
| R3 | **BLOCKING (F1).** [`test_volume_history_busy_signal_contracts.py:110`](../../tests/test_volume_history_busy_signal_contracts.py#L110) pins `spec.count("await waitForVolumeSplitterReady(page);") == 3`, and the same function forbids `waitForPageReady` and `networkidle` — so the new block's `beforeEach` reds it. | test-strategist | **accept** | Verified independently. The file joins the Artifacts table with the pin bumped **`3 → 4`**, declared in §v2.2(I) as an explicitly scoped, non-weakening contract-test edit and repeated in the PR body. `scripts/pyright_baseline_diff.py` is added to the gate set because a `.py` now enters the diff. The blast-radius path count is corrected from four to **six**. §v2.11 step 6's full-pytest justification is replaced with the correct one: **nothing in QUALITY_GATE's derivation routes `e2e/**` or `static/js/**` to any pytest target, so full pytest is the only thing that catches this** — not "the suite is cheap". |
| R4 | **BLOCKING (F2).** `s3` cannot fail — one disjunct is false under the plan's own implementation and the other is satisfied by the 3 s auto-dismiss inside a 10 s budget — and helper (F) has no mutation. | test-strategist (overlapping two architecture findings) | **accept, with one sub-point REJECTED** | Accepted: `s3` becomes a **time-bounded positive** assertion (`toBeHidden({ timeout: 1000 })` measured from the click, plus a separate assertion that the success actually rendered), and **`M7`** deletes the `dismissCalculateFailureToast()` call so `s3` must red. `c1` gains the selector pin the helper depends on. **Rejected:** the suggestion that `dismissCalculateFailureToast()` also clear `#toast-body`. **Why:** `toast.js` owns that node's rendering and already mutates it at [`:60-63`](../../static/js/modules/toast.js#L60-L63) and [`:84`](../../static/js/modules/toast.js#L84). Making U1 a *third* mutator of the shared toast body would deepen coupling to the open KI-011 defect — the precise hazard the architecture reviewer warns about in the same round — for an oracle the time bound already provides. `hide()` stays; the time bound plus `M7` carry the evidence. |
| R5 | **BLOCKING (F3) / non-blocking (architecture).** [`QUALITY_GATE.md:129`](../ai_workflow/QUALITY_GATE.md#L129) routes error **and** empty-state changes to four specs; §v1.11 ran two of them. | test-strategist **and** architecture-reviewer — **convergence** | **accept** | `e2e/validation-boundary.spec.ts` and `e2e/empty-states.spec.ts` join §v2.11 step 5 and the Expected gates block. `empty-states.spec.ts` is named in **`s4`** as a second inherited console-error guard — its `Empty Volume Splitter` block at [`:284-331`](../../e2e/empty-states.spec.ts#L284-L331) clicks Reset (the function R21 modifies) and asserts no console errors. |
| R6 | **BLOCKING (F4).** Criterion 7 (first-load failure) has no arm; "carried by the same call" is an argument about the draft's shape, not an oracle. | test-strategist | **accept** | New arm **`a4`**: fresh load, 500 route, Calculate with no prior success — region visible and count 1, toast asserted first, and the criterion-7 half measured directly: both sections still carry `d-none` and `#results-body tr` count 0. |
| R7 | **BLOCKING (F5).** Criterion 6's toast half is unmeasured; nothing can kill the dedup guard, so the council was asked to ratify behavior no test would notice being removed. | test-strategist | **accept** | New arm **`a6`** drives debounced failures past the toast's 3000 ms life and asserts the region persists while `#liveToast` becomes and stays hidden; new mutation **`M8`** replaces the guard with an unconditional `showToast(...)` and must red `a6`. |
| R8 | **F6.** `b1` runs with no prior success, so its clearing assertions are trivially true before the request is sent. | test-strategist | **accept** | §v2.8 gives `b1` a clean successful calculation first, then installs the poison-200 route — same shape as `a1`. Its clearing assertions become real and `b1` gains an `M3` kill it did not have. |
| R9 | **F7.** Dropping the `consoleErrors` fixture removes the only possible oracle for the double-fire edge §v1.2 admits it cannot defend; and the cited `error-handling.spec.ts` precedent is misdescribed. | test-strategist | **accept** | §v2.8 adopts the **allow-one** posture using the public `ConsoleErrorCollector.errors` field, so unexpected console or page errors on the failure path red while the deliberate diagnostic passes. The precedent account is corrected: [`error-handling.spec.ts:56-64`](../../e2e/error-handling.spec.ts#L56-L64) **does** take the fixture and **does** call `startCollecting()` — it simply has an empty `afterEach`, which is a *weaker* posture than U1's, not the same one. Re-read and confirmed. |
| R10 | **F8.** Criterion 4 (mode-switch failure) has no arm, and `setMode()` is the one entry point where `renderSliders()` has already rebuilt every row before the request. | test-strategist | **accept** | New arm **`a5`**: succeed in basic mode, install the 500 route, switch to advanced, assert the region appears and the previous mode's table is gone. `s4` additionally cites the existing `loadPlan()` success test at [`volume-splitter.spec.ts:354-366`](../../e2e/volume-splitter.spec.ts#L354-L366) — verified: it asserts a recomputed `8.4` and lives in a block that still calls `assertNoErrors()`. |
| R11 | **F9.** Toast-assertion ordering is a live flake source: the toast lives 3000 ms and preceding locator work can consume that window. | test-strategist | **accept** | §v2.8 fixes the order for every arm that observes a toast: **toast first**, then the region, then the clearing assertions; `c1` reads `role`, `aria-live` and `#toast-body` in one pass immediately after the failure is driven. |
| R12 | **F10.** `s6` was a `git diff` inspection sitting in a table of Playwright tests, and its behavioral half overstated coverage of sites 5 and 6. | test-strategist | **accept** | The inspection moves out of the invariant table into §v2.12 as blast-radius check **BR-4**, freeing the `s6` slot for R1's race arm. The caveat is stated plainly: the existing tests cover sites 2, 3 and 4 only; **site 5's error row and site 6's activate/deactivate have no behavioral coverage and rest on the `git diff` check alone.** |
| R13 | **F11.** §v1.1's restart-clause sentence is not a quotation of §6.5, the operative rule is under-cited, and option (ii)'s cost is understated. | test-strategist | **accept** | §v2.1 now quotes the operative practice — **"changed no JS test case"** — with all three anchors ([`:74-77`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L74-L77), [`:100-101`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L100-L101), [`:129-131`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L129-L131)), plus the [`:858-859`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L858-L859) carve-out that only makes sense if a non-packet change could otherwise restart the clock. Option (ii)'s cost line is hardened from *"arguably restarts"* to **restarts, on the document's own three-times-applied rule**. Option (iii) gets the named home it lacked. |
| R14 | **F12 / product-risk.** The Q5-strict trade means no automated a11y oracle covers the failure surface in either theme, and `theme-dark.css` has no `.alert` rules. | test-strategist **and** product-risk-reviewer (toast-residue half) — **convergence** | **accept** | Confirmed: zero `.alert` matches in `static/css/theme-dark.css`. §v2.11 step 8 adds a **one-off dual-theme axe or contrast reading against the failure state during manual smoke, recorded in the PR body as one-time evidence.** The axe matrix itself is still not edited, so the pins at [`accessibility.spec.ts:834`](../../e2e/accessibility.spec.ts#L834) and [`:839`](../../e2e/accessibility.spec.ts#L839) stay untouched. |
| R15 | The post-2xx path leaves `applyServerRanges()` residue — range state and track paint from a response that was declared a failure — which §v1.4's justification does not reach. | architecture-reviewer | **accept** | §v2.4 states the disposition explicitly: **the residue is accepted**, because a recommended range is a property of muscle and mode and reverting it would need a snapshot/restore that is more moving state than this packet wants. It is **pinned either way** by an assertion in `b1`, whose payload now carries a real non-empty `ranges` map (shape `{ min, max }`, per [`toNumericRange()`](../../static/js/modules/volume-splitter.js#L25-L36)) so the residue actually occurs rather than being masked by the empty map. The `applyServerRanges()` call is **not** moved. |
| R16 | KI-011 is live, U1 becomes its second caller, and Plan v1 never mentions it; the `#liveToast` scoping in helper (F) has no stated reason and invites being "tightened". | architecture-reviewer | **accept** | §v2.2 gains a KI-011 paragraph: the inline region is the durable retry path, toast-button loss to an unrelated `showToast` is accepted, and **the `#liveToast` scoping is deliberate and must not be narrowed to `#toast-body`** — the same instruction that keeps `toast.test.js` B30–B35 placement-neutral. The announce condition is extended so a failure also re-announces when our toast content no longer stands, measured by the shared probe specified at §v2.2 (J). |
| R17 | `docs/UI_SCENARIOS_GAP_ANALYSIS.md` is the registry this repair belongs in and it is not in the Artifacts table. | architecture-reviewer | **accept** | A **`KI-012`** row is added, marked Mitigated and linked to `a1`, `a2` and `b1`, per the file's own usage rule at [`:108-111`](../UI_SCENARIOS_GAP_ANALYSIS.md#L108-L111). The file joins the Artifacts table and §v2.12's blast radius. Confirmed KI-011 at [`:106`](../UI_SCENARIOS_GAP_ANALYSIS.md#L106) is the highest assigned ID, so `KI-012` is the next one. |
| R18 | OD-4's recommendation rests on a design argument when two stronger contract arguments exist. | architecture-reviewer | **accept** | OD-4 now carries both: with the flag flipped, a request failure fires the wrapper's toast at [`fetch-wrapper.js:213`](../../static/js/modules/fetch-wrapper.js#L213) **and then** the page's own — two notifications per failure, which is not one logical failure state (criterion 6); and the literal reading **cannot serve criterion 12 at all**, because the flag is never consulted on the post-2xx path. |
| R19 | Under the recommended OD-4 reading, `showErrorToast: false` ships with **zero** regression pressure, and no black-box arm can give it any — removing it would produce no user-visible difference. | product-risk-reviewer | **accept** | Traced and confirmed: the page's toast would win the race, so every proposed arm stays green. OD-4 now states this as **part of what the owner is accepting**, taking option (a) — accept on the record. Option (b), a `MutationObserver` on `#toast-body` via `addInitScript`, is **priced and declined** in v2 with its reason, so the choice is visible rather than silent. The recommendation is no longer presented as coverage-neutral. |
| R20 | Repeat-toast suppression misses the keyboard slider path: arrow keys fire `input` **and** `change`, so a keyboard user gets an assertive re-announcement per keypress. | product-risk-reviewer | **accept** | §v2.2(H) passes the suppression option from the slider `change` listener at [`:633`](../../static/js/modules/volume-splitter.js#L633) as well as from `scheduleCalculate()`. The first failure of an interaction still announces, because no region is standing; repeats fall through to the standing region. Recorded under OD-2. |
| R21 | **OD-3 narrows signed criterion 6** ("persists until the next successful calculation") and a council cannot disposition a criterion the owner signed. | product-risk-reviewer | **accept — and RE-ROUTED to the owner** | The council does not decide this. OD-3 is re-marked **owner-decided** and re-presented as a **scoped amendment to criterion 6** — "…until the next successful calculation **or until the user resets**" — with the merits argued but the decision left open. v2 specifies the behavior both ways so implementation is not blocked on it: if the owner declines the amendment, the single call in `resetValues()` is dropped and nothing else changes. |
| R22 | **Nit, three-way.** `b1`'s throw site is `:158` (`data.status`), not `:161` (`data.weekly_sets`). | architecture-reviewer, product-risk-reviewer **and** the manager — **independent three-way convergence** | **accept** | Re-read at [`:158`](../../static/js/modules/volume-splitter.js#L158): `const statusLabel = (data.status || 'optimal');` is the first null dereference, one statement before the `weekly_sets` interpolation. Corrected in §v2.8. Recorded as the one place Plan v1's own "measured, not inferred" discipline slipped — three readers catching it independently is the signal, not the severity. |
| R23 | **Nit.** §v1.4 cites criterion 8 to justify a failure-path exclusion, but criterion 8 opens "Given a **successful** POST" and is success-path-scoped. | product-risk-reviewer | **accept** | The criterion 8 citation is dropped from §v2.4's slider-track exclusion. The exclusion now rests on criterion 3's four-surface enumeration plus the muscle-and-mode-property argument, which stands on its own. |
| R24 | **Nit.** An inert hidden `.alert alert-danger` already exists at `base.html:268-273` and an implementer may reuse it. | product-risk-reviewer | **accept** | Verified inert — [`base.html:268-273`](../../templates/base.html#L268-L273) is `d-none` plus inline `display: none !important`, and `global-error-handler.js` only ever hides it. §v2.5 records that `#error-message-container` exists, is dead, and is **deliberately not reused**: it is page-global rather than adjacent to the results, and activating a permanently present element is exactly what Q5 strict rules out. |
| R25 | **Nit.** `announceFailure` misdescribes what it controls — `false` still announces when no region stands. | product-risk-reviewer | **accept** | Renamed **`forceAnnounce`**, which is what the flag actually selects: announce even when a region already stands. The condition reads `forceAnnounce || !standing`, and the fallthrough is documented at both suppressing call sites. |
| R26 | **Nit.** New e2e selectors bypass the `SELECTORS` registry, and either choice invalidates §v1.12's path count. | architecture-reviewer | **accept — settled one way** | **Raw selectors are deliberate for this single-spec block, and `e2e/fixtures.ts` is NOT changed.** The same spec already uses raw selectors for page-local hooks at [`:23`](../../e2e/volume-splitter.spec.ts#L23), [`:34-35`](../../e2e/volume-splitter.spec.ts#L34-L35) and [`:366`](../../e2e/volume-splitter.spec.ts#L366); the registry at [`fixtures.ts:155-158`](../../e2e/fixtures.ts#L155-L158) and [`:184-188`](../../e2e/fixtures.ts#L184-L188) carries cross-spec surfaces, and these two hooks have exactly one consumer. §v2.12's blast-radius list is stated to match, at **six** paths. |
| R27 | **Nit (N3 + architecture).** §v1.11 step 1 names one pinned inventory surface where the change moves two. | test-strategist **and** architecture-reviewer — **convergence** | **accept** | §v2.11 step 1 names **both**: per-spec Playwright counts and `waitForTimeout` lines per file ([`QUALITY_GATE.md:61`](../ai_workflow/QUALITY_GATE.md#L61); the committed artifact records 82 across 14 files at [`TEST_INVENTORY.md:21`](../test_inventory/TEST_INVENTORY.md#L21)). §v2.8 additionally requires `a3`, `a6` and `c2` to pace themselves on `page.waitForResponse('**/api/calculate_volume')` rather than `page.waitForTimeout`, holding that surface at **zero delta** for this file. |
| R28 | **Nit (N1).** `data-testid` duplicates `CALCULATE_ERROR_ID` as a bare literal and can drift from it. | test-strategist | **accept** | §v2.2(D) derives it: `region.dataset.testid = CALCULATE_ERROR_ID`. |
| R29 | **Nit (N2).** `volume-calculate-error` is a class with no rule in any stylesheet. | test-strategist | **accept** | Kept explicitly as a **JS-only hook**, with the escalation recorded: giving it an SCSS rule later moves the change into [`QUALITY_GATE.md:31`](../ai_workflow/QUALITY_GATE.md#L31) and pulls in `/build-css` plus the `visual.spec.ts` matrix — the escalation §v1.0 avoids. |
| R30 | **Nit (N4).** The marker paragraph is correct but immaterial, since U1 does not edit the template at all. | test-strategist | **accept** | Reduced to a clause inside §v2.2(D)'s placement sentence. |

---

## Plan v2

**This is a full restatement, not a diff against Plan v1.** Every accepted finding is folded in; the one rejected sub-point (R4) and the one finding re-routed out of the council's authority (R21) are marked **inline** where they bite, so the rationale survives without the reader holding the matrix open. Plan v1 is left above, unedited, as the record of what the three reviewers actually reviewed.

**Goal**: When `POST /api/calculate_volume` fails on `/volume_splitter`, the page tells the user so on both signed surfaces, clears every output that could be mistaken for the failed calculation's result, offers a Retry that uses the inputs as they stand, never lets a stale response overwrite a newer one, and leaves the success path observably identical to today.

### v2.0 Gate 0 reopening assessment — unchanged, and its one conditional trigger is now spent

Re-checked after the council. **No unconditional Gate 0 reopening trigger was found.**

- **No API response shape changes.** [`routes/volume_splitter.py`](../../routes/volume_splitter.py) and [`utils/volume_splitter_service.py`](../../utils/volume_splitter_service.py) are untouched. The `architecture-reviewer` independently re-derived the server contract and confirmed §v1.0's account of it.
- **No shared-contract changes.** [`toast.js`](../../static/js/modules/toast.js) and [`fetch-wrapper.js`](../../static/js/modules/fetch-wrapper.js) stay read-only. **This is why R4's sub-point was rejected**: clearing `#toast-body` from U1 would make this packet a third mutator of a node [`toast.js`](../../static/js/modules/toast.js) owns, deepening the coupling to the open KI-011 defect for an oracle a time bound already provides.
- **No calculation behavior changes.** Section 0's Calculation surface stays `none`. The `product-risk-reviewer` re-verified this against every calculation module and found no drift.
- **No CSS changes.** The region uses `alert alert-danger`, present in the shipped bundle and already an in-repo idiom. See **R29** for the escalation that giving it an SCSS rule would trigger.

**The one conditional trigger was OD-4, and it is now DECIDED — it did not fire.** The owner accepted Plan v2's non-literal reading of criterion 11 on 2026-08-26, so **Gate 0 does NOT reopen**. Its row in §v2.13 states the trigger, the three grounds for that reading, and — recorded on the owner's instruction rather than waived — exactly what taking it costs.

### v2.1 OD-1 — U1's coverage arms vs. the live JS-unit qualification window, DECIDED

**DECIDED by the owner on 2026-08-26 — option (i) now, with option (iii) as the REQUIRED follow-up.** Every artifact and gate line below is written for option (i). The measurement and the reasoning that produced the recommendation are left below exactly as the council left them.

[`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §6.5 ([`:844-868`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L844-L868)) is running a live strict 14-day qualification window: **T0 = `2026-08-22T17:59:26Z`**, strict mark **`2026-09-05T17:59:26Z`**, qualifying the suite pinned at **13 files / 231 cases**.

**R13 corrected how this must be cited.** §6.5's ratified sentence ties the restart to *"the first successful `JS Unit (Vitest, non-required)` run on `main` after the final expansion packet lands"* and, read alone, does not say "any suite change restarts". The operative rule is the document's own repeated practice, applied three times in a row, and **that** is what governs:

- [`:74-77`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L74-L77) — *"**Packet F changed no JS test case**, so Q2's restart clause never engaged"*
- [`:100-101`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L100-L101) — *"PR #412 was documentation-only and changed no JS test case"*
- [`:129-131`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L129-L131) — *"#413 changed **no JS test case**, so Q2's restart clause did not engage"*

The operative test is **"changed no JS test case."** The §6.5 carve-out at [`:858-859`](../testing_phase3/STEP12_JS_UNIT_GATE0.md#L858-L859) — Packet F *"is a separate required predecessor and may land inside the window; it does not restart it"* — only makes sense if something other than the A/B/C packets could otherwise restart the clock. **U1 is not a named predecessor.**

| Option | What U1 ships | Cost, stated honestly |
|---|---|---|
| **(i) E2E-only coverage now** — **CHOSEN** | Every arm lives in [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts). Zero Vitest files, zero Vitest cases. | The window is untouched — the suite stays at 13 files / 231 cases and the strict mark stays `2026-09-05T17:59:26Z`. Cost: the new helpers get no unit-level coverage, so a pure-logic regression is caught only through a browser. Playwright per-spec counts and `waitForTimeout` lines move, which is an ordinary inventory regeneration and reds nothing. |
| **(ii) Add Vitest coverage now** — **NOT CHOSEN** | A new `static/js/modules/__tests__/volume-splitter.test.js`. | **Hardened per R13: this restarts the window — not "arguably".** On the rule the document has applied three consecutive times, adding a Vitest file changes a JS test case and engages Q2's restart clause. The days already accumulated are discarded and the strict mark moves to roughly U1's merge plus fourteen days, delaying **D2**. D2 is not U1's to spend. |
| **(iii) Defer Vitest coverage past the strict mark** — **REQUIRED FOLLOW-UP** | Option (i) now, plus a follow-up packet adding the Vitest file after `2026-09-05T17:59:26Z`. | The window is untouched and the unit coverage is eventually written. Cost: a second PR and a second review cycle. **R13's outstanding requirement is met in §v2.14, which gives the obligation a named, committed home** rather than leaving it as a sentence that will be forgotten. |

**Plan v2 recommends (i), with (iii) as the named follow-up** — for the reason the `test-strategist` independently endorsed: all three Gate 0 arms are DOM-and-announcement failure behaviors (a live-region announcement, `document.activeElement` under a real focus model, a Bootstrap toast lifecycle) that jsdom approximates rather than measures. **This was a recommendation; the owner granted exactly it on 2026-08-26.** The binding consequences are recorded in **OD-1** at §v2.13.

### Scope

- **In**: the promise tail and sequencing of `calculateVolume()` in [`volume-splitter.js`](../../static/js/modules/volume-splitter.js); **five** new module-private helpers, two new module-private constants and one new module-private counter in that same file; one added line in `resetValues()`; one option passed from two call sites; one new `test.describe` block appended to [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts); a `3 → 4` count bump in [`test_volume_history_busy_signal_contracts.py`](../../tests/test_volume_history_busy_signal_contracts.py); a `KI-012` row in [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md); the regenerated [`docs/test_inventory/`](../test_inventory/) artifact; this planning document.
- **Out**: the five deliberate `showErrorToast: false` sites at [`:191`](../../static/js/modules/volume-splitter.js#L191), [`:251`](../../static/js/modules/volume-splitter.js#L251), [`:288`](../../static/js/modules/volume-splitter.js#L288), [`:372`](../../static/js/modules/volume-splitter.js#L372) and [`:828`](../../static/js/modules/volume-splitter.js#L828); [`fetch-wrapper.js`](../../static/js/modules/fetch-wrapper.js); [`toast.js`](../../static/js/modules/toast.js); [`e2e/fixtures.ts`](../../e2e/fixtures.ts) (**R26**, settled); the `/api/calculate_volume` server contract, status code and payload; [`routes/volume_splitter.py`](../../routes/volume_splitter.py); [`utils/volume_splitter_service.py`](../../utils/volume_splitter_service.py); volume calculations, classification, recommended ranges, DB schema and API response shapes; the 300 ms debounce interval, the request payload and the call sequence; any new `.spec.ts` file and therefore any edit to [`ci.yml`](../../.github/workflows/ci.yml); any `scss/**` or `static/css/**` edit; the axe matrix in [`accessibility.spec.ts`](../../e2e/accessibility.spec.ts); packets U2, U3, R1, R2, R3, V1, Track P1 and Track D1; PRs #415 and #416; branch protection and repository settings.
- **Out — recorded debt owned elsewhere, explicitly not repaired here**: [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md); [`DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md) row 9; [`PRODUCT_DOCS_PLAN.md`](../PRODUCT_DOCS_PLAN.md) line 113; [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md); [`ACTIVE_DEVELOPMENT.md`](../ACTIVE_DEVELOPMENT.md). **KI-011 itself is not fixed by U1** — only recorded (§v2.2, KI-011 paragraph).

### Artifacts

**Six changed paths.** The count is stated here and repeated identically in §v2.12's blast-radius check, because Plan v1's "four" was falsified by **R3** and **R17** and a mismatched count is how a real diff gets waved through.

| Path | Change | Notes |
|---|---|---|
| [`static/js/modules/volume-splitter.js`](../../static/js/modules/volume-splitter.js) | modify | The whole production change. Rewrite the tail of `calculateVolume()` into two independently-mutatable failure sites behind a request-sequence guard; add `calculateRequestSeq`, `CALCULATE_ERROR_ID`, `CALCULATE_ERROR_MESSAGE`, and the **five** helpers `enterCalculateFailureState()`, `renderCalculateFailureRegion()`, `exitCalculateFailureState()`, `dismissCalculateFailureToast()` and `ourToastContentStands()`; add one call in `resetValues()`; pass `forceAnnounce: false` from two call sites. |
| [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts) | modify | One new `test.describe` appended: `a1`–`a6`, `b1`, `c1`–`c2`, `s1`–`s3`, `s6`. Already on `ci.yml`'s required list at [`:363`](../../.github/workflows/ci.yml#L363), so extending it is structurally free. |
| [`tests/test_volume_history_busy_signal_contracts.py`](../../tests/test_volume_history_busy_signal_contracts.py) | modify | **R3.** [`:110`](../../tests/test_volume_history_busy_signal_contracts.py#L110)'s `== 3` becomes `== 4`. Explicitly scoped, justified in the PR body, and **non-weakening** — the assertion still pins an exact count and the sibling `waitForPageReady` / `networkidle` prohibitions at [`:111-112`](../../tests/test_volume_history_busy_signal_contracts.py#L111-L112) are untouched. This is the path that puts a `.py` in the diff. |
| [`docs/UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md) | modify | **R17.** Add row `KI-012` — the next ID after KI-011 at [`:106`](../UI_SCENARIOS_GAP_ANALYSIS.md#L106) — marked **Mitigated**, describing the two-site silence and linking `a1`, `a2` and `b1` as the locking tests, per the file's own rule at [`:108-111`](../UI_SCENARIOS_GAP_ANALYSIS.md#L108-L111). Editing an existing `docs/*.md` moves no inventory node. |
| [`docs/test_inventory/TEST_INVENTORY.json`](../test_inventory/TEST_INVENTORY.json) · [`.md`](../test_inventory/TEST_INVENTORY.md) | regenerate | Two pinned surfaces move, not one — see §v2.11 step 1. Regenerate with the generator; never hand-edit. |
| [`docs/volume_failure_feedback/PLANNING.md`](PLANNING.md) | modify | This document. |
| [`e2e/fixtures.ts`](../../e2e/fixtures.ts) | **not modified** | **R26, settled.** Raw selectors are deliberate for a single-spec block; the registry carries cross-spec surfaces. |
| [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | **not modified** | A new spec file would require editing [`:363`](../../.github/workflows/ci.yml#L363) and would red the `== 25` pin at [`test_playwright_shard_launcher_contracts.py:65-67`](../../tests/test_playwright_shard_launcher_contracts.py#L65-L67). |
| [`e2e/accessibility.spec.ts`](../../e2e/accessibility.spec.ts) | **not modified** | Run, not edited — §v2.10 `s5`. |
| `static/js/modules/__tests__/volume-splitter.test.js` | **not created under option (i)** | Listed so the omission stays deliberate and visible. See **OD-1** and §v2.14. |

**Effort**: M · **Owner**: implementation agent, after this signed planning PR merges · **Depends on**: nothing further from the owner — **OD-1**, **OD-3** and **OD-4** are decided and **OD-2**'s reading is ratified (§v2.13), and Plan v2 is approved at the sign-off block below. The single remaining precondition is that this signed planning PR merges successfully.

### v2.2 Exact production change — files, symbols, current lines, shape

All in [`static/js/modules/volume-splitter.js`](../../static/js/modules/volume-splitter.js). `showToast` is already imported and used in this module (for example at [`:217`](../../static/js/modules/volume-splitter.js#L217)), so no new import is added.

**A naming note, to prevent a collision with §0.2.** §0.2 numbers the six **call sites** 1 to 6, and the calculate call is its site 1. Below, **suppression site 1** and **suppression site 2** mean the two *suppressions inside that one call* — respectively `showErrorToast: false` at [`:131`](../../static/js/modules/volume-splitter.js#L131) (request-failure class) and the `console.error`-only `.catch` at [`:136-138`](../../static/js/modules/volume-splitter.js#L136-L138) (post-2xx response-handling class).

**(A) Three new module-private symbols**, placed beside the existing module constants near the top of the file.

- `CALCULATE_ERROR_ID = 'volume-calculate-error'` — the region's element id, and the uniqueness mechanism Q4 relies on.
- `CALCULATE_ERROR_MESSAGE` — one static string. **R2 changed what it must say.** The two required propositions are now: **the calculation failed**, and **no results are currently being shown**. The second is a statement of *current state*, not of an event, so the string is true on the first-load path (where nothing was ever shown) and on the post-success path (where `clearResults()` has just emptied everything). The rejected v1 phrasing — "your previous results were cleared" — is false on T1, the case Q6 affirmatively assigned to U1. Register: plain English, ending `Please try again.` to match four of the five existing messages in this file ([`:217`](../../static/js/modules/volume-splitter.js#L217), [`:263`](../../static/js/modules/volume-splitter.js#L263), [`:318`](../../static/js/modules/volume-splitter.js#L318), [`:439`](../../static/js/modules/volume-splitter.js#L439)).
- `let calculateRequestSeq = 0;` — **R1's new private counter.** Monotonic. It exists so the failure state machine is keyed on **request** order rather than response arrival order.

**(B) `calculateVolume()`** — [`:111-139`](../../static/js/modules/volume-splitter.js#L111-L139). Three edits; nothing else in the function moves.

1. The signature gains one defaulted option: `function calculateVolume(options = {})` destructuring `{ forceAnnounce = true }`. **Renamed from `announceFailure` per R25** — the flag does not mean "do not announce"; it selects whether to announce *even when a region already stands*. Because it is defaulted, the three call sites that pass nothing — the Calculate button at [`:64`](../../static/js/modules/volume-splitter.js#L64), `loadPlan()` at [`:213`](../../static/js/modules/volume-splitter.js#L213) and `setMode()` at [`:533`](../../static/js/modules/volume-splitter.js#L533) — keep today's behavior exactly, and the request payload built at [`:112-124`](../../static/js/modules/volume-splitter.js#L112-L124) is untouched. Criterion 9 holds by construction.
2. `const seq = ++calculateRequestSeq;` is the **first statement** of the function body.
3. The promise tail at [`:134-138`](../../static/js/modules/volume-splitter.js#L134-L138) is replaced. `showErrorToast: false` at [`:131`](../../static/js/modules/volume-splitter.js#L131) **stays**, per §v2.0 and OD-4. The new tail is:

   - `.then(response => response.data)` — unchanged.
   - `.then(data => { … })` whose body opens with `if (seq !== calculateRequestSeq) { return; }`, then a `try` calling `handleCalculateResponse(data)`, followed on success by `exitCalculateFailureState()`; and a `catch (error)` that logs a diagnostic `console.error` and calls `enterCalculateFailureState({ forceAnnounce })`, then `return`s. **This inner `catch` is suppression site 2's replacement and the sole handler of the post-2xx response-handling failure class.**
   - `.catch(error => { … })` opening with the same `if (seq !== calculateRequestSeq) { return; }`, then a diagnostic `console.error` and `enterCalculateFailureState({ forceAnnounce })`. **This outer `.catch` is suppression site 1's replacement and the sole handler of the request-failure class — non-2xx via [`fetch-wrapper.js:200-217`](../../static/js/modules/fetch-wrapper.js#L200-L217) and transport failure via [`:244-247`](../../static/js/modules/fetch-wrapper.js#L244-L247).**

   **All three tails are guarded, by two checks — stated explicitly so no reader thinks a tail was missed.** The `architecture-reviewer` asked for the guard at the head of all three tails. Two checks achieve exactly that: the inner `catch` is lexically nested **inside** the already-guarded success `.then`, and nothing between that check and the throw yields to the event loop, so no other request can bump the counter in between. A third check there would be provably unreachable. The guarantee is delivered in full; only the placement is reduced.

   **Why the inner `try`/`catch` rather than one shared `.catch`.** Load-bearing, not stylistic. A single handler would make the two failure classes converge on one line, and then no mutation could restore one class's suppression *in isolation* — criteria 11 and 12 would be provable only jointly, which §0.2 forbids. The `test-strategist` traced both mutations against the real control flow and confirmed the isolation is real in both directions.

   **One classification edge, stated rather than hidden.** If `response` were ever nullish, `response.data` throws inside the first `.then` and lands in the outer `.catch`, i.e. it is classified as a request failure. This cannot arise against the measured server contract and is recorded only so a reviewer does not mistake it for an unnoticed hole.

   **A second edge — now observed rather than merely admitted.** If `enterCalculateFailureState()` itself threw inside the inner `catch`, the rejection would reach the outer `.catch` and the handler would run twice. The region helper is idempotent, so the observable outcome would still be one region, but the double-fire would produce console noise. **Under R9's allow-one `consoleErrors` posture (§v2.8) that noise now reds a test** instead of going unobserved, which is the concrete reason the fixture is kept rather than dropped.

**(C) `enterCalculateFailureState({ forceAnnounce })`** — new. Order matters:

1. `clearResults()` — [`:870-899`](../../static/js/modules/volume-splitter.js#L870-L899). Carries criteria 3, 4 and 7 in one call; see §v2.4.
2. `const standing = Boolean(document.getElementById(CALCULATE_ERROR_ID));`
3. `renderCalculateFailureRegion()` — creates the region if and only if none stands.
4. Toast, conditionally: `if (forceAnnounce || !standing || !ourToastContentStands()) { showToast('error', CALCULATE_ERROR_MESSAGE, { action: { label: 'Retry', ariaLabel: 'Retry volume calculation', onClick: () => calculateVolume() } }) }`. The third disjunct is **R16's** extension: if an unrelated `showToast` has destroyed our action button, the standing region is no longer backed by our own calculate-failure toast and a repeat failure must re-announce rather than leave the user reading "Failed to load saved volume plans" as the only visible notification. `ourToastContentStands()` is specified in **(J)** and is the single shared probe — the dismiss helper `(F)` calls the same one, so there is one probe, not two.

**KI-011 — U1 is its second caller, and that is recorded here rather than discovered later (R16).** [`UI_SCENARIOS_GAP_ANALYSIS.md:106`](../UI_SCENARIOS_GAP_ANALYSIS.md#L106) records KI-011 as **Open, not mitigated**: any later `showToast()` destroys a still-live action button, because [`toast.js:60`](../../static/js/modules/toast.js#L60) clears `toastBody.innerHTML` and [`:84`](../../static/js/modules/toast.js#L84) appends the button into that same node. Today's sole caller is [`volume-splitter.js:299-306`](../../static/js/modules/volume-splitter.js#L299-L306); U1's Retry becomes the second. It is reachable on U1's own page: during a sustained fault the history refresh raises its own error toast at [`:439`](../../static/js/modules/volume-splitter.js#L439) and takes the Retry button with it. **U1 accepts that loss and does not fix KI-011** — the durable Retry is the inline region, which is a real argument *for* Q2's two-surface answer. Two instructions follow, and both are binding on the implementer: (a) the announce condition carries the `!ourToastContentStands()` disjunct above; (b) **the `#liveToast` scoping in the shared probe (J), and therefore in helper (F), is deliberate and must NOT be narrowed to `#toast-body`** — that scoping is what keeps the probe working across the node relocation a KI-011 fix would require, the same reason `toast.test.js` B30–B35 are deliberately placement-neutral.

**(D) `renderCalculateFailureRegion()`** — new, and **idempotent by contract**. It returns immediately if `document.getElementById(CALCULATE_ERROR_ID)` exists, and it does not rewrite the message text on a repeat failure, because rewriting identical text still mutates the DOM and is the churn Q4 rules out. Otherwise it builds the node with `createElement` and `textContent` — never `innerHTML` — assigns `id = CALCULATE_ERROR_ID`, `className = 'volume-calculate-error alert alert-danger …'`, and `region.dataset.testid = CALCULATE_ERROR_ID` (**R28** — derived, not a bare literal, so the id and the test hook cannot drift). It appends a message `<span>` and a `<button type="button" data-testid="volume-calculate-retry" aria-label="Retry volume calculation">Retry</button>` whose click handler is `() => calculateVolume()`, then inserts the node with `panel.prepend(region)` where `panel` is `document.querySelector('.volume-insights-panel')` ([`volume_splitter.html:83`](../../templates/volume_splitter.html#L83)), landing it immediately before `.results-section` at [`:85`](../../templates/volume_splitter.html#L85) — adjacent to the results, as Q2 requires, and outside the `AGENT:START B-5 PRIORITY-CLASSES` block, which is immaterial anyway since U1 does not edit the template (**R30**). `prepend` on a missing panel is guarded by the early return.

`volume-calculate-error` is kept as a **JS-only hook with no stylesheet rule** (**R29**). Giving it an SCSS rule later moves the change under [`QUALITY_GATE.md:31`](../ai_workflow/QUALITY_GATE.md#L31) and pulls in `/build-css` plus the `visual.spec.ts` matrix — the escalation §v2.0 avoids.

**(E) `exitCalculateFailureState()`** — new. `document.getElementById(CALCULATE_ERROR_ID)?.remove()`, then `dismissCalculateFailureToast()`. **`remove()`, never `classList.add('d-none')`** — Q5 strict forbids a permanently present element, and a hidden-but-present node is exactly what it rules out. Both calls are no-ops when nothing stands, so the success path gains no observable state.

**(F) `dismissCalculateFailureToast()`** — new, and deliberately narrow. `showToast`'s default duration is 3000 ms ([`toast.js:33`](../../static/js/modules/toast.js#L33)), so a success arriving within three seconds of a failure would otherwise leave an error toast standing over fresh results. The helper calls the shared probe `ourToastContentStands()` (**(J)**) so a success toast from an unrelated save or activate action is never dismissed, and then calls `bootstrap.Toast.getInstance(toastElement)?.hide()` — the same public API [`toast.js`](../../static/js/modules/toast.js) itself uses at [`:74`](../../static/js/modules/toast.js#L74) and [`:103`](../../static/js/modules/toast.js#L103). **No change to `toast.js` is required or made.**

> **R4's sub-point is REJECTED, and here is why.** The `test-strategist` suggested (F) also clear `#toast-body` after `hide()`, to turn `s3`'s first disjunct into a timing-independent oracle. **Declined.** [`toast.js`](../../static/js/modules/toast.js) owns that node and already mutates it at [`:60-63`](../../static/js/modules/toast.js#L60-L63) and [`:84`](../../static/js/modules/toast.js#L84); making U1 a third mutator would deepen exactly the coupling to open defect KI-011 that the `architecture-reviewer` warned against in the same round, and it would make a future KI-011 fix harder to land. The oracle problem is real and is solved instead by the **time-bounded** `s3` and by **M7** (§v2.9 and §v2.10), which cost nothing in coupling. `hide()` stays.

**(G) `resetValues()`** — [`:178-185`](../../static/js/modules/volume-splitter.js#L178-L185). Two additions after the existing `clearResults()` at [`:184`](../../static/js/modules/volume-splitter.js#L184):

- `calculateRequestSeq += 1;` — **R1.** Reset invalidates any in-flight calculation, so a failure that resolves after the user has zeroed the sliders cannot repaint a failure region over a deliberately blanked page.
- `exitCalculateFailureState();` — **OD-3 was GRANTED by the owner on 2026-08-26, so this line SHIPS** (§v2.13). The sequence bump above is **independent of OD-3 and required regardless**, because it is R1's race fix rather than OD-3's.

**(H) The two suppressing call sites.** Both pass `{ forceAnnounce: false }`:

- `scheduleCalculate()` — [`:863-868`](../../static/js/modules/volume-splitter.js#L863-L868); the single change is the timer body at [`:867`](../../static/js/modules/volume-splitter.js#L867). **The 300 ms interval, the `clearTimeout` guard and the call sequence are unchanged** (criterion 9).
- The slider `change` listener — [`:633`](../../static/js/modules/volume-splitter.js#L633). **R20.** Keyboard operation of `input[type=range]` fires `input` **and** `change` on every arrow keypress, so without this the keyboard path re-fires an `aria-live="assertive"` toast per keypress — the continuous re-announcement OD-2 exists to avoid, landing on the user for whom it is most hostile. The first failure of an interaction still announces, because `!standing` is true then; repeats fall through to the standing region.

Both call sites carry a one-line comment recording the `|| !standing` fallthrough, so no later reader assumes these paths are silent (**R25**).

**(I) [`tests/test_volume_history_busy_signal_contracts.py`](../../tests/test_volume_history_busy_signal_contracts.py)** — the `== 3` at [`:110`](../../tests/test_volume_history_busy_signal_contracts.py#L110) becomes `== 4`, because the new `test.describe`'s `beforeEach` adds a fourth `await waitForVolumeSplitterReady(page);` and the same function forbids both alternatives at [`:111-112`](../../tests/test_volume_history_busy_signal_contracts.py#L111-L112). Verified: the three current matches are at [`:45`](../../e2e/volume-splitter.spec.ts#L45), [`:616`](../../e2e/volume-splitter.spec.ts#L616) and [`:670`](../../e2e/volume-splitter.spec.ts#L670); the occurrence at [`:586`](../../e2e/volume-splitter.spec.ts#L586) is un-`await`ed and does not match. **Explicitly scoped, and non-weakening**: it stays an exact-count assertion and the sibling prohibitions are untouched. Declared here and repeated in the PR body.

**(J) `ourToastContentStands()`** — new, and the fifth helper. It is lettered last rather than inserted between (E) and (F) for one reason: re-lettering (F)–(I) would make Plan v2's letters disagree with Plan v1 and with all three verbatim reviews, every one of which uses **(F)** for the dismiss helper. Preserving that correspondence is worth an out-of-order letter.

- **What it does.** Returns `Boolean(document.querySelector('#liveToast button[aria-label="Retry volume calculation"]'))`. Nothing else. It is the **single** shared probe: `(C)`'s announce condition and `(F)`'s dismiss guard both call it, so the selector exists in exactly one place and cannot drift between them.
- **Why the name is what it is.** It measures whether **our content still stands in the toast body** — not whether a toast is on screen. §v2.5 establishes that `hide()` leaves the message span and the Retry button in `#toast-body`, and the inherited 3000 ms auto-dismiss does the same, so the probe **returns `true` for a toast that has already dismissed itself**. It is deliberately blind to visibility. The earlier name `ourToastIsLive()` claimed the opposite and was corrected at diff review — the same misnaming **R25** caught on `announceFailure`.
- **Why that blindness is correct for both callers.** `(F)` only needs to know that the node it is about to `hide()` is ours rather than an unrelated success toast's; hiding an already-hidden toast is a no-op. `(C)` only needs to know whether an unrelated `showToast` has *replaced* our content — the KI-011 case in the paragraph above — because that is what leaves the standing region unbacked. Neither caller asks about visibility, so the probe must not answer it.
- **Scoping.** `#liveToast`, **never** `#toast-body`. Binding, per the KI-011 paragraph above: the wider scope is what keeps the probe working across the node relocation a KI-011 fix would require.

**Untouched by name**, so a reviewer can confirm the blast radius: `displayResults()` [`:141`](../../static/js/modules/volume-splitter.js#L141), `displaySuggestions()` [`:322`](../../static/js/modules/volume-splitter.js#L322), `setMode()` [`:511`](../../static/js/modules/volume-splitter.js#L511), `renderSliders()` [`:537`](../../static/js/modules/volume-splitter.js#L537), `updateValueDisplay()` [`:694`](../../static/js/modules/volume-splitter.js#L694), `applyServerRanges()` [`:718`](../../static/js/modules/volume-splitter.js#L718), `handleCalculateResponse()` [`:748`](../../static/js/modules/volume-splitter.js#L748), `applyStatusToRow()` [`:763`](../../static/js/modules/volume-splitter.js#L763), `clearResults()` [`:870`](../../static/js/modules/volume-splitter.js#L870), and `loadPlan()` [`:187`](../../static/js/modules/volume-splitter.js#L187) apart from its existing call at [`:213`](../../static/js/modules/volume-splitter.js#L213). **`applyServerRanges()` is not moved** — reordering it relative to `displayResults()` would change the success path and need fresh criterion-8 scrutiny (**R15**).

### v2.3 State transitions, enumerated

The page does not calculate on load: `init()` ends at [`:94-97`](../../static/js/modules/volume-splitter.js#L94-L97) with `renderSliders()` and the history fetch, and never calls `calculateVolume()`. Every calculation is user-initiated or plan-initiated.

| # | Transition | Entry path | What the user sees afterwards |
|---|---|---|---|
| **T1** | **First-load failure** — no calculation has ever succeeded on this load | Calculate button [`:64`](../../static/js/modules/volume-splitter.js#L64), a slider, or a mode switch | Toast plus inline region. `clearResults()` re-adds `d-none` to both sections at [`:876-877`](../../static/js/modules/volume-splitter.js#L876-L877), which are already hidden, so the empty sections stay hidden. **The message is true here — R2's rewording is what makes it true.** Measured by **`a4`**, not left as an argument about the code's shape. **Criterion 7.** |
| **T2** | **Failure after a prior success** | Calculate button or slider `change` [`:633`](../../static/js/modules/volume-splitter.js#L633) | Toast plus inline region; previous rows, cards, status classes and pill modifiers all gone; sections return to `d-none`. Measured by `a1` and `a2`. |
| **T3** | **Mode-switch failure** | `setMode()` → `calculateVolume()` at [`:533`](../../static/js/modules/volume-splitter.js#L533), after `renderSliders()` at [`:528`](../../static/js/modules/volume-splitter.js#L528) rebuilt every `.muscle-row` | Toast plus inline region. The previous mode's results and suggestions — the divergence §0.1 measured separately — are cleared by the same `clearResults()`. Measured by **`a5`**, the one entry point where a mode-conditional clearing mistake would hide from every other arm. **Criterion 4.** |
| **T4** | **Load-plan failure** | `loadPlan()` → `setMode(…, { skipCalculate: true })` then `calculateVolume()` at [`:212-213`](../../static/js/modules/volume-splitter.js#L212-L213) | Same as T3. The plan `GET` failing is site 2 in §0.2 — deliberate and unchanged. T4's **success** side has an inherited guard at [`volume-splitter.spec.ts:354-366`](../../e2e/volume-splitter.spec.ts#L354-L366), cited in `s4`. |
| **T5** | **Retry** | The toast's Retry action, the region's Retry button, or the Calculate button, which stays enabled throughout | A fresh `POST` from the inputs as they stand. All three default `forceAnnounce` to `true`, so a retry that fails again always produces fresh feedback rather than appearing to do nothing. **Criterion 5.** |
| **T6** | **Repeated failure during a sustained fault** | Debounced `scheduleCalculate()` every 300 ms during a drag, or repeated arrow keypresses | Exactly **one** region, not replaced and not rewritten, and **no** repeat toast — both suppressing call sites pass `forceAnnounce: false` (**R20** covers the keyboard path). Measured by **`a3`** (region identity, via the `data-probe` stamp) and **`a6`** (toast silence past the 3000 ms life). **Criterion 6.** |
| **T7** | **The later success that clears everything** | Any successful `POST` **whose sequence is current** | `exitCalculateFailureState()` removes the region from the DOM and dismisses a still-standing calculate-failure toast; `handleCalculateResponse()` repaints exactly as today. **Criteria 5 and 8.** |
| **T8** | **Reset while a failure stands** | Reset button → `resetValues()` [`:178`](../../static/js/modules/volume-splitter.js#L178) | Sliders zeroed, results cleared, **the in-flight sequence invalidated**, and — **OD-3 granted** — the region removed. No request is issued. |
| **T9** | **A second calculation is in flight (NEW — R1)** | Any overlap. Guaranteed at every drag release: the `input` listener has armed the 300 ms timer at [`:627`](../../static/js/modules/volume-splitter.js#L627) → [`:867`](../../static/js/modules/volume-splitter.js#L867) while the `change` listener at [`:633`](../../static/js/modules/volume-splitter.js#L633) fires immediately without cancelling it — `clearTimeout` lives only inside `scheduleCalculate()` at [`:864-865`](../../static/js/modules/volume-splitter.js#L864-L865). Two POSTs, ~300 ms apart. | **Only the newest request may paint.** A stale failure resolving after a fresh success is discarded by the sequence guard, so it cannot call `clearResults()` and wipe valid current results; a stale success resolving after a newer failure is likewise discarded, so it cannot paint old numbers with no failure signal. Measured by **`s6`**, killed by **`M9`**. |

### v2.4 Clearing and reset, surface by surface

Q1 signed "clear". `clearResults()` at [`:870-899`](../../static/js/modules/volume-splitter.js#L870-L899) **already covers exactly the surface set criterion 3 enumerates** — both reviewers who checked it independently confirmed this line-for-line. It is reused as-is: not modified, not wrapped, not duplicated, and **no fifth clearing helper is introduced**, so there is no second source of truth for clearing.

| Stale surface | Covered by | Line |
|---|---|---|
| Results table body `#results-body` | `clearResults()` — `resultsBody.innerHTML = ''` | [`:879-881`](../../static/js/modules/volume-splitter.js#L879-L881) |
| Suggestion cards in `.suggestions-container` | `clearResults()` — `suggestionsContainer.innerHTML = ''` | [`:883-885`](../../static/js/modules/volume-splitter.js#L883-L885) |
| `.results-section` visibility | `clearResults()` — re-adds `d-none` | [`:876`](../../static/js/modules/volume-splitter.js#L876) |
| `.ai-suggestions-section` visibility | `clearResults()` — re-adds `d-none` | [`:877`](../../static/js/modules/volume-splitter.js#L877) |
| Per-muscle `status-low` / `status-optimal` / `status-high` / `status-excessive` on every `.muscle-row` | `clearResults()` | [`:887-888`](../../static/js/modules/volume-splitter.js#L887-L888) |
| `volume-value-pill--low` / `--optimal` / `--high` / `--excessive` on every `.current-value` badge | `clearResults()` | [`:889-897`](../../static/js/modules/volume-splitter.js#L889-L897) |

**Nothing in criterion 3's enumeration is left uncovered.**

Three surfaces are deliberately **outside** the stale set, each with a reason a reviewer can contest:

- **The slider value badge text**, repainted by `updateValueDisplay()` on `input` ([`:694-700`](../../static/js/modules/volume-splitter.js#L694-L700)). **Out.** It echoes the slider's own current value — an *input*, not calculation output. Resetting it would desynchronize the badge from the thumb and would itself change input state, which criterion 9 protects. What made it misleading in §0.1's reading was the *pill colour modifier* on the same element, and that **is** cleared at [`:889-897`](../../static/js/modules/volume-splitter.js#L889-L897). [`volume-splitter.spec.ts:33-39`](../../e2e/volume-splitter.spec.ts#L33-L39) already asserts badge text tracks slider value, so clearing it would red an existing test.
- **The slider track gradient**, painted by `updateSliderTrack()` [`:643`](../../static/js/modules/volume-splitter.js#L643) from `modeRangeState`. **Out.** **R23 removed the criterion 8 citation this used to lean on** — criterion 8 opens *"Given a **successful** POST"* and says nothing about the failure path, so citing it weakened a conclusion that stands without it. The exclusion now rests on two things only: criterion 3 enumerates four surfaces and the track is not among them; and a recommended range is a property of muscle and mode rather than of the failed calculation's inputs. On T3 and T4, `renderSliders()` → `updateAllSliderTracks()` [`:556`](../../static/js/modules/volume-splitter.js#L556) has already repainted from the new mode's state before the request, so no cross-mode range leak survives.
- **`applyServerRanges()` residue on the post-2xx path (NEW — R15).** `handleCalculateResponse()` calls `applyServerRanges()` at [`:751`](../../static/js/modules/volume-splitter.js#L751) **before** `displayResults()` at [`:755`](../../static/js/modules/volume-splitter.js#L755), so on `b1`'s path the range state at [`:743`](../../static/js/modules/volume-splitter.js#L743) and the track repaint at [`:744`](../../static/js/modules/volume-splitter.js#L744) have already been applied from a response that then throws and is declared a failure. **Disposition: the residue is ACCEPTED.** Reverting it would require snapshotting and restoring `modeRangeState`, which is more moving state than this packet wants, and the same muscle-and-mode-property argument applies. **It is pinned either way**: `b1`'s payload now carries a real non-empty `ranges` map so the residue actually occurs, and `b1` asserts the affected slider's track paint reflects the injected range. If a later change reverts the residue, that assertion reds and forces a deliberate decision rather than a silent one.

### v2.5 The two failure surfaces under Q5 strict — create, update, replace, remove

| | Inline region | Toast |
|---|---|---|
| **Create** | On the first failure since the last success. `renderCalculateFailureRegion()` builds the node and `prepend`s it to `.volume-insights-panel`. Before that moment `#volume-calculate-error` does not exist anywhere — not in [`volume_splitter.html`](../../templates/volume_splitter.html), not hidden, not empty. | `showToast('error', …)` on the transition into failure; on every attempt that is **not slider-driven** — the Calculate button, either Retry, a mode switch, a load-plan; and whenever our toast content no longer stands (**R16**). **Not** on the two slider paths, which pass `forceAnnounce: false` — an earlier draft said "every user-initiated attempt", which **R20** falsified by suppressing the slider `change` path, and that path is user-initiated. |
| **Update** | **Never on a repeat failure.** The early return means no attribute is rewritten and no text node replaced. One message, one state. | `showToast` rewrites `#toast-body` ([`toast.js:60-63`](../../static/js/modules/toast.js#L60-L63)) on each call. |
| **Replace** | Not applicable — the node is never replaced while a failure stands, which satisfies criterion 6's "updated or replaced rather than duplicated" by the strongest available reading: **not duplicated and not churned**. Measured by `a3`'s `data-probe` stamp. | Structurally guaranteed: a single `#liveToast`, body cleared at [`:60-63`](../../static/js/modules/toast.js#L60-L63), any live instance disposed and a new one constructed at [`:101-109`](../../static/js/modules/toast.js#L101-L109). **Toasts replace; they cannot stack.** Read and confirmed — but note `test-strategist`'s point that *this* half of criterion 6 cannot fail and is therefore not evidence of anything U1 does. The half that can fail is the dedup guard, and `a6` plus `M8` measure it. |
| **Remove** | `exitCalculateFailureState()` calls `.remove()`. **Not `d-none`.** After any success the DOM contains no `#volume-calculate-error` at all. Killed by **M5**. | `hide()` via `dismissCalculateFailureToast()`, plus the inherited 3000 ms auto-dismiss. Time-bounded assertion in `s3`, killed by **M7**. |

**Q5 strict, restated as the property the code must have**: `#volume-calculate-error` exists **if and only if** the last completed calculation failed **and the user has not since reset**. Never on load, never after a success, never as a hidden shell. **The reset clause is OD-3's**, granted 2026-08-26 — before it, the biconditional had no exception, and §v2.2 (G)'s call in `resetValues()` would have falsified it.

**Two corrections the council forced:**

- **The after-success DOM is not perfectly clean, and Plan v1 claimed it was (R14).** `bootstrap.Toast.hide()` does not clear `#toast-body`, so the failure message span and the Retry button remain inside a hidden `#liveToast` after a success. **This is inherited [`toast.js`](../../static/js/modules/toast.js) behavior shared by every toast on every page — it is not new state U1 introduces — and `toast.js` is out of scope under Section 0's shared-contract exclusion.** Q5 strict is therefore enforced against **U1's own element**, absolutely, and the toast residue is accepted as pre-existing. The residual node is inert: the compiled bundle carries `.toast:not(.show){display:none}`, which is also why `s5`'s pinned axe node counts cannot move. This is also why the shared probe (J) is named for content rather than liveness — it returns `true` for a toast that has already dismissed itself.
- **An inert `.alert alert-danger` already exists and is deliberately not reused (R24).** [`base.html:268-273`](../../templates/base.html#L268-L273) carries `#error-message-container`: `d-none` plus inline `display: none !important`, `role="alert"`, text "An unexpected error occurred. Please try again later." Verified dead — [`global-error-handler.js`](../../static/js/global-error-handler.js) only ever hides it and nothing in the repo shows it. An implementer grepping for an existing inline error surface will find it. **Do not reuse it**: it is page-global rather than adjacent to the results, and activating a permanently present element is exactly what Q5 strict rules out.

### v2.6 Retry — mechanism and payload freshness

Retry appears in two places and both use the **same** mechanism: an `onClick` of `() => calculateVolume()`, identical to the Calculate button's listener at [`:64`](../../static/js/modules/volume-splitter.js#L64).

- **It re-reads the DOM at click time. It does not replay a captured payload.** `calculateVolume()` re-reads `#training-days`, then calls `collectVolumes()` [`:702`](../../static/js/modules/volume-splitter.js#L702) and `collectRanges()` [`:714`](../../static/js/modules/volume-splitter.js#L714), all of which query live elements. **Why**: criterion 5 says the fresh `POST` is issued "from the input values as they stand at that moment". A captured payload would resend inputs the user has since changed — a new instance of the mismatch U1 is repairing.
- **No debounce on Retry.** It calls `calculateVolume()` directly, not `scheduleCalculate()`.
- **No automatic retry.** `retries` stays at the wrapper's `POST` default of `0` ([`fetch-wrapper.js:140`](../../static/js/modules/fetch-wrapper.js#L140)); no `retries` option is passed and no loop is added. Q3.
- Retry inherits `forceAnnounce: true`, so a second failure after Retry always produces fresh feedback — necessary because the toast's action button hides the toast before invoking `onClick` ([`toast.js:73-83`](../../static/js/modules/toast.js#L73-L83)).
- The in-repository precedent for `options.action` is this same file at [`:299-306`](../../static/js/modules/volume-splitter.js#L299-L306).

### v2.7 Focus and live-region behavior

**Announcement.** The toast carries it. `#liveToast` has `role="alert"`, `aria-live="assertive"`, `aria-atomic="true"`, and its container `aria-live="polite"` plus `data-testid="toast-container"` ([`base.html:235-251`](../../templates/base.html#L235-L251)). Gate 0 forbids treating that inherited markup as the **sole** evidence, so `c1` asserts the attributes **and** that the failure message text actually lands inside `#toast-body` while the toast is visible. The `test-strategist` confirmed this clears the Gate 0 evidence standard: the text-in-live-region assertion is the load-bearing one; the attribute reads are a guard against the markup being changed out from under it.

**The inline region is deliberately not a live region.** No `role="alert"`, no `role="status"`, no `aria-live`. With the toast announcing assertively, a second live region would double-announce every failure, and during a sustained fault the pairing would be hostile. The region is a persistent visual and programmatic artifact, first in the reading order of the insights panel. Its Retry button carries `aria-label="Retry volume calculation"`.

**Two distinct buttons share that one `aria-label` value, and conflating them is a trap.** The region's Retry button lives inside `#volume-calculate-error`; the toast's lives inside `#liveToast`. Neither can ever match the other's selector. The shared probe (J) and helper (F) are scoped to `#liveToast` and therefore only ever see the **toast** one, and `c1` pins that one by assertion rather than by prose (**R4**). **Practical warning for the implementer and for every arm**: an unscoped `button[aria-label="Retry volume calculation"]` locator resolves to **two** nodes while a failure stands and will raise a Playwright strict-mode violation. Every locator over either button must be scoped — `#liveToast button[…]` or `#volume-calculate-error button[…]`, or the `data-testid="volume-calculate-retry"` hook for the region's.

**Focus.** **No code path added by this plan calls `.focus()`, `scrollIntoView()`, `autofocus`, or `tabindex="-1"` plus focus.** The guarantee: after a failure, `document.activeElement` is the element it was before.

- **Mid-drag**: focus is on `input.volume-slider`; the region is inserted as a sibling in a different subtree, which does not move focus. `c2` reads `document.activeElement` back and compares by `data-muscle`.
- **Button path**: focus stays on `#calculate-volume` ([`volume_splitter.html:61`](../../templates/volume_splitter.html#L61)).
- The only pre-existing focus move in this module is `summary?.focus()` at [`:312`](../../static/js/modules/volume-splitter.js#L312), on the save-and-activate success path — untouched, and not on the calculate path.

**No automated a11y oracle covers the failure surface in either theme (R14), and that is stated rather than left implicit.** `static/css/theme-dark.css` contains **zero** `.alert` rules — verified — so the region renders with stock Bootstrap `alert-danger` on a dark page. Stock `alert-danger` sets its own background and foreground, so a contrast violation is not expected, but nothing measures it. §v2.11 step 8 closes this with a one-off dual-theme reading recorded in the PR body. The axe matrix is deliberately **not** extended to the failure state, because that would move the pinned node counts and convert a regression gate into a maintenance chore.

### v2.8 The regression arms

All arms live in one new `test.describe('Volume Splitter calculation failure feedback')` appended to [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts). **No new spec file.** Selectors are raw, deliberately (**R26**), matching the file's own idiom at [`:23`](../../e2e/volume-splitter.spec.ts#L23), [`:34-35`](../../e2e/volume-splitter.spec.ts#L34-L35) and [`:366`](../../e2e/volume-splitter.spec.ts#L366).

**Console-error posture — allow-one, not fixture-less (R9).** Plan v1 dropped the `consoleErrors` fixture; that removed the only possible oracle for §v2.2(B)'s admitted double-fire edge. The new block **keeps** the fixture, calls `startCollecting()`, and asserts in `afterEach` that every collected entry contains the deliberate diagnostic marker — so the intended `console.error` passes and **anything else reds**. The allow-list at [`fixtures.ts:29-44`](../../e2e/fixtures.ts#L29-L44) filters the wrapper's `API Error` logs but not a page-specific message, and `ConsoleErrorCollector.errors` is public at [`fixtures.ts:10`](../../e2e/fixtures.ts#L10), so this needs no fixture change. **The precedent citation is corrected**: [`error-handling.spec.ts:56-64`](../../e2e/error-handling.spec.ts#L56-L64) does take the fixture and does call `startCollecting()` — it simply has an empty `afterEach`, a **weaker** posture than U1's, not the same one. The in-file comment must say that.

**Assertion ordering is specified, not left to the implementer (R11).** In every arm that observes a toast: **assert the toast first**, then the region, then the clearing assertions. The toast lives 3000 ms ([`toast.js:33`](../../static/js/modules/toast.js#L33)) and `expectToast` ([`fixtures.ts:326`](../../e2e/fixtures.ts#L326)) only passes on a *visible* toast; on a slow runner, preceding locator work can consume that window and the flake reads as a product defect. `c1` reads `role`, `aria-live` and `#toast-body` in one pass immediately after the failure is driven.

**Pacing is `waitForResponse`, never `waitForTimeout` (R27).** `a3`, `a6` and `c2` all cross the 300 ms debounce; each waits on `page.waitForResponse('**/api/calculate_volume')` per iteration. `route.fulfill` still produces a response event, so the idiom works against the interception, and it holds the `waitForTimeout`-lines-per-file inventory surface at **zero delta** for this file.

**Arm (a) — request-failure class.**

- **`a1`** — non-2xx after a prior success. Calculate cleanly, assert results visible; install `route.fulfill({ status: 500, contentType: 'application/json', body: … })` matching the real server payload and the idiom at [`error-handling.spec.ts:71-77`](../../e2e/error-handling.spec.ts#L71-L77); click Calculate. **Assertions, in order**: `expectToast`; `#volume-calculate-error` visible with count 1; `#results-body tr` count 0; both sections hidden; no `.muscle-row` carries `status-*`; no `.current-value` carries `volume-value-pill--*`; `#calculate-volume` still enabled.
- **`a2`** — transport failure via `route.abort('failed')` ([`error-handling.spec.ts:148`](../../e2e/error-handling.spec.ts#L148)). Same assertions. This is the arm that covers the wrapper's outer branch at [`fetch-wrapper.js:244-247`](../../static/js/modules/fetch-wrapper.js#L244-L247) rather than only the HTTP-error branch.
- **`a3`** — region identity under a sustained fault. Drive repeated debounced failures; after the first region appears, stamp it with a `data-probe` attribute via `page.evaluate`, drive more failures, then assert `#volume-calculate-error[data-probe="1"]` still has count 1. **Stamping is what makes "not replaced" measurable** — a bare count of 1 cannot distinguish a surviving node from a rebuilt one.
- **`a4` (NEW — R6, criterion 7).** Fresh page load, 500 route installed, click Calculate with **no prior success**. Assert the toast, then `#volume-calculate-error` visible with count 1, then the criterion-7 half: `.results-section` and `.ai-suggestions-section` **still carry `d-none`** and `#results-body tr` count 0. This is the only place "shown anyway, but the empty sections are still not revealed" is measured. Without it, an implementer who gated the failure state behind "a previous success exists" would ship green.
- **`a5` (NEW — R10, criterion 4).** Calculate successfully in basic mode; install the 500 route; switch to advanced. Assert the region appears **and** the previous mode's table is gone — `#results-body tr` count 0, `.results-section` hidden. `setMode()` is the one entry point where `renderSliders()` has already rebuilt every `.muscle-row` before the request, so a mode-conditional clearing mistake hides from every other arm.
- **`a6` (NEW — R7, criterion 6's toast half).** With the 500 route standing, focus a slider and drive debounced failures continuously for **longer than the toast's 3000 ms life**, waiting on `page.waitForResponse` between dispatches. Assert `#volume-calculate-error` stays present **and** `#liveToast` becomes hidden and stays hidden while failures continue. Under an unconditional `showToast` the element re-shows and this reds.

**Arm (b) — post-2xx response-handling class.**

- **`b1`** — **run after a clean success (R8)**, then install a **200** whose body makes `handleCalculateResponse()` throw: `{ "ok": true, "data": { "results": { "Chest": null }, "ranges": { "Chest": { "min": 1, "max": 2 } }, "suggestions": [] } }`. The wrapper returns the parsed body and `.then(response => response.data)` unwraps it, so `displayResults()` dereferences `null` at [`:158`](../../static/js/modules/volume-splitter.js#L158) — `const statusLabel = (data.status || 'optimal');`, **not** `:161` (**R22**, corrected) — raising a `TypeError` **inside** the response handler where the wrapper's toast is never reached. **Assertions**: the same ordered set as `a1` — which are now real rather than trivially true, because a prior success populated everything. Plus the **R15** residue pin: the non-empty `ranges` map means `applyServerRanges()` has repainted the Chest track before the throw, and `b1` asserts that track paint reflects the injected range, recording the accepted disposition as a test rather than as prose. Range shape is `{ min, max }`, per [`toNumericRange()`](../../static/js/modules/volume-splitter.js#L25-L36).

**Arm (c) — accessibility.**

- **`c1`** — announcement. Drive a 500; immediately assert in one pass that `#liveToast` is visible with `role="alert"` and `aria-live="assertive"`, that `[data-testid="toast-container"]` carries `aria-live="polite"`, that `#toast-body` contains the failure message, and — **R4** — that `#liveToast button[aria-label="Retry volume calculation"]` exists, pinning the exact selector helper (F) depends on.
- **`c2`** — no disruptive focus movement, measured **mid-drag**. With the 500 route standing, `focus()` a `input.volume-slider`, dispatch `input` only, wait for `#volume-calculate-error`, then assert via `page.evaluate` that `document.activeElement` is still that slider (compared by `data-muscle`), that its value is unchanged, and that neither the region nor its Retry button is active. Repeat for the Calculate-button path, where `#calculate-volume` must retain focus.

### v2.9 Mutation and negative-control proof

Every mutation is a hand edit to [`static/js/modules/volume-splitter.js`](../../static/js/modules/volume-splitter.js), run in **both directions** — mutate, observe the expected red, then revert with `git checkout -- static/js/modules/volume-splitter.js` and observe green again. **Never revert by retyping the line**; a same-shape hand revert is how a live mutation survives a "verified" pass.

Base command, from the worktree root:

`npx playwright test e2e/volume-splitter.spec.ts --project=chromium --reporter=line -g "calculation failure feedback"`

Narrow to a single arm by replacing the `-g` pattern with that test's title.

| ID | Exact mutation | Restores / measures | Expected result |
|---|---|---|---|
| **M1** | In the **outer** `.catch`, delete the `enterCalculateFailureState(…)` call, leaving the `console.error` line. | Suppression site 1 — the `console.error`-only catch for the **request-failure** class, reproducing today's silence for non-2xx and transport failures. | `a1`, `a2`, `a3`, `a4`, `a5`, `a6`, `c1`, `c2`, `s2`, `s3` **RED**, plus **`s6` RED on its mirror case only** — that case drives a request failure into the exact handler M1 deletes, so the failure state it asserts never arrives; `s6`'s primary case stays green, because a stale failure discarded by the sequence guard and a deleted failure handler are indistinguishable from outside. `b1` and `s1` **GREEN**, and **the isolation claim therefore rests on `b1` alone** — it is the only arm exercising the post-2xx class. **Criterion 11.** |
| **M2** | In the **inner** `catch`, delete the `enterCalculateFailureState(…)` call, leaving the `console.error` and the `return`. | Suppression site 2 — the `console.error`-only catch for the **post-2xx response-handling** class. | `b1` **RED**. Every other arm **GREEN** — isolation in the other direction. **Criterion 12.** |
| **M3** | Delete `clearResults()` from `enterCalculateFailureState()`. | Measures the reviewer. | `a1`, `a2`, `a5`, `b1` **RED** on the stale-clearing assertions. `b1` only gained this kill because **R8** gave it a prior success. |
| **M4** | Append `region.querySelector('button')?.focus();` to `renderCalculateFailureRegion()`. | Measures the reviewer. | `c2` **RED**. Proves the focus guarantee is asserted, not merely stated. |
| **M5** | Change `exitCalculateFailureState()` to `classList.add('d-none')` instead of `.remove()`. | Measures the reviewer. | `s2` **RED**. Proves Q5 strict is enforced by a DOM-absence assertion, not by a visibility assertion a hidden shell would satisfy. |
| **M6** | Delete the early-return guard in `renderCalculateFailureRegion()` so every failure rebuilds the node. | Measures the reviewer. | `a3` **RED** on the `data-probe` survival check. |
| **M7** | **NEW (R4).** Delete the `dismissCalculateFailureToast()` call from `exitCalculateFailureState()`. | The helper that had no mutation at all in Plan v1. | `s3` **RED** — but only because `s3` is now time-bounded. Under Plan v1's `s3` this mutation was invisible, which is exactly why it was a blocking finding. |
| **M8** | **NEW (R7).** Replace `if (forceAnnounce \|\| !standing \|\| !ourToastContentStands())` with an unconditional `showToast(...)`. | The dedup guard, under the OD-2 reading the owner ratified. | `a6` **RED**. |
| **M9** | **NEW (R1).** Delete `if (seq !== calculateRequestSeq) { return; }` from both tails. | The request-sequence guard. | `s6` **RED**. Proves the out-of-order protection is measured rather than asserted in prose. |

**M1 and M2 together discharge §0.2's closing obligation**: the regression reds if either suppression is restored *in isolation*, and each arm fails for its own class only. The `test-strategist` independently traced both against the real control flow and confirmed the isolation is genuine in both directions. **M3–M9 exist because an arm that cannot be made to fail is not evidence** — and M7, M8 and M9 were all added because the council found three places where Plan v1 had exactly that problem.

**Note on M1's framing** — see **OD-4**. `showErrorToast: false` at [`:131`](../../static/js/modules/volume-splitter.js#L131) is retained deliberately, so "restoring the request-failure suppression" means restoring the `console.error`-only handler, which reproduces today's silence exactly. Re-adding the flag is not available as a mutation because the flag is never removed — **and what that costs is stated in OD-4**.

### v2.10 Success-path invariants — proving Q5 strict held

| ID | Assertion | Carries |
|---|---|---|
| `s1` | With no route interception, complete a normal calculation. Before and after, `[data-testid="volume-calculate-error"]` has count **0** — absence from the DOM, not hidden. Results section visible, `#results-body` rows present, status classes and pill modifiers applied. | Criterion 8; Q5 strict |
| `s2` | Failure-then-success recovery. Drive a 500, assert the region present, then `page.unroute('**/api/calculate_volume')` and click Calculate. Assert `#volume-calculate-error` count **0** — removed, not hidden — and results visible again. | Criteria 5 and 8; killed by **M5** |
| `s3` | **Rewritten per R4, then given an explicit precondition at diff review.** Drive the 500 and **first assert `#liveToast button[aria-label="Retry volume calculation"]` is present.** Only then `page.unroute` + Calculate, and assert that same locator is hidden **within 1000 ms measured from the click**, plus separately that the success actually rendered. Bootstrap's `hide()` transition is ~150 ms while an un-dismissed toast stays visible for the remainder of its 3000 ms, so a 1 s bound discriminates. **The precondition was added because a reviewer found the arm could still pass for the wrong reason**: with the toast-creating path deleted, "the button is hidden" is vacuously true, so without it `s3` went green under **M1**. Plan v1's version could not fail at all — one disjunct was false under the implementation and the other was satisfied by auto-dismiss inside the 10 s `expect` budget at [`playwright.config.ts:191-193`](../../playwright.config.ts#L191-L193). | Q5 strict; killed by **M7** and by **M1** |
| `s4` | **Inherited, not newly written.** Three standing guards: the untouched describe blocks in [`volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts) keep `consoleErrors.assertNoErrors()` ([`:41-50`](../../e2e/volume-splitter.spec.ts#L41-L50)); the `Empty Volume Splitter` block in [`empty-states.spec.ts:284-331`](../../e2e/empty-states.spec.ts#L284-L331) asserts the same on the Calculate and Reset paths (**R5**); and the `loadPlan()` success test at [`volume-splitter.spec.ts:354-366`](../../e2e/volume-splitter.spec.ts#L354-L366) asserts a recomputed value and covers T4's success side (**R10**). | Criterion 8 |
| `s5` | **Inherited, not newly written.** [`accessibility.spec.ts`](../../e2e/accessibility.spec.ts) pins `'volume_splitter:light'` at [`:834`](../../e2e/accessibility.spec.ts#L834) and `'volume_splitter:dark'` at [`:839`](../../e2e/accessibility.spec.ts#L839), each at `[{ rule: 'color-contrast', nodes: 2 }]`. **Q5 strict is what protects these pins**: the region is absent from the DOM in every non-failure state, so the axe scan sees exactly today's document. Run, not edited. | Criterion 8; the a11y pins |
| `s6` | **NEW (R1) — the slot freed by moving R12's inspection out.** Drive an out-of-order pair: a **slow 500** issued first (delayed `route.fulfill`) and a **fast 200** issued second, so the failure resolves after the success. Assert that when both have settled, the fresh results are still painted, `#volume-calculate-error` has count **0**, and no error toast stands. Then run the mirror case — slow 200 first, fast 500 second — and assert the failure state holds and the stale success did not paint. | Criteria 5 and 8; killed by **M9** |

**R12's `git diff` inspection is no longer in this table** — it is an inspection, not a Playwright test. It moves to §v2.12 as **BR-4**, with its overstatement corrected there.

### v2.11 Test routing and the gate set for the implementation PR

Changed paths under option (i): `static/js/modules/volume-splitter.js`, `e2e/volume-splitter.spec.ts`, `tests/test_volume_history_busy_signal_contracts.py`, `docs/UI_SCENARIOS_GAP_ANALYSIS.md`, `docs/test_inventory/TEST_INVENTORY.json` and `.md`, `docs/volume_failure_feedback/PLANNING.md`.

Routing from [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md): the **Frontend (JS)** row ([`:30`](../ai_workflow/QUALITY_GATE.md#L30)) → the feature map ([`:126`](../ai_workflow/QUALITY_GATE.md#L126)) gives `volume-splitter.spec.ts` and `volume-progress.spec.ts`, plus manual smoke; the validation/error/empty-state/accessibility row ([`:129`](../ai_workflow/QUALITY_GATE.md#L129)) gives **all four** of `validation-boundary.spec.ts`, `error-handling.spec.ts`, `empty-states.spec.ts` and `accessibility.spec.ts` — **R5 corrected Plan v1, which took that row at half strength**; the **E2E spec** row ([`:33`](../ai_workflow/QUALITY_GATE.md#L33)) says run the spec; the **Product docs** row ([`:37`](../ai_workflow/QUALITY_GATE.md#L37)) requires nothing further for the two `docs/*.md` edits.

Run in this order:

1. **Regenerate the inventory** — `.venv/Scripts/python.exe scripts/generate_test_inventory.py`, then commit [`docs/test_inventory/`](../test_inventory/); verify `--check` exits 0. **Two pinned surfaces move, not one (R27)**: per-spec Playwright counts **and** `waitForTimeout` lines per file ([`QUALITY_GATE.md:61`](../ai_workflow/QUALITY_GATE.md#L61); the artifact records 82 across 14 files at [`TEST_INVENTORY.md:21`](../test_inventory/TEST_INVENTORY.md#L21)). §v2.8's `waitForResponse` pacing is intended to hold the second at **zero delta**, so a non-zero delta there is a signal that an arm slipped a hard wait in — check it, do not just regenerate past it. **Never hand-edit the artifact**, and confirm no untracked or gitignored `.md` sits in a globbed surface directory before regenerating.
2. **`npm run test:js`** — must report **13 files / 231 cases**, unchanged. The affirmative proof that U1 did not move the suite under qualification (§v2.1) and the collection-failure guard [`QUALITY_GATE.md:60`](../ai_workflow/QUALITY_GATE.md#L60) calls for.
3. **`npx tsc --noEmit`** — zero errors; the blocking half of the `Type Check` job.
4. **`npx playwright test e2e/volume-splitter.spec.ts --project=chromium --reporter=line`** — the whole spec, so the untouched success-path blocks and their `assertNoErrors()` run too.
5. **`npx playwright test e2e/volume-progress.spec.ts e2e/error-handling.spec.ts e2e/empty-states.spec.ts e2e/validation-boundary.spec.ts e2e/accessibility.spec.ts --project=chromium --reporter=line`** — the corrected union. `accessibility.spec.ts` is the proof for `s5`; `empty-states.spec.ts` is a second inherited console guard and covers the Reset path OD-3 touches.
6. **`.venv/Scripts/python.exe -m pytest tests/ -q`** — full suite. **The reason, corrected per R3**: nothing in QUALITY_GATE's Targeted-test derivation routes `e2e/**` or `static/js/**` to *any* pytest target, so full pytest is the **only** thing that catches the three files that read what U1 changes — [`test_volume_history_busy_signal_contracts.py`](../../tests/test_volume_history_busy_signal_contracts.py) (must be green **after** the `3 → 4` bump), [`test_css_cascade_contracts.py:500-503`](../../tests/test_css_cascade_contracts.py#L500-L503) (four literal `volume-splitter.js` substrings, none of which this change touches), and the `== 25` pin at [`test_playwright_shard_launcher_contracts.py:65-67`](../../tests/test_playwright_shard_launcher_contracts.py#L65-L67). Not "the suite is cheap enough".
7. **`.venv/Scripts/python.exe scripts/pyright_baseline_diff.py`** — **added per R3.** A `.py` is now in the diff and this gate is repo-wide, not path-scoped.
8. **Manual smoke** via the `run-hypertrophy-toolbox` skill: load `/volume_splitter`, calculate successfully, force a failure, and eyeball the region, the toast, Retry, and the return to normal on success. **Plus, per R14: run a one-off axe scan or devtools contrast reading against the failure state in BOTH themes and record the reading in the PR body as one-time evidence.** This is the only accessibility measurement the failure surface gets, because the axe matrix is deliberately not extended.
9. **The mutation matrix in §v2.9**, both directions, all nine rows, before the PR is marked ready.

**Not run, and why**: `/build-css` and the `visual.spec.ts` matrix — no `scss/**` or `static/css/**` file changes and no rest-state paint moves. That exclusion holds **only while no stylesheet rule is written for `volume-calculate-error`** (**R29**).

**Known-red awareness**: the only documented exception is [`e2e/program-backup.spec.ts:79`](../../e2e/program-backup.spec.ts#L79), which is outside U1's run set. **No known-red applies to this change — every red in U1's gate set is real.**

**Diff-time reviewers**: `/unslop` — `code-reviewer` **and** `unslop-reviewer`, both, because they catch disjoint failure modes.

**PR workflow**: create the PR, poll CI to zero pending, mark ready, then **stop**. Merge only on a separate explicit owner confirmation naming the PR.

### v2.12 Scope containment and rollback

**Containment.** Six changed paths. The production change is additive apart from the rewritten promise tail of one function and three single-line edits ([`:184`](../../static/js/modules/volume-splitter.js#L184), [`:633`](../../static/js/modules/volume-splitter.js#L633) and [`:867`](../../static/js/modules/volume-splitter.js#L867)). No exported symbol is added or renamed — the **five** helpers, two constants and **the `calculateRequestSeq` counter** are all module-private, so nothing outside this file can depend on them. No import is added. No template, stylesheet, route or service file is touched, so the change cannot reach the server, the schema or any calculation. The failure state is held **only in the DOM**, not in a module-level boolean, so it cannot desync from what the user sees; `calculateRequestSeq` is a request counter, not a state flag, and is never read to decide what to render.

**Rollback.** The production revert is single-file: `git checkout -- static/js/modules/volume-splitter.js` restores today's behavior completely, because every new surface is created at runtime and nothing is persisted. If the spec block also comes out, revert [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts), **restore the `== 3` pin**, and **re-run step 1** — a partial revert that leaves the committed inventory or the count pin describing tests that no longer exist reds two required checks. Work happens in an isolated worktree; if the suite reds and the fix is not obvious within one attempt, `git stash push -- <file>` immediately rather than stacking a second speculative change.

**Blast-radius checks before marking ready:**

- **BR-1** — `git diff --stat` shows exactly the **six artifacts / seven files** listed in §v2.11, and no eighth. The two counts differ because `docs/test_inventory/` contributes two files, `TEST_INVENTORY.json` and `TEST_INVENTORY.md`, which the Artifacts table carries on one row; `--stat` prints them as separate lines. In particular [`e2e/fixtures.ts`](../../e2e/fixtures.ts) is absent (**R26**) and [`ci.yml`](../../.github/workflows/ci.yml) is absent.
- **BR-2** — `npm run test:js` still prints 13 files / 231 cases.
- **BR-3** — the `waitForTimeout` count for `e2e/volume-splitter.spec.ts` in the regenerated inventory is unchanged from its committed value.
- **BR-4** — **criterion 10, moved here from the arm table per R12.** `git diff` shows no change at [`:191`](../../static/js/modules/volume-splitter.js#L191), [`:251`](../../static/js/modules/volume-splitter.js#L251), [`:288`](../../static/js/modules/volume-splitter.js#L288), [`:372`](../../static/js/modules/volume-splitter.js#L372) or [`:828`](../../static/js/modules/volume-splitter.js#L828), or in their `.catch` bodies. **This is an inspection, not a test, and the behavioral backstop is not uniform.** The existing tests at [`volume-splitter.spec.ts:289-386`](../../e2e/volume-splitter.spec.ts#L289-L386) cover site 4 (save), site 2 (load plan) and site 3 (delete). **Site 5's error row and site 6's activate/deactivate have no behavioral coverage at all** — for those two, criterion 10 rests on this `git diff` check alone. Stated rather than implied.

### v2.13 Owner decisions — all four settled at Gate 1, 2026-08-26

The `Council recommendation and evidence` column is left as the council wrote it, so the basis of each decision stays readable; the `Owner decision` column is what governs.

| ID | Decision | Council recommendation and evidence | Owner decision — 2026-08-26 |
|---|---|---|---|
| **OD-1** | Coverage routing versus the live JS-unit qualification window — options (i), (ii), (iii) in §v2.1. | **(i)** now, **(iii)** as the follow-up registered in §v2.14. The Artifacts table and §v2.11 are both written for (i). Unchanged by the council. | **GRANTED — option (i) now, with option (iii) as the REQUIRED follow-up.** U1 uses E2E coverage only during the live JS-unit qualification window. **No Vitest file or case is added or changed**, and the qualifying suite is preserved at exactly **13 files / 231 cases**. **T0** and the strict mark are preserved unless the documented restart condition genuinely occurs. **U1-FOLLOWUP-1 is retained in §v2.14**, which the owner accepts as the authoritative record of the follow-up for now; [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) is **not** edited by this PR. The implementation PR body **must link §v2.14 explicitly**. |
| **OD-2** | Q4 interpretation. The plan suppresses the repeat toast while a region stands **and** the attempt came from a slider (debounced or `change`), while always announcing on an explicit user command and whenever our toast content no longer stands. The owner chose (a) "replace rather than stack" and explicitly did not choose (c) "cooldown". Is this within (a)? | **Yes, keep it.** The alternative re-announces assertively about three times a second during a drag — and, per **R20**, on **every arrow keypress** for a keyboard user, which is where it hurts most. `a6` measures the behavior and `M8` kills it. | **RATIFIED as recommended — no separate owner ruling was required.** Repeat **slider-originated** announcements are suppressed while the same failure region **and** U1-owned toast content stand; **explicit user commands always announce**, and so does any failure at a moment when U1's toast no longer stands. That is within Q4's answer (a). |
| **OD-3** | **Owner-decided — re-routed by R21.** May criterion 6 be amended in scope, from "the inline region persists until the next successful calculation" to "…until the next successful calculation **or until the user resets**"? Plan v1 treated this as a plan-level judgement call; it is not. **A council cannot narrow a criterion the owner signed.** | **Recommend granting the amendment.** Reset's contract is a blank page, and a stale "could not calculate" banner over freshly zeroed sliders reproduces exactly the input-output mismatch U1 exists to remove. But the decision is the owner's. **Implementation is not blocked either way**: if declined, the single `exitCalculateFailureState()` line in `resetValues()` is dropped and nothing else changes. The `calculateRequestSeq` bump in the same function stays regardless — it belongs to **R1**, not to OD-3. | **GRANTED — the scoped amendment to criterion 6 stands.** Criterion 6 now reads *"The inline failure region persists until the next successful calculation **or until the user resets**."* The `exitCalculateFailureState()` call proposed for `resetValues()` in §v2.2 (G) is therefore **approved and ships**. The request-sequence increment in the same function **remains required independently**, for R1's race fix, and does not depend on this amendment. |
| **OD-4** | Criterion 11's mutation reading (§v2.0). Restore the `console.error`-only handler, or literally re-add `showErrorToast: false`? | **The former**, now on three grounds rather than one. (1) The wrapper's toast cannot carry a Retry action — [`fetch-wrapper.js:212-214`](../../static/js/modules/fetch-wrapper.js#L212-L214) passes only `{ requestId }` — so the literal reading collides with **Q3**. (2) **R18**: with the flag flipped, a request failure fires the wrapper's toast at [`:213`](../../static/js/modules/fetch-wrapper.js#L213) **and then** the page's own, i.e. two notifications per failure, which is not one logical failure state — it collides with **criterion 6** too. (3) **R18**: the literal reading cannot serve **criterion 12** at all, because the flag is never consulted on the post-2xx path. **And what the owner is accepting, stated per R19:** under this reading `showErrorToast: false` ships with **zero regression pressure**. If a later edit removed it, the wrapper's toast and the page's toast would both fire and the page's would win the single `#liveToast`, producing **no user-visible difference** — so `a1`, `a2`, `c1` and every other arm stay green. §0.2 measured that flag as the single load-bearing cause of user-visible silence, and nothing will guard it. The alternative was priced: a `MutationObserver` on `#toast-body` installed via `addInitScript`, asserting the flag by observing that only one body-write occurs per failure. **Declined** — it pins an implementation detail of a shared module U1 does not own, it would break the moment KI-011 is fixed and the button relocates, and it is the kind of oracle that outlives its own accuracy. **Recorded as accepted, not as coverage-neutral.** *(The council recorded one conditional Gate 0 reopening trigger against this row: had the owner required the literal reading, Q3 and criterion 11 could not both hold and Gate 0 would have had to be reopened. **It did not fire** — see the decision beside it.)* | **DECIDED — Plan v2's non-literal reading is ACCEPTED, and Gate 0 does NOT reopen.** Criterion 11 is satisfied by restoring the prior `console.error`-only request-failure handler (**M1**) and proving that the request-failure arm goes red. `showErrorToast: false` is **not** to be literally removed or re-added as the criterion-11 mutation, and it **stays in production**, so the page-specific toast can carry Retry and one failure does not produce two competing notifications. The owner **explicitly accepts the documented tradeoff**: that flag ships without direct regression pressure. The **rejected `MutationObserver` oracle stays rejected** and must not be added. |

### v2.14 Follow-up obligation — U1-FOLLOWUP-1, OPEN and recorded here by owner decision

R13's outstanding point, actioned — and **OD-1 made this subsection the obligation's authoritative record**:

> **U1-FOLLOWUP-1 — Vitest unit coverage for the calculate failure helpers.** **OD-1 resolved to option (i), with (iii) as the required follow-up** (owner, 2026-08-26), so the **five** helpers added by §v2.2 (C)–(F) and (J) ship with **browser-level coverage only**. A follow-up packet must add `static/js/modules/__tests__/volume-splitter.test.js` covering the region's idempotence, the `forceAnnounce || !standing || !ourToastContentStands()` condition, the sequence guard, and the shared probe. **It must not land before `2026-09-05T17:59:26Z`**, the strict mark in [`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md) §6.5, because doing so restarts the qualification window under the operative "changed no JS test case" rule (§v2.1). **Status: OPEN.** The owner **accepts this subsection as the authoritative record** of the obligation for now, so [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) is not edited here (**OD-1**). Filing it there as its own packet in §4 or §7 remains an open owner option, not a precondition.

The implementation PR body **must link §v2.14 explicitly**, so the obligation is discoverable from the merge commit rather than only from a planning document nobody re-opens.

### Sequence

1. **Confirm that this signed planning PR has merged.** OD-1, OD-3 and OD-4 are decided and OD-2's reading is ratified (§v2.13), and Gate 1 is signed — but implementation is authorized only once this document is on `main`. Re-read §v2.13 before step 8: the mutation matrix runs under OD-4's accepted non-literal reading, and `showErrorToast: false` is never the mutation.
2. Add the three module-private symbols; rewrite the promise tail of `calculateVolume()` with the sequence guard and the two independent failure sites, retaining a diagnostic `console.error` at each.
3. Add the five helpers, including the shared `ourToastContentStands()` probe (§v2.2 (J)); add **both** `resetValues()` lines — the `exitCalculateFailureState()` one ships, because **OD-3 was granted**; pass `forceAnnounce: false` from `scheduleCalculate()` and from the slider `change` listener.
4. Bump the count pin at [`test_volume_history_busy_signal_contracts.py:110`](../../tests/test_volume_history_busy_signal_contracts.py#L110) from `3` to `4`.
5. Add the new `test.describe` block: `a1`–`a6`, `b1`, `c1`–`c2`, `s1`–`s3`, `s6`, with the allow-one console posture, the specified assertion ordering and `waitForResponse` pacing.
6. Add the `KI-012` row to [`UI_SCENARIOS_GAP_ANALYSIS.md`](../UI_SCENARIOS_GAP_ANALYSIS.md).
7. Run §v2.11 steps 1–7 and get them green.
8. Run the §v2.9 mutation matrix — all nine rows, both directions — and record the observed result for every row against its expectation. **A row that does not red as predicted is a defect in the arm, not a pass.**
9. Manual smoke including the dual-theme a11y reading (§v2.11 step 8); record it in the PR body.
10. Run the BR-1 through BR-4 blast-radius checks.
11. `/unslop` — `code-reviewer` and `unslop-reviewer`. Then open the PR, poll CI to zero pending, mark ready, and **stop**.

### Expected gates

*Proposed in Plan v1 by the `product-manager`, corrected here by `test-strategist` findings F1, F3 and F11.*

- **pytest**: full suite — `.venv/Scripts/python.exe -m pytest tests/ -q`. Named specifically, because no path glob routes to them: [`tests/test_volume_history_busy_signal_contracts.py`](../../tests/test_volume_history_busy_signal_contracts.py) (green only **after** the `3 → 4` bump), [`tests/test_css_cascade_contracts.py`](../../tests/test_css_cascade_contracts.py) (four literal `volume-splitter.js` substrings at [`:500-503`](../../tests/test_css_cascade_contracts.py#L500-L503)), and [`tests/test_playwright_shard_launcher_contracts.py`](../../tests/test_playwright_shard_launcher_contracts.py) (`== 25` at [`:65-67`](../../tests/test_playwright_shard_launcher_contracts.py#L65-L67)).
- **e2e**: [`e2e/volume-splitter.spec.ts`](../../e2e/volume-splitter.spec.ts) (whole spec), [`e2e/volume-progress.spec.ts`](../../e2e/volume-progress.spec.ts), [`e2e/error-handling.spec.ts`](../../e2e/error-handling.spec.ts), [`e2e/empty-states.spec.ts`](../../e2e/empty-states.spec.ts), [`e2e/validation-boundary.spec.ts`](../../e2e/validation-boundary.spec.ts), [`e2e/accessibility.spec.ts`](../../e2e/accessibility.spec.ts).
- **js-unit**: `npm run test:js` — asserted **unchanged** at 13 files / 231 cases. An anti-drift gate on the qualification window, not a coverage gate.
- **other**: `scripts/generate_test_inventory.py` plus `--check`; `npx tsc --noEmit`; `scripts/pyright_baseline_diff.py`; manual runtime smoke including the one-off dual-theme a11y reading; the §v2.9 mutation matrix, all nine rows, both directions; blast-radius checks BR-1 to BR-4. **Not** `/build-css`, **not** the `visual.spec.ts` matrix.

---

## Sign-off

- [x] Gate 0 complete when required by planning size; otherwise marked not applicable. **Gate 0 SIGNED 2026-08-25 — see the Section 0 sign-off above.**
- [x] Every finding has a disposition. **See the response matrix — 30 rows, none deferred.**
- [x] Agent provenance complete — both `product-manager` IDs, same-PM-resumed yes/no, the three reviewer IDs, and an evidence-gap line (or `none`). **All five IDs stamped as supplied; same PM resumed = `yes`; evidence gap = `none`.**
- [x] User approved Plan v2.
- [x] Ready to implement — **but not yet authorized: proceed to code only once this PR is on `main`**, then `/unslop` or `/verify-and-polish` for the diff-time gate. See the GATE 1 block below.

### GATE 1 — SIGNED 2026-08-26

**The owner approved Plan v2 on 2026-08-26.** All four decisions are settled in §v2.13; the dispositions
are restated here so the signature reads without the table:

- **OD-1 — GRANTED: option (i) now, with option (iii) as the REQUIRED follow-up.** U1 uses E2E coverage only
  during the live JS-unit qualification window. **No Vitest file or case is added or changed**, the qualifying
  suite is preserved at exactly **13 files / 231 cases**, and **T0** and the strict mark are preserved unless the
  documented restart condition genuinely occurs. **U1-FOLLOWUP-1 stays open in §v2.14**, which the owner accepts
  as its authoritative record for now, and the implementation PR body **must link §v2.14 explicitly**.
- **OD-2 — RATIFIED as Plan v2 recommended**, with no separate ruling required. Repeat slider-originated
  announcements are suppressed while the same failure region **and** U1-owned toast content stand; explicit user
  commands always announce, and so does any failure at a moment when U1's toast no longer stands.
- **OD-3 — GRANTED.** Criterion 6 is amended in scope to *"The inline failure region persists until the next
  successful calculation **or until the user resets**."* The `exitCalculateFailureState()` call in `resetValues()`
  ships. The request-sequence increment in the same function remains required **independently**, for R1's race fix.
- **OD-4 — DECIDED: Plan v2's non-literal mutation reading is ACCEPTED, and Gate 0 does NOT reopen.** Criterion 11
  is satisfied by restoring the prior `console.error`-only request-failure handler and proving the request-failure
  arm goes red. `showErrorToast: false` is not removed or re-added as the criterion-11 mutation and **stays in
  production**, so the page-specific toast can carry Retry and one failure does not raise two competing
  notifications. The owner **explicitly accepts** that this flag ships without direct regression pressure, and the
  **rejected `MutationObserver` oracle stays rejected**.

**Implementation becomes authorized only after this signed planning PR merges successfully.** Signing is not the
authorization; the merge is. Until `docs/u1-gate1-plan` is on `main`, no production code, no test code, no change
to [`volume-splitter.js`](../../static/js/modules/volume-splitter.js) and no edit to
[`test_volume_history_busy_signal_contracts.py`](../../tests/test_volume_history_busy_signal_contracts.py) is
authorized. Once that merge lands, what is authorized is exactly Plan v2 — the six changed paths in the Artifacts
table, the gate set in §v2.11, the nine-row mutation matrix in §v2.9 run in both directions, and nothing else.

**What this signing leaves stale elsewhere.**
[`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4's `**Status:** Execute — needs its own Gate 0
and Gate 1` line at [`:109`](../OPEN_WORK_EXECUTION_PLAN.md#L109) lost its first half when Gate 0 was signed and
loses its second half now, so the whole line is stale; §4's premise sentence stays falsified by §0.1. **A third
thing is stale that Section 0 could not foresee**: its *Out of scope* bullet prescribes the repair *"reduce the
§4 Status line to 'needs its own Gate 1'"*, and writing that today would put a fresh falsehood on `main` — U1 now
owes neither gate. **None of the three is repaired here.** The first two live in a file this PR is directed
not to edit, and it did not. The third sits inside signed Section 0, which this signing may not rewrite — its
only permitted additions were the two OD-3 pointers — so the spent prescription is recorded here instead of
annotated there. All three remain owner action owed. §8's Gate column at
[`:509-512`](../OPEN_WORK_EXECUTION_PLAN.md#L509-L512) and §10's *Gates it owes* table at
[`:539-541`](../OPEN_WORK_EXECUTION_PLAN.md#L539-L541) survive untouched, because both are framed as the gates a
packet *owes* rather than gates it has passed.

### Implementation status — 2026-08-26

**Plan v2 is IMPLEMENTED as written.** The signed planning PR
[#422](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/422) merged as squash commit
`1243728` on 2026-08-25, which is the precondition the Gate 1 block above names, so the
*“Ready to implement — but not yet authorized”* checkbox and the *“no production code, no test
code”* paragraph beside it are both **SPENT**. Nothing above is rewritten; the four owner
decisions govern exactly as recorded in §v2.13.

**The implementation diff carries SEVEN artifact paths / EIGHT files, and the eighth is not
scope creep.** §v2.1's Artifacts table and §v2.12's **BR-1** both say six artifacts / seven files,
and that count still governs the **functional** blast radius — it is what BR-1 is checked against
and it did not move. The extra path is
[`testing_phase3/STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md), added under a
separately authorized operational-documentation exception to carry **ledger row 11** — the
`main` `js-unit` result that #422's own merge produced and could not record. §13.0's LIVE block is
extended **in place** with row 11, its counters, its spent clauses and its carrier-debt wording,
plus the one counter annotation that block itself planted in the superseded post-#414 block above
it — the same in-place repair its three earlier extensions each made. **Nothing outside §13.0 is
edited**, which is a statement about the diff and **not** a claim that nothing outside §13.0 is
left stale; what is left stale is listed under *Debt this diff creates* below. A ledger-only PR
was rejected because it would mint a twelfth row and owe a thirteenth without end. **No ninth file
is authorized.**

**The qualification window is untouched, and that was measured rather than assumed.** U1 changes
the production JS tree — `static/js`'s tree hash moves off
`815ca75c109c93c0f914f36d0de24ba46a89bc3d` — but the operative restart rule is §v2.1's
*“changed no JS test case”*, not *“changed no JS”*. Under **OD-1** option (i) this PR adds no file
under `static/js/modules/__tests__/`, changes no existing Vitest case, leaves `vitest.config.js` at
blob `c16ca428f7478708d8dd96a20ebcb86f98a8b935` and leaves the collection mechanism alone, so
`npm run test:js` still reports **13 files / 231 cases**. **T0 stays `2026-08-22T17:59:26Z` and the
strict mark stays `2026-09-05T17:59:26Z`.**

**The §v2.9 mutation matrix ran in both directions, all nine rows.** Checkpoint commit
`cb52edd`; `volume-splitter.js` sha256 `ed6563c2…` before and after every row, restored with
`git checkout --` and never by retyping. **Every predicted red was observed.** Two rows red
*more* arms than predicted, which is over-detection rather than a defect in an arm, and both are
explained rather than waved through:

| Row | Predicted red | Observed red | Note |
|---|---|---|---|
| **M1** | `a1`–`a6`, `c1`, `c2`, `s2`, `s3`; `s6` mirror case only | `a1`–`a6`, `c1`, `c2`, `s2`, `s3`, `s6` | As predicted. `b1` and `s1` stayed **green**, so the isolation claim rests on `b1` alone exactly as §v2.9 says. `s6` is one test carrying both cases, so its mirror failing reds the whole test. |
| **M2** | `b1` | `b1` | Isolation in the other direction; every other arm green. |
| **M3** | `a1`, `a2`, `a5`, `b1` | `a1`, `a2`, `a5`, `b1`, **`s6`** | `s6`'s mirror asserts `#results-body tr` count 0 after the fast failure, which `clearResults()` is what delivers. |
| **M4** | `c2` | `c2` | |
| **M5** | `s2` | `s2` | |
| **M6** | `a3` | `a3`, **`a6`** | Measured, not inferred: deleting the early return `prepend`s a **second** `#volume-calculate-error` rather than replacing the first, so `a6`'s closing `expect(region).toBeVisible()` resolves to two nodes and fails on the ambiguous match. |
| **M7** | `s3` | `s3` | |
| **M8** | `a6` | `a6` | |
| **M9** | `s6` | `s6` | |

**Three coverage gaps are recorded rather than closed, because closing any of them would add an
arm or a mutation row beyond the ones §v2.8 and §v2.9 enumerate.** They were found by
`code-reviewer` at diff time and are stated here so a later session does not have to re-derive
them:

1. **`resetValues()`'s two added lines have no arm and no mutation row.** Deleting both
   `calculateRequestSeq += 1;` and `exitCalculateFailureState();` leaves all thirteen arms green.
   **OD-3** is the one criterion the owner amended at Gate 1, and the behaviour it authorises is
   therefore unmeasured; R1's reset-race bump likewise. An arm would be four lines — drive a 500,
   assert the region, click `#reset-volume`, assert count 0.
2. **The third disjunct `|| !ourToastContentStands()` is unmeasured.** **M8** replaces the whole
   condition, so `a6` reds; deleting only that disjunct keeps every arm green, because no arm puts
   an unrelated toast over a standing region. **R16**'s KI-011 extension is prose-only.
3. **The early return in `dismissCalculateFailureToast()` is unmeasured.** Removing it makes every
   success hide `#liveToast` unconditionally and nothing reds, so **R4**'s "never dismiss an
   unrelated toast" property is prose-only too.

**Two structural notes, neither a deviation.** (a) §v2.2 (G)'s claim that the sequence bump means a
failure "cannot repaint a failure region over a deliberately blanked page" holds for requests
already **in flight**; a debounce timer armed immediately before Reset still fires ~300 ms later
with a fresh, current sequence. Cancelling it would change the debounce and call sequence, which
criterion 9 forbids, so the behaviour is left as-is. (b) §v2.2 (B) records the inner-catch
double-fire edge; the symmetric edge exists on the success side, where a throw from
`exitCalculateFailureState()` would reach the outer `.catch` with a still-current sequence and
paint failure over fresh results. The only global that helper touches is `bootstrap`, now guarded
with the `typeof` form this file already uses in `initDeleteModal()`.

**Debt this diff creates in files it is not authorized to touch, recorded not repaired.** U1
shifts every `volume-splitter.js` line anchor by **+119** (and by +122 past the slider comment) and
adds a second caller of `toast.js`'s action button. That falsifies, in files outside the eight:
[`DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md) row 9, whose *"silently swallows"* symptom
and `:131` / `:136-137` anchors are both spent — already booked under §v2.1 *Out*;
[`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4's `:131` / `:136` anchors —
also already booked; and, inside
[`STEP12_JS_UNIT_GATE0.md`](../testing_phase3/STEP12_JS_UNIT_GATE0.md), **§10.7-R10**'s
*"Reachable inside its own only caller"* with three moved anchors, and **§10.11**'s
*"Still exactly **one** caller repo-wide"*, which is now two. The STEP12 exception this PR uses is
scoped to §13.0's LIVE ledger block, so neither STEP12 site is edited here. **All four remain owner
action owed.**

**U1-FOLLOWUP-1 (§v2.14) remains OPEN**, and the implementation PR body links this subsection and
§v2.14 explicitly, as **OD-1** requires.

---

## See also

- [`.claude/commands/council-plan.md`](../../.claude/commands/council-plan.md) — how to run the council.
- [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) — change-type → required tests/reviewers.
- [`PLAN_REVIEW_TEMPLATE.md`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md) — the shell this document follows.
