# Dome Study Lessons

**Status:** reusable technique notes.

## The measured method (proven)

A real successful spiraling glass dome was measured from its base JSON (round-trip residual <= 0.01) and recorded as method `DOME_RADIAL_RING_TAPER` with control recipe `dome_latitude_shell`:

- A dome IS built from rings — but **radius-tapering** rings, not constant-radius vertical rings. Constant-radius rings make a cylinder; radius-tapering rings plus surface-oriented glazing make a dome.
- Measured geometry: 24-fold symmetry, 15.0 deg step, 4 levels (r=16.00/10.67/5.34/0 at y=-1.12/2.21/5.55/8.88), linear taper radius = 14.21 - 1.60*height, 32 deg cone half-angle.
- Parts: roof glazing `S_ROOF_M_WIN` (24/ring; NOT in the snap map -> free/computed placement, precedence tier 1 recipe not tier 2 snap), sloped ribs `S_WALL_Q` (~12 at 30 deg, tilted ~32 deg), base ring `T_WALLT` (vertical, r=18.66).
- In-game appearance/color still pending.

## Surface-orientation basis

Surface-oriented panels use a local frame:

```text
local X = tangent around ring
local Y = meridian/surface-up direction
local Z = outward normal
```

Radius/chord controls ring count and scale; ring count tapers as radius shrinks.

## Part-count economy (one stylistic option)

- Dense `S_ROOF5` shells look detailed but are expensive.
- `S_WALLM_H` / wall-panel shells can conserve parts for an alternate smoother style — this is one stylistic option, not the proven measured build above.
- A separate topper/finial can preserve a recognizable silhouette with fewer body-shell parts.

## Visual standard

Part reduction is not enough. Any dome must still meet the visual objective: smooth silhouette, recognizable dome form, connected base/drum, and no random vertical panels.
