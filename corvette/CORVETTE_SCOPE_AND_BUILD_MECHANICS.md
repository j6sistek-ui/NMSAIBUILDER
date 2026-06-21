# Corvette Scope and Build Mechanics v48

Updated: `2026-05-28`

## Purpose

This file defines how Corvette knowledge interacts with the universal NMS build guidelines.

Corvette construction is not ordinary base architecture. It uses the same discipline around real ObjectIDs, plugin-created objects, dimensions, preflight, and audit, but it has a different destination: a valid, habitable, flyable ship assembled through Corvette-specific modules/workflow.

## Scope firewall

When a prompt is Corvette-specific, apply:

- `corvette/CORVETTE_KNOWLEDGE_REPOSITORY.md/json`;
- `corvette/CORVETTE_CORE_REQUIREMENTS.csv`;
- `corvette/CORVETTE_OBJECTID_CATALOG.csv`;
- universal generator rules;
- relevant part-specific FBX dimensions.

When a prompt is not Corvette-specific, do not apply:

- Corvette minimum category requirements;
- Corvette role/loadout logic;
- Corvette Workshop cache assumptions;
- Corvette single-deck reliability heuristics;
- Corvette module-stat assumptions.

## Same mechanics, different goal

Shared mechanics with other NMS build scripting:

- full ObjectID library inspection;
- real plugin object creation;
- no raw Blender mesh build parts;
- FBX bounds for size and placement;
- object-use manifest;
- runtime object audit.

Different Corvette-specific goals:

- meet the seven required categories first;
- preserve ship/module intent, not just visual architecture;
- keep role specialization visible in the part plan;
- validate plugin support for Corvette ObjectIDs before build generation;
- document ObjectID and required category in Blender for searchability.

## Baseline required categories

A minimum practical Corvette baseline must cover:

1. cockpit;
2. access module / landing bay;
3. habitation module;
4. reactor;
5. main engine / thruster;
6. weapon system;
7. landing gear.

See `CORVETTE_CORE_REQUIREMENTS.csv` for the current ObjectID baseline.

## v44 decorative Corvette-part use

Using a Corvette ObjectID decoratively in a normal base build **does not activate Corvette build validation by itself**.

Corvette build mode is activated by intent, not merely by ObjectID presence:

- user asks for a Corvette / ship / flyable vessel / Corvette module / Corvette Workshop output;
- the script claims to generate a valid Corvette;
- the object-use manifest assigns Corvette functional roles such as cockpit, reactor, landing gear, thruster, weapon, habitation, or access module.

If a Corvette ObjectID is used as a decorative, structural, architectural, furniture, display, greeble, lighting, trim, or kitbash element in a non-Corvette build:

- apply universal generator rules;
- validate that ObjectID's FBX dimensions, origin, orientation, and placement rules;
- record `use_type = decorative_non_corvette` or equivalent in the Object Use Manifest;
- do **not** require seven Corvette core categories;
- do **not** apply Corvette loadout/module completeness requirements;
- do **not** fail the script for not being a valid Corvette.

This prevents a false-positive failure mode where creative use of Corvette parts is incorrectly treated as a failed ship build.


## v47 boundary mechanics

Corvette work now has a strict build-envelope validation step. The current conservative rule is:

```text
safe Corvette side length <= 95m
absolute reported boundary ~= 100m
```

This is checked against the **occupied rotated bounding box** of the final layout, including FBX extents and scale. A center-only check is invalid.

This rule belongs only to Corvette-mode work and Corvette blueprint conversions. Within Corvette mode, it applies to the entire final assembly regardless of ObjectID category, including non-Corvette decorations placed on or in the ship. Do not carry it into ordinary base-building or architectural work.


## v48 category-agnostic Corvette assembly footprint

The Corvette boundary audit is triggered by the build's **Corvette intent**, not by each part's library category.

If the target is a Corvette, every final exported placement counts toward the 95m safe / 100m absolute footprint:

- Corvette modules;
- Corvette decorative/hull parts;
- non-Corvette base parts used as exterior decoration;
- non-Corvette furnishings, utility props, lights, decals, pipes, plants, and greebles used inside or on the ship.

Do not filter the boundary audit to `Category == Corvette`. That would miss decoration that can still push the functional Corvette outside the in-game boundary.
