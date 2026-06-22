# OPEN TOPICS LOG — authoritative continuity artifact

The **single file** a new chat reads to answer, for every open item: **What happened? Why? What was decided? What do we do next?** One topic per open item, each in the required structure (Issue / Discovery / Why It Matters / Decision / Next Steps / Status / Priority / Success Criteria / Last Updated). Resolved history lives in `CHANGELOG.md`, not here.

Current active version: 5.19.03

---

## TOPIC: Lighting/effect part behavior and JSON-only buildable ObjectIDs

* Issue: AI often tries to create colored lighting by repainting light fixtures, and newly discovered/modded game-file ObjectIDs can be buildable even when the Blender plugin shows only cube proxies or lacks FBX/verified geometry.
* Discovery: User supplied in-game lighting screenshots and JSON evidence. Key findings: LIGHTBOX and L_FLOOR_Q change emitted color with selected object color; BASE_BEAMSTONE emits a colorable beam; most fixture/post/pole lamps only tint the fixture body and do not materially recolor emitted light; wall-light colors are ObjectID variants; SET_CLASS_A/B/S can compose volumetric beam/cone effects; RACE_BOOSTER has purple surface glow; BLD_PLANET_HOLO is a blue planetary/solar-system hologram; B_SHL_A/B/C/D are moving/rotating/spinning Corvette shield/effect parts; SWARM_TROPHY_G/B/R are JSON-confirmed game-file buildable trophy/ring light effects with no plugin/FBX geometry and Blender cube proxies.
* Why It Matters: This information improves creative part selection without weakening placement authority. It prevents false claims about recoloring emitted light, and it makes JSON-only effect parts available while clearly blocking structural/verified-geometry assumptions.
* Decision: DONE in 5.19.03 — routed effect behavior into `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json`, dimensions guidance, method authority, negative knowledge, and the placement aid ledger. Added provisional partmaps for SWARM_TROPHY_G/B/R and B_SHL_D only because those ObjectIDs lacked verified/plugin geometry; the verified extraction overlay was not hand-edited. Resolver now exposes `CREATIVE_CONTEXT.part_effect_findings` so these findings can reach build packets without becoming placement law.
* Next Steps: Continue mapping exact ObjectID-level lighting outcomes as more screenshots/JSON arrive. Do not promote any effect to `GAME_VALIDATED` placement mechanics without measured/exported validation. Use color-responsive emitters or variant ObjectIDs when emitted color matters.
* Status: RESOLVED for current intake; OPEN for future lighting/effect coverage growth.
* Priority: HIGH
* Success Criteria: Resolver packets for effect ObjectIDs expose lighting/effect findings; `discover_by_quality` returns these objects for relevant qualities; release gate passes; verified extraction overlay remains unchanged.
* Last Updated: 2026-06-22


## TOPIC: Build-sheet per-part reconciliation — state, remaining work, decision fork

* Issue: For months, builds fought every part because the build sheet (resolver packet) delivered only a thin slice of the per-part data that exists; data had drifted across ~11 files with no single reconciled view and no confidence signal, so "looks good but isn't" could not be detected.
* Discovery: Per-part data lives in: nms_master_part_map_verified_data_v3 (FBX geometry anchor, VERIFIED_DATA_OK), nms_part_dimensions_and_rules_updated (spacing/guidance/ring/role/family/lessons), authoritative_snap/relational_map_combined (snap points/matrices/connectivity), part_placement_master_sheet.csv (the "everything sheet" — orientation phase/neighbor/fitment, but mostly UNTESTED/NEED_STUDY), NMS_PLUGIN_641 (socket classes, 26 parts), METHOD_AUTHORITY_TABLE, CREATIVE_USE_CASE_AND_STYLE_INDEX (characteristics), plus recipe/rule layers. The owner's design: verified part map is the anchor we never deviate from; the build sheet must reconcile everything into one per-ObjectID record (King) to lighten context (carry only the parts in play, not 2097 rows).
* Why It Matters: This is the core of "is it finally working." Without one reconciled, confidence-tagged record, every chat re-derives placement and the owner can't tell solid data from guesses.
* Decision: DONE through 5.19.00 — part_context_resolver.py reconciles ALL sources into MANDATORY parts[oid].placement_spec: geometry (verified-map origin/bbox/FBX anchor), orientation (rotation + RX90/RY90/RZ90 footprints + master-CSV phase/pivot + override), scale (size per scale + behavior), placement_rules (concrete snap + SpacingRule fallback + guidance + local axis rules + neighbor + fitment + recipes), family, characteristics, method authority, role, cautions. Each section carries _source provenance; a validation block reports verified-map status (VERIFIED_DATA_OK) and master-CSV placement-trial status (UNTESTED/NEED_STUDY) so unvalidated data is visible. Releases 5.16 (curated guidance + template-leak gate), 5.17 (concrete snap), 5.18 (consolidated placement_spec), 5.19 (full multi-source reconciliation). All gate PASS, verified inside zip.
* Next Steps: TWO remaining before trials prove it: (1) CONNECTION COMPOSER — record currently flags connections_TODO; cross-plane composed transforms (wall.TOP @ inv(roof.SOUTH)) not yet mapped, so roofs/ramps/stairs don't seat from the sheet alone; must reproduce the measured seat (roof at 0, 2.669, 3.33) by geometry, not screenshot. (2) MASTER-CSV TRIAL-FILL — the orientation-phase/neighbor/fitment columns are UNTESTED for most parts; build trials must fill+validate them. DECISION FORK pending owner: build the connection composer next, OR run a measured-geometry trial of the floor/wall shell (both VERIFIED_DATA_OK) first to prove the reconciled sheet places connected parts correctly.
* Status: OPEN — reconciliation shipped (5.19.00); connection composer + master-CSV trial-fill + measured-geometry trials remain.
* Priority: HIGH
* Success Criteria: A build placing parts from the reconciled sheet alone connects correctly (verified by exported transforms, not screenshots); roof seats on wall top with correct pitch offline; master-CSV layer filled+validated for the parts in active builds.
* Last Updated: 2026-06-22

## TOPIC: No end-to-end part-data UPDATE RUNBOOK (trial result -> store field -> build sheet)

* Issue: Rules exist for WHERE part data lives and WHAT outranks what, but there is no single documented procedure for taking a trial-validated behavior (e.g. a roof's correct rz, a wall-light override, a connection seat) and writing it to a specific field in a specific store so the build sheet reconciles it. This is where drift re-enters: validated knowledge stays in chat/reports instead of flowing back into the data.
* Discovery: Three governing docs found and read: rules/VERIFIED_PARTMAP_DATA_PROTOCOL.md (the verified part map is the FBX-extraction anchor, not hand-edited; evidence order = current-build JSON > validated recipe/toolkit > verified extraction overlay > FBX extents > raw/manual/in-game; ValidationStatus gates trust; in-game/JSON evidence can override, per the PIPE/BUBPIPE precedent). rules/RULE_UPDATE_PROTOCOL.md (promote validated lessons into the correct EXISTING store by type; required record incl. status hypothesis->validated->promoted->deprecated; never a new file). rules/PART_PLACEMENT_MAP_SCHEMA.md (mandatory storage target for "how to place this part"; must be written to the placement-map library, not left in chat). They predate the build-sheet reconciliation and are not wired into one concrete fill-this-field-here runbook.
* Why It Matters: Without one runbook, every chat re-derives placement and validated findings don't persist into the store the build sheet reads — the exact drift the owner has been fighting. The build sheet (5.19) now surfaces VERIFIED_DATA_OK vs UNTESTED, so the trust gate exists; the missing piece is the documented path that turns an UNTESTED field into a validated one.
* Decision: DONE in 5.19.03 — RULE_UPDATE_PROTOCOL.md now contains the end-to-end promotion runbook: trial validates behavior -> write to the named existing store -> regenerate placement-map sheet/index if needed -> resolver/build sheet re-resolves the value. Verified extraction overlay remains non-hand-edited; JSON-only/provisional parts route through dimensions library, partmaps, method authority, negative knowledge, and creative index as appropriate.
* Next Steps: Use the runbook for upcoming connection-composer and master-CSV trial-fill work; future optional hardening can add a check that promoted validated fields include validation_status + resolver reachability proof.
* Status: RESOLVED (5.19.03) — runbook authored into existing RULE_UPDATE_PROTOCOL.md and gate-checked.
* Priority: HIGH (governance integrity / anti-drift)
* Success Criteria: MET for procedure; future trial promotions must show store field + resolver/build-sheet reachability proof before being called durable.
* Last Updated: 2026-06-22

## TOPIC: Verification trust — live-Blender "looks good" is unreliable; verify by measured geometry

* Issue: Live-Blender viewport screenshots and "looks good" reports have repeatedly been wrong — the owner looks and the build is a mess. This has destroyed trust in chat-reported success and is a primary reason the owner is second-guessing every build and considering reverting to v4.0.
* Discovery: Known failure modes: stale-transform reads (matrix_world not recomputed without bpy.context.view_layer.update()), frozen/cached viewport frames, scene-camera hijack of the MCP capture, mis-framing when multiple builds share a collection. A screenshot "looking good" does not prove correct transforms.
* Why It Matters: If verification isn't trustworthy, no amount of mapping convinces the owner it works. Validation must be data-driven and repeatable.
* Decision: PENDING promotion into durable docs. Standing method: verify by MEASURED GEOMETRY — read the exported objects JSON / AI-review bundle and check actual transforms and seams against expected values; use run_gate; treat screenshots as a last resort, only on explicit request. After any transform write, call view_layer.update() before reading matrix_world.
* Next Steps: Promote the verification-by-measured-geometry method into 02_TECHNIQUE_TOOLKIT.md / METHOD_AUTHORITY_TABLE; use it for the upcoming build trials (floor/wall shell, then roof seat) so results are proven by numbers, not by a screenshot.
* Status: OPEN — adopted in principle; not yet in durable docs; the upcoming trials must demonstrate it.
* Priority: HIGH (owner trust)
* Success Criteria: Build trials are validated by exported transforms matching expected snap/connection values; no success is claimed from a screenshot alone.
* Last Updated: 2026-06-22

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
