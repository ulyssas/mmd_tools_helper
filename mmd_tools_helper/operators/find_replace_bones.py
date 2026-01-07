import re

import bpy

from .. import model, register_wrap


def main(context):
    replace_count = 0
    context.view_layer.objects.active = model.findArmature(context.active_object)

    for b in context.active_object.data.bones:
        if context.scene.bones_all_or_selected and not b.select:
            continue
        if "dummy" not in b.name and "shadow" not in b.name:
            if context.scene.use_regex:
                b.name = re.sub(
                    context.scene.find_bone_string, context.scene.replace_bone_string, b.name
                )
            else:
                b.name = b.name.replace(
                    context.scene.find_bone_string,
                    context.scene.replace_bone_string,
                )
            replace_count += 1

    return replace_count


@register_wrap
class FindReplaceBones(bpy.types.Operator):
    bl_idname = "mmd_tools_helper.find_replace_bones"
    bl_label = "Find and replace bone names"
    bl_description = "Find and replace strings in bone names"
    bl_options = {"REGISTER", "UNDO"}

    bpy.types.Scene.find_bone_string = bpy.props.StringProperty(
        name="From",
        description="",
        default="",
    )

    bpy.types.Scene.replace_bone_string = bpy.props.StringProperty(
        name="To",
        description="",
        default="",
    )

    bpy.types.Scene.bones_all_or_selected = bpy.props.BoolProperty(
        name="Selected bones only",
        description="",
        default=False,
    )

    bpy.types.Scene.use_regex = bpy.props.BoolProperty(
        name="Use Regular Expression",
        description="",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        if context.mode not in {"OBJECT", "POSE"}:
            return False

        active_object = context.active_object

        if active_object is None:
            return False

        return model.findRoot(active_object) is not None

    def execute(self, context):
        previous_mode = context.mode

        try:
            replace_count = main(context)
            self.report({"INFO"}, message=f"Replaced {replace_count} entries")
        except Exception as e:
            self.report({"ERROR"}, message=f"Failed to find and replace bones: {e}")
            return {"CANCELLED"}
        finally:
            bpy.ops.object.mode_set(mode=previous_mode)
        return {"FINISHED"}
