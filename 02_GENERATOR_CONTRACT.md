# NMS Generator Contract — Non-Negotiable Rules

This file exists because other AI chats may read the master docs but still generate generic Blender meshes. It defines what a valid NMS generator must do.

## Definition of a valid NMS generator

A valid NMS generator is a Python script that creates objects through the No Man's Sky Base Builder plugin and preserves NMS custom properties. It must use real NMS ObjectIDs such as `S_WALLM`, `S_FLOOR`, `S_ROOF5`, `CYLINDERSHAPE`, `SPHERESHAPE`, `S_ARCHB`, `S_ARCHM`, `S_ARCHT`, `S_WALL_Q`, `S_WALL_Q_H1`, `S_WALL_SUPPORTS`, `PIPESHAPE`, `S_RSJSTACK`.

A valid script does **not** create raw `Cube`, `Plane`, or `Cylinder` mesh objects as build parts. These calls are allowed only for debug markers when explicitly requested, never for final build parts:

```python
bpy.ops.mesh.primitive_cube_add
bpy.ops.mesh.primitive_plane_add
bpy.ops.mesh.primitive_cylinder_add
bpy.ops.mesh.primitive_uv_sphere_add
bpy.data.meshes.new
bpy.data.objects.new
```

Generic Blender mesh objects do not carry the required NMS properties (`ObjectID`, `SnapID`, `Timestamp`, `UserData`, `order`, `belongs_to_preset`, `snapped_to`). The NMS exporter serializes NMS parts; a pile of mesh cubes is not an NMS base.

## Performance: template + duplicate

Do not call `BUILDER.add_part()` for every placement — it can freeze Blender when repeated hundreds or thousands of times. Call it once per ObjectID to create a template, then duplicate the template.

**Delete templates before export (mandatory).** The templates created by `add_part()` carry live NMS part data, so the add-on exports them too. If they are not removed they survive the tag-scoped cleanup (they are prefixed `TPL_`, not the build TAG) and pile up at the origin `(0,0,0)` — the cluttered stack seen in failed builds. After all copies are placed, delete every template and add the `TPL_` prefix to the cleanup so stale templates also purge on re-run:

```python
for t in TEMPLATES.values():
    bpy.data.objects.remove(t, do_unlink=True)
```

`run_gate.py` enforces this mechanically: a build where stray `TPL_` parts survive to export, or where 2+ distinct ObjectIDs sit at exactly the origin, FAILS the gate (template-leak check).

## Before-run checklist

The script is not ready unless all answers are YES:

- Does it import/resolve `bl_ext.user_default.no_mans_sky_base_builder`?
- Does it create templates using `BUILDER.add_part(oid)`?
- Does it copy templates for repeated placements?
- Does every placed object inherit NMS custom properties?
- Does every part use working JSON orientation, a documented recipe, or a part-specific override when available, with generic `rx=90` only as the fallback?
  - *Authoring caution:* the orientation gate enforces each part's default rotation on RX/RY (≈90° for most parts). Flat-stacking at `rx=0` fails the gate; intentional deviations must be declared via `ORIENTATION_OVERRIDE_IDS` or a `PART_ORIENTATION_OVERRIDES.md` entry. RZ/facing is always free and never flagged.
- Does it avoid all raw mesh primitive calls?
- Does it delete only objects matching the script tag, not the entire scene?
- Does it estimate part count before heavy generation?

## Validation loop, scope, and scale

A script is not deliverable until the validation loop in `rules/SCRIPT_VALIDATION_LOOP.md` passes. If it fails, rewrite before delivery; if deviation is needed, request approval before delivery. Part-specific placement validation is scoped to ObjectIDs present in the current script — full-library inspection is for part selection and design potential, not for enforcing rules on unused parts.

Non-uniform scale restriction: final generated NMS parts use uniform scale; long members use repeated uniformly-scaled segments; non-uniform scale requires explicit approval or a documented validated exception. This is enforced by `validation/run_gate.py` (non-uniform final-scale check) and `rules/PROHIBITED_AND_PLACEHOLDER_OBJECTS.md`.

## Build object-use manifest

Every substantial generator documents how each ObjectID is used. Include a `BUILD OBJECT USE MANIFEST` comment block or printed section mapping ObjectID to role, use type, scale range, orientation notes, rules checked, and creative catalog references.

## Routing, traceability, and pre-generation gates

A valid generated script is traceable to the request type and rule bundle used to create it. For major scripts, include `REQUEST_CLASSIFICATION` with request type, user inputs, checked rule bundles, ambiguity handling, and JSON evidence status. Before generating any NMS script, classify the request and list applicable rule files via `rules/REQUEST_ROUTER_CHECKLIST.md`; outputs must not proceed if a relevant rule bundle has not been checked.

Before generating after a new master/source package is supplied: identify the chat's last version and the current version, review all intervening changelog/manifest/rule changes, verify the active rules relevant to the requested build, and state whether the review is a patch sanity check or a full continuity audit. Do not generate based only on the latest patch note.

## Design-intent contract (declare BEFORE placement)

A generated build must commit to a design *before* it places parts, so the result is intentional rather than a mechanically-valid pile. Mechanical validity (parts exist, connect, sit at default orientation) is necessary but not sufficient — a part that touches its neighbor but means nothing is still a defect.

Generated build scripts (`build_generation` and other build-type requests) must declare a `DESIGN_INTENT` block:

```python
DESIGN_INTENT = {
    "build": "<name>",
    "assemblies": [
        {
            "name": "<assembly>",
            "is_a": "<what it is, e.g. 'pitched roof'>",
            "target_read": "<what it must READ as, e.g. 'continuous gothic roof, no gaps'>",
            "style_source": "CREATIVE_USE_CASE_AND_STYLE_INDEX: <entry>",   # evidence, not invention
            "parts": [{"ObjectID": "<ID>", "purpose": "<why this part is here>"}, ...],
        },
        ...
    ],
}
```

Rules: every assembly must declare `is_a`, `target_read`, and a `style_source` drawn from the uploaded creative/style evidence (`data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json`) — not improvised. **Every used ObjectID must appear with a non-empty `purpose`**; a part placed with no declared purpose is a validation issue. `run_gate.py`'s design-intent gate enforces this (auto-required for build-type requests). The plan states intent; the AI visual review (AI_CAPTURE) then confirms the assembly actually reads as its declared `target_read` before delivery. Creative freedom selects *what* to build and *style* — it never licenses skipping the plan.


**Canonical build invocation (all build tiers) — run both gates together:**

```text
python3 validation/run_gate.py <script.py> library/nms_part_dimensions_and_rules_updated.json <TAG_PREFIX> --require-json-evidence --require-router
```

## JSON evidence contract

Relevant working exported JSON is mandatory first-tier evidence. Before writing or correcting placement-sensitive Python, check current uploads, the source package, reports, and recipe docs for working JSON; if found, extract and use it before generic orientation tables or FBX-only reasoning. Required actions when relevant JSON exists:

1. identify the JSON evidence source;
2. extract ObjectID clusters, Position deltas, Up/At basis vectors, vector-length scale evidence, UserData, local module envelopes, and physical anchors;
3. cross-check the extracted recipe with FBX bounds for geometry, clearance, and scale;
4. include `JSON_EVIDENCE_PROVENANCE` in the generated script;
5. if JSON is provided for the current build/subsystem, calculate orientation from JSON mapping (`Position`, `Up`, `At`, vector lengths, source local frame) before any generic orientation assumption;
6. use the JSON->Python transform stack only for JSON recreation, not for direct Blender-space procedural placement;
7. for generated builds, export JSON and compare serialized `Position`, `Up`, and `At` back to Python intent.

When a user provides exported/pasted JSON, JSON-derived studies, or failure evidence tied to JSON placement, the script must declare and use the validated mapping stack:

```python
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
```

For JSON->Python recreation scripts: use real builder-created NMS parts only; run builder preflight before cleanup/generation; strip `^` from exported `ObjectID` for builder calls while preserving the source ID in metadata; use the validated transform stack from `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`; preserve `UserData`, `Timestamp`, and extra fields such as `Message` where practical; skip only known non-build placeholders by default (`BASE_FLAG`, `U_PARAGON`); print a full ObjectID and transform audit; flag new ObjectIDs not previously validated.

`BUILDER.add_part(ObjectID)` may return a wrapper. Resolve it before object operations:

```python
part = BUILDER.add_part(oid)
obj = getattr(part, "object", part)
```

A script cannot be called validated unless `validation/run_gate.py` passes with nonzero placed objects and no wrapper-misuse issues. If known source-kit data (JSON/control) was bypassed and the output fails, stop and run `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md` before producing another geometry artifact; the next script must include evidence of the governing JSON/control recipe, expected ObjectID counts, and the NMS Builder object-resolution method.

## Recipe and spacing discipline

Before generating a fresh build or editing an existing one: check `toolkit/PLACEMENT_RECIPE_LIBRARY.md` for applicable feature recipes and `rules/SPACING_CONNECTION_SCALE_RULES.md` for repeated-part spacing; state the ObjectID, role, spacing source, scale, and connection logic for repeated systems; use JSON/FBX precedent for spacing when available; generate assemblies from local coordinate frames; reject floating stairs, unsupported platforms, random trim, and independent prop scatter. Stairs, ramps, vehicles, tabletop games, display walls, powerline hubs, rings, and airlocks all require explicit module logic.

Do not isolate lessons by project label — reuse a lesson whenever the same ObjectID, assembly pattern, terrain condition, or design problem appears. Before applying generic orientation, check `rules/PART_ORIENTATION_OVERRIDES.md`. Any bridge/tube/pipe/rail/conveyor/connector span follows `rules/CONTINUOUS_PATH_ASSEMBLY_RULE.md`. Large builds on unknown/uneven/floating terrain consider `rules/GROUND_ZERO_FOUNDATION_RULE.md`. Dense detail passes follow `rules/CURATED_DETAIL_HIERARCHY_RULE.md`. For placement-sensitive builds, run the exported JSON geometry loop in `rules/JSON_GEOMETRY_VALIDATION_LOOP.md` after Blender generation: the script gate proves hygiene, exported JSON proves serialized transforms, screenshots prove visual outcome.

## Connected-piece curvature contract

When generating any curved, rounded, tapered, shell-like, or hull-like feature, route through `rules/CONNECTED_PIECE_CURVATURE_GRAMMAR.md`. Identify the underlying geometry primitive, not only the named feature — dome, spire, cylindrical habitat, rounded object, insect body, vehicle hull, pod, and arch/rib/collar requests may all use the same connected-piece method with different paths/profiles/envelopes. Required fields:

```text
feature_type
local frame
curve/profile/control points
part layers
segment/chord/overlap policy
scale profile
contact/convergence validation
envelope limits
material/effect profile
```

For a spire requested before exported JSON exists, classify it as a provisional visual-recipe build (use `rules/CONNECTED_PIECE_CURVATURE_GRAMMAR.md` plus the consolidated spire study notes in `MASTER_LESSONS_LEARNED.md`); do not claim exact part spacing/orientation. Final recipe generation requires JSON extraction of centerline, base radius, convergence point, ribs, infill, collar bands, cap, and UserData.

## Power / utility default

Generated scripts default to:

```python
INCLUDE_POWER_UTILITY = False
```

Do not place powerlines, switches, batteries, solar panels, biofuel generators, or related utility devices unless the user explicitly requests them; the user places these manually in game.

## Disconnected assembly hard-stop

Generated builds and study boards may not deliver disconnected assemblies when the intended read is connected architecture or usable circulation. Before delivery, any repeated/adjacent subsystem (stairs, ramps, catwalks, spires, roof crowns, wall bays, vehicles, cave interiors, hatches, airlocks) must include connection proof:

```text
Subsystem name; ObjectIDs; source of placement; anchors or ring/center/radius; path/ring/local-frame basis; step/chord; overlap/contact tolerance; origin mode; expected continuity; failure action.
```

Acceptable origin modes for assembled subsystems are `place_bottom`, `place_top`, `place_center`, and `place_exact_json`. Direct origin placement must include explicit origin proof. If screenshots show disconnected pieces, stop broad generation and revert to a small control/proof module. Read `rules/DISCONNECTED_ASSEMBLY_HARDSTOP_RULE.md`.

## Placement-intelligence evidence artifacts

Generated builds must emit or be able to package placement session receipts, build placement snapshots, method summaries, assembly conformance plans, and part usage manifests. Dry-run placement is not a complete gate, and component part-map validation cannot substitute for assembly conformance. See `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md`.

## Experimental generator addendum

An experimental/creative generator additionally requires a concept-diversity plan before code, a `BUILD OBJECT USE MANIFEST`, an explicit role for every ObjectID, comfort-motif suppression unless justified, no filler rings/pads/floating antennas, and study variants separated from locked/core variants. Experimental scripts may take creative risks but must still use real NMS parts with valid ObjectIDs and safe builder preflight.

## Corvette generator addendum (Corvette-only)

When generating a Corvette script, the generator must additionally read `/corvette` and pass the Corvette validation checklist. Corvette scripts must cover the seven required categories when claiming a valid Corvette, probe whether the active plugin context can instantiate the required Corvette ObjectIDs, fail cleanly if Corvette Workshop modules are not exposed, never replace missing modules with proxy meshes, and include the ObjectID in Blender object names/descriptions for searchability.

When `BUILD_MODE == Corvette` or the user requests an in-game Corvette/blueprint: load `corvette/CORVETTE_BOUNDARY_LIMITS.md` / `.json`; compute final occupied rotated bounds from FBX extents and uniform scale across the **entire** final ship assembly (do not filter to `Category == Corvette` — non-Corvette exterior/interior decoration counts toward the footprint); enforce `CORVETTE_SAFE_BOUNDARY_SIDE_M = 95.0`; treat `100.0m` as an absolute redline; print the final X/Y/Z span; and fail/redesign before delivery if any axis exceeds 95m, identifying the violating ObjectIDs. This addendum is Corvette-only and must not be applied to ordinary planetary/freighter/base architecture.

## Plugin and environment

The active documented plugin version is No Man's Sky Base Builder 6.4.1. Blender 5.0.1 is the user-confirmed working environment; Blender 5.1.1 may work only after confirming the FBX import/export add-on is enabled for the plugin's internal part retrieval. Generated scripts must still use `BUILDER.add_part()` template-copy generation and must not import FBX directly. Before scripting with newly added 6.4.1 parts, confirm the ObjectID exists in the runtime builder and validate orientation/material behavior in Blender/in-game; treat newly exposed `SET_*` settlement/setpiece objects as validation-required before broad use; do not generate `HOLO_DISCO_0`.

## Plugin environment provenance
The canonical record of the plugin/Blender environment and library counts (2,097 part definitions, new-vs-v49 ObjectIDs, prohibited generated objects, source zip) is `library/NMS_PLUGIN_ENVIRONMENT_v50.json`. Consult it when confirming part counts or newly added 6.4.1 ObjectIDs.
