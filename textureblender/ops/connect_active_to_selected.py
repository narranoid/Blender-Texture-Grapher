

from bpy.types import Operator
from ..feature import ConnectNodesFeature


class ConnectActiveToSelectedOperator(Operator, ConnectNodesFeature):

    bl_idname = "texture_grapher.connect_active_to_selected"
    bl_label = "Connect Active to Selected"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Texture Grapher"

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        self.connect_active_to_selected(node_tree)
        return {'FINISHED'}
