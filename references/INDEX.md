# References Index

Load the relevant reference file(s) before executing any command. This index is the single source of truth for command routing, command descriptions, and environment fallbacks.

## Load Order

| Priority | File | Purpose | Load When |
|----------|------|---------|-----------|
| 1 | `course-profiles.md` | Current Course Snapshot, multi-course handling, persistence format | `/profile`, `/materials`, `/diagnose`, `/plan`, `/map`, `/mock`, `/grade`, `/fix`, `/quiz`, `/oral`, `/group-quiz`, `/summary`, `/resume`, course switch |
| 2 | `environment-adaptation.md` | Detect host capabilities and choose fallbacks | Any task involving files, retrieval, shell/scripts, persistence, citations, visuals, code demos, exports, or unknown host |
| 3 | `materials-ingestion.md` | Ingest PDFs, PPTs, notes, past papers; extract knowledge inventory and gaps | `/materials` or when user uploads course files |
| 4 | `subject-adaptation.md` | Adapt rigor, notation, examples, and visuals per subject family | Any review task after course profile is built |
| 5 | `interaction-modes.md` | Select teaching mode: Socratic, examiner, cram, etc. | Before generating questions, explanations, feedback, or mode switches |
| 6 | `learning-strategies.md` | Evidence-informed learning strategies and selection rules | `/plan`, `/quiz`, `/fix`, `/socratic`, `/feynman`, `/flashcards`, or when choosing how to study |
| 7 | `ima-adaptation.md` | ima-native tool, memory, note, knowledge-base, report, and PPT routing | Host is ima, user mentions ima/知识库/笔记, or tools include ask_user/fetch/search/memory/use_skill |
| 8 | `chinese-routing.md` | Chinese natural-language trigger mapping | Chinese request has no slash command or implies an ima-native learning workflow |

Only load files from `examples/` when the user asks for sample sessions, example outputs, behavior comparisons, or regression/reference behavior.

## Command Catalog and Reference Map

| Command | Description | Primary Reference | Secondary References |
|---------|-------------|-------------------|---------------------|
| `/help` | List commands with one-line descriptions and usage examples, grouped by stage | This index | - |
| `/profile` | Build a course profile and ask only essential missing questions | `course-profiles.md` | `course-templates.md`, `scripts/course_templates.py` |
| `/materials` | Ingest uploaded or pasted course files; summarize, update profile, list gaps | `materials-ingestion.md` | `course-profiles.md`, `environment-adaptation.md` |
| `/source-map` | Build a source-grounded map of course materials, coverage, high-value sources, gaps, and citation anchors | `ima-adaptation.md` | `materials-ingestion.md`, `review-plans.md` |
| `/paper` | Optimize review for closed-book or open-book paper exams | `course-profiles.md` | `subject-adaptation.md` |
| `/paper-analyze` | Analyze past papers, sample finals, homework sets, and question banks | `exam-paper-analysis.md` | `ima-adaptation.md`, `course-profiles.md` |
| `/teacher-emphasis` | Extract teacher emphasis from slides, messages, review notes, starred/highlighted material, and Q&A | `ima-adaptation.md` | `materials-ingestion.md`, `review-plans.md` |
| `/lab` | Optimize review for lab exams, experiments, reports, and viva questions | `course-profiles.md` | `subject-adaptation.md` |
| `/diagnose` | Run a 5-question rapid assessment across top chapters | `question-types.md` | `course-profiles.md`, `practice-workflows.md` |
| `/plan` | Generate a realistic 1/3/7/14/30-day review plan | `review-plans.md` | `course-profiles.md`, `subject-adaptation.md` |
| `/map` | Produce a concept map, exam map, formulas, definitions, and priorities | `review-plans.md` | `course-profiles.md` |
| `/explain [topic]` | Explain a single concept with definition, intuition, example, and recall prompt | `subject-adaptation.md` | `interaction-modes.md` |
| `/socratic [topic]` | Socratic tutoring: one focused question at a time, hint ladder, assumptions, counterexamples, and student summary | `socratic-mode.md` | `interaction-modes.md`, `learning-strategies.md`, `subject-adaptation.md` |
| `/feynman [topic]` | Feynman technique: student teaches, AI plays curious freshman, then grades the explanation | `feynman-mode.md` | `interaction-modes.md`, `subject-adaptation.md` |
| `/quiz` | Drill with adaptive questions | `question-types.md` | `interaction-modes.md`, `subject-adaptation.md`, `course-profiles.md` |
| `/mock` | Generate a timed mock final with answers and rubric | `practice-workflows.md` | `question-types.md`, `course-profiles.md` |
| `/oral` | Rehearse an oral exam with progressive questions and feedback | `practice-workflows.md` | `interaction-modes.md`, `subject-adaptation.md` |
| `/grade` | Grade a user answer and diagnose mistakes | `question-types.md` | `course-profiles.md`, `practice-workflows.md`, `spaced-repetition.md` |
| `/fix` | Repair weak points with mini-lessons and variant questions | `practice-workflows.md` | `question-types.md`, `subject-adaptation.md` |
| `/flashcards` | Create active-recall cards; export CSV/TSV with `scripts/export_flashcards.py` when requested | `SKILL.md` | `practice-workflows.md`, `learning-strategies.md`, `environment-adaptation.md` |
| `/review-due` | Check spaced-repetition schedule and list topics due today | `spaced-repetition.md` | `course-profiles.md` |
| `/group-quiz` | Run a multi-student quiz session | `group-study.md` | `question-types.md`, `subject-adaptation.md` |
| `/visual` | Create diagrams, image prompts, or visual explanations | `visual-generation.md` | `subject-adaptation.md`, `environment-adaptation.md` |
| `/video` | Create storyboard, animation plan, or video API workflow | `visual-generation.md` | `environment-adaptation.md` |
| `/code-demo` | Create runnable code demos or algorithm visualizations | `coding-demos.md` | `subject-adaptation.md`, `environment-adaptation.md` |
| `/cram` | Use exam-near rescue mode and prioritize scoring yield | `review-plans.md` | `interaction-modes.md` |
| `/last-page` | Generate the final one-page exam sheet: formulas, templates, traps, timing, and submission checks | `review-plans.md` | `ima-adaptation.md`, `materials-ingestion.md` |
| `/dashboard` | Generate a Markdown review dashboard with status, heat map, due topics, risks, and next action | `review-plans.md` | `ima-adaptation.md`, `spaced-repetition.md`, `course-profiles.md` |
| `/resume` | Restore context from a pasted Course Snapshot block | `course-profiles.md` | - |
| `/summary` | Print a session digest: topics practiced, accuracy changes, weak points, SRS updates, and next step | `practice-workflows.md` | `course-profiles.md`, `spaced-repetition.md` |
| `/wrong-note` | Create a wrong-question note from grading, quiz, or mock feedback and sync SRS summary | `wrong-note.md` | `question-types.md`, `spaced-repetition.md`, `ima-adaptation.md` |
| `/report` | Generate a structured stage review or coverage report through ima-report when available | `ima-adaptation.md` | `exam-paper-analysis.md`, `review-plans.md` |
| `/ppt` | Generate an exam-cram or wrong-question PPT through ima-ppt when available | `ima-adaptation.md` | `review-plans.md`, `wrong-note.md` |
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
| /source-map | Source-grounded material coverage map |
| /diagnose | Quick 5-question level assessment |
| /paper | Optimize for paper exams |
| /paper-analyze | Analyze past papers and question patterns |
| /teacher-emphasis | Extract teacher emphasis |
| /lab | Optimize for lab exams |

## Plan
| Command | Description |
|---------|-------------|
| /plan | Day-by-day review plan |
| /map | Concept map and exam priorities |
| /last-page | Final one-page exam sheet |
| /dashboard | Review dashboard |

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
| /socratic [topic] | Guided one-question-at-a-time tutoring |
| /feynman [topic] | Teach the concept back (Feynman technique) |
| /visual | Diagrams and visual explanations |
| /video | Storyboard or animation plan |
| /code-demo | Runnable code demo |

## Track & Export
| Command | Description |
|---------|-------------|
| /review-due | Spaced-repetition due today |
| /wrong-note | Create wrong-question note |
| /flashcards | Create and export flashcards |
| /summary | Session digest |
| /resume | Restore from pasted snapshot |
| /report | Stage review report |
| /ppt | Exam-cram PPT |

## Modes
| Command | Description |
|---------|-------------|
| /mode [name] | Switch interaction mode |
| /cram | Exam-near rescue mode |

Type any command or describe what you need in natural language.
```

## Environment Fallbacks

For detailed fallbacks, load `environment-adaptation.md`. This compact table is the routing overview:

| Command | Agent shell | RAG notebook | Notes app | Plain chat |
|---------|-------------|--------------|-----------|------------|
| `/materials` | Read files; use PDF/PPT/text tooling when available | Cite from document context | Ingest Markdown notes, backlinks, tags, pasted excerpts | Ask student to paste chapter text or OCR screenshots |
| `/flashcards` | Write Markdown, then run `scripts/export_flashcards.py` | Emit Markdown cards inline | Emit Markdown cards with tags/backlinks | Emit Markdown cards inline |
| `/visual` | Mermaid, HTML, Manim, Python plot, or image prompt as appropriate | Mermaid or ASCII inline | Mermaid/Markdown tables if supported; otherwise ASCII | ASCII diagrams or numbered step lists |
| `/video` | Storyboard plus Manim/HTML Canvas plan or file when tools exist | Storyboard inline | Storyboard Markdown | Storyboard inline only; never call video API |
| `/code-demo` | Write and run a file; show output | Code block plus expected output | Code block plus trace note | Code block plus expected output and walkthrough |
| `/plan` | Write `plan.md` when useful | Plan inline | Markdown plan with tags/backlinks | Plan inline plus copy/pin reminder |
| `/map` | Mermaid or Markdown file when useful | Mermaid or ASCII inline | Mermaid/Markdown concept map | ASCII concept map |
| `/mock` | Write `mock.md` and `answer.md` when useful | Mock inline | Mock as Markdown note | Mock inline with rubric |
| `/grade` | Read answer file and write graded artifact when useful | Grade inline with quotes/citations | Grade inline with `#错题` tags | Grade inline with quotes |
| `/explain`, `/socratic`, `/feynman`, `/quiz`, `/oral`, `/fix`, `/group-quiz` | Conversational by default | Conversational by default | Markdown-native conversational output | Conversational by default |

## File Overview

### `course-profiles.md`
Course profile construction and maintenance. Contains the Current Course Snapshot template, field update rules, paper/lab/coding/oral exam optimization, multi-course snapshots, and the exact on-disk snapshot format.

### `environment-adaptation.md`
Host capability detection and fallbacks for Codex, Claude Code, OpenClaw, Hermes, WorkBuddy, Qoder Work, NotebookLM, ima, Obsidian, notes apps, RAG notebooks, and ordinary chat boxes.

### `ima-adaptation.md`
ima-native runtime protocol covering 14 ima tools, 5 native skills, source levels, note-first persistence, knowledge-base retrieval, reports, PPT, and command overrides.

### `chinese-routing.md`
Chinese natural-language routing table for high-frequency study requests such as 老师划重点, 往年题分析, 整理错题, 今天该复习什么, and 复习 PPT.

### `materials-ingestion.md`
How to ingest course files. Covers PDF skill fallback, extraction targets, output contract, incremental ingestion, multi-file merging, and environment-specific ingestion.

### `subject-adaptation.md`
Subject-specific defaults for Mathematics, Physics, CS, Chemistry/Biology/Medicine, Economics/Law/History, Foreign Language, Design/Art, Engineering, and Clinical Medicine.

### `interaction-modes.md`
Teaching modes with selection rules, mixed-mode combinations, response contracts, and mode switching.

### `socratic-mode.md`
Detailed `/socratic` protocol: one focused question, hint ladder, assumption probes, counterexamples, student summary, and teacher close.

### `feynman-mode.md`
Detailed `/feynman` protocol: teach-back, curious freshman probing, grading, re-teach prompt, repair card, and SRS update.

### `learning-strategies.md`
Evidence-informed learning strategy guide: retrieval practice, spacing, interleaving, elaboration, self-explanation, concrete examples, dual coding, pretesting, and analogical comparison.

### `review-plans.md`
Study maps, review plans, cram mode, progress heat maps, and last-page sheets.

### `exam-paper-analysis.md`
Past-paper analysis workflow for question distribution, high-frequency topics, scoring patterns, evidence scope, and ima note updates.

### `practice-workflows.md`
Active recall, mock exams, error repair, oral rehearsal, and session summaries.

### `spaced-repetition.md`
SRS files, due-date calculation, `/review-due`, and automatic SRS updates.

### `wrong-note.md`
Wrong-question note template and ima workflow for turning graded mistakes into durable note and SRS assets.

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

### `course-templates.md`
Pre-built course profiles for quick onboarding via `scripts/course_templates.py`. Contains six common university course templates (数据结构与算法, 数学分析, 线性代数, 计算机网络, 操作系统, 大学物理).
