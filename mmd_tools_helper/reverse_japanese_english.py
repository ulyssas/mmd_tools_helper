import bpy

from . import register_wrap


@register_wrap
class SwapJapaneseEnglishPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_reverse_japanese_english"
    bl_label = "Swap Japanese & English names"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.label(text="Swap Japanese & English names", icon="TEXT")
        row = layout.row()
        row.operator("mmd_tools_helper.swap_japanese_english", text="Swap Japanese & English")
        row = layout.row()


def main(context):
    for m in bpy.data.materials:
        name_j = m.mmd_material.name_j
        name_e = m.mmd_material.name_e
        if name_e != "":
            m.mmd_material.name_e = name_j
            m.mmd_material.name_j = name_e
            m.mmd_material.name = name_e

    for m in bpy.data.materials:
        m.name = m.mmd_material.name

    for o in bpy.context.scene.objects:
        if o.type == "ARMATURE":
            o.data.show_names = True
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.mode_set(mode="POSE")
            for b in bpy.context.active_object.pose.bones:
                name_j = b.mmd_bone.name_j
                name_e = b.mmd_bone.name_e
                if name_e != "":
                    b.mmd_bone.name_j = name_e
                    b.mmd_bone.name_e = name_j
                    b.name = name_e

    bpy.ops.object.mode_set(mode="OBJECT")

    for o in bpy.context.scene.objects:
        if o.mmd_type == "ROOT":
            for vm in o.mmd_root.vertex_morphs:
                name_j = vm.name
                name_e = vm.name_e
                if name_e != "":
                    vm.name = name_e
                    vm.name_e = name_j


@register_wrap
class SwapJapaneseEnglish(bpy.types.Operator):
    bl_idname = "mmd_tools_helper.swap_japanese_english"
    bl_label = "Swap Japanese and English names"
    bl_description = "Swap Japanese and English names of shape keys, materials, bones"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        main(context)
        return {"FINISHED"}
