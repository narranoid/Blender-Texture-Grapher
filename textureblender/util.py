
from .string_source import StringSource
import bpy
from . import node_util


def get_strings(providers, source):
    strings = list()
    for provider in providers:
        strings.append(get_string(provider, source))
    return strings


def get_string(string_provider, source):
    if source == StringSource.NAME and string_provider.name:
        return string_provider.name
    elif source == StringSource.LABEL and string_provider.label:
        return string_provider.label

    img = get_image(string_provider)

    if img is not None:
        if source == StringSource.IMAGE_NAME:
            return img.name
        elif source == StringSource.FILEPATH or source == StringSource.RAW_FILEPATH:
            filepath = get_filepath(img, source == StringSource.RAW_FILEPATH)
            if filepath:
                return filepath

    return ""


def get_image(image_provider):
    if isinstance(image_provider, bpy.types.Image):
        return image_provider
    elif isinstance(image_provider, bpy.types.Texture):
        return get_image_from_texture(image_provider)
    elif hasattr(image_provider, 'texture'):
        return get_image_from_texture(image_provider.texture)
    elif hasattr(image_provider, 'image'):
        return image_provider.image
    return None


def get_image_from_texture(texture):
    if texture.use_nodes:
        node = node_util.get_node_with_type(texture.node_tree.nodes, 'TextureImageNode')
        return node.image
    elif str(texture.type).upper() == 'IMAGE':
        return texture.image
    return None


def is_external(image):
    return image.packed_file is None


def get_filepath(image, prefer_raw_filepath):
    if prefer_raw_filepath:
        return image.filepath_raw if image.filepath_raw else image.filepath
    return image.filepath if image.filepath else image.filepath_raw


def contains_source(string_provider, source):
    if source == StringSource.NAME and hasattr(string_provider, 'name'):
        return True
    elif source == StringSource.LABEL and hasattr(string_provider, 'label'):
        return True
    elif hasattr(string_provider, 'image') or isinstance(string_provider, bpy.types.Image):
        img = string_provider if isinstance(string_provider, bpy.types.Image) else string_provider.image
        if source == StringSource.IMAGE_NAME and hasattr(img, 'name'):
            return True
        elif source == StringSource.FILEPATH \
                and (hasattr(img, 'filepath') or hasattr(img, 'filepath_raw')) \
                and (not isinstance(img, bpy.types.Image) or is_external(img)):
            return True
    return False


def all_contain_source(string_providers, source):
    for string_provider in string_providers:
        if not contains_source(string_provider, source):
            return False
    return True


def get_best_source(string_providers, source_list, fallback_source):
    for source in source_list:
        if all_contain_source(string_providers, source):
            return source
    return fallback_source


def get_by_string(collection, string, source):
    for string_provider in collection:
        if source == StringSource.NAME and string_provider.name == string\
                or source == StringSource.LABEL and string_provider.label == string:
            return string_provider
        elif hasattr(string_provider, 'image') or isinstance(string_provider, bpy.types.Image):
            img = string_provider if isinstance(string_provider, bpy.types.Image) else string_provider.image
            if source == StringSource.IMAGE_NAME and img.name == string:
                return string_provider
            elif source == StringSource.FILEPATH or source == StringSource.RAW_FILEPATH:
                filepath = get_filepath(img, source == StringSource.RAW_FILEPATH)
                if filepath == string:
                    return string_provider
    return None


def get_qualified_socket_input_name(node, socket):
    return socket.name


def get_qualified_socket_output_name(node, socket, image_source=None, ao_name="Ambient Occlusion"):
    if isinstance(socket, int) or isinstance(socket, str):
        socket = node.outputs[socket]

    # Special shader nodes
    if node.bl_idname == 'ShaderNodeVertexColor':
        return node.layer_name
    elif node.bl_idname == 'ShaderNodeAttribute':
        return node.attribute_name
    elif node.bl_idname == 'ShaderNodeAmbientOcclusion':
        return ao_name
    elif node.bl_idname == 'ShaderNodeImageTexture' and image_source is not None:
        return get_string(node, image_source)

    # Special compositor nodes
    elif node.bl_idname == 'CompositorNodeTexture':
        return node.texture.name
    elif node.bl_idname == 'CompositorNodeImage' and image_source is not None:
        return get_string(node, image_source)

    return socket.name
