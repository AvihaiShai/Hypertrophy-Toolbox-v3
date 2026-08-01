# app.py Review Plan — DRAFT (brainstorming)

**Status:** DRAFT — not approved for execution. This document exists to mature the plan
through owner review before any code changes.
**Origin (2026-08-01):** started as a cross-check of an external (Codex) review of `app.py`
whose content was lost in transit; the owner then directed an independent review instead.
**Verification (2026-08-01):** F1–F3 were confirmed **empirically** by importing the real
`app.py` app object with `DB_FILE` pointed at a scratch database (the `explicit-override`
branch of `prepare_runtime_database()` guarantees the real DB is untouched) and firing
requests through `test_client()` with `DEBUG=False, TESTING=False`. Observed outputs are
quoted per finding.
**Cross-verification (2026-08-01, Codex):** an independent Codex review reproduced F1–F3
with the same method and confirmed them. It also raised six corrections (F4 inventory,
F5 coverage claim, F7 overstatement, F1-fix header preservation, F3 wording, F6
qualifications) — each was re-verified against the source and is folded in below.

---

## 1. Confirmed findings (evidence-verified)

### F1 — Generic `Exception` handler turns 405 (and any unhandled HTTP error) into 500 — **bug (CONFIRMED empirically)**

```
GET /export_to_workout_log            -> 500  "<title>Internal Server Error</title>..."
GET /export_to_workout_log  (as XHR)  -> 500  {"error":{"code":"INTERNAL_ERROR",...}}
```
Both should be 405. Each request also logs a full "Unhandled exception" stack trace.

In Flask 3.x, a handler registered for `Exception` also catches `werkzeug.HTTPException`
subclasses unless it re-raises them. The registered coverage today:

| Status | Handler | Where |
|---|---|---|
| 400, 422, 500, `APIError` | `register_error_handlers()` | `utils/errors.py:130-207` |
| 404 | `handle_404` | `app.py` |
| **everything else (405, 403, 413, …)** | **`handle_exception`** → logged as unhandled exception with stack trace, returned as **500** | `app.py` |

Most reachable case: any GET against a POST-only route (405). **Proof of divergence:**
`tests/test_exports.py:345-349` asserts `GET /export_to_workout_log` → 405 and *passes*,
because the conftest test app registers no error handlers at all — the real app returns
500 for that exact request. Pytest cannot see this bug (see F7).

**Contradictory test expectations (found in Codex round):** the suite currently encodes
*both* behaviors. `tests/test_exports.py:345-349` asserts GET-on-POST-only → **405**
(passes only because the conftest app lacks the handlers), while
`tests/test_priority7_error_handling.py:193-198` — a separate fixture that hand-copies
`app.py`'s handler layering — asserts an unrecognized HTTP error (418) → **500**, i.e. it
enshrines the buggy behavior as expected. Fixing F1 must deliberately update the
priority-7 test; that is a documented-behavior change, not a silent regression.

**Proposed fix:** guard `handle_exception` with
`if isinstance(e, HTTPException): ...` — but the fix must preserve, per Codex's
(correct) requirement:
1. the original **status code**;
2. exception-specific **headers** — a bare conversion through `error_response()` would drop
   `Allow` on a 405 (plain `return e` keeps them; a JSON negotiator must copy them);
3. the standard JSON envelope for XHR/API requests vs. Werkzeug/HTML for browser requests.

Preferred shape: a single generic `HTTPException` negotiator (not a 405-only handler) that
returns `e` for browser requests and, for XHR, builds the JSON envelope **and copies
`e.get_response().headers`** (at minimum `Allow`).

### F2 — `"404" in str(e)` misroutes genuine errors — **bug (CONFIRMED empirically)**

```
route raising ValueError("bad value 4041")  -> 404  "<title>Not Found</title>..."   (should be 500)
route raising ValueError("plain boom")      -> 500  (control, correct)
```

`handle_exception` starts with `if isinstance(e, Exception) and "404" in str(e): return handle_404(e)`.
Real `NotFound` never reaches this line (the code-registered 404 handler wins first), so the
branch fires **only** as a misfire: any exception whose message happens to contain "404"
(`ValueError("bad value 4041")`) renders the Not Found page instead of a 500.
`isinstance(e, Exception)` is also always true here.

**Proposed fix:** delete the branch entirely once F1's `isinstance(e, HTTPException)` guard exists —
it subsumes the legitimate purpose.

### F3 — `clear_trailing` drops query strings and breaks trailing-slash POSTs — **minor bug + redundancy (CONFIRMED empirically)**

```
GET  /workout_plan/?x=1          -> 302 Location: /workout_plan          (?x=1 dropped)
POST /export_to_workout_log/     -> 302 Location: /export_to_workout_log (clients re-issue as GET)
```

`redirect(rp[:-1])` (302):
- discards `request.query_string` (`/workout_plan/?x=1` → `/workout_plan`, param lost);
- a 302 on POST makes clients re-issue as GET, so `POST /path/` silently becomes a GET.

Wording corrected per Codex: the hook is not "shadowed by" `strict_slashes = False` — it
runs *first* and actively **counteracts** it, redirecting requests that permissive routing
would have served directly. The hook is unnecessary for route reachability: the conftest app
sets `strict_slashes = False`, has no `clear_trailing`, and the suite passes. That is
compatibility evidence (nothing in the app's own JS/tests needs the redirect), not proof no
external client relies on canonical redirects — acceptable risk for a local single-user app.

**Proposed fix (preferred):** delete the `clear_trailing` before_request hook.
Alternative if a canonical-URL redirect is genuinely wanted: preserve the query string and use 308.

### F4 — 1-year static cache + unversioned asset URLs = stale CSS/JS after a frozen-build upgrade — **risk**

Frozen builds set `SEND_FILE_MAX_AGE_DEFAULT = 31536000` (the comment says "compression
hints", which is wrong — it is static-file max-age). The caching policy is **mixed and
inconsistent** (inventory corrected in the Codex round — the first pass undercounted):

- **Unversioned (stale-after-upgrade risk):** all 8 global CSS bundles + route CSS bundles,
  and several first-party scripts (`global-error-handler.js`, `darkMode.js`,
  `accessibility.js`, page modules without busters).
- **Per-render random `?v={{ range(1, 1000000) | random }}` (defeats caching entirely):**
  four globally loaded scripts in `base.html:281-288` (`app.js`, `table-responsiveness.js`,
  `filter-view-mode.js`, `exercise-video-modal.js`) plus three page modules
  (`body_composition.html:219`, `session_summary.html:213`, `weekly_summary.html:226`).

**Proposed direction:** one app-version-derived `?v=` (context processor exposing the app
version) applied to all first-party static links; remove the three random busters. Needs its own
small packet — touches templates, not just `app.py`.

### F5 — the `/erase-data` confirm guard is regression-tested **nowhere** (corrected — worse than first assessed)

The real route requires `confirm == "ERASE_ALL_DATA"` and snapshots first; the conftest twin
(`tests/conftest.py:105-119`) does neither. The first pass claimed the confirm contract was
"covered by E2E" — **Codex refuted this and the refutation verifies**:
`e2e/erase-flow.spec.ts` tests only the happy path (the UI always sends the correct token via
`static/js/welcome.js:24`); it would still pass if the server-side guard were deleted. No test
anywhere submits a missing/invalid token. Pytest tests even POST `/erase-data` without a body
and expect success, because they hit the guard-less conftest twin.

**Upgraded proposal:** add a direct pytest for the guard (400 on missing/wrong `confirm`)
against the real handler once F7's shared registration exists — not merely "mirror or document".

### F6 — Cosmetic / dead code (bundle into one no-behavior-change cleanup)

- `if hasattr(e, '__class__')` in `handle_exception` — always true.
- Duplicate local imports: `make_response` (twice inside handlers; already imported at top),
  `redirect, request` inside `clear_trailing` (moot if F3 deletes the hook).
- `from utils.errors import success_response` inside `erase_data` — move to the top-level
  `utils.errors` import line.
- Comment "Handle SIGTERM (Ctrl+C)" — Ctrl+C is SIGINT; both are registered, comment is wrong.
- `format_datetime(value, format=...)` shadows the `format` builtin. *Qualification (Codex):
  renaming is internally safe — both template callers (`workout_log.html:230`,
  `progression_plan.html:80`) pass the format positionally — but would break any out-of-repo
  caller using `format=`. Low stakes; rename only inside the F6 cleanup packet.*
- *Qualification (Codex, accepted):* the stderr `print` in `handle_exception` fires for **every**
  unhandled exception, not only export routes as its comment claims, and duplicates the logger
  traceback. Reclassified from "intentional, keep" to "revisit in F6": either scope it to the
  stated purpose or delete it and rely on `logger.exception`.

### F7 — handler coverage exists only via **hand-copied duplicates**, never the real registration code (reworded per Codex)

The first pass overstated this as "pytest-invisible". Precise state:

- The shared conftest app registers blueprints only — no error handlers, no `clear_trailing`.
- `tests/test_priority7_error_handling.py:17-80` builds a separate `error_app` that calls the
  real `register_error_handlers()` but then **hand-copies** `app.py`'s 404 and catch-all
  handlers. So F1's behavior *is* exercised — through duplicated logic that can silently
  drift from `app.py`, and which currently asserts the buggy 500 outcome (line 193).
- F2 (`"404" in str(e)`) and F3 (`clear_trailing`) are covered nowhere: the hand-copied
  catch-all omits the string check, and no fixture installs the hook.

**Proposed fix (sharpened):** extract handler/hook registration from `app.py` into a shared
function; have `app.py` and `test_priority7_error_handling.py`'s fixture call it (killing the
hand-copy). Per Codex's caution, do **not** bolt the catch-all onto the shared conftest `app`
fixture — a global catch-all under `TESTING=True` would mask unexpected exceptions the rest of
the suite should surface. Use a dedicated production-like fixture instead. Regression tests:
405 stays 405 (+ `Allow` header), "404"-in-message stays 500, XHR vs HTML negotiation,
erase-data confirm guard (F5).

---

## 2. Looks wrong, is intentional — do NOT "fix" (pre-empting external review noise)

| Item | Why it stays |
|---|---|
| Module-level DB migration/seeding at import time | Load-bearing startup order (CLAUDE.md §2); tests deliberately never import `app.py` |
| Per-line `# noqa: E402` instead of file-level | flake8 7.x treats file-level noqa as blanket — would drop the F401/F811/E711/E712 gate (header comment in `app.py`) |
| Seeding/catalog upgrade not in `run_all_initializers()` | Test suite initializes empty schemas on purpose |
| ~~`print` to stderr in `handle_exception`~~ | **Moved to F6** (Codex round): it fires for every unhandled exception, not just export routes, and duplicates the logger traceback |
| `FLASK_DEBUG` default mismatch (`app.py` `'0'` vs `database.py` `'1'`) | Documented safe outcome in `utils/CLAUDE.md` (non-debug Flask + conservative journal mode) |
| `use_reloader` off by default | WAL-corruption avoidance, documented |
| ProxyFix on a localhost app | Harmless locally; app is local-first by non-goal. Optional: drop it, but zero urgency |

---

## 3. Codex cross-verification round — RECONCILED (2026-08-01)

Codex ran the verification prompt (`artifacts/CODEX_VERIFICATION_PROMPT.md`), independently
reproduced F1–F3 with the scratch-DB method, and raised 6 corrections. Disposition — every
one was re-verified against the source before acceptance:

| Codex point | Verdict | Folded into |
|---|---|---|
| F7 overstated — `test_priority7_error_handling.py` hand-copies the handlers and asserts 418→500 | **Accepted** (verified lines 17-80, 193-198) | F1 + F7 rewritten |
| F4 buster inventory missed 4 global scripts in `base.html:281-288` | **Accepted** (verified; first grep was truncated) | F4 rewritten |
| F5 "covered by E2E" is false — `erase-flow.spec.ts` is happy-path only | **Accepted** (verified spec) | F5 rewritten, proposal upgraded |
| F1 fix must preserve `Allow`/exception headers; prefer generic negotiator | **Accepted** | F1 proposed fix |
| F3 "shadowed" wording backwards | **Accepted** | F3 reworded |
| F6: `format=` rename qualification + stderr print fires for all exceptions | **Accepted** (verified both template callers are positional) | F6 + Section 2 |

---

## 4. Proposed packet split (once matured)

| Packet | Contents | Risk | Gate |
|---|---|---|---|
| P1 | F1 + F2 + F7: shared handler registration (also adopted by the priority-7 fixture, killing its hand-copy), `HTTPException` negotiator preserving status + `Allow`/headers + XHR JSON envelope, delete the `"404" in str(e)` branch, new regression tests. **Must deliberately flip `test_priority7_error_handling.py:193` from 500 to the correct status** — that is a documented-behavior change requiring migration notes | Low-medium — status codes change on currently-wrong paths (500→405 etc.); audit `e2e/error-handling.spec.ts`, `api-integration.spec.ts`, and all of `test_priority7_error_handling.py` first | `/verify-suite` |
| P2 | F3 (delete `clear_trailing`) | Low — conftest proves route reachability without it; scan E2E for trailing-slash URLs first | pytest + smoke-navigation E2E |
| P3 | F6 cleanup (now incl. stderr print decision) | None (no behavior change except removing duplicate stderr traceback) | pytest |
| P4 | F4 asset-cache policy: one app-version-derived `?v=` for all first-party CSS/JS; remove all 7 random busters | Medium — touches `base.html` + 3 templates; frozen-build verification needed | `/verify-suite` + packaged smoke |
| P5 | F5 confirm-guard pytest (missing/wrong `confirm` → 400) against the real handler — depends on P1's shared registration | None | pytest |

Per CLAUDE.md's refactor invariant: P1 changes API response *status codes* on paths that are
currently wrong — PR description must carry migration notes.

## 5. Open questions for the owner

1. F3: delete `clear_trailing` outright, or keep a query-preserving 308 canonicalizer?
2. F4: is an app-version cache-buster acceptable, or is there an existing version constant to reuse?
3. P1 flips `test_priority7_error_handling.py:193` (418 → 500 becomes 418 → 418): confirm the
   500-for-unrecognized-HTTP-errors behavior was never *intentionally* specified — the test
   name ("later exception handler owns unrecognized http errors") reads as characterization
   of the layering, not as a product decision, but the owner should confirm.
4. Priority relative to the active WP4.4 i→j→k CSS arc — this plan should not preempt it.
