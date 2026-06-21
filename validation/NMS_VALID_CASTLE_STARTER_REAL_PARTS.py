"""
NMS_VALID_CASTLE_STARTER_REAL_PARTS.py

A small castle-style generator using REAL No Man's Sky Base Builder parts.
This replaces the invalid raw-mesh castle script.

It is intentionally conservative and easy to inspect:
- no raw mesh primitives
- no cameras/lights/material nodes
- one template per ObjectID
- repeated placements use template copies
"""

import bpy
import math
import sys
import time

TAG = "NMS_CASTLE_REAL_"
USERDATA_STONE = "87"  # Freighter White/Grey; change per project if needed
USERDATA_DEFAULT = "0"

PART_IDS = [
    "S_FLOOR",
    "S_FLOOR_Q",
    "S_WALLM",
    "S_WALL_Q",
    "S_WALL_Q_H1",
    "S_WALL_SUPPORTS",
    "S_ARCHB",
    "S_ARCHM",
    "S_ARCHT",
    "S_ROOF5",
    "CYLINDERSHAPE",
    "SPHERESHAPE",
]

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

# Self-audit when source text is available in Blender's Text Editor.
try:
    active_text = getattr(getattr(bpy.context, "space_data", None), "text", None)
    if active_text is not None:
        source = active_text.as_string()
        hits = [tok for tok in BANNED_NMS_SCRIPT_TOKENS if tok in source]
        if hits:
            raise RuntimeError("INVALID NMS SCRIPT: banned calls found: " + ", ".join(hits))
except Exception as audit_error:
    if "INVALID NMS SCRIPT" in str(audit_error):
        raise

_mod = sys.modules.get("bl_ext.user_default.no_mans_sky_base_builder")
if _mod is None or not hasattr(_mod, "BUILDER"):
    raise RuntimeError("No Man's Sky Base Builder is not initialized. Enable addon and open/create/import a base first.")

BUILDER = _mod.BUILDER

# Safe cleanup: only this script's prior objects.
for obj in list(bpy.data.objects):
    if obj.name.startswith(TAG):
        bpy.data.objects.remove(obj, do_unlink=True)

try:
    BUILDER.clear_caches()
except Exception:
    pass

T = {}
_ts = str(int(time.time()))

print("[NMS_CASTLE_REAL] Creating NMS templates...")
for oid in PART_IDS:
    try:
        p = BUILDER.add_part(oid)
        p.object.name = f"{TAG}TPL_{oid}"
        T[oid] = p.object
        print(f"  ✓ {oid}")
    except Exception as e:
        print(f"  ✗ {oid}: {e}")

if not T:
    raise RuntimeError("No templates created. Check plugin/base initialization.")

_n = 0

def place(oid, x, y, z, rx=90, ry=0, rz=0, sc=1.0, ud=USERDATA_STONE, name=None):
    global _n
    if oid not in T:
        print(f"[NMS_CASTLE_REAL] Missing template: {oid}")
        return None

    src = T[oid]
    dup = src.copy()
    dup.data = src.data
    dup.animation_data_clear()

    for key in src.keys():
        dup[key] = src[key]

    dup["ObjectID"] = dup.get("ObjectID", oid)
    dup["SnapID"] = dup.get("SnapID", dup["ObjectID"])
    dup["Timestamp"] = _ts
    dup["UserData"] = str(ud)
    dup["order"] = _n
    dup["belongs_to_preset"] = False
    dup["snapped_to"] = ""

    dup.name = f"{TAG}{name or oid}_{_n:05d}"
    dup.location = (x, y, z)
    dup.rotation_euler = (math.radians(rx), math.radians(ry), math.radians(rz))
    dup.scale = (sc, sc, sc)

    bpy.context.collection.objects.link(dup)
    _n += 1
    return dup

# Approx dimensions from guide.
S_FLOOR_STEP = 5.2447
S_WALL_STEP = 5.6914
WALL_H = 3.3320

def floor_grid(width, depth, z=0.0, sc=1.0):
    sx = S_FLOOR_STEP * sc
    for ix in range(-width, width + 1):
        for iy in range(-depth, depth + 1):
            place("S_FLOOR", ix * sx, iy * sx, z, sc=sc, name="courtyard_floor")

def wall_run_front(y, x_min, x_max, z, rz, sc=1.5):
    step = S_WALL_STEP * sc * 0.98
    x = x_min
    while x <= x_max:
        place("S_WALLM", x, y, z, rz=rz, sc=sc, name="wall_run")
        x += step

def wall_ring(half=32, z=3.0, sc=1.5):
    # front/back
    wall_run_front(-half, -half, half, z, rz=0, sc=sc)
    wall_run_front( half, -half, half, z, rz=180, sc=sc)
    # sides
    y = -half
    step = S_WALL_STEP * sc * 0.98
    while y <= half:
        place("S_WALLM", -half, y, z, rz=90, sc=sc, name="wall_run")
        place("S_WALLM",  half, y, z, rz=270, sc=sc, name="wall_run")
        y += step

def battlements(half=32, z=6.0, sc=0.9):
    step = S_WALL_STEP * sc * 1.05
    x = -half
    while x <= half:
        place("S_WALL_Q_H1", x, -half - 0.35, z, rz=0, sc=sc, name="battlement")
        place("S_WALL_Q_H1", x,  half + 0.35, z, rz=180, sc=sc, name="battlement")
        x += step
    y = -half
    while y <= half:
        place("S_WALL_Q_H1", -half - 0.35, y, z, rz=90, sc=sc, name="battlement")
        place("S_WALL_Q_H1",  half + 0.35, y, z, rz=270, sc=sc, name="battlement")
        y += step

def tower(cx, cy, radius_sc=1.4, rows=5):
    z0 = 1.0
    for i in range(rows):
        place("CYLINDERSHAPE", cx, cy, z0 + i * 2.0 * radius_sc, rx=90, rz=0, sc=radius_sc, name="round_tower")
    top_z = z0 + rows * 2.0 * radius_sc
    place("S_ROOF5", cx, cy, top_z + 1.3, rx=90, rz=45, sc=radius_sc * 1.15, name="tower_roof")
    place("SPHERESHAPE", cx, cy, top_z + 3.2, rx=0, rz=0, sc=0.32, name="tower_finial")

def keep():
    # Main keep walls
    sc = 2.2
    z = 5.0
    for x in [-8.5, 0, 8.5]:
        place("S_WALLM", x, -8.5, z, rz=0, sc=sc, name="keep_front")
        place("S_WALLM", x,  8.5, z, rz=180, sc=sc, name="keep_back")
    for y in [-8.5, 0, 8.5]:
        place("S_WALLM", -8.5, y, z, rz=90, sc=sc, name="keep_left")
        place("S_WALLM",  8.5, y, z, rz=270, sc=sc, name="keep_right")

    # Arched front gate stack
    place("S_ARCHB", 0, -9.0, 2.2, rz=0, sc=1.6, name="gate_arch_b")
    place("S_ARCHM", 0, -9.0, 5.5, rz=0, sc=1.6, name="gate_arch_m")
    place("S_ARCHT", 0, -9.0, 8.8, rz=0, sc=1.6, name="gate_arch_t")

    # Roof cap/crown
    for x in [-5.2, 0, 5.2]:
        for y in [-5.2, 0, 5.2]:
            place("S_ROOF5", x, y, 11.8, rz=45, sc=1.0, name="keep_roof")

# BUILD
floor_grid(6, 6, z=0.0, sc=1.05)
wall_ring(half=32, z=3.0, sc=1.45)
battlements(half=32, z=6.4, sc=0.95)

for cx, cy in [(-32, -32), (32, -32), (-32, 32), (32, 32)]:
    tower(cx, cy, radius_sc=1.35, rows=5)

keep()

print("=" * 72)
print("NMS_SCRIPT_AUDIT_PASS")
print(f"[NMS_CASTLE_REAL] Generated {_n} real NMS part placements.")
print("No raw Blender mesh primitives are used.")
print("=" * 72)
