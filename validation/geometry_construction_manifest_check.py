#!/usr/bin/env python3
"""geometry_construction_manifest_check.py — enforce focal/complex build geometry plan receipts."""
import ast, sys

BAD_METHOD_WORDS = {"centroid_scatter", "generic_visual_sprinkle", "random_fill", "sprinkle"}

def assignment(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        return None
    return None

def flatten_strings(x):
    out = []
    if isinstance(x, str):
        out.append(x)
    elif isinstance(x, dict):
        for k,v in x.items():
            out.extend(flatten_strings(k)); out.extend(flatten_strings(v))
    elif isinstance(x, (list, tuple, set)):
        for v in x: out.extend(flatten_strings(v))
    return out

def check_script(path):
    src = open(path, encoding="utf-8", errors="ignore").read()
    tree = ast.parse(src, filename=path)
    fails = []
    plan = assignment(tree, "GEOMETRY_CONSTRUCTION_PLAN")
    if not isinstance(plan, dict):
        fails.append("GEOMETRY_CONSTRUCTION_PLAN missing or not a literal dict")
        plan = {}
    for key in ("construction_mode", "recognizable_features", "placement_derivation", "visual_conformance_checks"):
        if key not in plan:
            fails.append(f"GEOMETRY_CONSTRUCTION_PLAN missing {key}")
    mode = str(plan.get("construction_mode", "")).lower()
    deriv = str(plan.get("placement_derivation", "")).lower()
    if any(w in mode or w in deriv for w in BAD_METHOD_WORDS):
        fails.append("forbidden scatter/sprinkle placement derivation")
    if "C_TRIFLOOR" in src:
        if not any(k in src for k in ("C_TRIFLOOR_EDGE_GRAPH", "SURFACE_MESH_CONTRACT", "CURVE_FOLLOW_CONTRACT", "GEOMETRY_CONSTRUCTION_PLAN")):
            fails.append("C_TRIFLOOR build lacks edge/surface/curve geometry contract")
        strings = " ".join(flatten_strings(plan)).lower()
        if "edge" not in strings and "surface" not in strings and "curve" not in strings and "mesh" not in strings:
            fails.append("C_TRIFLOOR geometry plan does not identify edge/surface/curve/mesh derivation")
    return fails

def main():
    if len(sys.argv) < 2:
        print("usage: geometry_construction_manifest_check.py <script.py>")
        return 2
    try:
        fails = check_script(sys.argv[1])
    except Exception as e:
        print("GEOMETRY CONSTRUCTION MANIFEST CHECK: FAIL")
        print("  FAIL:", e)
        return 1
    print("GEOMETRY CONSTRUCTION MANIFEST CHECK")
    if fails:
        for f in fails: print("  FAIL:", f)
        print("GEOMETRY CONSTRUCTION MANIFEST CHECK: FAIL")
        return 1
    print("  geometry construction plan present")
    print("GEOMETRY CONSTRUCTION MANIFEST CHECK: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
