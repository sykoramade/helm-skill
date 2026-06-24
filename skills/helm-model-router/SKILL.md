---
name: helm-model-router
description: Route each task to the cheapest model that can still do it, across any mix of local and cloud models you choose. Bring your own models via an OpenAI-compatible endpoint, declare their cost and capability, and the CEO scores each task and sends it to the cheapest capable tier — escalating to a stronger model only when a cheaper one fails. Gate-critical reviewers (Security, Counterweight, QA) never go to a cheap tier. Use to set up routing, add a model, or understand why a task landed on a given model.
---

# HELM Model Router

> A frontier model is expensive. Most tasks in a real project don't need one. This
> skill lets the CEO score each task, send it to the **cheapest model that can
> actually do it**, and escalate only when a cheaper model falls short — so the
> expensive model is the exception, not the default.

**It's model-agnostic and you own the lineup.** Run everything locally for $0, mix
in a cheap hosted model, add a frontier model as the safety net — any model that
speaks the OpenAI-compatible API works, and you set cost and capability per model.

The principle in one line: **never pay for capability you don't need, but never
ship a result a cheap model got wrong.**

---

## 0. What this skill is (and is not) — read this first

HELM ships as **markdown**, not a service. So this router is what the *host* (the
CEO running in Claude Code, Cursor, etc.) can do with a config file and the
host's own tool/shell access: read your model lineup, score a task against rules
you can read, call the cheapest capable model, and escalate on failure. It is
**deterministic and inspectable** — the same task scores the same way every time,
and the CEO states the reason it picked a model.

What it deliberately does **not** do in the markdown pack: keep a live circuit
breaker, learn capability scores from history, or auto-calibrate thresholds over
time. Those need a persistent running process, which a skill pack is not — they
belong to the full **HELM engine (v2)** and are flagged as such in §9. This skill
claims only what markdown + the host can honestly execute.

```
                 ┌───────────────────────────────────────┐
   task ─────▶   │  1. SCORE    confidence 0.0–1.0        │
                 │  2. FILTER   drop models below the      │
                 │              capability bar for this    │
                 │              task type                  │
                 │  3. ROUTE    score → cheapest capable   │
                 │  4. EXECUTE  call that model            │
                 │  5. GATE     accept only if it passes   │
                 │  6. ESCALATE on failure, go stronger    │
                 │  7. LOG      record the choice          │
                 └───────────────────────────────────────┘
        cheapest ◀──────────────────────────────▶ most capable
   local-small ($0) → local-large → cloud-cheap → cloud-strong → frontier
```

---

## 1. Declare your models (`helm-models.toml`)

You provide a small registry of the models you want to use. Each entry says where
the model lives, what it costs, and what it's good at. **Keys are referenced by
environment-variable name only — never written into the file.**

```toml
# helm-models.toml  — your model lineup; lives at the project root, next to .helm/

# Local model via Ollama / LM Studio / llama.cpp / vLLM — free, no key
[[model]]
id          = "local-coder"
base_url    = "http://localhost:11434/v1"     # any OpenAI-compatible endpoint
model_name  = "qwen2.5-coder:14b"
input_cost  = 0.00
output_cost = 0.00
local       = true
capability  = { code_generation = 0.80, summarisation = 0.85, "*" = 0.70 }

# Cheap hosted model — cheapest cloud fallback
[[model]]
id          = "cloud-cheap"
base_url    = "https://api.groq.com/openai/v1"
model_name  = "llama-3.3-70b"
api_key_env = "GROQ_API_KEY"                   # name only; key read from env
input_cost  = 0.59
output_cost = 0.79
capability  = { "*" = 0.75 }

# Strong model — the safety net for hard / high-stakes / gate-critical work
[[model]]
id          = "cloud-strong"
base_url    = "https://api.openai.com/v1"
model_name  = "gpt-4.1"
api_key_env = "OPENAI_API_KEY"
input_cost  = 2.00
output_cost = 8.00
capability  = { "*" = 0.95, architecture = 0.95, security_audit = 0.90 }
```

**Local-first default.** With no `helm-models.toml` at all, the router does
nothing and the CEO uses the host's normal model — HELM's zero-config promise is
unchanged. With one local model declared, eligible tasks run on it for $0,
offline. Add cloud entries only when you want more headroom.

Because the interface is OpenAI-compatible, the same three lines (`base_url`,
`model_name`, `api_key_env`) reach Ollama, LM Studio, llama.cpp, vLLM, OpenAI,
Groq, DeepSeek, Together, Mistral, OpenRouter, and most others. Adding a provider
is a config entry, never a code change.

---

## 2. Score the task (how a task gets a number)

Each task is scored **0.0–1.0** by summing three components. A higher score means
a simpler, lower-blast-radius task — safe to push to a cheaper model.

| Component | Signal | Default scoring |
|---|---|---|
| **Complexity** | the dominant signal | `low` = 0.50, `medium` = 0.40, `high` = 0.00 |
| **Token size** | bigger context = riskier on small models | ≤500 tok = 0.35, ≤1500 = 0.20, >1500 = 0.00 |
| **Files touched** | blast radius | 0–1 = 0.15, 2–3 = 0.08, >3 = 0.00 |

```
score = complexity + tokens + files      (capped at 1.0)
```

Complexity and size dominate (up to 0.85 of the range); file count is the
tie-breaker that nudges a borderline task across a threshold.

> **Worked example.** Low-complexity, 400-token, 1-file task:
> `0.50 + 0.35 + 0.15 = 1.00` → cheapest tier. High-complexity, 2000-token,
> 5-file task: `0.00 + 0.00 + 0.00 = 0.00` → escalate to the strongest model.

These weights are **defaults, not laws** — tune them to your task mix.

---

## 3. The tier ladder (score → model)

The CEO sorts your models by cost and maps the score onto them by descending
threshold:

| Score | Tier | Goes to | Typical cost |
|---|---|---|---|
| **≥ 0.85** | AUTONOMOUS | cheapest local model | $0 |
| **0.70 – 0.84** | ASSISTED | local model | $0 |
| **0.60 – 0.69** | SPECIALIST | capability-matched model | $0–low |
| **0.45 – 0.59** | GUIDED | cheapest cloud model | low |
| **< 0.45** | ESCALATED | your strongest model | frontier |

Because the ladder is cost-ordered, "highest score wins the cheapest model" falls
out for free — you only start paying once a task scores below the cloud
threshold. The three thresholds (`0.85 / 0.70 / 0.60`) are the dials you'll touch
most: lower one → more tasks go cheap; raise it → more go up a tier.

---

## 4. Capability scores + the gate-reviewer floor

Routing by score alone assumes every model is interchangeable. They aren't. Each
model carries `task_type → 0.0–1.0` capability scores (1.0 = full quality, 0.0 =
can't do it; a `"*"` wildcard covers unmapped types). The CEO only considers a
model for a task type if its capability clears the bar, then picks the cheapest
that qualifies:

```
cheapest_capable(task_type, min_capability = 0.70)
  → models that clear the bar, sorted cheapest → most expensive
    (free / local models sort first)
```

This is the literal expression of the goal: *of everyone who can do this task to
standard, pick the cheapest.* It's also the safety valve — set a small local
model's `security_audit` or `multi_file_refactor` capability low and it is
**never** trusted with that work, no matter how high the task scored.

### HELM rule — gate-critical work never goes cheap (load-bearing)

A cheap model is allowed to *draft*; it is never allowed to *judge*. The
following are **always** routed to your strongest declared model, regardless of
score:

- **Counterweight** — the adversarial / overconfidence review.
- **Security Reviewer** (or the active pack's Integrity role: Compliance Reviewer,
  Sources Reviewer).
- **QA / Test** (or the pack's Verification role: Evidence Checker, Fact-Checker).
- Any decision the CEO would **escalate to the MD**, and anything written to
  `.helm/decisions.jsonl` as a verdict.

Mechanically: give cheap/local models a low capability for `gate_review`,
`security_audit`, `adversarial_review`, and `verification`, so the
`cheapest_capable` filter excludes them from gate work automatically. The cheap
tier accelerates the Maker's grunt work; it does not get a vote at a gate.

---

## 5. Escalate on failure (cheap-first, stronger on miss)

Scoring picks a *starting* model. Execution may need more. The CEO runs the task
down the cost-ordered ladder and stops at the first model whose result passes:

```
order   = cheapest capable → … → strongest declared model
MAX_HOPS = 2     # after 2 failed attempts, jump straight to the strongest model
```

Per attempt the result is **ACCEPT** (done), or **RETRY/ESCALATE** (advance to a
stronger model). After `MAX_HOPS` honest cheap attempts, commit to the model that
will actually finish it rather than grinding through every tier in between. Record
each hop's model and outcome in the log (§7).

---

## 6. The quality gate (cheap is only allowed if it's also correct)

Cost efficiency is bounded by one rule: **a cheaper result that fails review is
more expensive than routing correctly the first time.** A cheap-tier result is a
*draft* that still has to clear the same HELM gate any work clears (see
`helm-orchestrator`). If a reviewer returns `CHALLENGE` / `REJECT` / `FAIL`, the
task escalates to a stronger model and re-enters the gate. Cheap output that
doesn't pass simply isn't done — the router can't "save money" by shipping bad
work past a gate.

---

## 7. Keys, safety, and logging

- **Environment variables only.** The config names an `api_key_env`; the key is
  read from the environment at call time — never written to the file, never
  logged. Local models need no key.
- **Local-first.** With only local models declared, nothing leaves the machine.
  Nothing reaches the network until you add a cloud model and its key on purpose.
- **No lock-in.** Drop a provider by deleting its config entry; swap a model by
  editing two lines.
- **Log every routing decision.** Append a `routing_decision` line to
  `.helm/decisions.jsonl` so cost/quality is auditable like every other HELM
  decision:

```json
{"ts": "2026-06-24T10:15:00Z", "event": "routing_decision", "task": "draft README section", "task_type": "summarisation", "score": 0.90, "tier": "AUTONOMOUS", "model": "local-coder", "outcome": "ACCEPT", "hops": ["local-coder"], "est_cost": 0.0}
```

---

## 8. Optional: route through a gateway

Want many hosted models without managing a key per provider? Point one config
entry's `base_url` at an OpenAI-compatible gateway/proxy and let it fan out behind
one endpoint and one key. Lower setup, at the cost of an external dependency — so
keep at least one **local** model in the lineup if the offline / $0 path matters.

---

## 9. Deferred to the HELM engine (v2) — not in this skill

These are real parts of HELM's routing design but require a persistent process,
so they are **not** active in the markdown pack. Listed here so the boundary is
honest, not hidden:

- **Circuit breaker** — auto-skipping a model that fails repeatedly, with a
  cool-down and trial recovery.
- **Learning loop** — updating capability scores from observed outcomes so the
  lineup self-tunes toward the cheapest tier that actually works.
- **Threshold auto-calibration** — bounded automatic nudging of the tier
  thresholds.
- **Per-hop cost accounting history** across a project.

Until then: review your `routing_decision` log periodically and adjust capability
scores and thresholds by hand. The same `helm-models.toml` carries straight over
to the engine when it lands.

---

## Onboarding & orchestrator hooks

- **Onboarding** offers this as an opt-in step (`helm-onboarding`, Step 4b): off
  by default, enabled only if you declare a lineup. If no `helm-models.toml`
  exists or no endpoint is reachable, it is skipped silently — zero behaviour
  change.
- **The CEO** consults this skill when routing a Build-phase task to the Maker.
  It never overrides the gate-reviewer floor in §4, and it logs every choice.

## Summary: the efficiency loop

1. **Declare** your models — cost + capability, local-first by default.
2. **Score** each task (complexity + size + files).
3. **Filter** to models that clear the capability bar for the task type.
4. **Route** to the cheapest that qualifies — never a gate reviewer to a cheap tier.
5. **Execute**, **gate**, and **escalate** to a stronger model on failure.
6. **Log** the choice so it's auditable.

The expensive model stays the exception. That's the whole game.
