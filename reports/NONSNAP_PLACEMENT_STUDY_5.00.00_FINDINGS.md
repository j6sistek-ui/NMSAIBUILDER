# Non-Snap Placement Build Study — Findings (promoted in 5.00.00)

Live full-catalogue sweep via the add-on (ground-truth `part.serialise()` records
+ live geometry + live snap nature), reconciled against the verified part map.

- Catalogue swept: 2082 spawnable parts. Snap-enrolled (live): 955. Non-snap
  (live, `free_computed_placement_not_snappable`): 1127. The live snap count
  equals the verified part map's snap-enrolled count exactly.
- Geometry: of 1116 usable non-snap solids, 1116 agree with the verified part map
  to <=0.01u (joined on unique catalogue id). Validates both the live measurement
  and the stored map.
- Orientation: uniform NMS baseline Up~(0,1,0)/At~(0,0,1) for all parts except
  SET_LZ. No per-part build tilt; rx=90 is the Blender Z-up display conversion.
- Null placeholders (deterministic ~0.01u spawn) promoted to negative knowledge:
  FOS_LIMBS, FOS_SKULL, FOS_TAIL, SET_B_MONU_FA, SET_LZ, SET_SFXCONST_S0
  (CUBEWALL_SPACE, FRE_FACE_WALL, FRE_ROOM_IND1, PIPE already listed).
- Raw records and validated study live on the build machine under
  CLAUDE NMS REPOSITORY/runs/ (nonsnap_placement_study_v01*.json).

Validation tier: SCRIPT_VALIDATED / live-confirmed; in-game pending where noted.
