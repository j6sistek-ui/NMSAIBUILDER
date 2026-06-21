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
