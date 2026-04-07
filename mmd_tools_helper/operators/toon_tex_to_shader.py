import colorsys

import bpy
from mathutils import Vector

from .. import model, register_wrap

# Each image is a list of numbers(floats): R,G,B,A,R,G,B,A etc.
# So the length of the list of pixels is 4 X number of pixels
# pixels are in left-to-right rows from bottom left to top right of image


def toon_image_to_color_ramp(toon_tex_color_ramp, toon_tex_node):
    """Converts toon texture to monochrome color ramp. Returns start color for use in multiply_color."""

    def rgb_to_monochrome(colors, brightness=None):
        """colors: list[r, g, b, a], brightness: float (for setting brightness)"""

        r, g, b, _ = colors
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        if s > 0:
            v = 1.0 - s
        s = 0.0
        if brightness is not None:
            v = brightness
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return [r, g, b, 1.0]

    def get_rgb_brightness(colors):
        r, g, b, _ = colors
        _, _, v = colorsys.rgb_to_hsv(r, g, b)
        return v

    toon_image = toon_tex_node.image
    width, height = toon_image.size

    pixels_rgba = []
    sample_count = 32
    step = max(1, height // sample_count)
    for y in range(0, height, step):
        idx = (y * width + width // 2) * 4
        pixels_rgba.append(toon_image.pixels[idx : idx + 4])

    start_color = pixels_rgba[0]
    end_color = pixels_rgba[-1]

    mono_toon_gradient = [rgb_to_monochrome(c) for c in pixels_rgba]

    # normalize gradient (start color to black)
    b_start = get_rgb_brightness(mono_toon_gradient[0])
    if b_start < 1:
        b_multiplier = 1 / (1 - b_start)
        for i, s in enumerate(mono_toon_gradient):
            normal_dimness = (1 - get_rgb_brightness(s)) * b_multiplier
            mono_toon_gradient[i] = rgb_to_monochrome(s, 1 - normal_dimness)

    # reset color ramp
    cr = toon_tex_color_ramp.color_ramp
    cr.interpolation = "LINEAR"
    while len(cr.elements) > 1:
        cr.elements.remove(cr.elements[-1])

    offset = 1 / (len(mono_toon_gradient) - 1)
    for i, shade in enumerate(mono_toon_gradient):
        pos = i * offset
        s = cr.elements.new(pos) if i > 0 else cr.elements[0]
        s.color = shade

    return start_color


def clear_nodes(nodes: bpy.types.Nodes, keep_uv: bool = True):
    """Remove all nodes except specified types (image texture) from the node tree."""
    # specify node types to keep
    keep_types = {"ShaderNodeTexImage"}

    for node in list(nodes):
        if keep_uv and node.name == "mmd_tex_uv":
            continue
        if node.bl_idname not in keep_types:
            nodes.remove(node)


def main(context, clear_node=True, keep_sphere=True):
    o: bpy.types.Object = context.active_object
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

            # for adding shading color
            mmd_base_tex = nodes.get("mmd_base_tex")
            mmd_toon_tex = nodes.get("mmd_toon_tex")
            mmd_sphere_tex = nodes.get("mmd_sphere_tex")
            mult_shade_color = nodes.new(type="ShaderNodeMixRGB")
            mult_shade_color.blend_type = "MULTIPLY"
            mult_shade_color.inputs[0].default_value = 1.0
            shade_color = nodes.new(type="ShaderNodeRGB")
            shade_color.label = "Shade Color"
            if mmd_toon_tex:
                shade_color.outputs[0].default_value = toon_image_to_color_ramp(
                    color_ramp, mmd_toon_tex
                )

            # sphere Add/Multiply
            if keep_sphere and mmd_sphere_tex:
                mix_sphere = nodes.new(type="ShaderNodeMixRGB")
                mix_sphere.blend_type = {"1": "MULTIPLY", "2": "ADD"}.get(
                    m.mmd_material.sphere_texture_type, "MULTIPLY"
                )
                mix_sphere.inputs[0].default_value = 1.0

            # for no-shade material
            mix_toon_ramp = nodes.new(type="ShaderNodeMixRGB")
            mix_toon_ramp.blend_type = "MIX"
            emission = nodes.new(type="ShaderNodeEmission")

            # transparent cutout
            cutout_frame = nodes.new(type="NodeFrame")
            transparent = nodes.new(type="ShaderNodeBsdfTransparent")
            mix_alpha_shader = nodes.new(type="ShaderNodeMixShader")
            mix_alpha = nodes.new(type="ShaderNodeMath")
            mix_alpha.label = "Alpha"
            mix_alpha.operation = "MULTIPLY"
            mix_alpha.use_clamp = True
            mix_alpha.inputs[0].default_value = 1.0
            mix_alpha.inputs[1].default_value = m.mmd_material.alpha

            # edit node positions
            if mmd_base_tex:
                origin = mmd_base_tex.location.copy()
            else:
                origin = Vector([0, 0])
            if keep_sphere and mmd_sphere_tex:
                origin.x += 200

            diffuse.location = (origin[0] - 200, origin[1] + 300)
            shader_to_rgb.location = (diffuse.location[0] + 200, diffuse.location[1])
            color_ramp.location = (shader_to_rgb.location[0] + 200, shader_to_rgb.location[1])
            mix_toon_ramp.location = (color_ramp.location[0] + 300, color_ramp.location[1] - 100)
            mult_shade_color.location = (origin[0] + 300, origin[1])
            shade_color.location = (
                mult_shade_color.location[0],
                mult_shade_color.location[1] - 200,
            )
            emission.location = (mix_toon_ramp.location[0] + 200, mix_toon_ramp.location[1])
            transparent.location = (emission.location[0] + 250, origin[1])
            mix_alpha.location = (emission.location[0] + 250, emission.location[1])
            mix_alpha_shader.location = (transparent.location[0] + 200, emission.location[1])
            output.location = (mix_alpha_shader.location[0] + 200, mix_alpha_shader.location[1])
            if mmd_toon_tex:
                mmd_toon_tex.location = (origin[0] + 50, origin[1] - 300)
            if keep_sphere and mmd_sphere_tex:
                mix_sphere.location = (origin[0] + 100, origin[1])
                mmd_sphere_tex.location = (origin[0] - 200, origin[1] - 300)

            # Frame nodes
            toon_frame.label = "Toon Shading"
            diffuse.parent = toon_frame
            shader_to_rgb.parent = toon_frame
            color_ramp.parent = toon_frame
            mult_shade_color.parent = toon_frame
            shade_color.parent = toon_frame
            mix_toon_ramp.parent = toon_frame
            emission.parent = toon_frame
            if mmd_base_tex:
                mmd_base_tex.parent = toon_frame

            cutout_frame.label = "Texture Cutout & Alpha"
            transparent.parent = cutout_frame
            mix_alpha.parent = cutout_frame
            mix_alpha_shader.parent = cutout_frame

            # links
            links.new(diffuse.outputs[0], shader_to_rgb.inputs[0])
            links.new(shader_to_rgb.outputs[0], color_ramp.inputs[0])
            links.new(color_ramp.outputs[0], mix_toon_ramp.inputs[0])
            links.new(shade_color.outputs[0], mult_shade_color.inputs[2])
            links.new(mult_shade_color.outputs[0], mix_toon_ramp.inputs[1])
            links.new(mix_toon_ramp.outputs[0], emission.inputs[0])
            links.new(transparent.outputs[0], mix_alpha_shader.inputs[1])
            links.new(emission.outputs[0], mix_alpha_shader.inputs[2])
            links.new(mix_alpha.outputs[0], mix_alpha_shader.inputs[0])
            links.new(mix_alpha_shader.outputs[0], output.inputs[0])
            if keep_sphere and mmd_base_tex and mmd_sphere_tex:
                links.new(mmd_base_tex.outputs[0], mix_sphere.inputs[1])
                links.new(mmd_sphere_tex.outputs[0], mix_sphere.inputs[2])
                links.new(mix_sphere.outputs[0], mult_shade_color.inputs[1])
                links.new(mix_sphere.outputs[0], mix_toon_ramp.inputs[2])
                links.new(mmd_base_tex.outputs[1], mix_alpha.inputs[0])
            elif mmd_base_tex:
                links.new(mmd_base_tex.outputs[0], mix_toon_ramp.inputs[2])
                links.new(mmd_base_tex.outputs[0], mult_shade_color.inputs[1])
                links.new(mmd_base_tex.outputs[1], mix_alpha.inputs[0])

    return len(o.data.materials)


@register_wrap
class MMDToonTexToShader(bpy.types.Operator):
    bl_idname = "mmd_tools_helper.mmd_toon_shader"
    bl_label = "Convert MMD Toon to Toon Shader"
    bl_description = "Sets up nodes in Blender node editor for rendering toon textures"
    bl_options = {"REGISTER", "UNDO"}

    clear_node: bpy.props.BoolProperty(name="Clear existing nodes", default=True)
    keep_sphere: bpy.props.BoolProperty(name="Keep sphere", default=True)

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
            mesh_objects_list = model.find_MMD_MeshesList(context.active_object)
            assert mesh_objects_list is not None, "The active object is not an MMD model."
            for o in mesh_objects_list:
                context.view_layer.objects.active = o
                count = main(context, self.clear_node, self.keep_sphere)
            self.report({"INFO"}, message=f"Converted {count} materials")
        except Exception as e:
            self.report({"ERROR"}, message=f"Failed to add toon shaders: {e}")
            return {"CANCELLED"}
        finally:
            bpy.ops.object.mode_set(mode=previous_mode)
        return {"FINISHED"}
