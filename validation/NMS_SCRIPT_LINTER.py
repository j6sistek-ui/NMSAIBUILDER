"""
NMS_SCRIPT_LINTER.py

Use this before running any generated script.

Usage:
    python NMS_SCRIPT_LINTER.py generated_script.py

The script FAILS if it uses generic Blender mesh primitives or if it does not
look like a real NMS Base Builder template-copy generator.
"""

from pathlib import Path
import sys
import re

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
    "SnapID",
    "Timestamp",
    "UserData",
    "order",
    "belongs_to_preset",
    "snapped_to",
    "bpy.context.collection.objects.link",
    "nms_runtime_object_audit",
]

SUSPICIOUS = [
    "NMS-style",
    "create_block(",
    "create_cylinder(",
    "create_cone",
    "create_material(",
    "data.materials.append",
    "scene.render.engine",
    "bpy.ops.object.camera_add",
    "bpy.ops.object.light_add",
]

def lint(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    errors = []
    warnings = []

    for tok in BANNED:
        if tok in text:
            errors.append(f"BANNED raw Blender call: {tok}")

    for tok in REQUIRED:
        if tok not in text:
            errors.append(f"Missing required NMS marker: {tok}")

    for tok in SUSPICIOUS:
        if tok in text:
            warnings.append(f"Suspicious generic-Blender pattern: {tok}")

    if "PART_IDS" not in text:
        errors.append("No PART_IDS list found. The script must declare the ObjectIDs it uses.")

    if "NMS_OBJECT_AUDIT_PASS" not in text:
        errors.append("No NMS_OBJECT_AUDIT_PASS runtime audit marker found.")

    print("\n" + "=" * 78)
    print(f"NMS SCRIPT LINTER: {path}")
    print("=" * 78)

    if errors:
        print("RESULT: FAIL")
        for e in errors:
            print("ERROR:", e)
    else:
        print("RESULT: PASS")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print("WARN:", w)

    print("=" * 78)
    return 1 if errors else 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python NMS_SCRIPT_LINTER.py generated_script.py")
        raise SystemExit(2)

    code = 0
    for arg in sys.argv[1:]:
        code |= lint(Path(arg))
    raise SystemExit(code)
