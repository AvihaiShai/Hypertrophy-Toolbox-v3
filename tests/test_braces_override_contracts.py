"""Keep the braces remediation effective without changing stylelint."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
REVIEWED_ALIAS = "npm:@zklogic/braces@3.0.7"
REVIEWED_INTEGRITY = (
    "sha512-+MYCuqCdcYsZCVkG7BkHXWrkXklBDq+cTxrSMrCI8o1BQg6iAEPhkNuWrfwSt0Ll"
    "adX0XSx3V1HYV7RzMsKEWQ=="
)
NODE_SETUP = r"""
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
// Resolve exactly what micromatch uses, including npm's nested alias layout.
const micromatchRequire = createRequire(
  require.resolve('micromatch/package.json'));
const braces = micromatchRequire('braces');
"""


def _run_node(script: str) -> None:
    if not (ROOT / "node_modules").is_dir():
        pytest.skip("npm dependencies are absent in the Python-only job")
    node = shutil.which("node")
    assert node is not None, "Installed npm dependencies require Node"
    result = subprocess.run(
        [node, "-e", NODE_SETUP + script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_locked_braces_graph_uses_reviewed_artifact_without_waiver() -> None:
    package = json.loads(
        (ROOT / "package.json").read_text(encoding="utf-8")
    )
    lock = json.loads(
        (ROOT / "package-lock.json").read_text(encoding="utf-8")
    )
    allowlist_path = ROOT / "docs" / "npm_audit_allowlist.json"
    allowlist = json.loads(allowlist_path.read_text(encoding="utf-8"))
    assert package["overrides"]["braces"] == REVIEWED_ALIAS
    assert package["devDependencies"]["stylelint"] == "16.11.0"
    assert lock["packages"]["node_modules/stylelint"]["version"] == "16.11.0"
    assert allowlist["allow"] == []

    resolutions = {
        path: entry
        for path, entry in lock["packages"].items()
        if path.endswith("/node_modules/braces")
        or path == "node_modules/braces"
        or entry.get("name") in {"braces", "@zklogic/braces"}
    }
    assert resolutions, "The replacement must remain reachable"
    for path, entry in resolutions.items():
        assert entry.get("name") == "@zklogic/braces", path
        assert entry["version"] == "3.0.7", path
        assert entry["integrity"] == REVIEWED_INTEGRITY, path
        assert entry["resolved"] == (
            "https://registry.npmjs.org/@zklogic/braces/-/braces-3.0.7.tgz"
        ), path


def test_installed_braces_preserves_ordinary_glob_behavior() -> None:
    _run_node(r"""
assert.equal(braces.compile('static/{css,js}/*'), 'static/(css|js)/*');
assert.deepEqual(braces.expand('file{01..03}.css'),
  ['file01.css', 'file02.css', 'file03.css']);
assert.deepEqual(braces.expand('a/{b,{c,d}}/e'), ['a/b/e', 'a/c/e', 'a/d/e']);
assert.deepEqual(braces.expand('a\\{b,c\\}'), ['a{b,c}']);
const micromatch = require('micromatch');
const files = ['static/css/a.css', 'static/js/a.js', 'other/a.css'];
assert.deepEqual(micromatch(files, ['static/{css,js}/**/*.{css,js}']),
  ['static/css/a.css', 'static/js/a.js']);
""")


@pytest.mark.parametrize("operation", ["compile", "expand"])
def test_installed_braces_bounds_malicious_nesting(operation: str) -> None:
    # Attack shapes stay under the original 10,000-character cap. Expansion
    # has only one actual set, avoiding an unrelated exponential-output test.
    _run_node("const operation = " + json.dumps(operation) + r""";
const pattern = operation === 'compile'
  ? '{'.repeat(4900) + 'a,b' + '}'.repeat(4900)
  : '({'.repeat(2400) + 'a,b' + '})'.repeat(2400);
assert.ok(pattern.length < 10000);
const result = braces[operation](pattern);
assert.ok(operation === 'compile'
  ? typeof result === 'string' : Array.isArray(result));
assert.ok(result.length > 0);
// Successful execution alone can depend on Node's stack size. Independently
// require a bounded AST so losing the guard fails even on a larger-stack host.
const pending = [[braces.parse(pattern), 0]];
while (pending.length) {
  const [node, depth] = pending.pop();
  assert.ok(depth <= 512, 'untrusted nesting escaped the parser depth bound');
  for (const child of node.nodes || []) pending.push([child, depth + 1]);
}
""")
