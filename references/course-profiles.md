# Course Profiles

重大复习任务前先建立课程画像。用户已经给出足够线索时，直接推断并简短说明假设，不要让用户填长表。

## Snapshot Template

跨轮维护紧凑 snapshot。重大任务开头展示或更新它（`/materials`, `/diagnose`, `/plan`, `/map`, `/mock`, `/grade`, `/fix`, `/quiz`, `/oral`, `/group-quiz`, `/summary`），除非当前会话里课程上下文已经很清楚。

```markdown
## Current Course Snapshot
- **Course**: [name + subject family]
- **Assessment**: [闭卷/开卷/半开卷/机考/OJ/实验考/口试/论文/答辩/混合]
- **Days left**: [N days or unknown]
- **Level**: [beginner / shaky / basic ok / high-score / pass-only]
- **Environment**: [agent-shell / rag-notebook / notes-app / plain-chat / unknown]
- **Materials**: [uploaded sources or gaps]
- **LaTeX**: [rendered / plain-text / not applicable]
- **Weak points**: [tag1, tag2]
- **Completed**: [topics already practiced or mastered this session]
- **Accuracy**: [recent performance, e.g. "7/10 on limits, 3/5 on series"]
- **Last action**: [last command or task]
- **Next recommended**: [one concrete next step]
```

Update rules:

- After `/materials`: refresh **Materials**, knowledge priorities, and **Next recommended**
- After `/diagnose`: write ranked weak-point results to **Weak points** and **Accuracy**, calibrate **Level**, set **Last action**, update **Next recommended**
- After `/grade`, `/mock`, `/quiz`, or `/fix`: append or refine **Weak points**, update **Completed** and **Accuracy**, set **Last action**, update **Next recommended**
- After `/oral`: same as `/quiz`; additionally note confidence and structure quality in **Accuracy**
- After `/group-quiz`: aggregate per-participant weak points; update active student's **Weak points** and **Accuracy**
- After `/summary`: consolidate session topics into **Completed**, refresh **Accuracy** summary, set **Last action** to `/summary`, update **Next recommended**
- After `/profile` or new course info: rebuild the full snapshot; set **Level** from user declaration (high-score / pass-only are goals, not performance metrics)
- After environment detection or a clear environment change: refresh **Environment** using `references/environment-adaptation.md`
- For mathematics courses, use the LaTeX auto-detection flow in `references/subject-adaptation.md`; do not ask an abstract rendering-preference question first
- Keep **Weak points** short: topic labels, not paragraphs

## Required Fields

- Course name and subject family
- Assessment format: paper exam, lab exam, coding/on-machine exam, oral exam, open-book, closed-book, course project, mixed assessment
- 中文考试形式同义词：闭卷、开卷、半开卷、一页纸、机考、OJ、实验考、操作考、口试、课程论文、大作业、答辩、平时分+期末混合
- Course nature: theoretical proof, computation/application, programming practice, lab operation, memorization/essay, case analysis
- User level: beginner, learned but shaky, can solve basic problems, high-score target, pass-only target
  - **Note**: `pass-only` and `high-score` are user-declared goals (set during `/profile`), not inferred from performance. They override performance-based level assignments.
- Constraints: exam date, daily available time, target score, materials available, past papers, teacher emphasis

中文 `/profile` 最多问三件事：

1. 这门课叫什么，考试形式是什么？例如闭卷、开卷、机考、实验考、口试。
2. 还有几天，每天大概能复习多久，目标是及格还是冲高分？
3. 现在最卡的是概念、证明、计算、代码、实验操作、背诵，还是没有资料头绪？

如果用户只回答一部分，先建立低置信画像并推进 `/diagnose` 或 `/materials`，不要反复追问。

## Paper Exam Optimization

Use when the assessment is written, closed-book/open-book, or likely traditional final exam.

笔试优先：

- 考试地图：章节、权重、可能题型。
- 定义、定理条件、公式、模板、标准步骤。
- 限时训练、模拟卷、答案 rubric。
- 最后 30 分钟的一页纸。
- 常见坑和得分机会。

开卷/半开卷强调资料索引、页码定位、题型模板和避免考试时翻资料耗时。半开卷/一页纸要优先压缩成“公式条件 + 模板 + 易错点”，不要堆完整讲义。

## Lab Exam Optimization

Use when the assessment involves experiments, operation, reports, practical demonstrations, or lab viva.

实验考优先：

- 实验原理，以及每一步控制什么变量。
- 仪器设置、操作顺序、安全/处理注意事项。
- 数据记录表、计算流程、不确定度/误差分析。
- 常见失败操作和补救。
- 实验报告结构和口试/答辩问题。

Subject-specific lab emphasis:

- Chemistry: reagents, reaction mechanism, color/phase observations, safety, contamination, yield/error.
- Biology/medicine: sample handling, staining/assay steps, controls, observation criteria, contamination, interpretation.
- Physics/electronics: circuit/setup diagram, calibration, measurement range, uncertainty, graph fitting, units.
- Computer labs: environment setup, input/output format, test cases, debugging checklist, edge cases.

## Coding or On-Machine Exam

机考/OJ 优先：

- 已学语言范围和允许库。
- 常见输入输出格式。
- 边界情况、时间复杂度、调试和测试构造。
- 大题解前先用小例子跑通。
- 评分点：算法思路、数据结构、正确性、复杂度。

## Oral Exam

口试/答辩优先：

- 能在 30-60 秒说清的定义和例子。
- 递进追问：基础、应用、边界、对比。
- 回答模板：定义 -> 条件 -> 例子 -> 常见坑。
- 用短回答反复练，修复表达和信心。

## Unknown Course

Ask at most these three questions:

1. 这是什么课，怎么考？
2. 还有多久，每天能复习多久，目标分/目标档位是什么？
3. 现在最难的是概念、证明、计算、代码、实验还是背诵？

## Snapshot On-Disk Format

In agent shells, prefer `scripts/snapshot.py` for deterministic save/load/list/set-active operations instead of hand-rolling snapshot paths. Use the Markdown snapshot format below as the content passed to the script.

The script also maintains `.oh-my-teacher/state.json` in agent shells. Treat the Markdown snapshot as the human-facing format and `state.json` as the machine-readable state for scripts and future automation.

When persisting the Current Course Snapshot to `.oh-my-teacher/snapshot.md` (agent shell) or as a copyable block (plain chat), use the exact Markdown format below. The LLM must parse and write this structure byte-for-byte — do not add extra headings, YAML front matter, or narrative text outside the fenced block.

```markdown
## Current Course Snapshot
- **Course**: 数据结构与算法 / Computer Science
- **Assessment**: 机考（闭卷，2小时，OJ自动评测）
- **Days left**: 7
- **Level**: shaky
- **Environment**: agent-shell
- **Materials**: 课件PPT（12章全）、实验报告x4、往年OJ题库x3套
- **LaTeX**: not applicable
- **Weak points**: [图论-Dijkstra堆优化, 动态规划-状态设计]
- **Completed**: [线性表, 栈与队列, 二叉树遍历]
- **Accuracy**: "排序 8/10, 图最短路 4/10, DP 2/5"
- **Last action**: /fix on Dijkstra with negative-weight confusion
- **Next recommended**: /quiz on DP state design
```

File naming convention for single-course mode:

- Write to `.oh-my-teacher/snapshot.md` in the workspace root.
- Preferred helper: `python scripts/snapshot.py save < snapshot.md` and `python scripts/snapshot.py load`.
- To inspect machine-readable state, use `python scripts/snapshot.py load --json`.
- On session start, read this file and confirm with the user before continuing.
- After `/profile`, `/materials`, `/diagnose`, `/plan`, `/grade`, `/mock`, `/quiz`, `/fix`, `/oral`, `/group-quiz`, or `/summary`, overwrite the file with the updated snapshot.

For multi-course mode (see Multi-Course Independent Snapshots below), use:

- `.oh-my-teacher/snapshots/<course-slug>.md` per course.
- Keep a `.oh-my-teacher/snapshots/_active` file containing only the slug of the active course.
- Preferred helper: `python scripts/snapshot.py save --course "Course Name" --active < snapshot.md`, `python scripts/snapshot.py load --active`, `python scripts/snapshot.py list`, and `python scripts/snapshot.py set-active --course "Course Name"`.
- Multi-course saves also update `.oh-my-teacher/state.json` with the active slug and parsed snapshot fields.

When reading back a snapshot, parse the bullet fields exactly as written. If a field is missing, leave it blank in the restored snapshot — do not guess.

## Multi-Course Independent Snapshots

When the user is juggling multiple courses, do not discard data from previous courses. Instead, maintain one snapshot file per course under `.oh-my-teacher/snapshots/`.

### Activation

- If `.oh-my-teacher/snapshots/` directory does not exist, create it on first multi-course switch.
- When the user switches to course X, read `.oh-my-teacher/snapshots/<slug>.md` if it exists; otherwise treat it as a new course and build the profile from scratch.
- Write `.oh-my-teacher/snapshots/_active` containing only the slug of the currently active course (no newline, no Markdown).
- The legacy single-file `.oh-my-teacher/snapshot.md` is still supported as the fallback when only one course is in play.

### Slug Convention

`scripts/snapshot.py` provides a `slugify()` helper. The rule is:

- Lowercase, strip non-word Unicode punctuation, replace whitespace/underscores with hyphens, collapse multiple hyphens.
- Unicode letters (including Chinese characters) are preserved — the function does **not** romanize.
- English names stay English; Chinese names stay Chinese (with punctuation stripped).

Examples:

| Course name | `slugify()` output |
|---|---|
| `Data Structures` | `data-structures` |
| `Linear Algebra` | `linear-algebra` |
| `数据结构与算法` | `数据结构与算法` |
| `数学分析` | `数学分析` |
| `操作系统（OS）` | `操作系统os` |

If the user provides an explicit slug via `--slug`, that value is used verbatim and bypasses `slugify()`.

### Snapshot File Content

Each `snapshots/<slug>.md` uses the same format as the single-file snapshot (see Snapshot On-Disk Format above). It is a self-contained record of one course.

### Switching Workflow

1. Detect the switch signal: new course name, new subject family, or user says "切换到XX".
2. Save the current course's snapshot to `snapshots/<old-slug>.md`.
3. Load (or create) `snapshots/<new-slug>.md`.
4. Update `_active` with the new slug.
5. Confirm the switch with the user: "已切换到 [课程名]，之前的 [旧课程] 进度已保存。"
6. Show the new course's snapshot and next recommended action.

### Multi-Course Overview Command

When the user asks for an overview of all tracked courses (e.g., "/plan multi" or "我有哪些课在复习"), scan all `snapshots/*.md` files, extract Course, Days left, Level, and Weak points from each, and present a ranked priority table as shown in the Multi-Course Plan example in `examples/sample-course-profile.md`.
