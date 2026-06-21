# Blender AI Review Bundle Add-on

## Status

Active toolkit entry. Use the latest add-on in this folder when visual review evidence is needed.

## Current recommended version

`toolkit/nms_ai_review_bundle_addon_v04.py`

## Purpose

The add-on creates a review ZIP containing screenshots, capture-set metadata, object summaries, a review checklist, and an Open Topics Log.

It is designed for the NMS Builder workflow where the AI generates Blender scripts, the user runs them in Blender, and the AI reviews standardized visual evidence rather than arbitrary screenshots.

## Use

1. Install the add-on in Blender.
2. Run the generated NMS build script.
3. In the 3D View sidebar, use the `NMS AI` review panel.
4. Use JPEG and a capped image count for chat uploads.
5. Upload the review ZIP along with authoritative NMS Builder export JSON when run_gate/objective validation is needed.

## Important limitation

Visual bundles are not authoritative NMS save/export JSON. They complement, not replace, `validation/run_gate.py`, recipe conformance, intent graph conformance, and build-objective checks.
