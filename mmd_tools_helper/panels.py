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
    MMDDisplayFrames,
    MMDToonTexToShader,
    SwapJapaneseEnglish,
)


@register_wrap
class AddMMDArmIKPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_add_arm_ik"
    bl_label = "Add arm IK to MMD model"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.label(text="Add arm IK to MMD model", icon="ARMATURE_DATA")
        row = layout.row()
        row.operator(AddMMDArmIK.bl_idname, text="Add arm IK")
        row = layout.row()


@register_wrap
class AddMMDLegIKPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_add_leg_ik"
    bl_label = "Add leg IK to MMD model"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.label(text="Add leg IK to MMD model", icon="ARMATURE_DATA")
        row = layout.row()
        row.operator(AddMMDLegIK.bl_idname, text="Add leg IK")
        row = layout.row()


@register_wrap
class ArmatureDiagnosticPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_armature_diagnostic"
    bl_label = "Armature Diagnostic"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Armature Diagnostic", icon="ARMATURE_DATA")
        row = layout.row()
        layout.prop(context.scene, "selected_armature_to_diagnose")
        row = layout.row()
        row.operator(ArmatureDiagnostic.bl_idname, text="Diagnose armature")
        row = layout.row()


@register_wrap
class BatchBoneRenamePanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_bone_batch_rename"
    bl_label = "Batch rename bones"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.label(text="Batch rename bones", icon="ARMATURE_DATA")
        row = layout.row()
        layout.prop(context.scene, "origin_armature_type")
        row = layout.row()
        layout.prop(context.scene, "destination_armature_type")
        row = layout.row()
        row.operator(BatchBoneRename.bl_idname, text="Batch rename bones")
        row = layout.row()


@register_wrap
class MMDCameraToBlenderPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_mmd_camera_to_blender"
    bl_label = "MMD Camera to Blender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row = layout.row()
        row.operator(MMDCameraToBlender.bl_idname, text="Convert MMD Camera")
        row = layout.row()


@register_wrap
class MMDDisplayFramesPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_add_display_frames"
    bl_label = "Display Frame"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.label(text="Display Frame", icon="ARMATURE_DATA")
        row = layout.row()
        layout.prop(context.scene, "display_panel_options")
        row = layout.row()
        row.operator(MMDDisplayFrames.bl_idname, text="Add display panel items")
        row = layout.row()


@register_wrap
class FindReplaceBonesPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_find_replace_bones"
    bl_label = "Replace String"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "find_bone_string")
        row = layout.row()
        row.prop(context.scene, "replace_bone_string")
        row = layout.row()
        row.prop(context.scene, "bones_all_or_selected")
        row = layout.row()
        row.label(text="Selected bones only")
        row = layout.row()
        row.operator(FindReplaceBones.bl_idname, text="Find & replace string in bone names")
        row = layout.row()


@register_wrap
class MiscellaneousToolsPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_misc_tools"
    bl_label = "Miscellaneous Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Miscellaneous Tools", icon="WORLD_DATA")
        row = layout.row()
        layout.prop(context.scene, "selected_misc_tools")
        row = layout.row()
        row.operator(MiscellaneousTools.bl_idname, text="Execute")


@register_wrap
class SwapJapaneseEnglishPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_swap_japanese_english"
    bl_label = "Swap Japanese & English names"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.label(text="Swap Japanese & English names", icon="TEXT")
        row = layout.row()
        row.operator(SwapJapaneseEnglish.bl_idname, text="Swap Japanese & English")
        row = layout.row()


@register_wrap
class MMDToonTexToShaderPanel(bpy.types.Panel):
    bl_idname = "MMD_HELPER_PT_mmd_toon_shader"
    bl_label = "MMD Toon to Toon Shader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.label(text="MMD Toon to Toon Shader", icon="MATERIAL")
        row = layout.row()
        row.operator(MMDToonTexToShader.bl_idname, text="Convert to Toon Shader")
        row = layout.row()
