# e2e/ — Orientation

## Purpose
Playwright Chromium specs covering UI flows end-to-end. `playwright.config.ts` auto-starts Flask via `.venv/Scripts/python.exe app.py` on port 5000; serial execution (`fullyParallel: false`).

## Key files
| File | Coverage |
|---|---|
| `fixtures.ts` | Shared `test` fixture (console-error collector), `ROUTES`, `API_ENDPOINTS`, `SELECTORS`, `waitForPageReady()`, the page-specific `waitForWorkoutPlanReady()` / `waitForVolumeSplitterReady()` / `waitForBodyCompositionReady()`, `expectToast()` |
| `fixtures/database.visual.seed.db` | Seed DB used by visual specs (committed; whitelisted in `.gitignore`) |
| `smoke-navigation.spec.ts` | Page loads + nav cycle (no fixtures) |
| `dark-mode.spec.ts`, `nav-dropdown.spec.ts` | Theme + navbar |
| `workout-plan.spec.ts`, `workout-log.spec.ts` | Plan/log CRUD |
| `summary-pages.spec.ts`, `progression.spec.ts`, `volume-splitter.spec.ts` | Analyze + progress + distribute |
| `program-backup.spec.ts`, `erase-flow.spec.ts`, `user-profile.spec.ts` | Backup/erase recovery flows, profile questionnaire |
| `exercise-interactions.spec.ts`, `superset-edge-cases.spec.ts`, `replace-exercise-errors.spec.ts` | Per-row actions |
| `validation-boundary.spec.ts`, `error-handling.spec.ts`, `empty-states.spec.ts`, `accessibility.spec.ts` | Edge & a11y |
| `api-integration.spec.ts` | All API endpoints |
| `fatigue-context.spec.ts`, `listener-cleanup.spec.ts` | Advisory fatigue context + listener lifecycle regressions |
| `visual.spec.ts`, `visual-baseline-thumbnails.spec.ts`, `volume-progress.spec.ts`, `fatigue-stage4-smokes.spec.ts` | Visual snapshots + recent feature smokes |
| `visual-field-separator.spec.ts` | Rendered table separator/outline contrast (computed styles, not screenshots) — required functional gate |

Full per-spec test count map: `.claude/rules/testing.md`.

## Conventions
- Reuse the `test` fixture from `fixtures.ts` — it fails specs that emit console errors.
- Reference routes via `ROUTES.X`, selectors via `SELECTORS.X` — keeps locators centralized.
- `npx playwright test --project=chromium --reporter=line` — Chromium only; Firefox/WebKit are not configured.
- `PW_REUSE_SERVER=1` reuses an already-running Flask process.

## Database isolation (web-server command)
- The suite runs against an **isolated throwaway DB**, never the developer's live `data/database.db`. `playwright.config.ts` points `webServer.env.DB_FILE` at `artifacts/e2e/database.e2e.db` and the `webServer.command` seeds it *before* launching the app: `prepare_e2e_db.py --output <db> && python app.py`.
- Seeding lives in the web-server command (not `globalSetup`) on purpose: Playwright starts `webServer` **before** `globalSetup`, so seeding in `globalSetup` races `app.py`'s first DB open (fails in CI on a fresh checkout).
- `e2e/scripts/prepare_e2e_db.py` snapshots the committed seed (`fixtures/database.visual.seed.db`), applies migrations, ensures the learned-calibration tables exist, then **wipes all user-state** (profile, reference lifts, plan, logs, calibration, backups) — full exercise catalog preserved. Every run starts from an identical clean slate; tests must not depend on ambient saved data.
- With `PW_REUSE_SERVER=1` and a server already running, the command (and reseed) is skipped — the reused server owns its own DB.
- `nav-dropdown.spec.ts` uses a real Playwright click for `#darkModeToggle`; keep it that way so desktop navbar actionability stays guarded. `workout-plan.spec.ts` still dispatches `#muscleModeToggle` because that broader workflow has its own historical layout note.

## CI inclusion contract (`e2e-functional-shard` matrix + `e2e-functional` gate / `e2e-backup` jobs)
The GitHub Actions gate runs a curated, deterministic subset on **ubuntu/Chromium** (not every spec). Auditable contract for all specs:

| Spec | CI placement | Reason |
|---|---|---|
| `accessibility`, `api-integration`, `body-composition`, `browser-navigation-state`, `dark-mode`, `empty-states`, `error-handling`, `exercise-interactions`, `fatigue`, `fatigue-stage4-smokes`, `learned-calibration`, `nav-dropdown`, `progression`, `replace-exercise-errors`, `smoke-navigation`, `summary-pages`, `superset-edge-cases`, `ui-hardening`, `user-profile`, `validation-boundary`, `visual-field-separator`, `volume-progress`, `volume-splitter`, `workout-log`, `workout-plan` | `e2e-functional-shard` matrix job (`--shard=i/2`) | Deterministic functional/product coverage |
| `smoke-navigation` | also `e2e-smoke` job | Fast standalone "is the app up" signal |
| `program-backup` | `e2e-backup` job (isolated) | Live backup/restore mutations — own server + fresh seed avoids intra-run sequential-DB pollution without any between-spec reset |
| `fatigue-context` | `e2e-fatigue-context` job (**required**) | WPB.9: promoted after ten consecutive green PRs (#100–#109); its historical `E2E Fatigue Context (Chromium, non-required)` context name is now load-bearing and must not be renamed |
| `erase-flow` | `e2e-erase-flow` job (**non-required**) | Live erase/reset mutation and WPB.8 banner proof run on an isolated server/DB |
| `listener-cleanup` | local/targeted and manual deep gate only | Track A regression instrumentation; intentionally not in the required functional list |
| `exercise-catalog-fetch` | local/targeted and manual deep gate only | Pins the one-fetch-per-load contract for `/get_all_exercises` (duplicate `#routine` `change` listener → duplicate catalog fetch per navigation). Same tier as `listener-cleanup` for the same reason: it is duplicate-registration regression instrumentation, and its second test monkeypatches `addEventListener`. It is *technically* eligible for the required set — plain request count, no pixel/geometry/font dependency, no visual seed, ~5s — but promoting it is a four-file contract change (`ci.yml`, the `RequiredSpecs` array in `scripts/run-playwright-shards.ps1`, the pinned `== 25` in `tests/test_playwright_shard_launcher_contracts.py`, and the ADR-006 reference counts), and that pinned count exists precisely to make promotion a deliberate owner decision. The deep gate needs no edit: its "full suite (minus visual)" step globs `e2e/*.spec.ts`. It uses `networkidle` deliberately — the guarantee that nothing is still in flight is what makes the count final, the inverse of the ADR-005 reason it was removed from the five converted specs. |
| `accessibility`, `fatigue-stage4-smokes`, `volume-progress` | **promoted to `e2e-functional` (A10, 2026-06-11)** | Were measure-first (a11y run-cost; geometry/sub-pixel asserts). Promoted after a 5×-repeat ubuntu stability probe (225/225 green, zero flakes) + the 2026-06-05 deep-gate full-e2e green. Their asserts are coarse thresholds (tap-target ≥32/≥44, viewport-bound ±1px, overflow boolean), not pixel-exact snapshots. Watch the first ~10 PR runs for any geometry flake; revert that one spec line if one appears. **2026-08-13:** `accessibility`'s tap-target assert was tightened from "1 of 5 sampled clears 32px" to "every visible target clears 32px" (Testing Strategy Phase 2, Packet A). On `/` at 375px the binding element is `#eraseDataBtn`, whose height is derived from padding + line-height rather than declared — measured 37.2px, so ~5px of margin that moves with font metrics. If a geometry flake appears here, that is the element to look at. |
| `nav-dropdown` | **promoted to `e2e-functional` (2026-06-11)** | Fixed the 1440px dark-mode-toggle actionability red with compact desktop navbar utility chrome; spec now uses a real Playwright click. |
| `visual`, `visual-baseline-thumbnails` | manual deep gate only (`visual-linux` job) | Cross-OS rendering: compared against Linux baselines, never a required PR check. See "Visual spec contract" below. |
| `workout-plan-desktop-contract` | manual deep gate only (`visual-linux` job) | Carries the coverage of the five byte-gate-exempt captures as computed style / geometry / DOM structure. It needs the plan-bearing visual seed, so it runs in `visual-linux` (which sets `PW_VISUAL_SEED=1`) rather than on the required functional path, and is excluded from the deep gate's "full suite (minus visual)" step for the same reason. |
| `visual-field-separator` | `e2e-functional-shard` matrix job (**required**) | The `visual-` prefix is about *what it measures*, not *how*. It reads composited computed styles and asserts a numeric contrast ratio (WCAG 2.2 SC 1.4.11, ≥3:1) — no screenshot, no baseline, no font/renderer dependency, so it is cross-OS safe and belongs on the required path. It injects its own rows, so it needs no visual seed and runs against `prepare_e2e_db.py` like the rest of the functional set. The deep gate's "full suite (minus visual)" exclusion is anchored to the two snapshot specs by filename for the same reason. |

- The functional/backup specs assert **current shipped behavior**. A future intentional behavior change (e.g. a fatigue Stage-4 threshold tweak) must update the spec deliberately — it should not be treated as "CI caught a regression."
- **Sharded n=2 (leftovers A11).** The functional set runs as a 2-way matrix (`e2e-functional-shard`, `--shard=${{ matrix.shard }}/2`, `fail-fast: false`). Each matrix leg is its own runner with its own setup/server/freshly-seeded throwaway DB (seeded by the `webServer` command per server start), so cross-shard is clean by construction and within-shard serial order-safety (`fullyParallel: false` / `workers: 1`) is unchanged — `playwright.config.ts` is **not** modified for sharding. The **single branch-protection required check** stays the `e2e-functional` **fan-in gate** job, whose name `E2E Functional (Chromium)` must stay byte-for-byte (renaming it orphans the required check and blocks every PR). The per-shard contexts `E2E Functional Shard 1/2` / `E2E Functional Shard 2/2` are **not** required checks — do not add them to branch protection. The gate is `if: always()` + `needs: e2e-functional-shard` and is green iff `needs.e2e-functional-shard.result == 'success'` (i.e. both shards passed). Pre-A11 the single `E2E Functional (Chromium)` job ran ~13 min; the n=2 split runs the shards in parallel for roughly half the wall-clock at 2× runner cost.
- **Artifact-upload privacy**: trace/screenshot/video/HTML-report uploads are safe *because* the suite runs only against the committed, user-state-wiped seed (`prepare_e2e_db.py`) — no real user data. CI must **never** upload the developer's live `data/database.db` or `data/auto_backup/`.

## Local parallelism — N=1 only

**The supported local lane is serial: 25 required specs / 477 tests / 719.0s.**
`scripts/run-playwright-shards.ps1` defaults to `-Shards 1` and is the way to
reproduce that reference.

**Same-machine `-Shards` above 1 is rejected, not merely unproven** — see
[`docs/DECISIONS.md`](../docs/DECISIONS.md) ADR-006. Werkzeug closes the
connection per request, so every one of the suite's ~34k requests (89.9% static
assets) holds an ephemeral port for the 120s recycle window; N=2 peaks at 16,318
of this host's 16,384 ports and fails from a *measured clean start*. N>1 stays
runnable for reproducing that diagnosis and warns at runtime; a green N>1 run is
not evidence. Do not raise a timeout, add a retry, or tune the OS to make it
pass.

**None of that applies to CI.** The `e2e-functional-shard` matrix gives each leg
its own runner, port pool, server and freshly seeded database, so it shares none
of the machine state involved. Its N=2 design is valid and unchanged.

Local wall-clock therefore improves only by making the work smaller. Where that
time actually goes is profiled in
[`docs/E2E_PERFORMANCE_PROFILE.md`](../docs/E2E_PERFORMANCE_PROFILE.md) —
`networkidle` in `waitForPageReady()` is ~30% of the suite, most of it dead
time, but deleting it breaks a real assertion. Read that before optimizing
anything here, and read ADR-005 before proposing a change without timings.

## Visual spec contract (`visual.spec.ts`, `visual-baseline-thumbnails.spec.ts`)
- **Manual deep gate only.** Visual specs never run on the PR path and are **never** a required status check. They run via the `visual-linux` job in `.github/workflows/deep-gate.yml`, opt-in behind the `run_visual` input (`workflow_dispatch`-only). An `if:`-gated, non-required job cannot block merge.
- **Platform-split baselines** (`snapshotPathTemplate` carries a `{platform}` directory segment):
  - **Linux** baselines live under `e2e/__screenshots__/linux/` — used by CI (`visual-linux` job runs on pinned `ubuntu-24.04`). Generated by the job's `generate` mode (`--update-snapshots`), uploaded as the `visual-baselines-linux` artifact, and committed by the owner after review — CI never pushes.
  - **Windows** baselines live under `e2e/__screenshots__/win32/` — the owner's local visual workflow (`process.platform === 'win32'`).
  - The two sets never collide and are maintained independently. An intentional UI change re-baselines both.
- **`PW_VISUAL_SEED=1`** selects the plan-bearing visual seed (`prepare_visual_db.py`) over the user-state-wiped functional seed (`prepare_e2e_db.py`) in the `playwright.config.ts` webServer command, so the throwaway DB is seeded with the canonical visual data (plan rows + `media_path` thumbnails) **before Flask opens it** — no per-spec runtime DB rewrite. The `visual-linux` job sets it; local visual runs set it too. Default (unset) keeps the functional suite on `prepare_e2e_db.py`.
- **Runner image is pinned** (`ubuntu-24.04`, not `ubuntu-latest`): the generate and compare runs must share one image so the Chromium/freetype/font renderer matches by construction. A deliberate runner bump requires a re-baseline (`generate`); a silent `ubuntu-latest` promotion must not move pixels.
- **The prepared visual DB is already catalog-upgraded.** `prepare_visual_db.py` runs `upgrade_catalog_from_seed()` itself (`apply_migrations(..., upgrade_catalog=True)`). Without it `app.py` applied that upgrade ~1.6 s *after* the port opened — past Playwright's TCP-only readiness check — flipping `youtube_video_id` from all-NULL to 56 curated ids under a running capture, which gave every plan-bearing baseline two legal renderings. `prepare_e2e_db.py` shares the helper but keeps the upgrade **off**: `workout-plan.spec.ts` asserts the uncurated search-icon branch. See `docs/visual_determinism/PLANNING.md`.
- **Captures are segmented above 16,384 px.** Chromium truncates a taller `fullPage` screenshot to a flat, unpainted tail instead of failing. `expectFullPageScreenshot()` in `visual-helpers.ts` splits such a page into `<name>-segment-N.png` bands of `CAPTURE_SEGMENT_HEIGHT_PX`; every shorter page keeps its single baseline and its existing name. Only `user-profile-mobile-{dark,light}` is affected, so a regenerated `visual.spec.ts` platform carries **66** baselines (66 + 4 segments − 2 retired − 2 byte-gate-exempt) while `visual-baseline-thumbnails.spec.ts` carries **15** (18 − 3 exempt). Re-baselining that pair must also bump that platform's `EXPECTED_SNAPSHOT_COUNTS` entry in `tests/test_css_wp4_4_a_baseline_contracts.py`, regenerate `snapshotManifest` in `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` (`scripts/css_audit/emit_baseline.py`), and remove that platform's relative paths from `AWAITING_SEGMENTED_REGENERATION` in `tests/test_visual_capture_contracts.py`. The set becomes empty only after both independently maintained platforms are regenerated.
- **`prepareForScreenshot` blocks on decoded images.** `networkidle` fires *before* a below-fold `loading="lazy"` image is requested, so the capture used to race the raster it had just triggered. `waitForImagesSettled()` forces `loading="eager"` on the live DOM (a capture-time override — production markup keeps lazy loading), then waits for `complete && naturalWidth > 0` on every image and awaits `decode()`. It throws with the pending `src` list rather than proceeding; never shorten the wait to make it pass.
- **Five captures are exempt from byte comparison.** `BYTE_GATE_EXEMPT` in `visual-helpers.ts` names them: `workout-plan-desktop-{light,dark}`, `plan-desktop-{light,dark}-advanced`, `plan-desktop-dark-simple`. Chromium rasters exactly these five nondeterministically on `ubuntu-24.04` — measured over 8 experiment sets / 21 generations at 6 capture configurations, each flips between two states at **byte-identical layout**, and six documented capture controls failed to close it. They still run, still render at 1440×900, and still fail on a console error; only the pixel diff is dropped, and they have no committed PNG on either platform. Their coverage lives in `workout-plan-desktop-contract.spec.ts` (computed style + geometry + DOM structure), which runs beside them in `visual-linux`. Full evidence and the per-capture replacement table: `docs/visual_determinism/PLANNING.md` §8. **Do not add to this set** to quiet a failure — `tests/test_visual_capture_contracts.py` pins it as a strict equality, and two other captures that were seen to flip (`log-desktop-light` 178px, `workout-plan-mobile-light` 13px) deliberately stay on the gate because they land under the existing 800px tolerance.

## Gotchas
- **Known historical flake**: `program-backup.spec.ts` (`Backup Center Page` describe block) — sequential DB-pollution flake observed in earlier full runs; passes in isolation. This is why CI runs it in the isolated `e2e-backup` job (see CI inclusion contract above), not alongside other DB-mutating specs.
- Visual snapshot regressions need an intentional re-baseline. Don't blanket-`--update-snapshots`.
- Chromium is the only configured project (`playwright.config.ts`).

## See also
- `.claude/rules/testing.md` — spec inventory + baselines
- `/run-e2e` skill (full or single spec) and `/verify-suite` skill (full gate)
- [docs/E2E_TESTING.md](../docs/E2E_TESTING.md)
