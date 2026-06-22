#!/usr/bin/env python3
REQUEST_CLASSIFICATION = {"request_type": "build_generation", "source_docs_rev": "2.17.01"}
BUILD_INTENT_GRAPH = {
    "subassemblies_intended": False,
    "expected_connected_components": 1,
    "connection_policy": "FULLY_CONNECTED_BUILD",
    "required_connections": [{"from": "a", "to": "b", "type": "must_touch"}]
}
