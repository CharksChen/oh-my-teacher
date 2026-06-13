# Review Plans and Study Maps

用于 `/plan`、`/map`、`/cram`、`/last-page`、`/dashboard`、多课程排期、考前一页纸和进度热力图。学习策略选择见 `references/learning-strategies.md`；复习闭环见 `references/focus-feedback-iteration.md`；显式每日/每周提醒或知识归纳见 `references/opt-in-reminders.md`。

## Study Map

Produce:

- 课程画像假设：考试形式、剩余时间、目标分、资料置信度。
- 章节/知识树：按教材章节和老师课件顺序对齐。
- 优先级标签：必会、高频、难点、快速扫过、低优先级。
- 当资料包含考试范围、往年题或老师强调时，必须给 "Most Worth Studying Chapters" 表。按 exam-scope weight + past-paper frequency + teacher-emphasis strength 排 P0/P1/P2；缺证据写 unknown。
- 考试动作：背、理解、推导、计算、写代码、画图、操作、套模板。
- 可能题型和常见坑。
- 下一组练习。
- Current Course Snapshot 有 Accuracy 或 SRS 数据时，加入进度热力图。
- 当前复习闭环：重点、反馈证据、下一轮目标。

如果有往年题，从重复概念、题型、分值和出现年份估算权重。避免说“必考”，改说“高频/证据强/需要确认”。

中文输出建议结构：

```markdown
## 课程假设
## 知识树与章节地图
## Most Worth Studying Chapters
## 掌握度热力图
## 高频题型与常见坑
## 下一组练习
## 本轮闭环
```

## Progress Heat Map

对 `/map` 和 `/plan`，只要有掌握度数据，就给每章/主题一个紧凑 ASCII 进度条：

```text
Topic                    Mastery
Limits and continuity    [########--] 80%  (8/10 accuracy, SRS streak 3+)
Differentiation          [######----] 60%  (6/10 accuracy)
Integration              [##--------] 20%  (2/10 accuracy)
Series                   [----------]  0%  (not yet practiced)
```

Compute mastery as:

1. If Accuracy has a score for the topic: `pct = accuracy_score * 10`, capped at 100.
2. If no Accuracy data but SRS has entries: `pct = topics_at_streak_3_plus / total_topics_in_chapter * 100`.
3. If neither exists: `pct = 0`.

Place the heat map after the knowledge tree and before common traps.

## Review Plan

使用剩余天数和每天可用时间。计划必须现实，不要把 10 小时任务塞进 2 小时。

必须包含：

- 每日底线任务：为了目标分必须完成的部分。
- 可选加分任务：冲更高分时再做。
- 每天必须有主动回忆，不允许只安排“看书/看 PPT”。
- 每个学习块标注策略：retrieval、spaced review、interleaving、self-explanation、Socratic、Feynman、dual coding、mock。
- 练习后必须安排错题修复。
- 考前安排一次模考或微型限时套题。
- 最后 30 分钟复习 sheet。
- 每天一行闭环：Focus -> 练习/反馈信号 -> 迭代动作。

模式：

- Pass-only：优先标准题、定义/公式、常见模板和保底分。
- High-score：加入难变式、证明、综合题和完整限时模考。
- Cram：砍掉低收益阅读，用考前一页纸、标准方法和短循环刷题抢分。
- Multi-course：按考试日期、难度、学分/重要性和当前薄弱程度排序。

默认每日块结构：

1. 阅读前先做预检或主动回忆热身。
2. 修复最弱点或讲解最关键概念。
3. 做练习；基础稳定后改成交错练习。
4. 错题修复并要求自我解释。
5. 更新 SRS 和下一次到期复习。

中文 `/plan` 默认模板：

```markdown
## 目标与约束
- 距离考试:
- 每天可用时间:
- 目标:
- 资料置信度:

## 复习优先级
| 优先级 | 章节/主题 | 为什么先学 | 今日动作 |
|---|---|---|---|

## 每日计划
| 天 | 底线任务 | 可选加分 | 练习/反馈 | 本轮闭环 |
|---|---|---|---|---|

## 不要花太多时间
[低收益内容或暂时放弃项]

## 下一步
[一个马上开始的任务]
```

## Cram Mode

Use when time remaining is short or the user explicitly requests `/cram`.

- 从得分收益出发，不从章节顺序出发。
- 聚焦标准方法、公式条件、常见坑和高频题型。
- 用短练习闭环替代长摘要。
- 产出考前一页纸和简短“不要浪费时间”列表。

### Managing Exam Anxiety

Late-stage cramming is as much an emotional state as a knowledge gap; a panicking student retains little. Without being saccharine:

- **先给 quick win。** 先安排一个现在就能拿下的高收益点，打断慌乱，再进入难点。
- **范围有限且具体。** “3 个主题，90 分钟”比“全都复习”更可执行。
- **允许取舍。** 明确告诉学生跳过低收益内容是策略，不是失败。
- **保住基础分。** 定义、公式条件和标准模板通常比押最难题更稳。
- 语气冷静、直接，给下一个动作，不讲学习方法大道理。

## Last Page

考前最后复习，生成紧凑 sheet：

- 必背定义/公式。
- 标准题模板。
- 常见坑。
- 时间分配。
- 交卷前检查项。
- 实验课：步骤、数据表、误差分析、viva Q&A。

中文 `/last-page` 模板：

```markdown
# 考前一页纸

## 必背
## 标准模板
## 易错点
## 时间分配
## 交卷前检查
## 最后 30 分钟
```

In ima-native environments, build `/last-page` from `/source-map`, `/teacher-emphasis`, the Weak Point Board, SRS due items, and high-yield formulas/templates. Prefer writing it to ima-note; use it as the default input for `/ppt`.

## Dashboard

For `/dashboard`, generate a Markdown dashboard instead of relying on the local terminal dashboard:

```markdown
# 复习仪表盘

## 今日状态
- 距离考试:
- 当前目标:
- 今日必须完成:

## 掌握度热力图
[topic progress bars]

## 错误类型分布
[error-category table from wrong notes; see `references/wrong-note.md` → Error-Type Analytics. Omit if no wrong notes yet.]

## 今日待复习
| Topic | 原因 | 建议动作 |
|---|---|---|

## 最大风险
1.
2.
3.

## 下一步
```

In ima-native environments, gather data from `memory_recall`, `search source=note`, the course homepage, SRS table, weak-point board, and recent wrong notes. Update the dashboard through `ima-note` when available.
