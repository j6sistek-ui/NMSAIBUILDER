#!/usr/bin/env python3
"""
Validated stair-family helper functions.

These are dependency-free reference helpers for generated scripts. They encode the normal
full-ramp stair doctrine: floors anchor, stairs move, and ramp chains repeat in the local
At/Up frame.
"""
import math

RAMP_RUN_STEP = 5.33333
RAMP_RISE_STEP = 3.33333
STAIR_CONTACT_TUNE = 0.985
RUN_STEP = RAMP_RUN_STEP * STAIR_CONTACT_TUNE
RISE_STEP = RAMP_RISE_STEP * STAIR_CONTACT_TUNE
SMALL_OVERLAP = 0.10

def v_add(a,b): return [float(a[0])+float(b[0]), float(a[1])+float(b[1]), float(a[2])+float(b[2])]
def v_mul(a,s): return [float(a[0])*float(s), float(a[1])*float(s), float(a[2])*float(s)]
def v_len(a): return math.sqrt(sum(float(x)*float(x) for x in a))
def v_unit(a):
    L=v_len(a)
    return [0.0,0.0,0.0] if L <= 1e-9 else [float(a[0])/L, float(a[1])/L, float(a[2])/L]

def edge_start_primary(floor_extent_x, ramp_extent_z, small_overlap=SMALL_OVERLAP):
    return float(floor_extent_x) * 0.5 + float(ramp_extent_z) * 0.5 - float(small_overlap)

def local_step(up, at, run_step=RUN_STEP, rise_step=RISE_STEP):
    return v_add(v_mul(v_unit(at), run_step), v_mul(v_unit(up), rise_step))

def ramp0_from_floor_edge(floor_center, at, floor_extent_x, ramp_extent_z, small_overlap=SMALL_OVERLAP):
    return v_add(floor_center, v_mul(v_unit(at), edge_start_primary(floor_extent_x, ramp_extent_z, small_overlap)))

def ramp_chain(ramp0, up, at, count, run_step=RUN_STEP, rise_step=RISE_STEP):
    step = local_step(up, at, run_step, rise_step)
    return [v_add(ramp0, v_mul(step, i)) for i in range(int(count))]

def terminal_landing_from_last_ramp(last_ramp, up, at, run_step=RUN_STEP, rise_step=RISE_STEP):
    return v_add(last_ramp, local_step(up, at, run_step, rise_step))
