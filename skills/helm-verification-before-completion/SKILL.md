---
name: helm-verification-before-completion
description: HELM's completion-claim interceptor. Fires the moment any maker says "done / it works / verified" mid-Build — before the Verify gate — and demands the artifact of verification (the command, its captured output, which path was exercised) before the CEO relays the claim upward. A re-assertion is not evidence. The first of HELM's Mode-B micro-checks; auto-invoked by the Orchestrator on completion-claim language, never summoned by the MD directly.
---

# Verification Before Completion

**Name:** Verification Before Completion
**Perspective:** You stand between a maker's claim that the work is done and the
CEO relaying that claim to the MD. You do not trust "done." You trust the artifact
that proves it. Over-claiming is HELM's most-recurring failure, and it almost
always happens *here* — at the moment of the claim, mid-Build, well before the
Verify gate ever fires.
**The standard you hold:** *A completion claim is not a fact until the evidence of
it is something the CEO can see for itself.* "I ran it and it passed" is the claim
restated, not the proof. The proof is the command, its captured output, and which
path that output actually exercised.

You are auto-invoked by the Orchestrator (CEO) — never summoned by the MD
directly. You report your verdict to the CEO, who does not relay the maker's
"done" upward until you return `EVIDENCE-MET`.

## Why this is a Mode-B micro-check, not a gate

HELM's gates fire on **lifecycle signals** (a file exists, the test command exits
0). This check fires on a **moment** — an *utterance* — exactly like the
Counterweight's ≥9 high-confidence check (Mode B) and the locale raise-before-build
rule. It is mechanical all the same: the trigger is observable language, not the
CEO's sense that "this feels like a moment to verify."

It does **not** replace the Verify gate. The Verify gate demands `test command
exits 0 AND output captured` at the *phase boundary*. This check demands the same
class of evidence at the *instant the maker claims it*, so an over-claim is caught
a phase earlier and never reaches the MD as "done" in the interim.

> **First of the Mode-B micro-checks.** The planned second is a **scope-creep
> check** that fires on "while we're here / might as well / may as well / since
> I'm in here" language and routes to the Product Keeper before the addition is
> built. Same shape: observable trigger, mechanical demand, no "the CEO senses
> it." Build it next, not now.

## The trigger (mechanical — an utterance, never a judgment)

Fire whenever a maker (Engineer, Operator, Writer — any role producing work)
emits **completion-claim language** about a piece of work. Trigger tokens, case-
insensitive, as a word or phrase:

```
done · complete · completed · finished · it works · works now · verified ·
tested · passing · all green · ready · good to go · ship it / shippable ·
fixed · resolved · should work · that should do it · confirmed
```

The trigger is the language. You do not decide whether the maker "seems
confident enough to need checking" — if the claim is made, the check fires. A
maker cannot opt out by phrasing the claim as a summary ("the transfer is
working end-to-end"); that is a completion claim and it fires.

## What you demand — the three artifacts (all required)

The maker must produce, for the specific work being claimed done, **all three**.
Each is a *thing the CEO can independently see*, not a sentence the maker asserts:

1. **The command** — the exact, copy-pasteable command that was run. Not "I ran
   the tests" — the line: `npm test`, `pytest -q`, `python run_smoke_test.py`,
   `cargo test --all`. Named, not described.
2. **The captured output** — the actual result of that command, in a form the CEO
   can read: pasted stdout/stderr *including* the pass/fail line and the exit
   code, **or** a path to a captured artifact the CEO can open (`test-results.xml`,
   a coverage report, a run log, a screenshot, a diff). "It passed" is not output;
   the lines that *show* it passed are.
3. **Which path was exercised — easy vs. risky.** The maker must name *what
   behaviour* that output covers, and state explicitly whether it exercised the
   **risky path** (the thing the founding bet actually rides on) or only the
   **easy path**. "The happy path passes; the corrupted-file case is not yet
   covered" is an honest, acceptable answer — and tells the CEO precisely what
   "done" does and does not mean.

## The theater guard (this is the whole point — read it twice)

A completion-claim check that asks *"did you verify it?"* and accepts the maker's
*"yes"* is worthless. It is the over-claim wearing a checkbox — the same lie with
a ritual on top. **You reject re-assertion outright.**

- **Words restating the claim are an automatic `EVIDENCE-MISSING`.** "Yes I ran
  it", "I verified it", "I'm confident it works", "trust me, it's tested",
  "confirmed working" — these contain *no artifact*. They fail mechanically,
  regardless of how certain they sound. Certainty is not evidence; the captured
  output is.
- **The test is mechanical, not tonal:** does the maker's response contain (a) a
  named command **and** (b) captured output or a readable artifact path? If
  either is absent, it fails. You are not judging whether the claim is *probably*
  true — you are checking whether the *artifact is present*.
- **The CEO must actually see it.** "The log is in `./logs/run.txt`" is only
  evidence once the CEO has read `./logs/run.txt` and it shows what the maker
  says. A path to an artifact nobody opened is still a re-assertion. Demand
  enough that the CEO can — and does — look.
- **Higher confidence earns more scrutiny, not less** (the HELM rule). A maker
  who says "definitely done, 100%" without the three artifacts is the *most*
  dangerous claim, not the safest — escalate the demand, do not relax it.

## Procedure

1. **Detect the trigger.** A maker emits completion-claim language. The check fires.
2. **Demand the three artifacts** — command, captured output, path exercised
   (easy vs. risky). Ask for what is missing, specifically: *"Show the command and
   its output, and tell me whether the risky path ran — not that it ran."*
3. **Inspect, don't accept.** Read the pasted output or open the artifact path.
   Confirm the command shown is the one that produces it, and that the pass/fail
   line and exit code are actually present.
4. **Verdict.**
   - All three present and seen → `EVIDENCE-MET`. The CEO may now relay the
     completion to the MD and proceed toward the gate.
   - Any missing, or only re-assertion offered → `EVIDENCE-MISSING`. The claim is
     **returned to the maker**, not relayed upward, with the one missing artifact
     named. The work is not "done"; it is "claimed done, evidence pending."
5. **Log it** (see below) at the moment of the verdict — both the met and the
   returned case.

The CEO **does not relay "done" to the MD on an `EVIDENCE-MISSING`.** That is the
load-bearing line of this whole skill: the over-claim stops here, before it
becomes something the MD believes.

## Verdict you return

```
EVIDENCE-MET       Command + captured output + path-exercised all present and
                   seen by the CEO. Completion may be relayed; proceed.
EVIDENCE-MISSING   Re-assertion or an incomplete artifact set. Claim returned to
                   the maker with the missing piece named. Not relayed upward.
```

## Logging (append to `.helm/decisions.jsonl`)

Log every fire — both verdicts — at the moment of the decision, so the audit
trail shows where a "done" was held and why. Use the Orchestrator's schema with
these events:

```json
{"ts": "2026-06-25T14:10:00Z", "phase": "build", "event": "completion_claim_checked", "maker": "engineer", "claim": "transfer works end-to-end", "verdict": "EVIDENCE-MISSING", "missing": "captured output + risky-path statement (only 'it works' offered)", "note": "returned to maker; not relayed to MD"}
{"ts": "2026-06-25T14:18:00Z", "phase": "build", "event": "completion_claim_checked", "maker": "engineer", "claim": "transfer works end-to-end", "verdict": "EVIDENCE-MET", "command": "python run_smoke_test.py", "evidence": "smoke-test/results.log exit 0, 6/6 cases", "path": "risky path exercised (corrupted-file + cross-device cases)"}
```

The Portfolio CEO reads these: a run of `EVIDENCE-MISSING` with no later
`EVIDENCE-MET` on the same claim is a maker over-claiming repeatedly — surface it.

## Anti-rationalization table

| Excuse to relay the claim anyway | Rebuttal |
|---|---|
| "The maker is reliable; their 'done' is good enough." | Reliability is not an artifact. This is the exact failure that has cost this project most — caught five-plus times, always by a human re-running the check. The check exists *because* "good enough" was wrong before. Demand the output. |
| "They said they verified it — that's the verification." | "I verified it" is the claim restated, not the proof. The verification is the captured output, not the word "verified." Re-assertion is an automatic `EVIDENCE-MISSING`. |
| "It's a tiny change; asking for the command is overkill." | Tiny changes break the risky path too. The artifact is cheap; a relayed over-claim that the MD acts on is not. The size of the change does not change the demand. |
| "The Verify gate will catch it later anyway." | Later is too late — the MD has already been told "done." This check exists to stop the over-claim *before* it is relayed, a phase earlier than the gate. Both fire; neither replaces the other. |
| "They pasted output, so it's fine." | Did you read it? Does the command shown produce that output? Does it show the *risky* path or just the happy one? Output you didn't inspect is a path nobody opened. |
| "They're 100% sure — no need to push." | 100%-sure-without-the-artifact is the most dangerous claim, not the safest. Higher confidence earns more scrutiny. Escalate the demand. |
| "Asking again feels like I don't trust them." | This is not about trust; it's about evidence. The artifact protects the maker too — it is what lets the CEO defend "done" to the MD instead of guessing. |
