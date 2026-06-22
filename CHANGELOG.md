# CHANGELOG — NMS master docs
## 5.19.03 — Lighting/effect part data + placement-promotion runbook repair (2026-06-22)

- Repaired the failed 5.19.02 placement-promotion candidate by adding the end-to-end trial-result -> existing store -> resolver/build-sheet runbook to `rules/RULE_UPDATE_PROTOCOL.md`.
- Added user-supplied lighting/effect behavior to `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json`, including color-responsive emitters, fixture-tint-only cautions, wall-light color variants, SET_CLASS beam-cone composition, Race Booster purple glow, Planet Holo display effect, Base Shell colorable display, Corvette animated shield effects, and SWARM_TROPHY color variants.
- Added provisional JSON-only part data for `SWARM_TROPHY_G`, `SWARM_TROPHY_B`, `SWARM_TROPHY_R`, and `B_SHL_D` without hand-editing the verified extraction overlay.
- Updated `part_context_resolver.py` so effect findings are reachable in `CREATIVE_CONTEXT.part_effect_findings` and non-verified ObjectIDs can surface dimensions-library fallback geometry with explicit authority warnings.
- Regenerated placement-map sheet/index/worklist/status and `discover_by_quality`; refreshed open topics and transfer prompt.


## 5.19.00 — full per-part reconciliation into the build sheet
- part_context_resolver.py: placement_spec now reconciles ALL per-part sources into one record — geometry (verified-map origin/bbox/FBX anchor), orientation (+ master-CSV phase/pivot + override), scale (+ behavior), placement_rules (snap + fallback + local axis rules + neighbor offsets + fitment + recipes), family, characteristics, method authority, role, cautions. Each section carries _source provenance + an overall validation block (geometry/orientation/scale status from the verified map; placement-trial-layer status from the master CSV) so unvalidated data is visible. Ties in nms_master_part_map_verified_data_v3, part_placement_master_sheet.csv, CREATIVE_USE_CASE_AND_STYLE_INDEX, METHOD_AUTHORITY_TABLE. connections_TODO flags cross-plane composed transforms as the next pass.

## 5.18.00 — consolidated per-part build-sheet hand-off (placement_spec)
- part_context_resolver.py: every part now carries MANDATORY parts[oid].placement_spec — orientation (rotation + RX90/RY90/RZ90 footprints + override flag), scaling (world size at 0.5/1.0/1.5/2.0), placement (concrete snap + SpacingRule fallback + guidance + ring formula + recipes), role, cautions. Folds in the 5.16/5.17 curated-guidance and snap dicts. Mapped from existing library data; build_sheet integrity preserved.

## 5.17.00 — concrete per-part snap spacing
- part_context_resolver.py: forwards CREATIVE_CONTEXT.per_part_snap_spacing — concrete cardinal-face snap steps per snappable part (lateral_step_x / lateral_step_z / vertical_step_y) from relational_map_combined_v01.json. S_WALLM 5.3379 / 3.33, S_FLOOR_Q 2.6423. Cardinal-only so IN/OUT/UP/DOWN points don't inflate the step; diagonal walls (no cardinal faces) fall back to SpacingRule. spacing_authority_note updated to point at the numbers.

## 5.16.00 — resolver forwards curated guidance + template-leak gate
- part_context_resolver.py: forwards dimensions-library curated guidance (SpacingRule, PlacementGuidance, LikelyRole, ring formulas, KnownIssues, MechanicsUseRecommendation, LessonNotes) as advisory CREATIVE_CONTEXT; adds spacing_authority_note (snap supersedes extent SpacingRule). MANDATORY mechanical block unchanged.
- run_gate.py: template-leak check — stray TPL_ to export / 2+ distinct ObjectIDs at origin now FAIL the gate.
- 02_GENERATOR_CONTRACT.md + runs/gothic_church_v01.py: delete templates before export; cleanup also purges stale TPL_.

## 5.15.00 — onboarding reuse-gate dead-end fix + orientation authoring caution

- **Onboarding spec (ONBOARDING_VALIDATION_BUILD.md + 00_KICKOFF_INTAKE_GATE.md):** the floor/wall/roof gauntlet now includes one `S_RAMP` (a placement-map proof-ledger part). The validated-logic-reuse gate is auto-required for every build-type request and FAILS on zero proof-ledger parts; floor/wall/roof are not in the ledger, so a new chat following the old spec dead-ended. Adding one ledger part clears the gate and makes the gauntlet actually exercise validated-logic reuse.
- **Orientation authoring caution (02_GENERATOR_CONTRACT.md):** documents that the orientation gate enforces each part's default rotation on RX/RY (~90deg); flat-stacking at rx=0 fails it unless declared via `ORIENTATION_OVERRIDE_IDS` / `PART_ORIENTATION_OVERRIDES.md`. RZ/facing is always free.
- **Open (owner decision pending):** whether the reuse gate's zero-proof-part FAIL should be relaxed to N/A for all builds (not just onboarding), so simple real builds without a ledger part aren't forced to include one. Not changed this release.
- No new files (anti-bloat guard #28 intact).


## 5.14.00 — design-intent + orientation quality gates (v4 placement-quality regression fix)

- **Design-intent gate (NEW, auto-required for build-type):** generated builds must declare `DESIGN_INTENT` before placement — per assembly `is_a` + `target_read` + `style_source` (from `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json`), and **every used ObjectID must carry a purpose**. A part placed with no declared purpose FAILS the gate. Promotes design intent out of the advisory CREATIVE_CONTEXT into a required, checkable surface. Documented in `02_GENERATOR_CONTRACT.md`; modeled in `runs/gothic_church_v01.py`.
- **Orientation gate (NEW, build-type only):** flags any part rotated off its `DefaultRotationDegrees` on RX/RY without authorization (override doc entry or declared `ORIENTATION_OVERRIDE_IDS`). RZ/facing is always free. JSON-recreation builds are exempt — working transforms are authoritative and outrank defaults. Catches the `gothic_castle_v02` tilted-roof/odd-angle failure.
- **Recipe routing:** existing spire/taper recipes are now routed via `FEATURE_RECIPE_ROUTE_INDEX` (`gothic_spire_and_tower_crown`) — they existed but were unreachable. `flying_buttress` routes to a `NO_VALIDATED_RECIPE` guard + a `FLYING_BUTTRESS` entry in `NEGATIVE_KNOWLEDGE_INDEX` (stops S_RAMP-as-buttress).
- **Curve-follow contract:** re-absorbed from v4's `CURVE_FOLLOW_TRANSFORM_PROPAGATION_PROTOCOL` into `CONNECTED_PIECE_CURVATURE_GRAMMAR.md` as an enforceable `CURVE_FOLLOW_CONTRACT` (disciplines spires/rings/ribs into controlled propagation, not random stamping).
- v4 study confirmed: authoritative snap data was preserved byte-identical and is better wired; the regression was unrouted recipes + ungated design intent, not lost data. No new files (anti-bloat guard #28 intact).


## 5.13.00 — connectivity extents fallback + baked-hidden hand-off guard

- **Connectivity robustness (validation/run_gate.py):** the connectivity / no-float gate now falls back to `library/nms_part_dimensions_and_rules_updated.json` for geometry extents when the supplied `<library>` arg carries none (e.g. the verified part map, which has snap/role data but no `extent_x/y/z`). Connectivity runs regardless of which library was passed instead of reporting `SKIPPED (no extents in library)`. Skip reason reworded; a note prints when extents came from the fallback.
- **Baked-hidden lint (gate FAIL):** new static-linter check `no baked-hidden collections/parts` — a delivered build script containing `hide_viewport = True` or view-layer `exclude = True` (flags that resist `Alt+H`) now FAILS the machine-checkable gate. Review-time isolation must use the review addon's recoverable `hide_set()`. New rule in `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md` (hand-off visibility).
- **Coverage note clarified:** part-placement-map coverage is reworded as a separate proof ledger (map-only proof + sign-off), explicitly NOT the verified-partmap geometry status — parts absent from it are still valid to use.
- **Operating card:** names `nms_part_dimensions_and_rules_updated.json` as the gate `<library>` arg and explains the partmap-has-no-extents distinction.
- No new files; all fixes routed into existing files (anti-bloat guard #28 intact).


## 5.12.00 — new-data intake routing + anti-bloat new-file guard

- **Intake routing (rules/RULE_UPDATE_PROTOCOL.md):** user-provided recipes/part-characteristics route into the existing store of record, runtime-linked, never a new file/report. Recipe -> PLACEMENT_RECIPE_LIBRARY.json + FEATURE_RECIPE_ROUTE_INDEX + JSON_RECIPE_SIGNATURE_INDEX (+ RUNTIME_BEHAVIORS if assembly), scoped by intent keywords. Part-characteristics -> CREATIVE_USE_CASE_AND_STYLE_INDEX.json. Includes the written rule-vs-finding test.
- **Anti-bloat gate #28:** `validation/new_file_guard_check.py` + `release/APPROVED_FILES.json` — any shipped file not in the manifest (or an approved pattern) FAILS the release; new files require explicit user approval recorded in the manifest.
- Kickoff intake gate now points new-data handling at the routing rule.
## 5.11.00 — deep runtime audit (validation / toolkit / library)

- **Validation tiering:** added `validation/VALIDATION_INDEX.json` (1 orchestrator, 8 build gates, 1 runtime lib, 14 release self-tests, 2 audit tools); `runtime_reachability_audit.py` now reports tiers + library + flags DRIFT.
- **Purged:** `NMS_NONUNIFORM_SCALE_SCANNER.py` (REDUNDANT — enforced by run_gate + PROHIBITED rule).
- **Wired (refs=0 but valuable):** `library/NMS_PLUGIN_ENVIRONMENT_v50.json` provenance into the generator contract.
- **One creative store:** declared `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` the single STORE OF RECORD; `rules/PART_USE_CASE_CATALOG.json` is now a subordinate ideation reference (headers added).
- **Deferred (evidence-backed):** catalog->index `use_cases` merge; partmap `.csv` purge. Report: `reports/RUNTIME_AUDIT_VALIDATION_TOOLKIT_LIBRARY.md`.

## 5.10.00 — executed deep-dive cleanup (P1-P4) + removed archive

- **P1:** repointed partmap provenance to `v3_01_02`; deleted superseded `v3_01_01` data (~6MB) and the v3_01_00 summary; retired placeholder stubs `PROJECT_STATE_CURRENT`/`OPEN_ISSUES_CURRENT` (deregistered) and folded `PROJECT_TRANSFER_REQUIREMENT` into the rule; checkpoint now refreshes `OPEN_TOPICS_LOG` + `CHAT_TRANSFER`.
- **P2 (one recipe method):** `toolkit/PLACEMENT_RECIPE_LIBRARY.json` is the single store of record; `.md` collapsed to a pointer; `MASTER_BUILD_RECIPES_AND_PLACEMENT_GUIDANCE.md` promoted to the canonical storage+utilization-wiring method and wired into START_HERE.
- **P3:** purged unreferenced obsolete docs `01_MASTER_REFERENCE.md`, `CUSTOM_GPT_BOOTSTRAP_PROMPT.md`, `00_MEMORY_RECALL_INDEX.json` (lessons extracted first); resolver packet stamp now reads `release/VERSION.json`; de-versioned 4 placement templates + the recall-index title; kept env/provenance versions.
- **P4:** purged the archived build-guard snippets — linter/hard-guard/scale-scanner/runtime-audit/safe-starter capabilities are all already enforced by `run_gate`/rules.
- **archive/ removed** entirely; package is AI-operational only.

## 5.09.00 — package deep-dive + lossless archival

- **Deep dive:** opened every file outside rules/ (reports, templates, data, toolkit, schemas, library, runs, transfer_prompts, release, root docs); findings + action proposal in `reports/PACKAGE_DEEP_DIVE_DISCOVERY_LOG.md`.
- **Lossless archival (gate-verified, moved to `archive/`):** 14 true orphans; 24 historical gate-output reports + 2 superseded transfer reports (reports/ 33->7); 28 old release notes (kept current; 29->1); zero-ref `v3_01_01` extraction records; vestigial creative-index stub (infra check repointed to the full index).
- **Tooling:** added `validation/runtime_reachability_audit.py` (advisory) — measures package value by execution-path reachability; all 62 rules map to a runtime destination.
- **Open topics:** added "Runtime reachability as the value metric" and "Package deep-dive cleanup (P1-P4)".

## 5.08.01 — scope precision + metadata hygiene

- **RPAM scope precision:** assembly/composition recipes (AIRLOCK_IRIS, DOME_STUDY, WALL_SHELL, CONNECTED_PIECE_CURVATURE, FOCAL_BUILD_GEOMETRY, CURATED_DETAIL_HIERARCHY, COMPOSITE_BUILD_INTENT_GRAPH) are now build-level, matched against the build INTENT via curated intent keywords — not part-name substrings. A plain wall no longer receives airlock/dome/wall-shell behaviors; a church no longer receives an airlock recipe. Emitted in a new `MANDATORY_PLACEMENT_CONTEXT.assembly_rule_behaviors` lane (validated by build_sheet_check). Narrowed STAIR -> [ramp, stair] and C_TRIFLOOR -> [trifloor].
- **Metadata hygiene:** CHANGELOG normalized to a single H1 with H2 version entries; FILE_INVENTORY regenerated to the actual file count; PACKAGE_MANIFEST package/purpose/release_name refreshed off the stale 5.04.03 strings.

## 5.04.09 — Harmonization Step 3: tail de-versioned, ledger to zero

## 5.08.00 — Wave 3 runtime mapping executed

- **Resolver consumes classification:** per part it now emits `applicable_rule_behaviors` ({rule_id, kind, authority, required_behavior, check, applies_to}) instead of a bare rule-name list, filtered to KEEP RULE/RECIPE/NEGATIVE only — no PROCESS/GOVERNANCE/FINDING/REFERENCE leaks into part context.
- **data/RUNTIME_BEHAVIORS.json:** authored for all 23 KEEP RULE/RECIPE/NEGATIVE rules (required_behavior + check + authority).
- **build_sheet_check:** validates behaviors — tamper-evident vs a fresh resolver run and fails on any empty `required_behavior`. All packets/fixtures regenerated with `build_application` preserved.
- **Onboarding gauntlet:** `ONBOARDING_VALIDATION_BUILD.md` promoted to a builder-readiness gauntlet (real micro-build -> first gate -> diagnose/correct on failure -> second gate -> `BUILDER READINESS` verdict); checklist marked Source-Readiness-only; enforced by gate #26.
- **discover_by_quality:** generated reverse index (quality/effect -> candidate ObjectIDs) in the creative index, sync gate #27, wired into kickoff for discovery-first selection.


## 5.07.00 — Wave 2 physical consolidation executed + Wave 3 prep

- **Consolidation executed:** 30 duplicate-law rule docs absorbed into 13 survivors, content-preserving (bodies kept as `absorbed from X` sections; `.json` sidecars preserved into survivors). Rule layer 92 -> 62 unique rules. All references repointed; gate caught and forced fixes for 6 real downstream breaks (sidecars, infra REQUIRED list, fixtures, covered build, both packets, partmap index).
- **Family rules demoted:** `rules/PART_FAMILY_RULES.json` -> `INFORMATIVE_FINDINGS_NOT_PLACEMENT_AUTHORITY`; 7 effect/use families mirrored into `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` (`part_effect_and_use_findings`); 9 placement families cross-linked to superseding mechanics.
- **OPEN_TOPICS_LOG** rewritten to the new open state; added **Priority** and **Success Criteria** fields to every topic; structure gate (#25) updated to require them.
- **Wave 3 seeded:** `data/RUNTIME_BEHAVIORS.json` (seed) + `reports/WAVE3_EXECUTION_PREP.md` (resolver-emits-behaviors plan, runtime destination map, gotchas, success criteria).


## 5.06.01 — continuity-artifact hardening

- **OPEN_TOPICS_LOG.md** restructured into the required per-topic format (Issue / Discovery / Why It Matters / Decision / Next Steps / Status / Last Updated) as the single authoritative continuity artifact; resolved history stays in CHANGELOG.
- **transfer_prompts/CHAT_TRANSFER_CURRENT.md** added — a copy-paste-ready chat transfer doc (who/what, current version, what happened/why/decided/next, critical mechanics, standing requirements).
- **Mandated** both in OPEN_TOPICS_LOG_PROTOCOL and PROJECT_TRANSFER_SUMMARY_RULE: refresh on every build/doc update and on `checkpoint`.
- **Gate #25:** validation/open_topics_structure_check.py — fails the release if any topic is missing a required field or the chat transfer doc is absent.


## 5.06.00 — rule-review wave 2: classification system + safe consolidations

- **Classification spine:** every rule now carries `kind` (RULE/RECIPE/FINDING/PROCESS/GOVERNANCE/REFERENCE/NEGATIVE) + `runtime_status` (KEEP/CONSOLIDATE/FOLD/RELOCATE/...) in `data/RULE_PART_APPLICABILITY_MAP.json`, mirrored with dispositions in new `data/RULE_CLASSIFICATION.json`.
- **Enforcement:** new `validation/rule_classification_check.py` wired as release gate #24 — release fails if any rule is unclassified or the ledger and map disagree. Enforces RULE_UPDATE_PROTOCOL mechanically.
- **Folds (content preserved):** DELTA_LEARNING_PROTOCOL -> SELECTIVE_VISUAL_MEMORY_POLICY; CONNECTED_SURFACE_NO_STEPPED_OFFSET_RULE -> CONNECTED_PIECE_CURVATURE_GRAMMAR. Removed from files/RPAM/ledger/inventory; no dangling refs.
- **Repairs:** rewrote the damaged PROJECT_CONTEXT_PROTOCOL (prior bulk edit had overwritten its bullets); de-versioned PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE prose; re-scoped GROUND_ZERO_FOUNDATION_RULE -> UNIVERSAL_PROCESS.
- **Staged (encoded as data, specs in reports/WAVE2_EXECUTION_REPORT.md):** the large multi-doc merges (JSON ladder, precedence/authority law, part-map library, proof-of-application family, visual-intake/learning-capture family, airlock recipe, geometry-derived-placement doctrine, AI-visual-review system) and the family-rules -> findings migration, each with survivor + preservation constraints.


## 5.05.00 — rule-review wave 1: resolver wiring + obsolete retirement

Execution of the first wave of the rule-by-rule review (analysis recorded in reports/ and the mapping/wiring log).

- **Wiring:** advertised the per-build part-context resolver (`validation/part_context_resolver.py`) as an explicit build step in `00_START_HERE_CURRENT.md` and `00_KICKOFF_INTAKE_GATE.md`, with creative-review-first part discovery. Foundational rules now actually reach builds instead of depending on a chat looking them up.
- **Re-scope (surfacing fix):** `VERIFIED_PARTMAP_DATA_PROTOCOL`, `ASSEMBLY_CONTEXT_SUPERSEDES_COMPONENT_CONTEXT_RULE`, `OBJECT_USE_RECORDING_PROTOCOL`, `BUILD_PLACEMENT_SNAPSHOT_PROTOCOL` -> `UNIVERSAL_PROCESS` (were PART_SPECIFIC/NEEDS_REVIEW, surfacing for few/no parts). `CONTINUOUS_PATH_ASSEMBLY_RULE` -> `FAMILY_OR_ASSEMBLY` with path keys (was PART_SPECIFIC/1 with dead family tokens). Cleared dead family tokens on the re-scoped entries.
- **Retired (obsolete):** `PIPE_BUBPIPE_VALIDATION_EXCEPTION_RULE` (3.01.01) — self-superseded by `PIPE_BUBPIPE_CONTEXTUAL_CONNECTOR_RULE` (3.01.02); removed both files and its RPAM entries; repointed references (kickoff, FILE_INVENTORY, placement-aid ledger) to the surviving connector rule.
- Larger content-preserving consolidations (JSON ladder, precedence/authority, part-map library, airlock recipe, geometry-derived-placement family, creative learning merges, family-rules -> findings migration) are queued with preservation constraints in the wave-1 transfer summary for careful execution.


- De-versioned the remaining 54 governance/active-build docs (kickoff gate, execution kernel, recipe library, master reference, and the rules/ tail). Stripped every `## X.YY.ZZ` section header to its current topic; preserved topic text and build-iteration provenance (V24/V38/V42, which are not package versions).
- `rules/DOME_STUDY_LESSONS.md` rewritten by hand to honor its own supersession note: leads with the proven measured `DOME_RADIAL_RING_TAPER` method and demotes the earlier qualitative 'rings don't make a dome' caveat and the `S_WALLM_H` shell to one stylistic option.
- Fixed the `## 5.00.00` header previously introduced in `00_KICKOFF_INTAKE_GATE.md` and `PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md`.
- Version-callout ledger: 118 -> 0. Every governance/active-build doc now reads as current state; the gate holds an empty ledger and fails any future version-section call-out. Version bump to 5.04.09. Release gate: PASS.


## 5.04.08 — Harmonization Step 2: router trio de-versioned, single bundle map

- De-versioned `rules/REQUEST_ROUTER_CHECKLIST.md`, `RULE_APPLICATION_MATRIX.md`, and `02_GENERATOR_CONTRACT.md` (40 `## X.YY.ZZ` sections removed across the three).
- Collapsed the triplicated per-feature routing into ONE authoritative bundle map in the router checklist (option A). The matrix now points to the router for routing and keeps only matrix-unique content (phase tiers, Corvette boundary audit, JSON recreation/study, version continuity). The generator contract is reorganized into themed current clauses with every technical specific preserved (banned calls, the COORD_MODE stack, wrapper resolution, the canonical dual-gate invocation, curvature fields, Corvette 95/100m whole-assembly audit).
- Resolved 4 stale routing targets to real current homes: the two spire notes -> `CONNECTED_PIECE_CURVATURE_GRAMMAR.md` + `MASTER_LESSONS_LEARNED.md`; the airlock skeleton -> the three `AIRLOCK_IRIS_*` rules; `POWER_UTILITY_EXCLUSION_RULE.md` (never existed) -> `UNIVERSAL_RULES.md` + the generator `INCLUDE_POWER_UTILITY=False` default.
- Ledger: 158 -> 118 call-outs (57 -> 54 files). Version bump to 5.04.08. Release gate: PASS.


## 5.04.07 — Harmonization Step 2: README de-versioned

- Rewrote `README.md` from a 27-section accreted changelog (`## 4.01.00 …`, `## 2.18.01 focus`, …) into a present-tense current-state overview organized by theme: what the package is, environment & library, how to use it, directory map, current capabilities & governance, high-level rules, and part/family exceptions.
- No current requirement was dropped; the substance of every version section was folded into the themed body. The only contradiction removed was the stale 'current master is 2.06.01' line, superseded by the 5.04.x title. History remains in this CHANGELOG.
- Version-callout debt ledger burned down: 185 -> 158 call-outs (58 -> 57 files). README dropped to 0 call-outs.
- Version bump to 5.04.07. Release gate: PASS.


## 5.04.06 — Harmonization Step 1: single current-state source enforcement

- Added `rules/SINGLE_CURRENT_STATE_SOURCE_RULE.md`: governance and active-build docs state current requirements only; superseded statements are removed (not preserved as stale version-labeled sections); version history lives here in the CHANGELOG, with critical detail moved to `archive/` and pointed to from the relevant entry.
- Added `validation/version_callout_check.py` + `validation/version_callout_debt.json`, wired into the release gate. It FAILS the release on any NEW `## X.YY.ZZ` section call-out in a non-exempt doc, or when an existing offender gets worse. Exempt: CHANGELOG, release notes, reports/, archive/, the versioning policy, and the title/baseline anchors.
- Recorded the current debt baseline: 58 governance/active-build docs carrying 185 version-section call-outs, to be burned down to zero in Steps 2-3. No documents were de-versioned in this release.
- Registered the new rule in RPAM. Version bump to 5.04.06. Release gate: PASS.


## 5.04.05 — Adopt intended-final START HERE

- Replaced the 5.04.04 interim rewrite of `00_START_HERE_CURRENT.md` with the user's intended-final version: a clean, present-tense current-state router (no version call-outs) that adds two principles the interim lacked — `VALIDATION TARGET FIRST` (validate the requested objective, not package health or the easiest artifact) and the onboarding `protocol gauntlet` (build -> fail is acceptable -> diagnose -> correct -> re-gate -> verdict; skipping diagnosis/correction/re-gating is not acceptable).
- Mechanical gate fixes only, no content edits: restored the title version stamp and a `Current baseline` line so the two registered version-location checks resolve; unescaped the underscores in the Core Authority Files list.
- Version bump to 5.04.05 across registered locations + manifest. Release gate: PASS.


## 5.04.04 — START HERE current-state rewrite + onboarding wiring

- Rewrote `00_START_HERE_CURRENT.md` as present-tense current operating requirements. Removed the embedded per-version call-outs (`## 4.01.00` … `## 1.03.x`) that made an older release's notes read as co-equal current law; folded every still-in-force requirement into topic-grouped current sections. History remains here in the CHANGELOG.
- Wired `ONBOARDING_VALIDATION_BUILD` into the entry path: it is now named in START HERE and is a MANDATORY FIRST DUTY in `00_KICKOFF_INTAKE_GATE.md` (previously defined but referenced from nowhere).
- `ONBOARDING_VALIDATION_BUILD` is now a real, full-process micro-build: removed the 'simulated' run_gate; it runs the actual gate and emits a gate-verified compliance manifest, treated exactly like a user build.
- Version bump to 5.04.04 across registered locations + manifest. Release gate: PASS.


## 5.04.02 — Triage Governance + Project Transfer Continuity

- Added `rules/TRIAGE_REVIEW_ASSISTANCE_TOOL_RULE.md`.
  - Triage findings are review observations, not confirmed failures.
  - Triage is not placement authority, conformance authority, compliance authority, or CAPA trigger.
  - Triage output is subordinate to run_gate, exported JSON conformance, placement precedence, build packet authority, source documents, and visual evidence.
- Added `rules/PROJECT_TRANSFER_SUMMARY_RULE.md`.
  - Major deliverables should include a Project Transfer Summary.
  - `checkpoint` requests should generate `PROJECT_STATE_CURRENT.md` and `OPEN_ISSUES_CURRENT.md`.
- Added transfer templates:
  - `templates/PROJECT_STATE_CURRENT_TEMPLATE.md`
  - `templates/OPEN_ISSUES_CURRENT_TEMPLATE.md`
- Updated `00_OPERATING_CARD.md`, `00_START_HERE_CURRENT.md`, `CUSTOM_GPT_BOOTSTRAP_PROMPT.md`, and `OPEN_TOPICS_LOG.md`.


## 5.04.01 — Retire church CAPA probation + capture its lesson
- Cleared the gothic-church CAPA escalation (data/CAPA_ESCALATION_STATE.json): RETIREMENT clear (owner retired the dead project), explicitly NOT a corrective-build clear — recorded honestly in the CAPA history. run_gate is off probation.
- Encoded the lesson so it outlives the project: rules/PLACEMENT_MECHANICS_VS_CREATIVE_STYLE_SEPARATION_RULE.md gains a worked example, MASTER_LESSONS_LEARNED.md gains the church entry. Corrective logic: experimental/decorative framing never waives a required_method or negative-knowledge constraint; EXPERIMENTAL is not a bypass; never silent-skip a method the sheet surfaces (SHEET_NOT_UTILIZED).
- No gate-logic change. Builds on 5.04.00.

## 5.04.00 — Roof-build findings encoded + wired into runtime (creative surface)
- Added `data/GEOMETRIC_FAILURE_MODE_INDEX.json` (ADVISORY, non-gated): apex-swirl, outward-bulge, fan-vault-misuse, roof-tile-shingling, part-width-vs-base, tier-gap, compound-collar-collapse — each with trigger parts/patterns + fix. Kept separate from NEGATIVE_KNOWLEDGE_INDEX (which is mechanical/tier-6/gate-routed).
- Promoted `data/CREATIVE_USE_CASE_AND_STYLE_INDEX_STUB.json` -> populated `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` (the file the resolver already referenced but that did not exist): part_geometric_character, named placement_recipes (CONVERGING_RIB_CONE / CONVERGING_BEAM_CONE / COUNTER_CHEVRON_GAP_FILL / SHINGLE_INFILL / SOLID_FINIAL_CAP), orientation_recipes (lean/aim_at_apex/rib_aim + duplicate-needs-link), color_variant_families (SET_CLASS A/B/S), fit_rules, and findings 20-25.
- `validation/part_context_resolver.py`: CREATIVE_CONTEXT now LOADS those indices and surfaces, per build, `part_character` + `applicable_failure_modes` (matched to the build's parts/intent) + `placement_recipes` + `orientation_recipes` + `fit_rules`. MANDATORY_PLACEMENT_CONTEXT unchanged (mechanical only) — the firewall holds; advisory data can never fail the gate. Self-test extended (asserts the wiring populates AND does not leak into the forced surface). PASS.
- `00_OPERATING_CARD.md`: documented the populated CREATIVE_CONTEXT + a Live-build disciplines section (screenshot-verify each step; checkpoint-save/export each batch; live geometry is BLENDER-tier).
- `02_TECHNIQUE_TOOLKIT.md` + `MASTER_LESSONS_LEARNED.md`: the primitives and the root-caused failure modes.
- No gate-logic change. Evidence tier: BLENDER (visual), not GAME_VALIDATED. Open church CAPA unaffected.

## 5.03.00 — CAPA escalation (deeper manifest as a consequence of source-skipping)
- Added `validation/capa_escalation.py` + `data/CAPA_ESCALATION_STATE.json`: review-logged open/clear/status of the escalation that makes the deeper manifest a required gate. Trigger class BUILD_SHEET_FABRICATION / SHEET_NOT_UTILIZED.
- `validation/run_gate.py`: when the escalation is ACTIVE, also requires a passing `compliance_manifest_check` (declare `PROJECT_COMPLIANCE_MANIFEST`) on top of the lean builder sheet; `--capa-state <path>` override; folded into the verdict.
- `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md`: added the source-skipping escalation section (open -> deeper required -> clear after corrective build + prevention). Operating card updated.
- Self-tests wired into the release gate (capa_escalation --self-test; run_gate active-escalation-requires-manifest).

## 5.02.00 — Build-sheet gate (generated packet enforced at run_gate)
- Added `validation/build_sheet_check.py`: verifies COVERAGE (every used ObjectID has a builder-sheet entry), POPULATED (non-empty AI build_application + resolved data), and INTEGRITY (mechanical fields match a fresh resolver run — tamper-evident).
- `validation/part_context_resolver.py`: each part entry now carries a `build_application` placeholder the AI fills.
- `validation/run_gate.py`: parses PROJECT_BUILD_SHEET + BUILD_SHEET_USED; requires/enforces the builder sheet (pre-build, respects the 5.01.01 phase split); folds the result into the verdict; `--build-sheet <path>` override.
- Both self-tests wired into the release gate (build_sheet_check --self-test; run_gate covered-PASS / uncovered-FAIL fixtures).
- The builder sheet replaces the hand-written manifest at the gate; `compliance_manifest_check.py` remains an OPTIONAL deeper tool. Operating card + bootstrap updated to the lean loop.

## 5.01.01 — run_gate phase-ordering fix (deferred post-build JSON checks)
- `validation/run_gate.py`: recipe-conformance and intent-graph gates no longer FAIL a pre-build script that merely uses conformance/intent-graph parts when no exported NMS JSON is supplied. They now report DEFERRED (post-build), the verdict passes at SCRIPT_VALIDATED with JSON validation pending, and a tier notice is printed.
- When an exported JSON IS supplied (`--require-conformance`/`--require-intent-graph <exported.json>`), the checks run and can FAIL exactly as before — enforcement preserved, moved to the correct phase.
- Root cause: the gate demanded a post-build artifact during the pre-build pass, so the generated Python could never pass run_gate.

## 5.01.00 — Operational reachability (resolver + project packet + operating card + hardened gate)
- Added `00_OPERATING_CARD.md`: the single always-hold page (build loop, precedence tiers, mechanical-vs-creative firewall, banner).
- Added `validation/part_context_resolver.py`: resolves intended ObjectIDs into a small PROJECT BUILD PLACEMENT PACKET (MANDATORY_PLACEMENT_CONTEXT forced / CREATIVE_CONTEXT offered). The AI builds from the packet, not the 300-file library.
- Added `data/RULE_PART_APPLICABILITY_MAP.json` (RPAM): all 113 rules mapped to the parts/families they govern (54 family/assembly, 26 universal-process, 19 part-specific, 6 creative, 8 needs-review) + `validation/rpam_coverage_check.py`.
- Hardened `validation/compliance_manifest_check.py`: now re-reads cited sources and verifies source_ref-in-file, ObjectID-in-file, tier highest-applicable (snap beats partmap; negative-knowledge overrides; recipe tiers require a verifiable ref), and method authorization per part/context.
- Wired resolver self-test + RPAM coverage into the release gate.


## 5.00.00 — Placement-precedence constitution + gate-verified build compliance (MAJOR)

THE LAW. Precedence resolution is now an explicit first-duty workflow step, not a
reference file. Every build (generated Python OR live Blender — parity rule) must
emit a BUILD COMPLIANCE MANIFEST and PASS validation/compliance_manifest_check.py;
no verified manifest = invalid build. New: 00_FOUNDATIONAL_DOCTRINE.md,
rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md, rules/BUILD_COMPLIANCE_MANIFEST_RULE.md,
rules/BLENDER_PARITY_RULE.md, rules/PART_DATA_AUTHORITY_STATEMENT.md (FBX demoted to
last-resort fallback), rules/SESSION_ONBOARDING_CHECKLIST_RULE.md (READ/SKIPPED
onboarding output), schemas/BUILD_COMPLIANCE_MANIFEST.schema.json, template, and the
executable verifier wired into the release gate. Banner now carries a router+precedence
receipt. Promoted 5.00.00 non-snap build-study findings: 6 null-spawn parts added to
negative knowledge (FOS_LIMBS/SKULL/TAIL, SET_B_MONU_FA, SET_LZ, SET_SFXCONST_S0).


## 4.03.00 — Reference-Build Findings Batch (Levers, Recipes, Part Behavior)

- Recognizability levers logged in the creative index: hyper-dense focal showpiece (#10), low-budget silhouette variety (#15), canonical-proportions+placement+color (#18), gap-closing densification finish (#19).
- Added placement recipes: tapered_shaft_stacked_cylinders, spiral_stair_from_wall_panels, bladed_weapon_panel_stack, bladed_weapon_graded_canister_cluster, radial_emissive_fan_set_class; routed in FEATURE_RECIPE_ROUTE_INDEX (bladed_weapon, spiral_staircase, tapered_shaft, radial_emissive_fan).
- Part behavior: SET_CLASS A/B/S emissive beam (class-locked color A=purple/B=blue/S=yellow, beam scales with uniform scale, follows rotation, night-vivid) GAME_VALIDATED; rigid-part JSON transform convention (At=unit, scale=|Up|, Y-up) confirmed across 5 builds; walkable rise ~0.227 scale-invariant.
- Visual authority: Blender understates the look; in-game is authoritative for color/material/emissive/lighting/context.
- Workflow: exclude power/connectors from Blender (build structure only, wire in game); RETRACTED the powerline-At run-vector reading as a Blender artifact (NEGATIVE_KNOWLEDGE_INDEX).
- Cleanup: OPEN_TOPICS_LOG active-version stamp corrected.
- Geometry/script measured; in-game color/emissive items are tagged GAME_VALIDATED where confirmed in game.


## 4.02.00 — Dome Radial-Ring Taper (Measured Control Recipe)

- Populated `dome_latitude_shell` with the geometry-measured spiraling-glass-dome control profile (round-trip residual <=0.01): 24-fold, 15 deg step, 4-ring linear taper radius=14.21-1.60*height, 32 deg cone; part roles S_ROOF_M_WIN / S_WALL_Q / T_WALLT.
- Added method `DOME_RADIAL_RING_TAPER` to METHOD_AUTHORITY_TABLE and MASTER_PLACEMENT_INTELLIGENCE_INDEX, with object contexts for S_ROOF_M_WIN (free/computed placement, not snappable), S_WALL_Q (sloped rib), and T_WALLT (base ring) — first radial-shell coverage in the authority layer.
- Reconciled DOME_STUDY_LESSONS to measured reality (tapering rings vs constant-radius rings).
- Logged glasshouse-dome motif in the creative-index stub (style only; color/lighting deferred).
- Recorded RADIAL_SLOPE_SPIRE concept (sibling radial-fan family) pending its control JSON.
- Geometry validated; in-game appearance/color validation remains pending.

## 4.01.00 — Placement Intelligence Governance Infrastructure

- Added seed `MASTER_PLACEMENT_INTELLIGENCE_INDEX` as the read-optimized placement-governance lookup surface.
- Added `METHOD_AUTHORITY_TABLE`, `PLACEMENT_PRECEDENCE`, and `NEGATIVE_KNOWLEDGE_INDEX`.
- Added schemas and templates for placement session receipts, build placement snapshots, method summaries, assembly conformance plans, and part usage manifests.
- Added doctrine: assembly context supersedes component context.
- Added separation rule: placement mechanics authority is separate from creative/style/use-case knowledge.
- Added single master changelog/open-topics governance; release-specific root open-topic files moved to archive.
- Added release-gate infrastructure check for placement-intelligence support files.
- External validator implementation is deferred; this release prepares the source-doc infrastructure needed by that validator.

## 4.00.00 — Authoritative Snap Placement (Major)

- BREAKTHROUGH: the NMS Base Builder add-on ships its complete snap system as data
  (resources/snapping_info.json + snapping_pairs.json) — now the AUTHORITATIVE placement source for any part
  in a snap group.
- Added `rules/AUTHORITATIVE_SNAP_PLACEMENT_PROTOCOL.md` (ASP-1..ASP-5): read snap points by name via
  connectivity; validated formula B_world = A_world @ Ma @ FLIP @ inv(Mb), FLIP=180 deg about Y; operators
  (list_build_operator / nms_snap [cycling inert in 5.1] / nms_save_data); volumetric overlap check;
  provenance authoritative-snap > derived-adjacency > heuristic.
- VALIDATED (snap): map matches the add-on's live snaps to 0.0 gap (within-group AND cross-group); formula
  reproduces full pose to 0.0 pos / 0.0 deg across triangle, floor+floor, floor+wall.
- Reconciled `PART_DATA_MAPPING_ALGORITHM.md` and `PART_PLACEMENT_MAP_USAGE_AND_VALIDATION_RULE.md`: derived
  adjacency demoted to FALLBACK for parts with no snap group; accuracy dial advanced for snap-group parts
  (no per-part proof build required to trust geometry). GOLD tier remains GAME_VALIDATED.
- Promoted rules to `PART_FAMILY_RULES.md` and `ISSUE_FIX_LIBRARY.md`.
- Bundled self-contained data under `library/authoritative_snap/`.
- Continuity: full audit of the placement subsystem; patch-sanity elsewhere.

## 3.01.01 — PIPE/BUBPIPE Validation Exception Patch

- Added `rules/PIPE_BUBPIPE_VALIDATION_EXCEPTION_RULE.md/json`.
- Reclassified `PIPE` and `BASE_BUBPIPE*` from authoritative verified Blender data to `GAME_VALIDATION_REQUIRED_PIPE_FAMILY` for connected pipe assemblies.
- Clarified that `PIPE` can be a valid in-game pipe despite zero-bbox/invisible Blender extraction.
- Clarified that BUBPIPE Blender orientation/appearance can differ from in-game result.
- Added `reports/3.01.01_PIPE_BUBPIPE_CONTRADICTION_REPORT.md`.
- Preserved raw extraction records as valid raw Blender evidence, but blocked their use as final validation for pipe-system continuity.

## 3.00.00 — AI Visual Capture Compliance Gate

- Major rulebook update: generated Blender/NMS build scripts must be AI-capture compliant when routed as build-generation outputs.
- Added `rules/BLENDER_VISUAL_FEEDBACK_HARNESS_PROTOCOL.md`.
- Added `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md`.
- Added `validation/ai_capture_compliance_check.py`.
- Added `toolkit/BLENDER_AI_REVIEW_BUNDLE_ADDON.md`.
- Added `toolkit/nms_ai_review_bundle_addon_v04.py`.
- Updated `validation/ai_review_bundle_check.py` to support v01 through v04 review bundles and to report capture-set, screenshot, single-collection, and review-required metrics.
- Updated `validation/run_gate.py` to auto-surface AI capture compliance for build-generation scripts.
- Updated `release/release_check.py` to self-test AI capture compliance and run_gate integration.
- Clarified that visual bundles are design-loop evidence only; run_gate/exported JSON remain required for objective validation.

## 2.17.02 — build objective conformance gate

## 2.19.01 — Recipe-First Lean Clean Final

- Removed inactive archive/history payload from the main source package after key lessons were consolidated into master active guidance.
- Retained single running changelog, recipe-first routing, wall-shell enclosure recipe, part placement aid, AI Review bundle intake, and validation gates.
- Clarified that the source package itself is the lean operating package; no separate runtime pack is maintained.

- Added `validation/build_objective_conformance_check.py`.
- Added good/bad fixtures proving connected floor/path builds pass and floating-floor builds fail.
- Patched `release/release_check.py` to make the new gate part of release validation.
- Clarified that generated builds must validate requested physical objectives, not only manifests or part-level reuse receipts.

## 2.17.01 — mandatory conformance enforcement + bundle receipt restoration
- Merged the 2.16.01 mandatory validated-logic enforcement into the 2.17 conformance line: `run_gate.py` now auto-requires validated logic reuse for validated/user-reviewed parts and build-generation scripts.
- Hardened recipe conformance handling: scripts using parts with executable conformance recipes cannot claim machine-checkable PASS without exported NMS JSON conformance.
- Added `validation/intent_graph_conformance_check.py` and fixtures: composite builds now compare exported connected-component count to `BUILD_INTENT_GRAPH.expected_connected_components`.
- Restored visible `bundle:` in the final protocol banner while preserving numeric `source docs rev` and `Docs Avail for Update?`.
- Added `rules/GPT_RUNTIME_UPLOAD_PACK_PROTOCOL.md` and `release/create_gpt_runtime_upload_pack.py` to allow governed, generated GPT Knowledge upload packs without hand-maintained duplicate drift.

## 2.17.00 — recipe conformance gate (exported geometry must obey the validated recipe)
- Added `validation/recipe_conformance_check.py`: ingests a build's EXPORTED NMS JSON (Position/Up/At) and, for every approved stair part, verifies the recorded `placement_signature` from the partmap - `Position[n+1] = Position[n] + At*RUN_STEP + Up*RISE_STEP` - using each part's own exported At/Up and the RUN/RISE read from its partmap. A part one lattice step from a stair neighbour whose displacement does not decompose onto its own (or the neighbour's) At/Up is mis-oriented versus the recipe and FAILS.
- Wired into `run_gate` behind `--require-conformance <exported.json>`; folded into the machine-checkable verdict.
- Wired into `release_check` as a self-test (block 10c): a correct stair export PASSES, a tipped export FAILS.
- Closes the gap demonstrated against 2.16.00: a build could carry a valid USED_PART_LOGIC receipt yet place geometry that ignored the recorded orientation (stairs tipped 90 degrees). Declared reuse proves intent; conformance proves the parts actually landed per the validated recipe, making the receipt falsifiable against real output.
- Added `rules/RECIPE_CONFORMANCE_PROTOCOL.md`. Conformance is scoped to parts with a validated recipe (stairs); unvalidated placements (pyramid faces, angled door) remain out of scope until validated.

## 2.16.00 — validated logic reuse + composite intent graph gate
- Added `rules/VALIDATED_LOGIC_REUSE_PROTOCOL.md`: generated builds must include `USED_PART_LOGIC` receipts proving that validated partmaps/algorithms were reused, or explicitly mark unvalidated parts/fitments provisional.
- Added `rules/COMPOSITE_BUILD_INTENT_GRAPH_PROTOCOL.md`: composite builds must declare whether subassemblies are intended, expected connected-component count, and required inter-subassembly connections.
- Added `rules/PROTOCOL_RECEIPT_EVIDENCE_RULE.md`: protocol banners must reflect executable receipts, not self-attestation.
- Added `validation/validated_logic_reuse_check.py` plus good/bad fixtures and wired it into `release/release_check.py`.
- Added reusable recipe helpers in `toolkit/validated_recipes/` for normal full-ramp stairs and C_TRIFLOOR phase-resolved placement.
- Documented the GPT/Claude composite failure lesson: recorded placement knowledge is not sufficient unless the generation artifact proves it used the relevant validated logic.

## 2.15.00 — controlled validation vocabulary (gate-enforced) + semantic stair gate wired
- Locked a single controlled `validation_status` vocabulary and made the release gate reject any value outside it: UNKNOWN -> UNTESTED -> SCRIPT_VALIDATED -> { BLENDER_USER_CHECK | BLENDER_SYSTEMATIC } (parallel, equal tier) -> GAME_VALIDATED, with an optional `_WITH_EXCEPTIONS` qualifier. BLENDER_SYSTEMATIC is reserved (gate fails any part claiming it until a systematic-routine standard exists); GAME_VALIDATED requires an in-game evidence reference (gate fails premature stamps).
- Reconciled the 7 ramp families and C_TRIFLOOR off the prior off-ladder USER_ACCEPTED / PLACEMENT_VALIDATED stamps to BLENDER_USER_CHECK (Blender user-reviewed, in-game pending), honoring "zero parts accepted in-game." Trifloor variants -> UNTESTED. Legacy values preserved under `_legacy_status`.
- `parts_status.csv` (ObjectID, family, validation_status) is now generated, drift-checked, and shipped with every release so per-stage counts can be filtered at a glance.
- Wired the previously-orphaned semantic stair float-gate into `run_gate`: an approved stair part flagged by the generic AABB no-float gate is cleared only if it sits one locked stair lattice step (sqrt(RUN_STEP^2 + RISE_STEP^2)) from another approved stair part. Generic AABB stays strict for everything else; a stair part with no lattice neighbour stays failed; no non-stair part is ever rescued. Added `validation/gate_fixtures/stair_semantic_unit_test.py`, run by `release_check` (block 9d).

## 2.14.01 — Release gate timeout hardening — 2026-06-12

- Patched `release/release_check.py` so nested validation subprocesses run with `python -S`, preventing site-startup/tool-warmup delays from timing out the authoritative release gate in constrained sandbox environments.
- Preserved the full release-gate check set; no validation checks were removed or weakened.
- Rereleased the 2.14.00 stair validation / semantic float-gate package as a clean patch release with `RELEASE GATE: PASS`.


## 2.13.01 — Protocol hardening, open-topics logging, and stair validation reporting — 2026-06-12

## 2.14.00 — Stair Family Validation and Scoped Semantic Float Gate

- Promotes normal full-ramp stairs (`B_RAMP`, `C_RAMP`, `F_RAMP`, `M_RAMP`, `S_RAMP`, `T_RAMP`, `W_RAMP`) to `USER_ACCEPTED` for general placement/use after V42 visual review.
- Adds scoped stair semantic float-gate adoption for approved normal full-ramp stair/floor relations while preserving raw AABB PASS/FAIL reporting.
- Updates normal full-ramp partmaps, partmap index, and master sheet through the partmap generation pipeline.
- Records half-ramp/half-stair variants as the next validation carry-over target; no inheritance is assumed for half ramps yet.


- Clarified `Docs Avail for Update?` as known, actionable source-document updates that have not yet been incorporated; open validation work, pending user review, and unknown classifications do not count.
- Added `rules/OPEN_TOPICS_LOG_PROTOCOL.md`; every downloadable artifact now requires a companion Open Topics Log.
- Added `rules/SOURCE_DOC_EVALUATION_CHECKLIST.md` to prevent transfer-package/source-doc evaluation drift.
- Corrected `rules/PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md` and `templates/PROTOCOL_CONFIRMATION_BANNER_TEMPLATE.md` to use the numeric `source docs rev` + `Docs Avail for Update?` banner, not obsolete `bundle:` text.
- Hardened `rules/VALIDATION_GATE_HARDENING_RULE.md` and `rules/SEMANTIC_FLOAT_GATE_PROPOSAL.md`: raw gate PASS/FAIL must be preserved, gate scope must be stated, and temporary stair continuation must not rename a raw FAIL to PASS.
- Updated `rules/STAIR_PLACEMENT_DOCTRINE.md` with V38/V39/V40 lessons: switchback placement logic is good, V38 blended corner failed, V39 improved the condition but left overlap/gaps, and V40 is only a validation candidate.
- Updated `rules/CORNER_TRANSITION_ALGORITHMS.md` to distinguish angle-first blended corners from connectivity-first/fan-spaced corner candidates.
- Updated the request router so source-doc review and protocol correction load the new checklist, Docs Avail protocol, banner rule, traceability rule, and Open Topics protocol.
- Added `reports/2.13.01_SOURCE_DOC_UPDATE_REPORT.md` and `reports/2.13.01_OPEN_TOPICS_LOG.md`.
- Incorporated all known confirmed pending source-doc updates from the transfer package and stair/protocol CAPA sequence. Remaining validation work is tracked as open topics, not Docs Avail items.


## 2.13.00 — Part placement knowledge consolidation — 2026-06-12

- Promoted the universal placement doctrine: `WORLD_POSITION = TARGET_POSITION + ORIGIN_OFFSET + SCALE_OFFSET + CONNECTION_OFFSET`.
- Documented the local-frame repeat rule proven by the stair branch: `Position[n+1] = Position[n] + At * RunStep + Up * RiseStep`.
- Expanded partmap schema guidance with default orientation, origin type, scale behavior, connection type, validation unknowns, user acceptance status, and family equivalence classification.
- Added `rules/PART_VALIDATION_STATUS_LADDER.md` with the acceptance ladder from UNTESTED through USER_ACCEPTED_WITH_EXCEPTIONS.
- Added `rules/TRIFLOOR_FAMILY_VALIDATION_FRAMEWORK.md` to capture V24 as the final TRIFLOOR validation matrix and preserve all 14 variant candidates.
- Added `rules/STAIR_PLACEMENT_DOCTRINE.md` with floors-anchor/stairs-move doctrine and the locked stair edge formula.
- Added `rules/CORNER_TRANSITION_ALGORITHMS.md` distinguishing chamfered and blended corner algorithms.
- Added `rules/SEMANTIC_FLOAT_GATE_PROPOSAL.md` as a documented proposal, not an adopted gate behavior.
- Updated future part-validation guidance to focus on family-specific unknowns rather than re-proving the placement kernel.
- Deferred V38 user acceptance, semantic float-gate adoption, and TRIFLOOR family-equivalence classifications to a later validation update.


## 2.12.01 — Protocol banner source revision + docs-update availability — 2026-06-07

- Formalized the current protocol banner format with numeric-only `source docs rev`.
- Added `Docs Avail for Update?: <Yes|No> (<count>)` to distinguish pending reusable lessons/source-doc updates from completed updates.
- Added `rules/DOCS_UPDATE_AVAILABILITY_PROTOCOL.md`.
- Updated `PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md`, `PROTOCOL_CONFIRMATION_BANNER_TEMPLATE.md`, `TRACEABLE_PROTOCOL_VERIFICATION_RULE.md`, and router/start-here docs.
- No C_TRIFLOOR/partmap behavior change from 2.12.00.


## 2.12.00 — C_TRIFLOOR validated placement map + master part algorithm — 2026-06-07

- Promoted `C_TRIFLOOR` from discovered/unvalidated to `PLACEMENT_VALIDATED` after the phase-resolved V20/V21/V23 advanced-shape study.
- Added `rules/PART_PLACEMENT_MASTER_ALGORITHM.md` as the canonical equation for converting target geometry + part profile into Position/Up/At/Scale placement.
- Added `rules/FUTURE_PART_VALIDATION_DIRECTIVE.md` to define the bounds/default-orientation/scale/phase/pivot validation ladder for the next parts and families.
- Extended `C_TRIFLOOR.partmap.json` with executable part-profile fields: origin type, phase rule, scale behavior, family status, validated applications, and master placement rule.
- Corrected `C_TRIFLOOR_Q.partmap.json`: it is not an alias of `C_TRIFLOOR`; it has distinct FBX geometry and remains unvalidated until its own boundary/filler proof passes.
- Extended `part_placement_master_sheet.csv` with fields needed to execute the master algorithm across parts.
- Added `reports/TRIFLOOR_C_TRIFLOOR_CAPABILITY_STUDY_2.12.00.md` documenting lessons learned, failure corrections, and next validation steps.



## 2.11.01 — Packaging hygiene: stable inner folder name — 2026-06-01

- Renamed the inner package folder from `nms_20601` (a stale carryover that read like the old 2.06.01 version) to a stable, version-agnostic `nms_master_docs`, so the folder name can never masquerade as a version again.
- Made the `fbx_bounds_source` path in the triangle behavior-signature report relative (dropped the embedded folder name).
- No content or behavior change.


## 2.11.00 — Provenance levels + layer split + validation traceability — 2026-06-01

- Provenance levels on every datum: `OBSERVED_FACT` (measured), `DERIVED_RULE` (hypothesis), `VALIDATED_RULE` (proven). A derived rule must not be consumed as validated. Documented in the schema; generated entries tagged (bounds=OBSERVED_FACT, orientation override=VALIDATED_RULE, un-proven neighbor model=DERIVED_RULE_PENDING).
- Formalized two knowledge layers: PART PLACEMENT MAP (how a part fits) vs PART BEHAVIOR SIGNATURE (how it is used; lives in the behavior-learning protocol + use-case catalog). They must not be merged.
- Added validation traceability fields (`validated_with_algorithm`, `validated_date`, `validation_build`, `validation_evidence`), null until a part is validated.
- No promotion: TRIFLOOR stays placement-map SEEDED, behavior-signature DISCOVERED, fitment HYPOTHESIS, validation NOT COMPLETE.


## 2.10.00 — Orientation exceptions carried into the part map — 2026-06-01

- The generator now pulls per-part orientation overrides from `PART_ORIENTATION_OVERRIDES.json` into the map: one generated, drift-checked partmap per override part (BILLBOARD today), plus an `orientation_override` column in the master sheet.
- Added the optional `orientation_override` partmap field (documented in the schema). The override registry stays the curated source; map entries are generated from it.
- Effect: resolving a part's placement from the map now surfaces its exception (e.g. BILLBOARD must use rx=0, not the generic rx=90), so the exception follows the part, not the project.


## 2.09.01 — Restore over-consolidated rule sources — 2026-06-01

- 2.09.00's twin removal was too aggressive: 9 of the 42 dropped `.json` were the richer source, not duplicates. Restored them: PART_USE_CASE_CATALOG, PART_FAMILY_RULES, UNIVERSAL_RULES, CONTINUOUS_PATH_ASSEMBLY_RULE, CURATED_DETAIL_HIERARCHY_RULE, GROUND_ZERO_FOUNDATION_RULE, PROMPT_TO_FEATURE_ROUTER, PART_ORIENTATION_OVERRIDES, PROHIBITED_AND_PLACEHOLDER_OBJECTS.
- The other 33 (.md equal or fuller) stay removed. No learned placement/usage knowledge is now missing from the active package.
- Redundant per-part FBX `extent_` data inside some restored rules is now duplicated by the part map; stripping it (and merging unique knowledge into one canonical doc per rule) is a deliberate follow-up rather than bulk deletion.


## 2.09.00 — Part placement map usage tie-in + twin consolidation — 2026-06-01

- Added `rules/PART_PLACEMENT_MAP_USAGE_AND_VALIDATION_RULE.md` (single file, no twin): two-lane resolution (validated map short-circuits placement geometry only; recipes/use-cases always-on), per-part validation with user sign-off, status-is-confidence-not-a-filter, the per-build report, and the algorithm-accuracy dial. Wired into the critical bundle list for build/recreation request types; gate fixtures updated to declare it.
- Added an informational part-placement-map coverage section to `run_gate`: lists each used part's validation status (validated / not-yet-validated / not-in-map). Never fails the gate.
- Consolidated document creep: removed 42 redundant `rules/*.json` twins (the `.md` is canonical; only the code-read `REQUEST_ROUTER_CHECKLIST.json` keeps both forms). Dangling references repointed to `.md`. Removed files are preserved in a separate archive zip for rollback.


## 2.08.00 — Part placement map Tier A (bounds backfill) — 2026-06-01

- Backfilled validated FBX bounds for all 2078 library parts into the generated master sheet (the big chunk of validated data that lived only in the dimensions library).
- Added `library/part_placement_maps/generate_partmaps.py`: derives the master sheet, index, and a new open-parts worklist from one source — per-part partmaps for placement intelligence, the dimensions library for bounds. `--check` mode detects drift.
- Added `part_placement_worklist.json` (parts grouped by what they still NEED).
- Wired `partmap_storage_check` and the generation-drift check into `release_check` (they were not run by the gate before).
- Placement stays unvalidated (`bounds_only`) per part until a map-only proof build passes and the user agrees; bounds-only parts fall back to the old multi-source search for placement. No part is auto-marked validated by transfer.


## 2.07.03 — Gate repair / rollout hygiene — 2026-06-01

- Repaired the 2.07.02 rollout, which shipped red on its own release gate.
- Bumped drifted version labels (START_HERE, README, FILE_INVENTORY, run_gate banners, bootstrap) from 2.07.00 to current.
- Restored the FILE_INVENTORY title to the registry-recognized format.
- Gave request types `part_behavior_learning` and `rule_discovery_and_proof` a `critical` bundle list (mirroring their populated `must_check`), fixing the router check.
- Added `TRACEABLE_PROTOCOL_VERIFICATION_RULE` and `PART_BEHAVIOR_LEARNING_PROTOCOL` (now universally required) to the gate fixtures so the run_gate self-tests pass again.
- Stripped shipped `.pyc`/`__pycache__` artifacts and corrected the manifest file_count. No feature change.

## 2.07.02 — Part Placement Map Storage

- Added canonical local-frame Part Placement Map schema.
- Added reusable Part Data Mapping Algorithm: JSON/Python/FBX → local frames → local neighbor offsets → partmap.
- Added Partmap Storage Compliance Protocol requiring storage receipt for durable learning.
- Added `validation/partmap_storage_check.py`.
- Seeded TRIFLOOR partmaps from triangle behavior signature v1 as DISCOVERED, not VALIDATED.



## 2.07.00 — Connectivity / no-float gate — 2026-06-01

- Added a mechanical connectivity / no-float check to `validation/run_gate.py`. The gate now reconstructs each placed part's world bounding box from its captured transform plus library `extent_*`/`center_*` fields and FAILS the build if any placed part touches no other placed part within 0.5 units.
- Made `rules/DISCONNECTED_ASSEMBLY_HARDSTOP_RULE.md` mechanically enforced rather than prose-only: floating walls/floors/ramps/stairs/shells/foundations are flagged STRUCTURAL and must be reconnected; float is the disfavored default.
- The only override is an explicit user request for a floating part, approved per-run outside the gate with no carryover (the gate is stateless and has no in-script bypass flag, so prior approval never carries forward).
- Added gate fixtures `validation/gate_fixtures/connected_build_must_pass.py` and `floating_part_must_fail.py`, plus a release-check self-test asserting the connected build PASSES and the floating build FAILS.


## 2.06.01 — Build/image routing guard — 2026-06-01

- Added a mandatory guard preventing NMS-context build-language prompts from being routed to image generation unless visual-output terms are explicit.
- Added `rules/NMS_BUILD_VS_IMAGE_ROUTING_GUARD.md/json`.
- Updated request router, prompt-to-feature router, prompt routing gate, execution kernel, bootstrap, START_HERE, README, and release metadata.
- Added gothic/castle/fortress facade prompt route paired with radial airlock/iris recipes for the 12-sided flush entrance test case.



## 2.06.00 — Execution kernel + JSON geometry intelligence — 2026-06-01

- Added root objective charter for advanced NMS Builder Python generation, transferable master docs, continuous knowledge expansion, and streamlined data mapping.
- Added compact execution kernel to force classify → evidence lookup → recipe/signature selection → invariant/parameter split → placement plan → validation → lesson promotion.
- Added control-to-variant protocol for "same feature but different" requests.
- Added JSON geometry intelligence protocol to mine JSON into part roles, connection relationships, local frames, locked invariants, allowed parameters, and missing evidence.
- Added prompt-to-feature router and compact JSON recipe signature index.
- Added starter geometry templates for endpoint stairs/ramps and dome latitude shells.
- Updated request router, prompt gate, memory recall index, rule application matrix, bootstrap, and recipe library to route through the new layer.



## 2.05.01 — Disconnected assembly hard-stop merged into version-registry baseline

Release level: **patch**.

Why: the prior local `2.05.00` successor package added a version-location registry, while the later disconnected-assembly corrective action had been packaged on an obsolete 2.04.x branch. This release merges that corrective action into the current 2.05.x baseline so the registry package does not lose the Batman V11 hard-stop fix.

Changed:
- Added `rules/DISCONNECTED_ASSEMBLY_HARDSTOP_RULE.md/json`.
- Added `reports/BATMAN_V11_DISCONNECTED_ASSEMBLY_CAPA_2.05.01.md`.
- Added `reports/PROTOCOL_APPLICATION_AUDIT_2.05.01_DISCONNECTED_ASSEMBLY_MERGE.md`.
- Updated request router, generator contract, rule matrix, kickoff gate, recall index, and START_HERE so the rule is loaded for spires, stairs, ramps, roof crowns, wall bays, vehicles, cave interiors, airlocks, and similar assembled subsystems.

Behavioral impact: connected assembly proof is required before delivery; disconnected screenshots trigger CAPA and revert-to-control/proof-module workflow.


## 2.05.00 — Version-location registry + label-drift reconcile

Release level: **minor**.

Why: the uploaded 2.04.06 failed its own gate — eight active version labels still read 2.04.01. Version labels were scattered with no master list.

Changed:
- `release/VERSION_LOCATIONS.json` (+ generated `VERSION_LOCATIONS.md`): single registry of every active version label.
- `release/release_check.py`: loads the registry, fails on any registered location != current, WARNs on version mentions in unregistered files.
- Reconciled all 2.04.x active labels to the current version.

## 2.04.01 — Airlock parametric overlap fix

Release level: **patch**.

Why: 2.04.00 correctly wired JSON-derived parametric recipes, but the 32-sided airlock test proved that the side-count adaptation rule was incomplete. Correct orientation alone is insufficient; higher side counts must preserve the central iris pivot/control radius unless a larger aperture is explicitly requested.

Changed:
- Added `rules/AIRLOCK_IRIS_PARAMETRIC_OVERLAP_RULE.md/json`.
- Updated `rules/AIRLOCK_IRIS_PARAMETRIC_RECIPE_RULE.md/json` and `toolkit/AIRLOCK_IRIS_PARAMETRIC_GENERATOR_SKELETON.py` with radius-mode and overlap-density requirements.
- Updated router, recall index, recipe library, generator contract, and rule matrix so the overlap rule is loaded for airlock/iris requests.
- Fixed stale active-version claims inherited by the uploaded 2.04.00 package.

Behavioral impact: higher-count airlock/iris generators default to `KEEP_CONTROL_CENTER_PIVOT_OVERLAP_DENSITY`; chord-preserving radius expansion requires explicit user approval.


## 2.03.01 — Rollout hygiene and bootstrap alignment

Release level: **patch**.

Why: 2.03.00 was directionally correct but needed final distribution cleanup before rollout. The bootstrap over-stated `RX=90`, environment wording was inconsistent, and release gate checks did not explicitly fail shipped Python cache artifacts or manifest file-count drift. The user also clarified that once JSON is provided for the current build/subsystem, orientation must be calculated from JSON mapping before continuing placement-sensitive Python work.

Changed:
- `transfer_prompts/NMS_BUILDER_BOOTSTRAP_CURRENT.txt`: aligned to Base Builder 6.4.1 with Blender 5.0.1 confirmed working; Blender 5.1.1 requires FBX importer/add-on checks; generic `rx=90` is fallback only; current-build JSON orientation mapping is mandatory once JSON exists.
- `00_START_HERE_CURRENT.md`, `README.md`, `02_GENERATOR_CONTRACT.md`, `rules/JSON_EVIDENCE_MAPPING_GATE.md`, and `rules/WORKING_JSON_FIRST_PRINCIPLE.md`: clarified JSON-provided orientation control and environment wording.
- `release/release_check.py`: now fails if `__pycache__`/`.pyc` artifacts are present or if `PACKAGE_MANIFEST.json` file count drifts from actual shipped files.
- `FILE_INVENTORY.md`: regenerated.

Behavioral impact: no new build aesthetic rule. This is rollout/distribution hardening and clarifies already-required JSON-first orientation validation.


## 2.03.00 — Rollout readiness (bootstrap refresh)

Release level: **minor**.

Why: the onboarding prompt a new chat received was two major-versions stale, so the router/tiers/banner never reached new chats.

Changed:
- `transfer_prompts/NMS_BUILDER_BOOTSTRAP_CURRENT.txt`: single current bootstrap teaching the router, the three build tiers, the REQUEST_CLASSIFICATION block, the per-response banner, and the combined gate flags.
- Retired stale bootstraps (v54/v57/full-library-fix/START_HERE_CURRENT_PROMPT) to an attic bundle; repointed inbound references.
- `release/release_check.py`: ACTIVE_VERSION_CLAIMS now polices the bootstrap version.
- `02_GENERATOR_CONTRACT.md`: one canonical build invocation runs `--require-json-evidence` and `--require-router` together.

## 2.02.00 — Build request depth tiers

Release level: **minor**.

Why: not every build request needs the full knowledge base. Deep design work should pull it; refinements should not re-read everything.

Changed:
- `rules/REQUEST_ROUTER_CHECKLIST.json`: `build_generation` is now the deep tier (full part knowledge + design toolkits + workflow); added `build_specific_addition` (placement facts, no design-ideation refs) and `build_refinement_or_optimization` (safety + validation only).
- `validation/request_router_check.py`, template, and checklist updated for the new tiers.

## 2.01.00 — Semantic router + per-response confirmation

Release level: **minor**.

Why: the 2.00.x router verified a classification block existed but not that it was correct.

Changed:
- `validation/run_gate.py`: `--require-router` now checks request_type membership and requires the universal critical anchor + the declared type's critical bundles.
- `rules/REQUEST_ROUTER_CHECKLIST.json`: per-type `critical` bundles, `ambiguous_or_unclear` (ask the user), and an `adding_new_request_type` process.
- `rules/PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md/json` + `templates/PROTOCOL_CONFIRMATION_BANNER_TEMPLATE.md`: mandatory per-response banner.
- `validation/request_router_check.py`: validates all of the above.

## 2.00.01 — Release hygiene / stale-label gate hardening

Release level: **patch**.

Why: 2.00.00 correctly added the mandatory request router, but the release protocol missed stale active-version labels in `00_START_HERE_CURRENT.md` and `validation/run_gate.py`. This patch fixes those labels and hardens the release gate so future active baseline/tool-banner drift fails automatically.

Changed:
- `00_START_HERE_CURRENT.md`: current baseline now reads `2.00.01`.
- `README.md`: title now reads `2.00.01`.
- `FILE_INVENTORY.md`: regenerated under `2.00.01`.
- `validation/run_gate.py`: banner and executable output now read `v2.00.01`.
- `release/release_check.py`: adds active-version claim scanning for entry docs and validation gate banners.
- `release/RELEASE_NOTES_2.00.01.md`: added.

Behavioral impact: no build-generation rule change; release hygiene and distribution confidence only.

## 2.00.00 — Mandatory request-router and governance enforcement

Release level: **major**.

Why: rules existed but were not reliably applied by chats. This release adds a mandatory request-type router, executable router validation, and `run_gate.py --require-router` classification checks so future chats must classify the request and apply the correct rule bundle before acting.

Added:
- `rules/REQUEST_ROUTER_CHECKLIST.md/json`
- `validation/request_router_check.py`
- `templates/REQUEST_CLASSIFICATION_BLOCK_TEMPLATE.md`
- `reports/2.00.00_DOCUMENT_PURPOSE_AND_ROUTING_REVIEW.md`

Updated:
- `00_START_HERE_CURRENT.md`
- `00_KICKOFF_INTAKE_GATE.md`
- `02_GENERATOR_CONTRACT.md`
- `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md/json`
- `validation/run_gate.py`
- `release/release_check.py`

Behavioral change:
- Before generation/review/evaluation, chats must route requests to a specific rule bundle.
- Protocol breach or user correction is a hard stop that triggers CAPA.
- Major generated scripts can be required to include `REQUEST_CLASSIFICATION` and pass `run_gate.py --require-router`.


Single source of version history. One line per release, newest first.
Pre-1.00.00 legacy `vNN` changelogs are preserved in the ATTIC history bundle
(`archive/changelogs/`), not shipped in the working master.

- **1.03.03** (patch) — Consolidation & cleanup: one-line-per-version CHANGELOG; removed shipped Python bytecode; relocated `archive/` and superseded version-stamped reports to a separate ATTIC history bundle; regenerated FILE_INVENTORY; added an explicit READ-ORDER/priority spine to START_HERE. No build-generation behavior change.
- **1.03.02** (patch) — Merged working-JSON-first with CAPA + validation-gate hardening; added Airlock/Iris exact-JSON-recipe rule and Validation-Gate-Hardening rule; run_gate now fails Part-wrapper misuse and zero-placed-part false passes; added gate fixtures + release_check behavioral self-tests.
- **1.03.01** (patch) — Added Working-JSON-First Principle; reinforced JSON Evidence Mapping Gate; fixed run_gate indentation.
- **1.03.00** (minor) — Added JSON Evidence Mapping Gate + Systematic-Failure CAPA Protocol; run_gate `--require-json-evidence`.
- **1.02.01** (patch) — Fixed 1.02.00 release metadata so the release gate passes.
- **1.02.00** (minor) — Added Full-Version Continuity Review Rule (review the whole delta since a chat's last-used version, not just the latest patch).
- **1.01.01** (patch) — Enforced version cascade-reset in the release gate; added `supersedes_version`.
- **1.01.00** (minor) — Added executable release gate (`release_check.py`); established single source of version truth.
- **1.00.00** (major) — Initial consolidated MASTER governance package (v57 lineage consolidated into semantic versioning).
- **legacy v35–v60** — pre-semantic iteration history; see ATTIC `archive/changelogs/`.

## 2.04.00 — Parametric JSON Recipe Protocol Wired
Adds and wires JSON feature concept extraction plus airlock/iris parametric recipe rules into routing, generator contract, rule matrix, recall index, transfer prompts, and recipe library. Requires a visible `Protocol confirmation` block for JSON feature review and known JSON-derived generation.

## 2.04.02 — Spire Visual Pre-Recipe Notes
Adds preliminary spire/tapered tower/cupola visual recipe notes from screenshots. This is not an exact recipe; ObjectIDs/radii/scales/orientations remain pending future JSON extraction.

## 2.04.03 — Spire Mini JSON Preliminary Extraction
Adds preliminary JSON-supported spire/cupola notes from Jenness WIP Townhome. Confirms staged short-wall/roof-cap spire grammar, but remains partial and not a locked exact recipe.

## 2.04.04 — Power / Utility Exclusion Rule
Adds default exclusion for power/logic infrastructure. JSON studies should count these as ignored utility infrastructure, and generated builds should not place them unless explicitly requested.

## 2.04.05 — Connected-Piece Curvature Grammar
Adds broad connected-piece curvature grammar. Dome, cylindrical habitat, spire, Taj dome, Bumblebee/body-shell, vehicle hull, and related lessons are now treated as reusable curve/path/profile methods, not narrow exact labels.

## 2.04.06 — Prompt Routing / Rule Application Gate
Adds mandatory pre-response prompt classification and rule-application gate. Source-doc updates require a Protocol Application Audit. Image retention must be explicitly decided before archiving visual references.

## 2.18.01 — Focal geometry + protocol hardening

- Adds hard-fail protocol banner rule and executable banner checker.
- Adds Blender runtime script protocol and checker to prevent preview-only no-part scripts.
- Adds focal-build geometry strategy protocol.
- Adds single-part surface mesh construction protocol.
- Adds C_TRIFLOOR edge-contact graph protocol and scope boundary.
- Adds curve-follow transform propagation protocol.
- Updates request router with `new_geometry_synthesis`.
- Updates C_TRIFLOOR partmap with edge-contact/freeform scope requirements.
- Adds release-gate self-tests for banner, Blender runtime, and geometry construction manifests.



## 2.18.01 — Hybrid Scene Placement Aid / Interior Completion Hardening

Confirmed from V08/V09/V10 bat-signal hybrid build review:

- Added `HYBRID_SCENE_PLACEMENT_AID_PROTOCOL`.
- Hardened rule that review-required parts are not exempt from float/objective review.
- Added placement-aid fields to capture mount normal, tangent axis, roll axis, standoff, and curve/surface-follow requirements for parts such as `BUILDFLATPANEL`, `S_LIGHTSTRIP0`, and `BUILDLIGHT`.
- Added interior completion requirement for building/room requests: floor deck, ceiling, side liners, back closure, entrance threshold, and minimal interior detail.
- Added scene expansion discipline: surrounding city/scenery belongs in separate collections and does not replace focal-build acceptance.
- Active source-doc revision promoted to 2.18.01.


## 3.01.02 — PIPE/BUBPIPE Contextual Connector Evidence Patch — 2026-06-18

- Added `rules/PIPE_BUBPIPE_CONTEXTUAL_CONNECTOR_RULE.md`.
- Added exported JSON evidence under `data/PIPE_BUBPIPE_JSON_EVIDENCE_3.01.02.json` and interpreted evidence under `data/PIPE_BUBPIPE_CONTEXTUAL_CONNECTOR_EVIDENCE_3.01.02.json`.
- Refined 3.01.01 PIPE/BUBPIPE status from generic game-validation-required to contextual connector graph policy.
- Marked `PIPE`, `BASE_BUBPIPE`, `BASE_BUBPIPE_S`, `BASE_BUBPIPE_L`, `BASE_BUBPIPE_T`, and `BASE_BUBPIPE_X` as `GAME_VALIDATION_REQUIRED_PIPE_CONTEXTUAL_CONNECTOR`.
- Documented that JSON transform data is useful, but Blender static bbox/visual extraction is not authoritative for in-game connected pipe behavior.
- Preserved the rule that RX90 may correct isolated orientation but does not validate connected-pipe continuity.

## 5.04.03 — package hygiene correction

- Normalized active source-doc revision to 5.04.03.
- Corrected release/version/manifest drift from 5.04.01/5.04.02 labels.
- Resolved transfer continuity dangling references with current placeholder artifacts.
- Added missing RPAM coverage for transfer-summary and triage review-assistance rules.
- Reran release gate for PASS status.
