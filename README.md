# NMS Master Docs 5.18.00

The current master reference for AI-assisted No Man's Sky Base Builder Python generation. This README is an orientation overview; the operating authority is `00_START_HERE_CURRENT.md`, and per-release history is in `CHANGELOG.md`.

## What this package is

A consolidated, lean operating package: governing doctrine, a request router, placement-intelligence governance, authoritative snap placement, validated recipes, and an executable release gate. There is no separate runtime pack — this is the single source.

## Environment & library

- Base Builder add-on 6.4.1.
- Blender 5.0.1 is the user's confirmed working environment. Blender 5.1.1 can work only after confirming the FBX import/export add-on is enabled, because the plugin uses FBX retrieval internally.
- Generated scripts use plugin `BUILDER.add_part()` template-copy generation and must not import FBX directly.
- Active part library: `library/nms_part_dimensions_and_rules_updated.json` (2,097 documented ObjectID rows). Short lists in docs are examples, never a whitelist.

## How to use it

1. Start with `00_START_HERE_CURRENT.md` (the router and operating requirements).
2. Run `00_KICKOFF_INTAKE_GATE.md` and emit the INTAKE BLOCK.
3. Load only the context/risk gating docs the router names. Lessons follow the part, assembly pattern, terrain condition, or design problem — project categories are not knowledge silos.
4. Generate only with real NMS Builder ObjectIDs through `BUILDER.add_part()` templates, and include a provenance manifest (`templates/OBJECT_USE_MANIFEST_TEMPLATE.md`).
5. Check for relevant working JSON first and mine it as the first placement/recipe source; after generation, validate exported JSON and screenshots against intent (JSON is serialized transform truth; screenshots are visual outcome).
6. Run `validation/run_gate.py` and paste its real output.

`00_START_HERE_CURRENT.md` is authoritative for the session loop and the rules; the list above is a summary.

## Directory map

| Directory | Purpose |
|---|---|
| `/library` | ObjectID library, FBX bounds, dimensions, plugin updates, and part index |
| `/rules` | Universal rules, validation protocols, part orientation overrides, continuous path assembly, JSON geometry validation, visual intake, recipe parameterization, prohibited objects |
| `/toolkit` | Placement recipes and visual build techniques |
| `/project_briefs` | Current/active project briefs such as Alien Megatemple V04 |
| `/validation` | Starter scripts, run gate, lint/audit snippets, and helpers |
| `/templates` | Object-use/provenance manifest and lesson/project templates |
| `/reports` | Study reports, validation reports, package evaluations |
| `/corvette` | Corvette-specific branch rules and constraints |
| `/visual_library` and `/visual_references` | Selective visual anchors and lessons |
| `/archive` | Legacy/superseded/changelog/history files |

## Current capabilities & governance

**Routing & intake**
- Mandatory request router: classify the request, apply the correct rule bundle, check JSON/FBX/rules, run gates, and CAPA-stop on a breach (`rules/REQUEST_ROUTER_CHECKLIST.md`, `rules/REQUEST_ROUTER_CHECKLIST.json`, `validation/request_router_check.py`). Major generated scripts embed `REQUEST_CLASSIFICATION` (`validation/run_gate.py --require-router`).
- Build-vs-image routing guard: an NMS-context "create/build …" prompt produces or clarifies NMS Builder Python work, never a silent image.
- Prompt routing / rule-application gate: prompt classification and actual rule application precede source-doc updates, JSON studies, screenshot intake, or build generation; protocol-sensitive responses carry a visible `Protocol confirmation`.

**Placement intelligence**
- A Master Placement Intelligence Index, Method Authority Table, Placement Precedence, and Negative Knowledge Index govern placement-sensitive work. Assembly context supersedes component context — a verified part is not automatically a validated assembly.
- Authoritative snap placement: the add-on's own snap definitions are the authoritative source for snap-group parts, with a validated composition formula (FLIP = 180° about Y); derived adjacency is fallback (`rules/AUTHORITATIVE_SNAP_PLACEMENT_PROTOCOL.md`).
- `C_TRIFLOOR` is the validated advanced triangular-surface part (placement map with origin type, default orientation, phase rule, scale behavior, and family equivalence).
- A part-orientation overrides registry holds part-specific exceptions (e.g., `BILLBOARD rx=0`).

**JSON evidence**
- Working JSON first: when relevant working JSON exists, mine it as the first placement/recipe source, preserving the connection logic behind stairs, ramps, domes, curved shells, and local-frame assemblies — not just literal placement.
- A JSON evidence mapping gate and a parametric JSON recipe protocol apply; JSON-derived feature work includes a visible `Protocol confirmation`.
- JSON geometry validation loop: Python intent → plugin scene → exported JSON transform truth → screenshot outcome.

**Build evidence & gates (executable)**
- `validation/run_gate.py` is the build gate; PASS comes from a real run, never a hand-typed block.
- Validated-logic reuse + composite intent graph: build-generation scripts using validated parts include `USED_PART_LOGIC` and `BUILD_INTENT_GRAPH` (`validation/validated_logic_reuse_check.py`).
- Recipe conformance: `validation/recipe_conformance_check.py` verifies exported Position/Up/At against the partmap signature, so a mis-oriented build fails even with a perfect receipt.
- Build-objective conformance: `validation/build_objective_conformance_check.py` catches floating/disconnected pieces in builds meant to be connected.
- AI visual capture compliance: build-generation scripts plan semantic capture areas (`rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md`, `validation/ai_capture_compliance_check.py`, and the review-bundle addon).
- A controlled `validation_status` ladder is gate-enforced: UNKNOWN → UNTESTED → SCRIPT_VALIDATED → {BLENDER_USER_CHECK | BLENDER_SYSTEMATIC} → GAME_VALIDATED (evidence-gated). A drift-checked `parts_status.csv` ships each release.

**Continuity & governance**
- Single current-state source: governance and active-build docs state current requirements only; version history lives in `CHANGELOG.md` (`rules/SINGLE_CURRENT_STATE_SOURCE_RULE.md`, enforced by `validation/version_callout_check.py`).
- Full version continuity review when a newer package arrives (`rules/FULL_VERSION_CONTINUITY_REVIEW_RULE.md`).
- Triage review-assistance governance and project-transfer continuity rules.
- Open Topics Log Protocol and Source-Doc Evaluation Checklist.
- Systematic Failure CAPA: source-knowledge failures trigger a stop / root-cause / corrective-action response and cannot be bypassed by another generated study or script (`rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md`).
- A protocol banner closes every substantive response (numeric `source docs rev` and a `Docs Avail for Update?` count).

## Active high-level rules

- Use real NMS Base Builder parts only.
- Spacing comes from FBX bounds, JSON precedent, or confirmed in-game calibration.
- JSON recipe = baseline/control, not fixed mandate.
- Production shells should be connected angled surfaces, not stepped-offset lookalikes unless requested or experimental.
- Continuous means connected.
- Disconnected assembled subsystems are a hard-stop failure; use `rules/DISCONNECTED_ASSEMBLY_HARDSTOP_RULE.md` for stairs, ramps, spires, roof crowns, vehicles, cave interiors, hatches, and other multi-part assemblies.
- Floating means intentional; unknown terrain may require a designed ground-zero foundation platform.
- Wonder Projectors remain prohibited for generated builds: `HOLO_DISCO`, `HOLO_DISCO_0`.

## Part / family exceptions

- PIPE/BUBPIPE: Blender spawn/bbox/orientation is not authoritative for connected pipe assemblies (PIPE can be invisible/zero-bbox in Blender while valid in game; BUBPIPE can orient differently). Use the verified part map for ordinary component mechanics, but require in-game/exported-JSON validation before using `PIPE`, `BASE_BUBPIPE`, `BASE_BUBPIPE_L`, `BASE_BUBPIPE_S`, `BASE_BUBPIPE_T`, or `BASE_BUBPIPE_X` as connected pipe systems. `rx=90` may correct an individual part's orientation but does not prove connection continuity.
- Airlock/iris: higher side counts preserve the known-good iris center/pivot/radius and increase overlap density, rather than expanding the door into a larger annulus.

## Versioning

Releases use `X.YY.ZZ` (`rules/MASTER_DOC_VERSIONING_POLICY.md`). Per-release history is in `CHANGELOG.md`.
