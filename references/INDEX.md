# References Index

Load the relevant reference file(s) before executing any command. This index is the single source of truth for command routing, command descriptions, and environment fallbacks.

## Load Order

| Priority | File | Purpose | Load When |
|----------|------|---------|-----------|
| 1 | `course-profiles.md` | Current Course Snapshot, multi-course handling, persistence format | `/profile`, `/materials`, `/diagnose`, `/plan`, `/map`, `/mock`, `/grade`, `/fix`, `/quiz`, `/oral`, `/group-quiz`, `/summary`, `/resume`, course switch |
| 2 | `materials-ingestion.md` | Ingest PDFs, PPTs, notes, past papers; extract knowledge inventory and gaps | `/materials` or when user uploads course files |
| 3 | `subject-adaptation.md` | Adapt rigor, notation, examples, and visuals per subject family | Any review task after course profile is built |
| 4 | `interaction-modes.md` | Select teaching mode: Socratic, examiner, cram, etc. | Before generating questions, explanations, feedback, or mode switches |

Only load files from `examples/` when the user asks for sample sessions, example outputs, behavior comparisons, or regression/reference behavior.

## Command Catalog and Reference Map

| Command | Description | Primary Reference | Secondary References |
|---------|-------------|-------------------|---------------------|
| `/help` | List commands with one-line descriptions and usage examples, grouped by stage | This index | - |
| `/profile` | Build a course profile and ask only essential missing questions | `course-profiles.md` | - |
| `/materials` | Ingest uploaded or pasted course files; summarize, update profile, list gaps | `materials-ingestion.md` | `course-profiles.md` |
| `/paper` | Optimize review for closed-book or open-book paper exams | `course-profiles.md` | `subject-adaptation.md` |
| `/lab` | Optimize review for lab exams, experiments, reports, and viva questions | `course-profiles.md` | `subject-adaptation.md` |
| `/diagnose` | Run a 5-question rapid assessment across top chapters | `question-types.md` | `course-profiles.md`, `practice-workflows.md` |
| `/plan` | Generate a realistic 1/3/7/14/30-day review plan | `review-plans.md` | `course-profiles.md`, `subject-adaptation.md` |
| `/map` | Produce a concept map, exam map, formulas, definitions, and priorities | `review-plans.md` | `course-profiles.md` |
| `/explain [topic]` | Explain a single concept with definition, intuition, example, and recall prompt | `subject-adaptation.md` | `interaction-modes.md` |
| `/quiz` | Drill with adaptive questions | `question-types.md` | `interaction-modes.md`, `subject-adaptation.md`, `course-profiles.md` |
| `/mock` | Generate a timed mock final with answers and rubric | `practice-workflows.md` | `question-types.md`, `course-profiles.md` |
| `/oral` | Rehearse an oral exam with progressive questions and feedback | `practice-workflows.md` | `interaction-modes.md`, `subject-adaptation.md` |
| `/grade` | Grade a user answer and diagnose mistakes | `question-types.md` | `course-profiles.md`, `practice-workflows.md`, `spaced-repetition.md` |
| `/fix` | Repair weak points with mini-lessons and variant questions | `practice-workflows.md` | `question-types.md`, `subject-adaptation.md` |
| `/flashcards` | Create active-recall cards; export CSV/TSV with `scripts/export_flashcards.py` when requested | `SKILL.md` | `practice-workflows.md` |
| `/review-due` | Check spaced-repetition schedule and list topics due today | `spaced-repetition.md` | `course-profiles.md` |
| `/group-quiz` | Run a multi-student quiz session | `group-study.md` | `question-types.md`, `subject-adaptation.md` |
| `/visual` | Create diagrams, image prompts, or visual explanations | `visual-generation.md` | `subject-adaptation.md` |
| `/video` | Create storyboard, animation plan, or video API workflow | `visual-generation.md` | - |
| `/code-demo` | Create runnable code demos or algorithm visualizations | `coding-demos.md` | `subject-adaptation.md` |
| `/cram` | Use exam-near rescue mode and prioritize scoring yield | `review-plans.md` | `interaction-modes.md` |
| `/resume` | Restore context from a pasted Course Snapshot block | `course-profiles.md` | - |
| `/summary` | Print a session digest: topics practiced, accuracy changes, weak points, SRS updates, and next step | `practice-workflows.md` | `course-profiles.md`, `spaced-repetition.md` |
| `/mode [mode-name]` | Explicitly switch interaction mode for the current task | `interaction-modes.md` | - |

User commands override automatic mode selection for the current task only. Return to automatic mode afterward unless the user asks to stay in a mode.

### `/help` Output Template

When the user runs `/help`, use this exact structure:

```markdown
# Oh My Teacher — Commands

## Setup
| Command | Description |
|---------|-------------|
| /profile | Build a course profile |
| /materials | Ingest course files |
| /diagnose | Quick 5-question level assessment |
| /paper | Optimize for paper exams |
| /lab | Optimize for lab exams |

## Plan
| Command | Description |
|---------|-------------|
| /plan | Day-by-day review plan |
| /map | Concept map and exam priorities |

## Practice
| Command | Description |
|---------|-------------|
| /quiz | Adaptive drill |
| /mock | Timed mock exam |
| /oral | Oral exam rehearsal |
| /grade | Grade your answer |
| /fix | Repair weak points |
| /group-quiz | Multi-student quiz session |

## Explain
| Command | Description |
|---------|-------------|
| /explain [topic] | Explain one concept |
| /visual | Diagrams and visual explanations |
| /video | Storyboard or animation plan |
| /code-demo | Runnable code demo |

## Track & Export
| Command | Description |
|---------|-------------|
| /review-due | Spaced-repetition due today |
| /flashcards | Create and export flashcards |
| /summary | Session digest |
| /resume | Restore from pasted snapshot |

## Modes
| Command | Description |
|---------|-------------|
| /mode [name] | Switch interaction mode |
| /cram | Exam-near rescue mode |

Type any command or describe what you need in natural language.
```

## Environment Fallbacks

| Command | Agent shell | RAG notebook | Plain chat |
|---------|-------------|--------------|------------|
| `/materials` | Read files; use PDF/PPT/text tooling when available | Cite from document context | Ask student to paste chapter text or use OCR before continuing |
| `/flashcards` | Write Markdown, then run `scripts/export_flashcards.py` | Emit Markdown cards inline | Emit Markdown cards inline |
| `/visual` | Mermaid, HTML, Manim, Python plot, or image prompt as appropriate | Mermaid or ASCII inline | ASCII diagrams or numbered step lists; do not assume image API |
| `/video` | Storyboard plus Manim/HTML Canvas plan or file when tools exist | Storyboard inline | Storyboard inline only; never call video API |
| `/code-demo` | Write and run a file; show output | Code block plus expected output | Code block plus expected output; offer line-by-line walkthrough |
| `/plan` | Write `plan.md` when useful | Plan inline | Plan inline plus copy/pin reminder when needed |
| `/map` | Mermaid or Markdown file when useful | Mermaid or ASCII inline | ASCII concept map |
| `/mock` | Write `mock.md` and `answer.md` when useful | Mock inline | Mock inline with rubric in the same response |
| `/grade` | Read answer file and write graded artifact when useful | Grade inline with quotes | Grade inline with quotes |
| `/explain`, `/quiz`, `/oral`, `/fix`, `/group-quiz` | Conversational by default | Conversational by default | Conversational by default |

## File Overview

### `course-profiles.md`
Course profile construction and maintenance. Contains the Current Course Snapshot template, field update rules, paper/lab/coding/oral exam optimization, multi-course snapshots, and the exact on-disk snapshot format.

### `materials-ingestion.md`
How to ingest course files. Covers PDF skill fallback, extraction targets, output contract, incremental ingestion, multi-file merging, and environment-specific ingestion.

### `subject-adaptation.md`
Subject-specific defaults for Mathematics, Physics, CS, Chemistry/Biology/Medicine, Economics/Law/History, Foreign Language, Design/Art, Engineering, and Clinical Medicine.

### `interaction-modes.md`
Teaching modes with selection rules, mixed-mode combinations, response contracts, and mode switching.

### `review-plans.md`
Study maps, review plans, cram mode, progress heat maps, and last-page sheets.

### `practice-workflows.md`
Active recall, mock exams, error repair, oral rehearsal, and session summaries.

### `spaced-repetition.md`
SRS files, due-date calculation, `/review-due`, and automatic SRS updates.

### `group-study.md`
Group quiz setup, turn-based and buzzer-style sessions, scoreboards, and peer explanation rounds.

### `review-workflows.md`
Compatibility entry point that points to the narrower workflow files above.

### `question-types.md`
Adaptive difficulty, question generation defaults, paper exam types, programming types, lab types, and grading rubrics.

### `visual-generation.md`
Visual selection guide, environment-aware visual matrix, ASCII conventions, image prompt workflow, video storyboard workflow, and dynamic explanation defaults.

### `coding-demos.md`
Runnable demo guidelines: language inference, algorithm traces, data structure state, simulations, debugging, beginner constraints, animation choices, and environment-aware demo forms.
