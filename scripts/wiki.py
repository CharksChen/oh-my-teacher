#!/usr/bin/env python3
"""Manage the Oh My Teacher course wiki (LLM Wiki layer).

A course wiki is a persistent, interlinked Markdown knowledge base that
accumulates as the user adds materials, replacing "re-read every source on
every question" RAG. This helper keeps the on-disk layout and the
deterministic health check (lint) stable so the model does not hand-roll
file paths, orphan detection, or broken-link scanning.

Layout (per course slug):

    .oh-my-teacher/wiki/<slug>/
        INDEX.md        # home / map-of-content (MOC)
        sources/        # immutable raw captures (never edited after capture)
        pages/          # LLM-maintained wiki pages (*.md, interlinked via [[..]])

See references/course-wiki.md for the page taxonomy and Ingest/Query/Lint
operations this script supports.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[\s*([^\]|#]+?)\s*(?:[#|][^\]]*)?\]\]")
HOME_TARGETS = {"index", "home", "课程主页", "知识库", "wiki"}
CITATION_MARKERS = ("来源", "sources:", "课程资料确认", "引用", "出处")


def slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug, flags=re.UNICODE)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "page"


def state_root(workspace: Path) -> Path:
    return workspace / ".oh-my-teacher"


def wiki_root(workspace: Path) -> Path:
    return state_root(workspace) / "wiki"


def course_dir(workspace: Path, slug: str) -> Path:
    return wiki_root(workspace) / slug


def pages_dir(workspace: Path, slug: str) -> Path:
    return course_dir(workspace, slug) / "pages"


def sources_dir(workspace: Path, slug: str) -> Path:
    return course_dir(workspace, slug) / "sources"


def index_path(workspace: Path, slug: str) -> Path:
    return course_dir(workspace, slug) / "INDEX.md"


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and "\n---" in text[4:]


def has_citation(text: str) -> bool:
    return any(marker in text for marker in CITATION_MARKERS)


def wikilink_targets(text: str) -> list[str]:
    return [match.group(1).strip() for match in WIKILINK_RE.finditer(text)]


def page_files(workspace: Path, slug: str) -> list[Path]:
    directory = pages_dir(workspace, slug)
    if not directory.exists():
        return []
    return sorted(directory.glob("*.md"))


def page_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped.startswith("title:"):
            return stripped.split(":", 1)[1].strip()
    return fallback


INDEX_TEMPLATE = """# {course} 课程知识库（Course Wiki）

> Oh My Teacher 课程 wiki。原始资料在 `sources/`（只进不改），知识页面在 `pages/`。
> 用 `python scripts/wiki.py` 维护结构，不要手写链接索引。

## 章节 MOC（Map of Content）
（按章节加入页面 wikilink，例如 第3章-极限）

## 考点页（Exam Points）
（高频考点页面）

## 概念页（Concepts）
（定义、定理、公式页面）

## 错题页（Wrong Points）
（从错题本派生的页面）

## 待办缺口（Open Gaps）
（尚未覆盖的考试范围、缺少来源的主题）
"""


def cmd_slug(args: argparse.Namespace) -> int:
    print(slugify(args.course))
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    slug = args.slug or slugify(args.course)
    pages_dir(workspace, slug).mkdir(parents=True, exist_ok=True)
    sources_dir(workspace, slug).mkdir(parents=True, exist_ok=True)
    index = index_path(workspace, slug)
    if not index.exists():
        course_name = args.course or slug
        index.write_text(INDEX_TEMPLATE.format(course=course_name), encoding="utf-8")
    print(course_dir(workspace, slug))
    return 0


PAGE_TEMPLATE = """---
title: {title}
type: {type}
tags: [{tags}]
priority: {priority}
sources: [{sources}]
srs: {srs}
---

# {title}

来源: {citation}

（在此填写定义/条件/直觉/陷阱/例题）

相关:
"""


def cmd_add_source(args: argparse.Namespace) -> int:
    """Capture an input file into the immutable sources/ directory."""
    workspace = Path(args.workspace).resolve()
    slug = args.slug or slugify(args.course)
    if not index_path(workspace, slug).exists():
        print(f"Course wiki not initialized: run `wiki.py init --slug {slug}` first.", file=sys.stderr)
        return 1
    src = Path(args.file)
    if not src.is_file():
        print(f"Source file not found: {src}", file=sys.stderr)
        return 1
    target_dir = sources_dir(workspace, slug)
    target_dir.mkdir(parents=True, exist_ok=True)
    name = args.name or src.name
    target = target_dir / name
    if target.exists() and not args.force:
        # Immutable by default: refuse to overwrite a captured source.
        if target.read_bytes() == src.read_bytes():
            print(f"sources/{name}")  # already captured, identical content
            return 0
        print(f"Source already captured with different content: {target} (use --force).", file=sys.stderr)
        return 1
    shutil.copyfile(src, target)
    print(f"sources/{name}")
    return 0


def cmd_new_page(args: argparse.Namespace) -> int:
    """Create a wiki page with well-formed frontmatter so lint passes by construction."""
    workspace = Path(args.workspace).resolve()
    slug = args.slug or slugify(args.course)
    if not course_dir(workspace, slug).exists():
        print(f"Course wiki not found: {course_dir(workspace, slug)} (run init first).", file=sys.stderr)
        return 1
    page_slug = args.page_slug or slugify(args.title)
    directory = pages_dir(workspace, slug)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{page_slug}.md"
    if target.exists() and not args.force:
        print(f"Page already exists: {target} (use --force to overwrite).", file=sys.stderr)
        return 1
    tags = ", ".join(t.strip() for t in args.tags.split(",") if t.strip()) if args.tags else ""
    sources = ", ".join(s.strip() for s in args.sources.split(",") if s.strip()) if args.sources else ""
    citation = "需要确认" if not sources else "课程资料确认"
    target.write_text(
        PAGE_TEMPLATE.format(
            title=args.title,
            type=args.type,
            tags=tags,
            priority=args.priority,
            sources=sources,
            srs=args.srs or page_slug,
            citation=citation,
        ),
        encoding="utf-8",
    )
    print(target)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    slug = args.slug or slugify(args.course)
    directory = course_dir(workspace, slug)
    if not directory.exists():
        print(f"Course wiki not found: {directory}", file=sys.stderr)
        return 1
    index = index_path(workspace, slug)
    if index.exists():
        print(f"INDEX\t{index}")
    for path in page_files(workspace, slug):
        title = page_title(path.read_text(encoding="utf-8"), path.stem)
        print(f"{path.stem}\t{title}\t{path}")
    return 0


def collect_lint(workspace: Path, slug: str) -> dict:
    files = page_files(workspace, slug)
    page_slugs = {path.stem for path in files}
    inbound: dict[str, int] = {stem: 0 for stem in page_slugs}
    broken_links: list[dict[str, str]] = []
    missing_frontmatter: list[str] = []
    missing_citation: list[str] = []

    def register_links(text: str, source_label: str) -> None:
        for target in wikilink_targets(text):
            target_slug = slugify(target)
            if target.strip().lower() in HOME_TARGETS or target_slug in HOME_TARGETS:
                continue
            if target_slug in page_slugs:
                inbound[target_slug] += 1
            else:
                broken_links.append({"page": source_label, "target": target})

    index = index_path(workspace, slug)
    if index.exists():
        register_links(index.read_text(encoding="utf-8"), "INDEX")

    for path in files:
        text = path.read_text(encoding="utf-8")
        register_links(text, path.stem)
        if not has_frontmatter(text):
            missing_frontmatter.append(path.stem)
        if not has_citation(text):
            missing_citation.append(path.stem)

    orphans = sorted(stem for stem, count in inbound.items() if count == 0)
    issues = len(orphans) + len(broken_links) + len(missing_frontmatter) + len(missing_citation)
    return {
        "course": slug,
        "pages": len(files),
        "orphans": orphans,
        "broken_links": broken_links,
        "missing_frontmatter": sorted(missing_frontmatter),
        "missing_citation": sorted(missing_citation),
        "issues": issues,
        "ok": issues == 0,
    }


def cmd_lint(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    slug = args.slug or slugify(args.course)
    if not course_dir(workspace, slug).exists():
        print(f"Course wiki not found: {course_dir(workspace, slug)}", file=sys.stderr)
        return 1
    report = collect_lint(workspace, slug)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"# Wiki lint: {slug}")
        print(f"pages: {report['pages']}  issues: {report['issues']}")
        if report["orphans"]:
            print(f"orphans (无入链): {', '.join(report['orphans'])}")
        for link in report["broken_links"]:
            print(f"broken link: {link['page']} -> [[{link['target']}]]")
        if report["missing_frontmatter"]:
            print(f"missing frontmatter: {', '.join(report['missing_frontmatter'])}")
        if report["missing_citation"]:
            print(f"missing citation (无来源): {', '.join(report['missing_citation'])}")
        if report["ok"]:
            print("OK: no structural issues.")

    if args.strict and not report["ok"]:
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the Oh My Teacher course wiki.")
    parser.add_argument(
        "--workspace",
        default=os.environ.get("OMT_WORKSPACE", "."),
        help="Workspace root containing .oh-my-teacher/ (default: $OMT_WORKSPACE or current directory).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    slug = sub.add_parser("slug", help="Print the deterministic slug for a course name.")
    slug.add_argument("course")
    slug.set_defaults(func=cmd_slug)

    init = sub.add_parser("init", help="Create the course wiki layout (sources/, pages/, INDEX.md).")
    init.add_argument("--course", help="Course name used to derive a slug and title.")
    init.add_argument("--slug", help="Explicit course slug (overrides --course for the path).")
    init.set_defaults(func=cmd_init)

    add_source = sub.add_parser("add-source", help="Capture an input file into the immutable sources/ directory.")
    add_source.add_argument("file", help="Path to the input file (PDF/PPT/notes/past paper, etc.).")
    add_source.add_argument("--course", help="Course name used to derive a slug.")
    add_source.add_argument("--slug", help="Explicit course slug.")
    add_source.add_argument("--name", help="Stored filename (default: original filename).")
    add_source.add_argument("--force", action="store_true", help="Overwrite an existing captured source.")
    add_source.set_defaults(func=cmd_add_source)

    new_page = sub.add_parser("new-page", help="Create a wiki page with well-formed frontmatter.")
    new_page.add_argument("--title", required=True, help="Page title.")
    new_page.add_argument("--course", help="Course name used to derive a slug.")
    new_page.add_argument("--slug", help="Explicit course slug.")
    new_page.add_argument("--page-slug", help="Explicit page slug (default: slugified title).")
    new_page.add_argument("--type", default="concept", help="Page type: concept, theorem, exam-point, chapter, wrong-point.")
    new_page.add_argument("--priority", default="P1", help="Exam priority: P0/P1/P2.")
    new_page.add_argument("--tags", help="Comma-separated tags.")
    new_page.add_argument("--sources", help="Comma-separated source paths, e.g. sources/lecture-03.md.")
    new_page.add_argument("--srs", help="SRS topic name (default: page slug).")
    new_page.add_argument("--force", action="store_true", help="Overwrite an existing page.")
    new_page.set_defaults(func=cmd_new_page)

    list_cmd = sub.add_parser("list", help="List the wiki INDEX and pages for a course.")
    list_cmd.add_argument("--course", help="Course name used to derive a slug.")
    list_cmd.add_argument("--slug", help="Explicit course slug.")
    list_cmd.set_defaults(func=cmd_list)

    lint = sub.add_parser("lint", help="Report orphans, broken [[links]], missing frontmatter/citations.")
    lint.add_argument("--course", help="Course name used to derive a slug.")
    lint.add_argument("--slug", help="Explicit course slug.")
    lint.add_argument("--json", action="store_true", help="Emit the lint report as JSON.")
    lint.add_argument("--strict", action="store_true", help="Return non-zero exit code if any issue is found.")
    lint.set_defaults(func=cmd_lint)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "command", None) in {"init", "list", "lint", "add-source", "new-page"} and not args.slug and not args.course:
        parser.error(f"{args.command} requires --course or --slug.")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
