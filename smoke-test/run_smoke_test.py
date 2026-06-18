#!/usr/bin/env python3
"""
HELM skill-pack smoke test.

This is NOT the product. The product is the markdown in skills/. This script is a
faithful, dependency-free mirror of the deterministic selection table in
skills/helm-onboarding/SKILL.md and the gate table in
skills/helm-orchestrator/SKILL.md. It exists to prove — reproducibly, for any
future contributor — that the load-bearing case still passes:

    input "a local-only browser-based file-transfer tool"
      => the assembled team INCLUDES Security Reviewer with a project-specific WHY
      => the CEO AUTO-INVOKES Security Reviewer at the Plan and Build gates

If a change to the table breaks that, this script exits non-zero.

Run:  python3 run_smoke_test.py
"""
from __future__ import annotations
import sys
from dataclasses import dataclass


# --- the five steering answers (mirror of helm-onboarding Step 4) -------------
@dataclass(frozen=True)
class Answers:
    q1_risk: str       # data_loss | security | user_confusion | performance | correctness | legal | none
    q2_external: bool  # touches external systems, networks, or file transfer?
    q3_interface: str  # cli | web | api | none
    q4_correctness: bool  # one mistake causes harm?
    q5_design: bool    # custom protocols / multi-service / data pipeline?


@dataclass(frozen=True)
class Role:
    name: str
    why: str
    status: str        # "built" | "stub (v1.1)"


# --- the deterministic selection table ---------------------------------------
# Each rule references the answers in its WHY so the justification is generated
# FROM the answers, never a template string. Keep this in lockstep with
# skills/helm-onboarding/SKILL.md.
def assemble_team(a: Answers) -> list[Role]:
    team: list[Role] = [
        Role("Orchestrator (CEO)", "Always - coordinates the team and enforces the lifecycle gates.", "built"),
        Role("Counterweight", "Always - argues against the project's dominant assumption.", "built"),
        Role("Product Keeper", "Always - guards the founding bet (Orchestrator covers this until v1.1).", "stub (v1.1)"),
    ]

    if a.q2_external or a.q1_risk == "security":
        reasons = []
        if a.q2_external:
            reasons.append("it transfers data over a network (Q2=yes)")
        if a.q1_risk == "security":
            reasons.append("security is the primary risk surface (Q1=security)")
        why = ("Assigned because " + " and ".join(reasons) +
               "; transfers must be encrypted, authenticated, and integrity-checked.")
        team.append(Role("Security Reviewer", why, "built"))

    if a.q3_interface == "web":
        team.append(Role("UX Reviewer",
                         "Assigned because the interface is web (Q3=web): a stranger must understand the flow unaided.",
                         "stub (v1.1)"))

    if a.q4_correctness or a.q1_risk == "correctness":
        why = ("Assigned because " +
               ("a mistake causes real harm (Q4=yes)" if a.q4_correctness else "correctness is the primary risk (Q1=correctness)") +
               "; behaviour needs verification beyond the happy path.")
        team.append(Role("QA / Test", why, "stub (v1.1)"))

    if a.q5_design:
        team.append(Role("Architect",
                         "Assigned because the project needs custom protocol / multi-service / pipeline design (Q5=yes).",
                         "stub (v1.1)"))

    return team


def is_fallback(team: list[Role]) -> bool:
    """Fallback trio = only the three always-on roles, no specialist mapped."""
    return {r.name for r in team} == {"Orchestrator (CEO)", "Counterweight", "Product Keeper"}


# --- the gate table: which assigned specialist auto-fires at each phase -------
# Mirror of skills/helm-orchestrator/SKILL.md. Only LIVE wedge rows are exercised
# here. A row is included only if the specialist is on the team.
def auto_invocations(team: list[Role]) -> dict[str, list[str]]:
    names = {r.name for r in team}
    gates: dict[str, list[str]] = {
        "Spec":   ["Counterweight"],                       # LIVE
        "Verify": ["Counterweight"],                       # LIVE
    }
    if "Security Reviewer" in names:
        gates.setdefault("Plan", []).append("Security Reviewer")   # LIVE
        gates.setdefault("Build", []).append("Security Reviewer")  # LIVE
    return gates


# --- the load-bearing test case ----------------------------------------------
FILE_TRANSFER_CASE = Answers(
    q1_risk="security",
    q2_external=True,     # it transfers files over the local network
    q3_interface="web",   # browser-based
    q4_correctness=True,  # a corrupted or misdelivered file is real harm
    q5_design=True,       # a local peer-to-peer transfer protocol
)


def main() -> int:
    print("HELM skill-pack smoke test")
    print("=" * 60)
    print('Input: "a local-only browser-based file-transfer tool"\n')

    team = assemble_team(FILE_TRANSFER_CASE)
    gates = auto_invocations(team)

    print("Assembled team:")
    for r in team:
        print(f"  - {r.name:22} [{r.status:11}]  {r.why}")
    print("\nAuto-invocations by gate (LIVE wedge rows):")
    for phase, specialists in gates.items():
        print(f"  - {phase:7} -> {', '.join(specialists)}")
    print()

    # --- assertions: the contract this script exists to enforce --------------
    failures: list[str] = []

    names = {r.name for r in team}
    if "Security Reviewer" not in names:
        failures.append("Security Reviewer is NOT on the team (Q2=yes / Q1=security must add it).")

    if is_fallback(team):
        failures.append("Team collapsed to the generic fallback trio — selection logic is broken.")

    sec = next((r for r in team if r.name == "Security Reviewer"), None)
    if sec is not None:
        if sec.status != "built":
            failures.append("Security Reviewer must be a BUILT role in v1, not a stub.")
        # WHY must reference the actual answers, not be a template.
        if "Q2" not in sec.why and "Q1" not in sec.why:
            failures.append("Security Reviewer WHY-line does not reference the answers (template smell).")

    if "Security Reviewer" not in gates.get("Plan", []):
        failures.append("CEO does not auto-invoke Security Reviewer at the Plan gate.")
    if "Security Reviewer" not in gates.get("Build", []):
        failures.append("CEO does not auto-invoke Security Reviewer at the Build gate.")

    if failures:
        print("RESULT: FAIL")
        for f in failures:
            print(f"  x {f}")
        return 1

    print("RESULT: PASS")
    print("  ok  Security Reviewer is on the team")
    print("  ok  its WHY-line is project-specific (references the answers)")
    print("  ok  not the generic fallback trio")
    print("  ok  CEO auto-invokes Security Reviewer at the Plan and Build gates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
