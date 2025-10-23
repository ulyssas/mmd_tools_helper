import bpy

from .. import model, register_wrap

# Each image is a list of numbers(floats): R,G,B,A,R,G,B,A etc.
# So the length of the list of pixels is 4 X number of pixels
# pixels are in left-to-right rows from bottom left to top right of image


def toon_image_to_color_ramp(toon_texture_color_ramp, toon_image):
    pixels_width = toon_image.size[0]
    pixels_height = toon_image.size[1]
    toon_image_pixels = []
    toon_image_gradient = []

    for f in range(0, len(toon_image.pixels), 4):
        pixel_rgba = toon_image.pixels[f : f + 4]
        toon_image_pixels.append(pixel_rgba)

    for p in range(0, len(toon_image_pixels), int(len(toon_image_pixels) / 32)):
        toon_image_gradient.append(toon_image_pixels[p])

    toon_texture_color_ramp.color_ramp.elements[0].color = toon_image_gradient[0]
    toon_texture_color_ramp.color_ramp.elements[-1].color = toon_image_gradient[-1]

    for i in range(1, len(toon_image_gradient) - 2, 1):
        toon_texture_color_ramp.color_ramp.elements.new(i / (len(toon_image_gradient) - 1))
        toon_texture_color_ramp.color_ramp.elements[i].color = toon_image_gradient[i]
        if i > len(toon_image_gradient) / 2:
            toon_texture_color_ramp.color_ramp.elements[i].color[3] = 0.0  # alpha of non-shadow colors set to 0.0

    return


def clear_nodes(nodes):
    """Remove all nodes except specified types (image texture) from the node tree."""
    # specify node types to keep
    keep_types = {"ShaderNodeTexImage"}

    for node in list(nodes):
        if node.bl_idname not in keep_types:
            nodes.remove(node)


def main(context, clear_node=True):
    o = bpy.context.active_object
    if o.type != "MESH":
        return

    if o.data.materials is not None:
        for m in o.data.materials:
            m.use_nodes = True
            nodes = m.node_tree.nodes
            links = m.node_tree.links

            if clear_node:
                clear_nodes(nodes)

            output = nodes.get("Material Output")
            if output is None:
                output = nodes.new(type="ShaderNodeOutputMaterial")

            # basic toon shading
            toon_frame = nodes.new(type="NodeFrame")
            diffuse = nodes.new(type="ShaderNodeBsdfDiffuse")
            shader_to_rgb = nodes.new(type="ShaderNodeShaderToRGB")
            color_ramp = nodes.new(type="ShaderNodeValToRGB")
            color_ramp.color_ramp.interpolation = "CONSTANT"
            ramp = color_ramp.color_ramp
            if len(ramp.elements) < 2:
                while len(ramp.elements) < 2:
                    ramp.elements.new(1.0)
            ramp.elements[0].position = 0.0
            ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
            ramp.elements[1].position = 0.3
            ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)

            mmd_toon_tex = nodes.get("mmd_toon_tex")
            mmd_sphere_tex = nodes.get("mmd_sphere_tex")

            # for adding shading color
            mmd_base_tex = nodes.get("mmd_base_tex")
            multiply_color = nodes.new(type="ShaderNodeMixRGB")
            multiply_color.blend_type = "MULTIPLY"
            multiply_color.inputs[0].default_value = 1.0

            # for no-shade material
            mix_color = nodes.new(type="ShaderNodeMixRGB")
            mix_color.blend_type = "MIX"
            emission = nodes.new(type="ShaderNodeEmission")

            # transparent cutout
            cutout_frame = nodes.new(type="NodeFrame")
            transparent = nodes.new(type="ShaderNodeBsdfTransparent")
            mix_shader = nodes.new(type="ShaderNodeMixShader")

            # node positions
            if mmd_base_tex is not None:
                origin = mmd_base_tex.location
            else:
                origin = (0, 0)

            diffuse.location = (origin[0] - 200, origin[1] + 300)
            shader_to_rgb.location = (diffuse.location[0] + 200, diffuse.location[1])
            color_ramp.location = (shader_to_rgb.location[0] + 200, shader_to_rgb.location[1])
            mix_color.location = (color_ramp.location[0] + 300, color_ramp.location[1] - 100)
            multiply_color.location = (origin[0] + 300, origin[1])
            emission.location = (mix_color.location[0] + 200, mix_color.location[1])
            transparent.location = (emission.location[0] + 250, origin[1])
            mix_shader.location = (transparent.location[0] + 200, emission.location[1])
            output.location = (mix_shader.location[0] + 200, mix_shader.location[1])
            if mmd_toon_tex is not None:
                mmd_toon_tex.location = (origin[0], origin[1] - 300)
            if mmd_sphere_tex is not None:
                mmd_sphere_tex.location = (origin[0] + 300, origin[1] - 300)

            # Frame nodes
            toon_frame.label = "Toon Shading"
            diffuse.parent = toon_frame
            shader_to_rgb.parent = toon_frame
            color_ramp.parent = toon_frame
            multiply_color.parent = toon_frame
            mix_color.parent = toon_frame
            emission.parent = toon_frame
            if mmd_base_tex is not None:
                mmd_base_tex.parent = toon_frame

            cutout_frame.label = "Texture Cutout"
            transparent.parent = cutout_frame
            mix_shader.parent = cutout_frame

            # links
            links.new(diffuse.outputs[0], shader_to_rgb.inputs[0])
            links.new(shader_to_rgb.outputs[0], color_ramp.inputs[0])
            links.new(color_ramp.outputs[0], mix_color.inputs[0])
            links.new(multiply_color.outputs[0], mix_color.inputs[1])
            links.new(mix_color.outputs[0], emission.inputs[0])
            links.new(transparent.outputs[0], mix_shader.inputs[1])
            links.new(emission.outputs[0], mix_shader.inputs[2])
            links.new(mix_shader.outputs[0], output.inputs[0])
            if mmd_base_tex is not None:
                links.new(mmd_base_tex.outputs[0], mix_color.inputs[2])
                links.new(mmd_base_tex.outputs[0], multiply_color.inputs[1])
                links.new(mmd_base_tex.outputs[1], mix_shader.inputs[0])

    return len(o.data.materials)


@register_wrap
class MMDToonTexToShader(bpy.types.Operator):
    bl_idname = "mmd_tools_helper.mmd_toon_shader"
    bl_label = "Convert MMD Toon to Toon Shader"
    bl_description = "Sets up nodes in Blender node editor for rendering toon textures"
    bl_options = {"REGISTER", "UNDO"}

    clear_node: bpy.props.BoolProperty(name="Clear existing nodes", default=True)

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
            mesh_objects_list = model.find_MMD_MeshesList(bpy.context.active_object)
            assert mesh_objects_list is not None, "The active object is not an MMD model."
            for o in mesh_objects_list:
                bpy.context.view_layer.objects.active = o
                count = main(context, self.clear_node)
        except Exception as e:
            self.report({"ERROR"}, message=f"Failed to add toon shaders: {e}")
            return {"CANCELLED"}
        finally:
            self.report({"INFO"}, message=f"Converted {count} materials")
            bpy.ops.object.mode_set(mode=previous_mode)
        return {"FINISHED"}
