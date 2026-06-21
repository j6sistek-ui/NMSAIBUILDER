# Release Notes — 5.01.01

**run_gate phase-ordering fix.**

## Problem
The pipeline is: Python script -> run through run_gate -> build runs in NMS -> exports the base JSON. run_gate was forcing the recipe-conformance and intent-graph gates to FAIL whenever the script used those parts but no exported JSON was passed - but the JSON only exists AFTER the build runs. So the pre-build Python failed every time.

## Fix (two-phase gate)
- PRE-BUILD (no JSON): conformance + intent-graph are DEFERRED, not failed. Script-level verdict can PASS at SCRIPT_VALIDATED; the output states JSON validation is pending.
- POST-BUILD (JSON supplied): `--require-conformance <exported.json>` / `--require-intent-graph <exported.json>` run the real checks; they can FAIL. Enforcement unchanged, correct phase.

## Verified
- All run_gate release self-tests still PASS.
- A ramp-using pre-build script now shows `recipe conformance gate: DEFERRED` instead of `FAIL (REQUIRED_NOT_RUN)`.
