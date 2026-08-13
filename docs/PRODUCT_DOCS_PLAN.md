# Product Documentation Suite — Plan

**Status:** EXECUTED — the owner-selected subset (D0, D2, D4, D5, D6) shipped as `docs/product/**`. §1–§7 are the original proposal and the Sol5.6 review, kept as the audit trail; **§8 is the executed plan** (Gate 0 answers, Plan v1, council findings, response matrix, Plan v2, acceptance). D1 (PRD) and D3 (TECH_DESIGN) were deliberately **not built** — see §8.5.
**Created:** 2026-08-01
**Origin:** Owner request — evaluate the six-document suite (PRD / TDD / App Flow / Design Brief / Backend Schema / Engineering Plan) against what this repo already has.

---

## 1. Assessment — what already exists vs. the six documents

The six-document advice targets greenfield projects ("write these before you build"). This repo is brownfield with a mature docs surface, so the correct move is **fill the real gaps and consolidate the rest**, not write six documents from scratch.

| Suggested doc | Current coverage | Verdict |
|---|---|---|
| **PRD** — each core feature | `CLAUDE.md` §1 (workflows, terminology, non-goals); scattered feature docs (`FILTER_VIEW_MODE.md`, `program_backups.md`, `muscle_selector.md`); per-feature `PLANNING.md` Section 0s | **Partial** — no single human-readable per-feature reference |
| **TDD** — stack, decisions, APIs, tools | `CLAUDE.md` §2; `.claude/rules/{routes,database,frontend,debugging,testing}.md`; `docs/DECISIONS.md` ADRs | **Mostly covered** — but agent-oriented and split across 7+ files |
| **App Flow** — journeys, per-button behavior | Implicit only: 501 E2E tests across 30 specs; `UI_SCENARIOS_GAP_ANALYSIS.md` is risk-focused, not flow-focused | **Genuine gap** |
| **Design Brief** — palette, typography, components, per-screen look | `CSS_OWNERSHIP_MAP.md`; WP4.1 token inventory (`CSS_PHASE4_WP4_1_TOKEN_INVENTORY.md`); `.claude/rules/frontend.md` dark-mode notes | **Genuine gap** — raw material exists, no synthesized design-system doc |
| **Backend Schema** — tables, fields, types, relationships | `.claude/rules/database.md` (schema from `utils/db_initializer.py`); `utils/schema_registry.py` is the canonical registry | **Mostly covered** — missing a relationships/ER view |
| **Engineering Plan** — small testable tasks, build order, dependencies, acceptance | The `/council-plan` skill, per-feature `PLANNING.md`, `ai_workflow/QUALITY_GATE.md`, work-packet + evidence convention | **Fully covered as a living process** — a static doc would be a downgrade |

## 2. Design constraints (why this plan is shaped the way it is)

1. **Drift is the enemy.** This repo already fights doc drift actively (`ai_workflow/DOC_RETENTION.md`, the `/status` skill). Every new doc is a standing maintenance liability, so:
   - Each new doc is **descriptive, never status-bearing** — no test counts, branch names, or "current WP" claims.
   - Each doc opens with a `Derived from:` header naming its source-of-truth code files and the rule **"on conflict, the code wins."**
   - Prefer **thin docs that link** to existing rules files over duplicating their content.
2. **Placement.** All new docs live in a new `docs/product/` folder so the suite is one coherent unit, indexed from `docs/README.md`. This respects the "Always active" retention class without bloating the docs root.
3. **Repo invariants apply.** These are docs-only packets — no code, schema, or calculation changes anywhere in this plan.

## 3. Work packets

Ordered by build order. Each is a small, independently mergeable PR.

### D0 — Scaffold and index (prerequisite)
- Create `docs/product/` with a short `README.md` explaining the suite's purpose and its anti-drift rules (the `Derived from:` convention).
- Link the folder from `docs/README.md` under a new "Product Reference" heading.
- **Acceptance:** folder exists, indexed, retention class noted (Always active).

### D1 — `docs/product/PRD.md`
- One section per core workflow (Plan, Log, Analyze, Progress, Distribute, Profile, Backup — the seven from `CLAUDE.md` §1), each with: purpose, user value, key behaviors, boundaries/non-goals, and links to the deeper feature doc where one exists.
- Source: `CLAUDE.md` §1, existing feature docs, route surface in `routes/*.py`.
- **Acceptance:** every blueprint registered in `app.py` maps to exactly one PRD section (or is explicitly listed as supporting infrastructure); non-goals from `CLAUDE.md` reproduced verbatim, not paraphrased.

### D2 — `docs/product/APP_FLOW.md` *(highest value — fills the biggest gap)*
- Per screen: entry points, primary user journey, and a table of interactive controls → triggered API call → success outcome → failure outcome.
- Source: `templates/*.html`, `static/js/modules/*.js` (`apiFetch` call sites), and the E2E spec map in `.claude/rules/testing.md` as the journey oracle.
- **Acceptance:** every screen reachable from the `base.html` navbar has a section; every documented API call grep-verified against `routes/*.py`; spot-check three flows against running app via Playwright MCP.

### D3 — `docs/product/TECH_DESIGN.md` *(thin by design)*
- Stack summary (Flask + SQLite + vanilla JS + Bootstrap SCSS), module-boundary diagram, startup sequence, response contract, env-var table — each section a short summary **plus a link** to the owning rules file or ADR. No content duplicated that `.claude/rules/*` already owns.
- **Acceptance:** no section exceeds ~15 lines before deferring to a link; every link resolves.

### D4 — `docs/product/BACKEND_SCHEMA.md`
- Table-by-table listing (fields, types, defaults) generated by reading `utils/db_initializer.py` + `utils/schema_registry.py`, plus a Mermaid ER diagram showing relationships (`user_selection` ↔ `workout_log`, superset grouping, backup tables, etc.).
- Explicitly note SQLite's actual enforcement (which FKs are real vs. by-convention).
- **Acceptance:** table list byte-for-byte consistent with the registry (verified by grep, not memory); ER diagram renders; `.claude/rules/database.md` gains a one-line pointer, loses nothing.

### D5 — `docs/product/DESIGN_BRIEF.md`
- Synthesize the WP4.1 token inventory + `CSS_OWNERSHIP_MAP.md` into: color palette (light/dark), typography scale, spacing/radius tokens, component inventory (buttons, cards, tables, badges, filters), and one short per-screen look-and-feel note.
- **Acceptance:** every named token exists in the current SCSS/CSS bundle (grep-verified); no new design decisions introduced — this documents what shipped, it does not restyle anything.

### D6 — Engineering Plan: pointer only, no new doc
- Add a short "How work gets planned and built" section to `docs/product/README.md` (from D0) linking `/council-plan`, `PLANNING.md` convention, and `ai_workflow/QUALITY_GATE.md`.
- **Rationale:** the repo's living planning process already exceeds a static engineering-plan doc; duplicating it as a snapshot would create instant drift.

## 4. Build order and dependencies

```
D0 ──► D1 ──► D2        (D2 reuses D1's feature vocabulary)
  ├──► D3               (independent after scaffold)
  ├──► D4               (independent after scaffold)
  └──► D5               (independent after scaffold)
D6 folds into D0's README or ships as a trailing one-liner PR
```

Recommended priority if not doing all: **D2 (app flow) > D5 (design brief) > D4 (schema ER) > D1 (PRD) > D3 (TDD) > D6**. D2 and D5 are the only true gaps; D4 is a cheap win; D1/D3 are consolidation conveniences.

## 5. Explicitly out of scope

- Any change to code, schema, tests, CSS, or behavior.
- Any status-bearing content in the new docs (that stays in `MASTER_HANDOVER.md` / `ACTIVE_DEVELOPMENT.md`).
- Rewriting or relocating `.claude/rules/*` — those remain the agent-facing source of truth; the product suite links into them.

## 6. Open questions for the owner (Gate 0)

1. Scope: all six packets, or only the priority subset (D2 + D5 + D4)?
2. Audience check: are these docs for the owner's own reference, for showing others, or as grounding context for AI tools? (Affects tone and depth, especially D1/D3.)
3. Should D5 wait until the three open WP4.4 owner proposals are decided, since they could change tokens/components it would document?

---

## 7. Sol5.6 review — findings, recommendations, and required actions

**Reviewer identity:** Sol5.6  
**Review date:** 2026-08-01  
**Review disposition:** **NEEDS REVISION before Gate 0 approval.** The consolidation-first strategy is sound, but the current gates can pass while producing incomplete or misleading product documentation.

### 7.1 Blocking findings and actions

| Priority | Finding | Recommendation | Required plan action |
|---|---|---|---|
| **P1** | **Gate 0 alone does not authorize packet execution.** This is a cross-cutting, multi-packet documentation suite. `docs/ai_workflow/QUALITY_GATE.md` requires Gate 0 plus a council-reviewed Gate 1 for large, ambiguous, or new-workflow work. | Use the repository lifecycle: requirements approval → `/council-plan` → revised Plan v2 → Gate 1 owner approval → packet execution. | Revise the status and build-order section so D0–D6 remain blocked after Gate 0 and become executable only after Gate 1. Link `.claude/commands/council-plan.md` rather than relying on an unlinked slash-command name. |
| **P1** | **D4 names an incomplete schema source chain.** `utils/schema_registry.py` orchestrates schema creation but does not define all fields/defaults. DDL also lives in `utils/database.py`, `utils/program_backup.py`, and `utils/catalog_upgrade.py`; post-create migrations use `ALTER TABLE`. `OWNED_TABLES_DROP_ORDER` deliberately omits some application tables and therefore is not a complete schema inventory. | Treat the runtime schema produced by the complete initializer call graph as the verification target. Read every DDL/migration owner and corroborate the result from a fresh isolated database using SQLite PRAGMAs. | Replace D4's two-file source list and “byte-for-byte consistent with the registry” acceptance criterion. Require inventory of tables, columns, types, nullability, defaults, PKs, unique constraints, indexes, FKs, and by-convention relationships using `PRAGMA table_info`, `PRAGMA index_list`/`index_info`, and `PRAGMA foreign_key_list`. Do not touch the user's runtime database. |
| **P1** | **D1's seven-workflow taxonomy omits first-class product surfaces.** Body Composition and Fatigue are registered blueprints, rendered pages, E2E-covered features, and visible navbar destinations. The “supporting infrastructure” exception could misclassify them while still passing acceptance. | Define the product taxonomy from all user-facing page routes, then separately map supporting API-only blueprints. Body Composition and Fatigue must either receive their own sections or be explicitly owned as substantial subsections of Profile and Analyze. Home/welcome must also be dispositioned. | Expand or explicitly nest the workflow list before D1 starts. Replace the blueprint-only gate with two inventories: every user-facing page route has a product section, and every registered blueprint is mapped as product surface or supporting infrastructure with a reason. |

### 7.2 Important quality findings and actions

| Priority | Finding | Recommendation | Required plan action |
|---|---|---|---|
| **P2** | **D2's acceptance check is one-way.** Proving that each documented API route exists does not prove that every real control or network call was documented. Its fixed “control → API call” shape also fails for navigation, localStorage-only controls, client-side presentation, modal state, and file downloads. | Inventory actions from the rendered templates and their loaded JavaScript dependency graph. Classify each action as API, navigation, local state, download, or presentation-only. For API actions verify route, HTTP method, request shape, response contract, and meaningful failure behavior. | Replace the D2 table schema and completeness criterion. Require every in-scope interactive control and frontend network call site to be accounted for. Replace “Playwright MCP” with named repository Playwright specs plus recorded manual spot checks; three arbitrary flows alone are not a completeness gate. |
| **P2** | **The E2E map is evidence, not a journey oracle.** Tests intentionally emphasize risk and may omit untested product intent; test counts are also status-bearing and can drift. | Use templates, loaded JS, routes, and current product behavior as primary evidence. Use E2E specs to validate documented flows and expose gaps, not to define the product by themselves. | Change D2's source wording from “journey oracle” to “validation and gap-detection evidence.” Do not copy test counts into the permanent product document. |
| **P2** | **D5's grep-only token gate cannot establish the shipped design.** A token or declaration can exist without owning any rendered result. The active WP4.4 work has specifically shown that source presence and selector matching are insufficient evidence of effective ownership. | Complete D5 only against a stable CSS baseline. Validate token definitions, live consumers, and representative computed/rendered results across light/dark modes and supported viewports. | Reconcile Gate 0 question 3 with `docs/MASTER_HANDOVER.md`: WP4.4-i is active and i → j → k is already authorized. Either defer D5 until that arc closes or pin the exact source revision and rerun the live verification before merge. Replace the grep-only acceptance criterion with declaration plus live-consumer verification. |
| **P2** | **The new suite is called “Always active” without updating the canonical retention policy.** A note in `docs/product/README.md` does not amend `docs/ai_workflow/DOC_RETENTION.md`. | Make the retention class explicit in the canonical policy so later cleanup work cannot reasonably archive the suite as completed feature documentation. | Add `docs/product/**` to the Always active row in `DOC_RETENTION.md` during D0 and link it from the new README. Because this touches `docs/ai_workflow/**`, perform the manual dry-run/self-review required by `QUALITY_GATE.md`. |
| **P2** | **D3 asks for startup and environment summaries while prohibiting duplication, and its ~15-line gate measures length rather than correctness.** | Define an intentional duplication boundary: durable human-readable synopsis is allowed; operational details remain links to canonical owners. | Replace the line-count acceptance test with content checks: every claimed invariant has an owner link, no status-bearing facts are copied, and copied tables are limited to explicitly approved durable summaries. |

### 7.3 Recommended revised gate and packet sequence

```text
Current draft
   │
   ▼
Apply Sol5.6 required revisions
   │
   ▼
Gate 0 — owner approves requirements, audience, scope, taxonomy, and D5 timing
   │
   ▼
/council-plan — architecture, test-strategy, and product-risk review
   │
   ▼
Plan v2 + response matrix
   │
   ▼
Gate 1 — owner approves the executable plan
   │
   ▼
D0 ──► D1 ──► D2
 │      
 ├──► D3
 ├──► D4
 └──► D5 only after its CSS-baseline condition is satisfied

D6 is folded into D0 and points to the repository planning workflow.
```

### 7.4 Suggested replacement acceptance criteria

- **D0:** `docs/product/**` is indexed from `docs/README.md`, classified as Always active in `docs/ai_workflow/DOC_RETENTION.md`, and its README identifies canonical sources, conflict rules, audience, and maintenance ownership.
- **D1:** every user-facing page route is represented in the product taxonomy; Body Composition, Fatigue, and Home/welcome have explicit dispositions; every registered blueprint is separately classified as a product surface or supporting infrastructure with a reason; links resolve.
- **D2:** every in-scope interactive control is recorded with its action type and outcomes; every frontend network call site maps to a route and HTTP method; dynamic URLs are checked structurally rather than by literal grep alone; named relevant Playwright specs pass and manual spot-check evidence is recorded.
- **D3:** every technical claim links to its canonical owner; durable summaries are intentionally bounded; no branch, test-count, packet-status, or other time-sensitive facts are copied into the permanent document; links resolve.
- **D4:** the documented schema matches a fresh isolated runtime schema across tables, columns, defaults, constraints, indexes, and FKs; initializer-owned migrations are included; convention-only relationships are distinguished from enforced FKs; the Mermaid diagram renders.
- **D5:** every documented token exists at the pinned baseline and has at least one verified live consumer where applicable; light/dark and representative viewport behavior is checked against computed/rendered output; the active WP4.4 arc is complete or the document is revalidated immediately before merge; no new design decision is introduced.
- **D6:** D0's README links the checked-in planning sources—especially `.claude/commands/council-plan.md`, `docs/ai_workflow/PLAN_REVIEW_TEMPLATE.md`, and `docs/ai_workflow/QUALITY_GATE.md`—rather than treating a locally available skill name as sufficient documentation.

### 7.5 Sol5.6 recommendation

Proceed with the suite after the required revisions and both approval gates. Preserve the proposed priority of App Flow and Design Brief as the highest-value user-facing outputs, but move Backend Schema ahead of Design Brief if WP4.4 remains active. D4 is not a “cheap win” under the current schema topology; estimate it as a reconciliation task that must cover all initializer and migration owners.

---

## 8. Executed plan — Gate 0 answers, council, and Plan v2

### 8.1 Gate 0 — owner decisions (2026-08-13)

The owner answered §6's three open questions and added a fourth ruling, in writing, as
Gate-0 approval **and** pre-approval of Gate 1 for the smallest council-reviewed Plan v2
that implements them plus every accepted Sol5.6 correction:

| # | Question | Owner decision |
|---|---|---|
| 1 | Scope — all six packets or the priority subset? | **Priority subset only: D0, D2, D4, D5, D6.** No duplicate PRD (D1) and no thin TDD (D3) unless the council proves a concrete missing requirement that cannot live in the selected documents. |
| 2 | Audience | **The owner and future AI agents first**, with enough clarity for an external technical collaborator. Concise, source-linked, no marketing prose. |
| 3 | D5 timing | **Proceed now.** WP4.4 is closed and the design baselines are stable. Pin the exact source revision and verify live consumers and rendering. |
| 4 | Taxonomy (Sol5.6 P1) | **Body Composition, Fatigue, and Home are first-class product surfaces**, not "supporting infrastructure". |

### 8.2 Plan v1

**Goal**: give the owner, future agents, and an external collaborator one indexed product
reference — how the app behaves screen by screen, what the database actually looks like,
and what the shipped design system is — without creating a second source of truth for
anything the code or the existing guides already own.

**Scope**

- **In**: `docs/product/README.md` (D0 scaffold + D6 pointer section), `docs/product/APP_FLOW.md`
  (D2), `docs/product/BACKEND_SCHEMA.md` (D4), `docs/product/DESIGN_BRIEF.md` (D5);
  `docs/product/**` added to the Always-active retention class in
  `docs/ai_workflow/DOC_RETENTION.md`; the suite indexed from `docs/README.md`; this §8.
- **Out**: any change to code, schema, CSS, tests, CI, or behavior. Any status-bearing content
  (branch names, PR numbers, test counts, "current WP"). Rewriting or relocating
  `.claude/rules/*`. Regenerating any visual baseline or snapshot. Editing
  `docs/MASTER_HANDOVER.md`.

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `docs/product/README.md` | new | Suite purpose, audience, canonical-source map, conflict/ownership rules, D6 planning pointer |
| `docs/product/APP_FLOW.md` | new | Per-page journeys; control to action-type to outcome tables; blueprint classification |
| `docs/product/BACKEND_SCHEMA.md` | new | PRAGMA-derived table/column/constraint/index/FK inventory + Mermaid ER diagram |
| `docs/product/DESIGN_BRIEF.md` | new | Token inventory with live consumers, theming, motion, accessibility, per-page look |
| `docs/ai_workflow/DOC_RETENTION.md` | modify | Add `docs/product/**` to the Always-active row |
| `docs/README.md` | modify | New "Product Reference" section linking the suite |
| `docs/PRODUCT_DOCS_PLAN.md` | modify | Status banner + this §8 |

**Effort**: M · **Owner**: autonomous Opus session · **Depends on**: nothing (docs-only, no
merge-order coupling with the other in-flight packets)

**Sequence**

1. Derive ground truth mechanically before writing prose: the Flask `url_map` read off the real
   `app` object; the template to JS dependency closure; every frontend network call site; and a
   fresh isolated runtime database built by `run_all_initializers(force_base=True)` and read
   back with `PRAGMA table_info` / `table_xinfo` / `index_list` / `index_info` /
   `foreign_key_list`.
2. Write D0's README first so the conflict rules exist before the documents that must obey them.
3. Write D4 (mechanical, highest certainty), then D2, then D5.
4. Cross-check every documented route against the dumped `url_map`, every documented table and
   column against the PRAGMA dump, and every documented token against the pinned CSS bundles.
5. Verify rendering: Mermaid parse, relative-link resolution, and live computed styles taken
   from a running app in this worktree.

**Expected gates**: `docs/**` is the "Product docs only" row of `QUALITY_GATE.md` and requires
no tests. `docs/ai_workflow/DOC_RETENTION.md` is the "AI workflow / agent config" row and adds
a manual dry-run / self-review. The union is therefore: link and reference checks, schema
cross-check, Mermaid render, computed-style verification, AI-workflow self-review, and
independent architecture + product-risk review. No pytest or Playwright target is derived from
this diff; full `pytest` is nonetheless run once as a no-regression check, because committed
baseline JSON files live under `docs/` and a docs edit that moved one would red the suite in a
way only a full run reveals.

### 8.3 Council review

Run per [`.claude/commands/council-plan.md`](../.claude/commands/council-plan.md) — three
reviewers in parallel against Plan v1 above.

Three reviewers ran in parallel against Plan v1. All three returned **Needs revision**.

> **Deviation from [`PLAN_REVIEW_TEMPLATE.md`](ai_workflow/PLAN_REVIEW_TEMPLATE.md), recorded rather than hidden.** The
> template says to paste each reviewer's output verbatim. Their combined output is roughly
> four times the length of this whole plan document, and pasting it would make the plan
> unreadable for the thing it is actually for. Every finding below is reproduced with its
> severity, its file:line evidence, and its disposition; none was dropped, merged, or
> softened. What is not reproduced is the reviewers' connecting prose.

**Agent provenance.** `architecture-reviewer`, `test-strategist`, and `product-risk-reviewer`
were each spawned once, in parallel, by the primary session. No `product-manager` agent was
used: `.claude/hooks/guard-planning-write.ps1` restricts that agent's writes to
`docs/<feature>/PLANNING.md`, and this workstream's plan document is `docs/PRODUCT_DOCS_PLAN.md`,
which that pattern does not match. The primary session therefore owns every write in this
packet, including Plan v1, this matrix, and Plan v2. Recorded per `test-strategist` finding 9.

**Independent re-verification.** Reviewer findings were treated as leads, not as facts. Every
finding accepted below that makes a claim about runtime behavior was re-checked directly
against the source before it was allowed to shape a document. Two findings were corrected on
re-check and are marked as such.

#### 8.3.1 `architecture-reviewer`

| # | Severity | Finding | Evidence |
|---|---|---|---|
| A1 | blocking | D4 creates a second schema source of truth; Plan v1 dropped §3's required back-pointer from `.claude/rules/database.md`. That file's 9-row table auto-loads into agent context on any schema edit; the correct 19-table inventory would sit in `docs/product/` and never load. | `.claude/rules/database.md:1-8` (path front matter), `:12-23` (9 rows) vs. 19 tables across `utils/db_initializer.py`, `utils/database.py`, `utils/program_backup.py`, `utils/catalog_upgrade.py`; `docs/DUPLICATION_REGISTRY.md:52` |
| A2 | blocking | Reading `url_map` off the real `app` object risks importing `app.py`, which reassigns `utils.config.DB_FILE` at line 93 and can resolve the checkout's own database. | `app.py:92-95`, `app.py:103`, `app.py:108`; `tests/conftest.py:103-118` documents the same trap |
| A3 | important | The initializer call graph is complete at table level but unproven at index level; the shipped seed's index set is unpinned. Claimed *unverified*, not divergent. | `utils/maintenance.py:60,62` creates `idx_eim_exercise_muscle`, `idx_eim_ex`, unreachable from `run_all_initializers`; `tests/test_catalog_seed.py:39-60` pins only `type='table'` |
| A4 | important | §7.4's "enforced FK vs by-convention relationship" requirement was dropped from Plan v1. A PRAGMA-only pass renders `workout_log.exercise`, `progression_goals.exercise`, `learned_strength_calibrations.exercise_name` as unrelated. | `utils/db_initializer.py:195` (real FK) vs `:255-274`, `utils/database.py:544`, `:708` (no FK) |
| A5 | important | Plan v1 silently narrows §7.4's D2 requirement for named Playwright specs plus recorded manual spot checks. | `docs/PRODUCT_DOCS_PLAN.md:151` vs Plan v1 Expected gates |
| A6 | nit | `docs/product/` placement and the DOC_RETENTION edit are correct and sufficient — but `DOC_RETENTION.md` is inside a parametrized pytest surface, so its edit must not contain `SHARED_PLAN` or `Tier <n>` / `Appendix A<n>`. | `docs/ai_workflow/DOC_RETENTION.md:13`; `tests/test_agent_workflow_contracts.py:80-86`, `:139-155`, `:163-173` |
| A7 | nit | D2 must name `POST /erase-data` explicitly; it is registered directly on the app, not on a blueprint, and the conftest twin does not carry it. | `app.py:245`; `tests/conftest.py:10-22` |
| A8 | nit | D5's live-style step needs a served-asset identity check; a relative worktree launch has previously served the main checkout's static bundles. | prior-session evidence |
| A9 | — | **No finding.** No concrete D1 or D3 requirement exists that cannot live inside D0/D2/D4/D5. Do not add a PRD or a TECH_DESIGN. | `docs/PRODUCT_DOCS_PLAN.md:150`, `:152` read against the approved subset |

#### 8.3.2 `test-strategist`

| # | Severity | Finding | Evidence |
|---|---|---|---|
| T1 | important | Plan v1 cites the wrong reason for running pytest. No committed baseline JSON moves in this diff. The one genuinely derived target is `tests/test_agent_workflow_contracts.py`, because `DOC_RETENTION.md` is inside its parametrized `SURFACE` — two nodes. | `tests/test_agent_workflow_contracts.py:80-86`, `:139`, `:163`, `:92` |
| T2 | important | Exact gate union: "Product docs only" (no tests) ∪ "AI workflow / agent config" (self-review). It does not escalate to `/verify-suite`. CI has no path filter, so the full suite runs on the PR regardless. | `QUALITY_GATE.md:34-35`, `:16-20`; `.github/workflows/ci.yml:3-7` |
| T3 | important | Complete hidden-pin census: **no glob newly matches `docs/product/**`.** The `SURFACE` glob is `docs/ai_workflow` non-recursive; `scripts/generate_test_inventory.py` reads pytest/Playwright collection, not docs; `.gitignore` does not match the new subtree. Test Inventory Drift cannot red on this diff. | 12 pinned `docs/` paths enumerated, each checked; `docs/test_inventory/TEST_INVENTORY.json:258-259` |
| T4 | important | Two unwritten constraints: never add a new `.md` under `docs/ai_workflow/` (adds 2 nodes, moves the inventory pin, reds the blocking drift job); and `git status --porcelain docs/ai_workflow .claude` must be empty before pytest, because an untracked file there fails locally while CI stays green. | `tests/test_agent_workflow_contracts.py:206-238`, `:59-71`; `.github/workflows/ci.yml:1032-1086`, `:1103` |
| T5 | blocking | D4's single-database derivation is provably incomplete: `run_all_initializers(force_base=True)` never runs `utils/maintenance.py`'s three index statements, and the real startup path copies `data/catalog.seed.db` first. Derive from two databases and document the union with differences flagged. | `utils/maintenance.py:60-62`; `utils/db_initializer.py:153`; `utils/catalog_seed.py:72`; `app.py:94` |
| T6 | important | Three mechanical content checks are worth running once (route set-diff, two-database PRAGMA union, token set-diff) — but **no committed test should be added.** A parity test converts every future route or table PR into a docs-editing PR, which is strictly stricter than the suite's own "on conflict, the code wins" contract. A token-parity test naming `theme-dark.css` also enters an audit census with untraced consequences. | `docs/test_inventory/TEST_INVENTORY.json:256-259`; `scripts/css_audit/p3_ceiling.py:635`, `:794`, `:913` |
| T7 | important | No committed link checker exists anywhere in the repo, so "every link resolves" is currently unverifiable. A new four-document subtree at a new nesting depth is exactly where relative-link arithmetic breaks, and it would merge green. | `package.json:5-8`; no workflow job; `docs/LEFTOVERS_BY_PRIORITY.md:647` records a one-off sweep |
| T8 | nit | The PR will run every E2E job. The only pre-existing exception is `e2e/program-backup.spec.ts:79`; `nav-dropdown.spec.ts` is no longer a known red and a failure there would be real. | `QUALITY_GATE.md:124`, `:126` |
| T9 | nit | `product-manager` is hook-blocked from writing any of the seven planned paths, so `/council-plan`'s delegation step cannot apply to this workstream. | `.claude/agents/product-manager.md:8-13`; `.claude/hooks/guard-planning-write.ps1:4` |
| T10 | nit | No file under `docs/product/` may be named `PLANNING.md` or `EXECUTION_LOG.md` — both are claimed by the Active-workstream retention class and by `/status`'s glob, which would contradict the Always-active row the same diff adds. | `docs/ai_workflow/DOC_RETENTION.md:14`; `.claude/commands/status.md:66` |

#### 8.3.3 `product-risk-reviewer`

| # | Severity | Finding | Evidence |
|---|---|---|---|
| P1 | blocking | Plan v1 has no acceptance criteria at all, so §7.4's binding corrections are unenforced. | Plan v1 §8.2 vs `docs/PRODUCT_DOCS_PLAN.md:147-155` |
| P2 | blocking | The verification lane checks structure (routes, tables, tokens) but no behavioral claim. A document can be right about which endpoint fires and wrong about what the page computes. | Plan v1 sequence step 4 |
| P3 | blocking | The status banner declared EXECUTED for documents that did not exist. | `docs/PRODUCT_DOCS_PLAN.md:3` at review time |
| P4 | blocking | Cutting D1 orphaned the only requirement that `CLAUDE.md`'s non-goals be reproduced **verbatim**. | `docs/PRODUCT_DOCS_PLAN.md:43` vs `:173` |
| P5 | nit | The §4 build-order diagram still routes D2 through a cut D1; §7.2's "journey oracle" rewording was dropped rather than repositioned. | `docs/PRODUCT_DOCS_PLAN.md:70`, `:112` |
| P6 | blocking | Effective sets is **two** numbers. `base_effective = raw × effort × rep_range` carries no muscle weight; the weight is applied only when building `muscle_contributions`. `CLAUDE.md`'s one-line formula collapses the two stages. | `utils/effective_sets.py:257`, `:276`; `utils/weekly_summary.py:135` |
| P7 | blocking | `CountingMode.RAW` zeroes only the effort and rep-range factors. Muscle-contribution weighting still applies, so a 3-set bench press shows 1.5 "raw" sets for Triceps in TOTAL mode. | `utils/effective_sets.py:247-250`; `utils/weekly_summary.py:125`; `utils/session_summary.py:133` |
| P8 | important | The volume-class badge is always computed from effective sets even in RAW mode, and a second legacy classifier is emitted alongside it. | `utils/weekly_summary.py:186-187`; `utils/session_summary.py:210-211` |
| P9 | blocking | Weekly Summary is **planned** volume with **no date window**. It never reads `workout_log`; `method` is accepted and ignored; "frequency" counts routines clearing 1.0 effective sets, not sessions performed. | `utils/weekly_summary.py:36-50`, `:179`, `:217-221`, `:243` |
| P10 | important | Session Summary mixes plan-sourced volume with log-sourced session counts; the date window filters only the log side, so narrowing it changes the denominator and the warning, never the totals. | `utils/session_summary.py:21-43`, `:46-69`, `:206-235` |
| P11 | blocking | `_get_progression_status`'s docstring advertises a `reduce_weight` status the function cannot return. | `utils/progression_plan.py:78-82` vs `:84-94`, `:209-225` |
| P12 | important | Progression always returns a suggestion list, not one decision; missing RIR **and** RPE is treated as acceptable effort; the increment is flat (+2.5 / +5.0 kg) and ignores current load. | `utils/progression_plan.py:445-451`, `:64-65`, `:39-49` |
| P13 | important | Progression never writes back to the plan; the only write is an explicit `progression_goals` insert. | `utils/progression_plan.py:455-479` |
| P14 | blocking | Fatigue's "% of MRV" divides a fatigue **score** by a set-count landmark. It is an index, not a percentage of volume. | `utils/_fatigue/per_muscle.py:51-65`, `:132-143`, `:181-206` |
| P15 | important | Fatigue is mode-independent, raw-set-based, has no decay, returns an empty window when nothing is logged, and yields zero for a row whose `scored_*` fields are all NULL. | `utils/fatigue.py:9-11`; `utils/_fatigue/core.py:247-262`; `utils/_fatigue/period.py:114-121`, `:175-178`; `utils/_fatigue/sfr.py:37-38` |
| P16 | important | Fatigue bands are literature-anchored **defaults** reviewed once with no change applied; `docs/fatigue_meter/PLANNING.md` is stale and must not be a prose source. | `docs/fatigue_meter/PLANNING.md:510-517`, `:537` vs shipped `utils/_fatigue/` |
| P17 | blocking | The Volume Splitter's "AI Suggestions" panel contains no AI — it is a local rule-based heuristic with hardcoded thresholds and no network call. | `templates/volume_splitter.html:113-115`; `utils/volume_ai.py:1-30` |
| P18 | nit | Two arithmetic traps: exactly 10.0 classifies BORDERLINE despite a docstring saying "≤10 OK"; the rep-range factor averages min/max, so averages landing between buckets fall through to 1.0. | `utils/effective_sets.py:99-103`, `:297`, `:75-81`, `:199-204` |
| P19 | blocking | Replace-exercise "no result" outcomes are HTTP 200 with `ok:false`, keyed on `error.reason`, and surfaced as **warnings**. A status-keyed table documents three real outcomes as successes. | `utils/exercise_replacement.py:215-272`; `static/js/modules/workout-plan-replacement.js:74`; `static/js/modules/workout-plan-helpers.js:204-208` |
| P20 | blocking | Erase-data **destroys the Backup Center library**, and `docs/program_backups.md:27` states the opposite. | `app.py:247-263`; `utils/schema_registry.py:22-24`; `docs/program_backups.md:27` |
| P21 | blocking | Backup restore deletes the entire workout log and the entire plan, unconditionally; snapshots contain plan rows only. | `utils/program_backup.py:445-446`, `:423-428`, `:455-460` |
| P22 | important | Promotional page copy is not behavioral evidence: the pre-erase artifact is a raw file copy with no in-app restore path. | `templates/welcome.html:113`; `docs/program_backups.md:65-66` |
| P23 | blocking | Filter view mode has three names for one thing: stored `'advanced'`, UI label **Scientific**, and `docs/FILTER_VIEW_MODE.md` documents a control location that no longer exists plus a status-bearing test count. | `static/js/modules/filter-view-mode.js:297-330`, `:591-599`; `templates/base.html:209-211`; `docs/FILTER_VIEW_MODE.md:176-186` |
| P24 | important | Terminology: link `CLAUDE.md` as canonical and restate only the enum members, their URL values, and their defaults. Full restatement is the higher-drift option. | `routes/weekly_summary.py:43-44`; `routes/session_summary.py:46-47`; `utils/effective_sets.py:39-56` |
| P25 | important | "Advanced" is overloaded four ways; "raw sets" does not mean "unweighted by muscle role"; "weekly" means two different things. The suite must fix each once. | `static/js/modules/filter-view-mode.js:599`; `utils/volume_ai.py:5-7`; `utils/_fatigue/core.py:253-256` |
| P26 | important | The informational-only rule must be restated per advisory surface, not once in a README the reader has already left. | `utils/effective_sets.py:6-7`; `templates/user_profile.html:585-605`; `templates/_fatigue_badge.html:11` |
| P27 | important | `BACKEND_SCHEMA.md` is the artifact most likely to read as an invitation to multi-user. A clean ER diagram with no `user_id` looks like an omission to an outside engineer. | `.claude/rules/routes.md:70` |
| P28 | important | No-telemetry / no-outbound-data must be stated as a positive fact, precisely because the suite will describe a panel labelled "AI Suggestions". | repo-wide absence of outbound HTTP outside `scripts/smoke_packaged_app.py` |

---

### 8.4 Response matrix

Every finding has a disposition. Two are **corrected** — accepted in substance but with a factual
adjustment found on re-verification.

| Finding | Reviewer | Disposition | Action in Plan v2 |
|---|---|---|---|
| A1 | architecture | **accept** | Add `.claude/rules/database.md` to the artifact set: one pointer line under its `## Schema` heading. The 9-row table is recorded as incomplete, not repaired, in this packet. |
| A2 | architecture | **accept (already satisfied, now written down)** | Both derivations were already isolated — the schema dump ran with `DB_FILE` set to a scratch path and a guard that refuses a pre-existing file; the route dump ran with `HT_RUNTIME_DIR` set to a scratch root. Plan v2 states the mechanism so it is reproducible rather than incidental. |
| A3 | architecture | **accept — and resolved** | Executed the two-database comparison A3 asked for. Result: the empty-file path and the seed+initializer path produce **identical** schemas — 19 tables, 17 indexes, zero column-shape differences. A3's "unverified" is now verified as *no divergence*. `utils/maintenance.py`'s two extra indexes are absent from both and are documented as maintenance-only. |
| A4 | architecture | **accept** | D4 gains an explicit enforced-vs-convention section, and states that enforcement holds only because `_configure_connection()` sets `foreign_keys = ON` per connection. |
| A5 | architecture | **accept, narrowed with reason** | No Playwright spec is run as documentation validation: the specs assert behavior, not that a document describes it, so a green run would be evidence of nothing about the doc. Replaced with stronger direct evidence — a live HTTP probe of all 11 page routes, 14 GET APIs, and 9 deliberate failure paths against a running app, recorded under `artifacts/`. |
| A6 | architecture | **accept** | The `DOC_RETENTION.md` edit is a one-word glob addition to an existing row; it introduces none of the forbidden strings. Verified after editing. |
| A7 | architecture | **accept** | `POST /erase-data` is named explicitly in APP_FLOW's route classification as the one non-blueprint route. |
| A8 | architecture | **accept, with the check's real limit stated** | Served bundles were hashed against this worktree's files (3/3 match) and the listening process identified. Recorded honestly: because this branch modifies no CSS, a hash match cannot by itself distinguish this worktree from main; the launch cwd and port ownership are what establish provenance. |
| A9 | architecture | **accept** | No PRD, no TECH_DESIGN. Recorded in §8.5. |
| T1 | test-strategist | **accept** | Expected gates corrected: the derived target is `tests/test_agent_workflow_contracts.py`. The baseline-JSON rationale in Plan v1 was wrong and is removed. |
| T2 | test-strategist | **accept in part** | The gate union is adopted as stated. Full local pytest is still run once — not as a derived target, but because this packet edits two files inside auto-loading agent context and a three-minute local no-regression check before pushing is cheap insurance. Recorded as a deliberate addition, not a derived requirement. |
| T3 | test-strategist | **accept** | Census reproduced in §8.6 so the next reader need not re-run the sweep. |
| T4 | test-strategist | **accept** | Added as a hard constraint: no new file under `docs/ai_workflow/`; `git status --porcelain docs/ai_workflow .claude` verified empty before any test run. |
| T5 | test-strategist | **accept — and resolved** | Two-database derivation executed; see A3. The union is documented and the difference set is empty. |
| T6 | test-strategist | **accept** | All three mechanical checks run once at authoring time; **no committed test is added**. The commands are carried in `docs/product/README.md` so revalidation is a paste, not archaeology. |
| T7 | test-strategist | **accept** | A relative-link resolver was written as a scratchpad script, run over every link in the new and modified files, and its result recorded. Not committed. |
| T8 | test-strategist | **accept** | Recorded as the expected-flake policy for this PR. |
| T9 | test-strategist | **accept** | Recorded in §8.3's provenance note. |
| T10 | test-strategist | **accept** | Added to Scope→Out. |
| P1 | product-risk | **accept** | §8.7 adds an explicit acceptance block restating §7.4's criteria for the four built packets. |
| P2 | product-risk | **accept** | Sequence gains step 4b: every behavioral or numeric claim cites its owning `file.py:function` and is checked against the function body, never against a docstring or a feature planning doc. This is what caught P11. |
| P3 | product-risk | **accept** | The banner was corrected the moment the finding landed and is only set to EXECUTED once the four files exist and this section is complete. |
| P4 | product-risk | **accept** | The verbatim-non-goals requirement moves to D0. `docs/product/README.md` reproduces `CLAUDE.md` §1's non-goals verbatim. |
| P5 | product-risk | **accept** | §8.5 records that D2 owns the feature vocabulary now that D1 is cut, and that E2E specs are gap-detection evidence only. |
| P6, P7, P8 | product-risk | **accept — re-verified independently** | Confirmed at `utils/effective_sets.py:247-276` and `utils/weekly_summary.py:118-140`, `:175-192`. Bound into D2 as content rules. |
| P9 | product-risk | **accept — re-verified independently** | Confirmed: `_WEEKLY_PLAN_QUERY` joins `user_selection` to `exercises` only, and the docstring itself states `method` is ignored. Corroborated from outside the source: the live page title is **"Plan Volume Summary"**. |
| P10 | product-risk | **accept** | Bound into D2. |
| P11, P12, P13 | product-risk | **accept — re-verified independently** | Confirmed at `utils/progression_plan.py:39-49`, `:60-94`. The docstring/body divergence is real; D2 documents the three reachable statuses. |
| P14 | product-risk | **accept — re-verified independently** | Confirmed: landmarks are annotated "weekly counts per §5" while `score` accumulates `per_set.fatigue * sets * role_weight`. D2 describes the bar as score-against-landmark and records the unit caveat without proposing a change. |
| P15, P16 | product-risk | **accept** | Bound into D2; `docs/fatigue_meter/PLANNING.md` is excluded as a prose source. |
| P17 | product-risk | **accept — re-verified independently** | Confirmed at `utils/volume_ai.py:1-40`. D2 names the panel by its shipped heading and states plainly that it is local and rule-based. No rename is proposed — that would be a code change. |
| P18 | product-risk | **accept** | D2 derives thresholds from the constant dicts and states the boundary convention. |
| P19 | product-risk | **accept — corrected** | Confirmed, with one correction: the reviewer cited `utils/exercise_replacement.py:215-272`; the actual raise sites are `:182`, `:204`, `:216`, `:232`, `:260`, `:267`. The substance holds exactly — `NO_CANDIDATES`, `SELECTION_FAILED`, `DUPLICATE` all carry `status_code=200`. D2's outcome table gains a third column. |
| P20 | product-risk | **accept — re-verified independently** | Confirmed: `OWNED_TABLES_DROP_ORDER` begins with `program_backup_items`, `program_backups`. `docs/program_backups.md:27` is contradicted by the code. D2 documents the code behavior and flags the stale line; it does not edit that file, which is outside this packet's scope. |
| P21 | product-risk | **accept — re-verified independently** | Confirmed at `utils/program_backup.py:445-446`. D2 states the blast radius explicitly. |
| P22 | product-risk | **accept** | Content rule: controls are documented from their handler, never from template marketing copy. |
| P23 | product-risk | **accept — corrected** | Confirmed with one correction: the reviewer read the module docstring as evidence the *stored* value is user-facing. Re-checked — `filter-view-mode.js:591` and `:599` set the labels to `Simple` and `Scientific`, and the stored values are `'simple'` / `'advanced'`. Substance holds. D2 uses the UI names and marks the stored values as internal. |
| P24, P25 | product-risk | **accept** | D0 gains a canonical-terminology section using the hybrid rule and a short "words we use carefully" block. |
| P26 | product-risk | **accept** | Every advisory surface in D2 carries its own informational-only sentence. |
| P27 | product-risk | **accept** | D4 opens with an explicit single-user statement: no `user_id`, no tenancy, no auth tables — deliberately absent. |
| P28 | product-risk | **accept** | D0 states the no-outbound-network fact; D2 repeats it locally at the Splitter. **Scoped correction:** the application's own *routes* make no outbound calls, but `templates/base.html` loads five third-party assets from CDNs at page load. D0 and D2 state both facts rather than the flattering half. |

No finding was rejected. No finding was deferred.

---

### 8.5 D1 and D3 — not built

The owner permitted a PRD or a TECH_DESIGN only if the council proved a concrete missing
requirement that could not live inside the selected documents. The council was asked that
question directly and answered **no** (A9), with reasoning this session verified:

- **D1's obligations have homes.** The user-facing page taxonomy and the product-surface /
  supporting-infrastructure classification are owned by `APP_FLOW.md`. Gate 0 decision 4 already
  dispositions Body Composition, Fatigue, and Home. The one D1 requirement that was genuinely
  orphaned — verbatim non-goals (P4) — moves to `docs/product/README.md`.
- **D3 would be the duplication the plan exists to prevent.** §3 describes D3 as "a short summary
  plus a link to the owning rules file or ADR". That is precisely what D0's canonical-source map
  is, and building it twice creates the second source of truth §2.1 forbids.

Consequences recorded: D2 now owns the feature vocabulary that §4's build order routed through
D1, and E2E specs are used as gap-detection evidence only, never as the journey oracle (P5).

---

### 8.6 Pin census, re-derived at plan stage

Reproduced from `test-strategist` T3 so the next reader does not re-run the sweep. Every
hardcoded `docs/` path that is **read** by a test, workflow, or script:

| Consumer | Pinned path | Moved by this diff? |
|---|---|---|
| `tests/test_agent_workflow_contracts.py:84` | `docs/ai_workflow/*.md` — **non-recursive** | Content only (`DOC_RETENTION.md`) |
| `tests/test_agent_workflow_contracts.py:206` | every SURFACE file must be git-tracked | No new SURFACE file is added |
| `tests/test_volume_taxonomy.py:185` | `docs/archive/VOLUME_TAXONOMY_AUDIT.md` | No |
| `tests/test_css_wp4_4_a_baseline_contracts.py:36` | `docs/CSS_PHASE4_WP4_4_A_BASELINE.json` | No |
| `tests/test_css_cascade_contracts.py:161` | `docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json` | No |
| `tests/test_css_theme_dark_p3_audit_contracts.py:781`, `:850` | `docs/CSS_PHASE4_WP4_4_LINUX_INHERITED_REDS.json` | No |
| `.github/workflows/ci.yml:844` | `docs/ci_cd_phase3/pyright-baseline.json` | No |
| `.github/workflows/ci.yml:991` | `docs/CSS_PHASE4_WP4_1_STYLELINT_BASELINE.json` | No |
| `.github/workflows/ci.yml:1094`, `:1124` | `docs/test_inventory/TEST_INVENTORY.json` | No |
| `scripts/generate_test_inventory.py:39-41` | `docs/test_inventory/` (output only) | No |
| `scripts/fatigue_stage4_observer.py:44`, `scripts/check_fatigue_stage4_automation.ps1:48` | `docs/fatigue_meter/stage4_calibration_log.csv` | No |
| `scripts/css_audit/p3_ceiling.py:72`, `emit_baseline.py:22`, `:83` | WP4.4 JSON baselines | No |

`docs/product/**` is matched by **none** of them. The inventory generator reads pytest and
Playwright collection output, not the docs tree, so `Test Inventory Drift` cannot red on this
diff. `.gitignore` does not match the new subtree, so the files will actually commit.

---

### 8.7 Plan v2

**Goal**: unchanged from v1.

**Scope**

- **In**: v1's set, **plus** one pointer line in `.claude/rules/database.md` (A1).
- **Out**: v1's set, **plus** — no committed test (T6); no new file under `docs/ai_workflow/`
  (T4); no file under `docs/product/` named `PLANNING.md` or `EXECUTION_LOG.md` (T10); no edit
  to `docs/program_backups.md` or `docs/FILTER_VIEW_MODE.md`, whose staleness is flagged in
  place rather than repaired here (P20, P23); no rename of the "AI Suggestions" heading (P17).

**Artifacts**

| Path | Change | Notes |
|---|---|---|
| `docs/product/README.md` | new | D0 + D6. Canonical-source map, conflict rules, verbatim non-goals (P4), terminology (P24, P25), re-verification commands (T6), no-outbound-calls statement with its CDN caveat (P28) |
| `docs/product/APP_FLOW.md` | new | Per-page journeys, control action-type classification, three-outcome API tables (P19), per-surface informational-only sentences (P26), `/erase-data` named (A7) |
| `docs/product/BACKEND_SCHEMA.md` | new | Two-path PRAGMA derivation (T5, A3), enforced-vs-convention relationships (A4), single-user statement (P27), Mermaid ER diagram |
| `docs/product/DESIGN_BRIEF.md` | new | Tokens with measured live-consumer counts, computed styles across two themes and three viewports, motion and accessibility, intentional exceptions |
| `docs/ai_workflow/DOC_RETENTION.md` | modify | `docs/product/**` into the Always-active row; no forbidden strings (A6) |
| `.claude/rules/database.md` | modify | One pointer line to `BACKEND_SCHEMA.md` (A1) |
| `docs/README.md` | modify | Product Reference section |
| `docs/PRODUCT_DOCS_PLAN.md` | modify | Status banner + §8 |

**Sequence**

1. Derive ground truth mechanically, each derivation isolated by an explicit scratch path (A2).
2. Derive the schema **twice** — empty file, and shipped seed plus initializers — and document
   the union with any difference flagged by its owning DDL site (T5, A3).
3. Write D0 first so the conflict rules exist before the documents that obey them.
4. Write D4, then D2, then D5.
5. Cross-check routes against the dumped `url_map`, tables and columns against both PRAGMA
   dumps, tokens against the pinned bundles.
6. **4b.** Check every behavioral or numeric claim against its owning function body, citing
   `file.py:function`. Never against a docstring, never against a feature planning document (P2).
7. Verify rendering: Mermaid parse, relative-link resolution over every new and modified file
   (T7), and live computed styles from a running app whose served bundles are hash-checked and
   whose port ownership is confirmed (A8).
8. Confirm `git status --porcelain docs/ai_workflow .claude` is empty, then run
   `tests/test_agent_workflow_contracts.py` (T1) and a full local pytest as elective
   no-regression insurance (T2).

**Expected gates**: the union of `QUALITY_GATE.md`'s "Product docs only" row (no tests) and its
"AI workflow / agent config" row (manual dry-run / self-review, `code-reviewer` or careful
self-review). Derived pytest target: `tests/test_agent_workflow_contracts.py`. No E2E target, no
`/build-css`, no baseline regeneration, no `/verify-suite` escalation. CI has no path filter, so
the PR runs all required contexts regardless; the only pre-existing exception is
`e2e/program-backup.spec.ts:79` (T8).

**Acceptance** — §7.4's criteria for the four built packets (P1):

- [x] **D0** — `docs/product/**` indexed from `docs/README.md`, classified Always-active in
  `DOC_RETENTION.md`, README identifies canonical sources, conflict rules, audience, and
  maintenance ownership. Non-goals reproduced verbatim (P4).
- [x] **D2** — every in-scope interactive control accounted for with its action type; every
  frontend network call site mapped to a route and method; dynamic URLs checked structurally;
  live probe evidence recorded in place of the narrowed spec requirement (A5).
- [x] **D4** — documented schema matches a freshly derived runtime schema across tables,
  columns, defaults, constraints, indexes, and FKs, by two independent derivation paths;
  initializer-owned migrations included; convention-only relationships distinguished from
  enforced FKs; Mermaid diagram parses.
- [x] **D5** — every documented token exists at the pinned revision `bcbd973` and its live
  consumer count is measured, not assumed; light and dark and three viewports checked against
  computed output; no new design decision introduced.
- [x] **D6** — README links the checked-in planning sources by path, not by slash-command name.

### 8.8 Post-implementation review

Two independent reviewers read the finished documents against the source. Between them and one
self-directed census they found **twenty-two** defects in the first drafts, every one accepted and
fixed. This section is the record; §8.3–§8.4 is the plan-stage council.

The pattern in the misses is worth naming, because it is not random. Nearly every one was a claim
that *looked* verified: a route that exists and is documented as wired but has no caller, a column
whose `ALTER TABLE` is real but never fires on a fresh build, a badge computed on every request
that sits next to a genuinely opt-in feature of the same name. **Structural checks confirm that a
thing exists. They do not confirm that the sentence about it is true.**

#### 8.8.1 A self-directed census, run because the plan predicted this gap

Sol5.6 §7.2 warned that proving each documented route exists is a one-way check. Acting on that,
every registered rule was censused against the whole frontend in the reverse direction — matching
each rule's static prefix so dynamically assembled URLs still count.

It found **six routes with no caller anywhere**, and corrected three claims in the draft that
described unreachable endpoints as live controls:

| Route | Draft claimed | Reality |
|---|---|---|
| `GET /api/superset/suggest` | a "Superset suggestions" control on the Plan page | no caller |
| `GET /get_generator_options` | populates the Generate Plan modal | modal options are hardcoded in the template |
| `GET /get_workout_logs` | implied wired on the Log page | no caller; rows are server-rendered |

The other three — `/export_workout_log`, `/export_large_dataset`, `/export_summary` — were already
recorded. `/export_summary` is unreachable *because* its only intended caller builds a
non-existent URL, which links two findings that had looked separate.

#### 8.8.2 `architecture-reviewer`

| # | Severity | Finding | Disposition |
|---|---|---|---|
| R1 | important | Three status documents still described this plan as an unapproved proposal while the banner said EXECUTED — `INDEX.md`, `LEFTOVERS_BY_PRIORITY.md`, `MASTER_HANDOVER.md`. `INDEX.md` is the worst because it auto-loads. | **accept, in part.** First two updated here. `MASTER_HANDOVER.md` deliberately not edited — the parallel-session rule reserves it for the integration session, which the local handover briefs. |
| R2 | important | The new README designates `.claude/rules/database.md` as canonical for "adding a table", but its five-step recipe predates WP2.6 and tells the reader to call `add_*_table()` from `app.py`, which contains **zero** such calls. | **accept.** Verified independently. A correction note now precedes the recipe, naming `utils/schema_registry.py` as the real registration point. |
| R3 | important | Only the schema arm of the maintenance contract was wired; `routes.md` and `frontend.md` carried no pointer, so "update it in the same change" could never fire for the two documents the plan called the genuine gaps. | **accept.** Pointer mirrored into both. |
| R4 | nit | `.claude/rules/database.md`'s `paths:` front matter omitted `utils/schema_registry.py` and `utils/catalog_upgrade.py`, so an agent editing the registry loaded neither the misleading table nor the new pointer. | **accept.** Both added — this is what actually closes A1, since a pointer only helps if the file loads. |
| R5 | nit | Three documents restate material the README's own ownership table assigns elsewhere. | **accept, in part.** `BACKEND_SCHEMA.md`'s runtime-path section trimmed to a sentence plus link — pure how-to duplication. The response envelope stays (needed in place to make the outcome table legible); the measured bundle order and theming stay (the brief's own subject, distinct from the how-to). |
| R6 | — | **Status leakage: clean.** `bcbd973` judged an acceptable provenance pin, not status. | noted |
| R7 | — | **Retention and tooling: clean**, with one census gap — `SURFACE` also globs `.claude/rules/*.md`, which §8.6 did not record. | **accept** — corrected in §8.8.4. |
| R8 | nit | `QUALITY_GATE.md` requires no tests and no reviewers for `docs/**`, while the suite also declines a parity test. The maintenance contract is unenforced at both ends. | **accept.** Stated plainly in the README rather than left implied. Not a gate change. |

#### 8.8.3 `product-risk-reviewer`

| # | Severity | Finding | Disposition |
|---|---|---|---|
| Q1 | important | The three-outcome table claimed all three 200-status outcomes render a warning. Wrong in both directions: `selection_failed` has no case and falls through to an **error** toast, while `missing_metadata` — a **400** — renders a **warning**. | **accept.** Replaced the prose with the actual reason-to-severity map and stated that severity does not track HTTP status either way. |
| Q2 | important | `GET /get_routine_exercises/<routine>` was described as loading "that routine's rows". It ignores the routine and returns the full catalog — deliberately, because the dropdown it feeds is an *add* control. | **accept.** Corrected, with the reason. |
| Q3 | important | "There is no per-page bundle / JS cost is identical on every page" is false: five templates load an additional page module, and three of those five are also in `pageInitializers`. | **accept.** Replaced with a measured per-page table. |
| Q4 | important | The "40 modules" figure was the closure of *all* `base.html` scripts, not of `app.js`. | **accept.** Re-measured per entry point: `app.js` reaches **34** files; **17 of the 50** files in `static/js/modules/` are unreachable from it. The `window` assignment count was also corrected from ~18 to 20. |
| Q5 | important | Both summary pages render an always-on "Projected fatigue" badge the document never mentioned — and the "off by default" sentence pointed at a *different* surface, the gated fatigue-context block. | **accept.** Badge added to both control tables; the two fatigue surfaces now have their own comparison table so they cannot be conflated. |
| Q6 | important | Two `ALTER TABLE` provenance claims are wrong for a freshly built database — those columns are in the `CREATE TABLE`, and the `ALTER`s are guarded upgrade paths that never fire on a fresh build. | **accept.** Corrected for `exercises` (all four) and `user_selection` (`superset_group`); the genuine fresh-build ALTER set is five columns, now stated as such. |
| Q7 | important | The `pages-*.css` total of 8,032 excluded the largest page bundle. | **already fixed** — caught by self-check before the review landed; the correct total is 13,840. |
| Q8 | important | `safe_media_path` was attributed to the Plan page; it runs only on the Log page. The Plan table is built client-side and validates in JavaScript. | **accept.** Moved, with both mechanisms named. |
| Q9–Q16 | nit | Four replace-exercise codes should be three; progression writes are insert/update/delete not insert alone; the Fatigue page has no Apply button (the select auto-submits; the only button is inside `<noscript>`); "MRV" is internal vocabulary the UI never shows; navbar labels are Weekly / Session / Progress / Distribute, not the destination names; the maintenance-index heading over-generalized to three indexes when one of them *is* in the schema; `--layout-space-2xl` is declared once and never varies despite its name; there are 10 page bundles for 11 page routes because `/fatigue` has none. | **all accepted and fixed.** |
| Q17 | nit | The "verified live" annotations and every computed-style value rest on an unreproduced local run with no committed artifact. | **accept as a provenance note.** Both documents now say so plainly: those claims are not reproducible from the repository, the raw capture is deliberately not committed because a stale snapshot presented as current is worse than none, and re-running is the way to confirm. |

The reviewer also returned **clean bills** on the categories that mattered most — calculation
semantics across all five surfaces, route-surface arithmetic, every statically checkable status
and error code, the full 19-table schema apart from Q6, invariant fidelity including the verbatim
non-goals and the CDN caveat, and the entire token census including all 17 zero-consumer tokens
and every colour, band, and line count.

#### 8.8.4 Correction to §8.6's pin census

`tests/test_agent_workflow_contracts.py`'s `SURFACE` globs **`.claude/rules/*.md` as well as
`docs/ai_workflow/*.md`**. §8.6 recorded only the second arm, because `.claude/rules/database.md`
entered scope later through finding A1. Consequence: this change touches **five** files inside
that parametrized surface — `DOC_RETENTION.md`, `INDEX.md`, and three `.claude/rules/` files — and
each must avoid `SHARED_PLAN`, `Tier <digit>`, and `Appendix A<digit>`. Verified after editing;
the file stays at 77 nodes, so the inventory pin does not move.

#### 8.8.5 Verification performed

| Check | Result |
|---|---|
| Relative-link and anchor resolution across all twelve new and modified files | 169/169 resolve |
| Doc-versus-ground-truth cross-check, 8 assertions | all pass |
| Reverse census — every registered rule against the whole frontend | 6 unbound routes found and documented |
| Mermaid ER diagram rendered with the real engine | renders |
| `tests/test_agent_workflow_contracts.py` — the one derived target | 77 passed, matching the pinned count |
| Full local `pytest` — elective, not derived | 2673 passed, 2 skipped |
| Status-leakage scan over `docs/product/**` | clean |
| The three published re-verification commands, executed as written | all run clean and reproduce the documented numbers |

Four defects were caught by these checks rather than by either reviewer: a relative link in this
document that climbed one level too far, an arithmetic error in the design brief's bundle total,
a radius claim that implied a token owned 45 literal declarations, and the three unbound-route
claims above. That is the argument for running mechanical checks even when a document has already
been read carefully.

Raw evidence — both schema dumps, the route dump, the frontend dependency and network-call dumps,
the control inventory, the computed-style capture, and the live HTTP probe — sits under the
gitignored `artifacts/` directory in the working worktree. It is deliberately not committed: it is
regenerable from the commands in `docs/product/README.md`, and a committed snapshot would become
the stale artifact §2.1 warns about.

#### 8.8.6 Re-verification after rebase

Three sibling packets merged to `main` while this one was in review, touching CI, the Pyright and
test-inventory baselines, nine test modules, and two `utils/_profile_estimator/` files. There was
**zero file overlap** with this change set, and the rebase was clean.

Because the documents pin a source revision, the rebase makes that pin a claim about a tree the
measurements were not taken from. Rather than let it slide, the derivations were re-run against
the rebased tree:

- Schema: re-derived — 19 tables, 167 columns, unchanged.
- Routes: re-derived from the live `url_map` — unchanged.
- Design tokens: all eight global CSS bundles are **byte-identical** (SHA-256 compared), and no
  template changed, so the computed-style capture still describes this tree.
- The one merged change that touches a module this suite mentions — the profile estimator — is
  overloads, annotations, and docstrings only; no runtime expression changed.

The cross-check then passed 8/8 against the rebased tree, so the pin was updated to the new base.
It names a tree where every claim has actually been verified, not merely the tree the work started
from.

### 8.9 First drift correction — local-first assets

The suite went stale **within the hour of merging**, and the way it happened is worth recording
because it is the failure mode §2.1 predicts.

PR #341 (`ddbec6a`, "serve every runtime asset locally") merged shortly *before* this suite did.
It vendored Inter, Bootstrap's JavaScript bundle, Sortable, flatpickr, Popper, and Tippy under
`static/vendor/` and removed every CDN reference from the templates. The suite had been written
and reviewed against a tree where those five families were fetched from `fonts.googleapis.com`,
`cdn.jsdelivr.net`, `unpkg.com`, and `cdnjs.cloudflare.com` — so it merged carrying a table of
third-party hosts that no longer described the application.

Nothing was wrong with either change. The two packets were in flight simultaneously, and #341's
author could not have updated documents that did not yet exist. **This is exactly the gap the
maintenance pointers added in §8.8.2 exist to close going forward**: `.claude/rules/frontend.md`
now tells the next person editing assets that `DESIGN_BRIEF.md` describes them.

Corrected in a follow-up, against `53af816`:

| Document | Was | Now |
|---|---|---|
| `APP_FLOW.md` | "Third-party assets the browser fetches" — five CDN hosts, plus a degraded-offline paragraph | "Third-party assets — all served locally", with vendored versions and paths; offline behavior is complete |
| `APP_FLOW.md` | three controls annotated "CDN-dependent" | named as vendored libraries |
| `README.md` | "the browser does reach third parties … not yet local-only in its assets" | "nothing in this application talks to the network", server or browser |
| `DESIGN_BRIEF.md` | load order beginning `css2 (Inter, remote)`; "Inter is loaded from Google Fonts" | begins `vendor/inter/inter.css`; Inter documented as vendored, seven `woff2` subsets, relative paths |
| all four | pinned at `542df07` | pinned at `53af816` |

**Evidence, not inference.** The claim that changed is "no external requests", so it was verified
the way that claim deserves: a browser capture of **every** request issued across four pages —
including the two that carry extra vendored libraries — returned an empty external-request list.
Schema, routes, the reverse caller census, and the token census were all re-derived against the
same tree and are unchanged; the six unbound routes are still six.

One precision improvement fell out of the live capture: the `page_css` slot in the load-order
diagram holds whatever the template declares, not only that page's own bundle — `/progression`
loads the vendored `flatpickr.min.css` there ahead of `pages-progression.css`.

### 8.10 Second drift correction — the Fatigue body heatmap

PR #339 (`ea82ef1`) added a body-heatmap panel to `/fatigue` and merged between this suite and its
§8.9 correction. It invalidated three claims:

| Claim | Why it broke |
|---|---|
| "`/fatigue` loads no page-specific JavaScript at all — it is entirely server-rendered" | the page now loads `fatigue-heatmap.js`, which imports `bodymap-svg.js` |
| "`/fatigue` is the only page with neither an initializer nor a module" | it now has a module |
| the Fatigue control table | did not list the panel, its channel toggle, the figures, or the legend |

Corrected against the merged tree, and the per-page module table re-measured: **six** templates now
load an extra module, and **18 of 51** files under `static/js/modules/` are unreachable from
`app.js`. Fixing that also caught an error §8.9 had introduced — the claim that only
`/workout_log` and `/progression` run on `app.js` alone. It is four pages: those two plus
`/volume_splitter` and `/backup`.

Verified live rather than read off the template. On a planned-only page the `Planned` channel
button renders visible and pressed while `Logged` stays hidden, which is what the module's
reveal-if-populated behavior is *for* — so the documented statement is the measured one, not the
one the markup suggests. Both figures mount, the panel is open by default, and the select keeps its
12px radius in both themes.

One genuine improvement fell out of it. `/fatigue` still declares no `page_css` block, so the
"10 page bundles for 11 page routes" claim holds — but its styling, heatmap included, lives in
`scss/_fatigue.scss`, which is `@import`ed into `custom-bootstrap.scss` and compiles into
`bootstrap.custom.min.css`. It is the one page whose look is carried by the Bootstrap build
artifact rather than a route bundle, which is why its overrides are not findable in
`static/css/pages-*.css`. The design brief now says so.

**Two corrections within an hour of merging is the honest measure of this suite's maintenance
cost**, and both came from packets that were in flight simultaneously and could not have updated
documents that did not yet exist. The pointers added in §8.8.2 are the standing mechanism for the
steady state; a burst of parallel feature work is what they cannot cover. Further drift from
packets still in flight belongs to the integration session, not to this one.
