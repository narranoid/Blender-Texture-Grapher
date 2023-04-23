from ..ops import ImageNodeFileImporter, FrameImageSetOperator, GroupImageSetOperator

from bpy.types import Operator, Panel, Menu
from bpy.props import (
    FloatProperty,
    EnumProperty,
    BoolProperty,
    IntProperty,
    StringProperty,
    FloatVectorProperty,
    CollectionProperty,
)


def drawlayout(context, layout, mode='non-panel'):
    tree_type = context.space_data.tree_type
    col = layout.column(align=True)

    if tree_type == 'ShaderNodeTree':  # and is_cycles_or_eevee(context):
        pass

    #col = layout.column(align=True)
    col.operator(ImageNodeFileImporter.bl_idname, icon='NODE_SEL')
    col.operator(FrameImageSetOperator.bl_idname, icon='NODE_SEL')
    col.operator(GroupImageSetOperator.bl_idname, icon='NODE_SEL')

    # add operator
    col.separator()


class TextureSetSetupPanel(Panel):
    bl_idname = "NODE_PT_texture_grapher_textureset_setup_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Texture Set Setup"
    bl_region_type = "UI"
    bl_category = "Texture Grapher"

    prepend: StringProperty(
        name='prepend',
    )
    append: StringProperty()
    remove: StringProperty()

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        #self.layout.label(text="(Quick access: Shift+W)")
        drawlayout(context, self.layout, mode='panel')

