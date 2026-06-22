# Working JSON First Principle (1.03.01)

Status: **universal, mandatory, foundational**.

## Rule statement

Working exported No Man's Sky base JSON is one of the highest-priority evidence sources in the entire source package. When relevant working JSON exists, it must be checked and used before the generator falls back to generic orientation assumptions, memory, visual guesses, or FBX-only reasoning.

This is not optional context. Working JSON is **serialized transform truth** and **recipe evidence**.

## What must be checked

Before generating, repairing, validating, or converting an NMS Builder Python script, the assistant/generator must check whether the current sources, uploaded files, master docs, or user-provided material include relevant:

- exported base JSON;
- pasted JSON snippets;
- JSON-derived studies;
- known working module JSON such as airlocks, stairs, bridges, vehicles, signs, wall curvature, connected surfaces, market/stall modules, tower modules, room modules, interior machinery, or detail clusters;
- previous generated-build exported JSON used for Python-vs-outcome auditing.

If relevant JSON exists, it must be treated as the first placement source.

## Why this is foundational

A JSON object records the real saved transform evidence:

```text
ObjectID
Position
Up vector
At vector
scale encoded in Up/At vector lengths
UserData/material
object ordering and repeated cluster patterns
```

Those fields show how working parts actually placed, faced, scaled, connected, overlapped, and serialized. FBX bounds remain essential for native part geometry, clearance, spacing, collision, and scale adjustment, but FBX alone does not prove a working in-game assembly. Working JSON does.

## Mandatory priority order

When placing or correcting a subsystem, use this order:

1. **Exact working JSON object transform**: ObjectID, Position, Up, At, scale vector lengths, UserData.
2. **Extracted JSON recipe/cluster**: local coordinate frame, deltas, anchors, repeated spacing, module bounding box, role labels.
3. **Documented recipe or toolkit module** from the master docs.
4. **FBX bounds + part-family rule** for geometric adjustment, scale changes, contact/clearance, and collision estimation.
5. **Generic orientation fallback** only when no JSON or documented recipe exists, and with explicit uncertainty.

## Mandatory JSON recipe extraction

For each relevant working subsystem in JSON, extract:

- ObjectIDs and count;
- local cluster origin / coordinate frame;
- Position deltas between related parts;
- Up / At basis vectors and inferred Right vector;
- vector magnitudes as serialized scale evidence;
- FBX bounds transformed into world space;
- contact points, overlaps, gaps, vertical rise/run, ring chord spacing, or bridge path spacing as applicable;
- anchor relationships: what each prop, vine, panel, stair, bridge, sign, or canopy is physically attached to;
- UserData/material patterns;
- visual validation notes from screenshots if available.

## Required use in generated code

A JSON-informed script must include a `JSON_EVIDENCE_PROVENANCE` block naming the source JSON and the subsystems mined from it.

For **JSON→Python recreation**, also declare the validated recreation constants:

```python
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
```

For **Python-generated builds that will be audited through exported JSON**, declare the audit mapping intent instead:

```python
EXPORTED_JSON_AUDIT_REQUIRED = True
PYTHON_TO_JSON_POSITION_MAP = "Position=[x,z,-y] for Blender/Python (x,y,z)"
JSON_AUDIT_FIELDS = ["ObjectID", "Position", "Up", "At", "UserData"]
```

Do not double-apply the JSON→Python recreation stack to direct Blender-space procedural placement.

## Context distinction

| Context | Correct use of JSON |
|---|---|
| JSON→Python recreation | Use `XnZY + RIGHT_AT_UP + POST_RX90 + LOCAL_Y_180`; scale from Up/At lengths. |
| High-quality source JSON recipe mining | Extract working local recipes, deltas, anchors, basis vectors, and scale distributions; parameterize only after reproducing the control recipe. |
| Python→Blender→exported JSON validation | Use exported JSON as reverse serialized truth; compare `Position`, `Up`, `At`, scale, and UserData against Python intent. |

## Failure condition

It is a source-governance failure if a generator creates or fixes a subsystem from generic assumptions while relevant working JSON exists and was not checked.

Failure response:

1. stop generation;
2. identify the skipped JSON evidence;
3. extract the relevant recipe or serialized transform facts;
4. correct the script or docs;
5. rerun the executable gate and JSON geometry validation loop.

## rollout clarification

When the user provides JSON for the current build, treat it as the active orientation/placement control. The assistant must use JSON mapping to determine how parts actually ended up before making further Python changes. This includes comparing intended role to serialized `Position`, `Up`, `At`, scale vector lengths, local clusters, anchors, and transformed FBX bounds. Generic orientation tables are not acceptable in place of this check.

## geometry-intelligence reinforcement

When relevant JSON exists, exact recreation is not the end state. Apply `rules/JSON_TO_PYTHON_RECREATION_PROTOCOL.md` to preserve the reusable logic: part roles, anchors, local frames, connection/contact relationships, locked invariants, allowed parameter slots, and missing evidence.

If a prior JSON-derived technique cannot be found in `toolkit/PLACEMENT_RECIPE_LIBRARY.json`, `data/JSON_RECIPE_SIGNATURE_INDEX.json`, reports, or the source package, do not claim the technique was retained. Request the source JSON again or mark the recipe provisional.


## Working JSON as behavior training data

Working JSON is not only serialized transform truth. It is also behavior training data.

When the user is teaching part placement or asking for source-style reuse, first mine the working JSON for a `PART_BEHAVIOR_SIGNATURE`. Do not reinvent placement from generic geometry if the working JSON already proves fitment, mating, density, or construction style.
