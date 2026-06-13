# Lightweight Adaptive State

Use this file when choosing the next review action for `/plan`, `/map`,
`/dashboard`, `/summary`, `/quiz`, `/fix`, reminders, or any workflow that needs
to decide what the student should do next.

This is a pragmatic recommendation layer, not a psychometric model. Do not call
it real IRT, CAT, BKT, DKT, MIRT, or knowledge tracing unless the deployment has
a calibrated item bank, enough response history, and benchmark evidence.

## Topic State Fields

Keep human-facing progress in the Current Course Snapshot. When file persistence
exists, keep machine-readable topic state in `.oh-my-teacher/state.json` under
`adaptive.topics`.

Each topic entry may contain:

```json
{
  "priority": "P0",
  "mastery_band": "weak",
  "scaffold_level": "teach",
  "last_evidence": "quiz 2/5 on 2026-06-13",
  "prerequisites": ["limits-definition"],
  "blocked_by": ["limits-definition"],
  "exam_scope_weight": 30,
  "past_paper_frequency": 2,
  "teacher_emphasis_strength": "high"
}
```

Field meanings:

- `priority`: `P0`, `P1`, `P2`, or `unknown`; derived from exam-scope weight,
  past-paper frequency, and teacher-emphasis strength.
- `mastery_band`: `weak`, `unstable`, `ok`, or `strong`; derived from quiz,
  mock, grade, oral, SRS, wrong-note, or confidence-calibration evidence.
- `scaffold_level`: `teach`, `guide`, `prompt`, or `test`; controls how much help
  the AI gives before asking the student to perform.
- `last_evidence`: the most recent visible signal that justified the state.
- `prerequisites`: small list of required earlier topics.
- `blocked_by`: prerequisites currently blocking progress on this topic.
- `exam_scope_weight`: numeric percentage or point share when known.
- `past_paper_frequency`: count of recent papers where the topic appeared.
- `teacher_emphasis_strength`: `high`, `medium`, `low`, or `unknown`.

## Mastery Band Updates

Use visible evidence only:

- `weak`: score <= 2/5, repeated lost points, high-confidence miss, SRS leech, or
  cannot explain the prerequisite.
- `unstable`: score 3/5, mixed performance, correct answer with missing
  condition, or needs heavy hints.
- `ok`: score 4/5, mostly correct with one small repair.
- `strong`: score 5/5 or repeated clean answers under exam-like constraints.

When evidence is missing, leave the band unknown instead of guessing.

## Scaffolding Fading

Use the shared levels `teach -> guide -> prompt -> test`.

| Level | Use when | AI behavior |
|---|---|---|
| `teach` | new topic, score <= 2, prerequisite missing | explain compactly, show one worked step, then ask a recall question |
| `guide` | score 3, stuck after first attempt, unstable concept | ask targeted questions, give hint ladder, leave key blanks |
| `prompt` | score 4 or two improving attempts | ask the student to choose method, give minimal cues only |
| `test` | score 5 or repeated clean performance | exam-style question first, feedback after answer |

Move one level toward `test` after strong evidence. Move one level back toward
`teach` after a miss, leech warning, or prerequisite block. Do not keep giving
full explanations once the student can perform; transfer responsibility.

## Deterministic Recommendation Score

When several next actions are possible, rank topics with this lightweight score:

```text
score =
  priority_score
  + exam_scope_score
  + past_paper_score
  + teacher_emphasis_score
  + weakness_score
  + srs_due_score
  + prerequisite_block_score
  + urgency_score
```

Default weights:

| Signal | Score rule |
|---|---|
| Priority | P0 +40, P1 +25, P2 +10, unknown +0 |
| Exam-scope weight | numeric percent or points, capped at +25 |
| Past-paper frequency | +6 per appearance, capped at +18 |
| Teacher emphasis | high +18, medium +10, low +3, unknown +0 |
| Mastery band | weak +30, unstable +18, ok +5, strong -20 |
| SRS due | due today +12; overdue adds up to +10 more |
| Prerequisite blocking | +20 when this topic blocks a P0/P1 topic |
| Urgency | days left <= 3: +10 to weak P0/P1 topics |

Tie-breakers: P0 before P1 before P2, weaker mastery first, SRS due first, then
most recent evidence.

Recommended action:

- weak + blocked: `/fix` prerequisite first.
- weak without block: `/fix` or `/quiz` on the smallest lost point.
- unstable: `/quiz` with one close variant, then grade.
- ok: interleave once or schedule SRS.
- strong: de-prioritize to quick review unless it is a P0 memorization item.

## Output Contract

For dashboards, plans, summaries, and digests, show a compact next-action table:

```markdown
## 下一步推荐
| Rank | Topic | Why now | Action |
|---|---|---|---|
| 1 | [topic] | [P0 + weak evidence + SRS due / prerequisite block] | [/fix or /quiz action] |
```

Then end with the shared loop footer from `references/focus-feedback-iteration.md`.

## Script Support

In agent shells, prefer:

```bash
python scripts/recommend_next.py --today YYYY-MM-DD
```

Use `scripts/snapshot.py state-merge` to update machine-readable adaptive fields
without changing the human-facing Markdown snapshot. If scripts are unavailable,
apply the same rules manually and emit the recommendation table inline.
