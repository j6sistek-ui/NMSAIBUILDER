# Release Notes — 5.19.03

## Summary

This patch maps user-supplied lighting/effect behavior and JSON-only buildable ObjectIDs into existing runtime-linked stores while preserving the verified part map as the geometry anchor. It also repairs the placement-promotion runbook gap discovered in the failed 5.19.02 candidate.

## Key changes

- Added an end-to-end placement/effect behavior promotion runbook to `rules/RULE_UPDATE_PROTOCOL.md`.
- Added provisional JSON-only records for `SWARM_TROPHY_G`, `SWARM_TROPHY_B`, `SWARM_TROPHY_R`, and `B_SHL_D`.
- Added lighting/effect findings for color-responsive emitters, fixture-tint-only lights, wall-light color variants, SET_CLASS beam-cone effects, Race Booster purple glow, Planet Holo display, Base Shell colorable display, and Corvette animated shield effects.
- Updated `part_context_resolver.py` to surface `CREATIVE_CONTEXT.part_effect_findings`.
- Regenerated part-placement derived files and `discover_by_quality`.

## Guardrails preserved

- Verified extraction overlay was not hand-edited.
- Creative/effect findings remain informative and do not override placement precedence, snap authority, negative knowledge, or verified geometry.
- JSON-only/provisional objects are blocked from structural/snap/verified-map claims.
