# Deep-gate robustness — bounded Gate-1 plan

## Objective

Make the `full-e2e` selection exact and fail-closed while preserving today's
observable selection: 30 functional specs out of 33 total. Keep the newly
pinned no-baseline-write assertion behavior unchanged.

Gate 1 requires separate authorization. This Gate-0 packet does not implement
the workflow change.

## Permitted change set

1. `.github/workflows/deep-gate.yml`
   - replace the `ls | grep -vE | tr` scalar pipeline with a Bash array;
   - enumerate `e2e/*.spec.ts` with `nullglob` or an equivalent fail-closed
     mechanism;
   - exclude the three exact relative paths by literal membership, never by
     substring;
   - require all three declared exclusions to exist;
   - require at least one selected functional spec;
   - pass each spec as its own quoted argument to Playwright.
2. `tests/test_playwright_runner_contracts.py`
   - replace the temporary current-ERE characterization with a semantic
     exact-set contract over real and fabricated inventories;
   - promote/adapt the ignored intended-red cases so they turn green;
   - retain the exact visual-seed group and `visual-field-separator` prefix-trap
     contracts.
3. `tests/test_release_workflow_contracts.py`
   - retain the green unique/order/body contract for the no-baseline guard;
   - add mutation arms only if they can reuse an existing node or the generated
     test inventory is updated as required.

The implementation should prefer an array plus literal `case` arms and
`${#SPECS[@]}` checks. Avoid a new `mapfile < <(grep ...)` construction: process
substitution can hide producer failures in another form.

## Intended contract

For discovered set `D`, exact visual-seed set `V`, and selected functional set
`F`:

```text
V = {
  e2e/visual.spec.ts,
  e2e/visual-baseline-thumbnails.spec.ts,
  e2e/workout-plan-desktop-contract.spec.ts
}

V is a subset of D
F is nonempty
F and V are disjoint
F union V equals D
```

Every element of `F` is one Playwright argument. Names that merely contain an
excluded leaf remain in `F`.

## Required Gate-1 tests

The contract must cover:

- current inventory: 33 discovered, 3 exact exclusions, 30 selected;
- each exact excluded file missing or renamed: fail before Playwright;
- empty inventory: fail before Playwright;
- excluded-only inventory: fail before Playwright;
- representative near names such as `nonvisual.spec.ts`,
  `not-visual-baseline-thumbnails.spec.ts`, and
  `pre-workout-plan-desktop-contract.spec.ts`: included;
- selector deletion, nonempty-guard deletion, and Playwright-invocation
  deletion: contract red rather than vacuous;
- arguments containing legal filename punctuation remain separate quoted argv
  items;
- the no-baseline guard remains uniquely and immediately after the visual step,
  with its current condition/body/failing exit.

The ignored Gate-0 test is evidence, not necessarily final source shape. Adapt
it around the implemented array semantics.

## Verification gate

Because Gate 1 changes a CI workflow, run:

1. the two targeted workflow/Playwright contract files;
2. `scripts/generate_test_inventory.py --check`, regenerating the two committed
   inventory artifacts only if pytest node counts actually change;
3. full `pytest tests/ -q`, as required for `.github/workflows/**`;
4. collection-only Playwright comparison showing explicit selection remains
   586 tests / 30 files and empty/failure fixtures stop before Playwright;
5. a code review focused on Bash failure propagation, quoting, exact-set
   completeness, and vacuity/mutation strength.

No live workflow dispatch is required to establish the selection semantics.

## Explicitly out of scope

- Playwright retries or flaky classification;
- artifact upload predicates, paths, retention, or flaky-success retention;
- visual spec membership or seed routing;
- Playwright configuration;
- job/step names, triggers, runner images, timeouts, or branch protection;
- baseline or seed regeneration;
- the no-baseline guard's workflow body;
- the three falsified-artifact correction files;
- any merge of the Gate-0 or Gate-1 PR without separate owner action.
