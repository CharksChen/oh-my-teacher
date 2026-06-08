# Review Plans and Study Maps

Use this file for `/plan`, `/map`, `/cram`, multi-course planning, final review sheets, and progress heat maps.

## Study Map

Produce:

- Course profile assumptions.
- Chapter or knowledge tree.
- Priority labels: must know, high-yield, hard, quick scan, low priority.
- Exam actions: memorize, understand, derive, calculate, code, draw, operate.
- Likely question types and common traps.
- Next practice set.
- Progress heat map when the Current Course Snapshot has accuracy or SRS data.

If materials include past papers, estimate topic weight from repeated concepts and question types. Avoid claiming certainty.

## Progress Heat Map

For `/map` and `/plan`, include a compact ASCII progress bar per chapter/topic when mastery data exists:

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

Use available days and daily hours. Keep plans realistic.

Include:

- Daily minimum line: tasks required for the goal.
- Optional bonus line: tasks for a higher score.
- Active recall every day.
- Error repair after practice.
- Mock exam near the end.
- Final 30-minute sheet.

Modes:

- Pass-only: prioritize standard questions, definitions/formulas, and common templates.
- High-score: add hard variants, proofs, mixed problems, and timed full mocks.
- Cram: remove low-yield reading, use last-page sheet, standard methods, and focused drills.
- Multi-course: rank by exam date, difficulty, credit/importance, and current weakness.

## Cram Mode

Use when time remaining is short or the user explicitly requests `/cram`.

- Start from scoring yield, not chapter order.
- Focus on standard methods, formula conditions, common traps, and high-frequency question types.
- Prefer short drill loops over long summaries.
- Produce a final-page sheet and a short "do not waste time on" list.

## Last Page

For final review, generate a compact sheet:

- Must-know definitions/formulas.
- Standard templates.
- Common traps.
- Time allocation.
- Things to check before submitting.
- For labs: steps, data table, error analysis, viva Q&A.
