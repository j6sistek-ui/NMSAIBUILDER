# Part Placement Map Schema — 2.07.02

## Status

**Mandatory storage target for reusable part-placement learning.**

When a study teaches how a part behaves, the result must not remain only in chat memory or a one-off report. The learned mapping must be written into the placement-map library so future requests can load it during bootstrap/router execution.

## Purpose

The placement map is the canonical answer to:

```text
How do I place this part, at this scale, in this local frame?
```

It converts source evidence into reusable build intelligence.

## Universal source inputs

For each part/family, the mapper should gather:

```text
JSON / source build:
- ObjectID
- Position / origin
- Up
- At
- Scale
- UserData / grouping / material
- repeated placements
- neighbor positions
- neighbor rotations

Python:
- object constructor mapping
- JSON-to-Python axis conventions
- scale handling
- material/ObjectID substitutions
- transform-preservation rules
- helper functions that generated or recreated the source

FBX / bounds:
- model path
- min/max bounds
- extents
- center/pivot offset
- likely contact dimensions
```

## Canonical local frame

For every placement:

```text
Up    = normalize(source.Up)
At    = normalize(source.At projected onto plane perpendicular to Up)
Right = normalize(Up × At)
Origin = source.Position
```

Local-to-world:

```text
world_position = Origin + Right*x + Up*y + At*z
```

World-to-local neighbor delta:

```text
delta = neighbor.Position - current.Position

local_delta = [
  dot(delta, Right),
  dot(delta, Up),
  dot(delta, At)
]
```

## Required partmap fields

A `*.partmap.json` file must include:

```text
schema
part_id
part_family
status
source_evidence
fbx_bounds
canonical_local_frame
scale_mapping
source_transform_invariants
neighbor_offset_clusters_local
rotation_delta_clusters
fitment_modes
construction_applications
failure_modes
allowed_variation_slots
forbidden_substitutions
validation
storage_receipt
```

## Required master sheet columns

`library/part_placement_maps/part_placement_master_sheet.csv` must include one row per mapped part/family with:

```text
part_id
part_family
status
primary_source
partmap_path
fbx_path
baseline_scale
extent_x
extent_y
extent_z
center_x
center_y
center_z
local_x_rule
local_y_rule
local_z_rule
neighbor_offset_summary
fitment_modes
validated_applications
validation_status
last_updated
```

## Status values

```text
DISCOVERED
DOCUMENTED
VALIDATED
DEPRECATED
```

`DISCOVERED` means extracted from source evidence but not yet proven on new geometry.

`DOCUMENTED` means stored in the partmap library and indexed.

`VALIDATED` means successfully applied to a new proof build and passed the relevant gate.

## Hard rule

A response may not claim durable learning unless the mapping is stored in:

```text
library/part_placement_maps/
```

and the storage receipt identifies the exact partmap and master-sheet row.

## Optional field: orientation_override

Parts with a validated per-part orientation exception (registered in `PART_ORIENTATION_OVERRIDES.md`) carry an `orientation_override` field, generated into the map from that registry. It records the native-geometry evidence and the placement rule (e.g. BILLBOARD: rx=0, no generic rx=90, rz by compass side). The override registry stays the curated source; the map entry is generated from it and drift-checked, so the exception follows the part wherever it is used.

## Provenance levels (required on every datum)

Every datum in a placement map or behavior signature carries one of three provenance levels, so a hypothesis never reads as authoritative:

- `OBSERVED_FACT` — directly measured (FBX extents/center; a measured lattice pitch such as TRIFLOOR pitch ~3.07916 or the ~30 deg At offset).
- `DERIVED_RULE` — inferred or hypothesized from observations, not yet proven (e.g. "neighbor placement propagates through local frames").
- `VALIDATED_RULE` — proven by a passing proof build (and, for placement, user sign-off).

A `DERIVED_RULE` must not be consumed as if it were `VALIDATED_RULE`. Promotion `DERIVED_RULE -> VALIDATED_RULE` happens only through the validation exercise. Bounds carry `OBSERVED_FACT`; an evidence-validated orientation override carries `VALIDATED_RULE`; an un-proven fitment model stays `DERIVED_RULE`.

## Validation traceability (on validated parts)

A part's `validation` block carries, and these stay null until the part is validated:

- `validated_with_algorithm` — the PART_DATA_MAPPING_ALGORITHM version used.
- `validated_date`.
- `validation_build` — the proof build that placed it map-only and passed.
- `validation_evidence` — screenshots / JSON / build-audit references.

Every `VALIDATED_RULE` is thus traceable to the algorithm version and proof that earned it; a validated part may need re-proof when the algorithm version advances.


---

## Extension — executable part profile fields

C_TRIFLOOR validation proved that bounds alone are not enough. A partmap entry may now include a `part_profile` block and a `master_placement_rule` block.

Recommended `part_profile` fields:

```json
{
  "origin_type": "visual_centroid_anchor | bottom_anchor | socket_anchor | off_center_pivot | unknown",
  "origin_offset_local": {"x": 0, "y": 0, "z": 0, "status": "validated|derived|unknown"},
  "default_orientation_state": "builder_default | source_derived | orientation_override | unknown",
  "default_orientation_direction": "description",
  "bottom_origin_type": "bottom-anchored | not-bottom-anchored | unknown",
  "center_origin_type": "center/centroid behavior",
  "local_axes": {
    "Up": "target normal * scale",
    "At": "phase-resolved reference direction",
    "Right": "normalize(Up cross At)"
  },
  "orientation_phase_rule": {
    "status": "VALIDATED|DERIVED|UNKNOWN",
    "phase_a_deg": null,
    "phase_b_deg": null,
    "rule": "part-specific phase behavior"
  },
  "scale_behavior": {
    "uniform_scale": "validated|derived|unknown",
    "nonuniform_scale": "validated|forbidden|unknown"
  }
}
```

Recommended `master_placement_rule` fields:

```json
{
  "algorithm": "PART_PLACEMENT_MASTER_ALGORITHM",
  "doc": "rules/PART_PLACEMENT_MASTER_ALGORITHM.md",
  "equation": "Position=target+Right*x+Up*y+At*z; Up=normal*scale; At=rotate(reference, Up, phase)",
  "reference_direction": "edge/neighbor/path/reference",
  "validated_scope": "single part or family"
}
```

These fields are optional for old seeded maps but required before a part can be treated as placement-validated for advanced geometry.

## schema expansion — executable part profiles

The part placement map must contain enough information to execute the universal placement doctrine:

```text
WORLD_POSITION =
    TARGET_POSITION
    + ORIGIN_OFFSET
    + SCALE_OFFSET
    + CONNECTION_OFFSET
```

In addition to existing required fields, partmaps and master-sheet rows should eventually expose these executable profile fields:

```text
DefaultOrientation
OriginType
ScaleBehavior
ConnectionType
PrimaryDimensions
ConnectivityRules
TransformOverrides
PivotOffsets
PhaseOffsets
KnownExceptions
ValidationStatus
UserAcceptanceStatus
EvidenceSources
LastValidationRevision
ValidationUnknowns
FamilyEquivalenceClassification
```

### OriginType enumeration

```text
CENTER
BOTTOM_CENTER
FRONT_FACE
BACK_FACE
EDGE
CUSTOM
UNKNOWN
```

### ScaleBehavior enumeration

```text
UNIFORM
NON_UNIFORM
SPECIAL
```

### ConnectionType enumeration

```text
SNAP
VISUAL
HYBRID
```

### Acceptance-status fields

Use `validation_status` for technical proof state and `user_acceptance_status` for user approval state. Do not conflate them.

Reference ladder:

```text
UNTESTED
SCRIPT_VALIDATED
BLENDER_VALIDATED
PENDING_USER_ACCEPTANCE
USER_ACCEPTED
USER_ACCEPTED_WITH_EXCEPTIONS
```

### Family equivalence

For family expansion, record one of:

```text
SAME_RULE
SAME_RULE_WITH_SCALE_COEFFICIENT
SAME_RULE_WITH_PHASE_OFFSET
SAME_RULE_WITH_PIVOT_OFFSET
MODIFIED_RULE
UNIQUE_OUTLIER
FAIL
```

### Required caveat

A part may have strong Blender proof and still remain `PENDING_USER_ACCEPTANCE` until user review is explicitly recorded.


## Usage and validation (preserve SNAP_VALIDATED/GOLD tiers) (absorbed from PART_PLACEMENT_MAP_USAGE_AND_VALIDATION_RULE)
## Authoritative snap placement advances the accuracy dial

For parts in an add-on snap group, placement geometry is sourced from the authoritative add-on snap map
(`AUTHORITATIVE_SNAP_PLACEMENT_PROTOCOL.md`) and is SNAP_VALIDATED (matches the add-on's live snaps to 0.0
gap; composition formula validated to 0.0 pos / 0.0 deg). For these parts the per-part, map-only proof build
is no longer required to trust placement GEOMETRY — the authoritative source replaces re-derivation. The
"behave the old way / multi-source search" default below now applies only to parts NOT in a snap group.
Unchanged: status is confidence not a filter; the creative/behavior lane stays always-on; GOLD tier remains
GAME_VALIDATED (snap-validated is not game-validated); user signoff still governs aesthetic "masterful".

Single source for HOW the part placement map is consulted and how a part becomes
validated. Companion to `PART_PLACEMENT_MAP_SCHEMA.md` (what a map entry contains) and
`PART_PLACEMENT_MAP_SCHEMA.md` (when storage is mandatory). This rule is the
behavioral half: it makes the map actually change how builds are produced and checked.

## Two lanes — only one is cacheable

- **Placement geometry** (how a part seats, mates, connects): if the part is `validated`
  in the map, use the map and stop re-deriving its placement from scattered sources. If it
  is not validated, use whatever the map already holds as best-known starting info and fall
  back to the normal multi-source search. The default for anything not validated is to behave
  the old way.
- **Creative potential / technique** (what you can *do* with a part): always consult the
  recipes and `PART_USE_CASE_CATALOG`, on every build, regardless of map state. The map never
  replaces this lane and never caches it away. The efficiency win is only "don't re-measure the
  same geometry"; it is never "skip ideas."

## Validation is per part, earned, and signed off

- Validation is a verdict on the **whole part**, never a single cell. A part is `validated`
  only when the map alone places it masterfully — operationally, a proof build that placed the
  part using only the map (no fallback) came out right.
- For now, flipping a part to `validated` requires the **user's explicit agreement**: the gate
  proves the map-only build is connected and rule-compliant, but "masterful" is partly aesthetic.
  This may relax toward algorithm-automated validation once the mapping algorithm earns
  confidence (the accuracy dial below).
- Validation is never minted by transferring source data in. Seeded data is a hypothesis; the
  validation exercise tests and corrects it. "Source data went in" never means "it helped."

## Part status lifecycle

`EMPTY` → `SEEDED` (best-known-info loaded, usable, not validated) → `VALIDATED`. Bounds
backfilled from the dimensions library land a part at `SEEDED` /
`bounds_validated_placement_unmapped`: its bounds are validated truth, its placement is not.

## Status is confidence, never a filter

The map never restricts builds to validated parts and never down-ranks a part for being
unvalidated. Every part stays equally available. Validation status only tells the builder (and
the user) how much to trust the map's placement for that part.

## Accountability: per-build report

After a build's Python is generated, `run_gate` emits a part-placement-map coverage section
listing the parts the build used and their validation status (validated / not-yet-validated /
not-in-map). This is **informational and never fails the gate** — using best-known-info is
allowed. It serves as the user's backlog and as the first place to look when a build comes out
wrong ("these were not validated — likely suspects"). The builder may also suggest validating a
part that causes repeated trouble; validation is prioritized by real pain, not up front.

## Algorithm-accuracy dial

The mapping algorithm is not yet validated, so every `validated` verdict is provisional and is
stamped with the algorithm version. While the algorithm is immature, even validated parts are
re-checked; as it proves out, validated parts are trusted and the redundant searching drops away.
A validated part may need re-proof when the algorithm version advances.

## Known exception (future no-float refinement)

Outdoor flora — trees, plants, rocks — rest on terrain, so they are grounded but touch no other
placed part, and would false-positive in the no-float gate. When first encountered, exempt a part
that is either touching another part **or** ground-supported (a flora/tree/rock type by its
library category, base near the ground plane). Exempt flora is listed under a "terrain-grounded"
notice, not silently skipped. See `DISCONNECTED_ASSEMBLY_HARDSTOP_RULE.md`.

## Per-part exceptions

Validated per-part orientation exceptions (e.g. BILLBOARD's rx=0 rule) are carried from `PART_ORIENTATION_OVERRIDES.md` into the part's map entry as an `orientation_override`, so resolving a part's placement from the map surfaces its exception. The override registry remains the curated source; map entries are generated and drift-checked.

## Two knowledge layers: placement map vs behavior signature

These are distinct layers and must not be merged:

- PART PLACEMENT MAP — answers "how does this part physically fit?" (local frame, neighbor offsets, scale mapping, fitment, orientation overrides). Geometry; cacheable and validatable per part.
- PART BEHAVIOR SIGNATURE — answers "how is this part commonly used?" (silhouette roles, faceted shells, decorative lattices, polyhedra, known successful recipes). Lives in `PART_PLACEMENT_MAP_SCHEMA.md` and `PART_USE_CASE_CATALOG`; this is the always-on creative lane, not cached or replaced by the map.

A part can sit at different states in each layer independently. TRIFLOOR today: placement map SEEDED, behavior signature DISCOVERED, fitment rule a HYPOTHESIS (`DERIVED_RULE`), validation NOT COMPLETE.


## Storage compliance (absorbed from PARTMAP_STORAGE_COMPLIANCE_PROTOCOL)
## Status

**Mandatory gate for `PART_BEHAVIOR_LEARNING`, `RULE_DISCOVERY_AND_PROOF`, and JSON-derived style-transfer requests.**

## Purpose

Prevents temporary awareness from being mistaken for durable project knowledge.

## Rule

When a learned behavior, fitment rule, local-frame mapping, or part-use pattern is discovered, it must be stored in the placement-map library before the response can claim the learning is documented.

## Required storage locations

```text
library/part_placement_maps/<PART_OR_FAMILY>.partmap.json
library/part_placement_maps/part_placement_map_index.json
library/part_placement_maps/part_placement_master_sheet.csv
```

Reports may also be stored, but reports alone are not sufficient.

## Required receipt

Every relevant response or report must include:

```text
PARTMAP STORAGE RECEIPT
part_id:
partmap_path:
index_path:
master_sheet_path:
status:
source_evidence:
validation:
missing_items:
```

## PASS rule

For these request types:

```text
PART_BEHAVIOR_LEARNING
RULE_DISCOVERY_AND_PROOF
CONTROL_TO_VARIANT with learned fitment behavior
```

`PASS` requires one of:

```text
- existing partmap loaded and cited in the trace
- new/updated partmap written and storage check passed
```

If neither occurs, the gate is:

```text
blocked
```

## Soft override prevention

The following are not valid substitutes for storage:

```text
- saying "I learned"
- writing only a chat summary
- writing only a markdown report
- generating a proof build without updating the map
- using global angle assumptions instead of local-frame mappings
```

## Required validation script

Use:

```text
validation/partmap_storage_check.py
```

to confirm the partmap index, master sheet, and JSON partmap are present and parseable.


## Fallback derivation algorithm (preserve ~919 non-snap fallback) (absorbed from PART_DATA_MAPPING_ALGORITHM)
## Authoritative snap source supersedes derived adjacency (snap-group parts)

For any part in an add-on snap group, placement geometry is now READ from the authoritative add-on snap data
(see `AUTHORITATIVE_SNAP_PLACEMENT_PROTOCOL.md`), not derived from observed adjacency. The core equation
below remains valid but is now the FALLBACK lane for parts with NO snap group (~919 parts: decor/special
types). Provenance order: AUTHORITATIVE_ADDON_SNAP > DERIVED_ADJACENCY (this doc) > HEURISTIC. Do not
re-derive a join from adjacency clustering when the authoritative map covers the part.

## Status

**Mandatory for part behavior learning, rule discovery, and control-to-variant studies.**

## Core equation

```text
JSON placement data
+ Python conversion logic
+ FBX / bounds geometry
+ repeated successful adjacency
= PART_PLACEMENT_MAP
```

## Method

### 1. Load sources

Load the relevant working JSON/Python/control build and the FBX/bounds library.

### 2. Compute local frames from source transforms

For every observed placement compute:

```text
Up = normalize(JSON.Up)
At = normalize(JSON.At projected perpendicular to Up)
Right = normalize(Up × At)
Origin = JSON.Position
Scale = JSON scale, or source default if omitted
```

This must be computed from the source data. Do not replace it with generic global-angle assumptions.

### 3. Cross-check FBX/bounds

For the ObjectID/family, record:

```text
FBX path
bounds min/max
extents
center/pivot offset
baseline contact dimensions
```

Use this to interpret whether observed neighbor offsets are plausible contact, overlap, shell, lattice, decorative, or support relationships.

### 4. Derive local neighbor rules

For each likely neighboring placement:

```text
world_delta = neighbor.Position - current.Position

local_delta = [
  dot(world_delta, Right),
  dot(world_delta, Up),
  dot(world_delta, At)
]
```

Also compute rotation/frame deltas:

```text
neighbor Up/At/Right relative to current Up/At/Right
```

Cluster repeated local deltas and rotation deltas. These clusters are the reusable fitment candidates.

### 5. Separate source-space observations from portable rules

Global angles may be useful evidence but are not universal rules. Store portable rules in local-frame terms:

```text
neighbor_position = current_origin
                  + Right * dx
                  + Up    * dy
                  + At    * dz
```

### 6. Write storage artifacts

Every successful extraction must write:

```text
library/part_placement_maps/<PART>.partmap.json
library/part_placement_maps/part_placement_map_index.json
library/part_placement_maps/part_placement_master_sheet.csv
```

### 7. Verify storage

Run or manually complete the storage receipt:

```text
PARTMAP STORAGE RECEIPT
partmap written:
index updated:
master sheet row updated:
source files referenced:
status assigned:
unverified items:
```

### 8. Apply and validate

For proof builds, use the stored map first. Do not re-derive from memory if a partmap exists.

## Request-time compliance question

For part studies, the assistant must answer internally before generation:

```text
Did I load the existing part placement map, or create/update it if missing?
```

If the answer is no, the response cannot claim a protocol PASS.


---

## Master placement algorithm update

C_TRIFLOOR proved the general algorithm:

```text
part placement = target geometry + part profile
```

The target geometry supplies:

```text
Position target
Up / normal target
At reference direction
Scale
```

The part profile supplies:

```text
origin type
origin offset
default orientation
phase offset around Up
scale behavior
family equivalence status
```

Master placement equation:

```text
Up = normalize(target_normal) * scale

At = normalize(
  rotate_around_axis(
    project_perpendicular(target_reference_direction, normalize(target_normal)),
    normalize(target_normal),
    part_profile.orientation_phase_degrees
  )
)

Right = normalize(Up × At)

Position = target_anchor
         + Right * origin_offset_local.x * scale
         + Up    * origin_offset_local.y * scale
         + At    * origin_offset_local.z * scale
```

If the part has no validated phase, use a control matrix to solve it; do not guess. If the part has no validated origin behavior, use FBX center/bounds as observed evidence but require a proof build before promotion.

## Family expansion rule

Family validation is not inherited from similar names. Test each family candidate with:

```text
FBX equivalence
default orientation
origin/pivot behavior
uniform scale
phase rule
minimal proof build
```

Only then classify it as `same_rule`, `modified_rule`, `unique_outlier`, or `not_equivalent`.

## mapping update — offsets as reusable data

The mapping algorithm must now explicitly separate universal placement logic from part-specific data.

Universal logic:

```text
target frame + part profile -> Position / Up / At / Scale
```

Part-specific data:

```text
origin offset
scale offset/behavior
connection offset
default orientation
phase/pivot offsets
snap/contact semantics
family equivalence class
known exceptions
```

### Offset decomposition

When deriving a placement rule, map successful source evidence into:

```text
TARGET_POSITION
ORIGIN_OFFSET
SCALE_OFFSET
CONNECTION_OFFSET
```

Then store the result in the part profile. Do not encode it as a one-off placement formula when it is actually reusable part behavior.

### Local-frame adjacency extraction

Repeated part chains must be stored in local-frame terms:

```text
neighbor_position =
    current_position
    + Right * dx
    + Up    * dy
    + At    * dz
```

For stair/ramp chains, the validated specialization is:

```text
Position[n+1] =
    Position[n]
    + At * RUN_STEP
    + Up * RISE_STEP
```

### ValidationUnknowns

Every mapping study should begin with a `ValidationUnknowns` list. This avoids retesting the whole engine when only default orientation, origin type, or connectivity is unknown.
