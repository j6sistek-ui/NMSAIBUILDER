# Release Notes 5.00.00 — Placement-Precedence Constitution + Gate-Verified Build Compliance

Major release. Changes the governing workflow.

## What changed
- Foundational Doctrine block loads before everything (`00_FOUNDATIONAL_DOCTRINE.md`): the documents are law; deviation is failure.
- Placement Precedence is now a mandatory workflow STEP, per ObjectID: Placement Intent -> Precedence Resolution -> Method Selection (`rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md`).
- No build is valid without a gate-verified BUILD COMPLIANCE MANIFEST (`rules/BUILD_COMPLIANCE_MANIFEST_RULE.md`, `validation/compliance_manifest_check.py`). Receipts are re-verified against the cited sources, not self-attested.
- Blender parity: live Blender builds obey the identical procedure and gate as generated Python (`rules/BLENDER_PARITY_RULE.md`).
- Onboarding output is a READ/SKIPPED checklist of every package document (`rules/SESSION_ONBOARDING_CHECKLIST_RULE.md`).
- Part-data authority restated; FBX demoted to last-resort fallback (`rules/PART_DATA_AUTHORITY_STATEMENT.md`).
- Banner carries a router + precedence receipt.
- Promoted non-snap build-study findings: 6 null-spawn parts added to negative knowledge.

## Validation
Full `release/release_check.py` must report RELEASE GATE: PASS, including the new
compliance-manifest verifier self-test.
