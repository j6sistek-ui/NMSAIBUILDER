# Release Notes 4.00.00 — Authoritative Snap Placement

Major release. Establishes the add-on's own snap definitions as the authoritative placement source and adds a
validated placement composition formula, replacing derived/heuristic placement for snap-group parts.

- New rule: rules/AUTHORITATIVE_SNAP_PLACEMENT_PROTOCOL.md
- Validated (snap): map matches live snaps to 0.0 gap; formula reproduces full pose to 0.0/0.0 deg incl. cross-group
- Derived-adjacency method demoted to fallback for ~919 parts with no snap group
- Self-contained data bundled under library/authoritative_snap/
- Snap-validated, not yet game-validated; GOLD tier remains in-game confirmation

Cross-chat handling (Major): tell active chats to reload sources before further script generation.
