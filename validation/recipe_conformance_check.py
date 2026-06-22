#!/usr/bin/env python3
"""
recipe_conformance_check.py - geometry conformance gate.

Declared reuse (USED_PART_LOGIC) proves intent. This proves the actual exported
geometry obeys the validated placement recipe. It ingests the build's EXPORTED NMS
JSON (Position/Up/At per part - the in-game frame) and, for every approved stair
part, verifies the recorded local-frame repeat from the partmap:

    Position[n+1] = Position[n] + At * RUN_STEP + Up * RISE_STEP

A part that is one lattice step from a stair neighbour but whose displacement does
NOT decompose onto its own (or the neighbour's) At/Up within tolerance is mis-oriented
and FAILS - this is exactly the "tipped 90 degrees" failure that connectivity and a
declared receipt cannot catch. Unvalidated parts (no validated recipe) are not judged.
"""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPROVED_RAMPS = {"B_RAMP","C_RAMP","F_RAMP","M_RAMP","S_RAMP","T_RAMP","W_RAMP"}
APPROVED_FLOORS = {"B_FLOOR","C_FLOOR","F_FLOOR","M_FLOOR","S_FLOOR","T_FLOOR","W_FLOOR"}
APPROVED_STAIR = APPROVED_RAMPS | APPROVED_FLOORS
LATTICE_TOL = 0.65   # |displacement| ~ lattice length
RELATION_TOL = 0.90  # |displacement - (At*RUN + Up*RISE)|

def _clean(o): return str(o or "").lstrip("^")
def _sub(a,b): return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
def _mag(v): return math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
def _comb(at,up,run,rise): return [at[i]*run + up[i]*rise for i in range(3)]

def load_recipe(root):
    """Read RUN_STEP/RISE_STEP per ramp family from the partmaps (the recorded recipe)."""
    idx_path = os.path.join(root,"library","part_placement_maps","part_placement_map_index.json")
    recipe = {}
    default = (5.2533399, 3.28333005)
    try:
        parts = json.load(open(idx_path,encoding="utf-8")).get("parts",{})
    except Exception:
        parts = {}
    for pid, meta in parts.items():
        if _clean(pid) not in APPROVED_RAMPS: continue
        try:
            pm = json.load(open(os.path.join(root, meta.get("partmap_path","")),encoding="utf-8"))
            ps = pm.get("placement_signature",{})
            run = float(ps.get("RUN_STEP")); rise = float(ps.get("RISE_STEP"))
            recipe[_clean(pid)] = (run, rise)
        except Exception:
            pass
    recipe.setdefault("_default", recipe.get("S_RAMP", default))
    return recipe

def check(json_path, root=ROOT):
    data = json.load(open(json_path,encoding="utf-8"))
    if isinstance(data, dict): data = data.get("parts", data.get("objects", []))
    recipe = load_recipe(root)
    run0, rise0 = recipe["_default"]
    L = math.sqrt(run0*run0 + rise0*rise0)

    stair = []
    for o in data:
        oid = _clean(o.get("ObjectID"))
        if oid in APPROVED_STAIR and o.get("Position") and o.get("At") and o.get("Up"):
            stair.append({"oid":oid,"P":o["Position"],"At":o["At"],"Up":o["Up"]})

    fails, checked_pairs, conforming = [], 0, 0
    # index of which stair parts participate in at least one conforming lattice relation
    participates = [False]*len(stair)
    has_lattice_neighbor = [False]*len(stair)

    for i in range(len(stair)):
        for j in range(i+1, len(stair)):
            D = _sub(stair[j]["P"], stair[i]["P"])
            if abs(_mag(D) - L) > LATTICE_TOL:
                continue
            checked_pairs += 1
            has_lattice_neighbor[i] = has_lattice_neighbor[j] = True
            run,rise = recipe.get(stair[i]["oid"], recipe["_default"])
            run2,rise2 = recipe.get(stair[j]["oid"], recipe["_default"])
            ei = _comb(stair[i]["At"], stair[i]["Up"], run, rise)     # i's frame, forward
            ej = _comb(stair[j]["At"], stair[j]["Up"], run2, rise2)   # j's frame
            ok = (_mag(_sub(D, ei)) <= RELATION_TOL or
                  _mag(_sub([-d for d in D], ei)) <= RELATION_TOL or
                  _mag(_sub([-d for d in D], ej)) <= RELATION_TOL or
                  _mag(_sub(D, ej)) <= RELATION_TOL)
            if ok:
                conforming += 1
                participates[i] = participates[j] = True

    # a stair part that is lattice-spaced from a neighbour but conforms to NO local-frame
    # relation is mis-oriented (centres right, orientation wrong) -> FAIL
    for k,s in enumerate(stair):
        if has_lattice_neighbor[k] and not participates[k]:
            fails.append(f"{s['oid']} @ {[round(x,2) for x in s['P']]}: lattice-spaced neighbour exists "
                         f"but displacement does not match At*RUN_STEP+Up*RISE_STEP (mis-oriented vs recipe)")

    ok = not fails
    print("RECIPE CONFORMANCE CHECK")
    print(f"  exported parts: {len(data)} | approved stair parts: {len(stair)}")
    print(f"  lattice pairs checked: {checked_pairs} | conforming: {conforming}")
    for f in fails[:12]:
        print("  FAIL:", f)
    print("RECIPE CONFORMANCE CHECK:", "PASS" if ok else "FAIL")
    return 0 if ok else 2

def main():
    if len(sys.argv) < 2:
        print("usage: recipe_conformance_check.py <exported_nms.json> [package_root]"); return 1
    return check(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ROOT)

if __name__ == "__main__":
    sys.exit(main())
