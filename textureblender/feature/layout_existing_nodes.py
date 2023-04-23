
from bpy.props import BoolProperty

from .. import node_util as nu
from ..feature.layout_nodes import LayoutNodesFeature


class LayoutExistingNodesFeature(LayoutNodesFeature):
    prefer_nodes_over_frames: BoolProperty(
        name='Prefer Nodes Over Frames',
        description='Even if multiple frames are selected, prefer sorting their containing nodes per frame.',
        default=False
    )

    def draw_layout_nodes(self, context, operator, layout):
        super(LayoutExistingNodesFeature, self).draw_layout_nodes(context, operator, layout)
        layout.prop(operator, 'prefer_nodes_over_frames')

    def sorted(self, nodes):
        # sort by y, then by x position
        return sorted(nodes, key=lambda x: (-x.location[1], x.location[0]))

    def layout_nodes(self, node_tree, nodes, center=None):
        layouting_nodes = list(nodes)
        prefer_nodes = self.prefer_nodes_over_frames

        # if there are no nodes, don't layout
        if len(layouting_nodes) <= 0:
            return

        # if there is one node with children (a frame), layout the children
        if len(layouting_nodes) == 1:
            node_children = nu.get_children(layouting_nodes[0], node_tree.nodes)
            if len(node_children) > 1:
                layouting_nodes = node_children
            else:
                return

        # if there are multiple nodes, filter children
        if len(layouting_nodes) > 1 and self.prefer_nodes_over_frames:
            children_found = False
            for n in layouting_nodes:
                if nu.has_children(n, node_tree.nodes):
                    children_found = True
                    nodes_with_no_children_with_children = list()
                    find_children_with_no_children_recursive(n, node_tree.nodes, nodes_with_no_children_with_children)
                    for final_n in nodes_with_no_children_with_children:
                        ch = nu.get_children(final_n, node_tree.nodes)
                        super(LayoutExistingNodesFeature, self).layout_nodes(node_tree, ch, center=None)
            if not children_found:
                super(LayoutExistingNodesFeature, self).layout_nodes(node_tree, layouting_nodes, center=None)
        else:
            super(LayoutExistingNodesFeature, self).layout_nodes(node_tree, layouting_nodes, center=None)


def find_children_with_no_children_recursive(node, nodes, collector_list):
    result_nodes = list()
    children = nu.get_children(node, nodes)
    has_children_with_children = False
    for c in children:
        if nu.has_children(c, nodes):
            find_children_with_no_children_recursive(c, nodes, collector_list)
            if nu.has_children_with_children(c, nodes):
                has_children_with_children = True

    if not has_children_with_children:
        collector_list.append(node)