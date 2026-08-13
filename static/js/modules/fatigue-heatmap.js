// Fatigue body heatmap — colors the MuscleMap figure by each muscle's band.
//
// Pure visualization of what the server already computed. The bands come from
// `utils/_fatigue/per_muscle.py::classify_muscle_fatigue` via the `muscle_rows`
// JSON the template embeds; nothing here re-derives a band from a score.
//
// The three consts below are authored as a strict JSON subset (double quotes,
// no trailing comma, no inline comment) so `tests/test_fatigue_heatmap_mapping.py`
// can parse them with `json.loads` and check them against the Python landmarks,
// the SVG region keys, and the SCSS palette.

import { loadBodymapSvg } from './bodymap-svg.js';

// MuscleMap region key -> fatigue muscle bucket. Single-valued on purpose: each
// drawn region resolves to exactly one muscle, so rendering is total.
//
// Both deltoid regions map to Middle-Shoulder by owner decision. The unranked
// Front-Shoulder / Rear-Shoulder / Middle-Traps labels therefore drive no
// region; they keep their bars, and the panel note says so.
export const REGION_TO_MUSCLE = {
    "chest": "Chest",
    "lats": "Latissimus-Dorsi",
    "front-deltoid": "Middle-Shoulder",
    "rear-deltoid": "Middle-Shoulder",
    "biceps": "Biceps",
    "triceps": "Triceps",
    "quadriceps": "Quadriceps",
    "hamstring": "Hamstrings",
    "gluteal": "Glutes",
    "calves": "Calves",
    "abs": "Abdominals",
    "obliques": "Abdominals",
    "trapezius": "Traps",
    "forearms": "Forearms"
};

// Regions the figure draws that no fatigue muscle covers. They stay visible in
// the neutral state rather than being hidden.
export const UNMAPPED_REGIONS = ["neck", "adductors", "lower-back"];

// Band -> CSS class. `very_heavy` becomes `fatigue-very-heavy`; getting that
// conversion wrong is silent (the region just renders neutral), so the mapping
// is a table rather than a string transform.
export const BAND_CLASS = {
    "light": "fatigue-light",
    "moderate": "fatigue-moderate",
    "heavy": "fatigue-heavy",
    "very_heavy": "fatigue-very-heavy"
};

export const NEUTRAL_CLASS = 'fatigue-unranked';

// Mirrors `_BAND_LABELS` in utils/fatigue_context.py — sentence-case forms.
const BAND_LABELS = {
    light: 'light',
    moderate: 'moderate',
    heavy: 'heavy',
    very_heavy: 'very heavy',
};

const UNMAPPED_LABELS = {
    'neck': 'Neck',
    'adductors': 'Hip adductors',
    'lower-back': 'Lower back',
};

const SIDES = ['front', 'back'];
const CHANNELS = ['planned', 'logged'];
const CHANNEL_LABELS = { planned: 'Planned', logged: 'Logged' };

/**
 * Resolve which band should paint a region for one channel.
 *
 * Returns `band: null` for three distinct situations, all of which paint the
 * same neutral gray but read differently in the region title:
 *   - the region maps to no fatigue muscle (no reference range exists);
 *   - the muscle has no row at all;
 *   - the requested channel has no data for that muscle.
 */
export function resolveRegionBand(regionKey, rowsByMuscle, channel) {
    const muscle = REGION_TO_MUSCLE[regionKey] || null;
    if (!muscle) {
        return { muscle: null, band: null, percentOfMrv: null, hasData: false };
    }
    const row = rowsByMuscle[muscle];
    const side = row ? row[channel] : null;
    if (!side || !side.band) {
        return { muscle, band: null, percentOfMrv: null, hasData: false };
    }
    return {
        muscle,
        band: side.band,
        percentOfMrv: side.percent_of_mrv,
        hasData: true,
    };
}

export function bandClass(band) {
    return BAND_CLASS[band] || NEUTRAL_CLASS;
}

/**
 * Hover text for one region. Carries the percentage alongside the band because
 * colour alone is not comparable across regions: four muscles have MEV 0 and so
 * can never render `light`, and Abdominals can never render `heavy`.
 */
export function regionTitle(regionKey, result) {
    if (!result.muscle) {
        const label = UNMAPPED_LABELS[regionKey] || regionKey;
        return `${label} — no typical range yet`;
    }
    if (!result.hasData) {
        return `${result.muscle} — no volume in this window`;
    }
    const band = BAND_LABELS[result.band] || result.band;
    if (result.percentOfMrv === null || result.percentOfMrv === undefined) {
        return `${result.muscle} — ${band}`;
    }
    const pct = Math.round(result.percentOfMrv);
    return `${result.muscle} — ${band} · ${pct}% of typical recoverable range`;
}

export function indexRowsByMuscle(rows) {
    const out = {};
    for (const row of rows) {
        if (row && row.muscle) out[row.muscle] = row;
    }
    return out;
}

export function channelsWithData(rows) {
    return CHANNELS.filter((channel) => rows.some((row) => row && row[channel]));
}

// ---------------------------------------------------------------------------
// DOM layer. Everything above is pure so the vitest suite can run in `node`.
// ---------------------------------------------------------------------------

function readEmbeddedRows() {
    const node = document.getElementById('fatigue-heatmap-data');
    if (!node) return null;
    try {
        return JSON.parse(node.textContent);
    } catch {
        return null;
    }
}

function paint(panel, rowsByMuscle, channel) {
    panel.querySelectorAll('.muscle-region[data-canonical-muscles]').forEach((region) => {
        const key = region.dataset.canonicalMuscles.trim();
        const result = resolveRegionBand(key, rowsByMuscle, channel);

        region.classList.remove(NEUTRAL_CLASS, ...Object.values(BAND_CLASS));
        region.classList.add(bandClass(result.band));
        region.dataset.heatmapMuscle = result.muscle || '';
        region.dataset.heatmapBand = result.band || '';

        // A native <title> is the hover tooltip. It is NOT an accessibility
        // channel here: the SVG root carries role="img", which makes every
        // descendant presentational. The textual equivalent is the legend plus
        // the per-muscle bar list below the panel.
        let title = region.querySelector(':scope > title');
        if (!title) {
            title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
            region.insertBefore(title, region.firstChild);
        }
        title.textContent = regionTitle(key, result);
    });
}

function labelFigures(panel, channel) {
    panel.querySelectorAll('[data-heatmap-figure]').forEach((figure) => {
        const side = figure.dataset.heatmapFigure;
        const svg = figure.querySelector('svg');
        if (!svg) return;
        svg.setAttribute(
            'aria-label',
            `${CHANNEL_LABELS[channel]} fatigue by muscle, ${side} view`,
        );
    });
}

async function mountFigures(panel) {
    // A failed asset must not reject: an unhandled rejection is a console error,
    // and the console-error fixture fails every other /fatigue test when one
    // appears. The panel keeps its server-rendered fallback copy instead.
    const results = await Promise.all(
        SIDES.map(async (side) => {
            const figure = panel.querySelector(`[data-heatmap-figure="${side}"]`);
            if (!figure) return false;
            try {
                const svgText = await loadBodymapSvg(side);
                // Trusted first-party generated markup. Muscle labels never
                // travel this path - they go through textContent.
                figure.innerHTML = svgText;
                return Boolean(figure.querySelector('svg'));
            } catch {
                return false;
            }
        }),
    );
    return results.every(Boolean);
}

function showNoData(panel) {
    const figures = panel.querySelector('[data-heatmap-figures]');
    if (figures) figures.hidden = true;
    const message = panel.querySelector('[data-heatmap-nodata]');
    if (message) message.hidden = false;
}

export async function initFatigueHeatmap() {
    const page = document.querySelector('[data-testid="fatigue-page"]');
    if (!page) return;
    const panel = document.querySelector('[data-heatmap-panel]');
    const rows = readEmbeddedRows();
    if (!panel || !rows) return;

    // Every exit below is terminal, so the marker has to flip on all of them.
    // Leaving it at `pending` on any path strands the visual harness, which
    // waits for `ready|empty` and reports the timeout as a render failure.
    // Two frames because a single rAF callback runs before that frame's paint.
    const markReady = () => requestAnimationFrame(() => requestAnimationFrame(() => {
        page.dataset.heatmapState = 'ready';
    }));

    const rowsByMuscle = indexRowsByMuscle(rows);
    const available = channelsWithData(rows);
    if (available.length === 0) {
        // The panel renders on raw row counts, but a row whose sets resolve to
        // 0 - an unscored log row, most often - contributes no bar. Say that,
        // rather than leaving the figure fallbacks blaming the asset loader.
        showNoData(panel);
        markReady();
        return;
    }

    const mounted = await mountFigures(panel);
    if (!mounted) {
        markReady();
        return;
    }

    // The control only makes sense when there is something to switch between.
    // It ships hidden so it cannot flash before that is known, so this must
    // assign both ways - setting only `true` leaves it permanently hidden, and
    // reboot's `[hidden]{display:none !important}` means the container beats any
    // un-hiding of its children.
    const control = panel.querySelector('[data-heatmap-control]');
    if (control) control.hidden = available.length < 2;
    panel.querySelectorAll('[data-heatmap-channel]').forEach((button) => {
        button.hidden = !available.includes(button.dataset.heatmapChannel);
    });

    let channel = available[0];

    const render = () => {
        paint(panel, rowsByMuscle, channel);
        labelFigures(panel, channel);
        panel.dataset.heatmapChannel = channel;
        const caption = panel.querySelector('[data-heatmap-caption]');
        if (caption) caption.textContent = `Showing: ${CHANNEL_LABELS[channel]}`;
        panel.querySelectorAll('[data-heatmap-channel]').forEach((button) => {
            button.setAttribute(
                'aria-pressed',
                String(button.dataset.heatmapChannel === channel),
            );
        });
    };

    panel.querySelectorAll('[data-heatmap-channel]').forEach((button) => {
        button.addEventListener('click', () => {
            const next = button.dataset.heatmapChannel;
            if (!available.includes(next)) return;
            channel = next;
            render();
        });
    });

    render();
    markReady();
}

if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initFatigueHeatmap);
    } else {
        initFatigueHeatmap();
    }
}
