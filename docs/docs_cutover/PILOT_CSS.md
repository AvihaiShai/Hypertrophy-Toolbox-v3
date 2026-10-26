# CSS evidence cutover pilot

Baseline: `c29ddf0740ecd9dd90e65424c37050c764504431` (after #651 and #652).
This record describes one proposed batch, not a merge receipt or a completed cutover.
See the [completion criteria and rules](README.md).

## Scope and disposition

Twenty related CSS evidence records: **13 KEEP, 1 SPLIT, 6 ARCHIVE**. KEEP is an
explicit retention decision, not an archive nomination. Its dated handoffs now
carry a historical-evidence notice; original technical bodies remain intact.

The six archive records describe shipped foundation, selector, token, shared-frame,
Backup and Body Composition packets. Their closeouts are recorded in
[`REFACTOR_PLAN.md`](../REFACTOR_PLAN.md), Phase 4 WP4.-1 through WP4.3b, and in the
[historical handover](../archive/2026/master-handover/CURRENT_STATE_HISTORY.md).
Their former next-packet handoffs are historical, not outstanding follow-ups.
Neither current `MASTER_HANDOVER.md` nor the current `OPEN_WORK_EXECUTION_PLAN.md`
names them as an open follow-up. Current CSS loading/ownership reference is
[`CSS_OWNERSHIP_MAP.md`](../CSS_OWNERSHIP_MAP.md); behavior remains governed by the
existing cascade and selector contracts. The revised retention rule, already on
main, applies; this PR introduces no age waiver.

The Session Summary SPLIT keeps all technical and measurement content, including
both deferred findings and the `Next action` anchor. Only the obsolete sequential
handoff is replaced. [#623/AUD-0386](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/623)
is its verified tracking home; no CSS cleanup is authorized. The original handoff
remains available at the pinned baseline commit.

| Source record | Action | Retained home / reason |
|---|---|---|
| `CSS_PHASE4_WP4_-1_EVIDENCE.md` | ARCHIVE | [CSS_PHASE4_WP4_-1_EVIDENCE.md](../archive/2026/css-foundation-route-cleanup/CSS_PHASE4_WP4_-1_EVIDENCE.md) — Complete historical packet; current loading reference is CSS_OWNERSHIP_MAP.md. |
| `CSS_PHASE4_WP4_0A_EVIDENCE.md` | ARCHIVE | [CSS_PHASE4_WP4_0A_EVIDENCE.md](../archive/2026/css-foundation-route-cleanup/CSS_PHASE4_WP4_0A_EVIDENCE.md) — Complete historical packet; current loading reference is CSS_OWNERSHIP_MAP.md. |
| `CSS_PHASE4_WP4_0_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_0_EVIDENCE.md](../CSS_PHASE4_WP4_0_EVIDENCE.md) — Retain the immutable known-red ledger as the provenance for later visual comparisons. |
| `CSS_PHASE4_WP4_1_EVIDENCE.md` | ARCHIVE | [CSS_PHASE4_WP4_1_EVIDENCE.md](../archive/2026/css-foundation-route-cleanup/CSS_PHASE4_WP4_1_EVIDENCE.md) — Complete historical packet; current loading reference is CSS_OWNERSHIP_MAP.md. |
| `CSS_PHASE4_WP4_2_EVIDENCE.md` | ARCHIVE | [CSS_PHASE4_WP4_2_EVIDENCE.md](../archive/2026/css-foundation-route-cleanup/CSS_PHASE4_WP4_2_EVIDENCE.md) — Complete historical packet; current loading reference is CSS_OWNERSHIP_MAP.md. |
| `CSS_PHASE4_WP4_3A_EVIDENCE.md` | ARCHIVE | [CSS_PHASE4_WP4_3A_EVIDENCE.md](../archive/2026/css-foundation-route-cleanup/CSS_PHASE4_WP4_3A_EVIDENCE.md) — Complete historical packet; current loading reference is CSS_OWNERSHIP_MAP.md. |
| `CSS_PHASE4_WP4_3B_EVIDENCE.md` | ARCHIVE | [CSS_PHASE4_WP4_3B_EVIDENCE.md](../archive/2026/css-foundation-route-cleanup/CSS_PHASE4_WP4_3B_EVIDENCE.md) — Complete historical packet; current loading reference is CSS_OWNERSHIP_MAP.md. |
| `CSS_PHASE4_WP4_3C_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3C_EVIDENCE.md](../CSS_PHASE4_WP4_3C_EVIDENCE.md) — Retain the Progression cascade/compositor diagnosis and exact-value ownership proof. |
| `CSS_PHASE4_WP4_3D_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3D_EVIDENCE.md](../CSS_PHASE4_WP4_3D_EVIDENCE.md) — Retain the Volume Splitter token, cascade and rendering contracts. |
| `CSS_PHASE4_WP4_3E_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3E_EVIDENCE.md](../CSS_PHASE4_WP4_3E_EVIDENCE.md) — Retain the Welcome token and rendering contracts; the old integration handoff is historical. |
| `CSS_PHASE4_WP4_3F_EVIDENCE.md` | SPLIT | [CSS_PHASE4_WP4_3F_EVIDENCE.md](../CSS_PHASE4_WP4_3F_EVIDENCE.md) — Keep all technical evidence and deferred findings; replace the obsolete sequential queue with the verified owning issue #623/AUD-0386 and preserve the old handoff in the pinned source. |
| `CSS_PHASE4_WP4_3G_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3G_EVIDENCE.md](../CSS_PHASE4_WP4_3G_EVIDENCE.md) — Retain the Weekly Summary ownership proof; it does not discharge the opposite-direction Session cleanup. |
| `CSS_PHASE4_WP4_3H_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3H_EVIDENCE.md](../CSS_PHASE4_WP4_3H_EVIDENCE.md) — Retain the Profile token extraction and intentional-keep contracts. |
| `CSS_PHASE4_WP4_3I_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3I_EVIDENCE.md](../CSS_PHASE4_WP4_3I_EVIDENCE.md) — Retain the Workout Plan topology and section-boundary evidence. |
| `CSS_PHASE4_WP4_3I_B_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3I_B_EVIDENCE.md](../CSS_PHASE4_WP4_3I_B_EVIDENCE.md) — Keep the WPDD ownership contract and the retention-policy reference at its stable path. |
| `CSS_PHASE4_WP4_3I_C_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3I_C_EVIDENCE.md](../CSS_PHASE4_WP4_3I_C_EVIDENCE.md) — Keep the header/frame ownership and blur guarantees at the retention-policy reference path. |
| `CSS_PHASE4_WP4_3I_DEAD_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3I_DEAD_EVIDENCE.md](../CSS_PHASE4_WP4_3I_DEAD_EVIDENCE.md) — Keep the oracle limitations, interaction-state deferrals and retained live declarations. |
| `CSS_PHASE4_WP4_3I_D_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3I_D_EVIDENCE.md](../CSS_PHASE4_WP4_3I_D_EVIDENCE.md) — Keep the muscle-selector fallback contract and retention-policy reference path. |
| `CSS_PHASE4_WP4_3I_E_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3I_E_EVIDENCE.md](../CSS_PHASE4_WP4_3I_E_EVIDENCE.md) — Keep the popover fallback contract and retention-policy reference path. |
| `CSS_PHASE4_WP4_3I_FILTER_BTN_EVIDENCE.md` | KEEP | [CSS_PHASE4_WP4_3I_FILTER_BTN_EVIDENCE.md](../CSS_PHASE4_WP4_3I_FILTER_BTN_EVIDENCE.md) — Keep the same-CSS control requirement and interaction-state deferrals. |

The [machine-readable manifest](PILOT_CSS_MANIFEST.csv) binds each original path,
blob and SHA-256 to its proposed disposition, destination and resulting identity.
The original path is a historical identity, not a live link target.

## Content preservation and reference repairs

- Five archive moves preserve the exact original bytes and Git blob identity.
- WP4.1 changes only three relative link targets, to its token inventory, Stylelint
  JSON baseline and WP4.0 ledger. Reversing those link edits reproduces the original
  bytes. The moved WP4.1 file is not described as byte-identical.
- Every KEEP file preserves its original first heading and complete remaining
  bytes, with only the historical-evidence notice inserted between them. Existing
  headings and anchors are retained.
- The Session Summary SPLIT preserves every byte before `## Next action`; its
  former tail is bound to the pre-cutover source. Technical deferred findings,
  verdicts, limitations and measurements are not rewritten.
- Inbound repairs affect only targets in `REFACTOR_PLAN.md`, the historical
  handover and `css_phase4_wp4_4/PLANNING.md`. The historical handover's repository
  path citations follow the moved files; its surrounding dated prose is unchanged.
- The docs index gains one cutover-navigation bullet. No private-register content,
  machine input, production code, tests, workflow or baseline is changed.

The complete tracked text tree was searched for each moved filename and path,
including code, workflow and script surfaces; no non-document reader was found
for these six records. Machine-consumed JSON, token inventories and screenshot
manifests stay at their existing paths. Current and historical shorthand citations
were checked separately from literal filename matches. No current guide or live
queue pointed to a moved record as an open follow-up.

## Validation and review boundary

Validation for this docs-only diff consists of whitespace checks, exact preservation
and link-only differential checks, local link/anchor regression checks, a public-
payload scope review and GitHub CI at the PR head. The quality-gate product-docs
row requires no application test run for this prose/navigation change. Adding files
under `docs/docs_cutover/` does not alter the parametrized `docs/ai_workflow/` surface.
Historical gate results inside evidence documents are not rerun or presented as
new validation results.

The 167 held records and H1 are outside this pilot. Permanent private homes and
temporary-copy reconciliation remain unverified closeout obligations. Stop at a
ready PR for owner review; no further batch preparation, merge or deletion is
authorized by this record.
