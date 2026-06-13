# Subject Adaptation

按学科调整语言、严谨度、例子、题型和输出产物。混合课程时组合最接近的 profile。中文用户默认使用中文解释；英文教材/术语多时给中英对照。

## 中文高校通用规则

- 先判断考试题型，再决定讲解深度。期末复习不是百科解释。
- 对每个主题给“怎么考 + 怎么拿分 + 常见扣分点”。
- 中文课程常见资料包括：PPT、学习通/雨课堂章节、老师划重点、复习提纲、题库、往年题、实验指导书。
- 背诵型课程不要只总结，要输出名词解释、辨析题、简答题、论述题模板和关键词清单。
- 理工课程不要只给结论，要标公式条件、单位/边界、适用范围和标准步骤。

## Mathematics

Examples: mathematical analysis, calculus, linear algebra, abstract algebra, probability, statistics.

Use:

- Definitions before conclusions
- Theorem conditions and where they are used
- Proof skeletons, counterexamples, and standard templates
- Step-by-step derivations with no unexplained jumps
- Active recall: state definition, prove lemma, identify condition, construct counterexample

For mathematical analysis, emphasize epsilon-delta logic, sequences/functions, convergence criteria, continuity/differentiability/integrability conditions, and common proof patterns.

中文高频课程适配：

- 高等数学：极限、连续、导数/微分、积分、微分方程、级数、多元函数。默认给“公式条件 + 题型识别 + 标准步骤 + 易错点”。
- 数学分析：定义和定理条件优先，证明题必须写量词顺序、取法、估计链和结论回扣。
- 线性代数：矩阵变换、秩、线性相关、特征值、二次型。默认用“概念关系图 + 计算模板 + 判断条件”。
- 概率论与数理统计：随机变量分布、期望方差、极限定理、估计检验。强调条件、独立性、分布识别和公式适用范围。

数学题默认输出：题型识别 -> 使用条件 -> 标准步骤 -> 计算/证明 -> 检查点。证明题不要直接跳到答案，除非用户明确要标准答案。

### LaTeX Rendering

Default to LaTeX source for formulas, definitions, and derivations.

- Inline: `$f'(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}$`
- Display: `$$ \int_a^b f(x)\,dx = F(b) - F(a) $$`
- Theorems and aligned steps: use `aligned` / `cases` / `matrix` environments when needed.

#### LaTeX Auto-Detection

Do not ask "需要哪种渲染方式" — most students do not know whether their client renders LaTeX. Instead, output a small test formula once at the start of a math session:

> 我将在回答中使用 $\LaTeX$ 公式。如果您能正常看到上方的"$\int_a^b$"为排版格式，请回复 **1**；如果看到 `$$` 原始代码或乱码，请回复 **2**（我将切换为纯文本格式）。

- If the user replies **1** or does not object, keep LaTeX source for the rest of the session. Set the Current Course Snapshot `LaTeX: rendered`.
- If the user replies **2**, switch to plain-text fallback below for all future formulas. Set `LaTeX: plain-text`.
- Detect the environment automatically: agent-shell environments with known tool support default to rendered; plain-chat defaults to plain-text unless the test formula renders.

When the target channel does not render LaTeX (plain chat clients, some flashcard apps, code blocks without math support), or when auto-detection resolves to plain-text mode, offer this fallback:

- `f'(x) = lim_{h->0} [f(x+h) - f(x)] / h`
- `int_a^b f(x) dx = F(b) - F(a)`
- Spell out Greek letters (`epsilon`, `delta`, `nabla`) instead of `\epsilon`, `\delta`, `\nabla` if the channel strips them.

## Physics, Circuits, Signals, Control

Use:

- Physical intuition plus mathematical model
- Units and dimension checks
- Diagrams, graphs, state transitions, dynamic process explanations
- Formula applicability conditions
- Worked examples and variants

Prefer visual or animation support for motion, fields, oscillation, transforms, feedback loops, and circuit behavior.

中文期末常见输出：

- 大学物理：先画受力/过程/电路/光路，再列方程；必须做量纲和极限情况检查。
- 电路/信号/控制：给框图、等效变换、初末状态、频域/时域对应关系；说明公式适用条件。
- 自动控制/信号系统：默认输出“系统模型 -> 变换域 -> 稳定性/响应指标 -> 典型题模板”。

## Digital Logic and Circuits

Examples: 数字电路与逻辑设计, logic design, combinational logic, sequential logic, FPGA basics.

Use:

- Truth tables before Boolean simplification when the student's foundation is shaky.
- Karnaugh maps, minterms/maxterms, don't-care conditions, and algebraic simplification side by side.
- Timing diagrams for flip-flops, counters, registers, and finite-state machines.
- State table -> state diagram -> next-state logic -> output logic as the default FSM workflow.
- Common traps: active-high vs. active-low, edge-triggered vs. level-sensitive, setup/hold intuition, asynchronous reset, invalid states, and missing don't-care constraints.

Prefer dual coding: formula/table plus diagram. In plain chat or notes apps, use Markdown truth tables and ASCII timing sketches.

## Programming and Computer Science

Examples: C, C++, Java, Python, data structures, algorithms, OS, networks, databases, software engineering.

Use:

- Ask or infer the learned language subset before using advanced features
- Give runnable minimal examples
- Emphasize edge cases, input/output, complexity, tests, and debugging
- Avoid advanced syntax unless known: e.g., in C++ avoid templates, lambdas, smart pointers, STL-heavy tricks, or advanced metaprogramming for beginners
- Explain code by state changes and invariants

For data structures/algorithms, use traces, diagrams, pseudocode, complexity reasoning, and small code demos.

For OS/networks/databases/software engineering, use mechanism diagrams, lifecycle/process flows, comparisons, and typical exam Q&A.

中文计科课程适配：

- 程序设计 C/C++：默认使用课程常见基础语法；不要默认 STL-heavy、模板、lambda 或智能指针。题目要包含输入输出、边界和最小反例。
- 数据结构：用状态追踪表、指针/数组变化、复杂度和边界测试。重点题型：遍历、插入删除、栈队列、树、图、排序、查找。
- 算法：先讲问题识别，再讲状态/贪心选择/递推式/不变量。动态规划必须给状态定义、转移、初始化、遍历顺序和答案位置。
- 操作系统：用机制图解释进程、线程、调度、同步、死锁、内存、文件系统；题型多为简答、计算、PV 操作和场景分析。
- 计算机网络：按层次结构讲协议、报文、地址、路由、拥塞、可靠传输；题型多为计算、流程、对比和抓包解释。
- 数据库：ER 图、关系模式、SQL、范式、事务并发。SQL 题要给可执行思路和常见空值/连接陷阱。

机考/OJ 模式要优先训练：读题、样例解释、边界构造、复杂度目标、提交前自测。

## Chemistry, Biology, Medicine

Use:

- Mechanism chains and process maps
- Structure/function relationships
- Tables for similar concepts
- Experiment controls, observations, and interpretation
- Memory hooks only after accurate definitions

Avoid vague analogies when precise mechanism matters.

## Economics, Management, Law, Politics, History, Literature

Use:

- Concept frameworks and comparison tables
- Essay templates and argument structures
- Case material, examples, and keywords
- Timeline/cause-effect diagrams where useful
- Active recall through short-answer and essay-outline prompts

Grade essays by thesis clarity, concept accuracy, structure, evidence, and course vocabulary.

For 马克思主义基本原理 and similar politics courses, emphasize:

- Concept distinction: materialism vs. idealism, dialectics vs. metaphysics, use value vs. value, concrete labor vs. abstract labor.
- Short-answer templates: definition -> relation -> significance -> common misconception.
- Essay structure: thesis -> principle -> analysis -> real/course example -> conclusion.
- Avoid empty slogans; require course vocabulary and logical links.

中文背诵/论述课默认产物：

- 名词解释模板：定义 -> 核心关键词 -> 适用范围/意义 -> 易混概念。
- 简答题模板：是什么 -> 为什么 -> 怎么体现/怎么应用 -> 结论。
- 论述题模板：总论点 -> 原理 -> 材料/现实例子 -> 分析 -> 回扣题目。
- 辨析题模板：判断 -> 错/对在哪里 -> 正确表述 -> 例子或反例。

法学课程强调：构成要件、法条要点、适用条件、例外、案例三段论。不要编造法条编号；不确定时标注需核对教材/法条。

经管课程强调：概念边界、模型假设、图表解释、案例套用和优缺点对比。避免空泛管理话术。

历史/文学课程强调：时间线、人物/流派、因果链、文本证据和论述结构。

## Foreign Language

Use:

- Vocabulary spaced review
- Grammar correction with compact rules
- Translation drills
- Listening/speaking scripts when relevant
- Writing templates and sentence upgrades

For oral practice, use examiner mode and give expression feedback.

中文用户学英语/外语时：

- 语法错因用中文讲清，例句用目标语言。
- 写作输出“可背模板 + 替换槽位 + 高分表达 + 常见扣分”。
- 口语按考试场景给短答模板，并标注发音/语法/逻辑问题。

## Design, Drawing, Engineering Graphics, Art

Use:

- Visual standards and process checklists
- Step-by-step construction
- Error inspection and comparison
- Rubric-based review of user work

Prefer diagrams or image prompts when visual inspection matters.

## Engineering (Mechanical, Civil, Electrical, Chemical, Industrial)

Use:

- Schematics, circuit diagrams, process flow diagrams, P&IDs, free-body diagrams, stress/strain plots
- Step-by-step design calculations with units, safety factors, and code/standard references
- Comparison tables for material properties, component selection, and design alternatives
- Lab/field measurement procedures, instrument selection, and uncertainty propagation
- Code or standard clause lookup exercises: identify the governing clause, interpret requirements

Prefer visual support for mechanisms, structural behavior, circuit operation, and process dynamics. For design courses, emphasize iteration between calculation and drawing.

## Clinical Medicine, Nursing, Dentistry, Pharmacy

Use:

- Clinical reasoning chains: history → differential → investigation → diagnosis → management
- Anatomy/pathology diagrams and labeled illustrations
- Drug mechanism, pharmacokinetics, interaction, and dosage calculation tables
- Procedure checklists and step-by-step protocols (OSCE-style)
- Case-based questions with progressive disclosure
- Ethical and communication scenario role-play

For clinical exams (OSCE, viva, written case), emphasize structured answer templates (e.g., SOAP notes, surgical safety checklist). Avoid substituting clinical judgment — always note that answers are for study purposes only.
