
from bpy.types import Operator

from .. import node_util as nu
from ..feature import LayoutExistingNodesFeature


class LayoutNodesOperator(Operator, LayoutExistingNodesFeature):

    bl_idname = "texture_grapher.layout_nodes"
    bl_label = "Layout Nodes"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Texture Grapher"

    #hide_nodes: BoolProperty(
    #    name='Hide Nodes',
    #    description='Hide all created nodes',
    #    default=True
    #)

    def __init__(self):
        Operator.__init__(self)
        LayoutExistingNodesFeature.__init__(self)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout.column(align=True)
        self.draw_layout_nodes(context, self, layout)

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        all_nodes = node_tree.nodes
        tex_nodes = nu.get_selected(all_nodes)
        self.layout_nodes(node_tree, tex_nodes)

        return {'FINISHED'}
