# Prompt-to-Feature Router

Status: mandatory feature-intent routing aid for build_generation and build refinement.

## Purpose

The request router decides the broad task type. This file maps user language to likely feature recipes and geometry bases so a future chat does not forget which recipe/control family applies.

## Use

After request classification, scan the user prompt for feature intent. Load matching recipes/signatures before generating a placement plan or using the part map for component dimensions.

A known feature must produce a `FEATURE_RECIPE_LOOKUP` receipt. The receipt can say `none_found`, but it cannot be omitted.

## Routing examples

| Prompt intent | Likely recipe/signature | Geometry basis |
|---|---|---|
| airlock, iris, vault door, aperture, portal | radial_airlock_iris_door | ring + depth layers |
| stairs, stairway, ramp, bridge access | endpoint_stair_ramp_connection | endpoint_path |
| dome, cupola, rounded roof, oculus | dome_latitude_shell | latitude_shell |
| curved wall, shell, arch, hull, pod, canopy | connected_piece_curvature_grammar | ring/arc/shell/profile |
| spire, tower crown, taper, apex | tapered_spire_shell | tapered_shell |
| vehicle, cart, rover, chassis | jurassic_vehicle_chassis | local_frame |
| platform, deck, landing | facility_deck_platform | grid + support/load path |
| screen wall, control room, lab display | lab_display_wall_grid | wall-plane grid |
| powerlines, logic, circuits | powerline_hub_logic_cluster | preserved vectors |


## Build-vs-image routing guard

NMS-context build language such as "create a gothic castle" routes to `build_generation`, not image generation, unless the user explicitly asks for an image, render, mockup, concept art, or visual-only output.

The gothic/castle/fortress route should pair the facade/style route with applicable feature recipes. Example:

```text
Prompt: create a gothic castle with metal parts and a 12-sided flush airlock entrance
Request type: build_generation
Feature routes: gothic_metal_castle_facade + radial_airlock_iris_door
Required controls: execution kernel + control-to-variant + airlock/iris recipe + disconnected assembly hard-stop
```


## Priority rule

Recipe/signature/toolkit lookup outranks part-map component lookup for known features. The part map validates and supports the selected recipe; it is not a replacement for assembly logic.

## Required lookup receipt

For build scripts, record:

```text
FEATURE_RECIPE_LOOKUP.feature_intent
FEATURE_RECIPE_LOOKUP.matched_recipe_or_signature
FEATURE_RECIPE_LOOKUP.recipe_files_checked
FEATURE_RECIPE_LOOKUP.recipe_status
FEATURE_RECIPE_LOOKUP.part_map_role
```

If no recipe is found, set `recipe_status=none_found`, explain `reason_if_none`, and mark the placement plan as provisional.

## recipe-first additions

The following routes are explicit because they previously failed when the model started from part-map dimensions rather than assembly recipes.

| Prompt intent | Required recipe/signature | Geometry basis |
|---|---|---|
| building, room, enclosed walls, wall shell, city block, skyscraper, tower | `wall_shell_enclosure_recipe_v2_19_00` | closed grid shell + local frame |
| Gotham, Batman city, dark city, crime alley, dense city | `gotham_dark_city_recipe_v2_19_00` + wall shell + path recipes | district grid + enclosed tower shells + connected alleys |
| AI Review bundle / `NMS_AI_REVIEW_Scene_*.zip` | no build recipe; use `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md` | design-loop review bundle |

For a known feature, the part map is **not** the first creative source. The feature route selects the recipe/control logic. The part map then validates ObjectIDs, extents, centers, spacing, and scale behavior.

## Executable receipt enforcement

As of 2.19.00, `validation/feature_recipe_lookup_check.py` detects known feature terms and fails a generated script that omits or malforms `FEATURE_RECIPE_LOOKUP`. The run gate also surfaces the feature-recipe lookup gate during build validation.


## AI visual feedback additions

| Prompt intent | Required protocol/check | Geometry basis |
|---|---|---|
| AI visual review, review ZIP, screenshots from Blender add-on | `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md` + `validation/ai_review_bundle_check.py` | visual-review bundle |
| generated build script that will be reviewed by AI | `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md` + `validation/ai_capture_compliance_check.py` | semantic collections + capture metadata |
| hidden interiors, cutaways, collection images identical | `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md` | collection/name/spatial/geometric fallback |
