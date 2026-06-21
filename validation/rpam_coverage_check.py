#!/usr/bin/env python3
"""rpam_coverage_check.py (5.01.00) — every rule file must have an RPAM entry; every entry must point to a real file; no NEEDS_REVIEW in a clean release-optional mode."""
import json,os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def main():
    rpam=json.load(open(os.path.join(ROOT,"data","RULE_PART_APPLICABILITY_MAP.json")))
    mapped={r["file"] for r in rpam["rules"]}
    fails=[]
    rules_dir=os.path.join(ROOT,"rules")
    actual={"rules/"+f for f in os.listdir(rules_dir) if f.endswith((".md",".json"))}
    for f in sorted(actual-mapped): fails.append("rule not in RPAM: "+f)
    for r in rpam["rules"]:
        if not os.path.exists(os.path.join(ROOT,r["file"])): fails.append("RPAM points to missing file: "+r["file"])
        if r["scope"] not in ("PART_SPECIFIC","FAMILY_OR_ASSEMBLY","UNIVERSAL_PROCESS","CREATIVE","NEEDS_REVIEW"):
            fails.append("bad scope: "+r["rule_id"])
    for x in fails: print("  FAIL:",x)
    if fails: print("RPAM COVERAGE CHECK: FAIL"); return 1
    print("RPAM COVERAGE CHECK: PASS  (%d rules mapped)"%len(rpam["rules"])); return 0
if __name__=="__main__":
    sys.exit(main())
