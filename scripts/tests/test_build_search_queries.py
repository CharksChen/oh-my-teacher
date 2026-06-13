"""Tests for scripts/build_search_queries.py."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from build_search_queries import build_queries  # noqa: E402


class BuildSearchQueriesTests(unittest.TestCase):
    def test_chinese_math_generates_syllabus_and_past_paper_queries(self):
        groups = build_queries("高数")
        text = "\n".join(query for group in groups for query in group.queries)
        self.assertIn("高等数学", text)
        self.assertIn("Calculus", text)
        self.assertIn("课程大纲", text)
        self.assertIn("往年题", text)
        self.assertIn("复习课", text)

    def test_data_structures_oj_queries_include_coding_terms(self):
        groups = build_queries("Data Structures", assessment="oj")
        text = "\n".join(query for group in groups for query in group.queries)
        self.assertIn("OJ", text)
        self.assertIn("机考", text)
        self.assertIn("边界数据", text)
        self.assertIn("past problems", text)

    def test_school_scope_is_prefixed_when_present(self):
        groups = build_queries("线性代数", school="某大学", assessment="closed-book")
        text = "\n".join(query for group in groups for query in group.queries)
        self.assertIn("某大学 线性代数 课程大纲", text)
        self.assertIn("某大学 线性代数 闭卷", text)

    def test_cli_json_output(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "build_search_queries.py"), "数据结构", "--assessment", "oj", "--format", "json"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_DIR),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload)
        self.assertEqual(payload[0]["group"], "course_identity")
        all_queries = "\n".join(query for group in payload for query in group["queries"])
        self.assertIn("数据结构", all_queries)
        self.assertIn("OJ", all_queries)

    def test_cli_markdown_output(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "build_search_queries.py"), "大学物理", "--assessment", "lab"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_DIR),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## Search Query Groups", result.stdout)
        self.assertIn("实验考", result.stdout)
        self.assertIn("实验指导书", result.stdout)


if __name__ == "__main__":
    unittest.main()
