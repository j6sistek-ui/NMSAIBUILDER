# Selective Visual Memory + Delta Learning Policy v41

## Purpose

The visual-reference system is not a scrapbook. Its purpose is to convert user-supplied images, screenshots, JSON builds, and manual examples into compact, reusable build intelligence.

Store the **lesson first**. Retain the image only when the image itself is necessary for future recall or correction.

## Escalation levels

| Level | Action | When to use |
|---:|---|---|
| 0 | Do not log | Redundant, low-signal, or already covered by an existing principle/example. |
| 1 | Document lesson only | The image teaches a reusable principle, but the visual does not need to be stored. This should be the default. |
| 2 | Retain as visual anchor | The image is status-quo-breaking, best-in-class, hard to describe in text, or needed to prevent recurring failure. |
| 3 | Promote to rule | The example corrects a design rule, orientation rule, offset rule, scale/spacing rule, or part-specific behavior. Must update rule docs immediately. |

## Default behavior

Most useful references should become **Level 1** entries:
- principle learned
- changed assumption
- reusable build technique
- candidate object roles / part families
- failure risks
- where to apply / where not to apply

Only a small curated subset should become **Level 2** visual anchors.

## When to retain the image

Retain a thumbnail or image only if one or more are true:

1. **Status-quo-breaking:** shows something that contradicts or expands a prior assumption.
2. **Best-in-class exemplar:** unusually clear example of a technique/style.
3. **Failure reference:** visually captures a recurring failure mode.
4. **Hard-to-describe geometry:** text alone cannot communicate the spatial/scale relationship.
5. **Part-specific evidence:** proves an orientation, offset, depth, scale, or nonliteral use-case.

## Duplication limit

Do not keep many examples of the same principle. For repeated ideas such as “organic parts can become structure,” keep 1–2 anchor images maximum, then document additional examples as text-only lessons.

## Delta-first learning rule

When a reference shows something different from what was previously assumed, document the **delta**:

- prior assumption
- new observation
- corrected principle
- affected parts/families
- rule update required?
- image retained? yes/no and why

## Relationship to validation

Visual references are used for **design potential** and conceptual generalization.

Placement validation still checks only the ObjectIDs and part families present in the current script/build.

## v42 study-review visual memory
When the user provides screenshots of an experimental study, screenshots are selection signals.

- Screenshotted/praised variants: analyze and preserve the lesson.
- Unscreenshotted weak variants: removal or overhaul candidates.
- Do not retain every study variant as visual memory.
- Store the principle unless the geometry is hard to describe or critical.

## Image retention decision gate
Before copying screenshots/images into a master source package, make an explicit retention decision:

```text
DOCUMENT_LESSON_ONLY
KEEP_1_TO_2_ANCHORS
CONTACT_SHEET_ONLY
FULL_REFERENCE_SET_APPROVED
```

For repeated visual examples of the same concept, default to `DOCUMENT_LESSON_ONLY` or `KEEP_1_TO_2_ANCHORS`. Full-size multi-image retention requires explicit justification or user approval.

Source-doc update reports must state the image-retention decision.
## Blender understates the look; in-game is authoritative

Blender's viewport conveys geometry/placement only — flat grey, no materials, no emissive/glass, no lighting, no environment. In-game capture is authoritative for color, material, emissive, lighting, recognizability, and scene context. Never judge aesthetic quality or whether a build "reads" from Blender screenshots alone (e.g., SET_CLASS beams are invisible in Blender; a 15-color ball set is all grey in Blender).

## Delta learning (absorbed from DELTA_LEARNING_PROTOCOL)
## Purpose

The highest-value learning is not repeating known ideas. It is capturing what changed.

When a user example reveals something different than previously assumed, immediately document the delta.

## Required delta entry fields

- `prior_assumption`
- `new_observation`
- `corrected_principle`
- `affected_parts_or_families`
- `evidence_type` — screenshot, JSON build, manual placement, in-game observation, script failure
- `confidence` — exploratory / likely / validated
- `rule_update_required` — yes/no
- `visual_retention_level` — 0/1/2/3
- `next_action`

## Escalation

If the delta corrects a rule, offset, orientation, scale, or part-specific behavior, promote it to the relevant master rule file immediately.

If it is a design concept, log it in the part-use catalog or visual reference examples.

If it is redundant, do not store it.


## Visual reference intake (absorbed from VISUAL_REFERENCE_INTAKE_PROTOCOL)
## Purpose

When the user uploads No Man's Sky screenshots, reference photos, video stills, or architectural examples, treat them as potential **build-capability training data**, not only as current-project inspiration.

The assistant must perform a documentation pass before using the images to drive script changes.

## Required intake sequence

For every meaningful reference batch:

1. **Evaluate the visual lesson**
   - What changed compared with prior assumptions?
   - Does the image show a new composition strategy, part use, scale trick, lighting method, surface treatment, or pathing solution?

2. **Classify the lesson**
   - **Rule**: validated broadly or safety-critical.
   - **Toolkit technique**: broadly reusable, but not mandatory.
   - **Project observation**: useful only to the current build until further validation.
   - **Image-only anchor**: rare, retained when the image itself is important for recall.

3. **Document before generating the next major script**
   - Update active project notes if the lesson affects the current build.
   - Update toolkit/visual-reference notes if the lesson is broadly reusable.
   - Do not silently absorb references into code without recording the finding.

4. **Escalate storage selectively**
   - Most images should become text lessons, not stored assets.
   - Store a lightweight contact sheet only when the reference materially changes the build system or breaks the status quo.

5. **Tie part-use lessons to actual NMS parts**
   - If an image suggests a structural technique, list candidate NMS part families.
   - Validate ObjectIDs, dimensions, orientation, and scale before scripting.

## Classification defaults

When uncertain, use the less binding category:

```text
rule > toolkit technique > project observation > script comment only
```

Premature rule promotion is harmful. Toolkit entries can graduate later after repeated validation.

## Required response behavior

When the user provides reference images for learning, the next response should include a short intake block:

```text
Reference intake:
- Classification:
- Reusable build lessons:
- Candidate NMS part families:
- What will be documented:
- What is not yet validated:
```

## Failure mode corrected in v51

The Alien Megatemple reference images were initially evaluated verbally and applied to design direction, but they were not formally captured as reusable toolkit knowledge before additional scripting.

Corrective action: v51 adds the alien city-canyon toolkit notes and this protocol.

## Current retained visual anchor

`visual_library/contact_sheets/ALIEN_CITY_CANYON_VISUAL_TOOLKIT_v51.jpg`

## v52 clarification: reference photos vs validation photos

Not all in-game screenshots are treated the same.

### A. General reference / toolkit photos

Treat an in-game screenshot as **general build-knowledge intake** when it is **not directly derived from the current generated script/build under review**.

Examples:
- other players' bases;
- older user bases not created by the active script;
- Reddit/community examples;
- architectural style examples;
- photos sent to expand creativity, part usage, lighting language, or composition.

Required handling:
- classify as Rule / Toolkit technique / Project observation / Image-only anchor;
- document reusable lessons before major script changes;
- identify candidate part families and build methods;
- do not assume the exact visible build is reproducible without part validation.

### B. Current project validation photos

Treat an in-game screenshot as **validation evidence** when it is directly derived from the active/current script or current hand-adjusted build branch.

Examples:
- screenshots of V03 Alien Megatemple after loading the generated script;
- screenshots of Taj V46/V46e after script load and user minor adjustments;
- screenshots showing current-script failures, gaps, flipped parts, floating pieces, scale errors, lighting failures, or successful corrected behavior.

Required handling:
- compare the photo against the current script’s stated design target;
- identify pass/fail observations;
- document regressions, confirmed fixes, and validated part behavior;
- update project notes and rule/toolkit docs only after the behavior is confirmed;
- treat the screenshot as source-of-truth over what the code intended.

### Decision rule

```text
If the screenshot came from the active generated build branch → validation photo.
If it came from outside the active generated build branch → reference/toolkit intake.
```

### Mixed cases

If a screenshot is a current-project image but also reveals a broadly reusable technique, classify it twice:

```text
primary = validation photo
secondary = toolkit candidate after validation
```

Do not promote current-project observations to universal rules until repeated or clearly general.


## Screenshot intake taxonomy (absorbed from SCREENSHOT_INTAKE_TAXONOMY)
## Purpose

This file distinguishes two different screenshot workflows:

1. **General reference / toolkit intake**
2. **Current project validation**

The distinction matters because the documentation and action sequence are different.

## Taxonomy

| Screenshot type | Definition | Primary use | Required handling |
|---|---|---|---|
| General reference / toolkit photo | In-game or concept image not derived from the current generated script/build branch | Expand general build capability | Classify and document reusable lessons before applying to scripts |
| Current project validation photo | Screenshot from the active generated script/build branch or user-adjusted current branch | Validate or reject current script behavior | Compare against script intent, record pass/fail, confirm fixes/regressions |
| Mixed evidence photo | Current-project screenshot that also reveals a reusable technique | Validate current branch first, then optionally promote to toolkit candidate | Do not promote to general rule until validated/repeated |

## General reference workflow

Use this when the user sends other bases, community builds, older bases, architecture references, or examples intended to teach design language.

Required output:

```text
Reference intake:
- Classification:
- Reusable build lessons:
- Candidate NMS part families:
- What will be documented:
- What is not yet validated:
```

## Current project validation workflow

Use this when the user sends screenshots from the script/build currently under review.

Required output:

```text
Validation review:
- Version/build branch:
- Intended behavior:
- Observed behavior:
- Pass/fail:
- Required correction:
- Rule/toolkit impact:
```

## Action rule

```text
Current project photos are source-of-truth validation.
External or non-current-project photos are general knowledge-building references.
```

## Examples

### General reference

User sends an in-game cyberpunk city screenshot from another base while planning a new alien megatemple.

Classification:
- Toolkit technique candidate.
- Capture lessons about city-canyon enclosure, lighting infrastructure, surface density, and machinery-as-wall-skin.

### Validation

User loads `MASTER_LESSONS_LEARNED.md` (removed historical reference: nms_alien_megatemple_v03_surface_built_megatemple.py) and sends screenshots.

Classification:
- Current project validation.
- Check whether V03’s triangular shell, portal, side surfaces, and blade ribs match intended behavior.
- Update validated part behavior only after confirming it in those screenshots.

### Mixed

User sends a current-project screenshot showing a successful new blade-rib method.

Classification:
- Primary: validation of current build.
- Secondary: toolkit candidate if the method appears reusable.
## Blender understates the look; in-game is authoritative

Blender's viewport conveys geometry/placement only — flat grey, no materials, no emissive/glass, no lighting, no environment. In-game capture is authoritative for color, material, emissive, lighting, recognizability, and scene context. Never judge aesthetic quality or whether a build "reads" from Blender screenshots alone (e.g., SET_CLASS beams are invisible in Blender; a 15-color ball set is all grey in Blender).


## Visual reference lessons (absorbed from VISUAL_REFERENCE_LESSONS)
**Status:** universal workflow rule.

Screenshots and reference images are build data. The AI must extract design lessons from them, not merely look at them for the immediate answer.

## Extract from each useful image

- target scale: micro, medium, macro/landmark
- silhouette and dominant shapes
- connection logic: what touches/overlaps/anchors what
- part economy: where large scaled parts outperform many small parts
- detail density: where micro-detail helps or becomes noise
- spatial rhythm: rings, rows, bays, arches, columns, ribs, lattice, steps, clusters
- material/color role
- failure modes shown: gaps, floating parts, wrong handedness, over-density, flatness
- reusable technique to log

## Good-example handling

When the user sends examples from other bases or architecture, record transferable lessons even if those examples are not part of the current build.

## Do not overfit

Do not copy one example blindly. Translate it into part-role logic:

```text
reference form -> NMS part families -> scale/orientation/overlap strategy -> study file -> promote if successful
```


# v40 explicit screenshot-reference logging rule

When the user provides screenshots or external build-reference images, do not merely acknowledge them. Create/update a visual-reference entry with:

1. source filename or identifier
2. visual theme
3. silhouette / massing lesson
4. connection / structural lesson
5. lighting / color lesson
6. candidate ObjectID families or object roles
7. transferable use cases
8. known failure risks
9. whether the lesson is universal, project-specific, or exploratory

The visual-reference entry should be used during design-potential review. Placement validation remains scoped to ObjectIDs actually used in the current script.


# v41 visual retention rule

Visual references must be curated, not accumulated.

For each image/reference:
1. extract the principle,
2. decide whether it changes prior understanding,
3. assign retention level,
4. retain image only for Level 2+ entries,
5. promote rule-correcting deltas to Level 3.

Do not keep many images for the same principle. Keep one or two anchors; store additional examples as text-only lessons.

# v42 Visual Lessons — Deep Sea Skyscraper Cluster and Study Reviews
## VR42_deepsea_room_skyscraper_cluster

The user-provided skyscraper reference shows circular and square deep sea rooms used as colorful modular tower fabric. Reusable lesson:

- `MAINROOM_WATER` and `MAINROOMCUBE_W` create a strong repetitive high-rise language.
- Color blocking is part of the architecture.
- Rooftop features should create skyline identity, not just another stacked room.
- Topper modules should include distinct silhouettes: receiver yokes, crane caps, docking crowns, data racks, reactor caps, antenna gardens, parasite pods, or light arrays.
- Detail must be connected to room geometry.

Retention classification: Level 1 text lesson. The screenshot is useful, but the transferable rule is the modular-room skyline principle, not the exact image.

## VR42_experimental_study_review

User feedback on V29-V31 clarifies that experimental requests should not default to comfortable proven motifs. The desired output is exploratory: unique, detailed, advanced glitch-building style, with every part serving a purpose.

Retention classification: Level 3 promoted rule via `rules/EXPERIMENTAL_REQUEST_PROTOCOL.md`.

# v49 completed project outcome anchor

Completed projects may retain one lightweight final contact sheet when the outcome is important for future design recall. The Taj Mahal final contact sheet is retained as a Level 2 project-outcome anchor:

`project_outcomes/taj_mahal/TAJ_FINAL_V46E_CONTACT_SHEET_v49.jpg`

Do not store every screenshot. Store the result, the process lesson, and the validated part-use findings.

# v51 alien city-canyon visual reference lesson

Classification: **Toolkit technique**

The uploaded city/megatemple screenshots teach a reusable composition principle:

```text
scale is created by enclosure, layered depth, surface density, and lighting infrastructure
```

Not just by object height.

A lightweight reference contact sheet is retained:

`visual_library/contact_sheets/ALIEN_CITY_CANYON_VISUAL_TOOLKIT_v51.jpg`

Core build lessons:
- Build architectural canyons with tall side masses and overhead elements.
- Use repeated panels/seams to create surface-built monuments.
- Use negative-space portals as focal geometry.
- Embed machinery and pipes into walls rather than placing them as loose clutter.
- Treat lighting as infrastructure: seams, paths, portals, gravity columns.

# v52 current project validation exclusion

The visual reference intake protocol applies to screenshots that are **not directly derived from the active/current generated build branch**.

Current project screenshots are handled as validation evidence first. They may become toolkit candidates only after the observed behavior is validated and judged reusable.


## Creative use-case logging lane (absorbed from CREATIVE_USE_CASE_LOGGING_PROTOCOL)
**Status:** universal rule.

The part-use catalog is active memory. When a user provides screenshots, build JSON, manual edits, study winners, or direct feedback that demonstrates a creative or effective use of a part, log the lesson immediately.

## Why this exists

The AI repeatedly falls back to comfortable designs when creative examples are not recorded. This protocol forces useful examples to become retrievable build memory instead of staying in chat history.

## Trigger conditions

Log a candidate use case when any of these occur:

- user says a detail/build is good, amazing, creative, effective, or worth remembering
- a part is used for a nonliteral role, such as a wall becoming a book or backboard
- scale, rotation, color, clustering, partial burial, or repetition changes a part's perceived role
- a JSON export shows unusual high-frequency use, repeated rows/rings/shells, or scale/orientation patterns
- a screenshot demonstrates a successful architecture, furniture, landscape, micro-build, macro-build, or style technique
- a study reveals a better part-count vs visual-quality solution, such as a lower-count dome method

## Required log fields

```text
id
source_type
source_description
parts_or_families
visual_role
literal_role_if_known
transformation_methods
scale_pattern
orientation_pattern
color_or_material_notes
context_where_it_works
why_it_works
constraints_or_failure_modes
confidence
promotion_status
```

## Design-vs-validation distinction

- The catalog is used broadly for **design potential** and creative recall.
- Placement validation, offset correction, and part-family rule checks apply only to ObjectIDs present in the current script/build.

## Required behavior after user examples

If the user provides an example or says a use is important, the AI must either:

1. update the catalog in the same documentation pass, or
2. state exactly why the example cannot be logged yet and what evidence is missing.

Do not silently skip examples.


## v40 visual reference intake requirement

Every user-supplied build screenshot, architecture reference, or style example must be evaluated for reusable lessons. If it contains a reusable part application, style strategy, lighting method, structure/connection method, or part-count conservation strategy, log it in:

- `visual_references/VISUAL_REFERENCE_EXAMPLES_vXX.md/json`
- `rules/PART_USE_CASE_CATALOG.md/json`
- `reports/OBJECT_USE_CASE_MATRIX_vXX.csv` when applicable

Do not wait for the user to ask twice. The logging action is part of the normal response workflow.


## v41 selective storage clarification

The default action for useful examples is **document the lesson only**. Do not retain the image unless it meets the Level 2 visual-anchor criteria.

Escalation summary:
- Level 0: do not log redundant references.
- Level 1: document principle/use-case only.
- Level 2: retain image/thumbnail only if critical.
- Level 3: promote to rule when it corrects validated behavior.

This prevents master-doc bloat while preserving the learning value.

## v42 experimental prompt logging
Broad experimental prompts create new logging obligations:

- classify whether the prompt is exploration or consolidation;
- log comfort motifs that were intentionally suppressed;
- record which underused part families were considered;
- record which variants were screenshotted, praised, rejected, or ignored;
- promote user-corrected study principles immediately.


## v46 video reference logging

Videos are build data. They should be reviewed for walkthrough logic, not just static frames.

Log:
- zone structure
- pathing/circulation
- reveal order
- lighting/effects over time
- readable vs noisy detail while moving
- creative part-use candidates
- failure modes

Do not store the full video in the master docs unless explicitly required.

## v53 JSON recreation logging
When a JSON→Python recreation is performed, log:

- source object count;
- unique ObjectID counts;
- transform stack used;
- skipped placeholders;
- missing ObjectIDs;
- non-unit scale records;
- extra fields preserved;
- new/unvalidated ObjectIDs;
- visual validation status.


## Part-behavior learning lane (absorbed from PART_BEHAVIOR_LEARNING_PROTOCOL)
## Status

**Mandatory when the user is teaching how a part or part family behaves and wants that behavior reused.**

## Core principle

A working source build is not only reference geometry. It is training data for a reusable **part behavior model**.

The target shape is often only the proof case. The primary subject being learned is how the part places, mates, repeats, closes surfaces, forms shells, forms lattices, forms solids, or supports decorative applications.

## Trigger phrases

Use this protocol when the user says or implies:

```text
learn how this part works
same style
same construction method
same placement behavior
apply this to another shape
use the observed data
study file
prove capability
repeat this building style
do not reinvent the wheel
the JSON already proves fitment
```

## Required workflow: Observe → Infer → Apply → Verify

### 1. Observe

From the working JSON, Python, or validated build, extract:

```text
ObjectID family
Position / Up / At / scale
material/UserData
neighbor relationships
edge/contact spacing
rotation/orientation families
repeating local grid or frame
part roles
construction style
known successful applications
```

### 2. Infer

State the candidate part behavior rule before generating variants:

```text
PART_BEHAVIOR_SIGNATURE
- locked invariants
- mating/fitment rule
- orientation rule
- density rule
- offset/pivot rule if observable
- allowed variation slots
- forbidden substitutions
```

### 3. Apply

Apply the inferred behavior to new geometry. Do not replace behavior transfer with generic geometry construction.

### 4. Verify

Compare the output against the source behavior, not merely against the target shape. Identify any failure as one or more of:

```text
fitment
offset/pivot
orientation
density
coverage
scale
material/ObjectID mapping
wrong construction style
```

## Knowledge maturity statuses

Every learned behavior or CAPA entry must be labeled:

```text
DISCOVERED  = identified in conversation or failure analysis
DOCUMENTED  = patched into master docs or recipe/signature index
VALIDATED   = proven by successful application to new geometry/build
```

Do not call a behavior fully learned until it is VALIDATED.

## Triangle panel family rule seed

For JSON-derived triangle panel studies, treat the working source as behavior evidence. Unless the user explicitly asks otherwise:

```text
LOCKED:
- source-relative Position, Up, and At are preserved as a coupled transform frame when substituting compatible triangle ObjectIDs
- source triangle size is preserved for same-style studies
- solid surface/enclosure requests are satisfied by more correctly registered triangles, not by enlarging panels
- fitment observed in the JSON outranks generic centroid-only triangle placement

FORBIDDEN:
- scaling panels larger to reduce part count
- sparse lattice/cage substitution when user requested solid surfaces
- centroid-only tessellation if the source proves a different placement behavior
- part-count optimization before fitment and closure
```

For procedural triangle surfaces, the proposed geometric frame remains:

```text
local Y / Up = facet normal
local Z / At = in-plane tangent
local X / Right = Up cross At
location = triangle centroid adjusted by learned part behavior offset when required
scale = average face edge / triangle-part baseline edge only when scale variation is explicitly allowed
```

If source JSON provides a verified fitment pattern, extract and reuse that pattern instead of inventing a new one.


## required data mapping and storage

Part behavior learning must now produce or update a `PART_PLACEMENT_MAP`.

Required added workflow:

```text
source JSON/Python/FBX
→ compute local frames from Position/Up/At
→ derive local neighbor offsets and rotation deltas
→ cross-check FBX/bounds
→ write PART_PLACEMENT_MAP
→ update placement-map index and master sheet
→ include PARTMAP STORAGE RECEIPT
```

A chat-level lesson is only `TEMPORARY_AWARENESS` until it is stored in `library/part_placement_maps/`.

A response may not claim `DOCUMENTED` unless the partmap storage receipt names the exact file, index entry, and master-sheet row.

Load:
- `rules/PART_PLACEMENT_MAP_SCHEMA.md`
- `rules/PART_PLACEMENT_MAP_SCHEMA.md`
- `rules/PART_PLACEMENT_MAP_SCHEMA.md`


---

## Directive from C_TRIFLOOR study

When the user is teaching a part, the end goal is not merely a one-off build. The goal is a reusable part-control profile.

Required validation ladder:

```text
1. Bounds/equivalence preflight
2. Default orientation check
3. Single-part transform/scale/rotation matrix
4. Phase/pivot correction if needed
5. Small capability proof
6. Family expansion only after single-part validation
```

C_TRIFLOOR is the reference success case. C_TRIFLOOR_Q is the reference warning case: similar name and shape are not enough to inherit behavior.

## lessons from TRIFLOOR V24 and stair V25-V38

Part behavior learning must now distinguish:

```text
placement-kernel validation
family-attribute validation
acceptance validation
```

The C_TRIFLOOR/TRIFLOOR work validated the placement kernel for complex triangular geometry. The stair study showed that hard families usually fail on part attributes: origin, orientation, edge offset, rotation direction, or semantic connectivity.

### Required learning question

Before generating a new family proof, answer internally:

```text
What is still unknown about this part/family?
```

Do not default to retesting XYZ movement or basic transform ordering unless evidence shows those are in doubt.

### Family-attribute targets

```text
DefaultOrientation
OriginType
ScaleBehavior
ConnectionType
SnapBehavior
PivotOffset
PhaseOffset
ConnectivityRules
FamilyExceptions
ValidationUnknowns
FamilyEquivalenceClassification
```

### Acceptance status

A learned behavior may be documented before user acceptance, but it must carry the correct ladder status from `MASTER_LESSONS_LEARNED.md` (removed historical reference: PART_VALIDATION_STATUS_LADDER.md).

No behavior is `USER_ACCEPTED` without explicit user approval.
## reference-build findings

- SET_CLASS A/B/S emissive beam (GAME_VALIDATED): beam color is class-locked — A=purple, B=blue, S=yellow/gold — and is NOT changed by material/UserData. Beam structure is identical across classes; beam length / emitter height scales with uniform scale (height ~= 11.222 * scale); the beam follows part rotation; vivid at night, washed out in daylight; not visible in Blender (geometry only). SET_CLASS footprint ~1.312 x 11.222 x 1.305 at scale 1.0; plugin auto-applies rx=90; bottom-origin, stands +Y.
- Rigid-part JSON transform convention (GAME_VALIDATED, cross-checked across 5 builds): world up axis = Y (Position[1]); At = unit forward (|At|=1.0000); uniform scale = |Up|; Up perpendicular to At; UserData = material/color slot; Timestamp = build order. This applies to RIGID PLACED parts only. It is NOT extended to wired connectors (powerlines/cables) — see NEGATIVE_KNOWLEDGE_INDEX retraction of the powerline-At reading.
- Walkable rise is an absolute, scale-invariant constraint (GAME_VALIDATED): a working spiral stair holds rise ~= 0.227 across all levels regardless of part scale. Scaling a working stair up breaks walkability — mechanics lock spacing while decorative builds keep free scale.
