# Local-first navigation assets — Packet A

*Owner-approved 2026-08-13 (Session 10 residual program, Packet A). Gate 0 is
granted by the authorization text; Gate 1 is pre-approved for the smallest
council-reviewed plan that stays inside the locked behavior below.*

---

## Section 0 — Requirements

### Locked owner decisions (not re-openable here)

1. Eliminate the external runtime fetches in `templates/base.html` by serving
   **Inter fonts** and **Bootstrap runtime JS** locally from tracked, licensed
   vendor assets.
2. The compiled Bootstrap CSS (`static/css/bootstrap.custom.min.css`) remains
   the primary local stylesheet. **Remove** the network-only fallback rather
   than retaining a CDN dependency — offline / packaged operation is
   authoritative.
3. Preserve visual appearance and Bootstrap **5.3.8** behavior. Update
   packaging / license / version contracts and test offline resolution.
4. **Acceptance proof:** no navigation request targets `fonts.googleapis.com`,
   `fonts.gstatic.com`, `jsdelivr`, or `cdnjs`.

### Scope derivation

Decision 4's proof is written against a **host** list, and two of those hosts
are reached from templates other than `base.html` — `cdnjs` only by Sortable on
`/workout_plan`, `jsdelivr` also by flatpickr on `/progression`. So the proof
cannot be satisfied by editing `base.html` alone.

Plan v1 stopped there, at four hosts and five assets. That was wrong, and the
way it was wrong is the packet's main lesson: the count came from
[`E2E_PERFORMANCE_PROFILE.md`](../E2E_PERFORMANCE_PROFILE.md) Finding 4, which
profiled `/workout_plan` and read `base.html`, and therefore never saw
`/volume_splitter` loading Popper and tippy.js from a fifth host. All three
council reviewers caught it independently. The settled scope — five hosts, nine
elements, four templates — is §3.

### Non-goals

*(Section 1 is Plan v1 and is superseded throughout by §3, "Plan v2 — the plan
as built". Where the two disagree, §3 is what shipped.)*

- No schema, route, API-response, or calculation change.
- No CSS authoring change. `static/css/**` and `scss/**` are untouched;
  `bootstrap.custom.min.css` is **not** rebuilt.
- No Bootstrap/library version change. Every asset is pinned at the version the
  application resolves today.
- No new visual baseline. The expected result is **no intentional pixel
  change**; a moved pixel is a finding, not a rebaseline trigger.

### Calculation surface

**None.** No file under `utils/` is touched. `effective_sets`,
`weekly_summary`, `session_summary`, `progression`, and `fatigue` are not in
the diff.

---

## Section 1 — Plan v1

### A1. Acquire and track vendor assets

| Package | Version | Source | License | Files |
|---|---|---|---|---|
| Inter | v20 (Google Fonts release) | `fonts.googleapis.com/css2` + `fonts.gstatic.com` | SIL OFL 1.1 | `inter.css` + 7 subset `.woff2` + `LICENSE.txt` + `VERSION` + `NOTICE.md` |
| Bootstrap | 5.3.8 | `node_modules/bootstrap` (the already-pinned devDependency) | MIT | `bootstrap.bundle.min.js` (+ `.map`) + `LICENSE` + `VERSION` + `NOTICE.md` |
| SortableJS | 1.14.0 | cdnjs release artifact / upstream npm | MIT | `Sortable.min.js` + `LICENSE` + `VERSION` + `NOTICE.md` |
| flatpickr | 4.6.13 | jsdelivr npm artifact (the version the unpinned URL resolves to today) | MIT | `flatpickr.min.js` + `flatpickr.min.css` + `LICENSE` + `VERSION` + `NOTICE.md` |

Layout follows the existing `static/vendor/<package>/` precedent
(`fontawesome`, `musclemap`, `free-exercise-db`): upstream `LICENSE` verbatim,
a `VERSION` file recording source URL + version + import date + **SHA-256 of
every vendored payload byte**, and a `NOTICE.md` recording attribution and any
deviation from upstream.

**Byte-identity is the no-behavior-change argument.** Bootstrap's
`bootstrap.bundle.min.js` is already proven identical between the pinned npm
package and the jsdelivr URL the template uses
(`e4fd49181388c48ec5040bd3fe66f57c29c8e67fcd8502b3354b96ec7ab47cc7`). The same
digest comparison is recorded for every other asset.

**Inter subsetting.** Google Fonts serves the requested
`wght@400;500;600;700` as **7 files, not 28** — one variable `.woff2` per
unicode subset, shared by all four weights (218,512 bytes total). All seven are
vendored rather than narrowed to `latin`: at that size, subset narrowing buys
nothing and would be the only part of the packet capable of changing a rendered
glyph.

### A2. Rewrite the local `@font-face` stylesheet

`static/vendor/inter/inter.css` is the Google-served CSS with every
`https://fonts.gstatic.com/...` `url()` rewritten to a relative
`fonts/<name>.woff2`. `font-family`, `font-style`, `font-weight`,
`font-display: swap`, and every `unicode-range` are preserved verbatim, so the
browser's subset-selection behavior is unchanged.

### A3. Template edits

| File | Line(s) | Change |
|---|---|---|
| `templates/base.html` | 11–13 | Delete both `preconnect` hints; replace the Google Fonts `<link>` with `static/vendor/inter/inter.css?v={{ app_version }}` |
| `templates/base.html` | 15 | Delete the `onerror=` jsdelivr fallback attribute; the `<link>` itself is unchanged |
| `templates/base.html` | 278 | Bootstrap bundle `src` → `static/vendor/bootstrap/js/bootstrap.bundle.min.js?v={{ app_version }}` |
| `templates/workout_plan.html` | 558 | Sortable `src` → `static/vendor/sortable/Sortable.min.js?v={{ app_version }}` |
| `templates/progression_plan.html` | 7, 182 | flatpickr CSS + JS → `static/vendor/flatpickr/...?v={{ app_version }}` |

The Inter stylesheet keeps its **position** in the `<head>` (before
`tokens.css`), so cascade order is untouched.

### A4. Cache-busting

Every template-referenced vendor URL carries `?v={{ app_version }}`, which is
the token `apply_static_cache_policy()` in `app.py` requires before granting
the frozen build's year-long `immutable` cache. The seven `.woff2` files are
referenced from *inside* `inter.css` and cannot carry a token — the same
"transitive" class `tests/test_static_cache_policy.py` already documents, and
the same treatment Font Awesome's webfonts already get: they revalidate.

### A5. Packaging

`Hypertrophy-Toolbox.spec` collects `static/**` and `templates/**` from
`git ls-files`, so tracked vendor files are staged **by construction** with no
spec edit. What the packet must do instead is *pin* them:
`tests/test_packaging_contract.py::REQUIRED_ASSETS` and
`tests/test_package_asset_staging.py`'s representative map gain entries for the
new vendor payloads, so deleting one fails the packaging contract.

### A6. Tests (authored before implementation)

New `tests/test_local_first_assets.py`:

1. **No template references an external asset host.** Scans *every* template
   for `fonts.googleapis.com`, `fonts.gstatic.com`, `jsdelivr`, `cdnjs`, and
   for any `src=`/`href=` with an absolute `http(s)` scheme other than the
   documented off-page links (the LinkedIn signature anchor). This is the
   packet's acceptance proof in its cheapest form.
2. **No network-only fallback survives.** `onerror` does not appear on the
   Bootstrap stylesheet link.
3. **Every vendored file exists and is non-empty.**
4. **Every `url()` in `inter.css` resolves to a tracked local file** and none
   is absolute.
5. **Inter declares exactly weights 400/500/600/700**, `font-display: swap`,
   and a `unicode-range` on every `@font-face`.
6. **Every vendored payload matches the SHA-256 recorded in its `VERSION`
   file** — the mechanical form of "we shipped what we said we shipped",
   independent of `node_modules` availability.
7. **Each vendored package carries an upstream license file.**
8. **The running app serves every vendored URL** (200, non-empty, correct
   content type) — offline resolution proven through Flask rather than through
   the filesystem.

E2E: a request census added to `smoke-navigation.spec.ts` (already on the
required CI path) that navigates every route and asserts **zero** requests to a
non-local origin. It is folded into that existing spec rather than added as a
new spec file, because promoting a new spec into the required list is a
four-file contract change and an explicit owner decision.

### A7. Verification

| Gate | Why |
|---|---|
| `tests/test_local_first_assets.py`, `test_packaging_contract.py`, `test_package_asset_staging.py`, `test_static_cache_policy.py`, `test_visual_capture_contracts.py` | Directly changed contracts |
| Full `pytest` | The templates row plus cross-cutting contract files |
| `smoke-navigation`, `nav-dropdown`, `dark-mode`, `accessibility` | `base.html` is the shared surface |
| `workout-plan`, `exercise-interactions`, `superset-edge-cases` | Sortable (drag reorder) |
| `progression` | flatpickr (date picker) |
| `visual.spec.ts` **compare** (`PW_VISUAL_SEED=1`), before *and* after | Font origin change — the one thing in this packet that could move a pixel. Expected: identical. **No `--update-snapshots` under any outcome.** |
| Red-path mutation | Restore each CDN URL in turn; every acceptance test must fail for its stated reason |
| Real browser `/verify` | Drag-reorder, date picker, dropdowns, modals, toasts exercised by hand with the network blocked |
| Test inventory regeneration + `--check` | Test nodes are added |

### A8. Risks

| Risk | Mitigation |
|---|---|
| A baseline was captured mid-`swap` with the fallback font; local fonts resolve faster and change the render | Visual compare before/after is a required step, not an optional one. A moved pixel stops the packet for analysis. |
| Vendored bytes differ from what the CDN served | SHA-256 recorded per file; Bootstrap's is already proven equal to the CDN response. |
| Source-map 404 in devtools after vendoring the minified bundle | Vendor `bootstrap.bundle.min.js.map` alongside it. |
| flatpickr's URL is unpinned upstream (`/npm/flatpickr` → latest) | Vendoring **pins** it at the version production resolves today (4.6.13). Recorded explicitly in `VERSION` as a deliberate pin, not a silent upgrade. |
| Packaged build misses a vendor file | Packaging contract gains explicit entries; the staging tree is digest-verified. |

---

## Section 2 — Council response matrix

Three reviewers ran against Plan v1: `architecture-reviewer`, `test-strategist`,
`product-risk-reviewer`. Every finding is dispositioned. Conservative findings
were accepted automatically per the packet's authorization.

| # | Finding | Reviewer(s) | Disposition | What changed |
|---|---|---|---|---|
| 1 | **`/volume_splitter` loads Popper and tippy.js from `unpkg.com`** — a fifth host, named in no census. Both acceptance proofs fail as written; the tempting repair is an exemption that hollows out the proof. | all three (blocking) | **accept** | Both vendored (`static/vendor/popperjs/`, `static/vendor/tippy/`) at the versions the major-pinned URLs resolved to. Scope is now 9 elements / 5 hosts / 4 templates. |
| 2 | The scope argument leans on decision 2's offline principle, which equally condemns unpkg — a reviewer accepting it has accepted a case for growing scope further. | product-risk | **accept** | Settled by taking finding 1: the principle is now applied uniformly rather than selectively. The contract is origin-shaped, so it needs no host enumeration to stay true. |
| 3 | **`tests/test_bootstrap_version_contract.py:17` goes 2 to 0 and is named nowhere.** Deleting it would drop the only link between the pinned package and the shipped runtime. | architecture, test-strategist (blocking) | **accept** | Re-pointed at the vendored artifact: `VERSION`'s version must equal `package.json`'s pin, the bundle must carry that banner, and its bytes must match the recorded digest. Strictly stronger than the URL-substring check it replaces. |
| 4 | **`tests/test_package_asset_staging.py`'s font census is a closed equality** derived from `"Font Awesome"`-prefixed keys. Seven Inter files make it 10 vs 3. | architecture, test-strategist (blocking) | **accept** | Derivation replaced with an explicit `PACKAGED_FONTS` tuple naming all ten files. The closed-inventory property — the reason the assertion is worth having — is preserved; only the false label is gone. |
| 5 | **`core.autocrlf=true` with no `.gitattributes`** — every text payload would be LF in a Linux checkout and CRLF in a Windows one, so a SHA-256 pin fails on one platform and the "same bytes as upstream" claim is false of the file on disk. | architecture (blocking) | **accept** | `static/vendor/.gitattributes` sets `-text` on the six new packages. Verified two ways: staged blob == working tree == recorded digest for all 14 payloads; and the *unattributed* `fontawesome/css/all.min.css` demonstrably differs between blob and checkout (0 vs 4 CRLF, different digests), which is the failure this prevents. Scoped to the new packages so the pre-existing three do not churn. |
| 6 | Existence-on-disk is the wrong oracle: staging is `git ls-files`, so an untracked payload passes every disk-reading test *and* Flask, and is absent only from the frozen build. | product-risk, test-strategist | **accept** | Added `test_every_vendored_asset_is_tracked_by_git`, plus all ten font paths in the packaging inventories. |
| 7 | **Nothing proves the packaged build serves these files.** `scripts/smoke_packaged_app.py` is the only frozen-build gate and its map and link sweep are `css`/`js` only. | architecture, test-strategist | **accept** | Eight vendor entries added to `ASSETS`, `/volume_splitter` added to `PAGES`, and the rendered-link sweep widened to `(?:css|js|vendor)`. |
| 8 | **No gate covers `?v=` on vendor links** — `tests/test_version.py` matches only `css/`/`js/` filenames, so dropping the token fails nothing. | architecture, test-strategist | **accept** | Two new assertions: one on template source, one on **rendered** HTML across four routes. Widening the packaged sweep also forced Font Awesome's stale `?v=5.15.4` to `?v={{ app_version }}` — a one-token fix that moves it into the frozen long cache it was silently excluded from. |
| 9 | **The E2E census can pass vacuously**: `fixtures.ts` deliberately swallows `404` and `Failed to load resource`, so a page whose vendored URLs all 404 requests nothing external and passes. A listener registered after `goto` records nothing, forever. | architecture, test-strategist | **accept** | The census asserts three things: no foreign origin, no same-origin response at or above 400, and seven specific vendored paths actually fetched. |
| 10 | **flatpickr, tippy and Sortable have no E2E coverage at all**, and their consumers are `typeof`-guarded — a broken vendoring ships green. | test-strategist, architecture | **accept, and the finding understated it** | The `Sortable.create` call is unguarded, but `fixtures.ts` also ignores `is not defined` **page errors**, so even that throw is swallowed. There was no oracle of any kind. Added four tests: flatpickr binds `#goalDate` and its CSS positions the calendar; Popper-before-tippy load order plus a bound instance; a hover showing a styled `.tippy-box`; and SortableJS exposing `create` at version `1.14.0`. |
| 11 | **Removing four per-navigation requests changes `networkidle` timing suite-wide**, so a page-affinity spec list cannot bound the risk. | architecture, test-strategist | **accept** | Gate is the full required functional set, not the eight specs v1 named. |
| 12 | The visual oracle is blind on five `BYTE_GATE_EXEMPT` captures and has no PR-time Linux signal; "expected: identical" is not executable. | architecture, test-strategist | **accept** | Oracle restated as *the failing set and its per-capture diffs are unchanged before vs after*, with `git status --porcelain e2e/__screenshots__` empty after each run. Pre-change control recorded at **66 passed, nothing written**. A confirmed-correct pixel movement escalates to the owner rather than being absorbed here. |
| 13 | The offline breakage being repaired is larger than v1 stated: the unguarded `Sortable.create` aborts `populateWorkoutPlanTable()` **before** `initializeSupersetActions()`, and `goal_date` is required and sourced only from the picker, so a progression goal cannot be *saved* offline. | product-risk | **accept** | Verified in source (`workout-plan-table.js:467` immediately precedes `:470`). Recorded as intended behavior restorations below and in the PR body. |
| 14 | **The Bootstrap bundle embeds Popper and its copyright does not survive minification** — the file's only `Copyright` is Bootstrap's. Vendoring makes us a redistributor. | product-risk | **accept** | Confirmed (exactly one `Copyright` string). `bootstrap/NOTICE.md` now names `@popperjs/core` and its notice, and points at the MIT text this repo already ships. |
| 15 | "No intentional pixel change" is true online and **false offline**: `base.css:21` is `'Inter', Arial, sans-serif`, so offline renders Arial today and Inter after. A network-enabled visual compare cannot see it. | product-risk | **accept** | Restated below as the intended offline appearance change. |
| 16 | Precedent claim overstated — `fontawesome/` has only `LICENSE.txt`, and no existing `VERSION` records a digest. The digest convention is new. | architecture | **accept** | Stated below. The license assertion accepts `LICENSE` and `LICENSE.txt`, and scans only the six new packages, so Font Awesome is not retroactively required to comply. |
| 17 | The Google Fonts CSS2 response is User-Agent negotiated, so "7 files" is not reproducible without recording how it was fetched. | architecture | **accept** | The exact UA is recorded in `inter/VERSION` with a note that an unrecognized UA returns `.ttf` with no subsetting. |
| 18 | flatpickr's source URL has no path and resolves to the package default; "same bytes" is unproven without measuring it. | architecture | **accept** | Measured: the pinned 4.6.13 artifacts are byte-identical to what both unpinned production URLs served on the import date. Same check run for Sortable (cdnjs == npm) and Bootstrap (npm == jsdelivr). Recorded per package. |
| 19 | MIME assertions are platform-fragile (`mimetypes` reads the Windows registry). | architecture, test-strategist | **accept** | No content-type assertion is made in pytest; the packaged smoke keeps its existing loose substrings and uses `None` for `.woff2`. |
| 20 | Inventory regeneration collides with open PRs #334/#335; `templates/base.html` is a de-facto shared surface. | architecture | **accept** | Inventory is regenerated canonically, never hand-merged, after rebasing onto whatever main carries at merge time. |
| 21 | `runtime_probe.mjs`'s `jsdelivrRequested` / `googleFontsOk` fields become permanent no-ops; its verdict string is pinned by a contract test. | architecture | **accept — recorded, file untouched** | Noted in `E2E_PERFORMANCE_PROFILE.md` so a later audit does not read `googleFontsOk: false` as a regression. |
| 22 | Vendored `.css` now enters the recursive CSS-audit scan at `test_css_wp4_4_layout_contracts.py:566`. | architecture | **accept — no action** | Benign: neither `inter.css` nor `flatpickr.min.css` defines a `.tbl-*` helper. Recorded so the next audit knows third-party CSS is in that surface. |
| 23 | `smoke-navigation.spec.ts` walks 9 of 11 routes, so "every route" would be false; the origin filter must not hardcode `localhost` (`test_no_playwright_source_hardcodes_an_origin`). | test-strategist, architecture | **accept** | The census iterates `Object.values(ROUTES)` — all 11 — and derives the origin from the `baseURL` fixture. |
| 24 | Fold the census into the existing full-cycle test to avoid inventory churn, or accept a new node deliberately. | test-strategist | **partially accept** | Kept as its own node. The existing test asserts a per-route selector and deliberately omits `/backup` and `/fatigue`; folding would either weaken it or force those two in. A named node also gives the packet's headline proof a legible failure. Inventory is regenerated either way. |
| 25 | Two off-page anchors exist (`base.html`, `welcome.html`), not one. | architecture, test-strategist | **accept — obsolete by design** | The scan matches only subresource tags, so anchors need no allowlist at all and none can be added later to hide a CDN. |

---

## Section 3 — Plan v2 (the plan as built)

### Scope: 9 elements, 5 hosts, 4 templates

| Template | Element | Was | Now |
|---|---|---|---|
| `base.html` | two `preconnect` hints | `fonts.googleapis.com`, `fonts.gstatic.com` | deleted |
| `base.html` | Inter stylesheet | `fonts.googleapis.com/css2` | `static/vendor/inter/inter.css` |
| `base.html` | Bootstrap CSS `onerror` | `cdn.jsdelivr.net` fallback | deleted |
| `base.html` | Bootstrap bundle | `cdn.jsdelivr.net` | `static/vendor/bootstrap/js/` |
| `workout_plan.html` | SortableJS | `cdnjs.cloudflare.com` | `static/vendor/sortable/` |
| `progression_plan.html` | flatpickr CSS + JS | `cdn.jsdelivr.net`, **unpinned** | `static/vendor/flatpickr/` |
| `volume_splitter.html` | Popper + tippy.js | `unpkg.com`, major-pinned | `static/vendor/popperjs/`, `static/vendor/tippy/` |

Font Awesome's link is unchanged except for its cache-bust token (finding 8).

### The contract is origin-shaped, not host-shaped

`tests/test_local_first_assets.py` asserts that **no template loads a page asset
from any origin but this application's**. The five retired hosts are also named
individually, but only so a regression reports itself legibly — the guarantee
does not depend on that list being complete. This is the direct lesson of
finding 1: a four-host denylist is what let a fifth host survive a CDN census.

Out of scope by construction, and therefore needing no allowlist: an `<a href>`
to an off-site page, the reference-video iframe whose `src` is assigned by
JavaScript on user action, and `http://www.w3.org/2000/svg` namespaces inside
inline data URIs.

### Behavior changes, stated rather than implied

This packet is "same bytes, different origin" **online**. Offline it is a
repair, and the repairs are user-visible:

1. `/workout_plan` — `Sortable.create()` is unguarded, so a missing library
   threw and aborted `populateWorkoutPlanTable()` before
   `initializeSupersetActions()`. Drag-reorder **and** the superset action bar
   were both lost.
2. `/progression` — `goal_date` is required and read back from the picker's own
   `selectedDates`, so a goal could not be **saved**, not merely picked.
3. `/volume_splitter` — every tooltip vanished silently.
4. Typography — `base.css:21` is `'Inter', Arial, sans-serif`. An offline
   install rendered in Arial and now renders in Inter. **This is an intended
   appearance change, and a network-enabled visual compare is structurally
   unable to see it.** The non-goal "no intentional pixel change" holds for the
   online case only.

### Verification

| Gate | Result |
|---|---|
| `visual.spec.ts` compare, `PW_VISUAL_SEED=1`, **before** | 66 passed; `git status --porcelain e2e/__screenshots__` empty |
| Full `pytest` | recorded in the PR body |
| Required Chromium functional set | recorded in the PR body |
| `visual.spec.ts` compare, **after** | oracle: failing set and per-capture diffs unchanged versus the before run; nothing written |
| Red-path battery | one mutation per acceptance claim |
| Blob-digest proof | 14/14 payloads: staged blob == working tree == recorded digest |
| Real browser check with the network blocked | drag-reorder, date picker, tooltips, dropdowns, modals, toasts |
| Test inventory | regenerated canonically, `--check` clean |
