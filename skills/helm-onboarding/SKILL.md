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

## The flow

```
1. Describe   → MD states what the project is and who it is for
2. Review     → You read what is already in the folder and report it back
3. Founding bet → You recommend ONE project-specific bet (derived, not generic)
4. Assemble team → Ask the 5 steering questions, apply the mapping table
5. Lay out plan → Show the first-sprint plan and the lifecycle gates
6. Write       → Only after MD approves: write the artifacts to .helm/
```

Walk these in order. Get an explicit "yes / approved / go" before advancing.

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

Ask these **five steering questions**. Get an answer to each.

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

### Answer → role mapping (deterministic)

| Condition (read straight from the answers) | Role added | Status in v1 |
|---|---|---|
| Q2 = yes (network / file transfer) **OR** Q1 = security | **Security Reviewer** | **built** |
| Q3 = web | **UX Reviewer** | stub (v1.1) |
| Q4 = yes **OR** Q1 = correctness | **QA / Test** | stub (v1.1) |
| Q5 = yes | **Architect** | stub (v1.1) |
| *always, regardless of answers* | **Orchestrator (CEO)**, **Counterweight**, **Product Keeper** | Orchestrator + Counterweight built; Product Keeper stub (v1.1) |

**Stub roles are still assigned to the team and named in the manifest.** They
carry a project-specific WHY just like built roles. The stub note simply records
that the role's full persona file ships in v1.1; the Orchestrator already
enforces founding-bet discipline in the interim, and the gate table below shows
exactly when each stub will begin auto-invoking.

### Fallback (never force generics)

If the answers do **not** map to any specialist (all of: Q1 = none obvious / not
security / not correctness, Q2 = no, Q3 = none, Q4 = no, Q5 = no), assemble only:

> Orchestrator + Counterweight + Product Keeper

…and tell the MD: *"Additional roles are available in the library — add them as
needs emerge."* Do **not** pad the team with specialists the project does not
need.

### WHY-line rule (this is load-bearing)

Every assigned role gets a one-line justification **generated from the specific
answers**, referencing them. Never a template string.

- ✅ "Security Reviewer — assigned because the tool transfers files over the
  network (Q2 = yes); transfers must be encrypted, authenticated, and
  integrity-checked."
- ❌ "Security Reviewer — reviews security." *(template; rejected)*

Present the assembled team as a table: **Role · WHY (referencing the answers) ·
Status**. Ask the MD to confirm or adjust.

## Step 5 — Lay out the plan

Show the MD:

1. The lifecycle the project will move through:
   `spec → plan → build → verify → review → ship`
2. The **autonomous gates** the Orchestrator will enforce (see the
   `helm-orchestrator` skill for the full gate table) — in particular, which
   assigned specialist auto-fires at each gate. For this team, name them
   explicitly, e.g. *"When spec.md is complete, I will route to Counterweight
   automatically. When build is green, I will route to Security Reviewer."*
3. The first sprint's candidate tasks, each annotated with its one-sentence link
   to the founding bet.

Ask for approval to write.

## Step 6 — Write the artifacts

Only after approval. Create:

```
.helm/founding-bet.md     # the accepted bet (outcome / assumption / invalidation)
.helm/team.md             # the roster: role, WHY-line, status, gate it fires at
.helm/decisions.jsonl     # append the onboarding decision (see helm-orchestrator)
```

Append one line to `.helm/decisions.jsonl` recording the team assembled and the
answers that produced it, so the selection is auditable. Then hand off to the
`helm-orchestrator` skill to begin the lifecycle.

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
| Product Keeper | Always — guards the founding bet | stub (v1.1) |
| **Security Reviewer** | **Q2 = yes and Q1 = security: files move over an untrusted network, so transfers must be encrypted, authenticated, and integrity-checked** | **built** |
| UX Reviewer | Q3 = web: a browser drag-and-drop flow a stranger must understand unaided | stub (v1.1) |
| QA / Test | Q4 = yes: a corrupted or misdelivered file is real harm; transfers need verification | stub (v1.1) |
| Architect | Q5 = yes: a peer-to-peer transfer protocol needs deliberate design | stub (v1.1) |

This **must not** collapse to a generic Orchestrator+Counterweight+Product
Keeper trio. Security Reviewer is on the team with a project-specific WHY, and
(per the Orchestrator gate table) it auto-fires at the Plan and Build gates.
That is the contract this skill exists to satisfy.
