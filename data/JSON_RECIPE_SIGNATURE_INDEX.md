# JSON Recipe Signature Index

Status: active compact index.

## Purpose

This index stores lightweight signatures derived from working JSON and JSON studies. It should answer: "Do we have enough retained executable knowledge to reuse this feature without rereading the raw JSON?"

If the answer is no, ask the user for the source JSON again.

## Signature idea

Each signature records:

```text
feature type
control source
ObjectID multiset
geometry basis
locked invariants
allowed parameters
validation requirements
promotion status
missing evidence
```

This is intentionally smaller than raw JSON. Raw JSON remains the audit source when needed.


## provisional signature — gothic metal castle facade

`gothic_metal_castle_facade_template` is a provisional facade/control signature for the first build-execution test prompt. It locks the symmetric front axis, flush entrance wall plane, radial airlock center, ring depth layers, tower/wall contact grid, buttress support contact, and connected entrance wall-to-airlock frame. It must be promoted from generated control JSON or user-provided JSON before being treated as an exact reusable control.
