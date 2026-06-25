```                        
██╗  ██╗███████╗██╗     ███╗   ███╗      ███████╗██╗  ██╗██╗██╗     ██╗     
██║  ██║██╔════╝██║     ████╗ ████║      ██╔════╝██║ ██╔╝██║██║     ██║     
███████║█████╗  ██║     ██╔████╔██║█████╗███████╗█████╔╝ ██║██║     ██║     
██╔══██║██╔══╝  ██║     ██║╚██╔╝██║╚════╝╚════██║██╔═██╗ ██║██║     ██║     
██║  ██║███████╗███████╗██║ ╚═╝ ██║      ███████║██║  ██╗██║███████╗███████╗
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚═╝      ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
                                                                            
```

**Run a multiple projects within AI organization where you're the boss.**

You're the MD. HELM is the CEO. Teams are spun up for new projects and specialists do the work — and the CEO pulls in the
right one *automatically* at each stage, on fixed rules instead of guesswork.

It's just markdown. No service, no account, no telemetry. Every decision is logged
to `.helm/decisions.jsonl` in your own repo — yours, auditable, and nowhere else.

---

## Install (Claude Code)
Due to SSH issues with CC, input this to cache keys
```text
ssh -o StrictHostKeyChecking=accept-new -T git@github.com
```
Then run
```text
/plugin marketplace add sykoramade/helm-skill
/plugin install helm@helm-skill
```

Once installed - type "onboard" and follow the instructions.

## Start a project

```text
onboard a new project: <one line on what you're building>
```

You get: **a few steering questions → a project-specific team → a plan → automatic
review gates.** HELM reads the folder, proposes a real *founding bet*, builds the
team from an explicit answer→role table (you approve each step — nothing is written
until you do), then runs `spec → plan → build → verify → review → ship`, calling
the right specialist the moment each gate's signal is met.

## How it works

```
   You (the MD)  ──talk only to──▶  HELM (the CEO)
        ▲                                │
        │ reports back                   │ routes + auto-invokes specialists
        │                                ▼
        └──────────────  Specialists (Counterweight, Security, QA, …)
```

- **You** decide. Overrule, stop, or question anything.
- **The CEO** coordinates and routes. It never does the work itself, never skips
  the team, and is your only point of contact.
- **Specialists** do the work and report back through the CEO — each with its own
  standard and a built-in tension (QA's "green ≠ verified" pushes the engineer's
  "it's done").

## The team

```
helm-onboarding       Turn one line into a team + a founding bet.
helm-orchestrator     The CEO. Runs the lifecycle, fires the gates.
helm-router           Maps a phase or request to the right specialist.
helm-operating-rule   Standing defaults: delegate grunt work, guard scope, one portfolio root.
helm-update-check     Checks for a newer HELM on startup, recommends the update.

helm-counterweight    Argues against your dominant assumption. Fires at Spec, Verify.
helm-product-keeper   Guards the founding bet, cuts scope drift. Fires at Plan, Review.
helm-engineer         Builds the work and applies every fix. Routed during Build.
helm-architect        System design — boundaries, protocols, failure modes. Plan.
helm-qa-test          Walks the unhappy path. Green ≠ verified. Build.
helm-security-reviewer Audits networks, transfers, inputs, secrets. Plan, Build.
helm-ux-reviewer      The first-time user's advocate. Review.
helm-model-router     Optional: routes routine work to cheaper/local models.
```

The CEO turns specialist findings into short, plain updates — depth only when you
ask for it.

## Not just software

A neutral core (CEO, Counterweight, Product Keeper) plus a maker and four reviewer
archetypes bind to real roles through the active **pack**. Onboarding detects the
domain and confirms it:

- **software** — Engineer · Security · QA · UX · Architect
- **research-writing** — Writer · Sources · Fact-Checker · Reader Advocate · Argument Architect
- **business-product** — Operator · Compliance · Evidence · Stakeholder · Strategy Architect

Same engine, same gates. A project can be a paper or a business plan, not only code.

## One CEO across multiple projects

Nest projects under a portfolio root, each with its own `.helm/`. The **Portfolio
CEO** sits above them, reads each decision log, and tells you what needs you now —
`NEEDS-MD`, `BLOCKED`, `STALE`, or `ON-TRACK` — in priority order, plus the
cross-project risks no single project can see. You talk to one point of contact to manage all your projects.

## Bring your own models (optional)

`helm-model-router` sends routine, low-risk work to the cheapest model that can do
it — your local Ollama for $0, a cheap hosted model, a frontier model as backup.
Declare a lineup in `helm-models.toml` (any OpenAI-compatible endpoint; keys read
from the environment, never stored):

```toml
[[model]]
id = "local-coder"
base_url = "http://localhost:11434/v1"
model_name = "qwen2.5-coder:14b"
local = true
```

Off by default, and **gate reviewers always run on your strongest model** — the
cheap tier drafts, it never gets a vote at a gate. See `skills/helm-model-router`.

## Other hosts

The skills are plain markdown — they work anywhere that reads instructions.

| Host | How |
|---|---|
| **Cursor** | `for s in skills/*/SKILL.md; do cp "$s" ".cursor/rules/$(basename $(dirname $s)).mdc"; done`, then `@helm-onboarding` in chat |
| **Windsurf / Cline** | Add `skills/helm-onboarding/SKILL.md` and `helm-orchestrator/SKILL.md` to the rules / custom-instructions area |
| **Plain system prompt** | Paste `helm-onboarding` to start, keep the other files available so gates can invoke them |

## Local-first, on purpose

No server, no telemetry, no account. **Out of scope (until v2):** any learning
corpus, central data collection, ELO scoring/ranking across agents and skills, or a dashboard view.

## Troubleshooting

- **Marketplace won't load.** Update it: `/plugin marketplace update helm-skill`,
  then `/reload-plugins`.

## What's new


- **v1.3** — **Operating rule** (`helm-operating-rule`): enforced defaults on cost
  (delegate grunt work, don't grind it inline), focus (every task traces to the
  founding bet or stops), and portfolio structure (one `helm-skill-portfolio/`
  root, every project a child, mandatory relocation for strays). **Startup update
  check** (`helm-update-check`): compares your installed version to the latest and
  recommends the one-line update — read-only, network-optional.
- **v1.2** — **Model routing** (`helm-model-router`): bring your own models and
  route routine work to the cheapest one that can do it; gate reviewers always run
  on your strongest model. **Locale/market guardrail**: HELM never silently assumes
  "US / English / USD" — it asks and writes `.helm/context.md`.
- **v1.1** — **Domain-agnostic core** with three packs (software · research-writing
  · business-product) bound through an explicit archetype→role table. The full
  specialist team built out as live skills. **Portfolio orchestration**: nest
  projects under a root with a Portfolio CEO above them. Concise, non-technical
  MD communication.
- **v1.0** — The HELM skill pack: onboarding → a project-specific team + founding
  bet, the Orchestrator (CEO) running `spec → plan → build → verify → review →
  ship` with autonomous review gates, and Claude Code marketplace manifests.

## License

MIT — see `LICENSE`.
