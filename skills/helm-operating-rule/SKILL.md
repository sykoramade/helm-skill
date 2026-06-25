---
name: helm-operating-rule
description: HELM's standing operating rule — four enforced defaults on cost, focus, portfolio discipline, and completion honesty that apply to the Orchestrator and every agent for the whole session. Model routing (the orchestrating model never does grunt work), tangent & scope guards (every task traces to the founding bet or stops), portfolio structure (one parent root, projects as children), and completion honesty (a "done" is not relayed without the artifact that proves it). Loaded first by the Orchestrator, Onboarding, and Portfolio CEO. Read it at the start of any HELM session.
---

# HELM Operating Rule — Cost, Focus & Portfolio Discipline

> Standing rule for the HELM pack. Applies to the Orchestrator and every agent for
> the **whole session** — the entry-point skills (`helm-orchestrator`,
> `helm-onboarding`, `helm-portfolio`) load it first.
> These are **enforced defaults, not suggestions.** When a rule says "STOP and
> ask," surface a one-line check to the MD before spending more tokens.

These four policies sharpen rules HELM already holds: the CEO never executes the
work (`helm-orchestrator`), every task traces to the founding bet
(`helm-product-keeper`), projects nest under a portfolio root (`helm-portfolio`),
and a completion claim is not a fact until its evidence is shown
(`helm-verification-before-completion`). This skill makes the *cost*, *focus*,
*structure*, and *completion-honesty* edges of those rules mechanical and citable.

---

## 1. Model Routing — the orchestrating model never does grunt work

**Default:** the main-loop / orchestrating model **orchestrates, decides, and
reviews only.** It must NOT execute mechanical work inline. Mechanical work is
delegated to a cheaper tier via subagent (a strong build model for real work, a
cheap deterministic model for cheap deterministic steps).

**Grunt work (ALWAYS offload):** file/format conversion, zipping/packaging,
scaffolding, find-and-replace, boilerplate, running builds/tests/linters,
doc/report generation, dependency installs, log/format tidy-ups, and **retrying
flaky tooling**.

**Stays on the strong model (do NOT offload):** work that is *risky or complex* —
architectural decisions, ambiguous requirements, security/secrets/keys,
irreversible or destructive operations, cross-cutting design, or anything where
being wrong is expensive. This is the same line HELM already draws at the gates:
gate-critical work (Counterweight, the Integrity reviewer, the Verification
reviewer, anything you would `ESCALATE-TO-MD`) **never** goes to a cheap tier
(`helm-model-router` §4).

**Hard trigger:** if you catch yourself on the **2nd inline mechanical retry** of
the same step, STOP — delegate it to a subagent or hand it back. Never grind a
deterministic task across many orchestrator round-trips (each turn re-reads full
context at the top tier's rate; the round-trips, not the compute, are the cost).

**Relationship to `helm-model-router`.** That skill routes work across *declared
external models* (your Ollama, a cheap hosted model, a frontier safety net). This
rule is one level up: it governs whether the **host's own orchestrating model**
should be doing a task at all, or delegating it. The two compose — this rule says
"delegate the grunt work"; the router says "and here is the cheapest declared
model that can take it." If no `helm-models.toml` exists, delegate to a subagent
on the host's normal model instead; the discipline is unchanged.

---

## 2. Tangent & Scope Guards — protect the mission

Every task must trace to the project's founding bet **in one sentence**. If it
can't, it is out of scope (existing HELM principle — see `helm-product-keeper`
and the Orchestrator's founding-bet discipline; this section makes the stop
mechanical).

**STOP and ask before continuing when ANY of these fire:**

- **Unrequested scope:** you are doing something the MD did not ask for AND the
  bet does not require (e.g., MD asked for a PDF; you are building a DOCX).
- **No-deliverable churn:** **> 6 consecutive tool-call turns** on one sub-task
  with no shippable output.
- **Repeated failure:** the **same approach fails ≥ 2 times** — reassess and offer
  an alternative; do not keep retrying.
- **Mission drift:** the active thread no longer serves the founding bet.

**Resolution rule (who started the tangent?):**

- *MD-initiated but off-mission* → name the drift in one line and ask:
  **"continue / narrow / drop?"** Do not silently follow.
- *AI-initiated* (gold-plating, over-verification, pedantry) → **default to NOT
  doing it.** Bias to the smallest thing that satisfies the literal ask.

The thresholds (2 retries, 6 turns) are deliberate, tunable dials — adjust to
taste, but keep them mechanical so the stop is a check, not a vibe.

---

## 3. Portfolio Structure — one parent, projects as children

**Canonical layout — a single portfolio root holding every project as a child:**

```
helm-skill-portfolio/            ← the ONE parent folder
├── .helm/portfolio.jsonl        ← registers all child projects
├── <project-a>/.helm/...        ← each project self-contained
├── <project-b>/.helm/...
└── <project-c>/.helm/...
```

**Rules:**

- New projects are created **as children of `helm-skill-portfolio/`** — never as
  sibling folders of the root. (`helm-onboarding` writes the new project to
  `<root>/<project-slug>/.helm/`, never into the root's `.helm/`.)
- A project must **never live outside** the portfolio root. If one is detected
  outside (e.g., a deployed repo elsewhere), **flag it for relocation into the
  root and record the pending move in `portfolio.jsonl`.** This relocation is
  mandatory, not optional — surface it to the MD as a one-line decision.
- The root `portfolio.jsonl` is the single source of truth for which projects
  exist and where their `.helm/` state lives.
- Project state (`founding-bet.md`, `team.md`, `decisions.jsonl`, etc.) lives in
  **that project's** `.helm/`, not the portfolio root. The Portfolio CEO reads
  those logs; it never writes into a project's `.helm/` (`helm-portfolio`).

**Relocation record (append to the root's `portfolio.jsonl`):**

```json
{"ts": "2026-06-25T10:00:00Z", "event": "relocation_pending", "project": "verita-factcheck", "found_at": "../helm-skill-test", "target": "helm-skill-portfolio/verita-factcheck", "note": "outside the portfolio root — relocate into the root"}
```

---

## 4. Completion Honesty — a "done" is not relayed without its evidence

Every completion claim from a maker — *done, it works, verified, tested, passing,
fixed, ready* — is intercepted **the moment it is uttered**, before the CEO relays
it to the MD and before the Verify gate. This is HELM's most-recurring failure
(over-claiming), and it happens mid-Build, a phase earlier than any gate.

**The demand is mechanical: the artifact, not the assertion.** The maker must
show the exact **command** run, its **captured output** (pasted with the pass/fail
line and exit code, or a readable path the CEO opens), and **which path it
exercised** (easy vs. risky). A re-assertion — "yes, I verified it" — is *not*
evidence; it is an automatic miss. *Show the output, not the word "verified."*

**Hard rule:** the CEO does **not** relay "done" upward until the evidence is
present and seen. No artifact → the claim is returned to the maker with the
missing piece named, and logged to `.helm/decisions.jsonl`. The full mechanics
live in `helm-verification-before-completion` — the **first of HELM's Mode-B
micro-checks** (triggered by an utterance, not a gate). The planned **second** is
a scope-creep check on "while we're here / might as well" language → Product
Keeper. This rule says "intercept the claim"; the skill says "and here is exactly
what to demand."

---

## How this rule is loaded

The three entry-point skills read this rule first and apply it for the whole
session:

- `helm-orchestrator` — Step 0, before driving any phase.
- `helm-onboarding` — Step 0, before onboarding a project.
- `helm-portfolio` — Step 0, before briefing at a root.

On other hosts (Cursor, Windsurf, plain system prompt), include this file
alongside the entry-point skills so the same defaults are in context at runtime.
A rule only bites if it is loaded; this is where it gets loaded.
