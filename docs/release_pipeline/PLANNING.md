# Plan Review — Release/tag pipeline, Packet R1

*Planning size: **Large / new workflow** under [QUALITY_GATE.md](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) — a new CI workflow with new trigger surfaces. Gate 0 + Gate 1 both required, both signed.*

---

## Section 0 — Requirements Brief

**Raw request** (verbatim)

> Proceed with Packet R1 only and write Section 0 of
> docs/release_pipeline/PLANNING.md. Stop at Gate 0. Do not edit implementation
> files.
>
> Owner decisions:
> - D1: (a) — release tags are exact `v<APP_VERSION>` tags on main; version is
>   bumped manually in utils/version.py and package.json in the release PR.
> - D2: (a) — reuse the successful Windows visual comparison through provenance.
> - D3: (a) — keep visual-linux out of the release gate. Revisit only after the
>   2026-08-17 run and at least 3 consecutive green scheduled runs.
> - D4: (b) — consider Packaged Smoke for branch protection after exactly 10
>   consecutive green runs using its final composite check name.
> - D5: (b) — frozen × historical-schema coverage is a separate follow-up packet.
> - D6: (a) — `release-${{ github.ref }}`, `cancel-in-progress: false`.
>
> Before drafting Section 0, reconcile these issues explicitly:
>
> 1. The proposed acceptance test uses `v3.0.1-rc0`, but an exact
>    tag/version guard cannot accept that while APP_VERSION is `3.0.1`.
>    Do not weaken the production invariant silently. Define a coherent RC/dry-run
>    testing scheme and distinguish it from a publishable release tag.
>
> 2. The diagram mentions `workflow_dispatch (ref, dry_run)`, but the proposed
>    scope does not define those inputs or their semantics. Specify:
>    - how the target SHA is resolved;
>    - how version validation behaves in dry-run mode;
>    - whether a tag must exist;
>    - which ref is used in the concurrency group;
>    - which SHA the provenance query examines.
>
> 3. Define duplicate check-run handling. A stale successful run on the same SHA
>    must not mask a newer failed run with the same context name. Specify the
>    GitHub API filtering, pagination, selection rule, polling deadline, and
>    failure diagnostics.
>
> 4. Include the required workflow permissions, especially `checks: read` and
>    `contents: read`, in the contract.
>
> Preserve all previously stated Packet R1 constraints, especially:
> - do not touch `.github/workflows/deep-gate.yml`;
> - do not rename or convert any of the 11 required jobs to `uses:`;
> - no `--update-snapshots`;
> - no port 5000 in new jobs;
> - do not claim the scheduled deep gate is runtime-validated.
>
> In Section 0, turn the decisions and the reconciled behavior into testable
> requirements and acceptance criteria. Surface any remaining genuinely
> owner-blocking question, but do not begin implementation.

**Problem**

There is no release process. `ci.yml` triggers on `push: [main, develop]` and
`pull_request` only, so **a tag push runs nothing at all** — no build, no smoke, no
check of any kind. The frozen Windows executable that an end user actually
double-clicks is validated in two places (`ci.yml`'s `packaged-smoke-windows` and
`deep-gate.yml`'s `frozen-windows`), neither of which is tied to shipping, and the
build definition is duplicated between them. Nothing establishes, at the moment a
version is declared shippable, that the declared version matches the code, that the
shipped commit ever passed the pipeline, or that the packaged artifact starts.

The failure this must prevent is not a red gate. It is a **green gate that proves
nothing** — a release marked good because a job silently skipped, because a stale
successful check-run on the same commit masked a newer failed one, or because the
workflow never triggered and therefore never reported.

**Calculation surface**

`none`. This packet touches no module under `utils/` that participates in Effective
Sets, RIR/RPE, weekly/session summary, progression, fatigue, or volume distribution.
The only Python added is a CI provenance query script that reads the GitHub API and
writes no repository state.

---

### Reconciliation 1 — RC tags and the exact-version invariant

The prior draft's `v3.0.1-rc0` acceptance test is **withdrawn**. It cannot coexist with
D1 without weakening the guard, and the guard is the invariant.

The reconciled scheme introduces **no RC tag class at all**:

| Tag / event | Classification | Version-guard behavior |
|---|---|---|
| `v<MAJOR>.<MINOR>.<PATCH>`, strict `^v\d+\.\d+\.\d+$` | **Publishable release tag** | Strict: tag literal must equal `v` + `APP_VERSION` **and** `v` + `package.json` version |
| Any other tag matching `v*` (e.g. `v3.0.1-rc0`, `v3.0.1rc`, `vNEXT`) | **Unsupported** | Fails with an explicit message naming `workflow_dispatch` + `dry_run` as the rehearsal route |
| `workflow_dispatch`, `dry_run: true`, dispatched against a branch | **Rehearsal** | No tag identity to check; asserts internal parity and that `v<APP_VERSION>` does **not** already exist |

Rehearsal is a **dispatch**, not a tag. That is the whole reconciliation: the exact-tag
invariant is never relaxed because nothing is ever tagged for rehearsal.

The trigger pattern deliberately stays the broad `v*` rather than a narrow semver
filter. A narrow filter makes a malformed tag **silent** — nothing triggers, nothing
reports, nobody notices — which is the single failure mode this pipeline cannot detect
from inside itself. A broad trigger with a strict guard makes the same mistake **loud**.

The one thing a dispatch cannot exercise is the tag trigger itself. That is covered by
one deliberate push of a **real, strictly-valid** tag (see the blocking question below),
not by inventing a tag class the guard has to tolerate.

### Reconciliation 2 — dispatch inputs and SHA resolution

The prior draft's `ref` input is **withdrawn**. A custom `ref` input creates a
divergence hazard with no compensating benefit: the workflow *body* that executes is
always the one at the dispatched ref, so a separate `ref` input would let the pipeline
run version-guard logic from commit A against commit B. `workflow_dispatch` already
carries a built-in ref selector, and that is the resolution mechanism.

`dry_run` is the only input. Resolved behavior:

| Aspect | tag push (`refs/tags/v3.0.1`) | dispatch, branch ref, `dry_run: true` | dispatch, tag ref (any `dry_run`) |
|---|---|---|---|
| Target SHA | `github.sha` | `github.sha` | `github.sha` |
| Must a tag exist | yes — it is the trigger | **no** | yes |
| Tag-identity assertion | enforced | not applicable | **enforced** — `dry_run` is not a bypass |
| Parity assertion (`APP_VERSION` == `package.json`) | enforced | enforced | enforced |
| Additional dry-run assertion | — | `v<APP_VERSION>` must not already exist | — |
| Concurrency group | `release-refs/tags/v3.0.1` | `release-refs/heads/main` | `release-refs/tags/v3.0.1` |
| Provenance query SHA | `github.sha` | `github.sha` | `github.sha` |
| Packaged smoke, startup smokes, fan-in | run, blocking | run, blocking | run, blocking |

`dry_run` relaxes **exactly one** assertion — tag identity, and only where no tag
exists to assert against. It has no effect on any other job, and no effect at all on a
`push` event (a tag push carries no inputs and must resolve to release mode).

### Reconciliation 3 — duplicate check-run selection

A commit can carry several check-runs with the same name: a re-run creates a new
check-run, and a new check-suite can be created for the same SHA. Selecting the wrong
one lets a **stale success mask a newer failure**, which would make provenance worse
than no gate at all.

Required behavior:

- **Endpoint** `GET /repos/{owner}/{repo}/commits/{sha}/check-runs`, queried with
  `filter=all`. The API's default `latest` is **not** to be relied on — its dedupe is
  per check-suite, so it does not remove cross-suite duplicates.
- **Pagination** `per_page=100`, paging until the number of collected `check_runs`
  equals the envelope's `total_count`. The endpoint returns a wrapped object, not a
  bare array, so naive concatenation is wrong.
- **Provenance filter** only check-runs whose producing app is GitHub Actions are
  eligible. A third-party app can create a check-run with any name.
- **Selection** group eligible runs by `name`; within a group select the maximum by
  `(started_at, id)`, `id` breaking ties as the monotonic key. Exactly one run per
  expected name is then evaluated.
- **Pending** a selected run with `status != "completed"`, or an expected name with no
  run at all, counts as *pending* — never as pass and never as immediate failure.
- **Deadline** poll at 30-second intervals for up to **45 minutes**, inside a
  50-minute job timeout. *(This supersedes the 10-minute figure in the design memo,
  which was wrong: tagging immediately after a merge means `ci.yml`'s own E2E jobs may
  still be running, and an 8-minute deadline would red a healthy release.)*
- **Verdict** pass only when every expected name has a selected run with
  `conclusion == "success"`.
- **Diagnostics** on any failure or deadline, print one row per **expected** name —
  name, status, conclusion, id, `started_at`, `html_url` — plus, for every name that
  had more than one eligible run, the count and the id selected, plus a separate list
  of unexpected extra names as information only.

### Reconciliation 4 — permissions

Least privilege, declared explicitly rather than inherited:

| Scope | Permissions |
|---|---|
| `release.yml` workflow default | `contents: read` |
| `ci-provenance` job | `contents: read`, `checks: read` |
| `_packaged-windows.yml` reusable workflow | `contents: read` |

No job in either new file receives any `write` permission. This pipeline **gates; it
does not publish** — it creates no GitHub Release, uploads no release asset, and
pushes nothing. That is what keeps `contents: read` honest, and it is also why the
rehearsal tag in the blocking question below can be deleted without retracting
anything.

---

**Acceptance criteria**

*Version and tag identity (D1, Reconciliation 1)*

1. Given `APP_VERSION` is `3.0.1` and `package.json` is `3.0.1`, when tag `v3.0.1` is
   pushed, then `version-guard` passes.
2. Given `APP_VERSION` is `3.0.1`, when tag `v3.0.2` is pushed, then `version-guard`
   fails and its output names both the tag and the two version sources it compared.
3. Given `APP_VERSION` and `package.json` disagree, when any release run starts, then
   `version-guard` fails — independently of the tag, so the failure is attributable.
4. Given tag `v3.0.1-rc0` is pushed, when the workflow triggers, then it **does**
   trigger (it is not silently filtered out) and `version-guard` fails with a message
   directing the reader to `workflow_dispatch` with `dry_run`.
5. Given `version-guard` fails, when the run continues, then every other job still
   executes and reports — no `needs` short-circuit hides the rest of the gate.

*Dispatch semantics (Reconciliation 2)*

6. Given a dispatch against `main` with `dry_run: true`, when `version-guard` runs,
   then it asserts `APP_VERSION == package.json` and asserts that tag `v<APP_VERSION>`
   does not already exist, and it does not require any tag to exist.
7. Given a dispatch against a **tag** ref with `dry_run: true`, when `version-guard`
   runs, then tag identity is enforced exactly as on a tag push — `dry_run` is not a
   bypass.
8. Given a tag push (no inputs supplied), when `dry_run` is evaluated, then it resolves
   to release mode.
9. Given any event, when provenance runs, then the SHA it queries is `github.sha`, and
   no input can point it at a different commit.
10. Given a dispatch against `main` and a concurrent tag push, when both run, then their
    concurrency groups differ (`release-refs/heads/main` vs `release-refs/tags/…`) and
    neither cancels the other.
11. Given `dry_run: true`, when the run completes, then no job other than
    `version-guard` behaves differently from a release run — asserted by a contract
    test that no `dry_run` expression appears outside the `version-guard` job.

*Provenance (D2, Reconciliation 3)*

12. Given a SHA whose 12 expected check-runs all concluded `success`, when provenance
    runs, then it passes and lists all 12 with their ids.
13. Given a SHA where one expected name is absent, when the deadline expires, then
    provenance fails and the diagnostic names the missing check by its exact context
    string.
14. Given a SHA carrying two check-runs named `Run Tests` — an older `success` and a
    newer `failure` — when provenance runs, then it selects the newer one and **fails**.
15. Given the reverse (older `failure`, newer `success` from a re-run), when provenance
    runs, then it selects the newer one and passes. *(Run both directions; a rule that
    only catches one is indistinguishable from an unconditional one.)*
16. Given more than 100 check-runs on the SHA, when provenance queries, then it
    paginates to `total_count` and does not truncate.
17. Given a check-run with an expected name produced by an app other than GitHub
    Actions, when provenance selects, then that run is ineligible.
18. Given an expected check-run still `in_progress`, when provenance polls, then it
    keeps polling and never treats a non-`completed` status as a pass.
19. Given the tagged SHA never ran `ci.yml` at all, when the 45-minute deadline
    expires, then provenance fails listing all 12 as never reported.
20. Given the expected-name list, when a contract test compares it to the 11 branch
    protection contexts plus `Visual Regression (Windows baselines)`, then they match
    exactly — deleting a name from the workflow reds pytest before it can red a release.

*Anti-false-green (fan-in)*

21. Given any job in the release workflow concludes anything other than `success`
    (including `skipped` and `cancelled`), when `release-gate` runs under
    `if: always()`, then it fails and names the offending job.
22. Given a job id is removed from `release-gate`'s `needs`, when the contract test
    compares the key set of `toJSON(needs)` against the other job ids in the file, then
    the test fails. The same test fails when a phantom name is added to the expected set.
23. Given a guard step inside any job is skipped, when its job completes, then the job
    fails — every guard step carries an `id` and `if: always()`, and its job asserts
    `steps.<id>.outcome == 'success'`.

*Reuse, ports, and preserved contracts*

24. Given the packet is complete, when the frozen Windows build+smoke definitions are
    counted across all workflow files, then there are exactly **two**
    (`_packaged-windows.yml` and `deep-gate.yml`'s untouched `frozen-windows`) — never
    three. *(**Superseded by Packet R2-b**, which converted `frozen-windows` and moved
    the count to exactly **one** definition with **three** callers. The criterion's
    intent — never a third copy — is unchanged and now enforced more strictly; see the
    R2-b section at the end of this file.)*
25. Given `ci.yml` after the edit, when its `packaged-smoke-windows` job `name:` is
    read, then it is byte-identical to `Packaged Smoke (Windows bootloader, non-required)`.
26. Given `ci.yml` after the edit, when every job whose `name:` appears in the 11
    required contexts is inspected, then each still uses `steps:` and none uses `uses:`.
27. Given every job in the two new files, when timeouts are inspected, then each
    declares `timeout-minutes`, or — for a `uses:` job, which cannot declare one — passes
    it as an input to a reusable workflow that does.
28. Given every new or edited job, when its port configuration is read, then no value is
    `5000`; the packaged smoke uses `5123` and the two startup smokes use distinct
    non-5000 ports via `HT_PORT`.
29. Given all workflow files, when searched for `--update-snapshots`, then there are zero
    occurrences.
30. Given `deep-gate.yml`, when the packet's diff is inspected, then that file is
    unchanged.
31. Given `release.yml`, when its `concurrency` block is read, then the group contains
    `github.ref` and `cancel-in-progress` is `false`.
32. Given both new files, when every `permissions:` block is read, then no scope is
    granted `write`, and `ci-provenance` declares `contents: read` and `checks: read`.
33. Given the packet adds test files, when `scripts/generate_test_inventory.py --check`
    runs, then it passes against a regenerated, committed `docs/test_inventory/`.

**In scope**

- `.github/workflows/_packaged-windows.yml` — new `workflow_call` reusable workflow
  holding the frozen build + bootloader smoke, with `port` (default `5123`), `runner`,
  and `timeout-minutes` (default `45`) inputs. Body lifted from the existing
  `packaged-smoke-windows` job, comments included.
- `.github/workflows/release.yml` — new. Triggers `push: tags: ['v*']` and
  `workflow_dispatch` (`dry_run` only). Jobs: `version-guard`, `ci-provenance`,
  `packaged-windows` (calls the reusable workflow), `startup-smokes` (matrix:
  first-install, old-db-migration), `release-gate` (fan-in).
- `.github/workflows/ci.yml` — modify **only** the `packaged-smoke-windows` job body to
  call the reusable workflow. Its `name:` is untouched.
- `scripts/check_release_provenance.py` — new; the pagination, eligibility, selection,
  polling and diagnostics logic of Reconciliation 3, in Python so it is unit-testable
  rather than inline shell.
- `tests/test_release_workflow_contracts.py` — new; static YAML contracts (criteria
  20, 22, 24–32).
- `tests/test_release_provenance.py` — new; unit tests over the selection rule against
  fixture payloads (criteria 12–19), run in both directions.
- `docs/RELEASE_CHECKLIST.md` — new; the 10-minute manual layer
  (plan → log → summary → progression → backup/restore → erase) that
  `TESTING_STRATEGY_PLANNING.md` §5 has owed since 2026-08-01. Its **first** step is
  "confirm a run exists for this tag", the only available defense against a trigger that
  never fires. It also records that `main` must be green before tagging.
- `docs/test_inventory/TEST_INVENTORY.json` + `.md` — regenerated, never hand-edited.
- `docs/DECISIONS.md` — ADR recording D1, D6, and the three tag classes.
- `docs/TESTING_STRATEGY_PLANNING.md` — Phase 4 step 13 status only.
- `docs/ai_workflow/QUALITY_GATE.md` — one rule: converting a job to `uses:` renames its
  check to `parent / child`; never do it to a job in branch protection.
- This file.

**Out of scope / non-goals**

- `.github/workflows/deep-gate.yml` — **not touched under any circumstance.** A
  scheduled workflow executes the default branch's HEAD copy, so merging any edit before
  2026-08-17 03:17 UTC would mean the first scheduled run validates a different file than
  the one that shipped. Converting `frozen-windows` to the reusable workflow, and the B9
  `concurrency:` decision, are Packet R2.
  *(Scoped to R1. One narrow exception was taken later by **Packet R2-a**, 2026-08-15,
  for the `&&` assertion only — see residual **R-9**. The `frozen-windows` conversion
  is **Packet R2-b**, implemented 2026-08-15 and **merged 2026-08-16 as #388** under an
  owner override of the hold — see the R2-b section at the end of this file. The
  B9 `concurrency:` decision is still **not started**.)*
- `visual-linux` in the release gate (D3) — revisit only after the 2026-08-17 run and
  ≥3 consecutive green scheduled runs. *(The binding clause is the three green scheduled
  runs. **One has now occurred** — 2026-08-17, green (run 31993105305). Whether it counts
  toward the three is an **open owner question**: it ran R2-b's file, not the pre-#388
  one. Measure the count rather than reading it here; see the R2-b section
  → *Next clean checkpoint*.)*
  ⚠️ **UPDATED 2026-08-24 — the "open owner question" clause above is RETIRED as live
  guidance, and the clock is recorded at 2 of 3.** The sentence is kept because it was
  written in good faith on 2026-08-17, but it must not be acted on. **The question is now
  SETTLED by an owner ruling dated 2026-08-24, recorded in
  [`DECISIONS.md`](../DECISIONS.md) ADR-007 under R1-D3: the 2026-08-17 run COUNTS.** That
  ADR is the authority for this reading; do not re-derive it from the paragraphs below.
  Until that ruling the question had been *raised* in exactly three places — this bullet,
  ADR-007, and [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md)'s R1 block — and **answered
  nowhere**, which is why it was recorded rather than inferred. The reasoning behind it,
  kept for the reader and not as the authority: the binding text is the
  owner's D3 exactly as Section 0 of this file records it — *"Revisit only after the
  2026-08-17 run and at least 3 consecutive green scheduled runs"* — which **names** the
  2026-08-17 run as a milestone and nowhere excludes it from the count; and this file's own
  **2026-08-17 supersession** (*Next clean checkpoint*, below) already reads 2026-08-24 as
  **the second** consecutive green scheduled run. The contamination that prompted the
  question was an objection about the *pre-#388 file*, which no longer exists on `main`; it
  was never an objection to counting the run. **Measured 2026-08-24, not inferred:**
  `gh run list --workflow=deep-gate.yml --event=schedule` returns exactly **two** runs
  repo-wide, **both `success`** — `31993105305` (2026-08-17) and `32688747703`
  (2026-08-24). **The clock stands at 2 of 3; the third is due 2026-08-31 03:17 UTC.**
  Only a fresh owner ruling superseding the 2026-08-24 one could move that — discounting
  the first run would put the clock at **1 of 3** with the third due 2026-09-07.
  **D3 itself stays deferred regardless: nothing here puts `visual-linux` into the release
  gate, and closing the clock is not the same as acting on it.** Full job-level record: § *The
  second `schedule`-event run — 2026-08-24* at the end of this file.
- Frozen × historical-schema coverage (D5) — separate follow-up packet; it needs a
  `--legacy-db` argument on `scripts/smoke_packaged_app.py` and its own tests.
- Any branch-protection API change. D4's promotion of `Packaged Smoke` happens after 10
  consecutive green runs under its **composite** name, as a separate deliberate step.
- Creating a GitHub Release, uploading the built executable as a release asset, changelog
  generation, code signing, or any form of publishing or distribution.
- Adding a tag trigger to `ci.yml`.
- Re-running the 11 required contexts on the tag. D2 reuses the runs; that is the point.

**Assumptions made**

- ⚠️ The 11 required contexts were read live on 2026-08-14 from
  `gh api …/branches/main/protection/required_status_checks`. Branch protection can
  change outside this packet; the contract test pins the list as the packet's
  understanding, and a future change to protection will red that test deliberately.
- ⚠️ All 12 expected contexts are produced as GitHub **check-runs** (Actions jobs), not
  legacy commit statuses. If any were a commit status, the check-runs endpoint would not
  see it and provenance would report it missing. Believed true because all 12 are
  Actions jobs, but not separately verified against a live SHA.
- ⚠️ `filter=latest` on the check-runs endpoint dedupes per check-suite rather than
  globally. The design **avoids depending on this** by using `filter=all` with an explicit
  selection rule, so the assumption is defused rather than relied on.
- ⚠️ `github.sha` on an annotated-tag push resolves to the tagged **commit**, not the tag
  object, so the check-runs query finds the commit's checks.
- ⚠️ The 45-minute provenance deadline is derived from `ci.yml`'s slowest job timeout
  (`E2E Functional Shard`, 45 min), not from measured tag-push-after-merge latency. It is
  a hang detector, not a budget, following the #325 precedent.
- ⚠️ A `uses:` job accepts only `name`, `needs`, `if`, `permissions`, `with`, `secrets`,
  `strategy`, `concurrency` — not `timeout-minutes`, `runs-on`, `env`, or
  `continue-on-error`. Neither converted job uses `continue-on-error` today, so nothing is
  lost, but this shapes the reusable workflow's input list.
- ⚠️ Converting `packaged-smoke-windows` to `uses:` changes its check name to
  `Packaged Smoke (Windows bootloader, non-required) / <called job name>`. Safe **only**
  because that job is not in branch protection — verified against the live list. D4's
  10-run count therefore starts at the composite name, not before.
- ⚠️ Adding `scripts/check_release_provenance.py` routes this packet through
  QUALITY_GATE's `scripts/**` row, whose stem search will find the new test file and so
  produce a **non-empty** union — which suppresses the `/verify-suite` fallback. This
  packet nonetheless requires a full `/verify-suite`, because it edits `ci.yml` and
  changes the committed test inventory. Stated here so it is a decision, not an accident.
- ⚠️ The weekly scheduled deep gate is **implemented but not runtime-validated**. No
  scheduled execution has occurred; the first is due 2026-08-17 03:17 UTC. Nothing in this
  packet depends on it, and nothing in this packet may be read as validating it.

**Open questions for the user**

1. **Blocking — how is the tag trigger itself proven, and with which tag?**
   `APP_VERSION` is `3.0.1` and no release tag exists, so under D1 the only tag the guard
   can currently accept is `v3.0.1`. Acceptance criteria 1 and 4 require pushing a real tag
   to the repository — an outward-facing action this packet will not take unattended.
   Three routes:
   - **(a)** Push `v3.0.1` on a `main` SHA as the rehearsal, inspect the run, then delete
     the tag. Safe under this design because the pipeline publishes nothing, but it does
     mean the first real `3.0.1` release re-pushes a previously-deleted tag.
   - **(b)** Bump to `3.0.2` in the release PR and reserve `v3.0.1` purely as the
     throwaway rehearsal tag.
   - **(c)** Accept that the tag-trigger path stays unproven until the first genuine
     release, and validate everything else by `workflow_dispatch` dry-run.

   All other reconciliations are settled; this is the only decision the packet cannot make
   for itself.

### Section 0 sign-off — GATE 0
- [x] User confirms the acceptance criteria match intent.
- [x] User reviewed the assumptions and corrected or accepted each one.
- [x] Blocking questions are answered.

**GATE 0 APPROVED — 2026-08-14, owner.** The blocking question is answered with
**option (c)**:

> Do not create or delete a rehearsal tag. Validate through `workflow_dispatch` with
> `dry_run: true`. Leave the real tag-trigger path explicitly unproven until the first
> genuine release. Do not weaken the exact `v<APP_VERSION>` production invariant.

**Consequence for the acceptance criteria.** Criteria 1, 2 and 4 assert behavior on a
tag push. Under (c) no tag is pushed, so they are **not executable in this packet**.
They are not deleted and not weakened: they are re-classified as *deferred-to-first-release*
and each gains a **static** counterpart that is executable now — the guard logic is
exercised directly through its unit tests (the same code the workflow calls), and the
workflow's trigger block is asserted by a contract test. This preserves the invariant
while being honest that the GitHub-side trigger wiring is unproven. See the residual
register in Plan v2.

---

## Live re-verification (2026-08-14, before planning)

The owner required GitHub-dependent assumptions to be re-verified rather than trusted.
Executed against the live repository:

| Assumption | Command | Result |
|---|---|---|
| 11 required contexts, exact strings | `gh api …/branches/main/protection/required_status_checks --jq '.contexts[]'` | **Confirmed, 11**, byte-identical to Section 0's list |
| The 12 expected names all exist as check-runs on a completed `main` SHA | `gh api …/commits/5a03d47/check-runs?filter=all` | **Confirmed** — 18 check-runs, all `success`, all 12 expected names present |
| All are produced by GitHub Actions | `… --jq '[.check_runs[].app.slug]|unique'` | `["github-actions"]` — the app-eligibility filter is meaningful, not theoretical |
| The response is a wrapped envelope needing pagination | same | `{total_count, check_runs[]}` confirmed; 17–18 runs per SHA today, under one page |
| `filter=latest` vs `filter=all` | both, on three completed SHAs | **Identical counts (18/18) on every SHA sampled** — no live duplicate exists to distinguish them |

**Two findings that changed the plan:**

1. **`E2E Functional (Chromium)` materializes late.** On the in-flight SHA `a64ea76`,
   `filter=all` returned 17 check-runs and that name was **absent** — only
   `E2E Functional Shard 1/2` and `2/2` existed, still `in_progress`. The fan-in gate is
   a job with `needs:`, so its check-run is not created until its dependencies finish.
   This is live proof that *"expected name absent"* must mean **pending**, never
   **failure** — a design that failed fast on a missing name would red every release
   tagged promptly after a merge. Section 0 criterion 13 already required this; the
   evidence promotes it from prudence to necessity.
2. **The duplicate scenario cannot be reproduced live.** No sampled SHA carries two
   check-runs with one name, so `filter=all` and `filter=latest` are empirically
   indistinguishable here. The selection rule is therefore justified *by construction*
   and can only be tested against synthetic fixtures. Recorded as a residual: this packet
   asserts the rule's behavior, not that GitHub produces the shape it defends against.

---

## Plan v1

**Goal**: A tag push or dispatch of `release.yml` either proves — on the exact commit
being shipped — that the version is coherent, that commit passed the full PR pipeline,
the frozen Windows executable builds and starts, and a fresh and an upgraded database
both boot; or it goes red. It cannot go green with a job skipped, a stale check-run, or
a missing report.

**Scope**

- **In**: the twelve artifacts in the table below; Packet R1 as approved at Gate 0.
- **Out**: `deep-gate.yml` (Packet R2); `visual-linux` on release (D3); frozen ×
  historical-schema (D5); any branch-protection change (D4); tag creation/deletion;
  GitHub Releases, asset upload, publishing, signing; a tag trigger on `ci.yml`;
  re-running the 11 required contexts on the tag.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `.github/workflows/_packaged-windows.yml` | new | `workflow_call`; inputs `port` (5123), `runner` (`windows-latest`), `timeout-minutes` (45); `permissions: contents: read`; body lifted from `packaged-smoke-windows` with its comments |
| `.github/workflows/release.yml` | new | `push: tags: ['v*']` + `workflow_dispatch` (`dry_run` only); 5 jobs; `concurrency: release-${{ github.ref }}`, `cancel-in-progress: false` |
| `.github/workflows/ci.yml` | modify | `packaged-smoke-windows` body → `uses:`. `name:` byte-identical. No other job touched. |
| `scripts/release_gate.py` | new | Two subcommands, `version` and `provenance` — the whole gate's decision logic in tested Python rather than untested inline shell |
| `tests/test_release_gate.py` | new | Unit tests over both subcommands, including both directions of the duplicate-selection rule |
| `tests/test_release_workflow_contracts.py` | new | Static YAML contracts (Section 0 criteria 11, 20, 22, 24–32) |
| `docs/RELEASE_CHECKLIST.md` | new | The 10-minute manual layer; step 1 is "confirm a run exists for this tag" |
| `docs/test_inventory/TEST_INVENTORY.json` / `.md` | regen | Two new test files change node counts |
| `docs/DECISIONS.md` | modify | ADR: D1, D6, the three tag classes, and option (c) |
| `docs/TESTING_STRATEGY_PLANNING.md` | modify | Phase 4 step 13 status only |
| `docs/ai_workflow/QUALITY_GATE.md` | modify | One rule: `uses:` renames a check to `parent / child`; never for a protected job |
| `docs/release_pipeline/PLANNING.md` | this file | Section 0, council record, Plan v2 |

**Job design**

| Job | Runner | timeout | Purpose |
|---|---|---|---|
| `version-guard` | ubuntu-latest | 10 | `release_gate.py version` — parity + tag identity per the Reconciliation-2 matrix |
| `ci-provenance` | ubuntu-latest | 50 | `release_gate.py provenance` — 45-min poll deadline, 30s interval; `permissions: contents: read, checks: read` |
| `packaged-windows` | via reusable | 45 (input) | frozen build + `--mode bootloader --port 5123` |
| `startup-smokes` | ubuntu-latest, matrix ×2 | 15 | `first-install` (`HT_PORT=5124`), `old-db-migration` (`HT_PORT=5125`) |
| `release-gate` | ubuntu-latest | 5 | fan-in: literal expected `needs` key set + every result `success` |

**Sequence**

1. `_packaged-windows.yml`, then convert `ci.yml`'s job to call it. Verify by contract test that the required-context jobs are untouched.
2. `scripts/release_gate.py` + `tests/test_release_gate.py` — logic and its tests before the workflow that calls it.
3. `release.yml` wiring all five jobs.
4. `tests/test_release_workflow_contracts.py` against the finished YAML; run its mutations in both directions.
5. `docs/RELEASE_CHECKLIST.md`, then the three doc updates.
6. Regenerate the test inventory last, after every test file exists.

**Effort**: M · **Owner**: this session · **Depends on**: nothing. Explicitly *not* blocked by the 2026-08-17 scheduled run, because no artifact in this packet touches `deep-gate.yml`.

**Expected gates** (to be confirmed by `test-strategist`)
- pytest: `tests/test_release_gate.py`, `tests/test_release_workflow_contracts.py`, plus full `pytest` because the committed test inventory changes.
- e2e: **proposed none** — this packet changes no route, template, JS, CSS, or `utils/` module. Open for the council to overrule.
- other: `python scripts/generate_test_inventory.py` then `--check`.

**Open design questions carried into the council**

- **Q1** One `scripts/release_gate.py` with subcommands, or two single-purpose scripts?
- **Q2** Should the two startup smokes be extracted into a second reusable workflow now (making Packet R2 a six-line change), or stay inline in `release.yml` (smallest R1)?
- **Q3** Is a full `/verify-suite` including Chromium E2E warranted for a packet that touches no application code, or is full `pytest` + the contract tests the honest gate?
- **Q4** Does the fan-in job's expected-key-set literal belong in shell+`jq` inside the YAML, or should it too move into `release_gate.py`?

---

## Council response matrix — Gate 1

Three reviewers ran in parallel against this worktree. Every finding is answered.
**A / R / D** = Adopted / Revised-then-adopted / Declined.

### Architecture reviewer (`ac1dd79ac8a5ef591`)

| # | Finding | A/R/D | Response |
|---|---|---|---|
| A-B1 | `workflow_dispatch` cannot fire before the file is on the default branch, so `release.yml` gets **zero** runtime evidence pre-merge | **A** | Verified correct. The owner execution order already mandates a post-merge dispatch, so this is sequencing, not a defect. Added as sequence step 8 and residual **R-3**. The PR does not close the packet; the post-merge dry-run does. |
| A-B2 | Criterion 20 is literal-vs-literal and cannot catch a `ci.yml` job rename | **A** | Adopted in test-strategist's stronger form: derive one side from `ci.yml` job `name:` values. |
| A-B3 | The dry-run's only added assertion is a guaranteed false green — `checkout@v7` fetches no tags, so `git tag -l` is always empty | **A** | Verified. Replaced with `GET /git/matching-refs/tags/<tag>`, no checkout dependency. **A second defect was found here that the reviewer did not raise**: that endpoint is a *prefix* match, so an existing `v3.0.10` would satisfy a `v3.0.1` query. The implementation filters for exact `refs/tags/<tag>` equality and a unit test pins the prefix-collision case. |
| A-N1 | PyYAML unavailable; regex-over-YAML has a false-pass history here | **A** | Confirmed: absent from `requirements.txt`, `import yaml` fails in the venv. Using an indentation parser modelled on `tests/test_compiled_css_drift_gate_contracts.py:56-130`, generalized to take a path. PyYAML is **not** added. |
| A-N2 | The reusable workflow child job id is unpinned but becomes branch-protection-load-bearing under R1-D4 | **A** | Pinned as `build-and-smoke`; composite name recorded in the ADR, criterion 25 and the QUALITY_GATE rule. |
| A-N3 | Startup smokes are a rewrite, not a lift, with no duplication ceiling | **A** | Criterion 36 + cross-reference comments. See Q2. |
| A-N4 | Lifted comments carry three claims that become false in the new home | **A** | The `--mode bootloader` and non-5000-port paragraphs are kept verbatim; the "keep the two in step" and "non-required on purpose" sentences are rewritten for the reusable workflow perspective. |
| A-N5 | QUALITY_GATE has no `.github/workflows/**` row at all | **A** | Added in the edit the packet already makes to that file. |
| A-N6 | The two runtime-pin contracts parametrize over exactly two workflows | **A** | Adopted **with test-strategist's correction**: add both new files to the *python* list only. The node contract asserts `setup_count > 0` and neither new file uses `setup-node`. Verified by reading both. |
| A-N7 | Two rehearsal dispatches against `main` share a concurrency group | **R** | Group prefixed with `${{ github.workflow }}` to match the ci.yml convention. Same-ref supersession is **accepted and recorded** in the ADR — R1-D6 fixes `cancel-in-progress: false` and reshaping the key further would exceed it. |
| A-N8 | The pyright baseline diff is missing from expected gates | **A** | Added. |
| A-NIT1 | Section 0 names `check_release_provenance.py`; Plan v1 renamed it silently | **A** | Supersession recorded below. |
| A-NIT2 | Ban `github.event.inputs.dry_run`, mandate `inputs.dry_run` | **A** | Contract test asserts the ban. |
| A-NIT3 | `MASTER_HANDOVER.md` missing from the artifact table | **A** | Added. |
| A-NIT4 | Mixed `dry_run` / `timeout-minutes` input naming | **D** | Declined. `timeout-minutes` mirrors the GitHub key it feeds; `dry_run` follows this repo's own workflow inputs (`run_visual`, `visual_mode` in `deep-gate.yml`). Each convention is load-bearing in its own direction. |

### Test strategist (`a8a63e31cc3a5ff40`)

| # | Finding | A/R/D | Response |
|---|---|---|---|
| T-Q3 | Full pytest mandatory; the Chromium E2E half of `/verify-suite` is **not derivable** from any changed path | **A** | Nine pre-existing test files assert against the changed artifacts while the `scripts/**` stem union resolves to two files this packet writes itself. Local gate = full pytest + inventory regen/`--check` + pyright baseline diff + `tsc`. The E2E half is supplied by CI's own jobs, which still gate the merge — **no test is relaxed and no contract is weakened**. Residual **R-6**. |
| T-Q2 | Only the `e2e-functional-shard` spec list or a rename of that job trips the workflow-derived inventory surface | **A** | Confirmed against `scripts/generate_test_inventory.py:125-156`. Regeneration sequenced last. |
| T-B1 | The YAML contract file can go **entirely vacuous** if the parser stops matching | **A** | Vacuity floor: assert the job count in `release.yml`, 1 in `_packaged-windows.yml`, >=17 in `ci.yml` **before** any other assertion. Highest-value finding of the council. *(The `release.yml` figure as shipped is **6**, not the 5 this row originally wrote; Packet R2-b additionally pinned **7** in `deep-gate.yml`, since the floor now has to cover that file too. Read the counts off `test_the_parser_still_finds_every_job`, not off this row.)* |
| T-B2 | Criterion 28 as a negative `"5000" not in text` scan is **inverted** — deleting `HT_PORT` makes it pass more easily | **A** | Replaced with a positive assertion: each smoke leg must *set* `HT_PORT` to its named non-5000 value and its probe URL must use that same port. |
| T-B3 | Criterion 32 as `": write" not in text` passes when `permissions:` is deleted | **A** | Replaced with a positive assertion: every job in both new files declares a `permissions:` block and every scope is `read`. |
| T-B4 | Both new workflows are invisible to every runtime-pin contract | **A** | See A-N6. |
| T-fixtures | A/B are jointly insufficient — need C (id/time disagree), D (equal timestamps), E (array order), G1/G2 (eligibility), and a page-2-decisive pagination fixture | **A** | All adopted. Clock and deadline injected so the **poll loop itself** is the unit under test, not a pure helper the workflow never calls. |
| T-gap | **A genuine gap in the 33 criteria**: nothing covers a provenance verdict on `cancelled` / `skipped` / `neutral` / `timed_out` | **A** | New criterion **34**, parametrized. `conclusion == "success"` is the only pass. |
| T-Q5 #7 | Criterion 11 is satisfied maximally by dropping `dry_run` entirely | **A** | Paired with the positive: `dry_run` must appear inside `version-guard` and reach the script as an argument. |
| T-Q5 #8 | Criterion 21 must assert the `!= 'success'` operator, not the presence of `if: always()` | **A** | Adopted. |
| T-Q5 #9 | Criterion 24 counted by filename passes with "two definitions, zero callers" | **A** | Counted by command shape (`pyinstaller --clean --noconfirm` and `smoke_packaged_app.py` each exactly 2 across all workflow files) **plus** both callers asserted present. *(**Superseded by Packet R2-b**: with the inline `deep-gate.yml` copy gone the expected count is now **1** each, and the caller set is the **three** entries in `PACKAGED_CALLERS`, asserted in both directions. The counting *method* — by command shape, not by filename — is what T-Q5 #9 won, and it is unchanged.)* |
| T-Q5 #10 | Criterion 3 must not re-derive `tests/test_version.py` | **A** | The unit under test is fed two literal strings. |
| T-Q5 #11 | Criterion 23 must bind both halves | **A** | For every step declaring an `id:`, a later step in the same job must reference `steps.<id>.outcome`. |
| T-Q5 #12 | Criterion 29 over two files is vacuous by construction | **A** | Scans all four workflow files. |
| T-NIT13 | The empty-string `dry_run` a push event produces is the highest-value untested input | **A** | Explicit unit test. |
| T-static | Static substitutes for deferred criteria 1/2/4, incl. pinning the anchored `^v\d+\.\d+\.\d+$` regex and asserting the trigger is **not** semver-narrowed | **A** | Adopted; stronger than what Section 0 had. |
| T-30 | Criterion 30 substitute via the `test_consult_adapter.py:1066-1077` precedent | **A** | Assert `deep-gate.yml` still contains its five load-bearing strings **and** contains no `uses: ./.github/workflows/_packaged-windows.yml`. That negative catches R2 creep. *(**Both tests deleted by Packet R2-b**, which is the R2 they were guarding against — the negative had done its job. The underlying intent, that deep-gate's packaged-artifact guarantee is pinned somewhere, is discharged instead by `PACKAGED_CALLERS` and `test_the_weekly_gate_still_smokes_a_real_bootloader_on_windows`.)* |
| T-collect | Neither new test file may make its **collection** host-dependent | **A** | No `importorskip`, no glob-parametrization over `.github/workflows/*.yml`; explicit literal lists only. |

### Product-risk reviewer (`af59ffce656209012`)

| # | Finding | A/R/D | Response |
|---|---|---|---|
| P-B1 | The residual register is a dangling forward reference | **A** | Written below, six rows. |
| P-B2 | The Plan v1 Goal asserts a tag path that never ran, and implies the *frozen* build is proven against a historical schema when it is not | **A** | Goal rewritten. A real overstatement; the correction is material. |
| P-B3 | The TESTING_STRATEGY edit is under-scoped; four locations claim deferral and §7.3 entry criteria 2 and 3 stay unmet | **A** | All four locations updated plus a new §8.1b. Step 13 states verbatim that Phase 4 **remains open**. The "no scheduled run has executed yet" sentences are preserved **verbatim**. |
| P-B4 | The checklist erase step destroys the owner's live training data and every in-DB backup | **A** | Highest-severity finding. `HT_RUNTIME_DIR` isolation is mandatory step 0, and the checklist records that erase drops the backup tables so backup/restore is re-verified after it. |
| P-B5 | The checklist covers 5 of 7 core workflows; `/user_profile` has zero coverage in the frozen artifact *and* the manual layer | **A** | Extended to all seven using CLAUDE.md canonical vocabulary. |
| P-B6 | The criterion-20 assumption claims a defense that cannot exist offline | **A** | Reworded to claim only in-repository drift, plus a checklist step to re-read live protection before tagging. |
| P-B7 | No criterion pins the smoke **argv** across the lift — adding `--skip-upgrade` would pass all 33 criteria while deleting the only automated upgrade proof | **A** | New criterion **35**. |
| P-B8 | The startup smokes are the only place `program_backups` survival after a schema upgrade is asserted | **A** | New criterion **36**: the release copy required-table/column sets must be a **superset** of deep-gate's, both parsed from source. |
| P-B9 | `MASTER_HANDOVER.md` missing | **A** | Added. |
| P-N1 | The calculation-surface rationale sentence is stale against the renamed script | **A** | Rewritten. Verdict `none` unchanged and independently confirmed. |
| P-N2 | This packet's D1-D6 collide with TESTING_STRATEGY's own D1-D7 | **A** | Namespaced **R1-D1 … R1-D6** everywhere. |
| P-N3 | §8.1a signed the deferral; the supersession has no recorded home | **A** | §8.1b names §8.1a explicitly. |
| P-N4 | The ADR omits R1-D2 and R1-D3 | **A** | Both added with their residuals. |
| P-N5 | Q3 reopens a question Section 0 already decided | **A** | Resolved as a recorded supersession, not a silent change. |
| P-N6 | Artifact renames diverge from Gate-0 scope without a note | **A** | Recorded below. |
| P-N7 | The `runner` input is unused and would let a non-Windows runner produce a passing smoke of a different artifact | **A** | **Input dropped**; `runs-on: windows-latest` hard-coded. |
| P-D2 | D2's real trade is undisclosed: a re-run-to-green counts, and `Visual Regression` is not a protected context so `main` can merge with it red | **A** | Residual **R-4**. "Green before tagging" is defined as **all 12** expected contexts, not the 11 required. |
| P-(c) | Option (c) is under-disclosed in the three places a reader actually reaches | **A** | Header comment in `release.yml`, reason-carrying step 1 in the checklist, and the step-13 wording — all three adopted close to verbatim. |
| P-NIT | Name both summary pages; assert the Effective/Raw side-by-side contract; use canonical vocabulary | **A** | Adopted. |

### Open questions — resolved

- **Q1 → one `scripts/release_gate.py` with subcommands.** Unanimous. The expected-context list must be a single importable constant shared by the runtime and the contract test; splitting duplicates that literal. `QUALITY_GATE.md:102` routes `scripts/**` by file stem, so one stem is unambiguous where three give three chances for the union to go shallow.
- **Q2 → startup smokes stay inline in `release.yml`.** Extraction does **not** reduce R1's duplication count (a one-caller reusable workflow plus deep-gate's untouched pair is still two semantic copies) while adding a second `workflow_call` contract and permissions surface. Paired with criterion 36 and cross-reference comments.
- **Q3 → full pytest; no locally-derived E2E.** See T-Q3.
- **Q4 → the fan-in assertion moves into `release_gate.py`.** `toJSON(needs)` interpolated into YAML shell is a quoting hazard and forces the contract test to regex shell-inside-YAML. `needs` JSON is passed via `env:` to a `fan-in` subcommand whose expected job-id set is a module constant the contract test imports and compares against job ids parsed from `release.yml` — a two-source cross-check.

### Supersessions of the Gate-0-approved Section 0

Recorded so the diff is not read as scope creep. None expands the packet.

1. `scripts/check_release_provenance.py` → **`scripts/release_gate.py`** (three subcommands); `tests/test_release_provenance.py` → **`tests/test_release_gate.py`**.
2. Section 0's assumption that a full `/verify-suite` including Chromium E2E is required is **superseded** by T-Q3. Its reasoning (ci.yml edit + inventory change) survives and is exactly why *full* pytest rather than a targeted subset is required.
3. Criteria 1, 2 and 4 are deferred by owner option (c) with static substitutes. Criteria **34, 35, 36** added by the council.
4. `_packaged-windows.yml` has **no inputs at all**. The `runner` input was dropped at
   council (P-N7); `port` and `timeout-minutes` were dropped during the post-implementation
   unslop review once measurement showed no caller varies either — `deep-gate.yml`'s
   `frozen-windows` also uses 45 minutes and passes no `--port`. Both values are now
   literals inside the reusable workflow. *(**Partly superseded by Packet R2-b.** "No
   caller varies either" was true of the timeout and false of the port: passing no
   `--port` means the script's default **5000**, not the literal **5123** in the reusable
   workflow. Dropping the input was still right, but the consequence is that R2-b's
   conversion changes deep-gate's smoke port. See the R2-b difference table below.)*
5. Section 0's `startup-smokes` matrix (two legs) shipped as **two discrete jobs**,
   `first-install` and `old-db-migration`. A matrix would have needed a per-step `if:`
   to select the leg's body, and a conditional step is exactly what the anti-skip
   contract forbids. This is why `RELEASE_JOB_IDS` has five entries and the fan-in
   expects five rather than four.
6. Section 0 criterion 23 (`every guard step carries an id and if: always()`) is
   **replaced**, not merely extended. No step in either new workflow declares an `id:`,
   which would have made that contract vacuous. The executable form is the stronger
   inverse: *no step may carry a skip-capable `if:` at all* — only `failure()`
   diagnostics may be conditional.

---

## Plan v2 — approved for implementation

**Goal** (rewritten per P-B2). A **dispatch** of `release.yml` proves, on the exact commit
under test, that the two version sources agree, that this commit's 12 expected CI
check-runs all concluded success, that the frozen Windows executable builds and starts
from a fresh runtime, and that a source checkout boots both a freshly-seeded database
and a historical-schema one. A **tag push** is expected to do the same, but **that
trigger path has never executed** (owner option (c)). The frozen executable is proven
to build and start; it is **not** booted against a historical schema — that is R1-D5,
deferred.

**Artifacts** (14; supersedes the Plan v1 table)

| Path | Change |
|---|---|
| `.github/workflows/_packaged-windows.yml` | new — `workflow_call`, inputs `port` (5123) and `timeout-minutes` (45), no `runner` input, `runs-on: windows-latest`, job id `build-and-smoke`, `permissions: contents: read` |
| `.github/workflows/release.yml` | new — 5 jobs, option-(c) header comment, `concurrency: ${{ github.workflow }}-release-${{ github.ref }}` / `cancel-in-progress: false` |
| `.github/workflows/ci.yml` | modify — `packaged-smoke-windows` body → `uses:`; `name:` byte-identical; no other job touched |
| `scripts/release_gate.py` | new — subcommands `version`, `provenance`, `fan-in`; stdlib HTTP only; injectable clock |
| `tests/test_release_gate.py` | new — unit tests incl. all council fixtures, both directions |
| `tests/test_release_workflow_contracts.py` | new — structural contracts with a vacuity floor |
| `tests/test_python_version_contract.py` | modify — add the two new workflows to the *python* parametrize list only |
| `docs/RELEASE_CHECKLIST.md` | new — 7 workflows, mandatory `HT_RUNTIME_DIR` step 0, live-protection re-read |
| `docs/DECISIONS.md` | modify — ADR for R1-D1…R1-D6, tag classes, option (c) |
| `docs/TESTING_STRATEGY_PLANNING.md` | modify — four locations + new §8.1b; Phase 4 stays open |
| `docs/ai_workflow/QUALITY_GATE.md` | modify — `.github/workflows/**` row + the `uses:` composite-rename rule |
| `docs/MASTER_HANDOVER.md` | modify — what landed and what it does not establish |
| `docs/test_inventory/TEST_INVENTORY.json` / `.md` | regenerate, last |
| `docs/release_pipeline/PLANNING.md` | this file |

**Added acceptance criteria**

34. Given an expected check-run whose selected conclusion is `cancelled`, `skipped`,
    `neutral` or `timed_out`, when provenance evaluates it, then it **fails** —
    `success` is the only passing conclusion.
35. Given the reusable workflow, when its smoke step command is read, then it invokes
    `scripts/smoke_packaged_app.py` with `--mode bootloader` and **without**
    `--skip-upgrade` or `--skip-runtime`, so the upgrade-migration proof survives the lift.
36. Given `release.yml`'s `old-db-migration` leg, when its required-table and
    required-column sets are parsed and compared with `deep-gate.yml`'s, then the release
    copy is a **superset** of deep-gate's — `program_backups` and `program_backup_items`
    included.

**Sequence**

1. `_packaged-windows.yml`; convert `ci.yml`'s job to call it.
2. `scripts/release_gate.py`, then `tests/test_release_gate.py`.
3. `release.yml`.
4. `tests/test_release_workflow_contracts.py`; run every mutation in both directions.
5. `tests/test_python_version_contract.py` parametrize edit.
6. `docs/RELEASE_CHECKLIST.md`, then the four doc updates.
7. Regenerate the inventory; full pytest; pyright baseline diff; `tsc`.
8. **Post-merge**: dispatch `release.yml` against `main` with `dry_run: true` and inspect
   the whole job set. A-B1 makes this impossible before merge, so the packet is not
   complete at merge.

**Gates**: full `pytest`; `python scripts/generate_test_inventory.py` then `--check`;
`scripts/pyright_baseline_diff.py`; `npx tsc --noEmit`; the 15-mutation harness. No
locally-derived E2E; CI supplies it.

### Residual register

| # | Residual | Why accepted |
|---|---|---|
| **R-1** | The `push: tags` trigger has **never fired**. Its wiring is unproven. | Owner option (c). Disclosed in `release.yml`'s header, checklist step 1, and TESTING_STRATEGY step 13. |
| **R-2** | The duplicate-check-run selection rule is justified **by construction**; no live duplicate exists to test against. | `filter=latest` and `filter=all` returned identical counts on every sampled SHA. Synthetic fixtures assert the rule's behavior, not that GitHub produces the shape. |
| **R-3** | ~~`release.yml` cannot execute at all before merge.~~ **DISCHARGED 2026-08-14** — the post-merge dry-run ran and passed. See the evidence section below. |
| **R-4** | **R1-D2**: the release gate credits the visual comparison that already ran on the SHA and never runs an independent second one. A red-then-re-run-to-green counts. | Deliberate. `Visual Regression (Windows baselines)` is **not** a protected context, so `main` can merge with it red — "green before tagging" therefore means all **12** expected contexts, not the 11 required. |
| **R-5** | Branch-protection drift is **not detectable offline**. The contract test pins in-repository drift only. | Compensated by a checklist step that re-reads the live contexts before tagging. |
| **R-6** | No locally-derived Chromium E2E. | No changed path reaches a browser; CI's E2E jobs still gate the merge. |
| **R-7** | **R1-D5**: the frozen executable is never booted against a historical-schema database. | Deferred to a follow-up packet by owner decision. |

---

## Post-implementation review round

Two reviewers ran against the staged diff. `unslop-reviewer` returned 11 findings;
`code-reviewer` died on a session limit mid-run and was relaunched to completion.

### code-reviewer (`ae1d6047e9359b032`) — one blocking false green

| # | Finding | Response |
|---|---|---|
| **B1** | `[ "$root" = "200" ] && [ "$plan" = "200" ]` in `old-db-migration` **cannot fail the step**. Under `set -e` bash exempts every command in an `&&` list except the last, so a failing first test falls through to the schema assertions, which say nothing about HTTP. | **Confirmed empirically** before fixing: the `&&` form exits 0 and continues; the standalone form exits 1. A build serving **500 on `/`** would have passed every schema assertion and gated the release green. Split into two standalone commands, and pinned by a new contract test (`test_no_assertion_hides_inside_an_and_list`) so the shape cannot return. `deep-gate.yml` carried the identical defect — discharged 2026-08-15 by Packet R2-a; see **R-9**. |
| N2 | Paging on `total_count` fails **open**: a response missing the key defaults the total to 0 and stops after page 1, so a newer failure on page 2 is never read. | Switched to paging until a short page; the envelope is no longer trusted. New test drives a two-page fixture with **no** `total_count` and the decisive failure on page 2. |
| N3 | The rehearsal path never checks that `APP_VERSION` can *produce* a valid tag. Under option (c) that is the only path that runs before a real release, so an `APP_VERSION` of `3.0` would rehearse green and red at tag time — after the version-bump PR had merged. | Adopted. The format check now runs on both paths, parametrized over four unreleasable versions. |
| N4 | A run with no `started_at` sorts *lowest* on the primary tuple element, so a newer untimestamped run loses to an older success — the exact masking `select_runs` exists to prevent. | Adopted; a missing timestamp now sorts highest, so the run is selected and `classify` judges it on its status. |
| N5 | R1-D1 says "on `main`" and **nothing enforced it**. `github.ref` carries the tag name, not what it points at, and provenance is satisfied by a green feature-branch head. | Enforced rather than struck: this is the owner's decision verbatim, so leaving it unenforced would under-deliver R1-D1. `commit_is_on_main()` compares against `main` and accepts only `identical`/`behind` — an unmerged descendant reports `ahead` and is rejected. Rehearsals are exempt by design and that exemption is tested. |
| N6 | `urllib.error` imported and never used; it advertises error handling that does not exist. | Import deleted. Confirmed no path swallows an API error into a pass — `_api_get` lets `HTTPError`/`URLError` propagate, so a 403 or rate-limit fails the gate **closed**. Retry-on-transient was considered and declined as scope; recorded as **R-8**. |
| N7 | Two "shipped" claims about #362/#366 need a measurement, not a PR body. | Measured: `gh pr view` reports #362 MERGED `52331bf`, #366 MERGED `f627161`, #368 MERGED `9be1a3f`. The claims stand on the measurement. |
| NITs | empty `expected` passes vacuously; `sorted` crashes on a null name; `kill` without `wait`; `\|\| echo 000` doubling curl's own `000`; bare `1897` literal; stale fixture docstring | All adopted. |
| ADR numbering | `docs/backup_schema_version/` (untracked, unlanded) also targets ADR-007 | R1 takes ADR-007; that packet already carries a renumber instruction and must move to ADR-008. Flagged in the PR body, not silently resolved here. |

### Residual register additions

| # | Residual | Why accepted |
|---|---|---|
| **R-8** | A transient GitHub API error (502, rate-limit) aborts `ci-provenance` outright; there is no retry across the ~90 requests it may make over 45 minutes. | Fails **closed**, so it costs a re-run rather than a bad release. Retry logic was declined as scope creep in R1. |
| **R-9** | ~~`deep-gate.yml` carries the same `&&`-chained HTTP assertion that B1 fixed here.~~ **DISCHARGED 2026-08-15 by Packet R2-a**, under a narrow owner exception to the pre-2026-08-17 freeze. The assertion is split into two standalone commands and `deep-gate.yml` is now covered by `test_no_assertion_hides_inside_an_and_list`. Measured before the edit under `bash -e`: the combined form exits **0** on `root=500` and falls through to the schema assertions; the split form exits **1**. The exception was taken because the defect meant `old-db-migration` could not fail on a broken landing page during the first authoritative scheduled run. **Only that assertion and an adjacent rationale comment changed** — no job composition, runner, step order, schedule, `visual-linux` or compare-mode behavior, and no baseline. The `_packaged-windows.yml` conversion is **Packet R2-b**, implemented 2026-08-15 and merged 2026-08-16 as #388; see the section below. |

### Gate 1 assessment

Plan v2 stays entirely within Packet R1: no artifact touches `deep-gate.yml`, no
branch-protection change, no tag, no publish. Every blocking council finding is resolved
above. No hard constraint is weakened — the two changes that reduce work
(no local E2E; no rehearsal tag) both follow from evidence or from an explicit owner
decision, and each is compensated and recorded. **Gate 1 is therefore satisfied under the
owner's conditional authorization.**

### Agent provenance

| Role | Agent ID | Notes |
|---|---|---|
| Plan v1 + matrix + Plan v2 | this session (manager-less run under owner delegation) | The owner authorized direct execution; no `product-manager` agent was dispatched. |
| `architecture-reviewer` | `ac1dd79ac8a5ef591` | 3 blocking, 8 non-blocking, 4 nits. |
| `test-strategist` | `a8a63e31cc3a5ff40` | 4 blocking, 9 non-blocking, 2 nits. |
| `product-risk-reviewer` | `af59ffce656209012` | 9 blocking, 7 non-blocking, 3 nits. |
| `code-reviewer` | `ae1d6047e9359b032` | Post-implementation. 1 blocking (the `&&` false green), 6 non-blocking, 7 nits. An earlier run died on a session limit and was relaunched. |
| `unslop-reviewer` | `a34b7ec7152edeba8` | Post-implementation. 11 findings, 10 adopted. |

---

## Post-merge dry-run evidence — 2026-08-14

Packet R1 merged as **#374** → `5222db2`. Main's own CI on that SHA settled at **18
check-runs, all `success`** — including all 12 the release gate expects. The check
count grew 17 → 18 mid-run as `E2E Functional (Chromium)` materialized after its
shards, the behavior the provenance poller was built around.

`release.yml` was then dispatched against `main` with `dry_run: true`
([run 31840756293](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/31840756293)).
**Run conclusion: `success`, all six jobs green:**

| Job | Result |
|---|---|
| `Version and tag identity` | success |
| `CI provenance on this commit` | success |
| `Frozen Windows executable / Build and smoke` | success |
| `First install (catalog seed) smoke` | success |
| `Old-DB migration compatibility` | success |
| `Release Gate` | success |

**The run was inspected rather than trusted.** A green fan-in is exactly what this
packet exists to distrust, so the logs were read for evidence that each job proved
something:

- `[release-gate] all 12 expected check-runs succeeded on 5222db2fc0e3c8a1...` — with
  a per-name table carrying each run's id, `started_at` and URL, so the count is
  backed by identified runs rather than asserted.
- `[release-gate] rehearsal on refs/heads/main: versions agree at 3.0.1, tag v3.0.1
  not yet published` — the parity check and the API-based tag-existence check both
  executed.
- `[release-gate] all 5 release jobs succeeded: ['ci-provenance', 'first-install',
  'old-db-migration', 'packaged-windows', 'version-guard']` — the fan-in saw exactly
  the expected job-id set.
- `first install: GET / -> 200` and `old-DB migration: GET / -> 200 ; GET
  /workout_plan -> 200` — real HTTP responses, from the assertions that the `&&` bug
  had previously made unable to fail.
- The `ci-provenance` job's runner banner reports its token as **`Checks: read`,
  `Contents: read`, `Metadata: read`** and nothing else — the least-privilege design
  confirmed at runtime, not just in the YAML.
- The informational extras list rendered correctly, naming the non-expected
  check-runs present on the SHA (including the composite `Packaged Smoke (Windows
  bootloader, non-required) / Build and smoke`).

**What this does and does not discharge.** Residual **R-3** is discharged: the
workflow executes and its jobs pass. **R-1 stands unchanged — the `push: tags`
trigger has still never fired.** What ran was `workflow_dispatch` against a branch;
the tag path, the tag-identity comparison and the on-`main` ancestry check are still
unexecuted, and the first genuine release tag remains their first execution.

---

## Packet R2-b — `deep-gate.yml`'s `frozen-windows` → the reusable workflow

*Implemented 2026-08-15; **merged 2026-08-16 as #388 (`949b15e`)** under an explicit owner
override of the hold condition below, which was **waived, not satisfied**. See
*Hold discharged by owner override — 2026-08-16* at the end of this section.*

R1 shipped `_packaged-windows.yml` and pointed `ci.yml` and `release.yml` at it, but
left `deep-gate.yml`'s `frozen-windows` as a second copy of the same build. R2-b
converts that job to `uses: ./.github/workflows/_packaged-windows.yml`, which takes the
repository from **two definitions / two callers** to **one definition / three callers**.

### Hold condition

`deep-gate.yml` executes the **default branch's HEAD copy of its own file** on a
schedule. The first authoritative scheduled run is due **2026-08-17 03:17 UTC**, and
that run must exercise the workflow as it shipped. Merging R2-b before it would
substitute a different file and destroy the evidence the D3 stopgap exists to produce.

**This packet may not merge until a scheduled run after 2026-08-17 03:17 UTC has been
inspected under the pre-R2-b workflow, and that inspection has been recorded.** As of
this packet's implementation, **no scheduled deep-gate run has occurred** and nothing
here may be read as evidence that one has.

> ⚠️ **The hold above was WAIVED by explicit owner override on 2026-08-16**, and #388
> merged ahead of the scheduled run. The hold condition and the checklist are preserved
> as written because they state the obligation correctly; **none of rows 1–3 was ever
> satisfied on its own terms**. What the waiver costs, and the substitute evidence that
> does *not* cover the `schedule` trigger, are recorded in
> *Hold discharged by owner override — 2026-08-16* at the end of this section. Read that
> before citing anything below as evidence.

The hold is stated here but **enforced in the merge mechanism**, because this repository's
standing convention is auto-merge on green CI and this branch is green by construction —
its contract tests are written against the post-conversion state, so CI cannot express the
hold. The PR is therefore opened as a **draft** with the hold in its title. Do not mark it
ready for review until every row below is done. *(Superseded by the 2026-08-16 override:
#388 was marked ready and merged with rows 1–3 unsatisfied. The draft-plus-title mechanism
did its job — it held the packet until an owner made an explicit, recorded decision to
spend the evidence, rather than letting green CI merge it silently.)*

#### Merge checklist — all rows required

| # | Obligation | How it is discharged |
|---|---|---|
| 1 | ✅ **Satisfied 2026-08-17** by run 31993105305 (green), though it ran R2-b's file rather than the pre-#388 one this row was written to demand — that evidence is forfeited, not obtained. Originally: a scheduled run after **2026-08-24 03:17 UTC** | `gh run list --workflow=deep-gate.yml --event=schedule`. ⚠️ **Amended 2026-08-16.** As written this row said *after 2026-08-17 03:17 UTC*, which the very next cron satisfies — but #388 merged first, so that run executes R2-b's file and cannot be the clean evidence this row exists to demand. See *Next clean checkpoint* at the end of this section. |
| 2 | All **7** jobs inspected individually, `visual-linux` executed and not skipped | `gh run view <id>` per job — **never the overall green**. ⚠️ **Inverted by the 2026-08-16 merge, and this row read the other way before it.** Row 1 requires a scheduled run *after* **2026-08-24 03:17 UTC** (it read 2026-08-17 before the same 2026-08-16 amendment), and every scheduled run from 2026-08-17 onward is post-merge, so the packaged job will **always** report under its **composite** name, `Frozen executable (real bootloader, Windows) / Build and smoke`. On `main` the pre-composite name appears only in runs at or before `d583225` (a `workflow_dispatch` against a stale branch still carrying the inline job would also report it) — e.g. the pre-merge rehearsal 31970872927. An inspector expecting the bare name will conclude the packaged job is missing when it is present. |
| 3 | The inspection is written down | A "Hold discharged" subsection appended to this R2-b section, **and** the deep-gate block in [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md) |
| 4 | `docs/MASTER_HANDOVER.md` corrected | **CLOSED 2026-08-16.** Its R1 block read "Packet R2-b, still not started", which was already false; corrected to implemented, with R-10/R-11/R-12 and the 5000→5123 change stated. The `R2-B-PENDING-EVIDENCE` marker it carried has been **replaced** — not with the scheduled run's evidence, which does not exist, but with the override record: what the waiver forfeits, the substitute dispatch, and the 2026-08-24 checkpoint. |
| 5 | `docs/DECISIONS.md` ADR-007 corrected | **CLOSED.** Its Consequences said "one definition with **two** callers"; superseded in place. |
| 6 | Full `pytest` re-run against a freshly merged `origin/main` | **CLOSED** — see the execution log below. Regenerate `docs/test_inventory/` if a count moved; never hand-merge it, because `Test Inventory Drift` is a required context. |

#### Execution log — rows 3, 4, 6 (2026-08-15, owner-authorized)

| Item | Evidence |
|---|---|
| Base before | `c404a06` (five commits stale) |
| Merged in | `origin/main` @ **`8baddd2`** — #385 `15498ab`, #389 `729eb4a`, #387 `9e5997a`, #386 `81df507`, #390 `8baddd2`; then **`d583225`** (#391) in a second merge |
| Merge commits | **`a11f89b`** 2026-08-15T15:46Z, then **`7f93e03`** 2026-08-15T18:0xZ. `origin/main` confirmed an ancestor of `HEAD` after each. **`main` advanced roughly hourly on 2026-08-15, so re-merge and re-run the gates immediately before merging rather than trusting this row.** The second merge was clean; #391's `ci.yml` edit was comment-only and the `R2-B-PENDING-EVIDENCE` marker survived the `MASTER_HANDOVER.md` auto-merge (both re-asserted by grep). |
| Conflicts | `docs/test_inventory/TEST_INVENTORY.{json,md}` **only** — exactly as row 6 predicted. Resolved by re-running the generator; zero conflict markers survive; `--check` clean. |
| Node counts | pytest **2660 → 2667** (this branch's +4 contract nodes ∪ main's +3). Playwright unchanged at **649 / 33**, enumerated against the merged tree. |
| `node_modules` | Deliberately **not** reinstalled. #390 is an in-range lockfile bump, Playwright still enumerates 649/33, and this worktree junctions into the shared main checkout — `npm ci` here mutates that shared install and breaks every other worktree. |
| Full `pytest` | **2987 passed, 2 skipped** — re-run after the second merge, same result |
| `npx tsc --noEmit` | exit **0** (both merges) |
| `pyright_baseline_diff.py` | **PASS**, 0 net-new (baseline 132, current 132) — both merges |
| 26-mutation harness | **26/26 red**, tree restored green (40 contract nodes) — both merges |
| PR checks | 18/18 SUCCESS, polled to **zero pending**, on `b50ef6f`; re-polled on `7f93e03` |

**Rows 1 and 2 remain OPEN — and were WAIVED, not closed, by the 2026-08-16 override.**
Re-measured **2026-08-16T20:53Z**, immediately before the merge — `--event=schedule` for
`deep-gate.yml`, the repo-wide `--event=schedule` list, and the REST `total_count` for
workflow `290121548` all still return **empty / 0**. Measured
2026-08-15T13:45Z and again before this merge:
`gh run list --workflow=deep-gate.yml --event=schedule`, the repo-wide `--event=schedule`
list, and the REST API `total_count` for workflow `290121548` all returned **empty / 0**
**as of 2026-08-16T23:32Z**. No `schedule`-event run had occurred by then; every one of the
105 deep-gate runs was a `workflow_dispatch`, which is **never** row-1 evidence. *(The
cron fired the next morning — see* **The first `schedule`-event run** *below.)* The one-shot routine
`trig_01Dy1dDmAgPFCSzXg2nmanJo` is armed and unfired for **2026-08-17T03:30:00Z**.

R2-a took a narrow exception to the same freeze for the `&&` assertion (R-9) because
that defect would have made `old-db-migration` unable to fail during the very run being
protected. **No comparable argument applies here**: the duplicate build is a maintenance
cost, not a false green, so the freeze is honoured in full. *(That held until 2026-08-16,
when the owner overrode the freeze outright and #388 merged. This paragraph is preserved as
the reasoning that applied while the hold stood; **the freeze is no longer in force**.)*

### What was preserved, and how it is proven

The build body moved unchanged. Everything the inline job guaranteed is now stated once,
in `_packaged-windows.yml`, and pinned there by `tests/test_release_workflow_contracts.py`:
runner (`windows-latest`), timeout (45), the six-step build sequence in order, the
`--mode bootloader` smoke without `--skip-upgrade` / `--skip-runtime`, and the
`if: failure()` distribution-inventory dump. The job id, the job `name:`, the schedule,
`visual-linux`, compare mode and every baseline are untouched.

### Three deliberate differences

| # | Before (inline) | After (via the reusable workflow) | Why it is not a weakening |
|---|---|---|---|
| 1 | check reported as `Frozen executable (real bootloader, Windows)` | `Frozen executable (real bootloader, Windows) / Build and smoke` | A `uses:` job reports as `<caller> / <callee>`. Safe **only** because `deep-gate.yml` produces no branch-protection context — it triggers on `schedule` and `workflow_dispatch`, never `pull_request`. A contract test asserts that trigger set, so the premise cannot rot silently. |
| 2 | smoke on the script's default port **5000** | `--port 5123` | `smoke_packaged_app.py` refuses to start when the port is already owned, so neither value can let another process answer for the build. 5123 is the value the other two callers already use, and R1 records serving off-default as the thing that proves the `HT_PORT` wiring. |
| 3 | no `permissions:` block → repository-default token | `contents: read` from the called workflow | A strict narrowing. The job checks out, builds, and smokes; it uploads nothing and pushes nothing. |

Difference 2 is the only one R1's own supersession note (#4, "`deep-gate.yml`'s
`frozen-windows` … passes no `--port`") glossed over when it dropped the `port` input.
Dropping the input was still right — a per-caller knob is how one definition starts
producing three behaviors — but the consequence is that this conversion changes
deep-gate's port, and that is recorded here rather than discovered later.

### Bidirectional caller contract

`PACKAGED_CALLERS` in `tests/test_release_workflow_contracts.py` declares the three
`(workflow file, job id, job name)` triples and is compared against the set **measured**
from the workflow files:

- **Forward** — a declared caller that stops calling, re-inlines steps, grows a
  `runs-on:`, or reintroduces `pyinstaller` / `smoke_packaged_app.py` fails.
- **Reverse** — a caller that appears without being declared fails, because it mints a
  new composite check name that `docs/ai_workflow/QUALITY_GATE.md` requires to be a
  deliberate act.
- **Neither side can vary the build** — the reusable workflow declares no `inputs:` and
  no caller passes `with:`; both halves are asserted, since either alone passes once the
  other is deleted.
- **The claim is scoped to the repository, not to a literal.** Every contract here
  iterates a hardcoded four-file list, so a *new* workflow file would have been invisible
  to all of them — it could inline its own PyInstaller build, or mint a fourth composite
  check name, with the whole file green. A directory contract asserts that
  `.github/workflows/` holds exactly the files this test reads, which is what makes "the
  only definition in the repository" a true sentence rather than a hopeful one.

**26 mutations, each applied and reverted individually, all 26 red** — including
re-inlining the build, dropping the job, renaming either half of a composite name,
adding a fourth caller, moving the runner off Windows, unbounding the timeout, deleting,
reordering **or gutting the body of** the staging step, weakening the smoke to payload
mode, adding `--skip-upgrade`, returning to port 5000, making the shared smoke
`continue-on-error` (which would turn a red build green for all three callers at once),
adding a `pull_request:` trigger to `deep-gate.yml`, blinding the parser (the vacuity
floor), and **adding a whole new workflow file** that either inlines the build or calls
the reusable one undeclared.

### Residual register additions

| # | Residual | Why accepted |
|---|---|---|
| **R-10** | ~~The converted job has **never executed as a `uses:` job**; `workflow_dispatch` requires the file on the default branch, so there is zero runtime evidence available before merge.~~ **DISCHARGED 2026-08-16** — `workflow_dispatch` [31972476567](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/31972476567) on `main` @ **`949b15e`** (the merge commit itself): **7/7 jobs success**, `frozen-windows` executed as a `uses:` job for the first time and reported under the composite name `Frozen executable (real bootloader, Windows) / Build and smoke`. | The same sequencing R1 accepted, with the same compensation: the first post-merge action is a `workflow_dispatch` of `deep-gate.yml` whose `frozen-windows` result is inspected. **That dispatch is still not the held inspection and does not discharge the hold** — it says nothing about the `schedule` trigger. The two obligations are separate; the hold is checklist rows 1–3 above and was waived, not met. *(This row predicted the dispatch would use default inputs and so skip `visual-linux`. It was run with `run_visual=true visual_mode=compare`, so `visual-linux` executed and compared without writing a baseline — proven at step level, as *Next clean checkpoint* below requires: `Assert compare mode wrote no baseline` **passed** and `Upload generated Linux baselines` was **skipped**.)* |
| **R-11** | The B9 `concurrency:` decision for `deep-gate.yml` — the other half of the original Packet R2 — is **still not started**. | Out of scope for this packet by the owner's framing; it is a separate decision, not a consequence of the conversion. |
| **R-12** | `_packaged-windows.yml` uploads no build artifact and declares no `outputs:`, so all three callers discard `dist/`. A future packet that attaches the executable to a release needs both per-caller distinction and `contents: write`, and the no-`inputs`/no-`with:` contract plus the read-only-token contract forbid the second. | Pre-existing, not introduced here, and the cheapest correct answer does not need a relaxation: upload `dist/` unconditionally with a short retention and let a separate job in `release.yml`, which already carries its own `permissions:` blocks, download and publish. R1-D5's `--legacy-db` work needs no relaxation at all — the argv contract forbids *removals*, not additions, and `PACKAGED_STEP_SEQUENCE` pins a prefix. |
| **R-13** | `test_the_workflow_directory_holds_exactly_the_files_this_file_reads` measures `.github/workflows/` against the `ALL_WORKFLOWS` literal, so **adding or deleting any workflow file now reds the full pytest suite** — and `Run Tests` is a required branch-protection context. Creating a workflow therefore blocks its own PR until the literal is updated in the same commit. | **Deliberate, and the point of the test.** Every other contract in the file iterates that hardcoded literal, so before this a new workflow file was invisible to all of them — it could inline a second PyInstaller build or mint a fourth `<name> / Build and smoke` composite check with every contract still green. Coupling the two is what makes "one definition, three callers" a claim about the repository rather than about four named files. The assertion message names the literal to update, so the fix is one line and self-describing. Recorded here because the cost lands on an unrelated future packet that adds a workflow, not on this one. |

### Hold discharged by owner override — 2026-08-16

Rows 1–3 of the merge checklist above were **never satisfied on their own terms**. They
are **waived by explicit owner authorization on 2026-08-16**, which permitted this packet
to merge ahead of the 2026-08-17 scheduled run. This subsection records what that costs,
so that no later reader mistakes the waiver for the evidence it replaced. **Nothing below
is scheduled-run evidence.**

#### What is knowingly forfeited

The scheduled run due **2026-08-17 03:17 UTC** was the single opportunity to observe the
deep gate fire *on its own trigger* while running *the file that had actually shipped*.
Merging R2-b today spends it. `deep-gate.yml` executes the default branch's HEAD copy of
itself, so Monday's run will exercise **R2-b's** file, not the pre-R2-b one.

**The 2026-08-17 run is therefore forfeited as clean first-execution evidence of the
shipped deep gate — permanently, and by choice.** No re-run recovers it: the only way to
obtain that particular evidence was to let Monday arrive with the old file on `main`.

#### The substitute: dispatch 31970872927

Before this merge, the **currently shipped** (pre-R2-b) `deep-gate.yml` was dispatched on
`main` and inspected at job level:

| | |
|---|---|
| Run | [31970872927](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/31970872927) |
| Event | **`workflow_dispatch` — NOT `schedule`** |
| Ref / SHA | `main` @ **`d583225`** — the shipped, pre-R2-b file |
| Inputs | `run_visual=true`, `visual_mode=compare` (both required: `run_visual` defaults to **false**, so a bare dispatch runs the deep gate with no visual job at all) |
| Window | 2026-08-16T20:33:14Z → 20:51:03Z |
| Result | **7 / 7 jobs `success`**, each read individually — never off the overall green |

| Job | Conclusion |
|---|---|
| Full E2E incl. accessibility (Chromium) | success |
| First install (catalog seed) smoke | success |
| Empty-schema initializer smoke | success |
| Old-DB migration compatibility | success |
| Frozen executable (real bootloader, Windows) | success — inline body: stage assets → canonical spec → `--mode bootloader` |
| Visual regression (Linux baselines) | success — **executed, not skipped** |
| Dependency Health Check | success |

`visual-linux` was verified at **step** level, not job level: `Assert compare mode wrote
no baseline` **passed** and `Upload generated Linux baselines` was **skipped**, which
together prove the run compared rather than generated and wrote nothing to
`e2e/__screenshots__`. No baseline was regenerated, and none needed to be — there was no
red to make go away.

**What this dispatch establishes:** that all seven job *bodies* run green against `main`
as shipped, `visual-linux` included. **What it does not establish:** anything whatsoever
about the `schedule` trigger. A trigger that has never fired reports nothing, and a
`workflow_dispatch` is never evidence for it — the same lesson `release.yml`'s
`push: tags` still teaches, having never fired either. *(The `schedule` half of that
sentence was resolved on 2026-08-17: the cron fired for the first time. See
**The first `schedule`-event run** below. `push: tags` is unaffected and has still
never fired.)*

#### Correction to an earlier framing

Statements that the deep gate's *job bodies* had never executed were wrong and are
withdrawn. Dispatch [31851213502](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/31851213502)
(2026-08-14, `main`) already ran all seven jobs green with `visual-linux` executed. The
accurate and much narrower claim — the one this file made correctly elsewhere — is that
**no `schedule`-event run had ever occurred**, repo-wide, as of 2026-08-16T23:32Z. The
unproven thing was always the trigger, never the job bodies — and that trigger fired for
the first time hours later; see **The first `schedule`-event run** below.

#### The `schedule` trigger is still unvalidated, and remains so after Monday

> ⚠️ **Resolved by events, 2026-08-17.** The prediction below was written before the
> cron fired. It fired, and it came back green. The section is preserved because its
> *reasoning* was sound and its second bullet describes a risk that was accepted, not
> avoided — but the heading is no longer true. Read
> **The first `schedule`-event run** below for what actually happened.

The 2026-08-24 checkpoint below exists because Monday cannot close this. Monday's run, if
it fires, executes **R2-b's** file, so it is contaminated as evidence of the deep gate as
shipped and held. Specifically:

- A **green** Monday does not retroactively validate the gate that was held for it.
- A **red** Monday is **ambiguous** between "the scheduled deep gate never worked" and
  "R2-b broke it" — precisely the ambiguity the hold existed to prevent, now accepted
  knowingly rather than avoided.

~~Do not record the `schedule` trigger path as validated on the strength of the 2026-08-17
run, whatever it reports.~~ **Superseded 2026-08-17.** The run happened and was green; the
trigger *is* validated. What it does not validate is the pre-#388 file — that distinction,
not the blanket prohibition, is what survives.

#### Next clean checkpoint — 2026-08-24 03:17 UTC

> ✅ **EXECUTED 2026-08-24, and inspected as this subsection demands.** Run
> [`32688747703`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32688747703),
> event `schedule`, head `31659a5`: **7/7 jobs `success` read individually**, `visual-linux`
> **executed and not skipped**, compare mode proven at step level. Every requirement stated
> below was met, including the composite-name warning. It **is** the second consecutive green
> scheduled run, so **R1-D3's clock stands at 2 of 3** and the third is due **2026-08-31
> 03:17 UTC**. The full job- and step-level record is § *The second `schedule`-event run —
> 2026-08-24* at the end of this file; the tense below is left as written.

~~The **2026-08-24** scheduled run is the first uncontaminated `schedule`-event evidence:
by then R2-b's file will have been on `main` since before the preceding run, so the file
under test and the trigger under test finally agree.~~

**Superseded 2026-08-17.** The 2026-08-17 run turned out to be usable evidence after all
— see below — so 2026-08-24 is not "the first clean run". Its remaining value is that it
is the **second consecutive** green scheduled run, which is what R1-D3's *three
consecutive green scheduled runs* clock actually needs.

It must still be **judged at job level** — all seven jobs read individually, with
`visual-linux` confirmed **executed and not skipped**. The overall green is not coverage;
`visual-linux` is `if:`-gated and a skip leaves the run green. Confirm the event with
`gh run list --workflow=deep-gate.yml --event=schedule` before treating any run as
qualifying, and note that from this merge onward the packaged job reports under its
composite name, `Frozen executable (real bootloader, Windows) / Build and smoke`.

---

## The first `schedule`-event run — 2026-08-17

*The cron fired for the first time in the repository's history. Every earlier statement
that no `schedule`-event run had occurred was true when written and is now history.*

| | |
|---|---|
| Run | [31993105305](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/31993105305) |
| Event | **`schedule`** — the first ever, repo-wide |
| SHA | **`63b206e`** — R2-b's file, i.e. the post-#388 deep gate |
| Due / actual | 03:17:00Z scheduled, **started 04:02:52Z** — a **~46 minute** scheduler delay |
| Window | 2026-08-17T04:02:52Z → 04:20:46Z |
| Result | **7 / 7 jobs `success`**, read individually — never off the overall green |

| Job | Conclusion |
|---|---|
| Full E2E incl. accessibility (Chromium) | success |
| First install (catalog seed) smoke | success |
| Empty-schema initializer smoke | success |
| Old-DB migration compatibility | success |
| `Frozen executable (real bootloader, Windows) / Build and smoke` | success — the **composite** name, under a real scheduled event |
| Visual regression (Linux baselines) | success — **executed, not skipped** |
| Dependency Health Check | success |

Step-level proof: `Assert compare mode wrote no baseline` **passed**. That is the
load-bearing step — it is `always()`-guarded and greps `git status --porcelain` over
`e2e/__screenshots__`, so it runs and reports even on a failing job. `Upload generated
Linux baselines` was **skipped**, which corroborates the mode but proves nothing on its
own: its `if:` is `steps.visual.outputs.mode == 'generate'`, so a skip merely restates
that the mode was compare. `frozen-windows` ran Stage tracked package assets → Build via the canonical
spec → Smoke the real bootloader. No baseline was regenerated and none needed to be.

### What this establishes — first time for every item

- **The `schedule` trigger fires.** Previously zero evidence, and a trigger that never
  fires reports nothing. This is the D3 stopgap's whole premise, and it is now measured.
- **`visual-linux` runs on a schedule.** A `schedule` event carries **no `inputs` at all**,
  so `if: github.event_name == 'schedule' || inputs.run_visual` resolved down the
  *schedule* disjunct — a different code path from every dispatch that preceded it, and
  one that had never executed.
- **Compare mode holds when `inputs` is absent.** `MODE="${{ inputs.visual_mode || 'compare' }}"`
  plus the re-pin on the event name had also never run under a real schedule event.
- **R2-b's converted `uses:` job works on the schedule**, reporting under its composite name.

### What it does not establish

- **Nothing about the pre-R2-b file.** That evidence was forfeited by the 2026-08-16
  override and is unrecoverable. It is also now moot: that file no longer exists on `main`.
- **Nothing about `release.yml`'s `push: tags` trigger**, which is a separate trigger on a
  separate workflow and has **still never fired** (residual **R-1**).
- **Nothing about stability.** One green run is one green run; R1-D3 wants three.
- **Nothing about the gate's ability to go RED.** The Linux corpus was in sync, so
  `Assert compare mode wrote no baseline` passing shows nothing *was* written — not that
  real drift would have been caught. A gate that has only ever passed is not yet a gate
  known to fail correctly.

### An honest note on the contamination call

The override record predicted this run would be *contaminated*, and that a red here would
be **ambiguous** between "the scheduled gate never worked" and "R2-b broke it". It came
back green, so that ambiguity never materialised. **That is an outcome, not a vindication.**
The risk was real when it was accepted, and a red would have cost exactly what was
predicted. What changed the picture is narrower than it looks: the run is unusable as
evidence about the *held* file, but it is perfectly good evidence about the deep gate as it
now exists — which is the only version that will ever run again.

## The second `schedule`-event run — 2026-08-24

*The cron fired a second time, on schedule and unattended. This section is the job- and
step-level record the* Next clean checkpoint *subsection above demanded, and it is what
R1-D3's clock is counted from. Nothing here promotes `visual-linux` into the release gate.*

*Placement note: the* Contract hardening after the first scheduled run *section that follows
is dated 2026-08-20/21 and therefore predates this run — it sits after this one because it
closed the file before this section was added, not because it responded to anything here. Its
own closing paragraph carries a 2026-08-24 annotation pointing back to this section.*

| | |
|---|---|
| Run | [`32688747703`](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/32688747703) |
| Workflow | `Deep Gate (manual + weekly)` — `.github/workflows/deep-gate.yml` |
| Event | **`schedule`** — confirmed with `gh run list --workflow=deep-gate.yml --event=schedule`, not read off the run page |
| SHA | **`31659a5`** — `origin/main` after PR #414 |
| Due / actual | 03:17:00Z scheduled (`cron: '17 3 * * 1'`), **started 04:05:58Z** — a **48 m 58 s** scheduler delay |
| Window | `2026-08-24T04:05:58Z` → `2026-08-24T04:24:03Z`, attempt **1** |
| Result | **7 / 7 jobs `success`**, read individually — never off the overall green |

| Job | Job id | Conclusion |
|---|---|---|
| Full E2E incl. accessibility (Chromium) | `97318476914` | `success` |
| First install (catalog seed) smoke | `97318476932` | `success` |
| Empty-schema initializer smoke | `97318476965` | `success` |
| Old-DB migration compatibility | `97318476896` | `success` |
| `Frozen executable (real bootloader, Windows) / Build and smoke` | `97318476906` | `success` — the **composite** name, as the checklist's row 2 warned to expect |
| **Visual regression (Linux baselines)** | **`97318476983`** | `success` — **executed, not skipped** |
| Dependency Health Check | `97318476761` | `success` |

**Step-level proof on `visual-linux`, because the job's green alone is not the pass
condition.** `visual-linux` is the one deliberately conditional job in this workflow, and a
skip leaves the run green:

| Step | Status |
|---|---|
| Assert committed visual seed present | **`success`** |
| **Run visual specs** | **`success`** |
| **Assert compare mode wrote no baseline** | **`success`** |
| Upload generated Linux baselines | `skipped` |
| Upload Playwright report + diffs | `skipped` |

*Assert compare mode wrote no baseline* is the load-bearing one — it is `always()`-guarded
and greps `git status --porcelain` over `e2e/__screenshots__`, so it runs and reports even on
a failing job. *Upload generated Linux baselines* being skipped **corroborates** compare mode
and proves nothing on its own: its `if:` is `steps.visual.outputs.mode == 'generate'`, so a
skip merely restates that the mode was compare. **No baseline was regenerated and none was
needed** — the Linux corpus was in sync against `31659a5`.

### What this establishes, and what it does not

**Establishes.**

- **The `schedule` trigger fires repeatedly and unattended.** 2026-08-17 proved it can fire
  once; a single delivery is not a schedule. Two deliveries a week apart, both unattended,
  are.
- **The `schedule` disjunct of `visual-linux`'s `if:` resolved a second time.** A `schedule`
  event carries no `inputs` at all, so `github.event_name == 'schedule'` is the only branch
  that can run this job on a cron — the exact shape #400 pinned as a set of disjuncts.
- **A second, independent scheduler-delay observation: 48 m 58 s**, against 45 m 52 s on
  2026-08-17. Two points are still not a bound, and GitHub gives scheduled workflows no
  delivery guarantee. **Do not read a late run as a missed one.** Plan for up to an hour.
- **R1-D3's clock reaches 2 of 3** under the reading recorded in the *Out of scope* bullet in
  Section 0. The third qualifying run is due **2026-08-31 03:17 UTC**.

**Does not establish.**

- **Nothing about the gate's ability to go RED.** The Linux corpus was in sync, so *Assert
  compare mode wrote no baseline* passing shows nothing *was* written — not that real drift
  would have been caught. **A gate that has only ever passed is not yet a gate known to fail
  correctly**, and two green runs make that objection older, not weaker.
- **Nothing about `release.yml`'s `push: tags` trigger**, a separate trigger on a separate
  workflow, which has **still never fired** (residual **R-1**).
- **Nothing that authorizes acting on the clock.** Closing a clock is not the same as taking
  the decision it gates: putting `visual-linux` into the release gate is a fresh owner
  decision under D3, and reaching 3 of 3 confers no signature.
- **Nothing about the pre-#388 file**, which stays permanently forfeited and is now doubly
  moot — that file has not existed on `main` for eight days.

### Where the count lives

**Measure it; do not read it from prose.**
`gh run list --workflow=deep-gate.yml --event=schedule` is the only authority, and on
2026-08-24 it returned exactly two runs, both `success`. Every narrative surface in this
repository — including this section — is a dated reading, and a `workflow_dispatch` run never
counts however green it is. Measured the same day from the REST `total_count`:
`…/workflows/deep-gate.yml/runs?event=workflow_dispatch` reports **108** and
`?event=schedule` reports **2** — and **not one of the 108 is a qualifying run**.

---

## Contract hardening after the first scheduled run — #399, #400 and #402

*All three are **tests-only**. `.github/workflows/**` is byte-identical to
`origin/main` across every packet — each mutation was applied inside an isolated
worktree and reverted with `git checkout --`. No production behavior, schema,
calculation or API contract is involved. **[#402 added 2026-08-21; the heading and
this paragraph previously named #399 and #400 only.]***

The automation-QA review of #398 found that Packet R2-b's hardening was **one
level too shallow**: the `if:` bar covered the deep-gate *caller* only, while the
callee and the other two callers were unguarded, and several adjacent shapes were
unguarded entirely.

### #399 (`280c211`) — seven shapes, 13 mutation arms, all 13 missed beforehand

| # | Shape | Blast radius |
|---|---|---|
| 1 | `if:` on `_packaged-windows.yml`'s own `build-and-smoke` | Kills the frozen build for **all three callers at once** — PR path, release gate, weekly gate — while every "one definition / three callers" contract stays green |
| 2 | `if:` on the `ci.yml` / `release.yml` caller jobs | Per-caller kill |
| 3 | `needs:` on a caller | A skipped dependency skips the build and the run stays green |
| 4 | `strategy:`/matrix on a caller | Mutates the composite check to `<parent> (x) / <child>` — GitHub injects the matrix segment *between* two halves that were both already pinned |
| 5 | `secrets:` at either end | Contradicts the callee's own "No caller passes anything" comment, which the tests enforced for `with:`/`inputs:` only |
| 6 | `concurrency:` in the callee | Overrides all three callers' deliberately different policies from one place |
| 7 | The cron expression | `triggers()` reads trigger *names*, so `schedule:` staying present said nothing about whether the cron can fire. `grep -rn cron tests/ scripts/ e2e/` returned **zero** hits repo-wide |

**Why the step-level guard could not see the `if:`, for two independent reasons:**
`steps()` splits on `^    - name: ` and discards `parts[0]` — the job header — and
it matches a **six**-space step indent where a job-level key sits at **four**.

> **A note on that commit's subject line.** It reads *"close **five**
> mutation-proven false greens"*. The packet grew past five during the work and
> the subject was never rewritten; its own body enumerates **seven** and reports
> 13 mutation arms. **Read the body, not the subject.** History is not being
> rewritten to repair it, and there is no committed register of "five shapes"
> anywhere in this repository — the automation-QA review that prompted the packet
> was never committed.

### #400 (`81771d1`) — the two shapes #399 named and did not reach

1. **`visual-linux`'s `schedule` disjunct was unprotected.**
   `if: ${{ github.event_name == 'schedule' || inputs.run_visual }}` is the only
   job-level `if:` this repository deliberately allows, so every contract that
   *bars* the shape elsewhere had nothing to say about what this one contains. **A
   `schedule` event carries no `inputs` at all**, so deleting
   `github.event_name == 'schedule' ||` leaves a weekly run that skips its visual
   comparison entirely and still reports green — the exact opposite of the
   "executed, not skipped" pass condition
   [`MASTER_HANDOVER.md`](../MASTER_HANDOVER.md) states for this gate. The
   condition is now pinned as an exact **set of disjuncts**, not as a string, and
   `&&` is barred by name because it reads as a near-identical edit while
   inverting the meaning.
2. **`steps()` answered a 4→6-space reindent with `[]` instead of an error.** YAML
   lets a block sequence sit at its key's column or deeper, so the reindent is the
   **same document** — and matched nothing. Measured on `deep-gate.yml`: all seven
   jobs parsed to zero steps and **all 42 contracts stayed green**. Fixed at the
   root: `steps()` now cross-checks against an indentation-blind count of the same
   `- name:` entries, so a job declaring `steps:` must yield at least one, the two
   counts must agree (catching a *partial* reindent), and a `uses:` job stays
   legal. A second vacuity floor runs `steps()` over every job in all four
   workflows, because nothing in that file iterated `ci.yml`'s steps at all.

**The durable lesson.** A whole-file reindent is a **semantic no-op that silently
empties an indentation-pinned parser**. Three of the four workflows stayed fully
green under it; the fourth was caught only by dict-lookup `KeyError`s in four
tests, while the three contracts that actually *iterate* its steps passed
vacuously.

### What is still open — five jobs, not six

> **[CLOSED 2026-08-21 by #402 (`1f9c05a`)]** — this heading and the paragraphs
> under it describe the state between #400 and #402 and are kept as written. The
> count of five, and the reason it is five and not six, were correct — they are
> exactly what #402 implemented. The subsection after this one is the record.

`deep-gate.yml` declares **seven** jobs: `full-e2e`, `first-install`,
`empty-schema`, `old-db-migration`, `frozen-windows`, `visual-linux` and
`dependency-health`. Exactly **two** are pinned against a job-level `if:` —
`frozen-windows` (#399) and `visual-linux` (#400). The remaining **five** —
`full-e2e`, `first-install`, `empty-schema`, `old-db-migration` and
`dependency-health` — still accept a job-level `if:` unmeasured.

> **#400's own body says "the other six". That is wrong; it is five.**
> Re-derived 2026-08-20 against `origin/main` at `81771d1` by listing the job keys
> in `deep-gate.yml` and grepping `tests/test_release_workflow_contracts.py` for
> each name: `full-e2e`, `empty-schema` and `dependency-health` appear nowhere in
> that file, and `first-install` / `old-db-migration` appear only in the port and
> required-set contracts, neither of which constrains a job-level `if:`.

Pinning them is a **future packet and is not authorized**. It is a *newly
identified* gap — **not** a leftover from the shape set #399 and #400 closed, and
it must not be reported as one.

> **[SUPERSEDED 2026-08-21]** — the authorization sentence above is no longer live:
> the packet was authorized and merged as **#402** (`1f9c05a`). The sentence is
> kept because it was true when written and because it records that this work
> was *not* silently overtaken by a merge — #402's own body listed this line as an
> authorization claim needing explicit owner reconciliation, which is what this
> note is.

### #402 (`1f9c05a`) — the five jobs, pinned

*Tests only, shipped as squash **`1f9c05a`**. The PR changed
`tests/test_release_workflow_contracts.py` and the two generated inventory files
and nothing else. `.github/workflows/**` is byte-identical to the commit before
it — `deep-gate.yml` was mutated only inside an isolated worktree and restored —
so **no workflow behavior, runtime behavior, schema, API or response contract
changed**.*

**What is now pinned.** `full-e2e`, `first-install`, `empty-schema`,
`old-db-migration` and `dependency-health` are barred from carrying **any**
job-level `if:` key. The key alone is the violation: the contract matches
`^    if:` against the comment-stripped job block and captures the value only for
the failure message, so `if:` with its value on the following line, and `if:`
followed by a tab, are caught alongside the ordinary `if: ${{ false }}`. A first
draft that demanded `if: ` plus a value passed vacuously on both of those and was
replaced — **a new contract can be strictly weaker than the siblings it imitates**.

**Why a per-job contract, and not just the count floor.** The pre-existing
vacuity floor asserts `deep-gate.yml` declares seven jobs, so a job simply
*added* already redded there. It says nothing about *which* jobs: a **rename**,
or an add paired with a removal, holds the count at seven while moving a job out
of the protected set. `test_every_deep_gate_job_is_classified_as_conditional_or_not`
pins the job ids for that reason, and measures the exception set against the file
rather than trusting it — moving a job into the exception set is otherwise a
two-word edit that drops a parametrize arm and constrains nothing in its place.

**The two jobs #402 did not change.**

- **`visual-linux` remains the one deliberately conditional job.** Its condition
  is still pinned by #400 as the exact set of disjuncts
  `{github.event_name == 'schedule', inputs.run_visual}` — matched as
  `if: ${{ … }}`, split on `||`, with `&&` barred by name because a `schedule`
  event carries no inputs. #402 additionally asserts that the exception set is
  exactly `{visual-linux}`, so widening it has to be a deliberate edit.
- **`frozen-windows` retains its prior unconditional protection**, from
  `test_the_weekly_gate_still_smokes_a_real_bootloader_on_windows` and the
  `PACKAGED_CALLERS` delegation contract, which bars `if:`, `needs:`, `with:`,
  `secrets:` and `strategy:` on all three callers. #402 reads its job id back out
  of `PACKAGED_CALLERS` rather than repeating it, so the two classifications
  cannot drift apart.

**Mutation evidence.** `if: ${{ false }}` inserted immediately after each job's
`name:` key, run in both directions and restored between arms: all five arms —
and all five applied at once — were **green before the packet** against every
contract the file then held, and each is **killed individually now** by its own
parametrized arm, so the failing node id names the offending job. The
completeness half was measured separately: a job simply *added* was already
caught by the `== 7` floor, while the **rename** that holds the count at seven
was the arm that was green. The three deliberately preserved arms (dropping
`visual-linux`'s `schedule` disjunct, removing its `if:` entirely, and growing an
`if:` on `frozen-windows`) red both before and after — **this packet adds a
contract and weakens none**.

**Deliberately left open, and not established as defects.** `needs:` and a
job-level `continue-on-error:` are two further shapes that could stop one of these
five jobs from gating. Neither is barred, and **neither has been measured** —
they are recorded here so they are not lost, *not* as known false greens and
*not* as authorized work. Each requires its own mutation proof and its own
separately authorized packet before anything is claimed about it. Note in passing
that `dependency-health` already reports rather than gates — both its scan steps
are `continue-on-error: true` — so it is held to the `if:` shape because it is
the repository's only scheduled Python vulnerability scan, not because skipping
it would lose a blocking signal.

### Inventory

`tests/test_release_workflow_contracts.py` moved **40 → 44** across the two
packets (**40 → 42** in #399, then **42 → 44** in #400); deterministic
collected nodes are **2740** across **123** files, with **124** pytest files
in total. Read those from
[`test_inventory/TEST_INVENTORY.md`](../test_inventory/TEST_INVENTORY.md)
rather than restating them. No test file was added or removed by either packet.

> **[UPDATED 2026-08-21]** — #402 added six collected nodes on top of the figures
> above. That contract file is **44 → 50** (one census test plus five
> parametrized arms) and the deterministic total is **2740 → 2746**; file counts
> are unchanged at **123** deterministic files and **124** pytest files, because
> #402 added no test file either. The inventory was regenerated by the generator,
> never hand-edited. Read the live figures from
> [`test_inventory/TEST_INVENTORY.md`](../test_inventory/TEST_INVENTORY.md).

### What none of these packets establishes

*(Previously "What neither packet establishes"; #402 is in scope here too and
establishes nothing further on any of these points.)*

Nothing about **R1-D3's three-consecutive-green-scheduled-runs clock**, which
still stands at **one** (run 31993105305, 2026-08-17); nothing about
`release.yml`'s `push: tags` trigger, which has **still never fired** (residual
**R-1**); and nothing about the gate's ability to go **red**. These are contract
tests over the workflow *text* — they prove the file cannot silently lose a
guarantee, not that the guarantee holds at runtime. The next scheduled run is
still **2026-08-24**.

> ⚠️ **UPDATED 2026-08-24 — two of the readings above are dated and have moved; the
> paragraph is kept as written because what it *establishes* is unchanged.** The clock no
> longer *"stands at one"*: the 2026-08-24 cron fired and was green at job level, so it
> **stands at 2 of 3** and the third is due **2026-08-31 03:17 UTC** — see § *The second
> `schedule`-event run — 2026-08-24* above, and measure the count with
> `gh run list --workflow=deep-gate.yml --event=schedule` rather than reading it here or
> there. *"The next scheduled run is still 2026-08-24"* is likewise spent. **Everything the
> paragraph actually asserts still stands verbatim**: these are contract tests over the
> workflow *text*, they establish nothing about the clock, `push: tags` has **still never
> fired**, and nothing about the gate's ability to go **red** has been established by any
> run, green or otherwise.
