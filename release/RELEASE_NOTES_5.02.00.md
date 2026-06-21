# Release Notes — 5.02.00

**Build-sheet gate — packet coverage enforced in run_gate.**

## Loop
Resolve sheet -> fill build_application per part -> declare PROJECT_BUILD_SHEET + BUILD_SHEET_USED -> build from sheet -> run_gate.

## run_gate enforces (pre-build)
- COVERAGE: every ObjectID used in the Python has a sheet entry.
- POPULATED: each entry has resolved data + a non-empty build_application.
- INTEGRITY: sheet mechanical fields still match a fresh resolver run (AI can only add the application note).
- DECLARED: PROJECT_BUILD_SHEET + BUILD_SHEET_USED present.

## Why this over a hand-written manifest
The sheet is generated, so mechanical data is authoritative by construction; nothing to fabricate. Leaner and tamper-evident. The manifest + compliance_manifest_check.py remain an optional deeper tool.

## Phase-correct
The sheet is a pre-build artifact, so this is a hard pre-build requirement; JSON conformance/intent-graph stay DEFERRED to post-build (5.01.01).
