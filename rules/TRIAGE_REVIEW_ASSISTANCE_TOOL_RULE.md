# TRIAGE REVIEW ASSISTANCE TOOL RULE

## Status

Active governance rule for Blender/NMS triage tooling.

## Purpose

The Blender triage tool is a **review assistance tool**. Its purpose is to identify candidate review areas, improve AI-human communication, and provide consistent repeatable observations during build review.

Triage is useful for narrowing human review areas, generating object-selection helpers, and prioritizing likely discontinuities, gaps, visibility concerns, and assembly-quality concerns.

## Non-Authority Statement

Triage findings are **review leads**, not confirmed failures.

A triage observation does not prove the build is wrong.

A missing triage observation does not prove the build is clean.

Triage output shall not be treated as:

- placement authority
- source-document authority
- conformance authority
- compliance authority
- CAPA trigger
- run_gate replacement
- build packet replacement
- in-game visual evidence replacement
- Blender visual evidence replacement

## Authority Order

Triage output is subordinate to all of the following:

1. `validation/run_gate.py` and any required gate output
2. exported JSON conformance and build-script conformance
3. `data/PLACEMENT_PRECEDENCE.json`
4. `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md`
5. generated `PROJECT_BUILD_PLACEMENT_PACKET`
6. source-document authority and package rules
7. in-game visual evidence
8. Blender visual evidence and human inspection

If triage conflicts with higher authority, the higher authority controls.

## Correct Interpretation

Use triage to ask:

```text
Where should review attention go next?
```

Do not use triage to conclude:

```text
The build is valid.
The build is invalid.
The build requires CAPA.
The placement method is authorized.
The placement method is unauthorized.
```

## Human Review Loop

Triage findings should follow this workflow:

```text
Observation
↓
Evidence
↓
Question
↓
Human Decision
```

Allowed human-review outcomes:

- `OK`
- `FIX`
- `INTENTIONAL`
- `NEEDS_CONTEXT`

If a flagged condition is intentional and should not be repeatedly raised, the object may be renamed in Blender to include:

```text
!!!!SKIP
```

The triage tool may suppress ordinary review observations for objects containing that marker. The marker must not be used to hide unknown ObjectIDs, corrupted transforms, or severe build-integrity problems.

## Preferred Language

Use:

- observation
- review candidate
- candidate discontinuity
- candidate visibility issue
- candidate continuity break
- review recommended

Avoid unless independently confirmed by authoritative review:

- failure
- violation
- noncompliant
- CAPA required

## CAPA Relationship

Triage output alone shall not initiate CAPA.

A CAPA or correction workflow may begin only after a human or authoritative tool confirms the issue through source authority, run_gate, exported data, in-game evidence, Blender evidence, or other explicit review.
