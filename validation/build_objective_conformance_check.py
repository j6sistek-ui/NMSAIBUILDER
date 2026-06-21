#!/usr/bin/env python3
"""
build_objective_conformance_check.py — build-level objective gate.

This gate is intentionally higher-level than part-level recipe checks.  It checks
that a generated build's exported geometry satisfies common user-intent
constraints, especially connected walkable paths and prohibited unintended
subassembly gaps.

Inputs:
    build_objective_conformance_check.py <generated_script.py> <exported_nms.json> [library_json_or_empty] [package_root]

Current executable checks:
  - BUILD_INTENT_GRAPH must be present.
  - If subassemblies_intended is False, expected_connected_components must be 1.
  - S_FLOOR path continuity: each structural floor must have a nearby floor,
    ramp-semantic neighbor, or other declared connector unless explicitly exempt.
    This catches isolated/floating floor panels that a coarse component gate can
    miss because nearby shell geometry over-connects the build.
  - Suspicious floor-to-floor gaps in an otherwise linear path are reported.
"""
from __future__ import annotations
import ast, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FLOOR_ID = "S_FLOOR"
RAMP_ID = "S_RAMP"
FLOOR_STEP_DEFAULT = 5.244682
RUN_STEP_DEFAULT = 5.253329776
RISE_STEP_DEFAULT = 3.28333
EDGE_START_DEFAULT = 5.248783112

def _clean(o):
    return str(o or "").lstrip("^")

def _dist(a, b):
    return math.sqrt(sum((float(a[i]) - float(b[i])) ** 2 for i in range(3)))

def _norm(v):
    L = math.sqrt(sum(float(x)*float(x) for x in v))
    return [0.0,0.0,0.0] if L <= 1e-9 else [float(v[0])/L, float(v[1])/L, float(v[2])/L]

def _dot(a,b):
    return sum(float(a[i])*float(b[i]) for i in range(3))

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
    for idx,obj in enumerate(data or []):
        if not isinstance(obj, dict):
            continue
        pos = obj.get("Position")
        oid = _clean(obj.get("ObjectID"))
        if oid and isinstance(pos, list) and len(pos) >= 3:
            out.append({
                "idx": idx,
                "oid": oid,
                "P": [float(pos[0]), float(pos[1]), float(pos[2])],
                "Up": obj.get("Up", [0,1,0]),
                "At": obj.get("At", [1,0,0]),
                "raw": obj,
            })
    return out

def _floor_has_floor_neighbor(f, floors, tol=0.40):
    for g in floors:
        if g is f:
            continue
        d = _dist(f["P"], g["P"])
        if d <= FLOOR_STEP_DEFAULT + tol:
            return True
    return False

def _floor_has_ramp_semantic_neighbor(f, ramps, tol=0.65):
    # A floor may touch a ramp at either the start edge or terminal landing relation.
    P = f["P"]
    for r in ramps:
        R = r["P"]
        at = _norm(r.get("At", [1,0,0]))
        up = _norm(r.get("Up", [0,1,0]))
        candidates = [
            # floor center behind first ramp by edge-start
            [R[i] - at[i] * EDGE_START_DEFAULT for i in range(3)],
            # terminal lattice floor after ramp
            [R[i] + at[i] * RUN_STEP_DEFAULT + up[i] * RISE_STEP_DEFAULT for i in range(3)],
            # turn/edge landing after ramp
            [R[i] + at[i] * EDGE_START_DEFAULT + up[i] * RISE_STEP_DEFAULT for i in range(3)],
        ]
        for C in candidates:
            if _dist(P, C) <= tol:
                return True
    return False

def _floor_path_gap_fails(floors):
    # Detect linear path gaps by sorting floors that share nearly identical Y/Z lanes.
    fails = []
    by_lane = {}
    for f in floors:
        y = round(f["P"][1], 2)
        z = round(f["P"][2], 2)
        by_lane.setdefault((y,z), []).append(f)
    for lane, fs in by_lane.items():
        if len(fs) < 3:
            continue
        fs = sorted(fs, key=lambda x: x["P"][0])
        for a,b in zip(fs, fs[1:]):
            gap = _dist(a["P"], b["P"])
            # Allow exactly one floor step plus tolerance; larger gaps on a floor lane are suspect.
            if gap > FLOOR_STEP_DEFAULT + 0.75:
                fails.append(f"S_FLOOR path gap {gap:.3f}u on lane {lane} between export indexes {a['idx']} and {b['idx']}")
    return fails

def check(script_path, exported_json, libpath="", root=ROOT):
    src = open(script_path, encoding="utf-8", errors="ignore").read()
    tree = ast.parse(src, filename=script_path)
    graph = _assignment(tree, "BUILD_INTENT_GRAPH")
    fails, warns = [], []

    if not isinstance(graph, dict):
        fails.append("BUILD_INTENT_GRAPH missing or not a literal dict")
        graph = {}

    if graph.get("subassemblies_intended") is False:
        try:
            expected = int(graph.get("expected_connected_components"))
            if expected != 1:
                fails.append("subassemblies_intended=False requires expected_connected_components=1")
        except Exception:
            fails.append("expected_connected_components missing or invalid for connected build")

    parts = _load_export(exported_json)
    floors = [p for p in parts if p["oid"] == FLOOR_ID]
    ramps = [p for p in parts if p["oid"] == RAMP_ID]

    isolated_floors = []
    for f in floors:
        if _floor_has_floor_neighbor(f, floors) or _floor_has_ramp_semantic_neighbor(f, ramps):
            continue
        isolated_floors.append(f)

    if isolated_floors:
        for f in isolated_floors[:20]:
            fails.append(f"S_FLOOR export index {f['idx']} appears isolated/floating at {f['P']}")
        if len(isolated_floors) > 20:
            fails.append(f"{len(isolated_floors)-20} additional isolated S_FLOOR panels omitted from report")

    fails.extend(_floor_path_gap_fails(floors))

    # A connected user-intent build should not be mostly shell with a disconnected floor path.
    if graph.get("subassemblies_intended") is False and floors and ramps:
        if len(floors) < 2:
            fails.append("connected build has fewer than two floors despite floor/path intent")

    ok = not fails
    print("BUILD OBJECTIVE CONFORMANCE CHECK")
    print(f"  exported parts: {len(parts)}")
    print(f"  floors: {len(floors)}")
    print(f"  ramps: {len(ramps)}")
    print(f"  subassemblies_intended: {graph.get('subassemblies_intended')}")
    print(f"  expected_connected_components: {graph.get('expected_connected_components')}")
    for w in warns:
        print("  WARN:", w)
    for f in fails:
        print("  FAIL:", f)
    print("BUILD OBJECTIVE CONFORMANCE CHECK:", "PASS" if ok else "FAIL")
    return 0 if ok else 2

def main():
    if len(sys.argv) < 3:
        print("usage: build_objective_conformance_check.py <generated_script.py> <exported_nms.json> [library_json_or_empty] [package_root]")
        return 1
    root = sys.argv[4] if len(sys.argv) > 4 else ROOT
    return check(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "", root)

if __name__ == "__main__":
    sys.exit(main())
