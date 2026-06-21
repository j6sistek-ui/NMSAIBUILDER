
# Recipe Parameterization Protocol v56

## Status

**Universal process rule.**

This rule governs how extracted JSON recipes, screenshot/video-derived techniques, and placement studies should be used in future generated builds.

## Core principle

```text
JSON precedent is a control/reference, not a mandate.
```

JSON studies provide geometry truth for a specific source build, but they do not automatically define the only valid ObjectID, scale, density, radius, or use case.

A reusable recipe must separate:

```text
recipe concept
baseline/control geometry
variable parameters
validation requirements
design intent
```

## Why

A source JSON may show one effective implementation, but future builds may need:

- different scale;
- different material family;
- different ObjectID variant;
- different density/count;
- different radius;
- walk-through vs tiny aperture sizing;
- focal monument vs background detail;
- low-part-count vs high-detail version.

Blindly copying a JSON module can produce the wrong result even when the geometry is technically correct.

## Required recipe fields

Every placement recipe should identify:

| Field | Meaning |
|---|---|
| Concept | What the recipe creates |
| Baseline/control | Extracted or validated source example |
| Required geometry basis | Ring, grid, path, wall plane, local frame, etc. |
| Variable parameters | Count, radius, scale, ObjectID, material, density, depth |
| ObjectID families | Valid or candidate interchangeable families |
| Validation requirements | What must be checked before promotion |
| Design-use modes | Tiny, walk-through, monumental, decorative, high-density, low-density |

## Airlock / iris example

Baseline/control from JSON:

```text
S_GDOOR x12
B_FLOOR_Q x24
B_WALL_Q_H1 x12
F_WALLB_H x24
```

This is a proven/control recipe, not the only valid recipe.

Valid design variables include:

```text
ObjectID: any validated compatible *_GDOOR / garage-door family part
Panel count: 8, 12, 16, 24, 32, etc.
Scale: tiny aperture to walk-through portal
Radius: driven by desired opening and part dimensions
Material: stone, alloy, timber, concrete, etc.
Density: chunky hatch vs smooth iris
Use case: door, vault, reactor aperture, portal, decorative iris
```

## Decision rule

Use JSON precedent as the starting point when available. Then adapt using:

```text
design goal + FBX bounds + part-family behavior + visual validation
```

Never use JSON precedent alone.

## Documentation language

Use careful wording:

- “baseline/control recipe”
- “validated source implementation”
- “candidate variant”
- “parameterized adaptation”
- “requires orientation validation”

Avoid wording like:

- “must always use”
- “only valid ObjectID”
- “fixed count”
- “universal radius”
unless the user or repeated validation explicitly supports that hard rule.

## geometry-intelligence reinforcement

When relevant JSON exists, exact recreation is not the end state. Apply `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md` to preserve the reusable logic: part roles, anchors, local frames, connection/contact relationships, locked invariants, allowed parameter slots, and missing evidence.

If a prior JSON-derived technique cannot be found in `toolkit/PLACEMENT_RECIPE_LIBRARY.json`, `data/JSON_RECIPE_SIGNATURE_INDEX.json`, reports, or the source package, do not claim the technique was retained. Request the source JSON again or mark the recipe provisional.


## Control-to-variant derivation (absorbed from CONTROL_TO_VARIANT_PROTOCOL)
Status: mandatory when adapting a known JSON, recipe, or proven feature.

## Purpose

This protocol prevents the common failure where the AI can recreate a JSON control exactly, but fails when asked to make the same feature bigger, smaller, rotated, higher-count, different-material, or slightly stylistically different.

A control is not merely an example. It defines what must remain true for the feature to keep working.

## Trigger phrases

Use this protocol when the user asks for:

```text
same feature but different
make a variant
scale this
make it larger/smaller
make it 8/12/16/24-sided
reuse the stair/dome/curve/door concept
adapt this JSON
use the same construction logic elsewhere
```

## Required process

1. Identify the control source:
   - uploaded JSON;
   - JSON study;
   - recipe library entry;
   - recipe signature index entry;
   - prior validated generated build.

2. Extract or load the invariant set:
   - anchors;
   - local coordinate frame;
   - part roles;
   - connection/contact rules;
   - orientation basis;
   - scale basis;
   - ring/chord/endpoint/grid relationships.

3. Extract allowed variation slots:
   - count;
   - radius/run/height;
   - uniform scale;
   - material/UserData;
   - detail density;
   - compatible ObjectID family substitutions.

4. Derive placement mathematically from the control:
   - endpoint interpolation for stairs/ramps/paths;
   - chord and tangent math for rings/arcs;
   - profile tables for domes/spires/shells;
   - local-frame transforms for vehicles/furniture/modules;
   - row/column spacing for grids.

5. Run connection proof:
   - first/last segment contacts anchors;
   - repeated segments touch or overlap;
   - rings close;
   - shell layers align;
   - ramps/stairs meet landings;
   - no free-floating visual-only assemblies unless explicitly intended and supported.

## Forbidden shortcut

Do not treat a variant request as a new generic build when a known control exists. The control must be named in the placement plan or provenance manifest.

## Missing-control rule

If no usable control/recipe/signature is retained, ask the user for the JSON again, especially for prior submissions involving stairs, ramps, domes, curvature, airlocks, vehicles, or any feature where connection math was already proven.


## Behavior-transfer hardening

When adapting a known JSON, recipe, or proven feature, first decide whether the user is asking for generic geometry variation or behavior transfer.

If the user asks for the same style, same method, observed data, study reuse, or placement behavior, route through `SELECTIVE_VISUAL_MEMORY_POLICY` and `SYSTEMATIC_FAILURE_CAPA_PROTOCOL`.

Required additional ledgers:

```text
Locked objectives ledger
Forbidden substitutions ledger
Part behavior signature
Proof application ledger
Failure attribution ledger
```

A variant may not silently optimize for part count, scale enlargement, sparse approximation, or a different construction style when the control proves a specific fitment/mating behavior.
