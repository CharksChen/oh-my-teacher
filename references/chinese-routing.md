# Chinese Natural-Language Routing

用户用中文自然语言表达需求时，先读本文件，不要先要求用户记斜杠命令。若说法能明确映射到命令，直接执行，并用一句话说明解释出的命令，例如：`我把你的需求理解为 /paper-analyze：分析往年题并反推复习重点。`

## 直接路由表

| 用户说法 | Route |
|---|---|
| 老师说这些是重点 | `/teacher-emphasis` |
| 这些是老师划的重点 | `/teacher-emphasis` |
| 老师画了重点 | `/teacher-emphasis` |
| 老师上课强调了这些 | `/teacher-emphasis` |
| 复习提纲里哪些最重要 | `/teacher-emphasis -> /plan` |
| 帮我看往年题怎么复习 | `/paper-analyze` |
| 分析这套卷子 | `/paper-analyze` |
| 看看这几年都考什么 | `/paper-analyze` |
| 根据往年题押重点 | `/paper-analyze -> /plan` |
| 根据题库出复习计划 | `/paper-analyze -> /plan` |
| 整理错题 | `/wrong-note` |
| 做个错题本 | `/wrong-note` |
| 把这题加入错题本 | `/wrong-note` |
| 我这题哪里错了 | `/grade` |
| 帮我批改答案 | `/grade` |
| 按考试标准扣分 | `/grade` |
| 给我出几道类似题 | `/fix` or `/quiz` |
| 出几道同类型变式 | `/fix` |
| 我想刷题 | `/quiz` |
| 随机抽查我 | `/quiz` |
| 这章我总是错 | `/fix` |
| 我没时间了先做什么 | `/cram -> /dashboard` |
| 帮我背这个 | `/quiz` with recitation-coach mode |
| 我已经会了，别提示我 | `/quiz` with `test` scaffold level |
| 模拟一套期末卷 | `/mock` |
| 来一次限时模拟 | `/mock` |
| 今天该复习什么 | `/review-due` or `/dashboard` |
| 今天先学哪一章 | `/dashboard -> /plan` |
| 给我一个复习仪表盘 | `/dashboard` |
| 把知识库资料变成计划 | `/materials -> /source-map -> /plan` |
| 把这些资料变成复习计划 | `/materials -> /source-map -> /plan` |
| 整理这些课件 | `/materials` |
| 帮我读一下 PPT | `/materials` |
| 帮我读一下 PDF | `/materials` |
| 根据笔记整理考点 | `/materials -> /map` |
| 做考前速记 | `/last-page` |
| 最后一页复习 | `/last-page` |
| 生成复习 PPT | `/last-page -> /ppt` |
| 做一个考前速记 PPT | `/last-page -> /ppt` |
| 做阶段复盘报告 | `/dashboard -> /report` |
| 我还有三天考试，救一下 | `/cram` |
| 明天考试，怎么抢分 | `/cram` |
| 挂科边缘，先复习什么 | `/cram -> /diagnose` |
| 帮我复习知识库里的这门课 | `/profile -> /materials -> /source-map` |
| 建一个课程主页 | `/profile` with ima-note |
| 帮我建课程档案 | `/profile` |
| 我不知道自己哪里不会 | `/diagnose` |
| 先测一下我的水平 | `/diagnose` |
| 这门课怎么复习 | `/profile -> /diagnose -> /plan` |
| 没资料怎么复习 | `/profile -> /materials` with material retrieval |
| 我只有课程名 | `/profile -> /materials` with material retrieval |
| 没有课件先帮我整理 | `/materials` with material retrieval |
| 先帮我查一下这门课资料 | `/materials` with material retrieval |
| 做个知识图谱 | `/map` |
| 梳理知识框架 | `/map` |
| 闭卷怎么背 | `/paper -> /plan` |
| 开卷怎么整理资料 | `/paper -> /last-page` |
| 半开卷带什么纸 | `/paper -> /last-page` |
| 机考怎么练 | `/profile -> /quiz` with coding or OJ focus |
| OJ 怎么刷 | `/quiz` with coding focus |
| 实验考怎么准备 | `/lab -> /plan` |
| 实验报告哪里容易扣分 | `/lab -> /grade` |
| 口试怎么准备 | `/oral` |
| 模拟老师问我 | `/oral` |
| 用苏格拉底方式问我 | `/socratic` |
| 别直接讲，问我问题 | `/socratic` |
| 用费曼法检查我 | `/feynman` |
| 我来讲你来挑错 | `/feynman` |
| 给我画图解释 | `/visual` |
| 做个流程图 | `/visual` |
| 写个代码演示 | `/code-demo` |
| 跑个例子给我看 | `/code-demo` |
| 生成 Anki 卡片 | `/flashcards` |
| 生成 Quizlet 表格 | `/flashcards` |
| 做背诵卡 | `/flashcards` |
| 下次提醒我复习 | `/review-due` plus opt-in reminder handling |
| 每天给我知识归纳 | `/review-due` plus opt-in digest handling |

## 路由规则

- 中文请求能明确映射时直接执行，不要让用户先选命令。
- 如果一句话包含多个动作，按“资料 -> 画像/地图 -> 计划 -> 练习 -> 批改 -> 修复 -> 复习追踪”的顺序拆成工作流，并先执行最有用的一步。
- 在 ima 中，用户提到 知识库、笔记、课程主页、错题本、老师划重点、往年题、报告、PPT 时，优先使用 note/knowledge-base 工作流。
- 如果短语暗示多步骤任务，在 ima 中创建 `task_plan`，然后执行第一个能产生学习价值的步骤。
- 置信度低于 0.7 时，只问一个紧凑问题，例如：`你更想先整理资料，还是直接做诊断题？`
- 用户处于明显考前高压场景（明天考试、三天冲刺、挂科边缘）时，默认 `/cram`，但保留最小诊断和错题修复，不只给安慰或大纲。
- 用户要求主动提醒或每日/每周知识归纳时，必须走 `references/opt-in-reminders.md`；不要默认开启后台提醒。
- 用户没有外部资料或只给课程名时，必须走 `references/material-retrieval.md`，先检索或生成可复制查询词，再输出低置信复习框架。
