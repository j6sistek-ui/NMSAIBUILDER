# TRIFLOOR Family Validation Framework — 2.13.00

## Status

Canonical family-validation case study for triangular floor parts and the first broadly controlled part-family proof matrix.

This document consolidates the C_TRIFLOOR study and TRIFLOOR V24 family matrix so future part studies do not lose the placement-learning outcome.

## Scope

TRIFLOOR validation ended at V24.

All later V25-V38 validation history belongs to the stair family and must not be mixed with TRIFLOOR versioning.

## Proven by the TRIFLOOR program

The TRIFLOOR study validated that the master placement framework can handle:

```text
X movement
Y movement
Z movement
rotation
orientation
scale
connectivity
complex geometry generation
closed-shape generation
```

Validated shape/application classes included:

```text
flat patches
diamonds
tetrahedrons
pyramids
octahedrons
advanced closed polyhedra
```

## Core lesson

```text
Placement logic is universal.
Part-specific behavior is data.
```

Future part studies should validate family attributes, not re-prove the general placement engine, unless a new part supplies evidence that the engine fails.

## V24 family matrix

The V24 matrix scanned and generated isolated rows for 14 TRIFLOOR-family variants:

```text
B_TRIFLOOR
B_TRIFLOOR_Q
C_TRIFLOOR
C_TRIFLOOR_Q
F_TRIFLOOR
F_TRIFLOOR_Q
M_TRIFLOOR
M_TRIFLOOR_Q
S_TRIFLOOR
S_TRIFLOOR_Q
T_TRIFLOOR
T_TRIFLOOR_Q
W_TRIFLOOR
W_TRIFLOOR_Q
```

Each row used only one ObjectID and contained:

```text
18 parts: PATCH3X3 flat patch control
16 parts: TETRA4X4 closed-shape control
34 parts per row
476 total real NMS parts
```

The V24 proof was intentionally a family-equivalence matrix, not a final acceptance claim.

## Status after user Blender review

The user reported that all models appeared in good order, with proper orientation and gapping, but flagged the set for in-game final review.

Therefore:

```text
TRIFLOOR V24 family matrix = BLENDER_VALIDATED / PENDING_USER_ACCEPTANCE
No TRIFLOOR variant is USER_ACCEPTED solely because of V24.
```

## Family-equivalence classification options

After in-game review, classify each variant as one of:

```text
SAME_RULE
SAME_RULE_WITH_SCALE_COEFFICIENT
SAME_RULE_WITH_PHASE_OFFSET
SAME_RULE_WITH_PIVOT_OFFSET
MODIFIED_RULE
UNIQUE_OUTLIER
FAIL
```

## Q-variant caution

Q variants are smaller and have distinct geometry. They may use the same rule with a scale coefficient, but they must not be assumed equivalent without review.

## Generalized family-validation workflow

Use this workflow for future part families:

```text
1. Validate one control part.
2. Build a proof matrix that exercises the behavior needed for real builds.
3. Generate isolated rows for family variants.
4. Prevent ObjectID cross-over between rows.
5. Review Blender output.
6. Export/load in-game if required.
7. Classify each family member.
8. Store rule and status in partmap/master sheet.
```

## Reusable directive

The success of V24 means future validation should begin from the master placement algorithm and ask:

```text
What is unknown about this part/family?
```

not:

```text
Does XYZ placement work at all?
```
