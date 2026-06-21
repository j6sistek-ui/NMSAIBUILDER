# Prohibited and Placeholder Objects

## HOLO_DISCO / HOLO_DISCO_0

`HOLO_DISCO` and `HOLO_DISCO_0` are Wonder Projector ObjectIDs. Do not generate either in scripted builds because it requires in-game setup/configuration. It may only be preserved when the user explicitly provides an already configured existing object.

## U_PARAGON

`U_PARAGON` is not the Wonder Projector. Treat it as a plugin/default placeholder or non-visible artifact. Do not interpret it as intentional visible build geometry and do not design around it.

See `PROHIBITED_AND_PLACEHOLDER_OBJECTS.md` for machine-readable policy.


## v50 update

`HOLO_DISCO_0` was added/exposed in Base Builder 6.4.1 and is treated the same as `HOLO_DISCO`: prohibited for generated builds unless preserving an explicitly configured user object.


## Non-uniform scale safety (negative knowledge) (absorbed from NONUNIFORM_SCALE_SAFETY)
## Purpose

A script can use real NMS plugin ObjectIDs and still violate build safety if it stretches a part into geometry the game does not support.

The Bumblebee V01 leg failure demonstrated this: a real concrete short wall was non-uniformly stretched into a long leg member, causing weird in-game behavior.

## Rule

Default final-build behavior:

```text
Use uniform scale for generated NMS parts.
Do not non-uniformly stretch a part to fake a longer/wider/thinner geometry.
```

If a long line/leg/rail/rod is required:

```text
Repeat uniformly-scaled real segments with slight overlap.
Do not stretch one segment.
```

## Allowed exception

A non-uniform scale may be used only if:

1. the user explicitly approves the deviation, or
2. the specific part/family has a validated rule saying non-uniform scaling is safe for that role.

The exception must be documented in the Object Use Manifest.

## Validation requirement

Script validation must scan for obvious non-uniform scaling patterns:

```python
sx != sy or sx != sz
obj.scale = (a, b, c) where a/b/c differ
```

If found, the script must either:
- rewrite using uniform real segments, or
- request user approval before delivery.

## Preferred repair pattern

For long members:

```text
segment_count = ceil(target_length / (native_extent * uniform_scale * (1 - overlap)))
place repeated parts along the vector
each part scale = (s, s, s)
```

This preserves NMS part behavior and avoids unsupported stretching.


## Pipe/BUBPIPE contextual-connector validation-required (absorbed from PIPE_BUBPIPE_CONTEXTUAL_CONNECTOR_RULE)
Status: active exception rule. Supersedes the narrower 3.01.01 PIPE/BUBPIPE validation exception wording.

## Trigger

Apply this rule whenever a generated build, validation harness, JSON analysis, or placement analysis uses any of these ObjectIDs:

```text
PIPE
BASE_BUBPIPE
BASE_BUBPIPE_S
BASE_BUBPIPE_L
BASE_BUBPIPE_T
BASE_BUBPIPE_X
```

Also apply it to bubble ducts, default pipe, bent duct runs, translucent liquid/glass pipe runs, pipe loops, pipe assemblies, or any connected pipe feature using these parts.

## Evidence basis

User-provided evidence now includes:

- Blender screenshots where BUBPIPE appears as upright/disconnected cylinder-like parts rather than the in-game translucent pipe network.
- In-game screenshots where BUBPIPE resolves as translucent orange bubble tubing with bends and continuous runs.
- Exported JSON containing 16 `^BASE_BUBPIPE` placements and 3 `^PIPE` placements.
- JSON transforms showing stable local axes and approximately 2.0-unit connector steps along those local axes.

The supplied JSON has repeated `^BASE_BUBPIPE` records with approximately:

```text
Up ≈ [-0.989277, -0.000413, 0.146049]
At ≈ [0.000464, -0.999999, 0.000316]
```

The first observed BUBPIPE-to-BUBPIPE deltas project to approximately ±2.0 on local Up, At, or derived Right. This indicates a local-axis connector graph, not ordinary isolated mesh placement.

## Correct interpretation

BUBPIPE/PIPE are contextual connector parts.

```text
JSON transform data = useful / high-value evidence
Blender static visual rendering = not authoritative
Blender bbox extraction = not authoritative for final in-game pipe appearance
In-game screenshot/exported JSON/focused pipe harness = required for connected assembly validation
```

The 3.01.00 verified part-map data remains valid as raw Blender spawn/measurement data. It is not sufficient to mark this family as fully placement-validated for connected pipe assemblies.

## Object policy

For the listed parts:

```text
ValidationStatus = GAME_VALIDATION_REQUIRED_PIPE_CONTEXTUAL_CONNECTOR
MechanicsUseRecommendation = USE_ONLY_WITH_PIPE_ASSEMBLY_VALIDATION
```

`PIPE` must not be classified as `DO_NOT_USE`; it is a valid in-game default pipe object. Its Blender zero-bbox/invisible behavior only means Blender extraction cannot validate its in-game geometry.

## Required generation behavior

Generated scripts may use PIPE/BUBPIPE only when the output labels the assembly as provisional or includes a follow-up validation loop. For connected pipe features, the generator must treat the assembly as a pipe graph:

```text
node position = connector point
connector axes = local Up / local At / derived Right
observed step = approximately 2.0 units
visual result = game-resolved pipe network
```

A connected pipe feature is not validated until confirmed by in-game screenshot, exported JSON, or a focused pipe-specific validation harness.

## Rotation guidance

- RX90 may fix isolated Blender appearance/orientation.
- RX90 does not prove bend continuity.
- Do not assume global RX90 equals the correct local connector transform for all pipe nodes.
- Local-vs-global correction remains validation-TBD for pipe assemblies.

## Relation to recipe-first rule

This rule strengthens the existing recipe-first model:

```text
Recipes control assemblies.
Verified part map controls ordinary component mechanics.
PIPE/BUBPIPE require contextual connector recipe validation.
```


### PIPE_BUBPIPE_CONTEXTUAL_CONNECTOR_RULE structured sidecar (absorbed; preserved)
```json
{
  "schema": "NMS_PIPE_BUBPIPE_CONTEXTUAL_CONNECTOR_RULE_3.01.02",
  "status": "active_exception_rule",
  "source_docs_rev": "3.01.02",
  "trigger_objectids": [
    "PIPE",
    "BASE_BUBPIPE",
    "BASE_BUBPIPE_S",
    "BASE_BUBPIPE_L",
    "BASE_BUBPIPE_T",
    "BASE_BUBPIPE_X"
  ],
  "validation_status": "GAME_VALIDATION_REQUIRED_PIPE_CONTEXTUAL_CONNECTOR",
  "mechanics_use_recommendation": "USE_ONLY_WITH_PIPE_ASSEMBLY_VALIDATION",
  "evidence_files": [
    "data/PIPE_BUBPIPE_JSON_EVIDENCE_3.01.02.json",
    "data/PIPE_BUBPIPE_CONTEXTUAL_CONNECTOR_EVIDENCE_3.01.02.json"
  ],
  "observed_connector_step": "approximately 2.0 units along local Up/At/derived Right axes in user-provided JSON",
  "rule": "Treat PIPE/BUBPIPE as contextual connector assembly parts. JSON transform data is useful; Blender bbox/visual extraction is not authoritative for in-game connected pipe behavior.",
  "rx90_guidance": "RX90 may correct isolated parts but does not validate connected-pipe continuity or local/global transform correctness."
}
```
