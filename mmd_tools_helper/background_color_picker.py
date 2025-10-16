import sys

import bpy


class MMDBackgroundColorPicker_Panel(bpy.types.Panel):
    """Selects world background color and a contrasting text color"""

    bl_idname = "OBJECT_PT_mmd_background_color_picker"
    bl_label = "MMD background color picker"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row = layout.row()
        layout.prop(context.scene, "BackgroundColor")
        row.operator(
            "mmd_tools_helper.background_color_picker",
            text="MMD background color picker",
        )
        row = layout.row()


def main(context):
    screens = ["Animation", "Scripting", "UV Editing", "Layout"]

    for screen in screens:
        if screen in bpy.data.screens:
            for area in bpy.data.screens[screen].areas:
                if area.type == "VIEW_3D":
                    for space in area.spaces:
                        if space.type == "VIEW_3D":
                            space.shading.background_type = "WORLD"

    if bpy.context.view_layer.world:
        bpy.context.view_layer.world.color = bpy.context.view_layer.BackgroundColor

    theme = bpy.context.preferences.themes[0]
    theme.view_3d.space.text_hi = (
        round(1 - bpy.context.view_layer.BackgroundColor[0]),
        round(1 - bpy.context.view_layer.BackgroundColor[1]),
        round(1 - bpy.context.view_layer.BackgroundColor[2]),
    )


class MMDBackgroundColorPicker(bpy.types.Operator):
    """Selects world background color and a contrasting text color"""

    bl_idname = "mmd_tools_helper.background_color_picker"
    bl_label = "MMD background color picker"

    bpy.types.Scene.BackgroundColor = bpy.props.FloatVectorProperty(
        name="Background Color",
        description="Set world background color",
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        soft_min=0.0,
        soft_max=1.0,
        step=3,
        precision=2,
        options={"ANIMATABLE"},
        subtype="COLOR",
        unit="NONE",
        size=3,
        update=None,
        get=None,
        set=None,
    )

    def execute(self, context):
        main(context)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(MMDBackgroundColorPicker)
    bpy.utils.register_class(MMDBackgroundColorPicker_Panel)


def unregister():
    bpy.utils.unregister_class(MMDBackgroundColorPicker)
    bpy.utils.register_class(MMDBackgroundColorPicker_Panel)


if __name__ == "__main__":
    register()
