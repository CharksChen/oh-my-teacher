# Oh My Teacher 中文定制版

面向中文高校期末复习场景的 AI 助教 Skill。它会把课件、笔记、往年题、作业和实验资料整理成复习计划，用自适应练习和模拟考试训练你，严格批改答案，沉淀错题本，并用间隔复习追踪薄弱点。

> 这是一个 **Skill**：核心行为由 `SKILL.md` 和 `references/` 里的 Markdown 指令定义，供支持 Skill 的大模型 Agent 读取。它不是一个常驻运行的应用程序。

## 适合谁用

- 期末前需要快速建立课程复习计划的大学生。
- 想把 PPT、PDF、课堂笔记、学习通/雨课堂资料、题库或往年题整理成考点的人。
- 需要有人严格批改答案、指出扣分点、追踪错题的人。
- 需要苏格拉底追问、费曼讲解、背诵卡片、口试模拟或机考/OJ 训练的人。
- 想在 Codex、Claude Code、ima、NotebookLM、Obsidian 或普通聊天框里复用同一套复习流程的人。

## 它能做什么

- **课程画像**：自动识别课程、考试形式、剩余时间、资料范围和薄弱点。
- **资料摄取**：整理 PDF、PPT、笔记、实验指导书、题库、作业和往年题。
- **重点提炼**：处理“老师划重点”“复习提纲”“高频考点”“最值得花时间的章节”。
- **复习计划**：生成 1/3/7/14/30 天计划、考点地图、考前一页纸和复习仪表盘。
- **主动练习**：自适应 `/quiz`、限时 `/mock`、口试 `/oral`、小组 `/group-quiz`。
- **严格批改**：按真实考试扣分逻辑指出错因、失分点、标准答案和补救练习。
- **错题闭环**：生成错题本、错误类型分布、SRS 到期复习和下一轮修复任务。
- **深度讲解**：支持苏格拉底引导、费曼复述、图示讲解和可运行代码演示。
- **闪卡导出**：把复习卡片导出为 Anki/Quizlet 友好的 CSV/TSV。

## 学术诚信 Academic Integrity

Oh My Teacher 是备考和训练工具，不是代考或代写工具。它会帮助你在考试前理解、练习、批改和复盘；不会帮助你完成正在进行的考试、必须独立提交的计分作业、课程论文或实验报告，也不会编造考试内容、实验数据、引用或日期。

## 目录结构

```text
oh-my-teacher/
├── SKILL.md                  # 入口：运行原则、命令路由、输出风格
├── README.md                 # 中文社区说明页
├── agents/                   # 多 Agent 适配元数据
│   ├── registry.json
│   ├── openai.yaml
│   ├── ima.yaml
│   ├── codex.yaml
│   └── ...
├── references/               # 按命令懒加载的详细工作流
│   ├── INDEX.md              # 命令到 reference 的唯一事实来源
│   ├── chinese-routing.md    # 中文自然语言触发词映射
│   ├── course-profiles.md    # 课程画像与快照
│   ├── materials-ingestion.md# 资料摄取
│   ├── question-types.md     # 出题和评分 rubric
│   ├── review-plans.md       # 复习计划、考点地图、冲刺
│   ├── practice-workflows.md # 模考、口试、修复、总结
│   ├── spaced-repetition.md  # 间隔复习状态
│   ├── wrong-note.md         # 错题本
│   ├── ima-adaptation.md     # ima 知识库/笔记/报告/PPT 适配
│   └── ...
├── examples/                 # 示例会话和示例产物
└── scripts/
    ├── export_flashcards.py  # Markdown 卡片 -> CSV/TSV
    ├── snapshot.py           # 课程快照保存/加载
    ├── srs.py                # 间隔复习状态管理
    ├── validate_skill.py     # 结构校验
    └── package_check.py      # 一键验证
```

## 常用命令

可以输入斜杠命令，也可以直接说中文需求，例如“帮我看这套往年题怎么复习”“还有三天考试救一下”“把这些 PPT 整理成计划”。

| 阶段 | 命令 |
|------|------|
| 建档与资料 | `/profile`, `/materials`, `/diagnose`, `/paper`, `/paper-analyze`, `/teacher-emphasis`, `/lab` |
| 计划 | `/plan`, `/map`, `/last-page`, `/dashboard` |
| 练习 | `/quiz`, `/mock`, `/oral`, `/group-quiz`, `/grade`, `/fix` |
| 讲解 | `/explain`, `/socratic`, `/feynman`, `/visual`, `/video`, `/code-demo` |
| 追踪与导出 | `/review-due`, `/wrong-note`, `/flashcards`, `/summary`, `/resume`, `/report`, `/ppt` |
| 模式 | `/mode`, `/cram`, `/help` |

默认复习闭环：

```text
/profile -> /materials -> /diagnose -> /plan -> /quiz | /socratic | /feynman -> /grade -> /fix -> /review-due -> /summary
```

## 中文场景适配

内置触发词覆盖常见中文复习说法：

- “老师说这些是重点”“老师划的重点”
- “帮我看往年题怎么复习”“分析这套卷子”
- “整理错题”“做个错题本”
- “今天该复习什么”
- “还有三天考试，救一下”
- “做考前速记”“生成复习 PPT”
- “把知识库资料变成计划”
- “闭卷怎么背”“机考怎么练”“实验考口试怎么准备”

中文自然语言路由由 `references/chinese-routing.md` 维护。

## 课程模板

内置常见课程模板，便于快速建档：

- `advanced-math`：高等数学
- `physics`：大学物理 / 普通物理
- `programming-c-cpp`：程序设计（C/C++）
- `digital-logic`：数字电路与逻辑设计
- `marxism-basic-principles`：马克思主义基本原理
- 另含数据结构、数学分析、线性代数、计算机网络、操作系统、大学物理等别名

## 闪卡导出

```bash
# 单文件导出
python scripts/export_flashcards.py cards.md cards.csv --deck "期末复习"

# 合并多个主题并去重
python scripts/export_flashcards.py limits.md integrals.md all.csv --dedup

# Quizlet 友好的 cloze 展开 / TSV 输出
python scripts/export_flashcards.py cards.md out.csv --expand-cloze
python scripts/export_flashcards.py cards.md out.tsv --format tsv
```

支持格式见 `examples/sample-cards.md`。

## 开发与校验

```bash
python scripts/package_check.py
python scripts/validate_skill.py --root .
python scripts/course_templates.py list
python scripts/export_flashcards.py examples/sample-cards.md cards.csv --dedup
```

一键运行结构校验和单元测试：

```bash
python scripts/package_check.py
```

单独运行：

```bash
python scripts/validate_skill.py
python -m unittest discover -s scripts/tests -v
```

贡献或改写时注意：

- **命令是契约**：新增或改名命令时，同时更新 `SKILL.md` 和 `references/INDEX.md`。
- **reference 懒加载**：详细流程放在 `references/`，不要把所有内容塞进 `SKILL.md`。
- **中文路由**：新增中文触发词优先放进 `references/chinese-routing.md`。
- **不要编造**：保留学术诚信约束，不虚构考题、实验数据、引用或老师要求。
- **示例同步**：命令行为变化时，同步更新 `examples/`。
