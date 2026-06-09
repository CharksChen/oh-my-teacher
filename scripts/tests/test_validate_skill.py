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

from validate_skill import commands_from_index, course_template_keys, frontmatter  # noqa: E402


class ValidateSkillTests(unittest.TestCase):
    def test_skill_frontmatter_has_required_keys(self):
        text = (ROOT_DIR / "SKILL.md").read_text(encoding="utf-8")
        fm_keys = set(frontmatter(text))
        self.assertTrue(fm_keys >= {"name", "description"}, f"Missing required keys: {fm_keys}")
        allowed = {"name", "description"}
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
            "/socratic",
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

    def test_environment_reference_exists(self):
        text = (ROOT_DIR / "references" / "environment-adaptation.md").read_text(encoding="utf-8")
        for phrase in ["agent-shell", "rag-notebook", "notes-app", "plain-chat", "Codex", "NotebookLM", "Obsidian"]:
            self.assertIn(phrase, text)

    def test_mode_protocol_references_exist(self):
        socratic = (ROOT_DIR / "references" / "socratic-mode.md").read_text(encoding="utf-8")
        feynman = (ROOT_DIR / "references" / "feynman-mode.md").read_text(encoding="utf-8")
        self.assertIn("Hint ladder", socratic)
        self.assertIn("Teacher close", socratic)
        self.assertIn("Feynman Check", feynman)
        self.assertIn("Repair Card", feynman)

    def test_examples_cover_signature_modes(self):
        text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT_DIR / "examples").glob("*.md"))
        self.assertIn("/socratic", text)
        self.assertIn("/feynman", text)

    def test_agent_configs_do_not_request_hidden_reasoning(self):
        text = "\n".join(path.read_text(encoding="utf-8").lower() for path in (ROOT_DIR / "agents").glob("*.*"))
        self.assertNotIn("write your reasoning chain", text)
        self.assertNotIn("chain-of-thought", text)
        self.assertNotIn("<thought>", text)
        self.assertNotIn("推理链", text)
        self.assertNotIn("思维链", text)

    def test_common_course_templates_exist(self):
        templates = course_template_keys(ROOT_DIR / "scripts" / "course_templates.py")
        for template in [
            "advanced-math",
            "physics",
            "programming-c-cpp",
            "digital-logic",
            "marxism-basic-principles",
        ]:
            self.assertIn(template, templates)

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
