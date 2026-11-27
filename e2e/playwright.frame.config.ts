import { defineConfig } from '@playwright/test';
import path from 'node:path';
import defaults from '../playwright.config';

// The default test pattern would select every spec, so no check file selects nothing.
const NO_CHECK = 'no-frame-check-selected';

/**
 * The config of every frame-check route (#736, R21): one worker, no retries and the
 * launcher's own scratch server, never a reused one. `e2e/scripts/run_frame_check.py`
 * names the route's check file in FRAME_CHECK.
 */
export function frameConfig(check: string | undefined) {
  if (check !== undefined && !/^[\w-]+\.check\.ts$/.test(check)) {
    throw new Error(`A frame check is a .check.ts file in e2e/, got ${check}`);
  }
  const run = process.env.FRAME_RUN;
  const baseURL = process.env.FRAME_URL;
  return defineConfig({
    testDir: __dirname,
    testMatch: check ?? NO_CHECK,
    workers: 1,
    retries: 0,
    timeout: 180_000,
    reporter: 'list',
    projects: defaults.projects?.filter(project => project.name === 'chromium'),
    use: { ...defaults.use, baseURL },
    outputDir: run && path.join(run, 'playwright'),
    webServer: run && baseURL ? {
      command: `"${process.env.FRAME_PYTHON}" "${process.env.FRAME_SERVER}" --serve`,
      cwd: process.env.FRAME_SOURCE,
      url: new URL('/__frame_identity', baseURL).href,
      reuseExistingServer: false,
    } : undefined,
  });
}

export default frameConfig(process.env.FRAME_CHECK);
