# OPEN TOPICS LOG — authoritative continuity artifact

The **single file** a new chat reads to answer, for every open item: **What happened? Why? What was decided? What do we do next?** One topic per open item, each in the required structure (Issue / Discovery / Why It Matters / Decision / Next Steps / Status / Priority / Success Criteria / Last Updated). Resolved history lives in `CHANGELOG.md`, not here.

Current active version: 5.07.00

---

## TOPIC: Runtime destination / mapping audit (Wave 3)
- **Issue:** Rules are classified (kind + runtime_status), but the resolver/build packet does not yet consume that classification. A correctly classified rule that never reaches a packet is inert.
- **Discovery:** The external audit confirmed classification is real, but the packet still emits `applicable_part_rules` (a rule-name list) with blank `build_application`, and the resolver includes rules by broad family match rather than filtering by kind/runtime_status/authority.
- **Why It Matters:** Classification is *understanding*; runtime mapping is *execution*. Without it, the cleanup does not change AI behavior.
- **Decision:** Every retained rule/finding/recipe gets a defined runtime destination: RULE/RECIPE/NEGATIVE -> build packet as behavior; FINDING -> creative context; PROCESS/GOVERNANCE -> operating card / gates; REFERENCE -> on-demand lookup.
- **Next Steps:** See `reports/WAVE3_EXECUTION_PREP.md`. Build a `data/RUNTIME_BEHAVIORS.json` (rule_id -> required_behavior/check/authority); make the resolver emit `applicable_rule_behaviors` filtered by kind/runtime_status; regenerate all packets/fixtures.
- **Status:** OPEN — Wave 3, not started.
- **Priority:** CRITICAL
- **Success Criteria:** A build packet for any ObjectID lists only directly-applicable RULE/RECIPE/NEGATIVE survivors, each with an actionable `required_behavior` and `check`; no process/governance/finding/reference leaks into part context.
- **Last Updated:** 2026-06-21

## TOPIC: Resolver emits behaviors, not rule lists (Wave 3)
- **Issue:** Resolver output for a part is `applicable_part_rules: ["RULE_A","RULE_B"]` — the AI sees "this rule applies," not "here is what this part must do."
- **Discovery:** Auditor Fix 1. The packet `build_application` is authored per part but the rule layer itself is not turned into behavior.
- **Why It Matters:** Behavior is executable; a rule name is a lookup the AI may skip.
- **Decision:** Replace the rule-name list with `applicable_rule_behaviors` objects (`rule_id`, `kind`, `authority`, `required_behavior`, `check`, `applies_to`).
- **Next Steps:** Author `required_behavior`/`check` per KEEP RULE/RECIPE/NEGATIVE; wire the resolver (`validation/part_context_resolver.py`, ~line 118) to emit them; update `validation/build_sheet_check.py` to compare behaviors; regenerate `runs/*.PACKET.json` and `validation/gate_fixtures/*` packets.
- **Status:** OPEN — Wave 3, not started.
- **Priority:** CRITICAL
- **Success Criteria:** `part_context_resolver.py --ids S_WALLM` returns behavior objects with non-empty `required_behavior` for each applicable rule.
- **Last Updated:** 2026-06-21

## TOPIC: Build packet filters by classification (Wave 3)
- **Issue:** Packets can still dump process/governance/finding/reference material into part context.
- **Discovery:** Auditor Fix 2. RPAM scoping is by family/part, not by kind/runtime_status.
- **Why It Matters:** Part context should carry only what governs *this part's placement*, nothing else — that is the leanness objective.
- **Decision:** Packet inclusion filter = kind in {RULE, RECIPE, NEGATIVE} AND runtime_status == KEEP AND directly applicable.
- **Next Steps:** Add the filter in the resolver; emit excluded kinds only in their own lanes (creative/operating-card).
- **Status:** OPEN — Wave 3, not started.
- **Priority:** HIGH
- **Success Criteria:** No PROCESS/GOVERNANCE/FINDING/REFERENCE rule_id appears in a part's `applicable_rule_behaviors`.
- **Last Updated:** 2026-06-21

## TOPIC: Onboarding build gauntlet (Wave 3)
- **Issue:** Onboarding can still pass as a checklist exercise (READ/SKIPPED counts), proving Source Readiness but not Builder Readiness.
- **Discovery:** Auditor Fix 3. The onboarding doc requires a micro-build but the pass condition is not enforced as artifacts+gate+failure-handling.
- **Why It Matters:** "Package read" is not "can build correctly."
- **Decision:** Pass condition = generated build artifacts -> first gate -> failure handled if any -> diagnosis -> correction -> second gate -> builder-readiness verdict.
- **Next Steps:** Promote ONBOARDING_VALIDATION_BUILD to a gauntlet with that pass condition; add an enforcing check.
- **Status:** OPEN — Wave 3, not started.
- **Priority:** HIGH
- **Success Criteria:** Onboarding cannot report "ready" without a passing micro-build gate run recorded.
- **Last Updated:** 2026-06-21

## TOPIC: discover_by_quality view + sync gate
- **Issue:** Creative discovery ("futuristic -> colorful + light-emitting -> beam emitters") needs an effect->ObjectIDs view before ObjectID selection.
- **Discovery:** The creative index now holds part character + migrated effect/use findings, but there is no generated reverse index from effect to parts.
- **Why It Matters:** Discovery-first only works if intent maps to qualities maps to parts before selection.
- **Decision:** Generate a `discover_by_quality` view inside the creative index with a sync gate keeping it consistent with the source entries.
- **Next Steps:** Build the generator + gate; expand `part_geometric_character` / `color_variant_families`.
- **Status:** OPEN — not started.
- **Priority:** MEDIUM
- **Success Criteria:** Querying an effect returns candidate ObjectIDs from the index, and the gate fails if the view drifts from source entries.
- **Last Updated:** 2026-06-21

## TOPIC: One creative store (catalog vs index reconciliation)
- **Issue:** Two creative stores exist: `PART_USE_CASE_CATALOG` and `CREATIVE_USE_CASE_AND_STYLE_INDEX.json`.
- **Discovery:** Effect/use findings were migrated into the index this wave; the catalog remains as a separate REFERENCE store.
- **Why It Matters:** Two stores risk drift and duplicate discovery paths.
- **Decision:** Reconcile to one creative store (index as the source; catalog as a generated view or retired).
- **Next Steps:** Diff catalog vs index; choose source-of-truth; generate the other or retire it.
- **Status:** OPEN — partially addressed (effect findings migrated).
- **Priority:** MEDIUM
- **Success Criteria:** One authoritative creative store; the other is generated from it or gone.
- **Last Updated:** 2026-06-21

## TOPIC: Re-audit of wave-2/3 physical execution
- **Issue:** The consolidation merges and family migration are now physically executed; this should be re-reviewed.
- **Discovery:** 30 rule docs absorbed into 13 survivors (content preserved, gate caught 6 real downstream breaks); family rules demoted to findings.
- **Why It Matters:** Confirms no content/behavior loss before Wave 3 builds on the new structure.
- **Decision:** A separate chat audits using `reports/WAVE2_EXECUTION_REPORT.md` + `reports/WAVE3_EXECUTION_PREP.md` + the gates.
- **Next Steps:** Run the audit; apply feedback; begin Wave 3 runtime mapping.
- **Status:** OPEN — audit pending.
- **Priority:** HIGH
- **Success Criteria:** Auditor confirms preserved constants/tiers and correct survivors; Wave 3 cleared to start.
- **Last Updated:** 2026-06-21
