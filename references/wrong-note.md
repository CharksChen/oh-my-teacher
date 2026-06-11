# Wrong Question Notes

Use this file for `/wrong-note` and for wrong-answer follow-up after `/grade`, `/quiz`, or `/mock`.

## ima Workflow

1. Start from a graded answer or wrong quiz/mock item.
2. Generate a note-native wrong-question entry.
3. Use `ima-note` to create or update the wrong-question note when available.
4. Use `memory_write` only for a durable summary: course, topic, error category, next review.
5. Update the SRS table in the course homepage or output a copyable table fallback.

## Wrong Note Template

```markdown
# 错题：[topic]

## 题目

## 我的错误答案

## 正确答案

## 错因分类
- [ ] 概念不清
- [ ] 条件遗漏
- [ ] 公式记错
- [ ] 计算错误
- [ ] 方法选择错误
- [ ] 表达不规范

## 最小错误点

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

## Output After Creation

Return:

- wrong-note title
- topic
- error category
- next review
- one immediate repair drill
- whether ima-note and memory_write succeeded, or a Markdown fallback if not
