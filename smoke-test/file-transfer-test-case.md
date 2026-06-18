# Smoke test — the file-transfer case

The HELM skill pack must pass this case before any release. It is the
load-bearing proof that the deterministic selection logic works: a project whose
risk is obvious must get the right specialist *and* have it auto-invoked — not a
generic baseline trio, and not "wait to be asked."

## Input

> "a local-only browser-based file-transfer tool"

## The five steering answers

| Q | Answer | Reasoning |
|---|---|---|
| Q1. Primary surface of risk? | **security** (and data loss) | files can be intercepted, leaked, or corrupted |
| Q2. Touches external systems, networks, or file transfer? | **yes** | it transfers files over the local network |
| Q3. User-facing interface? | **web** | it is browser-based |
| Q4. Correctness critical — does one mistake cause harm? | **yes** | a corrupted or misdelivered file is real harm |
| Q5. Custom protocols / multi-service / data pipeline? | **yes** | a local peer-to-peer transfer protocol |

## Expected assembled team

| Role | Status | Why (must reference the answers) |
|---|---|---|
| Orchestrator (CEO) | built | always |
| Counterweight | built | always |
| Product Keeper | stub (v1.1) | always |
| **Security Reviewer** | **built** | **Q2=yes + Q1=security: files move over the network; transfers must be encrypted, authenticated, integrity-checked** |
| UX Reviewer | stub (v1.1) | Q3=web |
| QA / Test | stub (v1.1) | Q4=yes |
| Architect | stub (v1.1) | Q5=yes |

## Expected auto-invocations (LIVE wedge gates)

| Phase complete | CEO auto-invokes |
|---|---|
| Spec | Counterweight |
| Plan | Security Reviewer |
| Build | Security Reviewer |
| Verify | Counterweight |

## Pass criteria (asserted by `run_smoke_test.py`)

1. Security Reviewer **is on the team**.
2. Its WHY-line is **project-specific** (references the actual answers), not a
   template string.
3. The team is **not** the generic fallback trio (Orchestrator + Counterweight +
   Product Keeper only).
4. The CEO **auto-invokes** Security Reviewer at the **Plan** and **Build** gates
   — it is not waiting to be asked.

If any of these fail, the selection or gate logic is broken.

## How to run

**Automated (reproducible):**

```bash
python3 smoke-test/run_smoke_test.py
# exits 0 on PASS, non-zero on FAIL
```

The script is a faithful mirror of the tables in
`skills/helm-onboarding/SKILL.md` and `skills/helm-orchestrator/SKILL.md`. If you
change a table, update the script and re-run.

**Manual (in a host, end-to-end):**

1. Install the pack (see the root `README.md`).
2. Start the `helm-onboarding` skill and give it the input above.
3. Answer the five questions as in the table.
4. Confirm the assembled team and WHY-lines match the "Expected assembled team"
   table — especially that Security Reviewer is present with a project-specific
   WHY.
5. Approve the plan, then advance the lifecycle (`helm-orchestrator`) and confirm
   the CEO announces "routing to Security Reviewer" at the Plan and Build gates
   without being asked.
