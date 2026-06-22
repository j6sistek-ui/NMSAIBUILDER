# Plugin Version and Environment v50

## Current documented environment

- **No Man's Sky Base Builder add-on:** `6.4.1`
- **Blender confirmed working for user:** `5.0.1`
- **Manifest minimum Blender version:** `4.2.0`
- **Blender 5.1.1 note:** may work only after confirming the FBX import/export add-on is enabled for NMS Builder internal part retrieval.
- **Source ZIP reviewed:** `No Man's Sky Base Builder-984-6-4-1-1779969861.zip`

## 6.4.1 update meaning

This update is primarily workflow/UI oriented, but it also exposes or adds new build parts.

Major notes:

- Built-in Save Manager / save import-export workflow added.
- Backup save workflow is now available inside Blender; use it before import/export.
- New Swarm update parts are available in the plugin object library.
- Duplicate Part button bug is noted as fixed by the add-on release notes.
- Generator rules are unchanged: use real plugin parts, preflight builder runtime, avoid non-uniform unsupported scaling, and validate new parts before relying on them.

## New ObjectIDs

See:

- `library/NMS_PLUGIN_641_ADDED_OBJECTIDS.csv`
- `library/NMS_PLUGIN_641_ADDED_OBJECTIDS.json`
- `MASTER_LESSONS_LEARNED.md` (removed historical reference: reports/NMS_PLUGIN_641_UPDATE_REPORT_v50.md)

## Critical prohibition

`HOLO_DISCO_0` is a Wonder Projector variant and is now prohibited for generated builds alongside `HOLO_DISCO`.

```text
HOLO_DISCO
HOLO_DISCO_0
```

Allowed exception: preserve an explicitly supplied, already configured user object.


## environment clarification

The user-confirmed working environment is Blender 5.0.1 with NMS Base Builder 6.4.1. Blender 5.1.1 may work if the FBX import/export add-on is enabled for the plugin's internal part retrieval. This does not authorize generated scripts to import FBX directly; generated build scripts must use real NMS Builder objects through `BUILDER.add_part()` and template-copy placement.
