# Part Use Case Catalog

Use this catalog for **design potential** and creative memory recall. It is not a placement-validation file unless a listed ObjectID appears in the current script.

## Mandatory logging rule

When a screenshot, JSON export, manual example, or user feedback reveals a reusable part application, log it here immediately. See `SELECTIVE_VISUAL_MEMORY_POLICY.md`.

## Scale-mode rule

- **Micro builds:** density can work: foosball tables, books, dining tables, tabletop objects.
- **Macro landmarks:** scale and connected structure matter first; tiny detail fields often disappear or become clutter.
- **Environmental/style builds:** mood comes from color, clustering, burial, silhouette, and contrast.

## Catalog entries

| ID | Parts / families | Visual role | Why it works |
|---|---|---|---|
| `foosball_table_micro_build` | ABAND_BENCH, pipes/cylinders, small panels, colored small props | foosball table / tabletop game | At micro scale, repeated tiny components read as game mechanics instead of clutter. |
| `library_books_from_shrunk_walls` | walls, short walls, flat panels, trim pieces | book spines, shelves, library stacks | The rectangular wall silhouette becomes a book spine when reduced and repeated in shelf context. |
| `dining_table_centerpiece` | floor/tabletop pieces, cylinders/columns, spheres, decorative plants, small props | dining table, chairs, centerpiece, food/flower arrangement | A simple furniture silhouette plus a focal centerpiece reads clearly without many parts. |
| `cave_creeper_cherry_blossom_tree` | BASE_CAVE2, BASE_SWAMP2 or tree/stump parts, decorative plant families | cherry blossom canopy / flowering tree | Color + clustering overrides literal cave-plant identity and creates blossom mass. |
| `swampy_overgrown_scene` | BASE_SWAMP*, BASE_CAVE*, BASE_JUNGLE*, rocks, pods/domes, walls/platforms | swamp settlement / alien overgrowth | Mood comes from density, color, partial burial, and contrast between structure and organic growth. |
| `micro_build_normal_parts_reuse` | walls, floors, benches, lights, pipes, props | toys, furniture, appliances, small machines, signs, tabletop objects | At small scale, context dominates literal part name. |
| `macro_monument_scale_over_clutter` | S_ARCH, S_ARCH_H, S_WALLM, S_WALL_Q_H1, S_WALL_SUPPORTS, large wall/arch families | grand facade / monument architecture | Large forms are visible at monument scale; tiny details are lost or become noise. |
| `wall_panel_dome_surface_shell` | S_WALLM_H, S_WALL_Q_H1, wall/short-wall panel families | low-part-count dome or glass-dome-like shell | Achieves alternate dome style while conserving parts vs dense `S_ROOF5` tile fill. |
| `worktop_reflective_hull_skin` | BUILDWORKTOP, WORKTOP | reflective hull/wing/skin panels | A flat/worktop surface becomes a controllable reflective panel when repeated. |
| `dense_roof_tile_dome_vs_surface_shell_tradeoff` | S_ROOF5, S_WALLM_H, SPHERESHAPE | dome construction strategies | Shows tradeoff between ornate detail and part budget; choose based on visual objective. |
| `wonder_projector_not_general_decoration` | HOLO_DISCO | configured wonder projector only | Requires in-game setup; generated use is misleading unless explicitly configured. |

See `PART_USE_CASE_CATALOG.md` for machine-readable details.


# v40 Visual Reference Expansion

These are user-supplied reference-build lessons converted into reusable creative part-use memory. They are design-potential prompts, not mandatory project requirements.

| Reference | Reusable use-case lesson | Candidate role families |
|---|---|---|
| `VR40_001_cyberpunk_vertical_city_street` | Cyberpunk vertical city street with vegetation and signage: Strong build read comes from layered depth: foreground plants, street corridor, midground towers, distant sky object. | signage/screen panels, vertical glass/cylindrical tower modules, plants as urban canopy |
| `VR40_002_night_neon_megacity_overlook` | Night neon megacity overlook with crystals and platform lighting: At night, color zoning can carry the design: cyan/purple/red landmarks define districts. | crystal/beam/glow landmark, billboards as skyline identity, platform floor grid |
| `VR40_003_bioluminescent_bridge_garden` | Bioluminescent garden bridge with curved rails: A simple bridge becomes memorable when the rails define a strong curve and the surrounding plants glow. | rail cables/pipes, floor planks or tread panels, glowing plant clusters |
| `VR40_004_bioluminescent_portal_throne` | Bioluminescent portal/throne with giant flower canopy: Overscaled plant or shell-like parts can become canopy architecture, not just landscaping. | plant fronds as canopy petals, sphere/orb as portal core, tree/root parts as arch frame |
| `VR40_005_macro_train_and_station` | Macro train build with station context: Macro builds need a clean silhouette first: long body, cab/front, wheels, track, and station context. | cylinders/tanks as boiler, pipes as rods/rails, round parts as wheels |
| `VR40_006_pyramidal_roof_tower_cluster` | Pyramidal roof tower cluster with ribs and fire caps: Repeating steep roof modules creates identity quickly. | roof pieces as pyramid caps, beams/trim as ribs, lights/fire as tower caps |
| `VR40_007_dense_lab_display_room` | Dense laboratory/display room with shelves and illuminated objects: Interior density works when organized into shelves, cases, and zones. | shelves/display cases, small tech props as artifacts, light strips as shelf dividers |
| `VR40_008_compact_neon_shop_front` | Compact neon shop front with visible interior inventory: A small shop can feel complete with a strong sign, open front, and detailed back wall. | sign panels/decals, shelves and micro props, door/window frame |
| `VR40_009_split_lab_workstations` | Split lab/workstation interior with color-coded rooms: Two-room composition works when each side has a distinct lighting color and function. | console/control panels, glass dividers, central structural column |
| `VR40_010_rustic_cottage_terrain_integration` | Rustic cottage with terrain integration and stone retaining walls: Terrain integration sells small architecture: stairs, retaining rocks, and raised foundation make it grounded. | rock parts as retaining walls, floor/steps as path, roof panels as gable |
| `VR40_011_green_door_sci_fi_facade` | Green-lit sci-fi facade with crystal landmark: A single saturated doorway color can define an entire facade. | bright door/window panels, crystal/glitch parts as landmark, dark frame panels |
| `VR40_012_red_castle_towers` | Red-lit castle towers with steep roof modules: Steep roofs, red-lit apertures, and vertical massing create gothic/sci-fi castle identity. | roof modules as gothic caps, red lights/windows as oculi, wall panels as tower mass |
| `VR40_013_modern_coastal_house` | Modern coastal house with circular windows and turret cap: A few strong motifs—circular windows, clean horizontal bands, and a cap roof—define the build. | round window parts, turret/cap roof, horizontal wall bands |
| `VR40_014_grand_symmetric_stair_hall` | Grand symmetric stair hall with ceiling fins: Large symmetrical stairs are powerful because of repetition and scale, not micro-detail. | floor panels as checkerboard, wall/roof/trim parts as stair treads, ceiling ribs/fins |
| `VR40_015_luminous_garden_throne` | Luminous garden throne with crystal petals and organic framing: A small seating object can become a scene if framed by symmetrical light, plants, and trees. | crystal/shard petals, chairs/throne, trees/branches as arch frame |

## v40 Creative-use reminders

- Monumental builds should use scale, silhouette, and connected structure before micro-detail.
- Interior/lab/shop builds can support dense micro-detail when it is organized by shelves, cases, counters, or zoning.
- Organic and glitch parts should be considered as architecture: canopy, petals, frames, roots, ribs, landmarks, and light sources.
- Vehicle and mechanical builds require context objects—track, gantry, station, platform, or hangar—to make the macro silhouette legible.
- Lighting is often the object: signs, glowing doors, color zoning, crystals, hidden lights, and emissive strips can define the purpose of a space.


# v41 Selective Memory Update

The use-case catalog should grow by **principle**, not by raw example count.

When a screenshot/build shows a familiar concept, merge it into the existing principle unless it changes the rule. When it shows a new concept or contradicts a prior assumption, create a new entry and classify retention:

- Level 1: text lesson only
- Level 2: retained visual anchor
- Level 3: promoted rule

This keeps the catalog useful for creativity without becoming a bloated image/archive index.

# v42 Exploration and Recent Study Use-Cases
| ID | Parts / families | Visual role | Why it works |
|---|---|---|---|
| `deepsea_room_skyscraper_toppers` | `MAINROOM_WATER`, `MAINROOMCUBE_W`, screens, antennas, robot/FX parts | modular skyscraper crowns / colored rooftop identity | Circular and square deep sea rooms provide strong macro volume; creativity comes from silhouette diversity, offset pods, bridges, receivers, and purposeful detail. |
| `automation_gantry_conveyor_cassettes` | `B_WALL_CARG1`, `B_ROBOTARM`, `ROBOTICARM`, `BASE_ROBOTOY`, screens | robot factory / rooftop automation line | Conveyor/cargo pieces work when framed as machine cassettes with rails, arms, and drone bodies. |
| `connected_drone_hive_crown` | `S_TOWER_C`, `BASE_ROBOTOY`, `BLD_CRYS_DRONE`, `B_CON_*`, antennas | connected drone service crown | Drones read better when attached to visible docking/service structure instead of loose orbital placement. |
| `grounded_antenna_signal_crown` | `B_ANTENNA*`, `S_ANTENNA0`, cubes/cylinders/rooms | AI relay / broadcast crown | Antennas need bases and a named signal role; floating spires are a failure unless holographic suspension is intentional. |
| `harvester_reactor_pit` | `B_ROBOTARM`, `B_SHL_C`, `BASE_WEIRDCUBE`, `TURRET_ABAND`, square lips/rails | machine harvesting pit / robotic containment | Robotic arms gain purpose when aimed at a central subject with containment field, rails, and scanner projectors. |
| `red_lens_surveillance_iris` | `B_SHL_E`, `B_DECO_P`, walls/scaffolds, `TURRET_ABAND` | AI eye / surveillance portal | Red shield lenses work best as recessed surveillance optics or architectural apertures, not exposed generic rows. |
| `selective_variant_pruning` | all studies | study discipline | If a variant is not screenshotted, praised, or promising, remove or overhaul it rather than preserving it to fill count. |


# v45 reference batch lessons

This batch reinforces selective visual-memory behavior: most examples are recorded as principles only; only high-value anchors retain images.

## New/expanded reusable concepts

- **Macro vehicle/display context:** ships and vehicles need gantries, service towers, docks, cradles, tracks, hangars, or platforms to become believable.
- **Tiered ceremonial architecture:** large stairs, terraces, sparse corner ornaments, and repeated roof language create grandeur with low detail density.
- **Macro creature anatomy:** build body path, heads, eyes, mouth/claws, and silhouette before surface texture. Repeated small parts become scales/spines only after the macro creature reads correctly.
- **Formal entry axis:** banners, wall lights, and framed door/arch openings can create strong identity with very few parts.
- **Terrain-spanning city layout:** long stairs/walls/docks/bridges connect separated compounds into one scene.
- **Neon urban density:** signs and color zones should attach to readable tower masses and circulation paths, not become floating clutter.


# v46 video reference lesson — Jurassic preserve / theme-park build system

The Jurassic Park walkthrough demonstrates that large nostalgic/cultural builds should be treated as **scene systems**, not isolated objects.

## Reusable system

```text
identity marker → entrance/gate → habitat/paddock zones → viewing areas → lab/control interiors → vehicle/tour staging → terrain/path integration
```

## Core principle

Themed environments need recognition, containment, pathing, and zone logic. A creature build without fences/platforms/lab context reads weaker than a creature embedded in a park, preserve, museum, or research facility.

## Transferable applications

- Jurassic Park / dinosaur lab
- alien zoo or preserve
- safari base
- museum/exhibit build
- monster containment facility
- Halo outpost with zones
- Star Wars base with hangars and vehicle staging
- horror park / research compound

# v49 Taj Mahal project completion part-use lessons

## Taj/stone landmark part-use findings

- `S_ARCHM` can replace `S_ARCH` for cleaner visible façade arch surfaces when the base arch variant shows unwanted brown/patchy stone texture.
- `S_ARCHM_H` can replace `S_ARCH_H` for cleaner half-arch façade surfaces in the final Taj-style front/rear arch composition.
- `S_WALLM` works well as a large macro wall shell when the façade overlays carry the architectural read.
- `S_WALL_Q_H1` is high-value trim/banding; preserve it during part reduction if it carries the architectural register.
- Large scaled `S_FLOOR` panels can replace many raised plinth floor tiles when hidden/low-value tile seams are not essential.
- Large `S_FLOOR` should not blindly cover hidden central areas; use perimeter-only visible flooring where central floor is covered by structure.
- A single large `S_ROOF5`, buried/raised correctly, can replace many smaller dome/socket pieces.
- `S_WALL_SUPPORTS` can be stacked at façade corners as a finishing/pilaster feature, but requires visual offset calibration.

## Taj process lesson

The final build succeeded by solving the recognizable monument first, then optimizing construction. Future landmark projects should not let part limits erase the silhouette before the design is readable.

# v50 Swarm plugin 6.4.1 new part use

## New signage and faction identity parts

Base Builder 6.4.1 adds/exposes Swarm flags, posters, and decal parts.

Useful roles:
- faction signage
- expedition/Swarm identity markers
- banners and hanging fabric
- wall posters for shops, labs, museums, and cyberpunk streets
- district color/signage language

New/updated ObjectIDs include:
- `EXPD_DECAL22`
- `EXPD_POSTER22A`
- `EXPD_POSTER22B`
- `EXPD_POSTER22C`
- `SWARM_FLAG_B1/B2/B3`
- `SWARM_FLAG_G1/G2/G3`
- `SWARM_FLAG_R1/R2/R3`

## New effect/setpiece caution

- `SPEC_FIREWORK07/08/09` are firework/effect objects. Use for celebration/festival/event scenes, not as structural filler.
- `SET_*` ObjectIDs are newly exposed settlement/setpiece models. Validate before broad generated use.
- `HOLO_DISCO_0` is a Wonder Projector variant and is prohibited for generated builds.

# v51 alien city-canyon part-use candidates

These are toolkit candidates from in-game/reference photo analysis, not hard rules.

## Dense wall/city canyon surfaces

- `B_WALLM`, `B_WALLB`, `B_WALLT`, `B_WALL*_WIN*`
- `F_WALLM`, `F_CHEV_WALL`, `F_WALLM_WIN3`
- `CUBEROOM`, `CUBEGLASS`, `CUBEFRAME`

Use as layered vertical city-canyon walls. Avoid random panel scatter.

## Large monument/spire massing

- `B_ROOF6`, `B_ROOF7`, `B_ROOF8`
- `SET_B_MONU`, `SET_S_TOWER`, `S_TOWER_C`, `B_TOWER_B`

Use as mass contributors and skyline anchors. Do not stack blindly.

## Blade/rib language

- `B_WNG_R`, `B_WNG_R_T`, `B_WNG_R_B`
- `B_WNG_Q`, `B_WNG_Q_R`
- `B_WNG_A`, `B_WNG_A_R`
- `B_DECO_S`

Use as structural ribs/fins/buttresses with explicit load/shape logic.

## Energy / infrastructure lighting

- `BASE_BEAMSTONE`
- `WALLLIGHTBLUE`, `WALLLIGHTPINK`
- `LIGHTFRAME`, `LIGHT_VERT`
- `BASE_NEXUS*`, `BUILDANTIMATTER`

Use as energy seams, portal outlines, gravity shafts, and path infrastructure.

# v55 airlock / iris exact JSON baseline

The uploaded v54 JSON-study recipe library contains an exact airlock/iris extraction.

Baseline recipe:

- `S_GDOOR` x12 at ~30° angular steps for visible iris/garage-door blades.
- `B_FLOOR_Q` x24 at ~15° steps for radial fill ring.
- `B_WALL_Q_H1` x12 for casing/rib layer.
- `F_WALLB_H` x24 for secondary casing layer.

Use this as a geometric reference before attempting 8-sided or 32-sided variants.

# v56 airlock garage-door family parameterization

The airlock/iris recipe is not limited to `S_GDOOR`.

Use any compatible validated `*_GDOOR` / garage-door family part as the shutter/iris blade layer when appropriate:

```text
S_GDOOR
F_GDOOR
B_GDOOR
other *_GDOOR variants where available
```

The extracted `S_GDOOR x12` JSON module remains a control recipe, but future variants may use different part families, counts, scales, radii, and materials depending on whether the target is a tiny aperture, walk-through door, vault seal, or monumental portal.
