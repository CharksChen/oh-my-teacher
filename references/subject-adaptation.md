# Subject Adaptation

Adapt language, rigor, examples, and artifacts to the subject. If the subject is mixed, combine the closest profiles.

## Mathematics

Examples: mathematical analysis, calculus, linear algebra, abstract algebra, probability, statistics.

Use:

- Definitions before conclusions
- Theorem conditions and where they are used
- Proof skeletons, counterexamples, and standard templates
- Step-by-step derivations with no unexplained jumps
- Active recall: state definition, prove lemma, identify condition, construct counterexample

For mathematical analysis, emphasize epsilon-delta logic, sequences/functions, convergence criteria, continuity/differentiability/integrability conditions, and common proof patterns.

### LaTeX Rendering

At the start of a math course session, ask the user which LaTeX rendering target they need (rendered / plain-text), then set the **LaTeX** field in the Current Course Snapshot and keep it consistent for the rest of the session.

Default to LaTeX source for formulas, definitions, and derivations:

- Inline: `$f'(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}$`
- Display: `$$ \int_a^b f(x)\,dx = F(b) - F(a) $$`
- Theorems and aligned steps: use `aligned` / `cases` / `matrix` environments when needed.

When the target channel does not render LaTeX (plain chat clients, some flashcard apps, code blocks without math support), or if the user selects plain-text mode, offer this plain-text fallback:

- `f'(x) = lim_{h->0} [f(x+h) - f(x)] / h`
- `int_a^b f(x) dx = F(b) - F(a)`
- Spell out Greek letters (`epsilon`, `delta`, `nabla`) instead of `\epsilon`, `\delta`, `\nabla` if the channel strips them.

## Physics, Circuits, Signals, Control

Use:

- Physical intuition plus mathematical model
- Units and dimension checks
- Diagrams, graphs, state transitions, dynamic process explanations
- Formula applicability conditions
- Worked examples and variants

Prefer visual or animation support for motion, fields, oscillation, transforms, feedback loops, and circuit behavior.

## Programming and Computer Science

Examples: C, C++, Java, Python, data structures, algorithms, OS, networks, databases, software engineering.

Use:

- Ask or infer the learned language subset before using advanced features
- Give runnable minimal examples
- Emphasize edge cases, input/output, complexity, tests, and debugging
- Avoid advanced syntax unless known: e.g., in C++ avoid templates, lambdas, smart pointers, STL-heavy tricks, or advanced metaprogramming for beginners
- Explain code by state changes and invariants

For data structures/algorithms, use traces, diagrams, pseudocode, complexity reasoning, and small code demos.

For OS/networks/databases/software engineering, use mechanism diagrams, lifecycle/process flows, comparisons, and typical exam Q&A.

## Chemistry, Biology, Medicine

Use:

- Mechanism chains and process maps
- Structure/function relationships
- Tables for similar concepts
- Experiment controls, observations, and interpretation
- Memory hooks only after accurate definitions

Avoid vague analogies when precise mechanism matters.

## Economics, Management, Law, Politics, History, Literature

Use:

- Concept frameworks and comparison tables
- Essay templates and argument structures
- Case material, examples, and keywords
- Timeline/cause-effect diagrams where useful
- Active recall through short-answer and essay-outline prompts

Grade essays by thesis clarity, concept accuracy, structure, evidence, and course vocabulary.

## Foreign Language

Use:

- Vocabulary spaced review
- Grammar correction with compact rules
- Translation drills
- Listening/speaking scripts when relevant
- Writing templates and sentence upgrades

For oral practice, use examiner mode and give expression feedback.

## Design, Drawing, Engineering Graphics, Art

Use:

- Visual standards and process checklists
- Step-by-step construction
- Error inspection and comparison
- Rubric-based review of user work

Prefer diagrams or image prompts when visual inspection matters.

## Engineering (Mechanical, Civil, Electrical, Chemical, Industrial)

Use:

- Schematics, circuit diagrams, process flow diagrams, P&IDs, free-body diagrams, stress/strain plots
- Step-by-step design calculations with units, safety factors, and code/standard references
- Comparison tables for material properties, component selection, and design alternatives
- Lab/field measurement procedures, instrument selection, and uncertainty propagation
- Code or standard clause lookup exercises: identify the governing clause, interpret requirements

Prefer visual support for mechanisms, structural behavior, circuit operation, and process dynamics. For design courses, emphasize iteration between calculation and drawing.

## Clinical Medicine, Nursing, Dentistry, Pharmacy

Use:

- Clinical reasoning chains: history → differential → investigation → diagnosis → management
- Anatomy/pathology diagrams and labeled illustrations
- Drug mechanism, pharmacokinetics, interaction, and dosage calculation tables
- Procedure checklists and step-by-step protocols (OSCE-style)
- Case-based questions with progressive disclosure
- Ethical and communication scenario role-play

For clinical exams (OSCE, viva, written case), emphasize structured answer templates (e.g., SOAP notes, surgical safety checklist). Avoid substituting clinical judgment — always note that answers are for study purposes only.
