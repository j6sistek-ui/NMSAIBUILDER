# Blender Parity Rule — live Blender builds obey the same law as Python  (introduced 5.00.00)

## Status

**MANDATORY.** A build performed by issuing `BUILDER.add_part()` / transform calls
in a live Blender session is governed by exactly the same procedure and gates as a
generated Python script. There is no "quick Blender build" exemption.

For every live Blender build you MUST:
1. Run `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md` per ObjectID,
2. Emit a `BUILD COMPLIANCE MANIFEST`, and
3. Pass `validation/compliance_manifest_check.py` on it,

before the build is considered valid. Interactivity is not an excuse to skip the
procedure; it is exactly where shortcuts have been taken before.
