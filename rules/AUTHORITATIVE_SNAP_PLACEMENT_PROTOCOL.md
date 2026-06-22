# Authoritative Snap Placement Protocol — 4.00.00

## Status
**Active required governance rule (Major release 4.00.00).**
For any part that belongs to an add-on snap group, this is the PRIMARY placement source and supersedes
derived/heuristic placement for join geometry.

## Why (coordinate/transform breakthrough)
The "No Man's Sky Base Builder" Blender add-on ships its COMPLETE snap system as data. These files ARE the
placement source of truth:
  <addon>/resources/snapping_info.json   per group: parts[], snap_points{NAME:{matrix 4x4 (local), opposite}}
  <addon>/resources/snapping_pairs.json  group->group connectivity via named source/target point lists
Distilled, self-contained copy shipped with this package:
  library/authoritative_snap/relational_map_combined_v01.json
Placement geometry no longer needs to be derived from repeated observed adjacency for parts covered here.

## Provenance hierarchy (overrides prior default)
1. AUTHORITATIVE_ADDON_SNAP — snapping_info/pairs + combined map. Source of truth for join geometry.
2. DERIVED_ADJACENCY — PART_PLACEMENT_MAP_SCHEMA observed-offset method. FALLBACK for parts with NO snap group (~919 parts: decor/special types).
3. HEURISTIC/RECIPE — spacing/scale recipes; design guidance only, never overrides lane 1.
Part in a snap group -> lane 1. Part not in any snap group -> lane 2, then 3.

## RULE ASP-1 — Snap points are read, by name
- Scope: all parts present in snapping_info.json groups.
- Select snap points BY NAME via snapping_pairs connectivity; NEVER by nearest world position. Parts carry
  multiple CO-LOCATED snap points (orientation/quarter variants) at the same position; nearest-position
  selection picks the wrong frame.
- Problem prevented: wrong-orientation joins from picking a co-located sibling point.
- Status: VALIDATED (snap-validated). Source: library/authoritative_snap/map_vs_live_validation_v01.json
  (file points coincide with live snaps to 0.0 gap; within-group AND cross-group).

## RULE ASP-2 — Placement composition formula
- B_world = A_world @ Ma @ FLIP @ inv(Mb)
  Ma = chosen snap point on placed part A (local 4x4); Mb = mating NAMED point on B; FLIP = 180 deg about Y.
- Reconstructs FULL pose (position AND orientation) to 0.0 pos / 0.0 deg across triangle, floor+floor, and
  the asymmetric floor+wall (cross-group).
- Status: VALIDATED (snap-validated). Source: library/authoritative_snap/formula_validation_v01.json.
- Note: co-located variants yield equivalent alternate (point+flip) combos; canonical = named-opposite pair + 180 deg Y.

## RULE ASP-3 — NMS export pose
- Export via bpy.ops.object.nms_save_data(filepath=...): per object {ObjectID(^prefix), Position, Up, At}.
- No-Blender derivation: Position = world translation; Up = world +Y axis; At = world -Z axis (observed
  convention; confirm via export when Blender is available).

## RULE ASP-4 — Operators (Blender-equipped chats) [OBSERVED_FACT, Blender 5.1]
- spawn:  bpy.ops.object.list_build_operator(part_id=..., tooltip=...)
- snap:   bpy.ops.object.nms_snap(...)  — moves selected onto active. CYCLING ARGS ARE INERT (default snap
          only). Do not rely on operator cycling to reach alternate points; use named points from the map.
- export: bpy.ops.object.nms_save_data(filepath=...)

## RULE ASP-5 — Join-quality / no-float check
- Verify a join with VOLUMETRIC INTERIOR SAMPLING (fraction of points sampled inside B that are also inside
  A): CLEAN / FLOATING_GAP / MINOR_OVERLAP / HEAVY_OVERLAP. Do NOT use axis-aligned bbox overlap (false
  positives on rotated parts) or surface-vertex tests (false negatives on coincident parts).
- Complements, does not replace, the no-float gate in DISCONNECTED_ASSEMBLY_HARDSTOP_RULE.md.

## Validation status / accuracy dial
- The add-on-sourced relational map is SNAP_VALIDATED: matches the add-on's own live snaps to 0.0 gap and the
  composition formula reproduces full pose to 0.0/0.0 deg.
- This advances the PART_PLACEMENT_MAP_SCHEMA accuracy dial: for snap-group parts,
  placement GEOMETRY is sourced authoritatively and does NOT require a per-part map-only proof build to be
  trusted positionally.
- GOLD tier remains GAME_VALIDATED (in-game confirmation). Snap-validated != game-validated. Aesthetic
  "masterful" signoff still per user.

## Exceptions
- B_TRIFLOOR (Salvaged) is NOT a member of the TRI snap group -> no triangle snap points -> snapping
  misfires to a coincident overlap. Per-part exception; use other TRI materials or place manually.
- ~919 of ~2097 parts have no snap group (decor, etc.): lane-2 fallback applies.
- Cube floors / other special structural types: own checks; not covered by core snap-group joins.
- Flora/terrain-grounded no-float exception: unchanged (see usage rule).

## Source / validation note
- Authoritative: add-on resources/snapping_info.json + snapping_pairs.json (Blender 5.1, no_mans_sky_base_builder).
- Shipped data: library/authoritative_snap/{relational_map_combined_v01.json, map_vs_live_validation_v01.json, formula_validation_v01.json}.
