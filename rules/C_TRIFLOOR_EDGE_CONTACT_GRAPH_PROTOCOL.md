# C_TRIFLOOR Edge-Contact Graph Protocol

## Status

Mandatory for freeform `C_TRIFLOOR` structures beyond the validated regular/equilateral shape set.

## Validated base scope

`C_TRIFLOOR` has validated behavior for:

```text
- phase-resolved equilateral triangular surface placement
- centroid/normal/At placement for target triangular faces
- regular/equilateral closed solids
- recursive equilateral subdivision when generated from the validated V23-style logic
```

## Not automatically validated

```text
- arbitrary silhouette clipping
- freeform curved shells
- centroid-only scatter on a surface
- treating C_TRIFLOOR as a generic scalable triangle primitive
- nonuniform scale
- unpaired-edge surfaces
```

## Required freeform representation

Freeform builds must use an explicit edge/contact graph or curve/surface graph:

```python
C_TRIFLOOR_EDGE_GRAPH = {
    "nodes": {...},
    "adjacency": [
        {"a": "node_id", "a_edge": 0, "b": "node_id", "b_edge": 2, "relationship": "shared_edge", "hinge_angle_deg": 0.0}
    ],
    "boundary_edges": [
        {"node": "node_id", "edge": 1, "reason": "outer_silhouette"},
        {"node": "node_id", "edge": 2, "reason": "entrance_opening"}
    ]
}
```

## Required local-edge data

The part map must carry or reference enough geometry to compute:

```text
- local edge endpoints
- local edge midpoint
- local edge direction
- local face normal
- expected edge length / contact span
- edge-to-edge transform with optional hinge angle
```

## Generation rule

`C_TRIFLOOR` freeform placement must be derived from one of:

```text
- validated V23-style phase/equilateral lattice
- explicit shared-edge graph
- curve-follow transform propagation with declared step and tangent/normal frames
- surface mesh faces with edge-pair conformance
```

Centroid/spacing-only placement is insufficient for validated freeform builds.
