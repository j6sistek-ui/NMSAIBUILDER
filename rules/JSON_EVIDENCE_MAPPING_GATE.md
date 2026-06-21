# JSON Evidence Mapping Gate (1.03.01)

Status: **mandatory and foundational whenever relevant working JSON exists**.

This gate operationalizes `rules/WORKING_JSON_FIRST_PRINCIPLE.md`.

## Core rule

When exported NMS base JSON, pasted JSON, JSON-derived studies, or known working JSON recipes are available, they are not optional reference material. They are the best starting point for placement-sensitive generation because they contain serialized transform truth.

Do not write or repair a Python generator from generic `rx/rz`, memory, screenshot-only judgment, or FBX-only reasoning when relevant working JSON exists.

## Mandatory source check

Before generating or correcting code, check for relevant working JSON in:

- files provided in the current conversation;
- source/master-doc packages;
- reports and recipe studies;
- prior exported generated-build JSON;
- user-pasted JSON snippets;
- attached transfer packages.

If found, list the JSON evidence in the script provenance and use it first.

## Three JSON contexts

### A. JSON→Python recreation

Use the validated recreation stack:

```python
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
```

This context is for recreating an existing exported/copied JSON build in Blender/Python.

### B. High-quality source JSON recipe mining

Treat source JSON as a module/recipe database. Extract:

- ObjectID clusters;
- local coordinate frames;
- Position deltas;
- Up/At basis vectors;
- vector magnitudes/scale distributions;
- UserData/material choices;
- anchor relationships;
- module envelopes and repeated patterns.

Reproduce the control recipe first. Only then parameterize spacing, scale, count, material, or part variants using FBX bounds and design intent.

### C. Python-generated build validation

For fresh Python generators, do not blindly apply the JSON→Python recreation stack. Instead export the generated base to JSON and compare the serialized truth back to Python intent.

Use the reverse mapping:

```text
Blender/Python location (x, y, z) -> exported JSON Position [x, z, -y]
```

Then compare JSON `ObjectID`, `Position`, `Up`, `At`, vector magnitudes, and `UserData` against the intended object role.

## Required transform/recipe priority

1. Exact JSON ObjectID/Position/Up/At/UserData and scale vector lengths.
2. Extracted JSON cluster recipe: local frame, deltas, anchors, repeated spacing, module envelope.
3. Existing documented recipe/toolkit module.
4. FBX bounds and part-family rules for scale/spacing/contact adjustment.
5. Generic fallback only when no working JSON or recipe exists.

## Mandatory provenance block

Every JSON-informed script must include:

```python
JSON_EVIDENCE_PROVENANCE = {
    "source": "<filename, pasted JSON, study id, or master-doc recipe>",
    "context": "json_recreation | source_recipe_mining | generated_build_validation",
    "subsystems_derived_from_json": ["<stairs/airlock/vehicle/bridge/etc>"],
    "json_control_objectids": ["<ObjectID>"],
    "recipe_extraction": {
        "basis_vectors_checked": True,
        "position_deltas_checked": True,
        "scale_vector_lengths_checked": True,
        "anchors_checked": True,
        "fbx_bounds_cross_checked": True
    },
    "rule_refs": [
        "WORKING_JSON_FIRST_PRINCIPLE",
        "JSON_EVIDENCE_MAPPING_GATE",
        "JSON_GEOMETRY_VALIDATION_LOOP"
    ]
}
```

For JSON recreation scripts, include the recreation constants above.

For generated Python scripts that require post-export audit, include:

```python
EXPORTED_JSON_AUDIT_REQUIRED = True
PYTHON_TO_JSON_POSITION_MAP = "Position=[x,z,-y] for Blender/Python (x,y,z)"
JSON_AUDIT_FIELDS = ["ObjectID", "Position", "Up", "At", "UserData"]
```

## Failure-prone subsystems where this is non-negotiable

- stairs/ramps and landings;
- airlocks, iris doors, ring doors, hatch assemblies;
- skybridges, tubes, pipes, rails, conveyors, connected paths;
- vehicles, wheels, axles, shells, curved wall-panel bodies;
- billboards, signs, decals, display walls;
- rings/arcs/domes/chords;
- wall curvature, connected surfaces, trim runs;
- vines, plants, hanging objects, canopy attachments;
- interior machinery, market/shop modules, cargo/service bays.

## Governance failure

Skipping relevant working JSON evidence is a governance failure. If this occurs, activate `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md`, extract the JSON recipe, correct the generator, rerun the gate, and update the docs/memory if a new lesson is learned.

## validation hardening cross-check

When JSON evidence mode is required, `validation/run_gate.py` must not be treated as passed unless it reports nonzero generated objects, no execution error, no missing ObjectIDs, and no unresolved NMS Builder `Part` wrapper misuse. A script that declares the mapping constants but fails to actually create the expected JSON-derived objects is a validation failure, not a partial pass.

Required companion rule:

- `rules/VALIDATION_GATE_HARDENING_RULE.md`


## current-build JSON orientation requirement

If JSON has been provided for the current build or target subsystem, orientation is not to be guessed from the generic RX/RZ convention. Calculate it from the JSON basis: `Position`, `Up`, `At`, inferred Right vector, vector lengths, and the relevant context mapping. Use FBX bounds to understand the native part envelope and contact/clearance after transform. Only after the JSON-controlled placement is understood may the recipe be parameterized or adjusted.

## geometry-intelligence reinforcement

When relevant JSON exists, exact recreation is not the end state. Apply `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md` to preserve the reusable logic: part roles, anchors, local frames, connection/contact relationships, locked invariants, allowed parameter slots, and missing evidence.

If a prior JSON-derived technique cannot be found in `toolkit/PLACEMENT_RECIPE_LIBRARY.json`, `data/JSON_RECIPE_SIGNATURE_INDEX.json`, reports, or the source package, do not claim the technique was retained. Request the source JSON again or mark the recipe provisional.
