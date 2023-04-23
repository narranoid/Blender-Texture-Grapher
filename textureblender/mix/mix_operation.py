
from abc import ABC, abstractmethod
from textureblender.node_util import get_input_socket_object
from .socket_identity import SocketIdentity


class MixOperation:

    def __init__(self):
        pass

    @property
    def blending_socket_index(self):
        return -1

    @property
    def supports_blending(self):
        return self.blending_socket_index >= 0

    @property
    @abstractmethod
    def identifier(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def is_two_input_operation(self):
        pass

    @property
    @abstractmethod
    def is_recommended_for_blending(self):
        pass

    @property
    def enum_property_item(self):
        return self.identifier, self.name, self.description

    @abstractmethod
    def create_mixing_node(self, node_tree):
        pass

    def mix_sockets(self, sockets, node_tree):
        mixing_node = self.create_mixing_node(node_tree)
        source_socket_list = list(sockets)
        source_socket_index = 0

        for dest_socket in mixing_node.inputs:
            if source_socket_index == self.blending_socket_index:
                source_socket_index += 1
            if source_socket_index >= len(source_socket_list):
                break

            node_tree.links.new(source_socket_list[source_socket_index], dest_socket)
            source_socket_index += 1

        return mixing_node

