# Release notes — NMS master docs 5.18.00

## The build sheet now hands over the complete per-part spec

Previous releases restored the curated guidance (5.16) and the concrete snap step (5.17) but forwarded them as separate dicts. The build sheet's purpose was always to deliver the *whole* per-part spec, mapped from data that already exists in the library. This release does that: every part in MANDATORY_PLACEMENT_CONTEXT.parts[oid] now carries a `placement_spec` with five sections:

- **orientation** — default rotation, the world footprint under RX90/RY90/RZ90 (so the build knows how the footprint changes per facing), whether the part has a registered orientation override, ring-orientation guidance
- **scaling** — world size at scale 0.5 / 1.0 / 1.5 / 2.0, with the `step = world_size * scale * 0.92` rule
- **placement** — the concrete `snap_spacing` (connection authority), the extent-based `SpacingRule` as fallback, placement guidance, ring formula, recipe candidates
- **role** — likely/validated role, mechanics-use recommendation, known-good uses
- **cautions** — known issues, lessons, decorative-proxy cautions, validation flags, forbidden status

This folds in and replaces the `per_part_curated_guidance` and `per_part_snap_spacing` dicts from 5.16/5.17. It is sourced entirely from existing library fields (VerifiedRX90/RY90/RZ90WorldSize, VerifiedScale*WorldSize, SpacingRule, PlacementGuidance, LikelyRole, etc.) — no new data, just the mapping that should have been there. The MANDATORY mechanical integrity check is unaffected (placement_spec is additive); `build_sheet_check --self-test` passes.
