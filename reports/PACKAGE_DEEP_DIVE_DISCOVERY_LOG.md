# PACKAGE DEEP-DIVE DISCOVERY LOG & ACTION PROPOSAL

> **EXECUTION STATUS (5.10.00):** The P1-P4 proposal in section B has been EXECUTED. P1 (v3_01_01 ~6MB + placeholder stubs purged, provenance repointed), P2 (one recipe method: store=PLACEMENT_RECIPE_LIBRARY.json, canonical wiring=MASTER_BUILD_RECIPES, wired into START_HERE), P3 (obsolete unreferenced docs purged after lesson extraction; resolver stamp dynamic; templates/recall-title de-versioned), P4 (build-guard snippets purged — capabilities already in run_gate). `archive/` removed entirely. Remaining open: one-creative-store single-sourcing and promoting the version-callout WARN->FAIL (tracked in OPEN_TOPICS_LOG.md).

A file-by-file analysis of every area outside `rules/` (reports, templates, data, toolkit, schemas, library, runs, transfer_prompts, release, root docs), classifying each file by **runtime reachability** and **currency**. This pass executed the provably-safe, gate-verified cleanups and records the rest as an actionable proposal. Nothing was deleted — archived files moved to `archive/` (reversible).

---

## A. EXECUTED THIS PASS (lossless, gate-verified)

All moves are to `archive/`; the release gate passed after the batch.

- **14 true orphans** (referenced nowhere in code or docs, per `validation/runtime_reachability_audit.py`) → `archive/orphaned/`: stale validation snippets/templates (`NMS_SCRIPT_LINTER.py`, `NMS_HARD_GUARD_SNIPPET.py`, `NMS_SAFE`/`CASTLE` starters, `NMS_JSON_STUDY_Jurassic_*` incl. a `_REVISED` duplicate, `NMS_JSON_TO_PYTHON_RECREATION_TEMPLATE_v53.py`, `NMS_RUNTIME_OBJECT_AUDIT_SNIPPET.py`, `NMS_VALIDATE_TEXT_BLOCKS_IN_BLENDER.py`, `stair_semantic_float_gate.py` [proposed, never adopted], and superseded templates `LESSON_PROMOTION`, `PROJECT_CONTEXT`, `OPEN_ISSUES_CURRENT`, `PROJECT_STATE_CURRENT`).
- **Historical gate-output reports** (24 `.txt`: every `*_RELEASE_GATE_REPORT.txt` and the `3.01.x` check snapshots) + **2 superseded transfer reports** (`PROJECT_TRANSFER_SUMMARY_5.04.02`, `WAVE1_RULE_REVIEW_TRANSFER`) → `archive/reports/`. **reports/ went 33 → 7** (kept: PIPE/BUBPIPE evidence ×3, NONSNAP study, RUNTIME_REACHABILITY, WAVE2, WAVE3).
- **28 old `RELEASE_NOTES_*.md`** (kept only the current `5.08.01`) → `archive/release_notes/`. The gate only requires the current one; VERSION_LOCATIONS explicitly excludes historical notes.
- **`library/nms_full_partmap_extraction_records_combined_v3_01_01.csv`** (20,921 rows, 0 active refs) → `archive/library/`.
- **Creative-index stub:** repointed `placement_intelligence_infrastructure_check.py` from `CREATIVE_USE_CASE_AND_STYLE_INDEX_STUB.json` to the full index, then archived the stub (it was an existence-only requirement; nothing read its content).

Net: active surface materially reduced, all reversible, gate PASS.

---

## B. ACTION PROPOSAL — remaining gaps

### P1 — high value, low risk
1. **Superseded partmap data `v3_01_01` (~6 MB).** `library/nms_master_part_map_verified_data_v3_01_01.json` (4 MB) + `.csv` (2 MB) are superseded by `v3_01_02` (what `run_gate` uses). Two active refs remain: `data/PART_PLACEMENT_AID_LEDGER.json` (provenance) and `library/NMS_VERIFIED_PARTMAP_UPDATE_SUMMARY_v3_01_00.md` (a historical summary). **Action:** repoint the ledger provenance to `v3_01_02` (or add a one-line "superseded by" note), archive the v3_01_00 summary, then archive the `v3_01_01` `.json`/`.csv`. Verify `run_gate` + partmap drift still pass. Largest remaining size win.
2. **Old checkpoint workflow is superseded** by `OPEN_TOPICS_LOG.md` + `CHAT_TRANSFER_CURRENT.md`. `PROJECT_STATE_CURRENT.md` and `OPEN_ISSUES_CURRENT.md` literally describe themselves as "placeholder continuity artifact created during 5.04.03 ... so transfer references resolve." Their templates are already archived. **Action:** drop the two root stubs from `VERSION_LOCATIONS.json`, remove the transfer refs that point at them, archive them. (Update the registry first so the version cascade doesn't look for them.)
3. **`PROJECT_TRANSFER_REQUIREMENT.md`** is a single sentence duplicating `PROJECT_TRANSFER_SUMMARY_RULE` + the standing CHAT_TRANSFER requirement. **Action:** fold into the rule and retire.

### P2 — reconciliation / consistency
4. **`toolkit/PLACEMENT_RECIPE_LIBRARY` json vs md out of sync:** json `schema NMS_PLACEMENT_RECIPE_LIBRARY_v2_06_01`, md title `v2.06.00`. **Action:** declare the json the source of truth (it's the data the resolver reads), regenerate or bump the md, add a sync note. Consider a small sync check.
5. **Bootstrap entry-point sprawl:** `00_START_HERE_CURRENT.md`, `transfer_prompts/NMS_BUILDER_BOOTSTRAP_CURRENT.txt`, `CUSTOM_GPT_BOOTSTRAP_PROMPT.md`, and `transfer_prompts/CHAT_TRANSFER_CURRENT.md` all "bring a new chat up." **Action:** declare ONE canonical onboarding entry (START_HERE) + the CHAT_TRANSFER safety net; mark the bootstrap variants as generated-from-or-retire to remove drift.
6. **`00_MEMORY_RECALL_INDEX` `.json` vs `.md`:** confirm one authoritative; the `.json` appears vestigial (the `.md` is what's referenced).
7. **One creative store** (already in OPEN_TOPICS_LOG): reconcile `PART_USE_CASE_CATALOG` vs `CREATIVE_USE_CASE_AND_STYLE_INDEX.json` to a single source.

### P3 — version hygiene (active docs carry stale PACKAGE-version strings; the gate only WARNs)
8. **De-version or register-as-historical** these active docs: `01_MASTER_REFERENCE.md` (5 distinct), `CUSTOM_GPT_BOOTSTRAP_PROMPT.md` (4), `MASTER_LESSONS_LEARNED.md` (4), `README.md` (4), `00_MEMORY_RECALL_INDEX.md` (3), `02_GENERATOR_CONTRACT.md`. **Caution:** keep legitimate plugin/Blender environment versions (`6.4.1`, `5.0.1`, `5.1.1`) — only the package-version triples are drift. After cleanup, consider promoting the version-callout gate from WARN → FAIL so this can't re-accumulate.
9. **Templates with stale `source_docs_rev: 4.02.00`:** `ASSEMBLY_CONFORMANCE_PLAN`, `BUILD_PLACEMENT_SNAPSHOT`, `PLACEMENT_METHOD_SUMMARY`, `PLACEMENT_SESSION_RECEIPT`. **Action:** update to current or de-version (they're templates, so a token like `<rev>` is cleanest).
10. **Resolver stamps a hardcoded `generated_from_rev: "5.04.00"`** (and `schema PROJECT_BUILD_PLACEMENT_PACKET_1.1`) into every packet. **Action:** read the current version from `release/VERSION.json` so packets are self-dating.

### P4 — reachability frontier (measure value by execution path, not file count)
11. **WIRE-vs-ARCHIVE for the archived build snippets.** `NMS_SCRIPT_LINTER`, `NMS_SAFE_STARTER_TEMPLATE`, `NMS_HARD_GUARD_SNIPPET`, `NMS_NONUNIFORM_SCALE_SCANNER` are genuinely useful build-time tools that were simply unreachable (nothing pointed to them). Decide per-file: either **wire** them into `00_START_HERE_CURRENT.md` / `00_OPERATING_CARD.md` as named build-time tools (giving them a reading path), or leave them archived. Don't leave useful tools half-present.
12. **Track reachability as a release metric.** `validation/runtime_reachability_audit.py` is advisory; run it each release with a target of 0 true orphans, and route point-in-time gate outputs to `archive/` automatically so `reports/` stays current-only.

---

## C. Do-not-break list (verified active during the dive)
- `library/nms_master_part_map_verified_data_v3_01_02.json/.csv` — the live verified partmap (`run_gate`).
- `library/nms_part_dimensions_and_rules_updated.json` (~230k lines) — the authoritative 2,097-part library.
- PIPE/BUBPIPE evidence: `data/PIPE_BUBPIPE_*` + the 3 PIPE reports — evidence base for the negative-knowledge exception.
- `schemas/*` + placement `templates/*` receipts — required by `placement_intelligence_infrastructure_check.py`.
- `toolkit/validated_recipes/{c_trifloor.py, stairs.py}` — reachable (referenced); keep.
- `data/RUNTIME_BEHAVIORS.json` (23 behaviors), `data/RULE_CLASSIFICATION.json`, `data/RULE_PART_APPLICABILITY_MAP.json` — the Wave 3 runtime spine.

---

## D. Suggested execution order
P1 (size + supersession wins, gate-verified) → P2 (reconcile to single sources) → P3 (version hygiene + promote gate to FAIL) → P4 (wire-back the useful tools, make reachability a tracked metric). Each step is independently gate-checkable; bank clean releases rather than batching.
