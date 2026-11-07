# Purpose: make each tool folder importable from the tests.
# Book: Coding Agents in the Enterprise, Chapters 2-12 (tests)
# Licence: MIT (see LICENSE)
"""Add the tool folders to sys.path so tests can `import cost_model`, `did`, etc."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for folder in ("cost", "scorecard", "pilot", "metrics", "policies/hooks"):
    sys.path.insert(0, str(ROOT / folder))
