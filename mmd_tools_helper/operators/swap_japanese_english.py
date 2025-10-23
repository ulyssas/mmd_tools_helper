import bpy

from .. import model, register_wrap


def main(context, swap_mat=True, swap_bone=True, swap_morph=True):
    swap_count = 0
    if swap_mat:
        for m in bpy.data.materials:
            name_j = m.mmd_material.name_j
            name_e = m.mmd_material.name_e
            if name_e != "":
                m.mmd_material.name_e = name_j
                m.mmd_material.name_j = name_e
                m.mmd_material.name = name_e
                swap_count += 1

        for m in bpy.data.materials:
            m.name = m.mmd_material.name

    if swap_bone:
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
                        swap_count += 1

    bpy.ops.object.mode_set(mode="OBJECT")

    if swap_morph:
        for o in bpy.context.scene.objects:
            if o.mmd_type == "ROOT":
                for vm in o.mmd_root.vertex_morphs:
                    name_j = vm.name
                    name_e = vm.name_e
                    if name_e != "":
                        vm.name = name_e
                        vm.name_e = name_j
                        swap_count += 1

    return swap_count


@register_wrap
class SwapJapaneseEnglish(bpy.types.Operator):
    bl_idname = "mmd_tools_helper.swap_japanese_english"
    bl_label = "Swap Japanese and English names"
    bl_description = "Swap Japanese and English names of shape keys, materials, bones"
    bl_options = {"REGISTER", "UNDO"}

    swap_mat: bpy.props.BoolProperty(name="Swap material names", default=True)
    swap_bone: bpy.props.BoolProperty(name="Swap bone names", default=True)
    swap_morph: bpy.props.BoolProperty(name="Swap morph names", default=True)

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
            swap_count = main(context, self.swap_mat, self.swap_bone, self.swap_morph)
        except Exception as e:
            self.report({"ERROR"}, message=f"Failed to swap japanese and english names: {e}")
            return {"CANCELLED"}
        finally:
            self.report({"INFO"}, message=f"Swapped {swap_count} names")
            bpy.ops.object.mode_set(mode=previous_mode)
        return {"FINISHED"}
