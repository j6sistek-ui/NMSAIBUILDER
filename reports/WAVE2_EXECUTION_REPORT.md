# Rule-Review Wave 2 — Execution Report (for external audit)

Package: NMS master docs 5.06.00. This report tells an auditing chat exactly what the rule-by-rule review concluded, what was executed, what is staged, and how to verify it.

## Audit entry points
- `data/RULE_CLASSIFICATION.json` — the per-rule ledger: `kind`, `runtime_status`, `disposition` for all 92 rules. Source of truth for the review's verdicts.
- `data/RULE_PART_APPLICABILITY_MAP.json` — each rule entry now carries `kind` + `runtime_status` inline.
- `validation/rule_classification_check.py` — gate #24: fails the release if any rule lacks kind/runtime_status or if ledger and map disagree. Run `python3 release/release_check.py` -> must print `RELEASE GATE: PASS`.

## Classification scheme
- **kind**: RULE (governs behavior) · RECIPE (reusable assembly) · FINDING (descriptive part/build knowledge) · PROCESS · GOVERNANCE · REFERENCE (config/lookup, not a rule) · NEGATIVE (do-not-use).
- **runtime_status**: KEEP · CONSOLIDATE (merge into a survivor) · FOLD (small merge) · RELOCATE · SUPERSEDED · REPAIR · DEVERSION · RETIRE_TO_FINDING.
- Operating test: *removing it changes what is allowed/required -> RULE; removing it only changes what you know -> FINDING.*

## Executed this wave (verifiable in the package)
1. **Classification spine + gate** — all rules classified; gate #24 enforces completeness (enforces RULE_UPDATE_PROTOCOL, which the review found was not followed).
2. **Folds (content preserved):** `DELTA_LEARNING_PROTOCOL` -> `SELECTIVE_VISUAL_MEMORY_POLICY` (section "Delta learning"); `CONNECTED_SURFACE_NO_STEPPED_OFFSET_RULE` -> `CONNECTED_PIECE_CURVATURE_GRAMMAR` (section "Anti-pattern: no stepped-offset substitute"). Files deleted, RPAM/ledger/inventory updated, no dangling refs.
3. **Repair:** `PROJECT_CONTEXT_PROTOCOL` rewritten (a prior bulk edit had overwritten every project-folder bullet with the same filename).
4. **De-version:** `PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE` prose changed from changelog narration to present tense.
5. **Wiring:** `GROUND_ZERO_FOUNDATION_RULE` -> UNIVERSAL_PROCESS (build-context, not part-keyed). (Wave 1, 5.05.00, already re-scoped 5 other rules and wired the resolver into START HERE/kickoff.)

## Staged consolidations (encoded as data; specs below; deliberately not rushed)
These are large multi-doc, content-preserving merges. Each is marked CONSOLIDATE/FOLD/RELOCATE in the ledger with its survivor. Doing all of them in one pass risks the content loss the owner explicitly flagged, so they are staged with preservation constraints:

- **JSON ladder -> `JSON_TO_PYTHON_RECREATION_PROTOCOL`** (absorbs JSON_STUDY_PLACEMENT_RECIPE, JSON_GEOMETRY_INTELLIGENCE, JSON_FEATURE_CONCEPT_EXTRACTION). PRESERVE VERBATIM: `COORD_MODE="XnZY"`, `AXIS_MODE="RIGHT_AT_UP"`, `BASE_ROTATION_MODE="POST_RX90"`, `POST_BASELINE_CORRECTION="LOCAL_Y_180"`, `right=at.cross(up)`, `JSON Position=[x,z,-y]`. Keep WORKING_JSON_FIRST_PRINCIPLE + JSON_EVIDENCE_MAPPING_GATE + JSON_GEOMETRY_VALIDATION_LOOP separate.
- **Precedence/authority law -> `PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE`** (absorbs PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE, PLACEMENT_INTELLIGENCE_GOVERNANCE, ASSEMBLY_CONTEXT_SUPERSEDES). PRESERVE every precedence tier + "resolution is a recorded artifact". Keep data files `PLACEMENT_PRECEDENCE.json` + `METHOD_AUTHORITY_TABLE.json`.
- **Part-map library -> `PART_PLACEMENT_MAP_SCHEMA`** (absorbs PART_PLACEMENT_MAP_USAGE_AND_VALIDATION, PARTMAP_STORAGE_COMPLIANCE, PART_PLACEMENT_MAP_SCHEMA; VERIFIED_PARTMAP_DATA as data-provenance section). PRESERVE SNAP_VALIDATED/GOLD tiers + the ~919-non-snap fallback.
- **Airlock recipe -> `AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE`** (absorbs AIRLOCK_IRIS_PARAMETRIC_RECIPE + AIRLOCK_IRIS_PARAMETRIC_OVERLAP) -> recipe library.
- **Geometry-derived-placement doctrine -> `FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL`** (absorbs CURVE_FOLLOW, SINGLE_PART_SURFACE_MESH, HYBRID_SCENE as contracts; CONNECTED_PIECE_CURVATURE_GRAMMAR cross-linked).
- **Visual-intake/learning-capture -> `SELECTIVE_VISUAL_MEMORY_POLICY`** (absorbs VISUAL_REFERENCE_INTAKE, SELECTIVE_VISUAL_MEMORY_POLICY, SELECTIVE_VISUAL_MEMORY_POLICY, CREATIVE_USE_CASE_LOGGING, PART_BEHAVIOR_LEARNING) with lanes: creative->catalog, mechanics->part-map, image-triage.
- **Proof-of-application family -> `SYSTEMATIC_FAILURE_CAPA_PROTOCOL` + banner + receipt** (PROTOCOL_BANNER_HARD_FAIL, TRACEABLE_PROTOCOL_VERIFICATION, VALIDATED_LOGIC_REUSE, PROTOCOL_RECEIPT_EVIDENCE, BUILD_COMPLIANCE_MANIFEST).
- **AI-visual-review system -> `AI_CAPTURE_COMPLIANCE_CONTRACT`** (absorbs BLENDER_VISUAL_FEEDBACK_HARNESS, AI_REVIEW_BUNDLE_INTAKE).
- **Variant rule -> `RECIPE_PARAMETERIZATION_PROTOCOL`** (absorbs CONTROL_TO_VARIANT).
- **Script-actually-built -> `VALIDATION_GATE_HARDENING_RULE`** (absorbs BLENDER_RUNTIME_BUILD_SCRIPT).
- **Routing gate -> `REQUEST_ROUTER_CHECKLIST`** (folds REQUEST_ROUTER_CHECKLIST).
- **Relocations:** STAIR_PLACEMENT_DOCTRINE -> stair doctrine; PROHIBITED_AND_PLACEHOLDER_OBJECTS + PIPE_BUBPIPE_CONTEXTUAL_CONNECTOR -> negative-knowledge; PROMPT_TO_FEATURE_ROUTER + RECIPE_CONFORMANCE -> process.
- **Reference (not rules):** ISSUE_FIX_LIBRARY, PLUGIN_VERSION_AND_ENVIRONMENT, PART_USE_CASE_CATALOG.
- **Family rules -> findings:** migrate finding families (B_SHL_E glow, B_WNG_A electric FX, TURRET beam, design families) into `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json`; retire placement families incl. arch-mirror; reconcile catalog/index.

## Each staged merge, when executed, must
1. Concatenate the distinct content of the absorbed docs into the survivor (no content dropped; preservation constraints above).
2. Delete the absorbed files; remove their RPAM + ledger entries; repoint every backtick reference to the survivor.
3. Keep the survivor's scope correct so the resolver surfaces it.
4. Re-run `release/release_check.py` to PASS (it now includes the classification gate, dangling-ref scan, version-callout gate).

## How to audit this wave
- Run `python3 release/release_check.py` — expect RELEASE GATE: PASS.
- Run `python3 validation/rule_classification_check.py` — expect PASS (92 rules classified).
- Run `python3 validation/part_context_resolver.py --ids S_WALLM --intent test` — confirm universal rules surface.
- Spot-check the two folds: the absorbed content is present as a named section in the survivor; the folded files are gone; no dangling refs.
- Read `data/RULE_CLASSIFICATION.json` to verify each verdict against the doc content.
