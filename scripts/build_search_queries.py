#!/usr/bin/env python3
"""Build precise search query groups for missing course materials.

This helper never performs network access. It only produces query strings for
the current host's KB, note, workspace, RAG, or web search tool.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass


COURSE_ALIASES = {
    "高数": ["高等数学", "Calculus"],
    "高等数学": ["高数", "Calculus"],
    "线代": ["线性代数", "Linear Algebra"],
    "线性代数": ["线代", "Linear Algebra"],
    "数据结构": ["Data Structures", "数据结构与算法"],
    "数据结构与算法": ["数据结构", "Data Structures and Algorithms"],
    "操作系统": ["Operating Systems", "OS"],
    "计组": ["计算机组成原理", "Computer Organization"],
    "计算机组成原理": ["计组", "Computer Organization"],
    "概率论": ["概率论与数理统计", "Probability and Statistics"],
    "概率论与数理统计": ["概率论", "Probability and Statistics"],
    "大学物理": ["Physics", "General Physics"],
    "离散数学": ["Discrete Mathematics"],
}

ASSESSMENT_TERMS = {
    "paper": ["期末", "考试范围", "复习提纲", "闭卷", "开卷", "样卷"],
    "closed-book": ["闭卷", "考试范围", "复习提纲", "必背", "期末"],
    "open-book": ["开卷", "资料整理", "索引", "一页纸", "期末"],
    "oj": ["OJ", "机考", "题库", "输入输出", "边界数据", "past problems"],
    "coding": ["机考", "OJ", "programming exam", "past problems", "题库"],
    "lab": ["实验考", "实验指导书", "操作考", "viva", "实验报告", "安全注意事项"],
    "oral": ["口试", "答辩", "viva", "oral exam", "追问"],
}


@dataclass(frozen=True)
class QueryGroup:
    name: str
    purpose: str
    queries: list[str]


def dedup(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = " ".join(value.split())
        if normalized and normalized.lower() not in seen:
            seen.add(normalized.lower())
            result.append(normalized)
    return result


def has_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def course_terms(course: str) -> list[str]:
    terms = [course.strip()]
    terms.extend(COURSE_ALIASES.get(course.strip(), []))
    if not has_cjk(course) and " " in course:
        terms.append(course.replace(" ", ""))
    return dedup(terms)


def build_queries(course: str, school: str | None = None, assessment: str | None = None) -> list[QueryGroup]:
    terms = course_terms(course)
    scope = [school.strip()] if school else []
    assessment_key = (assessment or "paper").strip().lower()
    assessment_words = ASSESSMENT_TERMS.get(assessment_key, ASSESSMENT_TERMS["paper"])

    def scoped(*parts: str) -> str:
        return " ".join(scope + [part for part in parts if part])

    primary = terms[0]
    syllabus_queries = []
    exam_queries = []
    paper_queries = []
    teacher_queries = []
    textbook_queries = []

    for term in terms:
        syllabus_queries.extend([
            scoped(term, "课程大纲"),
            scoped(term, "教学大纲"),
            scoped(term, "syllabus"),
            scoped(term, "章节安排"),
        ])
        exam_queries.extend(scoped(term, word) for word in assessment_words)
        paper_queries.extend([
            scoped(term, "往年题"),
            scoped(term, "真题"),
            scoped(term, "样卷"),
            scoped(term, "题库"),
            scoped(term, "past exam"),
        ])
        teacher_queries.extend([
            scoped(term, "老师划重点"),
            scoped(term, "复习课"),
            scoped(term, "课堂强调"),
            scoped(term, "答疑"),
        ])
        textbook_queries.extend([
            scoped(term, "教材 目录"),
            scoped(term, "table of contents"),
            scoped(term, "课后题"),
        ])

    return [
        QueryGroup("course_identity", "Confirm the exact course variant and common names.", dedup([primary] + terms)),
        QueryGroup("syllabus", "Find chapter order, official outline, and teaching calendar.", dedup(syllabus_queries)),
        QueryGroup("exam_scope", "Find assessment format, scope, and final-review hints.", dedup(exam_queries)),
        QueryGroup("past_papers", "Find past papers, sample papers, problem banks, or OJ sets.", dedup(paper_queries)),
        QueryGroup("teacher_emphasis", "Find teacher-emphasis signals and review-session notes.", dedup(teacher_queries)),
        QueryGroup("textbook_map", "Map common textbook chapters and exercises when course sources are thin.", dedup(textbook_queries)),
    ]


def emit_markdown(groups: list[QueryGroup]) -> None:
    print("## Search Query Groups")
    for group in groups:
        print(f"\n### {group.name}")
        print(group.purpose)
        for query in group.queries:
            print(f"- {query}")


def emit_json(groups: list[QueryGroup]) -> None:
    print(json.dumps([
        {"group": group.name, "purpose": group.purpose, "queries": group.queries}
        for group in groups
    ], ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build search query groups for missing course materials.")
    parser.add_argument("course", help="Course name, e.g. 高等数学 or Data Structures.")
    parser.add_argument("--school", help="School, department, or teacher scope.")
    parser.add_argument("--assessment", help="paper, closed-book, open-book, oj, coding, lab, or oral.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    groups = build_queries(args.course, school=args.school, assessment=args.assessment)
    if args.format == "json":
        emit_json(groups)
    else:
        emit_markdown(groups)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
