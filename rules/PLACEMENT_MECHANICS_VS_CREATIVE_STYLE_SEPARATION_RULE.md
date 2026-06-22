# Placement Mechanics vs Creative Style Separation Rule (4.01.00)

## Rule

Placement mechanics and creative/style/use-case knowledge must remain separate authority lanes.

## Placement intelligence controls how parts physically work

Examples: orientation, snap, bbox/origin, assembly conformance, exceptions, do-not-use entries, support/contact rules.

## Creative/style knowledge controls what a build is trying to express

Examples: gothic castle motifs, Gotham mood, lighting tricks, decoration symbolism, silhouette, composition, cinematic style.

## Non-overwrite rule

Creative knowledge can suggest what to build. It must not override `data/MASTER_PLACEMENT_INTELLIGENCE_INDEX.json`, `data/METHOD_AUTHORITY_TABLE.json`, `data/NEGATIVE_KNOWLEDGE_INDEX.json`, or assembly conformance rules.
## worked example — mechanics lock spacing, style keeps free scale

A functional spiral stair holds a fixed walkable rise (~0.227) independent of part scale: you cannot uniformly scale a working stair up without breaking walkability. Decorative/showpiece assemblies (swords, tapered shafts, light fans) carry no such constraint and may be freely scaled. Treat walkable/connective spacing as a mechanics invariant; treat decorative scale as free.

## worked example (cautionary) — the retired gothic-church CAPA
**What happened:** a live gothic church reused `S_RAMP` as decorative buttresses with **guessed rotations**, labelled the result `EXPERIMENTAL_VARIANT`, and **skipped** the validated `STAIR_RAMP_ENDPOINT_RECIPE` that the builder sheet had surfaced for `S_RAMP` (which is on negative knowledge as `MANUAL_STRUCTURAL_RAMP`). Root class: `SHEET_NOT_UTILIZED`.

**Corrective logic (generalizes beyond that build):**
1. Creative / decorative / *experimental* framing changes WHICH part you choose and WHERE it sits aesthetically. It NEVER waives a `required_method` or a `NEGATIVE_KNOWLEDGE_INDEX` constraint on that part. If the sheet surfaces a required method (tier-6), the mechanical gate applies no matter how decorative the intent.
2. `EXPERIMENTAL_VARIANT` is not a bypass token. A novel placement of a part that HAS a required method must still either use the method or explicitly flag the divergence and accept that it is NOT validated and will NOT pass the gate.
3. If the builder sheet surfaces a method for a used part, USE IT or explicitly justify divergence — never silently skip it. Per the standing discipline: execute field-for-field or flag divergence; prove, don't attest.
4. Distinction to keep straight: decorative **scale/position** is free (see the 4.03.00 example); a part's required **placement method**, where one exists, is a mechanics invariant creative intent cannot override.
