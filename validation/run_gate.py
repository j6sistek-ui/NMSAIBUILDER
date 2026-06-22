#!/usr/bin/env python3
"""
run_gate.py (v5.18.00) — executable validation gate.

Usage:
    python3 validation/run_gate.py <generated_script.py> [library.json] [tag_prefix] [--require-json-evidence] [--require-router] [--require-validated-reuse] [--require-ai-capture-compliance] [--require-conformance <exported.json>]

Mocks bpy + the Base Builder runtime, provides a small mathutils.Vector/Matrix
stand-in, execs the generated script, then prints a tool-backed PASS/FAIL block.

Scope:
- catches raw Blender primitive usage;
- checks add_part/template-copy pattern;
- catches obvious non-uniform final scale assignments;
- dry-runs generated object creation with NMS custom properties;
- checks ObjectIDs against the supplied library;
- does not prove visual correctness, recipe correctness, or project taste.
Those must be checked against screenshots/JSON and the provenance manifest.
- Historical hardening introduced in v1.03.02 also fails zero placed parts and unresolved NMS Builder Part-wrapper misuse.
"""
import sys, types, re, json, math, ast

# ---------------------------------------------------------------------
# Minimal mathutils substitute for non-Blender dry-run environments.
# ---------------------------------------------------------------------
class Vector:
    def __init__(self, seq=(0,0,0)):
        if isinstance(seq, Vector):
            self.x, self.y, self.z = seq.x, seq.y, seq.z
        else:
            vals = list(seq)
            self.x = float(vals[0]) if len(vals) > 0 else 0.0
            self.y = float(vals[1]) if len(vals) > 1 else 0.0
            self.z = float(vals[2]) if len(vals) > 2 else 0.0
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    def __len__(self):
        return 3
    def __getitem__(self, i):
        return (self.x, self.y, self.z)[i]
    def __repr__(self):
        return f"Vector(({self.x}, {self.y}, {self.z}))"
    def __add__(self, other):
        other = Vector(other); return Vector((self.x+other.x, self.y+other.y, self.z+other.z))
    def __sub__(self, other):
        other = Vector(other); return Vector((self.x-other.x, self.y-other.y, self.z-other.z))
    def __mul__(self, val):
        return Vector((self.x*val, self.y*val, self.z*val))
    __rmul__ = __mul__
    def __truediv__(self, val):
        return Vector((self.x/val, self.y/val, self.z/val))
    def __neg__(self):
        return Vector((-self.x, -self.y, -self.z))
    @property
    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    def normalized(self):
        L = self.length
        return Vector((0,0,0)) if L == 0 else self / L
    def normalize(self):
        L = self.length
        if L != 0:
            self.x, self.y, self.z = self.x/L, self.y/L, self.z/L
        return None
    def cross(self, other):
        other = Vector(other)
        return Vector((self.y*other.z - self.z*other.y,
                       self.z*other.x - self.x*other.z,
                       self.x*other.y - self.y*other.x))
    def dot(self, other):
        other = Vector(other)
        return self.x*other.x + self.y*other.y + self.z*other.z

class _Quat:
    def to_euler(self, *args, **kwargs):
        return (0.0, 0.0, 0.0)

class Matrix:
    def __init__(self, rows):
        self.rows = rows
    def to_quaternion(self):
        return _Quat()
    def to_euler(self, *args, **kwargs):
        return (0.0, 0.0, 0.0)

def install_mathutils_mock():
    m = types.ModuleType("mathutils")
    m.Vector = Vector
    m.Matrix = Matrix
    sys.modules["mathutils"] = m

# ---------------------------------------------------------------------
# Mock bpy + Base Builder
# ---------------------------------------------------------------------
def build_fake_env():
    ALL = []

    class FakeObj:
        def __init__(s, name="obj"):
            s.name = name
            s._d = {}
            s.data = None
            s.location = Vector((0,0,0))
            s.rotation_euler = (0,0,0)
            s.scale = (1,1,1)
        def copy(s):
            o = FakeObj(s.name)
            o._d = dict(s._d)
            o.data = s.data
            o.location = s.location
            o.rotation_euler = s.rotation_euler
            o.scale = s.scale
            return o
        def animation_data_clear(s): pass
        def keys(s): return list(s._d.keys())
        def get(s,k,d=None): return s._d.get(k,d)
        def __setitem__(s,k,v): s._d[k]=v
        def __getitem__(s,k): return s._d[k]
        def __contains__(s,k): return k in s._d

    class ObjCollection:
        def __iter__(s): return iter(ALL)
        def __len__(s): return len(ALL)
        def __getitem__(s, i): return ALL[i]
        def __contains__(s, item):
            if isinstance(item, str):
                return any(getattr(o, "name", None) == item for o in ALL)
            return item in ALL
        def remove(s, o, do_unlink=True):
            if isinstance(o, str):
                for obj in list(ALL):
                    if getattr(obj, "name", None) == o:
                        ALL.remove(obj)
                        return
            elif o in ALL:
                ALL.remove(o)
        def link(s, o):
            if o not in ALL:
                ALL.append(o)

    class Data:
        def __init__(s):
            s.objects = ObjCollection()

    class Coll:
        def __init__(s):
            s.objects = ObjCollection()

    class Ctx:
        def __init__(s):
            s.collection = Coll()
            s.scene = types.SimpleNamespace(objects=s.collection.objects)

    bpy = types.ModuleType("bpy")
    bpy.data = Data()
    bpy.context = Ctx()
    sys.modules["bpy"] = bpy

    class Part:
        def __init__(s, oid):
            s.object = FakeObj(oid)
            s.object["ObjectID"] = oid
            s.object["SnapID"] = oid
            s.object["Timestamp"] = "mock"
            s.object["UserData"] = "0"
            s.object["order"] = 0
            s.object["belongs_to_preset"] = False
            s.object["snapped_to"] = ""

    class Builder:
        def add_part(s, oid):
            p = Part(oid)
            if p.object not in ALL:
                ALL.append(p.object)
            return p
        def clear_caches(s): pass

    # Install package chain and module expected by most generated scripts.
    for pkg in ["bl_ext", "bl_ext.user_default"]:
        sys.modules.setdefault(pkg, types.ModuleType(pkg))
    bb = types.ModuleType("bl_ext.user_default.no_mans_sky_base_builder")
    bb.BUILDER = Builder()
    sys.modules["bl_ext.user_default.no_mans_sky_base_builder"] = bb

    return ALL

def _string_list_from_node(node):
    vals = []
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        for elt in node.elts:
            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                vals.append(elt.value)
    return vals

def extract_nonuniform_allowed(src):
    """Read optional NONUNIFORM_ALLOWED = {"OBJECTID"} from generated scripts."""
    allowed = set()
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets = [getattr(t, "id", None) for t in node.targets]
                if "NONUNIFORM_ALLOWED" in targets:
                    allowed.update(x for x in _string_list_from_node(node.value) if re.fullmatch(r"[A-Z0-9_]{2,}", x))
    except Exception:
        pass
    return allowed


def extract_named_string_set(src, names):
    vals = set()
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets = [getattr(t, "id", None) for t in node.targets]
                if any(t in names for t in targets):
                    vals.update(x for x in _string_list_from_node(node.value) if re.fullmatch(r"[A-Z0-9_]{2,}", x))
    except Exception:
        pass
    return vals

def extract_named_dict(src, name):
    """Extract a top-level dict literal assigned to `name` (e.g. DESIGN_INTENT)."""
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if any(getattr(t, "id", None) == name for t in node.targets):
                    return ast.literal_eval(node.value)
    except Exception:
        pass
    return None

def extract_objectids(src):
    """Extract candidate ObjectIDs from common generator structures.

    v59 intentionally recognizes both top-level PART_IDS and appended helper lists
    such as GROUND_CITY_PART_IDS, because modern generators often build their final
    manifest from multiple validated ObjectID lists before template creation.
    """
    ids = set()
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets = [getattr(t, "id", None) for t in node.targets]
                # PART_IDS, *_PART_IDS, and other explicit ObjectID manifests.
                if any(t and (t == "PART_IDS" or t.endswith("PART_IDS") or t.endswith("OBJECT_IDS")) for t in targets):
                    ids.update(x for x in _string_list_from_node(node.value) if re.fullmatch(r"[A-Z0-9_]{2,}", x))
                # Manifest dictionaries usually key by ObjectID.
                if any(t and ("MANIFEST" in t or "DIM" in t or "BOUNDS" in t) for t in targets):
                    if isinstance(node.value, ast.Dict):
                        for k in node.value.keys:
                            if isinstance(k, ast.Constant) and isinstance(k.value, str) and re.fullmatch(r"[A-Z0-9_]{2,}", k.value):
                                ids.add(k.value)
            if isinstance(node, ast.Call):
                fname = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
                if fname in {"place", "place_bottom", "place_top", "place_center", "floor_top", "wall", "light", "iris_ring", "iris_casing", "add_part"}:
                    if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        val = node.args[0].value
                        if re.fullmatch(r"[A-Z0-9_]{2,}", val):
                            ids.add(val)
    except Exception:
        pass

    # Regex fallback for older scripts.
    ids.update(re.findall(r'PART_IDS\s*=\s*\[(.*?)\]', src, re.S)[0].split() if False else [])
    ids.update(re.findall(r'(?:place(?:_bottom|_top|_center)?|floor_top|wall|light|iris_ring|iris_casing|add_part)\([\"\']([A-Z0-9_]{2,})[\"\']', src))

    blacklist = {"PASS", "FAIL", "NONE", "TRUE", "FALSE"}
    return {x for x in ids if x not in blacklist}


def detect_part_wrapper_misuse(src):
    """Detect direct use of BUILDER.add_part() return as if it were a Blender object.

    Real NMS Builder may return a Part wrapper. Generated scripts must resolve
    `part.object` or `getattr(part, "object", part)` before `.copy()` or Blender
    object attribute assignment.
    """
    issues = []
    for m in re.finditer(r"(?m)^\s*(\w+)\s*=\s*(?:BUILDER\.)?add_part\([^\n]*\)", src):
        var = m.group(1)
        window = src[m.end():m.end()+650]
        resolved = (
            f"{var}.object" in window
            or f'getattr({var}, "object"' in window
            or f"getattr({var}, 'object'" in window
        )
        touched = re.search(rf"\b{re.escape(var)}\.(?:name|location|rotation_euler|scale|hide_viewport|hide_render|copy)\b", window)
        if touched and not resolved:
            issues.append(f"{var}=add_part used as Blender object without {var}.object resolution")
    return issues


def extract_request_classification(src):
    """Extract optional REQUEST_CLASSIFICATION dict from generated scripts."""
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets = [getattr(t, "id", None) for t in node.targets]
                if "REQUEST_CLASSIFICATION" in targets or "REQUEST_ROUTING_PROVENANCE" in targets:
                    try:
                        return ast.literal_eval(node.value)
                    except Exception:
                        return {"__parse_error__": True}
    except Exception:
        pass
    return None

def _router_spec():
    """Load valid request types, the universal critical anchor, and per-type critical
    bundles from REQUEST_ROUTER_CHECKLIST.json next to this gate. Falls back to a
    built-in minimum if the router file is not found."""
    import os as _os
    here = _os.path.dirname(_os.path.abspath(__file__))
    rp = _os.path.join(_os.path.dirname(here), "rules", "REQUEST_ROUTER_CHECKLIST.json")
    def norm(s): return _os.path.basename(str(s)).split(".")[0].strip().upper()
    try:
        d = json.load(open(rp, encoding="utf-8"))
        types = set(d.get("request_types", {}).keys())
        anchor = {norm(x) for x in d.get("always_required", []) if str(x).startswith("rules/")}
        crit = {t: {norm(x) for x in b.get("critical", [])} for t, b in d.get("request_types", {}).items()}
        return types, anchor, crit, norm
    except Exception:
        return set(), {"UNIVERSAL_RULES", "SYSTEMATIC_FAILURE_CAPA_PROTOCOL", "REQUEST_ROUTER_CHECKLIST"}, {}, norm

_UNCLEAR = {"", "other", "clarify", "unclear", "unknown", "tbd", "other / clarify"}

def validate_request_classification(src):
    rc = extract_request_classification(src)
    if rc is None:
        return False, ["REQUEST_CLASSIFICATION missing"]
    if not isinstance(rc, dict):
        return False, ["REQUEST_CLASSIFICATION is not a dict"]
    if rc.get("__parse_error__"):
        return False, ["REQUEST_CLASSIFICATION could not be literal-evaluated"]
    errors = []
    types, anchor, crit, norm = _router_spec()
    rtype = str(rc.get("request_type", "")).strip()
    if (not rtype) or rtype.lower() in _UNCLEAR:
        errors.append("request_type unresolved/ambiguous -> seek user clarification before generating")
    elif types and rtype not in types:
        errors.append("request_type '%s' is not a defined router type (add it via the documented process)" % rtype)
    bundles = rc.get("rule_bundles_checked") or rc.get("required_checks") or []
    if not isinstance(bundles, (list, tuple)):
        errors.append("rule_bundles_checked must be a list"); bundles = []
    declared = {norm(b) for b in bundles}
    miss_anchor = sorted(anchor - declared)
    if miss_anchor:
        errors.append("missing critical/universal rule bundles: " + ", ".join(miss_anchor))
    miss_crit = sorted(crit.get(rtype, set()) - declared)
    if miss_crit:
        errors.append("missing critical bundles for %s: %s" % (rtype, ", ".join(miss_crit)))
    amb = rc.get("ambiguity_resolution")
    if amb is None:
        errors.append("ambiguity_resolution missing")
    elif amb not in ("not_needed", "user_clarified", "clarification_required_before_action"):
        errors.append("ambiguity_resolution has an unrecognized value")
    elif amb == "clarification_required_before_action":
        errors.append("ambiguity unresolved -> seek user input before shipping a script")
    if "json_evidence_used" not in rc:
        errors.append("json_evidence_used missing")
    return len(errors) == 0, errors


# ---------------------------------------------------------------------
# Connectivity / no-float gate (v2.07.00)
# Mechanical enforcement of DISCONNECTED_ASSEMBLY_HARDSTOP_RULE. A placed part
# that touches no other placed part within tolerance is a FAIL. Float is the
# disfavored default; the only sanctioned exception is an explicit user request
# for a floating part, approved per-build OUTSIDE this gate (no carryover). The
# gate never self-clears a float and holds no state, so prior approval on another
# script grants nothing here.
# ---------------------------------------------------------------------
CONN_TOL = 0.5
_STRUCT_KEYS = ("floor", "wall", "ramp", "stair", "roof", "foundation", "shell",
                "shaft", "beam", "arch", "catwalk", "tower", "frame", "casing",
                "support", "collar", "socket", "platform", "gantry", "bridge",
                "corridor", "rail", "pillar", "column", "trim", "parapet")
_STRUCT_OID = ("FLOOR", "WALL", "RAMP", "STAIR", "ROOF", "FOUND", "ARCH", "RSJ")

def _conn_xyz(loc):
    try:
        return (float(loc[0]), float(loc[1]), float(loc[2]))
    except Exception:
        try:
            return (float(loc.x), float(loc.y), float(loc.z))
        except Exception:
            return (0.0, 0.0, 0.0)

def _conn_scalar(sc):
    try:
        return float(sc[0])
    except Exception:
        try:
            return float(sc)
        except Exception:
            return 1.0

def _conn_mat(rx, ry, rz):
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    Rx = ((1, 0, 0), (0, cx, -sx), (0, sx, cx))
    Ry = ((cy, 0, sy), (0, 1, 0), (-sy, 0, cy))
    Rz = ((cz, -sz, 0), (sz, cz, 0), (0, 0, 1))
    def mul(A, B):
        return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
    return mul(Rz, mul(Ry, Rx))

def _conn_apply(M, p):
    return (M[0][0]*p[0] + M[0][1]*p[1] + M[0][2]*p[2],
            M[1][0]*p[0] + M[1][1]*p[1] + M[1][2]*p[2],
            M[2][0]*p[0] + M[2][1]*p[1] + M[2][2]*p[2])

def _conn_aabb(loc, rot, s, ext, cen):
    ex, ey, ez = ext
    cx, cy, cz = cen
    rx, ry, rz = (rot[0], rot[1], rot[2]) if len(rot) >= 3 else (rot[0], 0.0, 0.0)
    M = _conn_mat(rx, ry, rz)
    # Axis-aligned (each euler ~ multiple of 90 deg) -> exact rotated box.
    # Tilted -> conservative max-extent cube so tilt-math uncertainty never
    # produces a FALSE float (bias is toward not blocking good builds on tilt).
    aligned = all((math.degrees(a) % 90 < 2 or math.degrees(a) % 90 > 88) for a in (rx, ry, rz))
    if not aligned:
        m = max(ex, ey, ez) / 2.0 * s
        c = _conn_apply(M, (cx*s, cy*s, cz*s))
        return ((loc[0]+c[0]-m, loc[1]+c[1]-m, loc[2]+c[2]-m),
                (loc[0]+c[0]+m, loc[1]+c[1]+m, loc[2]+c[2]+m))
    xs = []; ys = []; zs = []
    for ix in (-1, 1):
        for iy in (-1, 1):
            for iz in (-1, 1):
                p = ((cx + ix*ex/2.0)*s, (cy + iy*ey/2.0)*s, (cz + iz*ez/2.0)*s)
                w = _conn_apply(M, p)
                xs.append(loc[0]+w[0]); ys.append(loc[1]+w[1]); zs.append(loc[2]+w[2])
    return ((min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs)))

def _conn_gap(a, b):
    (amn, amx), (bmn, bmx) = a, b
    d = 0.0
    for i in range(3):
        g = 0.0
        if amn[i] > bmx[i]:
            g = amn[i] - bmx[i]
        elif bmn[i] > amx[i]:
            g = bmn[i] - amx[i]
        d += g * g
    return math.sqrt(d)

def _conn_structural(oid, role):
    blob = ((oid or "") + " " + (role or "")).lower()
    if any(k in blob for k in _STRUCT_KEYS):
        return True
    up = (oid or "").upper()
    return any(k in up for k in _STRUCT_OID)

def connectivity_floats(placed, lib_ext, tol=CONN_TOL):
    items = []
    for o in placed:
        oid = o.get("ObjectID")
        if oid is None or oid not in lib_ext:
            continue
        e = lib_ext[oid]
        loc = _conn_xyz(o.location)
        rot = tuple(o.rotation_euler) if hasattr(o, "rotation_euler") else (0.0, 0.0, 0.0)
        s = _conn_scalar(o.scale)
        box = _conn_aabb(loc, rot, s, (e[0], e[1], e[2]), (e[3], e[4], e[5]))
        role = o.get("Role") or o.get("RecipeLayer") or ""
        items.append((oid, role, box))
    n = len(items)
    if n < 2:
        return [], n
    floats = []
    for i in range(n):
        gi = min((_conn_gap(items[i][2], items[j][2]) for j in range(n) if j != i), default=999.0)
        if gi > tol:
            oid, role, box = items[i]
            cx = (box[0][0] + box[1][0]) / 2.0
            cy = (box[0][1] + box[1][1]) / 2.0
            cz = (box[0][2] + box[1][2]) / 2.0
            floats.append({"oid": oid, "role": role, "z": round(cz, 2), "c": (cx, cy, cz),
                           "gap": round(gi, 2), "structural": _conn_structural(oid, role)})
    return floats, n


# Scoped semantic stair float-gate (wired into the no-float decision below).
# An approved stair part that AABB-floats is cleared ONLY if it sits one locked stair
# lattice step from another approved stair part. Generic AABB stays strict for everything
# else; a stair part with no lattice neighbour stays failed. No part-type other than the
# approved stair families is ever rescued. Tolerance is tunable.
APPROVED_STAIR = {"B_RAMP", "C_RAMP", "F_RAMP", "M_RAMP", "S_RAMP", "T_RAMP", "W_RAMP",
                  "B_FLOOR", "C_FLOOR", "F_FLOOR", "M_FLOOR", "S_FLOOR", "T_FLOOR", "W_FLOOR"}
_RAMP_RUN_STEP = 5.33334
_RAMP_RISE_STEP = 3.33333
_STAIR_CONTACT_TUNE = 0.985
RUN_STEP = _RAMP_RUN_STEP * _STAIR_CONTACT_TUNE
RISE_STEP = _RAMP_RISE_STEP * _STAIR_CONTACT_TUNE
STAIR_LATTICE_L = math.sqrt(RUN_STEP ** 2 + RISE_STEP ** 2)
STAIR_LANDING_TOL = 0.65  # tunable; matches stair_semantic_float_gate

def _conn_clean(oid):
    return str(oid or "").lstrip("^")

def _conn_dist(a, b):
    return math.sqrt(sum((float(x) - float(y)) ** 2 for x, y in zip(a, b)))

def _stair_centers(placed, lib_ext):
    out = []
    for o in placed:
        oid = o.get("ObjectID")
        if oid is None or oid not in lib_ext:
            continue
        if _conn_clean(oid) not in APPROVED_STAIR:
            continue
        e = lib_ext[oid]
        loc = _conn_xyz(o.location)
        rot = tuple(o.rotation_euler) if hasattr(o, "rotation_euler") else (0.0, 0.0, 0.0)
        sc = _conn_scalar(o.scale)
        box = _conn_aabb(loc, rot, sc, (e[0], e[1], e[2]), (e[3], e[4], e[5]))
        out.append(((box[0][0] + box[1][0]) / 2.0, (box[0][1] + box[1][1]) / 2.0, (box[0][2] + box[1][2]) / 2.0))
    return out

def stair_semantic_rescue(placed, lib_ext, floats):
    centers = _stair_centers(placed, lib_ext)
    kept, rescued = [], []
    for f in floats:
        fc = f.get("c")
        if fc is not None and _conn_clean(f.get("oid")) in APPROVED_STAIR and \
           any(abs(_conn_dist(fc, c) - STAIR_LATTICE_L) <= STAIR_LANDING_TOL for c in centers if c != fc):
            rescued.append(f)
        else:
            kept.append(f)
    return kept, rescued



VALIDATED_STATUSES_FOR_AUTO_GATE = {"SCRIPT_VALIDATED", "BLENDER_USER_CHECK", "BLENDER_SYSTEMATIC", "GAME_VALIDATED"}
RECIPE_CONFORMANCE_STAIR_IDS = {"B_RAMP","C_RAMP","F_RAMP","M_RAMP","S_RAMP","T_RAMP","W_RAMP"}

def _gate_root():
    import os as _os
    return _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

def _load_partmap_index_for_gate():
    import os as _os, json as _json
    path = _os.path.join(_gate_root(), "library", "part_placement_maps", "part_placement_map_index.json")
    try:
        d = _json.load(open(path, encoding="utf-8"))
        return d.get("parts", {}) if isinstance(d, dict) else {}
    except Exception:
        return {}

def _norm_validation_status_for_gate(s):
    return str(s or "").split("|")[0].strip()

def _request_type_from_source_for_gate(src):
    rc = extract_request_classification(src)
    return rc.get("request_type") if isinstance(rc, dict) else ""

def _auto_gate_requirements(src):
    """2.17.02 hardening.
    Validated logic/conformance gates are not opt-in for scripts that use validated
    or user-reviewed parts. A build-generation script must expose receipts, and if
    it uses parts with an executable conformance recipe, exported JSON is required
    to claim a machine-checkable PASS.
    """
    idx = _load_partmap_index_for_gate()
    used = extract_objectids(src)
    req_type = _request_type_from_source_for_gate(src)
    validated = []
    recipe_parts = []
    for pid in used:
        meta = idx.get(pid, {})
        status = _norm_validation_status_for_gate(meta.get("validation_status"))
        if status in VALIDATED_STATUSES_FOR_AUTO_GATE:
            validated.append(pid)
        if pid in RECIPE_CONFORMANCE_STAIR_IDS:
            recipe_parts.append(pid)
    likely_build = req_type in {"build_generation", "part_behavior_learning", "rule_discovery_and_proof"}
    return {
        "used_ids": sorted(used),
        "request_type": req_type,
        "validated_parts": sorted(validated),
        "recipe_parts": sorted(recipe_parts),
        "validated_reuse_required": bool(validated or likely_build),
        "recipe_conformance_required": bool(recipe_parts),
        "intent_graph_required": bool(likely_build or "BUILD_INTENT_GRAPH" in src),
        "ai_capture_compliance_required": bool(likely_build),
        "design_intent_required": bool(likely_build),
    }


def main():
    if len(sys.argv) < 2:
        print("usage: run_gate.py <script.py> [library.json] [tag_prefix]")
        return 1

    script = sys.argv[1]
    libpath = sys.argv[2] if len(sys.argv) > 2 else None
    args = sys.argv[1:]
    require_json_evidence = "--require-json-evidence" in args
    require_router = "--require-router" in args
    require_validated_reuse = "--require-validated-reuse" in args
    require_ai_capture_compliance = "--require-ai-capture-compliance" in args
    conformance_json = None
    intent_graph_json = None
    if "--require-conformance" in args:
        _ci = args.index("--require-conformance")
        conformance_json = args[_ci + 1] if _ci + 1 < len(args) else None
        del args[_ci:_ci + 2]
    if "--require-intent-graph" in args:
        _ii = args.index("--require-intent-graph")
        intent_graph_json = args[_ii + 1] if _ii + 1 < len(args) else conformance_json
        del args[_ii:_ii + 2]
    build_sheet_arg = None
    if "--build-sheet" in args:
        _bi = args.index("--build-sheet")
        build_sheet_arg = args[_bi + 1] if _bi + 1 < len(args) else None
        del args[_bi:_bi + 2]
    capa_state_arg = None
    if "--capa-state" in args:
        _cs = args.index("--capa-state")
        capa_state_arg = args[_cs + 1] if _cs + 1 < len(args) else None
        del args[_cs:_cs + 2]
    args = [a for a in args if a not in {"--require-json-evidence", "--require-router", "--require-validated-reuse", "--require-ai-capture-compliance"}]
    script = args[0]
    libpath = args[1] if len(args) > 1 else None
    tag = args[2] if len(args) > 2 else None
    src = open(script, encoding="utf-8", errors="ignore").read()
    auto_gate = _auto_gate_requirements(src)
    auto_validated_reuse_required = bool(auto_gate.get("validated_reuse_required"))
    auto_conformance_required = bool(auto_gate.get("recipe_conformance_required"))
    auto_intent_graph_required = bool(auto_gate.get("intent_graph_required"))
    auto_ai_capture_required = bool(auto_gate.get("ai_capture_compliance_required"))
    auto_design_intent_required = bool(auto_gate.get("design_intent_required"))
    if auto_validated_reuse_required:
        require_validated_reuse = True
    if auto_ai_capture_required:
        require_ai_capture_compliance = True
    if intent_graph_json is None and conformance_json:
        intent_graph_json = conformance_json

    feature_recipe_ok = True
    feature_recipe_output = ""
    try:
        import subprocess, os as _osfr
        fr_check = _osfr.path.join(_osfr.path.dirname(_osfr.path.abspath(__file__)), "feature_recipe_lookup_check.py")
        if _osfr.path.exists(fr_check):
            fr = subprocess.run([sys.executable, "-S", fr_check, script],
                                text=True, capture_output=True, timeout=30)
            feature_recipe_output = (fr.stdout or fr.stderr or "").strip()
            feature_recipe_ok = (fr.returncode == 0 and "FEATURE RECIPE LOOKUP CHECK: PASS" in feature_recipe_output)
        else:
            feature_recipe_ok = False
            feature_recipe_output = "feature_recipe_lookup_check.py missing"
    except Exception as exc:
        feature_recipe_ok = False
        feature_recipe_output = f"feature recipe lookup check errored: {exc}"

    ai_capture_ok = True
    ai_capture_output = ""
    if require_ai_capture_compliance:
        try:
            import subprocess, os as _osai
            ai_check = _osai.path.join(_osai.path.dirname(_osai.path.abspath(__file__)), "ai_capture_compliance_check.py")
            ai = subprocess.run([sys.executable, "-S", ai_check, script],
                                text=True, capture_output=True, timeout=30)
            ai_capture_output = (ai.stdout or ai.stderr or "").strip()
            ai_capture_ok = (ai.returncode == 0 and "AI CAPTURE COMPLIANCE CHECK: PASS" in ai_capture_output)
        except Exception as exc:
            ai_capture_ok = False
            ai_capture_output = f"AI capture compliance check errored: {exc}"

    validated_reuse_ok = True
    validated_reuse_output = ""
    if require_validated_reuse:
        try:
            import subprocess, os as _os
            checker = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "validated_logic_reuse_check.py")
            vr = subprocess.run([sys.executable, "-S", checker, script],
                                text=True, capture_output=True, timeout=30)
            validated_reuse_output = (vr.stdout or vr.stderr or "").strip()
            validated_reuse_ok = (vr.returncode == 0 and "VALIDATED LOGIC REUSE CHECK: PASS" in validated_reuse_output)
        except Exception as exc:
            validated_reuse_ok = False
            validated_reuse_output = f"validated reuse check errored: {exc}"

    conformance_ok = True
    conformance_output = ""
    conformance_deferred = False
    if auto_conformance_required and not conformance_json:
        conformance_deferred = True
        conformance_output = (
            "RECIPE CONFORMANCE CHECK: DEFERRED\n"
            "  PENDING: exported NMS JSON is a POST-BUILD artifact. Recipe conformance for "
            f"{auto_gate.get('recipe_parts', [])} is validated after the build runs and exports. "
            "Re-run with --require-conformance <exported.json> to lift SCRIPT_VALIDATED to JSON-validated."
        )
    elif conformance_json:
        try:
            import subprocess, os as _os2
            cc = _os2.path.join(_os2.path.dirname(_os2.path.abspath(__file__)), "recipe_conformance_check.py")
            cr = subprocess.run([sys.executable, "-S", cc, conformance_json],
                                text=True, capture_output=True, timeout=30)
            conformance_output = (cr.stdout or cr.stderr or "").strip()
            conformance_ok = (cr.returncode == 0 and "RECIPE CONFORMANCE CHECK: PASS" in conformance_output)
        except Exception as exc:
            conformance_ok = False
            conformance_output = f"recipe conformance check errored: {exc}"

    intent_graph_ok = True
    intent_graph_output = ""
    intent_graph_deferred = False
    if auto_intent_graph_required and not intent_graph_json:
        intent_graph_deferred = True
        intent_graph_output = (
            "INTENT GRAPH CONFORMANCE CHECK: DEFERRED\n"
            "  PENDING: exported NMS JSON is a POST-BUILD artifact. BUILD_INTENT_GRAPH connected-component "
            "verification runs after the build is exported. Re-run with --require-intent-graph <exported.json>."
        )
    elif intent_graph_json:
        try:
            import subprocess, os as _os3
            ig = _os3.path.join(_os3.path.dirname(_os3.path.abspath(__file__)), "intent_graph_conformance_check.py")
            ir = subprocess.run([sys.executable, "-S", ig, script, intent_graph_json, libpath or ""],
                                text=True, capture_output=True, timeout=30)
            intent_graph_output = (ir.stdout or ir.stderr or "").strip()
            intent_graph_ok = (ir.returncode == 0 and "INTENT GRAPH CONFORMANCE CHECK: PASS" in intent_graph_output)
        except Exception as exc:
            intent_graph_ok = False
            intent_graph_output = f"intent graph conformance check errored: {exc}"

    # build-sheet gate (5.02.00) — PRE-BUILD. The generated builder sheet must COVER every used
    # ObjectID, each entry must carry a non-empty build_application, and the sheet's mechanical
    # fields must still MATCH the resolver (tamper-evident). Required for build_generation; enforced
    # whenever a sheet is declared. Lean replacement for the hand-written manifest at the gate.
    import re as _rebs, os as _osbs
    _bs = build_sheet_arg
    if _bs is None:
        _m = _rebs.search(r'PROJECT_BUILD_SHEET\s*=\s*["\']([^"\']+)["\']', src)
        _bs = _m.group(1) if _m else None
    _bsu = _rebs.search(r'BUILD_SHEET_USED\s*=\s*(True|1)\b', src) is not None
    build_sheet_required = (auto_gate.get("request_type") == "build_generation") or (_bs is not None)
    build_sheet_ok = True
    build_sheet_output = ""
    if build_sheet_required:
        _path = None
        if _bs:
            for _cand in (_bs, _osbs.path.join(_osbs.path.dirname(_osbs.path.abspath(script)), _bs)):
                if _osbs.path.exists(_cand): _path = _cand; break
        if not _bs or not _bsu:
            build_sheet_ok = False
            build_sheet_output = ("BUILD SHEET CHECK: FAIL\n  FAIL: build_generation requires a generated builder sheet. "
                                  "Declare PROJECT_BUILD_SHEET=\"<path>\" and BUILD_SHEET_USED=True, and generate it with "
                                  "validation/part_context_resolver.py.")
        elif _path is None:
            build_sheet_ok = False
            build_sheet_output = f"BUILD SHEET CHECK: FAIL\n  FAIL: declared build sheet not found: {_bs}"
        else:
            try:
                import subprocess
                _bsc = _osbs.path.join(_osbs.path.dirname(_osbs.path.abspath(__file__)), "build_sheet_check.py")
                _root = _osbs.path.dirname(_osbs.path.dirname(libpath)) if libpath else _osbs.path.dirname(_osbs.path.dirname(_osbs.path.abspath(__file__)))
                _r = subprocess.run([sys.executable, "-S", _bsc, script, _path, _root], text=True, capture_output=True, timeout=40)
                build_sheet_output = (_r.stdout or _r.stderr or "").strip()
                build_sheet_ok = (_r.returncode == 0 and "BUILD SHEET CHECK: PASS" in build_sheet_output)
            except Exception as _e:
                build_sheet_ok = False
                build_sheet_output = f"build sheet check errored: {_e}"

    # CAPA escalation (5.03.00): if a 'skipped known info / build-sheet not utilized' CAPA is OPEN,
    # the deeper BUILD COMPLIANCE MANIFEST becomes a REQUIRED gate (consequence) on top of the lean sheet.
    capa_state_path = capa_state_arg or (_osbs.path.join(_osbs.path.dirname(_osbs.path.dirname(libpath)), "data", "CAPA_ESCALATION_STATE.json") if libpath else _osbs.path.join(_osbs.path.dirname(_osbs.path.dirname(_osbs.path.abspath(__file__))), "data", "CAPA_ESCALATION_STATE.json"))
    capa_active = False
    try:
        capa_active = bool(json.load(open(capa_state_path)).get("active"))
    except Exception:
        capa_active = False
    deeper_manifest_ok = True
    deeper_manifest_output = ""
    if capa_active:
        _mm = _rebs.search(r'PROJECT_COMPLIANCE_MANIFEST\s*=\s*["\']([^"\']+)["\']', src)
        _mpath = _mm.group(1) if _mm else None
        _mfound = None
        if _mpath:
            for _c in (_mpath, _osbs.path.join(_osbs.path.dirname(_osbs.path.abspath(script)), _mpath)):
                if _osbs.path.exists(_c): _mfound = _c; break
        if not _mpath or _mfound is None:
            deeper_manifest_ok = False
            deeper_manifest_output = ("BUILD COMPLIANCE MANIFEST: REQUIRED (CAPA escalation active)\n  FAIL: a CAPA for skipping known "
                                      "source/build-sheet information is OPEN; this build must also pass the deeper manifest. "
                                      "Declare PROJECT_COMPLIANCE_MANIFEST=\"<path>\" and emit it; clear via validation/capa_escalation.py --clear after the corrective build.")
        else:
            try:
                import subprocess
                _cm = _osbs.path.join(_osbs.path.dirname(_osbs.path.abspath(__file__)), "compliance_manifest_check.py")
                _root2 = _osbs.path.dirname(_osbs.path.dirname(libpath)) if libpath else _osbs.path.dirname(_osbs.path.dirname(_osbs.path.abspath(__file__)))
                _cr = subprocess.run([sys.executable, "-S", _cm, _mfound, _root2], text=True, capture_output=True, timeout=40)
                deeper_manifest_output = (_cr.stdout or _cr.stderr or "").strip()
                deeper_manifest_ok = (_cr.returncode == 0 and "COMPLIANCE MANIFEST CHECK: PASS" in deeper_manifest_output)
            except Exception as _e:
                deeper_manifest_ok = False
                deeper_manifest_output = f"deeper manifest check errored: {_e}"

    raw_prim = len(re.findall(r"bpy\.ops\.mesh\.primitive_\w+|bpy\.data\.meshes\.new|bpy\.data\.objects\.new", src))
    has_addpart = "add_part(" in src
    has_copy = ".copy()" in src
    wrapper_misuse = detect_part_wrapper_misuse(src)
    has_wrapper_resolution = (".object" in src or "getattr(part" in src or "getattr(raw" in src or "getattr(created" in src or "getattr(p" in src)
    allow_zero_placed = "VALIDATION_ALLOW_ZERO_PLACED = True" in src
    # v59 accepts scoped cleanup by TAG, PREFIX, SCRIPT_TAG, TMP_PREFIX, tuple/list of old prefixes,
    # or helper functions that call .startswith(prefixes). It rejects only broad all-scene deletion patterns.
    has_tagdel = ("startswith(TAG)" in src or "startswith(PREFIX)" in src or "startswith(SCRIPT_TAG)" in src
                  or "startswith(DELETE_PREFIXES)" in src or "startswith(OLD_GENERATED_PREFIXES)" in src
                  or "delete_objects_with_prefixes" in src or "startswith(prefixes)" in src
                  or "startswith(tag)" in src.lower())

    # Baked-hidden-collection lint: a DELIVERED build script must leave every
    # collection/object visible and included in the view layer at hand-off.
    # hide_viewport / view-layer exclude resist Alt+H, so a user cannot recover
    # the parts in Blender. Review-time isolation is the review addon's job via
    # recoverable hide_set(). Flag only the un-recoverable bakes here.
    _hide_patterns = {
        "hide_viewport = True":       r"\.hide_viewport\s*=\s*True",
        "layer_collection.exclude = True": r"\.exclude\s*=\s*True",
        "collection hide via hide_viewport(": r"hide_viewport\s*\(\s*True",
    }
    hidden_bake_hits = sorted({label for label, pat in _hide_patterns.items() if re.search(pat, src)})
    hidden_bake = len(hidden_bake_hits)

    nonuniform_allowed = extract_nonuniform_allowed(src)
    nonuni = 0
    nonuni_static_suspect = 0
    for m in re.findall(r"\.scale\s*=\s*\(([^)]*)\)", src):
        parts = [p.strip() for p in m.split(",")]
        if len(parts) == 3 and len(set(parts)) > 1:
            nonuni_static_suspect += 1
            # Static regex cannot always know which ObjectID is being scaled.
            # If the script explicitly declares NONUNIFORM_ALLOWED, defer final
            # judgment to the runtime audit, which can inspect object ObjectID.
            if not nonuniform_allowed:
                nonuni += 1

    used_ids = extract_objectids(src)
    # Do not treat explicitly prohibited-list-only IDs as used parts. A script may carry
    # HOLO_DISCO/HOLO_DISCO_0 in PROHIBITED_OBJECT_IDS without generating them.
    prohibited_declared = extract_named_string_set(src, {"PROHIBITED_OBJECT_IDS", "PROHIBITED_IDS", "PROHIBITED"})
    used_ids = used_ids - prohibited_declared
    if tag is None:
        mt = (re.search(r'PREFIX\s*=\s*"([^"]+)"', src)
              or re.search(r'SCRIPT_TAG\s*=\s*"([^"]+)"', src)
              or re.search(r'TAG\s*=\s*"([^"]+)"', src))
        tag = mt.group(1) if mt else "BUILD_"

    install_mathutils_mock()
    ALL = build_fake_env()
    g = {"__name__": "__main__"}
    err = None
    try:
        exec(compile(src, script, "exec"), g)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"

    placed = [o for o in ALL if str(o.name).startswith(tag) and "TPL_" not in str(o.name)]
    # 5.18.00 — template-leak detector. The line above excludes TPL_ from the placed
    # count; that exclusion previously MASKED stray templates that survive the
    # tag-scoped cleanup and still get exported by the add-on (they pile at the origin,
    # the cluttered stack seen in failed builds). Detect them so the gate FAILS the
    # leak instead of hiding it. Remediation: delete/exclude templates before export.
    def _at_origin(o):
        loc = getattr(o, "location", None)
        if loc is None: return False
        try: x, y, z = loc[0], loc[1], loc[2]
        except Exception:
            try: x, y, z = loc.x, loc.y, loc.z
            except Exception: return False
        return abs(x) < 1e-4 and abs(y) < 1e-4 and abs(z) < 1e-4
    surviving_templates = [o.name for o in ALL if "TPL_" in str(o.name) and o.get("ObjectID") is not None]
    origin_ids = sorted({o.get("ObjectID") for o in ALL if o.get("ObjectID") is not None and _at_origin(o)})
    template_leak = len(surviving_templates) > 0 or len(origin_ids) >= 2
    missing = [o.name for o in placed if o.get("ObjectID") is None]
    prohibited = [o.name for o in placed if o.get("ObjectID") in {"HOLO_DISCO", "HOLO_DISCO_0"}]
    nonuniform_runtime = []
    for o in placed:
        try:
            sx, sy, sz = o.scale
            if abs(sx-sy) > 1e-6 or abs(sx-sz) > 1e-6:
                if o.get("ObjectID") not in nonuniform_allowed:
                    nonuniform_runtime.append(o.name)
        except Exception:
            pass

    zvals = []
    for o in placed:
        loc = o.location
        if isinstance(loc, Vector):
            zvals.append(loc.z)
        elif isinstance(loc, (tuple, list)) and len(loc) > 2:
            zvals.append(loc[2])
    zvals = sorted(zvals) if zvals else [0,0]

    libdiff = "(library not provided)"
    lib_ext = {}
    _ext_source = None
    def _f(x):
        try:
            return float(x)
        except Exception:
            return None
    def _load_extents(data, dest):
        for d in data:
            if not isinstance(d, dict):
                continue
            oid = d.get("ObjectID")
            if oid is None or "extent_x" not in d:
                continue
            vals = [_f(d.get(k)) for k in ("extent_x", "extent_y", "extent_z", "center_x", "center_y", "center_z")]
            if any(v is None for v in vals[:3]):
                continue  # cannot bound a part without numeric extents; skip it
            dest[oid] = tuple((v if v is not None else 0.0) for v in vals)
    # Per-part DEFAULT rotation (degrees) for the orientation-deviation gate.
    lib_rot = {}
    def _load_rot(data, dest):
        for d in data:
            if not isinstance(d, dict):
                continue
            oid = d.get("ObjectID")
            if oid is None:
                continue
            raw = d.get("DefaultRotationDegrees", d.get("VerifiedDefaultRotationDegrees"))
            if raw is None:
                continue
            try:
                vals = json.loads(raw) if isinstance(raw, str) else raw
                if isinstance(vals, (list, tuple)) and len(vals) >= 3:
                    dest[oid] = (float(vals[0]), float(vals[1]), float(vals[2]))
            except Exception:
                continue
    if libpath:
        try:
            data = json.load(open(libpath, encoding="utf-8"))
            lib = {d.get("ObjectID") for d in data if isinstance(d, dict)}
            notin = sorted(u for u in used_ids if u not in lib)
            libdiff = "NONE" if not notin else ", ".join(notin)
            _load_extents(data, lib_ext)
            _load_rot(data, lib_rot)
            if lib_ext:
                _ext_source = "library-arg"
        except Exception as e:
            libdiff = f"LIBRARY_READ_ERROR: {e}"

    # Connectivity needs geometry extents (extent_x/y/z). Some libraries carry
    # placement/snap data but NO extents (e.g. the verified part map). When the
    # supplied library has no extents, fall back to the canonical dimensions
    # library so connectivity runs regardless of which library was passed.
    if not lib_ext:
        try:
            import os as _os_fb
            _pkg_root = (_os_fb.path.dirname(_os_fb.path.dirname(libpath)) if libpath
                         else _os_fb.path.dirname(_os_fb.path.dirname(_os_fb.path.abspath(__file__))))
            _dimlib = _os_fb.path.join(_pkg_root, "library", "nms_part_dimensions_and_rules_updated.json")
            if _os_fb.path.exists(_dimlib):
                _load_extents(json.load(open(_dimlib, encoding="utf-8")), lib_ext)
                if lib_ext:
                    _ext_source = "dimensions-fallback"
        except Exception:
            pass

    # Rotation defaults: ensure they load even when the passed library lacks them
    # (verified part map carries DefaultRotationDegrees; if a sparse library was
    # passed, fall back to the dimensions library's VerifiedDefaultRotationDegrees).
    if not lib_rot:
        try:
            import os as _os_r
            _root_r = (_os_r.path.dirname(_os_r.path.dirname(libpath)) if libpath
                       else _os_r.path.dirname(_os_r.path.dirname(_os_r.path.abspath(__file__))))
            for _cand in ("library/nms_master_part_map_verified_data_v3_01_02.json",
                          "library/nms_part_dimensions_and_rules_updated.json"):
                _p = _os_r.path.join(_root_r, _cand)
                if _os_r.path.exists(_p):
                    _load_rot(json.load(open(_p, encoding="utf-8")), lib_rot)
                    if lib_rot:
                        break
        except Exception:
            pass

    conn_active = bool(lib_ext) and len(placed) >= 2
    conn_floats, conn_n = ([], 0)
    stair_rescued = []
    if conn_active:
        conn_floats, conn_n = connectivity_floats(placed, lib_ext)
        conn_floats, stair_rescued = stair_semantic_rescue(placed, lib_ext, conn_floats)
    no_floats = (len(conn_floats) == 0)

    # --- orientation-deviation check ---
    # Catches the gothic_castle_v02 failure: parts rotated off their DEFAULT
    # orientation (e.g. roofs at rx=0/70/62 instead of the packet default rx~90)
    # with nothing authorizing it. RZ (facing) is allowed to vary freely; only
    # RX/RY deviations from the part's own default are flagged. Authorized via an
    # orientation override doc entry or an explicit ORIENTATION_OVERRIDE_IDS set.
    import math as _math_o
    _orient_allow = set(extract_named_string_set(src, {"ORIENTATION_OVERRIDE_IDS", "ORIENTATION_JUSTIFIED_IDS"}))
    try:
        import os as _os_o
        _root_o = (_os_o.path.dirname(_os_o.path.dirname(libpath)) if libpath
                   else _os_o.path.dirname(_os_o.path.dirname(_os_o.path.abspath(__file__))))
        _ovp = _os_o.path.join(_root_o, "rules", "PART_ORIENTATION_OVERRIDES.md")
        if _os_o.path.exists(_ovp):
            _ovtxt = open(_ovp, encoding="utf-8", errors="ignore").read()
            for _oid in lib_rot:
                if _oid in _ovtxt:
                    _orient_allow.add(_oid)
    except Exception:
        pass

    def _ang_eq(a, b, tol=5.0):
        return abs((a - b + 180.0) % 360.0 - 180.0) <= tol

    orient_devs = []
    _is_build_type = auto_gate.get("request_type") in {"build_generation", "part_behavior_learning", "rule_discovery_and_proof"}
    orient_active = _is_build_type and bool(lib_rot) and len(placed) >= 1
    if orient_active:
        for o in placed:
            oid = o.get("ObjectID")
            if oid is None or oid not in lib_rot or oid in _orient_allow:
                continue
            re_ = getattr(o, "rotation_euler", None)
            if re_ is None:
                continue
            try:
                rx = _math_o.degrees(re_[0]) % 360.0
                ry = _math_o.degrees(re_[1]) % 360.0
            except Exception:
                continue
            drx, dry, _drz = lib_rot[oid]
            if not _ang_eq(rx, drx % 360.0) or not _ang_eq(ry, dry % 360.0):
                orient_devs.append({"oid": oid, "rx": round(rx, 1), "ry": round(ry, 1),
                                    "def_rx": round(drx % 360.0, 1), "def_ry": round(dry % 360.0, 1)})
    orientation_ok = (len(orient_devs) == 0)

    # --- design-intent check ---
    # Forces a committed design BEFORE placement so builds aren't a mechanically-valid
    # but meaningless pile. Required for build-type requests. Checks that a DESIGN_INTENT
    # plan exists, every assembly declares what it should READ as + an evidence source,
    # and EVERY used ObjectID is assigned a non-empty purpose (no part placed "just because").
    di = extract_named_dict(src, "DESIGN_INTENT")
    di_issues = []
    di_active = auto_design_intent_required
    if di_active:
        if not isinstance(di, dict):
            di_issues.append("DESIGN_INTENT block missing (declare it before placement)")
        else:
            assemblies = di.get("assemblies")
            if not isinstance(assemblies, list) or not assemblies:
                di_issues.append("DESIGN_INTENT.assemblies missing or empty")
            else:
                purposed = set()
                for i, a in enumerate(assemblies):
                    if not isinstance(a, dict):
                        di_issues.append(f"assembly #{i} is not a structured entry")
                        continue
                    nm = a.get("name") or f"#{i}"
                    for field in ("is_a", "target_read", "style_source"):
                        if not str(a.get(field, "")).strip():
                            di_issues.append(f"assembly '{nm}' missing '{field}'")
                    parts = a.get("parts")
                    if not isinstance(parts, list) or not parts:
                        di_issues.append(f"assembly '{nm}' has no parts")
                        continue
                    for pt in parts:
                        if isinstance(pt, dict) and str(pt.get("purpose", "")).strip():
                            oid = pt.get("ObjectID") or pt.get("object_id") or pt.get("id")
                            if oid:
                                purposed.add(oid)
                unpurposed = sorted(u for u in used_ids if u not in purposed)
                if unpurposed:
                    di_issues.append("parts placed with no declared purpose: " + ", ".join(unpurposed[:12]))
    design_intent_ok = (len(di_issues) == 0)

    required_json_constants = {
        "COORD_MODE": "XnZY",
        "AXIS_MODE": "RIGHT_AT_UP",
        "BASE_ROTATION_MODE": "POST_RX90",
        "POST_BASELINE_CORRECTION": "LOCAL_Y_180",
        "SCALE_MODE": "UP_LENGTH_UNIFORM",
    }
    missing_json_bits = []
    json_recreation_constants_ok = True
    for k, v in required_json_constants.items():
        if not re.search(rf'{k}\s*=\s*["\']{re.escape(v)}["\']', src):
            json_recreation_constants_ok = False
            missing_json_bits.append(k)

    has_json_provenance = "JSON_EVIDENCE_PROVENANCE" in src
    has_json_gate_reference = (
        "JSON_EVIDENCE_MAPPING_GATE" in src
        or "WORKING_JSON_FIRST_PRINCIPLE" in src
        or "JSON_TO_PYTHON_RECREATION_PROTOCOL" in src
        or "JSON_GEOMETRY_VALIDATION_LOOP" in src
        or "--require-json-evidence" in src
    )
    has_generated_audit_markers = (
        "EXPORTED_JSON_AUDIT_REQUIRED" in src
        and "PYTHON_TO_JSON_POSITION_MAP" in src
        and "JSON_AUDIT_FIELDS" in src
    )
    json_evidence_ok = (
        has_json_provenance
        and has_json_gate_reference
        and (json_recreation_constants_ok or has_generated_audit_markers)
    )
    router_ok, router_errors = validate_request_classification(src)

    json_evidence_missing = []
    if not has_json_provenance:
        json_evidence_missing.append("JSON_EVIDENCE_PROVENANCE")
    if not has_json_gate_reference:
        json_evidence_missing.append("JSON gate/rule reference")
    if not (json_recreation_constants_ok or has_generated_audit_markers):
        json_evidence_missing.append("JSON recreation constants OR generated-build audit markers")

    P = lambda b: "PASS" if b else "FAIL"
    print("SCRIPT VALIDATION — EXECUTABLE GATE (v5.18.00)")
    print(f"  script: {script}")
    print("--- static linter ---")
    print(f"  no raw mesh primitives: {P(raw_prim==0)} ({raw_prim} found)")
    print(f"  uses add_part templates: {P(has_addpart)}")
    print(f"  object creation path: {P(has_addpart and (has_copy or has_wrapper_resolution))} (copy={has_copy}, wrapper_resolution={has_wrapper_resolution})")
    print(f"  NMS Builder Part-wrapper misuse: {P(len(wrapper_misuse)==0)} ({len(wrapper_misuse)} issue(s))")
    print(f"  tag-scoped cleanup: {P(has_tagdel)}")
    print(f"  no unapproved non-uniform final scale in source: {P(nonuni==0)} ({nonuni} unapproved, {nonuni_static_suspect} static suspect)")
    print(f"  no baked-hidden collections/parts (un-hideable at hand-off): {P(hidden_bake==0)} ({hidden_bake} found)")
    if hidden_bake:
        print("    delivered build scripts must leave all collections visible + included in the view layer;")
        print("    these flags resist Alt+H. Use the review addon's recoverable hide_set() for review staging,")
        print("    or leave parts visible. offending pattern(s): " + ", ".join(hidden_bake_hits))
    print(f"  ObjectIDs extracted: {len(used_ids)}")
    if require_json_evidence:
        msg = "" if json_evidence_ok else f" (missing: {', '.join(json_evidence_missing)})"
        print(f"  JSON evidence mapping gate: {P(json_evidence_ok)}" + msg)
    if require_router:
        rmsg = "" if router_ok else f" (missing/invalid: {', '.join(router_errors)})"
        print(f"  request router classification gate: {P(router_ok)}" + rmsg)
    print(f"  feature recipe lookup gate: {P(feature_recipe_ok)}")
    if feature_recipe_output:
        for _line in feature_recipe_output.splitlines()[:10]:
            print("    " + _line)
    if auto_ai_capture_required and "--require-ai-capture-compliance" not in sys.argv:
        print(f"  AI capture compliance gate: AUTO-REQUIRED for {auto_gate.get('request_type')}")
    if require_ai_capture_compliance:
        print(f"  AI capture compliance gate: {P(ai_capture_ok)}")
        if ai_capture_output:
            for _line in ai_capture_output.splitlines()[:12]:
                print("    " + _line)
    if auto_validated_reuse_required and "--require-validated-reuse" not in sys.argv:
        print(f"  validated logic reuse gate: AUTO-REQUIRED for {auto_gate.get('validated_parts', []) or auto_gate.get('request_type')}")
    if require_validated_reuse:
        print(f"  validated logic reuse gate: {P(validated_reuse_ok)}")
        if validated_reuse_output:
            for _line in validated_reuse_output.splitlines()[:10]:
                print("    " + _line)
    if auto_conformance_required and not conformance_json:
        print(f"  recipe conformance gate: DEFERRED (post-build; supply exported JSON) for {auto_gate.get('recipe_parts', [])}")
        if conformance_output:
            for _line in conformance_output.splitlines()[:10]:
                print("    " + _line)
    elif conformance_json:
        print(f"  recipe conformance gate: {P(conformance_ok)}")
        if conformance_output:
            for _line in conformance_output.splitlines()[:10]:
                print("    " + _line)
    if auto_intent_graph_required and not intent_graph_json:
        print("  intent graph conformance gate: DEFERRED (post-build; supply exported JSON)")
        if intent_graph_output:
            for _line in intent_graph_output.splitlines()[:10]:
                print("    " + _line)
    elif intent_graph_json:
        print(f"  intent graph conformance gate: {P(intent_graph_ok)}")
        if intent_graph_output:
            for _line in intent_graph_output.splitlines()[:10]:
                print("    " + _line)
    if build_sheet_required:
        print(f"  build sheet (packet) gate: {P(build_sheet_ok)}")
        if build_sheet_output:
            for _line in build_sheet_output.splitlines()[:10]:
                print("    " + _line)
    if capa_active:
        print(f"  CAPA escalation: ACTIVE — deeper compliance manifest required")
        print(f"  deeper compliance manifest gate: {P(deeper_manifest_ok)}")
        if deeper_manifest_output:
            for _line in deeper_manifest_output.splitlines()[:10]:
                print("    " + _line)
    print("--- dry-run audit ---")
    print(f"  exec error: {err or 'NONE'}")
    print(f"  placed parts: {len(placed)}   missing ObjectID: {len(missing)}")
    if wrapper_misuse:
        for issue in wrapper_misuse[:5]:
            print(f"  wrapper issue: {issue}")
    print(f"  prohibited ObjectIDs placed: {len(prohibited)}")
    print(f"  template leak (stray TPL_ exported / origin pile): {P(not template_leak)}"
          + (f"  [{len(surviving_templates)} surviving template(s); {len(origin_ids)} distinct ObjectIDs at origin]" if template_leak else ""))
    if template_leak:
        print("    remediation: delete templates before export — `for t in TEMPLATES.values(): bpy.data.objects.remove(t, do_unlink=True)`")
        print("    and add the TPL_ prefix to the tag-scoped cleanup so stale templates also purge on re-run.")
    print(f"  runtime non-uniform scale: {len(nonuniform_runtime)}")
    print(f"  origin z span: {round(zvals[0],2)} .. {round(zvals[-1],2)}")
    print("--- library set-difference ---")
    print(f"  ObjectIDs not in library: {libdiff}")
    print("--- connectivity / no-float gate ---")
    if not conn_active:
        reason = ("<2 placed parts" if len(placed) < 2
                  else "no extents available (checked library arg + dimensions fallback)")
        print(f"  connectivity check: SKIPPED ({reason})")
    else:
        if _ext_source == "dimensions-fallback":
            print("  note: supplied library had no extents; extents loaded from library/nms_part_dimensions_and_rules_updated.json")
        print(f"  no floating parts: {P(no_floats)} ({len(conn_floats)} of {conn_n} placed parts touch nothing within {CONN_TOL}u)")
        if stair_rescued:
            print(f"  stair semantic rescue: {len(stair_rescued)} approved stair part(s) cleared as lattice-step landings (AABB false float)")
        for f in conn_floats[:12]:
            kind = ("STRUCTURAL — should essentially never float; reconnect it"
                    if f["structural"] else
                    "decorative — reconnect, or if the user explicitly requested this float, get publish approval")
            print(f"    {f['oid']:14s} {str(f['role'])[:26]:26s} z={f['z']:7.1f} gap={f['gap']:5.1f}  [{kind}]")
        if conn_floats:
            print("  remediation: reconnect each floating part to its structure (seat / socket / overlap).")
            print("    Float is the disfavored default and is almost never the right choice. The only")
            print("    sanctioned exception is an explicit user request for a floating part, which requires")
            print("    fresh user approval to publish EVERY run this gate fails — prior approval on another")
            print("    script or a previous run does not carry over.")
    print("--- orientation / default-rotation gate ---")
    if not orient_active:
        if not _is_build_type:
            print("  orientation check: N/A (JSON-recreation/non-build request — source transforms are authoritative)")
        else:
            print(f"  orientation check: SKIPPED ({'<1 placed part' if len(placed) < 1 else 'no default rotations in library'})")
    else:
        print(f"  parts on default orientation (RZ/facing free): {P(orientation_ok)} ({len(orient_devs)} deviate without authorization)")
        for d in orient_devs[:12]:
            print(f"    {d['oid']:14s} rx={d['rx']:6.1f} ry={d['ry']:6.1f}  (default rx={d['def_rx']:.1f} ry={d['def_ry']:.1f})")
        if orient_devs:
            print("  remediation: a part rotated off its default RX/RY is an invented orientation (this is how")
            print("    gothic_castle_v02 produced bad spires/roofs). Use the part's default rotation, follow a")
            print("    recipe / CURVE_FOLLOW_CONTRACT, or — if the deviation is intentional and validated —")
            print("    declare ORIENTATION_OVERRIDE_IDS = {...} (or add the part to PART_ORIENTATION_OVERRIDES.md).")
            print("    RZ/facing changes are always allowed and never flagged here.")
    print("--- design-intent gate ---")
    if not di_active:
        print("  design-intent check: N/A (not a build-type request)")
    else:
        print(f"  committed design plan (every part has a purpose): {P(design_intent_ok)} ({len(di_issues)} issue(s))")
        for m in di_issues[:12]:
            print(f"    - {m}")
        if di_issues:
            print("  remediation: declare DESIGN_INTENT = {\"assemblies\": [{\"name\":..., \"is_a\":..., ")
            print("    \"target_read\":..., \"style_source\":\"CREATIVE_USE_CASE_AND_STYLE_INDEX: ...\", \"parts\":[")
            print("    {\"ObjectID\":..., \"purpose\":...}, ...]}, ...]} BEFORE placement. Source the read/style")
            print("    from the creative evidence; every used ObjectID must carry a non-empty purpose.")
    # part placement map coverage (informational; never affects the verdict)
    import os as _os, csv as _csv
    print("--- part placement map coverage ---")
    _sheet = _os.path.join(_os.path.dirname(libpath), "part_placement_maps", "part_placement_master_sheet.csv") if libpath else None
    if not _sheet or not _os.path.exists(_sheet) or len(placed) < 1:
        print("  coverage: SKIPPED (no placement map or no parts)")
    else:
        _vs = {}
        try:
            with open(_sheet, encoding="utf-8", newline="") as _fh:
                for _row in _csv.DictReader(_fh):
                    _vs[_row.get("part_id")] = _row.get("validation_status", "")
        except Exception:
            _vs = {}
        _used = sorted({p.get("ObjectID") for p in placed if p.get("ObjectID")})
        _val = [u for u in _used if _vs.get(u) == "validated"]
        _nomap = [u for u in _used if u not in _vs]
        _nv = [u for u in _used if u in _vs and _vs.get(u) != "validated"]
        print(f"  parts used: {len(_used)} | placement-validated: {len(_val)} | not validated: {len(_nv)} | not in map: {len(_nomap)}")
        for u in (_nv + _nomap)[:20]:
            print(f"    {u}  [{_vs.get(u, 'not_in_map')}]")
        if _nv or _nomap:
            print("  note: status is informational and never affects the verdict; non-validated parts are allowed.")
            print("    This column is a separate PLACEMENT-MAP PROOF LEDGER (map-only proof build + user sign-off,")
            print("    PART_PLACEMENT_MAP_SCHEMA) — NOT the verified-partmap geometry status. A part absent here can")
            print("    still be fully valid to use; it simply has no dedicated placement-map proof on file yet.")
    print("--- gate verdict ---")
    ok = (raw_prim==0 and has_addpart and (has_copy or has_wrapper_resolution)
          and len(wrapper_misuse)==0 and has_tagdel and nonuni==0
          and hidden_bake==0 and orientation_ok
          and err is None and (len(placed) > 0 or allow_zero_placed)
          and len(missing)==0 and len(prohibited)==0
          and len(nonuniform_runtime)==0 and libdiff == "NONE"
          and (not require_json_evidence or json_evidence_ok)
          and (not require_router or router_ok)
          and feature_recipe_ok
          and (not require_ai_capture_compliance or ai_capture_ok)
          and (not auto_design_intent_required or design_intent_ok)
          and (not require_validated_reuse or validated_reuse_ok)
          and (not auto_conformance_required or conformance_ok)
          and (not auto_intent_graph_required or intent_graph_ok)
          and (not build_sheet_required or build_sheet_ok)
          and (not capa_active or deeper_manifest_ok)
          and not template_leak
          and no_floats)
    print(f"  MACHINE-CHECKABLE GATE: {P(ok)}")
    _deferred = []
    if conformance_deferred: _deferred.append("recipe conformance")
    if intent_graph_deferred: _deferred.append("intent graph")
    if ok and _deferred:
        print("  validation tier: SCRIPT_VALIDATED — JSON validation DEFERRED (post-build): " + ", ".join(_deferred))
        print("    Run the build, export the NMS base JSON, then re-run with --require-conformance/--require-intent-graph <exported.json> to reach JSON/GAME validation.")
    print("  Note: visual taste and non-implemented family recipes still require review; validated-recipe reuse/conformance and protected"
          " subsystems still require screenshot/JSON review and provenance manifest.")
    return 0 if ok else 2

if __name__ == "__main__":
    sys.exit(main())
