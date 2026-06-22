bl_info = {
    "name": "NMS Build Feedback Triage",
    "author": "OpenAI / NMS Builder workflow",
    "version": (0, 4, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > NMS Triage",
    "description": "NMS-aware assembly-first build feedback triage with human review bundles, zipped output, clipboard settings, screenshots, and AI repair prompts.",
    "category": "3D View",
}

import bpy
import json
import math
import os
import re
import time
import zipfile
import shutil
from pathlib import Path
from mathutils import Vector


# ---------------------------------------------------------------------------
# Constants / doctrine references
# ---------------------------------------------------------------------------

TRIAGE_DOC_NAMES = [
    "PLACEMENT_PRECEDENCE.json",
    "PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md",
    "PROJECT_BUILD_PLACEMENT_PACKET.json",
]

MECHANICAL_PACKET_FIELDS = [
    "required placement method",
    "allowed placement methods",
    "forbidden methods",
    "governing precedence tier",
    "applicable rules",
    "known recipes",
    "snap / connector guidance",
    "orientation requirements",
    "up-axis / front-axis / rotation constraints",
    "scaling constraints",
    "required offsets or overlap behavior",
    "assembly-context requirements",
    "negative knowledge warnings",
]

DEFAULT_SKIP_TOKEN = "!!!!SKIP"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def safe_name(text, limit=140):
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
    out = "".join(c if c in allowed else "_" for c in str(text))
    return out[:limit] or "unnamed"


def now_stamp():
    return time.strftime("%Y%m%d_%H%M%S")


def load_json(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=False)


def write_text(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def parse_float_list(value):
    if value is None:
        return None
    if isinstance(value, (list, tuple)) and len(value) >= 3:
        try:
            return [float(value[0]), float(value[1]), float(value[2])]
        except Exception:
            return None
    if isinstance(value, str):
        try:
            data = json.loads(value)
            if isinstance(data, list) and len(data) >= 3:
                return [float(data[0]), float(data[1]), float(data[2])]
        except Exception:
            pass
    return None


def object_world_bbox(obj):
    try:
        pts = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        return mn, mx, pts
    except Exception:
        loc = obj.location.copy()
        return loc, loc, [loc]


def bbox_center(mn, mx):
    return (mn + mx) * 0.5


def bbox_size(mn, mx):
    return Vector((max(0, mx.x - mn.x), max(0, mx.y - mn.y), max(0, mx.z - mn.z)))


def xy_overlap_area(a_mn, a_mx, b_mn, b_mx):
    dx = min(a_mx.x, b_mx.x) - max(a_mn.x, b_mn.x)
    dy = min(a_mx.y, b_mx.y) - max(a_mn.y, b_mn.y)
    if dx <= 0 or dy <= 0:
        return 0.0
    return dx * dy


def bbox_intersection_volume(a_mn, a_mx, b_mn, b_mx):
    dx = min(a_mx.x, b_mx.x) - max(a_mn.x, b_mn.x)
    dy = min(a_mx.y, b_mx.y) - max(a_mn.y, b_mn.y)
    dz = min(a_mx.z, b_mx.z) - max(a_mn.z, b_mn.z)
    if dx <= 0 or dy <= 0 or dz <= 0:
        return 0.0
    return dx * dy * dz


def nearest_multiple_delta(deg, step):
    if step <= 0:
        return 0.0
    q = round(deg / step) * step
    return abs(deg - q)


def obj_rotation_degrees(obj):
    return [math.degrees(v) for v in obj.rotation_euler]


def is_mesh_like(obj):
    return obj.type in {"MESH", "EMPTY"} and not obj.name.startswith("NMS_TRIAGE_")


def visible_candidate(obj, include_hidden):
    if not include_hidden and obj.hide_get():
        return False
    return is_mesh_like(obj)


# ---------------------------------------------------------------------------
# NMS knowledge loading
# ---------------------------------------------------------------------------

class NMSKnowledge:
    def __init__(self, root):
        self.root = Path(root) if root else None
        self.part_map = {}
        self.known_ids = set()
        self.families_by_oid = {}
        self.family_rules_by_family = {}
        self.negative = {}
        self.method_authority = {}
        self.rule_map = {}
        self.errors = []
        if self.root:
            self.load()

    def rel(self, *parts):
        return str(self.root.joinpath(*parts))

    def load(self):
        # Master verified part map
        pm = load_json(self.rel("library", "nms_master_part_map_verified_data_v3_01_02.json"), [])
        if isinstance(pm, list):
            for row in pm:
                if not isinstance(row, dict):
                    continue
                oid = str(row.get("ObjectID", "")).strip("^").strip()
                if oid:
                    self.part_map[oid] = row
                    self.known_ids.add(oid)

        # Part placement map index may contain additional ids
        pmi = load_json(self.rel("library", "part_placement_maps", "part_placement_map_index.json"), {})
        if isinstance(pmi, dict):
            for k in list(pmi.keys()):
                oid = str(k).strip("^").strip()
                if oid:
                    self.known_ids.add(oid)

        # Families
        pf = load_json(self.rel("rules", "PART_FAMILY_RULES.json"), {})
        if isinstance(pf, dict):
            families = pf.get("families", [])
            if isinstance(families, dict):
                families = [dict({"family_id": k}, **(v if isinstance(v, dict) else {"raw": v})) for k, v in families.items()]
            for fam in families:
                if not isinstance(fam, dict):
                    continue
                fid = str(fam.get("family_id") or fam.get("FamilyID") or fam.get("id") or fam.get("name") or "").strip()
                if not fid:
                    continue
                self.family_rules_by_family[fid] = fam
                members = fam.get("members") or fam.get("object_ids") or fam.get("ObjectIDs") or []
                if isinstance(members, (str, int, float)):
                    members = [members]
                if isinstance(members, dict):
                    members = list(members.keys())
                for m in members:
                    if isinstance(m, dict):
                        oid = str(m.get("ObjectID") or m.get("object_id") or m.get("id") or "").strip("^").strip()
                    else:
                        oid = str(m).strip("^").strip()
                    if oid:
                        self.families_by_oid.setdefault(oid, []).append(fid)
                        self.known_ids.add(oid)

        # Negative knowledge
        neg = load_json(self.rel("data", "NEGATIVE_KNOWLEDGE_INDEX.json"), {})
        if isinstance(neg, dict):
            entries = neg.get("entries", {})
            if isinstance(entries, dict):
                self.negative = {str(k).strip("^"): v for k, v in entries.items()}

        # Method authority
        mat = load_json(self.rel("data", "METHOD_AUTHORITY_TABLE.json"), {})
        if isinstance(mat, dict):
            self.method_authority = mat.get("method_definitions", {}) or {}

        # Rule applicability
        ram = load_json(self.rel("data", "RULE_PART_APPLICABILITY_MAP.json"), {})
        if isinstance(ram, dict):
            rules = ram.get("rules", [])
            if isinstance(rules, dict):
                rules = [dict({"rule_id": k}, **(v if isinstance(v, dict) else {"raw": v})) for k, v in rules.items()]
            for r in rules:
                if not isinstance(r, dict):
                    continue
                rid = r.get("rule_id") or r.get("RuleID") or r.get("id")
                if rid:
                    self.rule_map.setdefault(str(rid), r)

    def infer_oid(self, obj):
        # Prefer explicit custom properties written by builder/importer.
        for key in ("ObjectID", "object_id", "NMS_ObjectID", "SnapID"):
            if key in obj:
                val = str(obj.get(key, "")).strip("^").strip()
                if val:
                    return val

        name = obj.name.upper()
        name = name.replace(DEFAULT_SKIP_TOKEN, "")
        # Longest known ObjectID contained in object name wins.
        # This avoids B_RAMP matching before B_RAMP_H, etc.
        candidates = []
        for oid in self.known_ids:
            u = oid.upper()
            if u and u in name:
                candidates.append(oid)
        if candidates:
            return sorted(candidates, key=len, reverse=True)[0]

        # Fallback: derive likely ObjectID token from Blender name.
        # Example: "B_RAMP_012" => "B_RAMP"; "PIPE.001" => "PIPE".
        cleaned = re.sub(r"\.\d+$", "", name)
        cleaned = re.sub(r"[^A-Z0-9_]+", "_", cleaned)
        tokens = cleaned.split("_")
        if len(tokens) >= 2:
            # Try prefixes of decreasing length.
            for n in range(min(5, len(tokens)), 0, -1):
                cand = "_".join(tokens[:n])
                if cand in self.known_ids:
                    return cand
        return ""

    def family_for(self, oid):
        fams = self.families_by_oid.get(oid, [])
        if fams:
            return fams
        row = self.part_map.get(oid, {})
        guesses = []
        for k in ("PartClassGuess", "SnapGroups", "LikelyRole", "Category", "SubCategory"):
            v = row.get(k)
            if v:
                guesses.append(str(v))
        return guesses[:3]

    def part_details(self, oid):
        return self.part_map.get(oid, {})

    def negative_entry(self, oid):
        return self.negative.get(oid)

    def applicable_rule_summaries(self, oid):
        fams = {f.lower() for f in self.family_for(oid)}
        hits = []
        for rid, r in self.rule_map.items():
            ids = {str(x).strip("^") for x in r.get("object_ids", [])}
            rfams = {str(x).lower() for x in r.get("families", [])}
            scope = r.get("scope", "")
            if oid in ids or (fams and fams.intersection(rfams)) or scope == "UNIVERSAL_PROCESS":
                hits.append({
                    "rule_id": rid,
                    "file": r.get("file"),
                    "scope": scope,
                    "families": list(r.get("families", []))[:8],
                })
        return hits[:15]


# ---------------------------------------------------------------------------
# Issue creation
# ---------------------------------------------------------------------------

def make_issue(issue_id, severity, issue_type, obj=None, summary="", evidence=None, suggested_fix=""):
    return {
        "issue_id": issue_id,
        "severity": severity,
        "type": issue_type,
        "object_name": obj.name if obj else None,
        "object_id": obj.get("_nms_resolved_oid", "") if obj and "_nms_resolved_oid" in obj else None,
        "summary": summary,
        "evidence": evidence or {},
        "suggested_next_step": suggested_fix,
        "triage_status": "REVIEW_RECOMMENDED",
    }


def severity_rank(sev):
    return {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}.get(sev, 5)


# ---------------------------------------------------------------------------
# Core triage
# ---------------------------------------------------------------------------

def run_triage_analysis(context, settings, knowledge):
    """V0.3 assembly-first triage with clustered continuity and buried-detail review.

    Important design change:
    - This is not a CAD validator.
    - Rotations/intersections/walkable pair spam are no longer treated as primary findings.
    - Findings are capped and summarized so a known-good reference build should produce a small, reviewable list.
    """
    include_hidden = settings.include_hidden
    skip_token = settings.skip_token or DEFAULT_SKIP_TOKEN

    objects = [o for o in context.scene.objects if visible_candidate(o, include_hidden)]
    review_objects = []
    skipped_objects = []

    # Resolve ids once.
    for o in objects:
        oid = knowledge.infer_oid(o) if knowledge else ""
        o["_nms_resolved_oid"] = oid
        if skip_token and skip_token in o.name:
            skipped_objects.append(o)
        else:
            review_objects.append(o)

    # Cache bboxes.
    bb = {}
    for o in review_objects:
        mn, mx, pts = object_world_bbox(o)
        bb[o.name] = {"mn": mn, "mx": mx, "center": bbox_center(mn, mx), "size": bbox_size(mn, mx)}

    issues = []
    observations = []
    seq = 1

    def add(sev, typ, obj=None, summary="", evidence=None, fix=""):
        nonlocal seq
        if len(issues) >= settings.max_primary_findings:
            return
        issues.append(make_issue(f"TRIAGE-{seq:04d}", sev, typ, obj, summary, evidence, fix))
        seq += 1

    def observe(typ, obj=None, summary="", evidence=None):
        observations.append({
            "type": typ,
            "object_name": obj.name if obj else None,
            "object_id": obj.get("_nms_resolved_oid", "") if obj and "_nms_resolved_oid" in obj else None,
            "summary": summary,
            "evidence": evidence or {},
        })

    # ------------------------------------------------------------------
    # 1) Hard-ish metadata / governance review findings.
    # ------------------------------------------------------------------
    unknown_count = 0
    for o in review_objects:
        oid = o.get("_nms_resolved_oid", "")
        if not oid:
            unknown_count += 1
            if unknown_count <= 15:
                add(
                    "HIGH",
                    "UNKNOWN_OBJECT_ID",
                    o,
                    "ObjectID could not be resolved from custom properties or Blender object name.",
                    {"object_name": o.name},
                    "Assign the correct NMS ObjectID custom property or rename object with a recognizable ObjectID. Do not infer placement behavior without ObjectID coverage."
                )
            continue

        neg = knowledge.negative_entry(oid) if knowledge else None
        if neg:
            add(
                "MEDIUM" if not isinstance(neg, dict) or neg.get("severity") != "CRITICAL" else "HIGH",
                "NEGATIVE_KNOWLEDGE_REVIEW_REQUIRED",
                o,
                f"{oid} has negative-knowledge or contextual-validation guidance.",
                {
                    "status": neg.get("status") if isinstance(neg, dict) else None,
                    "severity": neg.get("severity") if isinstance(neg, dict) else None,
                    "forbidden_methods": neg.get("forbidden_methods", []) if isinstance(neg, dict) else [],
                    "required_method": neg.get("required_method") if isinstance(neg, dict) else None,
                    "reason": neg.get("reason") if isinstance(neg, dict) else str(neg),
                },
                "Check the Project Build Packet entry for this ObjectID and verify the required method / forbidden methods before repairing."
            )

    if unknown_count > 15:
        observe("UNKNOWN_OBJECT_ID_SUPPRESSED_COUNT", None, f"{unknown_count - 15} additional unknown ObjectID findings suppressed.", {"suppressed_count": unknown_count - 15})

    # ------------------------------------------------------------------
    # 2) Transform checks. Keep severe scale as findings; odd rotation is
    #    observation-only unless user enables legacy mode.
    # ------------------------------------------------------------------
    odd_rotation_count = 0
    nonuniform_count = 0
    for o in review_objects:
        sc = [abs(float(v)) for v in o.scale]
        if min(sc) <= settings.min_abs_scale:
            add("CRITICAL", "IMPOSSIBLE_OR_ZERO_SCALE", o,
                "Object has near-zero scale on at least one axis.",
                {"scale": list(o.scale)},
                "Restore documented scale behavior from the Project Build Packet or part map; do not invent corrective scaling.")
        elif max(sc) >= settings.max_abs_scale:
            add("HIGH", "EXTREME_SCALE", o,
                "Object scale exceeds configured maximum.",
                {"scale": list(o.scale), "threshold": settings.max_abs_scale},
                "Check scaling constraints in the Project Build Packet and part map.")
        elif (max(sc) / max(min(sc), 1e-6)) >= settings.nonuniform_scale_ratio:
            nonuniform_count += 1
            if settings.legacy_geometry_noise_mode and nonuniform_count <= 20:
                add("LOW", "NONUNIFORM_SCALE_REVIEW", o,
                    "Object has high non-uniform scale ratio.",
                    {"scale": list(o.scale), "ratio": max(sc) / max(min(sc), 1e-6)},
                    "Verify whether non-uniform scaling is documented for this part.")

        if settings.flag_odd_rotations:
            degs = obj_rotation_degrees(o)
            deltas = [nearest_multiple_delta(d, settings.rotation_step_degrees) for d in degs]
            if max(deltas) > settings.rotation_tolerance_degrees:
                odd_rotation_count += 1
                if settings.legacy_geometry_noise_mode and odd_rotation_count <= 20:
                    add("LOW", "ODD_ROTATION_REVIEW", o,
                        "Rotation is not near the configured documented increment.",
                        {"rotation_degrees": degs, "step": settings.rotation_step_degrees, "max_delta": max(deltas)},
                        "Check orientation requirements, up-axis/front-axis, and rotation constraints in the Project Build Packet.")
    if odd_rotation_count:
        observe("ODD_ROTATION_OBSERVATION_COUNT", None, "Odd rotations observed but suppressed as primary findings because NMS decorative builds commonly use intentional non-grid rotations.", {"count": odd_rotation_count})
    if nonuniform_count and not settings.legacy_geometry_noise_mode:
        observe("NONUNIFORM_SCALE_OBSERVATION_COUNT", None, "Nonuniform scale observations suppressed unless legacy geometry noise mode is enabled.", {"count": nonuniform_count})

    # ------------------------------------------------------------------
    # 3) Assembly continuity candidates: gaps between objects that appear
    #    intended to connect. This replaces per-part floating spam.
    # ------------------------------------------------------------------
    gap_candidates = []
    floor_z = settings.scene_floor_z

    def family_blob(o):
        oid = o.get("_nms_resolved_oid", "")
        return (" ".join(knowledge.family_for(oid)) + " " + oid + " " + o.name).upper() if knowledge else (oid + " " + o.name).upper()

    def is_candidate_structural(o):
        blob = family_blob(o)
        return any(t in blob for t in ("FLOOR", "RAMP", "STAIR", "BRIDGE", "WALKWAY", "PLATFORM", "WALL", "ROOF", "DOME", "ARCH", "COLUMN", "PILLAR"))

    structural_objs = [o for o in review_objects if o.name in bb and is_candidate_structural(o)]
    # Pair cap is intentionally lower in v0.2. We want candidate issues, not exhaustive geometry logs.
    pair_limit = min(settings.max_pair_checks, 75000)
    pair_count = 0
    for i, a_obj in enumerate(structural_objs):
        if pair_count >= pair_limit or len(gap_candidates) >= settings.max_gap_candidates:
            break
        a = bb.get(a_obj.name)
        if not a:
            continue
        for b_obj in structural_objs[i + 1:]:
            pair_count += 1
            if pair_count >= pair_limit or len(gap_candidates) >= settings.max_gap_candidates:
                break
            b = bb.get(b_obj.name)
            if not b:
                continue

            # Vertical stacking gap: overlapping in XY, small positive Z gap.
            xy_ov = xy_overlap_area(a["mn"], a["mx"], b["mn"], b["mx"])
            a_xy_area = max(1e-6, (a["mx"].x - a["mn"].x) * (a["mx"].y - a["mn"].y))
            b_xy_area = max(1e-6, (b["mx"].x - b["mn"].x) * (b["mx"].y - b["mn"].y))
            xy_ratio = xy_ov / min(a_xy_area, b_xy_area)

            z_gap_ab = b["mn"].z - a["mx"].z
            z_gap_ba = a["mn"].z - b["mx"].z
            z_gap = z_gap_ab if z_gap_ab > 0 else z_gap_ba
            if xy_ratio >= settings.assembly_xy_overlap_ratio and settings.assembly_min_gap <= z_gap <= settings.assembly_max_gap:
                upper = b_obj if z_gap_ab > 0 else a_obj
                lower = a_obj if z_gap_ab > 0 else b_obj
                gap_candidates.append((z_gap, xy_ratio, upper, lower, "VERTICAL_ASSEMBLY_GAP"))
                continue

            # Side gap: same rough height, very close but not touching in plan.
            dx_gap = max(0, max(a["mn"].x, b["mn"].x) - min(a["mx"].x, b["mx"].x))
            dy_gap = max(0, max(a["mn"].y, b["mn"].y) - min(a["mx"].y, b["mx"].y))
            planar_gap = math.sqrt(dx_gap * dx_gap + dy_gap * dy_gap)
            z_overlap = max(0, min(a["mx"].z, b["mx"].z) - max(a["mn"].z, b["mn"].z))
            min_h = max(1e-6, min(a["size"].z, b["size"].z))
            if settings.assembly_min_gap <= planar_gap <= settings.assembly_side_gap and (z_overlap / min_h) >= 0.25:
                gap_candidates.append((planar_gap, z_overlap / min_h, a_obj, b_obj, "SIDE_ASSEMBLY_GAP"))

    # Cluster gap candidates so repeated pattern issues do not spam the report.
    # V0.3 principle: report "dome/ring/platform continuity cluster", not 50 single parts.
    def gap_cluster_key(item):
        gap, score, a_obj, b_obj, typ = item
        aid = a_obj.get("_nms_resolved_oid", "") or a_obj.name.split(".")[0]
        bid = b_obj.get("_nms_resolved_oid", "") or b_obj.name.split(".")[0]
        pair = tuple(sorted([aid, bid]))
        return (typ, pair[0], pair[1])

    clusters = {}
    for item in gap_candidates:
        clusters.setdefault(gap_cluster_key(item), []).append(item)

    clustered = []
    for key, items in clusters.items():
        items.sort(key=lambda x: x[0], reverse=True)
        max_gap = max(x[0] for x in items)
        min_gap = min(x[0] for x in items)
        avg_gap = sum(x[0] for x in items) / max(1, len(items))
        top = items[0]
        clustered.append((max_gap, len(items), min_gap, avg_gap, key, top, items[:5]))
    clustered.sort(key=lambda x: (x[1], x[0]), reverse=True)

    for max_gap, count, min_gap, avg_gap, key, top, examples in clustered[:settings.max_gap_findings]:
        typ, ida, idb = key
        gap, score, a_obj, b_obj, raw_typ = top
        sev = "HIGH" if max_gap >= settings.assembly_high_gap and count >= 2 else "MEDIUM"
        issue_type = "VISUAL_CONTINUITY_REVIEW" if raw_typ == "SIDE_ASSEMBLY_GAP" else "ASSEMBLY_DISCONTINUITY_CANDIDATE"
        ex = []
        for egap, escore, ea, eb, etyp in examples:
            ca = bb.get(ea.name, {}).get("center")
            cb = bb.get(eb.name, {}).get("center")
            ex.append({
                "object": ea.name,
                "object_id": ea.get("_nms_resolved_oid", ""),
                "other_object": eb.name,
                "other_object_id": eb.get("_nms_resolved_oid", ""),
                "gap": round(float(egap), 4),
                "object_center": [round(ca.x, 3), round(ca.y, 3), round(ca.z, 3)] if ca else None,
                "other_center": [round(cb.x, 3), round(cb.y, 3), round(cb.z, 3)] if cb else None,
            })
        add(sev, issue_type, a_obj,
            f"{raw_typ} cluster between {ida} and {idb}: {count} candidate gap(s), max gap {max_gap:.3f}.",
            {
                "cluster_type": raw_typ,
                "object_id_pair": [ida, idb],
                "candidate_count": count,
                "gap_min": round(float(min_gap), 4),
                "gap_avg": round(float(avg_gap), 4),
                "gap_max": round(float(max_gap), 4),
                "relationship_score": round(float(score), 4),
                "example_pairs": ex,
            },
            "Review this as a repeated assembly/visual continuity issue. Locate the example object centers in Blender. Check PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md and the Project Build Packet for the documented connector, offset, orientation, or overlap behavior before repairing.")
    if len(clustered) > settings.max_gap_findings:
        observe("ASSEMBLY_GAP_CLUSTER_SUPPRESSED_COUNT", None, "Additional assembly gap clusters suppressed after top findings.", {"cluster_count": len(clustered), "reported": settings.max_gap_findings, "raw_candidate_count": len(gap_candidates)})
    elif len(gap_candidates) > 0:
        observe("ASSEMBLY_GAP_CLUSTERING_SUMMARY", None, "Raw gap candidates were clustered before reporting.", {"raw_candidate_count": len(gap_candidates), "cluster_count": len(clustered)})


    # ------------------------------------------------------------------
    # 3b) Floating ornamental / cap stack review.
    #     This catches cases like stacked spheres, roof/cap pieces, and decorative
    #     elements that should either touch/support visually or carry !!!!SKIP.
    # ------------------------------------------------------------------
    float_candidates = []
    all_objs_for_float = [o for o in review_objects if o.name in bb]
    for upper in all_objs_for_float:
        u = bb.get(upper.name)
        if not u:
            continue
        best = None
        upper_blob = family_blob(upper)
        # Review likely visual/cap/detail objects. Do not require NMS exact family.
        likely_detail_or_cap = any(t in upper_blob for t in (
            "SPHERE", "BALL", "ORB", "CAP", "ROOF", "DOME", "CROWN", "LIGHT", "DECOR", "SIGN", "BEACON", "PILLAR", "COLUMN"
        ))
        if not likely_detail_or_cap and u["size"].z > 2.5:
            continue
        for lower in all_objs_for_float:
            if lower == upper:
                continue
            l = bb.get(lower.name)
            if not l:
                continue
            z_gap = u["mn"].z - l["mx"].z
            if not (settings.assembly_min_gap <= z_gap <= settings.assembly_max_gap):
                continue
            xy_ov = xy_overlap_area(u["mn"], u["mx"], l["mn"], l["mx"])
            u_area = max(1e-6, (u["mx"].x - u["mn"].x) * (u["mx"].y - u["mn"].y))
            l_area = max(1e-6, (l["mx"].x - l["mn"].x) * (l["mx"].y - l["mn"].y))
            xy_ratio = xy_ov / min(u_area, l_area)
            if xy_ratio >= max(0.04, settings.assembly_xy_overlap_ratio * 0.5):
                if best is None or z_gap < best[0]:
                    best = (z_gap, xy_ratio, lower)
        if best:
            z_gap, xy_ratio, lower = best
            float_candidates.append((z_gap, xy_ratio, upper, lower))
    float_candidates.sort(key=lambda x: x[0], reverse=True)
    for z_gap, xy_ratio, upper, lower in float_candidates[:10]:
        cu = bb.get(upper.name, {}).get("center")
        cl = bb.get(lower.name, {}).get("center")
        add(
            "HIGH" if z_gap >= settings.assembly_high_gap else "MEDIUM",
            "FLOATING_ORNAMENT_STACK_REVIEW",
            upper,
            f"{upper.name} appears vertically separated from likely support {lower.name} by {z_gap:.3f}.",
            {
                "gap": round(float(z_gap), 4),
                "xy_overlap_ratio": round(float(xy_ratio), 4),
                "affected_objects": [upper.name, lower.name],
                "upper_object_id": upper.get("_nms_resolved_oid", ""),
                "lower_object_id": lower.get("_nms_resolved_oid", ""),
                "upper_center": [round(cu.x, 3), round(cu.y, 3), round(cu.z, 3)] if cu else None,
                "lower_center": [round(cl.x, 3), round(cl.y, 3), round(cl.z, 3)] if cl else None,
            },
            "If this is intentional, add !!!!SKIP to the object name. Otherwise rotate/offset/snap it so the decorative stack or cap visually connects to its support."
        )
    if len(float_candidates) > 10:
        observe("FLOATING_ORNAMENT_STACK_SUPPRESSED_COUNT", None, "Additional floating ornament/cap stack candidates suppressed.", {"candidate_count": len(float_candidates), "reported": 10})



    # ------------------------------------------------------------------
    # 4) Buried / low-contribution detail candidates.
    #    This is not a placement failure. It flags parts that may be mostly
    #    hidden inside larger geometry and therefore not contributing visibly.
    # ------------------------------------------------------------------
    buried_candidates = []
    pair_count = 0
    for i, small_obj in enumerate(review_objects):
        if len(buried_candidates) >= settings.max_buried_detail_findings:
            break
        s = bb.get(small_obj.name)
        if not s:
            continue
        s_size = s["size"]
        s_vol = max(1e-6, s_size.x * s_size.y * s_size.z)
        if s_vol <= 0.0001:
            continue
        for big_obj in review_objects:
            if small_obj == big_obj:
                continue
            pair_count += 1
            if pair_count >= pair_limit:
                break
            b = bb.get(big_obj.name)
            if not b:
                continue
            b_size = b["size"]
            b_vol = max(1e-6, b_size.x * b_size.y * b_size.z)
            if b_vol <= s_vol * 1.25:
                continue
            inter = bbox_intersection_volume(s["mn"], s["mx"], b["mn"], b["mx"])
            ratio = inter / s_vol
            if ratio >= settings.buried_detail_ratio:
                buried_candidates.append((ratio, small_obj, big_obj))
                break

    buried_candidates.sort(key=lambda x: x[0], reverse=True)
    for ratio, small_obj, big_obj in buried_candidates[:settings.max_buried_detail_findings]:
        c = bb.get(small_obj.name, {}).get("center")
        add("LOW", "DETAIL_VISIBILITY_REVIEW", small_obj,
            f"{small_obj.name} appears mostly buried/occluded inside or behind {big_obj.name}.",
            {
                "occluding_object": big_obj.name,
                "estimated_bbox_occlusion_ratio": round(float(ratio), 4),
                "object_center": [round(c.x, 3), round(c.y, 3), round(c.z, 3)] if c else None,
            },
            "This is a design-effectiveness review, not a failure. If the part is intended as visible detail or an effect source, expose/reposition it. If intentionally buried for support, mark with !!!!SKIP.")
    if len(buried_candidates) > settings.max_buried_detail_findings:
        observe("BURIED_DETAIL_SUPPRESSED_COUNT", None, "Additional buried/low-contribution detail candidates suppressed.", {"candidate_count": len(buried_candidates), "reported": settings.max_buried_detail_findings})

    # ------------------------------------------------------------------
    # 5) Intersections: observation-only by default. Report only severe,
    #    high-volume collisions unless legacy mode enabled.
    # ------------------------------------------------------------------
    intersection_count = 0
    severe_intersections = []
    n = len(review_objects)
    pair_count = 0
    for i in range(n):
        if pair_count >= pair_limit or len(severe_intersections) >= settings.max_intersection_findings:
            break
        a_obj = review_objects[i]
        a = bb.get(a_obj.name)
        if not a:
            continue
        for j in range(i + 1, n):
            pair_count += 1
            if pair_count >= pair_limit or len(severe_intersections) >= settings.max_intersection_findings:
                break
            b_obj = review_objects[j]
            b = bb.get(b_obj.name)
            if not b:
                continue
            vol = bbox_intersection_volume(a["mn"], a["mx"], b["mn"], b["mx"])
            if vol <= settings.intersection_volume_threshold:
                continue
            a_size = a["size"]
            b_size = b["size"]
            a_vol = max(1e-6, a_size.x * a_size.y * a_size.z)
            b_vol = max(1e-6, b_size.x * b_size.y * b_size.z)
            ratio = vol / min(a_vol, b_vol)
            if ratio >= settings.intersection_ratio_threshold:
                intersection_count += 1
                if ratio >= settings.severe_intersection_ratio:
                    severe_intersections.append((ratio, vol, a_obj, b_obj))

    severe_intersections.sort(key=lambda x: x[0], reverse=True)
    for ratio, vol, a_obj, b_obj in severe_intersections[:settings.max_intersection_findings]:
        add("MEDIUM", "SEVERE_INTERSECTION_REVIEW", a_obj,
            f"Large intersection with {b_obj.name}.",
            {"other_object": b_obj.name, "intersection_volume": vol, "ratio_vs_smaller_bbox": ratio},
            "NMS decorative overlap is often intentional. Review only if this looks visually destructive or contradicts packet overlap/offset behavior.")
    if intersection_count:
        observe("INTERSECTION_OBSERVATION_COUNT", None, "Intersection candidates observed; most are suppressed because intentional overlap is common in NMS builds.", {"candidate_count": intersection_count, "severe_reported": len(severe_intersections[:settings.max_intersection_findings])})

    # ------------------------------------------------------------------
    # 5) Duplicate/object outlier checks: keep small and reviewable.
    # ------------------------------------------------------------------
    duplicate_count = 0
    for i in range(n):
        if duplicate_count >= settings.max_duplicate_findings:
            break
        a_obj = review_objects[i]
        a = bb.get(a_obj.name)
        if not a:
            continue
        for j in range(i + 1, n):
            b_obj = review_objects[j]
            b = bb.get(b_obj.name)
            if not b:
                continue
            if a_obj.get("_nms_resolved_oid", "") and a_obj.get("_nms_resolved_oid", "") == b_obj.get("_nms_resolved_oid", ""):
                dist = (a["center"] - b["center"]).length
                if dist <= settings.duplicate_center_distance:
                    duplicate_count += 1
                    add("MEDIUM", "DUPLICATE_OVERLAP_CANDIDATE", a_obj,
                        f"Possible duplicate overlapping same ObjectID with {b_obj.name}.",
                        {"other_object": b_obj.name, "center_distance": dist},
                        "Confirm whether the duplicate is intentional. If yes, mark with !!!!SKIP for visual triage noise; if no, remove or reposition through packet-approved placement logic.")
                    break

    centers = [bb[o.name]["center"] for o in review_objects if o.name in bb]
    outlier_count = 0
    if centers:
        mean = Vector((sum(c.x for c in centers) / len(centers), sum(c.y for c in centers) / len(centers), sum(c.z for c in centers) / len(centers)))
        for o in review_objects:
            c = bb.get(o.name, {}).get("center")
            if c and (c - mean).length > settings.outlier_distance:
                outlier_count += 1
                if outlier_count <= settings.max_outlier_findings:
                    add("LOW", "OUTLIER_DISTANCE_REVIEW", o,
                        "Object is far from the build's average center.",
                        {"distance_from_scene_mean": (c - mean).length, "threshold": settings.outlier_distance},
                        "Confirm whether this is an intentional remote element or a misplaced part.")
        if outlier_count > settings.max_outlier_findings:
            observe("OUTLIER_SUPPRESSED_COUNT", None, "Additional outlier candidates suppressed.", {"count": outlier_count, "reported": settings.max_outlier_findings})

    issues.sort(key=lambda x: (severity_rank(x["severity"]), x["issue_id"]))

    issue_type_counts = {}
    for issue in issues:
        issue_type_counts[issue["type"]] = issue_type_counts.get(issue["type"], 0) + 1

    observation_type_counts = {}
    for obs in observations:
        observation_type_counts[obs["type"]] = observation_type_counts.get(obs["type"], 0) + 1

    knowledge_summary = {
        "package_root": str(knowledge.root) if knowledge and knowledge.root else "",
        "known_object_ids_loaded": len(knowledge.known_ids) if knowledge else 0,
        "part_map_rows_loaded": len(knowledge.part_map) if knowledge else 0,
        "family_mappings_loaded": len(knowledge.families_by_oid) if knowledge else 0,
        "negative_knowledge_entries_loaded": len(knowledge.negative) if knowledge else 0,
        "method_authority_entries_loaded": len(knowledge.method_authority) if knowledge else 0,
        "rule_map_entries_loaded": len(knowledge.rule_map) if knowledge else 0,
    }

    return {
        "schema": "NMS_BUILD_FEEDBACK_TRIAGE_REPORT_4.0",
        "triage_type": "BUILD_FEEDBACK_TRIAGE_NOT_AUDIT_NOT_CAPA",
        "triage_philosophy": "ASSEMBLY_FIRST_COMPONENT_SECOND",
        "generated_at": now_stamp(),
        "scene": context.scene.name,
        "skip_token": skip_token,
        "reviewed_object_count": len(review_objects),
        "skipped_object_count": len(skipped_objects),
        "skipped_objects": [o.name for o in skipped_objects],
        "knowledge_summary": knowledge_summary,
        "thresholds": {
            "assembly_min_gap": settings.assembly_min_gap,
            "assembly_max_gap": settings.assembly_max_gap,
            "assembly_side_gap": settings.assembly_side_gap,
            "assembly_xy_overlap_ratio": settings.assembly_xy_overlap_ratio,
            "severe_intersection_ratio": settings.severe_intersection_ratio,
            "buried_detail_ratio": settings.buried_detail_ratio,
            "duplicate_center_distance": settings.duplicate_center_distance,
            "outlier_distance": settings.outlier_distance,
        },
        "issue_type_counts": issue_type_counts,
        "observation_type_counts": observation_type_counts,
        "observations": observations[:200],
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Screenshot capture
# ---------------------------------------------------------------------------

def scene_bbox(objects):
    pts = []
    for o in objects:
        try:
            pts.extend([o.matrix_world @ Vector(c) for c in o.bound_box])
        except Exception:
            pts.append(o.location.copy())
    if not pts:
        return Vector((-5, -5, -5)), Vector((5, 5, 5))
    return Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts))), Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))


def ensure_camera(name):
    cam = bpy.data.objects.get(name)
    if cam and cam.type == "CAMERA":
        return cam
    data = bpy.data.cameras.new(name)
    cam = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(cam)
    return cam


def look_at(obj, target):
    direction = target - obj.location
    quat = direction.to_track_quat("-Z", "Y")
    obj.rotation_euler = quat.to_euler()


def render_camera_view(context, cam, out_path, resolution=1400):
    """Capture an OpenGL viewport-style render from the triage camera.

    V0.1 used full render, which can produce dark/blank images when scene lighting
    or render visibility is not configured. OpenGL render is closer to what the user
    sees in the viewport and is better for feedback triage.
    """
    scene = context.scene
    prev_camera = scene.camera
    prev_x = scene.render.resolution_x
    prev_y = scene.render.resolution_y
    prev_filepath = scene.render.filepath
    try:
        scene.camera = cam
        cam.data.clip_end = max(cam.data.clip_end, 100000.0)
        cam.data.clip_start = min(cam.data.clip_start, 0.01)
        scene.render.resolution_x = resolution
        scene.render.resolution_y = resolution
        scene.render.filepath = str(out_path)
        # Prefer viewport/OpenGL capture so unlit imported NMS geometry is visible.
        try:
            bpy.ops.render.opengl(write_still=True, view_context=False)
        except Exception:
            bpy.ops.render.render(write_still=True)
    finally:
        scene.camera = prev_camera
        scene.render.resolution_x = prev_x
        scene.render.resolution_y = prev_y
        scene.render.filepath = prev_filepath

def capture_fixed_angles(context, out_dir, settings):
    objects = [o for o in context.scene.objects if visible_candidate(o, settings.include_hidden)]
    mn, mx = scene_bbox(objects)
    center = (mn + mx) * 0.5
    size = bbox_size(mn, mx)
    radius = max(size.x, size.y, size.z, 10.0)
    dist = radius * 2.8

    shots = {
        "front": Vector((center.x, center.y - dist, center.z + radius * 0.25)),
        "right": Vector((center.x + dist, center.y, center.z + radius * 0.25)),
        "top": Vector((center.x, center.y, center.z + dist)),
        "iso": Vector((center.x + dist, center.y - dist, center.z + dist * 0.65)),
    }

    shot_paths = {}
    cam = ensure_camera("NMS_TRIAGE_CAPTURE_CAMERA")
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = max(size.x, size.y, size.z) * 1.35

    screenshots_dir = Path(out_dir) / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    for name, loc in shots.items():
        cam.location = loc
        look_at(cam, center)
        path = screenshots_dir / f"{name}.png"
        render_camera_view(context, cam, path, settings.screenshot_resolution)
        shot_paths[name] = str(path)

    return shot_paths


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def render_markdown_report(report, screenshot_paths):
    counts = {}
    for i in report["issues"]:
        counts[i["severity"]] = counts.get(i["severity"], 0) + 1

    lines = []
    lines.append("# NMS Build Feedback Triage Report")
    lines.append("")
    lines.append("> This is a BUILD FEEDBACK TRIAGE report, not an audit, CAPA, or compliance failure report.")
    lines.append("")
    lines.append(f"- Scene: `{report['scene']}`")
    lines.append(f"- Generated: `{report['generated_at']}`")
    lines.append(f"- Reviewed objects: `{report['reviewed_object_count']}`")
    lines.append(f"- Skipped objects: `{report['skipped_object_count']}`")
    lines.append(f"- Skip token: `{report['skip_token']}`")
    lines.append(f"- Severity counts: `{counts}`")
    lines.append(f"- Issue type counts: `{report.get('issue_type_counts', {})}`")
    lines.append(f"- Observation counts: `{report.get('observation_type_counts', {})}`")
    lines.append("")
    lines.append("## Knowledge Loaded")
    for k, v in report.get("knowledge_summary", {}).items():
        lines.append(f"- {k}: `{v}`")
    lines.append("")
    lines.append("## Screenshots")
    for k, v in screenshot_paths.items():
        lines.append(f"- {k}: `{v}`")
    lines.append("")
    lines.append("## Observations Suppressed From Primary Findings")
    obs_counts = report.get("observation_type_counts", {})
    if obs_counts:
        for k, v in obs_counts.items():
            lines.append(f"- {k}: `{v}`")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Human Review Index")
    lines.append("")
    lines.append("Each finding below includes exact Blender object names and a review question so the human can answer quickly without guessing.")
    lines.append("")
    lines.append("## Issues")
    if not report["issues"]:
        lines.append("")
        lines.append("No triage issues detected by configured checks.")
    for issue in report["issues"]:
        hr = issue.get("human_review", {})
        lines.append("")
        lines.append(f"### {issue.get('review_id', issue['issue_id'])} — {issue['severity']} — {issue['type']}")
        lines.append("")
        lines.append(f"- Triage ID: `{issue.get('issue_id')}`")
        lines.append(f"- Object: `{issue.get('object_name')}`")
        lines.append(f"- ObjectID: `{issue.get('object_id')}`")
        lines.append(f"- Summary: {issue.get('summary')}")
        lines.append(f"- Review question: {hr.get('review_question')}")
        lines.append(f"- Exact Blender objects to select: `{hr.get('exact_blender_objects_to_select', [])}`")
        lines.append(f"- Review center XYZ: `{hr.get('review_center_xyz')}`")
        lines.append(f"- Suggested next step: {issue.get('suggested_next_step')}")
        ev = issue.get("evidence") or {}
        if ev:
            lines.append("- Evidence:")
            for k, v in ev.items():
                lines.append(f"  - {k}: `{v}`")
    lines.append("")
    lines.append("## Intentional Design Handling")
    lines.append("")
    lines.append("If a flagged visual condition is intentional, rename the affected Blender object to include `!!!!SKIP`.")
    lines.append("Future triage scans will suppress normal visual triage warnings for objects whose Blender object name contains `!!!!SKIP`.")
    lines.append("Do not use `!!!!SKIP` to hide unknown ObjectIDs, corrupted transforms, missing packet coverage, or severe placement failures.")
    return "\n".join(lines) + "\n"


def render_ai_repair_prompt(report, screenshot_paths):
    lines = []
    lines.append("# AI Repair Prompt — NMS Build Feedback Triage")
    lines.append("")
    lines.append("You are reviewing an NMS Blender build using a BUILD FEEDBACK TRIAGE report.")
    lines.append("")
    lines.append("This is not an audit, CAPA, or compliance failure report. It is an assembly-first feedback triage report that identifies suspicious assembly discontinuities, gaps, severe transform problems, or package-knowledge reminders for review.")
    lines.append("")
    lines.append("Do not redesign the build. Fix only listed issues unless a directly related assembly continuity problem is discovered. Treat observations as context, not as required repairs.")
    lines.append("")
    lines.append("For each flagged issue:")
    lines.append("")
    lines.append("1. Review the evidence screenshots and geometry notes.")
    lines.append("")
    lines.append("2. Verify placement authority using these exact governance sources:")
    for doc in TRIAGE_DOC_NAMES:
        lines.append(f"   - `{doc}`")
    lines.append("")
    lines.append("3. In `PROJECT_BUILD_PLACEMENT_PACKET.json`, locate the specific ObjectID / part-family entry and look up the correcting behavior. Specifically check:")
    for field in MECHANICAL_PACKET_FIELDS:
        lines.append(f"   - {field}")
    lines.append("")
    lines.append("Do not invent a new fix if the packet already documents the correcting behavior. The good placement logic already exists and should not be reinvented.")
    lines.append("")
    lines.append("4. If the issue is intentional, mark it as `INTENTIONAL_DESIGN_CONFIRMED` and rename the affected Blender object to include `!!!!SKIP`.")
    lines.append("")
    lines.append("Future triage runs suppress normal visual triage warnings for objects whose Blender object name contains `!!!!SKIP`. Do not use `!!!!SKIP` to hide unknown ObjectIDs, corrupted transforms, missing packet coverage, or severe placement failures.")
    lines.append("")
    lines.append("5. If the correct behavior is unclear, do not guess. Ask the user for clarification and identify exactly what is missing:")
    lines.append("   - placement method")
    lines.append("   - ObjectID mapping")
    lines.append("   - part family rule")
    lines.append("   - recipe authority")
    lines.append("   - snap target")
    lines.append("   - orientation rule")
    lines.append("   - scale rule")
    lines.append("   - assembly context")
    lines.append("")
    lines.append("A repair recommendation must cite the correcting behavior from the Project Build Packet or placement hierarchy documents. If no correcting behavior is found, the recommendation must be `USER_CLARIFICATION_REQUIRED`.")
    lines.append("")
    lines.append("## Screenshot Evidence")
    for k, v in screenshot_paths.items():
        lines.append(f"- {k}: `{v}`")
    lines.append("")
    lines.append("## Triage Issues")
    if not report["issues"]:
        lines.append("No triage issues detected by configured checks.")
    else:
        for issue in report["issues"]:
            hr = issue.get("human_review", {})
            lines.append("")
            lines.append(f"### {issue.get('review_id', issue['issue_id'])} — {issue['severity']} — {issue['type']}")
            lines.append(f"- Triage ID: `{issue.get('issue_id')}`")
            lines.append(f"- Exact Blender objects: `{hr.get('exact_blender_objects_to_select', [])}`")
            lines.append(f"- Review center XYZ: `{hr.get('review_center_xyz')}`")
            lines.append(f"- Human question to ask: {hr.get('review_question')}")
            lines.append(f"- Summary: {issue.get('summary')}")
            lines.append(f"- Suggested next step: {issue.get('suggested_next_step')}")
            if issue.get("evidence"):
                lines.append(f"- Evidence: `{json.dumps(issue.get('evidence'), ensure_ascii=False)}`")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Blender properties / operator / panel
# ---------------------------------------------------------------------------

class NMS_Triage_Settings(bpy.types.PropertyGroup):
    package_root: bpy.props.StringProperty(
        name="NMS Package Root",
        description="Root folder containing library/, rules/, data/, validation/",
        subtype="DIR_PATH",
        default=""
    )
    output_dir: bpy.props.StringProperty(
        name="Output Folder",
        description="Folder where reports and screenshots are written",
        subtype="DIR_PATH",
        default="//nms_triage_output"
    )
    skip_token: bpy.props.StringProperty(
        name="Skip Token",
        description="Objects whose names contain this token skip normal visual triage warnings",
        default=DEFAULT_SKIP_TOKEN
    )
    include_hidden: bpy.props.BoolProperty(name="Include Hidden", default=False)
    capture_screenshots: bpy.props.BoolProperty(name="Capture Screenshots", default=True)
    screenshot_resolution: bpy.props.IntProperty(name="Screenshot Resolution", default=1400, min=256, max=4096)

    scene_floor_z: bpy.props.FloatProperty(name="Scene Floor Z", default=0.0)
    floating_gap: bpy.props.FloatProperty(name="Floating Gap", default=0.12, min=0.0)
    support_xy_overlap_ratio: bpy.props.FloatProperty(name="Support XY Overlap", default=0.08, min=0.0, max=1.0)
    intersection_volume_threshold: bpy.props.FloatProperty(name="Min Intersection Volume", default=0.001, min=0.0)
    intersection_ratio_threshold: bpy.props.FloatProperty(name="Intersection Ratio", default=0.10, min=0.0, max=1.0)
    intersection_depth: bpy.props.FloatProperty(name="Allowed Contact Depth", default=0.03, min=0.0)
    duplicate_center_distance: bpy.props.FloatProperty(name="Duplicate Center Dist", default=0.03, min=0.0)
    outlier_distance: bpy.props.FloatProperty(name="Outlier Distance", default=250.0, min=1.0)
    min_abs_scale: bpy.props.FloatProperty(name="Min Abs Scale", default=0.001, min=0.0)
    max_abs_scale: bpy.props.FloatProperty(name="Max Abs Scale", default=25.0, min=1.0)
    nonuniform_scale_ratio: bpy.props.FloatProperty(name="Nonuniform Scale Ratio", default=4.0, min=1.0)

    flag_odd_rotations: bpy.props.BoolProperty(name="Flag Odd Rotations", default=False)
    rotation_step_degrees: bpy.props.FloatProperty(name="Rotation Step", default=15.0, min=1.0, max=90.0)
    rotation_tolerance_degrees: bpy.props.FloatProperty(name="Rotation Tolerance", default=0.50, min=0.0, max=10.0)

    walkway_planar_gap: bpy.props.FloatProperty(name="Walkway Planar Gap", default=0.25, min=0.0)
    walkway_z_delta: bpy.props.FloatProperty(name="Walkway Z Delta", default=0.20, min=0.0)
    max_pair_checks: bpy.props.IntProperty(name="Max Pair Checks", default=250000, min=1000)
    max_walkable_checks: bpy.props.IntProperty(name="Max Walkable Checks", default=500, min=10)
    # V0.2 assembly-first controls
    legacy_geometry_noise_mode: bpy.props.BoolProperty(
        name="Legacy Geometry Noise Mode",
        description="Report older v0.1-style rotation/intersection/walkability noise as findings. Usually leave off.",
        default=False
    )
    max_primary_findings: bpy.props.IntProperty(name="Max Primary Findings", default=75, min=5, max=500)
    assembly_min_gap: bpy.props.FloatProperty(name="Assembly Min Gap", default=0.08, min=0.0)
    assembly_max_gap: bpy.props.FloatProperty(name="Assembly Max Gap", default=1.25, min=0.01)
    assembly_high_gap: bpy.props.FloatProperty(name="High Gap Threshold", default=0.35, min=0.01)
    assembly_side_gap: bpy.props.FloatProperty(name="Assembly Side Gap", default=0.18, min=0.0)
    assembly_xy_overlap_ratio: bpy.props.FloatProperty(name="Assembly XY Overlap", default=0.12, min=0.0, max=1.0)
    max_gap_candidates: bpy.props.IntProperty(name="Max Gap Candidates", default=400, min=10, max=5000)
    max_gap_findings: bpy.props.IntProperty(name="Max Gap/Continuity Clusters", default=25, min=1, max=200)
    buried_detail_ratio: bpy.props.FloatProperty(
        name="Buried Detail Ratio",
        description="Estimated bbox containment ratio used to flag mostly-hidden decorative/detail parts",
        default=0.85,
        min=0.50,
        max=1.0
    )
    max_buried_detail_findings: bpy.props.IntProperty(name="Max Buried Detail Findings", default=10, min=0, max=100)
    severe_intersection_ratio: bpy.props.FloatProperty(name="Severe Intersection Ratio", default=0.65, min=0.0, max=1.0)
    max_intersection_findings: bpy.props.IntProperty(name="Max Intersection Findings", default=10, min=0, max=100)
    max_duplicate_findings: bpy.props.IntProperty(name="Max Duplicate Findings", default=20, min=0, max=100)
    max_outlier_findings: bpy.props.IntProperty(name="Max Outlier Findings", default=10, min=0, max=100)




def settings_to_dict(settings):
    """Serialize user-facing triage settings into plain JSON."""
    keys = [
        "package_root", "output_dir", "skip_token", "include_hidden", "capture_screenshots",
        "screenshot_resolution", "scene_floor_z", "floating_gap", "support_xy_overlap_ratio",
        "intersection_volume_threshold", "intersection_ratio_threshold", "intersection_depth",
        "duplicate_center_distance", "outlier_distance", "min_abs_scale", "max_abs_scale",
        "nonuniform_scale_ratio", "flag_odd_rotations", "rotation_step_degrees",
        "rotation_tolerance_degrees", "walkway_planar_gap", "walkway_z_delta",
        "max_pair_checks", "max_walkable_checks", "legacy_geometry_noise_mode",
        "max_primary_findings", "assembly_min_gap", "assembly_max_gap", "assembly_high_gap",
        "assembly_side_gap", "assembly_xy_overlap_ratio", "max_gap_candidates",
        "max_gap_findings", "buried_detail_ratio", "max_buried_detail_findings",
        "severe_intersection_ratio", "max_intersection_findings", "max_duplicate_findings",
        "max_outlier_findings"
    ]
    data = {}
    for k in keys:
        if hasattr(settings, k):
            try:
                v = getattr(settings, k)
                if isinstance(v, Path):
                    v = str(v)
                data[k] = v
            except Exception:
                pass
    return data


def apply_settings_dict(settings, data):
    """Apply safe known settings from JSON clipboard payload."""
    changed = []
    allowed = set(settings_to_dict(settings).keys())
    # Do not allow package/output path changes from AI clipboard unless user explicitly edits UI.
    protected = {"package_root", "output_dir"}
    for k, v in data.items():
        if k not in allowed or k in protected:
            continue
        if not hasattr(settings, k):
            continue
        try:
            setattr(settings, k, v)
            changed.append(k)
        except Exception:
            pass
    return changed


def make_zip_from_folder(folder):
    folder = Path(folder)
    zip_path = folder.with_suffix(".zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in folder.rglob("*"):
            if f.is_file() and f != zip_path:
                z.write(f, arcname=str(f.relative_to(folder)))
    latest = folder.parent / "latest_triage.zip"
    try:
        shutil.copy2(zip_path, latest)
    except Exception:
        pass
    return zip_path


def _issue_object_names(issue):
    names = []
    obj = issue.get("object_name")
    if obj:
        names.append(obj)
    ev = issue.get("evidence") or {}
    for pair in ev.get("example_pairs", []) or []:
        for k in ("object", "other_object"):
            n = pair.get(k)
            if n and n not in names:
                names.append(n)
    for n in ev.get("affected_objects", []) or []:
        if n and n not in names:
            names.append(n)
    return names


def enrich_report_for_human_review(report):
    """Add human-review prompts and exact object lists to issues."""
    for i, issue in enumerate(report.get("issues", []), start=1):
        review_id = f"REVIEW-{i:03d}"
        issue["review_id"] = review_id
        issue["affected_object_names"] = _issue_object_names(issue)
        typ = issue.get("type", "")
        if typ in ("ASSEMBLY_DISCONTINUITY_CANDIDATE", "FLOATING_ORNAMENT_STACK_REVIEW"):
            q = "Does this appear to be an unintended detached/floating assembly, or should the affected objects touch / be flagged !!!!SKIP if intentional?"
        elif typ == "VISUAL_CONTINUITY_REVIEW":
            q = "Does this appear to be an unintended visible gap, pattern break, or unfinished ring/trim continuity?"
        elif typ == "DETAIL_VISIBILITY_REVIEW":
            q = "Is this mostly buried/hidden detail intentional, or should it be exposed, removed, or flagged !!!!SKIP?"
        elif typ == "NEGATIVE_KNOWLEDGE_REVIEW_REQUIRED":
            q = "Does the Project Build Packet document the correct behavior for this part, and was that behavior followed?"
        else:
            q = "Is this finding acceptable, intentional, or does it need repair?"
        issue["human_review_question"] = q
        issue["human_review_options"] = [
            "ACCEPT_AS_OK",
            "FIX_REQUIRED",
            "INTENTIONAL_ADD_SKIP_FLAG",
            "NEEDS_MORE_CONTEXT"
        ]
    return report


def write_issue_selection_scripts(report, out_root):
    """Create simple scripts to select affected Blender objects for each review issue."""
    out_dir = Path(out_root) / "selection_scripts"
    out_dir.mkdir(parents=True, exist_ok=True)
    for issue in report.get("issues", []):
        rid = issue.get("review_id") or issue.get("issue_id") or "REVIEW"
        names = issue.get("affected_object_names") or _issue_object_names(issue)
        script = [
            "import bpy",
            "bpy.ops.object.select_all(action='DESELECT')",
            f"names = {json.dumps(names, indent=2)}",
            "for name in names:",
            "    obj = bpy.data.objects.get(name)",
            "    if obj:",
            "        obj.select_set(True)",
            "        bpy.context.view_layer.objects.active = obj",
            "if bpy.context.view_layer.objects.active:",
            "    try:",
            "        bpy.ops.view3d.view_selected(use_all_regions=False)",
            "    except Exception:",
            "        pass",
            f"print('Selected {rid}:', names)",
        ]
        filename = f"select_{safe_name(rid)}.py"
        write_text(out_dir / filename, "\n".join(script))
        issue.setdefault("evidence", {})["selection_script"] = f"selection_scripts/{filename}"


def render_review_index(report):
    lines = []
    lines.append("# Human Review Index")
    lines.append("")
    lines.append("This is a build feedback triage report, not an audit, CAPA, or compliance failure report.")
    lines.append("")
    lines.append("For each finding, use the affected Blender object names or run the corresponding selection script.")
    lines.append("If the issue is intentional, add `!!!!SKIP` to the affected object name(s) so future triage suppresses normal visual warnings.")
    lines.append("")
    for issue in report.get("issues", []):
        lines.append(f"## {issue.get('review_id', issue.get('issue_id'))} — {issue.get('type')}")
        lines.append("")
        lines.append(f"Severity: {issue.get('severity')}")
        lines.append(f"Summary: {issue.get('summary')}")
        names = issue.get("affected_object_names") or []
        if names:
            lines.append("")
            lines.append("Affected Blender objects:")
            for n in names[:20]:
                lines.append(f"- `{n}`")
            if len(names) > 20:
                lines.append(f"- ... {len(names) - 20} more")
        ev = issue.get("evidence") or {}
        if ev.get("selection_script"):
            lines.append(f"Selection script: `{ev.get('selection_script')}`")
        if ev.get("example_pairs"):
            lines.append("")
            lines.append("Example pairs / locations:")
            for pair in ev.get("example_pairs", [])[:5]:
                lines.append(f"- `{pair.get('object')}` ↔ `{pair.get('other_object')}` gap={pair.get('gap')} centers={pair.get('object_center')} / {pair.get('other_center')}")
        lines.append("")
        lines.append(f"Question: {issue.get('human_review_question')}")
        lines.append("")
        lines.append("Decision: [ ] OK  [ ] Fix  [ ] Intentional/Skip  [ ] Needs context")
        lines.append("")
    return "\n".join(lines)



class NMS_OT_RunBuildTriage(bpy.types.Operator):
    bl_idname = "nms.run_build_feedback_triage"
    bl_label = "Run NMS Build Feedback Triage"
    bl_description = "Generate NMS-aware triage report, screenshots, and AI repair prompt"
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = context.scene.nms_triage_settings
        root = bpy.path.abspath(settings.package_root) if settings.package_root else ""
        out_root = Path(bpy.path.abspath(settings.output_dir)) / f"triage_{now_stamp()}"
        out_root.mkdir(parents=True, exist_ok=True)

        knowledge = NMSKnowledge(root) if root and os.path.isdir(root) else NMSKnowledge("")
        report = run_triage_analysis(context, settings, knowledge)
        report = enrich_report_for_human_review(report)

        screenshot_paths = {}
        if settings.capture_screenshots:
            try:
                screenshot_paths = capture_fixed_angles(context, out_root, settings)
            except Exception as e:
                report.setdefault("warnings", []).append(f"Screenshot capture failed: {e}")

        report["screenshots"] = screenshot_paths
        report["settings_profile"] = settings_to_dict(settings)

        # Create per-issue selection scripts before final JSON so paths are captured in evidence.
        write_issue_selection_scripts(report, out_root)

        json_path = out_root / "BUILD_TRIAGE_REPORT.json"
        md_path = out_root / "BUILD_TRIAGE_REPORT.md"
        prompt_path = out_root / "AI_REPAIR_PROMPT.md"
        review_index_path = out_root / "HUMAN_REVIEW_INDEX.md"
        settings_path = out_root / "TRIAGE_SETTINGS_USED.json"
        readme_path = out_root / "README_TRIAGE.md"

        write_json(json_path, report)
        write_text(md_path, render_markdown_report(report, screenshot_paths))
        write_text(prompt_path, render_ai_repair_prompt(report, screenshot_paths))
        write_text(review_index_path, render_review_index(report))
        write_json(settings_path, settings_to_dict(settings))
        write_text(readme_path, f"""# NMS Build Feedback Triage Bundle

Scene: {report.get('scene')}
Generated: {report.get('generated_at')}
Plugin Version: 0.4.1
Reviewed Objects: {report.get('reviewed_object_count')}
Primary Findings: {len(report.get('issues', []))}

This bundle is for feedback triage only. It is not an audit, CAPA, or compliance-failure report.

Start with:
- HUMAN_REVIEW_INDEX.md
- BUILD_TRIAGE_REPORT.md
- AI_REPAIR_PROMPT.md
""")

        zip_path = make_zip_from_folder(out_root)
        report["output_zip"] = str(zip_path)
        # Rewrite JSON with output_zip included, then refresh zip once.
        write_json(json_path, report)
        zip_path = make_zip_from_folder(out_root)

        self.report({"INFO"}, f"NMS triage complete: {len(report['issues'])} issues. ZIP: {zip_path}")
        return {"FINISHED"}



class NMS_OT_ImportTriageSettingsFromClipboard(bpy.types.Operator):
    bl_idname = "nms.import_triage_settings_clipboard"
    bl_label = "Import Settings From Clipboard"
    bl_description = "Import triage settings JSON from the system clipboard"
    bl_options = {"REGISTER"}

    def execute(self, context):
        s = context.scene.nms_triage_settings
        raw = bpy.context.window_manager.clipboard or ""
        try:
            data = json.loads(raw)
            if "triage_settings" in data and isinstance(data["triage_settings"], dict):
                data = data["triage_settings"]
            if not isinstance(data, dict):
                raise ValueError("Clipboard JSON must be an object")
        except Exception as e:
            self.report({"ERROR"}, f"Clipboard does not contain valid triage settings JSON: {e}")
            return {"CANCELLED"}
        changed = apply_settings_dict(s, data)
        self.report({"INFO"}, f"Imported {len(changed)} triage setting(s): {', '.join(changed[:8])}")
        return {"FINISHED"}


class NMS_OT_ExportTriageSettingsToClipboard(bpy.types.Operator):
    bl_idname = "nms.export_triage_settings_clipboard"
    bl_label = "Export Settings To Clipboard"
    bl_description = "Copy current triage settings JSON to the system clipboard"
    bl_options = {"REGISTER"}

    def execute(self, context):
        s = context.scene.nms_triage_settings
        payload = {
            "profile_name": "CURRENT_BLENDER_TRIAGE_SETTINGS",
            "triage_settings": settings_to_dict(s)
        }
        bpy.context.window_manager.clipboard = json.dumps(payload, indent=2)
        self.report({"INFO"}, "Current triage settings copied to clipboard")
        return {"FINISHED"}


class NMS_PT_BuildFeedbackTriagePanel(bpy.types.Panel):
    bl_label = "NMS Build Feedback Triage"
    bl_idname = "NMS_PT_build_feedback_triage"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "NMS Triage"

    def draw(self, context):
        layout = self.layout
        s = context.scene.nms_triage_settings

        layout.label(text="Package / Output")
        layout.prop(s, "package_root")
        layout.prop(s, "output_dir")
        layout.prop(s, "skip_token")
        row = layout.row(align=True)
        row.operator("nms.import_triage_settings_clipboard", icon="IMPORT")
        row.operator("nms.export_triage_settings_clipboard", icon="EXPORT")
        layout.prop(s, "include_hidden")
        layout.prop(s, "capture_screenshots")
        if s.capture_screenshots:
            layout.prop(s, "screenshot_resolution")

        layout.separator()
        layout.label(text="Core Checks")
        layout.prop(s, "scene_floor_z")
        layout.prop(s, "duplicate_center_distance")
        layout.prop(s, "outlier_distance")
        layout.prop(s, "legacy_geometry_noise_mode")

        layout.separator()
        layout.label(text="Assembly-First Checks")
        layout.prop(s, "assembly_min_gap")
        layout.prop(s, "assembly_max_gap")
        layout.prop(s, "assembly_side_gap")
        layout.prop(s, "assembly_xy_overlap_ratio")
        layout.prop(s, "max_gap_findings")
        layout.prop(s, "buried_detail_ratio")
        layout.prop(s, "max_buried_detail_findings")
        layout.prop(s, "max_primary_findings")

        layout.separator()
        layout.label(text="Transform Checks")
        layout.prop(s, "max_abs_scale")
        layout.prop(s, "nonuniform_scale_ratio")
        layout.prop(s, "flag_odd_rotations")
        if s.flag_odd_rotations:
            layout.prop(s, "rotation_step_degrees")
            layout.prop(s, "rotation_tolerance_degrees")

        layout.separator()
        layout.operator("nms.run_build_feedback_triage", icon="VIEW_CAMERA")


classes = (
    NMS_Triage_Settings,
    NMS_OT_RunBuildTriage,
    NMS_OT_ImportTriageSettingsFromClipboard,
    NMS_OT_ExportTriageSettingsToClipboard,
    NMS_PT_BuildFeedbackTriagePanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.nms_triage_settings = bpy.props.PointerProperty(type=NMS_Triage_Settings)


def unregister():
    if hasattr(bpy.types.Scene, "nms_triage_settings"):
        del bpy.types.Scene.nms_triage_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
