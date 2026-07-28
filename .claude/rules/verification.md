---
paths:
  - "static/css/**/*.css"
  - "scss/**/*.scss"
  - "scripts/css_audit/**/*.py"
  - "scripts/css_audit/**/*.mjs"
  - "e2e/visual.spec.ts"
  - "e2e/visual-baseline-thumbnails.spec.ts"
  - "e2e/dark-mode.spec.ts"
---

# Verification and evidence guide

Rules for any claim of the form "this rule is dead", "this change is
pixel-neutral", or "this declaration never wins".

## Division of ownership
**This file owns the durable method** — the invariants below hold for any CSS
arc and outlive the packet that discovered them.

**`docs/css_phase4_wp4_4/PLANNING.md` owns the arc.** Its §2b method table
(M1–M12) and §2 standing constraints (G1–G11) bind the WP4.4 packets, carry the
owner rulings, and record which packet paid for each rule. When that arc closes,
its arc-specific constraints retire with it; these do not.

Where both describe the same obligation, the plan's wording governs inside the
arc. Do not copy the M/G table here.

## Validate the oracle before trusting the oracle
A measurement script is not evidence until it has passed a control:
1. a **known-live** case it must report live,
2. a **known-dead** case it must report dead,
3. a **same-CSS control run** — identical CSS on both sides, which must report
   zero differing records.

The same-CSS control is a **validity precondition, not evidence of deadness**.
It tells you the harness is measuring your change rather than noise; it says
nothing about any particular declaration. A control that reports differences
invalidates every result from that run. WP4.3i-dead's control produced 52
differing records and correctly shrank the packet from 24 declarations to 14.

Report raw control output alongside the result. A result without its control is
not reportable.

**Choose control cases adversarially.** A case table built from the same
assumption as the implementation will pass and prove nothing — the first version
of `.claude/hooks/guard-destructive-command.ps1` passed 15 hand-picked cases and
still missed eight real bypasses, because the cases were derived from the
patterns rather than from the threat. Enumerate what *should* be caught first,
independently of how the check works.

## Deadness needs converging evidence, not one sweep
A sentinel sweep **alone over-reports deadness**. A deletion claim needs the
sweep **and** a rest-state differential, each capable of falsifying the other,
with the same-CSS control passing. A sweep reporting that 40 of 97 literals
never render is a hypothesis, not a finding.

Declarations reachable only through an interaction state (`:hover`, `:focus`,
`:active`) or a JS-applied class must be proven under that state — and that
proof is itself unreliable until the control reaches zero, because those states
animate. Declare interaction-state scope up front or defer it.

Declarations inside `@media` blocks require a capture taken under that block's
own condition — reduced-motion, print, and each breakpoint.

## Sentinels and transitions
Suppress transitions before applying, reading **and** removing a sentinel. A
sentinel written to a transitioned property reads back its pre-sentinel value
for the whole transition duration, so `getComputedStyle` reports "no effect" on
an element the sentinel reached perfectly. Inline `!important` does not help —
the lag is in the computed value, not the cascade. The release is symmetric:
drop the sentinel while transitions are still suppressed. `header` and `select`
carry `transition: all 0.3s` and will produce this false negative.

A probe that changes nothing proves nothing: assert per record that the sentinel
took effect. `var()`-bearing shorthands are invisible to longhand CSSOM queries.

## Visual capture
- Run the visual pipeline with `PW_VISUAL_SEED=1` (selected in
  `playwright.config.ts`); without it the seeded DB is absent and the run fails
  for reasons unrelated to the change.
- Scope every capture to the element under test. The full-page pixel oracle is
  unusable on animated-navbar routes.
- The animated-logo diff is a **band, not a constant**, and it can exceed the
  configured `maxDiffPixels`, so it presents as a real snapshot failure. Never
  assert an exact pixel count for it. Read the current threshold and observed
  range from the active arc's plan rather than from this file — those numbers
  are baseline state and go stale.

## Reuse the committed harness
`scripts/css_audit/` holds the reviewed tooling from WP4.4-a — `measure.py`,
`specificity.py`, `resolution_check.py`, `runtime_probe.mjs`,
`stylelint_surfaces.mjs`, `emit_baseline.py`. Extend these rather than writing a
throwaway parser. Specificity in particular must handle `:is()`/`:where()`/
`:not()`/`:has()`, must not naively comma-split, and must implement `@layer`
ordering plus the `!important` inversion.

## Windows scripting hazards
These have each corrupted an analysis run:
- Normalize CRLF before any line-offset or character-offset math.
- Avoid bash heredocs; write the script to the scratchpad with `Write` and run
  the file.
- Quote every PowerShell path; junctions and worktree paths break unquoted.
- Never use `nth-child` position or re-serialized CSS text for rule identity —
  re-serialization is not byte-preserving. Match on selector plus source offset.
- A comment stripper used for scanning must be length-preserving, or every
  offset after the first comment is wrong.

## Parallelism
Only parallelize packets whose file sets are disjoint. CSS packets that touch
the same bundle run **serially** — state that rather than re-litigating it each
session.
