# Retained CSS evidence corrections — #581 and #601

Reconciled 2026-11-16 against `main` at
`9249f0953bf926c025e7957f1893fd433a2e8cc8`. This record disposes of the
thirteen audit entries in [#581](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/581)
and [#601](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/601).
It corrects historical descriptions without rerunning a measurement, changing a
delivered contract, regenerating a baseline, or reopening a completed CSS packet.

## Per-entry disposition

| Entry | Disposition and retained evidence |
|---|---|
| **AUD-0323** | Corrected. [Base evidence §2](../CSS_PHASE4_WP4_4_B_BASE_EVIDENCE.md#2-what-was-retained--including-two-corrections-to-inherited-claims) records **two** falsified scan nominations; the `:root` row is an M9 retention with no scan claim. [Scan README](../scan/README.md#how-to-use-it) no longer says the corrected base prose still counts three. |
| **AUD-0348** | Already corrected before this pass; verified and retained. [Inventory A §2.1 and §2.3](../CSS_PHASE4_WP4_4_N4_INVENTORY_A_IS_FAMILY.md#2-terminology-corrections-this-inventory-makes) distinguish the lowest arm `:3335` **(1,2,0)** from `:3336` **(1,3,0)**. No selector, measured range or inventory row changed. |
| **AUD-0349** | Corrected after original-source inspection. [Inventory B §4](../CSS_PHASE4_WP4_4_N4_INVENTORY_B_REGIONS_ABC.md#4-controls--all-clean-all-fatal) now describes **21** ID-free arms, matching §2. The original committed driver defines **5 + 5 + 5 + 3 + 3** arms and checks only those region selector lines; the former 26 is unsupported by that population. The 56,304 ownership records and verdicts remain untouched. Provenance is below. |
| **AUD-0361** | Corrected. [Baseline evidence §7](../CSS_PHASE4_WP4_4_A_BASELINE_EVIDENCE.md#7-motion-oracle-for-wp44-c-f1) and the first `oracleBlindSpots[].why` in [baseline JSON](../CSS_PHASE4_WP4_4_A_BASELINE.json) state timing blindness, without claiming whole-file pixel blindness. The matching `why` string in [the producer register](../../scripts/css_audit/measure.py) is synchronized because the existing contract requires exact register equality. This is a prose-only metadata edit: no measured value, digest, selector, property, count or source pin changed. |
| **AUD-0364** | Already corrected before this pass; verified and retained. [Ownership map items 5–6](../CSS_OWNERSHIP_MAP.md#current-loading-architecture) name both `js/theme-init.js` and the vendored `inter.css` sheet before `tokens.css`, matching [base.html](../../templates/base.html). Application stylesheet order remains unchanged. |
| **AUD-0388** | Corrected throughout the affected plan, including the contradictory F8 reviewer row. [Table plan](../css_table_helpers_cleanup/PLANNING.md#preservation-invariants-revised) describes the names/counts/byte-sizes manifest and its same-size replacement limit. The zero-path Git diff check is complementary content evidence; no stronger hash guarantee is attributed to `nameAndSizeSha256`. The [existing manifest contract](../../tests/test_css_wp4_4_a_baseline_contracts.py) is unchanged. |
| **AUD-0395** | The port-5178 scratch-probe recipe was already present; its contradictory closing sentence is now corrected. [Table evidence §9b and §11](../css_table_helpers_cleanup/EVIDENCE.md#9b-a-rest-state-pair-that-measured-another-worktree) distinguish the oracle on **5177** from the accepted port-adapted runtime probe and second server on **5178**. No historical or current harness is executed or modified. |
| **AUD-0397** | Corrected. [Table evidence §6](../css_table_helpers_cleanup/EVIDENCE.md#6-contracts--c1c5-and-why-each-is-stronger) limits C3 to contiguous `tbl-show` / `tbl-hide` stems, including the three exercised application shapes. Fragmented construction such as `'tbl-' + kind + '-' + size` can evade it. The original tests and red-path outcomes remain unchanged. |
| **AUD-0398** | Corrected. The table plan's [terminal outcome](../css_table_helpers_cleanup/PLANNING.md#outcome) now agrees with the **12/12** retained cases and recognizes the superseding §8a–§8d blocker dispositions. Separate D-1/D-2, FU-1/FU-2 and R1 records remain preserved; none is silently discharged here. |
| **AUD-0412** | Corrected. The WP4.4 [final execution status](PLANNING.md) and sequence diagram mark i, j and k complete, matching the [closed handoff ledger](EXECUTION_HANDOFF_I_K.md#snapshot--2026-08-01--arc-closed). Historical authority remains recorded and grants no new execution. |
| **AUD-0419** | Corrected. [D2 evidence D7 and §7](../CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md#7-out-of-scope--carried-forward) scope the demonstrated universal stylesheet-suppressor defect to d2's own harness. The shared runtime probe already used inline `transition-property: none !important` at d2 delivery; the named stylesheet competitors cannot outrank it. No shared-harness defect or blanket invalidation of earlier sentinel packets is inferred. |
| **AUD-0382** | Corrected after inspecting the delivered packet's exact helper. [Scale evidence §9c](../css_scale_btn_cleanup/EVIDENCE.md#9c-the-windows-visual-gate-passed-at-its-configured-tolerance) retains **66/66** and **18/18** as historical test totals, with **800** differing pixels allowed, `threshold: 0`, masks and five named pixel exemptions. Raw accepted per-capture comparator outputs are not retained in the repository. The counts do not establish zero pixel differences or PNG byte identity; independent **0/339,120** computed-value evidence remains authoritative for its measured scope. |
| **AUD-0383** | Reconciled from the packet's committed history. [Scale evidence §7](../css_scale_btn_cleanup/EVIDENCE.md#7-contracts-with-executed-adversarial-red-paths) labels **37** as an intermediate contract shape and **36** as the delivered count. The review fix removed one duplicate assertion with unchanged parametrizations; final inventory and restored totals agree at 36. The raw invocation is unavailable and is not invented. No test is added, removed or changed by this correction. |

## Original-source provenance

- **Inventory B population:** [original N4 driver at `89523edcba7df540e2490fbec9849bf159f722dc`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/89523edcba7df540e2490fbec9849bf159f722dc/scripts/css_audit/n4_regions_abc.mjs#L85),
  `REGIONS` at lines 85–119 and ID-free validation at lines 709–718. These establish
  the intended 21-arm source population; the raw measurement is not regenerated.
- **Scale comparator:** [PR #302 final head `c3f1a33da0b9b763897859e59d761d97960db2e7`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/302),
  delivered as `9c8377745d4aee7d45e0ebf169d29106fcf6660d`.
  [The helper at that head](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/c3f1a33da0b9b763897859e59d761d97960db2e7/e2e/visual-helpers.ts#L378)
  supplies the screenshot options; its lines 49–55 and 425–427 identify the
  exemptions and bypass. This bounds the historical claim without asserting that
  missing raw comparator outputs were recovered.
- **Contract revision:** [initial `a610d6769f4770bde2595cb0e563554b2fdc8532`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/commit/a610d6769f4770bde2595cb0e563554b2fdc8532)
  and evidence revision `d8a7a201ce7497712f58855a6df23c5aba2894aa` have 19 test
  functions and already quote the same 37-passed transcript.
  [Review fix `9aef088dbf5bf900f5c75cfcc0fb9c048328af10`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/commit/9aef088dbf5bf900f5c75cfcc0fb9c048328af10)
  removes `test_bare_scale_btn_family_is_entirely_absent`, leaving 18. Both shapes
  parametrize the same 3 retained annotations and 17 sibling CSS surfaces, giving
  37 and 36 nodes respectively. The original red-path transcript is preserved as
  intermediate evidence, not presented as a final 37-node run.
- **D7 attribution:** [shared runtime probe at d2 delivery `0a912d9ebb9d1ec7b9aadb5856fdbf1d56c7aa92`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/blob/0a912d9ebb9d1ec7b9aadb5856fdbf1d56c7aa92/scripts/css_audit/runtime_probe.mjs)
  establishes the inline suppression method independently of today's probe.

## Validation and preservation

Static comparison verifies that the baseline JSON changes only one `why` field,
and the producer changes only the corresponding string constant. The existing
exact-register contract remains intact. Existing CSS, JavaScript, templates,
database files, screenshot PNGs, measurement outputs, source pins and delivered
contracts are outside the diff. Required test results and the independent tooling
review are recorded on the correction PR.

This correction record and its source evidence remain at their consumer paths.
It retires no document, changes no accepted owner hold and selects no new scale,
rendering or measurement implementation.
