#!/usr/bin/env python3
"""AI capture compliance checker (3.00.00).

Static checker for generated Blender/NMS scripts. It verifies that build scripts
are organized for visual review: semantic collections/roles, object metadata,
review-required isolation, and fallback declarations when appropriate.

This is a review-readiness gate. It does not evaluate visual quality and it does
not replace run_gate/no-float/exported JSON validation.
"""
import ast
import json
import re
import sys

BUILD_REQUEST_TYPES = {
    "build_generation",
    "new_geometry_synthesis",
    "build_refinement",
    "build_refinement_or_optimization",
    "part_behavior_learning",
    "rule_discovery_and_proof",
}

EXTERIOR_TOKENS = ("FRONT", "FOCAL", "EXTERIOR", "SHELL", "STRUCTURAL", "WALL", "ROOF", "FACADE")
INTERIOR_TOKENS = ("INTERIOR", "ROOM", "INSIDE", "CEILING", "FLOOR", "ACCESS", "WALKWAY", "CONTROL")
DECOR_TOKENS = ("DECOR", "LIGHT", "REVIEW", "ACCENT", "GOLD", "DETAIL", "EXPERIMENTAL")
SCENE_TOKENS = ("SCENE", "CITY", "GOTHAM", "SKYLINE", "PLAZA", "CONTEXT", "EXPERIMENTAL")

REQUIRED_METADATA_FIELDS = {"role", "collection_role", "review_required", "placement_method", "source_docs_rev"}

def _literal_assignments(tree):
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    try:
                        out[t.id] = ast.literal_eval(node.value)
                    except Exception:
                        pass
    return out

def _request_type(assigns):
    rc = assigns.get("REQUEST_CLASSIFICATION")
    if isinstance(rc, dict):
        return rc.get("request_type")
    return None

def _string_blob(value):
    if isinstance(value, str):
        return value.upper()
    if isinstance(value, dict):
        return " ".join(_string_blob(k) + " " + _string_blob(v) for k, v in value.items())
    if isinstance(value, (list, tuple, set)):
        return " ".join(_string_blob(v) for v in value)
    return str(value).upper()

def _manifest(assigns):
    for key in ("AI_CAPTURE_COMPLIANCE", "AI_REVIEW_CAPTURE_COMPLIANCE", "VISUAL_REVIEW_COMPLIANCE"):
        val = assigns.get(key)
        if isinstance(val, dict):
            return key, val
    return None, None

def _semantic_names(manifest, src):
    names = []
    for key in ("semantic_collections", "semantic_roles", "capture_sets", "review_collections"):
        val = manifest.get(key) if isinstance(manifest, dict) else None
        if isinstance(val, dict):
            names.extend([str(k) for k in val.keys()])
            names.extend([str(v) for v in val.values() if isinstance(v, str)])
        elif isinstance(val, (list, tuple, set)):
            names.extend([str(v) for v in val])
    for m in re.finditer(r'["\']([A-Z0-9_]*(?:INTERIOR|FRONT|FOCAL|SHELL|STRUCTURAL|ACCESS|DECOR|SCENE|GOTHAM|LIGHT|DETAIL|EXTERIOR|WALL|CEILING|PLAZA|SKYLINE)[A-Z0-9_]*)["\']', src, flags=re.I):
        names.append(m.group(1))
    return sorted(set(names))

def _has_any(names, tokens):
    blob = " ".join(str(n).upper() for n in names)
    return any(t in blob for t in tokens)

def _looks_like_build(src, request_type):
    if request_type in BUILD_REQUEST_TYPES:
        return True
    if "BUILDER.add_part" in src or ".add_part(" in src:
        if "REQUEST_CLASSIFICATION" in src:
            return True
    return False

def _building_intent(src):
    return bool(re.search(r"\b(building|room|interior|city|gotham|tower|shell|enclosure|hangar|base)\b", src, re.I))

def _scene_intent(src):
    return bool(re.search(r"\b(gotham|city|scene|skyline|plaza|street|district|context)\b", src, re.I))

def _review_required_present(src):
    return bool(re.search(r"\breview_required\b|REVIEW_REQUIRED|_REVIEW", src, re.I))

def _metadata_fields_declared(manifest, src):
    fields = set()
    val = manifest.get("object_metadata_fields") if isinstance(manifest, dict) else None
    if isinstance(val, (list, tuple, set)):
        fields.update(str(v) for v in val)
    for f in REQUIRED_METADATA_FIELDS:
        if re.search(rf'["\']{re.escape(f)}["\']\s*\]', src) or re.search(rf'\b{re.escape(f)}\b', src):
            fields.add(f)
    return fields

def check_source(src):
    errors = []
    warnings = []
    metrics = {}

    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return [f"syntax error: {exc}"], warnings, metrics

    assigns = _literal_assignments(tree)
    req_type = _request_type(assigns)
    key, manifest = _manifest(assigns)
    is_build = _looks_like_build(src, req_type)
    building = _building_intent(src)
    scene = _scene_intent(src)
    review_required = _review_required_present(src)

    metrics["request_type"] = req_type
    metrics["is_build_script"] = is_build
    metrics["building_or_room_intent"] = building
    metrics["scene_intent"] = scene
    metrics["review_required_present"] = review_required
    metrics["manifest_name"] = key

    if not is_build:
        metrics["not_applicable"] = True
        return errors, warnings, metrics

    if not isinstance(manifest, dict):
        errors.append("missing AI_CAPTURE_COMPLIANCE manifest")
        manifest = {}

    schema = manifest.get("schema")
    if schema != "NMS_AI_CAPTURE_COMPLIANCE_v1":
        errors.append("AI_CAPTURE_COMPLIANCE.schema must be NMS_AI_CAPTURE_COMPLIANCE_v1")

    names = _semantic_names(manifest, src)
    metrics["semantic_name_count"] = len(names)
    metrics["semantic_names"] = names[:50]

    single_fallback = bool(manifest.get("single_collection_fallback_declared"))
    metrics["single_collection_fallback_declared"] = single_fallback

    has_exterior = _has_any(names, EXTERIOR_TOKENS)
    has_interior = _has_any(names, INTERIOR_TOKENS)
    has_decor = _has_any(names, DECOR_TOKENS)
    has_scene = _has_any(names, SCENE_TOKENS)

    metrics["has_exterior_role"] = has_exterior
    metrics["has_interior_role"] = has_interior
    metrics["has_decor_or_review_role"] = has_decor
    metrics["has_scene_role"] = has_scene

    if len(names) < 2 and not single_fallback:
        errors.append("fewer than two semantic collection/role names and no single_collection_fallback_declared")

    if building and not (has_exterior and has_interior):
        errors.append("building/room/city intent requires both exterior/shell/focal and interior/access roles")

    if scene and not has_scene:
        errors.append("scene/city/Gotham intent requires separate scene/context role")

    if review_required and not has_decor:
        errors.append("review_required/experimental/decor parts require a decor/review role")

    fields = _metadata_fields_declared(manifest, src)
    metrics["metadata_fields_declared"] = sorted(fields)
    missing_fields = sorted(REQUIRED_METADATA_FIELDS - fields)
    if missing_fields:
        errors.append("missing object metadata fields: " + ", ".join(missing_fields))

    strategy = str(manifest.get("capture_strategy", "")).lower()
    if building and not any(x in strategy for x in ("cutaway", "interior", "semantic", "section")):
        warnings.append("capture_strategy should mention semantic/interior/cutaway/section review for building requests")

    min_addon = str(manifest.get("review_bundle_addon_min_version", ""))
    if min_addon and not re.search(r"v0?4|4", min_addon, re.I):
        warnings.append("review_bundle_addon_min_version is below v04; v04 is recommended for single-collection fallback/no-op detection")

    return errors, warnings, metrics

def check_file(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return check_source(f.read())

def self_test():
    good = """
from bl_ext.user_default.no_mans_sky_base_builder import BUILDER
REQUEST_CLASSIFICATION = {"request_type": "build_generation"}
AI_CAPTURE_COMPLIANCE = {
    "schema": "NMS_AI_CAPTURE_COMPLIANCE_v1",
    "source_docs_rev": "3.00.00",
    "capture_strategy": "semantic_collections_plus_interior_cutaways",
    "semantic_collections": [
        "ACCESS_AND_INTERIOR",
        "FRONT_FOCAL_FACE",
        "STRUCTURAL_SHELL",
        "INTERIOR_ARCHITECTURE",
        "DECOR_LIGHT_REVIEW",
        "SCENE_EXPERIMENTAL",
    ],
    "object_metadata_fields": ["role", "collection_role", "review_required", "placement_method", "source_docs_rev"],
    "single_collection_fallback_declared": False,
    "review_bundle_addon_min_version": "v04",
}
obj = BUILDER.add_part("S_FLOOR").object
obj["ObjectID"] = "S_FLOOR"
obj["role"] = "INTERIOR_ARCHITECTURE"
obj["collection_role"] = "INTERIOR_ARCHITECTURE"
obj["review_required"] = False
obj["placement_method"] = "fixture"
obj["source_docs_rev"] = "3.00.00"
"""
    bad = """
from bl_ext.user_default.no_mans_sky_base_builder import BUILDER
REQUEST_CLASSIFICATION = {"request_type": "build_generation"}
obj = BUILDER.add_part("S_FLOOR").object
obj["ObjectID"] = "S_FLOOR"
"""
    e1, w1, m1 = check_source(good)
    e2, w2, m2 = check_source(bad)
    ok = (not e1 and e2 and any("AI_CAPTURE_COMPLIANCE" in e for e in e2))
    if ok:
        print("AI CAPTURE COMPLIANCE CHECK SELF-TEST: PASS")
        return 0
    print("AI CAPTURE COMPLIANCE CHECK SELF-TEST: FAIL")
    print("good:", e1, w1, m1)
    print("bad:", e2, w2, m2)
    return 2

def main(argv=None):
    argv = argv or sys.argv[1:]
    if argv == ["--self-test"]:
        return self_test()
    if not argv:
        print("usage: ai_capture_compliance_check.py <generated_script.py> | --self-test")
        return 1
    try:
        errors, warnings, metrics = check_file(argv[0])
    except Exception as exc:
        print("AI CAPTURE COMPLIANCE CHECK: FAIL")
        print("  FAIL:", exc)
        return 2
    if errors:
        print("AI CAPTURE COMPLIANCE CHECK: FAIL")
        for e in errors:
            print("  FAIL:", e)
        for w in warnings:
            print("  WARN:", w)
        print("  metrics:", json.dumps(metrics, indent=2, sort_keys=True))
        return 2
    print("AI CAPTURE COMPLIANCE CHECK: PASS")
    for w in warnings:
        print("  WARN:", w)
    print("  metrics:", json.dumps(metrics, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
