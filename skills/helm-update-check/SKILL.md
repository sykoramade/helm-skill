---
name: helm-update-check
description: HELM's startup update check. Mechanically compares the installed HELM version against the latest published on GitHub and, if behind, recommends the one-line update command to the MD. Runs once per session, network-optional (skips silently offline), and never modifies the install itself. Invoked first by the Orchestrator, Onboarding, and Portfolio CEO.
---

# HELM Update Check

> HELM ships as markdown, so there is no background updater. Instead, the
> entry-point skills run this check **once at the start of a session**: compare
> the installed version to the latest published version and, if you're behind,
> hand the MD the exact one-liner to update. It checks and recommends
> automatically; it never changes the install (that is the MD's `/plugin`
> command to run).

## When to run

- **Once per session**, as Step 0 of `helm-orchestrator`, `helm-onboarding`, or
  `helm-portfolio` — whichever the MD enters through. If the check already ran
  this session, skip it.
- It must **never block work.** Run it, surface a single line if an update
  exists, and continue. If anything fails (offline, no `gh`, rate-limited), skip
  silently — no error to the MD.

## The check (mechanical)

1. **Read the installed version.** Read the `version` field from this pack's own
   `.claude-plugin/plugin.json` (it ships next to the `skills/` directory). Call
   it `INSTALLED`.
2. **Fetch the latest version.** Read the same field from the repo's `main`,
   using whatever the host has:
   - `gh api repos/sykoramade/helm-skill/contents/.claude-plugin/plugin.json --jq '.content' | base64 -d` (then parse `version`), or
   - `WebFetch` / `curl -s https://raw.githubusercontent.com/sykoramade/helm-skill/main/.claude-plugin/plugin.json` and parse `version`.

   Call it `LATEST`. If neither path is available or the fetch fails, **stop here
   silently** — no network, no nag. (On a host without `gh`, `WebFetch`, or
   `curl` — e.g. a plain system prompt — the check is simply a no-op; it never
   errors and never blocks, consistent with HELM's local-first, no-dependency
   promise.)
3. **Compare as semver** (`MAJOR.MINOR.PATCH`, numeric component by component).
   - `LATEST == INSTALLED` → up to date. Say nothing (or, only if the MD asked
     "am I current?", confirm in one line).
   - `LATEST > INSTALLED` → an update is available. Surface the recommendation
     (below).
   - `LATEST < INSTALLED` → you're ahead of `main` (a dev build); say nothing.

## The recommendation (what the MD sees)

One plain line, decision-first, then continue with their actual request:

> *"HELM v{LATEST} is out (you're on v{INSTALLED}). To update, run:
> `/plugin marketplace update helm-skill` then `/reload-plugins`. Want to do that
> now, or carry on?"*

Rules:

- **Recommend, don't apply.** You cannot run `/plugin` commands yourself, and
  changing an installed plugin is the MD's call. Surface the one-liner; let them
  run it.
- **One line, once.** Do not repeat the nag later in the session. Log it if a
  decision log is in scope, but never let the check derail the task the MD opened
  the session for.
- **Quiet when current.** No "you're up to date!" noise unless the MD asked.

## Why it's safe

- **Read-only and local-first.** The check reads two small JSON files and
  compares two strings. It writes nothing, installs nothing, and touches no
  project state.
- **Network-optional.** With no network (or no `gh`/fetch tool), it is a no-op —
  consistent with HELM's local-first, no-telemetry promise. It only ever reaches
  out to GitHub's public repo to read a version number, and only to recommend.
