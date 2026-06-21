import sys
sys.dont_write_bytecode = True
import importlib.util, os
RG = os.path.join(os.path.dirname(__file__), "..", "run_gate.py")
spec = importlib.util.spec_from_file_location("run_gate_mod", RG)
rg = importlib.util.module_from_spec(spec); spec.loader.exec_module(rg)

class O:
    def __init__(self, oid, loc):
        self._d = {"ObjectID": oid}; self.location = loc
        self.rotation_euler = (0.0, 0.0, 0.0); self.scale = 1.0; self.name = oid
    def get(self, k, d=None): return self._d.get(k, d)

LIB = {"S_RAMP": (1, 1, 1, 0, 0, 0), "S_FLOOR": (1, 1, 1, 0, 0, 0), "M_WALL": (1, 1, 1, 0, 0, 0)}
RUN, RISE = rg.RUN_STEP, rg.RISE_STEP
fails = []

# 1) terminal landing one lattice step out -> AABB floats, must be rescued
p1 = [O("S_RAMP", (0, 0, 0)), O("S_FLOOR", (0, RUN, RISE))]
f1, _ = rg.connectivity_floats(p1, LIB)
kept1, resc1 = rg.stair_semantic_rescue(p1, LIB, f1)
if not f1: fails.append("scenario1: expected an AABB float before rescue")
if not any(x["oid"] == "S_FLOOR" for x in resc1): fails.append("scenario1: lattice landing not rescued")
if any(x["oid"] == "S_FLOOR" for x in kept1): fails.append("scenario1: landing still failing after rescue")

# 2) stair part floating far away -> must NOT be rescued
p2 = [O("S_RAMP", (0, 0, 0)), O("S_FLOOR", (40, 0, 0))]
f2, _ = rg.connectivity_floats(p2, LIB)
kept2, resc2 = rg.stair_semantic_rescue(p2, LIB, f2)
if any(x["oid"] == "S_FLOOR" for x in resc2): fails.append("scenario2: far stair float wrongly rescued")
if not any(x["oid"] == "S_FLOOR" for x in kept2): fails.append("scenario2: far stair float not flagged")

# 3) non-stair floating part -> must NOT be rescued (scope)
p3 = [O("M_WALL", (0, 0, 0)), O("M_WALL", (40, 0, 0))]
f3, _ = rg.connectivity_floats(p3, LIB)
kept3, resc3 = rg.stair_semantic_rescue(p3, LIB, f3)
if resc3: fails.append("scenario3: non-stair part wrongly rescued by stair gate")

if fails:
    print("STAIR SEMANTIC UNIT TEST: FAIL")
    for x in fails: print("  -", x)
    sys.exit(1)
print("STAIR SEMANTIC UNIT TEST: PASS")
