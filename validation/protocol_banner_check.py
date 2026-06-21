#!/usr/bin/env python3
"""protocol_banner_check.py — machine-check final NMS protocol banner fields."""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def current_version(root=ROOT):
    try:
        return json.load(open(os.path.join(root, "release", "VERSION.json"), encoding="utf-8")).get("current_version")
    except Exception:
        return None

REQUIRED = ["type:", "source docs rev:", "bundle:", "gate:", "ambiguity:", "Docs Avail for Update?:"]

def check_text(text, expected_version=None):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    banner = next((ln for ln in reversed(lines) if ln.startswith("PROTOCOL ✓")), "")
    fails = []
    if not banner:
        return ["missing final PROTOCOL ✓ banner"], ""
    for token in REQUIRED:
        if token not in banner:
            fails.append(f"banner missing field: {token}")
    if expected_version and f"source docs rev: {expected_version}" not in banner:
        fails.append(f"banner source docs rev does not match {expected_version}")
    if not re.search(r"Docs Avail for Update\?: (Yes|No) \(\d+\)", banner):
        fails.append("Docs Avail field must be exactly Yes/No with count")
    if "bundle:" not in banner:
        fails.append("bundle receipt missing")
    return fails, banner

def main():
    if len(sys.argv) < 2:
        print("usage: protocol_banner_check.py <text_file> [expected_version]")
        return 2
    path = sys.argv[1]
    ver = sys.argv[2] if len(sys.argv) > 2 else current_version()
    text = open(path, encoding="utf-8", errors="ignore").read()
    fails, banner = check_text(text, ver)
    print("PROTOCOL BANNER CHECK")
    if banner:
        print("  banner:", banner)
    if fails:
        for f in fails:
            print("  FAIL:", f)
        print("PROTOCOL BANNER CHECK: FAIL")
        return 1
    print("  all checks passed")
    print("PROTOCOL BANNER CHECK: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
