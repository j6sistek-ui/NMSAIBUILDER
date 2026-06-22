# NMS Build vs Image Routing Guard — 2.06.01

## Status
**Mandatory guard** for every NMS-context prompt that uses words such as "create", "make", "build", "generate", "design", or "construct".

## Problem fixed
A prompt can use the ordinary word "create" while still meaning "create an NMS Builder Python build", not "create a rendered image." In NMS Builder sessions, project context wins unless the user explicitly asks for a visual artifact.

## Routing rule
When the user is operating inside the NMS Builder protocol, interpret build-language as NMS build generation/refinement unless the user explicitly requests one of:

- image
- picture
- render
- mockup
- concept art
- visual only
- screenshot-style reference
- illustration

Do **not** call an image generation tool for an NMS build request merely because the user said "create", "draw", "visualize", or described a scene/style.

## Required action
For an NMS-context prompt like:

```text
Create a gothic castle with metal parts, and the front entrance is an airlock door with 12 sides, flush with the entrance walls.
```

the correct route is:

```text
request_type: build_generation
prompt_class: PYTHON_BUILD_GENERATION + FEATURE_INTENT_ROUTING + CONTROL_TO_VARIANT_DERIVATION
feature routes: gothic/castle facade + radial_airlock_iris_door
output: Blender Base Builder Python, or a clarification if the requested output channel is ambiguous
```

The assistant must:

1. Run the request router first.
2. Load the build-generation bundle.
3. Load the execution kernel.
4. Use the prompt-to-feature router.
5. For "12-sided airlock", load the airlock/iris recipe and control-to-variant protocol.
6. Ask a clarification only when the requested output artifact is genuinely unclear.
7. End with the protocol banner.

## Clarification trigger
If the user asks to "create/design" a build but does not say whether they want Python, a planning schematic, or source-doc patch, ask a single targeted question rather than generating a visual artifact.

Preferred clarification:

```text
Do you want this as executable NMS Builder Python now, or as a short placement plan first?
```

If recent context says the user is testing build execution, default to executable NMS Builder Python rather than asking.

## CAPA link
This rule was added after a protocol breach where a gothic metal castle / 12-sided flush airlock prompt was misrouted to image generation and omitted the protocol banner.
