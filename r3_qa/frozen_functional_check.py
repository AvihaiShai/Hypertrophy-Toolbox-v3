"""Exercise RELEASE_CHECKLIST 3-10 against the already-running packaged payload.

No application modules are imported and no source server, DB, or build is started.
The caller must verify the frozen process uses a disposable isolated runtime before
passing --confirm-isolated-runtime. This check creates fixture data and ERASES it.
Evidence is flushed after every step, including failures; no HTML or app state is
injected. Browser evaluations only read DOM values/readiness. API calls are recorded
and used for persistence assertions, existing compatibility modes, and backup/erase.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright, expect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:5168')
    parser.add_argument('--confirm-isolated-runtime', action='store_true', required=True)
    parser.add_argument('--candidate-sha', required=True)
    parser.add_argument('--headed', action='store_true')
    parser.add_argument('--execution-mode', choices=('compiled_payload', 'real_bootloader'), default='compiled_payload')
    args = parser.parse_args()
    if args.base_url.rstrip('/') != 'http://127.0.0.1:5168':
        parser.error('This evidence script is restricted to the isolated frozen app on 127.0.0.1:5168.')

    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = Path(__file__).resolve().parent / ('functional-' + stamp)
    out.mkdir(parents=True, exist_ok=False)
    report = {
        'candidate_sha': args.candidate_sha, 'base_url': args.base_url,
        'started_utc': stamp, 'runtime_isolation_confirmed_by_caller': True,
        'test_target': 'already-running packaged application', 'execution_mode': args.execution_mode,
        'steps': [], 'api_calls': [], 'browser_errors': [], 'console_errors': [],
        'limitations': [
            'Scripted browser/API functional evidence; does not replace human exploratory QA.',
            'Runtime path/process identity and absence of writes to the real runtime must be verified by the launcher.',
            'compiled_payload mode is supplemental usability evidence and does not establish that the local Windows executable bootloader starts.',
            'Current summaries intentionally omit a CountingMode UI. Both columns and the existing counting_mode HTTP compatibility parameter are checked separately.',
        ],
    }
    state = {}

    def flush():
        (out / 'results.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)
        context = browser.new_context(base_url=args.base_url, viewport={'width': 1600, 'height': 1050})
        context.tracing.start(screenshots=True, snapshots=True, sources=False)
        page = context.new_page()
        page.set_default_timeout(20000)
        page.on('pageerror', lambda err: report['browser_errors'].append(str(err)))
        page.on('console', lambda msg: report['console_errors'].append(msg.text) if msg.type == 'error' else None)

        def api(method, path, data=None, expected_status=200, headers=None):
            kwargs = {'headers': headers or {}}
            if data is not None:
                kwargs['data'] = data
            response = context.request.fetch(path, method=method, **kwargs)
            try:
                payload = response.json()
            except Exception:
                payload = response.text()[:2000]
            report['api_calls'].append({'method': method, 'path': path, 'status': response.status, 'body': payload})
            flush()
            assert response.status == expected_status, (method, path, response.status, payload)
            if expected_status == 200 and isinstance(payload, dict):
                assert payload.get('ok') is True, payload
                return payload.get('data', payload)
            return payload

        def goto(path):
            response = page.goto(path, wait_until='networkidle')
            assert response and response.status == 200, (path, response.status if response else None)
            expect(page.locator('h1')).to_be_visible()

        def screenshot(name):
            page.screenshot(path=str(out / (name + '.png')), full_page=True)

        def select_value(select, value):
            """Use the visible enhanced control when native selects are hidden."""
            native_options = select.locator('option').evaluate_all(
                '(xs) => xs.map(x => ({value: x.value, label: x.textContent.trim()}))')
            matches = [option for option in native_options if option['value'] == value]
            assert len(matches) == 1, ('Native option value must be unique', value, matches)
            label = matches[0]['label']
            if select.get_attribute('aria-hidden') == 'true':
                control_id = select.get_attribute('id')
                page.locator('#' + control_id + '_button').click()
                popover = page.locator('#' + control_id + '_button_listbox')
                option = popover.get_by_role('option', name=label, exact=True)
                expect(option).to_have_count(1)
                option.click()
            else:
                select.select_option(value)
            expect(select).to_have_value(value)

        def step(name, fn, needs=()):
            item = {'step': name, 'started_utc': datetime.now(timezone.utc).isoformat()}
            report['steps'].append(item)
            if any(not state.get(key) for key in needs):
                item.update(status='blocked', reason='Prerequisite failed: ' + ', '.join(needs))
                flush()
                return
            try:
                item['evidence'] = fn()
                item['status'] = 'passed'
                screenshot(name)
            except Exception as exc:
                item.update(status='failed', error=str(exc), traceback=traceback.format_exc())
                try:
                    screenshot(name + '-FAILED')
                    (out / (name + '-FAILED.html')).write_text(page.content(), encoding='utf-8')
                except Exception as capture_exc:
                    item['capture_error'] = str(capture_exc)
            finally:
                item['finished_utc'] = datetime.now(timezone.utc).isoformat()
                print(name + ': ' + item['status'], flush=True)
                flush()

        def routine():
            page.locator('#routine-env').select_option('GYM')
            expect(page.locator('#routine-program')).to_be_enabled()
            page.locator('#routine-program').select_option('Full Body')
            expect(page.locator('#routine-day')).to_be_enabled()
            with page.expect_response(lambda r: '/get_routine_exercises/' in r.url and r.status == 200):
                page.locator('#routine-day').select_option('Workout A')
            page.wait_for_function("document.querySelector('#exercise').options.length > 1")
            return page.locator('#routine').input_value()

        def controls():
            return {key: float(page.locator('#' + key).input_value()) for key in
                    ('weight', 'sets', 'rir', 'rpe', 'min_rep', 'max_rep_range')}

        def baseline():
            goto('/workout_plan')
            before = {key: api('GET', path) for key, path in (
                ('plan', '/get_workout_plan'), ('logs', '/get_workout_logs'), ('backups', '/api/backups'))}
            assert all(not value for value in before.values()), 'Refusing to overwrite a non-empty runtime: ' + str(before)
            state['isolated_empty'] = True
            return before

        def plan():
            goto('/workout_plan')
            state['routine'] = routine()
            initial_options = page.locator('#exercise option').count()
            filters = page.locator('.filter-dropdown')
            chosen_filter = None
            for index in range(filters.count()):
                candidate = filters.nth(index)
                if re.search('primary|muscle', candidate.get_attribute('id') or '', re.I):
                    values = candidate.locator('option').evaluate_all('(xs) => xs.map(x => x.value)')
                    chest = next((v for v in values if v.lower() == 'chest'), None)
                    if chest:
                        with page.expect_response(lambda r: r.url.endswith('/filter_exercises') and r.status == 200) as filtered_response:
                            select_value(candidate, chest)
                        filtered_exercises = filtered_response.value.json()['data']
                        expect(page.locator('#exercise option')).to_have_count(len(filtered_exercises) + 1)
                        chosen_filter = {'id': candidate.get_attribute('id'), 'value': chest}
                        break
            assert chosen_filter, 'Chest filter was not available; no synthetic catalog fallback is allowed.'
            options = page.locator('#exercise option').evaluate_all('(xs) => xs.map(x => x.value).filter(Boolean)')
            assert 1 < len(options) < initial_options, (len(options), initial_options)
            bench = sorted([v for v in options if 'bench press' in v.lower()], key=lambda v: ('barbell' not in v.lower(), len(v)))
            assert len(bench) >= 2, ('Need two genuine chest pressing exercises', options)
            state['exercises'] = bench[:2]
            fixtures = [dict(weight=50, sets=3, min_rep=6, max_rep_range=8, rir=3, rpe=7),
                        dict(weight=25, sets=4, min_rep=10, max_rep_range=12, rir=4, rpe=6)]
            for exercise, fixture in zip(state['exercises'], fixtures):
                select_value(page.locator('#exercise'), exercise)
                page.wait_for_function("!document.documentElement.hasAttribute('data-workout-controls-busy')")
                for key, value in fixture.items():
                    page.locator('#' + key).fill(str(value))
                with page.expect_response(lambda r: r.url.endswith('/add_exercise') and r.request.method == 'POST') as added:
                    page.locator('#add_exercise_btn').click()
                assert added.value.status == 200, added.value.text()
                expect(page.locator('#workout_plan_table_body tr').filter(has_text=exercise)).to_have_count(1)
            saved = api('GET', '/get_workout_plan')
            assert [r['exercise'] for r in saved] == state['exercises'], saved
            for row, fixture in zip(saved, fixtures):
                for key, value in fixture.items():
                    mapped = {'min_rep': 'min_rep_range'}.get(key, key)
                    assert float(row[mapped]) == value, (row, fixture)
            assert any(r.get('secondary_muscle_group') for r in saved), 'Fixture must credit secondary muscles for the contribution check.'
            page.reload(wait_until='networkidle')
            rows = page.locator('#workout_plan_table_body tr[data-id]')
            if rows.count() == 0:
                rows = page.locator('#workout_plan_table_body tr[data-routine]')
            expect(rows).to_have_count(2)
            for i, exercise in enumerate(state['exercises']):
                expect(rows.nth(i)).to_contain_text(exercise)
            assert api('GET', '/get_workout_plan') == saved
            state['saved_plan'] = saved
            state['plan'] = True
            return {'filter': chosen_filter, 'before_filter_options': initial_options, 'filtered_options': len(options), 'saved_plan': saved,
                    'order_verified': 'Browser row order and persisted exercise_order survived reload.'}

        def log():
            goto('/workout_log')
            with page.expect_response(lambda r: '/export_to_workout_log' in r.url and r.request.method == 'POST') as imported:
                page.locator('#import-from-plan-btn').click()
            assert imported.value.status == 200, imported.value.text()
            page.wait_for_timeout(1600)  # product deliberately reloads after its success-toast delay
            page.wait_for_load_state('networkidle')
            rows = page.locator('.workout-log-table tbody tr[data-log-id]')
            expect(rows).to_have_count(2)
            for exercise, planrow in zip(state['exercises'], state['saved_plan']):
                row = rows.filter(has_text=exercise)
                expect(row).to_have_count(1)
                scores = dict(scored_min_reps=planrow['max_rep_range'], scored_max_reps=planrow['max_rep_range'],
                              scored_rir=2, scored_rpe=8, scored_weight=planrow['weight'])
                for field, value in scores.items():
                    cell = row.locator('[data-field="' + field + '"]')
                    cell.locator('.editable-text').click()
                    fieldinput = cell.locator('input')
                    expect(fieldinput).to_be_visible()
                    fieldinput.fill(str(value))
                    with page.expect_response(lambda r: r.url.endswith('/update_workout_log') and r.request.method == 'POST') as updated:
                        fieldinput.press('Enter')
                    assert updated.value.status == 200, updated.value.text()
                    expect(fieldinput).to_be_hidden()
            saved = api('GET', '/get_workout_logs')
            assert len(saved) == 2
            for item in saved:
                planrow = next(r for r in state['saved_plan'] if r['exercise'] == item['exercise'])
                for field, value in dict(scored_min_reps=planrow['max_rep_range'], scored_max_reps=planrow['max_rep_range'],
                                         scored_rir=2, scored_rpe=8, scored_weight=planrow['weight']).items():
                    assert float(item[field]) == float(value), (field, item)
            page.reload(wait_until='networkidle')
            for item in saved:
                row = page.locator('.workout-log-table tbody tr[data-log-id="' + str(item['id']) + '"]')
                for field in ('scored_min_reps', 'scored_max_reps', 'scored_rir', 'scored_rpe', 'scored_weight'):
                    assert float(row.locator('[data-field="' + field + '"] .editable-text').inner_text()) == float(item[field])
            state['logs'] = True
            return {'saved_and_reloaded_logs': saved, 'fixture': 'Top of planned rep range, same weight, acceptable RIR/RPE.'}

        def summary(kind):
            path = '/' + kind + '_summary'
            goto(path)
            container = page.locator('#' + kind + '-summary-container')
            expect(container.locator('thead')).to_contain_text('Effective Sets')
            expect(container.locator('thead')).to_contain_text('Raw Sets')
            body = page.locator('#' + kind + '-summary-table')
            expect(body.locator('td[data-label="Effective Sets"]').first).to_be_visible()
            expect(body.locator('td[data-label="Raw Sets"]').first).to_be_visible()
            total = body.inner_text()
            screenshot('05-' + kind + '-total')
            with page.expect_response(lambda r: path + '?' in r.url and 'contribution_mode=direct' in r.url and r.status == 200) as direct_response:
                page.locator('#contribution-mode').select_option('direct')
            direct_payload = direct_response.value.json()
            page.wait_for_load_state('networkidle')
            direct = body.inner_text()
            assert total != direct, ('Contribution mode did not change displayed data', total, direct)
            assert page.locator('#counting-mode').count() == 0, 'Unexpected new counting UI; re-review before assuming its semantics.'
            headers = {'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
            effective = api('GET', path + '?contribution_mode=total&counting_mode=effective', headers=headers)
            raw = api('GET', path + '?contribution_mode=total&counting_mode=raw', headers=headers)
            key = kind + '_summary'
            effective_rows, raw_rows = effective[key], raw[key]
            assert effective_rows and raw_rows
            assert any(float(r['raw_sets']) != float(r['effective_sets']) for r in effective_rows), effective_rows
            assert [r['total_sets'] for r in effective_rows] != [r['total_sets'] for r in raw_rows], (effective_rows, raw_rows)
            return {'total_display': total, 'direct_display': direct, 'direct_response': direct_payload,
                    'counting_mode_ui': {'status': 'not_applicable', 'reason': 'Intentionally absent; both columns are simultaneous.'},
                    'counting_mode_api': {'effective': effective, 'raw': raw},
                    'scope': 'Planned sets, not a claim that the summaries aggregate performed workout-log values.'}

        def progression():
            goto('/progression')
            exercise = state['exercises'][0]
            with page.expect_response(lambda r: r.url.endswith('/get_exercise_suggestions') and r.request.method == 'POST') as response:
                page.locator('#exerciseSelect').select_option(exercise)
            assert response.value.status == 200
            payload = response.value.json()
            suggestions = payload['data']
            primary = [s for s in suggestions if s['type'] in ('double_progression_weight', 'double_progression_reps')]
            assert len(primary) == 1 and primary[0]['type'] == 'double_progression_weight', suggestions
            suggestion = primary[0]
            assert float(suggestion['suggested_weight']) > float(suggestion['current_value'])
            expect(page.locator('#suggestionsList [data-goal-type="double_progression_weight"]').first).to_be_visible()
            assert page.locator('#suggestionsList [data-goal-type="double_progression_reps"]').count() == 0
            expect(page.locator('#suggestionsList')).to_contain_text(suggestion['title'])
            return {'exercise': exercise, 'suggestions': suggestions, 'one_dimension': 'Weight increases; action retains the original planned rep interval.'}

        def distribute():
            goto('/volume_splitter')
            page.locator('#training-days').select_option('3')
            expect(page.locator('.volume-slider').first).to_be_visible()
            sliders = page.locator('.volume-slider')
            targets = {}
            for i in range(sliders.count()):
                slider = sliders.nth(i)
                target = (12, 15)[i] if i < 2 else 0
                slider.focus()
                slider.press('Home')
                for _ in range(target):
                    slider.press('ArrowRight')
                assert int(slider.input_value()) == target
                targets[slider.get_attribute('data-muscle')] = target
            with page.expect_response(lambda r: r.url.endswith('/api/calculate_volume') and r.status == 200) as calculated:
                page.locator('#calculate-volume').click()
            payload = calculated.value.json()
            expect(page.locator('.results-section')).to_be_visible()
            rows = page.locator('#results-body tr')
            result = {}
            for i in range(rows.count()):
                cells = rows.nth(i).locator('td').all_inner_texts()
                assert len(cells) >= 3, cells
                weekly, per_session = float(cells[1]), float(cells[2])
                assert math.isfinite(weekly) and weekly >= 0 and weekly.is_integer(), cells
                assert math.isfinite(per_session) and per_session >= 0 and per_session.is_integer(), cells
                assert weekly == targets[cells[0]] and per_session * 3 == weekly, (cells, targets)
                result[cells[0]] = {'weekly_sets': weekly, 'sets_per_session': per_session}
            assert set(result) == set(targets), (result, targets)
            assert sum(r['weekly_sets'] for r in result.values()) == sum(targets.values()) == 27
            return {'training_days': 3, 'per_muscle_inputs': targets, 'results': result, 'api_response': payload,
                    'interpretation': 'Inputs are weekly sets per muscle; aggregate 27 is preserved. Targets 12/15 are divisible by 3, so this case has integer session allocations.'}

        def profile():
            goto('/user_profile')
            lift = page.locator('.reference-lift-row[data-lift-key="preacher_curl"]')
            expect(lift).to_be_visible()
            lift.locator('[name="weight_kg"]').fill('35')
            with page.expect_response(lambda r: r.url.endswith('/api/user_profile/lifts') and r.request.method == 'POST') as saved_lift:
                lift.locator('[name="reps"]').fill('8')
                lift.locator('[name="reps"]').press('Tab')
            assert saved_lift.value.status == 200
            expect(page.locator('#profile-lifts-form [data-autosave-status]')).to_have_attribute('data-autosave-status', 'saved')
            radio = page.locator('input[name="isolated"][value="moderate"]')
            with page.expect_response(lambda r: r.url.endswith('/api/user_profile/preferences') and r.request.method == 'POST') as saved_pref:
                page.locator('label.segmented-option:has(input[name="isolated"][value="moderate"])').click()
            assert saved_pref.value.status == 200
            expect(radio).to_be_checked()
            expect(page.locator('#profile-preferences-form [data-autosave-status]')).to_have_attribute('data-autosave-status', 'saved')
            page.reload(wait_until='networkidle')
            assert float(page.locator('.reference-lift-row[data-lift-key="preacher_curl"] [name="weight_kg"]').input_value()) == 35
            assert float(page.locator('.reference-lift-row[data-lift-key="preacher_curl"] [name="reps"]').input_value()) == 8
            expect(page.locator('input[name="isolated"][value="moderate"]')).to_be_checked()
            goto('/workout_plan')
            routine()
            exercise = 'EZ Bar Preacher Curl'
            with page.expect_response(lambda r: '/api/user_profile/estimate?' in r.url and 'Preacher' in r.url) as estimated:
                select_value(page.locator('#exercise'), exercise)
            assert estimated.value.status == 200
            estimate = estimated.value.json()['data']
            page.wait_for_function("!document.documentElement.hasAttribute('data-workout-controls-busy')")
            expect(page.locator('#workout-estimate-provenance')).to_have_text('from your profile')
            values = controls()
            assert values['min_rep'] == 6 and values['max_rep_range'] == 8, values
            assert values['weight'] > 0
            for key, api_key in [('weight', 'weight'), ('sets', 'sets'), ('rir', 'rir'), ('rpe', 'rpe'), ('min_rep', 'min_rep'), ('max_rep_range', 'max_rep')]:
                assert values[key] == float(estimate[api_key]), (values, estimate)
            return {'saved_reference_lift': {'lift_key': 'preacher_curl', 'weight_kg': 35, 'reps': 8},
                    'preference': {'isolated': 'moderate'}, 'exercise': exercise, 'estimate': estimate, 'workout_controls': values,
                    'persistence': 'Reference lift and radio preference survive reload; plan controls match actual estimator response.'}

        def backup_restore():
            before = api('GET', '/get_workout_plan')
            backup = api('POST', '/api/backups', {'name': 'R3 frozen release check ' + stamp, 'note': args.candidate_sha})
            assert backup['item_count'] == 2
            goto('/workout_plan')
            row = page.locator('#workout_plan_table_body tr').filter(has_text=state['exercises'][0])
            cell = row.locator('[data-field="weight"]')
            original_weight = float(cell.inner_text())
            cell.click()
            cell.locator('input').fill(str(original_weight + 7.5))
            with page.expect_response(lambda r: r.url.endswith('/update_exercise') and r.request.method == 'POST') as changed_response:
                cell.locator('input').press('Enter')
            assert changed_response.value.status == 200
            changed = api('GET', '/get_workout_plan')
            changedrow = next(r for r in changed if r['exercise'] == state['exercises'][0])
            assert float(changedrow['weight']) == original_weight + 7.5
            page.reload(wait_until='networkidle')
            visible = page.locator('#workout_plan_table_body tr').filter(has_text=state['exercises'][0]).locator('[data-field="weight"]')
            assert float(visible.inner_text()) == original_weight + 7.5
            screenshot('09-visible-plan-change')
            restored = api('POST', '/api/backups/' + str(backup['id']) + '/restore', {})
            assert restored['restored_count'] == 2 and not restored['skipped'], restored
            after = api('GET', '/get_workout_plan')
            fields = ('routine', 'exercise', 'sets', 'min_rep_range', 'max_rep_range', 'rir', 'rpe', 'weight', 'exercise_order')
            assert [{k: r.get(k) for k in fields} for r in after] == [{k: r.get(k) for k in fields} for r in before], (before, after)
            page.reload(wait_until='networkidle')
            assert float(page.locator('#workout_plan_table_body tr').filter(has_text=state['exercises'][0]).locator('[data-field="weight"]').inner_text()) == original_weight
            return {'backup': backup, 'before': before, 'visible_changed_plan': changed, 'restore_result': restored, 'after': after}

        def erase():
            before = api('GET', '/get_workout_plan')
            guard_results = []
            for invalid in ({}, {'confirm': 'WRONG'}):
                guard_results.append(api('POST', '/erase-data', invalid, expected_status=400))
                assert api('GET', '/get_workout_plan') == before
            erased = api('POST', '/erase-data', {'confirm': 'ERASE_ALL_DATA'})
            empty = {key: api('GET', path) for key, path in (
                ('plan', '/get_workout_plan'), ('logs', '/get_workout_logs'), ('backups', '/api/backups'))}
            assert all(not value for value in empty.values()), empty
            boot_pages = []
            for path in ('/', '/workout_plan', '/workout_log', '/weekly_summary', '/session_summary', '/user_profile'):
                goto(path)
                boot_pages.append({'path': path, 'status': 200})
            goto('/workout_plan')
            assert page.locator('#workout_plan_table_body tr[data-routine]').count() == 0
            return {'rejected_confirmations': guard_results, 'erase_result': erased, 'empty_state': empty, 'pages_after_erase': boot_pages,
                    'boot_limit': 'Verified the existing frozen process serves the reset state; process restart belongs to launcher evidence.'}

        try:
            step('00-isolated-empty-runtime', baseline)
            step('03-plan', plan, ('isolated_empty',))
            step('04-log', log, ('plan',))
            step('05-weekly-summary', lambda: summary('weekly'), ('plan',))
            step('05-session-summary', lambda: summary('session'), ('plan',))
            step('06-progression', progression, ('logs',))
            step('07-distribute', distribute, ('isolated_empty',))
            step('08-profile', profile, ('isolated_empty',))
            step('09-backup-restore', backup_restore, ('plan',))
            state['ready_to_erase'] = all(s['status'] == 'passed' for s in report['steps'])
            step('10-erase', erase, ('ready_to_erase',))
        finally:
            try:
                context.tracing.stop(path=str(out / 'browser-trace.zip'))
            finally:
                browser.close()
            report['finished_utc'] = datetime.now(timezone.utc).isoformat()
            report['status'] = 'passed' if all(s['status'] == 'passed' for s in report['steps']) and not report['browser_errors'] else 'failed'
            flush()
            print(json.dumps({'status': report['status'], 'results': str(out / 'results.json'), 'browser_errors': report['browser_errors']}), flush=True)
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
