# Corvette Validation Checklist v48

Updated: `2026-05-28`

Use this checklist before delivering any Corvette script or build package.

## 1. Scope check

- [ ] User asked for a Corvette, Corvette module, Corvette Workshop, or ship-specific build.
- [ ] `corvette/CORVETTE_KNOWLEDGE_REPOSITORY.md/json` was read.
- [ ] Corvette-only rules were not promoted into ordinary base-building behavior.

## 2. Full library check

- [ ] `library/nms_part_dimensions_and_rules_updated.json` was loaded.
- [ ] The file contains the expected full ObjectID library, not a short whitelist.
- [ ] Corvette candidates were selected from `Category == Corvette` unless intentionally using non-Corvette decorative/base parts.

## 3. Required category check

- [ ] Cockpit present.
- [ ] Access module / landing bay present.
- [ ] Habitation module present.
- [ ] Reactor present.
- [ ] Main engine / thruster present.
- [ ] Weapon system present.
- [ ] Landing gear present.

## 4. Plugin/API probe

- [ ] The script resolves the NMS Builder runtime before deleting anything.
- [ ] Required ObjectIDs are probed with the actual plugin creation path.
- [ ] If any required ObjectID fails, the script stops and writes diagnostics.
- [ ] No fallback proxy geometry is generated.


## 4A. v48 whole-assembly boundary check

- [ ] `corvette/CORVETTE_BOUNDARY_LIMITS.md/json` was read.
- [ ] Boundary audit includes every final placement in the Corvette assembly, including non-Corvette decorative/base parts.
- [ ] Boundary audit does not filter placements by `Category == Corvette`.
- [ ] Final intended Corvette occupied bounds were computed from rotated FBX extents, not centers only.
- [ ] Total X/Y/Z spans are printed in the validation report.
- [ ] Final occupied X span is <= `95.0m`.
- [ ] Final occupied Y span is <= `95.0m`.
- [ ] Final occupied Z span is <= `95.0m`.
- [ ] No part violates `abs(center_axis - origin_axis) + rotated_half_extent_axis <= 47.5m`.
- [ ] Any external/third-party/Blender blueprint over 95m was rejected, shrunk, or redesigned.

## 5. Object validity

- [ ] Every generated placement is a real plugin-created/copied object.
- [ ] No `bpy.ops.mesh.primitive_*` build geometry exists.
- [ ] NMS custom properties are preserved.
- [ ] Runtime object audit runs after generation.

## 6. Searchability

- [ ] Blender object name includes ObjectID.
- [ ] Description/custom properties include ObjectID, NiceName, required category, and role.
- [ ] Cute display names are optional and never replace technical identifiers.

## Delivery rule

If any required category, boundary audit, plugin instantiation, or object audit check fails, do not present the output as an in-game Corvette build. Present it as a failed probe/diagnostic only.

## v44 decorative-use bypass

If Corvette ObjectIDs appear but the build is not intended to be a Corvette:

- [ ] The script/build does not claim to create a valid Corvette.
- [ ] Corvette parts are tagged in the Object Use Manifest as decorative, structural, greeble, lighting, display, architectural, or other non-Corvette roles.
- [ ] Universal generator validation still passes.
- [ ] Part-specific validation for the used Corvette ObjectIDs still passes.
- [ ] Corvette required category checks are skipped intentionally.
- [ ] The output is not presented as a Corvette.

In this decorative-use case, absence of cockpit/reactor/landing gear/etc. is **not** a failure.
