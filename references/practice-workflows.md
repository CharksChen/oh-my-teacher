# Practice Workflows

用于主动回忆、`/mock`、`/oral`、`/fix`、`/summary` 和练习修复闭环。学习策略选择见 `references/learning-strategies.md`；保持“聚焦 - 反馈 - 迭代”见 `references/focus-feedback-iteration.md`。

## Active Recall

能出题时先出题，再总结。中文用户备考时，默认不要先给长篇知识点摘要。

可用形式：

- 闪卡：正反面、cloze、公式、定义、对比。见 `SKILL.md` Flashcard Export 和 `scripts/export_flashcards.py`。
- 简答抽查。
- 流程步骤填空。
- 证明骨架补全。
- 代码输出预测。
- 实验操作清单回忆。
- 中文背诵课：名词解释、辨析题、论述提纲补全、关键词默写。

每轮主动回忆后，更新相关 SRS 行（见 `references/spaced-repetition.md`），让掌握主题延后复习，薄弱主题更快回炉。

每轮主动回忆必须说明当前 focus topic，收集可见答案信号，并以一个迭代动作结束：repair、repeat、interleave、escalate、de-prioritize 或 schedule。

每个概念分三层：

1. Memory：定义/公式/事实。
2. Understanding：解释原因、条件或对比。
3. Exam application：解题、证明、计算、调试或分析。

当学生已掌握基础时，混入相近主题，不要重复刷同一种套路。使用 `references/learning-strategies.md` 的 interleaving 迫使学生识别方法。

中文 `/quiz` 输出默认：

```markdown
当前重点: [topic]
难度: [基础/变式/综合]
预计用时: [minutes]

题目:
[question]

请先作答。需要提示就说“提示1”。
```

批改后按 `references/question-types.md` 的中文评分结构输出，并给下一题难度调整。

## Mock Exam

生成模考时必须说明：

- 总分和时间。
- 题型分布。
- 是否闭卷/开卷/半开卷/可用资料假设。
- 难度分布。
- 答案和评分 rubric。
- 每题/每部分时间分配建议。

中文 `/mock` 模板：

```markdown
# 模拟卷
- 总分:
- 时间:
- 考试形式假设:
- 做题顺序建议:

## 题目
[按题型和分值列出]

## 答题要求
[是否先隐藏答案；如何提交答案；是否记录用时]
```

After the user answers, grade with `question-types.md` rules.

### Pacing and Time Management

模考也是时间分配训练。很多学生不是不会，而是难题耗时过长导致后面丢分。必须显式训练 pacing：

- 先给每题/每部分时间预算，总和等于考试时间，基本按分值比例分配。
- 可行时要求用户记录每题实际用时，或标出超时题。
- 模考复盘中，时间问题和知识错误并列指出：

```markdown
## 节奏复盘
| 题 | 分值 | 预算 | 实际 | 判断 |
|---|---|---|---|---|
| 大题3 | 15 | 18min | 32min | 超时，应在 20min 时战略性跳过 |
```

- 教 triage 规则：先做单位时间得分高的题；每题设硬上限；卡住就标记返回，不要硬耗。
- 机考/OJ 的 pacing 是做题顺序，不是部分分。

## Error Repair

批改或复盘错误时：

1. 找到最小错误知识点。
2. 分类错误：概念、条件、公式、计算、证明缺口、代码边界、实验操作、表达。
3. 给一个微课，不要重讲整章。
4. 如果错误涉及证明、推导、代码追踪或实验操作，要求学生用一句话解释改正后的关键步骤。
5. 生成三类修复：基础题、变式题、综合/混合题。
6. 如果错在“选错方法”，增加一道方法识别题。
7. 更新下一步复习建议。
8. 更新该主题 SRS 行（见 `references/spaced-repetition.md`）；Agent shell 中优先用 `scripts/srs.py update`。

中文 `/fix` 输出模板：

```markdown
## 错因定位
## 3 分钟微课
## 你来复述
## 修复练习
1. 基础:
2. 变式:
3. 综合:
## 下一轮
## 本轮闭环
```

错题修复必须以 `references/focus-feedback-iteration.md` 的 `本轮闭环` 结束：focus = 精确薄弱点，feedback = 答案证据，next round = 一个定向动作。

## Oral Exam Rehearsal

用于 `/oral`、口试、实验 viva、答辩和面试式考核。一次只问一个问题，等用户回答，批改后再决定加深或修复。

开场设置：

- 确认科目、预计时长和已知评分标准。
- 每个主题建立 6-12 个问题阶梯。
- 除非确认支持音频，默认文字口试。

深度阶梯：

1. Definition, about 30 seconds.
2. Condition/scope, about 45 seconds.
3. Example and counterexample, about 45 seconds.
4. Application, about 90 seconds.
5. Edge case, about 60 seconds.
6. Comparison, about 60 seconds.
7. Defense against a common misconception, about 60 seconds.

Stop climbing as soon as the user gets stuck. Repair the gap before continuing.

按准确性、简洁度、结构、信心和课程术语批改每个回答。

教可复用短答模板：

- 定义 -> 关键条件 -> 例子 -> 常见坑。
- 若条件成立 -> 结论；反例说明限制。
- 概念 A vs 概念 B 主要差在某个维度。

中文 `/oral` 默认开场：

```markdown
我会按口试方式一次问一个问题。你回答后，我会给分、指出缺口，再决定追问还是修复。
第 1 题（30 秒）：[question]
```

### Voice and Immersion (Agent Shell)

When the host environment supports audio or TTS tools:

- Generate the examiner's question as audio (TTS) so the student hears the question rather than reading it, simulating real oral-exam pressure.
- If speech-to-text is available, accept the student's spoken answer and transcribe it for grading.
- Always provide a text fallback alongside audio so the student can review what was asked and answered.

In plain chat or RAG notebook, skip audio and use text only.

## Summary

`/summary` 输出：

- 本轮练过的主题。
- 正确率/表现变化。
- 更新后的薄弱点。
- SRS 更新（如可用）。
- 一个具体下一步。
- focus-feedback-iteration 状态：当前优先重点、最强反馈证据、下一轮目标。

中文模板：

```markdown
## 本轮复盘
- 练习内容:
- 表现变化:
- 新增/修正薄弱点:
- SRS:

## 下一步
[一个马上执行的动作]

## 本轮闭环
重点:
反馈:
下一轮:
```

保持足够短，能直接粘到学习日志或课程主页。
