"""Tests for scripts/validate_skill.py."""
from __future__ import annotations

import subprocess
import sys
import os
import shutil
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from validate_skill import commands_from_index, frontmatter  # noqa: E402


class ValidateSkillTests(unittest.TestCase):
    def test_skill_frontmatter_has_required_keys(self):
        text = (ROOT_DIR / "SKILL.md").read_text(encoding="utf-8")
        fm_keys = set(frontmatter(text))
        self.assertTrue(fm_keys >= {"name", "description"}, f"Missing required keys: {fm_keys}")
        allowed = {"name", "description", "when"}
        extra = fm_keys - allowed
        self.assertFalse(extra, f"Unexpected frontmatter keys: {extra}")

    def test_index_includes_core_commands(self):
        text = (ROOT_DIR / "references" / "INDEX.md").read_text(encoding="utf-8")
        commands = commands_from_index(text)
        for command in [
            "/help",
            "/profile",
            "/materials",
            "/paper",
            "/lab",
            "/diagnose",
            "/plan",
            "/map",
            "/explain",
            "/quiz",
            "/mock",
            "/oral",
            "/grade",
            "/fix",
            "/flashcards",
            "/review-due",
            "/group-quiz",
            "/visual",
            "/video",
            "/code-demo",
            "/cram",
            "/resume",
            "/summary",
            "/mode",
        ]:
            self.assertIn(command, commands)

    def test_cli_passes_for_repo(self):
        script = SCRIPT_DIR / "validate_skill.py"
        for path in ROOT_DIR.rglob("__pycache__"):
            if path.is_dir():
                shutil.rmtree(path)
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run(
            [sys.executable, str(script), "--root", str(ROOT_DIR)],
            capture_output=True,
            text=True,
            cwd=str(ROOT_DIR),
            env=env,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Skill validation passed.", result.stdout)


if __name__ == "__main__":
    unittest.main()
