# HELM

**HELM orchestrates a project-specific AI team — you are the MD, HELM is the CEO,
and specialists are auto-invoked at lifecycle gates.**

You decide; a coordinator routes; specialists do the work — and the coordinator
pulls in the right specialist *automatically* at the right moment, with
deterministic rules instead of vibes.

This repo is **the method, as markdown skills**. There is no service to run and
no registry package. The skills *are* the product. Drop them into Claude Code,
Cursor, or any host that reads markdown instructions, and you have HELM.

> Everything is **local**. No telemetry, no server, no account. Every decision is
> logged to `.helm/decisions.jsonl` inside your own project repo — auditable,
> yours, and nowhere else.

## Install

### Claude Code — marketplace (primary)

```text
/plugin marketplace add sykoramade/helm-skill
/plugin install helm@helm-skill
```

The short form `sykoramade/helm-skill` resolves over **HTTPS**. If you prefer the
explicit URL it's the same source:

```text
/plugin marketplace add https://github.com/sykoramade/helm-skill.git
/plugin install helm@helm-skill
```

> **SSH-keys gotcha:** the marketplace fetch uses **HTTPS**, so it works with no
> SSH keys configured. If you instead `git clone` the repo by hand, use the
> **HTTPS** URL above unless you have SSH keys set up for GitHub — an
> `git@github.com:…` clone will fail without them.

### Troubleshooting

**`Permission denied (publickey)` or `Host key verification failed` on install.**
A fresh install with the manifest above clones over HTTPS and should never hit
this. If an **older install** (cached from before this fix) still tries to clone
over SSH, force git to rewrite SSH GitHub URLs to HTTPS, then retry:

```bash
git config --global url."https://github.com/".insteadOf "git@github.com:"
```

This needs no auth for a public repo and works on a machine with no SSH keys.

### Claude Code — dev path (local, no marketplace)

Point Claude Code straight at a local checkout while you iterate:

```bash
git clone https://github.com/sykoramade/helm-skill.git
claude --plugin-dir ./helm-skill
```

### Cursor

Cursor reads rules from `.cursor/rules/`. Convert each skill into a rule:

```bash
mkdir -p .cursor/rules
for s in skills/*/SKILL.md; do
  name=$(basename "$(dirname "$s")")
  cp "$s" ".cursor/rules/${name}.mdc"
done
```

Then reference a rule in chat with `@helm-onboarding` (or set the orchestrator to
always-apply).

### Any other host (Windsurf, Cline, plain system prompt, …)

These skills are just markdown — paste `skills/helm-onboarding/SKILL.md` (to start
a project) or `skills/helm-orchestrator/SKILL.md` (to run one) into the host's
system-prompt / rules / custom-instructions area, and keep the other skill files
available so they can be invoked when a gate fires.

## Quick start

Invoke HELM with:

```text
onboard a new project: <one-line description of what you're building>
```

Expect: **5 steering questions → a project-specific team → a plan → autonomous
lifecycle gates.** HELM reviews the folder, recommends a real **founding bet**,
assembles a team from an explicit *answer → role* table (you approve each step;
nothing is written until you do), then runs the project through
`spec → plan → build → verify → review → ship`, automatically invoking the right
specialist when each gate's mechanical signal is met.

## The model in one picture

```
   You (the MD)  ──talks only to──▶  HELM (the CEO/Orchestrator)
        ▲                                    │
        │ reports back                       │ autonomously invokes + routes
        │                                    ▼
        └──────────────  Specialists (Counterweight, Security Reviewer, …)
```

- **You (the MD)** decide. You can overrule, stop, or question anything.
- **HELM (the CEO)** coordinates and routes. It never writes the work itself and
  never bypasses the team. It is your **only** point of contact.
- **Specialists** do the work and report findings back through the CEO.

## What's in it — built wedge vs. v1.1 stubs

**Built (live in v1):**

```
skills/
  helm-onboarding/        Onboard a project: 5 questions -> a deterministic,
                          project-specific team + a real founding bet.
  helm-orchestrator/      The CEO. Coordinates the lifecycle and AUTONOMOUSLY
                          invokes specialists at mechanical phase gates.
  helm-counterweight/     Standing adversary. Argues against the dominant
                          assumption; challenges overconfidence (the
                          high-confidence check).
  helm-security-reviewer/ Audits networks / transfers / inputs / secrets.
  helm-router/            Meta-router: maps a phase or request -> the right role.
```

**Stubs (assigned today, personas land in v1.1):**

```
roles/                    Engineer, QA/Test, UX Reviewer, Architect,
                          Product Keeper — selected by the onboarding table now,
                          fleshed out as built skills in v1.1.
```

## Scope (honest)

**v1 assembles SOFTWARE-engineering teams.** Games, data, and hardware are **v1.1+
role libraries** — not built yet. v1 is the wedge: onboarding, the
Orchestrator/CEO, the Counterweight, the Security Reviewer, and the meta-router.

**Out of scope (v2, after adoption):** any learning corpus / lesson collection,
telemetry or central data collection, scoring/ranking systems, and a dashboard.
v1 is deliberately local-only — nothing to opt out of, nothing to trust us with.

## Prove it works

The pack must pass one load-bearing case: input *"a local-only browser-based
file-transfer tool"* must produce a team that **includes Security Reviewer with a
project-specific reason**, and the CEO must **auto-invoke it** at the Plan and
Build gates — not a generic trio, and not waiting to be asked.

```bash
python3 smoke-test/run_smoke_test.py    # runs from repo root, no dependencies, exits 0 on PASS
```

The script mirrors the selection and gate tables exactly, so it doubles as a
regression test. Full details in `smoke-test/file-transfer-test-case.md`.

## License

MIT — see `LICENSE`.
