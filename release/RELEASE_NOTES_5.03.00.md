# Release Notes — 5.03.00

**CAPA escalation — the deeper manifest as an earned consequence.**

## Policy
The lean build-sheet gate trusts the AI's BUILD_SHEET_USED attestation. When a CAPA's root cause is skipping known existing information in source docs or the build sheet (the sheet/JSON/recipe was available but not utilized, or a design failed because the provided sheet was ignored), the corrective action escalates: the deeper per-part BUILD COMPLIANCE MANIFEST becomes a REQUIRED run_gate gate until a corrective build clears it.

## Mechanism
- `validation/capa_escalation.py --open --reason "..."` sets `data/CAPA_ESCALATION_STATE.json` active (review-logged).
- While active, `run_gate` requires `PROJECT_COMPLIANCE_MANIFEST` to pass `compliance_manifest_check` in addition to the lean sheet.
- `--clear` after a corrective build passes the deeper requirement and a prevention update is logged.

## Defaults
- Scope: project-wide probation until cleared.
- Not triggered for CAPAs unrelated to skipping available information.
- Pre-build (manifest is a pre-build artifact), so it respects the 5.01.01 phase split.

## Also in this package (5.02.00 build-sheet gate)
run_gate enforces the generated builder sheet: coverage, populated build_application, tamper-evident integrity. The builder sheet replaced the hand-written manifest as the routine gate requirement; the manifest is the deeper escalation tool.
