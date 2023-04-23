

from bpy.types import Operator
from ..feature import ConnectNodesFeature


class ConnectSelectedToActiveOperator(Operator, ConnectNodesFeature):

    bl_idname = "texture_grapher.connect_selected_to_active"
    bl_label = "Connect Selected to Active"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Texture Grapher"

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        self.connect_selected_to_active(node_tree)
        return {'FINISHED'}
