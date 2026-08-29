# Active Development

This file is the execution source of truth for autonomous development sessions. Use it when it conflicts with older narrative planning text.

## Current Objective

**2026-08-29 (LATEST) — Track P1 is CLOSED at 0 / 0 / 0, `main` is at `225b7b0`,
and NO engineering packet is in flight. Everything still
open is either an owner decision or parked. `js-unit` is still NOT promoted, and
the JS-unit window's T0 is still CONDITIONAL and UNDECLARED.** `origin/main` is
at **`225b7b0`**, in full `225b7b0e6428418fa48a389b67365376debb0957` (PR
[#448](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/448), the
`REFACTOR_PLAN.md` reconciliation to Track P1's closure, merged
`2026-08-29T16:56:57Z`), with all 18 checks green on that commit — post-merge run
`33264331296`, **read at job level**, **18
jobs and 18 `success`**. The commit before it is `158ee40`
([#445](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/445), the
owner-facing status board added as §15 of the Open Work Execution Plan, merged
`2026-08-29T13:47:38Z`, run `33255921889`, 18/18).

**The open-PR count is an INSTANT, not a state, and this one was re-measured
after #448 landed.** Read at **`2026-08-29T17:06:46Z`**: **THREE** PRs are open,
all documentation-only — [#450](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/450)
(`OPEN_WORK_EXECUTION_PLAN.md` + `STEP12_JS_UNIT_GATE0.md`),
[#451](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/451)
(`OPEN_WORK_EXECUTION_PLAN.md` + `toast_type_word_collision/PLANNING.md`), and
the PR carrying this block, which counts itself. **Zero are dependency PRs.** An
earlier reading in this same pass, at `14:47:26Z`, also returned three — but a
*different* three, because **#448 has since merged and #451 opened at
`15:53:10Z`**. Neither #450 nor #451 touches either file this pass edits, so
there is no conflict — but **both claim work otherwise listed as owed below.**
The block below says TWO, which was true when written — #415 and #416 both merged
2026-08-26.
**Take no automatic feature action from this file, and take no action on any
owner decision it names.**

**1 — Track P1 (pyright reduction) is CLOSED at 0 / 0 / 0.**
[`ci_cd_phase3/pyright-baseline.json`](ci_cd_phase3/pyright-baseline.json) reads
`_meta.total_diagnostics` **0** and `_meta.distinct_keys` **0** at `225b7b0`,
with an empty `diagnostics` list. **[#446](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/446)** (`1226e46`) took
**37 / 16 / 11 → 9 / 2 / 1**; **[#447](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/447)** (`3532f86`) closed the last
nine in `routes/workout_plan.py` under an **explicit owner authorization that
lifted that file's off-limits designation for that one bounded packet — spent,
not repealed.** The allowlist is empty and has **no headroom**: one net-new
diagnostic reds the required
`Type Check (tsc blocking + pyright measure-only)` context, and the repair is to
fix the diagnostic, never to re-widen the baseline. The narrative record is
[`OPEN_WORK_EXECUTION_PLAN.md`](OPEN_WORK_EXECUTION_PLAN.md) §16.2 — read it, do
not re-derive it here.

**2 — There is NO automatic next engineering packet.** T0, U1, U2 and both halves
of U3 are on `main` — KI-010 `288667d` ([#431](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/431)), KI-011 `5b35966`
([#426](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/426)) — R0 is closed, Track P1 is closed. What remains is
**owner-decision-gated or parked**: the eight live decisions and one owed record
in [`OPEN_WORK_EXECUTION_PLAN.md`](OPEN_WORK_EXECUTION_PLAN.md) §15.4, and §5's
eight parked items. **No agent may start any of them.** The one track an agent may
continue unattended is **Track D1**, dependency-PR triage, and its queue is
**empty** — note §15.1's limit: an agent may *triage* a bump unattended, but
**landing one still needs explicit owner authorization.**

**3 — The JS-unit ledger on `main` ends at ROW 26, and rows 27–38 are OWED.** Row
26 is job `98703428098` of run `33125767570` (`push` / `288667d`, #431),
**`success`**, completed **`2026-08-27T23:18:21Z`** — the restart row. **Twelve**
`main` `ci.yml` runs have completed a green `JS Unit` job since and none is
written into §13.0. **All twelve were re-read at job level in this pass** — each
run's `/jobs` enumerated and matched on the exact context string
`JS Unit (Vitest, non-required)`, then that job's own `conclusion` and
`completed_at` read off it, never the run's overall conclusion — and all twelve
are 18 jobs / 18 `success`. **The identifiers for rows 27–36 are deliberately not
transcribed here** — rows 27–33 are numbered in §14.3, row 34 in §14.5 and rows
35–36 in §16.3. **Rows 37 and 38 are the exceptions, because no other document
carries them**: row 37 is job `99109487854` of run `33255921889`,
**`success`**, completed **`2026-08-29T13:48:04Z`** — minted by #445's own merge,
which #445 could not record; **row 38 is job `99131593513` of run `33264331296`,
`success`, completed `2026-08-29T16:57:25Z`** — minted by #448's own merge, which
#448 likewise could not record. Both are **published here as measurements to be
re-verified at §13.0 before transcription, not as rows already recorded.**

**The completeness check, with both instruments on the record.** The interval is
`2026-08-27T23:18:21Z` → `2026-08-29T17:06:46Z`, this pass's final read. **The broad query** —
`gh api "…/actions/runs?branch=main&per_page=100"`, filtered
to `created_at > 2026-08-27T23:18:00Z` — returns **exactly those twelve runs and
nothing else**, all `ci.yml` / `push`; twelve results against a 100-item page, so
no truncation is possible. **The narrow query** enumerated **all five**
non-`ci.yml` workflows the repository has, by workflow id, and each returns
**zero** `main` runs in the interval — by path:
`.github/workflows/_packaged-windows.yml`, `.github/workflows/deep-gate.yml`,
`.github/workflows/release.yml`, and the two Dependabot ones,
`dynamic/dependabot/dependabot-updates` and `dynamic/dependabot/update-graph`. **So this stretch hides no attempt and, unlike the 2026-08-24
window recorded below, contains no classified non-attempt run at all.** The
checkable reason for the Dependabot half is the schedule, not the queue: all
three ecosystems in [`.github/dependabot.yml`](../.github/dependabot.yml) are
`interval: "weekly"`, `day: "monday"`, and this interval — Thursday to Saturday —
**contains no Monday**. The ledger is kept at
**job** level in exactly one authoritative place —
[`testing_phase3/STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md)
**§13.0**. A row may be written only there, and no count may be read off this
paragraph at a later session.

**4 — T0 is CONDITIONAL and UNDECLARED; the old marks are SPENT.** #431 took the
Vitest corpus **231 → 245**, engaging owner ruling Q2's restart clause. **The old
T0 `2026-08-22T17:59:26Z` and the old strict mark `2026-09-05T17:59:26Z` no
longer exist** — every restatement of them below this block is history, not live
guidance. Whether `2026-08-27T23:18:21Z` is the new T0 turns on **whether #431 was
the final expansion packet**, an **owner determination that is OWED**: U3b's
KI-011 helper coverage and **U1-FOLLOWUP-1** are both still unlanded. **Read the
operative T0 from §13.0, never from here.** The corpus at `225b7b0` is **13 files
/ 245 cases**.

**5 — Live state, re-queried in this pass rather than carried over.**

| Reading | Value at `225b7b0` | Moved since §16.4's reading at `3532f86`? |
|---|---|---|
| Open PRs | **3** at `17:06:46Z`, all documentation-only — [#450](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/450) (`OPEN_WORK_EXECUTION_PLAN.md` + `STEP12_JS_UNIT_GATE0.md`), [#451](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/451) (`OPEN_WORK_EXECUTION_PLAN.md` + `toast_type_word_collision/PLANNING.md`), and the PR carrying this block, which counts itself. **A count is an instant:** 1 (#445) at §16.4, 0 at `13:57Z`, a *different* 3 at `14:47:26Z`, and this 3 after #448 merged and #451 opened | **Yes**, repeatedly |
| Open dependency PRs | **0** — Track D1's queue is still empty | No |
| Open Dependabot alerts | **0** | — §16.4 took no alerts reading |
| Open issues | **0** | — |
| `deep-gate.yml` `schedule` runs | **2**, both `success` — `31993105305`, `32688747703` | No. Third due **2026-08-31 03:17 UTC**, not yet occurred |
| `deep-gate.yml` runs, all events | **110** — 2 `schedule`, 108 `workflow_dispatch` | — |
| `release.yml` runs | **0** `push`, **1** `workflow_dispatch` — `31840756293`, `2026-08-14T21:03:46Z` | No. `push: tags` has **still never fired** |
| Live branch protection | **12** required contexts; `JS Unit (Vitest, non-required)` **absent**; `strict` **false** | No |
| `pyright-baseline.json` `_meta` | `total_diagnostics` **0**, `distinct_keys` **0** | No — closed at `3532f86` |
| Vitest corpus | **13 files / 245 cases** | No |

**R1-D3's clock is still 2 of 3**, and `scripts/release_gate.py`'s 12-required /
13-expected list has **still never executed by any trigger** — its lone
`workflow_dispatch` run predates `a937116`.

**Explicitly NOT authorized and NOT taken:** promotion of `js-unit` (**Q4** /
**D2**); **D4**; any branch-protection or repository-settings change; any tag or
workflow dispatch; any dependency merge; and any action on R1, R2, R3, V1 or
R1-D3 beyond recording the readings above.

> ⚠️ **[UPDATED 2026-08-30 — two of the five named items have since been acted on, with owner
> authorization. The sentence above is kept as the reading it was for the pass it describes.]**
> **R1** — the deep-gate mutation probes — was authorized and run, and shipped as
> [#455](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/455) (`2cb938c`). **V1** was
> ruled the same day and its documentation half shipped as
> [#454](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/454) (`8c844df`); the V1
> *measurement* half remains **blocked on runner access** and unstarted, and the V1 ruling
> itself stands exactly as #454 recorded it. **R2, R3 and R1-D3 are untouched** and the
> prohibition still holds for them, as it does for every other item in the sentence.
>
> **What R1 established, stated exactly:** the contract tests this repository held **do not
> detect** either shape — a job-level `needs:` or a job-level `continue-on-error:` on a
> `deep-gate.yml` job. It did **NOT** establish that a runtime false green occurs. **No workflow
> was dispatched and no run was inspected**; the runtime behavior rests on documented GitHub
> Actions semantics and the mechanism `ci.yml` already states in its own comments above the
> `test-inventory` job. Nothing in #455 may be cited as *"runtime false green demonstrated"*.
>
> **R1 left two things open, and neither was implemented.** A job-level `continue-on-error:` on
> the `uses:` job `frozen-windows` is likewise undetected (arm H2-M4) — **recorded, not fixed**,
> and now §15.4 item 11. And nothing bars the same shape in `release.yml` or
> `_packaged-windows.yml`, which sit on the **required** path — **recorded and not probed**.

**One further surface in THIS file is stale and is annotated in place rather than
rewritten** — the `## Next Action` section far below, which restates the spent T0
marks, asserts *"zero open PRs"* and calls **KI-010** and **KI-011** open. It sits
outside any dated block, so the blanket in item 4 does not reach it and it carries
its own `[UPDATED 2026-08-29 …]` banner. This mirrors the treatment
[`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) gives its three equivalent surfaces.

**Still owed, and not done here:** ledger rows **27–38** in §13.0 — §13.0 is the
only place a row may be written, and **a concurrent session has claimed that
pass as [#450](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/450)**, which writes rows 27–37 and refreshes the
plan's status layer, so **do not duplicate it**; note that **#448's merge has
since minted row 38**, so #450 must extend to it before it lands. Also owed on
`main`: the **OD-1 waiver record** for #431's early merge (a record gap, **not**
an improper merge — the owner has since confirmed the waiver preceded it),
**claimed by [#451](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/451)**,
which writes it as **OD-1-W**, so **do not duplicate that either**.

**One debt on that list is DISCHARGED.**
[`REFACTOR_PLAN.md`](REFACTOR_PLAN.md)'s continuous-track row — the last surface
actively asserting Track P1 was open — was refreshed by
**[#448](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/448), MERGED as
`225b7b0`** at `2026-08-29T16:56:57Z`, post-merge run `33264331296` 18/18 green at
job level. It now reads **"Done — closed 2026-08-29 at 0 / 0 / 0"**.

**Three readings on the Open Work Execution Plan's §15 board now sit past its own
derivation stamp** (*"Derived at `3532f86`, 2026-08-29"*): **§15.2 debt 1** reads
*"rows 27–36 … ten `main` runs"*, where the range is now **27–38** and twelve;
**§15.1's Track D1 row** reads *"the one open PR is this plan's own"*, where
#445 and #448 have both merged and three PRs are open; and **§15.2 debt 2**
carries the OD-1 waiver as owed, which #451 writes. **This is a dated view ageing,
not a defect** — debt 1 explicitly predicted that merging #445 would mint row 37 and
that it could not record it, and no §4 or §5 status field moved, so §15's *"fix
the board in the same commit"* rule did not fire. Refreshing the board is outside
this pass's two-file scope: **[#450](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/450) carries it** along
with the ledger rows, and **[#451](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/451)
carries debt 2's half.**

**Next actions, in order:** (1) **do not start a ledger append for rows 27–38** —
[#450](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/450) already carries rows **27–37**
into §13.0 and must extend to **row 38**, which #448's merge minted after that PR was written;
review or land that PR instead. **The standing rule is unchanged and applies to every merge,
including this one** (§11.10): a PR can never record its own post-merge row. Append at job level,
re-verifying against the API rather than transcribing from any status document; (2) **inspect the 2026-08-31 scheduled deep gate only after it executes**,
at job level, with `visual-linux` confirmed *executed* rather than skipped, never
off the overall green — expect drift of up to an hour; a green there is the third
consecutive green run and closes R1-D3's clock, but **acting on a closed clock is
still a separate owner decision**; (3) **do not start a `REFACTOR_PLAN.md`
refresh — it is DONE.** [#448](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/448) merged
as `225b7b0`. **Do not start the OD-1 waiver record either** —
[#451](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/451) carries it and is open; review
or land that PR instead, and the record returns as work only if #451 is closed unmerged; (4) **the owner determination on whether #431 was the
final Vitest expansion packet is owed**, and it blocks Q4 / D2; (5) **everything
else waits on the owner** — §15.4 items **2–6 and 8**, which is **six** live decisions.
*(Repaired 2026-08-29: this read "items 1–8 and 10"; item 10 was the OD-1 waiver record, landed
as **OD-1-W** in `fe15225` (#451) and discharged under §15.2. **Item 7 (V1) was then ruled**,
leaving seven. **Re-derived 2026-08-30 from the merged table after #455:** the queue is **nine
rows — items 1–8 and 11** — of which **six block**. **Item 1 is discharged** (the deep-gate
mutation probes ran), **item 7 is ruled** under the V1 decision, and **item 11 is new and blocks
nothing today**. The range "1–8" no longer describes the queue in either direction.)*

> **⚠️ "Packet R1" now names two unrelated things in this repository.** The *"Packet R1"*
> reference far below — *"the release/tag pipeline is no longer deferred"* — means
> [#374](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/374) (`5222db2`). The **R1**
> in item 5 above and in [`OPEN_WORK_EXECUTION_PLAN.md`](OPEN_WORK_EXECUTION_PLAN.md) §15.1 /
> §15.4 is a different packet entirely: the **deep-gate mutation probes**,
> [#455](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/455) (`2cb938c`). They share a
> letter and a number and nothing else. **Check which one a citation means before acting on it.**

**This reconciliation changed documentation only** — exactly two files,
[`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) and this one. No production, test,
workflow, dependency, inventory, generated, config, branch-protection or
repository-settings change.

**2026-08-24 (LATEST) — the 2026-08-24 scheduled deep gate EXECUTED and was green
at job level; R1-D3's clock is recorded at 2 of 3; the qualification ledger gains
row 5. `js-unit` is still NOT promoted and T0 is unmoved.** `origin/main` is at
**`31659a5`** (PR [#414](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/414),
the post-#413 status reconciliation, merged `2026-08-23T19:22:55Z`), with all 18
checks green on that commit — post-merge run `32661056527`, **read at job level**,
18 jobs and 18 `success`. **The repository has TWO open PRs**, both Dependabot and
both unmerged: **#415** (`pyinstaller` 6.22.0 → 6.22.2) and **#416** (`sass`
1.102.0 → 1.103.1), opened `2026-08-24T00:25Z`. Take no automatic feature action
from this file.
**[UPDATED 2026-08-29 — this block carried the `(LATEST)` marker until the block
above was written; `git rev-list --count 31659a5..225b7b0` is **35**, and
`git merge-base --is-ancestor` confirms `31659a5` is still an ancestor of `main`. Nothing below is edited except this
annotation. **Four** of its claims are spent, and all four are corrected above
rather than here: its *"`origin/main` is at `31659a5`"*; its *"TWO open PRs"* —
#415 and #416 both merged **2026-08-26** and there are now **three**, none a dependency PR; its
**five**-row ledger reading — `main`'s ledger now ends at **row 26** with rows
**27–38** owed, and §13.0 remains the only place that count lives; and its *"T0 is
UNCHANGED at `2026-08-22T17:59:26Z`"* / *"`2026-09-05T17:59:26Z`"* pair — **#431
engaged Q2's restart clause on 2026-08-27 and BOTH marks are SPENT**. Two further
statements have moved: **KI-010 and KI-011 are no longer open** (`288667d`,
`5b35966`), and its next-action item **(4)** is discharged. Its next-action item
**(1)** is **still live and undischarged** — the 2026-08-31 deep gate has not yet
run. **Its item (2) survives only in part:** the obligation to continue the
ledger stands, but its terminus `2026-09-05T17:59:26Z` is **spent**, and the
ledger now runs against §13.0's conditional T0. Item **(3)** is unchanged. **Its
remaining assertions were not re-measured in this pass, with three exceptions
item 5's table above did re-measure and confirms** — 12 required contexts with
`js-unit` absent, `push: tags` never fired, and the schedule clock at 2 of 3. For
everything else the live readings are item 5's table and §16.4 of the Open Work
Execution Plan.]**

**1 — The scheduled deep gate ran, and it is the second consecutive green
`schedule`-event run.** Run `32688747703`, event **`schedule`**, head `31659a5`,
`2026-08-24T04:05:58Z → 04:24:03Z`. Its 03:17:00Z cron delivered **48 m 58 s**
late — a second drift observation after 2026-08-17's 45 m 52 s, not a missed run.
**All seven jobs were read individually and all seven are `success`:**

| Job | Job id | Conclusion |
|---|---|---|
| Full E2E incl. accessibility (Chromium) | `97318476914` | `success` |
| First install (catalog seed) smoke | `97318476932` | `success` |
| Empty-schema initializer smoke | `97318476965` | `success` |
| Old-DB migration compatibility | `97318476896` | `success` |
| `Frozen executable (real bootloader, Windows) / Build and smoke` | `97318476906` | `success` — the **composite** name |
| **Visual regression (Linux baselines)** | **`97318476983`** | `success` — **executed, not skipped** |
| Dependency Health Check | `97318476761` | `success` |

**Proven at step level, because the job's green alone is not the pass condition.**
On job `97318476983`: *Assert committed visual seed present* **passed**, *Run
visual specs* **passed**, and *Assert compare mode wrote no baseline* **passed** —
that last step is the load-bearing one, `always()`-guarded and grepping
`git status --porcelain` over `e2e/__screenshots__`. *Upload generated Linux
baselines* and *Upload Playwright report + diffs* were both **skipped**, which
corroborates compare mode without proving it. **No baseline was regenerated and
none was needed.**

**2 — R1-D3's clock is 2 of 3, settled by an owner ruling.** The question
*"does the 2026-08-17 run count?"* is **SETTLED by an owner ruling dated
2026-08-24, recorded in [`DECISIONS.md`](DECISIONS.md) ADR-007 under R1-D3: it
COUNTS.** **ADR-007 is the authority — read it, do not re-derive this.** It was
recorded rather than inferred because a repository-wide search that day found the
question *raised* in three places —
[`release_pipeline/PLANNING.md`](release_pipeline/PLANNING.md), ADR-007 itself,
and [`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) — and **answered nowhere**. The
reasoning behind it, kept for the reader: R1-D3 as the release plan's Section 0
records it verbatim — *"Revisit only after the 2026-08-17 run and at least 3
consecutive green scheduled runs"* — names the 2026-08-17 run and nowhere
excludes it. **Measured, not inferred:**
`gh run list --workflow=deep-gate.yml --event=schedule` returns exactly **two**
runs repo-wide, **both `success`** — `31993105305` and `32688747703`. **The clock
stands at 2 of 3; the third is due 2026-08-31 03:17 UTC**, and only a fresh owner
ruling superseding the 2026-08-24 one could move it. **D3 itself stays deferred
regardless — nothing here puts `visual-linux` into the release gate, and closing
a clock is not the same as acting on it.** `release.yml`'s `push: tags` trigger has **still never fired**.

**3 — The qualification ledger now holds FIVE rows.** Read live at job level at
`2026-08-24T17:03:00Z`: **five** green `main` `JS Unit (Vitest, non-required)`
results since and including T0, with **zero** red, missing, skipped or cancelled.
Row 5 is job `97247194117` of run `32661056527` (`push` / `31659a5`, PR #414,
18/18), completed `2026-08-23T19:23:22Z`. The ledger is kept at **job** level in
exactly one authoritative place —
[`testing_phase3/STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md)
**§13.0**, *LIVE LEDGER* (its **post-#414** block). Do not restate its rows here,
and do not read a count off this paragraph at a later session.

**The ledger's qualification SCOPE is now stated, because 2026-08-24 is the first
day the broad query and the narrow one disagree.** §6.1 fixes qualification at
**`ci.yml` (`CI/CD Pipeline`)**. Four `main` runs in the window belong to other
workflows — three Dependabot `dynamic` update runs (`32676594582`, `32676594619`,
`32676594928`, path `dynamic/dependabot/dependabot-updates`, one `Dependabot` job
each) and the deep gate above (`32688747703`, `deep-gate.yml`, seven jobs).
**None is a qualification attempt and none may be recorded as a `js-unit` job
"missing"** — neither workflow declares that job at all, and `deep-gate.yml`
contains zero occurrences of `js-unit` / `JS Unit`. **The broad every-workflow API
query is kept** as the completeness check that no attempt is hidden; only its
result is classified rather than tallied into the *Missing* row. #415 and #416
will produce `ci.yml` runs on their **PR branches**, which are not `main` runs and
never enter the ledger.

**T0 is UNCHANGED at `2026-08-22T17:59:26Z`** — job `97070630453` on `main` run
`32589375849`, the **Packet C** post-merge run — and the strict 14-day mark is
still **`2026-09-05T17:59:26Z`**. #414 was documentation-only (three files:
`ACTIVE_DEVELOPMENT.md`, `MASTER_HANDOVER.md`, `testing_phase3/STEP12_JS_UNIT_GATE0.md`)
and changed no JS test case — 13 files / 231 cases, unchanged across
`b0aa393 → 31659a5` — so owner ruling Q2's restart clause never engaged. **No
PR's `mergedAt` is T0.**

**Explicitly NOT authorized and NOT taken:** promotion of `js-unit` (**Q4** /
**D2**) — branch protection carries **12** required contexts, re-read live
2026-08-24, and `JS Unit (Vitest, non-required)` is **absent**; **D4**; fixes for
**KI-010** or **KI-011**; any branch-protection or repository-settings change; and
any action on R1-D3 beyond recording the count. **D4 and the `js-unit` half of D2
stay unsigned**, and **Q4 and D2 stay undecided and unauthorized, pending a
separate owner decision.** **NT-4 stays closed, NT-7 stays open**, and
`Test Inventory Drift` still pins six surfaces.

**Next actions, in order:** (1) **inspect the 2026-08-31 scheduled deep gate only
after it executes** — at job level, with `visual-linux` confirmed *executed*
rather than skipped, never off the overall green; a green there is the **third**
consecutive green run and closes R1-D3's clock under the reading above, but
**acting on a closed clock is still a separate owner decision**; expect drift of
up to an hour; (2) **continue the qualification ledger** in §13.0 until
`2026-09-05T17:59:26Z`, at job level, recording any red, missing, skipped or
cancelled **`ci.yml`** result — a red **resets the window to zero**; (3) **leave
Q4 and D2 unsigned pending a separate owner decision**; (4) **#415 and #416 are
unreviewed and unmerged** — nothing here touches them.

**This reconciliation changed documentation only** — exactly six files
(`docs/release_pipeline/PLANNING.md`,
`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`,
`docs/TESTING_STRATEGY_PLANNING.md`, `docs/DECISIONS.md`,
`docs/MASTER_HANDOVER.md` and this file). No production, test, workflow,
dependency, inventory, generated, config or repository-settings change.

**2026-08-23 (LATEST) — repository state reconciled through PR #413; `js-unit`
is still NOT promoted.** `origin/main` is at **`b0aa393`**
(PR [#413](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/413), the Q6
documentation correction, merged `2026-08-23T18:03:43Z`), with all 18 checks green
on that commit — post-merge run `32656837264`, **read at job level**, 18 jobs and
18 `success`. The repository has **zero open PRs**. Take no automatic feature
action from this file.
**[UPDATED 2026-08-24 — this block carried the `(LATEST)` marker until the block
above was written; `origin/main` has since moved **one** commit to `31659a5`
(#414). Nothing below is edited except this annotation. **Three** of its claims
are spent, and all three are corrected above rather than here: its
*"`origin/main` is at `b0aa393`"*; its *"zero open PRs"* — there are now **two**,
Dependabot #415 and #416; and its **four**-row ledger reading — there are now
**five** rows, and §13.0's post-#414 block is the only place that count lives.
Its next-action item **(1)**, *"claim nothing about the 2026-08-24 deep gate until
it has run"*, is **DISCHARGED**: it ran, 7/7 green at job level, and the record is
above. Everything else it asserts — T0 and the strict mark, the A → B → C → F
shape, Packet D dropped and the letter E vacant, NT-4 closed and NT-7 open, the
six pinned surfaces, **12** required contexts with `js-unit` absent, Q4 / D2 / D4
unsigned, KI-010 and KI-011 open, and `push: tags` never fired — was re-checked on
2026-08-24 and still stands.]**

**Two PRs merged after `2c95bae`, and both are documentation-only.**

| PR | Commit | Terminal result |
|---|---|---|
| **#412** | `ca28ec0` | Post-#411 status reconciliation. Four documentation files: `ACTIVE_DEVELOPMENT.md`, `MASTER_HANDOVER.md`, `TESTING_STRATEGY_PLANNING.md` and `testing_phase3/STEP12_JS_UNIT_GATE0.md`. Post-merge run `32639359162`, 18/18 green. |
| **#413** | `b0aa393` | **Q6 — the stale JS-unit coverage/jsdom claims, corrected.** Exactly **three** tracked files: `docs/TESTING_STRATEGY_PLANNING.md` (new **§2.1a** carrying the live reading), `docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`, and **`vitest.config.js` — comment-only, no executable configuration changed**. **Zero** files under `static/js/**`; no workflow, dependency, inventory, generated or branch-protection change. Post-merge run `32656837264`, 18/18 green. |

**Q6 is DISCHARGED.** Every figure was re-measured rather than carried over:
**13 files / 231 cases**, statements **7.8 %** (582 / 7,453), **57** files under
`static/js` excluding `*.test.js`, **13** with any coverage, **44** at exactly
**0 %**, and **5** test files carrying the jsdom pragma. The superseded
**`9 of 57` / `5.6 %`** figure is the 2026-08-15 reading of run `31856035853` and
is preserved as that record — do not quote it as current.

**T0 is UNCHANGED at `2026-08-22T17:59:26Z`** — job `97070630453`
(`JS Unit (Vitest, non-required)`) on `main` run `32589375849`, the **Packet C**
post-merge run — and the strict 14-day mark is still **`2026-09-05T17:59:26Z`**.
Neither #412 nor #413 restarted the window: both are documentation-only and
changed no JS test case (13 files / 231 cases, unchanged across
`2c95bae → ca28ec0 → b0aa393`), so owner ruling Q2's restart clause never engaged.
**No PR's `mergedAt` is T0.** The ledger is kept at **job** level in exactly one
authoritative place —
[`testing_phase3/STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md)
**§13.0**, *LIVE LEDGER* (its post-#413 block) — and read live on 2026-08-23 after
#413 it holds **four** green `main` results with **zero** red, missing, skipped or
cancelled, and **no `schedule`-event run**. Do not restate its rows here, and do
not read a count off this paragraph at a later session.

**Explicitly NOT authorized and NOT taken:** promotion of `js-unit` (**Q4** /
**D2**) — branch protection carries **12** required contexts, re-read live
2026-08-23, and `JS Unit (Vitest, non-required)` is **absent**; **D4**; fixes for
**KI-010** or **KI-011**; and any branch-protection or repository-settings change.
**D4 and the `js-unit` half of D2 stay unsigned**, and **Q4 and D2 stay
undecided and unauthorized, pending a separate owner decision.** **NT-4 stays closed, NT-7 stays open**, and `Test Inventory Drift`
still pins six surfaces. `release.yml`'s `push: tags` trigger has **still never
fired**.

**Next actions, in order:** (1) **inspect the 2026-08-24 scheduled deep gate only
after it executes** — at job level, with `visual-linux` confirmed *executed*
rather than skipped, never read off the overall green; expect a scheduler delay of
up to an hour, and claim **nothing** about it until it has run; (2) **continue the
qualification ledger** in §13.0 until `2026-09-05T17:59:26Z`, at job level,
recording any red, missing, skipped or cancelled result — a red **resets the
window to zero**; (3) **leave Q4 and D2 unsigned pending a separate owner
decision** — the expansion packets confer no signature.

**This reconciliation changed documentation only** — exactly three files
(`docs/testing_phase3/STEP12_JS_UNIT_GATE0.md`, `docs/MASTER_HANDOVER.md` and this
file). No production, test, workflow, dependency, inventory, generated, config or
repository-settings change.

**2026-08-23 — Phase 3 step 12's expansion sequence is COMPLETE on
`main`; `js-unit` is still NOT promoted.** `origin/main` is at **`2c95bae`**
(PR [#411](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/411), Packet F,
merged `2026-08-22T21:52:14Z`), with all 18 checks green on that commit — post-merge
run `32600832091`, **read at job level**. The repository has **zero open PRs**. Take
no automatic feature action from this file.
**[UPDATED 2026-08-23 — this block carried the `(LATEST)` marker until the block
above was written; `origin/main` has since moved **two** commits to `b0aa393`
(#412 `ca28ec0`, then #413 `b0aa393`). Nothing below is edited except this
annotation. **Two** of its claims are spent, and both are corrected above rather
than here: its **two**-row ledger reading of `2026-08-23T10:11:56Z` — there are
now **four** rows, and §13.0 is the only place that count lives — and its listing
of **Q6** among the things not authorized, which is **DISCHARGED** by #413.
Everything else it asserts — T0 and the strict mark, the A → B → C → F shape,
Packet D dropped and the letter E vacant, NT-4 closed and NT-7 open, the six
pinned surfaces, **12** required contexts with `js-unit` absent, Q4 / D2 / D4
unsigned, KI-010 and KI-011 open, and the 2026-08-24 deep gate — was re-checked
on 2026-08-23 and still stands.]**

**Eleven PRs merged after `4d53487` and this file recorded none of them.** The
block below carried the `(LATEST)` marker through all of them; this block is the
record.

| PR | Commit | Terminal result |
|---|---|---|
| **#404** | `0984d2e` | Docs only — the auto-backup recovery procedure landed in `README.md` and D7 was recorded as signed. This is the change the block below describes; it merged **after** that block was written. |
| **#406** | `987588a` | **Phase 3 step 12 Packet B — `toast.js`.** Test-only: one new file, 47 jsdom cases. Two real production defects were measured, pinned and left **OPEN** as **KI-010** and **KI-011**. |
| **#407** | `f3b9313` | Docs only — registered KI-010 / KI-011 and reconciled Packet B to its merged state. |
| **#405** | `f252f5f` | npm-audit **M2 + M3** enforcement — `scripts/npm_audit_gate.mjs` plus an empty allowlist; levers L1 + L2. |
| **#409** | `a937116` | npm-audit **M4 / lever L3** — `JS Supply Chain (npm audit, non-required)` promoted into branch protection. **Required contexts 11 → 12; the job name is unchanged and must not be "fixed".** |
| **#410** | `9cb6cdc` | **Packet C — `exercises.js`.** Test-only, one new file. **This was the final expansion packet**, so it started the qualification clock. Post-merge run `32589375849`, 18/18 green. |
| **#411** | `2c95bae` | **Packet F — Vitest inventory + drift enforcement.** Seven tracked files: the generator, a new pytest contract file, both regenerated `docs/test_inventory/` artifacts, `QUALITY_GATE.md`, `.claude/rules/testing.md` and the step-12 packet doc. **Zero** files under `static/js/**` or `.github/workflows/**`; **no branch-protection change**. Post-merge run `32600832091`, 18/18 green. |
| **#395 / #396 / #397 / #408** | `d6da70b` / `f972373` / `924e363` / `b52df68` | Dependabot: pyinstaller 6.21→6.22, pytest-playwright 0.8→0.9, `@types/node` 26.1.2→26.2.0, and the vitest group. Recorded so the ledger has no hole. |

**The step-12 sequence is A → B → C → F, and all four are on `main`** — **A** shipped
inside the Gate 0 PR #387 (`9e5997a`), then #406, #410 and #411 above. **Packet D
is DROPPED** (owner ruling Q3, closed unstarted — `backup-center.js` is not covered
by step 12 and its 0 % coverage is an accepted recorded gap), and **the letter E is
deliberately vacant** in step 12, because `testing_phase3/PLANNING.md` keeps "Packet
E" for step 11's restore-path fuzz. Neither is leftover work; do not queue either.

**T0 is `2026-08-22T17:59:26Z`** — job `97070630453` (`JS Unit (Vitest,
non-required)`) on `main` run `32589375849`, the **Packet C** post-merge run — and
the strict 14-day mark is **`2026-09-05T17:59:26Z`**. **Packet F did not restart
the window**: it changed no JS test case (13 files / 231 cases, byte-identical
either side of `2c95bae`), so owner ruling Q2's restart clause never engaged.
**#411's `mergedAt` is not T0.** The ledger is kept at **job** level in exactly one
place — [`testing_phase3/STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md)
**§13.0**, *LIVE LEDGER* — and read `2026-08-23T10:11:56Z` it holds **two** green
`main` results with **zero** red, missing, skipped or cancelled. Do not restate its
rows here.

**NT-4 is closed by measurement**: the PR's ubuntu `Test Inventory Drift` job
`97094899990` (run `32599231895`, `ubuntu-latest`, `success`) checked the committed
inventory against a fresh **Linux** regeneration and passed against a
Windows-generated artifact. **NT-7 remains open.**

**`Test Inventory Drift` now pins six surfaces, not five.** From `2c95bae` onward,
adding, removing, **renaming**, `.skip`-ing or `.todo`-ing any
`static/js/**/*.test.js` case trips a **required** check and must ship a regenerated
`docs/test_inventory/` artifact in the same PR — a reversal of the rule Packets A–C
ran under.

**Explicitly NOT authorized and NOT taken:** promotion of `js-unit` (**Q4** /
**D2**) — branch protection carries **12** required contexts, re-read live
2026-08-23, and `JS Unit (Vitest, non-required)` is **absent**; **Q6**'s stale
coverage/jsdom prose correction; **D4**; fixes for **KI-010** or **KI-011**; and
any branch-protection or repository-settings change. **D4 and the `js-unit` half of
D2 stay unsigned.** The next scheduled deep-gate run is still **2026-08-24**, and
`release.yml`'s `push: tags` trigger has **still never fired**.

**2026-08-21 — Testing Strategy D7 is SIGNED; the auto-backup recovery
procedure is now in `README.md`.** `origin/main` is at **`4d53487`** (PR #403,
merged 2026-08-21), 18/18 checks green on that commit. Take no automatic feature
action from this file.
**[UPDATED 2026-08-23 — this block carried the `(LATEST)` marker until the block
above was written; `origin/main` has since moved **eleven** commits to `2c95bae`
(#411). Nothing below is edited except this annotation. Its D7 facts remain
accurate; its *"the next scheduled deep-gate run is still 2026-08-24"* is still
true, and its *"D4 and the `js-unit` half of D2 stay unsigned"* was re-checked on
2026-08-23 and is still true.]**

The owner signed D7 **exactly as recommended**: retain the "no in-app restore"
stance for startup database snapshots, and publish the already-reviewed manual
recovery procedure in `README.md`. The ruling and the scope it authorized are
[`TESTING_STRATEGY_PLANNING.md`](TESTING_STRATEGY_PLANNING.md) **§8.1d**; the
reviewed draft and its F1–F7 correction history stay in
[`finding1_residual/PLANNING.md`](finding1_residual/PLANNING.md), annotated in
place rather than rewritten.

Every recovery instruction was re-verified against `utils/auto_backup.py`,
`utils/database.py`, `utils/runtime_paths.py`, `utils/config.py`,
`utils/runtime_migration.py`, `utils/program_backup.py`,
`utils/schema_registry.py` and `app.py` before landing — the earlier review was
not treated as sufficient evidence on its own. The safety ordering the draft was
rewritten around is preserved intact: stop the app, copy the whole `auto_backup`
folder out **before any restart** (rotation keeps 7 and the `< 100` skip counts
the catalog, so an emptied database still snapshots and still deletes a real
one), rename the current database rather than overwrite it, carry the
`-wal`/`-shm`/`-journal` sidecars with it, and restore one snapshot at a time.

**Documentation only.** No Python, JavaScript, workflow, schema, test, inventory,
dependency or generated file changed. The test inventory is byte-identical.

**Explicitly NOT authorized by this signature and NOT taken here:** an in-app
restore feature, any backup or runtime behavior change, **D4**,
`scan_export_bounds()`, the `utils/rep_range_integrity.py` docstring follow-up,
`needs:`/`continue-on-error:` deep-gate work, and Dependabot PRs **#395–#397**.
D4 and the `js-unit` half of D2 stay unsigned; the next scheduled deep-gate run
is still **2026-08-24**.

**2026-08-21 — #402 merged; `origin/main` is at `1f9c05a`.**
**[UPDATED 2026-08-21 — this block carried the `(LATEST)` marker until the
block above was written; `origin/main` has since moved to `4d53487` (#403).
Nothing below is edited except the annotations marked `[UPDATED 2026-08-21]`.]** All 18
checks are green on that commit. Take no automatic feature action from this file.

| PR | Commit | Terminal result |
|---|---|---|
| **#401** | `96b3ef2` | Docs only — the post-#400 reconciliation, i.e. the 2026-08-20 block below. |
| **#402** | `1f9c05a` | Tests only, shipped as squash `1f9c05a`. Changed `tests/test_release_workflow_contracts.py` and the two generated inventory files, nothing else. The **five** `deep-gate.yml` jobs `full-e2e`, `first-install`, `empty-schema`, `old-db-migration` and `dependency-health` are now contract-pinned against **any** job-level `if:` key — the key alone is the violation, so a next-line value or a tab after the colon is caught too — plus a census test pinning the job **ids**, which a `== 7` count floor cannot do against a rename. |

`visual-linux` is untouched and remains the **deliberately conditional
exception**: its condition stays pinned by #400 as the exact disjunct set
`{github.event_name == 'schedule', inputs.run_visual}`, with `&&` barred by name.
`frozen-windows` retains its prior unconditional protection from the
`PACKAGED_CALLERS` delegation contract; #402 reads its id back out of that mapping
rather than repeating it.

**#402 changed no workflow file and no runtime behavior** — `.github/workflows/`
is byte-identical to the commit before it. Inventory moved by six collected
nodes: that contract file **44 → 50**, deterministic total **2740 → 2746**, file
counts unchanged at **123**/**124**. The five representative mutations
(`if: ${{ false }}` after each job's `name:`) were **false greens before the
packet** and are each killed individually now.

**Named by #402, unmeasured, not authorized:** `needs:` and a job-level
`continue-on-error:` are two further shapes that could stop one of these five jobs
from gating. Neither is a demonstrated false green and neither is an authorized
packet — each requires its own mutation proof first.

**Still open and unauthorized:** the `scan_export_bounds()` numeric `min > max`
behavior decision, and the related `utils/rep_range_integrity.py` docstring
correction. **D4 and D7 remain unsigned and `README.md` remains untouched.**
**[UPDATED 2026-08-21 — D7 is now SIGNED and the recovery section landed in
`README.md`; see `TESTING_STRATEGY_PLANNING.md` §8.1d. D4 and the two
still-open packets are unchanged.]**

**2026-08-20 — four PRs merged on `origin/main` at `81771d1` and no
status surface recorded them. This pass is the record.** All 18 checks were green
on that commit. **[UPDATED 2026-08-21 — this block shipped as #401 (`96b3ef2`);
`origin/main` has since moved to `1f9c05a` (#402), recorded in the block above.
Nothing below is edited except the annotation marked `[UPDATED 2026-08-21]`.]**
Take no automatic feature action from this file.

| PR | Commit | Terminal result |
|---|---|---|
| **#393** | `eff4362` | Register rows **X11, X12 and X13** RESOLVED — attribute-only WCAG 4.1.2 naming fixes on `/progression`, `/volume_splitter` and `/workout_log`. No `color-contrast` count moved; no baseline regenerated. New row **X16** recorded as documented-but-deliberately-unregistered. Owner-deferred set is now **X7–X10 and X15**. |
| **#394** | `c208745` | The **FINDING-1 residual** is closed at both user-visible surfaces: a poisoned rep range now names the routine and exercise to repair, and Plan-editor repair works whichever rep column is edited first. No calculation file, schema, status code or JSON envelope key changed. |
| **#399** | `280c211` | Tests only. Seven false-green shapes closed in the deep-gate / release workflow contract (13 mutation arms, all 13 missed beforehand). Its squash subject says "five" — the packet outgrew that count and the subject was never rewritten. |
| **#400** | `81771d1` | Tests only. Closed the two shapes #399 named and did not reach: `visual-linux`'s `schedule` disjunct, and `steps()` returning `[]` on a 4→6-space reindent. |

**Preserved as future packets, none authorized:** job-level `if:` protection for
the **five** unpinned `deep-gate.yml` jobs (`full-e2e`, `first-install`,
`empty-schema`, `old-db-migration`, `dependency-health` — #400's body says "six",
which is wrong); the `scan_export_bounds()` numeric `min > max` behavior
decision; and the related `utils/rep_range_integrity.py` docstring correction.
**D4 and D7 remain unsigned and `README.md` remains untouched.**
**[UPDATED 2026-08-21 — the first of those three SHIPPED as #402 (`1f9c05a`); the
count of five, and the reason it is five and not six, were correct and are what
#402 implemented. The `scan_export_bounds()` decision and the
`utils/rep_range_integrity.py` docstring correction are still open and still
unauthorized, and D4/D7 are still unsigned.]**
**[CORRECTED later on 2026-08-21 — D7 was signed that same day (§8.1d) and the
recovery section landed in `README.md`, so both this annotation and the sentence
above it are stale on D7. Only D4 is still unsigned; the two open packets are
unchanged.]**

**2026-08-14 — the pack's docs-only tail has landed and canonical truth
is reconciled against `origin/main` at `fbb76f5`.** **Eleven** PRs merged after
`7e4c1e9` (#352), the pack reconciliation that recorded the checkpoint described
below — every one squash-merged on green required checks.

Terminal outcomes for the set this reconciliation was asked to record:

| PR | Commit | Terminal result |
|---|---|---|
| #351 | `5a03d47` | Duplicated body-map caveat removed from `templates/_fatigue_heatmap.html`, mapping test added, and **all twelve** fatigue visual captures regenerated (six Linux, six win32). The stale-Linux consequence is discharged. |
| #357 | `e84d19c` | **P2.7 closed** — `tests/test_consult_adapter.py` derives its escape path from `REPO.name`, so the node passes in the canonical main checkout as well as in worktrees and on CI. |
| #358 | `a83a452` | Canonical council plan path pinned. |
| #359 | `fbb76f5` | Seven fatigue guardrails repointed from the `utils/fatigue.py` facade to `utils/_fatigue/per_muscle.py` / `utils/_fatigue/core.py`. **The owner widened it past documentation-only**, so `scripts/fatigue_stage4_observer.py:265` — the one code-side guardrail, printed on the `--analyze` signal path — was corrected in the same PR. **Nothing about it is left pending.** |
| #360 | `56316c5` | Executable runbook for validating the first scheduled deep-gate run. |
| #361 | `a224b39` | Root `AGENTS.md` added to the agent-workflow contract surface; retired known-red dropped from the test-strategist charter. Discharges the cross-model plan's Packet C. |
| #362 | `52331bf` | **Testing Phase-2 Packet C (strict console) SHIPPED** — `e2e/console-guard.ts` fails on every console error and page error, with anti-catch-all allowlist rules enforced at setup; three specs migrated. No production file, no test-node change. |

Recorded for completeness, same run: `7f8549c` (#353) product-docs caveat
discharged; `52c5a78` (#354) recorded P2.7, which #357 then closed; `710ef61`
(#355) Volume Splitter readiness oracle strengthened; `5177176` (#356)
`scripts/**` routed in the quality gate.

**Testing Strategy Phase 2 is COMPLETE (2026-08-14).** Packet **E** shipped as
#364 (`ebfa716`) and Packet **F** as #365 (`a49da8d`), closing register rows X1
and X6; #367 (`a64ea76`) recorded the X1/X2/X6 decisions, with **X2 declined**;
#368 (`9be1a3f`) migrated four more specs onto the strict console guard; and
**Packet D (axe) shipped as #366 (`f627161`)**, which closes the phase. Packet D
took the owner's **explicit-exception path** — axe executes every WCAG rule and
each existing violation is pinned by surface, rule id and exact node count, not
suppressed. No production or visual-baseline file changed across E, F or D.
Remaining accessibility debt is **X7–X13 and X15, all owner-deferred**; see
[`testing_phase2/A11Y_EXCEPTIONS.md`](testing_phase2/A11Y_EXCEPTIONS.md).
**[UPDATED 2026-08-17 — the debt set has shrunk.]** X11, X12 and X13 were taken
up and shipped in #393 as attribute-only WCAG 4.1.2 naming fixes, leaving
**X7–X10 and X15**. **[UPDATED 2026-08-20 — one row is missing from that
sentence.]** The same packet recorded a new row **X16** — the post-Calculate
`/volume_splitter` results wrapper, WCAG 2.1.1 — documented and **deliberately
not registered**, because an `AXE_REGISTER` entry pins the whole findings list
and would drag in data- and viewport-dependent contrast nodes. It is outstanding
accessibility debt without being part of the owner-deferred set.

**Shipped later the same day.** The **release/tag pipeline is no longer
deferred**: it shipped as Packet **R1** — #374 (`5222db2`), whose post-merge
dry-run evidence was recorded in #375 (`d3c3436`) — under
[`DECISIONS.md`](DECISIONS.md) **ADR-007**. Its `push: tags` trigger has still
never fired, and §7.3 entry criteria 2 and 3 are unmet, so Testing Phase 4 stays
open — a first real tag would not close it.

**Still open, unchanged by that.** The heavy `$orchestrate` mechanism stays
deliberately unimplemented. **The weekly deep-gate cron fired for the first time on
2026-08-17 and was green.** It ran R2-b's file, so it is not evidence about the pre-#388
file, which the 2026-08-16 override forfeited for good. Next scheduled run **2026-08-24**,
judged at job level with `visual-linux` executed. Run id, SHA, timings, step-level compare
proof and the scheduler-delay note live in one place — do not restate them here:
[`release_pipeline/PLANNING.md`](release_pipeline/PLANNING.md) § The first
`schedule`-event run.

No pack feature branch, worktree, local evidence artifact, or database is a
cleanup target.

> **Superseded 2026-08-14, later the same day, on four claims.** The block
> below is the feature-PR checkpoint record and is otherwise accurate. Four of
> its statements have been overtaken and are corrected above: *"strict-console
> Packet C and axe Packet D remain queued"* — Packet C shipped as #362 and
> Packet D as #366; *"Linux fatigue baseline follow-up #351 is an open
> clean/green draft"* — #351 merged as `5a03d47`; *"Sessions 1–9 have terminal
> outcomes through #350"* — the run continued through #362; and *"The release/tag
> pipeline remains deferred"* — it shipped as #374 (`5222db2`).

**2026-08-14 — the August integration pack is at its verified
feature-PR checkpoint; canonical truth is being reconciled.** Sessions 1–9 have
terminal outcomes through #350 (`d93a3dd`). The shipped set includes test
honesty, the profile-estimator Pyright slice, the compiled-CSS drift gate,
Fatigue Stage-4 closeout and heatmap, the product-reference suite, local-first
assets, cross-model consult, the routine-change superset reset, and two
page-readiness slices.

This is not a claim that every proposal in those source plans shipped. Testing
Phase-2 Packet A landed as #342; strict-console Packet C and axe Packet D remain
queued. The heavy `$orchestrate` mechanism remains deliberately unimplemented.
The release/tag pipeline remains deferred, and the first scheduled deep-gate
run is still due 2026-08-17 03:17 UTC. Linux fatigue baseline follow-up #351 is
an open clean/green draft owned by its existing session.

No pack feature branch, worktree, local evidence artifact, or database is a
cleanup target. Session 10 owns only the docs reconciliation and must leave all
of them in place.

> **Superseded 2026-08-14.** The P3 termination block below remains binding for
> P3, but stopped being the repository-wide latest objective once the August
> integration pack shipped.

**2026-08-02 — CSS closeout proposal P3 is TERMINATED at `P3-a0`. There
is no active P3 packet and none may be dispatched.**

Owner decision, 2026-08-02. **`P3-a0` is the arc's only implemented packet.
`P3-a1` is NOT funded; `P3-b`, `P3-c`, `P3-d` and `P3-e` are NOT authorized. P3
ends when a0 merges, and reopening it requires a new owner decision** — the
Gate 0 / Gate 1 sign-off confers no residual authority over any later packet.

**Why.** `P3-a0` was a read-only audit commissioned to price the rest of the arc
before any instrument existed. It assessed all nineteen committed
`scripts/css_audit/` tools and found the price is **nine new tools, not the seven
Plan v1 proposed** — the assessment raised the estimate rather than lowering it.
Against the yield already accepted at **Q6** (*"a small certified deletion plus a
reusable instrument, not a gutted file"*), that does not clear the cost/risk bar.

**a0 wrote no production CSS and no snapshot.** `static/css/**` and
`e2e/__screenshots__/**` are byte-identical to `main`; **R4 still forbids
unlinking `theme-dark.css`** and is unaffected by the termination.

**Three outputs outlive the arc — do not re-derive them:** the **ceiling emitter**
`scripts/css_audit/p3_ceiling.py`, which mechanised 14 prose deletion ceilings and
proved `tests/test_css_cascade_contracts.py:1007` is a bare substring check
satisfied by **4** lines rather than 2 (so `.frame-header`'s dark blur override is
deletable with that gate green); the **nineteen-tool assessment**, which is the
artifact that terminated the arc; and the **N8 denominator reconciliation** —
11 failed + 57 passed + **16 that never ran** = 84, making **`totalCount: 11` a
FLOOR**, which the separate Linux baseline recovery packet must carry.

Sized but not implemented and not tied to P3: the **Q10 blind-spot-register
repair**, ≈170–200 lines, standalone, gated by full pytest alone.

> **Scope note.** Under the owner's final **D3** ruling a terminal packet may write
> **only** the lead block and the next-step section of the three status documents.
> The WP4.4 execution-order block later in this file still calls P3 *"planning
> only, Gate 0 and Gate 1 both unsigned"*; **a0 left it untouched rather than
> exceed its authority. Read it as superseded by this entry.**

Full record: [`CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md`](CSS_THEME_DARK_P3_A0_AUDIT_EVIDENCE.md)
and [`css_theme_dark_p3/PLANNING.md`](css_theme_dark_p3/PLANNING.md).

**2026-08-01 — WP4.4 IS COMPLETE; the arc is closed at `k`.** Every
packet is merged: `a` (#187, `46e340e`), `c` (#188, `1b13bfc`), `b` (#192,
`3bec677`), `e` (#195, `1346a35`), `d1` (#197, `59e5b10`), `f1` (#199,
`1127486`), `d2` (#201, `0a912d9`), `f2` (#205, `6a5465c`), `g` (#207,
`4b7ca58`) with its terminology correction (#209, `a895cb0`), `h` (#208,
`b2b1cb7`), the visual-harness prerequisite (#211, `1019d34`), **`i` (#212,
`5f7b5ac`) with its oracle corrective (#215, `666471e`)**, and **`j` (#216,
`47c7687`)**.

**Arc result: −539 net lines across the seven shared bundles, 0 observable
change.** The arc-base-to-arc-end computed differential reports **0 differences
across 2,275,668 values** in both themes. Stylelint **2,883 → 2,751 (−132)**,
every surface down; `!important` −48. See
[`CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md`](CSS_PHASE4_WP4_4_K_INTEGRATION_EVIDENCE.md)
for the full report, the ledger reconciliation, and three proposals left open
for the owner (the incomplete Linux inherited-reds ledger, the N10
`QUALITY_GATE.md` row, and the `:where()` inertia finding in `theme-dark.css`).

Deferred and untouched: the 235 declarations WP4.4-h withheld, the superset
dark-tint gap, and unlinking `theme-dark.css`.

**The fresh N4 owner decision has been given.** Packet i is proof-first and may
narrow or use the pre-authorized N3 abandonment; either outcome continues
sequentially through j and k. Both required pre-change inventories are merged
([Inventory A](CSS_PHASE4_WP4_4_N4_INVENTORY_A_IS_FAMILY.md),
[Inventory B](CSS_PHASE4_WP4_4_N4_INVENTORY_B_REGIONS_ABC.md)) and the enumerated
repair shape is approved. Binding decisions, automatic fallbacks and genuine
hard stops are in
[`N4_CONTINUATION_AUTHORITY.md`](css_phase4_wp4_4/N4_CONTINUATION_AUTHORITY.md);
live restart state is in
[`EXECUTION_HANDOFF_I_K.md`](css_phase4_wp4_4/EXECUTION_HANDOFF_I_K.md).

The separate Packet-a decision is **defer**: do not re-pin the `@layer workout`
span or touch h's **235** withheld declarations during i–k.

**WP4.4-h** deleted **101 declarations**, **138 lines**, **20 `!important`
declarations**, **87 cuts** and **11 whole rules** from `components.css`
(SHA-256 after `883e6aa8…`). It withheld 235 behind the layer-span pin, 18
`.btn.btn-video` declarations for missing differential blast coverage, 2
removal-oracle withdrawals, and the 6 `.value-changed` declarations reachable
only through a JS-applied class (M10 / PR#3). The **`:is()` family: zero eligible
and untouched** — the whole family belongs to i. **Region H unchanged** (G9 holds
by construction: h wrote only `components.css`).

**The binding lesson from g + h, which no later packet may unlearn:** a
zero-winner ownership result is **not** a removal verdict. An inline-`!important`
sentinel proves reachability and probe integrity only. **Only a removal oracle
grants deletion authority.** g's census produced 342 zero-winner nominations;
h's removal oracle proved **35 of them live on removal**. Of the 336 that entered
the 264-context certification run: **35 removal-live / 180 `deadCertified` / 121
unmatched**; D384–D389 never entered it.

> **Superseded 2026-07-31.** This section previously announced WP4.4-f2 as LATEST
> with `g` next. `g` (#207), its terminology correction (#209) and `h` (#208)
> have since merged, and the arc is at the N4 hard stop.

**WP4.4-f2** consolidated three exact duplicate `navbar.css` source rules into
their existing generation owners. Style rules **193 → 190**, declarations
**692 → 690**, physical lines **1,536 → 1,533**. The single
`@layer navbar` block remains source-pinned at lines 6–883; layer membership,
all **93** `!important` occurrences, all **72** custom-property declarations,
and `--nav-gap` / `--nav-padding-y` / `--nav-padding-x` are unchanged.

Exact declaration-owner adjudication proved the merged scrollbar and
light-theme toggle background are live winners, mobile container `max-width`
and row gap remain live, and the desktop base `max-width` remains overridden.
The exhaustive post matrix had **486/486** candidate, restore and focus checks
green across 11 routes, both themes, 20 breakpoint-edge widths, navigation
states, forced interactions, reduced motion, contrast and print. The M6a
control observed and externally settled **7** genuine `CSSTransition` objects;
its `--no-settle` red path failed as required.

Gates: contracts **62 passed**; full pytest **2,271 passed / 1 skipped**;
required functional/navigation/accessibility Chromium **127 passed** plus
`fatigue.spec.ts` **8 passed**; visual **65 / 1 ledgered red** at
875/882/875 px inside the established band; Stylelint **2,849 → 2,844 (−5)**
over the seven surfaces, with no category increase. All 14 CI checks on PR #205
passed. Evidence:
[`CSS_PHASE4_WP4_4_F2_NAVBAR_EVIDENCE.md`](CSS_PHASE4_WP4_4_F2_NAVBAR_EVIDENCE.md).

**WP4.4-d2** adjudicated all **51** `!important` annotations left in
`a11y.css` after `d1`. Exactly one was certified and de-weighted:
`.is-invalid { box-shadow }`. The declaration remains present and remains the
effective owner wherever it owned before; only its priority changed.
`!important` **51 → 50**, declarations **240 → 240**, style rules **94 → 94**,
custom properties **17 → 17**, `@layer` **0 → 0**. No selector, value,
declaration, rule order or media placement changed.

The second apparent candidate,
`.selection-field.has-validation-error label { color }`, **failed**
certification and retains its `!important`. In a doubly-matched ancestor stress
state, de-weighting moves declaration ownership to the later
`pages-workout-plan.css:4449` rule in **15/15** light-mode measurements even
though the computed value remains the same. The broad census missed this
because its synthetic only applied `has-validation-error` to
`.selection-field`, never to `.cascade-dropdown-wrapper`. **A census verdict is
a nomination, not certification; declaration-owner adjudication against the
exact competing structure must follow it.**

The packet also proved that the arc's CSS-only M6a transition suppressor is
beatable: an unlayered universal `transition: none !important` loses both to
layered `!important` under layer-order inversion and to more-specific unlayered
`!important`. The packet's oracle bypassed that cascade with the Web Animations
API and added CTLF, whose `--no-settle` red path fails as designed.
`scripts/css_audit/runtime_probe.mjs` still carries the beatable suppressor and
must not be treated as transition-safe until its owning packet repairs it.

Gates: contracts **22 passed, 22/22 red-path proven** with every source restored
sha256-identical; full pytest **2,268 / 1 skipped**; nine required Chromium
specs **127 passed**; visual **65 / 1 ledgered red** at 875 px (882 retry),
inside the established band; Stylelint **2,850 → 2,849 (−1)** with no other
rule increased. CI on PR #201 passed all 14 checks. Evidence:
[`CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md`](CSS_PHASE4_WP4_4_D2_A11Y_EVIDENCE.md).

**WP4.4-f1** deleted **one rule from `navbar.css`, −6 lines, 0 insertions** —
`body:not(:has(#navbar)) .navbar`. Unreachable **by construction**, not only by
census: `navbar.css` is linked from exactly one template (`base.html:22`), that
template renders `#navbar` unconditionally (`base.html:36`), and every other
template extends it — `error.html` included. So every document loading the
stylesheet contains `#navbar` and the guard can never be satisfied. Runtime
census agreed at **0 matches in 522/522 contexts** (11 routes × 2 themes × 14
widths covering every breakpoint edge in the file's 11 distinct `@media`
conditions, plus collapsed/expanded, dropdown open, CDP-forced
hover/focus/active, reduced-motion, contrast and print).

**The plan projected −150 to −400 lines; the packet delivered −6, and that is
correct.** A projected line reduction is not an acceptance criterion. Scope was
not widened to produce a larger diff.

Gates: contracts **16 passed, 16/16 red-path proven** with a **sha256-identical**
restore; full pytest **2,262 / 1 skipped** (`main` collects 2,247, so +16 is
exactly the new file); nine required specs **127 passed**; visual **65 / 1
ledgered red**; owner differential **0 / 64,961**; motion **0 / 306,864**;
same-CSS control **0 / 17,048** on both sides; sentinels **4,270 / 4,270** took
effect and reverted on all three runs. Stylelint **2,851 → 2,850 (−1)**, no
category increased. `!important` **93 → 93**, custom properties **72 → 72**,
`@layer` blocks **1 → 1**, layered rules **103 → 103** (N2 held).
Evidence: [`CSS_PHASE4_WP4_4_F1_NAVBAR_EVIDENCE.md`](CSS_PHASE4_WP4_4_F1_NAVBAR_EVIDENCE.md).

**Three `f1` findings that bind later packets:**

1. **The "three live generations" count is established, not assumed** — layered
   scoped (103 rules), legacy `.navbar` fallback (2), unlayered override tail
   (89), plus 5 `@keyframes` steps.
2. **Generation B is NOT dead legacy, and `navbar.css:885` / `:893` lie about
   it.** The `.navbar` rule is **unlayered** while `#navbar { position: sticky }`
   is inside `@layer navbar`; for normal declarations the unlayered class
   selector beats the layered ID selector, so `position: fixed` is what the
   browser computes. Deleting it would unpin the navbar. Retained and
   contract-pinned, layer membership included.
3. **A relaxation that is not provably a superset manufactures deadness.** The
   first census run nominated 39 rules; **38 were artifacts** (`>` combinators
   corrupted, substitution inside `:not()` yielding invalid `:not()`,
   `@keyframes` steps parsed as rules, and a CDP listener attached after
   `CSS.enable` reporting 0 matched declarations). Each was caught by a control.

**Known-red update:** the animated-logo band is **875/882 ∪ 1,039/1,046**. `f1`
measured 875 (882 retry), matching `b` and `c`; a same-CSS pixel control with
`navbar.css` byte-identical to `main` produced the identical count, so it is
packet-independent.

**Deferred by `f1`, owner-gated, do NOT act:** 155 matched-but-never-winning
`navbar.css` declarations are **uncertified** (the owner sweep's
`!important`/layer arbitration was never validated against a known-live
*overridden* control) and are retained whole; and the six duplicate
`#navbar > .container-fluid` rules plus near-duplicate `@media` conditions are
consolidation, which is **`f2`'s exclusively**.

**WP4.4-d1** deleted **14 rule blocks from `a11y.css`, −99 lines, 0
insertions** — a *superseded generation* of the scale / accessibility UI
(`.scale-control`, `.scale-btn-group`, `.scale-labels`, `.accessibility-menu`,
`.accessibility-section*`), leaving the live compact generation
(`.scale-control-compact`, `.scale-btn-compact`, `.scale-indicator`) intact.

Full-selector runtime census was **0 for all 14 candidates across 164
contexts** (2 themes × 10 widths × 8 `data-scale` levels, plus print and
reduced-motion). The **oracle validity gate passed first**: the known-live
compact generation reported census > 0 in **160/160** contexts, so the oracle
demonstrably sees rules that render. `[data-visual-scale-control]` is a
registered visual blind spot, so computed-style and declaration-owner evidence
were load-bearing, not pixels.

Gates: contracts **16 passed, 15/15 red-path proven**; full pytest **2,245 / 1
skipped**; nine required specs **127 passed**; visual **65 / 1 ledgered red**;
Stylelint **2,857 → 2,851 (−6)**, no category increased. `!important` **51 →
51**, custom properties **17 → 17**, `@layer` **0 → 0** — the d1/d2 boundary held
by construction, since all 14 deleted rules contained zero `!important`.
Evidence: [`CSS_PHASE4_WP4_4_D1_A11Y_EVIDENCE.md`](CSS_PHASE4_WP4_4_D1_A11Y_EVIDENCE.md).

**Two `d1` findings that bind later packets:**

1. **State the post-deletion flip by source identity, never as "the rule went
   blind"** — that phrasing cannot be distinguished from "the oracle stopped
   working". `d1` proved its two residual `.scale-control` matches resolve via
   CDP `CSS.getMatchedStylesForNode` to the **retained** `@media print` rule at
   source lines 329–331, and to **zero** rules on `screen`. Separate four
   things: deleted rule identity, selector text, retained source rule, computed
   declaration owner.
2. **Substring assertions masked by duplicate selector text are a recurring
   defect class**, seen in both `e` and `d1`. Use occurrence-count or
   source-shape assertions.

**Recorded, not acted on:** `.scale-btn[data-scale]` has runtime census **0** —
`accessibility.js:144` and `:202` query an empty set, a second dormant JS path.
Those 11 bare `.scale-btn` rules were **never audited as `d1` candidates**
(the static pass wrongly treated a JS *query* as proof of reachability) and are
retained untouched. Deleting them needs its own census and its own packet.

**WP4.4-e** deleted **34 rule blocks from `layout.css`, −218 lines, 0
insertions**. The plan carried one candidate into the packet (`body.dark-mode`);
the audit found **42** fully-unreachable rules. `body.dark-mode` was re-proved,
not inherited: the rule *is* functional (all seven `--tbl-*` tokens change in
11/22 contexts when the class is applied) but its selector is never satisfied —
`<body>` never carries the class, and `darkMode.js:64` sets `data-theme` on the
root element. It was deleted on **unreachability**, not the ordinary non-winner
rule, which does not apply to custom properties. The tokens keep their live
`[data-theme="dark"]` definitions, now contract-pinned.

Evidence: 0 declaration-owner differences / 64,961 records; 0 motion /
306,864; 2 paint / 340,960, both the ledgered Welcome blur reproduced by the
before-run's own same-CSS control. Census 0 for all 42 candidates across 11
routes × 2 themes × 16 widths. Gates: contracts **13 passed, 13/13 red-path
proven**, full pytest **2,230 / 1 skipped**, seven required specs **89 passed**,
visual **65 / 1 ledgered red**, Stylelint **2,875 → 2,857 (−18)**, no category
increased. `!important` 24 → 24 and `@layer` 0 → 0.
Evidence: [`CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md`](CSS_PHASE4_WP4_4_E_LAYOUT_EVIDENCE.md).

**Nine rules were deliberately deferred** — the `.tbl-show-*` / `.tbl-hide-*`
family. Census is 0 and six of nine are oracle-visible, but three declare
`display: block` (a bare div's initial value), so no control element can
distinguish them. Splitting the family would leave `@media` overrides targeting
classes with no base rule, so it is deferred whole and pinned by exact
occurrence count. **Do not erode it rule by rule.**

**Execution order — fully discharged:**

```
a ✔ → c ✔ → b ✔ → e ✔ → d1 ✔ → f1 ✔ → d2 ✔ → f2 ✔ → g ✔ → h ✔ → N4 ✔ → helper ✔ → i ✔ → j ✔ → k ✔
```

**No packet in this arc is active or next. Do not dispatch one.** Of the three
closeout proposals, **P1 and P2 are owner-approved and merged** — `d543a4b`
(PR #223, ledger schema v2, 11 reds across two spec files) and `4b0670b`
(PR #222, the `static/css/**` gate row plus the derivation bullet that closes
F21). **P3** (`theme-dark.css` `:where()` inertia) is **TERMINATED**: both gates
were **signed 2026-08-02**, **`P3-a0` shipped** (PR #280, squash `cd93480`), and
the owner then **terminated the arc at a0** — a0's nineteen-tool assessment priced
`P3-a1` at **nine** new tools against the small deletion yield already accepted at
Q6. **`P3-a1` … `P3-e` carry no residual authorization; reopening requires a new
owner decision.** **No production CSS was ever touched** — a0 was read-only with
respect to `static/css/**`, so the arc ends with `theme-dark.css` byte-identical
to where it started. Full record:
[`css_theme_dark_p3/PLANNING.md`](css_theme_dark_p3/PLANNING.md).

> **Superseded 2026-08-01.** This block previously showed `i ▶ → j → k` and read
> *"Packet i is active."* Correct on 2026-07-31; stale once #212, #215, #216 and
> #217 merged. The Current Objective block at the top of this file was updated by
> packet `k` but this block was not, so the execution source of truth asserted
> both "the arc is closed" and "packet i is active" at once.
>
> **Superseded 2026-07-31.** This block previously read *"`g` is next"* and drew
> the order with `g → h` still pending. Both merged (#207/#209 and #208).
>
> **Superseded 2026-07-30.** This section previously announced
> WP4.4-d2 as LATEST with `f2` next. `f2` has since merged in PR #205.
>
> **Superseded 2026-07-29.** This section previously announced
> WP4.4-f1 as LATEST with `d2` next. `d2` has since merged in PR #201.
>
> **Superseded 2026-07-29.** This section previously announced WP4.4-d1
> as LATEST with `f1` next, and described `f1` as "deliberately last among the
> pure-deletion packets because navbar layering, global exposure and the
> animated-logo oracle make it the riskiest". That framing was correct and is
> retained as the `d1`-boundary record; `f1` has since merged in PR #199.

> **Superseded 2026-07-29 (later).** This section previously announced WP4.4-b
> as LATEST with `e` next. `e` has since merged in PR #195.

> **Superseded 2026-07-29.** This section previously read *"WP4.4-c is complete
> in PR #188 … `b`, `d1`, `e` and `f1` are eligible, none started, each still
> needs explicit owner direction."* That was accurate when written on 2026-07-28
> and is retained here as the `c`-boundary record. It went stale when PR #192
> merged `b`: an agent obeying it would have re-dispatched an already-shipped
> packet, which is exactly the `/status` drift class that previously caused
> re-dispatch at WP3.5 and WP4.3g.

**Separate owner-directed runtime maintenance (2026-07-29):** the repository
minimum is now Python 3.14.6 for source, CI, type analysis, and packaged builds.
This does not authorize or reorder any WP4.4 packet; see ADR-003.

**Superseded (2026-07-27):** *"WP4.3j-d-hover-paint is complete in PR #186; then
stop."* That instruction was correct when written and is retained below as the
Workout Log record. It stopped being the current objective when Gate 1 was
approved and WP4.4 began executing; this file, `MASTER_HANDOVER.md` and
`REFACTOR_PLAN.md` had drifted apart, which is what `/status` now reconciles.

**WP4.3j-d-hover-paint (PR #186) — complete, and the Workout Log boundary.**
The packet removes exactly four cascade-dead declarations from the two retained
Region G Workout Log hover rules: light/dark `background` and `box-shadow`.
Both full selector lists and both live filters are byte-identical; the rules are
now filter-only. `!important` **217 → 213**.

The real-hover differential is green across light/dark ×
desktop/tablet/mobile: **11,016 records, 0 computed-value differences, 0
declaration-owner differences, 6/6 byte-identical frame captures**. Known-live
filter controls passed 6/6 before and after. Same-CSS controls were 0 on both
sides; resolution self-check was **2,924 / 0 per side**; sentinels were **24/24
effective per side**. Positive control: **408 records lost candidates, 0 gained
any**, while rule counts remained unchanged.

The prior Region H hash contract accidentally anchored on an earlier prose
mention and covered Region G. Its unique banner anchor and corrected 282-line
span are now explicit; the old defect caused false failures, never false passes.
The new hover contract pins both selector lists and filter-only bodies and goes
red against the historical bundle, a removed live filter, and a restored
background.

Gates: visuals **6/6** update-free, CSS/visual contracts **33/33**, focused
functional Chromium **33/33**, full pytest **1,859 passed / 1 skipped**.
Stylelint total **5,498 → 5,490**, focused **431 → 423**, no category increased.
Evidence:
[`CSS_PHASE4_WP4_3J_D_HOVER_PAINT_EVIDENCE.md`](CSS_PHASE4_WP4_3J_D_HOVER_PAINT_EVIDENCE.md).
After this packet lands, await owner direction; do not begin further Workout Log
cleanup or WP4.4.

**2026-07-27 — WP4.3j-c-dead SHIPPED: the 37 cascade-dead header and
table-cell glass rules the j-c audit nominated are deleted.** Regions D (dark
cell glass, 3 rules), E (positional metric-lane glass, 20), F (dark-mode
visibility, 8) and six of the eight region-G final-override rules are gone from
`static/css/pages-workout-log.css`. **Lines 2,025 → 1,621 (−404); 69
declarations; `!important` 285 → 217 (−68).**

**The audit was re-proven, not inherited.** The branch was cut fresh from merged
`main` at `69dcf5e`. A pre-deletion sweep confirmed all 37 rules resolve to
exactly one CSSOM rule, all 37 genuinely match live elements, and **none ever
wins** any audited record. Before vs after: **0 computed-value differences and 0
declaration-owner differences across 15,336 records**, and **6/6 zero-diff**
`.workout-log-frame` captures (byte-identical PNGs). Positive controls that the
change reached the browser: matching-rule count fell by **exactly 37** in every
context, and **5,496 records lost candidates while 0 gained any**.

Retained on purpose and contract-asserted: the two region-G hover rules and
their winning `filter: saturate(…) brightness(…)` (51 records each); regions A,
B, C, H and I, with region H locked byte-for-byte by sha256; the nine unverified
declarations; the five empty media shells and every other excluded responsive
family. Gates: visuals **6/6** update-free (no baseline written), contracts
**32/32** with the red path proven five ways, focused functional Chromium
**33/33**, full pytest **1,858 passed / 1 skipped**. Stylelint total **5,784 →
5,498** and focused **717 → 431** (both −286), with `no-descending-specificity`
**200 → 38** — the biggest category move of the Phase-4 arc — and **no category
increased**. Evidence:
[`CSS_PHASE4_WP4_3J_C_DEAD_EVIDENCE.md`](CSS_PHASE4_WP4_3J_C_DEAD_EVIDENCE.md).

**Two measured corrections to the j-c audit.** Its projected `!important`
movement of 71 (`285 → 214`) counted region F over a line span that also covers
the retained editable-input and badge rules; the eight region-F rules carry 8,
so the real movement is 68 (`285 → 217`). And of the nine unverified
declarations it places "all in region H", eight are — the ninth is the region-A
header `text-transform`. Both regions are retained, so the scope is unaffected.

**Method rule added: *every deadness sweep must carry a known-live control.***
Two new oracle defects each made rules look deader than they are — `propKey`
enumerates expanded longhands, so matching authored shorthand names against it
hid 29 of the 37; and Chrome re-serializes `:nth-child(even)` as
`:nth-child(2n)`, hiding the other 13. Both were invisible to the "does it ever
win?" question, which answered 0 either way. What exposed them was the two
retained hover rules — known live winners — reporting 0 wins under the broken
matcher.

**2026-07-27 — WP4.3j-c was the preceding packet, an evidence-only audit that
changed no production file.** It audited the
overlapping header and table-cell glass systems in
`static/css/pages-workout-log.css` across all 17 columns, both themes, and
desktop/tablet/mobile.

Result: **the Workout Log table is painted by the shared `components.css`
`.table.table-calm` system, not by the page's own glass systems.** Of **322**
audited declarations in regions A–I, **227 never win anywhere**, **31** are live,
**55** are mixed, **9** are unverified, and **0** are winning-but-overpainted.
Regions **D (dark cell), E (metric-lane `nth-child` glass) and F (dark-mode
visibility)** are dead in their entirety. The cause is that the shared selector's
`:is()` carries an ID arm and so exports `(1,3,1)`/`(1,3,2)` ID-level
specificity, which no ID-free page-local rule can reach no matter how much
`!important` it carries. The one page-local family that *does* render — the
region-H lane rules — is the only one written with an ID, at `(1,5,2)`.

Gates for the audit itself: same-CSS pixel control **0 differing pixels in 6/6
contexts**, resolution self-check **9,358 checks / 0 mismatches**, sentinel
probes **222/222 verified effective**, **0** unexplained zero-diffs, **15,336**
ownership records. Evidence:
[`CSS_PHASE4_WP4_3J_C_AUDIT_EVIDENCE.md`](CSS_PHASE4_WP4_3J_C_AUDIT_EVIDENCE.md).

The audit **corrects a claim in the shipped WP4.3j-a evidence**: the eight
`color: #e0e0e0 !important` declarations in the dark-mode visibility block are
cascade-dead, not live winners — the computed dark cell colour is
`rgb(238, 241, 246)` from `components.css` at `(1,4,2)`. The j-a packet itself is
unaffected; only its stated reason for retaining that block was wrong.

A deletion candidate is **documented with exact selectors, oracle and gates —
37 rules, 436 lines, 71 `!important` — and is NOT authorized.** Do not start it
without new owner approval.

**Method rule added:** *a probe that changes nothing proves nothing.* Four
separate oracle defects in this packet each produced confident false "dead CSS"
before being caught — a `var()`-bearing shorthand being invisible to longhand
CSSOM queries, an injected sentinel losing the cascade, a running CSS transition
outranking important author declarations, and `page.screenshot` not painting
clip regions beyond the viewport. Every negative pixel result must carry
positive evidence that the probe worked.

**2026-07-26 — WP4.3j-b-dead was the previously shipped packet; WP4.3j-a is
merged at `99dfee1` (PR #181), and WP4.3j-b was an audit-only, no-op
investigation.**

WP4.3j-b-dead is the deletion packet the j-b audit nominated but explicitly did
not authorize. It removed three inert responsive families from
`static/css/pages-workout-log.css` — the eight-query `RESPONSIVE FRAME
ADJUSTMENTS` block, the first ladder's `thead th` / `td` padding and type blocks,
and the base `.workout-log-frame` `padding: var(--frame-padding, 1.25rem)`
declaration. Lines **2,180 → 2,025**; `@media` **17 → 9**. Every j-b claim was
re-proven on a fresh branch cut from merged `main`: **385 declaration-instances
examined across 14 widths, 0 ever a winning owner**; before vs after **0
differing records / 504** and **14/14 zero-diff** frame pixels; invariants
measured identical at every probe (cell padding `12px 16px`, font size
`14.08px`, frame padding `0px`). Stylelint moved by **zero** (focused 717,
total 5,784, `!important` 285, no category increased) — the deleted declarations
triggered no rule, so the win is 155 non-rendering lines rather than a lint
score. Gates: visuals **6/6** update-free, contracts **31/31**, focused
functional Chromium **33/33**, full pytest **1,857 passed / 1 skipped**.
Evidence: [`CSS_PHASE4_WP4_3J_B_DEAD_EVIDENCE.md`](CSS_PHASE4_WP4_3J_B_DEAD_EVIDENCE.md).

Two oracle constraints carried forward: the **full-page pixel oracle is unusable
on this route** (a same-CSS control drifts at 10 of 14 widths inside the animated
navbar strip `y ∈ [18,40]` — scope pixel claims to the element under test), and a
specificity model that mishandles `:is()` or splits selectors on a naive comma
will **report an owner contradicting the computed value**. Retained on purpose
and contract-asserted: the `992px` overflow rule, page padding, delete-button and
icon sizing, routine-cell widths and typography, the late legend query, and the
five now-empty first-ladder media shells.

WP4.3j-a removed five overpainted dark-mode Workout Log table-cell declarations:
`!important` **292 → 287**, visuals **6/6** update-free, contracts **30/30**,
focused functional Chromium **33/33**, and full pytest **1,856 passed /
1 skipped**.

WP4.3j-b changed no production file. Its supposed duplicate `@media` ladders
proved to be different selector/property families, and browser ownership tracing
showed that the measured table padding/type declarations never beat the shared
important `components.css` table-cell rule. The measured frame-padding family
never beats `html body .workout-log-frame { padding: 0 !important; }`. The
`992px` table overflow, first-ladder page/button/routine families, and separate
legend query were not measured and remain unclassified. Exact evidence:
[`CSS_PHASE4_WP4_3J_B_EVIDENCE.md`](CSS_PHASE4_WP4_3J_B_EVIDENCE.md).

The root-cleanup / data-packaging track also remains CLOSED. All packets shipped,
all 225 checklist items in [`rootdircleanup.md`](rootdircleanup.md) are ticked,
and that closed record must not be re-executed.

The Phase-4 CSS track is paused and owner-gated after WP4.3j-d ships. The j-b
and j-c dead-CSS packets are closed, and WP4.3j-d removes the final four
authorized Region G hover-paint declarations. WP4.4 may review the shared
`:is()` specificity trap, but it is not authorized or started. The ten WP4.3i
deferred interaction-state declarations and WP4.3i-c Page Header contract remain
untouched.

> **Superseded as to WP4.4 (2026-07-27 / 2026-07-29).** The sentence "WP4.4 …
> is not authorized or started" was true on 2026-07-26 and is retained for the
> j-b record only. Gate 1 approved WP4.4 on 2026-07-27; `a`, `c` and `b` have
> since merged. The later N4 continuation authority supersedes this paragraph's
> old statement that packet i was unauthorized. The WP4.3i and separate Workout
> Log cleanup statements remain current.

WPB.4 also remains unimplemented and owner-gated: it requires retaining one
synthetic `Unassigned` session, an explicit unresolved-denominator decision, and
intentional review of the exact golden diff before any behavior change.

## Next Action

> **[UPDATED 2026-08-29 — the block below is NO LONGER THE LATEST next-action reading, and is
> annotated rather than rewritten. `origin/main` is **`225b7b0`**, not the `2c95bae` this block
> verified against — `git rev-list --count 2c95bae..225b7b0` is **38**. **Three of its claims are
> spent:** its *"zero open PRs"* — there are now **three**, none a dependency PR; its ledger
> terminus **`2026-09-05T17:59:26Z`**, which #431 **spent** on 2026-08-27 by moving the Vitest
> corpus 231 → 245 and restarting the window, whose new T0 is **conditional and undeclared**; and
> its *"**KI-010** and **KI-011**"* still-open clause — **both shipped**, as `288667d` (#431) and
> `5b35966` (#426). **The obligation to continue the ledger stands**, but it now runs against
> §13.0's conditional T0 rather than that spent mark. **Most of what the block asserts still
> stands** — the A → B → C → F sequence, `js-unit` non-required at **12** required contexts,
> **D4** unsigned, the `scan_export_bounds()` and `rep_range_integrity.py` items open, `needs:`
> and job-level `continue-on-error:` unmeasured, and `push: tags` never fired. **The live
> next-action list is the 2026-08-29 block at the top of this file**; read that one. Nothing below
> is edited except this annotation.]**

**Current (2026-08-23, after #410 and #411) — take no automatic feature action
from this file.** Verified against `origin/main` at **`2c95bae`**, 18/18 green at
job level, **zero open PRs**. Phase 3 step 12's expansion sequence **A → B → C → F**
is complete on `main`; **D is dropped and E is deliberately vacant**.

**The four next actions, each needing its own authorization:**

1. **Q6 is a separate correction packet** — the stale coverage / jsdom prose in
   `STEP12_JS_UNIT_GATE0.md` §1. Deliberately **not** folded into any status
   reconciliation.
2. **Inspect the 2026-08-24 scheduled deep gate after it executes**, at **job**
   level, with `visual-linux` confirmed *executed* rather than skipped — never off
   the overall green. Allow up to an hour of scheduler delay.
3. **Continue the qualification-window ledger until `2026-09-05T17:59:26Z`**, at
   job level, in
   [`testing_phase3/STEP12_JS_UNIT_GATE0.md`](testing_phase3/STEP12_JS_UNIT_GATE0.md)
   §13.0 — extended, never restated from memory, recording any red, missing,
   skipped or cancelled result. A red resets the window to zero.
4. **Q4 and D2 remain unsigned until then**, and D2 needs its own separate owner
   signature even after the window closes.

**Still open and still unauthorized:** **D4**; the `scan_export_bounds()` numeric
`min > max` behavior decision; the `utils/rep_range_integrity.py` docstring
correction; `needs:` and job-level `continue-on-error:` on the deep gate (both
**unmeasured**); **KI-010** and **KI-011**; and the gap that nothing in the app
tells a user a quarantine happened or that snapshots exist.

**Current (2026-08-21, after #403 and the D7 signature) — take no automatic
feature action from this file.** Verified against `origin/main` at **`4d53487`**,
18/18 green.
**[UPDATED 2026-08-23 — superseded by the block above; `origin/main` is now
`2c95bae` (#411). Its D7 statement and its 2026-08-24 deep-gate date are both still
true and are carried forward unchanged.]** Testing Strategy **D7 is signed** (keep the "no in-app restore"
stance; publish the manual recovery procedure) and the reviewed procedure now
lives in `README.md` — ruling and authorized scope in
[`TESTING_STRATEGY_PLANNING.md`](TESTING_STRATEGY_PLANNING.md) §8.1d. The
signature was documentation-only and widened nothing.

**Still open and still unauthorized:** **D4** and the `js-unit` half of **D2**;
the `scan_export_bounds()` numeric `min > max` behavior decision; the
`utils/rep_range_integrity.py` docstring correction; `needs:` and job-level
`continue-on-error:` on the deep gate (both **unmeasured**); Dependabot PRs
**#395–#397**; and the separately-recorded gap that nothing in the app tells a
user a quarantine happened or that snapshots exist. The next scheduled deep-gate
run is **2026-08-24**.

**Current (2026-08-21, after #401/#402) — take no automatic feature action from
this file.** Verified against `origin/main` at `1f9c05a`, 18/18 green. #402 is
tests-only and closed the first of the three preserved packets: the five
`deep-gate.yml` jobs are now barred from any job-level `if:` key, with
`visual-linux` still the pinned conditional exception and `frozen-windows` still
unconditionally protected as before. **Two remain open and unauthorized** — the
`scan_export_bounds()` decision and the `utils/rep_range_integrity.py` docstring.
`needs:` and job-level `continue-on-error:` were named by #402 as possible further
gating shapes; both are **unmeasured** and neither is authorized work. D4 and D7
stay unsigned; the next scheduled deep-gate run is **2026-08-24**.
**[UPDATED 2026-08-21 — superseded by the block above: D7 was signed later the
same day (§8.1d) and the recovery section landed in `README.md`. D4, the two
open packets and the 2026-08-24 run are unchanged.]**

**Current (2026-08-20, after #393/#394/#399/#400) — take no automatic feature
action from this file.** Verified against `origin/main` at `81771d1`, 18/18
green. The four merges are recorded in Current Objective above; the three
packets they deliberately left open (the five unpinned `deep-gate.yml` jobs, the
`scan_export_bounds()` decision, and the `utils/rep_range_integrity.py`
docstring) each need their own authorization. D4 and D7 stay unsigned; the next
scheduled deep-gate run is **2026-08-24**.
**[UPDATED 2026-08-21 — superseded by the block above: the five-job packet
shipped as #402 (`1f9c05a`) and `origin/main` has moved off `81771d1`. The other
two packets, and D4/D7, are unchanged.]**
**[CORRECTED later on 2026-08-21 — D7 was signed that same day (§8.1d) and the
recovery section landed in `README.md`, so this annotation and the sentence above
it are both stale on D7. The two packets and D4 are unchanged.]**

**Current (2026-08-15, after #369/#372/#373/#374/#375) — Testing Strategy Phase 2
is COMPLETE and the release/tag pipeline has SHIPPED. There is still no automatic
feature action dispatched from this file.** Verified against `origin/main` at
`aec309d`:

- **Packet D (axe) shipped as #366 (`f627161`)**, and #372 (`385ce52`) recorded
  the phase closed. No Testing Phase-2 packet remains queued.
- **The release/tag half of Testing Phase 4 shipped** as #374 (`5222db2`), with
  #375 (`d3c3436`) recording the post-merge dry-run and discharging R-3.
- **Testing Strategy D6 closed** as a reserved informational `schema_version`
  label — #373 (`bae49ce`), ADR-008.
- **#369 (`5a48e89`)** pinned the four residual false-green contracts #334 had
  recorded and deliberately left; that residual set is now empty.
- **#370 (`ebe6390`)** re-pinned the fatigue observer guardrail pointer after #359
  shifted the line it named. Docs-only.
- **#376 (`94f0d8c`)** wrote this block; **#377 (`aec309d`)** corrected the two
  claims it left live.
- Unchanged: the first scheduled deep-gate run is inspected at job level; the
  heavy `$orchestrate` design stays unimplemented; do not revive P3 or add
  another readiness marker. **[UPDATED 2026-08-16 — this clause read "only
  after 2026-08-17 03:17 UTC". Post-#388 that run executes R2-b's file and is
  contaminated.] [UPDATED 2026-08-17 — the cron fired that day, 7/7 green, run
  31993105305; the next scheduled run is 2026-08-24.]**

> **Superseded 2026-08-15.** The instruction below said *"Testing Phase-2 Packet D
> (axe) is the only queued packet of that pair … it stays queued … with no open
> PR"*. Packet D shipped as **#366** (`f627161`) and the phase was recorded closed
> by **#372** (`385ce52`), so that boundary statement no longer holds. The rest of
> its guidance — take no automatic feature action, do not revive P3, do not treat
> the heavy orchestration design as shipped — is carried forward above unchanged.

**Current (2026-08-14, after the docs-only tail merged):** take no automatic
feature action from this file. The pack is closed out; what remains keeps its
own authority and none of it is dispatched from here. **Testing Phase-2 Packet D
(axe) is the only queued packet of that pair** — Packet C shipped as #362 — and
it stays queued in `docs/testing_phase2/PLANNING.md` with no open PR; the first
scheduled deep-gate run is inspected only after 2026-08-17 03:17 UTC, at job
level. Do not revive P3, add another readiness marker, or treat the
unimplemented heavy orchestration design as shipped.

> **Superseded 2026-08-14, later the same day.** The instruction below was
> written before the docs-only tail merged. Its *"complete the docs-only
> integration PR"* is discharged, and two of its boundary statements are stale:
> **#351 merged** (`5a03d47`), so it no longer sits with a separate
> visual-baseline owner, and **Packet C shipped** as #362, so only Packet D is
> queued. Retained as the dated record of what the objective was.

**Current (2026-08-14):** complete the docs-only integration PR, then take no
automatic feature action from this file. Existing authorized work keeps its own
boundary: #351 stays with its visual-baseline owner; Testing Phase-2 Packets C/D
remain queued in `docs/testing_phase2/PLANNING.md`; the first scheduled deep-gate
run is inspected only after 2026-08-17 03:17 UTC. Do not revive P3, add another
readiness marker, or treat the unimplemented heavy orchestration design as
shipped.

> **Superseded 2026-08-14.** The instruction below to resume WP4.4-i is retained
> as historical execution evidence; i, j and k have all shipped.

**Resume the existing WP4.4-i worktree from the live execution handoff.** The
fresh N4 decision authorizes sequential i → j → k and pre-answers routine
outcomes. Use one writer and parallel read-only reviewers; serialize DB/server/
browser gates. All ten earlier packets are merged and must not be re-dispatched.

Still forbidden: snapshot rebaseline, visible/behavioral change, layer movement,
protected-contract weakening, unrelated page/template/JS work, and touching the
**235** deferred declarations.

Both N4 pre-change inventories are prepared and merged:
[Inventory A — the complete `:is()` family](CSS_PHASE4_WP4_4_N4_INVENTORY_A_IS_FAMILY.md)
and
[Inventory B — G3 Workout Log regions A–C](CSS_PHASE4_WP4_4_N4_INVENTORY_B_REGIONS_ABC.md).
Inventory B's headline for the approved narrow-or-abandon execution: **29 of the 45 region A/B/C declarations
are currently suppressed, at least in part, by the very `:is()` selector i would
repair, and 16 of those have nothing else above them.** Per N3, if no branch can
be proven safe, **i is abandoned** and WP4.4 ends as audit + deletion — a
pre-authorized outcome, not a failure.

**What `f1` and `f2` established, and what remains protected:**

- The **"three live generations" count is confirmed at exactly three** and is no
  longer an assumption: layered scoped (103 rules), legacy `.navbar` fallback
  (2), unlayered override tail (89), plus 5 `@keyframes` steps.
- **Generation B is NOT dead legacy.** `navbar.css:885` and `:893` claim the
  `.navbar` rule is an overridden fallback that "only applies outside #navbar".
  It is the live winner for `position`: it is unlayered while
  `#navbar { position: sticky }` is inside `@layer navbar`, and for normal
  declarations the unlayered class selector beats the layered ID selector.
  Correcting those comments is an insertion, so `f1` recorded the defect rather
  than fixing it.
- **155 matched-but-never-winning declarations are nominated but UNCERTIFIED**
  and were retained whole. The owner sweep's `!important`/layer arbitration was
  never validated against a known-live *overridden* control, so the set is not
  actionable as it stands. Certifying it requires paying for that control.
- `f2` consolidated only the three exact, owner-proven duplicate structures:
  layered scrollbar declarations, layered dark-toggle defaults, and the
  identical-match-set calm container declarations. It did **not** chase the
  remaining near-duplicate media conditions or any of f1's 155 nominations.

**What `f2` proved, and later packets must not undo:**

- **Freeze layer membership (N2).** `navbar.css` holds the arc's only
  `@layer navbar` block, spanning lines 6-883 at the WP4.4-a baseline —
  **G11: the last `@layer navbar` block may never be deleted.**
- Preserve the contract-pinned `--nav-gap`, `--nav-padding-y` and
  `--nav-padding-x` declarations (pinned in the shared contract file, which
  packets **run but never edit**).
- Treat layered `!important` declarations as **potentially live winners** —
  A6/G10: for `!important`, layer order inverts, so an explicit layer outranks
  the implicit final unlayered layer regardless of specificity.
- The exhaustive matrix exercised collapsed and expanded navigation, dropdowns,
  keyboard navigation, both themes, all required routes, 20 breakpoint-edge
  widths, forced interaction states, reduced motion, contrast and print with
  **486/486** candidate/restore/focus checks green.
- Reconcile the animated-logo result **only** against its established known-red
  band, which is now **875/882 union 1,039/1,046 px** on
  `workout-plan-desktop-dark`. `f2` measured 875/882/875, while `f1` proved the
  low half packet-independent with a same-CSS control. It is a band, not a
  constant.
- M6a and every common packet gate apply.
- **A CSS-only transition suppressor does not satisfy M6a.** `f2` used a
  genuinely transitioned known-live control, observed 7 live
  `CSSTransition` objects, settled them outside the cascade, and proved the
  `--no-settle` red path. The shared suppressor alone remains insufficient.
- **A census verdict needs declaration-owner adjudication.** `d2`'s broad
  census called C50 removable because its synthetic never constructed the
  doubly-matched label. The targeted exact-structure probe found an owner
  transfer in 15/15 light-mode measurements and correctly retained it.

**Method carried from `e` and `d1` — binding:**

- A sentinel sweep and a rest-state differential **cannot falsify an unreachable
  rule**, because deleting one changes nothing on any rendered page. Pair them
  with a runtime **full-selector** census (taken *before* injecting synthetics)
  and a synthetic control that fails the selector by exactly one compound,
  reading properties **derived from the rule's own declarations**.
- **Validate the oracle before trusting it.** Measure a known-live control on
  the same surface first; if the oracle cannot see rules that demonstrably
  render, none of its findings count.
- **State the post-deletion flip by source identity**, never as "the rule went
  blind" — that is indistinguishable from "the oracle stopped working". Where a
  selector name legitimately survives in a retained rule, attribute the residual
  by declaration owner (CDP `CSS.getMatchedStylesForNode`) to that rule's source
  range.
- **Avoid substring assertions where duplicate selector text can mask a
  deletion** — a recurring defect class hit in both `e` and `d1`. Use
  occurrence-count or source-shape assertions.
- **A selector relaxation that is not provably a superset manufactures
  deadness.** `f1`'s first census nominated 39 rules and **38 were artifacts**:
  `>` combinators rewritten, substitution run inside `:not()` producing the
  invalid `:not()`, `@keyframes` steps parsed as style rules, and a CDP
  `styleSheetAdded` listener attached *after* `CSS.enable` (reporting 0 matched
  declarations, which would have made every rule look cascade-dead). Each was
  caught by a control, never by reading the verdicts. Relax only in the
  direction that makes a selector easier to match, and only at paren depth 0.
- **A projected line reduction is not an acceptance criterion.** `f1` shipped −6
  lines against a −150 to −400 projection and is complete.

No further Workout Log packet is authorized, and do not begin fatigue or feature
work or reopen the root-cleanup track. This restriction does not block the
explicitly authorized i → j → k continuation.

> **Superseded 2026-07-31.** The closing sentence previously read *"Do not begin
> `h`, `i`, `j` or `k` while `g` is next."* `g` and `h` have both merged; the
> later N4 continuation authority also supersedes its prohibition on `i`, `j`
> and `k`.
>
> **Superseded 2026-07-29.** This section previously read *"WP4.4-c is merged.
> `b`, `d1`, `e` and `f1` are eligible and unstarted — await owner direction."*
> `b` shipped in PR #192 (`3bec677`) and the owner has since directed the
> sequential order above, so `b` is no longer eligible and `e` no longer waits.
>
> **Superseded 2026-07-28.** This section previously read "Do not begin WP4.4",
> which contradicted merged history from PR #187 and PR #188 as well as the
> Current Objective above. Because this file declares itself the execution
> source of truth, an agent obeying it would have refused to continue work that
> was already built and green.

The sequencing constraint is now **discharged**: a WP4.4 repair of the shared
`:is()` selector would have **resurrected** regions D–G on this page, which is
why the deletion had to precede it. Those rules are gone, so WP4.4 can be
evaluated on its own merits whenever the owner authorizes it. Regions A, B and C
remain page-local and ID-free, so a WP4.4 selector repair would still change what
they own — that is a WP4.4 question, not an open item here.

Still untouched and owner-gated: the remaining Workout Log raw-literal → token
extraction, the ten WP4.3i deferred interaction-state declarations, and the
WP4.3i-c Page Header contract.

---

## Superseded — prior objective (historical)

**2026-07-19 — Phase-4 WP4.3d Volume Splitter dark/token cleanup is integrated
into local `main` as history-preserving merge `40bc09f`.** Exact repeated
status, accent, heading, and dark-surface values now use page-local semantic
tokens. Browser ownership proof removed only dead/redundant dark properties
already won by shared components or later type-specific rules; all live result
and suggestion owners remain. Thirty-seven stable dynamic targets per theme are
identical, with stylesheet order and hooks unchanged. Stylelint is **6,364
warnings** (**-40**: hardcoded **-36**, important **-4**) with duplicate and
specificity counts unchanged. Gates: contracts **16/16**, Flake8 **0**, tsc,
Node **64/64**, Vitest **105/105**, focused Volume Splitter Chromium **27/27**,
required Chromium **407/407**, and pytest **1,737 + the two catalog known-reds**.
All six Windows Volume Splitter variants passed; all twelve route images and all
156 screenshots are byte-identical. Full update-free visuals reproduced only the
exact 1,039- and 6,262-pixel known reds. Generated Bootstrap and both protected
DBs are unchanged. The narrow post-merge git-diff, contract, PostCSS, Flake8,
tsc, Node-syntax, and Vitest gates passed; all protected identities remained
unchanged. Nothing was pushed. Evidence:
`docs/CSS_PHASE4_WP4_3D_EVIDENCE.md`.

### Next Action (as of 2026-07-19 — superseded)

WP4.3d is integrated locally. Leave the branch/worktree intact; do not push or
begin Welcome, another WP4.3 page, or WP4.4 until explicit direction.

---

**2026-06-11 — Issue #8 navbar/dark-mode known-red fix ready.** Fixed the `e2e/nav-dropdown.spec.ts` 1440px dark-mode-toggle actionability red by compacting only the cramped desktop navbar utility chrome (`1360px–1500px`: hide decorative signature/dividers and the scale control, keep muscle + dark toggles reachable) and restoring the spec to a real Playwright `locator.click()`. Promoted `e2e/nav-dropdown.spec.ts` into the required `e2e-functional-shard` spec list without renaming any check context; `program-backup` remains isolated in `e2e-backup`, visual specs remain manual deep gate only. Local verification: `npx playwright test e2e/nav-dropdown.spec.ts --project=chromium --reporter=line` -> **7 passed**. `data/database.db` remains runtime dirt only.

---

**2026-06-11 — A12 pyright Python-version reconcile SHIPPED (PR #76, squash `e2778c0`; CI/config only).** Aligned pyright's analysis target to the CI runtime: `pyrightconfig.json` `pythonVersion` 3.12 → **3.11** (every other CI job — tests/lint/e2e/frontend/security — already runs 3.11, so the type gate had been validating against a Python version the tests never execute on). Also updated the `typecheck` job's `setup-python` 3.12 → 3.11 + the py3.12 notice/summary/comment text, the hardcoded regenerate-note in `scripts/pyright_baseline_diff.py`, and regenerated `docs/ci_cd_phase3/pyright-baseline.json` under 3.11. **The job `name:` was left byte-for-byte unchanged** (`Type Check (tsc blocking + pyright measure-only)`) — required branch-protection context preserved; no branch-protection change. **Measurement (old-vs-new delta = ZERO):** pyright reports **190 diagnostics / 58 distinct keys** under 3.11, identical to 3.12 — symmetric difference 0 (no net-new, no removals, no swaps); `reportMissingImports` = 0 (intrinsic, venv/platform-independent), so the regenerated baseline reproduced on CI's Linux runner (Type Check green, 0 net-new). Only content change to the baseline JSON is the `_meta.note` version string. **Verification:** local baseline gate PASS (0 net-new); `tests/test_pyright_baseline_diff.py` 13 passed; CI all 8 required checks green, `CLEAN`. Local `main` = `origin/main` tip **`e2778c0`** (0 commits ahead). `data/database.db` never staged. **Remaining A12 (optional/deferred, no owner gate forcing them): app-JS `tsc` expansion (`static/js/modules/*`, 29 files / ~14.6k untyped LOC — large), JS unit tests (Vitest/Jest — greenfield, needs owner direction), known-red E2E baseline audit (13+17 reds live only in the manual deep gate, never gate a PR). No CI backlog item is blocking.**

---

**2026-06-11 — A8 F401 flip SHIPPED (PR #74, squash `18de45e`; CI + cleanup) — leftovers A8 fully closed.** Completed the last flake8 measure-only→blocking flip. Drove `flake8 --select=F401` (unused imports) from **56 findings → 0** by removing genuinely-unused imports across ~30 test files plus `app.py`, `routes/body_composition.py`, `routes/user_profile.py`, `utils/fatigue_data.py`, and two `scripts/`; deleted the stray root-level `replace.py` throwaway (one-off template editor, no callers). Then added `F401` to the **blocking** `--select` in `.github/workflows/ci.yml`'s "Lint with flake8" step and removed it from the measure-only diagnostics (only `F841` `except … as e` idiom remains measured, non-flip). The A8 "load-bearing re-exports" caveat proved **moot**: `utils/__init__.py` guards re-exports with `__all__` (zero F401), and `app.py`'s two hits were plain unused `flask` symbols (`render_template`, `url_for`), not side-effect imports. **Verification:** `flake8 --select=F401` = 0; full blocking set `E9,F63,F7,F82,F811,E711,E712,F401` = 0; **pytest 1595 passed**; CI all checks green, `CLEAN`. Shipped as a narrow PR separate from the same-session docs sync (PR #73 `dbedeee`, A11 handover). Local `main` = `origin/main` tip **`18de45e`** (0 commits ahead). `data/database.db` never staged. **Remaining CI backlog: A12 misc (pyright py3.11-vs-3.12 reconcile now DONE — see A12 block above, PR #76 `e2778c0`; remaining optional: expand tsc to app JS, JS unit tests, audit the 13+17 known-red E2E baseline). No measure-only flake8 flip candidates remain.**

---

**2026-06-11 — A11 `e2e-functional` sharding SHIPPED (PR #71, squash `17b9d7f`; CI/docs only) — leftovers A11 closed.** Split the required functional E2E coverage into a 2-way `e2e-functional-shard` matrix plus a fan-in `e2e-functional` gate that keeps the branch-protection context **`E2E Functional (Chromium)`** byte-for-byte. Each shard runs the identical explicit functional spec list from A10 with only `--shard=${{ matrix.shard }}/2` appended, on its own runner/server/freshly-seeded throwaway DB. **No `playwright.config.ts` change** (`fullyParallel: false` stays); **no branch-protection change**; the new `E2E Functional Shard 1/2` / `Shard 2/2` contexts are non-required. Failure artifacts upload per shard as `playwright-functional-shard-<i>-of-2`. **CI proof:** PR #71 green path had Shard 1/2 = 205 passed, Shard 2/2 = 190 passed, fan-in green, `mergeStateStatus: CLEAN`; a throwaway red-path PR #72 broke one shard-1 assertion and proved Shard 2 still ran/passed while the fan-in failed. Realized critical path ≈ **8m28s** vs pre-A11 single job **12m58s** (~35% saved at 2x runner cost). Files already updated by the A11 branch: `.github/workflows/ci.yml`, `e2e/CLAUDE.md`, `docs/ci_cd_phase1/PLANNING.md`, `docs/LEFTOVERS_BY_PRIORITY.md`. Guardrails: no production/pyright/flake8/tsc/schema/API/calc/visual-baseline change; `data/database.db` not staged. Local `main` = `origin/main` tip **`17b9d7f`** (0 commits ahead, after prerequisite PR #70 `cf63ef9`). **Remaining CI backlog after A11: A12 misc; F401 was the last measure-only flip candidate — now flipped to blocking (see A8 block above, PR #74 `18de45e`).**

---

**2026-06-11 — A10 E2E spec promotion SHIPPED (PR #69, squash `45b6bec`; CI/docs only) — leftovers A10 closed.** Promoted `accessibility` + `fatigue-stage4-smokes` + `volume-progress` into the **required** `e2e-functional` Chromium job (added to its spec list in `.github/workflows/ci.yml`). **No job rename / no branch-protection change** — required context `E2E Functional (Chromium)` unchanged, just wider. **CI proof: widened job ran 395 tests, 395 passed (12.2m)** (+45 over prior 350). Promotion evidence: throwaway `--repeat-each=5` ubuntu probe → **225/225 green, zero flakes**, + 2026-06-05 deep-gate full-e2e green + local pass. Coarse-threshold asserts (tap-target ≥32/≥44, viewport ±1px, overflow boolean), not pixel snapshots. Files: `.github/workflows/ci.yml`, `e2e/CLAUDE.md` (CI inclusion contract), `docs/LEFTOVERS_BY_PRIORITY.md` (A10 done). Guardrails at A10 time: `nav-dropdown` + visual specs stayed excluded; issue #8 later fixed and promoted `nav-dropdown` on 2026-06-11, while visual specs stay excluded. No production/pyright-baseline/flake8/tsc/schema/API/calc/visual-baseline change; `data/database.db` not staged. **⚠️ Post-merge watch:** monitor the first ~10 real PR runs of `e2e-functional` for geometry flakes (`volume-progress` ±1px / `fatigue-stage4-smokes` overflow); revert that single spec line if one appears. Local `main` was `origin/main` tip **`45b6bec`** after A10; A11 shipped next (see current block above). **A7–A11 shipped; remaining P2: A12 misc; F401 still measure-only.**

---

**2026-06-10 — pyright baseline-allowlist gate SHIPPED (PR #66, squash `8d110fa`; CI/test/docs only) — leftovers A9 closed.** pyright is now **blocking on net-new errors only** (no existing error fixed). The `typecheck` job keeps its measure-only count + artifact, then runs a blocking baseline-diff. New files: `docs/ci_cd_phase3/pyright-baseline.json` (190 diagnostics / 58 distinct keys, committed `pyrightconfig.json` py3.12+Windows; old ~138 plan figure predates code growth), `scripts/pyright_baseline_diff.py` (repo-relative POSIX path normalization, key = `file+rule+message+severity`, multiset counts, fails only on exceeded counts, `--write-baseline` regenerates, stdlib-only), `tests/test_pyright_baseline_diff.py` (13 cases). Baseline **reproduced exactly on CI Linux** (intrinsic diagnostics, zero `reportMissingImports`). **Gotcha:** the typecheck job `name:` is a branch-protection required-check context — an initial rename orphaned it (green-but-BLOCKED); reverted + pinned with a comment, did not touch protection. Guardrails: no existing pyright error fixed; `pyrightconfig.json`/F401/flake8/tsc/production/schema/API/calc untouched; `data/database.db` not staged. **Verification:** diff unchanged PASS / temp-error FAIL(1); `pytest tests/test_pyright_baseline_diff.py` 13 passed; CI all 8 checks green, `CLEAN`. Local `main` = `origin/main` tip **`8d110fa`** (0 commits ahead). Intervening since `6b6b528`: PR #65 (`e26b895`, A8 handover sync). **A8+A9 done; remaining P2: A10 (promote excluded specs — under investigation), A11 (shard e2e), A12 (misc); F401 still measure-only.**

---

**2026-06-10 — flake8 blocking-rule flip SHIPPED (PR #64, squash `6b6b528`; CI/test/docs only) — leftovers A8 closed.** First rung of the Phase 3 flake8 "path to blocking": `F811,E711,E712` (all already at **0**) added to the blocking `--select=E9,F63,F7,F82` in the `lint` job; that step's `--exclude` aligned with the measure-only `EXCL`. The measure-only diagnostics now track **F401 as the sole remaining flip candidate** (its flip still needs a guardrailed cleanup PR — `utils/__init__.py` re-exports + `app.py` side-effects are load-bearing). One E712 fix: `tests/test_plan_generator.py:594` `== True` → `is True`. Files: `.github/workflows/ci.yml`, `tests/test_plan_generator.py`, `docs/LEFTOVERS_BY_PRIORITY.md` (A8 done), `docs/ci_cd_phase3/PLANNING.md` (follow-up note). No production/calculation/schema/API change; `data/database.db` never staged. **Verification:** `flake8 --select=F811,E711,E712` → **0**; `pytest tests/test_plan_generator.py` → **38 passed**; CI all 8 checks green. Local `main` = `origin/main` tip **`6b6b528`** (0 commits ahead). Intervening since the `284dca4` block below: PR #61 (`6acc537`), PR #62 (`89062d1`), PR #63 (`0d33563`) — docs/test hygiene.

---

**2026-06-10 — Stage 4 observer evidence-pipeline test-hardening SHIPPED (PR #59, squash `672491c`; tests-only, no source behavior change).** Added `tests/test_fatigue_stage4_observer.py` — **26 pytest cases** covering the two scripts that *collect* the Stage 4 calibration evidence gating Learned Calibration **Phase 2D-D** (`scripts/fatigue_stage4_observer.py` + `scripts/fatigue_stage4_status.py`), which previously had **zero** test coverage. Purpose: protect the evidence-collection path so a future 2D-D unblock decision can trust the observer's output. Covers `_direction` band math, `_pending_combos` dedup, `_append_csv` header-once/parent-dir, `analyze`'s **≥2 same-direction = signal / 1 = noise** bar, and the **2D-D gate invariant** — `observe` on an empty `workout_log` returns 0, appends nothing, and writes nothing to the DB; with a seeded log it appends only logged-side unfilled rows and a re-run yields no duplicates; plus `fatigue_stage4_status.main` JSON facts. All DB access via the isolated tmp-path test DB; live `data/database.db` untouched and not staged. **Guardrails:** no `utils/fatigue.py` thresholds/bands/landmarks edit, no estimator-priority/calibration-formula change, no 2D-D implementation (still BLOCKED — see [`docs/user_profile/LEARNED_CALIBRATION_PLAN.md`](user_profile/LEARNED_CALIBRATION_PLAN.md) §"Phase 2D-D Gate Review"). **Verification:** `tests/test_fatigue_stage4_observer.py` → **26 passed**; adjacent fatigue suites + new file → **201 passed**; **full `pytest tests/` → 1582 passed** (1556 documented baseline + 26 new). **Since merged:** PR #60 (`284dca4`, dropped the puppeteer MCP server, kept context7); local `main` = `origin/main` tip `284dca4` (0 commits ahead).

---

**As of 2026-06-10 (latest session): active branch is `main`, in sync with `origin/main` (0 commits ahead), tip `284dca4`.** Since the 2D-C ship, PR #59 (`672491c`, Stage 4 observer evidence-pipeline tests) and PR #60 (`284dca4`, drop-puppeteer-MCP) have merged on top of PR #58 (`5bf4880`). Phase 2D-C (Workout Controls manual fatigue-context nudge controls) **shipped to `origin/main`** via PR #58 (squash `5bf4880`, merged 2026-06-09); feature branch `feat/calibration-phase-2d-c-manual-nudge` merged and deleted. Phase 2D-B shipped via PR #57 (squash `9fb1337`, 2026-06-09); Phase 2D-A via PR #56 (squash `39fdd17`, 2026-06-08). The entire learned-calibration MVP + Phase 2A/2B/2C/2D-A/2D-B/2D-C track is now **shipped to `origin/main`**.

**Phase 2D-C — manual fatigue-context nudge controls (PR #58, squash `5bf4880`, merged 2026-06-09).** A neutral manual-adjustment affordance inside the existing Workout Controls fatigue-context section: ± steppers for **Weight** and **Sets** plus **"Reset to suggestion"**. It is a **neutral manual nudge** (each stepper moves the input by its own native step, clamped to `min`), **not** a fatigue-derived delta (that mapping is gated to 2D-D). **Weight + sets only; reps deferred.** **Client-side only** — sets input values directly (no `input` event → no user-dirty/re-estimate), no API/write path, no persistence to `user_selection`/`workout_log`/`user_profile_lifts`; **Reset restores the estimator suggestion exactly** (`latestTracePayload` weight + sets). **Reuses the shared 2D-A fatigue-context toggle** (no new setting; toggle-off hides it). **No schema/backend behavior change.** Code: `static/js/modules/workout-plan.js`, `static/css/pages-workout-plan.css` (hand-maintained route bundle — no SCSS rebuild), `e2e/fatigue-context.spec.ts` (+1 spec, +1 toggle-off assertion). Guardrails: no estimator suggestion-number change, no estimator-priority change, no fatigue-threshold/landmark/formula change (`utils/fatigue.py` untouched), no plan-row writes, no auto-apply; **2D-D out of scope and gated.** **Verification (2026-06-09):** full `pytest tests/` **1556 passed** (client-side-only — no pytest delta); Chromium E2E `fatigue-context` + `workout-plan` + `learned-calibration` + `progression` + `user-profile` **98 passed**; CI all 8 checks green before merge.

**Phase 2D-B — Progression fatigue context (PR #57, squash `9fb1337`, merged 2026-06-09).** Extends the 2D-A advisory layer to the **Progression page only** (`POST /get_exercise_suggestions`), reusing the 2D-A shared toggle/settings/copy verbatim (one `fatigue_context_settings` row, no per-surface toggle). The suggestions response keeps `data` as the list (contract unchanged) and attaches the same additive `fatigue_context` block as a top-level sibling — present only when the toggle is on and the muscle resolves; omitted otherwise; exception-guarded. New `build_fatigue_context_batch()` performs **one** `build_fatigue_page_context` build per request (no per-exercise scan, no new fatigue math); shared `_neutral_block`/`_block_from_page` keep per-exercise output identical to the single builder. A distinct "Fatigue context" chip + section renders below the suggestion cards. Code: `utils/fatigue_context.py`, `routes/progression_plan.py`, `templates/progression_plan.html`, `static/js/modules/progression-plan.js`, `static/css/pages-progression.css`, `tests/test_fatigue_context.py` (+5), `tests/test_progression_plan_routes.py` (+3), `e2e/progression.spec.ts` (+1, CI-covered). Guardrails: no suggestion-number change, no progression-decision change, no estimator-priority change, no fatigue-threshold/landmark/formula change, no plan-row writes, no auto-apply; `utils/fatigue.py` untouched; 2D-C/2D-D out of scope. **Verification (2026-06-08):** focused pytest **115 passed**; broader affected pytest **217 passed**; full `pytest tests/` **1556 passed**; Chromium E2E `progression.spec.ts` **26 passed**, `fatigue-context.spec.ts` + `user-profile.spec.ts` **29 passed**.

**Phase 2D-A — advisory fatigue context (PR #56, squash `39fdd17`, 2026-06-08).** Additive, post-estimate, default-off advisory layer: a read-only fatigue note for the muscle an exercise trains, rendered inside Workout Controls "show the math" behind an **independent** Profile toggle (separate from Learned Calibration). New `fatigue_context_settings` table; new `GET/POST /api/user_profile/fatigue_context_settings`; the estimate response gains an optional `fatigue_context` block attached **after** `estimate_for_exercise()` returns (omitted when disabled → byte-for-byte unchanged). Reuses the shipped `utils.fatigue_data.build_fatigue_page_context` (no new fatigue math); shows both planned + logged when they disagree; neutral advisory fallback for unranked/unknown/`Unassigned`; every variant says "This does not change your suggestion." Code: `utils/fatigue_context.py` (new), `utils/database.py`, `app.py`, `routes/user_profile.py`, `templates/user_profile.html` + `templates/workout_plan.html`, `static/js/modules/user-profile.js` + `static/js/modules/workout-plan.js`, `static/css/pages-workout-plan.css`, `tests/test_fatigue_context.py` (new), `e2e/fatigue-context.spec.ts` (new), `tests/conftest.py`. **Verification (2026-06-08):** pytest `test_fatigue_context` + `test_user_profile_routes` → 53 passed; `test_database_user_profile` + `test_db_migration` + `test_harness_isolation` + `test_fatigue` + `test_fatigue_routes` → 159 passed; Playwright `fatigue-context` + `learned-calibration` + `user-profile` (Chromium) → 37 passed; **full `pytest tests/` → 1548 passed**. CI: all 8 checks green before merge.

The learned-calibration MVP + Phase 2A/2B/2C track is **shipped to `origin/main`**. Recent learned-calibration history (newest first): `eb4dbf6` (docs handover close-out), `d3cb404` (**PR #55** Phase 2C promote learned rows → Profile references), `bad70c6` (**PR #54** Phase 2B review surface), `0f8b4b7` (**PR #53** Phase 2A related-exercise transfer plumbing).

The prior 2026-06-04 `feat/learned-calibration-backend` branch (commits `8a6d39a` / `76d7490` / `5587784`) and its UI/UX follow-up work landed on `main` and the branch is gone — that handoff is **superseded** by the merged Phase 2C state below.

**Learned-calibration state (all on `main`):**

- **MVP** (PR #37 `fd2e2f5`) — exact-exercise learned calibration backend, settings, estimator integration, Profile controls, Workout Controls source UI/actions, workout-log notifications. Estimator priority: `exact learned → exact log → related learned → Profile → cold-start → default`.
- **Phase 2A** (PR #53 `0f8b4b7`) — read-only, ratio-gated related-exercise transfer; ships with zero seeded ratios so no behavior change until learned + related modes + a ratio row all exist.
- **Phase 2B** (PR #54 `bad70c6`) — read/control review surface on `/user_profile` (learned-calibration list, ignored-transfer controls, bulk reset). No estimator math change.
- **Phase 2C** (PR #55 `d3cb404`) — per-row "Promote to reference lift" graduates an exact learned row into `user_profile_lifts` (measured top set, basis-converted). No schema change, no estimator-priority change, no silent overwrite (`REFERENCE_LIFT_EXISTS` guard + UI confirm). Full pytest **1524 passed**; CI all 8 checks green.

**Remaining learned-calibration work:** Phase 2D design review is complete (owner answers locked, `38d3b1c`); **Phase 2D-A shipped** (PR #56, squash `39fdd17`), **Phase 2D-B shipped** (PR #57, squash `9fb1337`), and **Phase 2D-C shipped** (PR #58, squash `5bf4880` — see the top block). **2D-D** (actual suggestion modification) was **gate-reviewed 2026-06-09 and is BLOCKED on insufficient Stage 4 real-use evidence — do not start.** It is the first advisory→prescriptive step, so it needs explicit owner approval **and** evidence. Evidence today (insufficient): `workout_log` **0 rows**; no `stage4_calibration_log.csv` observer output; **0 of ≥2** same-direction real-use disagreements; the one historical real anchor agreed with the engine and the synthetic mismatch does not count. Unblock: non-empty representative multi-week `workout_log` + ≥2 same-direction real-use disagreements + owner approval to cross advisory→prescriptive + decisions on touched output(s)/magnitude/double-counting (G4). Conditional narrowest future sketch (NOT actionable): sets-only, user-accepted, client-side, no auto-apply, no persistence. Split + gate detail: [`docs/user_profile/LEARNED_CALIBRATION_PLAN.md`](user_profile/LEARNED_CALIBRATION_PLAN.md) §"Phase 2D-D Gate Review — BLOCKED (2026-06-09)".

**Guardrails honored across the track:** no auto-apply, Profile reference lifts written only via the explicit 2C promote action, planned `user_selection` rows untouched, historical `workout_log` untouched, `utils/fatigue.py` untouched. Phase 2D-A adds advisory context only — no suggestion-number change, no estimator-priority change, no fatigue-threshold/landmark/formula changes. `data/database.db` is runtime-only and **must not be committed** (owner policy).

---

**Prior (2026-05-29) — `main` state: local `main` is in sync with `origin/main` (0 commits ahead) after pushing `df9b6f9` (movement_pattern cleanup, 2026-05-25), `f2cdc23` (Stage 4 calibration observer tooling, 2026-05-29), and this handover sync on top of the prior `origin/main` tip `39193f6`. Fatigue Meter Phase 2 Path 1 shipped 2026-05-23 via PR #35 (`d5b80bf`); Stage 3 verify-suite gate closed 2026-05-24 (`1a93f66`); Stage 4 calibration window OPEN 2026-05-24, earliest close 2026-06-07 — the observer is ready and read-only but stays blocked until real `workout_log` data exists (empty as of 2026-05-29).** Phase 2 Stage 0 lock landed via PR #33 (`24c6f46`) and Stage 1 close via PR #34 (`be22286`); planning extracted earlier in `f01ccb9`. The 2026-05-23 hygiene session, the six in-flight scope commits, the KI-001 / KI-009 / §4.6 baseline / §5 expansion follow-ups, and the YouTube curation closure all landed before Phase 2 work began. The lead-up: Body Composition Issue #21 fully shipped via PR #31 (squash `20b4b24`, 2026-05-20) and hardened in PR #32 (`94482d7`, 2026-05-21, `captured_at` ISO validation + JS↔Python parity test); response-contract exceptions migrated 2026-05-21 (`cbf745a`); §5 YouTube curation landed in two passes — `cf21191` (2026-05-22, 36 rows) + `ff244aa` (2026-05-23, +20 rows → **56 cumulative**, curation closed by diminishing returns). 2026-05-23 also landed the six in-flight scopes as separate commits (Profile #17/#18 hooks `de3e4d0`; workout-cool §3.6 Profile bodymap `18ad223`; navbar hover dropdowns `ef475cc`; navbar icon accents + motion `89561df`; Body Composition visual baselines `40d7dd2`; ui-hardening spec + Known Issues table `0ae5b39`), the docs-only hygiene commit, the KI-001 filter-cache deletion (`6d87284`), the KI-009 xlsxwriter exporter (`4bbe06b`) + docs (`f944366`), and the §4.6 visual-baseline `toHaveScreenshot()` lock-in (`b5b8c7a`). No active workstream remains in-flight.

workout.cool §4 (free-exercise-db thumbnails) is **fully shipped on `origin/main`**. PR #20 (squash `8b348a5`) landed the feature; PR #23 (`bfd9087`) landed the post-merge handoff refresh + nav-dropdown e2e stabilization + dependency pin bumps; PR #22 (`631b5f8`) landed the §4.6 visual-baseline spec + seed. workout.cool §5 reference-video infrastructure shipped 2026-05-11; the curated content shipped in two passes — `cf21191` (2026-05-22, 36 rows) + `ff244aa` (2026-05-23, +20 rows → **56 cumulative**). Curation is **closed by diminishing returns** (only 1 of the remaining ~1,841 uncurated rows has >1 actual uses; long-tail uses the search fallback by design). workout.cool §3.6 Profile coverage bodymap was previously "deferred indefinitely"; it shipped locally on 2026-05-23 (`18ad223`).

- **Redesign post-P8 triage** — closed (10 of 11 shipped, #1 deferred by owner choice; verified 2026-05-19, PR #25).
- **phase5_3i_plan** — closed (accepted-as-shipped 2026-05-19; planning doc shipped `c0da18e` and deleted `635fa3e`, 5A–5H validation never ran but `12c90ac` refactors have held 5+ weeks under the 1160-test baseline; PR #25).
- **Fatigue meter** — Phase 1 shipped; Phase 1 Stage 4 closed 2026-05-20 (owner-approved felt-label review, no threshold changes — `calibration-notes.md` authoritative). **Phase 2 Path 1 shipped 2026-05-23 via PR #35 (`d5b80bf`)** (per-muscle accumulator, period selector, dedicated `/fatigue` route, dual planned + logged bars, two SFR cards, nav link, badge → page link; 91 new pytest cases for total 1442; 8/8 `e2e/fatigue.spec.ts` green). Stage 0 lock PR #33 (`24c6f46`), Stage 1 close PR #34 (`be22286`). **Phase 2 Stage 3 verify-suite gate closed 2026-05-24 (`1a93f66`)** — 13 + 17 reds on full Chromium match the pre-existing baseline exactly with zero new Stage-2 reds. **Phase 2 Stage 4 calibration window opened 2026-05-24 and CLOSED 2026-08-13** — owner decision, no real-use evidence, no threshold change. Source of truth: [`docs/fatigue_meter/PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md).
  - 2026-05-20 history preserved: PR #26 (`2b34b50`) docs-only synthetic-override / coherence pass; PR #28 (`63c745d`) presentation-only badge restyle.

Pick a new workstream from owner direction.

## Owner-Approved Next Workstream Queue

Recorded 2026-05-20 so future agents do not need to re-evaluate the full docs
state before choosing what to do next.

1. **Body Composition (Issue #21) — DONE.** Shipped via PR #31 (`20b4b24`) +
   PR #32 (`94482d7`). Source of truth:
   [`docs/archive/body_composition/development_issues.md`](archive/body_composition/development_issues.md).
2. **Profile-page body-composition hooks (Issues #17/#18) — DONE.** Shipped
   2026-05-23 via local commit `de3e4d0`. Display-only BFP/ACE line + Lean
   Mass sub-line on the Profile insights card, read from the latest
   `body_composition_snapshots` row.
3. **workout.cool §5 YouTube curation — DONE (closed by diminishing returns
   2026-05-23).** `cf21191` (2026-05-22) populated 36 curated rows; `ff244aa`
   (2026-05-23) added 20 more for **56 cumulative**. Usage triage showed all
   remaining ~1,841 uncurated rows sit at 0–1 actual uses except one edge
   case, so the search fallback handles the long tail by design. Do not
   expand further without owner-vetted IDs. See
   [`docs/workout_cool_integration/YOUTUBE_REFERENCE_VIDEOS.md`](workout_cool_integration/YOUTUBE_REFERENCE_VIDEOS.md)
   "Curation Closed".
4. **Fatigue Meter Phase 2 Stage 4 — CLOSED 2026-08-13 (no evidence / no change).**
   Phase 2 Path 1 shipped 2026-05-23 (PR #35 `d5b80bf`); Stage 3 verify-suite gate
   closed 2026-05-24 (`1a93f66`); Stage 4 calibration window opened 2026-05-24 and
   **closed 2026-08-13** by owner decision. Nothing to track here any more — but
   **the guardrails survive the close**: see the "Live calibration guardrails"
   block below, which binds any future tuning. Source of truth:
   [`docs/fatigue_meter/PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md)
   Stage 4 + §10.
5. **Worktree disposition — DONE.** Closed 2026-05-23 via `21859a1`. Both old
   worktree paths (`Hypertrophy-Toolbox-v3-visual-baseline-s4`,
   `Hypertrophy-Toolbox-v3-redesign-calm-glass`) were already absent from
   `D:/development/` and neither was registered in `git worktree list`. Stale
   branch refs (`test/visual-baseline-thumbnails` local + remote;
   `origin/redesign/calm-glass-2026`) deleted with owner approval. Source of
   truth: [`docs/LEFTOVERS_BY_PRIORITY.md §6`](LEFTOVERS_BY_PRIORITY.md).

## Current Branch

`main`, **in sync with `origin/main` (0 commits ahead)**, tip `284dca4` (PR #60 `chore(mcp): drop puppeteer server, keep context7`, on top of `672491c` PR #59 Stage 4 observer evidence-pipeline tests, `8cb4c55` 2D-D gate-review-BLOCKED docs, `f442632` post-2D-C docs refresh, and `5bf4880` PR #58 Phase 2D-C manual fatigue-context nudge controls, squash merged 2026-06-09). The learned-calibration track merged on top of the prior 2026-05-29 handover-sync state: `0f8b4b7` (PR #53 Phase 2A), `bad70c6` (PR #54 Phase 2B), `d3cb404` (PR #55 Phase 2C), `eb4dbf6` (docs close-out), `39fdd17` (PR #56 Phase 2D-A), `acb67b0` (2D-A docs refresh), `9fb1337` (PR #57 Phase 2D-B), `f694333` (2D-B docs refresh), `5bf4880` (PR #58 Phase 2D-C). Feature branches `feat/calibration-phase-2d-c-manual-nudge` (PR #58) and `feat/calibration-phase-2d-b-progression-context` (PR #57) merged and deleted (local + remote). `data/database.db` runtime dirt is owner-approved and **never committed** (per `CLAUDE.md` agents-must-not list — it was never staged). Feature branches `feat/calibration-phase-2d-fatigue-context` (PR #56), `feat/calibration-phase-2c-promote-profile` (PR #55), `feat/calibration-phase-2b` (PR #54), and the Phase 2A branch were merged and deleted; earlier `feat/body-composition-issue-21` (PR #31), `feat/fatigue-meter-phase-2` (PR #34), and `feat/fatigue-meter-phase-2-stage-2` (PR #35) likewise merged and deleted.

Recent local / `main` history (newest first):

- 2026-05-30 — **chore(fatigue): add stage 4 automation health-check + install/repair tooling**. Adds `scripts/check_fatigue_stage4_automation.ps1` (read-only health check that classifies the observer automation as [BROKEN] / [SKIPPED] / [IDLE] / [READY], explains task result codes incl. `0` and `0x800710E0`, and reports the live `workout_log` count), `scripts/install_fatigue_stage4_observer_task.ps1` (idempotent `schtasks /Create ... /F` installer, default daily 20:00), and `scripts/fatigue_stage4_status.py` (read-only `COUNT(*)` DB helper via `DatabaseHandler`). Closes the automation-observability gap (the owner can now tell at a glance whether the task is installed, last ran clean, was skipped by Windows, or is just idle on empty `workout_log`). Verified 2026-05-30: check -> **[IDLE]** (last result `0`, `workout_log` empty), installer re-registered the task idempotently, `schtasks /Run` succeeded (last code `0`, latest log refreshed). No fatigue thresholds / scenarios / boundary tests touched; no DB write. See [`PHASE2_PLANNING.md §10`](fatigue_meter/PHASE2_PLANNING.md).
- 2026-05-29 handover sync — **docs(fatigue): sync handover after Stage 4 observer tooling**. Refreshes the branch-position lines in [`docs/MASTER_HANDOVER.md`](MASTER_HANDOVER.md) + this file to reflect `df9b6f9` / `f2cdc23` pushed and `origin/main` advanced from `39193f6`; records the Stage 4 observer as ready + still blocked on empty `workout_log`.
- `f2cdc23` (2026-05-29) — **chore(fatigue): add stage 4 observer tooling**. Adds `scripts/fatigue_stage4_observer.py` (read-only; reuses `utils.fatigue_data.build_fatigue_page_context` so numbers match `GET /fatigue`; never edits thresholds / scenarios / boundary tests), `scripts/run_fatigue_stage4_observer.bat`, `.gitignore` entries, +1 line in [`PHASE2_PLANNING.md §10`](fatigue_meter/PHASE2_PLANNING.md). Ran once 2026-05-29: `workout_log` empty → nothing appended → Stage 4 stays blocked on real logged workouts.
- `df9b6f9` (2026-05-25) — **chore(fatigue): close Phase 2 §10 #5 movement_pattern cleanup**. 454 NULL/blank `movement_pattern` rows → 0 (76 inferred via `utils.movement_patterns.classify_exercise()`, 378 `"unassigned"` sentinel); new invariant `tests/test_catalog_invariants.py::test_catalog_movement_pattern_has_no_nulls`; pytest 1442 → 1443. Pre-flight backup local id 5, label `pre-movement-pattern-cleanup-2026-05-25`.
- `39193f6` (2026-05-24) — **docs(fatigue): refresh phase 2 stage 4 handoff**.
- `1a93f66` (2026-05-24) — **docs(fatigue): close phase 2 stage 3 gate**. Flips [`docs/fatigue_meter/PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md) status banner to Stage 3 CLOSED + Stage 4 OPEN; verify-suite gate on `main` @ `d5b80bf` recorded (pytest 1442 passed; Playwright Chromium full 449 passed / 13 failed / 17 did-not-run — reds match pre-existing baseline exactly, zero new Stage-2 reds).

Recently landed on `origin/main` (newest first):

- `d5b80bf` (2026-05-23) — **PR #35** `feat(fatigue): add stage 2 fatigue breakdown surface`. Phase 2 Path 1 squash: per-muscle accumulator (`utils/fatigue.py` planned + logged + 4-week window), `routes/fatigue.py` blueprint, `templates/fatigue.html` + `_fatigue_muscle_bar.html`, period selector, two SFR cards, nav link, badge → page link, SCSS, 91 new pytest cases (1351 → 1442), `e2e/fatigue.spec.ts` 8 passed. Pre-merge restore point: backup id 5, label `pre-fatigue-meter-phase-2-stage-2-merge-2026-05-23`.
- `be22286` (2026-05-23) — **PR #34** `chore(fatigue): close Phase 2 Stage 1 prerequisites`. Catalog cleanup pass — 633 `primary_muscle_group` NULLs eliminated (132 inferred from `exercise_name` via `utils.constants.MUSCLE_ALIAS ∪ MUSCLE_GROUPS`, 501 dormant rows assigned `"Unassigned"` sentinel); `tests/test_catalog_invariants.py::test_catalog_primary_muscle_group_has_no_nulls` added; pre-flight backup id 5 captured (label `pre-fatigue-meter-phase-2-2026-05-23`); pytest 1350 → 1351.
- `24c6f46` (2026-05-23) — **PR #33** `docs(fatigue): lock Phase 2 Path 1 scope via Stage 0 walk`. Stage 0 decisions D2.1–D2.10 + stretch decisions + catalog re-scope synced into [`docs/fatigue_meter/BRAINSTORM.md §13.1 Phase 2 Decision Log`](fatigue_meter/BRAINSTORM.md); [`docs/fatigue_meter/PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md) authored as canonical Phase 2 source.
- `f01ccb9` (2026-05-23) — **docs(fatigue): extract Phase 2 planning**. Splits Phase 2 planning out of `docs/fatigue_meter/PLANNING.md` Stage 5/6 + `docs/fatigue_meter/BRAINSTORM.md` Phase 2 matrix.
- `15ea316` (2026-05-23) — **docs: sync handoff after worktree cleanup** (LEFTOVERS row #14 follow-up).
- `21859a1` (2026-05-23) — **docs: close stale worktree disposition backlog** (LEFTOVERS row #14 closed; old worktree paths already absent from disk; stale branch refs `test/visual-baseline-thumbnails` local + remote and `origin/redesign/calm-glass-2026` deleted with owner approval).
- `1956089` (2026-05-23) — **docs(workout-cool): close YouTube curation backlog** (LEFTOVERS row #12 closed by diminishing returns at 56 rows; ahead-of-origin status text refreshed).
- `ff244aa` (2026-05-23) — **content(workout-cool): expand curated YouTube references** (+20 owner-vetted rows on top of `cf21191`; `data/youtube_curated_top_n.csv` now 56 rows + header; curation closed by diminishing returns — see [`docs/workout_cool_integration/YOUTUBE_REFERENCE_VIDEOS.md`](workout_cool_integration/YOUTUBE_REFERENCE_VIDEOS.md) "Curation Closed").
- `b5b8c7a` (2026-05-23) — **test(workout-cool §4.6): lock visual-baseline thumbnails via `toHaveScreenshot()`** (18 committed PNG baselines at `maxDiffPixelRatio: 0.01`; closes LEFTOVERS row #13).
- `f944366` (2026-05-23) — **docs: record KI-009 resolution**.
- `4bbe06b` (2026-05-23) — **fix(workout-log): replace pandas with xlsxwriter direct writer** (KI-009 fix; drops pandas/numpy/python-dateutil from `requirements.txt`).
- `6d87284` (2026-05-23) — **chore: remove dormant filter cache (KI-001 resolved by deletion)**.
- 2026-05-23 docs hygiene commit — refresh after the six-scope landing.
- `0ae5b39` (2026-05-23) — **test+docs: lock down toast/form/modal contracts and add Known Issues table**. New `e2e/ui-hardening.spec.ts` (12 tests) + new `docs/UI_SCENARIOS_GAP_ANALYSIS.md §0` (KI-001..KI-008).
- `40d7dd2` (2026-05-23) — **test(visual): add Body Composition snapshot baselines**. Adds `/body_composition` to the visual.spec.ts sweep + 6 PNG baselines (desktop/tablet/mobile × light/dark); migration script applies `add_body_composition_snapshots_table()` so the page renders under the visual harness.
- `89561df` (2026-05-23) — **feat(navbar): accent colors + hover motion on Profile, Body Composition, and Backup icons**. CSS-only color accents + hover/focus motion + reduced-motion opt-out; swaps Profile icon to `fa-user-alt`.
- `ef475cc` (2026-05-23) — **feat(navbar): hover-to-open desktop dropdowns**. Gates on `(hover: hover) and (pointer: fine) and (min-width: 992px)`; touch + mobile remain click-to-open.
- `18ad223` (2026-05-23) — **feat(profile): mount workout-cool bodymap with worst-state aggregation (§3.6)**. Lifts the previously deferred §3.6 scope; multi-muscle BACK regions reflect the worst coverage state across the set.
- `de3e4d0` (2026-05-23) — **feat(profile): surface latest body composition snapshot (#17 + #18)**. Display-only BFP/ACE line + Lean Mass sub-line on the Profile insights card; reads latest snapshot, Navy-over-BMI fallback.
- `cf21191` (2026-05-22) — **Add curated YouTube references for core exercises** (36 rows; `data/youtube_curated_top_n.csv` populated and `scripts/apply_youtube_curated.py` applied).
- `cbf745a` (2026-05-21) — **fix(api): migrate remaining response-contract exceptions**. `/api/pattern_coverage` and the replace-exercise fallback branches now use `success_response()` / `error_response()`; "no result" cases pass `status_code=200` to keep the existing UI contract.
- `94482d7` (2026-05-21) — **chore(body-composition): validate captured_at, add JS↔Python parity test (#32)**. Tightens the snapshot create endpoint's ISO format validation and adds the Playwright JS↔Python numeric parity case.

Recent history on `origin/main` (newest first):

- `20b4b24` (2026-05-20) — **PR #31** `feat(body-composition): add page, API, and nav slot`. Squash bundles the two pre-squash Body Composition Issue #21 commits (backend formula + migration + tests; page + API + UI + Playwright). CI 6/6 green. Opus review verdict: ready to merge. Non-blocking follow-ups recorded for later: (1) add `captured_at` ISO format validation, (2) add JS↔Python numeric parity Playwright assertion, (3) minor docs test-count drift refresh.
- `63c745d` (2026-05-20) — **PR #28** `fix(fatigue-badge): compact, intentional widget on summary pages`. Presentation-only — 16 files changed, 184 insertions(+), 88 deletions(-). Restructures `templates/_fatigue_badge.html` (drops the `.card`/`.card-body` scaffold, switches to a `<section>` grid; promotes score + band to a readout row with eyebrow + info icon above; period label moves to the right column on desktop and stacks below on mobile). Rewrites `scss/_fatigue.scss` for a translucent surface harmonized with `.summary-frame` glass styling (score 2.1rem/700 tabular-nums; band rendered as a pill chip; empty-state pill is dashed-outline; tighter padding drops desktop badge height ~162px → ~86px). Rebuilds `static/css/bootstrap.custom.min.css` + source map. Refreshes 12 visual snapshots for weekly/session × {desktop,tablet,mobile} × {light,dark}. **No `utils/fatigue.py`, no thresholds, no APIs, no calibration, no scenario-script changes.** Existing Playwright selectors (`.fatigue-badge`, `.fatigue-badge__info-btn`, `.fatigue-badge__band`) preserved. Verification recorded in PR: pytest fatigue+summary 150 passed; `e2e/fatigue-stage4-smokes.spec.ts` 5 passed; `e2e/summary-pages.spec.ts` 20 passed; `e2e/visual.spec.ts` 42 passed (after intentional re-baseline).
- `330b2a9` (2026-05-20) — **PR #27** `docs: refresh handoff after fatigue synthetic override`. Docs-only — refreshed `ACTIVE_DEVELOPMENT.md` + `MASTER_HANDOVER.md` to reflect PR #25 + PR #26 on `origin/main` (current-SHA bump, recent-merges list, CI rows, fatigue-meter workstream-row update, 2026-05-20 override note in the "DO NOT REOPEN" block). No code, script, test, template, route, or runtime files touched.
- `2b34b50` (2026-05-20) — **PR #26** `docs(fatigue): record synthetic calibration override`. Docs-only — 1 file changed, 101 insertions(+), 0 deletions(-) in `docs/fatigue_meter/calibration-notes.md`. Reframes the existing 2026-05-11 generated calibration report as an owner-approved synthetic-override / coherence pass; flags `hard_4d` mismatch (intended `heavy`, computed `moderate` at 161.9 weekly); records hypothesis A (threshold drift) and B (scenario miscal, preferred) as proposals only. No `utils/fatigue.py`, no scenario script, no DB writes. CI 6/6 green.
- `1eebe54` (2026-05-19) — **PR #25** `docs: close stale handoff workstreams`. Docs-only — closes the redesign post-P8 triage and phase5_3i_plan rows after verifying both were already complete on `origin/main`. CI 6/6 green.
- `631b5f8` (2026-05-18) — **PR #22** `test(workout-cool §4.6): add visual-baseline thumbnail spec + seed`. Adds `e2e/visual-baseline-thumbnails.spec.ts` (18 tests) and `scripts/seed_visual_baseline.py`. `.gitignore` now ignores `e2e/artifacts/`. Screenshots are inspection artifacts only — no `toHaveScreenshot()` pixel baselines committed.
- `bfd9087` (2026-05-18) — **PR #23** `chore: post-section-4 handoff refresh + nav e2e + dependency pins`. Replaces closed PR #21. Rebased onto `origin/main` to drop the seven pre-squash §4 commits that had made the original branch `CONFLICTING`. Carries the nav-dropdown off-viewport fix and the Playwright/sass/TS/Node/Flask/pandas/click bumps.
- `8b348a5` (2026-05-15) — **PR #20** `feat(workout-cool §4): free-exercise-db exercise thumbnails`. Squash bundles checkpoints 3–6.
- `7a77315` (2026-05-14) — **PR #19** `feat(workout-cool §4): vendor free-exercise-db assets (checkpoint 2)`.

## Already Done

- §4 checkpoint 1: `media_path` schema, path validator, and `scripts/apply_free_exercise_db_mapping.py`.
- §4 checkpoint 2: `static/vendor/free-exercise-db/` assets, `LICENSE`, `NOTICE.md`, `VERSION`, `exercises.json`, 873 `0.jpg` images.
- §4 checkpoint 3: `scripts/map_free_exercise_db.py`, `data/free_exercise_db_mapping.csv` (raw 1,897 rows), `docs/workout_cool_integration/checkpoint3_coverage.md`.
- §4 checkpoint 4: `scripts/curate_free_exercise_db_mapping.py` (structural-equivalence rule) + curated `data/free_exercise_db_mapping.csv` (1784 auto / 98 confirmed / 10 manual / 5 rejected = 113 reviewed).
- §4 checkpoint 5: `_trim_exercise_name_whitespace` repair pass in `utils/db_initializer.py`; `media_path` surfaced in `/get_workout_plan` + `/get_workout_logs` JSON and in `utils/workout_log.py::get_workout_logs`; +4 trim tests + +4 route-contract tests.
- §4 checkpoint 6: `static/js/modules/exercise-helpers.js` with `escapeHtml()` + `resolveExerciseMediaSrc()`; workout-plan row renderer thumbnails; workout-log template `safe_media_path` Jinja filter; thumbnail CSS; +4 self-contained Playwright tests + +2 filter unit tests.
- §4 squash-merge (`8b348a5`) on 2026-05-15.
- Post-§4 follow-up (`bfd9087`) on 2026-05-18: nav e2e off-viewport fix + dependency pin refresh.
- §4.6 visual-baseline (`631b5f8`) on 2026-05-18: 18-test spec + seed.
- Apply-mapping: `exercises.media_path` populated for 108 rows (98 confirmed + 10 manual) in the main-checkout DB and the visual-baseline worktree DB.
- Fatigue meter Phase 1 / Stage 4 entry parked by owner choice (Option 1 confirmed 2026-05-13).
- Fatigue meter bounded synthetic-override / coherence pass (2026-05-20) — docs-only via PR #26 (`2b34b50`). Reuses 2026-05-11 generated report; `hard_4d` mismatch flagged; two hypotheses recorded as proposals only; no thresholds or scripts touched; Stage 4 still parked.
- Fatigue badge presentation polish (2026-05-20) — PR #28 (`63c745d`). Template + SCSS + built CSS + 12 refreshed visual snapshots. No `utils/fatigue.py`, no thresholds, no APIs, no calibration, no scenario-script changes; Stage 4 still parked.
- Body Composition Issue #21 (2026-05-20) — PR #31 (`20b4b24`). Both slices shipped as one squash commit: `utils/body_fat.py` (4 pure formulas with "MUST MATCH JS MIRROR" comment), `add_body_composition_snapshots_table()` migration in `utils/database.py`, `routes/body_composition.py` blueprint (4 endpoints), `templates/body_composition.html` page (calculator + ACE band + Jackson & Pollock + trend SVG + history), `static/js/modules/body-composition.js` (formula mirror + page wiring), `static/css/pages-body-composition.css` route bundle, navbar slot, `app.py` + `tests/conftest.py` blueprint registration, 67 route + formula + migration tests, 4 Playwright specs, smoke/nav-dropdown updates.

## Next Task

### Shipped 2026-05-20 via PR #31 — Body Composition Issue #21

Both slices landed as squash commit `20b4b24` on `origin/main`. Files included:

- **New** `routes/body_composition.py` — `body_composition_bp` blueprint with `GET /body_composition`, `POST /api/body_composition/snapshot`, `GET /api/body_composition/snapshots`, `DELETE /api/body_composition/snapshots/<id>`. All four routes use `success_response()` / `error_response()`, `DatabaseHandler`, and the shared logger pattern. Snapshot creation reads gender / age / height / bodyweight from the server-side `user_profile` row (the browser posts tape + notes only), then validates profile demographics and circumferences via the range constants exported from `utils.body_fat`. Tape data is all-or-nothing: provide all required tape values for the Navy method or leave blank to fall through to the BMI fallback.
- **New** `templates/body_composition.html` — `body-composition.html` page. Reads gender / age / height / bodyweight from the existing `user_profile` row (shown via `data-profile-*` attributes on the page wrapper), renders an "Profile incomplete" warning when demographics are missing, hosts the calculator form (tape inputs + collapsible "How to measure" guide), the live results panel (BFP / fat mass / lean mass / BMI / ACE segmented band with tick / Jackson & Pollock comparison line / citations footer), the trend SVG, and the snapshot history table with per-row delete.
- **New** `static/js/modules/body-composition.js` — pure-function mirror of the four Python formulas (`computeNavy`, `computeBmi`, `aceCategory`, `jacksonPollockIdeal`) with module-level "MUST MATCH PYTHON" comment, plus the page wiring: live results on every input event, ACE band tick positioning, trend polyline computation, snapshot save / delete via the `api` wrapper, toast notifications.
- **New** `static/css/pages-body-composition.css` — page bundle (calculator panel + results + ACE segmented band + trend SVG + history table; dark-theme overrides).
- **Edit** `templates/base.html` + `static/css/navbar.css` — moves `Profile` into the main left flow and adds the full-label `Body Composition` link between `Profile` and `Distribute` (`nav-volume-splitter`), with a ruler icon. `navbar.css` gives the longer label a wider fixed pill at desktop sizes so the text does not clip while the dark-mode toggle remains visible.
- **Edit** `static/js/modules/navbar.js` — adds `'/body_composition': 'nav-body-composition'` to the pathMap so the active-state highlight from Issue #12 fires.
- **Edit** `.claude/rules/frontend.md` — updates the route-bundle cap/list to include `pages-body-composition.css` and records the new nav flow with Profile + Body Composition before Distribute.
- **Edit** `app.py` + `tests/conftest.py` — register `body_composition_bp` (between `user_profile_bp` and `volume_splitter_bp` in both files).
- **New** `tests/test_body_composition_routes.py` — 18 route tests: page renders with + without profile, page lists existing snapshots, POST Navy male / female / male-rejects-hip / female-requires-hip / BMI-only / profile-demographics-source / missing-profile / out-of-range-height / partial-tape / log-domain-violation / captured-at passthrough, GET descending / empty, DELETE success / not-found.
- **New** `e2e/body-composition.spec.ts` — 4 Chromium specs: navbar routes to page, empty-state render, save-then-delete flow with live results assertion and trend update, BMI-fallback when tape blank.
- **Edit** `e2e/fixtures.ts`, `e2e/smoke-navigation.spec.ts`, `e2e/nav-dropdown.spec.ts` — adds body-composition route/selectors, smoke-cycles `/body_composition`, and asserts the top-level nav order `['Plan', 'Log', 'Analyze', 'Progress', 'Profile', 'Body Composition', 'Distribute', 'Backup']` plus a no-clipped-label check.
- **Edit** `docs/ACTIVE_DEVELOPMENT.md` + `docs/MASTER_HANDOVER.md` — this update.

First-slice files (now part of PR #31 squash, originally landed on the branch as `f4496f7`):

- **New** `utils/body_fat.py` — pure-function module with `compute_navy(...)`, `compute_bmi(...)`, `ace_category(bfp, gender)`, `jackson_pollock_ideal(age, gender)`. Carries the **"must match JS mirror"** module-level comment from the Issue #17 contract. Server-side validation (range checks + log-domain rejection) raises `ValueError`; route layer (not built here) will translate into structured 4xx responses.
- **New** `tests/test_body_fat.py` — 42 cases. Coverage: Navy male + female typical lifters, Navy log-domain rejection (both sexes), male-rejects-hip, female-requires-hip, out-of-range height, invalid gender; BMI adult male / adult female / boy <18 / girl <18 + age-18 boundary; ACE male + female boundary rows (parametrized 20 rows) + low-value clamp; Jackson & Pollock anchor rows + interpolation male/female + age clamp below 20 / above 55 + invalid gender.
- **Edit** `utils/database.py` — added `add_body_composition_snapshots_table()` migration. Creates the `body_composition_snapshots` table exactly per [`docs/archive/body_composition/development_issues.md`](archive/body_composition/development_issues.md) (14 columns; 6 NOT NULL: `captured_at`, `bodyweight_kg`, `height_cm`, `age_years`, `gender`, `bfp_bmi`) + `idx_body_composition_snapshots_captured_at` descending index. Idempotent (`CREATE TABLE/INDEX IF NOT EXISTS`). DatabaseHandler pattern only.
- **Edit** `app.py` — imports + calls `add_body_composition_snapshots_table()` in the startup sequence immediately after `add_user_profile_tables()`. Also registered in the `/erase-data` drop-list (between `user_profile` and `user_selection`) and in the post-drop re-init block.
- **Edit** `tests/conftest.py` — imports the new migration, calls it in `_initialize_test_database()` (between `add_user_profile_tables()` and `initialize_exercise_order()`), adds `body_composition_snapshots` to the inner `erase_data()` drop-list, and adds it to the `clean_db` fixture's per-test DELETE list.
- **New** `tests/test_db_migration.py` — 7 cases. Coverage: expected columns (incl. NOT NULL set), index existence + indexed column, idempotent re-run, accepts Navy-style insert, accepts BMI-only (tape-blank) insert, rejects missing NOT NULL, `/erase-data` recreates table + index.
- **New** `docs/body_composition/OPUS_START_PROMPT.md` — reusable prompt that scoped this workstream to the backend-first slice and preserved the fatigue / profile-hook / YouTube-curation guardrails.

**Verification (2026-05-20, second slice — pre-merge):**

- Original Opus targeted pytest: `.venv/Scripts/python.exe -m pytest tests/test_body_composition_routes.py tests/test_body_fat.py tests/test_db_migration.py -q` → **66 passed in 7.25s** (17 route tests on top of the 49 first-slice tests).
- Original Opus startup-touching subset: `.venv/Scripts/python.exe -m pytest tests/test_body_composition_routes.py tests/test_body_fat.py tests/test_db_migration.py tests/test_database_user_profile.py tests/test_harness_isolation.py tests/test_user_profile_routes.py tests/test_program_backup.py -q` → **132 passed in 21.06s**.
- Original Opus full pytest: `.venv/Scripts/python.exe -m pytest tests/ -q` → **1371 passed in 173.08s** (17 net new tests vs. 1354 first-slice baseline; no regressions).
- Opus post-Codex full pytest: `.venv/Scripts/python.exe -m pytest tests/ -q` → **1372 passed in 189.58s** (18 route tests after the profile-demographics contract test; no regressions).
- Original Opus Playwright targeted: `npx playwright test e2e/body-composition.spec.ts --project=chromium --reporter=line` → **4 passed in 5.4s**.
- Codex review pytest after fixes: `.venv/Scripts/python.exe -m pytest tests/test_body_composition_routes.py tests/test_body_fat.py tests/test_db_migration.py -q` → **67 passed in 4.76s**.
- Codex review Playwright, final: `npx playwright test e2e/body-composition.spec.ts e2e/smoke-navigation.spec.ts e2e/nav-dropdown.spec.ts --project=chromium --reporter=line` → **20 passed in 42.7s**.
- Codex review intermediate checks: same 20-spec sweep first exposed a strict-fixture failure after temporarily adding Profile to `nav-dropdown`'s backup-route list (`19 passed, 1 failed in 47.1s`; existing Profile bodymap SVG console error), then passed after narrowing that list back to the primary flow plus `/body_composition` (`20 passed in 42.8s`). `e2e/nav-dropdown.spec.ts` then failed twice while adding the no-clipped-label assertion (`5 passed, 1 failed in 19.7s` for clipped `Body Composition`; `5 passed, 1 failed in 19.0s` after an over-tight primary-pill adjustment), and finally passed after the targeted CSS width fix: `npx playwright test e2e/nav-dropdown.spec.ts --project=chromium --reporter=line` → **6 passed in 18.7s**.
- One unrelated flake from the original Opus pass remains noted: `e2e/accessibility.spec.ts:283 focus returns after modal closes` (modal close on `/workout_plan` — independent of body composition; passes in isolation).

**Explicitly NOT built in this slice (still deferred):**

- Profile-page display hooks (Issue #17 / #18 sub-lines: bodyweight-tile *Lean mass* + transparency-card *"Body fat: X % · {ACE band}"*) — owner-deferred follow-up after `/body_composition` ships and snapshots are routinely captured.
- Visual-baseline screenshots for `/body_composition` — out of scope for this slice; can be added later if owner wants pixel diffs.

Working tree post-merge: clean except for `data/database.db` (runtime, kept dirty by owner policy). `utils/fatigue.py`, `tests/test_fatigue.py`, and `scripts/fatigue_calibration_report.py` were **not touched**.

### Workstream queue (post Body Composition Issue #21)

No active workstream is currently in-flight on `origin/main`. Owner-approved queue (from the section above) still applies: Profile-page hooks (Issues #17 / #18) are the natural next step now that `/body_composition` ships and snapshots can accumulate, but owner has explicitly held them — do not start without a fresh go-ahead. YouTube curation is similarly held. Wait for owner direction.

### Closed workstreams (do not reopen as "next task")

- **Redesign post-P8 triage** — closed 2026-05-19 after verification against `origin/main`. 10 of 11 issues shipped (#2 `9052337`, #3+#4 `0a41725`, #5 `7880618`, #6 `38b1f59`, #7+#8 `9b0c71b`, #9 `a95b067`, #10 `f6e39d6`, #11 `f7d9f12`); #1 (nav Backup link) deferred by owner choice. `debug/redesign_post_p8_issues_SESSION_STATE.md` is historical only.
- **phase5_3i_plan** — closed 2026-05-19 as accepted-as-shipped. Planning doc `docs/phase5_3i_plan.md` was authored 2026-04-15 (`c0da18e`) and deleted 2026-04-24 (`635fa3e`) with the rest of the spring-cleanup planning suite. The 5A–5H retroactive confidence-recovery validation gates never ran, but the underlying `12c90ac` refactors (3i-a..3i-h decompositions) have held under the test baseline for 5+ weeks (1160 passed; baseline rose from 934 at session-state writing) with no regression traced back to them. `debug/phase5_3i_plan_SESSION_STATE.md` is historical only. Re-open only if a concrete regression appears in one of the decomposed functions.

### Closed — workout.cool §4 / §4.6 / §5 follow-ups

All previously-tracked follow-ups have shipped:

- §4.6 pixel baselines locked via `toHaveScreenshot()` in `b5b8c7a` (2026-05-23). 18 committed PNG baselines at `e2e/__screenshots__/visual-baseline-thumbnails.spec.ts-snapshots/`.
- §5 YouTube curation closed by diminishing returns at 56 rows (`cf21191` + `ff244aa`, 2026-05-23). Reopen only if owner supplies new vetted IDs — see [YOUTUBE_REFERENCE_VIDEOS.md "Curation Closed"](workout_cool_integration/YOUTUBE_REFERENCE_VIDEOS.md).
- Worktree disposition closed by inspection + branch cleanup in `21859a1` (2026-05-23). See [LEFTOVERS_BY_PRIORITY.md §6](LEFTOVERS_BY_PRIORITY.md).

### Fatigue meter Phase 2 — Stage 4 calibration window CLOSED (status updated 2026-08-13)

Phase 1 shipped; Phase 1 Stage 4 closed 2026-05-20 (no threshold changes). **Phase 2 Path 1 shipped 2026-05-23 via PR #35 (`d5b80bf`); Phase 2 Stage 3 verify-suite gate closed 2026-05-24 (`1a93f66`); Phase 2 Stage 4 calibration window opened 2026-05-24 and CLOSED 2026-08-13 — owner decision, no real-use evidence, no threshold change.** Source of truth: [`docs/fatigue_meter/PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md) Stage 4 + §10. `calibration-notes.md` remains the Phase 1 Stage 4 authority; STAGE4_PARKED_HANDOFF.md is superseded.

**Why it closed.** The window collected no real-use evidence in ~12 weeks; the measurement and the three-part reopen bar are in [`PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md) §5 Stage 4. The observer scripts and their 26 tests are kept for a possible restart; only the standing instruction to run them is retired.

**Live calibration guardrails — unchanged by the close** (do not, without an explicit new owner override):

> **These guardrails bind the definitions, not the re-export.** `utils/fatigue.py` is a facade and remains the correct *import* path for code, but editing a leaf module under `utils/_fatigue/` is a threshold change even though `utils/fatigue.py` shows no diff.

- Edit `utils/_fatigue/per_muscle.py::MUSCLE_VOLUME_LANDMARKS` / `utils/_fatigue/core.py::SESSION_FATIGUE_BANDS` / `WEEKLY_FATIGUE_BANDS` (per-muscle and global thresholds remain §24.B defaults + BRAINSTORM §5 verbatim for the 12 ranked muscles).
- Edit `tests/test_fatigue.py` boundary-classification tests.
- Tune `scripts/fatigue_calibration_report.py::SCENARIOS` (Hypothesis B retune of `hard_4d` is a documented-not-applied deferred follow-up).

**Calibration evidence that *would* have to be collected** — retained as the restart recipe, not as an open chore (per [`PHASE2_PLANNING.md`](fatigue_meter/PHASE2_PLANNING.md) Stage 4 / §10):

- Per-muscle band disagreements recorded as `(muscle, period, engine band, felt label, direction)`. **Two same-direction disagreements = signal; one isolated disagreement = noise** (Phase 1 §4.2 rule).
- Real-use only: `workout_log` data drives the signal. Synthetic generator mismatches do not justify threshold changes (Phase 1 `hard_4d` precedent — scenario under-shoot, not threshold drift).
- `/fatigue` UX notes: MRV sort usefulness, period selector reach (this session / this week / last 4 weeks), `fatigue == 0 → "—"` SFR sentinel behavior, planned-vs-logged side-by-side usefulness vs clutter.
- Watch the six unranked labels (Front-Shoulder, Rear-Shoulder, Lower Back, Hip-Adductors, Middle-Traps, Neck) — `—` neutral state is intentional pending vetted MEV/MAV/MRV (Phase-3 follow-up).
- Watch the `Unassigned` bucket — should stay empty in `workout_log`-driven bars (501 sentinel rows verified dormant at Stage 1); if a logged set lands there, name the offending exercise as a catalog cleanup signal.
- Link reciprocity (badge → page, page → summary) and console errors.
- `movement_pattern` cleanup (454 NULLs → 0) shipped 2026-05-25 via local `df9b6f9` — see [PHASE2_PLANNING.md §10](fatigue_meter/PHASE2_PLANNING.md) Open follow-ups item #5 (76 inferred, 378 `"unassigned"` sentinel; pytest 1442 → 1443).

Threshold tuning requires both the ≥2 same-direction real-use disagreement bar AND a fresh owner go-ahead.

**Earlier history (preserved):**

- 2026-05-20 — Phase 1 Stage 4 close (owner labeled 5 anchors; 4/5 agreed; 1 isolated `hard_4d` synthetic disagreement → no threshold change).
- 2026-05-20 — PR #26 (`2b34b50`) docs-only synthetic-override / coherence pass; PR #28 (`63c745d`) presentation-only badge restyle.
- 2026-05-23 — Phase 2 Stage 0 lock PR #33 (`24c6f46`); Stage 1 close PR #34 (`be22286`); Stage 2 ship PR #35 (`d5b80bf`).

## Agent Authority

Agents may, without asking the owner:

- Update docs that are stale relative to committed `origin/main` state.
- Run targeted pytest / Playwright checks.
- Continue from one listed task to the next after tests pass.

Agents must not:

- Reset, force-push, or otherwise discard working-tree state without owner approval.
- Commit `data/database.db` (runtime; agents-must-not list in CLAUDE.md).
- Edit `utils/_fatigue/per_muscle.py::MUSCLE_VOLUME_LANDMARKS` / `utils/_fatigue/core.py::SESSION_FATIGUE_BANDS` / `WEEKLY_FATIGUE_BANDS` (per-muscle and global thresholds; gated by the "Live calibration guardrails" block above — the Phase 2 Stage 4 close on 2026-08-13 did **not** discharge that gate).
- Edit `tests/test_fatigue.py` boundary-classification tests.
- Tune `scripts/fatigue_calibration_report.py::SCENARIOS`.
- Touch unrelated dirty files unless the active task requires it.

## Stop Conditions

Ask the owner only if:

- A destructive DB reset, branch reset, or file deletion is required.
- License / attribution status is unclear.
- A product behavior change would exceed the approved plan.
- Tests reveal a broad unrelated regression.
- The owner explicitly redirects the work.

Transport failures, idle stream stalls, or stale chat titles are not repo blockers. Start a fresh agent session and point it at this file.

## Required Checkpoint Closeout

Before calling a checkpoint done:

- Update `docs/MASTER_HANDOVER.md`.
- Update `docs/workout_cool_integration/EXECUTION_LOG.md` for workout.cool work; or the equivalent workstream log for other workstreams.
- Record tests run and results.
- Leave the diff commit-ready, with generated DB/runtime files excluded unless explicitly intended.
