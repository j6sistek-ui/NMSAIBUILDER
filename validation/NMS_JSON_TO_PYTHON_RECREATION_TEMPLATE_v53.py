# NMS JSON → Python Recreation Template v53
#
# Validated transform for current JSON export/import path:
#   COORD_MODE = "XnZY"
#   AXIS_MODE = "RIGHT_AT_UP"
#   BASE_ROTATION_MODE = "POST_RX90"
#   POST_BASELINE_CORRECTION = "LOCAL_Y_180"
#
# This template is intentionally a skeleton. Paste or load SOURCE_BASE_JSON,
# then run in an initialized NMS Base Builder scene.

import bpy
import json
import math
import sys
import os
import tempfile
from mathutils import Vector, Matrix

PREFIX = "JSON_RECREATE_V53_"
ROOT_COLLECTION_NAME = PREFIX + "RECREATED_BASE"
TEMPLATE_COLLECTION_NAME = PREFIX + "TEMPLATES"

COORD_MODE = "XnZY"
AXIS_MODE = "RIGHT_AT_UP"
BASE_ROTATION_MODE = "POST_RX90"
POST_BASELINE_CORRECTION = "LOCAL_Y_180"
SCALE_MODE = "UP_LENGTH_UNIFORM"

SKIP_OBJECT_IDS = {"BASE_FLAG", "U_PARAGON"}

# Paste exported base JSON here or load it from a file.
SOURCE_BASE_JSON = r