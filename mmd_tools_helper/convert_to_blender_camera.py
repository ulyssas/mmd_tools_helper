import bpy

from . import register_wrap


@register_wrap
class MMDCameraToBlenderPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_mmd_camera_to_blender_camera"
    bl_label = "MMD Camera to Blender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Helper"

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row = layout.row()
        row.operator("mmd_tools_helper.mmd_camera_to_blender", text="Convert MMD Camera")
        row = layout.row()


def main(context):
    for o in bpy.context.scene.objects:
        if o.type == "CAMERA":
            camera = o
            camera.lock_location[0] = False
            camera.lock_location[1] = False
            camera.lock_location[2] = False
            camera.lock_rotation[0] = False
            camera.lock_rotation[1] = False
            camera.lock_rotation[2] = False
            camera.lock_scale[0] = False
            camera.lock_scale[1] = False
            camera.lock_scale[2] = False

            if o.animation_data is not None:
                for d in o.animation_data.drivers:
                    d.mute = True

    if camera.parent is not None:
        if camera.parent.mmd_type == "CAMERA":
            bpy.context.collection.objects.unlink(camera.parent)
            bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")


@register_wrap
class MMDCameraToBlender(bpy.types.Operator):
    bl_idname = "mmd_tools_helper.mmd_camera_to_blender"
    bl_label = "Convert MMD Camera to Blender"
    bl_description = "Convert MMD camera to Blender camera"
    bl_options = {"REGISTER", "UNDO"}

    # @classmethod
    # def poll(cls, context):
    # return context.active_object is not None

    def execute(self, context):
        main(context)
        return {"FINISHED"}
