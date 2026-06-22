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

## File discipline (the package is at maturity)

Do not create new files — no new creative indexes, reports, stores, or locations — on a chat's initiative. Route new data into the stores above. New files require explicit USER approval, recorded by adding the path to `release/APPROVED_FILES.json` with an `approval_log` entry. This is enforced at release time by `validation/new_file_guard_check.py`, which FAILS the gate on any unapproved new file. New rules will still appear over time, but each new file is a deliberate, approved act.
