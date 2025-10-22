bl_info = {
    "name": "MMD Tools Helper",
    "author": "Hogarth-MMD",
    "version": (2, 4),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > MMD Tools Helper",
    "description": "various mmd_tools helper scripts",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

__bl_classes = []


def register_wrap(cls):
    # print('%3d'%len(__bl_classes), cls)
    # assert(cls not in __bl_classes)
    if __make_annotations:
        bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, __bpy_property)}
        if bl_props:
            if "__annotations__" not in cls.__dict__:
                setattr(cls, "__annotations__", {})
            annotations = cls.__dict__["__annotations__"]
            for k, v in bl_props.items():
                # print('   -', k, v)
                # assert(v.__class__.__name__ == '_PropertyDeferred' or getattr(v[0], '__module__', None) == 'bpy.props' and isinstance(v[1], dict))
                annotations[k] = v
                delattr(cls, k)
    if hasattr(cls, "bl_rna"):
        __bl_classes.append(cls)
    return cls


if "bpy" in locals():
    if bpy.app.version < (2, 71, 0):
        import imp as importlib
    else:
        import importlib
    importlib.reload(add_arm_ik)
    importlib.reload(add_leg_ik)
    importlib.reload(armature_diagnostic)
    importlib.reload(batch_bone_rename)
    importlib.reload(convert_to_blender_camera)
    importlib.reload(display_frame_groups)
    importlib.reload(find_replace_bones)
    importlib.reload(miscellaneous_tools)
    importlib.reload(model)
    importlib.reload(swap_japanese_english)
    importlib.reload(toon_tex_to_shader)
else:
    import logging

    import bpy

    __make_annotations = bpy.app.version >= (2, 80, 0)
    __bpy_property = bpy.props._PropertyDeferred if hasattr(bpy.props, "_PropertyDeferred") else tuple
    from . import (
        add_arm_ik,
        add_leg_ik,
        armature_diagnostic,
        batch_bone_rename,
        convert_to_blender_camera,
        display_frame_groups,
        find_replace_bones,
        miscellaneous_tools,
        model,
        swap_japanese_english,
        toon_tex_to_shader,
    )

if bpy.app.version < (2, 80, 0):
    bl_info["blender"] = (2, 70, 0)

logging.basicConfig(format="%(message)s", level=logging.DEBUG)


@register_wrap
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


def register():
    for cls in __bl_classes:
        bpy.utils.register_class(cls)
    print(__name__, "registed %d classes" % len(__bl_classes))


def unregister():
    for cls in reversed(__bl_classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
