import { defineConfig } from 'vitest/config';

// Plain-JavaScript Vitest scaffold (Refactor Plan v3 WP3.1). No TypeScript.
//
// `environment: 'node'` is the default because the seeded suite covers only
// genuinely pure helpers (no DOM). DOM/Bootstrap modules (e.g. toast.js) are
// deferred; when they are tested they must opt into jsdom per-file with a
//   // @vitest-environment jsdom
// docblock and stand up explicit DOM + Bootstrap fakes — never treated as
// trivial pure helpers. `jsdom` is installed as a devDependency for that use.
//
// `include` is scoped to co-located `*.test.js` files under static/js so this
// runner never collides with the Playwright E2E suite (e2e/*.spec.ts) or the
// pytest suite (tests/test_*.py).
export default defineConfig({
    test: {
        environment: 'node',
        include: ['static/js/**/*.test.js'],

        // Phase 1 step 6 of docs/TESTING_STRATEGY_PLANNING.md. REPORT-ONLY: no
        // `thresholds` key, so `vitest run --coverage` can report any number
        // without failing. The js-unit job stays non-required (decision D2's
        // js-unit half is explicitly NOT signed), so nothing here gates a merge.
        //
        // `all: true` is the whole point. Without it v8 reports only files a test
        // imported, which would score the 8 covered modules and silently omit the
        // 41 that have no test at all -- a flattering number that hides blindspot
        // B7. With it, every module under static/js counts, including the ones at
        // zero.
        coverage: {
            provider: 'v8',
            all: true,
            include: ['static/js/**/*.js'],
            exclude: ['static/js/**/*.test.js'],
            reporter: ['text-summary', 'json-summary', 'html'],
            reportsDirectory: 'artifacts/js-coverage',
        },
    },
});
