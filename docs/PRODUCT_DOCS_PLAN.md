# Product Documentation Suite — Plan

**Status:** PROPOSED — NEEDS REVISION (brainstorm output, not owner-approved; Gate 0 approves requirements only; no packet may start until the revised plan completes the repository-required council review and receives Gate 1 owner approval)
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
