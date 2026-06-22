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
def _master_csv(root):
    # The consolidated 'everything in one sheet' attempt: per-part orientation phase, local
    # axis rules, neighbor offsets, fitment, scale behavior, family equivalence, validation
    # status. Many rows are seeded/UNTESTED — surfaced with their validation_status so the
    # build knows which values are trial-confirmed and which are blanks.
    import csv as _csv
    try:
        with open(os.path.join(root,"library/part_placement_maps/part_placement_master_sheet.csv"),
                  encoding="utf-8",errors="ignore",newline="") as fh:
            return {r.get("part_id","").lstrip("^"):r for r in _csv.DictReader(fh) if r.get("part_id")}
    except Exception:
        return {}

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

def _placement_spec(oid, pmrow, drow, csvrow, char, snap_ss, has_override, recipe_cands, forbidden, allowed):
    # The build sheet's COMPLETE per-part record — every placement-relevant fact about this
    # ObjectID, reconciled from all sources into one place, each section tagged with its
    # provenance and validation status. Anchored on the verified part map (the working
    # baseline we don't deviate from); other sources layer on. This is the per-ObjectID
    # extraction the build sheet exists to provide so the AI carries the full spec for only
    # the parts in play, not the whole 2097-row library.
    BAD=(None,"",[],{},"NEED_STUDY","UNTESTED","none","NONE")
    def d(*keys):  # dims-library / generic getter
        for k in keys:
            v=drow.get(k)
            if v not in BAD: return v
        return None
    def p(*keys):  # verified-partmap (anchor) getter
        for k in keys:
            v=pmrow.get(k)
            if v not in BAD: return v
        return None
    def c(*keys):  # master-CSV getter
        for k in keys:
            v=(csvrow.get(k) if csvrow else None)
            if v not in BAD: return v
        return None
    def prune(x): return {k:v for k,v in x.items() if v not in (None,"",[],{})}

    # 1. GEOMETRY — verified part map is the anchor when present. For ObjectIDs absent
    #    from the verified overlay, expose dimensions-library / JSON-only fallback as
    #    provisional so the build sheet stays complete without pretending it is verified.
    geometry_source = "nms_master_part_map_verified_data_v3 (FBX-mined, anchor)" if pmrow else "dimensions_library_or_json_only_fallback (not verified overlay)"
    expected_extent = ([pmrow.get("ExpectedExtentX"),pmrow.get("ExpectedExtentY"),pmrow.get("ExpectedExtentZ")]
        if pmrow.get("ExpectedExtentX") is not None else
        ([drow.get("extent_x"), drow.get("extent_y"), drow.get("extent_z")] if drow else None))
    geometry=prune({
        "bounding_box_world_default": p("MeasuredWorldSize_DEFAULT") or d("VerifiedMeasuredWorldSizeDefault"),
        "bounding_box_local": p("MeasuredLocalSize") or d("VerifiedMeasuredLocalSize"),
        "bbox_center_local": p("LocalBBoxCenter") or d("VerifiedLocalBBoxCenter"),
        "origin_offset_from_bbox_center": p("LocalOriginOffsetFromBBoxCenter") or d("VerifiedLocalOriginOffsetFromBBoxCenter"),
        "local_bottom_offset_z": p("LocalBottomOffsetZ") or d("VerifiedLocalBottomOffsetZ"),
        "local_top_offset_z": p("LocalTopOffsetZ") or d("VerifiedLocalTopOffsetZ"),
        "expected_extent_xyz": expected_extent,
        "fbx_path": p("FBXPath") or d("FBXPath"), "model_name": p("ModelName") or d("ModelName"),
        "geometry_authority_warning": d("VerifiedExtractionStatus") if not pmrow else None,
        "_source": geometry_source,
    })
    # 2. ORIENTATION — verified rotation + per-facing footprints + master-CSV phase + override
    orientation=prune({
        "default_rotation_degrees": d("VerifiedDefaultRotationDegrees")  or p("DefaultRotationDegrees"),
        "footprint_rx90": pmrow.get("RX90WorldSize") or drow.get("VerifiedRX90WorldSize"),
        "footprint_ry90": pmrow.get("RY90WorldSize") or drow.get("VerifiedRY90WorldSize"),
        "footprint_rz90": pmrow.get("RZ90WorldSize") or drow.get("VerifiedRZ90WorldSize"),
        "ring_orientation_guidance": d("RingOrientationGuidance"),
        "phase_rule": c("orientation_phase_rule"), "phase_a_deg": c("phase_a_deg"), "phase_b_deg": c("phase_b_deg"),
        "default_state": c("default_orientation_state"), "default_direction": c("default_orientation_direction"),
        "pivot_center_type": c("pivot_center_type"), "origin_type": c("origin_type"),
        "override_source": "rules/PART_ORIENTATION_OVERRIDES.md" if has_override else None,
    })
    orientation["override_registered"]=bool(has_override)
    orientation["rule"]="RX=90 default unless override_registered; only RZ changes facing. phase_* (master CSV) hold validated rz when filled."
    orientation["_source"]="verified partmap (rotation/footprints) + master_csv (phase/pivot) + orientation_overrides"
    # 3. SCALE — verified world size at each scale + master-CSV scale behavior
    scaling=prune({
        "world_size_scale_0_5": p("Scale050WorldSize") or drow.get("VerifiedScale050WorldSize"),
        "world_size_scale_1_0": p("MeasuredWorldSize_DEFAULT") or drow.get("VerifiedMeasuredWorldSizeDefault"),
        "world_size_scale_1_5": p("Scale150WorldSize") or drow.get("VerifiedScale150WorldSize"),
        "world_size_scale_2_0": p("Scale200WorldSize") or drow.get("VerifiedScale200WorldSize"),
        "baseline_scale": c("baseline_scale"), "scale_behavior": c("scale_behavior"),
    })
    if scaling:
        scaling["rule"]="world size scales linearly; free-placed step = world_size * scale * 0.92 (snap steps are at scale 1.0)"
        scaling["_source"]="verified partmap (scale sizes) + master_csv (scale behavior)"
    # 4. SNAP-SPACING — concrete cardinal steps (authoritative snap map)
    # 5. CONNECTIONS — cross-plane seating (snap matrices/pairs). Surfaced as data here;
    #    the composed seated-transform composer is the dedicated next pass (OPEN topic).
    # 6. PLACEMENT RULES — named guidance + local axis rules + neighbor/fitment (master CSV)
    placement_rules=prune({
        "snap_spacing": snap_ss,
        "spacing_rule_fallback": d("SpacingRule"),
        "placement_guidance": d("ManualPlacementGuidance","PlacementGuidance"),
        "ring_placement_formula": d("RingPlacementFormula"), "ring_spacing_target": d("RingSpacingTarget"),
        "local_axis_rules": prune({"x":c("local_x_rule"),"y":c("local_y_rule"),"z":c("local_z_rule")}) or None,
        "neighbor_offset_summary": c("neighbor_offset_summary"), "fitment_modes": c("fitment_modes"),
        "recipe_candidates": recipe_cands or None,
    })
    if snap_ss and placement_rules.get("spacing_rule_fallback"):
        placement_rules["authority_note"]="snap_spacing is the connection authority and supersedes spacing_rule_fallback (full extent); fallback is for free-placed parts only"
    if placement_rules: placement_rules["_source"]="dims lib (spacing/guidance/ring) + master_csv (local rules/neighbor/fitment) + recipe library"
    # 7. FAMILY logic
    family=prune({
        "part_family": d("PartFamily","ManualPartFamily") or c("part_family"),
        "variant_of_clean": d("VariantOfClean"),
        "family_equivalence_status": c("family_equivalence_status"),
        "_source":"dims lib (PartFamily/variant) + master_csv (family equivalence)",
    })
    # 8. CHARACTERISTICS
    characteristics=dict(char) if char else None
    if characteristics: characteristics["_source"]="data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json (part_geometric_character)"
    # 9. METHOD AUTHORITY (allowed placement methods per context)
    method_authority={"allowed_methods":allowed,"_source":"data/METHOD_AUTHORITY_TABLE.json (object_contexts)"} if allowed else None
    # 10. ROLE
    role=prune({
        "likely_role": d("LikelyRole") or p("LikelyRole"),
        "validated_role": d("ValidatedRole","ManualCreativeRole"),
        "mechanics_use": d("MechanicsUseRecommendation") or p("MechanicsUseRecommendation"),
        "known_good_uses": d("KnownGoodUses"),
    })
    if role: role["_source"]="dims lib + verified partmap"
    # 11. CAUTIONS / negative knowledge
    cautions=prune({
        "known_issues": d("KnownIssues","KnownIssue","ManualKnownFailure"),
        "lesson_notes": d("LessonNotes"),
        "decorative_proxy_caution": d("DecorativeProxyCaution") or p("DecorativeProxyCaution"),
        "validation_flags": d("ValidationFlags","VerifiedFlags") or p("ValidationFlags"),
        "forbidden": forbidden,
    })
    if cautions: cautions["_source"]="dims lib + verified partmap + NEGATIVE_KNOWLEDGE_INDEX"
    # 12. VALIDATION STATUS — the trust signal. Geometry/orientation/scale ride the verified
    #     map's status; the placement-trial layer (orientation phase, neighbor, fitment) rides
    #     the master CSV status, which is UNTESTED/NEED_STUDY for most parts until trialed.
    pm_status=pmrow.get("ValidationStatus"); csv_status=(csvrow.get("validation_status") if csvrow else None)
    validation=prune({
        "geometry_orientation_scale": pm_status or "UNKNOWN",
        "placement_trial_layer": csv_status or "ABSENT",
        "validated_applications": c("validated_applications"),
        "validated_with_algorithm": c("validated_with_algorithm"),
        "next_validation_needed": c("next_validation_needed"),
    })
    validation["note"]=("geometry/orientation/scale are FBX-measured (trust per geometry_orientation_scale). "
        "The orientation-phase / neighbor-offset / fitment fields are only trustworthy where placement_trial_layer is "
        "validated; UNTESTED/NEED_STUDY/ABSENT means that value has not been trial-confirmed and must be verified by a build trial, not assumed.")

    spec={"geometry":geometry,"orientation":orientation,"validation":validation}
    if scaling: spec["scaling"]=scaling
    if snap_ss: spec["connections_TODO"]="cross-plane composed transforms not yet mapped (OPEN topic); snap_spacing covers in-plane tiling only"
    if placement_rules: spec["placement_rules"]=placement_rules
    if family: spec["family"]=family
    if characteristics: spec["characteristics"]=characteristics
    if method_authority: spec["method_authority"]=method_authority
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


def _part_effect_findings(ci, oids):
    """Return creative/effect family findings that mention any selected ObjectID."""
    oidset=set(oids); out={}
    pe=(ci.get("part_effect_and_use_findings",{}) or {}).get("families",[])
    for fam in pe:
        if not isinstance(fam,dict):
            continue
        members=[m.get("ObjectID") for m in fam.get("members",[]) if isinstance(m,dict) and m.get("ObjectID")]
        hit=sorted(oidset & set(members))
        if not hit:
            continue
        fid=fam.get("family_id") or ",".join(hit)
        out[fid]={
            "matched_objectids": hit,
            "status": fam.get("status"),
            "effect": fam.get("effect"),
            "rules": fam.get("rules",[]),
            "applications": fam.get("applications",[]),
            "authority": (ci.get("part_effect_and_use_findings",{}) or {}).get("authority","INFORMATIVE"),
            "_source":"data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json (part_effect_and_use_findings)"
        }
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
    mcsv=_master_csv(root)
    char_map=(_load(root,"data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json",{}) or {}).get("part_geometric_character",{})
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
        # 5.19.00 — gather every source for this ObjectID; assemble the full record below.
        drow=dims.get(oid,{}); csvrow=mcsv.get(oid,{}); char=char_map.get(oid)
        snap_ss=_part_snap_spacing(oid, snap_p2g, snap_groups) if oid in snap else None
        recipe_cands=_recipe_candidates(root,oid)
        has_override=("`"+oid+"`" in overrides_txt) or ("ObjectID "+oid in overrides_txt)
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
        placement_spec=_placement_spec(oid, row, drow, csvrow, char, snap_ss, has_override, recipe_cands, neg.get(oid), allowed)
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
    part_effect_findings=_part_effect_findings(ci, list(parts.keys()))

    return {"schema":"PROJECT_BUILD_PLACEMENT_PACKET_1.1","generated_from_rev":_pkg_rev(),"build_intent":intent or "",
        "MANDATORY_PLACEMENT_CONTEXT":{"parts":parts,"universal_process_rules":universal,
            "assembly_rule_behaviors":assembly_behaviors,
            "note":"FORCED. Build only from these parts; cite each in the BUILD COMPLIANCE MANIFEST; verified by compliance_manifest_check.py. assembly_rule_behaviors are build-level recipes triggered by the build intent."},
        "CREATIVE_CONTEXT":{"style_index":"data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json","creative_rules":creative_rules,
            "part_character":part_char,
            "part_effect_findings":part_effect_findings,
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
    ek=resolve(["BASE_BEAMSTONE","LIGHTBOX","SET_CLASS_A"],"colorable beam lighting")
    assert ek["CREATIVE_CONTEXT"]["part_effect_findings"], ek["CREATIVE_CONTEXT"]
    # firewall: advisory data must NOT leak into the forced mechanical surface
    assert "part_character" not in rk["MANDATORY_PLACEMENT_CONTEXT"]
    print("PART CONTEXT RESOLVER SELF-TEST: PASS"); return 0

if __name__=="__main__":
    if len(sys.argv)>=2 and sys.argv[1]=="--self-test": sys.exit(_self_test())
    ap=argparse.ArgumentParser(); ap.add_argument("--ids",nargs="+",required=True)
    ap.add_argument("--intent",default=""); ap.add_argument("--out",default=None); ap.add_argument("--root",default=None)
    a=ap.parse_args(); pk=resolve(a.ids,a.intent,a.root); s=json.dumps(pk,indent=1)
    (open(a.out,"w").write(s),print("wrote",a.out)) if a.out else print(s)
