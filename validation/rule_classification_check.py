#!/usr/bin/env python3
"""Rule classification completeness gate.
Fails if any RULE_PART_APPLICABILITY_MAP entry lacks kind/runtime_status, if a value
is outside the allowed set, or if RULE_CLASSIFICATION.json and the map disagree on the
set of rule_ids. Enforces RULE_UPDATE_PROTOCOL: a rule cannot silently rot unclassified.
"""
import json, os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KINDS={"RULE","RECIPE","FINDING","PROCESS","GOVERNANCE","REFERENCE","NEGATIVE"}
STATUS={"KEEP","CONSOLIDATE","FOLD","SUPERSEDED","RELOCATE","REPAIR","DEVERSION","RETIRE_TO_FINDING"}
def main():
    fails=[]
    rp=json.load(open(os.path.join(ROOT,"data/RULE_PART_APPLICABILITY_MAP.json")))["rules"]
    led=json.load(open(os.path.join(ROOT,"data/RULE_CLASSIFICATION.json")))["rules"]
    map_ids=set()
    for e in rp:
        rid=e["rule_id"]; map_ids.add(rid)
        if e.get("kind") not in KINDS: fails.append(f"{rid}: kind missing/invalid ({e.get('kind')})")
        if e.get("runtime_status") not in STATUS: fails.append(f"{rid}: runtime_status missing/invalid ({e.get('runtime_status')})")
        if rid not in led: fails.append(f"{rid}: not in RULE_CLASSIFICATION.json ledger")
    for rid in led:
        if rid not in map_ids: fails.append(f"{rid}: in ledger but not in applicability map")
    if fails:
        print("RULE CLASSIFICATION CHECK: FAIL"); [print("  - "+f) for f in fails]; return 1
    print(f"RULE CLASSIFICATION CHECK: PASS ({len(map_ids)} rules, all classified)"); return 0
if __name__=="__main__": sys.exit(main())
