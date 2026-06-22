# NMS Builder Execution Kernel

Status: mandatory compact execution layer for build, JSON, recipe, and source-doc work.

## Purpose

This kernel turns the master docs from passive knowledge into an ordered procedure. It must be used after the request router and before any substantive NMS build generation, JSON study, recipe derivation, or source-doc update.

## Core algorithm

```text
1. Classify the request type with the request router.
2. Load the smallest sufficient bundle for that type.
3. Run feature-intent routing for build work: check whether the prompt asks for a known feature, recipe, signature, toolkit entry, or subsystem.
4. Detect whether relevant current-build JSON, control JSON, JSON-derived recipes, or validated recipe signatures already exist.
5. Select the matching recipe/signature/control or explicitly declare that no known recipe exists.
6. Split the subsystem into locked invariants and allowed variation parameters.
7. Resolve recipe-required ObjectIDs and part families, then use the part map to validate component dimensions, centers, spacing, scale behavior, and role.
8. Resolve geometry basis: exact_json, local_frame, endpoint_path, grid, ring, shell, surface_normal, curve_follow, edge_contact_graph, or hybrid.
9. Generate a placement plan before Python.
10. Emit Python through real NMS Builder parts only.
11. Emit object-use, evidence/provenance, BUILD_INTENT_GRAPH, USED_PART_LOGIC, and FEATURE_RECIPE_LOOKUP manifests.
12. Validate with the applicable gate.
13. Promote newly proven lessons into recipe/signature/rule files.
```

## Mandatory invariant/parameter split

Before adapting a known feature, identify:

```text
LOCKED INVARIANTS
- object/part roles that make the feature work
- local frame / origin / anchors
- endpoint/radius/chord/contact relationships
- orientation basis and transform stack
- connection/contact proof

ALLOWED PARAMETERS
- count / segments
- radius / run / height
- scale
- material/UserData
- density/detail level
- compatible ObjectID family substitutions
```

If the request says "same feature but different," do not regenerate from scratch. Load the control recipe, preserve invariants, and vary only approved parameters.

## Assembly intelligence priority

When relevant working JSON, a known feature recipe, or a JSON-derived control exists, the generator must use evidence in this order:

```text
request router / protocol classification
→ feature-intent recipe lookup
→ current-build exact JSON transforms
→ current-build local cluster recipe
→ validated recipe/signature/toolkit invariants
→ part-specific rules and orientation overrides
→ part map component validation and spacing support
→ FBX/manual inspection fallback only when unresolved
→ generic fallback only with uncertainty noted
```

Recipes control assemblies. The part map controls component geometry. A known recipe must not be bypassed merely because the part map contains the component ObjectIDs.


## FEATURE_RECIPE_LOOKUP receipt

Generated build scripts that create or modify a known feature must include a literal `FEATURE_RECIPE_LOOKUP` manifest. Minimum fields:

```python
FEATURE_RECIPE_LOOKUP = {
    "feature_intent": "airlock / stairs / bridge / dome / spire / vehicle / ...",
    "matched_recipe_or_signature": "recipe_id or NONE",
    "recipe_files_checked": ["rules/...", "toolkit/...", "data/..."],
    "recipe_status": "exact_json | validated_recipe | toolkit_recipe | provisional | none_found",
    "reason_if_none": "only required when no match is found",
    "part_map_role": "component_validation_only | component_geometry_support | fallback_geometry"
}
```

If `matched_recipe_or_signature` is `NONE` for a common feature term, the build must declare uncertainty and use provisional routing.

## Build-code preflight

A generated script must include or be accompanied by:

```text
REQUEST_CLASSIFICATION
object-use manifest
evidence/provenance manifest
selected recipe/signature IDs
FEATURE_RECIPE_LOOKUP receipt for known features
JSON evidence status
connection proof for assembled subsystems
validation command and tool output
```

## Failure trigger

If the AI cannot find the claimed recipe/signature/control data, it must not pretend the data was retained. It must request the source JSON again or mark the recipe as provisional and list exactly what is missing.


## visual-artifact misroute guard

Before generation, check whether the user explicitly requested an image/render/mockup/concept-art artifact. If not, an NMS-context request to create/make/build/design a base or feature is routed to build generation/refinement, not image generation.

## executable feature-recipe enforcement

`validation/feature_recipe_lookup_check.py` is the machine-checkable receipt layer for known-feature routing. If a generated script contains known feature terms from `rules/PROMPT_TO_FEATURE_ROUTER.json` or common assembly terms such as wall, tower, airlock, stair, ramp, bridge, or skybridge, it must include a valid `FEATURE_RECIPE_LOOKUP` manifest.

`validation/run_gate.py` surfaces this as the feature recipe lookup gate. A known feature without the receipt is a gate failure. This protects recipes such as airlock doors and wall-shell buildings from being rebuilt from component dimensions alone.

## wall-shell permanence

For building, tower, room, city-block, or Gotham prompts, apply `rules/WALL_SHELL_ENCLOSURE_RECIPE.md` before selecting wall parts. The recipe preserves closure and contact invariants that the part map cannot infer from component dimensions alone.

## AI Review design-loop support

If the user provides an `NMS_AI_REVIEW_Scene_*.zip`, apply `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md`. This bundle is useful design-loop evidence but is not exported NMS JSON. It should not trigger a code fix unless the user asks for one.
## build-scope constraint — structure only, no power/connectors in Blender

When building or scripting in Blender, place STRUCTURE only. Do not place power or connector parts (U_POWERLINE, U_SOLAR_S, U_BATTERY_S, U_BIOGENERATOR, U_SWITCHWALL, bytebeat cable, mineral pipes, electrical); Blender does not represent connectors reliably. Power and wiring are handled by the user in game.
