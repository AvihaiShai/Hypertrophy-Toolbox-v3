# Q4 — standalone JS Unit rename

**Owner-approved scope, 2026-10-21:** use `JS Unit (Vitest)` and land the rename
in its own change before any protection change. D2's approval is conditional on
the canonical §13.0 ledger recording the declared cycle; the owner explicitly
selected exact JS Unit job conclusions. C4 settings activation needs a separate
owner approval. This change implements the rename only.

The `js-unit` job identifier, steps, commands, runner, timeout, permissions and
failure behavior remain identical. Coverage still has no thresholds. The release
contract names the renamed check among the checks excluded from release
provenance; the twelve protected contexts and thirteen release expectations are
unchanged. C4's proposed future target uses the approved name without activating
it. Dated ledger rows and protection snapshots retain their historical names.
Ledger readers use the exact new display name for commits containing this rename
and the historical name for older commits; a rename is not a missing JS job.

The bounded implementation was approved in the owner's response to the concrete
R2.3 proposal. Under QUALITY_GATE this change requires full pytest and the
independent code reviewer. It adds/removes no job and converts none to `uses:`.
No new tests are needed for the display-name change; the existing exact-name
workflow/release contract is updated without changing its expected membership.

**Publication sequencing:** PR #546 currently occupies the shared `ci.yml` slot.
Prepare and validate this isolated change, then re-read that slot and fresh main
before publishing a workflow PR. This is not merge or C4 authority.

## Verification

- Independent required `code-reviewer`, `/root/q4_code_review`, reviewed the
  complete diff against `43f5df33` and the new record: **no findings**. It
  confirmed the sole executable workflow change is the display name, the
  exclusion contract remains intact, and no D2/C4 activation is claimed. The
  reviewer ran no tests and supplied no merge or settings approval.
- Normalized `js-unit` body comparison: identical apart from display name and
  comments; job count unchanged. The Vitest configuration is executable-identical
  after removing comments; the test AST changes only the exact excluded name.
  `scripts/release_gate.py` is byte-identical to base.
- `npm run test:js -- --coverage`: **13 files / 245 tests passed**.
- Inventory `--check`: **up to date**. TypeScript: **zero errors**.
  Pyright 1.1.410 / baseline diff: **zero diagnostics, zero net-new diagnostics**.
- Full pytest: **5,580 passed / 2 skipped / 0 failed**, exit 0, in 1,226.89 s.
  Command: `.venv/Scripts/python.exe -m pytest tests/ -q -n 4 --dist loadfile`,
  with private temp/cache and JUnit output under `artifacts/r23/`.
- Environment correction: the first attempt was stopped after reproducing a
  conflict between a forced `DB_FILE` and a test that reloads a temporary runtime.
  Removing that process override while retaining private `HT_RUNTIME_DIR` made
  all **20** configuration tests pass, followed by the green complete rerun above.
  Git Bash and private dependency/runtime/temp/cache paths were used. No source
  or test was changed to repair the environment, and failed/aborted attempts are
  not credited as a green full gate.
- Live protection re-read before committing: **12** contexts, `strict: false`,
  neither JS Unit display name protected. No settings write was made.
