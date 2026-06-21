#!/usr/bin/env python3
REQUEST_CLASSIFICATION = {"request_type": "build_generation", "source_docs_rev": "2.16.00"}
PART_IDS = ["S_RAMP", "S_FLOOR", "C_TRIFLOOR", "S_DOOR"]
USED_PART_LOGIC = {
    "S_RAMP": {
        "partmap_path": "library/part_placement_maps/S_RAMP.partmap.json",
        "validated_algorithm": "STAIR_LOCAL_FRAME_REPEAT_AND_EDGE_START",
        "reuse_mode": "DIRECT_REUSE",
        "source_transform_invariants": ["Position", "Up", "At"],
        "recipe_source": "toolkit/validated_recipes/stairs.py"
    },
    "C_TRIFLOOR": {
        "partmap_path": "library/part_placement_maps/C_TRIFLOOR.partmap.json",
        "validated_algorithm": "C_TRIFLOOR_PHASE_RESOLVED_GEOMETRIC_SUBDIVISION_V23",
        "reuse_mode": "DIRECT_REUSE",
        "source_transform_invariants": ["Position", "Up", "At"],
        "recipe_source": "toolkit/validated_recipes/c_trifloor.py"
    },
    "S_FLOOR": {
        "partmap_path": "library/part_placement_maps/part_placement_master_sheet.csv",
        "validated_algorithm": None,
        "reuse_mode": "PROVISIONAL_BLOCK_OR_REVIEW",
        "reason": "floor is used as anchor; no advanced fitment claim"
    },
    "S_DOOR": {
        "partmap_path": "library/part_placement_maps/part_placement_master_sheet.csv",
        "validated_algorithm": None,
        "reuse_mode": "PROVISIONAL_BLOCK_OR_REVIEW",
        "reason": "door-on-sloped-triangle-face not validated"
    }
}
BUILD_INTENT_GRAPH = {
    "subassemblies_intended": False,
    "expected_connected_components": 1,
    "connection_policy": "FULLY_CONNECTED_BUILD",
    "required_connections": [
        {"from": "switchback_top_floor", "to": "walkway_start", "type": "must_touch", "tolerance": 0.5},
        {"from": "walkway_end", "to": "pyramid_threshold", "type": "must_touch", "tolerance": 0.5}
    ]
}
