import bpy

from .. import model, register_wrap


def main(context):
    bpy.context.view_layer.objects.active = model.findArmature(bpy.context.active_object)
    if bpy.context.scene.bones_all_or_selected:
        for b in bpy.context.active_object.data.bones:
            if b.select:
                if "dummy" not in b.name and "shadow" not in b.name:
                    b.name = b.name.replace(
                        bpy.context.scene.find_bone_string,
                        bpy.context.scene.replace_bone_string,
                    )
    if not bpy.context.scene.bones_all_or_selected:
        for b in bpy.context.active_object.data.bones:
            if "dummy" not in b.name and "shadow" not in b.name:
                b.name = b.name.replace(
                    bpy.context.scene.find_bone_string,
                    bpy.context.scene.replace_bone_string,
                )


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
        maxlen=0,
        options={"ANIMATABLE"},
        subtype="NONE",
        update=None,
        get=None,
        set=None,
    )

    bpy.types.Scene.replace_bone_string = bpy.props.StringProperty(
        name="To",
        description="",
        default="",
        maxlen=0,
        options={"ANIMATABLE"},
        subtype="NONE",
        update=None,
        get=None,
        set=None,
    )

    bpy.types.Scene.bones_all_or_selected = bpy.props.BoolProperty(
        name="Selected bones only",
        description="",
        default=False,
        options={"ANIMATABLE"},
        subtype="NONE",
        update=None,
        get=None,
        set=None,
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
            main(context)
        except Exception as e:
            self.report({"ERROR"}, message=f"Failed to find and replace bones: {e}")
            return {"CANCELLED"}
        finally:
            bpy.ops.object.mode_set(mode=previous_mode)
        return {"FINISHED"}
