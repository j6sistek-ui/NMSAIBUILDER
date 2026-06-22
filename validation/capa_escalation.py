#!/usr/bin/env python3
"""
capa_escalation.py  (5.03.00)

Records/clears the CAPA escalation that makes the deeper BUILD COMPLIANCE MANIFEST a
REQUIRED run_gate gate. Per policy it is OPENED (review-logged) only when a CAPA's root
cause is skipping known existing information in source docs or the build sheet
(BUILD_SHEET_FABRICATION / SHEET_NOT_UTILIZED). The lean sheet gate trusts the AI's
"sheet used" attestation; when that trust is breached, the deeper per-part proof becomes
mandatory until a corrective build clears it.

Usage:
  capa_escalation.py --status
  capa_escalation.py --open  --reason "..."
  capa_escalation.py --clear --note "corrective build <ver> passed deeper manifest; prevention logged"
  capa_escalation.py --self-test
"""
import json,os,sys,datetime
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE=os.path.join(ROOT,"data","CAPA_ESCALATION_STATE.json")
def load(p): 
    try: return json.load(open(p))
    except Exception: return {"schema":"NMS_CAPA_Escalation_State_1.0","active":False,"reason":"","opened":"","trigger_class":"","history":[]}
def save(d,p): json.dump(d,open(p,"w"),indent=2)
def _self_test():
    import tempfile
    p=os.path.join(tempfile.mkdtemp(),"s.json"); save({"active":False,"history":[]},p)
    assert not load(p)["active"]
    d=load(p); d["active"]=True; d["history"]=[{"action":"open"}]; save(d,p); assert load(p)["active"]
    d=load(p); d["active"]=False; save(d,p); assert not load(p)["active"]
    print("CAPA ESCALATION SELF-TEST: PASS"); return 0
def main(argv):
    if "--self-test" in argv: return _self_test()
    def opt(name,default=None):
        return argv[argv.index(name)+1] if name in argv and argv.index(name)+1<len(argv) else default
    path=opt("--state",STATE); now=datetime.date.today().isoformat(); d=load(path)
    if "--open" in argv:
        d["active"]=True; d["reason"]=opt("--reason","skipped known existing source/build-sheet information")
        d["opened"]=now; d["trigger_class"]="BUILD_SHEET_FABRICATION/SHEET_NOT_UTILIZED"
        d.setdefault("history",[]).append({"action":"open","date":now,"reason":d["reason"]}); save(d,path)
        print("CAPA ESCALATION: OPEN — deeper compliance manifest now REQUIRED at run_gate"); return 0
    if "--clear" in argv:
        d["active"]=False; d.setdefault("history",[]).append({"action":"clear","date":now,"note":opt("--note","")}); save(d,path)
        print("CAPA ESCALATION: CLEARED"); return 0
    print("CAPA ESCALATION:", "ACTIVE" if d.get("active") else "inactive", "-", d.get("reason","")); return 0
if __name__=="__main__": sys.exit(main(sys.argv[1:]))
