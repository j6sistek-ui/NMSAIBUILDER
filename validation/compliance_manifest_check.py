#!/usr/bin/env python3
"""
compliance_manifest_check.py  (v5.01.00)

Executable verifier for a BUILD COMPLIANCE MANIFEST. As of 5.02.00 this is an OPTIONAL
DEEPER tool: the run_gate requirement is the generated builder sheet (build_sheet_check.py).
Receipts, not attestation.
When a package root is given, it RE-READS the cited sources and verifies:
  - required fields present; one resolution per ObjectID; tier 1..7
  - cited source_file exists
  - source_ref value actually appears inside the cited file
  - the ObjectID actually appears inside the cited file
  - the claimed tier is backed by data and is the highest applicable
       (snap=2 beats partmap=4; negative-knowledge=6 overrides; recipe tiers 1/3
        require the ref to verify in a recipe index)
  - the method is authorized for that part/context (METHOD_AUTHORITY_TABLE)
  - DO_NOT_USE parts are not used without an EXCLUDE/justified method
  - compliance_statement affirms no deviation
Usage:
  compliance_manifest_check.py <manifest.json> [package_root]
  compliance_manifest_check.py --self-test
"""
import json,os,sys
REQUIRED=["build_name","build_surface","object_ids","precedence_resolutions","sources_checked","compliance_statement"]
RECIPE_FILES=["toolkit/PLACEMENT_RECIPE_LIBRARY.json","data/FEATURE_RECIPE_ROUTE_INDEX.json","data/JSON_RECIPE_SIGNATURE_INDEX.json"]
def _norm(o): return (o or "").lstrip("^")
def _read(root,rel):
    try: return open(os.path.join(root,rel),encoding="utf-8",errors="ignore").read()
    except Exception: return None
def _json(root,rel,d=None):
    try: return json.load(open(os.path.join(root,rel),encoding="utf-8"))
    except Exception: return d
def _snap_set(root):
    rel=_json(root,"library/authoritative_snap/relational_map_combined_v01.json",{}) or {}
    s=set(rel.get("part_to_groups",{}).keys())
    for g,info in rel.get("groups",{}).items():
        for p in info.get("parts",[]):
            if isinstance(p,str): s.add(p)
    return {x.lstrip("^") for x in s}
def _data_tiers(oid,snap,pm,neg,methods,ov):
    t=set()
    if oid in neg: t.add(6)
    if oid in snap: t.add(2)
    if oid in pm: t.add(4)
    if oid in methods.get("object_contexts",{}) or (ov and oid in ov): t.add(5)
    if not t: t.add(7)
    return t

def verify(manifest,root=None):
    f=[]
    for k in REQUIRED:
        if k not in manifest: f.append(f"missing required field: {k}")
    if f: return f
    if manifest["build_surface"] not in ("python","blender"): f.append("build_surface must be python|blender")
    oids=manifest["object_ids"]
    if not isinstance(oids,list) or not oids: f.append("object_ids empty"); return f
    by={}
    for r in manifest["precedence_resolutions"]:
        for need in ("objectid","governing_tier","source_file","source_ref","method"):
            if need not in r: f.append(f"resolution missing {need}: {r.get('objectid','?')}")
        by.setdefault(_norm(r.get("objectid")),[]).append(r)
        t=r.get("governing_tier")
        if not (isinstance(t,int) and 1<=t<=7): f.append(f"governing_tier out of range for {r.get('objectid')}: {t}")
    for oid in oids:
        n=_norm(oid)
        if n not in by: f.append(f"no precedence resolution for ObjectID: {oid}")
        elif len(by[n])>1: f.append(f"multiple resolutions for ObjectID: {oid}")
    if root is None: return f  # shallow mode

    snap=_snap_set(root)
    pm={r["ObjectID"].strip("^"):r for r in (_json(root,"library/nms_master_part_map_verified_data_v3_01_02.json",[]) or [])}
    neg=(_json(root,"data/NEGATIVE_KNOWLEDGE_INDEX.json",{}) or {}).get("entries",{})
    methods=_json(root,"data/METHOD_AUTHORITY_TABLE.json",{}) or {}
    mdefs=set(methods.get("method_definitions",{})); octx=methods.get("object_contexts",{})
    ov=_read(root,"rules/PART_ORIENTATION_OVERRIDES.md") or ""
    for r in manifest["precedence_resolutions"]:
        oid=_norm(r.get("objectid")); sf=r.get("source_file",""); ref=r.get("source_ref","") or ""
        tier=r.get("governing_tier"); method=r.get("method","")
        content=_read(root,sf)
        if content is None: f.append(f"cited source_file does not exist/readable: {sf} (for {oid})"); 
        else:
            refval=ref.split(":")[-1].strip()
            if refval and refval not in content: f.append(f"source_ref '{ref}' not found inside {sf} (for {oid})")
            if oid and oid not in content: f.append(f"ObjectID {oid} not found inside cited {sf}")
        # tier highest-applicable
        dt=_data_tiers(oid,snap,pm,neg,methods,ov)
        if tier in (1,3):
            if not any((ref.split(':')[-1].strip() in (_read(root,rf) or "")) for rf in RECIPE_FILES):
                f.append(f"{oid} claims recipe tier {tier} but source_ref does not verify in any recipe index")
        else:
            if tier not in dt and tier!=7: f.append(f"{oid} claims tier {tier} with no data backing (backed tiers {sorted(dt)})")
            if 2 in dt and tier not in (1,2,3) and 6 not in dt: f.append(f"{oid} has snap data (tier 2) but claims weaker tier {tier}")
            if 6 in dt and tier not in (1,6): f.append(f"{oid} is on negative knowledge (tier 6 overrides) but claims tier {tier}")
        # method authorization
        if method not in mdefs: f.append(f"method '{method}' for {oid} is not a defined method in METHOD_AUTHORITY_TABLE")
        elif oid in octx:
            allowed={m for c in octx[oid].get("contexts",{}).values() for m in c.get("allowed_methods",[])}
            if method not in allowed: f.append(f"method '{method}' not authorized for {oid} (allowed: {sorted(allowed)})")
    # negative knowledge DO_NOT_USE
    for oid in oids:
        e=neg.get(_norm(oid))
        if e and e.get("status")=="DO_NOT_USE":
            m=" ".join(str(by.get(_norm(oid),[{}])[0].get("method","")).upper().split())
            if "EXCLUDE" not in m and "JUSTIFIED" not in m: f.append(f"{oid} is DO_NOT_USE but used without EXCLUDE/justified method")
    stmt=str(manifest.get("compliance_statement","")).upper()
    if not stmt.strip(): f.append("compliance_statement empty")
    elif not any(tok in stmt for tok in ("FOLLOWED","NO DEVIATION","NO-DEVIATION")): f.append("compliance_statement does not affirm FOLLOWED / no deviation")
    return f

def _run(m,root=None):
    fails=verify(m,root)
    for x in fails: print("  FAIL:",x)
    print("COMPLIANCE MANIFEST CHECK:","FAIL" if fails else "PASS"); return 1 if fails else 0

def _self_test():
    # shallow
    good={"build_name":"t","build_surface":"blender","object_ids":["^S_WALL_H"],
      "precedence_resolutions":[{"objectid":"^S_WALL_H","governing_tier":2,"source_file":"x","source_ref":"snap:HALF_WALLS","method":"WALL_SHELL_GRID_COURSE"}],
      "sources_checked":["data/PLACEMENT_PRECEDENCE.json"],"compliance_statement":"documents FOLLOWED, no deviation"}
    bad={"build_name":"t","build_surface":"blender","object_ids":["^A","^B"],
      "precedence_resolutions":[{"objectid":"^A","governing_tier":2,"source_file":"x","source_ref":"y","method":"m"}],
      "sources_checked":[],"compliance_statement":"looks fine"}
    assert not verify(good,None) and verify(bad,None), "shallow self-test failed"
    # deep (rooted): use a real snap part and a real partmap part
    root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    snap=sorted(_snap_set(root)); 
    if snap:
        s=snap[0]; rel="library/authoritative_snap/relational_map_combined_v01.json"
        mdefs=sorted((_json(root,"data/METHOD_AUTHORITY_TABLE.json",{}) or {}).get("method_definitions",{}))
        meth=mdefs[0] if mdefs else "FLOOR_GRID_STANDARD"
        dgood={"build_name":"t","build_surface":"blender","object_ids":["^"+s],
          "precedence_resolutions":[{"objectid":"^"+s,"governing_tier":2,"source_file":rel,"source_ref":"snap:"+s,"method":meth}],
          "sources_checked":[rel],"compliance_statement":"FOLLOWED no deviation"}
        dbad={"build_name":"t","build_surface":"blender","object_ids":["^"+s],
          "precedence_resolutions":[{"objectid":"^"+s,"governing_tier":4,"source_file":rel,"source_ref":"snap:"+s,"method":meth}],
          "sources_checked":[rel],"compliance_statement":"FOLLOWED no deviation"}
        gf=verify(dgood,root); bf=verify(dbad,root)
        assert not gf, ("deep good should pass",gf)
        assert any("snap data" in x for x in bf), ("deep bad (tier-4 over snap) should fail",bf)
    print("COMPLIANCE MANIFEST CHECK SELF-TEST: PASS"); return 0

if __name__=="__main__":
    if len(sys.argv)>=2 and sys.argv[1]=="--self-test": sys.exit(_self_test())
    if len(sys.argv)<2: print("usage: compliance_manifest_check.py <manifest.json> [package_root]"); sys.exit(2)
    m=json.load(open(sys.argv[1])); root=sys.argv[2] if len(sys.argv)>2 else None
    sys.exit(_run(m,root))
