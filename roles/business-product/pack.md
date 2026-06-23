# Business / product pack

Assembles a team for a business plan, strategy doc, market analysis,
go-to-market, pitch/investor deck, product spec/PRD, financial model, or
proposal — any work whose product is a decision-grade business document.

## When this pack is selected (detection cues)

business plan, strategy, market analysis, go-to-market, GTM, pitch deck,
investor deck, product spec, PRD, financial model, proposal, roadmap, business
case — or the folder already contains decks / models / a strategy doc and no
source tree.

## Lifecycle vocabulary + completeness signals (mechanical)

| Phase | Means | Completeness signal the CEO checks |
|---|---|---|
| Spec | the brief | `spec.md` has headings *Founding Bet, Problem, Success Criteria, Scope* |
| Plan | the approach plan | `plan.md` exists AND every task line carries a `(BET: ...)` tag |
| Build | build the deliverable | the deliverable file (e.g. `deliverable.md`) exists AND `git status --porcelain` is empty (committed) |
| Verify | evidence & numbers check | `evidence-check.md` exists with per-figure source + recompute/sensitivity pass/fail |
| Review | stakeholder review | `review.md` has ≥1 section per assigned specialist |
| Ship | finalize / deliver | every assigned specialist signed off in `review.md` AND `dist/` has the final deliverable newer than the last commit |

## The five steering questions (business phrasing)

```
Q1. Primary surface of risk? (financial misrepresentation / legal-compliance /
    stakeholder confusion / weak strategy / data accuracy / none obvious)
Q2. Does it make external commitments/claims or carry regulatory exposure? (yes / no)
Q3. Is there a specific decision-maker it must land with? (exec / investor / customer / none)
Q4. Is quantitative accuracy critical — does a wrong number mislead a real decision? (yes / no)
Q5. Does it need a deliberate strategic structure (thesis, dependent bets)? (yes / no)
```

## Answer → archetype → role binding

| Condition | Archetype | Role skill |
|---|---|---|
| *always* | CEO | `helm-orchestrator` |
| *always* | Counterweight | `helm-counterweight` |
| *always* | Bet Keeper | `helm-product-keeper` |
| *always* | Maker | `helm-operator` |
| Q2 = yes **OR** Q1 = legal-compliance | Integrity (Plan, Build) | `helm-compliance-reviewer` |
| Q4 = yes **OR** Q1 = data-accuracy | Verification (Build) | `helm-evidence-checker` |
| Q3 has a specific decision-maker | Audience (Review) | `helm-stakeholder-reviewer` |
| Q5 = yes | Structure (Plan) | `helm-strategy-architect` |
