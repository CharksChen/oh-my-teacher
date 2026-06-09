#!/usr/bin/env python3
"""Run all Oh My Teacher skill validation checks in one command.

This is a convenience entry point that runs:
  1. validate_skill.py  — structural checks, command registration, stale references
  2. All unit tests under scripts/tests/

Usage:
    python scripts/package_check.py
    python scripts/package_check.py --root /path/to/skill
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run all Oh My Teacher skill checks.")
    parser.add_argument("--root", default=str(SCRIPT_DIR.parent), help="Skill root directory.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    failures = 0
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    # Step 1: validate_skill.py
    validate_script = SCRIPT_DIR / "validate_skill.py"
    print("=== Running validate_skill.py ===")
    result = subprocess.run(
        [sys.executable, str(validate_script), "--root", str(root)],
        cwd=str(root),
        env=env,
    )
    if result.returncode != 0:
        failures += 1
        print("validate_skill.py FAILED.", file=sys.stderr)
    else:
        print("validate_skill.py PASSED.")

    # Step 2: unit tests
    print("\n=== Running unit tests ===")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(SCRIPT_DIR / "tests"), "-v"],
        cwd=str(SCRIPT_DIR),
        env=env,
    )
    if result.returncode != 0:
        failures += 1
        print("Unit tests FAILED.", file=sys.stderr)
    else:
        print("Unit tests PASSED.")

    # Summary
    print(f"\n=== Summary: {2 - failures}/2 checks passed ===")
    if failures:
        print("Some checks failed. See output above for details.", file=sys.stderr)
        return 1
    print("All checks passed. Skill package is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
