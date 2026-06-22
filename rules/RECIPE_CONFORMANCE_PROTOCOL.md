# Recipe Conformance Protocol

Declared reuse is necessary but **not sufficient**. A `USED_PART_LOGIC` receipt proves the
script *intended* to reuse validated logic; it does not prove the produced geometry actually
obeys the recorded recipe. A build can carry a perfect receipt and still place parts that
ignore the validated orientation (e.g. a staircase rotated 90 degrees onto the ground). The
connectivity gate cannot catch this, because rigid rotation preserves centre-to-centre spacing.

## What is enforced

`validation/recipe_conformance_check.py` ingests the build's **exported NMS JSON**
(Position / Up / At per part - the in-game frame) and checks it against the partmap recipe.

For every approved stair part it verifies the recorded `placement_signature` from the partmap:

    Position[n+1] = Position[n] + At * RUN_STEP + Up * RISE_STEP

using each part's **own exported At/Up vectors** and the RUN_STEP / RISE_STEP read from that
part's partmap. A part that sits one lattice step from a stair neighbour but whose displacement
does not decompose onto its own (or the neighbour's) At/Up within tolerance is mis-oriented
versus the recipe and **FAILS** - this is exactly the tipped-build failure that connectivity
and a declared receipt both miss.

Unvalidated parts are not judged here: conformance is only asserted where a validated recipe
exists. (Pyramid-face C_TRIFLOOR tiling, the angled door, etc. remain UNTESTED and are out of
scope until their placement is validated.)

## How to run

Builds that place validated parts must be gated with the exported geometry:

    python3 validation/run_gate.py <script.py> <library.json> <TAG> \
        --require-router --require-json-evidence --require-validated-reuse \
        --require-conformance <exported_nms.json>

The receipt (`USED_PART_LOGIC` / `BUILD_INTENT_GRAPH`) answers "did the build claim to reuse the
validated logic?" The conformance gate answers "did the exported parts actually land where the
validated recipe says?" Both are required for a validated-part build; the second makes the first
falsifiable against real output.

## Scope and limits

- Conformance currently covers the validated stair local-frame repeat (run/rise along At/Up).
  Edge-start and terminal-landing relations are recorded in the partmap and are candidate
  extensions to this check.
- Tolerances (lattice 0.65u, relation 0.90u) are tunable.
- The check needs the exported JSON; it does not re-derive the Blender->NMS export transform.
  Validating that transform as a single shared routine remains the next lever (it is what every
  cold chat must apply identically).

## mandatory run-gate behavior

`run_gate.py` auto-detects validated/user-reviewed parts and build-generation scripts.

If validated logic is detected:
- `validated_logic_reuse_check.py` is auto-required.
- If an executable recipe conformance module exists for those parts, exported NMS JSON is required.
- If exported JSON is missing, the gate must report `REQUIRED_NOT_RUN` / `FAIL` and the final response must not claim validated placement compliance.

For current stair conformance, use:

```text
--require-conformance <exported_nms.json>
```

The same exported JSON is also used for intent-graph connected-component conformance when a `BUILD_INTENT_GRAPH` is present.
