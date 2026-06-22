# Build Compliance Manifest Rule  (introduced 5.00.00)

## Status

**MANDATORY.** Every real build — any user-requested design or structure, whether
emitted as a Python script or constructed in a live Blender session — must
produce a `BUILD COMPLIANCE MANIFEST` and pass
`validation/compliance_manifest_check.py`. A build delivered without a verified
manifest is invalid and must be rejected, by the AI and by the user.

## What the manifest contains
Schema: `schemas/BUILD_COMPLIANCE_MANIFEST.schema.json`;
template: `templates/BUILD_COMPLIANCE_MANIFEST_TEMPLATE.json`.

```text
build_name           : what was built
build_surface        : "python" | "blender"   (parity rule: same bar for both)
object_ids           : every unique ObjectID used (with ^ prefix)
precedence_resolutions: one per ObjectID -> {objectid, governing_tier, source_file, source_ref, method}
sources_checked      : the source files actually opened for placement data (receipts)
compliance_statement : an explicit statement that the documents were followed and no deviation occurred
```

## Receipts, not attestation
The manifest is checked, not trusted. `compliance_manifest_check.py` re-reads the
cited sources and confirms each ObjectID's resolution is real:
- every ObjectID has exactly one precedence resolution,
- the governing tier is 1–7 and the cited `source_file` exists,
- any ObjectID on `data/NEGATIVE_KNOWLEDGE_INDEX.json` with `DO_NOT_USE` is not
  used unless the resolution declares the required exception method,
- the compliance statement is present and affirms no deviation.

Missing, empty, or fabricated receipts FAIL. The build does not ship on a FAIL.

## The discipline this enforces
"Check the data before building" stops being a thing to remember. The deliverable
is structurally invalid without the verified receipt, so checking the data is the
only path that produces a passing build.
