# Stair Placement Doctrine — 2.13.00

## Status

Canonical stair-family placement doctrine derived from stair validation V25-V38.

V38 remained pending final user/in-game acceptance at the time of this release, but the core stair-placement doctrine below is locked by repeated user review and V35/V36 placement success.

## Version boundary

Stair validation begins after TRIFLOOR V24.

Do not treat V25-V38 as triangle revisions. These versions belong to the stair validation branch.

## Core discovery

Stairs are a worst-case placement family because they combine:

```text
slope
origin offset below/inside the visual stair body
floor landing offsets
stair-to-stair local-frame repetition
terminal landing behavior
90-degree turns
multi-row corner blending
AABB float-gate false positives
```

Most stair failures were not caused by the universal placement algorithm. They were caused by part-specific attributes:

```text
orientation
origin
rotation direction
edge offset
landing relationship
corner anchor behavior
```

## Local-frame stair repeat rule

Actual-base JSON evidence established that ramp chains repeat in the part's local frame:

```text
Position[n+1] =
    Position[n]
    + At * RUN_STEP
    + Up * RISE_STEP
```

Observed calibration:

```text
RAMP_RUN_STEP  ≈ 5.33334
RAMP_RISE_STEP ≈ 3.33333
STAIR_CONTACT_TUNE = 0.985
RUN_STEP  = RAMP_RUN_STEP  * STAIR_CONTACT_TUNE
RISE_STEP = RAMP_RISE_STEP * STAIR_CONTACT_TUNE
```

This produces the effective stair lattice step:

```text
RUN_STEP  ≈ 5.2533
RISE_STEP ≈ 3.2833
```

## Floors anchor / stairs move

Locked rule:

```text
Floors are anchors.
Stairs move.
```

Never:

```text
Move floors to fix stairs.
Add extra floor pads to satisfy a float gate.
Compress floor layouts to hide stair issues.
Shift floor grids after floor layout is accepted.
```

The correct response to stair misalignment is to adjust the stair rule, not to corrupt the floor grid.

## Locked stair edge formula

The accepted stair-to-floor edge rule is:

```text
EDGE_START_BASE =
    FLOOR_HALF
    + RAMP_HALF_DEPTH
    - SMALL_OVERLAP
```

With:

```text
SMALL_OVERLAP = 0.10
EDGE_START_PRIMARY = EDGE_START_BASE
```

Meaning:

```text
The stair begins at the floor edge.
The stair does not begin at floor center.
The stair is not placed halfway across the floor.
```

## Landing behavior

A top or bottom floor may visually overlap/cover the stair slightly. This is not automatically a failure.

The stair-to-stair local-frame repeat is the primary chain-spacing rule. Floor connection is a landing tolerance and must be interpreted semantically for stair families.

## Switchback result

The switchback staircase demonstrated:

```text
floor -> stair
stair -> stair
stair -> landing
90-degree turn
multi-floor traversal
single landing floors only
no useless companion floor pads
```

At the 2.13.00 consolidation point, this behavior is:

```text
SCRIPT_VALIDATED
BLENDER_VALIDATED
PENDING_USER_ACCEPTANCE
```

## Stadium result

The stadium branch demonstrated:

```text
straight side banks: successful
back bank: successful
45-degree corner placement: mostly successful
blended corner refinement: V38 pending review
```

The final unresolved issue at V38 is corner blending review, not the base stair-edge or local-frame stair repeat rule.

## Current acceptance status

```text
Stair family = SCRIPT_VALIDATED / BLENDER_VALIDATED / PENDING_USER_ACCEPTANCE
V38 user/in-game review = pending
Semantic float-gate adoption = pending
```

## V38-V40 review outcome and validation reporting lesson

### V38 outcome

User review after 2.13.00 established:

```text
Switchback staircase: visually intact / solid execution.
Base stair placement logic: good.
Stadium blended U-corner: not accepted; requires further iteration.
```

V38 therefore validated the core stair repeat and edge-placement logic, but not the multi-row blended-corner anchoring algorithm.

The V38 corner failure mode:

```text
middle rows stayed anchored to the expected true 45-degree angle
outer rows snapped/read as side-piece continuations
large gap remained between middle and outer rows
U-shape connectivity was not achieved
```

### V39 lesson

V39's connectivity-first contact-band approach significantly improved the stadium condition, but it still had:

```text
middle rows overlapping too much
remaining upper gaps
four-row corner geometry too constrained for full closure
```

Do not promote V39 as accepted.

### V40 candidate

V40 moved to a five-lane fan-spaced corner candidate:

```text
one true 45-degree center lane
distinct angles for every lane
reduced middle-row stacking
better closure direction
```

This is a validation candidate only until user/game review confirms it.

### Float-gate reporting rule for stairs

The stair branch must continue to run the raw float gate.

```text
Raw AABB PASS -> report PASS with gate scope.
Raw AABB FAIL -> report FAIL with gate scope.
Temporary stair continuation -> separate allowance, not a pass.
Semantic stair override -> not adopted unless explicitly updated.
```

Known context:

```text
V38 full stair matrix raw float gate failed on the isolated final switchback landing.
Later stadium-only/corner-only matrices may pass because the known switchback outlier is excluded.
That is a scope change, not proof that the family float issue is solved.
```


## V42 normal full-ramp acceptance

User visual review of V42 established that, for general placement and use-case validation, the normal full-ramp stair family is accepted.

Accepted scope:

```text
B_RAMP
C_RAMP
F_RAMP
M_RAMP
S_RAMP
T_RAMP
W_RAMP
```

Validated behavior:

```text
vertical multi-stair chaining
switchback staircase traversal
floor -> stair
stair -> stair
stair -> landing
90-degree turns
stadium side/back banks
five-lane U-corner fan distribution
general placement/use behavior for normal full ramps
```

The accepted stair rule remains:

```text
floors are anchors
stairs move
EDGE_START_PRIMARY is unchanged
Position[n+1] = Position[n] + At * RUN_STEP + Up * RISE_STEP
```

This acceptance does not promote half-ramp/half-stair variants. Half ramps are the next validation carry-over target.

## stair-family float-gate status

The project now adopts a scoped semantic float-gate allowance for normal full-ramp stairs only.

Required reporting remains:

```text
Raw generic AABB float gate: PASS/FAIL exactly as run
Gate scope: stated explicitly
Stair semantic connection: PASS/FAIL/NOT_RUN
Temporary continuation: separate if needed
```

Adopted scope:

```text
normal full-ramp stair/floor relations using the documented stair local-frame rule
```

Not adopted for:

```text
non-stair parts
unvalidated half ramps
unvalidated special ramps
global AABB tolerance relaxation
```

All non-stair parts must continue to strictly conform to the generic float-gate rule.


## Corner-transition algorithms (absorbed from CORNER_TRANSITION_ALGORITHMS)
## Status

Canonical taxonomy for multi-row stair/ramp corner transitions.

Derived from the stadium stair validation branch, especially V37/V38.

## Problem

A 90-degree turn with multiple stair lanes can be represented in different ways. Treating every lane as a single hard 45-degree diagonal can work as a chamfer, but it may produce uneven visual overlap or gaps when lanes are distributed across a wide structure.

Therefore, corner style must be explicit.

## Chamfered corner

All lanes use the true corner angle.

For a 90-degree turn:

```text
lane 0 = 45 degrees
lane 1 = 45 degrees
lane 2 = 45 degrees
lane 3 = 45 degrees
```

Use this when a hard diagonal transition is desired.

## Blended corner

Center lane(s) stay at the true corner angle.

Outer lanes interpolate toward the adjacent straight banks.

For a four-lane left corner:

```text
lane 0 = 157.5 degrees
lane 1 = 135.0 degrees
lane 2 = 135.0 degrees
lane 3 = 112.5 degrees
```

For a four-lane right corner:

```text
lane 0 = 22.5 degrees
lane 1 = 45.0 degrees
lane 2 = 45.0 degrees
lane 3 = 67.5 degrees
```

## General blended rule

For an even lane count:

```text
two center lanes = true center angle
outer lanes interpolate toward side/back half-angles
```

For an odd lane count:

```text
one center lane = true center angle
outer lanes interpolate toward side/back half-angles
```

## Implementation notes

The V38 algorithm keeps the middle lanes anchored to the V37 true-corner position and adjusts outer-lane angles. This preserves known-correct middle placement while creating a U-shaped blended transition.

## Documentation distinction

Do not collapse chamfered and blended corners into one rule.

They are both valid, but they produce different structures and must be selected intentionally.

## post-V38 refinement lessons

V38 proved that angle interpolation alone is not enough for multi-row U-corner connectivity.

Failure mode:

```text
center lanes remained true corner angle
outer lanes interpolated toward side/back banks
but lane anchors were still not connectivity-solved
visible gaps remained between middle and outer rows
```

V39 improved the condition by moving from an angle-first fan to a connectivity-first contact band, but four rows still produced excessive middle overlap and remaining upper gaps.

V40 introduced a five-lane fan-spaced candidate:

```text
odd lane count
one center lane at the true corner angle
outer lanes use distinct fan angles
middle duplicate overlap is reduced
```

Current rule:

```text
Chamfered corner = all lanes true corner angle.
Blended corner = center lane(s) true corner angle and outer lanes adjusted.
Connectivity-first corner = solve lane anchors/contact band first, then angle.
```

Do not promote any blended/fan corner to accepted until visual/user/game review confirms real U-shape continuity.


## V42 accepted normal stair U-corner pattern

V42 user review accepted the five-lane equal-step fan for normal full-ramp stair stadium/U-corner placement.

Accepted five-lane equal-step pattern for a 90-degree U-corner:

```text
t positions: 0.00, 0.25, 0.50, 0.75, 1.00

right side angles: 15°, 30°, 45°, 60°, 75°
left side angles: 165°, 150°, 135°, 120°, 105°
```

Use conditions:

```text
normal full-ramp stairs
wide U-corner / stadium-style transitions
floors remain fixed anchors
one center lane remains the true corner lane
outer lanes distribute the 90-degree turn evenly
```

This pattern is accepted for normal full-ramp stairs. Half-ramp variants must be validated separately before inheriting the rule.
