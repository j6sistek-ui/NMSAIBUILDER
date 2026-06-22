# Placement Recipe Library — pointer

The authoritative recipe store is **`toolkit/PLACEMENT_RECIPE_LIBRARY.json`** (machine-readable, consumed by `part_context_resolver.py`, `compliance_manifest_check.py`, and the gate). This file is intentionally a pointer, not a parallel copy, to prevent the json/md drift that previously existed.

For how recipes are stored and utilized end-to-end, see the canonical method: **`MASTER_BUILD_RECIPES_AND_PLACEMENT_GUIDANCE.md`**.

To read or edit recipes, use the JSON store. Do not hand-maintain recipe definitions here.
