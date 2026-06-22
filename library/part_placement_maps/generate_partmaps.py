#!/usr/bin/env python3
"""
generate_partmaps.py  (Tier A bounds backfill + orientation-override carry-in)

Single source of truth for the part placement map:
  - per-part *.partmap.json (hand-authored placement studies)   -> preserved as-is
  - rules/PART_ORIENTATION_OVERRIDES.json (per-part exceptions)  -> GENERATED into the map
  - library/nms_part_dimensions_and_rules_updated.json (bounds)  -> source for fbx_bounds

Derived artifacts (never hand-edited): the master sheet, the index, the worklist, and the
GENERATED override partmaps (one per part in the orientation-override registry, e.g. BILLBOARD).

Run with no args to (re)generate. Run with --check to verify on-disk artifacts match the
sources (drift detection); exits non-zero on mismatch.
"""
import json, csv, sys, io, os, glob, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LIB = os.path.join(ROOT, "library", "nms_part_dimensions_and_rules_updated.json")
OVERRIDES = os.path.join(ROOT, "rules", "PART_ORIENTATION_OVERRIDES.json")
MAPDIR = HERE
INDEX = os.path.join(MAPDIR, "part_placement_map_index.json")
SHEET = os.path.join(MAPDIR, "part_placement_master_sheet.csv")
STATUS_CSV = os.path.join(MAPDIR, "parts_status.csv")
CONTROLLED_STATUSES = ["UNKNOWN", "UNTESTED", "SCRIPT_VALIDATED", "BLENDER_USER_CHECK", "BLENDER_SYSTEMATIC", "GAME_VALIDATED"]
def CANON(raw):
    s = str(raw or "").split("|")[0].strip().replace("_WITH_EXCEPTIONS", "")
    M = {"USER_ACCEPTED": "BLENDER_USER_CHECK", "USER_ACCEPTED_GENERAL_PLACEMENT": "BLENDER_USER_CHECK",
         "PLACEMENT_VALIDATED": "BLENDER_USER_CHECK", "BLENDER_VALIDATED": "BLENDER_USER_CHECK",
         "VALIDATED": "BLENDER_USER_CHECK", "validated": "BLENDER_USER_CHECK",
         "BOUNDS_VALIDATED_PLACEMENT_UNMAPPED": "UNTESTED", "UNKNOWN": "UNKNOWN", "UNTESTED": "UNTESTED",
         "SCRIPT_VALIDATED": "SCRIPT_VALIDATED", "BLENDER_USER_CHECK": "BLENDER_USER_CHECK",
         "BLENDER_SYSTEMATIC": "BLENDER_SYSTEMATIC", "GAME_VALIDATED": "GAME_VALIDATED"}
    if s in M:
        return M[s]
    low = s.lower()
    if "game" in low and "valid" in low:
        return "GAME_VALIDATED"
    if "systematic" in low:
        return "BLENDER_SYSTEMATIC"
    if "script" in low and "valid" in low:
        return "SCRIPT_VALIDATED"
    if "blender" in low or "user_accept" in low or "placement_validated" in low:
        return "BLENDER_USER_CHECK"
    return "UNTESTED"
WORKLIST = os.path.join(MAPDIR, "part_placement_worklist.json")

COLUMNS = ["part_id", "part_family", "status", "primary_source", "partmap_path",
           "fbx_path", "baseline_scale", "extent_x", "extent_y", "extent_z",
           "center_x", "center_y", "center_z", "local_x_rule", "local_y_rule",
           "local_z_rule", "neighbor_offset_summary", "fitment_modes",
           "validated_applications", "validation_status", "orientation_override",
           "last_updated",
           "provenance_level", "origin_type", "origin_offset_local",
           "default_orientation_state", "default_orientation_direction", "pivot_center_type",
           "orientation_phase_rule", "phase_a_deg", "phase_b_deg", "scale_behavior",
           "family_equivalence_status", "geometry_capability", "validated_with_algorithm",
           "next_validation_needed"]

GENERIC_RIGHT = "Right = normalize(Up cross At)"
GENERIC_UP = "Up = normalize(source.Up)"
GENERIC_AT = "At = normalize(source.At projected perpendicular to Up)"
TODAY = "2026-06-07"


def _f(x):
    try:
        return float(x)
    except Exception:
        return None


def _family(oid):
    base = re.sub(r"^[A-Z]_", "", oid)
    base = re.sub(r"(_Q|_H1?|_C|_M|_IC|_SPACE)$", "", base)
    return base or oid


def load_library():
    data = json.load(open(LIB, encoding="utf-8"))
    out = {}
    for e in data:
        if not isinstance(e, dict):
            continue
        oid = e.get("ObjectID")
        if oid is None:
            continue
        ex = _f(e.get("extent_x"))
        if ex is None:
            continue
        out[oid] = {
            "extent_x": ex, "extent_y": _f(e.get("extent_y")) or 0.0, "extent_z": _f(e.get("extent_z")) or 0.0,
            "center_x": _f(e.get("center_x")) or 0.0, "center_y": _f(e.get("center_y")) or 0.0,
            "center_z": _f(e.get("center_z")) or 0.0,
            "fbx_path": e.get("FBXPath") or e.get("fbx_path") or e.get("FBX") or "",
        }
    return out


def load_overrides():
    try:
        d = json.load(open(OVERRIDES, encoding="utf-8"))
        return d.get("overrides", {}) if isinstance(d, dict) else {}
    except Exception:
        return {}


def load_handauthored(override_ids):
    """existing per-part partmaps that are NOT generated from the override registry."""
    out = {}
    for p in sorted(glob.glob(os.path.join(MAPDIR, "*.partmap.json"))):
        d = json.load(open(p, encoding="utf-8"))
        oid = d.get("part_id")
        if oid and oid not in override_ids:
            out[oid] = d
    return out


def _override_summary(ov):
    pr = ov.get("placement_rule", {})
    rx = pr.get("default_rx_degrees")
    rz = pr.get("rz_by_side_degrees", {})
    bits = []
    if rx is not None:
        bits.append(f"rx={rx}")
    if pr.get("do_not_inherit_generic_rx90"):
        bits.append("no_generic_rx90")
    if rz:
        bits.append("rz_by_side:" + "/".join(f"{k}{v}" for k, v in rz.items()))
    return "; ".join(bits)


def build_override_partmap(oid, ov, lib):
    lb = lib.get(oid, {})
    nge = ov.get("native_geometry_evidence", {})
    return {
        "schema": "NMS_PART_PLACEMENT_MAP_ORIENTATION_OVERRIDE",
        "part_id": oid,
        "part_family": _family(oid),
        "status": "SEEDED",
        "source_evidence": {
            "generated_from": "rules/PART_ORIENTATION_OVERRIDES.json",
            "nice_name": ov.get("NiceName", ""),
        },
        "fbx_bounds": {
            "extent_x": lb.get("extent_x", nge.get("extent_x")),
            "extent_y": lb.get("extent_y", nge.get("extent_y")),
            "extent_z": lb.get("extent_z", nge.get("extent_z")),
            "center_x": lb.get("center_x", 0.0), "center_y": lb.get("center_y", 0.0),
            "center_z": lb.get("center_z", 0.0), "FBXPath": lb.get("fbx_path", ""),
            "provenance": "OBSERVED_FACT",
        },
        "canonical_local_frame": {"Up": GENERIC_UP, "At": GENERIC_AT, "Right": GENERIC_RIGHT},
        "scale_mapping": {"baseline_scale": "source/control scale"},
        "source_transform_invariants": ["Position", "Up", "At"],
        "neighbor_offset_clusters_local": {"status": "NEED_STUDY", "provenance": "DERIVED_RULE_PENDING"},
        "rotation_delta_clusters": {"status": "VALIDATED_ORIENTATION_OVERRIDE", "provenance": "VALIDATED_RULE",
                                    "rule": ov.get("placement_rule", {})},
        "fitment_modes": ["NEED_STUDY"],
        "construction_applications": [],
        "failure_modes": ["applying the generic rx=90 facade rule misorients this part "
                          "(e.g. a billboard sign protrudes perpendicular like a shelf)"],
        "allowed_variation_slots": ["material substitution"],
        "forbidden_substitutions": ["inheriting the generic rx=90 facade rule"],
        "validation": {"status": "UNTESTED", "_legacy_status": "orientation_override_validated_placement_unmapped",
                       "note": "orientation override is evidence-validated; full placement not yet map-only proven",
                       "validated_with_algorithm": None, "validated_date": None, "validation_build": None,
                       "validation_evidence": {"orientation_override": "PART_ORIENTATION_OVERRIDES evidence chain (FBX->Python->JSON->screenshots)", "placement": "none"}},
        "storage_receipt": {
            "partmap_path": f"library/part_placement_maps/{oid}.partmap.json",
            "index_path": "library/part_placement_maps/part_placement_map_index.json",
            "source": "PART_ORIENTATION_OVERRIDES",
        },
        "orientation_override": {
            "native_geometry_evidence": nge,
            "placement_rule": ov.get("placement_rule", {}),
        },
    }


def row_from_partmap(oid, pm):
    b = pm.get("fbx_bounds", {})
    frame = pm.get("canonical_local_frame", {})
    noc = pm.get("neighbor_offset_clusters_local", {})
    pitch = noc.get("primary_lattice_pitch_median")
    nsum = (f"primary lattice pitch {pitch}; {noc.get('status', 'DISCOVERED')}"
            if pitch is not None else noc.get("status", "NEED_STUDY"))
    apps = [a.get("application") for a in pm.get("construction_applications", [])
            if a.get("status") in ("source_validated", "validated")]
    ov = pm.get("orientation_override")
    profile = pm.get("part_profile", {}) or {}
    phase = (profile.get("orientation_phase_rule", {}) or {})
    origin_offset = profile.get("origin_offset_local", {})
    if isinstance(origin_offset, dict):
        origin_offset_summary = f"[{origin_offset.get('x', '')},{origin_offset.get('y', '')},{origin_offset.get('z', '')}] {origin_offset.get('status', '')}".strip()
    else:
        origin_offset_summary = str(origin_offset)
    validation = pm.get("validation", {}) or {}
    family_eq = pm.get("family_equivalence", {}) or {}
    geom_cap = "; ".join(apps) if apps else "none"
    next_needed = validation.get("next_gate") or "; ".join(pm.get("storage_receipt", {}).get("missing_items", []))
    validated_alg = validation.get("validated_with_algorithm") or ""
    provenance_level = "VALIDATED_RULE" if validation.get("status") in ("validated", "PLACEMENT_VALIDATED") else "OBSERVED_FACT_OR_DERIVED_PENDING"
    return {
        "part_id": oid, "part_family": pm.get("part_family", _family(oid)),
        "status": pm.get("status", "DISCOVERED"),
        "primary_source": (pm.get("source_evidence", {}).get("validated_study_report")
                           or pm.get("source_evidence", {}).get("behavior_signature_source")
                           or pm.get("source_evidence", {}).get("generated_from") or "per_part_partmap"),
        "partmap_path": f"library/part_placement_maps/{oid}.partmap.json",
        "fbx_path": b.get("FBXPath", ""),
        "baseline_scale": pm.get("scale_mapping", {}).get("baseline_scale", "source/control scale"),
        "extent_x": b.get("extent_x", ""), "extent_y": b.get("extent_y", ""), "extent_z": b.get("extent_z", ""),
        "center_x": b.get("center_x", ""), "center_y": b.get("center_y", ""), "center_z": b.get("center_z", ""),
        "local_x_rule": frame.get("Right", GENERIC_RIGHT), "local_y_rule": frame.get("Up", GENERIC_UP),
        "local_z_rule": frame.get("At", GENERIC_AT), "neighbor_offset_summary": nsum,
        "fitment_modes": "; ".join(pm.get("fitment_modes", [])) or "NEED_STUDY",
        "validated_applications": geom_cap,
        "validation_status": CANON(validation.get("status", "DISCOVERED_NOT_VALIDATED")),
        "orientation_override": _override_summary(ov) if ov else (phase.get("rule", "") if phase else ""),
        "last_updated": TODAY,
        "provenance_level": provenance_level,
        "origin_type": profile.get("origin_type", "unknown"),
        "origin_offset_local": origin_offset_summary,
        "default_orientation_state": profile.get("default_orientation_state", "unknown"),
        "default_orientation_direction": profile.get("default_orientation_direction", "unknown"),
        "pivot_center_type": profile.get("center_origin_type", profile.get("bottom_origin_type", "unknown")),
        "orientation_phase_rule": phase.get("rule", ""),
        "phase_a_deg": phase.get("phase_a_deg", ""),
        "phase_b_deg": phase.get("phase_b_deg", ""),
        "scale_behavior": (profile.get("scale_behavior", {}) or {}).get("uniform_scale", "unknown") if isinstance(profile.get("scale_behavior", {}), dict) else str(profile.get("scale_behavior", "")),
        "family_equivalence_status": family_eq.get("equivalence_to_C_TRIFLOOR", profile.get("validated_scope", "single_part_or_unknown")),
        "geometry_capability": geom_cap,
        "validated_with_algorithm": validated_alg,
        "next_validation_needed": next_needed,
    }

def row_from_library(oid, lb):
    return {
        "part_id": oid, "part_family": _family(oid), "status": "SEEDED",
        "primary_source": "dimensions_library_fbx_bounds", "partmap_path": "",
        "fbx_path": lb["fbx_path"], "baseline_scale": "source/control scale",
        "extent_x": lb["extent_x"], "extent_y": lb["extent_y"], "extent_z": lb["extent_z"],
        "center_x": lb["center_x"], "center_y": lb["center_y"], "center_z": lb["center_z"],
        "local_x_rule": GENERIC_RIGHT, "local_y_rule": GENERIC_UP, "local_z_rule": GENERIC_AT,
        "neighbor_offset_summary": "NEED_STUDY", "fitment_modes": "NEED_STUDY",
        "validated_applications": "none", "validation_status": CANON("UNTESTED"),
        "orientation_override": "", "last_updated": TODAY,
    }


def build():
    lib = load_library()
    ov_reg = load_overrides()
    override_ids = set(ov_reg)
    pms = load_handauthored(override_ids)
    gen_override_pms = {oid: build_override_partmap(oid, ov_reg[oid], lib) for oid in sorted(ov_reg)}
    pms.update(gen_override_pms)

    rows = {oid: row_from_library(oid, lb) for oid, lb in lib.items()}
    for oid, pm in pms.items():
        rows[oid] = row_from_partmap(oid, pm)
    ordered = [rows[k] for k in sorted(rows)]

    index = {
        "schema": "NMS_PART_PLACEMENT_MAP_INDEX", "updated": TODAY, "status": "active",
        "storage_protocol": "rules/PART_PLACEMENT_MAP_SCHEMA.md",
        "schema_doc": "rules/PART_PLACEMENT_MAP_SCHEMA.md",
        "mapping_algorithm": "rules/PART_PLACEMENT_MAP_SCHEMA.md", "parts": {},
    }
    for oid in sorted(pms):
        pm = pms[oid]
        index["parts"][oid] = {
            "part_family": pm.get("part_family", _family(oid)),
            "partmap_path": f"library/part_placement_maps/{oid}.partmap.json",
            "status": pm.get("status", "DISCOVERED"),
            "validation_status": pm.get("validation", {}).get("status", "DISCOVERED_NOT_VALIDATED"),
            "source": (pm.get("source_evidence", {}).get("behavior_signature_source")
                       or pm.get("source_evidence", {}).get("generated_from") or "per_part_partmap"),
        }

    validated = [r["part_id"] for r in ordered if r["validation_status"] in ("validated", "PLACEMENT_VALIDATED")]
    bounds_only = [r["part_id"] for r in ordered if r["partmap_path"] == ""]
    open_frontier = [
        {"part_id": r["part_id"], "validation_status": r["validation_status"],
         "orientation_override": bool(r["orientation_override"])}
        for r in ordered if r["partmap_path"] and r["validation_status"] not in ("validated", "PLACEMENT_VALIDATED")
    ]
    worklist = {
        "schema": "NMS_PART_PLACEMENT_WORKLIST", "generated": TODAY,
        "summary": {
            "total_tracked_parts": len(ordered), "bounds_validated": len(ordered),
            "placement_validated": len(validated), "per_part_partmaps": len(pms),
            "orientation_override_parts": sorted(override_ids),
            "bounds_only_awaiting_placement": len(bounds_only),
        },
        "open_frontier": open_frontier,
        "note": "bounds are validated for all tracked parts; placement is unvalidated until a map-only "
                "proof build passes and the user agrees. Orientation overrides (e.g. BILLBOARD) are carried "
                "from PART_ORIENTATION_OVERRIDES and are evidence-validated for orientation only.",
    }
    return ordered, index, worklist, gen_override_pms


def render_sheet(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\r\n")
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def render_status_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["part_id", "part_family", "validation_status"], lineterminator="\r\n", extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({"part_id": r["part_id"], "part_family": r.get("part_family", ""), "validation_status": r.get("validation_status", "")})
    return buf.getvalue()


def main():
    check = "--check" in sys.argv
    rows, index, worklist, gen_pms = build()
    sheet_text = render_sheet(rows)
    status_csv_text = render_status_csv(rows)
    index_text = json.dumps(index, indent=2, ensure_ascii=False)
    worklist_text = json.dumps(worklist, indent=2, ensure_ascii=False)
    gen_files = {os.path.join(MAPDIR, f"{oid}.partmap.json"): json.dumps(pm, indent=2, ensure_ascii=False)
                 for oid, pm in gen_pms.items()}

    if check:
        problems = []
        def cmp(path, text, label):
            try:
                if open(path, encoding="utf-8", newline="").read() != text:
                    problems.append(f"{label} out of sync")
            except FileNotFoundError:
                problems.append(f"{label} missing")
        cmp(SHEET, sheet_text, "master sheet")
        cmp(STATUS_CSV, status_csv_text, "parts status csv")
        cmp(INDEX, index_text, "index")
        cmp(WORKLIST, worklist_text, "worklist")
        for path, text in gen_files.items():
            cmp(path, text, f"generated override partmap {os.path.basename(path)}")
        if problems:
            print("PARTMAP GENERATION DRIFT: " + "; ".join(problems))
            print("  run: python3 library/part_placement_maps/generate_partmaps.py")
            sys.exit(1)
        print(f"PARTMAP GENERATION: in sync ({len(rows)} tracked, {len(gen_files)} override partmap(s), "
              f"{worklist['summary']['placement_validated']} placement-validated)")
        return

    for path, text in gen_files.items():
        open(path, "w", encoding="utf-8").write(text)
    open(SHEET, "w", encoding="utf-8", newline="").write(sheet_text)
    open(STATUS_CSV, "w", encoding="utf-8", newline="").write(status_csv_text)
    open(INDEX, "w", encoding="utf-8").write(index_text)
    open(WORKLIST, "w", encoding="utf-8").write(worklist_text)
    print(f"generated: {len(rows)} sheet rows, {len(index['parts'])} indexed partmaps "
          f"({len(gen_files)} from orientation overrides)")


if __name__ == "__main__":
    main()
