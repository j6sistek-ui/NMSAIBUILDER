# 00 — KICKOFF / INTAKE GATE (5.18.00) — REQUEST ROUTER + FEATURE RECIPE ROUTER FIRST — REQUEST ROUTER + EXECUTION KERNEL FIRST — REQUEST ROUTER FIRST, EVERY TIME

## MANDATORY FIRST DUTIES (do these before Step 0)

1. Emit the `ONBOARDING CHECKLIST` (READ/SKIPPED for every package doc) — `rules/SESSION_ONBOARDING_CHECKLIST_RULE.md`.
2. On a new chat, complete the `ONBOARDING_VALIDATION_BUILD` before the first user build — a real, intentionally minimal floor/wall/roof + one ramp (a placement-map proof-ledger part) micro-build run through the full process (real `run_gate`, gate-verified `BUILD COMPLIANCE MANIFEST`), per `ONBOARDING_VALIDATION_BUILD.md`. Treat it exactly like a user build.
3. For every placement, run `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md` (Placement Intent -> Precedence Resolution -> Method Selection). This is THE LAW, not a reference.
4. Every build (Python OR live Blender — `rules/BLENDER_PARITY_RULE.md`) emits a `BUILD COMPLIANCE MANIFEST` and must PASS `validation/compliance_manifest_check.py`. No verified manifest = invalid build.


## placement-intelligence intake requirement

For every generated build, route placement through `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md` after request classification. High-risk assemblies must use `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md`. Generated build outputs should include `PLACEMENT_SESSION_RECEIPT`, `BUILD_PLACEMENT_SNAPSHOT`, `PLACEMENT_METHOD_SUMMARY`, `ASSEMBLY_CONFORMANCE_PLAN`, and `PART_USAGE_MANIFEST` evidence artifacts.

Do not accept component verification as assembly validation. If a part is used as a stair/ramp, bridge, wall shell, spire, dome, pipe, billboard, or C_TRIFLOOR structure, check the method authority table and assembly context before part-map component data.

## PIPE/BUBPIPE intake exception

If a build request uses pipes, bubble ducts, fluid ducts, or connected pipe assemblies, route through `rules/PROHIBITED_AND_PLACEHOLDER_OBJECTS.md`. Do not treat Blender-visible BUBPIPE orientation or zero-bbox PIPE extraction as sufficient evidence. Require in-game screenshot/exported JSON validation for pipe-system continuity unless the request explicitly accepts experimental/provisional pipe behavior.



## AI capture compliance intake

For generated Blender/NMS build scripts, include an `AI_CAPTURE_COMPLIANCE` manifest unless the request is not a build script. For buildings, rooms, interiors, cities, or scene-scale builds, explicitly plan semantic capture areas before coding: exterior/focal, structural shell, access/interior, interior detail, decor/review-required, and scene/context as applicable.

If the user uploads an AI review bundle, route to review-bundle validation first. The visual bundle does not replace exported JSON or `run_gate`.

## Step 0 — Request-router classification (mandatory)

Before Step 1, classify the request using `rules/REQUEST_ROUTER_CHECKLIST.md/json`. If the type is unclear or several apply, STOP and ask the user — do not guess. A new type is added via the documented `adding_new_request_type` process. End every response with the protocol confirmation banner (`rules/PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md`).

If the user input is ambiguous, ask a clarifying question before applying, storing, or promoting an interpretation. This is especially required for reference images/examples.

After request-router classification, apply `rules/NMS_BUILDER_EXECUTION_KERNEL.md` for substantive NMS work. If the prompt asks for a known-feature variant, also apply `rules/RECIPE_PARAMETERIZATION_PROTOCOL.md`, `rules/PROMPT_TO_FEATURE_ROUTER.md`, and `data/JSON_RECIPE_SIGNATURE_INDEX.json`.

If JSON is provided or known to exist, exact recreation is only the first layer. Also extract part roles, connection relationships, invariants, allowed parameters, and missing evidence under `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`.

If the user reports that a protocol was not followed, immediately route to `protocol_correction_or_failure` and run `SYSTEMATIC_FAILURE_CAPA_PROTOCOL` before continuing.
This gate runs **before any design or code**, on the first build-related message
of every session and again whenever the build mode changes. Its job is to make
the AI *proactively gather the inputs that make builds succeed* instead of
guessing. You (the AI) do not start building until you have emitted the INTAKE
BLOCK below and either (a) received the required inputs, or (b) explicitly listed
the assumptions you are proceeding on.

> Hard rule: if you find yourself writing build code and you have not emitted an
> INTAKE BLOCK this session, STOP and emit it first. Silence is not consent to
> proceed on missing data — name the gap.

## Step 1 — Classify the mode (pick one)

| Mode | Trigger | The 3 gating docs |
|---|---|---|
| NEW_BUILD | "build me a / design a …" | `rules/NMS_BUILDER_EXECUTION_KERNEL.md`, `02_GENERATOR_CONTRACT.md`, `rules/SCRIPT_VALIDATION_LOOP.md`, `toolkit/PLACEMENT_RECIPE_LIBRARY.md` |
| JSON_RECREATION | user has/exports a base JSON | `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`, `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`, `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md`, `rules/JSON_EVIDENCE_MAPPING_GATE.md` |
| VALIDATION_ITERATION | user posts screenshots or exported JSON of the current build | `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md`, `rules/JSON_GEOMETRY_VALIDATION_LOOP.md`, `rules/JSON_EVIDENCE_MAPPING_GATE.md` |
| REFERENCE_INTAKE | user posts external/in-game inspiration | `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md`, `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md` |
| EXPERIMENTAL | vague/creative/"surprise me" | `rules/EXPERIMENTAL_REQUEST_PROTOCOL.md` |
| CORVETTE | ship/Corvette intent | `corvette/CORVETTE_KNOWLEDGE_REPOSITORY.md` (+ checklist) |

You read the **3 gating docs for the active mode** — not all 40. Mode-specific
reading is the antidote to the 167-file overload.

## Step 2 — Request the inputs that mode needs (proactive)

Ask for what's missing. Do not proceed on a guess where the user can hand you
ground truth. Per mode, the inputs that change success/failure:

- **JSON_RECREATION**: the exported base **JSON file** (geometry truth). Without
  it you are guessing coordinates — ask for it before writing any transform. When JSON is provided, `rules/JSON_EVIDENCE_MAPPING_GATE.md` is mandatory and the validated transform constants must be declared before code.
- **VALIDATION_ITERATION**: screenshots **tagged with metadata** — for each
  image: *which build/version*, *camera angle/which face*, *what looks wrong*,
  and *is this the current generated branch or a user-edited branch* (decides
  validation-vs-reference per the taxonomy). Ask for any missing tag.
- **NEW_BUILD / landmark**: reference image(s); the **canonical view** to
  optimize for; **part budget**; **material/colour intent** (and the real
  `UserData` values if known); any **protected subsystems**.
- **REFERENCE_INTAKE**: what the user wants *learned* from the image vs merely
  admired; whether to promote it to toolkit/rule.

## Step 3 — Emit the INTAKE BLOCK (required output)

```text
INTAKE BLOCK  (v57)
Mode: <one of the modes above>
Objective (1 line): <what we are building/changing>
Gating docs loaded for this mode: <3 filenames>
Inputs provided: <list, e.g. "exported JSON (1,237 objs)", "3 screenshots tagged">
Inputs MISSING / requested: <list, or NONE>
Proceeding on assumptions: <explicit list, or NONE — only if user said go ahead>
Part budget: <range or "ask">
Material intent: <value/placeholder + note carry-over guard>
```

If "Inputs MISSING" is non-empty and the missing item is something only the user
can supply (a JSON export, a specific camera angle, the real material value),
**ask for it and stop** — unless the user has said to proceed, in which case the
assumption goes in "Proceeding on assumptions" so it's on the record.

## New data intake (user-provided recipes / part characteristics)

If the user provides new recipe or part-characteristic/creative data, route it into the existing store of record and runtime-link it per `rules/RULE_UPDATE_PROTOCOL.md` (New data intake routing). Do NOT create a new file, report, or index; new files require user approval and are enforced by `validation/new_file_guard_check.py`.

## Why this gate exists

Builds fail when the AI starts from a guess while the data that would have made
it correct was one question away. The cost of asking is one short turn; the cost
of not asking is a wrong build the user has to catch in a screenshot. Ask first.


## v1.03.00 hard stop: systematic failure CAPA

If the user shows that the response ignored source documents, JSON mapping, validated recipes, or known part-family rules, stop. The next response must follow `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md` before any additional code or studies are generated.


## WORKING_JSON_FIRST_CHECK

Before producing code, explicitly check whether the user/source package includes relevant working JSON or JSON-derived recipes. If yes, classify the work as JSON_RECREATION, SOURCE_JSON_RECIPE_MINING, or GENERATED_BUILD_JSON_VALIDATION and load `rules/WORKING_JSON_FIRST_PRINCIPLE.md` plus `rules/JSON_EVIDENCE_MAPPING_GATE.md`. Do not proceed from generic placement assumptions while relevant JSON evidence exists.

## Mandatory prompt classification
Before responding to NMS project prompts, classify the prompt and identify applicable rules. Use:

```text
rules/REQUEST_ROUTER_CHECKLIST.md
```

If images are present, apply `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md` before archiving them.


## disconnected assembly check
If the requested work creates or repairs stairs, ramps, ladders, catwalks, bridges, rails, towers, spires, roof crowns, wall bays, trim rings, vehicles, machinery, airlocks, or cave interiors, load `rules/DISCONNECTED_ASSEMBLY_HARDSTOP_RULE.md` before code. The INTAKE BLOCK or protocol confirmation must identify the connection model or say that the work is an exact JSON control recreation.

## Per-build resolution

For placement-sensitive builds, review the creative knowledge base for relevant part effects, then run `validation/part_context_resolver.py --ids <ObjectIDs> --intent "<request>"` to assemble the forced placement context and offered creative findings before generating. See 00_START_HERE_CURRENT.md → Per-build resolution.

## Discovery-first: intent -> qualities -> parts

Before selecting ObjectIDs, consult the generated `discover_by_quality` view in `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` (keep it in sync via `validation/discover_by_quality_check.py`). Map the creative intent to qualities/effects (e.g. "futuristic" -> smooth, light-emitting, beam) and let those qualities surface candidate ObjectIDs — then resolve the chosen parts through `part_context_resolver.py`.
