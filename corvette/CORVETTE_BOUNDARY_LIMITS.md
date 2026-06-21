# Corvette Boundary Limits v48

Updated: `2026-05-28`

This is a **Corvette-only constraint file**. It exists because the Swarm-era update/community warning indicates that large Blender/third-party Corvette blueprints can now be clipped, cut up, or invalid if they exceed the Corvette build boundary.

## Source status

- **User-provided evidence:** screenshot of a Reddit warning posted 2026-05-28 showing a Corvette build-boundary visualization and reporting a new boundary limit around **100m** / a little under **330 ft**.
- **User correction v48:** the boundary applies to the **entire finished Corvette assembly**, not only objects whose library `Category == Corvette`.
- **Official context:** Swarm / 6.40 patch notes include Corvette-adjacent stability/performance work, including a fix for crashes rendering thumbnails for multiple complex Corvette-class starships and broader complex-scene object-visibility optimisations.
- **Verification level:** Treat the exact 100m value as a **strict conservative operating rule** until superseded by direct in-game measurement or explicit official documentation.

## Hard rule

For any build intended to become or remain a functional in-game Corvette:

```text
CORVETTE_ABSOLUTE_BOUNDARY_SIDE_M = 100.0
CORVETTE_SAFE_BOUNDARY_SIDE_M     = 95.0
CORVETTE_SAFE_HALF_EXTENT_M       = 47.5
```

A generator must check the **occupied rotated bounding box of the entire Corvette assembly**, not just part-center positions and not just Corvette-category parts.

```python
abs(part_center_axis - corvette_origin_axis) + rotated_half_extent_axis <= 47.5
```

If a generated Corvette exceeds the 95m safe side-length envelope on X, Y, or Z, the script must fail validation or redesign the ship. Do not deliver the output as a usable Corvette.

## Category-agnostic Corvette assembly rule

Corvettes can be decorated with non-Corvette/base/decorative parts. Therefore, once the target build is a Corvette, the boundary audit must include **every generated placement in the Corvette assembly**, regardless of library category.

Include all of the following in the Corvette occupied-bounds calculation:

- required Corvette core modules;
- Corvette hull plating, windows, wings, shields, storage, and utility modules;
- non-Corvette exterior decorations mounted on the Corvette;
- non-Corvette interior decorations, furniture, utility props, greebles, lights, signs, decals, pipes, plants, or kitbash elements placed on/in the Corvette;
- any helper/scaffold/template object that remains in the final exported Corvette.

Do **not** include objects that are only temporary generation templates, deleted scaffolds, external scene labels, debug grids, or reference markers that are not part of the final Corvette export.

## Absolute maximum

The screenshot/community report describes a boundary around 100m. Therefore:

- **95m side length** = generator-safe envelope for the final Corvette assembly.
- **100m side length** = absolute redline, not a design target.
- Any final Corvette placement exceeding **±50m including half-extents** from the Corvette origin is invalid.
- Any final Corvette placement exceeding **±47.5m including half-extents** from the Corvette origin fails the safe-generator rule.

## Required generator behavior

Every future Corvette script must include a boundary audit that:

1. collects **all final placements in the Corvette assembly**, regardless of ObjectID category;
2. loads or stores FBX extents for every used ObjectID;
3. multiplies extents by scale;
4. maps extents through the part rotation/orientation into world axes;
5. computes per-part min/max world bounds;
6. computes total build min/max bounds;
7. rejects output if any total axis span exceeds `95.0m`;
8. prints the final X/Y/Z span in the validation report;
9. identifies which ObjectIDs caused any boundary violation.

Center-only validation is invalid because a large module can have a legal center and still exceed the boundary after its half-extent is included.

Category-filtered validation is invalid for Corvette builds because non-Corvette decoration can still push the functional ship outside the Corvette boundary.

## Conversion rule for external / third-party Corvette blueprints

Large Corvette blueprints from Blender, save editors, or third-party tools must be treated as high risk after this update.

Before importing or recommending any external Corvette blueprint:

- calculate the final occupied dimensions of the whole ship, including non-Corvette decorations;
- reject, shrink, or redesign anything over 95m side length;
- do not assume prior pre-update oversized ships remain safe;
- warn that ships near the old boundary may be bugged, clipped, or cut apart in-game.

## Scope firewall

This rule is **Corvette-mode only**, but within Corvette mode it applies to the **entire final build footprint**.

Apply it to:

- functional Corvette builds;
- Corvette Workshop module layouts;
- Corvette exterior decoration passes;
- Corvette interior decoration passes;
- Blender/save-editor/third-party blueprints intended for Corvette use;
- any non-Corvette part placed on, in, or as part of a Corvette.

Do not apply the 95m/100m Corvette boundary to:

- planetary bases;
- freighter bases;
- megacities;
- Taj Mahal / landmark builds;
- Jurassic/organic scenes;
- decorative architecture;
- ordinary NMS base scripts using Corvette parts as greebles or decoration when the output is not a Corvette.

Those builds still use their own base-complexity and object-placement constraints.

## Design impact

Future Corvette design should prefer:

- compact 60–85m ships;
- one-deck or low-profile multi-zone layouts;
- purposeful module density rather than long empty beams;
- visible silhouette within the safe envelope;
- no stretched or oversized proxy geometry;
- role-specialized builds instead of massive everything-ships;
- decoration that stays inside the same final 95m occupied envelope as the ship core.

For large cultural/novelty ship replicas, the correct response is now to **miniaturize the silhouette**, not exceed the Corvette envelope.
