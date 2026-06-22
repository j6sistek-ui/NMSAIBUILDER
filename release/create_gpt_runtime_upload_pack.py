#!/usr/bin/env python3
"""
create_gpt_runtime_upload_pack.py — build a small, derived GPT Knowledge upload pack.

The full source-doc ZIP remains authoritative. This pack is a generated derivative
for custom GPT runtime access. Never edit the generated pack by hand.
"""
import hashlib, json, os, shutil, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "NMS_GPT_RUNTIME_UPLOAD_PACK"
FILES = [
    "00_START_HERE_CURRENT.md",
    "release/VERSION.json",
    "rules/REQUEST_ROUTER_CHECKLIST.md",
    "rules/REQUEST_ROUTER_CHECKLIST.json",
    "rules/PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md",
    "rules/DOCS_UPDATE_AVAILABILITY_PROTOCOL.md",
    "rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md",
    "rules/COMPOSITE_BUILD_INTENT_GRAPH_PROTOCOL.md",
    "rules/RECIPE_CONFORMANCE_PROTOCOL.md",
    "rules/GPT_RUNTIME_UPLOAD_PACK_PROTOCOL.md",
    "validation/run_gate.py",
    "validation/validated_logic_reuse_check.py",
    "validation/recipe_conformance_check.py",
    "validation/intent_graph_conformance_check.py",
    "rules/PROTOCOL_BANNER_HARD_FAIL_RULE.md",
    "rules/VALIDATION_GATE_HARDENING_RULE.md",
    "rules/FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL.md",
    "rules/C_TRIFLOOR_EDGE_CONTACT_GRAPH_PROTOCOL.md",
    "validation/protocol_banner_check.py",
    "validation/blender_runtime_script_check.py",
    "validation/geometry_construction_manifest_check.py",
    "validation/build_objective_conformance_check.py",
    "library/part_placement_maps/part_placement_map_index.json",
    "library/part_placement_maps/part_placement_master_sheet.csv",
    "toolkit/validated_recipes/README.md",
    "toolkit/validated_recipes/stairs.py",
    "toolkit/validated_recipes/c_trifloor.py",
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    version = json.load(open(ROOT / "release" / "VERSION.json", encoding="utf-8")).get("current_version")
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    manifest = {
        "type": "NMS_GPT_RUNTIME_UPLOAD_PACK",
        "source_version": version,
        "authoritative_source": "full NMS master docs ZIP / source tree",
        "manual_editing_allowed": False,
        "regenerate_after_each_release": True,
        "files": []
    }

    for rel in FILES:
        src = ROOT / rel
        if not src.exists():
            raise SystemExit(f"missing required pack file: {rel}")
        dst = OUT_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        manifest["files"].append({"path": rel, "sha256": sha256(src)})

    manifest_path = OUT_DIR / "GPT_RUNTIME_UPLOAD_PACK_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    zip_path = OUT_DIR.with_name(f"NMS_GPT_RUNTIME_UPLOAD_PACK_{version}.zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(OUT_DIR.rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(OUT_DIR).as_posix())
    print(f"GPT runtime pack: {zip_path}")
    print(f"Manifest: {manifest_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
