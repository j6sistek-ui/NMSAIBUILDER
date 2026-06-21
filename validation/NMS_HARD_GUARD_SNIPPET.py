"""
NMS_HARD_GUARD_SNIPPET.py

Paste this near the top of any generated NMS script, immediately after imports.
It does not replace the required NMS template, but it helps catch invalid
generic Blender-mesh scripts before they run.
"""

BANNED_NMS_SCRIPT_TOKENS = [
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

def nms_guard_validate_source(source_text):
    hits = [tok for tok in BANNED_NMS_SCRIPT_TOKENS if tok in source_text]
    if hits:
        raise RuntimeError(
            "INVALID NMS SCRIPT: raw Blender mesh/scene calls found: "
            + ", ".join(hits)
            + ". Rewrite using BUILDER.add_part templates."
        )

# Validate the current Text block if Blender exposes it.
try:
    import bpy
    active_text = getattr(getattr(bpy.context, "space_data", None), "text", None)
    if active_text is not None:
        nms_guard_validate_source(active_text.as_string())
except NameError:
    pass
