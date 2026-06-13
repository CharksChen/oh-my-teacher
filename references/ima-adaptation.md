# ima Native Adaptation

宿主看起来像 ima 或暴露 ima-native 工具时使用本文件。在 ima 中不要把系统当普通 RAG 聊天框；知识库、笔记、记忆、计划和原生 skill 是主要运行时能力。

## Detection

Treat the environment as `ima-native` when any of these are true:

- Tools include `ask_user`, `fetch`, `search`, `memory_recall`, `memory_write`, `task_plan`, `subagent_spawn`, or `use_skill`.
- The user mentions ima, 知识库, 资料库, 笔记, 课程主页, 错题本, 往年题, 老师划重点, 复习仪表盘, or 考前速记 PPT.

Set the Current Course Snapshot `Environment` field to `ima / rag-notebook / note-native`.

中文社区默认：当用户说“知识库里的资料”“笔记里那门课”“生成 PPT/报告”“课程主页”“错题本”时，优先按 ima-native 处理，而不是只在聊天里回答。

## Source Levels

Every source-grounded output should label important claims as one of:

- `课程资料确认`: directly supported by fetched course files, notes, past papers, slides, or teacher messages.
- `ima 知识库检索`: retrieved through `search source=kb` but not fully fetched.
- `笔记历史`: retrieved from ima notes or memory.
- `通用课程推断`: inferred from common university syllabi or templates.
- `需要确认`: useful but uncertain; ask or mark as a gap.

输出考试重点、章节权重或老师强调时，必须给来源等级。不要把 `通用课程推断` 写成确定考点。

## Tool Rules

### `ask_user`

- Ask only for high-impact gaps: course name, exam date, knowledge-base scope, or whether to write/update notes.
- During `/profile`, ask at most three compact questions in one turn.
- During `/grade` and `/fix`, do not block on a missing full profile. Grade with low confidence and record missing context.
- 中文提问要短：`这门课叫什么？怎么考？还有几天？`。不要让用户填写复杂表格。

### `fetch`

- Use for complete content from a specific file, URL, media, or note.
- `/materials`, `/paper-analyze`, and `/teacher-emphasis` must prefer `fetch` when a concrete resource id is known.
- Always provide a focused `question`, such as "提取考试范围、老师强调、题型、章节覆盖".

### `file_edit`

- Use only for precise workspace file edits, such as modifying this skill.
- Do not use it as the primary way to edit ima notes; use `ima-note` through `use_skill` or emit ima-note-compatible Markdown.

### `file_read`

- Use for reading this skill's references, agent configs, and scripts.
- In learning workflows, course materials should come from `search` or `fetch`, not `file_read`.

### `file_write`

- Use for generated workspace files such as CSV, Markdown exports, or intermediate artifacts.
- If the user needs to download the file, follow with `provide_file`.

### `provide_file`

- Use for `/flashcards` CSV/TSV export, `/last-page` Markdown export, and `/paper-analyze` report export.
- Keep a copyable Markdown fallback in the response.

### `memory_recall`

- Before `/profile`, search prior user preferences, historical courses, and known review strategies.
- For `/review-due`, `/summary`, and `/dashboard`, recall prior study state.
- Default scope is `all`; use `user` for stable preferences and `memory` for course state.

### `memory_write`

- Save stable facts: user goal, course name, exam date, usual knowledge base, and output preferences.
- Do not store full transient wrong-question content in memory. Store wrong-question summaries in memory and full notes in ima-note.

### `match`

- Use for workspace search over this skill, generated files, or local templates.
- Do not use `match` instead of `search source=kb` for ima knowledge-base materials.

### `search`

- This is the central ima learning tool.
- `/materials` defaults to `search source=kb`.
- `/wrong-note` and `/review-due` default to `search source=note`.
- `/teacher-emphasis` searches both `source=kb` and `source=note`.
- Use `source=web` only for external facts, and label them as not course-material evidence.

### `shell`

- Run scripts only when shell is explicitly available and the script path exists.
- Allowed examples: `scripts/export_flashcards.py`, `scripts/snapshot.py`, `scripts/srs.py`, `scripts/validate_skill.py`.
- Never say a script ran unless shell returned success.
- In ima-native learning flows, prefer note-native Markdown fallback over shell.

### `subagent_spawn`

- Use `type=research` for large read-only scans in `/source-map`, `/paper-analyze`, or broad `/materials`.
- Use `type=general` only when the delegated task must write notes or files.
- The main agent must integrate subagent results; subagents do not produce the final answer directly.

### `task_plan`

- Create or update a plan for ima workflows longer than three steps.
- Required chains include `/materials -> /source-map -> /diagnose -> /plan` and `/mock -> /grade -> /wrong-note -> /review-due`.

### `use_skill`

- Use native ima skills instead of reimplementing their workflows:
  - `ima-knowledge`: knowledge-base location, folders, tags, file organization, permissions, kb_id.
  - `ima-note`: course homepage, wrong-question notes, SRS tables, weak-point boards, daily logs.
  - `ima-ppt`: exam-cram PPT or wrong-question PPT.
  - `ima-report`: stage review reports, coverage reports, paper-analysis reports.
  - `ima-skill-creator`: create or optimize skills; not used for ordinary studying.

## Native Skill Routing

| User intent | Native skill | Oh My Teacher action |
|---|---|---|
| 知识库, 资料库, 找课件, 整理课程资料 | `ima-knowledge` | Locate kb/files first, then `/materials` or `/source-map` |
| 笔记, 课程主页, 错题本, SRS, 每日复习日志 | `ima-note` | Create/update note-native Markdown artifacts |
| PPT, 演示文稿, 考前速记 PPT | `ima-ppt` | Use `/last-page` as source, then hand off to PPT generation |
| 报告, 阶段复盘, 覆盖报告, 往年题分析报告 | `ima-report` | Gather source-map/paper-analysis/dashboard, then report |
| 创建技能, 优化 skill, 自动化流程 | `ima-skill-creator` | Delegate skill creation/optimization |

## ima Command Overrides

| Command | ima-native behavior |
|---|---|
| `/profile` | Recall memory, search notes for existing course homepage, then create/update ima-note homepage |
| `/materials` | Use `ima-knowledge` if kb management is needed; otherwise `search source=kb`, `fetch`, then update 资料清单 / Materials Inventory |
| `/source-map` | `task_plan -> search source=kb -> fetch -> subagent_spawn research optional -> ima-note` |
| `/paper-analyze` | Fetch past papers, analyze patterns, write "based on uploaded papers only" caveat |
| `/teacher-emphasis` | Search kb and notes for teacher emphasis signals; update Exam Priority Map |
| `/grade` | Grade strictly and include Source Alignment against course materials when available |
| `/wrong-note` | Generate ima-note wrong-question note and memory summary |
| `/review-due` | Search note SRS tables first; use memory only as fallback |
| `/dashboard` | Combine memory, course homepage, SRS table, weak-point board, and recent notes |
| `/last-page` | Build from source-map, teacher emphasis, weak points, and high-yield formulas/templates |
| `/report` | Call `use_skill name=ima-report` with course homepage, source-map, paper-analysis, dashboard |
| `/ppt` | Call `use_skill name=ima-ppt` using `/last-page` or wrong-note cluster |

## Course Home Template

```markdown
# 课程主页：[课程名]期末复习

## Current Course Snapshot
- **Course**:
- **Assessment**:
- **Days left**:
- **Level**:
- **Environment**: ima / rag-notebook / note-native
- **Materials**:
- **Weak points**:
- **Completed**:
- **Accuracy**:
- **Last action**:
- **Next recommended**:

## 资料清单（Materials Inventory）
| 资料 | 覆盖内容 | 来源等级 | 缺口 |
|---|---|---|---|

## 考试优先级地图（Exam Priority Map）
| 知识点 | 优先级 | 常见题型 | 来源 |
|---|---|---|---|

## 薄弱点看板（Weak Point Board）
| 知识点 | 错因 | 最近得分 | 下次复习 | 修复动作 |
|---|---|---|---|---|

## 错题本（Wrong Questions）
- [[错题-YYYY-MM-DD-topic]]

## SRS Table
| Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |
|---|---|---:|---:|---|---|---:|---:|

## 接下来 3 个动作（Next 3 Actions）
1.
2.
3.
```

## 中文笔记命名约定

- 课程主页：`课程主页-[课程名]期末复习`
- 错题：`错题-YYYY-MM-DD-[课程名]-[topic]`
- 考前一页纸：`考前一页纸-[课程名]`
- 往年题分析：`往年题分析-[课程名]-[年份范围]`
- 阶段复盘：`阶段复盘-[课程名]-第N轮`

在 ima-note 可用时，优先更新已有课程主页，避免为同一门课创建多个分散笔记。若必须新建，先搜索同名/相似课程主页。

## Fallback

If ima tools are unavailable, output the same Markdown artifacts inline. Do not claim a note, memory, report, PPT, or script was created unless the corresponding tool actually succeeded.
