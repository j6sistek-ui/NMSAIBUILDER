GEOMETRY_CONSTRUCTION_PLAN = {
    "construction_mode": "edge_graph_shell",
    "recognizable_features": ["front silhouette", "declared opening"],
    "placement_derivation": "C_TRIFLOOR edge/surface mesh derived transforms",
    "visual_conformance_checks": ["front_read", "edge_pairing"]
}
USED_PART_LOGIC = {"C_TRIFLOOR": {"reuse_mode": "ADAPTED_VERIFIED"}}
BUILD_INTENT_GRAPH = {"subassemblies_intended": False, "expected_connected_components": 1}
C_TRIFLOOR_EDGE_GRAPH = {"nodes": {}, "adjacency": [], "boundary_edges": []}
PART_IDS = ["C_TRIFLOOR"]
