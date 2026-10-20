"""Run the release usability harness against an actual Windows bootloader.

Verification-only helper for an owner-approved disposable CI branch. Never imports
the candidate application's source. Source and build remain at the pinned SHA.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--sha', required=True)
    parser.add_argument('--harness', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    candidate, harness, output = (p.resolve() for p in (args.candidate, args.harness, args.output))
    assert os.name == 'nt', 'Real Windows bootloader validation requires Windows'
    assert os.environ.get('GITHUB_ACTIONS') == 'true', 'This verification helper is restricted to a disposable hosted CI runner'
    actual_sha = subprocess.check_output(['git', '-C', str(candidate), 'rev-parse', 'HEAD'], text=True).strip()
    assert actual_sha == args.sha, (actual_sha, args.sha)
    assert not subprocess.check_output(['git', '-C', str(candidate), 'status', '--porcelain'], text=True).strip(), 'Candidate tracked/untracked tree changed'
    with socket.socket() as check:
        check.bind(('127.0.0.1', 5168))
    output.mkdir(parents=True, exist_ok=False)
    report = {'candidate_sha': actual_sha, 'execution_mode': 'real_bootloader', 'port': 5168}

    def protected_snapshot():
        roots = [candidate / 'data/database.db', candidate / 'data/auto_backup', candidate / 'logs', Path(os.environ['LOCALAPPDATA']) / 'HypertrophyToolbox']
        snapshot = {}
        for root in roots:
            paths = [root] + (list(root.rglob('*')) if root.is_dir() else [])
            for path in paths:
                if path.exists():
                    stat = path.stat()
                    snapshot[str(path)] = {'is_dir': path.is_dir(), 'size': stat.st_size, 'mtime_ns': stat.st_mtime_ns}
                else:
                    snapshot[str(path)] = {'absent': True}
        return snapshot

    protected_before = protected_snapshot()
    report['protected_before'] = protected_before

    def flush():
        (output / 'real-frozen-launch.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

    def get(path):
        with urllib.request.urlopen('http://127.0.0.1:5168' + path, timeout=5) as response:
            return response.status, response.read()

    with tempfile.TemporaryDirectory(prefix='r3-real-frozen-') as scratch_name:
        scratch = Path(scratch_name)
        distribution = scratch / 'distribution'
        shutil.copytree(candidate / 'dist/Hypertrophy-Toolbox', distribution)
        executable = distribution / 'Hypertrophy-Toolbox.exe'
        runtime = scratch / 'runtime'
        report.update(executable_sha256=hashlib.sha256(executable.read_bytes()).hexdigest(), executable=str(executable), runtime=str(runtime))
        env = {**os.environ, 'HT_RUNTIME_DIR': str(runtime), 'HT_PORT': '5168', 'HT_NO_BROWSER': '1', 'FLASK_USE_RELOADER': '0', 'PYTHONDONTWRITEBYTECODE': '1'}
        env.pop('DB_FILE', None)
        process = None
        with (output / 'real-frozen-server.log').open('wb') as server_log:
            def launch():
                child = subprocess.Popen([str(executable)], cwd=distribution, env=env, stdout=server_log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
                for _ in range(60):
                    assert child.poll() is None, f'Bootloader exited: {child.returncode}'
                    try:
                        if get('/')[0] == 200:
                            return child
                    except OSError:
                        pass
                    time.sleep(1)
                child.terminate()
                child.wait(timeout=15)
                raise AssertionError('Frozen application did not start')

            def stop(child):
                if child and child.poll() is None:
                    child.terminate()
                    child.wait(timeout=15)

            try:
                process = launch()
                report['initial_pid'] = process.pid
                assert (runtime / 'data/database.db').is_file(), 'Isolated runtime database missing'
                assert (runtime / 'logs/app.log').is_file(), 'Isolated runtime log missing'
                flush()
                result = subprocess.run([sys.executable, str(harness), '--candidate-sha', actual_sha, '--confirm-isolated-runtime', '--execution-mode', 'real_bootloader'], check=False)
                report['functional_exit_code'] = result.returncode
                flush()
                assert result.returncode == 0, 'Frozen functional checklist failed; inspect harness evidence'
                stop(process)
                process = launch()
                status, body = get('/get_workout_plan')
                plan = json.loads(body)
                assert status == 200 and plan['ok'] is True and plan['data'] == [], plan
                report.update(restart_pid=process.pid, post_erase_restart='passed', status='functional_passed_awaiting_teardown')
                flush()
            except BaseException as exc:
                report.update(status='failed', error=str(exc))
                flush()
                raise
            finally:
                stop(process)
    protected_after = protected_snapshot()
    report['protected_after'] = protected_after
    report['scratch_removed'] = not scratch.exists()
    report['protected_runtime_unchanged'] = protected_before == protected_after
    if scratch.exists() or protected_before != protected_after:
        report['status'] = 'failed'
        flush()
        raise AssertionError('Teardown/preservation check failed')
    report['status'] = 'passed'
    flush()
    print(json.dumps(report))


if __name__ == '__main__':
    main()
