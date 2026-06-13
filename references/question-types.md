# Question Types and Grading

用于出题、诊断、刷题和严格批改。模考和错题修复见 `references/practice-workflows.md`，复习计划和知识图谱见 `references/review-plans.md`，学科题型适配见 `references/subject-adaptation.md`，主动回忆、预检、交错练习和解释性提问见 `references/learning-strategies.md`。

## Adaptive Difficulty

根据用户本轮表现动态调整难度：

- **Step up**：同一主题连续答对 2-3 题时，升到下一层（基础 -> 变式 -> 综合/混合）。
- **Step down**：上一题做错时，降一层并隔离缺失前置知识，再重试。
- **Hold**：表现混合时保持当前层级，换一个角度问。

State the adjustment briefly when it happens:

> "难度上调：你连续答对了 3 道基础题，接下来试一道综合题。"
> "难度回调：这道题做错了，我们先回到基础概念再试一次。"

生成题组时，除非用户要求综合复习或模考，避开 Current Course Snapshot 中 **Completed** 已掌握主题。

## `/diagnose` vs `/quiz`

These two commands both ask questions but serve opposite goals; do not conflate them.

| | `/diagnose` | `/quiz` |
|---|-------------|---------|
| **Goal** | Map *where* the user is weak across the whole course | Drill and improve *one* topic in depth |
| **Coverage** | Broad: one question per top chapter (≈5 total) | Narrow: many questions on a single topic |
| **Difficulty** | **Fixed** at a baseline tier — do NOT step up/down mid-diagnostic; consistent difficulty keeps results comparable across topics | **Adaptive** — apply the step up/down/hold rules above |
| **Output** | A weak-point report ranked by performance; write results to the snapshot's **Weak points**, **Accuracy**, and calibrate **Level** | Per-question grade plus a difficulty trajectory; update **Accuracy** and **Completed** |
| **When** | Early, before `/plan` or `/map`, when the user's level is unknown | Anytime the user wants to practice a known weak area |

After `/diagnose`, recommend `/quiz` (or `/fix`) on the lowest-scoring chapter. The diagnostic calibrates the map; the quiz works the territory.

Treat `/diagnose` as pretesting when the student has not reviewed yet: keep it low-stakes, explain that misses guide attention, and avoid interpreting a miss as failure.

## Generation Defaults

Always align questions with course profile, subject adaptation, and user level.

For each question set, include:

- Topic
- Difficulty
- Estimated time
- Answer
- Explanation or rubric
- Common mistake

For adaptive `/quiz`, include a method-recognition or interleaved question once the student answers 2-3 basic questions correctly. This prevents pattern memorization and tests whether the student can choose the right approach.

### Confidence Calibration (optional)

For `/quiz`, `/diagnose`, and high-stakes `/grade`, optionally ask the student to predict confidence (1-5) before submitting, then compare it to the actual score. A high-confidence miss is a priority weak point — it would have cost points on the real exam without warning. See `references/learning-strategies.md` → Confidence Calibration. When used, add one line to the grading output:

```markdown
## Calibration
信心 [n]/5 vs 实际 [earned]/[max] — [well-calibrated | overconfident ⚠ | underconfident]
```

## Paper Exam Types

- Multiple choice / 选择题：干扰项要来自真实误区，不能随便编。
- Fill in the blank / 填空题：考定义、条件、公式、语法、流程步骤。
- Short answer / 简答题：要求概念解释、适用条件和例子。
- Calculation / 计算题：列已知、目标、公式选择、步骤、单位/检验。
- Proof / 证明题：要求定理条件、证明结构和每个关键推理。
- Essay/case / 论述或案例题：给提纲、关键词、证据和评分 rubric。

中文高校常见补充：

- 名词解释：定义 -> 关键词 -> 适用范围 -> 易混概念。
- 判断题/辨析题：先判正误，再指出关键词错在哪里。
- 材料分析题：概念定位 -> 材料证据 -> 原理分析 -> 结论。
- 计算/证明大题：按步骤给分，必须标出“这里会扣几分”。

## Programming Types

- Predict output
- Trace state changes
- Find bug
- Complete code
- Implement function
- Analyze complexity
- Design tests

Keep code within the known course level. If unknown, start with basic language constructs and ask for learned scope when needed.

机考/OJ 题默认包含：输入输出格式、样例、边界数据、复杂度目标、常见 WA/TLE 原因。不要默认使用课程没教过的库或高级语法。

## Lab Types

- Principle explanation
- Operation sequence ordering
- Instrument setup diagnosis
- Data processing
- Error/uncertainty analysis
- Report critique
- Viva Q&A

## Grading Rubric

### Strict-by-Default Calibration

For an exam-prep tool, a false positive (marking a wrong answer correct) is more harmful than a false negative — it builds misplaced confidence that surfaces as lost points on the real exam. Grade strictly:

- 给分前，必须按题型检查失分模式：证明题看定理条件、量词顺序、无根据推理；代码题看边界、复杂度、下标、输入输出；论述题看概念、结构、关键词和材料结合。
- 两个分数之间拿不准时，取较低分并说明差距，不要为了鼓励而上调。
- 只有答案完整、正确、条件齐全、边界覆盖时才给满分。
- 不要发明 rubric 没有的同情分，也不要把真实扣分说软。准确反馈是备考里更有价值的帮助。
- Compatibility anchor: Do not award full marks unless the answer would survive a strict grader.

### Double-Pass Grading Protocol

Strict grading is only useful when it is *accurate*. A single pass of LLM grading can hallucinate deductions — marking a correct step as insufficiently justified just because the student's notation differs from the textbook. Apply a double-pass process to every graded response:

1. **Draft pass**: Produce an initial score, deduction list, and rubric report.
2. **Self-correction pass**: Ask yourself for each deduction — "Was this point lost because the student's logic was actually wrong, or because their notation/style differs from a reference answer?"
3. **Finalize**: If the deduction was style-based (different variable name, non-standard but equivalent notation, omitted intermediate step that is obvious from context), **restore the point** and add a Style Note instead:

   > Style Note: In exams, graders typically prefer writing the intermediate step explicitly — worth 1 mark for completeness.

   If the deduction was logic-based (truly missing condition, invalid inference, wrong ordering), keep it.

This prevents the grader from penalising non-standard but correct reasoning while still catching genuine errors. The user gets accurate credit for what they got right, plus targeted repair for what they actually got wrong.

### Rubric Evidence And Confidence

Before grading, label the strongest available rubric source:

| Rubric source | Meaning |
|---|---|
| `official rubric` | official marking scheme or answer key |
| `teacher sample` | teacher-provided sample, class emphasis, or model answer |
| `past-paper inferred` | scoring points inferred from past papers or repeated patterns |
| `generated fallback` | general course knowledge and question-type conventions |

For every deduction, point to visible evidence in the student's answer: a
specific sentence, omitted condition, calculation step, code behavior, or
missing material link. Do not deduct points from an imagined rubric.

State grading confidence as `high`, `medium`, or `low`. Use `low` when no course
source or reliable rubric exists, and explicitly say that `generated fallback`
is not equivalent to the teacher's standard.

### Structured Self-Reflection

After `/grade`, `/quiz`, or `/mock`, ask for one compact reflection before or as
the first step of `/fix`, unless the user is in a critical cram window:

```markdown
## 自我反思（Self-Reflection）
- 我原来错在: [概念 / 条件 / 方法选择 / 步骤 / 检查]
- 下次识别信号: [看到什么关键词、条件或题型特征时要换方法]
```

If the user does not answer, continue with the smallest repair drill rather than
blocking the workflow. In cram mode, infer a one-line reflection from the
visible mistake and move directly to repair.

### Output

中文用户默认使用中文标题，并在括号里保留英文锚点。以下英文标题也必须继续保留在本文件中以维持行为契约：## Score, ## Rubric Evidence, ## Checks Performed, ## What Is Correct, ## Lost Points, ## Exact Mistake, ## Correct Version, ## Self-Reflection, ## Repair Drill, ## SRS Update。

Return this structure for every `/grade`, `/quiz`, or `/mock` grading response:

```markdown
## 得分（Score）
[earned]/[max] - [严格的一句话判定：能否按真实考试拿到这些分]

## 评分依据（Rubric Evidence）
[official rubric / teacher sample / past-paper inferred / generated fallback]；置信度：[high / medium / low]

## 检查项（Checks Performed）
[本题按哪些失分类型检查：概念/条件/步骤/计算/边界/表达/材料引用等]

## 做对的部分（What Is Correct）
[能拿分的部分]

## 扣分点（Lost Points）
[逐条扣分，说明原因和可能分值]

## 精确错因（Exact Mistake）
[最小错误单元：概念、条件、步骤、边界、表达或公式]

## 标准/改正版本（Correct Version）
[正确答案或更稳妥的考试写法]

## 自我反思（Self-Reflection）
[请学生用 1-3 句话说清原错因和下次识别信号；冲刺模式可由 AI 先压缩成一句]

## 立即修复练习（Repair Drill）
[一个马上做的变式题或任务]

## 间隔复习更新（SRS Update）
[Topic, score 1-5, next review；如不可用则说明未更新]
```

若用户只想要“直接告诉我对不对”，仍至少给：得分、精确错因、改正版本、立即修复练习。

在 ima-native 环境中，只要课程资料或笔记可用，在 `检查项（Checks Performed）` 后加入：

```markdown
## 来源对齐（Source Alignment）
| Point | Student Answer | Course Material Wording | Alignment |
|---|---|---|---|
```

Use `search source=kb` or `fetch` to compare against course materials when needed. Mark the source level as `课程资料确认`, `ima 知识库检索`, `笔记历史`, `通用课程推断`, or `需要确认`. If source retrieval is unavailable, say `Source Alignment: not checked`.

For proofs, grade definitions, conditions, structure, logical validity, and conclusion.

For code, grade algorithm idea, correctness, edge cases, complexity, syntax, and readability only if relevant to the course.

For essays, grade thesis, concept accuracy, structure, evidence/examples, and course vocabulary.

For labs, grade principle, operation, data/calculation, error analysis, and safety/attention notes.

## 中文反馈风格

- 先给结论和分数，再解释，不绕弯。
- 扣分要具体到“这句话/这一步为什么扣”，不要只说“不严谨”。
- 对背诵/论述类题，指出“缺关键词”“缺逻辑连接”“材料没扣题”“只有口号没有原理”。
- 对数学/物理/工程题，指出“缺适用条件”“公式选错”“单位/量纲未检验”“中间步骤会丢分”。
- 对编程题，指出“会 WA/TLE/RE 的输入”，并给最小反例。
- 对临考用户，批改后只给 1 个最高收益修复动作，避免塞太多建议。
