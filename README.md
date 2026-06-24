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

```text
/plugin marketplace add sykoramade/helm-skill
/plugin install helm@helm-skill
```

That's it. Prefer clicking? Run `/plugin`, open **Discover**, pick **helm**, install.
After an update, run `/plugin marketplace update helm-skill` then `/reload-plugins`.

> Needs a recent Claude Code (`claude --version` ≥ 2.1.143). The fetch is over
> HTTPS — no SSH keys required.

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

## One CEO across many projects

Nest projects under a portfolio root, each with its own `.helm/`. The **Portfolio
CEO** sits above them, reads each decision log, and tells you what needs you now —
`NEEDS-MD`, `BLOCKED`, `STALE`, or `ON-TRACK` — in priority order, plus the
cross-project risks no single project can see. You talk to one CEO; it holds it all.

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
corpus, central data collection, scoring/ranking, or a dashboard. Nothing to opt
out of, nothing to trust us with.

## Troubleshooting

- **`Permission denied (publickey)` on install.** A fresh install clones over
  HTTPS and shouldn't hit this. If an old cached install still tries SSH, rewrite
  GitHub URLs to HTTPS: `git config --global url."https://github.com/".insteadOf "git@github.com:"`, then retry.
- **Marketplace won't load.** Update it: `/plugin marketplace update helm-skill`,
  then `/reload-plugins`.

## License

MIT — see `LICENSE`.
