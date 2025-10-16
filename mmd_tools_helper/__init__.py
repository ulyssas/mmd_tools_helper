import bpy

from . import (
    add_foot_leg_ik,
    add_hand_arm_ik,
    armature_diagnostic,
    background_color_picker,
    blender_bone_names_to_japanese_bone_names,
    boneMaps_renamer,
    convert_to_blender_camera,
    display_panel_groups,
    miscellaneous_tools,
    mmd_lamp_setup,
    mmd_view,
    model,
    replace_bones_renaming,
    reverse_japanese_english,
    toon_modifier,
    toon_textures_to_node_editor_shader,
)

bl_info = {
    "name": "MMD Tools Helper",
    "author": "Hogarth-MMD",
    "version": (2, 4),
    "blender": (4, 1, 0),
    "location": "View3D > Sidebar > MMD Tools Helper",
    "description": "various mmd_tools helper scripts",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}


class MMDToolsHelperPanel(bpy.types.Panel):
    """Creates the MMD Tools Helper Panel in a VIEW_3D TOOLS tab"""

    bl_label = "MMD Tools Helper"
    bl_idname = "OBJECT_PT_mmd_tools_helper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()


import importlib

modules = [
    model,
    mmd_view,
    mmd_lamp_setup,
    convert_to_blender_camera,
    background_color_picker,
    boneMaps_renamer,
    replace_bones_renaming,
    armature_diagnostic,
    add_foot_leg_ik,
    add_hand_arm_ik,
    display_panel_groups,
    toon_textures_to_node_editor_shader,
    toon_modifier,
    reverse_japanese_english,
    miscellaneous_tools,
    blender_bone_names_to_japanese_bone_names,
]

for m in modules:
    importlib.reload(m)


def register():
    for m in modules:
        if hasattr(m, "register"):
            m.register()
    bpy.utils.register_class(MMDToolsHelperPanel)


def unregister():
    for m in reversed(modules):
        if hasattr(m, "unregister"):
            m.unregister()
    bpy.utils.unregister_class(MMDToolsHelperPanel)


if __name__ == "__main__":
    register()
