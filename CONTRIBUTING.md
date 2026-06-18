# Contributing to HELM

Thanks for helping extend HELM. This pack ships a **built wedge** (five live
skills) and a set of **v1.1 role stubs** in `roles/`. The most common
contribution is promoting a stub to a built role.

## The one rule

**The smoke test must stay green.** It is the contract that proves the
load-bearing case still works. Run it from the repo root before and after any
change:

```bash
python3 smoke-test/run_smoke_test.py   # must exit 0
```

If your change touches team selection (`skills/helm-onboarding/SKILL.md`) or the
autonomous gate table (`skills/helm-orchestrator/SKILL.md`), the smoke test
mirrors those tables and must be kept in lockstep.

## Promoting a v1.1 stub to a built role

The stubs live as plain markdown in `roles/` (Engineer, QA/Test, UX Reviewer,
Architect, Product Keeper). To make one a live, auto-invoked skill:

1. **Move it into `skills/`** as its own skill directory:
   `roles/<role>.md` → `skills/helm-<role>/SKILL.md`.
2. **Add frontmatter** at the top of `SKILL.md`:
   ```yaml
   ---
   name: helm-<role>
   description: <one line — what this role does and when the Orchestrator invokes it>
   ---
   ```
3. **Fill the anatomy sections** to match the built skills (e.g.
   `helm-security-reviewer`): perspective, the standard it holds, what it does at
   each gate, the evidence required to exit, and an anti-rationalization table.
4. **Flip the gate row to LIVE** in both:
   - `skills/helm-orchestrator/SKILL.md` (the gate table), and
   - `skills/helm-router/SKILL.md` (the phase/request → role map).
   Change the role's status from a `stub (v1.1)` wedge row to a `LIVE` row.
5. **Keep `run_smoke_test.py` in lockstep** if you changed a selection or gate
   table the script mirrors, then re-run it (`exit 0`).

## Style

- Skills are markdown only — no build step, no runtime dependency.
- Keep deterministic tables deterministic: a role is selected or a gate fires
  because of an explicit rule, never a vibe.
- No telemetry, no network calls, no central service. HELM is local-only.

## License

By contributing you agree your contributions are licensed under the MIT License.
