"""
NMS_RUNTIME_OBJECT_AUDIT_SNIPPET.py

Add this to the end of generated NMS scripts. It verifies that built objects
are real NMS Base Builder objects with required custom properties.
"""

def nms_runtime_object_audit(tag):
    required = [
        "ObjectID",
        "SnapID",
        "Timestamp",
        "UserData",
        "order",
        "belongs_to_preset",
    ]
    built = [obj for obj in bpy.data.objects if obj.name.startswith(tag) and "_TPL_" not in obj.name]
    if not built:
        raise RuntimeError(f"NMS audit failed: no built objects found for tag {tag!r}.")

    failures = []
    for obj in built:
        missing = [key for key in required if key not in obj]
        if missing:
            failures.append((obj.name, missing))

    if failures:
        lines = ["NMS audit failed: built objects missing NMS custom properties."]
        for name, missing in failures[:25]:
            lines.append(f"  {name}: missing {', '.join(missing)}")
        if len(failures) > 25:
            lines.append(f"  ... and {len(failures) - 25} more")
        raise RuntimeError("\n".join(lines))

    print("=" * 72)
    print("NMS_OBJECT_AUDIT_PASS")
    print(f"Audited {len(built)} built NMS objects with tag {tag!r}.")
    print("=" * 72)

# Example call at the end of the script:
# nms_runtime_object_audit(TAG)
