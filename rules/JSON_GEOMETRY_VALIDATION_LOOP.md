# JSON Geometry Validation Loop (v59)

This is now a core validation requirement for serious procedural builds.

## Core concept

Python is **intent**. Blender/plugin generation is **scene realization**. Exported NMS base JSON is **serialized transform truth**. Screenshots are **visual outcome**.

The loop is:

```text
Python generator intent
→ Blender/NMS Builder generated objects
→ exported/imported base JSON
→ GPT JSON-vs-Python transform audit
→ Blender/in-game screenshot review
→ rule/script correction
→ regeneration
```

## What the JSON audit catches

The exported JSON can catch issues that screenshots alone miss or make ambiguous:

- wrong inherited rotations,
- side-map reversals,
- part-specific axis exceptions,
- local-X vs local-Z connector mistakes,
- missing or duplicated objects,
- non-uniform scale misuse,
- incorrect material/UserData assignment,
- objects that are mathematically placed but visually floating/clipping,
- mismatch between intended path assemblies and serialized rotation values.

## Required GPT audit format

For each sensitive subsystem, compare:

| Field | Python intent | Exported JSON | Screenshot/In-game outcome | Decision |
|---|---|---|---|---|
| ObjectID | expected part | actual part | visible role | keep/fix |
| Position | intended socket/center | serialized XYZ | clipping/floating? | adjust offset? |
| Rotation | intended RX/RY/RZ/path basis | serialized rotation | aligned? | add override? |
| Scale | intended scale | serialized scale | right size? | recalibrate? |
| Role | design role | object name/tag/metadata | reads correctly? | promote lesson? |

## Promotion rule

Do not promote a project observation into a universal rule just because it worked once. Classify lessons as:

- **universal generator contract**,
- **part-specific override**,
- **assembly-pattern rule**,
- **terrain/context rule**,
- **creative use-case/toolkit entry**,
- **niche project-specific note**.

The goal is not to wall knowledge off by project. The goal is to apply lessons broadly when the same part, assembly pattern, terrain condition, or design problem appears again.



## JSON evidence precondition

When JSON is available before code generation, the JSON loop starts before script authoring, not after a failed screenshot. The generator must use `rules/JSON_EVIDENCE_MAPPING_GATE.md` and the validated transform stack as the placement basis.

The exported JSON's `ObjectID`, `Position`, `Up`, `At`, and `Up`-vector scale must be treated as serialized transform truth. For known subsystems such as airlocks, stairs/ramps, vehicles, rings, and connected surfaces, use the JSON basis vectors and local spacing as control data before applying FBX-only or generic orientation assumptions.


## working JSON first reinforcement

When working JSON exists before generation, the JSON loop starts **before** script authoring. The generator must first search for and extract relevant JSON evidence using `rules/WORKING_JSON_FIRST_PRINCIPLE.md` and `rules/JSON_EVIDENCE_MAPPING_GATE.md`.

High-quality source JSON is a control recipe. Do not approximate a known working subsystem from memory. Extract ObjectID clusters, Position deltas, Up/At basis vectors, serialized scale vector lengths, UserData, anchor relationships, and module envelopes. Cross-check those transforms with FBX bounds for scale/clearance adjustment.

For generated Python builds, exported JSON is the reverse audit layer. Use `Position=[x,z,-y]` for Blender/Python `(x,y,z)`, then compare `Up` and `At` against the intended local path/facing/up. This is separate from JSON→Python recreation and must not double-apply `LOCAL_Y_180` to direct Blender-space procedural placement.

A build is not validated until the serialized JSON facts and screenshot/in-game outcome agree with the Python design intent.
