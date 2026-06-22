# BUILD OBJECT USE MANIFEST TEMPLATE  (v57 — with provenance)

The v54 manifest recorded *what* each part does. v57 adds **provenance**: where
each decision came from. This is how the user can verify the data was actually
used — the build's own manifest shows the source of every subsystem. A subsystem
with no citation is a visible gap, not a silent guess.

## Per-subsystem provenance table (required)

One row per subsystem (not per part). The last three columns are the new gate:

| Subsystem | Primary ObjectIDs | Recipe id cited | Rule/issue id cited | Library rows used | Why this source |
|---|---|---|---|---|---|
| e.g. cave airlock | `S_DOORM0`, ring walls | `radial_airlock_iris_door` | `SPACING_CONNECTION_SCALE_RULES#rings` | rows for those IDs | matched radial center/radius/chord recipe |
| e.g. tower cap | `CUBEROOF`,`PIPESHAPE` | (none — novel) | `PART_FAMILY_RULES#roof` | CUBEROOF row | no recipe yet; candidate to promote |

Rules:
- Every subsystem cites **at least one** of: a recipe id from
  `toolkit/PLACEMENT_RECIPE_LIBRARY.json`, a rule/issue id, or the specific
  library rows it pulled bounds from.
- If a subsystem cites **(none)**, you must say why (novel/experimental) and flag
  it as a candidate to promote into a recipe after validation.
- Do not invent a recipe id. If none fits, write `(none — novel)`.

## Per-part detail table (as in v54)

| ObjectID | Count | Role | Use type | Scale range | Orientation notes | Risks |
|---|---:|---|---|---|---|---|

Use type ∈ {literal, transformed, hidden, structural, decorative, experimental}.

## Why provenance

"I consulted the catalog" is unverifiable and drifts. A cited recipe id is
checkable: the user (or a linter) can confirm the id exists and that the
subsystem matches it. Traceability turns "trust me" into "here's the source."
