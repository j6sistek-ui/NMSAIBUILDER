# Release Notes — 5.04.00

**Date:** 2026-06-20  **Type:** minor (creative findings + runtime wiring)  **Supersedes:** 5.03.00

## What changed
A full live Blender build session (~21 castle roof/spire modules) produced reusable techniques and root-caused failure modes. This release encodes them AND wires the key knowledge into runtime so future builds operate with the findings automatically — without forcing any aesthetic guidance through the mechanical gate.

## New / changed files
- **NEW** `data/GEOMETRIC_FAILURE_MODE_INDEX.json` — advisory geometric-failure index (parallel to negative knowledge, never gated).
- **NEW** `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` — the live creative index the resolver referenced; now populated (part character, placement/orientation recipes, color-variant families, fit rules, findings 20-25).
- **CHANGED** `validation/part_context_resolver.py` — CREATIVE_CONTEXT populated per build (part_character + applicable_failure_modes + recipes + fit_rules); self-test extended; PASS.
- **CHANGED** `00_OPERATING_CARD.md`, `02_TECHNIQUE_TOOLKIT.md`, `MASTER_LESSONS_LEARNED.md`, `CHANGELOG.md`, `release/VERSION.json`.

## Firewall preserved
All new knowledge lives in CREATIVE_CONTEXT (offered, evaluated, never gated). MANDATORY_PLACEMENT_CONTEXT is unchanged. The resolver self-test asserts the advisory fields populate for a roof build AND that they do not leak into the forced mechanical surface.

## Evidence tier
BLENDER-tier (visual). Nothing here is GAME_VALIDATED. The open church-build CAPA is unaffected.
