# Continuous Path Assembly Rule (v59)

This is a general reusable build rule, not a megacity-only rule.

Use it for any bridge, tube, pipe, cable, rail, corridor, conveyor, or repeated connector assembly that spans between endpoints.

## Rule

Generate the assembly as one continuous path system:

1. Compute face/socket endpoint A.
2. Compute face/socket endpoint B.
3. Derive one 3D path vector and path basis.
4. Place every connector, glass sleeve, ring collar, adapter, rail, and socket in that same path basis.
5. Repeat modules along the normalized vector with slight overlap.
6. Only apply per-part yaw/pitch offsets after the ObjectID's native axis has been validated.

## Why

V10/V11 skybridge tests showed that position-only alignment is insufficient. Parts can sit along a bridge line while their local axes still point sideways, producing staggered steps, crosswise glass, or disconnected-looking modules.

## Validation

For path assemblies, screenshot review is not enough. Export the generated build JSON and compare:

- intended endpoint coordinates from Python,
- serialized positions in JSON,
- serialized rotations in JSON,
- ObjectID-specific local axis assumptions,
- in-game visual continuity.
