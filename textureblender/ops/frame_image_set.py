
from bpy.types import Operator

from .. import node_util as nu
from .. import blender_texture_characterizer as btc
from .. import util as string_util
from ..string_source import StringSource


class FrameImageSetOperator(Operator):

    bl_idname = "texture_grapher.frame_image_set"
    bl_label = "Frame Texture Set"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Texture Grapher"

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        nodes = nu.get_selected(node_tree.nodes)

        if len(nodes) > 0:
            texture_characterizer = btc.init_characterizer()
            name_characterize_source = string_util.get_best_source(nodes, [StringSource.IMAGE_NAME, StringSource.FILEPATH,
                                                                      StringSource.RAW_FILEPATH], StringSource.NAME)
            path_characterize_source = string_util.get_best_source(nodes, [StringSource.FILEPATH, StringSource.RAW_FILEPATH,
                                                                           StringSource.IMAGE_NAME], StringSource.NAME)

            name_set_char = texture_characterizer.characterize_image_nodes(nodes, name_characterize_source)
            path_set_char = texture_characterizer.characterize_image_nodes(nodes, path_characterize_source)
            set_char = name_set_char

            if len(path_set_char.texture_characterizations) >= len(name_set_char.texture_characterizations):
                set_char = path_set_char

            #set_char.apply_image_settings()
            format_source = string_util.get_best_source(nodes, [StringSource.FILEPATH, StringSource.RAW_FILEPATH,
                                                                StringSource.IMAGE_NAME], StringSource.NAME)

            set_char.frame_nodes_in_tree(node_tree, set_name=True, set_label=True, string_source=format_source)

        return {'FINISHED'}
