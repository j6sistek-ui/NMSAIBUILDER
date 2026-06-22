#!/usr/bin/env python3
"""Feature recipe lookup receipt checker (2.19.00).

Checks generated Python source for known feature terms from
rules/PROMPT_TO_FEATURE_ROUTER.json. If a known feature term is present, the script
must include a literal FEATURE_RECIPE_LOOKUP dict with required fields.
"""
import ast
import json
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED_FIELDS = [
    "feature_intent",
    "matched_recipe_or_signature",
    "recipe_files_checked",
    "recipe_status",
    "reason_if_none",
    "part_map_role",
]
VALID_STATUSES = {"exact_json", "validated_recipe", "toolkit_recipe", "provisional", "none_found"}

def read(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()

def router_terms():
    path = os.path.join(ROOT, "rules", "PROMPT_TO_FEATURE_ROUTER.json")
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception:
        return []
    terms = []
    for route in data.get("routes", []):
        for term in route.get("terms", []):
            t = str(term).strip().lower()
            if t:
                terms.append(t)
    # Add object/assembly words that often appear in generated source even when the user's prompt is absent.
    terms.extend(["wall_shell", "tower_shell", "airlock", "iris", "stair", "ramp", "skybridge", "building", "tower", "wall"])
    return sorted(set(terms), key=lambda x: (-len(x), x))

def detect_known_terms(src):
    low = src.lower()
    hits = []
    for term in router_terms():
        # ObjectID-like WALL tokens and source identifiers should count; ordinary short terms use word boundaries.
        if " " in term or "_" in term:
            if term in low:
                hits.append(term)
        else:
            if re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", low):
                hits.append(term)
    return sorted(set(hits))

def extract_manifest(src):
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "FEATURE_RECIPE_LOOKUP":
                    try:
                        return ast.literal_eval(node.value)
                    except Exception as exc:
                        raise ValueError(f"FEATURE_RECIPE_LOOKUP is not a literal dict: {exc}")
    return None

def validate_manifest(m):
    errors = []
    if not isinstance(m, dict):
        return ["FEATURE_RECIPE_LOOKUP missing or not a dict"]
    for field in REQUIRED_FIELDS:
        if field not in m:
            errors.append(f"missing field: {field}")
    status = str(m.get("recipe_status", ""))
    if status and status not in VALID_STATUSES:
        errors.append(f"invalid recipe_status: {status}")
    checked = m.get("recipe_files_checked")
    if not isinstance(checked, list) or not checked:
        errors.append("recipe_files_checked must be a non-empty list")
    matched = str(m.get("matched_recipe_or_signature", ""))
    if status != "none_found" and not matched:
        errors.append("matched_recipe_or_signature required unless recipe_status is none_found")
    if status == "none_found" and not str(m.get("reason_if_none", "")).strip():
        errors.append("reason_if_none required when recipe_status is none_found")
    pm = str(m.get("part_map_role", ""))
    if pm not in {"component_validation_only", "component_geometry_support", "fallback_geometry"}:
        errors.append("part_map_role must be component_validation_only, component_geometry_support, or fallback_geometry")
    return errors

def check_file(path):
    src = read(path)
    hits = detect_known_terms(src)
    manifest = extract_manifest(src)
    errors = []
    if hits and manifest is None:
        errors.append("known feature terms detected but FEATURE_RECIPE_LOOKUP is missing: " + ", ".join(hits[:12]))
    if manifest is not None:
        errors.extend(validate_manifest(manifest))
    return hits, errors

def self_test():
    good = '''
REQUEST_CLASSIFICATION = {"request_type": "build_generation"}
FEATURE_RECIPE_LOOKUP = {
    "feature_intent": "wall shell",
    "matched_recipe_or_signature": "wall_shell_enclosure_recipe_v2_19_00",
    "recipe_files_checked": ["rules/WALL_SHELL_ENCLOSURE_RECIPE.md"],
    "recipe_status": "validated_recipe",
    "reason_if_none": "",
    "part_map_role": "component_validation_only"
}
# build wall tower shell
'''
    bad = '''
REQUEST_CLASSIFICATION = {"request_type": "build_generation"}
# build wall tower shell without recipe receipt
'''
    none = 'REQUEST_CLASSIFICATION = {"request_type": "general_help"}\nvalue = 1\n'
    with tempfile.TemporaryDirectory() as td:
        paths = []
        for name, text in [("good.py", good), ("bad.py", bad), ("none.py", none)]:
            p = os.path.join(td, name)
            open(p, "w", encoding="utf-8").write(text)
            paths.append(p)
        gh, ge = check_file(paths[0])
        bh, be = check_file(paths[1])
        nh, ne = check_file(paths[2])
    ok = bool(gh) and not ge and bool(bh) and be and not ne
    if ok:
        print("FEATURE RECIPE LOOKUP CHECK SELF-TEST: PASS")
        return 0
    print("FEATURE RECIPE LOOKUP CHECK SELF-TEST: FAIL")
    print("good", gh, ge)
    print("bad", bh, be)
    print("none", nh, ne)
    return 2

def main(argv=None):
    argv = argv or sys.argv[1:]
    if argv == ["--self-test"]:
        return self_test()
    if not argv:
        print("usage: feature_recipe_lookup_check.py <generated_script.py> | --self-test")
        return 1
    path = argv[0]
    try:
        hits, errors = check_file(path)
    except Exception as exc:
        print("FEATURE RECIPE LOOKUP CHECK: FAIL")
        print("  FAIL:", exc)
        return 2
    if errors:
        print("FEATURE RECIPE LOOKUP CHECK: FAIL")
        for e in errors:
            print("  FAIL:", e)
        return 2
    if hits:
        print("FEATURE RECIPE LOOKUP CHECK: PASS")
        print("  known feature terms:", ", ".join(hits[:20]))
    else:
        print("FEATURE RECIPE LOOKUP CHECK: PASS")
        print("  known feature terms: none detected; receipt not required")
    return 0

if __name__ == "__main__":
    sys.exit(main())
