# Protocol Confirmation Banner Template — 2.13.01

One line, every substantive NMS response. See `rules/PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md`.

## Current required format

```text
PROTOCOL ✓ — type: <request_type> | source docs rev: <X.YY.ZZ> | bundle: <router_bundle_or_rule_receipt> | gate: <verdict> | ambiguity: <none|clarification requested> | Docs Avail for Update?: <Yes (N)|No (0)>
```

## Rules

- `source docs rev` is numeric only: `2.13.01`, not a package title or revision description.
- `Docs Avail for Update?` means confirmed source-doc update items known to the assistant that have not yet been incorporated.
- Use `No (0)` only when no learned/corrected source-doc information remains to be rolled into the source docs.
- Use `Yes (N)` when confirmed source-doc changes are pending.
- Build/script turns must cite the real executable gate result.
- Source-doc release turns must cite the real `release_check.py` result.
- Non-script turns must not overclaim machine validation.
- Include `bundle:` in every substantive NMS banner.

## Examples

Build/script turn:

```text
PROTOCOL ✓ — type: build_generation | source docs rev: 3.01.01 | bundle: build_generation + protocol_receipt | gate: run_gate PASS | ambiguity: none | Docs Avail for Update?: No (0)
```

Source-doc update after the package has been patched and gated:

```text
PROTOCOL ✓ — type: source_doc_update | source docs rev: 3.01.01 | bundle: source_doc_update + release_gate | gate: release_check PASS | ambiguity: none | Docs Avail for Update?: No (0)
```

Protocol correction identified but not yet patched:

```text
PROTOCOL ✓ — type: protocol_correction_or_failure | source docs rev: 3.01.01 | bundle: CAPA + rule_update_candidate | gate: self-reported | ambiguity: none | Docs Avail for Update?: Yes (1)
```

Ambiguous request:

```text
PROTOCOL ✓ — type: unresolved | source docs rev: 3.01.01 | bundle: clarification_gate | gate: blocked | ambiguity: clarification requested | Docs Avail for Update?: No (0)
```
