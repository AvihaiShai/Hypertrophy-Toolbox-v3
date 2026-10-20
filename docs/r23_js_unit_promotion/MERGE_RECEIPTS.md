# R2.3 merge receipts — 2026-10-21

The owner explicitly approved **#544, then #547**. Both were rechecked at their
approved heads before squash merge: **27 of 27 checks successful**, all produced
by GitHub Actions `app_id: 15368`. No bypass or branch deletion was requested.

| PR | Approved head | Main squash | Merged UTC |
|---|---|---|---|
| [#544](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/544), canonical ledger | `72de3e223aa781603a5a5a6182999e2695de84c8` | `b4a2653c0b64965a6bd906ebb981fef0cd412bf7` | 2026-10-20T23:15:04Z |
| [#547](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/547), owner ruling/evidence | `fea91820179f80bd97edc2d5c7907863ce70c2e1` | `aafba153cd0508d4f92934c3bf622ef0e9a9ff40` | 2026-10-20T23:15:25Z |

Fetched main contains both receipts in that order. Every canonical cycle row
26–75 matches the independently verified run ID, JS job ID, completion timestamp
and successful conclusion: **50 green / 0 red / 0 missing / 0 skipped / 0
cancelled JS executions**. The cancelled carrier stays recorded separately;
the attempt-2 copy remains one execution. **D2's ledger condition is fulfilled
and its approval is effective.** T0 and the strict mark are unchanged.

## Post-merge JS observations

These are exact-job results, not overall main-workflow success claims. The two
documentation merge workflows were still `in_progress` at the receipt snapshot.

| Ledger row | Main carrier | Main run | JS job | Completed UTC | JS result |
|---|---|---|---|---|---|
| 114 | #540 / `43f5df33` | [39504386125](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39504386125) | [118909532396](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39504386125/job/118909532396) | 2026-10-20T21:57:09Z | success |
| 115 | #544 / `b4a2653c` | [39513763499](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39513763499) | [118940855860](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39513763499/job/118940855860) | 2026-10-20T23:15:29Z | success |
| 116 | #547 / `aafba153` | [39513805113](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39513805113) | [118940988132](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39513805113/job/118940988132) | 2026-10-20T23:16:00Z | success |

The first-parent range `1f5ae0f0..aafba153` has exactly three main commits and
matches these three CI carriers one-to-one. A branch-wide all-workflow census
after the ledger's prior `2026-10-20T20:20:57Z` cutoff found five runs: these
three and scheduled Deep Gate Watch runs `39504346169` and `39507750144`.
Both watch runs have zero exact-name JS jobs and are classified non-attempts.
The rows are carried through §13.0 in this rename change, following §11.10.
Its own eventual merge will owe the next unclaimed row; no future number is
predicted.

## What remains separate

- **Q4:** the standalone rename is reviewed and locally validated (5,580 Python
  tests passed / 2 skipped; 245 JS tests passed; inventory and type checks clean).
  Its publication waits for #546 to free the shared CI workflow slot; #546 was
  still open at head `a8fca06806f2e2e1bce234f8ec7937543e72a9e6` at this read.
- **C4:** not approved or executed. Protection remains **12** contexts,
  `strict: false`, JS Unit absent. The rename does not add a requirement or
  change release expectations. A separate owner approval and live enforcement
  proof are still required for settings activation.
- **Verification reuse:** the tests, workflow tree and executable Vitest config
  are unchanged from the reviewed/tested rename commit; merging the two approved
  documentation PRs required no new full application test run. The new receipt
  and ledger annotations receive documentation self-review.

API receipts, exact job observations and the census are retained locally in
`artifacts/r23/merge-receipts.json`. No release, tag, baseline regeneration or
repository settings write was performed.
