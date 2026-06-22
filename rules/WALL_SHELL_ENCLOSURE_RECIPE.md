# Wall Shell Enclosure Recipe (2.19.00)

Status: **active validated pattern requirement for enclosed buildings, towers, rooms, and city blocks**.

## Purpose

Future chats must not relearn wall enclosure from scratch. If the user requests a building, tower, room, dense city block, Gotham tower, enclosed structure, or shell, use this recipe before using raw wall part dimensions.

## Assembly priority

```text
recipe controls assembly
part map validates component geometry
raw FBX only resolves missing geometry/origin details
```

## Required shell layers

A building shell must distinguish these roles:

```text
foundation / plinth
floor slab or floor grid
structural wall shell
corner closure
window/opening substitutions
facade relief / trim
roof/top closure
rooftop attachments
access path / door relationship
```

## Required invariants

```text
- Walls form closed loops or clearly declared open facade segments.
- Wall panels contact floor, foundation, adjacent wall, or structural shell grid.
- Corners must be closed by overlapping, perpendicular, or explicitly joined wall segments.
- Floors must align under the wall footprint unless intentionally voided.
- Roof/top closure must cap or intentionally expose the shell.
- Facade-only wall panels must be tagged as facade, not structural enclosure.
- Window walls may replace structural wall panels only inside the wall grid.
- Decorative relief must not be counted as enclosure unless it also satisfies contact/closure.
```

## Recommended wall family use

```text
structural wall: wall-family flat panels such as S_WALL/S_WALLM/B-wall equivalents
window wall: wall-window family substitutions inside the shell grid
short trim/cornice: short wall or quarter wall family
pilaster/buttress: support family tied to shell/foundation contact
roof cap: floor/roof/short-wall family depending style
```

## Failure modes

```text
- isolated wall panels presented as a building
- towers made of facade relief with no structural shell
- visible corner gaps
- walls floating above floors or foundation
- decorative wall pieces used as enclosure without contact proof
- missing roof/top closure when enclosure was requested
```

## Required receipts in generated scripts

```python
FEATURE_RECIPE_LOOKUP = {
    "feature_intent": "building_enclosure / tower_shell / wall_shell",
    "matched_recipe_or_signature": "wall_shell_enclosure_recipe_v2_19_00",
    "recipe_files_checked": [
        "rules/WALL_SHELL_ENCLOSURE_RECIPE.md",
        "MASTER_BUILD_RECIPES_AND_PLACEMENT_GUIDANCE.md",
        "data/PART_PLACEMENT_AID_LEDGER.json"
    ],
    "recipe_status": "validated_recipe",
    "reason_if_none": "",
    "part_map_role": "component_validation_only"
}
```

A `BUILD_INTENT_GRAPH` should identify shell, floors, roof/cap, and major paths as connected components.
