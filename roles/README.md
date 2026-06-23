# roles/ — role library

As of **v1.1**, the original software role stubs (Engineer, QA/Test, UX Reviewer,
Architect, Product Keeper) are **all built** and live under `skills/` as
auto-invoked specialists. The deterministic selection table in
`skills/helm-onboarding/SKILL.md` assigns them; the gate table in
`skills/helm-orchestrator/SKILL.md` fires them.

| Role | Built skill | Assigned when | Fires at |
|---|---|---|---|
| Orchestrator (CEO) | `helm-orchestrator` | always | coordinates every gate |
| Counterweight | `helm-counterweight` | always | Spec, Verify, and the ≥9 check |
| Product Keeper | `helm-product-keeper` | always | Plan, Review |
| Engineer | `helm-engineer` | always | routed during Build (implementer, not a gate reviewer) |
| Security Reviewer | `helm-security-reviewer` | `Q2 = yes` OR `Q1 = security` | Plan, Build |
| QA / Test | `helm-qa-test` | `Q4 = yes` OR `Q1 = correctness` | Build |
| UX Reviewer | `helm-ux-reviewer` | `Q3 = web` | Review |
| Architect | `helm-architect` | `Q5 = yes` | Plan |

## Domain packs (v1.1)

HELM is domain-agnostic. A domain-neutral core (CEO, Counterweight, Product
Keeper) plus a **Maker** and four **reviewer archetypes** (Integrity,
Verification, Audience, Structure) are bound to concrete role skills by the
active **pack**. Onboarding detects the domain, confirms it, and loads the pack.

| Pack | `pack.md` | Maker | Integrity | Verification | Audience | Structure |
|---|---|---|---|---|---|---|
| software (default) | `software/pack.md` | Engineer | Security Reviewer | QA / Test | UX Reviewer | Architect |
| research-writing | `research-writing/pack.md` | Writer | Sources Reviewer | Fact-Checker | Reader Advocate | Argument Architect |
| business-product | `business-product/pack.md` | Operator | Compliance Reviewer | Evidence Checker | Stakeholder Reviewer | Strategy Architect |

Each `pack.md` defines the domain's detection cues, its lifecycle vocabulary +
mechanical completeness signals, its five steering questions, and the
answer→archetype→role binding. The five risk dimensions and the mapping logic are
identical across packs — only the wording, the bound roles, and the gate signals
change.

To build a new role: create `skills/helm-<role>/SKILL.md` with frontmatter
(`name`, `description`), fill every anatomy section using
`skills/helm-security-reviewer/SKILL.md` as the reference (perspective · the
standard it holds · when it fires · method/checklist · cross-team tensions ·
evidence required to exit · anti-rationalization table), wire its row into
`helm-orchestrator` and `helm-router`, and keep `smoke-test/run_smoke_test.py` in
lockstep.
