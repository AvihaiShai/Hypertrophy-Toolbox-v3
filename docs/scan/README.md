# Codebase Grounding Scan — evidence, not backlog

> **These documents are historical evidence. They are not an active work queue, and nothing in
> them is authorized work.** `PHASE_02.md` through `PHASE_22.md` record a line-by-line grounding
> read taken on **2026-07-03** and merged on 2026-07-04 (PR #89, `59c03dd`). They are preserved
> so a later reader can see what was observed and when — not so a later session can pick items
> out of them and start working.

## What this set is

Twenty-one phase files, `PHASE_02.md` to `PHASE_22.md`. The scan ran **23** phases: phase 1
has no file of its own and is written up in [`../SCAN_FINDINGS.md`](../SCAN_FINDINGS.md), and
phase 23 is the synthesis, which is [`../SCAN_RECOMMENDATIONS.md`](../SCAN_RECOMMENDATIONS.md).
Progress is tracked in [`../SCAN_PROGRESS.md`](../SCAN_PROGRESS.md). Each phase file records
what a file does, its coupling, and anything that confirmed or contradicted the refactor plan
at the time.

## How to use it

1. **Treat every nomination as a hypothesis, never as a finding.** This is the rule
   [`../CSS_PHASE4_WP4_4_B_BASE_EVIDENCE.md`](../CSS_PHASE4_WP4_4_B_BASE_EVIDENCE.md) arrived at
   the hard way. Its §2 re-measured `PHASE_20.md`'s nominations for one file and found **two**
   of them false, both now pinned by contract — including a `@keyframes` rule the scan called
   dead that is in fact animated live from a different file, which would have broken had the
   nomination been acted on. (§2's own prose says *three*; its table carries three rows but
   the third states no scan claim at all — it is an M9 custom-property retention. Two is the
   count of falsified nominations.)
2. **Re-measure against current code before acting on anything here.** The scan's own citations
   have moved. Measured at `5ca4191`, the file lengths `PHASE_14.md` records in its opening
   paragraph are already wrong: `backup-center.js` is **1069** lines, not 1005;
   `volume-splitter.js` is **906**, not 912; `program-backup.js` is **152**, not 174. A
   `file:line` citation from 2026-07-03 should be assumed stale until re-derived.
3. **Active work is sequenced elsewhere.** It lives in
   [`../OPEN_WORK_EXECUTION_PLAN.md`](../OPEN_WORK_EXECUTION_PLAN.md), and current status lives
   in [`../MASTER_HANDOVER.md`](../MASTER_HANDOVER.md). Where a scan observation is still live,
   it has already been carried into one of those — or into
   [`../DUPLICATION_REGISTRY.md`](../DUPLICATION_REGISTRY.md), which cross-checked this scan
   against a fresh code read and records a disposition per instance.

## What has already been carried forward

The grounding scan's bug list A1–A12 is fully dispositioned and mapped to
`REFACTOR_PLAN.md` Track A and the WPB packets. The mapping is in
[`../LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md), which also warns that the
scan's `A`-numbering does **not** line up with Track A's. When citing an "A-number", always
name the source document.

## Retention

If one of these files is ever archived, use the criteria and procedure in
[`../ai_workflow/DOC_RETENTION.md`](../ai_workflow/DOC_RETENTION.md). That document records
**no disposition for this directory** — its assessed orphan list covers the
`CSS_PHASE4_WP4_3I_*` family plus three unrelated documents, and its pytest-pin note covers
the `CSS_PHASE4_WP4_4_*` family — near-identical names that document explicitly warns
against conflating. A scan file needs its own assessment, not an inherited one.
Do not delete these files to reduce a file count. Nothing here
is pytest-pinned: this set has no JSON siblings, and the only test citation is
`tests/test_css_wp4_4_base_contracts.py:24,122,137`, which names `PHASE_20.md` inside
docstrings only — so moving one reds nothing.
