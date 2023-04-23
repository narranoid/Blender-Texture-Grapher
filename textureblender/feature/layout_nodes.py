
from bpy.props import EnumProperty, FloatVectorProperty

from .. import node_util as nu
from ..node_layout import NodeLayout


class LayoutNodesFeature:
    node_layout: EnumProperty(
        name="Node Layout",
        description="How are nodes layout?",
        items=[
            (NodeLayout.DUAL_STEP.name, "Dual Step", "Nodes are placed stepped in two columns"),
            (NodeLayout.SINGLE_COLUMN.name, "Single Column", "Nodes are placed in a single column"),
            (NodeLayout.SQUARE.name, "Square", "Nodes are palced in a square")
        ]
    )

    node_padding: FloatVectorProperty(
        name='Padding ',
        description='X/Y padding between each node',
        default=(20.0, 20.0),
        min=0.0,
        soft_min=0.0,
        options=set(),
        size=2,
        subtype='XYZ'
    )

    def draw_layout_nodes(self, context, operator, layout):
        layout.prop(operator, 'node_layout')
        layout.prop(operator, 'node_padding')

    def sorted(self, nodes):
        return nodes

    def layout_nodes(self, node_tree, nodes, center=None):
        layout = NodeLayout[self.node_layout]
        padding = self.node_padding

        # if there are no nodes, don't layout
        if len(nodes) <= 1:
            return

        nu.layout_nodes(self.sorted(nodes), layout, padding_x=padding[0], padding_y=padding[1], center=center)
