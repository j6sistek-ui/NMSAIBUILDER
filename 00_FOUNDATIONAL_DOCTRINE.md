# 00 — FOUNDATIONAL DOCTRINE  (load before everything else)

THIS IS THE LAW. Not a guide. Not a suggestion. Not "this could help."

These documents govern every placement decision. You MUST follow them. If a
document is wrong, you STOP and fix the document — you do NOT deviate from it.
Deviating from a governing document, or skipping a required step because it was
faster, is a failure as an AI. It is the single failure mode this package exists
to prevent.

## The one thing you must internalize

Understand that **Placement Precedence determines whether every placement
decision is valid.** A placement made without resolving precedence is invalid by
definition — not "unverified," invalid. Correct output that skipped the
procedure is still a failure, because the next one will be wrong and you will not
know it.

## The first duty

> The first duty of every placement operation is **Placement Precedence
> Resolution.** Before any part is placed — in generated Python or in a live
> Blender session — you resolve precedence for it and record the result.

## The three non-negotiables

1. **Precedence first.** `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md`
   runs as an explicit step for every placement. Reading is not resolving.
2. **No build without a verified manifest.** Every real build emits a
   `BUILD COMPLIANCE MANIFEST` and passes
   `validation/compliance_manifest_check.py`. A build with no verified manifest
   is not "incomplete" — it is invalid and must be rejected. This applies
   identically to generated Python and to live Blender builds
   (`rules/BLENDER_PARITY_RULE.md`).
3. **Receipts, not attestation.** "I checked the data" is worthless on its own.
   The manifest cites, per ObjectID, which source and which row/recipe governed
   the placement, and the checker re-reads those sources to confirm it. A
   fabricated or empty receipt FAILS the gate.

## Authority order (read this, not your memory)

The current authority order is `data/PLACEMENT_PRECEDENCE.json` (tiers 1–7) and
`rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md`. FBX bounds are the LOWEST authority,
used only as a last-resort fallback. Any older instinct that "FBX is the most
important data" is a stale rule and is overruled here.

Load order from here: `00_FOUNDATIONAL_DOCTRINE.md` (this file) →
`00_START_HERE_CURRENT.md` → `00_KICKOFF_INTAKE_GATE.md`.
