# Universal Rules v37

These rules apply to every generated No Man's Sky Base Builder Python script unless explicitly superseded with user approval.

## Hard rules

1. **Real NMS parts only.** Use `BUILDER.add_part(ObjectID)` templates and duplicate them. Do not use raw Blender primitives as build parts.
2. **Full library for selection, not a whitelist.** Search the full ObjectID library for design potential.
3. **Validation before delivery.** Run `SCRIPT_VALIDATION_LOOP.md` before providing code. If it fails, rewrite.
4. **Scoped part-rule validation.** Validate placement/rule lessons only for ObjectIDs/families used in the script. Design exploration may still use the broader library.
5. **Immediate documentation update.** When a rule/fix is correctly understood and applied, promote it into the master docs/rules immediately.
6. **Origin is not visual center.** Use FBX `extent_*` and `center_*` to compute visible bottom/top/center placement.
7. **Connected means connected.** Trim/wall/ring runs called continuous must be calculated to touch or overlap.
8. **Builder preflight before cleanup.** Do not delete scene objects before NMS builder runtime is resolved.
9. **No Wonder Projector generation.** `HOLO_DISCO` is prohibited for generated builds unless preserving a configured existing object.
10. **U_PARAGON is not Wonder Projector.** Treat it as plugin/default placeholder/non-visible artifact.

11. **Per-response protocol confirmation.** Every substantive response emits the one-line banner from `rules/PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE.md`. If the request type is unclear, do not guess — ask the user. A genuinely new request type must be added cleanly via the documented `adding_new_request_type` process in `rules/REQUEST_ROUTER_CHECKLIST.json`, not improvised.

## Deviation policy

If a rule is bad, stale, or over-constrains design intent, ask the user for approval before violating it. Do not silently deviate.

See `UNIVERSAL_RULES.md` for machine-readable form.


## Object-use recording

As objects are used in a build, record their purpose. Each substantial script needs a `BUILD OBJECT USE MANIFEST`. Creative/nonliteral uses that succeed or receive user approval must be promoted to the part-use catalog.

## Creative use-case logging

Screenshots, JSON exports, reference images, and study results are memory inputs. Log reusable part applications immediately.


## Selective visual memory rule

Useful examples should be stored as lessons first, images second.

Default: document the principle/use-case in text or structured JSON.

Retain the image only if it is a critical visual anchor: status-quo-breaking, best-in-class, failure reference, hard-to-describe geometry, or part-specific evidence.

Do not over-store redundant visual examples. Prefer compact principles that improve future build execution.

## v42 experimental prompts
When a prompt is broad/experimental/creative, the default is exploration mode.

- Do not default to known-good motifs.
- Use proven rules as constraints, not as templates.
- Suppress comfort motifs unless they have a named role.
- Require each part to add visible value.
- Prefer fewer stronger concepts over filler variants.
- Treat screenshots/in-game review as truth.

## v43 specialized-mode scope firewall

Some knowledge repositories are mode-specific. Corvette building is the first explicit repository of this kind.

Universal low-level rules still apply everywhere, but mode-specific requirements must not leak into unrelated builds.

For Corvette work:

- read `/corvette` first;
- apply Corvette minimum categories only to Corvette projects;
- preserve the universal real-object/no-proxy generator contract;
- promote only genuinely universal lessons out of `/corvette`.

## v44 Corvette decorative-use scope rule

Corvette ObjectIDs are part of the full ObjectID library and may be used creatively outside Corvette builds.

Using a Corvette part as decoration, architecture, display, trim, lighting, greeble, or kitbash material does not trigger Corvette completeness requirements. It triggers normal ObjectID placement validation plus Object Use Manifest documentation.

Only Corvette build intent or Corvette functional-role assignment activates the Corvette repository's required-category failure checks.


## Non-uniform scale safety rule

A valid generator must use real NMS ObjectIDs, but that alone is not enough. Do not non-uniformly stretch a real part into unsupported geometry unless the user approves or a validated part/family exception exists.

For long rods, legs, rails, cables, or braces, repeat uniformly-scaled real segments instead of stretching one part.


## Video reference review rule

When the user uploads a build video, do not treat it as screenshots only. Review it for movement, pathing, reveal order, lighting/fx behavior, zone transitions, and scale over time.

Default storage: document lessons. Retain only a lightweight contact sheet/key frames if the video is a high-value anchor.

## HOLO_DISCO_0 Wonder Projector update

`HOLO_DISCO_0` is also a Wonder Projector ObjectID. Do not generate `HOLO_DISCO` or `HOLO_DISCO_0` in scripted builds unless explicitly preserving an already configured user-provided object.

## v53 JSON → Python recreation default
For the current exported NMS base JSON intake path, use the validated transform stack:

```python
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
```

This is the default for JSON→Python recreation after validation on the 249-object and 1,237-object multi-axis samples. Continue auditing new ObjectIDs and do not silently substitute missing parts.

## v54 JSON study and recipe extraction
When JSON is supplied for a finished base, analyze it as a placement dataset:

```text
ObjectID counts
scale distributions
spacing
connection behavior
module envelopes
feature recipes
negative lessons
```

Use JSON geometry, FBX dimensions, and screenshots together. Do not promote weak or context-only placement into a reusable rule.

## v54 Endpoint-driven stairs and assemblies
Stairs, ramps, vehicles, tabletop games, display walls, power networks, and circular doors must be generated as connected modules with local coordinate frames or endpoint/path/ring logic. Do not place them as independent decorative objects.

## Power / utility default exclusion
Power/logic utility infrastructure is not part of normal generated architecture unless explicitly requested. Ignore/exclude `U_POWERLINE`, `U_SWITCH*`, `U_BATTERY*`, `U_SOLAR*`, `U_BIOGENERATOR`, and related utility parts by default.

## Connected-piece curvature as broad feature grammar
Do not over-restrict curved feature knowledge to exact named recipes. Dome, cylindrical habitat, spire, Taj dome, Bumblebee body shell, vehicle hull, and similar examples are instances of connected-piece curvature grammar. Use curve/path/profile, overlap/chord spacing, scale profile, convergence/contact validation, and Position/Up/At transformation to adapt them to new shapes.

## Prompt routing is mandatory
Every NMS project prompt must be classified before action. Triggered rules must be checked and applied before output. Failure to apply an existing triggered rule is a protocol application failure.
