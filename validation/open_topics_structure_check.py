#!/usr/bin/env python3
"""Open-topics continuity structure gate.
Fails if OPEN_TOPICS_LOG.md topics lack the required fields, or if the copy-paste
chat transfer doc is missing. Enforces the single-authoritative-continuity-artifact rule.
"""
import os, re, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ=["Issue","Discovery","Why It Matters","Decision","Next Steps","Status","Priority","Success Criteria","Last Updated"]
def main():
    fails=[]
    otl=os.path.join(ROOT,"OPEN_TOPICS_LOG.md")
    if not os.path.exists(otl): return _fail(["OPEN_TOPICS_LOG.md missing"])
    text=open(otl,encoding="utf-8").read()
    topics=re.split(r"^## TOPIC:",text,flags=re.M)[1:]
    if not topics: fails.append("OPEN_TOPICS_LOG.md has no '## TOPIC:' entries")
    for t in topics:
        title=t.splitlines()[0].strip()
        for f in REQ:
            if f"**{f}:**" not in t and f"{f}:" not in t:
                fails.append(f"topic '{title}' missing field: {f}")
    if not os.path.exists(os.path.join(ROOT,"transfer_prompts/CHAT_TRANSFER_CURRENT.md")):
        fails.append("transfer_prompts/CHAT_TRANSFER_CURRENT.md missing (copy-paste chat transfer doc)")
    if fails: return _fail(fails)
    print(f"OPEN-TOPICS STRUCTURE CHECK: PASS ({len(topics)} topics, all fields present; chat transfer doc present)"); return 0
def _fail(fs):
    print("OPEN-TOPICS STRUCTURE CHECK: FAIL"); [print("  - "+f) for f in fs]; return 1
if __name__=="__main__": sys.exit(main())
