# Release Notes — 5.01.00

**Operational reachability layer.**

5.00.00 fixed the doctrine; 5.01.00 fixes runtime reachability.

## New build loop
Router -> declare ObjectIDs -> `part_context_resolver.py --ids ... --intent ...` -> small packet -> build from packet -> BUILD COMPLIANCE MANIFEST -> `compliance_manifest_check.py <manifest> .` PASS.

## What changed
- `00_OPERATING_CARD.md` — single always-hold page.
- `validation/part_context_resolver.py` — PROJECT BUILD PLACEMENT PACKET; MANDATORY (forced) vs CREATIVE (offered) split.
- `data/RULE_PART_APPLICABILITY_MAP.json` + `validation/rpam_coverage_check.py` — every rule mapped to parts/families.
- `validation/compliance_manifest_check.py` — hardened to re-read sources (real enforcement: source_ref/ObjectID in file, tier highest-applicable, method authorized).

## Honest boundaries
- The resolver only runs where a tool reads disk (Blender MCP / code execution). In a plain chat with no file access, paste a precomputed packet.
- RPAM is auto-seeded: 8 NEEDS_REVIEW + the 19 part-specific entries still warrant human review.
- run_gate does not yet enforce packet coverage (used ObjectIDs subset of packet); that wiring is the next open item.
