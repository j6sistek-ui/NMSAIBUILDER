# 00 — START HERE  (5.18.00 MASTER — current knowledge base & operating requirements)

## ⛔ THIS IS THE LAW — READ 00_FOUNDATIONAL_DOCTRINE.md FIRST

The first duty of every placement operation is Placement Precedence Resolution.

The documents in this package are mandatory.

If a document is wrong, fix the document.

Do not deviate.

Skipping a required authority source because it appears faster is a failure.

```text
Placement Intent
→ Placement Precedence Resolution
→ Method Selection
```

### Core Authority Files

* `00_FOUNDATIONAL_DOCTRINE.md` — governing doctrine.
* `00_OPERATING_CARD.md` — operational workflow.
* `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md` — mandatory placement procedure.
* `rules/BUILD_COMPLIANCE_MANIFEST_RULE.md` — build validity requirements.
* `rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md` — placement authority order.
* `rules/TRIAGE_REVIEW_ASSISTANCE_TOOL_RULE.md` — triage governance.
* `rules/PROJECT_TRANSFER_SUMMARY_RULE.md` — continuity governance.
* `rules/SESSION_ONBOARDING_CHECKLIST_RULE.md` — onboarding governance.
---

# ROUTER FIRST

Authority:

* rules/REQUEST_ROUTER_CHECKLIST.md

Before solving any request:

1. Classify the request.
2. Select the smallest sufficient bundle.
3. Load only the authority required for that route.
4. Do not preload the entire package.

Route first.

Reason second.

---

# CURRENT PLACEMENT INTELLIGENCE INFRASTRUCTURE

Placement-sensitive work is governed by:

```text
data/MASTER_PLACEMENT_INTELLIGENCE_INDEX.json
data/METHOD_AUTHORITY_TABLE.json
data/PLACEMENT_PRECEDENCE.json
data/NEGATIVE_KNOWLEDGE_INDEX.json

rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md
rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md
rules/PLACEMENT_MECHANICS_VS_CREATIVE_STYLE_SEPARATION_RULE.md
```

Mandatory doctrine:

```text
Assembly Context supersedes Component Context.

Component validation does not prove assembly validation.

Placement logic is universal.

Part-specific behavior is data.

Negative knowledge overrides positive component data.

Creative guidance never overrides placement authority.
```

Generated builds must produce:

```text
PLACEMENT_SESSION_RECEIPT
BUILD_PLACEMENT_SNAPSHOT
PLACEMENT_METHOD_SUMMARY
ASSEMBLY_CONFORMANCE_PLAN
PART_USAGE_MANIFEST
BUILD_COMPLIANCE_MANIFEST
```

## Per-build resolution (run this — do not rely on memory)

For any placement-sensitive build, resolution is an explicit step, not a recollection:

1. **Creative review FIRST.** Before choosing ObjectIDs, review the creative knowledge base for part characteristics and effects that serve the request (e.g. "futuristic" -> colorful, light-emitting): `data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json` (`part_geometric_character`, `color_variant_families`, `logged_motifs`) and `rules/PART_USE_CASE_CATALOG.md`. Let discovered effects inform part selection.
2. **Resolve the chosen ObjectIDs.** Run `validation/part_context_resolver.py --ids <ObjectIDs> --intent "<request>"`. It returns the FORCED placement context (precedence tier, snap, geometry, allowed methods, forbidden, applicable rules) plus the OFFERED creative context (`part_character`, recipes, fit-rules) as a firewalled advisory surface.
3. **Build only from the resolved snapshot**; cite each part in the BUILD COMPLIANCE MANIFEST.

The resolver is how universal-process rules, part-specific data, negative knowledge, and creative findings actually reach a build. A build that skips it is running on latent memory.

---

# CURRENT AUTHORITATIVE SNAP PLACEMENT

Authority:

```text
rules/AUTHORITATIVE_SNAP_PLACEMENT_PROTOCOL.md
library/authoritative_snap/
```

Rules:

```text
Snap data is authoritative when available.

Live snap relationships supersede generic placement assumptions.

Derived adjacency is fallback only when snap authority does not exist.

GAME_VALIDATED remains the highest confidence tier.
```

---

# CURRENT ONBOARDING REQUIREMENTS

Authority:

```text
ONBOARDING_VALIDATION_BUILD.md
rules/SESSION_ONBOARDING_CHECKLIST_RULE.md
```

Before accepting substantive build work:

Complete onboarding.

A successful onboarding proves:

```text
Source Readiness
+
Builder Readiness
```

Builder Readiness requires:

```text
tiny build
packet
manifest
placement snapshot
method summary
conformance plan
first gate run
failure diagnosis if failed
artifact/code correction
second gate run or BLOCKED explanation
final onboarding verdict
```

A packet-only exercise is not sufficient.

The onboarding mini build is a protocol gauntlet, not a demonstration.

First-run failure is acceptable.

Skipping diagnosis, correction, and re-gating is not acceptable.

The purpose of onboarding is to prove the build workflow can be:

```text
executed
validated
failed
diagnosed
corrected
re-validated
reported
```

---

# CURRENT TRIAGE GOVERNANCE

Authority:

```text
rules/TRIAGE_REVIEW_ASSISTANCE_TOOL_RULE.md
```

Triage is a review-assistance tool.

Triage findings are observations.

Triage findings are not:

```text
placement authority
compliance determinations
CAPA triggers
```

Missing a finding does not prove a build is clean.

Finding an issue does not prove a build is wrong.

Triage identifies candidate review areas.

Triage never overrides:

```text
run_gate
BUILD_COMPLIANCE_MANIFEST
PROJECT_BUILD_PLACEMENT_PACKET
PLACEMENT_PRECEDENCE
source-document authority
Blender evidence
in-game evidence
```

---

# ASSEMBLY FIRST

Assembly Context supersedes Component Context.

Component validation does not prove assembly validation.

Validate:

```text
Assembly
↓
Subsystem
↓
Component
```

Never reverse this hierarchy.

---

# RECIPE FIRST

For known structures, systems, and assemblies:

Read recipes before part maps.

Examples:

```text
bridges
stairs
ramps
towers
domes
rooms
walls
vehicles
airlocks
pipes
city modules
```

Do not reinvent known solutions when validated recipes exist.

---

# PLACEMENT AUTHORITY

Authority:

* data/PLACEMENT_PRECEDENCE.json
* data/METHOD_AUTHORITY_TABLE.json
* rules/PLACEMENT_PRECEDENCE_RESOLUTION_PROCEDURE.md

When placement authority exists:

1. Exact JSON / validated recipe
2. Authoritative snap or relational placement data
3. Validated assembly recipe
4. Verified placement intelligence
5. Part-specific overrides
6. Exception / prohibited knowledge
7. Manual heuristic only when unresolved

Do not reverse this order.

---

# NEGATIVE KNOWLEDGE

Negative knowledge remains authoritative until explicitly retired.

Do not use:

```text
prohibited parts
prohibited methods
invalid connectors
known failed placement approaches
```

even if they appear plausible.

---

# BUILD VALIDITY

No build is valid without:

```text
PROJECT_BUILD_PLACEMENT_PACKET
BUILD_COMPLIANCE_MANIFEST
required receipts
required gate results
```

Compliance must be demonstrated.

Not assumed.

---

# RECIPE SYSTEM

Recipes (how features are built) follow ONE method: see `MASTER_BUILD_RECIPES_AND_PLACEMENT_GUIDANCE.md` (storage + utilization wiring). Store of record: `toolkit/PLACEMENT_RECIPE_LIBRARY.json`.

# PROJECT CONTINUITY

When available, READ:

```text
OPEN_TOPICS_LOG.md
transfer_prompts/CHAT_TRANSFER_CURRENT.md
```

before reconstructing project state from memory.

Project continuity artifacts are preferred over conversation reconstruction.

---

# SOURCE-DOC IMPROVEMENT

If you discover:

```text
repeat failures
missing mappings
weak recipes
validation blind spots
governance gaps
triage weaknesses
```

recommend specific source-document updates.

Do not make major package changes without approval.

---

# PROJECT TRANSFER REQUIREMENT

Major deliverables must include:

```text
PROJECT_TRANSFER_SUMMARY
```

containing:

```text
Current Focus
Decisions Made
Open Issues
Resolved Issues
Files Created
Next Actions
Deferred Topics
```
---

# VALIDATION TARGET FIRST

When validating:

Validate the user's requested objective first.

Do not substitute:

```text
Package Health
```

for:

```text
Objective Validation
```

Do not validate the easiest measurable artifact.

Validate the requested target.

---

# OUTPUT DISCIPLINE

Generated NMS Python must use approved NMS Builder methods and pass run gate.

Do not substitute placeholder geometry, proxy objects, or unsupported techniques unless explicitly requested.

---

# VERSION

Current baseline: `5.18.00`

Release history: `CHANGELOG.md`

---

# PROTOCOL BANNER

Every substantive NMS response ends with:

```text
PROTOCOL ✓ — type: <request_type> | source docs rev: <revision> | bundle: <bundle> | gate: <verdict> | ambiguity: <none|clarification requested> | Docs Avail for Update?: <Yes (N)|No (0)>
```
