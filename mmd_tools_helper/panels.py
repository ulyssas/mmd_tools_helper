import bpy

from . import register_wrap
from .operators import (
    AddMMDArmIK,
    AddMMDLegIK,
    ArmatureDiagnostic,
    BatchBoneRename,
    FindReplaceBones,
    MiscellaneousTools,
    MMDCameraToBlender,
    MMDToonTexToShader,
    SwapJapaneseEnglish,
)


@register_wrap
class HelperBoneToolsPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_bone_tools"
    bl_label = "MMD Helper Bone Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text="IK Makers", icon="OUTLINER_OB_ARMATURE")
        grid = col.grid_flow(row_major=True, align=True)
        grid.row(align=True).operator(AddMMDLegIK.bl_idname, text="Add leg IK")
        grid.row(align=True).operator(AddMMDArmIK.bl_idname, text="Add arm IK")

        row = layout.row(align=True)
        row.label(text="Armature Diagnostic", icon="TOOL_SETTINGS")
        layout.prop(context.scene, "selected_armature_to_diagnose")
        layout.operator(ArmatureDiagnostic.bl_idname, text="Diagnose armature")


@register_wrap
class HelperRenameToolsPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_rename_tools"
    bl_label = "MMD Helper Rename Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.label(text="Replace bone names", icon="ARMATURE_DATA")
        layout.prop(context.scene, "find_bone_string")
        layout.prop(context.scene, "replace_bone_string")
        layout.prop(context.scene, "bones_all_or_selected")
        layout.prop(context.scene, "use_regex")
        layout.operator(FindReplaceBones.bl_idname, text="Find & replace string in bone names")

        row = layout.row(align=True)
        row.label(text="Batch rename bones", icon="ARMATURE_DATA")
        layout.prop(context.scene, "origin_armature_type")
        layout.prop(context.scene, "destination_armature_type")
        layout.operator(BatchBoneRename.bl_idname, text="Batch rename bones")

        row = layout.row(align=True)
        row.label(text="Swap Japanese & English names", icon="TEXT")
        layout.operator(SwapJapaneseEnglish.bl_idname, text="Swap Japanese & English")


@register_wrap
class HelperMiscToolsPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_misc_tools"
    bl_label = "MMD Helper Misc Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.label(text="MMD Camera to Blender", icon="TEXT")
        layout.operator(MMDCameraToBlender.bl_idname, text="Convert MMD Camera")

        row = layout.row(align=True)
        row.label(text="MMD Toon to Toon Shader", icon="MATERIAL")
        layout.operator(MMDToonTexToShader.bl_idname, text="Convert to Toon Shader")

        row = layout.row(align=True)
        row.label(text="Miscellaneous Tools", icon="WORLD_DATA")
        layout.prop(context.scene, "selected_misc_tools")
        layout.operator(MiscellaneousTools.bl_idname, text="Execute")
