# Contributing to HELM

Thanks for helping extend HELM. As of **v1.1** the pack ships the **full
software team as ten live skills**. The most common contribution is adding a new
built role (e.g. for a future domain pack) or sharpening an existing one.

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

## Adding a new built role

To add a live, auto-invoked specialist:

1. **Create the skill directory** `skills/helm-<role>/SKILL.md`.
2. **Add frontmatter** at the top:
   ```yaml
   ---
   name: helm-<role>
   description: <one line — what this role does and when the Orchestrator invokes it>
   ---
   ```
3. **Fill every anatomy section** to match the built skills (use
   `skills/helm-security-reviewer/SKILL.md` as the reference): perspective, the
   standard it holds, when it fires (per gate), its method/checklist, its
   **cross-team tensions** (the productive friction it carries with the other
   roles), the evidence required to exit with explicit verdicts, and an
   anti-rationalization table.
4. **Wire it in** in both:
   - `skills/helm-orchestrator/SKILL.md` (the gate table), and
   - `skills/helm-router/SKILL.md` (the phase/request → role map).
   And, if it is selected by the steering answers, add its row to the mapping
   table in `skills/helm-onboarding/SKILL.md`.
5. **Keep `run_smoke_test.py` in lockstep** with any selection or gate table you
   touched, then re-run it (`exit 0`).

## Style

- Skills are markdown only — no build step, no runtime dependency.
- Keep deterministic tables deterministic: a role is selected or a gate fires
  because of an explicit rule, never a vibe.
- No telemetry, no network calls, no central service. HELM is local-only.

## License

By contributing you agree your contributions are licensed under the MIT License.
