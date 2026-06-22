
bl_info = {
    "name": "NMS AI Review Bundle v04",
    "author": "OpenAI / NMS Builder workflow",
    "version": (0, 4, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > NMS AI",
    "description": "Budgeted visual bundle with semantic tokens, object-name clusters, spatial section/cutaway passes, and no-op capture detection.",
    "category": "3D View",
}

import bpy
import json
import math
import shutil
import time
from pathlib import Path
from mathutils import Vector


def safe_name(text):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
    return "".join(c if c in allowed else "_" for c in str(text))[:120]


def parse_tokens(text):
    return [t.strip().upper() for t in str(text).replace(";", ",").split(",") if t.strip()]


def nms_id(obj):
    for key in ("ObjectID", "SnapID", "object_id"):
        if key in obj:
            return str(obj[key])
    return ""


def is_review_obj(obj):
    return bool(nms_id(obj)) or (obj.type == "MESH" and not obj.name.startswith("NMS_AI_REVIEW_CAMERA"))


def get_all_review_objects(include_hidden=False):
    objs = [o for o in bpy.context.scene.objects if is_review_obj(o)]
    if not include_hidden:
        objs = [o for o in objs if not o.hide_get()]
    return objs


def object_collections(obj):
    return [c.name for c in obj.users_collection]


def object_blob(obj):
    return " ".join(object_collections(obj) + [
        obj.name,
        str(obj.get("collection_role", "")),
        str(obj.get("role", "")),
        str(obj.get("placement_method", "")),
    ]).upper()


def has_any_token(obj, tokens):
    if not tokens:
        return False
    blob = object_blob(obj)
    return any(t in blob for t in tokens)


def has_no_token(obj, tokens):
    if not tokens:
        return True
    return not has_any_token(obj, tokens)


def bbox(objs):
    pts = []
    for obj in objs:
        try:
            pts += [obj.matrix_world @ Vector(c) for c in obj.bound_box]
        except Exception:
            pts.append(obj.location.copy())
    if not pts:
        pts = [Vector((0, 0, 0))]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    center = (mn + mx) * 0.5
    size = mx - mn
    radius = max(size.x, size.y, size.z, 1.0) * 0.5
    return mn, mx, center, size, radius


def center_of(obj):
    try:
        pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
        return sum(pts, Vector((0, 0, 0))) / len(pts)
    except Exception:
        return obj.location.copy()


def collection_counts(objs):
    counts = {}
    for obj in objs:
        for c in obj.users_collection:
            counts[c.name] = counts.get(c.name, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def object_counts(objs):
    counts = {}
    for obj in objs:
        oid = nms_id(obj) or obj.name
        counts[oid] = counts.get(oid, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def unique_collection_count(objs):
    names = set()
    for o in objs:
        for c in o.users_collection:
            names.add(c.name)
    return len(names)


def get_camera():
    name = "NMS_AI_REVIEW_CAMERA"
    cam_data = bpy.data.cameras.get(name) or bpy.data.cameras.new(name)
    cam = bpy.data.objects.get(name)
    if cam is None:
        cam = bpy.data.objects.new(name, cam_data)
        bpy.context.scene.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    return cam


def look_at(cam, target):
    direction = target - cam.location
    if direction.length == 0:
        direction = Vector((0, 0, -1))
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def set_view(cam, center, radius, view):
    dist = max(radius * 4.0, 20.0)
    views = {
        "front": Vector((-dist, 0, 0)),
        "rear": Vector((dist, 0, 0)),
        "left": Vector((0, -dist, 0)),
        "right": Vector((0, dist, 0)),
        "top": Vector((0, 0, dist)),
        "iso_l": Vector((-dist, -dist, dist * 0.65)),
        "iso_r": Vector((-dist, dist, dist * 0.65)),
        "rear_iso": Vector((dist, dist, dist * 0.65)),
        "interior_entry": Vector((-dist * 0.38, 0, radius * 0.12)),
        "interior_rear": Vector((dist * 0.38, 0, radius * 0.12)),
        "interior_top": Vector((0, 0, dist * 0.40)),
    }
    cam.location = center + views.get(view, views["iso_l"])
    look_at(cam, center)
    cam.data.ortho_scale = max(radius * 2.35, 8.0)
    bpy.context.scene.camera = cam


def capture_image(filepath, cam, center, radius, view, resx, resy, image_format, jpeg_quality):
    scene = bpy.context.scene
    old = (
        scene.camera,
        scene.render.filepath,
        scene.render.resolution_x,
        scene.render.resolution_y,
        scene.render.resolution_percentage,
        scene.render.image_settings.file_format,
        scene.render.image_settings.quality,
    )
    set_view(cam, center, radius, view)
    scene.render.filepath = str(filepath)
    scene.render.resolution_x = int(resx)
    scene.render.resolution_y = int(resy)
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = image_format
    scene.render.image_settings.quality = int(jpeg_quality)
    try:
        bpy.ops.render.opengl(write_still=True, view_context=False)
    except Exception:
        bpy.ops.render.render(write_still=True)
    (
        scene.camera,
        scene.render.filepath,
        scene.render.resolution_x,
        scene.render.resolution_y,
        scene.render.resolution_percentage,
        scene.render.image_settings.file_format,
        scene.render.image_settings.quality,
    ) = old


def hide_all_review_objects(objs):
    original = {}
    for obj in objs:
        try:
            original[obj.name] = obj.hide_get()
            obj.hide_set(True)
        except Exception:
            pass
    return original


def restore_hidden_state(objs, original):
    for obj in objs:
        try:
            obj.hide_set(original.get(obj.name, False))
        except Exception:
            pass


def show_only(all_objs, show_objs):
    show_set = set(show_objs)
    for obj in all_objs:
        try:
            obj.hide_set(obj not in show_set)
        except Exception:
            pass


def profile_views(profile):
    if profile == "QUICK":
        return ["front", "left", "top", "iso_l"], ["front", "interior_entry", "top"]
    if profile == "FULL":
        return ["front", "rear", "left", "right", "top", "iso_l", "iso_r", "rear_iso"], ["front", "left", "right", "top", "iso_l", "interior_entry", "interior_rear", "interior_top"]
    return ["front", "rear", "left", "right", "top", "iso_l"], ["front", "left", "top", "iso_l", "interior_entry", "interior_rear"]


# ------------------------------
# Object-name clustering and spatial passes
# ------------------------------

def name_cluster_key(obj, max_parts=5):
    # Handles names like NMS_MEGACITY_V15_GOTHAM_gcpd_black_block_BILLBOARD_01107.
    parts = [p for p in obj.name.replace("-", "_").split("_") if p]
    if len(parts) <= 2:
        return obj.name
    # Drop final numeric suffixes.
    while parts and parts[-1].isdigit():
        parts = parts[:-1]
    # Prefer city/building chunk when present.
    upper = [p.upper() for p in parts]
    anchors = ["GOTHAM", "MEGACITY", "BUILDING", "TOWER", "GCPD", "BLOCK"]
    idx = None
    for a in anchors:
        if a in upper:
            idx = upper.index(a)
            break
    if idx is not None:
        return "_".join(parts[idx:idx + max_parts])
    return "_".join(parts[:max_parts])


def largest_name_clusters(objs, max_clusters=5, min_objs=10):
    groups = {}
    for o in objs:
        k = name_cluster_key(o)
        groups.setdefault(k, []).append(o)
    ranked = [(k, v) for k, v in groups.items() if len(v) >= min_objs]
    ranked.sort(key=lambda kv: -len(kv[1]))
    return ranked[:max_clusters]


def spatial_slices(objs):
    mn, mx, center, size, radius = bbox(objs)
    slices = []
    axes = [
        ("X", lambda p: p.x, mn.x, mx.x),
        ("Y", lambda p: p.y, mn.y, mx.y),
        ("Z", lambda p: p.z, mn.z, mx.z),
    ]
    for axis, getter, lo, hi in axes:
        span = hi - lo
        if span <= 0.001:
            continue
        q1 = lo + span * 0.33
        q2 = lo + span * 0.66
        low = [o for o in objs if getter(center_of(o)) <= q1]
        mid = [o for o in objs if q1 < getter(center_of(o)) <= q2]
        high = [o for o in objs if getter(center_of(o)) > q2]
        slices.append((f"SPATIAL_{axis}_LOW_THIRD", low))
        slices.append((f"SPATIAL_{axis}_MIDDLE_THIRD", mid))
        slices.append((f"SPATIAL_{axis}_HIGH_THIRD", high))
    return slices


def interior_candidate_by_margin(objs, margin_ratio=0.13):
    # Approximate geometric "inside" by hiding objects close to the global bounding shell.
    mn, mx, center, size, radius = bbox(objs)
    mxspan = max(size.x, size.y, size.z, 1.0)
    margin = mxspan * margin_ratio
    kept = []
    for o in objs:
        p = center_of(o)
        # Keep objects away from bounding extremes on at least two axes.
        inside_axes = 0
        if mn.x + margin < p.x < mx.x - margin:
            inside_axes += 1
        if mn.y + margin < p.y < mx.y - margin:
            inside_axes += 1
        if mn.z + margin < p.z < mx.z - margin:
            inside_axes += 1
        if inside_axes >= 2:
            kept.append(o)
    return kept


def exterior_candidate_by_margin(objs, margin_ratio=0.13):
    inside = set(interior_candidate_by_margin(objs, margin_ratio))
    return [o for o in objs if o not in inside]


def add_capture(plan, label, objs, views, reason, all_objs, skip_redundant=True, min_delta=0.05):
    if not objs or not views:
        return
    obj_set = set(objs)
    if skip_redundant:
        for item in plan:
            prev = set(item["objects"])
            if not prev:
                continue
            inter = len(obj_set & prev)
            union = len(obj_set | prev)
            same_ratio = inter / union if union else 1.0
            if same_ratio >= (1.0 - min_delta):
                item.setdefault("skipped_equivalent_labels", []).append(label)
                return
    plan.append({"label": label, "objects": objs, "views": list(views), "reason": reason})


def build_capture_plan(all_objs, settings):
    exterior_views, interior_views = profile_views(settings.capture_profile)
    scene_tokens = parse_tokens(settings.scene_exclude_tokens)
    exterior_tokens = parse_tokens(settings.exterior_tokens)
    interior_tokens = parse_tokens(settings.interior_tokens)
    decor_tokens = parse_tokens(settings.decor_tokens)
    priority_tokens = parse_tokens(settings.priority_collection_tokens)
    skip_redundant = settings.skip_redundant_sets
    min_delta = settings.redundancy_delta_percent / 100.0
    plan = []

    core_objs = [o for o in all_objs if has_no_token(o, scene_tokens)]
    interior_objs = [o for o in core_objs if has_any_token(o, interior_tokens)]
    exterior_objs = [o for o in core_objs if has_any_token(o, exterior_tokens)]
    no_front_decor = [o for o in core_objs if has_no_token(o, decor_tokens + ["FRONT", "FOCAL", "GOLD", "CTRIFLOOR"])]
    no_shell = [o for o in core_objs if has_no_token(o, exterior_tokens + ["SHELL", "FRONT", "FOCAL"])]

    add_capture(plan, "01_ALL_VISIBLE", all_objs, exterior_views, "all visible review objects", all_objs, False)
    add_capture(plan, "02_CORE_NO_SCENE", core_objs, exterior_views, "scene/city tokens removed", all_objs, skip_redundant, min_delta)
    add_capture(plan, "03_INTERIOR_TOKEN_ONLY", interior_objs, interior_views, "objects matching interior/access/detail tokens", all_objs, skip_redundant, min_delta)
    add_capture(plan, "04_EXTERIOR_TOKEN_ONLY", exterior_objs, exterior_views, "objects matching exterior/shell/front tokens", all_objs, skip_redundant, min_delta)
    add_capture(plan, "05_CUTAWAY_HIDE_FRONT_DECOR", no_front_decor, interior_views, "front/decor/gold hidden by token", all_objs, skip_redundant, min_delta)
    add_capture(plan, "06_CUTAWAY_HIDE_EXTERIOR_SHELL", no_shell, interior_views, "shell/front hidden by token", all_objs, skip_redundant, min_delta)

    if settings.capture_margin_cutaways:
        inside = interior_candidate_by_margin(core_objs, settings.margin_ratio)
        outside = exterior_candidate_by_margin(core_objs, settings.margin_ratio)
        add_capture(plan, "07_GEOMETRIC_INTERIOR_CANDIDATE", inside, interior_views, "approximate inside via bounding-box margin", all_objs, skip_redundant, min_delta)
        add_capture(plan, "08_GEOMETRIC_EXTERIOR_CANDIDATE", outside, exterior_views, "approximate outside via bounding-box margin", all_objs, skip_redundant, min_delta)

    if settings.capture_name_clusters:
        for key, objs in largest_name_clusters(core_objs, settings.max_name_clusters, settings.name_cluster_min_objects):
            add_capture(plan, "NAME_CLUSTER_" + safe_name(key), objs, ["front", "left", "top", "iso_l"], "largest object-name cluster", all_objs, skip_redundant, min_delta)

    if settings.capture_spatial_slices:
        for label, objs in spatial_slices(core_objs):
            add_capture(plan, label, objs, ["front", "left", "top"], "spatial third slice", all_objs, skip_redundant, min_delta)

    if settings.capture_priority_collections:
        by_collection = {}
        for obj in core_objs:
            for c in obj.users_collection:
                by_collection.setdefault(c.name, []).append(obj)
        count = 0
        for cname, objs in sorted(by_collection.items(), key=lambda kv: -len(kv[1])):
            if priority_tokens and not any(t in cname.upper() for t in priority_tokens):
                continue
            add_capture(plan, "COLLECTION_" + safe_name(cname), objs, ["front", "left", "top", "iso_l"], "priority collection pass", all_objs, skip_redundant, min_delta)
            count += 1
            if count >= settings.max_priority_collections:
                break

    # Apply hard image budget.
    budgeted = []
    used = 0
    for item in plan:
        remaining = int(settings.max_images) - used
        if remaining <= 0:
            break
        views = item["views"][:remaining]
        if not views:
            break
        item = dict(item)
        item["views"] = views
        budgeted.append(item)
        used += len(views)
    return budgeted


def export_json(folder, all_objs, capture_sets, skipped_notes, settings):
    rows = []
    for i, obj in enumerate(all_objs):
        loc = obj.matrix_world.translation
        rows.append({
            "index": i,
            "name": obj.name,
            "name_cluster_key": name_cluster_key(obj),
            "type": obj.type,
            "ObjectID": nms_id(obj) or obj.name,
            "collections": object_collections(obj),
            "review_required": bool(obj.get("review_required", False)),
            "role": str(obj.get("role", "")),
            "collection_role": str(obj.get("collection_role", "")),
            "location_blender": [round(float(loc.x), 6), round(float(loc.y), 6), round(float(loc.z), 6)],
            "scale": [round(float(v), 6) for v in obj.scale],
            "custom_properties": {str(k): str(obj[k]) for k in obj.keys()},
        })
    mn, mx, center, size, radius = bbox(all_objs)
    data = {
        "schema": "NMS_AI_REVIEW_BUNDLE_v04",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "blender_version": bpy.app.version_string,
        "scene": bpy.context.scene.name,
        "capture_profile": settings.capture_profile,
        "max_images": settings.max_images,
        "image_format": settings.image_format,
        "jpeg_quality": settings.jpeg_quality,
        "object_count": len(all_objs),
        "unique_collection_count": unique_collection_count(all_objs),
        "counts_by_object_id": object_counts(all_objs),
        "counts_by_collection": collection_counts(all_objs),
        "bounds_all_review_objects": {
            "min": [float(mn.x), float(mn.y), float(mn.z)],
            "max": [float(mx.x), float(mx.y), float(mx.z)],
            "center": [float(center.x), float(center.y), float(center.z)],
            "size": [float(size.x), float(size.y), float(size.z)],
            "offset_from_origin": [float(center.x), float(center.y), float(center.z)],
        },
        "capture_sets": capture_sets,
        "skipped_or_equivalent_capture_notes": skipped_notes,
        "diagnostics": {
            "single_collection_warning": unique_collection_count(all_objs) <= 1,
            "collection_isolation_useful": unique_collection_count(all_objs) > 1,
            "recommendation": "Use semantic build collections when possible; otherwise rely on name clusters and spatial/geometric cutaways.",
        },
        "objects": rows,
    }
    (folder / "nms_ai_review_objects.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def write_checklist(folder, data):
    text = "# NMS AI Review Checklist v04\\n\\n"
    text += f"Created: {data.get('created_at')}\\n"
    text += f"Scene: {data.get('scene')}\\n"
    text += f"Objects: {data.get('object_count')}\\n"
    text += f"Unique collections: {data.get('unique_collection_count')}\\n"
    text += f"Capture profile: {data.get('capture_profile')}\\n"
    text += f"Max images: {data.get('max_images')}\\n\\n"
    if data.get("diagnostics", {}).get("single_collection_warning"):
        text += "## Warning\\nAll review objects appear to be in one collection. Collection-isolated review will not reveal hidden interiors. This bundle uses name clusters and spatial/geometric cutaways instead.\\n\\n"
    text += "## Review questions\\n"
    text += "1. Are there hidden/interior parts the exterior photos miss?\\n"
    text += "2. Do name-cluster passes identify separate buildings/blocks?\\n"
    text += "3. Do geometric interior/exterior candidates expose inside details?\\n"
    text += "4. Are capture sets actually different or redundant?\\n"
    text += "5. Should the build script create semantic collections for future runs?\\n\\n"
    text += "## Capture sets\\n```json\\n" + json.dumps(data.get("capture_sets", []), indent=2) + "\\n```\\n\\n"
    text += "## Skipped/equivalent capture notes\\n```json\\n" + json.dumps(data.get("skipped_or_equivalent_capture_notes", []), indent=2) + "\\n```\\n\\n"
    text += "## Object counts\\n```json\\n" + json.dumps(data.get("counts_by_object_id", {}), indent=2) + "\\n```\\n"
    (folder / "NMS_AI_REVIEW_CHECKLIST.md").write_text(text, encoding="utf-8")
    (folder / "OPEN_TOPICS_LOG.md").write_text(
        "# Open Topics Log — NMS AI Review Bundle v04\\n\\n"
        "- AI visual/objective review pending.\\n"
        "- This bundle detects single-collection/no-op capture risk.\\n"
        "- This bundle uses object-name clusters and spatial/geometric cutaways when semantic collections are missing.\\n"
        "- Pair with authoritative NMS Builder export JSON for run_gate.\\n",
        encoding="utf-8"
    )


class NMSAIReviewSettingsV04(bpy.types.PropertyGroup):
    output_dir: bpy.props.StringProperty(name="Output Folder", subtype="DIR_PATH", default=str(Path.home() / "NMS_AI_Review_Bundles"))
    capture_profile: bpy.props.EnumProperty(
        name="Profile",
        items=[("QUICK", "Quick", "Small bundle"), ("STANDARD", "Standard", "Balanced"), ("FULL", "Full", "More views")],
        default="STANDARD",
    )
    max_images: bpy.props.IntProperty(name="Max Images", default=36, min=8, max=160)
    resolution_x: bpy.props.IntProperty(name="Width", default=1280, min=640, max=4096)
    resolution_y: bpy.props.IntProperty(name="Height", default=800, min=480, max=4096)
    image_format: bpy.props.EnumProperty(name="Image Format", items=[("JPEG", "JPEG", "Small"), ("PNG", "PNG", "Lossless")], default="JPEG")
    jpeg_quality: bpy.props.IntProperty(name="JPEG Quality", default=72, min=35, max=100)
    include_hidden: bpy.props.BoolProperty(name="Include Hidden Objects", default=False)

    skip_redundant_sets: bpy.props.BoolProperty(name="Skip Redundant Sets", default=True)
    redundancy_delta_percent: bpy.props.FloatProperty(name="Min Set Difference %", default=5.0, min=0.0, max=95.0)

    capture_name_clusters: bpy.props.BoolProperty(name="Capture Name Clusters", default=True)
    max_name_clusters: bpy.props.IntProperty(name="Max Name Clusters", default=6, min=0, max=30)
    name_cluster_min_objects: bpy.props.IntProperty(name="Name Cluster Min Objects", default=10, min=2, max=1000)

    capture_margin_cutaways: bpy.props.BoolProperty(name="Capture Geometric Interior/Exterior", default=True)
    margin_ratio: bpy.props.FloatProperty(name="Interior Margin Ratio", default=0.13, min=0.01, max=0.45)

    capture_spatial_slices: bpy.props.BoolProperty(name="Capture Spatial Slices", default=True)
    capture_priority_collections: bpy.props.BoolProperty(name="Capture Priority Collections", default=True)
    max_priority_collections: bpy.props.IntProperty(name="Max Priority Collections", default=4, min=0, max=20)

    priority_collection_tokens: bpy.props.StringProperty(name="Priority Collection Tokens", default="FRONT,FOCAL,SHELL,STRUCTURAL,INTERIOR,ACCESS,GOLD,LIGHT,DECOR")
    scene_exclude_tokens: bpy.props.StringProperty(name="Scene Exclude Tokens", default="SCENE,SKYLINE,PLAZA,CITY")
    exterior_tokens: bpy.props.StringProperty(name="Exterior Tokens", default="FRONT,FOCAL,SHELL,STRUCTURAL,EXTERIOR,WALL,ROOF")
    interior_tokens: bpy.props.StringProperty(name="Interior Tokens", default="INTERIOR,ACCESS,FLOOR,CEILING,WALL,DETAIL,ROOM,INSIDE")
    decor_tokens: bpy.props.StringProperty(name="Decor Tokens", default="DECOR,LIGHT,GOLD,ACCENT,REVIEW,BILLBOARD,SIGN")


class NMSAI_OT_make_review_bundle_v04(bpy.types.Operator):
    bl_idname = "nms_ai.make_review_bundle_v04"
    bl_label = "Create NMS AI Review Bundle v04"
    bl_description = "Create budgeted bundle with name clusters, spatial cutaways, and no-op capture detection"

    def execute(self, context):
        s = context.scene.nms_ai_review_settings_v04
        base = Path(bpy.path.abspath(s.output_dir)).expanduser()
        base.mkdir(parents=True, exist_ok=True)
        folder = base / ("NMS_AI_REVIEW_V04_" + safe_name(context.scene.name) + "_" + time.strftime("%Y%m%d_%H%M%S"))
        folder.mkdir(parents=True, exist_ok=True)

        all_objs = get_all_review_objects(s.include_hidden)
        if not all_objs:
            self.report({"ERROR"}, "No visible review objects found.")
            return {"CANCELLED"}

        original_hidden = hide_all_review_objects(all_objs)
        cam = get_camera()
        plan = build_capture_plan(all_objs, s)
        capture_sets = []
        ext = ".jpg" if s.image_format == "JPEG" else ".png"

        for item in plan:
            objs = item["objects"]
            views = item["views"]
            if not objs or not views:
                continue
            show_only(all_objs, objs)
            mn, mx, center, size, radius = bbox(objs)
            label = safe_name(item["label"])
            shots = folder / "screenshots" / label
            shots.mkdir(parents=True, exist_ok=True)
            for view in views:
                capture_image(shots / (view + ext), cam, center, radius, view, s.resolution_x, s.resolution_y, s.image_format, s.jpeg_quality)
            capture_sets.append({
                "label": item["label"],
                "object_count": len(objs),
                "views": views,
                "folder": "screenshots/" + label,
                "reason": item.get("reason", ""),
                "bounds_center": [float(center.x), float(center.y), float(center.z)],
                "bounds_size": [float(size.x), float(size.y), float(size.z)],
                "skipped_equivalent_labels": item.get("skipped_equivalent_labels", []),
            })

        restore_hidden_state(all_objs, original_hidden)
        skipped_notes = []
        for item in plan:
            if item.get("skipped_equivalent_labels"):
                skipped_notes.append({"kept": item["label"], "skipped_equivalent_labels": item["skipped_equivalent_labels"]})

        data = export_json(folder, all_objs, capture_sets, skipped_notes, s)
        write_checklist(folder, data)
        zip_base = shutil.make_archive(str(folder), "zip", str(folder))
        self.report({"INFO"}, "Created: " + zip_base)
        print("NMS AI review bundle v04 created:", zip_base)
        return {"FINISHED"}


class NMSAI_PT_review_panel_v04(bpy.types.Panel):
    bl_label = "NMS AI Review v04"
    bl_idname = "NMSAI_PT_review_panel_v04"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NMS AI"

    def draw(self, context):
        layout = self.layout
        s = context.scene.nms_ai_review_settings_v04
        layout.prop(s, "output_dir")
        layout.prop(s, "capture_profile")
        layout.prop(s, "max_images")
        row = layout.row(align=True)
        row.prop(s, "resolution_x")
        row.prop(s, "resolution_y")
        row = layout.row(align=True)
        row.prop(s, "image_format")
        row.prop(s, "jpeg_quality")
        layout.prop(s, "include_hidden")
        layout.separator()
        layout.prop(s, "skip_redundant_sets")
        layout.prop(s, "redundancy_delta_percent")
        layout.separator()
        layout.prop(s, "capture_name_clusters")
        layout.prop(s, "max_name_clusters")
        layout.prop(s, "capture_margin_cutaways")
        layout.prop(s, "capture_spatial_slices")
        layout.prop(s, "capture_priority_collections")
        layout.prop(s, "max_priority_collections")
        layout.separator()
        layout.operator("nms_ai.make_review_bundle_v04", icon="RENDER_STILL")
        layout.label(text="v04 handles one-collection builds better.", icon="INFO")


classes = (NMSAIReviewSettingsV04, NMSAI_OT_make_review_bundle_v04, NMSAI_PT_review_panel_v04)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.nms_ai_review_settings_v04 = bpy.props.PointerProperty(type=NMSAIReviewSettingsV04)


def unregister():
    if hasattr(bpy.types.Scene, "nms_ai_review_settings_v04"):
        del bpy.types.Scene.nms_ai_review_settings_v04
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
