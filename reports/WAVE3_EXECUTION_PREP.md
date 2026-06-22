# WAVE 3 EXECUTION PREPARATION

> STATUS (5.08.00): Fixes 1, 2, 4 and the onboarding gauntlet (Fix 3) and discover_by_quality are EXECUTED and gated. Remaining: family-scope precision residual, discover_by_quality coverage growth, one-creative-store reconciliation, external re-audit (see OPEN_TOPICS_LOG.md).

Purpose: hand the next chat everything needed to execute Wave 3 (runtime mapping) without rediscovering the package. Written immediately after Wave 2 *physical* execution, while the internals are fully in context. Read this together with `OPEN_TOPICS_LOG.md` (the why) and `reports/WAVE2_EXECUTION_REPORT.md` (the what).

---

## 1. Where the package is now (post-Wave-2)

- Version at time of writing: 5.06.01 working tree, releasing as **5.07.00** (major structural execution).
- **Rule layer: 62 unique rules** (was 92). 30 duplicate-law docs were physically absorbed into **13 survivors**, content-preserving. Absorbed `.md` and their `.json` sidecars are gone; their bodies live as `## … (absorbed from X)` sections inside the survivor.
- **Classification spine is live and enforced:** every rule carries `kind` + `runtime_status` in `data/RULE_PART_APPLICABILITY_MAP.json` (RPAM) and `data/RULE_CLASSIFICATION.json` (ledger). `validation/rule_classification_check.py` (gate #24) fails if any rule is unclassified or the two disagree.
- **Family rules demoted:** `rules/PART_FAMILY_RULES.json` is now `authority: INFORMATIVE_FINDINGS_NOT_PLACEMENT_AUTHORITY`; its 7 effect/use families were mirrored into `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` under `part_effect_and_use_findings`; its 9 placement families are cross-linked to the validated mechanics that supersede them (`placement_authority_superseded_by`).
- **Gates green:** `release/release_check.py` PASS, including run_gate self-tests, build-sheet/resolver consistency, partmap drift, RPAM coverage, version-callout, open-topics structure (#25).

### The 13 survivors (current rule set anchors)
`JSON_TO_PYTHON_RECREATION_PROTOCOL`, `PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE`, `PART_PLACEMENT_MAP_SCHEMA`, `AIRLOCK_IRIS_EXACT_JSON_RECIPE_RULE`, `FOCAL_BUILD_GEOMETRY_STRATEGY_PROTOCOL`, `SELECTIVE_VISUAL_MEMORY_POLICY`, `SYSTEMATIC_FAILURE_CAPA_PROTOCOL`, `AI_CAPTURE_COMPLIANCE_CONTRACT`, `RECIPE_PARAMETERIZATION_PROTOCOL`, `VALIDATION_GATE_HARDENING_RULE`, `REQUEST_ROUTER_CHECKLIST`, `STAIR_PLACEMENT_DOCTRINE`, `PROHIBITED_AND_PLACEHOLDER_OBJECTS`.

---

## 2. The Wave 3 mission (one sentence)

Make the resolver/build packet **consume** the classification: emit, per part, the **required behavior** of only the directly-applicable KEEP RULE/RECIPE/NEGATIVE survivors — not a flat list of rule names, and never process/governance/finding/reference material.

This is the auditor's "runtime mapping" / "resolver audit." Classification was *understanding*; this is *execution*.

---

## 3. Runtime destination map (the spine of Wave 3)

Every retained item has exactly one runtime home. Wave 3 enforces this.

| kind | runtime destination | appears in part packet? |
|---|---|---|
| RULE | build packet as a behavior | yes (if directly applicable + KEEP) |
| RECIPE | build packet as a behavior/recipe ref | yes (if applicable + KEEP) |
| NEGATIVE | build packet as a prohibition behavior | yes (if applicable + KEEP) |
| FINDING | creative context / `part_effect_and_use_findings` | no — offered, not forced |
| PROCESS | operating card / gate pipeline | no |
| GOVERNANCE | operating card / gate pipeline | no |
| REFERENCE | on-demand lookup | no |

Acceptance: no PROCESS/GOVERNANCE/FINDING/REFERENCE `rule_id` ever appears in a part's behavior list.

---

## 4. Concrete change set

### Fix 1 — resolver emits behaviors (CRITICAL)
- File: `validation/part_context_resolver.py`. Today it builds, per ObjectID, `"applicable_part_rules": sorted(set(prules))` (~line 118) inside `MANDATORY_PLACEMENT_CONTEXT.parts[ObjectID]`.
- Replace with `"applicable_rule_behaviors": [ {rule_id, kind, authority, required_behavior, check, applies_to}, … ]`.
- Source of `required_behavior`/`check`/`authority`: a new **`data/RUNTIME_BEHAVIORS.json`** (seeded this release — see §5) mapping `rule_id -> {required_behavior, check, authority}`. The resolver reads it and joins on rule_id.
- Keep `applicable_part_rules` temporarily as a secondary/compat field if needed, but the primary output is behaviors.

### Fix 2 — filter by classification (HIGH)
- In the resolver, before emitting, filter candidate rule_ids to: `kind ∈ {RULE, RECIPE, NEGATIVE}` AND `runtime_status == KEEP` AND directly applicable to the part/assembly. Read kind/runtime_status from RPAM (already present per entry).
- Excluded kinds go to their own lanes only (creative context; operating card). This is the leanness win the auditor is asking for.

### Fix 3 — onboarding gauntlet (HIGH)
- Promote `ONBOARDING_VALIDATION_BUILD` to a gauntlet. Pass condition is NOT "package read." It is: generate build artifacts -> run_gate (first gate) -> if fail, diagnose + correct -> run_gate (second gate) -> emit a builder-readiness verdict. Add an enforcing check so "ready" cannot be declared without a recorded passing micro-build gate.

### Fix 4 — build_sheet_check follows the new shape
- File: `validation/build_sheet_check.py` currently compares the packet's `applicable_part_rules` to the resolver. When the resolver switches to `applicable_rule_behaviors`, update this check to compare the behavior set (rule_id + required_behavior) against the resolver. Otherwise every covered build/fixture will fail.

---

## 5. Seed shipped this release for Wave 3

`data/RUNTIME_BEHAVIORS.json` is created now as a **seed** (schema + a few survivor entries) so Wave 3 starts from structure, not a blank page. Wave 3 fills it for every KEEP RULE/RECIPE/NEGATIVE. The resolver does not yet read it (that is Fix 1).

---

## 6. Gotchas learned the hard way in Wave 2 (do not relearn these)

1. **Packets and fixtures cite rule names.** After ANY rename/merge, regenerate every build packet (`runs/*__PACKET.json`) and fixture packet (`validation/gate_fixtures/build_sheet_good.json`) via `part_context_resolver.py --ids <ids> --intent <intent> --out <packet>`. The build-sheet/resolver consistency gate will FAIL on stale lists otherwise.
2. **`build_application` is AI-authored per part and the resolver WIPES it on regeneration.** After regenerating a packet, restore `build_application` per part from the prior packet (recover from the last shipped zip if overwritten). This will be true for `applicable_rule_behaviors` too.
3. **Rules can have a `.json` sidecar** in `rules/`. RPAM coverage requires every `rules/*.json` to be in RPAM. When absorbing/renaming, handle the sidecar (preserve into survivor + delete) or coverage fails.
4. **`validation/placement_intelligence_infrastructure_check.py`** has a hard-coded REQUIRED file list. Renames/merges of any listed file must repoint it.
5. **Router bundle map** `data/REQUEST_ROUTER_CHECKLIST.json` (and `rules/UNIVERSAL_RULES.json`) reference rule names; repoint on rename.
6. **Partmap index** drifts if `library/part_placement_maps/generate_partmaps.py` provenance strings change; run it (no `--check`) to regenerate, then `--check`.
7. **Survivor provenance is protected from blanket repoint** — so internal `.md` cross-links inside survivors must be repointed separately (bare-name "absorbed from X" headers are fine; `X.md` links are not).
8. **Version-callout gate (#23)** fails active docs that contain version numbers; absorbed historical content can drag version strings into a survivor — de-version them.

---

## 7. Success criteria for Wave 3 (when are we done)

- `part_context_resolver.py --ids <part>` returns `applicable_rule_behaviors` with a non-empty `required_behavior` for each applicable rule.
- No PROCESS/GOVERNANCE/FINDING/REFERENCE rule_id appears in any part's behavior list.
- `data/RUNTIME_BEHAVIORS.json` covers every KEEP RULE/RECIPE/NEGATIVE.
- `build_sheet_check.py` validates behaviors; all covered builds/fixtures PASS.
- Onboarding cannot report "ready" without a recorded passing micro-build gate.
- Net effect: a fresh chat **reads less, holds less, reasons less, while following more** of the actual package — the standing objective of this whole effort.

---

## 8. Recommended Wave 3 order

1. Author `data/RUNTIME_BEHAVIORS.json` for the 13 survivors + remaining KEEP RULE/RECIPE/NEGATIVE.
2. Resolver Fix 2 (filter) — smallest, lowest-risk, immediately reduces packet bloat.
3. Resolver Fix 1 (emit behaviors) + `build_sheet_check` Fix 4 together; regenerate all packets/fixtures; restore `build_application`; re-gate.
4. Onboarding gauntlet (Fix 3).
5. discover_by_quality view + sync gate; then one-creative-store reconciliation.
6. External re-audit.
