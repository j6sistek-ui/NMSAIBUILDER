# AI Capture Compliance Contract — 3.00.00

## Status

Active required contract for generated Blender/NMS build scripts.

## Purpose

Generated build scripts must be review-ready. The AI cannot evaluate a full build if all objects are dumped into one collection without role metadata, if interior objects are hidden behind the exterior shell, or if review-required parts are mixed into validated structural collections.

This contract defines the minimum script-side structure needed for the Blender visual feedback harness and for `validation/run_gate.py` to check AI-capture compliance.

## Required script receipt

Generated build scripts with request type `build_generation`, `new_geometry_synthesis`, `build_refinement`, or a similar build route must include an `AI_CAPTURE_COMPLIANCE` manifest.

Minimum shape:

```python
AI_CAPTURE_COMPLIANCE = {
    "schema": "NMS_AI_CAPTURE_COMPLIANCE_v1",
    "source_docs_rev": "3.00.00",
    "capture_strategy": "semantic_collections_plus_cutaways",
    "semantic_collections": [
        "ACCESS_AND_INTERIOR",
        "FRONT_FOCAL_FACE",
        "STRUCTURAL_SHELL",
        "INTERIOR_ARCHITECTURE",
        "INTERIOR_DETAIL",
        "DECOR_LIGHT_REVIEW",
        "SCENE_EXPERIMENTAL",
    ],
    "object_metadata_fields": [
        "role",
        "collection_role",
        "review_required",
        "placement_method",
        "source_docs_rev",
    ],
    "single_collection_fallback_declared": False,
    "review_bundle_addon_min_version": "v04",
}
```

The exact collection names may vary, but their roles must be semantically clear.

## Required semantic roles

For ordinary builds, at least two semantic roles are required. For buildings/rooms/cities, both exterior and interior roles are required.

Recommended roles:

| Role family | Examples |
|---|---|
| access | `ACCESS_AND_INTERIOR`, `WALKWAY`, `STAIR_ACCESS` |
| exterior/focal | `FRONT_FOCAL_FACE`, `EXTERIOR_SHELL`, `STRUCTURAL_SHELL` |
| interior | `INTERIOR_ARCHITECTURE`, `INTERIOR_DETAIL`, `CONTROL_ROOM` |
| decor/review | `DECOR_LIGHT_REVIEW`, `GOLD_ACCENTS_REVIEW`, `REVIEW_REQUIRED` |
| scene/context | `SCENE_EXPERIMENTAL`, `GOTHAM_SCENE`, `PLAZA`, `SKYLINE` |

## Review-required rule

`review_required` parts are not validation-exempt. They must be isolated by collection/role or explicitly declared in the manifest so the review tool can inspect them separately.

## One-collection exception

A script may intentionally use one collection only if it declares:

```python
AI_CAPTURE_COMPLIANCE["single_collection_fallback_declared"] = True
```

and explains how the review tool should fall back to object-name clustering, spatial slicing, or geometric interior/exterior candidates. This exception is for imported/third-party/legacy structures, not the default for generated builds.

## Gate implication

`validation/ai_capture_compliance_check.py` checks this contract statically. `validation/run_gate.py` runs that checker for build-generation scripts and reports the result in the machine-checkable gate.

A generated build that omits AI capture compliance is not review-ready.


## Blender visual feedback harness (absorbed from BLENDER_VISUAL_FEEDBACK_HARNESS_PROTOCOL)
## Status

Active required protocol for AI-assisted visual review of generated Blender/NMS builds.

## Purpose

A generated Blender build cannot be evaluated from exterior screenshots alone when it contains an interior, hidden details, cutaways, or scene-scale context. The visual review harness provides standardized, budgeted, repeatable image and metadata capture so the AI can review the build as a structure rather than as one attractive front-facing shot.

## Required review bundle concept

A compliant review bundle contains:

- NMS_AI_REVIEW_CHECKLIST.md
- OPEN_TOPICS_LOG.md
- nms_ai_review_objects.json
- one or more `screenshots/` subfolders
- capture-set metadata in nms_ai_review_objects.json

The review bundle is design-loop evidence. It does not replace authoritative NMS Builder exported JSON and it does not replace `validation/run_gate.py`.

## Capture set requirements

For full-building or room requests, the review bundle must capture more than all-object exterior views. At minimum, it should include:

| Capture set | Purpose |
|---|---|
| `ALL_VISIBLE` or equivalent | overall scene/form check |
| `CORE_NO_SCENE` or equivalent | focal build without city/context clutter |
| `INTERIOR` or equivalent | room/interior completion check |
| `EXTERIOR` or equivalent | shell/front/focal enclosure check |
| `CUTAWAY` or equivalent | interior visible after hiding shell/front/decor |
| semantic or fallback grouping | named collection, object-name cluster, or spatial section |

The exact names may vary, but the bundle JSON must make the intent of each capture set explicit.

## Budget rule

Review bundles must be upload-conscious. Prefer:

- JPEG over PNG for iterative chat review;
- 1280x800 or similar default resolution;
- a hard `max_images` cap;
- semantic capture sets before raw every-collection capture;
- collection/name/spatial fallback only when useful.

Large, unbounded screenshot bundles are a workflow failure unless explicitly requested.

## Semantic collection rule

Generated build scripts should make review easy by creating build-area collections and object metadata. Recommended collection roles:

- `ACCESS_AND_INTERIOR`
- `FRONT_FOCAL_FACE`
- `STRUCTURAL_SHELL`
- `INTERIOR_ARCHITECTURE`
- `INTERIOR_DETAIL`
- `DECOR_LIGHT_REVIEW`
- `SCENE_EXPERIMENTAL`

The build script should also stamp objects with role metadata such as `collection_role`, `role`, `review_required`, `placement_method`, and `source_docs_rev`.

## Single-collection fallback rule

Some imported or third-party builds place everything in one Blender collection. In that case, collection isolation is not enough and may produce no-op/identical screenshots.

The review harness must fall back to:

- object-name clustering;
- spatial third-slices or region slices;
- geometric interior/exterior candidate passes;
- no-op/redundant capture detection;
- explicit warnings in the checklist when only one collection is detected.

## Interior rule

If the user requests a building, city block, room, base interior, tower with floors, or any structure with implied internal content, the review bundle must include an interior/cutaway way to see it. Exterior-only review cannot prove interior completion.

## Gate implication

A build may not claim visual review PASS if:

- the review bundle only shows exterior views for a building/room;
- collection-isolated captures are identical/no-op without a fallback;
- hidden interior parts exist but no capture exposes them;
- review-required parts are present but not visually isolated or flagged.

The correct verdict is `BLOCKED`, `visual review incomplete`, or `capture bundle insufficient`, not PASS.
## exclude power/connectors; Blender is geometry-only

- Exclude all power/connector objects from Blender builds and scripts (powerlines, bytebeat cable, mineral pipes, electrical). Blender does not represent them reliably. Build structure in Blender; do power/wiring in game. See NEGATIVE_KNOWLEDGE_INDEX entries and the retraction of the powerline-At reading.
- Blender authority is geometry/placement only; color/material/emissive/lighting are judged in game.


## AI review bundle intake (absorbed from AI_REVIEW_BUNDLE_INTAKE_PROTOCOL)
Status: **active optional validation/design-loop protocol**.

## Purpose

The user may provide a standardized Blender review package named like `NMS_AI_REVIEW_Scene_*.zip`. Treat it as repeatable Blender-scene evidence for design review, not as an exported NMS save JSON.

## Required classification

If the user uploads an AI Review bundle:

```text
request_type: validation_iteration
secondary_mode: design_loop_review
```

Do not modify the build unless the user explicitly asks for code changes. First inspect the bundle and report findings.

## Expected bundle contents

```text
NMS_AI_REVIEW_CHECKLIST.md
OPEN_TOPICS_LOG.md
nms_ai_review_objects.json
screenshots/front_x_minus.png
screenshots/front_x_plus.png
screenshots/iso_front_left.png
screenshots/iso_front_right.png
screenshots/rear_iso.png
screenshots/side_y_minus.png
screenshots/side_y_plus.png
screenshots/top_z_plus.png
```

## Evidence hierarchy

```text
exported NMS JSON = serialized transform/export truth
AI Review object JSON = Blender-scene transform/design-loop evidence
AI Review screenshots = visual/design evidence
ordinary screenshots = visual evidence
part map = component geometry support
raw FBX = fallback when JSON + recipe + part map are insufficient
```

## Intake checks

When inspecting nms_ai_review_objects.json, report:

```text
schema
created_at
blender_version
scene name
object count
generated NMS object count
non-NMS/proxy/default objects
missing ObjectID count
non-uniform scale count
scene bounds / size
ObjectID frequency summary
role/tag/custom-property coverage
open topics from OPEN_TOPICS_LOG.md
screenshot set completeness
```

## Required cautions

- Do not treat the AI Review bundle as final in-game/export proof.
- Do not fix the build unless requested.
- Flag default Blender objects, proxies, raw meshes, or non-NMS objects separately from generated NMS parts.
- If the bundle reveals a repeated build lesson, propose promotion to `MASTER_LESSONS_LEARNED.md`, `MASTER_BUILD_RECIPES_AND_PLACEMENT_GUIDANCE.md`, or `data/PART_PLACEMENT_AID_LEDGER.json`.

## Standard output

A review response should include:

```text
Bundle contents
Scene stats
Validation concerns
Design observations
Recipe/part-map lessons to promote
Whether code changes are requested or blocked
```


## v01-v04 bundle handling

`validation/ai_review_bundle_check.py` now accepts classic v01 flat screenshot bundles and v02-v04 capture-set bundles.

Important review rule:

```text
If capture groups are identical/no-op or all objects are in one collection, do not claim collection-isolated review succeeded.
Use v04-style name clustering, spatial slices, and geometric interior/exterior candidates, or ask for a better bundle.
```

A visual bundle is design-loop evidence. It never replaces authoritative NMS Builder exported JSON or `validation/run_gate.py`.


### AI_REVIEW_BUNDLE_INTAKE_PROTOCOL structured sidecar (absorbed; preserved)
```json
{
  "schema": "NMS_AI_REVIEW_BUNDLE_INTAKE_PROTOCOL_2.19.00",
  "status": "active_optional_validation_protocol",
  "request_type": "validation_iteration",
  "secondary_mode": "design_loop_review",
  "expected_files": [
    "NMS_AI_REVIEW_CHECKLIST.md",
    "OPEN_TOPICS_LOG.md",
    "nms_ai_review_objects.json",
    "screenshots/front_x_minus.png",
    "screenshots/front_x_plus.png",
    "screenshots/iso_front_left.png",
    "screenshots/iso_front_right.png",
    "screenshots/rear_iso.png",
    "screenshots/side_y_minus.png",
    "screenshots/side_y_plus.png",
    "screenshots/top_z_plus.png"
  ],
  "evidence_rank": [
    "exported_nms_json",
    "ai_review_object_json",
    "ai_review_screenshots",
    "ordinary_screenshots",
    "part_map_component_geometry",
    "raw_fbx_fallback"
  ],
  "required_report_fields": [
    "schema",
    "created_at",
    "blender_version",
    "scene_name",
    "object_count",
    "generated_nms_object_count",
    "non_nms_or_default_objects",
    "missing_objectid_count",
    "nonuniform_scale_count",
    "scene_bounds",
    "objectid_frequency_summary",
    "screenshot_completeness",
    "open_topics"
  ],
  "action_policy": "do_not_modify_code_unless_user_explicitly_requests_code_changes"
}
```
