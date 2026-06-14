# Wrong Question Notes

用于 `/wrong-note`，以及 `/grade`、`/quiz`、`/mock` 后的错题跟进。错题本不是收藏夹；每条错题必须能指导下一次修复和间隔复习。

存在课程知识库时（见 `references/course-wiki.md`），每条错题同时作为一个错题页接入 wiki：从相关概念页用 `[[..]]` 双向链接，frontmatter 接上 SRS 主题，让错因沉淀进知识库而不是孤立存在。

## ima Workflow

1. Start from a graded answer or wrong quiz/mock item.
2. Generate a note-native wrong-question entry.
3. Use `ima-note` to create or update the wrong-question note when available.
4. Use `memory_write` only for a durable summary: course, topic, error category, next review.
5. Update the SRS table in the course homepage or output a copyable table fallback.

## Wrong Note Template

```markdown
# 错题：[topic]

## 来源
- 课程:
- 来源: [往年题/题库/PPT/作业/模拟/用户自写]
- 题型:
- 分值/扣分估计:

## 题目

## 我的错误答案

## 正确答案

## 错因分类
- [ ] 概念不清
- [ ] 条件遗漏
- [ ] 公式记错
- [ ] 计算错误
- [ ] 方法选择错误
- [ ] 审题错误
- [ ] 表达不规范

## 最小错误点

## 同类题识别
[看到哪些关键词/条件/图形/输入格式时，应该想到这个方法]

## 修复说明

## 变式题
1. 基础题
2. 变式题
3. 综合题

## 下次复习
- Next Review:
- Difficulty:
- Tags: #错题 #[课程名] #[topic]
```

若用户临考，只保留“来源、错因分类、最小错误点、正确版本、同类题识别、下次复习”，不要写成长笔记。

## Error Taxonomy

Classify every wrong item into exactly one primary category (add a secondary only if clearly needed). Use this fixed set so categories aggregate cleanly across notes:

- `概念不清` — concept misunderstood
- `条件遗漏` — missing/forgotten condition or assumption
- `公式记错` — wrong formula/definition recalled
- `计算错误` — arithmetic/algebra slip with correct method
- `方法选择错误` — chose the wrong approach
- `审题错误` — misread the question/requirements
- `表达不规范` — correct idea, lost points on rigor/notation/presentation

These align with the error categories in `references/practice-workflows.md` → Error Repair. Keep the exact labels — analytics below depends on them.

## Error-Type Analytics

Wrong notes are not just per-item records; their categories aggregate into a diagnosis. When the student has several wrong notes, count categories and surface the distribution so review targets the *kind* of mistake, not just individual topics:

```markdown
## 错误类型分布（近 N 题）
| 错因 | 次数 | 占比 | 行动 |
|---|---|---|---|
| 条件遗漏 | 6 | 40% | 每道证明先列条件清单 |
| 计算错误 | 4 | 27% | 限时计算专练 + 复核步骤 |
| 概念不清 | 3 | 20% | /explain + /feynman |
| 方法选择错误 | 2 | 13% | 交错练习强化题型识别 |
```

Use this in `/dashboard` and `/summary`. A dominant category changes the plan: e.g. 40% 条件遗漏 means drilling more problems helps less than a "list conditions first" habit. Mark the conclusion as derived from the available notes, not certainty.

## Output After Creation

Return:

- wrong-note title
- topic
- error category
- next review
- one immediate repair drill
- whether ima-note and memory_write succeeded, or a Markdown fallback if not

中文默认回复：

```markdown
已生成错题：[title]
- 主题:
- 主错因:
- 下次复习:
- 立即修复:
- 保存状态: [ima-note / memory_write / Markdown fallback]
```
