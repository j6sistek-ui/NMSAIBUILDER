# Release Notes — 5.04.08

**Date:** 2026-06-20  **Type:** patch (harmonization Step 2 — router trio)  **Supersedes:** 5.04.07

## Changed
- `rules/REQUEST_ROUTER_CHECKLIST.md` -> de-versioned; now holds the single authoritative bundle map (trigger/route -> docs).
- `RULE_APPLICATION_MATRIX.md` -> de-versioned; routing duplication removed and pointed to the router; matrix-unique tables kept.
- `02_GENERATOR_CONTRACT.md` -> de-versioned into themed current clauses; all technical specifics preserved.

## Stale refs resolved
- spire notes -> curvature grammar + MASTER_LESSONS_LEARNED; airlock skeleton -> AIRLOCK_IRIS_* rules; power -> UNIVERSAL_RULES + INCLUDE_POWER_UTILITY=False.

## Ledger
- 158 -> 118 call-outs (57 -> 54 files). Remaining top: VALIDATION_GATE_HARDENING_RULE (5), NMS_BUILDER_EXECUTION_KERNEL (5), then the rules/ tail.

## Gate
`release_check.py` -> RELEASE GATE: PASS.
