# Systematic Failure CAPA Protocol

Status: **mandatory** for all build-generation chats.

## Trigger

This protocol activates when any generated script, study board, or recommendation shows a **systematic failure to use known source-kit knowledge**, including:

- using generic placement/orientation assumptions when the source kit contains validated JSON mapping, FBX dimensions, part-family rules, or recipe data;
- repeating a previously documented failure mode;
- producing multiple failed subsystems from the same incorrect assumption stack;
- delivering a script that passes the machine gate but visibly violates known recipes, spacing, orientation, or transform evidence;
- user correction indicates that the answer ignored available source documents, JSON, or validated project lessons.

## Mandatory stop rule

When the trigger occurs, the **very next assistant action** must be a corrective-action response. Do not continue generating new studies, patches, or master scripts until the failure has been addressed.

Required first response:

```text
SYSTEMATIC FAILURE CAPA
Failure type:
Source knowledge ignored:
Root cause:
Containment action:
Corrective action:
Prevention update:
Docs/files updated:
Open verification item:
```

## Root-cause requirements

The root cause must identify **why** known information was not applied. Acceptable categories include:

- wrong context mode selected;
- source docs not loaded or not treated as governing;
- JSON mapping available but not used;
- part-family rule ignored;
- recipe treated as inspiration instead of geometry control;
- generic transform/orientation fallback used where a validated basis existed;
- validation gate lacked the correct context flag;
- too many subsystem changes hid the shared root failure.

Do not answer only with an apology. Do not blame uncertainty if the needed information was present in source files or user-provided JSON.

## Containment action

Containment must identify what output is now rejected or quarantined:

- rejected script filename/version;
- affected subsystem(s);
- instructions not to promote that output as a baseline;
- whether generated artifacts should be deleted, ignored, or kept only as negative examples.

## Corrective action

Corrective action must be specific and mechanical:

- the exact source doc/rule/JSON recipe to use next;
- the transform stack or spacing formula to apply;
- any required small control test before reintegration;
- the validator/gate flag that must be used;
- the docs updated so other chats cannot miss the rule.

## Prevention update

Every systematic failure must create or update at least one durable source item:

- `rules/ISSUE_FIX_LIBRARY.md` for the specific failure mode;
- a rule/protocol file if the failure is workflow-level;
- a toolkit/recipe entry if the correction is reusable;
- transfer/bootstrap prompts if other chats need the rule immediately;
- validation tooling when the failure can be machine-checked.

If no source update is made, the CAPA response must explicitly say why the lesson is not durable.

## Verification before continuing

After CAPA, future generation must verify:

- active source version and relevant gating docs;
- exact ObjectIDs and part families involved;
- whether JSON mapping is mandatory;
- whether a known recipe exists;
- whether the script uses the required validation mode.

Only then may new code be generated.

## hard-stop enforcement

The CAPA protocol is not advisory. When a systematic failure is identified, the next response must not deliver another build script, study board, or geometry patch until the following have been completed and explicitly reported:

1. the failed artifact/version is quarantined;
2. the source knowledge that should have governed the work is named;
3. the master source package is updated or a specific durable source patch is produced;
4. any machine-checkable failure mode is added to `validation/run_gate.py` or a named validator;
5. the release gate for the patched package passes;
6. any prior incorrect rule introduced by the assistant is corrected or superseded.

If the assistant recognizes a systematic failure but continues directly to another script, that response is itself a second systematic failure and this protocol must restart.

## Mandatory evidence before resuming code

After CAPA, the first generated code artifact must include a compact evidence block showing:

- active master-doc version;
- relevant rules read;
- exact JSON/control file used;
- exact ObjectID counts expected from the control recipe;
- whether the script uses direct `BUILDER.add_part()` placement or template-copy placement;
- how NMS Builder `Part` wrappers are resolved to Blender objects.

No script may be described as validated unless `validation/run_gate.py` reports nonzero placed parts, no execution error, and `MACHINE-CHECKABLE GATE: PASS`.
## enforcement addendum — protocol breach is a hard stop

A protocol failure is not resolved by an apology or by adding another standalone rule. The assistant must run this corrective workflow immediately when the user catches a missed rule, when the assistant self-detects skipped governance, or when an interpretation/memory/source promotion was overbroad.

Required sequence:

1. **Stop normal execution.** Do not continue generating scripts or design recommendations while the protocol breach is unresolved.
2. **Identify failed protocol.** Name the specific intake, JSON, validation, source-review, or example-handling rule that was skipped.
3. **Rollback overbroad interpretation.** Correct memory/source meaning if a reference, image, JSON, or lesson was promoted too broadly.
4. **Correct classification.** Reclassify the user input under `REQUEST_ROUTER_CHECKLIST`.
5. **Define prevention.** Say which router bundle/gate/checklist must have fired.
6. **Patch decision.** Decide whether docs, memory, tooling, or release gates need a patch. If the issue can recur across chats, patch the master docs/gates rather than relying on local memory.
7. **Resume only after containment.** Continue the original task only after the failure is contained.

This applies to all protocols, not just image intake.

## Source-skipping escalation (deeper manifest as a CAPA consequence)

The lean build-sheet gate (`validation/build_sheet_check.py` via `run_gate`) verifies COVERAGE, POPULATED, and INTEGRITY of the generated builder sheet, but it TRUSTS the AI's `BUILD_SHEET_USED` attestation. When a CAPA's root cause is **skipping known existing information in source docs or the build sheet** — the sheet/JSON/recipe/part-family data was available but not actually utilized, or a design failed because the provided sheet was ignored (trigger class `BUILD_SHEET_FABRICATION / SHEET_NOT_UTILIZED`) — the corrective action MUST escalate:

1. Open the escalation: `python3 validation/capa_escalation.py --open --reason "<root cause>"`.
2. While ACTIVE, `run_gate` ALSO requires a passing deeper `compliance_manifest_check` (per-part precedence resolution verified against sources) on top of the lean sheet. The build must declare `PROJECT_COMPLIANCE_MANIFEST="<path>"` and emit the manifest.
3. Clear only after a corrective build passes the deeper requirement AND a prevention update is logged: `python3 validation/capa_escalation.py --clear --note "<corrective build> passed; prevention logged"`.

Scope: project-wide probation until cleared (the breach is one of trust, not a single part). This is how the optional deeper tool becomes a required consequence. It is NOT invoked for CAPAs whose root cause is unrelated to skipping available information.


## Execution receipt: traceable protocol verification (absorbed from TRACEABLE_PROTOCOL_VERIFICATION_RULE)
## Status

**Mandatory for protocol-sensitive NMS Builder work.** This rule hardens the protocol banner by requiring a machine-readable or human-readable execution receipt. The banner alone is not enough evidence that the mapped rules were actually used.

## Purpose

Prior failures showed that the assistant can acknowledge a rule, claim it understands the user objective, and then silently substitute a generic geometry or optimization assumption. This rule prevents soft overrides by requiring explicit objective locks, forbidden substitutions, mapped-document evidence, and postflight verification.

## Required preflight block

Before build generation, JSON-derived variant work, control-to-variant work, rule discovery, style transfer, or source-doc patching, produce or internally maintain a request trace with these fields:

```text
REQUEST TRACE
User asked for:
Request type:
Mapped docs/rules loaded:
Source/control used:
Locked objectives:
Forbidden substitutions:
Invariants to extract:
Allowed variation slots:
Planned proof:
Validation gate planned:
```

If the user has already supplied any of these fields, do not ask again. Carry them forward.

## Required postflight receipt

After generation or source-doc work, provide a compliance receipt or embed it in the script/report:

```text
PROTOCOL VERIFICATION RECEIPT
Mapped docs/rules used: yes/no + evidence
Locked objectives preserved: yes/no + evidence
Forbidden substitutions avoided: yes/no + evidence
Source/control-derived rule used: yes/no + evidence
New application/proof produced: yes/no + evidence
run_gate or equivalent validation: PASS/FAIL/self-reported/blocked
Known unverified items:
```

## PASS rule

A response may not claim `PASS` unless the receipt includes evidence. For build scripts, `PASS` still requires the executable gate. For non-script protocol work, use `self-reported` and state what was checked.

## Hard stop

If any locked objective is missing, contradicted, or soft-overridden, stop normal generation and run `SYSTEMATIC_FAILURE_CAPA_PROTOCOL`.

## Applies to

```text
CONTROL_TO_VARIANT_DERIVATION
RULE_DISCOVERY_AND_PROOF
PART_BEHAVIOR_LEARNING
JSON_GEOMETRY_INTELLIGENCE_EXTRACTION
JSON_FEATURE_RECIPE_EXTRACTION
PYTHON_BUILD_GENERATION using a working JSON/control
PYTHON_BUILD_REFINEMENT after user correction
SOURCE_DOC_UPDATE involving protocol behavior
```


---

## Postflight Banner Fields

The protocol verification receipt must now support the current banner fields:

```text
Source docs revision used:
Docs update items pending:
Docs Avail for Update?:
```

Rules:

```text
source docs revision used = numeric semantic version only
Docs update items pending = list or count of pending source-doc update items
Docs Avail for Update? = Yes (N) if pending list is non-empty, otherwise No (0)
```

The final protocol banner must match the receipt. A response may not say `Docs Avail for Update?: No (0)` if the receipt lists pending source-doc updates.

## source-doc and banner hardening

For source-doc review, source-doc update, or protocol-correction work, the request trace must also confirm:

```text
- release/VERSION.json was checked for the active numeric source docs revision
- 00_START_HERE_CURRENT.md was checked before answering
- rules/SOURCE_DOC_EVALUATION_CHECKLIST.md was applied
- rules/DOCS_UPDATE_AVAILABILITY_PROTOCOL.md was applied
- rules/PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md was applied
- the final banner uses source docs rev + Docs Avail format, not obsolete bundle format
```

For validation reports, the postflight receipt must state gate scope:

```text
gate_scope:
  full_regression | partial_matrix | stadium_only | switchback_only | generated_file_only | source_doc_release
```

A partial `PASS` must not be promoted as a full family PASS.

For source-doc releases, the postflight receipt must include:

```text
version_updated:
changelog_updated:
release_notes_added:
file_inventory_updated:
package_manifest_updated:
open_topics_log_added:
release_check_result:
```


## Validated-logic reuse proof (absorbed from VALIDATED_LOGIC_REUSE_PROTOCOL)
## Status

**Mandatory for build generation using any part with a validated or user-reviewed placement status.**

This rule exists because the project discovered a serious failure mode: a chat can read the
source package, list the right protocol bundle, and still generate a build that does not
actually use the validated partmap logic.

## Failure that caused this rule

A composite build using only a few known parts exposed three distinct failures:

```text
- C_TRIFLOOR had validated pyramid / advanced-shape knowledge, but the generated script
  reimplemented a new ad-hoc triangle subdivision instead of reusing the validated lattice
  and phase recipe.
- S_RAMP had validated stair local-frame Up/At repeat behavior, but another cold-chat
  implementation ignored the local frame and tipped the stair rise into the wrong world axis.
- The final protocol banner claimed rule compliance even though no executable receipt proved
  the validated recipe was loaded or used.
```

The project conclusion is:

```text
Recorded != required != used.
```

A protocol banner is not evidence unless the generated artifact carries a machine-checkable
receipt proving the relevant partmap and validated recipe were applied.

## Required generated-script manifest

Every substantive NMS Builder generated script must include:

```python
USED_PART_LOGIC = {
    "S_RAMP": {
        "partmap_path": "library/part_placement_maps/S_RAMP.partmap.json",
        "validated_algorithm": "STAIR_LOCAL_FRAME_REPEAT_AND_EDGE_START",
        "reuse_mode": "DIRECT_REUSE",
        "source_transform_invariants": ["Position", "Up", "At"],
        "recipe_source": "toolkit/validated_recipes/stairs.py"
    },
    "C_TRIFLOOR": {
        "partmap_path": "library/part_placement_maps/C_TRIFLOOR.partmap.json",
        "validated_algorithm": "C_TRIFLOOR_PHASE_RESOLVED_GEOMETRIC_SUBDIVISION_V23",
        "reuse_mode": "DIRECT_REUSE",
        "source_transform_invariants": ["Position", "Up", "At"],
        "recipe_source": "toolkit/validated_recipes/c_trifloor.py"
    },
    "S_DOOR": {
        "partmap_path": "library/part_placement_maps/part_placement_master_sheet.csv",
        "validated_algorithm": None,
        "reuse_mode": "PROVISIONAL_BLOCK_OR_REVIEW",
        "reason": "door-on-sloped-triangle-face not validated"
    }
}
```

## Allowed reuse modes

```text
DIRECT_REUSE
    The generated script imports or directly calls the validated recipe function.

IMPORTED_RECIPE
    Same as DIRECT_REUSE, but the script uses an exported helper/module instead of inline code.

ADAPTED_VERIFIED
    The script adapts a validated recipe for a declared variant and provides explicit
    parameter differences. This is allowed only when the variant slots are declared.

EXPERIMENTAL_VARIANT
    The script intentionally deviates from validated logic. It must not claim validated
    placement behavior and must be visually reviewed.

PROVISIONAL_BLOCK_OR_REVIEW
    The part or fitment mode is not validated. Use is allowed only when clearly marked
    provisional and when the open-topics log records the validation gap.
```

## Hard requirements for validated parts

If a part's `validation_status` is:

```text
SCRIPT_VALIDATED
BLENDER_USER_CHECK
BLENDER_SYSTEMATIC
GAME_VALIDATED
```

then a generated build must:

```text
1. Load/reference that part's partmap.
2. Name the validated algorithm.
3. Preserve source transform invariants: Position, Up, and At.
4. Use a validated recipe module/function where one exists.
5. Declare any adaptation as ADAPTED_VERIFIED or EXPERIMENTAL_VARIANT.
```

Ad-hoc reimplementation is not allowed by default.

## Hard requirements for unvalidated parts

If a part is `UNTESTED` or has no partmap, it may still be used, but the script must declare:

```text
reuse_mode = PROVISIONAL_BLOCK_OR_REVIEW
reason = why this use is not validated
```

The final response must not imply that unvalidated fitment worked merely because the script
compiled or placed the object.

## Executable gate

The validator is:

```text
validation/validated_logic_reuse_check.py
```

It can be run directly:

```bash
python -S validation/validated_logic_reuse_check.py path/to/generated_build.py
```

`run_gate.py` also exposes this as an opt-in hard gate:

```bash
python -S validation/run_gate.py path/to/generated_build.py library/nms_part_dimensions_and_rules_updated.json TAG --require-validated-reuse
```

## Protocol banner implication

For generated builds using validated parts, the gate field should not say only:

```text
self-reported
```

It should cite the executable receipt, for example:

```text
gate: compile PASS; validated_logic_reuse PASS; run_gate PASS
```

or:

```text
gate: BLOCKED — validated C_TRIFLOOR recipe not reused
```

## mandatory conformance pairing

`USED_PART_LOGIC` proves that the generated script claims to reuse the validated recipe. It is necessary but insufficient.

If an executable recipe conformance checker exists for a validated part/family, it must also run against exported NMS JSON before the build can claim validated placement compliance.

Current executable conformance coverage:

```text
normal full-ramp stair local-frame repeat:
Position[n+1] = Position[n] + At*RUN_STEP + Up*RISE_STEP
```

Future conformance modules should be added for C_TRIFLOOR phase/lattice tiling, door-fitment, and other validated recipes as they become executable.


## geometry-use clarification

A validated partmap proves part behavior only within the validated scope. It does not automatically validate a new freeform shape.

For complex focal builds, a generated script must prove both:

```text
1. validated part behavior was reused
2. the generated geometry used that behavior through a declared curve/edge/surface graph
```

For `C_TRIFLOOR`, this means freeform structures must not be generated by independent centroid/spacing scatter. The script must declare `GEOMETRY_CONSTRUCTION_PLAN` and either `SURFACE_MESH_CONTRACT`, `C_TRIFLOOR_EDGE_GRAPH`, or `CURVE_FOLLOW_CONTRACT`.


## Protocol receipt evidence (absorbed from PROTOCOL_RECEIPT_EVIDENCE_RULE)
## Status

Mandatory for generated scripts, validation reports, and source-doc updates.

## Rule

A protocol banner is not a promise. It is a receipt.

The banner may claim a gate only when the corresponding check actually ran or when the
response clearly says the gate was self-reported / not run / blocked.

## Build-generation implications

For build generation, a valid receipt should include, where applicable:

```text
- python compile PASS
- run_gate PASS/FAIL/NOT_RUN
- validated_logic_reuse_check PASS/FAIL/NOT_RUN
- composite intent graph PASS/FAIL/NOT_RUN
- Blender runtime PASS/FAIL/NOT_RUN
```

Do not use generic `self-reported` when an executable check exists and was required but not run.

## Common incorrect banners

```text
gate: PASS
```

is invalid unless the required gate actually passed.

```text
gate: self-reported
```

is insufficient for generated builds that use validated parts, unless the response also says
the executable gates were not run and therefore no placement-compliance claim is made.

## Correct examples

```text
gate: compile PASS; validated_logic_reuse PASS; Blender runtime NOT_RUN
```

```text
gate: BLOCKED — C_TRIFLOOR validated recipe not reused
```

```text
gate: run_gate FAIL; temporary stair semantic continuation allowed; raw failure preserved
```


## bundle receipt and conformance receipts

The final protocol banner must include a visible `bundle:` field. The `bundle:` field is the compact receipt that the request router selected and applied the correct rule bundle. It does not replace executable checks.

For generated builds that use validated or user-reviewed parts, the receipt must distinguish:

```text
validated_logic_reuse_check  -> receipt/manifest conformance
recipe_conformance_check     -> exported Position/Up/At obeys validated recipe
intent_graph_conformance     -> exported connected-component count matches BUILD_INTENT_GRAPH
```

A build may not claim validated placement compliance unless all required executable receipts ran and passed.

Correct example:

```text
PROTOCOL ✓ — type: build_generation | source docs rev: <rev> | bundle: build_generation + partmap_reuse + recipe_conformance + intent_graph | gate: compile PASS; run_gate PASS; validated_logic_reuse PASS; recipe_conformance PASS; intent_graph PASS | ambiguity: none | Docs Avail for Update?: No (0)
```

Incorrect example:

```text
PROTOCOL ✓ — type: build_generation | source docs rev: <rev> | bundle: build_generation | gate: PASS | ambiguity: none | Docs Avail for Update?: No (0)
```

because it does not identify which executable receipts passed.
