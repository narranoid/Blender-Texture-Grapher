
import bpy
from bpy.utils import register_class, unregister_class
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, IntProperty, PointerProperty, StringProperty
from bpy.types import NodeTree, PropertyGroup
from ..mix import ShaderMixColorOperation, ShaderMathOperation, ShaderVectorMathOperation, SocketIdentity


class MixNodesFeature:

    def get_all_blending_operations(self):
        return ShaderMixColorOperation.get_all_operations()

    def get_blending_operation(self, index):
        return self.get_all_blending_operations()[index]

    def create_mix_property_types(self, first_node, second_node):
        first_node_sockets = self.create_input_selection_items(first_node)
        second_node_sockets = self.create_input_selection_items(second_node)
        blending_operation_items = [op.enum_property_item for op in self.get_all_blending_operations()]

        NodeMixListEntry = type(
            "NodeMixListEntry",
            (PropertyGroup,),
            {
                "create_sockets": BoolProperty(name="Create sockets", default=True),
                "output_socket_name": StringProperty(name="Output socket name", default=""),
                "input_socket_first": EnumProperty(name="First input socket", items=first_node_sockets),
                "input_socket_first_name": StringProperty(name="First input socket name", default=""),
                "input_socket_second": EnumProperty(name="Second input socket", items=second_node_sockets),
                "input_socket_second_name": StringProperty(name="Second input socket name", default=""),
                "blending_operation": EnumProperty(name="Blending operation", items=blending_operation_items)
            })

        NodeMixList = type(
            "NodeMixList",
            (PropertyGroup,),
            {
                "mix_sockets": CollectionProperty(name="Mix sockets", type=NodeMixListEntry),
                "mix_node_name": StringProperty(name="Mix node name", default=""),
                "mix_node_label": StringProperty(name="Mix node label", default=""),
                #"node_tree": PointerProperty(name="Node tree", type=NodeTree),
                #"first_node": StringProperty(name="Name of first node", default=""),
                #"second_node": StringProperty(name="Name of second node", default=""),
                #"active_index": IntProperty(name="Active index", default=0),
                "use_custom_input_names": BoolProperty(name="Use custom input names", default=False)
            })

        return NodeMixList, NodeMixListEntry

    def mix_nodes(self, first_node, second_node, node_tree, mix_config):
        mix_group = bpy.data.node_groups.new("MixTest", "ShaderNodeGroup")
        mix_group_node = node_tree.nodes.new(mix_group.name)
        mix_group_input_node = None
        mix_group_output_node = None

        first_inputs = list()
        second_inputs = list()

        mix_nodes_with_blending = list()

        for mix_entry in mix_config.mix_sockets:
            first_socket_identity = SocketIdentity("", mix_entry.input_socket_first, "")
            first_node_socket = first_socket_identity.get_from_sockets(first_node.outputs, ignore_identifier=True, ignore_name=True)
            second_socket_identity = SocketIdentity("", mix_entry.input_socket_first, "")
            second_node_socket = first_socket_identity.get_from_sockets(second_node.outputs, ignore_identifier=True, ignore_name=True)

            blending_operation = self.get_blending_operation(mix_entry.blending_operation)

            first_mix_input = mix_group.inputs.new(first_node_socket.type, first_node_socket.name + " 1")
            second_mix_input = mix_group.inputs.new(second_node_socket.type, second_node_socket.name + " 2")

            first_mix_group_node_input_socket = mix_group_node.inputs[first_mix_input.identifier]
            second_mix_group_node_input_socket = mix_group_node.inputs[second_mix_input.identifier]

            first_mix_group_input_node_output_socket = mix_group_input_node.outputs[first_mix_input.identifer]
            second_mix_group_input_node_output_socket = mix_group_input_node.outputs[second_mix_input.identifer]

        fac_input = mix_group.inputs.new("float", "Fac")
        mix_group_node = node_tree.nodes.new("MixTest")
        input_index = 0

        while input_index < len(first_inputs):
            first_input = first_inputs[input_index]
            second_input = second_inputs[input_index]
            mix_config_entry = self.get_blending_operation(mix_config.mix_sockets[input_index])



            input_index += 1


        pass
        #TODO create new group
        #TODO create inputs for both nodes
        #TODO create outputs
        #TODO create mix / vector math / math nodes
        #TODO connect nodes inside of group
        #TODO place group node
        #TODO connect nodes outside of group

    def register_property_types(self, list_type, entry_type):
        register_class(entry_type)
        register_class(list_type)

    def unregister_property_types(self, list_type, entry_type):
        unregister_class(list_type)
        unregister_class(entry_type)

    def create_input_selection_items(self, node):
        input_items = list()
        current_index = 1

        for output in node.outputs:
            input_items.append((str(current_index), output.name, "", current_index))
            current_index += 1

        return input_items
