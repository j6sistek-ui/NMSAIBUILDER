#!/usr/bin/env python3
"""
Validated C_TRIFLOOR helper constants and reference operations.

This module intentionally stays lightweight. It prevents generated builds from losing the
recorded C_TRIFLOOR phase constants and centroid/normal/At placement contract.
"""
import math

PHASE_A_DEG = 150.0014
PHASE_B_DEG = 30.001369
PRIMARY_LATTICE_PITCH = 3.07884779402489

def v_add(a,b): return [float(a[0])+float(b[0]), float(a[1])+float(b[1]), float(a[2])+float(b[2])]
def v_sub(a,b): return [float(a[0])-float(b[0]), float(a[1])-float(b[1]), float(a[2])-float(b[2])]
def v_mul(a,s): return [float(a[0])*float(s), float(a[1])*float(s), float(a[2])*float(s)]
def v_dot(a,b): return float(a[0])*float(b[0])+float(a[1])*float(b[1])+float(a[2])*float(b[2])
def v_cross(a,b):
    return [float(a[1])*float(b[2])-float(a[2])*float(b[1]),
            float(a[2])*float(b[0])-float(a[0])*float(b[2]),
            float(a[0])*float(b[1])-float(a[1])*float(b[0])]
def v_len(a): return math.sqrt(v_dot(a,a))
def v_unit(a):
    L=v_len(a)
    return [0.0,0.0,0.0] if L <= 1e-9 else [float(a[0])/L,float(a[1])/L,float(a[2])/L]
def centroid(points):
    n=float(len(points))
    return [sum(p[0] for p in points)/n, sum(p[1] for p in points)/n, sum(p[2] for p in points)/n]

def rotate_about_axis(v, axis, deg):
    axis = v_unit(axis)
    th = math.radians(float(deg))
    c, s = math.cos(th), math.sin(th)
    return v_add(v_add(v_mul(v,c), v_mul(v_cross(axis,v),s)), v_mul(axis, v_dot(axis,v)*(1.0-c)))

def face_normal(a,b,c):
    return v_unit(v_cross(v_sub(b,a), v_sub(c,a)))

def c_trifloor_vectors_for_face(triangle_vertices, phase="A", reference_edge=(0,1)):
    """Return (Position, Up, At) for one C_TRIFLOOR on a triangular face."""
    a,b,c = triangle_vertices
    up = face_normal(a,b,c)
    i,j = reference_edge
    ref = v_unit(v_sub(triangle_vertices[j], triangle_vertices[i]))
    phase_deg = PHASE_A_DEG if str(phase).upper() == "A" else PHASE_B_DEG
    at = v_unit(rotate_about_axis(ref, up, phase_deg))
    return centroid(triangle_vertices), up, at
