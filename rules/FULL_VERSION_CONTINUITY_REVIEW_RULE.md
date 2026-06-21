# Full Version Continuity Review Rule v1.02.00

Updated: 2026-05-30  
Status: **mandatory governance rule**

## Purpose

When a new No Man's Sky master/source package is provided, the assistant or coding AI must not inspect only the latest patch note or last visible change. It must understand the cumulative changes since the last version actually used by the current chat.

This rule exists to prevent missed knowledge when other chats make intermediate updates.

## Core rule

```text
Any time a newer master/source package is provided, review all updates since the last version used by the current chat.
Do not review only the latest patch.
Do not skip intermediate versions.
Do not claim "no critical changes" unless the continuity path has been checked.
```

## Required inputs

Before making claims about the current master package, identify:

```text
last version used by this chat
new version provided by user
whether intermediate versions exist
where changelogs/manifests/version files live
whether the package includes archived change history
```

If the last version used by the chat is unknown, state that explicitly and use the latest known trusted baseline in the conversation.

## Required review levels

### 1. Patch sanity review

A patch sanity review is limited. It may check:

```text
latest VERSION metadata
latest release gate status
latest changelog entry
package integrity
obvious blocking errors
```

A patch sanity review is **not** enough to prove all knowledge has been retained.

When giving this type of review, state clearly:

```text
This is a patch sanity review only, not a full continuity audit.
```

### 2. Full continuity audit

A full continuity audit is required when the user asks whether the current package is safe to trust, whether previous lessons were retained, or before the assistant claims that no important knowledge has been lost.

It must review:

```text
last used version → current version
all changelog entries between those versions
VERSION / PACKAGE_MANIFEST / release metadata
new, removed, renamed, or migrated files
rule changes
toolkit/recipe changes
part-family changes
known negative lessons
transfer/bootstrap prompt changes
validation/gate changes
```

## Minimum audit checklist

A full continuity audit must verify:

- JSON→Python recreation rules are still present if previously active.
- JSON Study / Placement Recipe Library content is retained or intentionally migrated.
- Spacing / connection / scale rules are retained.
- Part-family rules and ObjectID notes are retained.
- Negative lessons are retained and not accidentally promoted.
- Generator contract still enforces real NMS parts and builder preflight.
- Transfer/bootstrap prompts include the current critical rules.
- Versioning and release metadata are internally consistent.
- Any new governance structure does not hide or silence active build rules.

## Required output language

When reviewing a new package, use one of these classifications:

```text
Patch sanity review only
Full continuity audit complete
Full continuity audit incomplete
Critical issue found
No critical issue found after continuity audit
```

Do not write vague confirmations such as "looks fine" unless the scope is declared.

## Required behavior before generation

Before generating scripts from a newly provided source package:

1. load the current package;
2. identify the last version used by this chat;
3. read the current bootstrap/start-here docs;
4. review changelogs since the last used version;
5. verify active rules relevant to the requested task;
6. only then generate.

## Memory and source-document principle

The master docs are the source of truth. Chat memory is supporting context only.

```text
If a rule exists in memory but not in the current master docs, flag the mismatch.
If a rule exists in current master docs but not memory, follow the master docs.
If both conflict, ask or perform a documented reconciliation.
```

## Revision classification

This rule is a minor governance/process enhancement over 1.01.01, not a build-generation geometry change.

Recommended version bump:

```text
1.01.01 → 1.02.00
```

Rationale: the rule affects how all future source updates are reviewed and understood, but it does not change part placement formulas or build geometry.
