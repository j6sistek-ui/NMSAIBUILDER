# Visual Build Toolkit — Airlock / Garage-Door Iris Opening v53

## Classification

**Toolkit technique / part-use candidate.**

This is not a current-project validation photo. It came from a separate in-game video reference, so it is treated as general build-knowledge expansion with possible application to future builds.

## Source

- Video: `download_20260227_170536_0000.mov`
- Retained contact sheet: `visual_library/contact_sheets/AIRLOCK_GARAGE_IRIS_VIDEO_v53.jpg`

## Observed technique

The reference shows a circular/iris-style opening effect using an airlock/door frame and repeated door/shutter/garage-door-like panels arranged radially.

The key lesson:

```text
A circular opening can be built from repeated rectangular/door panels in a radial array.
Increasing panel count makes the circle read smoother.
```

The user note indicates that **32 panels** produce a cleaner/more perfect circular opening than lower-count rings.

## Reusable build applications

Use this technique for:

- alien airlock doors;
- circular vault doors;
- iris portals;
- plasma chamber openings;
- hangar bay seals;
- energy gates;
- ceremonial temple doors;
- sci-fi reactor apertures;
- underwater/space-station pressure doors.

## Candidate NMS parts

Exact ObjectID should be confirmed from the source build/JSON when possible, but the current candidate families are:

| Candidate | Likely role |
|---|---|
| `BUILDDOOR` | airlock / large-structure door candidate |
| `AIRLCKCONNECTOR` | airlock connector/frame candidate |
| `WALLDOOR` | shutter/garage-door-style panel candidate |
| `B_GDOOR`, `F_GDOOR`, `S_GDOOR` families | powered/garage-like door panel candidates |
| `B_DOOR*`, `F_DOOR*`, `S_DOOR*` families | rectangular door/panel substitutes |
| `F_ARCHM`, `B_ARCHM`, `S_ARCHM` | outer architectural frame candidates |
| `BASE_BEAMSTONE`, `WALLLIGHT*` | energy glow, pressure seal, portal seam |

## Orientation principle

For a radial iris:

```text
for each panel i:
    theta = 360 * i / N
    position = center + radius * (cos(theta), sin(theta))
    panel face/or long axis must be oriented consistently around the circle
```

Potential orientation modes:

| Mode | Visual result |
|---|---|
| Tangential panels | panels form a smooth circular rim / shutter edge |
| Radial panels | panels point into the center like iris leaves |
| Alternating tangent/radial | mechanical shutter or gear-like effect |

The correct garage/shutter-door orientation must be validated per ObjectID, because door parts do not all share the same visible front/hinge direction.

## Quality guidance

- Use `N=32` for smoother circular aperture quality when the part budget allows.
- Use `N=16` for medium-quality rings.
- Use `N=8` only for rough octagonal/stylized hatches.
- Keep ring radius and panel scale tied to FBX dimensions, not guessed spacing.
- Avoid heavy overlap that creates flicker.
- If making an animated-looking open/closed sequence, create separate static states or offset rings; NMS build parts do not provide true scripted animation in the generated base.

## Formula sketch

```python
N = 32
for i in range(N):
    theta = math.radians(360 * i / N)
    x = cx + math.cos(theta) * radius
    y = cy + math.sin(theta) * radius
    rz = math.degrees(theta) + tangent_offset  # validate per ObjectID
    place_bottom(DOOR_PANEL_OBJECTID, x, y, z, rz=rz, sc=sc)
```

## Documentation status

- General reusable technique: **captured**
- Exact part IDs: **candidate list only**
- Exact orientation offsets: **not validated yet**
- 32-panel quality recommendation: **user-observed; should be confirmed in Blender/in-game when scripted**
- Current-project impact: may be useful for Alien Megatemple portal/airlock/chamber openings, but not yet incorporated.

## Do not overgeneralize

This does not mean every circular opening should use 32 panels. Use the panel count that fits the part budget and viewing distance.

# v55 JSON-study enrichment — exact airlock / iris recipe baseline

The v54 JSON-study recipe library contains a focused extraction from the `Default` PlayerShipBase / corvette-base airlock module. This upgrades the airlock/iris technique from visual-only candidate to a partially geometry-backed recipe.

## Exact extracted baseline module

Source file:

`MASTER_LESSONS_LEARNED.md` (removed historical reference: archive/json_studies/NMS_JSON_STUDY_Airlock_Iris_Door_interim_findings.md)

Extracted object counts:

| ObjectID | Count | Role |
|---|---:|---|
| `S_GDOOR` | 12 | visible iris/garage-door blade layer |
| `B_FLOOR_Q` | 24 | radial quarter-floor/fill ring |
| `B_WALL_Q_H1` | 12 | structural/casing iris ribs |
| `F_WALLB_H` | 24 | secondary wall/casing layer |
| `U_POWERLINE` | 17 | power/logic visual/network layer |
| `U_SWITCHWALL` | 1 | switch |
| `U_SOLAR_S` | 1 | power source |
| `U_BIOGENERATOR` | 1 | power source |
| `U_BATTERY_S` | 1 | power storage |

## Extracted geometry basis

The visible circular plane is best understood in the source `Y/Z` plane, with `X` functioning largely as depth through the doorway.

| Layer | Count | Radius / step notes |
|---|---:|---|
| `S_GDOOR` | 12 | radius about `2.579`, angular step about `30°`, scale about `0.848` |
| `B_FLOOR_Q` | 24 | radius about `2.981`, angular step about `15°`, scale `0.5` |
| `B_WALL_Q_H1` | 12 | radius about `2.309`, angular step about `30°`, scale `0.5` |
| `F_WALLB_H` | 24 | radius about `2.459`, paired/secondary casing layer, scale `0.5` |

## Updated implementation guidance

Use the extracted 12-blade `S_GDOOR` module as the baseline proven recipe. Treat 8-sided and 32-sided versions as designed variants:

- `8` panels: chunky/octagonal ceremonial hatch.
- `12` panels: extracted/proven source baseline from JSON.
- `24` panels: matches the source filler/casing density.
- `32` panels: high-smoothness experimental iris; should be checked for overlap/flicker and part budget.

## V04 Alien Megatemple relevance

For V04:
- use one side as a lower-density chunky airlock candidate, likely 8 panels;
- use the opposite side as a high-density iris candidate, but compare it to the extracted 12/24-layer baseline rather than guessing from scratch;
- keep the portal integrated into the shell surface, not floating in front of it.

# v56 parameterization correction

The JSON-extracted `S_GDOOR x12` recipe is the baseline/control implementation, not a fixed requirement.

The iris blade layer may use any compatible validated garage-door family part, including:

```text
S_GDOOR
F_GDOOR
B_GDOOR
other *_GDOOR variants where available
```

Part choice depends on:

- desired material/style;
- scale and opening size;
- whether the iris is tiny, walk-through, or monumental;
- available part budget;
- visible face orientation;
- depth and overlap behavior.

Panel count is also variable:

```text
8  = chunky/octagonal
12 = extracted baseline/control
16 = medium smoothness
24 = dense casing/fill reference
32 = smoother high-quality iris
```

Use the extracted JSON frame as a geometric reference, then adapt count, radius, scale, and ObjectID to the design.
