# CHAT TRANSFER — copy/paste this whole block into a new chat to resume

You are resuming an NMS Base Builder governance-package work-stream in **Builder mode**: prove-don't-attest, executable validation over self-attestation, one clarifying question at a time, end every substantive reply with the PROTOCOL banner.

## Who / what
- User: James. Builds No Man's Sky bases via the "No Man's Sky Base Builder" Blender add-on (v6.4.1; Blender 5.0.1). Work-stream: auditing/cleaning/consolidating the `NMS_master_docs` governance package.
- Current package: **5.15.00** (gate PASS). Extract the uploaded package; deliverables to `/mnt/user-data/outputs`.

## What happened (most recent first)
- **5.15.00:** onboarding gauntlet now includes one `S_RAMP` (proof-ledger part) so floor/wall/roof builds don't dead-end on the auto-required validated-logic-reuse gate (FAILs on zero proof-ledger parts). Orientation authoring caution added to 02_GENERATOR_CONTRACT. OPEN: whether to relax the reuse gate's zero-proof-part FAIL for all builds (not just onboarding).
- **5.14.00 (design-intent + orientation quality gates):** Fixed the v4->5.x placement-QUALITY regression. Build-type scripts must now declare DESIGN_INTENT (per assembly is_a+target_read+style_source from CREATIVE_USE_CASE_AND_STYLE_INDEX; every used ObjectID needs a purpose) — auto-required, enforced in run_gate, documented in 02_GENERATOR_CONTRACT.md, modeled in gothic_church_v01.py. New orientation gate flags parts rotated off DefaultRotationDegrees on RX/RY without authorization (RZ/facing free; JSON-recreation exempt). Spire/taper recipes routed in FEATURE_RECIPE_ROUTE_INDEX; flying_buttress -> NO_VALIDATED_RECIPE guard + NEGATIVE_KNOWLEDGE entry. Curve-follow contract re-absorbed from v4 into CONNECTED_PIECE_CURVATURE_GRAMMAR.md. v4 study confirmed snap data preserved+better-wired; regression was unrouted recipes + ungated intent, not lost data. No new files. OPEN: wire AI_CAPTURE to confirm each assembly reads as its target_read.
- **5.13.00 (gate-report fixes):** connectivity/no-float gate now FALLS BACK to `library/nms_part_dimensions_and_rules_updated.json` for extents when the supplied `<library>` lacks them (the verified part map has IDs but no `extent_x/y/z`), so connectivity stops silently SKIPPING. New static linter check FAILS delivered scripts that bake `hide_viewport=True`/view-layer `exclude=True` (resist Alt+H); AI_CAPTURE_COMPLIANCE_CONTRACT.md now requires hand-off visibility, review isolation via recoverable `hide_set()`. Part-placement-map coverage note reworded as a proof ledger, not verified-partmap status. No new files.
- **5.12.00 (Wave 3 runtime mapping):** The resolver now CONSUMES the classification. Per part it emits `applicable_rule_behaviors` ({rule_id, kind, authority, required_behavior, check, applies_to}) filtered to KEEP RULE/RECIPE/NEGATIVE — no process/governance/finding/reference leaks. Behaviors come from new `data/RUNTIME_BEHAVIORS.json` (all 23 KEEP runtime rules authored). `build_sheet_check` validates behaviors (tamper-evident + non-empty). Onboarding is now a builder-readiness gauntlet (gate #26); `discover_by_quality` reverse index added with sync gate #27 and wired into kickoff.
- **5.07.00 (Wave 2 physical execution):** 30 duplicate-law docs absorbed into 13 survivors; rule layer 92 -> 62. Family rules demoted to findings.
- **5.06.x:** classification spine (gate #24) + continuity artifacts (gate #25).

## Why
Eyeball-era duplicates, mis-scoped rules invisible to the resolver, and a write-only creative KB. The full rule-by-rule review is complete and encoded as data; Wave 2 physically executed the consolidations the review approved.

## What was decided
- Operating test: *removing it changes what's allowed/required -> RULE; removing it only changes what you know -> FINDING.*
- Consolidate content-preserving (append as `absorbed from X`, never drop); gate every step.
- Family findings inform via the creative index; placement families are not law.

## What to do next (read `OPEN_TOPICS_LOG.md` + the two reports in `reports/`)
Deep runtime audit done (5.12.00): `validation/` is tiered in `validation/VALIDATION_INDEX.json` (build gates vs release self-tests vs audit tools; DRIFT-checked). One redundant script purged. Single creative STORE OF RECORD declared (`data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json`; catalog is subordinate reference). Two deferred evidence-backed reductions remain: (1) fold the catalog's 16 `use_cases` into the index then slim the catalog; (2) purge `library/nms_master_part_map_verified_data_v3_01_02.csv` after confirming `partmap_storage_check` doesn't need it. Also still open: discover_by_quality coverage, assembly-keyword recall, Wave2/3 re-audit. Run `validation/runtime_reachability_audit.py` each release (target 0 orphans, 0 DRIFT).

## New-data handling (important)
User-provided recipes/part-characteristics route into the EXISTING store of record, runtime-linked, NEVER a new file/report (see rules/RULE_UPDATE_PROTOCOL.md "New data intake routing"). The package is at file maturity: new files are blocked by gate #28 (new_file_guard_check.py + release/APPROVED_FILES.json) and require explicit user approval recorded in the manifest.

## Critical mechanics
- Gate to PASS: `python3 release/release_check.py` (gates #24 classification, #25 open-topics structure, version-callout, dangling-ref, RPAM coverage, run_gate self-tests, build-sheet/resolver consistency, partmap drift). Clear `__pycache__`/`.pyc`; set manifest `file_count` to actual; write `protocol_banner_good.txt` with a SEPARATE read-then-write.
- **After any rule rename/merge:** regenerate every packet (`runs/*__PACKET.json`, `validation/gate_fixtures/build_sheet_good.json`) via `part_context_resolver.py --ids … --intent … --out …` and RESTORE `build_application` per part from the prior packet (recover from the last shipped zip if overwritten).
- PRESERVE VERBATIM: `COORD_MODE="XnZY"` / `AXIS_MODE="RIGHT_AT_UP"` / `BASE_ROTATION_MODE="POST_RX90"` / `POST_BASELINE_CORRECTION="LOCAL_Y_180"`; `Position=[x,z,-y]`.

## Standing output requirement (every build/doc update or on "checkpoint")
Provide BOTH: this CHAT TRANSFER doc refreshed, and an updated `OPEN_TOPICS_LOG.md` in the per-topic structure (Issue / Discovery / Why It Matters / Decision / Next Steps / Status / Priority / Success Criteria / Last Updated). Gate #25 enforces it.


## Latest update — resolver forwards curated guidance + template-leak gate
The runtime packet was trimmed 'light on context' and had stopped forwarding the dimensions-library curated guidance (SpacingRule, PlacementGuidance, LikelyRole, ring formulas, KnownIssues, lessons) — the regression behind builds fighting every part. part_context_resolver.py now forwards it as advisory CREATIVE_CONTEXT.per_part_curated_guidance, plus a spacing_authority_note (snap points supersede the extent SpacingRule: S_WALLM 5.3379 snap vs 5.691 extent). run_gate.py now FAILS template leaks (stray TPL_ to export / 2+ ObjectIDs at origin); the generator contract and the canonical gothic_church_v01.py delete templates before export. A parallel live-Blender chat is auditing this against its own resolver patch — reconcile to one source of truth.
