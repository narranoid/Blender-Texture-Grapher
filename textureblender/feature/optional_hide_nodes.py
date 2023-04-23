
from bpy.props import BoolProperty

from .hide_nodes import HideNodesFeature


class OptionalHideNodesFeature(HideNodesFeature):
    hide_nodes_option: BoolProperty(
        name='Hide Nodes',
        description='Hide all created nodes',
        default=False
    )

    def hide_nodes_optional(self, nodes):
        self.hide_nodes(nodes, self.hide_nodes_option)

