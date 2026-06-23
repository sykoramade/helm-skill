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

## What lives here next

This directory is reserved for the **domain-pack role libraries** (a later V1.1+
phase): a domain-neutral founding core plus selectable packs — `software/`,
`research-writing/`, `business-product/` — so HELM can assemble teams for a
research paper or a business plan, not just software. The software roles above
are the first, reference pack.

To build a new role: create `skills/helm-<role>/SKILL.md` with frontmatter
(`name`, `description`), fill every anatomy section using
`skills/helm-security-reviewer/SKILL.md` as the reference (perspective · the
standard it holds · when it fires · method/checklist · cross-team tensions ·
evidence required to exit · anti-rationalization table), wire its row into
`helm-orchestrator` and `helm-router`, and keep `smoke-test/run_smoke_test.py` in
lockstep.
