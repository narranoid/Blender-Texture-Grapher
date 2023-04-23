
from bpy.types import Operator, Panel, Menu
from ..ops import LayoutNodesOperator, HideNodesOperator, UnhideNodesOperator


class LayoutNodesPanel(Panel):
    bl_label = "Layout Nodes"
    bl_idname = "NODE_PT_texture_grapher_layout_nodes"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Texture Grapher"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout.column(align=True)
        layout.operator(LayoutNodesOperator.bl_idname, icon='NODE_SEL')
        layout.operator(HideNodesOperator.bl_idname, icon='NODE_SEL')
        layout.operator(UnhideNodesOperator.bl_idname, icon='NODE_SEL')



