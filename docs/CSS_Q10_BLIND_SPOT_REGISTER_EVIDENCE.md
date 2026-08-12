# Q10 — the CSS visual-oracle blind-spot register, repaired

**Packet:** Q10, standalone. Authorized independently of the terminated theme-dark P3 arc.
**Scope:** test/evidence infrastructure only. No product rendering changes — `e2e/visual-helpers.ts`,
every stylesheet under `static/css/`, every template and every committed screenshot are **read, never
written**.

Sized (not implemented) at P3-a0 in
[`CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md`](CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md) §9. This document
records what the repair actually measured, which differs from that sizing in every count.

---

## 1. The defect

`measure.verify_blind_spots()` compared the curated register against `e2e/visual-helpers.ts` in **one
direction only**: for each register entry, it asked whether that entry's `helperEvidence` string still
occurred *somewhere* in the helper file. Two consequences, both live:

**It could not see an addition.** Nothing asked what the helper contained that the register did not, so
a neutralizer added to `prepareForScreenshot()` was invisible. `tests/test_css_wp4_4_a_baseline_contracts.py`
then pinned only `len(register) == len(measure.BLIND_SPOT_REGISTER)`, which an addition does not move
either.

**Its one direction was satisfiable by the wrong line.** `helperEvidence` was a plain substring search
over the whole file, not a selective match. The backdrop-filter entry cited
`backdrop-filter: none !important;` and the helper's own `-webkit-backdrop-filter: none !important;`
line *contains* that string, so deleting the property the entry described left the check green.

### The drift that escaped, measured

Two neutralizing rule blocks reached `prepareForScreenshot()` after the register was written, and full
pytest stayed green through both:

| Block | Declarations | Why the old check missed it |
|---|---|---|
| `html[data-theme='dark'] .summary-header` | `background`, `border-radius`, `box-shadow` | An added block moves neither an evidence search nor the register length. |
| `[data-testid="exercise-table"] thead th, … tr > :first-child, [data-testid="workout-log-table"] …` | `position: static` | Same, and `position` was not in the register's property vocabulary at all. |

A third, weaker defect was structural rather than escaped: the sizing instrument's substring matching
bound the register's form-control entry to the dark `.summary-header` **and** `[data-visual-accent]`
blocks, purely because all three contain the literal `box-shadow: none !important;`. Three unrelated
rules shared one identity.

---

## 2. Current-main census — re-derived, not inherited

Measured at `ae37365` against unmodified `e2e/visual-helpers.ts`. P3-a0 §9.1's table
(18 blocks / 19 unmapped declarations) and the historical audit's estimate are both **stale**; the
figures below supersede them.

| Channel | Blocks | Declarations |
|---|---|---|
| Injected `addStyleTag()` stylesheet — neutralizers | 18 | 45 |
| Injected `addStyleTag()` stylesheet — support tokens (`--visual-surface-*`) | 2 | 4 |
| Post-load inline `element.style.setProperty()` | 1 | 3 |
| **Total** | **21** | **52** |

The inline stage is a genuinely separate channel, not a restatement of the stylesheet: it applies
inline `!important`, which outranks every author rule, *after* the page has finished running its own
scripts. A stylesheet-only extractor does not see it.

### Register coverage, before and after

| | Before | After |
|---|---|---|
| Register entries | 6 | 22 |
| Registered declarations | 20 (as prose property lists) | 52 (as machine records) |
| Helper declarations with no registration | not derivable | 0 |
| Register records the helper does not apply | not derivable | 0 |
| Verification directions | 1 | 2 |

---

## 3. The repaired design

### Register entry shape

Each entry keeps its curated half — a machine cannot say which packet family a neutralizer blinds — and
gains a machine-verified half:

| Field | Kind | Purpose |
|---|---|---|
| `selector` | curated | human label / context, e.g. *form controls (post-load inline re-application)* |
| `why`, `neutralizedTo`, `blindsPackets`, `blindsSurfaces`, `helperEvidence` | curated | the reviewable statement of what the oracle cannot see |
| `stage` | machine | `stylesheet` or `inline` |
| `helperSelector` | machine | the normalized selector, exactly as the helper writes it |
| `classification` | machine | `neutralizer` or `support-token` |
| `declarations` | machine | `{property, value, important}` per declaration, in source order |
| `properties` | mirror | readable property list; verified to mirror `declarations` exactly, so it cannot rot into a claim of its own |

One entry is one `(stage, selector)` group. A block whose declarations blind different packet families
is split across several entries over the same selector — the `*, *::before, *::after` block stays two
entries (motion → **c**; backdrop-filter → **h/i/j**) exactly as the curation had it.

### Extraction

`measure.helper_rules()` derives the helper side from `prepareForScreenshot()` itself:

1. The function body is located by brace matching that skips string literals (backticks included) and
   both comment forms, so CSS braces inside the injected template never enter the count.
2. Exactly **one** `addStyleTag()` call is enumerated. A second is a parse failure, not a skipped rule.
3. The template literal is rejected if it interpolates (`${…}`) — its text would not be statically knowable.
4. Rule blocks are walked at depth 0. An at-rule prelude, a nested rule, an unparsable declaration, an
   empty block or stray text outside every block each raise `HelperParseError`.
5. The inline stage is read from each `querySelectorAll(…).forEach(…)` chain, requiring string-literal
   arguments throughout. Every `setProperty(` in the body must be reachable through an enumerated
   chain, or the count check fails closed.
6. Any other style channel inside the function — direct `element.style.<prop> =`, `cssText`,
   `setAttribute()`, CSSOM `insertRule()` — fails closed.

### Comparison

Identity is `(stage, normalizedSelector, property)`. `value`, `important` and `classification` are
compared on the matches. Failures are emitted for: a helper record with no register entry; a register
record the helper does not apply; a value / importance / classification mismatch; a duplicate signature
on either side; a `properties` mirror that has drifted; a `helperEvidence` citation absent from the
helper; and any `HelperParseError` at all.

Classification is derived, not asserted: a block whose declarations are **all** custom properties is a
support token, everything else is a neutralizer. So a *new* custom-property-only block is derived as
`support-token` and then fails as unregistered — custom properties are enumerated exactly, never
broadly ignored.

### Formatting independence

Selectors and values are whitespace-collapsed; comments are blanked length-preservingly; CRLF and CR
are normalized to LF before parsing. Line numbers are deliberately **not** part of any derived record —
a record carrying one would change every time a comment moved.

### Why `p3_ceiling.blind_spot_repair_sizing()` was not copied

Its matcher is the substring matcher named in §1: it associates `.summary-header` and
`[data-visual-accent]` with the unrelated form-control entry because all three contain
`box-shadow: none`. It stays in place, read-only, as the P3-a0 sizing instrument. Run against the
repaired register it now independently corroborates the result: **20 blocks, 18 fully mapped, 2 token
blocks, 0 unmapped, 0 partially mapped, 0 unmapped declarations.**

---

## 4. Repaired-state acceptance

| Claim | Measured |
|---|---|
| Injected stylesheet completely classified | 20 / 20 blocks |
| Neutralizing blocks | 18 |
| Explicit support-token blocks | 2 |
| Unmapped blocks | 0 |
| Partially mapped blocks | 0 |
| Inline `setProperty()` stage represented | 1 block, 3 declarations |
| `verify_blind_spots()` on unmodified `visual-helpers.ts` | `[]` |
| `register_rules() == helper_rules()` | true, 52 records |

---

## 5. Mutation matrix

Every case edits the helper **in memory**. The file on disk is never written.

| # | Mutation | Result | Named in the failure |
|---|---|---|---|
| 1 | add `.q10-unregistered { filter: none !important; }` | red | `.q10-unregistered` |
| 2 | add `opacity: 0 !important` to the registered `[data-visual-icon]` block | red | `opacity` |
| 3 | extend a registered selector to `[data-visual-icon], .q10-extra` | red | `.q10-extra` |
| 4 | delete `animation-duration: 0s !important;` | red (register → helper) | `animation-duration` |
| 5 | delete only the unprefixed `backdrop-filter`, keep `-webkit-` | red | `{ backdrop-filter:` |
| 6 | delete the dark `--visual-surface-*` block while the light one remains | red | `#090c16` |
| 7 | add `html[data-theme='sepia'] { --visual-surface-2: #fff; }` | red | `--visual-surface-2` |
| 8 | add an inline `setProperty('outline', 'none', 'important')` | red | `outline` |
| 9 | add a second `addStyleTag()` inside `prepareForScreenshot()` | red, fail-closed | `addStyleTag` |
| 10 | reword a comment, reindent, add blank lines, convert LF → CRLF | **green** | — |
| 11 | change one committed baseline entry at unchanged array length | red | exact-equality contract |
| 12 | add an unrelated `.q10-unrelated-shadow { box-shadow: none !important; }` | red, and **no** message mentions form controls | `.q10-unrelated-shadow` |

Three further fail-closed paths are covered: a changed value (`#273145` → `#111111`), a changed
importance (`display: none` → `display: none !important`), and an unenumerated style channel
(`element.style.cssText`).

Case 5 is the substring-shadowing repair stated as its own contract, and case 12 is the false-association
defect stated as its own contract. Both replace P3-a0 tests that required the defect to be present:
`test_the_shared_blind_spot_verifier_is_one_way` and
`test_the_blind_spot_evidence_string_for_backdrop_filter_is_substring_shadowed`. The guarantee each one
protected is preserved; only its sign changed.

---

## 6. The committed baseline

`docs/CSS_PHASE4_WP4_4_A_BASELINE.json` is patched in **one array only**. `oracleBlindSpots` goes from
6 entries to 22; every other top-level key — `sourceCommit`, `surfaces`, `totals`, `isFamily`,
`snapshotManifest`, `screenshotTolerances`, `contractAnchors`, `pinnedDeclarations` and the rest — is
byte- and value-identical.

Proved three ways rather than asserted:

1. The committed file was confirmed to be a canonical `json.dumps(indent=2, ensure_ascii=False)` render
   before anything was written, so re-dumping cannot move formatting outside the patched array.
2. After the patch, `[key for key in before if before[key] != after[key]] == ["oracleBlindSpots"]` over
   the parsed objects, with top-level key order unchanged.
3. Every hunk of `git diff -U0` falls inside the array's own line span (old 2221–2313, new 2221–2970).

`emit_baseline.py` was **not** run in write mode. A whole-file regeneration is the route P3-a0 §9.3
measured and rejected: it moves `sourceCommit`, `surfaces`, `totals` and `isFamily`, and the `isFamily`
movement reds `test_is_family_enumeration_is_complete_and_classified`.

The baseline pin is also strengthened. `test_oracle_blind_spot_register_matches_the_live_helper` now
asserts `register == json.loads(json.dumps(list(measure.BLIND_SPOT_REGISTER)))` — exact equality, not
equal length. Two tampered arrays that keep the committed entry count (one rewriting curated prose, one
rewriting a machine-verified value) are asserted to fail it.

---

## 7. What this packet does not do

- It does not reopen P3, implement P3-a1, or touch any theme-dark cleanup.
- It does not regenerate the WP4.4 baseline, edit `e2e/visual-helpers.ts`, or move a pixel. No
  Playwright, Stylelint or visual gate is engaged, because nothing they measure changed.
- `CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md` §8 still prints the original six-row register table and is
  now stale in its counts. Its adjacent claim — *"each entry is re-derived from `e2e/visual-helpers.ts`
  on every emit, so the register cannot drift from the file it describes"* — was false when written and
  is true as of this packet. Correcting that historical evidence document is outside this packet's
  authorized write scope and is left as follow-up.
- `p3_ceiling.blind_spot_repair_sizing()`'s docstring and its `verifyBlindSpotsDirection: "one-way"`
  field still describe the pre-repair verifier. `scripts/css_audit/p3_ceiling.py` is read-only here; no
  contract pins that string. Also follow-up.

---

## See also

- [`CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md`](CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md) §9 — the sizing this repair supersedes
- [`CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md`](CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md) §8 — the register as packet **a** shipped it
- `.claude/rules/verification.md` — "validate the oracle before trusting the oracle"
