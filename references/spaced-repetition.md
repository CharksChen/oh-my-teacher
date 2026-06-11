# Spaced Repetition

Use this file for `/review-due`, SRS file handling, due-date calculation, and automatic SRS updates after `/quiz`, `/mock`, `/oral`, `/grade`, `/fix`, `/socratic`, or `/feynman`. For host fallbacks, see `references/environment-adaptation.md`.

In agent shells, prefer `scripts/srs.py` for deterministic `init`, `update`, `due`, `list`, and `set-active` operations instead of hand-editing Markdown tables.

In ima-native environments, prefer the SRS table in the course homepage or a dedicated ima-note. Use `search source=note` to find it, `fetch type=note_id` to read the full note when needed, and `use_skill name=ima-note` to update it. Use `memory_recall` only as a fallback or to find the active course context.

## Slug Consistency

The SRS slug and the snapshot slug **must** be the same for a given course. `scripts/snapshot.py` exposes a `slugify()` helper that derives slugs from course names (Unicode-aware, see `course-profiles.md` → Slug Convention). `scripts/srs.py` does **not** derive slugs itself — it accepts them via `--slug` or `--active`. When initializing a new SRS file, derive the slug with `snapshot.py slug "Course Name"` first, then pass it to `srs.py`:

```bash
# Bash
SLUG=$(python scripts/snapshot.py slug "Course Name")
python scripts/snapshot.py set-active --course "Course Name"
python scripts/srs.py init --slug "$SLUG" --active
python scripts/srs.py set-active "$SLUG" --require-exists
```

```powershell
# PowerShell
$SLUG = python scripts/snapshot.py slug "Course Name"
python scripts/snapshot.py set-active --course "Course Name"
python scripts/srs.py init --slug "$SLUG" --active
python scripts/srs.py set-active "$SLUG" --require-exists
```

If the slugs diverge, the active SRS and active snapshot may point to different courses, causing incorrect review scheduling.

## SRS State Files

In agent shell:

- Single-course mode: `.oh-my-teacher/srs-state.md`.
- Multi-course mode: `.oh-my-teacher/srs/<course-slug>.md` plus `.oh-my-teacher/srs/_active`.

Use this table shape:

```markdown
| Topic | Last Review | Score | Streak | Next Review |
|-------|-------------|-------|--------|-------------|
| limits-epsilon-delta | 2026-06-01 | 4 | 2 | 2026-06-04 |
| rolle-theorem | 2026-06-05 | 2 | 0 | 2026-06-06 |
```

Fields:

- **Topic**: short label, consistent across sessions.
- **Last Review**: ISO date of last practice on this topic.
- **Score**: 1-5.
- **Streak**: consecutive reviews with score >= 3; resets to 0 on score <= 2.
- **Next Review**: ISO date for next review.
- **Difficulty**: easy / medium / hard. Adjusts the base interval by a multiplier before computing Next Review.

## Date Source

All scheduling depends on today's date.

- Agent shell: obtain the current date from the environment before computing intervals or filtering due topics. Use the available platform command, not a hardcoded shell.
- RAG notebook, notes app, or plain chat: if today's date is not already known from the conversation, ask once before computing absolute dates.
- If the date cannot be determined, store intervals relative to "last review + N days" and do not invent overdue counts.

## Interval Algorithm

When a topic is reviewed with score `S`:

1. If `S <= 2`: set streak to 0 and next review to tomorrow.
2. If `S >= 3`: increment streak and compute base interval:

| Streak | Base Interval |
|--------|---------------|
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 14 days |
| 5+ | 30 days |

3. Adjust by difficulty multiplier:

| Difficulty | Multiplier | Effect |
|------------|-----------|--------|
| easy | 1.4 | Review less often |
| medium | 1.0 | Default |
| hard | 0.6 | Review more often |

`final_interval = max(1, int(base_interval * multiplier))`

4. Update the existing row with the new score, streak, difficulty, and computed next review date. If the topic is new, append a row.

Separately, the model may suggest difficulty changes:

- After a topic is scored ≥ 4 three consecutive times → suggest bumping difficulty to `easy`.
- After a topic is scored ≤ 2 twice in a row → suggest dropping difficulty to `hard`.
- The user can always manually override via `--difficulty` on `srs.py update`.

## `/review-due`

When the user runs `/review-due`:

1. Agent shell:
   - If `.oh-my-teacher/srs/` and `.oh-my-teacher/srs/_active` exist, read the active multi-course SRS file.
   - Otherwise read `.oh-my-teacher/srs-state.md` if it exists.
   - Preferred helper: `python scripts/srs.py due` or `python scripts/srs.py due --today YYYY-MM-DD` (the `--today` flag defaults to the system date when omitted).
2. ima-native:
   - Use `search source=note` for the active course homepage, SRS Table, and recent wrong-question notes.
   - Use `fetch type=note_id` when a candidate note is found.
   - If multiple courses match, use `ask_user` once to confirm the active course.
   - Update the note via `ima-note` or output a copyable Markdown fallback.
3. RAG notebook, notes app, or plain chat: parse the last copyable SRS block or note table.
4. Determine today's date before filtering.
5. Filter rows where `Next Review <= today`.
6. Sort by overdue days descending, then lowest score first.
7. Present the due list and offer to start `/quiz` on the highest-priority topic.

## Automatic Updates

After each `/grade`, `/quiz`, `/mock`, `/oral`, or `/fix` answer:

- Extract the topic from the question.
- Use the score to update or create the topic row.
- Mention the update briefly with the next review date.
- Preferred helper: `python scripts/srs.py update "topic" --score 4` (omit `--today` to use the system date).

In RAG notebook, notes app, or plain chat, output the SRS table as a copyable Markdown block after each update. For notes apps, optional tags such as `#复习计划` and backlinks such as `[[极限]]` are useful when they do not clutter the table.
