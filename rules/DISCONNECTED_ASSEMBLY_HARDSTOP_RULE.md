# Disconnected Assembly Hard-Stop Rule (2.07.00)

## Status

Active required validation layer for all generated No Man's Sky build scripts and study boards.

## Mechanical no-float gate (run_gate, 2.07.00)

As of 2.07.00 this rule is no longer prose-only. `validation/run_gate.py` execs the
generated script, reconstructs each placed part's true world bounding box from its
captured transform plus the library `extent_*`/`center_*` fields, and **fails the gate
if any placed part touches no other placed part within 0.5 units.** This is enforcement
on the geometry, not on what the script's comments or role labels claim — a part named
`connected_*` that does not actually touch anything still fails.

Policy (most-restrictive interpretation):

- Float is the disfavored default and is almost never the right choice.
- Walls, floors, ramps, stairs, shells, and foundations must never float. The gate
  flags these as STRUCTURAL and the only correct response is to reconnect them.
- A floating part can be published only when the user has **explicitly requested** a
  floating part. That approval is obtained outside the gate and is required **every
  single run the gate fails** — it does not carry over from a prior script, a prior
  run, or a prior approval. The gate holds no state and never self-clears a float, so
  there is no in-script flag that can mark a float as intended; only fresh human
  approval of the publish can override a failing no-float gate.
- A "known JSON recipe" that intentionally spaces parts is not an automatic exception.
  It still fails the gate and still needs per-run approval.

The gate skips the check only when no library is supplied or fewer than two parts are
placed (a lone part cannot float relative to anything).

## Trigger

This rule applies when a script creates any assembled subsystem from repeated or adjacent parts, including but not limited to:

- stairs, ramps, ladders, catwalks, bridges, rails, corridors, pipes, gantries;
- towers, spires, roof crowns, caps, wall bays, trim rings, parapets;
- vehicles, machinery, consoles, doors, hatches, airlocks, and cave interiors.

## Hard-stop rule

Do not deliver a script whose subsystem relies on visual scatter, unsupported floating parts, or disconnected repeated pieces when a connected assembly is intended. A study file may test options, but every option must still state its connection model and either meet it or label itself as intentionally disconnected/negative.

## Required connection proof before delivery

For each assembled subsystem, record these fields in code comments and/or object properties:

```text
Subsystem name
ObjectIDs used
Source of placement: JSON control / FBX bounds / calibrated precedent / provisional
Anchor A / socket A
Anchor B / socket B, or ring/center/radius for radial systems
Path/ring/local-frame basis
Center-to-center step or chord
Overlap/contact tolerance
Origin mode: place_bottom / place_top / place_center / exact_json_transform
Expected continuity: touching / overlapped / intentionally separated
Failure action if disconnected in screenshot
```

## Origin-vs-bounds enforcement

Direct `place(x,y,z)` is not acceptable for vertical architecture unless the code explicitly states that `z` is the object origin and shows why that origin is correct. Prefer semantic wrappers:

```python
place_bottom(...)
place_top(...)
place_center(...)
place_exact_json(...)
```

For production or serious studies, the default is:

```text
Use FBX extent_y and center_y for vertical placement.
Use source JSON Position/Up/At for JSON-derived controls.
Never substitute guessed offsets for either.
```

## Path assemblies

Stairs, ramps, catwalks, rails, corridors, and gantries must be generated from endpoints, not decorative repetition. The script must compute or extract:

```text
start landing
end landing
path vector
yaw/orientation basis
module run
module rise
module count
first/last landing overlap
support cadence
```

If these fields are absent, the script fails this rule.

## Spire / tower / roof assemblies

A spire or roof crown is invalid if fins, roof parts, wall panels, or ornaments hover near the tower without a socket/collar/ring connection. Required practice:

1. Build the connected tower shaft first.
2. Add a physically connected collar or roof terrace.
3. Anchor crown parts into that collar by overlap/contact.
4. Add spire body with bottom/top placement, not origin guessing.
5. Add finial/antenna only after the spire body is visibly connected.

## Revert-not-patch behavior

If a disconnected assembly appears in screenshots, stop broad generation. Do not add more decorative parts. Revert to the last validated control or source JSON, produce a small isolated proof module, and only then resume full integration.

## Batman V11 regression note

This rule was added after `BATMAN_V11_POST_AIRLOCK_STUDIES` produced disconnected wall/spire pieces and non-connecting stair/ramp studies despite existing source rules. The root cause was using direct origin placement and broad visual studies instead of exact JSON controls, FBX origin-aware wrappers, and endpoint/path-based assemblies.
