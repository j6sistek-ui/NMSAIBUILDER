# Validation Gate Hardening Rule — 1.03.02

## Status

Mandatory for generated Python scripts.

## Rule

A script cannot be called validated unless the executable gate proves that it ran, created nonzero generated objects, and did not misuse NMS Builder `Part` wrappers.

## NMS Builder wrapper handling

`BUILDER.add_part(ObjectID)` may return a wrapper object whose real Blender object is stored on `.object`. Scripts must use a safe helper such as:

```python
part = BUILDER.add_part(oid)
obj = getattr(part, "object", part)
```

Only the resolved Blender object may receive `.name`, `.location`, `.rotation_euler`, `.scale`, `.hide_viewport`, or `.copy()` calls.

## Gate requirements

The gate must fail if:

- the script raises an exception;
- generated placed part count is zero, unless explicitly allowed;
- ObjectIDs are missing;
- a generated script assigns Blender-object attributes directly to an unresolved `Part` wrapper;
- the script claims JSON evidence mode but lacks the validated mapping constants or provenance block.

## False-pass lesson

The Batman airlock V06 failure showed that syntax, ObjectID extraction, and declared JSON constants are insufficient. The script failed in Blender at `template.copy()` because `template` was a `Part`, not a Blender object. This must be machine-blocked.


## Evidence-of-learning gate

For `PART_BEHAVIOR_LEARNING`, `RULE_DISCOVERY_AND_PROOF`, and JSON/control-derived variants, validation must include protocol evidence in addition to script execution.

Required evidence:

```text
1. Derived invariant or PART_BEHAVIOR_SIGNATURE is stated.
2. Each generated variation traces back to that signature.
3. Locked objectives are preserved.
4. Forbidden substitutions are avoided.
5. Failure mode is attributed to fitment, offset, orientation, density, coverage, scale, material/ObjectID mapping, or construction-style mismatch.
```

A build may pass `run_gate.py` and still fail the learning/proof gate if it does not reuse the source behavior requested by the user.

## semantic gate proposal note

The V25-V38 stair study identified a class of false positives in generic AABB no-float validation.

Generic AABB remains the primary gate. Do not globally loosen it to satisfy a family-specific edge case.

For families with proven semantic connection rules, a future gate may apply this pattern:

```text
AABB PASS -> PASS
AABB FAIL -> family semantic validator
semantic PASS -> override AABB failure
semantic FAIL -> FAIL
```

At 2.13.00 this is documented as a proposal in `MASTER_LESSONS_LEARNED.md` (removed historical reference: rules/SEMANTIC_FLOAT_GATE_PROPOSAL.md), not an adopted gate behavior.

Candidate family: stairs, especially terminal stair landings whose correct connection follows:

```text
expected_floor =
    ramp.position
    + ramp.At * RUN_STEP
    + ramp.Up * RISE_STEP
```

## raw gate verdict and scope hardening

Validation reports must preserve the raw executable verdict.

```text
Raw gate PASS -> report PASS.
Raw gate FAIL -> report FAIL.
Temporary continuation approval -> report separately.
Semantic review/proposed exception -> report separately.
```

Do not rename a raw gate failure as a pass because the build is visually plausible or because a semantic validator is proposed.

Every gate report must state scope:

```text
full_regression
partial_matrix
stadium_only
switchback_only
corner_only
generated_file_only
source_doc_release
```

Example:

```text
Generic AABB gate: FAIL
Gate scope: full stair regression
Temporary stair continuation: ALLOWED
Semantic stair override: NOT ADOPTED
```

or:

```text
Generic AABB gate: PASS
Gate scope: stadium-corner-only matrix
Semantic stair connectivity: NOT PROVEN
Full stair-family float status: NOT TESTED
```

## Stair float-gate lesson

The stair V25-V38 branch showed that a generic AABB/no-float gate can false-fail a semantically correct terminal stair landing. Later stadium-only/corner-only studies may pass the generic gate because the known switchback terminal-landing outlier is excluded.

Therefore:

```text
A no-float PASS must state test scope.
A stadium-only PASS is not a full stair-family PASS.
Temporary stair continuation does not convert raw FAIL to PASS.
Semantic float-gate behavior remains proposed until explicitly adopted.
```


## scoped stair semantic validator adoption

The 2.13.01 rule remains: raw executable gate results must be preserved.

At 2.14.00, a scoped semantic validator is adopted for normal full-ramp stairs only.

Reports must include both fields:

```text
raw_aabb_float_gate: PASS/FAIL
stair_semantic_connection_gate: PASS/FAIL/NOT_RUN
```

A stair semantic PASS may accept the normal stair placement relation, but it must not erase or rewrite the raw AABB verdict.

All other part families continue to require strict AABB conformance unless a separate source-doc semantic validator is approved for that family.


## release-check timeout hardening

`release/release_check.py` is the authoritative source-doc release gate. If it times out in a constrained environment due to repeated Python site-startup hooks, fix the release tooling rather than downgrading the gate.

Approved hardening:

```text
Nested release-check subprocesses may run with python -S.
This skips site-startup hooks only.
It must not remove or weaken validation checks.
```

A release package may claim `release_check PASS` only when the full release check actually completes and prints:

```text
RELEASE GATE: PASS
```


## Runtime build-script actually-built check (absorbed from BLENDER_RUNTIME_BUILD_SCRIPT_PROTOCOL)
## Status

Mandatory for every NMS Builder Python deliverable intended to place parts in Blender.

## Failure prevented

Multiple generated scripts compiled and produced preview JSON but placed no parts because they never imported the NMS Builder runtime. A static compile is not proof that a Blender build script will create objects.

## Required runtime path

A Blender placement script must include a real runtime path:

```python
import bpy
from bl_ext.user_default.no_mans_sky_base_builder import BUILDER
created = BUILDER.add_part(part_id)
obj = getattr(created, "object", created)
# copy/template or direct object use
bpy.context.collection.objects.link(obj)
```

Equivalent collection-specific linking is acceptable when it uses Blender collections and real linked objects.

## Prohibited for Blender deliverables

```text
- preview-JSON-only fallback as the only placement mechanism
- globals().get("BUILDER") with no import/runtime path
- claiming Blender runtime PASS when Blender was not run
- delivering a generated build script that cannot place parts in Blender
```

## Required receipts

Generated Blender scripts should embed:

```python
REQUEST_CLASSIFICATION
USED_PART_LOGIC
BUILD_INTENT_GRAPH
GEOMETRY_CONSTRUCTION_PLAN
```

and a companion Open Topics Log.

## Executable support

Use:

```text
validation/blender_runtime_script_check.py
```

before delivery. If it fails, the build artifact is blocked.


### BLENDER_RUNTIME_BUILD_SCRIPT_PROTOCOL structured sidecar (absorbed; preserved)
```json
{
  "schema": "VALIDATION_GATE_HARDENING_RULE",
  "status": "mandatory",
  "source_rule": "rules/VALIDATION_GATE_HARDENING_RULE.md",
  "purpose": "NMS build-generation hardening rule.",
  "required_for": [
    "Blender NMS Builder Python deliverables"
  ],
  "must_include": [
    "import bpy",
    "BUILDER.add_part",
    "object linking",
    "no preview-only fallback"
  ]
}
```
