"""
NMS_SAFE_STARTER_TEMPLATE.py

Use this as the base for every No Man's Sky Base Builder generator.

Purpose:
- Creates real NMS parts, not raw Blender mesh primitives.
- Uses BUILDER.add_part() once per ObjectID.
- Copies templates for fast placement.
- Preserves required NMS custom properties.
- Deletes only objects with this script's TAG.

Before running:
- Enable No Man's Sky Base Builder.
- Create/open/import a base so the builder runtime is initialized.
"""

import bpy
import math
import sys
import time

# =============================================================================
# CONFIG
# =============================================================================
TAG = "NMS_BUILD_"
USERDATA_DEFAULT = "0"

PART_IDS = [
    "S_FLOOR",
    "S_WALLM",
    "S_ROOF5",
    "CYLINDERSHAPE",
    "SPHERESHAPE",
    "S_ARCHB",
    "S_ARCHM",
    "S_ARCHT",
    "S_WALL_Q",
    "S_WALL_Q_H1",
    "S_WALL_SUPPORTS",
]

# =============================================================================
# PLUGIN PREFLIGHT
# =============================================================================
_mod = sys.modules.get("bl_ext.user_default.no_mans_sky_base_builder")
if _mod is None or not hasattr(_mod, "BUILDER"):
    raise RuntimeError(
        "No Man's Sky Base Builder is not initialized. "
        "Enable the addon and create/open/import a base first."
    )

BUILDER = _mod.BUILDER

# =============================================================================
# SAFE CLEANUP
# =============================================================================
for obj in list(bpy.data.objects):
    if obj.name.startswith(TAG):
        bpy.data.objects.remove(obj, do_unlink=True)

try:
    BUILDER.clear_caches()
except Exception:
    pass

# =============================================================================
# TEMPLATE CREATION — ONCE PER PART TYPE
# =============================================================================
T = {}
_ts = str(int(time.time()))

print(f"[NMS] Loading {len(PART_IDS)} part templates...")
for oid in PART_IDS:
    try:
        p = BUILDER.add_part(oid)
        p.object.name = f"{TAG}TPL_{oid}"
        T[oid] = p.object
        print(f"  ✓ {oid}")
    except Exception as e:
        print(f"  ✗ {oid}: {e}")

if not T:
    raise RuntimeError("No NMS templates were created. Check ObjectIDs and builder initialization.")

# =============================================================================
# PLACEMENT
# =============================================================================
_n = 0

def place(oid, x, y, z, rx=90, ry=0, rz=0, sc=1.0, ud=USERDATA_DEFAULT, name=None):
    """Place one real NMS part by copying a plugin-created template."""
    global _n

    if oid not in T:
        print(f"[NMS] Missing template, skipped: {oid}")
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

# =============================================================================
# SMOKE TEST BUILD — replace this section for actual projects
# =============================================================================
# This intentionally creates a small row of real NMS parts. If this produces
# generic Blender cubes/planes, something is wrong.

x = 0
for oid in PART_IDS[:8]:
    place(oid, x, 0, 0, rx=90, rz=0, sc=1.0, name=f"smoke_{oid}")
    x += 6

print("=" * 72)
print(f"[NMS] Smoke test completed with {_n} real NMS part placements.")
print("[NMS] Check Outliner names and custom properties: ObjectID should exist.")
print("[NMS] No raw mesh primitive calls are used in this template.")
print("=" * 72)

# =============================================================================
# RUNTIME NMS OBJECT AUDIT
# =============================================================================
def nms_runtime_object_audit(tag):
    required = [
        "ObjectID",
        "SnapID",
        "Timestamp",
        "UserData",
        "order",
        "belongs_to_preset",
    ]
    built = [obj for obj in bpy.data.objects if obj.name.startswith(tag) and "_TPL_" not in obj.name]
    if not built:
        raise RuntimeError(f"NMS audit failed: no built objects found for tag {tag!r}.")

    failures = []
    for obj in built:
        missing = [key for key in required if key not in obj]
        if missing:
            failures.append((obj.name, missing))

    if failures:
        msg = ["NMS audit failed: built objects missing NMS custom properties."]
        for name, missing in failures[:25]:
            msg.append(f"  {name}: missing {', '.join(missing)}")
        raise RuntimeError("\n".join(msg))

    print("NMS_OBJECT_AUDIT_PASS")
    print(f"Audited {len(built)} built NMS objects.")

nms_runtime_object_audit(TAG)

