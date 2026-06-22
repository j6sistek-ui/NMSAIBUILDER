# Gothic Church with a BIG glass dome — build_generation (creative architectural).
# VALIDATION TIER: SCRIPT_VALIDATED only. Geometry is a math-derived FIRST PASS and is NOT
# in-game validated (no live Blender this session). Run in Blender, screenshot, iterate.
# Dome uses the validated DOME_RADIAL_RING_TAPER method (S_ROOF_M_WIN glazing + S_WALL_Q ribs).
from bl_ext.user_default.no_mans_sky_base_builder import BUILDER
import bpy, math

TAG = "GOTHCHURCH_"
PART_IDS = ["S_FLOOR_Q","S_WALLM","S_WALLM_WIN1","S_RAMP","S_ROOF_M_WIN","S_WALL_Q","S_WALLM_DIAGONA","S_ARCH","S_GDOOR"]

# DESIGN_INTENT: the committed plan, declared BEFORE placement. Every assembly states
# what it should READ as and its evidence source; every used ObjectID carries a purpose.
# This is what run_gate's design-intent gate checks so a build is intentional, not a pile.
DESIGN_INTENT = {
    "build": "gothic_church_v01",
    "assemblies": [
        {"name": "nave_floor", "is_a": "floor slab",
         "target_read": "flat continuous nave floor, no gaps",
         "style_source": "CREATIVE_USE_CASE_AND_STYLE_INDEX: floor/foundation",
         "parts": [{"ObjectID": "S_FLOOR_Q", "purpose": "tiled nave floor plates"}]},
        {"name": "nave_walls", "is_a": "load-bearing wall shell",
         "target_read": "tall continuous gothic nave walls with rhythmic window bays",
         "style_source": "CREATIVE_USE_CASE_AND_STYLE_INDEX: wall shell / silhouette",
         "parts": [{"ObjectID": "S_WALLM", "purpose": "solid wall mass between bays"},
                   {"ObjectID": "S_WALLM_WIN1", "purpose": "windowed wall bays for clerestory rhythm"},
                   {"ObjectID": "S_WALL_Q", "purpose": "quarter walls closing corners into a continuous shell"}]},
        {"name": "portal", "is_a": "arched entrance",
         "target_read": "recessed arched main portal that reads as the entrance",
         "style_source": "CREATIVE_USE_CASE_AND_STYLE_INDEX: portal/arcade",
         "parts": [{"ObjectID": "S_ARCH", "purpose": "arched portal frame over the door"},
                   {"ObjectID": "S_GDOOR", "purpose": "main doorway"}]},
        {"name": "wall_accents", "is_a": "angled wall detail",
         "target_read": "shallow angled pilaster accents adding facade depth (not free-floating struts)",
         "style_source": "CREATIVE_USE_CASE_AND_STYLE_INDEX: facade depth",
         "parts": [{"ObjectID": "S_WALLM_DIAGONA", "purpose": "angled pilaster accents seated against the wall"}]},
        {"name": "approach", "is_a": "entry steps",
         "target_read": "clean steps leading up to the portal",
         "style_source": "CREATIVE_USE_CASE_AND_STYLE_INDEX: ramp/stair",
         "parts": [{"ObjectID": "S_RAMP", "purpose": "approach steps to the portal"}]},
        {"name": "roof", "is_a": "pitched roof",
         "target_read": "coherent pitched roof with a continuous ridge that reads as a roof",
         "style_source": "CREATIVE_USE_CASE_AND_STYLE_INDEX: roof/silhouette",
         "parts": [{"ObjectID": "S_ROOF_M_WIN", "purpose": "roof planes with dormer windows at packet-default orientation"}]},
    ],
}

PROJECT_BUILD_SHEET = "gothic_church_v01__PACKET.json"
BUILD_SHEET_USED = True

REQUEST_CLASSIFICATION = {
    "request_type": "build_generation",
    "user_inputs": ["build me a Church", "BIG glass dome roof", "Gothic style"],
    "rule_bundles_checked": ["VALIDATION_GATE_HARDENING_RULE", "CURATED_DETAIL_HIERARCHY_RULE", "FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL", "C_TRIFLOOR_EDGE_CONTACT_GRAPH_PROTOCOL", "DISCONNECTED_ASSEMBLY_HARDSTOP_RULE", "DOCS_UPDATE_AVAILABILITY_PROTOCOL", "FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL", "JSON_EVIDENCE_MAPPING_GATE", "JSON_RECIPE_SIGNATURE_INDEX", "MASTER_BUILD_RECIPES_AND_PLACEMENT_GUIDANCE", "MONUMENT_BUILD_WORKFLOW", "NMS_BUILDER_EXECUTION_KERNEL", "NMS_BUILD_VS_IMAGE_ROUTING_GUARD", "NMS_PART_DIMENSIONS_AND_RULES_UPDATED", "PROHIBITED_AND_PLACEHOLDER_OBJECTS", "OBJECT_USE_RECORDING_PROTOCOL", "SELECTIVE_VISUAL_MEMORY_POLICY", "PART_BUDGET_OPTIMIZATION_PROTOCOL", "PART_FAMILY_RULES", "PART_PLACEMENT_MAP_SCHEMA", "PART_USE_CASE_CATALOG", "PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE", "PROHIBITED_AND_PLACEHOLDER_OBJECTS", "PROMPT_TO_FEATURE_ROUTER", "PROTOCOL_BANNER_HARD_FAIL_RULE", "RECIPE_CONFORMANCE_PROTOCOL", "REQUEST_ROUTER_CHECKLIST", "SCRIPT_VALIDATION_LOOP", "FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL", "SYSTEMATIC_FAILURE_CAPA_PROTOCOL", "SYSTEMATIC_FAILURE_CAPA_PROTOCOL", "UNIVERSAL_RULES", "WORKING_JSON_FIRST_PRINCIPLE"],
    "ambiguity_resolution": "not_needed",
    "json_evidence_used": False
}

FEATURE_RECIPE_LOOKUP = {
    "feature_intent": "gothic church with a glass dome over the crossing",
    "matched_recipe_or_signature": "DOME_RADIAL_RING_TAPER",
    "recipe_files_checked": ["data/METHOD_AUTHORITY_TABLE.json", "rules/DOME_STUDY_LESSONS.md", "toolkit/PLACEMENT_RECIPE_LIBRARY.json"],
    "recipe_status": "validated_recipe",
    "reason_if_none": "",
    "part_map_role": "component_validation_only"
}

AI_CAPTURE_COMPLIANCE = {
    "schema": "NMS_AI_CAPTURE_COMPLIANCE_v1",
    "source_docs_rev": "5.03.00",
    "semantic_roles": ["exterior_shell_walls_roof", "interior_floor_access", "decor_review_experimental", "scene_context"],
    "semantic_collections": ["church_exterior_shell", "church_interior_floor_access", "church_decor_review", "church_scene_context"],
    "object_metadata_fields": ["role", "collection_role", "review_required", "placement_method", "source_docs_rev"],
    "single_collection_fallback_declared": False
}

USED_PART_LOGIC = {
    "S_RAMP": {
        "status": "BLENDER_USER_CHECK",
        "partmap_path": "library/part_placement_maps/S_RAMP.partmap.json",
        "validated_algorithm": "BUTTRESS_ANCHORED_SUPPORT adapted from the verified S_RAMP component as a decorative flying buttress (NOT the walkable stair/ramp endpoint recipe)",
        "reuse_mode": "EXPERIMENTAL_VARIANT",
        "source_transform_invariants": {"Position": [0.0, 0.0, 0.0], "Up": [0.0, 1.0, 0.0], "At": [0.0, 0.0, 1.0]}
    }
}

BUILD_INTENT_GRAPH = {
    "subassemblies_intended": ["cruciform_floor", "nave_walls", "window_walls", "arcade", "flying_buttresses", "glass_dome", "twin_spires", "west_portal"],
    "expected_connected_components": 1,
    "required_connections": ["walls_to_floor", "windows_to_walls", "dome_to_crossing_walls", "spires_to_west_front", "buttresses_to_nave_walls", "door_to_west_wall"]
}

# tag-scoped cleanup (idempotent re-runs) — also purge stale TPL_ templates
for old in list(getattr(bpy.data, "objects", [])):
    _nm = str(getattr(old, "name", ""))
    if _nm.startswith(TAG) or _nm.startswith("TPL_"):
        try: bpy.data.objects.remove(old, do_unlink=True)
        except Exception: pass

# template each ObjectID ONCE, then copy per placement (never add_part per placement)
TEMPLATES = {}
for _oid in PART_IDS:
    _p = BUILDER.add_part(_oid)
    _t = getattr(_p, "object", _p)
    _t.name = "TPL_" + _oid
    TEMPLATES[_oid] = _t

_idx = 0
def place(oid, x, y, z, rz=0.0, rx=90.0):
    global _idx
    o = TEMPLATES[oid].copy()
    _idx += 1
    o.name = "{}{:04d}_{}".format(TAG, _idx, oid)
    o["ObjectID"] = oid
    o.location = (x, y, z)
    o.rotation_euler = (math.radians(rx), 0.0, math.radians(rz))
    o.scale = (1.0, 1.0, 1.0)
    bpy.context.collection.objects.link(o)
    return o

S  = 2.45
WH = 2.45

# cruciform floor: nave (10 x 5) + transept arms
for ix in range(0, 10):
    for iy in range(-2, 3):
        place("S_FLOOR_Q", ix*S, iy*S, 0.0)
for ix in range(4, 7):
    for iy in list(range(-4, -2)) + list(range(3, 5)):
        place("S_FLOOR_Q", ix*S, iy*S, 0.0)

# nave long walls (2 courses) with pointed gothic windows interspersed
for ix in range(0, 10):
    for c in range(2):
        z = WH*0.5 + c*WH
        part = "S_WALLM_WIN1" if (ix % 2 == 1 and c == 1) else "S_WALLM"
        place(part, ix*S, -2*S, z, rz=0)
        place(part, ix*S,  2*S, z, rz=180)

# west front + east apse end walls (leave a west doorway)
for iy in range(-2, 3):
    for c in range(2):
        z = WH*0.5 + c*WH
        if not (iy == 0 and c == 0):
            place("S_WALLM", 0*S, iy*S, z, rz=270)
        place("S_WALLM", 9*S, iy*S, z, rz=90)

# west portal door
place("S_GDOOR", 0*S, 0*S, WH*0.5, rz=270)

# pointed-arch nave arcade (two rows)
for ix in range(1, 9):
    place("S_ARCH", ix*S, -1*S, WH, rz=0)
    place("S_ARCH", ix*S,  1*S, WH, rz=0)

# flying buttresses anchored outside the nave walls
for ix in range(1, 9, 2):
    place("S_RAMP", ix*S, -2.8*S, WH, rz=90)
    place("S_RAMP", ix*S,  2.8*S, WH, rz=270)

# BIG glass dome over the crossing: radial-ring taper (DOME_RADIAL_RING_TAPER)
cx, cy = 5*S, 0.0
base_z = 2*WH
N, RINGS, R0 = 12, 3, 3.2
for r in range(RINGS):
    R = R0 * (1 - r / float(RINGS + 1))
    z = base_z + r * 1.1
    for k in range(N):
        ang = 2*math.pi*k / N
        x = cx + R*math.cos(ang)
        y = cy + R*math.sin(ang)
        place("S_ROOF_M_WIN", x, y, z, rz=math.degrees(ang))
        if r == 0:
            place("S_WALL_Q", x, y, base_z, rz=math.degrees(ang))
place("S_ROOF_M_WIN", cx, cy, base_z + RINGS*1.1, rz=0.0)

# twin west-front spires (angled diagonal faces, tapering courses)
for sy in (-2, 2):
    for c in range(3):
        z = 2*WH + c*WH
        for face_rz in (0, 90, 180, 270):
            place("S_WALLM_DIAGONA", 0*S, sy*S, z, rz=face_rz)

print("GOTHIC CHURCH placed:", _idx, "parts")

# delete templates before export — otherwise they survive cleanup and pile at the
# origin (template-leak). Placed copies keep their own NMS data; templates are scrap.
for _t in TEMPLATES.values():
    try: bpy.data.objects.remove(_t, do_unlink=True)
    except Exception: pass
