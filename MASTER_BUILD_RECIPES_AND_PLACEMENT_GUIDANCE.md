# MASTER BUILD RECIPES AND PLACEMENT GUIDANCE

Status: active build guidance index.

## Priority order

1. Request-router classification and feature-intent route.
2. Current-build working JSON exact transforms, when available.
3. Current-build JSON local cluster recipe/signature.
4. Validated recipe/signature/toolkit entry for the requested feature.
5. Part-specific rules and orientation overrides.
6. Part map / placement aid ledger for component validation, dimensions, centers, spacing, role, and ObjectID validation.
7. FBX/manual mesh inspection only as fallback.
8. Generic geometric fallback only with uncertainty declared.

Recipes are assembly intelligence. The part map is component geometry intelligence. The part map supports and validates the recipe; it does not replace a known recipe.

## Required recipe fields

Every promoted recipe should define:

- feature name and scope;
- ObjectIDs and candidate part family;
- locked invariants;
- allowed parameters;
- geometry basis: exact_json, local_frame, endpoint_path, grid, ring, shell, surface_normal, curve_follow, edge_contact_graph, or hybrid;
- contact/anchor model;
- orientation basis;
- scale behavior;
- known failure modes;
- validation checks.

## Core active recipe families

- Airlock / iris door: use exact JSON or parametric overlap recipe; validate overlap, contact, and runtime placement.
- Continuous paths / bridges / rails: endpoint-path basis and socket/landing proof required.
- C_TRIFLOOR/freeform focal geometry: use validated logic, edge-contact graph, surface mesh contract, or curve-follow transform propagation.
- Stairs/ramps: bottom landing → run → top landing → rails/supports → attached route. No disconnected decorative stairs.
- Ground-zero foundations: use for unknown terrain/floating city placement, but shape and tier foundation to avoid one blank slab.
- Corvette builds: preserve required functional categories and total footprint limit.

## Part map enrichment backlog

The part map should absorb recurring fallback knowledge so future builds do not repeatedly search FBX or historical reports:

- native local axis;
- default placement orientation;
- part-specific overrides;
- valid scale behavior;
- contact/anchor roles;
- recipe links;
- screenshot/JSON-proven failure notes;
- connection model.


## AI visual review readiness

Recipe-first generation now includes review-readiness. A generated build script is incomplete if a human/AI cannot inspect its exterior, interior, cutaways, review-required parts, and scene/context separation.

Before coding full-building or scene-scale builds:

1. choose the feature recipe;
2. choose the part families;
3. choose semantic build areas;
4. declare `AI_CAPTURE_COMPLIANCE`;
5. create semantic collections/metadata in the script;
6. run `validation/run_gate.py`, which surfaces AI capture compliance;
7. use an AI review bundle only as visual/design-loop evidence, not as a replacement for exported JSON gates.



## Connected PIPE/BUBPIPE assembly guidance

Do not build validated pipe runs from Blender extraction data alone. For `PIPE` and `BASE_BUBPIPE*`, treat component spawn data as provisional raw evidence. A pipe run must include a focused validation loop: place straight, elbow, T, and X variants; test RX90/local rotation; export JSON or capture in-game screenshots; confirm that bends visually connect and maintain continuity. Until this validation exists, pipe assemblies must be labeled provisional.


## recipe guidance — connected pipe / bubble duct assemblies

For `PIPE` and `BASE_BUBPIPE*`, use the pipe contextual connector rule before generation. Build connected pipe systems as local-axis node/edge graphs with approximately 2.0-unit steps. Do not rely on Blender column/cylinder preview, Blender bbox, or an isolated RX90 correction to claim continuity. Validate through in-game screenshot, exported JSON, or a focused pipe harness.

Rule: `rules/PROHIBITED_AND_PLACEHOLDER_OBJECTS.md`

## placement precedence and method authority

Recipes and authoritative snap data remain higher authority than component part maps. Use `data/METHOD_AUTHORITY_TABLE.json` and `data/PLACEMENT_PRECEDENCE.json` to determine which method is allowed for the part role/context. Creative recipes can choose motifs, but physical placement must follow placement intelligence.
