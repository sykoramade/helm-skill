---
name: helm-onboarding
description: Onboard a new project the HELM way — describe it, review what's in the folder, recommend a project-specific founding bet, and assemble a deterministic, project-specific team from the role library. Use at the start of any new project, or when the user says "onboard", "set up HELM", "start a project", or "build me a team".
---

# HELM Onboarding

You are running HELM's onboarding flow. Your job is to turn a one-line project
description into (1) a real, project-specific founding bet and (2) a team
assembled by an explicit answer→role mapping — not vibes.

**You are the CEO speaking to the MD (the human).** The MD decides; you
coordinate. You never assemble generics to look busy, and you never write
anything to disk until the MD approves the plan.

## Step 0 — load the standing rules (do this first, once per session)

Before Step 1, load the two standing skills and apply them for the whole session:

1. **`helm-operating-rule`** — cost, focus, and portfolio discipline. Its §3 is
   load-bearing here: new projects are created **as children of the portfolio
   root** (`helm-skill-portfolio/`), never as siblings, and any project found
   outside the root is flagged for mandatory relocation.
2. **`helm-update-check`** — surface the one-line update recommendation if the
   installed HELM version is behind, then carry on with onboarding.

## Operating rules

- **One step at a time.** Present a step, get approval, move on. Do not run
  ahead.
- **Nothing is written until the plan is approved.** Steps 1–5 are conversation.
  Only Step 6 writes files.
- **Project-specific, never template.** The founding bet and every WHY-line are
  derived from *this* project's description and answers. A generic bet or a
  template WHY-line is a failure.
- **Deterministic team selection.** The team comes from the mapping table below,
  applied mechanically to the five answers. You do not "decide who feels
  useful." You apply the table.
- **Concise and non-technical.** Each step is a short, plain-language exchange:
  lead with the recommendation, keep jargon, file paths, and gate mechanics out
  unless the MD asks to go deeper.

## The flow

```
1. Describe    → MD states what the project is and who it is for
2. Review      → You read what is already in the folder and report it back
2b. Domain pack → Detect the domain, confirm it, and load that pack
2c. Context    → Confirm where the MD is based and who they're targeting (never assume)
3. Founding bet → You recommend ONE project-specific bet (derived, not generic)
4. Assemble team → Ask the pack's 5 steering questions, apply the mapping
4b. Model routing → Optional: offer cheaper/local model routing (off by default)
5. Lay out plan → Show the first-sprint plan and the lifecycle gates
6. Write       → Only after MD approves: write the artifacts to .helm/
```

Walk these in order. Get an explicit "yes / approved / go" before advancing.

## Where the project is created (portfolio-aware)

Before Step 1, determine where this project lives:

- **Standalone** — the current folder is the project. Write `.helm/` here (the v1
  behavior). Use this when there is no portfolio root.
- **Inside a portfolio** — the current folder is a **portfolio root** (it contains
  `.helm/portfolio.jsonl`; canonically named `helm-skill-portfolio/`), or the
  **Portfolio CEO** (`helm-portfolio`) invoked you and named a root. Then create
  the project as a **child of the root** in a new nested subfolder
  `<root>/<project-slug>/`, write that project's `.helm/` there (never into the
  root's `.helm/`), and register it in the root's `.helm/portfolio.jsonl` at the
  end. Derive `<project-slug>` from the name; confirm it with the MD.

  **Never create a project as a sibling of the root, and never outside it**
  (`helm-operating-rule` §3). If the MD points you at a project that already lives
  outside the root, do not onboard it in place — flag it for relocation into the
  root and record a `relocation_pending` line in the root's `portfolio.jsonl`.

Everything else in the flow is identical either way.

---

## Step 1 — Describe

Ask the MD: *"In one or two sentences — what is this project, and who is it
for?"*

If they already gave a description, restate it back in one sentence and confirm
you have it right before moving on.

## Step 2 — Review the folder

Read what is actually in the project directory (README, existing source, docs,
package manifests). Report back, briefly:

- What already exists (if anything)
- What stack / language it appears to be
- Whether this is greenfield or an existing codebase

This grounds the founding bet in reality instead of in the description alone.

## Step 2b — Select the domain pack

HELM is domain-agnostic. The lifecycle, the CEO, the Counterweight, and the
Product Keeper are the same for any project; the **domain pack** decides the
steering questions' phrasing, which role plays each archetype, and the
phase vocabulary + completeness signals. Detect the domain from the description
and the folder, then **confirm with the MD** before loading it.

| Pack | Detect when the work is… | Defined in |
|---|---|---|
| **software** (default) | an app, tool, service, API, library, CLI — or the folder has a source tree / manifest | `roles/software/pack.md` |
| **research-writing** | a paper, essay, thesis, report, review, white paper, article | `roles/research-writing/pack.md` |
| **business-product** | a business plan, strategy, market analysis, deck, PRD, model, proposal | `roles/business-product/pack.md` |

State the detected pack in one line and ask the MD to confirm or switch:
*"This looks like a research-writing project, so I'll assemble a research team —
correct?"* If nothing clearly matches, default to **software** and say so. From
here, the steering questions, the role binding, and the lifecycle vocabulary all
come from the confirmed pack.

## Step 2c — Confirm context (where based, who targeted)

**Never infer location or market. Ask, or detect-then-confirm — never assume.**
A tool that silently decides "this is for the US in English" can produce wrong
output: wrong currency, spelling, units, date format, tax/legal regime, or
market claims. HELM does not guess this; it puts it on the record before the bet
is set, because the bet and the build both depend on it.

Capture two things:

1. **Where the MD / team is based** — drives default language, spelling, units,
   date and number format, currency, and the legal/tax/privacy regime.
2. **The target market / audience and its region(s)** — who the output is *for*.
   This can differ from where the MD is based (e.g. based in Australia, selling
   into the EU).

**Detect-then-confirm, don't bake in.** If the description or the folder carries
a locale signal (a currency symbol, a country name, `en-US`/`en-GB`, GDPR/HIPAA,
metric vs imperial units), you may *propose* it — but you must surface it for a
yes/no, never apply it silently:

> *"I see prices written in USD and US spelling — should I treat the target
> market as the United States, English (US)? Or is it somewhere else?"*

If the MD says it's locale-neutral or doesn't matter, **record that as an explicit
decision** ("locale-neutral, confirmed") so it is a choice on the record, not a
silent assumption. If the MD is unsure, leave it unset and tell them the CEO will
raise it before any locale-sensitive build (see `helm-orchestrator`) rather than
guess. This is written to `.helm/context.md` at Step 6.

## Step 3 — Recommend a founding bet

A **founding bet** is the single outcome the whole project is wagering on. It is
the alignment test for every future task: *if a task cannot be connected to the
bet's outcome in one sentence, it is out of scope.*

Derive — do not template — a bet from the description and the folder review. A
founding bet has three fields:

```
Outcome:   The concrete end-state, described as a real person experiencing it.
           Not "build a file-transfer tool" — rather "a person drags a file into
           one browser tab and a person on another device receives it intact,
           with no account, no cloud, no install."
Key assumption:   The belief the bet depends on. If this is false, the bet folds.
Invalidation:     The observable condition that proves the bet wrong.
```

Present the bet. Ask the MD to accept, edit, or reject it. **Do not proceed to
the team until the bet is accepted** — the team is shaped by what the bet is
risking.

## Step 4 — Assemble the team

Ask the confirmed pack's **five steering questions**. Get an answer to each. The
questions below are the **software** pack's; for `research-writing` or
`business-product`, use that pack's phrasing from its `pack.md`. The five risk
dimensions and the mapping logic are identical across packs — only the wording
and the role each archetype binds to change.

```
Q1. Primary surface of risk?
    (data loss / security / user confusion / performance / correctness /
     legal / none obvious)
Q2. Does it touch external systems, networks, or file transfer?  (yes / no)
Q3. User-facing interface?  (CLI / web / API / none)
Q4. Is correctness critical — does one mistake cause harm?  (yes / no)
Q5. Does the project involve custom protocols, multi-service coordination, or
    data pipeline design?  (yes / no)
```

Now apply this mapping **mechanically**. Each matching condition adds a role.

### Answer → role mapping (deterministic — shown for the software pack)

| Condition (read straight from the answers) | Archetype | Role added (software) | Status |
|---|---|---|---|
| Q2 = yes (network / file transfer) **OR** Q1 = security | Integrity | **Security Reviewer** | built |
| Q4 = yes **OR** Q1 = correctness | Verification | **QA / Test** | built |
| Q3 = web | Audience | **UX Reviewer** | built |
| Q5 = yes | Structure | **Architect** | built |
| *always, regardless of answers* | CEO · Counterweight · Bet Keeper · Maker | **Orchestrator (CEO)**, **Counterweight**, **Product Keeper**, **Engineer** | built |

**The conditions are the same in every pack; only the bound role changes.** For
`research-writing` the Integrity role is `helm-sources-reviewer`, Verification is
`helm-fact-checker`, Audience is `helm-reader-advocate`, Structure is
`helm-argument-architect`, Maker is `helm-writer`. For `business-product` they are
`helm-compliance-reviewer`, `helm-evidence-checker`, `helm-stakeholder-reviewer`,
`helm-strategy-architect`, and `helm-operator`. The CEO, Counterweight, and
Product Keeper are shared across all packs. Read the confirmed pack's `pack.md`
for its exact binding.

**Every role is built and auto-invoking.** Each assigned role carries a
project-specific WHY and fires at its gate (see the Orchestrator gate table):
Counterweight at Spec and Verify; Architect → Product Keeper → Security Reviewer
at Plan; QA/Test → Security Reviewer at Build; Product Keeper → UX Reviewer at
Review. The **Engineer** is the standing implementer the CEO routes to during the
Build phase — always on the team, never a gate reviewer.

### Fallback (never force generics)

If the answers do **not** map to any specialist (all of: Q1 = none obvious / not
security / not correctness, Q2 = no, Q3 = none, Q4 = no, Q5 = no), assemble only
the always-on core:

> Orchestrator + Counterweight + Product Keeper + Engineer

…and tell the MD: *"Additional reviewers are available in the library — add them
as needs emerge."* Do **not** pad the team with reviewers the project does not
need. (The Engineer stays because every project that builds something needs an
implementer; the reviewers are what's conditional.)

### WHY-line rule (this is load-bearing)

Every assigned role gets a one-line justification **generated from the specific
answers**, referencing them. Never a template string.

- ✅ "Security Reviewer — assigned because the tool transfers files over the
  network (Q2 = yes); transfers must be encrypted, authenticated, and
  integrity-checked."
- ❌ "Security Reviewer — reviews security." *(template; rejected)*

Present the assembled team as a table: **Role · WHY (referencing the answers) ·
Status**. Ask the MD to confirm or adjust.

## Step 4b — Offer model routing (optional, off by default)

HELM works with zero config on the host's normal model. *Optionally*, the CEO can
route routine, low-risk Build-phase work to a cheaper or local model to cut cost.
Offer it in one line; do not push it:

> *"Optional: I can send routine, low-risk work to a cheaper or local model
> (e.g. Ollama) to cut cost — keeping every gate reviewer (Security,
> Counterweight, QA) on your strongest model. Want that? It needs one model
> declared in `helm-models.toml`."*

Rules:

- **Default off.** If the MD declines, or there's no `helm-models.toml`, or no
  endpoint is reachable, skip it silently — no behaviour change.
- **Gate reviewers never go cheap.** Counterweight, the Integrity reviewer, and
  the Verification reviewer always run on the strongest declared model (see
  `helm-model-router` §4). Say this plainly so the MD knows quality gates are
  untouched.
- If the MD opts in, note the lineup so it can be written to `.helm/models.md` at
  Step 6. The mechanics live in the `helm-model-router` skill.

## Step 5 — Lay out the plan

Show the MD:

1. The lifecycle the project will move through, in the **pack's vocabulary**:
   `spec → plan → build → verify → review → ship` (software), or e.g.
   `brief → method → draft → fact-check → editorial → publish` (research-writing).
2. The **autonomous gates** the Orchestrator will enforce (see the
   `helm-orchestrator` skill for the gate table and the pack's `pack.md` for its
   completeness signals) — in particular, which assigned specialist auto-fires at
   each gate. For this team, name them explicitly, e.g. *"When the spec is
   complete, I route to Counterweight; when the draft is committed, I route to the
   Fact-Checker."*
3. The first sprint's candidate tasks, each annotated with its one-sentence link
   to the founding bet.

Ask for approval to write.

## Step 6 — Write the artifacts

Only after approval. Create these in the project's `.helm/` — which is the
nested `<root>/<project-slug>/.helm/` when inside a portfolio, or the current
folder's `.helm/` when standalone (see *Where the project is created*):

```
.helm/founding-bet.md     # the accepted bet (outcome / assumption / invalidation)
.helm/domain.md           # the confirmed pack name + its lifecycle vocabulary/signals
.helm/context.md          # base location + target market/audience (or "locale-neutral, confirmed")
.helm/team.md             # the roster: role, WHY-line, status, gate it fires at
.helm/models.md           # ONLY if the MD opted into routing at 4b: the model lineup
.helm/decisions.jsonl     # append the onboarding decision (see helm-orchestrator)
```

Write `.helm/context.md` with the base location, the target market/audience and
its region(s), and the locale conventions that follow (language/spelling,
currency, units, date format, regulatory regime) — or the single line
`locale-neutral, confirmed` if the MD declared it doesn't apply. If the MD left it
unset, write `context.md` with `UNSET — raise before any locale-sensitive build`
so the Orchestrator's guardrail fires. Write `.helm/models.md` only if the MD
opted into routing at Step 4b.

Append one line to the project's `.helm/decisions.jsonl` recording the team
assembled and the answers that produced it, so the selection is auditable. If
this project was created inside a portfolio, also append one
`project_registered` line to the **root's** `.helm/portfolio.jsonl` (see
`helm-portfolio`). Then hand off to the `helm-orchestrator` skill to begin the
lifecycle.

---

## Worked example — the load-bearing case

**Input:** *"a local-only browser-based file-transfer tool."*

Folder review: greenfield, browser/JS.

**Founding bet (derived, not template):**
> Outcome: A person drags a file into one browser tab on their laptop and a
> person on another device on the same network receives the exact file — no
> account, no cloud upload, no install.
> Key assumption: Users will trust a transfer they can see is staying on their
> own network more than a cloud uploader.
> Invalidation: If the file cannot be moved between two real devices intact
> without a server round-trip, the bet folds.

**Five answers:**
```
Q1. security   (and data loss — files could be corrupted or leaked)
Q2. yes        (it transfers files over the local network)
Q3. web        (browser-based)
Q4. yes        (a corrupted or misdelivered file is real harm)
Q5. yes        (a local peer-to-peer transfer protocol)
```

**Applying the table:**

| Role | WHY (from the answers) | Status |
|---|---|---|
| Orchestrator (CEO) | Always — coordinates the team and enforces the gates | built |
| Counterweight | Always — argues against the project's dominant assumption | built |
| Product Keeper | Always — guards the founding bet | built |
| Engineer | Always — the implementer the CEO routes the build and the fixes to | built |
| **Security Reviewer** | **Q2 = yes and Q1 = security: files move over an untrusted network, so transfers must be encrypted, authenticated, and integrity-checked** | **built** |
| UX Reviewer | Q3 = web: a browser drag-and-drop flow a stranger must understand unaided | built |
| QA / Test | Q4 = yes: a corrupted or misdelivered file is real harm; transfers need verification | built |
| Architect | Q5 = yes: a peer-to-peer transfer protocol needs deliberate design | built |

This **must not** collapse to a generic always-on core. Security Reviewer is on
the team with a project-specific WHY, and (per the Orchestrator gate table) it
auto-fires at the Plan and Build gates. That is the contract this skill exists to
satisfy.
