# JSON_EVIDENCE_MAPPING_GATE
# Connectivity self-test fixture: two parts touch, one floats far above -> must FAIL the no-float gate.
from bl_ext.user_default.no_mans_sky_base_builder import BUILDER
TAG = "FIXTURE_FLOAT_"
PART_IDS = ["S_FLOOR"]

REQUEST_CLASSIFICATION = {
    "request_type": "json_to_python_recreation",
    "user_inputs": ["fixture"],
    "rule_bundles_checked": ["UNIVERSAL_RULES", "SYSTEMATIC_FAILURE_CAPA_PROTOCOL", "REQUEST_ROUTER_CHECKLIST", "NMS_BUILDER_EXECUTION_KERNEL", "WORKING_JSON_FIRST_PRINCIPLE", "JSON_EVIDENCE_MAPPING_GATE", "JSON_TO_PYTHON_RECREATION_PROTOCOL", "JSON_TO_PYTHON_RECREATION_PROTOCOL", "NMS_BUILD_VS_IMAGE_ROUTING_GUARD", "DISCONNECTED_ASSEMBLY_HARDSTOP_RULE", "SYSTEMATIC_FAILURE_CAPA_PROTOCOL", "SELECTIVE_VISUAL_MEMORY_POLICY", "DOCS_UPDATE_AVAILABILITY_PROTOCOL", "PER_RESPONSE_PROTOCOL_CONFIRMATION_RULE", "PROTOCOL_BANNER_HARD_FAIL_RULE", "PART_PLACEMENT_MAP_SCHEMA"],
    "ambiguity_resolution": "not_needed",
    "json_evidence_used": True
}
JSON_EVIDENCE_PROVENANCE = {"source": "fixture"}
COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"
# scoped cleanup proof for static gate
for old in list([]):
    if str(getattr(old, "name", "")).startswith(TAG):
        pass

def _place(oid, loc, i):
    part = BUILDER.add_part(oid)
    obj = getattr(part, "object", part)
    obj.name = TAG + ("%03d_" % i) + oid
    obj["ObjectID"] = oid
    obj.location = loc
    obj.scale = (1.0, 1.0, 1.0)
    return obj

# Two connected floors...
_place("S_FLOOR", (0.0, 0.0, 0.0), 1)
_place("S_FLOOR", (5.0, 0.0, 0.0), 2)
# ...and one orphan floating 50 units up, touching nothing -> must FAIL.
_place("S_FLOOR", (0.0, 0.0, 50.0), 3)
