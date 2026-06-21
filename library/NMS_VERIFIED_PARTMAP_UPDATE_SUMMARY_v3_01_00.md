# NMS Verified Part Map Update Summary v01

Source docs revision: 3.00.00  
Extraction run: NMS_FULL_PARTMAP_EXTRACTION_V01_PORTABLE_V02

## Coverage

- Extraction input library rows completed: 2092 / 2092
- Combined variant records: 20920
- Active 3.00 source-library rows: 2097
- Active rows with extracted ObjectID data: 2071
- Active rows not present in the extraction input library: 26
- Spawn failures in uploaded progress files: 0

## Important interpretation

This update verifies the measured Blender/NMS Builder spawn data for every ObjectID in the extraction input library. It does not guarantee every in-game visual footprint is perfectly represented by Blender geometry. Decorative proxy/plant/coral-style parts are flagged as diagnostic-only for bbox/visual-footprint conflicts.

## Key exceptions

- CUBEWALL_SPACE: DO_NOT_USE / invisible / zero-bbox.
- BASE_FLORAL03 / SPOONLEAF: decorative proxy or variant mismatch suspect; visual placement was user-reviewed as OK.
- TELEPORTER: extent mismatch review.
- Several special/freighter/pipe/internal objects show zero-bbox or missing expected extents and are flagged for caution.

## Status counts

- VERIFIED_DATA_OK: 2049
- DECOR_PROXY_OR_VARIANT_REVIEW: 1
- VERIFIED_DATA_NO_EXPECTED_EXTENT: 16
- DO_NOT_USE: 1
- NOT_EXTRACTED_FROM_INPUT_LIBRARY: 26
- REVIEW_ZERO_BBOX: 3
- REVIEW_EXTENT_MISMATCH: 1

## Recommendation

Use `nms_master_part_map_verified_data_v3_01_01.json` as the machine-readable master placement map overlay. Use the CSV/XLSX for human audit and review.
