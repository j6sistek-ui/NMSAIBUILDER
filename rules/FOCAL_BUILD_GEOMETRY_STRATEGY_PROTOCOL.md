# Focal Build Geometry Strategy Protocol

## Status

Mandatory for recognizable focal structures: ships, logos, animals, symbols, sculptures, buildings with a named silhouette, or any request where the visual identity is the objective.

## Principle

A focal build is not validated by part usage alone. It must be designed as a geometric object first, then populated with parts from the part maps.

## Mandatory construction plan

Every focal build script must include:

```python
GEOMETRY_CONSTRUCTION_PLAN = {
    "construction_mode": "silhouette_extrusion | curve_follow | edge_graph_shell | surface_patch | hybrid",
    "target_read": "front | side | top | three_quarter",
    "recognizable_features": [...],
    "primary_part_families": [...],
    "placement_derivation": "edge_graph | curve_tangent | surface_normal | validated_recipe",
    "declared_openings": [...],
    "forbidden_methods": ["centroid_scatter", "generic_visual_sprinkle"],
    "visual_conformance_checks": [...]
}
```

## Required methodology

```text
1. Identify the visual features that make the object recognizable.
2. Pick the construction mode before placing parts.
3. Derive every placement from a curve, edge graph, surface graph, or validated recipe.
4. For single-part builds, use the part as a geometric primitive, not a decorative token.
5. Declare the intended view and objective checks.
6. Stop after repeated objective failures and update the protocol/gate before generating more variants.
```

## Prohibited methodology

```text
- scattering parts into a region hoping the aggregate resembles the object
- using a validated part family while ignoring the specific contact/edge/orientation rules
- replacing a failed geometry strategy with another ad-hoc strategy without a construction plan
- claiming success because parts exist or because manifests are present
```

## Validation posture

If objective conformance cannot be checked automatically, the gate must say `Blender runtime NOT_RUN`, `objective conformance NOT_RUN`, or `visual review pending`. Do not claim PASS.


## Curve-follow transform contract (absorbed from CURVE_FOLLOW_TRANSFORM_PROPAGATION_PROTOCOL)
## Status

Mandatory when a build uses a part repeatedly along a curve, spiral, ring, path, outline, rib, wing edge, rail, or decorative sweep.

## Principle

Skilled manual builders often create strong shapes by repeating a single part along a curve with controlled tangent, spacing, roll, and offset. Generated builds must treat this as transform propagation, not as independent stamping.

## Required fields

Generated scripts using curve-follow placement must declare:

```python
CURVE_FOLLOW_CONTRACT = {
    "path_name": "...",
    "part_id": "...",
    "step_distance": ...,
    "frame_rule": "tangent + normal + binormal",
    "roll_rule": "...",
    "offset_rule": "...",
    "start_stop_policy": "...",
    "contact_or_overlap_policy": "edge_contact | controlled_overlap | visual_trace"
}
```

## Required behavior

```text
- position is sampled along a curve
- At follows the curve tangent or declared tangent projection
- Up/Right are derived from the curve frame
- roll/bank is continuous unless a hard corner is intentional
- endpoints and gaps are intentional
```

## Failure conditions

```text
- curve pieces use inconsistent random rotations
- endpoint gaps are not declared
- curve samples are not tied to tangent/normal frames
- a curve-follow object is presented as validated part contact without step/contact proof
```


## Surface-mesh construction contract (absorbed from SINGLE_PART_SURFACE_MESH_CONSTRUCTION_PROTOCOL)
## Status

Mandatory when a build primarily uses one validated part family to create a complex surface, shell, silhouette, or sculpture.

## Principle

Using one validated part creatively is allowed and expected. The build must, however, generate the target graph/surface first and derive every part transform from that graph.

## Required construction representation

Scripts must define a graph, mesh, or curve representation before placement:

```python
SURFACE_MESH_CONTRACT = {
    "primary_part": "C_TRIFLOOR",
    "surface_type": "flat_panel | prism | closed_shell | curve_sweep | hybrid",
    "nodes_or_faces": "...",
    "adjacency_rule": "shared_edge | curve_step | surface_patch",
    "boundary_policy": "declared_openings_only",
    "forbidden": ["independent_centroid_scatter"]
}
```

## Placement rules

```text
- Interior placements must be adjacency-derived.
- Boundary edges must be declared.
- Openings must be intentional and named.
- Scaling is not a substitute for density or edge-contact unless the scale mode is validated.
- A single part can form complex objects only when its transform propagation is coherent.
```

## Failure conditions

```text
- random gaps in a surface
- orphaned parts
- unsupported floating panels
- inconsistent normals
- part scale/Up magnitude used without declared scale validation
- a visual shape made by approximate density without edge/curve/surface provenance
```


## Hybrid scene placement-aid contract (absorbed from HYBRID_SCENE_PLACEMENT_AID_PROTOCOL)
## Purpose

This rule hardens lessons from the bat-signal hybrid build sequence.

A build may use validated focal-geometry logic and still fail if review-required parts are treated as decorative exceptions rather than placement objects with normals, tangents, depth offsets, and support relationships.

## Mandatory methodology

For hybrid focal builds:

1. **Focal face authority**
   - Define the front/readable face first.
   - Preserve recognizable silhouette and emblem logic before adding depth.
   - Do not allow side-shell or decorative overlays to obscure the focal silhouette.

2. **Role-based part selection**
   - Use high-resolution parts only where shape fidelity is needed.
   - Use larger panels/walls/floors for long spans, back closure, side shell, ceiling, and interior fill.
   - Keep decorative overlays separate from structural shell logic.

3. **Review-required does not mean validation-exempt**
   - Review-required parts must still be included in float/objective review.
   - If a panel, strip, or light is offset from the host surface, it must declare:
     - host surface
     - mount normal
     - tangent/orientation axis
     - stand-off depth
     - collection role
     - whether it is structural, decorative, or experimental.

4. **Interior completion requirement**
   - If the user requests a building/room, the output must include an interior plan:
     - floor deck
     - ceiling/roof interior
     - side wall liners
     - rear wall or back closure
     - entrance threshold
     - at least minimal lighting/detail pass when appropriate.
   - A solid exterior shell with an empty interior is not a full building.

5. **Scene expansion discipline**
   - Surrounding-scene elements must be in separate collections.
   - Experimental skyline/decor should not contaminate the core build acceptance.
   - The focal building remains the acceptance target unless user says otherwise.

## Placement aid fields to add to partmaps when discovered

For `BUILDFLATPANEL`, `S_LIGHTSTRIP0`, `BUILDLIGHT`, and similar review-required parts, capture:

```yaml
placement_aid:
  part_role_candidates:
    - panel_span
    - rim_segment
    - side_shell
    - interior_liner
    - light_overlay
  mount_frame:
    normal_axis: TBD_BY_STUDY
    tangent_axis: TBD_BY_STUDY
    roll_axis: TBD_BY_STUDY
  mount_behavior:
    requires_standoff: true
    standoff_distance: TBD_BY_STUDY
    can_curve_follow: needs_validation
    can_surface_mount: needs_validation
  validation_requirements:
    - no_float_even_if_review_required
    - host_surface_declared
    - tangent_continuity_checked
    - collection_role_declared
```

## Failure examples this rule prevents

- Front face looks acceptable but side panels float or rib instead of closing the shell.
- A building exterior exists but the interior is empty or visually unfinished.
- Decorative light strips are allowed to drift because they are review-required.
- Panels are used for large areas but no mount/normal/tangent logic is captured.
- Focal build expands into a scene without preserving collection separation.

## Build gate implication

A hybrid build may not claim full PASS unless:
- core structural shell passes visual/objective review,
- review-required components are either validated or explicitly scoped,
- interior completion is present for building/room requests,
- source-doc `Docs Avail for Update?` reflects any confirmed placement-aid findings.


### CURVE_FOLLOW_TRANSFORM_PROPAGATION_PROTOCOL structured sidecar (absorbed; preserved)
```json
{
  "schema": "FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL",
  "status": "mandatory",
  "source_rule": "rules/FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL.md",
  "purpose": "Skilled manual builders often create strong shapes by repeating a single part along a curve with controlled tangent, spacing, roll, and offset. Generated builds must treat this as transform propagation, not as independent stamping.",
  "required_for": [
    "curve/path/ring/outline transforms"
  ]
}
```


### SINGLE_PART_SURFACE_MESH_CONSTRUCTION_PROTOCOL structured sidecar (absorbed; preserved)
```json
{
  "schema": "FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL",
  "status": "mandatory",
  "source_rule": "rules/FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL.md",
  "purpose": "Using one validated part creatively is allowed and expected. The build must, however, generate the target graph/surface first and derive every part transform from that graph.",
  "required_for": [
    "single validated part family surface/shell/sculpture builds"
  ]
}
```
