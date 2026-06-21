"""
NMS_VALIDATE_TEXT_BLOCKS_IN_BLENDER.py

Run this in Blender BEFORE running a generated build script.

It scans all open Text Editor scripts and reports any file that contains
forbidden raw Blender mesh/scene calls. If the generated script fails this
validator, do not run it.
"""

import bpy

BANNED = [
    "bpy.ops.mesh.primitive_cube_add",
    "bpy.ops.mesh.primitive_plane_add",
    "bpy.ops.mesh.primitive_cylinder_add",
    "bpy.ops.mesh.primitive_cone_add",
    "bpy.ops.mesh.primitive_uv_sphere_add",
    "bpy.data.meshes.new",
    "bpy.data.objects.new",
    "bpy.ops.object.select_all(action='SELECT')",
    "bpy.ops.object.delete",
]

REQUIRED = [
    "bl_ext.user_default.no_mans_sky_base_builder",
    "BUILDER.add_part",
    ".copy()",
    "ObjectID",
    "Timestamp",
    "UserData",
    "belongs_to_preset",
    "bpy.context.collection.objects.link",
]

failed = False

for txt in bpy.data.texts:
    source = txt.as_string()
    if not source.strip():
        continue

    banned_hits = [tok for tok in BANNED if tok in source]
    if banned_hits:
        failed = True
        print(f"FAIL: {txt.name} contains banned raw Blender calls:")
        for hit in banned_hits:
            print(f"  - {hit}")

    # Only warn on required markers because non-build helper files may not need them.
    if "BUILDER.add_part" in source or "primitive_" in source or "NMS" in txt.name.upper():
        missing = [tok for tok in REQUIRED if tok not in source]
        if missing:
            print(f"WARN: {txt.name} may not be a valid NMS generator. Missing:")
            for miss in missing:
                print(f"  - {miss}")

if failed:
    raise RuntimeError("NMS validation failed. Do not run the generated build script.")
else:
    print("NMS validation complete: no banned raw primitive calls found in open Text blocks.")
