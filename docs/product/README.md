# Product Reference

*What this application is, how each screen behaves, what the database actually contains, and
what the shipped design system is.*

**Derived from:** the source tree at revision `542df07`. **On conflict, the code wins** — every
document here is a description of the code, never a specification for it. If you find a
disagreement, the code is right and the document is a bug.

---

## The suite

| Document | Answers |
|---|---|
| [`APP_FLOW.md`](APP_FLOW.md) | What is each screen for, what can the user do on it, and what happens — including when it fails |
| [`BACKEND_SCHEMA.md`](BACKEND_SCHEMA.md) | What tables and columns exist, what constrains them, and how they relate |
| [`DESIGN_BRIEF.md`](DESIGN_BRIEF.md) | What the shipped visual system is — tokens, theming, typography, motion, accessibility |

## Audience

Written for the owner and for future AI agents first, with enough context that an external
technical collaborator can follow it. Concise and source-linked by design: where an existing
document already owns a subject, this suite links to it rather than restating it.

## What these documents are not

They carry **no status**. No branch names, no pull-request numbers, no test counts, no "current
work packet", no dates that imply freshness. Point-in-time project state lives in
[`../MASTER_HANDOVER.md`](../MASTER_HANDOVER.md), which is the file to read first for anything
in flight. A count or a status claim appearing here would be a defect, not an update.

They are also **not implementation guides**. How to add a blueprint, how to add a table, which
tests a change requires — those belong to the canonical guides below and are deliberately not
duplicated here.

---

## Canonical sources — who owns what

When two documents disagree, the owner in this table wins.

| Subject | Canonical owner | This suite's role |
|---|---|---|
| Product intent, terminology, non-goals | [`../../CLAUDE.md`](../../CLAUDE.md) §1 | Links; restates only the enum vocabulary below |
| Architecture, module boundaries, startup order | [`../../CLAUDE.md`](../../CLAUDE.md) §2 | Links |
| Route patterns, response contract, validation, auth boundary | [`../../.claude/rules/routes.md`](../../.claude/rules/routes.md) | `APP_FLOW.md` describes observed per-route behavior; the contract shape is owned there |
| Database access pattern, adding a table, connection PRAGMAs, runtime paths | [`../../.claude/rules/database.md`](../../.claude/rules/database.md) | `BACKEND_SCHEMA.md` is the full field-level inventory; the how-to stays there |
| CSS bundle structure, adding a JS module, dark-mode mechanism | [`../../.claude/rules/frontend.md`](../../.claude/rules/frontend.md) | `DESIGN_BRIEF.md` describes the shipped visual result |
| CSS file ownership map | [`../CSS_OWNERSHIP_MAP.md`](../CSS_OWNERSHIP_MAP.md) | Links |
| Which tests and reviewers a change requires | [`../ai_workflow/QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) | Links |
| Durable cross-cutting decisions | [`../DECISIONS.md`](../DECISIONS.md) | Links |
| Current project state, open work, decisions in flight | [`../MASTER_HANDOVER.md`](../MASTER_HANDOVER.md) | Never duplicated here |

**Conflict rule, in order.** Running code beats every document. `CLAUDE.md` and
`.claude/rules/*` beat this suite on anything they own. `MASTER_HANDOVER.md` beats this suite on
anything time-sensitive. This suite is authoritative only for the descriptive material it
uniquely carries: per-screen behavior, the field-level schema, and the measured design system.

**Maintenance ownership.** These documents are maintained by whoever changes the behavior they
describe. A change to a route's outcomes, to the schema, or to the token set should update the
matching document in the same change. To make that reachable rather than aspirational, each of
the three canonical rules files that auto-load on those edits — `routes.md`, `database.md`,
`frontend.md` — carries a pointer back to its matching document.

**This contract is unenforced at both ends, deliberately.** No test checks that a document matches
the code (see *Re-verifying this suite* for why), and `QUALITY_GATE.md` requires no tests and no
reviewers for a `docs/**` change. So the suite can drift, and the mechanism that catches drift is
a person or an agent running the commands below — not CI. That is the accepted cost of a
descriptive document that is allowed to lag the code it describes.

---

## Product intent, in brief

A local-first Flask application for designing, logging, and analyzing hypertrophy resistance
training programs. Single user, no authentication, served on `localhost`. The seven core
workflows and the terminology table live in [`../../CLAUDE.md`](../../CLAUDE.md) §1.

### Non-goals — reproduced verbatim from `CLAUDE.md` §1

> - No user accounts or authentication — single-user local only.
> - No cloud sync or remote database.
> - Effective sets are **informational only** — never auto-adjust or block user actions (module docstring, `utils/effective_sets.py`).

These are load-bearing. The third one generalizes: **every advisory surface in this application
is informational.** Effective sets, volume classifications, session-volume warnings, fatigue
bands and stimulus-to-fatigue ratios, pattern-coverage warnings, progression suggestions, and
volume-splitter suggestions all describe; none of them adjusts a value, blocks an input, or
gates a control. A threshold in this application is never a target, a limit, a cap, or a
requirement.

### Network behavior

The application's own routes make **no outbound network calls and send no telemetry**. Nothing
is uploaded, and there is no analytics of any kind.

That statement is about the server, and the flattering half alone would be misleading. The
**browser** does reach third parties: `templates/base.html` loads the Inter web font from
`fonts.googleapis.com` / `fonts.gstatic.com` and the Bootstrap JavaScript bundle from
`cdn.jsdelivr.net` on **every** page, and three page templates each add their own CDN
dependency. So the application is local-first in its data and not yet local-only in its assets.
Exact hosts, per-page, are in
[`APP_FLOW.md`](APP_FLOW.md#third-party-assets-the-browser-fetches).

### Security boundary

There is no authentication, by design. `.claude/rules/routes.md` states the operating rule
directly: **do not expose this application to an untrusted network.** Anyone who can reach the
port can read and destroy all data.

---

## Words this suite uses carefully

Several terms are overloaded in this codebase. The suite fixes each one here and then obeys it.

**`CountingMode`** — `RAW` or `EFFECTIVE`. URL values `raw` and `effective`. Selects whether the
effort factor and the rep-range factor are applied. It does **not** control muscle-contribution
weighting. Missing or unrecognized input falls back to `EFFECTIVE`.

**`ContributionMode`** — `DIRECT_ONLY` or `TOTAL`. URL values `direct` and `total`. Selects
whether secondary and tertiary muscles are credited at all. Applies to raw and effective numbers
alike. Missing or unrecognized input falls back to `TOTAL`.

Both are defined in `utils/effective_sets.py` and normalized in `routes/weekly_summary.py` and
`routes/session_summary.py`.

**"Raw sets"** means *not adjusted for effort or rep range*. It does **not** mean *not weighted
by muscle role*. In `TOTAL` contribution mode a raw set count can be fractional for a secondary
or tertiary muscle. This surprises people; it is not a bug.

**"Advanced"** is used four unrelated ways in this codebase and this suite never uses it bare:

| Where | Meaning | What this suite calls it |
|---|---|---|
| Muscle-naming mode, stored value | `'advanced'` in `localStorage` | The **Scientific** mode; `'advanced'` is called out as the internal stored value |
| Muscle-naming mode, UI label | The button reads `Scientific` | **Scientific** |
| `utils/volume_ai.py` mode parameter | `'basic'` / `'advanced'` muscle grouping | The splitter's **advanced grouping mode**, always qualified |
| Exercise catalog column | `advanced_isolated_muscles` | Always written as the column name |

**"Weekly"** also means two things, neither of which is a date window. On the Weekly Summary page
it means the whole plan treated as one week — see
[`APP_FLOW.md`](APP_FLOW.md#weekly-summary--weekly_summary). In fatigue Phase 1 it means "the set
of routines passed in", which the source says in those words.

Everything else — RIR, RPE, effective sets, routine, movement pattern, superset — is defined
once in [`../../CLAUDE.md`](../../CLAUDE.md) §1 and is not redefined here.

---

## How work gets planned and built

*This section is the suite's engineering-plan pointer. The repository's planning process is a
living workflow, and a static snapshot of it would be wrong within a week — so this points at
the checked-in sources instead of restating them.*

| Stage | Source |
|---|---|
| Which approval gates a change needs, by planning size | [`../ai_workflow/QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md#plan-stage-routing) |
| Which tests and reviewers a change needs, by changed path | [`../ai_workflow/QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md) |
| The plan-review council — three reviewers, response matrix, Plan v2 | [`../../.claude/commands/council-plan.md`](../../.claude/commands/council-plan.md) |
| The planning-document shell to fill in | [`../ai_workflow/PLAN_REVIEW_TEMPLATE.md`](../ai_workflow/PLAN_REVIEW_TEMPLATE.md) |
| Working in parallel without corrupting shared state | [`../ai_workflow/PARALLEL_WORKFLOW.md`](../ai_workflow/PARALLEL_WORKFLOW.md) |
| Who owns which shared file | [`../ai_workflow/WORKSTREAM_OWNERSHIP.md`](../ai_workflow/WORKSTREAM_OWNERSHIP.md) |
| Autonomy model and its safety layers | [`../ai_workflow/AUTONOMY.md`](../ai_workflow/AUTONOMY.md) |
| Keeping, archiving, or deleting a document | [`../ai_workflow/DOC_RETENTION.md`](../ai_workflow/DOC_RETENTION.md) |
| Navigation spine for all of the above | [`../ai_workflow/INDEX.md`](../ai_workflow/INDEX.md) |

In short: work is scoped in a `docs/<feature>/PLANNING.md`, sized against the plan-stage routing
table, reviewed by the three-agent council when it is large or ambiguous, gated on the
change-type table, and recorded on merge. The active feature plan is the engineering plan.

---

## Re-verifying this suite

Nothing here is enforced by a committed test, and that is deliberate. A parity test between a
document and the code would turn every future route or schema change into a documentation-editing
change, and it would be stricter than what this suite promises: on conflict, the code wins, so
the document is allowed to lag until someone updates it.

What replaces the test is this — three commands that regenerate the ground truth these documents
were written from. Run them from the repository root when you need to know whether the suite has
drifted.

**Routes.** Every rule the application registers, with its methods:

```bash
HT_RUNTIME_DIR=<scratch-dir> .venv/Scripts/python.exe -c "import app; [print(sorted((r.methods or set()) - {'HEAD','OPTIONS'}), r.rule, r.endpoint) for r in app.app.url_map.iter_rules()]"
```

`HT_RUNTIME_DIR` matters. Importing `app` runs the real startup sequence, which resolves and
writes a database; without an isolated runtime root it will use the checkout's own.

**Schema.** The full field-level inventory, derived twice — once from an empty file and once
from the shipped catalog seed, which is what a real first run copies:

```bash
DB_FILE=<scratch>/a.db .venv/Scripts/python.exe -c "from utils.schema_registry import run_all_initializers; run_all_initializers(force_base=True)"
# then read it back with PRAGMA table_info / index_list / index_info / foreign_key_list
```

Both paths must agree; `BACKEND_SCHEMA.md` records that they currently do.

**Design tokens.** Definitions and their real consumers:

```bash
# what is defined (79 at the pinned revision)
grep -oE -- "--[A-Za-z0-9-]+\s*:" static/css/tokens.css | sort -u

# what is actually used, ranked by consumer count
grep -roE -- "var\(\s*--[A-Za-z0-9-]+" static/css/*.css \
  | sed 's/.*var(\s*//' | sort | uniq -c | sort -rn
```

The `sed` is not optional — `grep -r` prefixes each match with its filename, so without it
`uniq -c` counts file-token pairs instead of tokens.

A token that is defined and never referenced owns nothing on screen. `DESIGN_BRIEF.md` marks
those explicitly, because a token's presence in `tokens.css` is not evidence that it shipped.

---

## Retention

`docs/product/**` is classified **Always active** in
[`../ai_workflow/DOC_RETENTION.md`](../ai_workflow/DOC_RETENTION.md). It is not a feature
workstream and must not be archived when one closes. No file in this directory may be named
`PLANNING.md` or `EXECUTION_LOG.md` — those names are claimed by the Active-workstream retention
class and by the `/status` sweep, and would contradict this classification.

The plan and council review that produced this suite are recorded in
[`../PRODUCT_DOCS_PLAN.md`](../PRODUCT_DOCS_PLAN.md) §8.
