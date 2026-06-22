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
def _dims(root):
    # Dimensions library carries the curated, hand-authored guidance (SpacingRule,
    # PlacementGuidance, LikelyRole, ring formulas, known issues, lessons). The
    # verified partmap does not. Loaded so the packet can forward this as advisory.
    d=_load(root,"library/nms_part_dimensions_and_rules_updated.json",[]) or []
    return {x["ObjectID"].lstrip("^"):x for x in d if isinstance(x,dict) and x.get("ObjectID")}

def _snap_set(root):
    rel=_load(root,"library/authoritative_snap/relational_map_combined_v01.json",{}) or {}
    s=set(rel.get("part_to_groups",{}).keys())
    for g,info in rel.get("groups",{}).items():
        for p in info.get("parts",[]):
            if isinstance(p,str): s.add(p)
    return {x.lstrip("^") for x in s}

def _snap_geom(root):
    # Returns (part_to_groups, groups) from the authoritative snap map so callers can
    # derive concrete center-to-center snap steps per part.
    rel=_load(root,"library/authoritative_snap/relational_map_combined_v01.json",{}) or {}
    return rel.get("part_to_groups",{}), rel.get("groups",{})

def _part_snap_spacing(oid, p2g, groups):
    # Concrete face-to-face snap step from the authoritative map. Uses only the cardinal
    # opposing faces (EAST/WEST -> X, NORTH/SOUTH -> Z, TOP/BOTTOM -> vertical Y) so the
    # number is the true tiling step, not inflated by IN/OUT/UP/DOWN auxiliary points.
    def _tx(pt,i):
        mat=pt.get("matrix")
        try: return float(mat[i][3])
        except Exception: return None
    for gname in p2g.get(oid, []):
        g=groups.get(gname) or {}
        sp=g.get("snap_points") or {}
        if not sp: continue
        def pick(name):
            for k,v in sp.items():
                if k.upper()==name: return v
            return None
        def step(a,b,axis):
            pa,pb=pick(a),pick(b)
            if pa is None or pb is None: return None
            va,vb=_tx(pa,axis),_tx(pb,axis)
            if va is None or vb is None: return None
            return round(abs(va-vb),4)
        out={}
        sx=step("EAST","WEST",0); sz=step("NORTH","SOUTH",2); sy=step("TOP","BOTTOM",1)
        if sx: out["lateral_step_x"]=sx
        if sz: out["lateral_step_z"]=sz
        if sy: out["vertical_step_y"]=sy
        if out:
            out["group"]=gname
            out["derived_from"]="authoritative snap cardinal faces (relational_map_combined_v01.json); center-to-center for face-to-face snapping"
            return out
    return None

def _placement_spec(drow, snap_ss, has_override, recipe_cands, forbidden):
    # The build sheet's complete per-part hand-off, assembled from the library: orientation,
    # scaling, placement (incl. concrete snap), role, cautions. Everything the build needs
    # about this part, mapped, in one place — not re-derived and not scattered.
    def g(*keys):
        for k in keys:
            v=drow.get(k)
            if v not in (None,"",[],{}): return v
        return None
    def prune(d): return {k:v for k,v in d.items() if v not in (None,"",[],{})}
    orientation=prune({
        "default_rotation_degrees": g("VerifiedDefaultRotationDegrees","DefaultRotationDegrees"),
        "footprint_rx90": drow.get("VerifiedRX90WorldSize"),
        "footprint_ry90": drow.get("VerifiedRY90WorldSize"),
        "footprint_rz90": drow.get("VerifiedRZ90WorldSize"),
        "ring_orientation_guidance": g("RingOrientationGuidance"),
        "override_source": "rules/PART_ORIENTATION_OVERRIDES.md" if has_override else None,
    })
    orientation["override_registered"]=bool(has_override)
    orientation["rule"]="RX=90 default unless override_registered is true; only RZ changes facing"
    scaling=prune({
        "world_size_scale_0_5": drow.get("VerifiedScale050WorldSize"),
        "world_size_scale_1_0": g("VerifiedMeasuredWorldSizeDefault","MeasuredWorldSize_DEFAULT"),
        "world_size_scale_1_5": drow.get("VerifiedScale150WorldSize"),
        "world_size_scale_2_0": drow.get("VerifiedScale200WorldSize"),
    })
    if scaling: scaling["rule"]="world size scales linearly; free-placed step = world_size * scale * 0.92 (snap steps are at scale 1.0)"
    placement=prune({
        "snap_spacing": snap_ss,
        "spacing_rule_fallback": g("SpacingRule"),
        "placement_guidance": g("ManualPlacementGuidance","PlacementGuidance"),
        "ring_placement_formula": g("RingPlacementFormula"),
        "ring_spacing_target": g("RingSpacingTarget"),
        "recipe_candidates": recipe_cands or None,
    })
    if snap_ss and placement.get("spacing_rule_fallback"):
        placement["authority_note"]="snap_spacing is the connection authority and supersedes spacing_rule_fallback (full extent, over-spaces snap joins); fallback is for free-placed parts only"
    role=prune({
        "likely_role": g("LikelyRole"),
        "validated_role": g("ValidatedRole","ManualCreativeRole"),
        "mechanics_use": g("MechanicsUseRecommendation","VerifiedMechanicsUseRecommendation"),
        "known_good_uses": g("KnownGoodUses"),
    })
    cautions=prune({
        "known_issues": g("KnownIssues","KnownIssue","ManualKnownFailure"),
        "lesson_notes": g("LessonNotes"),
        "decorative_proxy_caution": g("DecorativeProxyCaution"),
        "validation_flags": g("ValidationFlags","VerifiedFlags"),
        "forbidden": forbidden,
    })
    spec={"orientation":orientation}
    if scaling: spec["scaling"]=scaling
    if placement: spec["placement"]=placement
    if role: spec["role"]=role
    if cautions: spec["cautions"]=cautions
    return spec

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

def _pkg_rev():
    import os,json as _j
    try:
        _vp=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"release","VERSION.json")
        return _j.load(open(_vp)).get("current_version","unknown")
    except Exception:
        return "unknown"

# ---- advisory (creative) loaders ----
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
    snap=_snap_set(root); pm=_partmap(root); dims=_dims(root)
    snap_p2g, snap_groups=_snap_geom(root)
    neg=(_load(root,"data/NEGATIVE_KNOWLEDGE_INDEX.json",{}) or {}).get("entries",{})
    methods=_load(root,"data/METHOD_AUTHORITY_TABLE.json",{}) or {}
    rpam=(_load(root,"data/RULE_PART_APPLICABILITY_MAP.json",{}) or {}).get("rules",[])
    runtime_beh=(_load(root,"data/RUNTIME_BEHAVIORS.json",{}) or {}).get("behaviors",{})
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
        # 5.18.00 — assemble the COMPLETE per-part spec the build sheet was always meant to
        # hand over: orientation + scaling + placement(+snap) + role + cautions, mapped from
        # the library. Replaces the piecemeal curated-guidance/snap dicts.
        drow=dims.get(oid,{})
        snap_ss=_part_snap_spacing(oid, snap_p2g, snap_groups) if oid in snap else None
        recipe_cands=_recipe_candidates(root,oid)
        has_override=("`"+oid+"`" in overrides_txt) or ("ObjectID "+oid in overrides_txt)
        placement_spec=_placement_spec(drow, snap_ss, has_override, recipe_cands, neg.get(oid))
        tiers=data_tiers(oid,snap,pm,neg,methods,overrides_txt)
        ctx=methods.get("object_contexts",{}).get(oid,{})
        allowed=sorted({m for c in ctx.get("contexts",{}).values() for m in c.get("allowed_methods",[])})
        oid_l=oid.lower(); behaviors=[]; seen=set()
        for r in rpam:
            rid=r["rule_id"]
            # Wave 3 Fix 2 — only directly-applicable KEEP RULE/RECIPE/NEGATIVE reach part context
            if r.get("kind") not in ("RULE","RECIPE","NEGATIVE"): continue
            if r.get("runtime_status")!="KEEP": continue
            if r.get("assembly_scope"): continue  # Wave 3.1 — assembly recipes are build-level (intent-matched), not per-part
            if r["scope"]=="PART_SPECIFIC" and oid in r.get("object_ids",[]): applies=f"part {oid}"
            elif r["scope"]=="FAMILY_OR_ASSEMBLY" and any(f in oid_l for f in r.get("families",[])): applies="family/assembly context"
            else: continue
            if rid in seen: continue
            seen.add(rid)
            beh=runtime_beh.get(rid,{})
            # Wave 3 Fix 1 — emit the required behavior, not just the rule name
            behaviors.append({"rule_id":rid,"kind":r.get("kind"),
                              "authority":beh.get("authority","active"),
                              "required_behavior":beh.get("required_behavior",""),
                              "check":beh.get("check",""),
                              "applies_to":applies})
        behaviors.sort(key=lambda b:b["rule_id"])
        parts[oid]={"governing_precedence_tier":governing_tier(tiers),"data_backed_tiers":sorted(tiers),
                    "snap":snap_nature,"geometry":geo,"allowed_methods":allowed,
                    "forbidden":neg.get(oid),"recipe_candidates":recipe_cands,
                    "placement_spec":placement_spec,
                    "applicable_rule_behaviors":behaviors,
                    "applicable_part_rules":[b["rule_id"] for b in behaviors],  # compat: derived from behaviors
                    "build_application":""}  # AI fills: what this part does in THIS build (gate checks non-empty)

    # Wave 3.1 — assembly/composition recipes are build-level, matched against the INTENT (not part names)
    intent_l=(intent or "").lower(); assembly_behaviors=[]; aseen=set()
    for r in rpam:
        if not r.get("assembly_scope"): continue
        if r.get("kind") not in ("RULE","RECIPE","NEGATIVE") or r.get("runtime_status")!="KEEP": continue
        rid=r["rule_id"]
        if rid in aseen: continue
        matched=[f for f in r.get("families",[]) if f in intent_l]
        if not matched: continue
        aseen.add(rid); beh=runtime_beh.get(rid,{})
        assembly_behaviors.append({"rule_id":rid,"kind":r.get("kind"),
                                   "authority":beh.get("authority","active"),
                                   "required_behavior":beh.get("required_behavior",""),
                                   "check":beh.get("check",""),
                                   "applies_to":f"build assembly (intent: {', '.join(sorted(matched))})"})
    assembly_behaviors.sort(key=lambda b:b["rule_id"])

    # ---- 5.04.00: populate the offered CREATIVE_CONTEXT from the runtime indices ----
    ci=_creative_index(root); fm=_failure_modes(root)
    char_all=ci.get("part_geometric_character",{})
    part_char={oid:char_all[oid] for oid in parts if oid in char_all}
    applicable_fm=_applicable_failure_modes(fm,list(parts.keys()),intent)

    return {"schema":"PROJECT_BUILD_PLACEMENT_PACKET_1.1","generated_from_rev":_pkg_rev(),"build_intent":intent or "",
        "MANDATORY_PLACEMENT_CONTEXT":{"parts":parts,"universal_process_rules":universal,
            "assembly_rule_behaviors":assembly_behaviors,
            "note":"FORCED. Build only from these parts; cite each in the BUILD COMPLIANCE MANIFEST; verified by compliance_manifest_check.py. assembly_rule_behaviors are build-level recipes triggered by the build intent."},
        "CREATIVE_CONTEXT":{"style_index":"data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json","creative_rules":creative_rules,
            "part_character":part_char,
            "applicable_failure_modes":applicable_fm,
            "placement_recipes":ci.get("placement_recipes",[]),
            "orientation_recipes":ci.get("orientation_recipes",{}),
            "fit_rules":ci.get("fit_rules",[]),
            "note":"OFFERED, not gated. part_character, failure-mode cautions, recipes and fit-rules inform part choice & composition; they can never override precedence/negative-knowledge or fail the gate. Per-part orientation/scaling/placement/snap/role/cautions are hand-delivered in MANDATORY_PLACEMENT_CONTEXT.parts[oid].placement_spec."}}

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
