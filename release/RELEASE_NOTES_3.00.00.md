# Release Notes 3.00.00 — AI Visual Capture Compliance Gate

## Status

Major rulebook release.

## Why this is major

Generated builds were becoming too complex for exterior-only screenshot review. Full buildings, interiors, Gotham/city scenes, and review-required decorations require semantic visual capture support and source-enforced script organization.

## Added

- `rules/BLENDER_VISUAL_FEEDBACK_HARNESS_PROTOCOL.md`
- `rules/AI_CAPTURE_COMPLIANCE_CONTRACT.md`
- `validation/ai_capture_compliance_check.py`
- `toolkit/BLENDER_AI_REVIEW_BUNDLE_ADDON.md`
- `toolkit/nms_ai_review_bundle_addon_v04.py`

## Updated

- `validation/run_gate.py` now surfaces AI capture compliance for build-generation scripts.
- `validation/ai_review_bundle_check.py` now supports v01-v04 review bundles.
- `release/release_check.py` runs AI capture compliance self-tests.
- `00_START_HERE_CURRENT.md`, bootstrap prompts, README, changelog, and rule matrix now include AI visual review requirements.

## Required behavior

Generated build scripts must include an `AI_CAPTURE_COMPLIANCE` manifest unless they are not build-generation scripts. Full buildings/rooms/cities must expose exterior and interior semantic roles. Review-required parts must be isolated or declared. One-collection builds must use fallback capture logic rather than fake collection isolation.

## Validation

Run:

```text
python -S release/release_check.py
```
