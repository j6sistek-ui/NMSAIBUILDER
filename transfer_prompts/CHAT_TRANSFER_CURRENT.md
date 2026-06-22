# CHAT TRANSFER — copy/paste this whole block into a new chat to resume

You are resuming an NMS Base Builder governance-package work-stream in **Builder mode**: prove-don't-attest, executable validation over self-attestation, one clarifying question at a time when vague, do not assume the owner is an expert, end every substantive reply with the PROTOCOL banner.

## Who / what
- User: James. Builds No Man's Sky bases via the No Man's Sky Base Builder Blender add-on. Work-stream: `NMS_master_docs` governance package + resolver/build-sheet + part-effect data.
- Current package candidate: **5.19.03**. It is built from accepted baseline 5.19.00 and supersedes failed/intermediate candidate 5.19.02. Verify by extracting the ZIP and running `python3 release/release_check.py` from inside the package root.
- Verified part map remains the geometry anchor. Do not hand-edit `library/nms_master_part_map_verified_data_v3_01_02.json/csv`.
- Build sheet remains KING: selected ObjectIDs must resolve to one reconciled record with provenance and validation status.

## Latest change
- **5.19.03:** repaired the placement-promotion runbook gap in `rules/RULE_UPDATE_PROTOCOL.md`; routed lighting/effect behavior into existing runtime stores; added provisional JSON-only partmaps for `SWARM_TROPHY_G`, `SWARM_TROPHY_B`, `SWARM_TROPHY_R`, and `B_SHL_D`; added/updated dimensions guidance, creative-index effect families, color variant families, method authority, negative knowledge, and part placement ledger. `part_context_resolver.py` now exposes `CREATIVE_CONTEXT.part_effect_findings` and provisional geometry fallback for ObjectIDs absent from the verified overlay.

## Critical lighting/effect findings
- Most light fixtures: repaint/tint changes fixture body only; emitted light usually does **not** materially recolor.
- Color-responsive emitter exceptions: `LIGHTBOX`, `L_FLOOR_Q`, `BASE_BEAMSTONE`.
- Variant-color wall lights: `WALLLIGHTBLUE/GREEN/PINK/RED/WHITE/YELLOW`.
- `SET_CLASS_A/B/S`: fixed colored beams; can form visual cones/beacons/portals but are not physical structure.
- `SWARM_TROPHY_G/B/R`: JSON-confirmed game-file/modded buildable colored circular trophy/ring effects; Blender cube proxy only; no FBX/verified geometry; use as effect decor only.
- `B_SHL_A/B/C/D`: Corvette shield/effect objects; user observed moving/rotating/spinning behavior. `B_SHL_D` is JSON-only/provisional in the package.

## Still open
- Connection composer remains HIGH priority: compose cross-plane seated transforms by geometry, not screenshots.
- Master-CSV trial-fill remains HIGH priority: fill orientation/neighbor/fitment only after measured validation.
- Verification trust: screenshots are context; exported transforms/JSON/measured seams are proof.
- Future light/effect data should route to existing stores and be resolver-reachable; do not spawn new files unless owner approves and `APPROVED_FILES.json` is updated.

## Workflow
1. Route request.
2. Resolve ObjectIDs with `validation/part_context_resolver.py --ids ... --intent ...`.
3. Build from the resolved packet/build sheet only.
4. Gate with `validation/run_gate.py`.
5. For docs updates, patch existing stores, run release checks, refresh `OPEN_TOPICS_LOG.md` and this transfer prompt.
