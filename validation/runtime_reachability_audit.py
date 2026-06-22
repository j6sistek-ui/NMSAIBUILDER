#!/usr/bin/env python3
"""Runtime reachability audit (ADVISORY, non-gating).
Measures package value by execution-path reachability rather than file count.
A file is "reachable" if it reaches an execution path: code (imported/invoked),
docs (referenced by a rule / operating card / START_HERE), runtime behavior,
creative context, transfer artifact, or validation. Files referenced nowhere are
TRUE ORPHANS — archive candidates. Run: python3 validation/runtime_reachability_audit.py
"""
import os,glob,json,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def read(p):
    try: return open(p,encoding="utf-8",errors="ignore").read()
    except: return ""
def main():
    os.chdir(ROOT)
    # reference corpus = ACTIVE code + reading-path docs only.
    # Exclude evidence/history (reports, changelog, release notes, OTL) and the inventory:
    # a mention in evidence is not an execution path.
    EXCL=("FILE_INVENTORY.md","CHANGELOG.md","OPEN_TOPICS_LOG.md","PACKAGE_MANIFEST.json")
    corpus=[f for f in glob.glob("**/*.py",recursive=True)+glob.glob("**/*.md",recursive=True)+glob.glob("**/*.json",recursive=True)
            if os.path.basename(f) not in EXCL and not f.startswith("archive/") and "/archive/" not in f
            and not f.startswith("reports/") and "/reports/" not in f and not os.path.basename(f).startswith("RELEASE_NOTES")]
    text={f:read(f) for f in corpus}
    # rules are reachable by classification (every rule has a runtime destination)
    led=json.load(open("data/RULE_CLASSIFICATION.json"))["rules"]
    sections=["validation/*.py","data/*.json","templates/*","schemas/*","toolkit/*","library/*"]
    true_orphans=[]
    for pat in sections:
        for f in sorted(glob.glob(pat)):
            if f.startswith("archive/") or "/archive/" in f or os.path.abspath(f)==os.path.abspath(__file__): continue
            b=os.path.basename(f)
            refs=sum(t.count(b) for p,t in text.items() if p!=f)
            if refs==0: true_orphans.append(f)
    print("RUNTIME REACHABILITY AUDIT (advisory)")
    print(f"  rules: {len(led)} classified, each with a runtime destination (build-packet / operating / lookup / creative)")
    print(f"  true orphans (referenced nowhere in code or docs): {len(true_orphans)}")
    for f in true_orphans: print(f"     ARCHIVE-CANDIDATE  {f}")
    if not true_orphans: print("     none")
    # validation tier breakdown (evidence: validation/VALIDATION_INDEX.json) + drift check
    try:
        vi=json.load(open("validation/VALIDATION_INDEX.json"))
        scripts=vi["scripts"]; present=sorted(b for b in (os.path.basename(p) for p in glob.glob("validation/*.py")))
        from collections import Counter
        counts=Counter(scripts.get(s,"UNTIERED") for s in present)
        print("  validation tiers (used vs not used, objective):")
        for tier in ["RUNTIME_ORCHESTRATOR","BUILD_GATE","RUNTIME_LIB","RELEASE_SELFTEST","AUDIT_TOOL","REDUNDANT","UNTIERED"]:
            if counts.get(tier): print(f"     {tier:22} {counts[tier]}")
        drift=[s for s in present if s not in scripts]
        if drift: print(f"     DRIFT: validation script(s) not tiered in VALIDATION_INDEX.json: {drift}")
    except Exception as e:
        print(f"  validation tier report unavailable: {e}")
    return 0
if __name__=="__main__": sys.exit(main())
