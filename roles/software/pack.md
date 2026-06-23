# Software pack (default)

The reference pack. Assembles a software-engineering team. This is the **default**
when no other domain is detected, and the only pack the smoke test exercises.

## When this pack is selected (detection cues)

App, tool, service, API, library, CLI, web app, script, SDK, firmware — or the
folder already contains source files / package manifests (`package.json`,
`pyproject.toml`, `Cargo.toml`, `go.mod`, …).

## Lifecycle vocabulary + completeness signals (mechanical)

| Phase | Means | Completeness signal the CEO checks |
|---|---|---|
| Spec | the spec | `spec.md` has headings *Founding Bet, Problem, Success Criteria, Scope* |
| Plan | the plan | `plan.md` exists AND every task line carries a `(BET: ...)` tag |
| Build | the implementation | `git status --porcelain` empty AND the build command exits 0 |
| Verify | the tests | the test command exits 0 AND output captured (results file / coverage / pass-fail log) |
| Review | the review | `review.md` has ≥1 section per assigned specialist |
| Ship | the release | every assigned specialist signed off in `review.md` AND `dist/` has files newer than the last commit |

## The five steering questions (the shared risk dimensions, software phrasing)

```
Q1. Primary surface of risk? (data loss / security / user confusion /
    performance / correctness / legal / none obvious)
Q2. Touches external systems, networks, or file transfer? (yes / no)
Q3. User-facing interface? (CLI / web / API / none)
Q4. Is correctness critical — does one mistake cause harm? (yes / no)
Q5. Custom protocols, multi-service coordination, or data-pipeline design? (yes / no)
```

## Answer → archetype → role binding

| Condition | Archetype | Role skill |
|---|---|---|
| *always* | CEO | `helm-orchestrator` |
| *always* | Counterweight | `helm-counterweight` |
| *always* | Bet Keeper | `helm-product-keeper` |
| *always* | Maker | `helm-engineer` |
| Q2 = yes **OR** Q1 = security | Integrity (Plan, Build) | `helm-security-reviewer` |
| Q4 = yes **OR** Q1 = correctness | Verification (Build) | `helm-qa-test` |
| Q3 = web | Audience (Review) | `helm-ux-reviewer` |
| Q5 = yes | Structure (Plan) | `helm-architect` |
