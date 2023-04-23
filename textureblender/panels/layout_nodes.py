
from bpy.types import Panel
from bpy_extras.io_utils import ImportHelper

from ..feature import LayoutNodesFeature


class LayoutNodesFileBrowserPanel(Panel):
    bl_label = "Layout Nodes"
    bl_idname = 'FILE_PT_texture_grapher_organize_nodes'
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'

    @classmethod
    def poll(cls, context):
        operator = context.space_data.active_operator
        return operator is not None and isinstance(operator, LayoutNodesFeature) and isinstance(operator, ImportHelper)

    def draw(self, context):
        operator = context.space_data.active_operator
        if operator is not None and isinstance(operator, LayoutNodesFeature):
            layout = self.layout.column(align=True)
            operator.draw_layout_nodes(context, operator, layout)


