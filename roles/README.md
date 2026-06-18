# roles/ — v1.1 role library (stubs)

These are the roles HELM can assign that are **not yet built**. They are real
parts of the deterministic selection table and the gate table — they get
assigned to teams and named in the manifest today — but their full personas land
in **v1.1**.

Until a role is built:

- Onboarding still assigns it (with a project-specific WHY) when the answers map
  to it, and records it in `.helm/team.md` with status `stub (v1.1)`.
- The Orchestrator's gate table still lists its row. In the wedge, that row is
  **inert**: the Orchestrator logs that the gate *would* fire and notes the role
  activates in v1.1, rather than silently skipping it.
- The Orchestrator covers the load-bearing part in the interim where it can
  (e.g. it enforces founding-bet discipline itself while Product Keeper is a
  stub).

Each stub below follows the **role persona anatomy** that every built role uses,
with the content left to v1.1:

```
name · perspective · the standard it holds · evidence required to exit ·
anti-rationalization table
```

To promote a stub to a built role: move it to `skills/helm-<role>/SKILL.md`, add
frontmatter (`name`, `description`), fill in every anatomy section (use
`skills/helm-security-reviewer/SKILL.md` as the reference), and flip its gate-row
status from `v1.1` to `LIVE` in `helm-orchestrator` and `helm-router`.

| Stub | Assigned when | Gate row it will activate |
|---|---|---|
| `engineer.md` | (implementation work — always needed once building starts) | Build (does the work routed by the CEO) |
| `qa-test.md` | `Q4 = yes` OR `Q1 = correctness` | Build → QA/Test |
| `ux-reviewer.md` | `Q3 = web` | (review of user-facing flows) |
| `architect.md` | `Q5 = yes` | (design review before build) |
| `product-keeper.md` | always | Plan → Product Keeper; Review → Product Keeper |
