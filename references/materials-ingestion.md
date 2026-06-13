# Materials Ingestion

用户上传或提到课程资料时使用：PDF、PPT、课堂笔记、作业、实验指导书、题库、往年题、复习提纲、老师划重点截图等。要把资料分析转成“聚焦 - 反馈 - 迭代”的复习状态时，使用 `references/focus-feedback-iteration.md`。当用户没有提供外部资料或只给很少线索时，先读 `references/material-retrieval.md`。

## Before Processing

1. 若尚无课程画像，先读 `references/course-profiles.md`。
2. PDF 先用 `pdf` skill 或可用工具提取文本、页码、标题层级和公式结构，再总结。
3. 笔记/课件图片可直接读图；看不清时只标注“未读清”，不要猜。
4. 中文高校资料优先识别：PPT 页码、章节标题、老师手写批注、星标/红框、复习提纲、学习通/雨课堂章节、题库编号、往年题年份。

## PDF Skill Fallback

The `pdf` skill may not be available in every environment. Before relying on it, check whether the skill is loaded; if not, fall back in this order:

1. `pdftotext` (poppler-utils) from the command line for text-based PDFs.
2. Ask the user to paste the relevant chapter/section text directly.
3. For scanned/image-only PDFs, ask the user to re-export with OCR enabled, or to provide the original source (slides, photos of notes).
4. Never fabricate missing pages, equations, or figures just because the PDF could not be read — say so explicitly and add the missing material to the gap list.

## Extraction Targets

From each material, extract:

- 章节/讲次顺序，以及与教材、PPT、题库的对应关系。
- 定义、定理条件、公式、标准解题模板、实验步骤或代码套路。
- 可能题型、重复出现的考法、往年题/作业/题库中的高频模式。
- 老师强调、星标、红框、复习提纲、课堂口头提示、答疑区高频问题。
- 用于章节排序的三类证据：考试范围权重、往年题频率、老师强调强度。
- 实验课要提取步骤、仪器、注意事项、安全点、数据处理和报告要求。
- 编程/机考要提取语言范围、允许库、输入输出格式、OJ 题型和边界条件。
- 缺口：缺少往年题、答案、评分标准、考试范围、不可读页、低置信章节。

## 中文资料优先级

同一主题有多个来源时，按下面顺序判断考试相关性：

1. 老师明确划重点、复习课 PPT、考试说明、答疑群公告。
2. 往年题、样卷、题库、课后重点题、实验考核要求。
3. 本学期课件和作业。
4. 教材章节和通用课程大纲。
5. 网络通用知识，只能作为补充，不得当作本课程考点确认。

若不同来源冲突，优先报告冲突，不要擅自合并成“确定范围”。

## Output Contract

中文用户默认输出中文栏目。为兼容旧示例和测试，英文锚点如下：Materials Inventory, Exam-Relevant Topics, Missing Materials, Priority Map, Stage 1 Core Review Pack, Updated Course Snapshot Fields, Next Action。

After `/materials`, produce this exact section structure so `/map`, `/plan`, and `/quiz` can reuse the result:

```markdown
## 资料清单（Materials Inventory）
[已读取的文件/片段；每份资料贡献了什么；不可读或缺页内容]

## 考试相关考点（Exam-Relevant Topics）
[高收益考点、必背内容、可能题型、老师强调信号]

## 缺失资料（Missing Materials）
[往年题、考纲、答案、实验评分标准、不可读页、低置信范围]

## 优先级地图（Priority Map）
[主题 -> P0/P1/P2 -> 考试动作 -> 证据来源 -> 置信度]

## 第一阶段核心复习包（Stage 1 Core Review Pack）
[使用 `references/staged-review-workflow.md`：★★★/★★/★ 必背项、概念摘要、题型识别、答题步骤，以及必需的 Most Worth Studying Chapters 表]

## 课程快照更新（Updated Course Snapshot Fields）
[Materials、Weak points（如有）、Next recommended]

## 下一步（Next Action）
[通常是 /map、/plan，或针对最高优先级缺口的 /quiz]

## 本轮闭环
[重点: 最高 P0/P1 主题；反馈: 资料证据或缺失信号；下一轮: 一个具体诊断、练习、补充上传或修复动作]
```

除非用户明确要求，不要在资料摄取后立刻生成整套模拟卷。先生成地图或计划，再进入练习。

For "most worth studying chapters", always combine exam-scope weight, past-paper frequency, and teacher-emphasis strength when those inputs exist. Use `P0` (must master), `P1` (focused breakthrough), and `P2` (understand / quick scan). If one input is missing, keep the table and mark that column as `unknown` rather than inventing values.

## Materials Missing or Too Thin

当用户给的资料很少，例如“帮我复习高数”：

1. 先读 `references/material-retrieval.md`，执行低置信资料检索流程。
2. 标准化课程名、学科族、可能考试形式和常见同义词。
3. 检测环境是否支持 `kb-search`、`note-search`、`workspace-search`、`rag-search` 或 `web-search`。
4. 优先检索用户自己的知识库、笔记、RAG 上下文和本地文件；再检索官方公开来源；最后才使用通用课程大纲。
5. 输出 `检索证据表`，标注 `课程资料确认 / 知识库检索 / 笔记历史 / 官方公开来源 / 通用课程推断 / 需要确认`。
6. 若检索仍为空，用课程名和常见教学大纲建立低置信临时画像，并在 Current Course Snapshot 中把 `Materials` 标为 `no external material; low-confidence scaffold`。
7. 先给一个有用诊断步骤或 P0 候选练习，再只请求一个最高价值补充材料：考纲、章节列表、老师重点、往年题或 PPT 目录。
8. 真实资料到达后修订地图；不要把通用章节当作已确认考试范围。

## Incremental Ingestion

Current Course Snapshot 已有资料，而用户又提供新文件或内容时：

1. **不要重复**旧资料总结，只报告新增或变化。
2. 按主题合并到现有知识清单，不按文件顺序堆叠。
3. 标出新旧资料冲突，例如公式、范围、考法、实验步骤不一致。
4. 更新缺口列表：移除已补齐缺口，加入新暴露的缺口。
5. 刷新 Current Course Snapshot 的 `Materials` 和 `Next recommended` 字段。
6. 新资料覆盖旧主题时，简短说明重叠，跳过冗余总结。

## Multi-File Handling

When multiple files arrive:

- 按章节/主题合并，不按文件顺序堆叠。
- 标出来源冲突。
- 计算考试权重时，优先使用往年题、老师课件和复习课材料，而不是教材默认顺序。
- 说明重复覆盖并跳过冗余总结。

## Ingestion by Environment

The ingestion step depends on host capabilities. Use `references/environment-adaptation.md` first when the host is unknown or when file access, retrieval, OCR, or persistence matters.

- **Agent shell**：直接读磁盘文件；可用时运行 `pdf` skill；用可用图像/PDF 工具 OCR 图片；从文件名和标题建立章节索引。典型环境包括具备文件/shell 工具的 Codex、Claude Code、OpenClaw、Hermes、WorkBuddy、Qoder Work。
- **RAG notebook**：模型已有文档上下文或检索。典型环境包括 NotebookLM 和文档问答笔记本。跳过本地读文件；以检索/粘贴片段为单位，宿主支持引用时给出处。检索很薄时，要求用户提供章节标题、页码范围或粘贴片段。
- **ima-native**：先用 `references/ima-adaptation.md`。优先用 `search source=kb` 找资料，再用 `fetch` 读具体文件、媒体、URL 或笔记。用户要整理知识库或定位 kb_id/files/tags 时，调用 `use_skill name=ima-knowledge`。通过 `use_skill name=ima-note` 更新课程主页，或输出 Course Home Markdown fallback。
- **Notes app**：用户在 Obsidian 或 Markdown/PKM 工具中。优先 Markdown-native 摄取：标题、标签、反链、粘贴笔记块、逐段摘要。需要时输出可复制块，使用 `#课程/高数`、`#错题`、`[[极限]]` 等标签/反链。未确认前不要假设可执行 shell 或直接访问 vault。
- **Plain chat**：没有可靠文件能力。请学生：
  1. 直接粘贴相关章节文本，一次只处理一个主题。
  2. 发送手写笔记照片或课件截图。
  3. 若客户端不能接收 PDF，把 PDF 按页转成图片发送。
  4. 资料很长时分轮处理：先目录和章节标题，再按优先级逐章处理。

在 notes app 或 plain chat 摄取后，必须先回显紧凑资料摘要，让学生确认“是我发的这些内容”，再开始复习任务。

当 plain chat 没有任何资料时，不要声称完成检索。输出 `references/material-retrieval.md` 的可复制查询词、低置信课程框架和一个诊断题。
