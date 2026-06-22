# Release notes — NMS master docs 5.19.00

## The build sheet is now the single reconciled per-part record

Per your reset: the build sheet must hand over every placement-relevant fact for a selected ObjectID, reconciled from whatever files hold it, anchored on the verified part map (`nms_master_part_map_verified_data_v3` — the baseline we don't deviate from). `placement_spec` now carries, per part:

- **geometry** — origin offset, bounding box (world + local), bbox center, bottom/top Z, expected extents, FBX path — from the verified map
- **orientation** — default rotation, per-facing footprints (RX90/RY90/RZ90), master-CSV phase/pivot/origin, override flag
- **scale** — world size at 0.5/1.0/1.5/2.0, scale behavior
- **placement_rules** — concrete snap step, SpacingRule fallback, placement guidance, local axis (Right/Up/At) rules, neighbor offsets, fitment modes, recipe candidates
- **family / characteristics / method authority / role / cautions**
- **provenance + validation** — every section tagged with `_source`; an overall `validation` block reports the verified-map status (e.g. `VERIFIED_DATA_OK`) and the master-CSV placement-trial status (e.g. `UNTESTED`/`NEED_STUDY`), so the build knows which facts are solid and which are unfilled blanks awaiting a trial.

This ties in four sources that were never reconciled into the sheet: the verified part map's full geometry, the `part_placement_master_sheet.csv` 'everything sheet', the characteristics index, and the method-authority table. The one remaining gap is flagged in-record as `connections_TODO`: cross-plane composed transforms (roof-on-wall seating) are the next mapping pass, followed by build trials to fill and validate the master-CSV layer.
