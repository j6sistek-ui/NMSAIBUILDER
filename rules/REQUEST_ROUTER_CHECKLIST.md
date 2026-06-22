# Request Router Checklist

## Status

**Mandatory first-gate rule.** This file is not optional background reading. It is the active routing layer that makes the rest of the master documents usable, and it holds the authoritative bundle map (the matrix and START HERE point here for it).

## Purpose

The master package contains many rules. A chat cannot reread every document for every message, but it must not guess which rules apply. Every request is first classified, then routed to the smallest sufficient rule bundle. This solves the failure mode where a rule exists in the master docs but is not applied.

## Mandatory first step — classify the request

Before acting, classify the current user input:

```text
□ build_generation             (deep: new build / redesign / added design features -> full knowledge base)
□ build_specific_addition       (specific: user named the exact element, e.g. 'add blue lights' -> placement facts)
□ build_refinement_or_optimization (lean: fix/optimize existing -> safety + validation only)
□ json_to_python_recreation
□ python_generated_json_audit
□ high_quality_source_json_recipe_mining
□ screenshot_or_ingame_evaluation
□ reference_image_or_external_example
□ source_doc_review_or_patch
□ protocol_correction_or_failure
□ script_debugging_or_error_log
□ project_specific_corvette
□ part_behavior_learning        (user teaches part behavior / fitment / reusable applications)
□ rule_discovery_and_proof      (working source -> infer rule -> apply -> verify)
□ new_geometry_synthesis        (new recognizable object / freeform shape)
□ other / clarify
```

Then load/check the matching bundle in `rules/REQUEST_ROUTER_CHECKLIST.json`, and the relevant rows of the bundle map below.

## Always-required governance bundle

Every non-trivial NMS response considers:

- `00_START_HERE_CURRENT.md`
- `00_KICKOFF_INTAKE_GATE.md`
- `rules/REQUEST_ROUTER_CHECKLIST.md` / `rules/REQUEST_ROUTER_CHECKLIST.json`
- `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md`
- `rules/UNIVERSAL_RULES.md`

For any generated build, also load the placement-intelligence set: `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md`, `data/METHOD_AUTHORITY_TABLE.json`, `data/PLACEMENT_PRECEDENCE.json`, `data/NEGATIVE_KNOWLEDGE_INDEX.json`, and `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md`.

## Execution kernel and recipe-first feature routing

After classification, apply `rules/NMS_BUILDER_EXECUTION_KERNEL.md`. For `build_generation`, run the feature router before part selection: `rules/PROMPT_TO_FEATURE_ROUTER.md` / `.json`, then check `MASTER_BUILD_RECIPES_AND_PLACEMENT_GUIDANCE.md`, `toolkit/PLACEMENT_RECIPE_LIBRARY.md`, and `data/JSON_RECIPE_SIGNATURE_INDEX.json` before using component dimensions to synthesize an assembly.

```text
known feature terms -> matching recipe/signature/toolkit entry -> FEATURE_RECIPE_LOOKUP receipt -> part-map component validation
```

If the user asks for a building, room, tower, skyscraper, enclosed wall, city block, airlock, iris, ramp, stair, bridge, catwalk, dome, spire, or vehicle, do not start from component dimensions alone — load the matching recipe route or declare `recipe_status=none_found` with uncertainty. If a prior JSON-derived recipe cannot be found in the recipe library, signature index, reports, or source package, say so and request the original JSON again rather than inventing the missing invariant set.

## The bundle map — trigger / route -> load these

This table is the authoritative routing map. Each row lists the docs to load for that trigger, on top of the always-required governance bundle.

| Trigger / route | Load |
|---|---|
| `build_generation` ("build / design a base / castle / facade / feature") | `02_GENERATOR_CONTRACT.md`, `rules/PROMPT_TO_FEATURE_ROUTER.md`, `MASTER_BUILD_RECIPES_AND_PLACEMENT_GUIDANCE.md`, `toolkit/PLACEMENT_RECIPE_LIBRARY.md`, `rules/SPACING_CONNECTION_SCALE_RULES.md`, placement-intelligence set |
| Known feature variant (same feature, different) | `rules/RECIPE_PARAMETERIZATION_PROTOCOL.md`, `rules/PROMPT_TO_FEATURE_ROUTER.md`, `data/JSON_RECIPE_SIGNATURE_INDEX.json` |
| User provides JSON for exact recreation | `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`, `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`, `rules/JSON_EVIDENCE_MAPPING_GATE.md`, `rules/WORKING_JSON_FIRST_PRINCIPLE.md` |
| JSON study / recipe mining | `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`, `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`, `toolkit/PLACEMENT_RECIPE_LIBRARY.md` |
| Airlock / iris / vault / portal door | `rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md`, `rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md`, `rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md` — visible `Protocol confirmation` required; higher side counts preserve the iris center/pivot/radius and increase overlap density |
| Spire / tapered tower / cupola / roof cap | `rules/CONNECTED_PIECE_CURVATURE_GRAMMAR.md` + `MASTER_LESSONS_LEARNED.md` (spire study notes are consolidated there). Preliminary until exported JSON is reviewed; do not lock exact ObjectIDs/orientations from images alone |
| Curved / rounded / tapered / shell / hull / ribbed / arched / circular feature | `rules/CONNECTED_PIECE_CURVATURE_GRAMMAR.md` — route by the underlying curve/path/profile/convergence method, not the named label (dome, spire, cupola, rounded shell, curved roof, vehicle hull, pod, cylindrical habitat, circular tower, machine core, arch, rib, collar, oculus) |
| Power / utility infrastructure in JSON or build | Default-exclude per `rules/UNIVERSAL_RULES.md` (`INCLUDE_POWER_UTILITY=False`). Do not promote powerlines, switches, batteries, solar, or biogenerators into feature recipes unless the user explicitly requests power/cable/logic design |
| Assembled subsystem from repeated/adjacent parts (stairs, ramps, ladders, catwalks, bridges, rails, towers, spires, roof crowns, caps, wall bays, trim rings, vehicles, machinery, airlocks, cave interiors) | `rules/DISCONNECTED_ASSEMBLY_HARDSTOP_RULE.md` — state the connection model and provide proof (anchors or ring/center/radius, endpoint/path basis, step/chord, contact tolerance, origin mode, expected continuity, failure action) |
| New recognizable object / freeform shape | `new_geometry_synthesis`: `rules/FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL.md`, `rules/FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL.md`, `rules/FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL.md`, `rules/C_TRIFLOOR_EDGE_CONTACT_GRAPH_PROTOCOL.md`, `rules/VALIDATION_GATE_HARDENING_RULE.md`, `validation/geometry_construction_manifest_check.py`, `validation/blender_runtime_script_check.py` — generate the target geometry first; scattering parts in a region is not a routed method |
| Screenshots / images included | `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md` (retention) and `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md` |
| Reference image / external example | `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md`, `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md` |
| `part_behavior_learning` / `rule_discovery_and_proof` | `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md`, `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md`, `rules/WORKING_JSON_FIRST_PRINCIPLE.md`, `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`, `rules/RECIPE_PARAMETERIZATION_PROTOCOL.md`, `rules/VALIDATION_GATE_HARDENING_RULE.md`; partmap storage: `rules/PART_PLACEMENT_MAP_SCHEMA.md`, `rules/PART_PLACEMENT_MAP_SCHEMA.md`, `rules/PART_PLACEMENT_MAP_SCHEMA.md` |
| `source_doc_review_or_patch` | `rules/SOURCE_DOC_EVALUATION_CHECKLIST.md`, `rules/DOCS_UPDATE_AVAILABILITY_PROTOCOL.md`, `rules/PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md`, `rules/OPEN_TOPICS_LOG_PROTOCOL.md`, `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md` |
| `protocol_correction_or_failure` | `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md` — check for wrong banner format, skipped Docs-Avail definition, softened/hidden raw verdict, partial gate PASS promoted as full PASS, a documented proposal treated as adopted doctrine, or a transfer summary used without reconciling source docs |
| NMS-context "create/make/build/design/generate a …" | `rules/NMS_BUILD_VS_IMAGE_ROUTING_GUARD.md` — routes to `build_generation`, never a silent image, unless explicit image/render/mockup/concept-art output is requested |
| New master/source package uploaded | `rules/FULL_VERSION_CONTINUITY_REVIEW_RULE.md` — review all changes since the chat's last version, not only the latest patch; state review scope |
| Generated Blender/NMS build script | `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md`, `validation/ai_capture_compliance_check.py`; full building/room/interior/city: `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md`, `rules/FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL.md` — plan exterior/interior/cutaway/decor/scene captures before coding |
| AI review bundle uploaded (`NMS_AI_REVIEW_Scene_*.zip`) | `validation_iteration` design-loop review: `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md`, `validation/ai_review_bundle_check.py` |
| Corvette / ship intent | `corvette/CORVETTE_KNOWLEDGE_REPOSITORY.md`, `corvette/CORVETTE_VALIDATION_CHECKLIST.md` (boundary limits applied per the Corvette rows in `RULE_APPLICATION_MATRIX.md` and the generator contract) |
| Experimental / vague / "surprise me" | `rules/EXPERIMENTAL_REQUEST_PROTOCOL.md` |

## Stop conditions

Immediately stop normal execution and run the CAPA workflow if any of these occur:

- the user corrects a rule, protocol, or source interpretation;
- intent of a reference/example/image is ambiguous;
- working JSON exists but was not checked before generation/correction;
- script output conflicts with `run_gate.py`, the JSON evidence gate, or exported JSON;
- screenshots contradict intended placement/orientation;
- the assistant realizes it skipped a required bundle.

## Required classification block for major generated scripts

Generated scripts embed a small manifest so `run_gate.py --require-router` can verify routing happened:

```python
REQUEST_CLASSIFICATION = {
    "request_type": "build_generation",
    "user_inputs": ["working_json", "screenshots"],
    "rule_bundles_checked": [
        "UNIVERSAL_RULES",
        "WORKING_JSON_FIRST_PRINCIPLE",
        "JSON_EVIDENCE_MAPPING_GATE",
        "FBX_PART_DIMENSION_RULES",
        "PART_ORIENTATION_OVERRIDES",
        "SCRIPT_VALIDATION_LOOP"
    ],
    "ambiguity_resolution": "not_needed_or_user_confirmed",
    "json_evidence_used": True
}
```

Protocol-sensitive responses (source-doc updates, JSON studies, screenshot intake, build generation) run `rules/REQUEST_ROUTER_CHECKLIST.md` and carry a visible `Protocol confirmation`. All substantive NMS responses end with the current banner (`rules/PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md`, `templates/PROTOCOL_CONFIRMATION_BANNER_TEMPLATE.md`, `rules/DOCS_UPDATE_AVAILABILITY_PROTOCOL.md`): numeric `source docs rev` and `Docs Avail for Update?: Yes/No (count)`.

## Core principle

Do not add more prose rules without a routing/gating mechanism. If a new rule is important enough to prevent failures, add it to the relevant router bundle above and, where possible, to an executable gate.


## Routing rule application gate (absorbed from PROMPT_ROUTING_RULE_APPLICATION_GATE)
Status: **mandatory pre-response gate**

## Purpose

Protocol rules are only useful if they are actually applied at the start of each user request. This gate exists because prior responses acknowledged rules but failed to apply them, especially the selective visual-memory/image-retention policy during source-doc updates.

## Core rule

```text
Before acting on any prompt, classify the prompt type and identify applicable rules.
If a rule is triggered, apply it before generating output or updating files.
If a rule is triggered but not applied, that is a failure.
```

This is a preflight gate, not a post-hoc explanation.

## Required pre-response classification

For every NMS project prompt, classify the request as one or more of:

```text
SOURCE_DOC_REVIEW
SOURCE_DOC_UPDATE
JSON_FEATURE_RECIPE_EXTRACTION
JSON_RECREATION_CONTROL
JSON_PARAMETRIC_VARIANT_DERIVATION
JSON_GEOMETRY_INTELLIGENCE_EXTRACTION
CONTROL_TO_VARIANT_DERIVATION
FEATURE_INTENT_ROUTING
PYTHON_BUILD_GENERATION
PYTHON_BUILD_REFINEMENT
SCREENSHOT_OR_VISUAL_REFERENCE_INTAKE
IMAGE_RETENTION_DECISION
PART_RULE_OR_FORBIDDEN_USAGE_UPDATE
MEMORY_RETENTION_OR_TRANSFER
GENERAL_QA
```

## Required rule lookup

After classification, check the relevant source locations.

### If substantive NMS work is involved

```text
rules/NMS_BUILDER_EXECUTION_KERNEL.md
NMS_BUILDER_OBJECTIVE_CHARTER.md
```

### If adapting a known feature or making a variant

```text
rules/RECIPE_PARAMETERIZATION_PROTOCOL.md
rules/PROMPT_TO_FEATURE_ROUTER.md
data/JSON_RECIPE_SIGNATURE_INDEX.json
```

### If JSON is being learned from, not merely recreated

```text
rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md
data/JSON_RECIPE_SIGNATURE_INDEX.json
```

### Always check for NMS source-doc work

```text
00_START_HERE_CURRENT.md
00_KICKOFF_INTAKE_GATE.md
rules/REQUEST_ROUTER_CHECKLIST.md
RULE_APPLICATION_MATRIX.md
00_MEMORY_RECALL_INDEX.md
```

### If new source package is involved

```text
rules/FULL_VERSION_CONTINUITY_REVIEW_RULE.md
release/VERSION.json
PACKAGE_MANIFEST.json
archive/changelogs/
```

### If JSON is involved

```text
rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md
rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md
rules/WORKING_JSON_FIRST_PRINCIPLE.md
rules/JSON_EVIDENCE_MAPPING_GATE.md
```

### If generated build/script is involved

```text
02_GENERATOR_CONTRACT.md
rules/SPACING_CONNECTION_SCALE_RULES.md
toolkit/PLACEMENT_RECIPE_LIBRARY.md
rules/FORBIDDEN_DEFAULT_EXCLUDED_OBJECTID_USAGE.md
rules/POWER_UTILITY_EXCLUSION_RULE.md
```

### If screenshots or visual examples are involved

```text
rules/SELECTIVE_VISUAL_MEMORY_POLICY.md
rules/SELECTIVE_VISUAL_MEMORY_POLICY.md
rules/SELECTIVE_VISUAL_MEMORY_POLICY.md
```

### If curved/rounded/tapered/shell features are involved

```text
rules/CONNECTED_PIECE_CURVATURE_GRAMMAR.md
```

### If airlock / iris / portal / vault door is involved

```text
rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md
toolkit/AIRLOCK_IRIS_PARAMETRIC_GENERATOR_SKELETON.py
```

## Required protocol-application audit for source-doc updates

Every source-doc update package must include a report section named:

```text
Protocol Application Audit
```

Minimum fields:

```text
Request classification:
Source package baseline:
Continuity reviewed:
Rules checked:
Rules applied:
Rules intentionally not applied:
Image-retention decision:
Forbidden/default-excluded ObjectIDs considered:
JSON evidence mode:
Generated files:
Known limitations:
```

## Visual/image retention hard gate

When images/screenshots are supplied and a package update may archive them, the image-retention policy must be applied before copying images into the package.

Required decision:

```text
image_retention_level = DOCUMENT_LESSON_ONLY | KEEP_1_TO_2_ANCHORS | CONTACT_SHEET_ONLY | FULL_REFERENCE_SET_APPROVED
```

Default for repeated concept screenshots:

```text
DOCUMENT_LESSON_ONLY
```

or, if images are truly needed:

```text
KEEP_1_TO_2_ANCHORS
```

Full-size multi-image retention requires explicit justification or user approval.

## Required response behavior

For NMS project protocol-sensitive requests, the final response must include:

```text
Protocol confirmation
```

At minimum:

```text
Request classification:
Rules checked:
Rules applied:
Known miss / limitation:
Next action:
```

Do not provide vague confirmations like "looks good" or "done" without the protocol context when a source-doc, JSON, screenshot, or generation rule is involved.

## Failure classification

If a previous response failed to apply a triggered rule, label the failure directly:

```text
Protocol application failure
```

Then either:

1. correct it in the current package, or
2. explain why no package correction is being made.

## Relationship to existing rules

This gate does not replace the existing router, visual policy, JSON protocols, or generator contract. It forces them to be used.

```text
Router finds the rule.
This gate proves the rule was applied.
```


## Image retention explicit check label

This rule explicitly requires an **Image retention** decision before screenshots/images are copied into a master source package.


## Traceable evidence requirement

For protocol-sensitive requests, the response must include or produce evidence that the mapped documents were used. The required evidence is defined in `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md`.

Add request classes:

```text
PART_BEHAVIOR_LEARNING
RULE_DISCOVERY_AND_PROOF
```

If these are triggered, `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md` and `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md` are mandatory. A protocol banner without a request trace or verification receipt is insufficient for claiming learning/proof compliance.
