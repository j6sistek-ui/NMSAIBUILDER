# Visual Build Toolkit — Alien City-Canyon / Megatemple Language v51

## Classification

**Toolkit technique**, not project-only.

These findings came from user-provided in-game and concept reference images. They apply to the current Alien Megatemple project, but they are broader NMS building knowledge for future builds.

## Core reusable lesson

Large alien/cyberpunk builds feel massive when they create **architectural enclosure**, not merely tall objects.

```text
scale = enclosure + layered depth + repeated surface language + controlled lighting
```

A single tower on an open platform usually reads smaller than a dense canyon of surrounding architecture.

## Toolkit techniques captured

### 1. Architecture-canyon composition

Use tall left/right wall masses, overhead bridges, pipes, and layered background towers to create a walkable canyon.

Reusable for:
- alien megatemples
- cyberpunk cities
- industrial bases
- freighter-city streets
- mining refineries
- capital-city districts

Implementation pattern:

```text
foreground entry frame
→ narrow/controlled processional street
→ tall wall masses left/right
→ overhead cross-beams / suspended machinery
→ distant vertical skyline stack
```

### 2. Surface-built monument

A monumental object should be built from surfaces and seams, not stacked props.

Good:
- repeated wall-panel fields
- nested trim rows
- relief panels only at focal zones
- carved portal/void
- large ribs/buttresses
- material-consistent surface density

Bad:
- tower prop + lights + random surrounding objects
- isolated floating platforms with no architectural hierarchy
- scattered boxes or capsules pretending to be city detail

### 3. Negative-space portal

The strongest alien temple references use voids/gaps as the focal object.

Technique:
- omit panels to create the opening;
- frame with nested arches/triangular ribs;
- place light/energy inside the recess;
- make the portal deep enough that it casts shadow and reads as an entrance.

### 4. Lighting as infrastructure

Lights should explain the building, not decorate it randomly.

Use lights for:
- vertical energy seams;
- portal outlines;
- bridge centerlines;
- tower ribs;
- gravity-lift shafts;
- backlit lattice panels;
- navigation/pathing.

Avoid:
- unstructured light scatter;
- lights floating without surface/structural role;
- red emissive overload when target palette is blue/purple.

### 5. Machine-city skin

Industrial parts become architecture when embedded into wall systems.

Use:
- pipes as façade conduits;
- tanks/cylinders as tower mass;
- screens/signs as district identity;
- repeated windows/vents as high-rise texture;
- crossbeams as overhead compression.

Do not place them as loose objects on a platform.

### 6. Controlled foreground-to-background layering

Make the build readable in three depths:

| Layer | Function |
|---|---|
| Foreground | entry frame, lamps, portal, street scale |
| Midground | main walls, bridges, walkable canyon |
| Background | high towers, machinery stacks, skyline fins |

## NMS part-use candidates

These are candidate part families, not hard rules. Validate orientation/material behavior per project.

### Structural wall/canyon surfaces

- `B_WALLM`, `B_WALLB`, `B_WALLT`
- `B_WALL*_WIN*`
- `F_WALLM`, `F_CHEV_WALL`, `F_WALLM_WIN3`
- `CUBEROOM`, `CUBEGLASS`, `CUBEFRAME`

The part library shows wall/window panels have measured FBX extents and should be spaced from actual bounds rather than guessed spacing.

### Large spire / roof / shell masses

- `B_ROOF6`
- `B_ROOF7`
- `B_ROOF8`
- `SET_B_MONU`
- `SET_S_TOWER`
- `S_TOWER_C`
- `B_TOWER_B`

Use these as mass contributors, not as random tower stacks.

### Blade ribs / alien fins

- `B_WNG_R`, `B_WNG_R_T`, `B_WNG_R_B`
- `B_WNG_Q`, `B_WNG_Q_R`
- `B_WNG_A`, `B_WNG_A_R`
- `B_DECO_S`

Use them as explicit structural ribs, buttresses, fins, or portal-frame members.

### Energy and lighting infrastructure

- `BASE_BEAMSTONE`
- `WALLLIGHTBLUE`
- `WALLLIGHTPINK`
- `LIGHTFRAME`
- `LIGHT_VERT`
- `BASE_NEXUS*`
- `BUILDANTIMATTER`

`BASE_BEAMSTONE` has a large vertical extent and is especially useful as a gravity-lift/energy-seam part.

### Machinery / conduit skin

- `BASE_BUBPIPE`, `BASE_BUBPIPE_L`, `BASE_BUBPIPE_T`, `BASE_BUBPIPE_X`
- `B_CON_*`
- `B_GEN_*`
- `B_SHL_*`

Use them in organized rows, trunks, or conduit systems.

## Applied to Alien Megatemple

The current project should not be treated as “floating islands around a spire.” The better direction is:

```text
floating alien city-canyon
with a giant sacred portal embedded into dense vertical architecture
```

The center should dominate as a coherent megastructure, with satellites/courts secondary.

## Non-validated items

These are not yet promoted to hard rules:

- exact palette values;
- exact part rotations for blade ribs;
- exact spacing for city-canyon wall density;
- whether V03 shell geometry works in-game;
- whether the contact sheet examples should become permanent visual-library anchors beyond this v51 update.

## Visual anchor

A small contact sheet is retained at:

`visual_library/contact_sheets/ALIEN_CITY_CANYON_VISUAL_TOOLKIT_v51.jpg`
