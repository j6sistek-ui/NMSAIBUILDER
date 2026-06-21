# Corvette Knowledge Repository v48

Updated: `2026-05-28`

This repository is a **Corvette-only knowledge layer** inside the NMS master docs. It exists because Corvette building uses many of the same low-level mechanics as other NMS Builder work — ObjectIDs, FBX bounds, plugin-created parts, runtime audits, and no raw Blender mesh primitives — but the **end goal, minimum validation requirements, part families, and in-game workflow are different**.

## Scope boundary

Use this file when the user asks for:

- Corvette construction;
- Corvette Workshop module planning;
- Corvette ObjectID lookup;
- Corvette-specific Blender/NMS plugin scripting;
- Corvette role/loadout decisions;
- Corvette part debugging.

Do **not** carry Corvette-only rules into ordinary planetary bases, freighter bases, landmark recreations, skyscrapers, ruins, organic scenes, or decorative builds unless the build explicitly uses Corvette parts.

Corvette rules that should **not** leak globally:

- seven-category minimum-valid-ship requirements;
- cockpit/access/hab/reactor/engine/weapon/landing-gear validation;
- ship role optimization such as explorer/combat/daily-driver packages;
- Corvette Workshop cache behavior;
- Corvette module bonus/stat assumptions;
- single-deck/low-profile reliability heuristics, unless the prompt is ship-like.

Universal rules that still apply:

- real NMS/plugin objects only;
- full library for part selection, not short whitelists;
- no raw Blender primitive build geometry;
- builder preflight before deletion/cleanup;
- FBX-derived dimensions and origin/bounds placement;
- runtime object audit;
- object-use manifest and ObjectID transparency.

## Current Corvette library inventory

The full v42/v43 object library contains `604` entries with `Category == Corvette`.

| Corvette subcategory | Count |
|---|---:|
| Access and Docking | 8 |
| Cockpits and Habitation Modules | 9 |
| Defensive Systems | 10 |
| Exterior Decoration | 21 |
| Hull Connectors | 23 |
| Hull Plating | 456 |
| Internal Configuration | 1 |
| Reactors | 4 |
| Storage | 10 |
| Thrusters | 8 |
| Utility Modules | 7 |
| Windows | 3 |
| Wings | 44 |

The complete extracted CSV is `corvette/CORVETTE_OBJECTID_CATALOG.csv`.

## v48 Corvette boundary limit — strict whole-assembly rule

The 2026-05-28 user-supplied community warning for the Swarm-era update reports that Corvette building boundaries now limit usable ship scale to around **100m** / a little under **330 ft**. This exact value has not been independently confirmed in the reviewed official patch notes, but it is now a **strict conservative operating rule** for this repository.

Use `corvette/CORVETTE_BOUNDARY_LIMITS.md/json` for the full rule.

Mandatory generator limit:

```text
CORVETTE_ABSOLUTE_BOUNDARY_SIDE_M = 100.0
CORVETTE_SAFE_BOUNDARY_SIDE_M     = 95.0
CORVETTE_SAFE_HALF_EXTENT_M       = 47.5
```

Corvette scripts must check **occupied rotated bounds**, not just object centers:

```python
abs(part_center_axis - corvette_origin_axis) + rotated_half_extent_axis <= 47.5
```

If a Corvette layout exceeds the 95m safe envelope in X, Y, or Z, do not deliver it as a usable in-game Corvette. Shrink, redesign, or reject it.

This boundary rule is **Corvette-mode only**, but in Corvette mode it applies to the **entire finished assembly**, including non-Corvette/base/decorative parts mounted on or placed inside the Corvette. Do not filter the boundary audit to `Category == Corvette`.

The boundary rule must not leak into ordinary bases, freighter bases, megacities, Taj/Jurassic/organic builds, or decorative non-Corvette builds that merely use Corvette ObjectIDs as greebles.


## v48 whole-assembly clarification

Because Corvettes can be decorated with non-Corvette parts, the boundary audit is based on **ship membership**, not library category.

When the output is a Corvette, include all final exported placements in the 95m/100m boundary calculation:

- Corvette modules and hull parts;
- non-Corvette base/decorative parts attached to the exterior;
- non-Corvette furniture, utility props, lights, signs, decals, pipes, plants, and greebles placed inside or on the Corvette.

Exclude only temporary templates, deleted scaffolds, and debug/reference objects that are not part of the final Corvette export.

## Minimum valid Corvette baseline

The current baseline core set is the Aegis/Explorer daily-driver package. It covers the seven minimum categories required by the Corvette study and is stored in `corvette/CORVETTE_CORE_REQUIREMENTS.csv`.

| Required category | ObjectID | NiceName | Library subcategory | FBX extents X × Y × Z |
|---|---|---|---|---:|
| cockpit | `B_COK_B` | AMBASSADOR-CLASS COCKPIT | Cockpits and Habitation Modules | 6.324219 × 4.624023 × 5.790321 |
| access_module | `B_ALK_B` | AMBASSADOR-CLASS LANDING BAY | Access and Docking | 5.929688 × 2.998047 × 3.697327 |
| habitation | `B_HAB_C` | AMBASSADOR-CLASS HAB | Cockpits and Habitation Modules | 5.847656 × 2.956696 × 11.820312 |
| reactor | `B_GEN_0` | ZENITH-CLASS REACTOR | Reactors | 6.0 × 3.766022 × 6.0 |
| main_engine | `B_TRU_C` | KINEOSTREAM THRUSTER | Thrusters | 6.859375 × 6.859375 × 4.856274 |
| weapon_system | `B_TUR_A` | PHOTON CANNON ARRAY | Defensive Systems | 3.378906 × 2.175049 × 4.15625 |
| landing_gear | `B_LND_B` | MAG-FIELD LANDING THRUSTERS | Access and Docking | 5.054688 × 2.299438 × 6.019531 |

## Initial lessons learned from Corvette scripting attempts

### 1. ObjectID + dimensions are not enough

The library can prove that `B_COK_B` or `B_GEN_0` exists and provide dimensions, but a script has not created an NMS/plugin object until it uses a valid plugin creation path or duplicates a verified plugin-created source object.

**Rule:** never deliver a Corvette script that silently falls back to cube proxies or dimension placeholders.

### 2. Proxy preview is not a safe fallback

The failed Aegis prototype generated blocky proxy meshes. This looked like a layout but was not a valid NMS/Corvette build.

**Rule:** if Corvette object instantiation fails, the script must stop before creating visible fake geometry.

### 3. Template copying must be source-strict

A template-copy workflow can fail if it accidentally copies old generated blocks. Scene scanning is unsafe unless the source collection is verified.

**Rule:** copy only plugin-created templates that pass ObjectID/custom-property audit; never copy prior proxy geometry.

### 4. ObjectID must be searchable in Blender

Cute names are secondary. Debugging requires the user to find `B_COK_B`, `B_ALK_B`, etc.

**Rule:** Corvette object names and descriptions should include:

```text
<ObjectID> | <NiceName> | <required category if any> | <role>
```

### 5. Corvette Workshop exposure is a separate unknown

The full library contains Corvette ObjectIDs, but the current Blender/NMS Builder plugin context may not expose Corvette Workshop modules through the same `BUILDER.add_part(ObjectID)` path used for ordinary base parts.

**Rule:** before generating a Corvette script, run a Corvette-specific add-part probe for the required ObjectIDs. If the probe fails, document the plugin/API limitation instead of making fake geometry.


### 6. Corvette boundary is now part of script validation

After the Swarm-era update/community warning, oversized Corvette blueprints from Blender, save editors, or third-party tools may be clipped, cut up, or invalid in-game.

**Rule:** every Corvette generator must run a 95m safe-boundary audit using rotated FBX extents before delivery. The 100m reported boundary is an absolute redline, not a target. The audit must include the whole final Corvette assembly: required Corvette modules plus any non-Corvette exterior/interior decoration that remains part of the ship.

## Recommended Corvette workflow

1. Read the universal master docs.
2. Read this Corvette repository.
3. Filter the full library for `Category == Corvette` when the prompt is Corvette-specific.
4. Select the seven required categories before any decorative hull work.
5. Run a Corvette add-part probe in the user’s initialized Blender/NMS Builder scene.
6. Run the v48 Corvette whole-assembly boundary audit and keep the final occupied rotated bounds within the 95m safe envelope.
7. Generate only real plugin objects or fail cleanly.
8. Put ObjectID in object name, description, and custom metadata.
9. Keep Corvette lessons in this repository unless they are universal plugin/validation failures.

## Research state

Current status: **initial repository baseline, not screenshot-validated as an in-game Corvette build**.

Known facts captured here come from:

- the user-provided Corvette building study;
- the extracted full ObjectID library;
- official Hello Games pages/patch notes reviewed during repository creation;
- the Aegis Corvette scripting/debugging failures in this conversation.

Patch-sensitive behavior such as module stats, cache behavior, and bug status should be treated as current-research material and rechecked before becoming hard permanent rules.

## v44 decorative-use scope note

This repository governs Corvette builds and Corvette-specific module logic. It does not prohibit using Corvette ObjectIDs as decorative or architectural parts in ordinary NMS base builds.

Decorative/non-Corvette use should be recorded in the Object Use Manifest and validated with universal part rules, not Corvette completeness checks.
