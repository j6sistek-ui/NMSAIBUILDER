# Part Budget Optimization Protocol v49

## Purpose

A low part cap should guide final optimization, not prevent design discovery.

## Principle

```text
First make the build read correctly.
Then reduce cost by changing construction strategy.
```

## Recommended sequence

1. Build without hard part-count fear until the macro subject is recognizable.
2. Identify recognition-critical systems and freeze them.
3. Rank all parts by visual value:
   - critical silhouette
   - focal façade/detail
   - functional pathing/entrance
   - context/scene identity
   - low-value repetition
   - hidden/occluded construction
4. Remove or replace only the low-value/hidden groups first.
5. Use larger parts where they preserve the same visual read.
6. Re-test in Blender and in-game after each major reduction pass.

## Replacement examples from Taj

- Many plinth floor tiles → large `S_FLOOR` layers.
- Platform `S_WALLM` rows → removed, while `S_WALL_Q_H1` banding stayed.
- Dense dome socket tiles → one large buried/raised `S_ROOF5`.
- Full all-side detail → front/macro emphasis with simplified side/rear work.

## Do not do

- Do not delete the elements that make the subject recognizable.
- Do not optimize while the silhouette is still unresolved.
- Do not count hidden parts as harmless; hidden parts still consume budget.
- Do not flatten or simplify a system until it loses the target identity.
## budget/variety spectrum and in-place densification

- NMS renders flicker-free at roughly 4,000-5,000 parts; plan to that ceiling.
- Spectrum: hyper-dense low-variety showpieces (sword ~353, winged ~2,724) at one end; low-budget high-variety silhouette props (helicopter 68 parts / 37 types) at the other. Spend density only where it buys identity.
- In-place densification is cheap: adding segments at a fixed envelope/scale to close gaps (portal ring 12 -> 32, total 72 -> 192 structural parts) stays far under the flicker ceiling. Prefer adding count over enlarging parts when chasing solidity.
