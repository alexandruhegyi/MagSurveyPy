#!/usr/bin/env python3
"""Compatibility launcher for running MagSurveyPy from a source checkout."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from magsurveypy.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
