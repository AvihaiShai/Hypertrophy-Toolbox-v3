// @vitest-environment jsdom
// U1-FOLLOWUP-1, Plan v2: exercise the six calculate-failure helpers through
// initializeVolumeSplitter(). Real toast.js supplies output and arrangements;
// its KI-011 helpers are not separate coverage or mutation targets here.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const apiMocks = vi.hoisted(() => ({ post: vi.fn(), get: vi.fn() }));
vi.mock('../fetch-wrapper.js', () => ({ api: apiMocks }));

const MSG = 'Volume calculation failed, so no results are shown. Please try again.';
const RETRY_SEL = 'button[aria-label="Retry volume calculation"]';
const FLUSH_DEPTH = 20;
// Reduced from templates/volume_splitter.html and base.html. History is outside
// the insights panel so the no-panel case still has a working history loader.
const FIXTURE = `
<button id="volume-active-summary" type="button">x</button>
<div id="volume-splitter-app"
     data-basic-muscles='["Chest","Back"]'
     data-advanced-muscles='["Upper Chest"]'
     data-basic-ranges='{}'
     data-advanced-ranges='{}'
     data-default-mode='basic'>
  <select id="training-days"><option value="3" selected>3</option></select>
  <input type="radio" name="volume-mode" id="mode-basic" value="basic" checked>
  <input type="radio" name="volume-mode" id="mode-advanced" value="advanced">
  <button id="calculate-volume">Calculate</button>
  <button id="reset-volume">Reset</button>
  <div id="sliders"></div>
  <aside class="volume-insights-panel">
    <div class="results-section d-none"><table><tbody id="results-body"></tbody></table></div>
    <div class="ai-suggestions-section d-none"><div class="suggestions-container"></div></div>
  </aside>
  <table><tbody id="history-body"></tbody></table>
</div>
<div class="position-fixed toast-container">
  <div id="liveToast" class="toast align-items-center text-white border-0"
       role="alert" aria-live="assertive" aria-atomic="true">
    <div class="d-flex">
      <div class="toast-body" id="toast-body"></div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto"
              data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  </div>
</div>`;

const SUCCESS = {
    results: { Chest: { weekly_sets: 10, sets_per_session: 3, status: 'optimal' } },
    suggestions: [],
};
// displayResults reads data.status on null, producing a post-2xx handling failure.
const HANDLING_FAIL = { results: { Chest: null } };
const REQ_ERR = { code: 'SERVER_ERROR', message: 'boom', requestId: null };

let pending;
let toastLog;
let strangerShows;
let FakeToast;
let toast;
let errorSpy;

function installApi() {
    pending = [];
    apiMocks.post.mockReset();
    apiMocks.post.mockImplementation((url, body, options) => new Promise((resolve, reject) => {
        pending.push({ url, body, options, resolve, reject });
    }));
    apiMocks.get.mockReset();
    apiMocks.get.mockResolvedValue({ data: {} });
}

function installBootstrap() {
    toastLog = [];
    strangerShows = new Set();
    const registry = new Map();
    FakeToast = class {
        constructor(element, options) {
            this.element = element;
            this.options = options;
            registry.set(element, this);
            toastLog.push({ ev: 'construct' });
        }
        show() {
            const button = this.element.querySelector('.toast-action-slot > button');
            toastLog.push({
                ev: 'show',
                message: document.querySelector('#toast-body span.toast-message')?.textContent ?? null,
                danger: this.element.classList.contains('bg-danger'),
                actionLabel: button?.textContent ?? null,
                actionAria: button?.getAttribute('aria-label') ?? null,
            });
        }
        hide() { toastLog.push({ ev: 'hide' }); }
        dispose() {
            registry.delete(this.element);
            toastLog.push({ ev: 'dispose' });
        }
    };
    FakeToast.getInstance = vi.fn(element => registry.get(element) ?? null);
    globalThis.bootstrap = { Toast: FakeToast, Modal: class { show() {} hide() {} } };
}

async function flush() {
    for (let index = 0; index < FLUSH_DEPTH; index += 1) {
        await Promise.resolve();
    }
}

const $ = selector => document.querySelector(selector);
const region = () => document.getElementById('volume-calculate-error');
const regions = () => document.querySelectorAll('#volume-calculate-error');
const rows = () => document.querySelectorAll('#results-body tr');
const slider = () => $('.volume-slider');
const liveToastBtn = () => $(`#liveToast ${RETRY_SEL}`);
const shows = () => toastLog.filter(entry => entry.ev === 'show');
// Only the test's own explicitly tagged stranger shows are excluded. No property
// checked by the shape assertion may also decide whether a show is counted.
const announcements = () => shows().filter(entry => !strangerShows.has(entry));
const hides = () => toastLog.filter(entry => entry.ev === 'hide').length;
const requestFailedLogs = () => errorSpy.mock.calls
    .filter(call => call[0] === 'Volume calculation: request failed').length;

const clickCalculate = () => $('#calculate-volume').click();
const clickReset = () => $('#reset-volume').click();
const clickRegionRetry = () => $('[data-testid="volume-calculate-retry"]').click();
const sliderChange = () => slider().dispatchEvent(new Event('change'));
const sliderInputDebounced = () => {
    slider().value = '7';
    slider().dispatchEvent(new Event('input'));
    vi.advanceTimersByTime(300);
};
const messageText = () => toast.toastMessageText();
const clickToastAction = () => $('#liveToast .toast-action-slot > button').click();
// Action expiry (toast.js per-action timer), independent of Bootstrap auto-hide.
const expireAction = () => vi.advanceTimersByTime(3001);

function setStrangerMessage(text) {
    const previousShows = new Set(shows());
    toast.showToast('info', text);
    for (const entry of shows()) {
        if (!previousShows.has(entry)) {
            strangerShows.add(entry);
        }
    }
}

function addSentinel() {
    const row = document.createElement('tr');
    row.id = 'sentinel';
    document.getElementById('results-body').appendChild(row);
}

function withGetter(payload) {
    const getter = vi.fn(() => payload);
    return { response: { get data() { return getter(); } }, getter };
}

async function failLast(error = REQ_ERR) {
    pending[pending.length - 1].reject(error);
    await flush();
}

async function succeedLast(payload = SUCCESS) {
    pending[pending.length - 1].resolve({ data: payload });
    await flush();
}

beforeEach(async () => {
    vi.useFakeTimers();
    errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    document.body.innerHTML = FIXTURE;
    installApi();
    installBootstrap();
    vi.resetModules();
    const module = await import('../volume-splitter.js');
    module.initializeVolumeSplitter();
    await flush();
    // Keep this import in the same module-registry generation as the module above.
    toast = await import('../toast.js');
});

afterEach(() => {
    try {
        for (const entry of announcements()) {
            expect(entry).toEqual({
                ev: 'show', message: MSG, danger: true,
                actionLabel: 'Retry', actionAria: 'Retry volume calculation',
            });
        }
    } finally {
        vi.clearAllTimers();
        vi.useRealTimers();
        errorSpy?.mockRestore();
        delete globalThis.bootstrap;
        apiMocks.post.mockReset();
        apiMocks.get.mockReset();
    }
});

describe('T-1 region idempotence', () => {
    it('2a repeat failure keeps the same single node and does not rewrite text', async () => {
        clickCalculate();
        await failLast();
        const node = region();
        expect(node).not.toBeNull();
        expect(node.dataset.testid).toBe('volume-calculate-error');
        expect($('.volume-insights-panel').firstElementChild).toBe(node);
        const span = node.querySelector('span');
        expect(span.textContent).toBe(MSG);
        const button = node.querySelector('button');
        expect(button.type).toBe('button');
        expect(button.dataset.testid).toBe('volume-calculate-retry');
        expect(button.getAttribute('aria-label')).toBe('Retry volume calculation');
        expect(node.hasAttribute('aria-live')).toBe(false);

        const records = [];
        const observer = new MutationObserver(changes => records.push(...changes));
        observer.observe(node, { subtree: true, childList: true, characterData: true, attributes: true });
        try {
            clickCalculate();
            await failLast();
            records.push(...observer.takeRecords());
        } finally {
            observer.disconnect();
        }

        expect(announcements()).toHaveLength(2);
        expect(regions()).toHaveLength(1);
        expect(region()).toBe(node);
        expect(node.querySelector('span')).toBe(span);
        expect(span.textContent).toBe(MSG);
        expect(records).toEqual([]);
    });

    it('2b no .volume-insights-panel: no region, nothing throws', async () => {
        $('.volume-insights-panel').className = 'not-the-panel';
        clickCalculate();
        await failLast();
        expect(announcements()).toHaveLength(1);
        expect(requestFailedLogs()).toBe(1);
        expect(regions()).toHaveLength(0);
    });

    it('2c-success next success removes the node from the DOM', async () => {
        clickCalculate();
        await failLast();
        const node = region();
        expect(node).not.toBeNull();
        clickCalculate();
        await succeedLast();
        expect(rows()).toHaveLength(1);
        expect(region()).toBeNull();
        expect(node.isConnected).toBe(false);
    });

    it('2c-reset reset removes the node from the DOM', async () => {
        clickCalculate();
        await failLast();
        const node = region();
        expect(node).not.toBeNull();
        slider().value = '5';
        clickReset();
        await flush();
        expect(slider().value).toBe('0');
        expect(region()).toBeNull();
        expect(node.isConnected).toBe(false);
    });
});

describe('T-2 announce condition', () => {
    it('3a explicit commands announce while region AND our message stand', async () => {
        clickCalculate();
        await failLast();
        expect(announcements()).toHaveLength(1);
        expect(region()).not.toBeNull();
        expect(messageText()).toBe(MSG);
        expect(liveToastBtn()).not.toBeNull();

        clickCalculate();
        await failLast();
        expect(announcements()).toHaveLength(2);

        clickRegionRetry();
        await failLast();
        expect(announcements()).toHaveLength(3);

        clickToastAction();
        await flush();
        await failLast();
        expect(announcements()).toHaveLength(4);

        $('#mode-advanced').checked = true;
        $('#mode-advanced').dispatchEvent(new Event('change'));
        await failLast();
        expect(announcements()).toHaveLength(5);
        expect(pending).toHaveLength(5);
    });

    it('3a-loadPlan loading a saved plan announces while region AND our message stand', async () => {
        clickCalculate();
        await failLast();
        expect(announcements()).toHaveLength(1);
        expect(region()).not.toBeNull();
        expect(messageText()).toBe(MSG);
        apiMocks.get.mockImplementation(url => Promise.resolve({
            data: url === '/api/volume_plan/4'
                ? { training_days: 3, mode: 'basic', volumes: { Chest: { weekly_sets: 6 } } }
                : {},
        }));
        const button = document.createElement('button');
        button.className = 'load-plan';
        button.dataset.planId = '4';
        $('#history-body').appendChild(button);
        const before = pending.length;
        button.click();
        await flush();
        expect(apiMocks.get).toHaveBeenCalledWith('/api/volume_plan/4', expect.anything());
        expect(pending).toHaveLength(before + 1);
        await failLast();
        expect(announcements()).toHaveLength(2);
    });

    it('3b slider-originated first failure announces (change)', async () => {
        sliderChange();
        await failLast();
        expect(region()).not.toBeNull();
        expect(announcements()).toHaveLength(1);
    });

    it('3b slider-originated first failure announces (debounced input)', async () => {
        sliderInputDebounced();
        expect(pending).toHaveLength(1);
        await failLast();
        expect(region()).not.toBeNull();
        expect(announcements()).toHaveLength(1);
    });

    it('3b-after-recovery slider failure after a success announces although our message text persists', async () => {
        clickCalculate();
        await failLast();
        clickCalculate();
        await succeedLast();
        expect(region()).toBeNull();
        expect(messageText()).toBe(MSG);
        sliderChange();
        await failLast();
        expect(region()).not.toBeNull();
        expect(announcements()).toHaveLength(2);
    });

    it('3c slider repeat while region and our message stand does NOT announce', async () => {
        clickCalculate();
        await failLast();
        expect(announcements()).toHaveLength(1);
        expect(messageText()).toBe(MSG);
        addSentinel();
        sliderChange();
        await failLast();
        expect($('#sentinel')).toBeNull();
        expect(requestFailedLogs()).toBe(2);
        expect(announcements()).toHaveLength(1);

        addSentinel();
        sliderInputDebounced();
        await failLast();
        expect($('#sentinel')).toBeNull();
        expect(requestFailedLogs()).toBe(3);
        expect(announcements()).toHaveLength(1);
    });

    it('3d slider repeat after a stranger replaced our message DOES announce, button still standing', async () => {
        clickCalculate();
        await failLast();
        setStrangerMessage('Plan #4 saved.');
        expect(liveToastBtn()).not.toBeNull();
        expect(messageText()).toBe('Plan #4 saved.');
        sliderChange();
        await failLast();
        expect(announcements()).toHaveLength(2);
    });

    it('3d-near-miss message probe is exact equality', async () => {
        clickCalculate();
        await failLast();
        setStrangerMessage(`${MSG} (Request ID: r1)`);
        expect(liveToastBtn()).not.toBeNull();
        sliderChange();
        await failLast();
        expect(announcements()).toHaveLength(2);
    });

    it('3e slider repeat after our button is gone but our message stands does NOT announce', async () => {
        clickCalculate();
        await failLast();
        expireAction();
        expect(liveToastBtn()).toBeNull();
        expect(messageText()).toBe(MSG);
        addSentinel();
        sliderChange();
        await failLast();
        expect($('#sentinel')).toBeNull();
        expect(requestFailedLogs()).toBe(2);
        expect(announcements()).toHaveLength(1);
    });
});

describe('T-3 request-sequence guard', () => {
    it('4a stale SUCCESS after a newer failure: no paint, no region removal, no dismiss', async () => {
        clickCalculate();
        clickCalculate();
        expect(pending).toHaveLength(2);
        pending[1].reject(REQ_ERR);
        await flush();
        const node = region();
        expect(node).not.toBeNull();
        expect(announcements()).toHaveLength(1);
        const beforeHides = hides();
        const { response, getter } = withGetter(SUCCESS);
        pending[0].resolve(response);
        await flush();
        expect(getter).toHaveBeenCalledTimes(1);
        expect(rows()).toHaveLength(0);
        expect(region()).toBe(node);
        expect(hides() - beforeHides).toBe(0);
        expect(announcements()).toHaveLength(1);
    });

    it('4b stale REQUEST FAILURE after a newer success: no region, no announce', async () => {
        clickCalculate();
        clickCalculate();
        pending[1].resolve({ data: SUCCESS });
        await flush();
        expect(rows()).toHaveLength(1);
        pending[0].reject(REQ_ERR);
        await flush();
        expect(rows()).toHaveLength(1);
        expect(region()).toBeNull();
        expect(announcements()).toHaveLength(0);
        expect(requestFailedLogs()).toBe(0);
    });

    it('4c stale POST-2xx HANDLING FAILURE after a newer success: no region, no announce', async () => {
        clickCalculate();
        clickCalculate();
        pending[1].resolve({ data: SUCCESS });
        await flush();
        expect(rows()).toHaveLength(1);
        const { response, getter } = withGetter(HANDLING_FAIL);
        pending[0].resolve(response);
        await flush();
        expect(getter).toHaveBeenCalledTimes(1);
        expect(rows()).toHaveLength(1);
        expect(region()).toBeNull();
        expect(announcements()).toHaveLength(0);
    });

    it('4c-control a CURRENT post-2xx handling failure does enter the failure state', async () => {
        clickCalculate();
        await succeedLast(HANDLING_FAIL);
        expect(region()).not.toBeNull();
        expect(announcements()).toHaveLength(1);
        expect(errorSpy.mock.calls.some(call => call[0] === 'Volume calculation: response handling failed')).toBe(true);
    });

    it('4d reset while in flight, then the request fails: no region, no toast', async () => {
        slider().value = '5';
        clickCalculate();
        expect(pending).toHaveLength(1);
        clickReset();
        expect(slider().value).toBe('0');
        pending[0].reject(REQ_ERR);
        await flush();
        expect(region()).toBeNull();
        expect(shows()).toHaveLength(0);
        expect(requestFailedLogs()).toBe(0);
    });

    it('4d-handling reset while in flight, then a post-2xx handling failure: no region, no toast', async () => {
        clickCalculate();
        clickReset();
        const { response, getter } = withGetter(HANDLING_FAIL);
        pending[0].resolve(response);
        await flush();
        expect(getter).toHaveBeenCalledTimes(1);
        expect(region()).toBeNull();
        expect(shows()).toHaveLength(0);
    });
});

describe('T-4 probes and dismiss guard', () => {
    const failThenSucceed = async arrange => {
        clickCalculate();
        await failLast();
        expect(announcements()).toHaveLength(1);
        arrange?.();
        const beforeHides = hides();
        clickCalculate();
        await succeedLast();
        expect(rows()).toHaveLength(1);
        expect(region()).toBeNull();
        return hides() - beforeHides;
    };

    it('5a both stand: success hides the toast', async () => {
        expect(await failThenSucceed()).toBe(1);
        expect(FakeToast.getInstance).toHaveBeenCalledWith($('#liveToast'));
    });

    it('5b action probe is scoped to #liveToast: button OUTSIDE #toast-body still counts', async () => {
        const hideDelta = await failThenSucceed(() => {
            $('#liveToast').appendChild(liveToastBtn());
            expect($(`#toast-body ${RETRY_SEL}`)).toBeNull();
            expect(liveToastBtn()).not.toBeNull();
            expect(messageText()).toBe(MSG);
        });
        expect(hideDelta).toBe(1);
    });

    it('5c only the button stands (stranger message): NOT hidden', async () => {
        const hideDelta = await failThenSucceed(() => {
            setStrangerMessage('Plan #4 saved.');
            expect(liveToastBtn()).not.toBeNull();
        });
        expect(hideDelta).toBe(0);
    });

    it('5d only the message stands (button gone): NOT hidden', async () => {
        const hideDelta = await failThenSucceed(() => {
            expireAction();
            expect(liveToastBtn()).toBeNull();
            expect(messageText()).toBe(MSG);
        });
        expect(hideDelta).toBe(0);
    });

    it('5e a same-label button OUTSIDE #liveToast does not count as ours', async () => {
        const hideDelta = await failThenSucceed(() => {
            expireAction();
            const decoy = document.createElement('button');
            decoy.setAttribute('aria-label', 'Retry volume calculation');
            document.body.appendChild(decoy);
            expect(messageText()).toBe(MSG);
        });
        expect(hideDelta).toBe(0);
    });
});
