"""
pytest configuration for the XHAIL test suite.

Adds the repo root to sys.path so that `import xhail` resolves to the
xhail/ package directory regardless of where pytest is invoked from.
"""
import sys
from pathlib import Path

import pytest

# Repo root is one level above this file (tests/ → repo root)
REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(autouse=True)
def ensure_output_dir():
    """Create xhail/output/ if it doesn't exist.

    The abduction and induction phases write intermediate ASP programs
    to this directory.  It is gitignored after Phase 1 cleanup; for now
    we just make sure it exists so tests don't fail with FileNotFoundError.
    """
    output_dir = REPO_ROOT / 'xhail' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    yield
