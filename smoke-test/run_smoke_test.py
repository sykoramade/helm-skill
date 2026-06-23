#!/usr/bin/env python3
"""
HELM skill-pack smoke test.

This is NOT the product. The product is the markdown in skills/. This script is a
faithful, dependency-free mirror of the deterministic selection table in
skills/helm-onboarding/SKILL.md, the archetype->role bindings in roles/<pack>/
pack.md, and the gate table in skills/helm-orchestrator/SKILL.md.

It enforces two contracts:

1. THE LOAD-BEARING SOFTWARE CASE (unchanged since v1):
     input "a local-only browser-based file-transfer tool"
       => the assembled team INCLUDES Security Reviewer with a project-specific WHY
       => the CEO AUTO-INVOKES Security Reviewer at the Plan and Build gates

2. THE AGNOSTIC-PACK CASE (v1.1):
     input "a peer-reviewed research paper with empirical claims"
       => the SAME deterministic engine binds the research-writing pack's roles
          (Writer, Sources Reviewer, Fact-Checker, Reader Advocate, Argument
          Architect) and NO software role names leak in.

If a change to a table breaks either, this script exits non-zero.

Run:  python3 run_smoke_test.py
"""
from __future__ import annotations
import sys
from dataclasses import dataclass


# --- the five steering answers (the shared risk dimensions) -------------------
@dataclass(frozen=True)
class Answers:
    q1_risk: str       # primary risk surface (pack-flavoured vocabulary)
    q2_external: bool  # touches external systems / sources / transfer?
    q3_audience: str   # the consumer/audience surface ("none" => no audience role)
    q4_correctness: bool  # is correctness/accuracy critical?
    q5_design: bool    # needs deliberate structure/design?


@dataclass(frozen=True)
class Role:
    name: str
    why: str
    status: str        # always "built" in v1.1


# --- archetype -> role binding per pack (mirror of roles/<pack>/pack.md) -------
PACKS: dict[str, dict[str, str]] = {
    "software": {
        "maker": "Engineer",
        "integrity": "Security Reviewer",
        "verification": "QA / Test",
        "audience": "UX Reviewer",
        "structure": "Architect",
    },
    "research-writing": {
        "maker": "Writer",
        "integrity": "Sources Reviewer",
        "verification": "Fact-Checker",
        "audience": "Reader Advocate",
        "structure": "Argument Architect",
    },
    "business-product": {
        "maker": "Operator",
        "integrity": "Compliance Reviewer",
        "verification": "Evidence Checker",
        "audience": "Stakeholder Reviewer",
        "structure": "Strategy Architect",
    },
}

# Q1 risk values (pack-flavoured) that trigger an archetype on their own.
INTEGRITY_RISK = {"security", "misrepresentation", "legal-compliance"}
VERIFICATION_RISK = {"correctness", "inaccuracy", "data-accuracy"}

# The integrity standard, phrased per pack, so the WHY stays domain-faithful.
INTEGRITY_STANDARD = {
    "software": "transfers must be encrypted, authenticated, and integrity-checked.",
    "research-writing": "every claim must trace to a credible, faithfully-represented source.",
    "business-product": "every claim and commitment must be substantiated and defensible.",
}


# --- the deterministic selection engine (shared across all packs) -------------
# Each rule references the answers in its WHY so the justification is generated
# FROM the answers, never a template string. Keep in lockstep with
# skills/helm-onboarding/SKILL.md and roles/<pack>/pack.md.
def assemble_team(a: Answers, pack: str) -> list[Role]:
    b = PACKS[pack]
    team: list[Role] = [
        Role("Orchestrator (CEO)", "Always - coordinates the team and enforces the lifecycle gates.", "built"),
        Role("Counterweight", "Always - argues against the project's dominant assumption.", "built"),
        Role("Product Keeper", "Always - guards the founding bet.", "built"),
        Role(b["maker"], "Always - the maker the CEO routes the build and the fixes to.", "built"),
    ]

    if a.q2_external or a.q1_risk in INTEGRITY_RISK:
        reasons = []
        if a.q2_external:
            reasons.append("it touches external systems / sources (Q2=yes)")
        if a.q1_risk in INTEGRITY_RISK:
            reasons.append(f"{a.q1_risk} is the primary risk surface (Q1)")
        why = "Assigned because " + " and ".join(reasons) + "; " + INTEGRITY_STANDARD[pack]
        team.append(Role(b["integrity"], why, "built"))

    if a.q4_correctness or a.q1_risk in VERIFICATION_RISK:
        why = ("Assigned because " +
               ("a mistake causes real harm (Q4=yes)" if a.q4_correctness else f"{a.q1_risk} is the primary risk (Q1)") +
               "; behaviour/claims need verification beyond the happy path.")
        team.append(Role(b["verification"], why, "built"))

    if a.q3_audience not in ("none", "", None):
        team.append(Role(b["audience"],
                         f"Assigned because there is an audience surface (Q3={a.q3_audience}): it must land with someone who did not build it.",
                         "built"))

    if a.q5_design:
        team.append(Role(b["structure"],
                         "Assigned because the work needs deliberate structure/design (Q5=yes).",
                         "built"))

    return team


def always_on(pack: str) -> set[str]:
    """The core present on every team of this pack: CEO, Counterweight, Bet Keeper, Maker."""
    return {"Orchestrator (CEO)", "Counterweight", "Product Keeper", PACKS[pack]["maker"]}


def is_fallback(team: list[Role], pack: str) -> bool:
    """Fallback = only the always-on core, no conditional reviewer mapped."""
    return {r.name for r in team} == always_on(pack)


# --- the gate table: which archetype auto-fires at each phase -----------------
# Mirror of skills/helm-orchestrator/SKILL.md. Archetype-keyed so it is identical
# across packs; the active pack binds each archetype to its role. Order mirrors
# the gate table. A role fires only if it is on the team.
GATE_ARCHETYPES: dict[str, list[str]] = {
    "Spec":   ["counterweight"],
    "Plan":   ["structure", "bet_keeper", "integrity"],
    "Build":  ["verification", "integrity"],
    "Verify": ["counterweight"],
    "Review": ["bet_keeper", "audience"],
}


def auto_invocations(team: list[Role], pack: str) -> dict[str, list[str]]:
    b = PACKS[pack]
    arch_role = {
        "counterweight": "Counterweight",
        "bet_keeper": "Product Keeper",
        "maker": b["maker"],
        "integrity": b["integrity"],
        "verification": b["verification"],
        "audience": b["audience"],
        "structure": b["structure"],
    }
    present = {r.name for r in team}
    gates: dict[str, list[str]] = {}
    for phase, archs in GATE_ARCHETYPES.items():
        for arch in archs:
            role = arch_role[arch]
            if role in present:
                gates.setdefault(phase, []).append(role)
    # The Maker is the implementer routed DURING Build, never a gate-completion row.
    return gates


def print_team(title: str, team: list[Role], gates: dict[str, list[str]]) -> None:
    print(title)
    for r in team:
        print(f"  - {r.name:22} [{r.status:11}]  {r.why}")
    print("  auto-invocations by gate:")
    for phase in ("Spec", "Plan", "Build", "Verify", "Review"):
        if phase in gates:
            print(f"    - {phase:7} -> {', '.join(gates[phase])}")
    print()


# --- case 1: the load-bearing software case ----------------------------------
FILE_TRANSFER_CASE = Answers(
    q1_risk="security",
    q2_external=True,        # it transfers files over the local network
    q3_audience="web",       # browser-based
    q4_correctness=True,     # a corrupted or misdelivered file is real harm
    q5_design=True,          # a local peer-to-peer transfer protocol
)

# --- case 2: the agnostic research-writing case ------------------------------
RESEARCH_PAPER_CASE = Answers(
    q1_risk="inaccuracy",
    q2_external=True,            # relies on cited sources / empirical claims
    q3_audience="peer-reviewers",  # a defined readership
    q4_correctness=True,         # one wrong claim discredits the work
    q5_design=True,              # a deliberate thesis / argument structure
)

SOFTWARE_ROLE_NAMES = {"Engineer", "Security Reviewer", "QA / Test", "UX Reviewer", "Architect"}


def check_software() -> list[str]:
    team = assemble_team(FILE_TRANSFER_CASE, "software")
    gates = auto_invocations(team, "software")
    print_team('Case 1 - software: "a local-only browser-based file-transfer tool"', team, gates)

    failures: list[str] = []
    names = {r.name for r in team}

    if "Security Reviewer" not in names:
        failures.append("Security Reviewer is NOT on the team (Q2=yes / Q1=security must add it).")
    if is_fallback(team, "software"):
        failures.append("Team collapsed to the always-on core — selection logic is broken.")

    sec = next((r for r in team if r.name == "Security Reviewer"), None)
    if sec is not None:
        if sec.status != "built":
            failures.append("Security Reviewer must be a BUILT role, not a stub.")
        if "Q2" not in sec.why and "Q1" not in sec.why:
            failures.append("Security Reviewer WHY-line does not reference the answers (template smell).")

    if "Security Reviewer" not in gates.get("Plan", []):
        failures.append("CEO does not auto-invoke Security Reviewer at the Plan gate.")
    if "Security Reviewer" not in gates.get("Build", []):
        failures.append("CEO does not auto-invoke Security Reviewer at the Build gate.")

    stubs = [r.name for r in team if r.status != "built"]
    if stubs:
        failures.append(f"These roles are still stubs, must be built: {', '.join(stubs)}.")

    for phase, role in [("Spec", "Counterweight"), ("Plan", "Architect"), ("Plan", "Product Keeper"),
                        ("Build", "QA / Test"), ("Verify", "Counterweight"),
                        ("Review", "Product Keeper"), ("Review", "UX Reviewer")]:
        if role in names and role not in gates.get(phase, []):
            failures.append(f"CEO does not auto-invoke {role} at the {phase} gate.")

    if "Engineer" not in names:
        failures.append("Engineer (the standing implementer) is not on the team.")
    if any("Engineer" in v for v in gates.values()):
        failures.append("Engineer must NOT be a gate-completion reviewer — it is routed during Build.")

    return failures


def check_research() -> list[str]:
    team = assemble_team(RESEARCH_PAPER_CASE, "research-writing")
    gates = auto_invocations(team, "research-writing")
    print_team('Case 2 - research-writing: "a peer-reviewed paper with empirical claims"', team, gates)

    failures: list[str] = []
    names = {r.name for r in team}

    expected = {"Writer", "Sources Reviewer", "Fact-Checker", "Reader Advocate", "Argument Architect"}
    for role in expected:
        if role not in names:
            failures.append(f"Research team is missing {role}.")

    leaked = names & SOFTWARE_ROLE_NAMES
    if leaked:
        failures.append(f"Software role names leaked into the research pack: {', '.join(sorted(leaked))}.")

    if is_fallback(team, "research-writing"):
        failures.append("Research team collapsed to the always-on core — pack binding is broken.")

    if any(r.status != "built" for r in team):
        failures.append("A research role is not built.")

    for phase, role in [("Spec", "Counterweight"), ("Plan", "Argument Architect"),
                        ("Plan", "Sources Reviewer"), ("Build", "Fact-Checker"),
                        ("Build", "Sources Reviewer"), ("Verify", "Counterweight"),
                        ("Review", "Reader Advocate")]:
        if role in names and role not in gates.get(phase, []):
            failures.append(f"CEO does not auto-invoke {role} at the {phase} gate.")

    if any("Writer" in v for v in gates.values()):
        failures.append("Writer (the maker) must NOT be a gate-completion reviewer.")

    return failures


def main() -> int:
    print("HELM skill-pack smoke test")
    print("=" * 64)

    failures = check_software() + check_research()

    if failures:
        print("RESULT: FAIL")
        for f in failures:
            print(f"  x {f}")
        return 1

    print("RESULT: PASS")
    print("  ok  software: Security Reviewer on the team with an answer-derived WHY")
    print("  ok  software: not the always-on core; auto-invoked at Plan and Build")
    print("  ok  software: all roles built; Engineer is the implementer, not a gate reviewer")
    print("  ok  research: same engine binds the research pack's roles")
    print("  ok  research: no software role names leaked; gates fire for the bound roles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
