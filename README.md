# Oh My Teacher

A university final-exam review assistant skill. It turns course materials into a focused study plan, practices you with adaptive quizzes and mock exams, grades your answers strictly, tracks your weak points with spaced repetition, and explains hard concepts with diagrams and runnable code.

> This is a **skill** — its behavior is defined by Markdown instructions that an LLM agent reads, not by a running program. `SKILL.md` is the entry point the model loads; the rest of the files are references it pulls in on demand.

## What it does

- **Profile a course** — infer the course, exam format, subject, your level, and time remaining.
- **Diagnose weak points** — a quick `/diagnose` pass calibrates where you stand before planning.
- **Plan & map** — realistic day-by-day review plans and exam-weighted concept maps.
- **Practice** — adaptive `/quiz`, timed `/mock` exams, `/oral` rehearsal, and `/group-quiz` sessions.
- **Grade strictly** — answer grading tuned to catch the mistakes that lose real exam points.
- **Spaced repetition** — `/review-due` schedules topics so you revisit them at the right time.
- **Explain** — subject-adaptive tutoring with diagrams, visuals, and runnable code demos.
- **Export** — turn study notes into Anki/Quizlet flashcards via `scripts/export_flashcards.py`.

It adapts to three host environments: **agent shells** (file system + tools), **RAG notebooks** (preloaded documents), and **plain chat** (no tools). See SKILL.md → Environment Adaptation.

## Directory structure

```
oh-my-teacher/
├── SKILL.md                  # Entry point: operating principles, command routing, output style
├── README.md                 # This file (human-facing overview)
├── agents/
│   └── openai.yaml           # Agent config: instructions, tools, model settings
├── references/               # Loaded on demand per command (see references/INDEX.md)
│   ├── INDEX.md              # Single source of truth: command → reference file mapping
│   ├── course-profiles.md    # Course snapshot, multi-course handling, persistence
│   ├── materials-ingestion.md# Ingesting PDFs/PPTs/notes/past papers
│   ├── subject-adaptation.md # Per-subject rigor, notation, and visuals
│   ├── interaction-modes.md  # Teaching modes (Socratic, examiner, cram, …)
│   ├── review-workflows.md   # ⚠ Compatibility redirect → see review-plans.md, practice-workflows.md, spaced-repetition.md, group-study.md
│   ├── review-plans.md       # /plan, /map, /cram, last-page sheets, heat maps
│   ├── practice-workflows.md # Active recall, /mock, /oral, /fix, /summary
│   ├── spaced-repetition.md  # /review-due, SRS files, due-date calculation
│   ├── group-study.md        # /group-quiz, turn-based groups, scoreboards
│   ├── question-types.md     # Question generation and grading rubrics
│   ├── visual-generation.md  # Diagrams, image/video API workflows
│   └── coding-demos.md       # Runnable code demos and algorithm traces
├── examples/                 # Worked sessions and sample artifacts
│   ├── sample-session.md     # Math analysis (paper exam) walkthrough
│   ├── sample-session-cs.md  # Data structures (machine-graded OJ) walkthrough
│   ├── sample-course-profile.md
│   └── sample-cards.md       # All supported flashcard formats
└── scripts/
    ├── export_flashcards.py  # Markdown → Anki/Quizlet CSV/TSV
    ├── snapshot.py           # Course snapshot save/load/list/set-active + state.json
    ├── srs.py                # Spaced-repetition init/update/due/list/set-active
    ├── validate_skill.py     # Skill package validation (commands, refs, stale checks)
    ├── package_check.py      # Unified entry point: runs validate_skill.py + all unit tests
    └── tests/                # Unit + CLI tests for all scripts
```

## Commands

Type a slash command or describe what you want in natural language. Full list and routing in `SKILL.md` → Command Routing and `references/INDEX.md`. Highlights:

| Stage | Commands |
|-------|----------|
| Setup | `/profile`, `/materials`, `/diagnose`, `/paper`, `/lab` |
| Plan | `/plan`, `/map` |
| Practice | `/quiz`, `/mock`, `/oral`, `/group-quiz`, `/grade`, `/fix` |
| Explain | `/explain`, `/visual`, `/video`, `/code-demo` |
| Track & Export | `/review-due`, `/flashcards`, `/summary`, `/resume` |
| Modes | `/mode`, `/cram`, `/help` |

## Flashcard export

```bash
# Single file
python scripts/export_flashcards.py cards.md cards.csv --deck "Final"

# Merge several per-topic files, dropping duplicates
python scripts/export_flashcards.py limits.md integrals.md all.csv --dedup

# Quizlet-friendly cloze expansion / TSV output
python scripts/export_flashcards.py cards.md out.csv --expand-cloze
python scripts/export_flashcards.py cards.md out.tsv --format tsv
```

See `examples/sample-cards.md` for every supported card format.

## Development

Run all validation checks and tests in one command:

```bash
python scripts/package_check.py
```

Or run them individually:

```bash
python scripts/validate_skill.py          # Structural checks and stale-reference detection
python -m unittest discover -s scripts/tests -v   # Unit and CLI tests
```

### Contributing notes

- **Commands** are the contract. When you add or rename one, update **both** `SKILL.md` → Command Routing **and** `references/INDEX.md` (the per-command map). INDEX.md is the single source of truth the model consults at runtime.
- **Reference files** are loaded lazily to save tokens. Keep each one focused on its topic and cross-link rather than duplicate.
- **Don't fabricate.** The skill's instructions forbid inventing exam content, lab data, or dates. Preserve that discipline in any new workflow.
- Keep example sessions in sync when command behavior changes.
