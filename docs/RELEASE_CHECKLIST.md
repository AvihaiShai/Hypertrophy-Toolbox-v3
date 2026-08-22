# Release Checklist

*The permanent manual layer. `release.yml` gates the machine-checkable half; this file
is the half no automation catches — that a build is usable, not merely responsive.
Budget 10 minutes. Run it before every tag, on the frozen build, never on a source
checkout.*

Owner of the automated half: [`.github/workflows/release.yml`](../.github/workflows/release.yml).
Design record and residuals: [`docs/release_pipeline/PLANNING.md`](release_pipeline/PLANNING.md).

---

## 0. Isolate the runtime — **mandatory, before anything else**

Every step below writes to whatever runtime is active, and **step 9 erases it
completely**. `erase_data()` drops all owned tables *including* `program_backups` and
`program_backup_items` ([`app.py`](../app.py)), so running this pass against your real
runtime destroys your training history and every in-app backup with it.

```powershell
$env:HT_RUNTIME_DIR = "$env:TEMP\ht-release-check"
```

`HT_RUNTIME_DIR` relocates the database, backups and logs in one move
([`utils/runtime_paths.py`](../utils/runtime_paths.py)). Confirm it took effect before
step 1: the app's log and database must be under that path and nowhere else. Delete the
directory when the pass is done.

## 1. Confirm a run exists for this tag — **do this first, do not skip it**

```bash
gh run list --workflow=release.yml --limit 5
```

**The tag trigger has never executed.** Packet R1's only validation route is
`workflow_dispatch` with `dry_run: true` (owner option (c), 2026-08-14), and that
dispatch runs post-merge. If no run appears within about two minutes of the push, the
trigger did not fire — a silent failure the pipeline cannot detect from inside itself,
and no green elsewhere substitutes for this check.

## 2. Confirm the contexts the gate expects still match branch protection

```bash
gh api repos/{owner}/{repo}/branches/main/protection/required_status_checks --jq '.contexts'
```

Compare against `REQUIRED_CONTEXTS` in [`scripts/release_gate.py`](../scripts/release_gate.py).
pytest runs offline and cannot see branch protection, so drift there is invisible to
every automated check in the repository — this read is the only thing that catches it.

**"`main` is green" means all 13 expected contexts, not the 12 required ones.**
*(11 and 12 until 2026-08-22, when npm-audit M4 / lever L3 promoted
`JS Supply Chain (npm audit, non-required)` into branch protection.)*
`Visual Regression (Windows baselines)` is *not* branch-protected, so `main` can merge
with it red; the release gate will then fail at tag time, after the version-bump PR has
already landed.

## 3. Plan — `/workout_plan`

Build a two-exercise routine: filter the catalog, set reps/sets/weight/RIR, save.
Reload the page and confirm both exercises persist in the order you left them.

## 4. Log — `/workout_log`

Record actual performance against that plan: scored reps, weight, RIR. Confirm the
logged values survive a reload and match what the plan expected.

## 5. Analyze — `/weekly_summary` **and** `/session_summary`

Both pages, not one. On each, confirm **Effective sets** and **Raw sets** render side by
side, and that the CountingMode and ContributionMode controls actually change the
numbers. A frozen build can serve HTTP 200 with this display contract broken, and the
packaged smoke only checks the status code.

## 6. Progress — `/progression`

Confirm a double-progression suggestion appears for the logged exercise and that it
recommends either more weight or more reps — not both, not neither.

## 7. Distribute — `/volume_splitter`

Allocate weekly sets across muscles. Confirm the resulting split sums to the input
total and that no muscle receives a negative or fractional-set allocation.

## 8. Profile — `/user_profile`

Save a reference lift and a rep preference. Confirm the value drives a Workout Controls
estimate on `/workout_plan`. **This page is not in the packaged smoke's page sweep**
([`scripts/smoke_packaged_app.py`](../scripts/smoke_packaged_app.py)), so this step is
its only coverage in a frozen build.

## 9. Backup and restore — `/api/backups`

Snapshot the program, change something visible in the plan, restore, confirm the change
is undone.

## 10. Erase — `POST /erase-data`

Confirm the confirmation guard rejects a missing or wrong `confirm` value, then erase
and confirm the app still boots to a working empty state.

**Erase drops the backup tables too.** The step 9 result is destroyed by this step, so
they must run in this order — a backup verified *after* an erase proves nothing about
the build a user upgrades into.

## 11. Tear down

Delete `$env:HT_RUNTIME_DIR` and unset it. Confirm your real runtime is untouched:
its database and `auto_backup/` should have the modification times they had before
step 0.

---

## What this checklist does not cover

- The **tag trigger firing at all** — step 1 is a manual compensation, not a proof.
- The frozen executable against a **historical-schema** database. The packaged smoke
  proves an install-directory database relocates intact; it does not plant an
  *old-schema* one. That gap is R1-D5, deferred to a follow-up packet.
- Exploratory QA. Use the `manual-qa-reviewer` agent for the category no scripted pass
  finds: layouts that are technically correct but unusable, suggestions that are
  arithmetically right but wrong in the gym.
