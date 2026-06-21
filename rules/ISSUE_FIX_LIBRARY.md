# NMS Issue / Fix Library

*Updated 2026-05-25. Use this as a preflight checklist before generating scripts.*

## builder_ui_visible_but_add_part_missing

**Scope:** universal_script_safety

**Symptom:** RuntimeError: Could not find bpy.context.scene.nmsdk_builder.add_part

**Cause:** NMS Base Builder UI can be visible while the active scene/base runtime is not initialized.

**Fix:** Resolve builder before cleanup/generation; try scene.nmsdk_builder, extension module BUILDER, then loaded modules. If unresolved, stop safely and have user create/import/open a base in the panel.

**Never:** Never delete/clear objects before builder preflight succeeds.

## permission_denied_optional_json_export

**Scope:** universal_script_safety

**Symptom:** PermissionError: [Errno 13] Permission denied when writing placement JSON

**Cause:** Blender current path may be protected or unsaved/internal.

**Fix:** Disable optional exports by default or probe writable folders. Export failure must not break geometry generation.

## ring_gaps_despite_correct_orientation

**Scope:** part_family_short_wall_trim

**Symptom:** Trim pieces face tangent direction but do not connect end-to-end around circle.

**Cause:** Radius, count, and scale were chosen independently.

**Fix:** Use chord formula and target small overlap.

## effect_part_body_noise

**Scope:** effect_parts

**Symptom:** B_SHL_E/TURRET_ABAND bodies look noisy or generic when repeated.

**Cause:** Effect parts treated like visible ornaments instead of hidden emitters/lenses/projectors.

**Fix:** Recess, bury, or frame bodies; expose only glow/beam/lens where possible.

## wrong_red_oculus_part_mapping

**Scope:** part_specific

**Symptom:** Red oculus study lost intended red glow or used wrong center part.

**Cause:** B_SHL_E and B_DECO_P roles were confused.

**Fix:** B_SHL_E = red glow/lens; B_DECO_P = radar dome/core only.

## temporary_electric_fx_misinterpreted

**Scope:** part_specific

**Symptom:** Electricity disappears after time or is missing after part swap.

**Cause:** Titan Heavy Booster electricity is temporary load-in FX and requires B_WNG_A.

**Fix:** Use B_WNG_A buried as emitter; design still reads after FX fades.

## study_variants_mixed_into_core

**Scope:** workflow

**Symptom:** Core file becomes cluttered or loses known-good variants.

**Cause:** Study variants were mixed into the core baseline before promotion.

**Fix:** Keep study files separate; preserve V25 locked core unless user promotes/removes variants.

## terrain_marker_adjustment_applied_to_build

**Scope:** workflow

**Symptom:** Actual geometry shifts when only grade reference should move.

**Cause:** Terrain/floor marker treated as build geometry.

**Fix:** Move only marker/reference layer unless the user explicitly says the object itself should move.


## bottom_origin_parts_treated_as_center_origin

**Scope:** universal_geometry / origin_semantics

**Symptom:** Walls, arches, trim rows, minarets, cylinders, or bead stacks float above floors/plinths even though the script appears to add/subtract half-heights. Entrance pieces may also appear half-buried.

**Cause:** The script assumes `place(x,y,z)` is the mesh center. In Blender/NMS Builder, `place()` sets the object origin. Many construction parts are bottom-origin after `rx=90` because FBX `center_y ≈ extent_y/2` (`S_WALLM`, `S_WALLM_H`, `S_WALL_Q_H1`, arches, cylinders, spheres). Some floors are center-origin (`S_FLOOR center_y = 0`).

**Fix:** Compute visible bottom/top from FBX bounds: `bottom_rel=(center_y-extent_y/2)*scale`, `top_rel=(center_y+extent_y/2)*scale`, then set `origin_z = desired_bottom - bottom_rel` or `origin_z = desired_top - top_rel`. Use semantic wrappers such as `place_bottom()` and `place_top()` so code cannot silently mix center and bottom placement.

**Never:** Never add `height/2` to wall, arch, cylinder, sphere, or `S_WALLM_H` ring z positions unless FBX `center_y` proves the part is actually center-origin.

## trim_rows_cross_at_corners

**Scope:** wall_rows / trim_rows

**Symptom:** End of long wall/cornice rows shows an odd plus/cross shape or overlapping perpendicular trim at corners.

**Cause:** Both face directions run trim pieces all the way to the same corner endpoint. Since trim pieces have length and depth, perpendicular rows overlap and create an unintended cross.

**Fix:** Use a trim-specific span helper with `corner_clear`, or stop one face's trim before the corner and cover the corner with a deliberate corner cap/post.

## stair_or_entrance_built_from_wall_slabs

**Scope:** entrances / elevation transitions

**Symptom:** Garden entrance/stairs are half below floor, float, or read as buried wall panels.

**Cause:** Vertical wall parts are used as stair treads without top-surface math.

**Fix:** Build entrances from floor/top-surface pieces (`S_FLOOR`, `S_FLOOR_Q`, paving) with explicit visible `top_z`; use wall parts only as risers when their visible bottom/top are intentionally calculated.


## Stone Architecture Close-Up Issues — added 2026-05-26

### Symptom: corner gaps remain even after wall rows are origin-corrected

**Likely cause:** trim/cornice rows were over-cleared at the endpoints to avoid cross artifacts. This leaves visible open end gaps.

**Fix:** trim rows should normally span nearly to the face endpoint and overlap slightly into the adjacent row. If gaps persist, add slim corner filler pieces inside the footprint rather than extending decorative trim far past the corner.

### Symptom: minaret still appears to float even when z math says it overlaps

**Likely cause:** no visible socket/pedestal connects the shaft to the plinth. Mathematical overlap below the floor is not enough if the viewer sees air or an unexplained transition.

**Fix:** build a visible foundation transition: wider lower wall-ring courses partly buried in the plinth, plus proud trim/cornice belts at the plinth/shaft junction. The base should visually grow out of the platform.

### Symptom: rooftop kiosk/chhatri base reads as generic cylinder posts, not reference-matching architecture

**Likely cause:** cylinders were used because they are easy vertical supports, but the reference uses open arch bays below the small dome.

**Fix:** use mirrored half-arch wall pieces (`S_ARCH*_H`) or scaled arch stacks to create open arched pavilion sides, then place the dome/cap above that arch base.

### Symptom: unexplained roof/parapet walls block the reference read

**Likely cause:** wall rows added for containment or height without a reference-matching role.

**Fix:** either lower them to a cornice/rail or remove them. A wall row needs a purpose: parapet, socket, arch base, visual band, or structural transition. Otherwise it becomes noise.


---

## Issue: rooftop chhatri square/mis-mirrored half-arch assemblies

**Symptom:** front/back chhatri arches look acceptable, but side faces are mirrored incorrectly or the whole kiosk reads square rather than octagonal.

**Fix:** use an 8-sided radial pavilion with full arch stacks (`S_ARCHB`, `S_ARCHM`, `S_ARCHT`) rotated around center. Phase by ~22.5° if the square read is too strong.

## Issue: minaret still reads as floating after collar fix

**Symptom:** a belt/collar touches the plinth mathematically, but from the viewer angle the minaret appears to hover.

**Fix:** add visible lower support courses/pier rings down through the plinth/base and small buttress strips where useful. Visible architectural continuity overrides pure origin math.

## scaled_macro_wall_depth_not_propagated_to_facade_overlays

**Scope:** scale / facade layering / macro wall replacement

**Symptom:** After replacing many smaller wall rows with one large macro wall
(for example `S_WALLM` or `S_WALL` at scale 6), arches, windows, relief panels,
supports, or lights disappear into the wall, float away from it, or show a
large gap even though the numeric offset was "increased."

**Cause:** The script reused offsets calibrated for the old smaller wall shell.
Scaling increased the backing wall's visible depth, so the old face coordinate
was no longer the actual visible surface. In a prior macro-wall cleanup, the facade correction was
also applied in the wrong direction: the front/stair side was moved inward
instead of outward.

**Fix:** Recalculate the visible face from FBX dimensions and current scale:
`scaled_depth = native_depth * scale`. Place overlay parts using the outward
normal from the scaled wall face. Front/stair side is `-Y`, back is `+Y`, left
is `-X`, right is `+X`. Use the overlay part's own scaled depth if it must sit
proud of the wall rather than with its origin on the face.

**Never:** Never reuse `FACE_OFF`, `FACADE_PUSH`, trim radius, or ring span
constants after a part scale change unless those constants are explicitly
re-derived from the new scaled dimensions.

## large_trim_band_short_at_row_ends

**Scope:** roof parapets / cornice rows / long scaled trim

**Symptom:** Large `S_WALL_Q` or trim-band pieces look good in the middle of a
wall but stop short near corners, leaving visible gaps or causing adjacent
architecture to look unfinished.

**Cause:** The row-span calculation uses the old wall span or over-clears
corners. At scale ~3.0, a small error in span endpoints becomes visually large.

**Fix:** Calculate row centers from the desired visible endpoint span and allow
deliberate overlap into adjacent row pieces. Use a longer span pad or one
additional piece per side rather than leaving a short band. Lower/outward
placement should be handled separately from endpoint coverage.


---

## validation_loop_skipped_before_delivery

**Scope:** universal_workflow

**Symptom:** A generated script repeats a known error, violates a documented part rule, uses the wrong part family, or fails to include required audit/guardrails.

**Cause:** Script was delivered before validating against universal rules, the current ObjectID set, part-family rules, issue/fix entries, and project constraints.

**Fix:** Extract ObjectID set, run `SCRIPT_VALIDATION_LOOP.md`, rewrite if any check fails. If a rule must be violated, request approval before delivery.

## unused_part_rules_overloaded_validation

**Scope:** workflow_efficiency

**Symptom:** Validation becomes slow/noisy because the AI attempts to apply every rule in the library to every script.

**Cause:** No distinction between broad design exploration and scoped placement validation.

**Fix:** Use full library for design potential. For placement/rule validation, inspect only ObjectIDs and families present in the current script.

## understood_fix_not_documented

**Scope:** memory_recall / documentation

**Symptom:** A previously solved orientation, offset, or spacing issue returns in a later script or different chat.

**Cause:** The fix lived only in chat memory or a one-off script and was not promoted into the master docs.

**Fix:** Immediately update the appropriate master rule/registry after the fix is correctly understood and incorporated.

## continuous_trim_has_visible_gaps

**Scope:** geometry_continuity / trim_rows

**Symptom:** A trim run is labeled continuous but has visible gaps between parts.

**Cause:** Centers were hand-spaced or set by rough offsets instead of visible scaled length and overlap.

**Fix:** Compute centers from `visible_native_length * scale` with deliberate overlap. Add end/corner closure pieces when needed. If gaps are intentional, label the row as separated/accent trim.

## user_exact_recipe_not_represented_in_study

**Scope:** study_workflow / user_directed_generation

**Symptom:** User requests an exact structural recipe, but all study options are interpretive variants.

**Cause:** The generator optimized for inferred style before proving the requested arrangement.

**Fix:** Include at least one literal option that follows the user's recipe exactly. Additional interpretive options are allowed only after the literal option exists.

## grand_structure_overdetailed_with_small_parts

**Scope:** design_execution / part_budget

**Symptom:** Landmark-scale structure uses many tiny details/cylinders that are visually lost and part-heavy.

**Cause:** Micro-build technique applied to macro architecture.

**Fix:** Use scale and connected architectural masses first. Add small details only after the main silhouette and structure read correctly.


## half_arch_mirror_orientation_flipped

**Scope:** part_family_arches / facade_geometry

**Symptom:** Mirrored half arches face the wrong direction or disappear into the macro wall.

**Cause:** Half arch pieces are handed; mirroring across an axis requires explicit orientation correction. Scaled macro wall depth can also consume overlays if offsets are not recalculated.

**Fix:** Use a per-facade handedness table, verify inward-facing openings by screenshot, and push arches outward from the scaled wall face.

## dome_wall_panels_read_vertical

**Scope:** dome_study / surface_shell

**Symptom:** Wall-panel dome reads as vertical bands rather than smooth surface.

**Cause:** Panels placed in circular rows without surface-frame tilt.

**Fix:** Use tangent/meridian/normal orientation with profile derivative and optional controlled tilt gain.

# v42 Study Failure Modes and Fixes
## comfort_zone_drift_in_experimental_prompts

**Symptom:** Experimental files repeat proven motifs such as red lens bands, antenna crowns, trim rings, light fissures, or stacked room crowns.

**Cause:** The generator treats broad creative prompts as consolidation of past successful ideas.

**Fix:** Activate exploration mode. Force divergent silhouettes, use underused part families, and require each known motif to have a new role.

## sparse_concept_thumbnail_failure

**Symptom:** Build looks like a light test layout or sparse parts on a pad rather than advanced glitch-building.

**Cause:** Not enough connected structure, focal density, or architectural integration.

**Fix:** Build macro silhouette first, then add connected detail clusters in focal zones. Prefer fewer strong concepts over many thin variants.

## floating_antenna_or_spire_failure

**Symptom:** Antennas, spires, or scanner parts float high above the object.

**Cause:** Signal parts were placed as final decorations without a mount.

**Fix:** Add visible pylon, equipment block, tower cap, scaffold, or room-top adapter. Floating is valid only if the design explicitly frames it as holographic suspension.

## conveyor_orientation_ambiguity

**Symptom:** `B_WALL_CARG1` / cargo or conveyor modules look like random barrels or misplaced cylinders.

**Cause:** No rails, target path, or machine-line context.

**Fix:** Add rails/cable trays, repeat modules with consistent orientation, place robot arms or drone bodies to establish assembly-line purpose.

## loose_drone_hive_failure

**Symptom:** Drone hive looks like loose orbiting props.

**Cause:** Drones are placed near a tower but not visibly connected.

**Fix:** Use docking collars, service struts, wall racks, bays, or visible mounts. Connect drone pods to a central spine.

## deepsea_topper_repetition

**Symptom:** Deep sea room topper study becomes repeated room stacks with red lens/antenna crowns.

**Cause:** The rooms are used as safe stackable shapes instead of distinct rooftop architecture.

**Fix:** Use room parts as macro fabric for diverse silhouettes: yokes, receivers, cranes, offsets, pods, bridges, asymmetric caps, reactor housings, and docking sockets.

# v43 Corvette / Specialized Repository Failure Modes

## corvette_objectid_dimension_proxy_failure

**Scope:** corvette_generation / script_contract

**Symptom:** Blender shows blocky proxy geometry named after Corvette ObjectIDs instead of real NMS/Corvette plugin objects.

**Cause:** The script used ObjectID metadata and FBX bounds to create generic geometry, but did not instantiate real NMS Builder objects through the plugin or copy verified plugin-created templates.

**Fix:** Corvette generators must use a valid plugin creation path or verified plugin-created templates. If required ObjectIDs cannot be instantiated, fail before creating any visible geometry.

## corvette_rules_leak_into_normal_builds

**Scope:** documentation_scope / workflow

**Symptom:** Corvette-specific ship rules such as seven required categories, ship role packages, Workshop cache behavior, or Corvette module assumptions influence ordinary base architecture.

**Cause:** Corvette knowledge was stored only as general chat/project memory instead of a scoped repository.

**Fix:** Store Corvette knowledge in `/corvette`; apply it only when the user asks for Corvette work or the script uses Corvette ObjectIDs. Promote only universal generator failures to global rules.

## corvette_objectid_not_searchable_in_blender

**Scope:** user_debugging / object_naming

**Symptom:** User cannot find generated required Corvette parts because objects have cute names or role names without ObjectIDs.

**Cause:** Names/descriptions prioritized aesthetics over technical lookup.

**Fix:** Include ObjectID, NiceName, required category, and role in object names and descriptions/custom properties.

## corvette_objectid_decorative_use_false_positive

**Scope:** scope_firewall / mode_specific_repository / creative_part_use

**Symptom:** A normal base build uses one or more Corvette ObjectIDs decoratively and is incorrectly failed for missing Corvette cockpit/reactor/landing gear/etc.

**Cause:** Corvette validation was activated by ObjectID category alone instead of by build intent or functional role.

**Fix:** Classify the use first. If the user did not request a Corvette and the Object Use Manifest marks the Corvette part as decorative, architectural, display, greeble, lighting, furniture, trim, or kitbash, skip Corvette required-category checks. Still validate the part's FBX dimensions, orientation, placement, and NMS object properties.

**Never:** Never present a decorative Corvette-part kitbash as a valid Corvette. Never require Corvette minimum categories for a non-Corvette decorative use.


## nonuniform_scale_stretches_real_nms_part

**Scope:** universal_script_safety / placement_validation

**Symptom:** Script uses a real NMS ObjectID but stretches it into an unsupported long/thin shape; object looks wrong or behaves strangely in-game.

**Cause:** Non-uniform scale was used as geometry modeling, e.g. `sx = length / native_width` while `sy` and `sz` remain small.

**Fix:** Use uniformly-scaled real parts repeated as segments. Compute segment count from FBX native extent, target length, uniform scale, and overlap.

**Never:** Do not claim the script is valid just because it uses `BUILDER.add_part()`. Real ObjectIDs can still be invalidly stretched.


## v47 — Corvette boundary clipping after Swarm-era update

**Symptom:** Large Blender/save-editor/third-party Corvette blueprints appear cut up, clipped, bugged, or invalid after the update. User-supplied community warning reports Corvette building boundaries around 100m.

**Cause:** Corvette build boundary is now materially relevant to external/generated ships. Oversized layouts that previously loaded may exceed the current build envelope.

**Fix:** For Corvette builds only, enforce `CORVETTE_SAFE_BOUNDARY_SIDE_M = 95.0` and compute occupied rotated bounds from FBX extents and scale. Reject, shrink, or redesign any Corvette layout exceeding 95m side length; never validate by object centers alone.

**Scope:** Corvette-only. Do not apply to planetary bases, freighter bases, landmark builds, megacities, or decorative non-Corvette architecture.


## v48 Corvette boundary category-filter failure

**Failure mode:** A Corvette script audits only `Category == Corvette` placements against the 95m safe / 100m absolute boundary, while ignoring non-Corvette/base/decorative parts placed on the ship.

**Why it fails:** Corvettes can be decorated with non-Corvette parts. Those parts still contribute to the final in-game ship footprint and can push the Corvette beyond the boundary.

**Fix:** In Corvette mode, run the boundary audit on every final exported placement assigned to the Corvette assembly, regardless of ObjectID category. Exclude only temporary templates, deleted scaffolds, and debug/reference markers not exported as part of the ship.

**Scope:** Corvette-mode only. Do not apply this boundary rule to normal planetary/freighter/base architecture.

## taj_arch_base_variant_patchy_face

**Scope:** Taj / white-stone façade / stone arch variants

**Symptom:** `S_ARCH` or `S_ARCH_H` shows unwanted brown/patchy stone material on the visible façade surface.

**Fix:** Use `S_ARCHM` and `S_ARCHM_H` for the same façade arch geometry when a cleaner single-color face is needed.

**Status:** validated for final Taj V46e front/rear façade context; revalidate before applying in unrelated orientations or non-stone styles.

## landmark_part_budget_over_optimization

**Scope:** large cultural/nostalgic/landmark builds

**Symptom:** The build meets the part cap but loses the recognizable subject.

**Cause:** Part-count reduction began before the macro identity and critical subsystems were solved.

**Fix:** Solve recognition first, then optimize hidden/low-value construction. Protect recognition-critical systems such as silhouette, entrance, focal façade, major towers, primary dome, or iconic vehicle/creature shapes.

## platform_floor_hidden_fill_waste

**Scope:** platform/plinth/floor optimization

**Symptom:** Large floor panels or tile fields are placed under already-covered structures, consuming parts without visual value.

**Fix:** Replace hidden central fill with visible perimeter flooring and necessary approach/stair underfloor only. Keep architectural trim/banding where it contributes to the read.

# v53 JSON → Python recreation issues/fixes
## json_recreation_wrong_side_of_axis

**Symptom:** Recreated structure has the right local shape but appears on the wrong side of a global axis.

**Cause:** Coordinate conversion/mirror error.

**Fix:** For the validated current JSON intake path use `COORD_MODE="XnZY"`.

## json_recreation_local_detail_reversed

**Symptom:** Structure overlays but square-panel local details, decals, billboards, shelves, or furniture appear reversed/upside-down.

**Cause:** Missing post-baseline local orientation correction. The square footprint can hide the error on floors/walls.

**Fix:** Apply `LOCAL_Y_180` after the validated baseline transform.

## json_recreation_family_guess_overcorrection

**Symptom:** Furniture or props pitch vertical after family-specific axis experiments.

**Cause:** Testing broad RX/RXNEG basis changes instead of preserving the validated global transform.

**Fix:** Return to the validated baseline and test only post-baseline local corrections. V14 showed universal local Y 180 is better for the tested sample.

## json_recreation_new_objectid_unknown

**Symptom:** A future base contains ObjectIDs not in the validated sample set.

**Cause:** New part family not yet observed in JSON recreation validation.

**Fix:** Recreate with the validated default transform, flag in audit, visually validate, and only then promote family-specific notes if needed.

# v54 recipe/spacing issue fixes
## generated_stairs_not_connected

**Symptom:** Stairs or ramps appear as a decorative line but do not connect to floor/landing.

**Fix:** Generate from start landing, end landing, path vector, rise/run, module count, center spacing, and contact tolerance.

## random_small_props

**Symptom:** Interior props, vehicle parts, rods, pegs, or table parts look scattered.

**Fix:** Use an object-local coordinate frame. Treat vehicle, foosball/tabletop games, lab tables, and consoles as assemblies.

## floating_platform_underside

**Symptom:** Elevated platform has a sea of floating parts underneath.

**Fix:** Generate foundation/deck/edge/underside support/access as separate connected subsystems.

## over_promoted_contextual_placement

**Symptom:** A visually successful but mechanically weak placement is treated as a reusable rule.

**Fix:** Classify it as project observation or negative lesson. Example: Jurassic Beach `C_GDOOR`/`S_GDOOR` dinosaur-mouth placements should not be promoted.

## powerline_deduplication_error

**Symptom:** Same-position `U_POWERLINE` entries are removed as duplicates.

**Fix:** Preserve same-position powerlines if vectors differ. They may encode multiple logical/visual connections.



## Failure: JSON mapping ignored despite available source truth

**Symptom:** Airlock doors, stairs/ramps, vehicle wheels, connected wall shells, or other JSON-studied systems appear flipped, disconnected, scattered, or visually unrelated to known working examples.

**Root cause:** The generator used generic Blender `rx/rz` assumptions or aesthetic placement instead of the validated JSON mapping stack and JSON-derived subsystem recipe.

**Fix:** Activate `rules/JSON_EVIDENCE_MAPPING_GATE.md`, declare the transform constants, extract ObjectID/Position/Up/At/scale from the JSON control, and rerun `validation/run_gate.py` with `--require-json-evidence`.

**Prevention:** If the user supplied JSON, pasted JSON, or referenced JSON-derived lessons, skipping JSON mapping is a systematic failure and triggers `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md`.


## NMS build prompt misrouted to image generation

### Failure
An active NMS Builder prompt requesting a gothic metal castle with a 12-sided flush airlock entrance was treated as an image-generation prompt. The response produced a visual artifact and omitted the required protocol banner.

### Correct classification
- `request_type`: `build_generation`
- prompt classes: `PYTHON_BUILD_GENERATION`, `FEATURE_INTENT_ROUTING`, `CONTROL_TO_VARIANT_DERIVATION`
- feature routes: `gothic_metal_castle_facade`, `radial_airlock_iris_door`

### Fix
Load `rules/NMS_BUILD_VS_IMAGE_ROUTING_GUARD.md` before build-generation turns. In active NMS Builder context, build-language defaults to NMS Builder Python unless the user explicitly asks for image/render/mockup/concept-art/visual-only output.

### Prevention
If the requested output artifact is ambiguous, ask one targeted clarification. If recent context says the user is testing build execution, default to executable NMS Builder Python.

## Snap/overlap fixes (promoted)

- ISSUE: nms_snap cycling arguments seem to select alternate snap points but are INERT in Blender 5.1
  (default snap only). FIX: do not rely on operator cycling; select named points from the authoritative map.
- ISSUE: snap "misfires" to a coincident overlap for some parts (e.g. B_TRIFLOOR). ROOT CAUSE: the part is
  not a member of the relevant snap group, so it has no snap points there. FIX: confirm group membership in
  snapping_info.json; use a member part or place manually.
- ISSUE: overlap/float detection false positives on rotated parts (axis-aligned bbox) or false negatives on
  coincident parts (surface-vertex test). FIX: use VOLUMETRIC INTERIOR SAMPLING. Validated metric.
