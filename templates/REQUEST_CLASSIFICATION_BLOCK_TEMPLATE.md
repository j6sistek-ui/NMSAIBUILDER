# Request Classification Block Template — 2.00.00

Use this block in generated scripts, major reports, and source-review patches so future chats and executable gates can see which rule bundle was selected.

```python
REQUEST_CLASSIFICATION = {
    "request_type": "build_generation | build_specific_addition | build_refinement_or_optimization | json_to_python_recreation | python_generated_json_audit | high_quality_source_json_recipe_mining | screenshot_or_ingame_evaluation | reference_image_or_external_example | source_doc_review_or_patch | protocol_correction_or_failure | script_debugging_or_error_log",
    "user_inputs": ["working_json", "python_script", "screenshots", "reference_image", "source_docs"],
    "rule_bundles_checked": [
        "UNIVERSAL_RULES",
        "REQUEST_ROUTER_CHECKLIST",
        "SYSTEMATIC_FAILURE_CAPA_PROTOCOL"
    ],
    "ambiguity_resolution": "not_needed | user_clarified | clarification_required_before_action",
    "json_evidence_used": False,
    "notes": "short explanation"
}
```
