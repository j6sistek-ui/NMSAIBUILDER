# Session Onboarding Checklist Rule — READ/SKIPPED proof of read  (introduced 5.00.00)

## Status

**MANDATORY.** The output of new-chat onboarding is a checklist. On the first
build-related message of a session, before any design or code, emit an
`ONBOARDING CHECKLIST` that lists every document the session relies on and marks
each **READ** or **SKIPPED (reason)**. This converts "I loaded the docs" from an
unverifiable claim into a visible artifact.

## Required form

```text
ONBOARDING CHECKLIST (session)
Package: <name> rev <X.YY.ZZ>
- 00_FOUNDATIONAL_DOCTRINE.md ................. READ
- 00_START_HERE_CURRENT.md .................... READ
- 00_KICKOFF_INTAKE_GATE.md ................... READ
- rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md ... READ
- data/PLACEMENT_PRECEDENCE.json .............. READ
- <mode gating docs> .......................... READ
- <everything else in PACKAGE_MANIFEST> ....... SKIPPED (not in scope for <mode>)
Doctrine acknowledged: precedence is the first duty; no build without a verified manifest.
```

Skipping is allowed and expected — you do not read all 298 files — but every file
must be accounted for as READ or SKIPPED-with-reason. An onboarding output that
does not enumerate the package is incomplete.

## Source Readiness vs Builder Readiness

This checklist proves **Source Readiness** only: the documents are in context. It does NOT prove the AI can build. **Builder Readiness** requires passing the gauntlet in `ONBOARDING_VALIDATION_BUILD.md` (real micro-build -> first gate -> failure handled if any -> second gate -> `BUILDER READINESS: READY`). Do not request the user's build objective on the strength of the checklist alone.
