# References Index

执行任何命令前，先加载对应 reference。本文件是命令路由、命令说明和环境降级策略的唯一事实来源。

## Load Order

| Priority | File | Purpose | Load When |
|----------|------|---------|-----------|
| 1 | `course-profiles.md` | 课程画像、Current Course Snapshot、多课程切换和持久化格式 | `/profile`, `/materials`, `/diagnose`, `/plan`, `/map`, `/mock`, `/grade`, `/fix`, `/quiz`, `/oral`, `/group-quiz`, `/summary`, `/resume`, course switch |
| 2 | `environment-adaptation.md` | 判断宿主能力并选择降级方案 | 涉及文件、检索、shell/scripts、持久化、引用、图示、代码演示、导出或未知环境 |
| 3 | `materials-ingestion.md` | 摄取 PDF/PPT/笔记/往年题，提取知识清单、重点和缺口 | `/materials` 或用户上传课程资料 |
| 4 | `subject-adaptation.md` | 按学科调整严谨度、符号、例子、题型和图示 | 已建立课程画像后的任何复习任务 |
| 5 | `interaction-modes.md` | 选择苏格拉底、费曼、阅卷人、冲刺等教学模式 | 生成题目、讲解、反馈或切换模式前 |
| 6 | `learning-strategies.md` | 主动回忆、间隔复习、交错练习等学习策略 | `/plan`, `/quiz`, `/fix`, `/socratic`, `/feynman`, `/flashcards` 或选择学习方法时 |
| 7 | `ima-adaptation.md` | ima-native 工具、记忆、笔记、知识库、报告和 PPT 路由 | 环境是 ima，用户提到 ima/知识库/笔记，或工具含 ask_user/fetch/search/memory/use_skill |
| 8 | `chinese-routing.md` | 中文自然语言触发词到命令/工作流的映射 | 中文请求没有斜杠命令，或暗示中文知识库/笔记学习流 |
| 9 | `agent-adapter-contract.md` | 多 Agent 适配契约和能力标签 | 打包或在命名 Agent 运行 skill |
| 10 | `agent-optimization.md` | 按 Agent 能力选择最佳执行路径 | 运行、打包、验证或调试 Agent 适配 |
| 11 | `agent-inventory.md` | 各 Agent 能力清单和不确定项 | 添加、验证或调试 Agent 适配 |
| 12 | `staged-review-workflow.md` | 两阶段“资料到练习”流程和 Stage 1 核心复习包 | 用户要阶段式复习、核心材料或最值得学的章节 |
| 13 | `focus-feedback-iteration.md` | 聚焦 - 反馈 - 迭代闭环 | 多步骤复习、计划、练习、批改、修复、总结或阶段工作流 |
| 14 | `opt-in-reminders.md` | 明确 opt-in 的提醒和每日/每周知识归纳契约 | 用户明确要求启用、修改、停止或生成提醒/归纳卷 |

只有用户要求示例会话、输出样例、行为对比或回归参考时，才加载 `examples/`。

## Command Catalog and Reference Map

| Command | Description | Primary Reference | Secondary References |
|---------|-------------|-------------------|---------------------|
| `/help` | 按阶段列出命令、用途和中文例句 | This index | - |
| `/profile` | 建立课程画像，只问真正缺失的关键信息 | `course-profiles.md` | `course-templates.md`, `scripts/course_templates.py` |
| `/materials` | 摄取上传/粘贴的课件、笔记、题库、往年题，更新画像并列出缺口 | `materials-ingestion.md` | `course-profiles.md`, `environment-adaptation.md` |
| `/source-map` | 基于来源建立资料覆盖图、重点来源、缺口和引用锚点 | `ima-adaptation.md` | `materials-ingestion.md`, `review-plans.md` |
| `/paper` | 针对闭卷、开卷、半开卷等笔试优化复习 | `course-profiles.md` | `subject-adaptation.md` |
| `/paper-analyze` | 分析往年题、样卷、作业题和题库，反推高频考点 | `exam-paper-analysis.md` | `ima-adaptation.md`, `course-profiles.md` |
| `/teacher-emphasis` | 提取老师划重点、课堂强调、星标页、复习提纲和答疑信号 | `ima-adaptation.md` | `materials-ingestion.md`, `review-plans.md` |
| `/lab` | 针对实验考、实验报告、操作考和 viva/口试优化复习 | `course-profiles.md` | `subject-adaptation.md` |
| `/diagnose` | 用约 5 题快速定位跨章节薄弱点 | `question-types.md` | `course-profiles.md`, `practice-workflows.md` |
| `/plan` | 生成可执行的 1/3/7/14/30 天复习计划 | `review-plans.md` | `course-profiles.md`, `subject-adaptation.md` |
| `/map` | 输出知识图谱、考试地图、公式/定义和优先级 | `review-plans.md` | `course-profiles.md` |
| `/explain [topic]` | 讲清一个概念：定义、直觉、例题、陷阱、回忆题 | `subject-adaptation.md` | `interaction-modes.md` |
| `/socratic [topic]` | 苏格拉底式引导：一次一个问题，先提示再给答案 | `socratic-mode.md` | `interaction-modes.md`, `learning-strategies.md`, `subject-adaptation.md` |
| `/feynman [topic]` | 费曼复述检查：学生讲，AI 挑漏项、追问并批改 | `feynman-mode.md` | `interaction-modes.md`, `subject-adaptation.md` |
| `/quiz` | 自适应刷题，按表现升降难度 | `question-types.md` | `interaction-modes.md`, `subject-adaptation.md`, `course-profiles.md` |
| `/mock` | 生成限时模拟卷、答案和评分 rubric | `practice-workflows.md` | `question-types.md`, `course-profiles.md` |
| `/oral` | 模拟口试/答辩，逐问追问并给反馈 | `practice-workflows.md` | `interaction-modes.md`, `subject-adaptation.md` |
| `/grade` | 严格批改用户答案，定位扣分点和错因 | `question-types.md` | `course-profiles.md`, `practice-workflows.md`, `spaced-repetition.md` |
| `/fix` | 针对薄弱点给微课、变式题和修复练习 | `practice-workflows.md` | `question-types.md`, `subject-adaptation.md` |
| `/flashcards` | 生成主动回忆卡片；需要时用 `scripts/export_flashcards.py` 导出 CSV/TSV | `SKILL.md` | `practice-workflows.md`, `learning-strategies.md`, `environment-adaptation.md` |
| `/review-due` | 查看今天到期的间隔复习主题 | `spaced-repetition.md` | `course-profiles.md` |
| `/group-quiz` | 组织多人小组问答、抢答或轮流讲解 | `group-study.md` | `question-types.md`, `subject-adaptation.md` |
| `/visual` | 生成图示、流程图、概念图或图像 prompt | `visual-generation.md` | `subject-adaptation.md`, `environment-adaptation.md` |
| `/video` | 生成分镜、动画方案或视频 API 工作流 | `visual-generation.md` | `environment-adaptation.md` |
| `/code-demo` | 生成可运行代码演示、算法追踪或仿真 | `coding-demos.md` | `subject-adaptation.md`, `environment-adaptation.md` |
| `/cram` | 进入考前冲刺/抢分模式，优先高收益内容 | `review-plans.md` | `interaction-modes.md` |
| `/last-page` | 生成考前一页纸：公式、模板、陷阱、时间分配、交卷检查 | `review-plans.md` | `ima-adaptation.md`, `materials-ingestion.md` |
| `/dashboard` | 生成复习仪表盘：状态、热力图、到期主题、风险和下一步 | `review-plans.md` | `ima-adaptation.md`, `spaced-repetition.md`, `course-profiles.md` |
| `/resume` | 从粘贴的 Course Snapshot 恢复上下文 | `course-profiles.md` | - |
| `/summary` | 输出本轮复盘：练了什么、正确率变化、弱点、SRS 和下一步 | `practice-workflows.md` | `course-profiles.md`, `spaced-repetition.md` |
| `/wrong-note` | 从批改/刷题/模考反馈生成错题本并同步 SRS 摘要 | `wrong-note.md` | `question-types.md`, `spaced-repetition.md`, `ima-adaptation.md` |
| `/report` | 在可用时通过 ima-report 生成阶段复盘或覆盖率报告 | `ima-adaptation.md` | `exam-paper-analysis.md`, `review-plans.md` |
| `/ppt` | 在可用时通过 ima-ppt 生成考前冲刺或错题复盘 PPT | `ima-adaptation.md` | `review-plans.md`, `wrong-note.md` |
| `/mode [mode-name]` | 显式切换当前任务的互动模式 | `interaction-modes.md` | - |

用户显式命令只覆盖当前任务的自动模式选择。除非用户要求保持某个模式，完成当前任务后回到自动选择。

### `/help` Output Template

When the user runs `/help`, use this exact structure:

```markdown
# Oh My Teacher — 命令

你可以直接说中文需求，不必记命令。例如：“还有三天考试救一下”“帮我分析这套往年题”“按考试标准批改我的答案”。

## 建档与资料
| Command | Description |
|---------|-------------|
| /profile | 建立课程画像 |
| /materials | 整理课程文件、笔记和题库 |
| /source-map | 基于来源生成资料覆盖图 |
| /diagnose | 5 题快速诊断水平 |
| /paper | 针对闭卷/开卷笔试优化 |
| /paper-analyze | 分析往年题和出题规律 |
| /teacher-emphasis | 提取老师划重点 |
| /lab | 针对实验考优化 |

## 计划
| Command | Description |
|---------|-------------|
| /plan | 按天生成复习计划 |
| /map | 知识图谱和考试优先级 |
| /last-page | 考前一页纸 |
| /dashboard | 复习仪表盘 |

## 练习
| Command | Description |
|---------|-------------|
| /quiz | 自适应刷题 |
| /mock | 限时模拟卷 |
| /oral | 口试/答辩模拟 |
| /grade | 严格批改答案 |
| /fix | 修复薄弱点 |
| /group-quiz | 多人小组问答 |

## 讲解
| Command | Description |
|---------|-------------|
| /explain [topic] | 讲解一个概念 |
| /socratic [topic] | 苏格拉底式追问 |
| /feynman [topic] | 费曼复述检查 |
| /visual | 图示和可视化讲解 |
| /video | 分镜或动画方案 |
| /code-demo | 可运行代码演示 |

## 追踪与导出
| Command | Description |
|---------|-------------|
| /review-due | 今日到期间隔复习 |
| /wrong-note | 生成错题本 |
| /flashcards | 生成/导出闪卡 |
| /summary | 本轮学习复盘 |
| /resume | 从快照恢复上下文 |
| /report | 阶段复盘报告 |
| /ppt | 考前冲刺 PPT |

## 模式
| Command | Description |
|---------|-------------|
| /mode [name] | 切换互动模式 |
| /cram | 考前抢分模式 |

直接输入命令，或用中文描述你现在需要什么。
```

## Environment Fallbacks

For detailed fallbacks, load `environment-adaptation.md`. This compact table is the routing overview:

| Command | Agent shell | RAG notebook | Notes app | Plain chat |
|---------|-------------|--------------|-----------|------------|
| `/materials` | Read files; use PDF/PPT/text tooling when available | Cite from document context | Ingest Markdown notes, backlinks, tags, pasted excerpts | Ask student to paste chapter text or OCR screenshots |
| `/flashcards` | Write Markdown, then run `scripts/export_flashcards.py` | Emit Markdown cards inline | Emit Markdown cards with tags/backlinks | Emit Markdown cards inline |
| `/visual` | Mermaid, HTML, Manim, Python plot, or image prompt as appropriate | Mermaid or ASCII inline | Mermaid/Markdown tables if supported; otherwise ASCII | ASCII diagrams or numbered step lists |
| `/video` | Storyboard plus Manim/HTML Canvas plan or file when tools exist | Storyboard inline | Storyboard Markdown | Storyboard inline only; never call video API |
| `/code-demo` | Write and run a file; show output | Code block plus expected output | Code block plus trace note | Code block plus expected output and walkthrough |
| `/plan` | Write `plan.md` when useful | Plan inline | Markdown plan with tags/backlinks | Plan inline plus copy/pin reminder |
| `/map` | Mermaid or Markdown file when useful | Mermaid or ASCII inline | Mermaid/Markdown concept map | ASCII concept map |
| `/mock` | Write `mock.md` and `answer.md` when useful | Mock inline | Mock as Markdown note | Mock inline with rubric |
| `/grade` | Read answer file and write graded artifact when useful | Grade inline with quotes/citations | Grade inline with `#错题` tags | Grade inline with quotes |
| `/explain`, `/socratic`, `/feynman`, `/quiz`, `/oral`, `/fix`, `/group-quiz` | Conversational by default | Conversational by default | Markdown-native conversational output | Conversational by default |

## File Overview

One line per reference; load on demand per the Load Order and Command Catalog above.

| File | Contents |
|------|----------|
| `course-profiles.md` | Current Course Snapshot template, field rules, paper/lab/coding/oral optimization, multi-course snapshots, on-disk format |
| `environment-adaptation.md` | Host capability detection, capability-probe order, downgrade matrix, per-host output rules |
| `agent-adapter-contract.md` | Shared multi-agent adapter contract, capability tags, state/script policy, runtime prompt policy |
| `agent-optimization.md` | Agent launch protocol, optimization profiles, capability-to-behavior mapping, quality gates |
| `agent-inventory.md` | Agent capability inventory, source status, unknowns, and platform-specific notes |
| `staged-review-workflow.md` | Stage 1 core review pack, most-worth-studying chapter ranking, Stage 2 mock/weak-point repair workflow |
| `focus-feedback-iteration.md` | Focus, action, feedback, and iteration contract for active review loops |
| `opt-in-reminders.md` | Explicit opt-in reminders, proactive-message capability rules, daily/weekly knowledge digests, weak-point and memory-target summaries |
| `ima-adaptation.md` | ima-native protocol: 14 ima tools, 5 native skills, source levels, note-first persistence, KB retrieval, reports, PPT, command overrides |
| `chinese-routing.md` | Chinese natural-language trigger → command/workflow mapping |
| `materials-ingestion.md` | PDF/PPT/note/past-paper ingestion, extraction targets, output contract, incremental + multi-file merge, per-host ingestion |
| `subject-adaptation.md` | Per-subject rigor, notation, examples, visuals (Math, Physics, CS, Chem/Bio/Med, Econ/Law/History, Language, Design, Engineering, Clinical) |
| `interaction-modes.md` | Teaching-mode selection rules, mixed modes, response contracts, mode switching |
| `socratic-mode.md` | `/socratic` protocol: one question, hint ladder, assumptions, counterexamples, student summary, close |
| `feynman-mode.md` | `/feynman` protocol: teach-back, curious-freshman probing, grading, re-teach, repair card, SRS update |
| `learning-strategies.md` | Evidence-informed strategies: retrieval, spacing, interleaving, elaboration, self-explanation, examples, dual coding, pretesting, analogy, confidence calibration |
| `review-plans.md` | Study maps, review plans, cram mode (incl. anxiety handling), heat maps, last-page sheets, dashboard |
| `exam-paper-analysis.md` | Past-paper analysis: distribution, high-frequency topics, scoring patterns, evidence scope, ima note updates |
| `practice-workflows.md` | Active recall, mock exams (incl. pacing), error repair, oral rehearsal, session summaries |
| `spaced-repetition.md` | SRS files, topic naming/dedup, interval+ease algorithm, leech detection, difficulty ownership, `/review-due`, auto-updates |
| `wrong-note.md` | Wrong-question note template, error taxonomy, ima workflow, SRS sync |
| `group-study.md` | Group quiz setup, turn-based/buzzer sessions, scoreboards, peer explanation |
| `question-types.md` | Adaptive difficulty, generation defaults, confidence calibration, paper/programming/lab types, grading rubrics |
| `visual-generation.md` | Visual selection guide, env-aware matrix, ASCII conventions, image-prompt + video-storyboard workflow |
| `coding-demos.md` | Runnable demos: language inference, traces, data-structure state, simulations, debugging, beginner constraints, env-aware forms |
| `course-templates.md` | Pre-built course profiles for quick onboarding via `scripts/course_templates.py` |
| `review-workflows.md` | Compatibility redirect → review-plans / practice-workflows / spaced-repetition / group-study |
