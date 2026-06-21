# MASTER LESSONS LEARNED

Status: active build guidance. This file replaces scattered revision notes and raw failure-example loading.

Use this file as an index of distilled lessons. When a lesson becomes obsolete, replace it here with the working rule or move it to the inactive archive ledger with the replacement named.

## Universal build method

- Use real NMS Builder parts only. Do not generate raw Blender primitives, proxy meshes, or FBX-imported geometry for generated builds.
- Use the part map first for ObjectID, dimensions, centers, likely role, and spacing. Use working JSON first when available because exported JSON contains serialized transform truth.
- Use raw FBX/manual mesh inspection only as fallback when the part map and JSON evidence do not answer origin, local-axis, contact, or shape questions.
- Emit a placement plan before code for recognizable/focal builds.
- Split every known feature into locked invariants and allowed parameters before variation.
- Validate with run_gate and the relevant specialized checks before publishing.

## JSON and transform lessons

- Working exported JSON is foundational evidence whenever relevant. Do not repair placement from memory, generic rx/rz, screenshots alone, or FBX-only reasoning when relevant JSON exists.
- JSON → Python recreation uses the validated stack: COORD_MODE XnZY, AXIS_MODE RIGHT_AT_UP, BASE_ROTATION_MODE POST_RX90, POST_BASELINE_CORRECTION LOCAL_Y_180, SCALE_MODE UP_LENGTH_UNIFORM.
- Python-generated builds audit back through exported JSON using the known serialized position relationship: Blender/Python `(x, y, z)` → JSON `Position = [x, z, -y]`.
- Up/At vector magnitudes are scale evidence. Do not assume non-uniform scale survives unless exported JSON proves it.

## Part map / placement aid lessons

- Part map fields should be treated as the operational geometry layer: ObjectID, FBX path, extents, centers, snap group, likely role, spacing rule, and promoted placement notes.
- The part map still needs enrichment for native local axis, default orientation, part-specific overrides, valid scale behavior, anchor/contact roles, JSON recipe links, and failure notes.
- If part map guidance conflicts with working JSON from the current build, current-build JSON wins for that build's geometry.

## Orientation and part-specific exceptions

- Default rx/rz conventions are fallback only. Part-specific overrides and working JSON precede generic orientation.
- BILLBOARD is a proven vertical sign-plane exception. It must not inherit generic facade rx=90 behavior.
- Bridge, stair, ramp, pipe, rail, corridor, and skybridge modules need endpoint/path basis, not independent default rotations.

## Assembly and anti-float lessons

- Assembled subsystems must prove contact/connection: stairs, ramps, bridges, rails, towers, roof crowns, wall bays, machinery, vehicles, airlocks, and cave interiors.
- A part name, role label, or comment saying “connected” is not proof. The check must be geometric.
- Floating structural parts are failures unless explicitly requested and approved for that run.

## Visual/reference intake lessons

- Reference images are not automatically macro direction. Ask or classify the intended lesson: mood, scale, part use, pathing, material/color, layout, failure, or specific technique.
- Convert useful references into text lessons, part candidates, recipe signatures, or project-study notes rather than loading image history by default.

## Project-specific lessons retained as reusable guidance

- Gotham/dark-city direction: use dense skyscrapers, rooftop use, narrow walkways, dark palette, ominous lighting, crime/danger props, and black vehicle/corvette-inspired elements. Treat as project direction, not universal build law.
- Corvette mode: 95m safe / 100m absolute envelope for total footprint, including non-corvette decoration attached to the build.## Extracted archive/report lessons retained

The inactive archive and historical reports were removed from the lean source after the following durable lessons were promoted:

- Request routing must happen before code. Loading rules is not enough; each response must show the applied bundle and gate result.
- JSON-derived known features, especially airlocks/iris doors, must route to their recipe/signature before part-map component lookup.
- Spires, domes, rounded shells, cylindrical habitats, vehicle hulls, and curved roofs need curve/ring/surface/contact recipes rather than random dense placement.
- Power utilities are excluded by default unless the user explicitly requests power-system scripting.
- Continuous trim, rails, rims, stairs, walkways, bridges, and shell parts must prove contact/connection geometrically.
- Failed scripts that create raw Blender mesh, proxy objects, or NMS-looking non-plugin geometry are invalid; generated builds must use real NMS Builder parts through the plugin add_part/template-copy path.
- Screenshot/reference examples should become text lessons, recipe candidates, or project-study summaries, not active runtime image history.
- Project-specific notes such as Gotham city style, alien megatemple direction, or Taj Mahal case-study visuals are retained only as reusable guidance when they affect validated build methods.

If a removed historical file is later needed, use the removed-file ledger to identify the original path and recover it from the superseded 2.19.00 candidate or 2.18.01 rollback package.



## PIPE/BUBPIPE verified-data exception

User-confirmed evidence showed that the verified Blender extraction overlay can be misleading for `PIPE` and the `BASE_BUBPIPE*` family. `PIPE` may be invisible/zero-bbox in Blender while valid in-game. BUBPIPE parts may show clean bbox/rotation in Blender but produce different in-game appearance/orientation. For connected pipe assemblies, RX90 may correct individual pieces but does not prove bend continuity or local/global transform correctness. Mark pipe-family rows `GAME_VALIDATION_REQUIRED_PIPE_FAMILY` until focused in-game or exported-JSON validation confirms assembly behavior.


## lesson — PIPE/BUBPIPE contextual connector behavior

User-provided JSON and in-game screenshots show that `PIPE` and `BASE_BUBPIPE*` must be treated as contextual connector parts. Blender visual/bbox extraction can be misleading or invisible, while exported JSON transforms are still useful evidence. Observed pipe graph deltas are approximately 2.0 units along local Up/At/derived Right axes. RX90 may repair isolated orientation but does not validate pipe assembly continuity.

## lesson — component validation is not assembly validation

The castle ramp/stair review proved that verified component data can still produce failed assemblies. Build generation must distinguish object-level mechanics from assembly-level conformance. High-risk assemblies require named methods and acceptance criteria.

## Roof-build session lessons (2026-06-20, 5.04.00) — BLENDER-tier
- **Apex-swirl** is interleaved 16-facet rings colliding at a tiny apex radius. Cap before convergence (SOLID_FINIAL_CAP).
- **Outward-bulge spikiness** is positive tilt and/or the x1.05 corner-facet outset. Keep tilt inward; drop the outset.
- **S_LARGETRYE0 is a fan/star vault, not a pyramid** — never a clean finial point. Cost several iterations before it was caught.
- **S_ROOF_M_WIN shingles and cannot smooth** (worse with RZ180). Smooth glass needs a flat panel or vertical facets.
- **Part width vs base**: _M diagonal walls (5.84) splay on an N=4 small base; N=8 octagon is the reliable minimum.
- **Tier gaps** come from ring spacing > facet vertical extent; **compound spires collapse** if the lower stage truncates too narrow before a collar.
- **Process**: screenshot-verify each step; checkpoint-save/export each batch (a crash wiped the live scene to default and only an autosave recovered it).
- All encoded into data/GEOMETRIC_FAILURE_MODE_INDEX.json + data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json and surfaced per build by the resolver's CREATIVE_CONTEXT.

## Retired gothic-church CAPA — lesson retained (2026-06-20)
Project is dead; the probation flag was lifted, but the failure is worth keeping:
- **Mistake:** reused S_RAMP as decorative buttresses with guessed rotations, marked it EXPERIMENTAL_VARIANT, and skipped the validated STAIR_RAMP_ENDPOINT_RECIPE the sheet surfaced (SHEET_NOT_UTILIZED).
- **Lesson/corrective logic:** decorative/experimental framing never waives a required_method or negative-knowledge constraint; the EXPERIMENTAL label is not a bypass; if the sheet surfaces a method for a used part, use it or explicitly flag divergence (never silent-skip). Decorative scale/position is free; a required placement method is not.
- Encoded in rules/PLACEMENT_MECHANICS_VS_CREATIVE_STYLE_SEPARATION_RULE.md (5.04.01 worked example).
