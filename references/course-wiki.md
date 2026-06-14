# Course Wiki（课程知识库 / LLM Wiki）

`/wiki`、`/wiki-ask`、`/wiki-lint` 的 primary reference。课程 wiki 是一个**持久、互相链接、由模型维护的 Markdown 知识库**，随着用户不断加入资料而累积，取代“每次提问都重新通读全部原始资料”的 RAG 方式。把它当作这门课的知识代码库：用户加来源，你写并维护页面，复习命令从页面读、再把新发现写回页面。

灵感来自 Andrej Karpathy 的 LLM Wiki（idea file）：不可变原始源 + 模型维护的 wiki + schema 文档，三个操作驱动一切——Ingest（摄取）、Query（查询）、Lint（体检）。

要把 wiki 工作转成“聚焦 - 反馈 - 迭代”状态时，读 `references/focus-feedback-iteration.md`。资料太少或没有外部资料时，先读 `references/material-retrieval.md`，**绝不**把通用大纲伪造成已确认考点写进 wiki。

## Three Components（三组件）

1. **Immutable raw sources（不可变原始源）** — 用户上传/粘贴的 PPT、PDF、笔记、往年题、老师划重点截图。捕获后**只进不改**，作为引用锚点。Agent shell 存于课程目录下的 `sources/` 子目录（见下方磁盘结构）。
2. **LLM-maintained wiki（模型维护的页面）** — 你写并持续修订的互联 Markdown 页面，存于课程目录下的 `pages/` 子目录。
3. **Schema 文档** — 本技能（SKILL.md + 本文件）定义结构与流程；每门课的 `INDEX.md` 是这门课的 Map of Content（MOC）。

页面间用 `[[页面 slug]]` 维基链接互连，兼容 Obsidian 图谱和 ima 笔记反链。

## On-Disk Layout（磁盘结构）

Agent shell 中优先用 `scripts/wiki.py` 维护，不要手写路径或链接索引：

```text
.oh-my-teacher/wiki/<slug>/
    INDEX.md     # 课程主页 / MOC
    sources/     # 不可变原始源
    pages/       # wiki 页面（*.md，[[..]] 互链）
```

```bash
python scripts/wiki.py init --course "数学分析"        # 建立目录与 INDEX 脚手架
python scripts/wiki.py add-source lecture03.pdf --slug 数学分析  # 捕获原始来源（不可变）
python scripts/wiki.py new-page --slug 数学分析 --title "极限的 epsilon-delta 定义" --type concept --priority P0 --sources "sources/lecture03.pdf" --tags "数学分析,极限"  # 创建页面脚手架
python scripts/wiki.py list --slug 数学分析            # 列出 INDEX 与页面
python scripts/wiki.py lint --slug 数学分析 --json     # 结构体检（孤页、断链、缺来源）
```

页面文件名用主题 slug（与 `[[链接]]` 的 slug 一致）。slug 规则与 `scripts/snapshot.py` 相同。

## Page Taxonomy（页面类型）

| 类型 | 内容 | 典型来源 |
|------|------|----------|
| 概念页（Concept） | 定义、直觉、典型例子、陷阱、回忆题 | `/materials`, `/explain` |
| 定理/公式页（Theorem/Formula） | 条件、适用前提、证明骨架、变形、易错点 | 课件、教材 |
| 考点页（Exam Point） | 高频考法、答题模板、评分要点、往年出现年份 | `/paper-analyze`, `/teacher-emphasis` |
| 章节 MOC 页（Chapter） | 本章页面索引、优先级（P0/P1/P2）、缺口 | 章节结构 |
| 错题页（Wrong Point） | 错因分类、正确版本、修复练习、SRS 链接 | `/wrong-note`, `/grade` |
| 课程主页（INDEX/MOC） | 全课入口、章节链接、待办缺口 | `init` |

## Page Template（页面模板）

每个页面以 YAML frontmatter 开头，正文用 `[[链接]]` 互连，并标注来源等级（与 `references/ima-adaptation.md` 的 Source Levels 一致）：

```markdown
---
title: 极限的 epsilon-delta 定义
type: concept
tags: [数学分析, 极限]
priority: P0
sources: [sources/lecture-03.md]
srs: 极限-epsilon-delta
---

# 极限的 epsilon-delta 定义

**定义**：对任意 epsilon > 0，存在 delta > 0，使得 0 < |x - a| < delta 时 |f(x) - L| < epsilon。

**来源**：课程资料确认（lecture-03，第 12 页）。

**直觉 / 陷阱 / 例题**：……

**相关**：[[连续性]]、[[函数极限的运算法则]]
**考法**：见 [[极限-考点]]
```

lint 要求每个页面**有 frontmatter** 且**含来源标注**（`来源` 或 `sources:`），并被至少一个其他页面或 INDEX 链接（无入链 = 孤页）。

## Operation 1 — Ingest（摄取，`/wiki`）

把新来源融入知识库。一份来源通常触及约 10 个页面。

1. 若没有课程画像，先读 `references/course-profiles.md`；若没有 wiki，`python scripts/wiki.py init`。
2. 按 `references/materials-ingestion.md` 抽取定义、定理条件、考法、老师强调、缺口。**不要**在这里重新发明抽取流程。
3. 用 `python scripts/wiki.py add-source <file>` 把原始内容存入 `sources/`，保持不可变。
4. 与用户快速对一遍 takeaways，再决定写哪些页面。
5. 用 `python scripts/wiki.py new-page` 建好 frontmatter 脚手架，再填写正文。为已存在主题**修订**页面（增量合并，不堆叠重复，见 materials-ingestion 的 Incremental Ingestion）。
6. 更新章节 MOC 与 `INDEX.md`：加入新页面链接，补全缺口列表。
7. 交叉链接：把新页面与相关旧页面用 `[[..]]` 双向连上。
8. 按 `references/staged-review-workflow.md` 标注 P0/P1/P2（考试范围权重、往年题频率、老师强调强度）。
9. 运行 `python scripts/wiki.py lint` 收尾，修复新引入的孤页或断链。

只摄取、不自动出整套模拟卷。摄取后回显紧凑改动摘要（新增/修订了哪些页面），让用户确认。

## Operation 2 — Query（查询，`/wiki-ask`）

回答问题时**先查 wiki 页面**，而不是重读全部原始资料：

1. 在 `pages/` 与 `INDEX.md` 中检索相关页面（Agent shell 用 grep/`wiki.py list`；ima 用 `search source=kb`；Obsidian 用反链/标签）。
2. 综合答案，引用具体页面 `[[页面]]` 与原始来源（sources/ 文件、页码）。标注来源等级；命中不足时说明，不要编造。
3. 若答案产生了有价值的新结论（一个被澄清的陷阱、一个推导、一条考法），**回填**为新页面或补进已有页面，并接上链接——知识库因此累积。
4. wiki 没有覆盖该问题时，明确说“知识库未覆盖”，给出补摄取建议（`/wiki` 加来源）或走 `references/material-retrieval.md`。

## Operation 3 — Lint（体检，`/wiki-lint`）

周期性健康检查，保持知识库可信、可导航。机械部分由脚本保证：

```bash
python scripts/wiki.py lint --slug <slug> --json
```

脚本检测：**孤页**（无入链）、**断链**（`[[目标]]` 指向不存在的页面）、**缺 frontmatter**、**缺来源标注**。在脚本结果之上，你再做语义体检：

- **矛盾（Contradictions）**：不同页面对同一定义/公式/范围说法冲突——报告冲突而非擅自合并。
- **陈旧（Stale）**：新来源已推翻旧页面结论时，修订并注明变化。
- **覆盖缺口（Coverage gaps）**：对照考试范围与 `/paper-analyze` 高频考点，列出尚无页面的 P0/P1 主题。
- **修复**：补链孤页、修正断链、为缺来源页面补引用或降级标注为 `需要确认`。

输出一份体检报告 + 一个排好序的修复清单（先 P0 缺口与矛盾）。

## Integration（与其他命令的集成）

- `/materials`：摄取后可直接进入 `/wiki` Ingest，把抽取结果落成页面。
- `/map`：从 wiki 的章节 MOC / `INDEX.md` 渲染知识图谱，而不是从零重建。
- `/explain [topic]`：先读对应 wiki 页面，按页面风格讲解，再把澄清的陷阱/例题回填页面。
- `/wrong-note`：每个错题成为一个错题页，从相关概念页 `[[..]]` 链接，并接上 SRS（`references/spaced-repetition.md`）。
- `/review-due`、`/dashboard`：用页面 frontmatter 的 `srs` 字段和 lint 的覆盖缺口作为复习与风险信号。

## By Environment（按环境）

先读 `references/environment-adaptation.md` 判定能力，再选形态：

- **Agent shell**：真实文件 + `scripts/wiki.py`（init/list/lint）。`sources/` 存原件，`pages/` 写页面，grep 检索。
- **ima-native**：读 `references/ima-adaptation.md`。用 `search source=kb` 检索，`fetch` 读原件；通过 `use_skill name=ima-knowledge` / `ima-note` 把页面写成知识库条目与笔记，用反链当 `[[链接]]`。
- **Notes app（Obsidian）**：Markdown 原生最契合 LLM Wiki——直接用 `[[页面]]`、`#标签`、图谱视图。把 `sources/` 与 `pages/` 建成两个文件夹。
- **RAG notebook**：无法可靠写文件时，把 wiki 页面作为内联合成笔记输出，并请用户保存；引用文档上下文。
- **Plain chat**：没有文件系统。输出一个可复制的单页知识摘要（带 `[[..]]` 占位），让用户粘进自己的笔记；逐主题累积，不假装已持久化。

## Academic Integrity（学术诚信）

wiki 只记录有来源支撑或可推导的内容。推断内容标 `通用课程推断` 或 `需要确认`，绝不写成已确认考点。不要编造考题、实验数据、引用、页码或老师要求。

## 本轮闭环

每次 `/wiki`、`/wiki-ask`、`/wiki-lint` 输出末尾给出：

- 重点：本轮触及/新建的最高优先级页面或考点。
- 反馈：来源证据、lint 发现的孤页/断链/缺口或矛盾。
- 下一轮：一个具体动作——补摄取一份来源、修复某个缺口页、把某错题接入概念页，或 `/quiz` 对应 P0 主题。
