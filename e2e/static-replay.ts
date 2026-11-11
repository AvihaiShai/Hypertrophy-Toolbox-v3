/**
 * Static-asset replay for the E2E harness (ADR-014).
 *
 * Every request opens a loopback connection that holds a client port in
 * TIME_WAIT for about two minutes, and at N=1 that density alone makes some
 * Windows connects fail. Repeated static GETs are therefore answered from
 * memory; the server, the OS and the served bytes are unchanged.
 *
 * Only a `200` that the network served (not a spec mock) for a plain `GET`
 * under the run's own `/static/`, carrying Flask's `ETag` and `Last-Modified`,
 * is recorded. Conditional and Range requests always reach the server, so they
 * keep their real `304`/`206`. Routing disables a context's HTTP cache, so
 * revalidation is only exercised with replay off: `PW_STATIC_REPLAY=0` for a
 * run, or the `staticReplay` option for a block.
 */
import { test as base, type BrowserContext, type Request, type Response } from '@playwright/test';

interface RecordedAsset {
  headers: Record<string, string>;
  body: Buffer;
}

// One cache per Playwright worker process. A worker never outlives the
// `playwright test` invocation that owns the web server, and keys are full
// URLs including origin, so no entry can be replayed against another server run.
const recorded = new Map<string, RecordedAsset>();

// Request headers whose answer is not the full 200 a recording holds.
const SERVER_ONLY_REQUEST_HEADERS = ['range', 'if-range', 'if-none-match', 'if-modified-since'];

// Response headers that describe one exchange rather than the asset.
const PER_EXCHANGE_RESPONSE_HEADERS = ['date', 'connection', 'x-request-id'];

function isStaticPath(url: URL, origin: string): boolean {
  return url.origin === origin && url.pathname.startsWith('/static/');
}

async function recordIfEligible(response: Response, missed: WeakSet<Request>): Promise<void> {
  const request = response.request();
  if (!missed.has(request) || response.status() !== 200) return;
  const headers = { ...response.headers() };
  if (!headers['etag'] || !headers['last-modified']) return;
  if ((await response.serverAddr()) === null) return;
  for (const name of PER_EXCHANGE_RESPONSE_HEADERS) delete headers[name];
  recorded.set(request.url(), { headers, body: await response.body() });
}

// Recordings still reading a body. Tests await them before asserting that
// something was *not* recorded, which would otherwise pass by racing.
const pending = new Set<Promise<void>>();

export function isStaticAssetRecorded(url: string): boolean {
  return recorded.has(url);
}

export async function staticRecordingsSettled(): Promise<void> {
  await Promise.all([...pending]);
}

export async function installStaticReplay(context: BrowserContext, origin: string): Promise<void> {
  const missed = new WeakSet<Request>();
  context.on('response', (response) => {
    // A page or context that closes before the body is read only loses this
    // cache entry; the request itself was already served natively.
    const attempt = recordIfEligible(response, missed)
      .catch(() => {})
      .finally(() => pending.delete(attempt));
    pending.add(attempt);
  });
  await context.route(
    (url) => isStaticPath(url, origin),
    async (route) => {
      const request = route.request();
      const headers = request.headers();
      if (request.method() !== 'GET' || SERVER_ONLY_REQUEST_HEADERS.some((name) => name in headers)) {
        await route.fallback();
        return;
      }
      const hit = recorded.get(request.url());
      if (hit) {
        await route.fulfill({ status: 200, ...hit });
        return;
      }
      missed.add(request);
      await route.fallback();
    },
  );
}

export const test = base.extend<{ staticReplay: boolean }>({
  staticReplay: [process.env.PW_STATIC_REPLAY !== '0', { option: true }],
  context: async ({ context, staticReplay, baseURL }, use) => {
    if (staticReplay && baseURL) {
      await installStaticReplay(context, new URL(baseURL).origin);
    }
    await use(context);
  },
});
