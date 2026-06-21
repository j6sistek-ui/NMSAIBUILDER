# ONBOARDING VALIDATION BUILD

Purpose:
Bring a new chat up to speed by forcing it through one real, intentionally minimal build
before the first user build request. This is **not a simulation** — it is a real micro-build
and follows the full build process end-to-end, exactly like a user build request, just
deliberately small so it is quick.

Required onboarding workflow:
1. Review package doctrine and placement precedence.
2. Review the build packet workflow.
3. Review run_gate expectations.
4. Perform the validation micro-build through the full, real process.

Validation Build (intentionally minimal):
- Simple floor
- Simple wall
- Simple roof

Must produce the same artifacts any real build owes:
- placement authority summary
- build packet
- build sheet
- `run_gate` result — actually run `validation/run_gate.py` on the micro-build script and paste its output. Never a hand-typed PASS.
- `BUILD COMPLIANCE MANIFEST` summary (gate-verified via `validation/compliance_manifest_check.py`).

The AI must then summarize its understanding of:
- placement precedence
- the build packet workflow
- governance / evidence requirements

Only after the micro-build has passed its gates may the AI request the user's build objective.
