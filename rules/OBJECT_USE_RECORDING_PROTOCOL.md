# Object Use Recording Protocol

**Status:** universal script-generation rule.

Every generated build/script should record how each ObjectID is used in that build. This is separate from part-family validation. It is a build-specific object-use manifest.

## Required manifest

Every substantial script should include a comment block or printed section named:

```text
BUILD OBJECT USE MANIFEST
```

For each ObjectID used, record:

```text
ObjectID
count_estimate_or_role_count
literal_part_name_if_known
build_role
use_type: literal / transformed / hidden / structural / decorative / experimental
scale_range
orientation_notes
placement_rule_sources_checked
creative_catalog_sources_used
known_risks
```

## Purpose

- make the build intelligible to future AI sessions
- reduce accidental repeated mistakes
- preserve creative use cases as they are applied
- make part-count review easier
- separate "this part is present" from "why this part is present"

## When to promote to catalog

If the build uses an ObjectID in a creative or nonliteral way and the result is visually successful or user-approved, promote that entry to `PART_USE_CASE_CATALOG.md/json`.

## Failure mode addressed

The AI was generating builds using objects without documenting the purpose of those objects. That prevented later recall and caused repeated comfortable/repetitive features.

## v44 Corvette decorative use-type

If a Corvette ObjectID is used outside a Corvette build, the Object Use Manifest must label it clearly, for example:

```text
ObjectID: <Corvette part>
Use type: decorative_non_corvette / architectural_kitbash / greeble / display / lighting / trim / furniture
Corvette functional role: none
Corvette required-category validation: not applicable
```

This preserves creative use without causing false Corvette validation failures.

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
