#!/usr/bin/env python3
"""
validated_logic_reuse_check.py — machine-checkable receipt gate.

Checks that generated scripts using validated parts include:
- USED_PART_LOGIC manifest
- BUILD_INTENT_GRAPH manifest for composite builds
- validated parts reference their partmap and algorithm
- unvalidated parts are marked provisional/experimental instead of silently treated as solved
"""
import ast, csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VALIDATED_STATUSES = {"SCRIPT_VALIDATED", "BLENDER_USER_CHECK", "BLENDER_SYSTEMATIC", "GAME_VALIDATED"}
PROVISIONAL_MODES = {"PROVISIONAL_BLOCK_OR_REVIEW", "EXPERIMENTAL_VARIANT"}
VALIDATED_MODES = {"DIRECT_REUSE", "IMPORTED_RECIPE", "ADAPTED_VERIFIED", "EXPERIMENTAL_VARIANT"}

def load_index(root):
    path = os.path.join(root, "library", "part_placement_maps", "part_placement_map_index.json")
    if not os.path.exists(path):
        return {}
    d = json.load(open(path, encoding="utf-8"))
    return d.get("parts", {}) if isinstance(d, dict) else {}

def get_assignment(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        return None
    return None

def string_literals(tree):
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            out.append(node.value)
    return out

def collect_used_parts(tree, known_parts):
    out = set()
    # PART_IDS = [...]
    part_ids = get_assignment(tree, "PART_IDS")
    if isinstance(part_ids, (list, tuple, set)):
        for p in part_ids:
            if isinstance(p, str) and p in known_parts:
                out.add(p)
    # ObjectID strings anywhere in source
    for s in string_literals(tree):
        if s in known_parts:
            out.add(s)
    return sorted(out)

def norm_status(s):
    return str(s or "").split("|")[0].strip()

def check_script(script, root=ROOT):
    src = open(script, encoding="utf-8", errors="ignore").read()
    tree = ast.parse(src, filename=script)
    index = load_index(root)
    known_parts = set(index.keys())

    used = collect_used_parts(tree, known_parts)
    used_logic = get_assignment(tree, "USED_PART_LOGIC")
    graph = get_assignment(tree, "BUILD_INTENT_GRAPH")

    fails, warns = [], []

    if not used:
        fails.append("no known ObjectIDs detected; cannot prove partmap/recipe reuse")

    if not isinstance(used_logic, dict):
        fails.append("USED_PART_LOGIC manifest missing or not a literal dict")
        used_logic = {}

    for pid in used:
        meta = index.get(pid, {})
        status = norm_status(meta.get("validation_status"))
        logic = used_logic.get(pid)
        if status in VALIDATED_STATUSES:
            if not isinstance(logic, dict):
                fails.append(f"{pid}: validated status {status} but no USED_PART_LOGIC entry")
                continue
            if not logic.get("partmap_path"):
                fails.append(f"{pid}: validated part missing partmap_path in USED_PART_LOGIC")
            expected_path = meta.get("partmap_path")
            if expected_path and logic.get("partmap_path") and logic.get("partmap_path") != expected_path:
                fails.append(f"{pid}: partmap_path mismatch: expected {expected_path}, got {logic.get('partmap_path')}")
            if not logic.get("validated_algorithm"):
                fails.append(f"{pid}: validated part missing validated_algorithm")
            if str(logic.get("reuse_mode")) not in VALIDATED_MODES:
                fails.append(f"{pid}: invalid reuse_mode for validated part: {logic.get('reuse_mode')}")
            inv = logic.get("source_transform_invariants", [])
            if not all(x in inv for x in ("Position", "Up", "At")):
                fails.append(f"{pid}: source_transform_invariants must include Position, Up, and At")
        else:
            if isinstance(logic, dict):
                mode = str(logic.get("reuse_mode"))
                if mode not in PROVISIONAL_MODES and not logic.get("validated_algorithm"):
                    fails.append(f"{pid}: unvalidated status {status or 'UNKNOWN'} must be provisional/experimental or have validated_algorithm")
            else:
                fails.append(f"{pid}: status {status or 'UNKNOWN'} requires USED_PART_LOGIC entry marking provisional/experimental")

    # build_generation/composite check
    request = get_assignment(tree, "REQUEST_CLASSIFICATION")
    req_type = request.get("request_type") if isinstance(request, dict) else ""
    likely_build = req_type in {"build_generation", "part_behavior_learning", "rule_discovery_and_proof"} or len(used) >= 2
    if likely_build:
        if not isinstance(graph, dict):
            fails.append("BUILD_INTENT_GRAPH missing or not a literal dict")
        else:
            if "subassemblies_intended" not in graph:
                fails.append("BUILD_INTENT_GRAPH.subassemblies_intended missing")
            if "expected_connected_components" not in graph:
                fails.append("BUILD_INTENT_GRAPH.expected_connected_components missing")
            else:
                try:
                    ecc = int(graph.get("expected_connected_components"))
                    if graph.get("subassemblies_intended") is False and ecc != 1:
                        fails.append("BUILD_INTENT_GRAPH: subassemblies_intended=False requires expected_connected_components=1")
                    if ecc < 1:
                        fails.append("BUILD_INTENT_GRAPH.expected_connected_components must be >= 1")
                except Exception:
                    fails.append("BUILD_INTENT_GRAPH.expected_connected_components must be an integer")
            if "required_connections" not in graph or not isinstance(graph.get("required_connections"), list):
                fails.append("BUILD_INTENT_GRAPH.required_connections must be a list")
            elif graph.get("subassemblies_intended") is False and len(graph.get("required_connections")) == 0:
                warns.append("BUILD_INTENT_GRAPH has no required_connections for a fully connected build")

    ok = not fails
    print("VALIDATED LOGIC REUSE CHECK")
    print(f"  script: {script}")
    print(f"  known parts detected: {len(used)} {used}")
    print(f"  USED_PART_LOGIC: {'present' if used_logic else 'missing'}")
    print(f"  BUILD_INTENT_GRAPH: {'present' if isinstance(graph, dict) else 'missing'}")
    for w in warns:
        print("  WARN:", w)
    for f in fails:
        print("  FAIL:", f)
    print("VALIDATED LOGIC REUSE CHECK:", "PASS" if ok else "FAIL")
    return 0 if ok else 2

def main():
    if len(sys.argv) < 2:
        print("usage: validated_logic_reuse_check.py <generated_script.py> [package_root]")
        return 1
    script = sys.argv[1]
    root = sys.argv[2] if len(sys.argv) > 2 else ROOT
    return check_script(script, root)

if __name__ == "__main__":
    sys.exit(main())
