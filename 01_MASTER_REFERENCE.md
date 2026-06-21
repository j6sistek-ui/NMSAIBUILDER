# NMS Master Reference — Universal Source of Truth

This document is the canonical universal rule reference for AI-generated No Man's Sky Base Builder Python scripts.

## 1. Mission

Produce real NMS Base Builder plugin parts with reliable placement, documented part behavior, and repeatable validation. The package is designed to support:

- creative part selection from the full ObjectID library
- precise placement using FBX-derived dimensions
- safe script execution in Blender
- validation before scripts are delivered
- memory recall across AI chats
- immediate promotion of understood fixes into master documentation

## 2. What is universal vs project-specific

Universal knowledge belongs in this package:

- plugin contract
- object-library rules
- placement/origin/spacing formulas
- part-family behavior
- known failure modes and fixes
- prohibited/placeholder objects
- validation loops
- reusable creative part-use patterns

Project-specific information belongs outside the master package:

- project scripts
- one-off build handoff notes
- style targets for a named build
- temporary study files
- locked baselines for an individual project

If a project discovers a rule that applies beyond that project, promote it into `/rules` immediately.

## 3. Valid NMS generator definition

A valid script must:

1. resolve the No Man's Sky Base Builder plugin runtime
2. call `BUILDER.add_part(ObjectID)` once per selected ObjectID to create templates
3. duplicate template objects for repeated placements
4. preserve NMS custom properties: `ObjectID`, `SnapID`, `Timestamp`, `UserData`, `order`, `belongs_to_preset`, and `snapped_to`
5. avoid raw Blender primitive mesh creation
6. delete only objects matching the script's own tag
7. include runtime object audit

See `02_GENERATOR_CONTRACT.md` and `validation/NMS_SAFE_STARTER_TEMPLATE.py`.

## 4. Full library rule

The complete part library is `library/nms_part_dimensions_and_rules_updated.json/csv`, currently containing `2097` ObjectID rows. Any short ObjectID list is examples only, never a whitelist.

When selecting parts, inspect the broader library for design potential. When validating placement rules, inspect only the ObjectIDs and part families actually present in the current script.

## 5. Origin-vs-bounds placement rule

The script sets the object's Blender origin, not necessarily the visible center of the mesh. Do not assume `z` is the visible center.

Use FBX bounds:

```python
bottom_rel = (center_y - extent_y / 2) * scale
top_rel    = (center_y + extent_y / 2) * scale
origin_for_bottom = visible_bottom_z - bottom_rel
origin_for_top    = visible_top_z - top_rel
```

Use semantic wrappers such as `place_bottom()`, `place_top()`, and `place_center()` rather than hand-placing origins.

## 6. Scale, spacing, and continuity

Spacing must be derived from the part's FBX dimensions or confirmed calibration:

```python
placement_step = visible_native_dimension * scale
```

Continuous rows/rings must actually touch or overlap. Do not label trim as continuous unless centers are calculated from visible scaled length with deliberate overlap.

## 7. Script-generation validation loop

Before delivering any script, run `rules/SCRIPT_VALIDATION_LOOP.md`.

If validation fails, rewrite. If a rule should be suspended or violated, request approval before presenting code.

## 8. Immediate documentation update rule

When a design rule, offset correction, orientation fix, scale/spacing formula, or part-specific behavior is finally understood and correctly applied, update the master documentation immediately. Do not leave durable lessons only in chat memory or a one-off script.

## 9. Prohibited and placeholder object behavior

- `HOLO_DISCO` is the Wonder Projector. Do not generate it unless explicitly preserving a user-provided configured object.
- `U_PARAGON` is a plugin/default placeholder or non-visible artifact, not Wonder Projector. Do not design around it as a visible part.

See `rules/PROHIBITED_AND_PLACEHOLDER_OBJECTS.md`.

## 10. Part-family rules

Use `rules/PART_FAMILY_RULES.md/json` for part-specific placement. Do not review every part-family rule for every script; first extract the script's ObjectID set, then validate only those families.

## 11. Creative part-use rule

Creative part use is encouraged. A wall may become a book, backboard, screen, trim, rib, or scaled architectural mass depending on orientation and scale. Use `rules/PART_USE_CASE_CATALOG.md/json` for design potential. Creative selection is broad; placement validation is scoped to used ObjectIDs.

## 12. Memory recall

Use `00_MEMORY_RECALL_INDEX.md/json` to find the right source file quickly. The goal is not to reread every file every time; the goal is to recall and apply the correct rule at the correct step.


## v39 creative memory and object-use logging

The package now treats screenshots, JSON exports, manual examples, and study results as durable memory inputs. New creative uses must be logged, and every substantial script/build should include a `BUILD OBJECT USE MANIFEST` describing how each ObjectID is used. This improves recall, supports broader design exploration, and reduces repetitive comfort-zone features.

## v42 experimental exploration discipline
Broad creative prompts are not consolidation prompts. If the user asks for experimental, creative, unique, futuristic, exploratory, or vague design work, activate `rules/EXPERIMENTAL_REQUEST_PROTOCOL.md`.

Key rule:

```text
Vague experimental prompt = exploration mode, not consolidation mode.
```

Past successful motifs are guardrails, not templates. The generator should deliberately explore:

- different macro silhouettes;
- underused part families;
- divergent structural logic;
- distinct effect strategies;
- different view/use contexts.

Comfort motifs such as short-wall rings, red-lens bands, antenna crowns, light-fissure beacons, Aeron blade cones, and simple stacked-room crowns must be suppressed unless they are specifically justified by the design.

Experimental outputs must include an object-use manifest and should not retain weak variants simply to fill a count. Screenshots and user in-game review override script intent.

## v42 deep sea room skyscraper topper lesson
Circular and square deep sea rooms (`MAINROOM_WATER`, `MAINROOMCUBE_W`) are validated macro fabric for skyscraper bodies and rooftop modules. They work well for colored modular towers and roof adapters, but a topper study must not reduce to repetitive room stacks.

For skyscraper toppers:

- use deep sea rooms as structural volume, roof sockets, pods, adapters, or crown masses;
- create distinct skyline silhouettes;
- attach antennas, cranes, dishes, gantries, and effect parts to visible room geometry;
- use color to identify districts, functions, and AI-control zones;
- avoid repeating the same red-lens/antenna/stack motif across all variants.

## v43 Corvette repository discipline

Corvette construction has its own repository at `/corvette`.

Corvette projects still use the universal NMS Builder contract, but their required categories, Workshop/module assumptions, role optimization, and plugin-exposure diagnostics are Corvette-only. Do not apply Corvette minimum categories or ship-role logic to ordinary base architecture.

For Corvette work, read `corvette/CORVETTE_KNOWLEDGE_REPOSITORY.md` before selecting parts or scripting.

## v44 Corvette parts used outside Corvette builds

Corvette ObjectIDs belong to the full ObjectID library. They can be used decoratively or architecturally outside a Corvette project.

Do not activate Corvette required-category validation solely because a script uses a Corvette ObjectID. Activate Corvette validation only when the build intent is Corvette/ship-specific or the Object Use Manifest assigns Corvette functional roles.

For decorative/non-Corvette use:
- apply universal generator validation;
- validate FBX dimensions/origin/orientation for the used Corvette ObjectIDs;
- record the role in the Object Use Manifest;
- skip Corvette completeness/loadout failure checks.

## Taj Mahal under-3k case study

The final Taj Mahal project is now documented as a completed landmark-build case study.

Use it as guidance for large cultural/nostalgic builds:
- macro silhouette first,
- subsystem studies,
- screenshot validation,
- protected baselines,
- late-stage part optimization.

Primary file:
`MASTER_LESSONS_LEARNED.md` (removed historical reference: case_studies/TAJ_MAHAL_UNDER_3000_CASE_STUDY_v49.md)

## v50 plugin 6.4.1 reference

The library has been updated against No Man's Sky Base Builder 6.4.1.

Current documented environment:
- Base Builder add-on: 6.4.1
- Blender: 5.0.1 confirmed working; 5.1.1 requires FBX importer/add-on checks

New parts are documented in `MASTER_LESSONS_LEARNED.md` (removed historical reference: reports/NMS_PLUGIN_641_UPDATE_REPORT_v50.md).

## v51 visual toolkit expansion

The master docs now include a general visual-reference intake protocol and an Alien City-Canyon / Megatemple toolkit entry.

Use these files when the user sends screenshots or architectural references as general building knowledge:

- `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md`
- `toolkit/VISUAL_BUILD_TOOLKIT_ALIEN_CITY_CANYON_v51.md`
- `MASTER_LESSONS_LEARNED.md` (removed historical reference: reports/REFERENCE_INTAKE_AUDIT_CORRECTION_v51.md)

## v52 screenshot taxonomy

The documentation now distinguishes:

```text
external/non-current-project in-game photos = general reference/toolkit intake
current generated build photos = validation evidence
```

Primary file:
`rules/SELECTIVE_VISUAL_MEMORY_POLICY.md`

## v53 JSON → Python recreation protocol
The JSON→Python recreation path is now validated for the current exported base JSON schema.

Use this transform stack by default:

```python
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
```

The decisive finding is that the final `LOCAL_Y_180` post-correction appears broadly required, not merely family-specific. It fixed subtle local orientation errors hidden by square wall/floor geometry and handled furniture, decals, billboards, shelves/wall-mounted props, counter props, curtains, and table props in the tested sample.

Validation basis:

- 249-object original-location overlay: visually perfect by user review.
- 1,237-object multi-location/multi-axis replicated sample: all locations and axes handled correctly by user review.

Caveat: this is validated for the tested JSON intake path and ObjectID set, not all possible future families. Future bases must print an ObjectID audit and flag new/unvalidated families.

## v54 JSON Study and Recipe Extraction
v54 adds a JSON Study / Placement Recipe Library process.

The v53 transform lets us accurately recreate base JSON. v54 uses that capability to learn from finished bases:

- part-family behavior;
- spacing;
- scale;
- connection logic;
- repeated systems;
- feature recipes;
- negative lessons.

Study outputs are now classified as:

```text
universal rule
part-family rule
toolkit technique
project observation
negative lesson
```

Major staged recipes include archive/book-spine walls, Jurassic vehicle chassis, facility decks, lab display walls, containment cylinders, promenade rows, compact 3x3x3 modular shells, radial airlock/iris doors, foosball/tabletop game assemblies, fossil/skull façade markers, observation-window lab facades, powerline hubs, and organic scatter zoning.

Negative lesson: the `C_GDOOR` / `S_GDOOR` dinosaur-mouth placements from Jurassic Beach are **not** a reusable mastery recipe. They were free-placed with bad mechanics and only worked contextually in an organic dinosaur mouth.

## v55 merged JSON recipe + connected surface reference

v55 merges the uploaded JSON-study recipe library with the connected-surface universal rule package.

Important active concepts:
- JSON = geometry truth for placement recipe extraction.
- In-game screenshots = visual truth.
- Production shells should be connected angled surfaces, not stepped-offset lookalikes.
- Airlock/iris doors now have an extracted JSON baseline using `S_GDOOR`, `B_FLOOR_Q`, `B_WALL_Q_H1`, and `F_WALLB_H`.

## v56 recipe parameterization reference

JSON = geometry truth for the source module, but not the only valid future implementation.

Recipes must identify:
- baseline/control;
- variable parameters;
- candidate ObjectID families;
- validation requirements.

Primary file:
`rules/RECIPE_PARAMETERIZATION_PROTOCOL.md`

## master versioning reference

The master documents now use `X.YY.ZZ` versioning.

Primary file:
`rules/MASTER_DOC_VERSIONING_POLICY.md`

Legacy `vNN` package numbering is deprecated for master releases.

## Source-package continuity requirement
Future chats must treat newly uploaded master/source packages as cumulative deltas from the version the chat last used. A quick patch sanity review is allowed only if labeled as such. A claim that no critical knowledge was lost requires a full continuity audit.

Rule file: `rules/FULL_VERSION_CONTINUITY_REVIEW_RULE.md`.


## release metadata fix

1.02.01 is a patch over 1.02.00 that fixes version metadata/release-gate consistency only. The 1.02.00 full continuity review rule remains active.



## JSON evidence and systematic-failure prevention

If the user provides JSON, JSON snippets, JSON-derived studies, or asks to compare Python/Blender output against JSON, generic orientation assumptions are not allowed as the first placement model. Load `rules/JSON_EVIDENCE_MAPPING_GATE.md` and use the validated transform stack before generating code.

If a generated output fails because known source-kit information was not used, activate `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md` immediately. The next response must root-cause the failure, contain the bad output, state corrective/preventive action, and update durable source docs before creating another script.
