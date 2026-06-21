# Protocol Banner Hard-Fail Rule

## Status

Mandatory for every substantive NMS response.

## Purpose

The protocol banner is the smallest visible proof that the request was routed, the correct source baseline was used, the validation gate status was honest, and `Docs Avail for Update?` was tracked. It is not optional formatting.

If the banner omits any active field, uses an obsolete bundle-free format, or drops `Docs Avail for Update?`, the response is a protocol failure and must trigger SYSTEMATIC FAILURE CAPA before any further work.

## Required final banner

```text
PROTOCOL ✓ — type: <request_type> | source docs rev: <X.YY.ZZ> | bundle: <router_bundle_or_rule_receipt> | gate: <verdict> | ambiguity: <none|clarification requested> | Docs Avail for Update?: <Yes (N)|No (0)>
```

## Hard-fail conditions

A response is nonconformant if:

```text
- the final banner is missing
- source docs rev is missing
- bundle is missing
- gate is missing or overclaims PASS
- ambiguity is missing
- Docs Avail for Update? is missing
- Docs Avail count contradicts confirmed pending updates
- an obsolete bundle-only or no-bundle banner is used
```

## Required CAPA

If the user catches a missing or incorrect banner, the assistant must:

```text
1. Stop normal work.
2. Acknowledge SYSTEMATIC FAILURE CAPA.
3. Correct the banner and Docs Avail state.
4. Add or confirm a source-doc update if the failure revealed a governance gap.
```

## Executable support

Use:

```text
validation/protocol_banner_check.py
```

to check response/report text artifacts where a machine-checkable protocol receipt is needed.
