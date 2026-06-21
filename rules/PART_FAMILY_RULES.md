# NMS Part Family Rules

*Updated 2026-05-25. Load this with the master reference before scripting.*

The purpose of this file is to prevent repeated placement mistakes by turning validated lessons into reusable part-family rules.

## Rule hierarchy

1. Universal workflow rules
2. Part-family rules
3. Part-specific rules
4. Project-specific rules
5. Unvalidated hypotheses

## SHORT_WALL_TRIM_RING

Validated issue: `S_WALL_Q_H1` and related stone trim pieces can have correct tangent orientation while still showing gaps. The fix is chord-spacing math.

```text
chord = 2 * radius * sin(pi / count)
target_chord <= visible_tangential_length * 0.96
```

Horizontal ring orientation starting point:

```python
rz = angle + 90
```

Validated stone bases:

| Part | Visible tangential length basis |
|---|---:|
| `S_WALL_Q` | `5.835 * scale` |
| `S_WALL_Q1` | `5.835 * scale` |
| `S_WALL_Q_H` | `3.063 * scale` |
| `S_WALL_Q_H1` | `3.063 * scale` |

Likely same-behavior candidates include metal, concrete, wood, timber, alloy, and salvaged `*_WALL_Q*` short-wall families. Use each part's own FBX extent and validate before promoting.

## B_SHL_E_RED_LENS_EFFECT

`B_SHL_E` is the Aeron Powershield and is the red glow/lens source. `B_DECO_P` is the Radar Dome core and is not the red glow source.

Use `B_SHL_E` as a framed/recessed lens, not an exposed repeated ornament. Best current application: tower/skyscraper crown or façade band. Promising: ceiling reactor oculus and simplified wall iris.

## TURRET_ABAND_BEAM_PROJECTOR

`TURRET_ABAND` is valuable for in-game orange/pink beam and triangular fan effects. Blender does not show the effect. Hide/anchor the body and use it as a projector node.

## TITAN_HEAVY_BOOSTER_ELECTRICITY

`B_WNG_A` / Titan Heavy Booster is the confirmed source of temporary blue electricity/glitch FX. It can be buried inside geometry. Do not substitute other booster parts if the electricity is required.

## AERON_BLADE_CONE_OCULUS

`B_WNG_R_T` D5 n=192 is locked. Wide `B_WNG_R` W3 and W7 are locked options with part-budget tradeoffs. Preserve V25 core variants unless explicitly changed.


## MACRO_WALL_SHELL_AND_FACADE_OVERLAYS

**Status:** rule

When using one large wall panel as a macro shell, all facade overlay parts must
be positioned from the scaled visible face of that wall.

- Compute `scaled_depth = native_depth * wall_scale`.
- Move overlays outward from building center, not by memorized sign.
- Front/stair wall outward: `-Y`.
- Back wall outward: `+Y`.
- Left wall outward: `-X`.
- Right wall outward: `+X`.
- Recompute offsets whenever the wall scale changes.
- Do not preserve overlay offsets from the previous wall system.

This rule was added after a prior macro-wall cleanup moved overlays the wrong direction after the
scale-6 macro wall replacement.

## Full machine-readable registry

See `MASTER_LESSONS_LEARNED.md` (removed historical reference: NMS_Part_Family_Rules.json).


---

## ORIGIN_BOUNDS_PLACEMENT

**Status:** universal placement rule

Object location is the Blender object origin, not guaranteed visual center. Many NMS parts need bottom/top placement helpers after the standard `rx=90` orientation.

Use FBX extents and centers:

```python
bottom_rel = (center_y - extent_y / 2) * scale
top_rel    = (center_y + extent_y / 2) * scale
origin_z_for_bottom = visible_bottom_z - bottom_rel
origin_z_for_top    = visible_top_z - top_rel
```

Do not hand-place rows by assumed center origin unless that part's bounds prove it.

## CONNECTED_TRIM_AND_ROW_RUNS

**Status:** universal continuity rule

A row, band, or trim run named "continuous" must actually touch/overlap from the viewer angle.

Validated fix:

```python
part_len = visible_native_length * scale
step = part_len * (1.0 - overlap)
```

Use overlap for rows and explicit end/corner closure pieces where required. If a separated accent is intentional, name it separated/accent trim, not continuous trim.

## GRAND_ARCH_HALF_ARCH_FACADE_STRUCTURES

**Status:** validated design-family rule

For grand landmark facades, scale and connected architecture often matter more than many small details. Prefer 10-20 purposeful, properly scaled parts over dense cylinder/detail fields when the structure is large.

Recommended architectural vocabulary:

- full arches stacked vertically for side bays
- mirrored oversized half arches overlapped into one grand central iwan/opening
- broad wall backing so arches read as structure, not loose decoration
- angled arch returns that disappear into building mass to create depth
- trim only when connected or clearly intentional as separate accents

Do not substitute relief walls or busy detail fields into an exact user-requested arch/half-arch study unless providing a separate interpretive option.

## DOME_SURFACE_ORIENTED_WALL_SHELLS

**Status:** validated method pattern

When using wall/half-wall parts to form a dome or shell, do not place them as vertical cylinder bands. Treat each panel as a surface tile:

- local X = tangent around the ring
- local Y = meridian / surface-up direction
- local Z = outward normal

Ring count should follow the silhouette radius and chord spacing. For a dome/onion/sphere form, counts can be high near the belly and taper toward the top.

## SCALE_OVER_QUANTITY_FOR_GRAND_STRUCTURES

**Status:** design rule

Some builds require micro detail. Grand landmark buildings generally require strong macro silhouette, correct scale hierarchy, and connected architectural masses first. Small face details can disappear visually while still costing parts.

Use larger scaled parts for primary recognition features. Add micro detail only after the silhouette and major architectural read are correct.


## HALF_ARCH_MIRRORING_AND_HANDEDNESS

Half arch parts such as `S_ARCH_H` and variants (`S_ARCHB_H`, `S_ARCHM_H`, `S_ARCHT_H`) are handed. Mirroring them across a centerline is not only a position change; orientation must be explicitly corrected per facade direction. Verify that open arch portions face inward and pull overlays outward from macro wall faces so the half arches are not consumed by wall depth.

Initial front/rear calibration from the corrected facade branch:

```python
# front/South, arch_rz = 0
left_half_rz  = arch_rz + 180
right_half_rz = arch_rz

# rear/North, arch_rz = 180
left_half_rz  = arch_rz
right_half_rz = arch_rz + 180
```

Side facades require separate calibration before use.


## SURFACE_ORIENTED_DOME_WALL_PANELS

Wall or half-wall panels used as dome shells must be placed as surface tiles, not vertical cylinder rings. Use tangent/meridian/normal orientation and chord-based ring counts. If panels still read too vertical, use a controlled profile-derivative tilt gain.

## DEEP_SEA_ROOM_SKYSCRAPER_TOPPERS
**Status:** validated design-family pattern from skyscraper/topper studies.

Primary parts:

- `MAINROOM_WATER` — circular deepwater chamber
- `MAINROOMCUBE_W` — square deepwater chamber

Use them as macro rooftop fabric:

- roof adapters / top floors;
- penthouse blocks;
- circular rotundas;
- square docking pods;
- skybridge sockets;
- machine rooms;
- multi-color skyline caps.

Rules:

- do not only stack rooms vertically;
- create distinct silhouettes through offsets, pods, overhangs, asymmetry, bridges, receivers, cranes, dishes, and layered modules;
- attach antennas/spires to visible mounts or room tops;
- use color deliberately for district/function identity;
- add micro-detail only after the macro room silhouette is clear;
- avoid repeating red lens band + antenna crown + stacked room as the default topper pattern.

`MAINROOM_WATER` and `MAINROOMCUBE_W` are structure, not decoration. They should carry the topper mass.

## MACHINE_AUTOMATION_AND_ROBOTIC_GANTRY
**Status:** study-derived design-family rule.

Primary parts:

- `B_ROBOTARM`
- `ROBOTICARM`
- `BASE_ROBOTOY`
- `BLD_CRYS_DRONE`
- `B_WALL_CARG1`
- `SERVERBOX1`, `SERVERBOX2`, `SERVERSTACK`
- screen/display families

Rules:

- robotic arms need visible mounts and a target task;
- conveyor/cargo parts must read as cassettes, rails, racks, or machine modules, not random barrels;
- orient repeated conveyor modules consistently and name their function;
- drone hive elements must connect to a docking ring, service collar, wall rack, or visible bay;
- sparse "robot parts on a pad" is a failed concept thumbnail, not a finished study.

## GROUNDED_SIGNAL_AND_ANTENNA_CROWNS
**Status:** study-derived issue/fix rule.

Antennas and spires must be physically mounted unless the design is explicitly a floating hologram.

Rules:

- add a pylon, equipment block, room cap, scaffold, or tower top before the antenna;
- do not place antennas high in the air with no connector;
- antenna crowns must have a named function: broadcast, scanner, docking guidance, defense, weather, relay, or AI-control signal;
- if many antennas are used, vary height and role but keep them structurally connected.


## TRIFLOOR_TRIANGLE_SURFACE_TILES

**Status:** single-part validated; family expansion pending.

`C_TRIFLOOR` is validated for phase-resolved triangular face placement and enclosed equilateral triangular solids.

Validated C_TRIFLOOR facts:

```text
phase_A = 150.0014 degrees
phase_B = 30.001369 degrees
origin_type = centroid/face placement for tiling
validated shapes = PATCH3X3, TETRA4X4, OCTA4X4, BIPYRAMID4X4, ICOSA4X4
```

Do **not** inherit this rule to `C_TRIFLOOR_Q`, `F_TRIFLOOR`, or `F_TRIFLOOR_Q` until each part passes family equivalence validation. `C_TRIFLOOR_Q` is specifically marked distinct/unvalidated because its FBX extents and center differ.

## Validated snap-placement family rules (promoted)

- TRI family join (M/C/W/F/S/T TRIFLOOR): same-material triangle join is At 60 deg apart, Up=(0,1,0) both,
  |offset| ~3.079; 6/7 materials identical. Status: validated (snap).
- B_TRIFLOOR (Salvaged) is NOT in the TRI snap group -> no triangle snap points -> misfires to coincident
  overlap. Status: validated exception. Fix: use other TRI materials or place manually.
- SELECT SNAP POINTS BY NAME (connectivity), never by nearest world position; parts carry co-located
  orientation/quarter variants. Status: validated. Affects: all snap-group families.
- Placement composition: B_world = A_world @ Ma @ FLIP @ inv(Mb), FLIP=180 deg about Y. Status: validated.
  See AUTHORITATIVE_SNAP_PLACEMENT_PROTOCOL.md.
