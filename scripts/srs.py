#!/usr/bin/env python3
"""Manage Oh My Teacher spaced-repetition state."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from dataclasses import dataclass
from pathlib import Path

HEADER = ["Topic", "Last Review", "Score", "Streak", "Next Review", "Difficulty"]
INTERVALS = {1: 1, 2: 3, 3: 7, 4: 14}
DIFFICULTY_MULTIPLIER = {"easy": 1.4, "medium": 1.0, "hard": 0.6}
LEVEL_LABELS = {"easy": "简单", "medium": "中等", "hard": "困难"}


@dataclass
class Row:
    topic: str
    last_review: str
    score: int
    streak: int
    next_review: str
    difficulty: str = "medium"


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid ISO date: {value}") from exc


def state_root(workspace: Path) -> Path:
    return workspace / ".oh-my-teacher"


def single_srs_path(workspace: Path) -> Path:
    return state_root(workspace) / "srs-state.md"


def srs_dir(workspace: Path) -> Path:
    return state_root(workspace) / "srs"


def active_path(workspace: Path) -> Path:
    return srs_dir(workspace) / "_active"


def srs_path(workspace: Path, slug: str | None) -> Path:
    if slug:
        return srs_dir(workspace) / f"{slug}.md"
    return single_srs_path(workspace)


def resolve_slug(workspace: Path, args: argparse.Namespace) -> str | None:
    if getattr(args, "slug", None):
        return args.slug
    if getattr(args, "active", False):
        active = active_path(workspace)
        if not active.exists():
            raise SystemExit("No active SRS slug is set.")
        return active.read_text(encoding="utf-8").strip()
    return None


def warn_multi_course(workspace: Path, slug: str | None) -> None:
    if slug is None and srs_dir(workspace).is_dir():
        print(
            "Warning: multi-course SRS directory exists but no --slug or --active was given. "
            "Falling back to single-course srs-state.md.",
            file=sys.stderr,
        )


def _format_difficulty(row: Row) -> str:
    label = LEVEL_LABELS.get(row.difficulty, row.difficulty)
    return f"{row.difficulty} ({label})"


def markdown_table(rows: list[Row]) -> str:
    lines = [
        "| Topic | Last Review | Score | Streak | Next Review | Difficulty |",
        "|-------|-------------|-------|--------|-------------|------------|",
    ]
    for row in rows:
        lines.append(
            f"| {row.topic} | {row.last_review} | {row.score} | {row.streak} | {row.next_review} | {_format_difficulty(row)} |"
        )
    return "\n".join(lines) + "\n"


def parse_table(text: str) -> list[Row]:
    rows: list[Row] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) not in (5, 6):
            continue
        if cells[0] == "Topic" or set(cells[0]) <= {"-"}:
            continue
        try:
            score = int(cells[2])
            streak = int(cells[3])
        except ValueError:
            continue
        if len(cells) == 5:
            # Legacy format without difficulty column
            rows.append(Row(cells[0], cells[1], score, streak, cells[4]))
        else:
            diff = cells[5].split(" (")[0] if " (" in cells[5] else cells[5]
            if diff not in DIFFICULTY_MULTIPLIER:
                diff = "medium"
            rows.append(Row(cells[0], cells[1], score, streak, cells[4], difficulty=diff))
    return rows


def read_rows(path: Path) -> list[Row]:
    if not path.exists():
        return []
    return parse_table(path.read_text(encoding="utf-8"))


def write_rows(path: Path, rows: list[Row]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown_table(rows), encoding="utf-8")


def next_interval(streak: int, difficulty: str = "medium") -> int:
    """Return days until next review, adjusted by difficulty.

    - easy:   multiply by 1.4 (review less often)
    - medium: multiply by 1.0 (base SM-0 interval)
    - hard:   multiply by 0.6 (review more often)
    """
    base = INTERVALS.get(streak, 30)
    multiplier = DIFFICULTY_MULTIPLIER.get(difficulty, 1.0)
    return max(1, int(base * multiplier))


def updated_row(
    topic: str,
    score: int,
    today: dt.date,
    old: Row | None = None,
    difficulty: str = "medium",
) -> Row:
    if score <= 2:
        streak = 0
        interval = 1
    else:
        streak = (old.streak if old else 0) + 1
        interval = next_interval(streak, difficulty)
    return Row(
        topic=topic,
        last_review=today.isoformat(),
        score=score,
        streak=streak,
        next_review=(today + dt.timedelta(days=interval)).isoformat(),
        difficulty=difficulty,
    )


def cmd_init(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    path = srs_path(workspace, args.slug)
    if path.exists() and not args.force:
        raise SystemExit(f"SRS file already exists: {path}")
    write_rows(path, [])
    if args.slug and args.active:
        active_path(workspace).write_text(args.slug, encoding="utf-8")
    print(path)
    return 0


def cmd_set_active(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    path = srs_path(workspace, args.slug)
    if args.require_exists and not path.exists():
        raise SystemExit(f"SRS file not found: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    active_path(workspace).write_text(args.slug, encoding="utf-8")
    print(args.slug)
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    today = parse_date(args.today)
    slug = resolve_slug(workspace, args)
    warn_multi_course(workspace, slug)
    path = srs_path(workspace, slug)
    rows = read_rows(path)
    old = next((row for row in rows if row.topic == args.topic), None)
    new = updated_row(args.topic, args.score, today, old, difficulty=args.difficulty)
    rows = [row for row in rows if row.topic != args.topic] + [new]
    write_rows(path, sorted(rows, key=lambda row: row.topic.lower()))
    print(f"{new.topic}\t{new.score}\t{new.streak}\t{new.next_review}\t{new.difficulty}")
    return 0


def cmd_due(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    today = parse_date(args.today)
    slug = resolve_slug(workspace, args)
    warn_multi_course(workspace, slug)
    rows = read_rows(srs_path(workspace, slug))
    due = [row for row in rows if parse_date(row.next_review) <= today]
    due.sort(key=lambda row: ((today - parse_date(row.next_review)).days, -row.score), reverse=True)
    if args.format == "tsv":
        writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
        writer.writerow(HEADER)
        for row in due:
            writer.writerow([row.topic, row.last_review, row.score, row.streak, row.next_review, row.difficulty])
    else:
        sys.stdout.write(markdown_table(due))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    slug = resolve_slug(workspace, args)
    warn_multi_course(workspace, slug)
    sys.stdout.write(markdown_table(read_rows(srs_path(workspace, slug))))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Oh My Teacher SRS state.")
    parser.add_argument("--workspace", default=".", help="Workspace root.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create an empty SRS table.")
    init.add_argument("--slug", help="Course slug for multi-course mode.")
    init.add_argument("--active", action="store_true", help="Set slug active.")
    init.add_argument("--force", action="store_true", help="Overwrite existing file.")
    init.set_defaults(func=cmd_init)

    active = sub.add_parser("set-active", help="Set active multi-course SRS slug.")
    active.add_argument("slug")
    active.add_argument("--require-exists", action="store_true")
    active.set_defaults(func=cmd_set_active)

    update = sub.add_parser("update", help="Update one topic after quiz or grading.")
    update.add_argument("topic")
    update.add_argument("--score", type=int, choices=range(1, 6), required=True)
    update.add_argument("--today", default=dt.date.today().isoformat(), help="ISO date (default: today).")
    update.add_argument("--slug")
    update.add_argument("--active", action="store_true")
    update.add_argument("--difficulty", choices=("easy", "medium", "hard"), default="medium",
                        help="Difficulty level (easy → 1.4x interval, medium → 1.0x, hard → 0.6x)")
    update.set_defaults(func=cmd_update)

    due = sub.add_parser("due", help="List due topics.")
    due.add_argument("--today", default=dt.date.today().isoformat(), help="ISO date (default: today).")
    due.add_argument("--slug")
    due.add_argument("--active", action="store_true")
    due.add_argument("--format", choices=("markdown", "tsv"), default="markdown")
    due.set_defaults(func=cmd_due)

    list_cmd = sub.add_parser("list", help="List all rows.")
    list_cmd.add_argument("--slug")
    list_cmd.add_argument("--active", action="store_true")
    list_cmd.set_defaults(func=cmd_list)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
