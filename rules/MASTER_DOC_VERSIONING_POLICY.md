
# Master Document Versioning Policy 1.00.00

## Status

**Active required governance rule.**

This package adopts the new master-document release format:

```text
X.YY.ZZ
```

Example:

```text
1.00.00
```

Legacy `vNN` package names are now deprecated for master-document releases.

## Version format

| Field | Name | Meaning |
|---|---|---|
| `X` | Major | Groundbreaking / urgent cross-chat capability, safety, or process change |
| `YY` | Minor | General enhancement, project input, toolkit expansion, recipe/library addition |
| `ZZ` | Patch | Cleanup, typo/link/reference fix, validation report correction, packaging-only change |

`YY` and `ZZ` are always two digits.

## Increment rules

### Major: `X`

Increment `X` when the update is important enough that active chats should reload or be notified before continuing build generation.

Use a major release for:

- new fundamental generation workflow;
- new required validation loop;
- coordinate/transform breakthrough;
- universal safety rule that invalidates existing assumptions;
- ObjectID library/toolchain change that breaks or materially changes generation;
- prohibited-object or data-safety change that must be applied immediately;
- governance change that all active chats must follow.

When `X` increments:

```text
X += 1
YY = 00
ZZ = 00
```

### Minor: `YY`

Increment `YY` when the update improves capability but does not require urgent cross-chat interruption.

Use a minor release for:

- new project case study;
- new toolkit technique;
- new placement recipe;
- visual-reference expansion;
- project-specific learning that may help future work;
- additional part-use catalog entries;
- non-breaking tool or protocol enhancement.

When `YY` increments:

```text
YY += 1
ZZ = 00
```

### Patch: `ZZ`

Increment `ZZ` for cleanup or low-risk corrections that do not alter build-generation behavior.

Use a patch release for:

- typo fixes;
- stale link/path correction;
- README cleanup;
- changelog cleanup;
- manifest correction;
- report formatting;
- small validation-script mock fix when it does not alter generation rules;
- packaging-only changes.

When `ZZ` increments:

```text
ZZ += 1
```

## Better decision rule

The release level should be selected by **urgency + behavior impact**, not by file count.

Ask:

1. **Would another active chat produce bad or unsafe builds if it did not get this update now?**
   - Yes → Major.
2. **Does this add reusable capability, recipes, project learning, or toolkit knowledge but older chats can finish safely?**
   - Yes → Minor.
3. **Is this only cleanup, packaging, wording, report correction, or non-behavioral maintenance?**
   - Yes → Patch.

## Behavioral impact table

| Change type | Default release |
|---|---|
| New universal hard rule | Major if urgent/cross-chat critical; otherwise Minor |
| New validation gate requirement | Major |
| Validation gate bug fix | Patch if non-behavioral; Major if old gate lets unsafe builds pass |
| New part library from plugin update | Major if generation compatibility changes; otherwise Minor |
| New part-use catalog entries | Minor |
| New project case study | Minor |
| New visual toolkit entry | Minor |
| New JSON recipe library | Minor, unless it changes required generation workflow |
| Stale filename/link cleanup | Patch |
| Changelog/manifest cleanup | Patch |
| Current project script revision | Not a master-doc release unless docs also change |

## Communication rule

| Release | Cross-chat handling |
|---|---|
| Major | Immediately tell other active chats to reload/update sources before more script generation |
| Minor | Upload/update project sources before the next substantial work session |
| Patch | Can wait until convenient; not urgent to interrupt active chats |

## Current baseline

This release starts the new scheme at:

```text
1.00.00
```

It supersedes the legacy v60-style package numbering as the current master-source baseline.

## Legacy mapping

| Legacy label | New baseline meaning |
|---|---|
| v60 review patch package | pre-1.00.00 legacy state |
| 1.00.00 | first semantic master-doc release with explicit revision governance |

## Filename guidance

Preferred master package filename:

```text
NMS_master_docs_1.00.00_MASTER.zip
```

Patch example:

```text
NMS_master_docs_1.00.01_cleanup.zip
```

Minor example:

```text
NMS_master_docs_1.01.00_airlock_recipe_expansion.zip
```

Major example:

```text
NMS_master_docs_2.00.00_new_transform_or_validation_system.zip
```

---

## Release gate (definition of done) — added 1.01.00

A version number may not be blessed until the package is internally consistent.
This is the docs-package analogue of the build `run_gate.py`: prove it, don't
attest it. Run from the package root:

```text
python3 release/release_check.py
```

It must print `RELEASE GATE: PASS` before a release ships. It enforces:

1. **Single source of version truth** — `release/VERSION.json` `current_version`
   is canonical; `PACKAGE_MANIFEST.json` `version` must equal it; the
   self-identifying TITLE of `00_START_HERE_CURRENT.md` and `README.md` must
   carry the current version (no legacy `vNN`, no mismatched `X.YY.ZZ`). Lineage
   mentions in body prose are allowed.
2. **Library row count** in START_HERE matches the actual library JSON length.
3. **CHANGELOG + release notes** exist for the current version.
4. **All JSON parses.**
5. **No dangling internal references** in live docs (CHANGELOG/reports history
   and external paths excluded).
6. **`validation/run_gate.py` present.**

### Single source of version truth

`release/VERSION.json` is authoritative. Any other file that names the version
must match it, and `release_check.py` enforces that match. When bumping, edit
VERSION.json first, then run the gate; it will tell you every file still out of
sync.

### One canonical master

Exactly one `NMS_master_docs_X.YY.ZZ_MASTER.zip` is canonical at a time.
`VERSION.json.legacy_supersedes` names the package it replaces. Older zips are
historical; do not distribute more than one master.

### Every release requires, in the same change

- a `CHANGELOG.md` entry naming the new version,
- a `release/RELEASE_NOTES_<version>.md`,
- a `release/VERSION.json` bump,
- a `RELEASE GATE: PASS`.

---

## Cascade reset — ENFORCED by the release gate (added 1.01.01)

Rolling a higher field resets every lower field to `00`, and exactly one field
moves, by one:

| Step | From | To | Rule |
|---|---|---|---|
| Patch | `1.04.07` | `1.04.08` | `ZZ += 1` |
| Minor | `1.04.08` | `1.05.00` | `YY += 1`, **`ZZ -> 00`** |
| Major | `1.05.00` | `2.00.00` | `X += 1`, **`YY -> 00`, `ZZ -> 00`** |

You never carry lower digits across a higher roll. Rolling to major 2 is
`2.00.00`, never `2.10.57`. Rolling minor resets patch to `00`.

`release/release_check.py` enforces this mechanically against
`release/VERSION.json.supersedes_version` (the immediately-prior version). Any
of these **fail the gate**:

- `1.09.09 -> 2.10.57` (major did not reset YY/ZZ),
- `1.00.00 -> 1.02.00` (skipped a minor),
- `1.00.00 -> 1.00.03` (skipped a patch),
- any non-`X.YY.ZZ` string, or YY/ZZ not two digits.

When bumping: set `current_version` and `supersedes_version` in VERSION.json,
then run the gate; it will reject an illegal step before the package can ship.
