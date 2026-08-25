# Plan Review — Packet U1: Volume calculation failure feedback

*Section 0 only. Plan v1, the council response matrix and Plan v2 are Gate 1 work and are deliberately absent — see [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4, whose closing blockquote records that U2's lighter requirement is not a precedent U1 may borrow to skip Gate 0, and §8, which records that U1 owes both gates and that no roadmap-level approval covers U1–U3 jointly.*

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
