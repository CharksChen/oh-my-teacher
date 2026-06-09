#!/usr/bin/env python3
"""Bundle Oh My Teacher markdown references into a single system prompt file.

Useful when deploying the skill to environments that do not support
multi-file reference loading, such as OpenAI GPTs, Dify custom tools,
or plain ChatGPT system prompts.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Files to include (in order) and the context tag to prepend.
INCLUDE_ORDER: list[tuple[str, str]] = [
    ("SKILL.md", "=== SKILL.md (operating principle + command routing) ==="),
    ("references/INDEX.md", "=== INDEX.md (reference map + command catalog + environment fallbacks) ==="),
    ("references/course-profiles.md", "=== course-profiles.md (snapshot template + exam optimization) ==="),
    ("references/interaction-modes.md", "=== interaction-modes.md (teaching modes) ==="),
    ("references/subject-adaptation.md", "=== subject-adaptation.md (subject-specific adaptation) ==="),
    ("references/question-types.md", "=== question-types.md (question types + grading rubric) ==="),
    ("references/practice-workflows.md", "=== practice-workflows.md (active recall + mock + oral + error repair) ==="),
    ("references/review-plans.md", "=== review-plans.md (plans + cram + last page) ==="),
    ("references/spaced-repetition.md", "=== spaced-repetition.md (SRS algorithm) ==="),
    ("references/visual-generation.md", "=== visual-generation.md (visual + image + video) ==="),
    ("references/coding-demos.md", "=== coding-demos.md (code demo guidelines) ==="),
    ("references/materials-ingestion.md", "=== materials-ingestion.md (file ingestion) ==="),
]


def build(skill_root: Path, skip_optional: bool = False) -> str:
    parts: list[str] = []
    parts.append("# Oh My Teacher — Bundled Runtime Prompt")
    parts.append("")
    parts.append(f"Generated from: {skill_root.resolve()}")
    parts.append("")

    for rel_path, header in INCLUDE_ORDER:
        full_path = skill_root / rel_path
        if not full_path.exists():
            if skip_optional:
                continue
            print(f"Warning: {full_path} not found, skipping.", file=sys.stderr)
            continue
        text = full_path.read_text(encoding="utf-8")
        parts.append(header)
        parts.append("")
        # Strip YAML frontmatter from SKILL.md
        if rel_path == "SKILL.md" and text.startswith("---\n"):
            try:
                _, _, rest = text.split("---", 2)
                text = rest.lstrip("\n")
            except ValueError:
                pass
        parts.append(text.strip())
        parts.append("")

    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a bundled system prompt from Oh My Teacher references.")
    parser.add_argument("--root", default=".", help="Skill root directory (default: current dir).")
    parser.add_argument("--output", "-o", help="Output file (default: stdout).")
    parser.add_argument("--skip-optional", action="store_true", help="Silently skip missing files instead of warning.")
    args = parser.parse_args(argv)

    prompt = build(Path(args.root).resolve(), skip_optional=args.skip_optional)
    if args.output:
        Path(args.output).write_text(prompt, encoding="utf-8")
        print(f"Bundled prompt written to {args.output} ({len(prompt)} chars)", file=sys.stderr)
    else:
        sys.stdout.write(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
