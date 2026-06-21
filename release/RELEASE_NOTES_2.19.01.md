# Release Notes 2.19.01 — Recipe-First Lean Clean Final

## Status

Final lean-clean source package.

## Changes

- Removed raw inactive archive/history payload from the main source package after user approval.
- Retained key information in `MASTER_LESSONS_LEARNED.md`, `MASTER_BUILD_RECIPES_AND_PLACEMENT_GUIDANCE.md`, `CHANGELOG.md`, active rules, data ledgers, and validation tools.
- Retained recipe-first feature routing, wall-shell enclosure recipe, part placement aid ledger, feature route index, AI Review bundle intake, and validation gates.
- Retained a single running changelog instead of many historical release-note files.
- No separate runtime pack is maintained; the source package itself is the lean operating package.

## Validation

Run `python release/release_check.py` from the package root.
