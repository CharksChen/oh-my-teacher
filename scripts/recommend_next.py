#!/usr/bin/env python3
"""Rank the next Oh My Teacher review actions from lightweight local state."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import srs

PRIORITY_SCORE = {"P0": 40, "P1": 25, "P2": 10}
TEACHER_SCORE = {"high": 18, "medium": 10, "low": 3}
MASTERY_SCORE = {"weak": 30, "unstable": 18, "ok": 5, "strong": -20}
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "unknown": 3}


@dataclass
class Recommendation:
    topic: str
    score: int
    why: list[str]
    action: str
    priority: str
    mastery: str
    due: bool


def state_root(workspace: Path) -> Path:
    return workspace / ".oh-my-teacher"


def state_json_path(workspace: Path) -> Path:
    return state_root(workspace) / "state.json"


def load_state(workspace: Path) -> dict:
    path = state_json_path(workspace)
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid state JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"State JSON must contain an object: {path}")
    return value


def parse_days_left(snapshot: dict) -> int | None:
    raw = str(snapshot.get("days_left", "")).strip()
    match = re.search(r"-?\d+", raw)
    if not match:
        return None
    return int(match.group(0))


def active_srs_slug(workspace: Path, state: dict, explicit: str | None, active: bool) -> str | None:
    if explicit:
        return explicit
    if active:
        active_file = workspace / ".oh-my-teacher" / "srs" / "_active"
        if active_file.exists():
            return active_file.read_text(encoding="utf-8").strip()
    slug = state.get("active_slug")
    return slug if isinstance(slug, str) and slug else None


def load_srs_rows(workspace: Path, slug: str | None) -> dict[str, srs.Row]:
    path = srs.srs_path(workspace, slug)
    return {row.topic: row for row in srs.read_rows(path)}


def score_topic(name: str, data: dict, row: srs.Row | None, today: dt.date, days_left: int | None) -> Recommendation:
    priority = str(data.get("priority", "unknown"))
    mastery = str(data.get("mastery_band", "unknown"))
    teacher = str(data.get("teacher_emphasis_strength", "unknown"))
    blocked_by = data.get("blocked_by") or []
    if not isinstance(blocked_by, list):
        blocked_by = [str(blocked_by)]

    total = 0
    why: list[str] = []

    value = PRIORITY_SCORE.get(priority, 0)
    if value:
        total += value
        why.append(priority)

    try:
        exam_scope = int(float(data.get("exam_scope_weight", 0)))
    except (TypeError, ValueError):
        exam_scope = 0
    if exam_scope:
        value = min(exam_scope, 25)
        total += value
        why.append(f"exam weight +{value}")

    try:
        frequency = int(float(data.get("past_paper_frequency", 0)))
    except (TypeError, ValueError):
        frequency = 0
    if frequency:
        value = min(frequency * 6, 18)
        total += value
        why.append(f"past papers +{value}")

    value = TEACHER_SCORE.get(teacher, 0)
    if value:
        total += value
        why.append(f"teacher {teacher}")

    value = MASTERY_SCORE.get(mastery, 0)
    if value:
        total += value
        why.append(mastery)

    due = False
    if row is not None:
        try:
            overdue = (today - srs.parse_date(row.next_review)).days
        except SystemExit:
            overdue = -1
        if overdue >= 0:
            due = True
            value = 12 + min(overdue, 10)
            total += value
            why.append(f"SRS due +{value}")

    if blocked_by:
        total += 20
        why.append("prerequisite block")

    if days_left is not None and days_left <= 3 and priority in {"P0", "P1"} and mastery in {"weak", "unstable"}:
        total += 10
        why.append("urgent")

    action = choose_action(name, priority, mastery, blocked_by, due)
    return Recommendation(name, total, why or ["needs evidence"], action, priority, mastery, due)


def choose_action(name: str, priority: str, mastery: str, blocked_by: list[str], due: bool) -> str:
    if blocked_by:
        return f"/fix prerequisite {blocked_by[0]} before {name}"
    if mastery == "weak":
        return f"/fix {name}"
    if mastery == "unstable":
        return f"/quiz {name} with one close variant"
    if mastery == "ok":
        return f"/quiz {name} interleaved, then schedule SRS"
    if mastery == "strong":
        if due and priority in {"P0", "P1"}:
            return f"/review-due quick recall for {name}"
        return f"de-prioritize {name} to quick review"
    if due:
        return f"/review-due {name}"
    return f"/diagnose or /quiz {name}"


def rank_recommendations(state: dict, rows: dict[str, srs.Row], today: dt.date) -> list[Recommendation]:
    adaptive = state.get("adaptive", {})
    topics = adaptive.get("topics", {}) if isinstance(adaptive, dict) else {}
    if not isinstance(topics, dict):
        raise SystemExit("state.json adaptive.topics must be an object when present.")

    for topic, row in rows.items():
        topics.setdefault(topic, {
            "priority": "unknown",
            "mastery_band": "weak" if row.score <= 2 else "ok" if row.score >= 4 else "unstable",
            "last_evidence": f"SRS score {row.score}, next {row.next_review}",
        })

    snapshot = state.get("snapshot", {}) if isinstance(state.get("snapshot"), dict) else {}
    days_left = parse_days_left(snapshot)
    ranked = [
        score_topic(str(name), data if isinstance(data, dict) else {}, rows.get(str(name)), today, days_left)
        for name, data in topics.items()
    ]
    ranked.sort(key=lambda item: (
        -item.score,
        PRIORITY_ORDER.get(item.priority, 3),
        {"weak": 0, "unstable": 1, "ok": 2, "strong": 3}.get(item.mastery, 4),
        not item.due,
        item.topic.lower(),
    ))
    return ranked


def emit_markdown(items: list[Recommendation], limit: int) -> None:
    print("## 下一步推荐")
    print("| Rank | Topic | Score | Why now | Action |")
    print("|---|---|---:|---|---|")
    for index, item in enumerate(items[:limit], start=1):
        why = "; ".join(item.why)
        print(f"| {index} | {item.topic} | {item.score} | {why} | {item.action} |")


def emit_json(items: list[Recommendation], limit: int) -> None:
    payload = [
        {
            "rank": index,
            "topic": item.topic,
            "score": item.score,
            "why": item.why,
            "action": item.action,
            "priority": item.priority,
            "mastery_band": item.mastery,
            "srs_due": item.due,
        }
        for index, item in enumerate(items[:limit], start=1)
    ]
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank next review actions from Oh My Teacher state.")
    parser.add_argument("--workspace", default=os.environ.get("OMT_WORKSPACE", "."))
    parser.add_argument("--today", default=dt.date.today().isoformat())
    parser.add_argument("--slug", help="Course slug for SRS lookup.")
    parser.add_argument("--active", action="store_true", help="Use active SRS slug when available.")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = Path(args.workspace).resolve()
    today = srs.parse_date(args.today)
    state = load_state(workspace)
    slug = active_srs_slug(workspace, state, args.slug, args.active)
    rows = load_srs_rows(workspace, slug)
    items = rank_recommendations(state, rows, today)
    if not items:
        raise SystemExit("No adaptive topics or SRS rows found. Run /diagnose, /quiz, /grade, or add adaptive topic state first.")
    if args.format == "json":
        emit_json(items, args.limit)
    else:
        emit_markdown(items, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
