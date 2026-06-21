#!/usr/bin/env python3
# Fixture: uses a validated part but omits USED_PART_LOGIC and BUILD_INTENT_GRAPH.
# run_gate must auto-require the validated reuse gate and FAIL even without explicit flags.
from bl_ext.user_default.no_mans_sky_base_builder import BUILDER
TAG = "AUTO_VALIDATED_BAD_"
PART_IDS = ["S_RAMP"]
REQUEST_CLASSIFICATION = {"request_type": "build_generation", "source_docs_rev": "2.17.01", "rule_bundles_checked": ["REQUEST_ROUTER_CHECKLIST", "PROTOCOL_BANNER_HARD_FAIL_RULE"], "ambiguity_resolution": "not_needed"}
for old in list([]):
    if str(getattr(old, "name", "")).startswith(TAG):
        pass
created = BUILDER.add_part("S_RAMP")
obj = getattr(created, "object", created)
obj.name = TAG + "001_S_RAMP"
obj["ObjectID"] = "S_RAMP"
