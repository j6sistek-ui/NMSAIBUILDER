# 00 — OPERATING CARD  (the only page you must always hold)

THIS IS THE LAW. Build from this card + the generated PROJECT BUILD PLACEMENT
PACKET. Do NOT try to read the 300-file library during a build — resolve a packet.


## Review assistance and transfer continuity

- Blender triage output is a review-assistance artifact only. It identifies candidate review areas and supports AI-human communication; it is not placement authority, conformance authority, compliance authority, or a CAPA trigger. See `rules/TRIAGE_REVIEW_ASSISTANCE_TOOL_RULE.md`.
- Major deliverables require a Project Transfer Summary so the project can survive chat-limit/context-loss events. If the user says `checkpoint`, refresh `OPEN_TOPICS_LOG.md` and `transfer_prompts/CHAT_TRANSFER_CURRENT.md`. See `rules/PROJECT_TRANSFER_SUMMARY_RULE.md`.

## The build loop (every build, Python or live Blender — identical)
```text
1. Router classifies the request.
2. Declare intended ObjectIDs.
3. RESOLVE the builder sheet:
     python3 validation/part_context_resolver.py --ids <IDs> --intent "<intent>" --out runs/<build>__PACKET.json
   -> small sheet: only these parts' geometry, snap, precedence tier, allowed methods,
      forbidden (negative knowledge), recipes, relevant rules — one entry per part.
4. ANNOTATE: fill each part's build_application (what the part does in THIS build).
   Do NOT edit mechanical fields — the gate re-runs the resolver and rejects edits.
5. In the Python build, declare:  PROJECT_BUILD_SHEET = "runs/<build>__PACKET.json"  and  BUILD_SHEET_USED = True
6. Build using ONLY the sheet's MANDATORY_PLACEMENT_CONTEXT.
7. GATE:  python3 validation/run_gate.py <script.py> <library.json> <TAG> --require-router
   <library.json> = library/nms_part_dimensions_and_rules_updated.json (the DIMENSIONS library — it carries
   extent_x/y/z, which the connectivity/no-float gate needs). The verified part map
   (nms_master_part_map_verified_data_v3_01_02.json) is placement/snap authority but has NO extents; if it is
   passed instead, run_gate now auto-falls-back to the dimensions library for extents so connectivity still runs.
   run_gate verifies: every used ObjectID is in the sheet (coverage); each build_application is
   filled (populated); the sheet's mechanical fields still match the resolver (tamper-evident);
   and the sheet was declared used. PASS or the build is INVALID.
```
(The hand-written BUILD COMPLIANCE MANIFEST + compliance_manifest_check.py remain an OPTIONAL deeper tool;
the gate requirement is the generated builder sheet, which can't be fabricated.)

**CAPA escalation:** if a build fails because known source/build-sheet info was skipped, open a CAPA escalation
(`validation/capa_escalation.py --open`). While active, run_gate ALSO requires the deeper compliance manifest until a
corrective build clears it. The deeper tool is the *consequence* of fabrication-without-utilization, not routine overhead.

## First duty — precedence resolution (per ObjectID)
Placement Intent -> Precedence Resolution -> Method Selection.
Governing tier comes from DATA BACKING (data/PLACEMENT_PRECEDENCE.json):
```text
1 exact JSON / known-feature recipe        (claim only with a verifiable recipe ref)
2 add-on snap / relational data            (snap-enrolled parts)
3 validated assembly recipe                (claim only with a verifiable recipe ref)
4 verified part map component mechanics
5 placement map / orientation override
6 negative knowledge / exception           (OVERRIDES positive data)
7 manual fallback                          (only if METHOD_AUTHORITY_TABLE allows)
FBX bounds = last resort, below tier 4.
```

## Mechanical vs creative
- MANDATORY_PLACEMENT_CONTEXT: forced, gate-verified. You may not deviate.
- CREATIVE_CONTEXT: offered, evaluated, NEVER gated. Style may choose parts; chosen
  parts still pass the mechanical gate; creativity never overrides precedence/negative knowledge.
- CREATIVE_CONTEXT is now POPULATED per build (5.04.00, advisory/never gated): `part_character` (geometric profile
  of each build part), `applicable_failure_modes` (geometric-failure cautions matched to the build's parts/intent —
  data/GEOMETRIC_FAILURE_MODE_INDEX.json), and named `placement_recipes` + `orientation_recipes` + `fit_rules`
  (data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json). Read these before composing; they are guidance, not constraints.

## Live-build disciplines (Blender)
- Screenshot-verify EVERY build step before continuing — visual review is how geometric artifacts are caught.
- Checkpoint-save the .blend / export through the add-on after each build batch; a crash resets the live scene to the default file.
- Live creative geometry is BLENDER-tier, never GAME_VALIDATED; do not claim a higher tier from a screenshot.

## Banner (end every substantive reply)
```text
PROTOCOL ✓ — type: <t> | source docs rev: <X.YY.ZZ> | bundle: <router route + rules> | precedence: <resolved per ObjectID | n/a> | gate: <compliance_manifest_check / run_gate verdict> | ambiguity: <none|...> | Docs Avail for Update?: <Yes (N)|No (0)>
```

The 300 documents are a SEARCHABLE SOURCE LIBRARY, not a reading list. The resolver
pulls what a build needs; everything else is reference/audit.

## Optional visual-review tool
For visual/in-game review loops, the optional Blender add-on `toolkit/nms_ai_review_bundle_addon_v04.py` captures exterior/interior/cutaway review evidence. It complements but never replaces exported-JSON gates or `validation/run_gate.py` (which enforces `AI_CAPTURE_COMPLIANCE`).
