# Release Notes — 5.04.06

**Date:** 2026-06-20  **Type:** patch (harmonization Step 1)  **Supersedes:** 5.04.05

## Added
- `rules/SINGLE_CURRENT_STATE_SOURCE_RULE.md` — the standard: current-state only in governance/active-build docs.
- `validation/version_callout_check.py` + `validation/version_callout_debt.json` — executable enforcement + burn-down ledger, wired into `release_check.py`.

## Baseline recorded (not yet fixed)
- 58 governance/active-build docs carry 185 `## X.YY.ZZ` section call-outs. Top: README (27), REQUEST_ROUTER_CHECKLIST (15), 02_GENERATOR_CONTRACT (13), RULE_APPLICATION_MATRIX (12), PLACEMENT_RECIPE_LIBRARY (7), 00_KICKOFF_INTAKE_GATE (7).
- These are allowlisted at their current counts; the gate blocks any increase or new offender. Steps 2-3 de-version them and `--refresh` the ledger toward empty.

## Gate
`release_check.py` -> RELEASE GATE: PASS.
