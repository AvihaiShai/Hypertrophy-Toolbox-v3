# `.d-none` visibility defect — evidence

Fixes the defect recorded as **OD-2 / FU-2** during the table-helper re-audit
([PR #300](https://github.com/avihay1989/Hypertrophy-Toolbox-v3/pull/300)): the
`/volume_splitter` Distribution and AI Suggestions cards rendered on first paint despite
carrying `d-none`.

Base commit `f8988f9`. Branch `wt/dnone-visibility`, isolated worktree, probe server on
port **5301** — verified by command line to be this checkout, never port 5000.

---

## 1. Root cause

`scss/custom-bootstrap.scss:34` imported `bootstrap/scss/utilities`, which only **defines**
the `$utilities` map. The classes are emitted by `bootstrap/scss/utilities/api`, which the
build never imported. **Every `d-*` class in the application has been inert for the app's
whole history** — not a `/volume_splitter` bug, a build-configuration bug with a
`/volume_splitter` symptom.

Measured before the change, on this worktree:

| Utility | Rules setting `display` | Consequence |
|---|---|---|
| `.d-none` | **1**, and it is ID-scoped — `#error-message-container.d-none` (`a11y.css:565`) | every other consumer unaffected by the class |
| `.d-flex` | **0** — the nine `.action-frame .d-flex` rules set only `gap` | 15 call sites computed `block` |
| `.d-inline-block` | **0** | `/fatigue` period `<select>` computed `block`, stretching to **1331px** at 1440 |
| `.d-lg-inline` | **0** | the `d-none d-lg-inline` pair at `base.html:213,219` did nothing |

The two reported cards, measured at four widths before the fix:

| Width | `.results-section` | `.ai-suggestions-section` |
|---|---|---|
| 375 | `block`, 343×142 | `block`, 343×70 |
| 991 | `block`, 460×141 | `block`, 460×141 |
| 992 | `block`, 460×141 | `block`, 460×141 |
| 1440 | `block`, 461×144 | `block`, 461×70 |

The Distribution card carries live **Export Volume Plan** and **Save & Activate** buttons
and an empty table; both were reachable before any split had been calculated.

`#error-message-container` was the one consumer that behaved correctly — and only because
`base.html:271` also carries an inline `style="display: none !important;"`. Someone had
already patched around the missing utility.

---

## 2. Why no gate saw it

- `e2e/volume-splitter.spec.ts:148` asserts `toHaveClass(/d-none/)` — **class-token
  presence**. It stayed green for the entire life of the defect, because the class *was*
  on the element; it simply did nothing.
- `tests/test_css_cascade_contracts.py:494` pins the same literal markup as a hook.

A class token is not a style. Both assertions are true of a class that does not exist.

---

## 3. The fix, and why it is scoped the way it is

```scss
$utilities: (
  "display": map-merge(
    map-get($utilities, "display"),
    (values: none inline)
  )
);

@import "bootstrap/scss/utilities/api";
```

Two narrowings, each measured rather than argued.

**Only the `display` utility.** The full API also emits spacing, colour, border, flex,
sizing and text utilities — hundreds of `!important` selectors this app never asked for,
each a chance to collide with the hand-written bundles.

**Only the `none` and `inline` values.** These are exactly what the defect needs:
`d-none` (12 call sites) and `d-lg-inline`, which is the other half of
`class="d-none d-lg-inline"` at `base.html:213,219`. **The pair is indivisible** —
emitting `d-none` alone would hide those two labels at every width, trading one defect for
another.

### What the wider fix would have cost, measured

The full value list was built and measured first, against a same-machine baseline
generated from the pre-change bundle through a scratch config resolving snapshots under
gitignored `artifacts/`:

| Scope | Rule heads added | Bundle | Visual captures moved |
|---|---:|---:|---|
| whole `display` utility | +83 | +3,369 B | **18 of 66** — volume-splitter ×6, **session-summary ×6, weekly-summary ×6** at 120k–564k px |
| `values: none inline` *(shipped)* | **+20** | **+665 B** | **6 of 66** — volume-splitter only |

The extra twelve come from `d-flex` activating on pages whose JS builds `d-flex` rows
(`session-summary.js:102`, `weekly-summary.js:75,91,120`). Those pages have rendered that
way for the app's entire history; changing them is an owner-reviewed visual decision with
its own baseline regeneration, not something a `.d-none` fix should carry silently.

**Both diffs are pure additions**: 0 rule heads removed — verified by parsing the built
artifact before and after, not by reading the SCSS.

Emitted by the shipped fix: **14 `.d-*` style rules**, wrapped by **6 `@media` at-rules**
(20 heads in total, which is where the `+20` above comes from — it counts at-rule heads
alongside selector rules). The 14 are `.d-none` and `.d-inline` unconditionally, plus a
`none`/`inline` pair inside each of `sm`, `md`, `lg`, `xl`, `xxl` and `print`. Counted
directly off the shipped bundle; `2 + 6×2 = 14`.

### Value order is `inline none`, matching upstream

`utilities/api` emits in list order, and between two utilities of equal specificity and
equal `!important` the **last one wins**. Upstream Bootstrap orders `inline` before
`none`, so stock `class="d-none d-inline"` resolves to `none`. This packet originally
wrote `values: none inline`, which silently **inverted** that precedence. No call site
pairs the two at the same infix, so it was latent — but it was a gratuitous divergence
from upstream, and it is now `values: inline none`.

**The swap is semantically inert, and that was measured rather than assumed.**

| Check | Result |
|---|---|
| Bundle delta | 1,031 rules before and after; **0 rules added or removed**; exactly **14 positions reordered** |
| Computed-style probe, `/workout_plan` @375px dark | **5,179 elements, 0 differences** in computed `display` or in geometry (`width/height/x/y`) |
| Same-machine capture differential | 65 of 66 identical; **`workout-plan-mobile-dark` differs** |

That one capture differs at **identical dimensions (375×9328) and a one-byte compressed
delta**, with every element's computed `display` and box geometry identical. It is
therefore a raster-level difference at byte-identical layout — the **same Chromium class**
already documented for `BYTE_GATE_EXEMPT`, whose five captures "flip between two states at
byte-identical layout". Unlike those, this one is *deterministic per bundle* (each side
reproduced its own hash across two runs), which is why it shows up as attributable in a
hash differential. **No `BYTE_GATE_EXEMPT` change is proposed** — that set is pinned as a
strict equality by `tests/test_visual_capture_contracts.py`.

**Two further win32 captures were observed flipping with the CSS held constant** across
the six generations run for this packet: `progression-mobile-light` and
`workout-plan-mobile-light`. Recorded as data for whoever regenerates the win32 corpus;
neither is a regression and neither is proposed for any exemption list.

---

## 4. Verification

`.d-none` is now a real declaration, read back from the browser's own CSSOM:

```
.d-none  ->  display: none !important   [bootstrap.custom.min.css]
.d-lg-inline -> display: inline !important  [bootstrap.custom.min.css @ (min-width: 992px)]
```

Consumer-by-consumer, before → after:

| Width | Route | Selector | Before | After |
|---|---|---|---|---|
| 375–1440 | `/volume_splitter` | `.results-section` | `block`, up to 461×144 | **`none`, 0×0** |
| 375–1440 | `/volume_splitter` | `.ai-suggestions-section` | `block`, up to 461×70 | **`none`, 0×0** |
| 375 / 991 | `/` | `.navbar .d-none.d-lg-inline` | `inline` | `none` — correct: hidden below `lg` |
| 992 | `/` | same | `inline` | `inline` — correct: shown from `lg` |
| all | `/` | `#error-message-container` | `none` | `none` — unchanged |
| all | any | `.d-flex`, `.d-inline-block` | inert | **inert, deliberately** |

The navbar rows are a behaviour change and are listed as one: those labels were visible
below `lg` only because `d-none` did nothing. Hiding them is what the markup asks for.
`nav-dropdown.spec.ts` — no longer a known red, so a failure there blocks — **passed**.

---

## 5. Regression coverage

**`tests/test_css_display_utilities_contracts.py` — 7 nodes.** The important one is
`test_no_template_uses_a_display_utility_the_build_does_not_emit`: every `d-*` token used
in `templates/**` or `static/js/**` must be emitted by a loaded stylesheet or listed in
`KNOWN_INERT` with a reason. **That contract would have caught the original defect**, and
it catches the next one.

`KNOWN_INERT` is an exact set, asserted in both directions, so it cannot rot into a
blanket exemption: a name that stops being used must be removed, and a name that starts
being emitted must be removed.

**`e2e/volume-splitter.spec.ts` — 3 new tests**, asserting visibility rather than class
tokens: both cards are `toBeHidden()` with computed `display: none` and a null bounding
box on first load; results become visible **only** after Calculate, with content; and
`.d-none` resolves to `display: none !important` in the browser's own CSSOM. The existing
`toHaveClass` test is left in place — not weakened, just no longer the only coverage.

### Red paths — 6 / 6 executed

| Violation | Contract | Result |
|---|---|---|
| remove the `utilities/api` import — the defect itself | `test_the_build_emits_the_display_utility_api` | RED |
| restore the pre-fix bundle | `test_d_none_resolves_to_display_none_important` | RED |
| drop `d-lg-inline` from the emitted set | `test_the_responsive_partner_of_d_none_is_emitted` | RED |
| add `class="d-md-flex"` to a template | `test_no_template_uses_a_display_utility...` | RED |
| add an unused name to `KNOWN_INERT` | `test_the_known_inert_list_has_no_stale_entries` | RED |
| emit `d-flex` after all | `test_the_deliberately_withheld_utilities_stay_withheld` | RED |

Tree byte-identical after every case; contracts 7 passed on restoration.

**A defect in the harness, recorded.** Its first version snapshotted only the production
files, but one red path mutates `KNOWN_INERT` inside the contracts file itself — so the
injected stale entry survived the run and left the suite red. Anything a case writes must
be snapshotted. Restores are from byte snapshots, never `git checkout --`, because this
packet's change is uncommitted and a git restore would revert the fix mid-run.

---

## 6. Gates

| Gate | Result |
|---|---|
| `tests/test_css_display_utilities_contracts.py` | **7 passed** |
| Red paths | **6 / 6** |
| `e2e/volume-splitter.spec.ts` | **30 passed** (27 existing + 3 new) |
| Chromium: `smoke-navigation`, `nav-dropdown`, `dark-mode`, `accessibility`, `summary-pages`, `volume-progress`, `ui-hardening` | **120 passed** — 115 on the scratch port plus the 5 port-bound `summary-pages` tests re-run on the default port, see below |
| Seven-surface Stylelint | **2,759 → 2,759 (+0)** — the seven surfaces exclude the generated Bootstrap artifact by design |
| `tsc --noEmit` | clean |
| Test inventory | regenerated, `--check` clean |
| **CI on the pushed branch** | **17 / 17 green**, all required contexts |
| Visual differential (same-machine, scratch snapshot path) | **6 of 66 attributable, all `volume-splitter`** — the fix itself. A 7th capture moved and was excluded by a same-CSS repeat control, see below |

### The five local failures were a hard-coded port, and they are now green

All five were `summary-pages.spec.ts` "Pattern Coverage Analysis" tests, and all five
failed with `apiRequestContext.get: connect ECONNREFUSED 127.0.0.1:5000`.

**They hard-code the port.** `summary-pages.spec.ts:297`, `:311`, `:333`, `:355`, `:372`
each call `request.get('http://127.0.0.1:5000/api/pattern_coverage')` — an absolute URL —
instead of a `baseURL`-relative path. Every local run in this packet used the scratch
config on a non-5000 port (deliberately: `playwright.config.ts` hard-codes 5000 and a
concurrent worktree owning it would certify this packet against another checkout's CSS).
So nothing was listening on 5000 and the five could only fail. That is also why the
earlier "control run on the pristine base" reproduced them exactly — the control ran on a
scratch port too, so it was measuring the port, not the base.

**Re-run on the default port they pass:** `npx playwright test e2e/summary-pages.spec.ts`
→ **20 passed (28.0s)**, the five included. Combined with the 115 from the scratch-port
run, the seven-spec set is **120 / 120**.

CSS cannot reach these assertions in any case — they read `/api/pattern_coverage` JSON and
never a computed style — so this change could not have moved them even had the port been
right.

**Pre-existing, out of scope, and worth its own packet.** Six specs hard-code
`http://127.0.0.1:5000`, so none of them is port-portable; CI never notices because it
runs the default config on 5000. Not fixed here, to keep this packet's scope narrow —
queued in [`LEFTOVERS_BY_PRIORITY.md`](../LEFTOVERS_BY_PRIORITY.md), which is where a
future packet-picker will actually look for it.

### The differential moved 7 captures; a same-CSS control excluded one as noise

Re-measured 2026-08-08 on the merged tree (win32, `PW_VISUAL_SEED=1`, scratch snapshot
path under gitignored `artifacts/`, explicit port). Two full 66-capture sets were
generated in one session differing **only** in the CSS bundle — control =
`origin/main`'s bundle (`ede5a4c9…`), candidate = this branch's (`c9f83c1e…`) — and
compared by SHA-256 per filename. A compare against the *committed* corpus would have
proved nothing: the win32 baseline set is broadly stale (58 failed / 8 passed on
unmodified `main`), so it cannot separate this change from inherited staleness.

**Result: `MOVED=7`, not 6** — the six `volume-splitter` captures plus
`progression-mobile-light`. That seventh does not have the shape of a CSS effect:
`progression-mobile-**dark**` did not move, and no other `progression` or mobile capture
moved.

**A third run settles it.** Holding the CSS constant (candidate bundle both times) and
regenerating:

| | Result |
|---|---|
| `progression-mobile-light` | **moves with the CSS held constant** → renderer nondeterminism, **not attributable** |
| all six `volume-splitter` captures | **stable under repeat**, and move only when the bundle changes → **attributable to this fix** |

So the attributable set is exactly the six `volume-splitter` captures, and that conclusion
now rests on a measured non-attribution control rather than on inspection.

`progression-mobile-light` is a **newly recorded win32 nondeterministic capture**. It is
*not* in `BYTE_GATE_EXEMPT` (that set is five `ubuntu-24.04` captures and this evidence
does **not** propose adding to it — `tests/test_visual_capture_contracts.py` pins that set
as a strict equality). Recorded here as a datum for whoever regenerates the win32 corpus:
a single flipping capture there is expected, not a regression.

### The `/volume_splitter` baselines will need regeneration

This fix changes what `/volume_splitter` renders, so its six committed captures per
platform no longer match — **that is the fix working**, not a regression. Regenerating and
reviewing them is an owner action; CI never pushes pixels. No snapshot, tolerance, mask or
retry was changed here, and `git status --porcelain e2e/__screenshots__` is empty.

---

## 7. Follow-up, measured and scoped

**`d-flex` (15 call sites) and `d-inline-block` (1) remain inert**, recorded in
`KNOWN_INERT` and pinned by
`test_the_deliberately_withheld_utilities_stay_withheld` so the narrowing cannot widen by
accident. Activating them is a one-line SCSS change — add the values back — but it moves
**session-summary ×6 and weekly-summary ×6** at 120k–564k pixels each, plus the `/fatigue`
period select from `block` to `inline-block`. It needs its own packet, its own visual
review and its own baseline regeneration.

---

## 8. Reproducing this

```bash
# probe server on an isolated port (never 5000 -- a concurrent worktree owns it)
env HT_PORT=5301 FLASK_DEBUG=0 FLASK_USE_RELOADER=0 .venv/Scripts/python.exe app.py
# and confirm the listener is THIS checkout:
#   (Get-CimInstance Win32_Process -Filter "ProcessId=$owner").CommandLine

node artifacts/dnone/probe_d_utilities.mjs --port 5301 --out artifacts/dnone/after.json

# visual differential, snapshots under gitignored artifacts/
PW_SCRATCH_PORT=5302 PW_VISUAL_SEED=1 npx playwright test \
  -c artifacts/dnone/pw-scratch.config.ts --project=chromium e2e/visual.spec.ts

.venv/Scripts/python.exe artifacts/dnone/redpath.py
npm run build:css
```
