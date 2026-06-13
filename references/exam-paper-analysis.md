# Exam Paper Analysis

用于 `/paper-analyze`、往年题、样卷、题库、作业题和老师发的复习卷。目标是从已提供资料中提取题型分布、高频考点、扣分模式和下一步复习策略，不做“押题确定性”承诺。

## ima Workflow

1. Use `search source=kb` to locate past papers, sample papers, homework, answer keys, and review sheets.
2. Use `fetch` for each concrete paper or answer key before extracting details.
3. Use `subagent_spawn type=research` when there are many papers or long answer keys.
4. Update the course homepage through `ima-note` with the analysis summary.

## Output Contract

```markdown
# 往年题分析

## Evidence Scope
- 已分析资料:
- 来源等级:
- 限制: 基于已导入试卷推断，不代表真实命题。

## 题型分布
| 题型 | 出现次数 | 平均分值 | 典型知识点 | 来源 |
|---|---:|---:|---|---|

## 高频知识点
1.
2.
3.

## 章节频率与优先级证据（Chapter Frequency For Priority Ranking）
| Chapter/topic | Paper count | Question types | Typical wording | Linked teacher/scope evidence | Confidence |
|---|---:|---|---|---|---|

## 出题模式
- 

## 扣分模式
- 

## 本周复习策略
- 必练:
- 快速过:
- 暂时降优先级:

## 下一步（Next Action）
```

## Rules

- 不要宣称真实考试一定会考。
- 区分“上传试卷证据”和“通用课程推断”。
- 缺答案时，把扣分模式结论标为低置信。
- 题库或往年题很多时，优先统计反复出现的题型、章节和问法，而不是逐题讲解。
- 对中文试卷，记录原题关键词，例如“证明”“求”“判断”“简述”“分析材料”，便于后续题型识别。
- 在 ima 中，如果 note 工具可用，把最终摘要写到课程主页或专门的往年题分析笔记。
