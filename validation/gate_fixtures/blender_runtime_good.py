import bpy
from bl_ext.user_default.no_mans_sky_base_builder import BUILDER
created = BUILDER.add_part("S_FLOOR")
obj = getattr(created, "object", created)
bpy.context.collection.objects.link(obj)
