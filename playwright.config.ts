import { defineConfig, devices } from '@playwright/test';
import fs from 'fs';
import path from 'path';

const venvPython = process.platform === 'win32'
  ? path.join(process.cwd(), '.venv', 'Scripts', 'python.exe')
  : path.join(process.cwd(), '.venv', 'bin', 'python');
const pythonExecutable = fs.existsSync(venvPython) ? `"${venvPython}"` : 'python';
const reuseExistingServer = process.env.PW_REUSE_SERVER === '1' && !process.env.CI;
const configuredWorkers = Number(process.env.PW_WORKERS ?? '1');
const workers = Number.isFinite(configuredWorkers) && configuredWorkers > 0 ? configuredWorkers : 1;
const artifactsRoot = process.env.TEST_ARTIFACTS_DIR ?? 'artifacts';
const playwrightArtifactsDir = path.join(artifactsRoot, 'playwright');

/* One port resolves every URL in this file: the port Flask listens on, the URL
   webServer polls for readiness, and the baseURL specs navigate against. They
   are derived from a single binding rather than written out three times because
   the failure mode of a mismatch is not a clear error — the server comes up
   fine on one port, the browser drives another, and the run hangs until the
   120s webServer timeout with nothing pointing at the cause.

   Defaults are unchanged: unset PW_PORT is 5000, exactly as before. */
const DEFAULT_PORT = 5000;
const DEFAULT_HOST = '127.0.0.1';

function resolvePort(): number {
  const raw = process.env.PW_PORT;
  if (raw === undefined || raw === '') {
    return DEFAULT_PORT;
  }
  const parsed = Number(raw);
  if (!Number.isInteger(parsed) || parsed < 1 || parsed > 65535) {
    throw new Error(`PW_PORT must be an integer between 1 and 65535, got "${raw}".`);
  }
  return parsed;
}

const port = resolvePort();
const baseURL = process.env.PW_BASE_URL || `http://${DEFAULT_HOST}:${port}`;

/* PW_BASE_URL exists to point a run at an already-running server (with
   PW_REUSE_SERVER=1). Letting it disagree with PW_PORT would reintroduce
   exactly the split this block removes, so it is a hard error rather than a
   precedence rule someone has to remember. */
if (process.env.PW_BASE_URL) {
  const declaredPort = new URL(baseURL).port || '80';
  if (declaredPort !== String(port)) {
    throw new Error(
      `PW_BASE_URL (${baseURL}) and the resolved port (${port}) disagree. ` +
      'Flask would listen on one port while the tests drove another. ' +
      'Set PW_PORT to match, or leave PW_BASE_URL unset to derive it.'
    );
  }
}

/* CI-only JUnit reporter, gated on process.env.CI so local `npx playwright test`
   (and the --update-snapshots visual-baseline workflow) keep the interactive
   list + html reporters untouched. Each CI job runs on its own runner, so a
   fixed filename never collides — the uploaded artifact is named per job. */
const ciReporters: import('@playwright/test').ReporterDescription[] = process.env.CI
  ? [['junit', { outputFile: path.join(playwrightArtifactsDir, 'junit.xml') }]]
  : [];

/* Throwaway DB the web server runs against (under gitignored artifacts/), so the
   suite never touches the developer's live data/database.db. It is seeded by the
   web-server command itself — Playwright starts webServer before globalSetup, so
   seeding in globalSetup would race the server's first DB open (CI failure).

   PW_DB_PATH gives a concurrent run its own file. Two Playwright processes
   sharing one SQLite path is not a slow run, it is a corrupt one, so the DB is
   parameterized alongside the port rather than after someone hits it. The
   seeder creates the parent directory and refuses live-data paths itself, so an
   arbitrary value here is safe. Unset keeps the previous literal path. */
const e2eDbPath = path.resolve(
  process.cwd(),
  process.env.PW_DB_PATH || path.join('artifacts', 'e2e', 'database.e2e.db')
);
/* PW_VISUAL_SEED=1 seeds the throwaway DB with the full visual fixture (plan rows
   + media_path thumbnails preserved) instead of the user-state-wiped functional
   seed, so the visual specs get their data from the web server before Flask opens
   the DB — no per-spec runtime DB rewrite. Default (unset) keeps the functional
   suite on prepare_e2e_db.py. */
const seedScript = process.env.PW_VISUAL_SEED === '1' ? 'prepare_visual_db.py' : 'prepare_e2e_db.py';
const seedDbCommand = `${pythonExecutable} ${path.join('e2e', 'scripts', seedScript)} --output "${e2eDbPath}"`;
const defaultViewport = { width: 1440, height: 900 };
const deterministicChromiumArgs = [
  '--disable-font-subpixel-positioning',
  '--font-render-hinting=none',
  '--disable-gpu',
  '--disable-skia-runtime-opts',
  '--run-all-compositor-stages-before-draw',
  '--disable-threaded-animation',
  '--disable-threaded-scrolling',
  '--disable-checker-imaging',
  '--disable-image-animation-resync',
  '--force-color-profile=srgb',
];

/**
 * Playwright configuration for Hypertrophy Toolbox E2E tests
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './e2e',
  /* Run tests in files in parallel */
  fullyParallel: false,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ['list'],
    ['html', { outputFolder: path.join(playwrightArtifactsDir, 'report') }],
    ...ciReporters,
  ],
  outputDir: path.join(playwrightArtifactsDir, 'test-results'),
  snapshotPathTemplate: '{testDir}/__screenshots__/{platform}/{testFilePath}-snapshots/{arg}{ext}',
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. Specs and the
       `request` fixture both resolve relative paths against this, which is why
       none of them spell out a host. */
    baseURL,
    locale: 'en-US',
    timezoneId: 'UTC',
    colorScheme: 'light',
    viewport: defaultViewport,
    deviceScaleFactor: 1,
    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',
    /* Screenshot on failure */
    screenshot: 'only-on-failure',
    /* Video recording */
    video: 'on-first-retry',
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        locale: 'en-US',
        timezoneId: 'UTC',
        colorScheme: 'light',
        viewport: defaultViewport,
        deviceScaleFactor: 1,
        launchOptions: {
          args: deterministicChromiumArgs,
        },
      },
    },
    // Uncomment to add more browsers
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],

  /* Run your local dev server before starting the tests */
  webServer: {
    /* Seed the throwaway DB, then start the app against it. Seeding here (not in
       globalSetup) guarantees the DB exists before app.py's first open. */
    command: `${seedDbCommand} && ${pythonExecutable} app.py`,
    url: baseURL,
    reuseExistingServer,
    timeout: 120 * 1000,
    /* Isolated throwaway DB under gitignored artifacts/, never the developer's
       live data/database.db.

       HT_PORT is the app's own existing knob (utils.config.runtime_port), not a
       new one — app.py already serves on it. Passing the same resolved `port`
       that produced baseURL above is what makes the server and the browser
       agree by construction. */
    env: {
      ...process.env,
      DB_FILE: e2eDbPath,
      HT_PORT: String(port),
    },
  },

  /* Global timeout settings */
  timeout: 30000,
  expect: {
    timeout: 10000,
  },
});
