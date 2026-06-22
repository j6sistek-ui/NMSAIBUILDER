#!/usr/bin/env python3
"""discover_by_quality view + sync gate.
Builds a deterministic reverse index (quality/effect token -> [ObjectIDs]) from the
creative index's part_geometric_character + part_effect_and_use_findings, so a chat can
go intent -> qualities -> candidate parts BEFORE selecting ObjectIDs (discovery-first).
--write regenerates the view into the index; default mode fails if the stored view drifts.
"""
import os,re,sys,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CI=os.path.join(ROOT,"data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json")
STOP=set("the a an and or of to for with plus from this that into onto between after note ideal capable true false local axis profile dims".split())
def _toks(s):
    return [w for w in re.split(r"[^a-z0-9]+",str(s).lower()) if len(w)>=4 and not w.isdigit() and w not in STOP]
def build_view(ci):
    inv={}
    def add(tok,oid):
        inv.setdefault(tok,set()).add(oid)
    for oid,v in (ci.get("part_geometric_character",{}) or {}).items():
        for field in ("profile","note","long_axis"):
            for t in _toks(v.get(field,"")): add(t,oid)
        if v.get("smooth_surface_capable") is True: add("smooth",oid)
    for fam in (ci.get("part_effect_and_use_findings",{}) or {}).get("families",[]):
        oids=[m.get("ObjectID") for m in fam.get("members",[]) if m.get("ObjectID")]
        text=" ".join(str(fam.get(k,"")) for k in ("effect","family_id"))+" "+" ".join(map(str,fam.get("applications",[]) if isinstance(fam.get("applications"),list) else [fam.get("applications","")]))
        for t in _toks(text):
            for oid in oids: add(t,oid)
    return {tok:sorted(oids) for tok,oids in sorted(inv.items())}
def main(write=False):
    ci=json.load(open(CI,encoding="utf-8"))
    view=build_view(ci)
    block={"schema":"discover_by_quality_v1","generated":True,
           "note":"GENERATED reverse index: quality/effect token -> candidate ObjectIDs. Consult at discovery time (intent -> qualities -> parts) BEFORE selecting ObjectIDs. Regenerate with discover_by_quality_check.py --write.",
           "by_quality":view}
    if write:
        ci["discover_by_quality"]=block
        json.dump(ci,open(CI,"w",encoding="utf-8"),indent=1)
        print(f"discover_by_quality written: {len(view)} quality tokens"); return 0
    stored=(ci.get("discover_by_quality") or {}).get("by_quality")
    if stored is None: print("DISCOVER_BY_QUALITY: FAIL — view missing (run --write)"); return 1
    if stored!=view: print("DISCOVER_BY_QUALITY: FAIL — out of sync (run --write)"); return 1
    print(f"DISCOVER_BY_QUALITY: in sync ({len(view)} quality tokens)"); return 0
if __name__=="__main__": sys.exit(main(write=("--write" in sys.argv)))
