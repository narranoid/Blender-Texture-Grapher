
from bpy.props import BoolProperty

from .. import node_util as nu
from .. import util as su
from ..blender_texture_characterizer import init_characterizer

class ConnectNodesFeature:

    override_existing_links: BoolProperty(
        name='Override Existing Links',
        description='Override already connected input links.',
        default=False
    )

    def try_connect_sockets(self, node_tree, from_node, from_socket, to_node, to_socket):
        from_name = su.get_qualified_socket_input_name(from_node, from_socket)
        to_name = su.get_qualified_socket_output_name(to_node, to_socket)



        characterizer = init_characterizer()
        characteristic_group_from = characterizer.get_characteristic_group_safe(from_name)
        characteristic_group_to = characterizer.get_characteristic_group_safe(to_name)

        if characteristic_group_from == characteristic_group_to:
            if self.override_existing_links or not to_socket.is_linked:
                node_tree.links.new(from_socket, to_socket, verify_limits=False)
            return True

        return False


    def connect_nodes(self, node_tree, from_nodes, to_nodes):
        #outputs = [outs for node in from_nodes for outs in node.outputs]
        #inputs = [ins for node in to_nodes for ins in node.inputs]

        connected_to_sockets = list()

        for from_node in from_nodes:
            for from_socket in from_node.outputs:
                for to_node in to_nodes:
                    for to_socket in to_node.inputs:
                        if to_socket not in connected_to_sockets and \
                                self.try_connect_sockets(node_tree, from_node, from_socket, to_node, to_socket):
                            connected_to_sockets.append(to_socket)
                            if len(connected_to_sockets) >= len(to_node.inputs):
                                return


        #self.connect_sockets(node_tree, outputs, inputs, override_existing_links)

    def connect_active_to_selected(self, node_tree, nodes=None):
        if nodes is None:
            nodes = node_tree.nodes

        selected = nu.get_selected(nodes)
        active = node_tree.nodes.active

        self.connect_nodes(node_tree, [active], selected)

    def connect_selected_to_active(self, node_tree, nodes=None):
        if nodes is None:
            nodes = node_tree.nodes

        selected = nu.get_selected(nodes)
        active = node_tree.nodes.active

        self.connect_nodes(node_tree, selected, [active])
