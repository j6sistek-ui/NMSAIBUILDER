# Release Notes — 5.04.04

**Date:** 2026-06-20  **Type:** patch (START HERE rewrite + onboarding wiring)  **Supersedes:** 5.04.03

## Changed
- `00_START_HERE_CURRENT.md` rewritten as the current knowledge base: version call-outs removed so a v5 reader no longer treats v4-era notes as equally current; all live requirements restated present-tense and topic-grouped. History stays in CHANGELOG.
- `ONBOARDING_VALIDATION_BUILD.md` is now a real full-process micro-build (removed 'simulated'); it runs the real gate and emits a gate-verified compliance manifest.
- `00_KICKOFF_INTAKE_GATE.md`: the onboarding validation build is now a mandatory first duty (it was previously orphaned from the entry path).

## Gate
`release_check.py` → RELEASE GATE: PASS.
