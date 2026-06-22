#!/usr/bin/env python3
"""AI Review bundle checker (3.00.00).

Validates standardized NMS_AI_REVIEW*.zip visual-design-loop bundles. This is
not an authoritative NMS export JSON conformance check; it verifies bundle
shape, capture metadata, and review-readiness signals.

Supported schemas:
- NMS_AI_REVIEW_BUNDLE_v01
- NMS_AI_REVIEW_BUNDLE_v02
- NMS_AI_REVIEW_BUNDLE_v03
- NMS_AI_REVIEW_BUNDLE_v04
"""
import json
import os
import sys
import tempfile
import zipfile

REQUIRED_BASE = [
    "NMS_AI_REVIEW_CHECKLIST.md",
    "OPEN_TOPICS_LOG.md",
    "nms_ai_review_objects.json",
]

V01_EXPECTED_SCREENSHOTS = [
    "screenshots/front_x_minus.png",
    "screenshots/front_x_plus.png",
    "screenshots/iso_front_left.png",
    "screenshots/iso_front_right.png",
    "screenshots/rear_iso.png",
    "screenshots/side_y_minus.png",
    "screenshots/side_y_plus.png",
    "screenshots/top_z_plus.png",
]

IMAGE_EXTS = (".png", ".jpg", ".jpeg")

def _find(name_set, suffix):
    for n in name_set:
        if n == suffix or n.endswith('/' + suffix):
            return n
    return None

def _read_json_from_zip(z, name):
    return json.loads(z.read(name).decode('utf-8'))

def _object_list(data):
    if isinstance(data, dict):
        for key in ("objects", "scene_objects", "items"):
            if isinstance(data.get(key), list):
                return data[key]
    if isinstance(data, list):
        return data
    return []

def _object_id(o):
    if not isinstance(o, dict):
        return None
    for key in ("ObjectID", "object_id", "objectid"):
        if o.get(key):
            return o.get(key)
    props = o.get("custom_properties") or o.get("properties") or {}
    if isinstance(props, dict):
        return props.get("ObjectID") or props.get("object_id")
    return None

def _scale_tuple(o):
    if not isinstance(o, dict):
        return None
    s = o.get("scale") or o.get("Scale")
    if isinstance(s, dict):
        vals = [s.get(k) for k in ("x", "y", "z")]
    elif isinstance(s, (list, tuple)) and len(s) >= 3:
        vals = s[:3]
    else:
        return None
    try:
        return tuple(float(v) for v in vals)
    except Exception:
        return None

def _collections_of(o):
    cols = o.get("collections") or o.get("collection_names") or []
    if isinstance(cols, str):
        return [cols]
    if isinstance(cols, list):
        return [str(c) for c in cols]
    return []

def _image_names(names):
    return [n for n in names if n.lower().endswith(IMAGE_EXTS) and "/screenshots/" in ("/" + n)]

def _capture_sets(data, image_names):
    sets = []
    if isinstance(data, dict) and isinstance(data.get("capture_sets"), list):
        for cs in data.get("capture_sets"):
            if isinstance(cs, dict):
                sets.append(cs)
    if not sets:
        # v01 flat screenshot bundle fallback.
        sets.append({
            "label": "V01_FLAT_STANDARD_VIEWS",
            "object_count": data.get("object_count") if isinstance(data, dict) else None,
            "views": [os.path.basename(n).rsplit(".", 1)[0] for n in image_names],
            "folder": "screenshots",
            "reason": "legacy flat bundle",
        })
    return sets

def check_bundle(path):
    errors = []
    warnings = []
    metrics = {}
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        missing = [e for e in REQUIRED_BASE if _find(names, e) is None]
        if missing:
            errors.append("missing required files: " + ", ".join(missing))
        obj_name = _find(names, "nms_ai_review_objects.json")
        data = _read_json_from_zip(z, obj_name) if obj_name else {}
        objects = _object_list(data)
        image_names = _image_names(names)
        if not image_names:
            errors.append("no screenshots found under screenshots/")
        schema = data.get("schema") if isinstance(data, dict) else None

        # v01 strict compatibility: accept classic flat bundle if schema is old/unknown.
        if schema in (None, "NMS_AI_REVIEW_BUNDLE_v01"):
            missing_v01 = [e for e in V01_EXPECTED_SCREENSHOTS if _find(names, e) is None]
            if missing_v01:
                warnings.append("legacy v01 expected screenshots missing: " + ", ".join(missing_v01))

        capture_sets = _capture_sets(data if isinstance(data, dict) else {}, image_names)
        if schema and schema >= "NMS_AI_REVIEW_BUNDLE_v02":
            if not isinstance(data.get("capture_sets"), list) or not data.get("capture_sets"):
                errors.append("v02+ bundle missing capture_sets metadata")
        if schema and schema >= "NMS_AI_REVIEW_BUNDLE_v03":
            if data.get("max_images") is None:
                warnings.append("v03+ bundle missing max_images budget metadata")
            if data.get("image_format") is None:
                warnings.append("v03+ bundle missing image_format metadata")
        if schema and schema >= "NMS_AI_REVIEW_BUNDLE_v04":
            diag = data.get("diagnostics") or {}
            if not isinstance(diag, dict):
                warnings.append("v04 bundle diagnostics missing or malformed")

        oid_counts = {}
        missing_oid = 0
        nonuniform = 0
        non_nms = []
        collections = {}
        review_required = 0
        for o in objects:
            oid = _object_id(o)
            if oid:
                oid_counts[oid] = oid_counts.get(oid, 0) + 1
            else:
                missing_oid += 1
                name = o.get("name") if isinstance(o, dict) else None
                if name:
                    non_nms.append(name)
            st = _scale_tuple(o)
            if st and (abs(st[0]-st[1]) > 1e-6 or abs(st[0]-st[2]) > 1e-6):
                nonuniform += 1
            if isinstance(o, dict) and o.get("review_required"):
                review_required += 1
            for c in _collections_of(o) if isinstance(o, dict) else []:
                collections[c] = collections.get(c, 0) + 1

        single_collection = len(collections) <= 1 and len(objects) > 1
        if single_collection:
            # This is not an error because v04 handles it via fallback.
            labels = [str(cs.get("label", "")).upper() for cs in capture_sets if isinstance(cs, dict)]
            has_fallback = any(("NAME_CLUSTER" in x or "SPATIAL" in x or "GEOMETRIC" in x or "INTERIOR" in x) for x in labels)
            if not has_fallback:
                warnings.append("all objects appear in one collection and no name/spatial/geometric fallback capture set is declared")

        metrics["schema"] = schema
        metrics["created_at"] = data.get("created_at") if isinstance(data, dict) else None
        metrics["blender_version"] = data.get("blender_version") if isinstance(data, dict) else None
        metrics["scene"] = (data.get("scene") or data.get("scene_name")) if isinstance(data, dict) else None
        metrics["object_count"] = data.get("object_count", len(objects)) if isinstance(data, dict) else len(objects)
        metrics["generated_nms_object_count"] = sum(oid_counts.values())
        metrics["missing_objectid_count"] = missing_oid
        metrics["nonuniform_scale_count"] = nonuniform
        metrics["review_required_count"] = review_required
        metrics["screenshot_count"] = len(image_names)
        metrics["capture_set_count"] = len(capture_sets)
        metrics["unique_collection_count"] = len(collections)
        metrics["single_collection_warning"] = single_collection
        metrics["non_nms_or_default_objects"] = non_nms[:25]
        metrics["top_objectids"] = sorted(oid_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:25]
        metrics["top_collections"] = sorted(collections.items(), key=lambda kv: (-kv[1], kv[0]))[:25]
        metrics["capture_sets"] = [
            {
                "label": cs.get("label"),
                "object_count": cs.get("object_count"),
                "views": len(cs.get("views", [])) if isinstance(cs.get("views"), list) else None,
                "folder": cs.get("folder"),
            }
            for cs in capture_sets if isinstance(cs, dict)
        ]

        if missing_oid:
            warnings.append(f"{missing_oid} object(s) have no ObjectID; check for default cube/proxy/non-NMS objects")
    return errors, warnings, metrics

def self_test():
    with tempfile.TemporaryDirectory() as td:
        # v01 fixture
        zpath = os.path.join(td, "NMS_AI_REVIEW_Scene_test_v01.zip")
        data = {
            "schema": "NMS_AI_REVIEW_BUNDLE_v01",
            "created_at": "2026-06-16 00:00:00",
            "blender_version": "5.0.1",
            "scene": "Scene",
            "object_count": 2,
            "objects": [
                {"name": "NMS_TEST_A", "custom_properties": {"ObjectID": "S_FLOOR"}, "scale": [1,1,1], "collections": ["CORE"]},
                {"name": "Cube", "scale": [1,1,1], "collections": ["CORE"]}
            ]
        }
        with zipfile.ZipFile(zpath, "w") as z:
            z.writestr("NMS_AI_REVIEW_CHECKLIST.md", "# checklist")
            z.writestr("OPEN_TOPICS_LOG.md", "# open")
            z.writestr("nms_ai_review_objects.json", json.dumps(data))
            for e in V01_EXPECTED_SCREENSHOTS:
                z.writestr(e, b"not-real-image-fixture")
        errors, warnings, metrics = check_bundle(zpath)
        ok1 = not errors and metrics.get("generated_nms_object_count") == 1 and metrics.get("screenshot_count") == 8

        # v04 fixture with capture sets and single-collection fallback.
        zpath2 = os.path.join(td, "NMS_AI_REVIEW_V04_test.zip")
        data2 = {
            "schema": "NMS_AI_REVIEW_BUNDLE_v04",
            "created_at": "2026-06-16 00:00:00",
            "blender_version": "5.0.1",
            "scene": "Scene",
            "capture_profile": "STANDARD",
            "max_images": 12,
            "image_format": "JPEG",
            "object_count": 2,
            "diagnostics": {"single_collection_warning": True},
            "capture_sets": [
                {"label": "01_ALL_VISIBLE", "object_count": 2, "views": ["front"], "folder": "screenshots/01_ALL_VISIBLE"},
                {"label": "NAME_CLUSTER_BUILDING_A", "object_count": 1, "views": ["front"], "folder": "screenshots/NAME_CLUSTER_BUILDING_A"},
                {"label": "07_GEOMETRIC_INTERIOR_CANDIDATE", "object_count": 1, "views": ["front"], "folder": "screenshots/07_GEOMETRIC_INTERIOR_CANDIDATE"},
            ],
            "objects": [
                {"name": "BUILDING_A_FLOOR_001", "ObjectID": "B_FLOOR", "scale": [1,1,1], "collections": ["Collection"]},
                {"name": "BUILDING_A_DETAIL_001", "ObjectID": "BILLBOARD", "scale": [1,1,1], "collections": ["Collection"], "review_required": True}
            ]
        }
        with zipfile.ZipFile(zpath2, "w") as z:
            z.writestr("NMS_AI_REVIEW_CHECKLIST.md", "# checklist")
            z.writestr("OPEN_TOPICS_LOG.md", "# open")
            z.writestr("nms_ai_review_objects.json", json.dumps(data2))
            z.writestr("screenshots/01_ALL_VISIBLE/front.jpg", b"fixture")
            z.writestr("screenshots/NAME_CLUSTER_BUILDING_A/front.jpg", b"fixture")
            z.writestr("screenshots/07_GEOMETRIC_INTERIOR_CANDIDATE/front.jpg", b"fixture")
        errors2, warnings2, metrics2 = check_bundle(zpath2)
        ok2 = not errors2 and metrics2.get("schema") == "NMS_AI_REVIEW_BUNDLE_v04" and metrics2.get("capture_set_count") == 3

    ok = ok1 and ok2
    if ok:
        print("AI REVIEW BUNDLE CHECK SELF-TEST: PASS")
        return 0
    print("AI REVIEW BUNDLE CHECK SELF-TEST: FAIL")
    print("v01:", errors, warnings, metrics)
    print("v04:", errors2, warnings2, metrics2)
    return 2

def main(argv=None):
    argv = argv or sys.argv[1:]
    if argv == ["--self-test"]:
        return self_test()
    if not argv:
        print("usage: ai_review_bundle_check.py <NMS_AI_REVIEW*.zip> | --self-test")
        return 1
    try:
        errors, warnings, metrics = check_bundle(argv[0])
    except Exception as exc:
        print("AI REVIEW BUNDLE CHECK: FAIL")
        print("  FAIL:", exc)
        return 2
    if errors:
        print("AI REVIEW BUNDLE CHECK: FAIL")
        for e in errors:
            print("  FAIL:", e)
        return 2
    print("AI REVIEW BUNDLE CHECK: PASS")
    for k in ("schema", "created_at", "blender_version", "scene", "object_count", "generated_nms_object_count",
              "missing_objectid_count", "review_required_count", "screenshot_count", "capture_set_count",
              "unique_collection_count", "single_collection_warning"):
        print(f"  {k}: {metrics.get(k)}")
    if warnings:
        for w in warnings:
            print("  WARN:", w)
    print("  top_objectids:", metrics.get("top_objectids"))
    print("  top_collections:", metrics.get("top_collections"))
    print("  capture_sets:", metrics.get("capture_sets")[:12])
    return 0

if __name__ == "__main__":
    sys.exit(main())
