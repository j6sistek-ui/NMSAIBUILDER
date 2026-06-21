# Composite Build Intent Graph Protocol — 2.17.01

## Status

**Mandatory for composite builds and large builds.**

A no-float check can pass while the requested build is still wrong. A build can contain
several internally connected subassemblies while the intended connections between them are
missing. The switchback/walkway/pyramid failure proved that the gate must understand the
user's build intent, not just local proximity.

## Required manifest

Every composite generated build must include:

```python
BUILD_INTENT_GRAPH = {
    "subassemblies_intended": False,
    "expected_connected_components": 1,
    "connection_policy": "FULLY_CONNECTED_BUILD",
    "required_connections": [
        {
            "from": "switchback_top_floor",
            "to": "walkway_start",
            "type": "must_touch",
            "tolerance": 0.50
        },
        {
            "from": "walkway_end",
            "to": "pyramid_threshold_or_door",
            "type": "must_touch",
            "tolerance": 0.50
        },
        {
            "from": "door",
            "to": "pyramid_face_opening",
            "type": "must_be_flush",
            "tolerance": 0.25
        }
    ]
}
```

## Subassemblies

Subassemblies are allowed when intended. The script must declare:

```text
subassemblies_intended = True
expected_connected_components = N
subassemblies = [...]
reason = why gaps are intentional
```

Examples:

```text
- separate display specimens
- validation matrix rows
- before/after comparison groups
- intentionally separated city districts
```

If `subassemblies_intended = False`, the expected connected-component count must be `1`.

## Reporting requirement

The build report must state:

```text
- expected connected components
- observed connected components when available
- required connections checked
- required connections not checked
- any intentional gaps
```

If the observed component count is far above the declared count, the build is not acceptable
even if every part has at least one neighbor.

## Gate status

2.16.00 checked that the manifest existed. 2.17.01 adds exported-geometry conformance:

```text
validation/intent_graph_conformance_check.py <script.py> <exported_nms.json> <library.json>
```

This computes observed connected components from exported ObjectID positions and dimension-library extents, then compares them to `BUILD_INTENT_GRAPH.expected_connected_components`.

For a fully connected build:

```text
subassemblies_intended = False
expected_connected_components = 1
```

any observed component count other than `1` is a failure.

For validation matrices or intentionally separated groups:

```text
subassemblies_intended = True
expected_connected_components = N
```

the observed count must match `N`, and the response/report must explain the role of each disconnected subassembly.

This gate is a conservative proxy, not visual proof. It is still mandatory when exported geometry is available because it catches the failure where stairs, walkway, door, and pyramid are each internally connected but the requested composite build is disconnected.


## Experimental option collections

Generated files may include experimental options in the same Blender script only if they are separated and declared.

Required:

```python
EXPERIMENTAL_VARIANTS = [
    {"collection": "EXPERIMENTAL_OPTION_A", "parts": [...], "reuse_mode": "EXPERIMENTAL_VARIANT"}
]
BUILD_INTENT_GRAPH["subassemblies_intended"] = True
```

or separate `CORE_BUILD_INTENT_GRAPH` / `EXPERIMENTAL_BUILD_INTENT_GRAPH` manifests.

Experimental collections must not be counted as proof that the core connected build passes. They must carry provisional/experimental reuse modes for unvalidated parts.
