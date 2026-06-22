# Placement Precedence Resolution Procedure — THE PART PROCEDURE  (introduced 5.00.00)

## Status

**MANDATORY. THIS IS THE LAW.** This procedure runs for every placement, in
generated Python and in live Blender sessions alike. Skipping it is a failure.

Reading `data/PLACEMENT_PRECEDENCE.json` is NOT resolving precedence. Resolution
is an explicit, recorded step that produces an artifact. The workflow reminds you
every time so you do not have to remember that it matters.

## The workflow — every placement, in order

```text
Placement Intent  ->  Precedence Resolution  ->  Method Selection
```

### 1. Placement Intent
State, for the part or subassembly: what it is, where it must go, and what it
must connect to. One line is enough, but it must exist.

### 2. Precedence Resolution  (the first duty)
Walk `data/PLACEMENT_PRECEDENCE.json` tiers 1 → 7 and select the HIGHEST tier
that has data for this ObjectID/feature. Record the resolution:

```text
objectid:        ^<ObjectID>
governing_tier:  <1..7 from PLACEMENT_PRECEDENCE.json>
source_file:     <the exact file that supplied the governing data>
source_ref:      <recipe id / snap group / part-map row / rule id>
```

Tier reminders:
1. EXACT_JSON_RECIPE_OR_KNOWN_FEATURE_RECIPE
2. AUTHORITATIVE_PLUGIN_SNAP_OR_RELATIONAL_DATA
3. VALIDATED_ASSEMBLY_RECIPE
4. VERIFIED_PARTMAP_COMPONENT_MECHANICS
5. PART_PLACEMENT_MAP_OR_ORIENTATION_OVERRIDE
6. EXCEPTION_OR_PROHIBITED_INDEX  (overrides positive component data)
7. MANUAL_REVIEW_FALLBACK  (only if `data/METHOD_AUTHORITY_TABLE.json` allows)

Hard rules (from the precedence file): assembly context supersedes component
context; component validation never proves assembly validity; an ObjectID on the
negative-knowledge / exception index is governed by tier 6 regardless of how good
its component data looks; FBX is below tier 4 and is fallback only.

### 3. Method Selection
Choose the placement method from `data/METHOD_AUTHORITY_TABLE.json` consistent
with the governing tier, then place.

## Output (required)
Every placement's resolution rolls up into the build's
`BUILD COMPLIANCE MANIFEST` (`rules/BUILD_COMPLIANCE_MANIFEST_RULE.md`), which is
verified by `validation/compliance_manifest_check.py`. No manifest, or a manifest
whose receipts do not re-verify against the cited sources, means the build is
invalid.

## Why this is a step and not a reference
A reference is something you may consult. A step is something the workflow forces
you to perform and record. Precedence is a step. If you produced placement code
without a recorded precedence resolution for each ObjectID, you did not do the
work — you guessed and it looked right.


## Authority order (absorbed from PART_DATA_AUTHORITY_STATEMENT)
## Status

**MANDATORY. Resolves stale authority rules.** There are several part-data
sources in this package. They are NOT equal, and older framing that elevated FBX
is overruled. Authority follows `data/PLACEMENT_PRECEDENCE.json`:

```text
HIGHEST
  1  exact exported JSON recipe / known-feature recipe / validated signature
  2  add-on snap + relational data (library/authoritative_snap/) for snap-covered joins
  3  validated assembly recipe (with conformance criteria)
  4  verified part map (library/nms_master_part_map_verified_data_v3_01_02.json):
        origin, bbox, default orientation, scale behavior  -- COMPONENT mechanics only
  5  part placement maps / orientation overrides (rules/PART_ORIENTATION_OVERRIDES.md)
  6  negative knowledge / exceptions (data/NEGATIVE_KNOWLEDGE_INDEX.json) -- overrides positive data
  7  manual review fallback (only if data/METHOD_AUTHORITY_TABLE.json permits)
LOWEST
     raw FBX bounds (library/nms_full_fbx_bounds.csv) -- LAST RESORT fallback only
```

## Explicit corrections to stale rules
- **FBX is no longer "the most important data."** It is the lowest-authority
  fallback, used only when JSON/recipe, snap/relational, validated recipe, the
  verified part map, placement maps, and exceptions are all silent. Where the
  verified part map and FBX-derived extents disagree, the verified part map wins.
- The 2,097-row dimensions library is a convenience index of component bounds; it
  sits at tier 4 (component mechanics), never above a recipe, snap, or exception.
- A part's family-compatibility `SnapGroups` label in the part map is NOT proof of
  live-enrolled snap points. Live snap (tier 2) is read from the add-on; a part
  absent from the relational map is `free_computed_placement_not_snappable`.

## Live-verified status (5.00.00 build study)
A full live sweep confirmed the split this authority order assumes: 955 parts live
snap-enrolled, 1127 non-snap (`free_computed_placement_not_snappable`); usable
non-snap geometry agreed with the verified part map to <=0.01u; and a set of parts
spawns as null placeholders (see `data/NEGATIVE_KNOWLEDGE_INDEX.json`). Findings:
`reports/NONSNAP_PLACEMENT_STUDY_5.00.00_FINDINGS.md`.


## Proof-of-use governance (absorbed from PLACEMENT_INTELLIGENCE_GOVERNANCE_PROTOCOL)
## Purpose

This protocol implements the scope item: generated builds must prove they used the best available placement knowledge. The AI may generate a build, but it may not certify its own rule compliance without machine-checkable evidence.

## Required source hierarchy

1. Exact JSON recipe / known feature recipe
2. Authoritative add-on snap / relational data
3. Validated assembly recipe
4. Verified part-map component mechanics
5. Part-specific placement maps / orientation overrides
6. Exception and prohibited-part index
7. Manual review fallback, only if explicitly allowed

## Required generated-build artifacts

Every build-generation script or submission must be able to emit or package:

- `templates/PLACEMENT_SESSION_RECEIPT_TEMPLATE.json`
- `templates/BUILD_PLACEMENT_SNAPSHOT_TEMPLATE.json`
- `templates/PLACEMENT_METHOD_SUMMARY_TEMPLATE.json`
- `templates/ASSEMBLY_CONFORMANCE_PLAN_TEMPLATE.json`
- `templates/PART_USAGE_MANIFEST_TEMPLATE.csv`
- `OPEN_TOPICS_LOG.md`

## Gate principle

A build cannot pass because objects were placed. A build passes only when every placement method used is allowed by the highest-priority available source, and every structural assembly has conformance evidence.

## Current implementation status

4.01.00 ships the infrastructure: schemas, templates, seed method authority table, placement precedence, negative knowledge index, and release-gate infrastructure check. The full external validator is intentionally deferred.


## Assembly supersedes component (absorbed from ASSEMBLY_CONTEXT_SUPERSEDES_COMPONENT_CONTEXT_RULE)
## Rule

Component placement validation never proves assembly validity.

## Rationale

A part can spawn, rotate, scale, and measure correctly while still being wrong in a connected assembly. The castle ramp failure is the representative case: `B_RAMP` had component data, but the approach stair/ramp assembly did not prove endpoint/rise/run continuity.

## Enforcement

For every structural or connected assembly, use the Method Authority Table and Assembly Conformance Plan. Component data from the verified part map may support a placement, but it cannot override recipe, snap, or assembly requirements.

## Examples

| ObjectID/context | Component knowledge | Required assembly authority |
|---|---|---|
| `B_RAMP` as walkable ramp | bbox/orientation known | `STAIR_RAMP_ENDPOINT_RECIPE` |
| `B_FLOOR` as bridge | grid behavior known | `BRIDGE_PATH_CONTINUITY` |
| `BASE_BUBPIPE` as pipe system | Blender data unreliable | `PIPE_CONTEXTUAL_CONNECTOR_VALIDATION` |
| `BILLBOARD` as facade sign | rx=0 override known | side/facade mapping review |
| wall pieces as megastructure shell | component verified | wall-shell grid-course conformance |
