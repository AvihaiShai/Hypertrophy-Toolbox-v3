# Repository Decisions

This document records durable, cross-cutting project decisions as lightweight
architecture decision records (ADRs). Accepted decisions remain here as
historical context even when the code or tool that prompted them is later
retired; changed decisions are superseded by a new ADR rather than silently
rewritten.

## Historical exercise-import rules

The Excel-to-SQLite merge utility that these rules governed is no longer present
under `scripts/`. The rules are retained as historical context for ADR-001, not
as instructions for a currently supported command.

- **Normalization rules**: Trim leading/trailing whitespace, collapse internal whitespace to a single space, and normalize endash/emdash characters to the ASCII hyphen before any comparisons.
- **Exact name matching**: Import logic only merges rows whose normalized `exercise_name` strings are identical. No fuzzy, partial, or substring matching is permitted.
- **Empty cell handling**: Blank strings and missing values coming from Excel are treated as nulls and never overwrite populated database fields.
- **Case sensitivity flag**: `--nocase` enforces a `COLLATE NOCASE` uniqueness constraint; when omitted, uniqueness is strictly case-sensitive.
- **Update-only flag**: `--update-only` converts unmatched Excel rows into skipped entries instead of inserts.
- **Default paths**: Unless overridden, the tool reads from `data/exercises.xlsx`, writes to `data/database.db`, and emits Markdown artifacts in `docs/`.

### Data semantics

- Equipment semantics: The equipment field intentionally includes both gear (Barbell, Dumbbells, …) and categories (Yoga, Recovery, Stretches, Cardio). These are first-class filter values.
- Enumerations: Incoming `force`, `mechanic`, and `difficulty` values are canonicalized to `Push`/`Pull`/`Hold`, `Compound`/`Isolation`, and `Beginner`/`Intermediate`/`Advanced` respectively before merging.

## ADR Log

New cross-cutting or durable project decisions should be added here as lightweight ADRs. Use the next sequential number, keep the original ADR unchanged after acceptance, and supersede it with a new ADR if the decision changes.

### ADR-001: Exercise import uses exact normalized name matching
- **Date**: 2026-05-11
- **Status**: accepted
- **Context**: The exercise import utility merges external Excel rows into the local SQLite exercise table. Fuzzy or partial matching could accidentally merge distinct movements and corrupt the exercise catalog.
- **Decision**: Import matching is based only on identical normalized `exercise_name` strings. Empty Excel cells never overwrite populated database values, and `--update-only` skips unmatched rows instead of inserting them.
- **Consequences**: Imports are predictable and auditable, but users must clean source exercise names before import when they expect two rows to match.

### ADR-002: The repository root holds five categories of file, and nothing else
- **Date**: 2026-07-26
- **Status**: accepted
- **Context**: The root-cleanup audit began from the impression that nearly every root file other than `app.py`, `CLAUDE.md`, `README.md`, and `requirements.txt` was accumulated clutter. Inspection did not support that. Most root files are there because a tool discovers them from the project root, and moving them would require wrapper commands or path overrides and make the project less conventional. The real problems the audit found were elsewhere — a tracked user database and unrestricted packaging inputs — and are addressed by `docs/rootdircleanup.md` Packets A and B. What the root actually lacked was a stated rule, so that the next judgment call is answerable without re-running the audit.
- **Decision**: The repository root may contain exactly these categories:

  | Category | Current members |
  |---|---|
  | Application entry points | `app.py`, `app_launcher.py` |
  | User-facing start / readme files | `README.md`, `QUICK_START.md`, `START.bat`, `RUN_APP.bat` |
  | Build manifests | `Hypertrophy-Toolbox.spec`, `build_exe.bat`, `requirements.txt`, `requirements-build.txt`, `package.json`, `package-lock.json` |
  | Tool configuration that relies on root discovery | `.gitignore`, `.mcp.json`, `.python-version`, `pyproject.toml`, `pyrightconfig.json`, `pytest.ini`, `.stylelintrc.json`, `.stylelintignore`, `tsconfig.json`, `vitest.config.js`, `playwright.config.ts` |
  | Repository operating instructions | `CLAUDE.md`, `AGENTS.md` |

  Generated reports, screenshots, scratch databases, baselines, and personal state do not belong in the root. They go under the gitignored `artifacts/` (build output under `build/` and `dist/`; runtime state under the path `utils/runtime_paths.py` resolves).

  Two corollaries, both learned the hard way:
  - **Do not move a root file merely to reduce the file count.** Some are load-bearing at the root: `Hypertrophy-Toolbox.spec` derives `REPO_ROOT` from `SPECPATH`, and a packaging contract test asserts `build_exe.bat` invokes it by that exact name. Root visibility is also part of what makes `START.bat` usable for its audience.
  - **A file in an approved category is not automatically justified.** It still has to be correct and non-duplicative; C2 trimmed `QUICK_START.md` rather than deleting it.
- **Consequences**: Adding a root file now requires naming its category, which makes the review question concrete instead of aesthetic. New generated output has an obvious destination, so the "temporary file at the root" habit has no excuse. The cost is that this table needs updating whenever a genuinely new root file is added — accepted, because the alternative is re-deriving the policy from scratch each time. The audit behind it is recorded in `docs/rootdircleanup.md` §8.4 and §12.

### ADR-003: Python 3.14.6 is the minimum supported runtime
- **Date**: 2026-07-29
- **Status**: accepted
- **Context**: The repository advertised Python 3.11+ while development and executable builds already ran on 3.14. CI and Pyright therefore validated an older runtime than the one used to ship the application, and local environments could silently retain an obsolete interpreter.
- **Decision**: Python 3.14.6 is the minimum for source runs, tests, CI, and executable builds. `.python-version` is the exact CI/environment-manager pin; Pyright targets the corresponding 3.14 language and standard-library surface; `utils/python_version.py` enforces the patch-level floor; and both Windows entry points derive the registered Python minor from the pin, validate its patch level, and validate any retained `venv`.
- **Consequences**: The project no longer promises Python 3.11–3.13 compatibility. Runtime, CI, analysis, and packaging now agree, and stale virtual environments fail with an actionable message. Adopting a newer minimum requires updating the canonical pin, runtime contract, Pyright target when the minor changes, its committed diagnostic baseline, and verification under the exact interpreter.

### ADR-004: The browser matrix is Chromium-only
- **Date**: 2026-08-02
- **Status**: accepted
- **Context**: `playwright.config.ts` declares exactly one project, `chromium`, and every CI invocation passes `--project=chromium`. Nothing had ever *decided* that — it was the Playwright scaffold default that no one revisited, so cross-browser coverage was absent by inertia rather than by choice. That left a standing implicit question ("shouldn't we add Firefox and WebKit?") that resurfaced in each testing review and could not be answered from the repository. The product context bounds it: this is a single-user, local-first tool served from `127.0.0.1:5000` and launched by its owner on Windows through `START.bat` / the packaged executable. There is no deployed multi-user surface and no analytics-derived browser distribution to serve. A matrix would multiply E2E wall-clock and, more importantly, multiply the visual-baseline set — already 84 committed Linux PNGs plus a Windows set, per renderer — and every added renderer needs its own baseline generation and human pixel review.
- **Decision**: Chromium is the only supported browser for the automated test suite, and the browser matrix is closed. Do not add Firefox or WebKit projects to `playwright.config.ts`, and do not add browser dimensions to the CI matrix, without superseding this ADR. This records the *testing* scope only; it makes no claim that the application is incompatible with other browsers, and it does not license Chromium-only code (vendor-prefixed CSS, Chrome-specific APIs) in the application itself.
- **Consequences**: E2E cost and visual-baseline maintenance stay bounded to one renderer, which is what makes per-platform pixel baselines affordable at all. The suite cannot catch a Firefox- or WebKit-specific rendering or API regression; if the owner ever opens the app in another browser, that is unverified territory and belongs to the manual layer. Reopening this is a real decision with a real bill — a new baseline set per renderer, generated on a pinned image and reviewed by a human — so it should be driven by an actual observed defect or a genuine distribution change, not by matrix-completeness instinct. Recorded per decision **D5** of [`TESTING_STRATEGY_PLANNING.md`](TESTING_STRATEGY_PLANNING.md) §6, signed 2026-08-02.

### ADR-NNN: <title>
- **Date**: YYYY-MM-DD
- **Status**: proposed | accepted | superseded by ADR-MMM
- **Context**: <forces at play>
- **Decision**: <what we chose>
- **Consequences**: <what becomes easier / harder>
