
from bpy.props import BoolProperty


class FormatNodeFeature:
    format_node_names: BoolProperty(
        name='Format Node Name',
        description='Automatically set node names.',
        default=True
    )

    format_node_labels: BoolProperty(
        name='Format Node Label',
        description='Automatically set node labels.',
        default=True
    )

    short_labels: BoolProperty(
        name='Short Labels',
        description='Exclude texture set name from labels?',
        default=True
    )
