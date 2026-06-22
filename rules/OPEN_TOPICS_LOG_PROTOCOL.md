# Open Topics Log Protocol — 2.13.01

## Status

**Mandatory for every downloadable artifact generated after 2.13.01.**

## Purpose

Prevent unresolved work from being lost across chats.

Downloadable outputs often travel without the surrounding conversation. Therefore every generated package, report, script, matrix, or release artifact must include a companion Open Topics Log that preserves unresolved validation items, pending decisions, risks, and recommended next actions.

## Trigger

Generate a companion Open Topics Log whenever producing any downloadable artifact, including:

```text
- Python validation script
- ZIP package
- generated file
- validation report
- part-family matrix
- source-doc release package
- run-gate or release-gate report
```

## File naming

Use a visible companion filename:

```text
<artifact_stem>_OPEN_TOPICS.md
```

For release packages:

```text
reports/<VERSION>_OPEN_TOPICS_LOG.md
```

## Required sections

Each Open Topics Log must include:

```text
1. Artifact / package name
2. Source docs revision used
3. Open validation items
4. Pending user decisions
5. Known unresolved questions
6. Deferred source-doc updates, if any
7. Known risks/exceptions
8. Recommended next actions
9. Docs Avail for Update? status
```

## Important distinction

Open topics are not automatically Docs Avail items.

```text
Open validation item -> Open Topics Log
Confirmed reusable source-doc change not yet incorporated -> Docs Avail for Update?
```

If an open topic later becomes confirmed doctrine, algorithm, schema, protocol, or lesson learned, then it becomes a Docs Avail item until incorporated into the source docs.

## Artifact-response requirement

When a downloadable artifact is provided to the user, the response must link both:

```text
- the primary artifact
- the companion Open Topics Log
```

For ZIP releases, the Open Topics Log should also be included inside the ZIP.

## source-doc release note

This protocol was added because prior stair-validation and protocol-correction work showed that unresolved items can be confused with pending source-doc updates. The log preserves unresolved work without inflating `Docs Avail for Update?`.

## Single authoritative continuity artifact

There is exactly one open-topics log: root `OPEN_TOPICS_LOG.md`. It is the file a new chat reads to answer, for every open item: **What happened? Why? What was decided? What do we do next?** Resolved history belongs in `CHANGELOG.md`, not here.

## Required structure per topic (mandatory)

Every open item is one `## TOPIC:` block containing all of these labelled fields:

```text
Issue
Discovery
Why It Matters
Decision
Next Steps
Status
Priority
Success Criteria
Last Updated
```

A topic missing any field is a structural failure (`validation/open_topics_structure_check.py` enforces this in the release gate).

## When it must be refreshed

`OPEN_TOPICS_LOG.md` must be updated, and a copy-paste chat transfer doc (`transfer_prompts/CHAT_TRANSFER_CURRENT.md`) provided, on **every build or document update, and whenever the user says `checkpoint`**. Both are continuity insurance against chat-limit/context-loss; they are not optional.
