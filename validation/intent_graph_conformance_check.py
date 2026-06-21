#!/usr/bin/env python3
"""
intent_graph_conformance_check.py — composite build connected-component gate.

This gate makes BUILD_INTENT_GRAPH falsifiable against exported geometry. It does
not replace visual review, but it catches the failure where a full build is
internally made of connected subassemblies that never connect to each other.

Inputs:
    intent_graph_conformance_check.py <generated_script.py> <exported_nms.json> [library_json_or_empty] [package_root]

It reads BUILD_INTENT_GRAPH from the script and compares expected connected
component count to observed component count inferred from exported ObjectID
positions and dimension-library extents.
"""
import ast, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TOL = 0.75

def _clean(o):
    return str(o or "").lstrip("^")

def _dist(a,b):
    return math.sqrt(sum((float(a[i])-float(b[i]))**2 for i in range(3)))

def _radius_for(oid, dims):
    d = dims.get(_clean(oid), {})
    vals = []
    for k in ("extent_x","extent_y","extent_z"):
        try:
            vals.append(float(d.get(k)))
        except Exception:
            pass
    if not vals:
        return 2.5
    # Use a conservative bounding-sphere radius. This can over-connect large parts,
    # but it is far better than allowing an intended one-piece build to silently
    # split into dozens of islands.
    return max(vals) * 0.5

def _load_dims(libpath, root):
    if not libpath:
        libpath = os.path.join(root, "library", "nms_part_dimensions_and_rules_updated.json")
    if not os.path.isabs(libpath):
        libpath = os.path.join(root, libpath)
    try:
        data = json.load(open(libpath, encoding="utf-8"))
    except Exception:
        data = []
    out = {}
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get("ObjectID"):
                out[_clean(item.get("ObjectID"))] = item
    elif isinstance(data, dict):
        for k,v in data.items():
            if isinstance(v, dict):
                out[_clean(k)] = v
    return out

def _assignment(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        return None
    return None

def _load_export(path):
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("parts", data.get("objects", data.get("Objects", [])))
    out = []
    for obj in data or []:
        if not isinstance(obj, dict):
            continue
        pos = obj.get("Position")
        oid = _clean(obj.get("ObjectID"))
        if oid and isinstance(pos, list) and len(pos) >= 3:
            out.append({"oid": oid, "P": [float(pos[0]), float(pos[1]), float(pos[2])]})
    return out

def _components(parts, dims, tol=DEFAULT_TOL):
    n = len(parts)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a,b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    radii = [_radius_for(p["oid"], dims) for p in parts]
    for i in range(n):
        for j in range(i+1,n):
            # approximate contact/shell overlap using sphere proxy
            if _dist(parts[i]["P"], parts[j]["P"]) <= radii[i] + radii[j] + tol:
                union(i,j)
    groups = {}
    for i,p in enumerate(parts):
        groups.setdefault(find(i), []).append(p)
    return list(groups.values())

def check(script_path, exported_json, libpath="", root=ROOT):
    src = open(script_path, encoding="utf-8", errors="ignore").read()
    tree = ast.parse(src, filename=script_path)
    graph = _assignment(tree, "BUILD_INTENT_GRAPH")
    fails, warns = [], []
    if not isinstance(graph, dict):
        fails.append("BUILD_INTENT_GRAPH missing or not a literal dict")
        graph = {}
    try:
        expected = int(graph.get("expected_connected_components"))
    except Exception:
        expected = None
        fails.append("BUILD_INTENT_GRAPH.expected_connected_components missing or not an integer")
    subassemblies = graph.get("subassemblies_intended")
    if subassemblies is False and expected is not None and expected != 1:
        fails.append("subassemblies_intended=False requires expected_connected_components=1")

    dims = _load_dims(libpath, root)
    parts = _load_export(exported_json)
    comps = _components(parts, dims)
    observed = len(comps)

    if expected is not None and observed != expected:
        fails.append(f"observed connected components {observed} != expected {expected}")

    if subassemblies is False and observed != 1:
        fails.append("fully connected build expected but exported geometry is disconnected")

    # Warn on suspicious fragmentation even if the user allowed subassemblies.
    if observed > 12:
        warns.append(f"observed {observed} connected components; if intentional, document subassembly roles explicitly")

    ok = not fails
    print("INTENT GRAPH CONFORMANCE CHECK")
    print(f"  exported parts: {len(parts)}")
    print(f"  expected connected components: {expected}")
    print(f"  observed connected components: {observed}")
    print(f"  subassemblies_intended: {subassemblies}")
    sizes = sorted([len(c) for c in comps], reverse=True)
    print(f"  component sizes: {sizes[:20]}")
    for w in warns:
        print("  WARN:", w)
    for f in fails:
        print("  FAIL:", f)
    print("INTENT GRAPH CONFORMANCE CHECK:", "PASS" if ok else "FAIL")
    return 0 if ok else 2

def main():
    if len(sys.argv) < 3:
        print("usage: intent_graph_conformance_check.py <generated_script.py> <exported_nms.json> [library_json_or_empty] [package_root]")
        return 1
    root = sys.argv[4] if len(sys.argv) > 4 else ROOT
    return check(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "", root)

if __name__ == "__main__":
    sys.exit(main())
