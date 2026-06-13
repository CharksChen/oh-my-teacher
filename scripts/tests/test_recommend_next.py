"""Tests for scripts/recommend_next.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent


class RecommendNextTests(unittest.TestCase):
    def _run(self, args: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "recommend_next.py")] + args,
            capture_output=True,
            text=True,
            cwd=cwd or str(SCRIPT_DIR),
        )

    def test_ranks_weak_p0_due_topic_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".oh-my-teacher"
            root.mkdir()
            (root / "state.json").write_text(json.dumps({
                "snapshot": {"days_left": "2"},
                "adaptive": {
                    "topics": {
                        "limits": {
                            "priority": "P0",
                            "mastery_band": "weak",
                            "exam_scope_weight": 30,
                            "past_paper_frequency": 2,
                            "teacher_emphasis_strength": "high",
                        },
                        "series": {
                            "priority": "P2",
                            "mastery_band": "strong",
                        },
                    }
                },
            }, ensure_ascii=False), encoding="utf-8")

            srs_path = root / "srs-state.md"
            srs_path.write_text(
                "| Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |\n"
                "|-------|-------------|-------|--------|-------------|------------|------|--------|\n"
                "| limits | 2026-06-10 | 2 | 0 | 2026-06-11 | hard (困难) | 2.10 | 2 |\n",
                encoding="utf-8",
            )

            result = self._run(["--workspace", tmp, "--today", "2026-06-13", "--format", "json"])
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload[0]["topic"], "limits")
            self.assertIn("/fix limits", payload[0]["action"])
            self.assertTrue(payload[0]["srs_due"])

    def test_markdown_output_has_next_action_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / ".oh-my-teacher"
            root.mkdir()
            (root / "state.json").write_text(json.dumps({
                "adaptive": {"topics": {"graphs": {"priority": "P1", "mastery_band": "unstable"}}}
            }), encoding="utf-8")
            result = self._run(["--workspace", tmp, "--today", "2026-06-13"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("## 下一步推荐", result.stdout)
            self.assertIn("| Rank | Topic | Score | Why now | Action |", result.stdout)
            self.assertIn("graphs", result.stdout)


if __name__ == "__main__":
    unittest.main()
