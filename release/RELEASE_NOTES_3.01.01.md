# Release Notes — 3.01.01

Patch release over 3.01.00.

## Purpose

Adds user-confirmed exception handling for `PIPE` and `BASE_BUBPIPE*` after in-game evidence showed that Blender extraction/visual orientation is not authoritative for connected pipe assemblies.

## Operational effect

- Do not treat `PIPE` / BUBPIPE family as verified for connected assembly from Blender extraction alone.
- Require in-game screenshot, exported JSON, or focused pipe validation harness before using pipe runs as accepted build logic.
- RX90 may correct individual parts, but does not validate bend continuity.

## Gate

Release gate report: `reports/3.01.01_FINAL_RELEASE_GATE_REPORT.txt`.
