# Technique Toolkit

This file provides reusable design techniques. It is not a hard rule file unless a technique has been promoted into `/rules`.

## Macro silhouette first

For landmark-scale builds, establish silhouette and major architectural masses before adding small details.

## Scale over quantity

When a build is grand or viewed from a distance, use larger scaled parts for recognisable features. Hundreds of tiny parts can disappear visually and add part count.

## Micro build mode

Micro builds and interiors can use dense, small, reinterpreted parts: books, tabletop games, centerpieces, shelving, appliances, counters, and props.

## Connected architecture

Arches, half arches, supports, trims, and walls should connect into an architectural system. Avoid partial features that hang in space without visual load path.

## Surface-oriented shelling

For domes/cones/spheres made from wall-like parts, orient pieces to the surface normal and tangent rather than stacking vertical bands.

## Partial burial

Objects may be sunk into floors, walls, or terrain so only the desired visible portion remains. Use this to solve scale/height conflicts and hide emitter bodies.

## Focal-zone detail

Put detail where the viewer recognises the subject. Do not fully detail hidden sides unless the build requires all-around viewing.

## v42 exploration toolkit
Use these techniques for broad experimental requests:

- **silhouette forcing:** assign each variant a different macro silhouette before selecting parts;
- **family rotation:** deliberately use different part families across variants;
- **comfort-motif audit:** remove repeated rings, lens bands, antenna crowns, and room stacks unless justified;
- **role labeling:** classify each part as structure, connector, lens, projector, data, robot, socket, silhouette, or FX;
- **screenshot pruning:** after review, preserve only variants that were screenshotted, praised, or clearly promising;
- **risk tiering:** label each variant as safe, refined, wildcard, FX-driven, structural, or sculptural.

## v53 JSON recreation technique
For existing-base repair/enhancement workflows, start from a JSON→Python recreation rather than rebuilding by design inference.

Technique:

```text
source JSON object
→ normalize ObjectID
→ duplicate real builder template
→ apply validated transform
→ preserve metadata
→ audit families/object IDs
```

If the replica overlays but a detail appears reversed, first test whether the validated universal local Y 180 was omitted before creating family-specific exceptions.

## v54 placement-recipe toolkit summary
Reusable modules now staged in `toolkit/PLACEMENT_RECIPE_LIBRARY.md` include:

- archive/book-spine texture wall;
- macro shell + detail overlay;
- Jurassic vehicle/jeep chassis;
- facility deck/elevated platform;
- lab display wall/screen grid;
- containment cylinder/specimen tank;
- pipe/rail/conduit path;
- vegetation zoning;
- gazebo/promenade row;
- social patio/seating cluster;
- compact 3x3x3 modular shell;
- curved/stepped arc from modular pieces;
- radial airlock/iris door;
- B_WNG_R teleporter/portal alcove variant;
- foosball/tabletop game assembly;
- fossil/skull façade marker;
- observation-window/red-wall lab façade;
- powerline hub/logic cluster.

These are recipes, not automatic decoration. Use only when they support the design intent.

## roof/spire placement primitives (from live build session)
Named recipes now in data/CREATIVE_USE_CASE_AND_STYLE_INDEX.json (offered via the packet CREATIVE_CONTEXT):

- **CONVERGING_RIB_CONE** — radial short-wall ribs (S_WALL_Q) chained end-to-end to ONE apex point. Cleanest spire found; double the rib count to close inter-rib gaps; half-scale walls + tighter base = tall pointy spire. Orientation: `rib_aim`.
- **CONVERGING_BEAM_CONE** — a single rim ring of SET_CLASS_* emitters each tilted to one apex = a true converging light cone in game. A/B/S are geometry-identical, color-only (magenta/blue/gold). Orientation: `aim_at_apex`.
- **COUNTER_CHEVRON_GAP_FILL** — close a floating base gap by snapping the same part to the drum and angling it OPPOSITE the spire's lean (chevron); same-angle extension reads unfinished.
- **SHINGLE_INFILL** — half-walls (S_WALLM_H) tiled between ribs with scale variation + azimuth stagger for overlap texture.
- **SOLID_FINIAL_CAP** — truncate facets BEFORE convergence, cap with a single un-stacked piece (anti-swirl).

Orientation recipes: `lean` (tangent tilt; negative=inward=clean, positive/outset=outward=spiky), `aim_at_apex` (-atan(radius/height) about tangent), `rib_aim` (align local X to apex direction, chain for length). API: .duplicate() objects are UNLINKED — must link to a collection.

Part-character cautions (see data/GEOMETRIC_FAILURE_MODE_INDEX.json): S_ROOF_M_WIN is a profiled tile that shingles (won't smooth — use a flat glass panel); S_LARGETRYE0 is a fan/star vault, NOT a clean point; _M diagonal walls need an N>=8 base (too wide for a small square).
