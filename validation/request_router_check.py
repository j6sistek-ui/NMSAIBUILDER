#!/usr/bin/env python3
"""Validate REQUEST_ROUTER_CHECKLIST.json and its referenced live files.

This is a docs-level gate. It prevents the router from becoming another passive
rule that references missing files or lacks enforceable request bundles.
"""
import json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
router_path = ROOT / "rules" / "REQUEST_ROUTER_CHECKLIST.json"
required_request_types = {
    "build_generation",
    "build_specific_addition",
    "build_refinement_or_optimization",
    "json_to_python_recreation",
    "python_generated_json_audit",
    "high_quality_source_json_recipe_mining",
    "screenshot_or_ingame_evaluation",
    "reference_image_or_external_example",
    "source_doc_review_or_patch",
    "protocol_correction_or_failure",
    "script_debugging_or_error_log",
}

def fail(msg):
    print("FAIL:", msg)
    return 1

def main():
    if not router_path.exists():
        return fail("rules/REQUEST_ROUTER_CHECKLIST.json missing")
    try:
        data = json.loads(router_path.read_text(encoding="utf-8"))
    except Exception as e:
        return fail(f"bad router JSON: {e}")
    errors = []
    if data.get("status") != "mandatory_first_gate":
        errors.append("router status must be mandatory_first_gate")
    always = data.get("always_required", [])
    for rel in always:
        if not (ROOT / rel).exists():
            errors.append(f"missing always_required file: {rel}")
    rtypes = data.get("request_types", {})
    missing_types = sorted(required_request_types - set(rtypes))
    if missing_types:
        errors.append("missing request types: " + ", ".join(missing_types))
    # --- 2.01.00 additions: critical bundles, ambiguity handling, new-type process, banner ---
    for name, block in rtypes.items():
        crit = block.get("critical")
        if not crit:
            errors.append(f"{name}: critical bundle list missing/empty")
            continue
        mc = set(block.get("must_check", []))
        for c in crit:
            if c not in mc:
                errors.append(f"{name}: critical entry not in must_check: {c}")
            if not (ROOT / c).exists():
                errors.append(f"{name}: critical file missing: {c}")
    amb = data.get("ambiguous_or_unclear", {})
    if "seek" not in str(amb.get("action", "")).lower():
        errors.append("ambiguous_or_unclear.action must seek user input")
    if not data.get("adding_new_request_type"):
        errors.append("adding_new_request_type process missing")
    prc = data.get("per_response_confirmation", {})
    for key in ("rule", "template"):
        ref = prc.get(key)
        if not ref or not (ROOT / ref).exists():
            errors.append(f"per_response_confirmation.{key} missing or file absent: {ref}")
    for name, block in rtypes.items():
        if not block.get("must_check"):
            errors.append(f"{name}: must_check is empty")
        for rel in block.get("must_check", []):
            if not (ROOT / rel).exists():
                errors.append(f"{name}: referenced file missing: {rel}")
    if errors:
        for e in errors:
            print("FAIL:", e)
        print(f"REQUEST ROUTER CHECK: FAIL ({len(errors)} issue(s))")
        return 2
    print("REQUEST ROUTER CHECK: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
