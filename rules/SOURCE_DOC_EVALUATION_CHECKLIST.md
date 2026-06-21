# Source-Doc Evaluation Checklist — 2.13.01

## Status

**Mandatory for source-doc review, source-doc update, protocol correction, and transfer-package evaluation.**

## Purpose

Prevent a chat from evaluating only the user-provided transfer summary while missing active source-doc rules already present in the package.

This checklist was added after a 2.13.00 evaluation failure where the assistant missed the active banner format, Docs Avail definition, semantic-float status, raw float-gate preservation, and test-scope distinction.

## When to run

Run this checklist before answering any request classified as:

```text
source_doc_review_or_patch
protocol_correction_or_failure
```

Also run it when the user says:

```text
review the transfer package
update the source docs
evaluate the master docs
why did you miss this
protocol banner is wrong
```

## Required checks

Before finalizing, verify:

```text
1. Active baseline
   - Read release/VERSION.json.
   - Treat its numeric current_version as the active source docs revision.

2. Bootstrap
   - Read 00_START_HERE_CURRENT.md.
   - Apply READ ORDER and authority order.

3. Request routing
   - Classify with REQUEST_ROUTER_CHECKLIST.
   - Load the matching source-doc or protocol-correction bundle.

4. Banner format
   - Use the current numeric source-rev banner:
     PROTOCOL ✓ — type: <request_type> | source docs rev: <X.YY.ZZ> | gate: <verdict> | ambiguity: <none|clarification requested> | Docs Avail for Update?: <Yes|No> (<count>)
   - Do not use obsolete `bundle:` banner text.

5. Docs Avail definition
   - Count only confirmed source-doc updates not yet incorporated.
   - Do not count open validation work, pending review, unknown classifications, or future possibilities.

6. Open Topics
   - If an artifact is generated, create an Open Topics Log.
   - Put unresolved work in the log, not in Docs Avail unless it is a confirmed source-doc patch.

7. Validation-gate scope
   - State whether a gate covers a full regression, a partial matrix, a stadium-only test, switchback-only test, or a generated-file-only check.
   - Never promote a partial PASS as a family PASS.

8. Raw gate verdict preservation
   - Report PASS/FAIL exactly as run.
   - Temporary continuation approval may be separate, but must not rename FAIL to PASS.

9. Proposed vs adopted rules
   - Distinguish documented proposals from adopted gate behavior.
   - Semantic float gate remains proposed unless the active docs explicitly say adopted.

10. Storage and release hygiene
   - For source-doc patching, update VERSION, CHANGELOG, README/START, FILE_INVENTORY, PACKAGE_MANIFEST, release notes, and any affected rule/router files.
   - Run release_check.py before claiming PASS.
```

## Failure trigger

If any of the above checks were skipped and the user catches the miss, stop normal work and run `rules/SYSTEMATIC_FAILURE_CAPA_PROTOCOL.md`.

## lesson learned

The source docs, not the transfer summary alone, determine active protocol. A transfer package may identify pending work, but it must be reconciled against the active baseline before responding.
