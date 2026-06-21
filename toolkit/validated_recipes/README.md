# Validated Recipes Package — 2.16.00

This directory contains lightweight, importable reference implementations for validated
part-family logic. It exists to prevent cold chats from re-deriving solved placement behavior.

If a generated build uses a validated part family and a helper exists here, the script should
call or mirror this helper and record that in `USED_PART_LOGIC`.

Current helpers:

```text
stairs.py      normal full-ramp local-frame repeat and edge-start helpers
c_trifloor.py  C_TRIFLOOR phase constants and tetra subdivision reference helpers
```
