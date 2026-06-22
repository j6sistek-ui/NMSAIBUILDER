# DEEP RUNTIME AUDIT — validation / toolkit / library

Evidence-driven follow-up to the package deep dive, scoped to the largest remaining active category: **tooling that executes**. Methodology is the same reachability tracing that produced P1–P4: trace each file's *actual execution role* (invocation by `run_gate.py` / `release_check.py` / the upload-pack builder, cross-imports, self-tests, doc reading-paths), then classify used vs not used. Repeatable via `python3 validation/runtime_reachability_audit.py` (now reports validation tiers + toolkit + library) and the new `validation/VALIDATION_INDEX.json` (per-script tier of record, drift-checked).

---

## A. `validation/` — the execution-tier map (the core question answered)

26 scripts, classified by what actually invokes them:

| Tier | Count | What it means | Scripts |
|---|---|---|---|
| RUNTIME_ORCHESTRATOR | 1 | the build-time gate entry | `run_gate.py` |
| BUILD_GATE | 8 | invoked by `run_gate`; a build can't PASS without it | `ai_capture_compliance_check`, `build_sheet_check`, `capa_escalation`, `compliance_manifest_check`, `feature_recipe_lookup_check`, `intent_graph_conformance_check`, `recipe_conformance_check`, `validated_logic_reuse_check` |
| RUNTIME_LIB | 1 | imported by build-runtime code | `part_context_resolver` |
| RELEASE_SELFTEST | 14 | run by `release_check.py` every release; validates the *package*, not a build | `ai_review_bundle_check`, `blender_runtime_script_check`, `build_objective_conformance_check`, `discover_by_quality_check`, `geometry_construction_manifest_check`, `onboarding_gauntlet_check`, `open_topics_structure_check`, `partmap_storage_check`, `placement_intelligence_infrastructure_check`, `protocol_banner_check`, `request_router_check`, `rpam_coverage_check`, `rule_classification_check`, `version_callout_check` |
| AUDIT_TOOL | 2 | advisory, on-demand (not gating) | `runtime_reachability_audit`, `NMS_BUILD_USE_CASE_MINER` |
| REDUNDANT | 0 | capability fully covered by a BUILD_GATE | (was `NMS_NONUNIFORM_SCALE_SCANNER`) |

**Finding:** the auditor's hypothesis is correct and now quantified — `validation/` *is* the largest active category, but it is **not** bloated: 10 of 26 are build-runtime, 14 are release-tier self-tests that genuinely execute each release, and only one was dead. The real gap was that the runtime/test/historical distinction was **implicit**. `VALIDATION_INDEX.json` now makes it explicit and the audit flags DRIFT if any future script is untiered.

**Executed:** purged `NMS_NONUNIFORM_SCALE_SCANNER.py` (its non-uniform-scale check is enforced by `run_gate` + `PROHIBITED_AND_PLACEHOLDER_OBJECTS`) and repointed its doc line in `02_GENERATOR_CONTRACT.md` to the enforced gate.

**Kept with reason:** `NMS_BUILD_USE_CASE_MINER.py` is retained as an AUDIT_TOOL — unlike the scale scanner it has no gate equivalent; it mines base-JSON exports to grow the single creative store (ties to the discover_by_quality coverage topic).

---

## B. `toolkit/` — all reachable

Every toolkit file has a live reference: `PLACEMENT_RECIPE_LIBRARY.json` (19), `.md` pointer (9), the two `VISUAL_BUILD_TOOLKIT_*` techniques (1–2), and `nms_ai_review_bundle_addon_v04.py` (1, wired last release). No orphans, no action.

---

## C. `library/` — one orphan, one wired

- **Wired this pass:** `NMS_PLUGIN_ENVIRONMENT_v50.json` was refs=0 but holds unique provenance (2,097 part-definition count, 26-new-vs-v49 ObjectIDs, prohibited generated objects, source-zip). Rather than purge provenance, it's now referenced from `02_GENERATOR_CONTRACT.md` (reachable).
- **Proposed (not executed — partmap-sensitive, so careful):** `library/nms_master_part_map_verified_data_v3_01_02.csv` is refs=0 — the runtime reads the `.json` twin (7 refs). It's a convenience export nothing queries. Safe to purge after confirming `partmap_storage_check` doesn't expect it; deferred to a deliberate step rather than executed blind.
- The big partmap/dimension data (`v3_01_02.json` ×7 refs, `nms_part_dimensions_and_rules_updated.json` ×14) is firmly live — keep.

---

## D. One Creative Store (the auditor's "biggest remaining win")

**Evidence:** the two systems are **complementary, not duplicate data**:
- `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` — the **runtime** store: findings, motifs, discover_by_quality, recipes, fit_rules. Queried at build time by `part_context_resolver`, `discover_by_quality_check`, `placement_intelligence_infrastructure_check`.
- `rules/PART_USE_CASE_CATALOG.json` — creative **ideation reference**: 16 seed use-cases, visual/video reference examples, project case studies. Only *cited* (not data-consumed) by the gothic run.

The real problem was that both presented as "the creative store," inviting drift.

**Executed (safe):** declared `CREATIVE_USE_CASE_AND_STYLE_INDEX.json` the single **store of record** (new findings/use-cases log there) and `PART_USE_CASE_CATALOG.json` a **subordinate ideation reference** that feeds it — via explicit `store_of_record` / `role` headers in both. This ends the "two competing stores" ambiguity with zero data loss.

**Proposed (evidence-driven next step):** fold the catalog's 16 seed `use_cases` into the index's `discover_by_quality`/findings so the queryable creative content lives in exactly one file, then slim the catalog to pure visual/video/case-study reference. This is the larger win but a 43KB migration touching ~10 doc references, so it should be a deliberate gated step, not bundled here.

---

## E. Recommendation (matching the external assessment)

The easy reductions are captured; the runtime/test/historical split is now **objective and maintained** (`VALIDATION_INDEX.json` + drift check). The next reductions are the two deferred, evidence-backed items above — the catalog→index `use_cases` merge and the partmap `.csv` purge — each done deliberately and gate-verified. Run `runtime_reachability_audit.py` each release; target 0 true orphans and 0 DRIFT.
