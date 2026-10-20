# R2.3 — JS Unit Q4 / D2 decision

**Status: Q4 approved; D2 approved conditionally, effective only after §13.0
records the specified cycle through its own process. C4 is not approved.**
Prepared 2026-10-20 on an isolated checkout of `main`; exact readings are in
[`EVIDENCE.md`](EVIDENCE.md) and [`main-js-jobs.csv`](main-js-jobs.csv).

## Owner decision — 2026-10-21

The owner approved the prepared recommendation with these exact conditions:

> Approve promotion and rename, conditional: D2 takes effect only once the §13.0 ledger records the 2026-08-27 → 2026-09-10T23:18:21Z cycle through its own process with zero red/missing/skipped/cancelled runs. The Q4 rename lands in its own change before any protection change. C4 settings activation stays a separate step needing my separate approval.

Asked whether the cancellation condition applies to JS Unit jobs or whole CI
workflows, the owner ruled:

> Assess exact JS Unit job conclusions under §13.0

This resolves the cancellation reading without changing the observed workflow
conclusion: run `34170988104` remains a cancelled CI workflow; its successful
JS Unit execution counts as one green result. Its attempt-2 copy receives no
second execution credit. The cycle contains **50 successful JS Unit executions,
zero red, zero missing, zero skipped and zero cancelled JS jobs**.

PR [#544](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/544), head
`72de3e223aa781603a5a5a6182999e2695de84c8`, already prepares the missing rows
65–113 in §13.0, including cycle rows 65–75. It is open at this recording;
publication in an unmerged PR is not represented as a completed mainline ledger
update. Until that prerequisite lands, D2 remains conditional. No replacement
T0, new window or repeat signature is requested.

**Fresh verification, 2026-10-21:** the implementer independently re-read all
50 cycle carriers and all JS job attempts from GitHub, then compared run ID,
job ID, conclusion and completion time with canonical proposal rows 26–75 at
the pinned #544 head. Every row matched; every actual Vitest step succeeded.
The result is **50 / 0 / 0 / 0 / 0** green/red/missing/skipped/cancelled JS
executions. The raw comparison is retained in
`artifacts/r23/cycle-ledger-comparison.json`; this is verification evidence, not
an independent reviewer verdict or a declaration that #544 has merged.

## Approved outcome

**D2: approve making JS Unit a required check. Q4: rename it to
`JS Unit (Vitest)` while it is still unprotected, before adding that exact name
to branch protection.** Test failures would block merges; coverage remains
informational with no new percentage threshold.

This removes the misleading suffix before the name becomes protected. Retaining
`JS Unit (Vitest, non-required)` is also technically safe if deliberately chosen;
renaming after protecting the old name can leave every PR waiting for a missing
check. The renaming rule is in
[`STEP12_JS_UNIT_GATE0.md` §7](../testing_phase3/STEP12_JS_UNIT_GATE0.md).

## Qualification

- The declared T0 is **2026-08-27T23:18:21Z**; the strict mark is
  **2026-09-10T23:18:21Z**. Neither is reset or re-declared by this packet.
- A fresh, paginated GitHub query independently verifies **50 main CI carriers**
  inside that window: **49 successful carriers and one cancelled carrier**.
  Every reported JS Unit job and Vitest execution step succeeded. Under the
  owner's job-level ruling, all **50 JS executions** count green; the cancelled
  workflow conclusion is preserved separately and its rerun is not another
  execution. No failed, missing, skipped or cancelled JS execution was found.
- There was no run on the closing day. The rule requires fourteen failure-free
  calendar days and specifies neither a minimum run count nor a closing-day run.
  This interpretation matches the separately recorded reconciliation in
  [`ci_cd_expansion/PLANNING.md` §11.5](../ci_cd_expansion/PLANNING.md).
- The test tree and `vitest.config.js` are byte-identical between T0's commit
  `288667d` and the audited main. Packet F is already merged as `2c95bae` (#411),
  and the required Test Inventory Drift check pins Vitest identities.
- Current local execution passes **13 files / 245 tests**, with coverage enabled.
  The committed inventory matches fresh collection. Coverage remains report-only.

The complete current-run audit also preserves runs after qualification, cancelled
carriers, rerun attempts and any in-progress carrier instead of selecting only
green rows. Its exact cutoff and counts are in EVIDENCE.md.

## Scope of the approval

**Q4 and D2 are recorded together**, including the selected display name and the
owner's explicit job-level accounting. The original task describes R2.3 as an
owner decision and documentation reconciliation, separate from engineering
activation. This record does not claim that protection has changed.

The repository explicitly requires a **“separate owner signature on D2 itself”**
([step-12 §0.1](../testing_phase3/STEP12_JS_UNIT_GATE0.md)). The owner's direct
answer above supplies that signature with its ledger prerequisite. It approves
the bounded standalone rename. It grants no C4 settings authority; publication
and named merge gates remain governed by the repository workflow.

| Decision | Ruling | Owner record |
|---|---|---|
| D2, JS Unit half | Approved, conditional on the specified §13.0 cycle being recorded with zero adverse JS job results | Owner, 2026-10-21; canonical ledger landing pending |
| Q4 | Use `JS Unit (Vitest)`; land the rename in its own change before protection | Owner, 2026-10-21; rename implementation and landing tracked separately |
| Cancellation scope | Exact JS Unit job conclusions; preserve carrier conclusions separately | Owner clarification, 2026-10-21 |
| C4 settings activation | Separate owner approval after code/contracts and live proofs | Not approved |

## Concrete follow-through after the decision

R2.3's decision closes when the owner ruling is recorded and the live references
are reconciled. Promotion itself closes only on verified GitHub enforcement.

1. Record the actual owner words here, then reconcile the current queue's R2.3
   row, step-12 Q4/D2 state and Testing Strategy sign-off state. Annotate dated
   history rather than rewriting its measurements. Coordinate the existing queue
   claim before publishing its bounded amendment.
2. For activation, prepare a bounded plan and obtain its applicable Gate 1 under
   [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md). Coordinate the sole
   `ci.yml` editing slot. B3 merged as `1f5ae0f0` (#539) during this audit; start
   from that merge or a newer main.
3. Rename only the unprotected `js-unit` display name to `JS Unit (Vitest)`.
   Update stale comments in `ci.yml` and `vitest.config.js` without changing the
   suite, include patterns, coverage thresholds or failure propagation. Keep the
   existing install and coverage commands, direct-job shape and job identifier.
4. Reconcile the exact name in C4's promotion sets/command sheet, release
   provenance constants and contracts together. C4 requires distinct
   `PR_REQUIRED_CONTEXTS` and `RELEASE_EXPECTED_CONTEXTS`, supported staged sets,
   existing enforcement floors, and rejection of missing/skipped/cancelled/failed,
   wrong-SHA, stale or untrusted-app evidence. With this candidate alone, the
   current 12-context PR floor becomes **13**, and the release set becomes **14**
   including Windows visual once. PR-only Dependency Review remains outside the
   release set. Other promotions and strict-mode activation remain independent.
5. Run full pytest for workflow changes, inventory `--check` (regenerate only on
   real drift), JS tests with coverage, release-provenance/contracts and staged-set
   cases. Obtain the independent `code-reviewer` required for workflow/script
   changes; add architecture review if the final diff adds/removes a job or
   converts one to `uses:`. Existing SHA, newest-run, app-binding and visual
   contracts must not weaken. Prove a seeded Vitest failure makes the job red.
6. Obtain publication/merge authority for the named implementation PR. Merge
   code/contracts before applying protection, and require a successful real
   check under the final exact display name on the merged main commit. No tag
   is created during a partially applied enforcement transition.
7. Only with C4 settings authority: re-read the live protection immediately
   before applying it. Preserve every existing `(context, app_id)` pair and
   `strict`; add only the qualified candidate with GitHub Actions
   `app_id: 15368`. Abort if the fresh floor differs from the reviewed snapshot.
   [`required-status-checks.proposed.json`](required-status-checks.proposed.json)
   shows the complete 13-context payload for this snapshot and is **not** an
   instruction to apply a stale payload.
8. Read settings back and prove the exact check appears as required on a
   throwaway PR; a failing check must actually block normal merge eligibility.
   Missing-name pending behavior, local tests, YAML and workflow success alone
   are not enforcement evidence. Record the final names, bindings, SHA and live
   blocking result, then reconcile all live status references.

**Completion evidence still needed:** mainline §13.0 ledger landing for D2's
effective state; the standalone Q4 rename with required tests/review and named
merge authority; separate C4 approval and live settings/blocking proof for actual
promotion. The direct Q4/D2 owner signature and cancellation reading are recorded
above and do not need to be requested again.
