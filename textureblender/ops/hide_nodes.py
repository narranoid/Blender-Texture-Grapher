
from bpy.types import Operator

from .. import node_util as nu
from ..feature import HideNodesFeature


class HideNodesOperator(Operator, HideNodesFeature):

    bl_idname = "texture_grapher.hide_selected_nodes"
    bl_label = "Hide Nodes"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Texture Grapher"

    def __init__(self):
        Operator.__init__(self)
        HideNodesFeature.__init__(self)

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        nodes = nu.get_selected(node_tree.nodes)

        self.hide_nodes(nodes, True)

        return {'FINISHED'}
