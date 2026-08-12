# Pyright burn-down packet — `routes/volume_splitter.py` `reportPossiblyUnboundVariable`

*Continuous track — pyright baseline burn-down (`docs/REFACTOR_PLAN.md` §"Continuous
track"). One file, one tightly coupled diagnostic family, structure-only.*

Branch `wt/pyright-volume-splitter`, worktree
`D:\development\Hypertrophy-Toolbox-v3-main-pyright-volume-splitter`, created with
`scripts/new-worktree.ps1 -Task pyright-volume-splitter -Seed empty` and
fast-forwarded to `origin/main` @ `e18d546` before any measurement. Planning size:
**Medium** (`docs/ai_workflow/QUALITY_GATE.md` §Plan-stage routing) — bounded, known
contracts, single route file, no schema or calculation surface. Gate 0 is waived:
requirements and non-goals were fully specified by the owner.

---

## 0. Objective

Eliminate exactly the four existing `reportPossiblyUnboundVariable` diagnostics in
`routes/volume_splitter.py` without changing runtime behavior, API contracts, database
schema, calculations, or error handling.

### Non-goals

- No change to endpoint behavior, response envelopes, or HTTP status codes.
- No change to validation order, exception handling, or logging.
- No suppression: no `cast`, no `Any`, no `# type: ignore`, no assertion added merely
  to silence Pyright, no rule disablement, no baseline-only edit.
- No opportunistic fixes to other diagnostics or other files.
- No change to the other six route handlers in the file.

---

## 1. Exact diagnostic identity

**Pyright version — pinned to CI.** `.github/workflows/ci.yml:826` runs
`npx pyright@1.1.410`, and `ci.yml:778` records that the committed baseline was
generated under 1.1.410. Every run in this packet uses `npx pyright@1.1.410`.

Reproduced on the unmodified branch at `e18d546` under the committed
`pyrightconfig.json` (pythonVersion 3.14, pythonPlatform Windows):

```
npx pyright@1.1.410 --outputjson
→ version 1.1.410, filesAnalyzed 220, errorCount 145, warningCount 0
```

| file | severity | rule | message | 1-based line:col | baseline count |
|---|---|---|---|---|---|
| `routes/volume_splitter.py` | `error` | `reportPossiblyUnboundVariable` | `"data" is possibly unbound` | 65:19 | 2 |
| `routes/volume_splitter.py` | `error` | `reportPossiblyUnboundVariable` | `"mode" is possibly unbound` | 67:51 | 2 |

The four instances are at **65:19** (`data`), **67:51** (`mode`), **69:28** (`data`)
and **101:80** (`mode`); the baseline keys on `(file, severity, rule, message)`, so
they collapse into two records of count 2.

Gate reproduction against the committed snapshot, **before** any edit:

```
python scripts/pyright_baseline_diff.py --current artifacts/pyright_before.json \
    --baseline docs/ci_cd_phase3/pyright-baseline.json
→ pyright baseline gate: PASS — 0 net-new diagnostics (baseline 145, current 145).
```

The pre-change multiset was additionally compared **key-by-key** against the committed
baseline through the tool's own `counts_from_diagnostics`: **equal**. The tree
therefore started clean, and every later delta is attributable to this packet.

Committed baseline `_meta` before: **145 total_diagnostics / 49 distinct_keys**
(re-derived, not assumed). Closing these four removes both records, taking the
baseline to **141 / 47**.

**The rule family is not eliminated repo-wide, and this packet does not claim it is.**
`reportPossiblyUnboundVariable` has **five** instances before the change; the fifth is
`"query" is possibly unbound` in `routes/progression_plan.py`, which is a different
file, is outside this packet's objective, and stays allowlisted. Repo-wide the family
goes **5 → 1**.

### 1.1 Scope notes — two neighbouring diagnostics that are not ours

- A path substring search for `volume_splitter` also surfaces a
  `reportAttributeAccessIssue` at `tests/test_volume_splitter_api.py:329`
  (`FaultyCursor` is not assignable to `Cursor`). Different file, different rule
  family.
- `routes/progression_plan.py` carries the fifth `reportPossiblyUnboundVariable`
  (`"query" is possibly unbound`). Same rule family, different file — and the burn-down
  track is scoped "one file or one tightly coupled diagnostic family per WP"
  (`docs/REFACTOR_PLAN.md:1542`), with the packet brief naming the file.

Both are left untouched and stay allowlisted in the regenerated baseline. Neither is
claimed as fixed.

---

## 2. Root cause

`calculate_volume` (`routes/volume_splitter.py:50`) opens with a `try` block that binds
**three** names and an `except (TypeError, ValueError)` handler that rebinds only
**one**:

```python
    try:
        data = request.get_json() or {}                       # :52
        mode = (data.get('mode') or 'basic').lower()          # :53

        training_days = int(data.get('training_days', 3))     # :55
    except (TypeError, ValueError):
        training_days = 3                                     # :57  ← only training_days
    except Exception as e:
        logger.exception('Error calculating volume: %s', e)
        return error_response('INTERNAL_ERROR', 'Failed to calculate volume', 500)

    try:
        ...
        volumes = data.get('volumes', {}) or {}               # :65  ← "data" possibly unbound
        active_muscles = get_muscle_list_for_mode(mode)       # :67  ← "mode" possibly unbound
        requested_ranges = data.get('ranges') or {}           # :69  ← "data" possibly unbound
        ...
        suggestions = generate_volume_suggestions(..., mode=mode)   # :101 ← "mode" possibly unbound
```

Python enters an `except` clause from **any** point inside its `try` body, so on the
path where `:52` or `:53` raises `TypeError`/`ValueError` the narrow handler completes
with `data` and `mode` never bound. Control then falls through to the second `try`,
which reads both. Pyright's report is a correct model of the language: it is the
three-statement `try` body, not the annotations, that is wrong.

**The narrow tolerance was only ever meant for the `int()` conversion.** `:57`'s
`training_days = 3` restates the same default already written at `:55`
(`data.get('training_days', 3)`) — it is a "the caller sent a non-numeric
`training_days`" fallback, and it has no sensible reading as a recovery from a failed
`get_json()`.

### 2.1 What the unbound path does today

It does **not** surface as an `UnboundLocalError` to the client. `:65` sits inside the
second `try`, whose `except Exception` logs and returns
`error_response('INTERNAL_ERROR', 'Failed to calculate volume', 500)`. So the current
observable outcome of that path is **HTTP 500 with the standard error envelope** — the
same envelope the first block's own generic handler produces. This is what makes the
chosen fix contract-preserving rather than merely behavior-adjacent (§3).

The path is also, as far as could be measured, unreachable: `request.get_json()`
signals failure with `werkzeug.exceptions.BadRequest` / `UnsupportedMediaType`, both
`HTTPException` subclasses and neither a `TypeError` nor a `ValueError`, and a
non-dict or non-string payload at `:53` raises `AttributeError`. All three route to
the generic handler. **The fix does not rest on that unreachability** — §3 shows the
contract holds even if the path is entered.

---

## 3. Chosen fix, and why the contract is unchanged

Scope the narrow `except (TypeError, ValueError)` to the statement it was written for,
by nesting it:

```python
     try:
         data = request.get_json() or {}
         mode = (data.get('mode') or 'basic').lower()

-        training_days = int(data.get('training_days', 3))
-    except (TypeError, ValueError):
-        training_days = 3
+        try:
+            training_days = int(data.get('training_days', 3))
+        except (TypeError, ValueError):
+            training_days = 3
     except Exception as e:
         logger.exception('Error calculating volume: %s', e)
         return error_response('INTERNAL_ERROR', 'Failed to calculate volume', 500)
```

**4 insertions / 3 deletions in one file.** No statement was added, removed, reordered
or rewritten; one existing handler changed which statements it guards. Every name is
now bound on every path that reaches the second `try`, because the only escape from the
outer `try` is the `return` in its generic handler — control-flow narrowing, not a
declaration or a cast.

### Path-by-path equivalence

| Path | Before | After |
|---|---|---|
| Valid body, numeric `training_days` | inner statements all succeed → 200 | identical — nesting is inert when nothing raises |
| Valid body, non-numeric `training_days` (`"abc"`, `[]`, `None`) | `int()` raises → `training_days = 3`; `data` and `mode` keep their parsed values → 200 | identical — the same handler, now the inner one |
| Body is not a JSON object (`[1,2,3]`, `"x"`, `5`) | `:53` raises `AttributeError` → generic handler → **500** `INTERNAL_ERROR` | identical — same generic handler, same log call |
| Missing / undecodable JSON | `get_json()` raises `HTTPException` → generic handler → **500** `INTERNAL_ERROR` | identical |
| `TypeError`/`ValueError` from `:52`–`:53` (unreachable, see §2.1) | narrow handler sets `training_days = 3`; `data`/`mode` unbound → `UnboundLocalError` at `:65` → second block's `except Exception` → **500** `INTERNAL_ERROR` | generic handler at `:61` → **500** `INTERNAL_ERROR`, same envelope and same `logger.exception('Error calculating volume: %s', e)` call. Only the *logged exception object* differs (the original `TypeError` instead of the derived `UnboundLocalError`) — same logger, same level, same message template, same traceback emission. |

Nothing else in the packet's surface moves:

1. **No calculation change.** The status loop, `sets_per_session` rounding, range
   sanitization, `generate_volume_suggestions` call and `success_response` payload keys
   are untouched; the second `try` block is byte-identical.
2. **No response-contract change.** Both envelopes (`success_response` /
   `error_response('INTERNAL_ERROR', 'Failed to calculate volume', 500)`) and both
   status codes are unchanged, on every path in the table.
3. **No validation-order change.** Statements execute in the same order.
4. **No signature, blueprint, route-decorator, import or schema change.** The other six
   handlers in the file are untouched.

### Rejected alternatives

| Alternative | Why rejected |
|---|---|
| Pre-initialize `data = {}` / `mode = 'basic'` above the `try` | Turns the §3 row-5 path from a 500 into a **200 with empty results** — a real contract change on an error path, defensible only by leaning on the unreachability argument the fix is meant not to need. |
| Bind `data = {}` / `mode = 'basic'` **inside** the narrow handler | Actively wrong: on the *live* non-numeric-`training_days` path it discards the caller's real `mode` and `volumes`. Proven to break behavior by mutation probe B (§5). |
| Split into two sibling `try` blocks, duplicating the generic handler | Contract-equivalent, but duplicates the 3-line `except Exception` body for no gain over nesting. |
| Split, without duplicating the generic handler | A non-`TypeError`/`ValueError` exception from `int(...)` would escape as an uncaught 500 HTML page instead of the JSON error envelope — an exception-handling change. |
| Merge both `try` blocks into one function-wide `try` | Contract-equivalent and arguably tidiest, but re-indents ~45 lines of calculation code. That is a behavior refactor disguised as a typing fix, barred by the burn-down track rule. |
| `cast` / `# type: ignore` / `assert data is not None` / rule disable / baseline-only edit | Explicitly forbidden by the packet brief; all hide the defect rather than remove it. |

---

## 4. Test plan

Two characterization tests were added to `tests/test_volume_splitter_api.py`. **No
existing assertion was weakened or modified.**

They were **required**, not optional: the three pre-existing tests that reach
`/api/calculate_volume` (`tests/test_volume_splitter_api.py:45`, `:64`,
`tests/test_ui_flows.py:472`) all send a valid integer `training_days`, so **the
`except (TypeError, ValueError)` branch this packet restructures had no coverage
anywhere in the repository**, and neither did the non-object-body path through the
generic handler. Restructuring an uncovered branch on an unpinned contract is exactly
the case the brief's "only if needed to prove behavior preservation" clause is for.

| Test | Pins |
|---|---|
| `test_calculate_volume_non_numeric_training_days_keeps_the_rest_of_the_payload` | The live narrow-handler path: `training_days: "not-a-number"` → **200**, `training_days` falls back to 3 (`12 / 3 == 4.0` in `sets_per_session`), **and** `mode: "advanced"` plus `volumes` survive the fallback (the advanced-only key `lats` is present, the basic key `Chest` is not). |
| `test_calculate_volume_non_object_body_returns_the_internal_error_envelope` | The generic-handler path: a JSON array body → **500** with `INTERNAL_ERROR` / `Failed to calculate volume` in the standard error envelope. |

**Both were written and run against the unmodified route first, and both passed**
(`14 passed`) — they characterize pre-existing behavior rather than describe the new
code.

---

## 5. Mutation probes

The tests were proven to discriminate, not merely to pass:

| Probe | Mutation | Result |
|---|---|---|
| **A** | Delete the narrow fallback entirely (`int()` raises straight into the generic handler) | `test_..._keeps_the_rest_of_the_payload` **FAILS** — `ValueError: invalid literal for int()` → 500 instead of 200. `1 failed, 13 passed` |
| **B** | The rejected alternative: rebind `data = {}` / `mode = 'basic'` inside the narrow handler | `test_..._keeps_the_rest_of_the_payload` **FAILS** — `assert lats_result is not None` → `None`, because `mode` reverted to basic. `1 failed, 13 passed` |

The fixed file was restored from a pre-probe copy afterwards and re-verified: diff back
to 4 insertions / 3 deletions, `14 passed`, and the post-restore full pyright run is
multiset-identical to the pre-probe one.

---

## 6. Gates and measured results

Derived from `docs/ai_workflow/QUALITY_GATE.md` (Route / API row: `routes/**` → route
pytest target + blueprint-registration coverage; `code-reviewer`, and **no**
`product-risk-reviewer` since no response shape changes) unioned with the burn-down
track gate in `docs/REFACTOR_PLAN.md:1546` ("zero net-new diagnostics, lower count,
focused tests, then full pytest").

| Gate | Command | Result |
|---|---|---|
| Pre-change reproduction | `npx pyright@1.1.410 --outputjson` on the unmodified branch | 145 / 49 — **multiset-equal to the committed baseline** |
| Focused pyright (before) | `npx pyright@1.1.410 routes/volume_splitter.py --outputjson` | 4 `reportPossiblyUnboundVariable` |
| Focused pyright (after) | same | **0 diagnostics in the file** |
| Diff shape | `git diff --stat -- routes/volume_splitter.py` | **4 insertions / 3 deletions**, one hunk at `:52–61` |
| Whitespace | `git diff --check` | clean, exit 0 |
| Net-new gate vs the **committed** baseline, pre-regeneration | `scripts/pyright_baseline_diff.py --current artifacts/pyright_after.json --baseline docs/ci_cd_phase3/pyright-baseline.json` | **PASS**, 0 net-new, 145 → 141 |
| Multiset delta, key-by-key | tool's own `counts_from_diagnostics` | exactly `2 → 0` on `"data"` and `2 → 0` on `"mode"`; **no other key moved; no key increased** |
| Baseline regeneration | `scripts/pyright_baseline_diff.py --current artifacts/pyright_final.json --baseline docs/ci_cd_phase3/pyright-baseline.json --write-baseline` | `_meta` **141 / 47**; `git diff` = the two records removed + the two `_meta` counts, nothing else |
| CI gate re-simulated on the committed tree | `scripts/pyright_baseline_diff.py` vs the regenerated baseline | **PASS**, 141 == 141 |
| Focused pytest | `tests/test_volume_splitter_api.py tests/test_volume_progress.py tests/test_ui_flows.py tests/test_volume_taxonomy.py tests/test_pyright_baseline_diff.py` | **83 passed** |
| flake8 blocking set (`ci.yml:110`) | `flake8 <changed files> --select=E9,F63,F7,F82,F811,E711,E712,F401` | **0**, exit 0. The measure-only 127-col pass reports 6 pre-existing `E302`s in `routes/volume_splitter.py`'s route decorators and none from this diff; longest added line is 90 chars |
| Full pytest | `.venv/Scripts/python.exe -m pytest tests/ -q` | **2640 passed, 2 skipped** in 198.80s, exit 0 (see §6.1 on the runner) |
| Test Inventory Drift | `scripts/generate_test_inventory.py --check` → regenerate → re-check | pytest nodes **2318 → 2320**, `test_volume_splitter_api.py` **12 → 14**; Playwright counts unchanged (611 / 33 / 478); re-check "up to date" |

### 6.1 The recommended parallel pytest command is not runnable in this venv

`docs/MASTER_HANDOVER.md`'s Current State block recommends `-n 8 --dist loadfile` as
the fast lane. **`pytest-xdist` is not installed in `.venv`**
(`ModuleNotFoundError: No module named 'xdist'`; pytest 9.1.1). Installing it would
write into the shared `.venv` that every worktree junctions to, which is outside this
packet's scope, so the full gate was run with CLAUDE.md §3's documented serial command
instead. Recorded here because the handover's recommendation reads as if it were
available.

### E2E

**No E2E is derived from the changed path.** `QUALITY_GATE.md:26` routes `routes/**`
to route pytest, and the change has no template, JS, CSS or response-shape effect. On
the merits, `e2e/volume-splitter.spec.ts` and `e2e/api-integration.spec.ts:638` drive
`/api/calculate_volume` only with a valid numeric `training_days`, so they cannot reach
the restructured branch. The two new pytest cases are the coverage that branch has.

### Shared-path and claim declarations

- `docs/ci_cd_phase3/pyright-baseline.json` is contended between concurrent pyright
  packets. Checked before editing: no live claim on it in any worktree's
  `MASTER_HANDOVER.local.md` / `WORKSTREAM_OWNERSHIP.local.md`, and the single open PR
  (#327) touches only `docs/LEFTOVERS_BY_PRIORITY.md` and
  `docs/WORKTREE_CLEANUP_PLAN.md`.
- `docs/MASTER_HANDOVER.md` is a **never-claimed shared path**
  (`WORKSTREAM_OWNERSHIP.md:33`). This packet **does not edit it**.
- Also explicitly not edited: `docs/REFACTOR_PLAN.md`, `docs/LEFTOVERS_BY_PRIORITY.md`,
  any CSS or visual artifact, `utils/volume_splitter_service.py`,
  `utils/volume_taxonomy.py`.

### PR description obligation

`CLAUDE.md` §1 "Refactor invariant" requires migration notes in the PR description for
any change to distribute-workflow behavior. Since §3 proves there is no delta, the PR
description says so explicitly rather than leaving it implicit.

---

## 7. Expected vs measured

| Measure | Before | After |
|---|---|---|
| `reportPossiblyUnboundVariable` in `routes/volume_splitter.py` | 4 | **0** |
| `reportPossiblyUnboundVariable` repo-wide | 5 | **1** — the surviving instance is `routes/progression_plan.py`, out of scope (§1.1) |
| Baseline `_meta.total_diagnostics` | 145 | **141** |
| Baseline `_meta.distinct_keys` | 49 | **47** |
| Any other diagnostic key or count | — | **unchanged** |
| Runtime behavior, response envelopes, status codes, calculations, DB | — | **unchanged** |

---

## 8. Recorded, deliberately not acted on

- **`tests/test_volume_splitter_api.py:329` `reportAttributeAccessIssue`** — the
  `FaultyCursor` / `Cursor` mismatch in the fault-injection fixture. Different file,
  different rule family, still allowlisted (§1.1).
- **`get_muscle_list_for_mode()` returns the module-level taxonomy lists by
  reference** (`utils/volume_splitter_service.py:37`), as does
  `routes/volume_splitter.py:38–39`. Read-only at every current call site, so latent
  rather than live. Already inventoried by the previous burn-down packet
  (`docs/pyright_volume_progress/PLANNING.md` §4) as one surface for a future hardening
  decision; this packet does not touch it.
- **The remaining six handlers in `routes/volume_splitter.py`** each carry the same
  `try` / `except Exception` / `error_response(500)` shape. None produces a diagnostic,
  and none was edited.
