````markdown

Your task is to perform the actual refactoring of the handbook by inserting pedagogical `tcolorbox` blocks into the session files, using the approved plan in:

`editorial_reports/box/planning.md`

## Primary objective

Read the planning document carefully and execute the refactoring it specifies across the handbook source files.

You must update the LaTeX content of the session files directly.

## Source layout

Each session has its own folder, and the main LaTeX file for each session is located inside that folder.

Examples:
- `session1/session1.tex`
- `session2/session2.tex`
- `session3/session3.tex`
- `session4/session4.tex`
- `session5_and_6/session5_and_6.tex`
- `session7/session7.tex`
- `session8/session8.tex`
- `session9/session9.tex`
- `session10/session10.tex`
- `session11/session11.tex`
- `session12/session12.tex`

Treat `session5_and_6/session5_and_6.tex` as covering both Session 5 and Session 6.

## Required behavior

1. Read `editorial_reports/box/planning.md` first.
2. Use it as the authoritative editorial plan.
3. Insert the proposed pedagogical boxes into the LaTeX files for Sessions 1–12.
4. Follow the planned:
   - insertion points,
   - box titles,
   - draft content,
   - continuity notes,
   - implementation guidance.
5. Preserve the intent, tone, and pedagogical flow of the handbook.
6. Keep all edits consistent with the existing terminology, notation, and technical framing of the handbook.

## Box format

Use this exact LaTeX structure:

```latex
\begin{tcolorbox}[title=Goal]
...
\end{tcolorbox}
````

Valid titles are only:

* `Goal`
* `Checkpoint`
* `Common Mistakes`
* `Hint`

Do not invent additional box titles.

## Editing rules

* Insert boxes only where justified by the plan.
* Do not add filler boxes.
* Do not rewrite large sections unnecessarily.
* Do not remove important existing content unless a very small local adjustment is needed to integrate a box cleanly.
* Preserve section headings, labels, references, tables, inputs, and overall document structure.
* Avoid inserting boxes inside fragile environments such as:

    * `table`
    * `tabular`
    * `tabularx`
    * `enumerate`
    * `itemize`
    * other float or nested environments
* If the planned insertion point falls inside such an environment, place the box immediately before or after the environment at the nearest safe location.
* Keep LaTeX compilable.

## Continuity requirements

The plan is cross-chapter by design. Maintain those links while editing.

Examples:

* Earlier choices should visibly support later sessions.
* A `Goal` may prepare students for the next session.
* A `Checkpoint` should verify outputs needed later.
* A `Common Mistakes` box should prevent errors that would weaken later work.
* A `Hint` should connect current work to earlier decisions or upcoming tasks.

## File-by-file scope

You must refactor all relevant session files:

* Session 1 → `session1/session1.tex`
* Session 2 → `session2/session2.tex`
* Session 3 → `session3/session3.tex`
* Session 4 → `session4/session4.tex`
* Sessions 5 & 6 → `session5_and_6/session5_and_6.tex`
* Session 7 → `session7/session7.tex`
* Session 8 → `session8/session8.tex`
* Session 9 → `session9/session9.tex`
* Session 10 → `session10/session10.tex`
* Session 11 → `session11/session11.tex`
* Session 12 → `session12/session12.tex`

## Quality bar

Your edits must be:

* grounded in `editorial_reports/box/planning.md`,
* pedagogically useful,
* concise,
* natural in context,
* consistent across the handbook,
* practical for real student use.

## Output expectation

Modify the LaTeX files directly.

After editing, provide a concise completion summary that includes:

* which files were updated,
* whether any planned insertions had to be shifted slightly for LaTeX safety,
* any plan items you could not implement exactly as written.

```

