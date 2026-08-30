# Gate 0 — blank/null rep-bound export validation

**Measured:** 2026-08-30T15:20:53Z  
**Base:** `e6e57eac224a09957d9c8ce3128ee6013cee6208` (`origin/main`)  
**Worktree:** `D:\development\Hypertrophy-Toolbox-v3-main-blank-null-rep-bound-gate0`  
**Branch:** `wt/blank-null-rep-bound-gate0`  
**Status:** contract and failing evidence complete; production implementation is not authorized by this packet

## 1. Gate-0 decision

At the plan-to-workout-log export boundary:

- actual `None` remains nullable;
- an exact blank string (`""`) in either rep bound is rejected;
- whitespace-only values remain rejected;
- numeric strings and valid numeric bounds remain accepted;
- a numeric minimum greater than the numeric maximum remains rejected under ADR-010;
- no value is trimmed, coerced, swapped, collapsed, or silently converted from blank to null;
- the complete persisted source set is validated before any workout-log row is written.

This packet changes tests, generated test inventory, and documentation only. It proposes no
schema constraint and makes no production change.

## 2. Boundary and reproduction

`POST /export_to_workout_log` does not accept rep bounds in its request body. The browser posts an
empty object, and the service reads the full persisted `user_selection` set. A test that posts
`{"min_rep_range": ...}` to this endpoint would therefore be a false oracle.

Current main calls `validate_workout_bounds(..., allow_null=True)`. That flag treats both actual
`None` and exactly `""` as null-equivalent for validation, but the service inserts the original
uncoerced values. SQLite accepts blank text in an `INTEGER`-affinity column, so the defect is not a
blank-to-null conversion: it is a blank TEXT write.

The committed characterization produces these exact current outcomes:

| Persisted source bounds | HTTP | Current target state | Scanner | Restore of equivalent item |
|---|---:|---|---|---|
| `min=""`, `max=12` | 200 | `planned_min_reps=""`, `typeof=text` | `[]` | skipped, minimum finite-number reason |
| `min=8`, `max=""` | 200 | `planned_max_reps=""`, `typeof=text` | `[]` | skipped, maximum finite-number reason |
| `min=""`, `max=""` | 200 | both target values blank TEXT | `[]` | minimum reason wins by field order |
| whitespace-only minimum or maximum | 400 | no log row | matching finding | skipped with matching reason |
| valid row plus blank row | 200 | both rows written | blank row omitted | restore keeps valid rows and skips invalid rows |

The mixed-row result is the observable defect, not a general transaction claim. Validation is
already a full-set preflight, so once blank is recognized as invalid it will reject before any
insert. Separately, the later insert loop commits each row individually; an unexpected database
error during insertion could leave earlier rows committed. General export transaction refactoring
is outside this packet.

## 3. Intended HTTP contract

For one `max=""` row named `GYM - Full Body - Workout A / Gate Zero Intended Blank`, the shared
blueprint test fixture must receive HTTP 400 and exactly:

```json
{
  "ok": false,
  "status": "error",
  "message": "Maximum reps must be a finite number. Invalid plan value on: GYM - Full Body - Workout A / Gate Zero Intended Blank. Fix these in the Workout Plan editor.",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Maximum reps must be a finite number. Invalid plan value on: GYM - Full Body - Workout A / Gate Zero Intended Blank. Fix these in the Workout Plan editor.",
    "requestId": null
  }
}
```

The shared pytest app does not install request-ID middleware, so its exact nested value is `null`.
The real app installs that middleware; there the same envelope carries the request ID and the
response header carries `X-Request-ID`. The route, response-envelope keys, error code, and status
do not change.

For a minimum blank, the canonical reason is `Minimum reps must be a finite number.`. When both
bounds are blank, the minimum reason wins because the validator parses minimum before maximum.

## 4. Mutation contract

On a recognized export validation rejection:

- every `user_selection` value remains byte-for-byte semantically unchanged, including blank TEXT;
- the complete pre-existing `workout_log` row set remains unchanged;
- no backup row or item is created;
- no Excel, backup, or other export artifact is created;
- no blank source value is repaired or rewritten to SQL `NULL`.

This is deliberately stated as no application/database-row mutation and no generated artifact.
Literal filesystem immutability is not the contract: error handling writes observability logs, and
closing a `DatabaseHandler` runs a WAL checkpoint that can alter a sidecar in WAL mode. The test
fixture uses DELETE journal mode and asserts the relevant logical database state.

## 5. Compatibility and policy matrix

| Case | Current | Intended | Gate-0 evidence |
|---|---|---|---|
| minimum `""` | 200 + blank TEXT write | 400 + exact minimum envelope + no write | green characterization; red patch |
| maximum `""` | 200 + blank TEXT write | 400 + exact maximum envelope + no write | green characterization; red patch |
| both `""` | 200 + two blank TEXT writes | 400; minimum reason first; no write | green characterization; red patch |
| minimum whitespace | 400 | unchanged 400 | committed characterization |
| maximum whitespace | 400 | unchanged 400 | committed characterization |
| both whitespace | 400 | unchanged 400; minimum first | committed characterization |
| rep-bound `None` | accepted at service boundary | remain accepted and forwarded as `None` | capturing fake DB, three cases |
| numeric strings `"8"`, `"12"` | accepted | remain accepted; no boundary rewrite | capturing fake DB |
| weight/RIR `0/0`, weight/RIR `1000/10`, rep equality `8/8` | accepted under existing bounds | unchanged | `tests/test_exports.py` existing boundary matrix |
| numeric `20 > 5` | 400 + named row | unchanged; never swap | ADR-010 tests in export and scanner suites |
| mixed valid + blank source set | 200 + both written | 400 + complete target snapshot unchanged | green characterization; red patch |

Canonical `user_selection.min_rep_range` and `max_rep_range` are `NOT NULL`; SQLite also coerces
numeric-looking strings under INTEGER affinity. The `None` and raw numeric-string cases therefore
use a capturing `DatabaseHandler` at the export service seam. No test alters or recreates the
schema to manufacture those inputs.

## 6. Export, scanner, and restore agreement

Agreement means the same blank disposition and canonical reason, not identical batch semantics:

- export rejects the complete source set with HTTP 400 and writes no new log row;
- `scan_export_bounds()` reports the same row and reason used to annotate that response;
- restore remains HTTP 200 and keeps its existing per-item policy, restoring valid items while
  reporting blank items in `data.invalid`.

The analysis scanners remain separate: their per-field `allow_null=False` predicate already
reports blanks, and their ADR-010 behavior for numeric inversion remains unchanged. The existing
`TestScanExportBounds.test_mirrors_allow_null_true` explicitly pins the defect and must be replaced
in Gate 1, not retained beside a contradictory assertion.

## 7. Executable evidence

Fixture state for every pytest observation:

- the session schema template is built with `run_all_initializers(force_base=True)`;
- each test receives a fresh copy at its own `tmp_path`;
- `TESTING=1`, SQLite DELETE journal mode, and empty application tables precede the named seed;
- no test reads or writes the worktree's runtime `data/database.db`.

Commands and exact results on the base above:

| Layer | Command | Result |
|---|---|---|
| pre-existing controls | selected export/scanner/restore nodes | `14 passed in 2.16s` |
| new characterization | `pytest -q tests/test_export_blank_rep_bounds_gate0.py` | `12 passed in 1.44s` |
| intended red contract | `pytest -q tests/test_export_blank_rep_bounds_contract_red.py` | `4 failed in 0.64s` |
| focused export/restore | five relevant files | `174 passed in 16.69s` |
| adjacent Python/API | workout-plan, workout-log, priority-0 API | `154 passed in 17.92s` |
| full Python suite | `pytest tests/ -q` | `3233 passed, 2 skipped in 219.12s` |
| generated inventory | `python scripts/generate_test_inventory.py --check` | up to date; `2913` deterministic nodes across `126` files |
| blocking Python lint | repository Flake8 `E9,F63,F7,F82,F811,E711,E712,F401` gate | `0` |
| Python type check | `npx --no-install pyright@1.1.410` | `0 errors, 0 warnings, 0 informations` |
| patch hygiene | `git diff --check` | clean |

The documented `-n 8 --dist loadfile` command could not run because the shared environment lacks
`pytest-xdist` (`unrecognized arguments: -n --dist`). The documented serial diagnostic form was
used instead and is the full-suite result above.

The local, gitignored red artifacts are:

- `artifacts/blank_null_rep_bounds_gate0/intended_contract.patch`
- `artifacts/blank_null_rep_bounds_gate0/red-test-output.txt`

Apply the patch at repository root to recreate the four intended-contract failures. It adds tests
only and passes `git apply --check` on this branch.

## 8. Gate-1 implementation boundary

Likely production files, to be confirmed in a separately authorized Gate-1 plan:

- `utils/workout_validation.py` — express null acceptance independently from blank acceptance;
- `utils/export_service.py` — select the stricter blank policy at this boundary;
- `utils/rep_range_integrity.py` — reproduce that exact export predicate.

Likely test files:

- `tests/test_exports.py` or the dedicated Gate-0 characterization file;
- `tests/test_rep_range_integrity.py`;
- optionally a narrow restore-fuzz extension for whitespace agreement.

Expected non-files: `routes/exports.py`, `utils/program_backup.py`, response helpers, frontend
code, schema/migration files, workflows, baselines, and branch-protection configuration.

A global change that makes `allow_null=True` reject blanks is unsafe: scored workout-log fields
use blank and null as clear operations. Dropping `allow_null=True` at export is also wrong because
it rejects actual `None`. Gate 1 needs an independently selectable blank policy.

## 9. Independent review findings

Three read-only reviewers inspected the same commit; only the manager wrote:

1. **Request/validation:** confirmed the no-payload boundary, exact envelope, validator order,
   scanner test that currently pins blank acceptance, and the unsafe global-change options.
2. **Persistence/atomicity:** confirmed full-set prevalidation, original-value TEXT persistence,
   the distinction between validation atomicity and unexpected insert-error atomicity, and why
   literal no-filesystem-write language would be false because of logging/WAL behavior.
3. **Test matrix:** confirmed the required blank/whitespace/None/numeric/inversion/mixed cases,
   the need for a fake source on `None` and numeric strings, and restore's intentionally different
   per-item batch policy.

No reviewer edited files or ran a mutating application flow.

## 10. Explicit non-goals

- No production validator, service, route, scanner, restore, or handler change.
- No migration, schema constraint, `CHECK`, backfill, or malformed-schema fixture.
- No silent blank-to-null conversion, trimming, rep-bound swap, or defaulting.
- No response-envelope redesign.
- No general export transaction refactor.
- No workflow, baseline, branch-protection, frontend, or restore-policy change.
- No implementation merge under this packet.
