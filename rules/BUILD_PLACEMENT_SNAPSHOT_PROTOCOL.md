# Build Placement Snapshot Protocol (4.01.00)

## Purpose

A generated build should not rely on broad latent memory. It should create a build-specific snapshot containing only the ObjectIDs, allowed methods, blocked ObjectIDs, and structural contexts needed for that build.

## Runtime knowledge lock

If an ObjectID is not present in the build snapshot, placement is blocked until the snapshot is updated. If a method is not present in the snapshot, placement is blocked until the method authority table authorizes it.

## Required file

`templates/BUILD_PLACEMENT_SNAPSHOT_TEMPLATE.json` using `schemas/BUILD_PLACEMENT_SNAPSHOT.schema.json`.

## Relationship to external validation

The future external validator will consume this file. 4.01.00 prepares the source-doc infrastructure but does not require a hosted validator.
