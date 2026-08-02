"""Static contracts for the Node.js version used by GitHub Actions."""

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
