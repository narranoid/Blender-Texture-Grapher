
import bpy

from .. import node_util as nu

class GroupNodesFeature:

    def make_group(self, texture_set_characterization, node_tree, nodes=None, set_group_node_active=False, select_group_node=False, select_nodes_in_group=False, enter_group=False):
        if not nodes:
            nodes = texture_set_characterization.get_nodes_in_tree(node_tree)
        if len(nodes) <= 0:
            return None

        previous_selection = nu.get_selected(nodes)
        previous_active = node_tree.nodes.active
        group = None
        group_node = None

        try:
            nu.select_nodes(previous_selection, select=False)
            nu.select_nodes(nodes, select=True)

            bpy.ops.node.group_make()
            group_node = node_tree.nodes.active
            group = group_node.node_tree

            # remove auto generated sockets
            input_sockets = list()
            for input in group.inputs:
                input_sockets.append(input)
            for input in input_sockets:
                group.inputs.remove(input)
            output_sockets = list()
            for output in group.outputs:
                output_sockets.append(output)
            for output in output_sockets:
                group.outputs.remove(output)

        finally:
            if group_node is not None:  # TODO: add condition to check for proper context
                bpy.ops.node.group_edit(exit=not enter_group)

            # restore previous selection
            if nodes:
                nu.select_nodes(nodes, select=False)
            if previous_selection:
                for prev_sel in previous_selection:
                    if group is None or prev_sel.name not in group.nodes:
                        prev_sel.select = True

            # make new selection and restore active node
            if group is not None:
                nu.select_nodes(group.nodes, select=select_nodes_in_group)
            if group_node is not None:
                group_node.select = select_group_node
                if set_group_node_active:
                    node_tree.nodes.active = group_node
                elif previous_active is not None and previous_active.name not in group.nodes:
                    node_tree.nodes.active = previous_active
            elif previous_active is not None and previous_active.name not in group.nodes:
                node_tree.nodes.active = previous_active

        return group_node



    def insert_into_group(self):
        pass
