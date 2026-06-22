# PROJECT TRANSFER SUMMARY RULE

## Status

Active continuity rule for major NMS package, tool, audit, and build deliverables.

## Purpose

Chat context limits can freeze active project state without warning. A Project Transfer Summary preserves current decisions, open issues, and next actions so a new chat can resume work with minimal reconstruction.

This is continuity insurance, not source authority.

## When Required

Every major deliverable should include a Project Transfer Summary.

Examples:

- source package updates
- audit reports
- governance reviews
- plugin revisions
- resolver updates
- build packet changes
- major architecture proposals
- major triage-tool revisions
- major build review reports

When the user says:

```text
checkpoint
```

generate current transfer artifacts.

## Required Sections

A Project Transfer Summary shall include:

1. Current Focus
2. Current Package / Tool Versions
3. Decisions Made
4. Active Open Issues
5. Recently Resolved Issues
6. Assumptions
7. Files / Artifacts Created
8. Next Recommended Actions
9. Deferred Topics
10. Items Not To Revisit Unless New Evidence Appears

## Checkpoint Artifacts

A checkpoint refreshes the two living continuity artifacts:

- `OPEN_TOPICS_LOG.md` (the authoritative open-topics state)
- `transfer_prompts/CHAT_TRANSFER_CURRENT.md` (the copy-paste resume block)

All major deliverables must include a Project Transfer Summary (absorbed from the retired PROJECT_TRANSFER_REQUIREMENT.md).

These files are not authoritative source documents. They are project-continuity artifacts intended for transfer into a new chat.

## Output Contract For Assistants

When producing a major file, source package patch, audit report, plugin update, or governance proposal, include a short transfer summary in the final response or generated artifact package.

The summary may be concise, but it must preserve enough state for a future chat to continue without re-litigating already-decided items.

## Copy-paste chat transfer doc (mandatory companion)

Every build or document update, and every `checkpoint`, must also produce a refreshed `transfer_prompts/CHAT_TRANSFER_CURRENT.md`: a self-contained block the user can paste into a new chat to resume with full critical context (who/what, current version, what happened, why, what was decided, what to do next, critical mechanics, standing requirements). It pairs with the authoritative `OPEN_TOPICS_LOG.md`.
