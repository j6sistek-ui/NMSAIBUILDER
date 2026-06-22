# Per-Response Protocol Confirmation Rule — 2.18.01

## Status

**Mandatory.** Every substantive NMS response must end with a single-line protocol confirmation banner.

The final banner carries a visible `bundle:` routing receipt as a check-and-balance: `REQUEST_ROUTER_CHECKLIST` requires selecting and applying the smallest sufficient bundle, and the banner records which one.

## Current required banner format

```text
PROTOCOL ✓ — type: <request_type> | source docs rev: <X.YY.ZZ> | bundle: <router_bundle_or_rule_receipt> | gate: <verdict> | ambiguity: <none|clarification requested> | Docs Avail for Update?: <Yes (N)|No (0)>
```

## Field rules

### type

Use the request type selected by `rules/REQUEST_ROUTER_CHECKLIST.md`.

Common values:

```text
build_generation
screenshot_or_ingame_evaluation
part_behavior_learning
source_doc_review_or_patch
source_doc_update
protocol_correction_or_failure
script_debugging_or_error_log
unresolved
```

### source docs rev

Use the numeric version from `release/VERSION.json`. Do not include package titles or release names.

### bundle

Use the route/bundle actually applied for the request. This is not a decoration: it is the visible receipt that the request router was used.

Acceptable compact forms include:

```text
bundle: request_router + validated_logic_reuse + recipe_conformance + intent_graph
bundle: source_doc_review + release_gate + protocol_receipt
bundle: screenshot_eval + part_behavior_learning + docs_avail
```

For complex work, include a short `Protocol Routing Receipt` block in the body and use a compact bundle summary in the final banner.

The body receipt should list:
- request_type
- router bundle selected
- critical source docs checked
- partmaps/validated recipes used
- executable gates run / not run

### gate

The gate field must not overclaim.

For generated scripts:

```text
gate: compile PASS; run_gate PASS; validated_logic_reuse PASS; recipe_conformance PASS; intent_graph PASS
gate: compile PASS; Blender runtime NOT_RUN; recipe_conformance NOT_RUN
gate: BLOCKED — validated recipe not reused
```

For source-doc releases:

```text
gate: release_check PASS
gate: release_check FAIL
```

For analysis/review turns without a script or release check:

```text
gate: self-reported
```

For blocked or ambiguous work:

```text
gate: blocked
```

### ambiguity

Use:

```text
ambiguity: none
```

or:

```text
ambiguity: clarification requested
```

### Docs Avail for Update?

Use `rules/DOCS_UPDATE_AVAILABILITY_PROTOCOL.md`.

```text
Docs Avail for Update?: No (0)
```

means there are no confirmed source-doc updates pending incorporation.

```text
Docs Avail for Update?: Yes (N)
```

means there are `N` confirmed source-doc updates not yet incorporated.

Open validation work, unknown classifications, pending user review, and future possibilities do not count unless they have become confirmed source-doc changes.

## Honesty rules

- A banner claiming `run_gate PASS` must be backed by a real gate run.
- A banner claiming `release_check PASS` must be backed by a real release-check run.
- A banner claiming `validated_logic_reuse PASS`, `recipe_conformance PASS`, or `intent_graph PASS` must be backed by the corresponding executable check.
- A required gate that was skipped is `BLOCKED`, `FAIL`, or `NOT_RUN`; it is not `self-reported PASS`.
- A partial validation must state scope in the response body. Example: `stadium-only generic AABB PASS` is not a full stair-family PASS.
- A raw gate failure remains `FAIL` even if temporary continuation is allowed.
- A documented proposal is not an adopted rule unless the active source docs say it is adopted.
- A `bundle:` field is not proof by itself; it must correspond to the routing receipt and/or generated script manifests.

## CAPA trigger

If the user identifies a missed route, missing/incorrect banner, skipped validation gate, wrong artifact type, ignored source rule, skipped validated logic, missing bundle receipt, missing USED_PART_LOGIC, missing BUILD_INTENT_GRAPH, or inflated gate result, stop normal work and run `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md` before continuing.

## Version notes

- 2.13.01 replaced the obsolete bundle-only banner with numeric source revision + Docs Avail.
- 2.17.01 restores `bundle:` while preserving numeric source revision and Docs Avail because the router/bundle receipt is a required check-and-balance.


## hard-fail clarification

The final banner is machine-checkable audit evidence. A missing `source docs rev`, `bundle`, `gate`, `ambiguity`, or `Docs Avail for Update?` field is a protocol failure, not a style issue.

Use `validation/protocol_banner_check.py` for report/artifact text when a response receipt is archived. If the user identifies a missing or obsolete banner, run SYSTEMATIC FAILURE CAPA and correct the Docs Avail state before continuing.


## router/precedence receipt is mandatory in the banner

`bundle:` is the visible router receipt and is NOT optional: every substantive
banner must name the route/bundle actually applied. For any placement or build
work the banner must also carry a precedence receipt token so the first duty is
visibly accounted for:

```text
... | bundle: <router route + rules applied> | precedence: <resolved per ObjectID | n/a (no placement)> | gate: <run_gate / compliance_manifest_check verdict> | ...
```

A banner with an empty or missing `bundle:`/`precedence:` for placement work is a
SYSTEMATIC FAILURE CAPA, same as a missing gate verdict.
