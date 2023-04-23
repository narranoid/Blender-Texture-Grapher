
from ..enums import MixBlendingMode
from .internal_node_mix_operation import InternalNodeMixOperation


class ShaderMixColorOperation(InternalNodeMixOperation):

    @staticmethod
    def get_all_operations():
        # Description sources:
        # https://en.wikipedia.org/wiki/Blend_modes
        # https://docs.blender.org/manual/en/latest/render/shader_nodes/color/mix.html
        # https://photoshoptrainingchannel.com/blending-modes-explained/
        return [
            ShaderMixColorOperation(MixBlendingMode.MIX, "Mix", "Alpha blending using Fac as alpha."),

            ShaderMixColorOperation(MixBlendingMode.DARKEN, "Darken", "Keeps the darker color of the two."),
            ShaderMixColorOperation(MixBlendingMode.MULTIPLY, "Multiply", "Multiplies the two colors (darker image)."),
            ShaderMixColorOperation(MixBlendingMode.COLOR_BURN, "Color Burn", "Divides the inverted first color by the second color, and then inverts the result."),

            ShaderMixColorOperation(MixBlendingMode.LIGHTEN, "Lighten", "Keeps the brighter color of the two."),
            ShaderMixColorOperation(MixBlendingMode.SCREEN, "Screen", "Inverts colors, multiplies them, then inverts again (brighter image)."),
            ShaderMixColorOperation(MixBlendingMode.COLOR_DODGE, "Color Dodge", "Decreases the contrast between the colors."),
            ShaderMixColorOperation(MixBlendingMode.ADD, "Add", "Adds values of one color with the other."),

            ShaderMixColorOperation(MixBlendingMode.OVERLAY, "Overlay", "Dark areas become darker, bright ares become brighter."),
            ShaderMixColorOperation(MixBlendingMode.SOFT_LIGHT, "Soft Light", "Dark areas become darker, bright ares become brighter, but in a more subtle way than Overlay."),
            ShaderMixColorOperation(MixBlendingMode.LINEAR_LIGHT, "Linear Light", "Sum of the first color and twice the second color, subtract 1."),

            ShaderMixColorOperation(MixBlendingMode.DIFFERENCE, "Difference", "Subtracts the first color from the second color."),
            ShaderMixColorOperation(MixBlendingMode.SUBTRACT, "Subtract", "Sums the value in the two colors and subtracts 1."),
            ShaderMixColorOperation(MixBlendingMode.DIVIDE, "Divide", "Divides pixel values of one color with the other."),

            ShaderMixColorOperation(MixBlendingMode.HUE, "Hue", "Uses hue of the second color as hue for the first color."),
            ShaderMixColorOperation(MixBlendingMode.SATURATION, "Saturation", "Uses saturation of the second color as saturation for the first color."),
            ShaderMixColorOperation(MixBlendingMode.COLOR, "Color", "Uses hue and saturation of the second color as hue and saturation for the first color."),
            ShaderMixColorOperation(MixBlendingMode.VALUE, "Value", "Uses value of the second color as value for the first color.")
        ]

    def __init__(self, blend_type, name, description):
        super(ShaderMixColorOperation, self).__init__(blend_type.name, name, description, "ShaderNodeMixRGB", 0)

    @property
    def blend_type(self):
        return MixBlendingMode[self.identifier]

    @property
    def is_two_input_operation(self):
        return self.blend_type in [
            MixBlendingMode.MIX,

            MixBlendingMode.DARKEN,
            MixBlendingMode.MULTIPLY,
            MixBlendingMode.COLOR_BURN,

            MixBlendingMode.LIGHTEN,
            MixBlendingMode.SCREEN,
            MixBlendingMode.COLOR_DODGE,
            MixBlendingMode.ADD,

            MixBlendingMode.OVERLAY,
            MixBlendingMode.SOFT_LIGHT,
            MixBlendingMode.LINEAR_LIGHT,

            MixBlendingMode.DIFFERENCE,
            MixBlendingMode.SUBTRACT,
            MixBlendingMode.DIVIDE,

            MixBlendingMode.HUE,
            MixBlendingMode.SATURATION,
            MixBlendingMode.COLOR,
            MixBlendingMode.VALUE
        ]

    @property
    def is_recommended_for_blending(self):
        return True

    def create_mixing_node(self, node_tree):
        mixing_node = super(ShaderMixColorOperation, self).create_mixing_node(node_tree)
        mixing_node.blend_type = self.identifier
        return mixing_node
