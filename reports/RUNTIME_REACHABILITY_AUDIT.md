# RUNTIME REACHABILITY AUDIT — first pass

Measure package value by **execution-path reachability**, not file count. A file earns its place if it reaches: runtime behavior (build packet), creative context, a transfer artifact, validation/gates, or the operating/reading path (referenced by a rule / START_HERE / operating card). Files referenced nowhere are dead weight regardless of size.

Repeatable measurement: `python3 validation/runtime_reachability_audit.py` (advisory, non-gating).

## First-pass results

- **Rules: 62/62 mapped.** Every rule has a runtime destination — 23 build-packet (RULE/RECIPE/NEGATIVE -> `applicable_rule_behaviors` / `assembly_rule_behaviors`), 34 operating/gates (PROCESS/GOVERNANCE), 3 lookup (REFERENCE), 2 creative (FINDING). The rule layer is fully execution-mapped.
- **data / templates / schemas / toolkit:** the referenced ones resolve to a check, the resolver, or the AI's fill-in path (e.g. `PART_PLACEMENT_AID_LEDGER.json`, the compliance-manifest template/schema, the banner template).
- **reports/ (~32):** evidence/transfer by design — not runtime. Strong candidate to move under an archive/attic to shrink the active surface.

## True orphans — referenced nowhere in code or docs (archive candidates)

These reach no execution path and nothing points to them, so a chat would never invoke or read them:

- `validation/NMS_HARD_GUARD_SNIPPET.py`
- `validation/NMS_JSON_STUDY_Jurassic_Beach_feature_isolation_helper.py`
- `validation/NMS_JSON_STUDY_Jurassic_Beach_feature_isolation_helper_REVISED.py`  (duplicate of the above)
- `validation/NMS_JSON_TO_PYTHON_RECREATION_TEMPLATE_v53.py`
- `validation/NMS_RUNTIME_OBJECT_AUDIT_SNIPPET.py`
- `validation/NMS_SCRIPT_LINTER.py`
- `validation/NMS_VALIDATE_TEXT_BLOCKS_IN_BLENDER.py`
- `validation/NMS_VALID_CASTLE_STARTER_REAL_PARTS.py`
- `validation/stair_semantic_float_gate.py`  (semantic float gate was proposed, not adopted)
- `templates/LESSON_PROMOTION_TEMPLATE.md`
- `templates/PROJECT_CONTEXT_TEMPLATE.md`

Recommended verdict: archive. Two are clear (`*_REVISED` duplicate; `stair_semantic_float_gate` never adopted). The standalone build snippets (linter, hard-guard, starters) are only true waste if no operating-card/START_HERE entry will ever point to them; the alternative is to *wire* the useful ones (give them a reading path) rather than archive. That per-file call is the audit's remaining work.

## Method notes / caveats

- "Referenced" = the basename appears in some other `.py`/`.md`/`.json` (excluding `FILE_INVENTORY.md`, which lists everything, and `/archive/`).
- A file with even one reference is treated as reachable; this is deliberately conservative (it under-flags, not over-flags), so the orphan list is a floor, not a ceiling.
- Next pass: classify each orphan as ARCHIVE vs WIRE (give it a reading path); then sweep `reports/` and historical references to an attic.
