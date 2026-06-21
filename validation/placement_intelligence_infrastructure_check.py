#!/usr/bin/env python3
"""Check that placement-intelligence governance infrastructure is present and internally coherent."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = [
  "rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md",
  "rules/BUILD_PLACEMENT_SNAPSHOT_PROTOCOL.md",
  "rules/PLACEMENT_MECHANICS_VS_CREATIVE_STYLE_SEPARATION_RULE.md",
  "rules/SINGLE_MASTER_CHANGELOG_GOVERNANCE_RULE.md",
  "data/PLACEMENT_PRECEDENCE.json",
  "data/METHOD_AUTHORITY_TABLE.json",
  "data/NEGATIVE_KNOWLEDGE_INDEX.json",
  "data/MASTER_PLACEMENT_INTELLIGENCE_INDEX.json",
  "data/CREATIVE_USE_CASE_AND_STYLE_INDEX_STUB.json",
  "schemas/PLACEMENT_SESSION_RECEIPT.schema.json",
  "schemas/BUILD_PLACEMENT_SNAPSHOT.schema.json",
  "schemas/PLACEMENT_METHOD_SUMMARY.schema.json",
  "schemas/ASSEMBLY_CONFORMANCE_PLAN.schema.json",
  "templates/PLACEMENT_SESSION_RECEIPT_TEMPLATE.json",
  "templates/BUILD_PLACEMENT_SNAPSHOT_TEMPLATE.json",
  "templates/PLACEMENT_METHOD_SUMMARY_TEMPLATE.json",
  "templates/ASSEMBLY_CONFORMANCE_PLAN_TEMPLATE.json",
  "templates/PART_USAGE_MANIFEST_TEMPLATE.csv",
  "OPEN_TOPICS_LOG.md",
]

def load_json(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)

def main():
    fails=[]
    for rel in REQUIRED:
        if not os.path.exists(os.path.join(ROOT, rel)):
            fails.append(f"missing required placement intelligence infrastructure file: {rel}")
    if fails:
        print("PLACEMENT INTELLIGENCE INFRASTRUCTURE: FAIL")
        print("\n".join(fails))
        return 1
    precedence=load_json("data/PLACEMENT_PRECEDENCE.json")
    authority=load_json("data/METHOD_AUTHORITY_TABLE.json")
    negative=load_json("data/NEGATIVE_KNOWLEDGE_INDEX.json")
    mpii=load_json("data/MASTER_PLACEMENT_INTELLIGENCE_INDEX.json")
    methods=set(authority.get("method_definitions",{}))
    for required in ["STAIR_RAMP_ENDPOINT_RECIPE","WALL_SHELL_GRID_COURSE","BILLBOARD_ORIENTATION_OVERRIDE","PIPE_CONTEXTUAL_CONNECTOR_VALIDATION","MANUAL_DIRECT_PLACEMENT"]:
        if required not in methods:
            fails.append(f"METHOD_AUTHORITY_TABLE missing method {required}")
    neg_entries=negative.get("entries",{})
    for obj in ["CUBEWALL_SPACE","PIPE","BASE_BUBPIPE"]:
        if obj not in neg_entries:
            fails.append(f"NEGATIVE_KNOWLEDGE_INDEX missing {obj}")
    if "EXCEPTION_OR_PROHIBITED_INDEX" not in [p.get("id") for p in precedence.get("precedence",[])]:
        fails.append("PLACEMENT_PRECEDENCE missing exception/prohibited priority lane")
    if mpii.get("creative_knowledge_policy") is None:
        fails.append("MASTER_PLACEMENT_INTELLIGENCE_INDEX missing creative knowledge separation policy")
    # enforce root hygiene for release-specific open topic files
    for fn in os.listdir(ROOT):
        if fn.startswith("OPEN_TOPICS_LOG_"):
            fails.append(f"root contains release-specific open topics file: {fn}")
    if fails:
        print("PLACEMENT INTELLIGENCE INFRASTRUCTURE: FAIL")
        print("\n".join(fails))
        return 1
    print("PLACEMENT INTELLIGENCE INFRASTRUCTURE: PASS")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
