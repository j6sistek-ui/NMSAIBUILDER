#!/usr/bin/env python3
"""
new_file_guard_check.py — anti-bloat release gate.

The package is at file maturity. New files must not appear on a chat's whim.
This guard FAILS the release if any shipped file is neither (a) listed in
release/APPROVED_FILES.json nor (b) matched by an approved pattern there.

To add a file legitimately: the USER approves it, then it is added to
release/APPROVED_FILES.json (with an approval_log entry). The manifest is NOT
auto-regenerated from the tree — that would defeat the guard. Adding a file is
a deliberate, logged act, not a side effect.

Prints 'NEW FILE GUARD: PASS' or 'NEW FILE GUARD: FAIL (...)'.
"""
import os, sys, json, fnmatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def shipped_files():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        if "__pycache__" in dp.split(os.sep):
            continue
        for f in fn:
            if f.endswith(".pyc"):
                continue
            out.append(os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/"))
    return sorted(out)

def main():
    mpath = os.path.join(ROOT, "release", "APPROVED_FILES.json")
    if not os.path.exists(mpath):
        print("NEW FILE GUARD: FAIL (release/APPROVED_FILES.json missing)")
        return 1
    m = json.load(open(mpath, encoding="utf-8"))
    approved = set(m.get("files", []))
    patterns = m.get("approved_patterns", [])
    ship = shipped_files()
    def ok(p):
        return p in approved or any(fnmatch.fnmatch(p, pat) for pat in patterns)
    unapproved = [p for p in ship if not ok(p)]
    missing = sorted(approved - set(ship))  # approved-but-removed: informational, not a fail
    if missing:
        print(f"  note: {len(missing)} approved file(s) no longer shipped (removal is allowed): "
              + ", ".join(missing[:10]) + (" ..." if len(missing) > 10 else ""))
    if unapproved:
        print(f"NEW FILE GUARD: FAIL ({len(unapproved)} unapproved new file(s) — these require explicit "
              f"user approval; if the user approved them, add to release/APPROVED_FILES.json with an "
              f"approval_log entry, otherwise route the data into an existing store instead of a new file):")
        for p in unapproved:
            print("   UNAPPROVED  " + p)
        return 1
    print(f"NEW FILE GUARD: PASS ({len(ship)} shipped files all approved)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
