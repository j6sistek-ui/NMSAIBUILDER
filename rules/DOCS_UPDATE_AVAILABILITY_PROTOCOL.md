# Docs Update Availability Protocol — 2.13.01

## Status

**Mandatory for all substantive NMS protocol banners.**

## Purpose

The protocol banner must tell the user whether there are **known, actionable source-document updates that have not yet been incorporated** into the active master-doc package.

This prevents a chat from temporarily learning a correction while failing to roll it into the source package.

## Banner field

```text
Docs Avail for Update?: <Yes|No> (<count>)
```

## Exact meaning

```text
No (0)
```

There are no known pending source-document updates from the current conversation or transfer package.

```text
Yes (N)
```

There are `N` distinct learned/corrected items that should be added to the master docs and have **not yet** been incorporated.

## What counts as a Docs Avail item

Count a pending source-doc update only when the user, source JSON, validation result, screenshot review, or protocol failure reveals a confirmed reusable item such as:

```text
- confirmed doctrine
- confirmed algorithm
- confirmed schema field
- confirmed protocol clarification
- confirmed lessons learned
- confirmed validation-gate requirement
- confirmed rule/template/banner format change
- confirmed source-doc packaging or release-hygiene requirement
```

## What does not count

Do not count the following as Docs Avail items:

```text
- open validation work
- unresolved decisions
- pending user review
- future possibilities
- status changes not yet known
- classification not yet known
- one-off user preference with no future NMS relevance
- temporary debugging status after the issue is fully resolved and documented
- plain restatement of an already documented rule
```

Examples of invalid Docs Avail items:

```text
- "V38 has not been reviewed yet"
- "TRIFLOOR classifications are not known yet"
- "semantic float gate is still being discussed"
- "future validation work remains"
```

Those belong in an Open Topics Log, not in `Docs Avail for Update?`, unless they become confirmed source-doc changes.

## Relationship to Open Topics Log

`Docs Avail for Update?` and the Open Topics Log are different.

```text
Docs Avail for Update? = confirmed source-doc updates not yet incorporated.
Open Topics Log = unresolved work, pending validation, decisions, risks, and next actions.
```

A response may correctly say:

```text
Docs Avail for Update?: No (0)
```

while still listing open validation topics in an Open Topics Log.

## Required behavior

If the banner says `Yes (N)`, the response should briefly name the pending update items unless the user has asked for a very short answer.

If the user asks to update the master docs, incorporate all confirmed Docs Avail items. After a successful source-doc package update and release check, the banner should normally end:

```text
PROTOCOL ✓ — type: source_doc_update | source docs rev: <new_version> | gate: release_check PASS | ambiguity: none | Docs Avail for Update?: No (0)
```

## clarification

This release incorporates the transfer-package clarification that Docs Avail means:

```text
Known, actionable source-document updates that have not yet been incorporated.
```

It does not mean:

```text
open validation work
unresolved decisions
pending user review
future possibilities
status changes not yet known
```
