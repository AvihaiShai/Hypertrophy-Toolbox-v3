# MSYS destination validation and drive-root monitoring — closeout

2026-10-28. This packet is accepted at all four levels below, by the manager under the
owner's task-specific delegation recorded in [PLANNING.md](PLANNING.md). Gate 0 remains the
owner's approval; these later decisions are delegated acceptance, not personal owner review.
`PREVENTION_COMPLETE` is not claimed.

| Level | Result | Evidence |
|---|---|---|
| Implementation | Accepted (delegated), exact candidate `68d52ba74a53a8ba4807842e512719b12e0a94fb` | 34/34 CI checks, all 12 protected context/app pairs, 34 AC7 neutralization arms, restored scope 2,301 passed / 1 documented skip, final corpus 69/12,612. [Acceptance evidence](evidence/ACCEPTANCE_20261028.md). |
| Merge | Accepted (delegated) | [PR #654](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/pull/654) merged through normal protections at `2026-10-28T15:56:55Z` as `d8e3e3c61866ca0fa123693335d65775d880225e`. No bypass; source branch retained. |
| Installation | Accepted (delegated) | User guard and monitor match the merged blobs; parse checks, staged/installed guard probes and monitor fixture checks passed. Settings changed by a verified pure insertion. Backup and rollback are retained. |
| Operational | Accepted (delegated), bounded headless check | Fresh extension-bundled `claude.exe` 2.1.310 session: exact guard refusal, SessionStart snapshot, silent first Stop, NEW notice and UNKNOWN notice. All Stop hooks and the CLI exited 0. Fixture child and mapping removed. |

The implementation PR is merged and the controls are installed. This closeout records the
packet's bounded operational acceptance; the coverage limits below remain.
The panel follow-up below additionally records owner-confirmed NEW rendering on 2.1.312.

## Installed copies and recovery

Only user-level files were installed under `C:\Users\aviha\.claude`. Existing PreToolUse
registration loads the updated guard. One SessionStart and one Stop entry load the monitor,
with `-Mode HookSessionStart` / `-Mode HookStop` and timeout 30. Project registrations were
not added. The shared checkout's guard and settings retain their original hashes.

| User file | Merged blob | Installed SHA-256 |
|---|---|---|
| `hooks/guard-destructive-command.ps1` | `427ae4c5ff28f23a41d765ae1e40928237d064fb` | `d66c52ef31db6342fb5b614d2ac0b1f3ffab171693a150d33df875892223f322` |
| `hooks/drive-root-monitor.ps1` | `6993a66d530fe2725d4fadc5c826ee1673d8765f` | `638fddd1b8d05749214e6c4a88f865ef112a8f3cd1f7042f5edf58bfa7617e79` |

Real-profile dry run: `C:\ht\MSYS-INSTALL\transcript-20261028T155711Z.json`.
Installation: `C:\ht\MSYS-INSTALL\transcript-20261028T155730Z.json`.
Byte-for-byte backup: `C:\ht\MSYS-INSTALL\backup-20261028T155730Z\`.
Prepared rollback: `C:\ht\MSYS-INSTALL\ROLLBACK.ps1 -BackupDir
C:\ht\MSYS-INSTALL\backup-20261028T155730Z -Execute` (run from PowerShell).
Install and rollback were rehearsed on a fake profile before the real installation; the real
installation remains active.

## Operational evidence

Accepted run: `C:\ht\MSYS-OPS\run-sol-20261028T155934Z\summary.json`, with retained stdout,
stderr, snapshots and harness. Session `ff872564-63a6-4d82-a4e8-d39a32deb274` used a disposable
cwd and `Q:` mapped to that run's disposable `qroot` folder.

- The harmless PowerShell resolver call was refused with the required drive-token wording,
  including `From cwd C: a native Windows program resolves it to C:\c\Users\x.`
- SessionStart recorded the fixture root before the first tool call. The first Stop was silent.
- Creating `Q:\probe-child` produced the NEW notice in the real CLI event stream.
- The controller injected malformed JSON only into this test session's own TEMP snapshot.
  The next normal Stop produced the UNKNOWN notice. No guard or registration was modified.
- Stop-hook elapsed times, from hook-start to hook-response events: 0.354976, 0.356810,
  0.395934 and 0.315970 seconds. All four exited 0; CLI exit 0. The fixture child was removed
  and `subst` confirmed no mapping remained.

The first run, `C:\ht\MSYS-OPS\run-sol-20261028T155803Z`, is retained as **incomplete**:
the model declined the requested snapshot corruption, so UNKNOWN was not exercised. Its
first three phases passed and its fixture was removed. It is not credited as full acceptance.

Initial headless acceptance label (panel status at that run): **fresh headless session on
the VS Code extension's bundled claude.exe
2.1.310; payload fields and Stop notice measured on the bundled 2.1.310 binary (headless) and
CLI 2.1.302; panel rendering unmeasured (open); detection exercised on a substitute (subst)
root; guard shown on one harmless row; charter-frontmatter payloads inferred**.

## VS Code panel follow-up — 2026-10-28

A fresh interactive VS Code Claude Code **2.1.312** session
`9313ae9d-8fb7-439b-81c7-d12542caa097` exercised the installed user-level monitor.
This extends the earlier headless evidence to owner-visible NEW rendering on this version.
The owner requested this panel check and a docs-only PR, with no merge.

| Observation | Evidence |
|---|---|
| Safe fixture | `Q:` was absent from native logical drives and `subst` before mapping to `C:\ht\MSYS-OPS\panel-20261028T191029Z\qroot`. The mapping was checked again before creating the child. No real drive-root fixture was created. |
| Fresh SessionStart | Snapshot source `startup`, created `2026-10-28T19:11:24.336Z`, recorded `Q:\` with no children before the first submitted message. |
| Baseline Stop | `PANEL_BASELINE_READY`; one Stop hook, 403 ms, no notice or hook errors. |
| Mid-session child | The controller created only `Q:\panel-probe-child` at `2026-10-28T19:12:21.3024557Z`, then submitted a second tool-free panel turn without resuming or clearing the session. |
| NEW Stop | After `PANEL_PROBE_STOP`, the panel rendered the notice below. The transcript records `hook_system_message` at `2026-10-28T19:12:32.227Z`, hook exit 0, empty stderr, duration 435 ms, no prevented continuation. |
| Owner observation | The owner directly confirmed: "Yes, I can see the NEW alert". This confirms NEW panel visibility; it grants no merge or broader acceptance. |
| Cleanup | After owner confirmation, the empty fixture child and `Q:` mapping were removed at `2026-10-28T20:04:43.3230733Z`. Native logical drives were C, D, E and F; `subst` returned no mappings and `qroot` was empty. |

The rendered notice was:

> Stop says: New direct child(ren) of Q:\ since monitoring began at 2026-10-28T19:11:24.336Z: Q:\panel-probe-child. Cause unknown; not necessarily created by this session.

Evidence retained locally in `C:\ht\MSYS-OPS\panel-20261028T191029Z\`:
`summary.json`, `sessionstart-snapshot.json`, `baseline-stop-snapshot.json`,
`new-stop-snapshot.json`, `panel-session-events.jsonl`, `installed-hook-hashes.json`,
`cleanup.json` and the panel-only capture `panel-probe-result.png`.
The session log remains in the user's Claude project directory. Installed guard and monitor
hashes match the installation table above. No hook, setting, app, DB or test was changed.
UNKNOWN rendering and other panel versions were not exercised by this follow-up;
`PREVENTION_COMPLETE` is not claimed.

## Retained limits

- The guard sees command text. Script files, stdin, runtime-built paths, MCP parameters and
  non-Claude processes are outside its coverage. Write path conversion was measured by the
  earlier harness probe; Edit conversion remains inferred.
- The monitor compares direct root children between snapshot and Stop. Writes beneath an
  existing child are invisible; standing single-letter children receive a fault-shape warning.
  Transient children created and removed between observations are also invisible.
- Root changes from other sessions, the OS or the owner are reported with cause unknown.
  Other open sessions may emit one UNKNOWN notice when a fixture drive appears or disappears;
  their UI was not inspected.
- VS Code NEW panel rendering is owner-confirmed on 2.1.312 by the follow-up above;
  UNKNOWN panel rendering remains unmeasured. Linux monitor behavior is covered by CI;
  Windows PowerShell 5.1 behavior is covered locally.
- Accepted textual false-positive classes remain; [the final corpus reconciliation](evidence/CORPUS_PASS_3d85fd9f.md)
  records their counts and pins. The guard is not a filesystem-wide prevention mechanism.

No application/DB changes, drive-root remediation, branch/worktree deletion, general approval
policy changes or Operation A memory edits were performed. H4 creation times remain unchanged.
Retain the clone, branches, environments, backups and evidence pending separate lifecycle
approval.
