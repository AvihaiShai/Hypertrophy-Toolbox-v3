# Root Directory Cleanup and Data Packaging Safety Plan

**Status:** Packets A0, A, and A2 shipped. Packet A3 and Packet B are
owner-approved and next; Packet C is unstarted.

**Last evidence pass:** 2026-07-26

**Scope:** Repository-root hygiene, shipped database privacy, PyInstaller data
allowlisting, first-run database bootstrap, and the later runtime-data location
decision

---

## 1. Purpose

The original concern was that nearly every root-level file other than
`app.py`, `CLAUDE.md`, `README.md`, and `requirements.txt` looked like clutter
accumulated during development.

The audit found three different problems that must not be treated as one:

1. **Disposable local artifacts in the root.** These were real clutter and have
   already been removed locally.
2. **Legitimate root-level project files.** Most configuration files are in the
   correct place because their tools discover them from the repository root.
3. **A data-boundary and packaging defect.** The tracked database contains user
   state, while both packaging definitions recursively include the entire
   on-disk `data/` directory, including ignored personal files and backups.

This document records the evidence, decisions, implementation packets,
checklists, acceptance criteria, rollback strategy, and blind spots. Its goal is
to prevent a cosmetic cleanup from either deleting working project
infrastructure or missing the more important privacy problem uncovered by the
audit.

---

## 2. Goals

- Keep the repository root understandable and intentional.
- Remove or redirect generated root-level clutter.
- Preserve configuration files that genuinely belong at the root.
- Preserve the supported Windows launcher and executable workflow unless it is
  retired through a separate product decision.
- Separate the immutable shipped exercise catalog from mutable user data.
- Ensure a packaged build can include only explicitly approved data files.
- Ensure a fresh installation starts with the exercise catalog and empty user
  state.
- Prevent ignored files, backups, or personal exports from entering a package.
- Add automated contracts so future schema or packaging changes cannot silently
  reintroduce the problem.
- Keep the privacy fix small enough to review independently from the larger
  runtime-path migration.
- Preserve existing user databases and recovery paths.

## 3. Non-goals

- Rewriting public Git history.
- Removing the Windows/PyInstaller distribution feature merely because it is
  old.
- Deleting normal root-level tool configuration.
- Moving the production runtime database in Packet A.
- Changing calculation behavior, API response contracts, or exercise catalog
  content.
- Treating `.gitignore` as a packaging or privacy boundary.
- Cleaning unrelated dirty files or active workstreams.

---

## 4. Current Evidence

### 4.1 Root artifacts already removed

The following ignored, untracked artifacts were removed from the working
directory during the initial cleanup:

- `_oldschema_check.db`
- `baseline_e2e.txt`
- `baseline_pytest.txt`
- `advmap-back-live.png`
- `advmap-live.png`
- `compare-all.png`
- `coverage-centered.png`
- `coverage-map-fixed.png`
- `preview1.png`
- `preview2.png`

They occupied approximately 29.6 MB, primarily from the 28.4 MB E2E baseline
log. Because every file was already ignored and untracked, this cleanup creates
no Git diff and requires no commit.

`MASTER_HANDOVER.local.md` remains at the root intentionally. It is ignored and
is the documented local handover/workstream record used by the repository's AI
workflow.

### 4.2 Root files that should normally remain

| Group | Files | Reason |
|---|---|---|
| Repository rules | `AGENTS.md`, `CLAUDE.md` | Automatically discovered operating guidance |
| Git/configuration | `.gitignore`, `.mcp.json` | Repository exclusions and project MCP configuration |
| Python checks | `pyproject.toml`, `pyrightconfig.json`, `pytest.ini` | Tool discovery from the project root |
| Node dependency metadata | `package.json`, `package-lock.json` | Canonical npm project files |
| Frontend checks | `.stylelintignore`, `.stylelintrc.json`, `tsconfig.json`, `vitest.config.js` | Stylelint, TypeScript, and Vitest configuration |
| E2E | `playwright.config.ts` | Playwright's canonical project configuration |
| User entry points | `README.md`, `QUICK_START.md`, `START.bat` | Root visibility is part of their usability |
| Distribution | `app_launcher.py`, `build_exe.bat`, `Hypertrophy-Toolbox.spec`, `RUN_APP.bat` | A coherent Windows/PyInstaller feature, still documented in `README.md` |

Some of these files can be consolidated or modernized later, but their
existence is not evidence that they are disposable.

### 4.3 Packaging is currently unsafe

Both packaging definitions recursively include the physical `data/` directory:

- `Hypertrophy-Toolbox.spec` uses `('data', 'data')`.
- `build_exe.bat` uses `--add-data "data;data"`.

PyInstaller reads the working directory, not the Git index. Consequently,
`.gitignore` provides no protection.

At audit time, a build from the main checkout would include at least:

- `data/auto_backup/` containing seven dated database snapshots, about 5.6 MB
  total.
- `data/.personal-export.json`, containing local user-state export data.
- `data/.personal_data_dance.py`, a local personal-data utility.
- `data/database.cleared-before-plan-icon-restore-20260613_175104.db`, an
  ignored historical database copy.
- `data/database.db`, whichever hidden working-copy version happens to be
  present.

The same class of defect is present outside `data/`. Packaging recursively
includes `static/`, while `static/bodymaps/GPT/` is ignored but physically
present. At audit time that directory contained 117 files (about 5.66 MB),
including scratch comparison pages, screenshots, third-party source, and a
nested `.git/` directory. It would be copied into the executable even though it
is absent from the parent repository's tracked file set.

No equivalent ignored content was found under `templates/` during this pass.
Nevertheless, every recursively packaged asset root has the same structural
risk.

The unrestricted filesystem inputs—not only the 70 tracked database rows—are
the highest-priority defect found by the root cleanup audit.

### 4.4 The tracked database has two incompatible roles

`data/database.db` currently acts as both:

1. The shipped exercise catalog used by catalog tests and distribution.
2. The default mutable runtime database for plans, logs, profiles, backups, and
   calibration state.

Those roles must be separated.

The path is covered by the existing `*.db` ignore rule, but it remains tracked
because it predates that rule. It is also marked `skip-worktree`:

```text
S data/database.db
```

This makes `git status` conceal working-copy differences.

### 4.5 Tracked versus local database state

The tracked `HEAD:data/database.db` contains exactly 70 rows in user-owned
tables:

| Table | Rows |
|---|---:|
| `user_selection` | 28 |
| `program_backups` | 5 |
| `program_backup_items` | 36 |
| `progression_goals` | 1 |
| **Total** | **70** |

The local working-copy database contains:

- 1,897 `exercises` rows.
- 1,598 `exercise_isolated_muscles` rows.
- Zero rows in every table listed in
  `utils.schema_registry.OWNED_TABLES_DROP_ORDER`.
- Zero user-owned entries in `sqlite_sequence`.
- `PRAGMA integrity_check = ok`.
- Zero `PRAGMA foreign_key_check` failures.
- No WAL, SHM, or journal sidecars at the time of inspection.
- One SQLite freelist page.

The two catalog tables are logically identical between the tracked and local
databases:

| Table | Rows in both | Hash of sorted logical rows |
|---|---:|---|
| `exercises` | 1,897 | `f95b78393c7f7d69…` |
| `exercise_isolated_muscles` | 1,598 | `a0c22b092553fdd1…` |

The local database is schema-newer. It contains five user-state tables missing
from the tracked file:

- `fatigue_context_settings`
- `learned_strength_calibrations`
- `user_calibration_settings`
- `ignored_calibration_transfers`
- `exercise_transfer_ratios`

This makes the local file the best available source for a clean seed, subject to
physical SQLite sanitization before commit.

### 4.6 Historical exposure decision

The historical database blobs were audited. No populated user profile, body
composition, secrets, or tokens were found. Historical workout-log content was
predominantly test/development residue, with only minimal scored UI-poking data.
The remaining exposure is limited to training-plan rows and ordinary weight
values.

**Standing decision:** do not rewrite public Git history.

The cost of coordinated force-pushing, invalidating clones and PR ancestry, and
losing provenance is disproportionate to the data found. This does not prevent
reconsidering history cleanup later if genuinely sensitive data is discovered.

### 4.7 Branch and baseline state is not fixed

During successive audits, the checkout moved through `db23801`, `cb5ff6e`,
`0cd44eb`, and then the post-merge handover branch at `a086915`. The reported
pytest baseline differed by one test between two of those revisions.

No implementation plan should hard-code either 1,752 or 1,753 as the expected
count. Record the starting commit and establish the baseline in the actual
implementation worktree.

At the latest 2026-07-25 review snapshot:

- PR #165 had merged successfully.
- `origin/main` was `95f30c1`.
- The primary checkout was on `docs/wp4-3i-post-merge-handover` at `a086915`,
  one commit ahead of `origin/main`, not on `main`.
- `CLAUDE.md` was modified.
- This plan was still untracked.
- The security fix from local commit `ce83690` was already present on
  `origin/main` as patch-equivalent PR #157 commit `3ce69dc`; the local commit
  itself was not an ancestor only because the change had been reapplied under a
  different SHA.

Earlier snapshots also contained active edits to `docs/MASTER_HANDOVER.md` and
`docs/REFACTOR_PLAN.md`, demonstrating why the preflight must discover rather
than assume the dirty-file set.

All unrelated changes present at implementation time must be preserved and
excluded from cleanup commits unless explicitly included by their owner.

---

## 5. Decisions

### D1. Keep legitimate root configuration

Do not move root configuration merely to reduce the file count. Moving it would
require wrapper commands or tool-specific path overrides and would make the
project less conventional.

### D2. Keep and repair executable packaging

The Windows/PyInstaller workflow remains documented and should not be removed
as a privacy workaround. Its inputs and reproducibility should be repaired.

### D3. Use a named immutable seed

The tracked catalog will become:

```text
data/catalog.seed.db
```

The mutable runtime file remains `data/database.db` during Packet A. Packet B
will decide its long-term location.

Because `*.db` is ignored, `.gitignore` must explicitly contain:

```gitignore
!data/catalog.seed.db
```

### D4. Package an allowlist, never a directory subtraction list

Packaging must enumerate the exact approved files. It must never include
`data/` recursively and must not attempt to exclude known-sensitive names from a
broad include.

The initial allowlist is:

- `data/catalog.seed.db`
- `data/free_exercise_db_mapping.csv`

`data/youtube_curated_top_n.csv` is intentionally excluded. Its only reader is
the development-side `scripts/apply_youtube_curated.py`; the packaged
application does not read it. The free-exercise mapping is required by the
production media fallback path.

`templates/` and `static/` are legitimate asset trees, but recursive inclusion
must still be constrained to reviewed project files.

Packet A takes the smaller immediate approach:

1. Explicitly exclude `static/bodymaps/GPT/` from the package.
2. Add a fail-closed pre-build guard that inventories ignored/untracked content
   under `static/` and `templates/`.
3. Allow only the exact, known, explicitly excluded GPT scratch root; fail on
   any new ignored/untracked path.
4. Verify the built asset tree and core media/UI smoke paths.

A guard that fails on every ignored path without recognizing the exact excluded
GPT root would make every build from the present checkout fail. Conversely, a
bare GPT exclusion without the general guard would allow the next ignored
directory to recreate the defect.

Packet A2 later replaces broad asset-tree collection with a staging directory
populated from an explicit tracked-file manifest. That is the stronger
long-term design, but separating it makes the asset-parity change independently
reviewable. **Shipped** — see §6.10; the GPT exclusion and the fail-closed
guard both became unnecessary once the manifest replaced the walk.

### D5. One canonical packaging definition

`Hypertrophy-Toolbox.spec` should become the single packaging source of truth.
`build_exe.bat` should invoke the committed spec rather than deleting it and
reconstructing a second configuration.

If that consolidation is not performed, both definitions must have equivalent
allowlist tests. Maintaining two independent packaging configurations is the
inferior fallback.

### D6. Split the implementation

- **Packet A0:** establish a pinned, clean, reproducible PyInstaller build
  environment without producing or distributing a package from sensitive
  checkout state.
- **Packet A:** privacy, seed separation, safe first-run bootstrap, `data/`
  allowlisting, the immediate static scratch exclusion/guard, and contracts.
- **Packet A2:** build `static/` and `templates/` from a tracked-file staging
  manifest, with an independently reviewed asset-parity diff.
- **Packet B:** external runtime-data directory and migration.
- **Packet C:** remaining root/tooling organization and distribution
  modernization.

Packet A does not depend on Packet B. Packet B must not be smuggled into the
privacy fix.

---

## 6. Packet A0, Packet A, and Packet A2

### 6.1 Packet A0 — Reproducible build prerequisite

Packet A cannot close on a packaged-app smoke unless the repository first
defines a clean build environment.

At review time:

- The `venv/` used by `build_exe.bat` did not exist.
- The local `.venv` did not contain PyInstaller.
- `requirements.txt` did not declare PyInstaller.
- `build_exe.bat` installed the latest PyInstaller without a version pin.
- The spec listed pandas and NumPy as hidden imports even though application
  code no longer imports either package.
- The local `.venv` happened to contain pandas and NumPy, but that incidental
  state is not part of a reproducible clean build.

Checklist:

- [x] Add `requirements-build.txt` with an exact PyInstaller version validated
      against the repository's supported Python version.
- [x] Make the build script install both runtime requirements and the pinned
      build requirements into its declared environment.
- [x] Decide whether the build environment remains `venv/` or becomes `.venv`;
      Packet A0 must resolve the inconsistency before Packet A relies on it.
- [x] Remove stale pandas/NumPy hidden imports from the canonical packaging
      definition after confirming no application import path requires them.
- [x] Keep genuine runtime/export dependencies such as XlsxWriter and openpyxl
      unless import analysis plus a packaged smoke proves otherwise.
- [x] Prove one clean build in a disposable, isolated worktree before changing
      the seed/bootstrap behavior.

#### Recorded A0 decisions

- **PyInstaller pinned to `6.21.0`** in `requirements-build.txt`. This machine
  runs Python 3.14.4; 6.15.0 is the earliest release offered for 3.14, and
  6.21.0 was the latest available at pin time. The first A0 probe ran with an
  unrecorded version and its environment was discarded, so the version could not
  be recovered — hence the explicit pin plus a re-proved build.
- **The build environment stays `venv/`, deliberately separate from `.venv`.**
  `.venv` has accumulated packages `requirements.txt` never declares — pandas
  3.0.3 and numpy 2.4.4 — which is precisely how the stale hidden imports
  appeared to work. Building from it would make the artifact depend on
  undeclared developer state. `venv/` is already gitignored.
- **Observed, not fixed here:** `requirements.txt` mixes runtime and test
  dependencies (`pytest`, `pytest-playwright`, `playwright`, `vulture`), so the
  build environment installs test tooling it never needs. Splitting them is
  Packet C's "decide whether PyInstaller belongs in a development requirements
  file" item; A0 deliberately does not change the runtime dependency set.
- **Dependency install is now unconditional.** The previous "install only if
  `flask` is missing" guard meant an environment created before a requirements
  change kept building against the stale set. pip is a no-op when satisfied.
- **`pandas` / `numpy` hidden imports removed** from both the spec and
  `build_exe.bat`. Neither is imported by `app.py`, `app_launcher.py`,
  `routes/`, or `utils/` — the exporters moved to XlsxWriter directly, and the
  only surviving mentions are comments recording that migration. Neither is in
  `requirements.txt`, so declaring them only produced resolution errors.
- **`xlsxwriter` stays declared.** It is imported lazily inside functions
  (`utils/export_utils.py`), so PyInstaller's static analysis will not find it.
  `openpyxl` is a module-level import in `utils/volume_splitter_service.py` and
  is kept as belt-and-braces.

#### A0 re-probe result (2026-07-25)

Built from a disposable `-Seed empty` worktree at commit `1155c06`, asserted
clean of `data/database.db`, `data/auto_backup/` content, `.personal-*`, and
`static/bodymaps/GPT/` before building.

- `pyinstaller==6.21.0` resolved and installed; build exit code 0.
- **Zero pandas/NumPy diagnostics** — the nonfatal build errors the first probe
  reported are gone, confirming those hidden imports were the cause.
- Distribution is 81 MB. `_internal/data/` contained **only**
  `free_exercise_db_mapping.csv` and `youtube_curated_top_n.csv`. No
  `auto_backup`, no `.personal-*`, no nested `.git`, no `static/bodymaps/GPT/`.
- **`_internal/data/` contained no database at all.** Built from a clean
  checkout the packaged app ships zero exercises, because the only catalog
  source is the builder's own working-copy `data/database.db`. This is the
  mirror image of the privacy defect and is independent confirmation that the
  seed plus first-run bootstrap (decision 4A) is required, not merely tidier.
- `youtube_curated_top_n.csv` is packaged today, confirming the allowlist need.

Consolidating `build_exe.bat` onto the committed spec (D5) stays in Packet A;
A0 changes only the dependency contract and the stale hidden imports, so the
two definitions still drift until §6.6 lands.

The preflight build must not use the present main-checkout `data/` directory.
Create a disposable worktree with `-Seed empty`, confirm it contains none of the
ignored personal or GPT scratch paths, and do not publish its artifact. This
proves the toolchain without creating a package from the tracked user-state
database or local ignored files.

The current worktree helper's `-Seed empty` mode explicitly removes the tracked
`data/database.db` that `git worktree add` initially checks out. Before the
preflight build, assert that the target worktree actually has no
`data/database.db`, `data/auto_backup/` contents, `.personal-*` files, or GPT
scratch tree. This protects against regression to the older behavior where
"empty" could accidentally leave the tracked 70-row database in place.

Packet A still performs a final build after the packaging changes. Packet A0
proves that a failure at that later gate is caused by the patch rather than by
an undefined build environment.

### 6.2 Packet A preflight

#### Packet A execution record (2026-07-25)

The implementation worktree was created with
`scripts/new-worktree.ps1 -Task rootdircleanup-packet-a -Seed copy-current`
from refreshed `origin/main` at `8dba5b226277909d8a13cb36679274dffdd89257`.
The copied source database had file SHA-256
`7585cd4d36be20d523e484298afd48d2950e68f4c8ad87e2e97b5456fe8707b6`;
its catalog counts, logical hashes, zero owned-table counts, integrity, and
foreign-key checks matched §4.5. A recoverable copy was preserved outside the
implementation and package paths. The pre-change targeted baseline was
**46 passed**, and the full baseline was **1,753 passed**.

- [x] Stop the Flask server and any process that may have the database open.
- [x] Confirm `data/database.db-wal`, `-shm`, and `-journal` do not exist.
- [x] Record the implementation worktree's starting commit.
- [x] Record the pre-change targeted and full pytest baseline at that commit.
- [x] Record SHA-256 hashes and row counts for the source local database.
- [x] Confirm all catalog hashes and user-table counts listed in Section 4.5.
- [x] Preserve a recoverable copy of the source database outside the paths that
      will be renamed or packaged.
- [x] Confirm unrelated dirty files and active workstream ownership before
      editing shared paths.
- [x] Confirm PR #165 merged; `origin/main` was `95f30c1` at the
      2026-07-25 review.
- [x] Fetch `origin` again immediately before execution and record the exact
      `origin/main` SHA selected as the Packet A base.
- [x] Start Packet A from that refreshed `origin/main`; do not inherit the
      current handover branch by accident.
- [x] Settle, update, or retire worktrees that retain `skip-worktree` state for
      `data/database.db` before landing the untracking change.

#### Base-branch and live-worktree warning

At the final 2026-07-25 review:

- PR #165 was merged into `origin/main` at `95f30c1`.
- The primary checkout had moved to `docs/wp4-3i-post-merge-handover` at
  `a086915`, one commit ahead of `origin/main`, and was still not a valid Packet
  A base.
- `scripts/new-worktree.ps1` created new branches from the caller's `HEAD`, not
  from an independently selected base ref.
- Two other live worktrees existed:
  `wt/css-wp4-3i-filter-btn` at `cb5ff6e` and
  `fix/security-audit-setuptools-83` at `ce83690`.

Therefore, do not run the worktree helper from the handover checkout for Packet
A. Create the Packet A worktree explicitly from the refreshed `origin/main`, or
first place the invoking checkout at that exact commit. Record the resulting
base SHA in the handover.

The filter-button worktree commit is already an ancestor of `origin/main`. The
security worktree's commit is not an ancestor, but `git cherry` marks it
patch-equivalent to the security fix already shipped by PR #157. Both worktrees
were clean at review time and their code changes are redundant, so both are
retirable after one final clean-status and runtime-data check.

They may keep an untracked `data/database.db` after Packet A removes the path
from the index. That data should not be deleted blindly. Inspect or preserve any
needed runtime state before removing the worktree directories.

#### Worktree warning

`scripts/new-worktree.ps1` defaults to `-Seed visual`. That mode replaces
`data/database.db` with the E2E visual fixture and is wrong for preparing the
production catalog seed.

If Packet A is implemented in a worktree:

- Use `-Seed copy-current`, not the default.
- Confirm the copied database hashes and zero user counts again.
- Remember that the script marks the database `skip-worktree` in the new
  worktree.
- Run `git update-index --no-skip-worktree data/database.db` in the
  implementation worktree before the intentional rename.
- Never assume a clean `git status` proves the database matches the index.

### 6.3 Create the canonical seed

- [x] Remove the `skip-worktree` flag deliberately.
- [x] Create `data/catalog.seed.db` from the validated local catalog.
- [x] Ensure the tracked `data/database.db` entry is removed.
- [x] Add `!data/catalog.seed.db` to `.gitignore` after the broad `*.db` rule,
      beside the existing `!e2e/fixtures/database.visual.seed.db` exception.
- [x] Prove the exception is effective: the seed is visible to Git, stages
      normally, and appears in a fresh-clone/file-list check.
- [x] Physically sanitize the seed using a clean SQLite backup/rebuild followed
      by `VACUUM`, rather than relying only on `DELETE`.
- [x] Confirm `PRAGMA freelist_count = 0` after finalization.
- [x] Confirm `sqlite_sequence` contains no user-owned sequence state.
- [x] Confirm no WAL/SHM/journal sidecars are staged or packaged.
- [x] Confirm only the two catalog tables contain rows.
- [x] Confirm all current schema tables exist.
- [x] Confirm the logical catalog hashes remain unchanged.
- [x] Confirm `PRAGMA integrity_check = ok`.
- [x] Confirm `PRAGMA foreign_key_check` returns zero rows.
- [x] Confirm ordinary app startup never writes to `catalog.seed.db`.

The seed should be treated as an immutable application asset. Runtime code may
copy from it but must never connect to it in writable mode.

### 6.4 Add first-run bootstrap

**Invocation-site invariant:** call the bootstrap utility directly from
`app.py`, immediately above the existing `run_all_initializers()` startup call.
Never call it from `run_all_initializers()`, `DatabaseHandler`, `utils.config`
import side effects, or any shared schema/connection helper.

This is required by owner decision 4A. The test suite points `DB_FILE` at fresh
temporary paths and calls `run_all_initializers(force_base=True)` to create
empty, isolated schemas. Putting seed bootstrap inside that shared initializer
would inject 1,897 exercises into roughly the entire pytest suite and change the
meaning of its fixtures.

Before `run_all_initializers()`:

1. Resolve the seed asset path in both source and PyInstaller-frozen execution.
2. Resolve `DB_FILE`.
3. If `DB_FILE` already exists, do not replace it.
4. If it does not exist and the seed exists, copy the seed atomically to
   `DB_FILE`.
5. Run the normal idempotent initializers against the runtime copy.

Checklist:

- [x] Put bootstrap logic in a testable utility rather than embedding a large
      block directly in `app.py`.
- [x] Invoke that utility only from real `app.py` startup immediately before
      `run_all_initializers()`.
- [x] Add regression tests proving `run_all_initializers()`,
      `DatabaseHandler`, and `utils.config` do not bootstrap the seed on their
      own.
- [x] Create the target parent directory safely.
- [x] Copy through a temporary sibling file and atomically rename it, preventing
      a partial database if startup is interrupted.
- [x] Handle two simultaneous first launches without corrupting or overwriting a
      completed target.
- [x] Never overwrite an existing database, including an old-schema or corrupt
      one; existing recovery/migration behavior remains authoritative.
- [x] Preserve the `DB_FILE` environment override.
- [x] Decide and document that an explicitly configured but missing `DB_FILE`
      receives the seed. This is the recommended behavior because it matches a
      real fresh installation at any selected path.
- [x] Ensure normal isolated pytest fixtures that intentionally create empty
      databases remain empty unless they explicitly exercise application
      bootstrap.
- [x] Update `.claude/rules/database.md`, which currently states that there is
      no built-in seed.

**First-run backup decision:** the pristine seed copy is not immediately
snapshotted. It is already identical to the immutable packaged recovery asset,
so `app.py` skips `create_startup_backup()` only on the process that wins
first-run publication. Normal later startups retain the existing rolling
backup behavior.

### 6.5 Preserve both first-install and empty-schema coverage

The existing deep-gate cold-start job proves that initializers can create a
database when the target is missing. Repurposing it solely to copy the seed
would lose the true empty-schema test.

Maintain two distinct contracts:

1. **First-install test:** missing runtime DB + available seed results in a
   successful boot, exactly 1,897 exercises, and zero user rows.
2. **Empty-schema initializer test:** with seed bootstrap deliberately bypassed
   in the test harness, initializers can still create a valid empty schema and
   serve the application.

Checklist:

- [x] Reword the deep-gate job so its name matches what it proves.
- [x] Assert `GET /` returns 200.
- [x] Assert the first-install database contains the expected catalog.
- [x] Assert every user-owned table is empty.
- [x] Preserve a separate missing/empty database initializer test.
- [x] Keep the old-schema migration job unchanged except for path terminology.

### 6.6 Consolidate and restrict packaging

- [x] Change the spec from `('data', 'data')` to explicit file entries.
- [x] Include only `data/catalog.seed.db` and
      `data/free_exercise_db_mapping.csv` from `data/`.
- [x] Do not package `data/youtube_curated_top_n.csv`; it is a developer-side
      catalog-application input, not a runtime dependency.
- [x] Make `build_exe.bat` invoke `Hypertrophy-Toolbox.spec`.
- [x] Stop deleting the committed spec during builds.
- [x] Confirm the destination paths match bootstrap's frozen asset lookup.
- [x] Exclude `static/bodymaps/GPT/` and its nested `.git/` content from the
      build.
- [x] Add a fail-closed pre-build guard that inventories ignored/untracked
      content under `static/` and `templates/`.
- [x] Permit only the exact `static/bodymaps/GPT/` root that the spec explicitly
      excludes; fail on every other ignored/untracked path.
- [x] Test the guard with a synthetic unexpected ignored/untracked asset so it
      is proven fail-closed.
- [x] Verify intended tracked vendor assets, licenses, templates, JavaScript,
      CSS, images, and fonts remain present after tightening asset collection.
- [x] Confirm `RUN_APP.bat` is still copied into the distribution.

Repair the E2E fallback without weakening the live-data guard:

- [x] Change `e2e/scripts/prepare_visual_db.py::DEFAULT_SOURCE` to fall back to
      `data/catalog.seed.db`, not the now-untracked `data/database.db`, when the
      visual fixture is missing.
- [x] Keep `LIVE_DB = data/database.db` and the `data/auto_backup/` output guard
      unchanged; those still identify paths a seeder must never overwrite.
- [x] Confirm `prepare_e2e_db.py` continues to prefer the tracked visual fixture
      and wipe its own throwaway user state.

### 6.7 Add privacy and packaging contracts

Use `utils.schema_registry.OWNED_TABLES_DROP_ORDER` as the canonical user-table
registry.

For every registered table, tests must:

- [x] Assert the table exists in the seed.
- [x] Assert its row count is zero.

The existence assertion matters: silently skipping a missing table would allow
a stale seed to pass.

Add a schema-registry completeness check:

- [x] Enumerate all non-internal tables in the seed.
- [x] Treat `exercises` and `exercise_isolated_muscles` as catalog tables.
- [x] Assert every other application table is represented in
      `OWNED_TABLES_DROP_ORDER`.

This catches the case where a developer creates a new user table but forgets to
add it to the registry; testing only the tuple cannot detect its own omissions.

Additional contracts:

- [x] Assert catalog row counts and stable logical-row hashes.
- [x] Assert SQLite integrity and foreign-key integrity.
- [x] Assert `catalog_db_path` copies `data/catalog.seed.db`, never the runtime
      database.
- [x] Assert the spec contains no recursive `data/` source.
- [x] Assert the spec's approved data source set exactly matches the allowlist.
- [x] If the batch file remains a second packaging definition, assert its
      approved data set too.
- [x] Build the executable and inspect the actual `dist/` tree; source-text tests
      are not sufficient.
- [x] Assert the distribution contains none of:
      `auto_backup`, `.personal-*`, additional `.db` files, SQLite sidecars, or
      unapproved files from `data/`.
- [x] Assert the distribution contains no `static/bodymaps/GPT/`, nested `.git`
      directories, or other ignored/untracked source-tree files.
- [x] Check a reviewed Packet A set of required static/template assets and smoke
      their production paths so the GPT exclusion cannot silently remove
      required UI assets.
- [x] Open the shipped seed from the built distribution read-only and rerun the
      privacy contract against that exact artifact.

### 6.8 Packet A verification gate

Recorded Packet A results: focused pytest **65 passed**; full pytest
**1,772 passed** (**1,753** baseline plus 19 Packet A contracts); Chromium
navigation/API smoke **67 passed**; real pinned PyInstaller build exit 0.
The built data allowlist contained exactly two files. Its shipped seed SHA-256
was `678c9641fc280afba98cb1c5b52979e0391200c891f540c476002b895cd22d1f`
and passed the read-only privacy contract. A clean-copy executable smoke
returned HTTP 200, exposed 1,897 exercises, returned 225 Barbell-filtered
results, created the runtime DB, left the seed unchanged, and created no
redundant first-run backup.

- [x] Targeted seed/privacy tests pass.
- [x] Catalog invariant and volume taxonomy tests pass.
- [x] Harness isolation tests pass.
- [x] Config/bootstrap tests pass.
- [x] Old-database migration tests pass.
- [x] Full pytest matches the baseline established at the packet's actual
      starting commit.
- [x] Relevant Playwright smoke tests pass against a throwaway runtime DB.
- [x] `build_exe.bat` completes successfully.
- [x] The packaged application boots from a clean extracted directory.
- [x] First packaged launch creates a runtime copy and leaves the packaged seed
      unchanged.
- [x] The packaged app serves the main page and exercise filters return catalog
      data.
- [x] The final `git diff` contains only intentional Packet A files.
- [x] `git status` is also checked with ignored and index-flag awareness.

### 6.9 Packet A expected file scope

Exact implementation may vary, but reviewers should expect changes around:

- `.gitignore`
- `requirements-build.txt`
- `data/database.db` removal
- `data/catalog.seed.db` addition
- `app.py`
- A small seed/bootstrap utility under `utils/`
- `tests/conftest.py`
- New seed/privacy/packaging/bootstrap tests
- A package-input guard under `scripts/`
- `e2e/scripts/prepare_visual_db.py`
- Directly affected `e2e/scripts/**` tests
- `Hypertrophy-Toolbox.spec`
- `build_exe.bat`
- `.github/workflows/deep-gate.yml`
- `.claude/rules/database.md`
- Any directly affected packaging documentation

Unexpected business-logic, route, template, or calculation changes are a scope
warning.

### 6.10 Packet A2 — Tracked-asset staging manifest

Packet A2 replaces Packet A's broad `static/` and `templates/` inputs with a
staging tree created from an explicit tracked-file manifest.

- [x] Generate the manifest deterministically from the intended repository
      assets.
- [x] Do not depend on ignored/untracked working-copy content.
- [x] Preserve executable-bit/path/case behavior needed by the supported
      platforms.
- [x] Compare the staged tree with the tracked source set before building.
- [x] Review a complete asset-parity diff, including vendor licenses and media.
- [x] Run page, CSS, JavaScript, favicon, body-map, and exercise-media packaged
      smoke tests.
- [x] Confirm the final distribution contains no nested repository metadata.
- [x] Remove Packet A's temporary broad-tree guard only when the staging
      manifest makes it redundant and equivalent fail-closed tests exist.

Packet A2 is not required to land Packet A. Keeping it separate reduces the risk
that privacy remediation silently drops required vendor assets.

#### Implemented design

`scripts/stage_package_assets.py` owns the manifest. `git ls-files -- static
templates` is the only source of truth, so the manifest is deterministic,
sorted, and structurally incapable of naming ignored or untracked content. The
script mirrors the manifest into `build/package-assets/` — gitignored build
output — with `shutil.copy2`, which carries mode bits and mtimes, then verifies
the staged tree against the manifest and against the tracked sources' sizes and
executable bits before returning. Stale files left by a previous manifest are
pruned, so a removed asset cannot survive in a distribution.

`Hypertrophy-Toolbox.spec` calls `staged_datas(REPO_ROOT)` and passes the result
straight to `Analysis(datas=...)`; the filesystem walk and its
`excluded_subtree='bodymaps/GPT/'` subtraction are gone. Staging therefore runs
inside the canonical packaging definition, which also covers a direct
`pyinstaller Hypertrophy-Toolbox.spec` invocation. `build_exe.bat` runs the same
script once before the build so a broken manifest fails in seconds rather than
after a full build; it must run *after* the `rmdir /s /q build` clean, and the
spec's own call is what survives, because PyInstaller's `--clean` wipes the work
path before executing the spec.

Fail-closed conditions: a manifest that is empty (built outside a git checkout),
a tracked asset missing from the working copy, a path whose segments include
`.git`, paths differing only by case, a staged tree with missing or unexpected
files, staged content whose size or executable bit diverges from the source, and
a `--staging-root` that contains a checkout — pruning would delete it.

Packet A's `scripts/guard_package_assets.py` and its test are removed. The guard
existed to detect ignored/untracked files that a recursive walk would collect;
with the manifest there is no walk to protect, and
`tests/test_package_asset_staging.py` proves the exclusion directly by staging a
synthetic repository containing an ignored `static/bodymaps/GPT/` root (with a
nested `.git/`), an ignored `*.tmp` file, and an untracked template.

#### Asset-parity diff

The Packet A collector (filesystem walk minus the GPT root) and the Packet A2
manifest were compared file by file in the implementation worktree:
**997 files on both sides, zero added, zero dropped.** Per category, both sides
carry 18 templates, 19 CSS files, 64 JavaScript files, 883 images, 6 vendor
license/notice/version files, and 883 vendor assets. Neither side carries a font
file — the repository tracks none, so the manifest cannot ship one; a future
font would be staged automatically because the manifest is not extension-filtered.

Run against the primary checkout, which does hold the ignored scratch tree, the
same comparison shows the mechanism working: an unfiltered walk of `static/` and
`templates/` finds **1,114** files, the manifest yields **997**, and the
**117**-file difference is exactly the ignored `static/bodymaps/GPT/` content,
including its nested `.git`. Under Packet A that exclusion depended on one
hard-coded subtree name; under Packet A2 it is a property of the manifest.

Dev-only tracked files (`CLAUDE.md` orientation notes, `static/js/modules/
__tests__/`, the Bootstrap source map, the vendored `.swift` path sources) stay
packaged, exactly as under Packet A. Shrinking the shipped set is a content
decision, not a safety one; keeping parity exact is what makes this diff
reviewable. Packet C can revisit it.

#### Recorded Packet A2 results

Baseline at the packet's starting commit `22350ec`: full pytest **1,772
passed**. After the change: full pytest **1,785 passed, 1 skipped** — the 15
staging contracts replace the guard's 3, plus one new spec contract, and the
skip is the POSIX-only executable-bit test that cannot assert on Windows.
Focused packaging pytest (staging, packaging contract, seed, bootstrap, harness
isolation) **35 passed / 1 skipped**. Chromium navigation + API smoke **67
passed** against the worktree's throwaway visual-seed database.

`build_exe.bat` completed with exit code 0 on pinned PyInstaller 6.21.0. The
staging step reported 979 `static/` and 18 `templates/` files. The built
`dist/Hypertrophy-Toolbox/_internal/` tree contains **exactly the 997 manifest
files** under `static/` and `templates/`, exactly two files under `data/`
(`catalog.seed.db`, `free_exercise_db_mapping.csv`), no `.git` directory
anywhere, no `auto_backup`, no `.personal-*`, no SQLite sidecars, and no second
`.db`. The shipped seed's SHA-256 is unchanged at
`678c9641fc280afba98cb1c5b52979e0391200c891f540c476002b895cd22d1f`.

The packaged smoke ran from a clean copy of the distribution and passed all 28
checks: the six main pages, `base.css`, the Bootstrap bundle, `app.js`,
`fetch-wrapper.js`, the favicon, the advanced body-map SVG, a MuscleMap vendor
path source, `exercises.json`, the free-exercise-db `LICENSE`, and a real
exercise-media JPEG all returned 200 with correct content types;
`/get_all_exercises` returned **1,897** rows and `/filter_exercises` returned
**225** Barbell rows; first run created the runtime database, left the packaged
seed byte-identical, and wrote no redundant first-run backup.

> **Environment note.** Windows Smart App Control is enforced on the build
> machine and refuses to launch the freshly built, unsigned PyInstaller
> bootloader (`WinError 4551`), so the runtime half of the smoke booted the
> packaged payload with the pinned build interpreter over the distribution's own
> `_internal/` tree — the same packaged templates, static assets, catalog seed,
> and compiled application modules, minus the bootloader. Every static
> distribution check ran against the real build output. This is a machine
> policy, not a packaging regression: nothing in Packet A2 touches the
> bootloader, and code signing is a distribution question for Packet C.

`scripts/new-worktree.ps1` needed a one-line repair to run this packet at all.
Packet A untracked `data/database.db`, after which
`git ls-files --error-unmatch data/database.db` wrote to stderr, and
`$ErrorActionPreference = "Stop"` turned that into a terminating error — the
script created the worktree and then aborted before seeding it. It now tests
`git ls-files -- data/database.db` for output instead, which stays silent for an
untracked path.

### 6.11 Packet A3 — Staging integrity and real frozen validation

Packet A2 proved the staged tree is *the tracked set* — the right file names,
sizes, and executable bits. It does not prove the staged bytes are the tracked
bytes.

Two gaps remain:

1. `_needs_copy()` decides on size plus integer mtime, and
   `verify_staging_tree()` compares only size and the executable bit. A staged
   file mutated in place to the same length, with its mtime restored, is
   neither recopied nor rejected. That is exactly the shape of an edit made by
   a tool that preserves timestamps, of a partially written copy that happens
   to land on the same length, and of deliberate tampering with a build
   directory.
2. Nothing records what was staged. After a build there is no artifact a
   reviewer can re-verify the distribution against.

Packet A3 closes both and is deliberately small: it changes no packaging
inputs, no allowlist, and no application behavior.

- [x] Compare staged content by SHA-256, not by size and mtime.
- [x] Keep a size fast path so the common case does not hash twice for nothing;
      equal sizes must fall through to the digest.
- [x] Make a content mismatch self-healing in `sync_staging_tree()` (restage)
      and fatal in `verify_staging_tree()` (fail closed). A stale staging tree
      must not be able to poison every later build.
- [x] Emit `manifest.sha256` in standard `sha256sum` format beside the staging
      root, so `sha256sum -c` and any reviewer can re-verify independently.
- [x] Write it beside the staging root, never inside it: the staging tree must
      keep matching the manifest exactly, and an extra file inside would be
      rejected as unexpected.
- [x] Add the mutation regression test: stage, rewrite a staged file with
      equal-length content, restore its mtime exactly, and assert both that
      restaging repairs it and that verification rejects it.

**Line endings are part of the contract.** Writing the record through Windows
text mode produced CRLF, and `sha256sum -c` then looked for paths with a
trailing carriage return and failed on all 997. The writer pins `newline="\n"`
and a test asserts the bytes contain no `\r` — found only because the record was
checked with the external tool it claims compatibility with, not just with the
reader that wrote it.

**Hashing cost is accepted.** The tracked asset tree is about 61 MB. Staging
reads it roughly three times per build (copy decision, copy, verification)
instead of once. That is seconds against a multi-minute PyInstaller build, and
the verification pass deliberately recomputes rather than trusting digests
cached by the copy decision — otherwise the proof and the thing it proves share
a failure mode.

#### Real frozen validation

**Correction — the Packet A2 environment note no longer reproduces.** It
recorded that Smart App Control refuses to launch the freshly built, unsigned
bootloader (`WinError 4551`), so the local smoke ran the packaged payload
instead. Re-measured on 2026-07-26 against a real `build_exe.bat` build:

- Smart App Control is still in **enforcement** mode
  (`VerifiedAndReputablePolicyState = 1`).
- `dist/Hypertrophy-Toolbox/Hypertrophy-Toolbox.exe` nonetheless launched and
  passed the full packaged smoke — 22 checks including six pages, ten assets,
  1,897 exercises, 225 Barbell matches, and an unmodified seed — **three runs
  out of three**.

So the block was conditional on something that has since changed, not on the
policy being on. The payload fallback is kept, and everything below still
holds: local success now is not a gate, because it depends on a machine state
this project does not control and cannot assert.

Standing decisions:

- **Smart App Control is never disabled.** Weakening host security to make a
  build gate pass inverts the trade. Windows Sandbox may be used only if it is
  already available without changing host security settings. That this became
  unnecessary is luck, not vindication.
- **Payload mode stays, and stays labelled** as not exercising the bootloader —
  in the script's `--mode` help, in its output, and here. It is the fallback
  for the next machine that does get blocked. A passing payload run is not
  evidence that the executable starts.
- **CI owns the real gate.** A `windows-latest` deep-gate job builds with
  pinned PyInstaller and launches the real
  `dist/Hypertrophy-Toolbox/Hypertrophy-Toolbox.exe`. This is what makes
  bootloader validation machine-independent and repeatable, which one
  developer's host policy never was in either direction.

- [x] Add a `windows-latest` deep-gate job that builds via the canonical spec.
- [x] Launch the real `.exe`, not the payload, and assert it serves the app.
- [x] Assert the packaged data allowlist and absence of ignored content in the
      built tree.
- [x] Verify the built assets against `manifest.sha256`.
- [x] Label the local payload smoke explicitly in code and documentation.

The smoke itself is now committed as `scripts/smoke_packaged_app.py` rather than
reconstructed by hand each packet, which is what let A2's environment note go
unchallenged for a day. Static checks run against the untouched build output;
the server runs from a throwaway copy, so first-run writes never dirty `dist/`.

`frozen-windows` lives in the manual deep gate beside the other packaged and
cold-start smokes, so it does not add ten minutes to every PR. Promoting it to a
required PR check is an owner decision: it needs a branch-protection change, and
required-check names are exact-match.

#### Recorded A3 results

Base `origin/main` `906b2fe` (plan-doc merge), itself on the `631f61a` verified
starting point. pytest baseline **1,785 passed / 1 skipped**; after the change
**1,792 passed / 1 skipped** — the seven new staging contracts.

A real `build_exe.bat` build completed (exit 0, pinned PyInstaller 6.21.0) and
regenerated both the staging tree and `build/manifest.sha256` after
`--clean` wiped `build/`. Against that distribution:

- Static inspection passed all eight checks, including **997 packaged assets
  matching `manifest.sha256`** and the two-file `data/` allowlist.
- `sha256sum -c` verified all 997 staged files independently.
- The **real bootloader** passed the full 22-check runtime smoke, three runs out
  of three, and payload mode passed once for comparison.

---

## 7. Packet B — Runtime Data Outside Immutable Application Assets

Packet B is the preferred long-term design but is intentionally separate
because it changes path semantics across the application, tests, scripts,
worktrees, logs, backups, and installed builds.

### 7.1 Required product decisions — owner-approved 2026-07-26

All five were accepted as proposed. They are recorded here as the authoritative
statement; the checklist in §12 tracks their closure.

- [x] **B-D1. One centralized runtime-path policy.** A single resolver owns
      every runtime path — database, backups, logs, recovery files — and
      applies one documented precedence order (§7.2). No module derives a
      runtime path from `__file__`, and nothing creates runtime directories as
      an import side effect.
- [x] **B-D2. Source stays repository-local; only frozen builds use OS
      user-data paths.** A checkout or worktree keeps `<repo>/data/database.db`.
      Worktree isolation is a property of the resolver, not of a launcher flag
      that a developer can forget. Pointing parallel worktrees at one OS-level
      SQLite file is precisely the WAL-corruption failure
      `scripts/new-worktree.ps1` exists to prevent.
- [x] **B-D3. Verified, non-destructive frozen-install migration.** The legacy
      database is copied through the SQLite backup API, verified, and left in
      place. It is never deleted, never moved, and never written to. An
      existing runtime database is never replaced. Migration that cannot be
      verified fails loudly with recovery instructions rather than falling
      through to a clean seed.
- [x] **B-D4. Logs relocate; legacy backups are copied once, best-effort; old
      logs do not migrate.** Logging must not require write access to the
      installation directory. Historical log files carry no user value and are
      left where they are. Backup copying is best-effort by design: a failure
      to copy old snapshots must never block startup, because the originals
      still exist.
- [x] **B-D5. Versioned, additive/update-only catalog upgrades.** Catalog
      content is versioned independently of the schema. A newer shipped catalog
      inserts new exercises and updates catalog-owned columns of existing ones.
      It never deletes or renames a catalog exercise automatically, and never
      cascades into user-owned rows.

Two consequences follow and are approved with them:

- **Portable installs are supported through the resolver**, not as a separate
  mode: an explicit runtime-root override (§7.2) is the documented mechanism.
- **`utils/database.py::DATA_DIR` is removed.** It is dead — recomputed from
  `DB_FILE` at import and read by nothing — and leaving a second, staler
  notion of "the data directory" beside a centralized resolver is exactly the
  drift B-D1 exists to prevent.

### 7.2 Approved path policy and precedence

The resolver answers one question — *where does mutable runtime state live* —
and everything else derives from its answer. Precedence, highest first:

1. **`DB_FILE`** — explicit, absolute authority over the database path. It is
   never migrated into, never overridden, and never inferred from. Tests and
   CI depend on this.
2. **An explicit runtime-root override** — relocates the whole runtime tree
   (database, backups, logs) in one move. This is the supported answer for
   portable/USB installs and for a launcher that wants a per-worktree root.
3. **Frozen build** — a per-user OS application-data directory:
   `%LOCALAPPDATA%` on Windows, `~/Library/Application Support` on macOS,
   `$XDG_DATA_HOME` (falling back to `~/.local/share`) on Linux. Local rather
   than roaming on Windows: a SQLite database should not be synchronized
   between machines by a roaming profile.
4. **Source checkout or worktree** — `<repo>/data`, exactly as today.

For frozen releases:

- Immutable assets, including `catalog.seed.db`, remain inside the application
  bundle.
- Mutable database, backups, logs, and recovery files live in a per-user
  writable application-data directory.

For source checkouts and worktrees:

- Do not let every checkout silently share one OS-level database.
- Either retain a worktree-local ignored runtime path or have the worktree
  launcher set a unique `DB_FILE`.
- Never point parallel worktrees at the same SQLite file.

This distinction is necessary. Moving the default to one global user-data path
without updating the worktree model would reintroduce the database-sharing and
WAL corruption risk that `scripts/new-worktree.ps1` was created to prevent.

### 7.2.1 Packet B sequencing — owner-required correction

Splitting Packet B into reviewable pieces creates one state that must never
exist, even transiently on `main`:

> The frozen application resolves its database to the **new** runtime path
> while legacy migration is **not yet active**.

A user upgrading into that state gets a freshly seeded, empty database while
their real data sits untouched at the old path. It is recoverable, but it
presents data loss to the user and is indistinguishable from it in the moment.

Therefore:

- **B1** introduces and tests the resolver, removes import-time directory
  creation, and relocates logging. It **must not** switch the frozen database
  path. The resolver may compute the frozen runtime path; nothing may use it
  for `DB_FILE` yet. **Shipped** — see §7.6.
- **B2** activates the frozen `DB_FILE` switch **atomically with** legacy
  migration and backup copying — one PR, or not at all. **Shipped** — see §7.7.
- **B3** adds catalog versioning and additive upgrade behavior. **Shipped** —
  see §7.8.

### 7.3 Migration precedence

The migration must be idempotent and follow an explicit precedence:

1. An explicit `DB_FILE` override wins; do not migrate unrelated default paths
   into it without an explicit migration command.
2. If the new runtime database already exists, use it and change nothing.
3. If the new database is absent and a legacy runtime database exists, create a
   verified backup and migrate the legacy database once.
4. If neither exists, bootstrap from `catalog.seed.db`.
5. Never replace a non-empty runtime database with the seed.

Checklist:

- [x] Use the SQLite backup API or an equivalent consistent copy for a live
      database.
- [x] Refuse migration while unresolved WAL/SHM state exists unless SQLite
      performs the copy through a live connection.
- [x] Record migration completion without putting sensitive paths or row data in
      logs.
- [x] Provide a clear recovery message if migration fails.
- [x] Verify old-schema migration after relocation.
- [x] Test paths containing spaces and non-ASCII characters.
- [x] Test read-only installation directories.
- [x] Test upgrade/reinstall over an existing user-data directory.

Non-destructiveness is absolute (B-D3):

- [x] Never delete, move, truncate, or write to the legacy database.
- [x] Never replace an existing runtime database, whatever its schema or state.
- [x] Verify the migrated copy before it is published as the runtime database —
      a copy that cannot be verified is not a migration.
- [x] On any failure, leave the legacy database authoritative and report
      recovery steps. Never seed a clean database after finding legacy data and
      never present that as success.

**Publication order matters.** Copy to a temporary file in the destination
directory, verify that copy, and only then publish it to the runtime path
atomically. Verifying after publication leaves a window in which a half-copied
database is already the live one.

### 7.3.1 Logs and backups (B-D4)

- [x] Logs are written under the resolved runtime root, never the installation
      directory.
- [x] `utils/logger.py` stops creating directories at import time; the resolver
      owns creation.
- [x] Existing log files are not migrated. They are development history, not
      user data.
- [x] Legacy `data/auto_backup/` snapshots are copied once into the new runtime
      root, best-effort.
- [x] A backup-copy failure is logged and startup continues. The originals are
      untouched, so a failure costs nothing; blocking startup over it would.
- [x] Backup rotation, `create_startup_backup()`, and erase-data recovery all
      target the resolved runtime root.

### 7.4 Catalog updates after first install (B-D5)

A seed only initializes new users. It does not automatically update the catalog
inside an existing runtime database, so fresh installs and upgraded installs
silently diverge until this exists.

The approved policy is **versioned, additive/update-only**:

- [x] Version catalog content independently from the mutable schema, and record
      the applied version in the runtime database.
- [x] Apply the upgrade idempotently: re-running it changes nothing.
- [x] Insert catalog exercises that the runtime database lacks.
- [x] Update catalog-owned columns of exercises it already has.
- [x] **Never delete or rename a catalog exercise automatically.** A row absent
      from a newer catalog is left alone. Renaming is deletion plus insertion
      against a text primary key, and the user's plans and logs reference that
      key.
- [x] Never cascade into user-owned tables. `exercise_isolated_muscles` is
      catalog data and is reconciled with the catalog; `user_selection`,
      `workout_log`, and every other registered owned table are untouchable.
- [x] Preserve user-owned columns and user-created rows according to an
      explicit, documented column split.
- [x] Test upgrade from at least the previous shipped catalog version.

The asymmetry is deliberate. Adding a wrong exercise is a cosmetic defect the
user can ignore; deleting one silently invalidates their training history.

### 7.5 Packet B verification

Per packet:

- **B1** — resolver precedence tests across frozen/source/override cases; no
  import-time directory creation; logging writes under the resolved root; the
  frozen database path is computed but unused. Full pytest plus a Chromium
  smoke.
- **B2** — every §7.3 migration contract, on real files: legacy present, legacy
  absent, both present, WAL/SHM outstanding, spaces and non-ASCII in paths,
  read-only installation directory, repeat startup, and the real
  frozen-executable gate.
- **B3** — catalog upgrade from the previous shipped version, idempotence,
  additive-only behavior, and user-row preservation.

Stop and report before merging if any of these becomes true:

1. Migration could fall through to a clean seed after finding legacy data.
2. An existing runtime database could be replaced.
3. A catalog operation would delete a catalog row or cascade into user rows.
4. Windows frozen validation cannot exercise the real bootloader.
5. Implementation requires materially changing any approved policy above.

Cross-packet:

- [x] Existing legacy user data survives migration exactly once.
- [x] Fresh install receives the full catalog and zero user rows.
- [x] Repeated startup does not recopy or reset the database.
- [x] Packaged upgrades do not overwrite runtime data.
- [x] Automatic backups and erase-data recovery target the new runtime
      directory.
- [x] Logs do not require write access to the installation directory.
- [x] Worktrees remain isolated.
- [x] `DB_FILE` overrides remain deterministic.
- [x] Full pytest, E2E, cold-start, old-schema migration, packaged smoke, and
      recovery tests pass.

### 7.6 Recorded B1 results

`utils/runtime_paths.py` is the resolver. Before it, "where does state live" was
answered independently by `utils/config.py` (from its own `__file__`),
`utils/database.py` (from `DB_FILE`), and `utils/auto_backup.py` (from the
database's parent). Three answers that happened to agree is not one policy, and
a frozen build made them disagree — the installation directory is not writable
in general, yet all three pointed at it.

What B1 changed:

- `runtime_root()` implements the §7.2 precedence. `HT_RUNTIME_DIR` is the
  runtime-root override; it relocates the whole tree in one move and is the
  supported portable-install mechanism.
- **Logs moved**; the database did not. `logs_dir()` is `runtime_root()/logs`,
  so a frozen install writes logs to `%LOCALAPPDATA%\HypertrophyToolbox\logs`
  instead of needing write access to its own installation directory. Logs carry
  nothing worth migrating, so relocating them cannot lose anything — which is
  exactly why they can move a packet before the database.
- **Import-time directory creation is gone.** `utils/config.py` used to
  `os.makedirs` both `data/` and `logs/` at import, in whatever directory
  happened to resolve — including during test collection. `get_db_connection()`
  now creates a missing database parent directory at connection time, which
  preserves the old guarantee for every entry point, and logging creates its own
  directory when it initializes.
- **`utils/database.py::DATA_DIR` removed.** Dead — recomputed from `DB_FILE` at
  import and imported by nothing.
- In a source checkout every resolved path is byte-for-byte what it was before.

The sequencing constraint is enforced by tests, not by discipline.
`TestPacketB1DoesNotMoveTheDatabase` asserts that a *frozen* process still
resolves `DB_FILE` to `legacy_database_path()`, and an AST scan asserts that no
module under `utils/` or `routes/` references `runtime_database_path()` at all.
Those tests fail the moment the switch lands early; deleting them is part of
B2's work, not a way to make B1 pass.

Baseline at the packet's starting commit `e576cda`: **1,792 passed / 1 skipped**.
After: **1,812 passed / 1 skipped** — 20 new resolver contracts, minus the
`test_config` pair that asserted import-time directory creation and the
`test_logger` case that asserted `os.makedirs` was called, both rewritten to
assert behavior instead of implementation.

Runtime check: `HT_RUNTIME_DIR` pointed at a throwaway directory, real `app.py`
startup served `GET /` → 200 and wrote **both** `data/database.db` and
`logs/app.log` under that root, leaving the repository's own `logs/` untouched.

### 7.7 Recorded B2 results

`utils/runtime_migration.py` owns the decision, and `app.py` calls it
immediately **before** `bootstrap_runtime_database()`. That order is the whole
safety property: seeding first would create an empty database at the new path,
after which migration would correctly decline to overwrite it — and the user
would be staring at an empty catalog with their data still on disk. A test
parses `app.py` and asserts the call order rather than trusting it.

Non-destructiveness, as implemented:

- The legacy database is opened `mode=ro` through a URI connection. It is
  physically never written, so a read-only installation directory migrates
  fine — which a test asserts by chmod-ing the source directory to `0o500`.
- Unresolved `-wal` / `-journal` sidecars **refuse** migration rather than
  copying past them. Copying a database whose committed transactions still live
  in a WAL would silently drop them, and resolving the WAL would mean writing to
  the legacy file. Refusing costs one restart; the alternative costs data.
- The copy goes to a temporary sibling, is verified there — `integrity_check`,
  `foreign_key_check`, and per-table row counts equal to the source — and only
  then is published with the same no-overwrite atomic rename the seed bootstrap
  uses. That primitive moved to `runtime_paths.publish_without_overwrite()`; two
  copies of an atomic-publication routine is one too many.
- Every failure path returns the **legacy** path as the database to use, logs
  what failed, and logs how to retry. A corrupt legacy database yields a refusal
  and a recovery message, never a clean seed.

Backups are copied best-effort, once, and a failure is logged and swallowed: the
originals are untouched, so a failed copy costs nothing, while blocking startup
over it would cost the user their session. Old logs are not migrated.

**A defect the tests caught before merge.** `_verify_copy` originally used
`with sqlite3.connect(...)`, which commits but does not close. On POSIX the
rename succeeds anyway with the handle open; on Windows it fails with
`WinError 32`. Every successful-migration test failed on Windows and would have
passed in Linux CI — the copy verified and then could not be published. Fixed
with `contextlib.closing`.

Baseline at the packet's starting commit `a7883d4`: **1,812 passed / 1 skipped**.
After: **1,837 passed / 1 skipped** — 25 migration contracts, including the B1
guards inverted into their B2 counterparts.

Real frozen validation, `--mode bootloader` against a fresh `build_exe.bat`
build:

- Fresh install: the runtime database is created **under the runtime root**, the
  packaged seed is byte-identical, **the installation directory gains no runtime
  files at all**, and `app.log` is written under the runtime root.
- Upgrade: a legacy database carrying a plan row was planted in the
  installation directory exactly where every earlier release put it. The app
  served 1,897 exercises, the database moved to the runtime root, **the plan row
  survived**, and **the original file is still there, byte-identical**.

### 7.8 Recorded B3 results

`utils/catalog_upgrade.py` applies the shipped catalog to an existing runtime
database. `app.py` calls it after `run_all_initializers()` and only when the
seed bootstrap did *not* just create the database — never from
`run_all_initializers()` itself, for the same reason the seed bootstrap is not
called there: the test suite initializes empty schemas deliberately, and
injecting 1,897 exercises would change what most of the suite means.

**Versioning is content-addressed.** The applied version is recorded in a
`catalog_version` table, but the trigger is a SHA-256 over the shipped catalog's
own rows rather than a hand-maintained number. A number can be forgotten during
a catalog change; a content hash cannot go stale. `catalog_version` is catalog
metadata and is deliberately absent from `OWNED_TABLES_DROP_ORDER`, so erasing
user data does not force a needless full re-scan.

#### The finding that shaped this packet

§7.4 assumed a clean split between catalog columns and user columns, and that
`exercise_isolated_muscles` could simply be "reconciled with the catalog". The
code says otherwise. `ExerciseManager.save_exercise()` — reached from
`POST /add_exercise` — lets a user rewrite an exercise's muscle groups,
equipment, mechanic, difficulty, utility, grips, stabilizers, synergists, and
force, **including on catalog exercises**. Those columns are user-owned the
moment a row exists, and refreshing them from the seed would silently discard
the user's edit. The same call derives `exercise_isolated_muscles` from the
user-editable `advanced_isolated_muscles` column, so reconciling that table
would overwrite user intent too.

The implemented split is therefore narrower than §7.4 implied, and deliberately
so:

- **Refreshed on existing rows:** `movement_pattern`, `movement_subpattern`,
  `youtube_video_id`, `media_path` — the four columns no application path lets a
  user write.
- **Never touched on existing rows:** every user-editable column, and
  `exercise_isolated_muscles`.
- **Inserted whole:** exercises absent from the runtime database, with their
  isolated muscles.
- **Never removed or renamed:** an exercise absent from a newer catalog is left
  alone, whether it is a user's own or a retired one.

A test parses `exercise_manager.py` and fails if any refreshed column appears in
`save_exercise`'s editable column list — so a column that later becomes
user-editable breaks the build instead of quietly starting to discard edits.

**A missing shipped value never erases a populated one.** Verifying against the
real catalog turned up the hazard: the shipped seed carries `media_path` for
**0 of 1,897** rows and `youtube_video_id` for **56**, while `movement_pattern`
is complete and `movement_subpattern` covers 1,282. Refreshing on plain
inequality would blank populated columns the moment a catalog was regenerated
without them — data loss dressed as an update. Only non-`NULL` shipped values
are applied, and a test pins both halves: the empty value does not erase, and a
real correction still lands.

This stays inside the approved B-D5 policy (additive/update-only, never delete
or rename); it is strictly more conservative than the policy's minimum.

Baseline at the packet's starting commit `abfc048`: **1,837 passed / 1 skipped**.
After: **1,856 passed / 1 skipped** — 19 catalog-upgrade contracts.

Checked against the real 1,897-exercise catalog, not only synthetic fixtures.
An "older install" was built by deleting three exercises, corrupting
`movement_pattern` on five, editing one exercise's equipment, setting a
`media_path` the seed does not carry, and adding a user-created exercise with a
plan row referencing it. The upgrade inserted the three, corrected all five,
preserved the equipment edit and the `media_path`, kept the user's exercise and
plan, and the second run reported `already-current`.

---

## 8. Packet C — Remaining Root and Tooling Hygiene

Packet C returns to the original cosmetic/organizational request after the data
boundary is safe.

### 8.1 Root generated-output policy

- [ ] Redirect baseline output to `artifacts/` instead of the root.
- [ ] Update the baseline command in `CLAUDE.md`.
- [ ] Update `docs/ai_workflow/INDEX.md`, which currently documents root
      `baseline_*.txt` files.
- [ ] Keep root screenshot patterns ignored as defense in depth.
- [ ] Prefer tools that write screenshots and reports directly under
      `artifacts/`.

### 8.2 Launcher and distribution modernization

- [ ] Revisit the Packet A0 build-environment choice only if user-launcher and
      developer-build ergonomics still conflict; do not undo the pinned,
      reproducible build contract.
- [ ] Standardize `START.bat` with canonical `.venv` commands, or document why
      the user launcher intentionally owns a separate `venv`.
- [ ] Remove the duplicate `pause` in `START.bat`.
- [ ] Verify the supported Python version in `QUICK_START.md` and `README.md`.
- [ ] Decide whether `QUICK_START.md` duplicates too much of `README.md`.
- [ ] Keep user-facing launchers at the root if double-click discoverability is
      still a product requirement.
- [ ] Keep the spec at the root unless a tested build command explicitly points
      elsewhere; a root spec is conventional.

### 8.3 IDE metadata

`.idea/` and `.vscode/` are ignored now, but some files remain tracked because
they predate the ignore rules.

- [ ] Decide whether `.vscode/launch.json` is useful shared project
      configuration.
- [ ] Remove tracked `.idea/` metadata unless there is a documented team reason
      to retain it.
- [ ] Do not delete personal IDE files from a user's filesystem merely to
      untrack them; use `git rm --cached` when appropriate.

### 8.4 Root documentation policy

The intended root allowlist should be documented by category, not as only four
filenames. A healthy root may contain:

- Application entry points.
- User-facing start/readme files.
- Build manifests.
- Tool configuration that relies on root discovery.
- Repository operating instructions.

Generated reports, screenshots, scratch databases, and personal state belong
under ignored artifact/runtime locations, not the root.

---

## 9. Blind-Spot Register

| Risk | Why it is easy to miss | Required mitigation |
|---|---|---|
| Ignored files enter packages | PyInstaller reads the filesystem, not Git | Exact packaging allowlist plus built-tree inspection |
| Ignored files exist under `static/` too | Broad asset-tree inclusion repeats the `data/` problem | Tracked-file staging or fail-closed asset-root guard |
| Asset guard rejects the known excluded scratch tree | A blanket `git status --ignored` failure makes current builds impossible | Allow only the exact excluded GPT root; fail on every new path |
| Tightening `static/` drops required vendor assets | A broad exclusion can fix leakage by breaking the UI | Compare packaged assets with reviewed tracked manifest and smoke media paths |
| Deleted SQLite rows remain recoverable | Zero row counts do not clear freelist pages | Clean rebuild or `VACUUM`; verify freelist and sequences |
| Spec and batch file diverge | The batch file currently deletes the spec | One canonical spec or tests for both definitions |
| Worktree gets visual test data | `new-worktree.ps1` defaults to `visual` | Packet A must use `-Seed copy-current` and revalidate |
| Packet A branches from unmerged work | Worktree helper uses the caller's `HEAD` | Wait for PR #165, refresh, and base explicitly on recorded `origin/main` |
| Old worktrees retain the untracked runtime DB | Their `skip-worktree` flag becomes inert after the path leaves the index | Inspect/preserve needed state, then retire both redundant clean worktrees |
| Patch-equivalent commit looks unmerged | SHA ancestry fails when the same change landed under another commit | Use `git cherry` or patch comparison before treating the work as open |
| Git status hides DB changes | `skip-worktree` suppresses normal status | Check `git ls-files -v`; intentionally clear flag |
| Seed negation is placed before `*.db` | Later ignore rules win, silently hiding the seed | Put the exception after `*.db` beside the visual-seed precedent and test visibility |
| Privacy tuple omits a new table | A registry cannot detect its own omissions | Compare all seed tables against catalog set plus registry |
| Seed table is missing | A test that skips absent tables falsely passes | Assert every registered table exists and is empty |
| Bootstrap is placed in shared initialization | Test fixtures intentionally create missing, empty DB paths | Invoke bootstrap only from `app.py` startup, never initializer/handler/config helpers |
| Cold-start coverage is weakened | Seed bootstrap masks schema-from-empty behavior | Preserve separate first-install and empty-schema tests |
| Interrupted first copy creates corrupt DB | Plain file copy is not atomic | Temporary sibling plus atomic rename/concurrency handling |
| Existing DB is overwritten | Missing/old/corrupt states can be conflated | Never replace an existing path with the seed |
| Packaged update overwrites runtime state | Mutable DB currently lives with bundled assets | Packet B moves writable state and tests upgrade behavior |
| Existing users miss catalog changes | Seed is copied only once | Versioned, idempotent catalog update strategy |
| Worktrees share global app data | A single OS data path defeats isolation | Frozen/source path distinction or unique worktree override |
| Backups and logs remain misplaced | Moving only `DB_FILE` is incomplete | Include backups, recovery files, and logs in Packet B |
| First launch creates redundant backup | Startup backup sees 1,897 exercises immediately | Decide whether pristine seed copies should be backed up |
| Binary hashes are unstable | SQLite page order and vacuum can change bytes | Contract on logical sorted-row hashes, not only file hash |
| Build inputs contain other sensitive content | Allowlisted files can still be wrong | Audit each allowed file and test its content contract |
| Branch baseline drifts | Active local commits change test count | Record starting SHA and baseline in the packet worktree |
| Approved plan remains untracked or branch-local | A clean or new worktree cannot see it | Commit and integrate the plan into main before Packet A branches |
| Local user changes are overwritten | Shared docs are already dirty | Targeted staging and explicit diff review |
| Runtime asset paths differ when frozen | `__file__`, `_MEIPASS`, and executable dir differ | Test source and packaged seed resolution |
| Build is not reproducible | PyInstaller is installed on demand and config is stale | Packet A0 pins build requirements and proves a clean isolated build |
| Build preflight packages sensitive checkout state | Proving the old toolchain still consumes broad filesystem inputs | Run preflight only in a disposable `-Seed empty` worktree with no ignored scratch |
| Visual seeder fallback dangles | It falls back to the runtime path that Packet A untracks | Repoint only `DEFAULT_SOURCE` to the catalog seed; preserve live-output guards |
| Development-only CSV is shipped | A conservative allowlist can become a new broad include | Ship only files reached by packaged runtime code |
| History rewrite creates greater damage | Force-push breaks ancestry without erasing caches reliably | Keep the standing no-rewrite decision |
| Staged file mutated at equal size and mtime | Size/mtime comparison passes and the file is never recopied or rejected | Packet A3 compares SHA-256; equal sizes fall through to the digest |
| Digest cache proves itself | Reusing the copy decision's digests in verification gives both the same failure mode | Verification recomputes independently |
| `manifest.sha256` staged inside the tree | The tree must match the manifest exactly, so the record of it becomes an unexpected file | Write it beside the staging root |
| Payload smoke mistaken for a bootloader smoke | It exercises the same packaged files and reads like a full packaged run | Label it in code and docs; require the real `.exe` on a `windows-latest` runner |
| Host security state recorded as a permanent fact | A2's `WinError 4551` note stopped reproducing without anything in the repository changing | Re-measure environment claims when acting on them; keep the gate in CI where the state is controlled |
| Frozen path switches before migration exists | Splitting Packet B for reviewability creates the gap between B1 and B2 | Activate the frozen `DB_FILE` switch atomically with migration (§7.2.1) |
| Migration verified after publication | A half-copied database is already live during the check | Copy to a temporary file, verify, then publish atomically |
| Legacy database "cleaned up" after migration | Deleting the source looks tidy and removes the only fallback | Never delete, move, or write to the legacy database |
| Backup copying blocks startup | Treating a best-effort copy as a hard dependency | Log and continue; the originals are untouched |
| Catalog upgrade removes a stale exercise | A row missing from a newer catalog looks like a deletion instruction | Additive/update-only; deletion and rename are never automatic |
| Catalog rename orphans user rows | The catalog primary key is the exercise name that plans and logs reference | Never rename automatically; treat as an owner-approved data migration |

---

## 10. Good and Bad Outcomes

### 10.1 A good Packet A result

- The root no longer contains disposable debug artifacts.
- The tracked seed is clearly named and contains only catalog data.
- Every user-owned table exists and is empty.
- The seed has no freelist residue or user-owned sequence state.
- A fresh runtime database is copied from the seed without mutating it.
- Existing databases are never overwritten.
- The build environment and PyInstaller version are reproducible from committed
  requirements.
- Packaging contains only explicitly approved data files.
- Recursive static/template inputs contain only reviewed tracked assets.
- Ignored personal files and backups are absent from the actual built
  distribution.
- The spec is the single packaging source of truth.
- Catalog tests read the seed, not mutable runtime data.
- Both first-install and empty-schema behavior remain tested.
- Full test and packaged smoke gates match the implementation baseline.
- The commit contains no unrelated user changes.

### 10.2 A bad Packet A result

- `data/` is still packaged recursively.
- The fix relies on `.gitignore`.
- The build passes only because of undeclared packages already installed in a
  developer's environment.
- `static/bodymaps/GPT/`, a nested `.git/`, or another ignored asset is still
  packaged.
- The package removes required tracked static/vendor files while attempting to
  exclude scratch content.
- A source-code assertion passes while the built distribution still contains
  backups or personal files.
- The tracked seed has zero visible rows but deleted data remains in freelist
  pages.
- A missing user table is treated as success.
- `build_exe.bat` and the spec retain independent, drifting definitions.
- App startup edits the seed in place.
- Existing runtime data is replaced on startup.
- The worktree accidentally promotes the visual E2E fixture as the production
  seed.
- The cold-start gate stops testing empty-schema initialization.
- A hard-coded test count is used from another revision.
- Unrelated dirty documentation or database state is committed.

### 10.3 A good Packet B result

- Frozen applications write only to a per-user writable runtime location.
- Existing user data migrates once and remains recoverable.
- Logs and backups follow the runtime-data policy.
- Source worktrees remain isolated.
- Application upgrades update catalog content without resetting user state.

### 10.4 A bad Packet B result

- Every checkout shares one OS-level SQLite file.
- Migration silently prefers the seed over an existing database.
- A read-only installation directory breaks startup or logging.
- Upgrade extraction overwrites the user's database.
- Backups remain inside the application bundle or repository.
- Catalog updates apply only to new installations.

---

## 11. Rollback and Recovery

### Packet A rollback

- Preserve the pre-change database copy until the packaged smoke and full test
  gates pass.
- Keep the change as an ordinary commit; no force-push or history rewrite is
  required.
- If the seed conversion fails, restore the exact tracked path and reapply
  `skip-worktree` only if returning to the old workflow.
- Never use a broad reset that could discard unrelated dirty files.
- Delete only generated `build/` and `dist/` outputs after resolving their exact
  paths.

### Packet B rollback

- Do not delete the legacy database during migration.
- Copy or back it up before switching the default path.
- On migration failure, continue using the legacy path or fail with explicit
  recovery instructions; do not start with an empty seed and present it as
  success.
- Retain migration tests and a manual restore procedure for at least one release
  cycle.

---

## 12. Final Execution Checklist

### Recommended sequence

1. Owner approvals — completed 2026-07-25.
2. Commit this plan and merge or cherry-pick it into `origin/main`; merely
   committing it on the handover branch does not make it visible to a Packet A
   worktree based on main.
3. Cleanly retire both redundant worktrees after one final clean-status and
   runtime-data check. The filter change is merged by ancestry; the security
   change shipped as patch-equivalent PR #157 commit `3ce69dc`.
4. Run Packet A0's non-publishing toolchain probe in a disposable
   `-Seed empty` worktree; discard its build output after recording the result.
5. Fetch and record the then-current `origin/main`.
6. Create the implementation worktree explicitly from that `origin/main`.
7. Land the committed Packet A0 build-definition changes as the first isolated
   commit, then implement and verify Packet A.
8. Review and land Packet A2 separately. Landed from `origin/main` at
   `22350ec`; see §6.10 for the recorded results.

The disposable A0 probe is technically independent and can occur earlier
because its artifact is never published. Any committed plan, A0, or Packet A
change must be integrated from the approved `origin/main` lineage.

### Packet A authorization checklist

Owner approval recorded on 2026-07-25. All five recommended options were
accepted explicitly.

- [x] Owner approves the no-history-rewrite decision.
- [x] Owner approves the seed name `data/catalog.seed.db`.
- [x] Owner approves packaging only `data/catalog.seed.db` and
      `data/free_exercise_db_mapping.csv` from `data/`.
- [x] Owner approves first-run seeding for a missing configured `DB_FILE`.
- [x] Owner approves the Packet A/Packet A2 split: immediate exclusion plus
      fail-closed guard now, tracked-asset staging in a separately reviewed
      packet.

### Packet A execution prerequisites

> **Bookkeeping note.** These items duplicate state also tracked in §6.1 and the
> §12 sequence, so they can drift out of sync — they did once already, when A0
> landed and only §6.1 was updated. Whoever completes an item must tick it in
> **both** places, or the next session will re-do finished work.

- [x] Active workstream ownership and starting revision are recorded. Packet A
      starts from `origin/main` at **`b715a02`**; no other workstream is active
      (zero open PRs, single worktree).
- [x] PR #165 is merged into `origin/main`.
- [x] This approved plan is tracked and integrated into `origin/main`, so the
      implementation worktree can read it. (PR #166.)
- [x] Packet A is based on the refreshed, recorded `origin/main`, not the
      handover-branch `HEAD`.
- [x] Both redundant CSS/security worktrees receive a final clean-status and
      runtime-data check, then are cleanly retired. Both were verified clean,
      removed, and their branches deleted; the leftover `filter-btn` directory's
      two junctions to the main checkout's `.venv` / `node_modules` were unlinked
      individually (never recursively) with both targets verified intact after.
- [x] Packet A0 pins the build environment and proves a clean disposable build.
      (PR #167, `b715a02` — `pyinstaller==6.21.0`, exit 0, zero pandas/NumPy
      diagnostics.)
- [x] Packet A0's `-Seed empty` worktree is verified to contain no runtime DB,
      backup, personal export, or GPT scratch input before building.
- [x] The sanitized source database is copied into the implementation worktree
      with hashes and counts revalidated.

### Packet A completion checklist

- [x] Packet A0 and privacy preflight complete.
- [x] Clean physical seed committed.
- [x] Runtime DB untracked and ignored.
- [x] Bootstrap implemented and tested.
- [x] Packaging definitions consolidated.
- [x] Privacy and registry-completeness contracts added.
- [x] Deep-gate coverage split correctly.
- [x] Full pytest baseline passes.
- [x] Built distribution inspected.
- [x] Packaged first-run smoke passes.
- [x] Documentation updated.
- [x] Final diff contains no unrelated changes.

### Packet A2 completion checklist

> **Bookkeeping note.** These items duplicate §6.10. Whoever completes one must
> tick it in **both** places.

- [x] Manifest generated deterministically from `git ls-files`.
- [x] Staging tree rebuilt, pruned, and verified against tracked sources.
- [x] Executable-bit, path, and case behavior preserved and tested.
- [x] Asset-parity diff reviewed: 997 files, zero added, zero dropped.
- [x] Packet A's broad-tree guard removed with equivalent fail-closed tests.
- [x] `Hypertrophy-Toolbox.spec` remains the canonical packaging definition.
- [x] Real `build_exe.bat` build completed and the `dist/` tree inspected.
- [x] Packaged smoke passed from a clean copy of the distribution.
- [x] Shipped seed unchanged, private, and never overwritten.
- [x] Full pytest and Chromium smoke pass against the recorded baseline.
- [x] Final diff contains only intentional Packet A2 files.

### Packet B authorization checklist

Owner approval recorded on 2026-07-26. All five decisions were accepted as
proposed; see §7.1 for their authoritative statement.

- [x] Runtime path policy selected. (B-D1 — centralized resolver, §7.2
      precedence.)
- [x] Source-worktree isolation policy selected. (B-D2 — repository-local for
      checkouts and worktrees; OS user-data paths only when frozen.)
- [x] Legacy migration policy selected. (B-D3 — verified, non-destructive;
      the legacy database is never deleted or modified.)
- [x] Logs and backups policy selected. (B-D4 — relocate logs, copy legacy
      backups once best-effort, do not migrate old logs.)
- [x] Catalog upgrade policy selected. (B-D5 — versioned, additive/update-only;
      never delete or rename catalog exercises automatically.)

Also approved in the same ruling:

- [x] Packet A3 lands first as an independent PR: SHA-256 staging
      verification, `manifest.sha256`, and the equal-size/equal-mtime mutation
      regression test.
- [x] A real `windows-latest` frozen-executable gate is added; the local
      payload smoke stays, clearly labelled as not exercising the bootloader.
- [x] Smart App Control is never disabled. Windows Sandbox may be used only if
      already available without changing host security settings.
- [x] `utils/database.py::DATA_DIR` is removed in the Packet B change that
      centralizes path resolution.
- [x] Sequencing correction: the frozen `DB_FILE` switch activates atomically
      with legacy migration (§7.2.1).

### Packet A3 / B execution sequence

Every packet starts from freshly fetched `origin/main`, records its actual
starting SHA and test baseline, ships as one PR declaring its behavior and
schema changes, and merges only on green CI.

1. [x] This document records the accepted decisions and closes the Packet B
       authorization checklist. (PR #171.)
2. [x] **A3** — staging SHA-256 hardening and the real frozen gate.
3. [x] **B1** — resolver, config, and logging foundation, without switching the
       frozen database path.
4. [x] **B2** — frozen runtime database path, legacy migration, and backup
       copying, activated atomically.
5. [x] **B3** — catalog versioning and additive upgrade behavior.

The verified starting point for this sequence is `origin/main` at
`631f61a13036861841a00ce8360d40b6698f16f8`.

### Packet C completion checklist

- [ ] Baselines write to `artifacts/`.
- [ ] Launcher environment naming is consistent.
- [ ] Packaging dependencies are reproducible.
- [ ] IDE tracking decision completed.
- [ ] Root-file policy documented in the main contributor guidance.

---

## 13. Definition of Done

The root cleanup is genuinely complete when:

1. Root files are intentional and categorized.
2. Generated output is directed away from the root.
3. The repository ships an immutable, physically sanitized catalog seed.
4. Mutable user data is never tracked or packaged as an asset.
5. Packaging is allowlist-based and verified against the real build output.
6. Fresh installs have the catalog and no user state.
7. Existing installations cannot be overwritten by seed bootstrap or upgrade.
8. Automated contracts fail when a new user table, unapproved package input, or
   dirty seed is introduced.
9. Worktree isolation, database recovery, and migration behavior remain intact.
10. All applicable test, E2E, and packaged smoke gates pass from the recorded
    starting revision.
