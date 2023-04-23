
import bpy
from ..texture.texture_characterization import TextureCharacterization
from .string_source import StringSource
from .util import get_string, contains_source, get_image

class BlenderTextureCharacterization(TextureCharacterization):

    def __init__(self, characterization_context, characteristic_group, affixable, file_path):
        super(BlenderTextureCharacterization, self).__init__(characterization_context, characteristic_group, affixable, file_path)
        self._images = set()
        self._shader_texture_nodes = set()
        self._aovs = set()
        self._aov_outputs = set()

        self._outer_group_sockets = list()
        self._inner_group_sockets = list()
        self._group_outputs = set()

    @property
    def images(self):
        return list(self._images)

    @property
    def image(self):
        for img in self._images:
            return img
        return None

    @property
    def shader_texture_nodes(self):
        return list(self._shader_texture_nodes)

    @property
    def shader_texture_node(self):
        for node in self._shader_texture_nodes:
            return node
        return None

    def get_nodes_in_tree(self, node_tree):
        nodes = list()
        for n in self.shader_texture_nodes:
            if n.name in node_tree.nodes:
                nodes.append(n)
        return nodes

    def get_node_in_tree(self, node_tree):
        for n in self.shader_texture_nodes:
            if n in node_tree.nodes:
                return n
        return None

    def add_image(self, image):
        self._images.add(image)

    def add_shader_texture_node(self, node, add_image=False):
        self._shader_texture_nodes.add(node)
        if add_image:
            self.add_image(node.image)

    def remove_image(self, image, remove_shader_texture_nodes=False):
        self._images.remove(image)
        if remove_shader_texture_nodes:
            nodes = list()
            for n in self._shader_texture_nodes:
                if n.image == image:
                    nodes.append(n)
            for n in nodes:
                self.remove_shader_texture_node(n, remove_image=False)

    def remove_shader_texture_node(self, node, remove_image=False):
        self._shader_texture_nodes.remove(node)
        if remove_image:
            self.remove_image(node.image, remove_shader_texture_nodes=False)

    def add_aov(self, aov):
        pass

    def add_aov_output(self, add_aov=False):
        pass

    def remove_aov(self, remove_aov_outputs=False):
        pass

    def remove_aov_output(self, remove_aov=False):
        pass

    def apply_image_settings(self, images=None):
        if images is None:
            images = self.images
        characteristics = self.characteristic_group
        if characteristics is not None:
            for img in images:
                img.colorspace_settings.name = characteristics.color_space

    def get_format_strings(self, string_provider, source, omit_characteristic_names=False):
        texture = None
        texture_set = None

        characteristic_group = self.characteristic_group
        if (source == StringSource.FILEPATH or source == StringSource.RAW_FILEPATH) and self.file_path:

            if self.file_path.startswith(self.affixable.prefix):
                texture_set = self.affixable.prefix
                texture = self.affixable.stem
            else:
                texture = self.file_path
        elif contains_source(string_provider, source):
            texture = get_string(string_provider, source)
        else:
            texture = get_string(string_provider, StringSource.NAME)

        if characteristic_group is not None and not omit_characteristic_names:
            texture = characteristic_group.first_name

        return texture, texture_set

    def format_images(self, source, names=False, images=None, omit_characteristic_names=False):
        if images is None:
            images = self.images
        for img in images:
            texture, texture_set = self.get_format_strings(img, source, omit_characteristic_names)
            if names:
                img.name = self.context.get_texture_image_name(texture, source, texture_set, source)

    def format_texture_nodes(self, source, names=False, labels=False, image_names=False, nodes=None, short_label=False,
                             omit_characteristic_names=False):
        if nodes is None:
            nodes = self.shader_texture_nodes
        for n in nodes:
            texture, texture_set = self.get_format_strings(n, source, omit_characteristic_names)
            if names:
                n.name = self.context.get_texture_node_name(texture, source, texture_set, source)
            if labels:
                if short_label:
                    n.label = self.context.get_texture_node_label(texture, source, None, None)
                else:
                    n.label = self.context.get_texture_node_label(texture, source, texture_set, source)
            if image_names:
                image = get_image(n)
                if image is not None:
                    image.name = self.context.get_texture_image_name(texture, source, texture_set, source)

    def create_shader_texture_node(self, nodes):
        stem = self.affixable.stem
        file_path = self.file_path
        add_image = False

        tex_node = nodes.new(type='ShaderNodeTexImage')
        #tex_node.label = self.source_characterizer.node_label_formatter.format_to_string(stem)
        #tex_node.name = self.source_characterizer.node_name_formatter.format_to_string(stem)

        if self.image is not None:
            tex_node.image = self.image
        elif file_path is not None:
            tex_node.image = bpy.data.images.load(file_path)
            add_image = True

        #characteristic_group = self.characteristic_group
        #print("Found char group: " + characteristic_group.first_name)

        #if characteristic_group is not None:
        #    tex_node.label = characteristic_group.first_name
        #    if tex_node.image is not None:
        #        tex_node.image.colorspace_settings.name = characteristic_group.color_space
        #        tex_node.image.name = characteristic_group.first_name
        #else:
        #    tex_node.label = self.source_characterizer.node_label_formatter.format_to_string(stem)
        #    if tex_node.image is not None:
        #        tex_node.image.name = self.source_characterizer.image_name_formatter.format_to_string(self.affixable.prefix)

        self.add_shader_texture_node(tex_node, add_image=add_image)
        return tex_node

    def add_node_group_output(self, group, nodes=None, output_node=None, omit_characteristic_names=False):
        if nodes is None:
            nodes = self.get_nodes_in_tree(group)

        if len(nodes) <= 0:
            return output_node

        output_input_index = len(group.outputs)
        if output_node is None:
            for n in group.nodes:
                if n.bl_idname == 'NodeGroupOutput':
                    output_node = n
                    break
            if output_node is None:
                output_node = group.nodes.new('NodeGroupOutput')

        for tex_node in nodes:
            output_type = 'NodeSocketColor' \
                if self.characteristic_group is None or self.characteristic_group.channels > 1 \
                else 'NodeSocketFloat'
            output_name = self.characteristic_group.first_name \
                if self.characteristic_group is not None and not omit_characteristic_names \
                else tex_node.label

            group_output = group.outputs[output_name] if output_name in group.outputs \
                else group.outputs.new(output_type, output_name)
            self._group_outputs.add(group_output)
            group.links.new(output_node.inputs[output_input_index], tex_node.outputs['Color'])
            self.add_inner_group_socket(output_node.inputs[output_input_index])
            output_input_index += 1

        return output_node

    def get_nodes_in_list(self, nodes):
        tex_nodes = list()
        for n in nodes:
            if n in self.shader_texture_nodes:
                tex_nodes.append(n)
        return tex_nodes

    def create_images(self):
        pass

    @property
    def inner_group_sockets(self):
        return list(self._inner_group_sockets)

    @property
    def inner_group_socket(self):
        return self.inner_group_socket[0]

    @property
    def outer_group_sockets(self):
        return list(self._outer_group_sockets)

    @property
    def outer_group_socket(self):
        return self.outer_group_sockets[0]

    def add_inner_group_socket(self, socket):
        self._inner_group_sockets.append(socket)

    def add_outer_group_socket(self, socket):
        self._outer_group_sockets.append(socket)

    def get_outer_group_socket_from_inner(self, group_node):
        pass

    #def get_inner_group_socket_from_outer(self, ):

