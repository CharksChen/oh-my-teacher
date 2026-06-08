#!/usr/bin/env python3
"""Validate the Oh My Teacher skill package.

The checks are intentionally local and dependency-free so they can run in
ordinary agent shells before packaging or after edits.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT_FILES = {"SKILL.md", "README.md"}
COMMAND_RE = re.compile(r"(?<![\w/])/(?P<cmd>[a-z][a-z0-9-]*)(?![\w.-])")
INDEX_ROW_RE = re.compile(r"^\|\s*`(?P<command>/[a-z][a-z0-9-]*)(?:\s+[^`]*)?`\s*\|")
INDEX_REF_RE = re.compile(r"`([\w-]+\.md)`")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(skill_md: str) -> dict[str, str]:
    if not skill_md.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter.")
    try:
        raw = skill_md.split("---", 2)[1]
    except IndexError as exc:
        raise ValueError("SKILL.md frontmatter is not closed.") from exc
    result: dict[str, str] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            if current_key is not None:
                result[current_key] += "\n" + line.strip()
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        current_key = key.strip()
        result[current_key] = value.strip()
    return result


def commands_from_index(index_md: str) -> set[str]:
    commands: set[str] = set()
    for line in index_md.splitlines():
        match = INDEX_ROW_RE.match(line)
        if match:
            commands.add(match.group("command"))
    return commands


def commands_from_markdown(root: Path) -> dict[Path, set[str]]:
    found: dict[Path, set[str]] = {}
    for path in sorted(root.rglob("*.md")):
        if any(part == "__pycache__" for part in path.parts):
            continue
        text = read_text(path)
        commands = {"/" + match.group("cmd") for match in COMMAND_RE.finditer(text)}
        if commands:
            found[path] = commands
    return found


def check(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    skill_path = root / "SKILL.md"
    index_path = root / "references" / "INDEX.md"
    agent_path = root / "agents" / "openai.yaml"

    check(skill_path.exists(), errors, "Missing SKILL.md.")
    check(index_path.exists(), errors, "Missing references/INDEX.md.")
    check(agent_path.exists(), errors, "Missing agents/openai.yaml.")

    required_scripts = [
        "export_flashcards.py",
        "snapshot.py",
        "srs.py",
        "validate_skill.py",
        "package_check.py",
    ]
    scripts_dir = root / "scripts"
    for name in required_scripts:
        check(
            (scripts_dir / name).exists(),
            errors,
            f"Missing required script: scripts/{name}.",
        )
    if errors:
        return errors

    try:
        fm = frontmatter(read_text(skill_path))
    except ValueError as exc:
        errors.append(str(exc))
        fm = {}
    check(set(fm) >= {"name", "description"}, errors, "SKILL.md frontmatter must contain at least name and description.")
    allowed_keys = {"name", "description", "when"}
    extra_keys = set(fm) - allowed_keys
    check(not extra_keys, errors, "SKILL.md frontmatter has unrecognized keys: " + ", ".join(sorted(extra_keys)))
    check(fm.get("name") == "oh-my-teacher", errors, "SKILL.md frontmatter name must be oh-my-teacher.")
    check(bool(fm.get("description")), errors, "SKILL.md frontmatter description must be non-empty.")

    index_text = read_text(index_path)
    index_commands = commands_from_index(index_text)
    check(bool(index_commands), errors, "references/INDEX.md does not define any command rows.")

    found_by_file = commands_from_markdown(root)
    all_found = set().union(*found_by_file.values()) if found_by_file else set()
    unregistered = sorted(all_found - index_commands)
    check(not unregistered, errors, "Unregistered slash commands found: " + ", ".join(unregistered))

    required_commands = {
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
    }
    missing_required = sorted(required_commands - index_commands)
    check(not missing_required, errors, "Core commands missing from INDEX.md: " + ", ".join(missing_required))

    # Check that reference files cited in INDEX.md Command Catalog actually exist
    refs_dir = root / "references"
    if refs_dir.exists():
        known_refs = {p.name for p in refs_dir.glob("*.md")}
        referenced_in_index: set[str] = set()
        in_catalog = False
        for line in index_text.splitlines():
            if line.startswith("## Command Catalog"):
                in_catalog = True
                continue
            if in_catalog and line.startswith("## "):
                break
            if in_catalog and line.startswith("|") and "`/" in line:
                referenced_in_index.update(INDEX_REF_RE.findall(line))
        # SKILL.md is a valid root-level reference, not in references/
        referenced_in_index.discard("SKILL.md")
        missing_refs = sorted(referenced_in_index - known_refs)
        check(not missing_refs, errors, "INDEX.md references non-existent files: " + ", ".join(missing_refs))

    pycache_dirs = [p for p in root.rglob("__pycache__") if p.is_dir()]
    check(not pycache_dirs, errors, "Generated __pycache__ directories found: " + ", ".join(str(p) for p in pycache_dirs))

    agent_text = read_text(agent_path)
    check("SKILL.md" in agent_text, errors, "agents/openai.yaml instructions should reference SKILL.md as the primary guide.")
    check("Follow SKILL.md" in agent_text or "Follow the SKILL.md" in agent_text, errors, "agents/openai.yaml instructions should tell the agent to follow SKILL.md rather than duplicate its rules.")

    # Stale-reference checks
    compat_path = root / "references" / "review-workflows.md"
    if compat_path.exists():
        compat_text = read_text(compat_path)
        is_compat = (compat_text.strip().startswith("# Review Workflows") and
                     ("compatibility" in compat_text.lower() or "redirect" in compat_text.lower() or "do not use" in compat_text.lower()))
        check(is_compat, errors, "references/review-workflows.md should be a compatibility entry point that redirects to narrower files, not contain substantive workflow content.")

    readme_path = root / "README.md"
    if readme_path.exists():
        readme_text = read_text(readme_path)
        stale_refs = []
        # Check for mentions of removed/renamed reference files
        known_refs = {p.name for p in (root / "references").glob("*.md")}
        referenced_in_readme = {m.group(1) for m in re.finditer(r"references/([\w-]+\.md)", readme_text)}
        for ref in sorted(referenced_in_readme):
            if ref not in known_refs:
                stale_refs.append(ref)
        check(not stale_refs, errors, "README.md references non-existent files: " + ", ".join(stale_refs))
        # Check for mentions of the old single-file review-workflows as a substantive source
        if "review-workflows.md" in readme_text and "compatibility" not in readme_text.lower() and "redirect" not in readme_text.lower():
            errors.append("README.md mentions review-workflows.md without noting it is a compatibility/redirect entry.")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Oh My Teacher skill package.")
    parser.add_argument("--root", default=".", help="Skill root directory.")
    args = parser.parse_args(argv)

    errors = validate(Path(args.root).resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
