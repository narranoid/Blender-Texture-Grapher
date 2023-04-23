
from bpy.types import Operator

from .. import node_util as nu
from .. import blender_texture_characterizer as btc
from .. import util as string_util
from ..feature import GroupNodesFeature
from ..string_source import StringSource


class GroupImageSetOperator(Operator, GroupNodesFeature):

    bl_idname = "texture_grapher.group_image_set"
    bl_label = "Group Texture Set"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Texture Grapher"

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        nodes = nu.get_selected(node_tree.nodes)

        if len(nodes) > 0:
            texture_characterizer = btc.init_characterizer()
            source = string_util.get_best_source(nodes, [StringSource.FILEPATH, StringSource.IMAGE_NAME],
                                                 StringSource.NAME)
            set_char = texture_characterizer.characterize_image_nodes(nodes, source)

            set_char.apply_image_settings()

            node_input_links = list()
            node_output_links = list()
            for link in node_tree.links:
                for n in nodes:
                    for input in n.inputs:
                        if link.to_socket == input:
                            node_input_links.append((link.from_socket, link.to_socket.name, link.to_node.name))
                    for output in n.outputs:
                        if link.from_socket == output:
                            node_output_links.append((link.from_socket.name, link.to_socket, link.from_node.name))

            group_node = set_char.group_nodes(node_tree, nodes=nodes,
                                              select_group_node=True,
                                              select_nodes_in_group=True,
                                              set_group_node_active=True,
                                              enter_group=False)
            group = group_node.node_tree
            nu.layout_input_output_nodes(group)
            set_char.setup_nodes_in_group(group)

            for from_socket, to_socket_name, grouped_node_name in node_input_links:
                grouped_node = group.nodes[grouped_node_name]
                to_socket = grouped_node.inputs[to_socket_name]
                group_node_to_socket = None

                for link in group.links:
                    if link.to_socket == to_socket and link.from_socket.name in group_node.inputs:
                        group_node_to_socket = group_node.inputs[link.from_socket.name]
                        break

                if group_node_to_socket is not None:
                    node_tree.links.new(from_socket, group_node_to_socket)

            for from_socket_name, to_socket, grouped_node_name in node_output_links:
                grouped_node = group.nodes[grouped_node_name]
                from_socket = grouped_node.outputs[from_socket_name]
                group_node_from_socket = None

                for link in group.links:
                    if link.from_socket == from_socket and link.to_socket.name in group_node.outputs:
                        group_node_from_socket = group_node.outputs[link.to_socket.name]
                        break

                if group_node_from_socket is not None:
                    node_tree.links.new(group_node_from_socket, to_socket)
        return {'FINISHED'}
