"""Static contracts for the Node.js version used by GitHub Actions."""

import json
import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "workflow",
    [".github/workflows/ci.yml", ".github/workflows/deep-gate.yml"],
)
def test_github_workflows_use_node_24_consistently(workflow):
    source = (REPO_ROOT / workflow).read_text(encoding="utf-8")

    setup_count = source.count("uses: actions/setup-node@")
    assert setup_count > 0
    assert source.count("node-version: '24'") == setup_count
    assert "node-version: '20'" not in source


def test_package_json_declares_the_node_floor_that_ci_actually_runs():
    """`engines.node` must track the workflow pin, not lag behind it.

    The declared floor sat at >=18 while CI had moved to 24 and `undici`
    (via jsdom) had begun requiring >=22.19.0, so `npm ci` was advertised as
    working on runtimes it would in fact reject. Deriving the expectation from
    ci.yml means bumping one without the other fails here rather than in a
    contributor's install.
    """
    pinned = re.findall(
        r"node-version: '(\d+)'",
        (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8"),
    )
    assert pinned, "ci.yml pins no Node version"
    assert len(set(pinned)) == 1, f"ci.yml pins mixed Node versions: {sorted(set(pinned))}"

    package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    assert package["engines"]["node"] == f">={pinned[0]}.0.0"
