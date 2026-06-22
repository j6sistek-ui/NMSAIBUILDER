#!/usr/bin/env python3
"""blender_runtime_script_check.py — static check for real Blender/NMS Builder placement path."""
import ast, re, sys

def check_source(src):
    fails = []
    if "import bpy" not in src and "from bpy" not in src:
        fails.append("missing bpy import")
    if "no_mans_sky_base_builder import BUILDER" not in src:
        fails.append("missing BUILDER import")
    if "BUILDER.add_part" not in src:
        fails.append("missing BUILDER.add_part runtime placement")
    if ".objects.link" not in src:
        fails.append("missing object collection link path")
    if 'globals().get("BUILDER")' in src or "globals().get('BUILDER')" in src:
        fails.append("preview-only globals BUILDER fallback detected")
    if "preview.json" in src and "BUILDER.add_part" not in src:
        fails.append("preview JSON fallback without runtime placement")
    return fails

def main():
    if len(sys.argv) < 2:
        print("usage: blender_runtime_script_check.py <script.py>")
        return 2
    src = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
    try:
        ast.parse(src)
    except Exception as e:
        print("BLENDER RUNTIME SCRIPT CHECK: FAIL")
        print("  FAIL: python parse failed:", e)
        return 1
    fails = check_source(src)
    print("BLENDER RUNTIME SCRIPT CHECK")
    if fails:
        for f in fails: print("  FAIL:", f)
        print("BLENDER RUNTIME SCRIPT CHECK: FAIL")
        return 1
    print("  real Blender/NMS Builder runtime path present")
    print("BLENDER RUNTIME SCRIPT CHECK: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
