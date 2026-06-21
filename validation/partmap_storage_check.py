#!/usr/bin/env python3
"""
Validate NMS part placement map storage.

Checks:
- part_placement_map_index.json exists and parses
- part_placement_master_sheet.csv exists and has required columns
- each indexed partmap exists and parses
- storage_receipt paths agree with actual paths where present
"""

from pathlib import Path
import json, csv, sys

ROOT = Path(__file__).resolve().parents[1]
MAP_DIR = ROOT / "library" / "part_placement_maps"
INDEX = MAP_DIR / "part_placement_map_index.json"
SHEET = MAP_DIR / "part_placement_master_sheet.csv"

REQUIRED_SHEET_COLUMNS = {
    "part_id", "part_family", "status", "primary_source", "partmap_path",
    "fbx_path", "baseline_scale", "extent_x", "extent_y", "extent_z",
    "center_x", "center_y", "center_z", "local_x_rule", "local_y_rule",
    "local_z_rule", "neighbor_offset_summary", "fitment_modes",
    "validated_applications", "validation_status", "last_updated"
}

REQUIRED_PARTMAP_FIELDS = {
    "schema", "part_id", "part_family", "status", "source_evidence",
    "fbx_bounds", "canonical_local_frame", "scale_mapping",
    "source_transform_invariants", "neighbor_offset_clusters_local",
    "rotation_delta_clusters", "fitment_modes", "construction_applications",
    "failure_modes", "allowed_variation_slots", "forbidden_substitutions",
    "validation", "storage_receipt"
}

def fail(msg):
    print(f"FAIL: {msg}")
    return 1

def main():
    if not INDEX.exists():
        return fail(f"missing {INDEX.relative_to(ROOT)}")
    if not SHEET.exists():
        return fail(f"missing {SHEET.relative_to(ROOT)}")

    try:
        index = json.loads(INDEX.read_text())
    except Exception as e:
        return fail(f"index JSON parse error: {e}")

    with SHEET.open(newline="") as f:
        reader = csv.DictReader(f)
        cols = set(reader.fieldnames or [])
        missing = REQUIRED_SHEET_COLUMNS - cols
        if missing:
            return fail(f"master sheet missing columns: {sorted(missing)}")
        rows = list(reader)

    row_ids = {r["part_id"] for r in rows}
    parts = index.get("parts", {})
    if not parts:
        return fail("index has no parts")

    for part_id, info in parts.items():
        if part_id not in row_ids:
            return fail(f"{part_id} missing from master sheet")
        rel = info.get("partmap_path")
        if not rel:
            return fail(f"{part_id} missing partmap_path")
        path = ROOT / rel
        if not path.exists():
            return fail(f"{part_id} partmap missing at {rel}")
        try:
            data = json.loads(path.read_text())
        except Exception as e:
            return fail(f"{part_id} partmap parse error: {e}")
        missing = REQUIRED_PARTMAP_FIELDS - set(data.keys())
        if missing:
            return fail(f"{part_id} partmap missing fields: {sorted(missing)}")
        receipt = data.get("storage_receipt", {})
        if receipt.get("partmap_path") and receipt["partmap_path"] != rel:
            return fail(f"{part_id} storage_receipt partmap_path mismatch")
        if data.get("part_id") != part_id:
            return fail(f"{part_id} part_id mismatch inside partmap")

    # --- controlled validation vocabulary enforcement (2.15.00) ---
    CONTROLLED = {"UNKNOWN", "UNTESTED", "SCRIPT_VALIDATED", "BLENDER_USER_CHECK", "BLENDER_SYSTEMATIC", "GAME_VALIDATED"}
    systematic_routine = (ROOT / "rules" / "SYSTEMATIC_VALIDATION_ROUTINE.md").exists()
    def _base(v):
        return str(v or "").split("|")[0].strip().replace("_WITH_EXCEPTIONS", "")
    for part_id, info in index.get("parts", {}).items():
        rel = info.get("partmap_path")
        if not rel:
            continue
        try:
            data = json.loads((ROOT / rel).read_text())
        except Exception:
            continue
        vstat = data.get("validation", {})
        b = _base(vstat.get("status") if isinstance(vstat, dict) else None)
        if b not in CONTROLLED:
            return fail(f"{part_id} validation.status not in controlled ladder: {vstat.get('status') if isinstance(vstat, dict) else vstat}")
        if b == "BLENDER_SYSTEMATIC" and not systematic_routine:
            return fail(f"{part_id} claims BLENDER_SYSTEMATIC but rules/SYSTEMATIC_VALIDATION_ROUTINE.md does not exist (level reserved)")
        if b == "GAME_VALIDATED" and not (isinstance(vstat, dict) and (vstat.get("in_game_evidence") or vstat.get("game_validated_evidence"))):
            return fail(f"{part_id} claims GAME_VALIDATED without an in-game evidence reference")
    for r in rows:
        if _base(r.get("validation_status")) not in CONTROLLED:
            return fail(f"master sheet row {r.get('part_id')} validation_status not in controlled ladder: {r.get('validation_status')}")
    if not (MAP_DIR / "parts_status.csv").exists():
        return fail("parts_status.csv missing (must ship with every release)")

    print("PASS: part placement map storage valid")
    print(f"Checked {len(parts)} indexed partmaps and {len(rows)} master-sheet rows")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
