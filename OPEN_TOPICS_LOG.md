# OPEN TOPICS LOG — authoritative continuity artifact

The **single file** a new chat reads to answer, for every open item: **What happened? Why? What was decided? What do we do next?** One topic per open item, each in the required structure (Issue / Discovery / Why It Matters / Decision / Next Steps / Status / Priority / Success Criteria / Last Updated). Resolved history lives in `CHANGELOG.md`, not here.

Current active version: 5.18.00

---

## TOPIC: resolver guidance-forwarding — cross-chat reconcile
- **Issue:** The runtime packet had stopped forwarding the dimensions-library curated guidance (SpacingRule, PlacementGuidance, LikelyRole, ring formulas, KnownIssues, lessons); builds re-derived spacing/role by hand and fought every part. 5.16.00 patches part_context_resolver.py to forward it as advisory CREATIVE_CONTEXT + a snap-supersedes-extent note.
- **Discovery:** Root-caused in this package chat AND independently in a parallel live-Blender chat. The resolver read only the verified partmap's 4 geometry fields and never touched the dimensions library (2097 SpacingRule/LikelyRole entries, 181 PlacementGuidance, etc.). Spacing authority is the snap map (S_WALLM 5.3379) not the extent SpacingRule (5.691).
- **Why It Matters:** Two chats edited part_context_resolver.py in separate working copies; they must be reconciled to one source of truth.
- **Decision:** This chat shipped the package implementation (5.16.00); the parallel chat audits it against its live-proven patch.
- **Next Steps:** (a) parallel chat audits the resolver + template-leak gate against its room_v02 live result; (b) DONE — 5.18.00 consolidated the full per-part hand-off into MANDATORY parts[oid].placement_spec (orientation/scaling/placement+snap/role/cautions); (c) reconcile any divergence into one resolver.
- **Status:** OPEN — package fix shipped; live audit + reconcile pending.
- **Priority:** HIGH
- **Success Criteria:** One resolver in the package; a real floor/wall build connects with no snap gaps in-game; both chats agree on the implementation.
- **Last Updated:** 2026-06-21

## TOPIC: discover_by_quality coverage growth
- **Issue:** The `discover_by_quality` reverse index works but draws on only ~8 `part_geometric_character` entries, so coverage is thin.
- **Discovery:** Wave 3 built the view + sync gate; querying `smooth`/`beam`/`electric` returns correct candidates, but most parts have no character entry yet.
- **Why It Matters:** Discovery-first only pays off when most build qualities resolve to candidate parts.
- **Decision:** Grow `part_geometric_character` and `color_variant_families` across categories; the sync gate keeps the view consistent.
- **Next Steps:** Add character entries for common structural/decor parts; re-run `discover_by_quality_check.py --write`.
- **Status:** OPEN — view built; coverage thin.
- **Priority:** MEDIUM
- **Success Criteria:** Common qualities (curved, tall, glowing, organic, angular, etc.) each return candidate ObjectIDs across more than one category.
- **Last Updated:** 2026-06-21

## TOPIC: Assembly-recipe intent-keyword tuning (recall)
- **Issue:** Build-level assembly recipes now match the build intent via curated keyword lists; those lists are a first pass and may miss synonyms (precision is good; recall needs watching).
- **Discovery:** 5.08.01 moved assembly recipes off part-name substrings onto intent keywords, eliminating the airlock/dome/wall-shell noise on plain parts. Recall is keyword-bound (e.g. WALL_SHELL needed `perimeter`/building-type words added to fire for a church).
- **Why It Matters:** A recipe that should fire for a build but lacks the keyword silently won't surface.
- **Decision:** Grow the intent keyword lists as new build types appear; consider a small synonym map.
- **Next Steps:** Add keywords when a build type misses its recipe; spot-check across build intents.
- **Status:** OPEN — first-pass keywords in place.
- **Priority:** LOW
- **Success Criteria:** Common build types (church, tower, dome, bridge, city, vehicle, airlock) each surface their expected assembly recipes.
- **Last Updated:** 2026-06-21

## TOPIC: One creative store (catalog vs index reconciliation)
- **Issue:** Two creative stores exist: `PART_USE_CASE_CATALOG` and `CREATIVE_USE_CASE_AND_STYLE_INDEX.json`.
- **Discovery:** Effect/use findings were migrated into the index (Wave 2); the catalog remains a separate REFERENCE store. Reconciliation was deferred to avoid content loss.
- **Why It Matters:** Two stores risk drift and duplicate discovery paths.
- **Decision:** Make the index the source of truth; generate the catalog as a view from it, or retire it after diffing.
- **Next Steps:** fold the catalog's 16 seed `use_cases` into the index's discover_by_quality/findings (one queryable creative file), then slim the catalog to visual/video/case-study reference. ~43KB migration touching ~10 doc refs — do as a deliberate gated step.
- **Status:** PARTIAL (5.11.00) — declared `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` the single runtime STORE OF RECORD and `rules/PART_USE_CASE_CATALOG.json` a subordinate ideation reference (headers added). Evidence: they are complementary (runtime findings vs ideation/visual reference), not duplicate data.
- **Priority:** MEDIUM
- **Success Criteria:** One authoritative creative store; the other is generated from it or gone, with nothing lost.
- **Last Updated:** 2026-06-21

## TOPIC: Re-audit of Wave 2 + Wave 3 execution
- **Issue:** The consolidation, family migration (Wave 2), runtime mapping (Wave 3), and scope-precision tuning (5.08.01) are physically executed and should be re-reviewed.
- **Discovery:** The last ZIP audit confirmed Wave 3 executed and flagged scope breadth + metadata drift; both are now addressed. Resolver emits classification-filtered per-part behaviors + a build-level assembly lane; metadata (changelog/inventory/manifest) corrected.
- **Why It Matters:** Confirms no behavior/content loss and that scope precision holds before more is built on it.
- **Decision:** A separate chat audits using `reports/WAVE2_EXECUTION_REPORT.md` + `reports/WAVE3_EXECUTION_PREP.md` + the gates, inspecting a sample packet's per-part behaviors and the assembly lane.
- **Next Steps:** Run the audit; apply feedback.
- **Status:** OPEN — audit pending.
- **Priority:** HIGH
- **Success Criteria:** Auditor confirms behaviors are actionable + correctly scoped (no noise, no missing expected recipes), and constants/tiers preserved.
- **Last Updated:** 2026-06-21

## TOPIC: Runtime reachability as the value metric
- **Issue:** Package value should be measured by execution-path reachability, not file count. Files that never become runtime behavior / creative context / transfer / validation are waste regardless of size.
- **Discovery:** A reachability scan (`validation/runtime_reachability_audit.py`) found all 62 rules mapped to a runtime destination, but 14 true orphans (referenced nowhere) plus large historical sections (gate-output reports, 29 release notes, superseded partmap data) with no execution path.
- **Why It Matters:** This is the actual remaining inefficiency now that the architecture is solved — the auditor's frontier.
- **Decision:** Measure by reachability; archive what reaches nothing; wire-back the useful unreachable tools.
- **Next Steps:** Run the reachability audit each release (target 0 orphans); route point-in-time outputs to `archive/`; decide WIRE-vs-ARCHIVE per the discovery log P4.
- **Status:** OPEN — 14 orphans + history now PURGED (archive deleted); audit reports 0 true orphans. Metric not yet enforced per-release.
- **Priority:** MEDIUM
- **Success Criteria:** Every active file reaches an execution path; `runtime_reachability_audit.py` reports 0 true orphans at release time.
- **Last Updated:** 2026-06-21

## TOPIC: Package deep-dive cleanup (P1-P4)
- **Issue:** The file-by-file deep dive found supersession, duplication, and version drift across non-rules areas.
- **Discovery:** Captured in `reports/PACKAGE_DEEP_DIVE_DISCOVERY_LOG.md` with evidence per item. The lossless archival pass (orphans, historical reports/notes, creative stub) is done; the rest needs judgment.
- **Why It Matters:** Closing these removes the last redundancy/drift and shrinks the active surface another notch.
- **Decision:** Execute the proposal in priority order, gating each step: P1 (v3_01_01 partmap ~6MB, checkpoint stubs, transfer-requirement stub), P2 (recipe-library json/md sync, bootstrap entry-point sprawl, memory-recall json/md, one creative store), P3 (de-version active root docs + templates; resolver version stamp; promote version-callout WARN->FAIL), P4 (wire-back useful build snippets; track reachability per release).
- **Next Steps:** Start with P1 — repoint the v3_01_01 ledger provenance to v3_01_02 and archive ~6MB; retire the superseded checkpoint stubs from VERSION_LOCATIONS.
- **Status:** RESOLVED (5.10.00) — P1-P4 executed: v3_01_01 data + placeholder stubs purged, one recipe method established, obsolete unreferenced docs purged after extracting lessons, resolver stamp dynamic, archive removed.
- **Priority:** DONE
- **Success Criteria:** MET for P1-P3 (recipe store single-sourced; superseded data/docs purged; resolver stamp dynamic). Remaining: creative store single-sourcing (one-creative-store topic) and a WARN->FAIL promotion of the version-callout check are still open.
- **Last Updated:** 2026-06-21

## TOPIC: Validation tier classification (runtime vs test vs historical)
- **Issue:** `validation/` is the largest active category and was an implicit mix of build-runtime gates, release self-tests, and dead scripts.
- **Discovery:** Traced every script's invocation (`reports/RUNTIME_AUDIT_VALIDATION_TOOLKIT_LIBRARY.md`): 1 orchestrator + 8 build gates + 1 runtime lib + 14 release self-tests + 2 audit tools + 1 redundant (purged). Captured in `validation/VALIDATION_INDEX.json`.
- **Why It Matters:** Makes "used vs not used" objective and maintainable; the reachability audit now flags DRIFT if a new script is untiered.
- **Decision:** Keep the index as the tier of record; purge only REDUNDANT-tier scripts.
- **Next Steps:** Keep VALIDATION_INDEX in sync; resolve the two deferred evidence-backed items (catalog->index use_cases merge; partmap `.csv` purge after confirming partmap_storage_check).
- **Status:** OPEN — index created, 1 redundant script purged; deferred items remain.
- **Priority:** MEDIUM
- **Success Criteria:** Audit reports 0 true orphans and 0 DRIFT; every validation script carries a justified tier.
- **Last Updated:** 2026-06-21

## TOPIC: File maturity + anti-bloat new-file guard
- **Issue:** The package is near file maturity; chats should not create new files (indexes, reports, stores) on a whim, which causes bloat.
- **Discovery:** New user-provided data should land in existing stores, runtime-linked; new files should require explicit approval.
- **Why It Matters:** Prevents the duplicate-store / orphan problems the audits kept finding, at the source.
- **Decision:** `validation/new_file_guard_check.py` (gate #28) + `release/APPROVED_FILES.json` hard-fail the release on any unapproved new file; intake routing folded into `rules/RULE_UPDATE_PROTOCOL.md`.
- **Next Steps:** When approving a genuinely new file, add its path to APPROVED_FILES.json with an approval_log entry. Keep routing new data into existing stores.
- **Status:** RESOLVED (5.12.00) — guard active; intake routing documented and referenced from the kickoff gate.
- **Priority:** DONE
- **Success Criteria:** MET — release FAILS on unapproved new files; new data has one documented destination per kind.
- **Last Updated:** 2026-06-21

## TOPIC: Connectivity gate library-arg sensitivity
- **Issue:** The connectivity / no-float gate read geometry extents only from the `<library>` arg passed to run_gate, and SKIPPED ("no extents in library") whenever that file lacked `extent_x/y/z`.
- **Discovery:** A live build (gothic_castle_v02, 1374 parts) passed the verified part map, which lists every ObjectID but carries no extents — set-difference passed, connectivity silently skipped.
- **Why It Matters:** A skipped connectivity check means floating parts can ship undetected; the gate looked like it ran but checked nothing.
- **Decision:** run_gate now falls back to `library/nms_part_dimensions_and_rules_updated.json` for extents when the supplied library has none, so connectivity runs regardless of which library was passed. Operating card names the dimensions library as the correct `<library>` arg.
- **Next Steps:** None required; optional future hardening could warn when the passed library lacks extents even though fallback succeeded.
- **Status:** RESOLVED (5.13.00) — fallback live; unit-verified extents load for the failing parts.
- **Priority:** DONE
- **Success Criteria:** MET — connectivity runs when ≥2 parts are placed even if a no-extent library is passed.
- **Last Updated:** 2026-06-21

## TOPIC: AI-capture hand-off visibility (un-hideable parts)
- **Issue:** After AI-capture compliance became auto-required for build_generation, generated scripts staged semantic review collections and baked in `hide_viewport` / view-layer `exclude`, leaving parts the user could not recover with `Alt+H`.
- **Discovery:** Owner reported a delivered build arriving with hidden parts that wouldn't unhide; old doc versions (no auto-capture) never did this.
- **Why It Matters:** A delivered build must be fully visible and editable; review staging is a capture-time concern, not a hand-off state.
- **Decision:** New static-linter check FAILS the gate on baked `hide_viewport=True` / view-layer `exclude=True` in delivered scripts; AI_CAPTURE_COMPLIANCE_CONTRACT.md requires all collections ship visible + included, with review isolation done by the addon's recoverable `hide_set()`.
- **Next Steps:** If the review addon evolves, keep isolation on recoverable `hide_set()` + restore; never bake view-layer exclusion into delivered scripts.
- **Status:** RESOLVED (5.13.00) — lint live and gate-wired; FAIL verified on an injected hide flag, no false positive on the clean template.
- **Priority:** DONE
- **Success Criteria:** MET — delivered scripts with un-recoverable hiding fail the machine-checkable gate.
- **Last Updated:** 2026-06-21

## TOPIC: Build placement-quality regression (mechanically valid, creatively meaningless)
- **Issue:** Generated builds (gothic_castle_v02) passed every gate yet read as part-piles — odd angles, no design intent, parts with no purpose. Owner felt v4 placed better.
- **Discovery:** v4 diff confirmed authoritative snap data was preserved byte-identical and is better wired in 5.x. The build sheet carried only mechanical per-part context; purpose/style/appearance lived in an advisory CREATIVE_CONTEXT marked "OFFERED, not gated," so the AI could skip design entirely and still PASS. Spire recipes existed but were unrouted; no buttress recipe; orientation ungated; the v4 curve-follow contract had decayed to prose.
- **Why It Matters:** Robustness (connect/no-float/anti-bloat) advanced while design quality stayed optional — the "more robust, worse-looking" paradox.
- **Decision:** Promote design intent to a required, gated surface (DESIGN_INTENT gate, auto-required for build-type); add an orientation gate (RX/RY off-default without authorization, build-type only, JSON-recreation exempt); route the existing spire/taper recipes and add a flying_buttress guard; re-absorb the v4 curve-follow contract. All into existing files (no new files; starter NOT restored per owner).
- **Next Steps:** Lean on AI_CAPTURE visual review to confirm each assembly reads as its declared target_read (gates force the plan; only the eyes judge the look). Consider surfacing a DESIGN_INTENT scaffold from the resolver in a future pass. Validate on the next real castle build.
- **Status:** RESOLVED (5.14.00) — both gates live and self-tested; recipes routed; curve-follow restored.
- **Priority:** DONE
- **Success Criteria:** MET — build-type scripts FAIL without a committed plan, every part must carry a purpose, and unauthorized tilts are flagged.
- **Last Updated:** 2026-06-21

## TOPIC: Design "looks right" cannot be text-gated (visual review dependency)
- **Issue:** The new gates force a plan and catch tilts, but no text gate can verify a build actually LOOKS like its intent.
- **Discovery:** "Reads as a roof" is inherently visual; only AI_CAPTURE review can judge it.
- **Why It Matters:** Without wiring intent->visual confirmation, a build can declare a good plan and still be executed badly.
- **Decision:** Keep DESIGN_INTENT.target_read as the contract the AI visual review checks against before delivery; do not pretend a text gate proves appearance.
- **Next Steps:** Strengthen AI_CAPTURE to compare each declared assembly/target_read against its review collection and flag mismatches.
- **Status:** OPEN — gates force intent; visual-confirmation wiring not yet built.
- **Priority:** HIGH
- **Success Criteria:** AI review reports, per assembly, whether the build reads as its declared target_read.
- **Last Updated:** 2026-06-21


## TOPIC: Reuse-gate zero-proof-part semantics (owner decision pending)
- **Issue:** `validated_logic_reuse_check.py` (L73) FAILS any build that uses zero placement-map proof-ledger parts ("no known ObjectIDs detected"). The gate is auto-required for every build-type request.
- **Discovery:** A new chat following the onboarding spec dead-ended on this. 5.16.00 fixed onboarding by adding an `S_RAMP`, but the same trap hits ANY simple real build (floor/wall/roof/arch) that uses no ledger part.
- **Why It Matters:** Forces every build to include one of 12 ramp/trifloor/billboard parts or fail — stricter than the check's own docstring ("scripts USING validated parts").
- **Decision:** PENDING owner call. Option A (done): onboarding includes a ledger part. Option B (not done): relax L73 so zero proof-parts = N/A/WARN not FAIL, so reuse-proof is required only for ledger parts actually used.
- **Next Steps:** Owner decides keep-strict vs relax. If relax: change L73 to N/A, re-gate, release.
- **Status:** OPEN — onboarding sidestepped (A); broader gate semantics undecided (B).
- **Priority:** MEDIUM
- **Success Criteria:** Simple valid builds aren't forced to include a proof-ledger part solely to pass the reuse gate (if B chosen), OR the strict requirement is confirmed intentional and documented (if A-only).
- **Last Updated:** 2026-06-21
