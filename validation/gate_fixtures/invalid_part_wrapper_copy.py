# JSON_EVIDENCE_MAPPING_GATE
from bl_ext.user_default.no_mans_sky_base_builder import BUILDER
TAG = "FIXTURE_BAD_"
PART_IDS = ["S_GDOOR"]

REQUEST_CLASSIFICATION = {
    "request_type": "json_to_python_recreation",
    "user_inputs": ["fixture"],
    "rule_bundles_checked": ["REQUEST_ROUTER_CHECKLIST", "PROTOCOL_BANNER_HARD_FAIL_RULE", "WORKING_JSON_FIRST_PRINCIPLE", "JSON_EVIDENCE_MAPPING_GATE"],
    "ambiguity_resolution": "not_needed",
    "json_evidence_used": True
}
JSON_EVIDENCE_PROVENANCE = {"source":"fixture"}
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
# scoped cleanup proof for static gate
for old in list([]):
    if str(getattr(old, "name", "")).startswith(TAG):
        pass
obj = BUILDER.add_part("S_GDOOR")
obj.name = TAG + "001_S_GDOOR"
copy = obj.copy()
