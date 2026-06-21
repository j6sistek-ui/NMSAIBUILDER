# Connected-Piece Curvature Grammar v2.04.05

Status: **active broad feature-generation grammar**

## Purpose

Recent JSON and screenshot studies produced strong examples of domes, cylindrical habitats, and spires. The important reusable lesson is broader than those labels.

The core method is:

```text
Use repeated real NMS pieces — walls, short walls, floors, roof pieces, panels, trim, pipes, cylinders, and related part families — along a controlled curve/path/profile/convergence frame to create a larger shaped object.
```

The examples are not isolated recipes only for:

```text
dome
cylindrical room
spire
```

They are instances of a broader construction grammar:

```text
connected-piece curvature
```

This rule prevents the knowledge base from becoming overly restrictive. A future request may ask for a shell, hull, rounded insect body, curved machine core, organic pod, tower crown, canopy, arch, rib cage, oculus, dome, spire, cupola, cylinder, or fantasy roof. The generator should search for the underlying curve/surface/convergence grammar, not only exact recipe names.

## Core principle

```text
Change the curve path/profile/shape, keep the connected-piece logic.
```

A successful curved feature usually comes from:

```text
local feature frame
+ curve/path/profile/control points
+ repeated similar parts
+ connected overlap/chord spacing
+ scale and density control
+ Position/Up/At transformed together
+ contact/convergence validation
+ color/material/effect layers
```

## What to extract from JSON

For any JSON feature using connected pieces to make a shape, extract:

```text
feature concept name
geometry primitive
local feature frame
curve/path/profile/control points
radius / chord / segment spacing
overlap tolerance
part-family roles
ObjectID counts
scale bands
height/radius/profile table
convergence points
material/UserData per layer
contact validation
negative lessons
```

Do not stop at the literal title of the feature.

## Geometry primitives

| Primitive | Meaning | Example sources |
|---|---|---|
| ring / arc | pieces placed around a circle or partial circle | stone trim rings, airlock, circular habitat rings |
| stacked latitude shell | rings at changing radius/height | dome roof example |
| tapered convergence shell | base ring converges toward apex/top ring | spire/cupola examples |
| path assembly | pieces follow a curve or line between endpoints | pipes, skybridges, side booms, ramps |
| surface tile shell | panels tiled over a curved/rounded surface | Taj dome, Bumblebee body, dome wall shell |
| rib overlay | trim/ribs trace a curve over a shell | spires, domes, gothic/tower ribs |
| local object hull | small parts approximate a recognizable object | vehicles, foosball, insects, machine shells |
| sector grid on curve | rooms/props divided around circular/radial sectors | cylindrical habitat interior |

## Examples now generalized

### Dome wall-shell example

Specific label:

```text
dome shell with cylinder band
```

Broad grammar:

```text
stacked latitude rings using wall/roof pieces, changing radius per height, with a belt/collar transition
```

Reusable for:

```text
domes
rounded roofs
caps
hulls
giant creature bodies
sci-fi pods
tower crowns
planetarium shells
```

### Cylindrical habitat example

Specific label:

```text
floating cylindrical habitat
```

Broad grammar:

```text
centerline + radial deck rings + vertical cylindrical modules + side path assemblies + sector interiors
```

Reusable for:

```text
space stations
round towers
orbital platforms
reactor cores
hotel pods
floating cities
circular labs
```

### Mini spire example

Specific label:

```text
short-wall spire / cupola
```

Broad grammar:

```text
base drum + staged wall courses + tilted short-wall/rib convergence + cap/collar
```

Reusable for:

```text
spires
cupolas
tower caps
fantasy roofs
gothic ribs
antenna housings
decorative finials
```

### Taj dome / Bumblebee / vehicle-shell lessons

Specific labels:

```text
Taj dome
Bumblebee body shell
vehicle hull
```

Broad grammar:

```text
connected panels along a curvature profile, using scale/rotation/overlap to approximate a larger curved object
```

Reusable for:

```text
rounded vehicles
creature bodies
insect shells
domes
pods
curved machine housings
```

## Generator contract

A generator using this grammar must explicitly define:

```text
feature_type
local frame
curve/profile type
control points
part families
segment count
radius/path/chord spacing
overlap tolerance
scale profile
orientation basis
contact/convergence targets
material/effect profile
```

### Required function pattern

```python
place_connected_piece_curved_feature(
    center,
    frame,
    profile,
    part_layers,
    segment_policy,
    overlap_policy,
    material_profile,
    validation_policy,
)
```

Where:

```text
profile = ring, arc, dome_latitudes, tapered_spire, path_curve, hull_surface, sector_grid
part_layers = shell panels, ribs, collars, lights, infill, caps, supports
segment_policy = count, angle step, spacing, density
overlap_policy = chord, visible length, seam overlap, burial/sinking if needed
```

## Mandatory transformation rule

For radial, tapered, curved, or shell features:

```text
Position, Up, and At must transform together.
```

Never rotate only positions.

## Connected-piece spacing rule

For repeated parts forming a curve:

```text
chord = 2 * radius * sin(pi / segment_count)
```

Use FBX bounds or JSON precedent to compare the chord to the visible part width/length.

If the curve is not circular, use local path length / segment count and validate against visible footprint.

## Contact and convergence validation

A curved feature is not valid because it has the right silhouette alone. It must pass contact checks:

```text
adjacent pieces overlap or touch by intended seam tolerance
ribs connect to base/collar
spires converge or terminate into cap/top ring
domes have closed or deliberately open crown
side booms connect to sockets
shell panels stay inside intended envelope
```

## Envelope rule

Curved features must stay inside an intended envelope:

```text
width/radius limits
height limits
walkable/interior clearance
part-count budget
base/collar footprint
viewing angle
```

Changing the path/profile changes the look, but the feature must not explode outward or float away from the design envelope.

## Material/color/effect layer rule

Color and effects are part of the shape read.

For curved objects, document:

```text
shell material
rib material
collar/belt material
infill material
light/effect accents
contrast bands
```

The same geometry with different colors can read as stone, metal, sci-fi, organic, machine, or fantasy architecture.

## Search behavior in the recipe library

When a user asks for:

```text
dome
spire
cupola
rounded shell
curved roof
insect body
vehicle hull
cylindrical habitat
circular tower
pod
rounded machine core
curved wall feature
```

the chat/AI should check this connected-piece curvature grammar, not only an exact named recipe.

## Safe adaptation

A recipe can be adapted when:

```text
same geometry primitive is preserved
part families are similar or validated
FBX/chord spacing is checked
Position/Up/At transformation is preserved
contact/convergence passes
```

## Caution

This rule does not mean every curved feature is solved. It means the generator must reason in terms of shape grammar and validation, not only copy specific examples.

The rule is broad. Exact ObjectIDs, dimensions, and material values still require JSON precedent, FBX bounds, or explicit user approval.

## geometry-intelligence reinforcement

When relevant JSON exists, exact recreation is not the end state. Apply `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md` to preserve the reusable logic: part roles, anchors, local frames, connection/contact relationships, locked invariants, allowed parameter slots, and missing evidence.

If a prior JSON-derived technique cannot be found in `toolkit/PLACEMENT_RECIPE_LIBRARY.json`, `data/JSON_RECIPE_SIGNATURE_INDEX.json`, reports, or the source package, do not claim the technique was retained. Request the source JSON again or mark the recipe provisional.

## Anti-pattern: no stepped-offset substitute (absorbed from CONNECTED_SURFACE_NO_STEPPED_OFFSET_RULE)
## Status

**Universal rule.**

This applies across generated No Man's Sky base scripts unless the user explicitly requests a stepped/terraced style or the file is clearly labeled as a study/experiment.

## Rule

Do not use stepped-offset stacking as a substitute for true connected curvature, slope, or shell geometry.

In normal production scripts:

```text
curved/sloped form must be built from connected angled surfaces
not from stacked horizontal rows that merely imply the silhouette from distance
```

## Why

Stepped offsets can create a distant silhouette, but they usually fail close inspection:

- visible gaps between courses;
- inconsistent overlap/gap behavior;
- surfaces read as stacked stairs rather than engineered architecture;
- trim/rail systems become visually discontinuous;
- the build looks like object placement rather than coherent structure.

The default expected quality is connected architectural geometry, not a distant look-alike.

## Allowed exceptions

Stepped-offset construction is allowed only when one of these is true:

1. The user explicitly requests a terraced / ziggurat / stepped style.
2. The file is labeled as a study or experiment.
3. The stepped parts are hidden structural backing and not the visible surface.
4. The design intentionally needs a staircase/terrace read.
5. The offset is a minor decorative relief layer over a connected main surface.

## Required practice for curved or sloped forms

Use one of these methods:

- angled wall/shell panels with connected edges;
- ring/chord placement for domes or circular shells;
- faceted surface planes with consistent angle and spacing;
- large roof/shell parts when they supply correct material and curvature;
- panel rows calculated from actual FBX bounds and visual seam tolerance.

## Continuous means connected

Any generator function or object name containing words like:

```text
continuous
ring
rail
rim
belt
trim
edge
perimeter
```

must create visibly connected parts or be renamed/removed.

A broken row of isolated pieces must not be labeled continuous.

## Floating/random part rule

Floating parts are generally disallowed unless they have a clear intentional role:

- light or glow emitter;
- energy node;
- levitation effect;
- suspended mechanical component;
- alien anti-gravity feature;
- deliberate ceremonial floating object.

Random floating parts or detached filler pieces should be removed.

## Validation checklist

Before releasing a script that builds a shell, dome, curved wall, slope, rail, rim, or trim:

- Are repeated parts connected or intentionally overlapping by a small controlled tolerance?
- Are gaps consistent and intentional?
- Are seams derived from part dimensions or confirmed calibration?
- Is any “continuous” part family actually continuous?
- Are floating pieces named/labeled by purpose?
- Would the structure still read as architecture close-up, not only from far away?

## Relevant prior lessons

- Taj dome: successful curved read came from profile, chord/angle logic, material, and controlled density.
- Alien Megatemple V03: central silhouette improved, but stacked-offset rows failed as a connected architectural shell.
