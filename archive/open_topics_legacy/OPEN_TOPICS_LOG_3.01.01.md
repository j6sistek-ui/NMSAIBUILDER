# Open Topics Log — 3.01.01

## PIPE/BUBPIPE focused validation required

Status: open.

Need a focused pipe validation harness that tests `PIPE`, `BASE_BUBPIPE`, `BASE_BUBPIPE_S`, `BASE_BUBPIPE_L`, `BASE_BUBPIPE_T`, and `BASE_BUBPIPE_X` in straight, elbow, T, X, and mixed runs. Must compare Blender, in-game screenshot, and exported JSON if possible.

Known issue: RX90 appears to help individual pipe parts, but connected bends do not reliably appear connected/bending in Blender. Need determine local vs global correction.


## Closed / superseded in 3.01.02

- PIPE/BUBPIPE generic validation exception refined into contextual connector rule with JSON transform evidence. Remaining topic: focused pipe harness still needed before using complex pipe assemblies in a flagship build.
