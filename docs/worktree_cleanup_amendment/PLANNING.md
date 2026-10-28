# Plan Review — Worktree cleanup: drive-root children outside Operations B and C

*Artifact created from [`docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md).
Source packet: [`docs/worktree_cleanup/AMENDMENT_2026-09-28.md`](../worktree_cleanup/AMENDMENT_2026-09-28.md).*

**Landing-path note.** This artifact is deliberately at
`docs/worktree_cleanup_amendment/PLANNING.md`, outside two hazards:

- `docs/ai_workflow/` is one of the non-recursively globbed directories in the
  parametrized test-inventory surface ([QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md),
  "What trips `Test Inventory Drift`"). *Adding* a file there moves an inventory node and
  reds the required `Test Inventory Drift` check. *Editing* a file already tracked there
  does not.
- `docs/worktree_cleanup/PLANNING.md` already exists in two divergent, unreconciled
  lineages (an upstream tracked copy and a local untracked copy). Neither is created,
  read-modify-written, overwritten, staged, or otherwise touched by this packet.

**Authority of this document.** Planning only. It authorizes no filesystem mutation,
preservation copy, quarantine, deletion, ref change, or worktree removal, and it widens
no existing approval.

---

## Section 0 — Requirements Brief

### Raw requests (verbatim)

**Original council authorization**

> I authorize a plan-stage council for the drive-root scope amendment only. You may use the required product-manager and three independent reviewer agents. No agent may perform cleanup or alter live preservation state.
>
> Read CLAUDE.md, the local and origin/main versions of QUALITY_GATE.md and .claude/commands/council-plan.md, PLAN_REVIEW_TEMPLATE.md, the draft at docs/worktree_cleanup/AMENDMENT_2026-09-28.md, its dated evidence and private local record, and both versions of the technical cleanup plan.
>
> First classify the amendment under QUALITY_GATE.md. Determine whether the existing signed Gate 0 covers this scope change. If a new Gate 0 is required, have the product-manager prepare a complete Section 0 for owner review and stop before the council. Do not infer Gate 0 approval from Operation A's Gate 1.
>
> If the council can proceed, follow /council-plan in order:
> 1. Have the product-manager write Plan v1 using the amendment packet as source. Use a new, collision-free docs/<feature>/PLANNING.md artifact, placed outside both docs/ai_workflow/ (the parametrized surface) and docs/worktree_cleanup/ (the divergent-PLANNING.md collision). Do not overwrite either divergent version of docs/worktree_cleanup/PLANNING.md.
> 2. Run architecture-reviewer, test-strategist, and product-risk-reviewer independently in parallel against the same Plan v1 and proposed Hunks 1–4. Record their actual agent IDs and verbatim findings. Do not share one reviewer's findings with another before their reviews finish.
> 3. Disposition every finding, then have the product-manager write the response matrix and Plan v2 in that same council artifact. Record provenance and any failed or missing review honestly. Stop for my Gate 1 decision; do not apply the proposed technical-plan hunks as approved text.
>
> Review in particular whether Hunks 1–3 merely define a gated route or appear to approve a C scope extension; whether later retirement stays separate from B's fixed two-root result and D's worktree slices; whether §4.2–§4.5 need reciprocal references; and which Hunk 4 wording accurately records published Operation A source and the remaining §5.4 obligations.
>
> The early targeted rescue decision is OUT OF SCOPE. Review whether the packet keeps it separate, but do not choose an option or count it among the council's in-scope decisions.
>
> Carry the dated evidence as evidence, not permanent live state. Operation A's reviewed source bytes were merged; the current guard is a successor whose behavior and deployment remain unverified here. The retained September 7 audit places the disappearance of the August backup artifacts after that audit; its cause is unknown. Keep the approved historical baseline unchanged.
>
> Correct test-inventory routing: adding files under docs/worktree_cleanup/ does not enter the parametrized Markdown surface. The untracked file under docs/ai_workflow/ can cause local collection drift, so do not regenerate or hand-edit the inventory from this dirty checkout. Treat PR #487 separately.
>
> Mechanical traps: bash heredocs are blocked by the guard hook — use the Write tool for scripts; backticks inside python -c "..." through Bash become command substitution; `origin/main:.claude/...` trips MSYS path conversion — use git ls-tree + cat-file blob, and never set or export either MSYS suppression variable. git stash is shared across worktrees here — never use it.
>
> Reviewers are read-only. Do not pull, stash, add -A, commit, push, open a live database, copy preservation sources, alter the baseline, prune, delete, retire refs, or remove worktrees. Report the classification, each reviewer's verbatim findings, response matrix, Plan v2, unresolved evidence, and exact owner approvals still needed.

**Revision instruction, 2026-09-28**

> Revise the Gate 0 Section 0 draft at docs/worktree_cleanup_amendment/PLANNING.md before asking me to sign it.
>
> Read CLAUDE.md, docs/ai_workflow/QUALITY_GATE.md, docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md, the draft amendment at docs/worktree_cleanup/AMENDMENT_2026-09-28.md, the dated evidence at docs/worktree_cleanup/evidence/2026-09-28-state.md, and the private local evidence at artifacts/worktree-cleanup-reentry-20260928/LOCAL_EVIDENCE.md. Compare the local plan with origin/main. Treat origin/main as the tracked amendment base, while preserving the divergent local file.
>
> Spawn multiple independent AI advisers in parallel to evaluate the two substantive Gate 0 choices:
>
> 1. Should the two additional D:\ root directories enter the preservation scope through an explicitly gated extension of Operation C, or through a separate preservation operation?
> 2. Should their eventual retirement use a separate, explicitly approved operation? Preserve Operation B's fixed two-root MALFORMED_ROOTS_QUARANTINED meaning and Operation D's approved-worktree scope.
>
> Give me each adviser's separate recommendation, supporting evidence, disagreements, and your synthesis. These advisers are consulting on Gate 0; they are not the required plan-stage council and cannot approve Gate 0.
>
> Revise Section 0 so that only genuine owner policy choices remain as blocking questions. Resolve wording, cross-references, landing mechanics, and other routine drafting choices using the evidence and your judgment. Keep dated counts, timestamps, and the backup-disappearance window in dated evidence, not in the stable technical plan. Correct the stale Operation A publication premise: reviewed source was merged on 2026-09-07, while the remaining §5.4 deployment and verification work is open. Do not attribute the missing preservation artifacts to the August cleanup; a retained 2026-09-07 audit showed them present then.
>
> Show the revised Section 0, the advisers' findings, your recommended answers to the two owner choices, and the exact Gate 0 decision you need from me. Do not mark Gate 0 approved on my behalf. Do not run the plan-stage council until I approve Gate 0. Once I approve it, the council work already requested is authorized; do not ask me for separate permission to spawn its reviewers.
>
> Keep the early-targeted-rescue question outside this amendment packet. Do not copy, delete, quarantine, prune, remove worktrees, change refs or the approved baseline, open a live database, or publish private material. Do not use git stash or git add -A in the shared checkout.

### Problem

The current technical design — [`docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md)
— has no defined outcome for a drive-root directory that is neither one of Operation B's
two named malformed roots (`D:\c`, `D:\d`) nor inside Operation C's owner-approved
`D:\development` source scope. Two such directories were observed on 2026-09-28,
referred to here only as **RESIDUE-1** and **RESIDUE-2**. The design leaves five things
unresolved for them.

1. **No classification.** §7.2 item 4 states C's scope as a single named tree, and §6
   and §11 name B's two roots exactly. A directory outside both has no status. The design
   does carry an adjacent vocabulary family — *"unintended"* drive-root child (§5.1),
   *"unexpected new children"* (§5.2), *"other unexpected root"* (§6), *"unexpected
   drive-root child"* (§8.3), *"unexpected drive-root children"* (§11) — but every member
   of that family is discriminated against the **owner-approved drive-root baseline**,
   not against an operation's approved source manifest. Introducing a second noun with a
   second discriminator into a signed design is a hazard in itself.
2. **Discovery without a route to preservation.** §7.5 obliges C's inventory to cover
   *"recovery/backup directories"*, *"local application-data roots"*, and *"explicit owner
   paths"*, and then to *"Preserve ignored/untracked/local settings, handovers/claims,
   evidence, loose files, recovery/salvage directories, and unique local payload."* That
   is an inventory obligation with an open-ended inclusion hook and no stated authority
   to add a discovered directory to C's immutable source manifest. The material can be
   seen and not preserved, with no recorded route from discovery to a reviewed,
   owner-approved manifest entry — and, read alone, §7.5 is also the strongest surface for
   the opposite misreading, that discovery already obliges capture.
3. **No boundary against removal.** Nothing prevents a future reader from treating
   preservation — or proximity to a named root, a generated-output classification, a
   filesystem creation timestamp, or an old campaign's completion receipt — as authority
   to remove the directory. That would silently widen Operation B's fixed two-root
   aggregate or Operation D's worktree-slice semantics.
4. **A standing monitoring conflict with no disposition.** §5.2's read-only drive-root
   audit compares configured roots against the owner-approved baseline and reports
   unexpected children; §8.3 requires each closeout to *"confirm no unexpected drive-root
   child was created"*; §11 requires unexpected drive-root children to *"remain consistent
   with their closeout manifest"* and defines `PREVENTION_COMPLETE` partly as *"lifecycle
   monitoring is active"*. Two known children now sit outside the frozen baseline with no
   scheduled clearing event, so every B/C/D closeout carries either a standing red or an
   undocumented allowance. The dated evidence separately forbids baselining a root to make
   that audit exit zero.
5. **A record that is stale in two places.** The plan's status header (lines 8–9) still
   asserts that *"Gate 2 and the remaining publication, installation and monitoring
   obligations remain open"*, and `docs/ai_workflow/INDEX.md` (lines 61–65, identical in
   the local copy and on `origin/main`) still describes the plan as *"Gate 1 plus the
   Windows-filesystem review pending"*. Operation A's reviewed guard and test bytes were
   merged on 2026-09-07; Operation A Plan v2 Gate 1 was signed 2026-09-05. Separately,
   `"Gate 2"` appears only in that header and in the local §12 checkbox, and is defined
   nowhere in the file — §5.4 is *"Gate A"*.

Separately, the 2026-08-24 cleanup summary names preservation artifacts and a pointer
file that are absent today, while a retained audit dated 2026-09-07 records them present
and identity-matched. **The August campaign is therefore positively refuted as the
cause.** The design has nowhere to record that bounded, unexplained discrepancy without
editing the owner-approved historical baseline — and, under §1.1, the dated facts of that
discrepancy do not belong in this design at all.

This packet is about *defining* outcomes as proposed text for council and owner review.
It is not about taking any route it defines.

### Amendment base — resolved

The amendment applies to the copy of `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`
**tracked on `origin/main`**, and the divergent local file is preserved untouched.

Measured in this checkout, read-only:

| | Tracked on `origin/main` | Local working tree |
|---|---|---|
| Path status | tracked (blob `1b41922e795e9202f128a9b1122d0ffb6c6134af`) | untracked at `HEAD`; this checkout is behind the commit that added it |
| Length | 1471 lines | 1475 lines |
| Divergence | one hunk only, at line 1389 (the §12 Gate 1 checkbox) | same |
| Hunk 1–3 anchors (lines 95, 923, 1384) | present and identical | present and identical |

Consequences, all resolved by drafting judgment rather than owner decision:

- The packet's Hunk 4 diff block is written against this base and applies to it cleanly.
- The local file's §12 text — *"Complete the separate Operation A Gate 2
  source/publication decision and remaining installation, acceptance, and monitoring
  obligations"* — rests on the superseded premise that publication is open. It is not the
  base, and it is not committed, staged, reverted, or overwritten by this packet.
- The amendment is an **in-place edit of a tracked file** in a globbed surface directory,
  which does not trip `Test Inventory Drift`. No file is added to or deleted from
  `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, or `docs/ai_workflow/`.

### Why a new Gate 0 is required

Classification under [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md):

| Axis | Result |
|---|---|
| Plan-stage routing (planning size) | **Large / ambiguous / new workflow** — a cross-cutting semantic change to an approved multi-operation design, with unclear requirements. **Gate 0 and Gate 1 are both required.** |
| Change-type row for the technical design being amended, and for `INDEX.md` | **AI workflow / agent config** (`docs/ai_workflow/**`) — manual dry-run/self-review; `code-reviewer` or careful self-review; run tests only if source behavior changed. The design's own §4.5 gate matrix pairs these two files in one row: *"This plan plus INDEX"*. |
| Change-type row for this council artifact itself | **Product docs only** (`docs/**` excluding AI workflow files) — no required tests or reviewers. |
| Blocking CI gates | `Test Inventory Drift` is not tripped: this artifact's directory is not a globbed surface, and both `docs/ai_workflow/` edits are in-place edits of tracked files. No inventory regeneration is performed from this checkout. The pyright baseline diff does not apply — no `.py` changes. |

**The existing signed 2026-09-05 Gate 0 does not cover this scope change.** That Gate 0
(recorded in the *upstream tracked* `docs/worktree_cleanup/PLANNING.md`) scopes its
in-scope list to: requirements and acceptance criteria for the sequence Gate 0 →
Operation A tranche → `PREVENTION_COMPLETE` → open-development closeout → stabilization
checkpoint → fresh evidence → separately approved cleanup; explicit authorization
boundaries for A, B–D and E; and its assumptions and blocking owner decisions. Its twelve
acceptance criteria contain **nothing** about drive-root children outside B and C, nothing
about additional preservation sources, and nothing about a new retirement operation class.

**Operation A's Gate 1 is not a substitute and must not be cited as one.** It approved
Operation A Plan v2 only. Independently, §1.1 of the design requires renewed Gate 1 review
for a semantic change to the plan, and §1.3 requires the Gate 0 record to live in the
council artifact.

### Acceptance criteria

Criteria 1–3 bound authority. Criteria 4–9 are **route-neutral**: they hold whichever
answer the owner gives to the blocking questions below, and none of them presumes a route.

1. Given this packet and any amendment text later approved from it, when any agent or
   reader looks for execution authority, then they find none: no preservation copy,
   quarantine, relocation, deletion, ref change, archive-ref creation, or worktree removal
   is authorized by this packet or by the approved amendment text, and the artifact says
   so in its own authority statement.
2. Given the approved amendment text, when a reviewer reads any individual sentence out
   of context, then no sentence can be read as approving a particular preservation scope,
   source, or removal: each states only the *shape* of a gated route, every permissive
   clause is anchored to a **dated owner approval record distinct from the amendment that
   introduced the clause**, and the approved text states that no source or target is
   approved by the plan's own text. A gated route being defined is not that route being
   taken.
3. Given the approved amendment, when the direction of inference is reversed, then it is
   also closed: the text states that **no existing aggregate, receipt, approval record,
   manifest, or baseline entry in this plan authorizes the new work**, and that completing
   the new work neither changes `PREVENTION_COMPLETE` nor permits an edit to the
   owner-approved drive-root baseline nor a zero exit from the §5.2 audit.
4. Given Operation B's completion aggregates, when `MALFORMED_ROOT_QUARANTINED(root)` or
   `MALFORMED_ROOTS_QUARANTINED` is evaluated, then the plural aggregate still means
   exactly its two named roots and nothing else, §4.3's *"exactly one malformed-root
   identity"* binding is unchanged, and no receipt, approval record, or quarantine
   destination of Operation B can cover another root.
5. Given Operation D, when its scope is evaluated, then it is still limited to approved
   worktree slices, and the approved text **states the structural seal** rather than
   relying on it: a drive-root directory can never satisfy §3.6 condition 1 (*"a
   registered immediate child of the approved development parent"*), can never record a
   §3.5 lifecycle basis, can never enter a §3.7 immutable target set, and therefore can
   never affect `WORKTREE_SLICE_COMPLETE`, `WORKTREE_SLICE_PARTIAL_CLOSED`,
   `TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED`, or `WORKTREE_CLEANUP_COMPLETE`.
6. Given any proposal to preserve an additional drive-root source — under whichever route
   the owner selects — when the proposal is assessed, then it enumerates an exact, closed
   set by canonical/final path and physical identity; applies the obligations of §7.2
   items 1–5 and the §7.5 and §7.6 gates to each source, named as obligations rather than
   by item number where an item's text is scope-specific; rejects wildcard or prefix
   expansion, source–source and source–destination overlap, overlap with the primary
   scope, a missing source, and a changed identity; states the per-source extraction root
   and how §7.6's whole-tree source-to-restoration equality is proven across disjoint
   sources; extends §7.1's runtime map and writer-shutdown set to each source, or records
   why none is needed; and has its capacity requirement and freeze budget **recalculated
   for the complete set, with the owner re-approving the maximum freeze duration** — a
   previously approved maximum does not carry over — and re-measured immediately before
   writing.
7. Given any such proposal, when a defect, overrun, or unresolved identity occurs on an
   additional source, then the approved text states unambiguously whether it aborts or
   blocks the primary `D:\development` capture, and which §7.2 abort branch applies. The
   meaning of `PRESERVATION_COMPLETE` — the single gate whose failure §7.6 says *"blocks D
   and E"* — is either provably unchanged or explicitly restated, so that pre-amendment
   and post-amendment receipts remain comparable.
8. Given that C's §7.5 inventory discovers a drive-root child outside the approved scope,
   when the discovery is recorded, then the child is retained and recorded only —
   discovery never adds it to an immutable source manifest — and that sentence appears **in
   §7.5 itself**, alongside a tightening of §7.5's *"explicit owner paths"* hook to paths
   enumerated in the approved manifest, not only in §7.2 where a §7.5 reader will not see
   it.
9. Given that such a source has been preserved, when its eventual retirement is
   considered, then the approved text requires, before any retirement authority exists:
   verified preservation of that exact source with a **proved off-machine restore from the
   stored secret** (the analogue of §7.5's *"Prove recovery with the stored secret before
   any removal"*, which today enumerates only *"a B quarantine move or D removal"*); an
   exact immutable, digest-bound, positive, non-empty target manifest; §4.2's non-LLM human
   and Windows-filesystem review with scratch proofs for the new path forms; §4.3 manifest
   integrity and owner approval; a §4.4 journal **and** the shared coordination lock and
   attempt register; a §4.5 pre-drilled and verified recovery playbook; a stated retention
   start and per-object retention period; and the named §11 retention-exit checks. The
   route is specified as archive plus non-overwriting same-volume quarantine, never
   recursive deletion; permanent deletion remains §11's separate later operation.
10. Given that the amendment creates any new operation class, when the design is read as a
    whole, then the class is **enrolled by name** everywhere the design quantifies over
    operations, or the amendment records why each is inapplicable: §1.2's approved rollout
    order and dependency graph, §1.2's *"before B, C, or D uses its filesystem
    mutation/copy primitives"*, §2.2 rule 3 and rule 6 (*"every B-E preservation/cleanup
    command"*), §2.2 rule 20's retention clock, §4.1's launcher-staging rule, §4.3's
    opening enumeration, §4.4's *"All B-E live launchers"* and *"every B-E live attempt"*,
    §4.5's trigger list and its gate-matrix row, §7.5's pre-removal recovery-proof clause,
    §10's abort and recovery rules, and §12's decision list. A class outside those
    quantifiers is textually outside the shared lock and the recovery-playbook
    precondition.
11. Given that the amendment creates any new operation class, when its completion is
    considered, then §11 defines a **named, distinct outcome** for it — parameterized per
    root, with no unqualified plural over an open set — because §8.1 permits only *"Section
    11's exact named outcome"* to be claimed. An operation with no named outcome is
    unclosable.
12. Given the terminology, when the amendment names these directories, then it defines the
    term **once**, states its discriminator explicitly against the design's existing
    baseline-discriminated family (§5.1, §5.2, §6, §8.3, §11), defines it by path identity
    rather than by approval status so the protection cannot lapse at the moment the
    directory enters an approved manifest, and states that entering any approved source
    manifest never removes a child from the unexpected-drive-root set checked by §8.3 and
    §11.
13. Given §5.2's drive-root audit, §8.3's closeout check, and §11's consistency
    requirement, when a known drive-root child outside B and C persists, then the approved
    text introduces an **owner-dispositioned known-unexpected register** and states
    precisely and only what it changes. It serves §8.3 and §11; it does not serve §5.2.
    Specifically, the approved text states each of the following:
    - **What it changes.** §8.3's closeout check is *"confirm no unexpected drive-root
      child was created"* — a delta over the operation window, not a census. The register
      pins, by exact canonical/final path and physical identity, the set of unexpected
      drive-root children **already recorded before the operation began**, so that closeout
      compares the post-operation drive-root enumeration against the owner-approved
      baseline **union** the register as frozen at that operation's start, and fails on a
      child **newly created during the operation**. A pre-existing registered child is
      therefore not a closeout failure; a newly created one is, whether or not it resembles
      a registered entry. It also gives §11's requirement that unexpected drive-root
      children *"remain consistent with their closeout manifest"* a determinate meaning for
      a child that belongs to no operation's manifest: each registered entry must be
      unchanged at its recorded identity at closeout.
    - **What it does not change.** It does not clear, suppress, or alter the §5.2 audit,
      which continues to compare configured drive roots against the owner-approved baseline
      and to report every unexpected child. The audit's non-zero exit is **unchanged and
      expected**, and a registered entry is neither a reason to suppress that report nor a
      reason to ignore it. A register entry is **not** a baseline entry, is not added to the
      baseline, does not alter the baseline's bytes, approver, approval timestamp, or
      `RESOLVED` meanings, and is not a source- or target-manifest entry. It confers no
      preservation, relocation, quarantine, or removal authority, and it is not a
      disposition that any operation may act on.
    - **Its own integrity.** Each entry carries an exact identity, the owner's disposition,
      and the fact that it is retained; an entry is added or changed only by owner decision,
      never by an executor, an audit run, or a closeout; and the register is frozen for the
      duration of an operation so the delta in the first bullet is computable and
      after-the-fact additions cannot retroactively excuse a child created during that
      operation.
14. Given §1.1's stable-policy rule, when any amendment text lands in the technical design
    or in `INDEX.md`, then it introduces **no dated live-history or live-state fact**:
    no merge date, PR number, commit SHA, CI run outcome, audit timestamp, observation date,
    disappearance window, count, file count, path, or remote advertisement. In particular
    the **2026-09-07 merge date is not introduced into the design or `INDEX.md`**; those
    surfaces state the merged-source *status* as a stable fact and nothing more, and the
    date itself lives in
    [`evidence/2026-09-28-state.md`](../worktree_cleanup/evidence/2026-09-28-state.md).
    The exclusion does **not** extend to the gate-approval signature dates the design
    already carries in §12 (*"signed 2026-09-05"*): a durable owner approval record is not
    live evidence, §1.1's enumeration does not list it, and §4.3 requires an approval to
    bind *"owner, date, and retention deadline"*. Those entries stay exactly as they are.
    The historical discrepancy is recorded, with its window, as an unresolved matter in the
    dated evidence only, with the August campaign **positively refuted** as its cause and
    the cause otherwise stated as unknown — not as an attributed incident and not as an
    unproven suspicion.
15. Given the owner-approved 2026-09-06 drive baseline, when any amendment lands, then its
    bytes, its approver, its approval timestamp, and the meaning of its `RESOLVED` entries
    are unchanged and unrelabelled; and when a successor baseline is ever proposed, then it
    is versioned through the owner process under the externally recorded constraints
    (non-empty approver; ISO-8601 approval timestamp with timezone and not in the future;
    development-parent and root set consistent with the generating runbook command).
16. Given the observed 2026-09-28 filesystem creation timestamps of both directories, when
    the amendment text is read, then those timestamps are neither an authorization for any
    action nor an incident finding; their relationship to the absent August artifacts is
    recorded as undetermined, and the record of them stays in dated evidence under
    criterion 14.
17. Given Operation A's actual state, when the design and `INDEX.md` are read, then both
    record it accurately **and without a date**, per criterion 14: the reviewed guard and
    test source **is merged**, stated as status rather than as a dated event; no surface
    asserts that publication or source integration is open or staged. What remains open is
    stated as obligations, not as live-state claims: §5.4's outstanding conditions —
    deployment, installation verification, interception and profile captures, and
    active-guidance coverage — together with §11's active-monitoring requirement, the
    disposition of the cancelled post-merge required check, and the reconciliation of **any
    successor of the reviewed artifact** against the reviewed bytes before the deployment
    decision. The orphaned `"Gate 2"` name is removed or defined. §12 retains an
    **unchecked** item for the renewed plan-level Gate 1 that later semantic amendments
    require, rather than leaving no open box for it. `INDEX.md`'s *"Gate 1 … pending"* line
    is corrected in the same change. Citations are exact: monitoring is §11's
    `PREVENTION_COMPLETE`, not a §5.4 bullet. The 2026-09-07 merge date, the PR number, and
    the cancelled check's run identity stay in the dated evidence.
18. Given the two divergent `docs/worktree_cleanup/PLANNING.md` lineages, when this packet
    is executed, then neither file is created, read-modify-written, overwritten, staged, or
    committed, and this council artifact lands outside both `docs/ai_workflow/` and
    `docs/worktree_cleanup/`.
19. Given this dirty checkout (locally modified, untracked Markdown inside the globbed
    `docs/ai_workflow/` directory, and behind `origin/main`), when the packet completes,
    then `docs/test_inventory/` has been neither regenerated nor hand-edited from it, and
    no `git pull`, `git stash`, `git add`, `git add -A`, `git commit`, `git push`,
    `git merge`, `git checkout`, `git reset`, `git clean`, worktree add/remove/prune, or
    ref deletion was run.
20. Given the private evidence record, when this artifact and any approved amendment text
    are read, then neither publishes the exact paths, identities, hashes, row counts, or
    member findings of RESIDUE-1 or RESIDUE-2.
21. Given the early targeted rescue decision, when this packet's decision list is read,
    then the rescue decision appears only as an explicitly separate, undecided item — no
    option is selected and it is not counted among this packet's in-scope decisions.
22. Given Gate 0 is unsigned, when any agent considers proceeding, then the council
    (`architecture-reviewer`, `test-strategist`, `product-risk-reviewer`) has not been run
    and no Plan v1 exists; work stops for the owner's Gate 0 decision.

### Calculation surface

- `none`.

This packet changes no application behavior, no database schema, no API response shape,
and no hypertrophy calculation. Specifically untouched: `utils/effective_sets.py`
(effective sets, `CountingMode`, `ContributionMode`), RIR/RPE handling,
`utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py`,
`utils/volume_*.py`, and `utils/fatigue*.py`. No worked example and no migration notes are
required, because no function's inputs or outputs change. The only artifacts in play are
planning/design Markdown.

### In scope

- The amendment packet's **proposed requirements 1–6**, reviewed as *proposals*, not as
  approved policy — with requirement 2's *"The preferred design is an explicit scope
  extension"* treated as a draft position the owner has not taken, not as settled policy.
- The amendment packet's **Hunks 1–4**, reviewed as *proposed text* and explicitly not
  applied as approved text at this stage. The council reviews them against the
  `origin/main` base, re-drafted after the owner answers the blocking questions, since
  Hunks 1–3 as written pre-commit the Operation C extension route.
- **Two further hunks this packet adds**, both consequences of the corrected Operation A
  record and both resolved by drafting judgment rather than owner decision. Both are
  **dateless** under acceptance criterion 14:
  - a status-header hunk at lines 8–9 of the plan, removing the stale open-publication
    assertion and the orphaned `"Gate 2"` name, and stating the merged-source status plus
    the remaining obligations without a merge date;
  - a `docs/ai_workflow/INDEX.md` hunk at lines 61–65, correcting *"Gate 1 … pending"* to
    record Gate 0 and Operation A Plan v2 Gate 1 as signed, with the Windows-filesystem
    review and the remaining Operation A obligations pending — again without a date.
- The **enumeration sweep** required by acceptance criterion 10 if the owner's answers
  create a new operation class, and the **reciprocal cross-references** from §4.2, §4.3,
  §4.4 and §4.5 back to whichever section carries the new route.
- The **§7.5 placement** required by acceptance criterion 8.
- The **terminology** resolution recorded under *Decisions resolved by drafting judgment*
  below.
- **Recording the historical discrepancy** in dated evidence only, as bounded, unresolved,
  and not attributable to the August campaign.
- This Gate 0 requirements brief and, only after owner sign-off, the council run and its
  artifacts within this same file.

### Out of scope / non-goals

- **The early targeted rescue decision.** Out of scope. This packet only records that the
  rescue decision is kept separate from the scope amendment. No option is selected, and it
  is not counted among this packet's in-scope decisions.
- Executing any step of Operation A, B, C, D, or E; any filesystem mutation; any
  preservation copy, protective copy, quarantine, move, deletion, junction unlink,
  archive-ref creation, or worktree removal.
- Reconciling the two divergent `docs/worktree_cleanup/PLANNING.md` lineages, and any
  commit, stage, overwrite, or read-modify-write on that path.
- The open Operation A decisions, each separate from this packet: the post-merge CI
  disposition of the cancelled required `Run Tests` context; the
  reviewed-artifact-versus-successor reconciliation on `origin/main`; the 93-target guard
  deployment proposal; and monitoring restoration. This packet corrects how the design
  *describes* them; it does not decide any of them.
- Assessing whether the successor guard on `origin/main` preserves the reviewed Operation
  A behavior, and measuring Operation A deployment state.
- Regenerating or hand-editing `docs/test_inventory/`. PR #487 is treated separately.
- Altering the owner-approved 2026-09-06 historical baseline, its bytes, its approver, its
  approval timestamp, or its `RESOLVED` meanings; and adding either Operation B root to a
  baseline to make the daily drive-root audit exit zero.
- Publishing RESIDUE-1's or RESIDUE-2's exact paths, identities, hashes, row counts, or
  other machine-local findings into this artifact; they stay in the gitignored private
  record.
- Running pytest, Playwright, Vitest, the inventory generator, or the application; opening
  or querying any live database.
- Characterizing the member classes of either directory (SQLite family, nested repository,
  reparse points, ADS, long paths) and measuring their byte size or file count. Acceptance
  criterion 6 requires that characterization **before any preservation proposal is
  approved**; performing it is not part of this packet, and no route recommendation here
  depends on its outcome.

### Assumptions made

- ⚠️ That the owner wants the scope amendment **defined but not exercised** — the
  deliverable is reviewed proposed text plus a Gate 1 decision, and approving the text
  grants no preservation, no additional source, and no retirement.
- ⚠️ That RESIDUE-1 and RESIDUE-2 remain exactly two, untouched, and unmoved for the
  duration of this packet. A third such child, or the disappearance of either, forces
  reassessment of the requirements rather than a silent count update.
- ⚠️ That the successor guard now on `origin/main` (post-#494) is **unverified in this
  checkout** and is not assumed to preserve the reviewed Operation A behavior. No claim
  about it is made or relied upon.
- ⚠️ That Operation A **deployment state is unmeasured**. Nothing in this packet assumes
  any target is or is not deployed.
- ⚠️ That the 2026-09-28 evidence is a **point-in-time** record, not live state; every
  path, identity, hash, ref, and database family must be revalidated before any approved
  operation.
- ⚠️ That the council, when run, reviews the hunks against the `origin/main` base, and
  that a hunk which does not apply cleanly to it is a finding, not a silent rebase. Hunk
  anchors are absolute line numbers measured against the unamended file, so application
  order matters: apply bottom-up, or re-derive each anchor after each insertion.
- ⚠️ That neither directory is written by a live process. This is **not established** —
  §7.1's runtime map has not been produced — and acceptance criterion 6 therefore requires
  the map to be extended or the absence of a writer recorded, rather than assumed.
- ⚠️ That the amendment is a documentation/design change only, so the change-type table
  requires no test run — on the premise that no source behavior changes. If the council
  concludes any hunk implies a tooling, launcher, or script change, this premise fails and
  the gates must be re-derived.

### Decisions resolved by drafting judgment

These were blocking questions in the previous draft. Each is resolved here from the
evidence, as routine drafting rather than owner policy. They are listed so the owner can
override any of them, but none blocks Gate 0.

| # | Question | Resolution | Basis |
|---|---|---|---|
| D1 | Amendment base | The `origin/main` tracked copy; the divergent local file is preserved untouched. | Owner instruction of 2026-09-28; the two copies differ in exactly one hunk, so Hunks 1–3 are unaffected and Hunk 4 applies cleanly to this base. |
| D2 | §12 wording | The §5.4-based replacement, corrected: monitoring is cited to §11's `PREVENTION_COMPLETE`, not to §5.4; the successor-versus-reviewed reconciliation is named; and an **unchecked** plan-level renewed-Gate-1 item is retained. | The local *"Gate 2 source/publication decision"* wording rests on the superseded premise that publication is open. The packet's own replacement misattributes monitoring to §5.4, which has no monitoring bullet, and drops the only open box tracking a plan-level Gate 1. |
| D3 | Terminology | Reuse the design's existing noun — *unexpected drive-root child* — with an added scope qualifier for "outside B's two named roots and outside an approved source manifest". Mint no second noun. State the discriminator once, define it by path identity, and state that manifest approval never removes a child from the unexpected set. | The design already carries five near-synonyms (§5.1, §5.2, §6, §8.3, §11), all discriminated against the approved baseline. A second noun discriminated against a manifest would go false on approval while *"unexpected"* must stay true, because the baseline is not edited — splitting the §8.3 and §11 checks. Acceptance criterion 12 holds whichever term the owner prefers. |
| D4 | Reciprocal references | Required, and widened: not only §4.2–§4.5 back-references, but the full enumeration sweep of acceptance criterion 10, plus the §7.5 placement of criterion 8 and the §3.6/§3.7 structural-seal sentence of criterion 5. | A new operation class is textually outside §4.4's shared lock and attempt register (*"All B-E live launchers"*, *"every B-E live attempt"*) and outside §4.5's trigger list, §4.3's opener, and §7.5's pre-removal recovery-proof clause. Without the sweep a new operation is **less** governed than the extension it would replace. |
| D5 | Landing path for the amended design | An in-place edit of the tracked `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` (plus `INDEX.md`) on a branch taken from `origin/main`, prepared in the owner-created standalone clone that §1.3 already requires — never from this checkout, and never as a new file. | Editing a tracked file in a globbed surface directory does not trip `Test Inventory Drift`; only adding or deleting one does. §1.3 already requires the standalone clone and the `--check` measurement there. |
| D6 | Where the dated facts live | The backup-disappearance window, the 2026-09-28 creation timestamps, the 2026-09-07 merge date, the PR number, the cancelled check's run identity, and every count stay in `evidence/2026-09-28-state.md` and the private record. The design and `INDEX.md` receive no dated live-history or live-state fact. **Carve-out:** the gate-approval signature dates already in §12 (*"signed 2026-09-05"*) are a durable approval record, not live evidence, and stay. | §1.1: *"Counts, SHAs, branch names, worktree paths, database counts, file counts, process lists, free-space measurements, and remote advertisements belong in dated operation evidence outside this document."* §1.1 does not list approval signatures, and §4.3 requires an approval to bind *"owner, date, and retention deadline"*. Now acceptance criterion 14. |
| D7 | Operation A record | Corrected in three places in one change — the status header, §12, and `INDEX.md` — stating the reviewed source **is merged** as a dateless status, with §5.4's outstanding conditions, §11's active-monitoring requirement, the cancelled post-merge check's disposition, and reconciliation of any successor against the reviewed bytes recorded as **obligations**, not as live-state claims. | Owner instruction of 2026-09-28, as amended by the owner's 2026-09-28 correction that the merge date stays in dated evidence; `"Gate 2"` is undefined in the file and would be orphaned in the header once §12 is corrected. Now acceptance criteria 14 and 17 together. |

### Open questions for the user — all blocking

Four remain. Each is a genuine owner policy choice that changes the amendment's text and
cannot be resolved from the evidence.

**Positions indicated 2026-09-28 — not a signature.** A position on each of the four was
relayed to this session on 2026-09-28, together with two corrections to Section 0 (now
applied as acceptance criteria 13, 14 and 17 and resolutions D6 and D7). The indicated
positions are recorded below and the amendment text is drafted against them. They are
**not** Gate 0 approval: the relaying message itself says the signature has not yet been
given, and this packet does not treat a relayed position as the owner's own signature. The
sign-off boxes stay unchecked until the owner signs directly. This distinction is the exact
one that produced the two divergent `docs/worktree_cleanup/PLANNING.md` lineages, where a
delegated Gate 1 decision self-described as *"not a personally authored owner signature"*
now sits beside the owner's own sign-off.

| # | Indicated position | Status |
|---|---|---|
| 1 | Separate preservation operation | matches the recommendation; drafted against |
| 2 | Separate, later-approved retirement operation | matches the recommendation; drafted against |
| 3 | Known-unexpected register, whose entries are not baseline entries and which does not make the drive-root audit pass | matches the recommendation; drafted against, and specified in full in acceptance criterion 13 |
| 4 | Investigate the historical discrepancy before proposing a successor baseline | matches the recommendation; drafted against |

1. **Preservation route.** Do RESIDUE-1 and RESIDUE-2 enter preservation scope through an
   explicitly gated **extension of Operation C's** owner-approved immutable source
   manifest, or through a **separate preservation operation** with its own manifest, freeze
   budget, gates, and approval? *Recommendation: separate operation.* This choice also
   settles acceptance criterion 7's failure-isolation requirement — a separate operation
   answers it by construction; an extension must answer it in text.
2. **Retirement route.** Is eventual retirement a **separate, explicitly approved
   operation** with its own named §11 outcome; an **amendment to an existing operation**
   (which requires editing either §11's two-root plural aggregate and §4.3's
   *"exactly one malformed-root identity"* binding, or §3.6 condition 1); or **no
   retirement route at all**, with indefinite retention and the question deferred to a
   later packet? *Recommendation: separate operation, built on Operation B's per-root
   template, with a distinct parameterized outcome.*
3. **The standing drive-root audit.** Two known children now sit outside the frozen
   baseline with no scheduled clearing event, while §8.3 requires each closeout to confirm
   no unexpected drive-root child was created and §11 requires active lifecycle monitoring
   for `PREVENTION_COMPLETE`. Do you want an **owner-dispositioned known-unexpected
   register** — exact identity per entry, explicitly not a baseline entry and explicitly
   not making the audit exit zero — or a different disposition? Leaving it unaddressed
   means every B/C/D closeout carries a standing red. *Recommendation: the register.*
4. **Historical baseline successor.** Supplement the preserved 2026-09-06 baseline with a
   new version **now**, or investigate the bounded discrepancy further before any successor
   version is proposed? *Recommendation: investigate first; propose no successor in this
   packet.*

### Section 0 sign-off — GATE 0

**Status: SIGNED — Gate 0 APPROVED by the owner, Yaakov Avihai Shai, 2026-09-28.**
The owner signed directly; no box below was checked on the owner's behalf, and no relayed
position, adviser recommendation, or prior gate was substituted for the signature.

#### Owner approval — verbatim, as given 2026-09-28

> GATE 0 — APPROVED.
>
> I sign Gate 0 for the drive-root scope amendment recorded in
> docs/worktree_cleanup_amendment/PLANNING.md. Record this approval verbatim in that
> file's Section 0 sign-off with my name and today's date, and check all five boxes. This
> approves requirements only. It grants no preservation, no additional source, no
> retirement, no filesystem mutation, and no widening of any existing approval.
>
> My answers to the four blocking questions, as decisions:
>
> 1. Preservation route — a SEPARATE preservation operation, not an extension of
>    Operation C's source manifest.
> 2. Retirement route — a SEPARATE, later-approved retirement operation, built on
>    Operation B's per-root template, with its own distinct parameterized Section 11
>    outcome. Operation B's fixed two-root MALFORMED_ROOTS_QUARANTINED meaning and
>    Operation D's approved-worktree-slice scope are preserved unchanged.
> 3. Drive-root audit — adopt the owner-dispositioned known-unexpected register exactly
>    as specified in acceptance criterion 13. Its entries are not baseline entries, and
>    it does not clear the Section 5.2 audit or make it exit zero.
> 4. Historical baseline — investigate the bounded discrepancy before any successor
>    baseline version is proposed. Propose none in this packet.
>
> I accept acceptance criteria 1-22, the nine flagged assumptions, and drafting
> resolutions D1-D7 as written, including D6's carve-out: the gate-approval signature
> dates already in Section 12 ("signed 2026-09-05") stay, while the 2026-09-07 merge
> date, PR number, CI run identities, counts, paths, and the disappearance window stay in
> dated evidence and never enter the technical design or INDEX.md.
>
> The early targeted rescue decision stays outside this packet — undecided, unselected,
> and not counted among its decisions.

**Owner:** Yaakov Avihai Shai. **Date:** 2026-09-28. **Scope of approval:** requirements
only. The signature authorizes the plan-stage council — and only the council — to run
next. It grants no preservation, no additional source, no retirement, no filesystem
mutation, and no widening of any existing approval.

**The four blocking questions are now decided**, as recorded verbatim above: **Q1 —
separate preservation operation**; **Q2 — separate, later-approved retirement operation on
Operation B's per-root template with its own distinct parameterized §11 outcome, with B's
fixed two-root `MALFORMED_ROOTS_QUARANTINED` meaning and D's approved-worktree-slice scope
preserved unchanged**; **Q3 — the owner-dispositioned known-unexpected register exactly as
specified in acceptance criterion 13, whose entries are not baseline entries and which
does not clear the §5.2 audit or make it exit zero**; **Q4 — investigate the bounded
discrepancy first; propose no successor baseline in this packet.** The positions indicated
on 2026-09-28 and recorded in the table above are, by this signature, decisions.

- [x] **Acceptance criteria.** The owner confirms that acceptance criteria 1–22 match
      intent, including the three revised by the 2026-09-28 corrections: **13** (what the
      known-unexpected register does and does not change), **14** (no dated live-history or
      live-state fact enters the design or `INDEX.md`, with the §12 approval-signature dates
      explicitly carved out), and **17** (the Operation A record is corrected as a dateless
      status plus obligations).
- [x] **Assumptions and drafting resolutions.** The owner reviewed the nine flagged
      assumptions and the drafting-judgment resolutions **D1–D7**, and corrected or accepted
      each one — in particular **D6**'s carve-out keeping *"signed 2026-09-05"* in §12 while
      excluding the merge date, and **D7**'s dateless three-surface correction.
- [x] **Blocking questions.** The owner's own answers to blocking questions **1–4** are
      given. The positions indicated on 2026-09-28 are recorded above and drafted against;
      confirming them here is what makes them decisions.
- [x] **Scope boundary.** The owner confirms that the early targeted rescue decision stays
      outside this packet, undecided and uncounted, and that approving this Gate 0 grants no
      preservation, no additional source, no retirement, and no filesystem mutation.
- [x] **Gate 0 approved.** The owner signs Gate 0 for this scope amendment, which authorizes
      the plan-stage council — and only the council — to run next.

On this signature, and without further permission, the next steps are: `product-manager`
writes Plan v1 against the `origin/main` base with Hunks 1–4 re-drafted to the four answers
plus the two dateless hunks; `architecture-reviewer`, `test-strategist` and
`product-risk-reviewer` run independently and in parallel against that same Plan v1, with
no reviewer shown another's findings before completion; every finding is dispositioned into
a response matrix; `product-manager` writes Plan v2; and work stops for the owner's Gate 1
decision. No hunk is applied to the technical design as approved text at any point before
Gate 1.

**Council status.** Gate 0 is signed, so the plan-stage council — `architecture-reviewer`,
`test-strategist`, `product-risk-reviewer` — is **authorized**. Its live status is recorded
under *Reviewer findings* below and nowhere else; this paragraph asserts no outcome.

> **Recorded defect in this artifact's own history.** An earlier revision of this paragraph,
> written at the moment Gate 0 was signed and before any reviewer had been spawned, asserted
> that the council *"has been run"* and that its findings were *"recorded under Reviewer
> findings below"*. Both statements were false when written; the *Reviewer findings*,
> *Response matrix*, and *Agent provenance* sections still read `NOT STARTED` at that time.
> `architecture-reviewer`, `test-strategist` and `product-risk-reviewer` each independently
> caught it (AR-none, TS-1, PR-14) while it was still false, and it is corrected above. It is
> recorded rather than quietly removed because it is exactly the failure root `CLAUDE.md` §3
> names: *"A review that did not run, or whose reviewer failed, is incomplete — never record
> it as 'no findings' or 'refuted', and never let it move an approval status."* It moved no
> approval status, and no Gate 1 or Plan v2 box was checked on its strength.

Gate 1 remains **unsigned**: no hunk is applied to the technical design as approved text.

**Gate 0 advisers are not the council.** Three independent advisers were consulted on
blocking questions 1 and 2 before this draft was revised. They are recorded under *Agent
provenance* below as Gate 0 consultation, they are read-only, they are not
`architecture-reviewer`, `test-strategist`, or `product-risk-reviewer`, and they cannot
approve Gate 0 or substitute for the council. Their unanimity is not a Gate 1 finding.

**Gate 1 is not Gate 0.** Operation A's 2026-09-05 Gate 1 sign-off was not, and cannot be
treated as, Gate 0 approval for this scope. It approved Operation A Plan v2 only.

---

## Plan v1

**Goal**: Produce the exact, final, quotable amendment text that gives a drive-root
directory outside Operation B's two named roots and outside Operation C's approved
source scope a defined classification, a gated route to preservation, a gated route to
eventual retirement, a determinate closeout meaning, and an accurate dateless record of
Operation A — without approving any source, any target, any removal, or any filesystem
mutation.

### Scope

**In**

- Six hunks (A below) and twenty-four enumeration-sweep edits (B below) against the
  `origin/main` tracked base of `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`, plus one
  hunk against the `origin/main` tracked base of `docs/ai_workflow/INDEX.md`.
- A new `## 14.` section in the technical design carrying the contracts for two new
  separately approved operation classes — **Operation F** (additional-source
  preservation) and **Operation G** (drive-root child retirement) — and the
  owner-dispositioned known-unexpected register.
- Enrolment of F and G by name in every place the design quantifies over operations,
  or a written reason that place is inapplicable.
- Reciprocal cross-references from §4.2, §4.3, §4.4 and §4.5 to §14 (resolution D4).

**Out**

- Applying any hunk. Plan v1 contains proposed text as quoted blocks only. No hunk is
  applied to `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` or
  `docs/ai_workflow/INDEX.md` before Gate 1.
- Naming, proposing, approving, or characterizing any actual source or target.
  RESIDUE-1 and RESIDUE-2 are never named, pathed, hashed, counted, or enumerated in
  the proposed text; they are not manifest entries and not register entries here.
- Any filesystem mutation, preservation copy, protective copy, quarantine, move,
  deletion, junction unlink, archive-ref creation, prune, worktree add/remove, or ref
  change.
- The early targeted rescue decision. It stays outside this packet, undecided,
  unselected, and uncounted; it is deliberately **not** added to §12's decision list,
  because adding it there would both count it and place a live-sequence exception in a
  stable-policy surface.
- Editing §5.2's audit, the owner-approved 2026-09-06 baseline, or `docs/test_inventory/`.
- Either divergent lineage of `docs/worktree_cleanup/PLANNING.md`.

### Naming the two new operation classes

The design letters its operations A–E. The two classes the owner's Q1 and Q2 answers
create are therefore lettered **F** and **G**, in dependency order (G consumes F's
outcome). Letters keep the enumeration sweep mechanical: every `B-E` range quantifier
widens to `B-G` and stays a range, rather than growing an ad-hoc list that the next
reader can silently under-read.

| Class | Full name | Template it is built on | Named §11 outcome |
|---|---|---|---|
| **F** | Operation F — separately approved additional-source preservation | Operation C's capture, encryption, off-machine and isolated-restore gates, applied per source | `ADDITIONAL_SOURCE_PRESERVED(source)` |
| **G** | Operation G — separately approved drive-root child retirement | Operation B's per-root archive-and-quarantine template | `DRIVE_ROOT_CHILD_RETIRED(root)` |

Both outcomes are parameterized per root/source. **The amendment defines no plural
aggregate over either class**, and says so, because §8.1 permits only *"Section 11's
exact named outcome"* to be claimed and an unqualified plural over an open set would be
unclosable and would invite the exact widening criterion 4 forbids.

### Terminology — D3 governs, and overrides the source packet

The source packet proposed the noun **"unapproved drive-root child"**
(`AMENDMENT_2026-09-28.md`, *Terminology*). **Drafting resolution D3 overrides that**,
and Plan v1 records the override explicitly:

- The design already carries five baseline-discriminated near-synonyms — *"unintended"*
  drive-root child (§5.1), *"unexpected new children"* (§5.2), *"other unexpected root"*
  (§6), *"unexpected drive-root child"* (§8.3), *"unexpected drive-root children"*
  (§11). The amendment **mints no second noun**. It reuses `unexpected drive-root child`
  and adds a **scope qualifier**: *outside approved operation scope*.
- **The discriminator is stated once**, in §14.0, and defined **by path identity**, not
  by approval status.
- `"unapproved"` is rejected for a specific reason the approved text records: it would
  go **false** the moment a manifest approval landed, while `"unexpected"` must stay
  **true**, because the owner-approved baseline is not edited. A term that flips on
  approval would split the §8.3 and §11 checks from §5.2's audit.
- The approved text therefore states that **entering an approved source or target
  manifest never removes a child from the unexpected-drive-root set** checked by §8.3
  and §11. Only the *scope qualifier* stops applying; the noun does not.

### Anchor mechanics — declared, not assumed

The source packet's anchors are absolute line numbers measured against the unamended
file, so application order matters.

**Chosen discipline: strictly bottom-up (descending base line number), single pass, no
re-derivation.** Every anchor below is an absolute line number in the amendment base,
and every anchor stays valid because no earlier-applied edit ever sits above a
later-applied one. The alternative — re-deriving after each insertion — was rejected: it
multiplies the number of derivations by the number of edits (thirty-one here) and every
derivation is an opportunity to land a paragraph in the wrong section.

**Every anchor below was re-derived by this `product-manager` against the extracted
`origin/main` blob** (`git hash-object` = `1b41922e795e9202f128a9b1122d0ffb6c6134af`,
1471 lines, equal to the `origin/main` blob OID for
`docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`) and against the extracted `INDEX.md` blob
(`027af297b1658f70f353dd298c545fa4108c6def`, 91 lines), not against this dirty
checkout's working-tree copies.

**Anchor resolution result: all thirty-one plan-file anchors and the one `INDEX.md`
anchor resolve cleanly against the base. No hunk failed to apply and nothing was
silently rebased.** Two anchors differ from the source packet's description and the
difference is recorded rather than absorbed:

| Source packet says | Base says | Disposition |
|---|---|---|
| Hunk 2 lands in §7.2, *"insert after line 923"* | Line 923 is `   Archive-to-itself or upload-to-download equality alone is insufficient.` — the anchor is correct | **The anchor resolves, but the hunk is relocated by decision, not by anchor failure.** See A/Hunk 2. |
| Hunk 4 replaces the §12 Gate 1 checkbox | Base line 1389 is `- [ ] Approve the Gate 1 council-reviewed version of this plan.` | Confirmed; this is the one line where the base and the local working copy differ |

### A. The six hunks

All six are against the `origin/main` base. All are dateless except the §12
gate-approval signature date that D6's carve-out explicitly keeps.

---

#### Hunk 1 — §1.2, definition and boundary, re-drafted for a separate operation

**Why re-drafted.** As written, Hunk 1 said *"Extending Operation C's source manifest to
an exact, closed set of such children requires its own council review and owner
approval"*. That sentence pre-commits the route the owner did **not** choose. It also
fails criterion 2 twice: read alone it names C's manifest as the destination, and it
offers no anchor to an approval record distinct from the amendment introducing it.

**Anchor.** Insert after base line 95, the last line of the technical-dependencies
bullet list. Exact anchor line 95:

> `  TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED, not successful worktree retirement.`

Line 96 is blank; line 97 is `### 1.3 Planning-artifact landing gate`.

**Proposed text** (two independence bullets continuing the list, then the boundary
paragraph):

```
- F does not depend on B, C, D, or E. No D slice, no E operation, and no
  PRESERVATION_COMPLETE waits on it, and an F failure blocks only G for that same
  source identity.
- G depends only on its own approval and on ADDITIONAL_SOURCE_PRESERVED already
  proved for its exact source identity. It is not part of worktree-cleanup
  completion.

An unexpected drive-root child is outside approved operation scope when it is neither
of Operation B's two named roots nor inside an approved operation source manifest.
Such a child is retained and recorded only. Proximity to a named root, a
generated-output classification, a filesystem creation time, or a previous campaign's
completion receipt creates no preservation, relocation, quarantine, or removal
authority for it, and neither does any existing aggregate, receipt, approval record,
manifest, or baseline entry in this plan. Section 14 defines the shape of two
separately approved operations, F and G, that the owner could later commission for
such a child. Section 14 approves neither. This plan names no source and no target for
either, and authority for either exists only under a dated Section 4.3 owner approval
record created separately from, and after, this plan text. Completing either changes
no Operation B aggregate, no Operation C PRESERVATION_COMPLETE, no Operation D
worktree-slice outcome, and no PREVENTION_COMPLETE declaration, and permits neither an
edit to the owner-approved drive-root baseline nor a zero exit from the Section 5.2
audit.
```

---

#### Hunk 2 — **relocated to §7.5**, discovery is not a source grant

**Where it lands and why.** The source packet placed this text in §7.2, after item 5,
and worded it as *"…names additional drive-root sources… enumerate each… in C's
immutable source manifest"*. With a separate preservation operation, that text must not
land in §7.2 at all:

- §7.2 is the contract for **Operation C's** whole-tree cold copy of the approved
  `D:\development` scope. Putting additional-source language there attaches the new
  route to C's scope paragraph — the single highest-risk surface under criterion 2,
  because a reader who lands on §7.2 alone sees C's manifest and additional drive-root
  sources in the same breath.
- The obligations the §7.2 paragraph restated (items 1–5, §7.5 and §7.6 gates, capacity
  and freeze recalculation) are now carried by §14.1 **as obligations, named rather than
  cited by item number where the item's text is scope-specific**, which is what
  criterion 6 asks for.
- **§7.2 is therefore proposed unchanged.** That is a decision, and Plan v1 records it
  so the council can contest it.

What remains genuinely §7.5's business is exactly what criterion 8 requires to be in
§7.5 itself: the discovery rule and the tightening of the *"explicit owner paths"* hook.

**Anchor.** Replace base lines 990–992, the opening paragraph of §7.5 (§7.5's heading is
line 988). Exact base text:

> ```
> 990  Inventory every root discovered in the pre-stop runtime map plus the repository,
> 991  artifacts, recovery/backup directories, local application-data roots, and explicit
> 992  owner paths.
> ```

**Proposed replacement text**:

```
Inventory every root discovered in the pre-stop runtime map plus the repository,
artifacts, recovery/backup directories, local application-data roots, and the owner
paths enumerated in C's approved immutable source manifest. A path is an inventory
target only because one of those categories covers it; being named by the owner
somewhere outside the approved manifest does not make it one.

This inventory is a discovery obligation, not a source grant. When it observes a
drive-root directory outside C's approved source scope, that directory is recorded and
retained only: discovery never adds it to an immutable source manifest, and discovery
alone obliges no capture. Adding any such directory to a source manifest requires the
separate Operation F approval of Section 14.1, which this plan does not give.
```

---

#### Hunk 3 — §11, the two named outcomes and the retirement boundary

**Why re-drafted.** The source packet's Hunk 3 opened *"Preserving an additional
drive-root source **under C**…"*, which again pre-commits the extension route, and it
defined **no named outcome at all** — leaving the new class unclosable under §8.1.

This hunk has two anchored parts, both in §11.

**Hunk 3a — anchor.** Insert after base line 1372, the last bullet of §11's outcome
list. Exact anchor line 1372:

> `- MAIN_RECONCILIATION_COMPLETE: E's independent plan passes.`

**Proposed text**:

```
- ADDITIONAL_SOURCE_PRESERVED(source): that one Operation F source, bound by exact
  canonical/final path and physical identity in F's approved immutable source
  manifest, has an Operation F live capture with VERIFIED_CLEAN_CLOSEOUT in the shared
  register, maintenance restored where F suspended it, no F-caused BLOCKED_RECOVERY
  remaining, a passing final capture receipt, and every Section 14.1 whole-tree,
  encryption, off-machine, and isolated-restore gate passing for that exact source.
  The outcome is defined per source. This plan defines no plural aggregate over
  Operation F sources; a plural claim would require a later amendment naming an exact
  closed set and reviewed under Section 1.1. ADDITIONAL_SOURCE_PRESERVED(source) is
  not an input to PRESERVATION_COMPLETE, neither contributes to nor blocks it, and
  authorizes no Operation B, D, or E step.
- DRIVE_ROOT_CHILD_RETIRED(root): that one Operation G root, bound by exact
  canonical/final path and physical identity in G's approved immutable target
  manifest, has ADDITIONAL_SOURCE_PRESERVED already proved for that same identity, has
  a VERIFIED Operation G attempt with the complete Section 4.4 clean-closeout protocol
  and final root receipt, is absent from its original path, is exact in its
  operation-specific nonexistent same-volume quarantine destination, and is
  independently recoverable off-machine from the stored secret. The outcome is defined
  per root. This plan defines no plural aggregate over Operation G roots. It does not
  alter, satisfy, or contribute to MALFORMED_ROOT_QUARANTINED(root),
  MALFORMED_ROOTS_QUARANTINED, PRESERVATION_COMPLETE, PREVENTION_COMPLETE,
  TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED, WORKTREE_SLICE_COMPLETE,
  WORKTREE_SLICE_PARTIAL_CLOSED, or WORKTREE_CLEANUP_COMPLETE, and is not part of any
  of them.
```

**Hunk 3b — anchor.** Insert after base line 1384, the last line of §11's retention-exit
paragraph. Exact anchor line 1384:

> `operations with new exact manifests. Nothing expires automatically.`

Line 1385 is blank; line 1386 is `## 12. Open owner decisions before execution`.

**Proposed text**:

```
Preserving a source under Operation F grants no quarantine, relocation, or removal
authority for it. No Operation F receipt, Operation B receipt, Operation C receipt,
Operation D receipt or campaign target set, approval record, or baseline entry in this
plan authorizes an Operation G step; Operation G authority exists only under its own
dated Section 4.3 owner approval, created separately from and after this plan text.
Operation G's route is archive plus non-overwriting same-volume quarantine and never
recursive deletion, so completing it deletes nothing. Permanent deletion of an
Operation F preservation object or an Operation G quarantine payload remains a
separate later operation with its own exact manifest and owner approval, exactly as
for B and C above.
```

---

#### Hunk 4 — §12, the Operation A record, corrected per D2

**Anchor.** Replace base line 1389. Exact base text:

> `- [ ] Approve the Gate 1 council-reviewed version of this plan.`

Line 1388 above it is `- [x] Approve Gate 0 requirements (requirements only; signed
2026-09-05).` — unchanged, per D6's carve-out.

**Proposed replacement text**:

```
- [x] Approve Operation A Plan v2 at Gate 1 (signed 2026-09-05); this approved neither
      B-G execution nor any later semantic amendment to this design.
- [ ] Approve the renewed plan-level Gate 1 that Section 1.1 requires for the
      council-reviewed version of this plan after each later semantic amendment.
- [ ] Complete Section 5.4's remaining Operation A conditions - deployment, owner
      installation verification, the interception and profile captures, and
      active-guidance coverage - together with Section 11's PREVENTION_COMPLETE
      requirement that lifecycle monitoring is active; dispose of the cancelled
      post-merge required check; and reconcile any successor of the reviewed guard and
      test artifact against the reviewed bytes before the deployment decision. The
      reviewed source is merged.
```

**How this satisfies D2.** Monitoring is cited to **§11's `PREVENTION_COMPLETE`**
(*"lifecycle monitoring is active"*), **not** to §5.4, which carries no monitoring
bullet — the source packet's replacement misattributed it. The
successor-versus-reviewed-bytes reconciliation is named. An **unchecked** plan-level
renewed-Gate-1 item is retained, which the source packet's replacement dropped. No merge
date, PR number, or run identity enters the design (criterion 14); the merged state is
stated as status. The `"signed 2026-09-05"` signature dates stay (D6 carve-out).

---

#### Hunk 5 — the status header, dateless (new in this packet)

**Anchor.** Replace base lines 8–10 up to the sentence boundary. The header paragraph is
lines 6–12. Exact base text of the replaced span:

> ```
>  8  and verified disposable interactive Windows acceptance. Gate 2 and the remaining
>  9  publication, installation and monitoring obligations remain open; PREVENTION_COMPLETE
> 10  is not declared. B, C, and D still require the operation-specific owner approvals
> ```

**Proposed replacement text** (lines 8 onward; lines 6–7 and 11–12 unchanged except for
the F/G sentence appended before the closing sentence):

```
and verified disposable interactive Windows acceptance. Operation A's reviewed guard
and test source is merged. What remains open for Operation A is stated as obligations:
Section 5.4's outstanding conditions, Section 11's requirement that lifecycle
monitoring is active, the disposition of the cancelled post-merge required check, and
the reconciliation of any successor of the reviewed artifact against the reviewed
bytes; PREVENTION_COMPLETE is not declared. B, C, and D still require the
operation-specific owner approvals below and the independent Windows-filesystem
review. E remains a separately planned and approved operation, as do the Section 14
operations F and G, neither of which is approved here. This factual status correction
changes no technical contract.*
```

**What this removes and why.** The stale *"the remaining publication … obligations
remain open"* assertion goes, because the reviewed source is merged. The orphaned
`"Gate 2"` name goes: it occurs only in this header and in the local working copy's §12
checkbox, and is **defined nowhere in the file** — §5.4 is *"Gate A"*. **No merge date,
PR number, CI run identity, or count is introduced** (criterion 14).

---

#### Hunk 6 — `docs/ai_workflow/INDEX.md`, dateless (new in this packet)

**Anchor.** Replace `INDEX.md` base lines 61–65 (blob
`027af297b1658f70f353dd298c545fa4108c6def`). Exact base text:

> ```
> 61  - [Worktree Cleanup and Preservation Plan](WORKTREE_CLEANUP_PLAN.md) — phase-gated,
> 62    slice-based path-conversion prevention, malformed-root quarantine, whole-tree
> 63    preservation, worktree retirement, and separately approved main reconciliation;
> 64    planning only with Gate 0 signed and Gate 1 plus the Windows-filesystem review
> 65    pending
> ```

**Proposed replacement text**:

```
- [Worktree Cleanup and Preservation Plan](WORKTREE_CLEANUP_PLAN.md) — phase-gated,
  slice-based path-conversion prevention, malformed-root quarantine, whole-tree
  preservation, worktree retirement, separately approved main reconciliation, and the
  separately approved routes for drive-root children outside Operations B and C;
  planning only. Gate 0 and Operation A Plan v2 Gate 1 are signed. Pending: the
  independent Windows-filesystem review, the renewed plan-level Gate 1 that later
  semantic amendments require, and Operation A's remaining deployment, installation,
  acceptance, and monitoring obligations
```

Dateless (criterion 14). No sentence reads as approving a scope, source, or removal
(criterion 2) — *"separately approved routes"* names the shape, not an approval.

---

### B. The enumeration sweep — acceptance criterion 10

The sweep was run against the base by grepping the quantifier families `B-E`, `B–E`,
`B, C, or D`, `B, C, and D`, `B/C/D`, `A-D`, `C/D`, `D and E`, `Operation [A-E]`, and
`the relevant operation`, then reading each hit in context. **Twenty-nine quantifier
sites were found.** The mandated eleven are all present and all addressed; **eight sites
beyond the mandated list were found and are reported below**, marked ★.

Everything in this sweep lands as a *carrier* section plus enrolling edits.

#### B.0 The carrier — new `## 14.` section (edit **N**)

**Placement decision and its trade-off.** The new section is **appended at end of file,
after base line 1471**, as `## 14.` with subsections 14.0–14.3.

- Chosen because inserting a new operation section between §9 (Operation E) and §10
  would renumber §10–§13, breaking every in-file cross-reference (`Section 10`,
  `Section 11`, `Section 11's exact named outcome` in §8.1, `Section 4.4`-style
  references are unaffected but `Section 11` references are not) and every external
  reference in this council artifact and the dated evidence. Silent renumbering of a
  signed design is a worse hazard than an appendix ordering wart.
- The cost is honest and recorded: §13 (*Review dispositions*) is a historical
  appendix, so §14 sits after an appendix. This is mitigated because **every** reader
  path into the new material is explicitly cross-referenced from §1.2, §2.2, §4.1–§4.5,
  §7.5, §7.6, §8.3, §10, §11, and §12 by the edits below — a reader cannot reach the new
  route only by scrolling.
- The considered alternative was a `## 9A.` heading between §9 and §10, which preserves
  reading order with zero renumbering but introduces a non-numeric section label. **This
  is an explicit decision point for the council.**

**Anchor.** Append after base line 1471, the last line of the file:

> `  aware disposition without treating PR state as removal authority.`

**Proposed text**:

```
## 14. Drive-root children outside Operations B and C

### 14.0 Scope, terminology, and what this section does not do

An unexpected drive-root child - the term Sections 5.1, 5.2, 6, 8.3 and 11 already
use, discriminated against the owner-approved drive-root baseline - is **outside
approved operation scope** when its exact canonical/final path and physical identity
are neither of Operation B's two named roots nor enumerated in an approved operation
source manifest. That is the only discriminator, it is stated once here, and it is a
statement about path identity, not about approval status or about who created the
directory.

Entering an approved source or target manifest never removes a child from the
unexpected-drive-root set checked by Sections 8.3 and 11. The owner-approved baseline
is not edited by any manifest approval, so a child that is unexpected stays unexpected
for as long as the baseline says so; only the scope qualifier above stops applying.
The term "unapproved drive-root child" is deliberately not used, because it would go
false at the moment of manifest approval while "unexpected" must stay true, splitting
the Section 8.3 and Section 11 checks from the Section 5.2 audit.

This section defines the **shape** of two separately approved operations. It approves
neither, names no source and no target, and widens no existing approval. Authority for
either exists only under a dated Section 4.3 owner approval record created separately
from, and after, this text. No existing aggregate, receipt, approval record, manifest,
or baseline entry in this plan authorizes any step of either operation. Completing
either neither changes PREVENTION_COMPLETE nor permits an edit to the owner-approved
drive-root baseline nor a zero exit from the Section 5.2 audit.

Operation B is unchanged. MALFORMED_ROOT_QUARANTINED(root) and
MALFORMED_ROOTS_QUARANTINED continue to mean exactly Operation B's two named roots and
nothing else; Section 4.3's binding of exactly one malformed-root identity to a B
approval is unchanged; and no Operation B receipt, approval record, or quarantine
destination may cover any other root. An Operation G approval is never an Operation B
approval, and an Operation G launcher may not emit an Operation B outcome name.

Operation D is unchanged, and the structural seal is stated here rather than relied
on: a drive-root directory can never satisfy Section 3.6 condition 1, which requires a
registered immediate child of the approved development parent; it can therefore never
be an ELIGIBLE row, can never record a Section 3.5 positive lifecycle basis, and can
never enter a Section 3.7 immutable cleanup target set. It follows that no drive-root
directory can affect WORKTREE_SLICE_COMPLETE, WORKTREE_SLICE_PARTIAL_CLOSED,
TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED, or WORKTREE_CLEANUP_COMPLETE, in either
direction.

### 14.1 Operation F - separately approved additional-source preservation

Operation F preserves one exactly identified source that Operation C's approved scope
does not cover. It is a separate operation, not an extension of Operation C's
immutable source manifest, and no Operation C manifest, approval, receipt, freeze
budget, or capacity approval is altered, reused, or extended by it.

An Operation F proposal is assessable only when all of the following hold.

1. It enumerates an exact, closed set of sources by canonical/final path and physical
   identity. Wildcard or prefix expansion, source-to-source overlap,
   source-to-destination overlap, overlap with Operation C's primary scope, a missing
   source, and a changed identity are each a rejection, not a warning.
2. Each source carries, as obligations rather than by item number where the cited
   item's text is scope-specific: no-follow enumeration and cold copy with reparse
   entries recorded as inert metadata; live-source manifests generated immediately
   before and after capture and required identical, compared directly with the
   extraction rather than by archive-to-itself or upload-to-download equality; raw
   SQLite family capture before any open, with integrity, foreign-key, schema, and
   logical checks on disposable or online copies only; preservation of ignored,
   untracked, local-settings, evidence, loose-file and unique local payload; separate
   exact archives for any ordinary private environment; volatile cache and log paths
   recorded separately; authenticated encryption with two independent offline custody
   copies under Section 7.5's key controls; private off-machine versioned upload,
   fresh-root download, ciphertext verification, decryption, and exact member/hash
   comparison; and Section 7.6's whole-tree source-to-restoration equality proved in a
   fresh isolated root.
3. It states the per-source extraction root, and states how whole-tree
   source-to-restoration equality is proved across disjoint sources: each source is
   proved separately against its own extraction root, and no union or aggregate
   comparison substitutes for a per-source proof.
4. It extends Section 7.1's runtime map and writer-shutdown set to each source, or
   records for each source why no writer exists. An unresolved writer or unresolved
   root blocks Operation F for that source, exactly as it blocks Operation C.
5. Its capacity requirement and freeze budget are calculated for the complete set, not
   per source in isolation, and re-measured immediately before writing under Section
   7.2 item 3's margin. **The owner re-approves the maximum freeze duration for
   Operation F. A maximum approved for Operation C, or for an earlier Operation F,
   never carries over.**
6. Each source contains at least one member class that has been characterized -
   SQLite family, nested repository, reparse point, alternate data stream, long path -
   before approval. An uncharacterized source is not approvable.

**Failure isolation.** A defect, overrun, or unresolved identity on an Operation F
source aborts or blocks only that Operation F source capture, under Operation F's own
safe-abort boundary and its own Section 4.5 recovery playbook. It never aborts,
blocks, delays, or alters Operation C's D:\development capture, and Section 7.2's
abort branches govern Operation C only. **PRESERVATION_COMPLETE is unchanged by this
section**: it remains Operation C's outcome, computed from Operation C's gates over
Operation C's approved scope only, so a pre-amendment and a post-amendment Operation C
receipt remain directly comparable. An Operation F failure does not block Operation D
or Operation E; it blocks only Operation G for that same source identity.

### 14.2 Operation G - separately approved drive-root child retirement

Operation G is built on Operation B's per-root template: archive, then a single
ordered non-overwriting move to a nonexistent operation-specific same-volume
quarantine destination. It never uses recursive deletion and never uses Operation D's
worktree-removal transaction core. Permanent deletion of a quarantine payload remains
Section 11's separate later operation.

No Operation G retirement authority exists for a root until every one of the following
is true for that exact identity:

1. ADDITIONAL_SOURCE_PRESERVED(root) is proved, including a **proved off-machine
   restore from the stored secret** for that exact source - the analogue of Section
   7.5's proof requirement, which Section 7.5 now states covers an Operation G
   retirement move as well as a B quarantine move or a D removal.
2. An exact immutable, digest-bound, positive, non-empty target manifest names that
   one root and its single nonexistent same-volume quarantine destination.
3. Section 4.2's non-LLM human and Windows-filesystem review has been performed
   against that actual mutation surface, with fresh scratch proofs for every path form
   a drive-root source or destination introduces. A prior review of another
   operation's surface does not satisfy it.
4. Section 4.3 manifest and production-package digest integrity and the owner's
   approval are recorded in a durable approval record outside every source and
   candidate.
5. A Section 4.4 journal is kept, and the shared Section 4.4 coordination lock and
   shared attempt register are used on the same single-hold protocol as every other
   live launcher.
6. A Section 4.5 recovery playbook for Operation G is approved and its scratch drills
   pass before the first live mutation.
7. A retention start and a per-object retention period are stated, and Section 11's
   named retention-exit checks apply to the resulting quarantine payload.

Operation G uses its own thin root-quarantine launcher built from the same reviewed
template as Section 4.1 item 2, bound to its own approved single-root manifest, its
own journal, and Operation G's own outcome name. It is not Operation B's launcher and
cannot emit an Operation B outcome. A failure for one Operation G root does not
invalidate another root's completed operation, and no Operation G attempt may
overwrite a prior attempt's evidence.

### 14.3 The owner-dispositioned known-unexpected register

The register is a durable owner record of unexpected drive-root children that are
already known and dispositioned as retained.

**What it changes.** Section 8.3's closeout check is "confirm no unexpected drive-root
child was created" - a delta over the operation window, not a census. The register
pins, by exact canonical/final path and physical identity, the set of unexpected
drive-root children already recorded before an operation began. A closeout therefore
compares the post-operation drive-root enumeration against the owner-approved baseline
**union** the register as frozen at that operation's start, and fails on a child newly
created during the operation. A pre-existing registered child is not a closeout
failure. A newly created child is a closeout failure whether or not it resembles a
registered entry. The register also gives Section 11's requirement that unexpected
drive-root children "remain consistent with their closeout manifest" a determinate
meaning for a child that belongs to no operation's manifest: each registered entry
must be unchanged at its recorded identity at closeout.

**What it does not change.** The register does not clear, suppress, alter, or
reinterpret the Section 5.2 read-only drive-root audit, which continues to compare
configured drive roots against the owner-approved baseline and to report every
unexpected child. **That audit's non-zero exit is unchanged and expected.** A
registered entry is neither a reason to suppress that report nor a reason to ignore
it. A register entry is **not** a baseline entry: it is not added to the baseline, and
it alters none of the baseline's bytes, approver, approval timestamp, or RESOLVED
meanings. It is not a source-manifest entry and not a target-manifest entry. It
confers no preservation, relocation, quarantine, or removal authority, and it is not a
disposition any operation may act on. Section 6's post-operation observation of the
configured drive-root allowlist is likewise unaffected: detection is never suppressed.

**Its own integrity.** Each entry carries an exact canonical/final path and physical
identity, the owner's disposition, and the fact that the child is retained. An entry
is added, amended, or removed only by owner decision - never by an executor, an audit
run, a closeout, or an agent. The register is frozen for the duration of an operation,
from that operation's start through its closeout, so that the delta above is
computable and an after-the-fact addition cannot retroactively excuse a child created
during that operation.
```

#### B.1 The sweep table

Every edit below is an absolute base-line anchor. **Application order is strictly
descending by anchor line**, given in the ordered list after the table.

| # | Site | Exact base text (line) | Enrolling edit, or reason inapplicable |
|---|---|---|---|
| S1 | §1.2 rollout order | `      -> consider E only under its separate plan and approval` (63) | **Enroll.** Insert after line 63: `      -> consider F and G only under their separate plans and approvals (Section 14)` |
| S2 | §1.2 sequence bypass | `No technical independence below permits B-E to bypass that sequence. During the` (65) | **Enroll.** `B-E` → `B-G` |
| S3 | §1.2 dependency graph | `          +--> E. Main reconciliation under a separate approval` (83) | **Enroll.** Append after line 83: `    \|` / `    +--> F. Separately approved additional-source preservation (Section 14.1)` / `          \|` / `          +--> G. Separately approved drive-root child retirement (Section 14.2)` — F hangs off A, not C, because §14.1 isolates F from C by construction; G hangs off F |
| S4 | §1.2 filesystem-proof precondition | `The shared Windows-filesystem proof in Section 4 is required before B, C, or D uses` (85) | **Enroll.** `before B, C, or D uses` → `before B, C, D, F, or G uses` |
| S5 ★ | §1.3 landing gate | `The first Gate 1 implementation decision is for Operation A only. Sections B-E retain` (108) | **Enroll.** `Sections B-E retain` → `Sections B-E and the Section 14 operations retain` |
| S6 | §2.2 rule 2 | `2. During A-D, never run a mutating worktree prune, manually delete .git/worktrees` (170) | **Enroll.** `During A-D` → `During A-D, F, and G`. The range is widened rather than replaced so E's narrow rename exception, stated later in the same rule, is untouched |
| S7 | §2.2 rule 3 | `3. Disable automatic Git maintenance for every cleanup Git child. During each C/D` (177) and `   live freeze, and any future E live-mutation window, suspend scheduled/background` (178) | **Enroll, partially, with a stated reason.** → `During each C/D live freeze, any Operation F live freeze whose approved source contains a live Git repository, and any future E live-mutation window, suspend…`. **Operation G is deliberately excluded**, matching Operation B: a same-volume quarantine move of a drive-root directory outside the repository does not require Git-maintenance suspension, and the amendment records that reason rather than widening silently |
| S8 | §2.2 rule 6 | `6. For every B-E preservation/cleanup command that invokes Git against live or` (194) | **Enroll.** `B-E` → `B-G` |
| S9 | §2.2 rule 20 retention clock | `    after the relevant operation and a successful normal-development observation.` (252) | **Enroll by name.** → `after the relevant operation, including each Operation F source capture and each Operation G quarantine payload, and a successful normal-development observation.` *"The relevant operation"* already quantifies universally, but criterion 10 requires enrolment **by name**, and criterion 9 requires G's retention clock to be unmistakable |
| S10 | §4.1 staging item 1 | `1. Before B or C, approve an early shared package containing the no-follow` (453) | **Enroll.** `Before B or C` → `Before B, C, or F` |
| S11 | §4.1 new staging item | `   removal surface speculatively.` (463) | **Enroll.** Insert item 5 after line 463: `5. Operation F uses the same established copy/archive/encryption wrappers as C and requires no new mutation primitive. Operation G uses its own thin root-quarantine launcher built from the same reviewed template as item 2, bound to its own approved single-root manifest and its own outcome name; it is not B's launcher. Neither F nor G may use D's worktree-removal transaction core, and no new removal surface is built for either.` |
| S12 ★ | §4.1 launcher cardinality | `approved immutable manifest and verifies its recorded digest. B handles exactly one` (475) and `root, C one live capture phase, and E one live maintenance window. One D launcher` (476) | **Enroll.** → `B handles exactly one root, C one live capture phase, F one approved source, G exactly one root, and E one live maintenance window.` |
| S13 | §4.2 human review (D4 reciprocal) | `an adversarial race-proof sandbox.` (502) | **Enroll + reciprocal.** Insert after line 502: `This review is required for an Operation F source capture and an Operation G root move exactly as it is for B, C, and D, and it must add fresh scratch proofs for every path form a drive-root source or quarantine destination introduces (Section 14). A prior review of a different operation's mutation surface never satisfies it.` |
| S14 | §4.3 opening enumeration (D4 reciprocal) | `Each B root operation, C preservation run, D slice, and future E operation uses an` (506) | **Enroll.** → `Each B root operation, C preservation run, D slice, future E operation, Operation F source capture, and Operation G root operation (Section 14) uses an…` |
| S15 ★ | §4.3 common approval fields | `Every B root-operation and D slice approval binds these common fields:` (515) | **Enroll.** → `Every B root-operation, D slice, Operation F source-capture, and Operation G root-operation approval binds these common fields:` |
| S16 ★ | §4.3 operation-specific bindings | `operation are absent, never populated with dummy values.` (531) | **Enroll.** Insert after line 531: `An Operation F approval additionally binds exactly one source identity, its extraction root, its destination identity, its freeze budget with the owner-approved maximum freeze duration approved for Operation F itself, its safe-abort boundary, and its expected capture/restore results. An Operation G approval additionally binds exactly one drive-root child identity, one nonexistent same-volume quarantine destination, its single ordered move, the ADDITIONAL_SOURCE_PRESERVED evidence for that exact identity, and its retention start and per-object retention period. An Operation G approval is never an Operation B approval, and no Operation B approval may bind an Operation G root.` |
| S17 | §4.4 shared lock (D4 reciprocal) | `All B-E live launchers use one fixed owner-approved coordination-file path` (551) | **Enroll — mandatory.** `All B-E live launchers` → `All B-G live launchers`. The owner stated that a new operation outside §4.4's shared lock and attempt register is not acceptable |
| S18 | §4.4 attempt register | `B-E live attempt and closeout. Every read, append, and flush occurs while holding the` (560) | **Enroll — mandatory.** `B-E live attempt` → `B-G live attempt` |
| S19 ★ | §4.4 restore-gate poisoning rule | `closeout blocks D and E through Gate C; it does not falsely poison B's live lock.` (597) | **Enroll.** Append after that sentence: `An offline Operation F restore-gate failure after that source's verified live capture closeout blocks only Operation G for that same source identity; it does not poison B's, C's, or another Operation F source's live lock.` |
| S20 | §4.5 trigger list (D4 reciprocal) | `Before the first live mutation in B, the first preservation write or ref creation in` (613) and `C, the first removal slice in D, or any future E mutation, approve the common recovery` (614) | **Enroll.** → `Before the first live mutation in B, the first preservation write or ref creation in C, the first removal slice in D, the first preservation write in an Operation F source capture, the first live mutation in an Operation G root operation, or any future E mutation, approve the common recovery playbook for that operation and pass its scratch drills.` |
| S21 | §4.5 gate matrix row | `\| B/C/D/E operation with no source change \| Manifest, restore, and receipt gates only; no invented browser gate \|` (661) | **Enroll.** `B/C/D/E operation` → `B/C/D/E/F/G operation` |
| S22 | §7.5 pre-removal recovery proof | `Use an established authenticated-encryption tool; do not invent crypto. Before a B` (1015) and `quarantine move or D removal, the owner must approve:` (1016) | **Enroll — criterion 9.** → `Before a B quarantine move, a D removal, or an Operation G retirement move, the owner must approve:` |
| S23 | §7.5 recovery proof before removal | `exact member/hash sets. Prove recovery with the stored secret before any removal and` (1028) and `again at retention exit.` (1029) | **Enroll — criterion 9.** → `Prove recovery with the stored secret before any removal and before any Operation G retirement move, and again at retention exit.` |
| S24 ★ | §7.6 `PRESERVATION_COMPLETE` | `encryption/upload/download/restore gate above passes. Anything less blocks D and E.` (1068) | **Enroll — criterion 7.** Insert after line 1068: `Operation F is outside this gate. No Operation F source, receipt, or failure contributes to or blocks PRESERVATION_COMPLETE, and no Operation C receipt covers an Operation F source, so PRESERVATION_COMPLETE keeps exactly the meaning it had before Section 14 existed and pre-amendment and post-amendment C receipts remain comparable.` |
| S25 | §8.3 closeout check | `- confirm no unexpected drive-root child was created;` (1240) | **Enroll — criterion 13.** → `- confirm that no unexpected drive-root child was created during the operation, by comparing the post-operation drive-root enumeration against the owner-approved baseline union the Section 14.3 known-unexpected register as frozen at this operation's start; a pre-existing registered child is not a failure and a newly created child is, whether or not it resembles a registered entry;` |
| S26 | §10 abort rules, maintenance | `failure occurred while a C/D freeze or E live-mutation window was active and` (1330) | **Enroll.** → `while a C/D freeze, an Operation F live freeze, or an E live-mutation window was active and…` |
| S27 | §10 abort rules, return point | `cannot waive its failed gate.` (1336) | **Enroll.** Insert after line 1336: `These rules apply unchanged to Operation F and Operation G (Section 14). An Operation F or Operation G failure returns only to that operation's own earliest affected source or root; it neither reopens nor waives a completed B, C, or D result, and no later F or G success waives a failed gate of any operation.` |
| S28 | §11 consistency requirement | `Git/ref relationships, guard installation, quarantines, and unexpected drive-root` (1378) and `children must remain consistent with their closeout manifest.` (1379) | **Enroll — criterion 13.** → `…and unexpected drive-root children must remain consistent with their closeout manifest. For an unexpected drive-root child that belongs to no operation's manifest, that requirement is met when its Section 14.3 register entry is unchanged at its recorded identity at closeout.` |
| S29 | §12 decision list | `- [ ] Decide whether and when to commission the separate E main-reconciliation plan.` (1412) | **Enroll.** Insert three unchecked items after line 1412 (text below the table) |

**S29's proposed text**:

```
- [ ] Decide whether to commission an Operation F additional-source preservation for
      any exactly identified unexpected drive-root child outside approved operation
      scope, and approve its Section 4.3 manifest, capacity requirement, freeze
      budget, and Operation-F-specific maximum freeze duration. No source is proposed
      or approved by this plan.
- [ ] Decide separately and later whether to commission an Operation G retirement for
      any such child whose ADDITIONAL_SOURCE_PRESERVED is already proved, and approve
      its Section 4.3 target manifest, retention start, and per-object retention
      period. No root is proposed or approved by this plan.
- [ ] Maintain the Section 14.3 known-unexpected register. Each entry is recorded,
      amended, or removed by owner decision only, and the register is frozen for the
      duration of each operation.
```

#### B.2 Sites judged inapplicable — with reasons

| Site | Exact base text (line) | Reason no edit is proposed |
|---|---|---|
| §5.2 drive-root audit bullet | `- add a read-only drive-root audit that compares configured drive roots with an` (735) / `  owner-approved baseline and reports unexpected new children without deleting them.` (736) | **Inapplicable by owner decision.** Gate 0 answer 3 states the register "does not clear the Section 5.2 audit or make it exit zero". Editing §5.2 is the exact change criterion 13 forbids. §14.3 states the non-effect explicitly instead |
| §6 post-operation observation | `both original paths and the configured drive-root allowlist so a future D:\tmp,` (874) | **Inapplicable.** This is a detection requirement, and the register suppresses no detection. §14.3 states that §6's observation is unaffected, so the non-enrolment is recorded rather than silent |
| §3.4 / §3.6 / §3.7 worktree row model | `1. It is a registered immediate child of the approved development parent and is not` (402) | **Inapplicable by construction, and the seal is stated.** A drive-root directory can never be a registered immediate child, so it can never be a row. Criterion 5's seal sentence is stated in §14.0 rather than by editing §3.6, so no §3 predicate changes |
| §8.1 / §8.2 Operation D contracts | `- ends with the full Section 8.3 closeout and explicit development resume.` (1099) | **Inapplicable.** These govern worktree candidate rows only, sealed off by §3.6 condition 1 |
| §9 Operation E prerequisites ★ | `The divergent-main repair is not a prerequisite for B, C, or D and is not included` (1261) | **Inapplicable.** The sentence asserts what E is *not* a prerequisite for. F and G do not depend on E either, and §1.2's amended graph (S3) already carries that. Adding F and G here would state the same fact in a second place and create a drift surface |
| §12 shared lock/register item ★ | `- [ ] Select the single shared B-E coordination lock/register root and verify its` (1397) | **Enrol not needed, and deliberately so.** The item selects **one** root for **all** live launchers; S17 and S18 widen the launcher set to `B-G`, so the same single root already serves F and G. Editing `B-E` here would imply a second root might be selected. **Recorded, not silently skipped.** |
| §13.1 / §13.2 review dispositions ★ | `- using one shared B-E coordination lock/register that remains blocked after any` (1432); `  independence of B, C, D, and E;` (1453); `- gives C and D measured, owner-approved maximum freeze budgets and explicit safe-` (1465) | **Inapplicable — historical record.** §13 records what the third and fourth review passes did. Enrolling F and G there would falsify a dated historical record of reviews that never saw them |
| Status header ★ | `is not declared. B, C, and D still require the operation-specific owner approvals` (10) | **Enrolled inside Hunk 5**, which already rewrites this paragraph and adds the F/G sentence. Listed here so the sweep is complete rather than appearing to have missed it |

#### B.3 Ordered application list — strictly descending anchor line

`docs/ai_workflow/INDEX.md` is a separate file: Hunk 6 applies independently of
everything below.

`docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`, in this exact order:

1. **N** — append §14 after line 1471
2. **S29** — after line 1412
3. **Hunk 4** — replace line 1389
4. **Hunk 3b** — after line 1384
5. **S28** — replace lines 1378–1379
6. **Hunk 3a** — after line 1372
7. **S27** — after line 1336
8. **S26** — replace line 1330
9. **S25** — replace line 1240
10. **S24** — after line 1068
11. **S23** — replace lines 1028–1029
12. **S22** — replace lines 1015–1016
13. **Hunk 2** — replace lines 990–992
14. **S21** — replace line 661
15. **S20** — replace lines 613–614
16. **S19** — after line 597
17. **S18** — replace line 560
18. **S17** — replace line 551
19. **S16** — after line 531
20. **S15** — replace line 515
21. **S14** — replace line 506
22. **S13** — after line 502
23. **S12** — replace lines 475–476
24. **S11** — after line 463
25. **S10** — replace line 453
26. **S9** — replace line 252
27. **S8** — replace line 194
28. **S7** — replace lines 177–178
29. **S6** — replace line 170
30. **S5** — replace line 108
31. **Hunk 1** — after line 95
32. **S4** — replace line 85
33. **S3** — after line 83
34. **S2** — replace line 65
35. **S1** — after line 63
36. **Hunk 5** — replace lines 8–10

### Artifacts

| Path | Change | Notes |
|---|---|---|
| `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` | modify (in-place, tracked) | Hunks 1–5, edit **N**, sweep edits S1–S29. Base = `origin/main` blob `1b41922e795e9202f128a9b1122d0ffb6c6134af` |
| `docs/ai_workflow/INDEX.md` | modify (in-place, tracked) | Hunk 6 only. Base = `origin/main` blob `027af297b1658f70f353dd298c545fa4108c6def` |
| `docs/worktree_cleanup_amendment/PLANNING.md` | modify | This council artifact — Plan v1, reviewer findings, response matrix, Plan v2 |
| `docs/worktree_cleanup/evidence/2026-09-28-state.md` | unchanged | Already holds every dated fact D6 keeps out of the design. No edit is proposed |
| `docs/worktree_cleanup/PLANNING.md` | **not touched** | Both divergent lineages. Not created, read-modify-written, overwritten, staged, or committed |
| `docs/test_inventory/**` | **not touched** | Neither regenerated nor hand-edited from this checkout |

No `.py`, `.js`, `.scss`, `.html`, test, or configuration file is touched.

**Effort**: **L** · **Owner**: `product-manager` drafts; the owner alone applies and
approves · **Depends on**: Gate 0 (signed 2026-09-28); Gate 1 (unsigned)

### Sequence

1. **Council review of this Plan v1** — `architecture-reviewer`, `test-strategist`, and
   `product-risk-reviewer`, independently and in parallel, against this same Plan v1 and
   the re-drafted hunks. No reviewer sees another's findings before completion.
2. **Response matrix** — every finding dispositioned, including any finding that a hunk
   does not apply cleanly, that a quantifier was missed, or that a sentence is readable
   out of context as approval.
3. **Plan v2** — the re-stated plan with accepted findings applied, in this same file.
4. **Stop for the owner's Gate 1 decision.** No hunk is applied to the technical design
   as approved text at any point before Gate 1.
5. *(After Gate 1 only, and not part of this packet's authority)* The owner prepares the
   branch. **Landing path per D5**: an in-place edit of the tracked
   `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` plus `docs/ai_workflow/INDEX.md`, on a
   branch taken from `origin/main`, prepared in the **owner-created standalone clone**
   that §1.3 already requires — never from this dirty checkout, and never as a new file.
   §1.3's four preconditions apply in full: the standalone clone (not a linked
   worktree), TEMP/TMP/`HT_RUNTIME_DIR`/`DB_FILE`/caches/bytecode redirected to scratch,
   `scripts/generate_test_inventory.py --check` run **there**, and proof that the
   checkout has no alternates or hardlinks to the live object store.
6. *(After Gate 1 only)* Renewed Gate 1 under §1.1 for this semantic change — which is
   precisely the item Hunk 4 keeps as an unchecked box.

### Expected gates

*Provisional; `test-strategist` confirms or corrects in step 2.*

- **pytest**: none required. Section 0's classification table routes the amended files
  to the **AI workflow / agent config** change-type row (`docs/ai_workflow/**`): manual
  dry-run and self-review, `code-reviewer` or careful self-review, and *"run tests only
  if source behavior changed"*. No source behavior changes. This rests on the flagged
  assumption that no hunk implies a tooling, launcher, or script change; **if the council
  concludes any hunk does, this premise fails and the gates must be re-derived.**
- **e2e**: none. No template, route, or static asset changes.
- **`Test Inventory Drift`**: **not tripped.** Both edits are in-place edits of files
  already tracked in the globbed `docs/ai_workflow/` directory. No file is added to or
  deleted from `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, or
  `docs/ai_workflow/`. `--check` is still run, in the standalone clone per §1.3, never
  from this checkout, and the inventory is never hand-edited.
- **pyright baseline diff**: **inapplicable** — no `.py` change.
- **Change-type row**: AI workflow / agent config. The design's own §4.5 gate matrix
  pairs the two files in one row: *"This plan plus INDEX"* → *"AI-workflow manual review;
  generate_test_inventory.py --check and regenerate only on proved drift"*.
- **This council artifact itself**: **Product docs only** (`docs/**` excluding AI
  workflow files) — no required tests or reviewers.
- **Gates this packet does not satisfy and does not claim**: Gate 1 (unsigned), the
  independent Windows-filesystem review, and every operation-specific owner approval.

### Evidence gaps and honest limits

These are stated rather than papered over. Each is a live input for the council.

1. **Operation A deployment state is unmeasured.** Hunk 4 and Hunk 5 record obligations,
   not measurements, precisely because nothing here measured whether any of the 93
   targets is deployed.
2. **The successor guard now on `origin/main` is unverified in this checkout.** Whether
   it preserves the reviewed Operation A behavior was not assessed. Hunk 4 records the
   reconciliation as an obligation and makes no claim about the outcome.
3. **No member class of any candidate source has been characterized.** §14.1's
   requirement 6 makes characterization a precondition of approvability, and this packet
   deliberately does not perform it. **No route recommendation here depends on its
   outcome.**
4. **§7.1's runtime map does not exist.** Whether a live process writes either observed
   directory is therefore **not established**; §14.1 requirement 4 makes the map or a
   recorded absence-of-writer mandatory rather than assuming it.
5. **The §14 placement is a genuine open choice.** Appending after §13 avoids renumbering
   §10–§13 but places operative content after a historical appendix. The `## 9A.`
   alternative is recorded in B.0 so the council can overturn the choice rather than
   discover it.
6. **The status header's link on base line 7 points at
   `../worktree_cleanup/PLANNING.md`** — the path with two divergent, unreconciled
   lineages, where a relative link resolves to the local copy that does *not* carry the
   owner's 2026-09-05 Gate 1 sign-off. **Hunk 5 deliberately leaves that link
   unchanged.** Repairing it would require deciding which lineage the design cites,
   which is a separate, explicitly out-of-scope owner decision. It is flagged here as a
   finding rather than silently fixed.
7. **The register's real entries are not drafted here.** §14.3 defines the register's
   shape, effect, non-effect, and integrity. It contains no entry, because an entry would
   require publishing an exact path and identity, which criterion 20 forbids in this
   artifact. The owner creates entries in the durable record, not here.
8. **Only the sweep families listed in B were searched.** The quantifier grep covered
   `B-E`, `B–E`, `B, C, or D`, `B, C, and D`, `B/C/D`, `A-D`, `C/D`, `D and E`,
   `Operation [A-E]`, `the relevant operation`, `each operation`, and `every operation`.
   A quantifier phrased in none of those shapes could still exist; the council should
   treat the sweep as thorough, not as proven exhaustive.
9. **No git command was run for this Plan v1.** The base was supplied as two extracted,
   hash-verified blobs. Every anchor is derived from those blobs. No working-tree copy
   was treated as the base.

### What Plan v1 explicitly does not do

- It applies no hunk, checks no Gate 1 or Plan v2 box, and alters no section of this
  artifact other than Plan v1.
- It names, proposes, approves, or counts no source, no target, no removal, and no
  filesystem mutation.
- It selects no option for the early targeted rescue decision and does not count it.
- It proposes no successor drive-root baseline (Gate 0 answer 4), and it proposes no
  change to the owner-approved 2026-09-06 baseline's bytes, approver, approval
  timestamp, or `RESOLVED` meanings.

---

## Agent provenance

**Council provenance: COMPLETE.** All three reviewers ran and returned. None failed and
none was skipped.

| Role | Agent ID | Notes |
|---|---|---|
| `product-manager` — Plan v1 | `a419e27d5f34b2435` | Author of Section 0 and Plan v1. |
| `product-manager` — response matrix + Plan v2 | `a419e27d5f34b2435` | Author of the matrix and Plan v2. |
| `architecture-reviewer` | `af4111665721a7030` | Step 2 reviewer. 23 findings; verdict *Needs revision*. |
| `test-strategist` | `a8f27c6488bba79eb` | Step 2 reviewer. 14 findings; verdict *Targeted gate sufficient*, but *not ready for Gate 1*. |
| `product-risk-reviewer` | `aec936ee4d0f52fdb` | Step 2 reviewer. 22 findings; verdict *Needs revision*. |

**Same product-manager resumed for the matrix + Plan v2?** `yes` — resumed via
`SendMessage` to the agent ID the manager recorded when the Step-1 `Agent(...)` call
returned. Every ID above was supplied by the manager; none was invented by the
`product-manager`, and no completed council work was rerun to manufacture continuity.

**Evidence gap** — the following could not be established and is recorded rather than
resolved:

> Two gaps the manager closed with read-only `git` work are **no longer open**, and are
> recorded here as closed so a later reader does not reopen them: TS-14 (which
> `QUALITY_GATE.md` copy the `test-strategist` read) — the `origin/main` blob
> `d3cd6f5ffa6845dc68a588412d96103440679ae2` was extracted and diffed against the
> modified working-tree copy, and the plan-stage routing table, the change-type table,
> the `Test Inventory Drift` rows and the two-step `Type Check` row are **byte-identical**
> between them, so every routing conclusion in Plan v1 and in the reviewer's report holds
> on the `origin/main` base; and TS-10's tracked-status question, answered below.
>
> What remains open: (1) **Operation A deployment state is unmeasured** — nothing in this
> packet measured whether any deployment target is or is not deployed. (2) **The successor
> guard now on `origin/main` is unverified here** — whether it preserves the reviewed
> Operation A behavior was not assessed, and no claim about it is made or relied upon.
> (3) **No member class of either observed drive-root child is characterized, and §7.1's
> runtime map does not exist**, so whether a live process writes either directory is not
> established; Plan v2 makes both a precondition of approvability instead of assuming
> them. (4) **The §14.3 register contains no entry**, because an entry requires an exact
> path and physical identity that acceptance criterion 20 forbids publishing here; the
> owner creates entries in the durable record. (5) **The enumeration sweep is thorough but
> not proven exhaustive** until TS-9's closure re-grep runs against the *amended* file at
> apply time — Plan v2 turns that admission into a required apply-time check, which has
> not yet been run because no hunk has been applied. (6) **`docs/worktree_cleanup/evidence/2026-09-28-state.md`
> is not tracked on `origin/main`** — `git ls-tree origin/main -- docs/worktree_cleanup/`
> returns exactly two blobs, and neither is that file nor the source packet. Acceptance
> criteria 14, 16 and 17 move every dated fact out of the tracked design and into a file
> that does not exist for a reader of `origin/main`. Plan v2 states this plainly and puts
> the remedy to the owner at Gate 1; it is not resolved here.

**Gate 0 advisers are not the council** — the table below records read-only Gate 0
*consultation* only. Those advisers approved nothing, are not
`architecture-reviewer`, `test-strategist`, or `product-risk-reviewer`, and their
unanimity is not a Gate 1 finding.

**Gate 0 consultation, 2026-09-28.** Three independent advisers were run in parallel on
blocking questions 1 and 2, read-only, with no shared findings before completion. They
were deliberately *not* the three council reviewer types, so council independence is
preserved. Their separate recommendations, evidence, and defect lists were used to revise
this Section 0; their conclusions are advisory and carry no approval authority.

| Adviser | Angle | Q1 | Q2 |
|---|---|---|---|
| A | Preservation mechanics and capture integrity | separate operation (high confidence) | separate operation (very high) |
| B | Approval semantics and adversarial misreading | separate operation (medium-high) | separate operation (high) |
| C | Program sequencing and cost of a new operation | separate operation (medium-high) | separate operation (high) |

---

## Reviewer findings

> Historical reviewer text is reproduced with machine-local scratch and absolute
> checkout paths redacted. The original is retained privately; these path redactions
> do not change a finding, disposition, approval or signature. References to verbatim
> reviewer findings in the historical record are subject to these disclosed redactions.

All three reviewers ran independently and in parallel against the same Plan v1, with no
reviewer shown another's findings before completion. Each report below is reproduced
**verbatim**, including severities, locations, the "categories with no findings" blocks,
and the verdicts. Findings are cited elsewhere in this artifact as **AR-n**, **TS-n**,
and **PR-n**.

### architecture-reviewer (agent `af4111665721a7030`)

I read the owner-signed Section 0, Plan v1 (lines 633–1449), and both extracted `origin/main` base blobs. Paths cited:

- Plan v1: `[repository]\docs\worktree_cleanup_amendment\PLANNING.md`
- Base design: `[private scratch base]` (cited below as `BASE`)
- Base index: `...\scratchpad\base\INDEX.origin-main.md` (cited as `BASE-INDEX`)

**Category result — anchor resolution.** I independently re-derived every anchor in Plan v1 against `BASE` and `BASE-INDEX`. All 36 plan-file anchors and the one `INDEX.md` anchor resolve, and every quoted anchor line is byte-exact (spot-verified at BASE:8–10, 63, 65, 83, 85, 95, 108, 170, 177–178, 194, 252, 453, 463, 475–476, 502, 506, 515, 531, 551, 560, 597, 613–614, 661, 923, 990–992, 1015–1016, 1028–1029, 1068, 1240, 1261, 1330, 1336, 1372, 1378–1379, 1384, 1389, 1397, 1412, 1471; BASE-INDEX:61–65). **No finding in the "anchor does not resolve" category.** The strictly-descending order in B.3 (PLANNING.md:1295–1332) is also correct as a sequence — every entry descends monotonically from 1471 to 8. The order is sound; what defeats it in three places is finding 3 below, which is a span-definition defect, not an ordering defect.

---

1. **Operation F's cardinality contract is self-contradictory: one source or a closed set** — **blocking** — Plan v1 §14.1 opening (PLANNING.md:1094–1095) and requirements 1, 3, 5 (PLANNING.md:1101–1104, 1119–1122, 1127–1130) versus sweep edits S12 (PLANNING.md:1241) and S16 (PLANNING.md:1245). §14.1 opens *"Operation F preserves one exactly identified source"*, and S12 makes §4.1's launcher cardinality *"F one approved source"* while S16 binds an F approval to *"exactly one source identity"*. But requirement 1 obliges the proposal to *"enumerate an exact, closed set of sources"*, requirement 3 governs proof *"across disjoint sources"*, and requirement 5 computes capacity and freeze *"for the complete set, not per source in isolation"*. Both readings are load-bearing: the single-source reading is what makes `ADDITIONAL_SOURCE_PRESERVED(source)` closable under criterion 11, and the closed-set reading is what criterion 6's re-approved freeze budget assumes. As drafted, a multi-source F is approvable under §14.1 but has no launcher that can run it (S12), no approval record that can bind it (S16), and no aggregate outcome that can close it — the exact "unclosable operation" hazard criterion 11 exists to prevent. Fix: pick one — either make F strictly one source per operation and rewrite requirements 1, 3 and 5 to speak of one source with cross-source *rejection* checks against previously approved F sources, or keep the closed set and rewrite S12, S16 and the §14.1 opening to bind an F operation to one approved set, adding the per-source outcome plus an explicit statement that no set-level aggregate exists.

2. **Hunk 5's declared replacement span (8–10) is narrower than its replacement text (8–12), which duplicates two lines of the status header** — **blocking** — Plan v1 Hunk 5 (PLANNING.md:947, 956–957, 959–969) and B.3 item 36 (PLANNING.md:1332). Hunk 5 says *"Replace base lines 8–10"* and B.3 repeats *"replace lines 8–10"*, while the parenthetical at PLANNING.md:956–957 claims *"lines 6–7 and 11–12 unchanged except for the F/G sentence appended before the closing sentence"* — an internal contradiction, since 11–12 cannot be both unchanged and appended to. The proposed text at PLANNING.md:965–969 restates the whole of BASE:11–12 (*"B, C, and D still require the operation-specific owner approvals below and the independent Windows-filesystem review. E remains a separately planned and approved operation… This factual status correction changes no technical contract.\*"*). Applied literally as a 8–10 replacement, the design's status header ends with two copies of the B/C/D sentence, two copies of the E sentence, and two closing `*` terminators — a malformed emphasis span in the first paragraph of a signed design. Fix: state the span as base lines 8–12 in both Hunk 5 and B.3 item 36, and delete the false "lines 11–12 unchanged" parenthetical.

3. **Three sweep edits are specified as line replacements but supplied as sentence fragments; literal application silently deletes base safety text** — **blocking** — S12 (PLANNING.md:1241), S26 (PLANNING.md:1255), S28 (PLANNING.md:1257), applied per B.3 items 23, 8 and 5 (PLANNING.md:1319, 1304, 1301). (a) S12 replaces BASE:475–476 but its text begins *"B handles exactly one root…"* and ends *"…one live maintenance window."*, omitting BASE:475's opening `approved immutable manifest and verifies its recorded digest.` and BASE:476's closing `One D launcher`; the result truncates the manifest-digest sentence and leaves BASE:477 beginning `invocation owns exactly one slice:` with no subject. (b) S26 replaces BASE:1330 with text beginning *"while a C/D freeze…"*, dropping `failure occurred`, so BASE:1329's `If the` runs straight into `while`. (c) S28 replaces BASE:1378–1379 with text beginning *"…and unexpected drive-root children must remain consistent…"*, which deletes `Git/ref relationships, guard installation, quarantines,` from §11's post-operation consistency requirement — i.e. an amendment about drive-root children silently removes guard installation and quarantines from a completion check. Fix: restate S12, S26 and S28 as full-line replacements whose text reproduces every non-target token of the replaced lines verbatim, or re-specify them as quoted-fragment substitutions with the exact search string, and mark in B.3 which entries are line replacements and which are in-line substitutions.

4. **The amendment's central term is defined twice, in two non-identical forms, while §14.0 asserts it is defined once** — **blocking** — Hunk 1's boundary paragraph (PLANNING.md:776–778) versus §14.0 (PLANNING.md:1052–1058). Hunk 1 lands in §1.2: *"An unexpected drive-root child is outside approved operation scope when it is neither of Operation B's two named roots nor inside an approved operation source manifest."* §14.0 states the same definition with a different and stronger test: *"…when its exact canonical/final path and physical identity are neither of Operation B's two named roots nor enumerated in an approved operation source manifest. That is the only discriminator, it is stated once here."* The §1.2 copy drops the physical-identity binding, so a reader in §1.2 can discriminate on path string alone — the aliasing failure §2.2 rule 8 (BASE:205–210) exists to block — and §14.0's "stated once" claim is false the moment Hunk 1 lands. Criterion 12 (PLANNING.md:268–274) requires the term be defined **once**. Fix: reduce Hunk 1's sentence to a pointer (*"Section 14.0 defines when such a child is outside approved operation scope"*) and keep the operative definition only in §14.0, or delete §14.0's "stated once here" and make the two texts byte-identical.

5. **§14.0's discriminator sentence contradicts the definition it immediately follows** — **significant** — PLANNING.md:1055–1058. The definition's second conjunct is *"nor enumerated in an approved operation source manifest"* — an approval-status test. The next sentence asserts *"it is a statement about path identity, not about approval status"*, and four lines later §14.0 concedes the opposite: *"only the scope qualifier above stops applying"* (PLANNING.md:1063). D3 (PLANNING.md:480) resolves this correctly at the level of noun-versus-qualifier, but §14.0's drafted text collapses the distinction into a false claim. A reviewer quoting PLANNING.md:1056–1058 alone is quoting something untrue of the design. Fix: rewrite as *"The noun is fixed by path identity against the owner-approved baseline; only the scope qualifier depends on manifest approval, and it is the qualifier — never the noun — that stops applying when a manifest is approved."*

6. **§14.1's opening sentence scopes Operation F to any source outside Operation C, far wider than drive-root children** — **significant** — PLANNING.md:1094–1097, against the §14 heading (PLANNING.md:1048) and S29's §12 items (PLANNING.md:1263–1271). §14.1 opens: *"Operation F preserves one exactly identified source that Operation C's approved scope does not cover."* Read as an isolated sentence — the test criterion 2 imposes (PLANNING.md:191–197) — that defines an approvable route for any path anywhere outside `D:\development`, including user-profile roots, other volumes, and off-repository application data. The section heading, S29's decision items, and the packet's entire remit are limited to unexpected drive-root children outside Operations B and C. Fix: open §14.1 with *"Operation F preserves one exactly identified unexpected drive-root child that is outside approved operation scope under Section 14.0"*, and state that Operation F is not a general route for arbitrary sources outside Operation C's scope.

7. **Five of the sections the plan claims cross-reference §14 contain no reference to it, defeating the stated mitigation for appending §14 after the §13 appendix** — **significant** — B.0's placement rationale (PLANNING.md:1033–1036) claims *"every reader path into the new material is explicitly cross-referenced from §1.2, §2.2, §4.1–§4.5, §7.5, §7.6, §8.3, §10, §11, and §12."* Checking each proposed edit's text: §2.2 (S6–S9, PLANNING.md:1235–1238), §4.1 (S10–S12, PLANNING.md:1239–1241), §4.4 (S17–S19, PLANNING.md:1246–1248), §4.5 (S20–S21, PLANNING.md:1249–1250), §7.5 (S22–S23, PLANNING.md:1251–1252) and §7.6 (S24, PLANNING.md:1253) contain no `Section 14` pointer at all — S17 and S18 only widen `B-E` to `B-G`. This is also a direct miss against resolution D4 (PLANNING.md:481), which requires reciprocal references from §4.2, §4.3, §4.4 **and** §4.5 back to the carrier; only §4.2 (S13) and §4.3 (S14) carry one. Because §14 sits after a historical appendix, a reader at §4.4 who encounters `B-G` has no in-file route to where F and G are defined. Fix: add `(Section 14)` to S17 or S18, to S20, to S22 or S23, and to S11, and either correct or delete the B.0 claim.

8. **§12's shared-lock selection item is left at `B-E` on a reason that does not hold, textually excluding F and G from the one artifact the owner called mandatory** — **significant** — B.2's row for BASE:1397 (PLANNING.md:1286), against S17/S18 (PLANNING.md:1246–1247). After the amendment, §4.4 reads *"All B-G live launchers use one fixed owner-approved coordination-file path"* while §12 still reads *"Select the single shared B-E coordination lock/register root."* The stated reason for not editing it — *"Editing `B-E` here would imply a second root might be selected"* — is not true of the proposed substitution: *"the single shared **B-G** coordination lock/register root"* retains the word "single" and implies exactly one root. As left, the owner's selection checklist scopes the lock to B–E, which is precisely the condition S17 itself calls unacceptable (*"a new operation outside §4.4's shared lock and attempt register is not acceptable"*). Fix: add a sweep edit replacing `B-E` with `B-G` at BASE:1397 and move that row from B.2 to B.1.

9. **Operations F and G have named §11 outcomes but no state machine, and those outcomes cite state names defined only for B, C and D** — **significant** — Hunk 3a (PLANNING.md:862–864, 873–875) and §14.2 (PLANNING.md:1153–1182). `ADDITIONAL_SOURCE_PRESERVED` is defined in terms of *"VERIFIED_CLEAN_CLOSEOUT in the shared register"* and *"no F-caused BLOCKED_RECOVERY remaining"*; `DRIVE_ROOT_CHILD_RETIRED` requires *"a VERIFIED Operation G attempt"*. `VERIFIED` is defined only by Operation B's forward-state list (BASE:846–849) and Operation D's (BASE:1121–1133); §14.1's failure-isolation paragraph says *"Section 7.2's abort branches govern Operation C only"* (PLANNING.md:1138–1139) and refers to *"Operation F's own safe-abort boundary"*, which no hunk defines. Every other operation in this design ships a state machine with explicit terminal branches before it can be claimed complete; F and G ship outcomes that quantify over states they never define. Fix: state in §14.2 that Operation G adopts Section 6's exact forward states and terminal branches unchanged, and give §14.1 either Operation C's §7.2 abort branches applied to F, or an explicit F abort-branch list, before `ADDITIONAL_SOURCE_PRESERVED` can be referenced.

10. **`ADDITIONAL_SOURCE_PRESERVED` is written with three different parameterizations, and the source↔root identity equivalence is never stated** — **significant** — PLANNING.md:860 (`ADDITIONAL_SOURCE_PRESERVED(source)` in §11), PLANNING.md:873 (bare, unparameterized, inside `DRIVE_ROOT_CHILD_RETIRED`), PLANNING.md:1156 (`ADDITIONAL_SOURCE_PRESERVED(root)` in §14.2 requirement 1), PLANNING.md:1245 (bare again, in S16's G approval bindings). §8.1 (BASE:1100–1101) permits only *"Section 11's exact named outcome"* to be claimed, so a differently-parameterized name is, strictly read, not the §11 outcome. Nothing in §14 states that an Operation G root's identity is the same identity as the Operation F source that preserved it — the precondition chain in §14.2 requirement 1 depends entirely on that equivalence. Fix: use `ADDITIONAL_SOURCE_PRESERVED(source)` in all four places and add one sentence to §14.2 binding G's target root identity to be equal to the F source identity for which that outcome was derived.

11. **S1 and S2 place F and G behind the B/C/D scheduling step of a sequence they simultaneously make binding, contradicting Hunk 1's independence claim** — **significant** — S1 (PLANNING.md:1230), S2 (PLANNING.md:1231) and Hunk 1 (PLANNING.md:769–771). S1 appends `-> consider F and G only under their separate plans and approvals (Section 14)` after BASE:63, i.e. after *"separately approve and schedule B, C, and D"* and after the E step; S2 widens BASE:65 to *"No technical independence below permits **B-G** to bypass that sequence."* Together these make F and G sequentially downstream of B/C/D scheduling. Hunk 1 then asserts *"F does not depend on B, C, D, or E"* and S3 hangs F off A in the dependency graph. The design already distinguishes rollout order from technical dependency, but BASE:65 as widened makes the rollout order binding on F, so the independence bullet is inoperative as drafted. Fix: state in Hunk 1 or S1 the exact rollout position intended — e.g. that F and G may be commissioned at any point after the stabilization checkpoint and fresh evidence, independent of whether B, C or D have been approved or scheduled — rather than leaving two conflicting statements four lines apart.

12. **§14.1 requirement 6 permits approving a source after characterizing only one of its member classes** — **significant** — PLANNING.md:1131–1133: *"Each source contains at least one member class that has been characterized - SQLite family, nested repository, reparse point, alternate data stream, long path - before approval."* As written this is satisfied by characterizing a single class and ignoring the rest, which is weaker than criterion 6 (PLANNING.md:220–227) and than the out-of-scope entry at PLANNING.md:437–440, both of which treat characterization of the member classes as a precondition of any preservation proposal. It also reads as a statement about what a source *contains* rather than an obligation on the proposer. Fix: *"Every member class present in the source — SQLite family, nested repository, reparse point, alternate data stream, long path — has been enumerated and characterized before approval. An uncharacterized member class makes the source unapprovable."*

13. **F's restated obligations omit §7.3 and §7.4 entirely, although F's own requirement 6 contemplates nested repositories** — **significant** — §14.1 requirement 2 (PLANNING.md:1105–1118) restates obligations drawn from §7.2, §7.5 and §7.6, but nothing from §7.3 (Git roots and OID preservation, BASE:935–964) or §7.4 (derived Git preservation, including *"Preserve and restore-test every nested Git repository separately"*, BASE:982). Requirement 6 (PLANNING.md:1131–1132) explicitly lists *"nested repository"* as a member class an F source may contain. So F can be approved over a source containing a live Git repository with no obligation to enumerate its OIDs, create archive refs for admin-only commits, or restore-test it — and §14.2 then grants G retirement authority on the strength of that F. Fix: add to requirement 2 (or as a new requirement) that any Git repository inside an F source carries §7.3's OID enumeration/archive-ref obligations and §7.4's separate preservation and restore-test, or state explicitly that a source containing a Git repository is not approvable under F.

14. **The known-unexpected register gates a closeout but is registered nowhere: no digest, no §4.3 approval binding, no evidence-root home** — **significant** — §14.3 (PLANNING.md:1184–1220), S25 (PLANNING.md:1254), S16 (PLANNING.md:1245). S25 makes every Operation D closeout compare the drive-root enumeration against *"the owner-approved baseline union the Section 14.3 known-unexpected register as frozen at this operation's start"*, and §14.3 says the register *"is frozen for the duration of an operation"* — but nothing gives that frozen snapshot an identity. Every other owner-approved artifact this design gates on is digest-bound and recorded in a §4.3 approval record (BASE:504–531) with an evidence root under §3.1 (BASE:260–263). S16 adds approval-field bindings for F and G only; no edit adds a register-version binding to §4.3's common fields (BASE:515) that B, C and D approvals bind — yet it is B/C/D-class closeouts that consume it. Without a bound snapshot hash, "frozen at this operation's start" is unverifiable at closeout and an after-the-fact addition is undetectable, which is the exact attack §14.3's integrity paragraph says it prevents. Fix: add a sweep edit binding *"the SHA-256 digest of the Section 14.3 register as frozen at operation start"* into §4.3's common approval fields, and require the closeout receipt to record it.

15. **The enumeration sweep misses §1.2's own heading, which counts the operations it is amending** — **significant** — `BASE:50` — `### 1.2 Five independently completable operations` — appears in neither the B.1 sweep table (PLANNING.md:1228–1258) nor the B.2 inapplicable table (PLANNING.md:1279–1288). S1 and S3 both land inside §1.2 and add two operations to its rollout order and dependency graph, making the section heading false on the same screen as the edits. The same gap applies to two further universal quantifiers the plan's own declared grep families should have surfaced (evidence gap 8, PLANNING.md:1430–1434): `BASE:1374` *"After each operation/slice, perform a normal guarded development observation"* and `BASE:552` *"outside every operation evidence root"*, neither reported as enrolled or as inapplicable. Fix: add `BASE:50` to B.1 (heading → *"Independently completable operations"*, or *"Seven"*), and add `BASE:1374` and `BASE:552` to B.2 with the reason that their universal quantifier already covers F and G.

16. **Hunks 4 and 5 introduce a CI run outcome into the stable design, which acceptance criterion 14 forbids and criterion 17 appears to require — the conflict is not flagged** — **significant** — Hunk 4 (PLANNING.md:929–930, *"dispose of the cancelled post-merge required check"*) and Hunk 5 (PLANNING.md:963, *"the disposition of the cancelled post-merge required check"*), against criterion 14 (PLANNING.md:307–310, which forbids *"no merge date, PR number, commit SHA, **CI run outcome**, audit timestamp…"* entering the design or `INDEX.md`) and criterion 17 (PLANNING.md:340–342, 347–348, which lists that disposition among the obligations the design must state while keeping *"the cancelled check's run identity"* in dated evidence). That a specific post-merge required check was **cancelled** is a CI run outcome and a live-state fact, dateless or not; §1.1 (BASE:36–39) restricts the file to *"stable predicates and procedures only"*. Plan v1 resolves in favour of criterion 17 silently. Fix: either phrase the obligation without asserting an outcome — *"complete the post-merge required-check disposition for the merged source"* — or record the criterion 14/17 conflict explicitly in the response matrix for the owner to settle at Gate 1.

17. **The design's only council-artifact pointer still names a path that will not contain this amendment's Gate record** — **significant** — `BASE:99–106` (§1.3: *"the product-manager must create docs/worktree_cleanup/PLANNING.md… It must contain… Section 0 requirements and Gate 0 sign-off, Plan v1… and owner Gate 1 sign-off"*) and `BASE:7` (the header's link to `../worktree_cleanup/PLANNING.md`), neither of which any hunk edits. This amendment's Gate 0 record and, later, its Gate 1 record live at `docs/worktree_cleanup_amendment/PLANNING.md`, which the amended design never names. Plan v1 flags the related hazard at evidence gap 6 (PLANNING.md:1419–1425) — that the header link resolves to the lineage lacking the Gate 1 sign-off — and deliberately leaves it. The consequence for §14 specifically: a future reader asked to verify that §14 was Gate-1 reviewed under §1.1 is sent by §1.3 to a file that does not contain that review. Fix: add one dateless sentence to §1.3 or §14.0 stating that each later semantic amendment records its own Gate 0/Gate 1 in its own council artifact and naming this one's path; if the owner prefers to defer, record the omission as a deliberate, owner-visible gap rather than only as an evidence note.

18. **§7.5's `Preserve … recovery/salvage directories` bullet — the strongest "discovery obliges capture" surface — is left unedited** — **significant** — `BASE:998–999`, against Hunk 2 (PLANNING.md:817–840) and Section 0's problem statement 2 (PLANNING.md:89–97), which identifies precisely that bullet plus the inventory paragraph as the surface for *"the opposite misreading, that discovery already obliges capture."* Hunk 2 replaces only BASE:990–992 and correctly adds *"This inventory is a discovery obligation, not a source grant."* But five lines below the new text, the imperative bullet still reads *"Preserve ignored/untracked/local settings, handovers/claims, evidence, loose files, recovery/salvage directories, and unique local payload."* Read as an isolated sentence — criterion 2's test — an unexpected drive-root child classified as a recovery/salvage directory is still under an unqualified instruction to preserve it, in the same section, under Operation C. Criterion 8 (PLANNING.md:235–239) asks for the discovery rule to be *"in §7.5 itself"*; it is, but it does not reach the bullet. Fix: qualify the bullet to *"Preserve, within C's approved source manifest, ignored/untracked/local settings…"*, or add a trailing clause to it pointing at the new discovery paragraph.

19. **Plan v1's own edit counts are wrong in three places, so its verification claim does not cover every edit** — **minor** — PLANNING.md:724 (*"thirty-one here"*), PLANNING.md:733–734 (*"all thirty-one plan-file anchors and the one INDEX.md anchor resolve cleanly"*), and PLANNING.md:1015–1017 (*"Twenty-nine quantifier sites were found… eight sites beyond the mandated list… marked ★"*). The plan-file edit list in B.3 (PLANNING.md:1297–1332) contains **36** entries (Hunks 1, 2, 3a, 3b, 4, 5 + edit N + S1–S29), not thirty-one. The sweep reports 29 rows in B.1 plus 8 further sites in B.2 — 37 sites, not twenty-nine — and the ★ marks number 10 (S5, S12, S15, S16, S19, S24 in B.1; the §9, §12, §13, status-header rows in B.2), not eight. Since PLANNING.md:733–734 is the audit statement that every anchor was re-derived, an undercount of five leaves the claim unproven for an unidentified subset. Fix: restate all three counts against B.3's actual list and re-assert the verification claim over 36 + 1.

20. **S5 silently departs from the plan's own stated enrolment policy** — **minor** — the naming rationale at PLANNING.md:679–681 states that *"every `B-E` range quantifier widens to `B-G` and stays a range, rather than growing an ad-hoc list that the next reader can silently under-read"*, but S5 (PLANNING.md:1234) turns BASE:108's `Sections B-E retain` into `Sections B-E and the Section 14 operations retain` — an ad-hoc list, unrecorded as an exception. S7 (PLANNING.md:1236) also departs from the range policy but records its reason in full; S5 does not. Fix: either widen S5 to `Sections B-G retain` or record the reason for the list form as S7 does.

21. **Operation G is the only operation that changes the drive-root enumeration, and it has no drive-root closeout check and no register-reconciliation rule** — **minor** — §14.2 (PLANNING.md:1177–1182) requires *"the complete Section 4.4 clean-closeout protocol and final root receipt"*; §4.4's protocol (BASE:574–581) contains no drive-root check, and S25's amended check lives in §8.3, which is Operation D's slice closeout only (BASE:1224). After a successful G, the register (PLANNING.md:1214–1220) still names a child at a path where it no longer exists, and entries are removable *"only by owner decision"* with no obligation or trigger to remove them; nothing says what a later closeout does with a registered entry that G legitimately retired. Fix: require an Operation G closeout to run the same baseline-union-register comparison S25 adds to §8.3, and add one sentence to §14.3 stating that a registered entry retired by a completed Operation G is dispositioned by the owner at that operation's closeout.

22. **S25 introduces a "post-operation drive-root enumeration" that no section defines** — **minor** — PLANNING.md:1254. The new §8.3 bullet turns a yes/no confirmation into a set comparison over *"the post-operation drive-root enumeration"*, but does not bind that enumeration to §5.2's term of art (*"configured drive roots"*, BASE:735–736) nor to §2.2 rule 9's mandatory no-follow explicit-stack enumeration (BASE:211–212). Two executors could compute different sets and both pass. Fix: write *"by comparing a no-follow enumeration of the configured drive roots (Section 5.2) against the owner-approved baseline union the Section 14.3 register as frozen at this operation's start"*.

23. **`INDEX.md`'s new "separately approved routes" phrase is approval-shaped when read alone** — **minor** — Hunk 6 replacement text, PLANNING.md:998–999, with the plan's own pre-emption at PLANNING.md:1006–1007. In isolation, *"the separately approved routes for drive-root children outside Operations B and C"* reads as routes that have been approved. It is defensible because `BASE-INDEX:63` already uses *"separately approved main reconciliation"* for the unapproved Operation E, so the phrasing is consistent with the file's existing convention — I raise it only so the response matrix records the choice rather than inheriting it. Fix, if the owner wants the isolation test applied strictly: *"separately gated routes"*.

---

**Categories with no findings.** Anchor resolution: none — all 37 anchors resolve and every quoted anchor line is byte-exact. Application ordering: none — B.3 is strictly descending and correct as a sequence (finding 3 is a span-definition defect, not an ordering one). Preservation of `MALFORMED_ROOT_QUARANTINED`, `MALFORMED_ROOTS_QUARANTINED`, `PRESERVATION_COMPLETE`, `WORKTREE_SLICE_COMPLETE`, `WORKTREE_SLICE_PARTIAL_CLOSED`, `TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED`, `WORKTREE_CLEANUP_COMPLETE`, `PREVENTION_COMPLETE`: none — no hunk edits BASE:1342–1372, S24 seals `PRESERVATION_COMPLETE` at §7.6, §14.0 states B's and D's seals affirmatively, and both new outcomes carry explicit non-contribution clauses. §1.1 stable-policy collision: only finding 16 (no dates, counts, SHAs, paths, or identities appear anywhere in the proposed design text; I confirmed RESIDUE-1 and RESIDUE-2 are never named, pathed, counted or hashed in Plan v1 or in any proposed hunk). §1.3 landing-gate collision: only finding 17 — the D5 landing mechanics (in-place edit of two tracked files in a globbed surface, standalone clone, `--check` run there) are correct and consistent with §1.3's four preconditions.

**Verdict: Needs revision** — four blocking defects (1–4), all mechanical or contract-level and all fixable in Plan v2 without reopening any owner decision.

---

### test-strategist (agent `a8f27c6488bba79eb`)

I have verified Plan v1's gate claims against the generator, the pytest contracts, and the hash-verified base blobs. Findings below.

---

## Required gates (my derivation, confirming/correcting Plan v1's "Expected gates")

- **pytest:** `tests/test_agent_workflow_contracts.py` (targeted, run in the standalone clone — see finding 5). Plan v1 says "none required"; that is defensible under the change-type row but leaves the only automated oracle that reads these two files' bytes unrun.
- **e2e:** none. No template, route, static asset, or spec changes. No feature-map hit.
- **other:** manual dry-run / self-review per the **AI workflow / agent config** row; `code-reviewer` or careful self-review; `scripts/generate_test_inventory.py --check` in the standalone clone per §1.3. No `/verify-suite`, no `/build-css`.
- **Conftest / fixture work:** none. No blueprint, no table, no route. `tests/conftest.py` is untouched and unaffected.

---

## Findings

**1. Section 0 asserts a council that had not run, while five sections of the same artifact say it has not — blocking.**
Location: artifact lines 616–620, *"Council status"* — *"the plan-stage council … is **authorized and has been run**. Its outcome, including each reviewer's real agent ID and verbatim findings, is recorded under *Reviewer findings* below."* Contradicted by line 1454 (*"Council provenance: NOT STARTED — blocked on Gate 0. No `product-manager` ID, no reviewer IDs."*), lines 1473–1474, 1480, 1486, 1492, and the unchecked box at line 1494. The claim was false when written — I am the first council reviewer to run — and it is exactly the class of record the repository forbids: a review that did not run must never be recorded as having produced an outcome. Separately, Plan v1 demonstrably exists, so the `product-manager` agent ID is owed and missing. Fix: change 616–620 to "authorized; the council is in progress and no findings are recorded yet", record the real `product-manager` ID at line 1454, and leave *Reviewer findings* as NOT STARTED until each reviewer actually returns.

**2. Hunk 5's declared anchor span is narrower than its own replacement text; applied literally it duplicates the status header and leaves an unbalanced italic delimiter — blocking.**
Location: Plan v1 Hunk 5, artifact lines 947–954 (*"Replace base lines 8–10 up to the sentence boundary"*, quoting base 8/9/10) and the ordered application list, artifact line 1332 (*"**Hunk 5** — replace lines 8–10"*). The proposed replacement (artifact lines 959–970) ends `…E remains a separately planned and approved operation, as do the Section 14 operations F and G, neither of which is approved here. This factual status correction changes no technical contract.*` — which reproduces base lines 11–12 (`below and the independent Windows-filesystem review. E remains a separately planned` / `and approved operation. This factual status correction changes no technical contract.*`) with the F/G clause inserted. The parenthetical at artifact lines 956–957 concedes this, self-contradictorily: *"lines 6–7 and 11–12 unchanged **except for the F/G sentence appended**"*. An executor following B.3 replaces only 8–10, base 11–12 survive, and the header ends with the closing sentence twice and two `*` terminators. Fix: state the span as **replace base lines 8–12** in both Hunk 5 and B.3 item 36, and delete the "11–12 unchanged" parenthetical.

**3. Plan v1 carries four mutually inconsistent counts of its own edits, and its anchor-verification claim covers 31 of the 36 edits an executor will apply — blocking.**
Locations: artifact line 646 (*"twenty-four enumeration-sweep edits"*), line 724 (*"thirty-one here"*), line 733 (*"**Anchor resolution result: all thirty-one plan-file anchors** and the one `INDEX.md` anchor resolve cleanly against the base"*), lines 1015–1017 (*"Twenty-nine quantifier sites were found … eight sites beyond the mandated list … marked ★"*). Measured from the artifact: B.1 lists **29** sweep edits (S1–S29, every row "Enroll"); B.3 lists **36** plan-file edits (edit N + S1–S29 + Hunks 1, 2, 3a, 3b, 5 + Hunk 4); ★ markers number **10** (S5, S12, S15, S16, S19, S24 in B.1; four rows in B.2), not eight. The verification consequence is the sharp one: the plan's only anchor-resolution statement asserts thirty-one anchors resolve, while thirty-six edits will be applied, so five edits' anchors are unverified *on the plan's own wording*, and there is no post-apply completeness check that would reveal a dropped or double-applied edit. Fix: recount; make B.3 the single authoritative list; state its length once; have the anchor-resolution sentence quote that same number.

**4. §14.0 asserts the discriminator "is stated once here" while Hunk 1 states it a second time, in different words — significant.**
Locations: Hunk 1 proposed text, artifact lines 776–777 — *"An unexpected drive-root child is outside approved operation scope when it is neither of Operation B's two named roots nor **inside** an approved operation source manifest."* — versus edit N §14.0, artifact lines 1052–1058 — *"…when its **exact canonical/final path and physical identity** are neither of Operation B's two named roots nor **enumerated in** an approved operation source manifest. **That is the only discriminator, it is stated once here**…"*. Two definitions of the same term in one signed design, differing on whether the test is loose membership ("inside") or identity-bound enumeration, and the second asserts the first does not exist. Acceptance criterion 12 (artifact lines 268–274) requires the term be defined **once**, and drafting resolution D3's entire rationale is that a second formulation drifts. This one *is* checkable by reading the amended design, and as drafted it fails. Fix: make Hunk 1 cite rather than restate — e.g. *"An unexpected drive-root child outside approved operation scope (Section 14.0) is retained and recorded only."* — keeping Hunk 1's boundary sentences (no authority from proximity, generated-output classification, creation time, or a prior campaign's receipt), which are what criteria 1 and 3 want at that location.

**5. "pytest: none required" omits the one pytest file that reads the exact bytes being edited — significant.**
Location: Plan v1 *Expected gates*, artifact lines 1377–1382. `tests/test_agent_workflow_contracts.py` builds `SURFACE` from `(REPO / "docs" / "ai_workflow").glob("*.md")` (test line 84) and asserts **content**, not only presence, on both amended files:
- `test_surface_does_not_direct_readers_to_the_retired_plan_file[docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md]` — reds if any added line contains `SHARED_PLAN` (test lines 139–156).
- `test_surface_does_not_direct_readers_to_the_retired_plan_file[docs/ai_workflow/INDEX.md]` — INDEX is the one file permitted exactly **one** such mention (`ANTI_RECREATION_NOTE`, test line 91); Hunk 6 rewrites INDEX lines 61–65 and a stray second mention reds it.
- `test_surface_does_not_use_the_retired_tier_numbering[docs/ai_workflow/INDEX.md]` — reds on `\bTier \d` or `\bAppendix A\d` (test lines 93, 159–174). Note `WORKTREE_CLEANUP_PLAN.md` is *exempt* from this second one by the `*_PLAN.md` filter at test line 161; `INDEX.md` is not.

I read every proposed block — Hunks 1–6, edit N, S1–S29, S29's text — and none introduces `SHARED_PLAN`, `Tier <digit>`, or `Appendix A<digit>`, so these cases are green as drafted. That is the result of reading, not of a gate. Fix: add to *Expected gates* — "pytest, targeted, in the standalone clone: `.venv/Scripts/python.exe -m pytest tests/test_agent_workflow_contracts.py -q`" — and record the three forbidden strings as an apply-time constraint on any re-drafted text.

**6. The dirty checkout changes the answer in a way criterion 19 does not cover: pytest here is red, not merely drifted — significant.**
Locations: acceptance criterion 19 (artifact lines 353–358) and *Expected gates* line 1387. The untracked `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` in this working tree enters `SURFACE`, which (a) adds one collected node to `tests/test_agent_workflow_contracts.py` — one, not two, because the `*_PLAN.md` filter excludes it from the second parametrization — so `--check` reds locally while CI is green, the exact hazard QUALITY_GATE.md's `Test Inventory Drift` row names; and (b) **fails `tests/test_agent_workflow_contracts.py::test_every_surface_file_is_tracked_by_git` outright** (test lines 207–239), which is a red test, not drift, and whose assertion message names the file. Criterion 19 forbids regenerating and hand-editing the inventory but is silent on the red. Fix: add to *Expected gates* — "A pytest run from *this* checkout is expected red on `test_every_surface_file_is_tracked_by_git` until the checkout catches up to `origin/main`, where the file is tracked. That red belongs to the checkout, not the amendment; it is not repaired by regenerating the inventory and it is not a gate result." On a branch cut from `origin/main` the file is tracked and the test passes.

**7. The `Test Inventory Drift` claim is correct — and correct for a mechanism Plan v1 never states — minor.**
Locations: Section 0 lines 152–154 and 165; *Expected gates* lines 1384–1388. Verified against `scripts/generate_test_inventory.py`: the generator has **no** configuration-surface collector at all. Its four collectors are `collect_playwright` (line 114), `collect_pytest` (195), `collect_vitest` (426), `collect_hard_waits` (449), and `build_inventory` (491–556) commits exactly those four surfaces. The `docs/ai_workflow/` sensitivity is entirely indirect: it arrives through `tests/test_agent_workflow_contracts.py`'s parametrized `SURFACE`, whose node count is a committed `pytest.files[]` row. Adding or deleting a file there moves that count; an **in-place edit moves nothing**. Plan v1's claim holds, and the council artifact's own landing path (`docs/worktree_cleanup_amendment/`) is outside every globbed directory, so creating it moves nothing either. Fix: state the mechanism — a parametrized pytest file, not a generator scan — because that is precisely what tells an executor the *count* is safe while the *content* is asserted (finding 5).

**8. The pyright claim is right; the required context it names is half a check — minor.**
Locations: Section 0 line 165, *Expected gates* line 1389. With the Artifacts table's statement that no `.py`, `.js`, `.scss`, `.html`, test, or configuration file is touched (line 1345), and QUALITY_GATE.md's rule that the pyright baseline diff is repo-wide and runs when the diff touches any `.py`, "inapplicable" is correct. But the branch-protection context is `Type Check (tsc blocking + pyright measure-only)` and it carries **two** blocking steps — `tsc --noEmit` and `scripts/pyright_baseline_diff.py`. Plan v1 names only the second. The conclusion is unchanged (no `.ts` either), but naming half a two-step required context is the misreading that row exists to correct. Fix: "`Type Check (tsc blocking + pyright measure-only)`: both steps inapplicable — no `.py` and no `.ts` in the diff."

**9. Criterion 10 is the acceptance criterion that cannot be demonstrated by reading the amended design, and no proposed check closes it — significant.**
Locations: criterion 10 (artifact lines 252–262); B.1, B.2, and Evidence gap 8 (lines 1430–1434). The *mandated-eleven* half is checkable and I confirmed every site is addressed: §1.2 rollout order (S1), dependency graph (S3), "before B, C, or D uses" (S4), §2.2 rule 3 (S7, partial with a recorded reason), rule 6 (S8), rule 20 retention clock (S9), §4.1 launcher staging (S10, S11), §4.3 opener (S14), §4.4 "All B-E live launchers" (S17) and "every B-E live attempt" (S18), §4.5 trigger list (S20) and gate-matrix row (S21), §7.5 pre-removal recovery proof (S22, S23), §10 abort and recovery (S26, S27), §12 decision list (S29). The *universal* half — "everywhere the design quantifies over operations" — is not demonstrable by reading the result: a surviving unamended quantifier is invisible in the amended text and visible only in a complete re-scan, and Plan v1 concedes the sweep is "thorough, not proven exhaustive". Fix: convert it into a closure condition run against the **amended** file at apply time — re-grep for `B-E`, `B–E`, `B-D`, `A-D`, `B, C, or D`, `B, C, and D`, `B/C/D`, `B/C/D/E`, `C/D`, `D and E`, and assert every surviving hit is on the recorded-inapplicable list (§13.1, §13.2, §12's single-shared-lock item, §9's E-prerequisite sentence). That turns Evidence gap 8 from an admission into a repeatable check, and it is the single highest-value verification this plan is missing.

**10. Criterion 16, and criterion 14's final sentence, impose content requirements on a file Plan v1 leaves unedited and never verifies — significant.**
Locations: criterion 14 (artifact lines 307–322: *"…recorded, with its window, as an unresolved matter in the dated evidence only, with the August campaign **positively refuted** as its cause and the cause otherwise stated as unknown"*), criterion 16 (lines 323–333: *"their relationship to the absent August artifacts is recorded as **undetermined**"*), and the Artifacts row at line 1341 marking `docs/worktree_cleanup/evidence/2026-09-28-state.md` *"unchanged … No edit is proposed."* Both criteria are satisfied only by that file's contents; neither is demonstrable by reading the amended design, and Plan v1 quotes nothing from it. Compounding this, Evidence gap 9 (lines 1435–1437) records that **no git command was run** for Plan v1 and only the two design blobs were extracted and hash-verified — so the tracked status of the file designated as the sole home for every date, count and path the amendment *removes* was never established, while the two files being edited were. I confirmed read-only that the file exists at that path and contains the "positively refuted" / "undetermined" family of strings; I am not quoting it, to stay inside the publication prohibition. Fix: quote the two sentences carrying the required framing into the response matrix, and state the file's tracked status on `origin/main`. If it is not tracked there, say so plainly — criterion 14 moves the merge date out of a tracked design and into that file, and a reader of `origin/main` must be able to follow the pointer.

**11. Nothing escalates the change type, but assumption nine's trigger is worded so it cannot be evaluated — significant.**
Locations: assumption nine (artifact lines 465–468) and *Expected gates* lines 1380–1382. I checked every proposed block for a tooling, launcher, or script implication. The two closest do not escalate: **S11** (artifact line 1240) inserts a §4.1 item stating *"Operation G uses its own thin root-quarantine launcher built from the same reviewed template as item 2…"*, echoed by §14.2's closing paragraph (lines 1177–1182) — a launcher that does not exist, that this packet does not write, and that the same text forbids building anew (*"requires no new mutation primitive"*, *"no new removal surface is built for either"*); and **S7/S26**, which widen Git-maintenance-suspension and abort-window prose to an "Operation F live freeze". The change-type table keys on **changed paths**, and the Artifacts table lists exactly two `.md` files under `docs/ai_workflow/` plus this artifact — no `scripts/**`, no `.claude/**`, no `.github/workflows/**` — so the Tooling/scripts row is never reached and no `/verify-suite` escalation follows. The defect is the wording: *"if the council concludes any hunk **implies** a tooling, launcher, or script change"* is ambiguous between "this diff changes tooling" (false) and "the amended design obliges someone to build tooling later" (true, for Operation G's launcher). Fix: restate the trigger as "if any hunk changes a file outside `docs/ai_workflow/**`", which is the condition the table actually keys on, and record separately that Operation G's launcher is future work behind its own approval with its own change-type derivation at that time.

**12. Executor and reviewer failure modes that no proposed check would catch — significant.**
- **A skipped or double-applied edit.** B.3's ordering is genuinely strictly descending (verified: 1471, 1412, 1389, 1384, 1378, 1372, 1336, 1330, 1240, 1068, 1028, 1015, 990, 661, 613, 597, 560, 551, 531, 515, 506, 502, 475, 463, 453, 252, 194, 177, 170, 108, 95, 85, 83, 65, 63, 8), so the discipline is sound — but nothing verifies afterwards that all thirty-six landed. Add a per-edit post-condition: the anchor text no longer appears (for replacements) and the replacement text appears **exactly once**; plus an expected final line count. Combined with finding 3, this is where a real error lands silently.
- **Editing the working-tree copy instead of a clone of `origin/main`.** D5 and Sequence step 5 forbid it in prose only. A single `git hash-object docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` == `1b41922e795e9202f128a9b1122d0ffb6c6134af` assertion *before the first edit*, and the same for INDEX against `027af297b1658f70f353dd298c545fa4108c6def`, makes it mechanical and costs nothing. Plan v1 already has both digests; it just never turns them into a precondition.
- **Running `--check` in a standalone clone with no `node_modules` or no venv.** `_npx()` raises `SystemExit("npx not found on PATH. Run `npm ci` first…")` (generator lines 104–111) and `collect_pytest` shells `sys.executable -m pytest`. A hard exit is neither "no drift" nor "proved drift", and §4.5's matrix row says *"regenerate only on proved drift"*. Fix: state that the clone needs `npm ci` and a venv before `--check` means anything, and that any `SystemExit` from a collector is a tooling failure to resolve, never a green.
- **Reading `Test Inventory Drift` green as "nothing regressed".** It pins counts only. The content assertions in finding 5 are the only thing in the repository that reads these two files' prose.

**13. Criterion 2 has no defined check, and criterion 19 is evidenced only by a transcript — minor.**
Criterion 2 (artifact lines 191–197) is a universal over every sentence of roughly 250 proposed lines, with no enumeration of the permissive clauses and no reviewer-facing checklist; its satisfaction is currently self-assessed by the drafter. The sharpest concrete risk is Hunk 6's INDEX phrasing (artifact lines 996–999) — *"and the separately approved routes for drive-root children outside Operations B and C"* — which reads at least as naturally as "routes that **have been** separately approved" as it does "routes requiring separate approval", on the one surface a reader reaches with no surrounding context. Criterion 19 (lines 353–358) is a process criterion about commands not run; no text in the amended design can evidence it. Fix: add a one-line out-of-context reading of each hunk to the response matrix; re-word the INDEX phrase to "routes that require their own separate approval"; and state explicitly that criterion 19 is evidenced by the session transcript, not by the artifact.

**14. Which QUALITY_GATE copy I read — minor, disclosure.**
I read the working-tree copy at `[repository]\docs\ai_workflow\QUALITY_GATE.md`, which `git status` reports as modified relative to `HEAD`. No `origin/main` extraction of that file was supplied and I ran no git command, so I could not diff the two. Every routing conclusion above — the AI workflow / agent config row, *"run tests only if source behavior changed"*, the "What trips `Test Inventory Drift`" table, the two-step Type Check row, and the plan-stage routing table — is derived from that copy. One reassurance I can offer: the three strings `tests/test_consult_adapter.py` pins in it (test lines 1075–1077 — `## Plan-stage routing`, `Gate 0 (requirements approval) + Gate 1 (council-reviewed plan approval)`, `Run the union, never the weaker set.`) are all present in the copy I read, so the local modification has not weakened the pinned parts. Fix: re-derive the classification from the `origin/main` blob before Gate 1, since the amendment lands on a branch cut from `origin/main`.

---

## Categories with nothing to report

- **E2E:** no finding. No template, route, static asset, `scss/**`, or `e2e/**` path is in scope; the frontend feature map produces no hit; no visual re-baseline is implicated.
- **Conftest / fixture impact:** no finding. No blueprint, table, or route is added, so neither the `app` fixture nor `erase_data()` in `tests/conftest.py` needs updating.
- **Known-red awareness:** the documented `e2e/program-backup.spec.ts:79` exception is not on any surface this plan touches. The only red relevant here is the checkout-local one in finding 6, which is not a documented known exception and should not be recorded as one.

---

## Verdict

**Targeted gate sufficient** — the change-type routing in Plan v1 is correct (AI workflow / agent config: manual dry-run and self-review; no `/verify-suite`, no e2e, no `/build-css`; `Test Inventory Drift` untripped; pyright and tsc inapplicable), with three additions: run `tests/test_agent_workflow_contracts.py` (finding 5), name the checkout-local red (finding 6), and name both steps of the Type Check context (finding 8).

**But Plan v1 is not ready for Gate 1 as drafted.** Findings 1, 2 and 3 are blocking and independent of the gate question: the artifact records a council that had not run, one of its thirty-six operative edits will corrupt the file if applied as written, and its own edit counts disagree four ways so no completeness check exists at apply time. Findings 4, 9 and 10 name the criteria whose satisfaction cannot currently be demonstrated — criterion 12 fails by reading, criterion 10's universal half is not demonstrable at all, and criteria 14 and 16 depend on a file the plan neither edits nor verifies.

---

### product-risk-reviewer (agent `aec936ee4d0f52fdb`)

## Scope note

I read Plan v1 (lines 633–1449 of `[repository]\docs\worktree_cleanup_amendment\PLANNING.md`), the owner-signed Section 0 above it, and verified every anchor and citation against the two hash-verified base blobs at `[private scratch base]`. No file was written, no git command run, no database opened, and neither residue directory's path, identity, hash, or count appears below.

**Calculation-surface declaration — verified TRUE.** Section 0 line 371 declares `none`. The Artifacts table (Plan v1 lines 1336–1345) touches only `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`, `docs/ai_workflow/INDEX.md`, and this council artifact. I read all six hunks, edit **N**, and all 29 sweep edits: none references `utils/effective_sets.py`, `CountingMode`, `ContributionMode`, `utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py`, `utils/volume_*.py`, `utils/_fatigue/**`, `utils/fatigue.py`, or `utils/fatigue_data.py`. The only application-adjacent identifier anywhere in the proposed text is the pre-existing `create_startup_backup` prohibition in base §2.2 rule 14, which no hunk touches. The declaration holds.

---

## Findings

**1. Hunk 5's replacement span contradicts its own replacement text — applying it as written duplicates two lines of the status header**
Severity: **blocking**
Location: Plan v1 lines 945–976 (Hunk 5) and line 1332 (ordered application list item 36); base `WORKTREE_CLEANUP_PLAN.origin-main.md` lines 8–12.
Hunk 5's anchor says *"Replace base lines 8–10 up to the sentence boundary"* and the prose at line 956 says *"lines 6–7 and 11–12 unchanged except for the F/G sentence appended before the closing sentence"*. But the proposed replacement block (lines 960–969) itself contains the full content of base lines 11–12 — *"below and the independent Windows-filesystem review. E remains a separately planned and approved operation… This factual status correction changes no technical contract.\*"* — including the paragraph's closing italic marker. Applying the block over lines 8–10 only, as item 36 of the ordered list directs, leaves base lines 11–12 in place and produces a header that states the Windows-filesystem review twice, states E's separate-approval status twice, and carries two closing `*` markers. The paragraph that carries this design's entire approval state would land malformed and self-contradictory.
Fix: change Hunk 5's anchor and ordered-list item 36 to *replace base lines 8–12*, and restate the prose at line 956 as "lines 6–7 unchanged".

**2. S24's sentence "Operation F is outside this gate" is ambiguous between PRESERVATION_COMPLETE and §7.6's restore gate, and the careless reading strips Operation F of its restore-proof obligation**
Severity: **blocking**
Location: Plan v1 line 1253 (S24); base line 1068, inside `### 7.6 Gate C and isolated restore`.
S24 inserts *"Operation F is outside this gate"* immediately after base line 1068. The enclosing section is titled **Gate C and isolated restore**, and base line 597 already names this gate *"Gate C"* in exactly this sense (*"blocks D and E through Gate C"*). A future executor who lands on §7.6 reads "this gate" as Gate C — i.e. as excusing Operation F from the isolated restore, whole-tree source-to-restoration equality, and the sanitizer/no-execution requirements of §7.6 — which is the opposite of the intent and the single most damaging misreading available in the whole packet. It also directly contradicts §14.1 requirement 2 (Plan v1 line 1117), which requires *"Section 7.6's whole-tree source-to-restoration equality proved in a fresh isolated root"* for each F source. Criterion 7 requires this to be unambiguous.
Fix: replace the opening clause with *"Operation F is outside PRESERVATION_COMPLETE. Operation F still performs every Section 7.6 restore verification for its own sources, under Operation F's own gate;"* and keep the remainder of S24 as drafted.

**3. §14.1 requirement 2 is presented as restating §7.5's obligations but silently drops three of them, including preservation of manifest-enumerated startup snapshots**
Severity: **blocking**
Location: Plan v1 lines 1105–1118 (§14.1 requirement 2); base §7.5 bullets at lines 994–1004.
Requirement 2 is framed as carrying §7.5's obligations *"as obligations rather than by item number"* — which is what acceptance criterion 6 asks for — and a future Operation F proposer will treat it as the complete list. Comparing it against §7.5's actual bullets, three obligations are missing:
- base line 997, *"Preserve every manifest-enumerated startup snapshot before any app/test launch"* — this is the app's `auto_backup` / startup-backup output, exactly the artifact class whose disappearance the packet's own evidence record is unable to explain. It appears nowhere in §14.1;
- base line 999's *"handovers/claims"* and *"recovery/salvage directories"* are dropped from the ignored/untracked/local-payload list — and a recovery/salvage directory is the most likely content class for the sources Operation F exists to capture;
- base line 1002's *"Record reconstruction versions and health output without installing or repairing anything."*
Criterion 6 says the obligations of §7.5 apply "to each source". As drafted they do not.
Fix: add the startup-snapshot bullet, `handovers/claims`, `recovery/salvage directories`, and the no-install/no-repair clause to §14.1 requirement 2; or replace the restatement with an explicit "every obligation in Section 7.5 applies to each Operation F source" plus only the scope-specific deviations.

**4. §14.1 states no owner-approval precondition and no "no authority exists" clause, while §14.2 states both — read alone, §14.1 is the packet's weakest surface**
Severity: **significant**
Location: Plan v1 lines 1099–1143 (§14.1) versus lines 1153–1176 (§14.2).
§14.2 opens *"No Operation G retirement authority exists for a root until every one of the following is true"* and its item 4 requires *"Section 4.3 manifest and production-package digest integrity and the owner's approval… recorded in a durable approval record"*. §14.1's six conditions are framed only as *"An Operation F proposal is assessable only when all of the following hold"* — a test for assessing a proposal, not for having authority — and the list contains **no owner-approval item and no §4.3 manifest item at all**. The only anchor is §14.0's blanket sentence two subsections earlier. Acceptance criterion 2 requires every permissive clause to be anchored to a dated owner approval record distinct from the amendment; §14.1, read alone as an executor will read it, has no such anchor.
Fix: open §14.1 with *"No Operation F preservation authority exists for a source until every one of the following is true"*, and add an item requiring a §4.3 immutable digest-bound manifest and a dated owner approval record created separately from, and after, this plan text.

**5. §14.1 requirement 6 requires only "at least one member class" to be characterized, which an uncharacterized source trivially satisfies**
Severity: **significant**
Location: Plan v1 lines 1131–1133.
The text reads *"Each source contains at least one member class that has been characterized - SQLite family, nested repository, reparse point, alternate data stream, long path - before approval. An uncharacterized source is not approvable."* The two sentences do not agree: characterizing one class out of five satisfies the first sentence while leaving the source substantially uncharacterized, and the second sentence then has no operative force. Section 0's out-of-scope entry (lines 437–440) describes the intended obligation as characterizing *"the member classes"* — plural, the whole enumeration. This matters beyond correctness: an Operation F source is approved for authenticated-encryption capture and **private off-machine upload**. A source whose member classes are unenumerated may carry a live SQLite family, credential material, or a nested repository off this machine under a gate that was satisfied by characterizing its long-path behavior alone.
Fix: reword to *"Every member class present in the source — SQLite family, nested repository, reparse point, alternate data stream, long path — has been enumerated and characterized before approval, and the absence of each unlisted class is positively recorded."*

**6. S1 inserts Operations F and G into a block the design attributes to "the Gate 0 requirements", making a 2026-09-05 approval record appear to impose the new work**
Severity: **significant**
Location: Plan v1 line 1230 (S1); base line 54 (*"The Gate 0 requirements impose this program order:"*) and line 63.
S1 appends *"-> consider F and G only under their separate plans and approvals (Section 14)"* as a new final line of the indented block at base lines 56–63. That block is introduced by base line 54 as the order **the Gate 0 requirements impose**. After the edit, the design states that the signed 2026-09-05 Gate 0 requirements impose a program order that contemplates F and G — which they do not; Section 0 itself establishes at lines 167–175 that that Gate 0's twelve acceptance criteria contain *"nothing about a new retirement operation class"*. This is precisely the reverse inference acceptance criterion 3 exists to close: an existing approval record made to look like it authorizes the new work.
Fix: place the F/G line outside the attributed block, as a following sentence — e.g. *"Operations F and G, added by a later amendment under Section 1.1, are considered only under their own separate plans and approvals (Section 14); the Gate 0 requirements above do not order or authorize them."*

**7. §14.0 cites five sections as already using the term "unexpected drive-root child"; three of them do not, and one uses a term with an incompatible discriminator**
Severity: **significant**
Location: Plan v1 lines 1052–1053; base line 691–692 (§5.1), lines 735–736 (§5.2), lines 874–876 (§6).
§14.0 states: *"An unexpected drive-root child - the term Sections 5.1, 5.2, 6, 8.3 and 11 already use, discriminated against the owner-approved drive-root baseline - …"*. Checked against the base: §8.3 (line 1240) and §11 (line 1378) use that exact term; **§5.1 does not** — it says *"creating an unintended drive-root child"*; **§5.2 does not** — it says *"reports unexpected new children"*; **§6 does not** — it says *"or other unexpected root"*. Worse, §5.1's term is discriminated by **cause of creation** (MSYS path conversion resolving a slash-rooted path from the current drive), not against a baseline, and §6's is discriminated against *"the configured drive-root allowlist"*, not the baseline. §14.0 then asserts its discriminator *"is not… about who created the directory"* — which is flatly incompatible with the §5.1 sense it has just claimed as the same term. Resolution D3's whole premise is that no second noun is minted; but the amendment leaves "unintended", "unexpected new children" and "other unexpected root" un-unified, so the five-member family becomes a six-member family with three discriminators. A citation that does not say what the citing text claims is a finding on its own.
Fix: narrow the citation to §8.3 and §11 (the two sections that use the exact term), state separately and accurately that §5.1's *"unintended"* is a causal description and §6's is allowlist-discriminated, and either normalize those two to the canonical noun in the sweep or record explicitly that they are left alone and why.

**8. §14.0's discriminator is defined by approval status while the same sentence claims it is a statement about path identity — and Hunk 1's protection clauses lapse at manifest approval**
Severity: **significant**
Location: Plan v1 lines 1052–1058 (§14.0) and lines 776–781 (Hunk 1); acceptance criterion 12 at Section 0 lines 268–274.
§14.0 defines *outside approved operation scope* as *"neither of Operation B's two named roots nor enumerated in an approved operation source manifest"* and then asserts *"it is a statement about path identity, not about approval status"*. The membership test is literally against an approval record; the sentence is false as written. The consequence is operative, not cosmetic: Hunk 1's protective sentences — *"Such a child is retained and recorded only"* and *"Proximity to a named root… creates no preservation, relocation, quarantine, or removal authority for it"* — are scoped to a child that is *outside approved operation scope*. §14.0 (line 1063) confirms *"only the scope qualifier above stops applying"*. So at the moment an Operation F source manifest is approved for a child, Hunk 1's no-removal-authority sentence stops applying to it. Criterion 12 required the term to be defined *"by path identity rather than by approval status so the protection cannot lapse at the moment the directory enters an approved manifest"*. D3 moved the lapse from the noun to the qualifier rather than eliminating it.
Fix: delete the false clause; state instead that the discriminator is evaluated by exact canonical/final path and physical identity rather than by name, prefix, or proximity; and re-anchor Hunk 1's no-removal-authority sentence to *"any unexpected drive-root child"* rather than to the scope-qualified subset, so the protection does not lapse on manifest approval.

**9. Hunk 2 leaves §7.5's "Preserve … recovery/salvage directories … and unique local payload" bullet unedited, directly contradicting the new paragraph six lines above it**
Severity: **significant**
Location: Plan v1 lines 817–840 (Hunk 2, replacing base lines 990–992); base line 998–999, unedited by any hunk.
Hunk 2 tightens the inventory's *"explicit owner paths"* hook and adds *"discovery never adds it to an immutable source manifest, and discovery alone obliges no capture."* But the replacement text retains *"recovery/backup directories"* as a standing inventory category, and base line 998 — untouched — still reads *"Preserve ignored/untracked/local settings, handovers/claims, evidence, loose files, recovery/salvage directories, and unique local payload."* A careless or motivated executor now has, inside a single section: a category that sweeps a drive-root recovery directory into the inventory, and an imperative bullet that says preserve it. Section 0's Problem item 2 (lines 93–97) identifies this exact bullet as *"the strongest surface for the opposite misreading, that discovery already obliges capture"* — and Plan v1 does not edit it. Acceptance criterion 3 requires the reverse inference to be closed.
Fix: qualify base line 998 in the same hunk — *"…recovery/salvage directories within C's approved source scope…"* — or append to that bullet *"Each item preserved under this bullet must already be enumerated in C's approved immutable source manifest; this bullet adds nothing to that manifest."*

**10. Hunk 4 dissolves the standing, never-satisfied plan-level Gate 1 checkbox into a conditional future one**
Severity: **significant**
Location: Plan v1 lines 922–932 (Hunk 4); base line 1389.
Base line 1389 is `- [ ] Approve the Gate 1 council-reviewed version of this plan.` — an outstanding, unsatisfied obligation for **this plan as it currently stands**. Base line 6 confirms only *"Gate 0 and Operation A Plan v2 Gate 1 are signed"*. Hunk 4 replaces that line with a checked Operation A item plus an unchecked item reading *"Approve the renewed plan-level Gate 1 that Section 1.1 requires for the council-reviewed version of this plan **after each later semantic amendment**"*. After the edit, §12 contains no box for the plan-level Gate 1 that is owed today independently of any amendment; a reader concludes the only outstanding plan-level Gate 1 is one triggered by future amendments. Criterion 17 asked for the renewed-Gate-1 box to be *retained*; it did not ask for the original obligation to be reframed out of existence.
Fix: keep two unchecked boxes — `- [ ] Approve the Gate 1 council-reviewed version of this plan.` verbatim, plus the renewed-Gate-1 item as drafted.

**11. §12's shared-lock decision item is left at "B-E" while §4.4 is widened to "B-G", on a reason that does not follow**
Severity: **significant**
Location: Plan v1 line 1286 (B.2 table row); base line 1397; contrast S17/S18 at Plan v1 lines 1246–1247.
S17 and S18 widen §4.4 to *"All B-G live launchers"* and *"every B-G live attempt"* — correctly, and Plan v1 marks both **mandatory**. But B.2 declines to enroll §12's decision item *"Select the single shared B-E coordination lock/register root"*, arguing that *"Editing `B-E` here would imply a second root might be selected."* That does not follow: `B-G` is as singular as `B-E`; the item's cardinality is carried by the word *"single"*, not by the range. What the un-edited text actually leaves behind is an owner decision whose stated scope covers B through E only, while §4.4 requires F and G to use that same lock — the exact textual gap criterion 10 exists to close (*"A class outside those quantifiers is textually outside the shared lock"*).
Fix: enroll it — *"Select the single shared B-G coordination lock/register root…"*.

**12. The §1.2 heading "Five independently completable operations" is left stale, and the sweep does not record it**
Severity: **significant**
Location: base line 50 (`### 1.2 Five independently completable operations`); Plan v1's sweep table (lines 1230–1258) covers §1.2 lines 63, 65, 83 and 85 only, and B.2 (lines 1279–1288) does not list it.
After the amendment the design defines seven operation classes and §1.2's own body enumerates F and G (S1, S3). The section heading continues to say five. This is neither enrolled nor recorded as inapplicable, so the sweep's own completeness claim ("Twenty-nine quantifier sites were found… all addressed") is inaccurate — *"Five"* is a quantifier over operations, and the grep families listed at Plan v1 lines 1430–1433 could not have caught it. A heading that undercounts the operation set is precisely the surface a later reader uses to conclude F and G are not real operations of this design.
Fix: enroll it — retitle to *"Independently completable operations"* (count-free, and also removes a count from a stable-policy surface) — and add the site to the sweep table.

**13. "the cancelled post-merge required check" puts a CI run outcome into the technical design, which acceptance criterion 14 bans literally**
Severity: **significant**
Location: Plan v1 lines 929–930 (Hunk 4) and line 963 (Hunk 5); acceptance criterion 14 at Section 0 lines 307–314; owner's signature at lines 566–568.
Criterion 14 enumerates what may not enter the design or `INDEX.md`: *"no merge date, PR number, commit SHA, **CI run outcome**, audit timestamp, observation date, disappearance window, count, file count, path, or remote advertisement"*, and says only *"the cancelled check's run identity"* stays in dated evidence. Both Hunk 4 and Hunk 5 introduce the phrase *"the cancelled post-merge required check"* — a CI run outcome, stated as fact, in the design. Criterion 17 does use the same phrase when listing what remains open, so 14 and 17 are in genuine tension, and the owner's signature accepted both. Plan v1 resolves the tension silently in favour of 17 and its Hunk 5 commentary (lines 972–976) asserts *"No merge date, PR number, CI run identity, or count is introduced"* — true of *identity*, not of *outcome*. The council must disposition this explicitly rather than let it pass as compliant.
Fix: either state the obligation without the outcome — *"dispose of the outstanding post-merge required-check status recorded in the dated evidence"* — or record an explicit, owner-visible disposition that criterion 17's phrasing overrides criterion 14 for this one phrase. Do not leave Hunk 5's commentary claiming full criterion-14 compliance.

**14. The artifact asserts the council "has been run" and that its findings are recorded below, while Agent provenance and Reviewer findings both say NOT STARTED and no product-manager ID exists**
Severity: **significant**
Location: Plan v1's containing artifact, lines 616–620 (Section 0 "Council status") versus lines 1454–1455 (Agent provenance) and lines 1471–1474 (Reviewer findings).
Section 0 states *"the plan-stage council… is **authorized and has been run**. Its outcome, including each reviewer's real agent ID and verbatim findings, is recorded under *Reviewer findings* below."* Those sections say *"**NOT STARTED — blocked on Gate 0.** No council reviewer has been run"* and *"Council provenance: NOT STARTED — blocked on Gate 0. No `product-manager` ID, no reviewer IDs."* — despite Plan v1 itself having been authored by a `product-manager`. Root `CLAUDE.md` §3 is explicit: *"A review that did not run, or whose reviewer failed, is **incomplete** — never record it as 'no findings' or 'refuted', and never let it move an approval status."* Asserting a completed council in the signed Section 0 while the outcome sections are empty is the same failure mode in the opposite direction, and Section 0's own sign-off checklist (line 1496) requires complete provenance.
Fix: change the Section 0 sentence to state the council is authorized and **in progress**, record the `product-manager` agent ID in Agent provenance now, and leave Reviewer findings as NOT STARTED until each reviewer actually returns.

**15. Whether Operations F and G require PREVENTION_COMPLETE is never stated, and the S3 graph and Hunk 1 text point in different directions**
Severity: **significant**
Location: Plan v1 lines 769–774 (Hunk 1 independence bullets) and line 1232 (S3).
Hunk 1 states *"F does not depend on B, C, D, or E"* and *"G depends only on its own approval and on ADDITIONAL_SOURCE_PRESERVED"* — neither mentions A. S3 hangs F off A in the dependency graph, with the rationale *"F hangs off A, not C"*. The graph implies a dependency the text does not state, and no sentence anywhere says whether PREVENTION_COMPLETE is a precondition for F or G. This is not a drafting nicety: Operation A is the prevention operation for the very defect that creates unexpected drive-root children (base §5.1, lines 686–692). If F may run before PREVENTION_COMPLETE, an F freeze window can itself produce a new drive-root child, which S25's amended §8.3 check would then correctly fail — an entirely avoidable deadlock designed in at the text level.
Fix: state it explicitly in Hunk 1 — e.g. *"F and G each require PREVENTION_COMPLETE, in addition to their own approvals; F does not depend on B, C, D, or E."*

**16. No privacy-review or redaction rule is stated for Operation F or G receipts, though those receipts necessarily name a drive-root path**
Severity: **significant**
Location: Plan v1 lines 1092–1182 (§14.1 and §14.2); base line 1256 (*"Publish only a privacy-reviewed redacted receipt after the shared Git state has settled"*, Operation D only); base §2.2 rules 16–17 (lines 234–245).
Operation F and G receipts bind an exact canonical/final path and physical identity of a drive-root child, plus an off-machine storage object. The design's only publication-redaction rule sits in §8.3 and is scoped to Operation D; §2.2 rule 17's private-by-default rule and rule 16's public/private/quarantine trichotomy are cited nowhere in §14. The packet spends acceptance criterion 20 keeping these identities out of this artifact and the private record; the amendment it proposes creates two new receipt classes carrying those same identities with no stated publication control. This is the local-first/custody axis of my charter: it is the one place in the packet where user-machine identity material gains a new route toward publication.
Fix: add to §14 — *"Operation F and Operation G receipts are private by default under Section 2.2 rules 16 and 17. Publish only a privacy-reviewed redacted receipt; no public receipt names a drive-root child's exact path, physical identity, or off-machine storage object."*

**17. §14.3's freeze-and-compare rule names a closeout step that only Operation D's §8.3 actually performs, so it has no operative trigger for F or G**
Severity: **significant**
Location: Plan v1 lines 1189–1200 (§14.3 "What it changes") and line 1254 (S25); base line 1240, which sits inside `## 8. Operation D` → §8.3.
§14.3 says *"A closeout therefore compares the post-operation drive-root enumeration against the owner-approved baseline **union** the register as frozen at that operation's start"* — phrased generally, over "an operation" and "a closeout". But the only closeout in the design that enumerates drive-root children is §8.3's, which governs **Operation D slices only**. Operations B, C, F and G close out under §4.4's clean-closeout protocol, which has no drive-root enumeration step. So for the two operations §14 creates, the register's delta rule — the entire mechanism Gate 0 answer 3 adopted — never fires. §11's universal *"After each operation/slice"* observation (base lines 1374–1379, amended by S28) covers consistency of registered entries but not the newly-created-child delta.
Fix: either add the drive-root enumeration and register comparison to §14.1's and §14.2's closeout requirements explicitly, or state in §14.3 that the delta check is performed at every B, C, D, F and G closeout and add the corresponding step where each operation's closeout is defined.

**18. S11's new §4.1 item 5 is the only staging item without a "do not build speculatively" guard, and it prescribes a new Operation G launcher**
Severity: **significant**
Location: Plan v1 line 1240 (S11); base lines 453–463, especially item 4's *"Do not build that removal surface speculatively."*
§4.1's existing items are each time-gated (*"Before B or C, approve…"*, *"Before B, add and review…"*, *"Only after C produces the real candidate model… add the D transaction core… Do not build that removal surface speculatively."*). S11's proposed item 5 is phrased entirely as present-tense capability — *"Operation F uses the same established copy/archive/encryption wrappers… Operation G uses its own thin root-quarantine launcher built from the same reviewed template as item 2, bound to its own approved single-root manifest and its own outcome name"* — with no "before" gate and no anti-speculation clause. Read alone inside a section whose purpose is authorizing tooling construction at stated times, it is the sentence a future executor would cite as permission to build a drive-root quarantine launcher now. Acceptance criterion 2 asks exactly this question of every sentence.
Fix: prefix the G half with a gate mirroring item 4 — *"Only after an approved Operation G target manifest exists for one exact root, add the thin root-quarantine launcher… Do not build that mutation surface speculatively."*

**19. Hunk 4's and Hunk 5's characterization of §5.4's outstanding conditions does not match §5.4's text**
Severity: **significant**
Location: Plan v1 lines 926–928 (Hunk 4) and lines 961–963 (Hunk 5); base §5.4 at lines 786–804.
Both hunks cite *"Section 5.4's outstanding conditions - deployment, owner installation verification, the interception and profile captures, and active-guidance coverage"*. Checked against §5.4: there is **no "deployment" condition** — the nearest is *"the owner-approved user-level guard/memory updates are installed and verified"*, which the same sentence separately lists as "installation verification", so "deployment" is a fifth item §5.4 does not contain. There is no "capture" of any kind in §5.4; the corresponding bullets read *"exact deny/allow cases pass on every installed PowerShell 5.1/7 host"* and *"all effective guard registrations and both profiles are tested"*. Only *"active-guidance coverage"* maps cleanly (*"the active guidance scan contains no prescriptive unsafe advice"*). In a design where §8.1 permits only a section's *exact named outcome* to be claimed, paraphrasing a gate's conditions into names it does not use is how an obligation later gets ticked off against the wrong bullet.
Fix: cite §5.4 without renaming its conditions — e.g. *"Section 5.4's outstanding conditions, including the guard-registration and profile tests, the active-guidance scan, and installation and verification of the owner-approved user-level guard/memory updates"*.

**20. Hunk 5 rewrites the approval-state paragraph for accuracy while leaving its approval citation pointing at a path whose resolved lineage does not carry the sign-off it claims**
Severity: **significant**
Location: Plan v1 lines 1419–1425 (evidence gap 6); base lines 6–7.
Base lines 6–7 read *"Gate 0 and Operation A Plan v2 Gate 1 are signed; the dated [planning record](../worktree_cleanup/PLANNING.md) records the approved implementation and verified disposable interactive Windows acceptance."* Plan v1 correctly identifies (and deserves credit for flagging rather than silently fixing) that this relative link resolves to a lineage that does **not** carry the owner's 2026-09-05 Gate 1 sign-off. But Hunk 5 is the hunk whose stated purpose is making the approval-state paragraph accurate, and it leaves the paragraph asserting an approval fact anchored to a citation that does not carry it. Acceptance criterion 2 requires every permissive clause to be anchored to a dated owner approval record; this one is anchored to an ambiguous one.
Fix: within Hunk 5, either drop the *"the dated [planning record] records…"* clause (the approval facts are stated directly in the same sentence and do not need it) or replace it with a lineage-neutral phrase such as *"the approved planning record"* with no link, and record the link repair as the separate out-of-scope decision it is. Do not leave it as an evidence gap only.

**21. `ADDITIONAL_SOURCE_PRESERVED` is parameterized inconsistently, and Operation F's restore gate has no name although the design names gates per operation**
Severity: minor
Location: Plan v1 line 860 and line 872 (Hunk 3a), line 1156 (§14.2 item 1), line 1245 (S16), line 1248 (S19); base line 597 (*"through Gate C"*), line 786 (`### 5.4 Gate A`), line 1031 (`### 7.6 Gate C and isolated restore`).
Hunk 3a defines `ADDITIONAL_SOURCE_PRESERVED(source)`, but §14.2 item 1 writes `ADDITIONAL_SOURCE_PRESERVED(root)` and Hunk 3a's own G bullet and S16 use it unparameterized. §8.1 permits only *"Section 11's exact named outcome"* to be claimed, so the exact spelling of a parameterized outcome is load-bearing. Separately, the design names each operation's gate by letter (Gate A = §5.4 for A, Gate C = §7.6 for C), and S19 refers to *"An offline Operation F restore-gate failure"* — a gate the amendment never names, breaking the convention the base sentence it attaches to relies on.
Fix: use `ADDITIONAL_SOURCE_PRESERVED(source)` everywhere, and give Operation F's restore gate an explicit name in §14.1 so S19's reference resolves.

**22. Hunk 4 ends an unchecked §12 checkbox with the completion statement "The reviewed source is merged."**
Severity: minor
Location: Plan v1 line 932.
The third proposed item is `- [ ]` and lists four outstanding obligations, then closes with *"The reviewed source is merged."* A reader scanning §12's checkbox list sees a status assertion inside an open obligation box; a careless one could read the merged state as the box's subject. It also sits adjacent to §5.4's merge condition (base line 802–803), which is a conjunction — *"passes every Section 4.5 implementation gate including Test Inventory Drift --check, **and** is merged"* — so a flat "is merged" next to an open obligation invites treating that §5.4 bullet as satisfied while the post-merge required check remains undisposed.
Fix: move the sentence out of the checkbox to unbulleted prose under §12, or reword to *"(The reviewed source is merged; Section 5.4's merge condition also requires its implementation gates to have passed.)"*

---

## Categories with no findings

- **Calculation-semantics drift** — none. Verified above: no hunk, sweep edit, or §14 text touches `utils/effective_sets.py`, `utils/weekly_summary.py`, `utils/session_summary.py`, `utils/progression_plan.py`, `utils/volume_*.py`, `utils/_fatigue/**`, `utils/fatigue.py`, or `utils/fatigue_data.py`. Section 0's `none` declaration is accurate.
- **"Effective sets are informational only"** — none. Nothing in the packet reads, thresholds, or gates on Effective vs Raw sets.
- **App terminology drift** — none. No proposed text alters user-facing copy; RIR, RPE, Effective sets / Raw sets, `CountingMode`, `ContributionMode`, Routine, Movement pattern, and Superset appear nowhere in the packet. All terminology findings above (7, 8, 21) are internal to the technical design's own vocabulary.
- **Workflow disruption** — none. The seven core workflows (Plan / Log / Analyze / Progress / Distribute / Profile / Backup) and all navigation and page layout are untouched.
- **Backup contract / DB schema** — no schema change and no change to `program_backup`, `auto_backup`, or the startup sequence. Base §2.2 rule 14's *"Never call create_startup_backup during preservation"* is universally quantified over operations and therefore already covers F and G unchanged. The one adjacent defect is finding 3's dropped startup-snapshot preservation obligation in §14.1.
- **Non-goals / local-first** — no user accounts, no auth, no cloud sync of application data, no remote database, and no telemetry is introduced. The off-machine encrypted upload in §14.1 is preservation under owner approval, mirroring the already-signed §7.5 regime, not application functionality. The two residual local-first risks are findings 5 and 16.
- **Parked / paused workstream conflicts** — none. Fatigue meter Phase 2 Stage 4 (closed 2026-08-13) and learned calibration are untouched, and no threshold constant is in play. The Operation A teardown hold is respected and in fact reinforced: S6 widens base §2.2 rule 2's prune/branch-deletion prohibition to cover F and G, and §14.2 states Operation G *"never uses Operation D's worktree-removal transaction core"*.
- **Scope discipline** — Plan v1 correctly keeps the early targeted rescue decision out (lines 668–671, 1445), decides none of the open Operation A questions (Hunks 4 and 5 record obligations only), touches neither `docs/worktree_cleanup/PLANNING.md` lineage (line 1342), and proposes no successor historical baseline (lines 1446–1448). The only scope-adjacent defect is finding 6's attribution of F and G to the Gate 0 requirements block.

---

**Verdict: Needs revision — three blocking findings (1, 2, 3), none of them a calculation or non-goal violation.**

---

## Response matrix

**59 findings, 43 rows, every finding ACCEPTED.** Nothing was rejected and nothing was
deferred. No rejection was manufactured for balance: the reviewers found real defects,
including three that would have corrupted a signed design on application.

**13 of the 43 rows carry more than one reviewer.** Where two or three reviewers reached
the same defect independently, without seeing each other's work, that is evidence and it
is left visible in a single row rather than split across three. The rows with the
heaviest independent confirmation — B1 (three reviewers), B4 (three reviewers plus a
fourth finding from the same reviewer) — are also the two most mechanically dangerous.

### Blocking — fixed in Plan v2

| # | Finding(s) | Reviewer(s) | Disposition | Action in Plan v2 |
|---|---|---|---|---|
| B1 | AR-2, TS-2, PR-1 | architecture-reviewer, test-strategist, product-risk-reviewer | **ACCEPT** — triple-confirmed independently | Hunk 5's declared span was narrower than its own replacement text, which would have left the design's approval-state paragraph with the B/C/D sentence twice, the E sentence twice, and two closing `*` emphasis terminators. **Plan v2 widens the span further than the reviewers asked — to base lines 6–12, not 8–12** — because PR-20's accepted fix also requires neutralizing the `[planning record](../worktree_cleanup/PLANNING.md)` citation, which lives on base line 6–7. The false *"lines 11–12 unchanged"* parenthetical is deleted. B.3's ordered list records the same span. |
| B2 | AR-3 | architecture-reviewer | **ACCEPT** — the most dangerous finding in the set | Three edits were specified as line replacements but supplied as sentence fragments. Applied literally, S12 truncates §4.1's manifest-digest sentence and orphans `invocation owns exactly one slice:`; S26 leaves §10's `If the` running into `while`; and **S28 deletes `Git/ref relationships, guard installation, quarantines,` from §11's post-operation consistency requirement** — an amendment about drive-root children silently removing guard installation and quarantines from a completion check. Plan v2 restates all three as full-line replacements reproducing every non-target token verbatim. **Then it re-audits the whole edit set for the same defect class, not only the three named**: Plan v2's B.1 now presents every edit as an explicit `FROM` / `TO` pair reproducing complete lines, and B.3 marks every row **R** (line replacement) or **I** (insertion). The re-audit found the same latent risk in S2, S4, S5, S6, S7, S8, S14, S20, S22, S23 and S31, all of which are now full-line. |
| B3 | TS-3, AR-19 | test-strategist, architecture-reviewer | **ACCEPT** | Plan v1 carried four mutually inconsistent self-counts, so its anchor-verification claim covered 31 of the 36 edits an executor would apply. Plan v2 makes **B.3 the single authoritative edit list**, states its length exactly once, and has the anchor-verification sentence quote that same number. The architecture-reviewer independently re-derived Plan v1's anchors and confirmed **all 36 plan-file anchors plus the one `INDEX.md` anchor resolve byte-exact**, so the claim is restated over that verified set and then re-derived again for the six anchors Plan v2 adds or widens. |
| B4 | AR-4, AR-5, TS-4, PR-8 | architecture-reviewer (×2), test-strategist, product-risk-reviewer | **ACCEPT** — triple-confirmed, and operative, not cosmetic | Three separate defects in one place. (a) The term was defined twice in non-identical forms while §14.0 claimed it was defined once; Plan v2 makes **Hunk 1 a pointer** and leaves the operative definition in §14.0 alone. (b) §14.0's *"it is a statement about path identity, not about approval status"* clause was false of the definition it followed; it is **deleted**, and replaced with the accurate noun-versus-qualifier statement. (c) Operatively: Hunk 1's no-preservation/no-removal-authority sentence was scoped to the *scope-qualified subset*, so it would lapse at the moment a manifest was approved — exactly what criterion 12 forbids, and what D3 did not achieve. Plan v2 **re-anchors it to any unexpected drive-root child**. See the note below this table on how that re-anchoring avoids colliding with Operation B. |
| B5 | AR-1 | architecture-reviewer | **ACCEPT** | Operation F's cardinality was self-contradictory: §14.1's requirements spoke of a closed set while S12 and S16 bound one source, so a multi-source F was approvable with no launcher, no approval record, and no closable outcome. Plan v2 resolves toward the **closed set** — one Operation F operation binds one approved closed set of sources — and rewrites the §14.1 opening, S12 and S16 accordingly. `ADDITIONAL_SOURCE_PRESERVED(source)` stays **per source**, and Plan v2 states explicitly that **no set-level aggregate exists**. Rationale: acceptance criterion 6 is owner-signed and speaks of an exact closed set with the freeze budget recalculated *"for the complete set"*, so the single-source reading strains a signed criterion. **Flagged as an owner-visible choice at Gate 1.** |
| B6 | PR-2 | product-risk-reviewer | **ACCEPT**, using the reviewer's exact wording | S24's *"Operation F is outside this gate"* sits inside `### 7.6 Gate C and isolated restore`, where *"this gate"* reads as Gate C — excusing F from the isolated restore, the whole-tree equality proof, and the sanitizer requirements. Plan v2 replaces the opening clause with *"Operation F is outside PRESERVATION_COMPLETE. Operation F still performs every Section 7.6 restore verification for its own sources, under Operation F's own gate;"* and keeps the remainder as drafted. §14.1 now also names that gate **Gate F**, closing PR-21's second half. |
| B7 | PR-3 | product-risk-reviewer | **ACCEPT**, taking the reviewer's second fix | §14.1 requirement 2 was framed as restating §7.5's obligations but silently dropped the manifest-enumerated **startup-snapshot** preservation, `handovers/claims`, `recovery/salvage directories`, and the no-install/no-repair clause. Plan v2 replaces the restatement with *"Every obligation of Section 7.5 applies to each source in the set, unchanged"* plus an explicit, closed list of the only two scope-specific deviations. **That closes the class, not the three instances** — a future §7.5 obligation is carried automatically. |
| B8 | TS-1, PR-14 | test-strategist, product-risk-reviewer | **ACCEPT** — already corrected, and the correction is recorded rather than hidden | Section 0's *"Council status"* asserted the council *"has been run"* and that findings were recorded below, while five sections of the same artifact said NOT STARTED. The sentence was written by the manager at the moment Gate 0 was signed, **before any reviewer was spawned**, and was false when written. Both reviewers caught it while it was still false — which is the review working. Section 0 now states the council is authorized, asserts no outcome, and carries a recorded-defect note naming the reviewers who caught it. **Section 0 is not edited by this council step.** The correction **moved no approval status**: Gate 0 was and remains signed on the owner's own verbatim text, and Gate 1 was and remains unsigned. The remaining half of both findings — the owed `product-manager` ID — is discharged by the Agent provenance block above, which now carries every real agent ID. |

**Note on B4's re-anchoring, raised by the `product-manager` rather than by a reviewer.**
Re-anchoring the protection sentence to *any* unexpected drive-root child has a
consequence neither the reviewers nor the manager's disposition names: `D:\c` and
`D:\d` **are** unexpected drive-root children — the dated evidence records that they are
deliberately excluded from the owner-approved baseline, which is why the audit reports
them and exits non-zero by design. A flat prohibition over "any unexpected drive-root
child" would therefore collide with Operation B's already-approved quarantine authority
for those exact two roots. Plan v2 avoids that by phrasing the sentence as a
**no-implicit-authority** rule rather than a prohibition: nothing in this plan's
proximity, classification, timestamp, receipt, aggregate, approval, manifest, or
baseline surfaces confers authority over any unexpected drive-root child, and authority
exists only where this plan names it explicitly — as Operation B's two named roots are
named — or under a dated §4.3 owner approval. That closes the lapse criterion 12
identifies **without** narrowing Operation B.

### Significant — all accepted

| # | Finding(s) | Reviewer(s) | Disposition | Action in Plan v2 |
|---|---|---|---|---|
| 9 | AR-6 | architecture-reviewer | ACCEPT | §14.1's opening scoped Operation F to *any* source outside Operation C — a route for arbitrary paths on any volume. Plan v2 opens §14.1 with *"exactly identified unexpected drive-root children that are outside approved operation scope under Section 14.0"* and states that F is **not** a general route for arbitrary sources outside Operation C's scope. |
| 10 | AR-7 (with the D4 miss) | architecture-reviewer | ACCEPT | Six sections Plan v1 claimed cross-referenced §14 contained no pointer, and D4's required reciprocals existed only at §4.2 and §4.3. Plan v2 adds an explicit `(Section 14)` pointer to S11, S17, S20, S22, S25 and S32, so §2.2, §4.1, §4.4, §4.5, §7.5 and §8.3 each carry one, and corrects B.0's placement claim to state only what the edits actually do. |
| 11 | AR-8, PR-11 | architecture-reviewer, product-risk-reviewer | ACCEPT — independently confirmed | §12's shared-lock item stayed at `B-E` on a reason that does not follow: *"single"* carries the cardinality, not the range. Plan v2 adds **S31**, replacing base line 1397's `B-E` with `B-G`, and moves the row from B.2 to B.1. |
| 12 | AR-9 | architecture-reviewer | ACCEPT | F and G had named outcomes quantifying over states they never defined. Plan v2 states that **Operation G adopts §6's forward states and terminal branches unchanged**, reading *"root"* as the Operation G root, and gives **Operation F §7.2's abort model explicitly**, with its safe-abort boundary at the first preservation write and no archive-ref creation at all. |
| 13 | AR-10, PR-21 | architecture-reviewer, product-risk-reviewer | ACCEPT — independently confirmed | Three parameterizations of one outcome name, in a design where §8.1 permits only *"Section 11's exact named outcome"*. Plan v2 uses `ADDITIONAL_SOURCE_PRESERVED(source)` in all four places, states the **F-source ↔ G-root identity equivalence** explicitly as a required equality rather than an inferred resemblance, and names F's restore gate **Gate F** so S19's reference resolves. |
| 14 | AR-11 | architecture-reviewer | ACCEPT | S1 and S2 made the rollout order binding on F while Hunk 1 asserted independence. Plan v2 states the intended rollout position once, in §14.0: F and G require `PREVENTION_COMPLETE` and their own approvals, and beyond that may be commissioned at any point after the stabilization checkpoint and fresh evidence, independently of whether B, C or D has been approved or scheduled. |
| 15 | AR-12, PR-5 | architecture-reviewer, product-risk-reviewer | ACCEPT — independently confirmed | *"At least one member class"* was trivially satisfiable, and an F source is approved for off-machine upload. Plan v2 requires **every member class present to be enumerated and characterized, and the absence of each unlisted class positively recorded**, with an uncharacterized class making the source unapprovable. |
| 16 | AR-13 | architecture-reviewer | ACCEPT | §7.3 and §7.4 were omitted from F although F's own member-class list contemplates nested repositories. Plan v2 adds a requirement: any Git repository inside an F source carries §7.3's OID enumeration, type-checking and archive-ref obligations and §7.4's separate preservation and restore-test, or the source is not approvable under F. |
| 17 | AR-14 | architecture-reviewer | ACCEPT | The register gated closeouts with no digest, no §4.3 binding, and no evidence root, so *"frozen at operation start"* was unverifiable. Plan v2 adds **S33**, binding the SHA-256 digest of the register as frozen at operation start into §4.3's **common** approval fields — the fields B, C and D approvals bind — gives the register an evidence-root home under §3.1, and requires the closeout receipt to record the same digest. |
| 18 | AR-15, PR-12 | architecture-reviewer, product-risk-reviewer | ACCEPT — independently confirmed | Plan v2 adds **S30**, retitling base line 50 to *"### 1.2 Independently completable operations"* — count-free, which also removes a count from a stable-policy surface under §1.1. `BASE:1374` and `BASE:552` are added to B.2 with the reason that their universal quantifier already covers F and G; `BASE:1374` is additionally edited by S28 for a different purpose. |
| 19 | AR-16, PR-13 | architecture-reviewer, product-risk-reviewer | ACCEPT — independently confirmed, and escalated to the owner | Criteria 14 and 17 are in genuine tension over *"the cancelled post-merge required check"*: 14 bans a **CI run outcome** from the design; 17 lists that disposition among the obligations the design must state. The owner signed both. Plan v2 adopts the **outcome-free phrasing** in both Hunk 4 and Hunk 5 — *"the outstanding post-merge required-check disposition recorded in the dated operation evidence"* — which satisfies 17's obligation without asserting 14's banned fact, and removes Plan v1's commentary claim of full criterion-14 compliance. **Listed in the owner-choice subsection**; the owner may prefer to let 17's own phrasing stand. |
| 20 | AR-17, PR-20 | architecture-reviewer, product-risk-reviewer | ACCEPT — independently confirmed | Two pointers, one lineage problem. Plan v2 (a) widens Hunk 5's span to base 6–12 and replaces the linked `[planning record](../worktree_cleanup/PLANNING.md)` citation with the **lineage-neutral, unlinked** *"the approved planning record"*, and (b) adds **S34**, one dateless sentence in §1.3 stating that each later semantic amendment records its own Gate 0 and Gate 1 in its own council artifact and naming this amendment's artifact path. Neither repairs the divergent-lineage collision, which stays the separate out-of-scope owner decision it is. **Listed in the owner-choice subsection.** |
| 21 | AR-18, PR-9 | architecture-reviewer, product-risk-reviewer | ACCEPT — independently confirmed | §7.5's *"Preserve … recovery/salvage directories …"* bullet, six lines below Hunk 2's new paragraph, is the exact surface Section 0's Problem item 2 names as the strongest "discovery obliges capture" misreading, and Plan v1 left it unedited. Plan v2 adds **S32**, qualifying the bullet to preservation *within C's approved immutable source manifest* and stating that the bullet adds nothing to that manifest. |
| 22 | AR-20 | architecture-reviewer | ACCEPT | S5 departed from the plan's own range policy with an unrecorded ad-hoc list. Plan v2 widens it to `Sections B-G retain`, restoring the policy. |
| 23 | AR-21, PR-17 | architecture-reviewer, product-risk-reviewer | ACCEPT — independently confirmed; folded into one fix | The register's delta check lived only in §8.3, which is Operation D's slice closeout, so **for F and G — the two operations the owner's answer 3 exists to serve — the mechanism never fired**. Plan v2 fixes it in three places at once: §14.1 and §14.2 each state the comparison as a closeout step; **S28 lifts it into §11's universal *"After each operation/slice"* observation**, which covers B, C, D, F and G in one edit; and §14.3 states where each trigger lives. AR-21's second half is also taken: §14.3 now says that a registered entry retired by a completed Operation G is dispositioned by the owner at that closeout, and until then the entry stands with its recorded identity expected absent. |
| 24 | AR-22 | architecture-reviewer | ACCEPT | S25's *"post-operation drive-root enumeration"* was undefined. Plan v2 binds it to **a no-follow enumeration (§2.2 rule 9) of the configured drive roots (§5.2)**, in S25, in §14.1, in §14.2, and in §14.3, so all four say the same thing. |
| 25 | AR-23, TS-13 | architecture-reviewer, test-strategist | ACCEPT — independently confirmed, all three parts of TS-13 taken | (a) `INDEX.md`'s *"separately approved routes"* is reworded to **"routes that require their own separate approval"**. (b) A one-line out-of-context reading of each hunk is added below this table. (c) Plan v2 states explicitly that **criterion 19 is evidenced by the session transcript, not by the artifact** — no text in the amended design can evidence a command that was not run. |
| 26 | TS-5 | test-strategist | ACCEPT | Plan v2's Expected gates now name `tests/test_agent_workflow_contracts.py` as a targeted pytest run in the standalone clone, and record `SHARED_PLAN`, `Tier <digit>` and `Appendix A<digit>` as **apply-time forbidden strings** binding on any re-drafted text — not merely as something a reviewer read once. |
| 27 | TS-6 | test-strategist | ACCEPT | Plan v2 names the checkout-local red explicitly: a pytest run from *this* checkout is expected red on `test_every_surface_file_is_tracked_by_git`, that red belongs to the checkout rather than the amendment, it is **not** repaired by regenerating the inventory, and it is not a gate result. On a branch cut from `origin/main` the file is tracked and the test passes. |
| 28 | TS-9 | test-strategist | ACCEPT — named by the reviewer as the single highest-value verification the plan was missing | Criterion 10's universal half cannot be demonstrated by reading the amended design. Plan v2 converts it into a **required apply-time closure re-grep against the amended file**, with the reviewer's exact pattern list, asserting every surviving hit is on the recorded-inapplicable list. Evidence gap 8 stops being an admission and becomes a repeatable check. |
| 29 | TS-10 | test-strategist | ACCEPT — and the answer is worse than the finding anticipated | The manager closed this read-only: **`docs/worktree_cleanup/evidence/2026-09-28-state.md` is not tracked on `origin/main`.** `git ls-tree origin/main -- docs/worktree_cleanup/` returns exactly two blobs, neither of which is that file nor the source packet. Criteria 14, 16 and 17 move every dated fact out of the tracked design into a file that **does not exist for any reader of `origin/main`** — as drafted the amendment deletes those facts from the tracked record and points at nothing. Plan v2 states this plainly and puts three remedies to the owner at Gate 1 without choosing. **Listed in the owner-choice subsection, with a recommendation.** |
| 30 | TS-11 | test-strategist | ACCEPT | Assumption nine's trigger was unevaluable — ambiguous between "this diff changes tooling" (false) and "the amended design obliges someone to build tooling later" (true, for Operation G's launcher). Plan v2 restates it as **"changes a file outside `docs/ai_workflow/**`"**, the condition the change-type table actually keys on, and records separately that Operation G's launcher is future work behind its own approval with its own change-type derivation at that time. |
| 31 | TS-12 | test-strategist | ACCEPT — all four apply-time failure modes | Plan v2 adds an **Apply-time verification protocol** carrying every one: per-edit post-conditions (anchor text absent, replacement text present exactly once) plus an expected final line count; a `git hash-object` precondition against both recorded blob OIDs **before the first edit**; the requirement that the clone has `npm ci` and a venv before `--check` means anything and that any collector `SystemExit` is a tooling failure, never a green; and the statement that a `Test Inventory Drift` green pins counts only. |
| 32 | PR-4 | product-risk-reviewer | ACCEPT | §14.1 had no "no authority exists" opener and no §4.3 approval item while §14.2 had both, making §14.1 the packet's weakest surface when read alone. Plan v2 opens §14.1 with *"No Operation F preservation authority exists for any source until every one of the conditions below is true"* and makes requirement 1 a §4.3 immutable digest-bound manifest plus a dated owner approval record created separately from and after this plan text. |
| 33 | PR-6 | product-risk-reviewer | ACCEPT | S1 placed F and G inside a block the design attributes to *"The Gate 0 requirements impose this program order"*, making the signed 2026-09-05 record appear to impose the new work — the reverse inference criterion 3 exists to close. Plan v2 moves the F/G text **outside** the attributed block as following prose that explicitly disclaims the attribution. |
| 34 | PR-7 | product-risk-reviewer | ACCEPT | §14.0 cited five sections as using the term; §5.1 says *"unintended"* (discriminated by **cause of creation**), §5.2 says *"unexpected new children"*, and §6 says *"other unexpected root"* (discriminated against the **allowlist**). Plan v2 narrows the citation to §8.3 and §11, states §5.1's and §6's senses accurately and separately, and records that both are **left unrenamed** and why — renaming §5.1's causal description would falsify a root-cause statement. |
| 35 | PR-10 | product-risk-reviewer | ACCEPT | Hunk 4 dissolved the standing plan-level Gate 1 obligation into a conditional future one. Plan v2 keeps **both** unchecked boxes: base line 1389's `- [ ] Approve the Gate 1 council-reviewed version of this plan.` **verbatim**, plus the renewed-Gate-1 item. |
| 36 | PR-15 | product-risk-reviewer | ACCEPT — recommendation recorded, decision left open | The reviewer's deadlock argument is that an F freeze could itself create a drive-root child that the amended §8.3 and §11 delta checks would then correctly fail. Plan v2 **requires `PREVENTION_COMPLETE` for both F and G** and says so in §14.0 and in Hunk 1. **Listed in the owner-choice subsection**, with the second-order effect named: requiring it keeps single-location material unpreserved until Operation A completes, which makes the out-of-scope early-rescue question more pressing, not less. |
| 37 | PR-16 | product-risk-reviewer | ACCEPT | F and G receipts necessarily bind a drive-root path, a physical identity and an off-machine storage object, while the design's only redaction rule is §8.3's and is Operation D-only. Plan v2 adds the reviewer's clause to §14.0, binding F and G receipts to §2.2 rules 16 and 17 as private by default with privacy-reviewed redacted publication only. |
| 38 | PR-18 | product-risk-reviewer | ACCEPT | S11's §4.1 item 5 was the only staging item with no time gate and no anti-speculation clause, while prescribing a quarantine launcher. Plan v2 gates the G half — *"Only after an approved Operation G target manifest exists for one exact root…"* — and adds *"Do not build that mutation surface speculatively."* |
| 39 | PR-19 | product-risk-reviewer | ACCEPT | §5.4 has no *"deployment"* condition and no *"captures"*; the hunks renamed a gate's conditions, which is how an obligation later gets ticked against the wrong bullet. Plan v2 cites §5.4 **without renaming its conditions**, and keeps "the deployment decision" only where it belongs — as the point before which the successor reconciliation must happen, not as a §5.4 condition. |
| 40 | PR-22 | product-risk-reviewer | ACCEPT | *"The reviewed source is merged."* sat inside an unchecked §12 box. Plan v2 moves it out of the checkbox into unbulleted prose appended at the end of §12 by S29, and pairs it with §5.4's merge condition being a conjunction. |
| 41 | TS-7 | test-strategist | ACCEPT | Plan v2 states the `Test Inventory Drift` **mechanism**: the generator has no configuration-surface collector, and the `docs/ai_workflow/` sensitivity arrives entirely through `tests/test_agent_workflow_contracts.py`'s parametrized `SURFACE`, whose node count is a committed `pytest.files[]` row. That is what tells an executor the count is safe while the content is asserted. |
| 42 | TS-8 | test-strategist | ACCEPT | Plan v2 names **both** steps of the `Type Check (tsc blocking + pyright measure-only)` required context and records both as inapplicable — no `.py` and no `.ts` in the diff. |
| 43 | TS-14 | test-strategist | ACCEPT — **resolved**, not left open | The reviewer disclosed reading the modified working-tree `QUALITY_GATE.md` and could not diff it. The manager extracted the `origin/main` blob `d3cd6f5ffa6845dc68a588412d96103440679ae2` and diffed it: the only difference is reviewer-selection prose. **The plan-stage routing table, the change-type table, the `Test Inventory Drift` rows, and the two-step `Type Check` row are byte-identical.** Every routing conclusion in Plan v1 and in the reviewer's report therefore holds on the `origin/main` base. Recorded in Agent provenance as closed. |

### Criterion 2 — the out-of-context reading of each hunk (TS-13a)

Each proposed hunk, read as an isolated sentence by a reader with no surrounding
context. This is the check criterion 2 imposes and that Plan v1 left self-assessed.

| Hunk | Read alone, it says | Verdict |
|---|---|---|
| **1** (§1.2) | "Section 14.0 defines the term; such a child is retained and recorded only; nothing in this plan confers authority over any unexpected drive-root child except where named explicitly or under a dated §4.3 approval; §14 approves neither operation." | Safe. Defines a shape and denies authority in the same breath. |
| **2** (§7.5) | "Inventory these categories and the owner paths *enumerated in C's approved manifest*; discovery is not a source grant; discovery never adds a directory to an immutable source manifest; adding one requires the separate Operation F approval, which this plan does not give." | Safe. The only imperative is to inventory; every permissive reading is closed in the same paragraph. |
| **3a** (§11) | "`ADDITIONAL_SOURCE_PRESERVED(source)` and `DRIVE_ROOT_CHILD_RETIRED(root)` mean these things, per source and per root, with no plural aggregate, and neither contributes to any existing outcome." | Safe. Definitions of outcome names, each carrying an explicit non-contribution clause. |
| **3b** (§11) | "Preserving under F grants no removal authority; no existing receipt authorizes a G step; G is archive plus quarantine and never deletion; permanent deletion stays a separate later operation." | Safe — this hunk is entirely prohibitive. |
| **4** (§12) | Three checkboxes: one checked, recording a past Operation A Gate 1; two unchecked, recording outstanding obligations. | Safe. A checked box records a signed past approval; nothing grants future authority. |
| **5** (header) | "Gate 0 and Operation A Plan v2 Gate 1 are signed; A's source is merged; these obligations remain open; B, C and D still require their approvals; E, F and G are separately planned and approved and F and G are not approved here." | Safe. Every status is either a recorded past approval or an explicit open obligation. |
| **6** (`INDEX.md`) | "…and the **routes that require their own separate approval** for drive-root children outside Operations B and C; planning only; Gate 0 and Operation A Plan v2 Gate 1 signed; these items pending." | Safe **after** the AR-23/TS-13 rewording. As drafted in Plan v1 it was not: *"separately approved routes"* read at least as naturally as "routes that have been approved". |
| **N** (§14) | Longest surface, and the one criterion 2 most strains. Every subsection now opens with a no-authority sentence (§14.0's blanket clause, §14.1's *"No Operation F preservation authority exists…"*, §14.2's *"No Operation G retirement authority exists…"*), and §14.3 opens by saying what the register is **not**. | Safe, but it is the surface a future reviewer should re-test first. |

### What this matrix does not do

- It selects **no option** for the early targeted rescue decision, and does not count it.
- It resolves **none** of the open Operation A decisions. Hunks 4 and 5 record
  obligations; they decide nothing.
- It proposes **no** successor drive-root baseline and **no** change to the owner-approved
  2026-09-06 baseline.
- It applies **no** hunk. Every disposition above is a change to proposed text inside this
  artifact only.
- It checks **no** Gate 1, Plan v2, or Sign-off box.

---

## Plan v2

*Complete replacement plan. Plan v1 is left intact above as the audit trail. Every one
of the 59 accepted findings is reflected here; nothing was deferred.*

**Goal**: Produce the exact, final, quotable amendment text that gives a drive-root
directory outside Operation B's two named roots and outside Operation C's approved
source scope a defined classification, a gated route to preservation, a gated route to
eventual retirement, a determinate closeout meaning, and an accurate dateless record of
Operation A — without approving any source, any target, any removal, or any filesystem
mutation.

### Scope

**In**

- **42 edits** against two hash-verified `origin/main` blobs: 41 against
  `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` (27 line replacements, 14 insertions) and
  1 against `docs/ai_workflow/INDEX.md` (1 line replacement). B.3 below is the single
  authoritative list, and **42** is the only edit count this plan states.
- A new `## 14.` section carrying the contracts for **Operation F** (separately approved
  additional-source preservation) and **Operation G** (separately approved drive-root
  child retirement), plus the owner-dispositioned known-unexpected register.
- Enrolment of F and G by name everywhere the design quantifies over operations, or a
  written reason each site is inapplicable.
- Reciprocal `Section 14` pointers from §2.2, §4.1, §4.2, §4.3, §4.4, §4.5, §7.5 and
  §8.3 back to the carrier (resolution D4, widened by AR-7).
- An **apply-time verification protocol** (section C) that turns the plan's self-audit
  claims into mechanical checks.

**Out**

- Applying any hunk. This plan contains proposed text as quoted blocks only. No hunk is
  applied to either file before Gate 1.
- Naming, proposing, approving, or characterizing any actual source or target. RESIDUE-1
  and RESIDUE-2 are never named, pathed, hashed, counted, or enumerated in the proposed
  text; they are not manifest entries and not register entries here.
- Any filesystem mutation, preservation copy, protective copy, quarantine, move,
  deletion, junction unlink, archive-ref creation, prune, worktree add/remove, or ref
  change.
- The early targeted rescue decision — undecided, unselected, uncounted, and deliberately
  **not** added to §12's decision list.
- Editing §5.2's audit, the owner-approved 2026-09-06 baseline, or `docs/test_inventory/`.
- Either divergent lineage of `docs/worktree_cleanup/PLANNING.md`.

### The two new operation classes

| Class | Full name | Template | Named §11 outcome |
|---|---|---|---|
| **F** | Operation F — separately approved additional-source preservation | Operation C's capture, encryption, off-machine and isolated-restore gates, applied to an approved closed set | `ADDITIONAL_SOURCE_PRESERVED(source)` — **per source** |
| **G** | Operation G — separately approved drive-root child retirement | Operation B's per-root archive-and-quarantine template and §6's state machine | `DRIVE_ROOT_CHILD_RETIRED(root)` — **per root** |

Letters keep the sweep mechanical: every `B-E` range quantifier widens to `B-G` and
stays a range. **No plural aggregate is defined over either class**, and the text says
so — §8.1 permits only *"Section 11's exact named outcome"* to be claimed, and an
unqualified plural over an open set would be unclosable.

**Cardinality, resolved (B5/AR-1).** One Operation F operation binds **one approved
closed set** of sources; its outcome remains per source and no set-level aggregate
exists. This follows owner-signed criterion 6, which speaks of an exact closed set with
the freeze budget recalculated *"for the complete set"*. Flagged for the owner in
section E.

### Terminology — D3, with the reviewers' corrections

- The source packet's **"unapproved drive-root child"** is rejected: it would go false at
  manifest approval while *"unexpected"* must stay true, splitting the §8.3/§11 checks
  from §5.2's audit.
- The noun `unexpected drive-root child` is reused, with the scope qualifier *outside
  approved operation scope* **defined once, in §14.0 only**. Hunk 1 points at that
  definition and does not restate it (B4).
- The citation is narrowed to **§8.3 and §11**, the only two sections using the exact
  term. §5.1's *"unintended drive-root child"* is a **causal** description of how path
  conversion creates one, and §6's *"other unexpected root"* is discriminated against the
  **configured drive-root allowlist**. Both are stated accurately and **left unrenamed** —
  renaming §5.1's causal description would falsify a root-cause statement (PR-7).
- The false *"a statement about path identity, not about approval status"* clause is
  **deleted** (AR-5/PR-8). What replaces it is accurate: the noun is fixed by the
  owner-approved baseline; only the qualifier depends on manifest approval; and the
  **no-implicit-authority rule is anchored to any unexpected drive-root child**, so no
  protection lapses when a manifest is approved — while Operation B's named authority
  over its own two roots is untouched.

### Anchor mechanics

**Discipline: strictly bottom-up, descending anchor line, single pass, no
re-derivation.** B.3 gives the full ordered list.

**Every replacement edit is specified as a full-line replacement whose `TO` text
reproduces every non-target token of the replaced lines verbatim** (B2/AR-3). Plan v1's
fragment-style specification would have truncated §4.1's manifest-digest sentence,
broken §10's `If the …` clause, and deleted `Git/ref relationships, guard installation,
quarantines,` from §11. B.1 now presents every edit as a `FROM` / `TO` pair, and B.3
marks every row **R** (replacement) or **I** (insertion).

**Anchor verification.** The `architecture-reviewer` independently re-derived Plan v1's
anchors against the extracted blobs and confirmed **all 36 plan-file anchors and the one
`INDEX.md` anchor resolve, every quoted anchor line byte-exact**. Plan v2 adds or widens
**nine** anchors — BASE:6–12, 50, 85–86, 106, 251–252, 524–525, 998–999, 1374–1379,
1397–1398 — and this `product-manager` re-derived each of those nine against the same
blobs. **All 41 plan-file anchors and the 1 `INDEX.md` anchor resolve cleanly. No edit
failed to apply and nothing was silently rebased.**

Bases: `WORKTREE_CLEANUP_PLAN.md` = `origin/main` blob
`1b41922e795e9202f128a9b1122d0ffb6c6134af`, 1471 lines. `INDEX.md` = `origin/main` blob
`027af297b1658f70f353dd298c545fa4108c6def`, 91 lines.

---

## A. The six hunks

### Hunk 1 — §1.2, pointer and boundary · **I** · insert after BASE:95

**Anchor** (BASE:95): `  TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED, not successful worktree retirement.`
BASE:96 is blank; BASE:97 is `### 1.3 Planning-artifact landing gate`.

**TO** (appended bullet, then the boundary paragraph):

```
- F and G each require PREVENTION_COMPLETE and their own approvals. Beyond that they
  are independent: F does not depend on B, C, D, or E; no D slice, no E operation, and
  no PRESERVATION_COMPLETE waits on it; and an F failure blocks only G, and only for
  the source identities it failed to preserve. G depends only on its own approval and
  on ADDITIONAL_SOURCE_PRESERVED(source) already proved for its exact root identity.
  Neither is part of worktree-cleanup completion.

Section 14.0 defines when an unexpected drive-root child is outside approved operation
scope; that definition is stated only there, and such a child is retained and recorded
only. No proximity to a named root, generated-output classification, filesystem
creation time, previous campaign completion receipt, aggregate, receipt, approval
record, manifest, or baseline entry in this plan confers preservation, relocation,
quarantine, or removal authority over any unexpected drive-root child. Authority
exists only where this plan names it explicitly, as Operation B's two named roots are
named, or under a dated Section 4.3 owner approval record created separately from and
after this plan text. Section 14 defines the shape of two separately approved
operations, F and G, and approves neither: this plan names no source and no target for
either. Completing either changes no Operation B aggregate, no Operation C
PRESERVATION_COMPLETE, no Operation D worktree-slice outcome, and no
PREVENTION_COMPLETE declaration, and permits neither an edit to the owner-approved
drive-root baseline nor a zero exit from the Section 5.2 audit.
```

*Changes from v1: definition replaced by a pointer (AR-4/TS-4); no-authority sentence
re-anchored to* any *unexpected drive-root child without narrowing Operation B
(PR-8, plus the `product-manager` note in the matrix); `PREVENTION_COMPLETE` stated as a
precondition (PR-15); rollout position stated once (AR-11).*

---

### Hunk 2 — §7.5, discovery is not a source grant · **R** · replace BASE:990–992

**Why §7.5 and not §7.2.** With a separate operation, additional-source language must
not land in §7.2 at all: §7.2 is Operation C's whole-tree scope paragraph and the
highest-risk surface under criterion 2. §7.2 is proposed **unchanged**, deliberately.
Criterion 8's sentence must appear *in §7.5 itself*, and §7.5 is where the
*"explicit owner paths"* hook lives.

**FROM** (BASE:990–992):

```
Inventory every root discovered in the pre-stop runtime map plus the repository,
artifacts, recovery/backup directories, local application-data roots, and explicit
owner paths.
```

**TO**:

```
Inventory every root discovered in the pre-stop runtime map plus the repository,
artifacts, recovery/backup directories, local application-data roots, and the owner
paths enumerated in C's approved immutable source manifest. A path is an inventory
target only because one of those categories covers it; being named by the owner
somewhere outside the approved manifest does not make it one.

This inventory is a discovery obligation, not a source grant. When it observes a
drive-root directory outside C's approved source scope, that directory is recorded and
retained only: discovery never adds it to an immutable source manifest, and discovery
alone obliges no capture. Adding any such directory to a source manifest requires the
separate Operation F approval of Section 14.1, which this plan does not give.
```

---

### Hunk 3a — §11, the two named outcomes · **I** · insert after BASE:1372

**Anchor** (BASE:1372): `- MAIN_RECONCILIATION_COMPLETE: E's independent plan passes.`

**TO**:

```
- ADDITIONAL_SOURCE_PRESERVED(source): that one Operation F source, bound by exact
  canonical/final path and physical identity in F's approved immutable source
  manifest, has an Operation F live capture with VERIFIED_CLEAN_CLOSEOUT in the shared
  register, maintenance restored where F suspended it, no F-caused BLOCKED_RECOVERY
  remaining, a passing final capture receipt, and every Section 14.1 Gate F
  whole-tree, encryption, off-machine, and isolated-restore check passing for that
  exact source. The outcome is defined per source. This plan defines no aggregate over
  an Operation F source set; an aggregate claim would require a later amendment naming
  an exact closed set and reviewed under Section 1.1.
  ADDITIONAL_SOURCE_PRESERVED(source) is not an input to PRESERVATION_COMPLETE,
  neither contributes to nor blocks it, and authorizes no Operation B, D, or E step.
- DRIVE_ROOT_CHILD_RETIRED(root): that one Operation G root, bound by exact
  canonical/final path and physical identity in G's approved immutable target
  manifest, has ADDITIONAL_SOURCE_PRESERVED(source) already proved for an Operation F
  source whose exact identity is that same root, has a VERIFIED Operation G attempt
  under Section 14.2's adopted Section 6 state machine with the complete Section 4.4
  clean-closeout protocol and final root receipt, is absent from its original path, is
  exact in its operation-specific nonexistent same-volume quarantine destination, and
  is independently recoverable off-machine from the stored secret. The outcome is
  defined per root. This plan defines no aggregate over Operation G roots. It does not
  alter, satisfy, or contribute to MALFORMED_ROOT_QUARANTINED(root),
  MALFORMED_ROOTS_QUARANTINED, PRESERVATION_COMPLETE, PREVENTION_COMPLETE,
  TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED, WORKTREE_SLICE_COMPLETE,
  WORKTREE_SLICE_PARTIAL_CLOSED, or WORKTREE_CLEANUP_COMPLETE, and is not part of any
  of them.
```

---

### Hunk 3b — §11, the retirement boundary · **I** · insert after BASE:1384

**Anchor** (BASE:1384): `operations with new exact manifests. Nothing expires automatically.`

**TO**:

```
Preserving a source under Operation F grants no quarantine, relocation, or removal
authority for it. No Operation F receipt, Operation B receipt, Operation C receipt,
Operation D receipt or campaign target set, approval record, or baseline entry in this
plan authorizes an Operation G step; Operation G authority exists only under its own
dated Section 4.3 owner approval, created separately from and after this plan text.
Operation G's route is archive plus non-overwriting same-volume quarantine and never
recursive deletion, so completing it deletes nothing. Permanent deletion of an
Operation F preservation object or an Operation G quarantine payload remains a
separate later operation with its own exact manifest and owner approval, exactly as
for B and C above.
```

---

### Hunk 4 — §12, the Operation A record · **R** · replace BASE:1389

**FROM** (BASE:1389): `- [ ] Approve the Gate 1 council-reviewed version of this plan.`

**TO**:

```
- [ ] Approve the Gate 1 council-reviewed version of this plan.
- [x] Approve Operation A Plan v2 at Gate 1 (signed 2026-09-05); this approved neither
      B-G execution nor any later semantic amendment to this design.
- [ ] Approve the renewed plan-level Gate 1 that Section 1.1 requires after each later
      semantic amendment to this design.
- [ ] Complete Section 5.4's outstanding conditions as that section states them,
      including installation and verification of the owner-approved user-level
      guard/memory updates; satisfy Section 11's PREVENTION_COMPLETE requirement that
      lifecycle monitoring is active; complete the outstanding post-merge
      required-check disposition recorded in the dated operation evidence; and
      reconcile any successor of the reviewed guard and test artifact against the
      reviewed bytes before the deployment decision.
```

*Changes from v1: the original plan-level Gate 1 box is **retained verbatim** as the
first line (PR-10); §5.4's conditions are cited without being renamed (PR-19);
`"the cancelled post-merge required check"` becomes the outcome-free `"the outstanding
post-merge required-check disposition recorded in the dated operation evidence"`
(AR-16/PR-13); `"The reviewed source is merged."` moves out of the checkbox into S29's
prose (PR-22). D2 is satisfied: monitoring is cited to §11's `PREVENTION_COMPLETE`, not
to §5.4; the successor reconciliation is named; the unchecked renewed-Gate-1 item is
retained. D6's carve-out keeps `"signed 2026-09-05"`.*

---

### Hunk 5 — the status header, dateless · **R** · replace BASE:6–12

**Span widened twice.** Plan v1 said 8–10 and its own text covered 8–12 (B1). PR-20's
accepted fix additionally requires neutralizing the `[planning record]` citation, which
sits on BASE:6–7 — so the span is **6–12**, the whole approval-state paragraph.

**FROM** (BASE:6–12):

```
*Approval state: Gate 0 and Operation A Plan v2 Gate 1 are signed; the dated
[planning record](../worktree_cleanup/PLANNING.md) records the approved implementation
and verified disposable interactive Windows acceptance. Gate 2 and the remaining
publication, installation and monitoring obligations remain open; PREVENTION_COMPLETE
is not declared. B, C, and D still require the operation-specific owner approvals
below and the independent Windows-filesystem review. E remains a separately planned
and approved operation. This factual status correction changes no technical contract.*
```

**TO**:

```
*Approval state: Gate 0 and Operation A Plan v2 Gate 1 are signed, and the approved
planning record records the approved implementation and verified disposable
interactive Windows acceptance. Operation A's reviewed guard and test source is
merged. What remains open for Operation A is stated as obligations: Section 5.4's
outstanding conditions, Section 11's requirement that lifecycle monitoring is active,
the outstanding post-merge required-check disposition, and the reconciliation of any
successor of the reviewed artifact against the reviewed bytes; PREVENTION_COMPLETE is
not declared. B, C, and D still require the operation-specific owner approvals below
and the independent Windows-filesystem review. E remains a separately planned and
approved operation, as do the Section 14 operations F and G, neither of which is
approved here. This factual status correction changes no technical contract.*
```

*What this removes: the stale open-publication assertion; the orphaned `"Gate 2"` name,
which occurs only here and in the local working copy's §12 box and is defined nowhere in
the file (§5.4 is "Gate A"); and the link to the path with two divergent lineages, which
resolves to the copy that does **not** carry the owner's 2026-09-05 Gate 1 sign-off.
No merge date, PR number, CI run identity, **or CI run outcome** is introduced.*

---

### Hunk 6 — `INDEX.md` · **R** · replace BASE-INDEX:61–65

**FROM**:

```
- [Worktree Cleanup and Preservation Plan](WORKTREE_CLEANUP_PLAN.md) — phase-gated,
  slice-based path-conversion prevention, malformed-root quarantine, whole-tree
  preservation, worktree retirement, and separately approved main reconciliation;
  planning only with Gate 0 signed and Gate 1 plus the Windows-filesystem review
  pending
```

**TO**:

```
- [Worktree Cleanup and Preservation Plan](WORKTREE_CLEANUP_PLAN.md) — phase-gated,
  slice-based path-conversion prevention, malformed-root quarantine, whole-tree
  preservation, worktree retirement, separately approved main reconciliation, and the
  routes that require their own separate approval for drive-root children outside
  Operations B and C; planning only. Gate 0 and Operation A Plan v2 Gate 1 are signed.
  Pending: the independent Windows-filesystem review, the renewed plan-level Gate 1
  that later semantic amendments require, and Operation A's remaining deployment,
  installation, acceptance, and monitoring obligations
```

*`"separately approved routes"` → `"routes that require their own separate approval"`
(AR-23/TS-13). Dateless. Introduces no `SHARED_PLAN`, `Tier <digit>`, or
`Appendix A<digit>` string (TS-5).*

---

## B. The carrier and the enumeration sweep

### B.0 Edit N — new `## 14.` section · **I** · append after BASE:1471

**Anchor** (BASE:1471, last line of file):
`  aware disposition without treating PR state as removal authority.`

**Placement.** Appended at end of file. Inserting between §9 and §10 would renumber
§10–§13 and break every in-file `Section 10`/`Section 11` reference — including §8.1's
*"Section 11's exact named outcome"* — plus every external reference. The cost is that
§14 follows §13's historical appendix. **Plan v1 claimed every reader path was
cross-referenced and AR-7 showed six were not; Plan v2 makes the claim true rather than
restating it**: S11, S13, S14, S17, S20, S22, S25, S29, S32 and S34 each carry an
explicit `Section 14` pointer, so §1.2, §1.3, §2.2, §4.1, §4.2, §4.3, §4.4, §4.5, §7.5,
§7.6, §8.3, §10, §11 and §12 all route a reader to the carrier. The `## 9A.` alternative
(reading order preserved, non-numeric label) remains available and is an owner-visible
choice.

**TO**:

```
## 14. Drive-root children outside Operations B and C

### 14.0 Scope, terminology, authority, and receipts

**The term.** Sections 8.3 and 11 use the noun unexpected drive-root child, and this
section uses it in exactly that sense: a drive root's child that the owner-approved
drive-root baseline does not list. Two adjacent terms elsewhere are deliberately left
unrenamed because their senses differ: Section 5.1's "unintended drive-root child" is a
causal description of how path conversion creates one, and Section 6's "other
unexpected root" is discriminated against the configured drive-root allowlist rather
than against the baseline. No second noun is minted here.

**The scope qualifier, defined once.** An unexpected drive-root child is outside
approved operation scope when, evaluated by exact canonical/final path and physical
identity rather than by name, prefix, proximity, or any alias form Section 2.2 rule 8
rejects, it is neither of Operation B's two named roots nor enumerated in an approved
operation source or target manifest. This is the only place the qualifier is defined.
The noun is fixed by the owner-approved baseline; only the qualifier depends on
manifest approval, and it is the qualifier - never the noun - that stops applying when
a manifest is approved, because no manifest approval edits that baseline. The term
"unapproved drive-root child" is deliberately not used: it would go false at the moment
of manifest approval while "unexpected" must stay true, splitting the Section 8.3 and
Section 11 checks from the Section 5.2 audit.

**No implicit authority over any unexpected drive-root child.** Proximity to a named
root, a generated-output classification, a filesystem creation time, a previous
campaign's completion receipt, and every existing aggregate, receipt, approval record,
manifest, and baseline entry in this plan confer no preservation, relocation,
quarantine, or removal authority over any unexpected drive-root child, whether or not
it is outside approved operation scope. Authority exists only where this plan names it
explicitly - Operation B for its two named roots - or under a dated Section 4.3 owner
approval record for an operation of this section, created separately from and after
this text. This section approves nothing, names no source and no target, and widens no
existing approval. Completing either operation of this section changes no
PREVENTION_COMPLETE declaration, permits no edit to the owner-approved drive-root
baseline, and permits no zero exit from the Section 5.2 audit.

**Prevention first.** Operations F and G each require PREVENTION_COMPLETE in addition
to their own approvals. Operation A is the prevention operation for the very defect
that creates unexpected drive-root children, and an operation freeze that ran before
prevention was complete could itself create one, which the Section 8.3 and Section 11
delta checks would then correctly fail. Beyond that precondition, F and G may be
commissioned at any point after the owner-accepted stabilization checkpoint and fresh
evidence, independently of whether B, C, or D has been approved or scheduled.

**Operation B is unchanged.** MALFORMED_ROOT_QUARANTINED(root) and
MALFORMED_ROOTS_QUARANTINED continue to mean exactly Operation B's two named roots and
nothing else; Section 4.3's binding of exactly one malformed-root identity to a B
approval is unchanged; and no Operation B receipt, approval record, or quarantine
destination may cover any other root. An Operation G approval is never an Operation B
approval, and an Operation G launcher may not emit an Operation B outcome name.

**Operation D is unchanged, and the structural seal is stated rather than relied on.**
A drive-root directory can never satisfy Section 3.6 condition 1, which requires a
registered immediate child of the approved development parent; it can therefore never
be an ELIGIBLE row, can never record a Section 3.5 positive lifecycle basis, and can
never enter a Section 3.7 immutable cleanup target set. No drive-root directory can
affect WORKTREE_SLICE_COMPLETE, WORKTREE_SLICE_PARTIAL_CLOSED,
TRIAGE_COMPLETE_NO_REMOVAL_AUTHORIZED, or WORKTREE_CLEANUP_COMPLETE, in either
direction.

**Receipts are private by default.** An Operation F or Operation G manifest, journal,
and receipt necessarily bind an exact canonical/final path, a physical identity, and,
for F, an off-machine storage object. Those are private under Section 2.2 rules 16 and
17. Publish only a privacy-reviewed redacted receipt; no public receipt names a
drive-root child's exact path, physical identity, or off-machine storage object.

### 14.1 Operation F - separately approved additional-source preservation

No Operation F preservation authority exists for any source until every one of the
conditions below is true. Operation F preserves an approved closed set of exactly
identified unexpected drive-root children that are outside approved operation scope
under Section 14.0. It is not a general route for arbitrary sources outside Operation
C's scope, and it is not an extension of Operation C's immutable source manifest: no
Operation C manifest, approval, receipt, freeze budget, or capacity approval is
altered, reused, or extended by it.

One Operation F operation binds one approved closed set. Its outcome is per source:
Section 11 defines ADDITIONAL_SOURCE_PRESERVED(source) and defines no aggregate over
the set, so no claim may be made over the set as a whole.

1. A Section 4.3 immutable, digest-bound manifest enumerates the exact, closed set of
   sources by canonical/final path and physical identity, and a dated Section 4.3
   owner approval record for that manifest exists, created separately from and after
   this plan text. Wildcard or prefix expansion, source-to-source overlap,
   source-to-destination overlap, overlap with Operation C's approved scope, overlap
   with a previously approved Operation F source, a missing source, and a changed
   identity are each a rejection, not a warning.
2. Every obligation of Section 7.5 applies to each source in the set, unchanged, with
   only these two scope-specific deviations: Section 7.5's opening inventory paragraph
   governs Operation C's pre-stop runtime map, and Operation F substitutes its own
   approved source set; and Section 7.5's live-capture freeze release governs
   Operation C's capture phase, and Operation F releases its own. Nothing else in
   Section 7.5 is narrowed - including raw SQLite-family capture before any open,
   completed online backups and logical checks on disposable copies only, preservation
   of every manifest-enumerated startup snapshot before any app or test launch,
   preservation of ignored/untracked/local settings, handovers/claims, evidence, loose
   files, recovery/salvage directories and unique local payload, separate exact
   no-follow archives for every ordinary private environment with reconstruction
   versions and health output recorded without installing or repairing anything, the
   separate recording of volatile cache and log paths, and the authenticated
   encryption, two independent offline custody copies, and off-machine
   upload/download/verify/decrypt/compare regime.
3. Section 7.2 items 4 and 5 apply to each source as obligations: a no-follow cold
   copy or archive of the complete approved source, including loose files, directories
   and reparse entries recorded as inert metadata; and live-source manifests generated
   immediately before and after capture, required identical, and compared directly
   with the extraction - archive-to-itself or upload-to-download equality alone is
   insufficient.
4. Section 7.6 applies to each source: the first decrypted extraction is immutable
   evidence, a second disposable copy with no hardlinks is sanitized before any Git
   invocation, extraction rejects traversal and absolute/device/ADS entries, and
   whole-tree source-to-restoration equality is proved in a fresh isolated root. Each
   source is proved separately against its own extraction root; no union or aggregate
   comparison substitutes for a per-source proof. This section's restore gate over the
   complete approved set is named Gate F.
5. Any Git repository inside a source carries Section 7.3's OID enumeration and
   type-checking and archive-ref obligations and Section 7.4's separate preservation
   and restore-test, or the source is not approvable under Operation F.
6. Section 7.1's runtime map and writer-shutdown set are extended to each source, or
   the absence of a writer is positively recorded for it. An unresolved writer or an
   unresolved root blocks Operation F for that source exactly as it blocks Operation
   C.
7. Every member class present in each source - SQLite family, nested repository,
   reparse point, alternate data stream, long path - has been enumerated and
   characterized before approval, and the absence of each unlisted class is positively
   recorded. An uncharacterized member class makes the source unapprovable.
8. The capacity requirement and the freeze budget are calculated for the complete
   approved set, not per source in isolation, and re-measured immediately before
   writing under Section 7.2 item 3's margin. The owner re-approves the maximum freeze
   duration for this Operation F operation. A maximum approved for Operation C, or for
   an earlier Operation F operation, never carries over.
9. The Section 4.5 recovery playbook for Operation F is approved and its scratch
   drills pass before the first preservation write, and the Section 4.2 non-LLM human
   and Windows-filesystem review has been performed against the actual mutation
   surface with fresh scratch proofs for every path form a drive-root source
   introduces.

**States and abort branches.** Operation F adopts Operation C's safe-abort model. Its
safe-abort boundary is the first preservation write: before it, a failed checkpoint or
projected overrun cleanly aborts under Section 7.2's abort paragraph, retaining and
labelling partial outputs INVALID_INCOMPLETE, restoring maintenance, recording
ABORTED_NO_MUTATION, and closing out under Section 4.4. After it, the operation
finishes the minimum manifest-enumerated capture and clean closeout or enters
BLOCKED_RECOVERY under its pre-drilled Section 4.5 playbook. Operation F creates no
archive ref and no live Git metadata in the live repository.

**Closeout.** An Operation F closeout runs the complete Section 4.4 single-hold
clean-closeout protocol and, in addition, the Section 14.3 drive-root delta
comparison: a no-follow explicit-stack enumeration of the configured drive roots of
Section 5.2, compared against the owner-approved baseline union the Section 14.3
register as frozen at this operation's start, failing on any child newly created
during the operation.

**Failure isolation.** A defect, overrun, or unresolved identity on an Operation F
source aborts or blocks only that Operation F operation, under its own safe-abort
boundary and its own recovery playbook. It never aborts, blocks, delays, or alters
Operation C's D:\development capture; Section 7.2's abort branches govern Operation C
on its own scope. PRESERVATION_COMPLETE is unchanged by this section: it remains
Operation C's outcome, computed from Operation C's gates over Operation C's approved
scope only, so a pre-amendment and a post-amendment Operation C receipt remain
directly comparable. An Operation F failure does not block Operation D or Operation E;
it blocks only Operation G, and only for the source identities it failed to preserve.

### 14.2 Operation G - separately approved drive-root child retirement

Operation G is built on Operation B's per-root template: archive, then a single
ordered non-overwriting move of one exact root to a nonexistent operation-specific
same-volume quarantine destination. It never uses recursive deletion, never
copy-deletes, and never uses Operation D's worktree-removal transaction core.
Permanent deletion of a quarantine payload remains Section 11's separate later
operation.

Operation G adopts Section 6's forward states and terminal branches unchanged -
NOT_STARTED, PREFLIGHTED, AUTHORIZED, QUARANTINE_MOVE_INTENT, MOVE_RESULT,
QUARANTINED, VERIFIED, with ABORTED_NO_MUTATION and FAILED_NEEDS_RECOVERY on the same
branches and the same QUARANTINE_MOVE_INTENT boundary - reading "root" as the
Operation G root. It derives its own aggregate per root and never derives an Operation
B aggregate.

No Operation G retirement authority exists for a root until every one of the following
is true for that exact identity:

1. ADDITIONAL_SOURCE_PRESERVED(source) is proved for an Operation F source whose exact
   canonical/final path and physical identity are the same identity as this Operation
   G root. That equality is required; resemblance, adjacency, and a matching name are
   not sufficient.
2. Recovery has been proved with the stored secret for that exact source before the
   move - the proof Section 7.5 requires before a B quarantine move, a D removal, or
   an Operation G retirement move - by downloading the encrypted object into a fresh
   root off this machine, verifying ciphertext hashes, decrypting, extracting, and
   comparing exact member and hash sets.
3. An exact immutable, digest-bound, positive, non-empty target manifest names that
   one root and its single nonexistent same-volume quarantine destination.
4. Section 4.2's non-LLM human and Windows-filesystem review has been performed
   against that actual mutation surface, with fresh scratch proofs for every path form
   a drive-root source or quarantine destination introduces. A prior review of another
   operation's mutation surface does not satisfy it.
5. Section 4.3 manifest and production-package digest integrity are verified and the
   owner's approval is recorded in a durable approval record outside every source and
   candidate.
6. A Section 4.4 journal is kept, and the shared Section 4.4 coordination lock and
   shared attempt register are used on the same single-hold protocol as every other
   live launcher.
7. The Section 4.5 recovery playbook for Operation G is approved and its scratch
   drills pass before the first live mutation.
8. A retention start and a per-object retention period are stated, and Section 11's
   named retention-exit checks apply to the resulting quarantine payload.

Operation G uses its own thin root-quarantine launcher built from the same reviewed
template as Section 4.1 item 2, bound to its own approved single-root manifest, its
own journal, and Operation G's own outcome name. It is not Operation B's launcher and
cannot emit an Operation B outcome. A failure for one Operation G root does not
invalidate another root's completed operation, and no Operation G attempt overwrites a
prior attempt's evidence.

**Closeout.** An Operation G closeout runs the complete Section 4.4 single-hold
clean-closeout protocol, the final root receipt, and, in addition, the Section 14.3
drive-root delta comparison described for Operation F above. Because a completed
Operation G changes the drive-root enumeration, that comparison also reports the
retired root as absent at its recorded identity, and the owner dispositions its
Section 14.3 register entry at that closeout.

### 14.3 The owner-dispositioned known-unexpected register

The register is a durable owner record of unexpected drive-root children that are
already known and dispositioned as retained. It is an owner-approved artifact: each
version carries a SHA-256 digest, lives in an evidence root meeting Section 3.1's
conditions, and is bound by digest into the Section 4.3 approval of every operation
that will consume it and again into that operation's closeout receipt.

**What it changes.** Section 8.3's closeout check is "confirm no unexpected drive-root
child was created" - a delta over the operation window, not a census. The register
pins, by exact canonical/final path and physical identity, the set of unexpected
drive-root children already recorded before an operation began. A closeout therefore
compares a no-follow explicit-stack enumeration of the configured drive roots of
Section 5.2 against the owner-approved baseline union the register as frozen at that
operation's start, and fails on a child newly created during the operation. A
pre-existing registered child is not a closeout failure. A newly created child is a
closeout failure whether or not it resembles a registered entry. This comparison is
performed at every Operation B, C, D, F and G closeout: Section 8.3 states it for a D
slice, Sections 14.1 and 14.2 state it for F and G, and Section 11's post-operation
observation states it for every operation and slice. The register also gives Section
11's requirement that unexpected drive-root children "remain consistent with their
closeout manifest" a determinate meaning for a child that belongs to no operation's
manifest: each registered entry must be unchanged at its recorded identity at that
closeout.

**What it does not change.** The register does not clear, suppress, alter, or
reinterpret the Section 5.2 read-only drive-root audit, which continues to compare
configured drive roots against the owner-approved baseline and to report every
unexpected child. That audit's non-zero exit is unchanged and expected. A registered
entry is neither a reason to suppress that report nor a reason to ignore it. A
register entry is not a baseline entry: it is not added to the baseline, and it alters
none of the baseline's bytes, approver, approval timestamp, or RESOLVED meanings. It
is not a source-manifest entry and not a target-manifest entry. It confers no
preservation, relocation, quarantine, or removal authority, and it is not a
disposition any operation may act on. Section 6's post-operation observation of the
configured drive-root allowlist is likewise unaffected: detection is never suppressed.

**Its own integrity.** Each entry carries an exact canonical/final path and physical
identity, the owner's disposition, and the fact that the child is retained. An entry
is added, amended, or removed only by owner decision - never by an executor, an audit
run, a closeout, or an agent. The register is frozen for the duration of an operation,
from that operation's start through its closeout; the frozen version's digest is
recorded in that operation's Section 4.3 approval and again in its closeout receipt,
so the delta above is computable and an after-the-fact addition is detectable. When a
completed Operation G retires a registered child, the owner dispositions that entry at
that operation's closeout; until the owner does so, the entry stands and its recorded
identity is expected absent.
```

---

### B.1 The sweep — 34 edits, each as a `FROM` / `TO` pair

Every quantifier site found by grepping `B-E`, `B–E`, `B-D`, `A-D`, `B, C, or D`,
`B, C, and D`, `B/C/D`, `B/C/D/E`, `C/D`, `D and E`, `Operation [A-E]`, `the relevant
operation`, `each operation`, `every operation`, and — added after AR-15/PR-12 — the
literal operation **count** in headings.

**S1 · I · insert after BASE:63** — §1.2 rollout order
FROM-anchor: `      -> consider E only under its separate plan and approval`
TO (blank line, then **non-indented prose outside the attributed block**, PR-6):
```

Operations F and G, added by a later amendment under Section 1.1, are considered only
under their own separate plans and approvals (Section 14). The Gate 0 requirements
above neither order nor authorize them.
```

**S2 · R · replace BASE:65**
FROM: `No technical independence below permits B-E to bypass that sequence. During the`
TO: `No technical independence below permits B-G to bypass that sequence. During the`

**S3 · I · insert after BASE:83** — §1.2 dependency graph
FROM-anchor: `          +--> E. Main reconciliation under a separate approval`
TO:
```
    |
    +--> F. Separately approved additional-source preservation (Section 14.1)
          |
          +--> G. Separately approved drive-root child retirement (Section 14.2)
```

**S4 · R · replace BASE:85–86**
FROM:
```
The shared Windows-filesystem proof in Section 4 is required before B, C, or D uses
its filesystem mutation/copy primitives.
```
TO:
```
The shared Windows-filesystem proof in Section 4 is required before B, C, D, F, or G
uses its filesystem mutation/copy primitives.
```

**S5 · R · replace BASE:108** — range form restored (AR-20)
FROM: `The first Gate 1 implementation decision is for Operation A only. Sections B-E retain`
TO: `The first Gate 1 implementation decision is for Operation A only. Sections B-G retain`

**S6 · R · replace BASE:170** — §2.2 rule 2; range widened so E's rename exception later in the same rule is untouched
FROM: `2. During A-D, never run a mutating worktree prune, manually delete .git/worktrees`
TO:
```
2. During A-D, F, and G, never run a mutating worktree prune, manually delete
   .git/worktrees
```

**S7 · R · replace BASE:177–178** — §2.2 rule 3, partial enrolment with a stated reason
FROM:
```
3. Disable automatic Git maintenance for every cleanup Git child. During each C/D
   live freeze, and any future E live-mutation window, suspend scheduled/background
```
TO:
```
3. Disable automatic Git maintenance for every cleanup Git child. During each C/D
   live freeze, any Operation F live freeze whose approved source contains a live Git
   repository (Section 14), and any future E live-mutation window, suspend
   scheduled/background
```
*Operation G is deliberately excluded, matching Operation B: a same-volume quarantine
move of a directory outside the repository requires no Git-maintenance suspension.*

**S8 · R · replace BASE:194** — §2.2 rule 6
FROM: `6. For every B-E preservation/cleanup command that invokes Git against live or`
TO: `6. For every B-G preservation/cleanup command that invokes Git against live or`

**S9 · R · replace BASE:251–252** — §2.2 rule 20 retention clock, enrolled by name
FROM:
```
20. Retain every preservation object and quarantine payload for at least 30 days
    after the relevant operation and a successful normal-development observation.
```
TO:
```
20. Retain every preservation object and quarantine payload for at least 30 days
    after the relevant operation, including each Operation F source capture and each
    Operation G quarantine payload (Section 14), and a successful
    normal-development observation.
```

**S10 · R · replace BASE:453** — §4.1 staging item 1
FROM: `1. Before B or C, approve an early shared package containing the no-follow`
TO: `1. Before B, C, or F, approve an early shared package containing the no-follow`

**S11 · I · insert after BASE:463** — §4.1 new staging item 5, time-gated and anti-speculative (PR-18)
FROM-anchor: `   removal surface speculatively.`
TO:
```
5. Operation F (Section 14.1) uses the same established copy/archive/encryption tools
   through the same reviewed wrappers as C and requires no new mutation primitive.
   Only after an approved Operation G target manifest exists for one exact root, add
   the thin root-quarantine launcher for Operation G (Section 14.2), built from the
   same reviewed template as item 2 but bound to its own manifest, journal and outcome
   name. Do not build that mutation surface speculatively. Neither F nor G may use D's
   worktree-removal transaction core.
```

**S12 · R · replace BASE:475–476** — §4.1 launcher cardinality (full-line; AR-3, B5)
FROM:
```
approved immutable manifest and verifies its recorded digest. B handles exactly one
root, C one live capture phase, and E one live maintenance window. One D launcher
```
TO:
```
approved immutable manifest and verifies its recorded digest. B handles exactly one
root, C one live capture phase, F one approved closed source set, G exactly one root,
and E one live maintenance window. One D launcher
```

**S13 · I · insert after BASE:502** — §4.2 reciprocal (D4)
FROM-anchor: `an adversarial race-proof sandbox.`
TO:
```
This review is required for an Operation F source capture and an Operation G root move
exactly as it is for B, C, and D (Section 14), and it must add fresh scratch proofs
for every path form a drive-root source or quarantine destination introduces. A prior
review of a different operation's mutation surface never satisfies it.
```

**S14 · R · replace BASE:506** — §4.3 opener (D4)
FROM: `Each B root operation, C preservation run, D slice, and future E operation uses an`
TO:
```
Each B root operation, C preservation run, D slice, future E operation, Operation F
source capture, and Operation G root operation (Section 14) uses an
```

**S15 · R · replace BASE:515** — §4.3 common approval fields
FROM: `Every B root-operation and D slice approval binds these common fields:`
TO:
```
Every B root-operation, D slice, Operation F source-capture, and Operation G
root-operation approval binds these common fields:
```

**S33 · R · replace BASE:524–525** — register digest bound into the **common** fields (AR-14)
FROM:
```
- expected pre/post Git and filesystem state; and
- owner, date, and retention deadline.
```
TO:
```
- expected pre/post Git and filesystem state;
- the SHA-256 digest of the Section 14.3 known-unexpected register as frozen at this
  operation's start, recorded again in the operation's closeout receipt; and
- owner, date, and retention deadline.
```

**S16 · I · insert after BASE:531** — §4.3 operation-specific bindings
FROM-anchor: `operation are absent, never populated with dummy values.`
TO:
```
An Operation F approval additionally binds the exact closed set of source identities,
each source's extraction root, the destination identity, the freeze budget with the
owner-approved maximum freeze duration approved for that Operation F operation, its
safe-abort boundary, and its expected capture and restore results. An Operation G
approval additionally binds exactly one drive-root child identity, one nonexistent
same-volume quarantine destination, its single ordered move, the
ADDITIONAL_SOURCE_PRESERVED(source) evidence for that exact identity, and its
retention start and per-object retention period. An Operation G approval is never an
Operation B approval, and no Operation B approval may bind an Operation G root.
```

**S17 · R · replace BASE:551** — §4.4 shared lock, mandatory (D4)
FROM: `All B-E live launchers use one fixed owner-approved coordination-file path`
TO:
```
All B-G live launchers, including the Section 14 operations F and G, use one fixed
owner-approved coordination-file path
```

**S18 · R · replace BASE:560** — §4.4 attempt register, mandatory
FROM: `B-E live attempt and closeout. Every read, append, and flush occurs while holding the`
TO: `B-G live attempt and closeout. Every read, append, and flush occurs while holding the`

**S19 · I · insert after BASE:597** — §4.4 restore-gate poisoning rule
FROM-anchor: `closeout blocks D and E through Gate C; it does not falsely poison B's live lock.`
TO:
```
An offline Operation F restore failure at Gate F, after that operation's verified live
capture closeout, blocks only Operation G and only for the source identities it failed
to preserve; it does not poison B's, C's, or another Operation F operation's live
lock.
```

**S20 · R · replace BASE:613–614** — §4.5 trigger list (D4)
FROM:
```
Before the first live mutation in B, the first preservation write or ref creation in
C, the first removal slice in D, or any future E mutation, approve the common recovery
```
TO:
```
Before the first live mutation in B, the first preservation write or ref creation in
C, the first removal slice in D, the first preservation write in an Operation F source
capture, the first live mutation in an Operation G root operation (Section 14), or any
future E mutation, approve the common recovery
```

**S21 · R · replace BASE:661** — §4.5 gate-matrix row
FROM: `| B/C/D/E operation with no source change | Manifest, restore, and receipt gates only; no invented browser gate |`
TO: `| B/C/D/E/F/G operation with no source change | Manifest, restore, and receipt gates only; no invented browser gate |`

**S32 · R · replace BASE:998–999** — §7.5's "Preserve …" bullet (AR-18/PR-9)
FROM:
```
- Preserve ignored/untracked/local settings, handovers/claims, evidence, loose files,
  recovery/salvage directories, and unique local payload.
```
TO:
```
- Preserve, within C's approved immutable source manifest, ignored/untracked/local
  settings, handovers/claims, evidence, loose files, recovery/salvage directories, and
  unique local payload. This bullet adds nothing to that manifest, and a drive-root
  directory outside C's approved source scope is recorded and retained only, per the
  discovery paragraph above and Section 14.
```

**S22 · R · replace BASE:1015–1016** — §7.5 pre-removal approval set
FROM:
```
Use an established authenticated-encryption tool; do not invent crypto. Before a B
quarantine move or D removal, the owner must approve:
```
TO:
```
Use an established authenticated-encryption tool; do not invent crypto. Before a B
quarantine move, a D removal, or an Operation G retirement move (Section 14), the
owner must approve:
```

**S23 · R · replace BASE:1028–1029** — §7.5 recovery proof
FROM:
```
exact member/hash sets. Prove recovery with the stored secret before any removal and
again at retention exit.
```
TO:
```
exact member/hash sets. Prove recovery with the stored secret before any removal and
before any Operation G retirement move, and again at retention exit.
```

**S24 · I · insert after BASE:1068** — §7.6, `PRESERVATION_COMPLETE` sealed (B6/PR-2, reviewer's exact wording)
FROM-anchor: `encryption/upload/download/restore gate above passes. Anything less blocks D and E.`
TO:
```
Operation F is outside PRESERVATION_COMPLETE. Operation F still performs every Section
7.6 restore verification for its own sources, under Operation F's own gate; no
Operation F source, receipt, or failure contributes to or blocks
PRESERVATION_COMPLETE, and no Operation C receipt covers an Operation F source, so
PRESERVATION_COMPLETE keeps exactly the meaning it had before Section 14 existed and
pre-amendment and post-amendment C receipts remain comparable.
```

**S25 · R · replace BASE:1240** — §8.3 closeout check (criterion 13; AR-22)
FROM: `- confirm no unexpected drive-root child was created;`
TO:
```
- confirm that no unexpected drive-root child was created during the operation, by
  comparing a no-follow explicit-stack enumeration of the configured drive roots
  (Section 5.2) against the owner-approved baseline union the Section 14.3
  known-unexpected register as frozen at this operation's start; a pre-existing
  registered child is not a failure and a newly created child is, whether or not it
  resembles a registered entry;
```

**S26 · R · replace BASE:1330** — §10 maintenance window (full-line; AR-3)
FROM: `failure occurred while a C/D freeze or E live-mutation window was active and`
TO:
```
failure occurred while a C/D freeze, an Operation F live freeze, or an E
live-mutation window was active and
```

**S27 · I · insert after BASE:1336** — §10 return point
FROM-anchor: `cannot waive its failed gate.`
TO:
```
These rules apply unchanged to Operation F and Operation G (Section 14). An Operation
F or Operation G failure returns only to that operation's own earliest affected source
or root; it neither reopens nor waives a completed B, C, or D result, and no later F
or G success waives a failed gate of any operation.
```

**S28 · R · replace BASE:1374–1379** — §11 post-operation observation (full-paragraph; AR-3, and the universal delta trigger for AR-21/PR-17)
FROM:
```
After each operation/slice, perform a normal guarded development observation
appropriate to its scope. Database bytes may legitimately change during normal app
use; capture a new closeout family and inspect only disposable copies rather than
claiming it still equals the pre-resume snapshot. Protected environment members,
Git/ref relationships, guard installation, quarantines, and unexpected drive-root
children must remain consistent with their closeout manifest.
```
TO:
```
After each operation/slice, perform a normal guarded development observation
appropriate to its scope. Database bytes may legitimately change during normal app
use; capture a new closeout family and inspect only disposable copies rather than
claiming it still equals the pre-resume snapshot. Protected environment members,
Git/ref relationships, guard installation, quarantines, and unexpected drive-root
children must remain consistent with their closeout manifest. For an unexpected
drive-root child that belongs to no operation's manifest, that requirement is met when
its Section 14.3 register entry is unchanged at its recorded identity at closeout.
Every operation and slice also performs the Section 14.3 delta comparison: a no-follow
explicit-stack enumeration of the configured drive roots (Section 5.2) against the
owner-approved baseline union the Section 14.3 register as frozen at that operation's
start, failing on any child newly created during the operation.
```

**S31 · R · replace BASE:1397–1398** — §12 shared-lock item (AR-8/PR-11)
FROM:
```
- [ ] Select the single shared B-E coordination lock/register root and verify its
      canonical path, non-reparse parent, and access boundary.
```
TO:
```
- [ ] Select the single shared B-G coordination lock/register root and verify its
      canonical path, non-reparse parent, and access boundary.
```

**S29 · I · insert after BASE:1412** — §12 new decision items plus the relocated status sentence (PR-22)
FROM-anchor: `- [ ] Decide whether and when to commission the separate E main-reconciliation plan.`
TO:
```
- [ ] Decide whether to commission an Operation F additional-source preservation
      (Section 14.1) for an exact, closed set of unexpected drive-root children
      outside approved operation scope, and approve its Section 4.3 manifest, capacity
      requirement, freeze budget, and Operation-F-specific maximum freeze duration. No
      source is proposed or approved by this plan.
- [ ] Decide separately and later whether to commission an Operation G retirement
      (Section 14.2) for any such child whose ADDITIONAL_SOURCE_PRESERVED(source) is
      already proved, and approve its Section 4.3 target manifest, retention start,
      and per-object retention period. No root is proposed or approved by this plan.
- [ ] Maintain the Section 14.3 known-unexpected register. Each entry is recorded,
      amended, or removed by owner decision only, and the register is frozen for the
      duration of each operation.

Operation A's reviewed guard and test source is merged. Section 5.4's merge condition
is a conjunction: it additionally requires that Operation A implement the approved
subplan and pass every Section 4.5 implementation gate.
```

**S30 · R · replace BASE:50** — §1.2 heading, count removed (AR-15/PR-12)
FROM: `### 1.2 Five independently completable operations`
TO: `### 1.2 Independently completable operations`

**S34 · I · insert after BASE:106** — §1.3, each amendment's own gate record (AR-17)
FROM-anchor: `product-risk-reviewer.`
TO:
```
Each later semantic amendment to this design records its own Gate 0 and Gate 1 in its
own council artifact rather than in the artifact named above, which is the Operation A
council artifact. The amendment that added Section 14 records its gates in
docs/worktree_cleanup_amendment/PLANNING.md.
```

---

### B.2 Sites judged inapplicable — each with a written reason

| Site | Exact base text (line) | Reason no edit is proposed |
|---|---|---|
| §5.2 drive-root audit bullet | `- add a read-only drive-root audit that compares configured drive roots with an` (735) | **Inapplicable by owner decision.** Gate 0 answer 3: the register "does not clear the Section 5.2 audit or make it exit zero". Editing §5.2 is the change criterion 13 forbids. §14.3 states the non-effect instead |
| §6 post-operation observation | `both original paths and the configured drive-root allowlist so a future D:\tmp,` (874) | **Inapplicable.** A detection requirement, and the register suppresses no detection. §14.3 says so explicitly, so the non-enrolment is recorded rather than silent. §6's noun is also left unrenamed — see §14.0 |
| §5.1 root-cause conjunction | `3. Windows resolved that path from the current drive, creating an unintended` (691) | **Inapplicable, deliberately.** §5.1's *"unintended"* is discriminated by **cause of creation**. Renaming it to the baseline-discriminated noun would falsify a root-cause statement (PR-7). §14.0 records the distinction |
| §3.4 / §3.6 / §3.7 worktree row model | `1. It is a registered immediate child of the approved development parent and is not` (402) | **Inapplicable by construction, and the seal is stated.** A drive-root directory can never be a registered immediate child, so it can never be a row. Criterion 5's seal is stated in §14.0 rather than by editing §3.6, so no §3 predicate changes |
| §8.1 / §8.2 Operation D contracts | `- ends with the full Section 8.3 closeout and explicit development resume.` (1099) | **Inapplicable.** These govern worktree candidate rows only, sealed off by §3.6 condition 1 |
| §9 Operation E prerequisites | `The divergent-main repair is not a prerequisite for B, C, or D and is not included` (1261) | **Inapplicable.** The sentence asserts what E is *not* a prerequisite for; §1.2's amended graph already carries F's and G's independence. Restating it here would create a second drift surface |
| §4.4 evidence-root quantifier | `outside every operation evidence root, source, and candidate. Its parent must be an` (552) | **Inapplicable — already universal.** *"Every operation evidence root"* covers F and G with no edit (AR-15) |
| §2.2 rules 8, 9, 13, 14, 16, 17, 18, 19 | e.g. `14. Once an operation's live-runtime preservation freeze begins, preserve every` (227) | **Inapplicable — already universal.** Each quantifies over *"an operation"*, *"every mutation"*, or *"every cleanup command"* and covers F and G unchanged. Rule 14's *"Never call create_startup_backup during preservation"* in particular binds F without edit |
| §13.1 / §13.2 review dispositions | `- using one shared B-E coordination lock/register that remains blocked after any` (1432); `  independence of B, C, D, and E;` (1453); `- gives C and D measured, owner-approved maximum freeze budgets and explicit safe-` (1465) | **Inapplicable — historical record.** §13 records what the third and fourth review passes did. Enrolling F and G would falsify a record of reviews that never saw them |
| Status header | `is not declared. B, C, and D still require the operation-specific owner approvals` (10) | **Enrolled inside Hunk 5**, which rewrites the whole paragraph. Listed so the sweep is complete rather than appearing to have missed it |
| §11 post-operation observation | `After each operation/slice, perform a normal guarded development observation` (1374) | **Enrolled by S28**, which replaces the paragraph this line opens. Listed because AR-15 correctly noted it was neither enrolled nor recorded in Plan v1 |

---

### B.3 The authoritative edit list — 41 plan-file edits + 1 `INDEX.md` edit

**This is the single authoritative list. Its length is 42. No other number in this plan
counts edits.** Application is strictly descending by the highest line of each span.
**R** = line replacement, **I** = insertion after the anchor.

`docs/ai_workflow/INDEX.md` — applied independently of everything below:

| # | Edit | Span | Kind |
|---|---|---|---|
| — | Hunk 6 | 61–65 | R |

`docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`, in this exact order:

| # | Edit | Anchor / span | Kind |
|---|---|---|---|
| 1 | Edit N | after 1471 | I |
| 2 | S29 | after 1412 | I |
| 3 | S31 | 1397–1398 | R |
| 4 | Hunk 4 | 1389 | R |
| 5 | Hunk 3b | after 1384 | I |
| 6 | S28 | 1374–1379 | R |
| 7 | Hunk 3a | after 1372 | I |
| 8 | S27 | after 1336 | I |
| 9 | S26 | 1330 | R |
| 10 | S25 | 1240 | R |
| 11 | S24 | after 1068 | I |
| 12 | S23 | 1028–1029 | R |
| 13 | S22 | 1015–1016 | R |
| 14 | S32 | 998–999 | R |
| 15 | Hunk 2 | 990–992 | R |
| 16 | S21 | 661 | R |
| 17 | S20 | 613–614 | R |
| 18 | S19 | after 597 | I |
| 19 | S18 | 560 | R |
| 20 | S17 | 551 | R |
| 21 | S16 | after 531 | I |
| 22 | S33 | 524–525 | R |
| 23 | S15 | 515 | R |
| 24 | S14 | 506 | R |
| 25 | S13 | after 502 | I |
| 26 | S12 | 475–476 | R |
| 27 | S11 | after 463 | I |
| 28 | S10 | 453 | R |
| 29 | S9 | 251–252 | R |
| 30 | S8 | 194 | R |
| 31 | S7 | 177–178 | R |
| 32 | S6 | 170 | R |
| 33 | S5 | 108 | R |
| 34 | S34 | after 106 | I |
| 35 | Hunk 1 | after 95 | I |
| 36 | S4 | 85–86 | R |
| 37 | S3 | after 83 | I |
| 38 | S2 | 65 | R |
| 39 | S1 | after 63 | I |
| 40 | S30 | 50 | R |
| 41 | Hunk 5 | 6–12 | R |

**Totals: 27 replacements, 14 insertions, 41 plan-file edits; plus 1 `INDEX.md`
replacement = 42.** Highest-line sequence, strictly decreasing: 1471, 1412, 1397, 1389,
1384, 1379, 1372, 1336, 1330, 1240, 1068, 1029, 1016, 999, 992, 661, 614, 597, 560, 551,
531, 525, 515, 506, 502, 476, 463, 453, 252, 194, 178, 170, 108, 106, 95, 86, 83, 65, 63,
50, 12.

---

## C. Apply-time verification protocol

*Added in full from TS-9 and TS-12. None of these checks has been run, because running
them requires applying edits, which Gate 1 has not authorized.*

**C.1 Precondition, before the first edit.** Assert
`git hash-object docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` ==
`1b41922e795e9202f128a9b1122d0ffb6c6134af` and
`git hash-object docs/ai_workflow/INDEX.md` ==
`027af297b1658f70f353dd298c545fa4108c6def`. A mismatch means the working copy is not the
`origin/main` base — stop. This converts D5's prose prohibition on editing this
checkout's copies into a mechanical gate.

**C.2 Per-edit post-condition.** After each edit: for a replacement, the `FROM` text no
longer appears anywhere in the file and the `TO` text appears **exactly once**; for an
insertion, the anchor line still appears exactly once and the `TO` text appears exactly
once immediately after it.

**C.3 Completeness.** Before the first edit, compute the expected final line count as
`1471 − Σ(replaced lines) + Σ(replacement lines) + Σ(inserted lines)` from B.1, record
it, and assert it after the last edit. **This plan states no numeral for it**, because
the drafter cannot verify one without applying the edits, and an unverified numeral in a
completeness check is worse than none. The executor computes and records it.

**C.4 Criterion-10 closure re-grep, against the amended file.** Re-grep for `B-E`,
`B–E`, `B-D`, `A-D`, `B, C, or D`, `B, C, and D`, `B/C/D`, `B/C/D/E`, `C/D`, `D and E`,
and assert every surviving hit is on B.2's recorded-inapplicable list — §13.1, §13.2,
§9's E-prerequisite sentence, §2.2 rule 3's retained `C/D` and `A-D`-adjacent forms, and
§10's retained `C/D`. Any hit not on that list is an unenrolled quantifier and a
blocker. **This is the check that makes criterion 10's universal half demonstrable**;
Plan v1 could only concede the sweep was thorough but not proven exhaustive.

**C.5 Forbidden-string constraint.** No added line in either file may contain
`SHARED_PLAN`, `Tier <digit>`, or `Appendix A<digit>`. `INDEX.md` is permitted exactly
one `SHARED_PLAN` mention, which already exists in its anti-recreation note and is
outside Hunk 6's span; `WORKTREE_CLEANUP_PLAN.md` is exempt from the tier-numbering check
by the `*_PLAN.md` filter but not from the `SHARED_PLAN` one. Every block in this plan was
read against all three; none introduces any of them.

**C.6 Targeted pytest, in the standalone clone.**
`.venv/Scripts/python.exe -m pytest tests/test_agent_workflow_contracts.py -q`. This is
the only automated oracle in the repository that reads these two files' **prose**.

**C.7 `--check`, in the standalone clone.** `scripts/generate_test_inventory.py --check`
requires `npm ci` and an active venv in that clone: `_npx()` raises `SystemExit` without
`npx`, and the pytest collector shells `sys.executable -m pytest`. **A `SystemExit` from
any collector is a tooling failure to resolve, never a green and never "proved drift".**
Regenerate only after the check proves real drift; never hand-edit the inventory.

---

## D. Artifacts, effort, sequence, gates

### Artifacts

| Path | Change | Notes |
|---|---|---|
| `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` | modify (in-place, tracked) | Hunks 1–5, edit N, S1–S34. Base blob `1b41922e795e9202f128a9b1122d0ffb6c6134af` |
| `docs/ai_workflow/INDEX.md` | modify (in-place, tracked) | Hunk 6 only. Base blob `027af297b1658f70f353dd298c545fa4108c6def` |
| `docs/worktree_cleanup_amendment/PLANNING.md` | modify | This council artifact |
| `docs/worktree_cleanup/evidence/2026-09-28-state.md` | **unchanged — and untracked on `origin/main`** | See section E item 5. This is the designated home for every dated fact criteria 14/16/17 remove from the design, and it does not exist for a reader of `origin/main` |
| `docs/worktree_cleanup/PLANNING.md` | **not touched** | Both divergent lineages. Not created, read-modify-written, overwritten, staged, or committed |
| `docs/test_inventory/**` | **not touched** | Neither regenerated nor hand-edited from this checkout |

No `.py`, `.ts`, `.js`, `.scss`, `.html`, test, or configuration file is touched.

**Effort**: **L** · **Owner**: `product-manager` drafts; the owner alone applies and
approves · **Depends on**: Gate 0 (signed 2026-09-28); Gate 1 (unsigned)

### Sequence

1. **Owner reads section E** and settles the five items that are choices rather than
   mechanical repairs.
2. **Owner's Gate 1 decision.** No hunk is applied to the technical design as approved
   text at any point before it.
3. *(After Gate 1 only)* The owner prepares a branch from `origin/main` **in the
   owner-created standalone clone §1.3 already requires** — never from this dirty
   checkout, and never as a new file (D5). §1.3's four preconditions apply in full: the
   standalone clone rather than a linked worktree; TEMP, TMP, `HT_RUNTIME_DIR`,
   `DB_FILE`, caches and bytecode redirected to scratch; `--check` run **there**; and
   proof that the checkout has no alternates or hardlinks to the live object store.
4. *(After Gate 1 only)* Apply the 42 edits under section C's protocol, bottom-up.
5. *(After Gate 1 only)* Renewed Gate 1 under §1.1 for this semantic change — the item
   Hunk 4 keeps as an unchecked box alongside the retained original.

### Expected gates

- **pytest**: `tests/test_agent_workflow_contracts.py`, targeted, in the standalone
  clone (TS-5). Plan v1 said "none required"; that is defensible under the change-type
  row but leaves the only oracle that reads these files' bytes unrun.
- **Checkout-local red (TS-6)**: a pytest run from *this* checkout is **expected red** on
  `test_every_surface_file_is_tracked_by_git`, because the untracked
  `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` enters `SURFACE`. **That red belongs to the
  checkout, not the amendment; it is not repaired by regenerating the inventory; it is
  not a gate result; and it is not a documented known exception.** On a branch cut from
  `origin/main` the file is tracked and the test passes.
- **e2e**: none. No template, route, static asset, `scss/**`, or `e2e/**` path in scope.
- **`Test Inventory Drift`**: **not tripped.** Mechanism (TS-7): the generator has **no**
  configuration-surface collector — its four collectors are Playwright, pytest, Vitest
  and hard-waits. The `docs/ai_workflow/` sensitivity arrives entirely through
  `tests/test_agent_workflow_contracts.py`'s parametrized `SURFACE`, whose node count is
  a committed `pytest.files[]` row. **Adding or deleting a file there moves that count;
  an in-place edit moves nothing.** This council artifact's own directory is outside every
  globbed surface. A green here pins **counts only** — C.5 and C.6 are what read content.
- **`Type Check (tsc blocking + pyright measure-only)`** (TS-8): **both steps
  inapplicable** — no `.py` and no `.ts` in the diff.
- **Change-type row**: AI workflow / agent config (`docs/ai_workflow/**`) — manual
  dry-run and self-review; `code-reviewer` or careful self-review; run tests only if
  source behavior changed. **Routing confirmed against the `origin/main`
  `QUALITY_GATE.md` blob**, whose routing and change-type tables are byte-identical to
  the working-tree copy the `test-strategist` read (TS-14, closed).
- **This council artifact itself**: Product docs only — no required tests or reviewers.
- **Escalation trigger, restated (TS-11)**: the gates are re-derived **if any hunk changes
  a file outside `docs/ai_workflow/**`** — the condition the change-type table keys on.
  Plan v1's *"implies a tooling, launcher, or script change"* was unevaluable. Recorded
  separately: **Operation G's launcher is future work behind its own approval, with its
  own change-type derivation at that time**; nothing in these 42 edits writes it.
- **Gates this packet does not satisfy and does not claim**: Gate 1 (unsigned), the
  independent Windows-filesystem review, and every operation-specific owner approval.

### Evidence gaps

1. **Operation A deployment state is unmeasured.** Hunks 4 and 5 record obligations, not
   measurements.
2. **The successor guard on `origin/main` is unverified here.** Whether it preserves the
   reviewed Operation A behavior was not assessed; Hunk 4 records the reconciliation as
   an obligation and makes no claim about its outcome.
3. **No member class of any candidate source is characterized, and §7.1's runtime map
   does not exist.** §14.1 requirements 6 and 7 make both preconditions of approvability
   rather than assumptions. No route recommendation here depends on their outcome.
4. **The §14.3 register contains no entry**, because an entry requires an exact path and
   physical identity that criterion 20 forbids publishing here.
5. **Section C's checks have not been run**, because running them requires applying
   edits. Criterion 10's universal half therefore remains demonstrable-in-principle
   rather than demonstrated, until C.4 runs against the amended file.
6. **Criterion 19 is evidenced by the session transcript, not by the artifact** (TS-13).
   No text in an amended design can evidence a command that was not run.
7. **Criterion 2 remains a universal over every sentence.** The per-hunk out-of-context
   reading in the response matrix is the best available check; it is not a proof.
8. **The divergent-lineage collision at `docs/worktree_cleanup/PLANNING.md` is not
   repaired.** Hunk 5 neutralizes the design's citation and S34 redirects §1.3, but which
   lineage is canonical stays a separate, explicitly out-of-scope owner decision.
9. **`docs/worktree_cleanup/evidence/2026-09-28-state.md` is not tracked on
   `origin/main`.** See section E item 5 — this is the one gap that Plan v2 cannot
   discharge by drafting.

---

## E. Where the council's fix is an owner choice, not a repair

*Five items. Each is a place where the reviewers identified a real defect but the remedy
is a judgement the owner may want to make differently. Plan v2 states its recommendation
and proceeds on it; none of these is settled by this council.*

**E.1 — Operation F cardinality: closed set, or one source per operation (B5/AR-1).**
Plan v2 resolves toward **one operation binding one approved closed set**, with a strictly
per-source outcome and no set-level aggregate. *Why:* owner-signed criterion 6 speaks of
an exact closed set with the freeze budget recalculated *"for the complete set"*, so the
one-source-per-operation reading strains a criterion the owner already signed. *The cost:*
a closed set means one freeze window covers several sources, so a defect on the third
source occurs inside a freeze already opened for the first two. The one-source reading
buys tighter blast radius at the price of re-approving a maximum freeze duration per
source and re-deriving criterion 6's "complete set" language. **The owner may prefer the
tighter form.**

**E.2 — Criteria 14 and 17 are in genuine tension, and the owner signed both
(AR-16/PR-13).** Criterion 14 bans a **CI run outcome** from the design and `INDEX.md`;
criterion 17 lists *"the disposition of the cancelled post-merge required check"* among
the obligations the design must state. *"Cancelled"* is an outcome. Plan v2 adopts the
**outcome-free phrasing** — *"the outstanding post-merge required-check disposition
recorded in the dated operation evidence"* — in both Hunk 4 and Hunk 5, which discharges
17's obligation without asserting 14's banned fact. **The owner may instead rule that 17's
own phrasing governs for this one phrase**, in which case both hunks revert to
*"the cancelled post-merge required check"* and criterion 14 carries a recorded,
owner-approved exception rather than a silent one.

**E.3 — Whether `PREVENTION_COMPLETE` gates Operations F and G (PR-15).** Plan v2
**requires it**, and recommends requiring it. *Why:* Operation A prevents the very defect
that creates unexpected drive-root children; an F freeze running before prevention is
complete could itself create one, which the amended §8.3 and §11 delta checks would then
correctly fail — a deadlock designed in at the text level. *The second-order effect the
owner should see, which no reviewer named:* requiring it means single-location material
stays unpreserved until Operation A completes, which makes the **early targeted rescue
question more pressing, not less**. That question is out of scope here and stays
undecided; this recommendation does not touch it, but it raises its stakes.

**E.4 — The two pointers that resolve to a lineage lacking the sign-off (AR-17/PR-20).**
Plan v2 **neutralizes without choosing**: Hunk 5 replaces the linked
`[planning record](../worktree_cleanup/PLANNING.md)` with the unlinked, lineage-neutral
*"the approved planning record"*, and S34 adds a dateless §1.3 sentence sending a reader
of any later amendment to that amendment's own council artifact, naming this one. **What
Plan v2 does not do is repair the link**, because doing so requires deciding which of the
two divergent lineages the design cites — a decision Section 0 places out of scope. The
owner may prefer to decide the lineage now and restore a correct link, which would make
both edits unnecessary.

**E.5 — The dated-evidence file is not tracked on `origin/main` (TS-10, closed by the
manager's read-only `git` work).** `git ls-tree origin/main -- docs/worktree_cleanup/`
returns exactly two blobs, and neither is `evidence/2026-09-28-state.md` nor the source
packet. **Consequence, stated plainly: as drafted, this amendment removes the merge date,
the PR number, the CI run identity, the counts, the disappearance window, and the creation
timestamps from the tracked design, and points at a file that does not exist for any
reader of `origin/main`.** Criteria 14, 16 and 17 are satisfied only by that file's
contents, so following the pointer is not optional. Three remedies, all the owner's to
pick:

1. **Commit the evidence file in the same change.** Cleanest — the pointer resolves for
   every reader. Cost: it adds a file under `docs/worktree_cleanup/`, which is **not** a
   globbed surface, so `Test Inventory Drift` is still untripped; but it also publishes
   the dated record, which must first be privacy-reviewed under §2.2 rules 16–17.
2. **Land a dateless pointer only**, and leave the dated facts entirely in the private
   record. Cheapest, and preserves privacy. Cost: criteria 14's and 16's framing
   requirements become unverifiable by any reader of the repository.
3. **Accept a dangling reference knowingly**, recorded as such. Cost: a future reader
   following criterion 14's instruction finds nothing, which is the failure mode the
   packet's own evidence record warns about elsewhere.

**Recommendation: option 1**, conditional on a privacy review of the evidence file
first. The packet's whole posture is that a receipt without a followable record is
incomplete, and option 3 reproduces exactly the defect the September re-entry found. This
council does **not** commit, stage, or edit anything — and it proposes no edit to either
`docs/worktree_cleanup/PLANNING.md` lineage.

---

**Plan v2 stops here, awaiting the owner's Gate 1 decision.** No hunk is applied. No
Gate 1, Plan v2, or Sign-off box is checked.

---

## Sign-off

**AWAITING THE OWNER'S GATE 1 DECISION.** The council has run and Plan v2 exists. **No
box below is checked**, and none may be checked by any agent: the boxes are the owner's
to check. The factual state of each is annotated so that the owner is not asked to infer
it, and annotating a box is not checking it.

- [ ] Gate 0 complete when required by planning size; otherwise marked not applicable.
      *(Factual state: Gate 0 was signed directly by the owner, Yaakov Avihai Shai, on
      2026-09-28, with the verbatim approval recorded in Section 0. The box stays
      unchecked here because this council step checks no box.)*
- [ ] Every finding has a disposition.
      *(Factual state: 59 findings across three reviewers, 43 matrix rows, all
      ACCEPTED, none rejected and none deferred.)*
- [ ] Agent provenance complete — both `product-manager` IDs, same-PM-resumed yes/no, the three reviewer IDs, and an evidence-gap line (or `none`).
      *(Factual state: the Agent provenance block carries both `product-manager` rows
      with the same ID `a419e27d5f34b2435`, same-PM-resumed `yes`, all three reviewer
      IDs, and a substantive evidence-gap line. No ID was invented and no completed
      council work was rerun.)*
- [ ] User approved Plan v2.
      *(Factual state: **not given.** Gate 1 is unsigned. Section E of Plan v2 lists the
      five items that are owner choices rather than mechanical repairs.)*
- [ ] Ready to implement — proceed to code, then `/unslop` or `/verify-and-polish` for the diff-time gate.
      *(Factual state: **not ready.** No hunk has been applied to
      `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` or `docs/ai_workflow/INDEX.md`, and
      none may be before Gate 1.)*

---

## See also

- [`docs/worktree_cleanup/AMENDMENT_2026-09-28.md`](../worktree_cleanup/AMENDMENT_2026-09-28.md) — the draft amendment packet (source).
- [`docs/worktree_cleanup/evidence/2026-09-28-state.md`](../worktree_cleanup/evidence/2026-09-28-state.md) — dated state evidence; the home for every dated count, timestamp, and the backup-disappearance window.
- [`docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md`](../ai_workflow/WORKTREE_CLEANUP_PLAN.md) — the current technical design being amended. The `origin/main` tracked copy is the amendment base.
- [`docs/ai_workflow/INDEX.md`](../ai_workflow/INDEX.md) — carries the stale *"Gate 1 … pending"* description corrected by this packet.
- [`docs/WORKTREE_CLEANUP_PLAN.md`](../WORKTREE_CLEANUP_PLAN.md) — the **other**, older document: the closed August P1.2 campaign record. It does not control the present machine; do not conflate the two.
- [`docs/ai_workflow/QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) — plan-stage routing and change-type gates.
- [`docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md) — the artifact shell.
- [`.claude/commands/council-plan.md`](../../.claude/commands/council-plan.md) — how the council runs, once Gate 0 is signed.

---

## 2026-10-29 — Gate 1 readiness refresh, proposed review input

**Status: Gate 0 is signed; Gate 1 remains unsigned.** The owner's current request is
to handle the cleanup amendment end to end with multiple agents and consultation as
needed. The quoted status, "Paused since 09-28. Section 0 is drafted, and Gate 0 is
unsigned", predates the direct owner signature recorded above. It is superseded by
that signature, the completed September council, and Plan v2. This refresh approves
nothing and checks no sign-off box.

### Provenance and scope

| Role | Actual agent identifier | Scope |
|---|---|---|
| Product manager — readiness draft | `/root/product_manager` | This dated appendix only; identifier supplied by the manager |
| Product manager — response matrix and final refresh | `/root/product_manager` | Same refresh PM resumed; identifier supplied by the manager |
| Same PM resumed for this refresh's matrix? | yes | Continuity applies to this October refresh only |
| Architecture reviewer | `/root/amendment_audit` | Fresh review and affected-text recheck complete; no remaining architecture blocker |
| Test strategist | `/root/state_audit` | Fresh review and affected-text recheck complete; no remaining readiness blocker; TS-3 withdrawn |
| Product risk reviewer | `/root/risk_review` | Fresh review and affected-text recheck complete; no remaining readiness blocker |

**Evidence gap:** this is a fresh product-manager agent, not the September agent.
The September IDs and completed reviews remain intact above. No September review
was rerun to manufacture continuity. The proposed status wording, evidence addendum,
and application-precondition repairs below are new review input. All three fresh
reviews completed with findings, reproduced below, and their affected-reviewer
rechecks are complete. The manager's candidate snapshots and verification records
are under `artifacts/cleanup-amendment-closeout-20261029/`; the final preparation
results and their limits are recorded at the end of this appendix. This is no claim
of owner approval or a completed implementation gate.

**Calculation surface: none.** This remains a document-only amendment. No
application, database, API, calculation, launcher, guard, or test behavior changes.
No source or target is selected for F or G, and no preservation or retirement is
commissioned. The early targeted rescue decision, both divergent Operation A
`PLANNING.md` lineages, and the historical baseline remain outside this amendment.

### Evidence that changed after the September draft

- The technical-plan base remains blob
  `1b41922e795e9202f128a9b1122d0ffb6c6134af` on the inspected `origin/main`.
  `INDEX.md` is now blob `d67a76f0027d038e5fbfca946dc187cdf91e8302`; its Hunk 6
  target paragraph is unchanged, but the full-file preimage in C.1 is stale.
- The tracked `docs/worktree_cleanup/CLOSEOUT.md`, blob
  `baf0139751047288783988d4ea89f09216598db1`, records later owner-authorized
  worktree removal and separate drive-root work. Its §12 keeps this amendment and
  F/G parked, §18.3 excludes RESIDUE-1 and RESIDUE-2, and §19.6/§20 preserve the
  unresolved prevention acceptance. This amendment does not repeat a historical
  assertion that B/C/D have never received an approval, nor infer that their later
  directives approved F/G.
- The retained October 13 reassessment records a surviving preservation copy on a
  **different volume**, two member identities verified against retained manifests,
  and a narrower observation interval for the disappearance. It does not establish
  a different physical device or an off-machine copy. It performed no restore.
  The September 28 evidence stays a dated historical assessment; its superseded
  premises must be framed by a dated addendum before publication.

### Recommended owner decisions — the same five choices

These remain recommendations for Gate 1, not decisions made by this refresh.

| Choice | Recommendation | Consequence |
|---|---|---|
| E.1 | One Operation F binds an approved closed source set; outcomes remain per source | The freeze budget and maximum duration cover the complete set; there is no set-level success aggregate |
| E.2 | Use outcome-free CI wording in the stable design | Dated evidence records the actual check outcome and its disposition; no outcome is silently treated as a pass |
| E.3 | Require `PREVENTION_COMPLETE` for F and G | This amendment cannot authorize either operation while prevention acceptance remains incomplete |
| E.4 | Keep the lineage-neutral approval reference and each amendment's own council pointer | Neither divergent Operation A planning lineage is overwritten or selected here |
| E.5 | Publish the privacy-reviewed September evidence, dated addendum, historical reference stub, and council copy with the narrow path redactions specified below | Repository readers receive the historical evidence, later corrections and approval trail; original local sources and private source identities remain private |

### Exact replacement Hunk 5 — status header

This replaces only Hunk 5's proposed `TO`; its upstream `FROM` span stays BASE:6–12.
The carrier and S16 corrections appended below also replace their specified proposed
text; every other Plan v2 operation contract and edit location remains unchanged.

```markdown
*Approval state: Gate 0 and Operation A Plan v2 Gate 1 are signed, and the approved
planning record records the approved implementation and verified disposable
interactive Windows acceptance. Operation A's reviewed guard and test source is
merged. Section 5.4, Section 11, and the dated operation evidence govern installation,
verification, monitoring, post-merge required-check disposition, and successor-artifact
reconciliation obligations; this amendment discharges none. Operation-specific owner
approval and Windows-filesystem review remain requirements under the contracts below.
Actual approvals, waivers, execution results, and the remaining prevention acceptance
are recorded in the dated [closeout record](../worktree_cleanup/CLOSEOUT.md) and
[state evidence](../worktree_cleanup/evidence/2026-10-29-amendment-readiness.md).
E requires its own separate plan and approval. Section 14 defines F and G under
their own separate plans and approvals; neither is approved here. This amendment
does not reopen completed operations or declare PREVENTION_COMPLETE.*
```

This wording carries no merge date, PR number, run identity, count, private path, or
CI outcome into the stable design. It records requirements without converting
unmeasured current state into a new "outstanding" verdict. Hunk 4's obligation list
and S29 remain requirements; any later completion or waiver belongs to its dated
authority and is not reset by this amendment.

### Exact replacement Hunk 6 — INDEX description

This replaces only Hunk 6's proposed `TO`. Its five-line upstream `FROM` paragraph
must match exactly once in the new INDEX base, with the current location determined
from that exact paragraph rather than the September line numbers.

```markdown
- [Worktree Cleanup and Preservation Plan](WORKTREE_CLEANUP_PLAN.md) — phase-gated
  prevention, malformed-root quarantine, preservation, worktree retirement, main
  reconciliation, and separately gated preservation and retirement routes for
  drive-root children outside Operations B and C. Gate 0 and Operation A Plan v2
  Gate 1 are signed; each later semantic amendment and operation requires its
  applicable approval. The dated [closeout record](../worktree_cleanup/CLOSEOUT.md)
  records completed work and the remaining prevention acceptance; this entry
  grants no operation approval
```

### Proposed public dated addendum — exact text

Proposed new path:
`docs/worktree_cleanup/evidence/2026-10-29-amendment-readiness.md`.
Publication remains conditional on E.5 and privacy review. The September 28 evidence
file is retained without rewriting its historical text. Private reports and source
paths are not published with this addendum.

```markdown
# Cleanup amendment — dated evidence addendum, 2026-10-29

This addendum frames the historical September 28 assessment for amendment review.
It grants no preservation, relocation, quarantine, deletion, or operation approval.
It reports retained evidence; no live preservation source or database was opened,
and no new restore or filesystem inventory was performed for this addendum.

## Reading the September assessment

[The September 28 assessment](2026-09-28-state.md) is a dated record, not current
live state. It records absence at the original paths and draws a retention-priority
inference; it does not establish that no other copy survives. The later reassessment
described below supersedes that absence-based retention inference and narrows the
observation window. Historical operation obligations must also be read with the later owner directives in the
[closeout record](../CLOSEOUT.md).

## Later preservation evidence

The retained October 13 reassessment records both named August preservation
artifacts in a surviving copy on a different volume. Two member identities were
recomputed and matched against retained manifests: the evidence tar and a Git
bundle. This establishes neither the integrity of every retained member nor a
successful restore. A different volume does not prove a different physical
device or an off-machine copy. The copy's private path is not reproduced here.

That reassessment records observations of the original backup parent as present
at 2026-09-28T15:27:01Z and absent at 2026-09-28T15:31:22Z, an interval of
4 minutes 21 seconds. The observations came from a retained session transcript,
corroborated by filesystem timestamps and undated interactive command history.
They bound observations; they do not identify the actor or exact removal time.
The August campaign remains refuted as the cause. Recovery and retention still
require their own verification; the surviving-copy report is not a restore receipt.

## Later operation authority

The tracked [closeout record](../CLOSEOUT.md), especially §§12, 18.3, 19.6 and 20,
records the later worktree and separately authorized drive-root operations, their
scope and waivers, and the remaining prevention acceptance. It keeps this
amendment and Operations F/G parked and excludes RESIDUE-1 and RESIDUE-2 from the
recorded drive-root cleanup. Those directives do not approve either new operation.
This addendum neither reopens completed operations nor declares
`PREVENTION_COMPLETE`.

## Amendment approval state

The amendment's [council artifact](../../worktree_cleanup_amendment/PLANNING.md)
records the owner's September 28 Gate 0 signature, the completed September council,
and the proposed readiness refresh. Gate 1 has not been given at this addendum's
drafting. Publication and implementation require the owner's Gate 1 decision.
Exact source identities, member details, and storage locations remain private.
```

### Historical source-reference landing

The September evidence links to `../AMENDMENT_2026-09-28.md`, which is absent from
the inspected upstream tree. Publishing the September evidence without a landing
would retain a dangling link. The proposed remedy is a clearly labelled reference
stub at `docs/worktree_cleanup/AMENDMENT_2026-09-28.md`, with this exact text:

```markdown
# Historical cleanup-amendment reference

This reference resolves links from the historical September assessment. The
original September draft at this path is retained privately and is not reproduced
by this reference.

Use the [council artifact](../worktree_cleanup_amendment/PLANNING.md) for the signed
requirements, council findings, proposed amendment text and recorded gate decisions.
Read the [dated evidence addendum](evidence/2026-10-29-amendment-readiness.md)
together with the [September assessment](evidence/2026-09-28-state.md).

This reference is navigation only. It grants no preservation, retirement, operation
or implementation approval. The council artifact records the approval state.
```

This adds a public reference without publishing the old, unapproved source draft
as the current design. The local original at that path remains untouched and
privately retained. The publication manifest must distinguish the new stub's bytes
from the local source; the stub must never overwrite that local source during
preparation or landing.

**Public council privacy treatment.** The publication copy of this council artifact
requires narrow redaction of machine-local scratch and absolute checkout paths in
the historical reviewer text, including alternate backslash spellings. Replace only those path values with descriptive
placeholders, retain the substantive findings, and leave approvals and signatures
unchanged. The exact source-line locations and preimage digests belong in the
private verification record. The canonical local artifact retains its original
bytes and the append-only readiness record. The proposed public copy must carry
this notice before its historical reviewer text:

> Historical reviewer text is reproduced with machine-local scratch and absolute
> checkout paths redacted. The original is retained privately; these path redactions
> do not change a finding, disposition, approval or signature. References to verbatim
> reviewer findings in the historical record are subject to these disclosed redactions.

**Proposed publication manifest, conditional on Gate 1 and E.5:**

| Path | Proposed publication treatment |
|---|---|
| `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md` | Apply its 41 reviewed edits to the pinned upstream base |
| `docs/ai_workflow/INDEX.md` | Apply the one reviewed paragraph replacement; retain unrelated upstream edits |
| `docs/worktree_cleanup_amendment/PLANNING.md` | Publish the council and readiness record with only the disclosed public-path redactions and notice |
| `docs/worktree_cleanup/evidence/2026-09-28-state.md` | Publish the unchanged historical assessment, read with the addendum |
| `docs/worktree_cleanup/evidence/2026-10-29-amendment-readiness.md` | Publish the dated addendum proposed above |
| `docs/worktree_cleanup/AMENDMENT_2026-09-28.md` | Publish the reference stub above, not the privately retained original draft |

No private local evidence, exact source identity, storage location, or divergent
Operation A `PLANNING.md` is included. The stub and redaction treatment are fresh
review input, not approved publication.

### Application and closure checks

The original 42-edit count remains 41 technical-plan edits plus one INDEX edit.
The proposed `TO` changes are Hunk 5, Hunk 6, the three specified blocks inside
Edit N's carrier, and S16. E.5 adds the publication documents listed in the manifest;
these changes do not change the 42-edit count for the two AI-workflow files.

Before approval, the manager may prepare clearly labelled unapproved snapshots and
a patch under the gitignored review directory. This does not apply approved text to
the actual design. Candidate checks are preparatory evidence, not the post-approval
implementation gate.

After Gate 1, use the standalone-clone landing requirements already specified in
§1.3 and D. Re-read upstream; abort on unreviewed base drift. C.1 must bind the
current reviewed INDEX blob rather than the obsolete September full-file hash,
while also requiring its target paragraph to match exactly once. Retain all
unrelated INDEX changes. Apply the 42 edits in their prescribed descending order
and record the expected and actual line counts for the refreshed text.

C.2 requires exact old spans and exact new text, but its universal "FROM text no
longer appears anywhere" claim must be checked rather than assumed: some `TO`
blocks deliberately retain old lines, including Hunk 4's original unchecked box.
The candidate verification must report each literal failure and the replacement
span proof; it must not label a retained old sentence as absent. Likewise C.4's
surviving quantifiers require a site-by-site disposition against B.2, not a raw
zero-hit assumption. No failing mechanical check is waived by this paragraph.

**Proposed replacement C.2 check, for review.** Immediately before each replacement,
assert that the complete current line span equals its specified `FROM` block.
Replace only that span; assert that the complete new span equals the specified
`TO` block and that the prefix and suffix outside the span are unchanged. For an
insertion, assert the exact anchor line, insert the complete `TO` immediately
after it, and assert that the surrounding prefix, anchor and suffix are unchanged.
Record both the old and new span for each operation. Assert that every complete
`TO` occurs exactly once in the final file. Retained lines inside a larger `TO`
are reported explicitly; they are not evidence that the replacement failed and
are never described as absent. No stale `FROM` is permitted at its replaced
location except where its text is explicitly retained within the approved `TO`.

**Proposed replacement C.4 check, for review.** Enumerate every surviving hit for
the original literal patterns, with exact line text, enclosing contract and
occurrence count. Require each hit to match an individually reviewed manifest
entry that gives its reason: a historical record, an operation-specific contract,
an explicit independence/exclusion statement, a template comparison, or an exact
preserved rollout requirement. A whole-section exemption is not permitted.
In particular, examine S13's B/C/D comparison, §7.6's C-only preservation seal,
§10's independent failure handling, §14.0's preserved B/D meanings, and the
rollout sequence. Every new or changed match without an exact reviewed entry
fails the check. Assert that all intended F/G enrollment edits are present as
complete `TO` blocks, so a surviving noun list cannot pass merely because it
resembles an exception. The manager must supply the actual enumerated manifest
and proposed dispositions for fresh review; this paragraph grants no unenumerated
exception and records no check result.

Run the targeted workflow-contract pytest and inventory `--check` in the approved
isolated clone, with the runtime, temp and cache redirects and object-store
independence checks already required. Do not run or regenerate inventory from the
dirty main checkout. No E2E gate is introduced by this document change. Complete
the applicable diff review and normal PR checks, then record the actual landed
commit and close the amendment row only after landing and verification. Amendment
closure does not mean that F/G have run or that prevention is complete.

**Fresh reviews and corrected-candidate rechecks completed. Owner Gate 1: unsigned.
Implementation: not started.**

### Fresh reviewers' findings — verbatim

#### Architecture reviewer — `/root/amendment_audit`

Reviewed the frozen six-file candidate, its patch and checks, the readiness-refresh appendix, the retained F/G contracts, and the upstream closeout record. No files were edited and no tests, database access or Git mutations were performed.

1. **High — Operation F’s eligibility condition invalidates itself when its manifest is approved.**  
   `proposed/docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md:1657–1663` defines “outside approved operation scope” as absent from any approved source/target manifest and explicitly says this qualifier stops applying upon manifest approval. Yet `:1713–1716` requires an **approved** F source set whose sources **are outside approved operation scope**, while `:1725–1728` requires an approved manifest enumerating those sources. A source cannot satisfy both predicates after approval.  
   **Fix:** Make the outside-scope eligibility test explicitly historical: evaluate and retain it immediately before approving that Operation F manifest; specify that the ensuing approval enrolls only that exact closed set and does not change its “unexpected” classification or the baseline. Update the corresponding proposed `TO` text and approval requirements together.

2. **Medium — Refreshed status wording can assert an Operation E approval that the cited closeout does not establish.**  
   `proposed/docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md:16` says **“E remains separately planned and approved.”** In this approval-state paragraph, that reads as a completed approval. The cited upstream `CLOSEOUT.md:403–410` instead keeps E/main reconciliation parked; this refresh establishes no new E approval. The neighboring F/G sentence explicitly withholds approval, making E’s different wording particularly misleading.  
   **Fix:** Replace it with **“E requires its own separate plan and approval.”** Apply the same correction to the refresh’s replacement Hunk 5.

The dated addendum appropriately separates retained reports from fresh measurements, avoids claiming a different physical device or successful restore, and preserves the Gate 1 boundary. The historical stub and disclosed path redactions preserve the distinction between private originals and proposed public copies. The reported C.2 literal failures are disclosed rather than presented as passing checks.

**Verdict: Needs revision.** These are drafting repairs; neither grants approval nor requires reopening the signed Gate 0 choices.

#### Test strategist — `/root/state_audit`

Fresh test-strategist review completed as `/root/state_audit`. No tests, DB access, mutations, or other reviewers’ findings were used.

1. **Blocking — C.4 does not yet enforce its proposed contract.** `refresh_candidate.py:80–103` enumerates matching *lines*, checks only that there are 15, then assigns reasons by position. A changed survivor with the same total receives an old disposition; multiple occurrences on one line are not counted. Fix: freeze individually reviewed entries keyed by exact text, enclosing contract and per-pattern occurrence counts; compare actual versus expected entries and fail on any difference. Keep the proposed dispositions advisory until reviewed.

2. **Significant — C.2’s reported proof is not bound to the inputs consumed by the final refresh.** `refresh_candidate.py:21–25` trusts saved edit JSON and September snapshots; line 131 unconditionally reports exact-span verification. Although `prepare_candidate.py:89–106` performs the proper assertions, the refresh neither reruns them nor verifies those saved inputs against their producing run. Fix: rebuild from pinned upstream snapshots in the final pass, or verify saved-input hashes and include the source/edit/intermediate bindings in `checks.json`.

3. **Significant — a known public link remains broken.** Proposed `PLANNING.md:998` contains an active quoted link to `WORKTREE_CLEANUP_PLAN.md`, resolving inside `docs/worktree_cleanup_amendment/`; `checks.json:301` correctly reports it missing. Fix its publication representation without altering the finding—e.g. render that historical quoted line as literal code, or disclose a navigation-only target correction. Require an empty unresolved-link report before publication.

4. **Significant — the promised redaction notice is not placed before the redacted findings.** Proposed `PLANNING.md:3542–3547` promises a notice before historical reviewer text, but the sole notice appears there, after the reviewer section beginning at line 1532. `refresh_candidate.py:40–52` redacts paths but inserts no earlier notice. Insert the disclosed notice immediately before the historical reviewer text and verify placement.

Required post-approval gates remain appropriate: isolated standalone clone; pinned-base and object-store independence checks; runtime/temp/cache/bytecode redirects; exact edit/C.4/link/privacy checks; targeted `tests/test_agent_workflow_contracts.py`; inventory `--check`; applicable diff review and normal CI. These are document changes: no E2E, fixture changes, new automated tests, or full `/verify-suite` is warranted. The two AI-workflow files have existing prose coverage; the four publication documents require manual link/evidence/privacy verification.

**Verdict:** targeted gate sufficient after these readiness defects are addressed. Gate 1 remains unsigned; candidate checks do not constitute implementation acceptance.

#### Product risk reviewer — `/root/risk_review`

1. **High — Operation F imports live archive-ref creation while prohibiting it.** Proposed `docs/ai_workflow/WORKTREE_CLEANUP_PLAN.md:1760` imports §7.3’s archive-ref obligations; §7.3 at `:1036` requires the owner to create needed refs, while F at `:1788` prohibits creating archive refs or live Git metadata. A Git-bearing source with a nonempty archive-ref-need set cannot satisfy both. **Fix:** explicitly reject such a source under F before approval, or separately review a precise alternative; do not leave an executor to infer ref-creation authority.

2. **Medium — Public-council privacy treatment is incomplete.** Proposed `docs/worktree_cleanup_amendment/PLANNING.md:1671` retains an absolute machine-local checkout path. The redaction proposal at `:3536` promises scratch and absolute-checkout redactions. Its required disclosure appears only as quoted future text at `:3544`, after the historical reviewer section at `:1536`, which still claims verbatim reproduction. **Fix:** redact every machine-local repository prefix consistently and install the disclosure immediately before the historical reviewer text in the public copy. Preserve the original local artifact.

3. **Medium — The new addendum attributes an unsupported claim to the September assessment.** Proposed `docs/worktree_cleanup/evidence/2026-10-29-amendment-readiness.md:11` says September claimed “no surviving copy.” The September evidence establishes absence of original paths (`2026-09-28-state.md:176–185`) and draws a retention-priority inference (`:212`); it does not establish universal absence of other copies. **Fix:** say the later investigation supersedes the inference from original-path absence and its retention rationale, rather than attributing an explicit no-copy claim.

Reviewed the six proposed publication files, relevant retained operation contracts, disclosure proposal and checks. No calculation, API, application-backup, telemetry or product cloud-sync change was found. Gate 0 is recorded as signed; this review grants no Gate 1 or operation approval.

**Verdict: Needs revision.**

### Fresh response matrix — all findings dispositioned

The manager proposed these dispositions after the independent reviews completed.
The same refresh product manager records them here, including the affected reviewer's
later withdrawal of TS-3. Eight findings were accepted and resolved; one was
withdrawn. None is deferred. These dispositions approve neither the amendment nor
publication nor an operation.

| Finding | Reviewer | Disposition | Action in corrected proposal |
|---|---|---|---|
| AR-1 | architecture reviewer | ACCEPT | F eligibility is assessed and retained immediately before manifest approval; the approval binds the exact historical eligibility record and enrolls only that set |
| AR-2 | architecture reviewer | ACCEPT | Hunk 5 now says E requires its own separate plan and approval; it asserts no approval occurred |
| TS-1 | test strategist | ACCEPT | Root freezes exact reviewed quantifier entries by text, enclosing contract and per-pattern counts, compares multisets, and forbids automatic manifest regeneration |
| TS-2 | test strategist | ACCEPT | Root reruns the pinned 42-edit extraction/assertions in every final refresh and binds producing inputs, edit data, intermediate and final outputs by digest |
| TS-3 | test strategist | WITHDRAWN after reviewer correction | The source line was already inside a blockquoted fenced code block. Preserve the original quoted text; the checker now recognizes quoted fences. The initial incorrect finding remains verbatim above |
| TS-4 | test strategist | ACCEPT | Root places the disclosed redaction notice immediately before the historical Reviewer findings section and verifies ordering |
| PR-1 | product risk reviewer | ACCEPT | F requires an empty read-only-computed archive-ref-need set before approval and rechecks it at capture; a nonempty or unresolved set rejects the source and requires a separately reviewed plan |
| PR-2 | product risk reviewer | ACCEPT | Public-copy path redaction covers every machine-local checkout prefix, including doubled-backslash spellings; private canonical bytes are retained |
| PR-3 | product risk reviewer | ACCEPT | The addendum now distinguishes the original-path absence finding from the superseded absence-based retention inference |

**Superseded formatting proposal:** the initial TS-3 disposition proposed adding
inline backticks to the historical INDEX quotation. The reviewer withdrew the
finding after recognizing its existing blockquoted code fence. That unnecessary
formatting change was reverted; the public copy preserves the original quotation.
The checker was corrected to recognize quoted fences. The separate path-redaction
notice and narrowly scoped path redactions remain required.

### Corrected semantic proposal — exact carrier and approval substitutions

These substitutions are applied only inside Edit N's proposed `TO` and S16's
proposed `TO`. They replace no signed text and select no source. They are drafting
repairs to the reviewed proposal. Their affected-reviewer rechecks are complete;
Gate 1 remains unsigned.

#### Carrier correction F opening

**FROM**

```markdown
No Operation F preservation authority exists for any source until every one of the
conditions below is true. Operation F preserves an approved closed set of exactly
identified unexpected drive-root children that are outside approved operation scope
under Section 14.0. It is not a general route for arbitrary sources outside Operation
C's scope, and it is not an extension of Operation C's immutable source manifest: no
Operation C manifest, approval, receipt, freeze budget, or capacity approval is
altered, reused, or extended by it.
```

**TO**

```markdown
No Operation F preservation authority exists for any source until every one of the
conditions below is true. Operation F preserves an approved closed set of exactly
identified unexpected drive-root children. Immediately before approval of that
Operation F manifest, an exact, retained eligibility assessment must establish that
every source in the set is outside approved operation scope under Section 14.0.
The ensuing approval enrolls only that same closed set by exact path and physical
identity. The scope qualifier then stops applying as Section 14.0 describes; neither
the sources' unexpected classification nor the owner-approved baseline changes.
Operation F is not a general route for arbitrary sources outside Operation C's scope,
and it is not an extension of Operation C's immutable source manifest: no Operation
C manifest, approval, receipt, freeze budget, or capacity approval is altered, reused,
or extended by it.
```

#### Carrier correction F approval

**FROM**

```markdown
1. A Section 4.3 immutable, digest-bound manifest enumerates the exact, closed set of
   sources by canonical/final path and physical identity, and a dated Section 4.3
   owner approval record for that manifest exists, created separately from and after
   this plan text. Wildcard or prefix expansion, source-to-source overlap,
   source-to-destination overlap, overlap with Operation C's approved scope, overlap
   with a previously approved Operation F source, a missing source, and a changed
   identity are each a rejection, not a warning.
```

**TO**

```markdown
1. A Section 4.3 immutable, digest-bound manifest enumerates the exact, closed set of
   sources by canonical/final path and physical identity. Immediately before its
   approval, retain a digest-bound assessment of that exact set's Section 14.0
   outside-scope eligibility. A dated Section 4.3 owner approval record binds that
   assessment's digest and the same manifest, created separately from and after
   this plan text. It enrolls only the assessed identities and changes neither the
   owner-approved baseline nor the sources' unexpected classification. Wildcard or
   prefix expansion, source-to-source overlap, source-to-destination overlap,
   overlap with Operation C's approved scope, overlap with a previously approved
   Operation F source, a missing source, and a changed identity are each a rejection,
   not a warning.
```

#### Carrier correction F Git

**FROM**

```markdown
5. Any Git repository inside a source carries Section 7.3's OID enumeration and
   type-checking and archive-ref obligations and Section 7.4's separate preservation
   and restore-test, or the source is not approvable under Operation F.
```

**TO**

```markdown
5. Any Git repository inside a source carries Section 7.3's OID enumeration and
   type-checking and Section 7.4's separate preservation and restore-test. Before
   approving the Operation F manifest, compute Section 7.3's archive-ref-need set
   read-only from durable named refs and retain the exact result with the approval.
   The set must be empty; a nonempty or unresolved set rejects the source under
   Operation F. Recompute it read-only against the frozen source immediately before
   capture; any nonempty result, unresolved result, or changed protected ref/OID set
   stops the capture under its approved safe-abort or recovery protocol. Operation F
   creates no archive ref or other live Git metadata. A source needing ref creation
   requires a separately reviewed plan and its own approval; this paragraph grants
   no such authority and never treats a reflog as a durable named ref.
```

#### Approval correction S16

**FROM**

```markdown
An Operation F approval additionally binds the exact closed set of source identities,
each source's extraction root, the destination identity, the freeze budget with the
owner-approved maximum freeze duration approved for that Operation F operation, its
safe-abort boundary, and its expected capture and restore results. An Operation G
approval additionally binds exactly one drive-root child identity, one nonexistent
same-volume quarantine destination, its single ordered move, the
ADDITIONAL_SOURCE_PRESERVED(source) evidence for that exact identity, and its
retention start and per-object retention period. An Operation G approval is never an
Operation B approval, and no Operation B approval may bind an Operation G root.
```

**TO**

```markdown
An Operation F approval additionally binds the exact closed set of source identities,
the digest of that same set's retained outside-scope eligibility assessment taken
immediately before manifest approval, each Git-bearing source's retained empty
archive-ref-need set and protected ref/OID inventory, each source's extraction root,
the destination identity, the freeze budget with the owner-approved maximum freeze
duration approved for that Operation F operation, its safe-abort boundary, and its
expected capture and restore results. The approval enrolls only the assessed set;
it changes no source's unexpected classification and no owner-approved baseline.
An Operation G approval additionally binds exactly one drive-root child identity,
one nonexistent same-volume quarantine destination, its single ordered move, the
ADDITIONAL_SOURCE_PRESERVED(source) evidence for that exact identity, and its
retention start and per-object retention period. An Operation G approval is never an
Operation B approval, and no Operation B approval may bind an Operation G root.
```

These are four substitutions within two of the existing 42 edits, not four new
base-file edit locations. Every unchanged part of the carrier and S16 remains as
specified. The final candidate was rebuilt and its line count recomputed as recorded
below; the earlier 1913-line candidate is historical, not a post-correction assertion.

### Affected-reviewer final rechecks — verbatim

#### Architecture reviewer — `/root/amendment_audit`

Rechecked the corrected candidate’s affected semantic text.

- **AR-1 resolved:** §14.1 now evaluates outside-scope eligibility immediately before F manifest approval. Item 1 and §4.3 bind the retained assessment and exact source set to that approval. Subsequent enrollment changes neither the unexpected classification nor the baseline.
- **AR-2 resolved:** the header now states that E **requires** its own separate plan and approval.
- The archive-ref restriction is consistent with the revised approval binding: unresolved or nonempty archive-ref need rejects the source before approval, and capture rechecks preserve that restriction.

**No remaining architecture blockers in the corrected text or its material interactions.** Gate 1 remains unsigned; this recheck grants no approval.

#### Product risk reviewer — `/root/risk_review`

Recheck complete: **no remaining readiness blockers in my three findings.**

- PR-1: F now rejects nonempty or unresolved archive-ref need before approval, binds the empty result and protected inventory, and rechecks before capture. It grants no ref-creation authority.
- PR-2: The missed checkout path is redacted, and the disclosure now precedes historical reviewer findings.
- PR-3: The addendum accurately distinguishes original-path absence from the superseded retention inference.

The new pre-approval eligibility assessment preserves F’s scope boundary without changing the baseline or approving a source.

**Plan respects product invariants.** Gate 1 remains unsigned; this recheck grants no implementation or operation approval.

#### Test strategist — `/root/state_audit`

**No remaining readiness blockers** from this affected-reviewer recheck.

- **C.4 resolved:** `refresh_candidate.py:124` compares exact text, section and per-pattern counts against the fixed manifest. The two negative controls reject same-count text and occurrence changes.
- **C.2 resolved:** each final build reruns preparation, whose upstream blobs are pinned (`prepare_candidate.py:29–34`); exact-span checks and saved input hashes bind the resulting candidate.
- **Notice placement resolved:** the publication notice appears before the historical reviewer text (`proposed/…/PLANNING.md:1534`, reviewer begins 1545).
- **Finding 3 withdrawn:** the alleged broken link was already inside a blockquoted fenced code block. My original “active link” classification was incorrect. Inline backticks are unnecessary; preserving the original quoted line and teaching the checker about quoted fences would be cleaner.

The carrier/S16 corrections remain document-only and do not introduce additional test or fixture requirements. The reported 42 edits, 1,934-line plan and artifact-only patch applicability are preparation evidence. Post-approval isolated-clone pytest, inventory, diff review, CI and landed-state verification remain required.

This review grants no Gate 1 approval or publication authority.

### Final preparation state and limits

The manager reports the rebuilt candidate has **42 edits and 1934 technical-plan
lines**, with exact old spans and unchanged surrounding content checked, every
complete `TO` unique, and the producing inputs bound by hashes. All 15 surviving
C.4 entries match the fixed reviewed text/contract/per-pattern-count manifest;
same-count text and occurrence mutations are rejected by the negative controls.
The link report has no unresolved rendered links, the specified machine-local
prefixes are absent from the public copy, and its disclosure precedes the historical
reviewer findings. Artifact-only `git apply --check --no-index` succeeds against
the prepared upstream snapshots. The entire September source prefix remains
byte-exact in the local canonical artifact.

These are preparation checks on proposed artifacts. No target design was amended,
no standalone implementation clone was created, no targeted pytest or inventory
gate was run for implementation, and no PR was landed by this readiness step.
The final public council copy must be rebuilt after this administrative record is
added; its integrity and link/privacy reports remain bound to the actual copy used
for the owner's decision.

### Owner Gate 1 decision required

**Gate 1 remains UNSIGNED.** All three fresh reviews and affected-text rechecks
are complete; eight findings are resolved and TS-3 is withdrawn. No owner box is
checked and no approval is inferred from the request to finish the work.

The proposed decision accepts the corrected Plan v2 and the reviewed six-file
publication candidate, with these five choices:

1. **E.1:** one Operation F binds one approved closed source set; success remains
   per source, with a complete-set capacity and freeze budget and no aggregate.
2. **E.2:** stable design wording records the CI-disposition obligation without
   embedding a CI outcome; dated evidence records actual outcomes and dispositions.
3. **E.3:** `PREVENTION_COMPLETE` is required before either F or G may run.
4. **E.4:** preserve lineage-neutral references and amendment-specific council
   records; neither divergent Operation A planning lineage is selected or overwritten.
5. **E.5:** publish exactly the six document paths in the manifest, including the
   unchanged September evidence, dated corrective addendum, historical-reference
   stub, and council copy with disclosed machine-local path redactions.

This approval would also adopt the reviewed drafting repairs: retain exact-source
eligibility immediately before F manifest approval, enroll only that assessed set,
and reject any F source with unresolved or nonempty archive-ref need. F grants no
new-ref authority; a source needing such creation requires a separate reviewed plan.

For end-to-end closure, the requested decision must authorize Codex to prepare the
document-only implementation in the required isolated standalone clone, preserve
the dirty checkout and private originals, run the specified gates and independent
diff review, and open and land the PR only after required checks pass. Record the
actual landed state before closing the amendment item. This decision commissions
no F/G operation, selects no source or target, decides no early rescue, changes no
historical baseline, and grants no preservation, relocation, quarantine or deletion.

**Ready for the owner's concrete Gate 1 decision. Implementation and publication
remain unapproved until that decision is given.**

---

## 2026-10-29 — Owner Gate 1 approval and bounded implementation authority

**Current approval state: Gate 1 APPROVED by the owner for corrected Plan v2 and
the reviewed six-file publication candidate. Merge is NOT authorized.** This dated
record supersedes the earlier unsigned-state descriptions for this amendment;
the historical text and its unchecked boxes remain unchanged.

### Owner decision — verbatim

> Gate 1 APPROVED for the worktree-cleanup amendment: corrected Plan v2, the reviewed six-file publication candidate, choices E.1–E.5, and the drafting repairs as written at PLANNING.md:3901–3918. Authorized: document-only implementation in an isolated standalone clone, keeping the dirty shared checkout and private originals as they are; the specified pytest/inventory gates; independent diff review, including confirming the edit count against the patch; push; open the PR; mark it ready once required checks pass. NOT authorized: merging. Stop at "ready" and report the PR number, head SHA and check results. I'll confirm the merge separately, naming the PR. This approval authorizes no F/G operation, source selection, preservation, quarantine or deletion.

### Accepted plan and drafting repairs

The owner approved **E.1–E.5 as proposed above**, including the closed Operation F
source set with per-source outcomes, outcome-free CI wording in the stable design,
the `PREVENTION_COMPLETE` prerequisite for F/G, lineage-neutral council references,
and the six-file privacy-reviewed publication manifest. The reviewed technical-plan
candidate contains **42 edits across the two AI-workflow files and 1934 plan
lines**. Independent diff review must confirm the edit count against the actual
implementation patch; approval does not substitute for that check.

The four exact substitutions under *Corrected semantic proposal* are approved:
the F opening evaluates eligibility immediately before manifest approval; F item 1
binds the retained exact-set assessment; F item 5 rejects unresolved or nonempty
archive-ref need and rechecks before capture; and S16 binds those records and the
protected inventory to the approval. They modify text within Edit N and S16, not
the number of base-file edit locations. No source is selected or made approvable
by this document approval. A source requiring ref creation needs a separate
reviewed plan and approval.

### Implementation location and required gates

Implementation is underway in the new isolated standalone clone. The manager
reports upstream base `207f5c3c` and verified object-store independence. The dirty
shared checkout and its private originals remain outside this implementation's
write scope. This product-manager record is written only in the standalone clone's
public council artifact.

At this record's creation, the specified targeted workflow-contract pytest,
inventory `--check`, independent diff review and edit-count confirmation, PR,
and required PR checks are **pending**. Their actual outcomes must be recorded
from subsequent evidence; this approval records no passing test or CI result.
The applicable isolation, runtime/temp/cache/bytecode redirects, pinned-base,
link, privacy and candidate-integrity checks continue to apply.

### Terminal boundary — stop at ready, do not merge

The owner authorizes the document-only implementation, specified gates, independent
diff review, push, opening the PR, and marking it ready after required checks pass.
The owner expressly withholds merge authority. The earlier proposal to "land the
PR" is superseded by this narrower decision. Stop at ready and report the PR
number, exact head SHA and check results. A later merge requires the owner's
separate confirmation naming that PR.

This record does not declare the amendment landed or closed. It commissions no
F/G operation, selects no source or target, decides no early rescue, changes no
historical baseline, and grants no preservation, relocation, quarantine or deletion.

**Gate 1 approved. Implementation gates and PR readiness pending. Merge forbidden
until separate owner confirmation naming the PR.**

### 2026-10-29 — Local implementation gates and independent diff review

**Local implementation verification passed. PR readiness is still pending.** The
object-independent standalone clone uses upstream base `207f5c3c`, with runtime,
temporary and cache paths redirected to scratch. The manager records:

- `pytest tests/test_agent_workflow_contracts.py -q`: **109 passed in 18.69s**.
- Inventory `--check`: **"Test inventory is up to date"**; no regeneration.
- Shared-checkout HEAD, index, tracked diff, status, and the five original-file
  hashes match the preimplementation capture. The shared checkout and private
  originals were preserved.

The independent review below confirms the actual staged patch, including its
logical edit count. Four intentional Markdown hard-break whitespace warnings are
retained to preserve the verbatim historical quotations.

#### Independent diff review — verbatim

**Independent diff review passed; no blocking findings.** Reviewer: `/root/implementation_review`.

- Reconstructed the approved edits from Git base and compared actual staged blobs: **41 technical-plan edits + 1 INDEX edit = 42 logical edits**, producing **1,934 plan lines**. Git reports 41 zero-context hunks; hunks are not logical edits.
- Exactly **six staged files**. Five match approved candidate bytes; the council retains its approved public prefix plus the exact owner approval and bounded implementation record.
- Checked **81 active relative links**; none unresolved. Public machine-local path scan is clear.
- Scope remains document-only. The recorded approval expressly prohibits merging and grants no F/G execution authority.
- The four whitespace warnings are intentional Markdown hard breaks inside verbatim reviewer text, not defects requiring altered quotations.

Inspected the recorded **109 passing pytest tests** and clean inventory check. I ran no tests, accessed no database, and changed no files or Git state.

#### Remaining publication boundary

Push, PR creation and CI are pending at this record's creation. Source preparation
and the local implementation gates are complete; ready status requires the PR's
required checks to pass on its exact head. This record declares neither readiness
nor merge, landing or amendment closure. The owner-required report must identify
the PR number, exact head SHA and check results. Merge remains expressly forbidden
until separate owner confirmation naming that PR. No operation or source-selection
authority is added.
