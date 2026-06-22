# JSON → Python Recreation Protocol v53

Status: **validated on current 249-object sample and 1,237-object multi-location / multi-axis validation sample**.

This protocol applies when the user provides exported No Man's Sky base JSON and asks for a Python recreation, repair, enhancement, or round-trip workflow.

## Core purpose

The converter must reproduce an existing NMS base through Python by using the exported JSON as the source-of-truth placement ledger.

```text
exported NMS base JSON
→ parse ObjectID / Position / Up / At / UserData / extra fields
→ create real NMS objects through the Base Builder plugin
→ apply validated transform mapping
→ duplicate/modify through Python
```

This enables existing-build repair and enhancement without manually editing JSON.

## Validated source schema

The tested JSON path uses object records with:

```json
{
  "ObjectID": "^M_FLOOR",
  "Position": [x, y, z],
  "Up": [x, y, z],
  "At": [x, y, z],
  "Timestamp": 1772861503,
  "UserData": 2
}
```

Some objects include extra state, such as:

```json
{
  "ObjectID": "^BYTEBEAT",
  "Message": "..."
}
```

The converter must preserve extra fields on recreated objects as custom properties where practical.

## Validated transform stack

For this JSON export/import path, the validated transform is:

```python
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
```

Equivalent conceptual order:

```text
1. strip caret from ObjectID for builder call
2. convert source vectors:
   source [x, y, z] → Blender (x, -z, y)
3. build local axes from converted Up/At:
   right = at.cross(up) or the equivalent RIGHT_AT_UP basis used in the validated converter
4. apply builder/native base correction:
   POST_RX90
5. apply universal post-baseline local Y-axis 180
6. use uniform scale from source Up-vector length unless a future validated case proves otherwise
```

Do **not** omit the final local Y 180. It fixed subtle local orientation errors that square wall/floor geometry can hide.

## Validation history

### V06/V07

Validated global placement and structural overlay for the first 25 objects, then the full 249-object sample. The initial failure mode looked like correct local shape but wrong side of a global axis. The fix was the validated `XnZY` mapping.

### V08–V13

Attempted family-specific fixes for furniture, decals, billboard, shelves, wall-mounted props, and counter objects. These tests identified real family differences but were ultimately superseded by the broader V14 result.

Intermediate observations remain useful as diagnostics:

- Decals are thin wall-art planes and can appear correctly placed but upside down.
- `BILLBOARD` is a planar sign exception.
- Wall-mounted props and shelves can expose local-basis failures.
- A candidate that fixes one part family can pitch another family incorrectly.

### V14

The full 249-object original-location overlay looked visually perfect using the broad post-baseline `LOCAL_Y_180` correction. This fixed structure, walls, floors, table props, decals, billboards, shelves, wall-mounted props, curtains, furniture, and counter props in that sample.

### V15

The same mapping was validated on a 1,237-object JSON where the base was copied into several different locations/orientations across axes. User review confirmed every location and axis was handled correctly.

## Validated ObjectIDs in sample set

The validated 1,237-object test included these major families/ObjectIDs:

```text
M_FLOOR, M_GFLOOR, M_WALL, M_ROOF, M_WALL_WINDOW, M_DOOR,
T_WALL_Q_H1, BUILDWORKTOP, BUILDSOFA2, BILLBOARD, BUILDDECALSIMP4,
DECAL_WORM_P*, EXPD_DECAL*, BLDWALLUNIT, BUILDFLATPANEL,
SERVERSTACK, WEAPONRACK, S_TRAY0, S_CUP0, S_BAR, S_BAR_H, S_BAR_C,
S_BARTAPS0, S_PAN0, S_TABLEPOT0, S_CURTAIN0, S16_HEATER,
BYTEBEAT, BASE_CAVE3, BASE_BARNACLE, BASE_TERRARIUM, BASE_NEXUS2,
BASE_TOYCUBE, PLANTTUBE, PLANTPOT4, WALLLIGHTRED, TELEPORTER,
DRESSING_TABLE, CONTAINER0, COOKER, FOS_SKULL, SPAWNER_BALL,
BLD_PLANET_HOLO, B_WATERTOWER, BUILDSAVE, AM_WEAPONTREE, S_SIGN_BAR3.
```

This is not proof that every NMS object family is solved. It is proof that this transform path is robust for the tested architectural/interior/decal/billboard/wall-prop families.

## Required converter behavior

### 1. Builder preflight before cleanup

Before deleting or generating anything:

```python
verify active scene has initialized NMS Builder/base context
verify bpy.context.scene.nmsdk_builder exists or equivalent builder resolver succeeds
verify add_part is callable
fail before deletion if missing
```

### 2. Real NMS parts only

Use `BUILDER.add_part(ObjectID)` or a verified builder-created template. Do not use Blender mesh proxies, cubes, or FBX imports as deliverables.

### 3. Template duplication

Create one hidden builder-created template per ObjectID, then duplicate hierarchy for every source object. Preserve custom properties.

### 4. Preserve source state

Store at least:

```text
SourceIndex
SourceObjectID
ObjectID
UserData
Timestamp
Message / extra fields when present
ValidatedCoordMode
ValidatedAxisMode
ValidatedBaseRotationMode
ValidatedPostCorrection
```

### 5. Skip only known non-build placeholders by default

Default skip set:

```python
SKIP_OBJECT_IDS = {"BASE_FLAG", "U_PARAGON"}
```

Do not skip ordinary parts silently.

### 6. Audit every run

Print and/or write a diagnostic report with:

```text
source object count
generated object count
unique ObjectID counts
missing ObjectIDs
skipped ObjectIDs
non-unit scale records
extra-field records
validated transform settings
unknown/high-risk ObjectIDs
```

### 7. Unknown family policy

For future bases with new ObjectIDs not in the validation set:

- do not assume they are broken;
- recreate them with the validated global transform + local Y 180 first;
- flag them in the audit as **new/unvalidated ObjectID**;
- validate visually;
- if wrong, create a focused family/object test, not broad random rotations.

## Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Structure is correct shape but across wrong axis | coordinate conversion/mirror error | use `COORD_MODE="XnZY"` for this path |
| Structure overlays but decals/billboards are upside down | local template basis not corrected | apply post-baseline `LOCAL_Y_180` |
| V08-style prop candidates pitch furniture vertical | wrong basis-family correction | do not use broad RX/RXNEG family guesses |
| Offset copies differ from original | correction is origin-dependent | transform was not truly local/global stable; retest |
| Missing template | ObjectID not available in plugin/runtime | report; do not substitute silently |
| Non-uniform scale appears | source may encode scale in Up/At | preserve source scale for recreation; flag for review before editing |

## Promotion status

This is a **validated method for the current JSON intake path and tested object set**.

It may be promoted as the default JSON→Python recreation baseline, with a caveat:

```text
Use validated transform by default.
Audit and visually confirm new/unseen ObjectID families before locking them.
```

Do not claim this solves all possible future object families until they are tested.



## mandatory mapping declaration

Any JSON-informed generator, recreation, repair, or placement study must declare the validated transform stack in code and provenance:

```python
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
```

Use `rules/JSON_EVIDENCE_MAPPING_GATE.md` whenever JSON is provided. Do not fall back to generic `rx/rz` orientation logic while JSON control data exists.


## context boundary

This transform stack is for JSON→Python/Blender recreation of existing exported base JSON. It must not be blindly applied to direct Blender-space procedural generators.

For direct Python generators, use exported JSON after generation as a reverse audit: Blender/Python `(x,y,z)` serializes as JSON `Position=[x,z,-y]` for the validated path, and JSON `Up`/`At` vectors are the authoritative serialized orientation and scale evidence.

When source JSON is high quality, mine it as recipe evidence before generating new code: ObjectID clusters, basis vectors, deltas, anchors, scale vector lengths, UserData, and module envelopes.


## JSON study extraction stage (absorbed from JSON_STUDY_PLACEMENT_RECIPE_PROTOCOL)
Status: **active required process** for No Man's Sky base-building work.

This protocol extends the v53 JSON→Python recreation breakthrough. v53 solved the coordinate/orientation language for exported base JSON. v54 defines how to use that capability to extract reusable placement knowledge, part-family behavior, spacing, scale, and feature recipes from real bases.

## Core principle

```text
JSON = geometry truth
Blender screenshot = placement/overlay review
In-game screenshot = visual truth
```

A JSON study is not just a part-count audit. It must answer:

```text
What parts were used?
Why were they used?
How were they spaced?
How were they scaled?
How were they oriented?
What feature did the cluster create?
Is the result worth reusing?
What should not be copied?
```

## Required JSON study sections

Every future JSON study must include:

1. **Source overview**
   - base name;
   - base type;
   - object count;
   - unique ObjectID count;
   - notable screenshots/in-game context if provided.

2. **ObjectID frequency and role**
   - top repeated ObjectIDs;
   - apparent functional role for each major part;
   - whether the role is default, recontextualized, or project-specific.

3. **Scale distribution**
   - per-ObjectID Up-vector scale range;
   - median/common rounded scales;
   - note non-unit scale patterns.

4. **Spacing / Connection / Scale Findings**
   - nearest-neighbor spacing for repeated parts;
   - horizontal run spacing vs vertical stack spacing;
   - chord/radius/angle spacing for circular or curved systems;
   - ramp/stair endpoint data when relevant.

5. **Feature/module envelopes**
   - bounding boxes or local coordinate frames for major clusters;
   - ObjectIDs used in each module;
   - inferred module recipe.

6. **Failure-prone subsystem extraction**
   - stairs/ramps;
   - wall and trim runs;
   - floors and quarter floors;
   - shelves/interior props;
   - vehicles;
   - powerline/logic networks;
   - display walls/screens;
   - doors/airlocks/portals.

7. **Reusable module recipes**
   - concise recipe name;
   - part list;
   - geometry basis;
   - spacing/scale/orientation rules;
   - where to reuse.

8. **Negative lessons / exclusions**
   - what worked only contextually;
   - what should not be promoted;
   - weak composition to avoid.

9. **Master-doc update candidates**
   - universal rules;
   - part-family rules;
   - toolkit techniques;
   - project-specific observations.

## Required spacing extraction

For every repeated family that could drive generated builds, calculate or manually record:

```text
ObjectID
count
scale range
nearest horizontal spacing
nearest vertical delta
common rounded spacings
same-position duplicate groups
module bounding box
role / feature
```

### Special handling

- **Floors:** separate full floor, quarter floor, triangle floor, and glass/freighter/basic/concrete/stone/timber families.
- **Walls:** separate straight runs, stacked rows, diagonal pieces, short walls, windows, and trim.
- **Rings/arcs:** extract center, radius, angle step, chord length, overlap tolerance, and depth layer.
- **Stairs/ramps:** extract start landing, end landing, path vector, module count, rise/run, contact overlap.
- **Vehicles/assemblies:** extract local coordinate frame, subpart roles, axle/body/rail/rod spacing.
- **Powerlines:** preserve same-position powerlines if vectors differ; they may be hub-and-spoke logic, not duplicates.
- **Organic scatter:** identify zones and scale bands rather than global random scatter.

## Promotion categories

Classify each finding conservatively.

| Category | Meaning |
|---|---|
| Universal rule | Applies broadly unless explicitly suspended |
| Part-family rule | Applies to a known family, such as short walls or floor modules |
| Toolkit technique | Reusable but context-dependent construction method |
| Project observation | Useful for one theme/project but not general |
| Negative lesson | Explicit thing not to copy or promote |

## JSON vs screenshots

### Use JSON for

- exact placement;
- orientation;
- scale;
- ObjectID/UserData;
- repeat spacing;
- connection relationships;
- reproducible Python generation;
- extracting construction grammar.

### Use screenshots for

- visual read;
- silhouette;
- lighting/effects;
- occlusion;
- terrain fit;
- in-game shader/render behavior;
- whether the result is aesthetically strong.

## Direct JSON vs Python

Python remains the preferred authoring/generation format.

```text
Existing base repair/enhancement:
  exported JSON → validated Python recreation → modify in Python → inspect/export

Fresh build generation:
  Python generator → Blender validation → in-game validation

JSON study:
  exported JSON + screenshots → extract recipes → update library/toolkit
```

Direct JSON can be accurate only when produced through the validated transform path. Hand-authored JSON remains high-risk compared with procedural Python.

## Required memory-retention strategy

Important NMS lessons should be stored in three places:

1. persistent memory when available;
2. master docs / recipe library;
3. transfer prompt / bootstrap files.

Do not rely on chat memory alone. The master docs must be the long-term source of truth.

## v56 recipe parameterization clarification

JSON study data is geometry truth for the studied source build, but it is not automatically the only best practice.

Every extracted recipe must separate:

```text
baseline/control geometry
from
variable design parameters
```

Parameters such as ObjectID variant, material, scale, radius, count/density, depth, and use case can change by design goal.

Use JSON precedent with:
- FBX bounds;
- part-family behavior;
- visual validation;
- project intent.

Do not blindly copy a JSON recipe when a different scale, density, or part variant better serves the design.



## JSON control recipe requirement

When a JSON study already contains a working instance of a subsystem, that subsystem is a control recipe. A new generator must first reproduce its ObjectIDs, local coordinate frame, Position deltas, Up/At basis vectors, and scale distribution before attempting design variations.

This is mandatory for failure-prone systems: stairs/ramps, airlocks/iris doors, vehicles, rings/arcs, connected wall curvature, and interior machinery modules. Visual approximation is not acceptable when JSON geometry exists.


## mandatory working-JSON-first update

Working JSON is now a foundational source tier. Before a generator creates or repairs a subsystem, it must check whether the source package or user has already provided working JSON evidence for the same part, assembly pattern, or design problem.

If a relevant working JSON recipe exists, the generator must use it as the control baseline:

1. reproduce the ObjectID set and local coordinate frame;
2. reproduce Position deltas and Up/At basis behavior;
3. reproduce serialized scale distributions where valid;
4. identify physical anchors and module envelopes;
5. only then adjust count, scale, spacing, material, or part variants using FBX bounds and design intent.

FBX geometry tells what a part is; working JSON tells how the part successfully behaved in a real Builder/save context. Both are required for robust procedural generation.


## JSON geometry intelligence stage (absorbed from JSON_GEOMETRY_INTELLIGENCE_PROTOCOL)
Status: mandatory when JSON is provided for learning, reuse, repair, exact recreation, or variant generation.

## Purpose

Working JSON should not be reduced to "part placement data." It must be mined into reusable geometry intelligence: how parts connect, how a feature closes gaps, how a local frame scales, and how a concept can be recreated elsewhere.

Exact JSON recreation proved that exported base JSON can be transformed into Python accurately. This protocol makes the next step explicit: turn that exact control into reusable, adaptable geometry.

## Required extraction levels

### 1. Literal transform ledger

Record:

```text
ObjectID
Position
Up
At
UserData/material
scale vector lengths
extra fields
source index / object order when useful
```

This is the exact recreation layer.

### 2. Part-role ledger

For each cluster or subsystem, label part roles:

```text
stair tread / landing / support
wall bay / corner / cap / trim
ring blade / fill panel / frame / depth layer
dome latitude ring / rib / cap / oculus
vehicle wheel / axle / body / cabin / lights
foundation / load path / underside support
```

### 3. Relationship ledger

Record why the geometry works:

```text
anchor-to-anchor relationship
nearest-neighbor spacing
endpoint closure
overlap/contact tolerance
ring radius / chord / angle step
height/radius/profile table
local X/Y/Z frame vectors
scale basis and allowed scaling direction
orientation basis and tangent/normal/up logic
```

### 4. Adaptation ledger

Record how to reuse it:

```text
locked invariants
allowed parameters
safe ranges if known
compatible ObjectID families if known
validation required before promotion
failure modes and negative lessons
```

## Required outputs from a JSON learning pass

A JSON learning pass should produce or update:

```text
toolkit/PLACEMENT_RECIPE_LIBRARY.json
data/JSON_RECIPE_SIGNATURE_INDEX.json
rules/PART_USE_CASE_CATALOG.md/json when new part behavior is learned
rules/SPACING_CONNECTION_SCALE_RULES.md when a general connection rule is learned
rules/CONNECTED_PIECE_CURVATURE_GRAMMAR.md when the feature is curve/shell/profile based
```

## Stairs and ramps

A working stair/ramp JSON must be converted into endpoint math, not memorized as loose placements.

Required fields:

```text
start landing anchor
end landing anchor
path vector
yaw from path
rise/run
segment count
center-to-center step
first/last contact condition
support/foundation condition
```

A future scaled variant must recompute count and spacing from endpoints and selected part bounds while preserving contact.

## Domes, curves, shells, and spires

A working dome/curve JSON must be converted into a profile/ring/path recipe.

Required fields:

```text
local centerline or surface frame
ring/layer index
height per layer
radius per layer
segment count per ring
angle step
chord spacing
part tangent orientation
vertical layer spacing
overlap/contact condition
cap/oculus/apex condition
```

A future variant must scale the profile or regenerate the profile table, not scatter pieces by visual angle guessing.

## Local-frame assemblies

Vehicles, machines, furniture, airlocks, façade modules, and complex props must be stored as local-frame assemblies:

```text
origin
local axes
anchor points
part roles
relative deltas
allowed uniform scale
orientation transform as a unit
```

Move/rotate/scale the frame, not each object independently by guess.

## Missing-data rule

If a prior JSON-derived feature cannot be found in the recipe library, signature index, reports, or source package, state that the data is not retained in executable form and request the original JSON again. Do not claim the system can reuse a recipe whose invariants are missing.


## Control recipe learning / part behavior model

When valid source JSON exists, assume the recipe already contains a working solution. The goal is not only to recreate placements, but to infer the part behavior model that made the placements work.

Add extraction level 5:

### 5. Part behavior signature

Record:

```text
part family
locked dimensions or scale policy
Position/Up/At coupling
neighbor/contact spacing
mating transforms
orientation cycle
density/fill rule
pivot or offset evidence
construction style
allowed variation slots
forbidden substitutions
knowledge maturity: DISCOVERED / DOCUMENTED / VALIDATED
```

For triangle-derived surface studies, ObjectID may change across verified compatible triangle families, but source-relative Position, Up, and At must be preserved together. If same-style solid surfaces are requested, preserve source triangle size and increase registered triangle count rather than scaling panels or substituting sparse lattice behavior.


## JSON feature-concept extraction stage (absorbed from JSON_FEATURE_CONCEPT_EXTRACTION_PROTOCOL)
Status: **mandatory when user provides working JSON for review, mining, replication, or future feature reuse**

## Purpose

The JSON→Python breakthrough proved that exported No Man's Sky base JSON can be used as geometry truth. This protocol closes the next gap: using working JSON not only as an exact control, but as a source for reusable **feature grammar**.

When the user provides a JSON file, the reviewer must not stop at exact recreation. The reviewer must also extract what feature or architecture concept the JSON proves, how it works, and how to generate variants later.

This applies even when the user does not explicitly ask for a toolkit update.

## Required request routing

Before analyzing a JSON file, load/check these protocol locations:

```text
00_START_HERE_CURRENT.md
00_KICKOFF_INTAKE_GATE.md
rules/REQUEST_ROUTER_CHECKLIST.md
rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md
rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md
rules/WORKING_JSON_FIRST_PRINCIPLE.md
rules/JSON_EVIDENCE_MAPPING_GATE.md
rules/SPACING_CONNECTION_SCALE_RULES.md
toolkit/PLACEMENT_RECIPE_LIBRARY.md
```

When the JSON contains an airlock / iris / vault / portal feature, also load/check:

```text
rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md
rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md
toolkit/AIRLOCK_IRIS_PARAMETRIC_GENERATOR_SKELETON.py
```

## Required classification

For each JSON input, classify the use mode:

| Mode | Meaning |
|---|---|
| `JSON_RECREATION_CONTROL` | Recreate the exact source objects and validate transform fidelity |
| `JSON_FEATURE_RECIPE_EXTRACTION` | Extract a reusable concept/feature recipe from working JSON |
| `JSON_PARAMETRIC_VARIANT_DERIVATION` | Convert a proven control into a generator for N-sided / scaled / material-swapped variants |
| `PYTHON_GENERATED_JSON_AUDIT` | Export generated Python build to JSON and compare serialized truth |
| `NEGATIVE_OR_CONTEXTUAL_OBSERVATION` | Identify what worked only contextually and must not be promoted |

A single JSON can have multiple modes.

## Required extraction layers

### 1. Exact control layer

Record the literal control data:

```text
base name / module name
source file
source hash if available
ObjectID counts
SourceIndex list
Position / Up / At / UserData preserved
first-object fingerprint for critical families
known skipped placeholders
```

Exact control recreation must never infer or simplify `Position`, `Up`, or `At`.

### 2. Concept layer

Name the feature concept and classify the geometry primitive:

| Primitive | Examples |
|---|---|
| radial aperture | airlock / iris / portal |
| chord ring / arc | trim ring, dome band, short-wall circle |
| dome shell | Taj dome, roof shell, sphere-like hull |
| path assembly | stairs, ramps, pipes, railings, skybridges |
| grid assembly | floors, display walls, archive shelves |
| local object assembly | vehicles, foosball tables, machinery |
| layered façade | lab observation wall, skull façade marker |
| organic scatter | jungle/terrain/plant zones |

### 3. Feature frame layer

Extract or define a local coordinate frame:

```text
center / anchor
normal axis
tangent axis
binormal/up axis
depth direction
origin relative to source cluster
```

All variant generation must work in this local feature frame first, then transform into the target build.

### 4. Layer table

For every part family in the feature, record:

```text
ObjectID
role
count rule
base scale
radius / path distance / grid spacing / depth offset
angular offset or row/column offset
material/UserData
connectivity expectation
fallback/substitution family if known
```

### 5. Parametric rule layer

Convert the control into a generator contract:

```text
required inputs
valid ranges
which values can be changed
which values must be preserved
formulas
validation checks
known failure modes
```

### 6. Variant policy

State how variants may be generated:

```text
same ObjectID family
same concept with different material
same concept with related part family
different side count
different radius
different scale
different decorative layer count
```

If the requested variant is outside the control's proven geometry, the script must say so and add validation.

### 7. Negative/pitfall layer

Record what must not be copied.

## Exact control vs parametric recipe

```text
Exact control:
  Use the source objects literally.

Parametric recipe:
  Derive a local feature frame and transform Position, Up, and At together.
```

A script is not allowed to call itself an “exact known-good JSON recipe” if it regenerated, simplified, normalized, or hand-authored any source `Position`, `Up`, or `At`.

## Required variant-generation rule

For any ring, airlock, dome, spire, arc, or rotated assembly:

```text
Position, Up, and At must be transformed together.
```

Do not rotate only positions.

## Required JSON study output

Every JSON study should add or update:

```text
archive/json_studies/<study>.md
toolkit/PLACEMENT_RECIPE_LIBRARY.md
toolkit/PLACEMENT_RECIPE_LIBRARY.json
rules/PART_APPLICATION_NOTES*.csv or json
rules/SPACING_CONNECTION_SCALE_RULES.md when applicable
transfer/bootstrap prompt when critical
```

## Required protocol confirmation in every response

When this protocol is used, explicitly include a **Protocol confirmation** section with these fields:

```text
Request route:
Source files checked:
JSON exact control captured:
Feature concept extracted:
Local frame / layer table captured:
Parametric recipe captured:
Variant limits documented:
Negative lessons documented:
Next action:
```

Do not omit this section when a JSON is being reviewed for feature learning or when generating from a known JSON-derived feature.

## Ignored utility infrastructure
When extracting feature recipes from JSON, exclude power/logic utility parts from the core feature layer table unless explicitly requested.

Default ignored patterns:

```text
U_POWERLINE
POWERLINE_HIDER
U_SWITCH*
U_BATTERY*
U_SOLAR*
U_BIOGENERATOR
```

Record their counts in an ignored-utility section, then focus extraction on architecture/feature geometry.

## Connected-piece curvature extraction
When JSON shows repeated walls, short walls, floors, roof pieces, panels, trim, pipes, or cylinders forming a curved/rounded/tapered object, extract the broader connected-piece curvature grammar.

Do not restrict the finding to the exact feature label.

Examples:

```text
dome → stacked latitude shell / wall-tile curvature
cylindrical room → centerline + radial deck rings
spire → tapered convergence shell / rib grammar
Bumblebee body → connected panel hull
vehicle shell → local object hull
```

Required file:

```text
rules/CONNECTED_PIECE_CURVATURE_GRAMMAR.md
```

## Prompt routing gate dependency
Before using this protocol, first classify the prompt using:

```text
rules/REQUEST_ROUTER_CHECKLIST.md
```

Then state the selected JSON mode and applicable rule bundle in the response.

## geometry-intelligence reinforcement

When relevant JSON exists, exact recreation is not the end state. Apply `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md` to preserve the reusable logic: part roles, anchors, local frames, connection/contact relationships, locked invariants, allowed parameter slots, and missing evidence.

If a prior JSON-derived technique cannot be found in `toolkit/PLACEMENT_RECIPE_LIBRARY.json`, `data/JSON_RECIPE_SIGNATURE_INDEX.json`, reports, or the source package, do not claim the technique was retained. Request the source JSON again or mark the recipe provisional.
