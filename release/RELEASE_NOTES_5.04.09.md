# Release Notes — 5.04.09

**Date:** 2026-06-20  **Type:** patch (harmonization Step 3 — complete)  **Supersedes:** 5.04.08

## Changed
- De-versioned the remaining 54 docs; version-callout ledger 118 -> 0.
- `DOME_STUDY_LESSONS.md` rewritten to lead with the proven measured method (supersession honored).
- Fixed the `## 5.00.00` kickoff/banner headers.

## State
- No governance/active-build doc carries a version-section call-out. Versions live only in CHANGELOG, release notes, reports/, archive/, and the title/baseline anchors. The `version_callout_check` ledger is empty and enforced.

## Gate
`release_check.py` -> RELEASE GATE: PASS.
