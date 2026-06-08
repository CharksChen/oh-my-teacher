"""Tests for scripts/snapshot.py."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from snapshot import slugify  # noqa: E402


SNAPSHOT = """## Current Course Snapshot
- **Course**: Data Structures / Computer Science
- **Assessment**: coding exam
- **Days left**: 7
- **Level**: shaky
- **Environment**: agent-shell
- **Materials**: notes
- **LaTeX**: not applicable
- **Weak points**: [graphs]
- **Completed**: []
- **Accuracy**: "graphs 4/10"
- **Last action**: /quiz
- **Next recommended**: /fix on graphs
"""


class SnapshotTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Data Structures!"), "data-structures")
        self.assertEqual(slugify("  Linear   Algebra  "), "linear-algebra")
        # Chinese characters are preserved (Unicode-aware), punctuation stripped
        self.assertEqual(slugify("数据结构与算法"), "数据结构与算法")
        self.assertEqual(slugify("操作系统（OS）"), "操作系统os")

    def test_save_load_and_active(self):
        script = SCRIPT_DIR / "snapshot.py"
        with tempfile.TemporaryDirectory() as tmp:
            save = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--workspace",
                    tmp,
                    "save",
                    "--course",
                    "Data Structures",
                    "--active",
                ],
                input=SNAPSHOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(save.returncode, 0, save.stderr)

            load = subprocess.run(
                [sys.executable, str(script), "--workspace", tmp, "load", "--active"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(load.returncode, 0, load.stderr)
            self.assertEqual(load.stdout, SNAPSHOT)

            active = Path(tmp) / ".oh-my-teacher" / "snapshots" / "_active"
            self.assertEqual(active.read_text(encoding="utf-8"), "data-structures")


if __name__ == "__main__":
    unittest.main()
