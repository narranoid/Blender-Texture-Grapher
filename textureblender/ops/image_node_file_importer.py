
from bpy.props import BoolProperty

from . import FileImporter, FileImporterMeta
from .. import blender_texture_characterizer as btc, node_util as nu
from ..feature import LayoutNodesFeature, OptionalHideNodesFeature, ApplyImageSettingsFeature, FormatImageNodeFeature
from ..string_source import StringSource

class ImageNodeFileImporter(FileImporter, LayoutNodesFeature, OptionalHideNodesFeature, ApplyImageSettingsFeature, FormatImageNodeFeature,
                            filter_glob_default='*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp',
                            directory_name='Directory',
                            directory_description='Folder to search in for image files',
                            directory_default=''):

    bl_idname = "texture_grapher.image_node_file_import"
    bl_label = "Import Texture Set"

    frame_nodes_option: BoolProperty(
        name='Frame Nodes',
        description='Frame the nodes',
        default=False
    )

    group_nodes_option: BoolProperty(
        name='Group Nodes',
        description='Group the nodes',
        default=True
    )

    def draw(self, context):
        layout = self.layout.column(align=True)
        layout.prop(self, 'hide_nodes_option')
        layout.prop(self, 'frame_nodes_option')
        layout.prop(self, 'group_nodes_option')

    def on_valid_files_selected(self, context):
        node_tree = context.space_data.edit_tree
        nodes = node_tree.nodes

        texture_characterizer = btc.init_characterizer()
        set_char = texture_characterizer.characterize(self.file_paths)

        frame_nodes = self.frame_nodes_option #bool(clustering & NodeClustering.FRAME)
        group_nodes = self.group_nodes_option #bool(clustering & NodeClustering.GROUP)

        view_center = context.space_data.edit_tree.view_center

        if group_nodes:
            group = set_char.create_shader_texture_group(frame_nodes)
            tex_nodes = set_char.get_nodes_in_tree(group)

            group_node = nodes.new("ShaderNodeGroup")
            group_node.node_tree = group
            group_width = nu.get_width(group_node)
            group_height = nu.get_height(group_node)
            group_node.location = (view_center[0] - (group_width * 0.5), view_center[1] + (group_height * 0.5))

            self.hide_nodes_optional(tex_nodes)
            self.layout_nodes(context, tex_nodes, center=(0, 0))
            nu.layout_input_output_nodes(group)
        else:
            tex_nodes = set_char.create_shader_texture_nodes(nodes, frame_nodes)

            self.hide_nodes_optional(tex_nodes)
            self.layout_nodes(context, tex_nodes, center=view_center)

        # Formatting
        self.apply_image_settings_to_set(set_char)
        self.format_image_nodes_of_set(set_char, StringSource.FILEPATH)

        return {'FINISHED'}
