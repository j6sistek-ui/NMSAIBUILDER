# Rule Application Matrix

This matrix covers cross-cutting application tiers and a few specialized situations. Feature and context routing bundles are **not** duplicated here — they live in the authoritative bundle map in `rules/REQUEST_ROUTER_CHECKLIST.md`. Use the router for "which docs to load for this feature/request"; use this matrix for "which rule tiers apply at which phase" and for the specialized Corvette / JSON-recreation / continuity tables.

## Library vs rules application, by phase

| Phase | Broad library? | Used ObjectID-specific rules? | Universal rules? | Project rules? |
|---|---:|---:|---:|---:|
| Design brainstorming | YES | Optional if likely candidates known | YES | YES if active project |
| Part selection | YES | YES for selected candidates | YES | YES if active project |
| Script writing | Selected ObjectIDs only | YES | YES | YES if active project |
| Validation loop | NO, except verifying selected IDs exist | YES, only used ObjectIDs/families | YES | YES if modifying project |
| Documentation update | As needed | YES if new part behavior | YES if workflow rule | YES if project-only lesson |

Key distinction: use the full library to discover design potential; use the script's actual ObjectID set to validate placement and part-specific behavior.

## General situation table

| Situation | Files to apply | Action |
|---|---|---|
| ObjectID appears in generated script | `OBJECT_USE_RECORDING_PROTOCOL`, `PART_FAMILY_RULES`, `ISSUE_FIX_LIBRARY` | Record build role/use type and validate relevant part rules. |
| User provides creative screenshot/example | `SELECTIVE_VISUAL_MEMORY_POLICY`, `PART_USE_CASE_CATALOG`, `SELECTIVE_VISUAL_MEMORY_POLICY` | Extract lesson and log candidate use case. |
| User provides base JSON | `BUILD_DATA_MINING_PROTOCOL`, `NMS_BUILD_USE_CASE_MINER.py` | Mine ObjectIDs/patterns and propose use-case/rule updates. |
| Dome strategy changes | `DOME_STUDY_LESSONS` | Compare visual objective and part budget before replacing subsystems. |

## Exploration mode

| Situation | Required files/rules |
|---|---|
| User asks for experimental/unique/creative vague design | `rules/EXPERIMENTAL_REQUEST_PROTOCOL.md`, `rules/PART_USE_CASE_CATALOG.md`, `rules/SELECTIVE_VISUAL_MEMORY_POLICY.md` |
| User asks for deep-sea room skyscraper toppers | `rules/PART_FAMILY_RULES.md` -> `DEEP_SEA_ROOM_SKYSCRAPER_TOPPERS`, plus part library entries for `MAINROOM_WATER` and `MAINROOMCUBE_W` |
| User says a study is too conservative/repetitive | Run comfort-motif audit and regenerate with forced divergent silhouettes |
| User screenshots only selected variants | Treat unscreenshotted weak variants as removal candidates |

## Corvette scope and boundary

| Situation | Required files/rules |
|---|---|
| Corvette construction or module planning | `corvette/CORVETTE_KNOWLEDGE_REPOSITORY.md`, `corvette/CORVETTE_SCOPE_AND_BUILD_MECHANICS.md`, `corvette/CORVETTE_CORE_REQUIREMENTS.csv` |
| Script uses `Category == Corvette` ObjectIDs | Load `/corvette`, then validate used ObjectIDs/families against universal rules and FBX data |
| Corvette ObjectIDs cannot be instantiated through the plugin | Stop as diagnostic; do not create proxy geometry |
| Ordinary base/architecture build | Do not apply Corvette minimum categories or ship-role requirements |

Boundary audit (Corvette-mode only — must not leak into non-ship builds):

| Scenario | Apply 95m safe / 100m absolute boundary? | Notes |
|---|---:|---|
| Functional Corvette core modules | Yes | Audit all final Corvette placements; use rotated FBX occupied bounds; fail over 95m side length. |
| Functional Corvette with non-Corvette exterior/interior decoration | Yes | Decoration counts toward the ship footprint; interior placements still occupy the assembly. |
| Third-party/Blender Corvette blueprint conversion | Yes | Audit the whole final ship before import/recommendation. |
| Planetary base using a Corvette part decoratively | No | Not a Corvette-mode build; use universal rules only. |
| Megacity / Taj / Jurassic / ordinary architecture | No | Corvette boundary does not apply. |

## JSON recreation and study

| Situation | Required rule/protocol |
|---|---|
| User provides exported base JSON and asks for Python recreation | `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md` |
| Recreated base overlays but local details appear reversed | Check `POST_BASELINE_CORRECTION="LOCAL_Y_180"` |
| New ObjectIDs appear in future JSON | Run ObjectID audit and flag as unvalidated family |
| Existing build repair/enhancement requested | Recreate JSON as Python first, then modify the generated Python |
| Missing builder template/ObjectID | Report; do not substitute silently |
| User provides base JSON for learning | `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md` |
| User asks for a fresh generated build | `toolkit/PLACEMENT_RECIPE_LIBRARY.md` + `rules/SPACING_CONNECTION_SCALE_RULES.md` |
| Repeated stairs/ramps | endpoint-driven stair/ramp rules |
| Circular/iris/portal/ring feature | radius/chord/angle/depth-layer rules |
| Vehicle or small assembly | object-local coordinate frame rules |
| Powerlines/logic | preserve hub vectors; do not deduplicate |
| Jurassic Beach garage-door mouth | negative lesson; do not promote |

## Version continuity review

| Situation | Required action |
|---|---|
| User uploads a newer master/source package | Identify last used version and current version |
| User asks if changes are critical | Perform full continuity audit unless explicitly only patch sanity |
| User says minor changes were made elsewhere | Review all changes since last used version, not only the last patch |
| Before script generation after a new source upload | Read current rules and changelogs relevant to the task |
| Review scope is limited | State `Patch sanity review only` |
