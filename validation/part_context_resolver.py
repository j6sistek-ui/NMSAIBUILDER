#!/usr/bin/env python3
"""
part_context_resolver.py  (5.04.00)

Given the ObjectIDs a build intends to use, assemble ONLY their governing data
into a small PROJECT BUILD PLACEMENT PACKET. Operational fix for the 300-file
reachability problem: the AI builds from the packet, not the library.

Mechanical (forced) and creative (offered) are split into separate sections.

5.04.00: CREATIVE_CONTEXT is now POPULATED from the runtime indices so build
findings operate automatically:
  - part_character          : geometric profile per build part (advisory)
  - applicable_failure_modes: geometric-failure cautions matched to this build's
                              parts/intent (data/GEOMETRIC_FAILURE_MODE_INDEX.json)
  - placement_recipes / orientation_recipes / fit_rules (data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json)
These are OFFERED, never gated; MANDATORY_PLACEMENT_CONTEXT is unchanged (mechanical only),
so advisory knowledge can never override precedence/negative-knowledge or fail the gate.

Tier rule: governing precedence tier comes from DATA BACKING -
  6 if on negative knowledge (exception overrides positive data)
  2 if snap-enrolled (relational map)
  4 if verified part map component
  5 if orientation override / placement map / method-authority context
  7 otherwise (manual fallback)
Recipe tiers (1 exact / 3 validated assembly) are CLAIMABLE per-build only against a
verified recipe ref; the resolver lists recipe_candidates as info, it does not auto-claim them.

Usage:
  part_context_resolver.py --ids B_RAMP B_FLOOR_Q PIPE BILLBOARD S_ROOF_M_WIN [--intent "..."] [--out f.json] [--root P]
  part_context_resolver.py --self-test
"""
import json,os,sys,argparse

def _root(p=None): return p or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _load(root,rel,default=None):
    try: return json.load(open(os.path.join(root,rel),encoding="utf-8"))
    except Exception: return default
def _norm(o): return (o or "").lstrip("^")

def _snap_set(root):
    rel=_load(root,"library/authoritative_snap/relational_map_combined_v01.json",{}) or {}
    s=set(rel.get("part_to_groups",{}).keys())
    for g,info in rel.get("groups",{}).items():
        for p in info.get("parts",[]):
            if isinstance(p,str): s.add(p)
    return {x.lstrip("^") for x in s}

def _partmap(root):
    pm=_load(root,"library/nms_master_part_map_verified_data_v3_01_02.json",[]) or []
    return {r["ObjectID"].strip("^"):r for r in pm}

def _recipe_candidates(root,oid):
    hits=[]
    for rel in ("toolkit/PLACEMENT_RECIPE_LIBRARY.json","data/FEATURE_RECIPE_ROUTE_INDEX.json","data/JSON_RECIPE_SIGNATURE_INDEX.json"):
        try:
            if oid in open(os.path.join(root,rel),encoding="utf-8",errors="ignore").read(): hits.append(rel)
        except Exception: pass
    return hits

# ---- 5.04.00 advisory (creative) loaders ----
def _creative_index(root):
    ci=_load(root,"data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json",None)
    if ci is None: ci=_load(root,"data/CREATIVE_USE_CASE_AND_STYLE_INDEX_STUB.json",{}) or {}
    return ci
def _failure_modes(root):
    return (_load(root,"data/GEOMETRIC_FAILURE_MODE_INDEX.json",{}) or {}).get("entries",{})
def _applicable_failure_modes(fm,oids,intent):
    oidset=set(oids); il=(intent or "").lower(); out={}
    for fid,e in fm.items():
        tp=set(e.get("trigger_parts",[])); pats=[p.lower() for p in e.get("trigger_patterns",[])]
        if (tp & oidset) or any(p in il for p in pats):
            out[fid]={"severity":e.get("severity"),"symptom":e.get("symptom"),"fix":e.get("fix")}
    return out

def data_tiers(oid,snap,pm,neg,methods,overrides_txt):
    """Set of precedence tiers BACKED BY DATA for this part (excludes recipe tiers 1/3)."""
    t=set()
    if oid in neg: t.add(6)
    if oid in snap: t.add(2)
    if oid in pm: t.add(4)
    if oid in methods.get("object_contexts",{}) or oid in overrides_txt: t.add(5)
    if not t: t.add(7)
    return t

def governing_tier(tiers):
    # exception (6) overrides positive component data; otherwise highest priority = lowest number
    if 6 in tiers: return 6
    return min(tiers)

def resolve(object_ids,intent,root=None):
    root=_root(root)
    snap=_snap_set(root); pm=_partmap(root)
    neg=(_load(root,"data/NEGATIVE_KNOWLEDGE_INDEX.json",{}) or {}).get("entries",{})
    methods=_load(root,"data/METHOD_AUTHORITY_TABLE.json",{}) or {}
    rpam=(_load(root,"data/RULE_PART_APPLICABILITY_MAP.json",{}) or {}).get("rules",[])
    overrides_txt=""
    try: overrides_txt=open(os.path.join(root,"rules/PART_ORIENTATION_OVERRIDES.md"),encoding="utf-8",errors="ignore").read()
    except Exception: pass
    universal=[r["rule_id"] for r in rpam if r["scope"]=="UNIVERSAL_PROCESS"]
    creative_rules=[r["rule_id"] for r in rpam if r["scope"]=="CREATIVE"]
    parts={}
    for raw in object_ids:
        oid=_norm(raw); row=pm.get(oid,{})
        geo={k:row.get(k) for k in ("MeasuredWorldSize_DEFAULT","WorldBottomOffsetFromOriginZ_DEFAULT",
              "WorldTopOffsetFromOriginZ_DEFAULT","DefaultRotationDegrees")} if row else None
        snap_nature={"nature":"snap","group_label":row.get("SnapGroups")} if oid in snap else {"nature":"free_computed_placement_not_snappable"}
        tiers=data_tiers(oid,snap,pm,neg,methods,overrides_txt)
        ctx=methods.get("object_contexts",{}).get(oid,{})
        allowed=sorted({m for c in ctx.get("contexts",{}).values() for m in c.get("allowed_methods",[])})
        oid_l=oid.lower(); prules=[]
        for r in rpam:
            if r["scope"]=="PART_SPECIFIC" and oid in r.get("object_ids",[]): prules.append(r["rule_id"])
            elif r["scope"]=="FAMILY_OR_ASSEMBLY" and any(f in oid_l for f in r.get("families",[])): prules.append(r["rule_id"])
        parts[oid]={"governing_precedence_tier":governing_tier(tiers),"data_backed_tiers":sorted(tiers),
                    "snap":snap_nature,"geometry":geo,"allowed_methods":allowed,
                    "forbidden":neg.get(oid),"recipe_candidates":_recipe_candidates(root,oid),
                    "applicable_part_rules":sorted(set(prules)),
                    "build_application":""}  # AI fills: what this part does in THIS build (gate checks non-empty)

    # ---- 5.04.00: populate the offered CREATIVE_CONTEXT from the runtime indices ----
    ci=_creative_index(root); fm=_failure_modes(root)
    char_all=ci.get("part_geometric_character",{})
    part_char={oid:char_all[oid] for oid in parts if oid in char_all}
    applicable_fm=_applicable_failure_modes(fm,list(parts.keys()),intent)

    return {"schema":"PROJECT_BUILD_PLACEMENT_PACKET_1.1","generated_from_rev":"5.04.00","build_intent":intent or "",
        "MANDATORY_PLACEMENT_CONTEXT":{"parts":parts,"universal_process_rules":universal,
            "note":"FORCED. Build only from these parts; cite each in the BUILD COMPLIANCE MANIFEST; verified by compliance_manifest_check.py."},
        "CREATIVE_CONTEXT":{"style_index":"data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json","creative_rules":creative_rules,
            "part_character":part_char,
            "applicable_failure_modes":applicable_fm,
            "placement_recipes":ci.get("placement_recipes",[]),
            "orientation_recipes":ci.get("orientation_recipes",{}),
            "fit_rules":ci.get("fit_rules",[]),
            "note":"OFFERED, not gated. part_character, failure-mode cautions, recipes and fit-rules inform part choice & composition; they can never override precedence/negative-knowledge or fail the gate. MANDATORY_PLACEMENT_CONTEXT is the only forced surface."}}

def _self_test():
    pk=resolve(["B_RAMP","B_FLOOR_Q","PIPE"],"stair/ramp corridor")
    p=pk["MANDATORY_PLACEMENT_CONTEXT"]["parts"]
    assert p["PIPE"]["governing_precedence_tier"]==6, p["PIPE"]
    assert p["B_FLOOR_Q"]["governing_precedence_tier"]==4, p["B_FLOOR_Q"]["data_backed_tiers"]
    assert "STAIR_RAMP_ENDPOINT_RECIPE" in p["B_RAMP"]["allowed_methods"]
    snap=_snap_set(_root())
    if snap:
        s=sorted(snap)[0]
        assert resolve([s],"")["MANDATORY_PLACEMENT_CONTEXT"]["parts"][s]["snap"]["nature"]=="snap"
    assert pk["CREATIVE_CONTEXT"]["creative_rules"] is not None
    # 5.04.00 runtime-wiring assertions: findings surface for the parts that triggered them
    rk=resolve(["S_ROOF_M_WIN","S_LARGETRYE0"],"smooth glass cone spire")
    cc=rk["CREATIVE_CONTEXT"]
    assert "S_ROOF_M_WIN" in cc["part_character"] and "S_LARGETRYE0" in cc["part_character"], cc["part_character"]
    fmk=cc["applicable_failure_modes"]
    assert "ROOF_TILE_SHINGLING_NONSMOOTH" in fmk, fmk
    assert "FAN_VAULT_MISUSE_AS_POINT" in fmk, fmk
    assert any(r["id"]=="CONVERGING_RIB_CONE" for r in cc["placement_recipes"]), cc["placement_recipes"]
    assert cc["fit_rules"], "fit_rules empty"
    # firewall: advisory data must NOT leak into the forced mechanical surface
    assert "part_character" not in rk["MANDATORY_PLACEMENT_CONTEXT"]
    print("PART CONTEXT RESOLVER SELF-TEST: PASS"); return 0

if __name__=="__main__":
    if len(sys.argv)>=2 and sys.argv[1]=="--self-test": sys.exit(_self_test())
    ap=argparse.ArgumentParser(); ap.add_argument("--ids",nargs="+",required=True)
    ap.add_argument("--intent",default=""); ap.add_argument("--out",default=None); ap.add_argument("--root",default=None)
    a=ap.parse_args(); pk=resolve(a.ids,a.intent,a.root); s=json.dumps(pk,indent=1)
    (open(a.out,"w").write(s),print("wrote",a.out)) if a.out else print(s)
