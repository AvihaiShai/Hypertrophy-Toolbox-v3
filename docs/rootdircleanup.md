# Root Directory Cleanup and Data Packaging Safety Plan

**Status:** Owner-approved execution plan; implementation has not started

**Last evidence pass:** 2026-07-25

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
reviewable.

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

- [ ] Stop the Flask server and any process that may have the database open.
- [ ] Confirm `data/database.db-wal`, `-shm`, and `-journal` do not exist.
- [ ] Record the implementation worktree's starting commit.
- [ ] Record the pre-change targeted and full pytest baseline at that commit.
- [ ] Record SHA-256 hashes and row counts for the source local database.
- [ ] Confirm all catalog hashes and user-table counts listed in Section 4.5.
- [ ] Preserve a recoverable copy of the source database outside the paths that
      will be renamed or packaged.
- [ ] Confirm unrelated dirty files and active workstream ownership before
      editing shared paths.
- [x] Confirm PR #165 merged; `origin/main` was `95f30c1` at the
      2026-07-25 review.
- [ ] Fetch `origin` again immediately before execution and record the exact
      `origin/main` SHA selected as the Packet A base.
- [ ] Start Packet A from that refreshed `origin/main`; do not inherit the
      current handover branch by accident.
- [ ] Settle, update, or retire worktrees that retain `skip-worktree` state for
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

- [ ] Remove the `skip-worktree` flag deliberately.
- [ ] Create `data/catalog.seed.db` from the validated local catalog.
- [ ] Ensure the tracked `data/database.db` entry is removed.
- [ ] Add `!data/catalog.seed.db` to `.gitignore` after the broad `*.db` rule,
      beside the existing `!e2e/fixtures/database.visual.seed.db` exception.
- [ ] Prove the exception is effective: the seed is visible to Git, stages
      normally, and appears in a fresh-clone/file-list check.
- [ ] Physically sanitize the seed using a clean SQLite backup/rebuild followed
      by `VACUUM`, rather than relying only on `DELETE`.
- [ ] Confirm `PRAGMA freelist_count = 0` after finalization.
- [ ] Confirm `sqlite_sequence` contains no user-owned sequence state.
- [ ] Confirm no WAL/SHM/journal sidecars are staged or packaged.
- [ ] Confirm only the two catalog tables contain rows.
- [ ] Confirm all current schema tables exist.
- [ ] Confirm the logical catalog hashes remain unchanged.
- [ ] Confirm `PRAGMA integrity_check = ok`.
- [ ] Confirm `PRAGMA foreign_key_check` returns zero rows.
- [ ] Confirm ordinary app startup never writes to `catalog.seed.db`.

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

- [ ] Put bootstrap logic in a testable utility rather than embedding a large
      block directly in `app.py`.
- [ ] Invoke that utility only from real `app.py` startup immediately before
      `run_all_initializers()`.
- [ ] Add regression tests proving `run_all_initializers()`,
      `DatabaseHandler`, and `utils.config` do not bootstrap the seed on their
      own.
- [ ] Create the target parent directory safely.
- [ ] Copy through a temporary sibling file and atomically rename it, preventing
      a partial database if startup is interrupted.
- [ ] Handle two simultaneous first launches without corrupting or overwriting a
      completed target.
- [ ] Never overwrite an existing database, including an old-schema or corrupt
      one; existing recovery/migration behavior remains authoritative.
- [ ] Preserve the `DB_FILE` environment override.
- [ ] Decide and document that an explicitly configured but missing `DB_FILE`
      receives the seed. This is the recommended behavior because it matches a
      real fresh installation at any selected path.
- [ ] Ensure normal isolated pytest fixtures that intentionally create empty
      databases remain empty unless they explicitly exercise application
      bootstrap.
- [ ] Update `.claude/rules/database.md`, which currently states that there is
      no built-in seed.

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

- [ ] Reword the deep-gate job so its name matches what it proves.
- [ ] Assert `GET /` returns 200.
- [ ] Assert the first-install database contains the expected catalog.
- [ ] Assert every user-owned table is empty.
- [ ] Preserve a separate missing/empty database initializer test.
- [ ] Keep the old-schema migration job unchanged except for path terminology.

### 6.6 Consolidate and restrict packaging

- [ ] Change the spec from `('data', 'data')` to explicit file entries.
- [ ] Include only `data/catalog.seed.db` and
      `data/free_exercise_db_mapping.csv` from `data/`.
- [ ] Do not package `data/youtube_curated_top_n.csv`; it is a developer-side
      catalog-application input, not a runtime dependency.
- [ ] Make `build_exe.bat` invoke `Hypertrophy-Toolbox.spec`.
- [ ] Stop deleting the committed spec during builds.
- [ ] Confirm the destination paths match bootstrap's frozen asset lookup.
- [ ] Exclude `static/bodymaps/GPT/` and its nested `.git/` content from the
      build.
- [ ] Add a fail-closed pre-build guard that inventories ignored/untracked
      content under `static/` and `templates/`.
- [ ] Permit only the exact `static/bodymaps/GPT/` root that the spec explicitly
      excludes; fail on every other ignored/untracked path.
- [ ] Test the guard with a synthetic unexpected ignored/untracked asset so it
      is proven fail-closed.
- [ ] Verify intended tracked vendor assets, licenses, templates, JavaScript,
      CSS, images, and fonts remain present after tightening asset collection.
- [ ] Confirm `RUN_APP.bat` is still copied into the distribution.

Repair the E2E fallback without weakening the live-data guard:

- [ ] Change `e2e/scripts/prepare_visual_db.py::DEFAULT_SOURCE` to fall back to
      `data/catalog.seed.db`, not the now-untracked `data/database.db`, when the
      visual fixture is missing.
- [ ] Keep `LIVE_DB = data/database.db` and the `data/auto_backup/` output guard
      unchanged; those still identify paths a seeder must never overwrite.
- [ ] Confirm `prepare_e2e_db.py` continues to prefer the tracked visual fixture
      and wipe its own throwaway user state.

### 6.7 Add privacy and packaging contracts

Use `utils.schema_registry.OWNED_TABLES_DROP_ORDER` as the canonical user-table
registry.

For every registered table, tests must:

- [ ] Assert the table exists in the seed.
- [ ] Assert its row count is zero.

The existence assertion matters: silently skipping a missing table would allow
a stale seed to pass.

Add a schema-registry completeness check:

- [ ] Enumerate all non-internal tables in the seed.
- [ ] Treat `exercises` and `exercise_isolated_muscles` as catalog tables.
- [ ] Assert every other application table is represented in
      `OWNED_TABLES_DROP_ORDER`.

This catches the case where a developer creates a new user table but forgets to
add it to the registry; testing only the tuple cannot detect its own omissions.

Additional contracts:

- [ ] Assert catalog row counts and stable logical-row hashes.
- [ ] Assert SQLite integrity and foreign-key integrity.
- [ ] Assert `catalog_db_path` copies `data/catalog.seed.db`, never the runtime
      database.
- [ ] Assert the spec contains no recursive `data/` source.
- [ ] Assert the spec's approved data source set exactly matches the allowlist.
- [ ] If the batch file remains a second packaging definition, assert its
      approved data set too.
- [ ] Build the executable and inspect the actual `dist/` tree; source-text tests
      are not sufficient.
- [ ] Assert the distribution contains none of:
      `auto_backup`, `.personal-*`, additional `.db` files, SQLite sidecars, or
      unapproved files from `data/`.
- [ ] Assert the distribution contains no `static/bodymaps/GPT/`, nested `.git`
      directories, or other ignored/untracked source-tree files.
- [ ] Check a reviewed Packet A set of required static/template assets and smoke
      their production paths so the GPT exclusion cannot silently remove
      required UI assets.
- [ ] Open the shipped seed from the built distribution read-only and rerun the
      privacy contract against that exact artifact.

### 6.8 Packet A verification gate

- [ ] Targeted seed/privacy tests pass.
- [ ] Catalog invariant and volume taxonomy tests pass.
- [ ] Harness isolation tests pass.
- [ ] Config/bootstrap tests pass.
- [ ] Old-database migration tests pass.
- [ ] Full pytest matches the baseline established at the packet's actual
      starting commit.
- [ ] Relevant Playwright smoke tests pass against a throwaway runtime DB.
- [ ] `build_exe.bat` completes successfully.
- [ ] The packaged application boots from a clean extracted directory.
- [ ] First packaged launch creates a runtime copy and leaves the packaged seed
      unchanged.
- [ ] The packaged app serves the main page and exercise filters return catalog
      data.
- [ ] The final `git diff` contains only intentional Packet A files.
- [ ] `git status` is also checked with ignored and index-flag awareness.

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

- [ ] Generate the manifest deterministically from the intended repository
      assets.
- [ ] Do not depend on ignored/untracked working-copy content.
- [ ] Preserve executable-bit/path/case behavior needed by the supported
      platforms.
- [ ] Compare the staged tree with the tracked source set before building.
- [ ] Review a complete asset-parity diff, including vendor licenses and media.
- [ ] Run page, CSS, JavaScript, favicon, body-map, and exercise-media packaged
      smoke tests.
- [ ] Confirm the final distribution contains no nested repository metadata.
- [ ] Remove Packet A's temporary broad-tree guard only when the staging
      manifest makes it redundant and equivalent fail-closed tests exist.

Packet A2 is not required to land Packet A. Keeping it separate reduces the risk
that privacy remediation silently drops required vendor assets.

---

## 7. Packet B — Runtime Data Outside Immutable Application Assets

Packet B is the preferred long-term design but is intentionally separate
because it changes path semantics across the application, tests, scripts,
worktrees, logs, backups, and installed builds.

### 7.1 Required product decisions

- [ ] Choose the per-user runtime directory convention on Windows, macOS, and
      Linux, or adopt a maintained helper such as `platformdirs`.
- [ ] Decide whether source checkouts use the OS user-data directory or retain a
      worktree-local ignored runtime path.
- [ ] Decide how an existing `data/database.db` is migrated.
- [ ] Decide whether logs move with the runtime database.
- [ ] Decide whether automatic backups move with the runtime database.
- [ ] Decide how portable/USB-style installs are supported, if at all.

### 7.2 Recommended path behavior

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

- [ ] Use the SQLite backup API or an equivalent consistent copy for a live
      database.
- [ ] Refuse migration while unresolved WAL/SHM state exists unless SQLite
      performs the copy through a live connection.
- [ ] Record migration completion without putting sensitive paths or row data in
      logs.
- [ ] Provide a clear recovery message if migration fails.
- [ ] Verify old-schema migration after relocation.
- [ ] Test paths containing spaces and non-ASCII characters.
- [ ] Test read-only installation directories.
- [ ] Test upgrade/reinstall over an existing user-data directory.

### 7.4 Catalog updates after first install

A seed only initializes new users. It does not automatically update the catalog
inside an existing runtime database.

Before Packet B is considered complete, define how future releases add or
correct catalog rows without overwriting user state:

- Version catalog content independently from the mutable schema.
- Apply idempotent catalog migrations/imports to existing runtime databases.
- Preserve user-owned columns or custom rows according to an explicit policy.
- Test upgrade from at least the previous shipped catalog version.

Without this, fresh installs and upgraded installs can silently diverge.

### 7.5 Packet B verification

- [ ] Existing legacy user data survives migration exactly once.
- [ ] Fresh install receives the full catalog and zero user rows.
- [ ] Repeated startup does not recopy or reset the database.
- [ ] Packaged upgrades do not overwrite runtime data.
- [ ] Automatic backups and erase-data recovery target the new runtime
      directory.
- [ ] Logs do not require write access to the installation directory.
- [ ] Worktrees remain isolated.
- [ ] `DB_FILE` overrides remain deterministic.
- [ ] Full pytest, E2E, cold-start, old-schema migration, packaged smoke, and
      recovery tests pass.

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
8. Review and land Packet A2 separately.

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

- [ ] Active workstream ownership and starting revision are recorded.
- [x] PR #165 is merged into `origin/main`.
- [ ] This approved plan is tracked and integrated into `origin/main`, so the
      implementation worktree can read it.
- [ ] Packet A is based on the refreshed, recorded `origin/main`, not the
      handover-branch `HEAD`.
- [ ] Both redundant CSS/security worktrees receive a final clean-status and
      runtime-data check, then are cleanly retired.
- [ ] Packet A0 pins the build environment and proves a clean disposable build.
- [ ] Packet A0's `-Seed empty` worktree is verified to contain no runtime DB,
      backup, personal export, or GPT scratch input before building.
- [ ] The sanitized source database is copied into the implementation worktree
      with hashes and counts revalidated.

### Packet A completion checklist

- [ ] Packet A0 and privacy preflight complete.
- [ ] Clean physical seed committed.
- [ ] Runtime DB untracked and ignored.
- [ ] Bootstrap implemented and tested.
- [ ] Packaging definitions consolidated.
- [ ] Privacy and registry-completeness contracts added.
- [ ] Deep-gate coverage split correctly.
- [ ] Full pytest baseline passes.
- [ ] Built distribution inspected.
- [ ] Packaged first-run smoke passes.
- [ ] Documentation updated.
- [ ] Final diff contains no unrelated changes.

### Packet B authorization checklist

- [ ] Runtime path policy selected.
- [ ] Source-worktree isolation policy selected.
- [ ] Legacy migration policy selected.
- [ ] Logs and backups policy selected.
- [ ] Catalog upgrade policy selected.

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
