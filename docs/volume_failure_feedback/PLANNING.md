# Plan Review — Packet U1: Volume calculation failure feedback

*Section 0 only. Plan v1, the council response matrix and Plan v2 are Gate 1 work and are deliberately absent — see [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4, whose closing blockquote records that U2's lighter requirement is not a precedent U1 may borrow to skip Gate 0, and §8, which records that U1 owes both gates and that no roadmap-level approval covers U1–U3 jointly.*

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

**Acceptance criteria**

1. Given the Volume Splitter page has loaded and a previous calculation succeeded, when a subsequent `POST /api/calculate_volume` returns HTTP 500, then a visible error message is presented to the user identifying that the volume calculation failed.
2. Given the same failure, when the message is presented, then it is announced to assistive technology without the user moving focus, and focus is not taken from the control the user is operating.
3. Given the same failure, when the message is presented, then the previously calculated results are no longer presented as current, by the disposition the owner selects in Q1.
4. Given a failure on the mode-switch or load-plan path, when the sliders have already been rebuilt for the new mode, then the results and suggestions computed for the previous mode are not left presented as belonging to the new one.
5. Given a failure, when the user takes the retry action defined by the owner's answer to Q3, then a fresh `POST /api/calculate_volume` is issued and, on success, the page returns to its normal successful state with the failure feedback removed.
6. Given a sustained server fault, when the user drags a slider and the debounced calculation fails repeatedly, then failure feedback follows the rule the owner selects in Q4.
7. Given the first calculation after page load fails, when the results sections have never been populated, then the outcome is the one the owner selects in Q6, and the empty results sections are not revealed empty either way.
8. Given a successful `POST /api/calculate_volume`, when the response is rendered, then the results table, suggestions, per-muscle status classes, value-pill modifiers, server-supplied ranges and slider track paint are what they are today, under the reading of "unchanged" the owner selects in Q5.
9. Given any slider interaction, when the user drags, releases, switches mode, resets, or loads a saved plan, then the debounce interval, the request payload and the call sequence are unchanged from today.
10. Given the shipped change, when the five neighbouring call sites at lines 191, 251, 288, 372 and 828 are exercised, then their behavior is unchanged.
11. Given the repaired code, when a regression arm restores the request-failure suppression at the calculate call, then that arm fails.
12. Given the repaired code, when a regression arm restores the post-2xx suppression at the calculate call, then that arm fails.

Criteria 11 and 12 are drafted on the corrected framing in §0.1. If Q0 is answered by routing the discrepancy back through [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4 first, both are re-derived after that correction lands.

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
- Packets U2, U3, R1, R2, R3, V1, Track P1 and Track D1; Dependabot PRs #415 and #416; branch protection and repository settings.

**Assumptions made**

- ⚠️ **The existing toast is assumed to be the intended vehicle**, because five of the six sites in this file already use it. The owner may prefer an inline-only region; Q2 asks.
- ⚠️ **"Accessible" is read as an `aria-live` announcement without a focus move.** The existing toast container already carries `aria-live="polite"` on the wrapper and `role="alert"` with `aria-live="assertive"` on `#liveToast` ([`base.html:236-248`](../../templates/base.html#L236-L248)), so a toast-based answer inherits an announcement today. Whether that inherited behavior is sufficient, or whether U1 owes an explicit announcement test, is not assumed.
- ⚠️ **The failure is assumed to be user-recoverable rather than fatal**, i.e. the page keeps working and recalculates on the next interaction. Whether an explicit retry affordance is required is not assumed; Q3 asks.
- ⚠️ **No new i18n or copy-review process is assumed.** The message is assumed to be plain English in the register the file already uses. That register is not quite uniform: four of the five existing messages end "Please try again." ([`:217`](../../static/js/modules/volume-splitter.js#L217), [`:263`](../../static/js/modules/volume-splitter.js#L263), [`:318`](../../static/js/modules/volume-splitter.js#L318), [`:439`](../../static/js/modules/volume-splitter.js#L439)); the activate/deactivate pair at [`:838`](../../static/js/modules/volume-splitter.js#L838) omits it.

**Open questions for the user**

These are blocking. Gate 0 is not signed until each is answered.

- **Q0 — the packet's premise is wrong in one direction; confirm the corrected framing.** §4 U1 says each suppression is independently sufficient. Measured (§0.1), only `showErrorToast: false` is sufficient for user-visible silence; the `.catch` is sufficient only for the post-2xx failure class. **Do you accept the corrected framing, or do you want the discrepancy resolved in [`OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md) §4 first?** This session did not edit §4.
- **Q1 — stale results: clear, or mark stale?** Three defensible answers: (a) the results and suggestions are cleared on failure, so the page shows nothing rather than something wrong; (b) they stay and are visibly marked as the previous result; (c) they are left untouched and the failure message alone carries the signal. Option (c) does not satisfy criteria 3 and 4 as written. **(a) is the smaller change and the safer default; (b) preserves more user context. Which do you want?**
- **Q2 — toast, inline region, or both?** A toast alone auto-dismisses after 3 s ([`toast.js:33`](../../static/js/modules/toast.js#L33)) and leaves no trace next to a stale table; an inline region persists but is easier to miss. Site 5 in §0.2 is the in-repository precedent for doing both. **Which surface, or both?**
- **Q3 — retry.** Is the existing Calculate button sufficient as the retry path, or must the failure feedback carry its own retry affordance? [`toast.js`](../../static/js/modules/toast.js) supports an inline action button (`options.action`), already used at [`volume-splitter.js:299-306`](../../static/js/modules/volume-splitter.js#L299-L306). **No automatic retry is proposed**: `retries` is `0` for `POST` today and changing it would alter request behavior on the success path.
- **Q4 — repeated failures: deduplicate or repeat?** During a slider drag against a down server, the debounced path can fail every 300 ms. Options: (a) one notification that persists until the next success, replacing rather than stacking; (b) a fresh notification per failure; (c) suppress subsequent notifications for a cooldown window. **Recommendation: (a).**
- **Q5 — how literally should "unchanged success path" in criterion 8 be read?** The strict reading is that no new element, class or attribute appears on the success path at all; the weaker reading is that nothing user-perceivable changes, which would permit a permanently-present region that is empty on success. **Which do you mean?**
- **Q6 — does U1 own the first-load case?** If the very first calculation of a page load fails, should the user be told, or should U1 stay silent when nothing has ever been calculated? Staying silent reduces scope but leaves a real failure unreported.

### Section 0 sign-off — GATE 0

- [ ] User confirms the acceptance criteria match intent.
- [ ] User reviewed the assumptions and corrected or accepted each one.
- [ ] Blocking questions Q0–Q6 are answered.

**Gate 0 is NOT signed. No implementation, no test authoring, and no Gate 1 planning may begin until it is.** U1 owes a separate Gate 1 — a council-reviewed plan — after this section is approved.
