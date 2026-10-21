# R2.3 qualification evidence — 2026-10-20

> **Owner ruling recorded 2026-10-21:** this remains the dated evidence snapshot.
> Its 49-carrier credit uses the stricter workflow-level exclusion considered
> before sign-off. The owner subsequently selected exact JS Unit job conclusions
> under §13.0, so the cycle has **50 green JS executions**, zero adverse JS job
> results, and one separately preserved cancelled CI carrier. The pending
> canonical ledger landing and conditional D2 signature are recorded in
> [DECISION.md](DECISION.md). No rerun copy counts as another execution.

**Read at 2026-10-20T20:09:59.748489+00:00**, main `1f5ae0f059f6cb4a994f92b6e03c57d689fd060c`. This is a
dated read-only snapshot, not an owner ruling or a report of activated protection.
The proposed decision is in [DECISION.md](DECISION.md).

## Method and accounting

Queried GitHub's `actions/workflows/ci.yml/runs` with pagination, branch `main`,
all events, `created >= 2026-08-27T23:00:00Z`; selected T0's carrier
`33125767570` (created `2026-08-27T23:17:53Z`) onward. The earlier carrier
`33124861791`, created `2026-08-27T23:03:13Z`, is outside this cycle.
Every selected run was resolved through `/actions/runs/<id>/jobs?filter=all`
with pagination. Matched the exact display name `JS Unit (Vitest, non-required)` and checked
the actual `Run Vitest with coverage` step. No workflow conclusion is substituted
for a JS job result. Raw API responses and the read-only collector are retained
locally under `artifacts/r23/`; the compact audit is included as
[main-js-jobs.csv](main-js-jobs.csv), with job URLs, timestamps and attempts.

| Measurement | Result |
|---|---|
| Declared T0 / strict mark | `2026-08-27T23:18:21Z` / `2026-09-10T23:18:21Z` |
| Main carriers inside the qualification window | 50: 49 successful, 1 cancelled |
| JS job entries in that window | 51 successful entries; rerun entries are not independent executions |
| Missing / failed / skipped / cancelled JS jobs inside the window | 0 / 0 / 0 / 0 |
| Cancelled carrier | [34170988104](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/34170988104); **excluded from qualification credit** |
| Last carrier before strict mark | `34170988104`, created `2026-09-07`; cancelled carrier, JS execution successful |
| Qualifying carrier credit | **49**, matching CI PLANNING §11.5's independent 39 + 10 reconciliation |
| All main carriers through this snapshot | 88: 86 successful, 1 cancelled, 1 in progress |
| All JS attempt entries through this snapshot | 89; all jobs and Vitest execution steps successful |
| Completed successful carriers after the qualification window | 37 |
| In-progress carriers | 39489279999; no workflow-success or qualification credit |
| Unresolved API reads inside the selected cycle | 0 |

The cancelled run has a successful attempt-1 JS job and an attempt-2 entry with
the same execution timestamps. Both are preserved in the CSV; neither a duplicate
execution nor an extra qualifying carrier is claimed. Latest completed carriers
are listed below; an in-progress carrier is excluded from that green sample even
if its JS job has already passed.

## Unchanged corpus and completed predecessor

| Surface | T0 commit `288667d` and audited main |
|---|---|
| `static/js/modules/__tests__` tree | `5858c8497c571548e5116f4b660ff7702dd298b1` |
| `vitest.config.js` blob | `c16ca428f7478708d8dd96a20ebcb86f98a8b935` |
| Commits changing `static/js/**/*.test.js` or `vitest.config.js` after T0 | None |
| Packet F | PR [#411](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/411), merged `2c95bae`; required inventory pins Vitest case identities |

The calendar interval is failure-free and longer than fourteen days. The rule has
no required closing-day execution or minimum-run count. This supports technical
qualification and **does not create the separate D2 owner signature**.
Toolchain updates since T0 are not represented as unchanged: audited main uses
Node 24 and Vitest / coverage-v8 5.0.5; the current suite is re-executed below.

## Latest ten completed carriers

| Main run | Head | JS job | Job completed UTC | JS + Vitest step |
|---|---|---|---|---|
| [39271181244](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39271181244) | `de05ef29` | 118123572058 | 2026-10-19T14:47:37Z | success |
| [39275601853](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39275601853) | `f85ec050` | 118138993535 | 2026-10-19T15:11:01Z | success |
| [39308135423](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39308135423) | `c7fec052` | 118250416341 | 2026-10-19T19:06:31Z | success |
| [39308234107](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39308234107) | `f3adacf1` | 118250757944 | 2026-10-19T19:07:59Z | success |
| [39428398134](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39428398134) | `1a5e0e6f` | 118646705547 | 2026-10-20T13:12:38Z | success |
| [39430536736](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39430536736) | `48d6a450` | 118654126696 | 2026-10-20T13:27:52Z | success |
| [39444332091](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39444332091) | `b86e9ad7` | 118702128572 | 2026-10-20T15:00:19Z | success |
| [39445358053](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39445358053) | `3b21384c` | 118705697180 | 2026-10-20T15:06:59Z | success |
| [39445379283](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39445379283) | `a305e5a4` | 118705785047 | 2026-10-20T15:10:57Z | success |
| [39449180398](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/actions/runs/39449180398) | `71c4cc6d` | 118719077698 | 2026-10-20T15:31:42Z | success |

## Live protection snapshot and proposed additive payload

Live GET `/branches/main/protection/required_status_checks`: **12** contexts,
`strict: false`, all `app_id: 15368`; both `JS Unit (Vitest, non-required)` and
`JS Unit (Vitest)` are absent. No settings write was performed.
[required-status-checks.proposed.json](required-status-checks.proposed.json) preserves
all twelve exact names/bindings and `strict`, adding only `JS Unit (Vitest)`.
This is a review snapshot; activation must re-read and compare the live floor,
merge the corresponding contracts first, obtain C4 authority and verify blocking.

## Local verification

- Private checkout dependencies installed from the committed lockfile.
- `npm run test:js -- --coverage`: **13 files / 245 tests passed**; statements
  8.24%, branches 10.77%, functions 7.95%, lines 8.07%. Coverage is informational.
- Targeted Vitest-inventory, release-gate and release-workflow pytest contracts:
  **196 passed initially; five environment failures all passed after selecting
  Git Bash**. The initial launcher was `C:/Windows/system32/bash.exe` with no WSL
  distribution; the corrected process PATH starts with `C:/Program Files/Git/bin`.
  No source or test change was used to repair the environment.
- `scripts/generate_test_inventory.py --check`: **up to date** on the audited base.

These checks support the decision. They are not the future workflow-change full
pytest gate, an independent reviewer pass, or live merge-blocking evidence.
