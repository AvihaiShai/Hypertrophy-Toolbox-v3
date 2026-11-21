import { defineConfig } from '@playwright/test';
import path from 'node:path';
import defaults from '../playwright.config';

const run = process.env.FRAME_RUN;
const baseURL = process.env.FRAME_URL;

export default defineConfig({
  testDir: __dirname,
  testMatch: 'workout-log-frame.check.ts',
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
