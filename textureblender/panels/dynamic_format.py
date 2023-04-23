
from bpy.types import Panel
from ..feature import ApplyImageSettingsFeature, FormatImageFeature, FormatNodeFeature


class DynamicFormatPanel(Panel):
    bl_label = "Format"
    bl_idname = 'FILE_PT_texture_grapher_dynamic_format'
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'

    @classmethod
    def poll(cls, context):
        operator = context.space_data.active_operator
        return operator is not None and (isinstance(operator, ApplyImageSettingsFeature)
                                         or isinstance(operator, FormatImageFeature)
                                         or isinstance(operator, FormatNodeFeature))

    def draw(self, context):
        operator = context.space_data.active_operator
        if operator is not None:
            layout = self.layout.column(align=True)
            if isinstance(operator, ApplyImageSettingsFeature):
                layout.prop(operator, 'apply_color_space', text='Color Spaces')
            if isinstance(operator, FormatImageFeature):
                layout.prop(operator, 'format_image_names', text='Image Names')
            if isinstance(operator, FormatNodeFeature):
                layout.prop(operator, 'format_node_names', text='Node Names')
                layout.prop(operator, 'format_node_labels', text='Node Labels')
                if operator.format_node_labels:
                    layout.prop(operator, 'short_labels', text='Short Labels')
