"""Tests for scripts/wiki.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from wiki import slugify  # noqa: E402


GOOD_PAGE = """---
title: 极限的 epsilon-delta 定义
tags: [数学分析, 极限]
sources: [sources/lecture-03.md]
---

# 极限的 epsilon-delta 定义

来源: 课程资料确认（lecture-03）。

相关: [[连续性]]
"""

LINKING_PAGE = """---
title: 连续性
tags: [数学分析]
sources: [sources/lecture-04.md]
---

# 连续性

来源: 课程资料确认。

依赖 [[极限的-epsilon-delta-定义]]。
"""


class WikiTests(unittest.TestCase):
    def _script(self) -> str:
        return str(SCRIPT_DIR / "wiki.py")

    def _run(self, tmp: str, *args: str, **kwargs) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, self._script(), "--workspace", tmp, *args],
            capture_output=True,
            text=True,
            **kwargs,
        )

    def test_slugify(self):
        self.assertEqual(slugify("Limit Definition!"), "limit-definition")
        self.assertEqual(slugify("  Epsilon   Delta  "), "epsilon-delta")
        self.assertEqual(slugify("数据结构"), "数据结构")

    def test_init_creates_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(tmp, "init", "--course", "数学分析")
            self.assertEqual(result.returncode, 0, result.stderr)
            root = Path(tmp) / ".oh-my-teacher" / "wiki" / "数学分析"
            self.assertTrue((root / "pages").is_dir())
            self.assertTrue((root / "sources").is_dir())
            index = root / "INDEX.md"
            self.assertTrue(index.exists())
            self.assertIn("课程知识库", index.read_text(encoding="utf-8"))

    def test_init_is_idempotent_and_keeps_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "init", "--slug", "ds")
            index = Path(tmp) / ".oh-my-teacher" / "wiki" / "ds" / "INDEX.md"
            index.write_text("# custom home\n[[a]]\n", encoding="utf-8")
            self._run(tmp, "init", "--slug", "ds")
            self.assertEqual(index.read_text(encoding="utf-8"), "# custom home\n[[a]]\n")

    def test_init_requires_course_or_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(tmp, "init")
            self.assertNotEqual(result.returncode, 0)

    def test_list_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "init", "--slug", "ma")
            pages = Path(tmp) / ".oh-my-teacher" / "wiki" / "ma" / "pages"
            (pages / "极限的-epsilon-delta-定义.md").write_text(GOOD_PAGE, encoding="utf-8")
            result = self._run(tmp, "list", "--slug", "ma")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("INDEX", result.stdout)
            self.assertIn("极限的 epsilon-delta 定义", result.stdout)

    def test_lint_clean_when_pages_linked_and_cited(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "init", "--slug", "ma")
            root = Path(tmp) / ".oh-my-teacher" / "wiki" / "ma"
            pages = root / "pages"
            (pages / "极限的-epsilon-delta-定义.md").write_text(GOOD_PAGE, encoding="utf-8")
            (pages / "连续性.md").write_text(LINKING_PAGE, encoding="utf-8")
            # INDEX links both so neither is an orphan.
            (root / "INDEX.md").write_text(
                "# home\n[[极限的-epsilon-delta-定义]] [[连续性]]\n", encoding="utf-8"
            )
            result = self._run(tmp, "lint", "--slug", "ma", "--json", "--strict")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertTrue(report["ok"], report)
            self.assertEqual(report["pages"], 2)

    def test_lint_detects_broken_link_and_orphan(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "init", "--slug", "ma")
            root = Path(tmp) / ".oh-my-teacher" / "wiki" / "ma"
            pages = root / "pages"
            # Orphan page (no inbound), with a broken link, no frontmatter, no citation.
            (pages / "孤页.md").write_text("# 孤页\n指向 [[不存在的页面]]\n", encoding="utf-8")
            result = self._run(tmp, "lint", "--slug", "ma", "--json", "--strict")
            self.assertNotEqual(result.returncode, 0)
            report = json.loads(result.stdout)
            self.assertFalse(report["ok"])
            self.assertIn("孤页", report["orphans"])
            self.assertEqual(report["broken_links"][0]["target"], "不存在的页面")
            self.assertIn("孤页", report["missing_frontmatter"])
            self.assertIn("孤页", report["missing_citation"])

    def test_add_source_captures_and_is_immutable(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "init", "--slug", "ma")
            src = Path(tmp) / "lecture03.md"
            src.write_text("# 第3章 极限\nepsilon-delta\n", encoding="utf-8")
            result = self._run(tmp, "add-source", str(src), "--slug", "ma")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "sources/lecture03.md")
            stored = Path(tmp) / ".oh-my-teacher" / "wiki" / "ma" / "sources" / "lecture03.md"
            self.assertTrue(stored.exists())
            # Re-capturing identical content is a no-op success.
            again = self._run(tmp, "add-source", str(src), "--slug", "ma")
            self.assertEqual(again.returncode, 0, again.stderr)
            # Changed content without --force is refused (immutable).
            src.write_text("# 第3章 极限 (改)\n", encoding="utf-8")
            refused = self._run(tmp, "add-source", str(src), "--slug", "ma")
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("different content", refused.stderr)

    def test_add_source_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "init", "--slug", "ma")
            result = self._run(tmp, "add-source", str(Path(tmp) / "nope.pdf"), "--slug", "ma")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not found", result.stderr)

    def test_add_source_requires_init(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "notes.md"
            src.write_text("hello\n", encoding="utf-8")
            result = self._run(tmp, "add-source", str(src), "--slug", "nope")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not initialized", result.stderr)

    def test_new_page_is_lint_clean_when_linked(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "init", "--slug", "ma")
            result = self._run(
                tmp, "new-page", "--slug", "ma", "--title", "极限",
                "--sources", "sources/lecture-03.md", "--tags", "数学分析,极限",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            page = Path(tmp) / ".oh-my-teacher" / "wiki" / "ma" / "pages" / "极限.md"
            text = page.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn("来源:", text)
            self.assertIn("课程资料确认", text)
            # Link it from INDEX so it is not an orphan, then lint must be clean.
            (Path(tmp) / ".oh-my-teacher" / "wiki" / "ma" / "INDEX.md").write_text(
                "# home\n[[极限]]\n", encoding="utf-8"
            )
            lint = self._run(tmp, "lint", "--slug", "ma", "--json", "--strict")
            self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)

    def test_new_page_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "init", "--slug", "ma")
            self._run(tmp, "new-page", "--slug", "ma", "--title", "极限")
            again = self._run(tmp, "new-page", "--slug", "ma", "--title", "极限")
            self.assertNotEqual(again.returncode, 0)
            self.assertIn("already exists", again.stderr)

    def test_new_page_without_sources_marks_unconfirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "init", "--slug", "ma")
            self._run(tmp, "new-page", "--slug", "ma", "--title", "连续性")
            page = Path(tmp) / ".oh-my-teacher" / "wiki" / "ma" / "pages" / "连续性.md"
            self.assertIn("需要确认", page.read_text(encoding="utf-8"))

    def test_lint_missing_course_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(tmp, "lint", "--slug", "nope")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
