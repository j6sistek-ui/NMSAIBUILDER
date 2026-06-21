# Part Orientation Overrides (v59)

This registry is the single canonical location for validated ObjectID-specific orientation exceptions.

The general `rx=90` convention remains a useful default for many structural/facade pieces, but it is not universal. A part becomes an override only when the evidence chain supports it:

1. FBX/part-library geometry suggests the native axis or plane.
2. Python/Blender placement shows a repeatable discrepancy or success.
3. Exported base JSON confirms the serialized transform.
4. Blender or in-game screenshots confirm the visual outcome.

## Current validated override

### `BILLBOARD` / Station Billboard

`BILLBOARD` is a thin vertical sign plane. Its FBX-derived bounds are approximately X `1.530`, Y `0.278`, Z `2.172`, so the thin axis is local Y and the object should not inherit the generic facade `rx=90` rule in the validated generated-base path.

Canonical rule:

```python
BILLBOARD_RX = 0
BILLBOARD_RZ_BY_SIDE = {
    "N": 0,
    "S": 180,
    "E": 270,
    "W": 90,
}
```

Failure mode: applying generic `rx=90` makes the sign protrude perpendicular to the building like a shelf.

## Governance rule

Do not duplicate this full rule in individual project notes. Scripts and design docs should reference `rules/PART_ORIENTATION_OVERRIDES.md`. If a future project uses `BILLBOARD`, this exception follows the part, not the prior megacity project.
