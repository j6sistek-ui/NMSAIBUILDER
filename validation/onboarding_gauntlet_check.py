#!/usr/bin/env python3
"""Onboarding gauntlet structure gate.
Fails the release if the onboarding validation build does not specify a true
builder-readiness gauntlet: real micro-build, actually-run run_gate (no hand-typed PASS),
a fail->diagnose->correct->second-gate loop, and an explicit BUILDER READINESS verdict.
"""
import os,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def main():
    p=os.path.join(ROOT,"ONBOARDING_VALIDATION_BUILD.md")
    if not os.path.exists(p): return _fail(["ONBOARDING_VALIDATION_BUILD.md missing"])
    t=open(p,encoding="utf-8").read().lower()
    need={
      "real micro-build":("micro-build" in t and "not a simulation" in t),
      "actually-run run_gate (no hand-typed PASS)":("run_gate" in t and "never a hand-typed pass" in t),
      "failure loop (diagnose+correct+second gate)":all(w in t for w in ("diagnose","correct","second gate")),
      "builder-readiness verdict":("builder readiness" in t),
      "source vs builder readiness distinction":("source readiness" in t and "builder readiness" in t),
    }
    miss=[k for k,ok in need.items() if not ok]
    if miss: return _fail([f"onboarding gauntlet missing: {m}" for m in miss])
    print("ONBOARDING GAUNTLET CHECK: PASS (real micro-build + run_gate + failure loop + readiness verdict)"); return 0
def _fail(fs):
    print("ONBOARDING GAUNTLET CHECK: FAIL"); [print("  - "+f) for f in fs]; return 1
if __name__=="__main__": sys.exit(main())
