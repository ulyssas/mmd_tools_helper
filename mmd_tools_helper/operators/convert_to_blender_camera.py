import bpy

from .. import model, register_wrap


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

    @classmethod
    def poll(cls, context):
        if context.mode not in {"OBJECT", "POSE"}:
            return False

        active_object = context.active_object

        if active_object is None:
            return False

        return model.findCamera(active_object) is not None

    def execute(self, context):
        previous_mode = context.mode

        try:
            main(context)
        except Exception as e:
            self.report({"ERROR"}, message=f"Failed to convert MMD camera: {e}")
            return {"CANCELLED"}
        finally:
            bpy.ops.object.mode_set(mode=previous_mode)
        return {"FINISHED"}
