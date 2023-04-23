
from .mix_operation import MixOperation


class InternalNodeMixOperation(MixOperation):

    def __init__(self, identifier, name, description, node_bl_idname, blending_socket_index=-1):
        super(InternalNodeMixOperation, self).__init__()
        self._identifier = identifier
        self._name = name
        self._description = description
        self._node_bl_idname = node_bl_idname
        self._blending_socket_index = blending_socket_index

    @property
    def identifier(self):
        return self._identifier

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def blending_socket_index(self):
        return self._blending_socket_index

    def create_mixing_node(self, node_tree):
        return node_tree.nodes.new(self._node_bl_idname)
