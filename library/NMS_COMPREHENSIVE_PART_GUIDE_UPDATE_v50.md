# NMS Comprehensive Part Guide Update v50

## Source

- Prior master library baseline: v49
- New plugin source: No Man's Sky Base Builder 6.4.1
- User Blender environment: 5.0.1 confirmed working; 5.1.1 requires FBX importer/add-on checks

## Updated counts

| Metric | Count |
|---|---:|
| Plugin unique ObjectIDs | 2097 |
| Plugin FBX files | 2104 |
| New ObjectIDs vs v49 | 26 |
| Removed ObjectIDs vs v49 | 0 |
| Master library rows after regeneration from plugin definitions | 2097 |
| Master unique ObjectIDs after regeneration | 2097 |
| FBX bounds rows after adding new FBX models | 2104 |

## New ObjectIDs

See `library/NMS_PLUGIN_641_ADDED_OBJECTIDS.csv`.

## Critical policy update

`HOLO_DISCO_0` is prohibited for generated builds as a Wonder Projector variant.

## Notes

The library CSV/JSON was regenerated from the 6.4.1 `DT_PartDefinition.csv`, while preserving manual rule columns from the v49 library where ObjectIDs already existed.
