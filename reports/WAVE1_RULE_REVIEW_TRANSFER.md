# Rule-Review Work-Stream — Transfer Summary (wave 1 complete, current package 5.05.00)

Claude-to-Claude handoff so the rule-by-rule review can resume without re-deriving it. Read this, then continue from "Resume here."

## The goal of this work-stream
Make the rules layer trustworthy and light: (1) decide what each mapped rule actually IS, (2) consolidate duplicates, (3) wire valuable rules into governed processes so they reach builds, (4) move part knowledge out of the rules layer into the creative knowledge base, (5) minimize context load. Driven by the package owner (James).

## The operating distinction (the spine)
- **RULE** governs behavior (placement mechanics, float/snap/orientation, process gates). Stays in rules/.
- **FINDING** is descriptive part/build knowledge (in-game effects, extents, "looks good as X"). Belongs in the creative knowledge base, surfaced on build sheets, governs nothing.
- **RECIPE** is a reusable assembly. Belongs in the recipe library/toolkit, not as a "rule."
- **PROCESS/GOVERNANCE** belongs in the operating card / gates, not inside per-part packets.
- Test: *if removing it changes what is allowed/required -> RULE; if it only changes what you know -> FINDING.*

## How knowledge actually reaches a build (critical)
`validation/part_context_resolver.py --ids <ObjectIDs> --intent "<request>"` emits a packet:
- MANDATORY_PLACEMENT_CONTEXT (forced): per-part precedence tier, snap, geometry, allowed methods, forbidden, applicable rules + all UNIVERSAL_PROCESS rules.
- CREATIVE_CONTEXT (offered, firewalled): `part_character` from `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` (`part_geometric_character`, `color_variant_families`, `logged_motifs`), recipes, fit-rules.
Resolver surfaces a rule by scope: UNIVERSAL_PROCESS (always), PART_SPECIFIC (its object_ids), FAMILY_OR_ASSEMBLY (its families tokens in a used ObjectID), CREATIVE (creative context). A rule with the wrong scope/keys is effectively invisible. As of 5.05.00 the resolver is advertised in START HERE + kickoff (was lookup-only before).

## Cluster audit status (95 unique rules)
- JSON_EVIDENCE (10): AUDITED. Collapse v53/v54/geometry-intelligence/v2.04 ladder -> one staged JSON protocol. PRESERVE the mapping verbatim: COORD_MODE="XnZY", AXIS_MODE="RIGHT_AT_UP", BASE_ROTATION_MODE="POST_RX90", POST_BASELINE_CORRECTION="LOCAL_Y_180"; right=at.cross(up); JSON Position=[x,z,-y]; Up/At authoritative. Keep WORKING_JSON_FIRST_PRINCIPLE + JSON_EVIDENCE_MAPPING_GATE (dedupe source lists) + JSON_GEOMETRY_VALIDATION_LOOP. Relocate AIRLOCK_IRIS_EXACT_JSON_RECIPE -> recipe library; PROTOCOL_RECEIPT_EVIDENCE -> process.
- PLACEMENT_MECHANICS (20): AUDITED. Mostly healthy keepers. Fold CONNECTED_SURFACE_NO_STEPPED_OFFSET -> CONNECTED_PIECE_CURVATURE_GRAMMAR. Consolidate precedence/authority (PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE + PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE + PLACEMENT_INTELLIGENCE_GOVERNANCE + ASSEMBLY_CONTEXT_SUPERSEDES) -> one law, PRESERVE every tier; backed by data/PLACEMENT_PRECEDENCE.json + METHOD_AUTHORITY_TABLE.json (keep data). Consolidate part-map library (PART_PLACEMENT_MAP_SCHEMA + PART_PLACEMENT_MAP_USAGE_AND_VALIDATION + PARTMAP_STORAGE_COMPLIANCE + PART_PLACEMENT_MAP_SCHEMA, with VERIFIED_PARTMAP_DATA as data-provenance section) -> one rule, PRESERVE SNAP_VALIDATED/GOLD tiers + non-snap fallback. Keep standalone: AUTHORITATIVE_SNAP, CONTINUOUS_PATH, DISCONNECTED_ASSEMBLY_HARDSTOP, GROUND_ZERO, PART_ORIENTATION_OVERRIDES, SPACING_CONNECTION_SCALE_RULES, STAIR_PLACEMENT_DOCTRINE.
- RECIPE_FEATURE (9): AUDITED. PIPE 3.01.01 retired (done, 5.05.00). Consolidate 3 airlock rules (EXACT + PARAMETRIC_RECIPE + PARAMETRIC_OVERLAP) -> one airlock recipe in recipe library. Relocate PIPE_BUBPIPE_CONTEXTUAL_CONNECTOR -> negative-knowledge; PROMPT_TO_FEATURE_ROUTER + RECIPE_CONFORMANCE -> process. Keep DOME_STUDY_LESSONS, WALL_SHELL_ENCLOSURE_RECIPE as recipes. Consolidate variant docs (RECIPE_PARAMETERIZATION + CONTROL_TO_VARIANT + variant-half of JSON_FEATURE_CONCEPT).
- CREATIVE_KB (7): AUDITED. Merge DELTA_LEARNING_PROTOCOL -> SELECTIVE_VISUAL_MEMORY_POLICY (both v41, overlap). Reconcile PART_USE_CASE_CATALOG (findings store) with the creative index ("one spot"). Fold retired SCALE_OVER_QUANTITY family -> CURATED_DETAIL_HIERARCHY. Keep PLACEMENT_MECHANICS_VS_CREATIVE_STYLE_SEPARATION_RULE (the boundary law) + SELECTIVE_VISUAL_MEMORY_POLICY. Cross-reference the learning-capture family by lane.
- FOCAL_GEOMETRY (6): AUDITED. Organize geometry-derived-placement family (FOCAL_BUILD_GEOMETRY + CURVE_FOLLOW + SINGLE_PART_SURFACE_MESH + CONNECTED_PIECE_CURVATURE_GRAMMAR + C_TRIFLOOR_EDGE_GRAPH + CONTINUOUS_PATH) into one doctrine with named contracts under FOCAL_BUILD_GEOMETRY (CURVE_FOLLOW ~= CURVATURE_GRAMMAR). Merge the two C_TRIFLOOR docs (TRIFLOOR_FAMILY_VALIDATION_FRAMEWORK = finding/proof; C_TRIFLOOR_EDGE_CONTACT_GRAPH = rule). Keep COMPOSITE_BUILD_INTENT_GRAPH (distinct from no-float). Merge HYBRID_SCENE_PLACEMENT_AID -> FOCAL_BUILD_GEOMETRY.
- PROCESS_GOVERNANCE (28): NOT YET AUDITED — the owner's "keep as process may not be needed" set; expect the most relocate/retire. Split into ~14+14.
- MISC (14): NOT YET AUDITED.

## Family rules -> findings (approved, not yet executed)
`rules/PART_FAMILY_RULES.json` (18 families) must stop being a rules file. Retire the placement-behavior families (all superseded by mined part data / curvature grammar / origin helpers / continuous-path / validated C_TRIFLOOR) INCLUDING HALF_ARCH_MIRRORING (owner said retire arch-mirror). Migrate the FINDING families (B_SHL_E red glow, B_WNG_A electric FX, TURRET beam projector, AERON options, design-families, ring-trim parts/use-cases) INTO `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` (`part_geometric_character` for effects/lighting, `color_variant_families` for recolor, `logged_motifs` for design families). No new files — the creative index is the one home (it already has part_geometric_character + color_variant_families + a deferred "color_mutability validation" item to retire on completion). Then reclassify/retire the PART_FAMILY_RULES RPAM entries.

## Discovery-first workflow (designed, partly built)
Owner wants the AI to review the creative knowledge base BEFORE selecting ObjectIDs ("futuristic" -> colorful + light-emitting -> discover beam emitters). The index has the data but no effect->parts view. TODO: add a generated `discover_by_quality` view (effect/quality -> ObjectIDs) inside the creative index, derived from each part's characteristics, with a sync gate. Proven live: SET_CLASS_A/B/S surface as magenta/blue/gold beam_emitters.

## What wave 1 (5.05.00) executed
- Wired the resolver into START HERE + kickoff (creative-review-first + resolve step).
- Re-scoped 5 mis-scoped rules: VERIFIED_PARTMAP_DATA, ASSEMBLY_CONTEXT_SUPERSEDES, OBJECT_USE_RECORDING, BUILD_PLACEMENT_SNAPSHOT -> UNIVERSAL_PROCESS; CONTINUOUS_PATH -> FAMILY_OR_ASSEMBLY with path keys. Cleared dead family tokens.
- Retired PIPE_BUBPIPE_VALIDATION_EXCEPTION_RULE (3.01.01); repointed references to the 3.01.02 contextual-connector rule.
- Gate PASS, resolver self-test PASS, version-callout ledger 0.

## Wiring backlog remainder (deferred)
- Add the generated discover_by_quality view + sync gate.
- Add a `kind` + `runtime_status` field to every RPAM entry and a gate failing release on any unclassified entry (enforces RULE_UPDATE_PROTOCOL going forward; the owner noted it wasn't followed — stale rules accumulated).
- Re-key GROUND_ZERO by build intent rather than floor/ramp/stair parts.
- After each consolidation, confirm the survivor's scope so it surfaces.

## Mechanics
- Version: X.YY.ZZ; cascade via `release/VERSION_LOCATIONS.json` + `release/VERSION.json` + manifest version + START HERE title/baseline + `protocol_banner_good.txt` (write that one with SEPARATE read-then-write). Bump CHANGELOG + `release/RELEASE_NOTES_<ver>.md`. Clear __pycache__/*.pyc, set manifest `file_count` to actual, then `python3 release/release_check.py` until "RELEASE GATE: PASS". Zip excluding pycache.
- Governance/active-build docs are present-tense only; version history lives in CHANGELOG/reports/archive (version_callout_check enforces no `## X.YY.ZZ` section headers; ledger currently 0).
- Working dir for this stream: extract the package; deliverables to /mnt/user-data/outputs. Analysis artifacts: MAPPING_WIRING_LOG.md, RULE_VS_FINDING_REVIEW_5.04.md, RULE_CLASSIFICATION_FIRST_PASS.csv.

## Resume here
Next batch: audit PROCESS_GOVERNANCE (28, split ~14+14), then MISC (14). Then execute the consolidations above one cluster at a time (preserve constraints; confirm destructive calls with the owner), the family-rules->findings migration, and the discover_by_quality view. Keep every release gated to true PASS and end substantive replies with the PROTOCOL banner.
