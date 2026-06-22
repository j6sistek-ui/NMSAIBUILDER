# Verified Part Map Data Protocol (3.01.02)

Status: active component-placement evidence rule.

## Purpose

This protocol tells generated builds and validation workflows how to use the verified Builder-spawn extraction overlay created from `NMS_FULL_PARTMAP_EXTRACTION_V01_PORTABLE_V02`.

## Core rule

Recipes still control assemblies. The verified part map controls component placement mechanics when a part is selected.

Evidence order for component mechanics:

```text
1. current-build/control JSON for exact transforms
2. validated recipe/signature/toolkit entry for assembly behavior
3. verified builder extraction overlay for ObjectID spawn/origin/rotation/scale/bbox behavior
4. original FBX-derived library extents and centers
5. raw FBX/manual/in-game confirmation only if unresolved
```

## Verified data scope

- Extraction input library rows completed: 2,092 / 2,092.
- Combined variant records: 20,920.
- Active source-library rows: 2,097.
- Active rows with extracted ObjectID data: 2,071.
- Active rows not present in extraction input: 26.
- Uploaded batch progress files reported 0 spawn failures.

## Interpretation cautions

- This verifies Blender/NMS Builder spawn measurement data, not every final in-game visual footprint.
- Decorative flora/coral/proxy-like objects may render or measure differently in Blender than in game; use bbox conflicts as diagnostic only unless placement visibly fails or in-game evidence confirms.
- Missing expected extents are not failures. They mean old library comparison data was absent.
- Zero-bbox and invisible parts require caution and should not be used unless specifically validated.

## Known exception policy

- `CUBEWALL_SPACE`: `DO_NOT_USE`; invisible/zero-bbox placeholder.
- `BASE_FLORAL03` / Spoonleaf: visual placement user-reviewed as OK; old library/variant extents conflict is diagnostic only.
- `TELEPORTER`: use with caution; spawned model extents differ from mapped expected extents.
- `FRE_FACE_WALL`, `FRE_ROOM_IND1`: zero-bbox review before use.
- `PIPE`, `BASE_BUBPIPE`, `BASE_BUBPIPE_S`, `BASE_BUBPIPE_L`, `BASE_BUBPIPE_T`, `BASE_BUBPIPE_X`: `GAME_VALIDATION_REQUIRED_PIPE_FAMILY`; Blender extraction/orientation data is raw evidence only and must not be treated as authoritative for connected pipe assemblies.

## Required build behavior

When a generated script uses a known ObjectID, `USED_PART_LOGIC` should cite the verified map status when available. If the status is not `VERIFIED_DATA_OK`, the script must either use the documented exception policy or mark the part as provisional/review-required.


## PIPE/BUBPIPE patch

User-confirmed in-game evidence overrides the prior 3.01.00 interpretation for pipe-family parts. The BUBPIPE rows had clean Blender extents, but the resulting in-game appearance/orientation differed from Blender. The default `PIPE` row can measure as zero-bbox/invisible in Blender while still being the valid in-game pipe object. Therefore pipe-family parts are not `VERIFIED_DATA_OK` for assembly use until a focused in-game/exported-JSON pipe validation confirms local/global rotation and connection continuity.


## PIPE/BUBPIPE contextual connector refinement

`PIPE` and `BASE_BUBPIPE*` are contextual connector parts. The verified map remains raw Blender extraction evidence, but connected-pipe behavior must be validated by exported JSON/in-game evidence or a focused pipe harness. Prefer `rules/PROHIBITED_AND_PLACEHOLDER_OBJECTS.md` over the older 3.01.01 validation-exception wording.
