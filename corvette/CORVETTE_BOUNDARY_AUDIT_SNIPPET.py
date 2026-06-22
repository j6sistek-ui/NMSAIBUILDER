# Corvette boundary audit snippet v48
# Use inside Corvette generators after final placements are assembled and before delivery.
# Safe envelope = 95m side length; reported absolute boundary ~= 100m.
# IMPORTANT: In Corvette mode this audit must include every final placement in the
# Corvette assembly, including non-Corvette/base/decorative parts placed on or in
# the ship. Do not filter to Category == Corvette.

CORVETTE_ABSOLUTE_BOUNDARY_SIDE_M = 100.0
CORVETTE_SAFE_BOUNDARY_SIDE_M = 95.0
CORVETTE_SAFE_HALF_EXTENT_M = CORVETTE_SAFE_BOUNDARY_SIDE_M / 2.0

# Placement input contract expected by this snippet:
# placements = [
#   {"ObjectID": "B_COK_B", "position": {"x":0,"y":0,"z":0}, "rotation": {"x":0,"y":0,"z":0}, "scale": 1.0},
#   {"ObjectID": "BILLBOARD", "position": {"x":8,"y":1,"z":0}, "rotation": {"x":0,"y":0,"z":90}, "scale": 1.0},
# ]
# part_dims = {"B_COK_B": {"extent_x": 6.324219, "extent_y": 4.624023, "extent_z": 5.790321}}
# Include only objects that remain in the final Corvette export. Exclude deleted templates/debug markers.

import math


def _rotation_matrix_xyz(rx_deg, ry_deg, rz_deg):
    rx, ry, rz = math.radians(rx_deg), math.radians(ry_deg), math.radians(rz_deg)
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    return [
        [cz*cy, cz*sy*sx - sz*cx, cz*sy*cx + sz*sx],
        [sz*cy, sz*sy*sx + cz*cx, sz*sy*cx - cz*sx],
        [-sy,   cy*sx,                cy*cx],
    ]


def _rotated_half_extents(extents, rotation_deg, scale):
    hx, hy, hz = (extents[0] * scale / 2.0, extents[1] * scale / 2.0, extents[2] * scale / 2.0)
    R = _rotation_matrix_xyz(rotation_deg.get('x', 0), rotation_deg.get('y', 0), rotation_deg.get('z', 0))
    return (
        abs(R[0][0])*hx + abs(R[0][1])*hy + abs(R[0][2])*hz,
        abs(R[1][0])*hx + abs(R[1][1])*hy + abs(R[1][2])*hz,
        abs(R[2][0])*hx + abs(R[2][1])*hy + abs(R[2][2])*hz,
    )


def audit_corvette_boundary(placements, part_dims, origin=(0.0, 0.0, 0.0), safe_side_m=CORVETTE_SAFE_BOUNDARY_SIDE_M):
    """Audit the final Corvette assembly footprint.

    Do not pre-filter placements by category. A non-Corvette decoration mounted on
    the Corvette can still exceed the ship boundary and must be counted.
    """
    safe_half = safe_side_m / 2.0
    min_v = [float('inf'), float('inf'), float('inf')]
    max_v = [float('-inf'), float('-inf'), float('-inf')]
    violations = []
    missing_dims = []

    for p in placements:
        oid = p['ObjectID']
        if oid not in part_dims:
            missing_dims.append(oid)
            continue
        dims = part_dims[oid]
        ext = (float(dims['extent_x']), float(dims['extent_y']), float(dims['extent_z']))
        pos = p.get('position', {})
        rot = p.get('rotation', {})
        scale = float(p.get('scale', 1.0))
        center = (float(pos.get('x', 0.0)), float(pos.get('y', 0.0)), float(pos.get('z', 0.0)))
        rh = _rotated_half_extents(ext, rot, scale)
        for i, axis in enumerate('xyz'):
            distance_with_half = abs(center[i] - origin[i]) + rh[i]
            if distance_with_half > safe_half:
                violations.append({
                    'ObjectID': oid,
                    'axis': axis,
                    'distance_plus_half_extent_m': round(distance_with_half, 3),
                    'safe_half_extent_m': safe_half,
                    'note': 'Final Corvette assembly boundary violation; category does not matter.'
                })
            min_v[i] = min(min_v[i], center[i] - rh[i])
            max_v[i] = max(max_v[i], center[i] + rh[i])

    if missing_dims:
        return {
            'ok': False,
            'safe_side_m': safe_side_m,
            'error': 'Missing FBX dimensions for one or more final Corvette placements.',
            'missing_dimension_objectids': sorted(set(missing_dims)),
        }

    spans = {axis: round(max_v[i] - min_v[i], 3) for i, axis in enumerate('xyz')}
    span_violations = {axis: span for axis, span in spans.items() if span > safe_side_m}
    ok = not violations and not span_violations
    return {
        'ok': ok,
        'safe_side_m': safe_side_m,
        'absolute_side_m': CORVETTE_ABSOLUTE_BOUNDARY_SIDE_M,
        'spans_m': spans,
        'part_boundary_violations': violations,
        'span_violations': span_violations,
        'scope_note': 'Audited all final Corvette placements, including non-Corvette parts.'
    }
