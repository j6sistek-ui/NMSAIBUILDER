# Script Validation Loop

This loop is required before delivering any generated NMS Blender Python script.

## Phase 1 — Candidate part selection

- Use the full library for design potential: `library/nms_part_dimensions_and_rules_updated.json/csv`.
- Treat short ObjectID lists as examples only.
- Print the `FULL LIBRARY CHECK` block from `00_START_HERE_CURRENT.md`.

## Phase 2 — Extract script ObjectID set

Before placement validation, identify the exact ObjectIDs used by the script:

```text
SCRIPT OBJECTID SET
- <ObjectID>
- <ObjectID>
```

This set controls scoped validation.

## Phase 3 — Universal validation

Check every script for:

- real NMS Builder plugin usage
- `BUILDER.add_part()` templates
- template duplication
- NMS custom property preservation
- tag-only cleanup
- no raw Blender mesh primitives
- no prohibited generated ObjectIDs
- runtime object audit

## Phase 4 — Scoped part validation

Only for ObjectIDs/families used in the script, check:

- FBX extents and centers
- origin/bottom/top placement formulas
- orientation conventions
- chord spacing / ring formulas
- known issue/fix entries
- part-family rules
- project constraints if editing an existing project

Do **not** review placement rules for parts not used in the current script. Broad library review remains valid for design selection.

## Phase 5 — Rewrite or ask approval

If any check fails, rewrite the script before presenting it.

If a rule needs to be violated because it is bad, outdated, or conflicts with design intent, ask for approval before presenting code.

## Phase 6 — Delivery block

Every delivered script should include this self-check:

```text
SCRIPT VALIDATION LOOP CHECK
Uses full library, not whitelist: PASS
ObjectID set extracted from script: PASS
Universal generator contract: PASS
Part-specific validation limited to used ObjectIDs/families: PASS
Applicable part-family rules checked: PASS
Known issue/fix checks applied: PASS
Protected subsystem/project constraints checked where relevant: PASS
No prohibited ObjectIDs: PASS
No raw Blender mesh primitives: PASS
Runtime NMS object audit included: PASS
Deviation approval needed: NO
```

## Phase 7 — Immediate documentation update

If the script confirms or correctly applies a new part-specific behavior, offset correction, orientation fix, design rule, or spacing formula, update the master docs immediately:

- part-specific/family behavior -> `PART_FAMILY_RULES.md/json`
- universal workflow -> `UNIVERSAL_RULES.md/json`
- issue/fix -> `ISSUE_FIX_LIBRARY.md`
- creative use -> `PART_USE_CASE_CATALOG.md/json`
- prohibited/placeholder object -> `PROHIBITED_AND_PLACEHOLDER_OBJECTS.md/json`

## v43 mode-specific repository check

Before Phase 3, check whether the prompt activates a mode-specific repository.

Current mode-specific repository:

- Corvette work -> `corvette/CORVETTE_KNOWLEDGE_REPOSITORY.md/json`

If the script targets a Corvette, claims to generate a valid Corvette, or assigns Corvette functional roles, the validation loop must also verify:

- seven required categories are covered when building a valid Corvette;
- a Corvette-specific plugin/add_part probe was run or included;
- no proxy geometry fallback exists;
- ObjectID is included in Blender object names/descriptions;
- Corvette rules are not exported into non-Corvette builds.

If the script merely uses one or more Corvette ObjectIDs decoratively or architecturally in a non-Corvette build, do **not** activate the seven-category Corvette failure mode. Instead:

- validate those ObjectIDs using universal/full-library FBX and placement rules;
- record the use as `decorative_non_corvette`, `architectural_kitbash`, `greeble`, `display`, `lighting`, or similar in the Object Use Manifest;
- skip Corvette completeness/loadout checks;
- ensure the script is not presented as a valid Corvette.


## v45 non-uniform scale validation

Before delivering a generated script, scan the code for non-uniform scale assignments or call arguments.

If any generated final-build part uses `sx`, `sy`, and `sz` with different values, or `obj.scale = (a, b, c)` with different values:

1. determine whether this is an approved/validated exception,
2. if not, rewrite the script using repeated uniformly-scaled real segments,
3. if a design reason exists, request user approval before delivery.

## v50 plugin asset availability validation

When a script uses parts added/exposed in Base Builder 6.4.1, explicitly preflight them with `BUILDER.add_part(ObjectID)` before scene cleanup. If any template fails, stop without deleting existing scene objects.

Newly added/exposed objects include Swarm flags/posters/decals, Titan fireworks, `SET_*` settlement/setpiece objects, and `HOLO_DISCO_0`. `HOLO_DISCO_0` is prohibited for generation.

## v52 screenshot validation distinction

Screenshots from the active generated script/build branch are validation evidence, not general reference intake.

Use them to compare intended script behavior against actual Blender/in-game behavior:
- pass/fail;
- gaps;
- flipped parts;
- bad offsets;
- lighting failures;
- confirmed fixes;
- validated reusable methods.

External/non-current-project screenshots should be handled by the visual reference intake protocol instead.

---

# v57 — EXECUTABLE GATE (supersedes the self-attested delivery block)

The phases above still define *what* to check. v57 changes *how the result is
proven*: the four machine-checkable claims may no longer be asserted in prose.
Run the bundled harness and paste its real output. A hand-typed `PASS` for a tool
that did not run does not count (a script with raw mesh primitives once shipped
with an all-PASS block — see `failure_examples/`).

## One command

```
python3 validation/run_gate.py <generated_script.py> \
        library/nms_part_dimensions_and_rules_updated.json [TAG_PREFIX]
```

It mocks `bpy` + the Base Builder runtime, execs the script, and prints:
- static linter (no raw primitives / add_part templates / template duplication /
  tag-scoped cleanup / no non-uniform final scale),
- dry-run audit (placed parts, missing ObjectID, origin z span, exec error),
- library set-difference (any ObjectID not in the 2,097-row library),
- a single `MACHINE-CHECKABLE GATE: PASS/FAIL` verdict.

## Required delivery block (v57)

Paste the harness output, then the manifest-backed attestations:

```text
SCRIPT VALIDATION — EXECUTABLE GATE (v57)
<pasted run_gate.py output, including MACHINE-CHECKABLE GATE: PASS>
--- attestations backed by the provenance manifest ---
Every subsystem has a provenance citation: YES/NO
Part-family rules applied for used IDs: YES/NO
Protected subsystems respected: YES/NO/NA
Recipes treated as parameterizable baselines, not copied blindly: YES/NA
Deviation approval needed: NO/<what>
```

If `MACHINE-CHECKABLE GATE` is FAIL, fix and re-run before presenting. If you
cannot execute the harness in your environment, say so explicitly and paste the
dry-run you can run — never substitute a typed PASS for a tool that did not run.



## JSON evidence gate

Before Phase 3, ask whether JSON was provided or referenced in the current task. This includes pasted JSON, exported base JSON, JSON study files, JSON-derived recipes, or a user correction based on JSON mapping.

If yes:

- load `rules/JSON_EVIDENCE_MAPPING_GATE.md`;
- require the validated transform constants in the script;
- require a `JSON_EVIDENCE_PROVENANCE` block;
- use JSON-derived ObjectID, Position, Up, At, scale, and spacing before generic orientation tables;
- run `validation/run_gate.py` with `--require-json-evidence`.

If a script fails because this information was skipped, activate `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md` before any rewrite.

## part-family validation note

When a script is part of a family validation study, include the family-validation classification plan:

```text
SAME_RULE
SAME_RULE_WITH_SCALE_COEFFICIENT
SAME_RULE_WITH_PHASE_OFFSET
SAME_RULE_WITH_PIVOT_OFFSET
MODIFIED_RULE
UNIQUE_OUTLIER
FAIL
```

If the script confirms a rule but user/in-game acceptance is still pending, do not claim `USER_ACCEPTED`. Use the validation ladder from `MASTER_LESSONS_LEARNED.md` (removed historical reference: rules/PART_VALIDATION_STATUS_LADDER.md).
