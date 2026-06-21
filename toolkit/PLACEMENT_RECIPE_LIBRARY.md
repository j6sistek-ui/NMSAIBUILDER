# Placement Recipe Library v2.06.00

Status: **active staging library** for reusable No Man's Sky construction methods extracted from validated JSON, screenshots, and prior build reviews.

## How to use this file

For future generated builds:

1. identify the requested feature;
2. search this file for a matching recipe;
3. apply the geometry basis and part-family notes;
4. validate spacing with FBX bounds and any JSON precedent;
5. generate in Python using real NMS Builder parts.

Do not use recipes blindly. Each recipe includes classification and limits.

---

## Recipe: Archive / Book-Spine Texture Wall

**Classification:** Toolkit technique  
**Primary source:** Buddies Library & Archives JSON study  
**Key parts:** `S_WALLM_H`, `W_WALL`, `W_WALL_WINDOW`, `T_FLOOR_Q`, `S_FLOOR_Q`, trim/wall families

### Application

Use dense repeated thin-wall/half-wall parts as a controlled texture field:

```text
library shelves
archive ribs
book spines
server-bank texture
bureaucratic records wall
stacked data vault
```

### Geometry basis

```text
macro shell surface
→ local wall plane
→ rows/columns
→ small wall-family texture pieces
→ slight depth offset
→ material zoning
```

### Rule

Dense tiny parts are acceptable only when they form a readable field. They are not random decoration.

---

## Recipe: Macro Shell + Detail Overlay

**Classification:** Universal design/process rule  
**Sources:** Buddies Library, Jurassic HQ, Riverside Town

### Application

For large buildings and themed scenes:

```text
macro shell
→ trim/bands
→ texture fields
→ props
→ lighting/effects
```

### Rule

Do not make small texture parts carry the full building mass. Establish the mass first with larger structural modules.

---

## Recipe: Jurassic Vehicle / Jeep Chassis

**Classification:** Toolkit technique  
**Primary source:** Jurassic HQ JSON study and screenshots  
**Key parts:** wheel/tire parts, panel parts, decals, lights, wall/floor support pieces

### Application

Vehicle replicas, Batmobile side studies, utility trucks, Jurassic jeeps, industrial carts.

### Geometry basis

```text
vehicle-local coordinate frame
→ wheel centers
→ axle/undercarriage
→ body panels
→ cabin/window panels
→ decals/lights
```

### Rule

Vehicle builds must use a local coordinate frame. Do not stretch a real NMS part into unsupported proportions and do not scatter vehicle pieces in world coordinates.

---

## Recipe: Facility Deck / Elevated Platform

**Classification:** Toolkit technique / universal subsystem rule  
**Sources:** Jurassic HQ, Riverside Town, recent floating-platform failures

### Application

Raised labs, visitor centers, megacity platforms, robot facility decks.

### Geometry basis

```text
foundation grid
→ deck surface
→ edge wall/rail
→ underside support/load path
→ connected stairs/ramps
→ props/lights
```

### Rule

A platform is incomplete unless underside support and access are deliberate. Floating underside clutter is a failure.

---

## Recipe: Lab Display Wall / Screen Grid

**Classification:** Toolkit technique  
**Sources:** Jurassic HQ, Riverside Town, Jurassic Beach

**Key parts:** `WALLSCREEN`, `BUILDFLATPANEL`, `BUILDDECAL`, `SERVERSTACK`, screens/decals/lights

### Geometry basis

```text
wall plane
→ row/column grid
→ framed screen panels
→ alternating screen/UserData/graphics
→ console context
```

### Rule

Solve one correct panel orientation and height first; then scale into rows/grids. Do not place screens as random wall clutter.

---

## Recipe: Containment Cylinder / Specimen Tank

**Classification:** Toolkit technique  
**Primary source:** Jurassic HQ

### Application

Jurassic lab tanks, alien biology containment, cloning tubes, robot-controlled specimen storage.

### Geometry basis

```text
base plinth
→ transparent/cylindrical enclosure
→ specimen chain/object
→ top cap
→ lights/consoles nearby
```

### Rule

A containment tank must include context: plinth, enclosure, specimen, cap, lighting, and controls.

---

## Recipe: Pipe / Rail / Conduit Path

**Classification:** Universal subsystem rule  
**Sources:** Jurassic HQ, Riverside Town, powerline studies

### Geometry basis

```text
path endpoints
→ tangent vector
→ module centers
→ curve/corner pieces
→ support brackets
```

### Rule

Pipes, rails, and conduits must follow a route with endpoints. Random pipe decoration is not acceptable.

---

## Recipe: Vegetation Zoning

**Classification:** Toolkit technique  
**Sources:** Jungle/ruins courtyard, Jurassic HQ, Riverside Town, Sloths 3x3x3

### Geometry basis

```text
groundcover
→ shrubs/flowers
→ mid-height plants
→ canopy / silhouette trees
→ focal organic pieces
```

### Rule

Organic scatter should be zoned by height, function, and scale band. Avoid uniform random scatter.

---

## Recipe: Gazebo / Promenade Row

**Classification:** Toolkit technique  
**Source:** Riverside Town

### Geometry basis

```text
path curve
→ repeated anchor pavilion/gazebo
→ fence/edge rhythm
→ worktop/table props
→ small statues/terminals/lights
```

### Rule

Promenades should be path-based. Anchor objects first, then props.

---

## Recipe: Social Patio / Seating Cluster

**Classification:** Toolkit technique  
**Source:** Riverside Town

### Geometry basis

```text
floor field
→ boundary/edge trim
→ table/worktop center
→ chairs radially or linearly around center
→ lights/signs/props
→ clearance check
```

### Rule

Furniture clusters must be generated from a local center; do not scatter chairs, tables, and props independently.

---

## Recipe: Compact 3x3x3 Modular Shell

**Classification:** Calibration / toolkit technique  
**Source:** Sloths 3x3x3

### Application

Small houses, compact cabins, module tests, timber/stone spacing calibration.

### Geometry basis

```text
3x3x3 grid
→ floor/quarter-floor fills
→ wall/window substitutions
→ roof/diagonal pieces
→ sparse interior props
```

### Rule

Compact bases are valuable calibration cases. Preserve shell/floor/wall logic before adding dense interior props.

---

## Recipe: Curved / Stepped Arc from Modular Pieces

**Classification:** Part-family/toolkit technique  
**Sources:** Sloths 3x3x3, Taj dome studies, short-wall ring lessons

### Geometry basis

```text
center
radius
angle_start / angle_end
angle step
chord length
overlap tolerance
part tangent orientation
```

### Rule

Curves must be generated from radius/chord/angle logic. Do not manually offset wall rows unless explicitly making a rough concept study.

---

## Recipe: Same-Position Layered Rotation

**Classification:** Toolkit caution  
**Source:** Sloths 3x3x3, powerline hubs

### Rule

Same-position objects with different `At` / `Up` vectors are not automatically duplicate errors. They may be layered rotations, multi-connection hubs, or radial fills. Check role before deleting.

---

## Recipe: Radial Airlock / Iris Door

**Classification:** Toolkit technique; part-application rule  
**Source:** uploaded `Default` PlayerShipBase / corvette JSON

**Key parts:**

```text
S_GDOOR x12
B_FLOOR_Q x24
B_WALL_Q_H1 x12
F_WALLB_H x24
U_POWERLINE / U_SWITCHWALL / U_SOLAR_S / U_BIOGENERATOR / U_BATTERY_S
```

### Geometry basis

```text
aperture center
normal axis
visible circular plane
radius per layer
depth offset per layer
12/24 segment rhythm
blade/casing/filler/power layers
```

### Observed values

```text
B_FLOOR_Q: 24 pieces, ~15° rhythm, radius ~2.981
B_WALL_Q_H1: 12 pieces, ~30° rhythm, radius ~2.309
S_GDOOR: 12 pieces, ~30° rhythm, radius ~2.579
F_WALLB_H: 24 pieces, secondary casing/support layer
```

### Generator form

```python
place_radial_airlock_iris(
    center,
    normal_axis,
    radius,
    depth,
    segments=12,
    blade_part="S_GDOOR",
    casing_part="B_WALL_Q_H1",
    filler_part="B_FLOOR_Q",
    support_part="F_WALLB_H",
    add_power_logic=True,
)
```

### Rule

Do not flatten this into a row. It is a radial aperture coordinate frame.

### parametric side-count lesson

For 24/32-sided airlock variants, correct orientation is not enough. The invariant is the central iris pivot/apex, not garage-door side-to-side chord spacing. Preserve the known-good center and usually preserve the known-good S_GDOOR radius; increase side count by reducing angular step and increasing overlap density. Only expand radius to preserve chord when the user explicitly requests a larger aperture.

### Caveat

The source is a corvette/player-ship base. Test in normal planet-base context before treating footprint behavior as fully transferable.

---

## Recipe: B_WNG_R Teleporter / Portal Alcove Variant

**Classification:** Staged future extraction  
**Source:** inline user JSON after airlock module

**Key parts:** `B_WNG_R`, `TELEPORTER`, `B_GEN_2`, `BUILDFLATPANEL`, `HOLO_MED2`, `SERVERSTACK`, `WALLSCREEN`, posters, worktop

### Status

Separate from the `S_GDOOR` iris door. Treat as a portal/teleporter doorway or sci-fi alcove variant to extract later.

---

## Recipe: Foosball / Tabletop Game Assembly

**Classification:** Toolkit technique; needs feature-isolation confirmation before locking  
**Source:** Jurassic Beach screenshot + JSON study

### Intended geometry

```text
table-local coordinate frame
→ rectangular table body
→ raised side rails
→ cross rods
→ repeated player/peg objects
→ ball / center focal object
→ optional decals/lights
```

### Rule

Generate rods, pegs, rails, body, and ball in a table-local coordinate frame. Do not scatter them as independent world props.

### Required extraction before locking

```text
table center
length / width / height
body ObjectIDs
rail ObjectIDs
rod ObjectIDs
player/peg ObjectIDs
ball ObjectID
material/UserData
rod spacing
peg spacing
clearance from floor/walls
```

---

## Recipe: Fossil / Skull Facade Marker

**Classification:** Toolkit technique  
**Source:** Jurassic Beach screenshot + JSON study

**Key parts:** `FOS_SKULL`, `BLD_SKULL`, `FOS_BIRD_DIS`

### Geometry basis

```text
wall/window bay
→ face normal
→ centered fossil/skull object
→ scale to bay width
→ offset outward from face
→ optional light/decal
```

### Rule

Skulls/fossils can act as façade focal markers when centered and normal-offset. Do not guess world offsets.

---

## Recipe: Observation Window / Red-Wall Lab Facade

**Classification:** Toolkit technique  
**Source:** Jurassic Beach screenshot + JSON study

### Geometry basis

```text
C_WALL / C_WALL_WINDOW grid
→ colored upper wall band
→ glass viewing strip
→ visible interior props
→ focal skull/sign/light markers
```

### Application

Labs, Jurassic facilities, visitor centers, containment-viewing areas, archive observation rooms.

---

## Recipe: Powerline Hub / Logic Cluster

**Classification:** Universal caution / toolkit technique  
**Sources:** Golden Rock Outpost, Airlock Iris Door, Jurassic Beach

### Rule

Repeated `U_POWERLINE` entries at the same position may encode distinct connection vectors. Do not deduplicate automatically.

### Extract

```text
hub point
endpoint vectors
visible vs hidden status
functional vs decorative role
connected devices
```

---

## Negative Lesson: Jurrasic Beach C_GDOOR / S_GDOOR Dinosaur-Mouth Placement

**Classification:** Project-specific visual accident / do not promote  
**Source:** Jurassic Beach JSON user correction

The `C_GDOOR` / `S_GDOOR` placements in the Jurassic Beach dinosaur mouth were freely placed with poor mechanics. They work contextually because off-placement/misalignment contributes to the organic dinosaur-mouth look.

### Rule

Do not promote those garage-door placements as a reusable mastery recipe. If door parts are used as ribs in future builds, create a separate validated path/ring/chord study.

## Recipe: Connected Angled Megastructure Shell

**Classification:** Universal geometry rule / toolkit method  
**Primary sources:** Alien Megatemple V03 validation, Taj dome lessons, connected-surface v54 rule

### Application

Use for:

```text
alien megatemple shells
pyramidal/shell monuments
Forerunner-style sloped buildings
large domes/cones/spherical shell studies
```

### Geometry basis

```text
target surface plane/profile
→ part extent from FBX or JSON precedent
→ row/column centers projected onto surface
→ panel rotation matches slope/normal
→ small controlled overlap
→ continuous trim only when it connects
```

### Rule

Do not fake shell curvature by simply stepping horizontal wall rows inward unless the user requested a stepped/terraced style or the file is explicitly experimental.

## Recipe: Airlock Iris Door

**Classification:** Toolkit technique / JSON-backed placement recipe  
**Primary source:** `MASTER_LESSONS_LEARNED.md` (removed historical reference: archive/json_studies/NMS_JSON_STUDY_Airlock_Iris_Door_interim_findings.md)

### Application

Use for:

```text
airlock doors
iris portals
vault doors
plasma chamber apertures
hangar seals
alien temple entrances
```

### Extracted baseline

```text
S_GDOOR x12 at ~30° steps
B_FLOOR_Q x24 at ~15° steps
B_WALL_Q_H1 x12 at ~30° steps
F_WALLB_H x24 as secondary casing
```

### Variants

```text
8 panels  = chunky/octagonal variant
12 panels = extracted baseline
24 panels = denser casing/fill
32 panels = high-smoothness experimental iris
```

### Rule

Use the extracted radial coordinate frame and orientation logic as the baseline. Do not guess orientation from scratch.

## Recipe Parameterization Rule

**Classification:** Universal process rule

Recipes are not fixed blueprints unless explicitly labeled as such.

Each recipe should be treated as:

```text
concept + baseline/control + variable parameters
```

Variables can include:

```text
ObjectID family
material
scale
count/density
radius
depth layer
opening size
viewing distance
part budget
```

JSON-derived recipes should be used as geometry references, not as unchangeable mandates.

### Airlock Iris Door — v56 parameterization

The extracted `S_GDOOR x12` module is a baseline/control recipe, not the only valid implementation.

Valid variants include:

```text
8-sided chunky hatch
12-sided extracted baseline
16-sided medium aperture
24-sided denser casing/fill
32-sided smoother high-quality iris
tiny aperture for object reveal
large walk-through portal
```

Compatible garage-door family parts may be substituted after validation:

```text
S_GDOOR
F_GDOOR
B_GDOOR
other *_GDOOR variants where available
```

The exact ObjectID, radius, scale, and orientation offset must be validated against the chosen use case.

## Protocol-linked airlock recipe
Airlock / iris / vault / portal door requests must reference:

```text
rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md
rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md
toolkit/AIRLOCK_IRIS_PARAMETRIC_GENERATOR_SKELETON.py
```

The response must include a `Protocol confirmation` block. The generator must state whether it is using exact control or parametric variant.

## Spire / Tapered Tower Visual Recipe Notes
Status: preliminary visual recipe, pending exported JSON.

User-provided screenshots show that spires do not have one true method. The transferable concept is:

```text
base drum
+ tapered ribs / short-wall or wall pieces
+ connected top convergence
+ infill or open sectors
+ collar bands
+ cap / finial / flag / antenna
```

Read:

```text
rules/SPIRE_TAPERED_TOWER_VISUAL_RECIPE_NOTES.md
```

Do not lock exact ObjectIDs, scale, radius, or orientation until the matching spire JSON is reviewed. Use the screenshot findings as concept classification and extraction checklist only.

## Mini JSON Spire Support Note
The `Jenness WIP Townhome` mini JSON adds partial JSON support to the visual spire notes.

Key concept:

```text
short-wall spire =
polygonal base drum
+ staged wall courses
+ tilted S_WALL_Q / S_TRIFLOOR_Q convergence pieces
+ roof-cap transition
+ optional powerline/light/detail layer
```

Read:

```text
rules/SPIRE_MINI_JSON_PRELIMINARY_EXTRACTION_NOTES.md
```

This is still not a locked exact spire recipe. Use as a partial-control observation until a more complete spire JSON is supplied.

## Power / utility parts are not feature geometry
Powerlines, switches, batteries, solar panels, biofuel generators, and related utility devices should not be promoted into feature recipes by default. If source JSON includes these, classify them as ignored utility infrastructure unless the user explicitly requests a power/logic/cable feature.

## Connected-Piece Curvature Grammar
This is a broad recipe-search layer, not one exact ObjectID recipe.

Use it when a design asks for:

```text
dome
spire
cupola
rounded shell
curved roof
insect/creature body
vehicle hull
pod
cylindrical habitat
circular tower
machine core
arch/rib/collar/oculus
```

The key method is:

```text
controlled curve/path/profile
+ repeated similar pieces
+ connected overlap/chord spacing
+ scale profile
+ convergence/contact validation
+ Position/Up/At transformed together
+ color/effect layers
```

Read:

```text
rules/CONNECTED_PIECE_CURVATURE_GRAMMAR.md
```

The dome, cylindrical habitat, and spire examples are instances of this broader grammar, not narrow recipes only for those exact requests.

---

## Recipe: Endpoint Stair / Ramp Connection

**Classification:** Geometry intelligence template pending source-specific control JSON  
**Primary rule:** `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`

### Application

Use for stairs, ramps, stepped bridges, access paths, and connected approach runs.

### Geometry basis

```text
start landing anchor
→ end landing anchor
→ path vector / yaw
→ rise and run
→ module count
→ center-to-center spacing
→ first/last contact
→ support/load path
```

### Rule

A stair/ramp is an endpoint-connected subsystem. Do not place segments as decorative repeated parts. Variants must recompute count and spacing from endpoints and part bounds while preserving contact.

---

## Recipe: Dome / Latitude Shell

**Classification:** Geometry intelligence template pending source-specific control JSON  
**Primary rules:** `rules/CONNECTED_PIECE_CURVATURE_GRAMMAR.md`, `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`

### Application

Domes, cupolas, rounded roofs, oculi, curved shells, pods, and shell-like canopies.

### Geometry basis

```text
local center axis
→ layer/profile table
→ radius per layer
→ height per layer
→ segment count per ring
→ chord spacing
→ tangent orientation
→ vertical contact
→ cap / oculus / apex condition
```

### Rule

A dome variant scales or regenerates the profile table. It must not scatter pieces by visual angle guessing.

---

## Recipe: JSON Control-to-Variant Workflow

**Classification:** Mandatory workflow  
**Primary rule:** `rules/RECIPE_PARAMETERIZATION_PROTOCOL.md`

### Application

Use whenever the user asks for the same feature with different size, count, radius, material, position, or style.

### Rule

Name the control source, preserve locked invariants, vary only declared parameter slots, and validate connection proof before treating the variant as successful.


## Provisional recipe — gothic metal castle facade

**ID:** `gothic_metal_castle_facade`

Use for NMS-context prompts requesting a gothic/castle/fortress facade, especially when paired with a known feature such as a radial airlock/iris door.

Locked invariants:

- symmetric front facade axis;
- entrance wall plane;
- airlock center on facade axis;
- 12-sided radial ring when requested;
- flush outer face with surrounding entrance wall;
- connected wall-to-airlock frame;
- tower, buttress, and spire contact proof.

Allowed parameters include width, tower count, tower height, wall height, airlock radius, detail density, and compatible metal/alloy part-family substitutions.

This is provisional until promoted from generated control JSON or user-provided JSON.
