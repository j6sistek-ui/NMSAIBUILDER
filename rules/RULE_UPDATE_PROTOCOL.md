# Rule Update Protocol

A lesson becomes documentation when it is understood and correctly applied.

## Promote immediately when

- an offset correction is finally understood
- an orientation fix is proven
- a scale/spacing formula stops a recurring error
- a part-specific behavior is validated by screenshot/in-game result
- a design rule becomes repeatable and useful

## Where to promote

| Lesson type | Destination |
|---|---|
| universal workflow | `UNIVERSAL_RULES.md/json` |
| part placement/orientation/family behavior | `PART_FAMILY_RULES.md/json` |
| known failure and fix | `ISSUE_FIX_LIBRARY.md` |
| experimental or effect behavior | `MASTER_LESSONS_LEARNED.md` (removed historical reference: EXPERIMENTAL_LESSONS_REGISTRY.json) |
| creative design potential | `PART_USE_CASE_CATALOG.md/json` |
| prohibited/placeholder object | `PROHIBITED_AND_PLACEHOLDER_OBJECTS.md/json` |
| project-only preference | project context file outside master package |

## Required record

Each promoted rule should include:

- rule ID
- scope
- affected ObjectIDs/families
- problem it prevents
- formula/placement guidance where applicable
- status: hypothesis, validated, promoted, deprecated
- source/validation note

## New data intake routing (recipe / part-characteristic) — route into existing stores, never a new file

When the user provides new recipe data or new part-characteristic/creative data, it MUST land in the correct EXISTING store, fully runtime-linked, and MUST NOT spawn a new report, index, or file.

**Classify first — the rule-vs-finding test:** *if removing it changes what is ALLOWED or REQUIRED, it is a RULE; if it only changes what you KNOW, it is a FINDING.* Findings never enter the rules layer and never gain placement authority.

**Routing map (the one correct spot for each kind):**
- New **recipe / assembly** → `toolkit/PLACEMENT_RECIPE_LIBRARY.json` (the single store of record). Register it across every layer it needs: `data/FEATURE_RECIPE_ROUTE_INDEX.json` (feature→recipe), `data/JSON_RECIPE_SIGNATURE_INDEX.json` (signature→recipe), and `data/RUNTIME_BEHAVIORS.json` if it is build-level. Scope it by explicit intent keywords / `assembly_scope` — NEVER by part-name substrings (that caused the "'wall' drags in airlock/dome" drift). If an importable implementation is warranted, add it under `toolkit/validated_recipes/`.
- New **part-characteristic / creative finding** → `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` (the single creative store of record): `part_geometric_character`, `part_effect_and_use_findings`, or `discover_by_quality`. Authority is INFORMATIVE — it suggests what to build, never overrides placement/recipes/snap/exceptions. Seed ideation goes to the subordinate `rules/PART_USE_CASE_CATALOG.json`, not a new index.
- New **placement mechanic that changes what is allowed/required** (a RULE by the test above) → the relevant existing rule in `rules/`; classify it in `data/RULE_CLASSIFICATION.json` and map applicability in `data/RULE_PART_APPLICABILITY_MAP.json` so the resolver emits it.

**Runtime-linked requirement:** after routing, the data must be reachable — `validation/runtime_reachability_audit.py` must report 0 true orphans and 0 DRIFT. Data that maps to nothing is not "documented," it is bloat.



## End-to-end placement behavior promotion runbook

This section closes the drift gap between a successful trial and the build sheet. A learned placement or effect behavior is not durable until it travels through this path and can be re-resolved by `validation/part_context_resolver.py`.

### Evidence order

Use the existing component-mechanics evidence order from `rules/VERIFIED_PARTMAP_DATA_PROTOCOL.md`:

1. current-build / control JSON for exact transforms,
2. validated recipe / signature / toolkit entry for assembly behavior,
3. verified extraction overlay for ObjectID spawn/origin/rotation/scale/bbox,
4. original FBX-derived extents and centers,
5. raw FBX / manual / in-game confirmation only if unresolved.

The verified extraction overlay remains an extraction artifact. Do **not** hand-edit `library/nms_master_part_map_verified_data_v3_01_02.csv` or `.json` for trial findings.

### Store routing

After a trial or user evidence provides reusable part behavior, write it to the correct existing runtime store:

| Learned behavior | Store | Resolver/build-sheet route |
|---|---|---|
| exact transform/orientation/neighbor/fitment behavior for a part | `library/part_placement_maps/<ObjectID>.partmap.json`; regenerate `library/part_placement_maps/part_placement_master_sheet.csv` and `part_placement_map_index.json` with `generate_partmaps.py` | `MANDATORY_PLACEMENT_CONTEXT.parts[oid].placement_spec` |
| bounds/role/guidance for ObjectIDs absent from the plugin or verified overlay | `library/nms_part_dimensions_and_rules_updated.json` and `.csv`; mark `VerifiedExtractionStatus` as non-verified/provisional | dimensions-library fallback in `placement_spec`; must not claim verified geometry |
| creative/effect/lighting/animation behavior | `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` under `part_effect_and_use_findings`, `color_variant_families`, or `part_geometric_character` | `CREATIVE_CONTEXT.part_effect_findings` and `discover_by_quality` |
| method authority / JSON-only caution | `data/METHOD_AUTHORITY_TABLE.json` and, where needed, `data/NEGATIVE_KNOWLEDGE_INDEX.json` | method authority and forbidden/caution surfaces |
| operational lesson / anti-drift reminder | `data/PART_PLACEMENT_AID_LEDGER.json` and `MASTER_LESSONS_LEARNED.md` when appropriate | operational bridge / human-readable continuity |

### Required promotion receipt

Every promoted behavior record must include:

- ObjectID or family,
- evidence source,
- exact value or guidance being promoted,
- validation status (`UNTESTED`, `SCRIPT_VALIDATED`, `BLENDER_USER_CHECK`, `GAME_VALIDATED`),
- target store and field,
- re-resolution proof: `part_context_resolver.py --ids <ObjectID> --intent "..."` shows the value in the expected packet surface.

A finding may remain informative, but it must not be represented as a rule unless removing it changes what is allowed or required. Creative findings never override placement precedence, snap authority, negative knowledge, or verified geometry.

## File discipline (the package is at maturity)

Do not create new files — no new creative indexes, reports, stores, or locations — on a chat's initiative. Route new data into the stores above. New files require explicit USER approval, recorded by adding the path to `release/APPROVED_FILES.json` with an `approval_log` entry. This is enforced at release time by `validation/new_file_guard_check.py`, which FAILS the gate on any unapproved new file. New rules will still appear over time, but each new file is a deliberate, approved act.
