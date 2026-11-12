# #565 — serial Windows Chromium socket-allocation failures

Owning issue: [#565](https://github.com/AvihaiShai/Hypertrophy-Toolbox-v3/issues/565).
Planning size: **Medium** under [`QUALITY_GATE.md`](../ai_workflow/QUALITY_GATE.md#plan-stage-routing).
The change is bounded to the E2E harness, with no schema, API or calculation surface. It needs
**Gate 1** (owner plan approval). The remedy uses a lever that ADR-006 names as out of bounds
without an owner decision (asset cache policy, applied here inside the test harness), so
Gate 1 also covers that decision explicitly.

## 1. Evidence

### 1.1 What survives from earlier runs

The October raw campaign directories cited in #565 are **not available**. They lived in a
worktree whose archives were deliberately deleted at the end of the cleanup campaign. Only
their summaries in #565, its comments and `docs/python315_migration/` survive. The Windows
System log does survive: it holds Tcpip 4227 and 4231 events dated across 2026-08 to 2026-11,
including the October campaign days. Windows throttles these events to a few per day, so
their counts show dates only, not frequencies.

### 1.2 New measurements (2026-11-11, unchanged `main` at `04816d8d`)

Host state: Windows 11, booted 2026-11-10 (the post-reboot observation; no new reboot was
requested). Dynamic TCP range 49152–65535 (16,384 ports), 60 administered exclusions, no
`TcpTimedWaitDelay` override. Toolchain: Python 3.15.1, Node 26, Playwright 1.61.0, Werkzeug
3.1.9, Flask 3.1.3.

**Connection-lifecycle probe.** Ten cold navigations to five pages against an isolated server:

- 65–77 same-origin requests per navigation. A second navigation in the same context costs
  the same number, because `no-cache` revalidation sends a request per asset.
- Werkzeug 3.x sends `Connection: close` on every response. Its source says it "always
  close[s] the connection", so keep-alive cannot be turned on there.
- **Chromium performs the active close.** 671 TIME_WAIT entries sat on the client's
  dynamic ports, against 1 on the server's port. Each request therefore holds one dynamic port.
- The hold lasted **about 120 s**: all 671 entries drained between 115 and 125 s after the probe ended.

**Observed canonical run D1.** `npm run test:e2e` with no arguments, one worker, zero retries,
`CI` unset, and a fresh isolated runtime, database and port. A 1 s TCP sampler and the server
access log recorded the run:

| Measure | Value |
|---|---|
| Functional partition | **575 passed, 16 failed / 591**, 12.2 min. Visual partition **did not run** (the runner stops after a functional failure) |
| Server requests (functional) | 43,302; 91.9% `/static/`; mean 59.6/s; peak 364/s |
| Worst 120 s window | 11,173 requests (68% of the usable range) |
| Peak client TIME_WAIT | 13,160 (81%). Server-side TIME_WAIT max 2; BOUND max 6 |
| Tcpip events in window | 4227 at 01:22:42Z and 01:28:55Z; 4231 at 01:30:14Z |
| Process cleanup | No listener left on the port; no process left referencing the run; no app or browser process from the run left alive |

The 16 failures fall into two unrelated causes:

1. **Environment drift, 14 failures.** The checkout's `node_modules` was installed on
   2026-10-17, before #524 moved `@axe-core/playwright` to 4.14.0. Every axe test failed
   its engine-version guard (`axe-core 4.13.0 is running`). This is not a socket failure.
   `npm ci` against the committed lockfile fixes it.
2. **Socket allocation, 2 failures.** In `program-backup.spec.ts:730`, a backup POST failed
   with `Failed to fetch` at about 01:22:42Z. That is the same second as event 4227, with about
   10,020 client TIME_WAIT (61%). In `workout-plan.spec.ts:980`, the console guard recorded
   `net::ERR_NO_BUFFER_SPACE` on a loopback resource at about 01:30:14Z. That is the same second
   as event 4231, with about 7,360 client TIME_WAIT (45%). The test's YouTube embed is
   route-mocked, so the failed request was not external.

### 1.3 Findings

- **Supported.** At N=1 the suite opens one loopback TCP connection per request. Each one
  leaves a client-side TIME_WAIT on a dynamic port for about 120 s, and every one of those
  entries points at the same remote endpoint. At the suite's request rate, those entries
  fill 45–81% of the dynamic range. Windows then fails some outgoing connects. It logs 4227
  (a local port reused against a recent TIME_WAIT to the same endpoint) or 4231 (allocation
  failure). Chromium surfaces these as `ERR_ADDRESS_IN_USE`, `ERR_NO_BUFFER_SPACE` or a
  failed `fetch()`. A failed module or API request then leaves a page partly initialized.
- **Not supported.** The failures do not require the whole range to be in use. Event 4231
  fired at 45% observed occupancy. This plan does not explain the Windows allocator's
  internals; it relies only on the measured density at which failures occur.
- **Not established.** The October `validation-boundary.spec.ts:232` `selectRoutine` timeout
  is the example. It passed in D1, and its raw evidence is gone, so no cause is assigned to it.
  Native 10055 is the WinSock code behind Chromium's `ERR_NO_BUFFER_SPACE`. D1 saw it only
  through that browser error.

## 2. Options considered

| Option | Effect on connections | Why accepted or rejected |
|---|---|---|
| **A. Test-harness static replay** (recommended) | −92% (simulated from D1's access log: 43,302 → ~3,663; worst window 11,173 → ~883) | Test-only. No product, server, OS or dependency change. Cost: after the first fetch, each `/static/` GET is answered from memory instead of by Flask. Needs owner approval as a cache-policy lever |
| B. OS tuning (TIME_WAIT delay, range size) | Indirect | Becomes a property of one machine, not the repository (ADR-006) |
| C. Server keep-alive / another WSGI server | Large | Werkzeug 3 cannot keep connections alive, so this means a production server change or a new dependency (ADR-006) |
| D. Pacing gate (wait for TIME_WAIT to drain) | None; spreads the same load over time | Steady state (~60/s × 120 s ≈ 7,200) is already inside the observed failure band, so pacing would roughly double run time. Its threshold would be specific to one machine |
| Retries, longer timeouts, allowlisting `ERR_*`, shared contexts | — | Forbidden: they buy green by weakening the gate |

## 3. Gate 1 decision (owner, 2026-11-11)

The owner approved `npm ci` and option A, subject to six requirements. Each is quoted, then
followed by how this plan meets it.

1. *Restore dependencies from the committed lockfile first; keep `package.json` and the lockfile
   unchanged.* Done before any implementation. The hashes of both files were unchanged, and
   `@axe-core/playwright` and `axe-core` are now at 4.14.0.
2. *Limit replay to immutable, same-origin static assets. Never replay APIs, HTML pages,
   non-GET requests, unsuccessful responses or responses supplied by another test's mocks.*
   A response is replayed only if it meets all of these conditions:
   - it answered a plain `GET` (no `Range`, `If-Range`, `If-None-Match` or
     `If-Modified-Since`) to the run's own origin under `/static/`; those headers always
     reach the server, so a real `206`/`304` is never answered from a recording;
   - it came from the server over the network (`response.serverAddr()` is non-null);
   - it had status `200`;
   - it carried Flask's `send_file` validators (`ETag` and `Last-Modified`).
   **Interpretation, recorded for review.** "Immutable" here means *committed files served by
   Flask's `static` endpoint, which no application code writes during a run*. No route or
   utility writes under `static/`. The HTTP `immutable` directive cannot be the test. Source
   runs send `no-cache, must-revalidate` on every static file, and only a frozen build
   long-caches `?v=` URLs. A header-based rule would therefore replay nothing. In D1 that
   would have left 25,924 unversioned module and asset requests and 13,880 versioned ones
   untouched.
3. *Prevent cache contamination between tests and server runs; preserve spec-specific
   interception, including simulated missing or failing assets.* Four properties cover this:
   - Entries are recorded only from requests that reached this harness's own context route
     and were then served by the network.
   - A page route registered by a spec runs first. A spec mock that fulfils, aborts or
     `continue()`s is never seen by the replay route, so it can never be recorded or
     overridden.
   - The cache is per Playwright worker process, so it cannot outlive one `playwright test`
     invocation and its single web server.
   - Keys are full URLs, including origin and port.
4. *Keep an explicit replay-disabled mode and a focused native-network regression selection
   covering real asset delivery, headers, cache behaviour and failure handling, passing
   alongside the replay-enabled suite.* There are two switches:
   - `PW_STATIC_REPLAY=0` disables replay for a whole run.
   - A `staticReplay` test option disables it for one block.

   The native selection is a `test.use({ staticReplay: false })` block in
   `smoke-navigation.spec.ts`, which is on the required CI path. Playwright disables a
   context's HTTP cache once routing is enabled, so revalidation can only be observed
   natively; that is one more reason the block runs without replay. It asserts:
   - real delivery: every asset on a full page load comes from the server with the right
     type, and the page initializes;
   - the source-run static headers: `Cache-Control`, `ETag` and `Last-Modified`;
   - `304` revalidation on a second navigation;
   - a missing asset `404`s natively every time.

   It runs inside every canonical run and also on its own under `PW_STATIC_REPLAY=0`.
5. *Demonstrate the reduction with actual measurements; preserve all test identities, zero
   retries, existing assertions and error reporting.* Acceptance measures server requests and
   client TIME_WAIT on a real run, compared with D1. No existing test, assertion, allowlist,
   timeout or retry setting changes. Tests are only added.
6. *Record the coverage trade-off in the ADR.* ADR-014 states that this mitigates
   connection pressure in the test harness. It does not show that the Windows allocation
   mechanism or the production server behaviour changed.

## 4. Plan

1. **`e2e/static-replay.ts`.** It holds a per-worker cache, `installStaticReplay(context, origin)`,
   and the shared `test` base with a `staticReplay` option (default: on unless
   `PW_STATIC_REPLAY=0`). The option overrides the `context` fixture, so the default `page`
   inherits it.
   - On a cache miss, the route calls `route.fallback()`, so the browser fetches natively.
   - The response is recorded only if it meets requirement 2.
   - Recording is skipped when a body cannot be read, for example because the page closed
     first. That request was already served natively.
2. **Wiring.** `fixtures.ts` and `console-guard.ts` extend the replay base, and
   `strict-fixtures.ts` inherits from `console-guard.ts`. Two specs are named exceptions:
   - `api-integration.spec.ts` uses only `request` and opens no browser;
   - `visual-baseline-thumbnails.spec.ts` builds 18 contexts of its own in the visual
     partition and stays native.
3. **Regression coverage.** The new replay and native blocks go in `smoke-navigation.spec.ts`.
   The replay block asserts the following on cold, unique URLs:
   - a second context gets a replay with identical bytes and validators, without the
     original exchange's `X-Request-ID`;
   - API, HTML, non-GET and `404` responses always reach the server;
   - a conditional `304` and a `Range` `206` are never recorded, and a recorded `200` never
     answers either kind of request;
   - a spec's page-route mock wins and is never recorded.

   The contract also confines `staticReplay`/`PW_STATIC_REPLAY` and `browser.newContext(`
   to this spec and the named exceptions.

   The native block is described under requirement 4. A pytest contract,
   `tests/test_static_replay_contracts.py`, binds the wiring and exceptions. `docs/test_inventory/`
   is regenerated.
4. **Docs.** ADR-014, plus the local-parallelism and fixture notes in `e2e/CLAUDE.md` and
   `.claude/rules/testing.md`.
5. **Synchronization found by the first replay run (D2).** D2 failed one test,
   `ui-hardening.spec.ts:964` (TS-3): `#min_rep` was `6` where the user had entered `10`.
   - **Cause.** An instrumented rerun showed the exercise recommendation landing in the
     middle of the test's `setAllControls`. The test's comment says the recommendation should
     land first, but nothing waited for it. Routing makes Playwright intercept every request
     in a context, APIs included, which delays the estimate response.
   - **Effect of replay.** Unchanged, the test failed 17 of 30 repeats with replay on and
     passed 30 of 30 with it off.
   - **Fix.** `selectFirstExercise()` now waits for the app's existing
     `data-workout-controls-busy` marker to clear. The test passes 30 of 30 in both modes, and
     the whole spec passes 37 of 37 in both. No assertion, timeout or retry changed.

## 5. Acceptance

- Targeted: the smoke spec passes with replay on and under `PW_STATIC_REPLAY=0`. The contract
  test and the full pytest suite pass.
- **Complete canonical run.** `npm run test:e2e` with no arguments, one worker, zero retries,
  observed as in D1. The functional and visual partitions are reported separately, with
  every collected identity counted. A partition that did not run is incomplete.
- Measured: server requests, the worst 120 s window and peak client TIME_WAIT, compared with
  D1. Any Tcpip 4227/4231 inside the run window is reported.
- `/unslop` reviewers (`code-reviewer`, `unslop-reviewer`); CI green at the exact PR head.
- Remaining limits are stated. ADR-006 is unchanged. The first fetch of each asset per
  worker still uses the network. The `visual-baseline-thumbnails` spec and every `request`
  fixture call stay native.
