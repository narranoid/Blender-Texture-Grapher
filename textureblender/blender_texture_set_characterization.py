
from ..texture.texture_set_characterization import TextureSetCharacterization
import bpy
from . import node_util


class BlenderTextureSetCharacterization(TextureSetCharacterization):

    def __init__(self, characterization_context, characteristic_group, texture_characterizations):
        super(BlenderTextureSetCharacterization, self).__init__(characterization_context, characteristic_group, texture_characterizations)

    def create_shader_texture_nodes(self, nodes, frame_nodes=False):
        tex_nodes = list()
        for tex_char in self.texture_characterizations:
            tex_nodes.append(tex_char.create_shader_texture_node(nodes))

        if frame_nodes and len(tex_nodes) > 0:
            self.frame_nodes(tex_nodes, nodes)

        return tex_nodes

    def frame_nodes_in_tree(self, node_tree, set_name=False, set_label=False, string_source=None):
        nodes_to_frame = self.get_nodes_in_tree(node_tree)
        return self.frame_nodes(nodes_to_frame, node_tree.nodes, set_name, set_label, string_source)

    def frame_nodes(self, frame_nodes, nodes, set_name=False, set_label=False, string_source=None):
        frame = node_util.frame_nodes(frame_nodes, nodes)
        format_string = self.affixed_group.prefix
        from .string_source import StringSource

        if set_name:
            frame.name = self.context.get_texture_set_node_name(format_string, string_source)
        if set_label:
            frame.label = self.context.get_texture_set_node_label(format_string, string_source)

        return frame

    def get_nodes_in_tree(self, node_tree):
        node_list = list()
        for tex_char in self.texture_characterizations:
            tex_nodes = tex_char.get_nodes_in_tree(node_tree)
            node_list += tex_nodes
        return node_list

    def _get_input_output_nodes(self, group):
        group_input_node = node_util.get_node_with_type(group.nodes, 'NodeGroupInput')
        if group_input_node is None:
            group_input_node = group.nodes.new('NodeGroupInput')

        group_output_node = node_util.get_node_with_type(group.nodes, 'NodeGroupOutput')
        if group_output_node is None:
            group_output_node = group.nodes.new('NodeGroupOutput')

        return group_input_node, group_output_node

    def create_nodes_in_group(self, group, add_inputs=False, add_outputs=False, omit_characteristic_names=False):
        tex_characterizations = self.texture_characterizations
        group_input_node, group_output_node = self._get_input_output_nodes(group)

        group.inputs.new('NodeSocketVector', 'Vector')

        tex_nodes = list()
        for tex_char in tex_characterizations:
            tex_node = tex_char.create_shader_texture_node(group.nodes)
            group.links.new(group_input_node.outputs[0], tex_node.inputs['Vector'])
            if add_outputs:
                tex_char.add_node_group_output(group, nodes=[tex_node], output_node=group_output_node,
                                               omit_characteristic_names=omit_characteristic_names)
            tex_nodes.append(tex_node)
        return tex_nodes

    def setup_nodes_in_group(self, group, omit_characteristic_names=False):
        tex_characterizations = self.texture_characterizations
        group_input_node, group_output_node = self._get_input_output_nodes(group)

        group.inputs.new('NodeSocketVector', 'Vector')

        for tex_char in tex_characterizations:
            tex_nodes = tex_char.get_nodes_in_tree(group)
            for tex_node in tex_nodes:
                group.links.new(group_input_node.outputs[0], tex_node.inputs['Vector'])
            tex_char.add_node_group_output(group, nodes=tex_nodes, output_node=group_output_node,
                                           omit_characteristic_names=omit_characteristic_names)

    def create_shader_texture_group(self, frame_nodes=False, node_group_type='ShaderNodeTree'):
        group_name = self.context.node_group_name_formatter.format_to_string(self.affixed_group.prefix)
        group = bpy.data.node_groups.new(group_name, node_group_type)
        tex_nodes = self.create_nodes_in_group(group, add_inputs=True, add_outputs=True)

        if frame_nodes and len(tex_nodes) > 0:
            self.frame_nodes(tex_nodes, group.nodes)

        return group

    def apply_image_settings(self):
        for char in self.texture_characterizations:
            char.apply_image_settings()

    def group_nodes(self, node_tree, nodes=None, set_group_node_active=False, select_group_node=False,
                    select_nodes_in_group=False, enter_group=False):
        if not nodes:
            nodes = self.get_nodes_in_tree(node_tree)
        if len(nodes) <= 0:
            return None

        previous_selection = node_util.get_selected(node_tree.nodes)
        previous_active = node_tree.nodes.active
        group = None
        group_node = None

        try:
            node_util.select_nodes(previous_selection, select=False)
            node_util.select_nodes(nodes, select=True)

            bpy.ops.node.group_make()
            group_node = node_tree.nodes.active
            group = group_node.node_tree

            format_string = self.affixed_group.prefix
            from .string_source import StringSource
            group_node.name = self.context.get_texture_set_node_name(format_string, StringSource.FILEPATH) #self.context.node_name_formatter.format_to_string(format_string)
            group_node.label = self.context.get_texture_set_node_label(format_string, StringSource.FILEPATH)
            group.name = self.context.get_texture_set_node_group_name(format_string, StringSource.FILEPATH) #self.context.node_group_name_formatter.format_to_string(format_string)

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
                node_util.select_nodes(nodes, select=False)
            if previous_selection:
                for prev_sel in previous_selection:
                    if group is None or prev_sel.name not in group.nodes:
                        prev_sel.select = True

            # make new selection and restore active node
            if group is not None:
                node_util.select_nodes(group.nodes, select=select_nodes_in_group)
            if group_node is not None:
                group_node.select = select_group_node
                if set_group_node_active:
                    node_tree.nodes.active = group_node
                elif previous_active is not None and previous_active.name not in group.nodes:
                    node_tree.nodes.active = previous_active
            elif previous_active is not None and previous_active.name not in group.nodes:
                node_tree.nodes.active = previous_active

        return group_node

