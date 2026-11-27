import { frameConfig } from './playwright.frame.config';

// Kept so the Log's own config path still selects its check. Every route, the Log
// included, is now launched through playwright.frame.config.ts.
export default frameConfig('workout-log-frame.check.ts');
