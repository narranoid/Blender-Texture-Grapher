
from bpy.types import Operator, Panel, Menu
from ..ops import ConnectActiveToSelectedOperator, ConnectSelectedToActiveOperator


class ConnectNodesPanel(Panel):
    bl_label = "Connect Nodes"
    bl_idname = "NODE_PT_texture_grapher_connect_nodes"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Texture Grapher"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ShaderNodeTree'

    def draw(self, context):
        layout = self.layout.column(align=True)
        layout.operator(ConnectSelectedToActiveOperator.bl_idname, icon='NODE_SEL')
        layout.operator(ConnectActiveToSelectedOperator.bl_idname, icon='NODE_SEL')



