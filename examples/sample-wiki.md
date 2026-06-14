# Sample Session — 课程知识库（/wiki, /wiki-ask, /wiki-lint）

演示 LLM Wiki 三操作在课程复习中的用法：Ingest、Query、Lint。环境为 Agent shell。

---

## /wiki —— Ingest（摄取一份课件）

**User**：把这份《数学分析》第 3 章课件整理进知识库。（上传 lecture-03.pdf）

**Assistant**：
当前策略：知识库摄取（Ingest），把资料沉淀成互联页面而不是一次性总结。

已 `python scripts/wiki.py init --course "数学分析"`，并把原件存入 `sources/lecture-03.md`（不可变）。

本次摄取触及的页面：

- 新建 `pages/极限的-epsilon-delta-定义.md`（概念，P0）
- 新建 `pages/函数极限的运算法则.md`（定理，P1）
- 新建 `pages/极限-考点.md`（考点：求极限三种典型考法）
- 修订 `INDEX.md`：第 3 章 MOC 加入上述页面链接
- 交叉链接：[[极限的-epsilon-delta-定义]] ↔ [[函数极限的运算法则]] ↔ [[极限-考点]]

页面示例（`pages/极限的-epsilon-delta-定义.md`）：

```markdown
---
title: 极限的 epsilon-delta 定义
type: concept
tags: [数学分析, 极限]
priority: P0
sources: [sources/lecture-03.md]
srs: 极限-epsilon-delta
---

# 极限的 epsilon-delta 定义

**定义**：对任意 epsilon > 0，存在 delta > 0，使 0 < |x - a| < delta 时 |f(x) - L| < epsilon。
**来源**：课程资料确认（lecture-03，第 12 页）。
**陷阱**：delta 依赖 epsilon 与 a，不能写成与 epsilon 无关的常数。
**相关**：[[函数极限的运算法则]]、[[极限-考点]]
```

确认一下：这三页是否覆盖了你课件里的第 3 章重点？

## 本轮闭环
- 重点：P0 [[极限的-epsilon-delta-定义]] 与 [[极限-考点]]。
- 反馈：3 个新页面 + 1 个 MOC 更新，全部来源等级为“课程资料确认”。
- 下一轮：再摄取往年题以补全 [[极限-考点]] 的高频考法，或 `/quiz` 测 epsilon-delta。

---

## /wiki-ask —— Query（基于知识库提问）

**User**：/wiki-ask 证明 lim 时 delta 可以和 a 无关吗？

**Assistant**：
先查到相关页面：[[极限的-epsilon-delta-定义]]、[[函数极限的运算法则]]。

**答案**：一般不行。delta 通常依赖 epsilon 和点 a；只有在**一致连续**时才能取与 a 无关的 delta。
**引用**：[[极限的-epsilon-delta-定义]]（来源：sources/lecture-03.md 第 12 页）。

这是一个被澄清的高频陷阱，已**回填**为新页面 `pages/一致连续-vs-逐点.md`，并从 [[极限的-epsilon-delta-定义]] 链接过去——知识库因此累积。

## 本轮闭环
- 重点：新增 [[一致连续-vs-逐点]]。
- 反馈：答案有页面与原始来源双重引用。
- 下一轮：`/wiki-lint` 确认新页面已被正确链接。

---

## /wiki-lint —— Lint（知识库体检）

**User**：/wiki-lint

**Assistant**：
运行 `python scripts/wiki.py lint --slug 数学分析 --json`：

```text
pages: 4  issues: 1
orphans (无入链): 一致连续-vs-逐点
```

机械体检发现 1 个孤页；语义体检无矛盾、无陈旧。

**修复**：在 [[极限的-epsilon-delta-定义]] 的“相关”里补上 [[一致连续-vs-逐点]]，孤页消除。
**覆盖缺口**：对照 `/paper-analyze`，[[极限-考点]] 还缺“夹逼定理”考法页面（P1）。

## 本轮闭环
- 重点：知识库结构归零问题。
- 反馈：孤页已修复；剩 1 个 P1 覆盖缺口。
- 下一轮：摄取一份往年题，新建“夹逼定理”考点页补缺口。
