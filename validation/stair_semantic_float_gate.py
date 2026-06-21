#!/usr/bin/env python3
"""
stair_semantic_float_gate.py

Scoped semantic connectivity helper for approved normal full-ramp stairs.

This script does not replace the generic AABB float gate. It is a supplemental
family-specific checker for exported JSON / placement reports that include
ObjectID, Position, Up, and At fields.

Approved scope:
  B_RAMP, C_RAMP, F_RAMP, M_RAMP, S_RAMP, T_RAMP, W_RAMP

Unapproved scope:
  half ramps, special ramps, non-stair parts, and global AABB relaxation.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

APPROVED_FULL_RAMPS = {"B_RAMP", "C_RAMP", "F_RAMP", "M_RAMP", "S_RAMP", "T_RAMP", "W_RAMP"}
APPROVED_FLOORS = {"B_FLOOR", "C_FLOOR", "F_FLOOR", "M_FLOOR", "S_FLOOR", "T_FLOOR", "W_FLOOR"}

RAMP_RUN_STEP = 5.33334
RAMP_RISE_STEP = 3.33333
STAIR_CONTACT_TUNE = 0.985
RUN_STEP = RAMP_RUN_STEP * STAIR_CONTACT_TUNE
RISE_STEP = RAMP_RISE_STEP * STAIR_CONTACT_TUNE

DEFAULT_TOLERANCE = 0.65

def clean_oid(oid: Any) -> str:
    return str(oid or "").lstrip("^")

def v_len(v: Iterable[float]) -> float:
    vals = [float(x) for x in v]
    return math.sqrt(sum(x * x for x in vals))

def v_unit(v: Iterable[float]) -> List[float]:
    vals = [float(x) for x in v]
    L = v_len(vals)
    if L <= 1e-9:
        return [0.0, 0.0, 0.0]
    return [x / L for x in vals]

def v_add(a: Iterable[float], b: Iterable[float]) -> List[float]:
    return [float(x) + float(y) for x, y in zip(a, b)]

def v_sub(a: Iterable[float], b: Iterable[float]) -> List[float]:
    return [float(x) - float(y) for x, y in zip(a, b)]

def v_mul(a: Iterable[float], s: float) -> List[float]:
    return [float(x) * float(s) for x in a]

def dist(a: Iterable[float], b: Iterable[float]) -> float:
    return v_len(v_sub(a, b))

def is_approved_ramp(item: Dict[str, Any]) -> bool:
    return clean_oid(item.get("ObjectID")) in APPROVED_FULL_RAMPS

def is_floor(item: Dict[str, Any]) -> bool:
    return clean_oid(item.get("ObjectID")) in APPROVED_FLOORS

def expected_next_ramp_or_landing(ramp: Dict[str, Any]) -> List[float]:
    pos = ramp["Position"]
    at = v_unit(ramp["At"])
    up = v_unit(ramp["Up"])
    return v_add(v_add(pos, v_mul(at, RUN_STEP)), v_mul(up, RISE_STEP))

def semantic_neighbors(items: List[Dict[str, Any]], tolerance: float = DEFAULT_TOLERANCE) -> Dict[str, Any]:
    """Return a report of approved ramp semantic neighbors.

    This helper checks whether each approved ramp has another approved ramp or floor
    near its expected next stair/landing position. It is intentionally narrow and
    does not certify non-stair parts.
    """
    ramps = [i for i in items if is_approved_ramp(i)]
    targets = [i for i in items if is_approved_ramp(i) or is_floor(i)]
    results = []
    for idx, ramp in enumerate(ramps):
        exp = expected_next_ramp_or_landing(ramp)
        best = None
        best_d = None
        for t in targets:
            if t is ramp:
                continue
            d = dist(exp, t.get("Position", [0, 0, 0]))
            if best_d is None or d < best_d:
                best = t
                best_d = d
        passed = best_d is not None and best_d <= tolerance
        results.append({
            "ramp_index": idx,
            "ramp_object_id": clean_oid(ramp.get("ObjectID")),
            "ramp_position": ramp.get("Position"),
            "expected_next_position": exp,
            "nearest_candidate_object_id": clean_oid(best.get("ObjectID")) if best else None,
            "nearest_candidate_position": best.get("Position") if best else None,
            "distance": best_d,
            "semantic_next_connection_pass": passed,
        })
    return {
        "checker": "stair_semantic_float_gate",
        "scope": "approved_normal_full_ramps_only",
        "raw_aabb_gate_replaced": False,
        "approved_ramps": sorted(APPROVED_FULL_RAMPS),
        "tolerance": tolerance,
        "ramp_count": len(ramps),
        "results": results,
        "summary": {
            "semantic_checked": len(results),
            "semantic_pass": sum(1 for r in results if r["semantic_next_connection_pass"]),
            "semantic_fail": sum(1 for r in results if not r["semantic_next_connection_pass"]),
        },
    }

def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("usage: stair_semantic_float_gate.py <exported_json_file> [tolerance]", file=sys.stderr)
        return 2
    path = Path(argv[1])
    tolerance = float(argv[2]) if len(argv) > 2 else DEFAULT_TOLERANCE
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("FAIL: expected top-level JSON list", file=sys.stderr)
        return 1
    report = semantic_neighbors(data, tolerance)
    print(json.dumps(report, indent=2))
    return 0 if report["summary"]["semantic_fail"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
