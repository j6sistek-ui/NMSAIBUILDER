# Spacing / Connection / Scale Rules v54

Status: **active required validation layer** for generated No Man's Sky builds.

This file consolidates recurring spacing and connection lessons from JSON studies, FBX-derived bounds, in-game screenshot reviews, and repeated generation failures.

## Core rule

```text
Never place repeated parts by visual guess when FBX bounds or JSON placement precedent exists.
```

Use:

```text
FBX bounds = physical footprint
JSON examples = proven real-builder placement behavior
Screenshots = final visual validation
```

## Required for generated scripts

Every generated Python build with repeated pieces must state:

```text
ObjectID
part role
source of spacing: FBX / JSON precedent / explicit user study / provisional
scale
center-to-center step or chord spacing
overlap tolerance
connectivity expectation
```

## Stairs and ramps

### Required approach

```text
start landing
end landing
path vector
yaw from path
rise
run
module count
center-to-center spacing
overlap/contact tolerance
first/last landing connection
```

### Rejection criteria

A stair/ramp run fails if:

- it is placed by decorative repetition rather than endpoints;
- segments do not touch/overlap;
- the final segment does not meet the landing;
- it floats without support;
- yaw is guessed instead of path-derived;
- rise/run is not physically plausible for the selected ObjectID.

## Floors and platforms

Observed floor spacing from JSON studies reinforces family-specific spacing:

```text
Full floor families often appear around ~5.3m center rhythm.
Quarter floor families often appear around ~2.6–2.7m center rhythm.
Triangle floor families use their own rhythm and cannot be treated as full floors.
```

These are precedents, not universal constants. Confirm with FBX bounds and project context.

## Walls and short walls

Rules:

```text
Wall/short-wall runs require connected center-to-center spacing from visible footprint.
Vertical stack spacing must be separated from horizontal run spacing.
Short-wall ring/arc placement requires radius/chord/angle calculation.
```

Do not call a trim/wall run “continuous” unless pieces actually meet or overlap from the intended viewer angle.

## Curves, rings, and apertures

Use:

```text
center
radius
angle_start
angle_end
segment_count
angle_step
chord = 2 * radius * sin(pi / count)
visible tangential length
overlap tolerance
part tangent orientation
depth layer
```

This applies to:

- Taj dome/curved-wall studies;
- short-wall rings;
- airlock/iris doors;
- portal rings;
- curved decorative arcs;
- circular floor/fill systems.

## Vehicles and small assemblies

Generate from local frames, not global scatter.

Required fields:

```text
assembly center
local X/Y/Z axes
primary dimensions
anchor points
subpart roles
spacing per subpart row
clearance
```

This applies to:

- vehicles;
- foosball/tabletop games;
- machinery lines;
- lab tables;
- display consoles.

## Same-position duplicates

Do not automatically delete same-position repeated objects.

They may represent:

- powerline hub vectors;
- layered/rotated quarter floors;
- radial fills;
- logic connections;
- visual multi-layering.

Only remove if confirmed redundant/hidden.

## Organic scatter

Organic scatter should use zones and scale bands:

```text
groundcover
flowers
shrubs
mid-height plants
canopy trees
focal organic forms
```

Uniform random scatter is weak unless intentionally making rough wilderness.

## Negative-case handling

Less-skilled JSON builds are still useful for spacing extraction and contrast. Do not promote weak composition into a style recipe.

Record:

```text
what works mechanically
what works visually
what not to copy
classification: negative lesson / project-specific observation
```

## Curvature spacing generalization
Dome, cylindrical habitat, spire, body-shell, and vehicle-hull examples all belong to the connected-piece curvature family. For repeated curved features, validate chord/path spacing, overlap, scale profile, contact/convergence, and envelope limits. Changing the curve path changes the shape, but the same connection rules apply.

## geometry-intelligence reinforcement

When relevant JSON exists, exact recreation is not the end state. Apply `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md` to preserve the reusable logic: part roles, anchors, local frames, connection/contact relationships, locked invariants, allowed parameter slots, and missing evidence.

If a prior JSON-derived technique cannot be found in `toolkit/PLACEMENT_RECIPE_LIBRARY.json`, `data/JSON_RECIPE_SIGNATURE_INDEX.json`, reports, or the source package, do not claim the technique was retained. Request the source JSON again or mark the recipe provisional.
