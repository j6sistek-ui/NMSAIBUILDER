# Airlock / Iris Exact JSON Recipe Rule — 1.03.02

## Status

Mandatory for radial airlock / iris-door assemblies when a known-good JSON recipe is available.

## Corrected rule

The known-good airlock recipe is a **direct JSON control recipe**. Do not infer a new per-piece radial orientation model from the circular positions. The generator must preserve the serialized source `ObjectID`, `Position`, `Up`, `At`, scale magnitude, and object count unless the user explicitly requests a controlled transformation.

## Failure being corrected

The 1.03.01 rule incorrectly stated that every `S_GDOOR` blade in the known-good airlock has a unique orientation basis. The working JSON provided for the Batman airlock shows the active pieces are arranged primarily by circular positions while retaining effectively shared `Up`/`At` vectors. V05/V06 failed because the generator inferred a new radial orientation scheme instead of directly reproducing the JSON control.

## Current known-good recipe count

The current control JSON contains 76 objects total, with one zero-position placeholder for each of the four ObjectID families. The active geometric recipe after removing placeholders is:

- `S_GDOOR` ×12 — garage-door/iris blade layer;
- `B_FLOOR_Q` ×24 — circular floor/filler ring;
- `B_WALL_Q_H1` ×12 — rib/casing ring;
- `F_WALLB_H` ×24 — secondary casing/wall layer.

If a script uses all 76 objects, it must state how placeholders are handled. If it uses the 72 active objects, it must state which placeholders were excluded.

## Required implementation

1. Parse the known-good JSON as the source of truth.
2. Count ObjectIDs and confirm the expected recipe count before placement.
3. Recreate the source recipe exactly in the original plane first.
4. Use the documented JSON mapping stack only for JSON→Blender conversion:
   - `COORD_MODE = "XnZY"`
   - `AXIS_MODE = "RIGHT_AT_UP"`
   - `BASE_ROTATION_MODE = "POST_RX90"`
   - `POST_BASELINE_CORRECTION = "LOCAL_Y_180"`
   - `SCALE_MODE = "UP_LENGTH_UNIFORM"`
5. Do not generate new radial `Up`/`At` vectors unless a separate exported-JSON control proves that transformation.
6. For a floor-hatch conversion, first pass the exact vertical/control recreation, then apply a single documented rigid transform and export/compare JSON.

## Prohibited shortcuts

- Do not place `S_GDOOR` as upright wall panels around a ring.
- Do not rotate each blade around its radial angle unless the source JSON does so.
- Do not claim an airlock is validated from Blender appearance alone.
- Do not use a study board with cave/stair/Batmobile context to validate the airlock. The airlock must pass as a single-purpose control first.

## Required gate behavior

A valid airlock-control script must place the expected object count during dry-run validation. A gate output with `placed parts: 0` is a failure, even if syntax and ObjectID extraction pass.


## Parametric recipe stage (absorbed from AIRLOCK_IRIS_PARAMETRIC_RECIPE_RULE)
Status: **active toolkit recipe and generation rule**

## Required protocol references

Any request for an airlock / iris / vault / portal door must route through:

```text
00_START_HERE_CURRENT.md
00_KICKOFF_INTAKE_GATE.md
rules/REQUEST_ROUTER_CHECKLIST.md
rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md
rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md
rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md
toolkit/AIRLOCK_IRIS_PARAMETRIC_GENERATOR_SKELETON.py
rules/SPACING_CONNECTION_SCALE_RULES.md
toolkit/PLACEMENT_RECIPE_LIBRARY.md
```

The response must include a protocol confirmation block stating these were checked.

## Purpose

The known-good airlock JSON proves a radial iris-door concept, not just a one-off 12-sided object.

## Known-good control

The validated 12-sided control uses these active visual part families:

| ObjectID | Count | Role |
|---|---:|---|
| `B_FLOOR_Q` | 24 | radial quarter-floor/fill ring, two placements per side |
| `F_WALLB_H` | 24 | paired casing/support layer, two depth/normal offsets per side |
| `B_WALL_Q_H1` | 12 | structural casing / iris rib layer |
| `S_GDOOR` | 12 | visible iris/door blade layer |

The full source JSON may also include `U_POWERLINE`, `U_SWITCHWALL`, `U_SOLAR_S`, `U_BIOGENERATOR`, `U_BATTERY_S`, and `U_PARAGON`.

## Critical control fingerprint

The first known-good `S_GDOOR` blade has this source fingerprint:

```python
ObjectID = "^S_GDOOR"
Position = [-0.45195436477661133, 1.2649855613708496, 0.025080421939492226]
Up       = [-0.84477698802948, 0.07355525344610214, 0.0010530155850574374]
At       = [-0.08674229681491852, -0.9962308406829834, 0.00010981160448864102]
UserData = 14
```

If an “exact” airlock control script does not match this fingerprint for the same source, it is not the known-good control.

## Failure that must not recur

```text
An airlock iris cannot be generated from radial positions alone.
Every segment must rotate Position, Up, and At together.
```

## Implementation levels

### Level 1 — Exact control recreation

Use literal source ObjectID / Position / Up / At / UserData with fingerprint and ObjectID count audits.

### Level 2 — Extracted feature recipe

Extract aperture center, normal/depth axis, visible circular plane, radius per part layer, depth offset per part layer, scale per ObjectID, angular offset per layer, count multiplier per layer, and material/UserData per layer.

### Level 3 — Parametric generator

Use this when the user asks for 12/24/32/3-sided airlock variants or asks to add an airlock to another build.

## Parametric generation contract

Canonical function form:

```python
place_airlock_iris(
    center,
    normal_axis,
    sides=12,
    radius=None,
    scale=1.0,
    material_userdata=14,
    include_power_logic=False,
    profile="known_good_12_derived",
    part_family="basic",
)
```

For each layer template:

```python
angle = angle0 + i * 2*pi/sides
P_variant  = center + R(angle) @ local_position
Up_variant = R(angle) @ local_up
At_variant = R(angle) @ local_at
```

Do not rotate `Position` without rotating `Up` and `At`.

## Layer profile

| Layer | ObjectID | Count rule | Scale source | Geometry behavior |
|---|---|---:|---|---|
| filler ring | `B_FLOOR_Q` | `2 * sides` | source Up length ≈ 0.5 | two angular/depth offsets per side |
| casing/rib | `B_WALL_Q_H1` | `sides` | source Up length ≈ 0.5 | radial casing ring |
| paired casing | `F_WALLB_H` | `2 * sides` | source Up length ≈ 0.5 | paired depth/normal offsets |
| iris blade | `S_GDOOR` | `sides` | source Up length ≈ 0.848 | visible door blade ring |

## Side-count policy

### 12 sides

Use the known-good control profile directly when possible.

### 24 / 32 sides

Allowed only through parametric generation with radius-mode and chord/overlap validation. Default behavior is **central-pivot overlap-density mode**, not chord-preserving expansion.

```python
chord = 2 * radius * sin(pi / sides)
overlap_density_ratio = control_chord / target_chord
```

For denser iris variants, preserve the known-good control center/pivot and usually preserve the control `S_GDOOR` radius. Let the chord shrink and overlap density increase so the added doors converge to the same center. Only expand radius to preserve the 12-sided chord when the user explicitly requests a larger aperture and the script records `RADIUS_MODE = "EXPAND_RADIUS_KEEP_CONTROL_CHORD"`.

### 3 sides

Treat as a triangular vault-door variant, not a direct airlock copy.

## Required audits

Any generated airlock script must print:

```text
request side count
ObjectID counts
radius per layer
radius_mode
scale per layer
chord per layer
overlap_density_ratio per layer
visible tangential footprint estimate
unique Up/At basis count per radial family
whether Position/Up/At were transformed together
whether exact control or parametric variant was used
```

Hard failure if:

```text
S_GDOOR unique rounded Up/At basis count < min(6, sides) for a radial airlock
all radial pieces share the same Up/At
the script claims exact control but source fingerprint mismatches
the script changes count/side/radius without chord and radius-mode validation
a 24/32+ side variant expands radius to preserve 12-sided S_GDOOR chord without explicit user approval
```

## Required response confirmation

When this rule is used, the response must explicitly include:

```text
Protocol confirmation:
- Request route: AIRLOCK_IRIS_PARAMETRIC_RECIPE or JSON_RECREATION_CONTROL
- Source files checked: [list]
- Exact control used: yes/no
- Parametric variant used: yes/no
- Position/Up/At transformed together: yes/no
- Chord/scale/radius-mode validation included: yes/no
```

## Relationship to JSON study protocol

This airlock rule is the model for future feature learning. Dome shells, spires, rounded objects, vehicle assemblies, and display walls should follow the same lifecycle:

```text
working JSON control
→ exact recreation
→ feature-frame extraction
→ layer table
→ parametric generator
→ variant validation
```


## Relationship to Airlock Iris Parametric Overlap Rule

For 24/32+ variants, also apply `rules/AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md`. The added rule documents the V09 failure and V10 correction: correct orientation alone is insufficient; higher side counts must preserve the central pivot/radius unless a larger aperture is explicitly requested.

## Power layer default exclusion
Power/logic parts that appeared in some source airlock JSON examples are excluded by default.

```text
include_power_logic = False
```

The active visual airlock control remains the 72-object visual assembly. Include power/logic only if the user explicitly requests functional wiring or visible cable/power aesthetics.


## Parametric overlap support (absorbed from AIRLOCK_IRIS_PARAMETRIC_OVERLAP_RULE)
Status: **active supporting rule for `AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE.md`**

## Scope

Applies when generating a parametric airlock/iris/vault/portal door from a validated JSON control recipe, especially variants such as 8, 12, 16, 24, or 32 sided `S_GDOOR` assemblies.

## Control baseline

The known-good 12-sided Batman airlock uses these active visual recipe families:

- `S_GDOOR` x12 — visible iris blades
- `B_FLOOR_Q` x24 — floor/filler ring
- `B_WALL_Q_H1` x12 — structural rib/casing ring
- `F_WALLB_H` x24 — secondary casing/support ring

The validated transform stack remains:

```python
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
```

## Correct higher-count parameterization

For higher side counts, do **not** enlarge the radius merely to preserve the original side-to-side garage-door chord. That creates a larger annulus and breaks the central iris read.

Use **central-pivot overlap-density mode** unless the user explicitly asks for a larger aperture:

1. Preserve the known-good control center.
2. Preserve the known-good `S_GDOOR` radius/source radius unless the request explicitly asks for a larger door.
3. Preserve the known-good scale and local orientation family.
4. Increase angular density: `theta = 2*pi*i / n`.
5. Let the chord shrink as `n` increases. Extra blades should overlap more and converge to the same center/pivot/apex.

The invariant is the central connection/pivot/apex, not side-to-side door spacing.

## Failure example

V09 32-sided airlock used correct part orientation but expanded the radius to maintain the 12-sided chord. User screenshot showed this was only a partial success: the door became a larger ring/annulus rather than a denser iris.

## Corrected example

V10 preserves the 12-sided `S_GDOOR` radius and creates 32 blades at smaller angular increments. The expected result is a smoother circular iris with heavier visual overlap and the same central convergence.

## Valid radius modes

Parametric airlock scripts must record the selected radius mode. Valid default names:

- `KEEP_CONTROL_CENTER_PIVOT_OVERLAP_DENSITY`
- `KEEP_CONTROL_RADIUS_OVERLAP_DENSITY`

Chord-preserving expansion is only allowed if explicitly named and user-approved:

- `EXPAND_RADIUS_KEEP_CONTROL_CHORD`

## Required audit fields

Generated parametric airlock scripts must print or store:

```text
radius_mode
control_sides
target_sides
control_radius per layer
target_radius per layer
control_chord per layer
target_chord per layer
overlap_density_ratio = control_chord / target_chord
whether larger aperture was explicitly requested
whether Position/Up/At were transformed together
```

## Hard failures

Hard fail if:

```text
32-sided or higher-count variant expands radius only to preserve 12-sided S_GDOOR chord without explicit user approval
script omits radius_mode
script changes count/radius/scale without reporting chord and overlap-density numbers
script rotates Position without rotating Up and At together
```
