# Research / writing pack

Assembles a team for a research paper, essay, thesis, report, literature review,
white paper, article, grant, or book chapter — any work whose product is a
written argument backed by evidence.

## When this pack is selected (detection cues)

paper, essay, thesis, dissertation, article, report, study, manuscript, review,
white paper, grant, book/chapter — or the folder already contains `.md`/`.tex`/
`.docx` prose, a bibliography, or a citations file and no source tree.

## Lifecycle vocabulary + completeness signals (mechanical)

| Phase | Means | Completeness signal the CEO checks |
|---|---|---|
| Spec | the brief / research question | `spec.md` has headings *Founding Bet, Question, Success Criteria, Scope* |
| Plan | the method & sources plan | `plan.md` exists AND every task line carries a `(BET: ...)` tag |
| Build (Draft) | the draft | `draft.md` exists AND `git status --porcelain` is empty (committed) |
| Verify | fact & citation check | `citations-checked.md` (or `verify-notes.md`) exists with per-claim source + pass/fail |
| Review | editorial review | `review.md` has ≥1 section per assigned specialist |
| Ship | submit / publish | every assigned specialist signed off in `review.md` AND `dist/` has the exported doc newer than the last commit |

## The five steering questions (research phrasing)

```
Q1. Primary surface of risk? (inaccuracy / misrepresentation of sources /
    reader confusion / weak argument / plagiarism-ethics / none obvious)
Q2. Does it make external/empirical claims or rely on cited sources or data? (yes / no)
Q3. Is there a defined readership it must land with? (peer reviewers / general / none)
Q4. Is accuracy critical — does one wrong claim discredit the work? (yes / no)
Q5. Does it need a deliberate argument structure (thesis, claim hierarchy)? (yes / no)
```

## Answer → archetype → role binding

| Condition | Archetype | Role skill |
|---|---|---|
| *always* | CEO | `helm-orchestrator` |
| *always* | Counterweight | `helm-counterweight` |
| *always* | Bet Keeper | `helm-product-keeper` |
| *always* | Maker | `helm-writer` |
| Q2 = yes **OR** Q1 = misrepresentation | Integrity (Plan, Draft) | `helm-sources-reviewer` |
| Q4 = yes **OR** Q1 = inaccuracy | Verification (Draft) | `helm-fact-checker` |
| Q3 has a defined readership | Audience (Review) | `helm-reader-advocate` |
| Q5 = yes | Structure (Plan) | `helm-argument-architect` |
