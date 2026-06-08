# Materials Ingestion

Use when the user uploads or references course files: PDFs, PPTs, notes, homework, lab manuals, or past papers.

## Before Processing

1. Read `references/course-profiles.md` if no course profile exists yet.
2. For PDF files, use the `pdf` skill to extract text and structure before summarizing.
3. For images of notes or slides, read the image directly when available.

## PDF Skill Fallback

The `pdf` skill may not be available in every environment. Before relying on it, check whether the skill is loaded; if not, fall back in this order:

1. `pdftotext` (poppler-utils) from the command line for text-based PDFs.
2. Ask the user to paste the relevant chapter/section text directly.
3. For scanned/image-only PDFs, ask the user to re-export with OCR enabled, or to provide the original source (slides, photos of notes).
4. Never fabricate missing pages, equations, or figures just because the PDF could not be read — say so explicitly and add the missing material to the gap list.

## Extraction Targets

From each material, extract:

- Chapters or lecture units and their order
- Definitions, theorems, formulas, and standard templates
- Likely question types and repeated exam patterns
- Teacher emphasis, starred topics, or "will be on the exam" notes
- Lab steps, instruments, safety notes, or report requirements when relevant
- Gaps: missing past papers, missing answer keys, unclear assessment scope

## Output Contract

After `/materials`, produce this exact section structure so `/map`, `/plan`, and `/quiz` can reuse the result:

```markdown
## Materials Inventory
[Files/snippets ingested, what each contributes, unreadable items]

## Exam-Relevant Topics
[High-yield topics, must-memorize items, likely question types, teacher emphasis]

## Missing Materials
[Past papers, syllabus, answer keys, lab rubric, unreadable pages, low-confidence areas]

## Priority Map
[Topic -> priority -> exam action -> confidence]

## Updated Course Snapshot Fields
[Materials, Weak points if any, Next recommended]

## Next Action
[Usually /map, /plan, or /quiz on the highest-priority gap]
```

Do not generate a full mock exam immediately after ingestion unless the user asks. Build the map first.

## Materials Missing or Too Thin

When the user gives little or no material (for example, "help me review calculus"):

1. Build a temporary low-confidence course profile from the course name and common curriculum.
2. Start with `/diagnose` rather than a detailed plan.
3. Mark `Materials` as `low-confidence / no syllabus yet` in the Current Course Snapshot.
4. Ask for the syllabus, chapter list, teacher emphasis, or past paper after giving the first useful diagnostic step.
5. Revise the map once real materials arrive; do not present generic chapter coverage as confirmed exam scope.

## Incremental Ingestion

When materials already exist in the Current Course Snapshot and the user provides additional files or content:

1. **Do not repeat** the existing material summary. Only report what is new or changed.
2. **Merge** the new content into the existing knowledge inventory by topic, not by file order.
3. **Flag** any conflicts between the new material and previously ingested content (e.g., a formula that differs between two sources).
4. **Update** the gap list: remove gaps that the new material fills, and add any new gaps the new material reveals (e.g., a new chapter with no corresponding past-paper coverage).
5. **Refresh** the `Materials` and `Next recommended` fields in the Current Course Snapshot.
6. If the new material covers topics already in the inventory, note the overlap briefly and skip redundant summaries.

## Multi-File Handling

When multiple files arrive:

- Merge by chapter/topic, not by file order
- Flag conflicts between sources
- Prefer past papers and teacher slides over generic textbook ordering for exam weighting
- Note duplicate coverage and skip redundant summaries

## Ingestion by Environment

The ingestion step looks very different depending on what the host can actually read.

- **Agent shell**: read files directly from disk, run the `pdf` skill, OCR images with the `pdf` or `image` skill. Build a chapter index from filenames and headings. This is the default assumed above.
- **RAG notebook**: the model already has the document context preloaded. Skip the file-reading step. Treat the student's pasted snippets as the unit of work and cite the source after each extraction. If the student does not paste, ask them to point at the section ("第三章 极限" or "the section on epsilon-delta definitions") rather than asking for the file.
- **Plain chat**: there are no files. Ask the student to:
  1. Paste the relevant chapter text directly (limit to one topic at a time to keep context).
  2. Send a photo of handwritten notes or a slide screenshot — the model can read the image inline.
  3. Send a PDF page-by-page as images, not as the PDF itself, if the chat client cannot accept PDFs.
  4. For very long materials, work in passes: first the table of contents + chapter titles, then the chapters in priority order.

After ingestion in a plain chat, the model should always echo back a compact material summary so the student can confirm "yes, this is what I sent" before any review work begins.
