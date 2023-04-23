
import bpy
from bpy.types import Operator, ShaderNodeTree
from enum import Enum

from ..node_util import get_selected


class Projection(Enum):
    MIXED = 0
    FLAT = 1
    BOX = 2
    SPHERE = 3
    TUBE = 4


class Interpolation(Enum):
    Mixed = 0
    Linear = 1
    Closest = 2
    Cubic = 3
    Smart = 4


class Extension(Enum):
    MIXED = 0
    REPEAT = 1
    EXTEND = 2
    CLIP = 3


class ShaderTexImageMultiEditOperator(Operator):

    bl_idname = "texture_grapher.shader_tex_image_multi_edit"
    bl_label = "Multi-Edit Image Textures"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Texture Grapher"
    bl_options = {'REGISTER', 'UNDO'}

    projection: bpy.props.EnumProperty(items=((Projection.MIXED.name, 'Mixed', 'Mixed projections'),
                                               (Projection.FLAT.name, 'Flat', 'Image is projected flat using the X and Y coordinates of the texture vector'),
                                               (Projection.BOX.name, 'Box', 'Image is projected using different components for each side of the object space bounding box'),
                                               (Projection.SPHERE.name, 'Sphere', 'Image is projected spherically using the Z axis as central'),
                                               (Projection.TUBE.name, 'Tube', 'Image is projected from the tube using the Z axis as central')),
                                        name="Projection",
                                        options={'HIDDEN', 'SKIP_SAVE'})

    interpolation: bpy.props.EnumProperty(items=((Interpolation.Mixed.name, 'Mixed', 'Mixed interpolations'),
                                                  (Interpolation.Linear.name, 'Linear', 'Linear interpolation'),
                                                  (Interpolation.Closest.name, 'Closest', 'No interpolation (sample closest texel)'),
                                                  (Interpolation.Cubic.name, 'Cubic', 'Cubic interpolation'),
                                                  (Interpolation.Smart.name, 'Smart', 'Bicubic when magnifying, else bilinear (OSL only)')),
                                           name="Interpolation",
                                           options={'HIDDEN', 'SKIP_SAVE'})

    extension: bpy.props.EnumProperty(items=((Extension.MIXED.name, 'Mixed', 'Mixed extensions'),
                                              (Extension.REPEAT.name, 'Repeat', 'Cause the image to repeat horizontally and vertically'),
                                              (Extension.EXTEND.name, 'Extend', 'Extend by repeating edge pixels of the image'),
                                              (Extension.CLIP.name, 'Clip', 'Clip to image size and set exterior pixels as transparent')),
                                       name="Extension",
                                       options={'HIDDEN', 'SKIP_SAVE'})

    projection_blend: bpy.props.FloatProperty(name="Blend",
                                               soft_min=0.0,
                                               soft_max=1.0,
                                               subtype='FACTOR',
                                               precision=3,
                                               options={'HIDDEN', 'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return context.space_data is not None and isinstance(context.space_data.edit_tree, ShaderNodeTree)

    def __init__(self):
        super(ShaderTexImageMultiEditOperator, self).__init__()
        self.__contains_mixed_blend_values = False
        self.__contains_blendables = False
        self.__previous_projection_blend = 0.0

    def supports_projection_blend(self, node):
        return node.projection == Projection.BOX.name

    def update_properties(self, nodes):
        if len(nodes) > 0:
            self.__previous_projection_blend = self.projection_blend

            first_node = nodes.pop()
            projection_blend_uses = dict()

            self.projection = first_node.projection
            self.interpolation = first_node.interpolation
            self.extension = first_node.extension

            if self.supports_projection_blend(first_node):
                projection_blend_uses[first_node.projection_blend] = 1

            while nodes:
                current_node = nodes.pop()
                if self.projection != Projection.MIXED.name \
                        and current_node.projection != first_node.projection:
                    self.projection = Projection.MIXED.name
                if self.interpolation != Interpolation.Mixed.name \
                        and current_node.interpolation != first_node.interpolation:
                    self.interpolation = Interpolation.Mixed.name
                if self.extension != Extension.MIXED.name \
                        and current_node.extension != first_node.extension:
                    self.extension = Extension.MIXED.name
                if self.supports_projection_blend(current_node):
                    if current_node.projection_blend in projection_blend_uses:
                        projection_blend_uses[current_node.projection_blend] = \
                            projection_blend_uses[current_node.projection_blend] + 1
                    else:
                        projection_blend_uses[current_node.projection_blend] = 1

            # Assign utility flags
            self.__contains_mixed_blend_values = len(projection_blend_uses) > 1
            self.__contains_blendables = len(projection_blend_uses) > 0

            # Assign most frequently used projection blend value
            if self.__contains_mixed_blend_values:
                self.projection_blend = sorted(projection_blend_uses.items(), key=lambda x: x[1])[-1][0]
            elif self.__contains_blendables:
                self.projection_blend = list(projection_blend_uses.keys())[0]

    def set_node_values(self, image_node):
        if self.projection != Projection.MIXED.name:
            image_node.projection = self.projection
        if self.interpolation != Interpolation.Mixed.name:
            image_node.interpolation = self.interpolation
        if self.extension != Extension.MIXED.name:
            image_node.extension = self.extension
        if self.supports_projection_blend(image_node) and self.projection_blend != self.__previous_projection_blend:
            image_node.projection_blend = self.projection_blend

    def get_image_nodes(self, context):
        nodes = get_selected(context.space_data.edit_tree.nodes)
        image_nodes = list()
        for n in nodes:
            if n.bl_idname == 'ShaderNodeTexImage':
                image_nodes.append(n)
            elif n.bl_idname == 'ShaderNodeGroup':
                for subn in n.node_tree.nodes:
                    if subn.bl_idname == 'ShaderNodeTexImage':
                        image_nodes.append(subn)
        return image_nodes

    def invoke(self, context, event):
        nodes = self.get_image_nodes(context)

        if len(nodes) > 0:
            self.update_properties(nodes)
            self.__previous_projection_blend = self.projection_blend
            return context.window_manager.invoke_props_popup(self, event)

        self.report({'WARNING'}, "No Image Texture nodes found in selection!")
        return {'CANCELLED'}

    def execute(self, context):
        nodes = self.get_image_nodes(context)
        for n in nodes:
            self.set_node_values(n)
        return {'PASS_THROUGH'}

    def draw(self, context):
        nodes = self.get_image_nodes(context)

        if len(nodes) > 0:
            self.update_properties(list(nodes))
            layout = self.layout.column(align=True)

            layout.prop(self, "interpolation", expand=False)
            layout.separator()
            layout.prop(self, "projection", expand=False)
            layout.separator()

            if self.__contains_blendables:
                blend_text = "Blend (Mixed)" if self.__contains_mixed_blend_values else "Blend"
                layout.prop(self, "projection_blend", text=blend_text)
                layout.separator()

            layout.prop(self, "extension", expand=False)
        else:
            layout = self.layout.row()
            layout.label(text='An error occurred while reading node values!', icon='ERROR')
