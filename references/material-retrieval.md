# Material Retrieval When Inputs Are Thin

Use this file when the user gives no course files, no syllabus, or only a thin
prompt such as "帮我复习高数", "这门课怎么复习", "没有资料先帮我整理", or a course
name plus very limited context.

Goal: retrieve or construct the best available evidence without pretending that
generic information is course-specific.

## Source Levels

Label every important claim with one of these levels:

- `课程资料确认`: directly supported by user-provided slides, notes, syllabus,
  past papers, teacher emphasis, or fetched course files.
- `知识库检索`: retrieved from the user's knowledge base or RAG context but not
  fully confirmed by a fetched full document.
- `笔记历史`: retrieved from the user's notes, course homepage, memory, or prior
  study state.
- `官方公开来源`: public university, course, department, textbook, or official
  exam source found through web/search tools.
- `通用课程推断`: inferred from common university syllabi, textbooks, or course
  templates.
- `需要确认`: useful candidate information that still needs syllabus, teacher,
  past-paper, or user confirmation.

Do not promote `通用课程推断` or `官方公开来源` to `课程资料确认` unless the source is
the user's actual course material.

## Retrieval Order

When material is missing or too thin:

1. Normalize the course name: Chinese name, English name if obvious, subject
   family, likely assessment type, and common abbreviations.
2. Detect search capabilities from `references/environment-adaptation.md`:
   `kb-search`, `note-search`, `workspace-search`, `rag-search`, `web-search`.
3. Search the user's own sources first:
   - ima / RAG: `search source=kb`, then `fetch` promising files.
   - notes: search course homepages, wrong-note boards, SRS tables, and tags.
   - agent shell: search local workspace filenames and text for course names,
     syllabus, PPT, PDF, past papers, notes, and teacher emphasis.
4. Search official/public sources only when user-owned sources are absent or
   thin, and label them as `官方公开来源`.
5. Use common syllabus knowledge only as a temporary scaffold and label it as
   `通用课程推断`.
6. Ask one compact question only after retrieval cannot resolve a high-impact
   gap, such as exam format, school/course variant, or whether the user has a
   syllabus/past paper.

## Query Generation

Generate precise query groups instead of one broad search:

| Query group | Purpose |
|---|---|
| Course identity | course Chinese/English name, abbreviation, subject family |
| Syllabus | `课程大纲`, `教学大纲`, `syllabus`, `教学日历`, `章节安排` |
| Exam scope | `考试范围`, `复习提纲`, `期末`, `闭卷`, `开卷`, `机考`, `实验考` |
| Past papers | `往年题`, `真题`, `样卷`, `题库`, `课后题`, `OJ`, `lab viva` |
| Teacher emphasis | `老师划重点`, `课堂强调`, `复习课`, `答疑`, `重点页` |
| Textbook map | textbook title, chapter names, common table of contents |

In agent shells, prefer `scripts/build_search_queries.py` to generate the query
set. The script does not search the web; the host search tool executes queries.

## Evidence Table

After retrieval, show a compact evidence table before producing a plan:

```markdown
## 检索证据表
| Source | Source level | Confirms | Still unknown | Next use |
|---|---|---|---|---|
| [file/link/note/search result] | [level] | [chapters/exam form/topics] | [gaps] | [/materials /diagnose /plan] |
```

If no useful source is found, say so directly and output:

- A low-confidence temporary course map.
- One diagnostic action.
- One smallest request for user-provided material.

## Output Rules

- Start with the highest-confidence evidence, not the longest generic syllabus.
- Keep public web claims separate from the user's actual course.
- If multiple sources conflict, report the conflict and ask for the smallest
  deciding signal.
- For plans and priority maps, mark unknown columns as `unknown` instead of
  inventing exam-scope weight, past-paper frequency, or teacher emphasis.
- When using web results, cite or link sources when the host supports it.
- When the host cannot search, output copyable query groups and a low-confidence
  scaffold; never claim retrieval happened.

## No-Source Fallback

If retrieval is unavailable or empty, use this sequence:

1. Build a temporary course profile from course name and likely subject family.
2. Mark `Materials` as `no external material; low-confidence scaffold`.
3. Give a 5-topic diagnostic or one P0 candidate drill.
4. Ask for exactly one high-value material next: syllabus, chapter list, past
   paper, teacher emphasis, or PPT table of contents.

## Chinese Examples

- "帮我复习高数" -> generate 高等数学 / Calculus query groups, look for syllabus
  and exam scope first, then diagnose limits/derivatives/integrals/series.
- "数据结构机考怎么复习" -> search for OJ/past problems/language constraints, then
  build a coding-focused diagnostic.
- "实验考但没资料" -> search lab manual, operation rubric, viva questions, safety
  notes; fallback to lab-assistant diagnostic.
