# Active Development

**No longer the execution source of truth.** The actionable queue is
[`OPEN_WORK_EXECUTION_PLAN.md`](OPEN_WORK_EXECUTION_PLAN.md) §0 and the entry point is
[`MASTER_HANDOVER.md`](MASTER_HANDOVER.md) *Current State*. This file keeps, verbatim, the fatigue
calibration guardrails and the agent authority, stop-condition and checkpoint rules; their
references to "this file" and to "listed" tasks predate the split, and rewording them is WS2
scope (`project_direction/AGREED_PLAN.md` §4). Its earlier
objectives and status blocks moved on 2026-10-20 to
[`archive/2026/active-development/ACTIVE_DEVELOPMENT_HISTORY.md`](archive/2026/active-development/ACTIVE_DEVELOPMENT_HISTORY.md);
the V1 and frozen-Windows closures they record are ADR-011 and ADR-012 in [`DECISIONS.md`](DECISIONS.md).

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
